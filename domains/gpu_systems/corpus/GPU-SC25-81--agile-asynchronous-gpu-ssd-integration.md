# GPU-SC25-81 — AGILE: Lightweight and Efficient Asynchronous GPU-SSD Integration

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `E GPU–storage and GPU–host I/O paths`
secondary_topics: `E HBM & data movement; GPU-initiated control`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv abs 2504.19365 (abstract, authors) + arXiv HTML v3 (arxiv.org/html/2504.19365v3) read across introduction/background, the deadlock analysis, the asynchronous API, the submission/doorbell protocol, the CQ-polling service, the software cache hierarchy, the Share Table, register-usage discussion, evaluation setup, results, limitations and related work. Plus artifact inspection of github.com/arc-research-lab/AGILE @ c644255b45f345fcd3c178159ab277ece2cb1d3d. (v1 HTML returns 404; v3 is the current version.)`

## 12.1 Bibliographic facts
- Title: *AGILE: Lightweight and Efficient Asynchronous GPU-SSD Integration* `[paper]` `[README]`.
- Authors `[paper]` `[README]`: Zhuoping Yang, Jinming Zhuang, Xingzhen Chen, Alex K. Jones, Peipei Zhou. (Affiliations are not printed in the fetched HTML rendering — `UNKNOWN`; the artifact lives under the `arc-research-lab` GitHub organisation.)
- Venue: **SC 2025**, DOI `10.1145/3712285.3759778`, pp. 1028–1042 `[census]`; the artifact's own BibTeX confirms `booktitle = {Proceedings of the International Conference for High Performance Computing, Networking, Storage, and Analysis, SC 2025}` `[README]`.
- arXiv 2504.19365 (v3 read; v1 HTML 404s).
- Artifact `[artifact]`: `github.com/arc-research-lab/AGILE` @ `c644255b45f345fcd3c178159ab277ece2cb1d3d`. A substantial tree: `driver/` (custom NVMe and GPU kernel drivers for Linux 6.8.0 and 6.17.0, plus a vendored GDRCopy), `include/` (23 headers, the device-side library), `baseline/`, `benchmarks/`, `experiments/`, `demo/`, `tutorial/`.
- Publication type: `ARCHIVAL_MAIN_PAPER`; the read source is the `PREPRINT`.

## 12.2 Core question (one sentence)
GPU-centric NVMe access lets a GPU thread issue a storage request without the CPU, but every existing such system is **synchronous** — so can it be made asynchronous, which requires solving a deadlock that arises specifically from GPU threads holding submission-queue locks while stalled? `[paper]`

## 12.3 GPU/HPC problem translation
- **Compute**: the point of the work is to let compute proceed while I/O is outstanding — latency hiding at thread granularity.
- **Memory**: an **HBM-resident software cache** is the staging structure; GPU BAR1 memory is the DMA target for peer-to-peer SSD transfers `[README]`.
- **Synchronization**: the centre of gravity. The paper's contribution is a lock protocol that cannot deadlock, plus a device-resident completion service.
- **Communication**: GPU ↔ NVMe SSD over PCIe, peer-to-peer, with no CPU in the data path.
- **Scheduling**: a persistent GPU kernel daemon polls completion queues round-robin.

## 12.4 Why the problem exists
Root causes the paper names `[paper]`:
1. **GPUDirect Storage and DeepNVMe keep the CPU in the control path.** They "still require the CPU to initiate the data transfer", causing "frequent synchronization between the GPU and the host CPU" and "significant performance degradation". This is the precise limitation of the GDS model.
2. **BaM removes the CPU but is synchronous.** BaM lets GPU threads issue NVMe commands directly, but uses a "synchronous access model, and threads must wait for the I/O requests to be completed before concurrently starting computation".
3. **The obvious fix — make it asynchronous — deadlocks, for a GPU-specific reason.** The paper's worked example:
   - Thread-1 locks an SQ entry and places a read request;
   - Thread-2 fills the remaining SQ entries, so the SQ becomes full;
   - both threads stall waiting for a free entry;
   - neither reaches the completion-checking code that would release the locks;
   - "Even though the corresponding completions become available in the CQ, if Threads-1 and 2 own all the occupied SQ entries, none can be released."

   The hardware root cause is that on a GPU the thread that submitted a request is also the thread expected to reap it, and threads cannot yield — there is no preemptive scheduler to run the reaper. A CPU thread blocking on I/O is descheduled; a GPU warp spinning on a full queue occupies its slot forever.
4. **A second deadlock class in the software cache**, when "simultaneous threads accessing multiple cache lines" hold locks while awaiting eviction of other lines — the classic lock-ordering deadlock, but again unrecoverable because nothing can preempt.

## 12.5 Mathematical / performance model
`NOT_IN_PAPER` as a closed-form model. The quantitative structures are `[paper]`:
- **Warp-centric CQ polling (Algorithm 1)**: 32 CQEs processed per warp iteration, one CQE per thread, using an NVMe **phase-bit** comparison, with a **32-bit mask** tracking completion; the warp updates the CQ doorbell only when all 32 bits are set, then rotates round-robin to the next registered CQ.
- **NVMe Command Identifier (CID), 16 bits**, used to map completions back to requests.
- **SQE state machine**: the paper describes **three** states — `EMPTY`, `UPDATED`, `ISSUED`. **The code has five** (see 12.8) — recorded as a paper/code discrepancy, not reconciled.
- **Cache-line state machine**: four states — `INVALID`, `BUSY`, `READY`, `MODIFIED`.

## 12.6 Data layout and ownership
- **thread → SQ entry**: a user thread attempts to claim an SQE, writes the command, and then **hands the lock-SQE off to the AGILE service, receiving back a barrier object** representing the transaction's status `[paper]`. Ownership of the SQE therefore transfers from the submitter to the daemon — this transfer is what breaks the deadlock.
- **warp → CQ**: "Each warp is assigned a specific CQ" and each thread in it checks one CQE `[paper]`. Confirmed at `[code]`: `class AgileCQ` carries per-warp fields commented `// used in a warp`: `unsigned int pos_offset; unsigned int mask;` (`include/agile_nvme.h:18-34`).
- **doorbell**: serialised under a lock, because "concurrent writes to the same doorbell registers" would "cause inconsistent SQ tail values in SSDs" `[paper]`. The doorbell is a single MMIO register shared by thousands of threads — the one truly serial resource in the design.
- **cache line → HBM**: the software cache is HBM-resident; cache-line ownership is per-line with an explicit lock chain (`AgileLockChain`, threaded through every device-side call) `[code]`.
- **user buffer → Share Table**: an optional hashtable tracks ownership of user-specified buffers under "a software-managed coherency protocol inspired by the **MOESI** model", with reference counters and exclusive ownership grants `[paper]`.
- **GPU → SSD**: transfers land in **GPU BAR1 memory**, which the artifact's install instructions require be enlarged from its typical 128 MB default via the NVIDIA Display Mode Selector Tool, with **IOMMU disabled** `[README]`.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only names printed in the paper `[paper]` or read in the artifact `[code]`:
```
# ---- user thread, asynchronous submit ----
AgileLockChain chain;
attemptEnqueue(cmd_type, table_idx, device_type, ssd_blk_idx, blocks, phy_addr, &chain)   # [code]
    -> claim an SQE, write the command, set cmd_status EMPTY -> PROCESSING -> READY        # [code]
attemptSQDB(&chain)                                                                        # [code]
    -> acquire the doorbell lock
    -> scan SQEs, transition READY -> ISSUSING -> ISSUED                                   # [code]
    -> write the SQ tail doorbell register
    -> release the doorbell lock
# thread does NOT wait here; it holds an AgileBufPtr barrier and goes on computing
... compute ...
bufptr.wait()                      # [code] AgileBufPtr::wait / AgileBuf::wait

# ---- AGILE service: a persistent GPU kernel daemon, warp-centric ----
for each registered CQ, round-robin:
    each lane examines one CQE:
        ready = ((cpl[3] >> 16) & 0x1) != cq.phase        # NVMe phase bit   [code]
    mask = __ballot_sync(0xFFFFFFFF, processed)           # [code]
    if all 32 processed:
        cq.phase = (~cq.phase) & 0x1                      # phase flip       [code]
        ring the CQ doorbell
    map CID -> transaction; release the SQ lock; signal the waiting thread's barrier
```

## 12.8 Real implementation
Artifact `github.com/arc-research-lab/AGILE` @ `c644255b45f345fcd3c178159ab277ece2cb1d3d` `[code]`. Symbols read, not inferred:
- `include/agile_nvme.h` — `class AgileCQ` (`:18`) with `volatile unsigned int * data; volatile unsigned int * cqdb; unsigned int pos; unsigned int phase; unsigned int depth;` and the warp fields `pos_offset`, `mask`; `class AgileSQ` (`:73`) with `__device__ void attemptSQDB(AgileLockChain*)` (`:173`) and `__device__ bool attemptEnqueue(unsigned int cmd_type, unsigned int table_idx, unsigned int device_type, SSDBLK_TYPE ssd_blk_idx, unsigned int blocks, unsigned long phy_addr, AgileLockChain* chain)` (`:214`); `class AgileQueuePair` (`:312`), `class AgilePollingList` (`:332`), `class AgileNvmeDev : public AGILE_Kernel_TEMP<AgileNvmeDev>` (`:338`) with `__device__ void issueRead(...)` (`:359`) and `__device__ void issueWrite(...)` (`:378`); a spin helper `__device__ void wati_status(unsigned int* cmd_status, unsigned int expected, unsigned int target)` (`:67`) — the typo is in the source.
- **SQE states, from the code** (`include/agile_nvme.h:60-64`): `AGILE_CMD_STATUS_EMPTY 0`, `AGILE_CMD_STATUS_PROCESSING 1`, `AGILE_CMD_STATUS_READY 2`, `AGILE_CMD_STATUS_ISSUSING 3`, `AGILE_CMD_STATUS_ISSUED 4`. **Five states, against the paper's three (`EMPTY`/`UPDATED`/`ISSUED`).** The extra `PROCESSING` and `ISSUSING` states are intermediate states used by the two `wati_status` spin calls at `:237` (`EMPTY → PROCESSING`) and `:300` (`ISSUSING → ISSUED`). Recorded as a discrepancy; the code is authoritative for implementation detail per `governance/SOURCE_EVIDENCE_RULES.md`.
- `include/agile_ctrl.tpp` — the completion service. NVMe phase-bit test read verbatim at `:168` and `:315`: `((cpl[3] >> 16) & 0x1) == this->list->pairs[queue_idx].cq.phase`; phase flip at `:187` and `:385`: `cq.phase = (~cq.phase) & 0x1`. Warp collectives: `__ballot_sync(0xFFFFFFFF, 1)` at `:262,278,297,403`, `__ballot_sync(0xFFFFFFFF, processed)` at `:379`, `__shfl_sync(0xFFFFFFFF, stop_sig, 0)` at `:408` (broadcasting the daemon's stop signal from lane 0), `__activemask()` at `:504,664`, `__shfl_sync(mask, gpu_cache_idx, master)` at `:521` and `__shfl_sync(eq_mask, gpu_cache_idx, master_id)` at `:710`, and `__popc(eq_mask)` at `:690,706` counting cache hits per warp.
- `include/agile_swcache.h` — `class AgileCacheBase` (`:19`) with `acquireBaseLock_lockStart`, `acquireBaseLockAttempt_lockStart`, `releaseBaseLock_lockEnd`, all taking `AgileLockChain*`; `class GPUCacheBase_T : public AgileCacheBase` (`:53`) with an `_inLockArea` naming convention on every state predicate (`getStatus_inLockArea`, `checkErasable_inLockArea`, `readReadyCheck_inLockArea`, `writableCheck_inLockArea`, `processingReading_inLockArea`, `finishWriting_inLockArea`, `isModified_inLockArea`, …) and `notifyEvict_inLockArea`, `appendAgileBuf_inLockArea`, `propagateAgileBuf_inLockArea`. The CRTP the paper describes is visible in the template signature `template <typename GPUCacheImpl, typename CPUCacheImpl, typename ShareTableImpl> class AgileCtrl;`.
- `include/agile_buf.h` — `class AgileBuf` (`:15`) with `incReference`/`decReference` (`:65,69`), `checkHit(NVME_DEV_IDX_TYPE, SSDBLK_TYPE)` (`:85`), `setTag`, `setModified`, `ready`, `setProcessingRead`, `moveData`, `propagateData`, `wait()` (`:172`); and `class AgileBufPtr` (`:188`) with host/device constructors and `wait()` (`:211`). `AgileBufPtr` is the "barrier" the paper says the user thread receives.
- **Environment requirements, from the artifact's own install guide** `[README]`: GPU **BAR1 memory must be enlarged** beyond the typical 128 MB default because "AGILE relies on the GPUs' BAR1 Memory as the source and destination in GPU-SSD peer-to-peer communication"; **IOMMU must be disabled** (`intel_iommu=off`); the NVIDIA driver kernel symbols must be rebuilt; custom `agile_gpu` and `agile_nvme` kernel modules must be inserted; a **vendored modified GDRCopy** is included. This is a heavyweight, root-privileged, kernel-modifying deployment.

## 12.9 Kernel execution
- **kernels**: at least two concurrent kernel populations — the application's compute kernels (which call the device-side AGILE API) and a **persistent "lightweight kernel daemon"** that polls all registered CQs "in a non-blocking fashion" `[paper]`. The daemon's stop signal is broadcast from lane 0 via `__shfl_sync` `[code]`.
- **thread block**: not specified by the paper for the daemon — `UNKNOWN`.
- **warp**: the central unit. One warp owns one CQ; one lane owns one CQE; completion status is aggregated into a `__ballot_sync` mask; the doorbell is rung once per fully-processed 32-entry group. The paper's justification is explicitly divergence-avoidance: this "maximizes parallelism while minimizing divergence across threads in a warp" `[paper]`.
- **instruction**: NVMe phase-bit extraction is a shift-and-mask on the completion DWord (`(cpl[3] >> 16) & 0x1`) `[code]`; cache-hit accounting uses `__popc` over a ballot mask `[code]`.
- **control placement**: `device-resident`. Both the submission (a GPU thread writes the SQE and rings the SQ doorbell) and the completion reaping (a GPU daemon kernel polls the CQ and rings the CQ doorbell) happen on the device. **The CPU is not in the control path or the data path.** This is a stronger device-residency claim than anything in the multi-GPU communication cluster, where inter-node RDMA still required a host proxy (cf. `GPU-ASPLOS26-01`, `GPU-SC26-22`).

## 12.10 Memory traffic
- **SSD → GPU**: peer-to-peer DMA into **GPU BAR1-mapped memory** `[README]`, no host bounce buffer. PCIe Gen4x16 to the GPU, Gen4x4 to each SSD `[paper]` — so three SSDs at Gen4x4 (~8 GB/s aggregate theoretical) against a Gen4x16 GPU link (~32 GB/s theoretical). **The SSDs, not the GPU link, are the bandwidth ceiling in this testbed** `[inference]` from the stated link widths.
- **HBM software cache**: the staging tier. Cache lines have four states and are evicted with write-back if `MODIFIED`.
- **register traffic**: the paper reports **up to 1.32× reduction in per-thread register usage versus BaM**, attributed to user threads being lock-free (the daemon owns the locks), minimal per-thread state, and no per-thread completion polling `[paper]`. This is an occupancy argument: fewer registers per thread means more resident warps means more outstanding I/O.
- **What the throughput is bounded by**: **not established, and for this paper the question is different from the compressor papers.** AGILE's results are all *relative speedups* (1.88×, 1.75×, 3.12×, 2.85×, 1.32×) with no absolute IOPS, GB/s, or queue-depth-vs-latency curve reported in the read text. Structurally the design targets **latency hiding**, so the binding constraint should be the number of outstanding requests, which is set by resident warps × per-warp outstanding depth — hence the emphasis on register reduction. That chain of reasoning is `[inference]`; the paper does not draw it and reports no occupancy figure. With three consumer/enterprise SSDs at PCIe Gen4x4 each, the hardware ceiling is low enough that this testbed cannot distinguish a software-limited from a device-limited result — `UNKNOWN`.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Overlap.** Asynchronous submission lets a thread compute while its request is outstanding; synchronous BaM cannot. This is the whole 1.88× and it is largest where the computation-to-communication ratio is favourable — the paper says "across workloads with diverse computation-to-communication ratios", which is the right framing.
2. **The deadlock fix is what makes overlap legal.** Handing the SQE lock to the service and taking back a barrier means a stalled thread never holds a resource the reaper needs. Without this, asynchrony is unsound, not merely slow.
3. **Warp-centric CQ polling amortises the doorbell.** 32 CQEs per doorbell write instead of one, with divergence minimised because every lane executes the same phase-bit test.
4. **Lower register pressure → higher occupancy → more outstanding I/O.** 1.32× fewer registers per thread than BaM.
5. **Cheaper cache path**: 3.12× lower software-cache overhead and 2.85× lower NVMe I/O overhead on graph applications, versus BaM.
6. **Where it costs**: the doorbell lock is a genuine serialisation point; the Share Table adds a MOESI-style coherence protocol in software whose overhead the paper does not isolate.

Numbers with full qualifiers `[paper]`:
- Hardware: **NVIDIA RTX 5000 Ada** GPU on **PCIe Gen4x16**; **one Dell Ent NVMe AGN MU AIC 1.6 TB + two Samsung 990 PRO 1 TB**, each on **PCIe Gen4x4**; Dell R750 server, Ubuntu 20.04, **NVIDIA driver 550.54, CUDA 12.8, Linux 5.4.0-200-generic**.
- Workloads: a micro-benchmark of **1024 threads issuing 64 NVMe commands** with interleaved computation; 4 KB random read/write scalability; **DLRM inference**; graph applications.
- Baseline: **BaM**.
- Results: **up to 1.88×** over synchronous across varying compute/communication ratios; **up to 1.75×** over BaM on DLRM; **3.12×** lower software-cache overhead and **2.85×** lower NVMe I/O overhead on graph applications; **1.32×** lower per-thread register usage.

## 12.12 Hardware generation dependence
- **A single GPU SKU: RTX 5000 Ada** — a workstation card, not a datacenter GPU `[paper]`. No A100/H100/MI300 result. This matters because BAR1 size, PCIe generation and HBM-vs-GDDR all differ on datacenter parts, and the design leans on BAR1 capacity.
- **BAR1 dependence is explicit and fragile**: the artifact requires enlarging BAR1 beyond the typical 128 MB via a vendor tool `[README]`. On many datacenter GPUs BAR1 is already large; on others resizable-BAR support is a platform question. This is a real portability constraint the paper does not discuss.
- **IOMMU must be disabled** `[README]` — a security-relevant system configuration that would be unacceptable in many production and multi-tenant settings, and is not mentioned as a limitation in the read text.
- **Kernel-version-coupled drivers**: the tree ships separate driver builds for Linux 6.8.0 and 6.17.0 `[code]`, evidence that the NVMe/GPU driver interface is not stable across kernels.
- NVMe itself (SQ/CQ, phase bit, CID) is a vendor-neutral standard, so the protocol logic would port; the GPU-side mechanisms (warp ballot, BAR1 peer-to-peer, persistent daemon kernel) are SIMT-specific but not NVIDIA-specific in principle. `[inference]`.

## 12.13 Limitations
Author-stated in the read text: the paper's own limitations discussion is thin. What the reading surfaced `[paper]`:
1. Limited treatment of when synchronous I/O suffices versus when asynchrony is necessary.
2. **Share Table overhead is not quantified separately.**
3. Scalability beyond the tested **3-SSD** configuration is not established.
4. Reliance on modified kernel drivers and a modified GDRCopy limits portability.

Recorded additionally from this reading:
5. **No absolute performance figures** — every result is a ratio against BaM. No IOPS, no GB/s, no latency distribution, no occupancy measurement.
6. **Single workstation-class GPU**, single server.
7. **IOMMU must be disabled and BAR1 enlarged** `[README]` — deployment constraints with security and portability consequences, not discussed in the paper.
8. **Paper/code discrepancy on the SQE state machine** (three states vs five) — §12.8.

## 12.14 Relation to prior corpus
- `NO_EXISTING_ANALYSIS`. `[repo-grep]` hits for "AGILE" were the English word in unrelated analyses (`GPU-SC25-01`, `GPU-HPCA24-41`) plus census rows. `[repo-grep]`
- **The cluster's strongest device-resident-control paper.** Compare `GPU-ASPLOS26-01` (MSCCL++), where the ledger records that GPU-initiated RDMA is *not supported* and inter-node transfers need a CPU proxy; and `GPU-HPDC26-01` (GICC), where the paper distinguishes GPU-*triggered* from GPU-*initiated* by fabric. AGILE achieves what those cannot on the network path, but on the **storage** path — a GPU thread writes an NVMe SQE and rings a doorbell, and a GPU daemon reaps the completion, with no host involvement in either direction. The reason the storage path is easier is that NVMe doorbells are plain MMIO registers mappable into the GPU's address space, whereas RDMA verbs require a driver-mediated work-queue protocol. `[inference]`, but strongly supported by the two papers side by side.
- **Complementary to Phoenix (SC 2025)**, the other GPU-storage paper in this cluster, which attacks the GPUDirect Storage bounce-buffer path. AGILE bypasses GDS entirely; Phoenix refactors it. Both are SC 2025.
- **Prior art the paper engages** `[paper]`: **BaM** (the direct baseline and the prior GPU-centric synchronous design), **GPUDirect Storage** and **DeepNVMe** (both CPU-initiated), **CXL-enabled SSDs**, and `cuda::memcpy_async` (an on-device async primitive that does not reach storage). The AGILE artifact also vendors a **BaM NVMe driver** (`driver/bam_nvme_driver-linux-6.8.0/`) `[code]`, i.e. the baseline is built from source in-tree — unusually good comparative hygiene.
- **No compression.** AGILE is in this cluster for the I/O-path axis, not the compression axis, and there is no citation traffic between it and the SZ-family papers in either direction.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO, emphatically.** The *problem* does not exist on a CPU:
1. **The deadlock is a GPU-scheduling artifact.** A CPU thread that blocks on a full submission queue is descheduled and the completion reaper runs. A GPU warp that spins on a full SQ holds its slot forever, because there is no preemption and no yield — so the thread that must release the lock can never be reached. The paper's worked deadlock ("none can be released") is only a deadlock under non-preemptive SIMT execution.
2. **The fix is a persistent device-resident daemon kernel**, a structure that exists only because a GPU can hold a long-running kernel resident alongside compute kernels.
3. **CQ polling is warp-collective**: one warp per CQ, one lane per CQE, phase-bit test per lane, `__ballot_sync` aggregation, one doorbell write per 32 entries `[code]`. The paper justifies it by warp divergence. A CPU reaps a completion queue with a loop.
4. **Register pressure is a first-class metric** — a 1.32× reduction is claimed as a contribution, because registers gate occupancy gates outstanding-request concurrency. Nothing analogous exists on a CPU.
5. **The data path is GPU BAR1 peer-to-peer DMA** `[README]`, i.e. the SSD DMAs directly into GPU device memory apertures. This is the GPUDirect-class mechanism and has no CPU counterpart.
6. **The doorbell serialisation problem** — thousands of concurrent threads writing one MMIO register — arises from GPU thread counts, not from the NVMe spec.

No qualification is needed. Even the software cache is HBM-resident and warp-collective in its lookup path (`__activemask` + `__shfl_sync` + `__popc` at `agile_ctrl.tpp:664-710`) `[code]`.

verdict_basis: The contribution is an asynchronous GPU-centric NVMe path whose central difficulty — a deadlock in which submitting threads hold SQ locks and cannot be preempted to reach the reaper — exists only under non-preemptive SIMT execution, and whose solution is a persistent device-resident daemon kernel doing warp-collective, ballot-aggregated completion-queue polling over BAR1 peer-to-peer DMA.

## What the throughput is bounded by
**`NOT_ESTABLISHED`.** The paper reports only relative speedups (1.88× over synchronous; 1.75× over BaM on DLRM; 3.12× / 2.85× overhead reductions on graphs; 1.32× register reduction) and **no absolute IOPS, GB/s, latency distribution or occupancy figure**. Structurally the design is a latency-hiding design, so the binding constraint should be outstanding-request concurrency = resident warps × per-warp depth, which is why register reduction is presented as a contribution — but that is `[inference]`, not a paper claim. The testbed's storage ceiling (three SSDs at PCIe Gen4x4 each, behind a Gen4x16 GPU link) is low enough that a device-limited and a software-limited result cannot be distinguished from the published numbers. `UNKNOWN`.

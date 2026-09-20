# GPU-ICS25-01 — DREAM: Device-Driven Efficient Access to Virtual Memory

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `D — GPU virtual memory / demand paging / oversubscription (device-initiated)` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `GPU-initiated data movement (GPUDirect RDMA); C — device-side page-table management; graph and query workloads under oversubscription`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation with the Fig. 2 fault-cost breakdown; background (UVM fault sequence Fig. 1, RNIC one-sided RDMA, BaM and GPU-initiated storage work); design §3 (GPU thread page-fault handler, RNIC work-request/completion-queue path, page-frame circular buffer Fig. 5, FIFO page map with reference counting, intra- and inter-warp leader election, device-side page-table update, dream_ptr abstraction Listing 1, Little's-Law queue-pair sizing §3.2); §4 limitations; §5 evaluation setup, results Figs. 8-16, Table 3, oversubscription sweep §5.4; related work. Read via two targeted full-text passes over the ICS 2025 proceedings PDF, PLUS the public artifact repository inspected at a pinned commit (see 12.8). The author slide deck at cs.ucr.edu was also read and is labelled [author-presentation] where used.`

## 12.1 Bibliographic facts

- Title: *DREAM: Device-Driven Efficient Access to Virtual Memory* `[paper]` (the ICS proceedings PDF and the repository README render it "Device-driven"; the official program row uses "Device-Driven" — `domains/gpu_systems/census/ICS_2025.md`)
- Authors: Nurlan Nazaraliyev, Elaheh Sadredini, Nael Abu-Ghazaleh — all University of California, Riverside `[paper]`
- Venue: ICS 2025 (39th ACM International Conference on Supercomputing), "Memory Systems" session, Wednesday 11 June 2025, Salt Lake City `[official-program, via census/ICS_2025.md; date/location corroborated by the author slide deck [author-presentation]]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- DOI: `10.1145/3721145.3725748` `[publisher-proceedings — DOI string observed in the ACM DL record title surfaced by search; the ACM page itself is unreachable here (403)]`
- Full text used: https://hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-9.pdf (ICS 2025 official program proceedings PDF) `[paper]`
- **Evidence-class warning:** https://www.cs.ucr.edu/~elaheh/papers/ICS2025-DREAM-Nurlan.pdf is the author's **slide deck**, not the paper. Claims sourced from it are labelled `[author-presentation]` and are not attributed to the paper, per `governance/SOURCE_EVIDENCE_RULES.md`.
- Artifact/code: **https://github.com/nnurlan008/dream**, inspected at commit **`8ed15b256f8ad88c88628c80cde06738349194e8`** (shallow clone, 2026-09-18). `[code]`

## 12.2 Core question (one sentence)

On a GPU page fault under UVM, the *control* path — interrupt to the driver, host-side fault batching, OS page-table update, TLB shootdown, DMA setup — costs several times more than the *data* transfer itself, so can the GPU's own threads take over page-fault handling and page-table maintenance entirely, using a commodity RDMA NIC as the data mover, with no CPU or OS in the critical path? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** Primary axis: GPU HBM oversubscription. Oversubscription is defined as "Workload Size / Available GPU memory − 1" and swept from 0 to 10×. `[paper]`
- **Communication.** The mechanism *is* a communication redesign: one-sided RDMA reads from pinned host memory into GPU memory over PCIe, issued by GPU threads. Measured: 6.5 GB/s with one NIC at 4 KB pages, 12 GB/s (full PCIe 3) with two NICs. `[paper]`
- **Compute.** Load-bearing rather than incidental: the fault handler *runs on the SMs*. 84 SMs × 16 warps yields "1,344+ concurrent page requests," which is the concurrency UVM's host-side batching cannot match. `[paper]`
- **Synchronization.** Central. Intra-warp leader election, inter-warp page locking, reference counting on page frames, and atomic coordination before ringing the RNIC doorbell. `[paper]`
- **Scheduling.** Queue-pair provisioning is sized by Little's Law: "72 queue pairs for 4KB pages; 36 for 8KB." `[paper]`

## 12.4 Why the problem exists (hardware root cause)

1. **The UVM fault path is a five-stage host round trip.** As the paper describes it: (i) the GMMU detects a TLB miss and writes the fault buffer; (ii) a hardware interrupt reaches the UVM driver; (iii) the driver batches faults and caches them in host memory; (iv) the OS performs page-table updates and TLB shootdowns; (v) the DMA engine migrates pages. `[paper]`
2. **The control path costs ~7× the data path.** "Host involvement overheads during the page fault are around 7× higher than the transfer time at 64KB page size" (Figure 2). `[paper]` The corresponding slide-deck figures are 12 µs data migration versus 88 µs control path at 64 KB `[author-presentation]` — those specific numbers are from the talk, not the paper text as read, and are labelled accordingly.
3. **The serialisation is structural, not a tuning problem.** "The UVM driver manages separate page tables in GPU and host memory, serializing fault processing and preventing parallel handling." `[paper]` A GPU generates faults with thousands of threads in parallel; a driver consumes them on one CPU control path. The asymmetry cannot be closed by making the driver faster.
4. **UVM's eviction granularity amplifies I/O.** UVM operates a 4 KB base page with a 60 KB speculative prefetch and evicts at **2 MB VABlock** granularity; for sparse access this moves data that is never used. Measured consequence: DREAM's 4 KB fine-grained eviction gives **1.8× fewer redundant transfers** under oversubscription. `[paper]`
5. **The enabling hardware fact.** "RNICs support one-sided RDMA connections to the CPU, which allow a device to move pages from other memories directly (without OS involvement)." `[paper]` Combined with GPUDirect RDMA peer-to-peer over PCIe, a GPU thread can post a work request and an RNIC can write straight into GPU memory. The paper is explicit about *why* a NIC rather than the CPU: "current CPU architectures do not support GPU-initiated memory management." `[README, quoting the paper's abstract]`
6. **Why a Tesla-class Volta-or-newer GPU specifically.** The artifact states the requirement directly: a Tesla-class GPU is needed "to expose all of its memory for P2P accesses over PCIe" (a T4 exposes only 256 MB of BAR space), and Volta or newer is needed because DREAM relies on "memory synchronization primitives only supported since Volta." `[README]` These are hard hardware preconditions, not preferences.

## 12.5 Mathematical / performance model

DREAM contains the one genuine analytic sizing argument in this cluster.

- **Queue-pair count by Little's Law** (§3.2): the number of in-flight requests needed to saturate the link is the bandwidth–latency product divided by request size, giving **72 queue pairs at 4 KB** pages and **36 at 8 KB**. `[paper]` Measured behaviour matches the shape: near-optimal at **≥48 QPs**, diminishing returns beyond **96**; below ~72 QPs requests serialise. `[paper]` In the graph configuration, "84 streaming multiprocessors with 84 queue pairs" are used. `[paper]`
- **Oversubscription ratio** = Workload Size / Available GPU memory − 1. `[paper]`
- **Eviction condition:** a FIFO page map entry is atomically acquired; when the target frame is occupied, the leader thread waits for the frame's **reference counter to reach zero** before evicting via write-back. `[paper]`
- No closed-form performance model for end-to-end speedup is given.

## 12.6 Data layout and ownership

- **thread:** issues the access that misses and participates in leader election.
- **warp:** the unit of fault coalescing. Intra-warp: one leader is elected among threads whose accesses map to the same page, using `__match_any_sync`. Inter-warp: among leaders from several warps, "only one leader will lock the page entry" and the others wait. `[paper]`
- **SM:** the concurrency unit for queue pairs — 84 SMs, 84 QPs in the graph configuration. `[paper]`
- **GPU memory — the paper's central data structure.** GPU memory is organised as a **circular queue of page frames with a global head cursor**, mapping host pages to GPU pages (Figure 5). `[paper]` A **FIFO page map** records occupancy; entries carry a reference count. `[paper]` In the artifact the cursors are device-global variables: `__device__ size_t R_cursor, E_cursor, num_pages;` in `include/runtime_eviction.h:54` `[code]` — two cursors (read/refill and eviction), which is the implementation shape of the head-cursor design.
- **Device-side page table:** "The device memory page table is updated directly by the device upon the completion of a work request on the RNIC," and "GPU threads access page tables stored in device memory for fast lookups and modifications." `[paper]` This is the ownership inversion that defines the paper: the page table for migrated pages is *owned and mutated by the GPU*.
- **RNIC:** owns the work-request and completion-queue rings; it "fetches work requests from GPU memory, performs RDMA reads from host memory, writes pages to GPU memory, updates completion queue entries." `[paper]`
- **Host:** provides pinned DRAM (512 GB DDR4 in the evaluated node) and is otherwise out of the critical path. `[paper]` The paper states the assumption explicitly: "DREAM assumes that host memory is pinned and that there is sufficient host DRAM capacity to accommodate the working set." `[paper]`
- **node / cluster:** the design is stated to extend "beyond local host memory, facilitating direct access to both remote host memory and remote GPU memory," but the implementation supports at most 2 GPUs + 2 NICs. `[paper]`
- **Programmer-facing ownership:** a `dream_ptr<T>` array abstraction (Listing 1) so existing kernels need "minimal modifications." `[paper]`

## 12.7 Pseudo code

Component names, the leader-election primitive, the circular buffer, the reference-counted FIFO map and the doorbell batching are `[paper]`; statement-level shape is `[reconstruction]`, cross-checked against the artifact where noted.

```
// GPU-side page fault handler, executed by the faulting threads       [paper]
__device__ T dream_ptr<T>::operator[](size_t i) {                      // [paper] Listing 1
    page = page_of(i);
    if (page_map.resident(page)) { atomicAdd(&refcnt[frame], 1); return data[...]; }

    // ---- intra-warp coalescing: elect one leader per distinct page ----
    unsigned mask1 = __match_any_sync(__activemask(), (unsigned long long)che); // [paper]+[code]
    leader = lowest_lane(mask1);

    if (is_leader) {
        // ---- inter-warp: only one leader owns the page entry ----     [paper]
        if (!page_map.try_lock(page)) wait_until_resident(page);         // [paper]
        else {
            frame = head_cursor++ (mod num_pages);                      // [paper] Fig. 5; [code] R_cursor/E_cursor
            while (refcnt[frame] != 0) { /* spin */ }                    // [paper]
            if (occupied(frame)) writeback(frame);                       // [paper] (synchronous; see 12.13)
            post_work_request(qp[my_sm], host_addr_of(page), frame);     // [paper]; [code] device_gpu_post_send
            // batching: several leaders post to the same QP; one randomly
            // chosen leader rings the doorbell after an atomic count settles [paper]
            ring_doorbell_if_last();                                     // [paper]
            poll_completion_queue(cq[my_sm]);                            // [paper]; [code] cq_wait[]
            update_device_page_table(page -> frame);                     // [paper]
            page_map.unlock_and_publish(page, frame);
        }
    }
    __syncwarp(mask1);
    return data[...];
}
```

## 12.8 Real implementation

This is the only paper in this cluster with an artifact that was actually read. Repository **https://github.com/nnurlan008/dream** at commit **`8ed15b256f8ad88c88628c80cde06738349194e8`**. `[code]`

Verified structure `[code]`:
- `src/rdma_utils.cu` — the GPU-side RDMA path. Real symbols: `__device__ int device_gpu_post_send(...)` (line 3225), `__global__ void global_gpu_post_send(...)` (line 3333), `int host_gpu_post_send(struct ibv_qp*, struct ibv_send_wr*, ...)` (line 3366), `int host_gpu_poll_cq(struct ibv_cq*, int, struct ibv_wc*)` (line 3717). `src/rdma_utils.h` declares `int cpu_poll_cq(struct ibv_cq*, int, struct ibv_wc*)` (line 818) and `int mlx5_post_send(struct ibv_qp*, struct ibv_send_wr*, ...)` (line 820) — i.e. the project reimplements parts of the mlx5 send path so it can be driven from device code.
- `include/` holds one runtime header per evaluated configuration: `runtime.h`, `runtime_warp.h`, `runtime_micro.h`, `runtime_eviction.h`, `runtime_eviction_write.h`, `runtime_eviction_2nic.h`, `runtime_eviction_2gpu.h`, `runtime_prefetching.h`, `runtime_prefetching_2nic.h`, `runtime_prefetching_2gpu.h`, `runtime_prefetching_2gpu_2nic.h`, `primitives.h`, `stdatomic.h`. The 2nic / 2gpu variants correspond to the paper's multi-NIC and 2-GPU configurations.
- Device-global state in `include/runtime_eviction.h`: `__device__ size_t R_cursor, E_cursor, num_pages;` (line 54), `__device__ struct post_content gpost_cont;`, `__device__ struct batch gbatch;`, `__device__ struct poll_content gpoll_cont;`, `__device__ size_t g_qp_index;`, `__device__ size_t cq_wait[128];`, `__device__ int activeThreads[128];` (lines 62–70). These are the concrete realisations of the paper's work-request batching, completion polling and per-SM queue-pair indexing.
- `mlnx-kernel/` and `rdma_core/` hold the custom Mellanox kernel module and rdma-core packages the README requires to be built and installed.
- Benchmarks present: `benchmarks/bfs/` (with `bfs.cu`, `readGraph.cpp`, `bfsCPU.cpp`, `check_odp_support.c`) and `benchmarks_multiNIC/`.

**A discrepancy worth recording.** The paper presents `__match_any_sync` as the intra-warp leader-election primitive (§3.3). In the artifact at this commit, `__match_any_sync` appears **28 times, of which only 6 are live code**; the live sites are `include/runtime_warp.h:824`, `include/runtime_eviction.h:1624`, `include/runtime_eviction_2gpu.h:1631`, `include/runtime_eviction_2nic.h:1374`, and `include/runtime_eviction_write.h:1724` and `:2001`, all of the form `unsigned int mask1 = __match_any_sync(__activemask(), (unsigned long long)che);`. Every occurrence in `runtime.h`, `runtime_micro.h` and all four `runtime_prefetching*` headers is **commented out**, and several commented variants match on `qp_index` rather than on `che`. `[code]` Reading: warp-level match-based coalescing is live in the warp and eviction runtimes (the oversubscription configurations) and disabled in the prefetching runtimes. This is a real difference between the paper's general description and the shipped configurations, and it is stated here as a code observation, not as a criticism of the paper's results.

Build/platform requirements from the artifact `[README]`: x86 with PCIe P2P; Mellanox ConnectX NIC; NVIDIA Tesla/datacenter GPU, Volta or newer; BIOS `Above 4G Decoding` enabled; **IOMMU disabled** (VT-d / AMD IOMMU, plus Linux `iommu` off); ACS disabled; Ubuntu 22.04 with a 5.x kernel; `nvidia-driver-535`; MLNX-OFED 23.07-0.5.1.2. Built on **CloudLab r7525 nodes at Clemson**, with the CloudLab profile checked into the repo (`profile`).

## 12.9 Kernel execution

DREAM changes kernel execution more than any other paper in this cluster, because the memory-management code *is* kernel code.

- **The fault handler executes in the warp that faulted.** Threads elect a leader, the leader posts the work request and polls the completion queue, and the warp resynchronises. `[paper]`
- **Register pressure is a real cost of that choice:** DREAM uses **20–114 registers per thread** depending on kernel, with no spilling observed (Figure 16). `[paper]` This is the occupancy tax for putting the page-fault path in the kernel.
- **Load balancing had to be fixed for graphs.** Standard CSR gives high-degree vertices enormous neighbour lists (7.5 M neighbours in GAP-Kron, 2.1 M in MOLIERE), so one thread serialises many page requests. DREAM introduces a **balanced CSR** that "chunks neighbor lists into equal-sized segments," costing up to 400 MB per graph, and gains **1.5× with 2 NICs** over baseline CSR (Figure 10). `[paper]` This is a genuinely GPU-execution-model consequence: the page-request rate is bounded by thread-level parallelism over the adjacency structure.
- **Concurrency achieved:** "84 SMs × 16 warps = 1,344+ concurrent page requests" versus UVM's host-batched path. `[paper]`

## 12.10 Memory traffic

Path: register ↔ L1/shared ↔ L2 ↔ GPU HBM (32 GB on the V100 used) ↔ **PCIe 3 (12 GB/s nominal) via GPUDirect P2P to the RNIC** ↔ pinned host DDR4. `[paper]`

- **Small-request efficiency is the headline traffic result.** DREAM reaches 6.5 GB/s at **4 KB** request size with one NIC and saturates PCIe 3 at **12 GB/s** with two; GPUDirect RDMA (CPU-initiated) "requires 512KB+ request size to saturate" and achieves only ~50% utilisation at small granularity; UVM averages ~6 GB/s at ~50% utilisation (Figure 8). `[paper]` DREAM's PCIe utilisation on transfer-bound applications is 80–100% versus UVM's ~40–50%. `[paper]`
- **I/O amplification.** 4 KB reference-counted eviction versus UVM's 2 MB VABlock eviction gives **1.8× fewer redundant transfers** under oversubscription, and "halves UVM's overhead" for the 0.08%-sparsity query workload. `[paper]`
- **The known traffic bottleneck** is the shared PCIe bridge: ingress and egress "share the same PCIe bridge channel, decreasing the one-directional bandwidth to half," mitigated by using two NICs on two dedicated bridges. `[paper]`
- **The NIC sits on the data path**, which the authors list as a drawback: "the interruption of the NIC as it is located on the data path." `[paper]`

## 12.11 Why it is faster/slower (decomposed)

1. **The eliminated term is the control path, and it was the larger one.** ~7× the transfer cost at 64 KB pages. `[paper]` Everything else follows.
2. **Fine granularity becomes affordable once the host is out of the loop.** UVM must amortise a 7× control overhead, which is *why* it uses a 60 KB prefetch and 2 MB eviction blocks; DREAM can afford 4 KB because its per-request cost is a work-request post. Hence both the small-request bandwidth result and the 1.8× I/O-amplification result are consequences of the same mechanism change, not independent wins. `[inference]` from the paper's own numbers.
3. **Parallelism replaces batching.** 1,344+ concurrent requests from 84 SMs, provisioned against a Little's-Law queue-pair count. `[paper]`
4. **Results with their full qualifiers** `[paper]`:
   - Graph analytics (SuiteSparse / GAP datasets, 3.61 B–6.67 B edges, 4 KB pages): **1.4×** over `cudaMemAdvise`-tuned UVM for BFS, **1.5×** for CC; **1.12–1.89×** over Subway with 2 NICs (BFS on GAP-Kron 2.04 s vs 3.86 s = 1.89×; CC on GAP-Kron 2.81 s vs 4.73 s = 1.68×).
   - SSSP with GPU memory capped at 16 GB: **1.9×** over UVM.
   - Transfer-bound kernels (MVT, ATAX, BIGC), 2-NIC: **2–4×** over UVM; Vector Add (2 B elements) **2×** with one NIC, **1.7×** under memory pressure.
   - Query evaluation (Chicago Taxi Trips, Q1–Q5, 0.08% sparsity): **3×** over UVM on average, **1.5–2.5×** over RAPIDS.
   - **Predictability under pressure, arguably the most important result:** across the oversubscription sweep, UVM slows by **4–10×** on graphs and "exponentially" for column-wise access (MVT, ATAX, BIGC), while DREAM stays at a consistent **1.5–2.5×** slowdown (Figure 14).
5. **Where it is slower.** Write-intensive workloads under memory pressure, because "we have not yet implemented asynchronous writebacks, resulting in increased latencies on these operations." `[paper]` Also register pressure (up to 114 registers/thread) constrains occupancy, and the balanced-CSR fix costs up to 400 MB per graph. `[paper]`

## 12.12 Hardware generation dependence

- **NVIDIA Tesla/datacenter GPU, Volta or newer** — required for full-BAR P2P exposure and for the memory-synchronisation primitives DREAM uses; a T4 is explicitly ruled out (256 MB BAR). `[README]`
- **Mellanox ConnectX-class RNIC** with a modifiable rdma-core/mlx5 send path; the repository ships custom `rdma_core/` and `mlnx-kernel/` packages and the paper notes customised `ibv_reg_mr`, `ibv_qp_create`, `ibv_cq_create`. `[paper]`+`[code]`
- **PCIe P2P enabled, IOMMU disabled, ACS disabled.** `[README]` The IOMMU requirement is a significant deployment constraint for shared systems and is a platform fact, not a tuning knob.
- Evaluated on **CloudLab r7525**: V100 32 GB, 2× AMD EPYC 7542 (32 cores, 2.40 GHz), 512 GB DDR4-3200, PCIe 3, ConnectX-5 (25 Gb/s) and ConnectX-6 (100 Gb/s), Ubuntu 22.04, driver 535.183.01, CUDA 12.2, MLNX-OFED 23.07. `[paper]`+`[README]`
- Authors state the platform dependence directly: "The performance of DREAM is specific to this platform and may be sensitive to the specific hardware." `[paper]`
- **Forward-looking caveat this analysis adds** `[inference]`: DREAM's premise is that "current CPU architectures do not support GPU-initiated memory management." The paper's own related work names **Grace-Hopper** with NVLink-C2C coherence as the hardware alternative that would obviate the NIC detour, noting it "requires new CPU design." On a coherent CPU–GPU part the NIC indirection is unnecessary, so DREAM's value is highest on commodity PCIe-attached systems.

## 12.13 Limitations

Author-stated `[paper]`:
1. Platform-specific performance; evaluated only on r7525 CloudLab nodes.
2. Shared PCIe bridge halves one-directional bandwidth; worked around with two NICs on separate bridges.
3. The NIC sits on the data path — an inherent detour.
4. Host memory must be pinned and large enough for the working set; future work is to pin only hot pages.
5. Mostly single-kernel applications and back-to-back multi-kernel; concurrent kernels need an extension.
6. Implementation supports only 2 GPUs + 2 NICs; cluster scaling not addressed.
7. Asynchronous write-back not implemented, raising write latencies under pressure.
8. 20–114 registers per thread (no spilling observed).

Observed here, not claimed `[inference]`/`[code]`:
9. **IOMMU must be disabled** (`[README]`). This is a security-relevant deployment requirement — the IOMMU is the isolation mechanism for device DMA — and the paper as read does not discuss the consequence of running without it.
10. **The shipped prefetching runtimes have warp match-based coalescing commented out** while the eviction/warp runtimes have it live (see 12.8). Which configuration produced which figure is not determinable from the artifact alone.
11. **No comparison against BaM** despite BaM being the closest GPU-initiated ancestor; the paper's stated reason is a different target ("DREAM targets system/host memory, not NVM"), which is a scope distinction rather than a performance argument.
12. Results are on **PCIe 3**; the small-request advantage over CPU-initiated GPUDirect RDMA may narrow on PCIe 5/6 where per-request overheads are relatively smaller. This is not evaluated.

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. Repository grep for the exact/normalised title and "Device-Driven Efficient Access" returned only `domains/gpu_systems/census/ICS_2025.md`. The census had marked this paper `[TITLE-ONLY]` with "GPU device identity UNVERIFIED without abstract"; the proceedings PDF and the artifact **resolve that**: it is an NVIDIA-GPU UVM-replacement system.
- **Lineage verified from DREAM's own related work** `[paper]`:
  - **UVM** — the baseline being replaced (4 KB base page + 60 KB speculative prefetch, 2 MB VABlock eviction).
  - **HMM** — Linux kernel unified memory; DREAM's stated distinction is that HMM "requires OS involvement" and has "no speculative prefetch support."
  - **DRAGON** — GPU memory extension via OS-level page eviction to NVM; DREAM uses RDMA and supports remote memory.
  - **BaM** — GPU-initiated high-throughput NVM access; DREAM's distinction is target (host/system memory rather than NVM). *This is a verified citation link, and it matters for this cluster: `GMT` (ASPLOS 2024, watchlist) is built on BaM — its artifact's `README.md` states "GMT is built on top of BaM" and its source contains a device-side TLB (`struct tlb`, `struct tlb_entry`, `struct bam_ptr_tlb` in `include/page_cache.h`) `[code, GMT repo commit 2f139b0d01791812e8f2d5aaa8c8cfd176f2d2ee]`. DREAM and GMT are therefore two independent descendants of the BaM GPU-initiated-access line, one reaching host memory via an RNIC and one building a GPU-orchestrated 3-tier GPU/host/SSD hierarchy.*
  - **GPUrdma**, **GPUnet** — GPU-side networking; network-focused, not virtual-memory management.
  - **FaRM**, **AIFM** — CPU-side far memory over RDMA.
  - **ActivePointers** — memory-map abstractions for device storage; no oversubscription support.
  - **Grace-Hopper** (NVLink-C2C coherence) — the hardware alternative, requiring new CPU design.
  - **Subway** — manual graph partitioning, compared quantitatively (DREAM 1.12–1.89× faster); **RAPIDS** — GPU query framework, compared quantitatively (1.5–2.5×).
- **Complementary and contrasting within this cluster.** DREAM and SUV (`GPU-MICRO24-01`) attack the same 7×-control-path problem from opposite ends: SUV keeps the host driver but feeds it compiler-derived semantics so fewer faults occur; DREAM removes the host driver from the fault path altogether. The ICS 2024 AMD SVM study (`GPU-ICS24-02`) independently measured the analogous decomposition on AMD hardware and reached the same structural conclusion — driver bookkeeping (`cpu_update`, `SDMA_setup`, `alloc`) exceeds data movement. Three papers, two vendors, one root cause. **No citation links among these three were verified**; this convergence is stated as `[inference]` from their separately-read contents.
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`/`[code]`-grounded reasons: (a) the problem is the **GPU UVM page-fault control path** — GMMU TLB miss, fault buffer, driver interrupt, host-side batching, OS page-table update and TLB shootdown — measured at ~7× the transfer cost; a CPU services its own faults locally and has no such split; (b) the solution *runs on the SMs*: the fault handler is device code that uses **warp-level primitives** (`__match_any_sync` over the active mask, verified live in the artifact) for intra-warp fault coalescing, and its request concurrency (84 SMs × 16 warps ≈ 1,344 in flight) is precisely the SIMT parallelism the host driver could not absorb; (c) the mechanism requires **GPUDirect PCIe peer-to-peer into GPU BAR space** on a Tesla-class Volta-or-newer GPU, with the artifact stating a T4's 256 MB BAR is insufficient; (d) the design premise is stated as a GPU/CPU asymmetry — "current CPU architectures do not support GPU-initiated memory management"; (e) the workload fix (balanced CSR) exists because GPU thread-level parallelism over adjacency lists bounds the page-request rate.

verdict_basis: DREAM relocates GPU demand paging and page-table maintenance into GPU kernel code executed by warps, using warp-level match primitives for fault coalescing and GPUDirect RDMA peer-to-peer into GPU BAR space, in order to eliminate a host-driver control path that costs ~7× the data transfer; every element depends on the GPU UVM fault path, SIMT warp execution, or GPU-specific PCIe P2P capability.

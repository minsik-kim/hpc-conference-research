# GPU-HPDC26-01 — GICC: GPU-Initiated Communication and Coordination Runtime

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `M GPU-aware / GPU-initiated communication & collectives`
secondary_topics: `L Multi-GPU interconnect & data paths`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2604.22126v1) read across motivation, the two fabric paths (InfiniBand direct posting vs OFI/CXI deferred work queue), the coordination abstraction (active messages, dissemination barriers, completion polling), the hybrid host-progress design (§3.3 blocking-flush problem), evaluation on Tioga and Maple, results tables incl. Table 3, limitations, and the related-work comparison table.`

## 12.1 Bibliographic facts
- **Title discrepancy, recorded**: the HPDC 2026 program title per census `HPDC_2026.md` row 1 is *GICC: GPU-Initiated Communication and Coordination Runtime* `[census]` `[official-web]`. The arXiv full text read here is titled *GICC: A High-Performance Runtime for GPU-Initiated Communication and Coordination in Modern HPC Systems* `[paper]`. Both recorded; neither discarded.
- Authors `[paper]` `[census]`: Baodi Shan (Stony Brook University), Mauricio Araya-Polo (TotalEnergies), Barbara Chapman (Stony Brook University). Census places it in HPDC 2026 Session 11 "Communication, Workflows & Sustainability", `CONFIRMED_IN_POPULATION`.
- arXiv ID 2604.22126. DOI `UNKNOWN`.
- Publication type: `ARCHIVAL_MAIN_PAPER`; read source is the `PREPRINT`.

## 12.2 Core question (one sentence)
If a GPU kernel needs frequent distributed coordination (barriers, reductions, phase ordering), can that coordination be driven from the device rather than by returning control to the host — and can it be done on **OFI/CXI fabrics** such as HPE Slingshot, where NVSHMEM-class runtimes remain host-mediated? `[paper]`

## 12.3 GPU/HPC problem translation
- **Synchronization**: the primary object, and the paper's distinguishing choice. Prior device-initiated work (NVSHMEM, rocSHMEM) provides device-visible *data movement*; GICC's claim is device-driven *coordination* — barriers and ordering.
- **Communication**: RDMA put/get, but deliberately decoupled from the coordination semantics.
- **Scheduling**: eliminating host round trips removes kernel-boundary fragmentation; the paper measures coordination as >32% of runtime in phase-heavy workloads.
- **Memory**: GPU-visible completion flags and NIC counters mapped into GPU-addressable memory.
- **Compute**: kernels stay resident across phases instead of terminating at each coordination point.

## 12.4 Why the problem exists
The paper's root-cause chain `[paper]`:
1. **Coordination points are host-driven by construction** in today's programming and runtime models, so each one costs a GPU→CPU→GPU round trip.
2. **On OFI/CXI the GPU physically cannot enqueue NIC work dynamically.** This is the hardware root cause and it is fabric-specific: on NVIDIA mlx5 InfiniBand a GPU kernel can construct work-queue elements and ring the NIC doorbell through the User Access Region; on HPE Slingshot's CXI provider it cannot.
3. **Therefore the existing device-initiated stack does not port.** NVSHMEM and rocSHMEM offer GPU-visible APIs but remain host-mediated on OFI — and the paper notes Slingshot powers 6 of the Top500 top 10, so this is not a corner case.
4. **NIC state is finite.** CXI limits recorded by the paper: deferred-work-queue capacity 256 entries; counter range 2047 shared across ranks. At P=4096 ranks only ~21 barrier instances can be pre-staged at once.
5. **A naive fix deadlocks**: the paper identifies a "blocking-flush problem" (§3.3) when libfabric progress is not driven.

## 12.5 Mathematical / performance model
`NOT_IN_PAPER` as a closed-form model. The paper reports measured per-coordination latency, weak-scaling parallel efficiency, and a resource-capacity calculation (256-entry DWQ, 2047 counters ⇒ ~21 pre-staged barriers at P=4096). The capacity arithmetic is the closest thing to a model and is a hardware-limit count, not a performance model. `[paper]`

## 12.6 Data layout and ownership
- **thread**: GPU threads invoke the coordination primitives and poll GPU-visible flags. The paper names `gicc_trigger()`, `gicc_wait_until()`, `gicc_barrier_all()`. `[paper]`
- **GPU → node**: on Tioga a node holds 8 MI250X GCDs; each rank owns pre-staged NIC operations plus a counter.
- **node → cluster**: barriers are multi-round dissemination; after each round GPU threads poll the round's signal location.
- **Ownership of NIC state**: the host pre-stages a bounded set of operations into the Deferred Work Queue with trigger thresholds on NIC counters; the device owns only the act of triggering. Epoch-based handoff with sliding-window double-buffering recycles that finite state. `[paper]`

## 12.7 Pseudo code
Reconstructed from the paper's prose, using only the primitive names the paper prints `[paper]` `[reconstruction]`:
```
// --- host, once per epoch (OFI/CXI path) ---
pre_stage_into_DWQ(ops, trigger_thresholds_on_NIC_counters);

// --- device kernel, per phase ---
gicc_trigger();          // doorbell write updates GPU-mapped NIC counter -> NIC executes pre-staged op
gicc_wait_until(flag);   // poll GPU-visible completion flag / sequence number written by the NIC
gicc_barrier_all();      // multi-round dissemination; poll signal location after each round

// --- active message ordering ---
sender: RDMA_write(payload); RDMA_write(sequence_number);   // sequence after payload
receiver: while (seq_field != expected) ;                    // poll sequence field
```
On InfiniBand the pre-staging step is absent: the kernel constructs the work-queue element and rings the doorbell directly through the mlx5 User Access Region. `[paper]`

## 12.8 Real implementation
No public artifact repository was established (census: `NOT_FOUND_AFTER_SEARCH`). `NOT_INSPECTED` — no code was read. The symbols `gicc_trigger`, `gicc_wait_until`, `gicc_barrier_all` are reported because the paper prints them `[paper]`; no other GICC symbol is asserted. The paper states GICC does **not** use NVSHMEM, GPUDirect Async, or IBGDA directly, but provides its own coordination abstraction layer.

## 12.9 Kernel execution
- **kernel**: the intended pattern is a long-lived kernel that spans multiple coordination points, instead of one kernel per phase. `[paper]`
- **thread block / warp**: `NOT_IN_PAPER` — the paper does not report the CTA/warp mapping of the polling loops.
- **instruction**: the two device-side operations are a doorbell store (to a GPU-mapped counter) and a polling load on a GPU-visible flag. `[paper]`

## 12.10 Memory traffic
- Device-side traffic is small: doorbell stores and polling loads on GPU-visible memory. Bulk payload moves NIC→NIC via RDMA and does not pass through SMs.
- The NIC writes sequence numbers into GPU-visible memory, which is what makes device-side completion detection possible.
- Register/shared/L1/L2/HBM decomposition: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)
1. **The GPU→CPU→GPU round trip per coordination point is removed**, replaced by a doorbell store plus a poll. This is the entire source of the coordination-latency result.
2. **Coordination is decoupled from data movement**, so ordering semantics do not force a data-path flush.
3. **Locking is eliminated** — the paper attributes its InfiniBand put-latency advantage over NVSHMEM to removing locking.
4. **Where it is slower / does not help** `[paper]`:
   - **GASNet-EX beats GICC on single-message active-message latency**: Table 3 gives 3.45 µs (GASNet-EX) vs 11.76 µs (GICC) on InfiniBand. GICC only wins once overhead amortizes across multi-message sequences. This is an unusually candid negative result and must be carried with the positive ones.
   - Canonical Cannon matrix multiply (one ring exchange per stage) shows minimal benefit.
   - The OFI path retains a host monitor thread costing ~1 µs per operation.

Numbers with qualifiers `[paper]`:
- **Per-coordination latency: 25.2 µs → 0.11 µs (reported as 229×) vs host-driven MPI on Tioga** (AMD MI250X, HPE Slingshot-11 / OFI-CXI).
- **Put latency 1.95× lower than NVSHMEM on InfiniBand** for small messages 4 B–1 KB: ~7.1 µs (GICC) vs 11.5–13.8 µs (NVSHMEM). *(Maple, NVIDIA GH200, InfiniBand HDR ConnectX-7, 2 nodes.)*
- **Jacobi weak-scaling efficiency 76.1% (GICC) vs 60.6% (MPI) at 64 GPUs** on MI250X/Slingshot.
- **Minimod stencil at 64 AMD MI250X: 42% parallel efficiency (GICC) vs 35.4% (MPI)**; MPI incurs 52% higher communication time.
- **Matrix multiply up to 6.4×** at 512×512 matrices, converging to parity at larger sizes.
- Motivating measurement: coordination consumes **>32% of runtime** in phase-heavy workloads.

## 12.12 Hardware generation dependence
The paper's central finding *is* a hardware dependence `[paper]`:
- **NVIDIA mlx5 InfiniBand**: GPU kernels post work-queue elements and ring doorbells directly — true **GPU-initiated**.
- **HPE Slingshot-11 / OFI-CXI**: GPUs cannot dynamically enqueue; the host pre-stages bounded operations into a DWQ and the GPU only triggers them. The paper itself calls this **"GPU-triggered" rather than GPU-initiated**.
- CXI resource ceilings (256 DWQ entries, 2047 counters) are hard hardware limits that bound scalability.
- Evaluated on both AMD (MI250X, 8 GCDs/node) and NVIDIA (GH200), so the runtime is not vendor-locked; the *fabric* is what changes the mechanism.

## 12.13 Limitations
Author-stated `[paper]`:
1. **OFI pre-staging constraint**: the GPU can only trigger pre-prepared operations, restricting coordination to regular or semi-regular patterns.
2. **Finite NIC resources**: DWQ 256 entries, counter range 2047 shared across ranks ⇒ ~21 simultaneously pre-staged barrier instances at P=4096. Sliding-window double-buffering mitigates but cannot remove the ceiling.
3. **Semantic portability gap**: code tuned for InfiniBand's direct posting may stall on OFI's triggered execution.
4. **Fail-stop assumption**: no fault tolerance; message loss and node failure out of scope.
5. **Single-exchange patterns gain little** (canonical Cannon).
6. Scale reached: 64 GPUs on Tioga, 2 nodes on Maple — modest relative to the P=4096 analysis.

## 12.14 Relation to prior corpus
- No prior in-repo analysis. `[repo-grep]` `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` applies.
- **This is the pivotal paper for the control-placement taxonomy in this cluster.** Its related-work table classifies the field explicitly `[paper]`: NVSHMEM — GPU-initiated on InfiniBand, host-mediated on Slingshot/OFI, and offering no GPU-driven barriers or collectives there; rocSHMEM — same limitation; NCCL — GPU-initiated on IB, host-driven on OFI, and focused on collective *algorithms* rather than kernel-level synchronization; GPU-aware MPI — entirely host-orchestrated; GASNet-EX — CPU-driven RMA.
- **Complementary / contrasting** to `GPU-SC26-21`: that paper reaches device-resident collectives by assuming GDAKI inside an NVLink domain; GICC shows what must be given up when the fabric is OFI/CXI instead.
- **Contrasting** to `GPU-ASPLOS26-01` (MSCCL++): MSCCL++ accepts a host proxy thread for RDMA and states the hardware requires it; GICC shows that on mlx5 InfiniBand it does not, and on CXI it does but can be reduced to triggering.
- **Direct counterpoint** to `GPU-IPDPS26-02` (Big Send-off), which stays fully host-initiated on the same class of fabric (Slingshot-11).
- The artifact of `aCG` (SC 2025, watchlisted in this cluster's ledger) is the closest measured CPU-vs-GPU-initiated comparison available; GICC's contribution is orthogonal — it is about coordination rather than halo exchange.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** The contribution exists only because a GPU kernel cannot cheaply return control to a host: the entire value proposition is removing the GPU→CPU→GPU round trip at coordination points. The mechanisms are GPU-and-NIC specific — a GPU kernel writing an mlx5 User Access Region doorbell, NIC counters mapped into GPU-addressable memory, and GPU threads polling NIC-written sequence numbers. On a CPU, "coordination without returning to the host" is not a meaningful statement.

**Control placement**: **fabric-dependent, and the paper draws the distinction itself.**
- On **InfiniBand (mlx5)**: `device-resident` — GPU kernels construct work-queue elements and ring NIC doorbells with no host involvement.
- On **OFI/CXI (Slingshot-11)**: `device-triggered` — the host pre-stages bounded NIC operations into a Deferred Work Queue with counter thresholds, and GPU kernels only issue doorbell writes that advance GPU-mapped counters. The paper's own term is **"GPU-triggered rather than GPU-initiated"**. A lightweight host monitor thread additionally drives libfabric progress at ~1 µs per operation, so the host is off the fast path but not absent.
Established from the full text (fabric-path and progress-engine sections), not from an abstract. `[paper]`

verdict_basis: The contribution is defined by the GPU's inability to cheaply yield to the host and by GPU-side NIC access mechanisms (mlx5 UAR doorbell from a kernel, CXI counters mapped into GPU memory, GPU-thread polling of NIC-written flags); it also supplies the field's sharpest hardware-grounded distinction between GPU-initiated and GPU-triggered control.

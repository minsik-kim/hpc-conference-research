# GPU-ICS25-162 — A Device-Side Execution Model for Multi-GPU Task Graphs (Mustard)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `J — GPU runtime, task graphs and scheduling`
secondary_topics: `multi-GPU / NVSHMEM device-side communication; device-side memory allocation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation (CPU-driven runtime overhead, StarPU vs CUDA Graphs); background on CUDA Graphs and device-side graph launch incl. the 120-graph limit; design (graph enrichment, DU/DW/DT vertices, subgraph coarsening, device-side Broker queue over NVSHMEM atomics, GPU-side scheduler kernel/Algorithm 2, occupancy tracking); implementation (Ouroboros device-side allocator, cuBLAS/cuSOLVER integration, NVSHMEM for multi-node); limitations. Read via one full-text pass over the ICS 2025 proceedings PDF hosted at hpcrl.github.io. **The evaluation section — GPU SKUs, node counts, benchmark set, baselines and speedup numbers — was NOT returned by that pass and is recorded as NOT_READ throughout; no performance number is asserted.**`

## 12.1 Bibliographic facts

- Title: *A Device-Side Execution Model for Multi-GPU Task Graphs* `[paper]`. The system is named **Mustard** in the text. `[paper]`
- Authors: Ilyas Turimbetov (Koç University, Istanbul); Mohamed Wahib (RIKEN Center for Computational Science, Tokyo); Didem Unat (Koç University, Istanbul) `[paper]`
- Venue: ICS '25, Salt Lake City UT, 8–11 June 2025, "GPU Scheduling" session. DOI `10.1145/3721145.3730426` `[paper]` `[census/ICS_2025.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Full text used: https://hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-66.pdf `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` in this pass → no repository or commit asserted; `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

CUDA Graphs removed the host from the critical path of a *single*-GPU task graph, but in a multi-GPU setting load balancing and inter-GPU dependency resolution went back to the programmer and the CPU — can the scheduling logic itself be compiled *into* the graph, so that a multi-GPU task graph runs with the CPU used "solely for task graph initialization"? `[paper]`

## 12.3 GPU/HPC problem translation

- **Scheduling (primary).** The object being moved is the *scheduler*, from host to device. "The interplay of runtime components, CPU-driven kernel initialization, and dynamic task graph construction creates significant overhead." `[paper]`
- **Synchronization (co-primary).** Dependency counters must be decremented by a producer on one GPU and observed by a consumer on another. This requires atomics whose visibility spans devices and, for multi-node, spans nodes.
- **Communication.** Data movement between GPUs becomes graph vertices rather than host-issued calls: `cudaMemcpy` within a node, NVSHMEM across nodes. `[paper]`
- **Compute.** Occupancy — threads, blocks and memory in use per device — becomes state the device-side scheduler must track in order to decide whether it may launch another subgraph.

## 12.4 Why the problem exists (hardware root cause)

1. **Kernel launch is a host→device transaction with a fixed cost, and a task graph has many of them.** This is the cost CUDA Graphs was built to amortise: a graph "allows for low-overhead static scheduling of task graphs … [whose] kernels … can be executed entirely on the GPU without engaging the host". `[paper]` The quantified consequence of *not* doing this: StarPU, efficient on CPUs, can be "up to 13x slower compared to CUDA Graphs" on GPUs. `[paper]`
2. **CUDA Graphs' automatic scheduling stops at the device boundary.** "In a single-GPU setting scheduling of the graph's kernels … is done automatically", but multi-GPU "load balancing and management of inter-GPU communications … remains contingent on the programmer's decisions and is only possible within a single node." `[paper]` So the programmer must statically assign vertices to GPUs — and "optimal scheduling may be difficult to achieve, since the execution time of graph nodes is unclear in advance and there is no runtime inter-GPU load balancing mechanism." `[paper]`
3. **Device-side atomics did not span GPUs until recently.** The paper is explicit that this was the blocker: "Queueing for multi-GPU systems has been done through the CPU … only recently, NVSHMEM bridged the gap by introducing multi-GPU atomics." `[paper]` Mustard exists because a hardware/runtime capability arrived, not because an algorithm was invented.
4. **Device-side graph launch has a hard numeric cap.** "Device-side graph launch comes with a limitation, which requires the number of graphs submitted to a device to be no more than **120**." `[paper]` This single constant shapes the entire design: it forces the task graph to be *coarsened into at most 120 subgraphs per device* rather than executed vertex-by-vertex.

## 12.5 Mathematical / performance model

No analytic model is given in the sections read. The design constants and structural rules are:

- **≤ 120 subgraphs per device**, from the device-side graph-launch limit. `[paper]` Subgraphs are the scheduling quantum: "Subgraphs serve as work items to be scheduled … The task graph vertices … are coarsened into subgraphs … The cut edges represent a dependency update and potential inter-device communication." `[paper]`
- **Dependency counting.** Each vertex carries a counter decremented by its parents; a remote dependency inserts an extra vertex "between the parent and a child. Since the child will be executed on a remote GPU, it needs to be able to poll from the same memory address that is being decremented by the parent." `[paper]` Vertex classes: **DU** (dependency update), **DW** (dependency wait), **DT** (data transfer). `[paper]`
- **Occupancy accounting.** "Mustard aims to maintain information about the amount of memory being allocated and the number of CUDA threads and blocks in use." `[paper]` Implemented as single-thread kernels fused with the dependency-update kernels: "each kernel is enclosed by two dependency update kernels … increment and decrement signs … occupancy and dependency update kernels are fused together." `[paper]`

## 12.6 Data layout and ownership

- **thread → block → kernel:** unchanged. Mustard's explicit claim is that "a single-GPU CUDA Graph can be executed across multiple GPUs **without requiring kernel code modifications**". `[paper]` This is the sharpest contrast with the sharing papers in this cluster, which all require either kernel-source cooperation (SGDRC) or per-model profiling (ParvaGPU).
- **kernel → vertex → subgraph:** a subgraph is the unit of ownership transfer between GPUs. A subgraph is claimed by exactly one device's scheduler from the shared queue.
- **GPU → device-side queue:** "we employ a device-side queue"; the implementation is "the Broker queue [26] … reimplemented with NVSHMEM atomics, introducing GPU-side queues that are consistent even in multi-GPU systems." `[paper]` Ownership of a work item is transferred by an atomic dequeue executed *by a GPU thread*, not by the host.
- **GPU → node → cluster:** within a node, dependency atomics and `cudaMemcpy`; across nodes, NVSHMEM atomics and NVSHMEM transfers. `[paper]`
- **Memory:** device-side dynamic allocation via **Ouroboros**, which "uses `cudaMalloc` API to reserve all the available memory in the initialization stage, [so] the memory pointers created by Ouroboros malloc calls can be shared with other devices." `[paper]` Reserving the whole device up front is what makes a device-allocated pointer meaningful to a peer.

## 12.7 Pseudo code

Algorithm 2 is quoted verbatim from the paper `[paper]`; the enrichment sketch is `[reconstruction]` over paper-named steps.

```
# Algorithm 2 — GPU-side scheduler (persistent kernel)    # [paper] verbatim
while q.itemsDequeued != S.size:
    if !O[deviceID].isBusy():
        int sID = q.dequeue()
        cudaGraphLaunch(S[sID])

# Graph enrichment (host, once; Algorithm 1 per the paper) # [reconstruction] over [paper] steps
enrich(G):
    partition G into subgraphs S, |S| <= 120 per device     # [paper] limit
    for each edge (u,v) cut across devices:
        insert DU vertex after u   # atomic decrement       # [paper]
        insert DW vertex before v  # poll same address      # [paper]
        insert DT vertex           # cudaMemcpy | NVSHMEM   # [paper]
    for each kernel k:
        wrap k with occupancy increment / decrement kernels # [paper]
        fuse occupancy + dependency-update kernels          # [paper]
```

Note what Algorithm 2 shows about the design: the scheduler kernel is itself **persistent** and calls `cudaGraphLaunch` from device code. The paper is careful to distinguish this from a megakernel approach — it *avoids* persistent kernels everywhere except the scheduler, by "splitting graph vertices into separate cudaGraphs and schedul[ing] them from a long-running device-side kernel." `[paper]`

## 12.8 Real implementation

No artifact located → `NOT_FOUND_AFTER_SEARCH`; nothing is asserted about a repository. The symbols and third-party components the paper itself names:

| Symbol / component | Role, as stated by the paper |
|---|---|
| `cudaGraphLaunch` | called **from device code** inside the scheduler kernel to launch a subgraph `[paper]` |
| `cudaMemcpy` | intra-node DT vertices `[paper]` |
| `cudaMalloc` | used by Ouroboros at init to reserve all device memory `[paper]` |
| NVSHMEM atomics | cross-GPU and cross-node dependency counters; the Broker-queue reimplementation `[paper]` |
| NVSHMEM transfers | inter-node DT vertices `[paper]` |
| Broker queue (ref. [26]) | the lock-free queue design reimplemented on NVSHMEM atomics `[paper]` |
| Ouroboros | device-side dynamic memory allocator `[paper]` |
| cuBLAS, cuSOLVER | integrated into the model; the paper notes they "choose thread block and thread count automatically" `[paper]` |

**Evaluation numbers are `NOT_READ`** — the pass over the PDF returned design and limitations but not the experimental section. No speedup, GPU SKU, node count or benchmark set is recorded here, and none may be quoted from this file.

## 12.9 Kernel execution

The execution chain is the point of the paper:

1. **Host** builds, partitions and enriches the graph, then performs one launch. "The CPU is used solely for task graph initialization." `[paper]`
2. **Scheduler kernel** (persistent, one per device) loops: check this device's occupancy record → atomically dequeue a subgraph ID → `cudaGraphLaunch` it. `[paper]`
3. **Subgraph** runs as an ordinary CUDA graph on that device; its internal kernel→block→warp behaviour is untouched.
4. **DU vertices** atomically decrement successor counters — via NVSHMEM when the successor is remote. **DW vertices** poll the same address. `[paper]`
5. **DT vertices** move the data.

The critical correctness requirement the paper names is GPU-wide synchronisation: "to ensure that all threads in all blocks have concluded the kernel execution" before a dependency is signalled. `[paper]` Graph enrichment is the answer — the DU vertex is a *separate graph node*, so the graph's own edge ordering provides the guarantee that a device-wide barrier inside a kernel could not.

## 12.10 Memory traffic

- **Data traffic** is explicit and scheduled: DT vertices, `cudaMemcpy` intra-node, NVSHMEM inter-node. `[paper]`
- **Metadata traffic** is the new cost: every cut edge adds an atomic decrement and a poll loop. Cross-node atomics ride NVSHMEM. No quantification of this overhead was in the read sections → `NOT_IN_PAPER` / `NOT_READ`.
- **Capacity pressure from the graph itself** is a stated limitation: "cudaGraph, when scaled to millions of vertices, can occupy the entire memory of a device." `[paper]` The graph is data resident in device memory, and it competes with the application's own working set — an unusual and important cost that has no analogue in host-side runtimes.
- No HBM/L2-level analysis → `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed)

Mechanistic causes, stated without any performance number (none was read):

- **Removed:** per-kernel host→device launch transactions and host-side runtime bookkeeping for every vertex; the comparison anchor the paper gives for this class of cost is StarPU being "up to 13x slower compared to CUDA Graphs". `[paper]`
- **Removed:** the programmer's static device assignment, replaced by runtime work stealing from a device-side queue — which is the only way to get load balance when "the execution time of graph nodes is unclear in advance". `[paper]`
- **Added:** DU/DW/DT vertices per cut edge, occupancy-tracking kernels around every kernel, the persistent scheduler occupying resources on every device, and device memory consumed by the graph structure itself.
- **Structurally bounded:** the ≤120-subgraph cap means coarsening is mandatory, and coarsening reduces the scheduler's freedom. The paper calls this "the most important and restraining" limitation. `[paper]`

## 12.12 Hardware generation dependence

- Requires **device-side CUDA graph launch** (a CUDA 12-era feature) and its 120-graph cap — a runtime/driver constant, not an architectural one, and one that could change. `[paper]`
- Requires **NVSHMEM multi-GPU atomics**, which the paper dates as recent. `[paper]` NVLink/NVSwitch-class connectivity is implied for intra-node atomic performance but is not characterised in the read sections → `NOT_IN_PAPER`.
- Nothing depends on SM counts or on a partition lattice, so the design is not tied to a specific SKU in the way MIG-based work is.

## 12.13 Limitations

Stated by the paper:
- **≤120 subgraphs per device** — "the most important and restraining one". `[paper]`
- **"Multi-node execution is only possible without dynamic load balancing."** `[paper]` The device-side queue's work stealing does not extend across nodes — a substantial scope limit that any reader should carry.
- **Vendor libraries defeat occupancy tracking:** "Libraries such as cuSOLVER and cuBLAS choose thread block and thread count automatically, limiting the efficiency of occupancy tracking." `[paper]`
- **Graph memory footprint** at millions of vertices. `[paper]`

Added here:
- **Evaluation not read in this pass** → the cost/benefit balance above is mechanistic only. This paper should be re-read for its experimental section before any quantitative claim is made from it.

## 12.14 Relation to prior corpus

- **Same cluster, different axis.** Every other paper analysed in this cluster partitions *one* GPU among tenants; Mustard aggregates *many* GPUs for one application. It is the task-graph/runtime half (taxonomy J) rather than the sharing half (K), and it is the cluster's clearest statement of what "GPU runtime" means when the host is removed.
- **Task-graph data point, ledger owned elsewhere:** CUDASTF (SC 2024) is the other CUDA task-graph system in this corpus; **its ledger row is owned by the compiler cluster** and is adjudicated here only as a comparison point. The contrast is that CUDASTF is a host-side task/stream programming model, whereas Mustard's contribution is moving the scheduler onto the device. No claim about CUDASTF's content is made from this file.
- **Device-initiated execution lineage, already analysed:** `GPU-HPDC26-01` (GICC, GPU-initiated communication coordination runtime) and `GPU-ICS25-01` (DREAM, device-driven access to virtual memory) are the same architectural move applied to communication and to memory respectively — the host being removed from a control path it historically owned. Mustard completes the set for *scheduling*. These three together are the strongest lineage claim available from this cluster.
- **Contrast within this cluster:** Mustard uses a persistent kernel *only* for the scheduler and explicitly rejects the megakernel style `[paper]`; SGDRC (`GPU-PPoPP25-164`) uses persistent-thread kernels for the *application's* work in order to control SM placement. Same primitive, opposite purposes.
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — `domains/ai_hpc_systems/` (`EXTERNAL_IMPORT_PENDING`) covers runtimes; no claim made.
- **`domains/hpc_systems_operations/`:** checked; nothing on GPU task graphs or device-side runtimes. No `GPU_DELTA_ANALYSIS` owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution exists only because of two GPU-specific runtime properties and one GPU-specific constant. (a) The *kernel-launch boundary* is a host→device transaction expensive enough that a host-side task runtime is "up to 13x slower compared to CUDA Graphs"; the whole point is to eliminate it. (b) The mechanism is **device-side `cudaGraphLaunch` from inside a persistent kernel**, gated by NVSHMEM's recently-introduced multi-GPU atomics — neither has a CPU analogue, since a CPU thread has always been able to enqueue work and take a lock. (c) The design is shaped by the **120-graphs-per-device** device-side-launch cap, which forces subgraph coarsening. `[paper]` A CPU task-graph runtime with work stealing is a solved, decades-old problem; nothing here would be publishable in that setting.

**Isolation mechanism: none — this is a task-graph runtime, not a sharing system.** Its scheduling quantum is the subgraph, claimed via device-side atomics; the only resource guard is voluntary occupancy accounting (threads, blocks, memory) maintained by fused single-thread kernels, which vendor libraries can defeat. `[paper]`

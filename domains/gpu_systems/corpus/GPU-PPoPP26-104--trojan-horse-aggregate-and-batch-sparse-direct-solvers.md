# GPU-PPoPP26-104 — Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `G — Sparse/irregular GPU kernels (sparse direct solvers, task batching, load balancing)`
secondary_topics: `H — irregular/DAG workloads; multi-GPU and multi-node scaling; batched BLAS/LAPACK kernel design; CPU-side scheduling for GPU execution`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author PDF (https://www.ssslab.cn/assets/papers/2026-li-TrojanHorse.pdf) — title/authors/affiliations, abstract, introduction and the two stated challenges, the four modules (Prioritizer, Container, Collector, Executor), the CUDA-block-to-task mapping and binary-search lookup, the four kernel types GETRF/TSTRF/GESSM/SSSSM and their per-kernel block assignment, CSC-vs-dense task handling and selective atomics, supernode/elimination-tree integration for both SuperLU_DIST and PanguLU, the full evaluation setup (three scale-up GPUs, two scale-out clusters, matrix suites, all solver baselines with versions), headline scale-up and scale-out numbers, the kernel-count and kernel-efficiency metrics, the stated limitations, and related work. Abstract cross-checked against the official PPoPP 2026 TOC (conference-publishing.com/toc/PPOPP26/abs).`

## 12.1 Bibliographic facts

- Title: **Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters** [paper]
- Venue: **PPoPP 2026**, session "Cluster and Cloud Computing"; **Best Paper Nominee** [census: `domains/gpu_systems/census/PPoPP_2026.md`]. DOI suffix `3786442` [census]; full DOI `10.1145/3774934.3786442` [census].
- Authors, all **SSSLab, Dept. of Computer Science and Technology, China University of Petroleum-Beijing** [paper]: **Yida Li, Siwei Zhang, Yiduo Niu, Yang Du, Qingxiao Sun, Zhou Jin, Weifeng Liu**. (Author list independently confirmed against the official PPoPP 2026 TOC [official-web].)
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Full text used: `https://www.ssslab.cn/assets/papers/2026-li-TrojanHorse.pdf` [paper].
- Artifact: none located. `NOT_INSPECTED`. No source symbols asserted.

## 12.2 Core question (one sentence)

Sparse direct factorisation decomposes into thousands of *tiny, heterogeneous, dependency-constrained* tasks — too small to fill a GPU individually and too dissimilar for any existing batched-BLAS interface — so can a **plug-in** that aggregates them on the CPU by DAG priority and executes the mixed batch in **one unified GPU kernel** finally make GPU sparse direct solvers beat their CPU counterparts?

## 12.3 GPU/HPC problem translation

- **Compute.** The stated deficit: unlike dense factorisation, which offers "large submatrices (thousands of orders)", sparse multifrontal/supernodal decomposition yields "small submatrix blocks (often with tens of orders and thousands of nonzero elements)" [paper]. Individually these cannot saturate an SM array.
- **Scheduling / load imbalance.** The central contribution. Tasks must be batched, but batching is constrained by the DAG; the Prioritizer ranks ready tasks by **distance to the main diagonal** (critical-path proxy) and the Container defers the rest in a priority heap "ensuring the highest-priority task among those it stores is retrieved first to prevent premature execution" [paper].
- **Synchronization.** Kernel-launch count is an explicit measured quantity: launches fall to **1.10% (SuperLU) and 1.48% (PanguLU)** of the baseline count [paper]. That is a ~91× and ~68× reduction in launch boundaries.
- **Dependency.** The elimination tree / task DAG is the constraint the whole design negotiates. SuperLU_DIST uses supernodes, PanguLU uses sparse blocks; both form elimination trees or DAGs [paper].
- **Communication.** Scale-out over 16 GPUs across two nodes (400 Gbps InfiniBand) or four nodes (200 Gbps IB) [paper]; the paper reports that speedups *shrink* at scale-out, attributing it to communication.

## 12.4 Why the problem exists (hardware root cause)

- A GPU kernel launch has a fixed cost and a grid-wide serialisation semantics; a solver that issues one launch per tiny factorisation task pays that cost thousands of times while each launch occupies a handful of SMs. The paper attacks the *number* of launches directly, and measures it.
- Existing **batched** kernels (batched GETRF etc.) assume *homogeneous* work. Sparse solver tasks violate every assumption at once: "arbitrary matrix sizes (typically up to a few thousand orders); variable sparsity levels; three kinds of kernels; and two kinds of dependency relationships" [paper]. So the batched-BLAS interface, the standard GPU answer to small work, does not apply.
- The Executor's answer is a **one-kernel-many-task-types** design held together by "an array mapping from CUDA blocks to tasks" with **binary search lookup during execution** [paper]. The binary search is the price of letting a single grid host heterogeneous tasks: a block must first discover *which* task and *which* kernel type it is.

## 12.5 Mathematical / performance model

No closed-form model is given. The paper's quantitative frame is a pair of *ratios* [paper], which is the right frame for this contribution:

- **Kernel count ratio** (Trojan Horse / baseline): **1.10%** for SuperLU_DIST, **1.48%** for PanguLU.
- **Kernel execution efficiency gain**: **15.02×** for SuperLU, **2.92×** for PanguLU.

The gap between the two solvers is itself informative: SuperLU_DIST's supernodes are small, so it suffers more from launch overhead and gains far more (15.02×); PanguLU's sparse blocks are already coarser (block size 512), so the headroom is smaller (2.92×). The end-to-end speedups follow the same ordering.

Tuning constants recorded [paper]: **maximum supernode size 256 in SuperLU**, **block size 512 in PanguLU**.

## 12.6 Data layout and ownership

- **CPU side (Aggregate stage)** [paper]:
  - **Prioritizer** — walks the task DAG, finds ready tasks, assigns urgency by distance to the main diagonal; critical-path tasks are high priority, the rest deferred.
  - **Container** — a **priority queue (heap)** holding deferred low-priority tasks.
- **GPU side (Batch stage)** [paper]:
  - **Collector** — two-phase assembly: first take the urgent tasks from the Prioritizer, then top up from the Container while GPU resource limits allow.
  - **Executor** — one unified kernel; a **block→task array** plus **binary search** routes each CUDA block.
- **CUDA block → task granularity, per kernel type** [paper]:
  - **GETRF** (LU factorisation): **one block per column**.
  - **TSTRF** (upper triangular solve): **one block per row**.
  - **GESSM** (lower triangular solve): **one block per column**.
  - **SSSSM** (Schur-complement GEMM): **one block per element**.
- **Per-task storage**: both **CSC** and **dense**; dense tasks "bypass sparse index overhead" [paper].
- **shared memory**: TSTRF/GESSM blocks use shared memory "when data fits; otherwise using global memory" [paper]. No byte budget given — `NOT_IN_PAPER`.
- **atomics**: the Executor "selectively enables atomic operations to resolve write conflicts in order-independent Schur complement accumulation" [paper] — i.e. atomics are switched on only for SSSSM, where accumulation order does not matter.
- **node/cluster**: scale-out over 16 GPUs; per-process workflow, so each MPI rank runs its own Aggregate+Batch pipeline [paper].

## 12.7 Pseudo code

```
# --- CPU: Aggregate ---                                          [paper]
ready = prioritizer.scan_dag()                 # tasks with satisfied dependencies
for t in ready:
    if urgency(t) == HIGH:      # distance to main diagonal
        urgent_queue.push(t)
    else:
        container.push(t)       # priority heap; highest-priority pops first

# --- GPU: Batch ---                                              [paper]
batch = collector.take_all(urgent_queue)
while gpu_resources_remain(batch):
    batch.append(container.pop())              # top up with deferred work

block_to_task = build_mapping(batch)           # array, searched by binary search
launch executor_kernel(batch, block_to_task)   # ONE kernel, mixed task types

# --- Executor kernel, per CUDA block ---                         [paper]
task = binary_search(block_to_task, blockIdx)
switch task.type:
  GETRF: # one block per column; synchronization-free LEFT-LOOKING
         gather_to_dense_buffer(); vectorized_column_process(); scatter_back()
  TSTRF: # one block per row;    use shared memory if it fits, else global
  GESSM: # one block per column; ditto
  SSSSM: # one block per element; column-column multiply;
         # dense tasks skip sparse indexing; atomics ENABLED here only
```

`GETRF`, `TSTRF`, `GESSM`, `SSSSM`, Prioritizer, Container, Collector, Executor, "synchronization-free left-looking", gather-to-dense-buffer/scatter-back, and the per-kernel block granularities are all the paper's own [paper]. `binary_search`, `build_mapping`, `urgency` are `[reconstruction]` names for described mechanisms.

## 12.8 Real implementation

`NOT_INSPECTED`. No artifact URL located [paper]. No source symbols asserted. The kernel names `GETRF`/`TSTRF`/`GESSM`/`SSSSM` are standard PLASMA/tile-algorithm names that the paper uses; they are recorded as the paper's terminology, not as symbols read from code.

Integration facts [paper]: Trojan Horse is "a lightweight plug-in" requiring no solver rewrite. For **SuperLU_DIST** it additionally "aggregates matrix U vectors in advance to enable larger GEMM operations on Schur complements". For **PanguLU**, because that solver has its own internal task queue, **only the Schur-complement (SSSSM) tasks are delegated** and PanguLU's own task management is preserved — a partial integration the paper states plainly.

## 12.9 Kernel execution

kernel (one, heterogeneous) → CUDA block (routed to a task by binary search over the mapping array) → warp → instruction. The execution-level novelty is the **dissolution of the kernel↔task-type correspondence**: normally one kernel = one operation; here one kernel hosts four operations at four different block granularities simultaneously. The cost is a per-block binary search before any useful work; the benefit is that the GPU sees one large grid instead of thousands of tiny ones.

The name is apt and the paper means it: the batched kernel is the vehicle that smuggles thousands of unbatchable tasks past the launch boundary.

## 12.10 Memory traffic

- **GETRF** uses "gather-to-dense-buffer, vectorized column processing, then scatter-back" [paper] — i.e. the sparse column is densified into a buffer so the inner loop is coalesced and index-free, then scattered back.
- **Dense-vs-CSC task typing** removes index traffic for tasks dense enough to be worth it [paper].
- **shared memory** used opportunistically for TSTRF/GESSM [paper].
- No L1/L2/HBM breakdown, no bandwidth numbers. `NOT_IN_PAPER`.
- **Inter-node**: 400 Gbps InfiniBand (H100 cluster) / 200 Gbps (MI50 cluster) [paper]; no communication-volume analysis. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Scale-up, all qualifiers carried** — GPUs: **NVIDIA RTX 5060 Ti** (4,608 cores, 0.37 TFlop/s FP64, 16 GB, 0.45 TB/s), **RTX 5090** (21,760 cores, 1.64 TFlop/s, 32 GB, 1.79 TB/s), **A100 PCIe 40 GB** (6,912 cores, 9.75 TFlop/s, 1.56 TB/s). Matrices: 4 moderate (`c-71`, `cage12`, `para-8`, `Lin`) plus **200 additional SuiteSparse matrices on A100** [paper]:

- **SuperLU_DIST v9.1.0 + Trojan Horse: 5.47× average, up to 418.79×** (A100)
- **PanguLU v5.0.0 + Trojan Horse: 2.84× average, up to 5.59×** (A100)

**Scale-out** — **16× NVIDIA H100 SXM** (14,592 cores each, 25.61 TFlop/s, 80 GB, 2.04 TB/s; two nodes × 8 GPUs, 400 Gbps IB) and **16× AMD MI50 PCIe** (3,840 cores, 6.71 TFlop/s, 16 GB; four nodes × 4 GPUs, 200 Gbps IB). Matrices: `Ga41As41H72`, `RM07R`, `cage13`, `audikw_1`, `nlpkkt80`, `Serena` [paper]:

- **SuperLU_DIST: 3.5× average, up to 24.6×**
- **PanguLU: 1.9× average, up to 2.3×**

Other baselines run [paper]: **PaStiX v6.4.0 with StarPU v1.4.8**; on CPU, **SuperLU_DIST v9.1.0** and **MUMPS v5.6.0** on a 32-core **Intel Xeon 6462C**.

Decomposed cause [paper]:
1. **Launch-count collapse** to ~1.1–1.5% of baseline — the primary mechanism.
2. **Kernel execution efficiency** 15.02× (SuperLU) / 2.92× (PanguLU) — i.e. once batched, each kernel does far more useful work per unit time.
3. **Critical-path-aware ordering** prevents the batching from stalling the DAG (the Prioritizer/Container split exists precisely so that filling a batch does not run ahead of the critical path).
4. **Working against it at scale**: speedups fall from 5.47× to 3.5× going from one GPU to 16, "suggesting communication becomes more constraining" [paper].

**The claim that matters most**: with Trojan Horse, GPU-accelerated sparse direct solvers "now match or exceed CPU performance, reversing the historic CPU advantage" (H100 vs Xeon 6462C) [paper]. The paper frames this as ending a four-decade pattern in which sparse direct methods were "less competitive on GPUs than their CPU counterparts" [paper]. That is a strong claim resting on a specific hardware pairing and should always be quoted with it.

## 12.12 Hardware generation dependence

- Unusually broad hardware coverage for this cluster: **five distinct GPU SKUs across three NVIDIA generations plus AMD CDNA (MI50)** [paper]. That materially strengthens the generality claim relative to single-SKU papers such as Insum (`GPU-ASPLOS26-101`, RTX 3090 only) or SMaT (`GPU-SC24-102`, A100 only).
- No named generation-specific instruction is used — no MMA, no TMA, no `cp.async` is mentioned. The mechanism is block-granularity scheduling and atomics, which is why it ports to AMD. `NOT_IN_PAPER` for any PTX-level detail.
- Consequence: the contribution is *robust* across generations but says nothing about matrix units. This is a **scheduling** paper, not a datapath paper.

## 12.13 Limitations

Stated by the paper [paper]:
1. **SuperLU scheduling overhead** — small supernodes give a high launch frequency; mitigation needs pre-aggregating U-matrix vectors.
2. **Integration complexity** — PanguLU's internal task queue forces a *partial* integration (only Schur-complement tasks delegated).
3. **Scale-out gains diminish** — 3.5× at 16 GPUs vs 5.47× at one, communication-bound.
4. **Solver-specific tuning** — per-solver constants (supernode 256, block 512).

Not stated but visible from the numbers [inference, flagged]: the 418.79× maximum for SuperLU_DIST is an outlier of a kind that usually indicates a baseline pathology rather than a 400-fold algorithmic gain; the **5.47× average** is the number to carry.

## 12.14 Relation to prior corpus

- **Same laboratory** as `GPU-SC24-103` (Mille-feuille) — SSSLab/CUPB, with **Weifeng Liu** and **Zhou Jin** on both — and as PanguLU (SC 2023), which appears here as *both* a baseline and an integration target. The SSSLab line in this corpus is now: DASP (SC 2023, baseline in SMaT) → PanguLU (SC 2023) → AmgT + Mille-feuille (SC 2024) → Cubie + DiggerBees + Trojan Horse (PPoPP 2026).
- **Complementary to** `GPU-PPoPP26-105` (DiggerBees, also SSSLab + BSC): both are load-balancing-by-work-redistribution papers from the same lab in the same proceedings, but DiggerBees redistributes *at runtime on the device* (work stealing) while Trojan Horse redistributes *ahead of time on the host* (priority aggregation). Together they bracket the design space.
- **Contrast with** `GPU-PPoPP26-02` (Cubie, same lab): Cubie asks whether matrix units help general parallel patterns; Trojan Horse ignores matrix units entirely. Useful evidence that the group is not committed to a single mechanism.
- Adjacent to `GPU-MICRO24-41` (over-synchronisation in GPU programs) in subject matter.
- `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The problem being solved *is created by the GPU execution model*. Tiny factorisation tasks are not a problem on a CPU — a core simply runs them. They are a problem on a GPU because (a) each one is launched as a grid that occupies a fraction of the SMs, and (b) the launch boundary is a grid-wide serialisation. The solution is equally GPU-specific: a **single kernel whose CUDA blocks are routed by binary search to heterogeneous task types at four different block granularities** (one block per column / per row / per element), with **atomics selectively enabled only for the order-independent Schur-complement accumulation** and shared memory used opportunistically per task. The headline evidence is a *launch-count* metric (down to 1.10% / 1.48%), which has no CPU meaning at all.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Synchronisation — claimed and established.** Kernel count reduced to 1.10%/1.48% of baseline, measured directly.
- **Load imbalance / scheduling — claimed and established.** The Prioritizer/Container/Collector split is the mechanism; kernel-execution-efficiency gains of 15.02×/2.92× are the measurement.
- **Compute — claimed and established indirectly.** GPU saturation is the stated goal; efficiency gain is the proxy. No FLOP/s utilisation numbers — `NOT_IN_PAPER`.
- **Dependency — claimed and addressed.** Critical-path-aware urgency keeps batching from violating or starving the DAG. Not isolated by ablation — `NOT_IN_PAPER`.
- **Memory — not a claim of this paper**, beyond gather-to-dense-buffer for GETRF.

verdict: `CORE_GPU`

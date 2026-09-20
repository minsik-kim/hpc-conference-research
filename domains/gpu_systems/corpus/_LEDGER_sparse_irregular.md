# Sparse and irregular GPU kernels — SpMM/SpGEMM/SpMV, sparse solvers, graph and irregular workloads, load balancing and format design — GPU relevance verdict ledger

cluster: `G` (taxonomy G, with H overlap)
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

Verdicts are `CORE_GPU` / `RELATED_GPU` / `EXCLUDE` / `UNRESOLVED`.
Access states are `PUBLIC_FULLTEXT` / `CLOSED_ACCESS` / `PENDING_FULLTEXT` /
`PUBLIC_ARTIFACT_ONLY` / `ABSTRACT_ONLY`.
`evidence_read` records what was actually read — a verdict reached from an
abstract says `ABSTRACT_ONLY` and **may not** be used to justify a deep analysis.

**Counterfactual answer** records the answer to: "If a generic accelerator or a
CPU were used instead, would the core contribution be substantially the same?"
The **strict** version applies in this cluster: *a sparse algorithm with a CUDA
implementation is `RELATED_GPU` at best.* A `NO` must name the GPU-specific
property. `NO (provisional)` = the mechanism is evident from a confirmed
title/abstract but the paper was not read.

**Bottleneck class** column uses the five classes: compute / memory /
dependency / synchronisation / load imbalance.

**Tooling constraints that shaped access states** (do not re-derive):
`dl.acm.org` → 403, `ieeexplore.ieee.org` → 418, `dblp.org` → robots,
`par.nsf.gov` → robots-disallowed, `arxiv.org/search` / `export.arxiv.org` /
`web.archive.org` → unavailable, `conference-publishing.com/toc/PPOPP24|25/abs`
→ server-side "empty event record" error (the PPOPP26 equivalent works).
Several papers below are genuinely open access but unreachable from here; those
are `PENDING_FULLTEXT`, **not** `CLOSED_ACCESS`.

**Cross-ledger note.** `_LEDGER_tensor_cores.md` had already adjudicated the
Tensor-Core-based sparse papers and recorded a distinction this ledger
preserves: **FlashSparse and Acc-SpMM run *dense* MMA on denser blocks**,
whereas **SPIDER / Bridging the Gap / N:M reordering / Coruscant / Uni-STC use
actual 2:4 Sparse-Tensor-Core metadata**. Two papers newly deep-analysed here
(`GPU-SC24-102` SMaT, `GPU-ASPLOS26-101` Insum) are confirmed from full text to
sit on the **dense-MMA-on-blocks** side, with SMaT the earliest of that line.
Two rows in that ledger are **corrected** here from read full text — see §5.

---

## 1. Priority papers

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Bottleneck class addressed | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|---|
| Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums | ASPLOS 2026 | `PUBLIC_FULLTEXT` — arXiv 2510.17505, HTML v1 read. DOI 10.1145/3779212.3790176. Second host `spice.cs.umd.edu/proceedings/5_Insum.pdf` (unused). | `FULL_PAPER` — motivation, indirect-Einsum definition, GroupCOO/BlockGroupCOO with the `g* = sqrt(S/n)` derivation, PyTorch-FX lowering, the `ops.dot`/`tl.dot` and lazy-broadcasting TorchInductor extensions, 4 case studies, Figure 13 ablation, Table 3, related work. **No limitations section exists.** | **NO** — BlockGroupCOO's inner block is sized so `tl.dot` (Tensor Core) is legal; lazy broadcasting exists only to avoid register-fragment reshape against a fixed MMA operand layout; the +2.6× fusion win is the removal of an HBM round-trip between three GPU kernels. | **memory** (established: indirection-count minimisation, ≈8× grouping step) + **compute** (established: blocking → Tensor Core, ≈20× cumulative) + **synchronisation** (claimed via "fewer atomics", weakly established) — **load imbalance NOT claimed and NOT addressed** (fixed group size). | `CORE_GPU` | A one-line Einsum replaces 202–4491 lines of hand-written kernel; the GPU content is the block shape chosen for the matrix unit and the compiler surgery that lets gather→MMA→scatter fuse into one kernel. Single SKU (RTX 3090) is the main evidential weakness. | `GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md` |
| High Performance Unstructured SpMM Computation Using Tensor Cores (**SMaT**) | SC 2024 | `PUBLIC_FULLTEXT` — arXiv 2408.11551 HTML v1 read. DOI 10.1109/SC41406.2024.00060. | `FULL_PAPER` — BCSR blocking, Jaccard row clustering, Algorithm 1 warp model, `mma.m16n8k16` / `LDMATRIX_X2`/`X4` / `cuda::memcpy_async`, `T_tot = T_e·n_e + T_init`, 9-matrix SuiteSparse suite with sizes and sparsities, all baselines, C/B/T breakdown, the `dc2` failure, related work. | **NO** — the storage block (16×8) *is* the `m16n8k16` operand shape; `LDMATRIX` delivers the exact lane-to-element fragment layout; `cuda::memcpy_async` moves global→shared by DMA without touching registers. | **compute** (established: T-step ≈10×, 22× over naive) + **memory** (established) + **load imbalance** (**claimed, only partially addressed, and the paper says so** — reordering cuts `mip1` block-count σ by 8.4× but the static 2D schedule still loses ~28× to DASP on `dc2`). | `CORE_GPU` | The earliest of the dense-MMA-on-blocks SpMM line; its own breakdown shows the low-level kernel work (≈10×) dominates the reordering algorithm (≤2.4× block reduction), which contradicts the usual framing. 9-matrix suite is too small for a SuiteSparse-wide claim. | `GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md` |
| Mille-feuille: A Tile-Grained Mixed Precision Single-Kernel Conjugate Gradient Solver on GPUs | SC 2024 | `PUBLIC_FULLTEXT` — author PDF `ssslab.cn/assets/papers/2024-yang-Millefeuille-final.pdf` read. DOI 10.1109/SC41406.2024.00064. **Corrects the tensor-cores ledger's `CLOSED_ACCESS (effectively)`.** Artifact `github.com/SuperScientificSoftwareLaboratory/Mille-feuille` `NOT_INSPECTED`. | `FULL_PAPER` — three motivating findings, the two-level tile format and its arrays, per-nonzero precision criterion (10⁻¹⁵ loss threshold), the `d_s`/`d_d`/`d_a` dependency arrays and Steps A–D, Algorithms 4 & 5, SpTRSV preconditioner, A100 + MI210 setup, 230 SPD + 686 nonsymmetric SuiteSparse matrices, 4 baselines with versions, Figure 11 ablation, Table II, 5 stated limitations, related work. | **NO** — the dominant win is removing the CUDA **kernel-launch boundary**, replaced by a hand-built software grid barrier (`atomicSub`/`atomicAdd` + `__threadfence()` busy-waits, chosen over `__grid_sync()` for portability); the ~10⁶-nnz applicability ceiling is set by shared memory per SM. | **synchronisation** (established: >30% of baseline runtime; best speedups where the baseline's sync share >50%) + **memory** (established: 1.03×–1.65× from mixed precision, honestly bounded) + **dependency** (addressed in-kernel, not separately quantified) — **load imbalance claimed but NOT established** (heuristic tile distribution, no imbalance measurement). | `CORE_GPU` | **Verdict upgraded from the tensor-cores ledger's `RELATED_GPU`** now that the text is read: no matrix unit is involved anywhere (that ledger's suspicion was right), but persistent-kernel grid synchronisation and shared-memory residency are GPU-specific mechanisms. Runs on **AMD MI210** as well as A100 — rare cross-vendor evidence. | `GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md` |
| Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters | PPoPP 2026 (Best Paper Nominee) | `PUBLIC_FULLTEXT` — author PDF `ssslab.cn/assets/papers/2026-li-TrojanHorse.pdf` read; abstract cross-checked against the official PPoPP26 TOC. DOI 10.1145/3774934.3786442. | `FULL_PAPER` — the two stated challenges, all four modules, the CUDA-block→task array with binary-search routing, the four kernel types and their per-kernel block granularities, CSC-vs-dense typing and selective atomics, SuperLU_DIST and PanguLU integration, five GPU SKUs across two vendors, 200+ SuiteSparse matrices, all solver baselines with versions, kernel-count and kernel-efficiency metrics, 4 stated limitations, related work. | **NO** — the problem is *created by* the GPU launch model (thousands of tiny grids, each a grid-wide serialisation); the solution is one kernel hosting four task types at four different block granularities, routed per-block by binary search, with atomics enabled only for the order-independent Schur-complement accumulation. The headline metric (kernel count → 1.10%/1.48%) has no CPU meaning. | **synchronisation** (established: launch count to 1.10% / 1.48% of baseline) + **load imbalance / scheduling** (established: kernel-execution efficiency 15.02× / 2.92×) + **compute** (established indirectly) + **dependency** (addressed via critical-path urgency; not ablated). | `CORE_GPU` | The strongest hardware coverage in this cluster — five SKUs, three NVIDIA generations plus AMD MI50 — and the claim that GPU sparse direct solvers now match or beat CPU (H100 vs Xeon 6462C). Carry the **5.47× average**, not the 418.79× outlier. | `GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md` |
| Ocean: Fast Estimation-Based Sparse General Matrix-Matrix Multiplication on GPU | ICS 2026 | `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT` — arXiv 2604.19004 HTML v1 read; artifact `github.com/CornellHPC/Ocean-SpGEMM` **cloned and read**, pinned at `cb093963f6e45d9deabf7848bc05a538af796315`. DOI 10.1145/3797905.3807868. | `FULL_PAPER + CODE` — the 28%-symbolic motivation, HyperLogLog construct-and-merge, precision configuration and measured error, the ER/CR workflow-selection table, hybrid accumulators, the split hash table, binning, overflow fallback, Perlmutter A100 + DeltaAI H100 setup, 337 square + 64 rectangular SuiteSparse matrices, all baselines, V1–V4 ablation, the 2.2× memory cost and the `JP` failure, 4 stated limitations. Code: `hllAdd`/`hllConstruct`, `SymbolicHashmap.ids_shared`, `NumericHashmap`, `atomicMax`/`atomicCAS`/`atomicAdd`, `__shfl_down_sync`. | **NO** — the symbolic pass exists only because **shared memory is allocated per block at launch and cannot be resized**; HLL is chosen because its update is a single **`atomicMax`** and not a CAS loop; the split hash table (indices in shared, values in global) is chosen because **FP64 shared-memory atomics are emulated as CAS loops on NVIDIA GPUs while global atomics are hardware fire-and-forget**. | **compute** (established: 28% symbolic share removed; V2 = 1.30×) + **synchronisation** (established: the CAS-vs-hardware-atomic argument, confirmed in code) + **memory** (established but **costs 2.2× peak memory** and loses one matrix) — **load imbalance weakly established** (geometric binning; no imbalance metric). | `CORE_GPU` | The only paper in this cluster whose artifact was read; the code discloses two things the paper does not — the sketch is widened to `uint32_t` because *"CUDA does not support atomic operations on `uint8_t`"*, and the numeric hash is `id * 11`, not MurmurHash. Reports its own 0.55× loss on `torso1`. | `GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md` |
| A Row Decomposition-based Approach for Sparse Matrix Multiplication on GPUs (**RoDe**) | PPoPP 2024 | `CLOSED_ACCESS` + `PUBLIC_ARTIFACT_ONLY` — DOI 10.1145/3627535.3638470; `dl.acm.org` 403; **no author PDF exists** (the Tsinghua CRAFT Lab publication page hosts metadata only, verified by fetch; ResearchGate is request-only). Artifact `github.com/CRAFT-THU/RoDe`. | `TITLE_AND_CENSUS_ROW` + **corroborating citation evidence**: RoDe is a named CUDA-core baseline in FlashSparse (`GPU-PPoPP25-01`), where FlashSparse reports geomean **3.22× over RoDe for SpMM on RTX 4090** and **2.92× (up to 18.59×) over RoDe for SDDMM on H100**. Abstract fragment recovered: "SpMM and SDDMM are important sparse kernels in various computation domains." | **NO (provisional)** — row decomposition is a *load-balancing* device: rows are split by length so warps get comparable work, which is a warp-granularity concern. | **load imbalance** (provisional, the title's whole premise) — not verifiable without the text. | `CORE_GPU` | The reference CUDA-core SpMM/SDDMM baseline of this period; every Tensor-Core SpMM paper in the sibling ledger measures against it. **Highest-value blocked item in this cluster** — no free full text exists anywhere reachable. | — (watchlist; **top access target**) |
| Caracal: A GPU-Resident Sparse LU Solver with Lightweight Fine-Grained Scheduling | SC 2025 | `CLOSED_ACCESS` — DOI 10.1145/3712285.3759792, pp. 1477–1494; `dl.acm.org/doi/full/...` renders an HTML view but returns 403 here; no arXiv, no author PDF, no artifact located. | `TITLE_AND_CENSUS_ROW`. | **NO (provisional)** — "GPU-**resident**" plus "fine-grained scheduling" names device-side task scheduling without host round-trips, i.e. a persistent-kernel/on-device-queue mechanism. | **synchronisation** + **dependency** + **load imbalance** (provisional, from the title's "GPU-resident" and "fine-grained scheduling"). | `CORE_GPU` | Directly comparable to `GPU-PPoPP26-104` (Trojan Horse) — same problem, opposite placement of the scheduler (on-device vs host-side aggregation). **The single most useful unread paper for this cluster's synthesis.** | — (watchlist; **highest research value among blocked items**) |
| Swift: High-Performance Sparse-Dense Matrix Multiplication on GPUs | HPCA 2026 | `CLOSED_ACCESS` — DOI 10.1109/HPCA68181.2026.11408479, `ieeexplore` 418; no preprint or author PDF located. **Abstract obtained** from the official HPCA 2026 detail page. | `ABSTRACT_ONLY` (official conference page) + census row. Authors: Jinyu Hu, Huizhang Luo (Hunan University), Hong Jiang (UT Arlington), **Marc Casas (BSC)**, Kenli Li, Chubo Liu. Abstract states **data loading overhead exceeds 32% of overall performance**, that existing solutions fail to support **coalesced memory access for both the sparse and the dense operand simultaneously**, and that Swift improves loading efficiency by **sorting and load balancing**, evaluated against four state-of-the-art solutions on **SuiteSparse**, on **RTX 4080s and RTX 3090Ti**. | **NO** — "coalesced memory access for both sparse and dense matrices" is a memory-transaction-granularity property of the GPU, and it is the paper's stated gap. This is a full `NO`, not provisional: the abstract names the GPU property explicitly. | **memory** (claimed: 32% loading overhead, coalescing) + **load imbalance** (claimed: sorting and load balancing). Establishment `UNKNOWN` — no text read. | `CORE_GPU` | Same coalescing-against-the-sparsity-pattern problem FlashSparse solves with a 2×2 thread shuffle, attacked one generation later without the matrix unit. Marc Casas also co-authors DiggerBees (`GPU-PPoPP26-105`) and BerryBees. **Abstract-only ⇒ no deep analysis.** | — (watchlist) |
| SparseWeaver: Converting Sparse Operations as Dense Operations on GPUs for Graph Workloads | HPCA 2025 | `CLOSED_ACCESS` (the paper) + `PUBLIC_FULLTEXT` (an **author PhD-thesis chapter** covering the same work: `corelab.or.kr/Pubs/phdthesis_shinnung.pdf`, read). DOI unknown; IEEE Xplore document 10946718, 418 here. | `THESIS_CHAPTER, PARTIAL` — from Shinnung Jeong's thesis "Decoupling Scheduling and Storage Formats for Balanced Graph Processing on a GPU": SparseWeaver is a **hardware/software co-design** adding a lightweight GPU functional unit called **Weaver**; it "converts sparse operations in graph processing into dense operations using Weaver and balances the workloads across GPU threads"; it builds on the **CR2** community-aware, **degree-ordered subgraph** format where "all vertices within a subgraph have a uniform, regularized number of edges … eliminat[ing] the need for offset arrays"; **2.49× execution-time reduction** at **0.045% area overhead**; evaluated on PR/CC/BFS/Delta-SSSP against GraphIt and GSwitch. **Not recovered**: the simulator and its configuration, the area/power model, the instruction table (Table 4.2) contents, the pipeline stage Weaver occupies. | **NO** — the contribution is a **new GPU functional unit** plus instructions, justified by SIMT warp-level workload imbalance; an area-overhead figure (0.045%) is by definition a GPU-microarchitecture claim. | **load imbalance** (the whole premise: irregular edge distribution idling threads within warps) + **compute** (regularised work per thread). Establishment `PARTIAL` — the thesis gives the result but not the microarchitectural detail. | `CORE_GPU` | The **only hardware-side paper** among this cluster's assigned set; everything else is software. Authors: Shinnung Jeong, Liam Paul Cooper, Ju Min Lee, Heelim Choi, Nicholas Parnenzini, Chihyo Ahn, Yongwoo Lee, Hanjun Kim, Hyesoon Kim. **Deep analysis withheld**: thesis evidence is real full text but the microarchitectural core was not recoverable, and thesis evidence must not be silently attributed to the HPCA paper. | — (watchlist; **partial full text exists via the author's thesis**) |
| ROME: Maximizing GPU Efficiency for All-Pairs Shortest Path via Taming Fine-Grained Irregularities | PPoPP 2026 | `CLOSED_ACCESS` — DOI 10.1145/3774934.3786461; no preprint (Qiang Wang's publication page checked, no PDF; Xiaowen Chu's page likewise); no artifact located. **Abstract obtained** from the official PPoPP26 TOC. | `ABSTRACT_ONLY` (official TOC). Authors: Weile Luo, Yuhan Chen, Xiangrui Yu, Qiang Wang, Ruibo Fan, **Hongyuan Liu**, Xiaowen Chu. Abstract: APSP is solved "by reducing the computational workload through vertex reordering"; GPU execution faces "fine-grained granularity, shape, and dependency irregularities, which cause severe hardware underutilization"; ROME "tames these irregularities by **spatially restructuring computation into regularized workloads and temporally overlapping them with an asynchronous pipeline**"; **14.7–244.5× over CPU** and **11.2–338.0× over prior GPU approaches**. | **NO** — three named irregularity classes (granularity, shape, dependency) said to cause "severe hardware underutilization", answered by spatial regularisation plus an asynchronous software pipeline. Both halves are GPU occupancy/latency-hiding mechanisms. | **load imbalance** (granularity/shape irregularity) + **dependency** (dependency irregularity) + **compute** (underutilisation), all **claimed**; establishment `UNKNOWN` — no text read. | `CORE_GPU` | The cleanest statement in this cluster of the *taxonomy* of irregularity (granularity / shape / dependency), and it is the same "regularise then pipeline" recipe that Acc-SpMM and Swift use in different guises. Hongyuan Liu also co-authors the MICRO 2025 BitGen regex work below. **Abstract-only ⇒ no deep analysis.** | — (watchlist) |
| DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs *(promoted from the verdict-only list — full text proved reachable)* | PPoPP 2026 | `PUBLIC_FULLTEXT` — author PDF `ssslab.cn/assets/papers/2026-niu-DiggerBees.pdf` read. DOI 10.1145/3774934.3786457. | `FULL_PAPER` — three stated challenges, the HotRing/ColdSeg two-level stack with capacities, the warp-as-traversal-unit decision, both stealing protocols with thresholds, the synchronisation primitives, A100 + H100 setup with CUDA 12.8, 234 SuiteSparse graphs (151 DIMACS10 / 68 SNAP / 15 LAW), five baselines, MTEPS methodology, the v1–v4 ablation, load-balance and parameter-sensitivity studies, 4 stated limitations, related work. | **NO** — the **warp** is the traversal unit so all 32 lanes follow one path (a direct answer to SIMT divergence); the stack is split across **shared memory (HotRing, 512 B/warp)** and **global memory (ColdSeg)** because the low-latency store is capacity-bounded; the stealing protocol is `atomicCAS` reservations + `__threadfence_block()`/`__threadfence()` + a 32-bit shared warp mask + a **leader warp per block**; flush/refill use Hopper `cp_async_bulk`/TMA. | **load imbalance** (established, strongly: CoV halved — `amazon` 2.48 → 0.72; 3.44× variance reduction; v2→v3 step is 25.94–38.41×) + **memory** (established: v1→v2 = +45%) + **dependency** (addressed *by relaxation* — unordered DFS drops lexicographic order, cost stated) + **synchronisation** (minimised by design; residual cost listed as an open limitation). | `CORE_GPU` | Beats CPU work-stealing DFS by only 1.37×/1.83× but the previous **GPU** DFS by 30.18× — so the contribution is precisely the GPU mapping. Same authors as BerryBees (bit-Tensor-Core BFS, PPoPP 2025, a baseline here): **the same people chose *not* to use the matrix unit for DFS.** | `GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md` |
| Optimizing Datalog for the GPU (**GPUlog**) *(promoted from the verdict-only list — full text proved reachable)* | ASPLOS 2025 | `PUBLIC_FULLTEXT` — author PDF `thomas.gilray.org/pdf/datalog-gpu.pdf` read. DOI 10.1145/3669940.3707274. **Title/name discrepancy recorded**: arXiv 2311.02206 v3 is the same work under the title "Modern Datalog on the GPU" with the system named **GDLog**. | `FULL_PAPER` — HISA's three layers, the semi-naïve Full/Delta/New pipeline, n-way join materialisation, Eager Buffer Management, strided thread mapping (stride = 32 × num SPs), Algorithms 1–3, named Thrust primitives, RMM pooling, H100/A100/MI250/MI50 setup with CUDA 11.8 and cuDF 23.10, dataset edge counts, all baselines, headline numbers, the 42% merge breakdown, seven stated limitations, related work. Cross-read against the arXiv preprint. | **NO** — HISA replaces B-trees/Bries with a dense row-major array + sorted index + open-addressing hash table **because pointer-chasing does not coalesce and lock-based insertion does not scale past 8–16 threads**; insertion is lock-free `AtomicCAS`; the thread map is grid-strided with a stride tied to the stream-processor count; the two-pass join and EBM exist because a GPU kernel cannot grow an allocation mid-flight. The HIP port underperforms **for want of RMM**, which locates the contribution in the GPU memory-management layer. | **memory** (established: coalescing is HISA's stated goal; merge = 42% of runtime; paper concludes "remains memory-bound") + **synchronisation** (established: lock-free insertion replaces a CPU bottleneck measured at 77.8%) + **load imbalance** (established: n-way materialisation removes idle lanes) — **dependency acknowledged, NOT addressed** (semi-naïve iteration stays sequential). | `CORE_GPU` | Shares its central hardware constraint with Ocean — allocating for an output whose size is unknown — and answers it the opposite way (exact two-pass vs probabilistic estimate). Neither cites the other. | `GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md` |

---

## 2. Verdict-only papers

All rows below were resolved from census evidence (confirmed titles, DOIs,
official program pages, artifact URLs) plus, where noted, citation evidence
recovered from the priority papers' own text. **No row in this section may be
used to justify a deep analysis.**

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Bottleneck class (claimed) | Verdict | Rationale (1-2 sentences) |
|---|---|---|---|---|---|---|---|
| NM-SpMM: Accelerating Matrix Multiplication Using N:M Sparsity with GPGPU | IPDPS 2025 | `CLOSED_ACCESS` — official IPDPS 2025 advance program, S23 Matrix Multiplication; no DOI, arXiv or artifact found. | `TITLE_AND_CENSUS_ROW` | **NO (provisional)** — N:M sparsity is the 2:4-family metadata contract. | compute | `CORE_GPU` | Belongs to the **2:4 Sparse-Tensor-Core metadata** side of the `_LEDGER_tensor_cores.md` distinction, alongside Bridging the Gap, the PPoPP'25 N:M graph reordering, Coruscant and Uni-STC — **not** the FlashSparse/Acc-SpMM/SMaT dense-MMA-on-blocks side. |
| HSMU-SpGEMM: Achieving High Shared Memory Utilization for Parallel SpGEMM on Modern GPUs | HPCA 2025 | `CLOSED_ACCESS` + `PUBLIC_ARTIFACT_ONLY` — `ieeexplore` 418; artifact `github.com/wuminqaq/HSMU-SpGEMM`; ADS metadata record exists. | `TITLE_AND_CENSUS_ROW` + **external corroboration from a read paper**: HSMU-SpGEMM is a named baseline in Ocean (`GPU-ICS26-106`), which reports **2.0× over it, geometric mean, 337 square SuiteSparse matrices, A100**. | **NO** — "shared memory utilization" is the per-SM scratchpad occupancy problem that dictates SpGEMM accumulator sizing; Ocean's whole binning design exists for the same reason. | memory + compute | `CORE_GPU` | Full `NO` rather than provisional because an independently read paper (Ocean) confirms the mechanism and the workload. Artifact public, un-inspected. |
| C3ache: Towards Hierarchical Cache-Centric Computing for Sparse Matrix Multiplication on GPGPUs | MICRO 2025 | `CLOSED_ACCESS` — DOI 10.1145/3725843.3756077, `dl.acm.org` 403. Session 6A GPUs-2. | `TITLE_AND_CENSUS_ROW` — authors Xiaojie Li, Mingyu Wang, Baiqing Zhong, Haiqiu Huang, Guangjie Cao, Zhiyi Yu. | **NO (provisional)** — "cache-centric computing" in a MICRO GPU session means near-cache compute units in the GPU memory hierarchy. | memory | `CORE_GPU` | A **microarchitecture** answer to SpMM, where everything else in this cluster is software; the closest neighbour to SparseWeaver. GPGPU is named in the title. |
| Tetris: Accelerating Sparse Convolution by Exploiting Memory Reuse on GPU | PPoPP 2024 | `CLOSED_ACCESS` — DOI 10.1145/3627535.3638471; `dl.acm.org` 403; no arXiv or artifact found. | `TITLE_AND_CENSUS_ROW` — session "ML Workloads". **Name collision flagged by the census**: a different "Tetris: Boosting Distributed DNN Execution with Flexible Schedule Search" exists; this row is the PPoPP'24 sparse-convolution one. | **NO (provisional)** — "memory reuse" for sparse convolution on GPU means shared-memory/register staging of overlapping input windows. | memory | `CORE_GPU` | Same workload as Insum's point-cloud case study (`GPU-ASPLOS26-101`, which beats TorchSparse by 1.14×); a useful comparison point when either becomes readable. |
| LiteForm: Lightweight and Automatic Format Composition for SpMM on GPUs | HPDC 2025 | `CLOSED_ACCESS` — official HPDC 2025 program, session "Numerical Methods"; no DOI, preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Zhen Peng, Polykarpos Thomadakis, Jacques Pienaar, Gokcen Kestor. | **NO (provisional)** — automatic *composition* of sparse formats for a GPU SpMM kernel, i.e. format selection driven by the GPU's access-granularity constraints. | memory + load imbalance | `CORE_GPU` | The closest published neighbour to Insum's GroupCOO/BlockGroupCOO family and to the SC 2026 "Format-Driven" seed below; Jacques Pienaar's involvement suggests an MLIR connection. |
| Sparsified Preconditioned Conjugate Gradient Solver on GPUs | SC 2025 | `CLOSED_ACCESS` — DOI 10.1145/3712285.3759796, pp. 602–616; `dl.acm.org` 403. | `TITLE_AND_CENSUS_ROW` | **PROVISIONAL** — "sparsified preconditioner" is a numerical-algorithm change; "on GPUs" alone does not name a GPU property. | memory (presumed) | `RELATED_GPU` | **Strict counterfactual applies**: a sparsification strategy for a preconditioner is an algorithm that would help on any parallel machine. Would need the text to show a warp/shared-memory/atomics mechanism to reach `CORE_GPU`. Direct neighbour of Mille-feuille (`GPU-SC24-103`), which *does* clear the bar. |
| Extending Sparse Patterns to Improve Inverse Preconditioning on GPU Architectures | HPDC 2024 | `CLOSED_ACCESS` — official HPDC 2024 program, session "Accelerators & Scientific applications"; no DOI, preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Sergi Laut, Ricard Borrell, **Marc Casas**. | **PROVISIONAL** — "extending sparse patterns" of an approximate-inverse preconditioner is a numerical choice; the GPU appears as the target, not the mechanism. | memory (presumed) | `RELATED_GPU` | Same strict-counterfactual reasoning as the row above. Marc Casas links this to DiggerBees (`GPU-PPoPP26-105`) and Swift. |
| StructILU: Dependency-Preserving Incomplete LU with Hierarchical Parallelism for Structured Grid PDEs on GPUs | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, session "Sparse Linear Algebra"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — Hao Luo et al. | **NO (provisional)** — "hierarchical parallelism" while "dependency-preserving" names the thread/warp/block level-scheduling of a triangular-solve dependency graph, which is a GPU-hierarchy mechanism. | dependency + synchronisation | `CORE_GPU` | ILU/SpTRSV dependency scheduling on GPUs is the same bottleneck class Mille-feuille's SpTRSV preconditioner and Caracal address. |
| CB-SpMV: A Data Aggregating and Balance Algorithm for Cache-Friendly Block-Based SpMV on GPUs | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, session "Sparse Linear Algebra"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — Xing Cong et al. | **NO (provisional)** — "cache-friendly block-based" plus "balance" names both the GPU cache-line/transaction granularity and warp-level load balancing. | memory + load imbalance | `CORE_GPU` | Straightforward member of the format+balance line (RoDe, Acc-SpMM, Swift). |
| HR-SpMM: Adaptive Row Partitioning and Hybrid Kernel Design for Sparse Matrix Multiplication | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, session "Sparse Linear Algebra"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — Qi Wang et al. **The census flags this `[TITLE-ONLY]`: the title does not say GPU**; GPU targeting is inferred only from session company (three explicit GPU papers alongside). | **PROVISIONAL** — "adaptive row partitioning" is the same idea as RoDe's row decomposition and would be a load-balancing mechanism *if* the target is a GPU, which is unverified. | load imbalance (presumed) | `UNRESOLVED` | **Verdict deliberately withheld.** The census's own caution is right: session-company evidence is not evidence about the paper. Cheap to resolve if the ICS 2025 proceedings become reachable. |
| CoLa: Towards Communication-efficient Distributed Sparse Matrix-Matrix Multiplication on GPUs | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, session "Graph Neural Networks"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — Lixing Zhang et al. | **PROVISIONAL** — distributed SpGEMM communication scheduling is largely a network/partitioning problem; "on GPUs" may only name the endpoints. | (inter-GPU) communication — outside the five classes | `RELATED_GPU` | Strict counterfactual: a communication-avoiding distributed SpGEMM algorithm is substantially the same on any distributed accelerator. Would upgrade if the text shows NVLink-topology-specific or device-initiated-communication mechanisms. |
| Communication-Avoiding SpGEMM via Trident Partitioning on Hierarchical GPU Interconnect | ICS 2026 | `CLOSED_ACCESS` — ICS 2026 program, S20 Sparse & Tensor Kernels; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — J. Bellavita et al. | **NO (provisional)** — the title names the **hierarchical GPU interconnect** (intra-node NVLink/NVSwitch vs inter-node) as the structure the partitioning is designed against; that is a GPU-system topology property, not a generic network. | (inter-GPU) communication + load imbalance | `CORE_GPU` | Stronger than CoLa because the *interconnect hierarchy* is named as the design target. Julian Bellavita also authors Popcorn (PPoPP 2025, below). |
| Loop-Carried Dependence Transformation for Parallel Sparse Solvers on GPUs | SC 2026 (seed) | **`NOT_FOUND`** | **NOT_FOUND_AFTER_SEARCH** — the census located no paper with this exact title; the nearest real work is SC'23 *Runtime Composition of Iterations for Fusing Loop-carried Sparse Dependence* by the same research line. Not re-searched here (quota); the census's negative result stands. | n/a | n/a | `UNRESOLVED` | **Existence unverified.** The SC 2026 population is not fully enumerated, so absence is weak evidence, but no source supports this title. Treat as a possibly-mistaken seed. |
| Format-Driven Automatic Pipeline Construction and Load Balancing for SpMM on GPUs | SC 2026 | `CLOSED_ACCESS` — official SC26 Best/Best-Student-Paper finalist announcement page; no DOI, preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — **`CONFIRMED_IN_POPULATION`** (official finalist); first author Kelun Lei (Beihang University), with Hailong Yang, **Kaige Zhang**, Zhongzhi Luan; 10 authors. | **NO (provisional)** — "pipeline construction" plus "load balancing" driven by the sparse *format* is the Acc-SpMM recipe (mapping + software pipeline) generalised and automated. | load imbalance + memory | `CORE_GPU` | **Kaige Zhang is also first author of "Exploiting Efficient Mapping and Pipelined Execution for Accelerating SpMV on Tensor Cores" (PPoPP 2026)** in the sibling ledger — the same group, the same mapping+pipeline recipe, one venue later, now automated and format-driven. A high-value watchlist item for the format-vs-balance question. |
| VDHA: Vector-Driven Hash Aggregation for Sparse Matrix-Sparse Vector Multiplication on GPUs | PPoPP 2026 | `CLOSED_ACCESS` — DOI 10.1145/3774934.3786447; no preprint or artifact found. **Abstract obtained** from the official PPoPP26 TOC. | `ABSTRACT_ONLY` (official TOC) — Yuchen Li, Zhe Pan, Peng Qu, Youhui Zhang. Abstract: SpMSpV "is often bottlenecked by the **write-back phase** of accumulating non-zero multiply–accumulate results"; VDHA uses "**block-private hash tables** for local aggregation, substantially reducing **write conflicts** and improving **memory coalescing**"; **1.41× geomean on web graphs, 1.13× on scientific workloads**. | **NO** — block-private hash tables to reduce write conflicts and improve coalescing are shared-memory-and-atomics mechanisms; the named bottleneck (atomic write-back) is a GPU contention problem. Full `NO`: the abstract names the properties. | **synchronisation** (write conflicts) + **memory** (coalescing), both claimed; establishment `UNKNOWN`. | `CORE_GPU` | The **same mechanism as Ocean's hash accumulator** (`GPU-ICS26-106`) applied to SpMSpV instead of SpGEMM — privatise the hash table to convert global atomic contention into local aggregation. Modest speedups honestly reported. |
| DiggerBees | PPoPP 2026 | — | — | — | — | — | **Promoted to the priority table** (full text proved reachable). See §1. |
| Root-Down Exposure for Maximal Clique Enumeration on GPUs (**RDMCE**) | PPoPP 2026 | `CLOSED_ACCESS` — DOI 10.1145/3774934.3786449; no preprint or artifact found. **Abstract obtained** from the official PPoPP26 TOC. | `ABSTRACT_ONLY` (official TOC) — Zhe Pan, Peng Qu, Youhui Zhang. Abstract: existing GPU MCE solutions "suffer from inefficient load-balancing mechanisms" that "introduce significant **synchronization overhead** and increase **memory usage**"; RDMCE uses "a root-down exposure mechanism where busy workers dynamically **expose their current root**"; **1.25–5.38× over prior GPU solutions**. | **NO** — dynamic exposure of a worker's search root so idle workers can take subtrees is a **work-stealing/donation protocol**, the same class as DiggerBees' hierarchical stealing, and the named costs (synchronisation overhead, memory usage) are GPU ones. | **load imbalance** (primary) + **synchronisation** + **memory**, all claimed; establishment `UNKNOWN`. | `CORE_GPU` | Same research group as VDHA (Pan/Qu/Zhang, Tsinghua) and the same bottleneck class as DiggerBees (`GPU-PPoPP26-105`) — **three independent PPoPP 2026 papers all attacking GPU load imbalance in irregular graph search by dynamic work redistribution.** That convergence is itself a finding. |
| GLUMIN: Fast Connectivity Check Based on LUTs For Efficient Graph Pattern Mining | PPoPP 2025 | `CLOSED_ACCESS` — official page `ppopp25.sigplan.org/.../40/x`; DOI unknown; no preprint or artifact found; the PPoPP25 TOC-with-abstracts service returns a server error here. | `TITLE_AND_CENSUS_ROW` — Weichen Cao, Ke Meng, Zhiheng Lin, Guangming Tan. Census notes: **the title has no GPU term but the abstract names GPU**, and it is scheduled in session "S10 GPU II". | **PROVISIONAL** — a lookup-table connectivity check could be a pure algorithmic trick; whether the LUT lives in shared memory / registers and is sized to a warp is exactly what would decide this, and is unknown. | compute (presumed) | `UNRESOLVED` | **Verdict withheld rather than guessed.** Zhiheng Lin also co-authors "Exploiting Fine-Grained Redundancy in Set-Centric Graph Pattern Mining" (PPoPP 2024, below) — the same group, the same workload, one year apart. |
| Popcorn: Accelerating Kernel K-means on GPUs through Sparse Linear Algebra | PPoPP 2025 | `CLOSED_ACCESS` — official page `ppopp25.sigplan.org/.../38/x`; DOI unknown; no preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Julian Bellavita et al. | **PROVISIONAL** — "through sparse linear algebra" describes an algorithmic reformulation of k-means; the GPU may be only the execution target. | compute (presumed) | `RELATED_GPU` | Strict counterfactual: recasting kernel k-means as sparse linear algebra is substantially the same on any machine with a good SpMM. Would upgrade if the text shows a kernel-level mechanism. Same author as the ICS 2026 Trident SpGEMM row. |
| Swift Unfolding of Communities: GPU-Accelerated Louvain Algorithm | PPoPP 2025 | `CLOSED_ACCESS` — official page `ppopp25.sigplan.org/.../35/x`; DOI unknown; no preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Zhibin Wang et al., session "S10 GPU II". | **PROVISIONAL** — "GPU-Accelerated Louvain" is, on the title alone, a port. Louvain's GPU difficulty (irregular neighbourhood aggregation, community-label contention) is real, but the title names no mechanism. | load imbalance (presumed) | `RELATED_GPU` | Strict counterfactual applied honestly: "GPU-Accelerated X" in a title is the archetype of a claim that needs the text. **Note this is a different "Swift" from the HPCA 2026 SpMM paper in §1** — a genuine title collision within this cluster. |
| Exploiting Fine-Grained Redundancy in Set-Centric Graph Pattern Mining | PPoPP 2024 | `CLOSED_ACCESS` — DOI 10.1145/3627535.3638507; `dl.acm.org` 403; no preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Zhiheng Lin et al. Census notes: **title has no GPU term; the abstract names GPU.** | **PROVISIONAL** — "fine-grained redundancy" in set intersections is an algorithmic observation; its GPU relevance depends on whether the redundancy is eliminated at warp granularity. | compute (presumed) | `UNRESOLVED` | Withheld for the same reason as GLUMIN, with which it shares an author and a workload. Resolving either would likely resolve both. |
| INFINEL: An efficient GPU-based processing method for unpredictable large output graph queries | PPoPP 2024 | `CLOSED_ACCESS` — DOI 10.1145/3627535.3638490; `dl.acm.org` 403; no preprint or artifact found. | `TITLE_AND_CENSUS_ROW` — Sungwoo Park et al. | **NO** — "unpredictable large output" on a GPU is *the* device-side dynamic-allocation problem: a kernel cannot grow its output buffer, so the size must be estimated, over-allocated, or produced in chunks. The title names the GPU-specific difficulty directly. | memory + synchronisation | `CORE_GPU` | **Full `NO`, not provisional.** This is the third independent attack in this cluster on the same constraint: INFINEL (PPoPP'24, graph queries), GPUlog's two-pass join + EBM (`GPU-ASPLOS25-107`), and Ocean's HyperLogLog estimate (`GPU-ICS26-106`). None of the three cites the others. **High-value watchlist item.** |
| Gallatin: A General-Purpose GPU Memory Manager | PPoPP 2024 | `CLOSED_ACCESS` — DOI 10.1145/3627535.3638499; `dl.acm.org` 403; no preprint located (an artifact may exist; not found). | `TITLE_AND_CENSUS_ROW` — Hunter James McCoy, Prashant Pandey. | **NO** — a device-side dynamic memory allocator *is* a GPU mechanism end to end: massively parallel `malloc`/`free` from thousands of concurrent threads, which on a CPU is a solved and uninteresting problem. | memory + synchronisation | `CORE_GPU` | The **general-purpose substrate** for the unpredictable-output-size problem that INFINEL, GPUlog and Ocean each solve ad hoc. If any of them cited Gallatin the line would be a coherent one; GPUlog uses **RMM** instead and Ocean uses fixed binning, so apparently not. |
| Efficient Weighted Graph Matching on GPUs | SC 2024 | `CLOSED_ACCESS` — DOI 10.1109/SC41406.2024.00024; `ieeexplore` 418; no preprint or artifact located. | `TITLE_AND_CENSUS_ROW` — Michael Mandulak et al. | **PROVISIONAL** — half-approximate weighted matching has a known irregular-parallel structure, but the title names no GPU mechanism. | load imbalance (presumed) | `RELATED_GPU` | Strict counterfactual. Would upgrade on evidence of warp-level conflict resolution or atomics-based pointer-jumping. |
| Distributed-Memory Parallel Algorithms for Sparse Matrix and Sparse Tall-and-Skinny Matrix Multiplication | SC 2024 | `CLOSED_ACCESS` — DOI 10.1109/SC41406.2024.00052; `ieeexplore` 418; no preprint located. | `TITLE_AND_CENSUS_ROW` — Isuru Ranawaka et al. Census flags the **GPU backend as unverified** `[title-inference]`. | **PROVISIONAL** — distributed SpGEMM/SpMM communication algorithms; the title does not mention GPUs at all. | (inter-node) communication | `RELATED_GPU` | Strict counterfactual, and GPU involvement is itself unverified. Recorded rather than excluded because the SpMM-tall-skinny shape is central to this cluster's workloads. |
| Arrow Matrix Decomposition: A Novel Approach for Communication-Efficient Sparse Matrix Multiplication | PPoPP 2024 | `PUBLIC_FULLTEXT` — arXiv 2402.19364 (**not fetched in this pass; capacity**). DOI 10.1145/3627535.3638496. | `TITLE_AND_CENSUS_ROW` — Lukas Gianinazzi et al. (Hoefler's group, same lab as SMaT `GPU-SC24-102`). Census notes: **title has no GPU term; the abstract names GPU as the execution target.** | **PROVISIONAL** — a matrix *decomposition* that reduces communication volume is a partitioning result; the GPU is where it runs. | (inter-GPU) communication | `RELATED_GPU` | Strict counterfactual applied on current evidence. **Cheapest upgrade path in this whole ledger** — the arXiv full text is public and reachable; a single fetch would settle it. |
| StraGCN: GPU-Accelerated Strassen's Sparse-Dense Matrix Multiplication for GCN Training | SC 2025 | `CLOSED_ACCESS` — DOI 10.1145/3712285.3759826; `dl.acm.org` 403. | `TITLE_AND_CENSUS_ROW` | **PROVISIONAL** — Strassen's algorithm applied to sparse-dense products is an arithmetic-complexity result; "GPU-Accelerated" in the title names no mechanism. | compute (presumed) | `RELATED_GPU` | Strict counterfactual. Strassen on a GPU does raise real register-pressure and numerical-stability questions, but none is evidenced from the title. |
| cuMIS: A Unified Scalable Framework for Computing Maximal Independent Sets on Trillion-Edge Graphs | ICS 2026 | `CLOSED_ACCESS` — ICS 2026 program, S13; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — J. Nke et al. Census flags `[TITLE-ONLY]`: **GPU identity is inferred from the `cu` prefix only — UNVERIFIED.** | **PROVISIONAL** | load imbalance (presumed) | `UNRESOLVED` | **Verdict withheld.** The `cu` naming convention is suggestive, not evidence. Trillion-edge scale implies multi-GPU or multi-node, which the title also does not state. |
| CORE-BFS: Communication-Optimized REctangular-partitioned BFS Achieving 160.845 TeraTEPS on Frontier | ICS 2026 | `CLOSED_ACCESS` — ICS 2026 program, S13; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — H. Yang et al. Census flags `[TITLE-ONLY]`: **Frontier is AMD-GPU-accelerated so a TeraTEPS record there implies GPU execution, but the title does not say GPU — UNVERIFIED.** | **PROVISIONAL** — rectangular partitioning of a BFS adjacency for communication is a distributed-algorithm result. | (inter-node) communication | `RELATED_GPU` | Strict counterfactual: a communication-optimised partitioning would be substantially the same on a CPU cluster. The Frontier record is a systems achievement, not a GPU-mechanism claim, on current evidence. |
| A Multi-GPU Algorithm for Computing Maximal Independent Sets in Large Graphs | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, "Graph Algorithms"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — Anju Mongandampulath Akathoott et al. | **PROVISIONAL** — "Multi-GPU algorithm for MIS" names the platform, not a mechanism. | (inter-GPU) communication + load imbalance (presumed) | `RELATED_GPU` | Strict counterfactual. MIS on GPUs does have a genuine warp-level conflict-resolution problem, but nothing in the title evidences it. |
| A Bidirectional GPU Algorithm for Computing Maximum Matchings in Bipartite Graphs | IPDPS 2025 | `CLOSED_ACCESS` — official IPDPS 2025 advance program, S8 Graph Algorithms II; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` | **PROVISIONAL** — bidirectional search is an algorithmic technique; "GPU Algorithm" names the target. | load imbalance (presumed) | `RELATED_GPU` | Strict counterfactual. Note the census separately flags a *different* IPDPS'25 paper — "Enumeration of Billions of Maximal Bicliques … **without** Using GPUs" — where the GPU keyword marks the displaced baseline, not a mechanism; that paper is correctly outside this cluster. |
| Interleaved Bitstream Execution for Multi-Pattern Regex Matching on GPUs | MICRO 2025 | `CLOSED_ACCESS` + `PUBLIC_ARTIFACT_ONLY` — DOI 10.1145/3725843.3756052, `dl.acm.org` 403; artifact `github.com/getianao/BitGen` and `zenodo.org/records/16664499`. | `TITLE_AND_CENSUS_ROW` — Tianao Ge, Xiaowen Chu, **Hongyuan Liu** (session 2D GPU-1). Census describes it as "GPU kernel/warp-level bit-parallel regex execution". | **NO (provisional)** — "interleaved bitstream execution" is a **warp-level bit-parallel** scheme: multiple patterns packed into machine words so one SIMT lane advances several automata at once, which is a register-width and divergence argument. | compute + load imbalance | `CORE_GPU` | Same authors' group as ROME (Chu, Liu). The bit-packing mechanism is the *non-matrix-unit* cousin of BerryBees' bit-MMA BFS in the sibling ledger. Artifact public and un-inspected. |
| cuJSON: A Highly Parallel JSON Parser for GPUs | ASPLOS 2026 | `CLOSED_ACCESS` + `PUBLIC_ARTIFACT_ONLY` — DOI 10.1145/3760250.3762222, volume 31V1; `dl.acm.org` 403; artifact `github.com/AutomataLab/cuJSON`. | `TITLE_AND_CENSUS_ROW` — AutomataLab, session "8A: GPU Programming". Census describes the mechanism as "warp-level tokenisation and structural-index construction". | **NO (provisional)** — structural-index construction by warp-level bit operations and prefix scans is the GPU-parallel-parsing mechanism class (simdjson's `pclmulqdq`/`popcnt` tricks recast for SIMT). | compute + memory | `CORE_GPU` | Irregular data-dependent parsing made data-parallel on a GPU — the same category as the regex row above. Artifact public and un-inspected. |
| Multi-node Multi-GPU Datalog | ICS 2025 | `CLOSED_ACCESS` — ICS 2025 program, session "Heterogeneity"; no DOI or artifact found. | `TITLE_AND_CENSUS_ROW` — **Ahmedur Rahman Shovon** et al. + **corroborating evidence from a read paper**: GPUlog (`GPU-ASPLOS25-107`) states multi-GPU/multi-node as its explicit future work, and Shovon is a GPUlog co-author. | **PROVISIONAL** — scaling GPUlog out is primarily an all-to-all communication and partitioning problem; the intra-GPU mechanisms are inherited from GPUlog. | (inter-node) communication | `RELATED_GPU` | Direct successor to `GPU-ASPLOS25-107`, confirmed by author overlap and by that paper's own stated future work. `RELATED_GPU` on the strict test because the *new* content is distribution, not a GPU mechanism — would upgrade if HISA itself is redesigned for multi-GPU. |
| Optimizing Datalog for the GPU | ASPLOS 2025 | — | — | — | — | — | **Promoted to the priority table** (author PDF proved reachable). See §1. |

---

## 3. Access-state summary

Total distinct papers adjudicated: **45** (12 in §1, 33 in §2).

| Access state | Count | Papers |
|---|---|---|
| `PUBLIC_FULLTEXT` (read) | 7 | Insum, SMaT, Mille-feuille, Trojan Horse, Ocean (+ artifact cloned and read), DiggerBees, GPUlog |
| `PUBLIC_FULLTEXT` (available, **not read — capacity**) | 1 | Arrow Matrix Decomposition (arXiv 2402.19364) |
| `PUBLIC_FULLTEXT` via **author PhD-thesis chapter**, partial | 1 | SparseWeaver |
| `ABSTRACT_ONLY` (official conference page / TOC) | 4 | Swift (HPCA 2026), ROME, VDHA, Root-Down Exposure |
| `CLOSED_ACCESS` **+ `PUBLIC_ARTIFACT`** | 4 | RoDe, HSMU-SpGEMM, Interleaved Bitstream (BitGen), cuJSON |
| `CLOSED_ACCESS` | 27 | Caracal, NM-SpMM, C3ache, Tetris, LiteForm, Sparsified PCG, Inverse Preconditioning, StructILU, CB-SpMV, HR-SpMM, CoLa, Trident SpGEMM, Format-Driven, GLUMIN, Popcorn, Swift Unfolding of Communities, Fine-Grained Redundancy, INFINEL, Gallatin, Weighted Graph Matching, Sparse Tall-and-Skinny, StraGCN, cuMIS, CORE-BFS, Multi-GPU MIS, Bipartite Matching, Multi-node Multi-GPU Datalog |
| `NOT_FOUND` (existence unverified) | 1 | Loop-Carried Dependence Transformation for Parallel Sparse Solvers on GPUs (SC 2026 seed) |

**Access reality of this cluster**: only **7 of 45** (16%) were readable in full.
By contrast the Tensor-Core sibling cluster read 9 of 42. The difference is not
venue mix but **author-PDF culture**: every one of the four author-PDF successes
here came from two labs that post their own papers (SSSLab/CUPB —
Mille-feuille, Trojan Horse, DiggerBees; and Thomas Gilray — GPUlog). ACM and
IEEE paywalls account for essentially all of the 27 `CLOSED_ACCESS` rows.

## 4. Verdict summary

| Verdict | Count |
|---|---|
| `CORE_GPU` | 27 |
| `RELATED_GPU` | 13 (Sparsified PCG, Inverse Preconditioning, CoLa, Popcorn, Swift Unfolding of Communities, Weighted Graph Matching, Sparse Tall-and-Skinny, Arrow Matrix, StraGCN, CORE-BFS, Multi-GPU MIS, Bipartite Matching, Multi-node Multi-GPU Datalog) |
| `UNRESOLVED` | 5 (HR-SpMM, GLUMIN, Fine-Grained Redundancy, cuMIS, Loop-Carried seed) |
| `EXCLUDE` | 0 |
| **total** | **45** |

**No paper was excluded**, but this cluster's verdicts are far less uniform than
the Tensor-Core cluster's, which returned 30 `CORE_GPU` / 5 `RELATED_GPU` / 7
`UNRESOLVED` and observed that naming a Tensor Core in a title reliably
indicates a GPU mechanism. **Naming "on GPUs" does not.** The 13 `RELATED_GPU`
calls are papers whose contribution is an **algorithm** — a preconditioner
sparsification, a communication-avoiding partitioning, a Strassen recursion, a
bidirectional search, a Louvain port — that happens to run on a GPU. That is
exactly what the strict counterfactual exists to catch, and it is a structural
feature of this cluster rather than an accident of sampling: sparse linear
algebra and graph analytics have large algorithm-first literatures that
Tensor-Core work does not.

Five verdicts are **withheld** rather than guessed, in every case because the
census itself flagged the GPU target as unverified (`HR-SpMM`, `cuMIS`), because
the title names no mechanism and the abstract was unreachable (`GLUMIN`,
`Fine-Grained Redundancy`), or because the paper's existence is unconfirmed
(`Loop-Carried`).

## 5. Corrections to `_LEDGER_tensor_cores.md`

Two rows in the sibling ledger are corrected here **from read full text**:

1. **High Performance Unstructured SpMM Computation Using Tensor Cores (SMaT)** —
   that ledger has it `PUBLIC_FULLTEXT`, "not fetched (capacity)", `CORE_GPU`,
   watchlist. The full text is now read; the verdict is **unchanged**
   (`CORE_GPU`) and the deep analysis is `GPU-SC24-102`. It is confirmed
   explicitly from the text to use **dense MMA on BCSR blocks (`m16n8k16`),
   not 2:4 Sparse-Tensor-Core metadata**, so it belongs on the
   FlashSparse/Acc-SpMM side of that ledger's distinction and is in fact the
   **earliest member of that line**.
2. **Mille-feuille** — that ledger has it `CLOSED_ACCESS (effectively)` and
   `RELATED_GPU`, with cluster-F membership `UNRESOLVED`. **Both the access
   state and the verdict are corrected**: the author PDF is reachable at
   `ssslab.cn`, and on the full text the verdict is **`CORE_GPU`** in cluster G.
   That ledger's *reasoning* was right and is confirmed — **no Tensor Core or
   matrix unit appears anywhere in the paper**; the mechanisms are persistent
   single-kernel execution with a hand-built software grid barrier and
   shared-memory-resident tiles. It is a cluster-G paper, not a cluster-F one.

A third, weaker note: that ledger's `AmgT` row is corroborated — the SSSLab
publication listing gives a reachable author PDF
(`ssslab.cn/assets/papers/2024-lu-AmgT-final.pdf`), so `AmgT` should be
`PUBLIC_FULLTEXT`, not `PUBLIC_ARTIFACT_ONLY`. Not fetched here (out of cluster).

## 6. Stable IDs assigned by this cluster

`GPU-ASPLOS26-101`, `GPU-SC24-102`, `GPU-SC24-103`, `GPU-PPoPP26-104`,
`GPU-PPoPP26-105`, `GPU-ICS26-106`, `GPU-ASPLOS25-107`.

All are drawn from the mandated 101–119 band. `GPU-ICS26-106` is distinct from
the two existing `GPU-ISC26-02` files (ISC, not ICS) — no collision.
IDs 108–119 in this band remain unassigned by this cluster.

---

## 7. Cross-paper findings and verified lineage

All lineage below is taken from the **papers' own citations, baselines and
author overlaps**, read in the full texts; nothing is inferred from the census.

### 7.1 SpMM and SpGEMM have mechanically diverged

- **SpMM (sparse × dense)** has become a **matrix-unit-and-format** problem. The
  line is now traceable end to end from read text: **SMaT (SC 2024)** fixes the
  block at the `m16n8k16` operand shape and attacks *tile count* by Jaccard row
  clustering → **FlashSparse (PPoPP 2025)** attacks *tile shape* by swapping
  operands to exploit `n = 8` → **Acc-SpMM (PPoPP 2025)** attacks the *schedule*
  → **Insum (ASPLOS 2026)** attacks the *source language*, reaching the same
  MMA through `tl.dot`. All four run **dense MMA on dense blocks**.
- **SpGEMM (sparse × sparse)** has not moved that way at all. **Ocean (ICS 2026)
  does not contain the string "Tensor Core", "MMA" or "tensor core" anywhere in
  its text or references** [verified by targeted full-text query]. Its related
  work names only cuSPARSE, spECK, OpSparse, TileSpGEMM, HSMU-SpGEMM, MOSparse,
  AC-SpGEMM and Bellavita's Trident partitioning. SpGEMM remains an
  **atomics-allocation-and-scheduling** problem because the output pattern is
  unknown, and no matrix unit helps with an unknown output pattern.

**So the answer to "is the sparse-GPU line converging on format design, on load
balancing, or on matrix-unit exploitation?" is: it has split.** SpMM converged
on matrix-unit exploitation *via* format design (the format exists to feed the
instruction). SpGEMM, sparse solvers and graph workloads converged on **load
balancing and synchronisation**, with no matrix unit in sight.

### 7.2 The unpredictable-output-size problem is being solved three times in parallel, with no cross-citation

Three papers in this cluster attack the identical GPU constraint — **a kernel
cannot grow an allocation mid-flight, and shared memory is sized at launch**:

| Paper | Answer | Cost it pays |
|---|---|---|
| **INFINEL** (PPoPP 2024, unread) | chunked/over-allocated output for graph queries | unknown |
| **GPUlog** (ASPLOS 2025, read) | exact **two-pass join** (count, allocate, recompute) + Eager Buffer Management | doubled outer-relation reads; the paper lists it as limitation 5 |
| **Ocean** (ICS 2026, read + code) | **probabilistic estimate** (HyperLogLog, `atomicMax` updates) + overflow fallback kernel | 0.3–1.2% overflow rows; **2.2× peak memory**; one matrix (`JP`) fails |

**Gallatin (PPoPP 2024)** is the general-purpose device-side allocator that would
subsume all three, and **none of them uses it** — GPUlog uses RAPIDS **RMM**,
Ocean uses fixed geometric binning. Neither read paper cites Gallatin or INFINEL.
This is the clearest un-exploited connection this cluster found.

### 7.3 Load imbalance is the cluster's dominant bottleneck class, and PPoPP 2026 converged on work redistribution

Of the five bottleneck classes, **load imbalance** is claimed by the most papers
and is where the measured ablations are strongest. Three *independent* PPoPP 2026
papers attack it by **dynamic work redistribution** in irregular graph search:

- **DiggerBees** (Niu, Lu, Liu, Casas) — hierarchical *work stealing*, intra-block
  through shared memory and inter-block through a leader warp; the inter-block
  tier alone is worth **25.94×–38.41×** in the ablation.
- **Root-Down Exposure / RDMCE** (Pan, Qu, Zhang) — busy workers *expose their
  root* so idle workers can take subtrees; **1.25–5.38×** over prior GPU MCE.
- **Trojan Horse** (Li … Liu) — host-side *priority aggregation* instead of
  device-side stealing; kernel count to **1.10%/1.48%** of baseline.

Two of the three are from the same lab (SSSLab/CUPB); RDMCE is from a different
group (Tsinghua) and shares authors with **VDHA**, which attacks the same class
in SpMSpV via block-private hash tables. **SMaT's honest failure on `dc2`**
(2.5 GFLOP/s vs DASP's 69.1) is the counter-example that shows why: a *static*
schedule, however well the matrix is reordered first, still loses ~28× on a
power-law block distribution.

### 7.4 Ray-tracing-unit work for sparse kernels is NOT cited by this community — verified

The corpus contains a substantial RT-unit line (`GPU-PPoPP25-128` LibRTS,
`GPU-MICRO24-121` HSU, `GPU-MICRO24-122` TTA, `GPU-ICS24-125` Arkade,
`GPU-ISCA25-127` CoopRT, `GPU-ASPLOS25-124` Treelet). Two of the full texts read
here were queried directly against their entire text and references:

- **SMaT (SC 2024)** — "ray tracing": **no**; "RT core": **no**; "RT unit":
  **no**; "BVH": **no**; "RTSpMSpM": **no**; "LibRTS": **no**. Its related work
  discusses **only Tensor Cores** among specialised units (applications in scan,
  reduction, stencil, FFT), plus TPUs in passing.
- **Ocean (ICS 2026)** — all six terms: **no**.

**Conclusion: the sparse-GPU kernel community and the RT-unit-repurposing
community do not cite each other.** The one bridge that exists in this corpus is
*within* the other direction — the tensor-cores ledger records BerryBees using
bit-MMA for BFS — and even there, the **same authors (Niu, Casas) wrote
DiggerBees one year later using no matrix unit at all** for DFS. That is the
strongest available evidence that fixed-function-unit repurposing is not
regarded by this community as a general answer to irregularity.

### 7.5 Lineage and lab structure verified from the papers themselves

- **SSSLab / China University of Petroleum-Beijing (Weifeng Liu, Zhou Jin)** is
  the most productive single group in this cluster: **DASP (SC 2023)** →
  **PanguLU (SC 2023)** → **AmgT + Mille-feuille (SC 2024)** → **Cubie +
  DiggerBees + Trojan Horse (PPoPP 2026)**. Verified by author lists on the read
  PDFs. Note the internal tension: **DASP is a baseline that beats SMaT by ~28×
  on `dc2`**, and **PanguLU is simultaneously a baseline and an integration
  target for Trojan Horse**.
- **Marc Casas (BSC)** appears on DiggerBees, BerryBees, **Swift (HPCA 2026)**
  and **Extending Sparse Patterns (HPDC 2024)** — i.e. on both the matrix-unit
  and the no-matrix-unit sides, and on both the kernel and the numerical-method
  sides.
- **Xiaowen Chu / Hongyuan Liu** appear on **ROME (PPoPP 2026)** and
  **Interleaved Bitstream Execution (MICRO 2025)** — irregularity taming in two
  very different workloads.
- **Kaige Zhang** appears on the SC 2026 **Format-Driven** finalist and on the
  PPoPP 2026 **SpMV on Tensor Cores** paper in the sibling ledger — the same
  mapping-plus-pipeline recipe, automated one venue later.
- **Yihao Sun / Ahmedur Rahman Shovon** — **GPUlog (ASPLOS 2025)** →
  **Multi-node Multi-GPU Datalog (ICS 2025)**, confirmed by GPUlog's own stated
  future work.
- **Ocean cites Bellavita's Trident partitioning**, which is the ICS 2026 row in
  §2 — an explicit intra-cluster link recovered from a read paper.

### 7.6 What the strict counterfactual actually separated

The cleanest discriminator across all 45 papers was not the workload but
**whether the paper's headline metric has a CPU meaning**:

- Trojan Horse's **kernel count → 1.10%** — no CPU meaning. `CORE_GPU`.
- Mille-feuille's **>30% inter-kernel synchronisation share** — no CPU meaning.
  `CORE_GPU`.
- DiggerBees' **30.18× over the previous GPU DFS while only 1.37× over CPU
  work-stealing DFS** — the gap *is* the GPU mapping. `CORE_GPU`.
- Ocean's **`atomicMax` vs CAS-loop** and **FP64 shared-atomic emulation** — no
  CPU meaning. `CORE_GPU`.
- By contrast, "a sparsified preconditioner converges in fewer iterations" or "a
  decomposition reduces communication volume" are machine-independent claims.
  `RELATED_GPU`.

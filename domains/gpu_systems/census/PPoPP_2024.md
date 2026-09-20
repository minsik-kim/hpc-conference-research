# PPoPP 2024 — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **32** |
| counted items excluded from population | **posters: 12** (separate Sun 3 Mar poster session); **workshops: 5** co-located events not counted (▽PP, GPGPU, PMAM, ExHET, Kotlin-Coroutines tutorial); artifact-evaluation track (separate track, no papers counted); keynotes |
| population source (primary) | https://conf.researchr.org/track/PPoPP-2024/PPoPP-2024-papers — `official-program` (32 entries) |
| population source (corroborating) | (a) per-item researchr detail pages `https://ppopp24.sigplan.org/details/PPoPP-2024-papers/<N>/x` for N=1..45: N=1..32 render as **Talk**, N=33..44 render as **Poster**, N=45 does not exist — `official-program`; (b) https://conf.researchr.org/program/PPoPP-2024/program-PPoPP-2024/ — 9 main-conference sessions + a 12-poster session — `official-program`; (c) https://csconfstats.xoveexu.com/conferences/ppopp/ — "151 submissions / 32 accepted / 21.2%" — third-party statistics aggregator |
| source class | `official-program` (primary + corroborating a,b); `search-engine` (c) |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | The 2024 `-papers` track page lists ONLY the 32 regular papers; posters are on a separate program slot and occupy researchr event IDs 33–44. Unlike PPoPP 2025, the 2024 track page does **not** mix posters into the accepted-papers list. Detail pages for the 2024 regular papers expose per-paper ACM DOIs (`10.1145/3627535.<n>`); poster pages do not. |

### 1.1 Population evidence notes

- Source statement: the official accepted-papers track page enumerates exactly 32 titles.
- Source statement: enumerating researchr event IDs 1..45 on the official site yields 32 items typed "Talk" (IDs 1–32) and 12 typed "Poster" (IDs 33–44); ID 45 returns no record. The 32 talk titles are a set-equal match to the 32 titles on the track page (verified title-by-title).
- Source statement (third-party): the csconfstats aggregator reports 32 accepted of 151 submitted (21.2%) for 2024.
- Inference: because two independent official enumerations agree at 32 and the poster class is separately typed, the population is EXACT.
- **No official acceptance-rate statement of the form "X of Y submissions" was located on any PPoPP 2024 official page.** The 32/151 figure is from a third-party aggregator only.
- `dl.acm.org` returns 403 and `dblp.org` is robots-disallowed, so no publisher/bibliographic cross-check was possible.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 32 regular
papers, each abstract read via its official detail page), not over the seed
list. Keyword hits were used only to order review, never to decide relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | AGAThA: Fast and Efficient GPU Acceleration of Guided Sequence Alignment for Long Read Mapping | Seongyeon Park et al. | UNKNOWN (session heading not captured by program fetch) | 10.1145/3627535.3638474 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/8/x | https://arxiv.org/abs/2403.06478 | NOT_FOUND_AFTER_SEARCH | "GPU Acceleration" in title; abstract names GPU |
| 2 | A Row Decomposition-based Approach for Sparse Matrix Multiplication on GPUs | Pang Meng et al. | Linear Algebra | 10.1145/3627535.3638470 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/4/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title; SpMM kernel design |
| 3 | Arrow Matrix Decomposition: A Novel Approach for Communication-Efficient Sparse Matrix Multiplication | Lukas Gianinazzi et al. | Linear Algebra | 10.1145/3627535.3638496 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/21/x | https://arxiv.org/abs/2402.19364 | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU as the execution target |
| 4 | ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores | Yuetao Chen et al. (Best Paper Award) | Optimizing for Memory | 10.1145/3627535.3638476 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/32/x | NOT_FOUND_AFTER_SEARCH (a related arXiv preprint "Stencil Matrixization", 2310.16298, was surfaced but its identity with this paper is UNVERIFIED) | NOT_FOUND_AFTER_SEARCH | Abstract names Tensor Core; GPU tensor-core remapping of stencils is the mechanism |
| 5 | Exploiting Fine-Grained Redundancy in Set-Centric Graph Pattern Mining | linzhiheng et al. | Graph Processing | 10.1145/3627535.3638507 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/31/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU |
| 6 | FastFold: Optimizing AlphaFold Training and Inference on GPU Clusters | Shenggan Cheng et al. | UNKNOWN (session heading not captured by program fetch) | UNKNOWN (detail page shows no DOI) | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/1/x | Related earlier preprint under a DIFFERENT title: https://arxiv.org/abs/2203.00854 ("FastFold: Reducing AlphaFold Training Time from 11 Days to 67 Hours") — same system name, title not identical | NOT_FOUND_AFTER_SEARCH | "GPU Clusters" in title; abstract names GPU |
| 7 | Fast Kronecker Matrix-Matrix Multiplications on GPUs | Abhinav Jangda, Mohit Yadav | Linear Algebra | 10.1145/3627535.3638489 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/16/x | https://arxiv.org/abs/2401.10187 (arXiv title uses singular "Multiplication") | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title |
| 8 | Gallatin: A General-Purpose GPU Memory Manager | Hunter James McCoy, Prashant Pandey | Optimizing for Memory | 10.1145/3627535.3638499 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/24/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU memory allocator — GPU-specific mechanism is the whole paper |
| 9 | INFINEL: An efficient GPU-based processing method for unpredictable large output graph queries | Sungwoo Park et al. | Graph Processing | 10.1145/3627535.3638490 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/17/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU-based" in title |
| 10 | Liger: Interleaving Intra- and Inter-Operator Parallelism for Distributed Large Model Inference | Jiangsu Du et al. | Compilers and Runtimes for Parallel Systems | 10.1145/3627535.3638466 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/2/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU as the platform for distributed inference |
| 11 | Shared Memory-contention-aware Concurrent DNN Execution for Diversely Heterogeneous System-on-Chips | Ismet Dagli, Mehmet Belviranli | ML Workloads | 10.1145/3627535.3638502 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/26/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names NVIDIA Orin / Xavier and Qualcomm Snapdragon 865 — integrated GPU is one of the contending accelerators |
| 12 | Tetris: Accelerating Sparse Convolution by Exploiting Memory Reuse on GPU | xiaoyanliu et al. | ML Workloads | 10.1145/3627535.3638471 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/5/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPU" in title; GPU memory-reuse mechanism |
| 13 | Training one DeePMD Model in Minutes: a Step Towards Online Learning | Siyu Hu et al. | ML Workloads | UNKNOWN (detail page links artifact instead) | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/29/x | NOT_FOUND_AFTER_SEARCH | https://doi.org/10.5281/zenodo.10213773 | Title has no GPU term; abstract names GPU |
| 14 | A Holistic Approach to Automatic Mixed-Precision Code Generation and Tuning for Affine Programs | Jinchen Xu et al. | Compilers and Runtimes for Parallel Systems | 10.1145/3627535.3638484 | https://ppopp24.sigplan.org/details/PPoPP-2024-papers/14/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names both CPU and GPU as code-generation targets — GPU centrality only PARTIAL (see §6) |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| Extreme-scale Direct Numerical Simulation of Incompressible Turbulence on the Heterogeneous Many-core System | Keywords: heterogeneous/many-core. Abstract names only "Tianhe supercomputer" and "heterogeneous many-core systems"; no GPU, CUDA or vendor GPU device is named. |
| Towards Scalable Unstructured Mesh Computations on Shared Memory Many-Cores | Keywords: shared memory, many-core. Abstract's only GPU reference is "integrate our approach into popular programming models on CPUs and GPUs"; framing and evaluation platform are shared-memory many-core, no GPU-specific mechanism. Borderline — see §6. |
| GraphCube: Interconnection Hierarchy-aware Graph Processing | Keywords: interconnect/hierarchy. Abstract names no GPU hardware; interconnect-hierarchy-aware graph processing on a supercomputer. |
| Fast American Option Pricing using Nonlinear Stencils | Keyword: stencil. Abstract names no hardware; algorithmic/parallel stencil work. |
| Are Your Epochs Too Epic? Batch Free Can Be Harmful | Keyword: memory (reclamation). Abstract names CPU; concurrent-data-structure memory reclamation. |
| Memory Bounds for Bounded Queues | Keyword: memory. Theory paper; no hardware named. |
| CPMA: An Efficient Batch-Parallel Compressed Set Without Pointers | Keywords: compressed/memory. No hardware named; CPU batch-parallel set. |
| Recurrence Analysis for Automatic Parallelization of Subscripted Subscripts | Keyword: compiler. No hardware named; CPU auto-parallelization. |
| Language-Agnostic Static Deadlock Detection for Futures | Keyword: compiler/static analysis. No hardware named. |
| Pure: Evolving Message Passing To Better Leverage Shared Memory Within Nodes | Keywords: shared memory, message passing. No GPU; MPI/shared-memory CPU runtime. |
| Locks as a Resource: Fairly Scheduling Lock Occupation with CFL | Keyword: scheduling. CPU lock scheduling. |
| Scaling Up Transactions with Slower Clocks | Keyword: clocks/memory. CPU software transactional memory. |
| VERLIB: Concurrent Versioned Pointers | Keyword: memory. CPU concurrent data structures. |
| Practical Hardware Transactional vEB Trees | Keyword: hardware. CPU HTM. |
| Parallel Integer Sort: Theory and Practice | — CPU multicore algorithms. |
| Parallel k-Core Decomposition with Batched Updates and Asynchronous Reads | Keyword: memory/async. CPU multicore algorithms. |
| ParANN: Scalable and Deterministic Parallel Graph-Based Approximate Nearest Neighbor Search Algorithms | — CPU multicore algorithms. |
| OsirisBFT: Say No to Task Replication for Scalable Byzantine Fault Tolerant Analytics | — No hardware named; distributed BFT analytics. |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| Arrow Matrix Decomposition: A Novel Approach for Communication-Efficient Sparse Matrix Multiplication | Abstract names GPU as the execution target for the decomposed SpMM |
| ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores | Abstract names Tensor Core; the contribution is a stencil→GEMM remapping onto GPU tensor cores |
| Exploiting Fine-Grained Redundancy in Set-Centric Graph Pattern Mining | Abstract names GPU |
| Liger: Interleaving Intra- and Inter-Operator Parallelism for Distributed Large Model Inference | Abstract names GPU as the distributed-inference platform |
| Shared Memory-contention-aware Concurrent DNN Execution for Diversely Heterogeneous System-on-Chips | Abstract names NVIDIA Orin / Xavier and Snapdragon 865; GPU is one of the co-resident accelerators contending for shared memory |
| Training one DeePMD Model in Minutes: a Step Towards Online Learning | Abstract names GPU |
| A Holistic Approach to Automatic Mixed-Precision Code Generation and Tuning for Affine Programs | Abstract names "programming models on CPUs and GPUs" (GPU centrality PARTIAL) |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| ConvStencil | `TITLE_CORRECTED_TO:` **ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores** — `CONFIRMED_IN_POPULATION` (Best Paper Award; DOI 10.1145/3627535.3638476) |
| Gallatin | `TITLE_CORRECTED_TO:` **Gallatin: A General-Purpose GPU Memory Manager** — `CONFIRMED_IN_POPULATION` (DOI 10.1145/3627535.3638499) |
| A Row Decomposition-based Approach for Sparse Matrix Multiplication on GPUs | `CONFIRMED_IN_POPULATION` — seed title is already the exact official title (DOI 10.1145/3627535.3638470) |

## 6. Unresolved / blocked items

- **No official acceptance-rate statement** ("X of Y submissions") found on any PPoPP 2024 official page. Only a third-party aggregator figure (32/151, 21.2%) is recorded.
- **Session headings for AGAThA and FastFold are UNKNOWN.** The program-page fetch returned 9 session headings covering only 30 of the 32 papers; the session containing these two was not captured. Not inferred.
- **DOIs UNKNOWN for two candidates** (FastFold, Training one DeePMD Model in Minutes): their official detail pages do not expose a DOI. `dl.acm.org` (403) and `dblp.org` (robots-disallowed) could not be used.
- **Borderline, needs full text:** *Towards Scalable Unstructured Mesh Computations on Shared Memory Many-Cores* — abstract mentions GPUs only as a programming-model integration target; placed in §3 but should be re-checked against the full paper.
- **Partial GPU centrality:** *A Holistic Approach to Automatic Mixed-Precision Code Generation and Tuning for Affine Programs* — listed as a candidate on the strength of "CPUs and GPUs" in the abstract; whether a GPU-specific mechanism is central is UNVERIFIED.
- Public full texts recorded as `NOT_FOUND_AFTER_SEARCH` were searched on arxiv.org via web search on 2026-09-18. arXiv's own search UI is robots-disallowed and `export.arxiv.org` returns 403, so only indexed search was available.

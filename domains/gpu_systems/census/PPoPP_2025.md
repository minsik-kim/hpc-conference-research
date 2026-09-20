# PPoPP 2025 — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **38** |
| counted items excluded from population | **posters: 11** (Sun 2 Mar poster session; each is explicitly prefixed `POSTER:` on its official detail page and is *interleaved into the accepted-papers track page*); **workshops/tutorials: 6** co-located events (17th GPGPU workshop, 2nd ▽PP, FastCode Programming Challenge FCPC, ExHET'25, Workshop on Parallel Graph Processing and Future Challenges, Memory-Centric Computing / DNN-training tutorials); artifact-evaluation track (separate track); keynotes |
| population source (primary) | https://ppopp25.sigplan.org/program/program-PPoPP-2025/ — 11 numbered main-conference sessions containing exactly 38 papers, plus a separate poster session — `official-program` |
| population source (corroborating) | (a) per-item official detail pages `https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/<N>/x` for N=1..49: **38 typed "Talk", 11 typed "Poster"** — `official-program`; (b) https://ppopp25.sigplan.org/track/PPoPP-2025-Main-Conference-1 — 49 entries = 38 + 11 — `official-program`; (c) https://csconfstats.xoveexu.com/conferences/ppopp/ — "189 submissions / 38 accepted / 20.1%" — third-party statistics aggregator |
| source class | `official-program` (primary + corroborating a,b); `search-engine` (c) |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | **Important trap:** the PPoPP 2025 "Main Conference" track page mixes the 11 posters into the accepted-papers list, giving a misleading apparent total of 49. Posters were separated two ways that agree exactly: (i) they are absent from the 11 numbered program sessions, and (ii) their official detail pages carry a `POSTER:` title prefix / Poster event type. 38 = 49 − 11 and also equals the session-by-session sum (3+3+4+3+3+3+3+4+4+4+4). |

### 1.1 Population evidence notes

- Source statement: the program page lists Sessions 1–11 with 3, 3, 4, 3, 3, 3, 3, 4, 4, 4, 4 papers = **38**.
- Source statement: enumerating detail pages for researchr event IDs 1..49 yields exactly 11 Poster records (IDs 3, 7, 9, 12, 17, 25, 27, 31, 33, 45, 46) and 38 Talk records. The 38 Talk titles are a set-equal match to the 38 titles in the 11 program sessions (verified title-by-title).
- Source statement: the 11 poster titles are — High-performance Visual Semantics Compression for AI-Driven Science; Triangle Counting on Tensor Cores; Magneto: Accelerating Parallel Structures in DNNs via Co-Optimization of Operators; A General and Scalable GCN Training Framework on CPU Supercomputers; Minimizing speculation overhead in a parallel recognizer for regular texts; Big Atomics and Fast Concurrent Hash Tables; Transactional Data Structures with Orthogonal Metadata; Boost Lock-free Queue and Stack with Batching; TENSORMD: Molecular Dynamics Simulation with Ab Initio Accuracy of 50 Billion Atoms; Frontier-guided Graph Reordering; FastBWA: Practical and Cost-Efficient Genome Sequence Alignment Pipeline.
- Source statement (third-party): csconfstats reports 38 accepted of 189 submitted (20.1%) — this independently matches the 38 derived from two official enumerations.
- Inference: three agreeing enumerations ⇒ EXACT.
- **No official acceptance-rate statement was located on any PPoPP 2025 official page.** The 38/189 figure is third-party.
- Proceedings are ACM `10.1145/3710848`. **Per-paper DOIs are UNKNOWN**: the PPoPP 2025 researchr detail pages do not expose DOIs (unlike 2024 and 2026), `dl.acm.org` returns 403, `dblp.org` is robots-disallowed, and `conference-publishing.com/toc/PPOPP25` returns "Problem with empty event record".

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 38 regular
papers; every abstract read via its official detail page), not over the seed
list. Keyword hits were used only to order review, never to decide relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Accelerating GNNs on GPU Sparse Tensor Cores through N:M Sparsity-Oriented Graph Reordering | Jou-An Chen et al. | S1 Graph Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/32/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Abstract names NVIDIA A100 Sparse Tensor Cores; N:M sparsity mapping onto SpTC is the mechanism |
| 2 | Helios: Efficient Distributed Dynamic Graph Sampling for Online GNN Inference | Jie Sun et al. | S1 Graph Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/6/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU |
| 3 | Adaptive Parallel Training for Graph Neural Networks | Kaihao Ma et al. | S1 Graph Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/34/x | NOT_FOUND_AFTER_SEARCH | https://anonymous.4open.science/r/APT-1CAB | Title has no GPU term; abstract names GPU |
| 4 | RT–BarnesHut: Accelerating Barnes–Hut Using Ray-Tracing Hardware | Vani Nagarajan et al. | S2 GPU I | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/36/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Abstract names GPU/NVIDIA; repurposes GPU RT cores |
| 5 | EVeREST: An Effective and Versatile Runtime Energy Saving Tool for GPUs | Anna Yue, Pen-Chung Yew, Sanyam Mehta | S2 GPU I | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/26/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "for GPUs" in title; GPU power/energy runtime |
| 6 | TurboFFT: Co-Designed High-Performance and Fault-Tolerant Fast Fourier Transform on GPUs | Shixun Wu et al. | S2 GPU I | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/5/x | https://arxiv.org/abs/2412.05824 | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title; abstract names NVIDIA A100 and Tesla T4 |
| 7 | Harnessing Inter-GPU Shared Memory for Seamless MoE Communication-Computation Fusion | Hulin Wang et al. | S4 Memory | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/19/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "Inter-GPU Shared Memory" in title; abstract names GPU |
| 8 | FlashTensor: Optimizing Tensor Programs by Leveraging Fine-grained Tensor Property | Runxin Zhong et al. | S5 Deep Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/15/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names H100 and A100 GPUs |
| 9 | Mario: Near Zero-cost Activation Checkpointing in Pipeline Parallelism | Weijian Liu, Mingzhen Li, Guangming Tan, Weile Jia | S5 Deep Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/29/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU (GPU-memory-driven checkpointing) |
| 10 | COMPSO: Optimizing Gradient Compression for Distributed Training with Second-Order Optimizers | Baixi Sun et al. | S5 Deep Neural Networks | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/4/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU |
| 11 | MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models | Elias Frantar et al. | S6 Large Language Models | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/22/x | https://arxiv.org/abs/2408.11743 | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU/NVIDIA; mixed-precision GPU GEMM kernel |
| 12 | WeiPipe: Weight Pipeline Parallelism for Communication-Effective Long-Context Large Model Training | Junfeng Lin et al. | S6 Large Language Models | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/20/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPUs and **NVLink** |
| 13 | ATTNChecker: Highly-Optimized Fault Tolerant Attention for Large Language Model Training | Yuhang Liang et al. | S6 Large Language Models | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/21/x | https://arxiv.org/abs/2410.11720 | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; GPU attention-kernel ABFT (GPU centrality from arXiv full text, see §6) |
| 14 | SGDRC: Software-Defined Dynamic Resource Control for Concurrent DNN Inference on NVIDIA GPUs | Yongkang Zhang et al. | S7 Scheduling and Resource Management | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/48/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "NVIDIA GPUs" in title; GPU spatial-sharing / resource control |
| 15 | FlashSparse: Minimizing Computation Redundancy for Fast Sparse Matrix Multiplications on Tensor Cores | Jinliang Shi et al. | S8 Tensor Cores | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/10/x | https://arxiv.org/abs/2412.11007 | NOT_FOUND_AFTER_SEARCH | Abstract names GPU / Tensor Core |
| 16 | Acc-SpMM: Accelerating General-purpose Sparse Matrix-Matrix Multiplication with GPU Tensor Cores | Haisha Zhao et al. | S8 Tensor Cores | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/39/x | https://arxiv.org/abs/2501.09251 | NOT_FOUND_AFTER_SEARCH | "GPU Tensor Cores" in title |
| 17 | BerryBees: Breadth First Search by Bit-Tensor-Cores | Yuyao Niu, Marc Casas | S8 Tensor Cores | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/11/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Abstract names NVIDIA; BFS on GPU bit-tensor-cores |
| 18 | FlashFFTStencil: Bridging Fast Fourier Transforms to Memory-Efficient Stencil Computations on Tensor Core Units | Haozhi Han et al. | S8 Tensor Cores | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/47/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Abstract names Tensor Core Units (TCU) |
| 19 | LibRTS: A Spatial Indexing Library by Ray Tracing | Liang Geng, Rubao Lee, Xiaodong Zhang | S9 Concurrent Data Structures and Synchronization II | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/2/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU ray-tracing cores |
| 20 | Popcorn: Accelerating Kernel K-means on GPUs through Sparse Linear Algebra | Julian Bellavita et al. | S10 GPU II | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/38/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title |
| 21 | Swift Unfolding of Communities: GPU-Accelerated Louvain Algorithm | Zhibin Wang et al. | S10 GPU II | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/35/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU-Accelerated" in title |
| 22 | GLUMIN: Fast Connectivity Check Based on LUTs For Efficient Graph Pattern Mining | Weichen Cao, Ke Meng, linzhiheng, Guangming Tan | S10 GPU II | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/40/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names GPU; placed in the GPU II session |
| 23 | Improving Tridiagonalization Performance on GPU Architectures | WangHansheng et al. | S10 GPU II | UNKNOWN | https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/44/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPU Architectures" in title |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| AC-Cache: A Memory-Efficient Caching System for Small Objects via Exploiting Access Correlations | Keywords: memory, cache. Abstract names no GPU hardware; object-cache system (S4 Memory). |
| Effectively Virtual Page Prefetching via Spatial-Temporal Patterns for Memory-intensive Cloud Applications | Keywords: prefetch, memory, TLB-adjacent. Abstract names no GPU; host virtual-memory paging for cloud VMs. |
| Publish on Ping: A Better Way to Publish Reservations in Memory Reclamation for Concurrent Data Structures | Keyword: memory. No hardware named; CPU concurrent memory reclamation. |
| Jigsaw: Toward Conflict-free Vectorized Stencil Computation by Tessellating Swizzled Registers | Keywords: stencil, register, vectorized. Abstract names no hardware device; framing is vector-register (SIMD) tessellation, not a GPU mechanism. Borderline — see §6. |
| Semi-StructMG: A Fast and Scalable Semi-Structured Algebraic Multigrid | Keywords: sparse/solver. Abstract names no hardware. |
| WaterWise: Co-optimizing Carbon- and Water-Footprint Toward Environmentally Sustainable Cloud Computing | Keyword: power/energy. Abstract names no GPU; datacenter sustainability scheduling. |
| An AI-Enhanced 1km-Resolution Seamless Global Weather and Climate Model to Achieve Year-Scale Simulation Speed using 34 Million Cores | Keywords: scale, kernel. Abstract names **Sunway** — not a GPU platform. |
| Aggregating Funnels for Faster Fetch&Add and Queues | Keywords: atomics/collective-like. No hardware named; CPU synchronization. |
| Reciprocating Locks | — No hardware named; CPU locks. |
| Fairer and More Scalable Reader-Writer Locks by Optimizing Queue Management | — No hardware named; CPU locks. |
| Balanced Allocations over Efficient Queues: A Fast Relaxed FIFO Queue | — No hardware named; CPU concurrent queues. |
| PANNS: Enhancing Graph-based Approximate Nearest Neighbor Search through Recency-aware Construction and Parameterized Search | Keyword: search/memory. No hardware named. |
| Crystality: A Programming Model for Smart Contracts on Parallel EVMs | Keyword: programming model. No hardware named. |
| DORADD: Deterministic Parallel Execution in the Era of Microsecond-Scale Computing | Keyword: scheduling. Abstract names CPU. |
| SBMGT: Scaling Bayesian Multinomial Group Testing | — No hardware named. |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| Helios: Efficient Distributed Dynamic Graph Sampling for Online GNN Inference | Abstract names GPU |
| Adaptive Parallel Training for Graph Neural Networks | Abstract names GPU |
| RT–BarnesHut: Accelerating Barnes–Hut Using Ray-Tracing Hardware | Abstract names GPU/NVIDIA; the mechanism is GPU RT-core repurposing |
| FlashTensor: Optimizing Tensor Programs by Leveraging Fine-grained Tensor Property | Abstract names H100 / A100 |
| Mario: Near Zero-cost Activation Checkpointing in Pipeline Parallelism | Abstract names GPU (GPU memory capacity is the constraint being optimized) |
| COMPSO: Optimizing Gradient Compression for Distributed Training with Second-Order Optimizers | Abstract names GPU |
| MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models | Abstract names GPU/NVIDIA; mixed-precision GPU kernel |
| WeiPipe: Weight Pipeline Parallelism for Communication-Effective Long-Context Large Model Training | Abstract names GPUs and NVLink |
| ATTNChecker: Highly-Optimized Fault Tolerant Attention for Large Language Model Training | GPU attention kernels (evidenced by arXiv 2410.11720; the researchr abstract does not name a device — see §6) |
| LibRTS: A Spatial Indexing Library by Ray Tracing | Abstract names GPU ray-tracing cores |
| GLUMIN: Fast Connectivity Check Based on LUTs For Efficient Graph Pattern Mining | Abstract names GPU; scheduled in the "GPU II" session |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| FlashSparse | `TITLE_CORRECTED_TO:` **FlashSparse: Minimizing Computation Redundancy for Fast Sparse Matrix Multiplications on Tensor Cores** — `CONFIRMED_IN_POPULATION` (S8 Tensor Cores) |
| BerryBees | `TITLE_CORRECTED_TO:` **BerryBees: Breadth First Search by Bit-Tensor-Cores** — `CONFIRMED_IN_POPULATION` (S8 Tensor Cores) |
| Harnessing Inter-GPU Shared Memory for Seamless MoE Communication-Computation Fusion | `CONFIRMED_IN_POPULATION` — seed title is the exact official title (S4 Memory) |
| Acc-SpMM | `TITLE_CORRECTED_TO:` **Acc-SpMM: Accelerating General-purpose Sparse Matrix-Matrix Multiplication with GPU Tensor Cores** — `CONFIRMED_IN_POPULATION` (S8) |
| EVeREST | `TITLE_CORRECTED_TO:` **EVeREST: An Effective and Versatile Runtime Energy Saving Tool for GPUs** — `CONFIRMED_IN_POPULATION` (S2 GPU I) |
| FlashFFTStencil | `TITLE_CORRECTED_TO:` **FlashFFTStencil: Bridging Fast Fourier Transforms to Memory-Efficient Stencil Computations on Tensor Core Units** — `CONFIRMED_IN_POPULATION` (S8) |
| a paper about accelerating GNNs on GPU sparse tensor cores through N:M sparsity | `TITLE_CORRECTED_TO:` **Accelerating GNNs on GPU Sparse Tensor Cores through N:M Sparsity-Oriented Graph Reordering** — `CONFIRMED_IN_POPULATION` (S1) |
| a GPU Louvain community-detection paper | `TITLE_CORRECTED_TO:` **Swift Unfolding of Communities: GPU-Accelerated Louvain Algorithm** — `CONFIRMED_IN_POPULATION` (S10 GPU II) |
| TurboFFT | `TITLE_CORRECTED_TO:` **TurboFFT: Co-Designed High-Performance and Fault-Tolerant Fast Fourier Transform on GPUs** — `CONFIRMED_IN_POPULATION` (S2 GPU I) |
| GLUMIN | `TITLE_CORRECTED_TO:` **GLUMIN: Fast Connectivity Check Based on LUTs For Efficient Graph Pattern Mining** — `CONFIRMED_IN_POPULATION` (S10 GPU II) |

All 10 PPoPP 2025 seeds are present in the main-conference population. None resolved to `NOT_IN_MAIN_POPULATION` or `NOT_FOUND`.

## 6. Unresolved / blocked items

- **Per-paper DOIs are UNKNOWN for every PPoPP 2025 entry.** The 2025 researchr detail pages do not publish DOIs; `dl.acm.org` (403), `dblp.org` (robots-disallowed) and `conference-publishing.com/toc/PPOPP25` ("Problem with empty event record") all failed. Proceedings-level DOI is `10.1145/3710848`.
- **No official acceptance-rate statement** found; 38/189 (20.1%) is a third-party aggregator figure that happens to match the officially derived 38.
- **ATTNChecker**: the official detail page's abstract does not name a device (the fetch's "GPU/CUDA" was flagged "implied"). It is listed as a candidate on the basis of the matching arXiv preprint 2410.11720; the GPU-specific mechanism should be confirmed from the full text at the verdict step.
- **Borderline, needs full text:** *Jigsaw: Toward Conflict-free Vectorized Stencil Computation by Tessellating Swizzled Registers* — placed in §3 because no hardware is named and the framing is vector-register SIMD; a GPU register-swizzle reading cannot be ruled out without the full paper.
- Artifact/code URLs: only one was discoverable from official pages (Adaptive Parallel Training → anonymous.4open.science). PPoPP 2025 artifact-evaluation badges exist but the AE track page does not link per-paper Zenodo records; recorded as `NOT_FOUND_AFTER_SEARCH`.
- Public full texts recorded as `NOT_FOUND_AFTER_SEARCH` were searched on arxiv.org via web search on 2026-09-18 (arXiv's own search UI is robots-disallowed; `export.arxiv.org` returns 403).

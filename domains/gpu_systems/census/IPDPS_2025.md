# IPDPS 2025 — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **105** (official statement) |
| counted items excluded from population | **posters: 21** (official statement: "21 papers presented as posters"); workshops (IPDPS 2025 co-located workshops — count not stated on the pages reached: UNKNOWN); tutorials; PhD Forum; keynotes; all-conference panel; industry participation |
| population source (primary) | https://www.ipdps.org/ipdps2025/index.html — official post-conference report: "the main conference included the **105 contributed papers** selected for presentation in **33 technical sessions** and **21 papers presented as posters**" — `official-program` |
| population source (corroborating) | (a) https://www.ipdps.org/ipdps2025/2025-advance-program.html — session-by-session listing, Sessions 1–33 plus a plenary "Best Paper Nominees" block; a flat enumeration of it yields **106 titles** — `official-program`; (b) https://openaccept.org/c/sys/ipdps/ — "425 submissions / 105 accepted / 24.71%" — third-party aggregator; (c) https://csconfstats.xoveexu.com/conferences/ipdps/ — "Submissions 425 / Accepted 105 / 24.7%" — third-party aggregator |
| source class | `official-program` (primary + corroborating a); `search-engine` (b, c) |
| enumeration completeness | `APPROXIMATE` |
| paper-type mixing notes | The advance program shows 33 numbered topical sessions **plus a separately-headed plenary "Best Paper Nominees" block of 5 papers**. Summing the numbered sessions gives 101 (Sessions 1 and 2 hold 4 papers each, Sessions 3–33 hold 3 each: 8 + 93 = 101); 101 + 5 = **106**. The official report says 105 papers in 33 sessions. The one-paper discrepancy is **unresolved** — see §1.1. Posters are on a separate page and are *not* interleaved into the technical sessions, so no poster/paper mixing trap exists here. |

### 1.1 Population evidence notes

- Source statement (official report page, verbatim): "the main conference included the 105 contributed papers selected for presentation in 33 technical sessions and 21 papers presented as posters".
- Source statement (official advance program): a flat, page-ordered enumeration of every technical paper title yields **N = 106** (Sessions 1–33 = 101 titles; Best Paper Nominees plenary = 5 titles). No title appears twice — the 5 Best Paper Nominee titles do not recur in any numbered session.
- **Unresolved discrepancy: official 105 vs enumerated 106.** Two readings are consistent with the evidence and neither can be confirmed from a reachable source: (i) one paper listed in the advance program was withdrawn before presentation, so 105 were actually presented; (ii) the official sentence's "33 technical sessions" figure and its "105" figure were written against slightly different cuts of the program. **The count is recorded as 105 because that is the only official number; the extra advance-program title is not identifiable.** No count was invented.
- **Official acceptance statistic:** official pages state only the accepted figure (105); **no submission total appears on any official IPDPS 2025 page.** The "425 submissions / 24.7%" figure is third-party (two independent aggregators agree).
- **Authors are NOT published on the official advance program page** (verified by a second fetch that explicitly asked for them: "Author affiliations are not displayed on this advance program page"). Author lists for IPDPS 2025 live on the Linklings program (`https://ssl.linklings.net/conferences/ipdps/ipdps2025_program/...`), which is **robots-disallowed** end to end (even `/robots.txt` on that host is disallowed). Hence the Authors column below is `UNKNOWN` except where an external source supplied it.
- **Abstracts: not reachable.** Same cause (Linklings robots-disallowed; IEEE Xplore 418). STEP B is therefore title-based; every non-obvious judgment is tagged `TITLE_ONLY`.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 106
advance-program titles read in page order), not over the seed list. Keyword
hits were used only to order review, never to decide relevance. Because no
abstract host was reachable, screening is title-based — see §1.1 and §6.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | ALGAS: A Low-latency GPU-Accelerated Approximate Nearest Neighbor Search System | UNKNOWN (not published on the official program page) | S5 Graph Algorithms I | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU-Accelerated" in title |
| 2 | FastCHGNet: Training one Universal Interatomic Potential to 1.5 Hours with 32 GPUs | UNKNOWN | S6 AI and Applications | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "32 GPUs" in title; ML-training acceleration |
| 3 | A Bidirectional GPU Algorithm for Computing Maximum Matchings in Bipartite Graphs | UNKNOWN | S8 Graph Algorithms II | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU Algorithm" in title |
| 4 | The Tensor-Core Beamformer: A High-Speed Signal-Processing Library for Multidisciplinary Use | UNKNOWN | S14 Data and Signal Processing | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "Tensor-Core" in title; Tensor Core execution-unit exploitation — GPU mechanism contribution |
| 5 | A GPU-Accelerated Distributed Algorithm for Optimal Power Flow in Distribution Systems | UNKNOWN | S17 HPC Applications I | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU-Accelerated" in title |
| 6 | Reducing the End-to-End Latency of DNN-based Recommendation Systems Deployed in GPU Pools | UNKNOWN | S18 Latency and Performance for ML | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU Pools" in title; GPU resource pooling for inference |
| 7 | A New Spin on the Fast Multipole Method for GPUs: Rethinking the Far-Field Operators | UNKNOWN | S20 HPC Applications II | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "for GPUs" in title |
| 8 | Large Scale Finite-Temperature Real-time Time Dependent Density Functional Theory Calculation with Hybrid Functional on ARM and GPU Systems | UNKNOWN | S20 HPC Applications II | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU Systems" in title |
| 9 | Fast and Effective Lossy Compression on GPUs and CPUs with Guaranteed Error Bounds | UNKNOWN | S22 Compression and Data Reduction I | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs and CPUs" in title; GPU compression kernels — GPU mechanism (memory/compression) contribution |
| 10 | BRP-SpMM: Block-Row Partition Based Sparse Matrix Multiplication with Tensor and CUDA Cores | UNKNOWN | S23 Matrix Multiplication | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "Tensor and CUDA Cores" in title; SpMM mapping across two GPU execution units — GPU mechanism contribution |
| 11 | NM-SpMM: Accelerating Matrix Multiplication Using N:M Sparsity with GPGPU | UNKNOWN | S23 Matrix Multiplication | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPGPU" + "N:M Sparsity" in title; sparse GPU GEMM mechanism |
| 12 | Unified Designs of Multi-rail-aware MPI Allreduce and Alltoall Operations Across Diverse GPU and Interconnect Systems | UNKNOWN | S24 Communication | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "Multi-rail" + "GPU and Interconnect" in title; GPU-aware multi-rail collectives — GPU communication mechanism |
| 13 | HiCCL: A Hierarchical Collective Communication Library | UNKNOWN | S24 Communication | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | `collective` keyword; hierarchical collective composition, placed in the same Communication session as two GPU-interconnect papers. `TITLE_ONLY` — GPU residency not verifiable without the abstract |
| 14 | Accelerating Homotopy Continuation with GPUs: Application to Trifocal Pose Estimation | UNKNOWN | S31 Data and Image Processing | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "with GPUs" in title |
| 15 | Fine-Grained Global Search for Inputs Triggering Floating-Point Exceptions in GPU Programs | UNKNOWN | S32 Error Prediction and Fault Tolerance | UNKNOWN | https://www.ipdps.org/ipdps2025/2025-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU Programs" in title; GPU numerical-reliability tooling — GPU mechanism (reliability) contribution |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| Performance Characterization of CXL Memory and Its Use Cases | `memory` keyword; **CXL host memory**, not GPU memory |
| RXT: Reflexive Address Translation for Pointer-Chasing Workloads | `TLB`/`memory` keywords; **CPU address translation** |
| CoRD: Converged RDMA Dataplane | `RDMA` keyword; host-side RDMA dataplane, no GPU term |
| Accelerating Sparse Linear Solvers on Intelligence Processing Units | `sparse` keyword; target is the **Graphcore IPU** |
| A Memory-efficient and Computation-balanced Lossy Compressor on Wafer-Scale Engine | `memory`/`compression` keywords; target is the **Cerebras Wafer-Scale Engine** |
| Enhanced JPEG Decoding using PIM Architectures with Parallel MCU Processing | `memory` keyword; **processing-in-memory**, not GPU |
| An Effective Uncorrectable Memory Error Prediction Framework by Exploiting UPH Indicator in Production Environment | `memory` keyword; **host DRAM** uncorrectable-error prediction |
| To Compress or Not To Compress: Energy and Runtime Trade-Offs in Lossy Compressed I/O | `compression`/`power` keywords; I/O-level compression trade-off study, no GPU term |
| Improving the Efficiency of Interpolation-Based Scientific Data Compressors with Adaptive Quantization Index Prediction | `compression` keyword; compressor algorithmics, no GPU term |
| An Adaptive Two-Stage Algorithm for Error-Bounded Scientific Data Compression | `compression` keyword; algorithmic, no GPU term |
| Achieving Better Benefits via Flexible Feature Matching in Post-Deduplication Delta Compression | `compression` keyword; storage deduplication |
| HPDR: High-Performance Portable Scientific Data Reduction Framework | `compression` keyword; portability framework, no GPU term (see §6 — portable frameworks often include GPU back-ends) |
| Sensitivity and Impacts on Parallel Compression of Prediction of Lossy Compression Ratios for Scientific Data | `compression` keyword; ratio-prediction study |
| Enabling Efficient Error-controlled Lossy Compression for Unstructured Scientific Data | `compression` keyword; Best Paper Nominee; unstructured-mesh compressor, no GPU term |
| Accelerating Graph Neural Networks Using a Novel Computation-Friendly Matrix Compression Format | `compression`/`sparse` keywords; a matrix format, platform not named in the title |
| Graph Input-Aware Matrix Multiplication for Pruned Graph Neural Network Acceleration | `sparse`/`kernel` keywords; platform not named in the title (same session as two GPU papers — see §6) |
| Leveraging Compilation Statistics for Compiler Phase Ordering | `compiler` keyword; LLVM phase ordering, no GPU |
| PolyMorphous: An MLIR-Based Polyhedral Compiler with Loop Transformation Primitives | `compiler` keyword; Best Paper Nominee; MLIR loop transformations, no GPU term in title |
| Gensor: A Graph-based Construction Tensor Compilation Method for Deep Learning | `compiler` keyword; tensor compilation, platform not named in the title |
| Compiler, Runtime, and Hardware Parameters Design Space Exploration | `compiler` keyword; DSE methodology |
| Using performance projection for design-space exploration on future HPC CPU architectures | `compiler`-adjacent; explicitly **CPU** architectures |
| Optimizing Fine-Grained Parallelism Through Dynamic Load Balancing on Multi-Socket Many-Core Systems | `memory` keyword; **multi-socket CPU** |
| Phase-based Frequency Scaling for Energy-efficient Heterogeneous Computing | `power` keyword; DVFS on heterogeneous **CPU** cores in the title framing |
| NBLFQ: a lock-free MPMC queue optimized for low contention | `memory` keyword; concurrent data structure, no GPU |
| FATHOM: Fast Attention Through Optimizing Memory | `memory`/`kernel` keywords; attention memory optimisation — platform not named in the title (see §6) |
| Characterizing the Behavior and Impact of KV Caching on Transformer Inferences under Concurrency | `memory` keyword; KV-cache behaviour, platform not named in the title (see §6) |
| Longer Attention Span: Increasing Transformer Context Length with Sparse Graph Processing Techniques | `sparse` keyword; algorithmic, platform not named |
| GIFTS: Efficient GCN Inference Framework on PyTorch-CPU via Exploring the Sparsity | `sparse` keyword; explicitly **PyTorch-CPU** |
| Automated MPI-X code generation for scalable finite-difference solvers | `compiler`/`kernel` keywords; MPI-X codegen, platform not named |
| Accelerating the Dutch Atmospheric Large-Eddy Simulation (DALES) model with OpenACC | OpenACC is a GPU-directed model but the title names no GPU — **see §6**, held as unresolved rather than asserted |
| Scalable and portable LU factorization with partial pivoting on top of runtime systems | `kernel` keyword; task-runtime LU, platform not named |
| Adaptive s-step GMRES with randomized and truncated low-synchronization orthogonalization | `kernel` keyword; Krylov algorithmics |
| GuardianOMP: A framework for highly productive fault tolerance via OpenMP task-level replication | `kernel` keyword; **OpenMP CPU task** replication |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| The Tensor-Core Beamformer: A High-Speed Signal-Processing Library for Multidisciplinary Use | "Tensor-Core" is an NVIDIA GPU execution unit; the contribution is mapping beamforming onto it |
| HiCCL: A Hierarchical Collective Communication Library | `collective` keyword; included on the keyword-ordered review as a communication-library contribution. `TITLE_ONLY` — GPU residency unverified (abstract host robots-disallowed) |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| NM-SpMM | `TITLE_CORRECTED_TO:` **NM-SpMM: Accelerating Matrix Multiplication Using N:M Sparsity with GPGPU** — CONFIRMED_IN_POPULATION, Session 23 Matrix Multiplication |
| a paper on fast and effective lossy compression on GPUs and CPUs | `TITLE_CORRECTED_TO:` **Fast and Effective Lossy Compression on GPUs and CPUs with Guaranteed Error Bounds** — CONFIRMED_IN_POPULATION, Session 22 Compression and Data Reduction I |
| The Tensor-Core Beamformer | `TITLE_CORRECTED_TO:` **The Tensor-Core Beamformer: A High-Speed Signal-Processing Library for Multidisciplinary Use** — CONFIRMED_IN_POPULATION, Session 14 Data and Signal Processing |
| HiCCL | `TITLE_CORRECTED_TO:` **HiCCL: A Hierarchical Collective Communication Library** — CONFIRMED_IN_POPULATION, Session 24 Communication |
| a multi-rail MPI collective paper | `TITLE_CORRECTED_TO:` **Unified Designs of Multi-rail-aware MPI Allreduce and Alltoall Operations Across Diverse GPU and Interconnect Systems** — CONFIRMED_IN_POPULATION, Session 24 Communication |

## 6. Unresolved / blocked items

- **`census_status: PARTIAL_CENSUS`.** Reason: the official count (105) and the official advance-program enumeration (106 titles) differ by one and the discrepancy cannot be resolved from any reachable source. The population *count* is officially attested; the *title list* is one item longer than the official count and the surplus item is unidentifiable.
- **Authors: UNKNOWN for every paper.** The official advance program does not publish them (explicitly verified). The author host is the Linklings program site, which is **robots-disallowed for the whole host** (`https://ssl.linklings.net/robots.txt` is itself robots-disallowed). `ieeexplore.ieee.org` → HTTP 418; `dblp.org`/`dblp.uni-trier.de`/`dblp.dagstuhl.de` → robots-disallowed; `dl.acm.org` → 403; `web.archive.org` → site blocked. No author name was invented.
- **Per-paper DOIs: UNKNOWN for all papers** — same blocked sources.
- **Abstracts: not reachable for any 2025 paper** — same blocked sources. Consequently the instruction "include GPU-resident papers without GPU in the title where an abstract supports it" could be honoured only for titles carrying a GPU-family term. The following titles are the strongest un-resolvable candidates and are recommended for a follow-up abstract pass once an abstract source is available: *Accelerating the Dutch Atmospheric Large-Eddy Simulation (DALES) model with OpenACC* (OpenACC is overwhelmingly a GPU offload model); *FATHOM: Fast Attention Through Optimizing Memory*; *Characterizing the Behavior and Impact of KV Caching on Transformer Inferences under Concurrency*; *FlexRLHF: A Flexible Placement and Parallelism Framework for Efficient RLHF Training* (Best Paper Nominee); *The Artificial Scientist: in-transit Machine Learning of Plasma Simulations* (Best Paper Nominee); *Graph Input-Aware Matrix Multiplication for Pruned Graph Neural Network Acceleration* (Session 23, alongside two GPU papers); *Accelerating Tensor-train Decomposition on Graph Neural Networks*; *HPDR: High-Performance Portable Scientific Data Reduction Framework*; *CELLO: Co-designing Schedule and Hybrid Implicit/Explicit Buffer for Complex Tensor Reuse*; *GNNPerf: Towards Effective Performance Profiling and Analysis across GNN Frameworks*; *PredTOP: Latency Predictor for Distributed Deep Learning Training with Operator Parallelism*; *SPRT²: Scalable, Parallel, and Real-Time fMRI Data Analysis on Heterogeneous Architectures*; *InkStream: Instantaneous GNN Inference on Dynamic Graphs via Incremental Update*.
- **Official submission total: not published on any official IPDPS 2025 page.** Third-party aggregators report 425 submissions / 24.7%.
- **Co-located workshop count for 2025: UNKNOWN** (not stated on the pages reached).

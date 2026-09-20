# IPDPS 2024 — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **88** |
| counted items excluded from population | **posters ("poster-elect papers"): 24** (official statement); **workshops: 17, "with over 150 papers presented"** (official statement); **PhD Forum** (poster-format, count not stated on the source page — UNKNOWN); keynotes; all-conference panel; tutorials; industry participation |
| population source (primary) | https://www.ipdps.org/ipdps2024/index.html — official post-conference report: "88 contributed papers selected for presentation in 19 technical sessions", "24 poster-elect papers presented as posters", "17 workshops with over 150 papers presented" — `official-program` |
| population source (corroborating) | (a) https://www.ipdps.org/ipdps2024/2024-advance-program.html — full session-by-session enumeration: **19 technical sessions containing exactly 88 papers** — `official-program`; (b) https://openaccept.org/c/sys/ipdps/ — "337 submissions / 88 accepted / 26.11%" — third-party statistics aggregator; (c) https://csconfstats.xoveexu.com/conferences/ipdps/ — "Submissions 337 / Accepted 88 / 26.1%" — third-party statistics aggregator |
| source class | `official-program` (primary + corroborating a); `search-engine` (b, c) |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | IPDPS 2024 separates types cleanly. The advance program lists only regular technical sessions (1A/1B … 9A/9B plus a plenary "Best Papers" session = 19 session slots, 2 parallel tracks); posters, PhD Forum, workshops and tutorials appear on separate days/pages and are not interleaved into the technical sessions. The plenary **Best Papers** session (4 papers) is counted inside the 88 — its papers do not recur in the topical sessions. |

### 1.1 Population evidence notes

- Source statement (official report page): "88 contributed papers selected for presentation in 19 technical sessions" and "24 poster-elect papers presented as posters" and "17 workshops with over 150 papers presented".
- Source statement (official advance program), per-session counts: 1A=6, 1B=6, 2A=3, 2B=3, 3A=5, 3B=5, Best Papers=4, 4A=6, 4B=6, 5A=3, 5B=3, 6A=5, 6B=5, 7A=6, 7B=6, 8A=4, 8B=4, 9A=4, 9B=4 → **19 sessions, 88 papers**. This is a set-exact match to the official 88/19 statement.
- **Official acceptance statistic:** the official pages state the *accepted* figure (88) but **no submission total**. The "337 submissions / 26.1%" figure is third-party only (two independent aggregators agree).
- Inference: official count + independent official enumeration agree exactly ⇒ `EXACT` / `COMPLETE_CENSUS`.
- **Per-paper DOIs are UNKNOWN for every paper.** IEEE Xplore (`ieeexplore.ieee.org`) returns HTTP 418 through this proxy; `dblp.org` and `dblp.uni-trier.de` are robots-disallowed; `dl.acm.org` is 403; `web.archive.org` is blocked. The IPDPS advance program does not publish DOIs.
- **Abstracts were not reachable.** For 2024 the abstract host is IEEE Xplore (blocked). The advance program gives titles + authors only. Consequently STEP B screening below is *title-and-author based* for all but the papers where an external public full text was located; every such judgment is tagged `TITLE_ONLY`.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 88 regular
papers, every title and author list read from the official advance program),
not over the seed list. Keyword hits were used only to order review, never to
decide relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining | Baolin Li et al. | 3B Scheduling I | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "Production GPU Clusters" in title; GPU-cluster telemetry/monitoring analysis |
| 2 | Optimized GPU Implementation of Grid Refinement in Lattice Boltzmann Method | Ahmed H. Mahmoud, Hesam Salehipour, Massimiliano Meneghin | 4A Applications II | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU Implementation" in title; application acceleration |
| 3 | Alya towards Exascale: Optimal OpenACC Performance of the Navier-Stokes Finite Element Assembly on GPUs | Herbert Owen et al. | 4A Applications II | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "on GPUs" in title; OpenACC GPU FE assembly |
| 4 | Automating GPU Scalability for Complex Scientific Models: Phonon Boltzmann Transport Equation | Eric Heisler et al. | 4A Applications II | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU Scalability" in title; code-generation/scaling for GPU |
| 5 | DRUTO: Upper-Bounding Silent Data Corruption Vulnerability in GPU Applications | Md Hasanur Rahman et al. | 5B Resilience | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU Applications" in title; GPU reliability / SDC vulnerability — GPU *mechanism* (reliability) contribution |
| 6 | DEFCON: Deformable Convolutions Leveraging Interval Search and GPU Texture Hardware | Malith Jayaweera et al. | 6A Accelerators | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU Texture Hardware" in title; repurposes a fixed-function GPU unit — GPU mechanism contribution |
| 7 | Benchmarking and Dissecting the Nvidia Hopper GPU Architecture | Weile Luo, Ruibo Fan, Zeyu Li, Dayou Du, Qiang Wang, Xiaowen Chu | 6A Accelerators | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (see §6) | NOT_SEARCHED (see §6) | "Nvidia Hopper GPU Architecture" in title; microarchitectural characterisation — core GPU mechanism paper |
| 8 | cuKE: An Efficient Code Generator for Score Function Computation in Knowledge Graph Embedding | Lihan Hu, Jing Li, Peng Jiang | 8A Graph and MoE Learning | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | `TITLE_ONLY`: the `cu` prefix is the CUDA library-naming convention; GPU code generator (compiler mechanism) |
| 9 | GCSM: GPU-Accelerated Continuous Subgraph Matching for Large Graphs | Yihua Wei, Peng Jiang | 9B Graph Algorithms | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "GPU-Accelerated" in title |
| 10 | A Comparative Study of Intersection-Based Triangle Counting Algorithms on GPUs | Jiangbo Li, Zichen Xu, Minh Pham, Yicheng Tu, Qihe Zhou | 9B Graph Algorithms | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | "on GPUs" in title |
| 11 | Comparative Study of Large Language Model Architectures on Frontier | Junqi Yin, Avishek Bose, Guojing Cong, Isaac Lyngaas, Quentin Anthony | 5A Performance | UNKNOWN | https://www.ipdps.org/ipdps2024/2024-advance-program.html | NOT_SEARCHED (deprioritised) | NOT_SEARCHED (deprioritised) | `TITLE_ONLY`: Frontier is an AMD Instinct MI250X GPU system (public fact); an LLM-architecture performance study on it is necessarily GPU-resident |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| CloverLeaf on Intel Multi-Core CPUs: A Case Study in Write-Allocate Evasion | `memory` keyword; explicitly Intel multi-core **CPU** memory behaviour |
| ARGO: An Auto-Tuning Runtime System for Scalable GNN Training on Multi-Core Processor | `kernel`/`memory` keywords; explicitly **multi-core CPU** |
| Accelerating Lossy and Lossless Compression on Emerging BlueField DPU Architectures | `compression` keyword; the accelerator is a **BlueField DPU**, not a GPU |
| AMST: Accelerating Large-Scale Graph Minimum Spanning Tree Computation on FPGA | `kernel` keyword; target is an **FPGA** |
| IPU-EpiDet: Identifying Gene Interactions on Massively Parallel Graph-Based AI Accelerators | accelerator keyword; target is the **Graphcore IPU** |
| Harmonica: Hybrid Accelerator to Overcome Imperfections of Mixed-signal DNN Accelerators | accelerator keyword; **mixed-signal/analog DNN accelerator**, not GPU |
| Exploration of Trade-offs Between General-Purpose and Specialized Processing Elements in HPC-Oriented CGRA | accelerator keyword; target is a **CGRA** |
| Aurora: A Versatile and Flexible Accelerator for Generic Graph Neural Networks | accelerator keyword; a **custom ASIC/accelerator** design, not GPU |
| VNEC: A Vectorized Non-Empty Column Format for SpMV on CPUs | `sparse`/`SpMV` keywords; explicitly **CPUs** |
| OpenFFT-SME: An Efficient Outer Product Pattern FFT Library on ARM SME CPUs | `kernel` keyword; **ARM SME CPU** |
| Optimizing General Matrix Multiplications on Modern Multi-core DSPs | `kernel` keyword; **DSP** target |
| Harnessing Deep Learning and HPC Kernels via High-Level Loop and Tensor Abstractions on CPU Architectures | `kernel`/`compiler` keywords; explicitly **CPU architectures** |
| Machine-Learning-Driven Runtime Optimization of BLAS Level 3 on Modern Multi-Core Systems | `kernel` keyword; **multi-core CPU** |
| CachedArrays: Optimizing Data Movement for Heterogeneous Memory Systems | `memory`/`prefetch` keywords; heterogeneous **host memory** (DRAM/NVM) tiering, no GPU in title |
| Practically Tackling Memory Bottlenecks of Graph-Processing Workloads | `memory` keyword; **CPU cache/memory-hierarchy** study |
| Attention, Distillation, and Tabularization: Towards Practical Neural Network-Based Prefetching | `prefetch` keyword; **CPU hardware prefetcher** |
| TEEMO: Temperature Aware Energy Efficient Multi-Retention STT-RAM Cache Architecture | `memory`/`power` keywords; **STT-RAM CPU cache** |
| HINT: Designing Cache-Efficient MPI_Alltoall using Hybrid Memory Copy Ordering and Non-Temporal Instructions | `collective`/`memory` keywords; **CPU-side** non-temporal memcpy for MPI |
| The Self-adaptive and Topology-aware MPI_Bcast leveraging Collective offload on Tianhe Express Interconnect | `collective` keyword; **NIC-side collective offload** on Tianhe, no GPU |
| An Optimized Error-controlled MPI Collective Framework Integrated with Lossy Compression | `collective`/`compression` keywords; framework is presented as an MPI-collective + compression co-design — **GPU residency not establishable without the abstract** (see §6) |
| CliZ: Optimizing Lossy Compression for Climate Datasets with Adaptive Fine-tuned Data Prediction | `compression` keyword; scientific-data compressor, no GPU term |
| Accelerating Sparse Linear Solvers / Fast multiplication of random dense matrices with sparse matrices | `sparse` keyword; distributed/CPU numerical linear algebra |
| Adaptive Prefetching for Fine-grain Communication in PGAS Programs | `prefetch` keyword; **PGAS/CPU** communication |
| HA-CSD: Host and SSD Coordinated Compression for Capacity and Performance | `compression` keyword; **SSD/computational storage** |
| Enabling High-Performance Physical Based Rendering on New Sunway Supercomputer | rendering; target is the **Sunway** many-core CPU, not a GPU |
| SWEEP: Adaptive Task Scheduling for Exploring Energy Performance Trade-offs | `power` keyword; CPU task scheduling |
| SYNPA: SMT Performance Analysis and Allocation of Threads to Cores in ARM Processors | `warp`-adjacent SMT keyword; **ARM CPU SMT** |
| MPI Errors Detection using GNN Embedding and Vector Embedding over LLVM IR | `compiler` keyword; static MPI error detection, no GPU |
| Automatic Task Parallelization of Dataflow Graphs in ML/DL Models | `compiler` keyword; graph-level parallelisation, no GPU term |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| cuKE: An Efficient Code Generator for Score Function Computation in Knowledge Graph Embedding | The `cu` name prefix is the CUDA library convention; a score-function code generator of this kind targets CUDA kernels. `TITLE_ONLY` — abstract not reachable (IEEE Xplore blocked) |
| Comparative Study of Large Language Model Architectures on Frontier | Frontier is an AMD Instinct MI250X GPU supercomputer (public fact); the whole study therefore runs on GPUs. `TITLE_ONLY` |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| Benchmarking and Dissecting the NVIDIA Hopper GPU Architecture | `TITLE_CORRECTED_TO:` **Benchmarking and Dissecting the Nvidia Hopper GPU Architecture** (official advance program spells the vendor "Nvidia", not "NVIDIA"). CONFIRMED_IN_POPULATION — Session 6A Accelerators |
| Optimized GPU Implementation of Grid Refinement in Lattice Boltzmann Method | CONFIRMED_IN_POPULATION — Session 4A Applications II, verbatim title match |

## 6. Unresolved / blocked items

- **Per-paper DOIs: UNKNOWN for all 88 papers.** Blocked sources: `ieeexplore.ieee.org` → HTTP 418; `dblp.org` and `dblp.uni-trier.de` and `dblp.dagstuhl.de` → robots-disallowed; `dl.acm.org` → 403; `web.archive.org` → site blocked.
- **Abstracts: not reachable for any 2024 paper.** The official advance program carries titles + authors only; the abstract host is IEEE Xplore (blocked). STEP B is therefore title-and-author based; all such judgments are tagged `TITLE_ONLY`.
- **Titles that plausibly are GPU-resident but could not be confirmed without an abstract** (recommended for a follow-up abstract pass; NOT counted as candidates here): *Exploiting Inter-Layer Expert Affinity for Accelerating Mixture-of-Experts Model Inference* (OSU NOWLAB MoE/MPI work); *An Optimized Error-controlled MPI Collective Framework Integrated with Lossy Compression*; *QSync: Quantization-Minimized Synchronous Distributed Training Across Hybrid Devices*; *Hadar: Heterogeneity-Aware Optimization-Based Online Scheduling for Deep Learning Clusters*; *TASER: Temporal Adaptive Sampling for Fast and Accurate Dynamic Graph Representation Learning*; *PckGNN: Optimizing Aggregation Operators with Packing Strategies in Graph Neural Networks*; *Performance-Portable Multiphase Flow Solutions with Discontinuous Galerkin Methods*; *Predicting Cross-Architecture Performance of Parallel Programs*; *Picasso: Memory-Efficient Graph Coloring Using Palettes With Applications in Quantum Computing*; *Scalable and Differentiable Simulator for Quantum Computational Chemistry*; *Optimizing and Scaling the 3D Reconstruction of Single-Particle Imaging*; *Cross-System Analysis of Job Characterization and Scheduling in Large-Scale Computing Clusters*.
- **Official submission total: not published on any official IPDPS 2024 page.** Third-party aggregators (openaccept.org, csconfstats) both report 337 submissions.
- **PhD Forum item count: UNKNOWN** (the official report describes the PhD Forum but gives no number).

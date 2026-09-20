# MICRO 2024 (MICRO-57) — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **113** |
| counted items excluded from population | Session 8C "SRC Competition Presentations" (listed as TBA, 0 paper titles); workshops & tutorials (Sat/Sun, separate program); 2 keynotes (Moinuddin Qureshi; Gilles Pokam); PhD Forum lightning session + its posters; SRC two rounds of presentations; nine numbered poster sessions (I–IX); welcome reception / award luncheon / banquet |
| population source (primary) | https://microarch.org/micro57/program/ — `official-program` (full session-by-session listing, sessions 1A–11C, with authors) |
| population source (corroborating) | https://microarch.org/micro57/program/index.php (same official program, session-ID enumeration re-fetched to confirm no session was dropped); per-paper corroboration via IEEE Xplore / ACM DL DOI records (`publisher-proceedings`) for the 20 screened candidates |
| source class | `official-program` |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | MICRO-57 does not separate an industry track in its program: industry papers (e.g. "SOPHGO BM1684X …", "SambaNova SN40L …") appear inside ordinary main-program sessions (10A, 9C) and are therefore counted in the population. The only non-research slot inside the numbered session grid is 8C (SRC Competition Presentations), which lists no papers and is excluded. Posters, PhD Forum and SRC posters are listed separately and excluded. |

### 1.1 Population evidence notes

- Enumerated 33 numbered sessions: 1A–1C, 2A–2C, 3A–3C, 4A–4C, 5A–5C, 6A–6C, 7A–7C, 8A–8C, 9A–9C, 10A–10C, 11A–11C. A second targeted fetch was used to confirm the session-ID list and to re-read 8A/8B/9A/9B/9C verbatim (the first pass had an ambiguous count in 9A; it is 3 papers: Terminus, SOFA, RAHP).
- Per-day research-paper counts from the official program: Day 1 (Mon 4 Nov) = 45; Day 2 (Tue 5 Nov) = 45; Day 3 (Wed 6 Nov) = 23. Total = **113**.
- Session 8C exists in the grid but its content is "TBA" = SRC Competition Presentations → 0 research papers, excluded.
- **No officially stated accepted-paper count was found.** microarch.org/news/ carries no MICRO-57 acceptance statistics, and dblp.org (robots-disallowed) / dl.acm.org (403) could not be fetched for an independent total. The count 113 is therefore an EXACT enumeration of the official program, **not** a figure restated from an official statistic. Status: `UNKNOWN` for any officially published accepted-paper total.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population, not over the
seed list. Keyword hits were used only to order review, never to decide
relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | HyFiSS: A Hybrid Fidelity Stall-Aware Simulator for GPGPUs | Jianchao Yang et al. | 2A Simulation | 10.1109/MICRO61859.2024.00022 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00022 | NOT_FOUND_AFTER_SEARCH (no arXiv; IEEE/ACM paywalled) | https://github.com/ConvolutedDog/HyFiSS | GPGPU performance simulator; warp-level stall modelling is the entire contribution |
| 2 | vTrain: A Simulation Framework for Evaluating Cost-Effective and Compute-Optimal Large Language Model Training | Jehyeon Bang et al. | 2A Simulation | UNKNOWN | https://ieeexplore.ieee.org/document/10764533/ | https://arxiv.org/abs/2312.12391 | NOT_FOUND_AFTER_SEARCH | Profiling-driven simulator for multi-GPU LLM training; GPU-cluster/kernel-level modelling is central (GPU term absent from title → see §4) |
| 3 | Unleashing CPU Potential for Executing GPU Programs Through Compiler/Runtime Optimizations | Ruobing Han, Jisheng Zhao, Hyesoon Kim | 2B Compiler Techniques/Optimizations | UNKNOWN | https://ieeexplore.ieee.org/document/10764678/ | https://par.nsf.gov/servlets/purl/10576251 | https://github.com/cupbop/CuPBoP | Compiles/runs unmodified CUDA (SIMT) programs on CPUs; the GPU execution model is the object of study |
| 4 | A Case for Speculative Address Translation with Rapid Validation for GPUs | Junhyeok Park et al. | 3A GPU Microarchitecture I | 10.1109/MICRO61859.2024.00029 | https://dl.acm.org/doi/abs/10.1109/MICRO61859.2024.00029 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU address translation / TLB + page-walk speculation |
| 5 | SUV: Static Analysis Guided Unified Virtual Memory | Pratheek B, Guilherme Cox, Jan Vesely, Arkaprava Basu | 3A GPU Microarchitecture I | UNKNOWN | https://ieeexplore.ieee.org/document/10764479/ | https://www.csa.iisc.ac.in/~arkapravab/papers/MICRO24_SUV.pdf | NOT_FOUND_AFTER_SEARCH | GPU Unified Virtual Memory (UVM) page-fault/migration management driven by static analysis |
| 6 | STAR: Sub-Entry Sharing-Aware TLB for Multi-Instance GPU | Bingyao Li et al. | 3A GPU Microarchitecture I | 10.1109/MICRO61859.2024.00031 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00031 | https://users.elis.ugent.be/~leeckhou/papers/MICRO2024-STAR.pdf (also https://par.nsf.gov/servlets/purl/10580567) | NOT_FOUND_AFTER_SEARCH | GPU TLB redesign for NVIDIA MIG multi-instance partitioning |
| 7 | CacheCraft: Enhancing GPU Performance under Memory Protection through Reconstructed Caching | Soyoung Park et al. | 3A GPU Microarchitecture I | 10.1109/MICRO61859.2024.00032 | https://dl.acm.org/doi/abs/10.1109/MICRO61859.2024.00032 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU cache hierarchy restructuring under ECC/memory protection |
| 8 | A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs | Zhuoran Ji et al. | 3B Security: Accelerators and Cryptography | UNKNOWN | https://ieeexplore.ieee.org/document/10764432/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU kernel/compiler optimization of big-integer multiply; CUDA-level scheduling is the mechanism |
| 9 | Atomic Cache: Enabling Efficient Fine-Grained Synchronization with Relaxed Memory Consistency on GPGPUs Through In-Cache Atomic Operations | Yicong Zhang et al. | 5A GPU Synchronization/Concurrency | UNKNOWN | https://ieeexplore.ieee.org/document/10764542/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPGPU cache-resident atomics and GPU memory-consistency model |
| 10 | Concurrency-Aware Register Stacks for Efficient GPU Function Calls | Ni Kang, Mengchi Zhang, Ahmad Alawneh, Timothy G. Rogers | 5A GPU Synchronization/Concurrency | UNKNOWN | https://ieeexplore.ieee.org/document/10764484/ | https://engineering.purdue.edu/tgrogers/publication/kang-micro-2024/kang-micro-2024.pdf (also https://par.nsf.gov/servlets/purl/10591701) | NOT_FOUND_AFTER_SEARCH | GPU register file / warp occupancy mechanism for function calls |
| 11 | CPElide: Efficient Multi-Chiplet GPU Implicit Synchronization | Preyesh Dalmia, Rajesh Shashi Kumar, Matt Sinclair | 5A GPU Synchronization/Concurrency | 10.1109/MICRO61859.2024.00058 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00058 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Multi-chiplet GPU kernel-boundary synchronization elision |
| 12 | Over-Synchronization in GPU Programs | Ajay Nayak, Arkaprava Basu | 5C Debugging Correctness/Performance | UNKNOWN | https://ieeexplore.ieee.org/document/10764471/ | https://www.csa.iisc.ac.in/~arkapravab/papers/MICRO24_ScopeAdvice.pdf | NOT_FOUND_AFTER_SEARCH | GPU memory-scope / synchronization-scope analysis tool for CUDA programs |
| 13 | Uncovering Real GPU NoC Characteristics: Implications on Interconnect Architecture | Zhixian Jin et al. | 6B Networks-on-Chip | 10.1109/MICRO61859.2024.00070 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00070 | https://people.ece.ubc.ca/aamodt/publications/papers/realgpu-noc.micro2024.pdf | NOT_FOUND_AFTER_SEARCH | Reverse-engineering of real NVIDIA GPU on-chip interconnect |
| 14 | ThreadFuser: A SIMT Analysis Framework for MIMD Programs | Ahmad Alawneh, Ni Kang, Mahmoud Khairy, Timothy G. Rogers | 7B GPU Microarchitecture II | UNKNOWN | https://ieeexplore.ieee.org/document/10764650/ | https://engineering.purdue.edu/tgrogers/publication/alawneh-micro-2024/alawneh-micro-2024.pdf | NOT_FOUND_AFTER_SEARCH | SIMT execution-model analysis (warp formation/divergence) applied to MIMD code |
| 15 | Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration | Aaron Barnes, Fangjia Shen, Timothy G. Rogers | 7B GPU Microarchitecture II | UNKNOWN | https://ieeexplore.ieee.org/document/10764676/ | https://engineering.purdue.edu/tgrogers/publication/barnes-micro-2024/barnes-micro-2024.pdf | https://github.com/purdue-aalp/rayflex | GPU ray-tracing unit (RT core) datapath extension |
| 16 | Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs | Dongho Ha et al. | 7B GPU Microarchitecture II | UNKNOWN | https://ieeexplore.ieee.org/document/10764639/ | https://people.ece.ubc.ca/aamodt/publications/papers/tta.micro2024.pdf (also https://intra.engr.ucr.edu/~htseng/files/2024MICRO-TTA.pdf) | https://zenodo.org/doi/10.5281/zenodo.13294690 | Generalizes GPU RT-core BVH traversal hardware to other tree traversals |
| 17 | LIBRA: Memory Bandwidth- and Locality-Aware Parallel Tile Rendering | Aurora Tomás, Juan Luis Aragón, Joan-Manuel Parcerisa, Antonio González | 7B GPU Microarchitecture II | 10.1109/MICRO61859.2024.00081 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00081 | https://upcommons.upc.edu/bitstream/handle/2117/426555/LIBRA_MICRO_2024_camera_ready.pdf?sequence=3 | NOT_FOUND_AFTER_SEARCH | Tile-Based Rendering mobile-GPU architecture (paper text: "the predominant architecture in mobile GPUs"); GPU term absent from title → see §4 |
| 18 | Ghost Arbitration: Mitigating Interconnect Side-Channel Timing Attacks in GPU | Zhixian Jin et al. | 8A Side-Channel Attacks/Defenses | UNKNOWN | https://ieeexplore.ieee.org/document/10764592/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU interconnect arbitration side-channel defence. NOTE: official IEEE title ends "… in GPU"; the program page prints it without that suffix → see §4 |
| 19 | Veiled Pathways: Investigating Covert and Side Channels Within GPU Uncore | Yuanqing Miao et al. | 8A Side-Channel Attacks/Defenses | 10.1109/MICRO61859.2024.00088 | https://dl.acm.org/doi/10.1109/MICRO61859.2024.00088 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Covert/side channels in GPU uncore (L2, interconnect, memory controller) |
| 20 | Pushing the Performance Envelope of DNN-based Recommendation Systems Inference on GPUs | Rishabh Jain et al. | 8B Dataflow & Recommendation Systems | UNKNOWN | https://ieeexplore.ieee.org/document/10764622/ | https://arxiv.org/abs/2410.22249 | NOT_FOUND_AFTER_SEARCH | GPU embedding-kernel / memory-hierarchy bottleneck analysis and optimization |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| Hardware-Assisted Virtualization of Neural Processing Units for Cloud Platforms | NPU (not GPU) virtualization; MIG-like partitioning but on an NPU substrate |
| Elastic Translations: Fast virtual memory with multiple translation sizes | CPU virtual memory / TLB; no GPU |
| Distributed Page Table: Harnessing Physical Memory as an Unbounded Hashed Page Table | CPU page-table structure; "page walk" keyword only |
| Secure Prefetching for Secure Cache Systems | CPU prefetcher security |
| Customizing Cache Indexing Through Entropy Estimation | CPU last-level cache indexing |
| Scalar Vector Runahead | CPU prefetch/runahead |
| Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache | DRAM cache in CPU memory hierarchy |
| Memory Allocation under Hardware Compression | CPU memory compression |
| A Mess of Memory System Benchmarking, Simulation and Application Profiling | CPU/DRAM memory-system benchmarking; "profiling" keyword only |
| SRender: Boosting Neural Radiance Field Efficiency via Sensitivity-Aware Dynamic Precision Rendering | Fixed-function NeRF accelerator; "rendering" keyword, not a GPU |
| Fusion-3D: Integrated Acceleration for Instant 3D Reconstruction and Real-Time Rendering | Dedicated 3D-reconstruction/rendering ASIC, not a GPU |
| GauSPU: 3D Gaussian Splatting Processor for Real-Time SLAM Systems | Standalone 3DGS processor; not a GPU architecture |
| Blenda: Dynamically-Reconfigurable Stacked DRAM | Stacked-DRAM/HBM keyword; DRAM organization, no GPU |
| LUCIE: A Universal Chiplet-Interposer Design Framework for Plug-and-Play Integration | "chiplet" keyword; general interposer design framework |
| SCAR: Scheduling Multi-Model AI Workloads on Heterogeneous Multi-Chiplet Module Accelerators | "chiplet" keyword; NPU/accelerator chiplets, not GPUs |
| Looking into the Black Box: Monitoring Computer Architecture Simulations in Real-Time with AkitaRTM | Implemented on MGPUSim, but the abstract frames it as a general architecture-simulator monitoring tool ("not constrained to MGPUSim"); no GPU-specific mechanism is the contribution |
| TACOS: Topology-Aware Collective Algorithm Synthesizer for Distributed Machine Learning | Collective-communication synthesis for accelerator networks; no GPU mechanism |
| Ring Road: A Scalable Polar-Coordinate-based 2D Network-on-Chip Architecture | Generic NoC topology |
| Sparsepipe: Sparse Inter-operator Dataflow Architecture with Cross-Iteration Reuse | "sparse" keyword; dataflow accelerator, not GPU |
| FlashLLM: A Chiplet-Based In-Flash Computing Architecture to Enable On-Device Inference of 70B LLM | "chiplet" keyword; in-flash computing |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| LIBRA: Memory Bandwidth- and Locality-Aware Parallel Tile Rendering | Paper text: "The increasing demand for high-quality graphics requires a significant increase in computational power of modern GPUs… particularly challenging in Tile-Based Rendering (TBR) GPUs, the predominant architecture in mobile GPUs"; evaluated on an ARM Valhall-like mobile GPU |
| ThreadFuser: A SIMT Analysis Framework for MIMD Programs | "SIMT" in the title is the GPU execution model; the framework studies warp formation for GPU-style execution of MIMD code |
| Ghost Arbitration: Mitigating Interconnect Side-Channel Timing Attacks | Official IEEE Xplore title is "… Timing Attacks in GPU"; the attack surface is the GPU interconnect arbiter. The program page's rendering omits "in GPU" |
| vTrain: A Simulation Framework for Evaluating Cost-Effective and Compute-Optimal Large Language Model Training | Profiling-driven simulation of LLM training on multi-GPU clusters; per-GPU kernel timing + inter-GPU parallelization strategy is the modelled mechanism |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| SUV: Static Analysis Guided Unified Virtual Memory | `CONFIRMED_IN_POPULATION` (Session 3A GPU Microarchitecture I). Program page prints "SUV: Static analysis guided Unified Virtual Memory"; IEEE/Semantic Scholar record capitalizes as "Static Analysis Guided". `TITLE_CORRECTED_TO: SUV: Static Analysis Guided Unified Virtual Memory` |
| STAR: Sub-Entry Sharing-Aware TLB for Multi-Instance GPU | `CONFIRMED_IN_POPULATION` (Session 3A) |
| (seed instruction) re-review all MICRO 2024 GPU microarchitecture sessions | Done. Sessions 3A (GPU Microarchitecture I), 5A (GPU Synchronization/Concurrency), 7B (GPU Microarchitecture II) fully enumerated, plus GPU papers found outside those sessions in 2A, 2B, 3B, 5C, 6B, 8A, 8B. 18 candidates beyond the 2 seeds — see §2 |

## 6. Unresolved / blocked items

- No officially published accepted-paper total for MICRO-57 was found; `UNKNOWN`. Population count 113 is an exact enumeration of the official program only.
- dblp.org is robots-disallowed for fetching and dl.acm.org returns 403, so an independent bibliographic-index total could not be obtained.
- ACM/IEEE DOIs for candidates 2, 3, 5, 8, 9, 10, 12, 14, 15, 16, 18, 20 were not surfaced as literal `10.1109/…` strings by search; IEEE Xplore document URLs are recorded instead rather than guessing DOI suffixes. Marked `UNKNOWN`.
- Artifact/code URLs marked `NOT_FOUND_AFTER_SEARCH` were not located; MICRO-57 has no single public artifact index reachable from here.

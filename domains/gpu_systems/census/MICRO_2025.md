# MICRO 2025 (MICRO-58) — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **123** |
| counted items excluded from population | Session 3D "SRC Forum" (Session Chair: SRC Org.; **no papers listed** — 0 items); workshops & tutorials (Sat–Sun 18–19 Oct, separate program); SRC Poster Session; welcome reception; 2 keynotes (Luis Ceze, NVIDIA/UW; Onur Mutlu, ETH Zürich) |
| population source (primary) | https://microarch.org/micro58/program/ — `official-program` (full main program grouped by session, sessions 1A–9C, with full author lists) |
| population source (corroborating) | Second targeted fetch of the same official program to enumerate all session IDs and to read Session 3D verbatim; per-paper corroboration via ACM DL DOI records (`publisher-proceedings`, proceedings DOI 10.1145/3725843) for the 12 screened candidates |
| source class | `official-program` |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | MICRO-58 does not separate an industry track in its program grid: industry papers (e.g. "OASIS: A Commercial High Performance Terminal AI Processor…", Session 7A) sit inside ordinary main-program sessions and are counted. Best Paper Awards / Best Paper Candidates are annotations on regular papers, not a separate type. 3D (SRC Forum) is the only non-research slot inside the numbered grid and is excluded. |

### 1.1 Population evidence notes

- **Session-completeness cross-check performed as instructed.** A first fetch of the program returned sessions 1A,1B,1C,1D,2A–2D,3A,3B,3C,4A–4D,5A–5D,6A–6D,7A–7D,8A,8B,8C,9A,9B,9C — i.e. it **dropped 3D**. A second targeted fetch confirmed the page's full session-ID list is: 1A, 1B, 1C, 1D, 2A, 2B, 2C, 2D, 3A, 3B, 3C, **3D**, 4A, 4B, 4C, 4D, 5A, 5B, 5C, 5D, 6A, 6B, 6C, 6D, 7A, 7B, 7C, 7D, 8A, 8B, 8C, 9A, 9B, 9C (34 slots), and that **3D is "SRC Forum" with no papers listed**. It also confirmed there is no Session 8D or 9D — the grid ends at 9C. The dropped session therefore contributes 0 research papers and the enumeration is complete.
- Per-session research-paper counts from the official program: 1A 3, 1B 3, 1C 3, 1D 3; 2A 4, 2B 4, 2C 4, 2D 4; 3A 4, 3B 4, 3C 4, 3D 0; 4A 4, 4B 3, 4C 4, 4D 4; 5A 3, 5B 3, 5C 3, 5D 3; 6A 3, 6B 4, 6C 4, 6D 4; 7A 5, 7B 5, 7C 5, 7D 5; 8A 3, 8B 3, 8C 3; 9A 4, 9B 4, 9C 4. Total = **123**.
- **Reconciliation against an officially stated accepted count: not possible.** microarch.org/news/ contains no MICRO-58 acceptance statistics; no official submission/acceptance figure was found by search. dblp.org is robots-disallowed and dl.acm.org returns 403, so the ACM proceedings table-of-contents count could not be read independently. Officially stated accepted-paper total: `UNKNOWN`. The figure 123 is an EXACT enumeration of the official program and matches the expected order of magnitude given in the task brief ("about 123 titles").

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population, not over the
seed list. Keyword hits were used only to order review, never to decide
relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Coruscant: Co-Designing GPU Kernel and Sparse Tensor Core to Advocate Unstructured Sparsity in Efficient LLM Inference | Donghyeon Joo, Helya Hosseini, Ramyad Hadidi, Bahar Asgari | 2A Systems for AI (LLMs) - 2 | 10.1145/3725843.3756065 | https://dl.acm.org/doi/full/10.1145/3725843.3756065 | https://dl.acm.org/doi/full/10.1145/3725843.3756065 (ACM DL renders a `/doi/full/` HTML view; arXiv preprint NOT_FOUND_AFTER_SEARCH) | https://github.com/dhjoo98/coruscant | GPU kernel + Sparse Tensor Core co-design |
| 2 | RayN: Ray Tracing Acceleration with Near-memory Computing | Mohammadreza Saed, Prashant J. Nair, Tor M. Aamodt | 2B Processing-In-Memory - 2 | 10.1145/3725843.3756067 | https://dl.acm.org/doi/10.1145/3725843.3756067 | NOT_FOUND_AFTER_SEARCH (no arXiv) | https://zenodo.org/records/16734933 | Offloads BVH traversal from the GPU to HBM logic dies; baseline and top-level traversal are GPU ray tracing (~1.8x geomean over baseline GPU ray tracing). GPU term absent from title → see §4 |
| 3 | Dissecting and Modeling the Architecture of Modern GPU Cores | Rodrigo Huerta, Mojtaba Abaie Shoushtary, José-Lorenzo Cruz, Antonio Gonzalez | 2D GPU - 1 | 10.1145/3725843.3756041 | https://dl.acm.org/doi/full/10.1145/3725843.3756041 | https://arxiv.org/pdf/2501.12084v2 | https://github.com/upc-arco/modern-gpu-simulator-micro-2025 | Reverse-engineers and models the GPU SM/core pipeline (issue, register file, warp scheduling) |
| 4 | Interleaved Bitstream Execution for Multi-Pattern Regex Matching on GPUs | Tianao Ge, Xiaowen Chu, Hongyuan Liu | 2D GPU - 1 | 10.1145/3725843.3756052 | https://dl.acm.org/doi/10.1145/3725843.3756052 | NOT_FOUND_AFTER_SEARCH (no arXiv) | https://github.com/getianao/BitGen ; https://zenodo.org/records/16664499 | GPU kernel/warp-level bit-parallel regex execution |
| 5 | SoftWalker: Supporting Software Page Table Walk for Irregular GPU Applications | Sungbin Jang, Junhyeok Park, Yongho Lee, Osang Kwon, Donghyun Kim, Juyoung Seok, Seokin Hong | 2D GPU - 1 | 10.1145/3725843.3756056 | https://dl.acm.org/doi/10.1145/3725843.3756056 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU page-table walk moved to software/warp execution; GPU MMU/TLB mechanism |
| 6 | LATPC: Accelerating GPU Address Translation Using Locality-Aware TLB Prefetching and MSHR Compression | Yeonan Ha, Jiho Park, Hanna Cha, Jiwon Lee, Joonsung Kim, Won Woo Ro, Youngsok Kim | 2D GPU - 1 | 10.1145/3725843.3756069 | https://dl.acm.org/doi/full/10.1145/3725843.3756069 | https://dl.acm.org/doi/full/10.1145/3725843.3756069 (ACM `/doi/full/` view) | NOT_FOUND_AFTER_SEARCH | GPU TLB prefetching + MSHR compression for address translation |
| 7 | ORCHES: Orchestrated Test-Time-Computation-based LLM Reasoning on Collaborative GPU-PIM HEterogeneous System | Sixu Li et al. | 3A Systems for AI (Emerging Applications) | 10.1145/3725843.3756039 | https://dl.acm.org/doi/10.1145/3725843.3756039 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPU–PIM heterogeneous system; GPU is one of the two compute substrates being orchestrated. NOTE: ACM DL renders the title as "…Test-Time-**Compute**-based…" whereas the program page prints "…Test-Time-**Computation**-based…" — discrepancy recorded, not resolved |
| 8 | Characterizing the Efficiency of Distributed Training: A Power, Performance, and Thermal Perspective | Seokjin Go et al. | 4A Systems for AI (Training) | 10.1145/3725843.3756111 | https://dl.acm.org/doi/10.1145/3725843.3756111 | https://arxiv.org/abs/2509.10371 | NOT_FOUND_AFTER_SEARCH | Measurement study of distributed training power/thermals on NVIDIA H100/H200 and AMD MI250 GPUs. GPU term absent from title → see §4 |
| 9 | C3ache: Towards Hierarchical Cache-Centric Computing for Sparse Matrix Multiplication on GPGPUs | Xiaojie Li, Mingyu Wang, Baiqing Zhong, Haiqiu Huang, Guangjie Cao, Zhiyi Yu | 6A GPUs - 2 | 10.1145/3725843.3756077 | https://dl.acm.org/doi/10.1145/3725843.3756077 | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | GPGPU cache-hierarchy near-cache computing for SpMM |
| 10 | Leveraging Chiplet-Locality for Efficient Memory Mapping in Multi-Chip Module GPUs | Junhyeok Park, Sungbin Jang, Osang Kwon, Yongho Lee, Seokin Hong | 6A GPUs - 2 | 10.1145/3725843.3756090 | https://dl.acm.org/doi/10.1145/3725843.3756090 | NOT_FOUND_AFTER_SEARCH (summary coverage: https://semiengineering.com/utilizing-chiplet-locality-for-efficient-memory-mapping-in-mcm-gpus-etri-sungkyunkwan-univ/) | NOT_FOUND_AFTER_SEARCH | MCM/chiplet GPU memory address mapping and locality |
| 11 | Security and Performance Implications of GPU Cache Eviction Priority Hints | Qizhong Wang, Xiangyue Huang, Yanan Guo, Yuanchao Xu | 6A GPUs - 2 | 10.1145/3725843.3756116 | https://dl.acm.org/doi/10.1145/3725843.3756116 | https://dl.acm.org/doi/pdf/10.1145/3725843.3756116 (publisher PDF link surfaced by search; OA status unverified) | NOT_FOUND_AFTER_SEARCH | GPU L2 cache eviction-priority hint instructions: performance + side-channel implications |
| 12 | Swift and Trustworthy Large-Scale GPU Simulation with Fine-Grained Error Modeling and Hierarchical Clustering | Euijun Chung, Seonjin Na, Sung Ha Kang, Hyesoon Kim | 7B Tools and Simulators | 10.1145/3725843.3757107 | https://dl.acm.org/doi/10.1145/3725843.3757107 | https://seonjinna.github.io/assets/pdf/MICRO25_stem_root.pdf | NOT_FOUND_AFTER_SEARCH | GPU architecture simulation sampling/error modelling at kernel and warp granularity |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| SHADOW: Simultaneous Multi-Threading Architecture with Asymmetric Threads | Verified from the authors' PDF: CPU SMT core (compared against MorphCore, FIFOShelf); no warp/wavefront/SIMT mechanism, despite a GPU-architecture co-author |
| Chasoň: Supporting Cross HBM Channel Data Migration to Enable Efficient Sparse Algebraic Acceleration | "HBM"/"sparse" keywords; a sparse-algebra accelerator's HBM channels, not a GPU |
| Stratum: System-Hardware Co-design with Tiered Monolithic 3D-DRAM for Efficient MoE Serving | 3D-DRAM/PIM stack for MoE serving; memory-substrate paper |
| Delegato: Locality-Aware Atomic Memory Operations on Chiplets | "chiplet"/"atomic" keywords; CPU chiplet atomics |
| LEGOSim: A Unified Parallel Simulation Framework for Multi-chiplet Heterogeneous Integration | "chiplet" keyword; generic multi-chiplet simulator |
| PyTorchSim: A Comprehensive, Fast, and Accurate NPU Simulation Framework | NPU simulator, not GPU |
| Learning to Walk: Architecting Learned Virtual Memory Translation | "page walk"/"TLB" keywords; CPU/datacenter address translation |
| ReGate: Enabling Power Gating in Neural Processing Units | "power" keyword; NPU power gating |
| Symbiotic Task Scheduling and Data Prefetching / Software Prefetch Multicast / RICH Prefetcher (Session 1D) | "prefetch" keyword; CPU manycore prefetching |
| Micro-MAMA / Ghost Threading / Elevating Temporal Prefetching Through Instruction Correlation (Session 5B) | "prefetch" keyword; CPU prefetching |
| ρHammer: Reviving RowHammer Attacks on New Architectures via Prefetching | "prefetch" keyword; DRAM RowHammer |
| Drishti: … Last-Level Cache Replacement Policies for Many-Core Systems | "cache" keyword; CPU LLC |
| A TRRIP Down Memory Lane: … Re-Reference Interval Prediction For Instruction Caching | "cache" keyword; CPU instruction cache |
| SeaCache: Efficient and Adaptive Caching for Sparse Accelerators | "cache"/"sparse" keywords; sparse accelerator, not GPU |
| COSMOS: RL-Enhanced Locality-Aware Counter Cache Optimization for Secure Memory | "cache" keyword; secure-memory counter cache |
| HiPACK: Efficient Sub-8-Bit Direct Convolution with SIMD and Bitwise Management | "SIMD" keyword; CPU SIMD, not SIMT |
| Empowering Vector Architectures for ML: The CAMP Architecture for Matrix Multiplication | CPU vector architecture, not GPU |
| GCC (3DGS inference architecture) / RTGS / REACT3D | Dedicated 3D Gaussian Splatting accelerators; "rendering"-adjacent but not GPU architectures |
| StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs | Dataflow/FPGA accelerator |
| Pimba / ComPASS / PIM-CCA / 3D-PATH / HEAT / FALA / PolymorPIC | PIM/PNM/NDP substrates; no GPU mechanism |
| SuperMesh: Energy-Efficient Collective Communications for Accelerators | Accelerator interconnect collectives; no GPU mechanism |
| Chameleon: Adaptive Caching and Scheduling for Many-Adapter LLM Inference Environments | "cache" keyword; serving-system scheduling, GPU not the studied mechanism |
| Optimizing All-to-All Collective Communication with Fault Tolerance on Torus Networks | Network topology/collectives |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| RayN: Ray Tracing Acceleration with Near-memory Computing | Integrates BVH-traversal logic into HBM logic dies **within existing GPU architectures**; the GPU handles top-level BVH traversal, HBM logic dies the lower levels; speedup reported "compared to baseline GPU ray tracing" |
| Characterizing the Efficiency of Distributed Training: A Power, Performance, and Thermal Perspective | arXiv abstract/body characterizes distributed LLM training across NVIDIA H100/H200 and AMD MI250 GPUs (power, performance, thermal per-GPU) |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| Dissecting and Modeling the Architecture of Modern GPU Cores | `CONFIRMED_IN_POPULATION` (Session 2D GPU - 1) |
| SoftWalker | `CONFIRMED_IN_POPULATION` — `TITLE_CORRECTED_TO: SoftWalker: Supporting Software Page Table Walk for Irregular GPU Applications` (Session 2D) |
| LATPC | `CONFIRMED_IN_POPULATION` — `TITLE_CORRECTED_TO: LATPC: Accelerating GPU Address Translation Using Locality-Aware TLB Prefetching and MSHR Compression` (Session 2D) |
| C3ache | `CONFIRMED_IN_POPULATION` — `TITLE_CORRECTED_TO: C3ache: Towards Hierarchical Cache-Centric Computing for Sparse Matrix Multiplication on GPGPUs` (Session 6A) |
| Leveraging Chiplet-Locality for Efficient Memory Mapping in Multi-Chip Module GPUs | `CONFIRMED_IN_POPULATION` (Session 6A) |
| Security and Performance Implications of GPU Cache Eviction Priority Hints | `CONFIRMED_IN_POPULATION` (Session 6A) |
| Coruscant | `CONFIRMED_IN_POPULATION` — `TITLE_CORRECTED_TO: Coruscant: Co-Designing GPU Kernel and Sparse Tensor Core to Advocate Unstructured Sparsity in Efficient LLM Inference` (Session 2A) |

All 7 seeds are in the main population. Screening added 5 candidates the seed
list did not name: Interleaved Bitstream Execution (2D), RayN (2B), ORCHES (3A),
Characterizing the Efficiency of Distributed Training (4A), and Swift and
Trustworthy Large-Scale GPU Simulation (7B).

## 6. Unresolved / blocked items

- Officially stated accepted-paper total for MICRO-58: `UNKNOWN` (not published on microarch.org/news/; ACM DL ToC unreachable — 403; dblp robots-disallowed). 123 is an exact program enumeration.
- Public full text `NOT_FOUND_AFTER_SEARCH` for candidates 2, 4, 5, 7, 9, 10 — no arXiv preprint or author-hosted PDF surfaced. ACM `/doi/full/` and `/doi/pdf/` links are recorded where search surfaced them, but their open-access status could not be verified (dl.acm.org returns 403 from this environment).
- Artifact URLs `NOT_FOUND_AFTER_SEARCH` for candidates 5, 6, 8, 9, 10, 11, 12; no MICRO-58 artifact-evaluation index was reachable.

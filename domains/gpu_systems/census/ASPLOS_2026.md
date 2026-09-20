# ASPLOS 2026 (31st) — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

Reason for `PARTIAL_CENSUS`: STEP B screening coverage is effectively **complete** — every
paper of the 2026 population appears among the 168 verbatim titles enumerated from the
official program page — but the population *boundary* is not resolvable per paper: the
program page mixes the 152 31st-edition papers with the 16 deferred 30V3 papers and gives no
volume or DOI, and the page's own statistic ("167 unique papers") does not match the 168 rows
it lists. See §1.1 and §6.

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **152** (proceedings-year basis, 31st-edition Volumes 1–2) |
| counted items excluded from population | **3** non-paper records in 31V2 (135 raw items → 132 papers; individually `UNKNOWN`, presumed front matter/keynote abstracts by analogy with 29V3). Excluded and *not* counted: the **16** deferred 30V3 papers that are on the 2026 program but belong to the ASPLOS 2025 proceedings. Workshops/tutorials/posters/ACM SRC/AE reports publish outside these volumes; counts `UNKNOWN` |
| population source (primary) | `https://api.crossref.org/` date-windowed `prefix:10.1145` cursor sweep filtered on volume DOI stem — retained extracts `domains/hpc_quantum/corpus/quantum-hpc-survey/working-evidence/asplos/vols.txt` and `.../v2_2026.txt` (125 of 135 31V2 DOI suffixes with page ranges, titles absent) |
| population source (corroborating) | `https://www.asplos-conference.org/asplos2026/program/index.html` — official program, 36 sessions (1A–9D), **168 rows enumerated verbatim**, page statistic *"Presentations: 25 min \| 167 unique papers"*. Per-paper volume confirmed for 10 papers via publisher landing pages surfaced in search (4 in 31V1, 6 in 31V2) |
| source class | `publisher-proceedings` (count) + `official-program` (complete title enumeration, session placement) |
| enumeration completeness | count: `UNVERIFIED_TOTAL` (31V1 = 20 and 31V2 = 135 rest on the sweep's reported item count; the retained 31V2 list covers 125/135 and carries no titles). Title-level enumeration of the *program*: `EXACT` (168/168). Title-level enumeration of the *population*: `APPROXIMATE` — the 152 are a subset of those 168 but cannot be individually separated from the 16 30V3 items |
| paper-type mixing notes | Both 31st volumes are main-conference research papers; no short/industry split. **There is no ASPLOS 2026 Volume 3** — the 2026 CFP lists only two submission cycles, so 2026 has no deferred outgoing cycle |
| official acceptance statistic | *"167 unique papers"* (official 2026 program page, verbatim). This is a **program** statistic, not an acceptance rate, and it is 1 lower than the 168 rows the same page lists. No accept-rate sentence found |

### 1.1 Population evidence notes

**Multi-cycle / multi-volume structure.**

| Edition | Volume | DOI stem | ISBN | Pub. date | Raw items | Non-papers | **Regular papers** | Presented at |
|---|---|---|---|---|---|---|---|---|
| 31st | V1 | `10.1145/3760250` | 9798400721656 | 2025-12-11 | 20 | 0 | **20** | ASPLOS 2026 |
| 31st | V2 | `10.1145/3779212` | 9798400723599 | 2026-03-22 | 135 | 3 | **132** | ASPLOS 2026 |
| | | | | | 155 | 3 | **152** | |

**Volumes counted and why.** Volumes 1 and 2 of the 31st edition, and only those, because
the population definition is proceedings-year. The **16 papers of 30V3** (ASPLOS 2025
Volume 3, published 2025-08-06) are presented in the 2026 program under the fall-cycle
deferral rule but are ASPLOS 2025 proceedings; they are excluded here and counted in
`ASPLOS_2025.md`. One of them is identified: *PowerMove: Optimizing Compilation for Neutral
Atom Quantum Computers with Zoned Architecture* (Session 1C). The other 15 cannot be
identified from any reachable source.

**Arithmetic that does not close, stated rather than papered over.** 152 (31V1+V2) + 16
(30V3) = **168**, which matches the 168 rows enumerated from the program page — but the page
itself says *"167 unique papers"*. There are **no duplicate titles** among the 168 rows
(checked by exact and normalised comparison). So either the page's statistic is stale by one,
or one row is not a distinct paper, or one of the volume counts is off by one. **Unresolved.**
This census uses 152 as the population and does not reconcile the discrepancy by choosing.

**Trap recorded.** `10.1145/3818671.*` is the *18th Workshop on General Purpose Processing
Using GPU* (GPGPU), which shares ASPLOS 2026's 2026-03-22 publication date and is *not*
ASPLOS. It must not be swept into the population. (One retained 31V2 suffix, `3818675`, pages
`23-29`, sits in a neighbouring `3818xxx` range and should be re-checked before it is trusted
as an ASPLOS record.)

**Site-navigation finding.** `https://www.asplos-conference.org/asplos2026/program/index.html`,
`.../asplos2026/program/`, `.../asplos2025/program/` and `.../asplos2024/program/` **all serve
the 2026 program** (the site resolves `/program/` to the current edition). Only the 2026 URL
is correctly named.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 152 population papers are
within the 168 enumerated program titles), not over the seed list. Keyword hits were used
only to order review, never to decide relevance. `[title-only]` marks a judgment from the
official title alone.

| # | Title (official) | Authors (first + et al.) | Session / Volume | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | MSCCL++: Rethinking GPU Communication Abstractions for AI Inference | `UNKNOWN` (Microsoft Research) | 2C: GPU Systems & Scheduling / 31V2 | `10.1145/3779212.3790188` | https://doi.org/10.1145/3779212.3790188 | https://dl.acm.org/doi/pdf/10.1145/3779212.3790188 (open PDF on publisher) ; https://arxiv.org/abs/2504.09014 (preprint titled *"…for Cutting-Edge AI Applications"*) | https://github.com/microsoft/mscclpp | GPU-driven communication stack: device-side channels, GPU-initiated transfers, collective abstractions replacing NCCL-style host orchestration |
| 2 | Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums | `UNKNOWN` | 2C: GPU Systems & Scheduling / 31V2 | `10.1145/3779212.3790176` | https://doi.org/10.1145/3779212.3790176 | https://arxiv.org/abs/2510.17505 ; https://spice.cs.umd.edu/proceedings/5_Insum.pdf | `NOT_FOUND_AFTER_SEARCH` | Sparse GPU kernel generation via indirect einsum abstraction; GPU kernel/codegen mechanism |
| 3 | Asynchrony and GPUs: Bridging this Dichotomy for I/O with AGIO | `UNKNOWN` | 2C: GPU Systems & Scheduling / 31V2 | `10.1145/3779212.3790130` | https://doi.org/10.1145/3779212.3790130 | `NOT_FOUND_AFTER_SEARCH` | `NOT_FOUND_AFTER_SEARCH` | Asynchronous I/O mechanism for GPU kernels (GPUDirect/storage-path class); GPU execution model is the contribution |
| 4 | gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform | `UNKNOWN` (China Telecom Cloud Computing Research Institute + Temple) | 2C: GPU Systems & Scheduling / 31V2 | `10.1145/3779212.3790168` | https://doi.org/10.1145/3779212.3790168 | https://cis.temple.edu/~jiewu/research/publications/Publication_files/3779212.3790168.pdf | `NOT_FOUND_AFTER_SEARCH` | GPU spatial/temporal sharing and scheduling (MPS/MIG-class multi-tenancy) |
| 5 | GFS: A Preemption-aware Scheduling Framework for GPU Clusters with Predictive Spot Instance Management | `UNKNOWN` | 2C: GPU Systems & Scheduling / **31V1** | `10.1145/3760250.3762231` | https://doi.org/10.1145/3760250.3762231 | https://arxiv.org/abs/2509.11134 | `NOT_FOUND_AFTER_SEARCH` | GPU-cluster preemption/checkpoint scheduling on spot capacity |
| 6 | CHERI-SIMT: Implementing Capability Memory Protection in GPUs | Matthew Naylor et al. (from the Cambridge PDF title line) | 8A: GPU Programming / **31V1** | `10.1145/3760250.3762234` | https://doi.org/10.1145/3760250.3762234 | https://www.cl.cam.ac.uk/~tmj32/papers/docs/naylor26-asplos.pdf | https://github.com/CTSRD-CHERI/SIMTight `[same group's SIMT platform; not stated as the paper's artifact]` | CHERI capabilities inside a SIMT pipeline: per-lane capability registers, GPU memory protection microarchitecture |
| 7 | cuJSON: A Highly Parallel JSON Parser for GPUs | `UNKNOWN` (AutomataLab) | 8A: GPU Programming / **31V1** | `10.1145/3760250.3762222` | https://doi.org/10.1145/3760250.3762222 | `NOT_FOUND_AFTER_SEARCH` | https://github.com/AutomataLab/cuJSON | Data-parallel GPU parsing: warp-level tokenisation and structural-index construction |
| 8 | Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation | `UNKNOWN` (Yaoyao Ding lists it on their publications page) | 5A: Generative Model Serving / **31V1** | `10.1145/3760250.3762219` | https://doi.org/10.1145/3760250.3762219 | https://arxiv.org/abs/2504.12984 | https://zenodo.org/records/16756860 (artifact) ; https://github.com/NVIDIA/tilus | GPGPU programming language with explicit shared-memory and register control for sub-byte types; GPU compiler/execution mechanism |
| 9 | Triton-Sanitizer: A Fast and Device-Agnostic Memory Sanitizer for Triton with Rich Diagnostic Context | `UNKNOWN` (CAT Lab / Keren Zhou group) | 4A: ML Training & Monitoring / 31V2 | `10.1145/3779212.3790241` | https://doi.org/10.1145/3779212.3790241 | https://dl.acm.org/doi/pdf/10.1145/3779212.3790241 (open PDF on publisher) ; https://www.jokeren.tech/publication/wu-2026-triton-sanitizer/ | https://github.com/Deep-Learning-Profiling-Tools/triton-viz `[same group's Triton tooling; not stated as the paper's artifact]` | GPU memory-safety instrumentation for Triton kernels; GPU compiler/runtime mechanism |
| 10 | CLM: Removing the GPU Memory Barrier for 3D Gaussian Splatting | Hexu Zhao et al. (from the NYU PDF title line) | 3C: 3D Gaussian Splatting & Rendering / 31V2 | `10.1145/3779212.3790140` | https://doi.org/10.1145/3779212.3790140 | https://arxiv.org/pdf/2511.04951 ; https://cs.nyu.edu/~apanda/assets/papers/asplos26-cvm.pdf | https://github.com/nyu-systems/CLM-GS ; project page https://tarzanzhao.github.io/CLM-GS/ | GPU memory capacity wall removed via CPU offloading with GPU-side prefetch/scheduling |
| 11 | Bullet: Boosting GPU Utilization for LLM Serving via Dynamic Spatial-Temporal Orchestration | `UNKNOWN` | 1A: LLM Serving: Throughput Optimization / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU SM-level spatial/temporal co-location for prefill+decode `[title-only]` |
| 12 | TempGraph: An Efficient Chain-driven Temporal Graph Computing Framework on the GPU | `UNKNOWN` | 6C: Graph & Sparse Computing / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU graph traversal/kernel design for temporal graphs `[title-only]` |
| 13 | Lobster: A GPU-Accelerated Framework for Neurosymbolic Programming | `UNKNOWN` | 8A: GPU Programming / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel/compilation backend for neurosymbolic execution `[title-only]` |
| 14 | A Framework for Developing and Optimizing Fully Homomorphic Encryption Programs on GPUs | `UNKNOWN` | 7A: Fully Homomorphic Encryption / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel scheduling/codegen for FHE `[title-only]` |
| 15 | Maverick: Rethinking TFHE Bootstrapping on GPUs via Algorithm-Hardware Co-Design | `UNKNOWN` | 7A: Fully Homomorphic Encryption / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU-targeted TFHE bootstrapping co-design `[title-only]` |
| 16 | Cheddar: A Swift Fully Homomorphic Encryption Library Designed for GPU Architectures | `UNKNOWN` | 9A: Systems Profiling & Optimization / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel library design for FHE `[title-only]` |
| 17 | FlashMem: Supporting Modern DNN Workloads on Mobile with GPU Memory Hierarchy Optimizations | `UNKNOWN` | 5B: On-Device & Edge AI / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Mobile GPU memory-hierarchy mechanism `[title-only]` |
| 18 | GS-Scale: Unlocking Large-Scale 3D Gaussian Splatting Training via Host Offloading | `UNKNOWN` | 3C: 3D Gaussian Splatting & Rendering / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU-host memory offloading for 3DGS training `[title-only]`; adjacent to CLM (#10) |
| 19 | Nebula: Infinite-Scale 3D Gaussian Splatting in VR via Collaborative Rendering and Accelerated Stereo Rasterization | `UNKNOWN` | 3C / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Stereo rasterisation acceleration `[title-only]` |
| 20 | Neo: Real-Time On-Device 3D Gaussian Splatting with Reuse-and-Update Sorting Acceleration | `UNKNOWN` | 3C / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Sorting-stage acceleration in the 3DGS rasterisation pipeline `[title-only]` |
| 21 | AGS: Accelerating 3D Gaussian Splatting SLAM via CODEC-Assisted Frame Covisibility Detection | `UNKNOWN` | 3C / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Rendering/SLAM pipeline acceleration `[title-only]` |
| 22 | DeepContext: A Context-aware, Cross-platform, and Cross-framework Tool for Performance Profiling and Analysis of Deep Learning Workloads | `UNKNOWN` | 4A: ML Training & Monitoring / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU profiling tooling (call-path attribution across CPU/GPU) `[title-only]` |
| 23 | NotebookOS: A Replicated Notebook Platform for Interactive Training with On-Demand GPUs | `UNKNOWN` | 4A / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | On-demand GPU allocation/replication `[title-only]` |
| 24 | DFVG: A Heterogeneous Architecture for Speculative Decoding with Draft-on-FPGA and Verify-on-GPU | `UNKNOWN` | 2B: Speculative Decoding / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | FPGA/GPU partitioning of speculative decoding `[title-only]` |
| 25 | SwiftSpec: Disaggregated Speculative Decoding and Fused Kernels for Low-Latency LLM Inference | `UNKNOWN` | 2B / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU kernel fusion for decoding `[title-only]` |
| 26 | PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel | `UNKNOWN` | 1B: LLM Serving: Latency & Scheduling / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Multi-tile GPU attention kernel `[title-only]` |
| 27 | SuperOffload: Unleashing the Power of Large-Scale LLM Training on Superchips | `UNKNOWN` | 2A: LLM Training Systems / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | CPU-GPU coherent "superchip" (GH/GB-class) offloading `[title-only]`; GPU centrality plausible, `UNRESOLVED` |
| 28 | LAIKA: Machine Learning-Assisted In-Kernel APU Acceleration | `UNKNOWN` | 4A / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | "APU" = AMD accelerated processing unit (integrated GPU) invoked from the OS kernel; GPU centrality `UNRESOLVED` from title `[title-only]` |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| Arm Weak Memory Consistency on Apple Silicon: What Is It Good For? | "Consistency"/"memory model" hit; Arm **CPU** memory model |
| Arancini: A Hybrid Binary Translator for Weak Memory Model Architectures | Memory-model hit; CPU binary translation |
| PF-LLM: Large Language Model Hinted Hardware Prefetching | Prefetch hit; CPU hardware prefetcher |
| EARTH: An Efficient MoE Accelerator with Entropy-Aware Speculative Prefetch and Result Reuse | Prefetch hit; custom MoE accelerator, not GPU |
| SLAWS: Spatial Locality Analysis and Workload Orchestration for Sparse Matrix Multiplication | Sparse hit; target platform not stated as GPU, `UNRESOLVED` `[title-only]` |
| FuseFlow: A Fusion-Centric Compilation Framework for Sparse Deep Learning on Streaming Dataflow | Sparse + compiler hits; streaming-dataflow accelerator target |
| HybridTier: An Adaptive and Lightweight CXL-Memory Tiering System | "Memory tiering" hit; CXL host memory, no GPU |
| REPA / STARC / DARTH-PUM / PUSHtap / CoGraf / Ouroboros / ASDR | PIM/CIM architectures; "memory"/"rendering" hits only, not GPU mechanisms |
| SpecProto: A Parallelizing Compiler for Speculative Decoding of Large Protocol Buffers Data | Compiler hit; protobuf parsing, no GPU |
| COGENT / Evaluating Compiler Optimization Impacts on zkVM Performance / LOOPRAG / Linear Layouts / Trinity / RedFuser | "Compiler" hits; RISC-V tagging, zkVM, loop transformation, tensor-program and AI-accelerator targets. *Linear Layouts* and *Trinity* are plausible GPU-codegen papers — GPU centrality `UNRESOLVED` (abstracts `NOT_SEARCHED`); flagged, not silently dropped |
| Wax: Optimizing Data Center Applications With Stale Profile | "Profile" hit; CPU profile-guided optimisation |
| PowerMove; QTurbo | Quantum compilation; "power"/"compiler" hits only. **PowerMove is 30V3**, i.e. not in this population at all |
| QoServe / Shift Parallelism / XY-Serve / BlendServe / ZipServ / MoE-APEX / TetriServe / oFFN / MoDM / Mugi / TPLA / STARC-class serving papers with no GPU term or keyword | No screening keyword and no GPU mechanism evident from the title; all `[title-only]`, abstracts `NOT_SEARCHED (deprioritised)` |
| It Takes Two to Entangle | Carries a quantum-sounding term but is a distributed-systems/LLM paper (31V2, `10.1145/3779212.3790178`); no GPU mechanism named in the title |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums | (GPU is in the title; listed because the seed gave only "Insum") |
| Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation | Title says GPGPU; the mechanism (explicit shared-memory and register control, sub-byte layouts) is established from the arXiv record `arxiv.org/abs/2504.12984` |
| CLM: Removing the GPU Memory Barrier for 3D Gaussian Splatting | Title names GPU memory; the mechanism (CPU offloading with GPU-side prefetch and scheduling) is established from the NYU/arXiv PDF |
| Nebula; Neo; AGS; GS-Scale | Session 3C rasterisation/rendering papers whose GPU pipeline stage (sorting, stereo rasterisation, covisibility) is the contribution but is not named "GPU" in the title. All `[title-only]`; abstracts `NOT_SEARCHED` |
| LAIKA: Machine Learning-Assisted In-Kernel APU Acceleration | "APU" denotes an integrated GPU; placed in §3 rather than here because GPU centrality could not be established without the abstract |
| Triton-Sanitizer | "Triton" is a GPU kernel language; the GPU nature is implicit in the tool's target rather than stated. Confirmed via the author-group publication page |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| MSCCL++ | `TITLE_CORRECTED_TO:` **MSCCL++: Rethinking GPU Communication Abstractions for AI Inference**. `CONFIRMED_IN_POPULATION` — 31V2, `10.1145/3779212.3790188`. Note the preprint carries a *different* subtitle ("…for Cutting-Edge AI Applications"); the ACM record is authoritative |
| Insum | `TITLE_CORRECTED_TO:` **Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums**. `CONFIRMED_IN_POPULATION` — 31V2, `10.1145/3779212.3790176` |
| gShare | `TITLE_CORRECTED_TO:` **gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform** (lower-case "platform" as published). `CONFIRMED_IN_POPULATION` — 31V2, `10.1145/3779212.3790168` |
| GFS | `TITLE_CORRECTED_TO:` **GFS: A Preemption-aware Scheduling Framework for GPU Clusters with Predictive Spot Instance Management**. `CONFIRMED_IN_POPULATION` — 31V1, `10.1145/3760250.3762231` |
| AGIO | `TITLE_CORRECTED_TO:` **Asynchrony and GPUs: Bridging this Dichotomy for I/O with AGIO** (AGIO is not the leading word). `CONFIRMED_IN_POPULATION` — 31V2, `10.1145/3779212.3790130` |
| CHERI-SIMT | `TITLE_CORRECTED_TO:` **CHERI-SIMT: Implementing Capability Memory Protection in GPUs**. `CONFIRMED_IN_POPULATION` — 31V1, `10.1145/3760250.3762234`. **Discrepancy recorded:** the official ASPLOS 2026 program page renders the subtitle as "…in GPGPUs"; the ACM publisher record and the authors' own PDF both say "…in GPUs". Publisher form taken as official |
| cuJSON | `TITLE_CORRECTED_TO:` **cuJSON: A Highly Parallel JSON Parser for GPUs**. `CONFIRMED_IN_POPULATION` — 31V1, `10.1145/3760250.3762222` |

All seven 2026 seed entries resolve into the population. None is false or absent.

## 6. Unresolved / blocked items

1. **Per-paper volume attribution is unavailable for 144 of the 152 population papers.** The
   official program page gives titles and sessions but no DOIs, volumes or pages; the retained
   31V2 extract (`v2_2026.txt`) gives 125 DOI suffixes and page ranges but **no titles**; the
   two cannot be joined. Volume is confirmed only for the 10 papers whose publisher landing
   page surfaced in search (4 in 31V1, 6 in 31V2). Consequence: for 18 of the 28 candidates in
   §2 the DOI and official URL are `UNKNOWN`.
2. **The 16 deferred 30V3 papers cannot be separated** from the 152 31st-edition papers on the
   program page, so any one of the 168 screened titles could in principle belong to ASPLOS 2025
   rather than 2026. Only *PowerMove* is positively identified as 30V3.
3. **167 vs 168 vs 152+16 does not reconcile** (see §1.1). Unresolved; no count was invented.
4. **31V2 raw count is 135 from a single source** and the retained list covers 125; the 3
   non-paper records are inferred from the raw-minus-papers arithmetic of the prior sweep and
   are not individually identified. One retained suffix (`3818675`) is in a DOI range shared
   with the **GPGPU workshop** (`10.1145/3818671.*`) and should be re-verified.
5. **Bibliographic APIs unusable**: `api.crossref.org` HTTP 429 through this proxy (verified
   live), ACM DL 403, dblp robots-disallowed, `web.archive.org` SITE_BLOCKED,
   `conference-publishing.com/toc/ASPLOS24|26` returns *"Problem with empty event record"*.
6. **No acceptance rate** published on the reachable official 2026 pages.
7. **Artifact badge status `UNKNOWN`** for every paper (ACM publishes badges only on the paper
   and in DL metadata; DL is 403). Where an artifact repository is listed above for CHERI-SIMT
   and Triton-Sanitizer, it is the authors' group repository and is tagged as *not* stated to
   be the paper's evaluated artifact.
8. **Full-text state `NOT_SEARCHED (deprioritised)`** for the LLM-serving / DNN-application
   candidates (#11, #23–#27) and `NOT_SEARCHED` for the rendering and FHE-on-GPU candidates
   (#12–#22) per the budget rule. None of these is `NOT_FOUND`.

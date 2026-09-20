# ASPLOS 2025 (30th) — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

Reason for `PARTIAL_CENSUS`: the **population count is established** (176), and **150 of 176
population titles (85%) are enumerated with volume and DOI certainty**. The residual 26 are
the 10 items the prior volume sweep did not retain from 30V1/30V2 plus the **16 papers of
30V3**, which is published separately (2025-08-06) and whose titles appear only intermixed
into the ASPLOS **2026** program page, where they cannot be separated from 31st-edition
papers. See §1.1 and §6.

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **176** (proceedings-year basis, 30th-edition Volumes 1–3) |
| counted items excluded from population | **3** non-paper records in 30V3 (19 raw items → 16 papers; the 3 are front-matter/keynote records, individually `UNKNOWN`). Workshops, tutorials, posters, ACM SRC and artifact-evaluation reports are published outside these volumes; their counts are `UNKNOWN` (not enumerated) |
| population source (primary) | `https://api.crossref.org/` date-windowed `prefix:10.1145` cursor sweep filtered on volume DOI stem — retained extracts `domains/hpc_quantum/corpus/quantum-hpc-survey/working-evidence/asplos/vols.txt`, `.../v1.txt` (67 titles+pages, 30V1), `.../v2.txt` (83 titles+pages, 30V2), `.../v1_2025.txt` (70 DOIs), `.../v2_2025.txt` (87 page ranges) |
| population source (corroborating) | `https://www.asplos-conference.org/asplos2025/program.html` — official program, 36 sessions (1A–9D), **168 papers**, retained locally as `.../working-evidence/prog.txt`. 132 of its 168 titles match the volume extracts exactly after normalisation |
| source class | `publisher-proceedings` (count) + `official-program` (session placement, corroboration) |
| enumeration completeness | count: `UNVERIFIED_TOTAL` (per-volume totals 72 / 88 / 19 rest on the sweep's own reported item count; the retained item lists cover 67/72 and 83/88 and 0/19). Title-level enumeration: `APPROXIMATE` — 150 of 176 with volume+DOI certainty |
| paper-type mixing notes | All three volumes are main-conference research papers; ASPLOS has no short/industry split inside them. 30V3 is the fall cycle and is presented at ASPLOS 2026, not 2025 |
| official acceptance statistic | `NOT_FOUND_AFTER_SEARCH` on the reachable official pages. The 2025 program page states presentation logistics, not an accept rate |

### 1.1 Population evidence notes

**Multi-cycle / multi-volume structure.** ASPLOS 2025 (30th edition) publishes three
submission cycles as three ACM volumes. All three are main conference. The fall cycle
(Volume 3) is published in the 2025-branded proceedings but **presented at ASPLOS 2026**.

| Edition | Volume | DOI stem | ISBN | Pub. date | Raw items | Non-papers | **Regular papers** | Presented at |
|---|---|---|---|---|---|---|---|---|
| 30th | V1 | `10.1145/3669940` | 9798400706981 | 2025-03-30 | 72 | 0 | **72** | ASPLOS 2025 |
| 30th | V2 | `10.1145/3676641` | 9798400710797 | 2025-03-30 | 88 | 0 | **88** | ASPLOS 2025 |
| 30th | V3 | `10.1145/3676642` | 9798400710803 | 2025-08-06 | 19 | 3 | **16** | **ASPLOS 2026** |
| | | | | | 179 | 3 | **176** | |

**Volumes counted and why.** All three 30th-edition volumes, because the population
definition is proceedings-year: *main-conference regular research papers summed over the
year's research-paper volumes*. 30V3 is counted here even though it was presented in 2026
(its known member *PowerMove* appears in ASPLOS 2026 Session 1C).

**The alternative denominator, stated rather than mixed in.** The ASPLOS 2025 **program**
year is 30V1 + 30V2 (160) + the deferred **29th Volume 4** (24) = **184** derived. The
official 2025 program page actually lists **168** papers. The 16-paper shortfall between the
derived 184 and the listed 168 is **unresolved**: the page may omit some accepted papers, or
some accepted papers may not have been presented. This census does not use 184 or 168 as the
population; it uses 176.

**Cross-year evidence recovered during STEP B.** *Towards Unified Analysis of GPU
Consistency* — which the seed list places at 2025 — has DOI `10.1145/3622781.3674174`, i.e.
**29th ASPLOS Volume 4**, proceedings year **2024**. It is not on the 2025 program page
either. Recorded in §5 and in `ASPLOS_2024.md`.

**Site-navigation finding.** `https://www.asplos-conference.org/asplos2025/program/` serves
the **ASPLOS 2026** program (the site resolves `/program/` to the current edition). The
working 2025 URL is `https://www.asplos-conference.org/asplos2025/program.html`.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population, not over the
seed list. Keyword hits were used only to order review, never to decide
relevance. Volume/DOI is given where the retained volume extract supplies it; `UNKNOWN`
where a title is known only from the official program page. `[title-only]` marks a judgment
from the official title alone.

| # | Title (official) | Authors (first + et al.) | Session / Volume | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Virgo: Cluster-level Matrix Unit Integration in GPUs for Scalability and Energy Efficiency | `UNKNOWN` (Berkeley SLICE/ucb-bar group) | 30V2 (not on the program page) | `10.1145/3676641.3716281` | https://doi.org/10.1145/3676641.3716281 | https://arxiv.org/abs/2408.12073 ; https://people.eecs.berkeley.edu/~ysshao/assets/papers/virgo-asplos2025.pdf | https://github.com/ucb-bar/virgo | GPU microarchitecture: a cluster-level (shared-across-SM) matrix unit replacing per-core tensor cores. Pure GPU execution/datapath mechanism |
| 2 | ARC: Warp-level Adaptive Atomic Reduction in GPUs to Accelerate Differentiable Rendering | `UNKNOWN` (Giannoula is a listed co-author) | Session 3B / 30V1 | `10.1145/3669940.3707238` | https://doi.org/10.1145/3669940.3707238 | https://people.mpi-sws.org/~cgiannoula/assets/publications/ARC_asplos25_full.pdf | `NOT_FOUND_AFTER_SEARCH` | Warp-level atomic reduction hardware/software mechanism inside the GPU SIMT pipeline |
| 3 | Treelet Accelerated Ray Tracing on GPUs | Chou et al. `[inferred from the author-page PDF filename chou.asplos2025.pdf]` | Session 3B / 30V2 | `10.1145/3676641.3716279` | https://doi.org/10.1145/3676641.3716279 | https://people.ece.ubc.ca/aamodt/publications/papers/chou.asplos2025.pdf | `NOT_FOUND_AFTER_SEARCH` | GPU ray-tracing memory-locality mechanism (treelet scheduling / BVH traversal on GPU) |
| 4 | Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains | `UNKNOWN` (Cornell CS) | 30V2 (not on the program page) | `10.1145/3676641.3715983` | https://doi.org/10.1145/3676641.3715983 | https://arxiv.org/abs/2407.21255 | `NOT_FOUND_AFTER_SEARCH` | Offloads GPU memory across a scale-up GPU domain (NVLink/NVSwitch-class fabric) using peer GPU memory; GPU memory-hierarchy mechanism |
| 5 | Dilu: Enabling GPU Resourcing-on-Demand for Serverless DL Serving via Introspective Elasticity | `UNKNOWN` | 30V1 (not on the program page) | `10.1145/3669940.3707251` | https://doi.org/10.1145/3669940.3707251 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU resource partitioning / elastic allocation mechanism for serverless DL `[title-only]` |
| 6 | Forecasting GPU Performance for Deep Learning Training and Inference | `UNKNOWN` | Session 5A / 30V1 | `10.1145/3669940.3707265` | https://doi.org/10.1145/3669940.3707265 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU performance modelling / prediction across GPU generations `[title-only]` |
| 7 | Accelerating Number Theoretic Transform with Multi-GPU Systems for Efficient Zero Knowledge Proof | `UNKNOWN` | Session 9D / 30V1 | `10.1145/3669940.3707241` | https://doi.org/10.1145/3669940.3707241 | `NOT_SEARCHED` | `NOT_SEARCHED` | Multi-GPU NTT: inter-GPU data exchange and kernel decomposition `[title-only]` |
| 8 | Optimizing Datalog for the GPU | `UNKNOWN` (Yihao Sun listed on the author PDF) | 30V1 (not on the program page) | `10.1145/3669940.3707274` | https://doi.org/10.1145/3669940.3707274 | https://arxiv.org/abs/2311.02206 ; https://thomas.gilray.org/pdf/datalog-gpu.pdf | `NOT_FOUND_AFTER_SEARCH` | GPU relational-algebra kernels / hash-index layout for Datalog fixpoint; GPU execution mechanism |
| 9 | Composing Distributed Computations Through Task and Kernel Fusion | `UNKNOWN` | Session 2B / 30V1 | `10.1145/3669940.3707216` | https://doi.org/10.1145/3669940.3707216 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel fusion across distributed task graphs `[title-only]` |
| 10 | BatchZK: A Fully Pipelined GPU-Accelerated System for Batch Generation of Zero-Knowledge Proofs | `UNKNOWN` | Session 9D / 30V1 | `10.1145/3669940.3707270` | https://doi.org/10.1145/3669940.3707270 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU pipeline design for MSM/NTT batch ZKP `[title-only]` |
| 11 | Efficient Lossless Compression of Scientific Floating-Point Data on CPUs and GPUs | `UNKNOWN` | Session 4C / 30V1 | `10.1145/3669940.3707280` | https://doi.org/10.1145/3669940.3707280 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel design for lossless FP compression; CPU/GPU codesign `[title-only]` |
| 12 | MoE-Lightning: High-Throughput MoE Inference on Memory-constrained GPUs | `UNKNOWN` | Session 6C / 30V1 | `10.1145/3669940.3707267` | https://doi.org/10.1145/3669940.3707267 | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU memory-constrained MoE inference; CPU-GPU pipelining `[title-only]` |
| 13 | Helix: Serving Large Language Models over Heterogeneous GPUs and Network via Max-Flow | `UNKNOWN` | Session 5C / 30V1 | `10.1145/3669940.3707215` | https://doi.org/10.1145/3669940.3707215 | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Heterogeneous GPU placement/partitioning `[title-only]` |
| 14 | Frugal: Efficient and Economic Embedding Model Training with Commodity GPUs | `UNKNOWN` | Session 8A / 30V1 | `10.1145/3669940.3707245` | https://doi.org/10.1145/3669940.3707245 | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Commodity-GPU memory/bandwidth constraints for embedding training `[title-only]` |
| 15 | OS2G: A High-Performance DPU Offloading Architecture for GPU-based Deep Learning with Object Storage | `UNKNOWN` | Session 2B / 30V2 | `10.1145/3676641.3716265` | https://doi.org/10.1145/3676641.3716265 | `NOT_SEARCHED` | `NOT_SEARCHED` | DPU→GPU data path, GPUDirect-class storage offload `[title-only]` |
| 16 | Vela: A Virtualized LLM Training System with GPU Direct RoCE | `UNKNOWN` | Session 5C / 30V2 | `10.1145/3676641.3716280` | https://doi.org/10.1145/3676641.3716280 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPUDirect RDMA over RoCE in a virtualised GPU cluster `[title-only]` |
| 17 | BQSim: GPU-accelerated Batch Quantum Circuit Simulation using Decision Diagram | `UNKNOWN` | Session 1B / 30V2 | `10.1145/3676641.3715984` | https://doi.org/10.1145/3676641.3715984 | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel/decision-diagram batching for circuit simulation `[title-only]` |
| 18 | FastGL: A GPU-Efficient Framework for Accelerating Sampling-Based GNN Training at Large Scale | `UNKNOWN` | Session 8A / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU sampling/feature-gather pipeline for GNN training `[title-only]`. Known only from the program page — may be 30V1/30V2 (unretained) or deferred 29V4 |
| 19 | MetaSapiens: Real-Time Neural Rendering with Efficiency-Aware Pruning and Accelerated Foveated Rendering | `UNKNOWN` | Session 3B / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Foveated rasterisation/rendering acceleration `[title-only]` |
| 20 | D-VSync: Decoupled Rendering and Displaying for Smartphone Graphics | `UNKNOWN` | Session 3B / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Mobile GPU render/display pipeline synchronisation `[title-only]` |
| 21 | TAPAS: Thermal- and Power-Aware Scheduling for LLM Inference in Cloud Platforms | `UNKNOWN` | Session 7A / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU-fleet thermal/power scheduling; GPU centrality plausible but `UNRESOLVED` `[title-only]` |
| 22 | FSMoE: A Flexible and Scalable Training System for Sparse Mixture-of-Experts Models | `UNKNOWN` | Session 6C / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Expert all-to-all collectives on GPUs `[title-only]` |
| 23 | MoC-System: Efficient Fault Tolerance for Sparse Mixture-of-Experts Model Training | `UNKNOWN` | Session 6C / volume `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU checkpointing/fault tolerance in MoE training `[title-only]` |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| PIM Is All You Need: A CXL-Enabled GPU-Free System for Large Language Model Inference (30V2, `10.1145/3676641.3716267`) | Title's GPU term is the thing being *removed*; the contribution is a CXL+PIM system explicitly without GPUs. GPU appears only as the displaced baseline |
| Stramash: A Fused-Kernel Operating System For Cache-Coherent, Heterogeneous-ISA Platforms (30V2, `10.1145/3676641.3716275`) | "Kernel" = OS kernel, not a GPU compute kernel |
| Snowplow: Effective Kernel Fuzzing with a Learned White-box Test Mutator; KernelGPT: Enhanced Kernel Fuzzing via Large Language Models | "Kernel" = Linux kernel; fuzzing, not GPU |
| Reload+Reload: Exploiting Cache and Memory Contention Side Channel on AMD SEV (30V2, `10.1145/3676641.3716017`) | "AMD" refers to an x86 CPU confidential-computing feature (SEV) |
| Spindle: Efficient Distributed Training of Multi-Task Large Models via Wavefront Scheduling | "Wavefront" = a scheduling wavefront (dependency frontier), not an AMD GPU wavefront |
| Using Analytical Performance/Power Model and Fine-Grained DVFS to Enhance AI Accelerator Energy Efficiency (30V1, `10.1145/3669940.3707231`) | DVFS/power hits, but the stated target is an "AI Accelerator". GPU centrality `UNRESOLVED` (abstract `NOT_SEARCHED`) — flagged, not silently dropped |
| RASSM (30V1, `10.1145/3669940.3707219`); GUST; DynaX; SLAWS-class sparse papers | Sparse-matrix keyword hits; target platform not stated as GPU in the title, `UNRESOLVED` `[title-only]` |
| UniZK: Accelerating Zero-Knowledge Proof with Unified Hardware and Flexible Kernel Mapping (30V1, `10.1145/3669940.3707228`) | "Kernel mapping" onto a custom ZKP accelerator, not a GPU |
| ShadowLoad: Injecting State into Hardware Prefetchers; Hierarchical Prefetching | Prefetch hits; CPU hardware prefetchers |
| CINM (Cinnamon); Be CIM or Be Memory | Compute-in-memory compilers; not GPU |
| Validating JVM Compilers…; The Mutators Reloaded; ClosureX; Ratte | "Compiler" hits; compiler-testing/fuzzing, no GPU target |
| Robustness Verification for Checking Crash Consistency of Non-volatile Memory | "Consistency" hit; NVM crash consistency, not a GPU memory model |
| Protecting Cryptographic Code Against Spectre-RSB (30V2, `10.1145/3676641.3716015`) | Security/CPU speculation |
| QECC-Synth: A Layout Synthesizer for Quantum Error Correction Codes on Sparse Architectures | "Sparse" hit; quantum code layout |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| Treelet Accelerated Ray Tracing on GPUs | (GPU *is* in the title — listed here only to note that "Treelet" alone, as the seed gave it, carries no GPU term) |
| Composing Distributed Computations Through Task and Kernel Fusion | "Kernel fusion" in the title is the GPU-kernel sense; the paper sits in the 30V1 ML-systems cohort. Abstract `NOT_SEARCHED` — inclusion is `[title-only]` and should be re-verified |
| MetaSapiens; D-VSync | Rendering-pipeline papers whose GPU/display-controller mechanism is implied by "Rendering"/"Graphics" but not named. Both `[title-only]`; abstracts `NOT_SEARCHED` |
| Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains | GPU is in the title; the *mechanism* (peer-GPU memory over a scale-up fabric) is established from the arXiv record `arxiv.org/abs/2407.21255` |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| Virgo | `TITLE_CORRECTED_TO:` **Virgo: Cluster-level Matrix Unit Integration in GPUs for Scalability and Energy Efficiency**. `CONFIRMED_IN_POPULATION` — 30V2, `10.1145/3676641.3716281` |
| Forecasting GPU Performance | `TITLE_CORRECTED_TO:` **Forecasting GPU Performance for Deep Learning Training and Inference**. `CONFIRMED_IN_POPULATION` — 30V1, `10.1145/3669940.3707265` |
| ARC | `TITLE_CORRECTED_TO:` **ARC: Warp-level Adaptive Atomic Reduction in GPUs to Accelerate Differentiable Rendering**. `CONFIRMED_IN_POPULATION` — 30V1, `10.1145/3669940.3707238` |
| Towards Unified Analysis of GPU Consistency | **`NOT_IN_MAIN_POPULATION`** for ASPLOS 2025. DOI `10.1145/3622781.3674174` places it in the **29th** ASPLOS **Volume 4** (proceedings year **2024**, presented at ASPLOS 2025). It is also absent from the official 2025 program page. Title itself is exact. Recorded in `ASPLOS_2024.md` §2 |
| Aqua | `TITLE_CORRECTED_TO:` **Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains**. `CONFIRMED_IN_POPULATION` — 30V2, `10.1145/3676641.3715983`. (Note: arXiv and Cornell render it "AQUA" in caps; the ACM record uses "Aqua") |
| Treelet | `TITLE_CORRECTED_TO:` **Treelet Accelerated Ray Tracing on GPUs**. `CONFIRMED_IN_POPULATION` — 30V2, `10.1145/3676641.3716279` |
| Dilu | `TITLE_CORRECTED_TO:` **Dilu: Enabling GPU Resourcing-on-Demand for Serverless DL Serving via Introspective Elasticity**. `CONFIRMED_IN_POPULATION` — 30V1, `10.1145/3669940.3707251` |
| a multi-GPU NTT-related paper | `TITLE_CORRECTED_TO:` **Accelerating Number Theoretic Transform with Multi-GPU Systems for Efficient Zero Knowledge Proof**. `CONFIRMED_IN_POPULATION` — 30V1, `10.1145/3669940.3707241`, official program Session 9D |

## 6. Unresolved / blocked items

1. **30V3 (16 papers) is not title-enumerated.** It was published 2025-08-06 and presented at
   ASPLOS 2026, so its titles are mixed into the ASPLOS 2026 program page with the 152
   31st-edition papers and cannot be separated there. Only one member is identified
   (*PowerMove: Optimizing Compilation for Neutral Atom Quantum Computers with Zoned
   Architecture*, ASPLOS 2026 Session 1C — not a GPU paper). **Any GPU paper in 30V3 is
   invisible to this census.**
2. **10 of the 160 papers in 30V1+30V2 have no retained title** (the prior sweep kept 67/72
   and 83/88). Up to 10 of the 31 program-page titles that do not match the volume extracts
   may be those items, but they cannot be distinguished from the 24 deferred 29V4 papers that
   the 2025 program also lists.
3. **The 184-vs-168 discrepancy is unresolved**: volume arithmetic plus the deferral rule
   predicts 184 papers in the 2025 program; the official program page lists 168.
4. **Bibliographic APIs are unusable here.** `api.crossref.org` returns HTTP 429 through this
   proxy (verified live); ACM DL returns 403; dblp is robots-disallowed; `web.archive.org` is
   SITE_BLOCKED. All volume counts therefore inherit the prior session's Crossref sweep as a
   single source.
5. **No official acceptance statistic found** for ASPLOS 2025.
6. **Artifact badge status `UNKNOWN`** for every paper (ACM publishes badges only on the paper
   and in DL metadata; DL is 403).
7. **Full-text state `NOT_SEARCHED (deprioritised)`** for the LLM-serving/DNN-application
   candidates (#12–#14, #21–#23) per the budget rule. These are not `NOT_FOUND` — no search
   was run for them.

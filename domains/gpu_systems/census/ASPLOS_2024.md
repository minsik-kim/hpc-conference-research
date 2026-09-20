# ASPLOS 2024 (29th) — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

Reason for `PARTIAL_CENSUS`: the **population count is established** (194, volume-enumerated),
but only **138 of 194 titles could be enumerated verbatim** from any reachable source, because
the official ASPLOS 2024 main-program page is truncated after Session 8C and the ACM DL
volume TOCs are unreachable from this environment (403). STEP B therefore screens 138/194
(71%) of the population. See §1.1 and §6.

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **194** (proceedings-year basis, 29th-edition Volumes 1–4) |
| counted items excluded from population | **4** keynote/front-matter records in 29V3 (DOI suffixes `3655589`–`3655592`, page ranges `2-2`, `3-3`, `4-4`); workshops, tutorials, WACI, the Debate, posters and artifact-evaluation reports are published outside these four volumes and are not counted. Exact counts for those exclusions: `UNKNOWN` (not enumerated) |
| population source (primary) | `https://api.crossref.org/` date-windowed `prefix:10.1145` cursor sweep, filtered client-side on volume DOI stem — retained extracts in `domains/hpc_quantum/corpus/quantum-hpc-survey/working-evidence/asplos/vols.txt` and `.../d2024.txt` (170 DOIs + page ranges for 29V2+29V3+29V4, reconciling exactly 76+70+24) |
| population source (corroborating) | `https://www.asplos-conference.org/asplos2024/main-program/index.html` — its "Additional Program Resources" block links exactly **Proceedings Volume 1 (`10.1145/3617232`), Volume 2 (`10.1145/3620665`), Volume 3 (`10.1145/3620666`)** and no Volume 4, which independently corroborates the volume identity and the deferral rule |
| source class | `publisher-proceedings` (count) + `official-program` (volume identity, session placement) |
| enumeration completeness | count: `EXACT` for 29V2/29V3/29V4 (item-level extract reconciles), `UNVERIFIED_TOTAL` for 29V1 (28 = sweep-reported item count, no retained item list). Title-level enumeration: `APPROXIMATE` — 138 of 194 |
| paper-type mixing notes | ASPLOS labels everything in these volumes as main-conference research papers; there is no "short paper"/"industry track" split inside them. The only non-papers found are 4 keynote abstracts in 29V3. Front matter carries no DOI in the retained extract |
| official acceptance statistic | `NOT_FOUND_AFTER_SEARCH` on the official ASPLOS 2024 site pages fetched (program, main-program). No accept-rate sentence appears on the program page |

### 1.1 Population evidence notes

**The multi-cycle / multi-volume structure — the controlling fact.** ASPLOS runs multiple
submission cycles per edition and publishes each cycle as a **separate ACM proceedings
volume** of the same edition. All volumes are main conference; none is a workshop or
satellite. The fall cycle is published in the edition-year volume but **presented at the
next year's conference** (verbatim from the ASPLOS 2024 CFP, quoted in the prior local
census: *"Accepted major revisions of the fall cycle will be published as ASPLOS'24 papers
but will be presented in ASPLOS'25."*).

| Edition | Volume | DOI stem | ISBN | Pub. date | Raw items | Non-papers | **Regular papers** | Presented at |
|---|---|---|---|---|---|---|---|---|
| 29th | V1 | `10.1145/3617232` | 9798400703720 | 2024-04-17 | 28 | 0 | **28** | ASPLOS 2024 |
| 29th | V2 | `10.1145/3620665` | 9798400703850 | 2024-04-27 | 76 | 0 | **76** | ASPLOS 2024 |
| 29th | V3 | `10.1145/3620666` | 9798400703867 | 2024-04-27 | 70 | 4 (keynotes) | **66** | ASPLOS 2024 |
| 29th | V4 | `10.1145/3622781` | 9798400703911 | 2024-04-27 | 24 | 0 | **24** | **ASPLOS 2025** |
| | | | | | 198 | 4 | **194** | |

**Volumes counted and why.** All four 29th-edition volumes are counted, because the task's
population definition is *"main-conference regular research papers, summed over the year's
research-paper volumes"* — i.e. a **proceedings-year** denominator. 29V4 is a 2024-branded
ASPLOS volume and is counted here even though its papers were presented in 2025.

**The alternative denominator, stated rather than mixed in.** The ASPLOS 2024 **program**
year is a different number: 29V1+V2+V3 = **170** papers, plus the deferred **28th-edition
Volume 4** cohort (`10.1145/3623278`), whose size was never enumerated. Program-year total
is therefore `TOTAL_COUNT_UNVERIFIED`. This census reports the proceedings figure (194) as
the population and never adds the two.

**Confirmed instance of the cross-year hazard.** *Predict; Don't React for Enabling
Efficient Fine-Grain DVFS in GPUs* appears in the official ASPLOS 2024 program (Session 4C:
Power and Energy) but its DOI is **`10.1145/3623278.3624756` — 28th ASPLOS Volume 4**,
proceedings year 2023. It is therefore **program-2024 but not population-2024**. Conversely
*Towards Unified Analysis of GPU Consistency* (`10.1145/3622781.3674174`) is **29V4**, i.e.
population-2024, but does not appear on the 2024 program page (it was presented in 2025).
Both facts were established from publisher landing-page titles surfaced in search, not from
memory.

**Enumeration gap — exactly what is missing.** The official program page
(`.../asplos2024/main-program/index.html`) lists Sessions 1A through 8C and then stops
mid-conference; Session 8C shows only 3 papers and there is no 8D or Session 9. Two URL
variants and a "start reading at 8C" re-fetch both return the same truncated page, so the
truncation is in the published page, not in retrieval. That page yields **133 verbatim
titles**. The companion *Paper Abstracts* page
(`.../asplos2024/main-program/abstracts/`) contains the full set but exceeds the fetch
transport limit and delivers only its first 52 entries. ACM DL returns 403; dblp is
robots-disallowed; Crossref/OpenAlex/Semantic Scholar return HTTP 429 through this proxy
(confirmed by a live attempt, not assumed). Adding the 5 titles independently established
by DOI during STEP B (Predict; Don't React — program-only; Towards Unified Analysis of GPU
Consistency; plus 3 already-known 29V4 items) gives **138 distinct titles**. The remaining
~56 titles are `NOT_FOUND_AFTER_SEARCH`.

**Site-navigation finding worth recording.** `https://www.asplos-conference.org/asplos2024/program/`
and `https://www.asplos-conference.org/asplos2025/program/` both serve the **ASPLOS 2026**
program (the site resolves `/program/` to the current edition). The working historical URLs
are `.../asplos2024/main-program/index.html` and `.../asplos2025/program.html`. Any census
that trusts `/asplos2024/program/` will silently census the wrong year.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population, not over the
seed list. Keyword hits were used only to order review, never to decide
relevance. Coverage: 138 of 194 population titles screened (71%). `[title-only]`
marks a judgment made from the official title alone — no abstract or full text was read.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives | Pati et al. `[inferred from Semantic Scholar author slug]` | 1B: Optimizing ML Communication | `10.1145/3620665.3640410` (29V2) | https://doi.org/10.1145/3620665.3640410 | https://arxiv.org/abs/2401.16677 | `NOT_FOUND_AFTER_SEARCH` | GPU hardware tracker that fuses a producer GEMM kernel with the collective that consumes it; near-memory reduction. GPU execution + collective mechanism is the contribution |
| 2 | TCCL: Discovering Better Communication Paths for PCIe GPU Clusters | Heehoon Kim et al. (from the ACM PDF title line) | 1B: Optimizing ML Communication | `10.1145/3620666.3651362` (29V3) | https://doi.org/10.1145/3620666.3651362 | https://dl.acm.org/doi/pdf/10.1145/3620666.3651362 (open PDF on publisher) ; author page https://junyeol.me/2024/05/05/tccl | https://zenodo.org/records/10799424 | NCCL-path search for PCIe-attached GPU clusters; GPU interconnect topology is the mechanism |
| 3 | GMT: GPU Orchestrated Memory Tiering for the Big Data Era | Chang et al. `[inferred from dblp record key ChangHSMQH24]` | 8B: Memory: Address Translation and Tiering | `10.1145/3620666.3651353` (29V3) | https://doi.org/10.1145/3620666.3651353 | `NOT_FOUND_AFTER_SEARCH` (institutional records only: experts.illinois.edu, pure.psu.edu) | https://github.com/wangqingheng/GMT | GPU-orchestrated host/SSD memory tiering; GPU-side page management is the contribution |
| 4 | GMLake: Efficient and Transparent GPU Memory Defragmentation for Large-scale DNN Training with Virtual Memory Stitching | `UNKNOWN` | 8B: Memory: Address Translation and Tiering | `10.1145/3620665.3640423` (29V2) | https://doi.org/10.1145/3620665.3640423 | https://arxiv.org/abs/2401.08156 | https://github.com/antgroup/glake (GMLake subdirectory) | CUDA virtual-memory-management stitching to defragment GPU allocator; pure GPU memory mechanism |
| 5 | MaxK-GNN: Extremely Fast GPU Kernel Design for Accelerating Graph Neural Networks Training | Peng et al. `[inferred from dblp record key PengXSHZHKKD24]` | 7D: Graph Neural Networks | `10.1145/3620665.3640426` (29V2) | https://doi.org/10.1145/3620665.3640426 | https://arxiv.org/abs/2312.08656 | https://github.com/xiexi51/MaxK-GNN | GPU SpGEMM/SpMM kernel design with row-wise product and shared-memory staging |
| 6 | Towards Unified Analysis of GPU Consistency | Haining Tong et al. (from the author-page PDF title line) | `UNKNOWN` (not on the 2024 program page; presented ASPLOS 2025) | `10.1145/3622781.3674174` (29V4) | https://doi.org/10.1145/3622781.3674174 | https://hernanponcedeleon.github.io/pdfs/asplos2024.pdf ; https://researchportal.helsinki.fi/files/646149224/Towards.pdf | `NOT_FOUND_AFTER_SEARCH` | GPU memory-consistency model; axiomatic unification of PTX/Vulkan/scoped GPU models. GPU memory model is the whole paper |
| 7 | Hector: An Efficient Programming and Compilation Framework for Implementing Relational Graph Neural Networks in GPU Architectures | `UNKNOWN` | 7D: Graph Neural Networks | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU code-generation / compilation framework targeting GPU architectures `[title-only]` |
| 8 | A Journey of a 1,000 Kernels Begins with a Single Step: A Retrospective of Deep Learning on GPUs | `UNKNOWN` | 1C: Case Studies and Experience | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | GPU kernel-level characterisation study of DL workloads `[title-only]` |
| 9 | RAP: Resource-aware Automated GPU Sharing for Multi-GPU Recommendation Model Training and Input Preprocessing | `UNKNOWN` | 3C: ML Cluster Scheduling | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Multi-GPU sharing / resource partitioning mechanism `[title-only]` |
| 10 | GSCore: Efficient Radiance Field Rendering via Architectural Support for 3D Gaussian Splatting | `UNKNOWN` | 4A: Accelerators | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED` | `NOT_SEARCHED` | Rasterisation/rendering pipeline architecture; GPU-baseline rendering mechanism `[title-only]` |
| 11 | Centauri: Enabling Efficient Scheduling for Communication-Computation Overlap in Large Model Training via Communication Partitioning | `UNKNOWN` | 1B: Optimizing ML Communication | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Collective/compute overlap partitioning in large-model training; GPU-cluster communication mechanism, no GPU term in title (see §4) `[title-only]` |
| 12 | SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification | `UNKNOWN` | 2D: ML Inference Systems | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | LLM-serving on GPUs; deprioritised per budget rule `[title-only]` |
| 13 | ExeGPT: Constraint-Aware Resource Scheduling for LLM Inference | `UNKNOWN` | 2D: ML Inference Systems | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU resource scheduling for LLM inference `[title-only]` |
| 14 | SpotServe: Serving Generative Large Language Models on Preemptible Instances | `UNKNOWN` | 2D: ML Inference Systems | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | Preemptible GPU instance serving `[title-only]` |
| 15 | Characterizing Power Management Opportunities for LLMs in the Cloud | `UNKNOWN` | 4C: Power and Energy | `UNKNOWN` | `UNKNOWN` | `NOT_SEARCHED (deprioritised)` | `NOT_SEARCHED` | GPU power/energy characterisation for LLM fleets; GPU centrality `UNRESOLVED` from title `[title-only]` |

**Program-only item (in the 2024 program, NOT in the 2024 population).** Recorded here so it
is not lost, and excluded from the counts above:

| Title (official) | Authors | Session | DOI | Official URL | Public full text | Artifact/code | Note |
|---|---|---|---|---|---|---|---|
| Predict; Don't React for Enabling Efficient Fine-Grain DVFS in GPUs | `UNKNOWN` | 4C: Power and Energy (ASPLOS 2024 program) | `10.1145/3623278.3624756` (**28th** ASPLOS V4) | https://doi.org/10.1145/3623278.3624756 | https://dl.acm.org/doi/pdf/10.1145/3623278.3624756 (open PDF on publisher) ; https://www.microsoft.com/en-us/research/publication/predict-do-not-react-for-enabling-efficient-fine-grain-dvfs-in-gpus/ | `NOT_FOUND_AFTER_SEARCH` | Fine-grain GPU DVFS prediction. **Proceedings year 2023 (28th V4)** — belongs to the ASPLOS 2023 population, presented 2024 |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| Explainable Port Mapping Inference with Sparse Performance Counters for AMD's Zen Architectures | "AMD" refers to Zen **CPU** cores; x86 port-mapping inference |
| Two-Face: Combining Collective and One-Sided Communication for Efficient Distributed SpMM | "collective"/"sparse" hits; distributed-memory SpMM. GPU centrality `UNRESOLVED` (abstract `NOT_SEARCHED`) — flagged, not silently dropped |
| Expanding Datacenter Capacity with DVFS Boosting: A safe and scalable deployment experience | DVFS hit; server/CPU fleet power deployment, no GPU indication `[title-only]` |
| ACES: Accelerating Sparse Matrix Multiplication with Adaptive Execution Flow and Concurrency-Aware Cache Optimizations | Sparse + cache hits; a dedicated SpMM accelerator, not a GPU mechanism `[title-only]` |
| FEASTA: A Flexible and Efficient Accelerator for Sparse Tensor Algebra in Machine Learning | Sparse hit; custom accelerator `[title-only]` |
| AttAcc! / SpecPIM / PIM-DL / NeuPIMs | PIM/NPU-PIM architectures; "power" keyword only. Not GPU mechanisms |
| Optimal Kernel Orchestration for Tensor Programs with Korch | "kernel" = tensor operator, framework-level; GPU backend incidental `[title-only]` |
| PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation | Compiler hit; Python-level tracing/compilation, not a GPU mechanism `[title-only]` |
| Supporting Descendants in SIMD-Accelerated JSONPath | SIMD hit; CPU SIMD, not SIMT/GPU |
| PDIP / Limoncello / PATHFINDER / RPG² / CrossPrefetch | Prefetch hits; CPU instruction/data/I-O prefetching |
| HIDA, SEER, Hydride, C4CAM, BaCO, SIRO, Pythia, TrackFM, and the remaining compiler-keyword hits | "compiler" hit only; HLS, CAM/in-memory, far-memory or security targets, no GPU |
| MECH / QuFEM / Promatch / Codesign / A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer / Elivagar / Red-QAOA / ProxiML / VarSaw | Quantum architecture papers; no GPU mechanism |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives | Title says "Compute & Collectives"; the mechanism is a GPU-side hardware tracker and near-memory reduction in the GPU memory system — established from the arXiv record (`arxiv.org/abs/2401.16677`), matched on abstract content because the arXiv markdown conversion strips the Title:/Authors: block |
| Centauri: Enabling Efficient Scheduling for Communication-Computation Overlap in Large Model Training via Communication Partitioning | Title has no GPU term; it sits in *Session 1B: Optimizing ML Communication* alongside TCCL and T3, i.e. GPU-cluster collective communication. Abstract `NOT_SEARCHED (deprioritised)` — inclusion is `[title+session-only]` |
| Characterizing Power Management Opportunities for LLMs in the Cloud | Listed in §3 rather than here, because GPU centrality could not be established without the abstract |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| T3: Transparent Tracking & Triggering for Fine-Grained Overlap of Compute & Collectives | `TITLE_CORRECTED_TO:` **T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives** (publisher capitalises "Fine-grained", not "Fine-Grained"). `CONFIRMED_IN_POPULATION` — 29V2, `10.1145/3620665.3640410` |
| GMT: GPU Orchestrated Memory Tiering | `TITLE_CORRECTED_TO:` **GMT: GPU Orchestrated Memory Tiering for the Big Data Era**. `CONFIRMED_IN_POPULATION` — 29V3, `10.1145/3620666.3651353` |
| TCCL | `TITLE_CORRECTED_TO:` **TCCL: Discovering Better Communication Paths for PCIe GPU Clusters**. `CONFIRMED_IN_POPULATION` — 29V3, `10.1145/3620666.3651362` |
| a GPU DVFS paper described as "Predict, Don't React" | `TITLE_CORRECTED_TO:` **Predict; Don't React for Enabling Efficient Fine-Grain DVFS in GPUs** (semicolon, not comma). Then **`NOT_IN_MAIN_POPULATION`** for ASPLOS 2024: DOI `10.1145/3623278.3624756` places it in the **28th** ASPLOS Volume 4 (proceedings year 2023). It *was* presented in the ASPLOS 2024 program, Session 4C. This is the clearest case in the seed list of program-year/proceedings-year conflation |

## 6. Unresolved / blocked items

1. **~56 of 194 population titles are not enumerable.** The official ASPLOS 2024 main-program
   page truncates after Session 8C (no 8D, no Session 9); the *Paper Abstracts* page exceeds
   the fetch transport limit at 52 of its entries; ACM DL = 403; dblp = robots-disallowed;
   Crossref = HTTP 429 through this proxy (attempted live, `api.crossref.org/works?filter=prefix:10.1145,...`);
   `web.archive.org` = SITE_BLOCKED. Consequence: **any GPU paper sitting in the unenumerated
   tail of the 2024 program, or in 29V1/29V4, is invisible to this census.** One such paper was
   recovered only by accident (*Towards Unified Analysis of GPU Consistency*, 29V4), which
   proves the gap is not empty.
2. **29V1's 28 items were never enumerated at item level** by the prior sweep either, so the
   28 rests on a sweep-reported count, not a displayable list (`UNVERIFIED_TOTAL`).
3. **No official acceptance statistic located** for ASPLOS 2024 on the conference site pages
   reachable here.
4. **DOIs `UNKNOWN` for 7 of 15 candidates** because there is no reachable title→DOI mapping:
   `d2024.txt` holds 170 DOIs with page ranges but no titles, and the program page holds titles
   but no pages or DOIs. The two cannot be joined from local evidence.
5. **Artifact-evaluation badge status is not publicly determinable** (ACM states badges live
   only on the paper and in ACM DL metadata; DL is 403). `UNKNOWN` for every paper.

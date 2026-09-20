# MICRO 2026 (MICRO-59) — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **UNKNOWN** — no public main-program or accepted-papers list exists as of 2026-09-18 |
| counted items excluded from population | N/A (nothing to exclude yet). What IS public on microarch.org/micro59 is: workshops & tutorials listings, calls for papers (main + industry track), artifact-evaluation and competition calls, venue/registration/visa pages, committees. None of these carries research-paper titles. |
| population source (primary) | https://www.microarch.org/micro59/ — `official-program` site, but the program section publishes only workshops/tutorials; **no accepted-papers page exists** |
| population source (corroborating) | https://mengli.me/news/micro-2026-accepted/ — `author-page` (names 2 accepted papers, see §1.1). No `official-proceedings`, `publisher-proceedings` or `bibliographic-index` source exists yet. |
| source class | `official-program` (for the negative finding) + `author-page` (for the two known titles) |
| enumeration completeness | `UNVERIFIED_TOTAL` |
| paper-type mixing notes | Cannot be assessed: MICRO-59 has a separate Industry Track call (https://www.microarch.org/micro59/submit/industrial.php), so when the program appears, industry-track papers will need to be checked for whether they are folded into the main session grid (as they were in MICRO-57 and MICRO-58) or labelled separately. |

### 1.1 Population evidence notes

**What is public (verbatim from the official site):**
- Conference dates and location: "October 31 – November 4, 2026" in "Athens, Greece". (Note: the task brief said "October 2026"; the official dates straddle Oct/Nov.)
- Author notification: **July 7, 2026**. Camera-ready deadline: **September 11, 2026**. Author registration deadline: September 11, 2026 AoE. Early registration deadline: September 28, 2026 AoE.
- The homepage navigation exposes Submit Work / Program / Attend / Committees / Code of Conduct. Under **Program**, only workshops and tutorials are listed. The official site fetch reported: "No accepted papers list or finalized main program has been published… There is no dedicated 'Accepted Papers' or comprehensive 'Program' link visible on the homepage at this stage."

**What is NOT public:**
- No accepted-papers list, no session grid, no paper count, no acceptance rate, no submission count. microarch.org/news/ carries nothing on MICRO-59 acceptance statistics.
- https://microarch.hosting.acm.org/micro59/program/main-program.php → **HTTP 404**.
- https://www.microarch.org/micro59/program/workshops.php → **HTTP 404**.

**Source-reliability warning (important for any later re-run):**
Fetches of `https://www.microarch.org/micro59/program/` and `https://www.microarch.org/micro59/program/program.php` returned the **MICRO 2025 (MICRO-58) main program** — the returned content self-identified as the October 18–22, 2025, Seoul program (sessions 1A–9C, MICRO-58 papers, MICRO-58 best-paper annotations), in one case mislabelled "main program for MICRO 59". These responses are **stale/misrouted MICRO-58 content and must not be used as MICRO-59 population evidence**. No MICRO-59 paper title was taken from them.

**Papers known to be accepted (incomplete, non-official-program source):**
From an author's own news page (`author-page`, https://mengli.me/news/micro-2026-accepted/): "Two papers on privacy-preserving AI accelerators (i.e., OptiPrime and Helios) are accepted by MICRO 2026."
1. **OptiPrime: Optimizing Private Inference through Protocol-Hardware Codesign** (led by Jiangrui Yu)
2. **Helios: Melting Kernel Boundaries for GPU-Accelerated HE via Graph Rewriting and Microarchitecture-Aware Mapping** (led by Yi Chen and Ziyu Tang)

These two titles are evidence that MICRO-59 acceptances exist, not evidence of the population size. **Do not treat 2 as any kind of count.** Because the camera-ready deadline was only 2026-09-11, the program should be expected to appear on microarch.org/micro59 within weeks; this census should be re-run then.

## 2. Broad GPU candidates (STEP B)

Screening could only be applied to the two titles that are publicly known, not
to a reconstructed population. **This section is incomplete by construction.**

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Helios: Melting Kernel Boundaries for GPU-Accelerated HE via Graph Rewriting and Microarchitecture-Aware Mapping | Yi Chen and Ziyu Tang (paper leads per the author news page); full author list UNKNOWN | UNKNOWN (no session grid published) | UNKNOWN | UNKNOWN (no official paper page yet) | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title keywords GPU + kernel + microarchitecture-aware mapping: GPU-accelerated homomorphic encryption with kernel-boundary fusion. Abstract not yet public, so centrality of the GPU mechanism is inferred from the title only |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| OptiPrime: Optimizing Private Inference through Protocol-Hardware Codesign | No GPU keyword; described by its authors as a privacy-preserving AI **accelerator** (protocol–hardware co-design), not a GPU paper. No abstract public to check for a GPU-specific mechanism. |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| (none) | Cannot be determined — no population and no abstracts are public. This section will be empty until the MICRO-59 main program is released. |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| Attention, Watch Your Progress: Balancing Warp Specialized GPU Pipelines | `NOT_FOUND` — no web result for this exact title. Searches returned only unrelated warp-specialization material (Tawa, WASP/HPCA 2024, PyTorch blog, FlashAttention work). Cannot be confirmed or refuted while no MICRO-59 program exists. |
| Ray-by-Ray: Fine-Grained Resource Management for GPU Ray Tracing Units | `NOT_FOUND` — no web result for this exact title. Searches returned only MICRO-57's "Extending GPU Ray-Tracing Units…" and MICRO-58's "RayN…". |
| Make Every Batch Count: Fault Entry Merging for Efficient Batching in Unified Virtual Memory | `NOT_FOUND` — no web result for this exact title. Searches returned only prior UVM batching work (Kim et al., ASPLOS'20 "Batch-Aware Unified Memory Management in GPUs for Irregular Workloads") and NVIDIA UVM documentation. |
| Complex Tensor Core: Software-Hardware Co-Design for Accelerating Complex-Valued Neural Networks on GPUs | `NOT_FOUND` — no web result for this exact title. Searches returned only MICRO-52's "Sparse Tensor Core" and vendor Tensor Core material. |

All four MICRO 2026 seeds are `NOT_FOUND`. This is **not** a statement that they
are wrong: with no accepted-papers list, no proceedings, and no arXiv/author-page
trace, there is no source against which they could be verified. They must be
re-checked once the MICRO-59 program is published.

Conversely, the one MICRO-59 GPU paper that **is** publicly attested — *Helios:
Melting Kernel Boundaries for GPU-Accelerated HE…* — does not appear in the seed
list.

## 6. Unresolved / blocked items

- **Primary blocker:** MICRO-59's main program / accepted-papers list is not public as of 2026-09-18. `census_status: PARTIAL_CENSUS`. Re-run after the program is posted (camera-ready was 2026-09-11; conference is 2026-10-31 → 2026-11-04).
- `https://www.microarch.org/micro59/program/` and `.../program/program.php` serve **stale MICRO-58 content**; do not use them for MICRO-59. `.../program/main-program.php` and `.../program/workshops.php` return 404 on the ACM-hosted mirror / main site respectively.
- dblp.org is robots-disallowed for fetching; dl.acm.org returns 403 — no bibliographic-index or publisher cross-check available.
- Full author lists, sessions, DOIs, full texts and artifacts for OptiPrime and Helios are all `UNKNOWN`; only the paper leads named on the author's news page are recorded.
- No officially stated MICRO-59 submission or acceptance count was found anywhere.

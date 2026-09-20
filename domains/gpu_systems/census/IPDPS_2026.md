# IPDPS 2026 — GPU Census

census_status: `PARTIAL_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **101** — *third-party attested only, no official statement located* |
| counted items excluded from population | **workshops: 18** (the official IPDPS 2026 announcement PDF is titled "ANNOUNCING 18 WORKSHOPS AT IPDPS 2026", https://www.ipdps.org/ipdps2026/ACM-final-ad-Dec2025.pdf); **keynotes: 3** (Vishkin, Kim, Bahar — anchor links on the official home page); **all-conference panel: 1** ("How Long Should a Supercomputer Live?"); tutorials, PhD Forum, posters and the Industry-Research Participation track all exist as separate official pages (https://www.ipdps.org/ipdps2026/2026-tutorials.html, .../2026-phd-forum.html, .../2026-industry.html) — **per-class counts UNKNOWN** because the detailed program host is unreachable |
| population source (primary) | https://openaccept.org/c/sys/ipdps/ — "434 submissions / 101 accepted / 23.27%" — `search-engine` (third-party statistics aggregator) |
| population source (corroborating) | (a) https://csconfstats.xoveexu.com/conferences/ipdps/ — "Submissions 434 / Accepted 101 / 23.3%" — `search-engine`; (b) https://www.ipdps.org/ipdps2026/2026-advance-program.html — official, confirms the conference structure and that the main-conference program is hosted off-site, but **contains no paper titles and no counts** — `official-program` |
| source class | `search-engine` (primary + corroborating a); `official-program` (corroborating b, structural only) |
| enumeration completeness | `UNVERIFIED_TOTAL` |
| paper-type mixing notes | Cannot be assessed. The only host of the IPDPS 2026 main-conference session/paper listing is the Linklings program site, which is unreachable (see §6). The official advance-program page explicitly defers to it: "The detailed Main Conference program is available here". |

### 1.1 Population evidence notes

- **No paper-by-paper enumeration of the IPDPS 2026 main conference was obtained.** The count of 101 rests on two independent third-party aggregators that agree exactly (434 / 101 / ~23.3%). Both aggregators also agree exactly with the *officially attested* counts for 2024 (88) and 2025 (105), which is the reason they are treated as usable corroboration here rather than discarded.
- **No official IPDPS 2026 acceptance statistic was located.** The pattern used for 2024 and 2025 — an official post-conference report on `ipdps.org/ipdps<year>/index.html` carrying the sentence "N contributed papers selected for presentation in M technical sessions" — has not (as of 2026-09-18) been published for 2026: `https://www.ipdps.org/ipdps2026/` still serves the pre-conference page (keynotes, awards, registration) and states no counts.
- Conference dates and identity confirmed officially: **40th IPDPS, 25–29 May 2026, Marriott on Canal Street, New Orleans, LA** (official advance-program page; corroborated by https://computing.llnl.gov/about/newsroom/ipdps-2026 and by the Zenodo artifact record 10.5281/zenodo.18716313).
- **The count 101 was not invented and is not presented as official.** It is tagged `search-engine` / `UNVERIFIED_TOTAL`.

## 2. Broad GPU candidates (STEP B)

**Screening scope warning — read before use.** Unlike the 2024 and 2025 sheets,
screening for 2026 was **NOT** applied over a reconstructed population: no
population listing exists in this sheet. The candidates below were found by
targeted resolution of the seed list plus author-page and preprint sweeps.
The set is therefore a **lower bound**, not a screened census. Session names
are `UNKNOWN` throughout because the program host is unreachable.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis | Aaron Jarmusch, Sunita Chandrasekaran (Univ. of Delaware) | UNKNOWN | UNKNOWN (artifact DOI 10.5281/zenodo.18716313) | https://www.ipdps.org/ipdps2026/2026-advance-program.html (detailed program unreachable) | https://arxiv.org/abs/2512.02189 | https://github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark and https://zenodo.org/records/18716313 | Microbenchmark suite for the NVIDIA Blackwell **B200** vs **H200**: memory subsystem, Tensor Core pipelines, FP precisions, energy efficiency. Core GPU microarchitecture-characterisation paper |
| 2 | From Skew to Symmetry: Node-Interconnect Multi-Path Balancing with Execution-time Planning for Modern GPU Clusters | Jinghan Yao, Kaushik Kandadi Suresh, Bharath Ramesh, Hari Subramoni, Dhabaleswar K. Panda (OSU NOWLAB) | UNKNOWN | UNKNOWN | https://nowlab.cse.ohio-state.edu/publications/ | https://arxiv.org/abs/2604.00317 | NOT_FOUND_AFTER_SEARCH | "Modern GPU Clusters" in title; runtime (named **NIMBLE**) rebalances intra-node and inter-node link utilisation, **CUDA-aware RDMA** pipelining, compared against **NCCL** and MPI/UCX. GPU communication mechanism |
| 3 | Design and Implementation of Casting Compression for GPU-Aware MPI Collectives | Chen Chen, Nick Contini, L. Xu, J. Queiser, Hari Subramoni, Dhabaleswar K. Panda (OSU NOWLAB) | UNKNOWN | UNKNOWN | https://nowlab.cse.ohio-state.edu/publications/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU-Aware MPI Collectives" + `compression` in title; on-the-fly casting compression inside GPU-aware collectives. GPU communication mechanism |
| 4 | One Memory-Many Paths: Early Experiences with Allocation and Data Copy Strategies on MI300A | Goutham Kuncham, S. Zhang, Dhabaleswar K. Panda (OSU NOWLAB) | UNKNOWN — **Best Paper Finalist** (per source) | UNKNOWN | https://nowlab.cse.ohio-state.edu/publications/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | **MI300A** in title; unified-memory allocation and data-copy strategies on an AMD APU. GPU memory mechanism |
| 5 | Design and Implementation of Multi-Rail-Aware Hierarchical MPI Reduce-Scatter and Allgather Operations | Chen Chen, Jinghan Yao, Dhabaleswar K. Panda (OSU NOWLAB) | UNKNOWN | UNKNOWN | https://nowlab.cse.ohio-state.edu/publications/ | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | `multi-rail` + `collective` keywords; hierarchical multi-rail collectives from the group whose 2026 companion papers are all GPU-aware. `TITLE_ONLY` — GPU residency not independently confirmed |
| 6 | The Big Send-off: Scalable and Performant Collectives for Deep Learning | Siddharth Singh, Keshav Pradeep, Mahua Singh, Cunyang Wei, Abhinav Bhatele (Univ. of Maryland) | UNKNOWN | UNKNOWN | https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026a.pdf | https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026a.pdf (also earlier preprint https://arxiv.org/abs/2504.18658, under the earlier title "The Big Send-off: High Performance Collectives on GPU-based Supercomputers") | NOT_FOUND_AFTER_SEARCH | `collective` keyword; the same work's earlier title names "GPU-based Supercomputers" explicitly. GPU collective-communication mechanism |
| 7 | The Case of the Elusive Application Performance on Production GPU Supercomputers | Cunyang Wei, Keshav Pradeep, Abhinav Bhatele (Univ. of Maryland) | UNKNOWN | UNKNOWN | https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf | https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf | NOT_FOUND_AFTER_SEARCH | "Production GPU Supercomputers" in title; application-performance characterisation on production GPU systems. GPU performance/telemetry mechanism |
| 8 | Characterizing Production GPU Workloads using System-wide Telemetry Data | Onur Cankur, Brian Austin, Dhruva Kulkarni, Abhinav Bhatele | UNKNOWN | UNKNOWN | https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026c.pdf | https://arxiv.org/abs/2502.18680 and https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026c.pdf | NOT_FOUND_AFTER_SEARCH | "Production GPU Workloads" + `telemetry` in title. GPU telemetry mechanism |
| 9 | SMART-MIG: A Learning Framework for Scalable and Energy-Efficient GPU Scheduling | Wenqing Yu, Neel Karia, Tanvi Hisaria, Clifford Stein, Olivier Tardieu, Asser Tantawi (IBM Research / Columbia) | UNKNOWN | UNKNOWN | https://research.ibm.com/publications/smart-mig-a-learning-framework-for-scalable-and-energy-efficient-gpu-scheduling | https://arxiv.org/abs/2606.29775 | NOT_FOUND_AFTER_SEARCH | "GPU Scheduling" in title; **MIG** repartitioning + energy-aware scheduling. GPU partitioning/power mechanism. Venue confirmed by both sources ("Accepted at the 40th IEEE IPDPS (IPDPS 2026)") |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

Only items independently confirmed as IPDPS 2026 main-conference papers are
listed. This section is **not** a complete keyword sweep of the population,
because the population is not enumerated.

| Title | Why not a GPU candidate |
|---|---|
| High-Performance Vector-Length Agnostic Quantum Circuit Simulations on ARM Processors (Pei-Hung Lin, Maya Gokhale, LLNL; https://computing.llnl.gov/about/newsroom/ipdps-2026) | `SIMT`/vector-adjacent keywords; the target is explicitly **ARM CPU** SVE-style vector hardware, not a GPU |
| Quantifying the Impact of Lossy Compression on Neural Generative Surrogate Modeling (Harshitha Menon, Charles Jekel, Peter Lindstrom, LLNL; same source) | `compression` keyword; a compression-vs-model-accuracy study; no GPU term in the title and no abstract reachable to establish GPU residency (see §6) |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| The Big Send-off: Scalable and Performant Collectives for Deep Learning | The same work's earlier preprint title is "…High Performance Collectives on **GPU-based Supercomputers**" (https://arxiv.org/abs/2504.18658), so the retitled IPDPS 2026 version is the GPU-collectives contribution |
| From Skew to Symmetry: … for Modern GPU Clusters | (GPU *is* in the title, but the mechanism is not obvious from it) abstract names **CUDA-aware RDMA**, intra/inter-node path balancing, and comparison against **NCCL** |
| One Memory-Many Paths: Early Experiences with Allocation and Data Copy Strategies on MI300A | "MI300A" is the AMD Instinct APU; the contribution is host/device allocation and copy-path selection under unified memory |
| Design and Implementation of Multi-Rail-Aware Hierarchical MPI Reduce-Scatter and Allgather Operations | `multi-rail`/`collective` keywords only. `TITLE_ONLY` — held as a candidate for review, GPU residency unconfirmed |
| SMART-MIG: A Learning Framework for Scalable and Energy-Efficient GPU Scheduling | (GPU in title) the mechanism is **MIG** repartitioning — a GPU hardware-partitioning feature |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| Microbenchmarking NVIDIA's Blackwell Architecture | `TITLE_CORRECTED_TO:` **Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis** — CONFIRMED_IN_POPULATION (arXiv 2512.02189; author's presentation deck https://ajarmusch.github.io/slides/blackwell-ipdps-2026.pdf states "IPDPS, May 25–29 2026, New Orleans"; Zenodo artifact record names the 40th IEEE IPDPS). *Note:* the slide deck spells the subtitle "An in-depth Architecture Analysis"; arXiv and Zenodo both use "Architectural". The arXiv/Zenodo form is used above |
| NIMBLE and/or "From Skew to Symmetry" | Split resolution. **"From Skew to Symmetry"** → `TITLE_CORRECTED_TO:` **From Skew to Symmetry: Node-Interconnect Multi-Path Balancing with Execution-time Planning for Modern GPU Clusters** — CONFIRMED_IN_POPULATION (listed under the 40th IEEE IPDPS, May 2026, on the OSU NOWLAB publications page). **"NIMBLE"** → `NOT_IN_MAIN_POPULATION`: NIMBLE is (a) the *system name* inside "From Skew to Symmetry" (per the arXiv abstract) and (b) the title of a **separate ISC High Performance 2026 research poster**, "NIMBLE: Node-Interconnect Multi-Path Balancing with On-the-fly Orchestration for High Bandwidth GPU Clusters" — not an IPDPS 2026 main-conference paper |
| "The Big Send-off" and/or PCCL | **"The Big Send-off"** → `TITLE_CORRECTED_TO:` **The Big Send-off: Scalable and Performant Collectives for Deep Learning** — CONFIRMED_IN_POPULATION (official author PDF at `…/pubs/pdf/2026/ipdps2026a.pdf`, listed as IPDPS 2026). **"PCCL"** → `NOT_FOUND`: no IPDPS 2026 paper named PCCL was located. Searches surfaced only unrelated PCCL works (ICCD 2024 "PCCL: Energy-Efficient LLM Training with Power-Aware Collective Communication"; arXiv 2509.15450 "PCCL: Photonic circuit-switched collective communication"; Prime Intellect's "Prime Collective Communications Library") — **none at IPDPS 2026** |
| Characterizing Production GPU Workloads using System-wide Telemetry Data | CONFIRMED_IN_POPULATION — verbatim title; Cankur, Austin, Kulkarni, Bhatele; official author PDF `…/pubs/pdf/2026/ipdps2026c.pdf`; preprint arXiv 2502.18680 |
| The Case of the Elusive Application Performance on Production GPU Supercomputers | CONFIRMED_IN_POPULATION — verbatim title; Wei, Pradeep, Bhatele; official author PDF `…/pubs/pdf/2026/ipdps2026b.pdf` |
| a Tensor-Core SpGEMM paper | `NOT_FOUND`. Two targeted searches for a Tensor-Core SpGEMM/SpMM paper at IPDPS 2026 returned only prior-venue works (PPoPP 2025 Acc-SpMM, ASPLOS 2024 DTC-SpMM, SC 2025, and a 2020 journal paper). **Caveat:** absence here is weak evidence — the IPDPS 2026 population is not enumerated, so such a paper could exist unlisted |
| Casting Compression for GPU-Aware MPI | `TITLE_CORRECTED_TO:` **Design and Implementation of Casting Compression for GPU-Aware MPI Collectives** — CONFIRMED_IN_POPULATION (OSU NOWLAB publications page, 40th IEEE IPDPS, May 2026); authors C. Chen, N. Contini, L. Xu, J. Queiser, H. Subramoni, D. K. Panda |
| "One Memory, Many Paths" / MI300A | `TITLE_CORRECTED_TO:` **One Memory-Many Paths: Early Experiences with Allocation and Data Copy Strategies on MI300A** (official listing uses a hyphen, "One Memory-Many Paths", not "One Memory, Many Paths") — CONFIRMED_IN_POPULATION; G. Kuncham, S. Zhang, D. K. Panda; marked **Best Paper Finalist** on the OSU NOWLAB publications page |
| SMART-MIG | `TITLE_CORRECTED_TO:` **SMART-MIG: A Learning Framework for Scalable and Energy-Efficient GPU Scheduling** — CONFIRMED_IN_POPULATION; Wenqing Yu, Neel Karia, Tanvi Hisaria, Clifford Stein, Olivier Tardieu, Asser Tantawi; both IBM Research's publication page and arXiv 2606.29775 state acceptance at the 40th IEEE IPDPS (IPDPS 2026) |

### 5.1 Candidates the seed list did not contain

| Title | Source |
|---|---|
| Design and Implementation of Multi-Rail-Aware Hierarchical MPI Reduce-Scatter and Allgather Operations — C. Chen, J. Yao, D. K. Panda | https://nowlab.cse.ohio-state.edu/publications/ (40th IEEE IPDPS, May 2026) |

## 6. Unresolved / blocked items

- **`census_status: PARTIAL_CENSUS`. Exactly what is missing: the IPDPS 2026 main-conference paper list.** No session listing and no paper titles were obtained from any source. Every access route was tried and failed:
  - `https://ssl.linklings.net/conferences/ipdps/ipdps2026_program/` and `.../views/at_a_glance.html` → **ROBOTS_DISALLOWED**. The whole host is disallowed: even `https://ssl.linklings.net/robots.txt` returns ROBOTS_DISALLOWED. This is the *only* host of the detailed program, and the official advance-program page defers to it.
  - `https://ieeexplore.ieee.org/xpl/conhome/1000178/all-proceedings` → **HTTP 418**.
  - `https://dblp.org/db/conf/ipps/ipps2026.html`, `https://dblp.uni-trier.de/db/conf/ipps/ipps2026.html`, `https://dblp.dagstuhl.de/db/conf/ipps/ipps2026.html` → **ROBOTS_DISALLOWED**.
  - `https://web.archive.org/web/2026/https://ssl.linklings.net/...` → **SITE_BLOCKED**.
  - `https://www.ipdps.org/ipdps2026/2026-program.html` → **404**; `https://www.ipdps.org/ipdps2026/2026-advance-program.html` → 200 but contains **no titles and no counts** (verified twice with different prompts).
  - `dl.acm.org` → 403; crossref / OpenAlex / Semantic Scholar APIs → 429 through this proxy.
- **Consequence for STEP B:** §2 is a **lower bound of 9 candidates**, produced by seed resolution plus author-page sweeps (OSU NOWLAB, UMD/Bhatele, IBM Research, LLNL) and preprint search — *not* by screening a population. Roughly 101 main-conference papers exist; ~90 of them were never seen. §3 is likewise incomplete by construction.
- **Sessions: UNKNOWN for every candidate** (program host unreachable). **Per-paper DOIs: UNKNOWN for every candidate** (IEEE Xplore 418; dblp robots-disallowed). The only DOI recorded is the Blackwell paper's *artifact* DOI, 10.5281/zenodo.18716313.
- **Official URLs** in §2 are author/institution pages and the official conference advance-program page, because no official per-paper page is reachable.
- **Official acceptance statistic for 2026: not located.** The 434/101/23.3% figures are third-party (two agreeing aggregators). An official post-conference report of the kind published for 2024 and 2025 had not appeared on `ipdps.org` as of 2026-09-18.
- **Excluded-class counts** beyond workshops (18) and keynotes (3) are **UNKNOWN**: poster count, PhD Forum count, tutorial count and industry-track count are all published only in the unreachable detailed program.
- Title-match note for the Blackwell paper: arXiv's markdown conversion strips the Title:/Authors: block, so the match was made on abstract content ("microbenchmark suite … B200 … H200 … tensor core pipelines") plus the author's own IPDPS 2026 slide deck and the Zenodo artifact record; the author names above come from those pages, not from the stripped arXiv header.

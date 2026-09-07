# V2 — SC26 / ORNL "From Alert Fatigue to Root Cause" verification

**Audit date:** 2026-09-06
**Auditor constraint:** WebSearch + WebFetch only. No curl/wget/scripted fetching. ACM DL / IEEE Xplore not attempted (known 403).
**Overall status of the primary target:** `SC26-PARTIAL-EVIDENCE` — the paper is **confirmed to exist and to be an SC26 Technical Papers submission**, but **no abstract or full text is public as of 2026-09-06**. Every content question below is `UNKNOWN`.

---

## 0. State of the SC26 program as of 2026-09-06

| Fact | Evidence | Depth |
|---|---|---|
| `https://sc26.conference-program.com/` returns **HTTP 401** (site not yet open to the public). Also tried the institution-hash form `?searchby=institution&institution=16969005850305409037` → **401**. Not indexed by search engines (`site:sc26.conference-program.com` returns zero results from that host). | direct fetch, 2026-09-06 | verified |
| Therefore the `Event Type:` / `Tracks:` structured-metadata method **cannot be used yet**. There is no per-presentation program metadata available for SC26. | — | verified |
| SC26 papers page: "Day, time, and location for each paper session will be published in the online SC Schedule by September 2026." | https://sc26.supercomputing.org/program/papers/ | `PROGRAM-METADATA-ONLY` |
| SC26 dates page lists **16 SEP 2026 — "Content/Schedule"** (appears in the Posters block of the dates table; poster notifications 9 SEP 2026). This is the nearest published date on which schedule content is expected. | https://sc26.supercomputing.org/all-dates-deadlines/ | verified |
| Proceedings: "(Available November 2026)" for both Technical Program Publications and Technical Program Archives; archived in ACM DL and IEEE Xplore, with ACM OpenTOC free access. | https://sc26.supercomputing.org/program/proceedings-archives/ | verified |
| Papers timeline: notifications 1 JUL 2026; final paper due 28 AUG 2026; artifact freeze 25 AUG 2026; presentations Tue–Thu 17–19 Nov 2026. | https://sc26.supercomputing.org/program/papers/ | verified |
| **The full SC26 accepted-Technical-Papers list is NOT public as of 2026-09-06.** The only publicly enumerated subset is the 9 Best Paper / Best Student Paper finalists. | see §2 | verified |
| Technical Papers topic areas (verbatim, 10): "Algorithms"; "Applications"; "Architecture & Networks"; "Data Analytics, Visualization, & Storage"; "HPC for Machine Learning"; "Performance Measurement, Modeling, & Tools"; "Post-Moore & Quantum Computing"; "Programming Frameworks"; "State of the Practice"; "System Software & Cloud Computing". Confirms **"State of the Practice" is a topic area inside Technical Papers, not a separate track.** | https://sc26.supercomputing.org/program/papers/ | verified |

---

## 1. PRIMARY TARGET — ORNL paper

### 1.1 Existence and exact title — `CONFIRMED`

**The paper exists.** Exact full title, verbatim from two independent sources:

> **"From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System"**

Note the title ends **"in HPC System"** (singular, no article) — this is what both sources print. Do not "correct" it to "Systems" when citing.

Sources:
- https://sc26.supercomputing.org/2026/08/announcing-best-paper-and-best-student-paper-finalists/
- https://www.hpcwire.com/off-the-wire/sc26-announcing-best-paper-and-best-student-paper-finalists/ (independent mirror, identical string)

Evidence depth: **`TITLE-ONLY`** (title + authors + affiliation + award-nomination status). No abstract anywhere.

### 1.2 Authors and affiliations — `CONFIRMED`

Verbatim, in printed order:

1. Awais Khan
2. Christopher Zimmer
3. Anjus George
4. Ahmad Maroof Karimi
5. Feiyi Wang
6. Woong Shin

Affiliation printed for all: **Oak Ridge National Laboratory, USA** (single affiliation; no external collaborators listed).

Evidence depth: `TITLE-ONLY` / author metadata from the SC26 announcement. Confirmed identically on HPCwire.

### 1.3 Event type / track — `CONFIRMED as Technical Papers`

- The paper appears under the heading **"Best Paper Nominees"** on the SC26 Best Paper / Best Student Paper finalists announcement.
- That announcement is explicitly scoped to the Technical Papers program: "Each year, the SC Technical Papers program recognizes outstanding research through its Best Paper and Best Student Paper awards."
- Nominations are described as arising "within technical areas during review discussions", i.e. from the Technical Papers topic areas.

**Verdict: Technical Papers (Event Type would be `Paper`). It is NOT a workshop paper, BoF, or poster.** This is a strong inference from the award mechanism, not from an `Event Type:` metadata line — the program site is still 401. Label: `PROGRAM-METADATA-ONLY (award-list level)`.

- **Which topic area?** `UNKNOWN`. Plausible candidates exist ("State of the Practice", "System Software & Cloud Computing", "Data Analytics, Visualization, & Storage") but the announcement does not name the nominating area. Not inferred.
- **Which session, day, time?** `UNKNOWN` — schedule not published.

### 1.4 Identifiers and preprints

| Item | Status |
|---|---|
| DOI | `NOT FOUND` / does not yet exist. Crossref query (`api.crossref.org`, bibliographic query on the exact title) returned **no match**; nearest hits were unrelated 2010–2025 works. Consistent with proceedings not appearing until November 2026. |
| Page numbers | `UNKNOWN` — proceedings not published. |
| arXiv preprint | `NOT FOUND` as of 2026-09-06. Multiple targeted searches on the exact title, on "Causal Failure Cascade Discovery", and on author combinations returned only unrelated microservice/cloud RCA papers. |
| OSTI deposit | `NOT FOUND`. osti.gov search is robots-blocked to WebFetch; searched via WebSearch with author names and title fragments — no OSTI record surfaced. An OSTI/ORNL deposit is **plausible but unverified**. |
| ORNL staff-profile publication lists | Checked https://www.ornl.gov/staff-profile/anjus-george and https://www.ornl.gov/staff-profile/ahmad-maroof-karimi — most recent entries are June 2025; **no 2026 entries at all**. Profiles lag; no content available there. |
| ORCID (Awais Khan, 0000-0003-2603-3516) | Public HTML profile is JS-rendered and returned no work list to WebFetch; `pub.orcid.org` API is robots-disallowed to WebFetch. `NOT RETRIEVED`. |
| ORNL / OLCF news release about the nomination | `NOT FOUND` as of 2026-09-06. |

### 1.5 Content questions — ALL `UNKNOWN`

No abstract, no preprint, no full text, no artifact description is public. I am recording explicit `UNKNOWN` rather than inferring anything from the title.

| Question | Answer | Basis |
|---|---|---|
| Label source — single or multiple combined? | **UNKNOWN** | no abstract |
| **Does it measure agreement/disagreement BETWEEN label sources** (alarms vs Slurm drain reason vs health checks vs tickets vs RMA)? | **UNKNOWN — cannot be determined from public materials** | no abstract |
| Root-cause taxonomy? How many classes? | **UNKNOWN** | no abstract |
| Number of operator-confirmed labels / incidents? | **UNKNOWN** | no abstract |
| Does it vary telemetry resolution / sampling rate / data volume? | **UNKNOWN** | no abstract |
| How many telemetry layers? | **UNKNOWN** | no abstract |
| Offline replay vs online deployment? | **UNKNOWN** | no abstract |
| Public artifact / dataset? | **UNKNOWN.** SC26 required an AD (Artifact Description) appendix (mandatory, due 28 APR 2026) and an artifact freeze deadline of 25 AUG 2026, so an AD appendix almost certainly exists — but whether the artifact is *public* is unknown, and the appendix itself is not published until the proceedings. | https://sc26.supercomputing.org/program/papers/ |
| Which system(s) — Frontier, Summit, etc.? | **UNKNOWN.** Author group is OLCF-side, but the title/announcement names no machine. Not inferred. |

**What the title alone licenses:** the words "Causal", "Failure Cascade", "Discovery", and "Alert Fatigue" are in the title. That is a lexical fact about the title, not evidence about method, data, labels, or evaluation. It does **not** establish that the paper does causal discovery on telemetry, nor that it uses alarms as labels, nor anything about label provenance.

### 1.6 Useful non-content context (verified, adjacent)

- **Woong Shin (ORNL), last author, is a co-organizer of the SC26 HPC-ODA workshop** ("1st International Workshop on HPC Operational Data Analytics", 20 Nov 2026), alongside Michael Ott (LRZ), Ayse Coskun (BU), Jeff Hanson (HPE), Melissa Romanus (NERSC/LBNL), Tim Osborne (ORNL). Source: https://hpc-oda.org/workshop2026/ — verified.
- Prior related-looking ORNL work by an overlapping author set exists (e.g. Anjus George's profile lists "From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments…", Nov 2024, conference paper). **This is prior work, not the SC26 paper, and says nothing about the SC26 paper's content.** Listed only as a lead for later reading.

---

## 2. Does it threaten a "label source disagreement measurement" research idea?

### **CANNOT DETERMINE**

Reasoning, grounded only in verified evidence:

- **What is verified:** the paper exists, is ORNL-authored by an OLCF operations/data group, is a Technical Papers Best Paper nominee, and is titled "From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System".
- **What is not verified:** anything about its label sources, whether it uses more than one label source, and whether it quantifies agreement between label sources. There is no abstract, preprint, or artifact description in public as of 2026-09-06.
- Consequently the threat cannot be graded either way. The honest position is neither "safe" nor "scooped".

**Risk posture I would recommend (judgement, flagged as such, not evidence):** treat this as an **elevated-but-unquantified** risk and do not commit the research framing until the abstract is readable. Two facts raise the prior enough to warrant a hard gate: (a) the author set is exactly the ORNL group that owns OLCF operational telemetry and would have access to alarms, Slurm state, health checks, and tickets simultaneously; (b) "Alert Fatigue" in the title indicates the paper's framing starts from alarm-stream quality, which is the same neighbourhood as label-source reliability. Neither fact shows the paper *measures inter-source disagreement*. A causal-cascade-discovery paper can perfectly well use a single label source and never compute cross-source agreement — that is the common case in this literature. **Do not write it off, and do not concede it.** Re-grade on 16 SEP 2026 (see §5).

---

## 3. SC26 operations-relevant papers table

**Coverage warning:** the full SC26 Technical Papers accepted list is **not public** on 2026-09-06. The table below is therefore **not** a filtered view of the accepted set — it is the *complete* publicly enumerable set of SC26 Technical Papers (the 9 award finalists), with the operations-relevance column applied. Any operations-relevant SC26 paper that was not award-nominated is currently invisible.

### 3.1 All publicly known SC26 Technical Papers (award finalists)

Source for all rows: https://sc26.supercomputing.org/2026/08/announcing-best-paper-and-best-student-paper-finalists/ (mirrored at HPCwire). Depth for all rows: `TITLE-ONLY`. Event type for all rows: **Technical Papers**.

| # | Category | Title (verbatim) | Authors | Affiliations | Ops-relevant? |
|---|---|---|---|---|---|
| 1 | Eligible for either award | Sensor Placement for Tsunami Early Warning via Large-Scale Bayesian Optimal Experimental Design | Sreeram Venkat, Omar Ghattas, Stefan Henneking | University of Texas at Austin, USA | No |
| 2 | Eligible for either award | Format-Driven Automatic Pipeline Construction and Load Balancing for SpMM on GPUs | Kelun Lei, Hailong Yang, Kaige Zhang, Zhongzhi Luan, Kejie Ma, Tianyu Feng, Xin You, Yi Liu, Depei Qian, Da Huo | Beihang University, China | No |
| 3 | Eligible for either award | Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives | Jeff R. Hammond, Torsten Hoefler, Anton Korzh, John Bachan, Siyuan Shen, Nishank Chandawala, Tiancheng Chen, Kamil Iskra, Sylvain Jeaugey, Arnav Goel, Zhenhao He | NVIDIA Corporation (Finland/USA/France/Switzerland); ETH Zürich, Switzerland | No (interconnect perf, not ops) |
| 4 | Best Student Paper nominee | Do We Need Tensor Cores for Stencil Computations? | Qiqi Gu, Haibing Guan, Chenpeng Wu, Jianguo Yao, Heng Shi | Shanghai Jiao Tong University, China; Shanghai Enflame Intelligence Technologies Co. Ltd, China | No |
| 5 | Best Student Paper nominee | DOLPHIN: Scalable Disk–RAM–GPU Pipelined Training for Massive Temporal GNNs | Wenbo Zhen, Jianliang Xu, Xike Xie, Rui Guo, Zezhong Ding, Junlin Lv | University of Science and Technology of China, China; Hong Kong Baptist University, Hong Kong | No |
| 6 | Best Paper nominee | FSZ: Breaking the Prediction-Throughput Trade-off in GPU Lossy Compression | Jiajun Huang | University of South Florida, USA | No |
| 7 | Best Paper nominee | **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** | Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin | Oak Ridge National Laboratory, USA | **YES — primary target** |
| 8 | Best Paper nominee | DySpin: A Plug-and-Play Library Advancing Dynamic Sparse Long-Context Inference | Chengyu Sun, Dazhao Cheng, Xiaobo Zhou, Yaqi Xia, Donglin Yang, Ruirui Pan | Wuhan University, China; University of Macau, China; NVIDIA Corporation, USA; Central China Normal University, China | No |
| 9 | Best Paper nominee | SwarmLoRA: Batched Computation across Isolated Functions for Serverless LoRA Inference | Mausam Basnet, Tong Shu | University of North Texas, USA | No |

**Net: exactly one operations/AIOps-relevant paper is publicly known in the SC26 Technical Papers program, and it is the ORNL target.** No other monitoring / telemetry / reliability / anomaly-detection / power / cooling / scheduling-analytics Technical Paper can be confirmed or ruled out yet.

### 3.2 SC26 workshops that will carry operations-relevant content (context, not Technical Papers)

Verified from the SC26 accepted-workshops announcement (https://sc26.supercomputing.org/2026/04/a-gold-standard-sc26-welcomes-50-workshops-to-chicago/ — 50 workshops; 43 with proceedings, 8 symposium-style):

| Workshop | Relevance | Accepted list public? |
|---|---|---|
| **Workshop on Operational Data Analytics in HPC (HPC-ODA)** — "1st International Workshop on HPC Operational Data Analytics", Fri 20 Nov 2026, 08:30–12:30 | **Highest** — direct ops/telemetry venue. Organizers: Michael Ott (LRZ), Ayse Coskun (BU), Jeff Hanson (HPE), Melissa Romanus (NERSC/LBNL), Woong Shin (ORNL), Tim Osborne (ORNL). Notifications were 4 SEP 2026; camera-ready 18 SEP 2026. | **No** (checked 2026-09-06, https://hpc-oda.org/workshop2026/) |
| **The 1st International Workshop on Edge-Cloud-HPC Operational Continuum (ECHO)** | High — operational continuum | Not checked in depth |
| **HPC Systems Professionals Workshop (HPCSYSPROS26)** | High — sysadmin / operations practice | Not checked |
| **FTXS: Workshop for Faults, Trustworthiness, and eXplainability for AI Systems at Scale** | High — faults/resilience | Not checked |
| **HUST-26: 13th International Workshop on HPC User Support Tools** | Medium — tickets/user support | Not checked |
| **Sustainable Supercomputing**; **EESP 2026** (Energy Efficiency with Sustainable Performance); **RISE 2026** | Medium — power/energy/cooling | Not checked |
| **AgenticAI4HPC'26** | See §4 | No |
| **PDSW'26**, **ROSS 2026**, **PMBS26**, **ProTools**, **HPCTESTS 2026** | Adjacent (storage, OS, perf modeling, tools, system testing) | Not checked |

---

## 4. AgenticAI4HPC 2026 status

**Verdict: CONFIRMED happening. Accepted-paper list NOT public as of 2026-09-06.**

| Item | Value | Source / depth |
|---|---|---|
| Full name | "AgenticAI4HPC'26: The First International Workshop on Agentic AI for HPC" (site: "The 1st International Workshop on Agentic AI for HPC") | SC26 workshops announcement + https://ornl.github.io/events/agenticai4hpc2026/ — verified |
| Officially accepted by SC26 | **Yes** — appears in the SC26 list of 50 accepted workshops, in the 43 "with proceedings" group | https://sc26.supercomputing.org/2026/04/a-gold-standard-sc26-welcomes-50-workshops-to-chicago/ — verified |
| Edition | 1st (first edition) — confirms the user's belief | verified |
| Date / time | Sunday 15 November 2026, 09:00–12:30, Chicago | verified |
| Organizers | Mohammad Alaul Haque Monil (Chair, ORNL); Pedro Valero-Lara (Co-Chair, ORNL); Daichi Mukunoki (Co-Chair, Nagoya University, Japan); Bogdan Nicolae (Co-Chair, ANL) | verified |
| Key dates | Submission 10 AUG 2026 (AoE); **Acceptance 4 SEP 2026 (AoE)**; Camera-ready 25 SEP 2026; workshop 15 NOV 2026. Site states "Submissions are closed." | verified |
| Proceedings | "Accepted papers will be published in the IEEE Digital Library as part of the workshop proceedings of SC 2026." | verbatim, verified |
| Accepted-paper list | **NOT PUBLIC.** Only a *tentative* agenda with unnamed slots: 9:00–9:05 Opening; 9:05–9:40 Invited Talk 1 (Ali Jannesari) "From Code Generation to Performance Reasoning — Agentic AI for the Autonomous HPC Stack"; 9:40–10:00 "Paper Presentation 1"; 10:00–10:30 break; 10:30–11:05 Invited Talk 2 (Abhinav Bhatele) "Agentic Approaches to Generate and Optimize Parallel Code"; 11:05–12:20 "Paper Presentations 2"; 12:20–12:30 Distinguished Paper Recognition and Closing. **No paper titles or authors.** Acceptances were sent only 2 days ago (4 SEP). | verified, 2026-09-06 |
| Any HPC-operations agent benchmark? | **CANNOT DETERMINE** — no titles public. The CFP does include relevant scope: topic area 3 "Co-Design & Human–AI Collaboration in HPC" explicitly mentions **"facility operations"**, and topic area 4 is "Evaluation, Benchmarking & Reliability" (benchmarking methodologies, robustness assessment, real-world case studies). So an ops-agent benchmark is **in scope and solicited**, but none is confirmed. | verified (CFP text) |
| Slot capacity | The tentative agenda has room for roughly 5 paper slots (one at 9:40–10:00 plus a 75-minute block) — so the workshop is small; the accepted set is likely single-digit. Flagged as inference from slot arithmetic, not a stated count. | inference |

### 4.1 Adjacent check performed — AGENT4SC 2026 (NOT SC26)

Worth recording so it is not confused with AgenticAI4HPC: **AGENT4SC 2026, "1st Workshop on Agentic AI for Large-scale Science", is co-located with IEEE eScience 2026, not SC26** (organizers Amal Gueroudji, Bogdan Nicolae, Renan Souza; steering committee Rosa Filgueira, Rafael Ferreira da Silva, Kyle Chard, Patrick Widener). Its program **is** public (https://agent4sc.github.io/) with these papers:

- SPECTRA: Detecting Silent Failures in LLM Multi-Agent Systems via Dual-Layer Observability — Leonardo Militano, Thomas Michael Bohnert
- Beyond the Session Boundary: Three Traces of Provenance in an Agent-Mediated Science Deployment — Zhiwei Li, Carl Kesselman, Jayanth Kumar Mallapu, Benjamin Xu, Kyle Bolo
- Multi-Agent Discovery and Resource-Aware Autonomous Exploration of Scientific Datasets — Aashish Panta, Hugo Lee, Giorgio Scorzelli, Kyongsik Yun, Valerio Pascucci
- Beyond Tool Execution: Evaluating Scientific MCP Interfaces with UXarray — Rajeev Jain, Robert Jacob
- (lightning) System Software Patterns for Agentic Scientific Codes in 2025 — Robert Underwood, Bogdan Nicolae, Franck Cappello, Thorsten Hellert, Alex Hexemer, Amarjit Singh, Kento Sato, Yadu Nand Babuji, Ian Foster, Alok Kamatar, Kyle Chard
- (lightning) Keeping the Agent Out of the Hot Loop: A Deterministic Control Plane for DFT Workflows Across HPC Centers — Daniel Speckhard, Lucas Pinede, Sagar Pal, Ali Ramlaoui, Hannah Bull, Cory Hargus, Victor Schmidt, Alexandre Duval
- (lightning) A Reliable Closed-Loop Agent for Autonomous Center-of-Rotation Selection in Synchrotron Computed Tomography — Austin Yunker, Peter Kenesei, Hemant Sharma, Antonino Miceli, Ian Foster, Rajkumar Kettimuthu
- (lightning) QUANTA: Quantum Network AgenTic Arena — Pablo Cesar Bedolla Ortiz, Joaquin Chung, Ian Foster, Rajkumar Kettimuthu

**None of these is an HPC-operations agent benchmark.** Closest observability-flavoured item is SPECTRA, but it targets LLM multi-agent systems, not HPC facility operations. Depth: `TITLE-ONLY`.

---

## 5. When to re-check

| Date | What becomes available | Action |
|---|---|---|
| **~16 SEP 2026** (10 days out) | SC26 dates page lists "Content/Schedule" for 16 SEP 2026, and the papers page promises the online SC Schedule "by September 2026". Expect `sc26.conference-program.com` to stop returning 401 and to expose per-presentation pages with `Event Type:` and session-level `Tracks:` lines — **and, critically, abstracts.** | **Highest-priority re-check.** Fetch the ORNL paper's presentation page: confirm `Event Type: Paper`, capture the topic area, session name, and **the abstract**. The abstract is what will settle the label-source-disagreement question in §2. Also re-run the institution-hash filter `?searchby=institution&institution=16969005850305409037` to enumerate all ORNL SC26 content, and sweep the full Technical Papers list for the ops/telemetry/reliability/power/cooling filter that §3 could not apply. |
| ~18–25 SEP 2026 | HPC-ODA 2026 camera-ready is 18 SEP; lightning-talk notifications 25 SEP. AgenticAI4HPC camera-ready 25 SEP. Workshop sites typically post programs shortly after camera-ready. | Re-check https://hpc-oda.org/workshop2026/ and https://ornl.github.io/events/agenticai4hpc2026/ for accepted-paper lists. HPC-ODA is the single most likely venue for competing label-quality / telemetry-provenance work. |
| Anytime from now | ORNL/OSTI deposit or an arXiv preprint could appear at any point now that the camera-ready (28 AUG 2026) has passed. Neither exists as of 2026-09-06. | Periodic search on the exact title; try OSTI once its robots policy permits, and watch the six authors' ORCID/profile pages. |
| **November 2026** | Proceedings: SC26 states Technical Program Publications "(Available November 2026)", archived in ACM DL and IEEE Xplore with free ACM OpenTOC. DOI and page numbers appear then. | Full-text read; answer every §1.5 content question definitively. Crossref will then resolve the DOI (it does not today). |
| 15 NOV 2026 / 17–19 NOV 2026 / 20 NOV 2026 | AgenticAI4HPC (15 Nov), paper presentations (17–19 Nov), HPC-ODA (20 Nov). | — |

---

## 6. Evidence-depth summary

| Claim | Depth |
|---|---|
| ORNL paper exists with that exact title | `TITLE-ONLY` — two independent public sources |
| Author list and single ORNL affiliation | `TITLE-ONLY` (author metadata) |
| It is a Technical Papers submission | `PROGRAM-METADATA-ONLY (award-list level)` — inferred from the Best Paper Nominee mechanism, which the SC26 announcement scopes to "the SC Technical Papers program". Not yet confirmed by an `Event Type:` line. |
| Topic area, session, day/time | `NOT FOUND` (schedule unpublished) |
| DOI, pages | `NOT FOUND` (Crossref: no match) |
| arXiv / OSTI preprint | `NOT FOUND` as of 2026-09-06 — **not** "does not exist" |
| All content questions (labels, cross-source agreement, taxonomy, incident counts, resolution sweep, telemetry layers, online vs offline, artifact) | `UNKNOWN` / `NOT FOUND` — nothing public to read |
| Full SC26 Technical Papers accepted list | `NOT FOUND` (not yet published; only 9 award finalists public) |
| AgenticAI4HPC'26 exists, is a first edition, is an accepted SC26 workshop, 15 Nov 2026 | verified |
| AgenticAI4HPC'26 accepted papers | `NOT FOUND` (acceptances 4 SEP 2026; nothing posted by 6 SEP 2026) |

## 7. Sources consulted
- https://sc26.supercomputing.org/2026/08/announcing-best-paper-and-best-student-paper-finalists/
- https://www.hpcwire.com/off-the-wire/sc26-announcing-best-paper-and-best-student-paper-finalists/
- https://sc26.supercomputing.org/program/papers/
- https://sc26.supercomputing.org/program/
- https://sc26.supercomputing.org/program/proceedings-archives/
- https://sc26.supercomputing.org/all-dates-deadlines/
- https://sc26.supercomputing.org/2026/07/from-paper-decisions-to-registration-a-guide-to-sc26-in-july-and-beyond/
- https://sc26.supercomputing.org/2026/04/a-gold-standard-sc26-welcomes-50-workshops-to-chicago/
- https://ornl.github.io/events/agenticai4hpc2026/
- https://hpc-oda.org/workshop2026/
- https://agent4sc.github.io/
- https://www.ornl.gov/staff-profile/anjus-george
- https://www.ornl.gov/staff-profile/ahmad-maroof-karimi
- https://api.crossref.org/works (one bibliographic query, no match)
- https://sc26.conference-program.com/ — **401, twice (root and institution-filter form)**
- osti.gov, pub.orcid.org — robots-disallowed to the permitted tooling

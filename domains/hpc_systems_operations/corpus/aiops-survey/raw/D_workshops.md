Research complete. Here are the structured notes.

---

# HPC WORKSHOP ECOSYSTEM MINING (2020–2026)
## Emerging operational research problems not yet promoted to SC Technical Paper level

**Compiled:** 2026-09-06. **Convention:** `VERIFIED` = confirmed on a program page, publisher TOC, or proceedings record I fetched. `UNVERIFIED` = could not confirm; treat as unknown, not as fact. Nothing below is inferred-and-presented-as-fact except where explicitly labelled `INFERRED`.

---

# PART 0 — HEADLINE CORRECTIONS TO THE TASK'S ASSUMPTIONS

Three of the premises in the brief are wrong or need adjusting, and they matter a lot for a KISTI researcher looking for un-promoted problems:

1. **There was NO SC-affiliated ODA *workshop* before 2026.** The SC/ISC ODA activity 2019–2025 was a **BoF series**, not a peer-reviewed workshop. `HPC-ODA 2026` at SC26 is explicitly billed as the **1st** International Workshop on HPC Operational Data Analytics, converting "eight years of successful BoF sessions at SC and ISC" into peer review. **This is the single most important structural finding: the SC-side ODA community has been generating operational problems for 8 years with no archival paper trail at all.**
2. **MODA is the only long-running peer-reviewed ODA venue**, and it is ISC-side, Springer LNCS, and *tiny* — 2–5 papers per year, 17 archival chapters total across 2020–2025. That is the entire peer-reviewed corpus of HPC operational data analytics as a named field.
3. **FTXS did not run at SC25**, and at SC26 it is **renamed and rescoped away from HPC fault tolerance** to "Faults, Trustworthiness, and eXplainability for **AI Systems** at Scale." The classical HPC-resilience workshop lane is closing.

---

# PART 1 — WORKSHOP-BY-WORKSHOP, YEAR-BY-YEAR MAP

## 1.1 W1 — SC-side workshops

### HPC-ODA / "Workshop on Operational Data Analytics in HPC" — SC
| Year | Ran? | Form | Host | Proceedings | Peer-rev. | ~Papers | URL |
|---|---|---|---|---|---|---|---|
| 2019 | Yes | **BoF** | SC19 | none | No | — | hpc-oda.org/events/2019-sc19-oda-bof/ |
| 2020 | **NOT FOUND** | — | — | — | — | — | (no ODA event listed for SC20/ISC20) |
| 2021 | Yes ×2 | **BoF** | ISC21 ("Guidelines for HPC Data Center Monitoring"), SC21 | none | No | — | hpc-oda.org/events/ |
| 2022 | Yes | **BoF** ("Drowning in Data") | SC22 | none | No | — | ditto |
| 2023 | Yes ×2 | **BoF** | ISC23, SC23 | none | No | — | sc23.supercomputing.org/proceedings/bof/bof_pages/bof142.html |
| 2024 | Yes ×2 | **BoF** (ISC24 "HPC Efficiency Improvements with Interoperable Monitoring"; SC24 "Data Journey Towards Insights") | ISC24, SC24 | none | No | — | sc24.conference-program.com/presentation/?id=bof125 |
| 2025 | Yes | **BoF** ("Operational Data Analytics: Mind the Gap") | SC25 | none | No | — | hpc-oda.org/events/2025-sc25-oda-bof/ |
| 2026 | **Yes — 1st WORKSHOP** | Workshop | SC26, Chicago, Nov 2026 | **SC26 Workshop Proceedings, IEEE Xplore** | **Yes** | `PARTIAL / NOT YET HELD` (submission deadline Aug 12, 2026) | hpc-oda.org/workshop2026/ |

- Organizers 2026: Michael Ott (LRZ), Ayse Coskun (BU), Jeff Hanson (HPE), Melissa Romanus (NERSC/LBNL), Woong Shin (ORNL), Tim Osborne (ORNL). 30-member PC. Formats: 8p full / 4p short / 1–2p lightning talk.
- Two date/deadline discrepancies exist between hpc-oda.org's `/events/` page (Nov 16; CFP Jul 31) and `/workshop2026/` (Nov 20; deadline Aug 12). `UNVERIFIED` which is correct.
- Community output has been **EE HPC WG workshop reports**, not papers.

### MODA — ISC (Springer LNCS, "ISC High Performance … International Workshops, Revised Selected Papers")
| Year | Edition | Date | LNCS volume | Peer-rev. | Chapters |
|---|---|---|---|---|---|
| 2020 | 1st ("Monitoring and **Data** Analytics") | Jun 25, 2020 | 978-3-030-59851-8 | Yes | **3** |
| 2021 | 2nd | Jul 2, 2021 (virtual) | 978-3-030-90539-2 | Yes | **2** |
| 2022 | 3rd | Jun 2, 2022 | 978-3-031-23220-6 | Yes | **2** |
| 2023 | 4th | May 25, 2023 | 978-3-031-40843-4 | Yes | **3** |
| 2024 | 5th | May 16, 2024 | 978-3-031-73716-9 | Yes | **2** (+4 lightning talks, not archived) |
| 2025 | 6th | Jun 13, 2025 | 978-3-032-07612-0 | Yes | **5** |
| 2026 | **7th — RENAMED** "Monitoring, **Observability**, and Operational Data Analytics" | Jun 26, 2026 | ISC26 workshops LNCS `NOT YET PUBLISHED` | Yes | **5** presented |

Program URLs: `moda.dmi.unibas.ch` (2022–2026), `moda21.sciencesconf.org`, `moda20.sciencesconf.org`.
Note: the unibas archive page mislabels MODA23/24/25 all as "Fourth"; the LNCS section headings are authoritative (MODA25 = 6th).

### HPCSYSPROS — SC
| Year | Ran? | Date/Host | Proceedings | Peer-rev. | Papers |
|---|---|---|---|---|---|
| 2020 | Yes | SC20 (virtual) | GitHub + Zenodo | Yes (workshop) | **7** |
| 2021 | Yes | SC21, Nov 14 (virtual) | GitHub + Zenodo | Yes | **6** |
| 2022 | Yes | SC22, Nov 14 | GitHub + Zenodo | Yes | **5** |
| 2023 | Yes | SC23, Nov 12 | **ACM SC-W'23 (10.1145/3624062)** + Zenodo | Yes | **10** |
| 2024 | Yes | SC24, Nov 22 | **Zenodo only** (10.5281/zenodo.157248xx, .1654xxxx) — did *not* appear under the IEEE SC-W 2024 volume as far as I could verify | Yes | **9** |
| 2025 | Yes | SC25, Nov 16 | GitHub + Zenodo | Yes | **9** |
| 2026 | Announced | SC26 | — | — | `PARTIAL` |

URL: sighpc-syspros.org/workshops/&lt;year&gt;/ ; proceedings repos github.com/HPCSYSPROS/Workshop&lt;YY&gt;.
**Important for a researcher:** HPCSYSPROS is the highest-volume source of *real production operational problems* in the whole ecosystem (46 papers 2020–2025) and is the *least* archivally visible (self-archived Zenodo, not indexed as a conference series).

### FTXS — SC
| Year | Ran? | Edition | Proceedings | Papers |
|---|---|---|---|---|
| 2020 | Yes (SC20, virtual) | 10th `INFERRED` | `UNVERIFIED` (no separate dblp volume) | `UNVERIFIED` |
| 2021 | Yes (SC21) | 11th | IEEE (FTXS54580.2021) | **5** |
| 2022 | Yes (SC22) | 12th | IEEE (FTXS56515.2022 / 10.1109) | **5** |
| 2023 | Yes (SC23, Nov 12) | 13th | ACM SC-W'23 | **4 full + 3 short** |
| 2024 | Yes (SC24, Nov 22) | **14th** (confirmed in front matter) | IEEE SC-W 2024 | **4** |
| 2025 | **DID NOT RUN** | — | — | — |
| 2026 | Yes — **renamed** "Faults, Trustworthiness, and eXplainability for AI Systems at Scale" | — | SC26 | `PARTIAL` |

URL: sites.google.com/site/ftxsworkshop/ ; sites.google.com/view/ftxs2023, /ftxs2024.

### PMBS — SC
Ran **every year 2020–2026** (PMBS20…PMBS26). PMBS26 = **17th**. Proceedings in the SC Workshops volumes (IEEE 2021/2022/2024; ACM 2023/2025). Peer-reviewed. Selected papers also extended into *Elsevier Parallel Computing* special issues (14th/15th editions). URL: pmbs-workshop.github.io. Rough paper count per year: `UNVERIFIED` (typically 8–12).

### ProTools — SC
Ran **every year 2019–2026**; SC26 = **8th**. 2020 SC20 (virtual), 2021 SC21, 2022 SC22, 2023 SC23, 2024 SC24, 2025 SC25 ("Workshop on Programming and Performance Visualization Tools"), 2026 SC26. Proceedings in SC-W volumes. URLs: vi-hps.org/symposia/protools/protools.html; sc-protools-workshop.github.io/protools25|26/. Paper counts `UNVERIFIED`.

### HPCTESTS — **VERIFIED TO EXIST; new series**
"International Workshop on HPC Testing and Evaluation of Systems, Tools, and Software."
| Year | Ran? | Edition | Papers | Proceedings |
|---|---|---|---|---|
| 2020–2022 | **DID NOT EXIST** | — | — | — |
| 2023 | Yes, SC23 Nov 17 | **1st** | **5** | SC23 Workshops (ACM) |
| 2024 | Yes, SC24 Nov 22 | 2nd | **5** | SC24 Workshops (IEEE) |
| 2025 | Yes, SC25 Nov 21 | 3rd | `UNVERIFIED` | SC25 Workshops (ACM 10.1145/3731599) |
| 2026 | Announced, SC26 | 4th | `PARTIAL` | — |

URL: olcf.github.io/hpc-system-test-wg/hpctests/. Run by the OLCF-led **HPC System Test Working Group** — an operator community, not an academic one.

### SuperCompCloud
**NOT FOUND** in the SC25 (44 workshops) or SC26 (50 workshops) lists. Treat as discontinued at SC by 2025. Earlier years `UNVERIFIED`.

## 1.2 W1 — HPDC-side workshops

| Workshop | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| **PERMAVOST** | — | **1st** (ACM 10.1145/3452412) | 2nd (10.1145/3526063) | 3rd (10.1145/3588993) | 4th | 5th (Jul 20, Notre Dame) | 6th (Jul 13, Cleveland) |
| **AI4Sys** ("AI for Systems") | — | — | — | **1st** `INFERRED` from numbering | 2nd (HPDC'24 Pisa) | **3rd** (HPDC'25) | **4th** (HPDC'26) |
| **SNTA** (Systems and Network Telemetry and Analytics) | Yes (Stockholm) | Yes (virtual) | Yes (Minneapolis) | Yes (Orlando) | Yes, **7th** (Pisa, 5 papers) | **DID NOT RUN** | **DID NOT RUN** |
| FRAME | — | — | — | — | Yes | 5th | — |
| REX-IO | — | — | — | — | — | — | 6th (returns) |

- AI4Sys accepted-paper lists are **not publicly posted** (HotCRP submission site only; "submissions closed"). Paper titles/authors for AI4Sys 2023–2025: `UNVERIFIED`. This is a real gap in the public record.
- SNTA is HPDC's telemetry workshop but is **network/streaming-algorithms oriented**, not HPC-center-operations oriented (2024: frugal quantile tracking, endpoint congestion management, eBPF gossip, bulk-synchronous writes, UAV channel capacity). Its disappearance after 2024 removes the only HPDC telemetry venue.

## 1.3 W1 — IPDPS-side workshops

### JSSPP (Springer LNCS, every year)
| Year | Edition | LNCS | Location |
|---|---|---|---|
| 2020 | 23rd | 12326 | New Orleans |
| 2021 | 24th | 12985 | virtual |
| 2022 | 25th | 13592 | virtual |
| 2023 | 26th | 14283 | St. Petersburg FL |
| 2024 | 27th | 14591 | San Francisco | (**10** papers) |
| 2025 | 28th | 16210 | Milan | (**17** papers) |
| 2026 | 29th | 16980 | New Orleans | (**13** papers announced) |

URL: jsspp.org. Peer-reviewed, archival LNCS. **JSSPP is the one W1 venue where operational scheduling problems DO get archived** — but into LNCS, not into SC/IPDPS main tracks.

### ESSA (IPDPS)
1st = 2020 … **6th = 2025**, **7th = 2026** (`INFERRED` from the 2026 official "7th" label + continuous IPDPS listing). IEEE IPDPSW proceedings. Per-year paper counts `UNVERIFIED`.

### iWAPT (IPDPS)
Ran 2025 and 2026 (**21st** in 2026). 2020–2024 continuity `UNVERIFIED` but the numbering is continuous with a 2006 start. IEEE IPDPSW.

## 1.4 W2 — topic-driven, present-where-found

| Workshop | Status found |
|---|---|
| **PDSW** | Ran every year. IEEE standalone volumes 2020 (5th, 10.1109/PDSW51947.2020), 2021 (6th), 2022 (7th). **From 2023 it folded into the combined SC-W proceedings** (no separate dblp volume) — 2023, 2024, PDSW'25 at SC25, PDSW'26 = **11th** at SC26. |
| **Sustainable Supercomputing** | SC-side: verified at **SC24** (e.g. "Towards Sustainable Post-Exascale Leadership Computing"), **SC25** (Nov 16), **SC26**. ISC-side: "International Workshop on Sustainable Supercomputing" in the **ISC 2024** LNCS workshops volume. SC23 and earlier: `UNVERIFIED`. |
| **EESP** (Energy Efficiency with Sustainable Performance) | **1st: ISC 2025** (Jun 13; 8 accepted / 36% acceptance; 6 archived in LNCS 978-3-032-07612-0). **2nd: ISC 2026** (Jun 26; 11 accepted from 19 submitted). **3rd: SC 2026** (Nov 15, Chicago) — `PARTIAL`. URL: ayeshaafzal91.github.io/eesp/ |
| **HUST** (HPC User Support Tools) | Ran **every year 2014–2026**; HUST-26 = **13th**. Proceedings: IEEE (2020, 2022), Zenodo (2021), ACM SC-W (2023, 2024, 2025). URL: hust-workshop.github.io. Per-year paper lists not posted on the site → `UNVERIFIED`. |
| **ISAV** | At SC through 2026; **renamed at SC25/SC26 to "In Situ AI, Analysis and Visualization"** (from "In Situ Infrastructures for Enabling Extreme-Scale Analysis and Visualization"). Per-year records `UNVERIFIED` (dblp venue page 404). |
| **Digital Twins for HPC** | **SC25 only**: "Digital Twins Workshop for High-Performance Computing" is in the SC25 44-workshop list. **NOT in the SC26 50-workshop list** — did not repeat at SC26. Earlier years `UNVERIFIED`. |
| **High Performance Fabrics for AI and HPC (HPF AI/HPC)** | **SC26 only** in the lists I verified. Earlier years `NOT FOUND`. |
| **Resource management** | RESDIS (RESource DISaggregation) — SC25 (5th), SC26 (6th). **ECHO — "1st International Workshop on Edge-Cloud-HPC Operational Continuum", NEW at SC26.** |
| **Resilience / fault tolerance** | FTXS only (see above); no replacement ran at SC25. |
| **New at SC26, operationally relevant** | **AgenticAI4HPC'26** (1st, Agentic AI for HPC), **RISE 2026** (Rising Innovators in Sustainable Exacomputing), **Sovereign AI Supercomputing Cloud**, **AI on HPC: Performance Engineering, Challenges and Opportunities**. |

---

# PART 2 — OPERATIONAL PROBLEM INVENTORY

Twelve problems recur across ≥3 workshops and ≥3 years. For each: appearances → representative verified papers → state of practice → archival status.

---

### **P-A. Every centre builds its own monitoring stack; no standard telemetry schema**
- **Appears in:** MODA 2020–2026 (every edition), ODA BoF SC19→SC25 (every edition), HPCSYSPROS 2023/2024, HPC-ODA'26 CFP topic 3.
- **Representative papers:**
  1. Terai, Yamamoto, Miura, Shoji — *An Operational Data Collecting and Monitoring Platform for Fugaku* — 2021 — MODA21 — LNCS 10.1007/978-3-030-90539-2_24
  2. Osborne, Palumbo, Huk, Adamson, Jones, Lester (ORNL) — *Advancing ODA Standardization Through an Open Source Dashboard* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724831
  3. Piccinali & Benini (CSCS) — *EMOI: CSCS Extensible Monitoring and Observability Infrastructure* — 2024 — MODA24 lightning talk — no DOI
  4. Whitney, Romanus, Davis, Bautista (NERSC/LBNL) — *Next-Generation Data Explanation: Bridging the Gap from Data Collection to Operational Data Analytics* — 2024 — MODA24 lightning talk — no DOI
  5. Guimarães, Sankaran, Frings (JSC) — *Supporting HPC Users with LLview* — 2025 — MODA25 — LNCS 978-3-032-07612-0_4
- **State of practice:** LDMS (Sandia), DCDB (LRZ), Examon (CINECA/UniBo), LLview (JSC), PIKA (TUD), XDMoD (Buffalo), EMOI (CSCS), CEEMS (CNRS), Prometheus+Grafana everywhere. Zero interoperability. The SC24 BoF explicitly stated "HPC sites are duplicating efforts."
- **Archival promotion:** **PARTIAL.** Netti et al., *A Conceptual Framework for HPC Operational Data Analytics*, **IEEE CLUSTER 2021**, and *Operational Data Analytics in practice*, **Parallel Computing 113 (2022)**. No archival paper defines or evaluates a **standard schema**. The EE HPC WG has pursued standardization since 2023 with **no peer-reviewed output**.

---

### **P-B. Node/system anomaly & fault detection from telemetry**
- **Appears in:** MODA20, MODA21, MODA22, MODA23, FTXS22, HPCSYSPROS23, MODA26.
- **Representative papers:**
  1. Ozer, Netti, Tafani, Schulz — *Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_18
  2. Molan, Borghesi, Beneventi, Guarrasi, Bartolini — *An Explainable Model for Fault Detection in HPC Systems* — 2021 — MODA21 — 10.1007/978-3-030-90539-2_25
  3. Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini — *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems* — 2022 — MODA22 — 10.1007/978-3-031-23220-6_18
  4. Anton, Willemot, Gougeaud, Zertal (CEA) — *ML-Based Methodology for HPC Facilities Supervision* — 2023 — MODA23 — 10.1007/978-3-031-40843-4_23
- **State of practice:** Rule-based thresholds in production; ML models in research. Labels come from sysadmin tickets and are scarce, which is why the field moved to unsupervised/semi-supervised.
- **Archival promotion:** **YES — this is the one problem that made it.** Aksar et al., *Prodigy: Towards Unsupervised Anomaly Detection in Production HPC Systems*, **SC'23** (10.1145/3581784.3607076); Molan et al., *RUAD*, **FGCS 141 (2023)**; Ardebili et al., *Multi-level anomaly prediction in Tier-0 datacenter*, **ACM Computing Frontiers 2022**; Aksar et al. *Proctor* (**ISC'21**) and *E2EWatch* (**Euro-Par'21**).

---

### **P-C. Heterogeneous log/syslog → actionable events**
- **Appears in:** HPCSYSPROS20, FTXS22, HPCSYSPROS23, MODA26.
- **Representative papers:**
  1. Lewis, Liu, Kettimuthu, Papka — *Log-Based Identification, Classification, and Behavior Prediction of HPC Applications* — 2020 — HPCSYSPROS20 — GitHub/Zenodo
  2. Egersdoerfer, Zhang, Dai — *ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection* — 2022 — FTXS22 — IEEE, pp. 1–10
  3. Quan, Howell, Greenberg (LANL) — *Heterogeneous Syslog Analysis: There Is Hope* — 2023 — HPCSYSPROS23 — 10.1145/3624062.3624128 / 10.5281/zenodo.10223395
  4. Mustiere (CEA) — *Enhancing Security in HPC Systems: A Clustering Approach for Filtering Weak Signals* — 2026 — MODA26 — proceedings pending
- **State of practice:** grep + hand-curated regex "noise lists" per site. The LANL paper is notable for testing **LLMs as log classifiers** and finding them more explainable but computationally expensive.
- **Archival promotion:** **LOW / NOT FOUND in the HPC venues.** Log anomaly detection is archival in the *cloud/SE* world (ICSE, FSE, DSN); the *HPC-specific* heterogeneous-syslog problem has no SC/HPDC/IPDPS/Cluster regular paper I could verify.

---

### **P-D. Telling users their job was inefficient (job-level efficiency reporting)**
- **Appears in:** MODA23, MODA25, MODA26, HPCSYSPROS23, HPCSYSPROS24, and the SC25 ODA BoF poll.
- **Representative papers:**
  1. Winkler & Knüpfer (TU Dresden) — *Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA* — 2023 — MODA23 — 10.1007/978-3-031-40843-4_22
  2. Guimarães, Sankaran, Frings (JSC) — *Supporting HPC Users with LLview* — 2025 — MODA25 — 10.1007/978-3-032-07612-0_4
  3. Guilbault (Université Laval) — *Self-service Monitoring of HPC and Openstack Jobs for Users* — 2023 — HPCSYSPROS23
  4. Simakov (SUNY Buffalo) — *Benchmarking and Continuous Performance Monitoring of HPC Resources using the XDMoD Application Kernel Module* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724847
  5. Ma et al. (NHR@FAU) — *Automatic Workload Characterization on Production HPC Systems via Roofline Telemetry* — 2026 — MODA26
- **State of practice:** Heuristic thresholds hand-tuned from operator experience (PIKA has run >5 years at TUD; LLview is production on JUWELS Cluster+Booster). No cross-site validation, no agreed definition of "inefficient."
- **Archival promotion:** **NOT FOUND.** ⚠️ **HIGH-VALUE GAP.** Quantitative evidence: the SC25 ODA BoF poll (29 respondents) found users rate operational data's value at **4.3/5** but their own capability to use it at **2.9/5**.

---

### **P-E. Per-job energy accounting, power capping, energy budget control**
- **Appears in:** MODA20, MODA24, MODA25, MODA26, EESP25, EESP26, JSSPP24, JSSPP25, Sustainable Supercomputing SC24/SC25.
- **Representative papers:**
  1. Tracey, Hoang, Subelet, Elisseev (IBM) — *AI-Driven Holistic Approach to Energy Efficient HPC* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_17 `DOI UNVERIFIED`
  2. Paipuri (CNRS) — *Monitoring of Energy and Emissions of HPC Batch Job Using CEEMS* — 2024 — MODA24 lightning talk
  3. Prica & Zamuda — *Monitoring Energy Consumption of Workloads on HPC Vega* — 2025 — MODA25 — LNCS 978-3-032-07612-0
  4. Angelelli, Carastan-Santos, Dutot — *Run your HPC jobs in Eco-Mode: revealing the potential of user-assisted power capping in supercomputing systems* — 2024 — JSSPP24 — LNCS 14591
  5. Corbalan & Alonso (BSC) — *Static powercap vs EAR hard-powercap: Performance evaluation* — 2025 — JSSPP25 — LNCS 16210
  6. Menear (NREL) — *Pre-runtime GPU Power Quantile Forecasting from Submission-Time Job Artifacts* — 2026 — MODA26
- **State of practice:** RAPL/IPMI/Redfish/DCGM sampling; EAR and SLURM plugins in production at BSC/CINECA; per-job attribution still contested (shared PSUs, cooling overhead, idle allocation).
- **Archival promotion:** **YES, partially.** Karimi, Maiterth, Shin, Sattar, Lu, Wang, *Exploring the Frontiers of Energy Efficiency using Power Management at System Scale* (arXiv:2408.01552, Frontier, 3 months telemetry, up to 8.5% / ~1,438 MWh savings) — `venue beyond arXiv UNVERIFIED`. **But: per-job energy *attribution methodology* has no archival paper.**

---

### **P-F. Facility thermal/cooling modelling and datacenter digital twins**
- **Appears in:** MODA22, Sustainable Supercomputing SC25, SC25 Digital Twins Workshop, HPC-ODA'26 CFP topic 6.
- **Representative papers:**
  1. Egan, Purkayastha, Sickinger (NREL) — *Data Center Facility Monitoring with Physics Aware Approach* — 2022 — MODA22 — 10.1007/978-3-031-23220-6 (pp. 251–261)
  2. Seyedkazemi Ardebili et al. — *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems* — 2022 — MODA22 (validated against real Marconi100 thermal emergencies)
  3. SC25 Sustainable Supercomputing — "HPC digital twins for scheduling evaluation", "Microgrid optimization for data centers", "Small modular reactor performance for data centers" — author attribution `UNVERIFIED` (program page lists topics without authors)
- **Archival promotion:** **YES — the clearest success story.** Brewer, Maiterth, Kumar, Wojda, Bouknight, Hines, Shin, Greenwood, Grant, Williams, Wang, *A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale*, **SC24 Technical Paper**, 10.1109/SC41406.2024.00029 (ExaDigiT; Frontier; validated on 6 months of operational data).

---

### **P-G. Component failure prediction — disks, GPUs, hardware errors**
- **Appears in:** FTXS23, FTXS24, HPCTESTS23, MODA26.
- **Representative papers:**
  1. Hagerty, Webb, Melesse Vergara, Ezell (ORNL) — *Experiences Detecting Defective Hardware in Exascale Supercomputers* — 2023 — HPCTESTS23 — SC23 Workshops
  2. George, Hanley, Oral (ORNL) — *Disk Failure Trends in Alpine Storage System* — 2023 — FTXS23 short paper
  3. George, Wang, Hanley, Ransom, Bent, Zimmer — *From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments* — 2024 — FTXS24 — IEEE SC-W 2024
  4. Brown (ANL) — *Evaluating Forecasting Techniques for Hardware Errors on a Large-scale HPC System* — 2026 — MODA26
- **Archival promotion:** **YES for GPUs, NOT FOUND for HPC disks.** GPUs: Oles, Schmedding, Ostrouchov, Shin, Smirni, Engelmann, *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*, **ICS'24** (27,648 V100s; DBEs recur on the same GPUs; correlated with sustained power, not temperature) — 10.1145/3650200.3656615. Disk/parallel-filesystem failure in HPC remains a workshop-only literature.

---

### **P-H. Acceptance testing / continuous system testing / silent regression detection** ⚠️
- **Appears in:** FTXS21, HPCSYSPROS22, HPCTESTS23/24/25, HPCSYSPROS24, MODA25, MODA26. **Every year 2021–2026.**
- **Representative papers:**
  1. DeBardeleben, Burr, Penton, Walker, Loncaric, Jones — *Statistical Framework for Two-Party Acceptance Testing of HPC Systems for Reliability* — 2021 — FTXS21 — IEEE pp. 21–30
  2. Siddiqui, Palmer, Shende, Spear, Sambrekar, Xiang (NERSC/UO) — *An Automated Approach to Continuous Acceptance Testing of HPC Systems at NERSC* — 2022 — HPCSYSPROS22
  3. Pearce, Scott, Becker, Haque, Hanford, Brink, Jacobsen, Poxon, Domke, Gamblin — *Toward Collaborative Continuous Benchmarking for HPC* — 2023 — HPCTESTS23 — SC23 Workshops
  4. Jacobsen & Bird (Google) — *Ramble: A Flexible, Extensible, and Composable Experimentation Framework* — 2023 — HPCTESTS23
  5. Siegmann, Carlson, Simakov, Curtis, Calder, Harrison — *What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years* — 2025 — MODA25 — LNCS 978-3-032-07612-0_5 (Ookami; 4+ years; 500+ users)
  6. Guimaraes (JSC) — *Centralised Dashboard for Continuous Benchmarking: From HPC Clusters to Quantum Processors* — 2026 — MODA26
- **State of practice:** buildtest, ReFrame, Ramble, Benchpark, XDMoD Application Kernels — all tool papers, no methodology paper. Every large centre reinvents its acceptance suite for each procurement.
- **Archival promotion:** **NOT FOUND. ⚠️ THE LARGEST GAP IN THE ECOSYSTEM.** An entire workshop series (HPCTESTS, now 4 editions) exists for this problem and it has produced **zero** SC/HPDC/IPDPS/Cluster/DSN regular papers.

---

### **P-I. Job runtime / queue-time / resource prediction feeding scheduling**
- **Appears in:** JSSPP every year, MODA24, MODA25, MODA26.
- **Representative papers:**
  1. Klusacek & Chlumsky — *Real-life HPC Workload Trace Featuring Refined Job Runtime Estimates* — 2024 — JSSPP24 — LNCS 14591
  2. Cui, Takahashi, Shimomura, Takizawa — *Clustering Based Job Runtime Prediction for Backfilling Using Classification* — 2024 — JSSPP24
  3. Menear, Duplyakin, Konate (NREL/LBNL) — *How well can we predict two most important metrics for HPC jobs: runtime and queue time?* — 2024 — MODA24 lightning talk
  4. Loreti, Leone, Borghesi — *Duration-Informed Workload Scheduler* — 2025 — MODA25 — LNCS 978-3-032-07612-0_1 (Marconi100 / M100 ExaData traces; **~11% reduction in mean waiting time**)
  5. Oztop, Schwaller, Leung, Kulis, Egele, Coskun (BU + Sandia) — *Job Grouping Based Intelligent Resource Prediction Framework* — 2025 — JSSPP25 — LNCS 16210
- **Archival promotion:** **PARTIAL.** Archived in LNCS (JSSPP) but rarely at SC/IPDPS main track. The **closed-loop deployment** of a predictor into a production scheduler is nowhere archival.

---

### **P-J. Centre-scale I/O monitoring and filesystem contention attribution**
- **Appears in:** MODA20, MODA25, PDSW every year, HPCSYSPROS24, SNTA24, PERMAVOST25.
- **Representative papers:**
  1. Sivalingam & Richardson (HPE) — *Application IO Analysis with Lustre Monitoring Using LASSi for ARCHER* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_16 (multi-year ARCHER data; joins scheduler job data with Lustre metrics)
  2. Paipuri (CNRS/IDRIS) — *A Unified I/O Monitoring Framework Using eBPF* — 2025 — MODA25 — 10.1007/978-3-032-07612-0_3 (eBPF on VFS kernel functions → Prometheus; validated vs IOR on production Lustre; negligible overhead)
  3. Kartik & Lockwood (VAST/Microsoft) — *Beyond the Hype: Uncovering the Real I/O Needs of LLMs* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724856
  4. Masih, Liem, Kunkel — *Factors Impacting I/O Time Proportion in AI Workloads* — 2025 — PERMAVOST25
- **Archival promotion:** **YES for characterization** (PDSW→SC pipeline is well established). **NOT FOUND for "who is slowing down the filesystem right now"** — real-time culprit attribution in production has no archival paper.

---

### **P-K. Operational data governance, retention, and public dataset release**
- **Appears in:** MODA24, SC24 BoF, SC25 BoF, HPC-ODA'26 CFP topic 3.
- **Representative papers:**
  1. Widener, May, Singleton, Kuchar (ORNL) — *Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository* — 2024 — MODA24 — 10.1007/978-3-031-73716-9 (pp. 287–292)
  2. (Dataset, not workshop) Borghesi/Bartolini et al. — *M100 ExaData: a data collection campaign on CINECA's Marconi100* — **Nature Scientific Data** 2023 — 10.1038/s41597-023-02174-3
- **State of practice:** Almost all operational telemetry is unreleasable (security, user privacy, vendor NDA). **SC25 BoF poll rated availability of public ODA datasets at 1.6/5** — the lowest score in the poll.
- **Archival promotion:** **NOT FOUND** for governance/anonymization methodology. Datasets exist (M100 ExaData, Fugaku, OLCF SMC data challenges) but there is no archival paper on *how* to release HPC operational data safely.

---

### **P-L. Login node / shared resource abuse control and multi-tenancy**
- **Appears in:** HPCSYSPROS 2023, 2024; MODA24 panel ("MODA in multitenant and federated environments", moderated by Utz-Uwe Haus, HPE).
- **Representative papers:**
  1. McKay, Forrest, Fischer (Univ. of Utah) — *Dynamic Login Node Resource Control and Monitoring with Arbiter 3* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.16541343
  2. Focht (Penn State) — *Democratizing Remote HPC Storage Access* — 2023 — HPCSYSPROS23
  3. Maloney (NCSA) — *Transparent Global File System Access in Environments with Multiple Authentication Domains* — 2025 — HPCSYSPROS25
- **Archival promotion:** **NOT FOUND** at SC/HPDC/IPDPS. Arbiter's archival lineage is at **PEARC**, a practice conference. ⚠️ Gap.

---

### **P-M. Configuration drift, node image consistency, provisioning at scale**
- **Appears in:** HPCSYSPROS **every year 2020–2025** — the single most persistent theme in the ecosystem.
- **Representative papers:** Allen, Ezell, Peltz, Jacobsen, Lueninghoener, Wofford, Roman — *Modernizing the HPC System Software Stack* (2020); Mickels — *Using xCAT and Git to Manage Node Software Consistency and DevOPs* (2022); Baker, Blaas, Tillotson (NCAR) — *Clushible: Tidal Wave-Like Configuration with Ansible* (2023); Trecakov, Von Wolff, Al-Tahat — *SStack* (2024); Glick — *Modernizing HPC Configuration Management* (2025); Kincl — *Exploring bootc for HPC Cluster Management* (2025); Anderson — *Provisioning to Disk with Warewulf v4* (2025).
- **Archival promotion:** **NOT FOUND anywhere.** Zero archival research papers. ⚠️ Gap (though arguably an engineering, not research, problem — the *research* framing would be drift detection and its correlation with job failures, which nobody has done).

---

### **P-N. Cloud-native / Kubernetes convergence in HPC operations**
- **Appears in:** HPCSYSPROS 2021–2024, JSSPP25, SC26 (new ECHO workshop).
- **Representative papers:** Knight — *Kubernetes for HPC Administration* (HPCSYSPROS21); Kincl & Bruszewski (Red Hat) — *Embracing Batch on Kubernetes* (HPCSYSPROS23); Gough & Lumas (Purdue) — *Kubernetes Resource Scaling via Batch Node Conversion on the Anvil Supercomputer* (HPCSYSPROS24, 10.5281/zenodo.16576621); Spišaková, Stoyanov, Hejtmánek, Klusacek, Reber, Bruno — *Kubernetes Scheduling with Checkpoint/Restore: Challenges and Open Problems* (JSSPP25).
- **Archival promotion:** **PARTIAL** (CCGrid/HPDC have converged-computing papers). Operations-specific (dynamic batch↔k8s node conversion on a production supercomputer): **NOT FOUND.**

---

### **P-O. Security posture and weak-signal detection in operational data**
- **Appears in:** HPCSYSPROS22, HPCSYSPROS25, MODA26, S-HPC (SC25 4th, SC26 5th).
- **Representative papers:** Deumens (UF) — *Cybersecurity Frameworks: NIST 800-171 and CMMC v2.0 Update* (HPCSYSPROS22); Rollins — *NIST SP 800-\* in HPC: Standards That Matter* (HPCSYSPROS25); Mustiere (CEA) — *Enhancing Security in HPC Systems: A Clustering Approach for Filtering Weak Signals* (MODA26).
- **Archival promotion:** **NOT FOUND.** ⚠️ Gap.

---

### **P-P. Carbon-aware and sustainability-driven operations**
- **Appears in:** JSSPP25, EESP25/26, Sustainable Supercomputing SC24/25/26.
- **Representative papers:** Benhari & Trystram — *Adaptive Carbon-Aware scheduling policies for HPC systems* (JSSPP25); Hossain, Abdurahman, Islam, Ahmed — *Power-Aware Scheduling for Multi-Center HPC Electricity Cost Optimization* (JSSPP25); Smith, Abt, Grant (Queen's) — *What A Waste* (EESP25, **Best Paper**); Tröpgen, Smejkal, Ilsche, Schöne, Schirmeier (TU Dresden) — *Pinpointing Idle-Power Regressions in Linux* (EESP25, LNCS pp. 205–218).
- **Archival promotion:** **NOT FOUND for HPC specifically.** Carbon-aware computing is archival at HotCarbon/ASPLOS/SOSP for cloud; the HPC-centre variant (fixed capacity, no migration, national-grid coupling) is workshop-only. ⚠️ Gap.

---

# PART 3 — THE 20 STRONGEST INDIVIDUAL WORKSHOP PAPERS

Coding: **L0** collection · **L1** viz · **L2** rule alert · **L3** anomaly detection · **L4** prediction · **L5** RCA · **L6** recommendation · **L7** closed loop. **D0** conceptual → **D5** closed-loop production. **P0–P4** = production-data maturity (P0 synthetic, P1 single-node/testbed, P2 partial production trace, P3 full production system, P4 multi-system/multi-year production).

---

**1. An Operational Data Collecting and Monitoring Platform for Fugaku: System Overviews and Case Studies in the Prelaunch Service Period**
Terai, Yamamoto, Miura, Shoji (RIKEN R-CCS) | 2021 | MODA21 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-030-90539-2_24 | *Problem:* collecting telemetry at exascale node counts without stealing application cores | *Component:* whole-system + facility BMS | *Data:* logs, metrics, building-management sensors | *Method:* three-tier pipeline → TSDB → dashboards; uses A64FX **redundant cores** for collection | *Eval:* Fugaku, **>150,000 compute nodes, full metric sweep in <20 s**, prelaunch period | *Real production data:* YES | *Deployed:* YES | **L0–L1** | **D4** | **P3** | *Contribution:* the reference point for "collection at exascale is a solved-ish engineering problem" | *Limits:* no analytics layer; no failure/efficiency use case | *SC-regular relevance:* **HIGH — architecture for exascale telemetry at 10⁵ nodes; the closest thing to a citable scale baseline.**

**2. An Explainable Model for Fault Detection in HPC Systems**
Molan, Borghesi, Beneventi, Guarrasi, Bartolini (UniBo/CINECA) | 2021 | MODA21 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-030-90539-2_25 | *Problem:* automated node fault detection with sysadmin-usable explanations | *Component:* compute nodes | *Data:* Examon holistic monitoring + manual admin state labels | *Method:* supervised classification + explainability | *Eval:* CINECA Tier-0 production system, **Apr–Jul 2019 (~4 months)** | *Production data:* YES | *Deployed:* NO (offline) | **L3** | **D2** | **P3** | *Contribution:* established the label-scarcity framing that drove the whole UniBo line | *Limits:* supervised, labels manual and noisy | *SC-regular relevance:* **HIGH — already promoted (see Lineage).**

**3. Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems**
Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini | 2022 | MODA22 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-031-23220-6_18 | *Problem:* detecting thermal hazards before they trigger emergency shutdown | *Component:* cooling/thermal, node inlet/outlet | *Data:* thermal monitoring signals | *Method:* complex statistical rule sets (deliberately not ML — operator-auditable) | *Eval:* **Marconi100 (CINECA), validated against real thermal emergency events** | *Production data:* YES | *Deployed:* validated on production events | **L2–L3** | **D3** | **P3** | *Contribution:* rare case of validation against actual facility incidents rather than injected anomalies | *Limits:* rules hand-derived; no generalization across sites | *SC-regular relevance:* **HIGH — facility-level incident prediction with ground truth is exactly what SC lacks.**

**4. Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA**
Winkler, Knüpfer (TU Dresden) | 2023 | MODA23 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-031-40843-4_22 | *Problem:* nobody tells users their jobs waste resources | *Component:* per-job performance counters, whole centre | *Data:* continuous job-level performance monitoring (PIKA) | *Method:* heuristic footprint checks; thresholds derived from operational experience | *Eval:* **NHR centre at TU Dresden, >5 years of continuous production monitoring** | *Production data:* YES | *Deployed:* **YES, production, used by both users and admins** | **L2–L3** | **D4** | **P4** | *Contribution:* the most mature production job-efficiency detector in the literature | *Limits:* heuristics not validated against ground truth; no cross-site transfer; **no archival version** | *SC-regular relevance:* **VERY HIGH — the strongest un-promoted paper in the corpus.**

**5. ML-Based Methodology for HPC Facilities Supervision**
Anton, Willemot, Gougeaud, Zertal (CEA) | 2023 | MODA23 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-031-40843-4_23 | *Problem:* supervising facility-level infrastructure across measurement layers | *Component:* facility + infrastructure devices | *Data:* multi-level device measurements; energy as exemplar | *Method:* 3-stage — data cleaning → clustering (DBSCAN/HDBSCAN/agglomerative) + anomaly detection → custom visualization | *Eval:* CEA facilities, scale/duration `UNVERIFIED` | *Production data:* likely, `UNVERIFIED` | *Deployed:* `UNVERIFIED` | **L1–L3** | **D2** | **P2** `UNVERIFIED` | *Contribution:* explicit methodology (not just a tool) for facility supervision | *Limits:* thin evaluation | *SC-regular relevance:* MEDIUM.

**6. A Fast Simulator to Enable HPC Scheduling Strategy Comparisons**
Wilkinson, Jones, Richardson, Dykes, Haus (HPE / UCL) | 2023 | MODA23 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-031-40843-4 pp. 320–333 | *Problem:* you cannot A/B-test scheduling policy on a production machine | *Component:* batch scheduler | *Data:* workload traces | *Method:* fast discrete-event scheduling simulator | *Eval:* `UNVERIFIED` | *Production data:* `UNVERIFIED` | *Deployed:* NO | **L6** (decision support) | **D1** | **P2** `UNVERIFIED` | *Contribution:* addresses the counterfactual-evaluation problem that blocks all L6/L7 operational work | *Limits:* simulator fidelity unvalidated against production | *SC-regular relevance:* **HIGH — "how do you evaluate an operational policy change without breaking production" is an unsolved, publishable meta-problem.**

**7. Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository**
Widener, May, Singleton, Kuchar (ORNL) | 2024 | MODA24 | **[WORKSHOP-PEER-REVIEWED — short paper]** | 10.1007/978-3-031-73716-9 pp. 287–292 | *Problem:* monitoring/analytics for a public data repository, incl. what can be released | *Component:* data repository / storage services | *Data:* repository access + system telemetry | *Method:* experience report | *Eval:* ORNL leadership data repository | *Production data:* YES | *Deployed:* n/a | **L0–L1** | **D3** | **P3** | *Contribution:* names the governance blockers explicitly | *Limits:* 6 pages, no evaluation | *SC-regular relevance:* MEDIUM–HIGH (governance is unaddressed archivally).

**8. An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads**
Hunhold, Wesner (University of Cologne) | 2024 | MODA24 | **[WORKSHOP-PEER-REVIEWED — full paper]** | 10.1007/978-3-031-73716-9 pp. 273–286 | *Problem:* validating that the resource manager itself survives exascale-shaped workloads | *Component:* Slurm | *Data:* synthetic DAG workloads | *Method:* generated-workload test harness | *Eval:* `UNVERIFIED` scale | *Production data:* NO (synthetic) | *Deployed:* NO | **L0** (test infra) | **D1** | **P0** | *Contribution:* the only paper I found that treats the *scheduler as the system under test* | *Limits:* synthetic only | *SC-regular relevance:* **HIGH — resource-manager scalability testing has no archival paper.**

**9. Supporting HPC Users with LLview**
Guimarães, Sankaran, Frings (JSC) | 2025 | MODA25 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-032-07612-0_4 (LLview: 10.5281/zenodo.12706843) | *Problem:* diagnosing and reporting operational issues to the right stakeholder | *Component:* whole system, job-centric | *Data:* near-real-time job + system metrics | *Method:* open-source monitoring framework, **role-based access** (user / support / admin views) | *Eval:* **JUWELS Cluster + Booster, production** | *Production data:* YES | *Deployed:* **YES, production, open source** | **L1–L2** | **D4** | **P3** | *Contribution:* role-based stratification of operational data — directly addresses the SC25 BoF "data reaches the wrong people" finding | *Limits:* no quantitative evaluation of whether user behaviour changes | *SC-regular relevance:* **VERY HIGH — the missing evaluation (does reporting change user behaviour?) is a publishable study.**

**10. A Unified I/O Monitoring Framework Using eBPF**
Paipuri (CNRS / IDRIS) | 2025 | MODA25 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-032-07612-0_3 | *Problem:* existing I/O tools only see MPI-IO and lack temporal resolution | *Component:* I/O path, all filesystems | *Data:* eBPF traces of VFS kernel functions → Prometheus | *Method:* kernel-level tracing, filesystem- and application-agnostic | *Eval:* production **Lustre**, validated against **IOR**; "negligible overhead" | *Production data:* YES | *Deployed:* YES (IDRIS) | **L0–L1** | **D4** | **P3** | *Contribution:* filesystem- and language-agnostic I/O telemetry that also covers AI/Python workloads Darshan misses | *Limits:* overhead claim under benchmark only, not full production mix | *SC-regular relevance:* **VERY HIGH — "Darshan doesn't see AI workloads" is a live, unaddressed problem.**

**11. Duration-Informed Workload Scheduler**
Loreti, Leone, Borghesi (UniBo) | 2025 | MODA25 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-032-07612-0_1 | *Problem:* user walltime estimates are useless; scheduling suffers | *Component:* batch scheduler | *Data:* **M100 ExaData** production traces | *Method:* ML duration prediction integrated into a scheduler | *Eval:* Marconi100 traces, simulation | *Production data:* YES (trace) | *Deployed:* NO | **L4 → L6** | **D2** | **P2** | *Contribution:* **~11% reduction in mean job waiting time** | *Limits:* simulation only; no production A/B | *SC-regular relevance:* **HIGH — an actual deployment of this would be an SC/IPDPS paper.**

**12. What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years**
Siegmann, Carlson, Simakov, Curtis, Calder, Harrison (Stony Brook / SUNY Buffalo) | 2025 | MODA25 | **[WORKSHOP-PEER-REVIEWED]** | 10.1007/978-3-032-07612-0_5 | *Problem:* which operational metrics actually predict project success over a system's lifetime | *Component:* whole system (Ookami, HPE Apollo 80 A64FX) | *Data:* multi-year usage + performance tracking | *Method:* longitudinal experience study | *Eval:* **4+ years, 500+ users** | *Production data:* YES | *Deployed:* YES | **L1** | **D3** | **P4** | *Contribution:* the only **multi-year longitudinal** operational study in the corpus | *Limits:* single small system; descriptive not predictive | *SC-regular relevance:* **HIGH — longitudinal ODA studies essentially do not exist archivally.**

**13. Heterogeneous Syslog Analysis: There Is Hope**
Quan, Howell, Greenberg (LANL) | 2023 | HPCSYSPROS23 | **[WORKSHOP-PEER-REVIEWED]** | 10.1145/3624062.3624128 / 10.5281/zenodo.10223395 | *Problem:* heterogeneous clusters emit incompatible log formats; hardware failures and security events drown in noise | *Component:* whole cluster, syslog | *Data:* production syslog | *Method:* ML classification of log messages into significant vs admin-defined noise; **LLMs evaluated as classifiers** | *Eval:* LANL clusters, scale `UNVERIFIED` | *Production data:* YES | *Deployed:* `UNVERIFIED` | **L2–L3** | **D2–D3** | **P3** | *Contribution:* early, honest LLM-vs-classical comparison — LLMs more explainable, computationally costlier | *Limits:* no quantitative F1/precision reported in the abstract; noise labels site-specific | *SC-regular relevance:* **VERY HIGH — LLM-based operational log triage is 2026's obvious paper and has no archival version.**

**14. Advancing ODA Standardization Through an Open Source Dashboard**
Osborne, Palumbo, Huk, Adamson, Jones, Lester (ORNL) | 2024 | HPCSYSPROS24 | **[WORKSHOP-PEER-REVIEWED]** | 10.5281/zenodo.15724831 | *Problem:* no shared ODA schema or visualization across centres | *Component:* cross-centre ODA layer | *Data:* site telemetry | *Method:* open-source reference dashboard as a standardization vehicle | *Eval:* ORNL, `UNVERIFIED` | *Production data:* YES | *Deployed:* `UNVERIFIED` | **L1** | **D3** | **P3** | *Contribution:* the concrete artifact behind 8 years of BoF standardization talk | *Limits:* no formal schema definition, no multi-site validation | *SC-regular relevance:* **HIGH — a validated cross-site ODA schema would be a genuine SC contribution.**

**15. Experiences Detecting Defective Hardware in Exascale Supercomputers**
Hagerty, Webb, Melesse Vergara, Ezell (ORNL) | 2023 | HPCTESTS23 | **[WORKSHOP-PEER-REVIEWED]** | SC23 Workshops (ACM 10.1145/3624062, article ID `UNVERIFIED`) | *Problem:* finding the small fraction of nodes that are silently defective at exascale | *Component:* nodes, GPUs, interconnect | *Data:* acceptance + continuous test results | *Method:* test-suite based detection; operational experience | *Eval:* **Frontier-class exascale system** (`exact system UNVERIFIED but ORNL exascale context`) | *Production data:* YES | *Deployed:* YES | **L2–L3** | **D4** | **P3** | *Contribution:* the definitive practitioner statement of the silent-defect problem | *Limits:* experience report; no reusable methodology or statistics | *SC-regular relevance:* **VERY HIGH — silent hardware defect detection at exascale has no archival paper.**

**16. Toward Collaborative Continuous Benchmarking for HPC**
Pearce, Scott, Becker, Haque, Hanford, Brink, Jacobsen, Poxon, Domke, Gamblin (LLNL, Google, RIKEN, HPE) | 2023 | HPCTESTS23 | **[WORKSHOP-PEER-REVIEWED]** | SC23 Workshops | *Problem:* every centre re-implements benchmarking; results are not comparable | *Component:* benchmarking/testing infrastructure | *Data:* benchmark result corpora | *Method:* shared specification + collaborative infrastructure (Benchpark lineage) | *Eval:* multi-institution | *Production data:* partial | *Deployed:* partially | **L0–L1** | **D2** | **P2** | *Contribution:* the community-level framing of continuous benchmarking | *Limits:* position/infrastructure paper | *SC-regular relevance:* **HIGH.**

**17. An Automated Approach to Continuous Acceptance Testing of HPC Systems at NERSC**
Siddiqui, Palmer, Shende, Spear, Sambrekar, Xiang (NERSC / U. Oregon / ASU / CMU) | 2022 | HPCSYSPROS22 | **[WORKSHOP-PEER-REVIEWED]** | Zenodo, DOI `UNVERIFIED` | *Problem:* acceptance testing is manual and one-shot; systems drift after acceptance | *Component:* whole system | *Data:* test suite results over time | *Method:* buildtest-based automation | *Eval:* NERSC production systems | *Production data:* YES | *Deployed:* YES | **L2** | **D4** | **P3** | *Contribution:* turns acceptance into a continuous process | *Limits:* no analysis of what drift was actually caught | *SC-regular relevance:* **HIGH.**

**18. Dynamic Login Node Resource Control and Monitoring with Arbiter 3**
McKay, Forrest, Fischer (University of Utah) | 2024 | HPCSYSPROS24 | **[WORKSHOP-PEER-REVIEWED]** | 10.5281/zenodo.16541343 | *Problem:* abusive/runaway processes on shared login nodes degrade service for everyone | *Component:* login nodes, cgroups | *Data:* per-user resource usage | *Method:* dynamic cgroup limits + user notification; **closed-loop enforcement** | *Eval:* Utah CHPC production | *Production data:* YES | *Deployed:* **YES** | **L7 (closed-loop)** | **D5** | **P3** | *Contribution:* one of the very few genuinely **closed-loop, production-deployed** systems in the entire corpus | *Limits:* no published evaluation of user-behaviour effect or false-positive rate | *SC-regular relevance:* **HIGH — an L7/D5 system with no archival evaluation is a ready-made paper.**

**19. From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments**
George, Wang, Hanley, Ransom, Bent, Zimmer (ORNL / LANL) | 2024 | FTXS24 | **[WORKSHOP-PEER-REVIEWED]** | IEEE SC-W 2024 (10.1109/SCWorkshops63240.2024, article ID `UNVERIFIED`) | *Problem:* disk failure behaviour in large HPC storage systems | *Component:* parallel filesystem storage (Alpine/Orion lineage) | *Data:* production disk failure records | *Method:* failure-trend analysis | *Eval:* ORNL-scale storage; exact scale/duration `UNVERIFIED` | *Production data:* YES | *Deployed:* n/a | **L3–L5** | **D2** | **P3** | *Contribution:* extends the FTXS23 Alpine short paper into a full analysis | *Limits:* descriptive; no predictive model deployed | *SC-regular relevance:* **HIGH — HPC-specific disk reliability has no post-2020 archival paper (cf. the GPU work that did make ICS).**

**20. ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection**
Egersdoerfer, Zhang, Dai (UNC Charlotte) | 2022 | FTXS22 | **[WORKSHOP-PEER-REVIEWED]** | IEEE FTXS 2022, pp. 1–10 | *Problem:* log-template explosion defeats log-based anomaly detectors | *Component:* system/storage logs | *Data:* HPC log corpora | *Method:* semantic clustering of log templates before anomaly detection | *Eval:* `UNVERIFIED` datasets/scale | *Production data:* `UNVERIFIED` | *Deployed:* NO | **L3** | **D1** | **P1–P2** `UNVERIFIED` | *Contribution:* attacks the vocabulary-explosion problem directly | *Limits:* likely public/benchmark logs rather than live production | *SC-regular relevance:* MEDIUM–HIGH.

**Honourable mentions (verified, not fully profiled):** Sivalingam & Richardson, *LASSi for ARCHER* (MODA20, multi-year Lustre+scheduler join); Egan, Purkayastha, Sickinger, *Data Center Facility Monitoring with Physics Aware Approach* (MODA22, NREL); Lewis, Liu, Kettimuthu, Papka, *Log-Based Identification, Classification, and Behavior Prediction of HPC Applications* (HPCSYSPROS20, ANL); Simakov, *XDMoD Application Kernel Module* (HPCSYSPROS24); Angelelli, Carastan-Santos, Dutot, *Run your HPC jobs in Eco-Mode* (JSSPP24); Tröpgen et al., *Pinpointing Idle-Power Regressions in Linux* (EESP25); DeBardeleben et al., *Statistical Framework for Two-Party Acceptance Testing* (FTXS21); Kartik & Lockwood, *Beyond the Hype: Uncovering the Real I/O Needs of LLMs* (HPCSYSPROS24).

---

# PART 4 — LINEAGE (workshop paper → archival regular paper)

**I found four clear lineages and one strong-but-unverified one. This is a small number — that is itself the finding.**

**L-1. MODA21 → FGCS (journal archival). CONFIRMED.**
- Workshop: Molan, Borghesi, Beneventi, Guarrasi, Bartolini, *An Explainable Model for Fault Detection in HPC Systems*, MODA21, LNCS 12761.
- Archival: Molan, Borghesi, Cesarini, Benini, Bartolini, ***RUAD: Unsupervised anomaly detection in HPC systems***, **Future Generation Computer Systems 141 (2023)**, 10.1016/j.future.2022.12.001 (arXiv:2208.13169).
- Same group, same system (CINECA Tier-0 / Marconi100), same problem. The workshop paper was supervised+explainable; the archival paper drops the label dependency. **Journal, not SC/HPDC/IPDPS.**

**L-2. MODA22 → ACM Computing Frontiers. CONFIRMED.**
- Workshop: Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini, *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems*, MODA22.
- Archival: Seyedkazemi Ardebili et al., ***Multi-level anomaly prediction in Tier-0 datacenter***, **ACM Computing Frontiers 2022**, 10.1145/3528416.3530864.
- Same authors, same Marconi100 thermal data, detection → prediction. **CF is a mid-tier archival venue, not SC.**

**L-3. MODA20 → IEEE CLUSTER 2021 + Parallel Computing. CONFIRMED (same author line, generalized problem).**
- Workshop: Ozer, **Netti**, Tafani, Schulz, *Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning*, MODA20.
- Archival: **Netti** et al., ***A Conceptual Framework for HPC Operational Data Analytics***, **IEEE CLUSTER 2021**; and *Operational Data Analytics in practice: Experiences from design to deployment in production HPC environments*, **Parallel Computing 113 (2022)**; underpinned by *DCDB Wintermute*, **HPDC 2020** (10.1145/3369583.3392674).
- **This is the single best-executed workshop→archival→PhD trajectory in the field** (Netti's TUM thesis, 2022, *Holistic and Portable Operational Data Analytics on Production HPC Systems*). Note Netti has since **left the field** (his 2024–2026 output is satellite/non-terrestrial computing) — the line has no successor.

**L-4. BU/Coskun anomaly-diagnosis line → SC'23 regular paper. CONFIRMED as a series, workshop-origin `UNVERIFIED`.**
- Archival chain: *Proctor* (**ISC High Performance 2021**, LNCS) → *E2EWatch* (**Euro-Par 2021**) → ***Prodigy: Towards Unsupervised Anomaly Detection in Production HPC Systems*, SC'23 main conference**, 10.1145/3581784.3607076.
- This group now co-chairs **HPC-ODA 2026** (Ayse Coskun). Whether an earlier *workshop* paper seeded Proctor: `UNVERIFIED`.

**L-5. Frontier/ExaDigiT operational-data line → SC24 regular paper. CONFIRMED archival; workshop precursor NOT FOUND.**
- Archival: Brewer, Maiterth, Kumar, Wojda, Bouknight, Hines, **Shin**, Greenwood, Grant, Williams, Wang, ***A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale***, **SC24**, 10.1109/SC41406.2024.00029.
- Related: Oles, Schmedding, Ostrouchov, **Shin**, Smirni, Engelmann, *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*, **ICS'24**, 10.1145/3650200.3656615.
- I searched for and **did not find** a workshop paper that visibly grew into ExaDigiT. The ORNL group's workshop presence is in the **ODA BoF** (non-archival) and HPCSYSPROS (Zenodo-only). **Woong Shin keynoted MODA26** on "The Past, Current, and Future of HPC ODA" — the flow here is archival-first, workshop-as-community, i.e. the *opposite* direction.

**Explicit negative findings on lineage:**
- **PIKA (TU Dresden), LLview (JSC), XDMoD Application Kernels (Buffalo), Arbiter (Utah), EMOI (CSCS), CEEMS (CNRS), buildtest (NERSC), Ramble (Google), the ORNL ODA dashboard** — I found **no** SC/HPDC/IPDPS/Cluster/DSN regular paper for any of them. Arbiter's only non-workshop home is **PEARC**, a practice conference.
- **No HPCSYSPROS paper 2020–2025 that I examined has a traceable archival successor.** 46 papers, zero promotions found.
- **No HPCTESTS paper 2023–2025 has an archival successor.** 10+ papers, zero.

---

# PART 5 — ⚠️ PROBLEMS THAT RECUR EVERY YEAR IN WORKSHOPS BUT HAVE **NO ARCHIVAL RESEARCH PAPER**

*This is the highest-value output. Ranked by (recurrence × operational importance × absence of archival work). Each is a candidate SC/IPDPS/Cluster Technical Paper topic.*

---

### **G1. Continuous acceptance testing and silent-regression detection at exascale** — recurrence 2021–2026, six straight years
Venues: FTXS21, HPCSYSPROS22, HPCTESTS 2023/24/25/26, HPCSYSPROS24, MODA25, MODA26.
**Why no archival paper exists:** it is framed as tooling (buildtest, ReFrame, Ramble, Benchpark) rather than as a measurable research problem.
**The archival framing nobody has taken:** *"What fraction of production capacity is lost to silently degraded nodes, and what detection latency does a given test cadence buy you?"* Requires a production system, a test corpus, and a ground-truth defect log — all of which ORNL demonstrably has (Hagerty et al. 2023). Nobody has published the quantitative version.

### **G2. Does telling users about inefficiency change anything?** — recurrence 2023–2026
Venues: MODA23 (PIKA), MODA25 (LLview), MODA26 (roofline telemetry), HPCSYSPROS23/24, SC25 ODA BoF.
**Evidence of the gap:** SC25 BoF poll — users value operational data **4.3/5**, self-rate their capability **2.9/5**; audience was 17 operators, 11 researchers, **1 user**.
**The archival framing nobody has taken:** a controlled before/after study on a production system measuring whether job-efficiency reporting changes user resource requests, node-hours wasted, or queue pressure. Every ingredient exists in production at TUD and JSC. **This is the most obviously publishable un-done study in the whole ecosystem.**

### **G3. Cross-site operational telemetry schema and its validation** — recurrence 2019–2026, every single year
Venues: ODA BoF ×9, MODA ×7, HPCSYSPROS24, HPC-ODA'26 CFP.
**Evidence of the gap:** SC24 BoF: "HPC sites are duplicating efforts." Eight years of standardization discussion, one reference dashboard (Zenodo), zero schema papers.
**The archival framing:** define a metric ontology, instantiate it at ≥3 centres with different stacks (LDMS / DCDB / Prometheus), and show a **portable** analytic (e.g. an anomaly detector) transfers with bounded accuracy loss. Netti's CLUSTER'21 conceptual framework is the *only* prior art and it is conceptual, not validated cross-site.

### **G4. Configuration drift as a measurable cause of job failure** — recurrence 2020–2025, every year in HPCSYSPROS
Venues: HPCSYSPROS 2020, 2021, 2022, 2023, 2024, 2025 (Ansible, xCAT+Git, SStack, bootc, Warewulf v4, config management modernization).
**Why no archival paper:** treated purely as sysadmin craft.
**The archival framing:** instrument node-image/config divergence across a production cluster and correlate it with job failure, performance variance, and support-ticket volume. **Nobody has ever quantified this.** Zero papers anywhere.

### **G5. Real-time attribution of shared-resource degradation to a culprit job** — recurrence 2020–2026
Venues: MODA20 (LASSi), MODA25 (eBPF), PDSW every year, SNTA24, HPCSYSPROS23/24.
**State of practice:** post-hoc, manual, by a storage admin with grep.
**The archival framing:** online causal attribution of filesystem/interconnect slowdown to a job, with precision/recall against operator-confirmed incidents. Characterization is archival (PDSW→SC); **online attribution is not.**

### **G6. LLM-based operational log triage and RCA in HPC** — emerging 2023→2026, accelerating
Venues: HPCSYSPROS23 (LANL, first honest LLM-vs-classical comparison), MODA26 (CEA weak-signal clustering), HPC-ODA'26 CFP topic 6 explicitly names LLMs, SC26 **AgenticAI4HPC'26** (brand new).
**Evidence of the gap:** the only HPC-specific data point in the literature is a 2023 workshop paper reporting "more explainable, more expensive."
**The archival framing:** evaluate LLM/agentic RCA against a labelled corpus of real HPC incidents with cost and latency budgets. **This will be published by someone in 2027 — the window is now.**

### **G7. Safe release of HPC operational data (anonymization / governance)** — recurrence 2024–2026
Venues: MODA24 (ORNL repository), SC24 BoF, SC25 BoF, HPC-ODA'26 CFP topic 3.
**Evidence of the gap:** SC25 BoF poll rated public ODA dataset availability at **1.6/5** — the lowest score recorded.
**The archival framing:** a privacy/utility trade-off study — how much can job-level telemetry be anonymized before ODA analytics (anomaly detection, runtime prediction) degrade? M100 ExaData and Fugaku data exist as raw material. **Zero papers.**

### **G8. HPC-specific carbon-aware operation under fixed capacity** — recurrence 2024–2026
Venues: JSSPP25, EESP25/26, Sustainable Supercomputing SC24/25/26, SC26 RISE.
**Why the cloud literature does not transfer:** no workload migration, no elastic capacity, national-grid and district-heating coupling, allocation-based fair-share instead of price.
**The archival framing:** a production-scale evaluation of carbon-aware deferral under fair-share constraints, with measured (not modelled) carbon.

### **G9. Login-node / shared-service abuse control as closed-loop control** — recurrence 2023–2025
Venue: HPCSYSPROS (Arbiter 3 is **L7/D5** — deployed closed-loop with automatic enforcement).
**The gap:** a production closed-loop controller exists and has **never been evaluated in a peer-reviewed archival paper** (false-positive rate, user-behaviour effect, stability/oscillation).

### **G10. Counterfactual evaluation of operational policy changes** — meta-problem, recurrence 2023–2026
Venues: MODA23 (HPE fast scheduling simulator), MODA25 (duration-informed scheduler, simulation-only), SC25 Sustainable Supercomputing ("HPC digital twins for scheduling evaluation"), SC25 Digital Twins Workshop.
**Why it blocks everything:** every L6/L7 result in this corpus stops at simulation because you cannot A/B-test a production supercomputer. ExaDigiT (SC24) proves the digital-twin substrate is now credible.
**The archival framing:** a validated methodology for evaluating scheduling/power/cooling policy changes against a digital twin, with error bars against the real system. **ExaDigiT solved the physics; nobody has done the policy-evaluation methodology.**

---

## Practical guidance for a KISTI researcher

- **The tightest fit for a first SC Technical Paper attempt** is **G2** (does efficiency reporting change user behaviour) or **G1** (quantified silent-defect capacity loss): both need only a production system, a monitoring stack, and a disciplined study design — no new algorithms.
- **The highest-leverage venue to enter now** is **HPC-ODA 2026 at SC26** (1st edition, Nov 2026, IEEE Xplore, 8-page full papers, PC chaired by LRZ/BU/ORNL/NERSC/HPE). A first-edition workshop with 8 years of pent-up community demand and no established paper canon is the cheapest possible entry point into this community — and its PC is exactly the set of people who would review an eventual SC submission.
- **MODA26's rename to "Monitoring, Observability, and Operational Data Analytics"** signals the community is adopting cloud-SRE vocabulary. Expect observability/tracing/SLO framings to be well-received in 2027.
- **Do not target FTXS** for operational work — it has been rescoped to AI trustworthiness for SC26.
- **Watch SC26's ECHO** (1st, Edge-Cloud-HPC Operational Continuum) and **AgenticAI4HPC'26** (1st) — both are brand-new operational lanes with no incumbents.

---

## Sources

[HPC-ODA workshop 2026](https://hpc-oda.org/workshop2026/) · [HPC-ODA events archive (BoF series)](https://hpc-oda.org/events/) · [SC25 ODA BoF "Mind the Gap"](https://hpc-oda.org/events/2025-sc25-oda-bof/) · [SC24 ODA BoF](https://hpc-oda.org/events/2024-sc24-oda-bof/) · [MODA workshop series (Univ. Basel)](https://hpc.dmi.unibas.ch/research/moda/) · [MODA main site / MODA26 program](https://moda.dmi.unibas.ch/) · [MODA24 program](https://moda.dmi.unibas.ch/wp-content/uploads/2024/12/index24-program.html) · [ISC 2020 workshops LNCS](https://link.springer.com/book/10.1007/978-3-030-59851-8) · [ISC 2021 workshops LNCS](https://link.springer.com/book/10.1007/978-3-030-90539-2) · [ISC 2022 workshops LNCS](https://link.springer.com/book/10.1007/978-3-031-23220-6) · [ISC 2023 workshops LNCS](https://link.springer.com/book/10.1007/978-3-031-40843-4) · [ISC 2024 workshops LNCS](https://link.springer.com/book/9783031737152) · [ISC 2025 workshops LNCS](https://link.springer.com/book/10.1007/978-3-032-07612-0) · [SC26 — 50 accepted workshops](https://sc26.supercomputing.org/2026/04/a-gold-standard-sc26-welcomes-50-workshops-to-chicago/) · [SC25 — 44 accepted workshops](https://sc25.supercomputing.org/2025/05/announcing-the-44-accepted-workshops-for-sc25/) · [HPCSYSPROS 2020 proceedings](https://github.com/HPCSYSPROS/Workshop20) · [HPCSYSPROS 2021 proceedings](https://github.com/HPCSYSPROS/Workshop21) · [HPCSYSPROS22](https://sighpc-syspros.org/workshops/2022/) · [HPCSYSPROS23](https://sighpc-syspros.org/workshops/2023/) · [HPCSYSPROS24](https://sighpc-syspros.org/workshops/2024/) · [HPCSYSPROS24 DOIs](https://github.com/HPCSYSPROS/Workshop24) · [HPCSYSPROS25](https://sighpc-syspros.org/workshops/2025/) · [FTXS workshop series](https://sites.google.com/site/ftxsworkshop/) · [FTXS 2023](https://sites.google.com/view/ftxs2023) · [FTXS 2024](https://sites.google.com/view/ftxs2024) · [FTXS 2024 front matter (14th edition)](https://conferences.computer.org/sc-wpub/pdfs/SC-W2024-6oZmigAQfgJ1GhPL0yE3pS/555400a470/555400a470.pdf) · [dblp: FTXS](https://dblp.org/db/conf/ftxs/index.html) · [dblp: FTXS 2021](https://dblp.org/db/conf/ftxs/ftxs2021.html) · [dblp: FTXS 2022](https://dblp.org/db/conf/ftxs/ftxs2022.html) · [PMBS workshop](https://pmbs-workshop.github.io/) · [ProTools series (VI-HPS)](https://www.vi-hps.org/symposia/protools/protools.html) · [HPCTESTS 2023](https://olcf.github.io/hpc-system-test-wg/hpctests/hpctests2023.html) · [HPCTESTS 2024](https://olcf.github.io/hpc-system-test-wg/hpctests/hpctests2024.html) · [HPCTESTS 2025](https://olcf.github.io/hpc-system-test-wg/hpctests/hpctests2025.html) · [HUST workshop](https://hust-workshop.github.io/) · [dblp: SC workshops volumes](https://dblp.org/db/conf/sc/index.html) · [dblp: PDSW](https://dblp.org/db/conf/pdsw/index.html) · [dblp: JSSPP](https://dblp.org/db/conf/jsspp/index.html) · [JSSPP](https://jsspp.org/) · [JSSPP 2024 program](http://jsspp.org/index.php?page=program24) · [JSSPP 2025 program](http://jsspp.org/index.php?page=program25) · [IPDPS 2025 workshops](https://www.ipdps.org/ipdps2025/2025-workshops.html) · [IPDPS 2026 workshops](https://www.ipdps.org/ipdps2026/2026-workshops.html) · [HPDC 2024 workshops](https://hpdc.sci.utah.edu/2024/workshops.html) · [HPDC 2025 workshops](https://hpdc.sci.utah.edu/2025/workshops.html) · [HPDC 2026 workshops](https://hpdc.sci.utah.edu/2026/workshops.html) · [PERMAVOST](https://permavost.github.io/) · [PERMAVOST 2025 program](https://permavost.github.io/2025.html) · [dblp: SNTA](https://dblp.org/db/conf/snta/index.html) · [dblp: SNTA 2024](https://dblp.org/db/conf/snta/snta2024.html) · [EESP workshop](https://ayeshaafzal91.github.io/eesp/) · [EESP 2025 program](https://ayeshaafzal91.github.io/eesp/2025.html) · [SC25 Sustainable Supercomputing](https://sites.google.com/view/sc25/home) · [PIKA (MODA23)](https://link.springer.com/chapter/10.1007/978-3-031-40843-4_22) · [ML-Based Facilities Supervision (MODA23)](https://link.springer.com/chapter/10.1007/978-3-031-40843-4_23) · [Explainable Fault Detection (MODA21)](https://link.springer.com/chapter/10.1007/978-3-030-90539-2_25) · [Fugaku monitoring platform (MODA21)](https://link.springer.com/chapter/10.1007/978-3-030-90539-2_24) · [Rule-Based Thermal Anomaly Detection (MODA22)](https://link.springer.com/chapter/10.1007/978-3-031-23220-6_18) · [LASSi for ARCHER (MODA20)](https://link.springer.com/chapter/10.1007/978-3-030-59851-8_16) · [Duration-Informed Workload Scheduler (MODA25)](https://link.springer.com/chapter/10.1007/978-3-032-07612-0_1) · [eBPF I/O monitoring (MODA25)](https://link.springer.com/chapter/10.1007/978-3-032-07612-0_3) · [LLview (MODA25)](https://link.springer.com/chapter/10.1007/978-3-032-07612-0_4) · [Ookami longitudinal monitoring (MODA25)](https://link.springer.com/chapter/10.1007/978-3-032-07612-0_5) · [Heterogeneous Syslog Analysis (HPCSYSPROS23, Zenodo)](https://zenodo.org/records/10223395) · [Heterogeneous Syslog Analysis (ACM)](https://dl.acm.org/doi/fullHtml/10.1145/3624062.3624128) · [ExaDigiT SC24 paper](https://impact.ornl.gov/en/publications/a-digital-twin-framework-for-liquid-cooled-supercomputers-as-demo/) · [Frontier power management (arXiv)](https://arxiv.org/abs/2408.01552) · [GPU memory corruption on Summit (ICS'24)](https://www.ornl.gov/publication/understanding-gpu-memory-corruption-extreme-scale-summit-case-study) · [Prodigy (SC'23)](https://dl.acm.org/doi/10.1145/3581784.3607076) · [RUAD (FGCS 2023)](https://dl.acm.org/doi/10.1016/j.future.2022.12.001) · [Multi-level anomaly prediction (CF'22)](https://dl.acm.org/doi/10.1145/3528416.3530864) · [DCDB Wintermute (HPDC'20)](https://dl.acm.org/doi/abs/10.1145/3369583.3392674) · [dblp: Alessio Netti](https://dblp.org/pid/211/5921.html) · [M100 ExaData (Scientific Data)](https://www.nature.com/articles/s41597-023-02174-3)agentId: a4b9ae21bec1718af (use SendMessage with to: 'a4b9ae21bec1718af', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 185376
tool_uses: 140
duration_ms: 1175997</usage>
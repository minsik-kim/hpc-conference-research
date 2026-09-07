I've completed the research. Web search budget ran out partway, but I got the primary sources directly from cug.org. Here are the notes.

---

# CUG + Vendor Ecosystem Mining for HPC Telemetry/AIOps Research Questions
**Compiled 2026-09-06. All URLs verified by fetch. Numbers quoted from source PDFs.**

## 0. Method, coverage, and honesty statement

**What I did:** fetched `cug.org/proceedings/` directory, then `at_a_glance.html`, `by_auth.html`, `by_sub_type.html` and individual PDFs for CUG 2020–2025. Verified archival citations through the Crossref REST API and USENIX.

**Coverage limits — read these before trusting completeness:**
- **CUG 2026: NOT ACCESSIBLE.** `https://cug.org/proceedings/cug2026_proceedings/` returns **404** (proceedings not yet posted; the 2025 folder is the newest, timestamped 2026-02-23). The live program at `https://ssl.linklings.net/conferences/cug/cug2026_program/views/at_a_glance.html` is **blocked by robots.txt**, and `https://cug.org/cug-2026-technical-program/` contains only logistics. **I have zero verified content for CUG 2026.** Treat any CUG 2026 claim from any source as unverified until the proceedings post.
- **CUG 2020: PARTIAL.** The proceedings exist (virtual event, sessions dated **November 2020**), but the `at_a_glance` fetch returned only the "New Special Paper Session" block. My 2020 list is incomplete.
- **WebSearch budget exhausted** (200/200) partway through Part B. Vendor audit is therefore narrower than scoped: I verified NVIDIA Mission Control docs, DDN Insight, HPE developer blog index, and NREL's AIOps report page directly, plus HPE's own CUG decks. Intel/VAST/others: **NOT COVERED** — flag as an open task.
- **dblp and ACM DL are blocked** through this environment's proxy (403/robots). Citation verification went through **Crossref** and **usenix.org**, which is sufficient for DOI-bearing venues but cannot prove a negative. Every "NO CLOSE ARCHIVAL WORK FOUND" below therefore means *"not found in this session's verified searching"* — a strong hint, not a proof.
- **Some CUG PDFs are simply not posted.** Notably the CUG2021 HPE AIOps paper and the CUG2022 Fallout paper (details in §1). I mark these `PDF NOT POSTED`, not "does not exist."

**On CUG publication form (verified, from the CUG 2026 CFP):** four submission types — **Paper** ("full-length abstracts presenting novel results", requires a final paper), **Presentation** ("presentation-only… not requiring a final paper"), **BoF**, **Tutorial**. On review: papers "will be considered for publication in a ACM International Conference Proceedings Series"; "Papers submitted by the due date will be reviewed for the proceeding publication"; "publication in the proceeding may require an **additional round of reviews**." → **A CUG "Paper" is an accepted abstract with a written paper; it is not by default a peer-reviewed archival publication.** Whether specific CUG 2024/2025 papers actually landed in ACM ICPS: **UNKNOWN — I could not verify.** Source: https://cug.org/cug-2026-call-for-papers/

---

## 1. Year-by-year CUG map, 2020–2026

Form codes: `[PAPER]` = CUG paper track (see caveat above); `[PRES]` = presentation-only; `[BOF]`; `[TUT]`; `[VENDOR]` = authored solely by HPE/vendor staff.

### CUG 2020 (virtual, Nov 2020) — PARTIAL COVERAGE
| Title | Who | Form | Note |
|---|---|---|---|
| Deriving Workload Expectations: Monitoring and Analysis Using HPC Job Profiles | Joshi Fullop, Brett L. Layman (LANL) | [PAPER] | time-series monitoring, anomaly detection, workload characterization |
| I/O Performance Characterization and Prediction through Machine Learning on HPC Systems | Wan, Wolf, Wang, Choi, Ostrouchov, Chen, Podhorszki, Logan, Mehta, Klasky, Pugmire (ORNL) | [PAPER] | reported "75% when SVM is used" |
| Performance and Power Modeling and Prediction Using MuMMI and Ten Machine Learning Methods | Wu, Taylor (ANL/UChicago), Lan (IIT) | [PAPER] | "prediction error rates…less than 10% for most cases"; XC40/BG-Q |
| Enabling Power Measurement and Control on Astra | Grant, Hammond, Laros, Levenhagen, Olivier, Pedretti, Ward, Younge (SNL) | [PAPER] | non-Cray Arm system; power telemetry+control |
| Advanced Topics in Configuration Management | Bak, Kleinman (HPE) | [PRES][VENDOR] | CFS |

Index: https://cug.org/proceedings/cug2020_proceedings/at_a_glance.html

### CUG 2021 (virtual)
| Title | Who | Form | URL / status |
|---|---|---|---|
| trellis — An Analytics Framework for Understanding Slingshot Performance | Srinivasan, Mallick, Maschhoff, Ayyalasomayajula (HPE) | [PAPER][VENDOR] | https://cug.org/proceedings/cug2021_proceedings/includes/files/pap115s2-file1.pdf |
| **AIOps: Leveraging AI/ML for Anomaly Detection in System Management** | Serebryakov, Hanson, Cader, Nanjundaiah, Subrahmanya (HPE) | [PAPER][VENDOR] | **PDF NOT POSTED** (by_auth shows "view only") — the single most-cited HPE AIOps CUG artifact is *not publicly readable* |
| Integrating System State and Application Performance Monitoring: Network Contention Impact | Brandt, Tucker, Hammond, Schwaller, Gentile, Stroup, Cook (SNL, OGC) | [PAPER] | **PDF NOT POSTED** |
| Real-time Slingshot Monitoring in HPCM | Priya K, Kurian, Deshpande (HPE) | [PRES][VENDOR] | PDF NOT POSTED |
| Analytic Models to Improve Quality of Service of HPC Jobs | Naureen, Kurian, Chilumukuru (HPE) | [PRES][VENDOR] | PDF NOT POSTED |
| Blue Waters System and Component Reliability | Bode, King, Mendes, Kramer, Jha, Ford, Davis, Dramstad (NCSA) | [PAPER] | .../pap102s2-file1.pdf |
| Configuring and Managing Multiple Shasta Systems (Perlmutter) | Botts, Crisler, Gaur, Jacobsen, Longley, Lovell-Troy, Poulsen, Roman, Samuel (NERSC+HPE) | [PAPER] | .../pap110s2-file2.pdf |
| Architecture and Performance of Perlmutter's 35 PB ClusterStor E1000 All-Flash File System | Lockwood, Chiusole, Gerhardt, Lozinskiy, Paul, Wright (NERSC) | [PAPER] | .../pap120s2-file1.pdf |
| Slurm on Shasta at NERSC | Samuel, Jacobsen, Gaur | [PAPER] | .../pap109s2-file2.pdf |
| Declarative automation of compute node lifecycle through Shasta API integration | Wofford, Pelzel (LANL) | [PAPER] | Kraken |
| Cray EX Shasta v1.4 System Management Overview | Longley (HPE) | [PRES][VENDOR] | |

### CUG 2022
| Title | Who | Form | URL / status |
|---|---|---|---|
| Fallout: System Stand-up Monitoring and Analysis Package | Brandt (SNL), Showerman (NCSA), Roman (NERSC), et al. | [PAPER] per program | **PDF 404** — `pres111s2.pdf` not retrievable |
| Slingshot Fabric Manager Monitor | John Stile (NERSC) | [PRES] | .../pres116s2.pdf |
| Using Loki for Simplifying the Usage of Shasta Logs | Siqi Deng (NERSC) | [PRES] | .../pres122s1.pdf |
| Augmenting HPCM System Management with Phoenix | Matt Ezell (ORNL) | [PRES] | anchor only |
| Cluster Health Check Diagnostics Suite | Kurian, Chilumukuru (HPE) | [PRES][VENDOR] | .../pres108s1.pdf |
| Crayport to HPE DCE Migration: Bidirectional Incident Management | Gens, Gann, Bautista (NERSC) | [PRES] | .../pres123s1.pdf |
| Network Integration of Perlmutter at NERSC | Basheer, Roman, et al. | [PAPER] | .../pap117s2-file1.pdf |
| Configuring and Managing The Perlmutter Supercomputer | Roman, Stile, et al. (NERSC) | [PAPER] | .../pap118s2-file1.pdf |
| Automated service monitoring in the deployment of ARCHER2 | Leach, Cass, et al. (EPCC/HPE) | [PAPER] | .../pap103s2-file1.pdf |
| HPE Performance Cluster Manager (HPCM) Update — incl. "AIOPs anomaly detection for IT metrics" | Hanson (HPE) | [BOF][VENDOR] | .../bof104s1-file1.pdf |
| Cray System Management for HPE Cray EX Systems | Longley (HPE) | [TUT][VENDOR] | .../tut102s2-file1.pdf |
| Crossroads: Status on Design, Deployment, Acceptance, Operation | Agelastos, Stroup (SNL), Green (LANL) | [PRES] | |
| Liquid Cooling for HPC, Enterprise and Beyond | Vinson, Zeiler, Slaby (HPE) | [PRES][VENDOR] | |

### CUG 2023
| Title | Who | Form | URL |
|---|---|---|---|
| **STREAM: A Scalable Federated HPC Telemetry Platform** | Adamson, Osborne, Lester, Palumbo (ORNL NCCS) | [PAPER] | .../cug2023_proceedings/includes/files/pap155s2-file1.pdf |
| **Evaluating and Influencing Extreme-Scale Monitoring Implementations** | Barry (HPE), Brandt, Gentile (SNL), Morrone, Scott, Shoga (LLNL), Roman (LBNL), Tucker (OGC) | [PAPER] | .../pap149s2-file1.pdf |
| Frontier Node Health Checking and State Management | Ezell (ORNL) | [PAPER] | .../pap151s2-file1.pdf |
| Monitoring and characterizing GPU usage | Weakley, Michael, Thota, Huber, Fulton, Kusz (Indiana U) | [PAPER] | .../pap139s2-file1.pdf |
| Powersched: A HPC System Power and Energy Management Framework | Marquardt, Mäder, Schiffmann, Simmendinger, Wilde (HPE) | [PAPER][VENDOR] | .../pap113s2-file1.pdf |
| Power Capping of Heterogeneous Systems | Nieuwsma, Wilde (HPE) | [PAPER][VENDOR] | pap103 |
| HPE's Holistic system Power and energy Management (HPM) vision | Wilde, Kaplan, Warner (HPE) | [PRES][VENDOR] | |
| **System Monitoring with CSM and HPCM** (tut107) | Hanson (HPE) + co-decks | [TUT] | posted decks: file1 = **NERSC OMNI deck by Siqi Deng (LBNL OTG)**, file3 = Shasta log-monitoring improvements. *Attribution caveat: the tutorial slot is HPE-led but the posted PDFs are site-authored.* |
| Advanced Topics for Cray System Management | Longley (HPE) | [TUT][VENDOR] | .../tut104s2-file1.pdf |
| Analyzing the Slingshot Fabric with the Slingshot Dashboard | Mahadevan, Godfrey, Mendes (HPE) | [TUT][VENDOR] | **no PDF posted** |
| Systems Monitoring Working Group BOF | West (BoM), Lopatina (LANL), Leak (NERSC) | [BOF] | |
| HPCM Users BOF | Hanson, Boac (HPE) | [BOF][VENDOR] | |
| Deploying a Parallel File System for the World's First Exascale Supercomputer (Orion, 679 PB) | Hanley, Leverman, Coffman, Gipson, Brumgard, Mohr (ORNL) | [PAPER] | .../pap122s2-file1.pdf |
| Balancing Workloads in More Ways than One (Frontier C5, expanded monitoring) | Melesse Vergara et al. (ORNL) | [PAPER] | |

### CUG 2024
| Title | Who | Form | URL |
|---|---|---|---|
| **EMOI: CSCS Extensible Monitoring and Observability Infrastructure** | Benini, Hanson (HPE), Gianolli, Piccinali, Brambilla, Marano, Ricciardi, Frisoni, Conciatore (CSCS+HPE) | [PAPER] | .../cug2024_proceedings/includes/files/pap113s2-file1.pdf |
| **CADDY: Scalable Summarizations over Voluminous Telemetry Data for Efficient Monitoring** | Mitra, Ragland, Zambrano, Mallick, Vollmer, Kelley, Mohan (HPE, "HPC and Slingshot BU") | [PAPER][VENDOR] | .../pap112s2-file1.pdf |
| **Multi-stage Approach for Identifying Defective Hardware in Frontier** | Hagerty (ORNL), Warner (HPE), Webb | [PAPER] | .../pap123s2-file1.pdf |
| From Frontier to Framework: Enhancing Hardware Triage for Exascale | Wazirzada, Mehta, Phadke (HPE) | [PAPER][VENDOR] | .../pap121s2-file1.pdf |
| Automated Hardware-Aware Node Selection for Cluster Computing | Sopena Ballesteros, Chesi, Gila, Klein (CSCS/ETH) | [PAPER] | .../pap106s2-file1.pdf |
| Towards the Development of an Exascale Network Digital Twin | Holmen (ORNL), Newaz (Oakland U), et al. | [PAPER] | .../pap140s2-file1.pdf |
| Nine Months in the life of an all-flash file system | Gerhardt, Simms, Bhimji (LBNL/NERSC), Moore (HPE), et al. | [PAPER] | .../pap141s2-file1.pdf |
| Swordfish/Redfish and ClusterStor | Kling Petersen, Morneau, Matthews, Rutman (HPE) | [PAPER][VENDOR] | **file1 → 404; file2 → effectively empty.** Content NOT RETRIEVABLE |
| HPE Cray EX Power Monitoring Counters | Martin, Collum, Byland (HPE) | [PRES][VENDOR] | .../pres127s2.pdf |
| Updated Node Power Management For EX255a/EX254n Blades | Collum, Martin (HPE) | [PRES][VENDOR] | |
| First Analysis on Cooling Temperature Impacts on MI250x Exascale Nodes | Wilde (HPE), Ott (LRZ), Guyan (HPE) | [PRES] | |
| EVeREST: Effective and Versatile Runtime Energy Saving Tool | Yue, Mehta, Wilde (HPE/UMN) | [PRES][VENDOR] | |
| CSM-based Software Stack Overview 2024 (SMA 1.8/1.9, CSM 1.4/1.5) | Longley, Sollom (HPE) | [PRES][VENDOR] | .../pres125s2.pdf |
| Overview of HPCM | Guyan, Miller (HPE) | [PRES][VENDOR] | anchor only |
| Monitoring, Tuning, and Troubleshooting a CSM system | Longley, Sollom (HPE) | [TUT][VENDOR] | |
| High Performance Data-centre Digital Twins | Maiterth (ORNL), Dykes, Jones (HPE), et al. | [BOF] | .../bof103s1-file1.pdf |
| AI/ML for HPC Workload Analysis | Konate, Gerber (LBNL) | [BOF] | |
| HPE Slingshot BoF | Treger (HPE) | [BOF][VENDOR] | |

### CUG 2025
| Title | Who | Form | URL |
|---|---|---|---|
| **Monitoring HPE Cray HPC systems** (tut106) — the single richest public artifact on the HPE monitoring stack | Longley, Miller, Guyan, Vasudevan (HPE) | [TUT][VENDOR] | .../cug2025_proceedings/includes/files/tut106s2-file1.pdf |
| CUG SIG System Monitoring Working Group BoF | Benini (CSCS), Lopatina (LANL), Hanson, Guyan (HPE) | [BOF] | .../bof102s1-file1.pdf — **posted deck is actually "A glimpse of YAULT" (Holanda Rusu, Benini, CSCS)**, eBPF syscall tracing for application identification. Program blurb mentions "operational data analytics (ODA)" but the posted deck does not cover it. |
| Causality inference for Digital Twins in GPU Data Centers and Smart Grids | Hong Enriquez, Prakash, Taheri, Dhakal (HPE Labs); Maiterth, Brewer (ORNL) | [PAPER] | .../pap118s2-file1.pdf |
| Co-design, deployment and operation of a Modular Data Centre (MDC) | Alam (Bristol), Moore, Over, Barnes, McIntosh-Smith, Podstata, Harris, Akinyemi | [PAPER] | .../pap133s2-file1.pdf |
| Evolving HPC services to enable ML workloads on HPE Cray EX | Schuppli et al. (CSCS/ETH) | [PAPER] | .../pap159s2-file1.pdf |
| Alps, a versatile research infrastructure | Martinasso, Klein, Schulthess (CSCS) | [PAPER] | .../pap157s2-file1.pdf |
| The HPE Slingshot 400 Expedition | Azgomi, Roweth, Faanes, Treger (HPE) | [PAPER][VENDOR] | .../pap109... |
| Slingshot Host Software Ethernet Tuning | Bissa, Ziemba, Roweth, Godfrey (HPE) | [PRES][VENDOR] | |
| A Brief Summary of the HPCM Evolution | Miller, Morecroft, Guyan (HPE) | [PRES][VENDOR] | |
| Rev Up Compute Node Reboots: 2x to 5x Faster | Walker (HPE), Selwood (Met Office) | [PAPER] | "300+% improvement" |
| System Visualization Using Rackmap | Guyan (HPE) | [PRES][VENDOR] | no PDF |
| Experimenting with Security Compliance Checking using ReFrame | Holanda Rusu, Basso, Gamboni, Zambrino, Benini (CSCS) | [PAPER] | .../pap107s2-file1.pdf |

### CUG 2026
**NOT FOUND / NOT ACCESSIBLE.** No proceedings directory; program blocked by robots.txt. Recommend re-checking `https://cug.org/proceedings/` in early 2027.

---

## 2. Operational problem inventory (evidence-based)

Each entry: **Problem → Reporter → What they built → What they said didn't work → Quantitative evaluation?**

**P1. Telemetry message bus scales, producers/consumers don't; schema drift corrupts the archive.**
- Reporter: ORNL NCCS (Adamson et al., CUG2023 STREAM, [PAPER]).
- Built: Kafka-centric federated bus (6 brokers on OpenShift), Kafka Connect for remote sources, Elasticsearch data lake, Grafana.
- Didn't work: *"STREAM's biggest pain point has been producers and consumers, not the Kafka bus itself."* Sensor data *"has not been standardized into a universal format and may as we have found, change throughout the lifetime of the data. This can cause significant and unexpected errors."* Bad topic names forced re-indexing (*"This can be a slow process"*). Broker failure → *"TBs of recovery traffic."* Documentation *"incomplete, inconsistent, and confusing."*
- Quantitative: yes, operational — 300M msgs/day, 200+ topics, 1.3 TB/day, 72 MB/s avg, 105 MB/s peak, 300 MB/s incl. replication, 7.5 GB/s theoretical ceiling. **No controlled experiment.**

**P2. The vendor telemetry service could not carry production data rates.**
- Reporter: Sandia/LLNL/LBNL + HPE co-author (CUG2023 pap149, [PAPER]).
- Finding: CSM `telemetry-api` was *"unreliable and often inefficient. It stopped feeding data at random times, and frequently caused Kafka rebalancing events"*; *"could not handle the data rate (100K to 1M messages per second)"* at Perlmutter full scale.
- Also: LDMS credential distribution at boot *"not only slow but unreliable… causes the boot-time Ansible plays to fail"*; single fixed worker `ncn-w001` bottleneck: *"If ncn-w001 is unavailable or overloaded then a boot will either be extremely slow or fail altogether."*
- Built: site bypass — NERSC custom LDMS store plugin → VictoriaMetrics → OMNI; LLNL LDMS→Kafka(Avro)→Kafka Connect→Elasticsearch, plus MirrorMaker→Sonar/Cassandra.
- Quantitative evaluation: **partial.** Monitoring overhead reported as *"no statistically significant performance penalty"* — but no method or numbers given for that claim. This is a notable evidence gap.

**P3. Encoding/format divergence between vendor and sites makes cross-site tuning non-transferable.**
- Reporter: same paper. *"LLNL and HPE have different formats. LLNL uses Avro encoding… HPE sends one metric per message in JSON format"*; LLNL's Avro yields *"significantly fewer bytes transmitted."* Consequence stated explicitly: *"the variation in the Kafka format means there can't easily be a rule of thumb in one implementation that extends to the other."*
- Also: CSM ships *"an internal version of LDMS which is significantly behind the latest LDMS release"*, with *"LDMS samplers that have not been up-streamed and may be proprietary"*, and site customization *"would need to be re-implemented with each CSM update."*
- Quantitative: no.

**P4. Fabric counter acquisition is itself expensive; counter selection is ad hoc.**
- Reporter: same paper. Slingshot switches expose *"over a thousand counters per port and over 64K total port counters per switch"*; El Capitan defaults to *"roughly forty"* counters *"from potentially hundreds"*; `dump_counters` takes *"about half a second"* per switch. *"We would like to work with HPE to identify more efficient port counter access mechanisms."*
- Quantitative: yes (counts + 0.5 s), but **no study of which counters matter** — that is the research gap.

**P5. Fabric telemetry volume defeats interactive analytics.**
- Reporter: HPE (CADDY, CUG2024, [PAPER][VENDOR]). Explicitly: *"Fabric AIOps' reliance on voluminous telemetry data generated from Slingshot's nodes and switches poses significant challenges for traditional disk-based storage solutions."*
- Built: hierarchical temporal/spatial "Bins" holding 5 Welford moments per counter; Ray-distributed in-memory store.
- Quantitative: **yes, the most rigorous vendor evaluation found.** Compression 425x (10-min bins) / 600x (15-min) / 1200x (30-min); single-frame fetch 355 ms → 151 ms (group level, −57%) / 267.51 ms (port level, −25%); ingest overhead **+32.5%** (0.7589 s → 1.007 s per 1M events); 300K events/min ingest; testbed 8 groups × 8 switches × 64 ports = 4096 ports, 4 counters (rxBW, txBW, rxCongestion, txCongestion); node = 128 AMD EPYC 7002 cores, 196 GB RAM. Live-mode horizon extended from **10 minutes to multiple days**. Stated limit: *"the ideal temporal window size should not exceed 3 hours."*
- Didn't work / limits: single-node evaluation only; 4 counters only; extreme compression *"may reduce granularity for certain anomaly detection workloads."* Also HPE's earlier trellis (CUG2021) admitted *"several petabytes"* of raw telemetry over 30 days and a *"trade-off between interactivity and computation time."*

**P6. Silent defective hardware ("bad actors") is not caught by boot-time health checks.**
- Reporter: ORNL + HPE (Hagerty, Warner, Webb; CUG2024, [PAPER]) — the strongest quantitative operational paper in the corpus.
- Built: three strategies — (1) targeted leadership-scale LAMMPS failure isolation, (2) formal HACC job-completion study in phases, (3) periodic single-node screening via Slurm **backfill**.
- Quantitative: 244 LAMMPS jobs → *"19 cases of defective hardware were successfully identified and repaired."* At 4096 nodes / 500 W TDP: *"17 of 50 jobs failed"*; with +100 mV HBM and default memory clock: *"11 of 50 jobs failed."* *"75% reduction in power faults from Phase 2 to Phase 4."* Backfill screening: *"Nearly 6 million single-node tests"* by April 2024; 1.9M in the Oct 2023–Apr 2024 window; per-test failure counts (BabelStream 562,671 runs / 2,796 failures; rocHPL 328,576 / 162; AMG 337,684 / 129; oblex 184,424 / 124; rocPRIM 304,361 / 24; LAMMPS 175,418 / 12); **99 unique failing nodes** in 6 months, classified as 54 software bugs, 27 transient performance, 12 GPU HBM UE, 11 numerical instability, 4 non-reproducible; backfill LAMMPS *"averaged identifying one failure per 14,618 tests."* Frontier: 9,408 nodes, 37,632 MI250X @ 560 W TDP.
- **Didn't work — explicitly:** the weekly `checknode` screen produced *"39,437 screens with no failures"* over 6 months and was **removed from production in December 2023** as ineffective (test duration too short: <1 min vs 24 min for backfill LAMMPS); the epilog variant was *"too disruptive to user workloads."* Also: *"Same error message can also be triggered from compiler bugs."*

**P7. Node health checking is script-and-rule based, with no published accuracy.**
- Reporter: ORNL (Ezell, CUG2023 pap151, [PAPER]). `checknode` bash script; full run at boot, reduced set in Slurm epilog; drains nodes with reason string; auto-resume if drain reason was self-set; SEC (Simple Event Correlator) over controller/console/syslog.
- Quantitative: **none.** Zero numbers on node counts tested, durations, drain counts, false positives. One qualitative datum: *"mean time between failure on a system this size is hours, it's not days."* One concrete defect: *"a bug in the power management firmware that prevented the CPU from going into burst mode"* causing MPI all-to-all degradation.
- HPE's parallel effort (Wazirzada et al., CUG2024, [VENDOR]) is a YAML-DSL **rule-based decision tree**, explicitly *no ML*, over node-controller debug JSON + Redfish; Frontier context *"more than 9400 compute nodes"*, *"over 150,000 node-level components"*; **zero evaluation numbers**; authors concede it *"is not a substitute for the discipline of system health checks."*

**P8. Cross-source attribution: job energy from telemetry vs from the scheduler disagrees, and the scheduler is not trusted.**
- Reporter: CSCS + HPE (EMOI, CUG2024, [PAPER]). Job 2665753: **5,663,156 J (telemetry) vs 5,662,307 J (Slurm)**; 984 jobs analyzed over 4 node types. Direct quote: *"Slurm on the other hand, shows sometimes a weird behaviour and cannot therefore always be trusted."*
- Also: Cray PM collection at **10 Hz**, telemetry pipeline at **~1 Hz**.
- Didn't work: the CSM-bundled Kafka *"does not expose any external listener, which means external applications can't connect to the Kafka cluster"*; message bundling of many sensors per message *"is not suitable for ingestion into ElasticSearch"*; **Fluent Bit rejected** — *"we couldn't make it stable for large throughputs."*
- Quantitative evaluation of any detection method: **no.** EMOI reports **no GB/day, no cardinality, no retention.**

**P9. Storage performance anomalies are real, frequent, and only found by scheduled active probing.**
- Reporter: NERSC + HPE (CUG2024, [PAPER]) — the best storage numbers in the corpus. Perlmutter all-flash Lustre: 36 PB, >7 TB/s theoretical peak, 16 MDS, 274→298 OSS/OST, 3,480 NVMe drives, ~10,000 users at 20 TB / 20M inodes default quota.
- Built: *"daily, off-hours obdfilter-survey test… configured by NERSC staff in August of 2023"*; IOR on 32 GPU nodes writing/reading ~250 TB; CoV acceptance target *"8% or below."*
- Found: *"several OSTs intermittently… reporting very slow write rates between 25% and 50% lower than expected"*; fix moved write performance *"from 15.1 GB/s to 19.9 GB/s — a 30% improvement"*, minimum rates *"from 260 MB/s to 9,032 MB/s"*. Security patch (SafeRet) cost *"a decrease in mean write bandwidth values of 14%"*; enabling checksums cost *"a 17% drop in mean write bandwidth (from 673320 MB/s ± 31779 to 554012 MB/s ± 37846)"*. Root causes: NVMe garbage collection, Lustre allocator *"useless c1 loops"* (fix: `mb_c2_threshold=25`), trim frequency. Optimal OST fullness *"around a surprising 75% of file system capacity."* 2024 regression traced to *"a large number of OSTs as read only. This meant only about 50 OSTs were available."* Purge horizon ~365 days.
- Didn't work: passive telemetry alone did not surface these; active daily probing was required.

**P10. Power/cooling anomaly detection is shipped as a feature with no published algorithm or evaluation.**
- Reporter: HPE (CUG2025 tut106 [TUT][VENDOR]; CUG2022 HPCM BoF [BOF][VENDOR]).
- Claimed: AIOps uses *"machine learning and deep learning technologies to identify and report trends"*, giving *"real-time and offline anomaly detection, prediction for time-series monitoring data"*, univariate and multivariate, containerized; alerts when *"anomaly score exceeds the anomaly threshold"*, expiring *"after a predefined period of time"*. Example targets: CDU valve position, cooling pressure, CPU/GPU temperature. Enabled via `cm monitoring grafana dashboard enable [category]`.
- **No algorithm named. No threshold-selection method. No precision/recall. No deployment scale. No false-alarm data.** The CUG2022 BoF likewise lists *"AIOPs anomaly detection for IT metrics"* with nothing behind it.

**P11. Retention economics dominate the design, and defaults are aggressive.**
- Reporter: HPE (CUG2025 tut106). HPCM 1.13 defaults: **Kafka 1 day** (≤1.12: CrayEX telemetry 24 h, others 168 h), **OpenSearch 7 days**, **VictoriaMetrics 7 days**, **TimescaleDB 30 days** (deprecated for new deployments), Timescale compression at 7 days saving *">90% disk space"*. Slingshot monitoring called *"the big hitter for disk space."* Native monitoring interval configurable, example 5 s.
- Stack transitions recorded: Prometheus/TimescaleDB → **VictoriaMetrics**; Filebeat → **Fluent Bit**; Elasticsearch → **OpenSearch** (CSM/SMA 1.8: *"Moved from Elasticsearch to Opensearch (due to licensing change)"*); Alerta/Elastalert → **Alertmanager only**.
- Missing: *"does not provide explicit performance benchmarks, node scaling limits, or expected data volumes for different cluster sizes."* **The vendor does not publish a sizing model.**

**P12. Log pipeline throughput is a site-solved problem, and the fix is 20x.**
- Reporter: NERSC/LBNL OTG (Siqi Deng), CUG2023 tut107 deck. OMNI pipeline scaled *"From 100k/s To 2 million/s"* log messages, with the pre-fix bottleneck *"< 100k messages/s"*, an intermediate *"200k messages/s"*, and resourcing of *"2 CPU cores + 150MB Mem per pod x 64~128 pods"* (Promtail). Fixes: rsyslog scale-up + Kafka scale-out. Also documented ClusterStor and Cassini monitoring pipelines.
- Corroborating CUG2022 NERSC deck (Deng): consolidation goal *"One Monitoring UI (Grafana), One Query Language (PromQL/LogQL), One Notification Engine (Alertmanager)"*; Loki explicitly *"not for replacing Elasticsearch."*

**P13. Fabric management observability is thin enough that sites write their own poller.**
- Reporter: NERSC (Stile, CUG2022 [PRES]). Python app as a Kubernetes CronJob polling the Slingshot Fabric Manager REST API (health status; switch topology/online; port state) → VictoriaMetrics + Loki. Detects switches offline, port flapping, health degradation, API connectivity loss. 11 metrics. Reported difficulties: *visualizing non-numeric health states*, *storing long-term port state histories*, *integrating Kafka-streamed telemetry*. **No polling interval, switch/port counts, or data volume given.**

**P14. Facility-side monitoring catches problems that IT-side monitoring misses — with a benchmark-sized payoff.**
- Reporter: EPCC/HPE (ARCHER2, CUG2022 [PAPER]). Checkmk (Nagios derivative) + Graphite + Grafana, distributed per system group over TCP agents. **Rectifier-level power collected every 5 seconds** from cabinet controllers; Slurm `sinfo` node-state checks; SSH login probes; Lustre and Slingshot HSN checks; alerts by email including HPE pagers. ARCHER2: 5,860 nodes / 750,080 cores.
- Payoff, quantified: during HPL, power monitoring identified *"power cycling"* behavior; isolating those nodes moved Top500 performance **from 16.8 PF to 19.5 PF**.
- Didn't work / limit: *"Historical Graphite data granularity reduces over time to conserve disk space"* — i.e. downsampling destroyed the ability to do long-term fine-grained analysis. This is a first-class, concretely reported downsampling failure mode.

**P15. GPU utilization telemetry is deliberately degraded to avoid agent overhead — and the resulting picture is grim.**
- Reporter: Indiana University (CUG2023 [PAPER]). Rejected DCGM: *"DCGM appeared to have too intrusive of a footprint to be viable for deployment."* Built pynvml-based epilog-time collection, JSON into Slurm `AdminComment` (MariaDB), 4,000-record GPU ring buffers.
- Quantitative: 295,470 GPU jobs (Jul 2020–Mar 2023); **mean GPU utilization 11%**; **53% of jobs never accessed the GPU**; excluding non-users, mean 26%; 645 unique applications, 53% AI/ML, 99.6% of those Python.
- Failure modes: `AdminComment` 65,535-character limit *"occasionally truncating long-running multi-GPU jobs"*; nvml `gpuUtilization` measures *"percentage of time that the GPU was active"*, not core utilization.
- CSCS corroborates the agent problem from the other side (CUG2025 pap159): *"DCGM's lack of native scheduler-level resource isolation, requiring cluster-level rather than node-group-level data querying."*

**P16. Digital twins hit a telemetry timescale wall.**
- Reporter: ORNL/Oakland U (CUG2024 [PAPER]). Frontier: 9,408 EX235a nodes, Slingshot 11 three-hop dragonfly, *"80 groups: one management, five I/O, and 74 compute groups"*, 4 NICs/node.
- Core problem, verbatim: *"The switching technology of the dragonfly network is between 100 to 350ns, whereas Frontier system telemetry is typically collected at 15-second time quanta."* And: *"network-related telemetry data must be obtained by systematically profiling applications"* — i.e. the production stack does not expose it.
- Cost: *"replaying a single MPI rank on each node of Frontier would take more than 30 hours"* (vs 2-hour job limit); SST-Core speedup *"~7x, which still does not provide enough speedup."* Scale context: *"approximately 1.8 million jobs and counting have been run across Frontier"*; *"about six months of Frontier telemetry have been replayed."*
- Open: *"further investigation remains to find a way to validate NIC-based spyplots."* **No accuracy numbers.**

**P17. Causal inference on operational telemetry fails for lack of data, not lack of method.**
- Reporter: HPE Labs + ORNL (CUG2025 [PAPER]). Summit, *"27,648 Tesla V100 GPUs"* monitored over three years — yet the usable failure dataset was **127 failure event entries** with **11 features**. Methods: causal calculus / do-calculus, multivariate transfer entropy (mTE), convergent cross mapping (CCM). Validation on 93 Mooij et al. pairs + synthetic sets; graph edit distances 1–37.
- Didn't work, verbatim: mTE *"did not produce significant results"*; CCM starved by *"only 127 records"*; *"scarcity of proper multivariate methods… for causal discovery"*; *"methods diverge in their results pointing to different perspectives."*

**P18. Hardware-aware node grouping automation exists but is explicitly not production-safe.**
- Reporter: CSCS (CUG2024 [PAPER]). CSM API-driven inventory, hardware component patterns (`a100:12:epyc:1`), scoring + delta + fuzzy matching, memory normalized to 16 GiB units.
- Authors' own verdict: *"this algorithm may not be valid"* under Slurm because reassignment could be *"highly disruptive"*; *"we do not recommend following this algorithm in a production environment."*
- Quantitative: **none.**

**P19. Application identification is an unsolved observability gap.**
- Reporter: CSCS (YAULT, CUG2025 [BOF]). *"Can we identify the applications used by the users?"* under mandatory access control, chrooted containers, user-owned environments. Approach: eBPF syscall tracing + Slurm plugin. No numbers.

---

## 3. Reverse search: CUG operational problem → archival literature

All archival citations below were **verified via Crossref or usenix.org in this session**. Venue/year/DOI are as returned by the registry.

**R1. Bad-actor node screening policy under scarce idle capacity (from P6).**
Abstraction: sequential experimental design — choose which node-level tests to run, for how long, on scavenged backfill capacity, to maximize defect detection per node-hour, given detection rates as low as 1 per 14,618 tests.
Closest archival: reliability *characterization*, not policy —
- Ostrouchov, Maxwell, Ashraf, Engelmann, Shankar, Rogers. "GPU Lifetimes on Titan Supercomputer: Survival Analysis and Reliability." **SC20**, DOI 10.1109/sc41405.2020.00045.
- Nie, Xue, Gupta, Patel, Engelmann, Smirni, Tiwari. "Machine Learning Models for GPU Error Prediction in a Large Scale HPC System." **DSN 2018**, DOI 10.1109/dsn.2018.00022.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** on *screening-policy optimization / test-scheduling under backfill*. This is the single strongest SC-paper-shaped gap in the corpus, and ORNL has already published the ground truth to evaluate against.

**R2. Node quarantine decisions and false-positive cost (from P6/P7).**
Abstraction: sequential hypothesis testing / value-of-information for drain-vs-return decisions; the CUG evidence shows an entire screening method being retired for zero yield (39,437 screens, 0 failures) with no decision-theoretic framing.
Closest archival: failure prediction with lead time, which is the adjacent but different problem —
- Das, Mueller, Siegel, Vishnu. "Desh: deep learning for system health prediction of lead times to failure in HPC." **HPDC 2018**, DOI 10.1145/3208040.3208051.
- Das, Mueller, Rountree. "Aarohi: Making Real-Time Node Failure Prediction Feasible." **IPDPS 2020**, DOI 10.1109/ipdps47924.2020.00115.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** on quarantine decision policy / FP-FN cost asymmetry in HPC node management.

**R3. Fabric counter selection under acquisition cost (from P4).**
Abstraction: given >1,000 counters/port and 64K/switch at ~0.5 s per switch dump, choose a counter subset and cadence maximizing diagnostic information per unit polling cost.
Closest archival:
- De Sensi, Di Girolamo, McMahon, Roweth, Hoefler. "An In-Depth Analysis of the Slingshot Interconnect." **SC20**, DOI 10.1109/sc41405.2020.00039. (Characterizes Slingshot; does not treat telemetry cost.)
- Jha, Patke, Lim, Kalbarczyk, Kramer, Iyer, Brandt, Gentile, Showerman, Bauer, Kaplan. "Measuring Congestion in High-Performance Datacenter Interconnects." **NSDI '20**, https://www.usenix.org/conference/nsdi20/presentation/jha. (Monet; Blue Waters Gemini/Aries; congestion-region detection from network counters — the closest methodological ancestor.)
Verdict: partial. **NO CLOSE ARCHIVAL WORK FOUND** on counter-subset selection as an optimization problem for Slingshot-class fabrics.

**R4. Streaming summarization of interconnect telemetry with bounded memory (from P5).**
Abstraction: sketch/moment-based multi-resolution summaries over fabric telemetry with provable error bounds and query-latency SLOs.
Closest archival: none located in HPC venues. CADDY itself (CUG2024, vendor) is the most quantitative artifact and is *not* archival.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** in SC/HPDC/IPDPS/Cluster. The sketch machinery lives in the networking/DB communities; the HPC-fabric instantiation with operator-facing accuracy guarantees is open. Note the concrete hook: CADDY reports 1200x compression but concedes it *"may reduce granularity for certain anomaly detection workloads"* — nobody has measured that degradation.

**R5. Telemetry retention/downsampling policy vs downstream analytic utility (from P11/P14).**
Abstraction: choose retention and downsampling per metric class to minimize storage/query cost subject to preserving detectability of known fault signatures. Evidence: HPCM defaults of Kafka 1 day / OpenSearch 7 days / VictoriaMetrics 7 days, and EPCC's explicit complaint that Graphite downsampling destroyed long-term fine-grained analysis.
Closest archival: infrastructure papers that store data but do not optimize retention —
- Agelastos et al. "The Lightweight Distributed Metric Service: A Scalable Infrastructure for Continuous Monitoring of Large Scale Computing Systems and Applications." **SC14**, DOI 10.1109/sc.2014.18.
- Netti, Müller, Guillen, Ott, Tafani, Ozer, Schulz. "DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems." **HPDC 2020**, DOI 10.1145/3369583.3392674.
- Bautista, Romanus, Davis, Whitney, Kubaska. "Collecting, Monitoring, and Analyzing Facility and Systems Data at the National Energy Research Scientific Computing Center." **ICPP 2019 Workshops**, DOI 10.1145/3339186.3339213.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** treating retention/downsampling as a constrained optimization against analytic utility. Excellent SC candidate — cheap to evaluate on replayed traces, and the vendor has published the defaults to beat.

**R6. Control-plane telemetry service scalability and backpressure (from P2).**
Abstraction: end-to-end flow control and admission for a 10^5–10^6 msg/s monitoring plane that must not perturb boot or job launch.
Closest archival: LDMS SC14 (transport scaling) and Wintermute HPDC20 (in-band analytics) — both above.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** on backpressure/degradation-mode design for HPC monitoring control planes. The CUG2023 evidence (telemetry-api causing *Kafka rebalancing events*, boot failures from credential fetch) is a fully-formed problem statement waiting for a paper.

**R7. Telemetry schema evolution and semantic drift (from P1).**
Abstraction: versioned metric semantics, schema-registry federation, and reprocessing cost over multi-year operational archives.
Closest archival: none located. STREAM documents the pain (re-indexing, federated schema registries needing proxies, fields that *"change throughout the lifetime of the data"*), but as an experience report.
Verdict: **NO CLOSE ARCHIVAL WORK FOUND.** Strong gap; also directly relevant to a new center that will run one archive for 5–10 years.

**R8. Cross-source attribution and ground truth for job-level energy/telemetry (from P8/P15).**
Abstraction: reconciling scheduler accounting, node counters (10 Hz PM counters), and pipeline-sampled telemetry (~1 Hz) into a defensible per-job attribution, with timestamp-synchronization error explicitly modeled. Evidence: CSCS's 849 J discrepancy on one job and *"Slurm… cannot therefore always be trusted"*; Sandia's measured *"sample time variations of a few milliseconds"* across compute nodes.
Closest archival:
- Klinkenberg, Terboven, Lankes, Müller. "Data Mining-Based Analysis of HPC Center Operations." **CLUSTER 2017**, DOI 10.1109/cluster.2017.23.
- Ahlgren, Andersson, Brandt, Cardo, Chunduri, Enos, Fields, Gentile, Gerber, Gienger, Greenseid, Greiner, Hadri, He, Hoppe, Kaila, Kelly, Klein, Kristiansen, Leak, Mason, Pedretti, Piccinali, Repik, Rogers, Salminen, Showerman, Whitney, Williams. "Large-Scale System Monitoring Experiences and Recommendations." **CLUSTER 2018**, DOI 10.1109/cluster.2018.00069. — *This is the CUG monitoring community's own archival crossover paper; the single best precedent for turning CUG practice into a peer-reviewed contribution.*
Verdict: partial coverage; **the reconciliation/uncertainty-quantification framing is open.**

**R9. Online detection and localization of straggler storage targets (from P9).**
Abstraction: detect and localize per-OST performance degradation in a 298-OST all-flash Lustre from passive telemetry, without daily active probing.
Closest archival — **this is the one area with genuine archival coverage:**
- Lockwood, Snyder, Wang, Byna, Carns, Wright. "A Year in the Life of a Parallel File System." **SC18**, DOI 10.1109/sc.2018.00077.
- Jha, Cui, Banerjee, Xu, Enos, Showerman, Kalbarczyk, Iyer. "Live Forensics for HPC Systems: A Case Study on Distributed Storage Systems." **SC20**, DOI 10.1109/sc41405.2020.00069.
Verdict: **CLOSE ARCHIVAL WORK EXISTS.** Contribution here would be extension to all-flash/NVMe-specific failure physics (garbage collection, trim cadence, the *"surprising 75%"* fullness optimum) — narrower, still publishable, but not a green field.

**R10. Network digital twin validated against production telemetry across a 10^8 timescale gap (from P16).**
Abstraction: multi-resolution fusion of ns-scale switch behavior with 15 s telemetry; simulation acceleration to fit operational windows; validation methodology for NIC-level traffic.
Closest archival:
- Brewer, Maiterth, Kumar, Wojda, Bouknight, Hines, Shin, Greenwood, Grant, Williams, Wang. "A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale." **SC24**, DOI 10.1109/sc41406.2024.00029. (Facility/thermal twin — same ExaDigiT program, different subsystem.)
- De Sensi et al., **SC20** (above).
Verdict: **NO CLOSE ARCHIVAL WORK FOUND** for a *network* digital twin validated from production Slingshot telemetry. ORNL has flagged this themselves.

**Additional gaps worth listing (evidence present, archival anchor absent):**
- **Anomaly detection on CDU/cooling telemetry with operator-actionable alerting.** Methods exist archivally — Borghesi, Bartolini, Lombardi, Milano, Benini, "Anomaly Detection Using Autoencoders in High Performance Computing Systems," **AAAI 2019**, DOI 10.1609/aaai.v33i01.33019428; Tuncer, Ates, Zhang, Turk, Brandt, Leung, Egele, Coskun, "Diagnosing Performance Variations in HPC Applications Using Machine Learning," **ISC 2017**, DOI 10.1007/978-3-319-58667-0_19; Aksar, Zhang, Ates, Schwaller, Aaziz, Leung, Brandt, Egele, Coskun, "Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems," **ISC 2021**, DOI 10.1007/978-3-030-78713-4_11. **What is missing is evaluation on Cray EX liquid-cooling telemetry** — i.e. the gap is evidence, not method. HPE ships exactly this feature with zero published evaluation (P10).
- **Job-neighborhood interference on Slingshot dragonfly.** Ancestor: Bhatele, Mohror, Langer, Isaacs, "There goes the neighborhood: performance degradation due to nearby jobs," **SC 2013**, DOI 10.1145/2503210.2503247. No verified Slingshot-11-era equivalent found.

---

## 4. Telemetry data-path reconstruction with reported costs

Pipeline template: sensor → agent/exporter → collector → bus → storage → aggregation → features → model → alert → action.

| Site / system | Sensor & agent | Collector / bus | Storage | Analytics / model | Action | Reported costs & failure modes (verbatim numbers) |
|---|---|---|---|---|---|---|
| **ORNL, 5 HPE systems + Frontier/Orion (STREAM)** | HPCM (Redfish); Telegraf for Lustre; xalt job records | Kafka Connect → **Apache Kafka**, 6 brokers on OpenShift | **Elasticsearch** data lake | Grafana, Confluent Control Center, Prometheus | dashboards / ops | **300M msgs/day, 200+ topics, 1.3 TB/day**; 72 MB/s avg, 105 MB/s peak, 38 MB/s w/o Orion, 300 MB/s incl. replication+consumption, 7.5 GB/s theoretical; 223 topics (May 2023); top topic `orion.lustre.rpc` **111K msg/s, 43 MiB/s**; HPCM **~18 MB/s @ 105,000 msg/s**; Lustre **50 MB/s @ 128,000 msg/s**; 6× Dell R740, 128 GB RAM, 24×12 TB SSD; 24 TB + 64 GB + 16 threads per Kafka pod. Projection: **20 PB over 5 years ⇒ 140 MB/s steady state**. Failure modes: producer/consumer bottleneck, re-indexing after topic renames, federated schema-registry conflicts, **broker failure ⇒ "TBs of recovery traffic"** |
| **NERSC Perlmutter (CSM default path)** | LDMS samplers on compute | LDMS L1 aggregators → **Kafka** (topic `cray-node`) | **PostgreSQL** persisters | Grafana | dashboards | Default sampling **10 s**; **"100K to 1M messages per second"** at full scale — CSM `telemetry-api` **"could not handle"** it; persister scaled to **"16 copies"** for **5,000-node** systems; compute-node LDMS dataset **"a few kilobytes"**; clock skew **"a few milliseconds"** |
| **NERSC Perlmutter (site bypass) + OMNI** | LDMS samplers | NERSC aggregator pod, custom store plugin; rsyslog collectors/aggregators; Promtail | **VictoriaMetrics** (metrics), **Loki** (logs), Elasticsearch (legacy) → **OMNI** | Grafana; Alertmanager → ServiceNow | ticketing | Log pipeline scaled **"From 100k/s To 2 million/s"**; pre-fix **"< 100k messages/s"**, intermediate **200k/s**; **"2 CPU cores + 150MB Mem per pod x 64~128 pods"** |
| **LLNL El Capitan (TOSS 4)** | LDMS samplers; `slingshot_metrics`, `rdc_sampler` | L1 aggregators → cluster-local **Kafka** (**Avro**) → Kafka Connect ES sink; MirrorMaker → Sonar Kafka | central **Elasticsearch**; **Cassandra** (Sonar) | Grafana on OpenShift | ops | Planned majority sampling **5 s**; Slingshot counters trimmed to **"roughly forty"** from **"over a thousand counters per port and over 64K total port counters per switch"**; `dump_counters` **~0.5 s/switch**; Avro yields **"significantly fewer bytes transmitted"** than HPE's one-metric-per-message JSON |
| **CSCS Alps (EMOI)** | Beats agents; Cray PM at **10 Hz**; SMA | Logstash (×2) → **Kafka** (Strimzi) → KafkaStream → Memcached | **Elasticsearch** (ECK) | Kibana, Grafana; job energy analysis | ops / energy accounting | Telemetry pipeline **~1 Hz**; ~10,000 GH200 + ~1,000 pre-Alps nodes; 984 jobs analyzed; job energy **5,663,156 J vs Slurm 5,662,307 J**. **No GB/day, no cardinality, no retention published.** Failure modes: CSM Kafka has **no external listener**; multi-sensor message bundling **"not suitable for ingestion into ElasticSearch"**; **Fluent Bit unstable at high throughput** |
| **HPE HPCM 1.13 (product default)** | MMD (admin) / Sec (leaders) / SMD (compute); **PCIM** for CDU/VCDU/PDU; **subsmon** Redfish subscriptions on EX switches; **Slingshot Telemetry Agent** (HTTP streaming); Telegraf for WLM; FMN | **Kafka** + Zookeeper + Confluent Schema Registry (Avro) + Kafka REST | **VictoriaMetrics** (vminsert/vmstorage/vmselect); **OpenSearch** (Fluent Bit + Logstash); TimescaleDB (deprecated) | **AIOps** container: univariate + multivariate anomaly scores; Alertmanager | Grafana/OpenSearch dashboards, email/Slack/webhook | Retention defaults: **Kafka 1 day; OpenSearch 7 days; VictoriaMetrics 7 days; TimescaleDB 30 days**; ≤1.12: CrayEX telemetry 24 h, others 168 h; Timescale compression at 7 days **">90% disk space"** saved; monitoring interval e.g. **5 s**; Slingshot is **"the big hitter for disk space."** **No sizing model, no scaling limits, no expected volumes published** |
| **HPE Fabric AIOps / CADDY** | Slingshot telemetry API | ETL layer → Ray in-memory actors | hierarchical Bins (5 Welford moments/counter) + historical disk | Python FAIO API, REST | admin queries | Ingest **300K events/min**; 4,096 ports (8×8×64); 4 counters; compression **425x/600x/1200x** at 10/15/30-min bins; fetch **355 ms → 151 ms / 267.51 ms**; **+32.5% ingest overhead**; live horizon **10 min → days**; recommended window **≤3 h**; single-node eval only |
| **ORNL Frontier node screening** | per-node benchmarks (BabelStream, rocHPL, AMG, LAMMPS, oblex, rocPRIM) via Slurm **backfill** | Slurm | results DB | rule-based pass/fail | drain / repair ticket | **~6M single-node tests** cumulative; 1.9M in 6 months; **99 unique failing nodes**; LAMMPS **1 failure / 14,618 tests**; runtimes 24 min (backfill) vs <1 min (checknode); weekly screen **39,437 screens, 0 failures → retired** |
| **ORNL Frontier health/state** | `checknode` bash (boot + epilog); SEC over controller/console/syslog | Slurm state | Slurm reason field | rules | drain + auto-resume | **No numbers published.** MTBF context only: **"hours, not days"** |
| **EPCC ARCHER2** | Checkmk TCP agents; **rectifier power every 5 s** from cabinet controllers; `sinfo`; SSH probes; Lustre/HSN checks | Checkmk servers per group → Carbon | **Graphite** | Grafana | email + HPE pager | 5,860 nodes / 750,080 cores; HPL **16.8 PF → 19.5 PF** after isolating power-cycling nodes. Failure mode: **Graphite granularity decays over time**, blocking long-term fine-grained analysis |
| **NERSC Slingshot fabric poller** | Fabric Manager REST API (health, switch, port) | K8s CronJob (Python, OCI) | **VictoriaMetrics** + **Loki** | 11 metrics, threshold | alerts | Detects switch-offline, port flapping, health degradation, API loss. **Interval, switch/port counts, volume: not reported.** Difficulties: non-numeric health states, long-term port history, Kafka integration |
| **Indiana U GPU accounting** | **pynvml** (DCGM rejected: *"too intrusive of a footprint"*), epilog-time | Slurm | **MariaDB** `AdminComment` (JSON), 4,000-record ring buffers | offline stats | reporting | 295,470 jobs; **mean GPU util 11%**; **53% of jobs never used the GPU**; 26% excluding non-users; 645 apps, 53% AI/ML. Failure mode: **65,535-char `AdminComment` truncation** for long multi-GPU jobs; nvml util = *active time*, not core utilization |
| **HPE Cray EX PM counters (node-level source)** | `bpmcdmod` kernel module → `/sys/cray/pm_counters/` | shared memory, cached | consumed by Slurm / `cray_pm` | — | per-job energy | **10 Hz** update (`raw_scan_hz`); J / W / °C, µs timestamps (v3+); EX254n **34 counter files** (4× GH200), EX255a **20 counter files** (4× MI300a) with **"Precision input power monitoring and reporting ≤ 2%"**. Limit: restricted access to **"socket-level and component-level power, energy, and thermal data at or above 10Hz"** for partner components |
| **NERSC all-flash Lustre** | obdfilter-survey (daily, off-hours); IOR | — | — | CoV vs **≤8%** target | tuning, OST repair | 36 PB, >7 TB/s peak, 16 MDS, 274→298 OSTs, 3,480 NVMe; probe writes/reads **~250 TB on 32 GPU nodes**; slow OSTs **25–50% below expected**; fix **15.1 → 19.9 GB/s (+30%)**, min **260 MB/s → 9,032 MB/s**; SafeRet **−14%**; checksums **−17%** (673320 ± 31779 → 554012 ± 37846 MB/s); optimal fullness **~75%**; purge horizon **~365 days** |
| **ORNL Network Digital Twin** | MPI tracing (fi_hook, PMPI), SST DUMPI traces; power/cooling telemetry at **15 s** | — | — | SST Macro dragonfly DES; FTQ histograms at **1 ms**; spyplots | design/fault-tolerance study | 9,408 nodes, 80 groups, 4 NICs/node, switch latency **100–350 ns**; full-Frontier single-rank replay **>30 h** vs 2 h limit; SST-Core **~7x** insufficient; **~1.8M Frontier jobs**; **~6 months of telemetry replayed**; **no accuracy numbers**; NIC spyplot validation unsolved |

**Cost/failure-mode categories the CUG corpus actually quantifies:** data volume (STREAM, CADDY), throughput ceilings (OMNI, telemetry-api), compression (CADDY 1200x; Timescale >90%), query latency (CADDY), ingest overhead (CADDY +32.5%), retention defaults (HPCM), polling cost (dump_counters 0.5 s), timestamp sync (few ms), agent overhead (DCGM rejected qualitatively), schema evolution (STREAM), downsampling loss (ARCHER2/Graphite).
**Categories nobody quantifies:** metric cardinality (no site reports series counts), sampling-overhead measurement methodology (the *"no statistically significant performance penalty"* claim has no supporting numbers), query cost at scale, per-metric value-of-information, monitoring TCO.

---

## 5. Vendor claims audit

Columns: documented feature | documented algorithm | quantitative evaluation | peer-reviewed validation | production deployment evidence.

| Claim | Feature | Algorithm | Quant. eval | Peer review | Production evidence |
|---|---|---|---|---|---|
| **HPE HPCM "AIOps" anomaly detection** (CUG2025 tut106; CUG2022 BoF) | YES — *"real-time and offline anomaly detection, prediction for time-series monitoring data"*, uni/multivariate, containerized, threshold on anomaly score, Grafana panels, `cm monitoring grafana dashboard enable` | **NO** — *"machine learning and deep learning technologies"*, nothing named | **NO** | **NO** | Illustrative screenshots only (CDU valve position, cooling pressure, CPU/GPU temp). No site, scale, or FP rate |
| **HPE "AIOps: Leveraging AI/ML for Anomaly Detection in System Management"** (CUG2021, [PAPER][VENDOR], NREL deployment claimed in program blurb) | YES | **UNKNOWN — PDF NOT POSTED** | UNKNOWN | NO (CUG paper track) | Program text cites NREL; the related NREL report is **NREL/TP-2C00-79712 (2021)**, an institutional technical report, whose abstract states only *"training models to operate on real-time data collected from both IT and facilities sources"* — **no algorithms, no datasets, no metrics**. https://research-hub.nrel.gov/en/publications/artificial-intelligence-for-data-center-operations-aiops/ |
| **HPE Fabric AIOps / CADDY** (CUG2024) | YES | **YES** — Welford online moments, hierarchical metadata-indexed bins, Ray | **YES — the only vendor artifact with real numbers** (compression, latency, overhead; see §4) | NO | Testbed only: *"Single node… telemetry modeled after HPE Hotlum (1024-node)"* — **not a production deployment** |
| **HPE trellis** (CUG2021) | YES | Visualization/aggregation only; ML explicitly future work (*"we plan to investigate advanced machine learning models"*) | **NO** — *"no quantitative performance benchmarks, accuracy metrics, or comparative evaluations"* | NO | 1024-node internal system (640 nodes used), 1 Hz, 4 h collection |
| **HPE Powersched** (CUG2023) | YES | **YES** — mean-shift clustering, 37 PMU events in 4 blocks, silhouette 0.85 vs DBSCAN 0.62 | **YES but tiny** — 14.382% avg energy saving, 1.65% avg runtime extension, range 8.18–18.46% / 0.28–3.09% | NO | **2 nodes**, DL385 Gen10, Infiniband; authors state *"the results come from an early prototype"* |
| **HPE Hardware Triage Tool** (CUG2024) | YES | Rule-based YAML decision trees; **explicitly no ML** | **NO** — zero defect rates, accuracy, or triage-time data | NO | Frontier context cited (9,400+ nodes, 150,000+ components); no outcome data. Authors: *"not a substitute for the discipline of system health checks"* |
| **HPE Cray EX PM Counters** (CUG2024) | YES — well documented | N/A (measurement, not inference) | Partial — 10 Hz, ≤2% accuracy on EX255a | NO | Product feature, broadly deployed |
| **HPE Swordfish/Redfish + ClusterStor** (CUG2024) | Claimed in program | **CONTENT NOT RETRIEVABLE** — file1 404, file2 effectively empty | UNKNOWN | NO | UNKNOWN |
| **NVIDIA Mission Control** (docs.nvidia.com/mission-control) | YES — *"Autonomous Recovery Engine"*, autonomous job + hardware recovery, runbooks, NVIDIA Resiliency Extension (NVRx), BCM, Run:ai, **NetQ** *"unified observability across NVLink and Ethernet"*, Grafana | **NO** | **NO** | **NO** | Docs are installation/licensing oriented. Note: the marketing pages I tried (`/data-center/gb200-nvl72/mission-control/`, `/data-center/products/mission-control/`) both **404** — my audit rests on the docs site only |
| **DDN Insight** (ddn.com/products/insight/) | Marketing-level only: *"Disruption Prevention"*, *"Proactive Issue Anticipation"*, *"Insight-Driven Productivity"*, *"Decision-Making Optimization"*, *"continuous real-time monitoring"* | **NO** | **NO** | **NO** | **NO named deployment.** Page makes **no explicit AI/anomaly-detection/predictive-analytics claim** despite the category positioning |
| **Intel, VAST, others** | **NOT COVERED** — WebSearch budget exhausted | — | — | — | Open task |

**Bottom line for Part B:** of eleven vendor items examined, **one** (CADDY) carries a documented algorithm *and* a quantitative evaluation, and even that is a single-node testbed. **Zero** carry peer-reviewed validation. **Zero** carry a production evaluation with operator-relevant outcome metrics (precision, recall, alert volume, MTTR delta). The recurring pattern is: feature documented → algorithm withheld → evaluation absent → deployment implied by proximity to a famous system name. Do not cite any of it as research evidence. The one honest exception worth citing *as engineering* is CADDY's compression/latency table.

---

## 6. What CUG evidence can and cannot support

**CAN support:**
1. **Existence and prevalence of operational problems.** When ORNL retires a screening method after 39,437 zero-yield runs, or NERSC finds OSTs 25–50% slow, or LLNL/Sandia report the vendor telemetry API failing at 100K–1M msg/s, that is credible primary evidence of a real production problem. Use it to *motivate* research questions.
2. **Ground-truth architecture and configuration facts.** Component names, data flows, retention defaults, sampling rates, API behaviors. The CUG2025 HPE tutorial is effectively the public specification of the HPCM 1.13 monitoring stack.
3. **Order-of-magnitude scale parameters** for system design: 1.3 TB/day at ORNL, 2M log msg/s at NERSC, 300M messages/day, 64K counters per switch, 10 Hz PM counters vs 15 s telemetry.
4. **Negative results that nobody else publishes.** "Fluent Bit was unstable at high throughput," "Graphite downsampling destroyed our long-term analysis," "we do not recommend this algorithm in production," "mTE did not produce significant results." These are unusually valuable and almost never appear in archival venues.
5. **Deployment reality checks** on archival proposals — e.g. Indiana rejecting DCGM on overhead grounds is direct evidence against a common assumption in ML-for-HPC papers.

**CANNOT support:**
1. **Any claim of method efficacy.** CUG papers almost never report precision/recall, baselines, ablations, or statistical tests. The Frontier screening paper is the corpus's high-water mark and still reports raw counts, not a designed comparison.
2. **Reproducibility.** Datasets are essentially never released; most CUG telemetry work is unreproducible by construction.
3. **Peer-reviewed standing.** The CFP language is explicit: acceptance is abstract-based, ICPS publication *"may require an additional round of reviews."* A CUG "Paper" label is not equivalent to SC/HPDC/IPDPS acceptance. Whether any given CUG 2024/2025 paper reached ACM ICPS is **UNVERIFIED here**.
4. **Vendor performance claims.** See §5.
5. **Generalization across sites.** The CUG2023 monitoring paper says this outright: format divergence means *"there can't easily be a rule of thumb in one implementation that extends to the other."*
6. **Completeness.** Several of the most-cited artifacts are not posted at all (CUG2021 HPE AIOps paper; CUG2021 Sandia system/application monitoring paper; CUG2022 Fallout; CUG2023 Slingshot Dashboard tutorial; CUG2024 Swordfish paper). Absence from the public record is common, so never infer "not studied" from "not found on cug.org."

**Practical rule for your writing:** cite CUG as *practice evidence* — "operators at ORNL report X" — and reserve claims of *validated method* for the Crossref-verified archival papers in §3. Where the two disagree, the disagreement is itself the paper.

---

## 7. Where the SC-Technical-Paper-shaped questions actually are

Ranked by (gap strength × availability of public ground truth × relevance to a new large system):

1. **Screening-policy optimization for silent hardware defects.** Formalize backfill node-screening as sequential design; objective = defects found per node-hour under a detection rate of ~1/14,618. ORNL published the outcome data to validate against, and published a *negative* result (the retired weekly screen) as a baseline. No close archival work.
2. **Retention/downsampling as constrained optimization against detectability.** Beat HPCM's 1-day/7-day/7-day defaults; use EPCC's Graphite regret and CADDY's 1200x compression as the two endpoints. Evaluable purely on replayed traces. No close archival work.
3. **Counter-subset selection under acquisition cost for Slingshot-class fabrics.** 64K counters/switch, 0.5 s/dump, sites arbitrarily choosing "roughly forty." Information-per-poll-second is a clean objective. Partial ancestry in Monet (NSDI'20).
4. **Backpressure and graceful degradation for the monitoring control plane.** The failure is documented (telemetry-api → Kafka rebalancing → boot failures); the design principle is not. No close archival work.
5. **Telemetry schema evolution over multi-year archives.** Versioned metric semantics + reprocessing cost. Directly actionable for a system you are about to specify. No close archival work.
6. **Network digital twin validation from production telemetry across the ns↔15 s gap.** ORNL flagged it; ExaDigiT gives you the facility-side precedent (SC24) and the collaboration surface.
7. **Cross-source attribution with explicit uncertainty** (10 Hz PM counters vs ~1 Hz pipeline vs Slurm accounting; ms-scale clock skew). CSCS handed you a discrepancy and a trust statement.
8. **Anomaly detection on liquid-cooling/CDU telemetry, evaluated properly.** Methods are archivally mature (AAAI'19, ISC'17, ISC'21); the vendor ships the feature with no evaluation. A rigorous evaluation on Cray EX cooling telemetry is a defensible contribution *because* the vendor refuses to publish one.

**Immediate follow-ups I could not complete:** CUG 2026 program (blocked/not posted — recheck early 2027); Intel and VAST vendor audit; whether CUG 2024/2025 papers appear in ACM ICPS; the five unposted CUG PDFs listed above (worth emailing the authors — ORNL, Sandia and NERSC authors typically share on request).

**Sources:**
- [CUG Proceedings index](https://cug.org/proceedings/)
- [CUG 2020 program](https://cug.org/proceedings/cug2020_proceedings/at_a_glance.html)
- [CUG 2021 program](https://cug.org/proceedings/cug2021_proceedings/at_a_glance.html) · [trellis](https://cug.org/proceedings/cug2021_proceedings/includes/files/pap115s2-file1.pdf)
- [CUG 2022 program](https://cug.org/proceedings/cug2022_proceedings/at_a_glance.html) · [ARCHER2 monitoring](https://cug.org/proceedings/cug2022_proceedings/includes/files/pap103s2-file1.pdf) · [Slingshot FM Monitor](https://cug.org/proceedings/cug2022_proceedings/includes/files/pres116s2.pdf) · [Loki](https://cug.org/proceedings/cug2022_proceedings/includes/files/pres122s1.pdf) · [HPCM BoF](https://cug.org/proceedings/cug2022_proceedings/includes/files/bof104s1-file1.pdf) · [Perlmutter network](https://cug.org/proceedings/cug2022_proceedings/includes/files/pap117s2-file1.pdf)
- [CUG 2023 program](https://cug.org/proceedings/cug2023_proceedings/at_a_glance.html) · [STREAM](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap155s2-file1.pdf) · [Extreme-Scale Monitoring](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap149s2-file1.pdf) · [Frontier node health](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap151s2-file1.pdf) · [GPU usage](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap139s2-file1.pdf) · [Powersched](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap113s2-file1.pdf) · [OMNI deck](https://cug.org/proceedings/cug2023_proceedings/includes/files/tut107s2-file1.pdf)
- [CUG 2024 program](https://cug.org/proceedings/cug2024_proceedings/at_a_glance.html) · [EMOI](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap113s2-file1.pdf) · [CADDY](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap112s2-file1.pdf) · [Frontier defective hardware](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap123s2-file1.pdf) · [Hardware triage](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap121s2-file1.pdf) · [Network digital twin](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap140s2-file1.pdf) · [All-flash FS](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap141s2-file1.pdf) · [PM counters](https://cug.org/proceedings/cug2024_proceedings/includes/files/pres127s2.pdf) · [CSM stack overview](https://cug.org/proceedings/cug2024_proceedings/includes/files/pres125s2.pdf) · [Node selection](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap106s2-file1.pdf)
- [CUG 2025 program](https://cug.org/proceedings/cug2025_proceedings/at_a_glance.html) · [Monitoring HPE Cray HPC systems tutorial](https://cug.org/proceedings/cug2025_proceedings/includes/files/tut106s2-file1.pdf) · [Causality inference](https://cug.org/proceedings/cug2025_proceedings/includes/files/pap118s2-file1.pdf) · [Modular Data Centre](https://cug.org/proceedings/cug2025_proceedings/includes/files/pap133s2-file1.pdf) · [ML workloads on Cray EX](https://cug.org/proceedings/cug2025_proceedings/includes/files/pap159s2-file1.pdf) · [Monitoring WG BoF deck](https://cug.org/proceedings/cug2025_proceedings/includes/files/bof102s1-file1.pdf)
- [CUG 2026 Call for Papers](https://cug.org/cug-2026-call-for-papers/) · [CUG 2026 Technical Program](https://cug.org/cug-2026-technical-program/)
- [Monet, NSDI '20](https://www.usenix.org/conference/nsdi20/presentation/jha) · [NREL AIOps report](https://research-hub.nrel.gov/en/publications/artificial-intelligence-for-data-center-operations-aiops/) · [NVIDIA Mission Control docs](https://docs.nvidia.com/mission-control/index.html) · [DDN Insight](https://www.ddn.com/products/insight/)agentId: a001e9fa5b1c86095 (use SendMessage with to: 'a001e9fa5b1c86095', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 192186
tool_uses: 126
duration_ms: 2012943</usage>
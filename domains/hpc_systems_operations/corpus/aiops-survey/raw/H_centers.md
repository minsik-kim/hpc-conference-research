I hit the session's web-search cap partway through (200/200), so the last few centers were covered by direct page fetches only. Everything below is from sources I actually opened; gaps are marked explicitly.

---

# HPC OPERATIONAL ANALYTICS / AIOps — PUBLIC PRODUCTION EVIDENCE
### Structured research notes, evidence-graded. Compiled 2026-09-06.

**Grading vocabulary used throughout**
- **DEPLOYED** = the center states it runs in production
- **PROTOTYPE** = published as an experiment/pilot on real data, not stated as production
- **ROADMAP** = aspirational language ("we plan to", "there is potential")
- **L-levels**: L0 raw collection · L1 dashboards · L2 threshold alerts · L3 statistical/anomaly detection · L4 prediction · L5 RCA · L6 recommendation · L7 closed-loop remediation

---

## 1. OLCF / OAK RIDGE (ORNL) — *strongest overall evidence base*

### 1.1 Systems 2020–2026
| System | Vendor | Scale | Accel | Fabric | Storage |
|---|---|---|---|---|---|
| Summit (2018–2024) | IBM | 4,608 nodes, ~200 PF | 27,648 NVIDIA V100 (9,252 POWER9 CPUs) | Mellanox EDR IB | Alpine (GPFS) |
| Frontier (2022– ) | HPE Cray EX | 9,408 nodes, ~1.1 EF | 37,632 AMD MI250X | HPE Slingshot-11 | Orion Lustre, "650+ PB" |

Node/GPU counts verified in Hagerty et al. CUG2024 (9,408 / 37,632) and Shin et al. Constellation dataset page (9,252 P9 / 27,756 V100 for Summit; the GPU-error dataset says 27,648 Tesla V100 — the two ORNL pages differ, quoted as-is).

### 1.2 Telemetry stack actually deployed — reconstructed data path

```
[sensors]                    [agent/exporter]        [bus]          [storage]                 [aggregation]        [consumers]
BMC/OpenBMC power+thermal  ─┐
Cray CSM telemetry-api     ─┤
Slingshot counters         ─┼─> per-source producers ─> APACHE KAFKA ─> ElasticSearch (LAKE)  ─> Spark Structured  ─> Grafana dashboards
Lustre/Orion RPC stats     ─┤   (Telegraf for Lustre)   "STREAM"        Apache Druid            Streaming            RATS-Report
syslog / RAS events        ─┤    HPCM agents            central bus     Parquet on MinIO        Bronze→Silver→Gold   Live Visual Analytics (LVA)
Slurm/resource-manager     ─┤    xalt (job records)     223 topics      (OCEAN / GLACIER)       medallion tiers      Copacetic (security)
Facility (cooling, power)  ─┘                           Schema Registry                          MLflow + DVC + Jupyter
```
Orchestration: RedHat OpenShift / **SLATE** Kubernetes. Schema federation via OLCF-built **Stream Schema Relay** (Flask).

### 1.3 Concrete operational numbers — QUOTED

**STREAM Kafka bus** — Adamson, Osborne, Lester, Palumbo, *STREAM: A Scalable Federated HPC Telemetry Platform*, OSTI 1995656 (https://www.osti.gov/servlets/purl/1995656):
- "300 million messages to over 200 topics producing around **1.3 Terabytes per day**"
- 223 topics configured (220+ as of May 2023)
- Average write rate **72 MB/s**; peak **105 MB/s**; sustained without Orion 38 MB/s; **300 MB/s** total including replication/consumption
- Top producer (Orion Lustre RPC): **111K avg / 246K max messages/sec**, 43 MiB avg / 85.9 MiB max per second
- HPCM: ~18 MB/s at 105,000 msg/s; Lustre storage ~50 MB/s at 128,000 msg/s
- Hardware: 6× Dell PowerEdge R740, 128 GB RAM, 24×12 TB SSD, 2× Xeon Gold 32-core, 10 GbE each; six Kafka pods (16 threads / 64 GB / 24 TB each)
- Storage goal: "**20 PB over 5-year period**"; required steady-state bandwidth 140 MB/s; theoretical max 7.5 GB/s

**Whole-facility ODA** — Shin, Osborne, Karimi, Palumbo, May, Lester, Hines, Sattar, Huk, Simmerman, Brewer, Miller, Adamson, Kuchar, Prout, Wang, Atchley, Oral, *Navigating Exascale Operational Data Analytics: From Inundation to Insight*, SC24 Workshops, DOI 10.1109/SCW63240.2024.00226 (PDF: https://conferences.computer.org/sc-wpub/pdfs/SC-W2024-6oZmigAQfgJ1GhPL0yE3pS/555400b795/555400b795.pdf):
- **4.2–4.5 TB/day** total across the HPC data center
- Stream breakdown: **storage system ~3.3 TB/day**; compute power & temp **~537 GB/day**; interconnect **~32 GB/day**; syslog & events **~8.64 GB/day**; compute storage client ~2 GB/day; CRM ~350 MB/day; resource manager **~11 MB/day**; facility **~2.5 MB/day**
- Retention tiers: **STREAM (hot) 3–14 days · LAKE (warm) 1–2 weeks · OCEAN (cold) 1–5 years · GLACIER ∞**
- Frontier power profiling: **0.5 TB/day**, live-visualization capable
- Aggregation at e.g. 15-second intervals in the medallion refinement

> **Note for architecture design:** the resource-manager stream is ~11 MB/day against a 3.3 TB/day storage stream — a 300,000× dynamic range across streams inside one facility. That asymmetry is the single most reusable design fact in this entire note.

### 1.4 Intelligence level in production
**Verified L0–L2 broadly; L3 in specific pipelines; L5 human-in-the-loop; no L7.**

- **L0/L1 DEPLOYED**: STREAM, LAKE, Grafana, LVA ("years of power/thermal data, real-time low-latency queries"), RATS-Report (decade+ utilization history, allocation burn-rate), User Assistance dashboards.
- **L2 DEPLOYED**: Copacetic — "real-time security event detection and alerting"; Nagios alerting listed in STREAM.
- **L3 DEPLOYED (statistical, non-ML)**: Hagerty, Warner, Webb, *Multi-stage Approach for Identifying Defective Hardware in Frontier*, CUG2024 (https://cug.org/proceedings/cug2024_proceedings/includes/files/pap123s2-file1.pdf). **Explicitly not ML** — "deterministic methods", performance thresholds + bisection. Numbers:
  - **1.9 million backfill node tests** Oct 2023 – Apr 2024
  - **99 unique failing nodes** identified; **12** GPU HBM uncorrectable errors; **54** software bugs; **19** defective-hardware cases from the LAMMPS campaign
  - 244 LAMMPS jobs (40–240 min), 290 HACC jobs across 5 phases (2,500–9,072 nodes, 75–90 min avg)
  - **27** transient performance failures (failed threshold once, passed later) — i.e. a stated false-positive population
  - Production status: Slurm-backfill screen "continues to run behind production workloads"; the **epilog variant "was removed from production in December 2023"** as "too disruptive to user workloads"
  - Test suite grew "from 7 initial tests to 11 tests" in 18 months
- **L3/L4 DEPLOYED (ML, narrow)**: "Job power classification pipeline (neural network clustering of power profiles)" listed under production in the SC-W'24 paper.
- **PROTOTYPE**: ExaDigiT digital twin (V&V ongoing); "Machine learning models for predictive/prescriptive analytics"; "advanced anomaly detection beyond current SIEM tools".
- **L7: NOT FOUND.** No closed-loop remediation claimed.

### 1.5 Publications (verified)
- [WORKSHOP-PEER-REVIEWED] Shin et al., *Navigating Exascale Operational Data Analytics: From Inundation to Insight*, SC24 Workshops, DOI 10.1109/SCW63240.2024.00226. **The single best "what a center actually runs" paper in this whole survey.**
- [STATE-OF-PRACTICE / CUG] Hagerty, Warner, Webb, *Multi-stage Approach for Identifying Defective Hardware in Frontier*, CUG2024, pap123.
- [TECH-REPORT / CONFERENCE] Adamson, Osborne, Lester, Palumbo, *STREAM: A Scalable Federated HPC Telemetry Platform*, OSTI 1995656.
- [WORKSHOP-PEER-REVIEWED] Osborne, Palumbo, Huk, Adamson, Jones, Lester, *Advancing ODA Standardization Through an Open Source Dashboard*, HPCSYSPROS @ SC24, DOI 10.5281/zenodo.15724831, CC-BY-4.0. Core claim quoted: *"If the telemetry data schema changes, dashboards must be recreated using different sources, query languages, and metric names."*
- [CONFERENCE-PEER-REVIEWED, non-SC] Shin, Oles, Schmedding, Ostrouchov, Smirni, Wang, *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*, ICS'24, DOI 10.1145/3650200.3656615.
- [STATE-OF-PRACTICE / CUG] Holmen et al., *Towards the Development of an Exascale Network Digital Twin*, CUG2024.
- [STATE-OF-PRACTICE / CUG] Hong Enriquez, Prakash, Taheri, Dhakal (HPE), Maiterth, Brewer (ORNL), Milojicic, *Causality inference for Digital Twins in GPU Data Centers and Smart Grids*, CUG2025.
- [PRACTITIONER] *OLCF Supercharges Supercomputer Analytics with Apache Kafka*, olcf.ornl.gov news, 2019-12-16.
- [TECH-REPORT] 2024 OLCF Operational Assessment Report (https://www.olcf.ornl.gov/wp-content/uploads/2024-OLCF-Operational-Assessment-Report.pdf) — not mined in detail here.

### 1.6 Public datasets released — **highest-value center**
Portal: **Constellation**, https://doi.ccs.ornl.gov (Globus delivery; site Terms & Conditions govern; re3data r3d100013634).
1. **Long Term Per-Component Power and Thermal Measurements of the OLCF Summit System** — Shin, Ellis, Karimi, Oles, Dash. DOI **10.13139/OLCF/1861393**. Five months across 3 years (Jan+Aug 2020, Feb+Aug 2021, Jan 2022). Collected at **1 Hz**, released aggregated to **10 s and 1 min means**. Covers 9,252 POWER9 + 27,756 V100. Companion code: https://github.com/at-aaims/summit_power_and_thermal_data. Related paper DOI 10.1145/3458817.3476188.
2. **OLCF Summit Supercomputer GPU Snapshots During Double-Bit Errors and Normal Operations** — Shin, Oles, Schmedding, Ostrouchov, Smirni, Wang. DOI **10.13139/OLCF/1970187**, released 2023-04-20. Telemetry from 27,648 V100s: **NVIDIA XID failure records + node reboot logs + job scheduler records + 1 Hz BMC metrics**. Companion: ICS'24 paper.
3. **OLCF Frontier 2023-04-29 HPL Power Data (Top500/Green500 submission)** — OSTI 1975494.

Also referenced in SC-W'24 as released via Constellation: Summit power/energy, GPU failures, I/O/Darshan, HPL data.

### 1.7 Stated pain points — DIRECT QUOTES
- *"The primary bottleneck in HPC operational intelligence lies within the initial stage of large-scale stream exploration."*
- *"ML development iterations [are] starved with unknown future data, low-yield features, rare events, and missing data."*
- *"Securing vendor cooperation for unplanned sensor implementation can be difficult."*
- *"Despite abundant data acquisition, there is a notable gap in the end-to-end understanding of how the data is used, resulting in the accumulation of unused data and uncoordinated efforts."*
- *"Even with experts in each domain, HPC operations and ML, basic cross-domain training was required for necessary communications."*
- *"Challenge of achieving immediate data availability in the face of the relatively short lifespan of supercomputers."*
- STREAM: *"STREAM's biggest pain point has been producers and consumers, not the Kafka bus itself."*
- STREAM: *"Sensors, metrics, and telemetry data has not been standardized into a universal format."*
- Frontier hardware triage: *"Discovering trends in failures is one of the most important yet most difficult tasks"*; distinguishing *"bad hardware vs bad code"*.

---

## 2. NERSC / LBNL

### 2.1 Systems
- **Cori** (Cray XC40, KNL+Haswell, retired 2023)
- **Perlmutter** (HPE Cray EX; AMD Milan CPU nodes + NVIDIA A100 GPU nodes; **HPE Slingshot-11**; all-flash Lustre scratch — CUG2024 plenary "Nine Months in the life of an all-flash file system", Gerhardt, Simms, Fox, Basheer, Lozinskiy, Moore (HPE), Bhimji)
- HPSS archive; Community File System (IBM ESS)

### 2.2 Telemetry stack — DEPLOYED
**OMNI** = Operations Monitoring and Notification Infrastructure. Deliberately independent infrastructure: *"first online and last offline"*, all data NTP-synced.

```
External: substations, water, weather ─┐
Facility: BMS (BACnet, Modbus), PDU,  ─┤
          UPS, temperature sensors     │
HPC: Cray Power Management DB, Slurm, ─┼─> RabbitMQ / Prometheus scrape / Kafka
     Lustre, Aries (now Slingshot)     │       │
Network: sFlow, SNMP, InfiniBand,ESnet ┤       ├─> Elasticsearch (OMNI warehouse)
syslog                                ─┘       └─> VictoriaMetrics ─> Promxy ─> Alertmanager
                                                                                    │
                                                              Grafana <─────────────┤
                                                              ServiceNow MID server ┘
                                                                    └─> incident + automated remediation workflows
```
Perlmutter adds **LDMS** alongside HPE **CSM** telemetry (CUG2023). HPSS monitoring migrated **Nagios → VictoriaMetrics + Loki + Alertmanager** (HUF 2024, Basil Lalli, NERSC-LBNL, https://indico.kit.edu/event/742/contributions/17318).

### 2.3 Concrete numbers — QUOTED
Romanus (Rutgers/LBNL), Bautista, Davis, Whitney (LBNL), *Collecting, Monitoring, and Analyzing Facility and Systems Data at NERSC*, ICPP 2019 Workshops, DOI 10.1145/3339186.3339213 (abstract page: https://datacenters.lbl.gov/resources/collecting-monitoring-and-analyzing; poster: https://www.hpcs.cs.tsukuba.ac.jp/icpp2019/data/posters/Poster18-abst.pdf):
- **"over 522 billion records totaling 125TB"**; *"over two years of online operational data (550 billion records)"*
- **"average of 25,000 data points per second"**
- Facility PUE monthly average **1.07** (Level 2)
- Outcomes claimed: reduced downtime during facility transition; **"$2.5 million electrical substation savings"** for Perlmutter

Sukhija (Slippery Rock Univ.), Bautista, James, Gens, Deng, Lam, Quan, Lalli (NERSC), *Event Management and Monitoring Framework for HPC Environments using ServiceNow and Prometheus*, MEDES '20, DOI 10.1145/3415958.3433046 (OA: https://escholarship.org/content/qt7ch6t25w/qt7ch6t25w.pdf):
- **"over 25,000 messages per second from heterogeneous and distributed sources"**
- **"more than 20,000 sensors with hundreds of sources"**
- 14 Elastic Storage Servers in 7 HA pairs (NERSC Community File System)

Barry (HPE), Brandt, Gentile (SNL), Morrone (LLNL), **Roman (LBNL)**, Scott, Shoga (LLNL), Tucker (OGC), *Evaluating and Influencing Extreme-Scale Monitoring Implementations*, CUG2023, LLNL-CONF-847852 (https://cug.org/proceedings/cug2023_proceedings/includes/files/pap149s2-file1.pdf):
- CSM default sampling **"10 seconds by default"**; some collection **"order of 1 second"**
- Kafka **"100K to 1M messages per second"**
- Slingshot counter retrieval **"about half a second"**
- PostgreSQL persisters: a 5,000-node system **"may require as many as 16 copies"**
- Sample-time skew: **"a few milliseconds are seen across compute nodes"**

### 2.4 Intelligence level
**L0–L2 DEPLOYED, plus genuine partial L7 in a narrow domain — the strongest closed-loop evidence in this survey.**
From MEDES'20, three DEPLOYED automated workflows:
1. IBM Elastic Storage monitoring — auto-opens ServiceNow incidents at high/medium/low priority, auto-collects diagnostics
2. Compute node remediation — *"gather logs and troubleshooting information… categorize the node failure… proceed to predetermined scenarios"*
3. Repetitive alert handling — disk space, load, service health, with automated resolution

Assessment: **L2 fully, L5-assist (automated triage + evidence collection), L7 partial and rule-based** for pre-categorized failure classes. Authors are explicit that manual intervention remains for *"vendor cases"* and out-of-category incidents. **No production ML/anomaly detection found.**

### 2.5 Publications
- [WORKSHOP-PEER-REVIEWED] Romanus et al., ICPP'19 Workshops, DOI 10.1145/3339186.3339213
- [CONFERENCE-PEER-REVIEWED] Sukhija, Bautista et al., MEDES'20, DOI 10.1145/3415958.3433046
- [CONFERENCE-PEER-REVIEWED] Sukhija et al., *Towards Anomaly Detection for Monitoring Power Consumption in HPC Facilities*, MEDES'22, DOI 10.1145/3508397.3564826 — **PROTOTYPE, not stated as production**
- [WORKSHOP-PEER-REVIEWED] Sukhija et al., *Towards a Data Provenance Collection and Visualization Framework for Monitoring and Analyzing HPC Environments*, Springer, DOI 10.1007/978-3-031-51643-6_5
- [WORKSHOP-PEER-REVIEWED] *Power Analysis of NERSC Production Workloads*, SC-W'23, DOI 10.1145/3624062.3624200 (ACM blocked fetch — title/venue verified only)
- [WORKSHOP-PEER-REVIEWED] *NPAT — A Power Analysis Tool at NERSC*, SC-W'23, DOI 10.1145/3624062.3624149 (ACM blocked fetch)
- [STATE-OF-PRACTICE / CUG] Gerhardt et al., *Nine Months in the life of an all-flash file system*, CUG2024 plenary
- [PRACTITIONER] Lalli, *Transitioning HPSS Monitoring from Nagios to VictoriaMetrics*, HUF 2024

### 2.6 Public datasets
**NOT FOUND** — no NERSC-released telemetry/job/RAS dataset located. The related https://portal.nersc.gov/project/m888/resilience/data.html page (HMDR project, NERSC-hosted) describes **Blue Waters, Trinity, Mutrino, Cielo** log corpora (e.g. Blue Waters "3.4 billion log lines yielding 150,000 patterns"; Trinity OS1 2.5 billion lines/52,000 patterns; OS2 4 billion lines/500,000 patterns) but **no download links or license terms are published on that page** — treat as described-but-not-released.

### 2.7 Stated pain points — QUOTES (CUG2023, NERSC/Perlmutter section)
- *"LDMS libfabric transport has not yet been tested at scale or for resiliency"*
- *"telemetry-api to be unreliable and often inefficient… stopped feeding data at random times"*
- *"frequently caused Kafka rebalancing events"*
- *"credentials distribution… nodes are frequently unable to retrieve the secrets"*

---

## 3. LLNL

### 3.1 Systems
- **El Capitan** (HPE Cray EX, AMD MI300A APUs, Slingshot-11, #1 Top500 as of Nov 2024), Tuolumne, plus TOSS-4 commodity clusters (CTS-1/CTS-2).

### 3.2 Stack — DEPLOYED
From CUG2023 (Morrone, Scott, Shoga — LLNL co-authors): **LDMS** on TOSS 4 and CSM; **Kafka**; **VictoriaMetrics**; **Grafana**; **Elasticsearch**; **Kubernetes/OpenShift**. HPE **CSM** supplies vendor telemetry.

### 3.3 Concrete numbers — QUOTED
- El Capitan LDMS collection at a **"five second interval"**
- Kafka **"100K to 1M messages per second"** (shared tri-lab/HPE figure in the same paper)
- PostgreSQL persister scaling: 5,000-node system → **"as many as 16 copies"**

Note: LLNL user documentation for El Capitan performance tools (https://hpc.llnl.gov/documentation/user-guides/using-el-capitan-systems/using-el-capitan-systems-performance-tools) mentions only AMD OmniPerf/OmniTrace/HPCToolkit plus *"LC is currently in the process of deploying Grafana and MongoDB such that they can be used for OmniPerf analysis"* — i.e. no user-facing facility telemetry service documented.

### 3.4 Intelligence level
**L0–L2 verified.** No production L3+ found in public sources. I could not verify any public LLNL description of "Sonar" (github.com/LLNL/sonar returns 404) — **NOT VERIFIED, do not cite it.**

### 3.5 Publications
- [STATE-OF-PRACTICE / CUG] Barry, Brandt, Gentile, **Morrone**, Roman, **Scott, Shoga**, Tucker, *Evaluating and Influencing Extreme-Scale Monitoring Implementations*, CUG2023, LLNL-CONF-847852. Cross-site LLNL+SNL+LBNL+HPE+OGC — notable as a **multi-center joint state-of-practice paper**, a format worth imitating.

### 3.6 Public datasets — NOT FOUND.

### 3.7 Stated pain points — QUOTES
- *"prohibitively difficult to build a standard TOSS 4 version of LDMS that can also use the Slingshot-enabled libfabric"*
- CSM's bundled LDMS is *"significantly behind the latest LDMS release and does not contain many of the enhancements"*
- Unclear upstream plans for HPE-proprietary LDMS samplers; schema management complexity; "version discrepancies affecting community coherence"

---

## 4. SANDIA (SNL) — *the tooling center; LDMS upstream*

### 4.1 Systems 2020–2026
Astra (Arm/Marvell TX2), CTS-1/CTS-2 commodity clusters, and co-ownership of **Trinity → Crossroads** with LANL (ACES). Detailed per-system specs NOT mined here.

### 4.2 Stack — DEPLOYED
**LDMS/OVIS** (SNL-authored, https://github.com/ovis-hpc/ovis) + **syslog-ng** + SOS/DSOS storage + web portal/dashboards + notification (email/text/events). LDMS **Darshan Connector** for runtime I/O (OSTI 2004294). Kokkos↔LDMS application-metric integration.

Data path: `sampler daemons (per node) -> aggregator daemons (fan-in) -> storage (SOS/DSOS, or Kafka/Elastic sinks) -> analysis -> portal/notification`. Transports: socket, **RDMA (IB/iWarp/RoCE)**, Cray Gemini/Aries.

### 4.3 Concrete numbers — QUOTED
Brandt, *HPC Monitoring & Analysis at Sandia National Laboratories*, SAND2020-1592C (https://www.osti.gov/servlets/purl/1765307):
- Data volume **"~10s of TB/day"**
- CPU overhead **"~0.1% of a core"**
- Sampling fidelity **"down to < 10ms"**
- Fan-in **"1000s:1"**
- Dimensionality **"100s to 1000s of discrete variables"**

LDMS README (ovis-hpc/ovis): *"LDMS has been run on 10,000 cores collecting over 100,000 metric values per second with less than 0.2% overhead."*

SAND2021-11954, *Integrated System and Application Continuous Performance Monitoring and Analysis Capability (Final)* (https://www.osti.gov/servlets/purl/1822583): EMPIRE, **week-long 290-node runs → 1 TB application data + 50 TB system data**.

### 4.4 Intelligence level
**L0–L2 DEPLOYED with credible L3 capability claimed.** SAND2020-1592C lists as production analysis: log/event analysis, **event prediction and correlation**, signal analysis, numerical and textual clustering, **performance anomaly detection**. This is a slide-deck claim without per-model evidence — grade it **L3 CLAIMED, evidence thin**; treat "event prediction" as L4-claimed-not-demonstrated.

### 4.5 Publications
- [TECH-REPORT] Brandt, SAND2020-1592C, OSTI 1765307
- [TECH-REPORT] SAND2021-11954, OSTI 1822583 (FY21 ASC L2 milestone)
- [TECH-REPORT/PAPER] *LDMS Darshan Connector: For Run Time [I/O monitoring]*, OSTI 2004294
- [STATE-OF-PRACTICE / CUG] co-author on CUG2023 LLNL-CONF-847852
- [SC-TECHNICAL-PAPER, pre-window] Agelastos et al., *The Lightweight Distributed Metric Service*, SC14 (https://www.sandia.gov/app/uploads/sites/218/2022/08/SC14_Final.pdf) — **this is the one genuine SC main-track technical paper in the monitoring-infrastructure lineage, and it is from 2014.**
- [PRACTITIONER] *'Always on' performance monitoring for HPC applications systems*, Sandia HPC annual report

### 4.6 Public datasets — NOT FOUND from SNL directly (SNL data appears inside HPC-ODA, see LRZ).

### 4.7 Stated pain point — QUOTE
*"Getting data is not a challenge!"* — the stated needs are **validated, explainable machine learning** and **feature extraction from high-volume, high-dimensional data**. This is the cleanest one-line framing of the field's actual gap that I found.

---

## 5. LANL

### 5.1 Systems: Trinity (Cray XC40, with SNL), **Crossroads** (HPE Cray EX, Sapphire Rapids HBM), Chicoma, Grizzly. Per-system telemetry detail NOT FOUND.

### 5.2 Stack — **NO DETAILED PUBLIC PRODUCTION EVIDENCE FOUND** for a named LANL telemetry pipeline in 2020–2026. CUG2025 LANL contributions are configuration-management and security-audit oriented (Stradling/HPE, *Pragmatic Security Audits*; Lovell-Troy/HPE, *From Weeks to Hours: Harnessing Configuration Management and Deployment Pipelines*; Ferrell & Goetsch, *Spack Based Production Programming Environments on Cray Shasta*).

### 5.3 Public datasets — **THIS IS LANL'S CONTRIBUTION.** USRC data portal, https://usrc.lanl.gov/data/
**Failure data** (https://usrc.lanl.gov/data/failure-data.php) — license stated as *"Universal release; cite LANL"*, delivered over `ftp://hpc-ftp.lanl.gov/data/failure/`:
| Dataset | Span | Size (gz/raw) |
|---|---|---|
| All-systems failure/interrupt data (LA-UR-05-7318) | 1996–2005 | 336 KB / 2.8 MB |
| System 20 usage w/ domain (LA-UR-06-0803) | 1996–2005 | 9.9 MB / 50 MB |
| System 20 usage w/ node (LA-UR-06-0803) | 1996–2005 | 10 MB / 42 MB |
| System 20 events (LA-UR-06-0803) | 1996–2005 | 3.1 MB / 32 MB |
| System 20 node disk failures (LA-UR-06-6079) | 1996–2005 | 8 KB / 16 KB |
| System 15 / 16 / 23 / 8 usage w/ node | 1996–2005 | 560 KB–52 MB gz |

**Operational data** (https://usrc.lanl.gov/data/operational-data.php):
- **Trinity Open Science Environmental Sensors (SEDC)** — voltage, temperature, fan speeds, water flow, **Feb 9–18, 2016**, LA-UR-17-24849, `ftp://hpc-ftp.lanl.gov/data/operational/trinity_open_science_SEDC.tar.gz`
- VPIC restart subset 2016; Memory usage statistics from four open clusters (LA-UR-19-28211)

Also: USENIX CFDR mirror (https://www.usenix.org/cfdr-data, https://www.usenix.org/lanl-data) and LANL cyber datasets (https://csr.lanl.gov/data/).

**Caveat: the headline LANL failure corpus is 1996–2005 — 20+ years old and pre-GPU. It remains the most-cited HPC failure dataset, which is itself a finding: the field's canonical failure data predates every system anyone operates today.**

### 5.4 Intelligence level: **UNKNOWN from public sources.** Do not assign.

---

## 6. ALCF / ARGONNE

### 6.1 Systems 2020–2026
Theta (Cray XC40, KNL, ret. 2024), ThetaGPU (A100, 2020–2024), Polaris (HPE Apollo 6500, AMD Milan + NVIDIA A100, Slingshot-10), **Aurora** (HPE Cray EX, Intel Xeon Max + Intel Data Center GPU Max "Ponte Vecchio", Slingshot-11, ~10,624 nodes/63,744 GPUs — *node/GPU counts not re-verified in this session*), Cooley (ret.), Mira (BG/Q, ret. 2019).

### 6.2 Telemetry stack — **NO DETAILED PUBLIC PRODUCTION EVIDENCE FOUND.**
I could not locate a published ALCF description of its facility telemetry pipeline comparable to OLCF/NERSC/CSCS. The one adjacent public item is a **Grafana Labs vendor talk**, *Aurora's observability evolution: From complexity to clarity with Grafana Cloud*, ObservabilityCON on the Road 2025, SF Bay Area (https://grafana.com/events/observabilitycon-on-the-road/2025/san-francisco-bay-area/auroras-observability-evolution-with-grafana-cloud/) — **[VENDOR], title/existence verified only, content not verified; do not cite as an ALCF architecture statement without watching it.** Also note the name collision risk: "Aurora" is a common product name.

CUG2024 ALCF paper (Bertoni, Kwack, Applencourt et al., *Early Application Experiences on Aurora*) is application performance, not operations.

### 6.3 Public datasets — **ALCF's real contribution, and it is large.**
**ALCF Data Catalog**, Kyrian Adimora, IEEE DataPort, May 2025, **doi:10.21227/bhfr-wx19** (https://ieee-dataport.org/documents/argonne-leadership-computing-facility-data-catalog):
- **17 years, 2008–2025**, eight systems: Aurora (Jan–Apr 2025 system status), Polaris (Aug 2022–Apr 2025 job + system health), Theta (Jul 2017–Dec 2024), ThetaGPU (Sep 2020–Dec 2024), Mira (Apr 2013–Dec 2020), Cooley (Jun 2015–Dec 2024), Intrepid (Mar 2008–Dec 2014), GRIDFTP (Apr 2013–Dec 2024)
- Record types: **DIM_JOB_COMPOSITE, DIM_MACHINE_STATUS, DARSHAN, RAS_EVENT, TASK_HISTORY, AUTOPERF**. CSV. Users/projects anonymized.
- **Access: IEEE DataPort subscription required** — a real barrier to reproducibility, unlike Zenodo/OEDI datasets.
- Sibling public portal: https://reports.alcf.anl.gov/data/theta.html (could not be fetched in this session — egress-blocked; verify separately).

### 6.4 Intelligence level: **L0–L1 assumed but UNVERIFIED.** Do not assign a level from public evidence.

---

## 7. TACC

### 7.1 Systems: Frontera (Dell/Intel CLX, 2019–), Stampede2 (ret.), **Stampede3** (Dell, Sapphire Rapids HBM + Ponte Vecchio, 2024–), Lonestar6, Vista (NVIDIA GH200).

### 7.2 Stack — DEPLOYED: **HPCPerfStats** (formerly TACC Stats)
https://github.com/TACC/HPCPerfStats · https://tacc.utexas.edu/research/tacc-research/hpcperf-stats/ · LGPL-2.1+ · 3,388 commits · developed since 2011.

```
hpcperfstatsd (C daemon on every compute node)
   collects: CPU, socket-level memory, swap/paging, load, process data, device counters,
             filesystem (NFS/Lustre/Panasas), interconnect traffic,
             CPU + uncore performance counters (memory controllers, cache agents)
   -> RabbitMQ (quorum queues; "thousands of monitor publisher connections")
   -> central server: Django + PostgreSQL (max 500 pooled connections, parallel query workers)
   -> zstd compression, Redis cache, daily archives sealed to .tar.zst
   -> web visualization + NIGHTLY ANALYSIS
```

### 7.3 Concrete numbers — QUOTED
- Stampede3 Sapphire Rapids overhead: **"sample-window peaks of at most 3.0% of one core"** and **"0.19% average over the full window"**
- Production sampling: "multi-minute intervals"
- Deployment: all TACC systems, plus SDSC Comet, SDSC Gordon, LSU SuperMIC

### 7.4 Intelligence level
**L0–L1 DEPLOYED; L3 DEPLOYED as rule-based nightly job triage.** TACC states the nightly analysis *"flag[s] underperforming and misconfigured jobs"* on criteria including idle nodes, incorrect network usage, performance drops, and low efficiency. This is threshold/heuristic, not ML — **L2/L3 boundary, credited as L3-lite because it produces per-job classifications, not just alerts.** No L4+ found.

### 7.5 Publications
- [WORKSHOP-PEER-REVIEWED] Evans et al., *Comprehensive resource use monitoring for HPC systems with TACC Stats*, HUST'14 @ SC14, DOI 10.1109/HUST.2014.7 (OA: https://par.nsf.gov/servlets/purl/10404199)
- [CONFERENCE-PEER-REVIEWED] Evans et al., IPDPSW 2016
- [BOOK-CHAPTER/WORKSHOP] *Verifying the Correctness of HPC Performance Monitoring Data*, DOI 10.1007/978-3-031-41673-6_15
- Related survey: *A Review of Supercomputer Performance Monitoring Systems*, Supercomputing Frontiers and Innovations, https://superfri.org/index.php/superfri/article/view/392

### 7.6 Public datasets — NOT FOUND from TACC in this search.

---

## 8. CSCS (Swiss National Supercomputing Centre)

### 8.1 Systems
- **Piz Daint** (Cray XC50, P100) — retired
- **Alps** (HPE Cray EX, Slingshot-11): **~10,000 NVIDIA GH200 Grace-Hopper nodes** (CUG2024 EMOI) / **"10,752 NVIDIA Grace-Hopper GPUs"** (CUG2025 arXiv:2507.01880), plus ~1,000 heterogeneous nodes: AMD Rome CPUs, AMD MI250x and MI300, NVIDIA A100. Software-defined multi-tenant "versatile software-defined cluster" model.

### 8.2 Stack — DEPLOYED: **EMOI** (Extensible Monitoring and Observability Infrastructure)
Benini, Hanson (HPE), Gianolli, Piccinali, Brambilla, Marano, Ricciardi, Frisoni, Conciatore, CUG2024 (https://cug.org/proceedings/cug2024_proceedings/includes/files/pap113s2-file1.pdf):
```
Alps node/BMC sensors -> Cray SMA (System Monitoring Application, bundled Kafka)
   -> Logstash in SMA (or Fluentbit, rejected) -> Kafka in EMOI (Strimzi operator)
   -> KafkaStream: splits bundled multi-sensor messages into one message per sensor
   -> Logstash in EMOI: enrich (Memcached + CSM RESTful API for node metadata)
   -> Elasticsearch (ECK on RKE2 Kubernetes) -> Kibana / Grafana / custom web UIs
Infra: Terraform, Rancher, Harvester, Ubuntu MAAS, ArgoCD GitOps, Helm
```
CUG2025 (Schuppli et al., arXiv:2507.01880) adds: EMOI *"ingests telemetry data from Alps into a scalable Elasticsearch backend"*; aggregates **GPU health (temperature throttling, ECC errors), Slingshot counters, Lustre performance, and user-supplied application metrics (tokens/sec, iteration latency)**; design goals are **job-scoped dashboards (per-rank, per-GPU, per-node), global system overlays, user metric augmentation, progressive opt-in.**

### 8.3 Concrete numbers — QUOTED (sparse, and the paper says so)
- Power/energy telemetry default collection **10 Hz**; general telemetry granularity **~1 Hz**
- Energy validation study: **984 jobs across 4 node types**; telemetry-vs-Slurm energy correlations **MC 0.9997357, AG 0.9999999, NG 0.9999997, GH 0.9999837**; job energies ~10⁷ J
- **Ingestion rate, GB/day, retention, cardinality, query latency: NOT SPECIFIED in the paper.**

### 8.4 Intelligence level
**L0–L1 DEPLOYED. L2 partial. No ML — explicitly.** EMOI paper's only ML sentence is ROADMAP: *"the creation of valuable datasets for developing machine learning models dedicated to infrastructure analysis."*

### 8.5 Publications
- [STATE-OF-PRACTICE / CUG] Benini et al., *EMOI: CSCS Extensible Monitoring and Observability Infrastructure*, CUG2024, pap113
- [STATE-OF-PRACTICE / CUG] Schuppli, Mujkanovic, Drescher, VandeVondele, Mohamed, Palme, Gila, Martinasso, Hoefler, Mendonça, Conciatore, Witlox, Schulthess, *Evolving HPC services to enable ML workloads on HPE Cray EX*, CUG2025, DOI 10.1145/3757348.3757366, arXiv:2507.01880
- [STATE-OF-PRACTICE / CUG] Gila, Bonesana, Dabin, *CSCS' journey towards complete platform automation in a multi-tenant environment*, CUG2025
- [STATE-OF-PRACTICE / CUG] Di Maria et al., *Infrastructure as a Service with Strong Tenant Separation on a Supercomputer*, CUG2025 (CSCS + PSI)
- [STATE-OF-PRACTICE / CUG] Di Maria, *The WLCG Journey at CSCS: from Piz Daint to Alps*, CUG2023, pap154

### 8.6 Public datasets — NOT FOUND.

### 8.7 Stated pain points — QUOTES
- *"One prevailing theme throughout our exploration is the inherent difficulty in acquiring relevant data. Whether due to the dispersed nature of the information or the differences in how various architectures expose hardware data."*
- Heterogeneity: *"This scale-up introduces significant challenges in monitoring and observability, particularly due to the increased hardware heterogeneity…"*
- Vendor bundling: the SMA Kafka *"does not expose any external listener, which means external applications can't connect."*
- Message schema: *"Each message bundles the value for a set of different sensors in the node… it is not suitable for ingestion into ElasticSearch."*
- **"Slurm… shows sometimes a weird behaviour and cannot therefore always be trusted."**
- Fluentbit *"couldn't make it stable for large throughputs."*
- CUG2025: inefficiencies *"such as stragglers, resource under-utilization, or suboptimal communication patterns"* remain *"unnoticed due to project time or expertise limits."*

---

## 9. LRZ (Leibniz-Rechenzentrum) — *the deepest ODA research-into-production stack in Europe*

### 9.1 Systems: SuperMUC-NG (Lenovo, Intel Skylake, ~6,480 nodes, warm-water cooled), SuperMUC-NG Phase 2 (Intel PVC), CooLMUC-3 (148 nodes, Xeon Phi 7210-F), CooLMUC-4.

### 9.2 Stack — DEPLOYED: **DCDB + Wintermute**
```
Pushers (per node & per facility device; sensor sampling)
  -> MQTT
  -> Collect Agents (data brokers)
  -> Apache Cassandra (storage)
  -> Wintermute: in-band Operator/Block framework for ONLINE analytics
  -> Grafana
```
Repo: https://gitlab.lrz.de/dcdb/dcdb (LGPL-2.1, 2,378 commits since Oct 2016). Also adopted in the EU REGALE project.

### 9.3 Concrete numbers — QUOTED
From Suarez et al. 2025 (Table 4, below): **8M metrics (56/node + 12/core), 0.1–30 s intervals, 30 days retention with sub-samples indefinite.**

From Netti, Müller, Guillen, Ott, Tafani, Ozer, Schulz, *DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems*, HPDC'20, DOI 10.1145/3369583.3392674, arXiv:1910.06156:
- Query engine overhead **"below 0.5% in all cases"**; memory **"never exceeds 25MB"**; per-core CPU load **"peaks at 1.2%"**
- Derived-metric overhead **"always lower than 0.5%"**; power-prediction case study overhead **"below 0.1% and thus negligible"**
- Deployed on **CooLMUC-3 (148 nodes) and SuperMUC-NG**
- Scaling test with 1,000 synthetic sensors; production sensor spaces described as **"millions of entries"**

### 9.4 Intelligence level
**L0–L2 DEPLOYED. L3/L4 implemented in-framework and demonstrated on production systems — the best L3/L4 *infrastructure* evidence anywhere, though the papers stop short of saying "operators act on this daily."**
Three Wintermute case studies, all running in-band:
1. **L4 prediction** — random-forest power prediction at **250 ms** intervals, **"average relative error is 6.2%"**
2. **L3 feature extraction** — two-stage per-core CPI/FLOPS/vectorization → job-level indicators
3. **L3 anomaly detection** — Bayesian Gaussian mixture clustering over 2-week node power/temperature/idle-time averages, **run hourly**

Cross-check: Suarez et al. 2025 says of all German sites including LRZ — *"none of the German sites in this study are using this in production at present"* regarding ML. **So grade LRZ: L3/L4 capability deployed in the framework, but ML-driven operational decision-making not claimed as production.** This is exactly the kind of distinction the field blurs.

### 9.5 Publications
- [CONFERENCE-PEER-REVIEWED] Netti et al., *DCDB Wintermute*, HPDC'20, DOI 10.1145/3369583.3392674
- [CONFERENCE-PEER-REVIEWED] Netti et al., *From facility to application sensor data: modular, continuous and holistic monitoring with DCDB*, SC'19 (DOI 10.1145/3295500.3356191 — SC19 technical program; **verify the exact track before citing as an SC technical paper**)
- [CONFERENCE-PEER-REVIEWED] Netti et al., *A Conceptual Framework for HPC Operational Data Analytics* (companion of HPC-ODA; verify venue)
- [JOURNAL-REVIEW] Ott (LRZ) co-author on Suarez et al., Frontiers in HPC 2025
- [STATE-OF-PRACTICE / CUG] Wilde (HPE), **Ott (LRZ)**, Guyan (HPE), *First Analysis on Cooling Temperature Impacts on MI250x Exascale Nodes (HPE Cray EX235A)*, CUG2024

### 9.6 Public dataset — **HPC-ODA Dataset Collection** ⭐
Netti, A. (LRZ). Zenodo **DOI 10.5281/zenodo.3701440**, CC-BY-4.0, published 2020-09-02. 1.5 GB record (1.1 TB total across versions).
*"monitoring sensor data, acquired from the components of different HPC systems"*, gathered with **DCDB and LDMS**. **Five segments**: power-consumption prediction, fault detection, application classification, infrastructure management, cross-architecture analysis. Funded by EU DEEP-EST.
**This is the only public dataset explicitly designed as an ODA ML benchmark suite.**

### 9.7 Stated pain points — QUOTES
- *"a block template is not guaranteed to be portable across HPC systems with different sensor hierarchies"*
- *"manual configuration of ODA is prohibitive when a large amount of independent models must be deployed"*
- *"there is no generic and comprehensive solution addressing the problem of online ODA on HPC systems"*

---

## 10. CINECA + University of Bologna — *the dataset superpower*

### 10.1 Systems: Marconi (Lenovo), **Marconi100** (IBM AC922, 980 nodes, 4× V100 per node, EDR IB, 2020–2022 in dataset window), Galileo100, **Leonardo** (Atos BullSequana XH2000, ~3,456 booster nodes × 4 A100 + ~1,536 DCGP nodes, NVIDIA HDR).

### 10.2 Stack — DEPLOYED: **ExaMon**
```
plugins (IPMI, Ganglia, Nagios, Slurm, facility/cooling/CRAC/PSU/weather)
  -> MQTT broker
  -> KairosDB
  -> Apache Cassandra
  -> Grafana
(deployed via Docker, plugins managed by supervisord)
```
Repo: https://github.com/EEESlab/examon · docs: https://examonhpc.github.io/examon/
Described in the ExaData paper as *"a decade-long effort to develop the EXAMON monitoring framework deployed across Italian supercomputers."*

### 10.3 Concrete numbers — QUOTED (from the dataset descriptor)
- Marconi100: **980+ nodes**, Slurm
- **573 metrics** across all sources
- Sampling primarily **1-second resolution** (sub-second truncated as collection artifacts)
- **49.9 TB uncompressed** over **934 days** (2020-03-09 → 2022-09-28), described as **"the largest ever made public"**
- Nagios anomaly labels available only at **15-minute aggregation intervals** — this is the stated ceiling on supervised-anomaly-detection granularity

### 10.4 Intelligence level
**L0–L2 DEPLOYED. L3/L4 published as PROTOTYPE on production data — I found no statement that any model drives operations.** The descriptor's own validation results are candid about difficulty:
- Thermal hazard prediction: **F1 = 0.94** (support vector classification)
- Unsupervised anomaly detection: **AUC = 0.57** (RUAD, single-node testing) — i.e. barely above chance. **This is the most honest published number in the whole survey and should anchor any KISTI expectation-setting.**

### 10.5 Publications
- [JOURNAL-DATA-DESCRIPTOR] Antici, Borghesi, Di Santi, Molan, Seyedkazemi Ardebili, Bartolini et al., *M100 ExaData: a data collection campaign on the CINECA's Marconi100 Tier-0 supercomputer*, **Scientific Data 10, 288 (2023)**, DOI 10.1038/s41597-023-02174-3
- Related: DECICE project page (https://www.decice.eu/project-news/paper-m100-exadata/)

### 10.6 Public datasets — ⭐⭐ **best-in-class**
**M100 ExaData** — 12 Zenodo datasets with individual DOIs (index record https://zenodo.org/records/10533504), **CC-BY-4.0**. Partitioned Parquet, **zstd level 9**, organized `year_month/plugin/metric`, accessed via PyArrow Dataset API; companion Python modules at https://gitlab.com/ecs-lab/exadata/ (CC-BY-SA-2.0).
Sources: **IPMI** (core loads, temps, frequencies, memory ops, CPU power, fan speeds, GPU usage), **Slurm** (job metadata, anonymized user/job IDs), **Nagios** (admin alerts / node anomaly flags), **Ganglia**, **facility** (liquid cooling, CRAC, PSUs, weather).
Stated limitations: sub-second timing discarded; anomaly labels only at 15-min; user/job identity fully anonymized so **user-behavior analysis is impossible**; node names randomized (spatial layout documented separately); gaps where the monitoring infrastructure itself was down.

---

## 11. RIKEN R-CCS (Fugaku)

### 11.1 System: **Fugaku** — Fujitsu, ~158,976 nodes (paper says **"over 150,000"**, F-DATA says "approximately 160,000"), A64FX 48 compute cores + assistant cores, 32 GiB HBM2 per node, Tofu-D interconnect, 537 PF peak (F-DATA).

### 11.2 Stack — DEPLOYED
Terai, Yamamoto, Miura, Shoji (RIKEN R-CCS), *An Operational Data Collecting and Monitoring Platform for Fugaku: System Overviews and Case Studies in the Prelaunch Service Period*, ISC High Performance 2021 Workshops, DOI 10.1007/978-3-030-90539-2_24:
```
Tier 1 collection: HPC system logs/metrics + Building Management System (BMS) sensors
   agents deployed on the A64FX ASSISTANT (redundant) CORES  <- notable design choice
Tier 2 aggregation: Prometheus (metrics TSDB) + Elasticsearch/Logstash (logs)
Tier 3 visualization: Grafana + Kibana
```

### 11.3 Concrete numbers — QUOTED
- **"Over 150,000"** compute nodes monitored
- **"Less than 20 seconds"** from 150k+ nodes to persistent storage
- Agents run on redundant A64FX cores (near-zero application interference by construction)

### 11.4 Intelligence level
**L0–L1 DEPLOYED (paper reports two operational case studies from the prelaunch period). L3+ NOT FOUND as production.** F-DATA is explicitly framed as enabling *"job-centric predictive modelling"* — i.e. L4 as a research target, not a deployed capability.

### 11.5 Publications
- [WORKSHOP-PEER-REVIEWED] Terai et al., ISC'21, DOI 10.1007/978-3-030-90539-2_24
- [JOURNAL-DATA-DESCRIPTOR] Antici, Domke, Yamamoto, Kiziltan, Bartolini, *F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems*, **Scientific Data (2025)**, DOI 10.1038/s41597-025-05633-1

### 11.6 Public dataset — ⭐⭐ **F-DATA**
Zenodo **DOI 10.5281/zenodo.11467483**. **~24 million job executions, March 2021 – April 2024. 45 features per record. 28 GB across 38 monthly Parquet chunks.** Fields include submission/start/completion, cores/memory/nodes/frequency, **per-component power (min/avg/max)**, performance counters and derived metrics, duration and exit codes. Sensitive text irreversibly encoded with **Sentence-BERT embeddings**.
Class balance: **>21 million completed vs ~2.5 million failed** jobs.
Stated limitations: A64FX-specific (transferability unclear); no per-job water usage; raw data remains proprietary to RIKEN with access "negotiable through institutional agreements."

**Note the pattern: both F-DATA and M100 ExaData have University of Bologna (Bartolini/Antici) as the common thread. The two largest public HPC operational datasets in the world come from one academic group partnering with two different centers. That is a replicable model for KISTI.**

---

## 12. JSC (Jülich) + the German bloc

The decisive source: **Suarez, E. et al. (23 authors, 8 institutions), *Energy-aware operation of HPC systems in Germany*, Frontiers in High Performance Computing, 19 Feb 2025, DOI 10.3389/fhpcp.2025.1520207**, arXiv:2411.16204. **Section 5 / Table 4 is the only published side-by-side monitoring comparison of production HPC centers I found anywhere.**

### 12.1 Table 4 as published (verbatim values)
| Center | Metrics | Interval | Retention/Storage | Stack |
|---|---|---|---|---|
| **JSC** | **3.4M (~600/node)** | 60 s | 14 weeks – indefinite | Prometheus, Promtail, Loki, Grafana, **LLview** |
| **LRZ** | **8M (56/node + 12/core)** | **0.1–30 s** | 30 days; sub-samples indefinite | **DCDB**, MQTT, Cassandra, Grafana |
| **DKRZ** | **960k (42/node + 9/socket + 2/core)** | 1–60 s | Meta indefinite; metrics **6 months** | Collectd, Prometheus, **ClusterCockpit**, Elasticsearch, Grafana |
| **FAU** | **660k (8/node + 7/core + 3/socket + 6/GPU)** | 60 s | Job data indefinite | **ClusterCockpit**, NATS, Grafana, Munin |
| **HLRS** | **500k** | 1–120 s | 8 weeks – indefinite | Collectd, Telegraf, **LDMS**, Kafka, BarrelEye, TimescaleDB, Influx, OpenSearch, MS SQL, Grafana |
| **TUD** | **330k (24/node + 4/core + 4/GPU)** | **0.25–30 s** | Indefinite | **MetricQ**, RabbitMQ, **PIKA**, Grafana |
| **KIT** | **115k (144/node)** | 30 s | 3 months | **JobMon**, ClusterCockpit, InfluxDB |
| **MPCDF** | **100k (40/node)** | 3–240 s | Indefinite | **hpcmd**, rsyslog, **Splunk**, PDF reports |

Range across sites: **100k → 8M metrics; 0.1 s → 240 s intervals.** A ~80× spread in metric count and ~2,400× in sampling interval between peer national centers.

### 12.2 JSC specifics
- Systems: JUWELS Cluster + Booster (A100), JURECA-DC, JUSUF, **JUPITER** (Europe's first exascale system, GH200).
- **LLview** (https://github.com/FZJ-JSC/llview, GPLv3, requires CLA): collects from resource manager/scheduler + per-node daemons at **minute-scale intervals** *"to minimize computational overhead on nodes"*; per-job reporting portal built on JURI. **Reporting and dashboards; no anomaly detection.**
- JuMonC: RESTful monitoring/control of simulations at scale, DOI in Future Generation Computer Systems (S0167739X24005053).

### 12.3 Intelligence level — the whole German bloc
**L0–L2 DEPLOYED. L3+ NOT IN PRODUCTION — stated explicitly.**
- Production actions listed: power capping and DVFS; job footprint collection by threshold-based binning; **idle node power-down via Slurm** (JSC: JUSUF consumption reduced **25% year-over-year**); rule-based job anomaly detection (manual and scripted); alerting via Prometheus Alertmanager and NSCA-protocol pushes; *"automatically notifying support personnel or users from a job or user requiring attention."*
- The killer quote: ***"Machine Learning on the time series data is feasible but challenging. There are ongoing investigations how ML can be used to provide additional insights, but none of the German sites in this study are using this in production at present."***

### 12.4 Stated pain points — QUOTES
- *"Due to the varying length and number of resources used, machine learning (ML) on the time series data is feasible but challenging."*
- *"Load management and advanced scheduling software does not yet exist, or at least not in production quality."*
- Slurm monoculture across all German sites, with constrained *"dynamic scheduling or support of heterogeneous jobs."*
- *"Storage systems under load consume only slightly more energy than at idle"* — limits conventional power savings.
- Heat reuse factors **0–20%** despite direct liquid cooling.
- Grid demand-response *"poses difficult challenges to HPC scheduling systems and their capability to predict future system behavior, adding another layer of complexity well beyond what HPC operation tools are currently able to cope with."*

### 12.5 Public datasets — NOT FOUND from JSC. (LRZ's HPC-ODA covers the German bloc's dataset contribution.)

---

## 13. BSC (Barcelona)

### 13.1 System — MareNostrum 5 (arXiv:2503.09917, Banchelli, Garcia-Gasulla, Mantovani, Vinyals, Pocurull, Vicente, Eguzkitza, Acosta, Girona; BSC + HLRS)
- **GPP**: 6,480 dual-socket Sapphire Rapids nodes (56 c/socket @ 2 GHz) = 6,192 DDR (256 GB DDR5) + 216 DDR-HM (1 TB) + 72 HBM (128 GB HBM2 + 32 GB DDR5)
- **ACC**: 1,080 nodes, 2× Xeon 8460Y+ + **4× NVIDIA H100 (64 GB HBM2e)**
- Peak **314 PF**; **InfiniBand NDR200**, three-layer fat-tree, 324 switches
- Storage: 4.79 PB NVMe L1 + 367 PB HDD L2, GPFS at 1.2 TB/s read / 1.6 TB/s write; 400 PB tape + 44 PB disk cache

### 13.2 Stack — partial
**EAR (Energy Aware Runtime)** is the only monitoring component described in the paper. *"EAR collects energy measurements of three components… PCK and DRAM are performed via RAPL counters while full-node power consumption is measured through an IPMI interface."* Components: PCK (CPU package + HBM), DRAM, DC (full node), aggregated across both sockets.
- **Periodic metrics: 1 sample per minute, always enabled**
- **Job accounting: minute-interval sampling during Slurm job execution**
- **EAR Library (EARL): 10-second intervals (6 samples/min), user opt-in**
- **No Prometheus, Grafana, Elasticsearch or DCDB mentioned in this paper.**
Vendor page: https://www.ear.energy/bsc-marenostrum-5/ [VENDOR].

### 13.3 Intelligence level: **L0–L1 verified from this source; L2+ NOT FOUND.** BSC's broader monitoring stack is likely richer than this paper shows — treat as **under-documented publicly**, not as absent.

### 13.4 Publications
- [JOURNAL-PEER-REVIEWED] Banchelli et al., *Introducing MareNostrum5: A European pre-exascale energy-efficient system designed to serve a broad spectrum of scientific workloads*, Future Generation Computer Systems, DOI S0167739X25004194, arXiv:2503.09917

### 13.5 Public datasets — NOT FOUND.

---

## 14. EPCC (ARCHER2)

### 14.1 System: ARCHER2 — HPE Cray EX, 5,860 nodes × 2× AMD Rome 64-core, Slingshot-10, Lustre. (Deployment ran 19.5 PF at #22 in the referenced Top500 submission.)

### 14.2 Stack — DEPLOYED
Leach, Cass, Robson, Kazakevicius, Lafferty, Turner, Simpson (EPCC, Univ. of Edinburgh, with HPE), *Automated service monitoring in the deployment of ARCHER2*, **CUG2022** (https://cug.org/proceedings/cug2022_proceedings/includes/files/pap103s2-file1.pdf) and **Concurrency and Computation: Practice and Experience 2024**, DOI 10.1002/cpe.7892, arXiv:2303.11731.
```
Checkmk agent (TCP) on management + LOGIN servers  [NOT on compute nodes]
  -> Checkmk server (distributed, per-system)
  -> Graphite (Carbon daemons)
  -> Grafana dashboards + SAFE (service management web app, API-integrated)
```
Custom checks: **cabinet rectifier power collected every 5 seconds** (per-cabinet and system-wide draw + voltage); Slurm node-state tracking; SSH login functional test; DNS resolution; Lustre LFS server availability.

### 14.3 Intelligence level
**L0–L2 DEPLOYED, competently.** No L3+. Demonstrated operational value: DNS/network/filesystem fault isolation during deployment, **login-node memory-leak detection with quantified progression**, remote threshold-based safety controls enabling out-of-hours US-team operation, automated contractual availability reporting.

### 14.4 Public datasets — NOT FOUND.

### 14.5 Stated future work (= their own gap list)
*"Log analysis integration; Slingshot error feed incorporation; per-job Lustre statistics collection; data-driven intrusion detection systems"*, plus expanding monitoring data availability to the user community.

---

## 15. NREL

### 15.1 Systems: **Eagle** (HPE/SGI, ~2,600 nodes, 2018–2023), **Kestrel** (HPE Cray EX, 4th-gen Xeon + NVIDIA H100, 2023–), housed in the ESIF data center (warm-water cooled, heat reuse).

### 15.2 Stack — **NO DETAILED PUBLIC PRODUCTION EVIDENCE FOUND** in this search. NREL's public HPC pages (https://www.nrel.gov/esif/hpc) describe the facility, not the telemetry pipeline.

### 15.3 Public dataset — ⭐ **NREL Eagle supercomputer jobs**
Duplyakin, D. & Menear, K. (2023). Open Energy Data Initiative, **https://data.openei.org/submissions/5860**.
- **11M+ jobs**, submissions **November 2018 – February 2023**
- Files: `eagle_data.csv.bz2` (110.25 MB) and `eagle_data.parquet` (241.36 MB); 351.61 MB across 3 files including a README documenting all fields
- **License: CC-BY-4.0** — no registration, no subscription, direct download
- Anonymized to exclude user/project identity
- Authors' own framing: *"HPC research community does not have many public, large, and complete job traces like this one."*

### 15.4 Intelligence level: **UNKNOWN.** Do not assign.

---

## 16. CENTERS WITH NO PUBLIC PRODUCTION EVIDENCE FOUND

- **Pawsey Supercomputing Research Centre (Setonix)** — `NO PUBLIC PRODUCTION EVIDENCE FOUND` for a monitoring/telemetry architecture. Pawsey's user documentation Resource Overview documents systems, filesystems, compilers, debuggers and profilers but **no monitoring/telemetry infrastructure or dashboards**. Pawsey staff do publish at CUG (Elahi et al., *Migrating Complex Workflows to the Exascale*, CUG2024; Deeptimahanti on LFRic scaling, CUG2024) — but on workflows and applications, not operations telemetry.
- **CSC / LUMI** — `NO PUBLIC PRODUCTION EVIDENCE FOUND`. The LUMI user documentation (https://docs.lumi-supercomputer.eu/) names only Cray PAT and gdb4hpc; **no monitoring/telemetry infrastructure, no job energy metrics, no Grafana**. CSC staff publish at CUG on applications (Enkovaara, ICON on AMD GPUs, CUG2025), not operations. Given LUMI's scale and EuroHPC prominence this is a genuine and notable publication gap, not merely a search failure — but flag it as a search-budget-limited conclusion.
- **KAUST Supercomputing Lab** — `NO PUBLIC PRODUCTION EVIDENCE FOUND for 2020–2026`. The only substantive artifact located is **pre-window**: *Jobs I/O monitoring for Lustre at scale*, CUG2016 BoF (https://cug.org/proceedings/cug2016_proceedings.orig/includes/files/bof105.pdf) — [BOF], Shaheen II era, Lustre jobstats. Shaheen III documentation (https://docs.hpc.kaust.edu.sa/systems/shaheen3/) does not describe operational telemetry.

---

# CROSS-CUTTING DELIVERABLES

## A. Comparison table

| Center | Flagship system | Telemetry stack (deployed) | Reported data volume | Highest **verified** L-level in production | Public dataset? | Strongest publication |
|---|---|---|---|---|---|---|
| **OLCF** | Frontier (9,408n / 37,632 MI250X) | Kafka(STREAM) → Elasticsearch/Druid/Parquet-MinIO → Spark → Grafana/LVA; OpenShift+SLATE; MLflow/DVC | **4.2–4.5 TB/day**; STREAM 1.3 TB/day, 300M msg/day, 223 topics | **L3** (deterministic node screen, 1.9M tests); L4 narrow (job power NN clustering); L5 human-assisted | ✅✅ Constellation: Summit power/thermal 1 Hz; Summit GPU DBE + XID; Frontier HPL power | Shin et al., SC-W'24 (10.1109/SCW63240.2024.00226) |
| **NERSC** | Perlmutter | OMNI: RabbitMQ/Prometheus/Kafka → Elasticsearch + VictoriaMetrics → Promxy/Alertmanager → Grafana + **ServiceNow**; LDMS on PM | 522B records / **125 TB** / **25k pts/s** (2019); 25k msg/s, 20k+ sensors (2020) | **L7 partial** (rule-based auto-remediation for pre-categorized node/storage failures) | ❌ none released | Sukhija, Bautista et al., MEDES'20 (10.1145/3415958.3433046) |
| **SNL** | ACES/CTS clusters | **LDMS/OVIS** + syslog-ng + SOS/DSOS → portal/notify | **~10s of TB/day**; 100k metric-values/s on 10k cores at <0.2% | **L2**; L3 claimed (anomaly detection, event correlation), evidence thin | ❌ (contributes to HPC-ODA) | Agelastos et al., **SC14** (LDMS) — the only SC main-track paper here |
| **LLNL** | El Capitan | LDMS (5 s) + Kafka + VictoriaMetrics + Elasticsearch + Grafana on K8s/OpenShift | Kafka 100k–1M msg/s (joint figure) | **L2** | ❌ | CUG2023 LLNL-CONF-847852 (joint 4-institution) |
| **LANL** | Crossroads | not publicly documented | — | UNKNOWN | ✅ historical: USRC failure data 1996–2005; Trinity SEDC Feb 2016 | USRC data portal (LA-UR-05-7318 etc.) |
| **ALCF** | Aurora | not publicly documented | — | UNKNOWN | ✅ ALCF Data Catalog 2008–2025 (**subscription**) | Adimora, IEEE DataPort 10.21227/bhfr-wx19 |
| **TACC** | Frontera / Stampede3 | **HPCPerfStats** → RabbitMQ → PostgreSQL/Django + Redis/zstd | overhead **0.19% avg / 3.0% peak** of one core (Stampede3) | **L3-lite** (nightly rule-based flagging of underperforming/misconfigured jobs) | ❌ | Evans et al., HUST@SC14 (10.1109/HUST.2014.7) |
| **CSCS** | Alps (~10k GH200) | **EMOI**: SMA→Logstash→Kafka(Strimzi)→KafkaStream→Logstash+Memcached→Elasticsearch/Kibana/Grafana on RKE2 | **not published** (PM counters 10 Hz; telemetry ~1 Hz) | **L1–L2**; explicitly no ML | ❌ | Benini et al., CUG2024 (EMOI) |
| **LRZ** | SuperMUC-NG | **DCDB + Wintermute**: pushers→MQTT→collectagent→Cassandra→Grafana | **8M metrics**, 0.1–30 s, 30 d retention; Wintermute overhead <0.5%, <25 MB | **L2** production; L3/L4 in-band framework demonstrated (RF power pred. 6.2% err @250 ms; hourly BGM clustering) but ML not production-decisional | ✅✅ **HPC-ODA** (10.5281/zenodo.3701440, CC-BY-4.0) | Netti et al., HPDC'20 (10.1145/3369583.3392674) |
| **CINECA** | Marconi100 / Leonardo | **ExaMon**: plugins→MQTT→KairosDB→Cassandra→Grafana | **49.9 TB / 934 days**, 573 metrics, 1 s | **L2**; L3/L4 prototypes only (RUAD AUC **0.57**) | ✅✅✅ **M100 ExaData**, 12 Zenodo DOIs, CC-BY-4.0 | Antici/Borghesi/Bartolini et al., *Sci Data* 10:288 (2023) |
| **RIKEN R-CCS** | Fugaku (>150k nodes) | Prometheus + Elasticsearch/Logstash/Kibana + Grafana; agents on A64FX assistant cores | **<20 s** ingest latency from 150k+ nodes | **L1** | ✅✅ **F-DATA** (10.5281/zenodo.11467483, 24M jobs, 45 features) | Terai et al., ISC'21 (10.1007/978-3-030-90539-2_24) |
| **JSC** | JUWELS / JUPITER | Prometheus, Promtail, Loki, Grafana, **LLview** | **3.4M metrics** (~600/node), 60 s, 14 wk–∞ | **L2** + energy actuation (idle node power-down; JUSUF −25% YoY) | ❌ | Suarez et al., Front. HPC 2025 (10.3389/fhpcp.2025.1520207) |
| **BSC** | MareNostrum 5 | **EAR** (RAPL + IPMI); broader stack undocumented publicly | 1 sample/min periodic; EARL 10 s | **L1** verified | ❌ | Banchelli et al., FGCS 2025, arXiv:2503.09917 |
| **EPCC** | ARCHER2 | **Checkmk → Graphite → Grafana + SAFE**; agents on mgmt/login only | rectifier power every **5 s** | **L2** | ❌ | Leach et al., CC:P&E 2024 (10.1002/cpe.7892) |
| **NREL** | Kestrel | not publicly documented | — | UNKNOWN | ✅ **Eagle jobs**, 11M+ jobs, CC-BY-4.0 | Duplyakin & Menear, OEDI 5860 (2023) |
| **DKRZ / HLRS / FAU / KIT / MPCDF / TUD** | Levante, Hawk, etc. | see Table 4 §12.1 | 100k–960k metrics; 3 mo–∞ retention | **L2**; "none… using [ML] in production" | ❌ | Suarez et al., Front. HPC 2025 |
| **Pawsey / CSC-LUMI / KAUST** | Setonix / LUMI / Shaheen III | — | — | — | ❌ | `NO PUBLIC PRODUCTION EVIDENCE FOUND` |

## B. Which centers publish *research* vs only *practice* — and what it means

**Publish genuine research (novel method + evaluation, peer-reviewed at a research venue):**
- **LRZ** — HPDC'20, SC'19, Cluster; released a purpose-built ML benchmark dataset. The only center that built an online ODA *framework* as a research contribution and shipped it as production software.
- **CINECA (via University of Bologna)** — *Scientific Data*, plus a decade of anomaly-detection/ML papers. But note: the research author list is dominated by the **university**, not the center. CINECA supplies the machine and the data; Bologna supplies the papers.
- **RIKEN R-CCS (via University of Bologna again, for F-DATA)** — RIKEN's own contribution (Terai et al.) is an ISC *workshop* system-overview paper.
- **ORNL/OLCF** — genuinely straddles. ICS'24 GPU memory corruption is a real research paper (with **William & Mary** as the academic partner). SC-W'24 ODA is a reflective state-of-practice paper at a research venue.
- **SNL** — research-grade, but the flagship is **SC14**. Twelve years without an SC main-track follow-up.

**Publish practice only (CUG / HPCSYSPROS / HUF / tech reports):**
- **CSCS, EPCC, LLNL, NERSC (mostly), TACC (post-2016), LANL, HLRS, KIT, MPCDF, DKRZ, JSC.**
- CUG is the dominant outlet. The CUG2024/2025 monitoring sessions are overwhelmingly **HPE-authored** (Power Monitoring Counters, CADDY, Swordfish/Redfish, SDU/Metis, EVeREST) with centers as co-authors or consumers.

**What this says about where SC-regular contributions come from — three findings:**
1. **Almost none of this work reaches the SC Technical Program.** In the entire 2020–2026 window I found **zero** SC main-track technical papers on production HPC operational analytics from these centers. The good work lands at SC *Workshops*, CUG, HPCSYSPROS, ISC workshops, HPDC, ICS, or *Scientific Data*. This is a **structural opportunity**, not an absence of substance.
2. **Research output correlates with an academic partner, not with system size.** Bologna↔CINECA, Bologna↔RIKEN, W&M↔ORNL, Basel/TUM↔LRZ. Centers without a bound university group publish practice. **The highest-leverage institutional move for KISTI is to bind a university ML group to the operational data, contractually, before designing the pipeline.**
3. **Data release and research output are almost perfectly correlated.** Every center producing research (ORNL, LRZ, CINECA, RIKEN, NREL, LANL, ALCF) has released data. Every center publishing only practice (CSCS, EPCC, JSC, LLNL, TACC, NERSC, CSC, Pawsey) has released none. Releasing data appears to be the *cause*, not the effect.

## C. The 5 most useful publicly available datasets for reproducible HPC AIOps research

**1. M100 ExaData (CINECA Marconi100)** — Zenodo, 12 DOIs, index https://zenodo.org/records/10533504, **CC-BY-4.0**. 49.9 TB uncompressed, 934 days (2020-03→2022-09), 573 metrics at 1 s, 980+ nodes, **holistic**: IPMI + Slurm + Nagios labels + Ganglia + facility (cooling/CRAC/PSU/weather). Parquet/zstd, PyArrow API, tooling at https://gitlab.com/ecs-lab/exadata/.
*Best for:* node-level anomaly detection, thermal/power prediction, facility↔IT correlation. *Only dataset that spans the full sensor→facility stack.* *Limits:* Nagios labels only at 15-min; users fully anonymized.

**2. F-DATA (Fugaku)** — Zenodo **10.5281/zenodo.11467483**. 24M jobs, Mar 2021–Apr 2024, **45 features** incl. per-component power (min/avg/max) and performance counters, 28 GB Parquet, SBert-encoded text fields.
*Best for:* job-level power prediction, failure/exit-code prediction, runtime estimation, memory- vs compute-bound classification, scheduling. *The largest labeled job corpus in existence.* *Limits:* A64FX-specific; 21M success vs 2.5M failure imbalance.

**3. HPC-ODA Dataset Collection (LRZ)** — Zenodo **10.5281/zenodo.3701440**, **CC-BY-4.0**, 1.5 GB. Five task-specific segments (power prediction, fault detection, application classification, infrastructure management, cross-architecture), from **DCDB and LDMS** on multiple production systems.
*Best for:* method benchmarking and cross-system generalization. *The only dataset built as an ODA ML benchmark suite rather than a data dump — start here for method comparison, then scale to #1/#2.*

**4. OLCF Constellation operational pair (Summit)** —
 (a) **Long Term Per-Component Power and Thermal Measurements**, DOI **10.13139/OLCF/1861393** — 1 Hz native, released at 10 s / 1 min means, 5 months across 3 years, 9,252 CPUs + 27,756 GPUs;
 (b) **Summit GPU Snapshots During Double-Bit Errors and Normal Operations**, DOI **10.13139/OLCF/1970187** — XID failure records + reboot logs + scheduler records + 1 Hz BMC metrics for 27,648 V100s.
*Best for:* the only public **GPU-failure-with-telemetry-context** dataset at leadership scale — directly usable for GPU failure prediction and RCA. *Access:* Globus, Constellation terms & conditions (not a blanket open license — check before publishing derivatives).

**5. NREL Eagle supercomputer jobs** — OEDI **https://data.openei.org/submissions/5860**, **CC-BY-4.0**, 11M+ jobs, Nov 2018–Feb 2023, CSV.bz2 + Parquet, 351 MB, README documents every field.
*Best for:* scheduling, queue-wait prediction, workload characterization — and it is the **lowest-friction dataset in the list** (direct download, permissive license, small). Ideal baseline/teaching set.

*Honorable mentions with caveats:* **ALCF Data Catalog** (doi:10.21227/bhfr-wx19) — 17 years, 8 systems, RAS_EVENT + DARSHAN + AUTOPERF, richest breadth, but **IEEE DataPort subscription required**, which disqualifies it from "reproducible by anyone." **LANL USRC failure data** — canonical, universally citable, but 1996–2005 and pre-GPU.

## D. Unsolved pain points named independently by multiple centers — the research-question signals

Ranked by number of independent centers stating them.

**1. Telemetry schema / semantics are not standardized, and dashboards + models break on every system generation.** — *ORNL (twice, incl. a dedicated HPCSYSPROS paper), LLNL, CSCS, LRZ, SNL.*
> ORNL: *"Sensors, metrics, and telemetry data has not been standardized into a universal format."*
> ORNL/HPCSYSPROS: *"If the telemetry data schema changes, dashboards must be recreated using different sources, query languages, and metric names."*
> LRZ: *"a block template is not guaranteed to be portable across HPC systems with different sensor hierarchies."*
> CSCS: *"differences in how various architectures expose hardware data."*
> **Research question:** Can a schema-and-semantics layer (sensor ontology + automatic re-binding) make an ODA model or dashboard survive a system replacement with zero re-authoring — and can that be *measured* (e.g. % of models transferring Summit→Frontier, M100→Leonardo)? This is measurable today using M100 ExaData + HPC-ODA + Constellation, and no one has done it.

**2. Vendor telemetry is the weakest link: unreliable, under-documented, non-extensible, and version-lagged.** — *NERSC, LLNL, CSCS, ORNL.*
> NERSC: *"telemetry-api to be unreliable and often inefficient… stopped feeding data at random times."*
> LLNL: CSM LDMS is *"significantly behind the latest LDMS release."*
> CSCS: bundled SMA Kafka *"does not expose any external listener."*
> ORNL: *"Securing vendor cooperation for unplanned sensor implementation can be difficult."*
> **Research question:** what is the *measured* completeness/fidelity loss of vendor-supplied telemetry versus an independent collector on the same nodes, and what does that loss do to downstream model accuracy? Nobody has published a telemetry-quality benchmark. This is a strong, defensible SC-paper shape: a **telemetry integrity/observability-debt metric**.

**3. Labels are the bottleneck, not data.** — *SNL, ORNL, CINECA, all German sites.*
> SNL: *"Getting data is not a challenge!"* — the need is *"validated, explainable machine learning."*
> ORNL: ML iterations *"starved with unknown future data, low-yield features, rare events, and missing data."*
> CINECA: anomaly labels exist only at 15-min Nagios granularity; unsupervised AUC **0.57**.
> **Research question:** weak/programmatic supervision for HPC operational anomalies — can ticket systems, node-drain events, and job exit codes be composed into probabilistic labels that beat the 0.57 unsupervised baseline on M100 ExaData? A clean, reproducible, high-impact target.

**4. Nobody knows which collected data is actually used — massive unused-data accumulation.** — *ORNL (explicit), implied by the 100k→8M metric spread in Suarez et al.*
> ORNL: *"there is a notable gap in the end-to-end understanding of how the data is used, resulting in the accumulation of unused data and uncoordinated efforts."*
> **Research question:** metric utility attribution — rank streams by their marginal contribution to operational decisions, and derive a principled retention/sampling policy per stream. Given ORNL's 300,000× volume spread between streams, a utility-per-byte analysis would be immediately actionable and is entirely novel. **This is, in my judgment, the single strongest SC-Technical-Paper opportunity in the set.**

**5. ML on HPC operational time series is feasible but not production-worthy — stated by an eight-center consortium.** — *All German centers, CSCS, CINECA, ORNL.*
> Suarez et al.: *"none of the German sites in this study are using this in production at present."*
> Suarez et al.: *"Due to the varying length and number of resources used, machine learning (ML) on the time series data is feasible but challenging."*
> **Research question:** what specifically blocks the pilot→production transition? Model lifecycle under hardware drift, alert-fatigue economics, explainability requirements for operators, and the cost of a false node-drain. A rigorous **cost-of-error / operator-trust framework** for HPC AIOps does not exist and would be widely cited.

**6. Distinguishing bad hardware from bad code / bad user.** — *ORNL (explicit), CSCS (implicit).*
> ORNL: some error messages occur for *"either defective hardware or an application code bug"*; *"Discovering trends in failures is one of the most important yet most difficult tasks."*
> CSCS: stragglers and under-utilization *"unnoticed due to project time or expertise limits."*
> **Research question:** joint attribution across the system/application boundary. Requires exactly the pairing that M100 ExaData (system+job) and F-DATA (job+counters) now enable.

**7. Sub-second sampling is affordable but nobody has shown it pays.** — LRZ samples at **0.1 s** and TUD at **0.25 s**, while JSC and FAU sample at **60 s** — an ~600× disagreement between peer national centers, with **no published study justifying either end.** CINECA explicitly *discarded* sub-second data as artifacts.
> **Research question:** the sampling-rate/detection-power curve. What is the minimum sampling rate at which each class of operational event (thermal hazard, GPU DBE, straggler, network degradation) remains detectable? This directly determines KISTI's storage budget and is answerable from M100 ExaData's 1 s data by decimation. Highly practical, highly citable, and it settles a live disagreement among centers.

**8. Operational data outlives no system.** — *ORNL only, but structurally universal.*
> *"Challenge of achieving immediate data availability in the face of the relatively short lifespan of supercomputers,"* necessitating *"knowledge accumulation across generations to minimize re-work."*
> **Research question:** cross-generation transfer learning for operational models — quantify how much of a Summit-trained model survives to Frontier. Constellation now makes this partially testable.

---

### Method notes / limits of this survey
- Web search budget was exhausted at 200 queries; **LLNL "Sonar", CINECA production-deployment claims, ALCF's operational stack, and any CSC/LUMI or Pawsey monitoring documentation were not exhaustively searched.** Treat those `NOT FOUND` verdicts as provisional.
- `dl.acm.org` full-text and `osti.gov` search returned 403/robots errors; a few titles are verified by metadata only and are flagged inline (NERSC SC-W'23 power papers; ALCF Grafana vendor talk).
- `reports.alcf.anl.gov` was blocked by the egress proxy — ALCF's own public-data portal should be checked directly.
- Every number above is quoted from a page I opened. Where a center reports two different figures (e.g. ORNL Summit V100 count 27,648 vs 27,756), both are shown rather than reconciled.

**Sources:**
[STREAM (OSTI 1995656)](https://www.osti.gov/servlets/purl/1995656) · [Navigating Exascale ODA, SC-W'24](https://conferences.computer.org/sc-wpub/pdfs/SC-W2024-6oZmigAQfgJ1GhPL0yE3pS/555400b795/555400b795.pdf) · [Multi-stage Defective Hardware in Frontier, CUG2024](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap123s2-file1.pdf) · [Evaluating and Influencing Extreme-Scale Monitoring, CUG2023](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap149s2-file1.pdf) · [NERSC OMNI (LBNL datacenters)](https://datacenters.lbl.gov/resources/collecting-monitoring-and-analyzing) · [OMNI ICPP19 poster](https://www.hpcs.cs.tsukuba.ac.jp/icpp2019/data/posters/Poster18-abst.pdf) · [NERSC ServiceNow+Prometheus, MEDES'20](https://escholarship.org/content/qt7ch6t25w/qt7ch6t25w.pdf) · [Sandia HPC Monitoring & Analysis (OSTI 1765307)](https://www.osti.gov/servlets/purl/1765307) · [SAND2021-11954 (OSTI 1822583)](https://www.osti.gov/servlets/purl/1822583) · [ovis-hpc/ovis](https://github.com/ovis-hpc/ovis) · [EMOI, CUG2024](https://cug.org/proceedings/cug2024_proceedings/includes/files/pap113s2-file1.pdf) · [CSCS ML workloads, arXiv:2507.01880](https://arxiv.org/html/2507.01880v1) · [DCDB Wintermute, arXiv:1910.06156](https://arxiv.org/pdf/1910.06156) · [HPC-ODA, Zenodo](https://zenodo.org/records/3701440) · [M100 ExaData, Sci Data](https://www.nature.com/articles/s41597-023-02174-3) · [M100 ExaData Zenodo](https://zenodo.org/records/10533504) · [F-DATA, Sci Data](https://www.nature.com/articles/s41597-025-05633-1) · [Fugaku monitoring platform, ISC'21](https://link.springer.com/chapter/10.1007/978-3-030-90539-2_24) · [Energy-aware operation of HPC systems in Germany, Frontiers 2025](https://www.frontiersin.org/journals/high-performance-computing/articles/10.3389/fhpcp.2025.1520207/full) · [same, arXiv:2411.16204](https://arxiv.org/pdf/2411.16204) · [LLview](https://github.com/FZJ-JSC/llview) · [MareNostrum5, arXiv:2503.09917](https://arxiv.org/pdf/2503.09917) · [ARCHER2 monitoring, arXiv:2303.11731](https://ar5iv.labs.arxiv.org/html/2303.11731) · [TACC HPCPerfStats](https://github.com/TACC/HPCPerfStats) · [TACC HPCPerf Stats page](https://tacc.utexas.edu/research/tacc-research/hpcperf-stats/) · [Summit power/thermal dataset](https://doi.ccs.ornl.gov/dataset/086578e9-8a9f-56b1-a657-0ed8b7393deb) · [Summit GPU DBE dataset](https://doi.ccs.ornl.gov/dataset/56c244d2-d273-5222-8f4b-f2324282fab8) · [Frontier HPL power (OSTI 1975494)](https://www.osti.gov/dataexplorer/biblio/dataset/1975494-olcf-frontier-supercomputer-hpl-power-data-used-top500-green500-submission) · [ALCF Data Catalog, IEEE DataPort](https://ieee-dataport.org/documents/argonne-leadership-computing-facility-data-catalog) · [NREL Eagle jobs, OEDI](https://data.openei.org/submissions/5860) · [LANL USRC failure data](https://usrc.lanl.gov/data/failure-data.php) · [LANL USRC operational data](https://usrc.lanl.gov/data/operational-data.php) · [ORNL ODA dashboard, Zenodo](https://zenodo.org/records/15724831) · [HPCSYSPROS24 proceedings](https://github.com/HPCSYSPROS/Workshop24) · [CUG2024 at-a-glance](https://cug.org/proceedings/cug2024_proceedings/at_a_glance.html) · [CUG2025 at-a-glance](https://cug.org/proceedings/cug2025_proceedings/at_a_glance.html) · [NERSC HPSS→VictoriaMetrics, HUF2024](https://indico.kit.edu/event/742/contributions/17318) · [ExaMon](https://github.com/EEESlab/examon) · [DCDB GitLab](https://gitlab.lrz.de/dcdb/dcdb) · [KAUST Lustre jobstats, CUG2016 BoF](https://cug.org/proceedings/cug2016_proceedings.orig/includes/files/bof105.pdf)agentId: a9e32bfeacb808943 (use SendMessage with to: 'a9e32bfeacb808943', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 180970
tool_uses: 114
duration_ms: 1266545</usage>
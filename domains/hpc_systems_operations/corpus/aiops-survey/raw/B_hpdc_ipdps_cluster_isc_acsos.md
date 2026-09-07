I hit hard infrastructure limits partway through (session WebSearch budget was already exhausted by other agents; dblp.org is blocked at the network layer for direct fetch and its ToC pages truncate under WebFetch; Crossref rate-limited aggressively). I worked the census through the Crossref REST API instead, which gave me **complete proceedings tables of contents** for nearly every venue-year. Notes below separate *verified bibliography* from *my assessment*.

---

# HPC AIOps / Operational Intelligence Census — HPDC, IPDPS, Cluster, ISC, ACSOS (2020–2026)

## 0. METHOD, COVERAGE, AND CONFIDENCE

**Index used:** Crossref REST API (`api.crossref.org`), exact `container-title` / ISBN filters, full ToC enumeration with paging. dblp used only for volume discovery (blocked/truncated thereafter). ACM DL and IEEE Xplore not reachable.

**What is VERIFIED** (from Crossref records): title, DOI, venue, year, and — for the ~25 papers I pulled individually — full author list and page range.
**What is ASSESSED** (marked `[A]`): operational problem, component, data source, method, L/D/P levels, SC-relevance. **Abstracts were not retrievable at scale** — Crossref carries no abstracts for IEEE/ACM proceedings, and both search and publisher pages were blocked. So per-paper *evaluation scale* and *production-deployment* claims are marked `[UNVERIFIED — confirm from PDF]` unless I state otherwise. **No title, author, year or DOI below is invented.**

**Volume completeness verified (record counts incl. front matter):**

| Venue | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| HPDC (ACM prefix) | 3369583 ✓ | 3431379 ✓ | 3502181 ✓ | 3588195 ✓ | 3625549 ✓ | 3731545 ✓ | 3806645 ✓ (pub. 13 Jul 2026) |
| IPDPS main | 121 ✓ | 118 ✓ | 135 ✓ | 108 ✓ | 100 ✓ | 118 ✓ | 115 ✓ |
| Cluster | 82 ✓ | 119 ✓ | 83 ✓ | 39 ✓ | 47 ✓ | 46 ✓ | **not found — PARTIAL / NOT YET PUBLISHED** |
| ISC research | LNCS 978-3-030-50743-5, 27 papers ✓ | 978-3-030-78713-4, 24 papers ✓ | 978-3-031-07312-0, 15 papers ✓ | 978-3-031-32041-5, 20 papers ✓ | **UNVERIFIED** (only the *Workshops* volume 978-3-031-73716-9 is indexed) | **UNVERIFIED** | **UNVERIFIED** |
| ACSOS main | acsos49614 ✓ | acsos52086 ✓ | acsos55765 ✓ | acsos58161 ✓ | acsos61780 ✓ | acsos66086 ✓ (~13 papers) | **NOT YET PUBLISHED** |

**Three structural findings about the venues themselves (verified, and they matter for a KISTI publication strategy):**

1. **IEEE Cluster proceedings bundled its co-located workshops through 2022, then stopped.** Cluster 2020 (82 recs), 2021 (119), 2022 (83) contain HPCMASPA, EE HPC SOP, REX-IO, EA-HPC papers in the *same DOI space* as main-track papers. Cluster 2023 (39), 2024 (47), 2025 (46) contain main-track only. **Consequence:** several of the most operationally relevant "Cluster papers" from 2020–2022 (PIKA, Global Experiences with HPC ODA, LDMS Darshan Connector, out-of-band telemetry classification) are *workshop* papers, and citing them as "IEEE Cluster main track" would be wrong. I tag them `[WORKSHOP-IN-PROCEEDINGS]`.
2. **ISC's research-paper track has been shrinking and its proceedings status after 2023 is unclear.** Verified paper counts: 2020 = 27 → 2021 = 24 → 2022 = 15 → 2023 = 20. For 2024 Crossref indexes only *ISC High Performance 2024 International Workshops* (LNCS, 978-3-031-73716-9); I could **not** locate a 2024/2025/2026 Springer research-paper volume in any reachable index. The isc-hpc.com site does still advertise a research-paper submission track (deadline listed for the 2027 edition). **Report this as: ISC research-paper proceedings confirmed 2020–2023; 2024–2026 UNVERIFIED, do not cite as absent without checking Springer directly.**
3. **ACSOS is small and getting smaller, and it is essentially not an HPC venue.** ACSOS 2025 main track has ~13 technical papers. Across 2020–2025 I found **zero** ACSOS main-track papers evaluated on an HPC/supercomputer system. Everything is cloud microservices, serverless, CPS, robotics, swarm, or self-adaptive-software. The one HPC-flavoured item is a *companion/workshop* paper (Lustre metadata server, ACSOS-C 2021).

---

## 1. HPDC — ACM High-Performance Parallel and Distributed Computing

### HPDC 2020 (10.1145/3369583)
- **DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems** | Alessio Netti, Micha Müller, Carla Guillen, Michael Ott, Daniele Tafani, Gence Ozer, Martin Schulz (LRZ + TUM) | 2020 | HPDC main | `[ARCHIVAL-PEER-REVIEWED]` | 10.1145/3369583.3392674, pp.101–112 | **Problem:** no framework for *online*, in-band+out-of-band operational data analytics at center scale | **Component:** whole-center (facility, node, job) | **Data:** DCDB continuous monitoring streams | **Method:** streaming analytics plugin framework (hierarchical, in-band/out-of-band, job- and node-level models) | **Eval:** LRZ production systems `[UNVERIFIED scale/duration]` | **Real production data:** yes | **Production deployment:** DCDB is LRZ center infrastructure — `[A]` strongest deployment claim in the HPDC set, confirm from PDF | **L0–L4 (framework spanning collection→prediction)** | **D4–D5** `[A]` | **P3** | **Contribution:** the reference architecture for HPC ODA in the archival literature | **Limitation:** framework/engineering paper; limited generalizable-method claim | **SC-REGULAR-PRECEDENT**
- **Towards HPC I/O Performance Prediction through Large-scale Log Analysis** | Sunggon Kim, Alex Sim, Kesheng Wu, Suren Byna, Yongseok Son, Hyeonsang Eom (SNU/LBNL/Chung-Ang) | 10.1145/3369583.3392678, pp.77–88 | I/O performance prediction from center-scale logs | storage/PFS | Darshan-class + system logs `[A]` | ML regression `[A]` | NERSC-class logs `[UNVERIFIED]` | production data: yes | **L4 / D2 / P3** | **SC-REGULAR-RELEVANT** — *note: Korean first author, direct methodological analogue for a KISTI 한강 I/O study*
- **Orchestrating Fault Prediction with Live Migration and Checkpointing** | 10.1145/3369583.3392672 | fault prediction coupled to proactive mitigation | node/resilience | `[A]` | **L4→L7 conceptually** | authors/eval `[UNVERIFIED]` | **SC-REGULAR-RELEVANT**
- **ASA — The Adaptive Scheduling Architecture** | 10.1145/3369583.3392693 | runtime-estimate-driven adaptive scheduling | scheduler | **L4/L6** `[A]` | **SC-REGULAR-RELEVANT**

### HPDC 2021 (10.1145/3431379)
Thin for this topic. Crossref carries several ACM one-word short titles — flagged.
- **AITurbo** 10.1145/3431379.3460639 — predictable-training-job compute allocation `[A]`; **Q-adaptive** .3460650 — RL routing on Dragonfly `[A]`; **DRLPart** .3460648 — DRL resource partitioning `[A]`; **Apollo:** .3460640 `[TITLE TRUNCATED IN INDEX — UNVERIFIED]`; **Parallel Program Scaling Analysis using Hardware Counters** .3464453 (short); **Machine Learning Augmented Hybrid Memory Management** .3464450 (short). All **L4, D1, P4-ish**, **SC-REGULAR-POTENTIAL** at best for AIOps framing.

### HPDC 2022 (10.1145/3502181)
- **Understanding Memory Failures on a Petascale Arm System** | Kurt B. Ferreira, Scott Levy, Joshua Hemmert, Kevin Pedretti (Sandia) | 10.1145/3502181.3531465, pp.84–96 | **Problem:** DRAM failure behaviour on an unstudied architecture class (Astra, Arm) | **Component:** memory | **Data:** field error logs | **Method:** empirical characterization | **Eval:** Sandia Astra, production `[scale/duration UNVERIFIED]` | production data: **yes** | **L0/L2 (characterization)** | **D2** | **P2** | **Contribution:** first Arm-petascale field memory reliability study | **Limitation:** single-system, descriptive | **SC-REGULAR-PRECEDENT** (this is the exact genre SC accepts as a regular paper)
- **Access Patterns and Performance Behaviors of Multi-layer Supercomputer I/O Subsystems under Production Load** .3531461 — production I/O characterization — **L2/P2/D2** — **SC-REGULAR-PRECEDENT**
- **SchedInspector** .3531470 (RL-based scheduling inspection `[A]`); **Machine Learning Assisted HPC Workload Trace Generation for Leadership Scale Storage Systems** .3531457 (**L4**, trace synthesis, **SC-REGULAR-RELEVANT**); **Holmes** .3531464, **Heterogeneous Systems Resilience** .3531456, **Capri** .3531474, **TAC** .3531458 — `[TITLES TRUNCATED IN INDEX — UNVERIFIED]`

### HPDC 2023 (10.1145/3588195)
- **AIIO: Using Artificial Intelligence for Job-Level and Automatic I/O Performance Bottleneck Diagnosis** | Bin Dong, Jean Luca Bez, Suren Byna (LBNL / OSU) | 10.1145/3588195.3592986, pp.155–167 | **Problem:** per-job I/O bottleneck root-cause diagnosis without expert interpretation | **Component:** parallel I/O stack | **Data:** Darshan/DXT job I/O profiles | **Method:** supervised ML classifier over engineered I/O features | **Eval:** NERSC-class Darshan corpus `[UNVERIFIED]` | production data: **yes** | **L5 (RCA)** | **D2–D3** | **P4** | **Contribution:** cleanest L5 archival exemplar in HPDC | **Limitation:** label provenance / generalization across centers | **SC-REGULAR-PRECEDENT**
- **Early Exploration of Using ChatGPT for Log-based Anomaly Detection on Parallel File Systems Logs** .3595943 (short) — first LLM-for-HPC-logs item in these five venues — **L3 / D1 / P1** — **SC-REGULAR-POTENTIAL**
- **Thicket: Seeing the Performance Experiment Forest for the Individual Run Trees** .3592989 — multi-run performance data model/tooling — **L1/L2, D1–D4, P1** — **SC-REGULAR-RELEVANT**
- **Performance Optimization using Multimodal Modeling and Heterogeneous GNN** .3592984 — **L4/P4** — **PERIPHERAL** to operations

### HPDC 2024 (10.1145/3625549)
- **Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field** | Isaac Boixaderas, Sergi Moré, Javier Bartolome, David Vicente, Petar Radojković, Paul M. Carpenter, Eduard Ayguadé (BSC + MareNostrum ops) | 10.1145/3625549.3658686, pp.240–252 | **Problem:** deciding *when to act* on predicted uncorrected DRAM errors (page offlining / node draining) trading availability vs. lost work | **Component:** memory / node health | **Data:** field CE+UE logs from a production supercomputer | **Method:** RL policy over prediction outputs | **Eval:** MareNostrum-class field data `[scale/duration UNVERIFIED]` | production data: **yes** | **production deployment:** paper is framed "in the field" — `[A]` closest thing to **L7 closed-loop** in the whole 2020–2026 HPDC/IPDPS/Cluster set; confirm whether the policy actually drives the operator workflow | **L4→L7** | **D3–D5** | **P3–P4** | **Contribution:** moves the field from *predict* to *act-under-uncertainty*; the single best template for "operational problem → generalizable research" | **Limitation:** one vendor/one memory generation | **SC-REGULAR-PRECEDENT** ★ *highest-value model for a KISTI SC submission*
- **ETS: Deep Learning Training Iteration Time Prediction based on Execution Trace Sliding Window** .3658658 — runtime prediction for DL jobs — **L4/D1/P4** — **SC-REGULAR-RELEVANT**
- **Semantic-Aware Log Understanding and Analysis** .3658830 — log analytics (short / EU-projects session) — **L3/D1/P1** — **PRACTICE-ONLY**
- **FaaSRail: Employing Real Workloads to Generate Representative Load** .3658684 — workload characterization→synthesis — **P2** — **SC-REGULAR-POTENTIAL**

### HPDC 2025 (10.1145/3731545) — main track DOIs .3731570–.3731594
- **Bringing Differential Privacy to HPC: Privacy-Preserving Transformations of HPC Traces** .3731573 — **directly relevant to a national center that wants to publish/share telemetry** — **L0 (data-plane)** / **D2** / **P4** — **SC-REGULAR-RELEVANT** (and a live gap-filler: nobody else in these venues addresses telemetry release)
- **AutoSSD: CXL-Enhanced Autonomous SSDs for Low Tail Latency** .3731579 — self-managing storage device — **L7-in-the-small** — **SC-REGULAR-POTENTIAL**
- **FT2: First-Token-Inspired Online Fault Tolerance on Critical Layers for Generative LLMs** .3731570 — **SC-REGULAR-POTENTIAL**
- Workshop/poster tier: **SibylOpt: Managing Green Data Centers Using Off-Online Deep Reinforcement Learning** .3735123; **BanditWare: A Contextual Bandit-based Framework for Hardware Prediction** .3743643; **Adaptive GPU Power Capping: Balancing Energy Efficiency, Thermal Control and Performance** .3735119; **Can Large Language Models Predict Parallel Code Performance?** .3743645; **Factors Impacting I/O Time Proportion in AI Workloads** .3736815; **Multi-Node Spot Instances Availability Score Collection System** .3735122. All `[WORKSHOP/POSTER]`, **PRACTICE-ONLY** / **SC-REGULAR-POTENTIAL**.
- **Note:** HPDC 2025 main track is nearly empty of operational-intelligence work. That is itself a finding.

### HPDC 2026 (10.1145/3806645, published 13 July 2026) — **COVERAGE PARTIAL** (I enumerated ~50 of the volume's records before rate limiting; main-track DOIs run .380757x–.380760x and .38078xx, workshops/posters .3816xxx/.3818xxx/.3820xxx)
- **When RDMA Goes Long-Haul: Characterization, Modeling, and Verbs-Level Emulation with Implications for Federated Learning** .3807582 — network characterization — **P2** — **SC-REGULAR-RELEVANT**
- **GLANCED-IO: Taming I/O Optimization for Deep Learning at Scale** .3807588; **ResiHP: Taming LLM Training Failures with Dynamic Hybrid Parallelism** .3807815 (**distributed-training failure handling — the only main-track item in this class**, **L4→L7**, **SC-REGULAR-RELEVANT**); **Cremes: Cost-Efficient and Reliable Microservice Execution on Spot Instances** .3807817; **PKAS: Predictive KVCache-Aware Scheduling** .3807819
- Poster/workshop tier: **Motivating Regime-Aware User-Profiles for Runtime Prediction in Large-Scale HPC Systems** | Austin Yunker, Raj Kettimuthu (ANL) | pp.579–580 | 10.1145/3806645.3820074 — **2-page poster**, runtime prediction via per-user regime profiles — **L4/D1/P1** — **SC-REGULAR-POTENTIAL** *(a natural full-paper opportunity)*; **Decay Driven Multi Objective Optimization for HPC nodes** .3818780; **Robust I/O Characterization of Machine Learning Workloads Across Performance Analysis Tools** .3816123; **Thermal-Aware Scheduling for DNN Inference on 3D Logic-to-DRAM PNM** .3820075; **I/O Optimisation at the Compiler Level: IOOpt** .3816125.

---

## 2. IEEE IPDPS — main track only (workshops excluded per scope)

### IPDPS 2020 (10.1109/ipdps47924.2020.*)
- **Aarohi: Making Real-Time Node Failure Prediction Feasible** | Anwesha Das, Frank Mueller, Barry Rountree (NCSU + LLNL) | .00115, pp.1092–1101 | **Problem:** failure prediction latency — inference must beat the failure | **Component:** node | **Data:** system logs / RAS `[A]` | **Method:** lead-time-aware online inference pipeline | **Eval:** production HPC log corpora `[UNVERIFIED]` | production data: **yes** | **L4** | **D2–D3** | **P4** | **Contribution:** reframes failure prediction as a *latency* problem, not an accuracy problem — a genuinely generalizable research move | **SC-REGULAR-PRECEDENT**
- **Understanding the Interplay between Hardware Errors and User Job Characteristics on the Titan Supercomputer** | Seung-Hwan Lim, Ross G. Miller, Sudharshan S. Vazhkudai (ORNL) | .00028, pp.180–190 | field reliability study joining RAS + job accounting | **L2** | **D2** | **P2** | **SC-REGULAR-PRECEDENT** ★ *the canonical "join RAS with workload metadata" study — direct template for 한강*
- **The Case of Performance Variability on Dragonfly-based Systems** | Abhinav Bhatele, Jayaraman J. Thiagarajan, Taylor Groves, Rushil Anirudh, Staci A. Smith, Brandon Cook, David K. Lowenthal | .00096, pp.896–905 | **Problem:** run-to-run performance variability attribution on production Dragonfly | **Data:** network counters + job placement | **Method:** ML attribution / feature importance | **Eval:** NERSC Cori-class `[UNVERIFIED]` | **L2/L5** | **D2** | **P4** | **SC-REGULAR-PRECEDENT** ★
- **CanarIO: Sounding the Alarm on IO-Related Performance Degradation** | Michael R. Wyatt, Stephen Herbein, Kathleen Shoga, Todd Gamblin, Michela Taufer (LLNL + UTK) | .00018, pp.73–83 | online detection of shared-filesystem contention using lightweight canary probes | **L3** | **D3** `[A]` | **P4** | **SC-REGULAR-PRECEDENT**
- **What does Power Consumption Behavior of HPC Jobs Reveal?: Demystifying, Quantifying, and Predicting Power Consumption Characteristics** .00087 — **L2+L4**, power — **SC-REGULAR-PRECEDENT**
- **StragglerHelper: Alleviating Straggling in Computing Clusters via Sharing Memory Access Patterns** .00068 — straggler mitigation — **L6/L7** — **SC-REGULAR-RELEVANT**
- **A Self-Optimized Generic Workload Prediction Framework for Cloud Computing** .00085 — **L4**, cloud — **PERIPHERAL**
- Adjacent: **Sturgeon: Preference-aware Co-location ... Power Constrained Computers** .00079; **Varity: Quantifying Floating-Point Variations in HPC Systems Through Randomized Testing** .00070; **Reservation and Checkpointing Strategies for Stochastic Jobs** .00092; **Resilient/Learning-based perf modeling**: .00034, .00095.

### IPDPS 2021 (10.1109/ipdps49936.2021.*)
- **Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data** | Alessio Netti, Daniele Tafani, Michael Ott, Martin Schulz | .00010, pp.2–12 | **Problem:** monitoring data volume/dimensionality — how to reduce telemetry without losing signal | **Component:** center-wide monitoring | **Data:** DCDB monitoring streams | **Method:** correlation-based feature aggregation/reduction | **Eval:** LRZ / Marconi-class `[UNVERIFIED]` | production data: **yes** | **L0/L1** | **D2–D4** | **P4** | **Contribution:** *the* telemetry-reduction paper in these venues — and there is essentially no competitor | **SC-REGULAR-PRECEDENT** ★ *directly addresses the 한강 telemetry-volume problem*
- **Systemic Assessment of Node Failures in HPC Production Platforms** | Anwesha Das, Frank Mueller, Barry Rountree | .00035, pp.267–276 | production node-failure field study | **L2** | **D2** | **P2** | **SC-REGULAR-PRECEDENT**
- **Interpreting Write Performance of Supercomputer I/O Systems with Regression Models** .00064 — interpretable I/O performance modeling on production logs — **L4/L5** — **D2** — **P4** — **SC-REGULAR-PRECEDENT** `[authors not fetched]`
- **Performance Evaluation of Adaptive Routing on Dragonfly-based Production Systems** .00042 — production network study — **P2** — **SC-REGULAR-RELEVANT**
- **Towards Internet-Scale Convolutional Root-Cause Analysis with DIAGNET** .00084 — **L5**, internet/network not HPC — **PERIPHERAL** but methodologically citable for RCA
- **Demystifying GPU Reliability: Comparing and Combining Beam Experiments, Fault Simulation, and Profiling** .00037 — GPU reliability methodology — **P2/P4** — **SC-REGULAR-RELEVANT**
- **Improving checkpointing intervals by considering individual job failure probabilities** .00038 — prediction→policy — **L4→L6** — **SC-REGULAR-RELEVANT**
- **Deep Reinforcement Agent for Scheduling in HPC** .00090 — **L6** — **SC-REGULAR-RELEVANT**
- **Noise-Resilient Empirical Performance Modeling with Deep Neural Networks** .00012; **Dancing in the Dark: Profiling for Tiered Memory** .00011; **AuTraScale** .00100 (cloud autoscaling); **AlphaR** .00089 (microservice RM) — **PERIPHERAL**

### IPDPS 2022 (10.1109/ipdps53621.2022.*)
- **Resource Utilization Aware Job Scheduling to Mitigate Performance Variability** .00040 — variability-aware scheduling from utilization telemetry — **L4→L6** — **SC-REGULAR-RELEVANT**
- **A Quantitative Study of the Spatiotemporal I/O Burstiness of HPC Application** .00133 — **P2** — **SC-REGULAR-RELEVANT**
- **An End-to-end and Adaptive I/O Optimization Tool for Modern HPC Storage Systems** .00128 — **L6** — **SC-REGULAR-RELEVANT**
- **Hybrid Workload Scheduling on HPC Systems** .00052 — **L6** — **SC-REGULAR-RELEVANT**
- **P-ckpt: Coordinated Prioritized Checkpointing** .00049; **PowerSpector: Towards Energy Efficiency with Calling-Context-Aware Profiling** .00126; **RLRP: High-Efficient Data Placement with Reinforcement Learning for Modern Distributed Storage Systems** .00064; **Multi-Phase Task-Based HPC Applications: Quickly Learning how to Run Fast** .00042; **MemGaze**-class trace analysis — **SC-REGULAR-POTENTIAL / PERIPHERAL**
- **Observation:** IPDPS 2022 (135 records, the largest volume in the window) contains **no** dedicated anomaly-detection or failure-prediction paper. Notable trough.

### IPDPS 2023 (10.1109/ipdps54959.2023.*)
- **Drill: Log-based Anomaly Detection for Large-scale Storage Systems Using Source Code Analysis** | Di Zhang, Chris Egersdoerfer, Tabassom Mahmud, Mai Zheng, Dong Dai (UNC Charlotte + Iowa State) | .00028, pp.189–199 | **Problem:** log-based anomaly detection without labels, using the *source code that emits the logs* as a semantic prior | **Component:** parallel file system (Lustre-class) | **Data:** PFS logs + source | **Method:** static source analysis → log-template semantics → anomaly detection | **Eval:** `[UNVERIFIED]` | **L3** | **D1–D2** | **P4** | **Contribution:** the most methodologically original log-anomaly idea in the window — sidesteps the labelled-data problem | **SC-REGULAR-PRECEDENT** ★
- **FaultyRank: A Graph-based Parallel File System Checker** .00029 — storage fault localization at scale — **L5** — **SC-REGULAR-RELEVANT**
- **Alioth: A Machine Learning Based Interference-Aware Performance Monitor for Multi-Tenancy Applications in Public Cloud** .00095 — **L3/L5**, cloud — **PERIPHERAL** (good method, wrong system class)
- **Optimizing HPC I/O … / Evaluating Asynchronous Parallel I/O on HPC Systems** .00030; **RLP: Power Management Based on a Latency-Aware Roofline Model** .00052; **Power Constrained Autotuning using Graph Neural Networks** .00060; **SRC: Mitigate I/O Throughput Degradation in Network Congestion Control of Disaggregated Storage** .00035 — **SC-REGULAR-POTENTIAL**

### IPDPS 2024 (10.1109/ipdps57955.2024.*)
- **Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining** | Baolin Li (Northeastern), Siddharth Samsi, Vijay Gadepally (MIT-LL), Devesh Tiwari (Northeastern) | .00037, pp.337–349 | **Problem:** operators cannot act on black-box models — need *interpretable* rules over GPU-cluster telemetry | **Component:** GPU cluster (MIT SuperCloud-class) | **Data:** production GPU monitoring time series | **Method:** association rule mining | **Eval:** production GPU cluster `[scale/duration UNVERIFIED]` | production data: **yes** | **L2/L3/L5** | **D2–D4** | **P3–P4** | **Contribution:** explicitly optimizes for *operator consumability*, which is the D4 bridge almost nobody else crosses | **SC-REGULAR-PRECEDENT** ★ *closest published analogue to a 한강 GPU-telemetry paper*
- **Cross-System Analysis of Job Characterization and Scheduling in Large-Scale Computing Clusters** .00069 — **multi-system** workload/scheduling comparison — **L2** | **D2** | **P2** | **SC-REGULAR-PRECEDENT** (multi-center comparison is rare and valued)
- **TunIO: An AI-powered Framework for Optimizing HPC I/O** .00050 — **L6** — **SC-REGULAR-RELEVANT**
- **A2FL: Autonomous and Adaptive File Layout in HPC through Real-time Access Pattern Analysis** .00051 — **L7 (closed loop, in-system)** — **SC-REGULAR-RELEVANT**
- **Drilling Down I/O Bottlenecks with Cross-layer I/O Profile Exploration** .00053 — **L5** — **SC-REGULAR-RELEVANT**
- **Capturing Periodic I/O Using Frequency Techniques** .00048 — signal-processing on I/O telemetry — **L2/L3** — **SC-REGULAR-RELEVANT**
- **MAAD: A Distributed Anomaly Detection Architecture for Microservices Systems** .00094 — **L3**, cloud — **PERIPHERAL**
- **FEDGE: An Interference-Aware QoS Prediction Framework for Black-Box Scenario in IaaS Clouds with Domain Generalization** .00020 — cloud, but the *domain-generalization* framing is transferable across HPC systems — **PERIPHERAL / methodologically useful**
- **Druto: Upper-Bounding Silent Data Corruption Vulnerability in GPU Applications** .00058; **Predicting Cross-Architecture Performance of Parallel Programs** .00057; **SYNPA: SMT Performance Analysis and Allocation of Threads** .00068; **Hadar** .00066 — **SC-REGULAR-POTENTIAL**

### IPDPS 2025 (10.1109/ipdps64566.2025.*)
- **An Effective Uncorrectable Memory Error Prediction Framework by Exploiting UPH Indicators in Production Environments** | Xiaobo Zheng, Lisha Qin, Shiyi Li, Wen Xia, Chentao Wu, Yunfei Gu, Qicong Lin, Jun Wan, Huifang Jiao, Rubing Huang | .00112, pp.1238–1248 | UE prediction from novel "UPH" indicators, production environment | **L4** | **D2–D4** | **P3** | **SC-REGULAR-PRECEDENT** — *pairs with HPDC'24 BSC paper; together they are the memory-failure-prediction state of the art in these venues*
- **IOAgent: Democratizing Trustworthy HPC I/O Performance Diagnosis Capability via LLMs** | Chris Egersdoerfer, Arnav Sareen, Jean Luca Bez, Suren Byna, Dongkuan DK Xu, Dong Dai | .00036, pp.322–334 | **Problem:** I/O diagnosis expertise doesn't scale to users; LLM outputs are untrustworthy | **Component:** I/O stack | **Data:** Darshan/DXT + tool outputs | **Method:** LLM agent with grounding/trust mechanisms | **L5/L6** | **D2–D3** | **P4** | **Contribution:** first *trustworthiness-aware* LLM-agent operations paper in this venue set | **SC-REGULAR-PRECEDENT** ★ — the live frontier
- **A Deep Look into the Temporal I/O Behavior of HPC Applications** .00072 — **P2** — **SC-REGULAR-RELEVANT**
- **Be Aware of Metadata Corruption in Parallel File System: It can be Silent and Catastrophic** .00063 — silent-corruption field/analysis study — **SC-REGULAR-RELEVANT**
- **PALLAS: A Generic Trace Format for Large HPC Trace Analysis** .00032 — telemetry/trace data-plane — **L0** — **SC-REGULAR-RELEVANT**
- **FlowForecaster: Automatically Inferring Detailed & Interpretable Workflow Scaling Models for Forecasts** .00045 — **L4**, interpretable — **SC-REGULAR-RELEVANT**
- **P³ Forecast: Personalized Privacy-Preserving Cloud Workload Prediction Based on Federated GANs** .00038 — cloud; but *privacy-preserving workload prediction* pairs with HPDC'25 DP-traces — **PERIPHERAL / strategically interesting**
- **GNNPerf** .00079; **AdapTBF: Decentralized Bandwidth Control … for HPC Storage** .00074; **AI and HPC Applications on Leadership Computing Platforms: Performance and Scalability Studies** .00027; **Phase-Based Frequency Scaling for Energy-Efficient Heterogeneous Computing** .00078 — **SC-REGULAR-POTENTIAL**

### IPDPS 2026 (10.1109/ipdps65963.2026.*) — **published, verified**
- **Characterizing Production GPU Workloads using System-wide Telemetry Data** | Onur Cankur, Brian Austin, Dhruva Kulkarni, Abhinav Bhatele (UMD + NERSC) | .00078, pp.899–912 | **Problem:** what do GPU jobs actually do, center-wide, as seen only from always-on system telemetry | **Component:** GPU nodes, center-wide | **Data:** system-wide GPU telemetry (NERSC Perlmutter-class, given the NERSC co-authors) `[system identity A — confirm]` | **Method:** large-scale empirical characterization | production data: **yes** | **L2** | **D2** | **P2–P3** | **SC-REGULAR-PRECEDENT** ★★ *this is the single closest published analogue to the 한강 GPU telemetry census; anything KISTI writes must differentiate from it*
- **The Case of the Elusive Application Performance on Production GPU Supercomputers** | Cunyang Wei, Keshav Pradeep, Abhinav Bhatele (UMD) | .00079, pp.913–927 | performance variability/attribution on production GPU systems | **L2/L5** | **D2** | **P4** | **SC-REGULAR-PRECEDENT** ★★ — *direct lineal descendant of Bhatele's IPDPS'20 Dragonfly variability paper, now on GPU machines*
- **KORAL: Knowledge Graph Guided LLM Reasoning for SSD Operational Analysis** .00085 — **L5/L6**, knowledge-graph-grounded LLM for storage operations — **SC-REGULAR-PRECEDENT** (the 2026 frontier: LLM + structured operational knowledge)
- **Beyond Thread States: Diagnosing Performance Degradation with eBPF and Thread Dynamics** .00073 — low-overhead in-production diagnosis — **L5/D3** — **SC-REGULAR-RELEVANT**
- **Enhancing HPC Batch Job Scheduling via Imitation Learning-Based Search** .00104 — **L6** — **SC-REGULAR-RELEVANT**
- **PowerMorph: Shaping LLM Training for Data Center Demand Response** .00100 — power/grid-aware operation — **L7** — **SC-REGULAR-RELEVANT**
- **SMART-MIG: A Learning Framework for Scalable and Energy-Efficient GPU Scheduling** .00084; **Characterizing Dataflow for I/O-Aware Scheduling in HPC Workflows** .00076; **Toward Energy-Efficient HPC: Insights from Power Profiling a Cloud-Resolving Earth System Model** .00082; **Beyond Throughput: Performance and Energy Insights of LLM Inference Across AI Accelerators** .00083; **QoSFlow: … Interpretable Sensitivity Models** .00112; **WaterSplit: Coordinated On-Site and Off-Site Water Allocation for Sustainable Datacenter Cooling** .00113; **UCTRACE** .00074; **SecPerf: Demystifying Cost of Confidential HPC** .00075 — **SC-REGULAR-POTENTIAL**

---

## 3. IEEE Cluster

### Cluster 2020 (10.1109/cluster49012.2020.*) — main + bundled workshops
**Main track:**
- **Quantifying the Impact of Network Congestion on Application Performance and Network Metrics** | Yijia Zhang, Taylor Groves, Brandon Cook, Nicholas J. Wright, Ayse K. Coskun (BU + NERSC) | .00026, pp.162–168 | congestion→performance attribution on production | **L2/L5** | **D2** | **P4** | **SC-REGULAR-PRECEDENT**
- **Co-scheML: Interference-aware Container Co-scheduling Scheme Using ML Application Profiles for GPU Clusters** .00020 — **L4/L6** — **SC-REGULAR-RELEVANT**
- **Analysis of Cooling Water Temperature Impact on Computing Performance and Energy Consumption** .00027 — facility↔compute coupling, rare in a main track — **L2** — **SC-REGULAR-RELEVANT**
- **Towards End-to-end SDC Detection for HPC Applications Equipped with Lossy Compression** .00043; **Resilient Scheduling of Moldable Jobs on Failure-Prone Platforms** .00018; **tf-Darshan** .00046; **Modeling the Performance of Scientific Workflow Executions … with Burst Buffers** .00019; **Predicting MPI Collective Communication Performance Using Machine Learning** .00036; **Grade10** .00016 — **SC-REGULAR-POTENTIAL**

**`[WORKSHOP-IN-PROCEEDINGS]` (HPCMASPA .00061–.00066; EE HPC SOP .00067–.00074):**
- **PIKA: Center-Wide and Job-Aware Cluster Monitoring** .00061 — production monitoring infrastructure (TU Dresden) — **L0/L1** | **D5** | **P0/P1** — **PRACTICE-ONLY** but a key ODA citation
- **HPC System Data Pipeline to Enable Meaningful Insights through Analysis-Driven Visualizations** .00062; **MAP: A Visual Analytics System for Job Monitoring and Analysis** .00063; **Towards Workload-adaptive Scheduling for HPC Clusters** .00064; **Democratizing Parallel Filesystem Monitoring** .00065; **LDMS Monitoring of EDR InfiniBand Networks** .00066
- **Global Experiences with HPC Operational Data Measurement, Collection and Analysis** .00071 — **multi-center ODA survey; the field's reference "state of practice" paper** — **PRACTICE-ONLY**, high citation value
- **A Study of Operational Impact on Power Usage Effectiveness Using Facility Metrics and Server Operation Logs in the K Computer** .00072; **A Supercomputing Center Experience With Cooling Control Design** .00073; **Investigative Report on Electrical Commissioning in HPC Data Centers** .00074; **HUD-Oden** .00070; **Toward an End-to-End Auto-tuning Framework in HPC PowerStack** .00068; **Energy Optimization and Analysis with EAR** .00067

### Cluster 2021 (10.1109/cluster48925.2021.*)
**Main track:**
- **Monitoring Large Scale Supercomputers: A Case Study with the Lassen Supercomputer** | Tapasya Patki, Adam Bertsch, Ian Karlin, Dong H. Ahn, Brian Van Essen, Barry Rountree, Bronis R. de Supinski (LLNL), Nathan Besaw (IBM) | .00057, pp.468–480 | **Problem:** what it actually takes to monitor a leadership GPU system end-to-end | **Component:** center-wide | **Data:** LDMS/Splunk-class production monitoring `[A]` | **Method:** case study + architecture | **Eval:** Lassen (LLNL), production | production data: **yes** | production deployment: **yes** | **L0–L2** | **D4–D5** | **P0–P2** | **SC-REGULAR-PRECEDENT** — *the "we built and ran it" archetype; note it got into the main track, not a workshop*
- **Understanding the Effects of DRAM Correctable Error Logging at Scale** | Kurt B. Ferreira, Scott Levy, Victor Kuhns, Nathan DeBardeleben, Sean Blanchard (Sandia + LANL) | .00060, pp.421–432 | CE logging cost/benefit at scale — **field study with an operational decision attached** | **L2** | **D2–D4** | **P2** | **SC-REGULAR-PRECEDENT**
- **Characterizing Impacts of Storage Faults on HPC Applications: A Methodology and Insights** .00048 — **P2/P4** — **SC-REGULAR-RELEVANT**
- **Bellamy: Reusing Performance Models for Distributed Dataflow Jobs Across Contexts** .00052 — cross-context transfer of performance models — **L4/P4** — **SC-REGULAR-RELEVANT**
- **RPTCN: Resource Prediction for High-dynamic Workloads in Clouds based on Deep Learning** .00038; **READYS: A Reinforcement Learning Based Strategy for Heterogeneous Dynamic Scheduling** .00031; **WIRE: Resource-efficient Scaling with Online Prediction for DAG-based Workflows** .00025; **RELAR: RL for Adaptive Routing in NoCs** .00069; **Understanding Soft Error Sensitivity of Deep Learning Models and Frameworks through Checkpoint Alteration** .00045; **Incorporating Fault-Tolerance Awareness into System-Level Modeling and Simulation** .00080 — **SC-REGULAR-POTENTIAL**

**`[WORKSHOP-IN-PROCEEDINGS]` (HPCMASPA ≈.00086–.00095; EE HPC SOP ≈.00081–.00089):**
- **A Conceptual Framework for HPC Operational Data Analytics** .00086 — **the definitional ODA paper (Netti/Ott/Schulz lineage); cite this for taxonomy** — **PRACTICE-ONLY** but foundational
- **Sequence-RTG: Efficient and Production-Ready Pattern Mining in System Log Messages** .00090 — log template mining, production-ready framing — high relevance
- **An Integrated Job Monitor, Analyzer and Predictor** .00091; **An Execution Fingerprint Dictionary for HPC Application Recognition** .00092; **Backfilling HPC Jobs with a Multimodal-Aware Predictor** .00093; **The Challenge of Disproportionate Importance of Temporal Features in Predicting HPC Power Consumption** .00094; **Dynamic and Adaptive Monitoring and Analysis for Many-task Ensemble Computing** .00095; **Halcyon: Unified HPC Center Operations** .00081; **Cooling the Data Center: … Owner Project Requirements (OPR) Template** .00085; **FIRESTARTER 2** .00084; **A Dynamic Power Capping Library for HPC Applications** .00073

### Cluster 2022 (10.1109/cluster51413.2022.*)
**Main track:**
- **ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems** | Burak Aksar, Efe Sencan, Benjamin Schwaller, Omar Aaziz, Vitus J. Leung, Jim Brandt, Brian Kulis, Ayse K. Coskun (BU + Sandia) | .00048, pp.369–380 | **Problem:** labelling anomalies in production telemetry is the bottleneck | **Component:** compute nodes, center-wide | **Data:** Sandia LDMS production telemetry (Eclipse/Voltrino-class `[A]`) | **Method:** active learning over telemetry features to minimize labelling cost | production data: **yes** | **L3/L5** | **D2–D3** | **P4** | **Contribution:** attacks the *label-scarcity* problem head-on — the single most transferable idea for a center starting from zero labels | **SC-REGULAR-PRECEDENT** ★★ *most directly reusable for 한강*
- **Be SMART, Save I/O: A Probabilistic Approach to Avoid Uncorrectable Errors in Storage Systems** .00038 — SMART-driven proactive avoidance — **L4→L7** — **SC-REGULAR-RELEVANT**
- **Extracting and characterizing I/O behavior of HPC workloads** .00037 — **P2** — **SC-REGULAR-RELEVANT**
- **What does Inter-Cluster Job Submission and Execution Behavior Reveal to Us?** .00019 — **multi-cluster** user-behaviour study — **P2** — **SC-REGULAR-RELEVANT**
- **MRSch: Multi-Resource Scheduling for HPC** .00020 (RL scheduling); **HPC Storage Service Autotuning Using Variational-Autoencoder-Guided Asynchronous Bayesian Optimization** .00049; **PYTHIA: an oracle to guide runtime system decisions** .00025; **ACCLAiM: … MPI Collective Communication Autotuning Using Machine Learning** .00030; **The role of storage target allocation in applications' I/O performance with BeeGFS** .00039; **Protecting Metadata Servers From Harm Through Application-level I/O Control** .00075 — **SC-REGULAR-RELEVANT / POTENTIAL**

**`[WORKSHOP-IN-PROCEEDINGS]` HPCMASPA 2022 (.00076–.00082):**
- **Towards Real-Time Classification of HPC Workloads via Out-of-band Telemetry** .00078 — *out-of-band only* classification; extremely relevant to a center that cannot instrument user jobs — **L2/L3** — high value despite workshop status
- **LDMS Darshan Connector: For Run Time Diagnosis of HPC Application I/O Performance** .00082; **Shasta Log Aggregation, Monitoring and Alerting in HPC Environments with Grafana Loki and ServiceNow** .00079 (**L2 rule alerting, D5 production, P0**); **Bridging the Gap between Application Performance Analysis and System Monitoring** .00080; **IncProf** .00081; **A Comprehensive I/O Knowledge Cycle for Modular and Automated HPC Workload Analysis** .00076; **Assessment of the I/O and Storage Subsystem in Modular Supercomputing Architectures** .00077
- Also in-proceedings: **An Analysis of Performance Variability on Dragonfly+ topology** .00061

### Cluster 2023 (10.1109/cluster52292.2023.*) — main track only, 39 records
- **Optimizing HPC I/O Performance with Regression Analysis and Ensemble Learning** .00027 — **L4/L6** — **SC-REGULAR-RELEVANT**
- **PredictDDL: Reusable Workload Performance Prediction for Distributed Deep Learning** .00009 — **L4/P4** — **SC-REGULAR-RELEVANT**
- **GPU Occupancy Prediction of Deep Learning Models Using Graph Neural Network** .00034; **Hierarchical Resource Partitioning on Modern GPUs: A Reinforcement Learning Approach** .00023; **ExplSched: Maximizing Deep Learning Cluster Efficiency for Exploratory Jobs** .00022; **ProvLight: Efficient Workflow Provenance Capture on the Edge-to-Cloud Continuum** .00026 — **SC-REGULAR-POTENTIAL**
- **Observation:** Cluster 2023 has **no** anomaly-detection, failure-prediction, or monitoring-infrastructure paper in the main track. The topic left with the workshops.

### Cluster 2024 (10.1109/cluster59578.2024.*) — 47 records
- **GPU Reliability Assessment: Insights Across the Abstraction Layers** .00008 — **P2** — **SC-REGULAR-RELEVANT**
- **A Protocol to Assess the Accuracy of Process-Level Power Models** .00014 and **Automated Approach for Accurate CPU Power Modelling** .00016 — power-model validity — **P4** — **SC-REGULAR-RELEVANT**
- **I/O Behind the Scenes: Bandwidth Requirements of HPC Applications with Asynchronous I/O** .00044 — **P2**
- **DaYu: Optimizing Distributed Scientific Workflows by Decoding Dataflow Semantics and Dynamics** .00038; **Holistic Performance Analysis for Asynchronous Many-Task Runtimes** .00015; **Job Scheduling in HPC Systems with Disaggregated Memory Resources** .00033; **Understanding Mixed Precision GEMM with MPGemmFI** .00022; **FT K-Means** .00035; **RL-Cache** .00025 — **SC-REGULAR-POTENTIAL**
- **Observation:** again no monitoring/anomaly/failure-prediction main-track paper.

### Cluster 2025 (10.1109/cluster59342.2025.*) — 46 records — **the topic returns**
- **Proactive SSD Failure Prediction with A Gradient-Guided LSTM-xLSTM Hybrid Model** | Xiaofei Wang, Yang Zhang, Junyan Chen, Xin Wu, Daiwei Du, Feng Wang, Gang Wang, Xiaozhou Liu, Xiaoguang Liu, Yu Zhang | .11186457, pp.1–11 | device failure prediction — **L4** | **D2–D3** | **P3–P4** | **SC-REGULAR-RELEVANT**
- **Are We There Yet? Predicting the Queue Wait Times for HPC Jobs** | Christin Whitton, William Jones, Craig Walker, Vanessa Job, Steven Senator, Nathan DeBardeleben (LANL + Coastal Carolina) | .11186489, pp.1–12 | **Problem:** user-facing queue-wait prediction from real scheduler history | **Component:** batch scheduler | **Data:** LANL production job records `[A]` | **L4** | **D2–D4** | **P3** | **SC-REGULAR-PRECEDENT** — *a lab-authored, user-facing prediction service; excellent template for a center deliverable that is also publishable*
- **Detecting Silent Data Corruption from Hardware Counters** .11186479 — **L3** — **SC-REGULAR-RELEVANT**
- **EquilibrIO: Taming the I/O Tides in High-Performance Computing** .11186490 — I/O contention control — **L6/L7** — **SC-REGULAR-RELEVANT**
- **Multi-agent Independent PPO-based Automatic ECN Tuning for High-Speed Data Center Networks** .11186496 — **L7** network self-tuning — **SC-REGULAR-RELEVANT**
- **CFseq: A Framework for Constructing Compression-Friendly Field Sequences for Network Logs** .11186454 — log data reduction — **L0** — **SC-REGULAR-POTENTIAL**
- **Fine-Grain Energy Consumption Modeling of HPC Task-Based Programs** .11186478; **NSYS2PRV: Detailed and Quantitative Analysis of Large-Scale GPU Execution Traces with Paraver** .11186477; **DDRM: An SLO-aware Deep Dynamic Resource Management Framework for Microservices** .11186472; **TRACE: A Targeted Recommender for VM Assignment** .11186461; **GreenK8s** .11186459 — **SC-REGULAR-POTENTIAL / PERIPHERAL**

### Cluster 2026 — **PARTIAL / NOT YET PUBLISHED** (no records indexed as of this census)

---

## 4. ISC High Performance — research paper track

**Track history (report this accurately):** verified Springer LNCS research-paper volumes for **2020 (978-3-030-50743-5, 27 papers), 2021 (978-3-030-78713-4, 24), 2022 (978-3-031-07312-0, 15), 2023 (978-3-031-32041-5, 20)**. Volume sizes are small and shrinking, and the track is organized into fixed sections ("Performance Modeling, Evaluation, and Analysis" is where operational work lands). For **2024–2026** I could confirm only the *ISC 2024 International Workshops* volume (978-3-031-73716-9); the research-paper volumes are **UNVERIFIED** — I could not reach dblp or Springer search to settle it. Do not state the track was discontinued without direct confirmation.

### ISC 2020
- **Predicting Job Power Consumption Based on RJMS Submission Data in HPC Systems** | 10.1007/978-3-030-50743-5_4 | job power prediction from *submission-time* metadata (no runtime telemetry needed) | scheduler + power | **L4** | **D2** | **P3–P4** | **SC-REGULAR-RELEVANT** — *very attractive framing: predicts before the job runs*
- **Semi-automatic Assessment of I/O Behavior by Inspecting Individual Client-Node Timelines** | _9 | **L2/L5** — **SC-REGULAR-RELEVANT**
- **Desynchronization and Wave Pattern Formation in MPI-Parallel and Hybrid Memory-Bound Programs** | _20 — performance variability mechanism — **P4** — **SC-REGULAR-RELEVANT**
- **Timemory: Modular Performance Analysis for HPC** _22; **Time Series Mining at Petascale Performance** _6; **Footprint-Aware Power Capping for Hybrid Memory Based Systems** _18; **Understanding HPC Benchmark Performance on Intel Broadwell and Cascade Lake Processors** _21; **Reinit++** _27; **TeaMPI** _23 — **SC-REGULAR-POTENTIAL**
- `[WORKSHOPS VOLUME 978-3-030-59851-8]`: **Application IO Analysis with Lustre Monitoring Using LASSi for ARCHER** _16; **Characterizing I/O Optimization Effect Through Holistic Log Data Analysis of Parallel File Systems and Interconnects** _11 — both highly on-topic but **workshop**

### ISC 2021
- **Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems** | Burak Aksar, Yijia Zhang, Emre Ates, Benjamin Schwaller, Omar Aaziz, Vitus J. Leung, Jim Brandt, Manuel Egele, Ayse K. Coskun | 10.1007/978-3-030-78713-4_11, pp.195–214 | **Problem:** anomaly *diagnosis* (which anomaly, not just that one exists) with few labels | **Component:** compute nodes | **Data:** Sandia production LDMS telemetry | **Method:** semi-supervised representation learning + classification | production data: **yes** | **L3→L5** | **D2–D3** | **P4** | **SC-REGULAR-PRECEDENT** ★★
- **Scalability of Streaming Anomaly Detection in an Unbounded Key Space Using Migrating Threads** _9 — streaming AD at architecture level — **SC-REGULAR-POTENTIAL**
- **Artemis: Automatic Runtime Tuning of Parallel Execution Parameters Using Machine Learning** _24; **Analytic Modeling of Idle Waves in Parallel Programs: Communication, Cluster Topology, and Noise Impact** _19 (**noise/variability theory — P4**); **Ubiquitous Performance Analysis** _23; **Optimizing GPU-Enhanced HPC System and Cloud Procurements for Scientific Workloads** _17 (procurement from workload data — **P0/P2**, unusual and operationally useful); **Characterizing Containerized HPC Applications Performance at Petascale** _22

### ISC 2022 (15 research papers — ToC verified from Springer)
- **NVIDIA's Quantum InfiniBand Network Congestion Control Technology and Its Impact on Application Performance** — vendor+center congestion study — **L2/L7** — **SC-REGULAR-RELEVANT**
- **Understanding Distributed Deep Learning Performance by Correlating HPC and Machine Learning Measurements** — cross-layer telemetry correlation — **L2/L5** — **SC-REGULAR-RELEVANT**
- **Rapid Execution Time Estimation for Heterogeneous Memory Systems Through Differential Tracing**; **MAPredict: Static Analysis Driven Memory Access Prediction Framework for Modern CPUs**; **Comparative Evaluation of Call Graph Generation by Profiling Tools**; **"Hey CAI" — Conversational AI Enabled User Interface for HPC Tools**; **A Motivating Case Study on Code Variant Selection by Reinforcement Learning** — **SC-REGULAR-POTENTIAL**
- `[WORKSHOPS VOLUME 978-3-031-23220-6]`: **Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems** _18 (**the only thermal-anomaly paper in this entire census**); **Data Center Facility Monitoring with Physics Aware Approach** _17; **Detecting Interference Between Applications and Improving the Scheduling Using Malleable Application Proxies** _9; **Precise Energy Consumption Measurements of Heterogeneous Artificial Intelligence Workloads** _8

### ISC 2023 (20 research papers)
- **Analyzing Resource Utilization in an HPC System: A Case Study of NERSC's Perlmutter** | 10.1007/978-3-031-32041-5_16 | center-scale utilization characterization on a flagship GPU system | **L2** | **D2** | **P2** | **SC-REGULAR-PRECEDENT** — *the direct ISC-track precedent for a "한강 utilization census" paper* `[authors not fetched]`
- **Illuminating the I/O Optimization Path of Scientific Applications** _2 — **L5** — **SC-REGULAR-RELEVANT**
- **SAI: AI-Enabled Speech Assistant Interface for Science Gateways in HPC** _21 — user-facing AI on HPC — **PERIPHERAL**
- **Ready for the Frontier: Preparing Applications for the World's First Exascale System** _10 — **P0/P2**
- `[WORKSHOPS VOLUME 978-3-031-40843-4]`: **Analyzing Parallel Applications for Unnecessary I/O Semantics that Inhibit File System Performance** _13; **Performance Losses with Virtualization** _9

### ISC 2024 workshops (978-3-031-73716-9) — main volume unverified
- **Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository** _20 — on-topic, **workshop**, **PRACTICE-ONLY**
- **Introducing the Metric Proxy for Holistic I/O Measurements** _15; **An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads** _19; **Impact of Computational Load Balance and Power Capping on Energy Efficiency in HPC Centers** _26; **FLOTO: Beyond Bandwidth — A Framework for Adaptable, Multi-sensor Data Collection** _30; **Augmentation of MPI Traces Using Selective Instrumentation** _3

---

## 5. ACSOS — and the answer to your specific question about it

**Verdict: ACSOS 2020–2025 is NOT an HPC venue and its self-healing/autonomic lineage does not connect to supercomputer operations.** Every main-track paper I found evaluates on cloud microservices, serverless, Kubernetes, CPS, robotics, IoT, or simulation. I found **zero** main-track papers evaluated on a supercomputer, a batch scheduler, or a parallel file system across all six editions. Use ACSOS for *conceptual framing* (MAPE-K, self-adaptation, uncertainty, causal RCA), never as evidence of HPC applicability.

**Main-track items worth citing conceptually:**
- **2020** (acsos49614.2020.*): ENSURE .00020 (serverless autonomous RM); PRESTO .00021 (latency-aware power capping, cloud-native); Self-Patch .00022; Hierarchical Scaling of Microservices in Kubernetes .00023; Automated Management of Collections of Autonomic Systems .00029; Taming Resource Heterogeneity In Distributed ML Training With Dynamic Batching .00041; **A Survey of Methodology in Self-Adaptive Systems Research** .00039; Understanding Uncertainty in Self-adaptive Systems .00047
- **2021** (acsos52086.2021.*): **Causal Inference Techniques for Microservice Performance Diagnosis: Evaluation and Guiding Recommendations** | Li Wu, Johan Tordsson, Erik Elmroth, Odej Kao | .00029 — **best generic-RCA methodology citation in ACSOS; L5, cloud, P4**; **Empirical Characterization of User Reports about Cloud Failures** .00039 (**P2**); Towards Highly Automated ML-Empowered Monitoring of Motor Test Stands .00031; LOS: Local-Optimistic Scheduling … Anomaly Detection on Sensor Data Streams .00033; FaaSRank .00023; A Meta Reinforcement Learning-based Approach for Self-Adaptive System .00024; Architecture-based Evaluation of Scaling Policies for Cloud Applications .00035. *Companion only:* **Data Separation Scheme on Lustre Metadata Server based on Multi-stream SSD** (acsos-c52956.2021.00026) — the sole HPC-storage item, and it is a companion paper.
- **2022** (acsos55765.2022.*): **On Evaluating Self-Adaptive and Self-Healing Systems using Chaos Engineering** .00018 (self-healing evaluation methodology — **useful for D3/D4 experimental design**); SHIL: Self-Supervised Hybrid Learning for Security Attack Detection in Containerized Applications .00022; Reducing the Tail Latency of Microservices Applications via Optimal Configuration Tuning .00029; Explaining Online Reinforcement Learning Decisions of Self-Adaptive Systems .00023; A Systematic Review of Fault Tolerance Techniques for Adaptive and Context-Aware Systems .00020. *Companion:* **Performance Variability and Causality in Complex Systems** (acsosc56246.2022.00021); **A Heuristic for an Online Applicability of Anomaly Detection Techniques** (.00042)
- **2023** (acsos58161.2023.*): **Prolego: Time-Series Analysis for Predicting Failures in Complex Systems** .00025 — **the one ACSOS failure-prediction paper; L4, generic complex systems** — worth citing; Prediction-driven resource provisioning for serverless container runtimes .00033; μOpt .00024; Online ML Self-adaptation in Face of Traps .00023; Energy Efficient Scheduling for Serverless Systems .00020; Worst-Case Impact Assessment of Multi-Alarm Stealth Attacks Against Control Systems with CUSUM-Based Anomaly Detection .00029
- **2024** (acsos61780.2024.*): **ClearCausal: Cross Layer Causal Analysis for Automatic Microservice Performance Debugging** .00039 — **best 2024 RCA method, L5, cloud**; **CIRCE: a Scalable Methodology for Causal Explanations in Cyber-Physical Systems** .00026; Employing Software Diversity in Cloud Microservices to Engineer Reliable and Performant Systems .00030; Dynamic Storage Selection for Mitigating Tail Latency in Serverless Pipelines .00029; FairCIM .00025; Evaluating the Benefits of Model Retraining for Self-Aware Vehicle Traffic Forecasting .00022. *Companion:* Towards Interference-Resilient Multi-Tenant Microservices via Spatio-Temporal Models of Self-Configuration (acsos-c63493.2024.00054)
- **2025** (acsos66086.2025.*, ~13 technical papers): **Uncertainty-Driven Monitoring for ML-Based Autonomic Systems** .00021 (**monitoring policy driven by model uncertainty — the most transferable 2025 idea**); **Finding Relevant Causes in Complex Systems: a Generic Method Adaptable to Users and Contexts** .00026 (**L5**); Neuro-Symbolic Causal Reasoning for Cautious Self-Adaptation Under Distribution Shifts .00025; Antifragility via Online Learning and Monitoring: An IoT Case Study .00022; Coordinated Online RL for Self-Adaptive Systems Using Factored Q-Learning .00024
- **2026**: **NOT YET PUBLISHED**

---

## 6. DE FACTO HOME OF EACH SUB-TOPIC (within these five venues)

| Sub-topic | Home venue | Evidence |
|---|---|---|
| **Field reliability / failure characterization** | **IEEE Cluster main + IPDPS**, with HPDC as the prestige outlet | Ferreira Cluster'21 → HPDC'22; Das/Mueller IPDPS'20→'21; Lim/ORNL IPDPS'20. *(DSN and SC are the true heavyweights and sit outside this scope — note that in any positioning argument.)* |
| **Monitoring / ODA infrastructure** | **HPDC (Wintermute) + Cluster/HPCMASPA** | ODA framework papers get into HPDC main track only when they carry a novel analytics mechanism; pure infrastructure lands in HPCMASPA |
| **Anomaly detection & diagnosis on HPC telemetry** | **ISC research track + IEEE Cluster** — dominated by the **BU (Coskun) ↔ Sandia (Brandt/Schwaller/Leung/Aaziz)** axis | Proctor (ISC'21), ALBADross (Cluster'22) |
| **Log anomaly detection** | **IPDPS** (Dai/UNC-Charlotte + Zheng/Iowa State) | Drill IPDPS'23; ChatGPT-logs HPDC'23 short; Sequence-RTG (HPCMASPA'21) |
| **I/O performance diagnosis / RCA** | **HPDC + IPDPS**, jointly, around the **Darshan/DXT (LBNL: Byna, Bez)** ecosystem | AIIO HPDC'23; TunIO/Drilling-Down/Periodic-I/O IPDPS'24; IOAgent IPDPS'25 |
| **Performance variability & network congestion** | **IPDPS** (Bhatele line) with Cluster as secondary | IPDPS'20 Dragonfly → IPDPS'26 Elusive GPU performance; Cluster'20 congestion (Zhang/Coskun/NERSC), Cluster'22 Dragonfly+ |
| **Workload characterization from telemetry** | **IPDPS 2024–2026** — clearly the rising centre of gravity | Li/Tiwari IPDPS'24; Cross-System IPDPS'24; Cankur/Bhatele/NERSC IPDPS'26 |
| **Memory error prediction & mitigation** | **HPDC (BSC) + IPDPS (industry) + Cluster (Sandia/LANL)** | HPDC'24 RL-DRAM; IPDPS'25 UPH; Cluster'21 CE logging |
| **Queue-wait / runtime prediction** | **IEEE Cluster** (labs) and HPDC posters | Cluster'25 LANL queue-wait; HPDC'26 poster regime-aware profiles |
| **Intelligent / RL scheduling** | **IPDPS + Cluster**, roughly evenly | MRSch, SchedInspector, READYS, DRL-HPC, IPDPS'26 imitation learning |
| **Self-healing / autonomic** | **ACSOS — but for cloud only.** No HPC home exists in these five venues. | see §5 |
| **Thermal / cooling / facility** | **Nowhere in a main track.** Only Cluster/EE HPC SOP and ISC workshops. | ISC'22 workshop thermal anomaly; Cluster'20 EE HPC SOP items |
| **Telemetry sampling & reduction** | **IPDPS'21 Correlation-wise Smoothing, essentially alone** | — |
| **Distributed-training anomaly** | **Absent** until IPDPS'26 ResiHP-adjacent work; owned by MLSys/OSDI/NSDI | — |

---

## 7. THE 5–8 STRONGEST ARCHIVAL PRECEDENTS FOR "OPERATIONAL PROBLEM → GENERALIZABLE SYSTEMS RESEARCH"

Ranked. These are the papers to hold up as the target shape for an SC regular paper.

1. **Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field** — Boixaderas et al., HPDC 2024, 10.1145/3625549.3658686, pp.240–252. *Why:* a real center's real decision (offline the page? drain the node?) turned into a formal sequential-decision problem, learned from that center's own field data, evaluated on the operational cost function. This is the only paper in the census that plausibly reaches **L7/D5** with **P3–P4** research content.
2. **ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems** — Aksar et al., Cluster 2022, 10.1109/cluster51413.2022.00048, pp.369–380. *Why:* the operational obstacle (no labels, expensive expert time) *is* the research contribution. Maximum transferability to a center starting cold.
3. **Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems** — Aksar et al., ISC 2021, 10.1007/978-3-030-78713-4_11, pp.195–214. *Why:* moves from detection to *diagnosis* (naming the fault class) on production telemetry, with a semi-supervised formulation that survives label scarcity.
4. **Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data** — Netti, Tafani, Ott, Schulz, IPDPS 2021, 10.1109/ipdps49936.2021.00010, pp.2–12. *Why:* takes the most mundane operational complaint (too much telemetry) and produces a general, cheap, evaluable reduction method. Highest ratio of practical value to research effort.
5. **The Case of Performance Variability on Dragonfly-based Systems** — Bhatele et al., IPDPS 2020, .00096, pp.896–905 → **The Case of the Elusive Application Performance on Production GPU Supercomputers** — Wei, Pradeep, Bhatele, IPDPS 2026, .00079, pp.913–927. *Why (as a pair):* demonstrates how to keep publishing top-tier from the same operational question across an architecture generation — attribution of variability using only what the center already collects.
6. **Aarohi: Making Real-Time Node Failure Prediction Feasible** — Das, Mueller, Rountree, IPDPS 2020, .00115, pp.1092–1101. *Why:* reframes a saturated topic (failure prediction accuracy) around a constraint that only an operator would notice (inference must complete inside the lead time). Textbook example of operations generating a new research axis.
7. **Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining** — Li, Samsi, Gadepally, Tiwari, IPDPS 2024, .00037, pp.337–349. *Why:* optimizes for operator-actionability (interpretable rules) rather than F1, which is the actual D3→D4 barrier.
8. **AIIO: Using AI for Job-Level and Automatic I/O Performance Bottleneck Diagnosis** — Dong, Bez, Byna, HPDC 2023, 10.1145/3588195.3592986, pp.155–167. *Why:* clean per-job L5 built entirely on telemetry a center already has (Darshan), with an obvious path to a user-facing service.

*Honourable mention for a different reason:* **Monitoring Large Scale Supercomputers: A Case Study with the Lassen Supercomputer** — Patki et al., Cluster 2021, .00057, pp.468–480 — proof that a rigorous, honest **P0/P2, D5** center experience paper can hold a main-track slot at Cluster. Useful as the *first* paper of a program, not the SC target.

---

## 8. LINEAGE OBSERVATIONS

**Workshop → conference → production, documented:**
- **LRZ/TUM (Netti, Ott, Schulz):** DCDB tooling and ODA framing developed in workshop venues → **HPDC'20 Wintermute** (framework, main track) → **IPDPS'21 Correlation-wise Smoothing** (a general method extracted from the framework) → the definitional **"A Conceptual Framework for HPC Operational Data Analytics"** (HPCMASPA, Cluster'21 .00086). This is the cleanest *practice → framework → method → taxonomy* arc in the field, and DCDB runs at LRZ. **Model this arc.**
- **BU + Sandia (Coskun, Brandt, Schwaller, Leung, Aaziz; students Ates, Zhang, Aksar, Sencan):** LDMS production telemetry (Sandia operations) → **ISC'21 Proctor** → **Cluster'22 ALBADross**, with parallel congestion work at **Cluster'20** (Zhang/Groves/Cook/Wright/Coskun, NERSC). A single production telemetry asset sustaining a decade of archival papers across three venues. **The strongest argument that owning telemetry is a research asset, not just an ops burden.**
- **UNC-Charlotte + LBNL (Dai, Egersdoerfer, Bez, Byna):** **IPDPS'23 Drill** (log AD via source analysis) → **HPDC'23 short: ChatGPT for log-based AD on PFS logs** (exploratory) → **IPDPS'25 IOAgent** (LLM agent with trust guarantees, full paper). A textbook short-paper→full-paper escalation on the LLM axis in **two years**.
- **Sandia memory reliability (Ferreira, Levy):** **Cluster'21 DRAM correctable error logging at scale** → **HPDC'22 Understanding Memory Failures on a Petascale Arm System**. Same instrument, new architecture, venue upgrade.
- **NCSU + LLNL (Das, Mueller, Rountree):** **IPDPS'20 Aarohi** → **IPDPS'21 Systemic Assessment of Node Failures in HPC Production Platforms** — method paper followed by the field study that justifies it (note the *reverse* of the usual order).
- **UMD + NERSC (Bhatele, Cankur, with Austin & Kulkarni from NERSC):** **IPDPS'26 Characterizing Production GPU Workloads using System-wide Telemetry Data** — a center co-authoring with an academic group so the center's telemetry becomes a top-tier paper. **This is exactly the collaboration structure KISTI should replicate.**
- **BSC (Boixaderas, Radojković, Carpenter) with MareNostrum operations staff (Moré, Bartolome, Vicente as co-authors):** memory-error prediction work maturing into **HPDC'24** RL-based *mitigation in the field*. Note the operations staff on the author list — that is what makes the "in the field" claim credible. `[A: I believe there is a prior SC-track paper from this group on cost-aware UE prediction — verify before citing.]`
- **Emerging, not yet a lineage:** LLM-for-operations. **HPDC'23 (short) → IPDPS'25 IOAgent → IPDPS'26 KORAL (knowledge-graph-guided LLM for SSD operational analysis)**. Three data points in three years, from different groups. This is the fastest-moving open front.

---

## 9. CONSPICUOUS GAPS (ordered by how exploitable they look for an SC regular paper)

1. **Nothing closes the loop.** Across ~700 in-scope records, essentially one paper (HPDC'24 RL-DRAM) plausibly reaches **L7/D5**. Detection and prediction papers overwhelmingly stop at **D2 (offline production data)**. A paper that runs a predictor *in the operator workflow* and reports what the operators actually did with it (**D4**) would be nearly unprecedented in these venues.
2. **No multi-center studies, and no shared datasets or benchmarks.** Exactly one cross-system paper (IPDPS'24 .00069). There is no HPC-anomaly-detection benchmark comparable to what exists for cloud logs. HPDC'25's **DP-transformed HPC traces** (.3731573) is the only paper even addressing the *release* problem — a KISTI dataset-plus-benchmark contribution would be highly differentiating and is a natural pairing with a 한강 telemetry census.
3. **Thermal, cooling, and facility-side intelligence is absent from every main track.** The only items are ISC 2022 workshop (rule-based thermal anomaly detection, physics-aware facility monitoring) and Cluster EE HPC SOP 2020–2021. Given 한강's cooling/facility instrumentation, a *facility↔compute joint* anomaly or control paper has almost no incumbent competition in these venues.
4. **Telemetry sampling/reduction has one paper (IPDPS'21) and no follow-up in five years** — despite every center complaining about telemetry volume. Adaptive/uncertainty-driven sampling (cf. ACSOS'25 "Uncertainty-Driven Monitoring") applied to HPC telemetry is an open, well-motivated problem.
5. **GPU health and GPU failure prediction do not exist as a main-track topic.** 2024–2026 delivered GPU *characterization* (IPDPS'24 .00037, IPDPS'26 .00078) and GPU *reliability assessment* (Cluster'24 .00008), but no GPU-failure-prediction-at-scale paper. With large GPU partitions now standard, this is the most obvious unclaimed slot.
6. **Distributed-training anomaly detection is missing** from all five venues (IPDPS'26 ResiHP is failure *tolerance*, not detection). It has migrated to MLSys/OSDI/NSDI — but an HPC-center framing (shared multi-tenant supercomputer, not a dedicated AI cluster) is unoccupied here.
7. **No RCA that crosses layers from facility to application** in a main track. RCA work is siloed: I/O RCA (LBNL), log RCA (Dai), network attribution (Bhatele), and generic causal RCA sits in ACSOS on microservices. A cross-layer causal RCA on a real supercomputer would be novel *and* could import mature method from ACSOS'21 Wu et al. and ACSOS'24 ClearCausal.
8. **Almost no economic/operational-cost framing.** Papers report accuracy; almost none report node-hours saved, MTBF impact, or operator time. HPDC'24 and Cluster'25 queue-wait are the exceptions. Reviewers reward it and few supply it.
9. **The autonomic-computing lineage is severed from HPC.** ACSOS has the vocabulary (MAPE-K, self-healing, antifragility, uncertainty-driven monitoring) and none of the systems; HPDC/IPDPS/Cluster have the systems and none of the vocabulary. Explicitly bridging them — an ACSOS-grade self-adaptation formalism instantiated and evaluated on a national supercomputer — is a genuinely open position.

---

## 10. CAVEATS TO CARRY FORWARD

- **Not verified:** ISC research-paper proceedings for **2024, 2025, 2026**; IEEE **Cluster 2026**; the **latter half of HPDC 2026**'s volume (I enumerated ~50 of its records). ACSOS 2026 and Cluster 2026 are **NOT YET PUBLISHED** as far as any index I could reach shows.
- **Author lists** were individually verified for ~25 papers (marked with names above). Where no names appear, the record exists in Crossref but I did not fetch the author field — **retrieve before citing**, do not reconstruct from memory.
- **Several ACM HPDC titles arrive truncated in Crossref** (single-word: *Apollo:*, *Holmes*, *Capri*, *TAC*, *SchedInspector*, *Heterogeneous Systems Resilience*). These are real papers with real DOIs; the *titles as printed above are incomplete* and must be re-fetched from ACM DL.
- **No abstracts were readable** for any of these papers in this session. Every field beyond title/authors/venue/DOI/pages is my assessment from title, venue section, and author group, and is flagged `[A]` or `[UNVERIFIED]`. Treat evaluation-scale and production-deployment claims as hypotheses to confirm from the PDFs — especially for the eight papers in §7, which is where a fabricated "deployed in production" claim would do the most damage.agentId: ac04e1438d13b0b30 (use SendMessage with to: 'ac04e1438d13b0b30', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 299392
tool_uses: 196
duration_ms: 2832680</usage>
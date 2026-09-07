Search budget exhausted (200/200). Below are the notes from what I verified.

---

# ADVERSARIAL NOVELTY AUDIT — HPC AIOps, Axes D/E/F/G

**Scale codes used.** L0–L7 and D0–D5 as you defined. **P0–P4 was undefined in your brief** — I use it as a *production-evidence tier* and state the definition so you can remap: **P0** synthetic/simulation only · **P1** testbed / controlled injection · **P2** single production system, weeks · **P3** single production system, multi-month · **P4** multi-system and/or multi-year production.

**Verification discipline.** Items marked ✅ were fetched and read (abstract or full text). Items marked ⚠️ had title/venue/DOI confirmed via search result metadata but content not fetched. `UNVERIFIED` flags specific fields I could not confirm. **No citation below is fabricated**; where I was unsure of an author list I say so rather than guess.

---

# AXIS D — Performance degradation / slow-node diagnosis with *cause discrimination*

## D.1 Verified works

| # | Work | Yr | Venue | Type | ID | Problem / Method | Data & scale | Prod? | Deployed? | L | D | P |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 ✅ | **Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems** — Gunawi et al. | 2018 | FAST'18 + ACM TOS 14(3) | conf+journal | [10.1145/3242086](https://dl.acm.org/doi/10.1145/3242086), [USENIX](https://www.usenix.org/conference/fast18/presentation/gunawi) | Establishes fail-slow hardware as a first-class failure mode; taxonomy of root causes and symptoms | Incident reports from ~12 institutions (exact counts `UNVERIFIED` — commonly cited as 101 reports) | Yes | N/A (study) | L5 (taxonomy) | D1 | P4 |
| D2 ⚠️ | **Gray Failure: The Achilles' Heel of Cloud-Scale Systems** — Huang, Guo, Zhou, Lorch, Dang, Chintalapati, Yao (author list `UNVERIFIED`) | 2017 | HotOS'17 | workshop | [RG record](https://www.researchgate.net/publication/318575785_Gray_Failure_The_Achilles'_Heel_of_Cloud-Scale_Systems) | Concept of *differential observability*: system sees healthy, app sees degraded | Azure experience | Yes | N/A | L2/L5 concept | D0 | P4 (anecdotal) |
| D3 ⚠️ | **The Case for Limping-Hardware Tolerant Clouds** — Do, Gunawi | 2013 | HotCloud'13 | workshop | [PDF](https://ucare.cs.uchicago.edu/pdf/hotcloud13-limpingHw.pdf) | Position: degraded-but-alive hardware is under-addressed | — | Partly | No | L2 | D0 | P1 |
| D4 ⚠️ | **Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems** — Lu et al. | 2023 | FAST'23 | conf | [USENIX](https://www.usenix.org/conference/fast23/presentation/lu) | Per-drive latency-vs-load regression to spot fail-slow drives | Alibaba cloud storage fleet (details `UNVERIFIED`) | Yes | Yes | L3/L5 | D4 | P4 |
| D5 ✅ | **Understanding and Detecting Fail-Slow Hardware Failure Bugs in Cloud Systems** (Sieve) — Dong, Hua, Zhang, Chen, Chen | 2025 | USENIX ATC'25 | conf | [PDF](https://www.usenix.org/system/files/atc25-dong.pdf) | 48 real FSH bugs studied; fault-injection framework | ZooKeeper/Kafka/HDFS/HBase/MapReduce/Cassandra; 3–4 node Docker clusters | No | No | L3 (testing) | D1 | P0/P1 |
| D6 ✅ | **ARGUS: Production-Scale Tracing and Performance Diagnosis for over 10,000-GPU Clusters** — Zhou, Zeng, Chen, Lu, Yang, Ye, Ying, Zhang | 2026 | arXiv (venue not stated) | preprint | [2606.20374](https://arxiv.org/abs/2606.20374) | Always-on layered tracing (CPU stacks / framework semantics / GPU kernels), <2% overhead, 3700× kernel-event compression, **progressive diagnosis** | >10,000 GPUs, **6 months continuous** | Yes | Yes | **L5** | **D4** | **P3/P4** |
| D7 ✅ | **LLMPrism: Black-box Performance Diagnosis for Production LLM Training Platforms** — Jiang, Ren, Yu, Wu, Gu, Li, Huang, Feng, Yang, Yang, Lyu | 2025 | arXiv | preprint | [2505.00342](https://arxiv.org/abs/2505.00342) | Reconstruct per-job training timelines from **network flow data alone** (no instrumentation); infer parallelism strategy | "Platform-X" production, since Oct 2024; 0.3% timeline error | Yes | Yes | L5 | D4 | P3 |
| D8 ✅ | **Understanding Stragglers in Large Model Training Using What-if Analysis** — Lin, Jiang, Song, Zhao +11 | 2025 | arXiv (venue `UNVERIFIED`; Cornell systems seminar Feb 2026) | preprint | [2505.05713](https://arxiv.org/abs/2505.05713) | Counterfactual "what-if" simulation to quantify straggler impact; temporal/spatial distribution; candidate root causes | **5-month ByteDance LLM cluster trace** | Yes | Analysis | L5 | D2 | P3 |
| D9 ✅ | **FALCON: Pinpointing and Mitigating Stragglers for Large-Scale Hybrid-Parallel Training** — Wu, Wang, Yu, Yang, Wu, Duan, Yang, Wang, Qu, Zhang | 2024 | arXiv | preprint | [2410.12588](https://arxiv.org/abs/2410.12588) | Identify slow GPUs **and** slow comm links; multi-level mitigation, no human in loop | >10,000-GPU production cluster; >99% detection acc on human-labeled fail-slows; 60.1% slowdown reduction | Yes | Yes | **L7** | **D5** | P3 |
| D10 ✅ | **The Case of the Elusive Application Performance on Production GPU Supercomputers** — Wei, Pradeep, Bhatele | 2026 | IPDPS 2026 | conf | [PDF](https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf) | Longitudinal variability study; attributes among GPU HW, dragonfly placement, neighbor interference, congestion, collectives | **Perlmutter (1,792 GPU nodes) + Frontier (9,408 nodes)**, 4 months 2024–25, 761 runs / 8,118 node-hours | Yes | No (study) | L5 (semi-auto) | D2 | P3 |
| D11 ⚠️ | **The Case of Performance Variability on Dragonfly-based Systems** — (Bhatele/Lowenthal group; exact author list `UNVERIFIED`) | 2020 | IPDPS 2020 | conf | [IEEE 9139880](https://ieeexplore.ieee.org/document/9139880/) | Variability attribution on dragonfly | `UNVERIFIED` | Yes | No | L5 | D2 | P2 |
| D12 ✅ | **Quantifying the impact of network congestion on application performance and network metrics** — Zhang, Groves, Cook, Wright, Coskun | 2020 | IEEE Cluster 2020 | conf | [PDF](https://www.bu.edu/peaclab/files/2020/08/Cluster_CameraReady_Network_Congestion.pdf) | Controlled congestor injection on Aries; **ntile stall-to-flit ratio** as congestion metric | Cori (12k-node XC40), 64-node app + 64-node congestor, 8 apps | Yes | No | L3/L5 | D1 | P1 |
| D13 ⚠️ | **An In-Depth Analysis of the Slingshot Interconnect** — De Sensi et al. | 2020 | SC20 | conf | [arXiv 2008.08886](https://arxiv.org/abs/2008.08886) | First public characterization of Slingshot incl. congestion control | Cray/HPE testbeds | Partly | No | L0/L1 | D1 | P1 |
| D14 ✅ | **Live Forensics for HPC Systems: A Case Study on Distributed Storage Systems** (Kaleidoscope) — Jha, Cui, Banerjee, Xu, Enos, Showerman, Kalbarczyk, Iyer | 2020 | SC20 | conf | [NSF PAR](https://par.nsf.gov/servlets/purl/10293041) | PGM-based failure **localization** + LOF-based **diagnosis distinguishing reliability failure vs resource overload** | Blue Waters Cray Sonexion: 6 MDS, 420 OSS, 17,280 HDDs; 2 yrs data, 3 mo live; **843 operator-resolved ground-truth issues** | Yes | Yes (3 mo) | **L5** | **D4** | **P4** |
| D15 ✅ | **Effective Node-Level Anomaly Detection in HPC Systems via Coarse-Grained Clustering and Fine-Grained Model Sharing** (NodeSentry) — Xia, Sun, Pan, Yuan, Zhang, Hu, Tao, Li, Feng | 2025 | **SC'25** | conf | [10.1145/3712285.3759794](https://dl.acm.org/doi/full/10.1145/3712285.3759794) | Unsupervised per-node AD; HAC clustering of job patterns + Transformer-MoE | NG-Tianhe: D1 = 1,294 nodes / 13,379 jobs / 3,014 metrics / 1 week; D2 = 30 nodes / 8 days. Anomaly ratio 0.16% / 0.04% | Yes | No | **L3 only** | D2 | P2 |
| D16 ⚠️ | **Diagnosing Performance Variations in HPC Applications Using Machine Learning** — Tuncer, Ates et al. | 2017 | ISC 2017 | conf | [10.1007/978-3-319-58667-0_19](https://link.springer.com/chapter/10.1007/978-3-319-58667-0_19) | Supervised classification of *injected* anomaly type from node telemetry | Testbed + Volta | No (injected) | No | L5 | D1 | P1 |
| D17 ⚠️ | **Online Diagnosis of Performance Variation in HPC Systems Using Machine Learning** — Tuncer, Ates et al. | 2019 | IEEE TPDS | journal | [OSTI 1474092](https://www.osti.gov/biblio/1474092) | Online version of D16 | Same lineage | No | Partial | L5 | D2 | P1 |
| D18 ✅ | **E2EWatch: An End-to-End Anomaly Diagnosis Framework for Production HPC Systems** — Aksar et al. | 2021 (`UNVERIFIED` yr) | Euro-Par | conf | [PDF](https://www.bu.edu/peaclab/files/2021/06/E2EWatch_EuroPar_CR.pdf) | LGBM on 60s telemetry windows; classifies **memleak / membw / cpuoccupy / cachecopy / normal** | **Eclipse, 1,488 nodes** (Sandia) — but anomalies are **synthetically injected via HPAS** | Prod system, **synthetic anomalies** | No | L5 | D1 | **P1** |
| D19 ⚠️ | **Runtime Performance Anomaly Diagnosis in Production HPC Systems Using Active Learning** — Aksar et al. | 2024 | IEEE TPDS | journal | [10.1109/TPDS.2024.3365462](https://dl.acm.org/doi/abs/10.1109/TPDS.2024.3365462) | Active learning to cut labeling cost for anomaly *type* diagnosis | `UNVERIFIED` (403 on fetch) | `UNVERIFIED` | `UNVERIFIED` | L5 | D2 | P1/P2 |
| D20 ✅ | **Don't Predict, Prioritize: Rethinking GPU Reliability Assessment** (HeaRank) — Ma, Pei, Lu, Zhou, Wang, Zhu, Jiang, Pei, Li, Xie | 2026 | **KDD 2026** (accepted) | conf | [2607.15115](https://arxiv.org/abs/2607.15115) | Argues GPU failure *timing* is unpredictable (DBE, GPU-Lost are stochastic); replaces prediction with **learning-to-rank risk prioritization** | Production cluster, thousands of GPUs; AUC 0.83; 64% of failures in top-5% ranked nodes vs 21% incumbent | Yes | Yes | L4→L6 | D4 | P3 |
| D21 ✅ | **When GPUs Fail Quietly: Observability-Aware Early Warning Beyond Numeric Telemetry** — Bidollahkhani, Nordsiek, Kunkel | 2026 | arXiv | preprint | [2603.28781](https://arxiv.org/html/2603.28781v2) | "Detachment-class" GPU failures have no numeric precursor; uses **monitoring-pipeline degradation** (scrape latency, sample loss, metric-family disappearance) as signal | **GWDG production, 7 nodes / 28 GPUs, ~353 days** (Feb'25–Jan'26); 69 incidents catalogued, 7 detachment; Slurm + NHC correlation; **Zenodo dataset released** | Yes | Prototype | L3/L4 | D2 | P3 |
| D22 ✅ | **Enhancing Performance Insight at Scale: A Heterogeneous Framework for Exascale Diagnostics** — Grbic (Rice) | 2025/26 | ICS (`UNVERIFIED`) | preprint | [2605.03561](https://arxiv.org/abs/2605.03561) | GPU-accelerated query over HPCToolkit traces; localizes GPU load imbalance + **Slingshot congestion across 22 racks** | Frontier (16 ranks), **Aurora 100,000 ranks / 1,000 nodes** | Yes | Open source | L1/L5 | D2 | P1 |

## D.2 Strongest existing method

**ARGUS (D6)** for GPU-cluster fail-slow, and **Kaleidoscope (D14)** for HPC storage.

- **ARGUS does:** always-on hierarchical tracing at <2% overhead on >10k GPUs for 6 months, with progressive multi-level isolation that *names* the cause class — compute straggler, **link degradation**, pipeline-bubble amplification, FlashAttention JIT stall, communication-masked compute straggler. This is genuine, deployed, multi-cause discrimination.
- **ARGUS does NOT do:** anything for a general multi-tenant HPC batch workload. It assumes a *synchronous, iterative, homogeneous* training job as its reference model — the periodicity is what makes "compare rank i to rank j at iteration k" work. It has no notion of Slurm-scheduled heterogeneous MPI jobs, no CPU-only jobs, no Lustre, no cooling/power, no cross-job interference attribution, no topology/placement cause class.
- **Kaleidoscope does:** 99.3% localization of 843 real operator-confirmed storage issues on Blue Waters, and discriminates **exactly two** cause classes (reliability failure vs resource overload) at 95.8%.
- **Kaleidoscope does NOT do:** compute nodes, GPUs, fabric, or interference; it is storage-path-specific and needs curated regex libraries.

## D.3 Closest production implementation operators actually run

**Frontier `checknode` (Ezell, CUG 2023)** — [PDF](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap151s2-file1.pdf). This is the honest baseline. Across 685 blades / ~60M components with MTBF in *hours*: deterministic threshold checks at boot and in every Slurm job epilog; auto-drain with the error string as the reason; auto-resume only if `checknode` itself set the reason. **Zero ML. Zero cause discrimination beyond "which check failed."** Root cause is a human hardware engineer opening a ticket. Everything else in the table is research; this is what runs.

Second: **LBNL Node Health Check (NHC)** — the de-facto community tool, same character.

## D.4 Remaining difference (concrete, testable)

No verified work does **multi-cause discrimination across GPU / CPU / network / I/O / topology / interference for a general multi-tenant HPC batch workload on production telemetry with operator-confirmed labels.** Every existing work drops at least one of those:

| Requirement | ARGUS | Kaleidoscope | NodeSentry | E2EWatch | IPDPS'26 |
|---|---|---|---|---|---|
| Production HPC batch (not LLM training) | ✗ | ✓ | ✓ | ✓ | ✓ |
| ≥4 cause classes discriminated | ✓ | ✗ (2) | ✗ (0) | ✓ (4, CPU/mem only) | partial |
| GPU + network + I/O all in scope | ✓ | ✗ | ✗ | ✗ | ✓ |
| Real (not injected) anomalies | ✓ | ✓ | ✓ | **✗** | ✓ |
| Deployed / online | ✓ | ✓ | ✗ | ✗ | ✗ |
| Multi-month trace | ✓ | ✓ | **✗ (1 week)** | ✗ | ✓ (4 mo) |

**The testable gap:** a discriminator that, given a job whose runtime is anomalous relative to its own history, outputs a ranked cause attribution over {GPU degradation, CPU freq/thermal throttle, NIC/link degradation, fabric congestion from neighbors, Lustre contention, placement/topology, application-intrinsic}, evaluated against operator-confirmed ground truth on a production Tier-0 machine over ≥6 months.

## D.5 Verdict: **STILL_OPEN — but narrowly, and closing fast**

Detection alone is **CLOSED** (NodeSentry, Prodigy, RUAD). Cause discrimination in *LLM-training* clusters is **CLOSED to PARTIALLY_ADDRESSED** (ARGUS, FALCON, LLMPrism — all 2024-26, all production, all >10k GPU). Cause discrimination for *general multi-tenant HPC* is **STILL_OPEN**, with two caveats: (a) IPDPS 2026 (D10) already did the measurement study on Perlmutter+Frontier and found *network congestion dominates, GPU HW is stable* — that finding pre-empts a naive "GPUs are the problem" framing; (b) the SC'25 NodeSentry paper shows the SC PC will accept detection-only work from a national center, which lowers the bar but also means a detection-only submission is now derivative.

## D.6 SC Technical Paper viability (D)

**Reviewer will demand:**
- ≥1 production system, ≥1,000 nodes, **≥6 months** of telemetry (SC'25 accepted 1 week; a 2027 paper competing with ARGUS's 6 months will not survive at 1 week).
- **Real, operator-confirmed labels** — not HPAS injection. This is the single sharpest discriminator vs the BU/Sandia lineage. Injection-only evaluation is now a rejection risk given D6/D9/D14 all have real labels.
- Baselines: NodeSentry (SC'25), Prodigy (SC'23), RUAD, E2EWatch/ALBADross, plus at least one cloud fail-slow baseline (Perseus or FALCON) — reviewers from outside HPC will ask.
- Metrics: per-cause-class precision/recall (not just aggregate F1), top-k localization accuracy, **lead time**, false-drain rate, and detection latency. Report under a fixed alert budget (as D21 does) — reviewers now know point-adjusted F1 is inflated (see Axis E).
- An ablation showing which telemetry channel carries which cause signal.

**Strongest counterargument against novelty:** *"ARGUS (2026) already does always-on multi-cause fail-slow diagnosis at 10,000-GPU production scale with six months of deployment, and Kaleidoscope (SC'20) already did PGM-based cause discrimination on a production HPC system with 843 real labels. What is new here besides the machine being a Korean one?"* — You must answer this with a **cause taxonomy that ARGUS structurally cannot produce** (cross-job interference, topology/placement, Lustre, cooling/power) and an evaluation on **heterogeneous batch jobs** where ARGUS's iteration-periodicity assumption fails.

## D.7 Testability with center telemetry

Fully testable at a large center. Mapping: GPU cause → DCGM (SM clocks, `DCGM_FI_DEV_*_THROTTLE`, ECC, XID, power); CPU cause → per-core freq/temp/RAPL, `perf` counters, thermal throttle flags; network cause → **Slingshot fabric counters** (per-port stall/flit, congestion-control state, link retrains, degraded-lane events) — note D12 established stall-to-flit ratio as the workhorse metric on Aries and the Slingshot analogue is the obvious port; I/O cause → Lustre `llite`/OST stats + Darshan; topology/placement → Slurm `hostlist` → dragonfly group mapping; interference → concurrent-job map from Slurm accounting joined on shared switch/OST; environmental → CDU inlet temp, rack power. **Labels** come from the RAS/syslog + ticket + maintenance-record join (see Axis E) — that join is itself a contribution.

---

# AXIS E — Label-scarce operational learning

## E.1 Verified works

| # | Work | Yr | Venue | Type | ID | Contribution | Scale | L | D | P |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 ✅ | **M100 ExaData: a data collection campaign on CINECA's Marconi100** — Borghesi et al. | 2023 | Scientific Data | journal | [10.1038/s41597-023-02174-3](https://www.nature.com/articles/s41597-023-02174-3) | Largest public HPC telemetry release: **573 metrics, 980+ nodes, 934 days (Mar'20–Sep'22), 49.9 TB**; node internals + cooling + power + job data + **system alerts**. Weak labels via **Nagios offline-state**; paper's own classifier reaches only **AUC 0.57** on them | Tier-0 | L0 | D2 | P4 |
| E2 ⚠️ | **RUAD: Unsupervised anomaly detection in HPC systems** — Molan, Borghesi, Cesarini, Benini, Bartolini (`UNVERIFIED` list) | 2023 | Future Gener. Comput. Syst. 141 | journal | [10.1016/j.future.2022.12.001](https://dl.acm.org/doi/10.1016/j.future.2022.12.001) | Recurrent unsupervised AD on M100; explicitly motivated by label absence | M100 | L3 | D2 | P3 |
| E3 ⚠️ | **A semisupervised autoencoder-based approach for anomaly detection in HPC systems** — Borghesi et al. | 2019 | Eng. Appl. of AI | journal | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0952197619301721) | Train on normal-only; the canonical HPC semi-supervised baseline | D.A.V.I.D.E. / Eurora (`UNVERIFIED`) | L3 | D2 | P2 |
| E4 ✅ | **Prodigy: Toward Unsupervised Anomaly Detection in Production HPC Systems** — Aksar, Sencan, Schwaller, Aaziz, Leung, Brandt, Kulis, Egele, Coskun | 2023 | **SC'23** | conf | [10.1145/3581784.3607076](https://dl.acm.org/doi/10.1145/3581784.3607076) | VAE, no labeled training samples; job+node level with explanations; 0.95 F1 controlled, **88% on a real production system** | Sandia | L3 | D3 | P2 |
| E5 ✅ | **Fresco: A Public Multi-Institutional Dataset for Understanding HPC System Behavior and Dependability** — McKerracher, Mukherjee, Kalyanam, Bagchi | 2025 | PEARC'25 | conf | [10.1145/3708035.3736090](https://dl.acm.org/doi/10.1145/3708035.3736090) | Purdue Anvil + Conte + TACC Stampede; **20.9M jobs, 75 months (2013–2023)**; job accounting + CPU/GPU/mem/NFS/block-IO; **labels = Slurm exit-code taxonomy only** | 3 systems | L0 | D2 | P4 |
| E6 ✅ | **When GPUs Fail Quietly** — Bidollahkhani, Nordsiek, Kunkel (see D21) | 2026 | arXiv [2603.28781](https://arxiv.org/html/2603.28781v2) | preprint | — | **Operator-curated incident catalog** built from Slurm + Node Health Check + ~353 days GWDG telemetry; sanitized dataset on Zenodo. Explicit about labels being **day-level and coarse** | 28 GPUs | L0/L3 | D2 | P3 |
| E7 ⚠️ | **Towards a Rigorous Evaluation of Time-series Anomaly Detection** — Kim, Choi, Jang, Yoon (`UNVERIFIED` list) | 2022 | **AAAI 2022** | conf | [arXiv 2109.05257](https://arxiv.org/abs/2109.05257), [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/20680) | **The killer paper.** Shows the *point-adjustment* protocol used by essentially all deep TSAD papers inflates F1 so severely that a **random-score detector beats SOTA** | — | — | — | — |
| E8 ⚠️ | **Multivariate Time Series Anomaly Detection: Fancy Algorithms and Flawed Evaluation Methodology** (authors `UNVERIFIED`) | 2024 | Springer vol. | chapter | [10.1007/978-3-031-68031-1_1](https://link.springer.com/chapter/10.1007/978-3-031-68031-1_1) | Same critique, independent | — | — | — | — |
| E9 ⚠️ | **Did We Actually Fix It? An Independent Adversarial Stress-Test of Post-Point-Adjustment Evaluation Metrics for TSAD** | 2026 | arXiv | preprint | [2607.11969](https://arxiv.org/abs/2607.11969) | Stress-tests the *replacement* metrics proposed after E7 — content `UNVERIFIED` | — | — | — | — |
| E10 ⚠️ | **Navigating the metric maze: a taxonomy of evaluation metrics for anomaly detection in time series** | 2023/24 | Data Min. Knowl. Discov. | journal | [10.1007/s10618-023-00988-8](https://link.springer.com/article/10.1007/s10618-023-00988-8) | Metric taxonomy | — | — | — | — |
| E11 ⚠️ | **Log-based Anomaly Detection with Deep Learning: How Far Are We?** — Le, Zhang | 2022 | **ICSE 2022** | conf | [arXiv 2202.04301](https://arxiv.org/pdf/2202.04301) | Deep log AD collapses under realistic (non-shuffled, label-noisy) settings | HDFS, BGL, etc. | — | — | — |
| E12 ⚠️ | **A comprehensive study of machine learning techniques for log-based anomaly detection** | 2025 | Empir. Softw. Eng. | journal | [arXiv 2307.16714](https://arxiv.org/html/2307.16714v3) | Classical ML often matches DL | Loghub | — | — | — |
| E13 ⚠️ | **Impact of log parsing on deep learning-based anomaly detection** | 2024 | Empir. Softw. Eng. | journal | [10.1007/s10664-024-10533-w](https://link.springer.com/article/10.1007/s10664-024-10533-w) | Parser choice dominates model choice | — | — | — | — |
| E14 ⚠️ | **Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics** — He et al. (venue `UNVERIFIED`, commonly cited as ISSRE 2023) | 2023 | — | conf | [RG](https://www.researchgate.net/publication/375267895_Loghub_A_Large_Collection_of_System_Log_Datasets_for_AI-driven_Log_Analytics) | The standard log corpus, **includes BGL/Thunderbird/Spirit HPC RAS logs** | — | L0 | — | P4 |
| E15 ✅ | **Literature study on Operational Data Analytics frameworks in large-scale computing infrastructures** — Suman, Chu, Iosup | 2026 | arXiv | preprint | [2603.19016](https://arxiv.org/html/2603.19016) | Surveys 10 production ODA frameworks (OMNI/NERSC, DCDB Wintermute/LRZ, ExaMon/CINECA, Fugaku, Theta/ANL, Summit/OLCF, Kaleidoscope/NCSA, Apollo, AutoDiagn, IBM EAS). Finds **no LLM integration in any surveyed framework**; closed-loop "partially manual"; RCA not a standardized capability | 10 centers | L0–L4 | D3 | P4 |
| E16 ⚠️ | **HPC ODA Commons: Community-Governed Contracts and Toolkit for Reproducible Operational Data Analytics** (authors `UNVERIFIED`) | 2026 | PEARC'26 | conf | [10.1145/3785462.3815891](https://doi.org/10.1145/3785462.3815891) | Data contracts / reproducibility for ODA — direct competitor if you plan a dataset paper | — | L0 | — | — |
| E17 ⚠️ | **DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems** — Netti et al. | 2020 | HPDC'20 | conf | [10.1145/3369583.3392674](https://dl.acm.org/doi/abs/10.1145/3369583.3392674), [arXiv 1910.06156](https://arxiv.org/abs/1910.06156) | Production online ODA at LRZ; HPC-ODA companion dataset | LRZ | L0–L3 | D4 | P3 |
| E18 ⚠️ | **Rethinking Weak Supervision in Anomaly Detection: A Comprehensive Benchmark** | 2026 | arXiv | preprint | [2605.26068](https://arxiv.org/html/2605.26068v3) | Weak-supervision AD benchmark — content `UNVERIFIED`, **not HPC** | — | — | — | — |
| E19 ⚠️ | **Weak Supervision: A Survey on Predictive Maintenance** — Martínez-Heredia et al. | 2025 | WIREs DMKD | journal | [10.1002/widm.70022](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/widm.70022) | Weak supervision for PdM — adjacent domain, **not HPC** | — | — | — | — |
| E20 ⚠️ | **Seeing the Needle in the Haystack: Towards Weakly-Supervised Log Instance Anomaly Localization via Counterfactual Perturbation** | 2026 | arXiv | preprint | [2605.10988](https://arxiv.org/html/2605.10988) | Weak labels at sequence level → instance-level localization. Content `UNVERIFIED` | — | — | — | — |
| E21 ✅ | **What Artificial Intelligence can do for High-Performance Computing systems?** — Pochelu, Cartiaux, Schleich | 2025/26 | arXiv | survey | [2602.00014](https://arxiv.org/html/2602.00014) | ~1,800 papers screened → 74 on "AI for HPC". States: *"AI models are trained using proprietary data or simulators, limiting reproducibility"*; *"lack of standardized data sources"*; *"providing explainable anomaly scores and actionable diagnostics remains an open problem"* | — | — | — | — |

## E.2 Strongest existing method

There is no single "method"; the strongest *position* is **E1 (M100 ExaData) + E2 (RUAD)** as a pair: release 2.5 years of Tier-0 telemetry, derive weak labels from the operational alerting system (Nagios offline-state), and admit that a classifier on those labels reaches only **AUC 0.57**. That AUC number is the most useful single fact in this axis — it is a published, citable admission that operational-state weak labels are *nearly uninformative* as-is.

- **Does:** proves a national center can release multi-year telemetry with weak operational labels; establishes unsupervised/semi-supervised HPC AD baselines.
- **Does NOT:** build a *principled* label model. Nagios-offline is used as a single noisy oracle with no denoising, no source fusion, no confidence, no separation of "drained for maintenance" vs "drained for fault" vs "drained by mistake." No use of tickets, RAS, or maintenance records as complementary weak sources. No labeling-function framework.

## E.3 Closest production implementation

Nothing. Centers run **Nagios / Zabbix / Prometheus alerting + Slurm drain reasons + a ticket system (RT/ServiceNow)** as four *disconnected* sources. Frontier's `checknode` (D.3) writes its failing-check name into the Slurm drain reason — that string is, in practice, the closest thing to a production label pipeline anywhere, and nobody has published it as a labeling method.

## E.4 Remaining difference (concrete, testable)

**A principled multi-source weak-label model for HPC operations, plus a label-free evaluation protocol that survives the E7 critique.** Specifically:

1. **Labeling functions over heterogeneous operational sources** — Slurm drain reason strings, RAS/syslog error classes, DCGM XID codes, ticket resolution categories, maintenance/RMA records, job exit codes — combined with an explicit noise model (agreement/disagreement structure, source-specific precision), rather than one oracle.
2. **Denoising:** separate *planned* from *unplanned* node-state transitions; RMA record as delayed high-precision label to bootstrap precision estimates for the noisier sources.
3. **Evaluation without clean labels:** report under a fixed alert budget (ops-realistic), report **time-to-detect relative to the ticket timestamp** and **fraction of tickets preceded by an alert**, and *explicitly refuse* point-adjusted F1. Add an operator-adjudicated sample with inter-rater agreement.

Nobody in E has done 1+2+3 together on an HPC system. E6 gets closest (operator-curated catalog + fixed 1% alert budget + honest lead-time reporting) but at **28 GPUs**.

## E.5 Verdict: **STILL_OPEN** for the label-model contribution; **CLOSED** for "yet another unsupervised HPC AD model."

Sub-verdicts:
- "Unsupervised AD for HPC nodes" → **CLOSED** (E2, E3, E4, D15). Do not do this.
- "Public HPC telemetry dataset" → **PARTIALLY_ADDRESSED / TOO_SITE_SPECIFIC risk.** M100 (2.5 yr, 49.9 TB) and Fresco (20.9M jobs, 75 mo, 3 systems) exist and PEARC'26 is standardizing contracts (E16). A Korean dataset release alone is **not** an SC Technical Paper — it's a PEARC/dataset-track paper.
- "Principled weak-label model + label-free eval protocol for HPC ops" → **STILL_OPEN.** This is the most defensible thing in Axis E.

## E.6 SC Technical Paper viability (E)

**Reviewer will demand:** ≥1 year of telemetry; the label-source join described end-to-end and released or at least fully specified; a held-out **operator-adjudicated** gold set with inter-rater agreement; comparison of your weak-label model against (a) single-source Nagios/drain-reason labels (i.e., reproduce M100's AUC 0.57 setting and beat it), (b) fully unsupervised (Prodigy, RUAD), (c) fully supervised on the small gold set; and explicit reporting under both point-adjusted and non-point-adjusted metrics with a discussion citing E7.

**Strongest counterargument:** *"Weak supervision is a solved ML technique (Snorkel-style); applying it to HPC labels is engineering, and the evaluation critique (Kim et al. AAAI'22) is not yours."* — Defense must be that the *structure* of HPC operational labels is materially different (delayed RMA ground truth, planned-vs-unplanned confound, cause-class labels not just binary, per-node vs per-job label granularity mismatch) and that you produce a **reusable protocol + released gold set**, not just an application.

**Note this is also the natural companion contribution to Axis D** — the label pipeline is what makes a D paper's "real operator-confirmed labels" claim credible. A combined D+E paper is stronger than either alone.

## E.7 Testability

Directly testable: Slurm `sacct`/`sreport` (exit codes, drain reasons, node state history), syslog/RAS, DCGM XID + ECC, ticket system export, maintenance/RMA log, plus the D-axis telemetry. The binding join key is (node, time-window). The hard part is the ticket system export and RMA records — those require center administrative buy-in, which is exactly the asset a national center has and academics do not.

---

# AXIS F — Safe automated remediation

## F.1 Verified works

| # | Work | Yr | Venue | Type | ID | Contribution | Scale | Prod? | L | D | P |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 ✅ | **Predictive and Adaptive Failure Mitigation to Avert Production Cloud VM Interruptions** (**Narya**) — Levy, Yao, Wu, Dang, Huang, Mu, Zhao, Ramani, Govindaraju, Li, Lin, Shafriri, Chintalapati | 2020 | **OSDI'20** | conf | [USENIX](https://www.usenix.org/conference/osdi20/presentation/levy) | **The bar.** Predicts host failure from multi-layer signals, then chooses mitigation via **online experimentation / bandit + RL feedback** rather than a static policy. **15 months in Azure production, 26% reduction in VM interruptions** | Azure fleet | Yes | **L7** | **D5** | **P4** |
| F2 ⚠️ | **Proactive Process-Level Live Migration in HPC Environments** — Wang, Mueller, Engelmann, Scott | 2008 | **SC'08** | conf | [ACM](https://dl.acm.org/doi/10.5555/1413370.1413414), [PDF](https://arcb.csc.ncsu.edu/~mueller/ftp/pub/mueller/papers/sc08.pdf) | Founding paper of the HPC proactive-migration lineage | Small cluster | No | L7 | D1 | P1 |
| F3 ⚠️ | **Proactive process-level live migration and back migration in HPC environments** — Wang et al. | 2012 | JPDC | journal | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0743731511002085) | Adds back-migration | — | No | L7 | D1 | P1 |
| F4 ✅ | **Orchestrating Fault Prediction with Live Migration and Checkpointing** — Behera, Wan, Mueller, Wolf, Klasky | 2020 | **HPDC'20** | conf | [10.1145/3369583.3392672](https://dl.acm.org/doi/abs/10.1145/3369583.3392672), [PDF](https://arcb.csc.ncsu.edu/~mueller/ftp/pub/mueller/papers/hpdc20.pdf) | Decision tree: if lead time sufficient → migrate to reserved healthy nodes, else → checkpoint; burst-buffer-accelerated. 20–86% overhead reduction, 29% fewer BB writes | **SimPy simulation** of Summit, Titan Weibull failure model, 6 real app traces, 1000 iterations | **No — simulation only; prediction accuracy assumed high without validation** | L7 | **D0/D1** | **P0** |
| F5 ✅ | **Frontier node health checking and state management** — Ezell (ORNL) | 2023 | **CUG 2023** | conf | [PDF](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap151s2-file1.pdf) | Real production closed loop: boot-time + per-job-epilog checks, **auto-drain**, **auto-resume gated on provenance of the drain reason** (only checknode's own reasons auto-clear — this is the de-facto safety mechanism), post-repair "node screen" verification | 685 blades, ~60M components, MTBF in hours | **Yes** | **L7** (rule-based) | **D5** | **P4** |
| F6 ⚠️ | **Unicron: Economizing Self-Healing LLM Training at Scale** — (Alibaba; author list `UNVERIFIED`) | 2024 | arXiv | preprint | [2401.00134](https://arxiv.org/abs/2401.00134) | In-band error detection + cost-aware reconfiguration plan for training recovery | Alibaba (`UNVERIFIED`) | Likely | L7 | D3/D4 | P2/P3 |
| F7 ✅ | **FALCON** (see D9) | 2024 | arXiv [2410.12588](https://arxiv.org/abs/2410.12588) | preprint | — | **Multi-level mitigation with no human intervention** on a >10k-GPU production cluster; 60.1% slowdown reduction. This is a real L7 closed loop for stragglers | >10k GPUs | Yes | **L7** | **D5** | P3 |
| F8 ✅ | **Don't Predict, Prioritize** (HeaRank, see D20) | 2026 | KDD'26 | conf | [2607.15115](https://arxiv.org/abs/2607.15115) | Reframes the *input* to remediation: rank risk, don't predict timing. 64%@top-5% vs 21% incumbent | 1000s GPUs | Yes | L4→L6 | D4 | P3 |
| F9 ⚠️ | **Safe Remediation as Risk-Constrained Intervention Decision in Microservice Systems** | 2026 | arXiv | preprint | [2607.20005](https://arxiv.org/html/2607.20005) | Frames remediation as risk-constrained intervention. **Content `UNVERIFIED`** (fetch rate-limited). Closest named "safe remediation" formulation I found — must be read before you claim novelty | `UNVERIFIED` | `UNVERIFIED` | L6/L7 | ? | ? |
| F10 ⚠️ | **Systemic Assessment of Node Failures in HPC Production Platforms** — (Mueller group; authors `UNVERIFIED`) | 2021 | IPDPS 2021 | conf | [PDF](https://arcb.csc.ncsu.edu/~mueller/ftp/pub/mueller/papers/ipdps21.pdf) | Production node-failure characterization feeding prediction | — | Yes | L4 | D2 | P3 |
| F11 ⚠️ | **Reducing False Node Failure Predictions in HPC** (venue `UNVERIFIED`, likely HiPC 2019) | 2019 | — | conf | [RG](https://www.researchgate.net/publication/339257965_Reducing_False_Node_Failure_Predictions_in_HPC) | Directly addresses the FP problem that blocks automated action | — | — | L4 | D1 | P2 |
| F12 ⚠️ | **Mantis: Decoding HPC Telemetry Data for Robust System Prediction** | 2026 | **ACM ICS 2026** | conf | [10.1145/3797905.3800527](https://dl.acm.org/doi/10.1145/3797905.3800527) | Content `UNVERIFIED` (403). Recent HPC telemetry→prediction work; must be read | — | — | L4 | ? | ? |
| F13 ⚠️ | **NØMAD: Lightweight HPC Monitoring and Diagnostics with ML-Based Failure Prediction** | — | J. Open Research Software | journal | [10.5334/jors.686](https://openresearchsoftware.metajnl.com/articles/10.5334/jors.686) | Released software | — | — | L4 | D2 | P2 |
| F14 ⚠️ | **Automated System Health and Performance Benchmarking Platform** | 2017 | HPCSYSPROS'17 | workshop | [10.1145/3155105.3155106](https://dl.acm.org/doi/10.1145/3155105.3155106) | Operational health benchmarking | — | Yes | L2 | D4 | P3 |
| F15 | **LBNL Node Health Check (NHC)** | — | — | software | community tool | Community-standard Slurm-integrated health check → drain | many centers | Yes | L7 (rule) | D5 | P4 |

## F.2 Strongest existing method

**Narya (F1).** It is the only verified system that closes the loop *with a learned, safety-aware action policy* validated in production at fleet scale.

- **Does:** predict imminent host failure; choose among mitigation actions (live migrate, soft reboot, mark unallocatable, etc.); **continually A/B-test actions online** so the policy adapts; 15 months production; 26% interruption reduction.
- **Does NOT:** apply to HPC. A cloud VM is migratable at will and the blast radius of a wrong action is one tenant. An HPC job is a gang-scheduled, tightly-coupled MPI/NCCL allocation where draining one node kills the whole job, and where "reserved healthy nodes" is a capacity cost the center pays continuously. Narya has no analogue for job-level blast radius, no scheduler coupling, no rollback of a *scheduling* decision, and no notion of a job's checkpoint state.

**Frontier checknode (F5)** is the strongest *HPC* closed loop and it is entirely rule-based. Its one genuine safety idea — **auto-resume only if checknode itself set the drain reason**, preserving human-set drains — is exactly the kind of provenance-gated automation an SC paper could generalize and formalize.

## F.3 Closest production implementation

`checknode` (ORNL Frontier) and LBNL NHC. Both: deterministic checks → drain. Neither has confidence, cost model, rollback, or verification-of-repair automation (F5 explicitly leaves post-repair "node screen" and partner-node draining as **manual**, and names partner-node drain automation as future work).

## F.4 Remaining difference (concrete, testable)

**The entire HPC proactive-remediation lineage (F2, F3, F4) never reached production, and F4 — the most recent and most sophisticated — is pure SimPy simulation that *assumes* high prediction accuracy.** Meanwhile the cloud (F1) and the GPU-training world (F6, F7) have real closed loops. This is a genuine, documentable 18-year gap.

Concretely open and testable:
1. **Blast-radius-aware action selection.** Cost of draining node *n* is not constant — it depends on which jobs are on it, their elapsed time, their checkpoint recency, and queue pressure. No verified work models this. Frontier drains at a fixed policy.
2. **Provenance- and confidence-gated auto-resume with verification.** Formalize F5's ad-hoc rule: an action taken by an automated agent may be auto-reverted; an action taken by a human may not. Add a confidence threshold and a **post-action verification test** that must pass before the node re-enters the pool, with measured false-return rate.
3. **Counterfactual/off-policy evaluation of drain policies from historical logs.** Narya used *online* experimentation. A center cannot A/B-test drains on a Tier-0 machine cheaply. Off-policy evaluation of remediation policies from Slurm node-state history + job outcomes is unaddressed and is a real methodological contribution.
4. **Closing the loop at the scheduler.** E15 (Iosup survey) finds closed-loop control "partially manual" across all 10 production ODA frameworks and notes AI-based schedulers "have not been implemented in MLOps pipelines... due to lack of standardized benchmarks and concerns about interpretability and trust."

## F.5 Verdict: **STILL_OPEN in HPC / CLOSED in cloud and LLM-training**

More precisely: **CLOSED** for "predict failure then checkpoint/migrate" as a *concept* (F2 2008, F4 2020 — the idea is 18 years old and simulated to death). **STILL_OPEN** for *any* production-validated learned remediation policy on an HPC batch system. **ENGINEERING_ONLY** risk is high: if you build a health-score→drain integration and report that it worked, reviewers will call it a HPCSYSPROS/CUG paper. The research content must be in the **decision theory** (blast radius, off-policy evaluation, safety gating), not the plumbing.

## F.6 SC Technical Paper viability (F)

**This is the highest-risk axis for SC-Technical-Paper acceptance and simultaneously the one with the widest genuine gap.** The risk is not novelty — it is *evaluability*. Reviewers will not accept another simulation (F4 already occupies that slot), and no center will let you run randomized drain experiments on a production Tier-0 machine.

**Reviewer will demand:**
- Real actions taken on a real system, or a defensible **off-policy evaluation** on ≥1 year of node-state + job-outcome history with confidence intervals.
- Explicit cost model: node-hours lost to unnecessary drains vs node-hours saved from averted job failures, both measured.
- **False-drain rate** and **false-return rate** as first-class metrics. Cite F11.
- Baseline = the center's existing rule-based NHC/checknode policy, not a strawman.
- Safety argument: what the agent may do unsupervised, what requires human approval, what the rollback is, and what the verification test is. Show a case where the agent's action was wrong and the guard caught it.
- Comparison/positioning against Narya (F1) and FALCON (F7) — reviewers will know these.

**Strongest counterargument:** *"Narya solved adaptive mitigation with online experimentation in production in 2020; FALCON does automatic multi-level straggler mitigation on 10k GPUs; Frontier already auto-drains. The HPC-specific delta is a cost model, which is engineering."* — The only durable defense is the **off-policy evaluation methodology** (you cannot online-experiment on a Tier-0 machine, Narya could on Azure — that is a real methodological difference, not an excuse) combined with **job-level blast radius**, which has no cloud analogue.

**Recommendation:** F is the strongest *scientific* gap but the weakest *publishable-in-2027* bet unless you have (a) authority to take real automated actions on the production machine, or (b) ≥1 year of node-state history rich enough for credible off-policy evaluation. If you have neither, fold F into D/E as a "what the diagnosis enables" section rather than making it the paper.

## F.7 Testability

Requires: full Slurm node-state transition history with reasons and actor (who/what set it), job outcome records, checkpoint metadata if available, plus the D-axis telemetry as the policy input. The *actor* field (human vs automated vs epilog) is the critical and often-missing column — check whether your center records it. Without it, off-policy evaluation is not possible and F is not viable.

---

# AXIS G — Operational LLM / agents

## G.1 Verified works

| # | Work | Yr | Venue | Type | ID | Contribution | Scale / eval | Prod? | L | D | P |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 ⚠️ | **Recommending Root-Cause and Mitigation Steps for Cloud Incidents using Large Language Models** — Ahmed, Ghosh, Bansal, Zimmermann, Zhang, Rajmohan | 2023 | **ICSE 2023** | conf | [10.1109/ICSE48619.2023.00149](https://dl.acm.org/doi/10.1109/ICSE48619.2023.00149), [arXiv 2301.03797](https://arxiv.org/abs/2301.03797), [dblp AhmedGBZZR23](https://dblp.org/rec/conf/icse/AhmedGBZZR23.html) | First large-scale LLM-for-incident study; fine-tuned GPT-3.x on Microsoft incidents; **human evaluation by on-call engineers** | 10s of thousands of incidents (`UNVERIFIED` count) | MS internal | L5/L6 | D2 | P4 |
| G2 ✅ | **Automatic Root Cause Analysis via Large Language Models for Cloud Incidents** (**RCACopilot**) — Chen, Xie, Ma, Kang, Gao, Shi, Cao et al. | 2024 | **EuroSys'24** | conf | [10.1145/3627703.3629553](https://dl.acm.org/doi/10.1145/3627703.3629553), [arXiv 2305.15778](https://arxiv.org/pdf/2305.15778) | Two-stage: handler-driven **diagnostic collection** (this is the real systems contribution) → FastText+temporal retrieval of similar incidents → few-shot CoT GPT-4 category + explanation | **653 incidents, Microsoft Transport, 1 year.** Micro-F1 **0.766**, Macro-F1 **0.533**, 4.2 s/incident | **Yes** — collection component deployed **>4 years across >30 MS teams**; prediction module in Transport for months | **L5/L6** | **D4** | **P4** |
| G3 ✅ | **AIOpsLab: A Holistic Framework to Evaluate AI Agents for Enabling Autonomous Clouds** — Chen, Shetty, Somashekar, Ma, Simmhan, Mace, Bansal, Wang, Rajmohan | 2025 | arXiv (MSR) | preprint/benchmark | [2501.06706](https://arxiv.org/abs/2501.06706), [code](https://github.com/microsoft/AIOpsLab) | Agent-cloud interface + task suite spanning detection → localization → RCA → mitigation in live microservice environments | Microservice benchmarks; specific agent scores `UNVERIFIED` from my fetch | — | L3–L7 | benchmark | — |
| G4 ✅ | **ITBench: Evaluating AI Agents across Diverse Real-World IT Automation Tasks** — Jha, Arora, Watanabe, Yanagawa +36 (IBM + UIUC) | 2025 | arXiv; **ICML 2025 poster** | benchmark | [2502.05352](https://arxiv.org/abs/2502.05352), [ICML](https://icml.cc/virtual/2025/poster/44303) | **94 real-world scenarios** across SRE / CISO / FinOps. **SOTA agents: SRE 13.8%, CISO 25.2%, FinOps 0%** | 94 scenarios | — | L3–L7 | benchmark | — |
| G5 ⚠️ | **OpsEval: A Comprehensive Benchmark Suite for Evaluating LLMs' Capability in IT Operations Domain** — Liu, Pei et al. | 2025 | **FSE 2025** | conf | [10.1145/3696630.3728572](https://dl.acm.org/doi/10.1145/3696630.3728572), [arXiv 2310.07637](https://arxiv.org/abs/2310.07637) | Bilingual (EN/ZH) IT-ops LLM benchmark | — | — | benchmark | — | — |
| G6 ✅ | **L4: Diagnosing Large-scale LLM Training Failures via Automated Log Analysis** — Jiang, Huang, Yu, Chen, Li, Zhong, Feng, Yang, Yang, Lyu | 2025 | **FSE Companion '25** | conf (industry) | [10.1145/3696630.3728531](https://doi.org/10.1145/3696630.3728531) | **Empirical study: 428 real LLM-training failures, Platform-X, May'23–Apr'24, avg 941 accelerators, avg 16.92 GB logs/failure. Avg diagnosis time 34.7 h; 41.9% >24 h.** Method: Drain parsing → cross-job filtering vs successful jobs → spatial (IsolationForest across ranks) + temporal (DTW + 3σ across iterations) → fault-pattern library. **F1 0.873** (R 0.982 / P 0.786) for failure-indicating logs vs 0.207–0.366 for LogAnomaly/LogRobust/NeuralLog; faulty-node top-1 **65.8%**, top-5 **80%** | 100-failure eval set | **Yes, live since Jun 2024**, recommends to SREs | **L5** | **D4** | **P3** |
| G7 ✅ | **FRAGATA: Semantic Retrieval of HPC Support Tickets via Hybrid RAG over 20 Years of Request Tracker History** — Paramés-Estévez, Filloy-Montesino, Fernández-Fabeiro, Carlos-Mouriño Gallego (CESGA) | 2026 | **Jornadas SARTECO 2026** | conf (regional) | [2604.13721](https://arxiv.org/html/2604.13721) | FAISS + BM25 + cross-encoder rerank + weighted RRF over **20 years of CESGA RT tickets**; ES/GL/EN cross-lingual; deployed (FastAPI, incremental Slurm-driven reindex, hot-swap) | 20 yr; ticket count not stated | Yes | L6 | D4 | P3 |
| G8 ⚠️ | **TicketHub: Enabling Actionable Analysis of Support Requests With NLP** | 2023 | PEARC'23 | conf | [10.1145/3569951.3604397](https://dl.acm.org/doi/10.1145/3569951.3604397) | NLP over HPC support requests | — | — | L1/L5 | D3 | P3 |
| G9 ⚠️ | **Generating Frequently Asked Questions from Technical Support Tickets using Large Language Models** | 2025 | **SC'25 Workshops** | workshop | [10.1145/3731599.3767429](https://doi.org/10.1145/3731599.3767429) | LLM over HPC tickets → FAQ | — | — | L6 | D2 | P2 |
| G10 ⚠️ | **LLM Agents for Interactive Workflow Provenance: Reference Architecture and Evaluation Methodology** (ORNL) | 2025 | **SC'25 Workshops** | workshop | [10.1145/3731599.3767582](https://dl.acm.org/doi/full/10.1145/3731599.3767582), [arXiv 2509.13978](https://arxiv.org/pdf/2509.13978) | Reference architecture + eval methodology for LLM agents querying HPC workflow provenance. **Closest DOE-lab LLM-agent-for-HPC-data work I found — and it is a workshop paper, not a Technical Paper** | — | — | L5/L6 | D1/D2 | P1 |
| G11 ✅ | **How Far Can Root Cause Analysis Go on Real-World Telemetry Data?** — Gopal, Krishnan (QPIAI) | 2026 | arXiv (**venue claim of "ICLR 2025" in the page is inconsistent with a 2026 arXiv ID — treat as `UNVERIFIED`; OpenRCA is the ICLR'25 artifact it evaluates against**) | preprint | [2607.13548](https://arxiv.org/html/2607.13548v1) | On **OpenRCA** (64 GB; Market CB1/CB2, Bank, Telecom; 30-min windows, 1–2 labeled root causes): best structured multi-agent RCA = **25.71%** full score; OpenRCA agent 11.43%; GALA 2.56%; RCLAgent 0%. **All classical causal-discovery methods (Granger, PC, FCI, LiNGAM, NTLR) = 0% Acc@1.** Error analysis: **65.7% of failures are "reasoning gaps" (evidence present, unused)** vs 11.4% genuine data ambiguity. Explicit causal graphs "accumulate spurious edges" | — | — | — | — | — |
| G12 ⚠️ | **RCAEval: A Benchmark for Root Cause Analysis** — Pham Qui Luan et al. | ASE'24 / WWW'25 / FSE'26 | — | benchmark | [GitHub](https://github.com/phamquiluan/RCAEval) | RCA benchmark series. Details `UNVERIFIED` | — | — | benchmark | — | — |
| G13 ✅ | **What Artificial Intelligence can do for HPC systems?** — Pochelu, Cartiaux, Schleich | 2025/26 | arXiv | survey | [2602.00014](https://arxiv.org/html/2602.00014) | On LLMs for HPC: *"**There is no documented evidence of production-level deployment to date**, and the reliance on simplified tasks... does not reflect the skills required..."*; *"papers in this area are rare and pursue heterogeneous objectives... **without shared benchmarks**"* | 74 papers | — | — | — | — |
| G14 ✅ | **Literature study on ODA frameworks** — Suman, Chu, Iosup (see E15) | 2026 | arXiv [2603.19016](https://arxiv.org/html/2603.19016) | survey | — | **No LLM integration in any of the 10 surveyed production ODA frameworks** | 10 centers | — | — | — | — |
| G15 ⚠️ | **AI Agents for HPC Services** — Alberto Garcia (Do IT Now), ISC 2026 HPC Solutions Forum | 2026 | ISC'26 vendor forum | talk | [session](https://isc.app.swapcard.com/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQ2NDEzMA==) | RAG + LLM for HPC consulting/deployment/support. **Vendor talk, no deployed system or results presented.** Evidence of commercial interest, not of prior art | — | — | — | — | — |

## G.2 Strongest existing method

**RCACopilot (G2)** and **L4 (G6)** are the two bars.

- **RCACopilot does:** deployed >4 years across >30 Microsoft teams for the *diagnostic collection* half; the LLM half predicts root-cause category with Micro-F1 0.766 on 653 hand-labeled incidents from one service, in 4.2 s, with explanations on-call engineers report as time-saving.
- **RCACopilot does NOT do:** generalize across services (authors state this as a limitation: "evaluation conducted on single service"); Macro-F1 is only **0.533**, i.e., it is weak on rare categories — which are precisely the ones that need help; it cannot function without a pre-existing incident handler for the alert type. It is not autonomous — it recommends.
- **L4 does:** the only verified work that does *quantified* LLM/ML-era failure diagnosis on a real 900+-accelerator training platform, in production, with a released empirical study of 428 real failures and a 34.7-hour human baseline to beat.
- **L4 does NOT do:** use an LLM in the diagnosis path at all (Drain + IsolationForest + DTW). It is honest that **36% of failures need multi-modal data (metrics, network traces)** beyond logs, and 10.1% leave no log evidence.

## G.3 Closest production implementation operators actually run

In HPC: **essentially nothing.** Two independent 2026 surveys (G13, G14) state there is no documented production LLM deployment in HPC operations and no LLM in any of 10 surveyed production ODA frameworks. The closest real deployed HPC artifact is **FRAGATA (G7)** — a hybrid-RAG ticket search at CESGA, published at a **regional Spanish conference**, with **no quantitative evaluation** (the authors say so: "no quantitative metrics or formal relevance judgments provided yet").

In cloud: RCACopilot's collection layer, >30 teams, >4 years.

## G.4 Remaining difference (concrete, testable)

Two genuinely open things, and one that is not:

**Open — (a) an operational-LLM benchmark for HPC.** ITBench (94 scenarios, SRE 13.8%), AIOpsLab, OpsEval, RCAEval, OpenRCA all exist for *cloud microservices*. **None covers HPC**: no Slurm, no MPI/NCCL collectives, no fabric counters, no parallel filesystem, no batch queue semantics, no node-state machine. G13 names "no shared benchmarks" as the specific blocker. A benchmark with real HPC incidents + the telemetry needed to solve them + a scored agent-system interface is a defensible artifact contribution.

**Open — (b) agents that must query heterogeneous HPC telemetry to reach a diagnosis, evaluated against operator ground truth.** G11 is the key enabler *and* the key warning: on real telemetry, **65.7% of RCA failures are reasoning gaps, not missing data**, and all classical causal-discovery baselines score **0% Acc@1**. That means (i) the problem is real and unsolved, and (ii) you must not propose causal graphs as the fix — that's already been shown to add spurious edges.

**Not open — (c) log summarization, chatbots, ticket FAQ generation, RAG over docs.** G7, G8, G9, G15 occupy this. It is workshop/PEARC material. Do not build an SC Technical Paper on it.

## G.5 Verdict: **PARTIALLY_ADDRESSED, and for HPC specifically INSUFFICIENT_EVIDENCE trending to STILL_OPEN**

Split verdict:
- LLM for cloud incident RCA → **CLOSED** (G1, G2 — production, evaluated, deployed).
- Benchmarks for operational LLM agents → **CLOSED for cloud** (G3, G4, G5, G12), **STILL_OPEN for HPC**.
- LLM/agents for HPC operations → **STILL_OPEN**, but with **INSUFFICIENT_EVIDENCE** that anyone has yet shown it works. Two 2026 surveys independently report zero production deployments. That is either a wide-open gap or a signal that the value isn't there.
- HPC ticket RAG / summarization → **CLOSED / ENGINEERING_ONLY**.

## G.6 SC Technical Paper viability (G) — honest assessment for 2026–2027

**Plausible, but only in one of two shapes, and both are hard.**

**Shape 1 — HPC operational agent benchmark (recommended).** Build the HPC analogue of ITBench/AIOpsLab: N real incidents from a Tier-0 machine, each with the frozen telemetry snapshot needed to diagnose it, an agent-system interface exposing Slurm/DCGM/fabric/Lustre/RAS as tools, and an operator-adjudicated ground-truth diagnosis. Report frontier-model agent scores. **Why it works:** artifact contributions are accepted at SC; both surveys name the missing-benchmark gap explicitly; ITBench's 13.8% SRE score gives you a credible expectation that scores will be low and therefore *interesting*. **Why it's hard:** you must release real operational data (sanitization, institutional approval) and hand-adjudicate ground truth. Budget most of the project on this.

**Shape 2 — agent that beats a measured human baseline on real diagnosis time.** L4's 34.7-hour average diagnosis time is the template: measure your operators' current time-to-diagnosis, then show the agent reduces it, with a controlled operator study. **Why it's hard:** requires an operator study with enough incidents for significance.

**What will get you rejected:** "we applied GPT-N to our syslog and it summarized it nicely"; RAG over documentation; any evaluation that is LLM-as-judge only; any claim of RCA without operator-confirmed ground truth.

**Reviewer will demand:** real HPC incidents (≥50, ideally ≥100) with adjudicated causes; a measured human baseline; comparison against non-LLM baselines (L4's Drain+IsolationForest+DTW pipeline is the right one — note L4 *beats* LLM-era log-AD baselines without an LLM, which is the strongest anti-LLM argument in this space); ablation on which telemetry channels the agent actually used; cost and latency; and **safety constraints** if the agent can act (tie to Axis F).

**Strongest counterargument against novelty:** *"Microsoft did LLM incident RCA in production in 2023–24 (ICSE'23, EuroSys'24); AIOpsLab and ITBench already benchmark ops agents; ITBench shows agents score 13.8% on SRE tasks, and 'How Far Can RCA Go' shows the ceiling is agent reasoning, not data. Substituting Slurm for Kubernetes is a domain port, not a contribution."* — The defense must be that **HPC telemetry is structurally different** (dense numeric multivariate time series at 1 Hz across 10⁴ nodes with tight spatial/topological coupling and gang-scheduled blast radius, vs sparse traces + logs in microservices), that the **cause taxonomy is different**, and that **no benchmark exists**, backed by the two 2026 survey quotes. That is a defensible but not overwhelming position — it is the weakest of the four axes on pure novelty and the strongest on artifact value.

## G.7 Testability

Benchmark construction is testable with exactly the telemetry you listed, plus the ticket/RAS/maintenance join from Axis E. **Axis G is downstream of Axis E**: without the label pipeline you cannot build ground truth, and without ground truth a G paper is not publishable at SC.

---

# CROSS-AXIS SYNTHESIS

**Ranking by SC-Technical-Paper defensibility for a KISTI Tier-0 center, 2026–2027:**

1. **D+E combined** (cause-discriminating slow-node diagnosis, trained/evaluated on a principled multi-source weak-label pipeline, ≥6–12 months, production Tier-0). This is the strongest bet. E supplies the label credibility that D's reviewers will attack; D supplies the systems contribution that E alone lacks. Verdict **STILL_OPEN**.
2. **G Shape-1** (HPC operational-agent benchmark built on the D+E ground truth). Strong artifact value, explicitly-named gap in two independent 2026 surveys, but a domain-port novelty objection. Verdict **STILL_OPEN / INSUFFICIENT_EVIDENCE**.
3. **F** (safe remediation). Widest genuine scientific gap — an 18-year lineage that never reached production while cloud and LLM-training clusters closed the loop — but the hardest to evaluate. Viable **only** if you can take real automated actions or have ≥1 year of node-state history with an *actor* field for off-policy evaluation. Otherwise fold into D+E. Verdict **STILL_OPEN but ENGINEERING_ONLY risk high**.

**Three facts that should shape the framing, all verified:**
- IPDPS 2026 (D10) already measured Perlmutter+Frontier and found **network congestion dominates variability while individual GPU performance is stable**. Do not frame a paper around GPU degradation being the main cause; that has been measured and contradicted.
- M100's own paper reports **AUC 0.57** using Nagios weak labels (E1) — the single best citation for why the label problem is real and unsolved.
- **65.7% of RCA failures on real telemetry are reasoning gaps, not missing data** (G11), and **all classical causal-discovery methods score 0% Acc@1**. Do not propose causal graph discovery.

**Highest-risk unverified items you must read before committing** (I could not fetch these): **Mantis** (ICS 2026, [10.1145/3797905.3800527](https://dl.acm.org/doi/10.1145/3797905.3800527)) for Axis D/F; **Safe Remediation as Risk-Constrained Intervention Decision** ([arXiv 2607.20005](https://arxiv.org/html/2607.20005)) for Axis F — this one could directly pre-empt the F framing; **ALBADross/TPDS 2024** ([10.1109/TPDS.2024.3365462](https://dl.acm.org/doi/abs/10.1109/TPDS.2024.3365462)) for Axis D/E; **HPC ODA Commons** (PEARC'26, [10.1145/3785462.3815891](https://doi.org/10.1145/3785462.3815891)) if you plan any dataset release.

Sources: [Fail-Slow at Scale](https://www.usenix.org/conference/fast18/presentation/gunawi) · [Gray Failure](https://www.researchgate.net/publication/318575785_Gray_Failure_The_Achilles'_Heel_of_Cloud-Scale_Systems) · [Limping-Hardware Tolerant Clouds](https://ucare.cs.uchicago.edu/pdf/hotcloud13-limpingHw.pdf) · [Perseus FAST'23](https://www.usenix.org/conference/fast23/presentation/lu) · [Sieve ATC'25](https://www.usenix.org/system/files/atc25-dong.pdf) · [ARGUS](https://arxiv.org/abs/2606.20374) · [LLMPrism](https://arxiv.org/abs/2505.00342) · [What-if Stragglers](https://arxiv.org/abs/2505.05713) · [FALCON](https://arxiv.org/abs/2410.12588) · [Elusive GPU Performance IPDPS'26](https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf) · [Dragonfly Variability IPDPS'20](https://ieeexplore.ieee.org/document/9139880/) · [Network Congestion Cluster'20](https://www.bu.edu/peaclab/files/2020/08/Cluster_CameraReady_Network_Congestion.pdf) · [Slingshot SC20](https://arxiv.org/abs/2008.08886) · [Kaleidoscope SC20](https://par.nsf.gov/servlets/purl/10293041) · [NodeSentry SC'25](https://dl.acm.org/doi/full/10.1145/3712285.3759794) · [Tuncer ISC'17](https://link.springer.com/chapter/10.1007/978-3-319-58667-0_19) · [Tuncer TPDS](https://www.osti.gov/biblio/1474092) · [E2EWatch](https://www.bu.edu/peaclab/files/2021/06/E2EWatch_EuroPar_CR.pdf) · [ALBADross TPDS'24](https://dl.acm.org/doi/abs/10.1109/TPDS.2024.3365462) · [HeaRank KDD'26](https://arxiv.org/abs/2607.15115) · [When GPUs Fail Quietly](https://arxiv.org/html/2603.28781v2) · [Exascale Diagnostics](https://arxiv.org/abs/2605.03561) · [M100 ExaData](https://www.nature.com/articles/s41597-023-02174-3) · [RUAD](https://dl.acm.org/doi/10.1016/j.future.2022.12.001) · [Borghesi semi-supervised AE](https://www.sciencedirect.com/science/article/abs/pii/S0952197619301721) · [Prodigy SC'23](https://dl.acm.org/doi/10.1145/3581784.3607076) · [Fresco PEARC'25](https://dl.acm.org/doi/10.1145/3708035.3736090) · [Rigorous TSAD Evaluation AAAI'22](https://arxiv.org/abs/2109.05257) · [Flawed Evaluation Methodology](https://link.springer.com/chapter/10.1007/978-3-031-68031-1_1) · [Did We Actually Fix It?](https://arxiv.org/abs/2607.11969) · [Metric Maze](https://link.springer.com/article/10.1007/s10618-023-00988-8) · [Log AD How Far Are We ICSE'22](https://arxiv.org/pdf/2202.04301) · [Comprehensive ML Log AD Study](https://arxiv.org/html/2307.16714v3) · [Log Parsing Impact](https://link.springer.com/article/10.1007/s10664-024-10533-w) · [Loghub](https://www.researchgate.net/publication/375267895_Loghub_A_Large_Collection_of_System_Log_Datasets_for_AI-driven_Log_Analytics) · [ODA Literature Study](https://arxiv.org/html/2603.19016) · [HPC ODA Commons](https://doi.org/10.1145/3785462.3815891) · [DCDB Wintermute](https://dl.acm.org/doi/abs/10.1145/3369583.3392674) · [Weak Supervision AD Benchmark](https://arxiv.org/html/2605.26068v3) · [Weak Supervision PdM Survey](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/widm.70022) · [Weakly-Supervised Log Localization](https://arxiv.org/html/2605.10988) · [AI for HPC Survey](https://arxiv.org/html/2602.00014) · [Narya OSDI'20](https://www.usenix.org/conference/osdi20/presentation/levy) · [Proactive Live Migration SC'08](https://dl.acm.org/doi/10.5555/1413370.1413414) · [Back Migration JPDC](https://www.sciencedirect.com/science/article/abs/pii/S0743731511002085) · [Orchestrating Fault Prediction HPDC'20](https://arcb.csc.ncsu.edu/~mueller/ftp/pub/mueller/papers/hpdc20.pdf) · [Frontier checknode CUG'23](https://cug.org/proceedings/cug2023_proceedings/includes/files/pap151s2-file1.pdf) · [Unicron](https://arxiv.org/abs/2401.00134) · [Safe Remediation](https://arxiv.org/html/2607.20005) · [Systemic Node Failures IPDPS'21](https://arcb.csc.ncsu.edu/~mueller/ftp/pub/mueller/papers/ipdps21.pdf) · [Reducing False Predictions](https://www.researchgate.net/publication/339257965_Reducing_False_Node_Failure_Predictions_in_HPC) · [Mantis ICS'26](https://dl.acm.org/doi/10.1145/3797905.3800527) · [NØMAD](https://openresearchsoftware.metajnl.com/articles/10.5334/jors.686) · [Health Benchmarking HPCSYSPROS](https://dl.acm.org/doi/10.1145/3155105.3155106) · [Ahmed ICSE'23](https://dl.acm.org/doi/10.1109/ICSE48619.2023.00149) · [RCACopilot EuroSys'24](https://dl.acm.org/doi/10.1145/3627703.3629553) · [AIOpsLab](https://arxiv.org/abs/2501.06706) · [ITBench](https://arxiv.org/abs/2502.05352) · [OpsEval FSE'25](https://dl.acm.org/doi/10.1145/3696630.3728572) · [L4 FSE'25](https://doi.org/10.1145/3696630.3728531) · [FRAGATA](https://arxiv.org/html/2604.13721) · [TicketHub PEARC'23](https://dl.acm.org/doi/10.1145/3569951.3604397) · [FAQ from Tickets SC'25W](https://doi.org/10.1145/3731599.3767429) · [LLM Agents Workflow Provenance SC'25W](https://dl.acm.org/doi/full/10.1145/3731599.3767582) · [How Far Can RCA Go](https://arxiv.org/html/2607.13548v1) · [RCAEval](https://github.com/phamquiluan/RCAEval) · [ISC'26 AI Agents for HPC Services](https://isc.app.swapcard.com/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQ2NDEzMA==)agentId: a9241ddb04ef0a4bf (use SendMessage with to: 'a9241ddb04ef0a4bf', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 152693
tool_uses: 85
duration_ms: 832559</usage>
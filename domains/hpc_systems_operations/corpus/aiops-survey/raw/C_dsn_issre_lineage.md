I've completed the census. Web search budget was exhausted mid-task, so the remainder was done via direct page fetches (dblp record pages, conference program pages, USENIX presentation pages, arXiv). ACM DL and IEEE Xplore are blocked from this environment, which constrains verification of some ICSE/FSE/ASPLOS/SOSP items — those are marked `UNVERIFIED`.

---

# HPC AIOps / Operational Intelligence — Literature Census
**Compiled 2026-09-06. For SC Technical Paper positioning.**

## 0. METHOD, COVERAGE, AND VERIFICATION STATUS

**Sources actually used (and what worked):**
| Source | Status |
|---|---|
| dblp `/db/conf/*` ToC pages | Works but **truncates at ~10 entries** — unusable for full ToCs |
| dblp `/rec/*.html` record pages | Works perfectly — used for per-paper verification of titles/venues/years/DOIs |
| dblp search API | ROBOTS_DISALLOWED |
| ISSRE official program pages (`issre.github.io`, `2020/2021.issre.net`) | Works — **full ToCs obtained** |
| DSN official accepted-papers pages (`dsn20XX.github.io`, `dsn2023.dei.uc.pt`) | Works for 2022–2025 |
| USENIX `/conference/*/presentation/*` | Works — used for OSDI/NSDI/ATC/FAST verification |
| arXiv `/abs/*` | Works |
| ACM DL, IEEE Xplore, Semantic Scholar, OpenAlex, web.archive.org | **Blocked (403 / robots / JS-only / rate-limited)** |

**Coverage achieved:**

| Venue | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| **DSN** | ⚠ PARTIAL | ⚠ PARTIAL | ✅ full | ✅ full | ✅ full | ✅ full | ❌ NOT YET PUBLISHED |
| **ISSRE** | ✅ full | ✅ full | ✅ full | ✅ full | ✅ full | ✅ full | ❌ NOT YET PUBLISHED |

- **DSN 2020 / DSN 2021: verified only partially.** The Valencia (2020) and Taipei (2021) conference sites are gone or robots-blocked; dblp truncates. I verified only the first ~10 entries of each dblp ToC. **Any claim about DSN 2020/2021 content below is explicitly flagged.** This is the one real hole in the census and should be filled manually via IEEE Xplore from an institutional network.
- **DSN 2026 (56th) / ISSRE 2026 (37th): `PARTIAL / NOT YET PUBLISHED`.** ISSRE 2026 CFPs (research + industry track) are circulating; no accepted-paper list exists. Note that the NKU AIOps group publication list already advertises 2026 acceptances (FSE, ICSE, ASE, ISSTA, FAST) — see §C.

**Scale/dimension coding.** L0–L7 and D0–D5 as you defined them. You did not define P0–P4, so I use a **portability scale**, stated explicitly: **P0** = one system, one site; **P1** = multiple systems, one site/operator; **P2** = multi-site, same vendor/generation; **P3** = cross-vendor or cross-generation demonstrated; **P4** = system-agnostic / no site assumption.

---

# PART A — DSN & ISSRE 2020–2026, IN-SCOPE SUBSET

## A.1 The five records that matter most for an HPC-AIOps SC submission

**A1. Time Machine: Generative Real-Time Model For Failure (and Lead Time) Prediction in HPC Systems**
- Authors: Khalid Ayed Alharthi, Arshad Jhumka, Sheng Di, Lin Gui, Franck Cappello, Simon McIntosh-Smith | 2023 | **DSN 2023**, research track (session RT-14 "Potpourri") | conference full paper | ✅ verified (DSN 2023 official program)
- Problem: predict node/system failures **and their lead time** from RAS logs. Component: whole-system (node-level RAS). Data: HPC RAS logs (Blue Waters / Mira-class public log corpora). Method: generative sequence model over log-event streams producing next-event + time-to-failure. Eval: multi-year public HPC log datasets. Real production data ✅ / production deployment ❌.
- **L4** (prediction) | **D2** (offline production logs) | **P1**
- Contribution: joint failure *and lead-time* prediction — lead time is what makes proactive action feasible. Limitation: offline, log-only, no cross-system transfer, no action loop.
- **Relevance: this is the single closest DSN-side prior work to any "HPC failure prediction" SC submission. Must be cited and differentiated.**

**A2. Exploring Hierarchical Patterns for Alert Aggregation in Supercomputers**
- Authors: Yuan Yuan, Tongqing Zhou, Xiuhong Tan, Yongqian Sun, Yuqi Li, Zhixing Li, Zhiping Cai, Tiejun Li | 2024 | **ISSRE 2024**, research track, **Best Paper Candidate / Best Paper Award** | ✅ verified (ISSRE 2024 program + NKU list)
- Problem: alert storm reduction in a supercomputer; aggregate correlated alerts into incidents. Component: cross-component alerts. Data: production supercomputer alert stream (NUDT-affiliated system). Method: hierarchical pattern mining over alert taxonomy + topology.
- **L2→L3** | **D2/D4** | **P0**
- **Relevance: proves supercomputer-scale operational alerting is a live ISSRE topic and that Chinese national-lab supercomputer telemetry is being published. Direct competitor for "alert/event reduction" framings.**

**A3. ClusterRCA: An End-to-End Approach for Network Fault Localization and Classification for HPC System**
- Authors: Yongqian Sun, Xijie Pan, Xiao Xiong, Lei Tao, Jiaju Wang, Shenglin Zhang, Yuan Yuan, Yuqi Li, Kunlin Jian | 2025 | **ISSRE 2025**, research track (RS8) | ✅ verified (ISSRE 2025 program + NKU list)
- Problem: localize *and classify* network faults in an HPC cluster. Component: interconnect. Data: production HPC cluster network telemetry + fault records. Method: end-to-end learned localization + fault-type classification.
- **L3+L5** | **D2** | **P0/P1**
- **Relevance: THE closest work for any "HPC interconnect RCA" claim. Strongly constrains axis (A) and (D) novelty for the network layer specifically.**

**A4. Too Many Cooks: Assessing the Need for Multi-Source Data in Microservice Failure Diagnosis**
- Authors: Shenglin Zhang, Xiaoyu Feng, Runzhou Wang, Minghua Ma, Wenwei Gu, Yongqian Sun, Zedong Jia, Jinrui Sun, Dan Pei | 2025 | **ISSRE 2025**, **Best Research Paper Candidate** | ✅ verified
- Problem: does fusing logs + metrics + traces actually improve failure diagnosis, or is one modality enough? Finding: **diminishing/negative returns from multi-source fusion.**
- **L5** | **D2** | **P2**
- **Relevance: this is a NOVELTY HAZARD, not a supporting citation. Any SC paper claiming "we fuse CPU/GPU/network/storage/scheduler telemetry and that is the contribution" must pre-empt this paper's negative result. It is the strongest available "you have not shown fusion is necessary" reviewer weapon.**

**A5. Can We Trust Auto-Mitigation? Improving Cloud Failure Prediction with Uncertain Positive Learning**
- Authors: Haozhe Li, Minghua Ma, Yudong Liu, Pu Zhao, Shuo Li, Lingling Zheng, Ze Li, Murali Chintalapati, Yingnong Dang, Chetan Bansal, Saravan Rajmohan, Qingwei Lin, Dongmei Zhang | 2024 | **ISSRE 2024**, research track (RT-12) | Microsoft | ✅ verified
- Problem: once auto-mitigation is deployed, ground-truth failure labels are destroyed (mitigated failures never manifest) → positive-unlabeled learning under uncertainty. Data: Microsoft Azure production.
- **L4+L7** | **D5** (auto-mitigation is live) | **P2**
- **Relevance: the sharpest statement of the closed-loop label-corruption problem. Directly constrains axes (E) and (F). If you propose closed-loop HPC remediation, this paper defines the evaluation problem you must solve.**

## A.2 DSN 2022–2025, in-scope (all ✅ verified from official accepted-paper pages)

**DSN 2022 (Baltimore)**
- `Predicting DRAM-Caused Node Unavailability in Hyper-Scale Clouds` — Pengcheng Zhang, Yunong Wang, Xuhua Ma, Yaoheng Xu, Bin Yao, Xudong Zheng, Linquan Jiang (Alibaba). Research track. Memory-error → node-unavailability prediction at hyperscale. L4 | D2/D3 | P1. *Closest cloud analogue to HPC DRAM-driven node failure prediction.*
- `Characterizing and Mitigating Anti-patterns of Alerts in Industrial Cloud Systems` — Tianyi Yang, Jiacheng Shen, Yuxin Su, Xiaoxue Ren, Xiao Ling, Yongqiang Yang, Michael Lyu (Huawei Cloud). Field study of alert-rule pathologies. L2 | D2/D4 | P1. *Prior art for "your alert rules are the problem" framings.*
- `RAPMiner: A Generic Anomaly Localization Mechanism for CDN System with Multi-dimensional KPIs` — Chang Liu, Yanwei Liu, Zhen Xu, Liang Dai. L3+L5 | D2 | P1.
- `Active-MTSAD: Multivariate Time Series Anomaly Detection With Active Learning` — Wenlu Wang, Pengfei Chen, Yibin Xu, Zilong He. L3 | D1/D2 | P3. *Axis (E).*
- `COMET: On-die and In-controller Collaborative Memory ECC Technique...` — Irina Alam, Puneet Gupta. Hardware correction, not AIOps; relevant to DRAM-reliability framing.
- `Exploiting Temporal Data Diversity for Detecting Safety-critical Faults in AV Compute Systems` — Saurabh Jha, Shengkun Cui, Timothy Tsai, Siva Kumar Sastry Hari, Michael Sullivan, Zbigniew Kalbarczyk, Stephen W. Keckler, Ravishankar K. Iyer (NVIDIA + UIUC). GPU/accelerator SDC detection at runtime. L3 | D1 | P2.
- Industry track: `Long-Term Study of Honeypots in a Public Cloud` (Microsoft) — marginal.

**DSN 2023 (Porto)**
- `HiMFP: Hierarchical Intelligent Memory Failure Prediction for Cloud Service Reliability` — Q. Yu, W. Zhang, S. Haeri, P. Notaro, J. Cardoso, O. Kao (Huawei Munich + TU Berlin). Hierarchical (cell→bank→DIMM→node) memory failure prediction. L4 | D2 | P1.
- `How Different are the Cloud Workloads? Characterizing Large-Scale Private and Public Cloud Workloads` — X. Qin, M. Ma, Y. Zhao, J. Zhang, C. Du, Y. Liu, A. Parayil, C. Bansal, S. Rajmohan, Í. Goiri, E. Cortez, S. Qin, Q. Lin, D. Zhang (Microsoft). Field characterization; L0/L1 | D2 | P2. *Template for a "characterize before you model" SC paper.*
- `Āpta: Fault-tolerant object-granular CXL disaggregated memory for accelerating FaaS` — hardware/architecture, relevant only as CXL-reliability context.

**DSN 2024 (Brisbane)**
- `Mutiny! How does Kubernetes fail, and what can we do about it?` — Marco Barletta, Marcello Cinque, Catello Di Martino, Zbigniew Kalbarczyk, Ravishankar K. Iyer. Fault-injection field-failure study of the orchestrator. L0/L3 | D1/D2 | P3. *Methodological template: injection-driven failure taxonomy for a resource manager — directly transferable to Slurm/PBS.*
- `iPrism: Characterize and Mitigate Risk by Quantifying Change in Escape Routes` — Shengkun Cui, Saurabh Jha, Ziheng Chen, Zbigniew T. Kalbarczyk, Ravishankar K. Iyer. L5/L6 | D1 | P2.
- `A Fast Low-Level Error Detection Technique` — Zhengyang He, Hui Xu, Guanpeng Li. SDC detection. L3 | D1 | P3.
- Industry: `Investigating Memory Failure Prediction Across CPU Architectures` — Qiao Yu, Wengui Zhang, Min Zhou, Jialiang Yu, Zhenli Sheng, Jorge Cardoso, Jasmin Bogatinovski, Odej Kao (Huawei). **The single most direct prior work on cross-generation/cross-architecture transfer of a hardware failure-prediction model.** L4 | D2 | **P3** — *critical for axis (B).*
- Industry: `Fault Localization Using Interventional Causal Learning for Cloud-Native Applications` — Saurabh Jha, Jesus Rios, Frank Bagehorn, Larisa Shwartz, Naoki Abe (IBM). Causal (interventional) RCA. L5 | D1/D2 | P2. *Closest "principled causal RCA" prior work.*
- Industry: `Active Learning Omnivariate Decision Trees for Fault Diagnosis in Robotic Systems` — Casidhe Hutchison et al. Axis (E) method.
- Disrupt: `When Green Computing Meets Performance and Resilience SLOs` — Haoran Qiu, Weichao Mao, Chen Wang, Saurabh Jha, Hubertus Franke, Chandra Narayanaswami, Tamer Başar, Zbigniew Kalbarczyk, Ravishankar Iyer (IBM+UIUC). Power/perf/resilience joint objective. L6 | D0/D1 | P2.

**DSN 2025 (Naples)** — *the industry track is unusually rich for HPC/AI-infra*
- Industry: `Large-Scale AI Infra Reliability: Challenges, Strategies, and Llama 3 Training Experience` — Jiao, Pandey, Pattabiraman, Lin (Meta + UBC). **The reference field-experience paper for GPU-cluster reliability at 16K-GPU scale.** L0–L4 | D4/D5 | P0. *Must-cite for any GPU-fleet reliability SC paper.*
- Industry: `Hardware Telemetry at Scale: A Case Study on SSDs Endurance Monitoring in Datacenters` — Medaiyese, Lin, Dixit, et al. (Meta). **The closest existing work to "telemetry cost at scale" (axis C)** — though it is a case study, not an optimization formulation. L0/L4 | D4 | P1.
- Industry: `Cordial: Cross-row Failure Prediction Method Based on Bank-level Error Locality for HBMs` — Gu, Gu, Zhong, et al. **HBM (i.e., GPU memory) failure prediction.** L4 | D2 | P1. *Direct prior art for GPU-memory failure prediction.*
- Industry: `LLMPrism: Black-box Performance Diagnosis for Production LLM Training Platforms` — Jiang, Ren, Yu, et al. **Black-box cross-layer performance diagnosis on a production GPU training platform — the closest work to axis (A)/(D) for GPU clusters.** L3+L5 | D3/D4 | P1.
- Industry: `DDR5 DRAM Faults in the Field` — Valad Beigi, Cao, Tsai, et al. Field failure study, current-generation memory. L0 | D2 | P2.
- Research: `ParaVerser: Harnessing Heterogeneous Parallelism for Affordable Fault Detection in Data Centers` — Liao, Ainsworth, Mukhanov, et al. Cost-aware SDC detection. L3 | D1 | P3. *Relevant to axis (C) framed as detection-cost.*
- Poster: `DeepICS: Deep Causal Relationship Modeling for Multi-Source Log-Based Anomaly Detection in ICS` — Yoon, Euom, Shin (Korean group; poster only, D0/D1).

**DSN 2020 / DSN 2021 — ⚠ PARTIAL.** Verified in-scope items only:
- DSN 2020: `PolygraphMR: Enhancing the Reliability and Dependability of CNNs` (Latifi, Zamirai, Mahlke, pp. 99–112); `ML-Driven Malware that Targets AV Safety` (Jha, Cui, Banerjee, Cyriac, Tsai, Kalbarczyk, Iyer, pp. 113–124). ✅ verified. **Remainder of DSN 2020 UNVERIFIED — assume in-scope papers exist that this census missed.**
- DSN 2021: `A Low-cost Fault Corrector for Deep Neural Networks through Range Restriction` (Chen, Li, Pattabiraman); `MILR: Mathematically Induced Layer Recovery...`; `A Comprehensive Study of Bugs in Software Defined Networks` (Bhardwaj, Zhou, Benson). ✅ verified. **Remainder UNVERIFIED.**

## A.3 ISSRE 2020–2025, in-scope (all ✅ verified from official program pages)

**ISSRE 2020** — `LogTransfer: Cross-System Log Anomaly Detection for Software Systems with Transfer Learning` (Rui Chen, Shenglin Zhang, Dongwen Li, et al.) **[axis B anchor]**; `SwissLog: Robust and Unified Deep Learning Based Log Anomaly Detection for Diverse Faults` (Xiaoyun Li, Pengfei Chen, Linxiao Jing, Zilong He, Guangba Yu); `How Far Have We Come in Detecting Anomalies in Distributed Systems?` (Yong Yang, Yifan Wu, Karthik Pattabiraman, Long Wang, Ying Li) **[reality-check paper]**; `Unsupervised Detection of Microservice Trace Anomalies through Service-Level Deep Bayesian Networks` (Ping Liu, Haowen Xu, Qianyu Ouyang, et al.); `Fault Injection to Generate Failure Data for Failure Prediction: A Case Study` (João Campos, Ernesto Costa) **[axis E]**; `Locating the Clues of Declining Success Rate of Service Calls` (Guoping Rong et al.); `Dependability Evaluation of Middleware Technology for Large-scale Distributed Caching` (Cotroneo, Natella, Rosiello).

**ISSRE 2021** — `LogFlash: Real-time Streaming Anomaly Detection and Diagnosis from System Logs` (Tong Jia, Yifan Wu, Chuanjia Hou, Ying Li); `Identifying Root-Cause Metrics for Incident Diagnosis in Online Service Systems` (Canhua Wu, Nengwen Zhao, ..., Dan Pei); `Robust KPI Anomaly Detection for Large-Scale Software Services with Partial Labels` (Shenglin Zhang, Chenyu Zhao, Yicheng Sui, Ya Su, Yongqian Sun, Yuzhi Zhang, Dan Pei, Yizhe Wang) **[axis E]**; `How Long Will it Take to Mitigate this Incident for Online Service Systems?` (Weijing Wang, Junjie Chen, ..., Microsoft) **[TTM prediction]**; `CloudPin: A Root Cause Localization Framework of Shared Bandwidth Package Traffic Anomalies in Public Cloud Networks`; `Optimizing Selective Protection for CNN Resilience` (Mahmoud, Hari, Fletcher, Adve, Sakr, Shanbhag, Molchanov, Sullivan, Tsai, Keckler — NVIDIA) **[GPU/accelerator resilience, cost-aware protection → axis C analogue]**.

**ISSRE 2022** — `Share or Not Share? Towards the Practicability of Deep Models for Unsupervised Anomaly Detection in Modern Online Systems` (Zilong He, Pengfei Chen, Tao Huang) **[Best Paper Candidate; axis B — model sharing across systems]**; `PUTraceAD: Trace Anomaly Detection with Partial Labels based on GNN and PU Learning` (Ke Zhang, Chenxi Zhang, Xin Peng, Chaofeng Sha) **[axis E]**; `Going through the Life Cycle of Faults in Clouds: Guidelines on Fault Handling` (Xiaoyun Li, Guangba Yu, Pengfei Chen, Hongyang Chen, Zhekang Chen); `LogVM: Variable Semantics Miner for Log Messages` (Yintong Huo, Yuxin Su, Michael Lyu); `Effective Attribute Selection for Multi-dimensional Root Cause Analysis` (Yiran Cheng, Bo Cheng, Pengxiang Jin, Yongqian Sun, Xiaohui Nie, Nengwen Zhao, Shenglin Zhang, Dan Pei); `Identifying Erroneous Software Changes through Self-Supervised Contrastive Learning on Time Series Data` (Xuanrun Wang et al.); `VECROsim: A Versatile Metric-oriented Microservice Fault Simulation System`; `SlowCoach: Mutating Code to Simulate Performance Bugs` (Yiqun Chen, Oliver Schwahn, Roberto Natella, Matthew Bradbury, Neeraj Suri).

**ISSRE 2023** — `AutoKAD: Empowering KPI Anomaly Detection with Label-Free Deployment` (Zhaoyang Yu, Changhua Pei, Shenglin Zhang, Xidao Wen, Jianhui Li, Gaogang Xie, Dan Pei) **[Best Paper Candidate; axis E]**; `Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics` (Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu) **[the benchmark corpus; includes BGL/Thunderbird/Spirit HPC logs — your baseline dataset]**; `AFALog: A General Augmentation Framework for Log-based Anomaly Detection with Active Learning` (Chiming Duan, Tong Jia, Huaqian Cai, Ying Li, Gang Huang) **[axis E]**; `EvLog: Identifying Anomalous Logs over Software Evolution` (Yintong Huo, Cheryl Lee, Yuxin Su, Shiwen Shan, Jinyang Liu, Michael Lyu) **[axis B — drift over software evolution]**; `fKPISelect: Fault-Injection Based Automated KPI Selection for Practical Multivariate Anomaly Detection` (Xingjian Zhang, Yinqin Zhao, Chang Liu, Long Wang, et al.) **[axis C — the closest existing "which telemetry do we actually need" paper]**; `Log Parsing Evaluation in the Era of Modern Software Systems` (Stefan Petrescu, Floris den Hengst, Alexandru Uta, Jan S. Rellermeyer); `Using Transformer Models and Textual Analysis for Log Parsing` (Bertalan, Aloise); `ServerRCA: Root Cause Analysis for Server Failure using Operating System Logs` (Jiahao Shi, Sihang Jiang, Bo Xu, Yanghua Xiao); `TraceStream: Anomalous Service Localization based on Trace Stream Clustering with Online Feedback` (Tencent); `Online Failure Prediction Through Fault Injection and Machine Learning: Methodology and Case Study` (João R. Campos, Ernesto Costa, Marco Vieira); `Practical Anomaly Detection over Multivariate Monitoring Metrics for Online Services` (Jinyang Liu, Tianyi Yang, Zhuangbin Chen, Yuxin Su, Cong Feng, Zengyin Yang, Michael R. Lyu — Huawei); `How to Manage Change-Induced Incidents? Lessons from the Study of Incident Life Cycle` + `Identifying Root-Cause Changes for User-Reported Incidents in Online Service Systems` (both Yujin Zhao, Ling Jiang, Ye Tao, ... Tong Jia, Ying Li, Zhonghai Wu); `CODEC: Cost-Effective Duration Prediction System for Deadline Scheduling in the Cloud` (Microsoft) **[scheduler-aware prediction]**; `An Empirical Analysis of Anomaly Detection Methods for Multivariate Time Series` (Dongwen Li, Shenglin Zhang, Yongqian Sun, et al.); `Efficient and Robust Trace Anomaly Detection for Large-Scale Microservice Systems` (Tencent); `Resilience Assessment of Large Language Models under Transient Hardware Faults` (Udit Kumar Agarwal, Abraham Chan, Karthik Pattabiraman).

**ISSRE 2024** — (see A.1 for #A2, #A5) plus: `KPIRoot: Efficient Monitoring Metric-based Root Cause Localization in Large-scale Cloud Systems` (Wenwei Gu, Xinying Sun, Jinyang Liu, Yintong Huo, Zhuangbin Chen, Jianping Zhang, Jiazhen Gu, Yongqiang Yang, Michael Lyu — Huawei); `Demystifying and Extracting Fault-indicating Information from Logs for Failure Diagnosis` (Junjie Huang, Zhihan Jiang, Jinyang Liu, Yintong Huo, Jiazhen Gu, Zhuangbin Chen, Cong Feng, Hui Dong, Zengyin Yang, Michael Lyu — Huawei); `Large Language Models Can Provide Accurate and Interpretable Incident Triage` (Zexin Wang, Jianhui Li, Minghua Ma, Ze Li, Yu Kang, Chaoyun Zhang, Chetan Bansal, Murali Chintalapati, Saravan Rajmohan, Qingwei Lin, Dongmei Zhang, Changhua Pei, Gaogang Xie) **[axis G]**; `LLMeLog: An Approach for Anomaly Detection based on LLM-enriched Log Events`; `Leveraging RAG-Enhanced Large Language Model for Semi-Supervised Log Anomaly Detection` (LogRAG); `LogCAE: ... Active Learning and Contrastive Learning`; `Self-Evolutionary Group-wise Log Parsing Based on Large Language Model` (Changhua Pei et al.); `TimeSeriesBench: An Industrial-Grade Benchmark for Time Series Anomaly Detection Models`; `Detection Latencies of Anomaly Detectors: An Overlooked Perspective?` (Puccetti, Ceccarelli) **[under-cited; lead-time framing]**; `LabelEase: A Semi-Automatic Tool for Efficient and Accurate Trace Labeling in Microservices` **[axis E]**; `SparseRCA: Efficient Root Cause Analysis in Sparse Microservice Testing Trace`; `FaaSRCA: Full Lifecycle Root Cause Analysis for Serverless Applications`; `Aspis: Lightweight Neural Network Protection Against Soft Errors` (Schmedding, Yang, Jog, Smirni); `DRLFailureMonitor`.

**ISSRE 2025** — (see A.1 for #A3, #A4) plus: `ZeroLog: Zero-Label Generalizable Cross-System Log-based Anomaly Detection` (Xinlong Zhao, Tong Jia, Minghua He, Ying Li, Gang Huang) **[axis B+E — strongest current cross-system claim]**; `Prepared for the Unknown: Adapting AIOps Capacity Forecasting Models to Data Changes` (Lorena Poenaru-Olaru, Wouter van 't Hof, Adrian Stańdo, Arkadiusz P. Trawiński, Eileen Kapel, Jan S. Rellermeyer, Luis Cruz, Arie van Deursen) **[axis B — concept drift, explicit]**; `Understanding Recommendation System Robustness Against Silent Data Corruption: An Empirical Study` (Dongning Ma, Xun Jiao, Fred Lin, Daniel Moore, Sriram Sankar — Meta) **[Best Paper Candidate; SDC at fleet scale]**; `An Empirical Study of Production Incidents in Generative AI Cloud Services` (Haoran Yan, Yinfang Chen, Minghua Ma, Ming Wen, Shan Lu, Shenglin Zhang, Tianyin Xu, Rujia Wang, Chetan Bansal, Saravan Rajmohan, Chaoyun Zhang, Qingwei Lin, Dongmei Zhang) **[GenAI-service incident taxonomy]**; `AetherLog: Log-based Root Cause Analysis by Integrating Large Language Models with Knowledge Graphs` (Tianyu Cui, ..., Shenglin Zhang, Yongqian Sun, Dan Pei) **[axis G]**; `DeST: An Unsupervised Decoupled Spatio-Temporal Framework for Microservice Incident Management`; `Integrating GraphSAGE and Mamba for Self-Supervised Spatio-Temporal Fault Detection in Microservice Systems`; `CSLParser: A Collaborative Framework Using Small and Large Language Models for Log Parsing`; `DLAFI: Software-Based Fault Injection for Permanent Faults in Deep Learning Accelerators` (Sadati, Chan, Agarwal, Pattabiraman).

**Structural observation across A.** In six years of DSN+ISSRE, **HPC-specific operational-intelligence papers number roughly five** (Time Machine DSN'23; Alert Aggregation in Supercomputers ISSRE'24; ClusterRCA ISSRE'25; plus GPU/HBM/AI-infra items on the DSN'25 *industry* track). Everything else is cloud/microservice. **The venue is not saturated on the HPC side — the saturation is on the method side.**

---

# PART B — HISTORICAL LINEAGE (pre-2020)

Five lines feed 2020s HPC AIOps. All records below **✅ verified via dblp record pages** unless marked.

### Line 1 — Autonomic / self-managing computing (the framing that AIOps inherited)
1. **The Vision of Autonomic Computing** — Jeffrey O. Kephart, David M. Chess. *IEEE Computer* 36(1):41–50, 2003. DOI 10.1109/MC.2003.1160055. ✅
   → Origin of the MAPE-K loop (Monitor–Analyze–Plan–Execute over shared Knowledge). **Your L0–L7 ladder is a re-derivation of MAPE-K; say so, and use it — reviewers reward the acknowledgement.** Evolution: MAPE-K → cloud autoscaling/self-healing (2010s) → "AIOps" branding (Gartner, 2016) → LLM-agent "AgentOps" (AIOpsLab, 2025). *The 2020s literature almost never closes the loop — Narya and Azure auto-mitigation are the rare D5 exceptions.*
2. **Microreboot — A Technique for Cheap Recovery** — George Candea, Shinichi Kawamoto, Yuichi Fujiki, Greg Friedman, Armando Fox. *OSDI 2004*, pp. 31–44. ✅
   → The self-healing/recovery-action ancestor. Evolution: microreboot → node drain/reschedule → Narya predictive mitigation (OSDI'20) → Just-In-Time Checkpointing (EuroSys'24). **This is the ancestor of your axis (F).**

### Line 2 — Failure prediction from system events
3. **Critical event prediction for proactive management in large-scale computer clusters** — Ramendra K. Sahoo, Adam J. Oliner, Irina Rish, Manish Gupta, José E. Moreira, Sheng Ma, Ricardo Vilalta, Anand Sivasubramaniam. *KDD 2003*, pp. 426–435. ✅
   → First serious "predict critical events in a large cluster from event logs" paper (IBM BlueGene-lineage).
4. **Failure Prediction in IBM BlueGene/L Event Logs** — Yinglung Liang, Yanyong Zhang, Hui Xiong, Ramendra K. Sahoo. *ICDM 2007*, pp. 583–588. DOI 10.1109/ICDM.2007.46. ✅
   → The canonical BG/L RAS-log failure-prediction paper; source of the BGL dataset that still appears in Loghub and in every 2020s log-anomaly benchmark. **Every modern log-AD paper is still evaluated on BGL — a 2007 dataset. That staleness is itself an SC-paper argument.**
5. **A survey of online failure prediction methods** — Felix Salfner, Maren Lenk, Miroslaw Malek. *ACM Computing Surveys* 42(3):10:1–10:42, 2010. DOI 10.1145/1670679.1670680. ✅
   → The taxonomy (symptom monitoring / error reporting / undetected-fault auditing; lead-time, prediction-window, precision/recall framework) that all later failure-prediction papers implicitly use. **Cite this for your evaluation protocol; most 2020s papers report metrics Salfner already showed are insufficient without lead time and warning window.**
6. **Fault prediction under the microscope: a closer look into HPC systems** — Ana Gainaru, Franck Cappello, Marc Snir, William Kramer. *SC 2012*, art. 77. DOI 10.1109/SC.2012.57. ✅ *(note: the commonly mis-cited title "…a closed-loop approach" is wrong — verified)*
   → The SC-venue ancestor of HPC failure prediction; signal-analysis + data-mining hybrid on Blue Waters/LANL-class logs. **Direct SC lineage — cite this to show you know the venue's own history.**
   → Evolution of line 2: Sahoo'03 → Liang'07 → Gainaru'12 → Time Machine (DSN'23, generative + lead time) → HiMFP/Cordial (DSN'23/'25, hierarchical hardware-level) → uncertain-positive-learning under auto-mitigation (ISSRE'24).

### Line 3 — System log analytics (the DSN/SC log-mining lineage)
7. **What Supercomputers Say: A Study of Five System Logs** — Adam J. Oliner, Jon Stearley. *DSN 2007*, pp. 575–584. DOI 10.1109/DSN.2007.103. ✅
   → Released the BGL/Thunderbird/Spirit/Liberty/RedStorm logs. **This single paper created the HPC log-analytics benchmark ecosystem still used in 2026.**
8. **Detecting large-scale system problems by mining console logs** — Wei Xu, Ling Huang, Armando Fox, David A. Patterson, Michael I. Jordan. *SOSP 2009*, pp. 117–132. DOI 10.1145/1629575.1629587. ✅
   → Source-code-informed log parsing + PCA on state-ratio vectors. The methodological root of "parse → featurize → detect".
9. **Mining Invariants from Console Logs for System Problem Detection** — Jian-Guang Lou, Qiang Fu, Shengqi Yang, Ye Xu, Jiang Li. *USENIX ATC 2010*. ✅
   → Linear invariants over log-event counts; the interpretable branch that deep methods later abandoned (and that 2024–25 papers are re-discovering, e.g. "Try with Simpler").
10. **Advances and challenges in log analysis** — Adam J. Oliner, Archana Ganapathi, Wei Xu. *CACM* 55(2):55–61, 2012. DOI 10.1145/2076450.2076466. ✅
    → The agenda-setting survey; states the problems (heterogeneity, lack of labels, non-stationarity) that are *still* the open problems in 2026.
11. **Experience Report: System Log Analysis for Anomaly Detection** — Shilin He, Jieming Zhu, Pinjia He, Michael R. Lyu. *ISSRE 2016*, pp. 207–218. DOI 10.1109/ISSRE.2016.21. ✅
    → First systematic comparison of six log-AD methods on HDFS+BGL. The benchmark discipline that led to Loghub.
12. **Drain: An Online Log Parsing Approach with Fixed Depth Tree** — Pinjia He, Jieming Zhu, Zibin Zheng, Michael R. Lyu. *ICWS 2017*, pp. 33–40. DOI 10.1109/ICWS.2017.13. ✅
    → The default template extractor for the entire field; still the baseline in ISSRE 2024–25 LLM-parser papers (CSLParser, Self-Evolutionary Group-wise Log Parsing).
13. **Tools and benchmarks for automated log parsing** — Jieming Zhu, Shilin He, Jinyang Liu, Pinjia He, Qi Xie, Zibin Zheng, Michael R. Lyu. *ICSE-SEIP 2019*, pp. 121–130. DOI 10.1109/ICSE-SEIP.2019.00021. ✅
    → Logparser benchmark; → Loghub (ISSRE 2023) → Loghub-2.0 (2024, `UNVERIFIED`).
14. **DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning** — Min Du, Feifei Li, Guineng Zheng, Vivek Srikumar. *CCS 2017*, pp. 1285–1298. DOI 10.1145/3133956.3134015. ✅
    → LSTM next-event prediction + workflow model; the deep-log ancestor.
15. **LogBERT: Log Anomaly Detection via BERT** — Haixuan Guo, Shuhan Yuan, Xintao Wu. *IJCNN 2021*, pp. 1–8. DOI 10.1109/IJCNN52387.2021.9534113. ✅
    → Masked-log-key modelling; the transformer branch. Evolution: DeepLog'17 → LogBERT'21 → NeuralLog / parser-free (2021, `UNVERIFIED`) → LLM-based (LLMeLog, LogRAG, LogLM, R-Log, 2024–25). **The line has plateaued: 2024–25 papers report gains on the same 2007 BGL logs. That is exploitable.**

### Line 4 — Large-scale field failure studies
16. **A large-scale study of failures in high-performance computing systems** — Bianca Schroeder, Garth A. Gibson. *DSN 2006*, pp. 249–258. DOI 10.1109/DSN.2006.5. ✅
    → The **LANL failure dataset** (22 systems, 9 years); founded the Computer Failure Data Repository (CFDR). *The archetype of the SC/DSN field-failure-study paper.*
17. **Failure Trends in a Large Disk Drive Population** — Eduardo Pinheiro, Wolf-Dietrich Weber, Luiz André Barroso. *FAST 2007*, pp. 17–28. ✅ (with Schroeder & Gibson's companion FAST'07 disk study, `UNVERIFIED key`)
    → Established that SMART is a weak failure predictor — the finding that "Making Disk Failure Predictions SMARTer!" (FAST'20) revisits 13 years later.
18. **DRAM errors in the wild: a large-scale field study** — Bianca Schroeder, Eduardo Pinheiro, Wolf-Dietrich Weber. *SIGMETRICS/Performance 2009*, pp. 193–204. DOI 10.1145/1555349.1555372. ✅
    → Ancestor of every DRAM/HBM failure-prediction paper: HiMFP (DSN'23), Investigating Memory Failure Prediction Across CPU Architectures (DSN'24), DDR5 Faults in the Field + Cordial (DSN'25).
19. **Characterizing cloud computing hardware reliability** — Kashi Venkatesh Vishwanath, Nachiappan Nagappan. *SoCC 2010*, pp. 193–204. DOI 10.1145/1807128.1807161. ✅
    → The cloud-side sibling; started the "hyperscaler publishes its fleet statistics" genre that Meta/Microsoft/Alibaba continue on the DSN industry track.
20. **Lessons Learned from the Analysis of System Failures at Petascale: The Case of Blue Waters** — Catello Di Martino, Zbigniew T. Kalbarczyk, Ravishankar K. Iyer, Fabio Baccanico, Joseph Fullop, William Kramer. *DSN 2014*, pp. 610–621. DOI 10.1109/DSN.2014.62. ✅
    → The definitive petascale field study; cross-layer (hardware + system software + application) failure attribution. **This is the closest historical ancestor of axis (A) and the model for what an SC field-study contribution looks like.**
21. **Failures in large scale systems: long-term measurement, analysis, and implications** — Saurabh Gupta, Tirthak Patel, Christian Engelmann, Devesh Tiwari. *SC 2017*, art. 44. DOI 10.1145/3126908.3126937. ✅
    → Multi-system, multi-year ORNL study; establishes temporal/spatial failure correlation as first-class. **The SC-venue field-study template.**
22. **A large-scale study of soft-errors on GPUs in the field** — Bin Nie, Devesh Tiwari, Saurabh Gupta, Evgenia Smirni, James H. Rogers. *HPCA 2016*, pp. 519–530. DOI 10.1109/HPCA.2016.7446091. ✅
    → GPU field-reliability ancestor (Titan). Companion: Tiwari et al., "Understanding GPU errors on large-scale HPC systems and the implications for system design and operation," *HPCA 2015* — `UNVERIFIED` (dblp record returned 503 repeatedly; title/venue/year believed correct, confirm before citing).
    → Evolution: Nie'16/Tiwari'15 → Meta SDC papers (2021–22) → GPU-cluster AI-infra reliability (NSDI'24 Acme, ATC'24 SuperBench, DSN'25 Llama-3) → HBM prediction (Cordial, DSN'25).

### Line 5 — Datacenter/service diagnosis (the RCA ancestor)
23. **Pinpoint: Problem Determination in Large, Dynamic Internet Services** — Mike Y. Chen, Emre Kiciman, Eugene Fratkin, Armando Fox, Eric A. Brewer. *DSN 2002*, pp. 595–604. DOI 10.1109/DSN.2002.1029005. ✅
    → Request-path tracing + statistical fault localization. Ancestor of all trace-based microservice RCA (Eadro, Nezha, SparseRCA, DeST).
24. **Fingerprinting the datacenter: automated classification of performance crises** — Peter Bodík, Moisés Goldszmidt, Armando Fox, Dawn B. Woodard, Hans Andersen. *EuroSys 2010*, pp. 111–124. DOI 10.1145/1755913.1755926. ✅
    → Signature/fingerprint representation of a system-wide performance state — **the direct ancestor of "cluster-state fingerprinting" formulations, and a good frame for an HPC cross-layer state representation.**
    → Also in this line but `UNVERIFIED` here: Cohen, Goldszmidt, Kelly, Symons, Chase, "Correlating instrumentation data to system states," *OSDI 2004*; Nagaraj, Killian, Neville, "Structured comparative analysis of systems logs to diagnose performance problems," *NSDI 2012*; Huang et al., "Gray Failure: The Achilles' Heel of Cloud-Scale Systems," *HotOS 2017*.

**HPC performance-anomaly branch (essential, and often missed by DSN-only searches):**
25. **Online Diagnosis of Performance Variation in HPC Systems Using Machine Learning** — Ozan Tuncer, Emre Ates, Yijia Zhang, Ata Turk, Jim M. Brandt, Vitus J. Leung, Manuel Egele, Ayse K. Coskun. *IEEE TPDS* 30(4):883–896, 2019. DOI 10.1109/TPDS.2018.2870403. ✅
    → Supervised classification of *performance anomaly type* (network contention, CPU contention, memory bandwidth, orphan processes) from LDMS node telemetry on production HPC systems. **This is the strongest pre-2020 falsifier for axis (D) and part of (A). Any "slow-node diagnosis" SC submission must beat or extend Tuncer et al.** (Predecessor: Tuncer et al., ISC 2017 Best Paper, `UNVERIFIED`.)
26. Borghesi, Bartolini, Lombardi, Milano, Benini — autoencoder-based semi-supervised anomaly detection in HPC systems (AAAI/IAAI 2019 and *Eng. Appl. of AI* 2019), and Borghesi et al., anomaly detection/anticipation in HPC, *IEEE TPDS* 2022. **`UNVERIFIED` — dblp record fetches returned 404/503.** Substantively: the ExaMon/Marconi (CINECA) line — per-node autoencoders trained on healthy telemetry. **This is the direct competitor for "node-level unsupervised anomaly detection on HPC telemetry" and must be checked before claiming novelty there.**

---

# PART C — NON-HPC AIOps BENCHMARK SET (what an SC submission is measured against)

Selected for "would be cited as closest work / would be used to say *already solved*". 22 items.

**C1. Predictive and Adaptive Failure Mitigation to Avert Production Cloud VM Interruptions (Narya)** — Sebastien Levy, Randolph Yao, Youjiang Wu, Yingnong Dang, Zheng Mu, Tarun Ramani, Naga Govindaraju, Xukun Li, Gil Lapid Shafriri, Murali Chintalapati (Microsoft Azure); Peng Huang (JHU); Pu Zhao, Qingwei Lin (MSR) | 2020 | **OSDI 2020**, pp. 1155–1170 | ✅ verified
Problem: avert VM interruptions by acting on predicted host failures. Data: Azure multi-layer host signals. Method: prediction + **online experimentation / bandit-RL to choose mitigation action**. Eval: **15 months in production, 26% reduction in VM interruptions.**
**L4+L6+L7 | D5 | P1.** → **The strongest single falsifier for axis (F).** Anything you propose for closed-loop HPC remediation will be compared to Narya.

**C2. FIRM: An Intelligent Fine-grained Resource Management Framework for SLO-Oriented Microservices** — Haoran Qiu, Subho S. Banerjee, Saurabh Jha, Zbigniew T. Kalbarczyk, Ravishankar K. Iyer (UIUC) | 2020 | **OSDI 2020**, pp. 805–825 | ✅
Localizes SLO-violating microservices **and identifies the contended low-level resource** (CPU/mem/net/IO), then reprovisions via RL. **L3+L5+L7 | D1/D3 | P3.** → Falsifier for axis (A)+(D) *in the cloud*: "identify which resource is the bottleneck and act" is already an OSDI result.

**C3. Making Disk Failure Predictions SMARTer!** — Sidi Lu, Bing Luo, Tirthak Patel, Yongtao Yao, Devesh Tiwari, Weisong Shi | 2020 | **FAST 2020** | ✅
380,000 drives, 64 sites, 2 months; 0.95 F1 / 0.95 MCC at 10-day horizon. **L4 | D2 | P2.** → Sets the bar for "fleet-scale hardware failure prediction with a real horizon". Also the model for reporting MCC rather than F1 on imbalanced data — reviewers will expect that.

**C4. Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems** — Ruiming Lu, Erci Xu, Yiming Zhang, Fengyi Zhu, Zhaosheng Zhu, Mengtian Wang, Zongpeng Zhu, Guangtao Xue, Jiwu Shu, Minglu Li, Jiesheng Wu (SJTU/Alibaba/Xiamen) | 2023 | **FAST 2023** | ✅
248,000 drives / 10 months; found 304 fail-slow drives; isolating them cut p99.99 tail latency by 48%; released a labeled dataset (41K normal, 315 verified fail-slow). **L3+L5+L7 | D4/D5 | P1.** → **Strongest falsifier for axis (D) at the device level**, and one of very few works with a *validated* fail-slow ground-truth set.

**C5. IASO: A Fail-Slow Detection and Mitigation Framework for Distributed Storage Services** — Biswaranjan Panda, Deepthi Srinivasan, Huan Ke, Karan Gupta, Vinayak Khot, Haryadi S. Gunawi | 2019 | **USENIX ATC 2019** | ✅ *(pre-2020 anchor)*
39,000 nodes, 1.5+ years; peer-based timeout signals; isolates a slow node "within minutes"; 232 incidents / 1.02% annual fail-slow rate. **L3+L7 | D5 | P1.** → Establishes that **peer-comparison slow-node detection is a solved production technique.** Your HPC contribution cannot be "we compare a node to its peers".

**C6. Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems** — Haryadi S. Gunawi et al. (16 institutions incl. LANL, ANL, Utah, NetApp, Pure, Huawei, Twitter) | 2018 | **FAST 2018** | ✅ *(pre-2020 anchor)*
101 fail-slow incident reports; taxonomy of fault→symptom transformation and cascading. **L0 | D2 | P4.** → **The definitional paper for axis (D).** Note it already includes LANL and ANL (HPC) incidents — you cannot claim fail-slow in HPC is unstudied.

**C7. SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation** — Yifan Xiong, Yuting Jiang, Ziyue Yang, Lei Qu, Peng Cheng, Yongqiang Xiong, Lidong Zhou (MSR) + 13 Microsoft co-authors | 2024 | **USENIX ATC 2024, Best Paper** | ✅
Proactively benchmarks GPU hardware to find **gray failures** before they degrade training; a **Selector that optimizes validation scheduling under a time budget**; MTBI improved up to **22.61×**; deployed in Azure over **hundreds of thousands of GPUs for two years**.
**L2+L3+L6+L7 | D5 | P1.** → **Simultaneously the strongest falsifier for axis (D) on GPUs AND the closest thing that exists to axis (C)** (it explicitly trades validation cost against detection benefit). Read this before writing any telemetry-cost or GPU-gray-failure SC paper.

**C8. Characterization of Large Language Model Development in the Datacenter (Acme)** — Qinghao Hu, Zhisheng Ye, Zerui Wang, Guoteng Wang, Meng Zhang, Qiaoling Chen, Peng Sun, Dahua Lin, Xiaolin Wang, Yingwei Luo, Yonggang Wen, Tianwei Zhang | 2024 | **NSDI 2024**, pp. 709–729 | ✅
6-month GPU-datacenter trace; job-failure taxonomy; **fault-tolerant pretraining with failure diagnosis + recovery**. Released trace. **L0+L3+L4+L7 | D4 | P0.** → The reference "GPU cluster field study + operational system" paper.

**C9. MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs** — Ziheng Jiang et al. (ByteDance) + Yinmin Zhong, Xin Jin (PKU) | 2024 | **NSDI 2024**, pp. 745–760 | ✅
Full-stack diagnostic tooling for stability at 12,288 GPUs; 55.2% MFU. **L0+L3+L5+L7 | D5 | P0.** → Falsifier for "nobody does cross-layer diagnosis on huge GPU clusters" — ByteDance does, in production.

**C10. Automatic Root Cause Analysis via Large Language Models for Cloud Incidents (RCACopilot)** — Yinfang Chen, Huaibing Xie, Minghua Ma, Yu Kang, Xin Gao, Liu Shi, Yunjie Cao, Xuedong Gao, Hao Fan, Ming Wen, Jun Zeng, Supriyo Ghosh, Xuchao Zhang, Chaoyun Zhang, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, Tianyin Xu | 2024 | **EuroSys 2024** | ✅
Handler-matched diagnostic collection → root-cause category prediction → narrative explanation. Microsoft year-long incident dataset; RCA accuracy up to 0.766; the diagnostic-collection component in production **4+ years**. **L5+L6 | D4 | P1.** → **The reference point for axis (G).** Note the systems contribution is the *handler/evidence-collection* architecture, not the LLM.

**C11. Recommending Root-Cause and Mitigation Steps for Cloud Incidents using Large Language Models** — Toufique Ahmed, Supriyo Ghosh, Chetan Bansal, Thomas Zimmermann, Xuchao Zhang, Saravan Rajmohan | 2023 | **ICSE 2023** (arXiv 2301.03797) | ✅
40,000+ Microsoft incidents; zero-shot / fine-tuned / multi-task GPT-3.x; human evaluation by incident owners. **L5+L6 | D2/D4 | P1.** → Established the genre. Everything after it must add a systems mechanism, not a bigger model.

**C12. AIOpsLab: A Holistic Framework to Evaluate AI Agents for Enabling Autonomous Clouds** — Yinfang Chen, Manish Shetty, Gagan Somashekar, Minghua Ma, Yogesh Simmhan, Jonathan Mace, Chetan Bansal, Rujia Wang, Saravan Rajmohan | 2025 | arXiv 2501.06706 (Microsoft) | ✅ arXiv verified; conference venue `UNVERIFIED`
Deploys microservice environments, injects faults, generates workload, exports telemetry, and provides an agent-evaluation interface across the whole incident lifecycle ("AgentOps"). **L3–L7 | D1 | P4.** → **The benchmark against which agentic-ops claims are now judged. There is no HPC equivalent — that gap is itself a contribution opportunity.**

**C13. The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems** — Lei Zhang, Zhiqiang Xie, Vaastav Anand, Ymir Vigfusson, Jonathan Mace | 2023 | **NSDI 2023**, pp. 321–339 | ✅
Retroactive trace sampling: buffer everything cheaply, persist only when a symptom fires ("dash-cam"). **L0 | D1 | P3.** → **The most important prior work for axis (C).** It solves *trace* cost-vs-coverage. It does **not** solve "which telemetry channels at what rate, subject to a budget, to maximize downstream detection/RCA quality" — that gap is real.

**C14. Just-In-Time Checkpointing: Low Cost Error Recovery from Deep Learning Training Failures** — Tanmaey Gupta, Sanjeev Krishnan, Rituraj Kumar, Abhishek Vijeev, Bhargav Gulavani, Nipun Kwatra, Ramachandran Ramjee, Muthian Sivathanu (Microsoft) | 2024 | **EuroSys 2024** | ✅
Checkpoint only on failure detection, exploiting determinism. **L7 | D3/D4 | P2.** → Falsifier for "recovery-action cost" framings in GPU training.

**C15. Silent Data Corruptions at Scale** — Harish Dattatraya Dixit, Sneha Pendharkar, Matt Beadon, Chris Mason, Tejasvi Chakravarthy, Bharath Muthiah, Sriram Sankar (Meta) | 2021 | arXiv 2102.11245 | ✅
Hundreds of thousands of machines, 18+ months; hundreds of SDC-affected CPUs from silicon defects. **L0+L3 | D4 | P0.**

**C16. Detecting silent data corruptions in the wild** — Harish Dattatraya Dixit, Laura Boyle, Gautham Vunnam, Sneha Pendharkar, Matt Beadon, Sriram Sankar (Meta) | 2022 | arXiv 2203.08989 | ✅
**Fleetscanner** (out-of-production testing) vs **Ripple** (in-production testing); 3+ years of experience; explicit **cost/coverage trade-off between the two regimes**. **L0+L3 | D5 | P0.** → Also relevant to axis (C): this is a real "detection cost vs coverage" analysis, just for SDC rather than telemetry.

**C17. Cores that don't count** — Peter H. Hochschild, Paul Turner, Jeffrey C. Mogul, Rama Govindaraju, Parthasarathy Ranganathan, David E. Culler, Amin Vahdat (Google) | 2021 | **HotOS XVIII** | `UNVERIFIED` (ACM DL blocked; title/venue/year high confidence)
Google's counterpart to C15: "mercurial cores". → Together C15–C17 make **"SDC exists at fleet scale" a closed question**; only detection/attribution methods remain open.

**C18. Understanding Recommendation System Robustness Against Silent Data Corruption: An Empirical Study** — Dongning Ma, Xun Jiao, Fred Lin, Daniel Moore, Sriram Sankar (Villanova + Meta) | 2025 | **ISSRE 2025**, Best Paper Candidate | ✅
→ Shows the SDC line has moved from "does it happen" to "which workloads care".

**C19. Large-Scale AI Infra Reliability: Challenges, Strategies, and Llama 3 Training Experience** — Jiao, Pandey, Pattabiraman, Lin (Meta + UBC) | 2025 | **DSN 2025 industry track** | ✅ → see A.2.

**C20. LLMPrism: Black-box Performance Diagnosis for Production LLM Training Platforms** — Jiang, Ren, Yu, et al. | 2025 | **DSN 2025 industry track** | ✅ → see A.2. **The closest existing work to axis (A) on GPU clusters.**

**C21. Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data** — Cheryl Lee, Tianyi Yang, Zhuangbin Chen, Yuxin Su, Michael R. Lyu | 2023 | **ICSE 2023** (arXiv 2302.05092) | abstract ✅ verified, venue/authors `UNVERIFIED` via fetch
Joint anomaly detection + root-cause localization from traces + logs + KPIs via multi-task learning. **L3+L5 | D1/D2 | P3.** → Companion falsifier for axis (A) alongside "Too Many Cooks".

**C22. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics** — Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu | 2023 | **ISSRE 2023** | ✅
→ The de-facto benchmark. **Contains BGL/Thunderbird/Spirit (2007-era HPC logs). A new, modern, released HPC telemetry corpus is one of the most durable SC contributions available to you** — Loghub's own citation count shows how much a dataset is worth.

**Additional items believed relevant but `UNVERIFIED` in this environment** (ACM DL blocked — confirm before citing): Nezha (multi-modal fine-grained microservice RCA, ESEC/FSE 2023); Sage (Gan, Liang, Dev, Lo, Delimitrou, ASPLOS 2021); Nenya (cost-aware RL failure mitigation, KDD 2022); "NVMe SSD Failures in the Field: the Fail-Stop and the Fail-Slow" (Lu et al., USENIX ATC 2023); Mint (cost-efficient tracing, ASPLOS 2024); "Exploring LLM-based Agents for Root Cause Analysis" and "X-lifecycle Learning for Cloud Incident Management" (FSE 2024 industry); "Labeling the Invisible: A Scalable Framework for Labeling Fail-Slow Failures in Cloud Storage Systems" (Zhao, Sun, Zhang et al. — NKU list says **FAST '27**, which is almost certainly FAST '26; year `UNVERIFIED`, but note this is the **fail-slow labeling** problem, i.e. it directly attacks the ground-truth gap in axis D+E).

---

# PART D — NOVELTY FALSIFICATION BY AXIS

For each axis: the work a reviewer would cite to say "already solved", how strong that argument is, and the verdict.

---

### (A) Cross-layer performance-degradation RCA combining CPU/GPU/network/storage/scheduler telemetry
**Strongest "already solved" citations, in order of danger:**
1. **"Too Many Cooks" (ISSRE 2025, Best Paper Candidate)** — argues empirically that **adding data sources yields diminishing or negative returns** for failure diagnosis. This is the *hardest* attack: it does not say your problem is solved, it says your premise may be wrong. **Danger: HIGH.**
2. **FIRM (OSDI 2020)** — cross-resource contention localization + action, in production-grade evaluation. "Identify which layer is the bottleneck" is an OSDI-2020 result. **Danger: HIGH for the framing, LOW for the HPC instance.**
3. **LLMPrism (DSN 2025 industry)** — black-box cross-layer performance diagnosis on a *production LLM training platform* (i.e., a real GPU cluster). **Danger: HIGH and rising** — this is the nearest neighbour and it is one year old.
4. Eadro (ICSE 2023), Nezha (FSE 2023 `UNVERIFIED`), Sage (ASPLOS 2021 `UNVERIFIED`), Fault Localization Using Interventional Causal Learning (DSN 2024 industry), ClusterRCA (ISSRE 2025, HPC but network-only), Blue Waters DSN 2014 (cross-layer but manual/retrospective).

**Argument strength that it is already solved: STRONG for cloud microservices; WEAK for HPC batch systems.** No published work performs joint RCA over {CPU counters, GPU/NVLink, IB/Slingshot, parallel filesystem, Slurm/PBS scheduler state, MPI collectives} on a leadership-class machine. The coupling mechanism in HPC — a *synchronous collective* that converts one slow rank into a system-wide stall, mediated by the scheduler's placement decisions — has no cloud analogue and is not modelled by any of the above.

**VERDICT: PARTIALLY_ADDRESSED.** Open specifically at: (i) collective-synchronization-aware attribution; (ii) scheduler/placement as a *causal variable* rather than metadata; (iii) shared-PFS interference across concurrent jobs.
**Required defence in the paper:** you must directly answer "Too Many Cooks" with an ablation showing which sources are load-bearing for *which* fault classes, and you must position against LLMPrism.

---

### (B) Cross-system / cross-generation generalization (domain adaptation, distribution shift, concept drift)
**Strongest "already solved" citations:**
1. **"Investigating Memory Failure Prediction Across CPU Architectures" (DSN 2024 industry, Huawei)** — this is *literally* cross-architecture transfer of a hardware failure-prediction model. **Danger: VERY HIGH** if your axis-B instance is hardware failure prediction. Must be cited.
2. **ZeroLog (ISSRE 2025)** — *zero-label* generalizable cross-system log anomaly detection. **Danger: VERY HIGH** for the log instance.
3. **"Prepared for the Unknown: Adapting AIOps Capacity Forecasting Models to Data Changes" (ISSRE 2025)** — explicit concept-drift adaptation for AIOps models. **Danger: HIGH** for the drift framing.
4. LogTransfer (ISSRE 2020), "Share or Not Share?" (ISSRE 2022, Best Paper Candidate — asks exactly "can one model serve many systems"), EvLog (ISSRE 2023, drift across software versions), CTF (INFOCOM 2020), transfer-learning KPI work (JSAC 2022, TOSEM 2023), Poenaru-Olaru et al. on drift detectors for AIOps (`UNVERIFIED`, IEEE BigData 2022).

**Argument strength: STRONG for logs and KPIs — this sub-problem has been worked hard for six years and a pure method contribution will be rejected.** It is **MODERATE** for hardware/RAS (the DSN 2024 Huawei paper exists but covers CPU architectures, not accelerator generations) and **WEAK** for the HPC-specific instance: transferring an operational model across *supercomputer generations* where the vendor, interconnect topology, accelerator, scheduler, and RAS vocabulary all change simultaneously, and where you have exactly one machine of each generation (N=1 per domain, which breaks standard domain-adaptation assumptions).

**VERDICT: PARTIALLY_ADDRESSED.** The ML-methods path is effectively closed. What is open: **the N=1-per-domain regime and telemetry-schema mismatch across procurement generations.** Frame it as a *systems and measurement* problem (how do you even align telemetry semantics across two vendors' RAS taxonomies?), not as a domain-adaptation-algorithm problem.

---

### (C) Telemetry cost vs downstream detection/RCA quality as a constrained optimization
**Strongest "already solved" citations:**
1. **SuperBench (ATC 2024, Best Paper)** — its *Selector* explicitly optimizes which validation benchmarks to run under a time budget, trading validation cost against defect-detection benefit, at 100K+ GPU scale. **Danger: HIGH** — this is the closest formulation that exists, and it is a best paper. But note: it optimizes *active validation* scheduling, not *passive telemetry* collection.
2. **Hindsight (NSDI 2023)** — retroactive sampling; solves cost-vs-coverage for distributed tracing by deferring the retention decision. **Danger: HIGH** for the tracing sub-case, **LOW** for multi-channel telemetry.
3. **fKPISelect (ISSRE 2023)** — fault-injection-driven automated KPI *selection* for multivariate anomaly detection. **Danger: MODERATE-HIGH** — this is "pick the telemetry that matters, validated by injected faults", which is a large part of your axis. Cite it; it is under-known.
4. **"Hardware Telemetry at Scale: SSDs Endurance Monitoring in Datacenters" (DSN 2025 industry, Meta)** — a real cost-of-telemetry-at-scale case study. **Danger: MODERATE** (case study, no optimization formulation).
5. Sifter (SoCC 2019), Mint (ASPLOS 2024, `UNVERIFIED`), ParaVerser (DSN 2025, cost-aware fault detection), and Meta's Fleetscanner-vs-Ripple cost/coverage analysis (C16).

**Argument strength that it is already solved: WEAK.** Every item above optimizes *one* channel (traces, or validation runs, or KPI subset) against *one* proxy objective. **Nobody has formulated the joint problem**: given a per-node telemetry budget (bytes/s, CPU %, storage $), choose sampling rates and channel subsets across heterogeneous sources (RAS, hardware counters, IB counters, PFS stats, scheduler events, job logs) to maximize a *measured downstream* objective (detection lead time, RCA top-k accuracy) — with an evaluation showing the Pareto frontier and where the current default configuration sits on it.

**VERDICT: STILL_OPEN — the strongest of your seven axes.** It is also the axis where HPC has a genuine structural advantage: HPC sites actually control the full telemetry stack (LDMS, RAS, Slurm, Lustre/GPFS, Redfish), whereas cloud AIOps papers inherit whatever the platform emits. Additional strength: this axis produces an artifact (a measured cost/quality Pareto frontier for a real supercomputer) that is durable regardless of which model wins.
**Caveat:** you must position explicitly against SuperBench's Selector, or a reviewer who knows it will call it a re-derivation.

---

### (D) Slow-node diagnosis: GPU vs CPU vs network vs I/O vs interference
**Strongest "already solved" citations:**
1. **Tuncer et al., TPDS 2019** — supervised ML *classification of the type* of HPC performance anomaly (network contention, CPU contention, memory-bandwidth, orphan process) from node telemetry, evaluated on production HPC systems. **Danger: VERY HIGH — this is your axis, in HPC, already done, seven years ago.** If you do not cite and beat this, the paper fails review.
2. **SuperBench (ATC 2024)** — gray-failure detection on a production GPU fleet; **Danger: VERY HIGH for the GPU sub-case.**
3. **Perseus (FAST 2023) + IASO (ATC 2019) + Fail-Slow at Scale (FAST 2018)** — device-level fail-slow detection and slow-node isolation are production-solved. **Danger: HIGH for "detection", LOW for "attribution".**
4. **LLMPrism (DSN 2025)**, **Acme (NSDI 2024)**, **MegaScale (NSDI 2024)** — GPU-cluster slow-node diagnosis in production. **Danger: HIGH.**
5. **"Effective Node-Level Anomaly Detection in HPC Systems via Coarse-Grained Clustering" (SC 2025, Sibo Xia, Yongqian Sun et al.)** — **Danger: VERY HIGH and most recent; it is at your target venue.** Must be obtained and read first.
6. Borghesi et al. (CINECA autoencoder line, `UNVERIFIED`) — per-node unsupervised anomaly detection on HPC telemetry.

**Argument strength: VERY STRONG for detection; STRONG for GPU gray failure; MODERATE for layer attribution under concurrency.** The remaining genuine gap is narrow and must be stated precisely: **disambiguating "this node is slow because of its own hardware" from "this node is slow because a co-scheduled job is saturating the shared PFS / the same IB switch"** — i.e., separating *intrinsic* fail-slow from *induced* interference, in a multi-tenant batch system, without a controlled experiment. Tuncer et al. treats contention as a *label class*; it does not attribute contention to a specific neighbouring job. Perseus/IASO operate in environments where peer comparison is valid because peers run identical workloads — an assumption that **fails** in an HPC batch system.

**VERDICT: PARTIALLY_ADDRESSED, bordering CLOSED for detection; STILL_OPEN only for interference-vs-intrinsic attribution under multi-tenancy.** Do not submit "we detect slow nodes". Submit "we attribute slowness to a layer *and to a responsible co-tenant*, and we validate the attribution against controlled injections."

---

### (E) Label-scarce operational learning (weak labels from tickets, RAS events, maintenance records)
**Strongest "already solved" citations:** an unusually deep bench, almost all at ISSRE:
- Robust KPI Anomaly Detection with **Partial Labels** (ISSRE 2021); **PU learning** for traces — PUTraceAD (ISSRE 2022); **label-free deployment** — AutoKAD (ISSRE 2023); **active learning** — AFALog (ISSRE 2023), LogCAE (ISSRE 2024), Active-MTSAD (DSN 2022); **semi-automatic labeling tooling** — LabelEase (ISSRE 2024); **zero-label cross-system** — ZeroLog (ISSRE 2025); **uncertain-positive learning under auto-mitigation** — Li et al. (ISSRE 2024); **fault injection as a label generator** — Campos & Costa (ISSRE 2020, ISSRE 2023), fKPISelect (ISSRE 2023); LogClass partial labels (TNSM 2020).

**Argument strength: VERY STRONG methodologically.** Weak supervision, PU learning, active learning and label-free deployment are, at this point, standard equipment. **A paper whose contribution is a label-efficiency technique will be rejected as incremental.**

**What remains genuinely open** is *not* the learning algorithm but the **label semantics**: in HPC the candidate weak-label sources (RAS event severities, Slurm job exit codes, node drain/DOWN reason strings, maintenance tickets, user "my job was slow" complaints) are **mutually inconsistent and none of them is ground truth**. No published work quantifies the agreement between these sources on a real supercomputer, or measures how much downstream model quality is destroyed by their disagreement. The one paper attacking this head-on elsewhere is the fail-slow *labeling* work from NKU/FAST (`UNVERIFIED` year) — which confirms the problem is recognized as important, and that the HPC version is unclaimed.

**VERDICT: PARTIALLY_ADDRESSED — methods CLOSED, label-semantics STILL_OPEN.** Reframe from "learning with few labels" to "**what is a label, in an HPC operations context, and how wrong are the ones we have?**" That is a measurement contribution and it is defensible.

---

### (F) Safe automated remediation (drain/reroute/reschedule/restart) with confidence and rollback
**Strongest "already solved" citations:**
1. **Narya (OSDI 2020)** — predictive, confidence-gated, adaptively-learned mitigation in production for 15 months with a measured 26% improvement. **Danger: VERY HIGH.** This is the axis, done, at OSDI, in a hyperscaler.
2. **"Can We Trust Auto-Mitigation?" (ISSRE 2024)** — identifies and addresses the label-corruption consequence of running closed-loop mitigation. **Danger: HIGH** — it means "we noticed the closed loop breaks evaluation" is also taken.
3. **SuperBench (ATC 2024)** — validate→isolate→repair loop at GPU-fleet scale. **Danger: HIGH.**
4. **Perseus (FAST 2023)** — detect→isolate, with a measured downstream benefit (48% p99.99 reduction). **Danger: MODERATE-HIGH.**
5. Just-In-Time Checkpointing (EuroSys 2024); Nenya (KDD 2022, `UNVERIFIED`); Microreboot (OSDI 2004) as the conceptual ancestor.

**Argument strength: VERY STRONG for the concept; WEAK for the HPC instance.** The cloud action space (migrate VM, drain host, live-migrate, restart container) is *cheap and reversible*, which is exactly what makes bandit/RL exploration ethical there. **The HPC action space is not**: draining a node mid-job kills the job; requeuing costs hours of allocation; rerouting an IB fabric perturbs every tenant; the "rollback" of a killed 4000-node job does not exist. **No published work has a cost model for remediation in a batch-scheduled, allocation-accounted, checkpoint-dependent environment**, and no HPC system has been demonstrated at D5.

**VERDICT: STILL_OPEN for HPC, but only if the contribution is the cost model and the safety envelope, not the policy learner.** Concretely defensible framings: (i) an action-cost model denominated in node-hours and queue-delay rather than "incidents"; (ii) a confidence threshold derived from the *asymmetric* cost of a false drain vs. a missed failure, with the threshold *derived* rather than tuned; (iii) shadow-mode (D3) evaluation against operator decisions with an explicit counterfactual accounting. **Expect the reviewer question "why is this not Narya with a different action set?" — answer it in the introduction, not the related work.**

---

### (G) LLM/agent-based operations with an actual systems contribution
**Strongest "already solved" citations:** the field is saturated. In two years: RCACopilot (EuroSys 2024), Ahmed et al. (ICSE 2023), LLM incident triage (ISSRE 2024), AetherLog (ISSRE 2025), LLMeLog / LogRAG / LogCAE / CSLParser / Self-Evolutionary Log Parsing (ISSRE 2024–25), LogLM (ICSE 2025), R-Log (ICSE-SEIP 2025), OpsEval (FSE 2025), FlowXpert (KDD 2025), TrioXpert (ASE 2025), plus 2026 acceptances already announced (FoundRoot/ICSE, KRCA/ASE, OpsAgent/ASE). And **AIOpsLab (2025)** now supplies the evaluation harness, which raises the bar: an agent paper without a benchmark comparison is no longer publishable.

**Argument strength: VERY STRONG.** "We prompted an LLM with our operational data and it worked better than a baseline" is a fully commoditized result. At SC specifically, an LLM-ops paper with no systems mechanism will be read as a workshop paper.

**VERDICT: ENGINEERING_ONLY as an axis on its own.** It becomes viable **only** when the contribution is a systems mechanism that happens to have an LLM inside it. Defensible mechanisms: (i) **cost-bounded evidence collection** — the agent must pay for telemetry it requests, connecting axis (G) to axis (C); (ii) **grounding/verification** — every claim the agent makes must be checkable against a telemetry query, with a measured hallucination rate on operational data; (iii) **action guards** — a formal envelope of permitted remediations with proofs or invariants, connecting to axis (F). RCACopilot's actual durable contribution was the handler-based evidence-collection architecture (4+ years in production), not the LLM. Copy that pattern.

---

## D.1 Ranked recommendation

| Rank | Axis | Verdict | Why |
|---|---|---|---|
| **1** | **(C) telemetry cost vs downstream quality** | **STILL_OPEN** | No joint formulation exists; HPC sites uniquely control the whole stack; yields a durable measured artifact; main risk is SuperBench's Selector |
| **2** | **(F) safe remediation, HPC cost model** | **STILL_OPEN** (conditional) | Narya closed the concept; HPC's irreversible, allocation-denominated action space is genuinely unmodelled |
| **3** | **(E) label semantics in HPC ops** | **PARTIALLY_ADDRESSED** — reframe as measurement | Methods closed; "how wrong are our labels" is unclaimed and testable |
| **4** | **(A) cross-layer RCA** | **PARTIALLY_ADDRESSED** | Open only for collective-sync + scheduler-as-cause; must pre-empt "Too Many Cooks" and LLMPrism |
| **5** | **(D) slow-node attribution** | **PARTIALLY_ADDRESSED**, near-closed for detection | Only interference-vs-intrinsic attribution under multi-tenancy remains; Tuncer TPDS'19 and SC'25 are hard blockers |
| **6** | **(B) cross-generation generalization** | **PARTIALLY_ADDRESSED** | Only the N=1-per-generation / telemetry-schema-mismatch framing survives; DSN'24 Huawei is a direct hit |
| **7** | **(G) LLM agents** | **ENGINEERING_ONLY** | Viable only as a carrier for a mechanism from (C) or (F) |

**Two cross-cutting observations.**
1. **The single most under-exploited asset is a released, modern, multi-layer HPC telemetry corpus.** The field is still benchmarking on Oliner & Stearley's 2007 BGL/Thunderbird/Spirit logs (via Loghub, ISSRE 2023). Loghub's influence shows what a dataset contribution is worth. A Hanggang-class corpus spanning RAS + hardware counters + interconnect + PFS + scheduler + job outcomes, with validated labels, would be cited for a decade and is immune to method obsolescence.
2. **Deployment depth, not method novelty, is the differentiator.** Across everything surveyed, D4/D5 (operator-workflow or closed-loop) papers are rare and almost exclusively industrial (Narya, Perseus, IASO, SuperBench, Azure auto-mitigation, Meta Ripple). **Almost no academic HPC operational-intelligence paper reaches beyond D2.** A KISTI submission that reaches D3 (shadow) or D4 (operator workflow) on a national supercomputer is, by itself, a stronger claim than any modelling improvement.

---

## E. KNOWN GAPS IN THIS CENSUS
1. **DSN 2020 and DSN 2021 full proceedings — NOT covered.** Retrieve from IEEE Xplore on an institutional network. Expect 3–8 additional in-scope papers.
2. **DSN 2026 / ISSRE 2026 — `PARTIAL / NOT YET PUBLISHED`.** ISSRE 2026 CFPs are open; monitor `issre.github.io/2026`.
3. **ACM DL / IEEE Xplore blocked** — the following are `UNVERIFIED` here and must be checked before citation: Nezha (FSE'23), Sage (ASPLOS'21), Nenya (KDD'22), NVMe SSD Failures in the Field (ATC'23), Mint (ASPLOS'24), Cores that don't count (HotOS'21), Tiwari et al. GPU errors (HPCA'15), Borghesi et al. (AAAI/IAAI'19, TPDS'22), Gunawi et al. SoCC'14/'16, Cohen et al. OSDI'04, Nagaraj et al. NSDI'12, Gray Failure HotOS'17, Schroeder & Gibson FAST'07.
4. **SC / HPDC / IPDPS / ICS were out of scope** but supply the two hardest falsifiers found (Gainaru SC'12, Gupta SC'17, and especially **"Effective Node-Level Anomaly Detection in HPC Systems via Coarse-Grained Clustering," SC 2025**). **A follow-up census of SC 2020–2025 is the single highest-value next step** — it is your target venue and it contains your nearest competitors.
5. One title correction worth propagating: the Gainaru et al. SC 2012 paper is **"Fault prediction under the microscope: a closer look into HPC systems"** — the widely circulated "…a closed-loop approach" variant is wrong.agentId: a91a23c1515c23aa3 (use SendMessage with to: 'a91a23c1515c23aa3', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 216772
tool_uses: 117
duration_ms: 1715184</usage>
> ## ⚠️ 정정 고지 (2026-09-06 추가)
>
> **이 문서의 일부 주장은 `09_ADVERSARIAL_NOVELTY_AUDIT.md`의 반례 탐색으로 반박(FALSIFIED)되거나 약화되었다.**
> 이 문서를 인용·활용하기 전에 반드시 **`09` §13의 문서별 정정표**를 먼저 확인할 것. 특히:
> - `09` §0.1 — **인용 자체가 틀린 항목 3건** (SC25 Aurora 저자·소속, 504-GPU 논문의 수치, Gleaner의 수치). **절대 그대로 쓰지 말 것**
> - `09` §0.2 — "65.7%" 수치 해석 오류 → overall 40.0% vs 1.4%
> - `09` §2 — "센터 주도 SC 본트랙 논문 0편" 주장 **FALSIFIED** (반례 9편). SC의 State of the Practice는 **Technical Papers 트랙 내 토픽 영역**이며 별개 트랙이 아니다
> - `09` §4 — telemetry 비용 관련 헤드라인 가설 **not novel**. retention 해상도 축만 무조건 생존
> - `09` §5 — cross-layer RCA 주장 **FALSIFIED as stated** (Beacon, NSDI'19)
> - `09` §7 — safe remediation 비용모델 주장 **FALSIFIED** (HPDC'24)
> - `09` §9 — **KISTI 국내 선행연구 16편**이 이 문서군에서 누락되어 있었다
>
> **후속 문서:** `08`(보존 요구사항) · `09`(반례 감사) · `10`(최종 후보 순위) · `11`(첫 실험 설계) · `12`(미확보 자료 watchlist)

# 04. Workshop · CUG · Center 운영 문제 인벤토리
## HPC AIOps / Operational Intelligence — 현장 운영자가 실제로 겪는 문제의 증거 기반 목록

**작성일:** 2026-09-06
**출처:** `D_workshops.md` (workshop ecosystem mining), `E_cug_vendor.md` (CUG + vendor audit), `H_centers.md` (center production evidence)
**성격:** 이 문서는 "무엇이 연구되었는가"가 아니라 **"운영자가 무엇 때문에 실패했는가"** 를 모은 1차 증거집이다. 영어 원문 인용은 운영자의 육성이며, 이 서베이 전체에서 가장 대체 불가능한 자산이다. 따라서 **원문을 그대로 보존**하고 한국어 주석을 덧붙인다.

**표기 규약 (원 소스의 마커를 그대로 승계):**

| 마커 | 뜻 |
|---|---|
| `VERIFIED` | 프로그램 페이지 / 출판사 TOC / proceedings 레코드에서 직접 확인 |
| `UNVERIFIED` | 확인 실패. "사실 아님"이 아니라 "모름" |
| `NOT FOUND` | 이번 조사 범위에서 찾지 못함 (부재의 증명 아님) |
| `PARTIAL` | 일부만 확인 |
| `PDF NOT POSTED` | 문헌은 존재하나 공개 PDF가 게시되지 않음 |
| `INFERRED` | 명시적으로 추론임 |
| ⚠️ | archival 공백이면서 가치가 높은 지점 |

**성숙도 코드 (Part 3에서 사용):**
`L0` 수집 · `L1` 시각화 · `L2` 규칙 알람 · `L3` 이상탐지 · `L4` 예측 · `L5` RCA · `L6` 추천 · `L7` closed loop
`D0` 개념 → `D5` closed-loop production
`P0` synthetic · `P1` single-node/testbed · `P2` partial production trace · `P3` full production system · `P4` multi-system/multi-year production

---

# 1. 이 문서의 증거 등급 규칙

## 1.1 CUG / workshop / center 증거가 **뒷받침할 수 있는 것**

| # | 뒷받침 가능 | 근거 예시 |
|---|---|---|
| 1 | **운영 문제의 존재와 만연성 (existence & prevalence)** | ORNL이 39,437회 zero-yield screen 후 주간 checknode를 폐기했고, NERSC가 OST를 expected 대비 25–50% 느리다고 보고했고, LLNL/Sandia가 벤더 telemetry API가 100K–1M msg/s에서 무너졌다고 보고한 것 — 이는 실제 production 문제의 신뢰할 만한 1차 증거다. **연구 질문의 동기(motivation)로 사용하라.** |
| 2 | **아키텍처·설정의 ground truth** | 컴포넌트 이름, 데이터 흐름, retention 기본값, 샘플링 주기, API 거동. CUG2025 HPE tutorial(tut106)은 사실상 HPCM 1.13 모니터링 스택의 **공개 사양서**다. |
| 3 | **설계용 order-of-magnitude 스케일 파라미터** | ORNL 1.3 TB/day, NERSC 2M log msg/s, 300M messages/day, switch당 64K counters, PM counter 10 Hz vs telemetry 15 s. |
| 4 | **아무도 출판하지 않는 negative result** | *"Fluent Bit was unstable at high throughput"*, *"Graphite downsampling destroyed our long-term analysis"*, *"we do not recommend this algorithm in a production environment"*, *"mTE did not produce significant results"*. archival 학회에서는 거의 나오지 않는, 이례적으로 가치 높은 정보다. |
| 5 | **archival 제안에 대한 현실 검증(deployment reality check)** | Indiana University가 overhead를 이유로 DCGM을 거부한 것은, ML-for-HPC 논문들이 흔히 전제하는 가정에 대한 **직접적 반증**이다. |

## 1.2 **뒷받침할 수 없는 것**

| # | 뒷받침 불가 | 이유 |
|---|---|---|
| 1 | **방법의 효능(method efficacy) 주장** | CUG 논문은 precision/recall, baseline, ablation, 통계 검정을 거의 보고하지 않는다. corpus 최고 수준인 Frontier screening 논문조차 raw count만 보고하며 설계된 비교(designed comparison)가 아니다. |
| 2 | **재현성(reproducibility)** | 데이터셋이 사실상 공개되지 않는다. 대부분의 CUG telemetry 작업은 구조적으로 재현 불가능하다. |
| 3 | **peer-reviewed 지위** | **CUG "Paper" ≠ peer-reviewed archival.** CUG 2026 CFP 원문: 제출 유형은 **Paper** (*"full-length abstracts presenting novel results"*), **Presentation** (*"presentation-only… not requiring a final paper"*), **BoF**, **Tutorial**. 논문은 *"will be considered for publication in a ACM International Conference Proceedings Series"*, 그리고 *"publication in the proceeding may require an **additional round of reviews**."* → **CUG Paper는 채택된 초록 + 작성된 논문이며, 기본적으로 peer-reviewed archival publication이 아니다.** 특정 CUG 2024/2025 논문이 실제로 ACM ICPS에 실렸는지는 **UNVERIFIED**. |
| 4 | **벤더 성능 주장** | §6 참조. 기능명은 연구 결과가 아니다. |
| 5 | **사이트 간 일반화** | CUG2023 모니터링 논문이 직접 말한다: format divergence 때문에 *"there can't easily be a rule of thumb in one implementation that extends to the other."* |
| 6 | **완전성(completeness)** | 가장 많이 인용되는 artifact 여럿이 애초에 게시되지 않았다 — CUG2021 HPE AIOps 논문, CUG2021 Sandia system/application monitoring 논문, CUG2022 Fallout, CUG2023 Slingshot Dashboard tutorial, CUG2024 Swordfish 논문. **cug.org에서 못 찾았다는 사실로 "연구되지 않았다"를 추론하면 안 된다.** |

## 1.3 워크숍 측 추가 규칙 (D_workshops.md Part 0의 구조적 정정)

1. **SC 계열에 2026년 이전까지 ODA *workshop*은 없었다.** 2019–2025 SC/ISC의 ODA 활동은 **BoF 시리즈**였고 peer review가 없었다. `HPC-ODA 2026` (SC26)이 *"eight years of successful BoF sessions at SC and ISC"* 를 peer review로 전환하는 **1st** International Workshop on HPC Operational Data Analytics다. → **SC 측 ODA 커뮤니티는 8년간 운영 문제를 생산했으나 archival paper trail이 전혀 없다.**
2. **MODA가 유일하게 오래 운영된 peer-reviewed ODA 장소**이며, ISC 계열 Springer LNCS이고 규모가 **매우 작다** — 연 2–5편, 2020–2025 통틀어 **archival chapter 17편**. 이것이 "HPC operational data analytics"라는 이름을 가진 분야의 peer-reviewed corpus 전부다.
3. **FTXS는 SC25에 열리지 않았고**, SC26에서는 "Faults, Trustworthiness, and eXplainability for **AI Systems** at Scale"로 개명·재범위화되었다. 고전적 HPC resilience 워크숍 레인은 닫히는 중이다.

## 1.4 실무 규칙

> **CUG·workshop은 *practice evidence* 로 인용하라** — "operators at ORNL report X". ***validated method* 주장은 Crossref로 검증된 archival 논문에만 유보하라.** 둘이 어긋나는 지점, 그 불일치 자체가 논문이다.

---

# 2. Workshop operational problem inventory (P-A ~ P-P)

16개 문제 전부. 각 항목: **어디에 몇 년간 나타났는가 → 대표 논문(정확한 인용) → 현재 실무 상태 → archival 승격 여부**.

---

## P-A. 모든 센터가 자기 모니터링 스택을 따로 만든다; 표준 telemetry schema가 없다

| 항목 | 내용 |
|---|---|
| **출현** | MODA 2020–2026 (전 회차), ODA BoF SC19→SC25 (전 회차), HPCSYSPROS 2023/2024, HPC-ODA'26 CFP topic 3 |
| **대표 논문** | ① Terai, Yamamoto, Miura, Shoji — *An Operational Data Collecting and Monitoring Platform for Fugaku* — 2021 — MODA21 — LNCS 10.1007/978-3-030-90539-2_24<br>② Osborne, Palumbo, Huk, Adamson, Jones, Lester (ORNL) — *Advancing ODA Standardization Through an Open Source Dashboard* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724831<br>③ Piccinali & Benini (CSCS) — *EMOI: CSCS Extensible Monitoring and Observability Infrastructure* — 2024 — MODA24 lightning talk — no DOI<br>④ Whitney, Romanus, Davis, Bautista (NERSC/LBNL) — *Next-Generation Data Explanation: Bridging the Gap from Data Collection to Operational Data Analytics* — 2024 — MODA24 lightning talk — no DOI<br>⑤ Guimarães, Sankaran, Frings (JSC) — *Supporting HPC Users with LLview* — 2025 — MODA25 — LNCS 978-3-032-07612-0_4 |
| **State of practice** | LDMS (Sandia), DCDB (LRZ), Examon (CINECA/UniBo), LLview (JSC), PIKA (TUD), XDMoD (Buffalo), EMOI (CSCS), CEEMS (CNRS), 그리고 어디에나 있는 Prometheus+Grafana. **상호운용성 zero.** SC24 BoF 명시적 진술: *"HPC sites are duplicating efforts."* (사이트들이 같은 일을 중복하고 있다) |
| **Archival 승격** | **PARTIAL.** Netti et al., *A Conceptual Framework for HPC Operational Data Analytics*, **IEEE CLUSTER 2021**; *Operational Data Analytics in practice*, **Parallel Computing 113 (2022)**. **표준 schema를 정의·평가한 archival 논문은 없다.** EE HPC WG가 2023년부터 표준화를 추진했으나 **peer-reviewed output 0건**. |

---

## P-B. 텔레메트리 기반 노드/시스템 이상·결함 탐지

| 항목 | 내용 |
|---|---|
| **출현** | MODA20, MODA21, MODA22, MODA23, FTXS22, HPCSYSPROS23, MODA26 |
| **대표 논문** | ① Ozer, Netti, Tafani, Schulz — *Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_18<br>② Molan, Borghesi, Beneventi, Guarrasi, Bartolini — *An Explainable Model for Fault Detection in HPC Systems* — 2021 — MODA21 — 10.1007/978-3-030-90539-2_25<br>③ Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini — *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems* — 2022 — MODA22 — 10.1007/978-3-031-23220-6_18<br>④ Anton, Willemot, Gougeaud, Zertal (CEA) — *ML-Based Methodology for HPC Facilities Supervision* — 2023 — MODA23 — 10.1007/978-3-031-40843-4_23 |
| **State of practice** | production에서는 rule-based threshold, 연구에서는 ML. label이 sysadmin ticket에서 나오고 희소하기 때문에 분야가 unsupervised/semi-supervised로 이동했다. |
| **Archival 승격** | **YES — 승격에 성공한 유일한 문제.** Aksar et al., *Prodigy: Towards Unsupervised Anomaly Detection in Production HPC Systems*, **SC'23** (10.1145/3581784.3607076); Molan et al., *RUAD*, **FGCS 141 (2023)**; Ardebili et al., *Multi-level anomaly prediction in Tier-0 datacenter*, **ACM Computing Frontiers 2022**; Aksar et al. *Proctor* (**ISC'21**), *E2EWatch* (**Euro-Par'21**). |

---

## P-C. 이기종 log/syslog → actionable event

| 항목 | 내용 |
|---|---|
| **출현** | HPCSYSPROS20, FTXS22, HPCSYSPROS23, MODA26 |
| **대표 논문** | ① Lewis, Liu, Kettimuthu, Papka — *Log-Based Identification, Classification, and Behavior Prediction of HPC Applications* — 2020 — HPCSYSPROS20 — GitHub/Zenodo<br>② Egersdoerfer, Zhang, Dai — *ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection* — 2022 — FTXS22 — IEEE, pp. 1–10<br>③ Quan, Howell, Greenberg (LANL) — *Heterogeneous Syslog Analysis: There Is Hope* — 2023 — HPCSYSPROS23 — 10.1145/3624062.3624128 / 10.5281/zenodo.10223395<br>④ Mustiere (CEA) — *Enhancing Security in HPC Systems: A Clustering Approach for Filtering Weak Signals* — 2026 — MODA26 — proceedings pending |
| **State of practice** | 사이트별 grep + 수작업 regex "noise list". LANL 논문은 **LLM을 log classifier로 시험**하여 더 설명 가능하지만 계산 비용이 크다고 보고한 점에서 주목할 만하다. |
| **Archival 승격** | **LOW / NOT FOUND (HPC 계열 학회 기준).** log anomaly detection은 cloud/SE 세계(ICSE, FSE, DSN)에서 archival이지만, *HPC 고유의* heterogeneous-syslog 문제는 확인 가능한 SC/HPDC/IPDPS/Cluster regular paper가 없다. |

---

## P-D. 사용자에게 "당신 job이 비효율적이었다"고 알리기 (job-level efficiency reporting) ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | MODA23, MODA25, MODA26, HPCSYSPROS23, HPCSYSPROS24, SC25 ODA BoF poll |
| **대표 논문** | ① Winkler & Knüpfer (TU Dresden) — *Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA* — 2023 — MODA23 — 10.1007/978-3-031-40843-4_22<br>② Guimarães, Sankaran, Frings (JSC) — *Supporting HPC Users with LLview* — 2025 — MODA25 — 10.1007/978-3-032-07612-0_4<br>③ Guilbault (Université Laval) — *Self-service Monitoring of HPC and Openstack Jobs for Users* — 2023 — HPCSYSPROS23<br>④ Simakov (SUNY Buffalo) — *Benchmarking and Continuous Performance Monitoring of HPC Resources using the XDMoD Application Kernel Module* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724847<br>⑤ Ma et al. (NHR@FAU) — *Automatic Workload Characterization on Production HPC Systems via Roofline Telemetry* — 2026 — MODA26 |
| **State of practice** | 운영자 경험에서 손으로 튜닝한 heuristic threshold. PIKA는 TUD에서 5년 이상 가동, LLview는 JUWELS Cluster+Booster에서 production. **cross-site 검증 없음, "비효율"의 합의된 정의 없음.** |
| **Archival 승격** | **NOT FOUND. ⚠️ HIGH-VALUE GAP.** 정량 근거: SC25 ODA BoF poll (29명 응답) — 사용자는 운영 데이터의 가치를 **4.3/5**로 평가하지만, 그것을 활용할 자기 역량은 **2.9/5**로 평가했다. |

---

## P-E. Per-job energy accounting, power capping, energy budget control

| 항목 | 내용 |
|---|---|
| **출현** | MODA20, MODA24, MODA25, MODA26, EESP25, EESP26, JSSPP24, JSSPP25, Sustainable Supercomputing SC24/SC25 |
| **대표 논문** | ① Tracey, Hoang, Subelet, Elisseev (IBM) — *AI-Driven Holistic Approach to Energy Efficient HPC* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_17 `DOI UNVERIFIED`<br>② Paipuri (CNRS) — *Monitoring Energy and Emissions of HPC Batch Job Using CEEMS* — 2024 — MODA24 lightning talk<br>③ Prica & Zamuda — *Monitoring Energy Consumption of Workloads on HPC Vega* — 2025 — MODA25 — LNCS 978-3-032-07612-0<br>④ Angelelli, Carastan-Santos, Dutot — *Run your HPC jobs in Eco-Mode: revealing the potential of user-assisted power capping in supercomputing systems* — 2024 — JSSPP24 — LNCS 14591<br>⑤ Corbalan & Alonso (BSC) — *Static powercap vs EAR hard-powercap: Performance evaluation* — 2025 — JSSPP25 — LNCS 16210<br>⑥ Menear (NREL) — *Pre-runtime GPU Power Quantile Forecasting from Submission-Time Job Artifacts* — 2026 — MODA26 |
| **State of practice** | RAPL/IPMI/Redfish/DCGM 샘플링; BSC/CINECA에서 EAR 및 SLURM plugin이 production. **per-job attribution은 여전히 논쟁 중** (공유 PSU, 냉각 오버헤드, idle 배분). |
| **Archival 승격** | **YES, partially.** Karimi, Maiterth, Shin, Sattar, Lu, Wang, *Exploring the Frontiers of Energy Efficiency using Power Management at System Scale* (arXiv:2408.01552; Frontier, 3개월 telemetry, 최대 8.5% / 약 1,438 MWh 절감) — `venue beyond arXiv UNVERIFIED`. **그러나 per-job energy *attribution methodology* 에 대한 archival 논문은 없다.** |

---

## P-F. Facility 열/냉각 모델링과 데이터센터 digital twin

| 항목 | 내용 |
|---|---|
| **출현** | MODA22, Sustainable Supercomputing SC25, SC25 Digital Twins Workshop, HPC-ODA'26 CFP topic 6 |
| **대표 논문** | ① Egan, Purkayastha, Sickinger (NREL) — *Data Center Facility Monitoring with Physics Aware Approach* — 2022 — MODA22 — 10.1007/978-3-031-23220-6 (pp. 251–261)<br>② Seyedkazemi Ardebili et al. — *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems* — 2022 — MODA22 (실제 Marconi100 thermal emergency에 대해 검증)<br>③ SC25 Sustainable Supercomputing — "HPC digital twins for scheduling evaluation", "Microgrid optimization for data centers", "Small modular reactor performance for data centers" — 저자 귀속 `UNVERIFIED` (프로그램 페이지가 저자 없이 주제만 나열) |
| **Archival 승격** | **YES — 가장 명확한 성공 사례.** Brewer, Maiterth, Kumar, Wojda, Bouknight, Hines, Shin, Greenwood, Grant, Williams, Wang, *A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale*, **SC24 Technical Paper**, 10.1109/SC41406.2024.00029 (ExaDigiT; Frontier; 6개월 운영 데이터로 검증). |

---

## P-G. 부품 고장 예측 — disk, GPU, hardware error

| 항목 | 내용 |
|---|---|
| **출현** | FTXS23, FTXS24, HPCTESTS23, MODA26 |
| **대표 논문** | ① Hagerty, Webb, Melesse Vergara, Ezell (ORNL) — *Experiences Detecting Defective Hardware in Exascale Supercomputers* — 2023 — HPCTESTS23 — SC23 Workshops<br>② George, Hanley, Oral (ORNL) — *Disk Failure Trends in Alpine Storage System* — 2023 — FTXS23 short paper<br>③ George, Wang, Hanley, Ransom, Bent, Zimmer — *From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments* — 2024 — FTXS24 — IEEE SC-W 2024<br>④ Brown (ANL) — *Evaluating Forecasting Techniques for Hardware Errors on a Large-scale HPC System* — 2026 — MODA26 |
| **Archival 승격** | **GPU는 YES, HPC disk는 NOT FOUND.** GPU: Oles, Schmedding, Ostrouchov, Shin, Smirni, Engelmann, *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*, **ICS'24** — 10.1145/3650200.3656615 (27,648 V100; DBE가 동일 GPU에서 재발; 온도가 아니라 sustained power와 상관). HPC의 disk/parallel-filesystem 고장은 여전히 workshop-only 문헌이다. |

---

## P-H. Acceptance testing / continuous system testing / silent regression detection ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | FTXS21, HPCSYSPROS22, HPCTESTS23/24/25, HPCSYSPROS24, MODA25, MODA26. **2021–2026 매년.** |
| **대표 논문** | ① DeBardeleben, Burr, Penton, Walker, Loncaric, Jones — *Statistical Framework for Two-Party Acceptance Testing of HPC Systems for Reliability* — 2021 — FTXS21 — IEEE pp. 21–30<br>② Siddiqui, Palmer, Shende, Spear, Sambrekar, Xiang (NERSC/UO) — *An Automated Approach to Continuous Acceptance Testing of HPC Systems at NERSC* — 2022 — HPCSYSPROS22<br>③ Pearce, Scott, Becker, Haque, Hanford, Brink, Jacobsen, Poxon, Domke, Gamblin — *Toward Collaborative Continuous Benchmarking for HPC* — 2023 — HPCTESTS23 — SC23 Workshops<br>④ Jacobsen & Bird (Google) — *Ramble: A Flexible, Extensible, and Composable Experimentation Framework* — 2023 — HPCTESTS23<br>⑤ Siegmann, Carlson, Simakov, Curtis, Calder, Harrison — *What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years* — 2025 — MODA25 — LNCS 978-3-032-07612-0_5 (Ookami; 4년 이상; 500명 이상 사용자)<br>⑥ Guimaraes (JSC) — *Centralised Dashboard for Continuous Benchmarking: From HPC Clusters to Quantum Processors* — 2026 — MODA26 |
| **State of practice** | buildtest, ReFrame, Ramble, Benchpark, XDMoD Application Kernels — **전부 tool paper이고 methodology paper는 없다.** 모든 대형 센터가 조달(procurement)마다 acceptance suite를 새로 만든다. |
| **Archival 승격** | **NOT FOUND. ⚠️ 생태계 최대 공백.** 이 문제만을 위한 워크숍 시리즈(HPCTESTS, 현재 4회)가 존재함에도 SC/HPDC/IPDPS/Cluster/DSN regular paper가 **0편**이다. |

---

## P-I. Job runtime / queue-time / resource 예측의 스케줄링 반영

| 항목 | 내용 |
|---|---|
| **출현** | JSSPP 매년, MODA24, MODA25, MODA26 |
| **대표 논문** | ① Klusacek & Chlumsky — *Real-life HPC Workload Trace Featuring Refined Job Runtime Estimates* — 2024 — JSSPP24 — LNCS 14591<br>② Cui, Takahashi, Shimomura, Takizawa — *Clustering Based Job Runtime Prediction for Backfilling Using Classification* — 2024 — JSSPP24<br>③ Menear, Duplyakin, Konate (NREL/LBNL) — *How well can we predict two most important metrics for HPC jobs: runtime and queue time?* — 2024 — MODA24 lightning talk<br>④ Loreti, Leone, Borghesi — *Duration-Informed Workload Scheduler* — 2025 — MODA25 — LNCS 978-3-032-07612-0_1 (Marconi100 / M100 ExaData trace; **평균 대기시간 약 11% 감소**)<br>⑤ Oztop, Schwaller, Leung, Kulis, Egele, Coskun (BU + Sandia) — *Job Grouping Based Intelligent Resource Prediction Framework* — 2025 — JSSPP25 — LNCS 16210 |
| **Archival 승격** | **PARTIAL.** LNCS(JSSPP)에는 archival되지만 SC/IPDPS main track에는 드물다. **예측기를 production 스케줄러에 넣는 closed-loop deployment는 archival이 전무하다.** |

---

## P-J. 센터 규모 I/O 모니터링과 파일시스템 경합 원인 규명 ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | MODA20, MODA25, PDSW 매년, HPCSYSPROS24, SNTA24, PERMAVOST25 |
| **대표 논문** | ① Sivalingam & Richardson (HPE) — *Application IO Analysis with Lustre Monitoring Using LASSi for ARCHER* — 2020 — MODA20 — 10.1007/978-3-030-59851-8_16 (다년 ARCHER 데이터; scheduler job data와 Lustre metric을 조인)<br>② Paipuri (CNRS/IDRIS) — *A Unified I/O Monitoring Framework Using eBPF* — 2025 — MODA25 — 10.1007/978-3-032-07612-0_3 (VFS kernel function에 eBPF → Prometheus; production Lustre에서 IOR 대비 검증; overhead 무시 가능)<br>③ Kartik & Lockwood (VAST/Microsoft) — *Beyond the Hype: Uncovering the Real I/O Needs of LLMs* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.15724856<br>④ Masih, Liem, Kunkel — *Factors Impacting I/O Time Proportion in AI Workloads* — 2025 — PERMAVOST25 |
| **Archival 승격** | **characterization은 YES** (PDSW→SC 파이프라인이 잘 확립되어 있음). **"지금 누가 파일시스템을 느리게 만들고 있는가"에 대해서는 NOT FOUND** — production에서의 실시간 원인 귀속(culprit attribution)에 archival 논문이 없다. |

---

## P-K. 운영 데이터 거버넌스, 보존, 공개 데이터셋 릴리즈 ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | MODA24, SC24 BoF, SC25 BoF, HPC-ODA'26 CFP topic 3 |
| **대표 논문** | ① Widener, May, Singleton, Kuchar (ORNL) — *Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository* — 2024 — MODA24 — 10.1007/978-3-031-73716-9 (pp. 287–292)<br>② (dataset, workshop 아님) Borghesi/Bartolini et al. — *M100 ExaData: a data collection campaign on CINECA's Marconi100* — **Nature Scientific Data** 2023 — 10.1038/s41597-023-02174-3 |
| **State of practice** | 거의 모든 운영 telemetry가 공개 불가(보안, 사용자 프라이버시, 벤더 NDA). **SC25 BoF poll에서 공개 ODA 데이터셋 가용성은 1.6/5** — poll 최저점. |
| **Archival 승격** | 거버넌스/익명화 방법론에 대해 **NOT FOUND.** 데이터셋은 존재하지만(M100 ExaData, Fugaku, OLCF SMC data challenge), *어떻게* HPC 운영 데이터를 안전하게 공개하는가에 대한 archival 논문은 없다. |

---

## P-L. Login node / 공유 자원 남용 통제와 multi-tenancy ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | HPCSYSPROS 2023, 2024; MODA24 panel ("MODA in multitenant and federated environments", moderated by Utz-Uwe Haus, HPE) |
| **대표 논문** | ① McKay, Forrest, Fischer (Univ. of Utah) — *Dynamic Login Node Resource Control and Monitoring with Arbiter 3* — 2024 — HPCSYSPROS24 — 10.5281/zenodo.16541343<br>② Focht (Penn State) — *Democratizing Remote HPC Storage Access* — 2023 — HPCSYSPROS23<br>③ Maloney (NCSA) — *Transparent Global File System Access in Environments with Multiple Authentication Domains* — 2025 — HPCSYSPROS25 |
| **Archival 승격** | SC/HPDC/IPDPS에서 **NOT FOUND.** Arbiter의 archival 계보는 실무 학회인 **PEARC**에 있다. ⚠️ Gap. |

---

## P-M. Configuration drift, node image 일관성, 대규모 provisioning ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | HPCSYSPROS **2020–2025 매년** — 생태계에서 가장 끈질긴 단일 주제 |
| **대표 논문** | Allen, Ezell, Peltz, Jacobsen, Lueninghoener, Wofford, Roman — *Modernizing the HPC System Software Stack* (2020); Mickels — *Using xCAT and Git to Manage Node Software Consistency and DevOPs* (2022); Baker, Blaas, Tillotson (NCAR) — *Clushible: Tidal Wave-Like Configuration with Ansible* (2023); Trecakov, Von Wolff, Al-Tahat — *SStack* (2024); Glick — *Modernizing HPC Configuration Management* (2025); Kincl — *Exploring bootc for HPC Cluster Management* (2025); Anderson — *Provisioning to Disk with Warewulf v4* (2025) |
| **Archival 승격** | **어디에도 NOT FOUND. archival 연구 논문 0편.** ⚠️ Gap (다만 이는 연구가 아니라 엔지니어링 문제라는 반론이 가능하다 — *연구* 프레이밍은 drift 탐지와 그것의 job failure 상관관계이며, 이는 아무도 하지 않았다). |

---

## P-N. Cloud-native / Kubernetes 수렴

| 항목 | 내용 |
|---|---|
| **출현** | HPCSYSPROS 2021–2024, JSSPP25, SC26의 신규 ECHO 워크숍 |
| **대표 논문** | Knight — *Kubernetes for HPC Administration* (HPCSYSPROS21); Kincl & Bruszewski (Red Hat) — *Embracing Batch on Kubernetes* (HPCSYSPROS23); Gough & Lumas (Purdue) — *Kubernetes Resource Scaling via Batch Node Conversion on the Anvil Supercomputer* (HPCSYSPROS24, 10.5281/zenodo.16576621); Spišaková, Stoyanov, Hejtmánek, Klusacek, Reber, Bruno — *Kubernetes Scheduling with Checkpoint/Restore: Challenges and Open Problems* (JSSPP25) |
| **Archival 승격** | **PARTIAL** (CCGrid/HPDC에 converged-computing 논문 존재). 운영 특화 부분(production supercomputer에서의 동적 batch↔k8s node 전환)은 **NOT FOUND.** |

---

## P-O. 운영 데이터에서의 보안 태세와 weak-signal 탐지 ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | HPCSYSPROS22, HPCSYSPROS25, MODA26, S-HPC (SC25 4th, SC26 5th) |
| **대표 논문** | Deumens (UF) — *Cybersecurity Frameworks: NIST 800-171 and CMMC v2.0 Update* (HPCSYSPROS22); Rollins — *NIST SP 800-\* in HPC: Standards That Matter* (HPCSYSPROS25); Mustiere (CEA) — *Enhancing Security in HPC Systems: A Clustering Approach for Filtering Weak Signals* (MODA26) |
| **Archival 승격** | **NOT FOUND.** ⚠️ Gap. |

---

## P-P. Carbon-aware / sustainability 기반 운영 ⚠️

| 항목 | 내용 |
|---|---|
| **출현** | JSSPP25, EESP25/26, Sustainable Supercomputing SC24/25/26 |
| **대표 논문** | Benhari & Trystram — *Adaptive Carbon-Aware scheduling policies for HPC systems* (JSSPP25); Hossain, Abdurahman, Islam, Ahmed — *Power-Aware Scheduling for Multi-Center HPC Electricity Cost Optimization* (JSSPP25); Smith, Abt, Grant (Queen's) — *What A Waste* (EESP25, **Best Paper**); Tröpgen, Smejkal, Ilsche, Schöne, Schirmeier (TU Dresden) — *Pinpointing Idle-Power Regressions in Linux* (EESP25, LNCS pp. 205–218) |
| **Archival 승격** | HPC 특화로는 **NOT FOUND.** carbon-aware computing은 cloud 쪽에서 HotCarbon/ASPLOS/SOSP에 archival이지만, HPC 센터 변종(고정 capacity, migration 불가, national-grid 및 district-heating 결합)은 workshop-only다. ⚠️ Gap. |

---

## 2.x 요약: archival 승격 현황 한눈에

| 문제 | 승격 | 비고 |
|---|---|---|
| P-A schema 표준 | PARTIAL | 개념 프레임워크만 (CLUSTER'21) |
| P-B 노드 이상탐지 | **YES** | SC'23 Prodigy — 유일한 완전 승격 |
| P-C 이기종 syslog | NOT FOUND (HPC) | cloud/SE에는 있음 |
| **P-D job 비효율 리포팅** | **NOT FOUND ⚠️** | 최고 가치 공백 |
| P-E per-job energy | PARTIAL | attribution 방법론은 공백 |
| P-F facility/digital twin | **YES** | SC24 ExaDigiT |
| P-G 부품 고장 예측 | GPU YES / disk NOT FOUND | ICS'24 |
| **P-H acceptance testing** | **NOT FOUND ⚠️** | 생태계 최대 공백 |
| P-I runtime 예측 | PARTIAL | LNCS까지만 |
| P-J I/O 경합 귀속 | 특성화 YES / 실시간 귀속 NOT FOUND ⚠️ | |
| **P-K 데이터 거버넌스** | **NOT FOUND ⚠️** | poll 1.6/5 |
| **P-L login node 남용** | **NOT FOUND ⚠️** | PEARC까지만 |
| **P-M config drift** | **NOT FOUND ⚠️** | 어디에도 0편 |
| P-N cloud-native | PARTIAL | |
| **P-O 보안 weak signal** | **NOT FOUND ⚠️** | |
| **P-P carbon-aware** | **NOT FOUND ⚠️** | cloud만 있음 |

---

# 3. Workshop 최강 논문 20편

D_workshops.md Part 3의 프로파일 목록. L/D/P 코드와 SC-regular relevance를 원문대로 보존한다.

| # | 논문 / 저자 / 연도 / 장소 / DOI | 문제 · 데이터 · 방법 | 평가 규모 | L / D / P | SC-regular relevance |
|---|---|---|---|---|---|
| **1** | **An Operational Data Collecting and Monitoring Platform for Fugaku: System Overviews and Case Studies in the Prelaunch Service Period** — Terai, Yamamoto, Miura, Shoji (RIKEN R-CCS) | 2021 · MODA21 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-030-90539-2_24 | *Problem:* exascale 노드 수에서 application core를 뺏지 않고 telemetry 수집 · *Data:* logs, metrics, building-management sensors · *Method:* 3-tier pipeline → TSDB → dashboards; A64FX **redundant cores**를 수집에 사용 | Fugaku, **>150,000 compute nodes, full metric sweep in <20 s**, prelaunch 기간 | **L0–L1 / D4 / P3** | **HIGH — 10⁵ 노드급 exascale telemetry 아키텍처; 인용 가능한 scale baseline에 가장 가까움.** *Limits:* analytics layer 없음, failure/efficiency use case 없음 |
| **2** | **An Explainable Model for Fault Detection in HPC Systems** — Molan, Borghesi, Beneventi, Guarrasi, Bartolini (UniBo/CINECA) | 2021 · MODA21 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-030-90539-2_25 | sysadmin이 쓸 수 있는 설명을 갖춘 자동 노드 결함 탐지 · Examon holistic monitoring + 수작업 admin state label · supervised classification + explainability | CINECA Tier-0 production, **Apr–Jul 2019 (~4개월)**; deployed NO (offline) | **L3 / D2 / P3** | **HIGH — 이미 승격됨 (Lineage 참조).** *Limits:* supervised, label이 수작업이고 noisy |
| **3** | **Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems** — Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini | 2022 · MODA22 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-031-23220-6_18 | emergency shutdown 이전에 thermal hazard 탐지 · thermal monitoring signal · 의도적으로 ML이 아닌 복합 통계 rule set (operator-auditable) | **Marconi100 (CINECA), 실제 thermal emergency event로 검증** | **L2–L3 / D3 / P3** | **HIGH — injected anomaly가 아니라 실제 facility incident에 ground truth로 검증한 드문 사례.** *Limits:* rule 수작업 도출, 사이트 간 일반화 없음 |
| **4** | **Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA** — Winkler, Knüpfer (TU Dresden) | 2023 · MODA23 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-031-40843-4_22 | 아무도 사용자에게 job이 자원을 낭비한다고 말해주지 않는다 · 연속 job-level performance monitoring (PIKA) · 운영 경험에서 도출한 heuristic footprint check | **NHR centre at TU Dresden, 5년 이상 연속 production monitoring**; deployed **YES, production, 사용자와 admin 모두 사용** | **L2–L3 / D4 / P4** | **VERY HIGH — corpus에서 가장 강력한 un-promoted 논문.** *Limits:* heuristic이 ground truth로 검증되지 않음, cross-site transfer 없음, **archival 버전 없음** |
| **5** | **ML-Based Methodology for HPC Facilities Supervision** — Anton, Willemot, Gougeaud, Zertal (CEA) | 2023 · MODA23 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-031-40843-4_23 | 측정 계층을 가로지르는 facility 인프라 감독 · multi-level device 측정, 에너지를 예시로 · 3단계: cleaning → clustering (DBSCAN/HDBSCAN/agglomerative) + anomaly detection → custom visualization | CEA facilities, 규모·기간 `UNVERIFIED`; deployed `UNVERIFIED` | **L1–L3 / D2 / P2 `UNVERIFIED`** | MEDIUM. *Contribution:* 도구가 아닌 명시적 methodology. *Limits:* 평가가 얇음 |
| **6** | **A Fast Simulator to Enable HPC Scheduling Strategy Comparisons** — Wilkinson, Jones, Richardson, Dykes, Haus (HPE / UCL) | 2023 · MODA23 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-031-40843-4 pp. 320–333 | production 머신에서 스케줄링 정책을 A/B 테스트할 수 없다 · workload trace · fast discrete-event scheduling simulator | `UNVERIFIED`; deployed NO | **L6 / D1 / P2 `UNVERIFIED`** | **HIGH — "production을 망가뜨리지 않고 운영 정책 변경을 어떻게 평가하는가"는 미해결이며 출판 가능한 meta-problem.** *Limits:* simulator fidelity가 production 대비 미검증 |
| **7** | **Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository** — Widener, May, Singleton, Kuchar (ORNL) | 2024 · MODA24 · **[WORKSHOP-PEER-REVIEWED — short paper]** · 10.1007/978-3-031-73716-9 pp. 287–292 | 공개 data repository의 모니터링/분석, 무엇을 릴리즈할 수 있는가 포함 · repository access + system telemetry · experience report | ORNL leadership data repository | **L0–L1 / D3 / P3** | MEDIUM–HIGH (거버넌스가 archival로 다뤄지지 않음). *Limits:* 6쪽, 평가 없음 |
| **8** | **An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads** — Hunhold, Wesner (University of Cologne) | 2024 · MODA24 · **[WORKSHOP-PEER-REVIEWED — full paper]** · 10.1007/978-3-031-73716-9 pp. 273–286 | resource manager 자체가 exascale 형태의 workload를 견디는지 검증 · synthetic DAG workload · generated-workload test harness | 규모 `UNVERIFIED`; production data NO (synthetic) | **L0 / D1 / P0** | **HIGH — 스케줄러를 *system under test* 로 다루는 유일한 논문. resource-manager scalability testing에 archival 논문 없음.** |
| **9** | **Supporting HPC Users with LLview** — Guimarães, Sankaran, Frings (JSC) | 2025 · MODA25 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-032-07612-0_4 (LLview: 10.5281/zenodo.12706843) | 운영 이슈를 진단하고 올바른 이해관계자에게 보고 · near-real-time job + system metrics · open-source 프레임워크, **role-based access** (user / support / admin view) | **JUWELS Cluster + Booster, production**; deployed **YES, production, open source** | **L1–L2 / D4 / P3** | **VERY HIGH — 누락된 평가(리포팅이 사용자 행동을 바꾸는가?)가 곧 출판 가능한 연구.** *Contribution:* 운영 데이터의 role-based 계층화 — SC25 BoF의 "데이터가 엉뚱한 사람에게 간다"는 발견에 직접 대응 |
| **10** | **A Unified I/O Monitoring Framework Using eBPF** — Paipuri (CNRS / IDRIS) | 2025 · MODA25 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-032-07612-0_3 | 기존 I/O 도구는 MPI-IO만 보고 시간 해상도가 없다 · VFS kernel function의 eBPF trace → Prometheus · filesystem·언어 무관 kernel-level tracing | production **Lustre**, **IOR** 대비 검증; "negligible overhead"; deployed YES (IDRIS) | **L0–L1 / D4 / P3** | **VERY HIGH — "Darshan은 AI workload를 보지 못한다"는 현재진행형 미해결 문제.** *Limits:* overhead 주장이 benchmark 하에서만, full production mix 아님 |
| **11** | **Duration-Informed Workload Scheduler** — Loreti, Leone, Borghesi (UniBo) | 2025 · MODA25 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-032-07612-0_1 | 사용자 walltime 추정치가 쓸모없어 스케줄링이 손해 · **M100 ExaData** production trace · ML duration prediction을 스케줄러에 통합 | Marconi100 trace, simulation; deployed NO | **L4 → L6 / D2 / P2** | **HIGH — 이것의 실제 배포는 SC/IPDPS 논문이 된다.** *Contribution:* **평균 job 대기시간 약 11% 감소.** *Limits:* simulation only, production A/B 없음 |
| **12** | **What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years** — Siegmann, Carlson, Simakov, Curtis, Calder, Harrison (Stony Brook / SUNY Buffalo) | 2025 · MODA25 · **[WORKSHOP-PEER-REVIEWED]** · 10.1007/978-3-032-07612-0_5 | 시스템 수명 전체에서 어떤 운영 지표가 실제로 project success를 예측하는가 · 다년 usage + performance tracking · longitudinal experience study | Ookami (HPE Apollo 80 A64FX), **4년 이상, 500명 이상 사용자** | **L1 / D3 / P4** | **HIGH — longitudinal ODA 연구는 archival로 사실상 존재하지 않음.** *Limits:* 단일 소규모 시스템, 서술적이며 예측적이지 않음 |
| **13** | **Heterogeneous Syslog Analysis: There Is Hope** — Quan, Howell, Greenberg (LANL) | 2023 · HPCSYSPROS23 · **[WORKSHOP-PEER-REVIEWED]** · 10.1145/3624062.3624128 / 10.5281/zenodo.10223395 | 이기종 클러스터가 호환되지 않는 로그 포맷을 뱉고, 하드웨어 고장·보안 이벤트가 noise에 익사한다 · production syslog · significant vs admin-defined noise로 ML 분류; **LLM을 classifier로 평가** | LANL clusters, 규모 `UNVERIFIED`; deployed `UNVERIFIED` | **L2–L3 / D2–D3 / P3** | **VERY HIGH — LLM 기반 운영 로그 triage는 2026년의 명백한 논문 주제이며 archival 버전이 없다.** *Contribution:* 이르고 정직한 LLM-vs-classical 비교 — LLM이 더 설명 가능하지만 계산 비용이 크다. *Limits:* 초록에 정량 F1/precision 없음, noise label이 사이트 고유 |
| **14** | **Advancing ODA Standardization Through an Open Source Dashboard** — Osborne, Palumbo, Huk, Adamson, Jones, Lester (ORNL) | 2024 · HPCSYSPROS24 · **[WORKSHOP-PEER-REVIEWED]** · 10.5281/zenodo.15724831 | 센터 간 공유 ODA schema나 시각화가 없다 · site telemetry · 표준화 수단으로서의 open-source 참조 dashboard | ORNL, `UNVERIFIED`; deployed `UNVERIFIED` | **L1 / D3 / P3** | **HIGH — 검증된 cross-site ODA schema는 진짜 SC 기여가 된다.** *Contribution:* 8년간의 BoF 표준화 논의 뒤에 있는 구체적 artifact. *Limits:* 형식적 schema 정의 없음, multi-site 검증 없음 |
| **15** | **Experiences Detecting Defective Hardware in Exascale Supercomputers** — Hagerty, Webb, Melesse Vergara, Ezell (ORNL) | 2023 · HPCTESTS23 · **[WORKSHOP-PEER-REVIEWED]** · SC23 Workshops (ACM 10.1145/3624062, article ID `UNVERIFIED`) | exascale에서 조용히 결함이 있는 소수 노드를 찾아내기 · acceptance + continuous test 결과 · test-suite 기반 탐지 | **Frontier-class exascale system** (`exact system UNVERIFIED but ORNL exascale context`); deployed YES | **L2–L3 / D4 / P3** | **VERY HIGH — exascale silent hardware defect 탐지에 archival 논문 없음.** *Contribution:* silent-defect 문제에 대한 결정적 실무자 진술. *Limits:* experience report, 재사용 가능한 방법론·통계 없음 |
| **16** | **Toward Collaborative Continuous Benchmarking for HPC** — Pearce, Scott, Becker, Haque, Hanford, Brink, Jacobsen, Poxon, Domke, Gamblin (LLNL, Google, RIKEN, HPE) | 2023 · HPCTESTS23 · **[WORKSHOP-PEER-REVIEWED]** · SC23 Workshops | 모든 센터가 벤치마킹을 재구현하고 결과가 비교 불가 · benchmark result corpora · 공유 사양 + 협업 인프라 (Benchpark 계보) | multi-institution; production data partial | **L0–L1 / D2 / P2** | **HIGH.** *Limits:* position/infrastructure paper |
| **17** | **An Automated Approach to Continuous Acceptance Testing of HPC Systems at NERSC** — Siddiqui, Palmer, Shende, Spear, Sambrekar, Xiang (NERSC / U. Oregon / ASU / CMU) | 2022 · HPCSYSPROS22 · **[WORKSHOP-PEER-REVIEWED]** · Zenodo, DOI `UNVERIFIED` | acceptance test가 수작업·1회성이며 시스템은 acceptance 후 drift한다 · 시간에 따른 test suite 결과 · buildtest 기반 자동화 | NERSC production systems; deployed YES | **L2 / D4 / P3** | **HIGH.** *Limits:* 실제로 어떤 drift가 잡혔는지 분석 없음 |
| **18** | **Dynamic Login Node Resource Control and Monitoring with Arbiter 3** — McKay, Forrest, Fischer (University of Utah) | 2024 · HPCSYSPROS24 · **[WORKSHOP-PEER-REVIEWED]** · 10.5281/zenodo.16541343 | 공유 login node의 남용/폭주 프로세스가 모두의 서비스를 저해 · per-user resource usage · dynamic cgroup limit + 사용자 통지; **closed-loop enforcement** | Utah CHPC production; deployed **YES** | **L7 (closed-loop) / D5 / P3** | **HIGH — archival 평가가 없는 L7/D5 시스템은 이미 만들어진 논문.** *Contribution:* corpus 전체에서 진정으로 **closed-loop, production-deployed** 인 극소수 사례 중 하나. *Limits:* 사용자 행동 효과나 false-positive rate에 대한 공개 평가 없음 |
| **19** | **From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments** — George, Wang, Hanley, Ransom, Bent, Zimmer (ORNL / LANL) | 2024 · FTXS24 · **[WORKSHOP-PEER-REVIEWED]** · IEEE SC-W 2024 (10.1109/SCWorkshops63240.2024, article ID `UNVERIFIED`) | 대규모 HPC 스토리지의 disk 고장 거동 · production disk failure record · failure-trend 분석 | ORNL-scale storage; 정확한 규모·기간 `UNVERIFIED` | **L3–L5 / D2 / P3** | **HIGH — HPC 특화 disk reliability에 2020년 이후 archival 논문이 없다 (ICS에 간 GPU 연구와 대조).** *Limits:* 서술적, 예측 모델 배포 없음 |
| **20** | **ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection** — Egersdoerfer, Zhang, Dai (UNC Charlotte) | 2022 · FTXS22 · **[WORKSHOP-PEER-REVIEWED]** · IEEE FTXS 2022, pp. 1–10 | log-template 폭발이 log 기반 이상탐지기를 무력화 · HPC log corpora · anomaly detection 전에 log template의 semantic clustering | 데이터셋·규모 `UNVERIFIED`; production data `UNVERIFIED`; deployed NO | **L3 / D1 / P1–P2 `UNVERIFIED`** | MEDIUM–HIGH. *Limits:* live production보다는 공개/benchmark 로그일 가능성 |

**Honourable mentions (verified, 완전 프로파일은 아님):** Sivalingam & Richardson, *LASSi for ARCHER* (MODA20, 다년 Lustre+scheduler 조인); Egan, Purkayastha, Sickinger, *Data Center Facility Monitoring with Physics Aware Approach* (MODA22, NREL); Lewis, Liu, Kettimuthu, Papka, *Log-Based Identification, Classification, and Behavior Prediction of HPC Applications* (HPCSYSPROS20, ANL); Simakov, *XDMoD Application Kernel Module* (HPCSYSPROS24); Angelelli, Carastan-Santos, Dutot, *Run your HPC jobs in Eco-Mode* (JSSPP24); Tröpgen et al., *Pinpointing Idle-Power Regressions in Linux* (EESP25); DeBardeleben et al., *Statistical Framework for Two-Party Acceptance Testing* (FTXS21); Kartik & Lockwood, *Beyond the Hype: Uncovering the Real I/O Needs of LLMs* (HPCSYSPROS24).

---

# 4. CUG operational problem inventory (P1 ~ P19)

**이 절이 서베이 전체에서 가장 가치 있는 부분이다.** 각 항목 구조: **문제 → 보고 주체 → 무엇을 만들었나 → 무엇이 안 되었나(원문 인용) → 정량 평가 유무.**
영어 인용문은 운영자의 원문이며 **일절 수정하지 않았다.** 한국어는 짧은 gloss일 뿐이다.

> ⚠️ 재확인: **CUG "Paper"는 peer-reviewed archival이 아니다** (§1.2-3). 아래는 전부 *practice evidence* 다.

---

## P1. Telemetry message bus는 확장되는데 producer/consumer가 안 된다; schema drift가 아카이브를 오염시킨다

- **보고 주체:** ORNL NCCS — Adamson, Osborne, Lester, Palumbo, *STREAM: A Scalable Federated HPC Telemetry Platform*, CUG2023 `[PAPER]` (OSTI 1995656)
- **무엇을 만들었나:** Kafka 중심 federated bus (OpenShift 위 broker 6대), 원격 소스용 Kafka Connect, Elasticsearch data lake, Grafana
- **무엇이 안 되었나 (원문):**
  > *"STREAM's biggest pain point has been producers and consumers, not the Kafka bus itself."*
  > (가장 큰 고통은 Kafka bus 자체가 아니라 producer와 consumer였다)

  > *"[Sensor data] has not been standardized into a universal format and may as we have found, change throughout the lifetime of the data. This can cause significant and unexpected errors."*
  > (센서 데이터는 통일 포맷으로 표준화되어 있지 않고, 우리가 겪은 바로는 데이터 수명 동안 변한다. 이것이 심각하고 예기치 못한 오류를 유발한다)

  잘못된 topic 이름 때문에 재색인이 강제되었고 — *"This can be a slow process"*; broker 장애 시 → *"TBs of recovery traffic"*; 문서는 *"incomplete, inconsistent, and confusing."*
- **정량 평가:** **운영 수치는 YES** — 300M msgs/day, 200+ topics, 1.3 TB/day, 72 MB/s avg, 105 MB/s peak, 복제 포함 300 MB/s, 이론 상한 7.5 GB/s. **controlled experiment는 없음.**

---

## P2. 벤더 telemetry 서비스가 production 데이터율을 감당하지 못했다 ★

- **보고 주체:** Sandia / LLNL / LBNL + HPE 공저 — Barry (HPE), Brandt, Gentile (SNL), Morrone, Scott, Shoga (LLNL), Roman (LBNL), Tucker (OGC), *Evaluating and Influencing Extreme-Scale Monitoring Implementations*, CUG2023 pap149 `[PAPER]`, LLNL-CONF-847852
- **핵심 발견 (원문):** CSM `telemetry-api` 는
  > *"unreliable and often inefficient. It stopped feeding data at random times, and frequently caused Kafka rebalancing events"*
  > (신뢰할 수 없고 자주 비효율적. 임의의 시점에 데이터 공급을 멈췄고, 빈번히 Kafka rebalancing을 유발했다)

  그리고 Perlmutter full scale에서
  > ***"could not handle the data rate (100K to 1M messages per second)"***
  > (초당 10만~100만 메시지의 데이터율을 감당하지 못했다)
- **또한 (원문):** boot 시 LDMS credential 배포가
  > *"not only slow but unreliable… causes the boot-time Ansible plays to fail"*

  단일 고정 worker `ncn-w001` 병목:
  > *"If ncn-w001 is unavailable or overloaded then a boot will either be extremely slow or fail altogether."*
- **무엇을 만들었나:** 사이트 우회로 — NERSC 자체 LDMS store plugin → VictoriaMetrics → OMNI; LLNL LDMS→Kafka(Avro)→Kafka Connect→Elasticsearch, 추가로 MirrorMaker→Sonar/Cassandra
- **정량 평가:** **PARTIAL.** 모니터링 overhead를 *"no statistically significant performance penalty"* 라고 보고했으나 **방법도 수치도 제시되지 않았다. 주목할 만한 증거 공백이다.**

---

## P3. 벤더와 사이트 간 인코딩/포맷 분기 때문에 사이트 간 튜닝이 이전되지 않는다

- **보고 주체:** 위와 동일 논문 (CUG2023 pap149)
- **원문:**
  > *"LLNL and HPE have different formats. LLNL uses Avro encoding… HPE sends one metric per message in JSON format"*

  LLNL의 Avro는 *"significantly fewer bytes transmitted"* 를 낳는다. 결과가 명시적으로 진술된다:
  > ***"the variation in the Kafka format means there can't easily be a rule of thumb in one implementation that extends to the other."***
  > (Kafka 포맷의 차이 때문에, 한 구현에서 얻은 경험칙이 다른 구현으로 쉽게 확장되지 않는다)
- **또한:** CSM은 *"an internal version of LDMS which is significantly behind the latest LDMS release"* 를 탑재하며, *"LDMS samplers that have not been up-streamed and may be proprietary"* 를 포함하고, 사이트 커스터마이즈는 *"would need to be re-implemented with each CSM update."*
- **정량 평가:** **없음.**

---

## P4. Fabric counter 취득 자체가 비싸다; counter 선택이 임의적이다

- **보고 주체:** 위와 동일 논문 (CUG2023 pap149)
- **원문:** Slingshot switch는 *"over a thousand counters per port and over 64K total port counters per switch"* 를 노출한다. El Capitan은 *"potentially hundreds"* 중 기본값으로 *"roughly forty"* 를 쓴다. `dump_counters` 는 switch당 *"about half a second"*.
  > *"We would like to work with HPE to identify more efficient port counter access mechanisms."*
- **정량 평가:** counter 수와 0.5 s는 있음. **그러나 어떤 counter가 중요한지에 대한 연구는 없다 — 그 지점이 연구 공백이다.**

---

## P5. Fabric telemetry 볼륨이 대화형 분석을 무너뜨린다

- **보고 주체:** HPE — Mitra, Ragland, Zambrano, Mallick, Vollmer, Kelley, Mohan, *CADDY: Scalable Summarizations over Voluminous Telemetry Data for Efficient Monitoring*, CUG2024 `[PAPER][VENDOR]`
- **원문:**
  > *"Fabric AIOps' reliance on voluminous telemetry data generated from Slingshot's nodes and switches poses significant challenges for traditional disk-based storage solutions."*
- **무엇을 만들었나:** counter당 5개 Welford moment를 담는 계층적 시간/공간 "Bins"; Ray 분산 in-memory store
- **정량 평가:** **YES — 찾아낸 벤더 평가 중 가장 엄밀함.** 압축 425x (10-min bins) / 600x (15-min) / 1200x (30-min); 단일 frame fetch 355 ms → 151 ms (group level, −57%) / 267.51 ms (port level, −25%); ingest overhead **+32.5%** (1M event당 0.7589 s → 1.007 s); ingest 300K events/min; testbed 8 groups × 8 switches × 64 ports = 4096 ports, counter 4종 (rxBW, txBW, rxCongestion, txCongestion); node = 128 AMD EPYC 7002 cores, 196 GB RAM. Live-mode horizon이 **10분 → 수일**로 확장. 명시된 한계: *"the ideal temporal window size should not exceed 3 hours."*
- **한계 (원문):** 단일 노드 평가만; counter 4종만; 극단 압축이 *"may reduce granularity for certain anomaly detection workloads."* 또한 HPE의 이전 trellis (CUG2021)는 30일간 raw telemetry가 *"several petabytes"* 이며 *"trade-off between interactivity and computation time"* 이 있다고 시인했다.

---

## P6. 조용한 결함 하드웨어("bad actors")는 boot-time health check로 잡히지 않는다 ★★

- **보고 주체:** ORNL + HPE — Hagerty (ORNL), Warner (HPE), Webb, *Multi-stage Approach for Identifying Defective Hardware in Frontier*, CUG2024 pap123 `[PAPER]` — **corpus에서 가장 정량적으로 강한 운영 논문**
- **무엇을 만들었나:** 세 전략 — (1) leadership-scale LAMMPS failure isolation, (2) 단계별 HACC job-completion 정식 연구, (3) Slurm **backfill** 을 이용한 주기적 단일 노드 screening
- **정량 평가 (전부 원문 수치):**
  - LAMMPS 244 jobs → *"19 cases of defective hardware were successfully identified and repaired."*
  - 4096 nodes / 500 W TDP: *"17 of 50 jobs failed"*; HBM +100 mV 및 기본 memory clock 조건: *"11 of 50 jobs failed."*
  - *"75% reduction in power faults from Phase 2 to Phase 4."*
  - Backfill screening: 2024년 4월까지 *"Nearly 6 million single-node tests"*; 2023-10 ~ 2024-04 구간에 1.9M
  - 테스트별 실패 수: BabelStream 562,671 runs / 2,796 failures; rocHPL 328,576 / 162; AMG 337,684 / 129; oblex 184,424 / 124; rocPRIM 304,361 / 24; LAMMPS 175,418 / 12
  - 6개월간 **99 unique failing nodes** — 분류: software bug 54, transient performance 27, GPU HBM UE 12, numerical instability 11, non-reproducible 4
  - backfill LAMMPS는 *"averaged identifying one failure per 14,618 tests."*
  - Frontier: 9,408 nodes, 37,632 MI250X @ 560 W TDP
- **무엇이 안 되었나 — 명시적 (원문):**
  > 주간 `checknode` screen은 6개월간 ***"39,437 screens with no failures"*** 를 냈고 **2023년 12월 production에서 제거**되었다 — 효과가 없어서. 테스트 시간이 너무 짧았기 때문(backfill LAMMPS 24분 대비 1분 미만). epilog 변형은 *"too disruptive to user workloads."*
  > (39,437회를 돌려 단 한 건도 못 잡았다 → 폐기. HPC 운영에서 공개된 가장 값진 negative result 중 하나다)

  또한: *"Same error message can also be triggered from compiler bugs."*

---

## P7. 노드 health check는 스크립트·규칙 기반이며 공개된 정확도가 없다

- **보고 주체:** ORNL — Ezell, *Frontier Node Health Checking and State Management*, CUG2023 pap151 `[PAPER]`
- **무엇을 만들었나:** `checknode` bash script; boot 시 전체 실행, Slurm epilog에서 축소 세트; reason string과 함께 노드 drain; drain 사유가 self-set이면 자동 resume; controller/console/syslog에 대한 SEC (Simple Event Correlator)
- **정량 평가:** **전무.** 테스트한 노드 수, 기간, drain 수, false positive에 대한 수치가 0. 정성 데이터 하나:
  > *"mean time between failure on a system this size is hours, it's not days."*
  > (이 규모 시스템의 MTBF는 일 단위가 아니라 시간 단위다)

  구체적 결함 하나: *"a bug in the power management firmware that prevented the CPU from going into burst mode"* — MPI all-to-all 성능 저하 유발
- **HPE의 병렬 노력:** Wazirzada, Mehta, Phadke, *From Frontier to Framework: Enhancing Hardware Triage for Exascale*, CUG2024 `[PAPER][VENDOR]` — node-controller debug JSON + Redfish 위의 YAML-DSL **rule-based decision tree**, **명시적으로 ML 아님**; Frontier context *"more than 9400 compute nodes"*, *"over 150,000 node-level components"*; **평가 수치 0**; 저자 스스로 인정: *"[it] is not a substitute for the discipline of system health checks."*

---

## P8. Cross-source attribution: telemetry의 job energy와 scheduler의 job energy가 불일치하고, scheduler는 신뢰되지 않는다 ★

- **보고 주체:** CSCS + HPE — Benini, Hanson (HPE), Gianolli, Piccinali, Brambilla, Marano, Ricciardi, Frisoni, Conciatore, *EMOI: CSCS Extensible Monitoring and Observability Infrastructure*, CUG2024 pap113 `[PAPER]`
- **정량 발견:** Job 2665753 — **5,663,156 J (telemetry) vs 5,662,307 J (Slurm)**; 4개 node type에 걸쳐 984 jobs 분석
  > ***"Slurm on the other hand, shows sometimes a weird behaviour and cannot therefore always be trusted."***
  > (반면 Slurm은 때때로 이상한 거동을 보이며, 따라서 항상 신뢰할 수는 없다)
- **또한:** Cray PM 수집은 **10 Hz**, telemetry pipeline은 **약 1 Hz**
- **무엇이 안 되었나 (원문):** CSM 번들 Kafka는
  > *"does not expose any external listener, which means external applications can't connect to the Kafka cluster"*

  한 메시지에 여러 센서를 묶는 방식은 *"is not suitable for ingestion into ElasticSearch"*; **Fluent Bit 기각** —
  > *"we couldn't make it stable for large throughputs."*
- **정량 평가:** 탐지 방법에 대한 평가 **없음.** EMOI는 **GB/day도, cardinality도, retention도 보고하지 않는다.**

---

## P9. 스토리지 성능 이상은 실재하고 빈번하며, 오직 예약된 능동 probing으로만 발견된다 ★

- **보고 주체:** NERSC + HPE — Gerhardt, Simms, Bhimji (LBNL/NERSC), Moore (HPE) 외, *Nine Months in the life of an all-flash file system*, CUG2024 pap141 `[PAPER]` — **corpus 최고의 스토리지 수치**
- **시스템:** Perlmutter all-flash Lustre — 36 PB, 이론 peak >7 TB/s, 16 MDS, 274→298 OSS/OST, 3,480 NVMe drives, 사용자 약 10,000명, 기본 quota 20 TB / 20M inodes
- **무엇을 만들었나:** *"daily, off-hours obdfilter-survey test… configured by NERSC staff in August of 2023"*; GPU 노드 32대에서 약 250 TB write/read하는 IOR; CoV 수용 목표 *"8% or below."*
- **발견 (원문):**
  > *"several OSTs intermittently… reporting very slow write rates between 25% and 50% lower than expected"*
  > (여러 OST가 간헐적으로 기대치보다 25~50% 낮은 write rate를 보고했다)

  수정 후 write 성능이 *"from 15.1 GB/s to 19.9 GB/s — a 30% improvement"*, 최저 rate가 *"from 260 MB/s to 9,032 MB/s"*.
  보안 패치(SafeRet) 비용: *"a decrease in mean write bandwidth values of 14%"*; checksum 활성화 비용: *"a 17% drop in mean write bandwidth (from 673320 MB/s ± 31779 to 554012 MB/s ± 37846)"*.
  근본 원인: NVMe garbage collection, Lustre allocator의 *"useless c1 loops"* (수정: `mb_c2_threshold=25`), trim 빈도. 최적 OST 사용률은 *"around a surprising 75% of file system capacity."* 2024년 회귀는 *"a large number of OSTs as read only. This meant only about 50 OSTs were available."* 로 추적됨. purge 지평 약 365일.
- **무엇이 안 되었나:** **passive telemetry만으로는 이 문제들이 드러나지 않았다. 매일의 능동 probing이 필요했다.**

---

## P10. Power/cooling 이상탐지가 알고리즘도 평가도 없이 "기능"으로 출하된다

- **보고 주체:** HPE — CUG2025 tut106 `[TUT][VENDOR]`; CUG2022 HPCM BoF `[BOF][VENDOR]`
- **주장 (원문):** AIOps는 *"machine learning and deep learning technologies to identify and report trends"* 를 사용하여 *"real-time and offline anomaly detection, prediction for time-series monitoring data"* 를 제공하며, univariate/multivariate, containerized. *"anomaly score exceeds the anomaly threshold"* 시 경보하고 *"after a predefined period of time"* 만료. 예시 대상: CDU valve position, cooling pressure, CPU/GPU temperature. `cm monitoring grafana dashboard enable [category]` 로 활성화.
- **무엇이 안 되었나:** **알고리즘 명시 없음. threshold 선택 방법 없음. precision/recall 없음. 배포 규모 없음. false alarm 데이터 없음.** CUG2022 BoF도 마찬가지로 *"AIOPs anomaly detection for IT metrics"* 를 나열할 뿐 뒤에 아무것도 없다.
- **정량 평가:** **없음.**

---

## P11. Retention 경제성이 설계를 지배하고, 기본값은 공격적이다

- **보고 주체:** HPE — CUG2025 tut106 `[TUT][VENDOR]`
- **HPCM 1.13 기본값:** **Kafka 1 day** (≤1.12: CrayEX telemetry 24 h, 그 외 168 h), **OpenSearch 7 days**, **VictoriaMetrics 7 days**, **TimescaleDB 30 days** (신규 배포에는 deprecated), 7일 시점 Timescale 압축이 *">90% disk space"* 절감. Slingshot 모니터링은 *"the big hitter for disk space."* native monitoring interval은 설정 가능, 예시 5 s.
- **스택 전환 기록:** Prometheus/TimescaleDB → **VictoriaMetrics**; Filebeat → **Fluent Bit**; Elasticsearch → **OpenSearch** (CSM/SMA 1.8: *"Moved from Elasticsearch to Opensearch (due to licensing change)"*); Alerta/Elastalert → **Alertmanager only**.
- **무엇이 안 되었나:** *"[HPE] does not provide explicit performance benchmarks, node scaling limits, or expected data volumes for different cluster sizes."* → **벤더가 sizing model을 공개하지 않는다.**

---

## P12. 로그 파이프라인 처리량은 사이트가 해결하는 문제이고, 해법의 효과는 20배다

- **보고 주체:** NERSC/LBNL OTG — Siqi Deng, CUG2023 tut107 deck (OMNI)
- **정량:** OMNI 파이프라인이 로그 메시지를 *"From 100k/s To 2 million/s"* 로 확장. 수정 전 병목은 *"< 100k messages/s"*, 중간 단계 *"200k messages/s"*, 자원 배정 *"2 CPU cores + 150MB Mem per pod x 64~128 pods"* (Promtail). 해법: rsyslog scale-up + Kafka scale-out. ClusterStor 및 Cassini 모니터링 파이프라인도 문서화.
- **보강 (CUG2022 NERSC deck, Deng):** 통합 목표 *"One Monitoring UI (Grafana), One Query Language (PromQL/LogQL), One Notification Engine (Alertmanager)"*; Loki는 명시적으로 *"not for replacing Elasticsearch."*

---

## P13. Fabric 관리 observability가 얇아서 사이트가 직접 poller를 짠다

- **보고 주체:** NERSC — John Stile, *Slingshot Fabric Manager Monitor*, CUG2022 `[PRES]`
- **무엇을 만들었나:** Slingshot Fabric Manager REST API를 polling하는 Python 앱(Kubernetes CronJob) — health status, switch topology/online, port state → VictoriaMetrics + Loki. switch offline, port flapping, health degradation, API 연결 상실을 탐지. metric 11종.
- **보고된 어려움:** *비수치 health state의 시각화*, *장기 port state 이력 저장*, *Kafka 스트리밍 telemetry 통합*
- **정량 평가:** **polling interval, switch/port 수, 데이터 볼륨 모두 미제시.**

---

## P14. Facility 측 모니터링이 IT 측이 놓친 문제를 잡는다 — 벤치마크 규모의 보상과 함께 ★

- **보고 주체:** EPCC/HPE — Leach, Cass 외, *Automated service monitoring in the deployment of ARCHER2*, CUG2022 pap103 `[PAPER]`
- **무엇을 만들었나:** Checkmk (Nagios 파생) + Graphite + Grafana, 시스템 그룹별 TCP agent 분산. cabinet controller로부터 **rectifier 수준 전력을 5초마다 수집**; Slurm `sinfo` 노드 상태 점검; SSH 로그인 probe; Lustre 및 Slingshot HSN 점검; HPE pager 포함 이메일 경보. ARCHER2: 5,860 nodes / 750,080 cores.
- **정량화된 보상:** HPL 수행 중 전력 모니터링이 *"power cycling"* 거동을 식별했고, 해당 노드들을 격리하자 Top500 성능이 **16.8 PF → 19.5 PF** 로 이동했다.
- **무엇이 안 되었나 (원문):**
  > *"Historical Graphite data granularity reduces over time to conserve disk space"*
  > (디스크 절약을 위해 과거 Graphite 데이터의 해상도가 시간이 지나며 감소한다)

  → **downsampling이 장기 고해상도 분석 능력을 파괴했다. 구체적으로 보고된 1급 downsampling failure mode다.**

---

## P15. GPU 이용률 telemetry가 agent overhead를 피하려고 의도적으로 열화되어 있다 — 그리고 그 결과 드러난 그림은 참담하다 ★

- **보고 주체:** Indiana University — Weakley, Michael, Thota, Huber, Fulton, Kusz, *Monitoring and characterizing GPU usage*, CUG2023 pap139 `[PAPER]`
- **DCGM 기각 (원문):**
  > ***"DCGM appeared to have too intrusive of a footprint to be viable for deployment."***
  > (DCGM은 배포 가능하다고 보기엔 발자국이 너무 침습적으로 보였다)
- **무엇을 만들었나:** pynvml 기반 epilog-time 수집, Slurm `AdminComment` (MariaDB)에 JSON, 4,000-record GPU ring buffer
- **정량:** 295,470 GPU jobs (2020-07 ~ 2023-03); **평균 GPU 이용률 11%**; ***53% of jobs never accessed the GPU***; 미사용 job 제외 시 평균 26%; 645개 고유 애플리케이션, 그 중 53%가 AI/ML, 그 AI/ML의 99.6%가 Python
- **실패 모드:** `AdminComment` 의 65,535자 제한이 *"occasionally truncating long-running multi-GPU jobs"*; nvml `gpuUtilization` 은 core 이용률이 아니라 *"percentage of time that the GPU was active"* 를 측정
- **CSCS의 반대편 보강 (CUG2025 pap159):** *"DCGM's lack of native scheduler-level resource isolation, requiring cluster-level rather than node-group-level data querying."*

---

## P16. Digital twin이 telemetry 시간척도의 벽에 부딪힌다 ★

- **보고 주체:** ORNL / Oakland U — Holmen (ORNL), Newaz (Oakland U) 외, *Towards the Development of an Exascale Network Digital Twin*, CUG2024 pap140 `[PAPER]`
- **시스템:** Frontier — 9,408 EX235a nodes, Slingshot 11 three-hop dragonfly, *"80 groups: one management, five I/O, and 74 compute groups"*, node당 NIC 4개
- **핵심 문제 (원문 그대로):**
  > ***"The switching technology of the dragonfly network is between 100 to 350ns, whereas Frontier system telemetry is typically collected at 15-second time quanta."***
  > (dragonfly 네트워크의 스위칭은 100~350 ns인 반면, Frontier 시스템 telemetry는 통상 15초 단위로 수집된다 — 약 10⁸배의 시간척도 격차)

  그리고: *"network-related telemetry data must be obtained by systematically profiling applications"* — 즉 production 스택이 그것을 노출하지 않는다.
- **비용:** *"replaying a single MPI rank on each node of Frontier would take more than 30 hours"* (job 제한 2시간 대비); SST-Core 가속 *"~7x, which still does not provide enough speedup."* 규모 맥락: *"approximately 1.8 million jobs and counting have been run across Frontier"*; *"about six months of Frontier telemetry have been replayed."*
- **미해결:** *"further investigation remains to find a way to validate NIC-based spyplots."* **정확도 수치 없음.**

---

## P17. 운영 telemetry에 대한 인과 추론이 방법이 아니라 데이터 부족으로 실패한다 ★

- **보고 주체:** HPE Labs + ORNL — Hong Enriquez, Prakash, Taheri, Dhakal (HPE Labs); Maiterth, Brewer (ORNL); Milojicic, *Causality inference for Digital Twins in GPU Data Centers and Smart Grids*, CUG2025 pap118 `[PAPER]`
- **데이터:** Summit, *"27,648 Tesla V100 GPUs"* 를 3년간 모니터링 — **그럼에도 사용 가능한 failure dataset은 11개 feature를 가진 127개 failure event entry 뿐이었다.**
- **방법:** causal calculus / do-calculus, multivariate transfer entropy (mTE), convergent cross mapping (CCM). Mooij et al. 93 pairs + synthetic set으로 검증; graph edit distance 1–37
- **무엇이 안 되었나 (원문):**
  > mTE *"did not produce significant results"*
  > CCM은 *"only 127 records"* 로 굶주렸다
  > *"scarcity of proper multivariate methods… for causal discovery"*
  > *"methods diverge in their results pointing to different perspectives."*
  > (3년, 27,648 GPU를 모니터링하고도 인과추론에 쓸 수 있는 레코드가 127건. 데이터 부족이 방법론 부족보다 앞선다)

---

## P18. 하드웨어 인지 노드 그룹핑 자동화는 존재하지만, 저자 스스로 production에 부적합하다고 명시한다

- **보고 주체:** CSCS — Sopena Ballesteros, Chesi, Gila, Klein (CSCS/ETH), *Automated Hardware-Aware Node Selection for Cluster Computing*, CUG2024 pap106 `[PAPER]`
- **무엇을 만들었나:** CSM API 기반 인벤토리, 하드웨어 컴포넌트 패턴(`a100:12:epyc:1`), scoring + delta + fuzzy matching, 메모리를 16 GiB 단위로 정규화
- **저자 자신의 판정 (원문):**
  > *"this algorithm may not be valid"* — Slurm 하에서 재배정이 *"highly disruptive"* 할 수 있기 때문
  > ***"we do not recommend following this algorithm in a production environment."***
  > (우리는 이 알고리즘을 production 환경에서 따르는 것을 권장하지 않는다)
- **정량 평가:** **없음.**

---

## P19. 애플리케이션 식별은 미해결 observability 공백이다

- **보고 주체:** CSCS — Holanda Rusu, Benini, *A glimpse of YAULT*, CUG2025 bof102 `[BOF]`
- **문제 (원문):** *"Can we identify the applications used by the users?"* — mandatory access control, chrooted container, 사용자 소유 환경 하에서
- **접근:** eBPF syscall tracing + Slurm plugin
- **정량 평가:** **수치 없음.**

---

## 4.x P1–P19 요약 표

| # | 문제 | 보고 주체 | 정량 평가 | 대표 수치 / 인용 |
|---|---|---|---|---|
| P1 | Kafka bus는 되는데 producer/consumer가 안 됨, schema drift | ORNL | 운영수치 O, 실험 X | 300M msg/day, 1.3 TB/day, 223 topics |
| **P2** | **벤더 telemetry-api가 데이터율 감당 실패** | SNL/LLNL/LBNL+HPE | PARTIAL | *"could not handle the data rate (100K to 1M messages per second)"* |
| P3 | 벤더-사이트 인코딩 분기 | 동상 | X | *"can't easily be a rule of thumb…"* |
| P4 | Fabric counter 취득 비용 | 동상 | 부분 O | >1,000 counters/port, 64K/switch, 0.5 s/dump, 기본 "roughly forty" |
| P5 | Fabric telemetry 볼륨 vs 대화형 분석 | HPE (CADDY) | **O (최고)** | 1200x 압축, +32.5% ingest overhead, 355→151 ms |
| **P6** | **silent defective hardware** | ORNL+HPE | **O (corpus 최고)** | **39,437 zero-yield screens → 폐기**; 1 failure / 14,618 tests; 99 unique failing nodes |
| P7 | 노드 health check 정확도 미공개 | ORNL / HPE | **X** | *"MTBF … is hours, it's not days"*; HPE 측 평가 수치 0 |
| **P8** | **job energy telemetry vs Slurm 불일치** | CSCS+HPE | 부분 O | 5,663,156 J vs 5,662,307 J; *"Slurm … cannot therefore always be trusted"* |
| **P9** | **스토리지 이상은 능동 probing으로만 발견** | NERSC+HPE | **O** | slow OST **25–50% below expected**; **15.1 → 19.9 GB/s (+30%)** |
| P10 | power/cooling 이상탐지 = 알고리즘 없는 기능 | HPE | **X** | 알고리즘·precision/recall·FP rate 전무 |
| P11 | retention 경제성이 설계 지배 | HPE | 기본값 O | Kafka 1 d / OpenSearch 7 d / VictoriaMetrics 7 d / Timescale 30 d |
| P12 | 로그 파이프라인 처리량 | NERSC | O | *"From 100k/s To 2 million/s"* |
| P13 | fabric 관리 observability 부족 | NERSC | **X** | metric 11종, interval·볼륨 미보고 |
| **P14** | **facility 모니터링이 IT가 놓친 것을 잡음** | EPCC/HPE | **O** | **16.8 PF → 19.5 PF**; Graphite downsampling이 장기분석 파괴 |
| **P15** | **GPU telemetry 의도적 열화 + 참담한 이용률** | Indiana U | **O** | DCGM *"too intrusive"*; **평균 GPU util 11%, 53%는 GPU를 아예 안 씀** |
| **P16** | **digital twin의 시간척도 벽** | ORNL/Oakland | **X (정확도)** | **100–350 ns vs 15 s**; 단일 rank replay >30 h |
| **P17** | **인과추론이 데이터 부족으로 실패** | HPE Labs+ORNL | **X** | 3년 27,648 GPU → **127 failure records**; mTE *"did not produce significant results"* |
| P18 | 노드 그룹핑 자동화, production 부적합 자인 | CSCS | X | *"we do not recommend following this algorithm in a production environment"* |
| P19 | 애플리케이션 식별 불가 | CSCS | X | *"Can we identify the applications used by the users?"* |


---

# 5. Telemetry data path 복원표 (숫자 포함)

파이프라인 템플릿: `sensor → agent/exporter → collector → bus → storage → aggregation → features → model → alert → action`
**모든 숫자는 원문에서 인용한 것이다. 추정치는 없다.**

## 5.1 사이트별 데이터 경로와 실측 비용

| 사이트 / 시스템 | Sensor & agent | Collector / bus | Storage | Analytics / model | Action | 보고된 비용·실패 모드 (원문 인용) |
|---|---|---|---|---|---|---|
| **ORNL — 5개 HPE 시스템 + Frontier/Orion (STREAM)** | HPCM(Redfish); Lustre용 Telegraf; xalt job 기록; BMC/OpenBMC power+thermal; Cray CSM telemetry-api; Slingshot counter | Kafka Connect → **Apache Kafka** 6 broker on OpenShift; **Stream Schema Relay**(Flask)로 schema federation | **Elasticsearch** data lake(LAKE); Apache Druid; Parquet on MinIO (OCEAN/GLACIER) | Spark Structured Streaming (Bronze→Silver→Gold medallion); Grafana; **LVA**(Live Visual Analytics); RATS-Report; Copacetic(보안); MLflow+DVC | 대시보드 / 운영 / 티켓 | **300M msgs/day, 200+ topic, 1.3 TB/day**; 223 topic(2023-05); 평균 **72 MB/s**, 피크 **105 MB/s**, 복제·소비 포함 **300 MB/s**, 이론 최대 7.5 GB/s; 최상위 producer `orion.lustre.rpc` **111K 평균 / 246K 최대 msg/s, 43 MiB 평균 / 85.9 MiB 최대 per second**; HPCM **~18 MB/s @ 105,000 msg/s**; Lustre **50 MB/s @ 128,000 msg/s**; HW: 6× Dell R740, 128 GB RAM, 24×12 TB SSD; Kafka pod당 24 TB/64 GB/16 thread. 목표 **20 PB over 5 years ⇒ 정상상태 140 MB/s**. **실패 모드:** *"STREAM's biggest pain point has been producers and consumers, not the Kafka bus itself"*; *"Sensors, metrics, and telemetry data has not been standardized into a universal format and may as we have found, change throughout the lifetime of the data"*; topic 개명 후 재색인 *"can be a slow process"*; broker 장애 시 **"TBs of recovery traffic"**; 문서가 *"incomplete, inconsistent, and confusing"* |
| **ORNL — 데이터센터 전체 (SC-W'24)** | 위 전부 + facility | — | STREAM(hot) → LAKE(warm) → OCEAN(cold) → GLACIER(∞) | 15초 간격 집계, medallion refinement | — | **총 4.2–4.5 TB/day.** 스트림별: **스토리지 ~3.3 TB/day · compute power&temp ~537 GB/day · interconnect ~32 GB/day · syslog&events ~8.64 GB/day · compute storage client ~2 GB/day · CRM ~350 MB/day · resource manager ~11 MB/day · facility ~2.5 MB/day.** 보존: **STREAM 3–14일 · LAKE 1–2주 · OCEAN 1–5년 · GLACIER ∞.** Frontier 전력 프로파일링 **0.5 TB/day** |
| **NERSC Perlmutter (CSM 기본 경로)** | compute의 LDMS sampler | LDMS L1 aggregator → **Kafka**(topic `cray-node`) | **PostgreSQL** persister | Grafana | 대시보드 | 기본 샘플링 **10초**; 전규모에서 **"100K to 1M messages per second"** — CSM `telemetry-api`가 **"could not handle"**; persister를 **5,000노드 시스템에 "as many as 16 copies"**로 확장; compute-node LDMS 데이터셋 **"a few kilobytes"**; 클럭 skew **"a few milliseconds"** |
| **NERSC Perlmutter (사이트 우회로) + OMNI** | LDMS sampler; rsyslog collector/aggregator; Promtail; 시설 BMS(BACnet/Modbus), PDU, UPS, 온도센서; sFlow/SNMP/IB/ESnet | NERSC aggregator pod + **커스텀 store 플러그인**; RabbitMQ / Prometheus scrape / Kafka | **VictoriaMetrics**(metric), **Loki**(log), Elasticsearch(legacy) → **OMNI** | Grafana; Promxy; Alertmanager | **ServiceNow MID server → 인시던트 + 자동 remediation 워크플로** | 로그 파이프라인 **"From 100k/s To 2 million/s"**(수정 전 *"< 100k messages/s"*, 중간 200k/s); Promtail 리소스 **"2 CPU cores + 150MB Mem per pod x 64~128 pods"**. OMNI 전체: **"over 522 billion records totaling 125TB"**, **"average of 25,000 data points per second"**, **"more than 20,000 sensors with hundreds of sources"**; 시설 PUE 월평균 **1.07** |
| **LLNL El Capitan (TOSS 4)** | LDMS sampler; `slingshot_metrics`, `rdc_sampler` | L1 aggregator → 클러스터 로컬 **Kafka**(**Avro**) → Kafka Connect ES sink; MirrorMaker → Sonar Kafka | 중앙 **Elasticsearch**; **Cassandra**(Sonar) | OpenShift 위 Grafana | 운영 | 계획 샘플링 **5초**; Slingshot counter를 **"over a thousand counters per port and over 64K total port counters per switch"**에서 **"roughly forty"**로 축소; `dump_counters` **~0.5초/switch**; LLNL의 Avro가 HPE의 metric당 1 메시지 JSON 대비 **"significantly fewer bytes transmitted"** |
| **CSCS Alps (EMOI)** | Beats agent; Cray PM **10 Hz**; SMA | Logstash(×2) → **Kafka**(Strimzi) → KafkaStream → Memcached | **Elasticsearch**(ECK) | Kibana, Grafana; job 에너지 분석 | 운영 / 에너지 회계 | telemetry 파이프라인 **~1 Hz**; ~10,000 GH200 + ~1,000 pre-Alps 노드; 984 job 분석; job 에너지 **5,663,156 J (telemetry) vs 5,662,307 J (Slurm)**. **GB/day·cardinality·retention 미공개.** 실패 모드: CSM Kafka가 **"does not expose any external listener"**; 다중 센서 메시지 번들링이 **"not suitable for ingestion into ElasticSearch"**; **Fluent Bit 거부** — *"we couldn't make it stable for large throughputs"* |
| **LRZ SuperMUC-NG (DCDB + Wintermute)** | pusher | MQTT → collectagent | **Cassandra** | Grafana; Wintermute in-band/out-of-band analytics operator | 운영 | **14.5M 센서(6.8M raw를 로컬 처리)**, **0.1–30초** 샘플링, 30일 보존(sub-sample은 무기한), **2.5 TB Cassandra**, 전용 머신 10대. **사전집계로 70만 → 6만 insert/s (~11.7배)**; 10초 → 2분 집계. Wintermute 오버헤드 **<0.5%, <25 MB**. DEEP-EST: 141노드, 70k 센서. 원문: *"allocating resources for monitoring and ODA requires significant thought at system design time, with storage being critical"* |
| **CINECA Marconi100 (ExaMon)** | 플러그인 | MQTT | KairosDB → **Cassandra** | Grafana; RUAD 등 프로토타입 | 운영 | **49.9 TB / 934일**, **573 metric @ 1초**, 980+ 노드. label은 Nagios 15분 입도 → 그 위 분류기 **AUC 0.57** |
| **RIKEN Fugaku** | A64FX **assistant core**를 수집에 사용하는 3계층 파이프라인 | — | TSDB; Prometheus + Elasticsearch/Logstash/Kibana | Grafana 대시보드 | 운영 | **>150,000 노드에서 전체 metric sweep <20초.** 애플리케이션 코어를 훔치지 않음 |
| **JSC (LLview)** | resource manager/scheduler + 노드별 데몬, **분 단위 간격** *"to minimize computational overhead on nodes"* | — | — | JURI 기반 job 리포팅 포털; **role-based access**(user/support/admin) | 사용자·지원·관리자 리포트 | **3.4M metric(~600/node)**, **60초**, 보존 **14주–무기한**. **이상탐지 없음** |
| **TACC (HPCPerfStats)** | 노드 agent | RabbitMQ | PostgreSQL/Django + Redis/zstd | 야간 규칙 기반 저성능·오설정 job 플래깅 | 리포트 | 오버헤드 **1코어의 0.19% 평균 / 3.0% 피크**(Stampede3) |
| **EPCC ARCHER2** | Checkmk TCP agent(**관리·로그인 노드만, compute에는 없음**); **캐비닛 컨트롤러에서 rectifier 전력 5초마다**; `sinfo`; SSH 프로브; Lustre/HSN 검사 | 그룹별 Checkmk 서버 → Carbon | **Graphite** | Grafana + SAFE | 이메일 + HPE 페이저 | 5,860 노드 / 750,080 코어. **HPL 16.8 PF → 19.5 PF**(power-cycling 노드 격리 후). **실패 모드:** *"Historical Graphite data granularity reduces over time to conserve disk space"* — downsampling이 장기 세밀 분석을 파괴 |
| **BSC MareNostrum 5** | **EAR** — PCK·DRAM은 RAPL, full-node는 IPMI | — | — | EAR | 에너지 회계 | **주기 metric 1 sample/분(항상)**; job accounting 분 단위; **EARL 10초(6 samples/분, 사용자 opt-in)**. Prometheus/Grafana/Elasticsearch/DCDB 언급 없음 |
| **HPE HPCM 1.13 (제품 기본값)** | MMD(admin)/Sec(leader)/SMD(compute); **PCIM**(CDU/VCDU/PDU); EX 스위치의 **subsmon** Redfish 구독; **Slingshot Telemetry Agent**(HTTP streaming); WLM용 Telegraf; FMN | **Kafka** + Zookeeper + Confluent Schema Registry(Avro) + Kafka REST | **VictoriaMetrics**(vminsert/vmstorage/vmselect); **OpenSearch**(Fluent Bit + Logstash); TimescaleDB(deprecated) | **AIOps 컨테이너**: univariate + multivariate anomaly score; Alertmanager | Grafana/OpenSearch 대시보드, 이메일/Slack/webhook | 보존 기본값: **Kafka 1일; OpenSearch 7일; VictoriaMetrics 7일; TimescaleDB 30일**; ≤1.12에서는 CrayEX telemetry 24h, 나머지 168h; Timescale 압축이 7일에 **">90% disk space"** 절감; 모니터링 간격 예 **5초**; **Slingshot이 "the big hitter for disk space"**. **사이징 모델·확장 한계·예상 볼륨 미공개.** 스택 전환 기록: Prometheus/TimescaleDB → **VictoriaMetrics**; Filebeat → **Fluent Bit**; Elasticsearch → **OpenSearch**(라이선스 변경); Alerta/Elastalert → **Alertmanager only** |
| **HPE Fabric AIOps / CADDY** | Slingshot telemetry API | ETL → Ray in-memory actor | 계층적 Bin(counter당 **Welford 5-moment**) + 이력 디스크 | Python FAIO API, REST | 관리자 질의 | ingest **300K events/min**; **4,096 port**(8 group × 8 switch × 64 port); **counter 4종**(rxBW, txBW, rxCongestion, txCongestion); 압축 **425×(10분) / 600×(15분) / 1200×(30분)**; 단일 프레임 fetch **355 ms → 151 ms(group, −57%) / 267.51 ms(port, −25%)**; **ingest 오버헤드 +32.5%**(1M 이벤트당 0.7589 s → 1.007 s); live 시야 **10분 → 수일**; 권장 window **≤3시간**; 노드 = 128 AMD EPYC 7002 코어 / 196 GB. **단일 노드 평가만**; 극단 압축이 *"may reduce granularity for certain anomaly detection workloads"* |
| **ORNL Frontier 노드 스크리닝** | Slurm **backfill**을 통한 노드별 벤치마크(BabelStream, rocHPL, AMG, LAMMPS, oblex, rocPRIM) | Slurm | 결과 DB | 규칙 기반 pass/fail | drain / 수리 티켓 | 누적 **~600만** 단일 노드 테스트; 6개월 **190만**; **고유 실패 노드 99개**; LAMMPS **1 failure / 14,618 tests**; 실행시간 **24분(backfill) vs <1분(checknode)**; 주간 스크린 **39,437회 무수확 → 폐기**. 테스트별: BabelStream 562,671 실행/2,796 실패 · rocHPL 328,576/162 · AMG 337,684/129 · oblex 184,424/124 · rocPRIM 304,361/24 · LAMMPS 175,418/12 |
| **ORNL Frontier health/state** | `checknode` bash(boot + epilog); 컨트롤러·콘솔·syslog 위 SEC(Simple Event Correlator) | Slurm state | Slurm reason 필드 | 규칙 | drain + 자동 resume(자기가 설정한 이유일 때만) | **수치 미공개.** 맥락만: *"mean time between failure on a system this size is hours, it's not days"*. 구체 결함 1건: *"a bug in the power management firmware that prevented the CPU from going into burst mode"* → MPI all-to-all 저하 |
| **NERSC Slingshot fabric poller** | Fabric Manager REST API(health, switch, port) | K8s CronJob(Python, OCI) | **VictoriaMetrics** + **Loki** | metric 11종, 임계값 | 알림 | switch offline, port flapping, health degradation, API 소실 탐지. **폴링 간격·switch/port 수·볼륨 미보고.** 어려움: 비수치 health 상태 시각화, 장기 port 상태 이력 저장, Kafka 통합 |
| **Indiana University GPU accounting** | **pynvml**(DCGM 거부: *"too intrusive of a footprint to be viable for deployment"*), epilog 시점 | Slurm | **MariaDB** `AdminComment`(JSON), 4,000-record ring buffer | 오프라인 통계 | 리포팅 | 295,470 GPU job(2020-07~2023-03); **평균 GPU 이용률 11%**; **53%의 job이 GPU 미접근**; 미사용 제외 시 26%; 645개 애플리케이션(53% AI/ML, 그중 99.6% Python). 실패 모드: `AdminComment` **65,535자 제한**으로 장시간 다중 GPU job 절단; nvml `gpuUtilization`은 *"percentage of time that the GPU was active"*이지 코어 이용률이 아님 |
| **HPE Cray EX PM counters (노드 수준 원천)** | `bpmcdmod` 커널 모듈 → `/sys/cray/pm_counters/` | 공유 메모리, 캐시 | Slurm / `cray_pm`이 소비 | — | job별 에너지 | **10 Hz** 갱신(`raw_scan_hz`); J/W/°C, µs 타임스탬프(v3+); EX254n **34 counter 파일**(4× GH200), EX255a **20 counter 파일**(4× MI300a), **"Precision input power monitoring and reporting ≤ 2%"**. 제한: **10Hz 이상의 socket·component 수준 전력·에너지·열 데이터**는 파트너 컴포넌트에 한해 접근 제한 |
| **NERSC all-flash Lustre** | obdfilter-survey(매일 off-hours); IOR | — | — | CoV **≤8%** 목표 | 튜닝, OST 수리 | 36 PB, >7 TB/s 이론, 16 MDS, 274→298 OST, 3,480 NVMe, ~10,000 사용자(기본 쿼터 20 TB / 20M inode); probe가 **32 GPU 노드에서 ~250 TB** 읽기/쓰기; 느린 OST **예상 대비 25–50% 낮음**; 수정 후 **15.1 → 19.9 GB/s (+30%)**, 최소 **260 MB/s → 9,032 MB/s**; SafeRet 보안 패치 **−14%**; checksum 활성화 **−17%**(673320 ± 31779 → 554012 ± 37846 MB/s); 최적 fullness **약 75%**; purge horizon ~365일 |
| **ORNL Network Digital Twin** | MPI tracing(fi_hook, PMPI), SST DUMPI trace; power/cooling telemetry **15초** | — | — | SST Macro dragonfly DES; FTQ 히스토그램 **1 ms**; spyplot | 설계·내결함성 연구 | 9,408 노드, 80 group(관리 1, I/O 5, compute 74), 노드당 NIC 4; **스위치 지연 100–350 ns**; 전체 Frontier 단일 rank replay **>30시간**(2시간 job 제한 대비); SST-Core **~7배** 가속으로도 부족; **~180만 Frontier job**; **~6개월 telemetry replay**; **정확도 수치 없음**; NIC spyplot 검증 미해결 |

## 5.2 독일 8개 국가센터 비교표 (Suarez et al., Frontiers in HPC 2025, Table 4)

**동종 국가센터 간에 공개된 유일한 나란한 모니터링 비교표다.**

| Center | Metrics | Interval | Retention/Storage | Stack |
|---|---|---|---|---|
| **JSC** | **3.4M (~600/node)** | 60 s | 14주–무기한 | Prometheus, Promtail, Loki, Grafana, **LLview** |
| **LRZ** | **8M (56/node + 12/core)** | **0.1–30 s** | 30일; sub-sample 무기한 | **DCDB**, MQTT, Cassandra, Grafana |
| **DKRZ** | **960k (42/node + 9/socket + 2/core)** | 1–60 s | 메타 무기한; metric **6개월** | Collectd, Prometheus, **ClusterCockpit**, Elasticsearch, Grafana |
| **FAU** | **660k (8/node + 7/core + 3/socket + 6/GPU)** | 60 s | job 데이터 무기한 | **ClusterCockpit**, NATS, Grafana, Munin |
| **HLRS** | **500k** | 1–120 s | 8주–무기한 | Collectd, Telegraf, **LDMS**, Kafka, BarrelEye, TimescaleDB, Influx, OpenSearch, MS SQL, Grafana |
| **TUD** | **330k (24/node + 4/core + 4/GPU)** | **0.25–30 s** | 무기한 | **MetricQ**, RabbitMQ, **PIKA**, Grafana |
| **KIT** | **115k (144/node)** | 30 s | 3개월 | **JobMon**, ClusterCockpit, InfluxDB |
| **MPCDF** | **100k (40/node)** | 3–240 s | 무기한 | **hpcmd**, rsyslog, **Splunk**, PDF 리포트 |

> **동종 국가센터 사이에 metric 수가 100k→8M(약 80배), 샘플링 간격이 0.1초→240초(약 2,400배) 벌어져 있다.** LRZ는 0.1초, TUD는 0.25초로 sub-second를 수집하고 JSC·FAU는 60초를 쓴다 — **어느 쪽도 정당화하는 발표된 연구가 없다.** CINECA는 sub-second 데이터를 artifact로 판단해 **폐기**했다.
> 그리고 같은 논문의 결정적 문장: ***"Machine Learning on the time series data is feasible but challenging. There are ongoing investigations how ML can be used to provide additional insights, but none of the German sites in this study are using this in production at present."***

## 5.3 코퍼스가 실제로 정량화하는 비용 범주 vs 아무도 정량화하지 않는 것

**정량화됨:** 데이터 볼륨(STREAM, CADDY, ORNL 전체) · 처리량 한계(OMNI, telemetry-api) · 압축률(CADDY 1200×; Timescale >90%) · 질의 지연(CADDY) · ingest 오버헤드(CADDY +32.5%) · 보존 기본값(HPCM) · 폴링 비용(`dump_counters` 0.5초) · 타임스탬프 동기(수 밀리초) · agent 오버헤드(DCGM은 정성적 거부, TACC은 0.19%로 정량) · schema 진화(STREAM) · downsampling 손실(ARCHER2/Graphite)

**아무도 정량화하지 않음:** **metric cardinality**(series 수를 보고한 사이트 0곳) · **샘플링 오버헤드 측정 방법론**(*"no statistically significant performance penalty"* 주장에 뒷받침 수치 없음) · 대규모 질의 비용 · **metric별 value-of-information** · **모니터링 TCO**

---

# 6. Vendor claims audit

열: documented feature | documented algorithm | quantitative evaluation | peer review | production deployment evidence

| 주장 | Feature | Algorithm | Quant. eval | Peer review | Production 증거 |
|---|---|---|---|---|---|
| **HPE HPCM "AIOps" anomaly detection** (CUG2025 tut106; CUG2022 BoF) | **YES** — *"real-time and offline anomaly detection, prediction for time-series monitoring data"*, uni/multivariate, 컨테이너, anomaly score 임계값, Grafana 패널, `cm monitoring grafana dashboard enable [category]` | **NO** — *"machine learning and deep learning technologies"*, 명명된 것 없음 | **NO** | **NO** | 예시 스크린샷만(CDU valve position, cooling pressure, CPU/GPU temp). 사이트·규모·FP rate 없음 |
| **HPE "AIOps: Leveraging AI/ML for Anomaly Detection in System Management"** (CUG2021, NREL 배포 주장) | YES | **UNKNOWN — PDF 미게시** | UNKNOWN | NO (CUG paper track) | 프로그램 문구가 NREL을 인용; 관련 NREL 보고서 **NREL/TP-2C00-79712 (2021)**는 기관 기술보고서이며 초록에 *"training models to operate on real-time data collected from both IT and facilities sources"*만 있고 **알고리즘·데이터셋·지표 없음** |
| **HPE Fabric AIOps / CADDY** (CUG2024) | YES | **YES** — Welford online moment, 계층적 metadata-indexed bin, Ray | **YES — 실제 수치를 가진 유일한 벤더 artifact**(압축·지연·오버헤드, §5.1) | NO | **testbed만** — *"Single node… telemetry modeled after HPE Hotlum (1024-node)"*. **production 배포 아님** |
| **HPE trellis** (CUG2021) | YES | 시각화·집계만; ML은 명시적 future work(*"we plan to investigate advanced machine learning models"*) | **NO** — *"no quantitative performance benchmarks, accuracy metrics, or comparative evaluations"* | NO | 1024노드 내부 시스템(640노드 사용), 1 Hz, 4시간 수집. 30일 raw telemetry가 *"several petabytes"* |
| **HPE Powersched** (CUG2023) | YES | **YES** — mean-shift clustering, 4블록 37 PMU 이벤트, silhouette 0.85 vs DBSCAN 0.62 | **YES이지만 매우 작음** — 평균 에너지 절감 14.382%, 평균 런타임 연장 1.65%(범위 8.18–18.46% / 0.28–3.09%) | NO | **2 노드**, DL385 Gen10, InfiniBand. 저자 자인: *"the results come from an early prototype"* |
| **HPE Hardware Triage Tool** (CUG2024) | YES | 규칙 기반 YAML decision tree; **명시적으로 ML 아님** | **NO** — 결함률·정확도·triage 시간 데이터 전무 | NO | Frontier 맥락 인용(9,400+ 노드, 150,000+ 컴포넌트), 결과 데이터 없음. 저자 자인: *"not a substitute for the discipline of system health checks"* |
| **HPE Cray EX PM Counters** (CUG2024) | YES — 문서화 양호 | N/A(추론이 아니라 계측) | 부분 — 10 Hz, EX255a에서 ≤2% 정확도 | NO | 제품 기능, 광범위 배포 |
| **HPE Swordfish/Redfish + ClusterStor** (CUG2024) | 프로그램에 주장됨 | **CONTENT NOT RETRIEVABLE** — file1 404, file2 사실상 비어 있음 | UNKNOWN | NO | UNKNOWN |
| **NVIDIA Mission Control** (docs.nvidia.com/mission-control) | YES — *"Autonomous Recovery Engine"*, 자율 job·하드웨어 복구, runbook, NVIDIA Resiliency Extension(NVRx), BCM, Run:ai, **NetQ** *"unified observability across NVLink and Ethernet"*, Grafana | **NO** | **NO** | **NO** | 문서가 설치·라이선스 지향. ⚠ 마케팅 페이지 2종(`/data-center/gb200-nvl72/mission-control/`, `/data-center/products/mission-control/`)이 **404** — 감사는 docs 사이트에만 근거 |
| **DDN Insight** (ddn.com/products/insight/) | 마케팅 수준만: *"Disruption Prevention"*, *"Proactive Issue Anticipation"*, *"Insight-Driven Productivity"*, *"Decision-Making Optimization"*, *"continuous real-time monitoring"* | **NO** | **NO** | **NO** | **명명된 배포 없음.** 카테고리 포지셔닝에도 불구하고 페이지에 **명시적 AI/이상탐지/예측분석 주장이 없다** |
| **Intel, VAST, 기타** | **NOT COVERED** — WebSearch 예산 소진 | — | — | — | 미완 작업 |

> **결론: 검토한 벤더 항목 11건 중 알고리즘과 정량 평가를 모두 갖춘 것은 1건(CADDY)이며 그것도 단일 노드 testbed다. peer-reviewed validation을 갖춘 것은 0건. 운영자 관련 성과 지표(precision, recall, alert volume, MTTR delta)로 production 평가를 제시한 것도 0건.**
> 반복되는 패턴: **feature는 문서화 → algorithm은 비공개 → evaluation은 부재 → deployment는 유명 시스템 이름과의 근접성으로 암시.** **어느 것도 research evidence로 인용하지 말 것.** *engineering* 증거로 인용할 만한 유일한 예외는 CADDY의 압축·지연 표다.

---

# 7. Center별 프로덕션 증거 요약

## 7.1 비교표

| Center | Flagship | Telemetry stack (배포됨) | 보고된 데이터 볼륨 | **검증된** production 최고 L-level | 공개 데이터셋 | 최강 발표 |
|---|---|---|---|---|---|---|
| **OLCF** | Frontier (9,408n / 37,632 MI250X) | Kafka(STREAM) → Elasticsearch/Druid/Parquet-MinIO → Spark → Grafana/LVA; OpenShift+SLATE; MLflow/DVC | **4.2–4.5 TB/day**; STREAM 1.3 TB/day, 300M msg/day, 223 topic | **L3**(결정적 노드 스크린, 190만 테스트); L4 협소(job power NN clustering); L5 사람 보조 | ✅✅ Constellation: Summit power/thermal 1 Hz; Summit GPU DBE+XID; Frontier HPL power | Shin et al., SC-W'24 (`10.1109/SCW63240.2024.00226`) |
| **NERSC** | Perlmutter | OMNI: RabbitMQ/Prometheus/Kafka → Elasticsearch + VictoriaMetrics → Promxy/Alertmanager → Grafana + **ServiceNow**; PM에 LDMS | 522B 레코드 / **125 TB** / **25k pts/s**(2019); 25k msg/s, 20k+ 센서(2020) | **L7 부분** — 사전 분류된 노드·스토리지 장애에 대한 **규칙 기반 자동 remediation** | ❌ 없음 | Sukhija, Bautista et al., MEDES'20 (`10.1145/3415958.3433046`) |
| **SNL** | ACES/CTS 클러스터 | **LDMS/OVIS** + syslog-ng + SOS/DSOS → portal/notify | **~수십 TB/day**; 1만 코어에서 10만 metric-value/s를 **<0.2%**로 | **L2**; L3 주장(이상탐지, 이벤트 상관)은 증거 빈약 | ❌ (HPC-ODA에 기여) | Agelastos et al., **SC14** (LDMS) — 여기서 유일한 SC 본트랙 논문 |
| **LLNL** | El Capitan | LDMS(5초) + Kafka + VictoriaMetrics + Elasticsearch + Grafana on K8s/OpenShift | Kafka 100k–1M msg/s(공동 수치) | **L2** | ❌ | CUG2023 LLNL-CONF-847852(4개 기관 공저) |
| **LANL** | Crossroads | 공개 문서 없음 | — | **UNKNOWN — 부여하지 말 것** | ✅ 역사적: USRC failure data 1996–2005; Trinity SEDC 2016-02 | USRC 데이터 포털 |
| **ALCF** | Aurora | 공개 문서 없음 | — | **UNKNOWN** | ✅ ALCF Data Catalog 2008–2025(**구독 필요**) | IEEE DataPort `10.21227/bhfr-wx19` |
| **TACC** | Frontera / Stampede3 | **HPCPerfStats** → RabbitMQ → PostgreSQL/Django + Redis/zstd | 오버헤드 1코어의 **0.19% 평균 / 3.0% 피크**(Stampede3) | **L3-lite**(야간 규칙 기반 저성능·오설정 job 플래깅) | ❌ | Evans et al., HUST@SC14 (`10.1109/HUST.2014.7`) |
| **CSCS** | Alps (~10k GH200) | **EMOI**: SMA→Logstash→Kafka(Strimzi)→KafkaStream→Logstash+Memcached→Elasticsearch/Kibana/Grafana on RKE2 | **미공개** (PM counter 10 Hz; telemetry ~1 Hz) | **L1–L2**; **명시적으로 ML 없음** | ❌ | Benini et al., CUG2024 (EMOI) |
| **LRZ** | SuperMUC-NG | **DCDB + Wintermute**: pusher→MQTT→collectagent→Cassandra→Grafana | **8M metric**, 0.1–30초, 30일 보존; Wintermute 오버헤드 <0.5%, <25 MB | **L2** production; L3/L4는 in-band 프레임워크로 시연(RF power 예측 6.2% 오차 @250 ms; 시간별 BGM clustering)되었으나 **ML이 운영 의사결정에 들어가지 않음** | ✅✅ **HPC-ODA** (`10.5281/zenodo.3701440`, CC-BY-4.0) | Netti et al., HPDC'20 (`10.1145/3369583.3392674`) |
| **CINECA** | Marconi100 / Leonardo | **ExaMon**: 플러그인→MQTT→KairosDB→Cassandra→Grafana | **49.9 TB / 934일**, 573 metric, 1초 | **L2**; L3/L4는 프로토타입만 (RUAD **AUC 0.57**) | ✅✅✅ **M100 ExaData**, Zenodo DOI 12개, CC-BY-4.0 | Antici/Borghesi/Bartolini et al., *Sci Data* 10:288 (2023) |
| **RIKEN R-CCS** | Fugaku (>150k 노드) | Prometheus + Elasticsearch/Logstash/Kibana + Grafana; A64FX **assistant core**의 agent | **150k+ 노드에서 <20초** ingest 지연 | **L1** | ✅✅ **F-DATA** (`10.5281/zenodo.11467483`, 2,400만 job, 45 feature) | Terai et al., ISC'21 (`10.1007/978-3-030-90539-2_24`) |
| **JSC** | JUWELS / JUPITER | Prometheus, Promtail, Loki, Grafana, **LLview** | **3.4M metric**(~600/node), 60초, 14주–∞ | **L2** + 에너지 작동(유휴 노드 전원차단; JUSUF 전년 대비 **−25%**) | ❌ | Suarez et al., Front. HPC 2025 (`10.3389/fhpcp.2025.1520207`) |
| **BSC** | MareNostrum 5 | **EAR**(RAPL + IPMI); 더 넓은 스택은 공개 문서 없음 | 주기 1 sample/분; EARL 10초 | **L1** 검증 | ❌ | Banchelli et al., FGCS 2025, arXiv 2503.09917 |
| **EPCC** | ARCHER2 | **Checkmk → Graphite → Grafana + SAFE**; agent는 관리·로그인 노드에만 | rectifier 전력 **5초** | **L2** | ❌ | Leach et al., CC:P&E 2024 (`10.1002/cpe.7892`) |
| **NREL** | Kestrel | 공개 문서 없음 | — | **UNKNOWN** | ✅ **Eagle jobs**, 1,100만+ job, CC-BY-4.0 | Duplyakin & Menear, OEDI 5860 (2023) |
| **DKRZ / HLRS / FAU / KIT / MPCDF / TUD** | Levante, Hawk 등 | §5.2 Table 4 참조 | 100k–960k metric; 3개월–∞ 보존 | **L2**; *"none… using [ML] in production"* | ❌ | Suarez et al., Front. HPC 2025 |
| **Pawsey / CSC-LUMI / KAUST** | Setonix / LUMI / Shaheen III | — | — | — | ❌ | **`NO PUBLIC PRODUCTION EVIDENCE FOUND`** |

> ⚠ **Pawsey·CSC/LUMI·KAUST의 `NOT FOUND` 판정은 검색 예산 소진 상태의 잠정 결론이다.** 특히 LUMI는 규모와 EuroHPC 위상을 감안하면 실질적이고 주목할 만한 발표 공백으로 보이나, 단정하지 말 것. KAUST에서 확인된 유일한 실질 artifact는 **범위 이전**의 것이다: *Jobs I/O monitoring for Lustre at scale*, CUG2016 BoF.

## 7.2 연구를 내는 센터 vs 실무만 내는 센터 — 세 가지 발견

**진짜 연구를 발표하는 곳:** **LRZ**(HPDC'20, SC'19, Cluster; ML 벤치마크 데이터셋을 목적 구축해 공개. 온라인 ODA *프레임워크*를 연구 기여로 만들고 production 소프트웨어로 출하한 유일한 센터) · **CINECA**(단, 저자 목록을 **University of Bologna**가 지배한다. CINECA는 기계와 데이터를 대고 Bologna가 논문을 쓴다) · **RIKEN R-CCS**(F-DATA도 다시 Bologna 경유. RIKEN 자체 기여인 Terai et al.은 ISC *워크숍* 시스템 개요 논문) · **ORNL/OLCF**(양다리. ICS'24 GPU memory corruption은 진짜 연구 논문이며 학술 파트너는 **William & Mary**) · **SNL**(연구 수준이지만 대표작이 **SC14**. **12년간 SC 본트랙 후속 없음**)

**실무만 발표하는 곳:** CSCS, EPCC, LLNL, NERSC(대체로), TACC(2016 이후), LANL, HLRS, KIT, MPCDF, DKRZ, JSC. **CUG가 지배적 출구**이며, CUG2024/2025 모니터링 세션은 압도적으로 **HPE 저작**(Power Monitoring Counters, CADDY, Swordfish/Redfish, SDU/Metis, EVeREST)이고 센터는 공저자나 소비자다.

**세 가지 발견:**
1. **이 작업 중 거의 아무것도 SC Technical Program에 도달하지 않는다.** 2020–2026 전 구간에서 이들 센터로부터 production HPC 운영 분석을 다룬 **SC 본트랙 technical paper를 0편** 찾았다. 좋은 작업은 SC *Workshops*, CUG, HPCSYSPROS, ISC workshops, HPDC, ICS, *Scientific Data*로 간다. **이것은 실체의 부재가 아니라 구조적 기회다.**
2. **연구 산출은 시스템 규모가 아니라 학술 파트너와 상관된다.** Bologna↔CINECA, Bologna↔RIKEN, W&M↔ORNL, Basel/TUM↔LRZ, UMD(Bhatele)↔NERSC. 대학 그룹이 결합되지 않은 센터는 실무만 낸다. → **KISTI에게 가장 레버리지 높은 기관적 조치는, 파이프라인을 설계하기 *전에* 대학 ML 그룹을 운영 데이터에 계약으로 결합시키는 것이다.**
3. **데이터 공개와 연구 산출이 거의 완벽하게 상관된다.** 연구를 내는 모든 센터(ORNL, LRZ, CINECA, RIKEN, NREL, LANL, ALCF)가 데이터를 공개했다. 실무만 내는 모든 센터(CSCS, EPCC, JSC, LLNL, TACC, NERSC, CSC, Pawsey)는 공개하지 않았다. **공개가 결과가 아니라 원인으로 보인다.**

---

# 8. 여러 센터가 독립적으로 지목한 미해결 문제 (연구 질문 신호)

독립적으로 같은 말을 한 센터 수로 순위를 매겼다.

### 1. Telemetry schema / semantics가 표준화되어 있지 않고, 대시보드와 모델이 시스템 세대마다 깨진다
*지목: ORNL(2회, 전용 HPCSYSPROS 논문 포함), LLNL, CSCS, LRZ, SNL*
> ORNL: *"Sensors, metrics, and telemetry data has not been standardized into a universal format."*
> ORNL/HPCSYSPROS: *"If the telemetry data schema changes, dashboards must be recreated using different sources, query languages, and metric names."*
> LRZ: *"a block template is not guaranteed to be portable across HPC systems with different sensor hierarchies."*
> CSCS: *"differences in how various architectures expose hardware data."*
> **연구 질문:** schema-and-semantics 계층(센서 온톨로지 + 자동 재바인딩)이 ODA 모델이나 대시보드를 시스템 교체에도 재작성 0으로 생존시킬 수 있는가 — 그리고 이를 *측정* 가능한가(예: Summit→Frontier, M100→Leonardo로 전이되는 모델의 %)? **M100 ExaData + HPC-ODA + Constellation으로 오늘 측정 가능하며, 아무도 하지 않았다.**

### 2. 벤더 telemetry가 가장 약한 고리다 — 불안정, 문서 부족, 확장 불가, 버전 지연
*지목: NERSC, LLNL, CSCS, ORNL*
> NERSC: telemetry-api가 *"unreliable and often inefficient… stopped feeding data at random times."*
> LLNL: CSM LDMS가 *"significantly behind the latest LDMS release."*
> CSCS: 번들 SMA Kafka가 *"does not expose any external listener."*
> ORNL: *"Securing vendor cooperation for unplanned sensor implementation can be difficult."*
> **연구 질문:** 동일 노드에서 벤더 제공 telemetry 대비 독립 수집기의 *측정된* 완전성·충실도 손실은 얼마이며, 그 손실이 하류 모델 정확도에 무엇을 하는가? **telemetry 품질 벤치마크를 아무도 발표한 적이 없다. 방어 가능한 SC 논문 형태 — telemetry integrity / observability-debt 지표.**

### 3. 병목은 데이터가 아니라 label이다
*지목: SNL, ORNL, CINECA, 독일 전 사이트*
> SNL: ***"Getting data is not a challenge!"*** — 필요한 것은 *"validated, explainable machine learning."*
> ORNL: ML 반복이 *"starved with unknown future data, low-yield features, rare events, and missing data."*
> CINECA: anomaly label이 15분 Nagios 입도에만 존재; 비지도 **AUC 0.57**.
> **연구 질문:** HPC 운영 anomaly를 위한 weak/programmatic supervision — 티켓 시스템, 노드 drain 이벤트, job exit code를 확률적 label로 합성하여 M100 ExaData에서 0.57 비지도 baseline을 이길 수 있는가? **깨끗하고 재현 가능하며 임팩트 높은 목표.**

### 4. 수집한 데이터 중 무엇이 실제로 쓰이는지 아무도 모른다 — 대량의 미사용 데이터 축적
*지목: ORNL(명시적), Suarez et al.의 100k→8M 격차가 함의*
> ORNL: *"there is a notable gap in the end-to-end understanding of how the data is used, resulting in the accumulation of unused data and uncoordinated efforts."*
> **연구 질문:** metric utility attribution — 각 스트림을 운영 의사결정에 대한 한계 기여도로 순위 매기고, 스트림별 원칙적 보존·샘플링 정책을 도출. **ORNL 자신의 스트림 간 30만 배 볼륨 격차를 감안하면 utility-per-byte 분석은 즉시 실행 가능하고 완전히 새롭다. 이 세트에서 가장 강한 SC-Technical-Paper 기회로 판단된다.**

### 5. HPC 운영 시계열 위의 ML은 가능하지만 production 수준이 아니다 — 8개 센터 컨소시엄의 공식 진술
*지목: 독일 전 센터, CSCS, CINECA, ORNL*
> Suarez et al.: ***"none of the German sites in this study are using this in production at present."***
> Suarez et al.: *"Due to the varying length and number of resources used, machine learning (ML) on the time series data is feasible but challenging."*
> **연구 질문:** 파일럿→production 전환을 구체적으로 무엇이 막는가? 하드웨어 drift 하의 모델 수명주기, alert-fatigue 경제학, 운영자를 위한 설명가능성 요건, 잘못된 노드 drain의 비용. **HPC AIOps를 위한 엄밀한 cost-of-error / operator-trust 프레임워크가 존재하지 않으며, 있으면 널리 인용될 것이다.**

### 6. 나쁜 하드웨어와 나쁜 코드 / 나쁜 사용자를 구별하기
*지목: ORNL(명시적), CSCS(암시적)*
> ORNL: 일부 에러 메시지가 *"either defective hardware or an application code bug"*에서 발생; *"Discovering trends in failures is one of the most important yet most difficult tasks."*
> CSCS: straggler와 저이용률이 *"unnoticed due to project time or expertise limits."*
> **연구 질문:** 시스템/애플리케이션 경계를 가로지르는 결합 귀속. **M100 ExaData(system+job)와 F-DATA(job+counter)가 이제 가능하게 만든 정확한 짝짓기가 필요하다.**

### 7. Sub-second 샘플링은 감당 가능하지만 그 값어치를 아무도 보이지 않았다
> LRZ는 **0.1초**, TUD는 **0.25초**로 샘플링하고 JSC와 FAU는 **60초**를 쓴다 — 동종 국가센터 사이의 **약 600배 불일치**이며, **어느 쪽도 정당화하는 발표된 연구가 없다.** CINECA는 sub-second 데이터를 artifact로 판단해 **명시적으로 폐기**했다.
> **연구 질문:** 샘플링률–탐지력 곡선. 각 운영 이벤트 클래스(열 위험, GPU DBE, straggler, 네트워크 저하)가 탐지 가능하게 남는 최소 샘플링률은? **한강의 저장 예산을 직접 결정하며, M100 ExaData의 1초 데이터를 decimation하여 답할 수 있다. 매우 실용적이고, 인용 가치가 높고, 센터 간의 실재하는 불일치를 해결한다.**

### 8. 운영 데이터가 어떤 시스템보다 오래 산다
*지목: ORNL만, 그러나 구조적으로 보편적*
> *"Challenge of achieving immediate data availability in the face of the relatively short lifespan of supercomputers"* — *"knowledge accumulation across generations to minimize re-work"* 필요.
> **연구 질문:** 운영 모델의 cross-generation transfer learning — Summit에서 학습한 모델이 Frontier에서 얼마나 살아남는가. **Constellation이 이제 부분적으로 검증 가능하게 만든다.**

---

# 9. Lineage — workshop / practice → archival

## 9.1 확인된 lineage 5건

**L-1. MODA21 → FGCS (저널 아카이벌). CONFIRMED.**
Molan, Borghesi, Beneventi, Guarrasi, Bartolini, *An Explainable Model for Fault Detection in HPC Systems*, MODA21, LNCS 12761 → Molan, Borghesi, Cesarini, Benini, Bartolini, ***RUAD: Unsupervised anomaly detection in HPC systems***, **FGCS 141 (2023)**, `10.1016/j.future.2022.12.001`(arXiv 2208.13169). 같은 그룹·같은 시스템(CINECA Tier-0 / Marconi100)·같은 문제. 워크숍판은 supervised+explainable, 아카이벌판은 label 의존을 제거. **저널이지 SC/HPDC/IPDPS가 아니다.**

**L-2. MODA22 → ACM Computing Frontiers. CONFIRMED.**
Seyedkazemi Ardebili, Bartolini, Acquaviva, Benini, *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems*, MODA22 → ***Multi-level anomaly prediction in Tier-0 datacenter***, **ACM CF 2022**, `10.1145/3528416.3530864`. 같은 저자·같은 Marconi100 열 데이터, 탐지→예측. **CF는 중간 티어 아카이벌이지 SC가 아니다.**

**L-3. MODA20 → IEEE CLUSTER 2021 + Parallel Computing. CONFIRMED.**
Ozer, **Netti**, Tafani, Schulz, *Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning*, MODA20 → **Netti** et al., ***A Conceptual Framework for HPC Operational Data Analytics***, **IEEE CLUSTER 2021**; *Operational Data Analytics in practice*, **Parallel Computing 113 (2022)**; 기반은 ***DCDB Wintermute***, **HPDC 2020**(`10.1145/3369583.3392674`).
**이 분야에서 가장 잘 실행된 workshop→archival→PhD 궤적**(Netti의 TUM 박사논문 2022, *Holistic and Portable Operational Data Analytics on Production HPC Systems*). ⚠ **Netti는 이후 이 분야를 떠났다**(2024–2026 산출은 위성·비지상 컴퓨팅). **이 라인에 후계자가 없다.**

**L-4. BU/Coskun anomaly-diagnosis 라인 → SC'23 regular paper. 시리즈로 CONFIRMED, workshop 기원은 `UNVERIFIED`.**
*Proctor*(**ISC High Performance 2021**, LNCS) → *E2EWatch*(**Euro-Par 2021**) → ***Prodigy***, **SC'23 본프로그램**, `10.1145/3581784.3607076`. 이 그룹이 현재 **HPC-ODA 2026을 공동 의장**한다(Ayse Coskun).

**L-5. Frontier/ExaDigiT 운영데이터 라인 → SC24 regular paper. 아카이벌 CONFIRMED, workshop 선행 NOT FOUND.**
Brewer, Maiterth, Kumar, Wojda, Bouknight, Hines, **Shin**, Greenwood, Grant, Williams, Wang, ***A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale***, **SC24**, `10.1109/SC41406.2024.00029`. 관련: Oles, Schmedding, Ostrouchov, **Shin**, Smirni, Engelmann, *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*, **ICS'24**, `10.1145/3650200.3656615`.
ExaDigiT로 자라난 workshop 논문을 **찾지 못했다.** ORNL 그룹의 워크숍 존재감은 **ODA BoF**(비아카이벌)와 HPCSYSPROS(Zenodo 전용)에 있다. **Woong Shin이 MODA26에서 "The Past, Current, and Future of HPC ODA"로 keynote를 했다 — 흐름이 archival-first, workshop-as-community, 즉 통상과 *반대* 방향이다.**

## 9.2 명시적 부정 결과

- **PIKA(TU Dresden), LLview(JSC), XDMoD Application Kernels(Buffalo), Arbiter(Utah), EMOI(CSCS), CEEMS(CNRS), buildtest(NERSC), Ramble(Google), ORNL ODA 대시보드** — 어느 것에도 SC/HPDC/IPDPS/Cluster/DSN regular 논문이 **없다.** Arbiter의 유일한 비워크숍 출구는 **PEARC**(실무 학회)다.
- **2020–2025 HPCSYSPROS 논문 중 검토한 어느 것도 추적 가능한 아카이벌 후속이 없다. 46편, 승격 0건.**
- **2023–2025 HPCTESTS 논문 중 아카이벌 후속이 있는 것이 없다. 10편 이상, 0건.**

## 9.3 CUG 역검색 (R1–R10) — 운영 문제 → 가장 가까운 아카이벌 연구

**모든 아카이벌 인용은 Crossref 또는 usenix.org로 검증되었다.** `NO CLOSE ARCHIVAL WORK FOUND`는 *"이 세션의 검증 범위에서 발견되지 않았다"*는 뜻이며 강한 시사이지 증명은 아니다.

| # | CUG 운영 문제 (출처) | 추상화 | 가장 가까운 아카이벌 | 판정 |
|---|---|---|---|---|
| **R1** | 유휴 용량이 희소한 조건에서의 bad-actor 노드 스크리닝 정책 (P6) | 순차 실험 설계 — backfill 용량 위에서 어떤 노드 테스트를 얼마나 오래 실행해 node-hour당 결함 발견을 최대화할 것인가. 검출률이 **1/14,618**로 낮음 | 신뢰성 *특성화*만: Ostrouchov et al., *GPU Lifetimes on Titan Supercomputer*, **SC20**, `10.1109/sc41405.2020.00045`; Nie, Xue, Gupta, Patel, Engelmann, Smirni, Tiwari, *Machine Learning Models for GPU Error Prediction*, **DSN 2018**, `10.1109/dsn.2018.00022` | **NO CLOSE ARCHIVAL WORK FOUND** — 코퍼스에서 **가장 SC 논문 형태에 가까운 gap**이며, ORNL이 검증용 ground truth와 **negative baseline을 이미 발표**했다 |
| **R2** | 노드 격리 결정과 오탐 비용 (P6/P7) | 순차 가설 검정 / value-of-information으로서의 drain-vs-return | 인접하지만 다른 문제(lead time 있는 장애 예측): Das, Mueller, Siegel, Vishnu, *Desh*, **HPDC 2018**, `10.1145/3208040.3208051`; Das, Mueller, Rountree, *Aarohi*, **IPDPS 2020**, `10.1109/ipdps47924.2020.00115` | **NO CLOSE ARCHIVAL WORK FOUND** — HPC 노드 관리의 격리 결정 정책 / FP-FN 비용 비대칭 |
| **R3** | 취득 비용 하의 fabric counter 선택 (P4) | 포트당 1,000+ counter, 스위치당 64K, dump당 ~0.5초에서 폴링 비용당 진단 정보를 최대화하는 counter 부분집합·cadence 선택 | De Sensi et al., *An In-Depth Analysis of the Slingshot Interconnect*, **SC20**, `10.1109/sc41405.2020.00039`(특성화, telemetry 비용 미다룸); **Jha et al., *Measuring Congestion in High-Performance Datacenter Interconnects* (Monet), NSDI '20** — 네트워크 counter로 congestion region 탐지, **가장 가까운 방법론적 조상** | **부분.** Slingshot급 fabric에 대한 **counter 부분집합 선택을 최적화 문제로 다룬 연구 NOT FOUND** |
| **R4** | 유한 메모리 하의 인터커넥트 telemetry 스트리밍 요약 (P5) | 증명 가능한 오차 bound와 질의 지연 SLO를 갖는 sketch/moment 기반 다해상도 요약 | HPC venue에서 **없음.** CADDY(CUG2024, 벤더)가 가장 정량적이며 **아카이벌이 아니다** | **NO CLOSE ARCHIVAL WORK FOUND** — sketch 기계는 네트워킹/DB 커뮤니티에 있고, 운영자 대면 정확도 보증을 갖춘 HPC-fabric 구현은 열려 있다. **구체적 고리:** CADDY가 1200배 압축을 보고하면서 *"may reduce granularity for certain anomaly detection workloads"*를 인정 — **그 저하를 아무도 측정하지 않았다** |
| **R5** | 하류 분석 효용 대비 telemetry 보존·downsampling 정책 (P11/P14) | 알려진 결함 시그니처의 탐지 가능성을 보존하면서 저장·질의 비용을 최소화하는 metric 클래스별 보존·downsampling 선택 | 데이터를 저장하지만 보존을 최적화하지 않는 인프라 논문들: Agelastos et al., **SC14**, `10.1109/sc.2014.18`; Netti et al., **HPDC 2020**, `10.1145/3369583.3392674`; Bautista, Romanus, Davis, Whitney, Kubaska, **ICPP 2019 Workshops**, `10.1145/3339186.3339213` | **NO CLOSE ARCHIVAL WORK FOUND** — 분석 효용에 대한 제약 최적화로서 보존·downsampling을 다룬 연구. **훌륭한 SC 후보** — replay trace만으로 평가 가능하고 **벤더가 이길 기본값을 이미 공개**했다 |
| **R6** | control-plane telemetry 서비스 확장성과 backpressure (P2) | boot나 job launch를 교란하지 않아야 하는 10^5–10^6 msg/s 모니터링 plane의 end-to-end 흐름 제어·admission | LDMS SC14(전송 확장), Wintermute HPDC20(in-band analytics) — 둘 다 backpressure 미다룸 | **NO CLOSE ARCHIVAL WORK FOUND** — HPC 모니터링 control plane의 backpressure / 저하 모드 설계. CUG2023 증거(telemetry-api가 *Kafka rebalancing events* 유발, credential fetch로 boot 실패)가 **완성된 문제 진술** |
| **R7** | Telemetry schema 진화와 의미론적 drift (P1) | 버전화된 metric 의미론, schema-registry federation, 다년 운영 아카이브의 재처리 비용 | **없음.** STREAM이 고통을 문서화(재색인, federated schema registry에 프록시 필요, 필드가 *"change throughout the lifetime of the data"*)하지만 경험 보고서다 | **NO CLOSE ARCHIVAL WORK FOUND.** 강한 gap이며, **5–10년간 하나의 아카이브를 운영할 신규 센터에 직접 관련** |
| **R8** | job 수준 에너지·telemetry의 cross-source 귀속과 ground truth (P8/P15) | scheduler accounting, 노드 counter(10 Hz PM), 파이프라인 샘플 telemetry(~1 Hz)를 타임스탬프 동기 오차를 명시적으로 모델링하여 방어 가능한 job별 귀속으로 조정 | Klinkenberg, Terboven, Lankes, Müller, *Data Mining-Based Analysis of HPC Center Operations*, **CLUSTER 2017**, `10.1109/cluster.2017.23`; **Ahlgren et al.(29인, 다기관), *Large-Scale System Monitoring Experiences and Recommendations*, CLUSTER 2018, `10.1109/cluster.2018.00069`** — ⭐ **CUG 모니터링 커뮤니티 자신의 아카이벌 크로스오버이며, CUG 실무를 peer-review 기여로 전환한 최고의 선례** | **부분 커버리지. 조정/불확실성 정량화 프레이밍은 열려 있다** |
| **R9** | straggler 스토리지 타깃의 온라인 탐지·국소화 (P9) | 매일 능동 probing 없이 수동 telemetry만으로 298-OST all-flash Lustre의 OST별 성능 저하를 탐지·국소화 | Lockwood, Snyder, Wang, Byna, Carns, Wright, *A Year in the Life of a Parallel File System*, **SC18**, `10.1109/sc.2018.00077`; Jha et al., *Live Forensics for HPC Systems*, **SC20**, `10.1109/sc41405.2020.00069` | ✅ **CLOSE ARCHIVAL WORK EXISTS.** 기여는 all-flash/NVMe 특유의 장애 물리(garbage collection, trim cadence, *"surprising 75%"* fullness 최적점)로의 확장 — 더 좁고 여전히 발표 가능하나 **green field는 아니다** |
| **R10** | 10^8 시간척도 격차를 가로지르는 production telemetry 기반 네트워크 digital twin 검증 (P16) | ns 규모 스위치 거동과 15초 telemetry의 다해상도 융합; 운영 창에 맞는 시뮬레이션 가속; NIC 수준 트래픽 검증 방법론 | Brewer et al., **SC24**, `10.1109/sc41406.2024.00029`(facility/thermal twin — 같은 ExaDigiT 프로그램, 다른 서브시스템); De Sensi et al., **SC20** | **NO CLOSE ARCHIVAL WORK FOUND** — production Slingshot telemetry로 검증된 *네트워크* digital twin. **ORNL이 스스로 이를 지목했다** |

**증거는 있으나 아카이벌 앵커가 없는 추가 gap 2건:**
- **운영자 조치 가능 알림을 갖춘 CDU/cooling telemetry 이상탐지.** 방법은 아카이벌로 성숙: Borghesi, Bartolini, Lombardi, Milano, Benini, *Anomaly Detection Using Autoencoders in HPC Systems*, **AAAI 2019**, `10.1609/aaai.v33i01.33019428`; Tuncer et al., **ISC 2017**, `10.1007/978-3-319-58667-0_19`; Aksar et al., *Proctor*, **ISC 2021**, `10.1007/978-3-030-78713-4_11`. **빠진 것은 Cray EX 액냉 telemetry 위에서의 평가다** — 즉 gap은 방법이 아니라 증거다. **HPE는 정확히 이 기능을 발표된 평가 없이 출하한다(P10).**
- **Slingshot dragonfly에서의 job 이웃 간섭.** 조상: Bhatele, Mohror, Langer, Isaacs, *There goes the neighborhood: performance degradation due to nearby jobs*, **SC 2013**, `10.1145/2503210.2503247`. **Slingshot-11 시대의 등가물을 찾지 못했다.**

---

## 부록. 이 문서가 완료하지 못한 후속 작업

1. **CUG 2026 프로그램** — 차단/미게시. **2027년 초 재확인**
2. **Intel·VAST 벤더 감사** — WebSearch 예산 소진으로 미수행
3. **CUG 2024/2025 논문이 실제로 ACM ICPS에 실렸는지** — `UNVERIFIED`
4. **미게시 CUG PDF 5건** — CUG2021 HPE AIOps, CUG2021 Sandia system/application monitoring, CUG2022 Fallout, CUG2023 Slingshot Dashboard tutorial, CUG2024 Swordfish. **ORNL·Sandia·NERSC 저자는 요청 시 대개 공유한다 — 이메일 권장**
5. **LLNL "Sonar", CINECA production 배포 주장, ALCF 운영 스택, CSC/LUMI·Pawsey 모니터링 문서** — 충분히 검색하지 못함. 해당 `NOT FOUND`는 **잠정**
6. **`reports.alcf.anl.gov`가 egress 프록시에 차단** — ALCF 자체 공개 데이터 포털을 직접 확인할 것

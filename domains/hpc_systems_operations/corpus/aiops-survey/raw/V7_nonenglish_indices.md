# V7 — Non-English Indices Sweep (Korean / Chinese / Japanese)

**Purpose.** Close the language-coverage blind spot. Until this sweep, the audit searched
English-language indices only, and therefore could not legitimately assert that any body of
work "does not exist." This file records what was found, at what evidence depth, and — equally
important — which portals could and could not be reached, because that determines how strongly
the audit may word any negative claim.

**Date of sweep:** 2026-09-06
**Tooling:** WebSearch + WebFetch only (no curl/wget/scripted fetching, per constraint).
**Evidence labels:** `FULL-TEXT` / `ABSTRACT` / `TITLE-ONLY` / `RECORD-METADATA` / `NOT FOUND`.
All native-language titles are verbatim. All English renderings are marked either
**[pub-EN]** (the publisher's own English title, as printed on the record) or
**[my-TR]** (my translation, not authoritative).

---

## 0. Headline

Three things were established.

1. **Korean (the priority section): a substantial, continuous, Korean-language-only
   operational-analytics program exists at KISTI's Supercomputing Infrastructure Center.**
   It runs from at least 2019 to 2026 (21 items recorded below), is published almost entirely
   in the **한국정보처리학회 학술대회논문집 (KIPS Annual Conference proceedings)**, and covers
   precisely the audit's target topics: automated node health-checking, automated node
   recovery, automated failure notification, per-job power / GPU / I/O telemetry, scheduler-driven
   performance-data collection, monitoring-system design, and thermally-induced performance
   degradation with automated remediation. Most of it has **no English counterpart**, which is
   exactly why an English-only search missed it.

2. **Chinese: the Sunway (神威) builders publish substantial operational data in Chinese only.**
   In particular a 2021 reliability/availability paper reports a **measured MTBF of 11.84 h** for
   Sunway TaihuLight with a full hardware-failure attribution breakdown and a claimed ~70%
   fault-prediction accuracy. The Chinese-language successor of the Beacon NSDI'19 line
   (**Beacon+**, 2022) was also located.

3. **Japanese: operational analytics is present but thin and facility-weighted**, concentrated in
   IPSJ SIGHPC technical reports and in the university-IT venue 大学ICT推進協議会年次大会論文集
   (AXIES). J-STAGE contains essentially **no** HPC anomaly-detection or failure-prediction
   research — a real negative, though a partial one, because the IPSJ digital library and CiNii
   were both robots-blocked.

---

## 1. KOREAN FINDINGS  ★ priority section

### 1.1 The KISTI series — KIPS Annual Conference proceedings

Venue for every row: **한국정보처리학회 학술대회논문집** (Annual Conference of KIPS),
pISSN 2005-0011 / eISSN 2671-7298. DOI prefix `10.3745/PKIPS.*`.
Affiliation, where verified on the record: **한국과학기술정보연구원 슈퍼컴퓨팅인프라센터**
(Dept./Center of Supercomputing Infrastructure, KISTI). **★ = KISTI-affiliated, verified on record.**
**⬤ = concerns Nurion (누리온) or Neuron (뉴론) operations specifically.**

| # | Native title (verbatim) | English title | Authors | Yr | Pages / DOI | Depth | What it actually does |
|---|---|---|---|---|---|---|---|
| K1 ★⬤ | PBS 작업 스케줄러 Hook를 이용한 슈퍼컴퓨터 5호기 계산노드 자동 점검 기능 구현 | Implementation of automatic checking function of calculation node of Supercomputer 5th using Hook of PBS job scheduler **[pub-EN]** | 권민우(Kwon, Min-Woo); 윤준원(Yoon, JunWeon); 홍태영(Hong, TaeYoung) | 2019 | 101–102 / `10.3745/PKIPS.y2019m10a.101` | ABSTRACT | Automated compute-node health checking on **Nurion (8,432 compute nodes)** implemented as **PBS scheduler Hooks**, to cut operator response time. This is the "K-hook" later reported in English (see §1.3 E1). |
| K2 ★ | RESTful API를 이용한 슈퍼컴퓨터 서비스 데시보드 구축 | Building a supercomputer service dashboard using a RESTful API **[my-TR]** | 김성준(Kim, Sung-Jun); 홍태영(Hong, Tae-Young) | 2019 | 180 | RECORD-METADATA | Operations dashboard over supercomputer service data. |
| K3 ★⬤ | 효율적인 배치 작업 정보 관리를 위한 모니터링 시스템 설계 | Design of efficiency monitoring system for managing batch job information **[pub-EN]** | 김성준(Kim, Sung-Jun); 이재국(Lee, Jae-Kook); 홍태영(Hong, Tae-Young) | 2020 | 178–181 / `10.3745/PKIPS.y2020m11a.178` | ABSTRACT | Explicitly about **monitoring-induced load on the scheduler**: admins poll PBSPro and SLURM frequently for status and statistics, "빈번한 정보 요청은 작업관리 솔루션에 부하를 줄 수 있다"; proposes an efficient polling/monitoring design. Directly relevant to the audit's sampling-cost axis. |
| K4 ★ | 공동 활용 컴퓨팅 시스템에서의 사용자 작업별 전력 사용량 생성 기능 구현 | Implementation of per-user-job power consumption generation on a shared computing system **[my-TR]** | 권민우; 고동건(Ko, Dong-Geon); 윤준원; 홍태영 | 2020 | 24 / `10.3745/PKIPS.y2020m11a.24` | RECORD-METADATA | **Per-job power accounting** on a shared HPC system. |
| K5 | 클러스터 시스템에서 하드웨어 퍼포먼스 카운터 데이터 수집 방법 및 오버헤드 연구 | A study of hardware performance counter data collection methods and their overhead in cluster systems **[my-TR]** | 박근철; 박찬열; 노승우; 최지은 | 2020 | 106 / `10.3745/PKIPS.y2020m11a.106` | TITLE-ONLY (article page 5xx; affiliation NOT verified) | **Collection method *and overhead* for hardware performance counters** on a cluster. Directly on the audit's collection-overhead question. Worth re-chasing — affiliation unconfirmed. |
| K6 ★⬤ | 슈퍼컴퓨터 5호기 사용자의 작업별 IO 통계정보 획득 방안에 대한 연구 | A study on the method of acquiring IO statistical information for each user task of the KISTI-5 supercomputer **[pub-EN]** | 권민우; 윤준원; 홍태영 | 2021 | 6–8 / `10.3745/PKIPS.y2021m11a.6` | ABSTRACT (quantitative) | **The most telemetry-architecture-specific Korean item.** Records verbatim: Nurion = "8,437대의 계산노드와 33.88PB 규모의 병렬스토리지가 100Gbps의 Omni-Path(OPA) 인터커넥트로 연결"; compute managed by **PBS**; parallel storage monitored by **DDN Exascaler Monitoring System (ESMON)** writing read/write I/O statistics into **InfluxDB**. Joins scheduler accounting to storage telemetry to get per-job I/O. |
| K7 ★ | Performance Co-Pilot, Bpftrace, Grafana 기반 슈퍼컴퓨터 모니터링 및 성능 분석 시스템 구축 방안 연구 | A study on how to build a supercomputer monitoring and performance analysis system based on Performance Co-Pilot, Bpftrace and Grafana **[pub-EN]** | 곽재혁(Kwak, Jae-Hyuck), KISTI | 2021 | 118–121 / `10.3745/PKIPS.y2021m11a.118` | ABSTRACT | A **monitoring + performance-analysis stack design** (PCP / bpftrace / Grafana) for hundreds-to-thousands of nodes, motivated by the fact that "unexpected problems in certain nodes can lead to overall system performance degradation" — i.e. a **fail-slow** framing. No sampling interval or retention stated in the accessible abstract. |
| K8 ★ | 오픈소스를 이용한 KI Cloud 모니터링 기능 구현 | Implementation of KI Cloud monitoring using open source **[my-TR]** | 정기문; 조혜영 | 2021 | — | TITLE-ONLY | Prometheus/Grafana monitoring for KISTI's KI Cloud. |
| K9 ★ | 클러스터 시스템의 계산자원 활용률을 극대화하기 위한 작업배치스케줄러의 공유노드 정책 적용 방안 연구 | Applying a shared-node policy in the batch scheduler to maximise compute-resource utilisation **[my-TR]** | 권민우; 윤준원; 홍태영 | 2022 | — | TITLE-ONLY | Utilisation policy on PBS/SLURM. |
| K10 ★ | 공유노드 정책으로 운영 중인 클러스터 시스템에서 작업별 GPU 사용 통계 생성 방안에 대한 연구 | Generating per-job GPU usage statistics on a shared-node cluster **[my-TR]** | 권민우; 윤준원; 홍태영 | 2022 | — | TITLE-ONLY | **Per-job GPU telemetry** under a shared-node policy (SLURM). |
| K11 ★ | 작업관리 소프트웨어의 스케줄링 정책을 이용한 클러스터 시스템의 공정한 작업 실행 우선순위 관리 방안 연구 | Fair job-priority management using the scheduler's policies **[my-TR]** | 권민우; 윤준원; 안도식; 홍태영 | 2023 | — | TITLE-ONLY | Scheduling fairness policy. |
| K12 ★⬤ | 대규모 클러스터 시스템에서 배치작업 스케줄러를 활용한 성능 분석 데이터 수집 방법 연구 | A Study on Performance Analysis Data Collection Method Using Batch-job Scheduler on Large-Scale Cluster System **[pub-EN]** | 이재국(Jae-Kook Lee); 권민우(Min-Woo Kwon); 안도식(Do-Sik An); 홍태영(Taeyoung Hong) | 2023 | 37–39 / `10.3745/PKIPS.y2023m11a.37` | ABSTRACT | **Scheduler-driven, user-transparent profiling collection** ("without user intervention") on Nurion (>8,400 nodes) — profiling data captured during application execution via the batch scheduler. This is a telemetry-collection-architecture paper. |
| K13 ★ | GPU 클러스터 시스템의 계산노드 간 인터커넥트 네트워크 통신 성능 비교 분석 연구 | Comparative analysis of interconnect communication performance between compute nodes of a GPU cluster **[my-TR]** | 권민우; 안도식; 홍태영 | 2023 | — | TITLE-ONLY | InfiniBand cable/topology comparison. |
| K14 ★⬤ | 클러스터 시스템의 장애 발생 계산노드 자동 복구 기능 구현 | Implementation of automatic recovery function for computing node with failure of cluster system **[pub-EN]** | 권민우(Min-Woo Kwon); 안도식(Do-Sik An); 홍태영(TaeYoung Hong) | 2024 | 2–4 / `10.3745/PKIPS.y2024m05a.2` | ABSTRACT | **Automated remediation.** Auto-recovery of compute nodes suffering *software* failures on the **Neuron** GPU cluster, built by combining the **SLURM** batch scheduler with Linux **crontab**, to reduce failure response time. Funded under KISTI's "National Flagship Supercomputer Infrastructure Development and Services (2024)". |
| K15 | PCIe 서브시스템 모니터링 도구 구현 | Implementation of a PCIe subsystem monitoring tool **[my-TR]** | 차광호(Cha, Gwang-Ho) | 2024 | — | TITLE-ONLY | Real-time PCIe subsystem monitoring in HPC. |
| K16 ★ | 작업 배치 스케줄러와 컨테이너 오케스트레이션 툴을 활용한 이중 클러스터 서비스 환경 구현 | A dual-cluster service environment using a batch scheduler and a container orchestration tool **[my-TR]** | 권민우; 이국화; 안도식; 홍태영 | 2024 | — | TITLE-ONLY | SLURM + orchestrator dual-cluster operation. |
| K17 ★⬤ | GPU 온도 상승에 따른 어플리케이션 성능 저하를 해결하기 위한 자동화된 서버 관리 기능 구현 | Implementation of automated server management function to resolve application performance degradation caused by GPU temperature increase **[pub-EN]** | 권민우(Min-Woo Kwon); 이국화(Gukhua Lee); 홍태영(Taeyoung Hong) | 2025 | 19–21 / `10.3745/PKIPS.y2025m11a.19` | ABSTRACT | **Fail-slow / performance-variation detection with automated remediation.** Detects application performance degradation caused by rising **GPU temperature** on the **Neuron** cluster and takes automated server-management action. Threshold values and the exact action are in the full text (not retrieved). |
| K18 ★ | AI 기반의 HPC 환경을 위한 I/O 분석 모니터링 기법 연구 | A study of I/O analysis and monitoring techniques for AI-based HPC environments **[my-TR]** | 윤준원; 홍태영 | 2025 | 26 / `10.3745/PKIPS.y2025m11a.26` | RECORD-METADATA | I/O monitoring/analysis for AI workloads on HPC. |
| K19 ★ | GPU 클러스터 시스템의 장애 통보 자동화 기능 개발에 관한 연구 | A Study on the Development of an Automated Failure Notification Function for GPU Cluster Systems **[pub-EN]** | 권민우(Min-Woo Kwon); 홍태영(Taeyoung Hong) | 2026 | 35–37 / `10.3745/PKIPS.y2026m05a.35` | ABSTRACT | **Automated GPU-failure detection and user notification** implemented via the batch scheduler's **Epilog** hook. Abstract explicitly frames it against the forthcoming **국가슈퍼컴퓨터 6호기 (KISTI-6)** "초거대 GPU 클러스터", with Neuron in service since 2019 as the porting/experience vehicle. Directly load-bearing for the KISTI-6 AIOps roadmap. |
| K20 ★ | 대형 클러스터 시스템의 작업 배치 스케줄러 확장성 검증 기법에 관한 연구 | A study on scalability-verification techniques for the batch job scheduler of large cluster systems **[my-TR]** | 권민우; 홍태영 | 2026 | 38 / `10.3745/PKIPS.y2026m05a.38` | RECORD-METADATA | Scheduler scalability verification ahead of KISTI-6. |
| K21 ★ | 분산 컴퓨팅 관리 도구를 활용한 이기종 시스템 프로비저닝 설계 및 구현 | Design and implementation of heterogeneous system provisioning using a distributed computing management tool **[my-TR]** | 정대용; 최지우; 안도식; 이재국 | 2026 | — | TITLE-ONLY | Provisioning/config management for heterogeneous clusters. |

Also present in the same proceedings and adjacent but **not** operational analytics (recorded so the
audit does not mistake them for hits): 누리온 All-Reduce evaluation (명훈주·정기문, 2020);
슈퍼컴퓨터 누리온을 활용한 전산구조공학 성능 비교 연구 (이재국·안도식·홍태영, 2020);
누리온 시스템 상에서 거대 규모 딥러닝 수행 연구 (명훈주, 2019); 고성능 I/O 지원을 위한 계층형
스토리지 구현 (윤준원·홍태영, 2023); 대규모 병렬 파일시스템에서 분산 메타데이터의 성능 영향 분석
(윤준원·홍태영, 2026); 웹 기반 슈퍼컴퓨터 서비스 포털 (박주원·우준·홍태영, 2024).

### 1.2 Korean journal papers (KCI-indexed)

| # | Native title | English title | Authors / affiliation | Venue | Yr | Record | Depth | Note |
|---|---|---|---|---|---|---|---|---|
| K22 | 배치 작업 로그 분석을 통한 스케줄링 최적화 연구 | Scheduling Optimization Research through Batch Job Log Analysis **[pub-EN]** | 윤준원(Yoon Jun-won), **KISTI**; 송의성(Song Ui-sung), 부산교육대학교 | 디지털콘텐츠학회논문지 (J. Digital Contents Society) 18(7) | 2017 | pp. 1411–1418; DBpia `NODE07271965`; ScienceON `JAKO201707153703653` | ABSTRACT | **Job-log analytics.** Analyses scheduler execution logs for user success rate, execution time, wait time and resource scale, to inform scheduling-algorithm choice. Fields cited: job scripts, environment variables, libraries, wait time, start/end time, success rate, duration, utilisation. |
| K23 | HPC 환경에서 사용자 로그 분석을 통한 작업 성공률 개선 | Improving the Job Success Rate through Analysis of User Logs in HPC **[pub-EN]** | **NOT VERIFIED** — record page fetch failed | 디지털콘텐츠학회논문지 (J. Digital Contents Society) | c. 2015 | KCI `ART002047779`; KoreaScience `JAKO201501256374291` | RECORD-METADATA (title + venue only) | **Job-failure / success-rate analysis from user logs.** Almost certainly the same 윤준원 line, but authors, year and pages are **unverified** — KCI is robots-blocked and the KoreaScience article page returned 5xx on two attempts. Flagged for re-chase. |

### 1.3 English counterparts — the pairing question

The task asked, for each Korean paper, whether an English version exists. Result:

| # | English publication | Pairs with | Note |
|---|---|---|---|
| E1 | Jae-Kook Lee, Min-Woo Kwon, Do-Sik An, Junweon Yoon, Taeyoung Hong, Joon Woo, Sung-Jun Kim, Guohua Li, **"Improvements to Supercomputing Service Availability Based on Data Analysis"**, *Applied Sciences* 11(13):6166, 2021, DOI `10.3390/app11136166`. Affiliation: National Supercomputing Center, KISTI. | **K1** (and thematically K3) | ABSTRACT/FULL. Nurion = 8,305 KNL + 132 Skylake nodes under PBS Pro; **full-year 2019 job-scheduler logs**; the **"K-hook"** deployed from May 2019 is the PBS-hook mechanism of K1. Reports **25.6% of jobs failed**, decomposed as program errors 44.4%, PBS scheduler errors 37%, I/O errors 12.6%. |
| E2 | Ju-Won Park, Xin Huang, Jae-Kook Lee, Taeyoung Hong, **"I/O-signature-based feature analysis and classification of high-performance computing applications"**, *Cluster Computing*, version of record 2023-09-24 (preprint Research Square `rs-3329294`). | K6, K12, K18 (thematic only) | ABSTRACT. Nurion (~8,400 nodes, ~20 PB); **7 months of monitoring data, Aug 2021 – Mar 2022**; ML classification of applications from I/O signatures, >90% accuracy. No Korean companion cited. |

**Pairing verdict.** Only a *minority* of the Korean operational stream has an English counterpart.
K1 → E1 is a clear domestic-then-international pairing (and E1 is the citable form of the K-hook
work). But for K4, K6, K7, K10, K12, K14, K17, K19, K20 no English version was found by targeted
author search. **This is the substantive reason the English-only audit under-counted KISTI:** the
operations engineers (권민우 / 이재국 / 안도식 / 홍태영 / 곽재혁) publish their operational
engineering as Korean-language KIPS proceedings notes, and only occasionally promote a synthesis
to an international journal.

---

## 2. CHINESE FINDINGS

Author names below are given **as romanized on the publisher's own English metadata**; where I did
not see the Chinese characters on a reachable record I say so rather than guessing them.

| # | Native title (verbatim) | English title | Authors / affiliation | Venue | Yr | Record | Depth | What it does |
|---|---|---|---|---|---|---|---|---|
| C1 **★Sunway** | 神威太湖之光可靠性及可用性设计与分析 | Design and Analysis of Reliability and Availability on Sunway TaihuLight **[pub-EN]** | Gao Jiangang, Hu Jin, Gong Daoyong, Fang Yanfei, Liu Xiao, He Wangquan, Jin Lifeng, Zheng Fang, Li Hongliang (Chinese characters not verified on a reachable record; group = NRCPC / 国家并行计算机工程技术研究中心 lineage) | **计算机研究与发展** (J. Computer Research and Development) 58(12) | 2021 | pp. 2696–2707; DOI `10.7544/issn1000-1239.2021.20200967` | **FULL-TEXT (quantitative)** | **The single highest-value non-English item.** See §2.1 for the numbers. Multi-level fault tolerance (fault **prediction**, active migration, task degradation) plus a statistical failure-distribution study; **lognormal** fits the empirical failure data best; MTBF derived from it. |
| C2 **★Sunway** | 神威超级计算机运行时故障定位方法 | Runtime Fault Location Method for Sunway Supercomputer **[pub-EN]** | Gao Jiangang, Zheng Yan, Yu Kang, Peng Dajia, Li Hongliang, Liu Yong, He Wangquan, **Chen Dexun**, Wang Fei (characters not verified) | **计算机研究与发展** 61(1) | 2024 | pp. 86–97; DOI `10.7544/issn1000-1239.202220821` | ABSTRACT | **Root-cause analysis / fault localisation at runtime** on the **new-generation Sunway** exascale machine (SW26010-Pro many-core). Three components: fault-correlation analysis exploiting the message-passing structure, online diagnosis from globally aggregated information, and **anomalous-thread filtering** for the many-core processor. Explicitly targets the hard case: **failures with no log data and no obvious symptom.** No scale/overhead numbers in the accessible abstract. |
| C3 **★Beacon lineage** | Beacon+：面向E级超级计算机的轻量级端到端I/O性能监控与分析诊断系统 | Beacon+: a lightweight end-to-end I/O performance monitoring, analysis and diagnosis system for exascale supercomputers **[my-TR]** | 杨斌, 王敬宇, 刘世超, 邵明山, 肖伟, 陈起, **何晓斌**, 刘卫国, **薛巍** — affils: 山东大学软件学院; **国家超级计算无锡中心**; **国家并行计算机工程技术研究中心**; 清华大学计算机科学与技术系 | **计算机工程与科学** (Computer Engineering and Science) 44(9) | 2022 | issue 9; abstract paywalled | ABSTRACT (partial) / TITLE-ONLY for the numbers | **The Chinese-language successor of Beacon (NSDI'19).** Same senior authors (薛巍 Wei Xue, Tsinghua; 何晓斌 NRCPC) and the same NSCC-Wuxi setting. Motivation quoted verbatim: "多层级的存储架构、冗长的I/O路径和复杂的软件栈". One hard number reachable from the intro: the target Lustre deployment has "144个盘阵，能提供10 PB的存储容量，最大吞吐率达到200 GB/s以上". Full abstract, per-layer design, data volumes, sampling and overhead sit behind a login wall on the only reachable mirror. **This is the top re-chase target.** |
| C4 **★Tianhe/NUDT** | 监控分系统在E级高性能计算机系统中的挑战与设计 | Monitoring subsystem for exascale HPC systems: Challenges and design **[pub-EN]** | YUAN Yuan, LI Shi-jie, XING Jian-ying, JIANG Ju-ping — College of Computer Science and Technology, **国防科技大学 (NUDT)** | **计算机工程与科学** 43(8) | 2021 | pp. 1366–1375 | ABSTRACT | **A monitoring-subsystem architecture paper for an exascale machine**, from the Tianhe institution. Design treated along four dimensions — architecture, network, functionality, maintenance — against scalability / reliability / serviceability / maintainability requirements. A prototype validates parts of the design. **No machine name, node count, sampling rate or data volume** in the accessible abstract; the machine is presumably Tianhe-3 but the record does not say so. |
| C5 | 面向天河新一代超算系统通用处理器的性能分析工具集 | A Set of Performance Profiling Tools for the General Purpose Processors of TianHe New Generation Supercomputing System **[pub-EN]** | Feng Wen-Tao, Luan Zhong-Zhi (corresponding), Yang Hai-Long, Qian De-Pei — 北京航空航天大学 (Beihang) | **计算机学报** (Chinese J. Computers) 47(2) | 2024 | Feb 2024 | **FULL-TEXT** | **Recorded with a caveat: this is application performance debugging, not operational telemetry.** Instruction-granularity dynamic binary instrumentation (DrCCTProf) for cache-conflict, false-sharing and heap-memory-defect detection on Phytium S2500 ARMv8. Overhead is **40–100× time (avg 60–110×), 100–200× memory (avg 120×)** — far outside any always-on operational budget, which is itself a useful data point for the audit's overhead discussion. |

Chinese-language **background** work located but **not** HPC-operational (logged so the audit does
not over-claim the Chinese 智能运维 literature as HPC work):
`基于日志数据的分布式软件系统故障诊断综述` (软件学报, 2020, art. 6045) — log-based fault
diagnosis of *distributed software systems*;
`大规模软件系统日志研究综述` (软件学报, art. 4936);
`智能运维的实践: 现状与标准化` (软件学报, art. 6876 — abstract page returned **403**);
`互联网服务场景下基于机器学习的KPI异常检测综述` (计算机研究与发展) — explicitly
*互联网服务场景*, i.e. internet services;
`基于人工智能方法的数据库智能诊断` (软件学报, 2021);
`云计算系统可靠性研究综述` (计算机研究与发展, DOI `10.7544/issn1000-1239.2020.20180675`).

**Finding on 智能运维 (AIOps):** the Chinese-language AIOps literature is very active but is
overwhelmingly **cloud / internet-service** oriented (KPI anomaly detection, microservice root
cause, database diagnosis). I found **no** Chinese-language paper applying the 智能运维 framing to
an HPC/supercomputer estate. The Chinese HPC-operational work I did find (C1–C4) is framed instead
as 可靠性/可用性, 故障定位 and 监控分系统 — i.e. as systems engineering, not as AIOps. That
vocabulary gap is worth stating in the audit, because searching 智能运维 alone would have missed
C1–C4 entirely.

### 2.1 C1 in detail — the operational numbers

Quoted verbatim from the reachable PDF preview of `10.7544/issn1000-1239.2021.20200967`
(numerals appear in the source in full-width form; transcribed here):

- Abstract, opening: 「随着系统规模与集成度的快速增加，可靠性与可用性问题成为构建 E 级计算机系统所面临的重大挑战。」
- Keywords: 「E级计算机；可靠性；可用性；失效；故障容错；累积分布函数」
- Scale: 「神威太湖之光超级计算机共安装 40960 个国产众核处理器，全机运算核心达到 10649600 个」; 主存容量 **1.3 PB**; peak **125.43 PFLOPS**, Linpack **93.01 PFLOPS**.
- **Hardware-failure attribution:** compute nodes **58.92%**, power subsystems **18.60%**, maintenance/diagnostic subsystems **12.79%**.
- **MTBF: 「系统平均无故障时间 MTBF 为 11.84 h」**
- **Application-perceived MTBF improves to 24.2 h** with active migration.
- **Fault-prediction accuracy: 约 70%.**
- Job-degradation fault tolerance reduces losses by **90% 以上**.
- Distribution fitting: exponential, lognormal and Weibull compared; **lognormal** fits best.

The **observation period** over which the failure records were gathered is *not* stated in the
abstract or in the reachable preview text. That is a gap; the audit should not assert a period.

---

## 3. JAPANESE FINDINGS

| # | Native title (verbatim) | English title | Authors / affiliation | Venue | Yr | Depth | What it does |
|---|---|---|---|---|---|---|---|
| J1 **★R-CCS/Fugaku** | スーパーコンピュータ「富岳」における冷却設備保護のための電力変動監視システムの改修 | Modification of the power-fluctuation monitoring system for cooling-equipment protection on the supercomputer Fugaku **[my-TR]** | 寺井 優晃 (理研), 三浦 信一 (理研), 永田 英治 (富士通) | 情報処理学会 **第193回HPC研究発表会** (IPSJ SIGHPC) | — (mtg. 193) | TITLE-ONLY / RECORD-METADATA | **Facility telemetry on Fugaku.** A power-fluctuation monitoring system whose purpose is to *protect the cooling plant* — i.e. cross-layer facility/system coupling, exactly the audit's facility axis. |
| J2 **★R-CCS** | スーパーコンピュータ「京」におけるログデータに基づいたファイルステージングの分析と評価 | Analysis and evaluation of file staging based on log data on the K supercomputer **[my-TR]** | 伊藤 俊, 山本 啓二, 松田 元彦, 辻田 祐一, **庄司 文由** — all 理化学研究所 (RIKEN) | IPSJ **第168回HPC研究発表会**, 2019-03-05/07, 加賀市 | 2019 | TITLE-ONLY | **Operational log analytics on the K computer** — file-staging behaviour reconstructed from log data. 庄司文由 is R-CCS's operations lead and the author of the English K-computer failure-statistics line. |
| J3 | 計算ノードの使用効率向上を目指した「京」のファイルシステムの運用改善 | Operational improvement of the K computer's file system aimed at raising compute-node utilisation **[my-TR]** | 古谷 吉隆 (富士通); 辻田 祐一, 山本 啓二, 宇野 篤也 (理研); 末安 史親, 肥田 元, 岡本 光央 (富士通) | IPSJ 第168回HPC研究発表会 | 2019 | TITLE-ONLY | Operations change driven by utilisation data. |
| J4 **★R-CCS** | 消費電力を考慮した「京」の運用方法の検討 | *Operation of the K computer Focusing on System Power Consumption* **[pub-EN, from R-CCS's own list]** | Uno A., Hida H., Inoue F., Ikeda N., Tsukamoto T., Sueyasu F., Matsushita S., **Shoji F.** (romanized as recorded on researchmap; Japanese characters for the middle authors not verified) | **情報処理学会論文誌 コンピューティングシステム (IPSJ Trans. Computing Systems / ACS)** Vol. 8 No. 4 | 2015 | RECORD-METADATA | pp. 13–25. A **Japanese-language journal** paper on power-aware operation of the K computer. Distinct from the group's English output. |
| J5 | ノード保守タイミングのジョブスケジューリングへの影響評価 | *A Study of Job Scheduling Performance focusing on Compute Node Maintenance* **[pub-EN, from R-CCS's own list]** | 宇野 篤也 (Uno A.), Sekizawa R. | HPCと計算科学シンポジウム (HPCS) | 2016 | RECORD-METADATA | **Maintenance-scheduling interaction** — how node-maintenance timing perturbs job scheduling. |
| J6 | 消費電力の変動を考慮したジョブスケジューリングの検討 | Job scheduling accounting for power-consumption fluctuation **[my-TR]** | 宇野 篤也 (理研 AICS); 末安 史親 (富士通); et al. | IPSJ **第161回HPC研究発表会** | — | TITLE-ONLY | Power-aware scheduling. |
| J7 | 電力制約下における最適なアプリケーション実行パラメータの導出手法 | Deriving optimal application execution parameters under a power cap **[my-TR]** | 小野 美由紀?/ Ono Miyuki, 福本 尚人 (Fukumoto Naoto), 本多 巧 (Honda Takumi), 中島 耕太 (Nakajima Kota) — 富士通研究所 | IPSJ 第161回HPC研究発表会 | — | TITLE-ONLY (given-name kanji not verified) | Power-capped execution tuning. |
| J8 **★R-CCS facility** | 理研計算科学研究機構における設備最適運転条件の検討 | Study of optimal facility operating conditions at RIKEN AICS **[my-TR]** | 関口 芳弘, 瀧塚 博之 | 空気調和・衛生工学会大会 学術講演論文集 (SHASE) | 2013 | RECORD-METADATA | **Facility/cooling analytics for the K computer site**, published in the HVAC society — a venue no CS index covers. |
| J9 **★Fugaku facility** | スーパーコンピュータ「富岳」向け設備改修と運用検証（その1）設備増強改修の概要 | Facility renovation and operational verification for Fugaku (Part 1): outline of the capacity upgrade **[my-TR]** | 野々瀬 恵司, 長谷川 巌, 関 悠平, 塚本 俊之, 松下 聡, 苗村 元 | SHASE 大会学術講演論文集 | 2020 | RECORD-METADATA | Fugaku facility upgrade. |
| J10 **★Fugaku facility** | スーパーコンピュータ「富岳」向け設備改修と運用検証（その2）富岳実機負荷による機能試験 | …(Part 2): functional testing under real Fugaku machine load **[my-TR]** | 関 悠平, 野々瀬 恵司, 長谷川 巌, 塚本 俊之, 苗村 元 | SHASE 大会学術講演論文集 | 2020 | RECORD-METADATA | **Facility functional test driven by real machine load** — the facility-side counterpart to J1. |
| J11 | スーパーコンピュータ「不老」の湧水噴霧による節電効果の評価 / …の再評価 | Evaluation / re-evaluation of the power-saving effect of spring-water spray on the supercomputer "Flow" **[my-TR]** | 山田 一成, 田島 嘉則, 高橋 一郎, 林 秀和, 片桐 孝洋, 大島 聡史, (星野 哲也), 永井 亨 — 名古屋大学 | 大学ICT推進協議会年次大会論文集 (AXIES) | 2022 / 2023 | RECORD-METADATA | **Measured cooling-intervention effect** on a production supercomputer, with a follow-up re-evaluation. |
| J12 | 大阪大学スーパーコンピュータの電力コスト算定の仕組み | The mechanism for calculating power costs of Osaka University's supercomputers **[my-TR]** | 木越 信一郎, 勝浦 裕貴, 寺前 勇希, 上野 雅矢, 伊達 進 | AXIES | 2022 | RECORD-METADATA | Power-cost attribution from facility + system data. |
| J13 | スーパーコンピュータWisteria/BDEC-01における利用状況を考慮した運用の再検討 | Reconsidering the operation of Wisteria/BDEC-01 in light of usage data **[my-TR]** | 中張 遼太郎, 須貝 佳義, 昆野 長典, 前田 光教, 佐藤 孝明, 山崎 一哉, 三木 洋平, 胡 曜, 下川辺 隆史, 住元 真司, 塙 敏博, 中島 研吾 — 東京大学 | AXIES | 2024 | RECORD-METADATA | **Usage-data-driven operational-policy change** on Wisteria. |
| J14 | Miyabi スーパーコンピュータシステムの運用 | Operation of the Miyabi supercomputer system **[my-TR]** | 須貝 佳義, 山本 和男, 佐藤 孝明, 前田 光教, 昆野 長典, 中張 遼太郎, 中島 研吾, 塙 敏博, 住元 真司, 下川辺 隆史, 三木 洋平, 胡 曜, 山崎 一哉 | AXIES | 2025 | RECORD-METADATA | Operations report. |
| J15 | Ipomoea-01 大規模共通ストレージシステムの運用 | Operation of the Ipomoea-01 large-scale shared storage system **[my-TR]** | 前田 光教, 宮嵜 洋, 佐藤 孝明, 福沢 秋津, 中張 遼太郎, 山田 新, 山本 和男, 中島 研吾, 塙 敏博 | AXIES | 2022 | RECORD-METADATA | Storage operations. |
| J16 | スーパーコンピュータ「不老」の利用状況について / …の運用状況と次期システムへのファイル移行について | On the usage status of "Flow" / on its operational status and file migration to the next system **[my-TR]** | 山田 一成, 毛利 晃大, 林 秀和, 片桐 孝洋, 星野 哲也, 永井 亨 (2024); 岩瀬 雄祐, 宇田川 暢, 林 秀和, 山田 一成, 田島 嘉則, 毛利 晃大, 椋木 大地, 星野 哲也, 片桐 孝洋 (2025) | AXIES | 2024 / 2025 | RECORD-METADATA | Utilisation reporting. |
| J17 | スーパーコンピュータシステムの運用状況について | On the operational status of the supercomputer system **[my-TR]** | 更科 高広, 吉川 浩, 角鹿 千枝, 吉川 潤, 高口 智美, 折谷 智咲, 齋藤 珠紀, 村田 欽正, 深谷 猛, 岩下 武史 — 北海道大学 | AXIES | 2023 | RECORD-METADATA | Operations report. |
| J18 | スーパーコンピュータAOBAサブシステムAOBA-Sの運用状況と利用者支援について | On the operational status of the AOBA-S subsystem and user support **[my-TR]** | 木村 優太, 森谷 友映, 山下 毅, 小野 敏, 大泉 健治, 滝沢 寛之 — 東北大学 | AXIES | 2024 | RECORD-METADATA | Operations report. |
| J19 | FOCUSスパコンシステム運用の（10+4）年 / …の15年 | (10+4) years / 15 years of FOCUS supercomputer system operations **[my-TR]** | 西川 武志, 木下 朋子 (FOCUS / 計算科学振興財団) | IPSJ 第196回 / 第204回HPC研究発表会 | — | TITLE-ONLY | **Long-horizon operational retrospective** — 15 years of one centre's operations. Potentially valuable longitudinal material. |
| J20 | 次世代計算基盤の資源管理に関する調査研究の報告 | Report on investigative research into resource management for next-generation computing platforms **[my-TR]** | 佐賀 一繁, 竹房 あつ子, 田中 秀樹, 高倉 弘喜, 藤原 一毅, 坂根 栄作, 合田 憲人 (国立情報学研究所), 山本 啓二 (理研), 塙 敏博 (東京大学) | IPSJ 第201回HPC研究発表会 | — | TITLE-ONLY | National-scale resource-management study; includes R-CCS. |
| J21 | 業務時間を考慮したジョブスケジューリング手法に関する一考察 | A consideration of job-scheduling methods that take working hours into account **[my-TR]** | 粟飯原 俊介, フィネルティ パトリック, 朱 致儀, 太田 能 — 神戸大学システム情報学研究科 | IPSJ 第201回HPC研究発表会 | — | TITLE-ONLY | Scheduling policy. |
| J22 | LSTMによるジョブの実行時間予測および予測実行時間と要求実行時間を併用するジョブスケジューリング | Job runtime prediction with LSTM, and job scheduling that uses predicted and requested runtimes together **[my-TR]** | 久保 優也, 吉田 幸平, 三輪 忍, 八巻 隼人, 本多 弘樹 — 電気通信大学 | IPSJ 第193回HPC研究発表会 | — | TITLE-ONLY | **ML on job telemetry** — LSTM runtime prediction feeding the scheduler. The closest Japanese item to "ML on operational data". |

**Japanese negative results worth recording.** A J-STAGE search for
`スーパーコンピュータ 異常検知` returned 13 hits, **none** of which is HPC-operational (they are
meteorology, aerospace, nuclear, wind energy, medical informatics). `高性能計算 ログ 解析`
returned 226 hits dominated by earthquake/structural simulation — again **no** HPC operational log
analytics. `富岳 運用 障害` returned 27 hits with **no** Fugaku failure-analysis paper. So within
J-STAGE's coverage, Japanese-language HPC anomaly detection / failure prediction is essentially
absent. The caveat is important: **IPSJ SIGHPC technical reports are not on J-STAGE**, and the two
routes into them (IPSJ digital library, CiNii Research) were both robots-blocked, so this negative
does not extend to SIGHPC.

Also noted (Japanese, vendor gray literature, **NOT retrieved**):
`スーパーコンピュータ「富岳」の運用系ソフトウェア` — Fujitsu Technical Review 2020-03, article 10.
The URL 302-redirects to a generic Fujitsu landing page; content not obtained. Recorded as
**NOT FOUND (redirect)**; a likely home for Fugaku monitoring/job-management architecture detail.

RIKEN R-CCS **システム運転技術ユニット** (System Operation Technology Unit) publication list was
reached and confirms the unit's remit includes operations-data analysis and power management. Its
listed output is predominantly English-venue (ISC/ICCS/LNCS), with J4 and J5 the Japanese-language
exceptions. Notably it also lists *"Long term failure analysis of 10 Petascale supercomputer"*
(ISC 2015 HPC-in-Asia poster) — English, poster-only, and therefore easy for an index-based search
to miss.

---

## 4. ACCESS LOG PER PORTAL

Status is for **WebFetch** unless stated. "Search-usable" means a query URL returned real results.

### Korean
| Portal | Status | Detail |
|---|---|---|
| **KoreaScience** (koreascience.kr / .or.kr) | **REACHED — primary workhorse** | Journal/proceedings **TOC pages** (`/journal/JBCRA1/y<YYYY>m<MM>a.page?lang=ko`) and **article pages** (`/article/<ID>.page?lang=ko`) fetch reliably and carry authors, affiliations, pages, DOI and Korean abstracts. **`/article/*.pdf` paths are robots-blocked.** The site's own search endpoint (`/search.page?keywords=`) returns **HTTP 400** — unusable. Intermittent 5xx on individual pages (hit on 2021-spring TOC and on two article pages); retry sometimes works. |
| **ScienceON** (scienceon.kisti.re.kr) | **ROBOTS-BLOCKED** | Every `selectPORSrch*` record URL refused with `ROBOTS_DISALLOWED`. Records are still *discoverable* through WebSearch result titles/snippets, but not fetchable, so nothing was verified from ScienceON. Its KISTI technical-report holdings (TRKO*) are therefore unexamined. |
| **KCI** (kci.go.kr) | **ROBOTS-BLOCKED** | Both `ciSereArtiView.kci` article pages and `poCitaView.kci` journal pages refused. Contrary to the task's expectation that KCI would be among the most accessible, it was among the least. Titles were recoverable only via WebSearch. |
| **DBpia** (dbpia.co.kr) | **PARTIAL — article pages reached, search unusable** | `/journal/articleDetail?nodeId=…` pages fetch fine and gave full metadata + abstracts (used for K22). **The search endpoint returns a JavaScript shell**: `topSearch?query=누리온` reported "총 0건" even though a 누리온 article demonstrably exists in DBpia. **All DBpia search zeros are artefacts and were discarded — none is used as negative evidence here.** |
| **RISS** (riss.kr) | **NOT FETCHED** | Only appeared in WebSearch results; no direct fetch attempted after KCI/ScienceON both refused. |
| **KISS** (kiss.kstudy.com) | **NOT REACHED** | Login-gated commercial portal; not attempted. |
| **KIISE** (kiise.or.kr) | **NOT SEARCHED DIRECTLY** | KIISE 정보과학회논문지 / KSC / KCC proceedings are distributed via DBpia, whose search is unusable (above). **This is the largest remaining Korean gap.** |
| **KIPS** society site | **NOT NEEDED** | KoreaScience carries the full KIPS proceedings run; used instead. |
| **KISTI repository** (repository.kisti.re.kr) | **NOT FETCHED** | Surfaced PDF links in WebSearch (older 2005 technical notes); not pursued. |

### Chinese
| Portal | Status | Detail |
|---|---|---|
| **CNKI** (jsjk.cbpt.cnki.net, cnki.net) | **CAPTCHA-BLOCKED** | The journal-hosting page rendered only a 请填写验证码 image CAPTCHA. No content obtainable. |
| **Wanfang** (wanfangdata.com.cn) | **NOT REACHED** | Not attempted after CNKI's CAPTCHA made the commercial-aggregator route look unproductive; no evidence it would differ. |
| **CQVIP** (cqvip.com / qikan.cqvip.com) | **NOT REACHED** | Only marketing/landing pages surfaced in search; one article-detail URL (`dianda.cqvip.com/Qikan/Article/Detail?id=…`) appeared but was not fetched. |
| **计算机研究与发展** (crad.ict.ac.cn) | **REACHED — best Chinese source** | `/article/doi/<DOI>`, `/cn/article/id/<n>` and **`/cn/article/pdf/preview/<DOI>.pdf`** all fetch. The PDF-preview path is what yielded C1's hard numbers. |
| **计算机工程与科学** (joces.nudt.edu.cn) | **PARTIAL** | Article pages of the form `/CN/Y<YYYY>/V<vol>/I<iss>/<startpage>` fetch (used for C4). Issue-TOC paths (`/CN/Y2022/V44/I9/0`) failed with a **robots.txt fetch ConnectTimeout**, which is why C3 (Beacon+) could not be pinned to a page range from the publisher. |
| **计算机学报** (cjc.ict.ac.cn) | **REACHED** | `/online/onlinepaper/*.pdf` and `/online/bfpub/*.pdf` fetch as full text (used for C5). |
| **软件学报** (jos.org.cn) | **PARTIAL** | Legacy `/html/<year>/<issue>/<id>.htm` pages fetch. Newer `/jos/article/abstract/<id>` returned **HTTP 403**. |
| **参考网 mirror** (m.fx361.com) | **REACHED but paywalled** | Carried C3's identity, full author/affiliation list, journal and issue, plus the introduction — then "登录APP查看全文". Abstract, keywords beyond one, and all architecture/overhead numbers withheld. |
| **api.crossref.org** | **NOT USED** | Chinese, Korean and Japanese domestic items here largely lack DOIs, or carry publisher-local DOIs (`10.3745/PKIPS.*`) already captured directly; the 65 s rate limit made it poor value. |

### Japanese
| Portal | Status | Detail |
|---|---|---|
| **J-STAGE** (jstage.jst.go.jp) | **REACHED — search-usable** | `/result/global/-char/ja?globalSearchKey=<encoded>` returns real, paginated, counted results. Four queries run (運用 / 監視 / 異常検知 / ログ解析, plus 富岳 運用 障害). This is what established the Japanese negatives and surfaced the AXIES and SHASE venues. |
| **IPSJ event program pages** (ipsj.or.jp/kenkyukai/event/hpc<N>.html) | **REACHED — enumerable** | Full programmes with titles and affiliations. **Six meetings sampled: 161, 168, 173, 193, 196, 201, 204.** These pages do **not** carry 研究報告 volume/number citations, so J1/J2/J3/J6/J7/J19/J20/J21/J22 lack a formal volume reference. |
| **IPSJ digital library** (ipsj.ixsq.nii.ac.jp) | **ROBOTS-BLOCKED** | Both a `/records?…` form (404) and a `/search?…q=` form (`ROBOTS_DISALLOWED`) failed. **This is the single most damaging Japanese access failure** — it is the authoritative home of SIGHPC 研究報告 and of IPSJ Trans. ACS. |
| **CiNii Research** (cir.nii.ac.jp) | **ROBOTS-BLOCKED** | `/all?q=` refused. No CiNii record was verified. |
| **researchmap.jp** | **REACHED** | `/<handle>/published_papers` returns full publication lists. Used for J4/J5 (via 宇野篤也's list). Note: researchmap lists are self-maintained, so author lists there are RECORD-METADATA, not publisher-verified. |
| **riken.jp lab pages** | **REACHED** | R-CCS System Operation Technology Unit page fetched; gave the unit's remit and its own publication list. |
| **Fujitsu Technical Review** | **REDIRECTED / NOT FOUND** | The 2020-03 Fugaku operations-software article 302s to a generic landing page. |

---

## 5. COVERAGE VERDICT — what the audit may now defensibly say

### Korean — **moderate-to-strong**, and the negative claim must now be *retracted or narrowed*
The audit can no longer say anything resembling "we found no Korean work on HPC operational
analytics." Twenty-one KIPS proceedings items plus two journal papers were found, most of them
KISTI-authored and directly on target.

What is genuinely well covered: the **KIPS Annual Conference proceedings**, swept year by year via
KoreaScience TOCs for **2019 fall, 2020 fall, 2021 fall, 2022 spring, 2022 fall, 2023 spring,
2023 fall, 2024 spring, 2024 fall, 2025 spring, 2025 fall, 2026 spring** — twelve issues.
(2021 spring failed with a 5xx and was **not** re-attempted; 2018 and earlier were **not** swept.)

What is **not** covered: KIISE venues (정보과학회논문지, KSC, KCC) — reachable only through DBpia,
whose search is unusable; KISS-only journals; ScienceON's KISTI technical-report holdings (TRKO),
robots-blocked; and KIPS *Transactions* (정보처리학회논문지) as distinct from its proceedings.

**Defensible wording:** *"A year-by-year sweep of twelve issues of the KIPS Annual Conference
proceedings (2019–2026) via KoreaScience, together with targeted searching of ScienceON, KCI and
DBpia records, identified 23 Korean-language items on HPC operational analytics, 20 of them
KISTI-authored. KIISE proceedings, KISS-only journals, KIPS Transactions and KISTI's TRKO technical
reports could not be searched, because DBpia's search endpoint, ScienceON and KCI were respectively
non-functional or robots-blocked; Korean-language coverage before 2019 was not attempted."*
Do **not** write "no Korean work exists on X" for any X — write "not found in the KIPS proceedings
2019–2026 or in KoreaScience-indexed journals."

### Chinese — **weak-to-moderate**; absence is *not* established
Every general-purpose Chinese aggregator failed: **CNKI CAPTCHA-blocked, Wanfang not reached,
CQVIP not reached.** All five Chinese findings came from **publisher-side journal websites**
(crad.ict.ac.cn, joces.nudt.edu.cn, cjc.ict.ac.cn) reached through WebSearch, i.e. by luck of
search-engine indexing rather than by systematic enumeration. No Chinese journal was swept
issue-by-issue.

**Defensible wording:** *"Targeted searching of four publisher-hosted Chinese journal sites
(计算机研究与发展, 计算机工程与科学, 计算机学报, 软件学报) located five Chinese-language items on
HPC operational analytics, including quantitative reliability data for Sunway TaihuLight and the
Chinese-language successor of Beacon. CNKI, Wanfang and CQVIP could not be searched (CAPTCHA and
access barriers), and no Chinese journal was enumerated issue-by-issue, so the Chinese-language
literature is sampled, not surveyed. No absence claim about Chinese-language work is supportable."*

One Chinese claim **is** safe to make positively, because it is a vocabulary observation rather
than an exhaustiveness claim: *"the very active Chinese-language 智能运维 (AIOps) literature is
oriented to cloud and internet services; the Chinese HPC-operational work located instead uses the
vocabulary of 可靠性/可用性, 故障定位 and 监控分系统."*

### Japanese — **moderate for facility and operations reporting; weak for SIGHPC**
J-STAGE was searched properly and is a genuine negative for HPC anomaly detection and failure
prediction. But J-STAGE does not carry IPSJ SIGHPC 研究報告 or IPSJ Trans. ACS, and **both routes
into those (IPSJ digital library and CiNii Research) were robots-blocked**. IPSJ coverage is
therefore a **sample of six meetings out of roughly forty-five** in the 2016–2026 window.

**Defensible wording:** *"J-STAGE was searched with five Japanese-language queries and contains
essentially no HPC operational anomaly-detection or failure-prediction research; the Japanese
operational literature it does contain is facility- and utilisation-reporting work, concentrated in
大学ICT推進協議会年次大会論文集 and 空気調和・衛生工学会大会論文集. Because the IPSJ digital
library and CiNii Research were robots-blocked, IPSJ SIGHPC technical reports were sampled only
through six meeting programmes (161, 168, 173, 193, 196, 201, 204); Japanese-language work in
SIGHPC therefore cannot be claimed absent."*

### Ranking of confidence
**Korean > Japanese > Chinese.** Korean because a real venue was enumerated end-to-end; Japanese
because one major index was searched properly but the most likely venue was not; Chinese because
no index was searchable at all and every find was opportunistic.

---

## 6. THE SINGLE MOST IMPORTANT ITEM

**C1 — 神威太湖之光可靠性及可用性设计与分析, 计算机研究与发展 58(12):2696–2707, 2021,
DOI `10.7544/issn1000-1239.2021.20200967`.**

Why it matters more than anything else found:

1. **It supplies hard operational ground truth that the English literature does not have for this
   machine.** MTBF **11.84 h** at 40,960 processors / 10,649,600 cores, with a **failure attribution
   breakdown** (compute nodes 58.92%, power 18.60%, maintenance/diagnostic 12.79%). Numbers of this
   kind, for a machine of this class, are exactly what an operational-analytics audit needs and
   almost never gets.
2. **It reports a fault-prediction accuracy figure — ~70% — and a measured operational payoff:**
   application-perceived MTBF rising from 11.84 h to **24.2 h** through active migration. That is a
   *deployed* prediction-plus-remediation loop with a before/after number, in production, at
   exascale-adjacent scale. Any audit claim that HPC failure prediction has not been shown to pay
   off operationally has to engage with this.
3. **It is Chinese-language only**, in a journal not covered by the audit's English indices, from
   the NRCPC group that actually built the machine. It is the clearest single demonstration that the
   English-only search was not merely incomplete but was missing *quantitative operational
   evidence*, not just additional citations.
4. It also fixes a methodological point: the failure-time distribution is **lognormal**, not
   exponential — which bears directly on how the audit should treat MTBF-based reasoning.

**Runner-up, and the more important finding as a *body* rather than an item:** the **KISTI KIPS
series K1–K21**. No single one of those papers is individually weighty — they are two-to-four-page
operational engineering notes. But taken together they document a **continuous eight-year
in-house operational-analytics program at the very institution the audit concerns**: health-checking
(K1), monitoring-load-aware design (K3), per-job power (K4), per-job I/O joined across scheduler and
DDN/InfluxDB storage telemetry (K6), a PCP/bpftrace/Grafana monitoring stack (K7), per-job GPU stats
(K10), scheduler-driven profiling collection (K12), automated node recovery (K14), thermal
fail-slow remediation (K17), and automated GPU-failure notification explicitly scoped to KISTI-6
(K19). Because most of these have **no English counterpart**, the audit's count of KISTI work was
low by roughly an order of magnitude, and any claim of the form "KISTI has not previously worked on
X" needs re-checking against this list before it is written.

**Top three re-chase targets, in order:**
1. **C3 Beacon+** full text — the only reachable copy is paywalled; the per-layer design, data
   volumes, sampling strategy and overhead are the numbers the audit most wants. Try the
   publisher issue TOC at `joces.nudt.edu.cn` (robots timeout may be transient) or a library copy.
2. **K5** (hardware performance counter collection *and overhead*, KIPS 2020) — article page
   returned 5xx twice; affiliation unverified; topic is squarely on the audit's overhead axis.
3. **K23** (HPC user-log job-success-rate paper) — authors, year and pages unverified because KCI is
   robots-blocked and the KoreaScience page 5xx'd.

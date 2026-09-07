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

# 05. RESEARCH–PRACTICE GAPS
## 운영 현장이 하는 것 vs 문헌이 한 것, 그리고 그 사이에 실제로 남은 것

**작성일:** 2026-09-06
**판정값:** `CLOSED` / `PARTIALLY_ADDRESSED` / `STILL_OPEN` / `TOO_SITE_SPECIFIC` / `ENGINEERING_ONLY` / `INSUFFICIENT_EVIDENCE`
**원칙:** 확실하지 않으면 `INSUFFICIENT_EVIDENCE`. gap 선언 전에 반드시 closest work를 먼저 찾았다.

---

# PART I — 마스터 gap 표

**Research maturity** = 아카이벌 문헌이 도달한 최고 L레벨 · **Production maturity** = 실제 센터가 운영 중인 최고 L/D 레벨

| # | Problem | Production practice (실제로 돌아가는 것) | Closest research (검증된 최강 선행) | Research maturity | Production maturity | Remaining gap | Evidence | 판정 |
|---|---|---|---|---|---|---|---|---|
| **G1** | 조용히 성능이 저하된 하드웨어(silent defect) 색출 | ORNL Frontier: Slurm **backfill**로 단일 노드 벤치마크 상시 실행. 6개월 **190만 테스트 → 고유 실패 노드 99개**. LAMMPS **14,618 테스트당 1건**. 주간 `checknode` 스크린은 **39,437회 무수확 후 2023-12 폐기**, epilog 변형은 "too disruptive" | 신뢰성 *특성화*만 존재: Ostrouchov SC20(Titan GPU survival), Nie DSN'18(GPU error prediction). **screening-policy 최적화 논문 없음** | L3 | **L3 / D5** (실제 운영) | **어떤 테스트를, 얼마나, 어느 cadence로, 남는 backfill 용량에 태울 것인가**를 순차 실험 설계로 정식화한 연구가 없다. 목적함수: node-hour당 발견 결함 수 | CUG2024 pap123 (ORNL Hagerty/Warner/Webb) — 숫자 전부 원문 | **STILL_OPEN** |
| **G2** | 사용자에게 job 비효율을 알려주기 | TU Dresden **PIKA 5년 이상 production**, JSC **LLview** JUWELS Cluster+Booster production, SUNY Buffalo XDMoD Application Kernels. 전부 **운영 경험으로 손튜닝한 임계값** | **NOT FOUND.** archival 논문 없음 | — | **L2–L3 / D4** | "비효율"의 합의된 정의도, cross-site 검증도, **알려주면 사용자 행동이 바뀌는가에 대한 측정도 없다** | MODA23 PIKA(`10.1007/978-3-031-40843-4_22`), MODA25 LLview(`10.1007/978-3-032-07612-0_4`); SC25 ODA BoF 설문(29명): 운영데이터 가치 **4.3/5** vs 사용자 활용역량 **2.9/5** | **STILL_OPEN** |
| **G3** | cross-site telemetry schema / 의미론 표준 | 사이트마다 자체 스택. LDMS(Sandia), DCDB(LRZ), ExaMon(CINECA), LLview(JSC), PIKA(TUD), XDMoD(Buffalo), EMOI(CSCS), CEEMS(CNRS), OMNI(NERSC), STREAM(ORNL). **상호운용성 0** | Netti et al. *A Conceptual Framework for HPC ODA*, **IEEE Cluster 2021**(HPCMASPA) + *ODA in practice*, Parallel Computing 113(2022) — **개념적이며 cross-site 검증 없음**. HPC ODA Commons(PEARC'26, `10.1145/3785462.3815891`) = data contract, **모델 이전은 다루지 않음**(내용 `INSUFFICIENT_EVIDENCE`, 403) | L0/L1 | **L0–L1** | **metric ontology를 정의하고, ≥3개 센터(LDMS/DCDB/Prometheus)에 인스턴스화하고, portable analytic이 정해진 정확도 손실 안에서 이전됨을 보인 연구가 없다** | ODA BoF 2019–2025 9회 · MODA 7회 · SC24 BoF "HPC sites are duplicating efforts" · ORNL "Sensors, metrics, and telemetry data has not been standardized into a universal format" | **STILL_OPEN** |
| **G4** | configuration drift가 job 실패의 원인인가 | HPCSYSPROS **2020–2025 매년** 등장(Ansible, xCAT+Git, SStack, bootc, Warewulf v4). 전부 sysadmin 공예 | **어디에도 없음. 0편** | — | L0–L1 | **노드 이미지/설정 divergence를 계측하고 job 실패·성능분산·티켓량과 상관시킨 연구가 존재하지 않는다.** 아무도 정량화한 적이 없다 | HPCSYSPROS 2020–2025 전 연도 | **STILL_OPEN** (단, 연구 프레이밍 없이는 `ENGINEERING_ONLY`로 읽힐 위험) |
| **G5** | 공유자원 저하의 실시간 원인 job 귀속 | 사후·수동. 스토리지 관리자가 grep. NERSC는 **매일 off-hours obdfilter-survey 능동 probing**으로만 발견 | 특성화는 archival(PDSW→SC 파이프라인 확립): Lockwood *A Year in the Life of a Parallel File System* SC18; Kaleidoscope SC20(스토리지 스택 한정) | L5 (스토리지 한정) | L1–L2 + 능동 probing | **온라인 원인 귀속**(지금 파일시스템/인터커넥트를 누가 느리게 하는가)을 운영자 확인 인시던트 대비 precision/recall로 평가한 연구 없음 | MODA20 LASSi · MODA25 eBPF I/O · CUG2024 NERSC all-flash(느린 OST 25–50%↓, 15.1→19.9 GB/s) | **PARTIALLY_ADDRESSED** |
| **G6** | HPC 운영 log triage / RCA에 LLM | 사실상 없음. **2026년 독립 서베이 2편이 HPC 운영에 LLM production 배포 사례 0건이라고 명시** | 클라우드는 포화: RCACopilot EuroSys'24(653 인시던트, Micro-F1 0.766, 수집부 30팀 4년+), Ahmed ICSE'23, L4 FSE'25(**LLM 미사용으로 LLM baseline 압도**), AIOpsLab/ITBench(SRE **13.8%**) | L5/L6 (클라우드) | **L0** (HPC) | **HPC용 운영 agent 벤치마크가 존재하지 않는다** — Slurm/MPI·NCCL collective/fabric counter/PFS/배치 큐 의미론을 다루는 것이 없음 | Pochelu et al. arXiv 2602.00014: *"no documented evidence of production-level deployment to date"*; Suman/Chu/Iosup arXiv 2603.19016: 10개 production ODA 프레임워크 중 **LLM 통합 0** | **STILL_OPEN (HPC)** / **CLOSED (클라우드)** |
| **G7** | HPC 운영 데이터의 안전한 공개 | 대부분 공개 불가(보안·사용자 프라이버시·벤더 NDA). 예외적으로 M100 ExaData, F-DATA, HPC-ODA, OLCF Constellation, NREL Eagle | 익명화/거버넌스 **방법론 논문 NOT FOUND.** 인접: HPDC'25 *Bringing Differential Privacy to HPC: Privacy-Preserving Transformations of HPC Traces*(`10.1145/3731545.3731573`) | L0 | L0 | **job 수준 telemetry를 어디까지 익명화해도 ODA 분석(이상탐지·런타임예측)이 견디는가**에 대한 privacy/utility trade-off 연구 0편 | SC25 BoF 설문: 공개 ODA 데이터셋 가용성 **1.6/5 — 설문 최저점** | **STILL_OPEN** |
| **G8** | 고정 용량 하의 carbon-aware 운영 | JSSPP/EESP/Sustainable Supercomputing에 정책 제안 다수. SC24 Fugaku 인센티브(production 배포), SC25 Core Hours and Carbon Credits | 클라우드용은 HotCarbon/ASPLOS/SOSP에 archival. **HPC 변종(워크로드 이주 불가, 탄력 용량 없음, 국가 전력망·지역난방 결합, 가격이 아닌 fair-share)은 workshop-only** | L6 | L6–L7 (정책 개입) | **fair-share 제약 하 carbon-aware 지연을 production 규모에서 *측정된*(모델링 아닌) 탄소로 평가한 연구 없음** | JSSPP25, EESP25/26, SC24/25/26 Sustainable Supercomputing | **PARTIALLY_ADDRESSED** |
| **G9** | login node / 공유 서비스 남용의 closed-loop 통제 | Utah CHPC **Arbiter 3 — L7/D5, 실제 자동 강제 시행 중** | archival **NOT FOUND**. Arbiter의 유일한 비-workshop 발표는 **PEARC**(practice conference) | — | **L7 / D5** | **production에서 돌아가는 closed-loop controller가 peer-review로 평가된 적이 한 번도 없다** — 오탐률, 사용자 행동 효과, 안정성/진동 | HPCSYSPROS24 Arbiter 3(`10.5281/zenodo.16541343`) | **STILL_OPEN** |
| **G10** | 운영 정책 변경의 counterfactual 평가 | 불가능. production 슈퍼컴퓨터에서 A/B 테스트를 못 한다 | **ExaDigiT SC24**가 물리를 풀었다(Frontier 6개월 replay로 V&V). MODA23 HPE 고속 스케줄링 시뮬레이터. MODA25 duration-informed scheduler는 **시뮬레이션만** | L4/L6 | D3–D4 (twin) | **정책 평가 방법론이 없다** — digital twin에 대한 스케줄링/전력/냉각 정책 변경 평가를 실제 시스템 대비 오차 막대와 함께 제시한 연구 없음. **이것이 모든 L6/L7 연구를 시뮬레이션에서 멈추게 하는 메타 문제** | ExaDigiT SC24(`10.1109/SC41406.2024.00029`); MODA23/25 | **STILL_OPEN** |
| **G11** | telemetry 비용 대 하류 지능 품질 | 3가지 무딘 레버로만 통제: 고정 샘플링 간격(5–10초, 가끔 1초), 저장 전 in-memory 사전집계(SuperMUC-NG **70만→6만 insert/s, ~11.7배**), 보존 thinning(HPCM 기본 Kafka 1일/OpenSearch 7일/VictoriaMetrics 7일). **셋 다 엔지니어 판단으로 설정되며 어떤 것도 측정된 하류 품질 제약에 묶여 있지 않다** | 네트워킹은 정식화 완료: Sonata SIGCOMM'18(ILP query partition, 3–7 자릿수 감소), PINT SIGCOMM'20(패킷당 비트 예산 + 증명된 bound), AutoSketch NSDI'24. 클라우드: **SuperBench ATC'24 Best Paper의 Selector**가 검증 비용 대 탐지 이득을 명시적으로 최적화. HPC 측 감소는 전부 *모델링용* 차원 축소: NodeSentry **3,014→82**, Prodigy **806→156**, Tuncer **−57%** | L0/L1 | **L0** | **어떤 HPC 시스템에 대해서도 telemetry 비용 대 하류 운영 품질의 Pareto frontier가 발표된 적이 없다.** 샘플링 간격을 변화시킨 논문 0편, 보존 해상도를 변화시킨 논문 0편, telemetry rate의 함수로 **탐지 지연**을 보고한 논문 0편, 축소가 **RCA**(탐지가 아니라)에 미치는 품질 비용을 측정한 논문 0편 | CUG2023 pap149; CUG2023 STREAM(1.3 TB/day, 20 PB/5년); ORNL SC-W'24(4.2–4.5 TB/day, 스트림 간 **30만 배** 동적 범위); CADDY CUG2024(1200배 압축, ingest +32.5%); ARCHER2 Graphite downsampling 후회 | **STILL_OPEN (HPC)** / **CLOSED (네트워크 flow telemetry)** |
| **G12** | 운영 모델의 cross-system / cross-generation 일반화 | **없다.** Netti et al.: 센터들이 *"insular ODA solutions"*를 돌린다. Bartolini 그룹은 **per-node** 모델(RUAD)과 노드 간 federated learning을 쓴다 — 한 시스템 *안에서도* 단일 모델이 안 맞는다는 최강 증거 | 텍스트 로그는 **닫혔다**: MetaLog ICSE'24, CroSysLog(F1 97.6–99.2%, support 2,000 이벤트), ZeroLog ISSRE'25, LogTAD. 방법론은 SE venue가 소유: TOSEM data-splitting/model-update, EMSE model-reuse. 하드웨어는 DSN'24(Huawei) *Investigating Memory Failure Prediction Across CPU Architectures* | L3/L4 (로그) | L0 | **수치 HPC telemetry의 이전 손실을 (a) 두 사이트, (b) 두 GPU 세대, (c) 두 fabric 세대, (d) schema 변경에 대해 측정한 연구가 없다.** 유일한 측정치는 **한 시스템의 노드 간 F1 0.898 → 0.726**(AI4Sys'23 워크숍 3쪽) | SeT-Diff(CF'26, arXiv 2607.22548)는 **이 문제를 동기로 명시하고 cross-system 평가를 하지 않는다**; 서베이 THPC 8(3)이 cross-system generalization을 최상위 open challenge로 지목 | **STILL_OPEN (수치 telemetry)** / **CLOSED (텍스트 로그)** |
| **G13** | slow-node 진단의 원인 판별 | ORNL Frontier `checknode` — 결정적 임계값 검사, drain, **ML 0, "어느 검사가 실패했나" 이상의 원인 판별 0.** LBNL NHC가 커뮤니티 표준, 동일 성격 | **HPC:** Tuncer TPDS 2019가 anomaly *type*(network contention/CPU contention/memory bw/orphan process)을 분류 — **7년 전에 이미 이 축을 했다**. **GPU 클러스터:** ARGUS(>1만 GPU, 6개월, <2% overhead, compute straggler·link degradation·pipeline bubble·JIT stall 판별), FALCON(L7/D5, 60.1% 저하 감소), LLMPrism. **장치:** Perseus FAST'23, IASO ATC'19 | L5 | **L2 / D5** (규칙) | **다중 테넌트 배치 워크로드에서 *내재적* fail-slow와 *유발된* 간섭을 구분하는 것**만 남았다. ARGUS는 동기·반복·동질 학습 job을 전제하므로 이 전제가 HPC 배치에서 깨진다. Perseus/IASO의 peer 비교는 peer가 동일 워크로드일 때만 유효 | Frontier checknode CUG'23; IPDPS'26이 Perlmutter+Frontier에서 **네트워크 혼잡이 지배하고 개별 GPU 성능은 안정적**이라고 이미 측정 | **PARTIALLY_ADDRESSED** (탐지는 near-CLOSED) |
| **G14** | label 부족 하의 운영 학습 | Nagios/Zabbix/Prometheus 알림 + Slurm drain reason + 티켓 시스템(RT/ServiceNow)이 **서로 연결되지 않은 4개 소스**로 돌아간다. Frontier `checknode`가 실패한 검사 이름을 drain reason에 쓰는 것이 사실상 가장 가까운 production label 파이프라인이며 **아무도 이를 labeling method로 발표한 적이 없다** | 방법은 **닫혔다**: partial label(ISSRE'21), PU learning(ISSRE'22), label-free 배포 AutoKAD(ISSRE'23), active learning(AFALog/LogCAE), LabelEase, ZeroLog, ALBADross(28배 절감). 평가 비판: **Kim et al. AAAI'22 — point-adjustment 프로토콜이 F1을 부풀려 랜덤 점수가 SOTA를 이긴다** | L3 | L2 | **label semantics.** HPC 약한 label 소스(RAS severity, Slurm exit code, drain reason 문자열, 유지보수 티켓, RMA 기록, 사용자 "느려요" 민원)는 **서로 불일치하며 어느 것도 ground truth가 아니다.** 실제 슈퍼컴퓨터에서 이 소스들의 일치도를 정량화하거나, 불일치가 하류 모델 품질을 얼마나 파괴하는지 측정한 연구가 없다 | M100 ExaData 자체 논문이 Nagios 약한 label로 **AUC 0.57** 보고 — 이 축이 실재함을 보여주는 최고 인용 | **PARTIALLY_ADDRESSED** (방법 CLOSED, label semantics STILL_OPEN) |
| **G15** | 안전한 자동 조치 | Frontier `checknode`(자동 drain, **자기가 설정한 drain reason일 때만 자동 resume** — 사실상의 안전장치), LBNL NHC. **confidence 없음, 비용 모델 없음, rollback 없음, 수리 검증 자동화 없음** | **Narya OSDI'20이 개념을 닫았다** — 예측 + bandit/RL 조치 선택 + 온라인 실험, Azure **15개월, VM 중단 26% 감소**. FALCON(GPU 학습, L7/D5), SuperBench(검증→격리→수리), Perseus. HPC 계보(SC'08 → JPDC'12 → **HPDC'20 Behera et al.**)는 **production에 도달한 적이 없고 HPDC'20은 순수 SimPy 시뮬레이션이며 예측 정확도를 *가정*한다** | L7 (클라우드) | **L7 / D5** (규칙 기반) | **배치 스케줄·할당 회계·체크포인트 의존 환경에서의 조치 비용 모델이 없다.** 노드 drain 비용은 상수가 아니다 — 어떤 job이 올라가 있는지, 경과 시간, 체크포인트 신선도, 큐 압력에 의존한다. 그리고 **production Tier-0에서 drain을 A/B 테스트할 수 없으므로 off-policy 평가 방법론 자체가 미해결** | HPDC'20 `10.1145/3369583.3392672`(시뮬레이션); Iosup 서베이: 10개 production ODA 프레임워크에서 closed-loop이 *"partially manual"* | **STILL_OPEN (HPC)** / **CLOSED (클라우드·LLM 학습)** |
| **G16** | cross-layer 성능저하 RCA | 없음. **어떤 HPC 센터도 cross-layer causal RCA 시스템을 운영하지 않는다.** LDMS/DCDB + Kafka/Prometheus → Grafana + 임계값 알림 + 사람이 티켓 분류. ORNL EPIC이 유일한 LLM 보조 운영자 인터페이스이며 **RCA가 아니라 descriptive/predictive analytics** | **Kaleidoscope SC20이 가장 가깝고, 한 서브시스템만 닫는다**(스토리지). PACE(SC'25 Workshops, HPE/ORNL)가 유일한 명시적 causal discovery이나 **workshop, Granger, job 성능 미접촉**. 클라우드: FIRM OSDI'20, Eadro ICSE'23, ClearCausal ACSOS'24 | L5 (서브시스템 한정) | L1–L2 | **{CPU/메모리, GPU, fabric(어느 링크·스위치그룹), Lustre(어느 OST/MDT), 스케줄러 배치 결정, CDU/전력}에 대한 순위 귀속을, (a) 운영자 확인 인시던트 티켓으로 검증하고, (b) 고전 causal discovery가 0%를 기록하는 소표본 영역에서 견디며, (c) 운영자가 실제 취할 수 있는 닫힌 조치 집합으로 종결하는 시스템이 없다** | Kaleidoscope 843건이 SC의 기준선. *How Far Can RCA Go*: 실제 telemetry에서 **Granger/PC/FCI/LiNGAM/NTLR 전부 Acc@1 0%**, 실패의 **65.7%가 reasoning gap이지 데이터 부족이 아님** | **PARTIALLY_ADDRESSED** (탐지 CLOSED, localization PARTIAL, causal attribution STILL_OPEN, operator action STILL_OPEN) |
| **G17** | 벤더 telemetry 품질 자체 | 사이트가 벤더 경로를 우회한다. CSM `telemetry-api`는 Perlmutter 전규모에서 *"could not handle the data rate (100K to 1M messages per second)"*, *"stopped feeding data at random times"*, Kafka rebalancing 유발. CSM 내장 LDMS는 *"significantly behind the latest LDMS release"* | **NOT FOUND.** telemetry 품질 벤치마크 논문이 존재하지 않음 | — | D5 (우회로) | **동일 노드에서 벤더 제공 telemetry와 독립 수집기의 완전성·충실도 손실을 *측정*하고, 그 손실이 하류 모델 정확도에 무엇을 하는지 보인 연구가 없다.** "telemetry integrity / observability debt" 지표 자체가 없다 | CUG2023 pap149 (LLNL-CONF-847852, Sandia/LLNL/LBNL + HPE 공저) | **STILL_OPEN** |
| **G18** | 모니터링 control plane의 backpressure·우아한 저하 | 실패가 문서화되어 있다: telemetry-api → Kafka rebalancing → **boot 실패**; LDMS credential 배포가 *"not only slow but unreliable"*; 단일 고정 worker `ncn-w001` 병목 | LDMS SC14(전송 확장), Wintermute HPDC20(in-band analytics) — 둘 다 **backpressure를 다루지 않음** | L0 | D5 | 10^5–10^6 msg/s 모니터링 plane의 end-to-end 흐름 제어·admission·저하 모드 설계 원칙이 없다 | CUG2023 pap149 | **STILL_OPEN** |
| **G19** | telemetry schema 진화와 다년 아카이브 | STREAM이 고통을 문서화: 필드가 *"change throughout the lifetime of the data"*, topic 개명 후 재색인(*"slow process"*), federated schema registry 충돌 | **NOT FOUND** | — | D5 | 버전화된 metric semantics, schema registry federation, 다년 아카이브 재처리 비용 | CUG2023 STREAM (OSTI 1995656) | **STILL_OPEN** |
| **G20** | 지속적 acceptance testing / silent regression 탐지 | buildtest(NERSC), ReFrame, Ramble(Google), Benchpark(LLNL), XDMoD Application Kernels. **6년 연속 workshop 등장(FTXS21 → HPCTESTS 2023/24/25/26)** | **NOT FOUND. 전용 workshop 시리즈(HPCTESTS 4회)가 존재하는데 SC/HPDC/IPDPS/Cluster/DSN regular 논문 0편** | — | L2 / D4 | *"조용히 저하된 노드에 production 용량의 몇 %가 소실되며, 주어진 테스트 cadence가 사는 탐지 지연은 얼마인가"* — 정량판을 아무도 쓰지 않았다 | HPCTESTS 2023–2026; HPCSYSPROS22 NERSC; FTXS21 DeBardeleben | **STILL_OPEN** |

---

# PART II — 축별 종합 판정 (원 요청 §11의 A–G)

각 축에 대해 **가장 강한 기존 방법 / 가장 가까운 production 구현 / 남은 차이 / 판정 / SC 심사에서의 최강 반론**을 정리한다.

---

## AXIS A — Cross-layer performance degradation / RCA

**가장 강한 기존 방법: Kaleidoscope (SC20).** anomaly → component localization → failure-mode classification → likely cause를 **843건의 실제 production 이슈**로 99.3%/95.8%로 검증한 유일한 HPC 연구.
**하지 않는 것:** 단일 서브시스템(분산 스토리지)에 한정. 모델 계층을 도메인 지식으로 손수 구축. GPU·fabric switch·스케줄러 정책·facility 신호 없음. 운영자 조치를 내놓지 않음. 다른 시스템/서브시스템 이식 미실증.

**breadth 준우승: PACE (SC'25 Workshops, `10.1145/3731599.3767471`).** cooling/power/network에 대한 명시적 causal discovery. 그러나 **workshop**이고, lag-aware Granger를 쓰며(실제 짧은 telemetry window에서 붕괴한다고 실증됨), job 성능을 건드리지 않고, 검증이 "물리 과정과 부합한다"이지 인시던트 ground truth가 아니다.

**가장 가까운 production 구현:** LDMS/OVIS + DCDB-Wintermute + Kafka(STREAM)/Prometheus → Grafana + 임계값 알림 + 사람의 티켓 분류. ML 탐지기가 운영자 콘솔에 실제로 연결된 것은 Prodigy/E2EWatch(Sandia)와 NodeSentry(NG-Tianhe)뿐. **cross-layer causal RCA를 운영하는 센터는 없다.**

**남은 차이 (구체적·검증가능):**
1. **Layer-identifiability.** 센터가 수집하는 telemetry로 책임 계층이 애초에 식별 가능한가? 아무도 identifiability/confusion 분석을 발표한 적이 없다. 검증법: 계층별 주입 결함에 대한 계층 귀속 confusion matrix를 production 규모에서 구축.
2. **배치(placement) 교란 하의 귀속.** Slurm placement가 노드 건강과 fabric locality를 confound한다. **스케줄러를 조건화한 연구가 없다. 이것은 HPC 고유이며 클라우드 RCA에 등가물이 없다.**
3. **explanation-value가 아니라 action-value.** 모든 HPC 논문이 F1/top-k로 평가한다. **운영자 조치의 regret을 평가한 논문이 없다.**

**판정:** **PARTIALLY_ADDRESSED** — 세분하면 탐지 `CLOSED`, localization `PARTIALLY_ADDRESSED`, causal attribution `STILL_OPEN`, operator action `STILL_OPEN`.

**최강 반론 (심사평 예상):** *"Cross-layer, multi-modal RCA with causal graphs is a mature literature in cloud/microservices (CauseInfer, Sage ASPLOS'21, CausalRCA, RCD, CIRCA). Kaleidoscope did it for HPC storage at SC'20. PACE did causal discovery on datacenter telemetry at SC'25W. The authors have changed the domain, not the method."*
**추가로 ISSRE'25 *Too Many Cooks*가 더 위험하다** — multi-source fusion이 수익 체감 또는 음의 수익이라는 실증. 문제가 풀렸다는 게 아니라 **전제가 틀렸을 수 있다**는 공격이다.
**방어 가능한 답:** (i) 스케줄러 + 밀결합 collective에 의한 HPC 고유 confounding — 마이크로서비스의 request trace 가정을 통째로 깨뜨린다(HPC에는 request trace가 없다. 이것이 진짜 구조적 차이이며 여기서 시작해야 한다). (ii) DOE 밖에서 아무도 발표하지 못한 규모의 운영자 검증 인시던트 코퍼스. (iii) identifiability negative result. **파이프라인 조합은 통과하지 못한다.**

> ⚠️ **SC26 위험:** Best Paper finalist *From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System*(ORNL)이 이 축 정중앙이다. **공개 즉시 읽고 재평가할 것.**

---

## AXIS B — Cross-system / cross-generation generalization

**가장 강한 demonstrated 결과: CroSysLog** (arXiv 2412.15445) — MAML 학습 단일 모델, source 2개, support 2,000 이벤트로 미지 슈퍼컴퓨터 2대에서 F1 97.6–99.2%. 단일 source는 33.8–58.7%로 붕괴, MAML 없으면 0.04–18%.
**가장 강한 개념적 위협: CENTILE**(arXiv 2608.01725) — telemetry foundation model, 개월 간 zero-shot 전이와 도메인 간 pretrained weight 전이를 주장하고 **의사결정 품질로 평가**한다(mean bounded slowdown 최대 77% 감소).
**하지 않는 것:** CroSysLog는 **텍스트 로그 전용** — DCGM·fabric counter·전력 같은 수치 telemetry를 전혀 건드리지 않는다. 4개 "시스템"은 2005–2006 CFDR 클러스터로 같은 시대·같은 아키텍처 계열·같은 로그 관용구다. 배포도 ROI 측정도 없다(저자 자인). **schema 변경을 다루지 않는다** — 자유 텍스트를 써서 schema를 우회한다. CENTILE은 telemetry 비용을 고려하지 않고, "도메인 간"은 "GPU 세대 간"이 아니며 preprint다.

**선물 같은 논문: SeT-Diff (ACM Computing Frontiers '26, arXiv 2607.22548).** 동기가 *정확히* 이 축이다 — *"models fail when hardware configurations change, sensor metrics vary, or layouts are reconfigured"* — 그리고 **cross-system/cross-generation 전이를 명시적으로 평가하지 않는다.** 2026년 논문이 당신의 문제를 이름 붙이고 열어둔 채 남겼다.

**가장 가까운 production 구현: 없다.** Netti et al.이 센터들이 *"insular ODA solutions"*를 돌린다고 못박고, future work로 *"develop portable, shareable ML models across institutions"*를 든다. 커뮤니티의 유일한 움직임은 HPC ODA Commons(데이터 *계약*이지 이전 가능한 모델이 아님). Bartolini 그룹은 **per-node 모델**과 노드 간 federated learning을 쓴다.

**남은 차이:**
1. **전이 손실 행렬 정량화.** {M100(V100/IB-HDR), Fugaku(A64FX/Tofu-D), Eclipse(CPU), Nurion(KNL/OPA), 한강(H100급/Slingshot)}에서 학습·교차평가. ΔF1, Δ탐지지연, 목표시스템 복구 표본 수.
2. **어떤 shift가 아픈지 분해.** (i) 하드웨어 세대 shift, (ii) schema shift, (iii) workload mix shift, (iv) 스케줄러 정책 shift. **어떤 systems 도메인에서도 이 분해를 한 사람이 없다.**
3. **물리적으로 근거 있는 invariant feature가 격차를 메우는가.** 가설: raw counter는 이전되지 않지만 *무차원* 파생량(utilization ratio, bytes/flop, stall fraction, power/TDP, capacity 정규화 queue depth)은 이전된다. 검증이 싸고, 어느 쪽 결과든 쓸모 있다.
4. **정확도가 아니라 유지비용.** SE venue가 "언제 재학습하나"를 소유한다. **HPC 센터의 연간 GPU-시간으로 가격을 매긴 사람이 없다.**

**판정:** **STILL_OPEN (수치 HPC telemetry)** · **CLOSED (텍스트 로그)** · **PARTIALLY_ADDRESSED (방법론 — SE 문헌이 drift/재학습/모델선택을 소유)**
세부: cross-system log AD = **CLOSED**(가지 말 것). cross-*generation*(GPU/NIC) = **STILL_OPEN, 완전 미개척**. schema 강건성 = **PARTIALLY_ADDRESSED**.

**최강 반론:** *"Cross-system generalization, concept drift, model-update strategy and model-selection for AIOps are a mature body of work in TOSEM/EMSE/ICSE, and cross-system anomaly detection specifically has been solved with meta-learning at ICSE'24 and beyond. This paper transfers a known technique to a new modality."*
**방어:** (i) 그 연구는 전부 로그 또는 클라우드 KPI다 — **아무도 수치 HPC telemetry에서 손실을 측정한 적이 없고**, 유일한 측정치(0.898→0.726, 같은 시스템의 노드 간)는 손실이 크다고 시사한다. (ii) HPC에는 클라우드에 없는 shift 유형이 있다 — **counter schema가 바뀌는 하드웨어 세대 shift**(V100 DCGM 필드 ≠ H100 DCGM 필드; Aries counter ≠ Slingshot counter) — 이는 모든 domain adaptation 방법이 전제하는 "같은 feature space, 다른 분포"를 깨뜨린다. (iii) 분해 + invariant representation 결과는 응용이 아니라 메커니즘 기여다. **(ii)로 시작할 것. SE 문헌이 구조적으로 가질 수 없는 유일한 카드다.**
**DSN'24 (Huawei) *Investigating Memory Failure Prediction Across CPU Architectures*는 직격탄이다** — 하드웨어 고장 예측 모델의 아키텍처 간 전이를 문자 그대로 했다. axis B를 하드웨어 고장 예측으로 인스턴스화하면 반드시 인용·차별화해야 한다.

---

## AXIS C — Telemetry cost vs downstream intelligence

**가장 강한 기존 방법 (두 세계):**
- **형식적 비용-효용:** PINT(SIGCOMM'20, 패킷당 hard bit budget + 증명된 bound, 16 bit/packet이 full-INT 품질에 필적), Sonata(SIGCOMM'18, 실제 하드웨어 자원 제약 하 ILP query partition + dynamic refinement, 3–7 자릿수 감소). **하지 않는 것:** 효용 함수가 *패킷 스트림* 위 *프로그래머블 데이터플레인*에서의 *정확하거나 해석적으로 bound 가능한 의미론의 선언적 query*다. HPC 운영 telemetry는 셋 다 없다 — 고정 schema 주기 counter, 프로그래머블 수집 기질 없음, 효용이 **학습된 비해석적 하류 탐지기**. 비용도 다르다: 스위치 메모리/스테이지/패킷당 비트 vs **수집기 CPU + 네트워크 + 장기 저장(20 PB/5년)**.
- **production 비용-편익 최적화:** **SuperBench의 Selector(ATC'24 Best Paper)** — 10만 GPU 규모에서 관측 비용과 탐지 이득을 명시적으로 최적화한 유일한 배포 시스템. **하지 않는 것:** *능동 벤치마크 스케줄링*(비용 = 훔친 GPU 시간) 최적화이지 수동 telemetry 수집(비용 = 바이트)이 아니다. 클라우드다.

**가장 가까운 production 구현:** LDMS/DCDB + Kafka(STREAM)/Prometheus + Cassandra/Elasticsearch, 세 개의 무딘 레버(§G11). ORNL 자신의 축소 전략은 *"identifying data fields that either provide no useful information"* — 즉 수동이다.

**남은 차이 — 야심 순:**
1. **측정 격차 (쉽고 가치 높고 현재 비어 있음).** CUG2023 pap149는 1 Hz 모니터링이 *"no statistically significant adverse effects"*라고 **측정치를 제시하지 않고 단언한다.** 현대 GPU 시스템에서 샘플링 rate를 바꿔가며, 밀결합 collective와 jitter 민감 앱으로, 규모에서 수행한 엄밀한 모니터링 교란 연구가 문헌에 없다. 이것만으로 ISC/Cluster/MODA 논문이 되고, SC 논문의 필수 구성요소다.
2. **탐지 지연 격차.** 운영자가 실제로 신경 쓰는 지표다(10분 늦게 죽인 노드 = 10분 × N 노드). **HPC AD 논문 중 F1을 샘플링 간격의 함수로 보고한 것이 단 하나도 없다.** NodeSentry는 포인트당 36 ms 추론을 보고하지만 60초 vs 15초 vs 1초 수집에서 무슨 일이 일어나는지 묻지 않는다.
3. **탐지-진단 비대칭 (가장 날카로운 주장).** 가설: **탐지는 싸고 진단은 비싸다** — 작고 거친 metric 부분집합으로 *탐지*는 충분하지만, *어느 계층이 문제인지 localize*하려면 탐지가 버린 metric과 해상도가 필요하다. 참이면, "97%를 잘라도 F1이 유지되었다"는 모든 결과가 **수집을 줄여도 된다는 논거로서 무효**가 된다 — 잘린 metric이 바로 RCA가 필요로 하는 것이기 때문이다. **HPC·클라우드·네트워킹 어디에서도 이를 검증한 논문을 찾지 못했다.**
4. **결합 정식화.** minimize bytes(metric-subset × sampling-rate × retention-tier) s.t. 탐지 F1 ≥ τ, 탐지 지연 ≤ δ, RCA top-k localization ≥ ρ. **계층적 답**(항상 저rate 수집 / 트리거 시 고rate burst / 인시던트 주변만 전해상도 보존) — Sonata의 dynamic refinement를 query predicate 대신 학습된 탐지기가 트리거하는 HPC 판.

**판정:** **STILL_OPEN (HPC)** · **CLOSED (네트워크 flow telemetry)** · **현재 HPC 관행 자체는 ENGINEERING_ONLY**

**최강 반론:** *"Telemetry-cost-under-accuracy-constraint was formalized and solved in networking — Sonata, PINT, AutoSketch — with formal bounds this paper does not provide. On the HPC side, metric reduction is routine: NodeSentry (SC'25) already cut 3,014 metrics to 82 with no accuracy loss. This is feature selection with a cost label attached."*
**방어:** (i) 그 시스템들은 *프로그래머블 데이터플레인 위 해석적 의미론의 query*에 대해 최적화한다. HPC 효용은 **닫힌 형태가 없는 학습된 탐지기**이고 지배적 비용은 **다PB 보존**이다 — 목적도, 제약 집합도, 해의 구조도 다르다. (ii) **NodeSentry는 모델이 소비하는 것을 줄였지, 시스템이 수집·전송·저장하는 것을 줄이지 않았다.** 3,014개 metric은 여전히 수집되고, 여전히 전송되고, 여전히 저장된다. **수집을 멈춰도 된다는 것을 보인 사람이 없다.** (iii) **탐지-진단 비대칭** — 탐지를 보존하는 축소가 진단을 파괴한다면 기존 축소 문헌 전체가 틀린 질문에 답한 것이고, 그것을 보이는 것은 진짜 결과다. **(iii)으로 시작할 것. 셋 중 유일하게 범위 논증이 아니라 새로운 과학적 주장이다.**

---

## AXIS D — Slow-node 진단의 원인 판별

**가장 강한 기존 방법:** GPU 클러스터 fail-slow는 **ARGUS**(>1만 GPU, 6개월 상시, <2% overhead, 커널 이벤트 3700배 압축, progressive diagnosis로 compute straggler / **link degradation** / pipeline-bubble amplification / FlashAttention JIT stall / communication-masked compute straggler를 *명명*), HPC 스토리지는 **Kaleidoscope**(843건 실제 라벨, 원인 클래스 **2개**를 95.8%로 판별).
**ARGUS가 하지 않는 것:** 일반 다중 테넌트 HPC 배치 워크로드에 대해 아무것도. 참조 모델이 *동기적·반복적·동질적* 학습 job이며 — 그 주기성이 "rank i와 rank j를 iteration k에서 비교"를 가능하게 한다. Slurm 스케줄 이기종 MPI job 개념 없음, CPU-only job 없음, Lustre 없음, cooling/power 없음, cross-job 간섭 귀속 없음, topology/placement 원인 클래스 없음.

**가장 가까운 production 구현: Frontier `checknode` (Ezell, CUG'23).** 685 blade / 약 6,000만 컴포넌트, MTBF가 *시간* 단위. boot 시와 매 Slurm epilog에서 결정적 임계값 검사, 에러 문자열을 이유로 자동 drain, **`checknode` 자신이 설정한 이유일 때만 자동 resume**. **ML 0. "어느 검사가 실패했나" 이상의 원인 판별 0.** root cause는 사람이 티켓을 여는 것이다. 나머지 표의 전부가 연구이고, 이것이 실제로 돌아가는 것이다.

**남은 차이:** 자기 이력 대비 런타임이 비정상인 job에 대해 {GPU 저하, CPU 주파수/열 throttle, NIC/링크 저하, 이웃 job의 fabric 혼잡, Lustre 경합, placement/topology, 애플리케이션 내재}에 대한 **순위 원인 귀속**을 내고, production Tier-0에서 **≥6개월** 운영자 확인 ground truth로 평가.

| 요건 | ARGUS | Kaleidoscope | NodeSentry | E2EWatch | IPDPS'26 |
|---|---|---|---|---|---|
| production HPC 배치(LLM 학습 아님) | ✗ | ✓ | ✓ | ✓ | ✓ |
| ≥4개 원인 클래스 판별 | ✓ | ✗ (2) | ✗ (0) | ✓ (4, CPU/mem만) | 부분 |
| GPU + network + I/O 전부 범위 | ✓ | ✗ | ✗ | ✗ | ✓ |
| 실제(주입 아닌) anomaly | ✓ | ✓ | ✓ | **✗** | ✓ |
| 배포/온라인 | ✓ | ✓ | ✗ | ✗ | ✗ |
| 다개월 trace | ✓ | ✓ | **✗ (1주)** | ✗ | ✓ (4개월) |

**판정:** **STILL_OPEN — 그러나 좁고 빠르게 닫히는 중.** 탐지 단독은 **CLOSED**(NodeSentry, Prodigy, RUAD). LLM 학습 클러스터의 원인 판별은 **CLOSED~PARTIALLY_ADDRESSED**(ARGUS, FALCON, LLMPrism — 전부 2024–26, 전부 production, 전부 >1만 GPU). 일반 다중 테넌트 HPC의 원인 판별만 **STILL_OPEN**.

**두 가지 주의:**
- **IPDPS 2026(Wei, Pradeep, Bhatele)이 Perlmutter + Frontier에서 이미 측정을 수행했고, 네트워크 혼잡이 변동성을 지배하며 개별 GPU 성능은 안정적이라고 보고했다.** → **"GPU가 주범"이라는 순진한 프레이밍은 이미 측정되어 반박되었다.**
- SC25 NodeSentry가 채택되었다는 사실은 SC PC가 국가센터의 탐지 전용 연구를 받아준다는 뜻이지만, 동시에 **이제 탐지 전용 제출은 파생적**이라는 뜻이다.

**최강 반론:** *"ARGUS (2026) already does always-on multi-cause fail-slow diagnosis at 10,000-GPU production scale with six months of deployment, and Kaleidoscope (SC'20) already did PGM-based cause discrimination on a production HPC system with 843 real labels. What is new here besides the machine being a Korean one?"*
**추가 위협: Tuncer et al. TPDS 2019가 7년 전에 이 축을 HPC에서 이미 했다.** 인용하고 이기지 못하면 심사를 통과하지 못한다.
**방어:** ARGUS가 구조적으로 만들 수 없는 원인 taxonomy(cross-job 간섭, topology/placement, Lustre, cooling/power) + ARGUS의 iteration 주기성 가정이 깨지는 **이기종 배치 job**에서의 평가.

---

## AXIS E — Label-scarce operational learning

**가장 강한 position: M100 ExaData + RUAD 쌍.** Tier-0 telemetry 2.5년을 공개하고, 운영 알림 시스템(Nagios offline-state)에서 약한 label을 유도하고, 그 label 위 분류기가 **AUC 0.57**밖에 안 된다고 인정했다. **이 AUC 숫자가 이 축에서 가장 유용한 단일 사실이다** — 운영 상태 약한 label이 그대로는 거의 무정보라는, 발표되고 인용 가능한 자인.
**하지 않는 것:** 원칙적 label 모델이 없다. Nagios-offline을 단일 잡음 oracle로 쓰고, denoising 없고, 소스 융합 없고, confidence 없고, "유지보수로 drain" vs "결함으로 drain" vs "실수로 drain"의 분리가 없다. 티켓·RAS·유지보수 기록을 보완적 약한 소스로 쓰지 않는다. labeling function 프레임워크가 없다.

**가장 가까운 production 구현: 없다.** Nagios/Zabbix/Prometheus 알림 + Slurm drain reason + 티켓 시스템이 **서로 연결되지 않은 4개 소스**로 돌아간다.

**남은 차이:**
1. 이기종 운영 소스(Slurm drain reason 문자열, RAS/syslog 에러 클래스, DCGM XID 코드, 티켓 해결 카테고리, 유지보수/RMA 기록, job exit code)에 대한 **labeling function**과 명시적 잡음 모델(일치/불일치 구조, 소스별 precision) — 단일 oracle이 아니라.
2. **Denoising:** *계획된* 노드 상태 전이와 *비계획* 전이를 분리. RMA 기록을 지연된 고정밀 label로 써서 잡음 소스들의 precision을 부트스트랩.
3. **깨끗한 label 없는 평가:** 고정 alert budget(운영 현실적) 하 보고, **티켓 타임스탬프 대비 탐지까지의 시간**과 **알림이 선행한 티켓의 비율** 보고, **point-adjusted F1을 명시적으로 거부**. 운영자 판정 표본 + inter-rater agreement 추가.

1+2+3을 함께 한 HPC 연구가 없다. 가장 근접한 것(GWDG, arXiv 2603.28781)은 운영자 큐레이션 인시던트 카탈로그 + 고정 1% alert budget + 정직한 lead-time 보고를 하지만 **GPU 28개** 규모다.

**판정:** **PARTIALLY_ADDRESSED — 방법은 CLOSED, label semantics는 STILL_OPEN.**
세부: "HPC 노드용 비지도 AD" → **CLOSED**(하지 말 것). "공개 HPC telemetry 데이터셋" → **PARTIALLY_ADDRESSED / TOO_SITE_SPECIFIC 위험**(M100 2.5년 49.9 TB, Fresco 2,090만 job 75개월 3시스템이 이미 존재; PEARC'26이 계약을 표준화 중). **한국 데이터셋 공개 단독은 SC Technical Paper가 아니다 — PEARC/데이터셋 트랙 논문이다.**

**최강 반론:** *"Weak supervision is a solved ML technique (Snorkel-style); applying it to HPC labels is engineering, and the evaluation critique (Kim et al. AAAI'22) is not yours."*
**방어:** HPC 운영 label의 *구조*가 실질적으로 다르다 — 지연된 RMA ground truth, 계획-비계획 confound, 이진이 아닌 원인 클래스 label, 노드 단위 vs job 단위 label 입도 불일치 — 그리고 응용이 아니라 **재사용 가능한 프로토콜 + 공개된 gold set**을 낸다는 것.

> **E는 D의 자연스러운 동반 기여다.** label 파이프라인이 D 논문의 "real operator-confirmed labels" 주장을 신뢰 가능하게 만든다. **D+E 결합 논문이 각각보다 강하다.**

---

## AXIS F — Safe remediation

**가장 강한 기존 방법: Narya (OSDI'20).** 학습된 안전 인지 조치 정책으로 루프를 닫고 fleet 규모 production에서 검증된 유일한 시스템. 임박 호스트 장애 예측 → 완화 조치 선택(live migrate, soft reboot, mark unallocatable 등) → **온라인 A/B로 정책을 계속 적응** → 15개월 production, 중단 26% 감소.
**하지 않는 것: HPC에 적용되지 않는다.** 클라우드 VM은 언제든 마이그레이션 가능하고 잘못된 조치의 blast radius가 테넌트 하나다. **HPC job은 gang-scheduled 밀결합 MPI/NCCL 할당이며, 노드 하나를 drain하면 job 전체가 죽는다.** "예약된 건강한 노드"는 센터가 계속 지불하는 용량 비용이다. Narya에는 job 수준 blast radius 등가물이 없고, 스케줄러 결합이 없고, *스케줄링* 결정의 rollback이 없고, job 체크포인트 상태 개념이 없다.

**가장 가까운 production 구현:** `checknode`(ORNL Frontier)와 LBNL NHC. 둘 다 결정적 검사 → drain. **confidence 없음, 비용 모델 없음, rollback 없음, 수리 검증 자동화 없음.** `checknode`의 유일한 진짜 안전 아이디어 — **`checknode` 자신이 설정한 drain reason일 때만 자동 resume**(사람이 설정한 drain은 보존) — 은 SC 논문이 일반화·형식화할 수 있는 종류의 provenance-gated automation이다.

**남은 차이:**
1. **Blast-radius 인지 조치 선택.** 노드 n을 drain하는 비용은 상수가 아니다 — 어떤 job이 올라가 있는지, 경과 시간, 체크포인트 신선도, 큐 압력에 의존한다. **이를 모델링한 검증된 연구가 없다.**
2. **Provenance·confidence gated auto-resume + 검증.** `checknode`의 임시방편 규칙을 형식화: 자동 에이전트가 취한 조치는 자동 되돌릴 수 있고, 사람이 취한 조치는 안 된다. confidence 임계값과 **재투입 전 통과해야 할 사후 검증 테스트**를 추가하고 false-return rate를 측정.
3. **이력 로그로부터 drain 정책의 counterfactual/off-policy 평가.** Narya는 *온라인* 실험을 썼다. 센터는 Tier-0에서 drain을 싸게 A/B 할 수 없다. Slurm 노드 상태 이력 + job 결과로부터 remediation 정책을 off-policy 평가하는 것은 미해결이며 진짜 방법론적 기여다.
4. **스케줄러에서 루프 닫기.** Iosup 서베이가 10개 production ODA 프레임워크 전부에서 closed-loop 제어가 *"partially manual"*이라고 보고하며, AI 기반 스케줄러가 *"have not been implemented in MLOps pipelines... due to lack of standardized benchmarks and concerns about interpretability and trust"*라고 적는다.

**판정:** **STILL_OPEN (HPC)** / **CLOSED (클라우드·LLM 학습)**
더 정확히: "장애 예측 후 체크포인트/마이그레이션"은 *개념으로서* **CLOSED**(SC'08 → HPDC'20, 18년 되었고 시뮬레이션으로 소진). **HPC 배치 시스템에서 production 검증된 학습 remediation 정책은 어떤 것도 STILL_OPEN.** `ENGINEERING_ONLY` 위험이 높다 — health score→drain 통합을 만들고 잘 됐다고 보고하면 reviewer는 HPCSYSPROS/CUG 논문이라고 부른다. **연구 내용은 배관이 아니라 의사결정 이론(blast radius, off-policy 평가, 안전 gating)에 있어야 한다.**

**최강 반론:** *"Narya solved adaptive mitigation with online experimentation in production in 2020; FALCON does automatic multi-level straggler mitigation on 10k GPUs; Frontier already auto-drains. The HPC-specific delta is a cost model, which is engineering."*
**지속 가능한 유일한 방어:** **off-policy 평가 방법론**(Tier-0에서 온라인 실험을 할 수 없다 — Narya는 Azure에서 할 수 있었다. 이는 변명이 아니라 진짜 방법론적 차이다) + **job 수준 blast radius**(클라우드 등가물 없음).
추가 위험: **ISSRE'24 *Can We Trust Auto-Mitigation?***가 closed-loop 배포가 ground-truth label을 파괴하는 문제를 이미 제기하고 다룬다. 즉 "닫힌 루프가 평가를 깬다는 것을 알아챘다"도 이미 선점되었다.

---

## AXIS G — Operational LLM / agents

**두 개의 기준선: RCACopilot (EuroSys'24)와 L4 (FSE'25).**
- RCACopilot: 30개 Microsoft 팀에서 **4년 이상** 운영된 *diagnostic collection* 절반 + 653건 라벨 인시던트에서 Micro-F1 0.766, 4.2초. **진짜 systems 기여는 handler 기반 evidence-collection 아키텍처이지 LLM이 아니다.** 하지 않는 것: 서비스 간 일반화(저자 자인), **Macro-F1 0.533** — 드문 카테고리에 약한데 그것이 바로 도움이 필요한 곳이다.
- L4: 실제 900+ accelerator 학습 플랫폼에서 정량화된 진단을 한 유일한 검증 연구. **428건 실제 장애**, 장애당 평균 16.92 GB 로그, **평균 진단 시간 34.7시간, 41.9%가 24시간 초과**. F1 0.873(LLM 시대 log-AD baseline 0.207–0.366 대비), faulty-node top-1 65.8%. **하지 않는 것: 진단 경로에 LLM을 전혀 쓰지 않는다**(Drain + IsolationForest + DTW). 정직하게 **장애의 36%가 로그를 넘어선 다중 모달 데이터를 필요로 하고, 10.1%는 로그 증거를 전혀 남기지 않는다**고 적는다.

**가장 가까운 production 구현: HPC에는 사실상 없다.** 2026년 독립 서베이 2편이 HPC 운영에 문서화된 LLM production 배포가 없고, 조사된 10개 production ODA 프레임워크에 LLM이 없다고 명시한다. 가장 가까운 실제 배포 HPC 산출물은 **FRAGATA**(CESGA, 20년치 RT 티켓 hybrid RAG) — **스페인 지역 학회 발표이고 정량 평가가 없다**(저자 자인). 클라우드에서는 RCACopilot의 수집 계층이 30팀 4년.

**열려 있는 것 / 아닌 것:**
- **열림 (a): HPC용 운영 LLM 벤치마크.** ITBench(94 시나리오, SRE **13.8%**), AIOpsLab, OpsEval, RCAEval, OpenRCA가 전부 *클라우드 마이크로서비스*용이다. **HPC를 다루는 것이 없다** — Slurm 없음, MPI/NCCL collective 없음, fabric counter 없음, 병렬 파일시스템 없음, 배치 큐 의미론 없음, 노드 상태 기계 없음.
- **열림 (b): 진단에 도달하기 위해 이기종 HPC telemetry를 질의해야 하는 agent**, 운영자 ground truth 대비 평가. **핵심 조력자이자 핵심 경고:** 실제 telemetry에서 RCA 실패의 **65.7%가 reasoning gap이지 데이터 부족이 아니며**, **고전 causal discovery baseline 전부가 Acc@1 0%**다. 즉 문제는 실재하고 미해결이지만, **causal graph를 해법으로 제안하면 안 된다** — 이미 spurious edge를 쌓는다고 실증되었다.
- **닫힘 (c): log summarization, chatbot, 티켓 FAQ 생성, 문서 RAG.** workshop/PEARC 소재다. 여기에 SC Technical Paper를 세우지 말 것.

**판정:** **PARTIALLY_ADDRESSED이며, HPC에 한정하면 INSUFFICIENT_EVIDENCE → STILL_OPEN 방향.**
세부: 클라우드 인시던트 RCA용 LLM = **CLOSED**. 운영 LLM agent 벤치마크 = **클라우드 CLOSED, HPC STILL_OPEN**. HPC 운영용 LLM/agent = **STILL_OPEN이나, 누군가 작동을 보인 적이 있다는 증거가 INSUFFICIENT**. 2026년 서베이 2편이 독립적으로 production 배포 0건을 보고한다 — 이는 활짝 열린 gap이거나, 가치가 없다는 신호다.
**축 자체로는 `ENGINEERING_ONLY` 위험이 가장 크다.** 안에 LLM이 들어 있는 *systems 메커니즘*이 기여일 때만 성립한다: (i) **비용 제한 evidence collection**(agent가 요청하는 telemetry에 비용을 지불해야 한다 — G축을 C축에 연결), (ii) **grounding/검증**(agent의 모든 주장이 telemetry query로 확인 가능해야 하며 운영 데이터에서 hallucination rate를 측정), (iii) **action guard**(허용 remediation의 형식적 envelope — F축에 연결).

**최강 반론:** *"Microsoft did LLM incident RCA in production in 2023–24 (ICSE'23, EuroSys'24); AIOpsLab and ITBench already benchmark ops agents; ITBench shows agents score 13.8% on SRE tasks, and 'How Far Can RCA Go' shows the ceiling is agent reasoning, not data. Substituting Slurm for Kubernetes is a domain port, not a contribution."*

---

# PART III — 축 순위와 두 개의 "가지 말 것"

## 3.1 두 독립 감사의 순위 (원자료 F와 G가 각각 도출)

| | 감사 F (축 A/B/C) | 감사 G (축 D/E/F/G) | 감사 C (DSN/ISSRE 관점, 7축 전부) |
|---|---|---|---|
| 1위 | **C** telemetry cost | **D+E 결합** | **C** telemetry cost — STILL_OPEN |
| 2위 | **B** cross-generation | **G** Shape-1 (HPC agent 벤치마크) | **F** safe remediation, HPC 비용 모델 |
| 3위 | **A** cross-layer RCA (최고위험) | **F** safe remediation (평가 불가 위험) | **E** label semantics (측정으로 재프레이밍) |
| 4–7위 | — | — | **A** → **D** → **B** → **G**(ENGINEERING_ONLY) |

**세 감사가 독립적으로 C를 1위 또는 공동 1위로 놓았다.** 이것이 이 조사에서 가장 강한 수렴 신호다.

## 3.2 절대 하지 말 것 (두 감사가 독립적으로 같은 경고)

1. **HPC node-level anomaly detector를 제안하지 말 것.** SC'23 Prodigy와 SC'25 NodeSentry가 이 lane을 닫았다. RUAD, ExaMon 계열도 있다.
2. **cross-system *log* anomaly detection을 제안하지 말 것.** ICSE'24 MetaLog + CroSysLog가 F1 97–99%로 닫았다.
3. (추가) **causal graph discovery를 RCA 해법으로 제안하지 말 것.** 실제 telemetry에서 Granger/PC/FCI/LiNGAM/NTLR 전부 Acc@1 0%로 실증되었다.
4. (추가) **"우리는 노드를 peer와 비교한다"를 기여로 삼지 말 것.** IASO(ATC'19)가 3.9만 노드에서 production-solved.
5. (추가) **한국 데이터셋 공개 단독으로 SC Technical Paper를 노리지 말 것.** M100/F-DATA/Fresco가 이미 있다. PEARC/데이터셋 트랙 논문이다.

## 3.3 세 축의 교집합에 있는 단일 최강 질문

원자료 F가 도출했고, 이 조사 어디에서도 반증하지 못한 질문:

> **탐지 품질을 보존하는 telemetry 축소가 cross-layer *진단* 품질을 파괴하는가 — 그리고 최적화된 telemetry 부분집합은 HPC 세대를 넘어 이전되는가, 아니면 시스템마다 다시 유도해야 하는가?**

A × B × C의 교집합이다. 반증 가능하고, 어느 쪽 결과가 나와도 발표 가능하며, 대형 센터가 이미 수집하는 telemetry만 필요하고, baseline(NodeSentry, Prodigy, Gorilla, Sonata-refinement, MAML-transfer)이 전부 존재하고 실행 가능하다. **이 질문을 던진 논문을 찾지 못했다.**

---

# PART IV — 이 문서의 판정을 뒤집을 수 있는 미확보 문헌

관련연구를 쓰기 전에 반드시 확보해서 읽어야 한다. **어느 것이든 위 판정을 바꿀 수 있다.**

| 문헌 | venue / ID | 어느 축을 위협하나 | 상태 |
|---|---|---|---|
| **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** (Khan, Zimmer, George, Karimi, Wang, Shin — ORNL) | **SC26 Best Paper finalist** | **A (정면)** | DOI 미발행, 미개최. 공개 즉시 확보 |
| **Mantis: Decoding HPC Telemetry Data for Robust System Prediction** | ACM **ICS 2026**, `10.1145/3797905.3800527` | B, D, F | 403 차단, 내용 미확인 |
| **Safe Remediation as Risk-Constrained Intervention Decision in Microservice Systems** | arXiv 2607.20005 (2026) | **F (정면 선점 가능)** | fetch rate-limited, 내용 미확인 |
| **HPC ODA Commons: Community-Governed Contracts and Toolkit** | **PEARC'26**, `10.1145/3785462.3815891` | B(schema), E(데이터셋 공개) | 403, 내용 미확인 |
| **WisIO: Automated I/O Bottleneck Detection with Multi-Perspective Views** | **ICS'25**, `10.1145/3721145.3725742` | A(I/O 계층) | 저자·내용 미확인 |
| **ALBADross 후속 / Runtime Performance Anomaly Diagnosis Using Active Learning** | **IEEE TPDS 2024**, `10.1109/TPDS.2024.3365462` | D, E | 403 |
| **Labeling the Invisible: A Scalable Framework for Labeling Fail-Slow Failures in Cloud Storage** | FAST(연도 `UNVERIFIED`, '26 추정) | **D+E ground truth gap 정면** | 미확인 |
| DSN 2020 · DSN 2021 전체 proceedings | — | 전 축 | 프로그램 페이지 소실/차단, in-scope 3–8편 누락 추정 |
| ISC research-paper 2024–2026 | Springer | 전 축 | 미확인. **"track이 없어졌다"고 쓰지 말 것** |
| CUG 2026 proceedings | cug.org | practice 전반 | 404. 2027년 초 재확인 |
| Nezha(FSE'23), Sage(ASPLOS'21), Nenya(KDD'22), Mint(ASPLOS'24), NVMe SSD Failures(ATC'23), Cores that don't count(HotOS'21), Borghesi(AAAI/IAAI'19, TPDS'22) | 각 venue | A, C, F | ACM DL/Xplore 차단으로 UNVERIFIED |

**인용 위생 정정 1건:** Gainaru et al. SC 2012 논문의 정확한 제목은 **"Fault prediction under the microscope: a closer look into HPC systems"**(`10.1109/SC.2012.57`)이다. 널리 유통되는 "…a closed-loop approach" 변형은 **틀렸다.**

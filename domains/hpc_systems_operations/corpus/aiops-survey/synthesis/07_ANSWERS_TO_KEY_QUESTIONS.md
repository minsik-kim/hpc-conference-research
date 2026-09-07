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

# 07. 최종 10개 질문에 대한 답변

**작성일:** 2026-09-06 · 근거는 `01`–`06`에 있으며, 여기서는 결론만 직접 답한다.

---

## Q1. HPC AIOps / Operational Intelligence 관련 SC regular paper precedent는 실제로 얼마나 존재하는가?

**적다. 연 4–12편이고, 2024년에 계단식으로 늘었다.**

| 연도 | 열거한 본프로그램 항목 | Core | Broad | Core 비중 |
|---|---|---|---|---|
| SC20 | ~105 | 8 | 14 | ~8% |
| SC21 | ~110 | 4 | 8 | ~4% |
| SC22 | ~92 | 4 | 7 | ~4% |
| SC23 | ~99 | 5 | 11 | ~5% |
| SC24 | ~114 | 10 | 17 | ~9% |
| SC25 | ~120 | 12 | 18 | ~10% |
| SC26 | 미공개 | ≥1 확인 | UNKNOWN | — |

(±2편, 제목 기반 분류 포함. SC22의 저점은 열거 오류가 아니라 실제 dip이며 두 독립 열거가 일치했다.)

**2021–2023 평탄(연 4–5편) → 2024–2025 계단식 증가(연 10–12편).** 증가분은 거의 전부 (a) GPU/AI 클러스터 신뢰성, (b) power/cooling/carbon/water에서 왔다. 이 공간은 **2년 만에 대략 두 배**가 되었다.

**중대한 유보 2가지.**
- SC 논문 페이지는 모든 트랙을 "Technical Papers Archive"로 표시한다. **Technical Paper와 State of the Practice를 구분하지 못했다.** 위 숫자는 "SC 본프로그램"이지 "SC Technical Paper"가 아니다.
- **깊이 있는 진짜 precedent는 훨씬 적다.** `03`에서 심층 분석 가치가 있다고 판정한 것은 SC 본프로그램 9편 + SC 밖 archival 10편이다.

**그리고 센터 관점에서 보면 더 심각하다.** 조사한 15개 주요 센터(ORNL, NERSC, LLNL, SNL, LANL, ALCF, TACC, CSCS, LRZ, CINECA, RIKEN, JSC, BSC, EPCC, NREL) 중 **2020–2026에 production 운영 분석으로 SC 본프로그램 technical paper를 낸 곳은 0곳이다.** 좋은 작업은 SC *Workshops*, CUG, HPCSYSPROS, ISC workshops, HPDC, ICS, *Scientific Data*로 간다. **이것은 실체의 부재가 아니라 구조적 기회다.**

---

## Q2. 어떤 operational problem이 SC regular research로 승격된 전례가 있는가?

승격에 성공한 문제 유형은 여섯 가지로 수렴한다.

| 승격된 문제 | 대표 precedent | 승격시킨 방법 |
|---|---|---|
| **장애·저하의 localization과 원인 분류** | Kaleidoscope SC20 | 계층적 도메인 지식 모델 + **843건 운영자 확인 ground truth** |
| **label 없는 이상 탐지** | Prodigy SC23 → NodeSentry SC25 | "label 부재가 제약이 아니라 문제 정의"라는 재프레이밍 |
| **하드웨어 수명·오류의 통계적 이해** | GPU Lifetimes on Titan SC20 → Story of Two GPUs SC25 | survival analysis / MTBE + 가용성 투영 + **데이터 공개** |
| **오류 예측을 운영 비용으로 평가** | Cost-Aware DRAM Prediction SC20 → RL Mitigation HPDC24 | F1을 **node-hour 비용 모델**로 대체하고, 이후 예측→행동으로 확장 |
| **facility와 IT의 결합 모델링** | ExaDigiT SC24 | 6개월 telemetry replay로 V&V된 digital twin |
| **수집 인프라 자체의 결함** | SIREN SC25 | "job 이름은 거짓말"이라는 전제조건 문제를 privacy-preserving fuzzy hash로 해결 |
| **운영 ML이 왜 실패하는가 (메타)** | I/O ML Error Taxonomy SC22 | **새 알고리즘 없이** 실패 모드 taxonomy + 진단 도구 |
| **닫힌 루프 조치** | Aurora Failure Management SC25 | meta-database + multi-strike 정책, **MTTR 84배** |

**승격 공통 조건 3가지.**
① **운영 성과 지표로 평가한다** (MTTR, node-hour, overprovisioning %) — F1만으로는 한 단계 아래로 읽힌다.
② **production 데이터 + 실제 배포 주장을 함께 낸다** — 2024년 이후 이 기준선이 눈에 띄게 올라갔다.
③ **측정 논문이 먼저, 메커니즘 논문이 나중** — SC22 Not All GPUs → SC24 PAL, SC20 Titan GPU → SC25 Two GPUs, SC21 Summit power → SC24 ExaDigiT, IPDPS'20 Dragonfly → IPDPS'26 Elusive GPU. **1년차 characterization + 2년차 mechanism의 2편 계획이 이 venue의 실제 작동 방식과 일치한다.**

---

## Q3. workshop/CUG에서 반복되지만 아직 regular research로 충분히 해결되지 않은 문제가 있는가?

**있다. 그리고 그 목록이 이 조사의 최대 산출물이다.**

먼저 구조적 사실: **HPCSYSPROS 46편(2020–2025)에서 아카이벌 승격이 추적되는 사례 0건. HPCTESTS 10편 이상에서 0건.** PIKA, LLview, XDMoD Application Kernels, Arbiter, EMOI, CEEMS, buildtest, Ramble, ORNL ODA 대시보드 — **어느 것도 SC/HPDC/IPDPS/Cluster/DSN regular 논문이 없다.**

그리고 **2019–2025 SC/ISC의 ODA 활동은 workshop이 아니라 BoF 시리즈였다.** HPC-ODA 2026(SC26)이 8년간의 BoF를 peer review로 전환하는 **1회차**다. → **SC측 ODA 커뮤니티가 8년간 운영 문제를 생산하면서 아카이벌 논문 흔적을 전혀 남기지 않았다.**

**아카이벌 논문이 전혀 없는 반복 문제 (상위 10):**

| # | 문제 | 반복 기간 | 아카이벌 상태 |
|---|---|---|---|
| G20 | **지속적 acceptance testing / silent regression 탐지** | 2021–2026 (6년 연속) | **0편.** HPCTESTS라는 전용 workshop 4회차가 있는데 regular 논문 0 |
| G2 | **사용자에게 job 비효율 알리기 — 효과 측정** | 2023–2026 | **0편.** PIKA 5년 production, LLview production, 그러나 행동 변화 측정 0 |
| G3 | **cross-site telemetry schema 표준과 검증** | 2019–2026 (매년) | 개념 프레임워크 1편(Cluster'21)뿐, cross-site 검증 0 |
| G4 | **configuration drift가 job 실패의 원인인가** | 2020–2025 (HPCSYSPROS 매년) | **어디에도 0편.** 아무도 정량화한 적 없음 |
| G5 | **공유자원 저하의 실시간 원인 job 귀속** | 2020–2026 | 특성화는 아카이벌, **온라인 귀속은 0편** |
| G7 | **HPC 운영 데이터의 안전한 공개(익명화/거버넌스)** | 2024–2026 | **0편.** SC25 BoF 설문에서 공개 데이터셋 가용성 **1.6/5 — 최저점** |
| G9 | **login node 남용의 closed-loop 통제** | 2023–2025 | **0편.** Arbiter 3가 L7/D5로 실제 돌아가는데 peer review 평가가 없다 |
| G10 | **운영 정책 변경의 counterfactual 평가** | 2023–2026 | **0편.** ExaDigiT가 물리를 풀었고 정책 방법론은 공백 |
| G1 | **backfill 기반 silent-defect screening 정책** | CUG | **0편.** ORNL이 ground truth와 negative baseline을 이미 공개 |
| G6 | **HPC 운영 log triage / RCA에 LLM** | 2023→2026 (가속 중) | HPC 특화 아카이벌 0편. **2027년에 누군가 쓸 것 — 창이 지금이다** |

CUG 역검색(R1–R10)에서도 **7건이 `NO CLOSE ARCHIVAL WORK FOUND`**였다: screening-policy 최적화, quarantine 의사결정 정책, fabric counter 부분집합 선택, 인터커넥트 telemetry의 스트리밍 요약, retention/downsampling 최적화, 모니터링 control plane의 backpressure, telemetry schema 진화. 유일하게 `CLOSE ARCHIVAL WORK EXISTS`였던 것은 스토리지 straggler(Lockwood SC18, Kaleidoscope SC20)다.

---

## Q4. anomaly detection 이후 RCA/decision/remediation은 어느 정도까지 발전했는가?

**L3에서 절벽이 있다.**

| 레벨 | HPC 아카이벌 문헌 | HPC production 현실 | 비HPC |
|---|---|---|---|
| L3 탐지 | **포화** (Prodigy SC23, NodeSentry SC25, RUAD, ExaMon 계열) | 시범 수준 (Sandia, NG-Tianhe만 운영자 콘솔 연결) | 포화 |
| L4 예측 | 활발 (DRAM/UE, disk, GPU 메모리, 런타임, 전력) | 거의 없음 | 활발 |
| **L5 RCA** | **희소.** Kaleidoscope(스토리지 한정), AIIO(I/O 한정), ClusterRCA(네트워크 한정) | **없음. cross-layer causal RCA를 운영하는 센터가 0곳** | 성숙 (RCACopilot, FIRM, Eadro) |
| **L6 권고** | 거의 없음 | 없음 | 있음 |
| **L7 닫힌 루프** | **6년간 SC 본프로그램 1편**(Aurora, 정책 공학). HPDC/IPDPS/Cluster ~700건 중 사실상 1편(HPDC'24 RL-DRAM) | **규칙 기반만** (checknode 자동 drain, NHC, Arbiter 3, NERSC ServiceNow 자동 워크플로) | **성숙** (Narya 15개월/26%↓, FALCON, SuperBench, Perseus) |

**핵심 수치:** 독일 8개 국가센터 컨소시엄이 공식 문서에 이렇게 적었다 — *"Machine Learning on the time series data is feasible but challenging. There are ongoing investigations how ML can be used to provide additional insights, but **none of the German sites in this study are using this in production at present.**"* Iosup 그룹의 10개 production ODA 프레임워크 조사도 closed-loop 제어가 *"partially manual"*이라고 보고한다.

**결론: 탐지는 닫혔고, 예측은 활발하고, RCA는 서브시스템 안에서만 되고, 조치는 규칙 기반이다. L5→L7 구간이 census 전체 최대의 구조적 공백이며, 그 공백은 클라우드에서는 이미 메워졌다.**

---

## Q5. cross-system / cross-generation generalization은 실제로 해결되었는가?

**텍스트 로그는 해결되었다. 수치 telemetry는 아무도 측정조차 하지 않았다.**

- **해결(CLOSED):** cross-system *log* anomaly detection. MetaLog(ICSE'24), CroSysLog(MAML, 미지 시스템 2대에서 support 2,000 이벤트로 **F1 97.6–99.2%**), ZeroLog(ISSRE'25), LogTAD. **여기로 가지 말 것.**
- **미해결(STILL_OPEN):** 수치 HPC telemetry. **두 사이트 간, 두 GPU 세대 간, 두 fabric 세대 간, telemetry schema 변경 시의 전이 손실을 측정한 발표 연구가 존재하지 않는다.** 유일한 측정치는 3쪽짜리 워크숍 논문의 **F1 0.898 → 0.726**이고, 그것도 *같은 시스템의 노드 간*이다.
- **production 현실:** 없다. Netti et al.이 센터들이 *"insular ODA solutions"*를 돌린다고 못박는다. Bartolini 그룹은 **per-node 모델**과 노드 간 federated learning을 쓴다 — 한 시스템 *안에서도* 단일 모델이 안 맞는다는 최강 증거.
- **결정적 정황:** **SeT-Diff**(ACM Computing Frontiers '26)가 이 문제를 동기로 명시하고(*"models fail when hardware configurations change, sensor metrics vary, or layouts are reconfigured"*) **cross-system/cross-generation 전이를 평가하지 않는다.** 2026년 논문이 문제를 이름 붙이고 열어둔 채 남겼다.

**HPC 고유의 shift 유형이 존재한다:** counter schema가 함께 바뀌는 **하드웨어 세대 shift**(V100 DCGM 필드 ≠ H100 DCGM 필드; Aries counter ≠ Slingshot counter). 이는 모든 domain adaptation 방법이 전제하는 "같은 feature space, 다른 분포"를 깨뜨린다. **SE 문헌이 구조적으로 가질 수 없는 카드다.**

⚠️ 단, **DSN'24(Huawei) *Investigating Memory Failure Prediction Across CPU Architectures***가 하드웨어 고장 예측의 아키텍처 간 전이를 문자 그대로 했다. 이 축을 하드웨어 고장 예측으로 인스턴스화하면 직격탄이다.

---

## Q6. telemetry sampling/storage overhead 자체가 SC급 systems research가 될 여지가 있는가?

**있다. 그리고 세 개의 독립 감사가 모두 이것을 1위 또는 공동 1위로 놓았다 — 이 조사에서 가장 강한 수렴 신호다.**

**근거:**
- **어떤 HPC 시스템에 대해서도 telemetry 비용 대 하류 운영 품질의 Pareto frontier가 발표된 적이 없다.**
- 샘플링 간격을 변화시킨 논문 **0편**. 보존 해상도를 변화시킨 논문 **0편**. telemetry rate의 함수로 **탐지 지연**을 보고한 논문 **0편**. 축소가 **RCA**(탐지가 아니라)에 미치는 품질 비용을 측정한 논문 **0편**.
- HPC 측의 모든 축소 결과(NodeSentry 3,014→82, Prodigy 806→156, Tuncer −57%)는 **모델이 소비하는 것**을 줄였을 뿐 **시스템이 수집·전송·저장하는 것**을 줄이지 않았다.
- CUG2023 논문이 1 Hz 모니터링에 *"no statistically significant adverse effects"*라고 **측정치 없이 단언한다.** 현대 GPU 시스템에서의 엄밀한 모니터링 교란 연구가 문헌에 없다.
- 비용은 실재한다: ORNL 데이터센터 **4.2–4.5 TB/day**, STREAM **1.3 TB/day / 5년 20 PB**, 스트림 간 **30만 배** 동적 범위, Slingshot `dump_counters` **약 0.5초/스위치**, HPCM 기본 보존 Kafka 1일/OpenSearch 7일/VictoriaMetrics 7일.
- 반대 방향 증거도 있다: EPCC ARCHER2가 Graphite downsampling이 장기 세밀 분석을 파괴했다고 기록했다.

**하지만 조건이 있다.** 프레이밍이 **메커니즘 + 측정**이어야 하고 압축 파이프라인이면 실패한다. 최강 반론은 네트워킹(Sonata SIGCOMM'18, PINT SIGCOMM'20 — 형식적 bound 보유)과 **SuperBench ATC'24 Best Paper의 Selector**(비용 대 탐지 이득을 명시 최적화, 10만+ GPU 2년 배포)에서 온다.

**유일하게 새로운 과학적 주장은 이것이다:**
> **탐지 품질을 보존하는 축소가 cross-layer 진단 품질을 파괴하는가?** 참이면 기존 축소 문헌 전체가 틀린 질문에 답한 것이다. **HPC·클라우드·네트워킹 어디에서도 이를 검증한 논문을 찾지 못했다.**

**전제조건 하나:** **지금부터 전해상도 다계층 telemetry를 보관해야 한다.** 이미 downsample된 데이터로는 downsampling을 소급 연구할 수 없다.

---

## Q7. Slingshot/GPU/Lustre/Slurm 등을 결합한 cross-layer diagnosis 연구는 어디까지 와 있는가?

**서브시스템 안에서는 잘 되고, 계층을 건너면 아무도 못 했다.**

| 범위 | 최고 도달점 | 한계 |
|---|---|---|
| 스토리지 스택 내부 | **Kaleidoscope SC20** — 843건 실제 이슈, localization 99.3%, root-cause 95.8% | 분산 스토리지 한정. GPU·fabric switch·스케줄러·facility 신호 없음. 원인 클래스 **2개** |
| I/O 스택 내부 | AIIO HPDC'23, WisIO ICS'25 | Darshan 관점만. 서버측 Lustre telemetry 없음 |
| 네트워크 내부 | ClusterRCA ISSRE'25 (HPC 네트워크 fault localization + classification) | 네트워크 전용 |
| facility 계층 | **PACE SC'25 Workshops** — cooling/power/network causal discovery | **workshop**, Granger 기반, **job 성능 미접촉**, 검증이 "물리와 부합"이지 인시던트 ground truth 아님 |
| GPU 클러스터(LLM 학습) | **ARGUS** — >1만 GPU, 6개월, <2% overhead, 다중 원인 판별. **FALCON** L7/D5 | **동기적·반복적·동질적 학습 job 전제.** Slurm 이기종 MPI job, CPU-only job, Lustre, cooling/power, cross-job 간섭 귀속, topology/placement 원인 클래스 전부 없음 |
| **진짜 cross-layer (CPU+GPU+fabric+Lustre+scheduler+facility)** | **없음** | — |

**production에서는 더 단순하다.** LDMS/DCDB + Kafka/Prometheus → Grafana + 임계값 알림 + 사람의 티켓 분류. ML 탐지기가 운영자 콘솔에 연결된 것은 Prodigy/E2EWatch(Sandia)와 NodeSentry(NG-Tianhe)뿐. ORNL EPIC이 유일한 LLM 보조 인터페이스이며 **RCA를 하지 않는다.** **cross-layer causal RCA를 운영하는 센터는 0곳이다.**

**두 가지 최신 경고.**
- **IPDPS 2026**(Wei, Pradeep, Bhatele)이 Perlmutter + Frontier에서 이미 측정했다: **네트워크 혼잡이 변동성을 지배하고 개별 GPU 성능은 안정적이다.** "GPU가 주범"이라는 프레이밍은 이미 반박되었다. 그리고 저자들이 **Rosetta 스위치 counter를 얻지 못했다고 명시**한다 — KISTI가 Slingshot counter를 확보하면 그 자체가 최강 경쟁 그룹 대비 차별점이다.
- **SC26 Best Paper finalist *From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System*(ORNL)이 이 축 정중앙이다.** 공개 즉시 읽고 재평가할 것.

**추가로, 고전 인과추론은 이 데이터에서 작동하지 않는다는 실증이 있다.** 실제 telemetry에서 **Granger, PC, FCI, LiNGAM, NTLR 전부 Acc@1 0%**이며, RCA 실패의 **65.7%가 reasoning gap이지 데이터 부족이 아니다.** HPE Labs+ORNL도 Summit 3년치 27,648 GPU 모니터링에서 사용 가능한 장애 데이터가 **127건**뿐이어서 multivariate transfer entropy가 *"did not produce significant results"*, CCM은 *"only 127 records"*로 굶었다고 보고했다. → **causal graph discovery를 해법으로 제안하지 말 것.**

---

## Q8. production implementation과 research literature 사이의 가장 큰 gap은 무엇인가?

**세 개의 gap이 있고, 방향이 서로 반대다.**

**Gap 1 — 문헌이 앞서 있는 곳: L5–L7.** 문헌은 진단·권고·닫힌 루프를 논하는데 production은 L0–L2에 머문다. 15개 센터 중 production에서 검증된 최고 레벨이 L3를 넘는 곳은 사실상 없다(NERSC가 사전 분류된 장애 클래스에 한해 규칙 기반 L7 부분 보유). 독일 8개 센터 컨소시엄이 공식적으로 "production에서 ML을 쓰는 곳이 없다"고 적었다.

**Gap 2 — production이 앞서 있는 곳: 인프라와 negative result.** 이쪽이 더 흥미롭다. 운영자들은 문헌이 모르는 것을 안다.
- 벤더 telemetry 서비스가 **10만–100만 msg/s를 감당하지 못한다** — 이를 측정하거나 설계 원칙을 낸 논문 0편
- Graphite downsampling이 장기 분석을 파괴한다 — 이를 정식화한 논문 0편
- 주간 스크리닝이 **39,437회 무수확 후 폐기**되었다 — 이런 negative result는 아카이벌 venue에 거의 실리지 않는다
- Fluent Bit가 고처리량에서 불안정했다, DCGM이 *"too intrusive"*라서 거부되었다, Slurm 에너지 값을 *"cannot always be trusted"* — **전부 아카이벌 문헌의 흔한 가정에 대한 직접 반증인데 어디에도 실리지 않았다**
- 조용한 결함 하드웨어가 **6개월에 190만 테스트로 99개 노드**에서 발견된다 — 이 규모의 운영 사실이 아카이벌 문헌에 없다

**Gap 3 — 가장 크고 구조적인 것: 평가 가능성.**
production 시스템에서 **A/B 테스트를 할 수 없다.** 그래서 모든 L6/L7 연구가 시뮬레이션에서 멈추고, 모든 closed-loop 주장이 검증 불가능해진다. 클라우드는 이 문제가 없다(Narya가 Azure에서 온라인 실험을 15개월 돌렸다). **이 비대칭이 HPC 운영 연구가 클라우드 운영 연구에 뒤처진 진짜 이유이며, 방법론적 기여의 기회이기도 하다.**

**그리고 gap을 만드는 메커니즘이 하나 더 있다.** 연구 산출은 시스템 규모가 아니라 **학술 파트너 유무**와 상관된다(Bologna↔CINECA, Bologna↔RIKEN, W&M↔ORNL, Basel/TUM↔LRZ, UMD↔NERSC). 대학 그룹이 결합되지 않은 센터는 practice만 낸다. **그리고 데이터를 공개한 센터가 곧 연구를 내는 센터다** — 공개가 결과가 아니라 원인으로 보인다.

---

## Q9. 현재 접근 가능한 대규모 HPC telemetry로 실제 검증 가능한 research question은 무엇인가?

한강이 고려 중인 계층(Slurm · DCGM · CPU · Slingshot · Lustre · power · cooling/CDU · syslog)으로 **바로 검증 가능한 것**과 **조건이 붙는 것**을 나눈다.

**✅ 즉시 검증 가능 (외부 label 의존성 없음)**

| 후보 | 필요한 것 | 비고 |
|---|---|---|
| **C1 telemetry 축소의 탐지–진단 비대칭** | 전해상도 다계층 trace ≥6개월, 2개 시스템 | **지금부터 전해상도 보관 시작이 전제.** 가장 자족적 |
| **C2 세대 간 전이 손실 분해** | Nurion + 한강 + M100 ExaData + F-DATA | **공개 데이터 2종만으로도 선행 착수 가능.** KISTI의 구조적 우위 |
| **C8 job 효율 리포팅의 행동 효과** | job accounting + 이용률 telemetry + staggered rollout | 새 알고리즘 불필요. 가장 쉬움 |
| **C10 telemetry integrity / observability debt** | 벤더 경로 + 독립 수집기 이중 수집 | 한강 도입 시점에 설계해 넣으면 자연 획득 |

**⚠️ 조건부 (행정적·운영적 전제 필요)**

| 후보 | 전제 |
|---|---|
| **C5 내재적 fail-slow vs 유발 간섭 판별** | **Slingshot fabric counter 접근권**(HPE STT / fabric manager) + 운영자 확인 incident label |
| **C4 label semantics 측정** | **티켓 시스템 export + 유지보수/RMA 기록** 접근권 |
| **C6 remediation 비용 모델 + off-policy 평가** | Slurm 노드 상태 이력의 **actor 필드**(사람/자동화/epilog). **없으면 성립 불가** |
| **C3 backfill screening 정책 최적화** | 자체 screening 프로그램 운영 (한강 초기 운영에 설계해 넣을 것) |
| **C7 HPC 운영 agent 벤치마크** | C4 완료(ground truth) + 데이터 공개 승인 |
| **C9 정책 counterfactual 평가** | digital twin 구축 (ExaDigiT 기반, ORNL 협업 권장) |

**무료로 지금 쓸 수 있는 공개 데이터:**

| 데이터셋 | 규모 | 라이선스 | 용도 |
|---|---|---|---|
| **M100 ExaData** (CINECA) | 49.9 TB, 934일, 573 metric @1s, 980+ 노드, IPMI+Slurm+Nagios label+facility | CC-BY-4.0 | C1 decimation 실험, C2 source 도메인, C4 AUC 0.57 baseline 재현 |
| **F-DATA** (Fugaku) | 2,400만 job, 2021-03~2024-04, 45 feature, 28 GB | Zenodo | C2 두 번째 아키텍처(A64FX/Tofu-D) |
| **HPC-ODA** (LRZ) | 1.5 GB, 5개 task segment, DCDB+LDMS | CC-BY-4.0 | 방법 벤치마킹 출발점 |
| **OLCF Constellation** (Summit) | 1 Hz power/thermal 5개월 + **GPU DBE + XID + 재부팅 + 스케줄러 기록**(27,648 V100) | Constellation T&C | **유일한 공개 GPU-failure-with-telemetry 데이터** |
| **NREL Eagle jobs** | 1,100만+ job, 2018-11~2023-02 | CC-BY-4.0 | 스케줄링·큐 대기 예측 baseline. 진입 장벽 최저 |

---

## Q10. 그중 정말로 SC Technical Paper를 목표로 할 만한 것은 무엇인가?

**관대하게 평가하지 않은 결과는 다음과 같다.**

### `SC Technical Paper plausible` — 3개

**① C1 — telemetry 축소의 탐지–진단 비대칭과 비용/품질 Pareto frontier**
세 독립 감사가 모두 1위로 놓았다. 유일하게 **새로운 과학적 주장**(범위 논증이 아님)을 담고 있다: *탐지를 보존하는 축소가 진단을 파괴한다면, 기존 축소 문헌 전체가 틀린 질문에 답한 것이다.* 운영자 label 의존성이 없어 자족적이다.
**최대 위험:** SuperBench Selector와의 차별화. **전제조건:** 지금부터 전해상도 보관.

**② C2 — 세대 간 telemetry 전이 손실의 분해**
gap 진술이 가장 깨끗하고, **KISTI가 사내에 진짜 cross-generation 쌍을 보유**하며 공개 데이터 2종을 무료로 더할 수 있다 — 경쟁 그룹이 발표하지 못한 구조적 우위다.
**최대 위험:** 데이터셋/측정 논문으로 읽히는 것. **완화:** shift 분해 실험 + invariant representation 결과. **반드시 하드웨어 세대 + schema shift로 시작할 것** — SE 문헌이 구조적으로 가질 수 없는 유일한 카드다.

**③ C3 — backfill 기반 silent-defect screening 정책 최적화**
ORNL이 ground truth(190만 테스트, 99개 노드, 1/14,618)와 **공개된 negative baseline**(39,437회 무수확 후 폐기)을 이미 발표했다. 가까운 아카이벌 연구가 없다.
**최대 위험:** SuperBench Selector. **차별화:** 전용 검증 창이 아니라 **남는 backfill 용량**이라는 자원 모델과, 사용자 워크로드 교란이라는 1급 제약.

### `SC Technical Paper stretch` — 4개
**C4 label semantics**(C5와 결합 시 plausible) · **C5 간섭-내재 판별**(Tuncer TPDS'19와 ARGUS 양쪽에서 압박) · **C6 remediation 비용 모델**(과학적 gap은 최대이나 평가 가능성이 최소) · **C7 HPC 운영 agent 벤치마크**(artifact 가치는 높으나 도메인 이식 반론)

### `strong workshop paper` — 2개
**C8 job 효율 리포팅의 행동 효과** — **첫 논문으로 최적.** 위험이 낮고, 데이터가 이미 있고, **HPC-ODA 2026(SC26, 1회차)** 진입에 완벽하며, 그 PC(LRZ/BU/ORNL/NERSC/HPE)가 나중에 SC 제출물을 심사할 사람들이다. 다중 센터 + staggered rollout + 측정된 효과 크기를 갖추면 **SC State of the Practice** 트랙에 도달 가능하다.
**C10 telemetry integrity** — 단독으로는 workshop, **C1의 필수 구성요소로 통합하면 SC 논문의 일부.**

---

### 그리고 별도 경로: SC State of the Practice

SC26 CFP에서 SotP 트랙 존속이 확인되었고, 범위가 *"All aspects of the pragmatic practices of HPC, including operational IT infrastructure, services, facilities..."*이며 *"do not need to cover novel research or developments"*다. **한강/KISTI-6 도입·운영 경험 자체가 이 트랙의 정확한 입구다.** SC23 *Frontier: Exploring Exascale*, SC24 Fugaku 인센티브, SC25 *Breaking the System Noise Barrier at Exascale*(El Capitan)이 형식 선례다.

**→ 권고: Technical Paper 트랙(C1 또는 C2)과 SotP 트랙(한강 운영 경험)을 병행하는 2트랙 전략.** 서로 다른 심사 기준을 쓰므로 경쟁하지 않고, SotP 논문이 Technical Paper의 데이터 자산과 신뢰도를 만들어 준다.

---

## 종합 한 줄

> **탐지는 닫혔고, 예측은 붐비고, RCA는 서브시스템에 갇혀 있고, 조치는 규칙 기반이며, 일반화는 아무도 측정한 적이 없고, telemetry 비용은 누구도 최적화한 적이 없다. 그리고 이 분야에서 아카이벌 논문을 내는 것은 큰 기계를 가진 센터가 아니라 대학 그룹을 결합시키고 데이터를 공개한 센터다.**

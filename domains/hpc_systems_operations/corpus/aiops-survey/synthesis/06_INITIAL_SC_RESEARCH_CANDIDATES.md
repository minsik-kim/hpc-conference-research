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

# 06. INITIAL SC RESEARCH CANDIDATES
## novelty falsification을 통과한 연구 후보

**작성일:** 2026-09-06
**전제:** 사용자는 대규모 HPC 시스템의 telemetry/monitoring architecture를 설계 중이며, 다음 계층을 고려한다 — Slurm · GPU/DCGM · CPU telemetry · HPE Slingshot fabric · Lustre · power · cooling/CDU · system logs. 장기 telemetry는 operations · RCA · performance analysis · user support · AIOps · research에 활용될 가능성이 있다.

**평가 척도 (1–5).** 점수보다 근거가 중요하다.
Operational importance · Research novelty potential · Generalizability · Data availability · Experimental feasibility · Publication potential

**최종 publication class.** `SC Technical Paper plausible` / `SC Technical Paper stretch` / `strong workshop paper` / `practitioner / state-of-practice` / `engineering report only`
**SC를 목표로 한다는 이유로 관대하게 평가하지 않았다.**

**`REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?`** — 위 계층으로 실제 검증 가능한지 별도 평가한다. 모든 후보를 이 시스템에 억지로 연결하지 않았다 — C7과 C9는 부분적으로만 연결된다.

---

# 요약표

| # | 후보 | 축 | 판정 근거 | Publication class | 재현성 |
|---|---|---|---|---|---|
| **C1** | Telemetry 축소의 탐지–진단 비대칭과 비용/품질 Pareto frontier | C(+A) | 세 감사가 독립적으로 1위. 새로운 과학적 주장 | **SC Technical Paper plausible** | ✅ 단, **지금부터 전해상도 보관 필요** |
| **C2** | 세대 간 telemetry 전이 손실의 분해 | B | 수치 telemetry에서 아무도 측정한 적 없음. KISTI의 구조적 우위 | **SC Technical Paper plausible** | ✅ 최고 |
| **C3** | Backfill 기반 silent-defect screening 정책 최적화 | G1 | ORNL이 ground truth와 negative baseline을 이미 공개 | **SC Technical Paper plausible** | ⚠️ 자체 screening 프로그램 운영 필요 |
| **C4** | HPC 운영 label의 semantics 측정 + 약한 label 모델 | E(+D) | 방법은 닫혔으나 label semantics는 미개척 | **SC Technical Paper stretch** (C5와 결합 시 plausible) | ✅ 티켓/RMA 접근 확보 시 |
| **C5** | 다중 테넌트에서 내재적 fail-slow vs 유발된 간섭 판별 | D(+A) | 좁지만 실재. ARGUS 전제가 깨지는 지점 | **SC Technical Paper stretch** | ✅ Slingshot counter 확보가 관건 |
| **C6** | Blast-radius 인지 remediation 비용 모델 + off-policy 평가 | F | 개념은 Narya가 닫음. 방법론이 진짜 gap | **SC Technical Paper stretch** (조건부) | ⚠️ Slurm 상태 이력의 *actor* 필드 필요 |
| **C7** | HPC 운영 agent 벤치마크 | G | 2026 서베이 2편이 명시적으로 지목한 부재 | **SC Technical Paper stretch** (artifact 가치 높음) | ⚠️ C4의 ground truth에 종속 |
| **C8** | job 비효율 리포팅이 사용자 행동을 바꾸는가 | G2 | 생태계 최대의 미수행 연구. 알고리즘 불필요 | **strong workshop paper** → 규모 확보 시 SC SotP | ✅ 가장 쉬움 |
| **C9** | 운영 정책 변경의 counterfactual 평가 방법론 | G10 | ExaDigiT가 물리를 풀었고 정책 방법론은 공백 | **SC Technical Paper stretch** | ⚠️ twin 구축 비용 큼 |
| **C10** | Telemetry integrity / observability debt 지표 | G17 | 벤더 telemetry 품질 벤치마크 자체가 없음 | **strong workshop paper** → C1과 결합 시 SC 구성요소 | ✅ 매우 높음 |

---

# C1. Telemetry 축소의 탐지–진단 비대칭 (최우선 권고)

> **연구 질문:** 이상 *탐지* 품질을 보존하는 telemetry 축소가 cross-layer *진단* 품질을 파괴하는가? 그리고 telemetry 비용 대 운영 품질의 Pareto frontier는 실제로 어떤 모양인가?

**Operational problem.** 센터는 telemetry 볼륨에 압도된다. ORNL은 데이터센터 전체에서 **4.2–4.5 TB/day**, STREAM Kafka 버스만 **1.3 TB/day, 300M msg/day**, 5년 **20 PB** 예상. 스트림 간 동적 범위가 **30만 배**(스토리지 3.3 TB/day vs resource manager 11 MB/day). HPE HPCM 1.13 기본 보존은 Kafka 1일 / OpenSearch 7일 / VictoriaMetrics 7일. 무엇을 버려도 되는지 아무도 모른다.

**Existing production practice.** 세 개의 무딘 레버뿐: ① 고정 샘플링 간격(5–10초, 가끔 1초), ② 저장 전 in-memory 사전집계(SuperMUC-NG: 70만 → 6만 insert/s, **~11.7배**), ③ 보존 thinning. **셋 다 엔지니어 판단으로 설정되며, 어떤 것도 측정된 하류 품질 제약에 묶여 있지 않다.** ORNL 자신의 축소 전략은 *"identifying data fields that either provide no useful information"* — 수동이다. EPCC ARCHER2는 반대 방향의 후회를 기록했다: *"Historical Graphite data granularity reduces over time to conserve disk space"* — downsampling이 장기 세밀 분석을 파괴했다.

**Closest research.**
- 네트워킹(닫힘): **Sonata** SIGCOMM'18(ILP query partition + dynamic refinement, 3–7 자릿수 감소), **PINT** SIGCOMM'20(패킷당 hard bit budget, 증명된 bound, 16 bit/packet이 full-INT 품질), **AutoSketch** NSDI'24.
- 클라우드(가장 위험): **SuperBench** ATC'24 Best Paper의 **Selector** — 검증 비용 대 탐지 이득을 명시 최적화, 10만+ GPU, 2년 배포.
- 트레이싱: **Hindsight** NSDI'23(retroactive sampling — 싸게 버퍼링하고 증상 발생 시에만 영속화).
- HPC 측 축소(전부 *모델링용* 차원 축소): NodeSentry **3,014→82**, Prodigy **806→156**, Tuncer **−57%**, Reveal ~700→60 채널.
- KPI 선택: **fKPISelect** ISSRE'23(fault-injection 기반 자동 KPI 선택) — 과소평가된 선행. 반드시 인용.

**Why existing approaches are insufficient.**
Sonata/PINT의 효용 함수는 *프로그래머블 데이터플레인 위 해석적 의미론의 선언적 query*다. HPC 운영 telemetry에는 셋 다 없다 — 고정 schema 주기 counter, 프로그래머블 수집 기질 없음, 효용은 **닫힌 형태가 없는 학습된 탐지기**. 비용 구조도 다르다: 스위치 메모리/패킷당 비트 vs **수집기 CPU + 네트워크 + 다PB 장기 보존**. SuperBench는 *능동 벤치마크 스케줄링*(비용 = 훔친 GPU 시간)이지 수동 telemetry(비용 = 바이트)가 아니다.
그리고 결정적으로: **NodeSentry는 모델이 소비하는 것을 줄였을 뿐, 시스템이 수집·전송·저장하는 것을 줄이지 않았다.** 3,014개 metric은 여전히 전부 수집·전송·저장된다. **수집을 멈춰도 된다는 것을 보인 사람이 없다.**

**Hypothesis (검증 가능, 어느 쪽이든 발표 가능).**
> **H1 (비대칭).** 탐지 F1을 τ 이상으로 유지하는 최소 telemetry 구성 S_det와, RCA top-k localization을 ρ 이상으로 유지하는 최소 구성 S_rca에 대해 **S_det ⊊ S_rca**이며, |S_rca| / |S_det| ≫ 1이다. 즉 탐지는 싸고 진단은 비싸다.
> **H2 (지연).** 탐지 F1은 샘플링 간격에 대해 완만하게, **탐지 지연은 급격하게** 저하한다. 따라서 F1만 보고하는 기존 축소 결과는 운영 관점에서 오도한다.
> **H3 (계층별 비대칭).** 계층별 바이트당 진단 가치가 크게 다르며, 특히 **fabric counter는 수집 비용이 측정 가능하게 비싸고**(Slingshot: 포트당 1,000개 이상, 스위치당 64K, `dump_counters` **약 0.5초/스위치**) 그에 걸맞은 진단 가치를 갖는지가 미검증이다.

**Required data.** 한강급 시스템에서 **≥6개월의 전해상도 다계층 trace**. Slurm accounting ✅ · DCGM ✅(**DCGM field-group 선택 자체가 비용 레버 — 연구 대상**) · CPU/메모리 ✅ · Lustre client+server jobstats ✅ · power ✅ · CDU ✅ · syslog/RAS ✅ · **Slingshot fabric counter가 핵심 위험이자 차별점**.
> ⚠️ **최우선 실행 항목: 지금부터 전해상도 보관을 시작할 것.** 이미 downsample된 데이터로는 downsampling을 소급 연구할 수 없다. 이것이 이 후보의 유일한 hard dependency이며, 지금 결정하지 않으면 2년을 잃는다.

**Baselines.** 균일 시간 downsampling · **Gorilla/delta-of-delta 무손실 압축**(PVLDB'15) · 상관 pruning(NodeSentry 방식) · PCA · 랜덤 부분집합 · mutual-information greedy · **Sonata 방식 dynamic refinement 이식**(네트워킹 reviewer가 요구한다) · fKPISelect.

**Metrics.** 수집·저장 **바이트/노드/일** · **측정된** 수집기 CPU/메모리/네트워크 오버헤드 · **애플리케이션 교란 측정**(이것이 이 논문을 *HPC* 논문으로 만든다) · 탐지 F1 · **탐지 지연 분포** · **RCA/localization top-k** · 센터 규모에서의 PB/년 또는 비용. **Pareto frontier 플롯**과 계층별 민감도 ablation.

**Required scale.** production 시스템 **≥2대**, 각 **≥6개월 전해상도**. **replay만으로는 부족하다** — 비용 주장에는 실제 온라인 배포에서 수집기 오버헤드를 측정해야 한다.

**Generalizability.** 정식화(비용 제약 하 하류 품질 최대화)와 비대칭 결과는 시스템 독립적이다. 구체적 Pareto frontier는 시스템 의존적이며, 그 점 자체가 C2로 연결된다.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 예, 세 후보 중 가장 자족적이다 — 운영자 label 의존성이 없다.** 단, 전해상도 아카이빙이 전제.

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 모든 센터가 겪고, 한강 아키텍처 결정에 직결. 20 PB/5년이 실제 숫자 |
| Research novelty potential | **4** | 정식화는 네트워킹에서 왔으나 **탐지–진단 비대칭은 HPC·클라우드·네트워킹 어디에서도 검증된 적 없음** |
| Generalizability | **4** | 방법론과 비대칭 결과는 이식됨 |
| Data availability | **4** | 자체 시스템 + M100 ExaData(1초 573 metric, 934일)로 decimation 실험 가능 |
| Experimental feasibility | **4** | replay는 쉬움. 온라인 오버헤드 측정과 전해상도 보관이 비용 |
| Publication potential | **4** | 메커니즘 + 측정으로 프레이밍하면 통과. 압축 파이프라인으로 프레이밍하면 실패 |

**SC regular potential:** **SC Technical Paper plausible.**

**최강 반론:** *"Telemetry-cost-under-accuracy-constraint was formalized and solved in networking — Sonata, PINT, AutoSketch — with formal bounds this paper does not provide. On the HPC side, metric reduction is routine: NodeSentry already cut 3,014 metrics to 82 with no accuracy loss. This is feature selection with a cost label attached."*
**대응:** (i) 목적·제약·해 구조가 다르다(위 참조). (ii) NodeSentry는 소비를 줄였지 수집을 줄이지 않았다. (iii) **비대칭이 참이면 기존 축소 문헌 전체가 틀린 질문에 답한 것이다.** — **(iii)으로 시작할 것.** 셋 중 유일하게 범위 논증이 아니라 새로운 과학적 주장이다.

---

# C2. 세대 간 telemetry 전이 손실의 분해

> **연구 질문:** 수치 HPC telemetry로 학습한 운영 모델은 사이트·GPU 세대·fabric 세대·스케줄러 정책·telemetry schema를 건널 때 얼마나 잃는가? 그리고 그 손실은 어떤 shift에서 오는가?

**Operational problem.** 센터는 5–7년마다 시스템을 교체하고, 그때마다 모델과 대시보드를 처음부터 다시 만든다. ORNL: *"Challenge of achieving immediate data availability in the face of the relatively short lifespan of supercomputers"* — *"knowledge accumulation across generations to minimize re-work"*가 필요하다. ORNL HPCSYSPROS: *"If the telemetry data schema changes, dashboards must be recreated using different sources, query languages, and metric names."* LRZ: *"a block template is not guaranteed to be portable across HPC systems with different sensor hierarchies."*

**Existing production practice.** **없다.** Netti et al.이 센터들이 *"insular ODA solutions"*를 돌린다고 못박고, future work로 *"develop portable, shareable ML models across institutions"*를 든다. Bartolini 그룹은 **per-node 모델**(RUAD)과 노드 간 federated learning을 쓴다 — 한 시스템 *안에서도* 단일 모델이 안 맞는다는 최강 증거. HPC ODA Commons(PEARC'26)는 데이터 *계약*이지 이전 가능한 모델이 아니다.

**Closest research.** 텍스트 로그는 **닫혔다**(MetaLog ICSE'24, CroSysLog F1 97.6–99.2%, ZeroLog ISSRE'25, LogTAD). 방법론은 SE venue가 소유(TOSEM data-splitting·model-update, EMSE model-reuse, drift 적응). 하드웨어는 **DSN'24(Huawei) *Investigating Memory Failure Prediction Across CPU Architectures*** — 직격탄. **SeT-Diff**(CF'26)는 이 문제를 동기로 명시하고 cross-system 평가를 하지 않는다. **CENTILE**(arXiv 2608.01725)은 telemetry foundation model로 도메인 간 전이를 주장하며 의사결정 품질로 평가한다.

**Why existing approaches are insufficient.** 전부 로그 또는 클라우드 KPI다. **수치 HPC telemetry의 전이 손실을 측정한 연구가 존재하지 않는다.** 유일한 측정치는 AI4Sys'23 3쪽 워크숍 논문의 **F1 0.898(node-specific) → 0.726(generic)** — 이것도 *같은 시스템의 노드 간*이다. 그리고 HPC에는 클라우드에 없는 shift가 있다: **counter schema가 함께 바뀌는 하드웨어 세대 shift**(V100 DCGM 필드 ≠ H100 DCGM 필드; Aries counter ≠ Slingshot counter). 이는 모든 domain adaptation 방법이 전제하는 "같은 feature space, 다른 분포"를 깨뜨린다.

**Hypothesis.**
> **H1.** 전이 손실은 크며(ΔF1 ≥ 0.15 예상), 손실의 지배적 성분은 workload mix가 아니라 **schema shift + 하드웨어 세대 shift**다.
> **H2.** raw counter는 이전되지 않지만 **무차원 파생량**(utilization ratio, bytes/flop, stall fraction, power/TDP, capacity 정규화 queue depth)은 이전된다.
> **H3.** N=1-per-generation 영역(각 세대의 기계가 한 대뿐)에서는 표준 domain adaptation 가정이 깨지며, 표본 효율 곡선이 정식 DA 방법과 단순 fine-tuning 사이에서 예상과 다르게 나타난다.

**Required data.** **≥3개, 이상적으로 ≥4개 시스템, ≥2개 하드웨어 세대, ≥2개 인터커넥트 계열.** 각 **≥3개월**, **시간순 분할**(랜덤 분할 금지 — TOSEM data-splitting 논문을 아는 reviewer가 이것만으로 논문을 죽인다).
KISTI 조합: **Nurion(KNL/OPA) + 한강(H100급/Slingshot) + M100 ExaData(V100/IB-HDR, 공개) + F-DATA(A64FX/Tofu-D, 공개)** → **4–5개 시스템, 무료로.** Eclipse trace를 얻을 수 있으면 5개.
> **구세대 fabric에 Slingshot counter의 대응물이 없다는 것은 문제가 아니라 연구 대상이다** — 그것이 바로 연구하려는 schema shift다.

**Baselines.** target에서 from-scratch 학습 · fine-tuning · **MAML(CroSysLog/MetaLog를 수치로 이식)** · domain-adversarial(LogTAD 방식) · foundation-model baseline(**SeT-Diff 및/또는 CENTILE**) · 자명한 **per-node 모델**(RUAD).

**Metrics.** ΔF1 · **표본 효율 곡선**(target 표본 수 → 복구) · 탐지 지연 shift · calibration drift · **재학습 비용을 GPU-시간으로**. 그리고 손실을 하드웨어 / schema / workload / 정책으로 귀속하는 **분해 실험**.

**Required scale.** 시스템 3–5대. **2대는 부족하다** — reviewer가 "n=2 is an anecdote"라고 말한다.

**Generalizability.** 분해 방법론과 invariant-representation 결과는 정의상 일반화된다. 이것이 이 후보가 데이터셋 논문이 아니라 메커니즘 논문이 되는 이유다.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 예, 세 축 중 최고.** KISTI는 **사내에 진짜 cross-generation 쌍을 보유**하며, 공개 데이터셋 2종을 무료로 추가할 수 있다. **이것이 경쟁 그룹이 발표하지 못한 구조적 우위다.**

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 시스템 교체마다 반복되는 비용. 여러 센터가 독립적으로 지목 |
| Research novelty potential | **4** | 수치 telemetry 전이 손실 측정이 0편. 단, SE 문헌이 방법론을 소유 |
| Generalizability | **5** | 분해 자체가 기여 |
| Data availability | **5** | 사내 2세대 + 공개 2종 |
| Experimental feasibility | **4** | 데이터는 있으나 schema 정렬 노동이 크다 |
| Publication potential | **4** | 하드웨어 세대 + schema shift로 시작하면 통과. 측정 논문으로 읽힐 위험 |

**SC regular potential:** **SC Technical Paper plausible.** 단, "데이터셋/측정 논문"으로 읽힐 위험이 가장 크다 — **분해 실험과 invariant-representation 결과로 완화할 것.**

**최강 반론:** *"Cross-system generalization, concept drift, model-update strategy and model-selection for AIOps are a mature body of work in TOSEM/EMSE/ICSE, and cross-system anomaly detection specifically has been solved with meta-learning at ICSE'24. This paper transfers a known technique to a new modality."*
**대응:** **하드웨어 세대 + schema shift로 시작할 것.** SE 문헌이 구조적으로 가질 수 없는 유일한 카드다. DSN'24 Huawei 논문은 반드시 인용·차별화(그쪽은 CPU 아키텍처, 이쪽은 accelerator/fabric 세대 + schema 변경).

---

# C3. Backfill 기반 silent-defect screening 정책 최적화

> **연구 질문:** 남는 backfill 용량 위에서 어떤 노드 수준 테스트를, 얼마나 오래, 어떤 cadence로 실행해야 node-hour당 발견 결함 수가 최대가 되는가?

**Operational problem.** exascale 규모에서 소수의 노드가 조용히 결함 상태다. ORNL Frontier: 9,408 노드, 37,632 MI250X, 15만+ 노드 수준 컴포넌트, MTBF가 *시간* 단위.

**Existing production practice (정량 근거가 이례적으로 풍부).** ORNL이 세 전략을 발표했다: 표적 leadership 규모 LAMMPS 실패 격리, 단계별 HACC job 완료 연구, **Slurm backfill을 통한 주기적 단일 노드 스크리닝**.
- 누적 **약 600만** 단일 노드 테스트, 2023-10~2024-04 창에 **190만**
- **고유 실패 노드 99개** — 소프트웨어 버그 54, transient performance 27, GPU HBM UE 12, 수치 불안정 11, 재현 불가 4
- backfill LAMMPS **14,618 테스트당 1건** 실패 검출
- 244건 LAMMPS job → **결함 하드웨어 19건 식별·수리**
- 4,096 노드 / 500 W TDP에서 **50건 중 17건 실패**; HBM +100 mV & 기본 메모리 클록에서 **50건 중 11건**
- **Phase 2 → Phase 4에서 power fault 75% 감소**
- **negative result:** 주간 `checknode` 스크린이 6개월간 **39,437회 무수확** → 2023-12 production에서 제거(테스트 시간이 너무 짧았다 — 1분 미만 vs backfill LAMMPS 24분). epilog 변형은 *"too disruptive to user workloads"*

**Closest research.** 신뢰성 *특성화*만 있다 — Ostrouchov SC20(Titan GPU survival analysis), Nie DSN'18(GPU error prediction). **screening-policy 최적화 / backfill 하 테스트 스케줄링에 대한 가까운 아카이벌 연구를 찾지 못했다.** 인접: SuperBench ATC'24의 Selector(검증 스케줄링 최적화, 그러나 클라우드·전용 검증 창).

**Why existing approaches are insufficient.** ORNL은 결과를 발표했지 **정책을 최적화하지 않았다.** 테스트 선택도 cadence도 duration도 운영 경험으로 정해졌고, 실패한 정책(주간 스크린)은 사후에 폐기되었다. 1/14,618이라는 검출률에서 이것은 명백히 순차 실험 설계 문제다.

**Hypothesis.**
> 결함 발견율을 테스트 종류 × 지속시간 × 노드 이력의 함수로 모델링하면, 동일 node-hour 예산에서 **현행 균일 스크리닝 대비 결함 발견 수를 유의하게 늘리는 적응적 정책**이 존재한다. 특히 (i) 노드별 사전 위험(과거 실패, 열 이력, 가동 시간)으로 우선순위를 매기고, (ii) 테스트 지속시간을 검출력 곡선에 맞춰 배분하면, 39,437회 무수확 같은 사건이 사전에 예측 가능하다.

**Required data.** 자체 screening 프로그램의 테스트 결과 로그(테스트 종류·노드·지속시간·통과/실패), 노드 수리 기록/RMA, Slurm backfill 가용 용량 이력, 노드 telemetry(열·전력·오류).

**Baselines.** ORNL의 발표된 정책(균일 backfill 스크리닝)과 **폐기된 주간 스크린**(negative baseline으로 사용 — 이것이 이 후보의 특별한 강점이다) · 랜덤 스케줄링 · 사전 위험 없는 greedy · SuperBench Selector 이식.

**Metrics.** node-hour당 발견 결함 · 결함 발생부터 검출까지 지연 · 무수확 테스트 비율 · 오탐(transient performance)으로 인한 불필요 조치 비용 · 사용자 워크로드 교란(ORNL이 epilog 변형을 폐기한 이유).

**Required scale.** production 시스템 1대, ≥6개월 스크리닝 운영. ORNL 데이터가 공개된 비교 기준선을 제공한다.

**Generalizability.** 순차 실험 설계 정식화는 시스템 독립적이며, 검출률·테스트 비용만 파라미터로 바뀐다.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **⚠️ 부분.** telemetry는 충분하지만 **자체 screening 프로그램을 운영해야 데이터가 생긴다.** 즉 이것은 데이터 분석 과제가 아니라 **운영 프로그램 설계 과제**다. 한강 초기 운영에 이를 설계해 넣으면 2년 뒤 논문이 된다.

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 수리 자원과 가용성에 직결 |
| Research novelty potential | **4** | 가까운 아카이벌 연구 없음. 단, SuperBench Selector와의 차별화 필요 |
| Generalizability | **4** | 정식화가 이식됨 |
| Data availability | **3** | 자체 생성 필요. ORNL 공개 수치가 baseline |
| Experimental feasibility | **3** | 운영 프로그램 구축과 6개월 이상의 대기 |
| Publication potential | **4** | negative baseline이 공개되어 있다는 것이 큰 이점 |

**SC regular potential:** **SC Technical Paper plausible.** CUG 조사에서 "가장 SC 논문 형태에 가까운 gap"으로 독립 지목되었다.

**최강 반론:** *"SuperBench (ATC'24) already optimizes validation scheduling under a cost budget at 100k-GPU scale. This is that, on a smaller machine."*
**대응:** SuperBench는 **전용 검증 창**에서 GPU 시간을 훔친다. 이쪽은 **다른 사용자의 job 사이에 남는 backfill 용량**이라는 전혀 다른 자원 모델이며, 사용자 워크로드 교란이 1급 제약이다(ORNL이 epilog 변형을 폐기한 이유). 또한 검출률이 1/14,618로 SuperBench 영역보다 훨씬 희소하다.

---

# C4. HPC 운영 label의 semantics 측정 + 다중 소스 약한 label 모델

> **연구 질문:** HPC 운영에서 "label"이란 무엇이며, 우리가 가진 label들은 얼마나 틀렸는가?

**Operational problem.** anomaly/failure label이 없다. 있는 것은 서로 불일치하는 대리 지표들뿐이다.

**Existing production practice.** Nagios/Zabbix/Prometheus 알림 + Slurm drain reason + 티켓 시스템(RT/ServiceNow)이 **서로 연결되지 않은 4개 소스**로 돌아간다. Frontier `checknode`가 실패한 검사 이름을 Slurm drain reason에 쓰는 것이 사실상 가장 가까운 production label 파이프라인이며, **아무도 이를 labeling method로 발표한 적이 없다.**

**Closest research.** 학습 방법은 **닫혔다**: partial label(ISSRE'21), PU learning(PUTraceAD ISSRE'22), label-free 배포(AutoKAD ISSRE'23), active learning(AFALog ISSRE'23, LogCAE ISSRE'24, **ALBADross Cluster'22 — 28배 절감**), LabelEase(ISSRE'24), ZeroLog(ISSRE'25), fault injection as label generator(Campos ISSRE'20/'23, fKPISelect ISSRE'23).
평가 비판: **Kim et al. AAAI'22** — point-adjustment 프로토콜이 F1을 부풀려 **랜덤 점수 탐지기가 SOTA를 이긴다**. 그리고 **ISSRE'24 *Can We Trust Auto-Mitigation?***가 closed-loop 배포가 ground-truth label을 파괴하는 문제를 다룬다.

**Why existing approaches are insufficient.** 방법이 아니라 **label 의미론**이 문제다. **실제 슈퍼컴퓨터에서 이 소스들의 일치도를 정량화하거나, 불일치가 하류 모델 품질을 얼마나 파괴하는지 측정한 연구가 없다.** M100 ExaData 논문 자신이 Nagios 약한 label 위에서 **AUC 0.57**을 보고한 것이 이 축이 실재한다는 최고의 인용 가능한 증거다.

**Hypothesis.**
> **H1.** 약한 label 소스 간 pairwise 일치도는 낮으며(Cohen's κ < 0.4 예상), 특히 *계획된* drain과 *비계획* drain을 분리하지 않으면 label 잡음의 지배적 성분이 된다.
> **H2.** 명시적 잡음 모델(소스별 precision, 일치/불일치 구조)로 소스를 융합하면 단일 oracle(Nagios AUC 0.57) 대비 유의한 개선이 나온다.
> **H3.** RMA 기록을 **지연된 고정밀 label**로 쓰면 잡음 소스들의 precision을 부트스트랩할 수 있다.

**Required data.** Slurm `sacct`/노드 상태 이력(**이유와 actor 포함**) · syslog/RAS · DCGM XID + ECC · 티켓 시스템 export · 유지보수/RMA 기록 · C5 축의 telemetry. 결합 키는 (node, time-window).
> **행정적 접근권이 핵심 자산이다.** 티켓 export와 RMA 기록은 국가센터가 가지고 대학 그룹이 못 가지는 것이다.

**Baselines.** 단일 소스 Nagios/drain-reason label(**M100의 AUC 0.57 설정을 재현하고 이기기**) · 완전 비지도(Prodigy, RUAD) · 소규모 gold set 위 완전 지도.

**Metrics.** 소스 간 일치도(κ, F1) · **고정 alert budget 하** 성능 · **티켓 타임스탬프 대비 탐지까지의 시간** · **알림이 선행한 티켓의 비율** · point-adjusted와 non-point-adjusted **양쪽 보고**(Kim et al. 인용 필수) · 운영자 판정 표본 + **inter-rater agreement**.

**Required scale.** ≥1년 telemetry, 운영자 판정 gold set(≥50–100건).

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 예 — 단, 티켓/RMA 접근권 확보가 전제.** 이것이 hard dependency다.

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 모든 하류 ML의 전제조건 |
| Research novelty potential | **3** | 약한 지도 자체는 표준 장비. **측정으로 재프레이밍해야만** 성립 |
| Generalizability | **4** | 프로토콜과 gold set이 재사용됨 |
| Data availability | **4** | 행정 접근권만 확보되면 높음 |
| Experimental feasibility | **4** | 노동집약적이나 위험 낮음 |
| Publication potential | **3** | 단독으로는 stretch. C5와 결합하면 plausible |

**SC regular potential:** **SC Technical Paper stretch** — **C5와 결합하면 plausible.**

**최강 반론:** *"Weak supervision is a solved ML technique; applying it to HPC labels is engineering, and the evaluation critique (Kim et al. AAAI'22) is not yours."*
**대응:** HPC 운영 label의 *구조*가 다르다 — 지연된 RMA ground truth, 계획-비계획 confound, 이진이 아닌 원인 클래스 label, 노드 단위 vs job 단위 입도 불일치. 그리고 응용이 아니라 **재사용 가능한 프로토콜 + 공개된 gold set**.

---

# C5. 다중 테넌트에서 내재적 fail-slow vs 유발된 간섭 판별

> **연구 질문:** 느려진 job에 대해, 원인이 그 노드 자신의 하드웨어인가 아니면 공동 스케줄된 이웃 job이 공유 자원을 포화시킨 것인가를 구분할 수 있는가?

**Operational problem.** 노드가 느리다는 것은 안다. **왜** 느린지 모른다. ORNL이 명시적으로 지목: 같은 에러 메시지가 *"either defective hardware or an application code bug"*에서 나온다. *"Discovering trends in failures is one of the most important yet most difficult tasks."*

**Existing production practice.** **Frontier `checknode`** — 결정적 임계값 검사, 자동 drain, **ML 0, "어느 검사가 실패했나" 이상의 원인 판별 0.** root cause는 사람이 티켓을 연다. **LBNL NHC**가 커뮤니티 표준, 동일 성격.

**Closest research (위험도 높음).**
- **Tuncer et al. TPDS 2019** — HPC 성능 anomaly의 *유형*(network contention / CPU contention / memory bandwidth / orphan process)을 노드 telemetry에서 지도 분류. **7년 전에 이 축을 HPC에서 이미 했다. 인용하고 이기지 못하면 심사를 통과하지 못한다.**
- **ARGUS** — >1만 GPU, 6개월 상시, <2% overhead, 다중 원인 판별. **하지만 동기적·반복적·동질적 학습 job을 전제한다.**
- **FALCON**(L7/D5, 60.1% 저하 감소), **LLMPrism**(네트워크 flow만으로 학습 timeline 재구성).
- **Perseus** FAST'23, **IASO** ATC'19 — 장치 수준 fail-slow는 production-solved. **"peer와 비교한다"는 기여가 될 수 없다.**
- **IPDPS'26** (Wei, Pradeep, Bhatele) — Perlmutter + Frontier, 761 runs, 8,118 node-hours. **네트워크 혼잡이 변동성을 지배하고 개별 GPU 성능은 안정적**이라고 이미 측정. 저자들이 **Rosetta 스위치 counter를 얻지 못했다고 명시**한다.

**Why existing approaches are insufficient.** Tuncer는 contention을 *label 클래스*로 다루지, contention을 **특정 이웃 job에 귀속**하지 않는다. Perseus/IASO의 peer 비교는 peer가 동일 워크로드를 돌릴 때만 유효한데 **HPC 배치 시스템에서는 그 가정이 깨진다.** ARGUS의 iteration 주기성 가정도 이기종 배치 job에서 깨진다.

**Hypothesis.**
> 동시 실행 job 지도(Slurm accounting을 공유 스위치/OST로 조인)를 조건화하면, {GPU 저하, CPU throttle, NIC/링크 저하, 이웃 job의 fabric 혼잡, Lustre 경합, placement/topology, 애플리케이션 내재}에 대한 순위 귀속이 운영자 확인 ground truth 대비 유의한 top-1/top-3 정확도를 달성한다. **그리고 스케줄러 배치를 조건화하지 않으면 이 정확도가 크게 떨어진다**(= placement가 confounder라는 실증).

**Required data.** GPU → DCGM(SM clock, `DCGM_FI_DEV_*_THROTTLE`, ECC, XID, power) · CPU → 코어별 주파수/온도/RAPL, thermal throttle flag · **네트워크 → Slingshot fabric counter**(포트별 stall/flit, congestion control 상태, 링크 재훈련, degraded-lane 이벤트; Aries에서 stall-to-flit ratio가 확립된 지표이므로 Slingshot 대응물이 명백한 출발점) · I/O → Lustre `llite`/OST + Darshan · topology → Slurm hostlist → dragonfly group 매핑 · 간섭 → Slurm accounting을 공유 스위치/OST로 조인한 동시 job 지도 · 환경 → CDU 흡입 온도, 랙 전력. **label은 C4의 RAS/syslog + 티켓 + 유지보수 기록 조인** — 그 조인 자체가 기여다.

**Baselines.** NodeSentry(SC'25) · Prodigy(SC'23) · RUAD · E2EWatch/ALBADross · **Tuncer TPDS'19(필수)** · 클라우드 fail-slow 1종(Perseus 또는 FALCON — HPC 밖 reviewer가 요구한다).

**Metrics.** **원인 클래스별** precision/recall(집계 F1이 아니라) · top-k localization · **lead time** · false-drain rate · 탐지 지연. **고정 alert budget 하 보고**(point-adjusted F1이 부풀려진다는 것을 reviewer들이 이제 안다). 어느 telemetry 채널이 어느 원인 신호를 담는지에 대한 ablation.

**Required scale.** production 시스템 ≥1대, ≥1,000 노드, **≥6개월** telemetry. **주입이 아닌 운영자 확인 label** — 이것이 BU/Sandia 계열 대비 가장 날카로운 차별점이다. SC'25가 1주짜리를 받아줬지만, ARGUS의 6개월과 경쟁하는 2027년 논문은 1주로 살아남지 못한다.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 예 — 단 두 가지 조건.** (i) **Slingshot fabric counter 확보**(HPE STT / fabric manager). Bhatele 그룹이 Perlmutter/Frontier에서 Rosetta 스위치 counter를 못 얻었다는 점을 감안하면, **KISTI가 이를 확보하면 그 자체가 최강 경쟁 그룹 대비 차별점이다.** (ii) **운영자 확인 incident label**(C4). 진짜 병목은 telemetry가 아니라 label이다.

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 매일 발생하고 매일 사람이 처리한다 |
| Research novelty potential | **3** | 좁다. Tuncer TPDS'19와 ARGUS가 양쪽에서 압박 |
| Generalizability | **3** | 원인 taxonomy가 시스템 의존적 |
| Data availability | **4** | telemetry는 충분, label이 관건 |
| Experimental feasibility | **3** | 6개월 + 운영자 labeling 약속 필요 |
| Publication potential | **3** | 간섭-내재 구분으로 좁히면 stretch, 넓히면 파생적 |

**SC regular potential:** **SC Technical Paper stretch.** **"우리는 느린 노드를 탐지한다"를 제출하지 말 것. "우리는 느림을 *계층에* 그리고 *책임 있는 공동 테넌트에* 귀속하고, 통제된 주입으로 그 귀속을 검증한다"를 제출할 것.**

**최강 반론:** *"ARGUS already does always-on multi-cause fail-slow diagnosis at 10,000-GPU production scale with six months of deployment, and Kaleidoscope did PGM-based cause discrimination with 843 real labels at SC'20. Tuncer et al. classified HPC anomaly types in TPDS 2019. What is new?"*
**대응:** ARGUS가 구조적으로 만들 수 없는 원인 클래스(cross-job 간섭, topology/placement, Lustre, cooling/power) + ARGUS 전제가 깨지는 **이기종 배치 job** 평가 + Tuncer가 하지 않은 **특정 이웃 job으로의 귀속**.

---

# C6. Blast-radius 인지 remediation 비용 모델 + off-policy 평가

> **연구 질문:** production Tier-0에서 drain 정책을 A/B 테스트할 수 없을 때, remediation 정책을 어떻게 평가하는가? 그리고 노드를 drain하는 진짜 비용은 무엇인가?

**Operational problem.** 예측/탐지 후 조치(drain, reroute, reschedule, restart, migration, 설정 변경)로 넘어갈 때 안전성·확신도·rollback 문제가 발생한다. HPC에서는 오조치가 되돌릴 수 없다 — 노드 하나를 drain하면 4,000 노드 job이 죽는다.

**Existing production practice.** `checknode`(ORNL Frontier)와 LBNL NHC. 둘 다 결정적 검사 → drain. **confidence 없음, 비용 모델 없음, rollback 없음, 수리 검증 자동화 없음.** `checknode`의 유일한 진짜 안전 아이디어: **자신이 설정한 drain reason일 때만 자동 resume**(사람이 설정한 drain은 보존). 사후 "node screen"과 partner-node drain은 **수동**으로 남아 있고, 저자들이 partner-node drain 자동화를 future work로 명시한다.

**Closest research.** **Narya OSDI'20**(15개월 production, VM 중단 26% 감소, bandit/RL 온라인 실험) · **FALCON**(>1만 GPU, 사람 개입 없는 다단계 완화) · **SuperBench**(검증→격리→수리) · **Perseus**(탐지→격리, p99.99 48% 감소) · HPC 계보 SC'08 → JPDC'12 → **HPDC'20 Behera et al.**(순수 SimPy 시뮬레이션, 예측 정확도를 *가정*).

**Why existing approaches are insufficient.** 클라우드 조치 공간은 **싸고 되돌릴 수 있어서** bandit/RL 탐색이 윤리적으로 가능하다. **HPC 조치 공간은 그렇지 않다.** 그리고 **배치 스케줄·할당 회계·체크포인트 의존 환경에서의 조치 비용 모델을 가진 발표된 연구가 없고, D5에 도달한 HPC 시스템이 실증된 적이 없다.** 18년 된 HPC proactive-migration 계보는 production에 도달한 적이 없다.

**Hypothesis.**
> **H1.** 노드 n을 drain하는 비용은 상수가 아니라 (올라간 job, 경과 시간, 체크포인트 신선도, 큐 압력)의 함수이며, 이를 모델링한 정책이 고정 정책 대비 동일 안전성에서 유의하게 적은 node-hour를 잃는다.
> **H2.** false drain과 missed failure의 **비대칭 비용**에서 confidence 임계값을 *유도*할 수 있으며, 튜닝된 임계값보다 낫다.
> **H3.** Slurm 노드 상태 이력 + job 결과로부터 remediation 정책의 **off-policy 평가**가 가능하며, 그 추정치가 shadow-mode 실측과 신뢰구간 내에서 일치한다.

**Required data.** **이유와 actor를 포함한 완전한 Slurm 노드 상태 전이 이력** · job 결과 기록 · 가능하면 체크포인트 메타데이터 · C5 축의 telemetry.
> ⚠️ **결정적 전제:** **actor 필드**(사람 / 자동화 / epilog 중 누가 상태를 설정했는가). 이 컬럼이 없으면 off-policy 평가가 불가능하고 **이 후보는 성립하지 않는다.** 한강 설계 단계에서 이 필드를 반드시 기록하도록 할 것 — 나중에 소급 생성할 수 없다.

**Baselines.** 센터의 기존 규칙 기반 NHC/checknode 정책(**strawman이 아니라 실제 정책**) · 고정 임계값 · Narya 이식 · FALCON 이식.

**Metrics.** 불필요 drain으로 잃은 node-hour vs 회피된 job 실패로 절감된 node-hour(**양쪽 측정**) · **false-drain rate**와 **false-return rate**를 1급 지표로 · 신뢰구간 포함 off-policy 추정치 · 에이전트가 틀렸는데 guard가 잡은 사례 1건 이상 제시.

**Required scale.** 실제 시스템에서 실제 조치를 취하거나, **≥1년 노드 상태 + job 결과 이력에 대한 방어 가능한 off-policy 평가.**

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **⚠️ 조건부.** actor 필드가 있어야 한다. 없으면 불가.

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 가용성에 직결 |
| Research novelty potential | **4** | 과학적 gap은 가장 넓다(18년간 production 미도달) |
| Generalizability | **4** | 비용 모델과 off-policy 방법론이 이식됨 |
| Data availability | **3** | actor 필드 의존 |
| Experimental feasibility | **2** | **가장 낮다.** 평가 자체가 문제. 시뮬레이션은 HPDC'20이 이미 점유 |
| Publication potential | **3** | 의사결정 이론이 기여여야 함. 배관이면 HPCSYSPROS/CUG 논문 |

**SC regular potential:** **SC Technical Paper stretch (조건부).** (a) production 기계에서 실제 자동 조치를 취할 권한이 있거나 (b) off-policy 평가가 가능한 1년치 노드 상태 이력이 있을 때만 착수할 것. **둘 다 없으면 F를 독립 논문으로 만들지 말고 C5/C4의 "진단이 무엇을 가능하게 하는가" 절로 접을 것.**

**최강 반론:** *"Narya solved adaptive mitigation with online experimentation in production in 2020; FALCON does automatic multi-level straggler mitigation on 10k GPUs; Frontier already auto-drains. The HPC-specific delta is a cost model, which is engineering."*
**대응:** **off-policy 평가 방법론**(Tier-0에서 온라인 실험을 할 수 없다 — Narya는 Azure에서 할 수 있었다. 변명이 아니라 방법론적 차이다) + **job 수준 blast radius**(클라우드 등가물 없음). **"왜 이것이 조치 집합만 다른 Narya가 아닌가"를 related work가 아니라 서론에서 답할 것.**
추가 위험: **arXiv 2607.20005 *Safe Remediation as Risk-Constrained Intervention Decision***가 이 프레이밍을 선점했을 수 있다. **확보해서 읽기 전에 F 기반 제안서를 확정하지 말 것.**

---

# C7. HPC 운영 agent 벤치마크

> **연구 질문:** LLM/agent가 실제 HPC 운영 인시던트를 진단할 수 있는가 — 그리고 그것을 측정할 방법이 존재하는가?

**Operational problem.** 인시던트 진단이 사람의 시간을 지배한다. L4(FSE'25)가 유사 환경에서 **평균 진단 시간 34.7시간, 41.9%가 24시간 초과**를 측정했다.

**Existing production practice.** HPC에는 사실상 없다. 2026년 서베이 2편이 독립적으로 **HPC 운영에 문서화된 LLM production 배포 0건**, 조사된 10개 production ODA 프레임워크에 **LLM 통합 0**이라고 보고한다. 가장 가까운 실제 배포 HPC 산출물은 **FRAGATA**(CESGA, 20년치 RT 티켓 hybrid RAG) — 스페인 지역 학회이고 **정량 평가가 없다**(저자 자인). ORNL **EPIC**(Frontier 50만 job 로그, 배포된 챗봇, 서술적 분석에서 26% 정확도 향상, LLM 비용 19배 절감)이 유일한 배포 LLM 운영자 인터페이스이며 **RCA를 하지 않는다**(routing F1 0.77, hallucination 0.33).

**Closest research.** 클라우드는 포화: RCACopilot(EuroSys'24, 30팀 4년+, Micro-F1 0.766, **Macro-F1 0.533**), Ahmed(ICSE'23, 4만+ 인시던트), LLM incident triage(ISSRE'24), AetherLog(ISSRE'25). 벤치마크: **ITBench**(94 시나리오, **SRE 13.8% / CISO 25.2% / FinOps 0%**), **AIOpsLab**, OpsEval(FSE'25), RCAEval, OpenRCA.
**핵심 경고: *How Far Can RCA Go***(arXiv 2607.13548) — 실제 telemetry에서 최고 구조화 multi-agent RCA가 **25.71%**, **고전 causal discovery 전부 Acc@1 0%**, 실패의 **65.7%가 reasoning gap이지 데이터 부족이 아니다.**
**그리고 L4(FSE'25)가 결정적이다: 진단 경로에 LLM을 전혀 쓰지 않고**(Drain + IsolationForest + DTW) LLM 시대 log-AD baseline(0.207–0.366)을 F1 0.873으로 압도했다. **이 공간에서 가장 강력한 anti-LLM 논거다.**

**Why existing approaches are insufficient.** 모든 벤치마크가 *클라우드 마이크로서비스*용이다. **HPC를 다루는 것이 없다** — Slurm 없음, MPI/NCCL collective 없음, fabric counter 없음, 병렬 파일시스템 없음, 배치 큐 의미론 없음, 노드 상태 기계 없음. 서베이가 *"no shared benchmarks"*를 구체적 병목으로 지목한다.

**Hypothesis.** 프런티어 모델 agent는 실제 HPC 운영 인시던트에서 **낮은 점수**(ITBench SRE 13.8%에 준하는 수준)를 받을 것이며, 실패의 지배적 원인은 telemetry 부재가 아니라 **HPC 특유의 시스템 의미론에 대한 추론 실패**일 것이다.

**Required data / 구성.** Tier-0 기계의 실제 인시던트 N건(≥50, 이상적으로 ≥100), 각각에 대해 **진단에 필요한 동결된 telemetry 스냅샷**, Slurm/DCGM/fabric/Lustre/RAS를 도구로 노출하는 **agent-system 인터페이스**, **운영자 판정 ground-truth 진단**.

**Baselines.** L4의 **Drain + IsolationForest + DTW 파이프라인**(비LLM baseline으로 정확히 이것 — L4가 LLM 없이 LLM baseline을 이겼다는 사실이 이 벤치마크의 가장 흥미로운 축이다) · 프런티어 모델 agent 다수 · 인간 운영자 baseline(측정된 진단 시간).

**Metrics.** top-1/top-3 진단 정확도 · 시간 · **비용과 지연** · agent가 실제로 사용한 telemetry 채널 ablation · hallucination rate.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **⚠️ 부분 — C4에 종속된다.** label 파이프라인 없이는 ground truth를 만들 수 없고, ground truth 없이는 SC에 낼 수 없다. **G는 E의 하류다.**

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **4** | 진단 시간이 실제 병목 |
| Research novelty potential | **3** | 도메인 이식 반론이 강함. artifact 가치는 높음 |
| Generalizability | **5** | 벤치마크는 정의상 커뮤니티 자산 |
| Data availability | **2** | 실제 운영 데이터 공개(정제·기관 승인) + 수작업 판정 |
| Experimental feasibility | **2** | 프로젝트 예산 대부분이 여기 들어간다 |
| Publication potential | **3** | artifact 기여는 SC에서 받아들여지나 novelty 반론 |

**SC regular potential:** **SC Technical Paper stretch.** artifact 가치가 novelty 약점을 부분 상쇄한다.

**거부당하는 형태:** *"we applied GPT-N to our syslog and it summarized it nicely"* · 문서 RAG · LLM-as-judge 단독 평가 · 운영자 확인 ground truth 없는 RCA 주장.

---

# C8. job 비효율 리포팅이 사용자 행동을 바꾸는가 (가장 착수하기 쉬움)

> **연구 질문:** 사용자에게 job이 비효율적이었다고 알려주면, 실제로 자원 요청·낭비 node-hour·큐 압력이 변하는가?

**Operational problem.** 아무도 사용자에게 job이 자원을 낭비했다고 말해주지 않는다. Indiana University가 측정한 실태: 295,470 GPU job에서 **평균 GPU 이용률 11%**, **53%의 job이 GPU를 아예 쓰지 않았다**(사용하지 않은 job 제외 시 26%).

**Existing production practice.** TU Dresden **PIKA**(5년 이상 production, 사용자와 관리자 모두 사용), JSC **LLview**(JUWELS Cluster+Booster production, 오픈소스, role-based access), SUNY Buffalo **XDMoD Application Kernels**. **전부 운영 경험으로 손튜닝한 임계값이며, ground truth 대비 검증도 cross-site 이전도 없다.**

**Closest research.** **NOT FOUND.** archival 논문이 없다. workshop만 있다(MODA23 PIKA, MODA25 LLview, MODA26 roofline telemetry, HPCSYSPROS23/24).

**Why existing approaches are insufficient.** "비효율"의 합의된 정의가 없고, **알려주면 행동이 바뀌는가에 대한 측정이 전혀 없다.** SC25 ODA BoF 설문(29명)이 정확히 이 격차를 보여준다: 사용자는 운영 데이터의 가치를 **4.3/5**로 평가하지만 자기 활용 역량은 **2.9/5**로 평가하며, 청중은 운영자 17 / 연구자 11 / **사용자 1명**이었다.

**Hypothesis.** production 시스템에서 job 효율 리포팅을 도입하면 (i) 사용자의 자원 요청 정확도가 개선되고, (ii) 낭비 node-hour가 감소하며, (iii) 큐 대기가 감소한다 — 그리고 그 효과 크기는 측정 가능하다.

**Required data.** 도입 전후의 job accounting + per-job 자원 이용률 telemetry + 자원 요청 이력. 이상적으로는 **단계적 도입(staggered rollout)**으로 대조군 확보.

**Baselines.** 도입 전 기간 · 리포팅을 받지 않은 사용자 집단 · 리포팅을 열어본 사용자 vs 안 열어본 사용자.

**Metrics.** 요청 자원 대비 실사용 비율의 변화 · 낭비 node-hour · 큐 대기 시간 · 리포트 열람률 · 사용자별 시계열 변화.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 예 — 가장 쉽다.** 필요한 것은 production 시스템, 모니터링 스택, 그리고 규율 있는 연구 설계뿐이다. **새 알고리즘이 필요 없다.**

**Researchability.**

| 항목 | 점수 | 근거 |
|---|---|---|
| Operational importance | **5** | 11% GPU 이용률이 실제 숫자다 |
| Research novelty potential | **3** | 알고리즘 novelty 없음. **미수행이라는 사실이 novelty** |
| Generalizability | **3** | 사용자 문화 의존적. 다중 센터면 크게 강해진다 |
| Data availability | **5** | 이미 다 있다 |
| Experimental feasibility | **5** | 최고 |
| Publication potential | **3** | workshop은 확실. SC는 규모와 설계에 달림 |

**SC regular potential:** **strong workshop paper** (HPC-ODA 2026 / MODA 최적). **다중 센터 + staggered rollout + 측정된 효과 크기**를 갖추면 **SC State of the Practice** 트랙에 실질적으로 도달 가능하다.

> **전략적 위치:** 이것은 **첫 논문**으로 최적이다. 위험이 낮고, 데이터가 이미 있고, HPC-ODA 2026(1회차, PC가 LRZ/BU/ORNL/NERSC/HPE)에 진입하기에 완벽한 주제이며, 그 PC가 나중에 SC 제출물을 심사할 사람들이다.

---

# C9. 운영 정책 변경의 counterfactual 평가 방법론

> **연구 질문:** production 슈퍼컴퓨터에서 A/B 테스트를 할 수 없을 때, 스케줄링·전력·냉각 정책 변경을 어떻게 평가하는가?

**Operational problem.** 모든 L6/L7 결과가 시뮬레이션에서 멈춘다. 이것이 이 분야 전체를 가로막는 메타 문제다.

**Existing production practice.** 없다. 정책은 판단으로 바뀌고, 사후에 대시보드로 확인된다.

**Closest research.** **ExaDigiT SC24**가 물리를 풀었다 — Frontier 6개월 telemetry replay로 V&V된 결합 power + transient thermo-fluidic + scheduling 모델, 오픈소스. MODA23 HPE 고속 스케줄링 시뮬레이터(*"you cannot A/B-test scheduling policy on a production machine"*를 명시적으로 겨냥, 그러나 검증 없음). MODA25 duration-informed scheduler(M100 ExaData trace, 평균 대기 **~11% 감소**, **시뮬레이션만**).

**Why existing approaches are insufficient.** **ExaDigiT는 물리를 풀었고 정책 평가 방법론은 아무도 하지 않았다.** 실제 시스템 대비 오차 막대를 갖춘 정책 평가 프로토콜이 없다.

**Hypothesis.** digital twin 위의 정책 평가에 대해, 실제 시스템 대비 예측 오차를 정량화하고 정책 순위의 신뢰도를 진술하는 검증 프로토콜을 구성할 수 있다.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **⚠️ twin 구축 비용이 크다.** ExaDigiT가 오픈소스이므로 처음부터 만들 필요는 없으나, 한강용 파라미터화와 검증에 상당한 투자가 필요하다. **ORNL과의 협업이 자연스러운 경로다**(ExaDigiT 팀 = SC21/SC24/SC26 ORNL ODA 그룹).

**Researchability:** Operational importance **5** · Novelty **4** · Generalizability **4** · Data availability **3** · Feasibility **2** · Publication **3**
**SC regular potential:** **SC Technical Paper stretch.** 자원 투입이 크고 협업 의존적이다.

---

# C10. Telemetry integrity / observability debt 지표

> **연구 질문:** 벤더가 제공하는 telemetry는 독립 수집기 대비 무엇을 잃고 있으며, 그 손실이 하류 모델 정확도에 무엇을 하는가?

**Operational problem.** 사이트들이 벤더 telemetry 경로를 우회한다. NERSC: CSM `telemetry-api`가 *"unreliable and often inefficient. It stopped feeding data at random times, and frequently caused Kafka rebalancing events"*, Perlmutter 전규모에서 *"could not handle the data rate (100K to 1M messages per second)"*. LLNL: CSM 내장 LDMS가 *"significantly behind the latest LDMS release"*, up-stream되지 않은 독점 sampler 포함, CSM 업데이트마다 사이트 커스터마이징 재구현 필요. CSCS: CSM 내장 Kafka가 *"does not expose any external listener"*, Fluent Bit는 *"we couldn't make it stable for large throughputs"*. CSCS EMOI: 동일 job의 telemetry 기반 에너지 **5,663,156 J** vs Slurm **5,662,307 J**, 그리고 *"Slurm on the other hand, shows sometimes a weird behaviour and cannot therefore always be trusted."*

**Existing production practice.** 사이트별 우회로 구축. 측정도 비교도 없다.

**Closest research.** **NOT FOUND.** telemetry 품질 벤치마크 논문이 존재하지 않는다. 인접: DSN'25 industry의 *Hardware Telemetry at Scale: SSDs Endurance Monitoring in Datacenters*(Meta) — 사례 연구이지 최적화도 품질 지표도 아니다.

**Hypothesis.** 동일 노드에서 벤더 경로와 독립 수집기를 동시에 돌리면 측정 가능한 완전성·충실도 손실(누락 표본, 타임스탬프 왜곡, 값 불일치, cardinality 손실)이 존재하며, 그 손실이 하류 탐지 F1과 탐지 지연에 유의한 영향을 준다.

**Required data.** 동일 노드 집합에 대한 이중 수집 캠페인. CSCS가 이미 제공한 불일치(849 J)와 Sandia가 측정한 노드 간 **수 밀리초의 sample-time 편차**가 출발점.

**Metrics.** 표본 완전성 · 타임스탬프 동기 오차 · 값 일치도 · metric cardinality 손실 · 그리고 이것들이 C1/C5의 하류 지표에 미치는 영향.

**REPRODUCIBLE_WITH_AVAILABLE_HPC_TELEMETRY?** **✅ 매우 높다.** 한강 도입 시점에 이중 수집을 설계해 넣으면 자연스럽게 얻어진다.

**Researchability:** Operational importance **5** · Novelty **3** · Generalizability **4** · Data availability **4** · Feasibility **4** · Publication **3**
**SC regular potential:** **strong workshop paper** 단독. **C1의 필수 구성요소로 통합하면 SC 논문의 일부가 된다** — "telemetry를 얼마나 줄일 수 있는가"를 논하기 전에 "지금 수집되는 telemetry가 무엇을 놓치고 있는가"를 측정해야 하기 때문이다.

---

# PART III — 실행 권고

## 3.1 우선순위와 순서

| 시기 | 활동 | 산출 |
|---|---|---|
| **즉시 (지금)** | **전해상도 다계층 telemetry 아카이빙 시작.** Slurm 노드 상태 이력에 **actor 필드** 기록 설계. 운영팀과 **incident labeling 약속** 체결. **Slingshot fabric counter 접근권**(HPE STT / fabric manager) 확보 협상. **이중 수집**(벤더 경로 + 독립 수집기) 설계 | 이후 모든 후보의 전제조건 |
| **~6개월** | **C8** 착수(job 효율 리포팅, staggered rollout). **C10** 이중 수집 결과 1차 분석 | **HPC-ODA 2026(SC26, 1회차)** 제출 |
| **6–18개월** | **C1**(비대칭 + Pareto frontier) 본격 착수. **C2**(전이 손실 분해)를 M100 ExaData + F-DATA로 선행 착수 — 공개 데이터만으로도 초기 결과가 나온다 | ISC / IEEE Cluster 중간 논문 |
| **18–30개월** | **C1** 또는 **C2**를 SC Technical Paper로. **C4+C5** 결합을 두 번째 트랙으로 | **SC 제출** |
| **조건부** | **C3**(운영 프로그램 설계 필요), **C6**(actor 필드 + 권한 필요), **C7**(C4 완료 후), **C9**(ORNL 협업 시) | — |

## 3.2 협업 권고

`03_SC_REGULAR_PRECEDENTS` §3.1이 보여주듯, **연구 산출은 시스템 규모가 아니라 학술 파트너 유무와 상관된다**(Bologna↔CINECA, Bologna↔RIKEN, W&M↔ORNL, Basel/TUM↔LRZ, UMD↔NERSC). 그리고 **데이터를 공개한 센터가 곧 연구를 내는 센터다.**

→ **가장 레버리지 높은 기관적 결정은 파이프라인을 설계하기 *전에* 대학 ML 그룹을 운영 데이터에 계약으로 결합시키는 것이다.**

접촉 후보(전부 이 census에서 반복 등장):
- **Ayse Coskun (BU)** — HPC-ODA 2026 공동 의장, Prodigy/Proctor/ALBADross 계열
- **Andrea Bartolini / Andrea Borghesi (Univ. of Bologna)** — M100 ExaData와 F-DATA를 모두 만든 그룹. **세계 최대 공개 HPC 운영 데이터셋 2종이 한 학술 그룹에서 나왔고, 그들은 서로 다른 두 센터와 협업했다. 이것이 KISTI가 복제해야 할 모델이다**
- **Woong Shin / Feiyi Wang (ORNL)** — ODA 라인, MODA26 keynote, SC26 Best Paper nominee 저자군
- **Abhinav Bhatele (UMD)** — NERSC와 공저로 IPDPS'26 두 편. **센터가 학술 그룹과 공저해서 자기 telemetry를 top-tier 논문으로 만드는 정확한 구조**
- **Martin Schulz / Michael Ott (TUM/LRZ)** — DCDB/Wintermute, HPC-ODA 2026 조직

## 3.3 마지막 경고

1. **HPC node-level anomaly detector를 제안하지 말 것** (SC'23 + SC'25가 닫음)
2. **cross-system log anomaly detection을 제안하지 말 것** (ICSE'24 + CroSysLog가 F1 97–99%로 닫음)
3. **causal graph discovery를 RCA 해법으로 제안하지 말 것** (실제 telemetry에서 Acc@1 0% 실증)
4. **"peer와 비교한다"를 기여로 삼지 말 것** (IASO ATC'19가 3.9만 노드에서 production-solved)
5. **한국 데이터셋 공개 단독으로 SC를 노리지 말 것** (PEARC/데이터셋 트랙 논문이다)
6. **`05_RESEARCH_PRACTICE_GAPS` PART IV의 미확보 문헌을 먼저 읽을 것.** 특히 **SC26 *From Alert Fatigue to Root Cause*(ORNL)**, **Mantis(ICS'26)**, **Safe Remediation as Risk-Constrained Intervention(arXiv 2607.20005)**. 어느 것이든 위 판정을 뒤집을 수 있다.

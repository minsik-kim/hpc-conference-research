# 13. VERIFICATION ROUND 2 — 회수 결과와 순위 재판정
## 8개 병렬 검증 트랙의 통합, `09`–`12`에 대한 정정, 최종 순위 개정

> **문서 지위:** `12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md`의 최우선 항목에 대해 8개 검증 트랙을 실행하고 회수한 결과. **`09`의 감사 결과 중 여러 항목이 다시 뒤집혔으므로, `09`–`12`를 읽기 전에 이 문서를 먼저 볼 것.**
> **원천:** `raw/V1_db_retention_sweep.md` · `V2_sc26_ornl.md` · `V3_pika_tuncer.md` · `V4_hindsight_suffbench.md` · `V5_fdi_sensor_placement.md` · `V6_lcopt_centile_setdiff.md` · `V7_nonenglish_indices.md` · `V8_grey_isc.md`
> **작성일:** 2026-09-06

---

# §0. 한 페이지 요약 — 이번 라운드가 바꾼 것

| # | 발견 | 영향 |
|---|---|---|
| **1** | **SC26 ORNL 논문의 정확한 제목이 확인되었다: *"From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System"* — Technical Papers, Best Paper Nominee** | ⚠️ **이번 라운드 최대 사건.** "causal failure **cascade**" = F1의 Q-δ가 다루려던 바로 그 대상(계층 간 cascade 순서)이며, F3가 겨눈 alert→root cause 공간이기도 하다. **F1과 F3를 동시에 위협한다** |
| **2** | **H1a(ordering/lag 손실이 진단 열화의 메커니즘)는 novel하지 않다** — Plis & Danks UAI 2015, Gong & Zhang ICML 2015, Gong UAI 2017이 정확히 이 메커니즘을 정리로 확립 | **`09` §12.2가 "가장 novel한 부분"으로 지정한 Q-δ의 메커니즘 주장 FALSIFIED.** 헤드라인을 또 한 번 옮겨야 한다 |
| **3** | 그런데 **retention 해상도 축은 두 개의 독립 문헌에서 각각 생존**했다 — DB venue 스윕(Goku PVLDB'24가 완전한 age-tiering을 기술하고 throughput/latency/cost만 평가)과 FDI 스윕(retention이 FDI 존재론에 아예 없음) | ✅ **`09` §4.3의 유일 생존 축이 이번에 훨씬 강한 근거를 얻었다.** F1은 죽지 않았고, 중심이 이동했다 |
| **4** | **CAMEO(EDBT 2026)**가 downsampling 비율을 변화시키며 anomaly detection 정확도를 측정한다 | 일반형 주장("데이터 축소를 변화시키며 탐지 정확도를 측정한 논문이 없다")은 **거짓**. 운영 IT/HPC 다변량 telemetry + retention 프레이밍으로 좁혀야 함 |
| **5** | **연속 통계 진단 품질 축은 FDI에서 15년 된 분야다** — Eriksson Automatica 2013, Jung SAFEPROCESS 2015. Eriksson/Krysander/Frisk SAFEPROCESS 2012는 **시간 변수만 뺀 동형 정식화** | **`09` §12.1의 "Rosich에 없는 것" 4개 중 3번(연속 통계 품질) DEAD.** 철회 필수 |
| **6** | **Slingshot switch counter는 확보 불가가 아니다** — CUG 자료에서 확보 실패를 보고한 사이트가 없다. 제약은 접근 거부가 아니라 **조회 비용**(포트당 1000+ counter, 스위치당 64K+, 전량 조회 약 0.5초) | ✅ **`09` §11 C5의 최강 feasibility 반론이 약화.** F3의 실현성이 올라간다 |
| **7** | **KISTI 국내 문헌이 16편이 아니라 23편**(KISTI 저자 20편)이며, **약 9편은 영어판이 없다** | ⚠️ `09` §9의 수가 낮았던 이유가 규명되었다. 누리온 telemetry 아키텍처, GPU 열 기반 fail-slow 자동 조치, 6호기를 명시한 2026년 논문이 포함 |
| **8** | **S-RAPS(SC'25 Workshops)**가 C9의 진짜 gate다(LC-Opt 아님). ExaDigiT의 RAPS를 실제로 확장하고 5개 실trace로 스케줄링 정책 what-if를 수행 | C9의 물리 twin은 닫혔으나, **정책 평가 방법론과 remediation 조치 클래스는 양쪽 논문 모두 손대지 않았다** → F4로 흡수 |
| **9** | **ISC 연구논문은 2023년 이후 Springer LNCS를 떠났다**(Prometeus/IEEE, DOI prefix `10.23919/isc.<year>`) | ⚠️ 방법론 오류 정정. LNCS 기반 census는 2024–2026에서 0편을 발견하고 "트랙이 비었다"고 잘못 결론낼 수 있다. 실제로는 **24 / 28 / 35편**이며 관련 논문 **4 / 8 / 9편** |
| **10** | **PIKA는 IEEE Cluster 본트랙이 아니라 HPCMASPA 2020 워크숍 논문**이다 | `09` §8.1의 정정을 다시 정정. 아카이브 등재는 맞으나 워크숍 |

**순위 개정 결과:** F1은 `TOP-CANDIDATE` → **`SC-PLAUSIBLE` (SC26 ORNL 초록 확인 조건부)**. F2는 상대적으로 상승해 **실행 순서상 1순위 + 강도상 공동 1위**. F3는 실현성 상승·선점 위험 상승으로 순위 유지. F4는 S-RAPS의 자체 각주로 **소폭 상승**.

---

# §1. 인용 정정 — 반드시 반영할 것

`09` §0.1과 동일한 등급의 항목이다. **정정 전에는 절대 인용하지 말 것.**

## 1.1 CENTILE — `09` §6.3의 서술과 인용 문구가 틀렸다

| 항목 | `09`의 서술 | 검증 결과 |
|---|---|---|
| 제목 | (미기재) "cross-domain 전이 + adapter" | ***"Centile: A Telemetry Foundation Model Evaluated by the Decisions It Drives"*** |
| 저자 | (미기재) | **Zifan Zhang, Zhichao Hou, Tingxiang Ji, Yuchen Liu** — 전원 NC State |
| ID | arXiv 2608.01725 | **ID는 정확함** |
| 날짜/venue | (미기재) | [cs.NI] 2026-08-03, 게재 venue 미발견 |
| 성격 | "cross-domain 전이 + adapter" | **telemetry foundation model.** adapter는 입력 embedding 단계의 일부이고, cross-domain 전이는 6개 실험 절 중 하나일 뿐 논지가 아니다 |
| 전이 축 | "cross-domain" | **cross-month(zero-shot) + cross-domain(ISP/cloud → Fugaku walltime). cross-generation은 없다** — 문자열 탐색으로 "generation" / "schema" / "hardware change" 부재 확인 |
| 손실 분해 | (암시) | **없음.** 전이를 *from-scratch 대비 이득*으로 보고(저장소 README: 6시간 예산에서 35.9±1.3 vs 83.0±36.0 mBSLD) — penalty matrix와 반대 방향의 객체 |
| 분할 | (미기재) | **엄격한 시간순.** 저자 문구: *"Training reads only data strictly earlier than the evaluation window… so no prediction ever reads its own future."* |

> 🚨 **`09` §6.3에 CENTILE에 귀속된 인용 문구는 재확인되지 않았다.** 검증 결과 확인된 초록·서론과 정합하지 않으며, 해당 문구가 있을 절(IV–VI)은 arXiv HTML이 §IV-A 이후 4회 모두 절단되어 회수 실패. **`09` §6.3의 해당 인용을 삭제하거나, PDF에서 재추출하기 전까지 `MISATTRIBUTED — 재확인 필요`로 표시할 것.**

**F2에 대한 판정: 재프레이밍(측정 + transfer-penalty matrix)은 `SUFFICIENT`.** CENTILE은 cross-generation도, 원인 분해도 하지 않는다. 단 조건 3개: (a) related work의 서술을 위 표대로 고칠 것, (b) 문제의 인용을 빼거나 재추출할 것, (c) CENTILE의 시간순 분할과 seed 분산 보고를 **맞출 것**. 잔존 위험: CENTILE이 Fugaku와 M100을 함께 싣고 adapter가 신규 소스 추가를 쉽게 만들었으므로 cross-system 후속이 용이하다 — 방어선은 우선권이 아니라 **분해**다.

## 1.2 TelemetrySuffBench — 수치의 적용 조건이 빠져 있었다

| 항목 | 검증 결과 |
|---|---|
| ID | **arXiv 2608.07899 — 정확함** |
| 제목 | *"TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?"* |
| 저자 | **Yuxuan Zhu, Peng Pu** (소속 NOT FOUND), 2026-08-08, venue 없음 |
| 대상 | ⚠️ **LLM 에이전트 실행 trace이지 HPC metric이 아니다.** 진단자는 프런티어 LLM들 |
| 데이터 | 합성. *"generated deterministically from instrumented, stateful workflows"*, 312 trace |
| 변화시킨 것 | **의미적 view 6종 + field masking 요인 7종.** **시간 해상도는 변화시키지 않는다**(용어 탐색 2회로 확인: "sampling"/"downsampl"/"frequency"/"timestamp"/"temporal"/"lag" 부재. "coarse"는 축소된 field set을 의미) |
| lag/ordering | **없음.** 오히려 **경쟁 메커니즘**을 제시: *"reliable causal attribution requires explicit decision-to-provenance links."* |
| 비용 축 | 없음 |

> 🚨 **`09` §4.1 HIT 1의 "탐지 F1 99.5–100% vs origin-step 정확도 ≤0.5%"는 조건을 잃은 인용이다.** 두 수치는 모두 원문에 있으나 **서로 다른 조건**의 값이다: ≤0.5%는 **restricted view**에서만 성립하고, **full telemetry**에서 origin-step Top-1은 **33.8%–97.2%**다. 무조건적으로 인용하면 원문을 왜곡한다.

**F1에 대한 판정:** H1을 `PARTIAL`하게 손상시킨다(비대칭의 존재를 뒷받침하나, 시간 해상도가 아니라 field 내용을 변화시키고, 합성 에이전트 trace이며, 비용 축이 없다). **H1a는 죽이지 못한다 — 단정적으로 `NO`.**

## 1.3 Rosich 2012 — 단독 저자다

**정정:** `A. Rosich (2012). "Sensor Placement for Fault Detection and Isolation based on Structural Models." 8th IFAC SAFEPROCESS, Mexico City, pp. 391–396. DOI `10.3182/20120829-3-MX-2028.00161`. **단독 저자.** Sarrate/Nejjari는 SAFEPROCESS 2012의 **다른 논문** 저자다(§2.3 참조).

`09`가 기록한 세부는 전부 전문에서 verbatim 확인됨: *"Diagnosis specifications are feasible as long as D ⊆ Dmax and I ⊆ Imax"*, *"First, the detectability problem is solved. And then, based on the obtained results, the isolability problem is solved"*, Problem 3의 형태. **단 Rosich 2012에는 비용 모델이 없다** — 모든 minimal 구성을 열거한다.

**추가 확인:** Krysander & Frisk 2008 = `IEEE Trans. SMC-A 38(6):1398–1410`, DOI `10.1109/TSMCA.2008.2003968`. Fault Diagnosis Toolbox의 `SensorPlacementDetectability()` / `SensorPlacementIsolability()` **함수명 둘 다 API 문서에서 verbatim 확인**. 단 툴박스의 1차 인용은 **Frisk, Krysander & Jung (2017), IFAC World Congress, DOI `10.1016/j.ifacol.2017.08.504`**.

## 1.4 LC-Opt — 전체 metadata 및 "ExaDigiT 기반" 표현 주의

**정정:** *"LC-Opt: Benchmarking Reinforcement Learning and Agentic AI for End-to-End Liquid Cooling Optimization in Data Centers."* Naug, Guillen, V. Kumar, Greenwood, Brewer, Ghorbanpour, Ramesh Babu, Gundecha, Luna Gutierrez, Sarkar. **HPE + ORNL**(Kumar/Greenwood/Brewer가 ORNL). **NeurIPS 2025 Datasets & Benchmarks Track**, DOI `10.52202/085713-5325`, arXiv 2511.00116(2025-10-31). 코드 `github.com/HewlettPackard/sustain-lc`.

⚠️ **두 가지 주의:** (a) 부록과 저장소는 이를 **SustainLC**로 부른다. (b) **코드로서 ExaDigiT 기반이 아니다** — ExaDigiT를 서술하고 Modelica 계보와 ORNL 저자 3명을 공유할 뿐이다(*"The intention is for this tool specifically to help standardize digital twin workflows for ExaDigiT"*). **"ExaDigiT 위에 세웠다"고 무조건 쓰지 말 것.**

## 1.5 PIKA — 워크숍 논문이다

**정정:** Dietrich, Winkler, Knüpfer, Nagel, *"PIKA: Center-Wide and Job-Aware Cluster Monitoring"*, **pp. 424–432**, DOI `10.1109/CLUSTER49012.2020.00061` — **HPCMASPA 2020 워크숍 논문**(Workshop on Monitoring and Analysis for High Performance Computing Systems Plus Applications, 2020-09-14 Kobe, IEEE Cluster 2020 병설). 저자 측 두 개 독립 출처(ProPE 프로젝트 발표목록, 저자 자신의 2023 후속 논문 ref [5])로 확정.

**용어 정정:** **HPCMASPA는 IEEE Cluster 병설, MODA는 ISC 병설**이다. `09`가 "PIKA MODA 2023 후속"이라 한 것은 실제로 **ISC 2023 워크숍 chapter, LNCS 13999, pp. 295–306**이다.

→ **`09` §8.1의 "PIKA는 창립 논문이 IEEE Cluster 2020이다"를 "PIKA의 창립 논문은 IEEE Cluster 2020 proceedings에 수록된 HPCMASPA 2020 워크숍 논문이다"로 교체.** 아카이브 등재는 사실이므로 §8.1의 취지(PIKA에 아카이브 논문이 있다)는 유지되나, 본트랙이라는 함의는 제거.

## 1.6 기타 metadata 정정

| 항목 | 정정 |
|---|---|
| **SeT-Diff** | Esposito, Antici, Cesarini, Bartolini (Bologna + CINECA). **CF '26, Catania, pp. 109–112**(4쪽 short paper), DOI `10.1145/3801487.3806064`, arXiv 2607.22548v1 |
| **Hindsight** | *"The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems"* — Lei Zhang(Emory/Princeton), Zhiqiang Xie(MPI-SWS), Vaastav Anand(MPI-SWS), Ymir Vigfusson(Emory), Jonathan Mace(MPI-SWS), **NSDI '23** |
| **Tuncer TPDS** | *"Online Diagnosis of Performance Variation in HPC Systems Using Machine Learning"*, Tuncer, Ates, Zhang, Turk, Brandt, Leung, Egele, Coskun, **IEEE TPDS 30(4):883–896, 2019-04**, DOI `10.1109/TPDS.2018.2870403`. 학회판: *"Diagnosing Performance Variations in HPC Applications Using Machine Learning"*, **ISC HPC 2017, LNCS 10266, pp. 355–373**, DOI `10.1007/978-3-319-58667-0_19`, **Gauss Award** |
| **LDMSCON** | **2019–2025**. `09`/`12`의 "2015–2025"는 오류. 비아카이브 |
| **HPC-ODA** | BoF 시리즈 2019–2025. **최초의 peer-reviewed 워크숍판이 SC26(2026-11)** — 아직 개최되지 않았다. `D_workshops`의 정정과 일치 |
| **MODA** | **6판, 총 17 chapter 전량 열거 확인**(LNCS 12321 / 12761 / 13387 / 13999 / 15058 / 16091). `09`의 "17 chapter" 추정이 정확히 맞았다. **그중 다중 rate 오버헤드 연구는 0편** |
| **ISC 연구트랙** | 2024년부터 **Prometeus GmbH / IEEE**, ISBN 978-3-9826336-0-2 / -1-9 / -2-6, DOI prefix `10.23919/isc.<year>` |

---

# §2. Claim 재판정 — 이번 라운드로 뒤집힌 것

## 2.1 🚨 H1a(ordering/lag 메커니즘) — **FALSIFIED as a general claim**

`09` §12.2는 Q-δ를 *"가장 novel한 부분… 어느 분야에서도 발표된 것을 찾지 못했다"*로 지정했다. **그 판정이 뒤집혔다.** 인과 구조 학습(causal discovery) 문헌이 subsampling과 temporal aggregation 하에서 정확히 이 메커니즘을 확립해 두었으며, 계보는 약 55년에 이른다.

**가장 치명적인 인용:**
> **Plis, Danks, Yang, UAI 2015** (전문 확인): *"an apparent A → B connection at τM can be consistent with any possible connection at τS: A → B, A ← B, or no connection at all."*

이것은 H1a의 메커니즘을 **문자 그대로** 진술한 것이다.

> **Gong, Zhang, Schölkopf, Tao, Geiger, ICML 2015** (초록 verbatim): *"when the data resolution becomes lower due to subsampling, neither the original Granger causal analysis nor the extended one is able to discover the underlying causal relations."*

**추가 확인:** Gong 외 UAI 2017이 temporal **aggregation**(= HPC의 rollup에 정확히 대응)에 대해 동일 결과. Plis 외 NIPS 2015 및 Hyttinen, Plis, Järvisalo, Eberhardt, Danks 2016: *"in general underdetermined, even when the subsampling rate u is known and small."* 계량경제학 계보(Sims 1971, Wei 1982, Marcellino 1999, Breitung & Swanson 2002)도 동일 방향.

### 두 개의 추가 위협 — 단순 비-novelty보다 나쁘다

| 위협 | 내용 | 대응 |
|---|---|---|
| **(a) 복원 가능성** | Gong ICML'15: *"if the noise terms are non-Gaussian, the underlying model for the high frequency data is identifiable from subsampled data under mild conditions."* → **H1a는 정보이론적으로 거짓이고, 나이브 추정기에 대해서만 참이다** | ⚠️ **실험에 subsampling-aware 추정기를 baseline으로 반드시 넣어야 한다.** 넣지 않으면 심사자가 "당신이 측정한 손실은 추정기의 결함"이라고 말하고 그 말이 옳다. **`11` §1.7의 baseline 목록에 B7을 추가**(§4.2) |
| **(b) 비단조성** | **Solovyeva, Danks, Abavisani, Plis, CLeaR 2023** — 더 느린 측정이 인과 정보를 *추가*할 수 있다는 반례. 단조적 H1a를 반박 | 해상도-품질 곡선이 단조라고 가정하지 말 것. `11` §1.8의 곡선 해석과 §1.11의 폐기 기준을 수정(§4.3) |

### 무엇이 남는가

**메커니즘이 아니라 운영적 실증이다.** 검증 결과의 표현을 그대로 옮긴다: 실제 다계층 HPC telemetry에서 이것을 측정한 사람이 없고, **비용 축을 붙인 사람이 없으며**(bytes/node/day, $/GB-month — *"the cleanest unclaimed ground in the audit"*), 운영점(operating point)을 갖는 해상도-대-진단가능성 곡선을 낸 사람이 없다.

**권고 프레이밍:** Plis/Danks와 Gong/Zhang을 **기반으로 인용**하고, 주장을 *"cross-layer cascade order 복원이 붕괴하는 해상도 문턱에 대한, 실제 telemetry 기반의 최초 비용인식 정량화, 그리고 그로부터 도출되는 retention 정책 설계점"*으로 좁힐 것.

## 2.2 ✅ Retention 해상도 축 — **두 문헌에서 독립적으로 재확인, 이번 라운드 최대 강화**

`09` §4.3의 유일 생존 축이 두 개의 서로 무관한 스윕에서 각각 살아남았다.

### DB venue 스윕 결과 (V1)

**판정: `NO COUNTEREXAMPLE FOUND IN THIS SWEEP`.** 4개 기준(retention/rollup을 독립변수로 변화 + 하류 분석 품질 측정 + peer-reviewed + 운영 telemetry) 전부를 만족하는 논문 없음.

**가장 강력한 gap 인용 3건 — 반드시 쓸 것:**

| 논문 | 왜 결정적인가 |
|---|---|
| **Goku, PVLDB 2024** | **완전한 age-tiered 정책을 명시**한다 — *"24 hours of data in-memory… 80 days… SSD… 80 days to 384 days… HDD"* — 그리고 rollup과 downsampling을 이름으로 언급한 뒤, **throughput·latency·연간 비용만 평가한다.** gap에 대한 가장 깔끔한 단일 인용 |
| **Chronix, FAST 2017** | 설계 전체를 **미측정 주장** 위에 세운다: *"Chronix never drops the exact values of the data points. They always matter in the domain of anomaly detection."* |
| **Lindorm TSDB, PVLDB 2023** | pre-downsampling과 in-DB anomaly detection을 **둘 다 탑재**하고, 전자는 지연·저장으로, 후자는 wall-clock **시간**으로 평가하며 **둘을 교차시키지 않는다** |

**보너스:** PVLDB 17의 참조 TSAD 벤치마크는 8개 요인을 변화시키면서 전문 확인 결과 "granularity", "resolution", "sampling rate", "downsampling", "interval" 중 **어느 단어도 포함하지 않는다.**

**명명된 시스템 검증(전부 전문 확인, 전부 음성):** Monarch, Gorilla, Goku, Timon, Lindorm TSDB, ModelarDB, BTrDB, Chronix, Mach, PromSketch, SEER — 어느 것도 retention/rollup을 독립변수로 하지 않고, 어느 것도 분석 품질을 측정하지 않는다. **ByteSeries와 TimeUnion은 `TITLE-ONLY`로 남았다**(모든 경로에서 공개본 없음).

### FDI 스윕 결과 (V5)

**판정: retention은 `STILL OPEN` — 세 gap 중 최강.** 6개 질의군에서 FDI 히트 0건, 전문 확인한 4편에서 명시적으로 부재. 이유가 구조적이다: **FDI는 온라인 스트리밍 관측기 패러다임이며, 데이터 나이(data age)가 그 존재론에 자리가 없다.**

→ **결론: retention 해상도를 결정변수로 하는 축은 DB venue와 FDI 양쪽에서 비어 있다. 이것이 F1의 유일한 무조건 생존 근거이며, 이제 두 배로 확인되었다.**

## 2.3 🚨 연속 통계 진단 품질 축 — **DEAD. `09` §12.1에서 철회할 것**

`09` §12.1은 "Rosich에 없는 것" 4개를 나열했다. 그중 **3번(품질 제약이 binary structural isolability이지 연속 통계 품질이 아니다)이 falsified.**

**FDI에는 15년 된 quantitative diagnosability 분야가 있다:** Eriksson CDC 2011; **Eriksson 외, Automatica 2013, DOI `10.1016/j.automatica.2013.02.045`**; Jung 외 SAFEPROCESS 2015(KL-divergence distinguishability, 전문 확인). 이 분야는 **자신에 대한 비판을 스스로 발표했다** — 결정론적 분석은 *"only give yes/no answers."*

### 최강 적대 인용 — 사실상 동형 정식화

> **Eriksson, Krysander & Frisk (2012), *"Using quantitative diagnosability analysis for optimal sensor placement"*, 8th IFAC SAFEPROCESS, pp. 940–945, DOI `10.3182/20120829-3-MX-2028.00196`** (전문 확인, Eriksson 학위논문 LiU Thesis 1584 / DiVA diva2:610541 경유)
>
> *"the cheapest set of sensors that achieves a required fault diagnosability performance"* — **"minimum required diagnosability performance"를 제약으로 사용**하며, 연속 KL 기반 품질과 detectability·isolability 각각의 하한을 둔다.

**즉 `09` §12.1의 제약 최소화 형태 자체가 이미 발표되어 있다 — 시간 변수만 빼고.** 이것이 다루지 않는 것: **샘플링 rate, retention, 탐지 지연, 다자원 비용, 관측기 교란.** 그리고 **확률적 선형 descriptor 모델을 요구한다.**

### 비용 주장도 재진술 필요

**"기존 연구는 센서 개수만 센다"는 거짓이다.** **Sarrate, Nejjari & Rosich (2012), DOI `10.3182/20120829-3-MX-2028.00233`**(전문 확인)은 BILP 최소비용 정식화를 갖고, 비용이 *"can comprise... the purchase price, the maintenance price, the sensor reliability or the measurement precision"*이다.

→ **정확한 주장: 부재한 것은 비용 모델 자체가 아니라 (i) 데이터 볼륨 비용(bytes/s, TB-month, query cost)과 (ii) 관측기 교란(observer perturbation)이다.** 어디에도 bytes/s·TB-month·query cost에 상응하는 것이 없다.

### 모델 요구 방어논거 — 유지되나 문구를 정밀하게

**"이 방법들은 모델을 요구한다"고 쓰지 말 것.** 대신: *"isolability / 진단품질 제약 하에서 모니터링 구성을 선택하는 기존 방법 중, 해석적 또는 구조적 모델 없이 그것을 하는 것은 없다. data-driven 분야는 센서 집합을 고정한 뒤 분류기를 학습하거나, 2클래스 탐지 목적에 대해서만 센서를 선택한다."* 최근접 시도로 **Jung & Axelsson, DX 2024, DOI `10.4230/OASIcs.DX.2024.4`**(open access)를 인용 — 데이터의 intrinsic dimension에서 중복 구조를 복원하나 배치나 비용 최적화는 하지 않는다.

## 2.4 ⚠️ CAMEO (EDBT 2026) — 일반형 주장을 깬다

**Esposito 외가 아님 — 별개 논문.** *"CAMEO: Autocorrelation-Preserving Line Simplification for Lossy Time Series Compression"*, **EDBT 2026**, `openproceedings.org/2026/conf/edbt/paper-21.pdf`(arXiv 2501.14432). 전문 확인.

downsampling 비율을 변화시키고 탐지 품질을 그에 대해 그린다. **그림 캡션 verbatim:** *"Figure 13: (left) Impact on the Anomaly Detection Accuracy as the Compression Ratio Increases."* 압축을 *"from 2 (half the points sampled) to 10 (only 1000 points sampled)"*, 최대 100배까지 변화. Matrix Profile + UCR archive + UCR-score, 예측은 STL-ARIMA/ETS/LSTM.

**기준 4(운영 telemetry)에서 실패:** 데이터가 단변량 에너지/환경/UCR 계열(ElecPower, UKElecDem, SolarPower, Humidity, Pedestrian)이지 운영 IT/HPC telemetry가 아니다. **retention 프레이밍도 없다** — 나이 tiering 없음, rollup 스케줄 없음. 조절 변수는 압축기 내부의 ACF 오차 bound이고, 하류 품질은 목적함수가 아니라 압축기가 안전함을 **검증**하는 용도다.

→ **판정: 반례가 아니다(기준 4에서). 그러나 일반형 주장 "데이터 축소를 변화시키며 탐지 정확도를 측정한 논문이 없다"는 거짓이다.** F1의 주장은 **운영 IT/HPC 다변량 telemetry + retention 프레이밍**으로 명시적으로 좁혀야 하며, CAMEO를 related work에서 정면으로 인용해야 한다.

**두 번째 제약 — RALF (PVLDB 17, 2024):** **feature-update 예산**을 변화시키고 하류 anomaly detection 오차(MASE)를 **Azure VM telemetry**에서 측정한다. 기준 2·3·4 통과, 기준 1 실패(전문 확인: *"the paper does not discuss reducing the resolution of stored historical time series"*). **그러나 방법론(데이터 유지 예산 → 실제 VM telemetry의 탐지 품질)이 이미 PVLDB에 있다. 심사자가 인용할 것이다.**

## 2.5 GPU 교란 측정 gap — **conjunction으로 간신히 SURVIVES**

발견된 어느 논문도 4개 요건(다중 rate + 정량 측정 + GPU/BMC/fabric + 품질 축) 중 2개를 넘지 못한다. **그러나 각 leg가 서로 다른 논문에 의해 개별적으로 깨졌다.**

| 논문 | 깨는 leg | 하지 않는 것 |
|---|---|---|
| **Chen, Qian, Chien, Zilberman, *"Detecting Anomalies in Systems for AI Using Hardware Telemetry"* (Reveal), Oxford, arXiv 2510.26008v2** | GPU 포함 다중 rate 정량 오버헤드: *"overhead decreases as the sampling interval increases: from ~1.2-1.4% at 100 ms to below 0.6% at 600 ms"* | **수집기 CPU만 — 애플리케이션 지연은 미측정.** BMC/Redfish 없음, fabric 없음, 2/1/9 노드 테스트베드, 정확도-대-rate 곡선 없음, arXiv only |
| **McDaniel 외, ISC 2026, *"Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes"*** | GPU 세대 exascale(Frontier 128노드 MI250X, Portage 128노드 MI300A), 오버헤드 *"below 1%"* 측정, 실제 fidelity-vs-rate 논증(1 ms rocm-smi vs 100 ms Cray PM: 1 ms가 *"short transients that moving-average sensors smooth out"*를 드러냄) | 두 rate가 **소스 고유값이지 스윕한 설정이 아니다.** fabric 없음, Redfish 없음 |
| **Barry, Brandt, Gentile 외, CUG 2023, *"Evaluating and Influencing Extreme-Scale Monitoring Implementations"*** | **GPU(dcgm + rdc_sampler) + Redfish(hms-hmcollector) + Slingshot NIC 및 switch sampler가 한 시스템에 공존하는 유일한 사례**(El Capitan / Perlmutter) | 오버헤드가 **주장뿐**: *"no statistically significant adverse effects on system or application performance"* — CPU 세대 연구를 인용 |

**정정 2건:**
- **Wintermute(HPDC 2020)에는 GPU metric이 전혀 없다**(KNL, Omni-Path 플러그인). 단 accuracy-vs-rate 결과는 있다(전력 예측 오차 10.4% @125 ms vs 6.7% @500 ms). → **`12` W-12의 우려와 반대로, Wintermute는 주장을 강화한다**
- **ExaMon/Marconi100은 막다른 길이다** — ANTAREX book chapter도 M100 ExaData도 오버헤드 수치를 보고하지 않는다. `12` W-13 종결

**커뮤니티 자체 증거:** **Dagstuhl Seminar 23171**에 오버헤드·샘플링 rate 논의가 **전혀 없다** — 커뮤니티의 의제 문서가 이것을 미해결 문제로 명명하지 않는다. 양날의 검이다(문제가 인식되지 않았다 = 기회, 또는 = 중요하지 않다).

**안전한 최종 문구:** *"다중 rate 오버헤드 문헌과 GPU+BMC+fabric 커버리지 문헌은 **서로 겹치지 않는 두 집합**이며, 어느 쪽도 품질-대-rate 축을 갖지 않는다."* 여기에 "peer-reviewed"와 "production-scale"을 추가하면 Reveal에 대해서도 반박 불가.

## 2.6 Tuncer — **WINDOW. 단 한 문장의 유보가 따라간다**

**판정: `WINDOW`.** TPDS 2019에서 스윕되는 시간 변수는 **sliding window 크기**이고 sampling interval은 **1 s 고정**이다. 전문 verbatim: *"Fig. 2 shows the impact of window size on the overall F-score…"*, *"we conclude that a 45-second window size is a reasonable choice…"* 확인된 전체 스윕 목록: window size W(~10–90 s), FDR target, confidence threshold C, anomaly intensity, unknown input configurations, leave-one-application-out, application scale(4 vs 32 노드), classifier 선택. **미스윕: window 개수, sampling interval, training-set 크기.**

⚠️ **그러나 ISC 2017 학회판 §6.1에 다음 문장이 있다 (전문 verbatim):**
> *"We also measure the impact of data collection period by increasing it to 5 s; however, the impact on classification accuracy is negligible."*

**맥락:** 저자들이 MOC가 Volta보다 낮은 점수를 낸 이유의 후보 설명들(metric set 크기, 데이터셋 크기, collection period)을 소거하는 중. 1 s → 5 s 단일 확인, 산문뿐, **그림·표·수치 delta 없음.**

→ **`09`/`11`의 주장을 좁힐 것:** "샘플링 rate는 건드려지지 않았다" ❌ → **"샘플링 rate 민감도 *연구*는 존재하지 않는다. 유일한 데이터점은 학회판의 정량화되지 않은 산문 한 문장이며, 그 문장은 영향이 negligible이라고 말한다."** ⚠️ 이 문장은 H1에 **약하게 불리**하다. 숨기지 말고 인용하고, 5 s는 F1이 검증하려는 범위(수십 초~수 분)에 비해 훨씬 미세한 변화임을 지적할 것.

## 2.7 ✅ Slingshot switch counter — feasibility 반론 약화

`09` §11 C5의 최강 feasibility 반론은 *"Bhatele 그룹이 Perlmutter/Frontier에서 Rosetta switch counter를 얻지 못했다"*였다.

**CUG 자료 전체에서 switch counter를 *얻을 수 없다*고 보고한 사이트는 없다.** 제약은 **조회 비용**이다(verbatim):
- *"over a thousand counters per port and over 64K total port counters per switch"*
- *"execution time to retrieve the full set of metrics is about half a second"*
- *"the HPE-provided dump_counters binary"*를 경유
- *"We would like to work with HPE to identify more efficient port counter access mechanisms."*
- NIC 측은 수백 개 중 *"roughly forty"*가 기본값
- CSM/SMA가 *"fabric switch hardware telemetry"* 대시보드와 `cray-fabric-perftelemetry` Kafka 토픽을 노출. RouterBMC는 Redfish 센서 소스

→ **두 방향의 함의:** (a) **F3의 최강 feasibility 반론이 약화된다** — 네트워크 원인 클래스가 붕괴할 위험이 낮아졌다. (b) 그런데 스위치당 64K counter를 0.5초에 조회한다는 것 자체가 **F1의 C_query·C_network 비용 축의 완벽한 실증 대상**이다. 두 후보 모두에 유리한 발견이다.

⚠️ 단 `08` §6.1의 계약 단계 요구사항은 **유지**한다. "다른 사이트가 얻었다"는 것과 "한강 계약에 명시되어 있다"는 것은 다르다.

## 2.8 KISTI 국내 선행연구 — 16편이 아니라 23편, 그리고 원인 규명

`09` §9가 국제 색인만으로 16편을 찾았다. 국내 색인 스윕 결과 **KIPS 연차학술대회 논문집에서 21건 + 학술지 2편 = 23건**이며 **20건이 KISTI 저자**다. **약 9건은 영어판이 없다 — 이것이 국제 색인 기반 조사가 KISTI를 과소계수한 메커니즘이다.**

**F1·F3·F4에 직접 관계되는 확인 항목:**

| 항목 | 왜 중요한가 |
|---|---|
| 권민우·윤준원·홍태영, **PBS 작업 스케줄러 Hook를 이용한 슈퍼컴퓨터 5호기 계산노드 자동 점검 기능 구현**, 2019, `10.3745/PKIPS.y2019m10a.101` | 누리온 8,432노드 **자동 health check**. 국제판 존재: [Applied Sciences 11(13):6166, 2021] — 2019 전년 job log, **job 실패율 25.6%** |
| 권민우·윤준원·홍태영, **슈퍼컴퓨터 5호기 사용자의 작업별 IO 통계정보 획득 방안**, 2021, `…y2021m11a.6` | ⭐ **어느 언어에서든 누리온 telemetry 아키텍처에 대해 발견된 최상의 기술 세부.** 8,437노드, **33.88 PB** 병렬저장, 100 Gbps Omni-Path, PBS + **DDN ESMON → InfluxDB** |
| 곽재혁, **Performance Co-Pilot, Bpftrace, Grafana 기반 슈퍼컴퓨터 모니터링 및 성능 분석 시스템**, 2021, `…y2021m11a.118` | 모니터링 스택 설계, **fail-slow를 명시적 동기로**("특정 노드의 문제 → 전체 성능 저하") |
| 김성준·이재국·홍태영, **효율적인 배치 작업 정보 관리를 위한 모니터링 시스템 설계**, 2020, `…y2020m11a.178` | ⭐ **모니터링이 스케줄러에 주는 부하**를 다룸: "빈번한 정보 요청은 작업관리 솔루션에 부하를 줄 수 있다" → **F1의 C_agent/C_query에 대한 자기 기관 선행 관측** |
| **클러스터 시스템의 장애 발생 계산노드 자동 복구 기능 구현**, 2024, `…y2024m05a.2` | Neuron(SLURM + crontab) **자동 remediation** → **F4의 자기 기관 선행연구** |
| **GPU 온도 상승에 따른 어플리케이션 성능 저하를 해결하기 위한 자동화된 서버 관리**, 2025, `…y2025m11a.19` | ⭐ **GPU 열 기반 fail-slow + 자동 조치** → **F3의 자기 기관 선행연구** |
| **GPU 클러스터 시스템의 장애 통보 자동화**, 2026, `…y2026m05a.35` | Slurm **Epilog** 기반 GPU 장애 통보, **국가슈퍼컴퓨터 6호기를 명시적 배경으로** |
| 윤준원·송의성, **배치 작업 로그 분석을 통한 스케줄링 최적화 연구**, 디지털콘텐츠학회논문지 18(7):1411–1418, 2017 | 학술지 |

그 외: job별 전력(2020), job별 GPU 통계(2022), 스케줄러 연동 프로파일링 수집(2023).

→ **결론: 어떤 논문에서도 "KISTI가 X를 이전에 하지 않았다"는 주장을 하기 전에 이 목록을 확인해야 한다.** `11` PART C 함정 8의 위험도가 대폭 상승했다.

## 2.9 ⭐ 새 발견 — Sunway 신뢰성 논문이 "예측이 운영적으로 이득이 되는가"에 답한다

**神威太湖之光可靠性及可用性设计与分析**, 计算机研究与发展 58(12):2696–2707, 2021 (전문 수치 추출):
- **MTBF 11.84 h** @ 40,960 프로세서 / 10,649,600 코어
- 장애 귀속: **계산노드 58.92% / 전원 18.60% / 유지보수·진단 12.79%**
- **장애 예측 정확도 약 70%**
- **배포된 예측 + 조치의 실제 성과: 능동 마이그레이션으로 애플리케이션 체감 MTBF 11.84 h → 24.2 h**
- 장애 시간 분포가 **지수분포가 아니라 로그정규분포** — MTBF 기반 추론 전반에 함의

→ **"HPC 장애 예측이 운영적으로 이득이 됨을 보인 사례가 없다"는 어떤 주장도 이 논문과 대면해야 한다.** 그리고 이것은 F4(remediation)의 관련연구에 반드시 들어간다.

**추가 중국어 발견:** **神威超级计算机运行时故障定位方法**(计算机研究与发展 61(1):86–97, 2024) — 신세대 Sunway의 런타임 **RCA/장애 국소화**, *로그 데이터도 명확한 증상도 없는* 장애를 표적으로 한다. **Beacon+**(计算机工程与科学 44(9), 2022, 薛巍/Tsinghua + 何晓斌/NRCPC, NSCC-Wuxi) — **Beacon NSDI'19의 중국어 후속판**, 유일 접근 가능본이 유료. **监控分系统在E级高性能计算机系统中的挑战与设计**(计算机工程与科学 43(8):1366–1375, 2021, NUDT) — exascale 모니터링 서브시스템 아키텍처.

⚠️ **중요한 관찰:** 활발한 중국어 **智能运维**(AIOps) 문헌은 **클라우드/인터넷 서비스 전용**이다. HPC에 智能运维를 적용한 중국어 논문을 찾지 못했다. 중국 HPC 운영 연구는 대신 **可靠性/可用性, 故障定位, 监控分系统** 어휘를 쓴다 — **智能运维만으로 검색하면 이 문헌 전체를 놓친다.**

## 2.10 S-RAPS — C9의 진짜 gate. LC-Opt는 아니었다

> **Maiterth, Dey, Duplyakin, Brewer, Islam, Kabir, Kuruvella, Menear, Patki, Jones (ORNL/TXST/NREL/LLNL/CSU), *"HPC Digital Twins for Evaluating Scheduling Policies, Incentive Structures and their Impact on Power and Cooling"*, SC '25 Workshops, DOI `10.1145/3731599.3767559`, arXiv 2508.20016**

이것이 `12` W-07이 LC-Opt가 했다고 우려한 것을 **실제로** 하며, 그 이상이다: **ExaDigiT의 RAPS를 실제로 확장**하고, **5개 실trace**로 스케줄링 정책·인센티브 구조 what-if를 수행 — Frontier(1,238 job), Marconi100(231,238), Fugaku(116,977), Lassen(1,467,746), Adastra(30,570) — FCFS/SJF/LJF/priority/replay, backfill 변종, ScheduleFlow, FastSim, Fugaku point-score 인센티브 연구.

**그런데 자기 각주가 잔존 gap을 넘겨준다 (verbatim):**
> *"The datasets do not contain reservations and job dependencies, nor was information about down or drained nodes available."*

→ **`08` §2.3의 `actor` 필드 요구사항과 F4의 provenance 주장이 이 문장으로 직접 정당화된다.** 그리고 S-RAPS도 신뢰구간을 보고하지 않는다 — 검증은 정성적(*"can match the observed changes in both utilization and simulated power"*).

**LC-Opt 판정 (V6):** 환경 우선(벤치마크 쪽에 가중). baseline은 본문 표에서 **PPO뿐**, 부록 B에 SAC — TD3/MADDPG/IPPO 없음, offline RL 없음. **행동공간은 냉각 setpoint 전용**(blade-group 밸브 벡터(Dirichlet, 합 1.0), CDU 급수 온도, CDU 유량, 냉각탑 환수 setpoint delta) — 스케줄링·power capping·drain·requeue·remediation 없음, 워크로드는 순수 외생 열 trace. **OPE 없음, counterfactual 추정량 없음, 신뢰구간 없음, seed 수 미기재.** twin 검증은 수치 0의 단순 주장(*"has been validated against the operational dynamics of the Frontier supercomputer's cooling system"*)이며, 부록 H는 4단계 배포 **로드맵**으로 hardware-in-the-loop과 shadow mode를 명시적 future work로 둔다. 노드 건강: 부재.

**→ C9 판정: 물리/냉각 twin은 사실상 닫혔다. 정책 평가 방법론은 `STILL OPEN`(양쪽 모두 손대지 않음). remediation/노드상태 조치 클래스는 `STILL OPEN`.** `10` §4의 C9 `DROP`을 해제하되 **독립 후보로 부활시키지 말고 F4의 하위 구성요소로 흡수**한다(§3.4).

**참고:** **arXiv 2601.02275**(Jadhav & Liu)는 Frontier 냉각 surrogate를 실측 대비 정량화한다 — 0.026 MW MAE, 테스트 표본 98.7%에서 PUE 오차 0.01 이내. LC-Opt가 주장만 한 오차 보고를 실제로 한다. **WANDER**(arXiv 2506.04049, Islam 그룹)는 HPC에 대해 불확실성 순위화된 counterfactual 구성 합성을 한다.

## 2.11 Hindsight — `09`의 특징 규정이 **검증되었고 강화되었다**

전문 확인. `09` §4.3이 "trace이고 binary keep/discard"로 분류한 것이 **정확**하며, 논문 자신이 해상도 축을 명시적으로 부인한다 (verbatim):
> *"Agents do this atomically at the granularity of a trace; there is no point in only dropping part of a trace."*

나이 기반 retention은 있으나 *"event horizon"*(1 GB 버퍼에서 약 1분)을 갖는 **LRU eviction뿐** — rollup 없음, tiering 없음, 점진적 조립화 없음. **절벽이지 gradient가 아니다.** metric은 다루지 않고(trace/span 전용, metric은 `PercentileTrigger` 같은 트리거 술어로만 등장하며 보존되지 않는다), **진단 품질을 평가하지 않으며**(capture rate, 대역폭, 지연/처리량, ns 오버헤드만), ordering/lag의 진단적 처리가 없고, 비용 모델이 **순간적**(7.9–8.6 ns/tracepoint, 지연 <3.5%, 2.6 vs 78 MB/s, 0.3 코어, 1 GB RAM)이며 **storage-over-time이 없다.**

→ **`09`의 서술 유지 + 강화: 논문 자신의 문장으로 해상도 축 부재를 인용할 수 있다.** 후속 연구 중 해상도 차원을 추가한 것: `NOT FOUND`. 최근접 **Trace Sampling 2.0**(arXiv 2509.13852, span 수준) — `TITLE-ONLY`, 읽을 가치 있음.

## 2.12 SeT-Diff — 위협이 아니라 조력자다

"schema permutation invariance"는 운영적으로 **metric 순서(ordering)만** 의미한다 — 위치 인덱스 대신 텍스트 센서 설명의 의미적 조건화를 통해(shuffled 0.0472 vs clean 0.0470 MAE). **renaming 미실증. 상이한 metric 집합은 학습된 261-metric 어휘 내 masking으로만. 상이한 cardinality / 미학습 metric 미실증.** 평가는 **단일 실시스템** — M100 ExaData, Marconi100 20개월, 약 40K window, P=261. **cross-system·cross-generation 실험 없음. schema shift를 독립 손실 원인으로 정량화하지 않는다**(permutation test는 방법의 견고성 확인). 기여는 **방법**(diffusion 아키텍처).

→ **F2에게 유용한 조력자:** 위치 기반 모델이 schema 교란에서 크게 실패한다는 수치를 발표해 준다(**0.154 vs 0.047 MAE, 약 3.3배**). F2의 schema 요인 분해에 인용할 근거다.

## 2.13 ISC 연구트랙 2024–2026 — venue 모델 정정 + 신규 관련 논문 21편

**정정:** ISC 연구논문은 2023년 이후 Springer LNCS를 떠났다. 2024년부터 "ISC High Performance <year> Research Paper Proceedings", **Prometeus GmbH / IEEE**, ISBN 978-3-9826336-0-2 / -1-9 / -2-6, DOI prefix `10.23919/isc.<year>`.
→ ⚠️ **LNCS 기반 census는 0편을 발견하고 트랙이 비었다고 잘못 결론낼 수 있다. `01`/`02`의 ISC 커버리지 서술을 정정할 것.**

**Crossref DOI-prefix 질의로 3개 연도 전량 열거 완료**(dblp TOC는 WebFetch에서 절단됨): **2024 = 24편 중 관련 4편 / 2025 = 28편 중 8편 / 2026 = 35편 중 9편.**

주요 항목: **Refine**(BU/Sandia 이상탐지, LDMS 1 Hz, GPU 없음), **Application-Focused HPC Network Monitoring**(Friese/Marsden/Schulz), **EPIC** 및 **LLM log-mining 논문**(둘 다 ORNL, ISC 2026), **A Dynamic GPU Power Prediction Framework**(BU/NERSC, ISC 2026), **McDaniel 외 GPU/APU 전력 귀속**(§2.5).

## 2.14 워크숍 지도 정정

| 시리즈 | 정정된 사실 |
|---|---|
| **MODA** | **6판, 17 chapter 전량 확인**(LNCS 12321/12761/13387/13999/15058/16091). **다중 rate 오버헤드 연구 0편** |
| **HPCMASPA** | 시리즈 색인에서 **2014–2023 확인**, 2024 추정, **2025 `UNVERIFIED`**. 아카이브이나 접근성 나쁨. **IEEE Cluster 병설** |
| **HPC-ODA** | BoF 시리즈 2019–2025. **최초 peer-reviewed 워크숍판이 SC26**(2026-11, 아직 미개최). 공동조직자에 **Woong Shin(ORNL)** — SC26 표적 논문의 마지막 저자 |
| **LDMSCON** | **2019–2025**(2015 아님). 비아카이브. 슬라이드 일부 온라인이나 2024 일정표가 판독 불가한 Google Drawing 내부 |

## 2.15 SC26 — 프로그램 상태와 표적 논문

**표적 논문 확정 (`SC26-PARTIAL-EVIDENCE`):**
> ***"From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System"*** — Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin (전원 ORNL, 외부 협력자 없음). **Technical Papers, Best Paper Nominee.**

(제목은 두 독립 출처에서 verbatim 동일하며 "in HPC System" 단수·무관사 그대로다.)

**트랙 확인 근거:** SC26 finalists 발표문이 *"Each year, the SC Technical Papers program recognizes outstanding research through its Best Paper and Best Student Paper awards"*라 명시. 깊이 `PROGRAM-METADATA-ONLY (award-list level)` — `sc26.conference-program.com`이 **HTTP 401**(프로그램 사이트 미개방)이라 `Event Type:` 라인으로는 확인 불가.

**내용 관련 모든 질문은 `UNKNOWN`이다.** 초록·preprint·artifact 설명이 공개된 곳이 없다. label 소스, 소스 간 일치도 측정 여부, taxonomy 및 클래스 수, 운영자 확인 인시던트 수, 해상도/샘플링/볼륨 스윕, telemetry 계층 수, offline replay vs online, 공개 artifact — 전부 `UNKNOWN`. **기계 이름(Frontier/Summit)조차 명시되지 않았다.** DOI/페이지 `NOT FOUND`. arXiv/OSTI preprint `NOT FOUND as of 2026-09-06`(부재 증명은 아님).

**제목에서 추론하지 않았다.** 그러나 제목이 licensing하는 어휘적 사실 하나는 지적해야 한다: **"Causal Failure Cascade Discovery"** — cascade는 계층 간 전파 **순서**의 대상이다. **F1의 Q-δ가 다루려는 것이 정확히 cascade order 복원이다.** 이것은 추론이 아니라 어휘의 중첩이며, 위험 평가에 반영해야 한다(§3.1).

**SC26 프로그램 전체:** 채택 Technical Papers 전체 목록은 **비공개**. 공개적으로 열거 가능한 부분집합은 9편의 award finalist뿐이며, 그중 **운영 관련은 표적 논문 1편**이다. 비지명 운영 논문은 현재 보이지 않는다.

**AgenticAI4HPC'26 확인:** SC26의 50개 채택 워크숍 중 하나(43개 "with proceedings" 그룹). 2026-11-15(일) 09:00–12:30. 의장 Mohammad Alaul Haque Monil(ORNL), 공동의장 Pedro Valero-Lara(ORNL), Daichi Mukunoki(Nagoya), Bogdan Nicolae(ANL). **채택 통보가 2026-09-04 — 이틀 전.** 제목·저자 없는 잠정 일정만 공개. 슬롯 산술상 한 자리 수 채택 추정. → **C7 판정 유지(`DROP`), 재확인 시점은 2026-09-18~25.**

⚠️ **혼동 방지:** **AGENT4SC 2026은 eScience 2026이며 SC26이 아니다.** 프로그램은 공개되어 있고 8개 제목 전량 확인 — HPC 운영 agent 벤치마크는 없다(최근접 SPECTRA는 LLM 다중에이전트 시스템 대상).

**결정적 재확인 날짜: 2026-09-16.** SC26 dates 페이지가 "Content/Schedule"을 9/16에 두고, papers 페이지가 *"Day, time, and location for each paper session will be published in the online SC Schedule by September 2026"*라 명시. 이때 `sc26.conference-program.com`이 401을 멈추고 `Event Type:`/`Tracks:` metadata **및 초록**을 노출할 것으로 예상된다. **초록이 §3.1의 판단을 결정한다.**

---

# §3. 순위 재판정

`10_SC_CANDIDATE_RANKING.md`의 F1–F4 + W1을 이번 라운드 증거로 다시 평가한다. **관대하게 평가하지 않았다.**

## 3.1 F1 — Telemetry Policy Optimization: `TOP-CANDIDATE` → **`SC-PLAUSIBLE` (조건부)**

### 무엇이 강화되었는가

- ✅ **retention 해상도 축이 두 개의 독립 문헌에서 각각 생존**(§2.2). DB venue와 FDI가 서로 무관한 이유로 이 축을 비워 두었고, FDI의 경우 **패러다임상 구조적 부재**다(온라인 관측기 존재론에 데이터 나이가 없다). 이전 라운드보다 훨씬 강한 근거
- ✅ **인용 가능한 gap 자백 3건 확보**(Goku PVLDB'24의 age-tiering 기술 후 비용만 평가, Chronix FAST'17의 미측정 주장, Lindorm TSDB의 두 기능 비교차)
- ✅ **비용 축의 미점유 부분이 명확해졌다.** FDI에도 DB에도 **bytes/s·TB-month·query cost가 없고, observer perturbation이 없다**. 검증 보고의 표현: *"the cleanest unclaimed ground in the audit"*
- ✅ **Slingshot switch counter 실증 대상 확보**(§2.7) — 스위치당 64K counter, 전량 0.5초. C_query·C_network의 이상적 측정 대상
- ✅ **Wintermute가 위협이 아니라 근거였다**(§2.5) — GPU가 없으므로 GPU 세대 gap을 강화하고, 동시에 accuracy-vs-rate가 CPU 세대에 존재함을 보여 주어 "해 볼 만한 일"임을 정당화

### 무엇이 약화되었는가

- 🚨 **H1a(ordering/lag 메커니즘)가 novel하지 않다**(§2.1). `09` §12.2가 지정한 "가장 novel한 부분"이 사라졌다
- 🚨 **정보이론적으로 거짓일 수 있다** — non-Gaussian noise 하에서 lag 구조가 subsampled 데이터로부터 식별 가능(Gong ICML'15). **subsampling-aware 추정기 baseline 없이는 결과가 추정기 결함으로 읽힌다**
- 🚨 **비단조성 반례 존재**(Solovyeva CLeaR'23) — 더 느린 측정이 인과 정보를 추가할 수 있다
- 🚨 **연속 통계 품질 축이 죽었다**(§2.3). Eriksson/Krysander/Frisk SAFEPROCESS'12가 시간 변수만 뺀 동형 정식화
- 🚨 **"기존 연구는 센서 개수만 센다"가 거짓**(§2.3) — Sarrate 외 2012의 BILP
- 🚨 **CAMEO(EDBT'26)가 일반형 주장을 깬다**(§2.4). RALF(PVLDB'17)가 실제 VM telemetry에서 방법론을 선점
- 🚨 **Tuncer ISC'17의 산문 한 문장이 약하게 불리하다**(§2.6) — 1 s → 5 s에서 *"negligible"*
- 🚨 **SC26 ORNL이 "Causal Failure **Cascade** Discovery"다**(§2.15). Q-δ의 대상과 어휘가 중첩. Best Paper nominee이므로 가시성이 최대

### 생존하는 주장 — 이번이 세 번째 재정의다

`09` §12가 "탐지≠진단"에서 "정책 최적화"로 옮겼다. 이제 한 번 더 옮겨야 한다.

> **F1의 주장:** *실제 다계층 HPC production telemetry에서, cross-layer cascade order 복원이 붕괴하는 **retention 해상도 문턱**을 **비용인식적으로** 정량화하고, 그로부터 도출되는 **retention 정책 설계점**을 제시한다.*
>
> **명시적으로 채택(자기 것이라 주장하지 않음):** Plis & Danks UAI'15 / Gong & Zhang ICML'15 / Gong UAI'17 — 메커니즘. AWStream SIGCOMM'18 — frontier formulation. Eriksson/Krysander/Frisk SAFEPROCESS'12 — 제약 최소화 형태와 연속 진단품질. Sarrate 외 2012 — 비용 정식화. CAMEO EDBT'26 — 축소-대-탐지 곡선.
>
> **F1의 delta 4개:** (i) **retention/age를 1급 결정변수로**(양 문헌 공백), (ii) **데이터 볼륨 비용**(bytes/s, TB-month, query cost — 양 문헌 공백), (iii) **observer perturbation을 비용 항으로**(양 문헌 공백, HPC 고유), (iv) **해석적 모델 없는 경험적 정식화**(§2.3의 정밀한 문구로).

### 판정

**`SC-PLAUSIBLE`, 두 조건부.**
1. **SC26 ORNL 초록 확인 후에만 착수**(2026-09-16 예상). 그 논문이 cascade order 복원을 telemetry 해상도와 함께 다뤘다면 F1은 폐기 또는 전면 재정의다
2. **subsampling-aware 추정기 baseline 확보** — 없으면 결과가 방어되지 않는다

**그럼에도 착수하지 말아야 할 가장 강한 이유 (개정):**
> 이 후보는 **세 번 재정의되었고 매 라운드마다 헤드라인을 잃었다.** 남은 것은 "메커니즘은 남의 것, formulation도 남의 것, 우리 것은 비용 축과 실제 데이터"다. 그것으로 SC 본트랙이 되려면 **비용 측정이 논문의 중심**이어야 하고, 비용 측정은 12개월 전해상도 아카이브 + 수락시험 실험 창 + 두 시스템을 요구한다. 리드타임은 여전히 가장 길고, 이제 **선점 위험이 가장 큰 후보이기도 하다.**

## 3.2 F2 — Cross-Generation Transfer 측정: **`SC-PLAUSIBLE` 유지, 상대 순위 상승**

### 이번 라운드의 순효과: **긍정**

- ✅ **CENTILE은 위협이 아니었다**(§1.1). cross-generation을 하지 않고, 원인 분해를 하지 않으며, 전이를 penalty가 아니라 gain으로 보고한다. **재프레이밍 `SUFFICIENT`**
- ✅ **SeT-Diff는 조력자다**(§2.12). 위치 기반 모델이 schema 교란에서 3.3배 악화된다는 수치를 발표해 준다 — F2의 schema 요인 분해에 직접 인용
- ✅ **데이터 리드타임 0이라는 유일한 구조적 우위 유지.** 그리고 §2.8의 KISTI 국내 문헌이 누리온 telemetry 아키텍처를 문서화해 두었다(33.88 PB, DDN ESMON→InfluxDB) — cross-generation 쌍의 구시스템 측 schema 문서가 이미 존재한다는 뜻
- ⚠️ **새 위협 1건: ModelX(HPDC 2025), DOI `10.1145/3731545.3731593`, LLNL-CONF-870385, *"ModelX: A Novel Transfer Learning Approach Across Heterogeneous Datasets"*** — `TITLE-ONLY`. 접근 전량 실패(ACM DL 403, HPDC 슬라이드 robots/TLS, OSTI robots, Crossref 429). **CENTILE보다 F2에 더 위협적일 수 있다. `12`의 최우선 미해결 항목으로 승격**

### 판정

**`SC-PLAUSIBLE` 유지. 그러나 F1이 강등되었으므로 상대 순위는 사실상 공동 1위이며, 실행 순서상으로는 명확히 1순위다.**

**그럼에도 착수하지 말아야 할 가장 강한 이유 (개정):**
> **ModelX를 읽지 않은 상태다.** LLNL의 heterogeneous-dataset 전이 논문이 HPDC 2025에 있고 제목만 아는 상태에서 F2를 시작하면, 관련연구를 쓸 때 그것이 F2의 기여를 이미 포함하고 있음을 발견할 수 있다. **ModelX 확보가 F2 착수의 전제조건이다.** 그리고 N=1 per generation이라는 근본 제약은 그대로다.

## 3.3 F3 — Label Semantics + Fail-slow: **순위 유지, 위험 구조가 바뀌었다**

### 강화

- ✅ **최강 feasibility 반론 약화**(§2.7). Slingshot switch counter는 확보 가능하며, 제약은 조회 비용이다. 네트워크 원인 클래스 붕괴 위험이 낮아졌다
- ✅ **CUG 2023 Barry 외**가 GPU + Redfish + Slingshot NIC/switch sampler가 한 시스템에 공존하는 실증을 제공(El Capitan/Perlmutter) — 다계층 수집이 가능함의 근거
- ✅ **자기 기관 선행연구 확보**(§2.8) — 2025년 GPU 열 기반 fail-slow + 자동 조치, 2024년 자동 복구. 국제 논문에서 "우리 센터에서 이미 이 문제를 다뤘다"고 쓸 수 있는 근거

### 약화

- 🚨 **SC26 ORNL 위험이 이제 구체적이다.** 제목이 *"From Alert **Fatigue** to Root Cause"*이며 alert fatigue는 정의상 알람 스트림 품질에서 출발한다. 그리고 저자 6명 전원 ORNL로, 알람·Slurm 상태·health check·티켓에 동시 접근하는 정확히 그 그룹이다. **다만 내용은 `UNKNOWN`이며, causal-cascade 논문이 단일 label 소스를 쓰고 소스 간 일치도를 계산하지 않는 것이 오히려 일반적인 경우다.** 판정: **`CANNOT DETERMINE` — 양보하지도, 무시하지도 말 것**
- ⚠️ **HPC-ODA 2026의 공동조직자가 Woong Shin(ORNL)**이며 그는 표적 논문의 마지막 저자다. ORNL이 이 공간을 커뮤니티 차원에서 조직하고 있다

### 판정

**`SC-STRETCH` 유지(C4+C5 병합 상태에서). 착수는 2026-09-16 이후.**

**그럼에도 착수하지 말아야 할 가장 강한 이유 (개정):**
> **ORNL이 이 공간을 논문·워크숍 양쪽에서 동시에 점유하고 있다.** Best Paper nominee 논문 한 편과 신설 워크숍 공동조직이 같은 저자에게서 나왔다. F3로 들어가면 그들이 정의한 프레임 안에서 후발로 경쟁하게 된다. 9월 16일 초록이 label 소스 일치도를 언급하면 즉시 폐기해야 한다.

## 3.4 F4 — Remediation 비용모델 + OPE: **소폭 상승, C9 흡수**

### 강화

- ✅ **S-RAPS의 자체 각주가 F4의 데이터 요구사항을 정당화한다**(§2.10, verbatim): *"The datasets do not contain reservations and job dependencies, nor was information about down or drained nodes available."* → **`08` §2.3의 `actor` 필드 요구가 공개 문헌의 인정된 공백으로 뒷받침된다**
- ✅ **정책 평가 방법론이 LC-Opt와 S-RAPS 양쪽에서 `STILL OPEN`**(§2.10). 둘 다 신뢰구간을 보고하지 않고, OPE도 counterfactual 추정량도 없다. LC-Opt의 twin 검증은 수치 0의 주장이다
- ✅ **C9을 하위 구성요소로 흡수**하면 F4의 범위가 "조치 클래스 + OPE + provenance"에서 "**운영 정책의 counterfactual 평가 방법론 일반**"으로 넓어지고, remediation은 그 중 하나의 조치 클래스가 된다. 이 프레이밍이 더 강하다
- ✅ **Sunway 신뢰성 논문**(§2.9)이 예측+조치의 운영적 이득을 실증(MTBF 11.84→24.2 h) — F4의 동기 절에 강력한 근거
- ✅ **자기 기관 선행연구**: 2024년 Neuron 자동 복구(§2.8)
- ⚠️ **Jadhav & Liu(arXiv 2601.02275)**가 Frontier 냉각 surrogate의 오차를 실측 보고(0.026 MW MAE, PUE 오차 0.01 이내 98.7%) — twin 오차 보고의 기준선이 생겼다. F4가 신뢰구간을 낸다면 비교 대상

### 판정

**`SC-STRETCH` (조건부) 유지 — 그러나 `10` §3의 "독립 후보로 유지하지 말 것" 권고를 **철회**한다.** C9 흡수 후 F4는 다음 형태로 독립 후보 자격이 있다:

> **F4′:** *HPC 운영 정책(remediation을 포함한 조치 클래스)의 counterfactual 평가 방법론 — behavior policy provenance를 갖춘 production 이력에서 형식적 OPE(DR/IPS)와 신뢰구간을 산출하고, node-hour로 환원되지 않는 조치 비용(큐 위치 손실, fairshare charge-back, reservation 단편화)을 모델링한다.*

**여전히 `actor_type` 필드(`08` P-2)가 없으면 존재하지 않는다.** 그러나 이제 그 필드의 필요성이 S-RAPS의 각주로 외부 근거를 얻었다.

**그럼에도 착수하지 말아야 할 가장 강한 이유 (개정):**
> **12개월 리드타임 + HPDC'24가 여전히 비용모델의 세 요소를 갖고 있다.** 강화된 것은 provenance/OPE 방법론 쪽이고 그것은 "방법론 기여"로 읽히기 쉬워 SC 본트랙에서 약하다. HPDC/ICPP/Cluster가 정직한 목표다.

## 3.5 W1 — 유지

변경 없음. HPC-ODA의 최초 peer-reviewed 판이 **SC26(2026-11)**임이 확인되었으므로(§2.14), `10`이 권고한 "2027년 판"이 실제로는 **2회차**가 된다. 제출 시점은 2027년 중반 예상. 목표 유지.

## 3.6 개정 순위표

| 순위 | 후보 | 판정 | 이번 라운드 변화 | 착수 조건 |
|---|---|---|---|---|
| **1 (실행)** | **F2** Cross-generation 전이 측정 | `SC-PLAUSIBLE` | ↑ CENTILE 위협 해소, SeT-Diff 조력, 리드타임 0 | **ModelX(HPDC'25) 확보·독해** |
| **1 (강도, 조건부)** | **F1** Telemetry policy / retention 문턱 | `SC-PLAUSIBLE` | ↓ H1a falsified, 품질축 주장 철회, 선점위험 최대 / ↑ retention 축 이중 확인 | **SC26 ORNL 초록**(2026-09-16) + subsampling-aware baseline |
| **3** | **F3** Label semantics + fail-slow | `SC-STRETCH` | ↑ Slingshot feasibility 개선, 자기 선행연구 확보 / ↓ ORNL 선점 위험 구체화 | **SC26 ORNL 초록** |
| **4** | **F4′** 운영 정책 counterfactual 평가(C9 흡수) | `SC-STRETCH` (조건부) | ↑ S-RAPS 각주가 데이터 요구를 정당화, C9의 방법론 공간 확인 | `actor_type` 12개월 축적 |
| **W** | **W1** 효율 리포팅 행동 효과 | 워크숍 | — | staggered rollout 설계 |
| — | C3 / C7 | `DROP` 유지 | C7은 AgenticAI4HPC 채택목록(2026-09-18~25) 재확인 | — |

**핵심 변화 한 문장:** **F1이 여전히 가장 비어 있는 땅을 갖고 있으나, 이제 가장 위험한 후보이기도 하다. F2가 확실성에서 앞선다.**

---

# §4. `08`–`12`에 적용할 정정

## 4.1 문서별 정정표

| 문서 | 위치 | 정정 |
|---|---|---|
| `08` | §2.1(a) fabric 행 | ⚠️ "Slingshot switch counter 확보 불가 위험"을 **"확보는 가능하나 조회 비용이 크다"**로 교체(§2.7). 계약 명시 요구는 **유지**하되 사유를 "접근 거부 방지"에서 "**조회 rate·counter 부분집합·전용 접근 경로의 명시**"로 변경 |
| `08` | §2.1(b) C_query 행 | "어디에도 없는 항"에 **DB venue 스윕과 FDI 스윕 양쪽에서 확인**을 근거로 추가(§2.2). 그리고 **스위치당 64K counter / 전량 0.5초**를 구체적 측정 대상으로 명기 |
| `08` | §2.1(c) | Reveal(arXiv 2510.26008), McDaniel ISC'26, Wintermute HPDC'20을 **비교 대상 선례**로 추가. 특히 **McDaniel의 "below 1%"와 Reveal의 "1.2–1.4% @100 ms → <0.6% @600 ms"를 목표 정밀도 기준선으로** |
| `08` | §2.3(a) | `actor` 필드 요구에 **S-RAPS(SC'25 Workshops) 각주를 외부 근거로 인용** 추가(§2.10) |
| `08` | §2.4 | schema 이력 요구에 **SeT-Diff의 0.154 vs 0.047 MAE(3.3배)**를 근거로 추가(§2.12). 그리고 **누리온 측 schema 문서가 KIPS 2021 논문에 이미 있다**는 사실(§2.8) |
| `08` | §4.3 T2 | Hindsight 비교에 **논문 자신의 부인 문구**를 인용(§2.11) — *"there is no point in only dropping part of a trace"*. 차별점이 논문 자체 문장으로 확보됨 |
| `08` | §4.4 | 4개 점검 항목 중 **1(DB 스윕) 완료 / 2(PIKA) 완료 / 3(Tuncer) 완료 / 4(Hindsight) 완료**. 신규 항목으로 **ModelX(HPDC'25)**와 **SC26 ORNL 초록** 추가 |
| `09` | §0.1 | 인용 오류 목록에 **§1.1(CENTILE 서술·인용 오류), §1.2(TelemetrySuffBench 수치 조건 누락), §1.3(Rosich 단독저자), §1.4(LC-Opt "ExaDigiT 기반" 표현), §1.5(PIKA 워크숍)** 5건 추가 |
| `09` | §4.1 HIT 1 | TelemetrySuffBench 수치를 **조건과 함께** 재기술(§1.2). 그리고 대상이 **LLM 에이전트 trace**임을 명기 |
| `09` | §4.1 HIT 2 | Rosich 단독저자 정정. **Eriksson/Krysander/Frisk SAFEPROCESS'12를 더 강한 적대 인용으로 추가**(§2.3) |
| `09` | §4.3 | ✅ **판정 유지 및 강화.** DB venue 스윕 완료 결과(§2.2)와 FDI 스윕 결과를 근거로 추가. near-miss 표에 **CAMEO(EDBT'26), RALF(PVLDB'17), Goku(PVLDB'24), Chronix(FAST'17), Lindorm TSDB**를 추가. **Monarch/Gorilla/ModelarDB/Timon의 `UNVERIFIED`를 전문 확인 음성으로 승격.** ByteSeries·TimeUnion은 `TITLE-ONLY` 유지 |
| `09` | §4.3 "in ANY field" | **최종 문구 확정:** *"metrics store의 retention/rollup 정책에 대해서는, 그리고 FDI/model-based diagnosis 문헌에서도"*. Miao 2023 / Zhong 2011은 `UNVERIFIED` 유지 |
| `09` | §4.5 | Wintermute를 **위협에서 근거로 이동**(GPU 없음, accuracy-vs-rate 있음). ExaMon **종결(막다른 길)**. PIKA **종결(워크숍, rate 스윕 없음, 오버헤드 정성적)**. **신규 위협 3건 추가: Reveal, McDaniel ISC'26, Barry CUG'23**. 최종 문구를 §2.5의 "두 개의 겹치지 않는 집합"으로 교체 |
| `09` | §4.5 미해결위험 표 | 1(PIKA) 해소 / 2(Tuncer) 해소 / 3(DB 스윕) 해소 / 4(grey lit) 부분 해소 — **LDMSCON 2023–2025 튜토리얼 번들만 잔존** / 5(Hindsight) 해소 |
| `09` | §4.6 | 5개 하위주장 판정 갱신: #1 **HPC 한정 SURVIVES 유지** + CAMEO/RALF 추가로 문구 강화 필요 / #2 FALSIFIED 유지 + Tuncer ISC'17 산문 추가 / #3 **✅ 최강 생존 — 이중 확인** / #4 FALSIFIED 유지 + Reveal 추가 / #5 FALSIFIED 유지 |
| `09` | §6.3 | 🚨 **CENTILE 인용 문구 삭제 또는 `MISATTRIBUTED` 표시**(§1.1). CENTILE의 실제 성격으로 서술 교체. **SeT-Diff를 위협에서 조력자로 이동**. **ModelX를 신규 최강 위협으로 추가** |
| `09` | §8.1 ② | PIKA를 **"IEEE Cluster 2020 proceedings에 수록된 HPCMASPA 2020 워크숍 논문"**으로 정정(§1.5). HPCMASPA/MODA 병설 학회 정정 |
| `09` | §9 | KISTI 선행연구를 **16편 → 23편(KISTI 저자 20편)**으로 갱신(§2.8). **약 9편은 영어판 없음**을 과소계수 원인으로 명기 |
| `09` | §10.2 | 사각지대 갱신: **ICDE 2015–2026이 최대 미탐색 영역으로 확정**(IEEE Xplore 403, 공개 proceedings 없음, 미러 없음). **discrete-event systems diagnosability(Sampath/Lafortune 계보)** 신규 사각지대 추가 — bounded-delay diagnosability가 δ 지연 제약에 가장 가깝다 |
| `09` | §10.3 | 언어권 커버리지 갱신(§4.2). **한국어 moderate-to-strong, 일본어 moderate(facility)/weak(SIGHPC), 중국어 weak** |
| `09` | §11 C1 | §3.1로 교체 |
| `09` | §11 C2 | ModelX 위협 추가, CENTILE 위협 하향 |
| `09` | §11 C5 | **feasibility 반론 약화 반영**(§2.7) |
| `09` | §11 C6 | S-RAPS 각주 추가, C9 흡수 반영(§3.4) |
| `09` | §11 C7 | AgenticAI4HPC 채택 통보 2026-09-04, 재확인 시점 2026-09-18~25. AGENT4SC≠SC26 명기 |
| `09` | §11 C9 | **LC-Opt가 gate가 아니었음**을 정정. **S-RAPS가 진짜 gate**. 방법론 공간은 `STILL OPEN` → F4′로 흡수 |
| `09` | §11 C10 | 변경 없음 |
| `09` | §12.1 | 🚨 **"Rosich에 없는 것" 4개 중 3번(연속 통계 품질) 삭제**(§2.3). 비용 주장을 "센서 개수만 센다"에서 **"데이터 볼륨 비용과 observer perturbation이 없다"**로 교체. 4번(모델 요구)의 문구를 §2.3의 정밀한 형태로 교체 |
| `09` | §12.2 | 🚨 **Q-δ를 "가장 novel한 부분"에서 강등**(§2.1). 4개 질문 중 Q-δ의 근거를 "미발견"에서 **"메커니즘은 확립되어 있고, 실제 telemetry·비용축·운영점이 없다"**로 교체 |
| `09` | §12.3 | 인용 목록에 추가: **Plis & Danks UAI'15, Gong & Zhang ICML'15, Gong UAI'17, Solovyeva CLeaR'23, Hyttinen 외 2016, Eriksson 외 Automatica'13, Eriksson/Krysander/Frisk SAFEPROCESS'12, Sarrate 외 2012, Jung 외 SAFEPROCESS'15, Jung & Axelsson DX'24, Frisk/Krysander/Jung IFAC'17, CAMEO EDBT'26, RALF PVLDB'17, Goku PVLDB'24, Chronix FAST'17, Lindorm TSDB PVLDB'23, Reveal arXiv 2510.26008, McDaniel ISC'26, Barry CUG'23, S-RAPS SC'25W, LC-Opt NeurIPS'25, Sunway 可靠性 2021** |
| `10` | 전체 | §3의 개정 순위로 교체. 비교표의 Novelty·데이터·실현성 점수 갱신 |
| `10` | §3 4위 항목 | **"F4를 독립 후보로 유지하지 말 것" 권고 철회**(§3.4). C9 흡수 후 F4′로 재정의 |
| `10` | §4 | C9의 `DROP` 사유를 LC-Opt에서 **S-RAPS**로 교체하고, 방법론 공간이 열려 있음을 명기 |
| `10` | §5 | 실행 배치 갱신: **2026-09-16 SC26 초록 확인이 F1·F3의 착수 게이트**. F2는 ModelX 확보 후 즉시 |
| `11` | §1.1 | H1a의 지위를 "novelty의 핵심"에서 **"채택하는 기존 메커니즘"**으로 강등. 새 novelty 진술은 §3.1 |
| `11` | §1.7 | 🚨 **B7 신규 추가: subsampling-aware 인과 추정기**(Plis/Danks/Hyttinen 계열, non-Gaussian 식별성 활용). **이 baseline 없이는 결과가 방어되지 않는다.** 그리고 B5(ordering 보존 요약) vs B7의 대비가 새로운 심장 |
| `11` | §1.8 | 해상도-품질 곡선의 **단조성을 가정하지 말 것**(Solovyeva CLeaR'23). 비단조 구간의 존재 자체를 결과로 보고할 준비 |
| `11` | §1.11 | **F1-K8 신규**: *subsampling-aware 추정기가 나이브 추정기의 손실을 대부분 복구한다 → H1a가 추정기 결함이었음 → 폐기 또는 "실용 추정기 하의 손실"로 대폭 축소.* **F1-K9 신규**: *SC26 ORNL 논문이 cascade order 복원을 telemetry 해상도와 함께 다뤘다 → 폐기.* F1-K6·K7은 **해소됨**으로 표시(반례 없음, 단 ICDE 미탐색) |
| `11` | §1.12 | 예상 심사 비판 1번을 **Plis/Danks·Gong/Zhang으로 교체**(FDI보다 이 쪽이 더 정확하고 더 치명적). Eriksson SAFEPROCESS'12를 2번으로 승격. CAMEO·RALF 추가 |
| `11` | §2.5 | B5(CENTILE adapter) 설명을 §1.1의 실제 성격으로 교체. **B8 신규: ModelX 계열**(확보 후) |
| `11` | §2.9 | **F2-K6 신규**: *ModelX가 이미 세대/이질 데이터셋 간 손실 분해를 한다 → 폐기 또는 재정의* |
| `11` | §3.2 | Slingshot switch counter 요구를 **"확보 가능, 조회 비용 설계 필요"**로 완화(§2.7) |
| `11` | §3.9 | **F3-K5를 구체화**: SC26 ORNL 논문의 label 소스 처리. 확인 시점 2026-09-16 |
| `11` | PART C | 함정 8(KISTI 자기 선행연구)의 목록을 §2.8의 23편으로 확장. **함정 11 신규: ISC 2024–2026을 LNCS로 찾으면 0편이 나온다**(§2.13) |
| `12` | W-01 | **해소.** `NO COUNTEREXAMPLE FOUND IN THIS SWEEP`. 단 **ICDE 2015–2026 미탐색이 최대 잔존 구멍**으로 승격 |
| `12` | W-02 | **부분 해소.** 제목·저자·트랙 확정, 내용 전량 `UNKNOWN`. 재확인 **2026-09-16** |
| `12` | W-03, W-04 | **해소** |
| `12` | W-06 | **해소** |
| `12` | W-07 | **해소, 그러나 대상 교체** — 진짜 gate는 S-RAPS |
| `12` | W-08, W-09 | **해소** |
| `12` | W-10 | **해소** (ID 정확, 수치 조건 정정) |
| `12` | W-12, W-13 | **해소** (Wintermute는 근거, ExaMon은 막다른 길) |
| `12` | W-14 | **부분 해소** — 2019–2025로 정정. **2023–2025 튜토리얼 번들 잔존** |
| `12` | W-15 | **부분 해소** — Slingshot counter 가용성 확보. **CUG 2026, "The HPE Slingshot 400 Expedition" 잔존** |
| `12` | W-19 | **해소.** venue 모델 정정 + 24/28/35편 전량 열거 |
| `12` | W-20 | **부분 해소** — 개최 확정, 채택 통보 2026-09-04, 목록 비공개 |
| `12` | W-21~W-23 | **부분 해소** — §4.2의 커버리지 판정 |
| `12` | 신규 | **W-30 ModelX(HPDC'25)** 최우선. **W-31 SC26 ORNL 초록** 최우선. **W-32 ICDE 2015–2026**. **W-33 discrete-event systems diagnosability**. **W-34 Beacon+ 전문**. **W-35 HPE Slingshot admin guide "Telemetry Metrics and Counters"**. **W-36 LDMSCON 2023–2025 튜토리얼**. **W-37 KISTI TRKO 내부보고서 + KIISE/KIPS Transactions**. **W-38 Eriksson SAFEPROCESS'12 원문**(현재 인용은 학위논문의 자기요약) |

## 4.2 언어권 커버리지 — 최종 방어 가능 문구

| 언어 | 커버리지 | 방어 가능한 문구 |
|---|---|---|
| **한국어** | **moderate-to-strong** | *"KoreaScience 경유로 KIPS 연차학술대회 논문집 12개 호를 연도별로 전수 스윕(2019 추계 → 2026 춘계; 2021 춘계는 5xx 실패, 2018 이전 미시도)하고 ScienceON/KCI/DBpia를 표적 검색하여 한국어 23건(KISTI 저자 20건)을 확인했다. KIISE 논문집, KISS 전용 학술지, KIPS Transactions, KISTI TRKO 보고서는 검색하지 못했다."* — **"한국어 문헌에 X가 없다"는 절대 쓰지 말 것** |
| **일본어** | **facility/utilisation moderate, SIGHPC weak** | *"J-STAGE를 정상 검색했고(진성 음성), IPSJ SIGHPC 研究報告는 J-STAGE에 수록되지 않으며 두 접근 경로 모두 robots 차단으로 약 45개 연구회 중 6개만 표본화했다."* — **IPSJ SIGHPC에 관해 부재를 주장할 수 없다** |
| **중국어** | **weak — 부재 미확립** | *"표본 조사이며 전수 조사가 아니다. 모든 집계 색인(CNKI CAPTCHA, Wanfang·CQVIP 미도달)이 실패했고 5건 모두 출판사 사이트 경유 기회적 발견이다. 중국어 문헌에 대한 어떤 부재 주장도 지지되지 않는다."* — 단 **"智能运维 문헌은 클라우드/인터넷 서비스 전용이며 HPC 적용 사례를 찾지 못했다"**는 안전하게 진술 가능 |

**신뢰도 순위: 한국어 > 일본어 > 중국어.**

⚠️ **검색 함정 기록:** DBpia의 search endpoint는 JS shell을 반환하며, **누리온 관련 논문이 실제로 존재함에도 "총 0건"을 보고했다.** 따라서 **DBpia 검색의 모든 0건 결과는 폐기했고 음성 증거로 사용하지 않았다.** 같은 함정이 다른 국내 포털에도 있을 수 있다.

## 4.3 방법론 교훈 — 다음 라운드를 위한 도구 지식

| 항목 | 내용 |
|---|---|
| `vldb.org/pvldb/volumes/NN/` | ⚠️ **front matter만 있고 논문 제목이 없다.** 이전 가정이 틀렸다. PVLDB 열거는 키워드 기반이 될 수밖에 없으며 **전수가 아니다** |
| dblp 페이지 + WebFetch | ⚠️ **긴 목록을 조용히 절단한다.** vol-16이 Lindorm TSDB·TSM-Bench·Blink-hash를 포함함을 아는데도 1건만 반환. **대형 TOC는 좁은 질문으로 여러 번 나눠 fetch할 것** |
| **Crossref DOI-prefix 질의** | ✅ **회의 전수 열거의 최선 경로.** ISC 2024–2026을 이 방법으로 완전 열거했다(dblp TOC 절단 우회) |
| 신뢰 가능 | openproceedings.org(EDBT), usenix.org, arxiv.org(특히 `/html/`), proceedings.neurips.cc, openreview.net(리뷰가 논문의 한계를 명시), cug.org, link.springer.com(volume TOC), koreascience.kr, crad.ict.ac.cn, joces.nudt.edu.cn, J-STAGE, DiVA(LiU) |
| 차단 | ACM DL 403, IEEE Xplore 403, ICDE 전량, ScienceON robots, KCI robots, CiNii robots, IPSJ digital library robots, CNKI CAPTCHA, ResearchGate 429, core.ac.uk robots, OSTI robots, ORCID robots |
| Springer 302 | 쿠키 오류 쿼리 문자열을 붙여 302 대상에 재발행하면 동작 |

---

# §5. 다음 행동 — 우선순위

| 우선 | 행동 | 마감 | 무엇을 결정하는가 |
|---|---|---|---|
| **1** | **ModelX(HPDC 2025) 확보·독해** — DOI `10.1145/3731545.3731593`, LLNL-CONF-870385. KISTI의 ACM DL 기관 접근으로 즉시 가능 | 즉시 | **F2 착수 가능 여부** |
| **2** | **SC26 프로그램 재확인** — `sc26.conference-program.com` 401 해제 및 초록 공개 | **2026-09-16** | **F1·F3 착수 가능 여부.** 이번 라운드가 남긴 최대 미결 |
| **3** | **KISTI 내부 문의** — TRKO 기술보고서, 누리온 운영 분석 미공개 결과, 이미 시도해 실패한 것. §2.8의 23편 저자들이 사내에 있다 | 즉시 | 모든 후보의 자기 선행연구 완전성 |
| **4** | **PIKA 전문 확보** — IEEE Xplore 기관 접근(pp. 424–432). Q3(정량 오버헤드 수치 존재 여부)만 미해결 | 1주 | `08` §2.1(c)의 목표 정밀도 |
| **5** | **AgenticAI4HPC'26 채택 목록** | **2026-09-18~25** | C7 영구 폐기 여부 |
| **6** | **ICDE 2015–2026 스윕** — 기관 IEEE Xplore 접근으로만 가능. F1의 최대 잔존 문헌 리스크 | 1개월 | F1의 retention 축 최종 확정 |
| **7** | **discrete-event systems diagnosability(Sampath/Lafortune)** — bounded-delay diagnosability가 δ 제약에 가장 가깝다. 검증 보고가 *"the most likely remaining source of a surprise"*로 지목 | 1개월 | F1의 formulation 방어선 |
| **8** | **Eriksson/Krysander/Frisk SAFEPROCESS'12 원문** — 현재 인용은 학위논문의 자기요약. 관련연구 작성 전 필수 | 1개월 | F1의 related work 정확성 |
| **9** | **Beacon+ 전문**(计算机工程与科学 44(9), 2022) — 계층별 설계·데이터 볼륨·샘플링·오버헤드 수치가 가장 필요한 대상 | 1개월 | F1의 비용 축 비교 기준선 |
| **10** | **LDMSCON 2023–2025 튜토리얼 번들** — GPU 세대 다중 rate 오버헤드 발표가 남아 있을 가장 유력한 장소. 비아카이브이므로 검색 누락이 약한 증거임에 유의 | 2개월 | `08` §2.1(c) |

---

# §6. 정직한 자기평가

1. **`09`가 한 라운드 만에 여러 항목에서 뒤집혔다.** 이것은 감사 체계가 작동한다는 뜻이지만, 동시에 **현재의 `13`도 다음 라운드에서 뒤집힐 수 있다**는 뜻이다. 특히 ICDE와 discrete-event systems가 미탐색이다
2. **F1은 세 번 재정의되었다.** "탐지≠진단" → "정책 최적화" → "retention 문턱의 비용인식 정량화". 매번 좁아졌다. **네 번째 축소가 필요해지면 그것은 후보가 아니라 논문 한 절이라는 신호로 읽어야 한다**
3. **CENTILE 인용 오류는 `09`에서 발생한 것이다.** 1차 조사의 인용 오류 3건을 `09`가 잡았는데, `09` 자신이 새 인용 오류를 만들었다. **metadata 수준 확인만으로 문헌을 특징 규정하면 안 된다**는 교훈이 반복 확인되었다
4. **`12`가 "가장 저비용·고위험"으로 지목한 W-05(국내·내부)가 정확히 그랬다.** 23편이 나왔고 9편은 영어판이 없었다. **아직 KISTI 내부 보고서는 손도 대지 않았다** — 이것이 남은 최대 자기 선행연구 리스크다
5. **ORNL의 위치를 과소평가했을 가능성이 있다.** Best Paper nominee 논문 + 신설 워크숍 공동조직 + ISC 2026의 EPIC 및 LLM log-mining 논문 2편이 모두 같은 기관에서 나온다. **F1·F3 둘 다 ORNL과 같은 공간에 있다.** 협업 가능성을 적대 경쟁의 대안으로 검토할 가치가 있다
6. **F2가 1순위로 올라간 것은 F2가 강해졌기 때문이 아니라 F1이 약해졌기 때문이다.** F2의 절대 강도는 변하지 않았고 ModelX라는 미확인 위협이 있다. 이 순위는 확실성 기준의 순위이며 잠재력 기준의 순위가 아니다

---

**연결 문서:** `09`(감사, §4.1의 정정 적용 후), `10`(순위, §3으로 교체), `11`(실험, §4.1의 baseline·폐기기준 추가 후), `12`(watchlist, §4.1의 해소·신규 항목 반영 후), `08`(보존 요구사항, §4.1의 정정 적용 후).
**원천 증거:** `raw/V1`–`V8`.

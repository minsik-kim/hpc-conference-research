> ## ⚠️ 정정 고지 (2026-09-06 2차 검증 후 추가)
>
> **`13_VERIFICATION_ROUND2.md`가 이 문서의 여러 주장을 정정·강등·강화했다. 이 문서보다 `13`이 우선한다.**
> 특히:
> - **인용 오류 5건 추가 발견** — CENTILE의 성격·인용 문구(`13` §1.1, **삭제 필요**), TelemetrySuffBench 수치의 조건 누락(§1.2), Rosich 단독저자(§1.3), LC-Opt "ExaDigiT 기반" 표현(§1.4), PIKA는 HPCMASPA 워크숍 논문(§1.5)
> - **H1a(ordering/lag 메커니즘) FALSIFIED** — Plis & Danks UAI'15, Gong & Zhang ICML'15가 정리로 확립(`13` §2.1)
> - **연속 통계 진단 품질 축 DEAD** — Eriksson/Krysander/Frisk SAFEPROCESS'12가 동형 정식화(`13` §2.3)
> - ✅ **retention 해상도 축은 DB venue·FDI 양쪽에서 독립 재확인 — 강화됨**(`13` §2.2)
> - **SC26 ORNL 논문 확정**: *"From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System"*, Technical Papers **Best Paper Nominee**(`13` §2.15)
> - **KISTI 국내 선행연구 16편 → 23편**(`13` §2.8)
> - **순위 개정**: F1 `TOP-CANDIDATE` → `SC-PLAUSIBLE`(조건부), F2가 실행 1순위(`13` §3)
> - **문서별 정정표는 `13` §4.1**

# 10. SC CANDIDATE RANKING
## 10개 후보 → 최종 4개 + 워크숍 진입용 1개

> **문서 지위:** `06_INITIAL_SC_RESEARCH_CANDIDATES.md`의 후보 C1–C10을 `09_ADVERSARIAL_NOVELTY_AUDIT.md` §11의 심사자 관점 판정으로 압축한 결과.
> **원칙:** 후보를 많이 살려두지 않는다. 살려둔 후보에는 각각 **"그럼에도 착수하지 말아야 할 가장 강한 이유"**를 붙인다.
> **SC를 목표로 한다는 이유로 관대하게 평가하지 않았다.** 10개 중 6개를 잘라냈다.

---

# §1. 압축 결과 — 무엇을 자르고 무엇을 합쳤는가

| 원 후보 | `09` §11 판정 | 최종 처분 | 근거 |
|---|---|---|---|
| C1 Telemetry 축소의 탐지–진단 비대칭 | `TOP-CANDIDATE` (재정의 조건부) | → **F1**(재정의, C10 흡수) | 헤드라인 가설은 falsified(`09` §4.1). retention 해상도 축만 무조건 생존(§4.3) |
| C10 Telemetry integrity / observability debt | `WORKSHOP-LEVEL` 단독 | → **F1에 흡수** | `09` §11 C10: "C1의 필수 구성요소". 단독 기여 부족 |
| C2 세대 간 telemetry 전이 손실 | `SC-PLAUSIBLE` | → **F2** | KISTI cross-generation 쌍이 구조적 우위. 단 측정/벤치마크 기여로 재프레이밍 필수 |
| C4 운영 label semantics 측정 | `SC-STRETCH` (C5 결합 시 `SC-PLAUSIBLE`) | → **F3**(C5와 병합) | `09` §11 C4가 명시적으로 결합을 권고 |
| C5 내재적 fail-slow vs 유발 간섭 판별 | `SC-STRETCH` | → **F3**(C4와 병합) | 단독으로는 ARGUS·Kaleidoscope·Tuncer 3중 압박. label 기여와 결합해야 방어선이 생긴다 |
| C6 Remediation 비용모델 + OPE | `SC-STRETCH` (조건부) | → **F4**, **조건부 보류** | `actor_type` 필드 확보 시에만 존재. `08` §0 P-2 |
| C8 job 효율 리포팅의 행동 효과 | `WORKSHOP-LEVEL` | → **W1**(워크숍 진입용, SC 후보 아님) | 알고리즘 기여 없음. 그러나 **첫 논문으로 최적** |
| C3 Backfill silent-defect screening | `SC-STRETCH` (강등됨) | **DROP** | SuperBench(ATC'24 Best Paper)가 비용 예산 하 검증 스케줄 최적화를 이미 함. Meta RSC가 FP 회계를 발표. 차별점이 자원 모델(backfill vs 전용 창) 하나에 걸려 있고 그것은 좁다 |
| C7 HPC 운영 agent 벤치마크 | `KEEP-WATCHING` | **DROP (2026년 기준)** | ground truth가 F3에 종속. 도메인 이식 반론 강함. **AgenticAI4HPC'26(SC26 1회차)이 lane을 선점** → 2027 착수는 이미 늦음. F3 완료 후 재검토 |
| C9 운영 정책 counterfactual 평가 | `KEEP-WATCHING` | **DROP (자료 확보 전 착수 금지)** | ExaDigiT SC24 → **LC-Opt(NeurIPS'25)**로 인접 공간이 채워지기 시작. LC-Opt 전문 확보·독해 전 착수 금지 |

**최종: SC 후보 4개(F1–F4, 중 F4는 조건부) + 워크숍 진입 1개(W1).**

---

# §2. 비교표

| | **F1** Telemetry Policy Optimization | **F2** Cross-Generation Transfer 측정 | **F3** 운영 Label Semantics + Fail-slow 판별 | **F4** Remediation 비용모델 + OPE |
|---|---|---|---|---|
| **Novelty** | **4/5** — retention 해상도 축이 무조건 생존(`09` §4.3). Q-δ(lag/ordering 손실)는 어느 분야에서도 미발견. 단 formulation은 AWStream에서 채택해야 함 | **3/5** — CENTILE·SeT-Diff·Farooq가 방법 공간을 채웠다. 생존 주장은 **transfer matrix의 off-diagonal 측정**으로 축소 | **3/5** — 방법(weak supervision, PU learning) 전부 닫힘. 생존은 **"label이란 무엇인가"의 측정 프로토콜** + 원인 taxonomy | **2/5** — 비용모델 핵심 주장 falsified(HPDC'24). CMDP+FRR+blast radius도 선점(arXiv 2607.20005). 생존은 조치 클래스·OPE 형식성·provenance 3개 |
| **운영 중요도** | **5/5** — 저장·수집 예산이 실제 의사결정 사안. 결과가 곧 운영 정책 | **3/5** — 세대 교체 시점에만 강하게 관련. 그러나 그 시점이 지금이다 | **5/5** — 오탐/미탐이 매일의 비용. 원인 판별 부재가 최대 운영 통증 | **4/5** — 오조치의 실제 비용이 크다. 단 현재는 사람이 처리 중 |
| **데이터 확보 가능성** | **2/5 → 4/5** — 현재 없음. `08` P-1 시행 시 12개월 후 4/5. **가장 큰 리드타임** | **4/5** — 구시스템 아카이브 보존 시 즉시. + 공개 데이터셋 2종 | **3/5** — 티켓/RMA는 행정 승인 필요. 원인 taxonomy는 지금 정의 가능. **Slingshot switch counter가 관문** | **1/5 → 3/5** — `actor_type` 없으면 0. 있으면 12개월 축적 필요 |
| **실험 실현성** | **3/5** — replay로 Pareto frontier 가능. 그러나 비용 항은 실측 필요(수락시험 창 의존) | **4/5** — 순수 소급 분석. production 실험 불필요 | **2/5** — 운영자 판정 시간을 산다. label 수 확보가 병목(기준선 843건) | **2/5** — tier-0에서 drain A/B 불가. 시뮬레이션은 HPDC'20이 이미 점유 |
| **일반화 가능성** | **4/5** — 정책 최적화 프레임은 사이트 독립. 2개 시스템만 있으면 주장 성립 | **2/5** — N=1 per generation. 표준 domain adaptation 가정 붕괴 | **3/5** — 프로토콜과 taxonomy는 이전 가능. 결과 수치는 사이트 특이적 | **3/5** — 조치 클래스 비용 모델은 Slurm 사이트 전반 적용 |
| **SC 적합성** | **4/5** — 시스템 설계 + 정량 평가 + 운영 함의. SC 본트랙 폼에 정확히 맞음 | **3/5** — 측정/벤치마크 논문. SC는 받으나 "메커니즘 없음" 반론에 노출 | **3/5** — 측정 프로토콜 논문. Kaleidoscope SC'20 선례가 있어 폼은 존재 | **2/5** — HPDC/ICPP/Cluster 적합. SC 본트랙은 무리 |
| **최대 위험** | **전해상도 데이터 리드타임.** 그리고 VLDB/SIGMOD retention 스윕 미검색(`08` §4.4) | **CENTILE·SeT-Diff에 의한 novelty 침식**, schema 정렬 노동이 연구의 대부분을 차지 | **SC26 ORNL "From Alert Fatigue to Root Cause"**가 정확히 이 공간일 수 있음(`09` §5.7) | **`actor_type` 부재 시 후보 자체 소멸** |
| **종합** | **1위** | **2위** | **3위** | **4위 (조건부)** |

**W1 (워크숍 진입용, SC 후보 아님):** job 효율 리포팅의 사용자 행동 효과. Novelty 2/5, 데이터 4/5, 실현성 5/5, SC 적합성 1/5. **HPC-ODA 2027 또는 MODA 대상.**

---

# §3. 순위와 근거

## 1위 — F1. Telemetry Policy Optimization (retention 해상도 중심)

**한 줄:** 다계층 HPC telemetry에서 정책 π = {metric, sampling rate, **retention 해상도(나이의 함수)**}를 결정변수로 두고, 비용(수집기·네트워크·저장·쿼리·**애플리케이션 교란**) 대 운영 품질(탐지 정확도·탐지 지연·국소화·**RCA**)의 Pareto frontier를 측정·최적화한다.

**왜 1위인가:**
1. **조사 전체에서 무조건 생존한 유일한 축을 포함한다.** `09` §4.6: 5개 하위주장 중 retention 해상도만 전역 생존. 다른 세 후보는 모두 부분 falsified 상태에서 좁혀서 생존한 것이다
2. **Q-δ가 메커니즘적으로 방어 가능하다.** RCA는 lag/ordering 구조에 의존하고(Granger, cross-correlation, cascade 순서) downsampling이 정확히 그것을 파괴한다. HPC에서는 cascade가 fabric topology와 OST map을 따라 **물리적으로** 전파되므로 lag 구조가 물리적으로 참이다. AWStream·FDI·TelemetrySuffBench 어느 것도 이 메커니즘을 다루지 않는다
3. **운영 결정과 논문이 같은 산출물이다.** 한강 telemetry 설계가 곧 실험이다. 다른 후보는 운영을 위해 하는 일과 논문을 위해 하는 일이 다르다
4. **C10을 흡수하면 서론이 자연스럽다** — "얼마나 줄일 수 있는가" 전에 "지금 무엇을 놓치고 있는가"

**그럼에도 착수하지 말아야 할 가장 강한 이유:**
> **데이터가 없다. 그리고 데이터를 만드는 데 12개월이 걸린다.** 전해상도 다계층 코퍼스는 `08` P-1을 지금 시행해도 2027년 하반기에야 12개월 분량이 된다. 그 사이 **VLDB/SIGMOD/ICDE/EDBT/CIDR의 retention·rollup 스윕**(미검색 최대 영역)에서 반례가 나오면 축의 중심이 사라진다. 즉 **가장 긴 리드타임과 가장 큰 미검증 리스크가 결합**되어 있다. 착수 결정 전에 DB 문헌 스윕을 반드시 완료할 것.

**착수 전 필수 조건:** (a) `08` P-1 시행 결정, (b) 수락시험에 교란 측정 매트릭스 포함, (c) VLDB/SIGMOD 스윕 완료, (d) PIKA CLUSTER'20 PDF 확인.

---

## 2위 — F2. Cross-Generation Telemetry Transfer 측정

**한 줄:** 동일 기관의 서로 다른 세대 시스템 간에 운영 이상탐지/진단 모델이 이전될 때의 성능 손실을 **shift 원인별로 분해**하고(하드웨어 세대 / schema / workload mix / 스케줄러 정책), transfer-penalty matrix를 공개 artifact로 낸다.

**왜 2위인가:**
1. **데이터가 이미 있다.** 구시스템 아카이브를 보존하기만 하면 즉시 시작 가능. 4개 후보 중 유일하게 리드타임이 0
2. **KISTI의 구조적 우위가 실재한다.** 동일 기관·동일 운영팀·동일 사용자 커뮤니티의 세대 쌍은 흔하지 않다. 대부분의 transfer 연구는 서로 다른 기관의 공개 데이터셋 조합이며, 그 경우 confound가 훨씬 많다
3. **F1의 리드타임을 메우는 배치로 최적** — F1 데이터가 쌓이는 동안 F2를 진행하면 시간 손실이 없다

**그럼에도 착수하지 말아야 할 가장 강한 이유:**
> **novelty가 계속 침식되고 있다.** CENTILE(arXiv 2608.01725)이 cross-domain 전이 + adapter를, SeT-Diff(CF'26)가 schema permutation invariance를, Farooq ESWA 2026이 tier-0 실세계 federated transfer를 이미 발표했다. 2026년 중에 발표되는 논문 한 편이 이 후보를 `DROP`으로 만들 수 있다. 그리고 **N=1 per generation**이라는 근본 제약 때문에 통계적 주장의 강도에 상한이 있다. 심사자가 *"세대가 2개인데 무엇을 일반화하는가"*라고 물으면 답이 약하다.

**필수 재프레이밍:** 메커니즘 기여가 아니라 **측정/벤치마크 기여**로. transfer-penalty matrix 자체가 산출물이어야 한다. adapter를 제안하면 CENTILE에 정면으로 진다.

---

## 3위 — F3. 운영 Label Semantics + Fail-slow 원인 판별 (C4+C5 병합)

**한 줄:** HPC 운영에서 "장애 label"이 무엇인지를 복수 독립 소스(알람 / drain reason / health check / 티켓 / RMA)의 일치도로 **측정**하고, 그 위에서 내재적 fail-slow와 이웃 job에 의한 유발 간섭을 판별하는 원인 taxonomy를 세우고 평가한다.

**왜 3위인가:**
1. **운영 통증이 가장 크다.** 8개 센터가 독립적으로 명명한 pain point와 직결
2. **병합이 실제로 방어선을 만든다.** C5 단독은 ARGUS(1만 GPU 6개월)·Kaleidoscope(843 label, SC'20)·Tuncer(TPDS'19)에 3중으로 눌린다. 그러나 *"그들이 사용한 label 자체가 무엇인지 아무도 측정하지 않았다"*는 것은 그 논문들이 답하지 않은 질문이다
3. **원인 taxonomy는 지금 정의해야 하는 운영 산출물**이므로 F1과 마찬가지로 운영·연구가 같은 작업

**그럼에도 착수하지 말아야 할 가장 강한 이유:**
> **SC26 ORNL "From Alert Fatigue to Root Cause"가 정확히 이 공간일 가능성이 있다.** `09` §5.7에서 이 논문은 `SC26-PARTIAL-EVIDENCE` 상태이며 내용을 알 수 없다. 제목만으로 판단하면 alert → root cause 파이프라인이고, ORNL은 Frontier 규모의 label과 checknode 이력을 갖고 있다. **만약 그 논문이 label 소스 간 불일치를 측정했다면 F3의 novelty 절반이 사라진다.** 그리고 두 번째 이유: `09` §11 C5의 feasibility 반론 — **Slingshot switch counter를 확보하지 못하면 네트워크 원인 클래스가 붕괴**하고, 그러면 taxonomy가 3–4 클래스로 줄어 워크숍 수준이 된다.

**착수 전 필수 조건:** SC26 ORNL 논문 전문 확인(2026년 9월 말–10월 프로그램 공개 시점). 그 전에 F3에 인력을 배정하지 말 것.

---

## 4위 (조건부) — F4. Remediation 조치 비용모델 + Off-policy 평가

**한 줄:** 자동 remediation(drain/requeue/reboot/유지)의 비용을 node-hour를 넘어선 조치 클래스(큐 위치 손실, fairshare charge-back, reservation 단편화)로 확장하고, `actor` provenance를 갖춘 과거 이력에서 형식적 off-policy 평가(DR/IPS + 신뢰구간)를 수행한다.

**왜 4위인가:** 핵심 novelty 주장이 이미 falsified되었다. `09` §7.1: HPDC'24 BSC가 비용 모델의 세 요소를 모두 갖췄고(54% 감소, Oracle 대비 6% 이내), arXiv 2607.20005이 CMDP + FRR budget + blast radius/reversibility/epistemic 분해 + abstention-as-action을 선점했다. 남은 것은 조치 클래스 확장, OPE 형식성, provenance 3개이며 **provenance가 가장 논쟁이 적다**(기존 인용으로 거부할 수 없다).

**그럼에도 착수하지 말아야 할 가장 강한 이유:**
> **후보가 존재하지 않을 수 있다.** `actor_type` 필드(`08` P-2)가 없으면 behavior policy를 재구성할 수 없고 OPE는 정의되지 않는다. `09` §11 C6의 판정이 명시적으로 *"actor 필드 확보 시. 없으면 `DROP`하고 F3 절로 접을 것"*이다. 그리고 확보해도 12개월 축적이 필요하다. **즉 F1과 같은 리드타임에 F1보다 약한 novelty.** 합리적 처분은 SC 후보로 두지 않고 **`08` P-2를 시행해 두고 F3의 한 절로 흡수, 2028년에 재평가**하는 것이다.

**권고:** F4를 독립 후보로 유지하지 말 것. **`08` P-2만 시행하고 후보 목록에서는 대기 상태로 둘 것.** 데이터가 쌓인 뒤 HPDC/ICPP 대상으로 재검토.

---

## W1 (워크숍 진입) — job 효율 리포팅의 사용자 행동 효과

**왜 목록에 남기는가:** SC 후보가 아니지만 **첫 논문으로 최적**이다. 데이터 확보 4/5, 실험 실현성 5/5, feasibility 반론 없음. 그리고 `09` §8.3의 발견 — 실무와 연구를 잇는 다리는 워크숍 논문이 아니라 **데이터셋**이지만, 워크숍 논문은 **연구 그룹의 존재를 커뮤니티에 등록하는 기능**을 한다. F1/F3의 심사에서 "이 그룹이 누구인가"가 이미 알려져 있는 것은 실질적 이득이다.

**주의:** HPC-ODA 2026 제출 마감(2026-08-12)은 이미 지났다. **2027년 판이 목표.** MODA도 대안.

**그럼에도 착수하지 말아야 할 가장 강한 이유:**
> 알고리즘 기여가 없어서 SC로 올라가지 않으며, **단일 센터·대조군 없음으로 진행하면 워크숍에서도 약하다.** staggered rollout을 설계에 넣지 않으면 인과 주장을 할 수 없고, 그러면 "우리 센터에서 리포팅을 시작했다"는 경험 보고가 된다. 그 상태로 낼 가치는 없다.

---

# §4. 잘라낸 후보 — 다시 열릴 조건

| 후보 | 처분 | 다시 열릴 조건 |
|---|---|---|
| **C3** Backfill screening | DROP | ORNL의 negative baseline(주간 39,437회 무수확)을 **사전 예측**하는 방법이 있고, backfill 자원 모델이 SuperBench의 전용 창과 근본적으로 다름을 정량화할 수 있을 때 |
| **C7** 운영 agent 벤치마크 | DROP (2026) | F3의 ground truth 코퍼스가 완성되고, AgenticAI4HPC'26의 결과물을 확인한 뒤. **비용 제한 evidence collection**(F1과 연결)이 중심이 되어야 함 |
| **C9** 정책 counterfactual | DROP (자료 대기) | **LC-Opt(NeurIPS'25) 전문 확보·독해 후.** 그것이 채운 공간을 정확히 알기 전에는 판단 불가 |
| **C6** → F4 | 조건부 대기 | `actor_type` 12개월 축적 완료 시 |

---

# §5. 실행 배치 권고

**시간 축의 제약이 순위보다 강하다.** F1이 1위이지만 데이터가 12개월 뒤에 생긴다. 따라서:

| 시기 | 활동 | 산출물 |
|---|---|---|
| **즉시 (2026 H2)** | `08` P-1·P-2 시행 결정. 계약·수락시험 항목 반영. 원인 taxonomy 정의. **VLDB/SIGMOD retention 스윕**. SC26 프로그램 공개 시 ORNL 논문 확인 | 데이터 파이프라인 + F1/F3 착수 가능 여부 판정 |
| **2026 H2–2027 H1** | **F2 착수**(데이터 이미 있음). 병행하여 W1 설계(staggered rollout 포함) | F2 논문(2027 SC 또는 Cluster/ICPP), W1(HPC-ODA 2027) |
| **2027 H1** | F1 데이터 6개월 축적 시점에 **예비 실험**(§`11` E1-a) 수행하여 Q-δ 효과 크기 확인 | 계속/폐기 판정 |
| **2027 H2–2028** | F1 본 실험. F3은 SC26 ORNL 결과에 따라 착수 또는 재정의 | F1 논문(2028 SC 목표) |
| **2028+** | F4 재평가 | — |

**중요:** F1을 1위로 두고 F2를 먼저 실행하는 것은 모순이 아니다. F1의 병목은 우선순위가 아니라 데이터 리드타임이며, 그 시간을 F2가 채운다.

---

# §6. 이 순위가 틀릴 수 있는 지점

정직하게 기록한다.

1. **F1의 retention 축이 DB 문헌에 이미 있을 수 있다.** VLDB/SIGMOD/ICDE/EDBT/CIDR 미검색은 `09` §4.3이 명시한 "남은 최대 구멍"이다. 여기서 반례가 나오면 순위 전체가 바뀐다
2. **SC26 ORNL 논문이 F3뿐 아니라 F1의 일부도 덮을 수 있다.** alert fatigue → root cause 파이프라인이 telemetry 감축을 다뤘다면
3. **F2의 novelty는 2026년 안에 사라질 수 있다.** 가장 빠르게 침식되는 후보다. 지금 시작하는 것이 유일한 방어
4. **W1을 과소평가했을 수 있다.** `09` §8.3의 "다리는 데이터셋"이 맞다면, W1과 함께 **데이터셋 릴리스**를 하는 것이 F1–F4의 어느 논문보다 커뮤니티 영향이 클 수 있다. 단 그것은 SC 정규 논문이 아니다
5. **F4를 너무 빨리 접었을 수 있다.** provenance/accountability 주장은 기존 인용으로 거부되지 않는다(`09` §7.4). 만약 감사·설명책임이 정책적으로 중요해지면(자동 조치에 대한 기관 책임) 이 후보의 운영 중요도가 급상승한다

---

**연결 문서:** `09` §11(원 판정), `09` §12(F1 정식화), `08`(각 후보의 데이터 전제), `11_INITIAL_EXPERIMENT_DESIGNS.md`(F1·F2·F3의 첫 실험), `12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md`(§6의 위험 항목 추적).

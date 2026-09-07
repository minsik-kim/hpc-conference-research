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

# 12. UNRESOLVED EVIDENCE AND WATCHLIST
## 아직 확보하지 못한 중요 자료 — 그리고 각각이 무엇을 죽일 수 있는가

> **문서 지위:** `09_ADVERSARIAL_NOVELTY_AUDIT.md` §10.2(새로 발견된 사각지대)·§10.3(검색 한계)와 §4.5(미해결 위험)를 실행 가능한 추적 목록으로 정리한 것.
> **각 항목 7필드:** 제목 / venue / 예상 공개 시점 / 왜 중요한가 / 어떤 후보를 무효화할 수 있는가 / 현재 확보한 증거 / 확보되면 무엇을 확인해야 하는가
> **원칙:** 이 목록의 항목들은 **추측으로 채우지 않았다.** 내용을 알 수 없는 것은 알 수 없다고 적었다.
>
> **후보 코드는 `10_SC_CANDIDATE_RANKING.md` 기준:** F1(telemetry policy) · F2(cross-generation) · F3(label semantics + fail-slow) · F4(remediation OPE, 조건부) · W1(효율 리포팅).

---

# §0. 우선순위 요약

| 우선 | 항목 | 위험 대상 | 마감 성격 |
|---|---|---|---|
| **1** | VLDB/SIGMOD/ICDE/EDBT/CIDR retention·rollup 스윕 | **F1 중심축** | 착수 전 필수. 문헌 작업이므로 지금 가능 |
| **2** | SC26 ORNL *From Alert Fatigue to Root Cause* | **F3 절반, F1 일부** | 2026년 9월 말–11월(SC26 프로그램/proceedings) |
| **3** | PIKA IEEE Cluster 2020 전문 | F1의 GPU 교란 gap | 지금 가능(유료/기관 접근) |
| **4** | Tuncer 외 TPDS 2019 전문 | F1의 HPC rate 민감도 주장 | 지금 가능 |
| **5** | LC-Opt (NeurIPS 2025) 전문 | C9 재개 판단 | 지금 가능 |
| **6** | 국내(KISS/RISS/DBpia/ScienceON/KSC) + KISTI 내부 기술보고서 | **모든 후보의 자기 선행연구 누락 위험** | 지금 가능. **가장 저비용·고위험** |
| **7** | Hindsight (NSDI 2023) 전문 | F1의 positioning | 지금 가능 |
| **8** | CENTILE / SeT-Diff / TelemetrySuffBench 전문 | F2, F1 | 지금 가능(arXiv) |
| **9** | 중국어·일본어 색인(CNKI/Wanfang, J-STAGE/CiNii/IPSJ) | F1·F3의 zero-claim | 지금 가능 |
| **10** | Wintermute HPDC'20, ExaMon DATE'17, LDMSCON, CUG monitoring track | F1의 GPU 교란 gap | 지금 가능(grey literature) |

---

# §1. 최우선 5건 — 상세

## W-01. 시계열 DB의 retention / rollup 정책과 하류 분석 품질

| 필드 | 내용 |
|---|---|
| **제목/대상** | 특정 논문이 아니라 **문헌 영역**. Monarch(Google), Gorilla(Facebook), ByteSeries, TimeUnion, ModelarDB, Timon 등 TSDB 논문 + rollup/downsampling 정책 논문 일반 |
| **Venue** | VLDB / PVLDB / SIGMOD / ICDE / EDBT / CIDR |
| **예상 공개 시점** | 이미 발표되어 있음. **미검색** |
| **왜 중요한가** | `09` §4.3이 명시한 **"남은 최대 구멍"**. retention 해상도를 결정변수로 다루고 하류 분석 품질을 평가한 논문이 이 영역에 있으면, 조사 전체에서 무조건 생존한 유일한 novelty 축이 사라진다 |
| **무효화 대상** | **F1 전체.** F1이 1위인 유일한 이유가 이 축이다 |
| **현재 증거** | Crossref 제목 탐침 2회(`downsampling anomaly detection time series` 25건, `multi-resolution rollup retention time series database monitoring metrics` 25건) 모두 해당 0건. 검색 결과는 벤더 블로그(ClickHouse, Last9, Alibaba, VictoriaMetrics)만. **DB venue 색인 직접 접근 불가로 `UNVERIFIED`**. 기억 수준의 판단: 위 TSDB 논문들은 rollup 메커니즘을 *기술*하지만 하류 분석 품질을 *평가*하지는 않는다 — **이 판단이 검증되지 않았다** |
| **확보 시 확인할 것** | ① rollup/retention이 **결정변수**로 변화되었는가(단순 기술이 아니라) ② 평가 대상이 **하류 분석 품질**인가(복원 오차·쿼리 지연이 아니라) ③ anomaly detection 또는 diagnosis/RCA를 평가했는가 ④ 비용 축(저장·쿼리)과 함께 다뤘는가. **①②③이 모두 예인 논문이 있으면 F1 폐기(F1-K6)** |
| **실행 방법** | DBLP venue 페이지 → 연도별 제목 스캔(VLDB 2015–2026, SIGMOD 2015–2026). Crossref `container-title` 필터 질의. 키워드: rollup, downsampling, retention, resolution, aggregation, tiering, multi-resolution, lossy + monitoring/observability/anomaly |

## W-02. SC26 — ORNL *From Alert Fatigue to Root Cause*

| 필드 | 내용 |
|---|---|
| **제목** | *From Alert Fatigue to Root Cause* (정확한 부제 미확인) |
| **Venue** | SC26 (SC26 Technical Papers, ORNL) |
| **예상 공개 시점** | SC26 프로그램 상세 공개 시점(통상 9–10월), proceedings는 회의 개최 시점 |
| **왜 중요한가** | 제목이 alert → root cause 파이프라인을 가리키며, ORNL은 Frontier 규모의 알람·drain·checknode 이력과 운영자 판정을 보유한다. **F3가 겨냥한 공간과 직접 겹칠 가능성이 있다** |
| **무효화 대상** | **F3의 절반 이상.** 만약 label 소스 간 불일치를 측정했다면 F3의 핵심 기여가 소멸. 만약 telemetry 감축을 다뤘다면 **F1의 일부**도 위험 |
| **현재 증거** | `09` §5.7에서 **`SC26-PARTIAL-EVIDENCE`**로 분류. 제목과 기관 외에 확인된 것이 없다. **내용을 추측하지 않았다** |
| **확보 시 확인할 것** | ① label의 출처와 정의 — 단일 소스인가 복수 소스 결합인가 ② **소스 간 일치도를 측정했는가**(측정했다면 F3-K5) ③ 원인 taxonomy가 있는가, 몇 클래스인가 ④ 운영자 확인 label 수 ⑤ telemetry 해상도·감축을 다뤘는가 ⑥ 계층 수 ⑦ 평가가 offline replay인가 online인가 ⑧ 공개 artifact 여부 |
| **실행 방법** | `sc26.conference-program.com`에서 Event Type: Paper 및 세션 Tracks 확인(`09` §2.2의 방법 재사용). ORNL 기관 해시 `16969005850305409037`. OSTI(ORNL 논문은 통상 OSTI에 등재), 저자 개인 페이지, arXiv 사전공개 확인 |
| **비고** | **F3에 인력을 배정하기 전에 이 항목이 해소되어야 한다**(`10` §3) |

## W-03. PIKA — IEEE Cluster 2020 전문

| 필드 | 내용 |
|---|---|
| **제목** | PIKA 창립 논문 (TU Dresden) |
| **Venue** | IEEE Cluster 2020, DOI `10.1109/cluster49012.2020.00061` |
| **예상 공개 시점** | 발표 완료. Unpaywall `oa_status: closed` — 기관 구독 필요 |
| **왜 중요한가** | **TU Dresden Taurus에는 GPU 파티션이 있었다.** 이 논문이 1개 이상의 수집 rate에서 GPU 모니터링 오버헤드를 보고했다면, `09` §4.5의 "GPU 세대 교란 측정 gap"이 죽는다 |
| **무효화 대상** | **F1의 C_perturb 차별점 (ii)** — AWStream 대비 delta의 하나. F1 전체는 아니나 비용 축이 크게 약화 |
| **현재 증거** | metadata만 확인. `09` §8.1에서 **PIKA가 아카이브 정규 논문을 갖고 있다**는 사실 자체가 census의 오류를 정정한 항목. 오버헤드 표의 존재 여부는 `UNKNOWN` |
| **확보 시 확인할 것** | ① 수집 rate가 몇 종인가(단일이면 위험 없음) ② GPU metric을 수집했는가 ③ **애플리케이션 교란(런타임 증가)을 측정했는가** ④ 측정 규모(노드 수) ⑤ 품질 축을 함께 평가했는가(했다면 더 심각) |
| **실행 방법** | IEEE Xplore(기관 접근), TU Dresden 기관 리포지터리, 저자 개인 페이지, ResearchGate 저자 업로드본. MODA23의 PIKA 후속 논문에 인용된 수치로 간접 확인도 가능 |

## W-04. Tuncer 외 — TPDS 2019 전문

| 필드 | 내용 |
|---|---|
| **제목** | HPC 시스템 anomaly의 지도학습 분류 (정확한 제목은 `02` 참조) |
| **Venue** | IEEE TPDS 2019 |
| **예상 공개 시점** | 발표 완료 |
| **왜 중요한가** | 이 논문에 민감도 연구가 있는데, 그것이 *aggregation window 크기*가 아니라 **sampling interval**을 변화시킨 것이라면 `09` §1.3 C-08(HPC에 rate 민감도 사례 없음)이 크게 약화된다 |
| **무효화 대상** | F1의 "HPC에서 샘플링 간격을 변화시키며 하류 품질을 측정한 논문이 없다"는 주장. **retention 축은 살아남지만** 서론의 논거가 약해진다 |
| **현재 증거** | 민감도 연구의 **존재는 확인**, 변화시킨 변수가 window인지 interval인지 **미확인** |
| **확보 시 확인할 것** | ① 변화시킨 변수의 정확한 정의 ② 몇 수준인가 ③ 평가한 품질이 탐지인가 분류인가 ④ 비용 축이 있는가(거의 확실히 없음) ⑤ GPU가 있는가(거의 확실히 없음) |
| **실행 방법** | IEEE Xplore, 저자(Tuncer/Coskun) 개인 페이지, BU 리포지터리, arXiv 사전공개본 |

## W-05. 국내 문헌 및 KISTI 내부 기술보고서

| 필드 | 내용 |
|---|---|
| **대상** | KISS / RISS / DBpia / ScienceON / 한국정보과학회(KSC·KCC) 논문지 + **KISTI 내부 기술보고서·연차보고서·과제 결과보고서** |
| **Venue** | 국내 학술지·학술대회 + 비공개/준공개 기관 문서 |
| **예상 공개 시점** | 대부분 이미 존재. **전혀 검색되지 않았다** |
| **왜 중요한가** | `09` §9에서 이미 **16편의 KISTI 국내 선행연구**를 발견했고, 그 중 K-3(Shim 2026, Scientific Reports, `10.1038/s41598-026-42625-6`)은 L6/L7에 도달한다. 국제 색인만으로 이만큼 나왔다는 것은 **국내 색인과 내부 보고서에 더 있을 가능성이 높다**는 의미다. 누리온 운영 분석의 미공개 결과가 가장 있을 법한 장소 |
| **무효화 대상** | **모든 후보.** 특히 자기 기관 선행연구를 누락한 채 SC에 제출하는 것이 심사에서 가장 나쁘게 읽힌다(`11` PART C 함정 8). F2는 특히 위험 — 누리온 cross-generation 분석이 이미 내부적으로 되어 있을 수 있다 |
| **현재 증거** | `09` §9의 K-1..K-16(국제 색인 경유). 국내 색인·내부 문서는 **미탐색** |
| **확보 시 확인할 것** | ① 누리온/GPU 클러스터 telemetry 분석 결과물 ② 장애 예측·이상탐지 시도와 그 결과(부정 결과 포함) ③ 수집 아키텍처 설계 문서와 당시의 rate/retention 결정 근거 ④ 운영 통계(장애율, drain 이력, 티켓 통계) ⑤ **이미 시도했고 실패한 것** — 이것이 가장 가치 있다 |
| **실행 방법** | 기관 내부 문서 조회는 검색이 아니라 **동료·부서 문의**로 해결된다. 운영팀·이전 과제 참여자 인터뷰가 문헌 검색보다 효율적. 국내 색인은 ScienceON부터 |
| **비고** | **가장 저비용이고 가장 위험이 큰 항목.** 다른 모든 항목보다 먼저 해도 된다 |

---

# §2. 문헌 확보 목록 — 확보 가능하나 미확보

| # | 대상 | Venue / ID | 왜 중요한가 | 무효화 대상 | 현재 증거 | 확보 시 확인할 것 |
|---|---|---|---|---|---|---|
| W-06 | **Hindsight** | NSDI 2023 | 발표된 "retention as decision variable"의 최근접. F1의 positioning이 여기에 달려 있다 | F1의 novelty 범위(폐기는 아님) | `09` §4.3에서 "trace이고 binary keep/discard"로 분류. **전문 미확인** | ① 해상도 차원이 있는가(있으면 위험) ② metric에 적용 가능한 형태인가 ③ 소급 pin의 구현이 `08` §4.3 T2와 얼마나 겹치는가 |
| W-07 | **LC-Opt** | NeurIPS 2025 | ExaDigiT SC24 위에 RL 벤치마크를 세운 것으로 파악. C9의 인접 공간을 채웠다 | C9(현재 DROP). 재개 판단의 유일 근거 | `09` §8.2 lineage 6에서 발견. 전문 미확인 | ① 정책 평가 방법론을 다루는가 ② twin의 오차 막대를 어떻게 처리했는가 ③ HPC 운영 정책(스케줄링·remediation)까지 포함하는가 |
| W-08 | **CENTILE** | arXiv 2608.01725 | F2의 최강 반례 | **F2** | metadata + 요약 수준. `09` §6.3에 인용 문구 확보 | ① 평가 대상 시스템이 실제 HPC인가 ② cross-generation을 다루는가 아니면 cross-domain만인가 ③ 손실 **분해**를 하는가(하면 F2 치명) |
| W-09 | **SeT-Diff** | CF 2026 | schema permutation invariance — F2의 schema 요인을 선점 가능 | F2의 schema 분해 | metadata 수준 | ① schema shift를 정량화하는가 ② 실제 운영 telemetry인가 |
| W-10 | **TelemetrySuffBench** | arXiv 2608.07899 | F1의 헤드라인 가설을 제목에 걸고 실증한 논문 | F1의 H1(단 H1a는 무관) | `09` §4.1 HIT 1: 탐지 F1 99.5–100% vs origin-step 정확도 ≤0.5%, **합성 데이터, 비용 축 없음** — 요약 수준 확인 | ① 정확히 합성인가(실데이터가 있으면 위험) ② **시간 해상도를 변화시켰는가**(했으면 F1 치명) ③ lag/ordering을 다루는가(다뤘으면 H1a 소멸) ④ 비용 축이 정말 없는가 |
| W-11 | **arXiv 2607.20005** | arXiv | CMDP + FRR budget + blast radius/reversibility/epistemic + abstention-as-action을 선점 | **F4** | `09` §7.1에서 metadata·요약 확인 | ① HPC 대상인가 ② 실배포 평가가 있는가 ③ 조치 클래스가 몇 개인가 |
| W-12 | **Wintermute** | HPDC 2020 | GPU 오버헤드-rate 표가 숨어 있을 수 있는 곳 | F1의 GPU 교란 gap | `09` §4.5 위험 4순위 | rate 변화 여부, GPU 포함 여부, 교란 측정 여부 |
| W-13 | **ExaMon** | DATE 2017 + 후속 | 동일 | 동일 | 동일 | 동일 |
| W-14 | **LDMSCON 2015–2025** | 비아카이브 컨퍼런스 | LDMS 계열의 rate/오버헤드 실측이 있을 정확한 장소 | F1의 "DCDB SC'19 이후 없음" 주장 | `09` §4.5 위험 4순위. 발표자료 접근성 불확실 | GPU 세대에서의 rate별 오버헤드 표 |
| W-15 | **CUG monitoring track 2020–2026** | CUG(비peer-review 다수) | 동일 + Slingshot telemetry 실무 정보 | F1, F3(switch counter 접근성) | `04` §5에 일부 확보. **전수 아님** | Slingshot counter 노출 범위, 수집 rate 실무 상한 |
| W-16 | **Too Many Cooks** | (IEEE, 403) | `09` §0.3에서 4개 수치가 검증 불가로 강등 | 인용 정확성 | 초록의 방향성 문구만 citable | 4개 수치의 실제 값 |
| W-17 | **Miao 외 2023 / Zhong 외 2011** | CPSS TPEA `10.24295/cpsstpea.2023.00004` / SCHM `10.1002/stc.469` | `09` §4.3에서 "in ANY field"를 falsify한 두 논문. 수치가 `UNVERIFIED` | F1의 범위 표현 | metadata만 | 샘플링 주파수를 변화시킨 범위, 진단 정확도 정의, 비용 축 부재 확인 |
| W-18 | **Mantis** | ICS 2026 | `09` §10.2에서 누락 venue(ICS)로 식별 | F1/F3 미확정 | 제목·venue 수준 | 내용 전반 |
| W-19 | **ISC High Performance research track 2024–2026** | ISC | `B_hpdc_ipdps_cluster_isc_acsos` 기준 **2024–2026 미검증** | 전 후보의 census 완전성 | 전수조사 미완 | ODA/telemetry/운영 논문 유무 |
| W-20 | **AgenticAI4HPC 2026** | SC26 워크숍(1회차) | C7의 lane을 선점 | C7(현재 DROP) | 개최 예정 확인 수준 | 채택 논문 목록 — HPC 운영 agent 벤치마크가 나오면 C7 영구 폐기 |

---

# §3. 언어권 사각지대

`09` §10.3의 근거 — **어떤 `NO SUCH WORK EXISTS`도 주장할 수 없는 이유**가 여기에 있다.

| # | 대상 | 왜 중요한가 | 무효화 가능 대상 | 현재 상태 |
|---|---|---|---|---|
| W-21 | **CNKI / Wanfang / 万方** (중국어) | 중국은 세계 최대 규모 HPC 운영 주체 중 하나이고(Sunway, Tianhe), **Beacon(NSDI'19)이 Sunway TaihuLight 40,960노드 4계층 telemetry를 이미 했다**는 사실이 그 자체로 이 언어권에 더 있을 가능성을 시사한다 | **F1, F3** — 특히 다계층 telemetry 비용·RCA | **미탐색** |
| W-22 | **J-STAGE / CiNii / IPSJ** (일본어) | 富岳(Fugaku)/RIKEN R-CCS의 운영 분석. `09` §0.1에서 Gerofi(Intel + RIKEN 겸직)를 확인한 것처럼 일본 커뮤니티는 국제 색인에 부분적으로만 나타난다 | F1, F3 | **미탐색** |
| W-23 | **국내 색인 + 내부 문서** | W-05 참조 | 전부 | **미탐색 (최우선)** |
| W-24 | 독일어권 grey literature (GWDG, JSC, LRZ, HLRS 기술보고서) | `04` §5의 German 8-center Table 4가 이 계열에서 나왔다. LLview·PIKA·DCDB의 실무 문서가 여기 있다 | F1의 GPU 교란 gap, C10 | 부분 확보 |

**따라서 논문에서 사용할 안전한 문구:**
> *"우리가 검색한 범위(영어 색인: Crossref, dblp, arXiv, USENIX, OSTI, 기관 리포지터리; 2020–2026 + 특정 계보의 소급 검색) 안에서 …를 찾지 못했다."*
> **절대 쓰지 말 것:** *"존재하지 않는다"*, *"최초"*, *"유일한"*, *"어떤 분야에서도"*.

---

# §4. 방법론적 미확인 사항

| # | 항목 | 내용 | 영향 |
|---|---|---|---|
| W-25 | `01_VENUE_MAP.md` 전문 미독 | 이 문서는 하위 에이전트가 작성했고 **전체를 읽지 않았다**(위험 주장만 grep). 20개 상속 caveat의 정확성이 미확인 | venue 전략 판단의 근거. 논문 제출 전 통독 필요 |
| W-26 | `B_hpdc_ipdps_cluster_isc_acsos` 평가 필드의 `[A]` 표시 | **초록을 읽을 수 없었으므로** 평가 규모·배포 성숙도 필드는 전부 **assessment**다 | `02`의 L/D/P 등급 신뢰도. 인용 전 개별 확인 필요 |
| W-27 | IEEE Cluster 2020–2022의 워크숍 번들 | 이 3년간 워크숍이 본 proceedings에 묶여 있어 **PIKA 등이 워크숍 논문인지 본트랙인지 구분이 어렵다** | `09` §8.1의 PIKA 판정. W-03과 함께 확인 |
| W-28 | Crossref rate limit | 검증 시 ~65 s/call 제약으로 20개 중 6개 DOI만 전문 대조 검증 | 나머지 14개 DOI는 metadata 수준. 인용 전 개별 확인 |
| W-29 | WebSearch 예산 소진 | 1차 조사에서 200/200 소진. ACM DL·IEEE Xplore 403, dblp/Scholar 검색 robots 차단, OpenAlex·Semantic Scholar 429 | 검색 완전성의 상한. `09` §10.3의 근거 |

---

# §5. 시점 기반 재확인 캘린더

| 시점 | 확인할 것 | 트리거하는 판정 |
|---|---|---|
| **즉시** | W-05(국내·내부), W-01(DB 스윕), W-03, W-04, W-06, W-07, W-08, W-10 | F1 착수 가능 여부, F2 novelty 잔존 여부 |
| **2026-09~10** | **W-02(SC26 ORNL)**, W-20(AgenticAI4HPC 채택 목록), SC26 proceedings 전체 | F3 착수 여부, C7 영구 폐기 여부 |
| **2026-11 (SC26 개최)** | SC26 SotP 토픽 영역 논문 전수, BoF·워크숍 발표자료 | 전 후보 재평가 |
| **2026-12** | W-19(ISC 2024–2026 소급), W-21/W-22(언어권) | zero-claim 문구 확정 |
| **2027-03** | F2 관련 신규 발표 재확인(3개월 주기) | F2-K5 |
| **2027-06** | ISC 2027, HPDC/IPDPS/Cluster 2027 채택 목록 | 전 후보 |
| **2027-09** | F1 예비 실험 결과 + SC27 프로그램 | F1 계속/폐기(`11` §1.11) |

**F2는 3개월 주기 확인이 필요한 유일한 후보다.** 가장 빠르게 침식된다(`10` §3, 2위 항목).

---

# §6. 이 목록을 다루는 규칙

1. **항목이 해소되면 이 문서에 결과를 기록하고 `09`의 해당 claim label을 갱신한다.** 목록만 유지하고 결과를 반영하지 않으면 감사 체계가 무의미해진다
2. **`UNKNOWN`을 `NOT EXIST`로 승격하지 않는다.** `09` §1.2의 두 등급(`NO COUNTEREXAMPLE FOUND IN CURRENT CENSUS` vs `NO SUCH WORK EXISTS`) 구분을 유지
3. **검색 snippet으로 high-stakes 결론을 만들지 않는다.** 출처 우선순위: 공식 proceedings → 출판사 → DOI/Crossref → 기관 페이지 → 저자 원고/preprint
4. **접근 불가능한 내용을 추측해 채우지 않는다.** W-02가 대표 사례 — 제목과 기관만 알고 있으며 그 이상 쓰지 않았다
5. **W-05를 가장 먼저 한다.** 비용이 거의 없고 위험이 가장 크며, 다른 모든 항목과 달리 문헌 검색이 아니라 기관 내부 문의로 해결된다

---

**연결 문서:** `09` §4.5(미해결 위험 원본)·§10.2(사각지대)·§10.3(검색 한계), `08` §4.4(F1 착수 전 점검), `10` §6(순위가 틀릴 수 있는 지점), `11`(각 실험의 문헌 기반 실패 기준 F1-K6/K7, F2-K5, F3-K5).

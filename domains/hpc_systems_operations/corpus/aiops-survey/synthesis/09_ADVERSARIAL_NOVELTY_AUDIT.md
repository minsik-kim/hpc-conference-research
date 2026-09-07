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

# 09. ADVERSARIAL NOVELTY AUDIT
## 기존 8개 문서의 주장 감사, 반례 탐색, 그리고 필수 정정

**작성일:** 2026-09-06 (2차 작업)
**대상:** `00`–`07` 문서의 모든 주요 claim
**방법:** 9개 병렬 적대적 검증 에이전트. 목적은 확인이 아니라 **반증**이었다.

> ### ⚠️ 이 문서를 먼저 읽어야 하는 이유
> **2차 검증에서 `00`–`07`의 핵심 claim 다수가 falsified 또는 weakened 되었고, 인용 자체가 잘못된 항목 3건(fabrication-grade)이 발견되었다.** 아래 §0의 정정 목록을 반영하지 않고 `00`–`07`을 인용하면 논문 심사에서 치명적이다.
>
> **문서 명칭 정정:** 사용자가 지칭한 `07_FINAL_SYNTHESIS.md`는 실제로 `07_ANSWERS_TO_KEY_QUESTIONS.md`다. 다른 이름의 파일은 존재하지 않는다.

---

# §0. 즉시 정정 목록 (CRITICAL)

## 0.1 인용 자체가 틀린 항목 — 절대 그대로 쓰지 말 것

| # | 어디에 있나 | 무엇이 틀렸나 | 정확한 사실 |
|---|---|---|---|
| **F-1** | `02` M-?? / `03` P3 / `05` / `07` — SC25 Aurora 논문을 "Intel/Argonne", 일부 출처는 "Allen et al. (ANL/Intel)"로 표기 | **저자·소속이 틀렸다. Argonne 소속 저자는 없다.** 또한 `arXiv:2509.08207`은 **다른 논문**(Aurora 시스템 아키텍처 개요)이며 이 논문이 아니다 | **Yonatan Levitt, Richard Barella, Sam Zeltner, Thomas E. Musta, Lance Cheney, Gustavo Espinosa, Olivier Franza, Balazs Gerofi — 전원 Intel Corporation**(Gerofi만 Intel + RIKEN R-CCS 겸직). SC'25, **DOI `10.1145/3712285.3759883`, pp.1073–1084**, dblp key `conf/sc/LevittBZMCEFG25`. **arXiv ID를 붙이지 말 것.** "MTTR 최대 84× 감소"는 abstract에서 확인됨 |
| **F-2** | 2차 조사 중 등장한 "From Detection to Recovery" 관련 수치 | **"bandwidth paradox", "0.84 FP/day", "1.4–10.4% RoCE", "128-slot NFS RPC", "10/10 XID 탐지 / 2/10 pre-XID" — 이 표현과 수치는 논문(HTML·PDF 양쪽)에 존재하지 않는다** | 실제 수치: NFS 평균 read throughput **150.8 GB/s = 최대 read 대역의 21.5%**, write **16.0%**; **XID로 식별된 GPU 장애 10건**; auto-retry 성공률 **33.3%(12 chain / 73 attempt) vs 수동 12.5%**(≈2.7배), median retry interval 11분(IQR 10–11); checkpoint event 523건; **63노드 중 상위 3노드가 exclusion의 >50%**. 논문의 실제 결론: ***"no single precursor metric dominates consistently across failure types"*** |
| **F-3** | 2차 조사 중 등장한 Gleaner 관련 서술 | **"0.1%–10% sampling rate sweep"과 "MicroRCA/Nezha/ShapleyIQ를 평가 대상 RCA 시스템으로 사용"은 근거 없음** | 실제: baseline은 *sampler*들 — Random, Sieve, Sifter, TraStrainer, TracePicker. Nezha는 배경/관련연구에만 등장. **headline은 1% sampling rate에서 "improves RCA accuracy by 42%-107% over the next-best sampler"** |

**추가 metadata 정정 5건:**

| 항목 | 정정 |
|---|---|
| Brauckhoff et al. IMC'06 | 저자에 **Lakhina** 누락. 정확: Brauckhoff, Tellenbach, Wagner, May, **Lakhina**, IMC'06 **pp.159–164**, DOI `10.1145/1177080.1177101`. Mai et al.은 **pp.165–176**, DOI `10.1145/1177080.1177102` |
| Mint | 단순 preprint가 아니라 **ASPLOS'25 채택**. 정식 제목은 더 길다: *"Mint: Cost-Efficient Tracing with **All Requests Collection via Commonality and Variability Analysis**"* |
| Uptake (ISSRE'24) | 표기는 **Uptake**(전부 대문자 아님). DOI `10.1109/ISSRE62328.2024.00054`, pp.499–510 |
| Meta RSC | **HPCA 2025**, DOI `10.1109/HPCA61900.2025.00096`, pp.1259–1274 |
| Kestrel | baseline 하한은 **0.50 s**이지 0.20 s가 아니다(3GPP-PM baseline 기준). Kestrel median **0.80 s**, F1 **0.81**, export bandwidth **10× 감소** |

## 0.2 수치 해석 오류 1건 — "65.7%" 논란 해결

`05`/`07`이 인용한 *How Far Can RCA Go* (arXiv 2607.13548)의 **"실패의 65.7%가 reasoning gap"**은 **표의 하위 컬럼을 헤드라인으로 잘못 인용한 것**이다.

정확한 Table VII (Market CB1, DK OFF, n=70):

| 항목 | Component | **Reason** | Timestamp | **Overall** |
|---|---|---|---|---|
| Reasoning Gap | 51.4% | **65.7%** | 54.3% | **40.0%** |
| Data Ambiguity | — | — | — | **1.4%** |
| Mixed | — | — | — | **38.6%** (27건) |
| Correct | — | — | — | **20.0%** (14건) |

→ **인용할 값: Overall reasoning gap 40.0% vs data ambiguity 1.4%, 또는 그 비 ≈29:1.** Mixed를 reasoning 측에 포함하면 78.6%다. **"65.7%를 전체 실패율로" 쓰면 안 된다.**
또한 최고 성능 시스템은 논문 자신의 **Structured Multi-Agent RCA (DK ON): Full Score 25.71 / Partial Score 45.60** — **Acc@1이 아니다.** Granger/PC/FCI/LiNGAM/NTLR가 Acc@1·Acc@10 모두 **0**인 것은 확인됨.

## 0.3 검증 불가로 강등해야 할 수치 1건

**Too Many Cooks (ISSRE'25)**의 구체 수치 4개 — "CloudRCA에서 로그 제외 시 AIOps22 F1 +10pp", "metric 제외 시 GAIA F1 +40%", "DiagFusion +10% Acc@1 / +15% F1" — **검증 실패.** arXiv preprint 없음, IEEE Xplore 403.
**확인된 것은 방향성 주장뿐이다:** abstract 원문 *"Surprisingly, we find that adding more data sources does not necessarily improve the performance of microservice failure diagnosis in some cases."*
저자·venue는 확인됨: Shenglin Zhang, Xiaoyu Feng, Runzhou Wang, Minghua Ma, Wenwei Gu, Yongqian Sun, Zedong Jia, Jinrui Sun, Dan Pei · ISSRE 2025, DOI `10.1109/ISSRE66568.2025.00014`, pp.1–12.
→ **방향성만 인용하고 구체 수치는 쓰지 말 것.**

---

# §1. Claim label 체계와 전체 감사 결과

## 1.1 라벨 정의

| 라벨 | 의미 |
|---|---|
| `STRONG-EVIDENCE` | 1차 출처에서 verbatim 확인. 반례 탐색 후에도 생존 |
| `SUPPORTED` | 1차 출처 확인, 반례 탐색은 부분적 |
| `CENSUS-DEPENDENT` | 이 census가 조사한 venue 집합 안에서만 참. venue를 넓히면 깨진다 |
| `ZERO-CLAIM` | "0편/유일/최초/없다" 형태. **최고 위험군** |
| `PARTIAL-COVERAGE` | 근거 데이터에 알려진 구멍이 있음 |
| `NEEDS-VERIFICATION` | 미확인. 인용 전 확보 필요 |
| `SPECULATIVE` | 추론. 사실로 쓰면 안 됨 |

## 1.2 zero-count claim의 두 등급 — 반드시 구별

- **`NO COUNTEREXAMPLE FOUND IN CURRENT CENSUS`** — 이 조사 범위에서 못 찾았다. 반례가 있을 수 있다. **논문에 쓸 수 있는 최대 강도는 이것이다.**
- **`NO SUCH WORK EXISTS`** — 존재하지 않는다. **이 조사는 어떤 claim에도 이 등급을 부여할 수 없다.** 이유: WebSearch 예산 200/200 소진(9개 에이전트 전부), ACM DL·IEEE Xplore 403, OpenAlex·Semantic Scholar search 429, dblp/Google Scholar search robots 차단, 중국어(CNKI/Wanfang)·일본어(J-STAGE/CiNii/IPSJ)·한국어(KISS/RISS/DBpia/ScienceON/KSC) 색인 미검색, KISTI 내부 기술보고서 미검색.

## 1.3 주요 claim 감사표

| # | Claim (출처 문서) | 라벨 | 2차 검증 결과 |
|---|---|---|---|
| C-01 | SC 본프로그램의 이 주제 비중은 연 4–12편, 2024년 계단식 증가 (`03` §3.2, `07` Q1) | `SUPPORTED` `PARTIAL-COVERAGE` | **생존.** 독립 재검증에서 SC22 broad=7이 정확히 일치. 다만 **약간의 undercount**: SC20 +1, SC22 +1~3, SC23 +1~2, SC24 +1~2, SC25 +1 |
| **C-02** | **"2020–2026에 15개 주요 센터로부터 production 운영 분석 SC 본트랙 Technical Paper 0편"** (`03` §3.1, `07` Q1·Q8) | `ZERO-CLAIM` → **FALSIFIED** | **§2 참조. ≥9편의 반례. 그리고 전제 자체가 범주 오류였다** |
| C-03 | SC Technical Paper와 State of the Practice는 별개 트랙이며 구분 불가 (`00` §6.2, `03` 서두) | **FALSIFIED** | **SOP는 Technical Papers 트랙 *안의* 토픽 영역이다.** SC21/22/24/25/26 CFP에서 확인. SC22 Papers FAQ: SOP 제출은 *"the same double-blind review process and revise-and-respond procedures as all other papers"* |
| C-04 | HPC AIOps는 L3에서 정체, L5–L7 production 증거 극히 희소 (`05` PART I, `07` Q4) | `CENSUS-DEPENDENT` → **WEAKENED, 재범위 필요** | **§3 참조.** 4개 독립 반례 |
| **C-05** | **"HPDC/IPDPS/Cluster ~700편 중 L7/D5는 사실상 1편(HPDC'24 BSC)"** (`05` G15, `07` Q4) | `ZERO-CLAIM` → **정정** | **HPDC'24 BSC는 L6/D2(offline historical replay)다. 저자 방법론에서 verbatim 확인.** → 정정된 주장은 **더 강하다: HPDC/IPDPS/Cluster 2020–2026에 L7/D5는 0편**. 단 IOAgent(IPDPS'25)가 L6/D1이므로 "L5/L6도 1편"은 undercount |
| **C-06** | **"telemetry 비용 대 하류 품질의 Pareto frontier는 어떤 HPC 시스템에도 발표된 적 없다"** (`05` G11, `06` C1, `07` Q6) | `ZERO-CLAIM` → **재작성 필수** | **§4 참조. 비용 축은 이미 발표되었다(DCDB SC'19). formulation도 이미 있다(AWStream SIGCOMM'18)** |
| **C-07** | **"탐지에 충분한 telemetry 표현이 진단에는 불충분할 수 있다"가 novel hypothesis** (`05` §3.3, `06` C1, `07` Q6) | `SPECULATIVE` → **FALSIFIED as novel** | **§4.2 참조. FDI 제어이론에서 사실상 정리(theorem)이며, 2026년에 벤치마크로 실증되었다** |
| C-08 | "0편: 샘플링 간격 변화" (`05` G11) | `ZERO-CLAIM` → **FALSIFIED, HPC 한정 시에도 부분 falsified** | LDMS SC'14(1/20/60 s), **DCDB SC'19(100 ms→1 s, 25 configs)**, Mai IMC'06, Brauckhoff IMC'06, Gleaner, AdaM. **정확한 잔존 주장: "품질을 측정하면서 샘플링 간격을 변화시킨 HPC 논문이 없다"** |
| **C-09** | **"0편: 보존 해상도(retention resolution) 변화"** (`05` G11) | `ZERO-CLAIM` → **최강 생존** | **§4.3 참조. TSDB rollup/retention을 결정변수로 다루고 하류 품질을 측정한 peer-reviewed 논문을 어느 분야에서도 찾지 못했다.** 단 "in ANY field" 표현은 falsified(Miao 2023, Zhong 2011) |
| C-10 | "0편: telemetry rate 함수로서의 탐지 지연" (`05` G11) | `ZERO-CLAIM` → **FALSIFIED(네트워킹), HPC 한정 생존** | Kestrel(arXiv 2510.27664)이 정확히 이것을 한다 |
| C-11 | "0편: telemetry 축소가 RCA 품질에 미치는 비용 측정" (`05` G11) | `ZERO-CLAIM` → **FALSIFIED, HPC 한정 생존** | Gleaner, Mint(ASPLOS'25), TraceDiag(FSE'23), TelemetrySuffBench, FDI isolability 문헌 |
| **C-12** | **"cross-layer RCA를 production 슈퍼컴퓨터에서 한 연구가 없다"** (`05` G16, `07` Q7) | `ZERO-CLAIM` → **FALSIFIED as stated** | **Beacon(NSDI'19), Sunway TaihuLight 40,960 노드, 18개월 production, 4계층(compute→forwarding→storage→metadata).** §5 참조 |
| **C-13** | **"수치 telemetry의 cross-system 전이 손실을 측정한 연구가 없다 / 유일한 측정치는 0.898→0.726"** (`05` G12, `07` Q5) | `ZERO-CLAIM` → **WEAKENED** | Farooq/Milano/Borghesi ESWA 2026("First real-world validation on a tier-0 supercomputer", federated **transfer** learning)이 cross-node 일반화를 보고. **정확한 잔존 주장은 §6** |
| **C-14** | **"배치 스케줄·할당 회계·체크포인트 의존 환경의 remediation 비용 모델이 없다"** (`05` G15, `06` C6) | `ZERO-CLAIM` → **FALSIFIED** | **HPDC'24 BSC가 세 요소를 전부 갖췄다.** §7 참조 |
| **C-15** | **"HPCSYSPROS 46편 / HPCTESTS 10편+ 승격 0건; PIKA·LLview·XDMoD·Arbiter·EMOI·CEEMS·buildtest·Ramble·ORNL ODA dashboard 모두 아카이브 논문 없음"** (`04` §9.2, `01` §5.5) | `ZERO-CLAIM` → **부분 FALSIFIED** | **§8 참조. LDMS·PIKA·XDMoD는 아카이브 정규 논문이 있고, LDMS는 NSDI'20+ICS'21까지 이어지는 끊기지 않은 사슬을 갖는다** |
| C-16 | 연구 산출은 시스템 규모가 아니라 학술 파트너·데이터 공개와 상관 (`03` §3.1, `07` Q8) | `SPECULATIVE` (인과 주장 금지) | **exploratory observation으로 생존, 그리고 메커니즘이 정교해졌다: 다리는 워크숍 논문이 아니라 *공개 데이터셋*이다.** §8.3 |
| C-17 | ACSOS 2020–2025 본트랙에 HPC 평가 논문 0편 (`01` §3.8) | `ZERO-CLAIM` `CENSUS-DEPENDENT` | 반례 못 찾음. 유지하되 `NO COUNTEREXAMPLE FOUND` 등급 |
| C-18 | IEEE Cluster 2023/2024 본트랙에 monitoring/anomaly/failure-prediction 0편 (`01` §3.4) | `ZERO-CLAIM` `NEEDS-VERIFICATION` | 재검증 안 됨. abstract 미독 상태의 제목 기반 판정 |
| C-19 | SC 본프로그램에 syslog/log analytics 사실상 0편 (`03` §3.4) | `ZERO-CLAIM` `CENSUS-DEPENDENT` | 유지. 단 SC24 *LLMs for Anomaly Detection in Computational Workflows*는 로그 기반이므로 "사실상"의 범위를 좁혀야 함 |
| C-20 | production Slingshot/Dragonfly 혼잡 field study 0편 (`03` §3.4) | `ZERO-CLAIM` → **WEAKENED** | **Monet(NSDI'20)와 ICS'21 Delay-Sensitivity가 Cray Aries production counter로 혼잡을 측정·완화한다.** Slingshot 세대 한정으로 좁혀야 함 |
| C-21 | facility 부품 예지보전 0편 (`03` §3.4) | `ZERO-CLAIM` → **WEAKENED** | NSCC Tianjin *Anomaly Detection Method for Chiller System of Supercomputer*(HPCCT 2019, `10.1145/3341069.3341076`) |
| C-22 | 벤더 항목 11건 중 알고리즘+정량평가 1건(CADDY), peer-review 0건 (`04` §6) | `SUPPORTED` | 재검증 안 했으나 1차 출처 기반. Intel·VAST 미포함은 명시됨 |
| C-23 | L0–L7 사다리 (`00` §3.2 전체) | **출처 누락** | **Netti, Shin, Ott, Wilde, Bates, *A Conceptual Framework for HPC Operational Data Analytics*, IEEE Cluster 2021, `10.1109/cluster48925.2021.00086`** (LRZ+ORNL+EE HPC WG)이 이 분야의 표준 ODA maturity 프레임워크다. **인용하지 않으면 기존 taxonomy를 재발명한 것으로 읽힌다** |
| C-24 | "Nankai/Tsinghua 그룹이 슈퍼컴퓨터 운영 연구를 발표한다" (`02` §2.9, `05` 참조) | **FALSIFIED** | Dan Pei NetMan / Nankai(Shenglin Zhang, Yongqian Sun) 산출은 압도적으로 microservice·cloud·network AIOps다. **중국 슈퍼컴 운영의 실제 중심: NSCC-Wuxi + Tsinghua(Wei Xue/Jidong Zhai), CNIC-CAS(Changhua Pei), NUDT(Gang Xian, Wenxiang Yang, Jie Yu)** |
| **C-25** | (암묵적) 한국/KISTI에는 이 분야 선행 연구가 없다 | **FALSIFIED — 가장 중요한 발견** | **§9 참조. KISTI는 10년 이상의 운영 분석 발표 계보를 이미 갖고 있고, 그중 하나는 L6/L7이다** |

---

# §2. Claim A — SC 희소성: **FALSIFIED**

## 2.1 전제 자체가 범주 오류였다

`00` §6.2와 `03` 서두는 "SC 논문 페이지가 모든 트랙을 'Technical Papers Archive'로 표시하므로 Technical Paper와 State of the Practice를 구분할 수 없다"고 적었다. **틀렸다. 전부 Technical Paper이기 때문에 그렇게 표시되는 것이다.**

**SC에서 State of the Practice는 단일 Technical Papers 트랙 안의 *토픽 영역(topic area)*이다.** SC21/SC22/SC24/SC25/SC26에서 독립 확인:

- **SC25 CFP**(`areas/Tracks` 항목): *"Submissions will be considered on any topic related to high performance computing within the areas below. Authors must indicate a primary area from the choices on the submissions form..."* — SOP는 11개 area 중 하나이며 Algorithms, Applications, Architecture & Networks와 나란히 나열된다.
- **SC26 CFP**: SOP는 10개 area 중 9번째, 동일 제출 폼.
- **SC22 Papers FAQ**: SOP 제출은 *"the same double-blind review process and revise-and-respond procedures as all other papers"*를 거친다.
- **SC 프로그램 스케줄러(linklings)**: `Event Type` 필드가 **`Paper`**로 표시된다. `State of the Practice`라는 event type은 존재하지 않는다. SOP는 **세션 수준** `Tracks:` 태그 줄에만 Energy Efficiency, Resource Management, Accelerators 등과 섞여 나타난다.

**따라서 "SOP였으니 Technical Paper가 아니다"라는 방어는 불가능하다. SC 본 proceedings에 실린 SOP 태그 논문은 SC 본트랙 Technical Paper다.**
그리고 `Tracks:` 줄은 **세션 단위**이므로 개별 논문을 SOP-primary로 특정하는 것도 공개 자료로는 불가능하다.

## 2.2 발견된 방법 (재사용 가치 높음)

`sc2X.conference-program.com`(SC22는 `sc22.supercomputing.org`)이 `Event Type`과 세션 수준 `Tracks:` 줄을 노출한다. `/organization/?inst=<stable-id>`가 기관별 기여를 event type과 함께 열거한다. **기관 해시는 연도 간 안정적이다: ORNL = `16969005850305409037`, LBNL = `13588942530137301385`.**
→ **완전한 재계수 방법이 확보되었다: 연도별로 `Event Type: Paper` 세션을 전부 뽑고 `Tracks:` 줄에 "State of the Practice"가 있는 것을 남긴다.** 제목 키워드 스크린이 아니라 트랙 기반 스크린이다.

## 2.3 반례 — 센터 주도 SC 본트랙 Technical Paper 9편

| # | 연도 | 논문 | 주도 센터 | 근거 |
|---|---|---|---|---|
| 1 | SC20 | GPU Lifetimes on Titan Supercomputer: Survival Analysis and Reliability | **ORNL** (Ostrouchov, Maxwell, Ashraf, Engelmann, Shankar, Rogers — 전원 ORNL) | `10.1109/SC41405.2020.00045`. 6년/18,688 GPU/10만+ GPU-년. 코드 `olcf/TitanGPULife` |
| 2 | SC21 | Revealing power, energy and thermal dynamics of a 200PF pre-exascale supercomputer | **ORNL** (W. Shin, Oles, Karimi, Ellis, F. Wang) | `10.1145/3458817.3476188`, pp.1–14 |
| 3 | SC23 | Frontier: Exploring Exascale | **ORNL** (Atchley 외) | `10.1145/3581784.3607089`. **Best Paper Finalist** |
| 4 | SC24 | A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale | **ORNL** (11인 전원 ORNL) | `10.1109/SC41406.2024.00029`, 18pp. Event Type `Paper`, Tracks 줄에 SOP 포함 |
| 5 | SC24 | Toward Sustainable HPC: In-Production Deployment of Incentive-Based Power Efficiency Mechanism on the Fugaku Supercomputer | **RIKEN R-CCS + Sandia** (Solórzano, Sato, Yamamoto, Shoji, Brandt, Schwaller, Walton, Green, Tiwari) | `10.1109/SC41406.2024.00030`, 16pp |
| 6 | SC24 | An Evaluation of the Effect of Network Cost Optimization for Leadership Class Supercomputers | **ORNL** (10인 전원 ORNL) | `10.1109/SC41406.2024.00037`, 16pp |
| 7 | SC24 | Understanding Data Movement Patterns at HPC: A NERSC Case Study | **LBNL/NERSC** (Giannakou, Enders, Ramakrishnan, N. Wright) | `10.1109/SC41406.2024.00077`. NERSC 3년 production 네트워크 트래픽 |
| 8 | SC25 | Breaking the System Noise Barrier at Exascale | **LLNL** (León, Hanford, D'Hooge, Behlendorf, Pankajakshan, Leininger) + HPE | `10.1145/3712285.3759793`, pp.411–436 |
| 9 | **SC26** | **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** | **ORNL** (Awais Khan, Zimmer, Anjus George, Karimi, F. Wang, W. Shin — 전원 ORNL) | SC26 공식 Best Paper Finalist 발표(2026-08-13). **Best Paper Nominee** |

보조: SC25 *Fine-grained Automated Failure Management*(`10.1145/3712285.3759883`, Intel, Gerofi가 Intel+RIKEN 겸직) — Event Type `Paper`.

**판정: C-02의 두 부분 모두 실패.**
① "0편" → **거짓, ≥9편, SC22를 제외한 모든 연도에 존재.**
② "좋은 센터 작업은 워크숍/CUG로 간다" → **배타적 주장으로서 거짓.** 센터 운영 분석은 SC Technical Papers 본무대에 도달하며 **거기서 수상 후보가 된다**(SC23 ORNL Frontier = Best Paper Finalist; SC26 ORNL alert-fatigue RCA = Best Paper Nominee).

**유일하게 실제로 얇은 해: SC22.** `NO COUNTEREXAMPLE FOUND`이지 `NO SUCH WORK EXISTS`는 아니다. `sc22.conference-program.com`이 TLS hostname mismatch로 실패해 ORNL 외 센터를 확인하지 못했다.

## 2.4 이 falsification이 전략에 주는 함의 (중요)

**나쁜 뉴스로 읽지 말 것.** 원래 claim은 "SC는 센터 운영 논문을 안 받는다 → 구조적 기회"였다. 정정된 사실은 **"SC는 센터 운영 논문을 받고, 심지어 상을 준다"**이며, 이는 목표 달성 가능성을 **높인다**. 다만:
- 경쟁은 예상보다 치열하다. ORNL이 이 lane을 지배한다(SC20·21·23·24×2·26).
- **비교 기준선이 올라간다.** 심사는 "센터가 이런 걸 쓸 수 있나"가 아니라 "ORNL 수준인가"로 이루어진다.
- **SOP를 별도 우회로로 생각하면 안 된다.** 동일 double-blind 심사, 동일 폼이다. `07` §"별도 경로: SC State of the Practice"의 "서로 다른 심사 기준을 쓰므로 경쟁하지 않는다"는 서술은 **틀렸다. 삭제할 것.**

---

# §3. Claim B — L3 정체: **핵심은 생존, 3개 하위주장 정정**

## 3.1 반례 4건

**① Meta RSC — 가장 강한 경계 반례.**
Kokolis 외 (FAIR at Meta), *Revisiting Reliability in Large-Scale Machine Learning Research Clusters*, **HPCA 2025**, `10.1109/HPCA61900.2025.00096`, pp.1259–1274, arXiv 2410.21680. **모든 수치 verbatim 확인:**
- *"health checks that are periodically scheduled to run every five minutes"*
- *"When a health check fails for a node, the node will transition to a remediation state and will become unavailable for scheduling until it is fixed."*
- 심각도 높은 실패 → 즉시 스케줄러 핸들러가 노드 제거 + 해당 노드의 모든 job 재스케줄. 낮은 심각도 → job 종료 후 제거.
- *"The identified lemon nodes represent 1.2% of RSC-1's footprint, 13% of daily jobs, and 1.7% of RSC-2's footprint."* ← **주의: 1.2%/13%는 *lemon node 한정* 수치다. "전체 footprint가 remediation 중"이 아니다.**
- *"less than 1% of successfully completed jobs observe a failed health check"* (FP 보정)
- **"lemon node" 탐지는 통계적 peer-outlier 분석**이며 단순 임계값이 아니다.
→ **Slurm 관리 16k GPU 슈퍼컴퓨터급 시스템에서 production closed-loop 노드 조치 + 데이터 기반 탐지기 + 발표된 비용/FP 회계.** 산업계(Meta)이고 venue는 **HPCA — census venue 집합 밖**이다. 즉 **coverage gap**이며 HPC-센터 하위주장의 반박은 아니다.

**② EAR / GEOPM 계열 — 에너지 도메인의 L7/D5.**
EAR(Energy Aware Runtime, BSC+Lenovo)는 MareNostrum 5와 LRZ에서 production 배포되어 학습된 power/performance 모델로 DVFS/power를 closed-loop 제어한다. **L7/D5이지만 장애 remediation이 아니라 에너지 최적화이며, RL이 아니라 모델 기반이다.**
→ **"HPC AIOps는 L3에 정체"라는 넓은 해석은 틀렸다. *remediation 한정* 해석은 생존한다.**

**③ Fugaku SC24 인센티브 메커니즘 — L6/L7 in-production.**
`10.1109/SC41406.2024.00030`. RIKEN 저자, exascale production 기계에 실제 배포. census가 이를 SotP로 분류하면서 L-레벨 논증에서 빠뜨렸다.

**④ KISTI 자신의 Shim 2026 — 국내 L6/L7.**
Hyungwook Shim (KISTI), *Policy-aware GPU resource allocation for national supercomputing*, **Scientific Reports 2026**, `10.1038/s41598-026-42625-6`. trigger 기반 회수 + 비례 재분배 + 피드백 조정 컨트롤러. MAE 8.03%→1.30%, 이용률 >92%. **완화 요인: 1주 horizon / 4시간 간격 시뮬레이션이며 배포는 아니다.**
→ **KISTI 저자가 "HPC는 L3 천장"이라고 쓰면 KISTI 자신의 발표에 의해 반박된다.**

추가: **Google TPUv4 *Resiliency at Scale*(NSDI'24)**, **MegaScale(NSDI'24, ByteDance)**, **Acme(NSDI'24, Shanghai AI Lab)** — 모두 명시적으로 슈퍼컴퓨터로 프레이밍된 production 자동 remediation.
그리고 **TSLoc(KDD 2026, `10.1145/3770855.3818499`, CNIC-CAS+Tsinghua+StepFun)** — self-supervised faulty node localization, **Top-5 acc 0.908, 평균 4.2초**, 미지 장애·신규 metric에 일반화. L5.

## 3.2 정정: HPDC'24 BSC는 L7/D5가 아니다

**저자 방법론에서 verbatim 확인:**
> *"In our implementation based on historical logs, the environment obtains the UEs, CEs, events and job state from the logs"*
> *"When the events are taken from a historical log, the CE, UE and system state features and their relative rates of change over time do not depend on the agent's last action."*
> 저자 자신의 한계 서술: *"For practical reasons, it was impossible to use error and job logs from the same period and system."*

→ **L6 / D2 (offline historical replay).** 배포된 closed loop가 아니다.
성과 수치는 확인됨: ***"our method reduces lost compute time by 54% compared with no mitigation and is just 6% below the optimal Oracle method"***. MareNostrum 3 3,056 노드, DDR3-1600 DIMM 25,000+개(제조사 3사: 6,694/5,207/13,419), 2014-10~2016-11. mitigation cost 2/5/10 node-minutes 스윕. MN4 job log 2018-03~2019-03. RL 학습 비용 *"less than twenty node-hours per year"*.

**결과: 정정된 주장이 원래 주장보다 강하다 — HPDC/IPDPS/Cluster 2020–2026에 L7/D5 논문은 0편이다.**
동시에 **L5/L6은 존재한다**: IOAgent(IPDPS'25, `10.1109/ipdps64566.2025.00036`)는 RCA + 구체적 실행 권고(`lfs setstripe -S 4M` 등)로 **L5→L6**이며 D1(TraceBench trace, 배포 없음)이다.

## 3.3 ⚠️ 프레이밍을 뒤집는 발견: 클라우드도 깔끔하게 닫지 못했다

**Uptake (ISSRE 2024, `10.1109/ISSRE62328.2024.00054`, pp.499–510, Microsoft).** 모든 수치 확인:
> *"a decline in prediction accuracy, approximate 9%, subsequent to model retraining"*
> *"Performance on Azure decreases from 78.22% on T2 to 57.46% on T5, a decrease of 20.66%"*
> *"Backblaze and Alibaba also show decreases of 8.34%"* *"and 13.77%, respectively"*
> Uptake의 회복: *"enhance failure prediction accuracy by an average of 5%"*

**즉 auto-mitigation은 자기 학습 신호를 파괴한다.** 완화된 장애는 실현되지 않으므로 ground-truth label이 사라진다.
→ **"클라우드는 이 문제를 닫았다"는 프레이밍을 "클라우드는 루프를 닫았고, 그 대가로 측정된 9–20%의 모델 열화를 지불했으며, 그것을 감당할 수 있는 것은 fleet 규모 때문이다"로 바꿔야 한다.**
**이것이 claim B에 유리한 가장 날카로운 구조적 논거이며, 현재 `05`/`07`에 없다.** 노드 10³개와 월 10¹–10²건 장애를 가진 HPC 센터는 label을 그렇게 태울 여유가 없다.

## 3.4 구조적 어려움 — 근본적인가 제도적인가

| 클라우드가 의존하는 전제 | HPC에서 깨지는 방식 | 근본/제도 |
|---|---|---|
| **조치 단위가 독립적 호스트** | HPC 단위는 **gang-scheduled MPI job**. 노드 1개 drain이 N rank 전부를 죽인다. blast radius는 노드 수가 아니라 job width로 스케일한다 | **근본** (프로그래밍 모델에 뿌리) |
| **production에서 randomize 가능** | Narya의 sticky randomization은 Azure에 거의 동일한 호스트가 수백만 개 있어서 가능하다. Tier-0는 기계가 1대, 노드 10³–10⁴, job mix가 정상성도 노드 간 독립성도 없다 | **단일 기계에는 근본. 다중 사이트 연합 수준에서는 제도적**(컨소시엄이 사이트 간 randomize할 수 있으나 아무도 안 했다) |
| **조치의 가역성** | Narya의 조치는 싸고 대체로 가역적(live migration, 자동 리셋되는 Avoid). HPC drain은 **실행 중 job에 대해 비가역**이며 복구 경로는 체크포인트/재시작으로 그 비용은 센터가 아니라 애플리케이션이 진다 | **근본** |
| **용량 회계** | Narya는 클러스터당 동시 unallocatable 노드 수를 bound한다. HPC의 예비 노드는 **funded project에 갚아야 하는 할당 node-hour에 대한 직접 차감**이며 fleet 파라미터가 아니라 거버넌스 객체다 | **제도적, 그러나 어렵다** |
| **exchangeable peer** | Perseus/IASO의 peer 비교는 복제 스토리지에서 통계적으로 교환 가능한 peer가 다수 존재하기에 성립한다. HPC는 peer 노드가 job별로 이질적 작업을 한다 | **제도적** — Meta RSC의 lemon-node 탐지가 슈퍼컴 규모에서도 작동함을 증명했다 |
| **체크포인트 복원성** | FALCON/Unicron/MegaScale/Acme는 체크포인트 재시작 가능·탄력적·복제 풍부한 워크로드를 다룬다. HPC 체크포인팅은 애플리케이션 수준·opt-in·비싸다 | **근본** |
| **SuperBench의 Selector** | Aurora는 이미 *"a subset of these tests… randomly chosen and run before each compute job"*를 돌린다 — 메커니즘은 있고 **비용 최적화기가 없다**(random vs optimized) | **순수 제도적. HPC가 Selector를 못 할 이유가 없다** |

## 3.5 판정

| 하위주장 | 판정 |
|---|---|
| L3 정체, L5–L7 production 증거 희소 | **SURVIVES — 단 "open-science 국가 슈퍼컴퓨터의 장애 remediation" 범위로 한정할 때** |
| SC에 L7/D5는 1편(Aurora), 학습이 아니라 정책 | **SURVIVES.** 다만 저자/소속 정정(§0.1 F-1) 필수 |
| HPDC/IPDPS/Cluster에 L7/D5 사실상 1편 | **FALSIFIED → 정정: 0편** (더 강한 주장) |
| production HPC 센터는 규칙 기반만 | **국가/학술 센터에는 SURVIVES. 경계에서 WEAKENED**(Meta RSC). **에너지 도메인에서는 FALSIFIED**(EAR) |
| 클라우드는 이 문제를 닫았다 | **VERIFIED, 단 Uptake 발견으로 의미가 반전됨** |

**권고 문구:** *"운영 지능은 **open-science 국가 슈퍼컴퓨터**에서 L3–L4에 머물러 있다. L5–L7은 존재하지만 (a) 에너지/전력 도메인, (b) 하이퍼스케일러 및 AI 학습 클러스터, (c) 시뮬레이션 연구에 국한된다."*

---

# §4. Claim C — Telemetry 비용: **가장 중요한 정정**

## 4.1 ⚠️ 헤드라인 가설은 novel하지 않다 — 두 번 확인되었다

### HIT 1 — 정확히 이 가설을 제목에 걸고 실증한 논문 (2026)

**TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?** — Yuxuan Zhu, Peng Pu · arXiv:2608.07899, 2026-08-08. **존재·제목·저자·날짜 전부 확인.**
verbatim:
> *"Agent systems increasingly expose execution traces, yet **telemetry that reveals a failure may still be inadequate for identifying where that failure originated.** We introduce TelemetrySuffBench, a controlled benchmark that **separates failure detection, fault-origin localization, and safe abstention under insufficient evidence.**"*
> *"Metadata, OpenTelemetry-compatible, and OpenInference-compatible views yield detection F1 between 99.5% and 100.0% across all models"* · *"origin-step accuracy never exceeds 0.5%"* (전체 telemetry에서는 33.8%–97.2%)

**그러나 killer citation으로서는 약하다 — 두 가지 이유:**
1. **시스템 비용 축이 전혀 없다.** 샘플링 rate 없음, 바이트 없음, 보존 없음, 오버헤드 없음. 논문의 유일한 "비용"은 *"Reproducing the complete experiment costs approximately US$2,400 in model API charges"*다. telemetry "view"는 **스키마 ablation**(metadata-only, structural, OpenTelemetry-compatible)이며 비용 제약 수집 체제가 아니다.
2. **데이터가 synthetic이다.** *"TelemetrySuffBench is generated deterministically from instrumented, stateful workflows"*, 3개 도메인(tickets, documents, orders). production LLM-agent trace가 아니다.

→ **HPC의 *비용 제약* telemetry 충분성 문제에 대해서는 인접하지만 치명적이지 않다.**

### HIT 2 — FDI 제어이론에서는 사실상 정리다 (더 심각한 쪽)

- **Krysander & Frisk, *Sensor Placement for Fault Diagnosis*, IEEE Trans. SMC-A 38(6):1398–1410, 2008, DOI `10.1109/TSMCA.2008.2003968`.** metadata 전부 확인. abstract: *"An algorithm is developed for computing which sensors to add to meet a diagnosis requirement specification concerning fault detectability and isolability."*
  ⚠️ **주의: detectability⊂isolability의 형식적 superset 정리는 abstract에 없다.** IEEE 전문 403. **이 논문을 superset 주장의 근거로 인용하지 말 것 — 아래 Rosich를 인용할 것.**
- **Rosich, *Sensor Placement for Fault Detection and Isolation based on Structural Models*, IFAC SAFEPROCESS 2012** (Mexico City, 8th symposium). 확인. verbatim:
  > *"First step deals with those sensors that solve the problem only for fault detectability, while in the second step the sensors solving the fault isolability problem are computed."*
  ⚠️ **표기 정정: 실제 표기는 `D ⊆ Dmax`와 `I ⊆ Imax`이지 `D ⊆ D′`/`I ⊆ I′`가 아니다.**
- **Fault Diagnosis Toolbox** (Frisk & Krysander, Linköping) — `SensorPlacementDetectability()`와 `SensorPlacementIsolability()`가 **별개 메서드로 출시되어 있다.** 확인.
- 실증 예: Li-ion 배터리 팩 FDI(arXiv 2008.10533) 표에서 센서 1–2개 → **"D,NI"(Detectable, Not Isolable)**, 3개 이상 → 고유 isolable.

→ **"탐지에 충분한 표현이 진단에는 불충분할 수 있다"는 2008년 정리의 재진술이다. 제어·네트워킹·AIOps 어느 쪽 심사자에게도 기존 결과로 읽힌다.**

### HIT 3 — 시스템 측 축소를 RCA로 평가한 논문들
- **Gleaner** (arXiv 2604.16810, Yang·Fang·Zhang·He, CUHK-Shenzhen): 시스템 측 trace sampling, C1. **1% sampling에서 "improves RCA accuracy by 42%-107% over the next-best sampler"**, 샘플당 0.74 ms. 동기 예시가 정확히 이 가설이다 — 모든 span-level metric으로는 정상으로 보이는 trace가 conventional sampler에 버려지지만 embedded ERROR log가 결정적 설정 오류를 드러낸다.
- **Mint** (arXiv 2411.04605, **ASPLOS'25**): 시스템 측, C1. storage → 평균 **2.7%**, network → **4.2%**. Table 3 A@1: MicroRank 0.1563→**0.6563**, TraceAnomaly 0.2813→**0.7037**, TraceRCA 0.2500→**0.6563**.
- **TraceDiag** (ESEC/FSE 2023, `10.1145/3611643.3613864`, Microsoft M365 Exchange production): 모델 측 pruning, C1.

## 4.2 ⚠️ 비용 축도 이미 발표되었다 — DCDB SC'19

**Netti, Müller, Auweter, Guillen, Ott, Tafani, Schulz, *From Facility to Application Sensor Data: Modular, Continuous and Holistic Monitoring with DCDB*, SC'19, `10.1145/3295500.3356191`, arXiv 1906.07509.** 전문 확인.

**DCDB SC'19가 이미 제공하는 것:**
- **25개 configuration**: 샘플링 간격 **100 ms → 1 s** × 센서 **100 → 100,000**개
- **수집기 CPU:** Skylake **1.77%**, Haswell **0.69%**, KNL **4.14%** (production, 1 s); 스트레스 하 최대 3%
- **메모리:** 일반 <50 MB → 100,000 readings/s에서 350 MB
- **애플리케이션 교란**을 `O = (Tp − Tr)/Tr`로 형식화하여 HPL + **CORAL-2 벤치마크**(LAMMPS, Quicksilver, Kripke, AMG)에서 측정: *"never goes above 3%"*, **AMG는 1024노드에서 9% 피크**
- 센서 rate 대비 오버헤드의 선형회귀 모델

**DCDB SC'19가 하지 않는 것 = 진짜 잔존 gap:**
1. **네트워크 바이트 없음, 저장 볼륨/일 없음** (부재 확인)
2. **GPU 없음** — 명시적 future work: *"we plan to further extend DCDB … to support … sensors and performance events, such as those deriving from GPU usage"*
3. **retention / rollup / downsampling 논의 전무** (부재 확인)
4. **품질 축이 전혀 없음** — 탐지·진단 지표 0
5. **joint frontier 없음** — 비용은 특성화되지만 분석 가치와 교환되지 않는다

→ **`05` G11과 `06` C1을 다음으로 재작성해야 한다:** *"이 frontier의 **비용 측면은 확립되어 있고**(DCDB SC'19), **품질 측면도 별도로 확립되어 있으나**(Netti FGCS'20, Tuncer TPDS'19), **둘을 하나의 frontier로 결합한 연구가 없고, 네트워크/저장 비용 항과 GPU 차원을 추가한 연구가 없다."* 훨씬 방어 가능하고 공격이 어렵다.

**그리고 "LDMS SC'14 이후 아무것도 없다"는 서술은 삭제해야 한다.** DCDB SC'19가 SC'14보다 더 철저한 다중 rate 교란 연구다.

## 4.3 ✅ 유일하게 완전히 생존한 gap: retention resolution

> **TSDB retention resolution / rollup 정책 / downsampling 스케줄을 결정변수로 변화시키고 그 결과가 이상탐지 또는 RCA 품질에 미치는 영향을 측정한 peer-reviewed 논문을, 어떤 분야에서도 찾지 못했다.**

검색 결과 벤더 블로그(ClickHouse, Last9, Alibaba, VictoriaMetrics)만 나왔다. Crossref 제목 탐침 2회(`downsampling anomaly detection time series` 25건, `multi-resolution rollup retention time series database monitoring metrics` 25건) 모두 **해당 논문 0건**.

**단, "in ANY field"라는 표현은 falsified:**
- **Miao, Jigui 외 (2023), *Research on the Influence of Signal Sampling Frequency on Soft Fault Diagnosis Accuracy of DC/DC Converters*, CPSS Transactions on Power Electronics and Applications, `10.24295/cpsstpea.2023.00004`** — 샘플링 주파수를 독립변수로, **soft-fault 진단 정확도**를 측정. 비용 축 없음.
- **Zhong, Shuncong 외 (2011), *Sampling interval sensitivity analysis for crack detection by stationary wavelet transform*, Structural Control and Health Monitoring, `10.1002/stc.469`** — 샘플링 간격 민감도, crack **탐지**. 비용 축 없음.
(둘 다 metadata 수준 검증만. 수치는 `UNVERIFIED`.)

→ **정확한 표현: "metrics store의 retention/rollup 정책에 대해서는"이며, "어떤 분야에서도"는 쓰지 말 것.**

**거부한 near-miss와 이유:**

| 후보 | 왜 반례가 아닌가 |
|---|---|
| **Netti, Kiziltan, Babaoglu, Sîrbu, Bartolini, Borghesi, *A machine learning approach to online fault classification in HPC systems*, FGCS 2020, `10.1016/j.future.2019.11.029`, arXiv 2007.14241** — **전문 확인. 가장 위험했던 후보** | LDMS 1 s 고정, 집계 window 60 s / step 10 s **고정. 변화 없음, 민감도 연구 없음.** *"as the length of the aggregation window increases… more pronounced adverse effects on the classification accuracy"*라고 **정성적으로 주장하면서 실증 비교가 0이다.** → **이것은 반례가 아니라, 그 효과가 미측정임을 인정한 인용 가능한 선행연구다. 숨기지 말고 쓸 것** |
| Netti 외 Euro-Par 2019 (arXiv 1810.11208) | 동일. 1 s 고정, 60 s window 고정, 단일 CPU 노드(Xeon E5-2630 v3), GPU 없음 |
| Jiao 외, *Toward Quantity-of-Interest Preserving Lossy Compression for Scientific Data*, PVLDB 2023, `10.14778/3574245.3574255` | 파생량에 오차 bound를 묶는 가장 가까운 formulation. 그러나 QoI ≠ 탐지/진단 결과이고 변수는 압축 오차 bound이지 시간 해상도가 아니다 |
| Z-checker(IJHPCA 2017), Cappello 외(IJHPCA 2019), Lu 외(IPDPS 2018) | **복원/압축 오차만.** 규칙상 반례 아님 |
| AdaM(IEEE BigData 2015), *Low-Cost Adaptive Monitoring for IoT*(IEEE TSC 2021) | 적응 샘플링 rate vs 데이터/에너지 절감. 품질이 **스트림 복원 정확도(MAPE)**이지 탐지·진단이 아니다. retention 차원 없음 |
| Salim 외, NOMS 2016, `10.1109/noms.2016.7502890` | WBSN. 샘플링 감소 vs **event/emergency 탐지** — WSN 최근접. 그러나 비용이 에너지 한정, 진단 없음, 저장 retention 없음 |
| Sifter(SoCC'19), Tracemesh(IEEE CLOUD 2024) | trace 샘플링 예산 vs 이상 trace 보존. **binary keep/discard이지 *해상도*가 아니다.** metric이 아니라 trace, HPC 아님 |
| INT 오버헤드 감소 계열 | 대역폭 vs **측정 정확도**, spatial/flow 샘플링, **retention 차원 없음** |
| Monarch(Google), Gorilla, ByteSeries, TimeUnion, ModelarDB, Timon | **`UNVERIFIED` — DB venue 색인 접근 불가.** rollup/retention 메커니즘을 *기술*하지만 하류 분석 품질을 평가하지는 않는 것으로 기억됨. **VLDB/SIGMOD 스윕이 남은 최대 구멍** |

## 4.4 ⚠️ 채택해야 할 formulation: AWStream (SIGCOMM'18)

**Zhang, Jin, Ratnasamy, Wawrzynek, Lee, *AWStream: Adaptive Wide-Area Streaming Analytics*, ACM SIGCOMM 2018, `10.1145/3230543.3230554`.** 저자·venue·DOI 확인.

**왜 가장 위험한가:** AWStream은 **frame rate(= 시간 해상도)를 포함한 degradation knob 집합에 대해 애플리케이션 정확도 대 대역폭의 명시적 Pareto frontier를 프로파일링**하고 **실제 하류 분석 결과**(객체·보행자 탐지 정확도, F1)를 측정한 뒤 그 frontier 위에서 온라인 적응한다. **제안하려는 formulation과 구조적으로 동형이다.**

**AWStream이 다루지 않는 것 = 방어 가능한 delta:**
1. **retention/age 차원 없음.** knob이 *live* 스트림의 ingest 시점에만 작용한다. *어떤 해상도를 얼마나 오래* 보관할지에 대한 개념이 없다 — rollup 스케줄 없음, tiering 없음, age 의존 정책 없음. **영상 문헌 전체가 이 축을 갖지 않는다.**
2. **품질 = 탐지만.** **진단/RCA localization 품질 없음.**
3. **비용 = 대역폭(+일부 compute).** **애플리케이션 교란 항 없음** — 영상 소스는 관측 대상 워크로드와 동일 노드에 있지 않다. HPC에서는 수집기가 자신이 관측하는 애플리케이션의 사이클을 훔치고 jitter를 주입한다. **이 피드백 항은 AWStream에 등가물이 없다.**
4. 저장 비용 없음, 다년 비용 모델 없음.
5. 단일 테넌트 스트림 vs 시설 전체 telemetry(in-band + out-of-band + fabric).

같은 계열로 인용될 것: **Chameleon(SIGCOMM'18), Reducto(SIGCOMM'20), VideoStorm(NSDI'17), CASVA(INFOCOM'22, `10.1109/infocom48880.2022.9796875`), ILCAS(IEEE TMC 2024, `10.1109/tmc.2023.3327097`), AdaDSR(IEEE IoT-J 2024, `10.1109/jiot.2023.3331699`)**.

→ **논문 자세: 서론에서 AWStream을 채택하는 formulation으로 인용하고, delta를 (i) retention/age를 1급 knob으로, (ii) 교란을 비용 항으로, (iii) 진단을 품질 항으로 명시할 것. "미발표"라고 주장하면 desk reject를 부른다.**

## 4.5 GPU 교란 측정 gap — 생존하나 프레이밍은 falsified

**생존:** DCGM / Redfish / Slingshot telemetry를 갖춘 **현대 GPU 시스템**에서 샘플링 rate를 변화시킨 모니터링 교란 측정은 찾지 못했다.
**프레이밍 falsified:** "LDMS SC'14가 마지막/유일"은 거짓. **DCDB SC'19가 더 철저하다**(100 ms–1 s, 25 configs, CORAL-2 앱, 1024노드까지, 명시적 오버헤드 모델) — 다만 CPU 세대 하드웨어(Skylake/Haswell/KNL), GPU 없음.

**안전한 문구:** *"다중 rate 모니터링 오버헤드·애플리케이션 교란 측정은 CPU 세대 HPC에 존재하지만(Agelastos 외 SC'14; Netti 외 SC'19) GPU(DCGM)·BMC/Redfish·Slingshot telemetry를 갖춘 시스템에는 없으며, DCDB 저자들은 GPU 센서를 future work로 명시한다."*

**⚠️ 미해결 위험 (주장 전 확인 필수):**
| 우선순위 | 대상 | 왜 |
|---|---|---|
| 1 | **PIKA CLUSTER'20 PDF** (`10.1109/cluster49012.2020.00061`, Unpaywall `oa_status: closed`) | TU Dresden **Taurus는 GPU 파티션이 있었다.** 1개 이상 rate에서 GPU 모니터링 오버헤드를 보고했다면 **이 gap이 죽는다** |
| 2 | **Tuncer TPDS'19 PDF** | 민감도 연구가 *window 크기*가 아니라 *샘플링 간격*을 변화시켰다면 C-08의 HPC 사례가 크게 약화 |
| 3 | **VLDB/SIGMOD/ICDE/EDBT/CIDR의 rollup·retention 스윕** | **미검색 최대 영역** |
| 4 | Wintermute HPDC'20, ExaMon DATE'17, LDMSCON 2015–2025, CUG monitoring track | grey/workshop 문헌이 GPU 오버헤드-rate 표가 숨어 있을 정확한 장소 |
| 5 | **Hindsight NSDI'23** | 발표된 "retention as decision variable"의 최근접(단, trace이고 binary) |

## 4.6 판정 — 5개 zero 하위주장

| # | 하위주장 | 판정 |
|---|---|---|
| 1 | HPC 시스템에 telemetry 비용 대 하류 품질 Pareto frontier 0편 | **HPC 한정 SURVIVES.** 단 §4.2에 따라 재작성 필수. HPC 밖에서는 거짓(Kestrel Fig.5, Gleaner Fig.4+Table 6, Mint Table 3) |
| 2 | 샘플링 간격 변화 0편 | **FALSIFIED.** HPC 안에서도 부분 falsified(LDMS SC'14, DCDB SC'19 — 단 품질 미측정). 재작성: *"샘플링 간격을 변화시키면서 하류 분석 품질을 측정한 HPC 논문이 없다"* |
| 3 | **retention 해상도 변화 0편** | **✅ 최강 생존.** 유일하게 전역적으로 생존. "in ANY field"만 삭제 |
| 4 | telemetry rate 함수로서 탐지 지연 0편 | **FALSIFIED**(Kestrel). HPC 한정 생존 |
| 5 | 축소가 RCA에 미치는 비용 측정 0편 | **FALSIFIED — 가장 약한 하위주장.** HPC 한정으로만 방어 가능 |

**순 결과: 5개 중 2개가 무조건 생존(#3 전면, #1 범위 한정), 3개는 명시적 HPC 범위 한정이 필요하다.**

---

# §5. Cross-layer RCA: **FALSIFIED as stated**

## 5.1 🚨 Beacon — 가장 심각한 반례

**Yang, Ji, Ma, Wang, Zhang, Zhu, El-Sayed, Lan, Yang, Zhai, Liu, Xue, *End-to-end I/O Monitoring on a Leading Supercomputer*, USENIX NSDI'19.** 소속: **National Supercomputing Center in Wuxi**, Tsinghua, Shandong Univ., QCRI, Emory.

- **기판: Sunway TaihuLight, 40,960 노드** (발표 시점 세계 3위)
- **compute nodes → forwarding nodes → storage nodes → metadata servers** 4계층을 명시적으로 계측하고 상관
- 시스템 데이터로부터 애플리케이션 수준 I/O 행동을 재구성
- **aggressive online + offline trace compression + distributed caching/storage**로 production 오버헤드 억제
- **18개월 production 배포.** 설정 오류, 이상, 성능 간섭, 자원 프로비저닝 문제를 실제로 발견

→ **C-12("cross-layer RCA를 production 슈퍼컴퓨터에서 한 연구가 없다")와 C-06의 HPC 부분("telemetry 비용이 HPC에서 미연구") 양쪽을 동시에 공격한다.**

**Beacon이 하지 않는 것:** I/O 스택 한정 — CPU/GPU/전력/열/fabric 융합 없음; 티켓 기반 ground truth 없음; 자동 remediation 없음(진단하고 사람이 조치); cross-system 전이 없음; 형식적 causal model 없음.

→ **정확한 잔존 주장:** *"**compute + facility + fabric + storage + scheduler**를 아우르며 형식적 causal model을 갖는 cross-layer RCA는 미해결이다."* **삭제하지 말고 좁힐 것.**
그리고 **비용 측면:** Beacon의 핵심 엔지니어링 기여가 40,960노드 모니터링을 낮은 오버헤드로 유지하기 위한 압축·캐싱이다. 최적화 연구로 프레이밍되지 않았어도 비용-품질 엔지니어링 결과다. → *"어떤 HPC 연구도 샘플링 rate·metric 선택·retention horizon의 함수로서 품질/효용 frontier를 체계적으로 특성화하지 않는다"*가 방어 가능한 잔존 형태다.

## 5.2 가장 가까운 published neighbour — 그리고 그것은 한국 논문이다

**Kang, Hwang, Lee, Kim, Koo, Shin, Kang, Kang, Heo, Kim, Lee, Yang, Cho, Song (14인), *From Detection to Recovery: Operational Analysis on LLM Pre-training with 504 GPUs*, arXiv:2605.09370** (v1 2026-05-10, v5 2026-06-15), **Lablup + SKT + Upstage + NVIDIA Korea + VAST Data**. **Lablup 기술보고서 / arXiv preprint — peer-review 아님.** 42pp, 19 figs, 16 tables.

- 63노드 NVIDIA B200, 504 GPU. **751 metric**, **30초 간격**, **Prometheus 55일 + 운영 로그 73일, 224개 multi-node 학습 세션**
- 계층: DCGM(temp/power/ECC/**XID**/NVLink) + node_exporter(CPU/mem/disk/net/**IB**/NFS) + all-smi(chassis) + **Backend.AI 스케줄러 metric** → **5계층, 스케줄러 포함**
- 확인된 핵심 결과: **751개 metric과 XID로 식별된 GPU 장애 10건에 대해 어떤 단일 metric도 장애 유형 간에 일관되게 지배적이지 않다** → 다중 신호 탐지 필요; checkpoint 523건을 GPU VRAM→NFS로 추적, restart load = 최대 read 대역의 **21.5%**, save burst = 최대 write의 **16.0%**; 노드 exclusion이 집중됨(**63노드 중 상위 3개가 >50%**); auto-retry chain **33.3% 성공(12 chain/73 attempt) vs 수동 12.5%**, median retry interval 11분
- **L3 + L5-descriptive + L7-measured.** 기존 closed loop(auto-retry)를 *관찰하고 효능을 정량화*하며, 새로 제안하지는 않는다
- production 데이터 ✅, production 배포 ✅(모니터링 파이프라인이 5개 조직에 걸쳐 live)

**하지 않는 것:** 형식적 RCA 알고리즘·causal model 없음; layer-graph/dependency formalism 없음; telemetry 비용-품질 연구 없음(751 metric은 소비되지 그 예산이 정해지지 않음); 운영자 확인 incident label set 없음; 클러스터 간 전이 없음; **N=1 클러스터, 63노드 — Nurion/KISTI-6보다 두 자릿수 작다**; peer-review 아님; 스토리지가 NFS/VAST이지 Lustre/GPFS 아님; **fabric counter 분석 없음**(IB/Slingshot telemetry 없음).

→ **반드시 인용하고 차별화할 것.** §0.1 F-2의 수치 오류를 조심할 것.

## 5.3 계층/깊이별 반례 정리

**L = 계층 범위**(L0 단일 · L1 2계층 · L2 3+계층 · L3 스케줄러+전력 포함 전스택) · **D = 깊이**(D1 탐지 · D2 국소화 · D3 원인귀속 · D4 조치)

| 연구 | Venue | L | D | 융합 계층 | Ground truth | 하지 않는 것 |
|---|---|---|---|---|---|---|
| **Beacon** | NSDI'19 | L2(I/O 스택 내) | D3 | compute+forwarding+storage+metadata | production 진단 사례 | CPU/GPU/전력/fabric 없음; 티켓 없음; 조치 없음 |
| **Kaleidoscope** | SC20 | L2(스토리지 스택 내) | D3 | client I/O + 네트워크 경로 + 스토리지 perf·RAS | **843건 운영자 확인** | GPU/스케줄러/전력 없음; 조치 없음. 99.3%/95.8%, <0.01% 오버헤드 |
| **ClusterRCA** | ISSRE'25 | L1 | D3(+fault type) | NIC 176 + compute 38 metric + 로그 105,095건 + **네트워크 topology** | 운영자 라벨 culprit node + 장애 유형; 739 장애/117 정상, 6 앱 | **네트워크 전용.** GPU/Lustre/스케줄러/전력 없음. spine switch 제외. **AC@1 0.98, Avg@5 0.9962** |
| **ARGUS** | ATC 2026 (SIGOPS) | L1–L2 | D3(L1–L3 자동, L4–L5 수동) | GPU 커널 trace(CUPTI) + host Python stack(py-spy) + comm 커널 | production 사례 5건 | 스토리지/스케줄러/전력 없음; **FP/FN율 없음, 티켓 비교 없음**; 동기·반복 학습 전제. verbatim: *"No automated node isolation or drain actions are performed by the system itself."* |
| **504-GPU (§5.2)** | arXiv | **L3** | D1→D4 | 5계층, 스케줄러 포함 | production telemetry, W&B | §5.2 |
| **Host-Side Telemetry** | arXiv 2510.16946 | L2 | D3 | GPU NVML+NCCL 10 Hz, CPU eBPF, NET_RX, block I/O 100 Hz | **synthetic 주입** | **단일 노드.** fabric topology·Lustre OST/MDT·Slurm·CDU 없음. 81–88%, 6–8s 지연 |
| **PACE** | SC'25 Workshops | L2(facility만) | D3 | cooling+power+network facility | 미명시 | **job/애플리케이션 성능 전무.** HPE 주도(Prakash, Hong Enriquez, Serebryakov, Grant, Milojicic + Brewer/ORNL) |
| **TSLoc** | KDD 2026 | — | D2 | 다양한 metric의 universal normal-behavior 표현 | real-world | 노드 granularity만; 원인 클래스·계층 귀속 없음 |
| **FIRM** | OSDI'20 | L1 | D4 | microservice + 저수준 자원 경합 | 클라우드 벤치마크 | 클라우드; fabric/PFS/배치 스케줄러/facility 없음 |
| **WANDER** | arXiv 2506.04049 | L1 | D3(prescriptive) | **PM100(Marconi100, 231,116 job) + Fugaku F-DATA** | 없음(offline) | ⚠️ **"HPC에 counterfactual causal inference 없다"를 falsify한다.** 단 *runtime configuration knob* 결정지원이지 장애/저하 RCA가 아니며 placement·site-wide를 명시적으로 배제 |
| **BU/Sandia HPEC 2021** | HPEC | L1 | D4(optimize) | flits/s per node→parent-router link + MPI time-ratio | production 실행 | ⚠️ **"scheduler as causal variable"에 최근접.** 그러나 *prospective 최적화*이지 retrospective 귀속이 아니다. 11% 평균 / 34% 최대(miniMD) 개선 |
| **Graph Traversal Agent** | arXiv 2606.08590 | L2 | D3 | K8s 자원·서비스·알림·trace·로그·이벤트 typed multigraph | ITBench + ChaosMesh | 저자 스스로 일반화 불가 명시. **ablation: scenario hint 제거 시 entity F1 0.9474 → 0.6958** — 헤드라인의 대부분이 prompt 튜닝 |

**GNN RCA:** MicroEGRCL(ICSOC'22), MicroIRC(JSS'24), heterogeneous-GNN(Springer'25), GALR(Electronics'26), cloud-edge RCL(arXiv 2406.13604) — **거의 전부 microservice/cloud.** {CPU, GPU, fabric, PFS, scheduler, power}를 HPC에서 아우르는 GNN RCA는 `NO COUNTEREXAMPLE FOUND`.

## 5.4 Scheduler placement as causal variable — 좁혀서 생존

- **NOT FALSIFIED:** HPC 장애/성능저하 진단의 causal model 내부에서 스케줄러 배치 결정을 confounder로 조건화한 연구를 찾지 못했다. 조사된 모든 RCA 시스템은 스케줄러를 무시하거나(Kaleidoscope, ClusterRCA, ARGUS, Host-Side, LOGos, IBM interventional, FIRM, PACE, PeacLab 계열) **평범한 telemetry 스트림으로 흡수한다**(504-GPU의 Backend.AI metric).
- **PARTIALLY FALSIFIED — "아무도"라는 표현은 위험:** BU/Sandia HPEC 2021이 "배치가 job의 통신 성능을 바꾼다"는 causal 신념으로 할당에 개입한다(prospective). **WANDER는 실제 HPC job telemetry에 SCM + counterfactual을 적용한다** → "HPC에 counterfactual causal inference 없다"는 **falsified**. HPC 네트워크 경합 문헌(LLNL inter-job interference, Dragonfly contention, SC-W 2024 cross-application I/O interference, NSDI'19 end-to-end I/O monitoring)이 20년간 배치→성능 인과를 **비형식적으로** 확립해 왔다.

**안전한 재진술:** *"기존 HPC 진단 시스템은 스케줄러 배치를 모델링하지 않거나 평범한 telemetry feature로 취급한다. 어느 것도 서브시스템 상태가 job 성능에 미치는 causal effect를 추정할 때 배치를 confounder로 조건화하지 않는다."* — 이 형태는 falsify하지 못했다.

## 5.5 잔존 gap은 conjunction으로만 성립

| 요건 | 상태 | 최근접 |
|---|---|---|
| ≥4계층 순위 귀속 | 약하게 열림 | Host-Side(4계층, 단일노드, synthetic); 504-GPU(5계층, 순위 없음) |
| fabric link/switch-group granularity | 열림 | ClusterRCA(NIC-pair/switch-port, 네트워크 전용) |
| Lustre OST/MDT granularity | 열림 | Kaleidoscope(스토리지 내부, 스토리지 전용) |
| **scheduler placement를 causal variable로** | **열림 — 반례 없음** | HPEC'21(최적화), 504-GPU(feature) |
| CDU/전력 envelope | 약하게 열림 | PACE(job 성능 전무) |
| **운영자 확인 티켓 검증** | 약하게 열림 | Kaleidoscope 843건(스토리지), ClusterRCA 739+117(네트워크) — **단일 계층에서 이미 기준이 세워졌다** |
| closed-set 조치로 종결 | 약하게 열림 | FIRM(클라우드), 504-GPU(retry/exclude, 편익 미검증) |
| **종속변수 = 성능 저하, 장애 아님** | 열림 | ARGUS/Host-Side는 성능이나 fabric/FS/스케줄러/전력 없음 |

→ **join — 다중 테넌트 production HPC에서 성능 저하에 대한 cross-layer 순위 귀속을, 배치를 조건화하고, 티켓으로 검증하고, 조치로 종결하는 것 — 은 `NO COUNTEREXAMPLE FOUND`.** 개별 conjunct는 모두 최근접 이웃이 있으므로 **novelty는 join에 있고, 이는 방어 가능하지만 공격 가능한 위치다.**

## 5.6 최강 심사 반론

**#1 — 반대 증거가 이미 두 편 있고 둘 다 최신이다.**
> *"'Too Many Cooks'(ISSRE'25)는 multi-source fusion이 장애 진단에서 수익 체감 또는 음의 수익을 낸다는 것을 실증했고, 'How Far Can RCA Go'(2026)는 모든 고전 causal discovery 방법 — Granger, PC, FCI, LiNGAM, NTLR — 이 실제 telemetry에서 **Acc@1 0%**이며 병목은 데이터 가용성이 아니라 추론과 도메인 지식(overall reasoning gap 40.0% vs data ambiguity 1.4%)이라는 것을 보였다. 이 제출물의 전체 논지는 '계층을 더 넣자'다. 세 번째 소스 추가가 실패한 곳에서 여섯 번째 telemetry 소스 추가가 왜 성공하는가?"*

**답하지 않으면 논문이 죽는다. 필수 대응 3종:**
(a) **계층별 ablation** — 각 계층의 marginal value를, 음의 사례까지 정직하게 보고. 심사자가 가장 먼저 찾는다.
(b) **HPC의 *물리적* 구조가 바로 "How Far Can RCA Go"가 병목으로 지목한 domain knowledge를 공급한다는 논증.** fabric topology, OST map, CDU-rack mapping, 할당 기록. 마이크로서비스 topology는 논리적이고 계속 변하지만 **HPC topology는 고정적이고 알려져 있고 물리적으로 참이다.** ← **최고의 반박이며, 부정 결과를 위협에서 동기로 전환한다.**
(c) **raw telemetry에 고전 causal discovery 알고리즘을 적용하는 것으로 시작하지 말 것.** 그 구성은 이미 Acc@1 0%로 발표되었다.

**#2 — "Kaleidoscope를 여섯 번 돌린 것".** 답은 **cross-layer 귀속이 스케줄러 조건화를 요구하기 때문**이어야 한다 — 배치가 계층 간 spurious correlation을 유발하는 공통 원인이므로 어떤 per-layer localizer도 이를 할 수 없다. placement를 load-bearing으로 만들지 못하면 엔지니어링 통합으로 채점된다.

**#3 — ground truth 품질.** Kaleidoscope 843, ClusterRCA 739. 비슷한 N + 티켓 잡음(티켓은 *적용된 수리*를 기록하지 *원인*을 기록하지 않는다) + 불완전성(silent degradation은 티켓이 거의 없다 — **성능 저하 논문에는 실질적 sampling bias 문제**) + inter-rater agreement.

**#4 — counterfactual 증거 없는 조치.** 도움이 됨을 보이지 않은 closed action set은 결과가 아니라 권고다.

**#5 — 단일 시스템·비공개 데이터.** ClusterRCA가 정확히 이것으로 지적받았다.

**#6 — 타이밍/충돌.** ORNL SC26 논문이 11월에 Frontier 규모 데이터와 OLCF 운영자 ground truth로 나오면, 이후 제출물은 인용 여부와 무관하게 그것과 비교된다.

## 5.7 SC26 ORNL 논문 — `SC26-PARTIAL-EVIDENCE`

**검증된 사실만:**

| 항목 | 값 |
|---|---|
| 제목 | *From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System* ("System" 단수 — 두 출처에서 일치하므로 실제 제출 제목) |
| 저자 | Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin |
| 소속 | **Oak Ridge National Laboratory (6인 전원 단일 소속)** |
| 분류 | **Best Paper Nominee** — "Best Paper 또는 Best Student Paper 중 하나에 적격" 그룹이 아니므로 학생 저자 진출 없음 |
| 발표일 | SC26 공식 2026-08-13; HPCwire 재게재 2026-08-18 |
| 미해결 | 공식 페이지 헤더는 Best Paper Nominee "5편"이라 하는데 SC26·HPCwire 양쪽에 **4편만 열거** — 개수 불일치 |

**부정 결과 (전부 "NOT FOUND", "does not exist" 아님):** arXiv preprint 없음(제목·6인 저자명·인접 표현 전부 검색); ACM DL/IEEE Xplore에 SC26 proceedings 미존재; dblp에 Woong Shin의 2026 항목은 있으나(Wattchmen ICS'26, CoRR preprint 3건) 이 논문은 없음; Feiyi Wang dblp에 2026 항목 전무; ornl.gov staff profile·impact.ornl.gov에 해당 기록 없음(Khan의 2026 항목은 *FitCache*만); **OSTI.gov는 egress 정책으로 접근 불가 — 미확인으로 취급**; SC26 technical program 미공개(`sc26.conference-program.com` 401, 세션 스케줄은 "by September 2026" 예정); 워크숍/기술보고서 선행연구 없음.

**저자 계보 (검증됨 — 논문이 무엇일 수 있는지를 제약)**

| 저자 | 검증된 연구 정체성 | 최근접 공개 산출물 |
|---|---|---|
| Awais Khan | 스토리지/I-O/dedup/캐싱. impact.ornl.gov fingerprint: I/O 100%, filesystems 87%, dedup 84% | DEDUPKV(2025), FitCache(2026) |
| Woong Shin | 전력/에너지/열, ODA, digital twin | SC24-W *Navigating Exascale ODA*, ExaDigiT(2024), Wattchmen(ICS'26), ICS'25 전력 프로비저닝 |
| Ahmad Maroof Karimi | ODA + 운영용 생성 AI | **EPIC**(arXiv 2509.16212) — 계층적 multi-agent LLM ODA 플랫폼, Frontier 평가, LLM 비용 19× 절감, 정확도 +26% |
| Feiyi Wang | OLCF 그룹 리드; chatHPC(J. Supercomputing 2025) | — |
| Christopher Zimmer | Frontier 시스템 운영/스토리지 | FitCache 공저 |
| Anjus George | 스토리지/캐싱, Lustre | — |

**⚠️ 중요 정정:** PACE(*From Exploration to Explanation*, SC'25 Workshops, `10.1145/3731599.3767471`)는 **HPE 주도**이며 SC26 논문과 **저자 겹침 0**이다. ORNL 선행연구가 아니다. **SC26 논문을 PACE로 모델링하지 말 것.**

**⚠️ 아래는 추론이며 사실이 아님:** 제목이 주장하는 영역 — `alert fatigue` → 입력이 **운영 알림/이벤트 스트림**(RAS 로그, 콘솔 이벤트, 모니터링 알림)이고 연속 raw telemetry가 아니다; `causal failure cascade discovery` → 출력이 **장애/알림 이벤트에 대한 방향성 cascade 구조**; `root cause` → cascade의 종단 노드; `in HPC System` → 단일 시스템 검증, 거의 확실히 **Frontier**.
**남겨둘 가능성이 높은 것(경쟁 제출의 wedge):** ① **종속변수가 장애이지 성능이 아니다** — silent performance degradation은 알림을 전혀 발생시키지 않으므로 alert-fatigue 프레이밍 밖에 구조적으로 존재한다. **가장 강한 차별점.** ② 이벤트 스트림 ≠ 다계층 수치 telemetry. ③ job/테넌트 귀속. ④ 스케줄러 배치. ⑤ 조치.
**⚠️ 잔존 위험:** cascade graph에 Frontier DCGM + Lustre + Slingshot + 전력이 실제로 포함되어 있다면 차별화 대부분이 붕괴한다. **camera-ready 또는 SC26 스케줄 공개 전까지 falsify 불가.** 2026년 9월 말~10월에 `sc26.conference-program.com`·ACM DL 재확인, 그리고 접근 가능한 네트워크에서 OSTI 확인.

**⚠️ 포지셔닝 고려사항:** **Woong Shin은 SC26 best-paper nominee 공저자이면서 동시에 HPC-ODA 2026 공동 조직자다.** HPC-ODA에 cross-layer RCA를 제출하면 ORNL 저자들이 포함된 커뮤니티 안에서 처리된다. 부적절함이 아니라 포지셔닝 사항으로 인지할 것.

**HPC-ODA 2026 검증 사실:** 2026-11-20 금 08:30–12:30, Chicago. 1st **peer-reviewed** 판(선행은 BoF 9회: SC19, SC21, ISC21, SC22, ISC23, SC23, ISC24, SC24, SC25 "Mind the Gap"). 조직: **Michael Ott(LRZ), Ayse Coskun(BU), Jeff Hanson(HPE), Melissa Romanus(NERSC/LBNL), Woong Shin(ORNL), Tim Osborne(ORNL)**. 제출 2026-08-12, **통보 2026-09-04**, camera-ready 2026-09-18, lightning talk 통보 2026-09-25. 4p short / 8p full / 1–2p lightning, IEEE 템플릿, IEEE Xplore + SC26 워크숍 proceedings. **채택 논문 미공개**(통보 2일 전). 사이트 내부 불일치: events 페이지는 11/16, workshop 페이지는 11/20 — **11/20을 신뢰**.

---

# §6. Cross-system generalization: **WEAKENED**

## 6.1 반례

| 연구 | 실제로 건넌 경계 | 하지 않는 것 |
|---|---|---|
| **Farooq, Milano, Borghesi, *Federated transfer learning for anomaly detection in HPC systems: First real-world validation on a tier-0 supercomputer*, Expert Systems with Applications 2026, `10.1016/j.eswa.2025.129754`** | **cross-NODE** — federated 학습에 참여하지 않은 미지 노드로의 일반화. Marconi100 100노드 | 단일 시스템. cross-site 아님, cross-generation 아님. → **"유일한 측정치는 0.898→0.726"을 FALSIFY** |
| 동 저자, *Harnessing Federated Learning for Anomaly Detection in Supercomputer Nodes*, FGCS 2024, `10.1016/j.future.2024.07.052` | 노드 간 federated 학습 | 동일 |
| **CENTILE** (arXiv 2608.01725, Zhang, Hou, Ji, Liu) | **cross-DOMAIN**(ISP network ↔ HPC ↔ cloud VM) + Fugaku 내 cross-month zero-shot. adapter: *"a new telemetry source… is added by declaring its feature vector while the stages above it stay fixed"* | **multi-site HPC 전이 없음, 하드웨어 세대 전이 없음.** HPC modality가 **scheduler trace이지 수치 센서 telemetry가 아니다.** in-domain 대비 전이 열화를 정량화하지 않음. F-DATA(~117K job/월; replay 48,826 job/298 user/2주), CESNET-TimeSeries24, Azure VM CPU |
| **SeT-Diff** (ACM CF'26, `10.1145/3801487.3806064`, arXiv 2607.22548, Esposito, Antici, Cesarini, Bartolini) | **센서 순서 permutation만**(0.0472 vs 0.0470 MAE) + task-level zero-shot | **확인: cross-system 없음, cross-generation 없음, 실제 schema 마이그레이션 없음.** 단일 시스템 chronological split. M100 ExaData 261 센서 20개월 |
| **DSN'24 Huawei, *Investigating Memory Failure Prediction Across CPU Architectures*** (arXiv 2406.05354) | ⚠️ **경계를 건너지 않는다.** 아키텍처별 **별도 모델**(Intel Purley, Intel Whitley, Huawei K920 ARM). 논문 자체가 *"Data Scientists might develop various models designed to distinct CPU architectures, utilizing unique features for each"* | X86→ARM 전이 실험 없음; 전이 penalty 보고 없음. ~250K 서버, >90K DDR4 DIMM, 2023-01~10 |
| **Prodigy** (SC'23) | **경계 없음.** Eclipse F1 0.95, Volta F1 0.88을 **독립적으로** 5-fold CV | **두 시스템 데이터를 다 가지고도 train-Eclipse→test-Volta 실험을 하지 않았다** |
| **REFINE** (ISC HPC'26, PeacLab) | 없음. 동일 | 한 세대 뒤에도 같은 gap |
| **NCSA Delta GPU resilience** (arXiv 2503.11901v2) | **3개 GPU 세대 공존(A40/A100/H100)** — 그러나 특성화만. 1,168 GPU, 855일 | **모델 없음.** 예측 없음, 전이 없음. SRE drain/reboot 수동 |
| Disk TL, IEEE Trans. Reliability 2020, Xplore 9057467 | **cross-disk-model/vendor 전이 — 발견된 유일한 진짜 수치 telemetry 전이** | 스토리지 도메인, HPC 아님; 단일 운영자; cross-site 아님, schema 변경 아님. 내용 `UNVERIFIED` |

**부정 결과:** **HPC-ODA "cross-architecture" 세그먼트로 cross-architecture *전이* 결과를 발표한 논문 `NO COUNTEREXAMPLE FOUND`.** M100 ExaData + F-DATA를 함께 쓴 논문 없음. **1개 이상의 공개 수치 telemetry 데이터셋으로 전이를 한 HPC 논문 없음.**

## 6.2 HPC-ODA 세그먼트 5의 정확한 내용 (검증)

| # | 세그먼트 | 내용 |
|---|---|---|
| 1 | Power Consumption Prediction | fine granularity, 단일 노드, 노드+per-core metric, 회귀 target = 노드 전력 |
| 2 | Fault Detection | medium, 단일 노드 fault injection, 노드 metric + **애플리케이션·결함 라벨** |
| 3 | Application Classification | medium, **16 compute 노드**, 병렬 MPI 앱, 노드 분리 데이터 + 앱 라벨 |
| 4 | Infrastructure Management | coarse, **클러스터 전체**, 온수 냉각 + rack 전력; target = **출수 온도, 제거 열량** |
| 5 | **Cross-architecture** | ⚠️ **세그먼트 3의 변종** — 동일 앱의 단일 노드 구성을 **CPU 아키텍처가 다른 3종 compute 노드 타입**에서 실행. cross-architecture 분류·전이 연구용. **GPU/accelerator 세그먼트가 아니고, cross-*system* 세그먼트도 아니다** |

## 6.3 판정과 잔존 주장

| 하위주장 | 판정 |
|---|---|
| (a) 두 HPC 사이트 간 전이 penalty 측정 0편 | **SURVIVES** — CENTILE·SeT-Diff·Prodigy·REFINE 모두 할 데이터가 있었고 하지 않았다 |
| (b) 두 GPU 세대 간 | **전이 주장으로는 SURVIVES; novelty로는 WEAKENED**(Delta 3세대 공존 특성화가 이미 발표) |
| (c) 두 fabric 세대 간 | **SURVIVES** — 어느 방향으로도 없음 |
| (d) telemetry schema 변경 | **WEAKENED** — SeT-Diff(semantic conditioning)와 CENTILE(feature-vector 선언 adapter)이 *메커니즘*을 이미 출시. 어느 쪽도 penalty를 측정하지 않음 |
| "수치 HPC telemetry는 미개척" vs 로그는 CLOSED | **WEAKENED** — CENTILE이 cross-domain 전이를 명시 주장하는 수치/이벤트 telemetry foundation model이며 HPC 의사결정으로 평가된다 |
| "유일한 측정치는 0.898→0.726" | **FALSIFIED** — Farooq ESWA 2026이 미지 노드 일반화를 정식 저널에 보고(F1 최대 0.50 향상). 그리고 **0.898/0.726 수치 자체가 이 세션에서 `UNVERIFIED`**(AI4Sys'23 원문 미확보) |

**최강 거부 무기 — CENTILE:**
> *"수치 운영 telemetry에 cross-boundary 전이 문헌이 없다는 주장은 과장이다. CENTILE(2026)은 HPC job telemetry(F-DATA/Fugaku), ISP backbone traffic(CESNET-TimeSeries24), cloud VM 이용률에 걸쳐 단일 telemetry foundation model을 pretrain하고, zero-shot 시간 전이와 목표 도메인 수 시간 데이터로부터의 cross-domain weight 전이를 보고하며, 새 telemetry 소스를 feature vector 선언만으로 온보딩하도록 설계된 adapter를 갖는다. M100 ExaData에서 semantic sensor conditioning으로 schema-permutation invariance를 이미 실증한 SeT-Diff(CF'26)와 합치면, 저자들이 도입하려는 메커니즘은 이미 발표되어 있다. 사이트 경계를 건너 기존 기계를 돌리고 delta를 보고하는 것을 넘어 무엇이 새로운지 밝혀야 한다."*
보조: **Prodigy(SC'23)** — "저자들 자신이 인용한 baseline이 이미 두 시스템에서 평가한다."

**잔존 주장 (검증 가능):**
> 수치 telemetry 운영 모델을 (시스템 A 학습) → (시스템 B 평가)로 평가하고, A≠B가 실제 사이트·GPU 세대·fabric 세대 경계일 때의 **정량적 열화 곡선**과 **in-domain 성능 회복에 필요한 목표 도메인 데이터량**을 함께 보고한 발표 연구가 없다.

**더 날카로운 형태:** 이 분야는 **per-system F1 쌍**(Prodigy 0.95/0.88; DSN'24 0.64/0.50/0.54)을 발표하지만 **그 행렬의 off-diagonal을 절대 발표하지 않는다.** off-diagonal이 기여다.
→ **최강 프레이밍은 새 모델이 아니라 *transfer-penalty matrix를 벤치마크 artifact로*** 만드는 것이며, 가장 값싼 방어 가능 실현은 Eclipse↔Volta(Prodigy/REFINE 데이터 존재) 또는 M100↔Fugaku(공개)다.

---

# §7. Safe remediation: **핵심 비용모델 주장 FALSIFIED**

## 7.1 반례 — 그리고 그것은 census 자신의 인용이다

**HPDC'24 BSC (§3.2)가 census가 없다고 말한 비용 모델을 정확히 갖고 있다:**
- 실제 Tier-0 HPC 시스템 필드 데이터 위의 **학습된(RL) remediation 정책**
- **lost node-hours = nodes × wallclock lost**
- **mitigation cost를 2/5/10 node-minutes로 스윕**
- **checkpoint-restart 의존성 모델링**(mitigation에서 resume vs 전체 재시작 분기)
- **MareNostrum 4 Slurm 로그(2018-03~2019-03)에서 가져온 배치 job mix**
- RL 학습 오버헤드 amortize: 연 **20 node-hour 미만**
- **결과: *"reduces lost compute time by 54% compared with no mitigation and is just 6% below the optimal Oracle method"***
- **DRAM 제조사 간, job 크기 10× 범위에서 정책이 일반화**된다고 보고 ← **Axis D 논문 안에 있는 Axis C 성격의 결과이며, 발견된 HPC 운영 모델 전이 결과 중 최근접**

**추가 반례:**
- **SC'20 Cost-Aware Prediction of Uncorrected DRAM Errors in the Field**(`10.5555/3433701.3433782`, github `bsc-mem/UEPREDICT`) — HPC remediation 비용 모델을 **2020년까지 밀어 올린다**
- **arXiv 2607.20005 *Safe Remediation as Risk-Constrained Intervention Decision in Microservice Systems*** (Chengxiao Dai, Zhaokun Yan, Chenjun Lei, Qiao Li, Luyan Zhang, 2026-07-22). **모든 요소 verbatim 확인: CMDP with bounded FRR; `ℒ(θ,λ)=𝔼[Q_θ(s,a)]−λ(𝔼[c(s,a)]−ϵ_safe)`; inference-time filter `π(s)=arg max_a Q(s,a) s.t. r(s,a)⪯τ(s)`; risk triad "blast radius, reversibility, and epistemic uncertainty"; action set `𝒜=𝒜_exec ∪{a_escalate, a_wait, a_noop}`; Train Ticket + Chaos Mesh + RCAEval taxonomy.** 결과: **FRR −39%, repair success +2.5pt, escalation load −17%.** → **프레이밍 전체를 선점한다.** 마이크로서비스 한정, 시뮬레이션.
- **DeepMind DC cooling (2018, 비peer-review 블로그)** — **L7/D5 production 학습 정책** + 안전 스택 전체: uncertainty 추정 → 저확신 조치 제거, 2계층 검증(cloud + local controller), 지속적 제약 모니터링, **중립 상태로 자동 failover**, smooth-transition failover, heuristic backup, **운영자 상시 이탈 가능**. 9개월간 냉각 에너지 ~30% 절감. **냉각 플랜트이지 노드 remediation이 아니고, peer-review도 아니며 FP/정확도 수치 없음.**
- **NENYA (KDD'22, Microsoft M365)** — 클라우드 production의 cost-aware RL mitigation.

**⚠️ FALSE POSITIVE 경고:** arXiv **2608.07440 "Blast Radius"**는 **LLM-agent context eviction**(SWE-agent용, Pitsane & Mogale) 논문이며 시스템 운영과 무관하다. **인용하지 말 것.**

## 7.2 부정 결과 (검증)

- **자동 drain 정책을 정확도/FP 수치와 함께 발표한 HPC 센터: `NO COUNTEREXAMPLE FOUND`.** 최근접은 Mueller 그룹 *Reducing False Node Failure Predictions in HPC*(Xplore 8990497) — 예측 측 FP 감소이지 *배포된 drain 정책의* 운영 FP율이 아니다. 벤더/센터 자료(Azure CycleCloud NHC+Slurm 통합, Delta SRE 실무)는 메커니즘을 문서화하고 정확도 수치는 0이다. **ORNL Frontier checknode 관찰이 일반화됨을 확인.**
- **HPC 스케줄링/운영에서 blast radius를 1급 비용으로 다룬 연구: `NO COUNTEREXAMPLE FOUND`.** 유일한 blast-radius-as-risk 형식화는 arXiv 2607.20005이며 마이크로서비스다.
- **자동 운영 조치의 provenance / audit trail: 벤더 마케팅만.** 학술 연구 없음. 진짜 gap.
- **시스템 운영 정책의 off-policy evaluation:** OPE 문헌은 recsys/광고. HPDC'24는 **OPE를 쓰지 않는다**(on-policy replay + nested CV). arXiv 2607.20005은 retrieval-augmented counterfactual aggregation이며 형식적 IPS/DR estimator가 아니다. **진짜 gap.**
- **링크 저하 시 네트워크 rerouting을 학습된 closed-loop 조치로:** 없음.

## 7.3 판정

| 하위주장 | 판정 |
|---|---|
| SC'08 → JPDC'12 → HPDC'20 계보가 production에 도달 못함 | **SURVIVES** |
| HPDC'20은 순수 SimPy 시뮬레이션이며 예측 정확도를 *가정* | **VERIFIED — verbatim으로 생존.** *"It is assumed here that the accuracy is high [7] and lead times are reliable except for a few outliers [6]."* 배치 스케줄러 requeue 비용·할당 오버헤드 미모델링 |
| **배치/할당/체크포인트 환경의 remediation 비용 모델 없음** | **FALSIFIED.** 삭제하거나 **조치 클래스**로 좁힐 것 |
| 학습된 정책의 D5를 실증한 HPC 시스템 없음 | **HPC에는 SURVIVES.** 일반적으로는 **WEAKENED**(DeepMind 냉각, NENYA) |

## 7.4 잔존 주장 3개 (강도 순)

1. **조치 클래스 gap.** HPC remediation 비용 모델은 정확히 한 조치(DRAM UE mitigation)에만 존재한다. **node drain, job requeue, quarantine, link rerouting, power capping**에 대한 발표된 비용 모델이 없다.
   **검증법:** drain/requeue 비용 모델을 구축하고 HPDC'24의 node-hours formulation으로 환원되지 않음을 보인다 — 구체적으로 **queue-position 손실, fairshare/할당 charge-back, reservation fragmentation**이 HPDC'24 formulation이 표현할 수 없는 비용 항임을 보인다.
2. **평가 방법론 gap.** HPC 운영 remediation 연구 중 **off-policy evaluation**을 쓴 것이 없다.
   **검증법:** 센터의 과거 조치 로그로부터 후보 drain 정책의 가치를 형식적 DR/IPS estimator + 신뢰구간으로 추정하고, 그 bound가 production rollout을 gate할 만큼 tight함을 보인다.
3. **책무성 gap.** 어떤 센터도 자동 조치 정책을 FP율과 함께 발표하지 않고, HPC에서 자동 운영 조치의 **provenance/audit**을 다룬 학술 연구가 없다.
   **검증법:** drain 정책을 측정된 FP율, 잘못 제거된 node-hours, 그리고 각 조치를 그것을 촉발한 telemetry window와 모델 버전에 연결하는 provenance 기록과 함께 발표한다. ← **가장 논쟁이 적고 운영상 가장 신뢰 가능한 기여이며, 기존 인용으로 심사자가 거부할 수 없는 유일한 것이다.**

---

# §8. Lineage: **부분 FALSIFIED — census의 가장 큰 사실 오류**

## 8.1 세 개의 명명된 도구가 아카이브 정규 논문을 갖고 있다

### ① LDMS — 끊기지 않은 사슬. 주장 **결정적으로 반박됨**

출처: [OVIS publications archive](https://ovis.ca.sandia.gov/publications-presentations-archive/), [ovis-publications wiki](https://github.com/ovis-hpc/ovis-publications/wiki)

```
DSN'12   Filtering Log Data: Finding Needles in the Haystack (Yu, Zheng, Lan, Jones, Brandt, Gentile)
SC14     LDMS: A Scalable Infrastructure for Continuous Monitoring... (Agelastos et al.)
Cluster'15  Toward Rapid Understanding of Production HPC Applications and Systems
Parallel Computing 2016  Continuous Whole-System Monitoring (저널 확장)
ISC'17   Diagnosing Performance Variations in HPC Applications Using ML — GAUSS AWARD
TPDS'18  Online Diagnosis of Performance Variation in HPC Systems Using ML (저널 확장)
Euro-Par'18  Taxonomist: Application Detection through Rich Monitoring Data — Best Artifact
Cluster'18   A Methodology for Characterizing Real vs Proxy Applications
ICPP'18/'19  Integrating Low-latency Analysis into HPC System Monitoring; HPAS anomaly suite
TOMPECS'19   Production Application Performance Data Streaming for System Monitoring
NSDI'20  ★ Measuring Congestion in High-Performance Datacenter Networks (Jha, Gentile, Brandt, Patke, Lim, Bauer, Showerman, Kaplan, Kalbarczyk, Kramer, Iyer)
ICS'21   ★ Delay Sensitivity-driven Congestion Mitigation for HPC Systems (Patke, Jha, Qiu, Brandt, Gentile, Greenseid, Kalbarczyk, Iyer)
```

**ICS'21 직접 확인**(par.nsf.gov/servlets/purl/10292980): *"network telemetry data … aggregated … by the Lightweight Distributed Metric Service (LDMS)"*를 Cray Aries에서 사용, Sandia **Voltrino** testbed와 NERSC **Cori**(130,560 링크, Dragonfly)에서 평가. **운영 모니터링 → 최상위 아카이브의 정확한 사례.**

**부차 정정: BU/Coskun 계보는 ISC'21 Proctor에서 시작하지 않는다.** 기원은 Sandia/LDMS 협업 **ISC'17 Tuncer → TPDS'18 → Euro-Par'18 Taxonomist**로, census가 잡은 시작점보다 4년 이르다.

### ② PIKA — 창립 논문이 IEEE Cluster 2020이다
**PIKA: Center-Wide and Job-Aware Cluster Monitoring**, Dietrich, Winkler 외, IEEE Cluster 2020, [Xplore 9229636](https://ieeexplore.ieee.org/document/9229636). → 주장 반박.

### ③ XDMoD Application Kernels — 아카이브 논문 3편
Cluster'15 `10.1109/CLUSTER.2015.114`; Simakov 외, *Concurrency & Computation* 2015 `cpe.3564`; Furlani 외, *C&C:P&E* 2013 `cpe.2871`. → 주장 반박.

### 부분 반박 2건
- **Arbiter (Utah)**: SC/HPDC/IPDPS/Cluster/DSN는 없으나 **ACM 아카이브 논문 존재 — PEARC'19 `10.1145/3332186.3333043`**. → 주장 **한정 필요**.
- **LLview (JSC)**: *Supporting HPC Users with LLview*(Guimarães, Sankaran, Frings), ISC High Performance 2025, Springer LNCS 16091, `10.1007/978-3-032-07612-0_4`. 본트랙 vs 워크숍 볼륨 `UNVERIFIED`. → 주장 **한정 필요**.

## 8.2 census가 놓친 검증된 lineage 6건

| # | Lineage | 상태 |
|---|---|---|
| 1 | **OLCF GPU 신뢰성.** Titan GPU 운영/교체 기록 → **SC20 본트랙** *GPU Lifetimes on Titan*(data+code `olcf/TitanGPULife`, OSTI 1657202) → Summit XID/DBE 데이터셋 공개 `10.13139/OLCF/1970187`(2023-04) → **ICS'24** *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*(Schmedding, Shin, Oles, Ostrouchov, Smirni, Wang, `10.1145/3650200.3656615`) | **VERIFIED — 완전한 ops→archival→dataset→archival 순환** |
| 2 | **OLCF 전력/열.** Summit 1 Hz BMC telemetry → **SC21 본트랙** `10.1145/3458817.3476188` → 데이터셋 `10.13139/OLCF/1861393`(2022-04) → **SMC Data Challenge 2022** → SC24-W ODA + **ICS'25** 전력 프로비저닝 | **VERIFIED** |
| 3 | **LLNL 전력/모니터링.** **IEEE Cluster'21** *Monitoring Large Scale Supercomputers: A Case Study with the Lassen Supercomputer*(Patki 외, Xplore 9555952, LLNL-CONF-822940) → **ICS'25** *A Global Perspective on Supercomputer Power Provisioning*(`10.1145/3721145.3734532`) | **VERIFIED.** ICS'25가 Cluster'21을 선례로 인용[ref 57]. LLNL/HPE/Bologna/CSC/NVIDIA/ORNL/LBNL/HLRS 16인; Perlmutter·Cori·Summit·Sierra·Marconi-100·LUMI·Hawk; **LDMS·ExaMon·DCDB·IBM CSM·Splunk·Redfish를 하나의 아카이브 논문으로 융합** — Sandia·Bologna·LRZ 도구 계보의 수렴점 |
| 4 | **NERSC 운영 데이터.** Perlmutter production 이용률 → **ISC High Performance 2023 본트랙** *Analyzing Resource Utilization in an HPC System: A Case Study of NERSC's Perlmutter*(Li, Michelogiannakis, Cook, Cooray, Chen, `10.1007/978-3-031-32041-5_16`, LNCS 13948, arXiv 2301.05145) | **VERIFIED** |
| 5 | **LANL queue-wait.** **PEARC'24** *Quantifying Uncertainty in HPC Job Queue Time Predictions*(`10.1145/3626203.3670627`) → **IEEE Cluster'25** *Are We There Yet?*(Xplore 11186489) + PEARC'25 `10.1145/3708035.3736067` | **PROBABLE.** 두 논문 존재 확인, 저자 목록 `UNVERIFIED`(403) |
| 6 | **ExaDigiT 전방.** SC24 digital twin(arXiv 2410.05133) → **NeurIPS 2025** *LC-Opt: Benchmarking reinforcement learning…*(Naug 외) | **NEW — 아카이브 후속 존재**(exadigit.github.io) |

## 8.3 ⭐ 진짜 패턴 — census가 주장해야 할 것

**다리는 워크숍 논문이 아니라 *데이터셋*이다.**

승격이 실제로 일어나는 경로: **시설이 telemetry 아카이브를 인용 가능한 데이터셋으로 공개 → 외부 연구자를 끌어들임**(Summit 데이터에 대한 Smirni 그룹, ICS'25의 7-시스템 컨소시엄). HPCSYSPROS/HPCTESTS/CUG는 실제로 거의 승격하지 않는다.

**확인된 최강 부정 사례 — 벤더/시설 도구 보고서는 전부 종단이다:** buildtest(최고 venue = Springer LNCS *워크숍* 볼륨, HUST/SE-HER/WIHPC 2019 `10.1007/978-3-030-44728-1_1`), OMNI(ICPP 2019 Workshops `10.1145/3339186.3339213` + 도서 챕터), STREAM(OSTI 1995656), EPIC(arXiv 2509.16212), ORNL ODA dashboard(SC24-W `10.1109/SCW63240.2024.00226`), EMOI(CUG'24), trellis(CUG'21), CADDY(CUG'24), Ezell health checking(CUG'23), Hagerty defective-hardware(SC23-W HPCTESTS, OSTI 2224160), Holmen network twin(CUG'24). **ExaDigiT 역방향 선행연구도 확인: 최초 발표 항목이 2024년 — census의 "워크숍 선행연구 없음"을 확인.**

`UNVERIFIED`: LANL syslog HPCSYSPROS23(Quan/Howell/Greenberg — 해당 인용에서 논문을 찾지 못함), Aurora failure management 선행연구, LLNL *Breaking the System Noise Barrier* SC25 선행연구, Benchpark(HPEC 2025만).

---

# §9. ⭐ 가장 중요한 발견: KISTI의 국내 선행 연구

**`00`–`07`은 이것을 전혀 다루지 않았다. 이것은 심각한 누락이다 — 국내 선행연구를 인용하지 않은 논문은 심사 이전에 신뢰를 잃는다.**

**KISTI는 이미 10년 이상의 운영 분석 발표 계보를 갖고 있다.** 중심은 한 그룹: **Ju-Won Park(박주원, 주저자)**, **Taeyoung Hong(홍태영)**, **Jae-Kook Lee**, **Xin Huang**, **Min-Woo Kwon**, **Joon Woo**, **JunWeon Yoon**, **ChanYeol Park**.

| # | 논문 | 저자 | 연도 | Venue | DOI | L | 무엇을 하는가 / 무엇을 안 하는가 |
|---|---|---|---|---|---|---|---|
| **K-1** | **Analyzing and predicting job failures from HPC system log** | Ju-Won Park, Xin Huang, Chul-Ho Lee | 2024 (online 2023) | **J. Supercomputing 80(1)** | `10.1007/s11227-023-05482-y` | **L4** | **KISTI 시스템 로그로 job 실패 예측. 가장 직접적인 국내 선례 — 반드시 인용·차별화.** cross-layer 융합 없음, RCA 없음, remediation 없음, telemetry 비용 분석 없음 |
| **K-2** | **Correlation Analysis of Event Logs for System Fault Detection** | Ju-Won Park, Eunhye Kim, Jaekeun Yeom, Sungho Kim | 2016 | J. Soc. Korea Industrial & Systems Engineering 39(2) | `10.11627/jkise.2016.39.2.129` | L3/L5-lite | **multi-source 이벤트 상관 — cross-layer RCA의 개념적 국내 선례.** 국내 venue, 소규모, 계층 모델 없음, 티켓 라벨 없음 |
| **K-3** | **Policy-aware GPU resource allocation for national supercomputing** | **Hyungwook Shim (KISTI)** | **2026** | **Scientific Reports** | `10.1038/s41598-026-42625-6` | **L6/L7** | ⚠️ **KISTI에 이미 closed-loop 컨트롤러 논문이 있다.** Neuron GPU 로그 + NERSC. MAE 8.03%→1.30%, 이용률 >92%. **1주 horizon / 4시간 간격 시뮬레이션, 배포 아님.** 장애 기반 아님; anomaly/RCA 없음; 제어 대상이 정책 정합성이지 incident remediation이 아님 |
| K-4 | Application I/O behavior analysis on leadership cluster system | Ju-Won Park, Taeyoung Hong | 2025 | J. Supercomputing 81(6) | `10.1007/s11227-025-07235-5` | L3 | job 수준 성능 귀속(부분). 단일 계층(I/O), 결함 귀속 없음 |
| K-5 | I/O-signature-based feature analysis and classification of HPC applications | Ju-Won Park, Xin Huang, Jae-Kook Lee, Taeyoung Hong | 2024 | Cluster Computing 27(3) | `10.1007/s10586-023-04139-y` | L3 | job 특성화. anomaly/RCA 연결 없음 |
| K-6 | Improving Runtime Prediction Performance Based on Application Type of Jobs on Large-scale Cluster System | Ju-Won Park, Taeyoung Hong | 2025 | IEEE ICMLT 2025 | `10.1109/icmlt65785.2025.11193314` | L4 | 스케줄링 한정 |
| K-7 | Queue congestion prediction for large-scale HPC systems using a hidden Markov model | Ju-Won Park, Min-Woo Kwon, Taeyoung Hong | 2022 | J. Supercomputing 78(10) | (Crossref/DBLP 확인) | L4 | 큐 한정 |
| K-8 | Queue Waiting Time Prediction for Large-scale High-performance Computing System | Ju-Won Park | 2019 | HPCS 2019 | (DBLP 확인) | L4 | — |
| K-9 | Exploiting the behavior of the failed job in high performance computing system | Ju-Won Park, Eunhye Kim | 2018 | ICCSA 2018 (LNCS) | (DBLP 확인) | L3 | 기술적 특성화만 |
| K-10 | Runtime prediction of parallel applications with workload-aware clustering | Ju-Won Park, Eunhye Kim | 2017 | J. Supercomputing 73(11) | (DBLP 확인) | L4 | — |
| K-11 | MyKSC: Disaggregated Containerized Supercomputer Platform | Ju-Won Park, Joon Woo, Taeyoung Hong | 2023 | ICWS 2023 (LNCS) | `10.1007/978-3-031-44836-2_6` | — | 플랫폼. 분석 아님 |
| K-12 | Accelerated Purge Processes of Parallel File System on HPC by Using MPI Programming | Min-Woo Kwon, JunWeon Yoon, TaeYoung Hong, ChanYeol Park | 2017 | LNEE (CSA/CUTE) | `10.1007/978-981-10-7605-3_181` | L7-lite(운영 자동화) | 좁은 단일 작업 |
| **K-13** | **A Study on Building of KISTI Integrated Help Desk System** | Jeong-Gu Lee | 2007 | Journal of Information Management 38(2) | `10.1633/jim.2007.38.2.175` | — | ⭐ **KISTI가 ticket corpus를 보유한다는 증거.** ground truth 확보 경로. 분석 없음, 국내 venue |
| K-14 | Development of Big Data Platform Operation and Management System Considering HPC Environments | Jae-Hyuck Kwak, Jieun Choi, Eunkyu Byun, Sangwan Kim | 2020 | Journal of KIISE 47(3) | `10.5626/jok.2020.47.3.240` | — | **한국어**(영문 abstract만) |
| K-15 | The Implementation and Performance Analysis of Container-based HPC Cluster System | Ju-Won Park, Seungmin Lee, Taeyoung Hong | 2021 | KIISE Trans. Computing Practices 27(5) | `10.5626/ktcp.2021.27.5.228` | — | **한국어** |
| K-16 | High Performance Computing: Infrastructure, Application, and Operation | Byung-Hoon Park, Youngjae Kim, Byoung-Do Kim, Taeyoung Hong, Sungjun Kim, John K. Lee | 2012 | J. Computing Science & Engineering 6(4) | `10.5626/jcse.2012.6.4.280` | — | 오래됨 |

## 9.1 중복 판정

**중복하지 않는 것:** 형식적 계층 모델을 갖는 cross-layer RCA; telemetry 비용 대 품질; 운영자 확인 티켓 ground truth; cross-generation 모델 전이(Nurion→한강); fabric counter 분석.

**반드시 인용·차별화할 것:** **K-1**(job 실패 예측 — 직접 선례), **K-2**(이벤트 로그 상관 — multi-source 융합의 개념적 선례), **K-3**(Shim 2026 — KISTI closed-loop 컨트롤러가 이미 인쇄됨), **K-4/K-5**(I/O 귀속), 그리고 **Lablup 504-GPU 보고서**(한국, cross-layer, cross-org).

**⚠️ 실질 위험: K-3은 KISTI 단독 저자이며 L6/L7에 도달한다. "한국/KISTI에 closed-loop 운영 연구가 없다" 형태의 어떤 주장도 이제 인쇄물에 의해 거짓이다.**

**검색했으나 운영 관련 결과 없음:** KAIST, SNU, ETRI, Samsung SDS, NAVER, Kakao — KIISE(prefix 10.5626)·KIPS(prefix 10.3745) 주제 질의에서 HPC 운영/모니터링/telemetry/장애 논문 미발견. **`NOT FOUND`이지 `NONEXISTENT`가 아니다** — §10.3의 검색 한계 참조.

---

# §10. Claim label 적용 — 전체 요약과 검색 한계

## 10.1 라벨별 집계

| 라벨 | 개수 | 대표 |
|---|---|---|
| **FALSIFIED** | 7 | C-02(SC 0편), C-03(트랙 구분), C-07(탐지≠진단 novelty), C-12(cross-layer RCA), C-14(remediation 비용모델), C-24(Nankai 전제), C-25(한국 선행연구 부재) |
| **부분 FALSIFIED / WEAKENED** | 8 | C-04, C-05, C-06, C-08, C-10, C-11, C-13, C-15, C-20, C-21 |
| **SURVIVES (범위 한정 필요)** | 5 | C-01, C-04(remediation 한정), C-06(HPC 한정), C-17, C-19 |
| **✅ 무조건 생존** | 1 | **C-09 (retention resolution)** |
| **NEEDS-VERIFICATION** | 2 | C-18(Cluster 2023/24), C-22(벤더 감사 미재검증) |
| **출처 누락** | 1 | C-23(L-ladder는 Netti Cluster'21을 인용해야 함) |

## 10.2 새로 발견된 사각지대

| 사각지대 | 내용 |
|---|---|
| **HPCA / ASPLOS / OSDI / ATC / FAST / NSDI / EuroSys / MLSys / KDD** | census venue 집합이 closed-loop 운영 연구가 실제로 발표되는 곳을 체계적으로 배제했다. **Meta RSC(HPCA'25)와 ARGUS·TSLoc(KDD'26)이 이 때문에 누락되었다** |
| **NSDI** | **Beacon(NSDI'19)이 cross-layer RCA와 telemetry 비용 주장을 동시에 falsify한다.** Monet(NSDI'20)도 |
| **한국 국내 문헌** | §9. 가장 심각한 누락 |
| **러시아** | MSU Lomonosov-2 — 10년 이상의 production deep-monitoring 프로그램. *Supercomputer Lomonosov-2: Large Scale, Deep Monitoring and Fine Analytics for the User Community*, JSFI 2019, `10.14529/jsfi190201`; Voevodin 외, *Data mining method for anomaly detection in the supercomputer task flow*, AIP Conf. Proc. 2016, `10.1063/1.4965379`. Octoshell/JobDigest/Octotron 계보 |
| **ENEA (이탈리아)** | 완전히 누락. Chinnici 외, *Towards Sustainability and Energy Efficiency Using Data Analytics for HPC Data Center*, Electronics 2024, `10.3390/electronics13173542` |
| **FDI / 제어이론** | §4.2. 헤드라인 가설의 출처 |
| **영상 분석 (accuracy vs bitrate)** | §4.4. 채택해야 할 formulation의 출처 |
| **NSCC Tianjin facility** | Li, Feng, Li, *Anomaly Detection Method for Chiller System of Supercomputer*, HPCCT 2019, `10.1145/3341069.3341076` — facility 예지보전 0편 주장을 약화 |
| **NUDT의 한국 저널 발표** | Zhang, Xian, Yang, Yu, *A Study of Job Failure Prediction on Supercomputers with Application Semantic Enhancement*, **JCSE(KIISE, Korea) 16(4) 2022**, `10.5626/jcse.2022.16.4.222` — 중국 스윕도 Anglo venue 스윕도 못 찾는 위치 |
| **HPC Asia / SCA** | TRIOS(Tseng, Kawai, Takahashi, Takizawa, HPC Asia/SCA 2026) — 예측적 I/O 경합 시뮬레이션을 스케줄링에 투입. L4→L6 |
| **기타 미포함** | K computer Operations(Procedia CS 2014, `10.1016/j.procs.2014.05.052`) — cross-generation 비교 파트너; SaNSA(FTXS 2018, `10.1109/ftxs.2018.00011`); NØMAD(J. Open Research Software 2026, `10.5334/jors.686`) |

## 10.3 검색 한계 — 어떤 `NO SUCH WORK EXISTS`도 주장할 수 없는 이유

**9개 에이전트 전부가 WebSearch 예산 200/200 소진 상태로 작동했다.** 일부는 첫 질의부터 예산이 0이었다.

| 채널 | 상태 |
|---|---|
| Google Scholar, Bing, DuckDuckGo, Mojeek, Brave | robots 차단 / fetch 불가. **일반 웹·grey literature 탐색 전무** |
| **OpenAlex** | 모든 시도에서 HTTP 429. 기관/ROR 필터와 비-Anglo 커버리지에 최적 도구였으나 **단 한 번도 응답 받지 못함 — 이 감사의 최대 단일 구멍** |
| **Semantic Scholar `/paper/search`** | 429. `/paper/DOI:` 조회만 성공 → **semantic/주제 검색 능력 0** |
| dblp | `/search`·API·bibtex·XML·JSON 전부 robots 차단. 허용된 `/db/`·`/pers/hd/` HTML도 절반은 503/timeout. **HPC Asia 2018–2025 ToC 미확보** |
| ACM DL | 403. TSLoc·*Don't Predict, Prioritize* abstract는 2차 출처 또는 부재. **KDD 2026 쌍의 모든 소속은 추론** |
| IEEE Xplore | 403. Too Many Cooks 세부 수치, PIKA Cluster'20 전문, Cluster'25 저자 목록 미확인 |
| OSTI | egress 정책 403. **ORNL preprint/기술보고서가 나타날 가장 유력한 장소를 제대로 검색하지 못했다** |
| Crossref | 유일하게 신뢰 가능. 그러나 **일반 다항 질의에서 relevance가 붕괴**한다(HPC telemetry sampling 질의에서 computing 논문 0건; "KISTI"가 터키어 *kisti*="cyst"에 매칭). 고유명사(Fugaku, Nurion, Tianhe, Marconi100)에만 작동 |
| **중국어** | CNKI, Wanfang, CQVIP, 计算机学报·软件学报·计算机研究与发展 — **미검색.** Sunway/OceanLight의 Crossref 운영 논문 0건은 색인 artifact로 읽어야 함 |
| **일본어** | CiNii, J-STAGE, **IPSJ/JIP**, IPSJ SIG-HPC 기술보고 — **미검색.** RIKEN/JCAHPC/도쿄대 운영 보고가 주로 여기 있고 대개 일본어 전용 |
| **한국어** | KISS, RISS, DBpia, ScienceON/NDSL, **KSC proceedings** — Crossref DOI를 등록한 학회지만 도달(KIISE 10.5626, KIPS 10.3745, JCSE, JKISE 10.11627). **DOI 없는 KISTI 내부/연차 기술보고서는 이 감사 범위 밖이며, 미공개 Nurion 운영 분석이 있을 가장 유력한 장소다** |
| 미방문 venue | Euro-Par, CCGrid, PDP, ICPADS, HPCC, ISPA, NPC, SC Asia, CUG(census 외), HPCSYSPROS·MODA(census 외), JPDC, CCPE, Frontiers in HPC. **NSCC Singapore, NCHC Taiwan, C-DAC India, IIT는 사실상 미수행** |

**따라서 이 문서의 모든 부정 결과는 `NO COUNTEREXAMPLE FOUND IN THIS SEARCH`다.** 어떤 것도 `NO SUCH WORK EXISTS`가 아니다.

**필수 후속:** ① 작동하는 OpenAlex/Scholar 경로로 전체 스윕 재실행 ② CNKI·J-STAGE/CiNii·KISS/ScienceON 모국어 검색 ③ **KISTI 내부 기술보고서 계열을 수작업 확인**(색인이 가장 적고 중복 확인에 가장 중요) ④ §4.5 표의 5개 미해결 위험 ⑤ VLDB/SIGMOD/ICDE/EDBT/CIDR의 rollup·retention 스윕.

---

# §11. 후보 10종에 대한 심사자 관점 재평가

각 후보에 대해: **최강 기존 논문 / 최강 production 구현 / 최강 novelty 반론 / 최강 feasibility 반론 / 최강 evaluation 반론 / 워크숍에 머물게 하는 것 / SC로 올리는 추가 메커니즘 / 판정**
판정: `DROP` / `KEEP-WATCHING` / `WORKSHOP-LEVEL` / `SC-STRETCH` / `SC-PLAUSIBLE` / `TOP-CANDIDATE`

---

## C1 (구) Telemetry 축소의 탐지–진단 비대칭 → **재정의 필요**

- **최강 기존 논문:** **AWStream(SIGCOMM'18)** — frame rate를 포함한 knob에 대한 accuracy-vs-bandwidth Pareto frontier + 하류 탐지 정확도 + 온라인 적응. 그리고 **Rosich(SAFEPROCESS 2012)** + **Krysander & Frisk(2008)** — detectability/isolability 분리가 정리. 그리고 **TelemetrySuffBench(2026)** — 가설을 제목에 걸고 실증.
- **최강 production 구현:** **DCDB SC'19** — 25 config, 100 ms–1 s, 수집기 CPU 0.69–4.14%, CORAL-2 애플리케이션 교란 최대 9%(AMG, 1024노드).
- **최강 novelty 반론:** *"가설은 2008년 정리이고 2026년에 벤치마크로 확인되었으며, frontier formulation은 SIGCOMM'18이고, HPC 비용 축은 SC'19다. 남은 것은 무엇인가?"*
- **최강 feasibility 반론:** *"downsampling을 소급 연구하려면 전해상도 아카이브가 필요한데, 그것을 지금 시작하면 6–12개월 뒤에야 데이터가 생긴다. 그리고 온라인 오버헤드 측정은 production 기계에서 실험 시간을 요구한다."*
- **최강 evaluation 반론:** *"Pareto frontier는 replay로 그릴 수 있지만, 비용 주장은 실제 배포에서 수집기 오버헤드를 측정해야 한다. 두 시스템 6개월씩은 확보 가능한가?"*
- **워크숍에 머물게 하는 것:** 압축 파이프라인 또는 feature selection으로 프레이밍하는 것. 품질 축이 탐지 하나뿐인 것. 애플리케이션 교란을 측정하지 않는 것.
- **SC로 올리는 추가 메커니즘:** **(i) retention/age를 1급 결정변수로**(§4.3에서 전역 생존한 유일한 축), **(ii) 애플리케이션 교란을 비용 항으로**(AWStream에 등가물 없음, HPC 고유), **(iii) 진단 품질을 2번째 품질 항으로**, **(iv) 계층적 정책**(항상 저rate / 트리거 시 burst / 인시던트 주변만 전해상도) — Sonata dynamic refinement의 HPC판이나 트리거가 학습된 탐지기.
- **판정: `TOP-CANDIDATE` — 단 재정의 조건부.** 헤드라인을 "탐지≠진단"에서 **"telemetry policy π = {metric, sampling rate, retention resolution}의 결합 최적화"**로 바꿔야 한다. §12에서 정식화.

---

## C2 세대 간 telemetry 전이 손실 분해

- **최강 기존 논문:** **CENTILE(arXiv 2608.01725)** — cross-domain 전이 + adapter. **SeT-Diff(CF'26)** — schema permutation invariance. **Farooq ESWA 2026** — tier-0 실세계 검증 federated transfer.
- **최강 production 구현:** 없음. Netti: 센터들이 *"insular ODA solutions"*를 돌린다.
- **최강 novelty 반론:** §6.3의 CENTILE 문구. 그리고 *"Prodigy가 이미 두 시스템에서 평가한다"*.
- **최강 feasibility 반론:** *"N=1 per generation이다. 표준 domain adaptation 가정이 깨지는데, 그 regime에서 무엇을 측정하겠다는 것인가?"*
- **최강 evaluation 반론:** *"3–5 시스템, 각 3개월 이상, 시간순 분할이 필요하다. 랜덤 분할을 쓰면 TOSEM data-splitting 논문 하나로 죽는다. 그리고 schema 정렬 노동이 연구의 대부분을 차지할 것이다."*
- **워크숍에 머물게 하는 것:** 데이터셋/측정 논문으로 읽히는 것. delta만 보고하고 왜 그런지 설명하지 못하는 것.
- **SC로 올리는 추가 메커니즘:** **shift 분해**(하드웨어 세대 / schema / workload mix / 스케줄러 정책) + **invariant representation 결과**(무차원 파생량이 이전되는가) + **transfer-penalty matrix를 벤치마크 artifact로 공개**.
- **판정: `SC-PLAUSIBLE`.** KISTI의 사내 cross-generation 쌍 + 공개 데이터 2종이 구조적 우위다. 다만 **메커니즘 기여가 아니라 측정/벤치마크 기여로 재프레이밍**해야 한다.

---

## C3 Backfill silent-defect screening 정책 최적화

- **최강 기존 논문:** **SuperBench(ATC'24 Best Paper)** — 검증 비용 대 탐지 이득을 명시 최적화하는 Selector, 10만+ GPU 2년.
- **최강 production 구현:** ORNL Frontier backfill screening — 600만 테스트 누적, 6개월 190만, 고유 실패 노드 99개, LAMMPS 1/14,618, **주간 스크린 39,437회 무수확 후 폐기**. 그리고 **Meta RSC의 5분 주기 health check + lemon-node 통계 탐지 + 발표된 FP 회계**.
- **최강 novelty 반론:** *"SuperBench가 이미 비용 예산 하에서 검증 스케줄을 최적화한다. 더 작은 기계에서 같은 것을 하는 것이다."*
- **최강 feasibility 반론:** *"자체 screening 프로그램을 운영해야 데이터가 생긴다. 6개월 이상 대기이며, 그 프로그램 설계 자체가 연구의 전제조건이다."*
- **최강 evaluation 반론:** *"검출률이 1/14,618이면 통계적 검정력을 얻으려면 얼마나 많은 테스트가 필요한가? 그리고 정책 비교를 위해 A/B를 어떻게 하는가?"*
- **워크숍에 머물게 하는 것:** "우리 센터도 backfill screening을 했고 결함을 찾았다"는 경험 보고.
- **SC로 올리는 추가 메커니즘:** 순차 실험 설계 정식화 + **사용자 워크로드 교란을 1급 제약으로**(ORNL이 epilog 변형을 폐기한 이유 — SuperBench의 전용 검증 창과 다른 자원 모델) + ORNL이 공개한 **negative baseline(39,437회 무수확)에 대한 사전 예측 능력** 실증.
- **판정: `SC-STRETCH`.** 원래 `SC-PLAUSIBLE`로 평가했으나 SuperBench 반론과 Meta RSC의 FP 회계 발표로 강등. 차별화가 자원 모델(backfill vs 전용 창)에 의존하며 이는 좁다.

---

## C4 HPC 운영 label semantics 측정

- **최강 기존 논문:** **Uptake(ISSRE'24)** — auto-mitigation의 label 파괴를 정량화(9%, 20.66%/8.34%/13.77%). label 효율 방법론은 전부 닫힘(partial label ISSRE'21, PU learning ISSRE'22, AutoKAD ISSRE'23, ALBADross Cluster'22 28× 절감, LabelEase, ZeroLog). 평가 비판: **Kim et al. AAAI'22**.
- **최강 production 구현:** 없음 — Nagios/Zabbix/Prometheus + Slurm drain reason + 티켓 시스템이 연결되지 않은 4개 소스. Frontier checknode가 실패 검사 이름을 drain reason에 쓰는 것이 사실상 최근접.
- **최강 novelty 반론:** *"weak supervision은 해결된 ML 기법이고, HPC label에 적용하는 것은 엔지니어링이다. 평가 비판(Kim et al.)도 당신 것이 아니다."*
- **최강 feasibility 반론:** *"티켓 export와 RMA 기록에 대한 행정적 접근권이 필요하다. 그리고 gold set 판정은 운영자 시간을 산다."*
- **최강 evaluation 반론:** *"inter-rater agreement가 낮으면 무엇을 결론 내리는가? 그리고 M100의 AUC 0.57을 이겼다고 해서 label이 좋아졌음을 어떻게 아는가?"*
- **워크숍에 머물게 하는 것:** labeling function을 만들고 F1이 올랐다고 보고하는 것.
- **SC로 올리는 추가 메커니즘:** **"label이란 무엇인가"를 측정 문제로** 재프레이밍 — 소스 간 일치도(κ), 계획-비계획 confound 분리, RMA를 지연 고정밀 label로 하는 bootstrap, 그리고 **재사용 가능한 프로토콜 + 공개 gold set**. Uptake를 인용해 closed-loop이 label을 파괴한다는 것을 HPC 규모에서 논증(HPC는 태울 label이 없다).
- **판정: `SC-STRETCH`.** C5와 결합 시 `SC-PLAUSIBLE`. 단독으로는 방법론 기여로 읽힐 위험.

---

## C5 내재적 fail-slow vs 유발된 간섭 판별

- **최강 기존 논문:** **Tuncer et al. TPDS 2019**(HPC anomaly 유형 지도 분류 — 7년 전에 이 축을 HPC에서). **ARGUS**(>1만 GPU 6개월, 다중 원인 판별). **IASO(ATC'19)**(peer 비교는 production-solved). **IPDPS'26 Bhatele**(Perlmutter+Frontier에서 네트워크 혼잡 지배·GPU 안정을 이미 측정).
- **최강 production 구현:** Frontier `checknode`(규칙, ML 0, 원인 판별 0), LBNL NHC, **Meta RSC lemon-node**(통계적 peer-outlier, production).
- **최강 novelty 반론:** *"ARGUS가 이미 1만 GPU production 규모에서 6개월간 always-on 다중 원인 fail-slow 진단을 하고, Kaleidoscope가 843건 실제 라벨로 PGM 기반 원인 판별을 SC'20에 했고, Tuncer가 2019년에 HPC anomaly 유형을 분류했다. 기계가 한국제라는 것 말고 무엇이 새로운가?"*
- **최강 feasibility 반론:** **Slingshot fabric counter 접근권**. Bhatele 그룹이 Perlmutter/Frontier에서 Rosetta 스위치 counter를 얻지 못했다고 명시한다. 확보하지 못하면 네트워크 원인 클래스가 붕괴한다.
- **최강 evaluation 반론:** *"운영자 확인 label이 몇 건인가? Kaleidoscope 843, ClusterRCA 739가 기준이다. 그리고 silent degradation은 티켓이 거의 없으므로 label 집합에 sampling bias가 있다."*
- **워크숍에 머물게 하는 것:** 탐지 전용. 주입 anomaly만. 원인 클래스가 3개 이하.
- **SC로 올리는 추가 메커니즘:** ARGUS가 구조적으로 만들 수 없는 원인 taxonomy(cross-job 간섭, topology/placement, Lustre, cooling/power) + **이기종 배치 job**에서의 평가(ARGUS의 iteration 주기성 가정 붕괴) + **특정 이웃 job으로의 귀속**(Tuncer는 contention을 label 클래스로만 다룸).
- **판정: `SC-STRETCH`.** 좁고 양쪽에서 압박받으며 SC26 ORNL 논문 위험이 있다.

---

## C6 Blast-radius remediation 비용 모델 + off-policy 평가

- **최강 기존 논문:** **HPDC'24 BSC** — 비용 모델의 세 요소를 전부 갖췄다(§7.1). **arXiv 2607.20005** — CMDP + FRR budget + blast radius/reversibility/epistemic risk 분해 + abstention as action. **Narya(OSDI'20)**.
- **최강 production 구현:** Frontier checknode(정확도 수치 0), LBNL NHC, **Meta RSC**(FP 회계 발표), **DeepMind DC cooling**(confidence gating + failover + 운영자 이탈).
- **최강 novelty 반론:** §7.3의 HPDC'24 문구 + *"CMDP-with-FRR, blast-radius/reversibility/epistemic 분해, abstention-as-action이 이미 발표되었다. HPC로 옮기는 것은 응용이다."*
- **최강 feasibility 반론:** *"Tier-0에서 drain을 A/B할 수 없다. 그리고 Slurm 노드 상태 이력에 actor 필드가 없으면 off-policy 평가가 불가능하다."*
- **최강 evaluation 반론:** *"HPDC'20이 이미 시뮬레이션 슬롯을 차지했다. 시뮬레이션은 받아들여지지 않을 것이다."*
- **워크숍에 머물게 하는 것:** health score → drain 통합을 만들고 잘 됐다고 보고하는 것 = HPCSYSPROS/CUG 논문.
- **SC로 올리는 추가 메커니즘:** **조치 클래스 확장**(drain/requeue의 queue-position 손실, fairshare charge-back, reservation fragmentation이 HPDC'24 node-hours로 환원되지 않음을 보이기) + **형식적 DR/IPS OPE + 신뢰구간** + **provenance/audit**(가장 논쟁 적고 기존 인용으로 거부 불가).
- **판정: `SC-STRETCH` (조건부).** actor 필드 확보 시. 없으면 `DROP`하고 C5 절로 접을 것.

---

## C7 HPC 운영 agent 벤치마크

- **최강 기존 논문:** **ITBench**(94 시나리오, SRE 13.8%), **AIOpsLab**, **RCACopilot(EuroSys'24)**, **L4(FSE'25 — LLM 없이 LLM baseline 압도)**, **How Far Can RCA Go**(reasoning gap 40.0% vs data 1.4%).
- **최강 production 구현:** HPC에는 사실상 없음(2026 서베이 2편이 배포 0건). **ORNL EPIC**(Frontier 50만 job, 배포 챗봇, RCA 안 함). **FRAGATA**(CESGA, 정량 평가 없음).
- **최강 novelty 반론:** *"Slurm을 Kubernetes로 치환한 도메인 이식이다."*
- **최강 feasibility 반론:** *"실제 운영 데이터를 공개해야 하고(정제·기관 승인) ground truth를 수작업 판정해야 한다. 프로젝트 예산 대부분이 여기 들어간다."*
- **최강 evaluation 반론:** *"L4가 LLM 없이 이겼다. 벤치마크에서 점수가 낮으면 그것이 흥미로운 결과인가 아니면 문제 설정이 나쁜 것인가?"*
- **워크숍에 머물게 하는 것:** log summarization, chatbot, 티켓 FAQ, 문서 RAG, LLM-as-judge 단독 평가.
- **SC로 올리는 추가 메커니즘:** **비용 제한 evidence collection**(agent가 요청하는 telemetry에 비용을 지불 → C1과 연결) + **grounding/검증**(모든 주장이 telemetry query로 확인 가능, hallucination rate 측정) + **action guard**(C6과 연결).
- **판정: `KEEP-WATCHING`.** C4의 ground truth에 종속되고 도메인 이식 반론이 강하다. **AgenticAI4HPC'26(SC26 1회차)이 이 lane을 선점할 것이므로 2027년에는 이미 늦을 수 있다.**

---

## C8 job 효율 리포팅의 사용자 행동 효과

- **최강 기존 논문:** 없음(아카이브). PIKA MODA23, LLview MODA25가 워크숍.
- **최강 production 구현:** PIKA 5년+ production, LLview JUWELS production, XDMoD Application Kernels. **단 §8.1에 따라 PIKA와 XDMoD는 아카이브 논문을 갖고 있다** — "선행연구 없음"이 아니라 "행동 효과 측정이 없음"으로 좁혀야 한다.
- **최강 novelty 반론:** *"알고리즘 기여가 없다. 이것은 사용자 연구다."*
- **최강 feasibility 반론:** 없음 — 가장 쉽다.
- **최강 evaluation 반론:** *"staggered rollout 없이는 인과 주장을 못 한다. 그리고 사용자 문화가 사이트별로 다르므로 일반화가 약하다."*
- **워크숍에 머물게 하는 것:** 단일 센터, 대조군 없음, 효과 크기 미측정.
- **SC로 올리는 추가 메커니즘:** 다중 센터 + staggered rollout + 측정된 효과 크기 + **낭비 node-hour로 표현된 운영 성과**.
- **판정: `WORKSHOP-LEVEL`, 규모 확보 시 SC SotP.** **첫 논문으로 최적. HPC-ODA 2026이 정확한 입구다** — 단 2026-08-12 제출 마감이 이미 지났으므로 **2027년 판을 노려야 한다.**

---

## C9 운영 정책 counterfactual 평가 방법론

- **최강 기존 논문:** **ExaDigiT SC24**(물리 해결, Frontier 6개월 replay V&V) → **NeurIPS 2025 LC-Opt**(§8.2 lineage 6 — **이 후보의 인접 공간이 이미 채워지기 시작했다**). MODA23 HPE 시뮬레이터, MODA25 duration-informed scheduler.
- **최강 production 구현:** 없음.
- **최강 novelty 반론:** *"ExaDigiT가 twin을 만들고 LC-Opt가 그 위에서 RL 벤치마크를 만들었다. 정책 평가 방법론이 정말 비어 있는가?"*
- **최강 feasibility 반론:** *"twin 구축·파라미터화·검증에 상당한 투자가 필요하고 ORNL 협업 의존적이다."*
- **최강 evaluation 반론:** *"twin의 오차 막대를 실제 시스템 대비 어떻게 얻는가? 정책을 실제로 실행해 봐야 하지 않는가?"*
- **판정: `KEEP-WATCHING`.** **LC-Opt(NeurIPS'25) 발견으로 강등.** 확보해서 읽기 전에 착수하지 말 것.

---

## C10 Telemetry integrity / observability debt

- **최강 기존 논문:** 없음(telemetry 품질 벤치마크 부재). 인접: DSN'25 industry *Hardware Telemetry at Scale*(Meta, 사례 연구).
- **최강 production 구현:** 사이트별 우회로. NERSC CSM telemetry-api 실패, LLNL CSM LDMS 버전 지연, CSCS Kafka listener 부재·Fluent Bit 불안정, CSCS 849 J 불일치 + *"Slurm... cannot therefore always be trusted"*.
- **최강 novelty 반론:** *"이것은 엔지니어링 감사다."*
- **최강 feasibility 반론:** 없음 — 한강 도입 시 이중 수집을 설계해 넣으면 자연 획득.
- **최강 evaluation 반론:** *"손실을 측정했다. 그래서 무엇인가? 하류 영향을 보이지 않으면 결과가 아니다."*
- **SC로 올리는 추가 메커니즘:** **C1의 필수 구성요소로 통합.** "telemetry를 얼마나 줄일 수 있는가"를 논하기 전에 "지금 수집되는 telemetry가 무엇을 놓치고 있는가"를 측정해야 한다. 그리고 **GWDG의 발견(모니터링 파이프라인 열화 자체가 신호)**과 연결: 결측 데이터가 증거다.
- **판정: `WORKSHOP-LEVEL` 단독, **C1의 하위 구성요소로는 필수.**

---

# §12. 재정의된 최우선 후보: Telemetry Policy Optimization

§4의 falsification 결과를 반영한 정식화. **헤드라인 가설을 버리고 정책 최적화 문제로 재정의한다.**

## 12.1 정식화

**Telemetry policy:**
$$\pi = \{(m_i,\ f_i,\ r_i(\tau))\}_{i=1}^{N}$$
- $m_i$ — 수집되는 metric $i$ (수집 여부 자체가 결정변수)
- $f_i$ — metric $i$의 샘플링 주파수
- $r_i(\tau)$ — **데이터 나이 $\tau$의 함수로서의 보존 해상도** ← **§4.3에서 전역적으로 생존한 유일한 축. 여기가 novelty의 중심이다**

**비용:**
$$C(\pi) = C_{\text{agent}}(\pi) + C_{\text{network}}(\pi) + C_{\text{storage}}(\pi) + C_{\text{query}}(\pi) + \underbrace{C_{\text{perturb}}(\pi)}_{\text{HPC 고유}}$$
- $C_{\text{agent}}$ — 수집기 CPU/메모리 (DCDB SC'19가 CPU 세대에서 측정: 0.69–4.14%)
- $C_{\text{network}}$ — **DCDB에 없음**
- $C_{\text{storage}}$ — **DCDB에 없음.** 다PB 다년 (ORNL 20 PB/5년)
- $C_{\text{query}}$ — **어디에도 없음**
- $C_{\text{perturb}}$ — 애플리케이션 교란 $O=(T_p-T_r)/T_r$. **AWStream에 등가물 없음** (DCDB가 CPU 세대에서 측정, GPU 세대에 없음)

**운영 품질:**
$$Q(\pi) = \{Q_{\text{detect}},\ T_{\text{detect}},\ Q_{\text{localize}},\ Q_{\text{RCA}}\}$$

**문제:**
$$\min_{\pi} C(\pi) \quad \text{s.t.} \quad Q_{\text{detect}}(\pi) \ge \alpha,\ \ T_{\text{detect}}(\pi) \le \delta,\ \ Q_{\text{RCA}}(\pi) \ge \beta$$

**가장 가까운 기존 formulation:** **Rosich(SAFEPROCESS 2012) Problem 3** — 모든 minimal 센서 구성 $S' \subseteq S$ 중 `D ⊆ Dmax`(detectability spec)와 `I ⊆ Imax`(isolability spec)를 만족하는 것을 찾기. 예산 변종은 정수계획으로 존재(*Optimal test and sensor selection for active fault diagnosis using integer programming*, Control Eng. Practice 2020; *Optimal Sensor Selection for Active Fault Diagnosis using Test Information Criteria*, IFAC-PapersOnLine 2019).

**Rosich에 없는 것 = formulation gap:**
1. 결정변수가 **binary sensor presence만**. **rate 변수 없음, retention 해상도 변수 없음**
2. 비용이 **센서 개수/구매비**이지 bytes/s·storage-TB-months·ingest cost가 아님
3. 품질 제약이 **binary structural isolability**이지 **연속적 통계 품질**(RCA acc@k, MTTD, localization precision)이 아님
4. **plant의 해석적 모델을 요구한다** — 슈퍼컴퓨터에는 없다. **바로 이것이 HPC판이 structural이 아니라 empirical/statistical이어야 하는 이유이며, 방어 가능한 논거다**

## 12.2 검증할 4개 질문

| # | 질문 | 왜 살아 있는가 |
|---|---|---|
| **Q-α** | **최소 telemetry 비용으로 anomaly detection뿐 아니라 root-cause diagnosis까지 보존할 수 있는가?** | 가설 자체는 novel하지 않지만(§4.1) **비용 제약 하의 정량적 답은 HPC에 없다** |
| **Q-β** | **Detection-optimal telemetry와 RCA-optimal telemetry가 다른가 — 그리고 그 차이가 바이트로 얼마인가?** | FDI는 정성적으로 그렇다고 말한다(isolability ⊃ detectability). **바이트·rate·retention으로 정량화한 것이 없다** |
| **Q-γ** | **uniform sampling보다 metric-specific adaptive sampling이 Pareto frontier를 개선하는가?** | AWStream이 영상에서 그렇다고 보였다. **HPC 다계층 telemetry에서 미검증** |
| **Q-δ** | **downsampling으로 사라지는 temporal ordering / lag 정보가 RCA 품질에 어떤 영향을 주는가?** | ⭐ **가장 novel한 부분.** RCA는 lag 구조에 의존하는데(Granger, cross-correlation, cascade 순서) downsampling이 정확히 그것을 파괴한다. **retention 해상도 축과 직결되며, 어느 분야에서도 발표된 것을 찾지 못했다** |

**Q-δ가 이 후보의 중심이 되어야 한다.** 이유:
- retention 해상도는 §4.3에서 **전역적으로 생존한 유일한 축**이다
- lag/ordering 정보 손실은 **detection보다 diagnosis에 비대칭적으로 치명적**이라는 메커니즘적 근거가 있다(탐지는 진폭 이상으로 충분, 진단은 순서가 필요)
- AWStream·FDI·TelemetrySuffBench 어느 것도 이 메커니즘을 다루지 않는다
- HPC 고유: cascade가 fabric topology와 OST map을 따라 물리적으로 전파되므로 lag 구조가 *물리적으로 참*이다

## 12.3 반드시 인용하고 positioning할 문헌

**서론에서 채택:** AWStream(SIGCOMM'18) — formulation.
**Related work에서 명시적 차별화:** Rosich(SAFEPROCESS'12), Krysander & Frisk(2008), Fault Diagnosis Toolbox — detectability/isolability 분리는 기존 결과임을 먼저 인정. TelemetrySuffBench(2026) — synthetic·비용축 없음. DCDB SC'19 — 비용 축은 확립됨, GPU·retention·품질 없음. Netti FGCS'20 — 집계 window 효과가 미측정임을 저자가 인정. NodeSentry(SC'25)/Prodigy(SC'23)/Tuncer(TPDS'19) — 모델 측 축소. Gleaner/Mint(ASPLOS'25)/TraceDiag — trace 측 C1. Kestrel — 탐지 지연 vs 비용(네트워킹). Sonata/PINT/AutoSketch — 네트워크 formulation. Hindsight(NSDI'23) — retroactive retention. SuperBench(ATC'24) — 능동 검증 비용 최적화. Beacon(NSDI'19) — HPC 압축·캐싱. Mai/Brauckhoff(IMC'06) — 샘플링 vs 탐지. Chameleon/Reducto/VideoStorm — 영상 계열.

---

# §13. `00`–`07`에 적용해야 할 정정 요약

| 문서 | 정정 |
|---|---|
| `00` §6.2 | "SC 트랙 라벨 구분 불가"를 **"SOP는 Technical Papers 트랙 내 토픽 영역이며 별개 트랙이 아니다"**로 교체. §2.2의 재계수 방법 추가 |
| `00` §3.2 | L0–L7 사다리에 **Netti 외, IEEE Cluster 2021, `10.1109/cluster48925.2021.00086`** 인용 추가 |
| `00` §8 | 발견 (4) "가장 강한 precedent는 SC20 Kaleidoscope"에 SC26 ORNL 논문 위험 추가 |
| `02` | §0.1의 인용 정정 3건 + metadata 정정 5건. §9의 KISTI 국내 선행연구 16편 추가. 누락 venue(HPCA/NSDI/KDD/ICS) 항목 추가 |
| `03` P3 | SC25 Aurora 저자·소속 정정(§0.1 F-1). arXiv ID 삭제 |
| `03` §3.1 | "센터 SC 본트랙 0편" 주장 삭제 → §2.3의 9편 반례로 교체 |
| `03` §3.4 | "SC에 부재한 것" 목록에서 syslog·Slingshot 혼잡·facility 예지보전 항목을 §1.3 C-19/C-20/C-21에 따라 좁힐 것 |
| `04` §9 | LDMS·PIKA·XDMoD·Arbiter·LLview 정정(§8.1). §8.2의 놓친 lineage 6건 추가. §8.3의 "다리는 데이터셋"으로 패턴 재진술 |
| `05` G11 | §4.2/§4.3/§4.6에 따라 전면 재작성 |
| `05` G15 | §7.3에 따라 "비용 모델 없음" 주장 삭제, 조치 클래스로 좁힘 |
| `05` G16 | §5.1의 Beacon 반례 추가, 주장 좁힘 |
| `05` PART II AXIS A | "65.7%" → "overall 40.0% vs 1.4%"(§0.2) |
| `05` PART II AXIS C | 5개 zero 하위주장 판정 교체(§4.6) |
| `05` PART II AXIS F | HPDC'24가 비용 모델을 갖고 있음 인정(§7.1) |
| `06` C1 | §12로 전면 재정의 |
| `06` C6 | HPDC'24 반론 추가, 3개 잔존 주장으로 좁힘(§7.4) |
| `06` 전체 | §11의 심사자 관점 판정으로 갱신 |
| `07` Q1 | "센터 SC 0편" 삭제 → §2 |
| `07` Q4 | "L3 정체"를 open-science 국가센터 + 장애 remediation으로 범위 한정. Uptake 반전 추가(§3.3) |
| `07` Q5 | Farooq ESWA·CENTILE·SeT-Diff 반례 추가, 잔존 주장을 off-diagonal로 좁힘(§6.3) |
| `07` Q6 | §4 전면 반영. 헤드라인 가설 폐기, §12로 교체 |
| `07` Q7 | Beacon·504-GPU 추가(§5.1/§5.2) |
| `07` "SC SotP 별도 경로" | **삭제** — 동일 double-blind 심사, 동일 폼(§2.4) |

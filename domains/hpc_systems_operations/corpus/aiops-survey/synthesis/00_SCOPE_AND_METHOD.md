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

# 00. SCOPE AND METHOD
## HPC AIOps / Operational Intelligence → SC Regular Paper Research Landscape

**작성일:** 2026-09-06
**대상:** KISTI 김민식 (한강 / KISTI-6 AIOps 과제)
**문서 세트:** `00_SCOPE_AND_METHOD` · `01_VENUE_MAP` · `02_PAPER_CENSUS` · `03_SC_REGULAR_PRECEDENTS` · `04_WORKSHOP_AND_CUG_CASES` · `05_RESEARCH_PRACTICE_GAPS` · `06_INITIAL_SC_RESEARCH_CANDIDATES` · `07_ANSWERS_TO_KEY_QUESTIONS`

---

## 1. 이 조사의 목적

일반적인 literature survey가 아니다. 답해야 할 질문은 하나다.

> **실제 HPC production operation에서 반복적으로 발생하는 문제 가운데, 단순 monitoring이나 engineering implementation을 넘어 SC Technical Paper 수준의 systems research로 발전할 수 있는 문제는 무엇인가?**

따라서 논문 수집이 아니라 **연구 구조(research structure)의 복원**이 산출물이다. 모든 후보는 다음 사슬을 통과해야 한다.

```
operational problem
  → current production implementation
    → known limitations / failure modes
      → problem abstraction
        → closest research literature
          → existing SC-regular precedent
            → novelty falsification
              → remaining research gap
                → SC Technical Paper potential
```

이 사슬에서 **novelty falsification 단계가 가장 중요하다.** 흥미로운 문제를 발견했다는 이유만으로 `OPEN RESEARCH GAP`이라고 쓰지 않는다. 항상 "가장 가까운 기존 연구"와 "가장 가까운 production 구현"을 먼저 찾고, 남은 차이를 구체적·검증가능한 형태로 진술한 뒤에만 gap을 선언한다.

---

## 2. 조사 범위

### 2.1 연도

| 연도 | 상태 |
|---|---|
| 2020–2025 | 전수조사 대상 |
| 2026 | **진행 중.** 개최 전이거나 proceedings 미공개인 경우 `PARTIAL / NOT YET PUBLISHED` 표기 |
| ~2019 | **전수조사 안 함.** 아래 계보에 한해 backward/citation search만 수행 |

2020년 이전으로 내려간 계보(§ `02_PAPER_CENSUS`, `C_dsn_issre_lineage` 원자료 Part B):

- autonomic computing / self-managing systems (Kephart & Chess 2003; Microreboot OSDI'04)
- failure prediction from system events (Sahoo KDD'03 → Liang ICDM'07 → Salfner CSUR'10 → Gainaru SC'12)
- system log analytics (Oliner & Stearley DSN'07 → Xu SOSP'09 → Lou ATC'10 → He ISSRE'16 → Drain ICWS'17 → DeepLog CCS'17 → LogBERT 2021)
- large-scale field failure studies (Schroeder & Gibson DSN'06 → Pinheiro FAST'07 → Schroeder SIGMETRICS'09 → Di Martino DSN'14 → Gupta SC'17 → Nie HPCA'16)
- datacenter/service diagnosis, RCA 조상 (Pinpoint DSN'02 → Bodík EuroSys'10)
- HPC performance-anomaly 분기 (Tuncer et al. ISC'17 / TPDS 2019 — **axis D의 최강 pre-2020 falsifier**)

### 2.2 Venue

**Anchor venue는 SC**이며, SC 내부 트랙을 반드시 구분한다.

| Tier | Venue | 조사 방식 |
|---|---|---|
| **Anchor** | SC (Technical Papers / State of the Practice / Workshops / Posters / BoF / Panels / Tutorials) | 본프로그램 SC20–SC25 전수 열거, SC26 부분 |
| **A** | HPDC, IPDPS(main), IEEE Cluster, ISC High Performance, DSN, ISSRE, ACSOS | 2020–2026 proceedings ToC 전수 열거 후 주제 필터 |
| **B** | CCGrid, Euro-Par, ICPE, SIGMETRICS, MLSys, EuroSys, USENIX ATC, OSDI, SOSP, NSDI, FAST, ICS, KDD, ICSE/FSE/ASE | **전수조사 안 함.** closest-work 확인이 필요할 때만 targeted search |
| **Workshop (W1)** | MODA(ISC), HPC-ODA(SC26~), HPCSYSPROS, FTXS, PMBS, ProTools, HPCTESTS, PERMAVOST, AI4Sys, SNTA, JSSPP, ESSA, iWAPT | emerging problem 발굴 source |
| **Workshop (W2)** | PDSW, HUST, ISAV, EESP, Sustainable Supercomputing, Digital Twins for HPC, RESDIS, ECHO, AgenticAI4HPC 등 | 주제 기반 선택 조사 |
| **Practice** | CUG, 센터 tech report, 센터 공개 데이터셋 | production operational problem mining |

**Tier B 확장 규칙:** OSDI/SOSP/NSDI/EuroSys/FAST/ATC는 문제가 일반 systems problem으로 충분히 추상화될 때만 확장한다. 다만 이 조사에서는 **거의 항상 확장이 필요했다** — SC 제출물의 novelty를 죽이는 논문 대부분이 HPC 밖에 있기 때문이다(Narya OSDI'20, SuperBench ATC'24, Perseus FAST'23, RCACopilot EuroSys'24, MetaLog ICSE'24 등). 이는 §`05_RESEARCH_PRACTICE_GAPS`의 핵심 발견 중 하나다.

### 2.3 검색 terminology

"AIOps"라는 단어만 검색하지 않았다. 실제로 사용한 용어:

operational data analytics · HPC monitoring · system telemetry · system analytics · anomaly detection · failure prediction · fault prediction · reliability · root cause analysis · fault localization · performance diagnosis · performance variability · slow node · straggler · workload characterization · workload prediction · runtime prediction · intelligent scheduling · resource prediction · system logs · log anomaly · predictive maintenance · self-healing · autonomic computing · self-managing systems · adaptive systems · telemetry sampling · telemetry reduction · power prediction · thermal anomaly · network congestion diagnosis · storage performance anomaly · GPU health · distributed training anomaly · fail-slow · gray failure · concept drift · domain adaptation

---

## 3. Taxonomy (multi-tagging)

각 논문/사례를 하나의 카테고리에 강제로 넣지 않고 중복 태깅한다.

### 3.1 Component / domain
CPU·node·memory / GPU / network·fabric (Slingshot, InfiniBand, Dragonfly) / storage·Lustre / scheduler·Slurm / workload·job / logs·events / power / cooling·facility / telemetry infrastructure

### 3.2 Intelligence maturity (L0–L7)

| 레벨 | 정의 | 판정 기준 |
|---|---|---|
| **L0** | data collection | 수집·전송·저장만 |
| **L1** | visualization / observability | 대시보드, 조회 |
| **L2** | rule-based alerting | 임계값, 규칙 |
| **L3** | statistical / anomaly detection | 통계·ML로 "이상하다"까지 |
| **L4** | prediction | 미래 사건(고장·전력·런타임) 예측 |
| **L5** | diagnosis / RCA | 어디가·왜 문제인지 지목 |
| **L6** | recommendation / decision support | 사람에게 행동을 제안 |
| **L7** | closed-loop remediation | 시스템이 스스로 행동 |

L0–L7은 사실상 **MAPE-K loop(Kephart & Chess 2003)의 재유도**다. 논문에서 이 점을 명시하면 reviewer가 좋게 본다.

### 3.3 Deployment maturity (D0–D5)

| 레벨 | 정의 |
|---|---|
| **D0** | conceptual / synthetic / simulation |
| **D1** | prototype / testbed |
| **D2** | production data used offline (trace replay) |
| **D3** | online / shadow deployment |
| **D4** | used in operator workflow (운영자가 매일 본다) |
| **D5** | closed-loop production action (실제로 조치한다) |

### 3.4 Research character (P0–P4)

| 레벨 | 정의 |
|---|---|
| **P0** | pure operational practice |
| **P1** | useful engineering technique |
| **P2** | empirical system characterization |
| **P3** | research method applied in production |
| **P4** | generalizable research contribution |

> ⚠️ **스케일 혼용 경고.** 원자료 `F_axes_ABC.md`와 `G_axes_DEFG.md`를 생성한 조사 에이전트는 브리핑에 L/D/P 정의가 없다고 판단하여 **자체 정의를 만들어 사용**했다(각 파일 상단에 명시). 예: F의 L0–L7은 "telemetry layer breadth", P0–P4는 "production-data realism"이다. `02_PAPER_CENSUS`에서 해당 항목을 옮길 때 가능한 것은 위 정본 스케일로 재매핑하고 `[L/D/P re-mapped]`로 표기했으며, 재매핑 불가한 것은 `원 출처 정의 상이 — 재확인 필요`로 남겼다. **두 스케일을 섞어 읽지 말 것.**

---

## 4. Evidence rules (증거 등급 규칙)

### 4.1 절대 동일시하지 않는 것

```
telemetry collection ≠ monitoring ≠ dashboard ≠ threshold alert
  ≠ anomaly detection ≠ prediction ≠ RCA ≠ recommendation ≠ automated remediation
```

### 4.2 Publication type 태그

`[SC-TECHNICAL-PAPER]` `[STATE-OF-PRACTICE]` `[ARCHIVAL-PEER-REVIEWED]` `[WORKSHOP-PEER-REVIEWED]` `[POSTER]` `[BOF]` `[PANEL]` `[TUTORIAL]` `[PRACTITIONER]` `[VENDOR]` `[TECH-REPORT]`

**SC Technical Paper와 workshop/BoF/CUG 발표를 동일한 publication evidence로 취급하지 않는다.**

### 4.3 벤더 주장 처리

벤더가 기능 이름에 `AI`, `RCA`, `AIOps`를 붙였다는 이유로 research result로 판정하지 않는다. 다음 5개 항목을 따로 확인한다.

`documented feature` / `documented algorithm` / `quantitative evaluation` / `peer-reviewed validation` / `production deployment`

이 조사에서 감사한 벤더 항목 11건 중 **알고리즘과 정량 평가를 모두 갖춘 것은 1건(HPE CADDY)**, 그것도 단일 노드 testbed였고, **peer-reviewed validation을 갖춘 것은 0건**이었다. 상세는 `04_WORKSHOP_AND_CUG_CASES` §6.

### 4.4 CUG의 지위

CUG 2026 CFP에서 확인된 사실: 제출 유형은 Paper / Presentation / BoF / Tutorial이고, 채택은 abstract 기반이며 ACM ICPS 게재는 *"may require an additional round of reviews"*다. → **CUG "Paper"는 peer-reviewed archival publication과 동등하지 않다.** CUG는 *practice evidence*로만 인용하고("ORNL 운영자가 X를 보고했다"), *validated method* 주장은 Crossref로 검증된 archival 논문에만 사용한다.

### 4.5 Novelty falsification 판정값

`CLOSED` / `PARTIALLY_ADDRESSED` / `STILL_OPEN` / `TOO_SITE_SPECIFIC` / `ENGINEERING_ONLY` / `INSUFFICIENT_EVIDENCE`

**확실하지 않으면 `INSUFFICIENT_EVIDENCE`.** 이 규칙은 실제로 여러 축에서 적용되었다.

---

## 5. Exclusion rules

다음은 census에서 제외하거나 PERIPHERAL로 강등했다.

1. 논문 수를 늘리기 위한 peripheral ML-for-HPC 논문 (application performance prediction, autotuning, code optimization 등 operations와 직접 연결되지 않는 것)
2. 순수 application-level performance analysis (profiler, tracing tool) — 단, telemetry infrastructure 자체가 기여인 경우는 포함
3. fault injection / architecture resilience 연구 중 운영 데이터와 무관한 것
4. cloud/microservice 전용 연구 — 단, **novelty falsification용 closest work로는 반드시 포함**
5. topology design, congestion control 설계 논문 (진단이 아니라 설계)

---

## 6. 실제 수행 방법과 한계 (반드시 읽을 것)

### 6.1 수행 방법

8개의 병렬 조사 트랙으로 수행했다: ① SC 본프로그램 ② HPDC/IPDPS/Cluster/ISC/ACSOS ③ DSN/ISSRE + 역사적 계보 + 비HPC AIOps ④ workshop ecosystem ⑤ CUG + 벤더 ⑥ research axis A–C 적대적 검증 ⑦ research axis D–G 적대적 검증 ⑧ 센터별 production evidence. 이후 novelty falsification과 후보 종합을 수행했다.

열거의 1차 근거는 **proceedings ToC**였다: SC는 `scXX.supercomputing.org/proceedings/tech_paper/` 인덱스 + Crossref proceedings DOI, HPDC/IPDPS/Cluster/ISC/ACSOS는 Crossref REST API의 container-title/ISBN 필터 전수 페이징, DSN/ISSRE는 공식 accepted-paper 프로그램 페이지, CUG는 `cug.org/proceedings/` PDF 직접 fetch.

### 6.2 환경적 한계 — 결과 해석에 직결

| 한계 | 영향 |
|---|---|
| **dblp ToC 페이지가 WebFetch에서 ~10건에서 절단**, dblp search API는 robots 차단 | 전체 ToC 확보에 Crossref/프로그램 페이지로 우회. dblp record 페이지(개별 논문)는 정상 동작하여 개별 검증에 사용 |
| **ACM DL, IEEE Xplore가 403** | **어떤 논문의 abstract도 대량으로는 읽지 못했다.** B census(HPDC/IPDPS/Cluster/ISC/ACSOS)의 evaluation scale·production deployment 필드는 **검증된 사실이 아니라 가설**이다 |
| **WebSearch 예산 200/200 소진** | 후반 조사는 Crossref·Semantic Scholar·직접 fetch로만 수행. 벤더 감사에서 Intel·VAST는 `NOT COVERED` |
| **SC 논문 페이지가 트랙 라벨을 노출하지 않음** (모든 트랙이 "Technical Papers Archive"로 표시) | **SC 항목 대부분이 `TRACK-UNKNOWN`.** Technical Paper와 State of the Practice를 구분하지 못했다. 추정은 명시했으나 사실로 쓰지 않았다 |
| **DSN 2020·2021 프로그램 페이지 소실/차단** | 해당 2년은 `PARTIAL`. in-scope 논문 3–8편을 놓쳤을 가능성이 높다 |
| **CUG 2026 proceedings 404, 프로그램은 robots 차단** | CUG 2026 내용 **0건 검증**. 2027년 초 재확인 필요 |
| **CUG PDF 5건 미게시** (CUG2021 HPE AIOps, CUG2021 Sandia system/application monitoring, CUG2022 Fallout, CUG2023 Slingshot Dashboard tutorial, CUG2024 Swordfish) | "미게시"이지 "없음"이 아니다. 저자에게 직접 요청 권장 |
| **ISC research-paper track 2024–2026 proceedings 미확인** | 2020–2023만 검증(각 27/24/15/20편). **"track이 없어졌다"고 쓰지 말 것** — 확인되지 않았을 뿐이다 |
| **IEEE Cluster 2026, ACSOS 2026** | 색인 없음 → `NOT YET PUBLISHED` |

### 6.3 조사 품질 규칙 (실제 적용)

1. 논문 제목·연도·venue를 추측하지 않았다. 확인 불가 시 `UNVERIFIED`.
2. 공식 proceedings / DOI / publisher / author page를 우선했다.
3. 검색 snippet만 보고 내용을 단정하지 않았다. abstract 미독 항목은 `ABSTRACT-UNREAD`.
4. workshop과 regular paper를 구분했다.
5. poster/BoF/vendor presentation을 peer-reviewed evidence로 쓰지 않았다.
6. production deployment 주장은 원문에서 확인했고, 불가하면 `UNKNOWN`.
7. workshop → regular paper 발전은 중복 계수하지 않고 lineage로 기록했다.
8. peripheral ML-for-HPC 논문을 수 채우기용으로 넣지 않았다.
9. application performance prediction보다 operations/reliability/diagnosis/management 직결 연구를 우선했다.
10. 미발견 정보는 `NOT FOUND` / `UNKNOWN`으로 남겼다.

### 6.4 이 문서 세트를 쓸 때의 원칙

> **`02_PAPER_CENSUS`의 인용을 그대로 논문에 옮기지 말 것.** 특히 §7에 나열된 미검증 항목과, `[A]`/`ABSTRACT-UNREAD`로 표시된 evaluation·deployment 필드는 PDF에서 재확인해야 한다. "production에 배포되었다"는 잘못된 주장이 related work에 들어가는 것이 이 조사에서 가장 큰 피해를 낳는 오류다.

---

## 7. 산출물 구성

| 문서 | 내용 | 상태 |
|---|---|---|
| `00_SCOPE_AND_METHOD.md` | 이 문서 | 완료 |
| `01_VENUE_MAP.md` | venue별 역할·구조·진입 전략 | 완료 |
| `02_PAPER_CENSUS.md` | Must Read / Relevant / Peripheral 전수 목록, 공개 데이터셋, 연도별 집계, 검증 상태 | 완료 |
| `03_SC_REGULAR_PRECEDENTS.md` | SC regular precedent 심층 분석 (A–G 항목: operational starting point → why practice was insufficient → research abstraction → novel mechanism → evaluation → generality → why SC) | 완료 |
| `04_WORKSHOP_AND_CUG_CASES.md` | workshop/CUG/센터 운영 문제 인벤토리, telemetry data path 복원, 벤더 감사 | 완료 |
| `05_RESEARCH_PRACTICE_GAPS.md` | Problem / Production practice / Closest research / Research maturity / Production maturity / Remaining gap / Evidence 표 + 축별 판정 | 완료 |
| `06_INITIAL_SC_RESEARCH_CANDIDATES.md` | 생존한 연구 후보별 상세 설계 + researchability 점수 + 최강 반론 | 완료 |
| `07_ANSWERS_TO_KEY_QUESTIONS.md` | 원 요청 §21의 10개 질문에 대한 직접 답변 | 완료 |

---

## 8. 조사 중 발견된 taxonomy 자체의 문제 (원 요청 §20에 따른 보고)

원 요청은 taxonomy가 잘못되었거나 예상 밖의 축이 반복 등장하면 명시하라고 지시했다. 네 가지가 있다.

**(1) L0–L7 사다리는 실제 분포를 잘못 예측한다.** 실제 분포는 연속적이지 않고 **L3에서 절벽**이다. 2020–2026 아카이벌 문헌에서 L3(detection)은 포화, L4(prediction)는 활발, **L5(RCA)는 희소, L6–L7은 사실상 공백**이다. SC 본프로그램 6년치에서 L7/D5에 도달한 논문은 **정확히 1편**(SC25 Aurora failure management)이며 그것도 학습이 아니라 정책 공학이다. HPDC/IPDPS/Cluster ~700건에서도 L7/D5는 사실상 1편(HPDC'24 RL-DRAM)이다. → **사다리를 한 칸씩 올라가는 로드맵보다, L3를 건너뛰고 L5–L7을 직접 노리는 편이 논문 관점에서 합리적이다.**

**(2) "monitoring 대 research"라는 대립축이 틀렸다.** SC25 SIREN(executable fuzzy hashing으로 애플리케이션 식별)이 보여주듯, **telemetry 수집 인프라 자체가 SC regular 기여로 인정된다** — 단, 그것이 *다른 사람들의 분석을 무효화하는 문제*를 풀 때만. 이는 원 요청의 "telemetry collection ≠ ... ≠ remediation" 구분과 모순되지 않지만, 수집 계층을 연구 대상에서 배제하면 안 된다는 뜻이다.

**(3) 예상하지 못했으나 반복 등장한 축: "평가 방법론 자체가 기여"인 논문 계열.** SC22 *A Taxonomy of Error Sources in HPC I/O Machine Learning Models*(왜 배포된 모델이 실패하는가), SC20 BSC의 cost-aware 평가(F1이 아니라 node-hour로 평가하라), AAAI'22 point-adjustment 비판(랜덤 점수가 SOTA를 이긴다), ISSRE'25 *Too Many Cooks*(multi-source fusion은 수익 체감), TOSEM의 data-splitting/model-update 계열. → **이 계열은 새 알고리즘 없이도 SC regular가 된다.** 데이터와 정직함만 필요하다. 신규 진입 그룹에게 가장 레버리지가 높은 형태다.

**(4) 가장 강한 SC regular precedent가 예상보다 오래되고, 기준이 예상보다 높았다.** SC20 Kaleidoscope는 Blue Waters 2년 telemetry와 **843건의 실제 운영자 확인 이슈**로 99.3% localization / 95.8% root-cause를 보고했다. 이것이 SC가 HPC RCA에 세운 기준선이며, 6년간 아무도 넘지 못했다. → **A축(cross-layer RCA)에 진입하려면 operator-confirmed incident label 확보가 전제조건이고, 이는 알고리즘보다 먼저 확보해야 할 자산이다.**

이 네 가지는 `05`와 `06`의 판정에 모두 반영되어 있다.

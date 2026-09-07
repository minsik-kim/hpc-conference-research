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

# 01. VENUE MAP — HPC AIOps / Operational Intelligence 연구 지형도

**대상:** KISTI 연구자 (한강 / KISTI-6 AIOps 과제)
**목적:** "SC Regular Paper"를 최종 목표로 할 때, 어떤 venue가 무엇을 담고 있고 어디부터 진입해야 하는지에 대한 참조 문서
**작성 기준일:** 2026-09-06
**출처:** `A_SC_main.md`(SC 본회의 전수조사 2020–2026), `B_hpdc_ipdps_cluster_isc_acsos.md`, `C_dsn_issre_lineage.md`, `D_workshops.md`, `E_cug_vendor.md`. 보조로 `F_axes_ABC.md` / `G_axes_DEFG.md`(ICS'25 WisIO, ICS'26 Mantis 확인용), `H_centers.md`.

> **표기 원칙.** 본 문서는 원 조사 노트의 검증 상태 표기를 그대로 승계한다. `VERIFIED`가 아닌 항목은 `UNVERIFIED` / `NOT FOUND` / `PARTIAL` / `NOT YET PUBLISHED`로 남겨 두었으며, 임의로 사실로 승격하지 않았다. 논문 제목·저자·연도·DOI·URL은 모두 원 조사 노트에서 그대로 옮긴 것이며 새로 만들어낸 항목은 없다.

---

## 1. 전체 구조 (한 장 요약)

### 1.1 생태계 계층도

```
                        ┌──────────────────────────────────────────────┐
   [APEX]               │  SC Technical Papers                         │
   최종 목표            │  (연 ~90–140편 중 본 주제 core 4–12편)        │
                        └───────────────▲──────────────────────────────┘
                                        │  승격 (rare: 워크숍→SC 직접 승격 사례 극소)
                        ┌───────────────┴──────────────────────────────┐
   [ARCHIVAL]           │ IEEE Cluster · IPDPS · HPDC · ISC(LNCS)      │
   피어리뷰 아카이브     │ DSN · ISSRE   (+ ACSOS = 개념 어휘 전용)      │
                        └───────────────▲──────────────────────────────┘
                                        │  method 성숙 / 데이터 자산 축적
                        ┌───────────────┴──────────────────────────────┐
   [WORKSHOP]           │ MODA(ISC,LNCS) · HPC-ODA(SC26 1st) · FTXS    │
   피어리뷰 워크숍       │ JSSPP(LNCS) · PDSW · HPCTESTS · PMBS · ESSA  │
                        │ HPCSYSPROS(Zenodo) · EESP · HUST · PERMAVOST │
                        └───────────────▲──────────────────────────────┘
                                        │  운영 문제의 최초 공개 지점
                        ┌───────────────┴──────────────────────────────┐
   [PRACTICE]           │ CUG (abstract 심사) · HPCSYSPROS · HPCTESTS  │
   비(非)아카이브 실무   │ ODA BoF 시리즈(2019–2025) · 벤더 발표         │
                        └──────────────────────────────────────────────┘

   ┌─── 병렬 트랙 (HPC 밖) : SC 리뷰어가 "이미 풀렸다"고 말할 때 인용하는 곳 ───┐
   │ OSDI · SOSP · NSDI · USENIX ATC · FAST · EuroSys · ICSE/FSE/ASE       │
   │ ISSRE(cloud 부분) · KDD · ASPLOS · MLSys                              │
   │  → novelty bar를 결정한다. 여기서 falsification을 통과하지 못하면        │
   │    SC 본회의 심사에서 살아남지 못한다.                                  │
   └───────────────────────────────────────────────────────────────────────┘
```

### 1.2 계층별 성격 요약표

| 계층 | 대표 venue | 심사 형태 | 아카이브 | 이 분야에서의 실제 역할 | 핵심 caveat |
|---|---|---|---|---|---|
| Practice | CUG, HPCSYSPROS, HPCTESTS, ODA BoF | abstract 심사(CUG) / 워크숍 심사 / 무심사(BoF) | CUG=ACM ICPS "may require additional review", HPCSYSPROS=Zenodo 자가아카이브, BoF=없음 | 운영 문제가 **최초로 공개되는 곳**. 정량 수치·실패 사례의 1차 출처 | method 유효성 근거로 인용 불가 (§6) |
| Workshop | MODA, HPC-ODA'26, FTXS, JSSPP, PDSW, HPCTESTS | 피어리뷰 | LNCS / IEEE Xplore / ACM SC-W / Zenodo | 커뮤니티 진입점. ODA 분야의 **유일한** 장기 피어리뷰 코퍼스(MODA)가 여기 | 규모가 극히 작다 (MODA 2020–2025 총 17편) |
| Archival | Cluster, IPDPS, HPDC, ISC, DSN, ISSRE | 정식 피어리뷰 | IEEE / ACM / Springer | 방법론이 검증되는 곳. SC 제출 전 "가장 가까운 선행연구"가 대부분 여기 | Cluster 2020–2022는 워크숍이 본 proceedings에 섞여 있음 (§3.4) |
| Apex | SC Technical Papers | 정식 피어리뷰 | IEEE(홀수년 이전)/ACM | 최종 목표 | 트랙 라벨을 논문 페이지에서 복원할 수 없음 (§2.3) |
| 병렬 non-HPC | OSDI/SOSP/NSDI/ATC/FAST/EuroSys/ICSE/FSE/ISSRE-cloud | 정식 피어리뷰 | — | **novelty bar 결정자**. Narya(OSDI'20), Perseus(FAST'23), SuperBench(ATC'24), RCACopilot(EuroSys'24) 등 | 여기서 이미 풀린 문제를 HPC로 옮기기만 하면 "domain change, not method change"로 반려 |

### 1.3 흐름에 대한 정량적 사실 두 가지

1. **워크숍 → 아카이브 승격은 사실상 일어나지 않는다.** `D_workshops.md` 기준으로 HPCSYSPROS 2020–2025 46편 중 **아카이브 후속 논문이 확인된 것은 0편**, HPCTESTS 2023–2025 10편 이상 중 **0편**이다. 명확히 확인된 lineage는 4개뿐이다(§5.5).
2. **SC 본회의에서 이 주제의 비중은 4–10%이며 2024년에 계단식으로 늘었다.** SC20 8편(~8%) → SC21 4편(~4%) → SC22 4편(~4%) → SC23 5편(~5%) → SC24 10편(~9%) → SC25 12편(~10%). SC26은 미발표(확인된 in-scope 논문 1편).

---

## 2. SC의 트랙 구조

### 2.1 트랙 종류와 성격

| 트랙 | 성격 | 아카이브 | 이 분야 관련성 |
|---|---|---|---|
| **Technical Papers** | 정규 연구 논문. 일반화 가능한 기여 요구 | proceedings 수록 | 최종 목표. Prodigy(SC23), Kaleidoscope(SC20), NodeSentry(SC25) 등이 여기 |
| **State of the Practice (SotP)** | 운영 실무 논문. **"do not need to cover novel research or developments"** | 동일 proceedings 수록 | **한강/KISTI-6 운영 논문의 정식 통로**. Frontier: Exploring Exascale(SC23), Fugaku 인센티브(SC24), El Capitan system noise(SC25)가 내용상 여기에 해당 |
| **Workshops** | 별도 CFP, SC-W proceedings | IEEE/ACM SC-W volume | HPC-ODA'26이 신설(§5) |
| **Posters** | 2페이지급, 요약 심사 | 별도 | 진입 비용 최저 |
| **BoF** | 비심사 커뮤니티 세션 | **아카이브 없음** | ODA는 2019–2025 내내 BoF로만 존재했다 (§5.1) |
| **Panels** | 비심사 | 없음 | — |
| **Tutorials** | 별도 심사(교육 자료) | 없음/부분 | 벤더 모니터링 스택 공개 문서로서 가치 (CUG 쪽에 더 많음, §6) |

### 2.2 SC26 State-of-the-Practice 트랙 — 검증된 원문

SC26 CFP(`sc26.supercomputing.org/program/papers/`)에서 확인된 SotP 트랙의 scope는 다음과 같다 (verbatim):

> *"All aspects of the pragmatic practices of HPC, including operational IT infrastructure, services, facilities, large-scale application executions and benchmarks"*

그리고 논문은

> *"capture experiences and ongoing practice relating to modern computing centers or HPC-related software"*

해야 하며

> *"do not need to cover novel research or developments."*

`A_SC_main.md`의 평가: **이것이 한강/KISTI-6 운영 논문의 정확한 진입로다.**

### 2.3 SC26 CFP 일정 (verified)

| 항목 | 일자 |
|---|---|
| Abstracts | 2026-04-01 |
| Papers | 2026-04-08 (**no extensions**) |
| AD(Artifact Description) appendix | 2026-04-28 (**mandatory**) |
| Notification | 2026-07-01 |
| Camera-ready | 2026-08-28 |
| 학회 개최 | 2026-11-15 ~ 11-20, Chicago, McCormick Place |

SC26 accepted-papers 전체 목록은 fetch 가능한 페이지에 게시되지 않았다(SC26 program site 401, ACM DL/IEEE Xplore 403). → **UNVERIFIED / UNAVAILABLE.**

확인된 in-scope SC26 논문은 2026-08-13 Best-Paper-finalist 발표에서 나온 **1편**뿐이다:

- **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** — Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin (**ORNL**) | SC26 Best Paper Nominee | DOI 미발급 | L5 | **SC-REGULAR-PRECEDENT (pending)**.
  저자 구성이 SC21 Summit power 논문, SC24 ExaDigiT, SC24 Frontier network cost 논문과 동일한 ORNL 운영 텔레메트리 그룹이다.

### 2.4 ⚠️ 전수조사가 부딪힌 한계 — 반드시 인지할 것

**SC의 per-paper 페이지는 트랙 라벨을 노출하지 않는다.** 모든 SC 논문 페이지가 트랙과 무관하게 "Technical Papers Archive"라는 라벨을 렌더링한다. dblp ToC 페이지 및 dblp/OpenAlex API는 robots/rate-limit로 접근 불가였고, ACM DL과 IEEE Xplore는 403을 반환한다.

> **결과: A_SC_main.md의 SC 항목은 거의 전부 `TRACK-UNKNOWN`이다.** "Technical Paper"인지 "State of the Practice"인지는 조사 시점에 복원되지 않았다. 조사자는 추정만 병기하고 추측으로 채우지 않았다.

즉, 본 survey에서 "SC23 Frontier 논문은 SotP다"류의 서술은 **내용 기반 추정**이며, 공식 트랙 라벨 확인이 아니다. 인용 시 이 구분을 유지할 것.

부수적 한계: SC24 사이트는 robots-blocked여서 Crossref(`10.1109/SC41406.2024`)로, SC25는 Crossref(`10.1145/3712285`)로 열거했다. 검증된 proceedings DOI는 SC20 `10.1109/SC41405.2020`, SC21 `10.1145/3458817`, SC22 `10.1109/SC41404.2022`, SC23 `10.1145/3581784`, SC24 `10.1109/SC41406.2024`, SC25 `10.1145/3712285`.

---

## 3. Tier A 메인 컨퍼런스별 프로파일

### 3.1 SC (The International Conference for High Performance Computing, Networking, Storage and Analysis)

**역할.** 최종 목표. 이 분야에서 "operational problem → generalizable systems research"의 최고 사례들이 모이는 곳이며, 동시에 State-of-the-Practice 트랙을 통해 순수 운영 논문도 수용한다.

**연도별 물량 (verified counts, ±2/년).**

| Year | 열거된 본회의 항목 | Core | Broad | Core 비율 | 열거 근거 |
|---|---|---|---|---|---|
| SC20 | ~105 | **8** | 14 | ~8% | proceedings index + Crossref |
| SC21 | ~110 | **4** | 8 | ~4% | proceedings index |
| SC22 | ~92 | **4** | 7 | ~4% | index + Crossref (2개 독립 열거가 일치) |
| SC23 | ~99 | **5** | 11 | ~5% | proceedings index |
| SC24 | ~114 | **10** | 17 | ~9% | Crossref only (사이트 robots-blocked) |
| SC25 | ~120 (재현성 리포트 ~20편 제외) | **12** | 18 | ~10% | Crossref only |
| SC26 | 미발표 | ≥1 확인 | UNKNOWN | — | CFP + Best Paper finalist 발표 |

**여기 사는 하위 주제.** 구조화된 수치 텔레메트리 기반의 (a) GPU/AI 클러스터 신뢰성, (b) power/cooling/carbon/water, (c) unsupervised anomaly detection, (d) I/O 진단, (e) 텔레메트리 인프라 자체, (f) LLM as ops tooling.

**대표 precedent (전부 검증된 DOI 보유).**

| 논문 | 연도/DOI | 왜 중요한가 |
|---|---|---|
| Live Forensics for HPC Systems (Kaleidoscope) — Jha, Iyer et al., UIUC/NCSA | SC20 | Blue Waters 2년 텔레메트리, 843건 실제 인시던트, localization 99.3% / RCA 95.8%, overhead <0.01%, 실제 배포. 이 census 전체의 template |
| Prodigy — Aksar, Coskun et al. (BU+Sandia) | SC23, `10.1145/3581784.3607076` | 라벨 없는 production anomaly detection. offline F1 0.95 / production 88%. KISTI anomaly 논문이 취해야 할 형태 |
| Fine-grained Automated Failure Management (Aurora) — Intel/Argonne | SC25, `10.1145/3712285.3759883` | census 전체에서 **유일한 L7/D5**. MTTR 최대 84× 감소. Aurora 10,624 nodes |
| GPU Lifetimes on Titan — Ostrouchov et al. (ORNL) | SC20 | 18,688 GPU, >100,000 GPU-year. survival analysis + **데이터·코드 공개** |
| Story of Two GPUs — Cui, Iyer et al. (UIUC/NCSA) | SC25, `10.1145/3712285.3759821` | Delta/DeltaAI 1,056 GPU, 2.5년, 11.7M GPU-hour. H100 memory MTBE가 A100 대비 **3.2× 악화**, ~5% overprovisioning 필요 |
| Cost-Aware Prediction of Uncorrected DRAM Errors — BSC | SC20 | **평가 방법론 자체가 기여**. F1/precision 대신 lost node-hour 비용모델. 57% 감소 = 연 ~21,000 node-hour |
| A Taxonomy of Error Sources in HPC I/O ML Models — Isakov et al. | SC22, `10.1109/SC41404.2022.00021` | negative-results / epistemics 논문. "왜 운영 ML이 배포되면 실패하는가" 5개 실패모드 |
| ExaDigiT — Brewer, F. Wang et al. (ORNL) | SC24, `10.1109/SC41406.2024.00029` | Frontier 6개월 텔레메트리 replay로 V&V된 liquid-cooled digital twin. facility↔IT 통합 축 |
| SIREN — Jakobsche, Ciorba (HPE/Basel, LUMI) | SC25, `10.1145/3712285.3759873` | 텔레메트리 수집 인프라 자체가 SC-regular 기여가 될 수 있음을 증명 |
| NodeSentry — S. Xia, Y. Sun et al. (Nankai) | SC25, `10.1145/3712285.3759794` | Prodigy의 직계 후속. F1 > 0.876, baseline 대비 +0.560, 학습 오버헤드 −45.69% |

**정직한 caveat.**
- 트랙 라벨 복원 불가 (§2.4). "SC Technical Paper"라고 단정할 수 없는 항목이 다수다.
- 열거는 long tail에 대해 **제목 기반**이다. 약 25편만 abstract를 읽었고 나머지는 제목만 읽었다. 오분류 가능성 ±2편/년.
- L/D/P 등급은 전부 조사자의 판단이며 논문에서 온 것이 아니다.
- SC26 accepted list는 **UNVERIFIED / UNAVAILABLE**.

**SC에서 눈에 띄게 부재한 것 (= 기회).** syslog/log analytics(본회의 사실상 0편), production Slingshot/Dragonfly 혼잡 진단(실측 필드 스터디 0편), facility 부품(CDU/펌프/밸브/칠러) 예지보전(0편), 텔레메트리 샘플링·축소·보존(시스템 텔레메트리 기준 0편), learned closed-loop remediation(0편), telemetry 기반 slow-node 탐지(0편), **cross-site 일반화(0편 — 사이트 A에서 학습한 운영 모델이 사이트 B에서 동작함을 보인 논문이 census에 없다)**.

---

### 3.2 HPDC (ACM High-Performance Parallel and Distributed Computing)

**역할.** ODA 프레임워크의 prestige outlet. "novel analytics mechanism"을 동반한 모니터링 프레임워크가 본트랙에 들어가고, 순수 인프라는 HPCMASPA 같은 워크숍으로 간다.

**볼륨 검증 (Crossref, front matter 포함).** 2020 `3369583` ✓ · 2021 `3431379` ✓ · 2022 `3502181` ✓ · 2023 `3588195` ✓ · 2024 `3625549` ✓ · 2025 `3731545` ✓ · 2026 `3806645` ✓ (2026-07-13 발행).

**핵심 논문.**

| 논문 | 연도/DOI | 의미 |
|---|---|---|
| **DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems** — Netti, Müller, Guillen, Ott, Tafani, Ozer, Schulz (LRZ+TUM) | HPDC 2020, `10.1145/3369583.3392674`, pp.101–112 | 아카이브 문헌에서 HPC ODA의 **레퍼런스 아키텍처** |
| **Towards HPC I/O Performance Prediction through Large-scale Log Analysis** — Sunggon Kim, Alex Sim, Kesheng Wu, Suren Byna, Yongseok Son, Hyeonsang Eom | HPDC 2020, `10.1145/3369583.3392678`, pp.77–88 | **한국인 1저자**, 한강 I/O 연구의 직접적 방법론 유사체 |
| **Understanding Memory Failures on a Petascale Arm System** — Ferreira, Levy, Hemmert, Pedretti (Sandia) | HPDC 2022, `10.1145/3502181.3531465`, pp.84–96 | Arm petascale 최초 필드 메모리 신뢰성 연구 |
| **AIIO: Using AI for Job-Level and Automatic I/O Performance Bottleneck Diagnosis** — Bin Dong, Jean Luca Bez, Suren Byna | HPDC 2023, `10.1145/3588195.3592986`, pp.155–167 | HPDC 세트에서 가장 깨끗한 L5(RCA) 사례 |
| **Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field** — Boixaderas, Moré, Bartolome, Vicente, Radojković, Carpenter, Ayguadé (BSC + MareNostrum 운영진) | HPDC 2024, `10.1145/3625549.3658686`, pp.240–252 | **census 전체에서 "predict → act under uncertainty"에 가장 근접**. 저자에 운영 스태프가 포함된 것이 "in the field" 주장의 신뢰 근거 |
| **Bringing Differential Privacy to HPC: Privacy-Preserving Transformations of HPC Traces** | HPDC 2025, `.3731573` | 국가센터가 텔레메트리를 공개하려 할 때 유일한 선행연구 |

**연도별 caveat.**
- HPDC 2021은 이 주제에 대해 얇다. Crossref에 ACM 단어형 축약 제목이 다수(**Apollo:**, **Holmes**, **Capri**, **TAC**, **SchedInspector**, **Heterogeneous Systems Resilience**) — **제목이 불완전하므로 ACM DL에서 재확인 필요**.
- **HPDC 2025 본트랙은 operational intelligence가 거의 비어 있다. 이것 자체가 finding이다.**
- **HPDC 2026 COVERAGE PARTIAL** — 볼륨의 ~50 레코드만 열거된 상태에서 rate limit에 걸렸다.

---

### 3.3 IPDPS (IEEE International Parallel and Distributed Processing Symposium)

**역할.** 이 분야에서 **가장 두꺼운 아카이브 본진**. 특히 telemetry 기반 workload characterization과 performance variability 축이 2024–2026 사이 IPDPS로 무게중심을 옮겼다.

**볼륨 검증 (main track only, 워크숍 제외).** 2020: 121 ✓ · 2021: 118 ✓ · 2022: 135 ✓ · 2023: 108 ✓ · 2024: 100 ✓ · 2025: 118 ✓ · 2026: 115 ✓.

**핵심 논문.**

| 논문 | 연도/DOI | 의미 |
|---|---|---|
| **Aarohi: Making Real-Time Node Failure Prediction Feasible** — Das, Mueller, Rountree | IPDPS 2020, `.00115`, pp.1092–1101 | failure prediction을 **정확도 문제가 아니라 latency 문제**로 재정의 |
| **Understanding the Interplay between Hardware Errors and User Job Characteristics on the Titan Supercomputer** — Seung-Hwan Lim, Miller, Vazhkudai (ORNL) | IPDPS 2020, `.00028`, pp.180–190 | **RAS + job accounting을 조인하는 정석**. 한강에 직접 이식 가능 |
| **The Case of Performance Variability on Dragonfly-based Systems** — Bhatele, Thiagarajan, Groves, Anirudh, Smith, Cook, Lowenthal | IPDPS 2020, `.00096`, pp.896–905 | production Dragonfly variability attribution |
| **CanarIO: Sounding the Alarm on IO-Related Performance Degradation** — Wyatt, Herbein, Shoga, Gamblin, Taufer (LLNL+UTK) | IPDPS 2020, `.00018`, pp.73–83 | canary probe 기반 온라인 공유 FS 경합 탐지 |
| **Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data** — Netti, Tafani, Ott, Schulz | IPDPS 2021, `10.1109/ipdps49936.2021.00010`, pp.2–12 | **이 다섯 venue 통틀어 유일한 텔레메트리 축소 논문**. 5년간 후속 없음 |
| **Systemic Assessment of Node Failures in HPC Production Platforms** — Das, Mueller, Rountree | IPDPS 2021, `.00035`, pp.267–276 | Aarohi를 정당화하는 필드 스터디(순서가 역방향) |
| **Drill: Log-based Anomaly Detection for Large-scale Storage Systems Using Source Code Analysis** — Di Zhang, Egersdoerfer, Mahmud, Mai Zheng, Dong Dai | IPDPS 2023, `.00028`, pp.189–199 | 로그를 뱉는 **소스코드를 semantic prior로 사용**. 라벨 문제 우회 |
| **Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining** — Baolin Li, Samsi, Gadepally, Tiwari | IPDPS 2024, `.00037`, pp.337–349 | **한강 GPU 텔레메트리 논문의 가장 가까운 기출간 유사체**. operator-consumability를 명시적으로 최적화 |
| **Cross-System Analysis of Job Characterization and Scheduling in Large-Scale Computing Clusters** | IPDPS 2024, `.00069` | census 전체에서 **거의 유일한 multi-system 비교 논문** |
| **An Effective Uncorrectable Memory Error Prediction Framework by Exploiting UPH Indicators in Production Environments** — Zheng, Qin, Li, Xia, Wu, Gu, Lin, Wan, Jiao, Huang | IPDPS 2025, `.00112`, pp.1238–1248 | HPDC'24 BSC 논문과 함께 memory failure prediction의 SOTA |
| **IOAgent: Democratizing Trustworthy HPC I/O Performance Diagnosis Capability via LLMs** — Egersdoerfer, Sareen, Bez, Byna, D.K. Xu, Dong Dai | IPDPS 2025, `.00036`, pp.322–334 | 최초의 **trustworthiness-aware** LLM ops 논문 |
| **Characterizing Production GPU Workloads using System-wide Telemetry Data** — Cankur, Austin, Kulkarni, Bhatele (UMD + NERSC) | IPDPS 2026, `.00078`, pp.899–912 | ★★ **한강 GPU 텔레메트리 전수조사의 가장 가까운 기출간 유사체. KISTI가 쓰는 것은 무엇이든 이것과 차별화되어야 한다** |
| **The Case of the Elusive Application Performance on Production GPU Supercomputers** — Cunyang Wei, Pradeep, Bhatele (UMD) | IPDPS 2026, `.00079`, pp.913–927 | Bhatele IPDPS'20의 GPU 세대 직계 후속 |
| **KORAL: Knowledge Graph Guided LLM Reasoning for SSD Operational Analysis** | IPDPS 2026, `.00085` | 2026 프론티어: LLM + 구조화된 운영 지식 |

**caveat.**
- **IPDPS 2022(135편, 이 구간 최대 볼륨)에는 anomaly detection이나 failure prediction 전담 논문이 하나도 없다.** 뚜렷한 골짜기.
- Crossref는 IEEE proceedings의 abstract를 담지 않는다. 위 표에서 저자명이 명시된 항목 외에는 저자 필드를 fetch하지 않았다 — **인용 전 반드시 재확인**.

---

### 3.4 IEEE Cluster

**역할.** 필드 신뢰성 연구와 "우리는 이걸 만들어 운영했다" 유형의 센터 경험 논문이 **본트랙**에 들어갈 수 있는 드문 아카이브 venue.

**볼륨 (레코드 수, front matter 포함).** 2020: 82 · 2021: 119 · 2022: 83 · 2023: 39 · 2024: 47 · 2025: 46 · 2026: **not found — PARTIAL / NOT YET PUBLISHED**.

#### ⚠️ 반드시 알아야 할 구조적 사실 — 2020–2022 "Cluster 논문"의 상당수는 워크숍 논문이다

**IEEE Cluster proceedings는 2022년까지 병설 워크숍을 같은 DOI 공간에 묶어 발행했고, 2023년부터 중단했다.**

- Cluster 2020(82), 2021(119), 2022(83)에는 **HPCMASPA, EE HPC SOP, REX-IO, EA-HPC** 논문이 본트랙 논문과 같은 DOI 공간에 들어 있다.
- Cluster 2023(39), 2024(47), 2025(46)은 **본트랙만** 포함한다.
- **결과:** 운영 측면에서 가장 자주 인용되는 2020–2022 "Cluster 논문" 몇 편이 실제로는 **워크숍 논문**이다. 대표적으로:
  - **PIKA: Center-Wide and Job-Aware Cluster Monitoring** (TU Dresden) — `10.1109/cluster49012.2020.00061` → **HPCMASPA 워크숍 논문**
  - **Global Experiences with HPC Operational Data Measurement, Collection and Analysis** — `.00071` → **EE HPC SOP 워크숍 논문** (이 분야의 레퍼런스 "state of practice" 문서지만 본트랙이 아니다)
  - **LDMS Darshan Connector** — Cluster 2022 `.00082` → HPCMASPA
  - **Towards Real-Time Classification of HPC Workloads via Out-of-band Telemetry** — Cluster 2022 `.00078` → HPCMASPA
  - **A Conceptual Framework for HPC Operational Data Analytics** — Cluster 2021 `.00086` → HPCMASPA (ODA 정의 논문이지만 워크숍이다)
  - **Sequence-RTG: Efficient and Production-Ready Pattern Mining in System Log Messages** — Cluster 2021 `.00090` → HPCMASPA

  → 이들을 "IEEE Cluster main track"으로 인용하면 **틀린다**. 조사 노트는 이들을 `[WORKSHOP-IN-PROCEEDINGS]`로 태깅했으며, 본 survey도 그 태깅을 승계한다.

**진짜 본트랙 핵심 논문.**

| 논문 | 연도/DOI | 의미 |
|---|---|---|
| **Quantifying the Impact of Network Congestion on Application Performance and Network Metrics** — Yijia Zhang, Groves, Cook, N. Wright, Coskun (BU+NERSC) | Cluster 2020, `.00026`, pp.162–168 | production 혼잡→성능 귀속 |
| **Monitoring Large Scale Supercomputers: A Case Study with the Lassen Supercomputer** — Patki, Bertsch, Karlin, Ahn, Van Essen, Rountree, de Supinski (LLNL), Besaw (IBM) | Cluster 2021, `.00057`, pp.468–480 | **"우리가 만들어 돌렸다" 원형이 본트랙에 들어간 증거.** 프로그램의 *첫* 논문으로 적합, SC 목표로는 부적합 |
| **Understanding the Effects of DRAM Correctable Error Logging at Scale** — Ferreira, Levy, Kuhns, DeBardeleben, Blanchard (Sandia+LANL) | Cluster 2021, `.00060`, pp.421–432 | 운영 의사결정이 붙은 필드 스터디 |
| **ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems** — Aksar, Sencan, Schwaller, Aaziz, Leung, Brandt, Kulis, Coskun (BU+Sandia) | Cluster 2022, `.00048`, pp.369–380 | ★★ **라벨 부족 문제를 정면으로 공격**. 라벨 0에서 시작하는 센터에 가장 이식성 높음 |
| **Are We There Yet? Predicting the Queue Wait Times for HPC Jobs** — Whitton, Jones, Walker, Job, Senator, DeBardeleben (LANL + Coastal Carolina) | Cluster 2025, `.11186489`, pp.1–12 | **랩이 저술한 사용자 대면 예측 서비스**. "센터 산출물이면서 동시에 논문"의 좋은 템플릿 |
| **Proactive SSD Failure Prediction with A Gradient-Guided LSTM-xLSTM Hybrid Model** | Cluster 2025, `.11186457`, pp.1–11 | 디바이스 failure prediction |

#### ⚠️ Cluster 2023 / 2024 본트랙에는 이 주제 논문이 아예 없다

- **Cluster 2023(39편): monitoring / anomaly detection / failure prediction 논문 0편.** 주제가 워크숍으로 빠져나갔다.
- **Cluster 2024(47편): 마찬가지로 0편.**
- **Cluster 2025(46편): 주제가 복귀했다** (SSD failure prediction, queue-wait prediction, SDC from hardware counters 등).

---

### 3.5 ISC High Performance (research paper track)

**역할.** HPC telemetry 기반 anomaly detection/diagnosis가 실제로 자리 잡은 곳 중 하나. BU(Coskun) ↔ Sandia(Brandt/Schwaller/Leung/Aaziz) 축이 지배한다.

#### ⚠️ 트랙 상태에 대한 정직한 보고

| 연도 | LNCS 볼륨 | 연구논문 수 | 상태 |
|---|---|---|---|
| 2020 | 978-3-030-50743-5 | **27** | ✓ verified |
| 2021 | 978-3-030-78713-4 | **24** | ✓ verified |
| 2022 | 978-3-031-07312-0 | **15** | ✓ verified |
| 2023 | 978-3-031-32041-5 | **20** | ✓ verified |
| 2024 | — | — | **UNVERIFIED** (Crossref에는 *Workshops* 볼륨 978-3-031-73716-9만 색인됨) |
| 2025 | — | — | **UNVERIFIED** |
| 2026 | — | — | **UNVERIFIED** |

- 연구논문 트랙은 **축소 추세**(27 → 24 → 15 → 20)이며, 2024–2026 Springer 연구논문 볼륨을 어떤 접근 가능한 색인에서도 찾지 못했다.
- isc-hpc.com은 여전히 research-paper 제출 트랙을 광고하고 있다(2027 에디션 마감일 게시).
- → **"ISC 연구논문 proceedings는 2020–2023 확인, 2024–2026 UNVERIFIED. Springer를 직접 확인하지 않고 '중단되었다'고 서술하지 말 것."**

**핵심 논문.**

| 논문 | 연도/DOI | 의미 |
|---|---|---|
| **Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems** — Aksar, Y. Zhang, Ates, Schwaller, Aaziz, Leung, Brandt, Egele, Coskun | ISC 2021, `10.1007/978-3-030-78713-4_11`, pp.195–214 | ★★ detection → **diagnosis**(어떤 종류의 이상인지)로 이동 |
| **Predicting Job Power Consumption Based on RJMS Submission Data in HPC Systems** | ISC 2020, `10.1007/978-3-030-50743-5_4` | **제출 시점 메타데이터만으로** 예측 — 런타임 텔레메트리 불필요 |
| **Analyzing Resource Utilization in an HPC System: A Case Study of NERSC's Perlmutter** | ISC 2023, `10.1007/978-3-031-32041-5_16` | "한강 utilization 전수조사" 논문의 직접적 ISC 선례 (저자 미fetch) |
| **NVIDIA's Quantum InfiniBand Network Congestion Control Technology and Its Impact on Application Performance** | ISC 2022 | 벤더+센터 공동 혼잡 연구 |

**ISC 워크숍 볼륨의 중요 항목(본트랙 아님).** ISC 2022 워크숍 `978-3-031-23220-6`: **Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems** `_18` — **이 census 전체에서 유일한 thermal anomaly 논문**; **Data Center Facility Monitoring with Physics Aware Approach** `_17`. ISC 2020 워크숍 `978-3-030-59851-8`: **Application IO Analysis with Lustre Monitoring Using LASSi for ARCHER** `_16`. ISC 2024 워크숍 `978-3-031-73716-9`: **Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository** `_20`.

---

### 3.6 DSN (IEEE/IFIP International Conference on Dependable Systems and Networks)

**역할.** 신뢰성 연구의 중량급 venue. **다만 HPC 비중은 매우 낮고, industry track이 오히려 HPC/AI 인프라에 가깝다.**

**커버리지.** 2020 ⚠ PARTIAL · 2021 ⚠ PARTIAL · 2022 ✅ · 2023 ✅ · 2024 ✅ · 2025 ✅ · 2026 ❌ NOT YET PUBLISHED.
DSN 2020(Valencia)/2021(Taipei) 사이트는 사라졌거나 robots-blocked이고 dblp ToC는 절단된다. **각 연도 dblp ToC의 앞 ~10개 항목만 검증됨. DSN 2020/2021에 대한 서술은 전부 명시적으로 flag되어 있으며, 이 census의 유일한 실질적 구멍이다.** 기관 네트워크에서 IEEE Xplore로 보완 필요(예상 추가 in-scope 논문 3–8편).

**HPC 관련 핵심.**

- **Time Machine: Generative Real-Time Model For Failure (and Lead Time) Prediction in HPC Systems** — Alharthi, Jhumka, Sheng Di, Lin Gui, Cappello, McIntosh-Smith | **DSN 2023** research track (session RT-14) | L4/D2/P1 | **"HPC failure prediction" SC 제출의 가장 가까운 DSN 측 선행연구. 반드시 인용·차별화**
- DSN 2022: `Predicting DRAM-Caused Node Unavailability in Hyper-Scale Clouds` (Alibaba); `Characterizing and Mitigating Anti-patterns of Alerts in Industrial Cloud Systems` (Huawei Cloud); `Active-MTSAD`
- DSN 2023: `HiMFP: Hierarchical Intelligent Memory Failure Prediction for Cloud Service Reliability` (Huawei Munich + TU Berlin); `How Different are the Cloud Workloads?` (Microsoft)
- DSN 2024 industry: **`Investigating Memory Failure Prediction Across CPU Architectures`** (Huawei) — **하드웨어 failure prediction 모델의 cross-generation/cross-architecture 전이에 대한 가장 직접적인 선행연구. 축 (B)에 치명적**; `Fault Localization Using Interventional Causal Learning for Cloud-Native Applications` (IBM)
- DSN 2024 research: `Mutiny! How does Kubernetes fail, and what can we do about it?` (Barletta, Cinque, Di Martino, Kalbarczyk, Iyer) — **fault-injection 기반 resource manager 실패 taxonomy. Slurm/PBS로 직접 이식 가능한 방법론 템플릿**
- **DSN 2025 industry track은 HPC/AI 인프라에 대해 이례적으로 풍부하다:**
  - `Large-Scale AI Infra Reliability: Challenges, Strategies, and Llama 3 Training Experience` (Meta+UBC) — 16K GPU 규모 레퍼런스 필드 경험 논문
  - `Hardware Telemetry at Scale: A Case Study on SSDs Endurance Monitoring in Datacenters` (Meta) — **"telemetry cost at scale"에 가장 가까운 기존 연구**
  - `Cordial: Cross-row Failure Prediction Method Based on Bank-level Error Locality for HBMs` — **HBM(=GPU 메모리) failure prediction 직접 선행연구**
  - `LLMPrism: Black-box Performance Diagnosis for Production LLM Training Platforms` — **GPU 클러스터 cross-layer 진단의 최근접 이웃, 1년밖에 안 됨**
  - `DDR5 DRAM Faults in the Field`

---

### 3.7 ISSRE (IEEE International Symposium on Software Reliability Engineering)

**역할.** log anomaly detection, KPI anomaly detection, RCA, label-scarce learning **방법론**의 본진. 클라우드/마이크로서비스가 압도적이며, HPC는 소수다.

**커버리지.** 2020–2025 전 연도 ✅ full (공식 프로그램 페이지에서 전체 ToC 확보). 2026 ❌ NOT YET PUBLISHED (CFP 유통 중).

**HPC 관련 핵심.**

- **Exploring Hierarchical Patterns for Alert Aggregation in Supercomputers** — Yuan Yuan, Tongqing Zhou, Xiuhong Tan, Yongqian Sun, Yuqi Li, Zhixing Li, Zhiping Cai, Tiejun Li | **ISSRE 2024, Best Paper Award/Candidate** | 슈퍼컴퓨터 alert storm 축약. **중국 국가랩 슈퍼컴 텔레메트리가 출판되고 있다는 증거**
- **ClusterRCA: An End-to-End Approach for Network Fault Localization and Classification for HPC System** — Yongqian Sun, Xijie Pan, Xiao Xiong, Lei Tao, Jiaju Wang, Shenglin Zhang, Yuan Yuan, Yuqi Li, Kunlin Jian | **ISSRE 2025** | **"HPC interconnect RCA" 주장에 대한 최근접 선행연구**

**⚠️ novelty hazard로서의 ISSRE.**

- **Too Many Cooks: Assessing the Need for Multi-Source Data in Microservice Failure Diagnosis** — Shenglin Zhang, Xiaoyu Feng, Runzhou Wang, Minghua Ma, Wenwei Gu, Yongqian Sun, Zedong Jia, Jinrui Sun, Dan Pei | **ISSRE 2025, Best Research Paper Candidate** | **다중 소스 융합이 진단 성능에 감소하거나 부정적인 수익을 낸다는 실증 결과.** "우리는 CPU/GPU/네트워크/스토리지/스케줄러 텔레메트리를 융합했고 그게 기여다"라고 쓰면 이 논문이 정면으로 반박한다. **Danger: HIGH — 문제를 풀렸다고 하는 게 아니라 전제가 틀렸다고 말하는 유형**
- **Can We Trust Auto-Mitigation? Improving Cloud Failure Prediction with Uncertain Positive Learning** — Haozhe Li, Minghua Ma 외 (Microsoft) | **ISSRE 2024** | closed-loop을 돌리면 ground-truth 라벨이 파괴된다는 문제의 가장 날카로운 진술. closed-loop HPC remediation을 제안하면 이 논문이 정의한 평가 문제를 풀어야 한다
- **ZeroLog: Zero-Label Generalizable Cross-System Log-based Anomaly Detection** (ISSRE 2025) — cross-system 일반화 주장에 **Danger: VERY HIGH**
- **Prepared for the Unknown: Adapting AIOps Capacity Forecasting Models to Data Changes** (ISSRE 2025) — concept drift 프레이밍에 **Danger: HIGH**
- 라벨 희소성 계열은 ISSRE에 매우 두껍게 축적되어 있다: Robust KPI AD with Partial Labels(2021), PUTraceAD(2022), AutoKAD(2023, Best Paper Candidate), AFALog(2023), LabelEase(2024), LogCAE(2024), fKPISelect(2023). → **"라벨 효율 기법"을 기여로 내세우면 incremental로 반려된다.**
- **Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics** — Zhu, He, He, Liu, Lyu | ISSRE 2023 | 사실상의 벤치마크 코퍼스. **BGL/Thunderbird/Spirit 등 2007년산 HPC 로그를 포함한다. 2024–25 논문들이 여전히 2007 로그로 평가받고 있다는 것 자체가 exploitable한 논거**

**구조적 관찰.** DSN + ISSRE 6년치에서 **HPC 특화 operational-intelligence 논문은 대략 5편**(Time Machine DSN'23, Alert Aggregation ISSRE'24, ClusterRCA ISSRE'25 + DSN'25 industry의 GPU/HBM/AI-infra 항목). 나머지는 전부 클라우드/마이크로서비스다. → **venue는 HPC 쪽에서 포화되지 않았다. 포화는 method 쪽에서 일어났다.**

---

### 3.8 ACSOS (IEEE International Conference on Autonomic Computing and Self-Organizing Systems)

**역할 — 명확히 하자: ACSOS는 HPC venue가 아니다.**

**볼륨 검증.** 2020 `acsos49614` ✓ · 2021 `acsos52086` ✓ · 2022 `acsos55765` ✓ · 2023 `acsos58161` ✓ · 2024 `acsos61780` ✓ · 2025 `acsos66086` ✓ (~13편) · 2026 NOT YET PUBLISHED.

#### ⚠️ 검증된 부정 결과

> **ACSOS 2020–2025 본트랙에서 HPC/슈퍼컴퓨터 시스템 위에서 평가된 논문은 0편이다.**
> 모든 것이 cloud microservices, serverless, Kubernetes, CPS, robotics, IoT, swarm, self-adaptive software다. HPC 성격의 항목은 단 하나이며 그것도 **companion/workshop** 논문이다 — *Data Separation Scheme on Lustre Metadata Server based on Multi-stream SSD* (ACSOS-C 2021, `acsos-c52956.2021.00026`).
> **ACSOS는 개념적 프레이밍(MAPE-K, self-adaptation, uncertainty, causal RCA)에만 사용하고, HPC 적용성의 근거로는 절대 인용하지 말 것.**

**개념적으로 인용할 가치가 있는 항목.**

| 논문 | 연도 | 왜 |
|---|---|---|
| **Causal Inference Techniques for Microservice Performance Diagnosis: Evaluation and Guiding Recommendations** — Li Wu, Tordsson, Elmroth, Kao | ACSOS 2021, `.00029` | ACSOS 내 최고의 범용 RCA 방법론 인용처 (L5, cloud, P4) |
| **On Evaluating Self-Adaptive and Self-Healing Systems using Chaos Engineering** | ACSOS 2022, `.00018` | self-healing **평가 방법론** — D3/D4 실험 설계에 유용 |
| **Prolego: Time-Series Analysis for Predicting Failures in Complex Systems** | ACSOS 2023, `.00025` | ACSOS 유일의 failure prediction 논문 |
| **ClearCausal: Cross Layer Causal Analysis for Automatic Microservice Performance Debugging** | ACSOS 2024, `.00039` | 2024 최고의 RCA 방법 |
| **Uncertainty-Driven Monitoring for ML-Based Autonomic Systems** | ACSOS 2025, `.00021` | **모델 불확실성이 모니터링 정책을 구동한다** — 2025년 항목 중 가장 이식성 높음. 텔레메트리 적응 샘플링 축과 직결 |
| **Finding Relevant Causes in Complex Systems: a Generic Method Adaptable to Users and Contexts** | ACSOS 2025, `.00026` | L5 |

**전략적 함의.** ACSOS는 어휘(MAPE-K, self-healing, antifragility, uncertainty-driven monitoring)를 가지고 있고 시스템이 없다. HPDC/IPDPS/Cluster는 시스템을 가지고 있고 어휘가 없다. **이 둘을 명시적으로 잇는 것 — ACSOS 수준의 self-adaptation 형식론을 국가 슈퍼컴퓨터 위에 구현·평가하는 것 — 은 진짜로 비어 있는 자리다.**

---

### 3.9 Tier A 하위 주제별 "사실상의 본거지" (B_hpdc_ipdps_cluster_isc_acsos.md §6 기준, 5개 venue 범위 내)

| 하위 주제 | 본거지 | 근거 |
|---|---|---|
| Field reliability / failure characterization | **IEEE Cluster main + IPDPS** (HPDC가 prestige outlet) | Ferreira Cluster'21→HPDC'22; Das/Mueller IPDPS'20→'21; Lim/ORNL IPDPS'20. *(DSN과 SC가 진짜 중량급이며 이 범위 밖)* |
| Monitoring / ODA 인프라 | **HPDC(Wintermute) + Cluster/HPCMASPA** | 신규 분석 메커니즘이 있어야 HPDC 본트랙, 순수 인프라는 HPCMASPA |
| HPC 텔레메트리 anomaly detection & diagnosis | **ISC research track + IEEE Cluster** — BU(Coskun) ↔ Sandia 축 지배 | Proctor(ISC'21), ALBADross(Cluster'22) |
| Log anomaly detection | **IPDPS** (Dai/UNC-Charlotte + Zheng/Iowa State) | Drill IPDPS'23; ChatGPT-logs HPDC'23 short; Sequence-RTG(HPCMASPA'21) |
| I/O 성능 진단 / RCA | **HPDC + IPDPS**, Darshan/DXT(LBNL: Byna, Bez) 생태계 중심 | AIIO HPDC'23; TunIO/Drilling-Down/Periodic-I/O IPDPS'24; IOAgent IPDPS'25 |
| Performance variability & network congestion | **IPDPS** (Bhatele 라인), Cluster 보조 | IPDPS'20 Dragonfly → IPDPS'26 Elusive GPU |
| 텔레메트리 기반 workload characterization | **IPDPS 2024–2026** — 명백히 부상하는 중심 | Li/Tiwari IPDPS'24; Cross-System IPDPS'24; Cankur/Bhatele/NERSC IPDPS'26 |
| Memory error prediction & mitigation | **HPDC(BSC) + IPDPS(industry) + Cluster(Sandia/LANL)** | HPDC'24 RL-DRAM; IPDPS'25 UPH; Cluster'21 CE logging |
| Queue-wait / runtime prediction | **IEEE Cluster**(랩) + HPDC 포스터 | Cluster'25 LANL queue-wait; HPDC'26 poster |
| RL/지능형 스케줄링 | **IPDPS + Cluster** 반반 | MRSch, SchedInspector, READYS, IPDPS'26 imitation learning |
| Self-healing / autonomic | **ACSOS — 단, 클라우드 전용. 이 5개 venue에 HPC 본거지가 없다** | §3.8 |
| Thermal / cooling / facility | **어떤 본트랙에도 없다.** Cluster/EE HPC SOP와 ISC 워크숍뿐 | ISC'22 워크숍 thermal anomaly; Cluster'20 EE HPC SOP |
| 텔레메트리 샘플링·축소 | **IPDPS'21 Correlation-wise Smoothing, 사실상 단독** | — |
| 분산학습 anomaly | **부재.** MLSys/OSDI/NSDI가 소유 | — |

---

## 4. Tier B 확장 venue — 언제 가는가

### 4.1 사용 규칙

> **Tier B는 "논문을 낼 곳"이 아니라 "novelty를 반증(falsify)하기 위해 closest-work를 찾으러 가는 곳"이다.**
>
> SC 리뷰어가 "이건 이미 풀렸다"고 말할 때 드는 논문의 대부분은 Tier B, 특히 OSDI/NSDI/ATC/FAST/EuroSys에 있다. 관련연구를 쓰기 전에 해당 축의 Tier B 최근접 이웃을 반드시 읽고 **서론에서** 차별화해야 한다(관련연구 섹션이 아니라). 예: closed-loop remediation을 제안하면 "why is this not Narya with a different action set?"이라는 질문이 반드시 나온다.

### 4.2 venue별 실제 내용물

| Venue | 무엇이 여기 있는가 (검증된 구체 항목) | 언제 가는가 |
|---|---|---|
| **FAST** | **fail-slow 계보의 본거지.** `Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems` — Gunawi 외 16개 기관(LANL, ANL 포함), **FAST 2018**, 101건 인시던트 리포트 + fault→symptom 변환 taxonomy = **축 (D)의 정의 논문**. `Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems` — Ruiming Lu, Erci Xu 외(SJTU/Alibaba/Xiamen), **FAST 2023**, 248,000 drive/10개월, fail-slow 304건 발견, p99.99 tail latency 48% 감소, **라벨된 데이터셋 공개**(정상 41K, 검증된 fail-slow 315). `Making Disk Failure Predictions SMARTer!` — Sidi Lu, Tirthak Patel, Tiwari, Weisong Shi, **FAST 2020**, 380,000 drive/64 사이트, 10일 horizon F1 0.95 / MCC 0.95 | slow-node / fail-slow / 디바이스 failure prediction을 주장하기 전 |
| **OSDI** | **Narya**: `Predictive and Adaptive Failure Mitigation to Avert Production Cloud VM Interruptions` — Levy, Yao, Wu, Dang 외(Microsoft Azure) + Peng Huang(JHU), **OSDI 2020**, pp.1155–1170. 예측 + **online experimentation/bandit-RL로 완화 조치 선택**, **15개월 프로덕션, VM 중단 26% 감소**. L4+L6+L7 / D5. → **축 (F)에 대한 단일 최강 반증**. **FIRM**: Qiu, Banerjee, Jha, Kalbarczyk, Iyer(UIUC), **OSDI 2020**, pp.805–825, SLO 위반 마이크로서비스 + 경합 자원(CPU/mem/net/IO) 식별 후 RL 재프로비저닝 | closed-loop remediation, 자원 병목 식별 |
| **USENIX ATC** | **SuperBench**: `Improving Cloud AI Infrastructure Reliability with Proactive Validation` — Yifan Xiong 외(MSR + Microsoft 13인), **ATC 2024 Best Paper**. GPU 하드웨어를 선제적으로 벤치마킹해 **gray failure**를 학습 저하 전에 발견; **시간 예산 하에서 검증 스케줄을 최적화하는 Selector**; MTBI 최대 **22.61×** 개선; Azure에서 **수십만 GPU 규모로 2년간 배포**. → 축 (D) GPU 하위사례 최강 반증이자 **축 (C)에 존재하는 가장 가까운 formulation**. **IASO**(ATC 2019, Nutanix 계열): 39,000 노드/1.5년+, peer 기반 timeout 신호로 느린 노드를 "수 분 내" 격리, 인시던트 232건/연간 fail-slow율 1.02% → **peer-comparison slow-node 탐지는 이미 프로덕션에서 해결된 기술이다. "우리는 노드를 이웃과 비교한다"는 기여가 될 수 없다** | GPU gray failure, 검증 비용 최적화, slow-node |
| **NSDI** | **Acme**: `Characterization of Large Language Model Development in the Datacenter` — Qinghao Hu 외, **NSDI 2024**, pp.709–729. 6개월 GPU 데이터센터 trace, job failure taxonomy, 결함 진단+복구가 포함된 fault-tolerant pretraining, **trace 공개**. **MegaScale**: Ziheng Jiang 외(ByteDance)+Yinmin Zhong, Xin Jin(PKU), **NSDI 2024**, pp.745–760, 12,288 GPU 안정성을 위한 full-stack 진단 도구, MFU 55.2%. **Hindsight**: `The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems` — Lei Zhang, Zhiqiang Xie, Anand, Vigfusson, Mace, **NSDI 2023**, pp.321–339, retroactive trace sampling("dash-cam") → **축 (C)에 대한 가장 중요한 선행연구지만 trace 한 채널만 다룬다**. **Monet**: `Measuring Congestion in High-Performance Datacenter Interconnects` — Jha, Patke, Lim, Kalbarczyk, Kramer, Iyer, Brandt, Gentile, Showerman, Bauer, Kaplan, **NSDI '20**, Blue Waters Gemini/Aries 네트워크 카운터 기반 혼잡 영역 탐지 — **fabric counter 관련 연구의 최근접 방법론 조상** | 분산학습 신뢰성, tracing cost, 네트워크 혼잡 |
| **FAST/ATC/NSDI 종합** | 위 세 venue가 사실상 "이미 프로덕션에서 풀린 것"의 목록을 정의한다 | 모든 축 |
| **EuroSys** | **RCACopilot**: `Automatic Root Cause Analysis via Large Language Models for Cloud Incidents` — Yinfang Chen, Minghua Ma 외, **EuroSys 2024**. handler-matched 진단 수집 → 근본원인 분류 예측 → 서술 생성. Microsoft 1년치 인시던트, RCA 정확도 최대 0.766, **진단 수집 컴포넌트는 4년+ 프로덕션 운영**. → **축 (G)의 기준점. 지속된 기여는 LLM이 아니라 handler/evidence-collection 아키텍처였다는 점이 핵심 교훈**. **Just-In-Time Checkpointing**(EuroSys 2024, Microsoft). 역사적으로: `Fingerprinting the datacenter` — Bodík, Goldszmidt, Fox, Woodard, Andersen, **EuroSys 2010** — 시스템 전역 성능 상태의 signature 표현, cross-layer 상태 표현의 직계 조상 | LLM 기반 RCA, 상태 표현 |
| **SOSP** | `Detecting large-scale system problems by mining console logs` — Wei Xu, Ling Huang, Fox, Patterson, Jordan, **SOSP 2009**, pp.117–132, `10.1145/1629575.1629587` — "parse → featurize → detect"의 방법론적 뿌리 | 로그 분석 계보 인용 |
| **ICSE / FSE / ASE** | **log anomaly와 AIOps 방법론 문헌의 본거지.** `Recommending Root-Cause and Mitigation Steps for Cloud Incidents using Large Language Models` — Ahmed, Ghosh, Bansal, Zimmermann, Zhang, Rajmohan, **ICSE 2023**, Microsoft 인시던트 40,000+ — 이 장르를 만든 논문. `Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data` — Cheryl Lee 외, **ICSE 2023**(venue/저자 `UNVERIFIED` — fetch 실패). `Tools and benchmarks for automated log parsing` — Zhu 외, **ICSE-SEIP 2019** → Logparser → Loghub. 2024–26에도 LogLM(ICSE'25), R-Log(ICSE-SEIP'25), OpsEval(FSE'25), TrioXpert(ASE'25) 등 계속 나옴. `UNVERIFIED`: Nezha(ESEC/FSE 2023) | LLM ops, 로그 파싱, AIOps 방법론 전반 |
| **ISSRE (cloud 부분)** | §3.7 참조. 라벨 희소 학습, KPI/trace anomaly, incident 관리의 방법론 대부분 | 방법론 novelty 확인 |
| **ICS (ACM International Conference on Supercomputing)** | **Summit GPU 메모리 손상 논문이 여기 있다**: `Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study` — **ICS'24**, `10.1145/3650200.3656615`. 27,648개 V100; DBE가 동일 GPU에서 재발; **온도가 아니라 지속 전력과 상관**. ⚠️ *저자 순서에 출처 간 불일치가 있다: `D_workshops.md`는 "Oles, Schmedding, Ostrouchov, Shin, Smirni, Engelmann", `H_centers.md`는 "Shin, Oles, Schmedding, Ostrouchov, Smirni, Wang". 인용 전 원문 확인 필요.* 또한 **WisIO**: `Automated I/O Bottleneck Detection with Multi-Perspective Views for HPC Workflows`, **ICS'25**, `10.1145/3721145.3725742` (저자 `UNVERIFIED`), 그리고 **Mantis**: `Decoding HPC Telemetry Data for Robust System Prediction`, **ICS'26**, `10.1145/3797905.3800527` — **내용 UNVERIFIED(403 차단으로 읽지 못함). 관련연구를 쓰기 전에 반드시 확보해서 읽을 것 — 판정을 뒤집을 수 있는 항목으로 표시되어 있다** | GPU 신뢰성, I/O 병목, HPC 텔레메트리 예측 |
| **KDD** | `Critical event prediction for proactive management in large-scale computer clusters` — Sahoo, Oliner, Rish, Gupta, Moreira, Ma, Vilalta, Sivasubramaniam, **KDD 2003**, pp.426–435 — 이 계보의 출발점. 최근: `Don't Predict, Prioritize` (HeaRank), **KDD 2026** accepted, GPU 실패 *시점*은 예측 불가하므로 learning-to-rank 위험 우선순위화로 대체; AUC 0.83, 상위 5% 노드에 실패의 64% 집중(기존 21% 대비). `UNVERIFIED`: Nenya(KDD 2022) | 예측 vs 우선순위화 프레이밍 |
| **SIGMETRICS** | `DRAM errors in the wild: a large-scale field study` — Schroeder, Pinheiro, Weber, **SIGMETRICS/Performance 2009**, pp.193–204, `10.1145/1555349.1555372` — 모든 DRAM/HBM failure prediction 논문의 조상 | 필드 신뢰성 통계 계보 |
| **ASPLOS** | `UNVERIFIED`: Sage(Gan, Liang, Dev, Lo, Delimitrou, ASPLOS 2021), Mint(cost-efficient tracing, ASPLOS 2024). **ACM DL 차단으로 이 세션에서 검증 불가 — 인용 전 확인** | cross-layer 진단, tracing 비용 |
| **MLSys** | 분산학습 anomaly detection이 HPC 5개 venue에서 부재하고 **MLSys/OSDI/NSDI가 소유**하고 있다는 것이 조사 결과 | 분산학습 축 |
| **CCGrid** | `LOGAIDER: A Tool for Mining Potential Correlations of HPC Log Events` — Sheng Di, Gupta, Snir, Pershey, Cappello, 2017, CCGrid (`UNVERIFIED`), IEEE 7973730 — 고전적 HPC 로그 상관 RCA | 로그 상관 계보 |
| **Euro-Par** | **E2EWatch: An End-to-End Anomaly Diagnosis Framework for Production HPC Systems** — Aksar, Schwaller, Aaziz, Leung, Brandt, Egele, Coskun, **Euro-Par 2021**, `10.1007/978-3-030-85665-6_5`. Sandia Eclipse(1,488 노드)에서 LGBM으로 60초 텔레메트리 윈도우를 memleak/membw/cpuoccupy/cachecopy/normal로 분류 — 단, **anomaly는 HPAS로 합성 주입**. BU 라인의 operator-facing 패키징 | BU/Sandia 계보 추적 |
| **ICPE** | 조사 노트에 별도 항목 없음 — **NOT COVERED in this census** | 성능 공학 벤치마킹 |

### 4.3 Tier B가 이미 닫아버린 것 (반드시 인지)

`C_dsn_issre_lineage.md` PART D의 축별 판정을 요약하면:

| 축 | 판정 | 닫힌 부분 / 열린 부분 |
|---|---|---|
| (C) telemetry cost vs downstream quality | **STILL_OPEN — 7개 축 중 최강** | 열림: 여러 채널을 예산 하에서 동시에 최적화하는 joint formulation. 닫힘 위험: SuperBench의 Selector(명시적 반증 필요) |
| (F) safe remediation with HPC cost model | **STILL_OPEN (조건부)** | 닫힘: 개념 자체(Narya). 열림: HPC의 비가역적·allocation 기반 action space에 대한 비용모델과 안전 봉투 |
| (E) label semantics | **PARTIALLY_ADDRESSED — 방법은 CLOSED, 라벨 의미론은 OPEN** | "라벨을 적게 쓰는 학습"은 죽었다. "HPC 운영에서 라벨이란 무엇이며 우리가 가진 것은 얼마나 틀렸나"는 measurement 기여로 방어 가능 |
| (A) cross-layer RCA | **PARTIALLY_ADDRESSED** | 열림: collective-sync 인지 귀속, 스케줄러 배치를 *인과 변수*로, 공유 PFS 간섭. 필수 방어: "Too Many Cooks"에 ablation으로 답하고 LLMPrism 대비 포지셔닝 |
| (D) slow-node attribution | **탐지는 거의 CLOSED, 간섭 vs 내재 귀속만 OPEN** | 하드 블로커: **Tuncer et al., TPDS 2019**(HPC 노드 텔레메트리로 성능 이상의 *종류*를 분류 — 7년 전에 이미 이 축을 했다), SuperBench, NodeSentry(SC'25 — 타겟 venue에 있다) |
| (B) cross-generation generalization | **PARTIALLY_ADDRESSED** | ML 방법 경로는 닫혔다. 열림: N=1-per-generation 체제와 조달 세대 간 telemetry-schema 불일치 — **domain-adaptation 알고리즘이 아니라 systems/measurement 문제로 프레이밍할 것** |
| (G) LLM agents | **ENGINEERING_ONLY** | 단독 축으로는 불가. (C)나 (F)의 메커니즘을 실어 나르는 캐리어일 때만 성립 |

**두 가지 교차 관찰.**
1. **가장 저평가된 자산은 공개된 현대적 다층 HPC 텔레메트리 코퍼스다.** 이 분야는 아직도 Oliner & Stearley의 2007년 BGL/Thunderbird/Spirit 로그로 벤치마킹하고 있다(Loghub 경유).
2. **차별화 요인은 method novelty가 아니라 deployment depth다.** D4/D5(운영자 워크플로 또는 closed-loop)에 도달한 논문은 드물고 거의 전부 산업계다(Narya, Perseus, IASO, SuperBench, Azure auto-mitigation, Meta Ripple). **학계 HPC 운영지능 논문 중 D2를 넘는 것은 거의 없다.** 국가 슈퍼컴에서 D3(shadow)이나 D4(운영자 워크플로)에 도달하는 것 자체가 어떤 모델링 개선보다 강한 주장이다.

---

## 5. Workshop ecosystem

### 5.0 ⚠️ 세 가지 헤드라인 정정 — 이 절에서 가장 중요한 부분

> **(a) SC 계열 ODA "워크숍"은 2026년 이전에 존재하지 않았다.**
> 2019–2025년의 SC/ISC ODA 활동은 전부 **BoF 시리즈**였고 피어리뷰 워크숍이 아니었다. `HPC-ODA 2026`은 SC26에서 열리는 **제1회** International Workshop on HPC Operational Data Analytics이며, "eight years of successful BoF sessions at SC and ISC"를 피어리뷰로 전환한다고 명시하고 있다.
> → **구조적 함의: SC 쪽 ODA 커뮤니티는 8년간 운영 문제를 생산했지만 아카이브 논문 흔적이 전혀 없다.**
>
> **(b) MODA가 유일한 장기 피어리뷰 ODA venue이며, 매우 작다.**
> ISC 계열, Springer LNCS, 연 2–5편. **2020–2025 통틀어 아카이브 챕터 17편** — 이것이 "HPC operational data analytics"라는 이름의 피어리뷰 코퍼스 전체다. 2026년 제7회부터 **"Monitoring, Observability, and Operational Data Analytics"로 개명**되었다.
>
> **(c) FTXS는 SC25에 열리지 않았고, SC26에서 AI 시스템으로 재범위화되었다.**
> SC26 명칭: *"Faults, Trustworthiness, and eXplainability for **AI Systems** at Scale."* 고전적 HPC resilience 레인이 닫히고 있다. → **운영 관련 연구를 FTXS에 겨냥하지 말 것.**

### 5.1 HPC-ODA (SC) — BoF 시리즈 → 2026년 1st 워크숍

| Year | 개최 | 형태 | Host | Proceedings | 피어리뷰 | 편수 |
|---|---|---|---|---|---|---|
| 2019 | Yes | **BoF** | SC19 | 없음 | No | — |
| 2020 | **NOT FOUND** | — | — | — | — | — |
| 2021 | Yes ×2 | **BoF** | ISC21("Guidelines for HPC Data Center Monitoring"), SC21 | 없음 | No | — |
| 2022 | Yes | **BoF** ("Drowning in Data") | SC22 | 없음 | No | — |
| 2023 | Yes ×2 | **BoF** | ISC23, SC23 | 없음 | No | — |
| 2024 | Yes ×2 | **BoF** (ISC24 "HPC Efficiency Improvements with Interoperable Monitoring"; SC24 "Data Journey Towards Insights") | ISC24, SC24 | 없음 | No | — |
| 2025 | Yes | **BoF** ("Operational Data Analytics: Mind the Gap") | SC25 | 없음 | No | — |
| **2026** | **Yes — 제1회 WORKSHOP** | Workshop | SC26, Chicago | **SC26 Workshop Proceedings, IEEE Xplore** | **Yes** | `PARTIAL / NOT YET HELD` (제출 마감 2026-08-12) |

- **2026 조직위:** Michael Ott (LRZ), Ayse Coskun (BU), Jeff Hanson (HPE), Melissa Romanus (NERSC/LBNL), Woong Shin (ORNL), Tim Osborne (ORNL). **PC 30인.**
- **형식:** 8p full / 4p short / 1–2p lightning talk.
- ⚠️ `hpc-oda.org/events/`(Nov 16; CFP Jul 31)와 `/workshop2026/`(Nov 20; 마감 Aug 12) 사이에 날짜 불일치가 있다. **어느 쪽이 맞는지 `UNVERIFIED`.**
- 커뮤니티 산출물은 논문이 아니라 **EE HPC WG workshop report**였다.

### 5.2 MODA (ISC, Springer LNCS)

| Year | 회차 | 개최일 | LNCS 볼륨 | 피어리뷰 | 챕터 |
|---|---|---|---|---|---|
| 2020 | 1st ("Monitoring and **Data** Analytics") | 2020-06-25 | 978-3-030-59851-8 | Yes | **3** |
| 2021 | 2nd | 2021-07-02 (virtual) | 978-3-030-90539-2 | Yes | **2** |
| 2022 | 3rd | 2022-06-02 | 978-3-031-23220-6 | Yes | **2** |
| 2023 | 4th | 2023-05-25 | 978-3-031-40843-4 | Yes | **3** |
| 2024 | 5th | 2024-05-16 | 978-3-031-73716-9 | Yes | **2** (+ lightning talk 4건, 미아카이브) |
| 2025 | 6th | 2025-06-13 | 978-3-032-07612-0 | Yes | **5** |
| 2026 | **7th — 개명** "Monitoring, **Observability**, and Operational Data Analytics" | 2026-06-26 | ISC26 workshops LNCS `NOT YET PUBLISHED` | Yes | **5** 발표 |

**합계 2020–2025 = 17 아카이브 챕터.** 프로그램 URL: `moda.dmi.unibas.ch`(2022–2026), `moda21.sciencesconf.org`, `moda20.sciencesconf.org`.
⚠️ unibas 아카이브 페이지는 MODA23/24/25를 모두 "Fourth"로 잘못 표기한다. **LNCS 섹션 헤딩이 authoritative** (MODA25 = 6th).

### 5.3 HPCSYSPROS (SC)

| Year | 개최 | 일정/Host | Proceedings | 피어리뷰 | 편수 |
|---|---|---|---|---|---|
| 2020 | Yes | SC20 (virtual) | GitHub + Zenodo | Yes | **7** |
| 2021 | Yes | SC21, Nov 14 (virtual) | GitHub + Zenodo | Yes | **6** |
| 2022 | Yes | SC22, Nov 14 | GitHub + Zenodo | Yes | **5** |
| 2023 | Yes | SC23, Nov 12 | **ACM SC-W'23 (`10.1145/3624062`)** + Zenodo | Yes | **10** |
| 2024 | Yes | SC24, Nov 22 | **Zenodo only** (`10.5281/zenodo.157248xx`, `.1654xxxx`) — IEEE SC-W 2024 볼륨 아래에는 나타나지 않음(검증 범위 내) | Yes | **9** |
| 2025 | Yes | SC25, Nov 16 | GitHub + Zenodo | Yes | **9** |
| 2026 | 예고됨 | SC26 | — | — | `PARTIAL` |

URL: `sighpc-syspros.org/workshops/<year>/`, `github.com/HPCSYSPROS/Workshop<YY>`.

> **연구자에게 중요:** HPCSYSPROS는 생태계 전체에서 **실제 프로덕션 운영 문제의 최대 공급원**(2020–2025 46편)이면서 **아카이브 가시성은 최저**다(자가 아카이브 Zenodo, 컨퍼런스 시리즈로 색인되지 않음).

### 5.4 나머지 워크숍 전체 표

#### SC 계열

| Workshop | 상태 |
|---|---|
| **FTXS** | 2020 SC20(10th `INFERRED`, proceedings `UNVERIFIED`) · 2021 SC21 11th, IEEE(FTXS54580.2021), **5**편 · 2022 SC22 12th, IEEE(FTXS56515.2022), **5**편 · 2023 SC23 13th, ACM SC-W'23, **4 full + 3 short** · 2024 SC24 **14th**(front matter 확인), IEEE SC-W 2024, **4**편 · **2025 DID NOT RUN** · 2026 개명·재범위화 → AI Systems |
| **PMBS** | **2020–2026 매년 개최**(PMBS20…PMBS26). PMBS26 = **17th**. SC Workshops 볼륨(IEEE 2021/2022/2024; ACM 2023/2025). 일부는 *Elsevier Parallel Computing* 특집으로 확장(14th/15th). 연도별 편수 `UNVERIFIED`(통상 8–12) |
| **ProTools** | **2019–2026 매년**; SC26 = **8th**. SC-W 볼륨. 편수 `UNVERIFIED` |
| **HPCTESTS** | "International Workshop on HPC Testing and Evaluation of Systems, Tools, and Software". **2020–2022 존재하지 않음** · 2023 SC23 Nov 17 **1st**, **5**편, SC23 Workshops(ACM) · 2024 SC24 Nov 22 2nd, **5**편, SC24 Workshops(IEEE) · 2025 SC25 Nov 21 3rd, 편수 `UNVERIFIED`, ACM `10.1145/3731599` · 2026 SC26 4th `PARTIAL`. URL: `olcf.github.io/hpc-system-test-wg/hpctests/`. **OLCF 주도 HPC System Test Working Group — 학계가 아니라 운영자 커뮤니티가 운영** |
| **PDSW** | 매년 개최. IEEE 독립 볼륨 2020(5th, `10.1109/PDSW51947.2020`), 2021(6th), 2022(7th). **2023부터 통합 SC-W proceedings로 흡수**(독립 dblp 볼륨 없음) — 2023, 2024, PDSW'25@SC25, PDSW'26 = **11th**@SC26 |
| **HUST** (HPC User Support Tools) | **2014–2026 매년**; HUST-26 = **13th**. Proceedings: IEEE(2020, 2022), Zenodo(2021), ACM SC-W(2023, 2024, 2025). 연도별 논문 목록 미게시 → `UNVERIFIED` |
| **ISAV** | SC에서 2026까지 지속; **SC25/SC26에서 "In Situ AI, Analysis and Visualization"으로 개명**(기존 "In Situ Infrastructures for Enabling Extreme-Scale Analysis and Visualization"). 연도별 기록 `UNVERIFIED`(dblp venue 페이지 404) |
| **Sustainable Supercomputing** | SC 계열: **SC24**(예: "Towards Sustainable Post-Exascale Leadership Computing"), **SC25**(Nov 16), **SC26** 확인. ISC 계열: ISC 2024 LNCS 워크숍 볼륨에 수록. SC23 이전 `UNVERIFIED` |
| **Digital Twins for HPC** | **SC25 only** (SC25 44개 워크숍 목록에 포함). **SC26 50개 목록에는 없음** — 반복되지 않았다. 이전 연도 `UNVERIFIED` |
| **SuperCompCloud** | SC25(44개)·SC26(50개) 목록에서 **NOT FOUND**. 2025년 기준 SC에서 중단된 것으로 간주. 이전 연도 `UNVERIFIED` |
| **RESDIS** (RESource DISaggregation) | SC25 (5th), SC26 (6th) |
| **S-HPC** | SC25 4th, SC26 5th |
| **SC26 신설 (운영 관련)** | **ECHO** — "1st International Workshop on Edge-Cloud-HPC Operational Continuum" · **AgenticAI4HPC'26** (1st, Agentic AI for HPC) · **RISE 2026** (Rising Innovators in Sustainable Exacomputing) · **Sovereign AI Supercomputing Cloud** · **AI on HPC: Performance Engineering, Challenges and Opportunities** · **High Performance Fabrics for AI and HPC (HPF AI/HPC)** — SC26에서만 확인, 이전 연도 `NOT FOUND` |

#### HPDC 계열

| Workshop | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| **PERMAVOST** | — | **1st** (`10.1145/3452412`) | 2nd (`10.1145/3526063`) | 3rd (`10.1145/3588993`) | 4th | 5th (Jul 20, Notre Dame) | 6th (Jul 13, Cleveland) |
| **AI4Sys** ("AI for Systems") | — | — | — | **1st** `INFERRED` (번호에서) | 2nd (HPDC'24 Pisa) | **3rd** | **4th** |
| **SNTA** (Systems and Network Telemetry and Analytics) | Yes (Stockholm) | Yes (virtual) | Yes (Minneapolis) | Yes (Orlando) | Yes, **7th** (Pisa, 5편) | **DID NOT RUN** | **DID NOT RUN** |
| **FRAME** | — | — | — | — | Yes | 5th | — |
| **REX-IO** | — | — | — | — | — | — | 6th (복귀) |

- **AI4Sys의 accepted-paper 목록은 공개되지 않는다**(HotCRP 제출 사이트만 존재, "submissions closed"). 2023–2025 논문 제목·저자 `UNVERIFIED`. 공개 기록의 실질적 공백.
- **SNTA는 HPDC의 텔레메트리 워크숍이지만 네트워크/스트리밍 알고리즘 지향**이며 HPC 센터 운영 지향이 아니다(2024년: frugal quantile tracking, endpoint congestion management, eBPF gossip 등). **2024년 이후 소멸 = HPDC 유일의 텔레메트리 venue 상실.**

#### IPDPS 계열

| Workshop | 상태 |
|---|---|
| **JSSPP** (Springer LNCS, 매년) | 2020 23rd LNCS 12326 New Orleans · 2021 24th LNCS 12985 virtual · 2022 25th LNCS 13592 virtual · 2023 26th LNCS 14283 St. Petersburg FL · 2024 27th LNCS 14591 San Francisco (**10**편) · 2025 28th LNCS 16210 Milan (**17**편) · 2026 29th LNCS 16980 New Orleans (**13**편 예고). URL: `jsspp.org`. **W1 계열에서 운영 스케줄링 문제가 실제로 아카이브되는 유일한 venue** — 단 SC/IPDPS 본트랙이 아니라 LNCS로 |
| **ESSA** | 1st = 2020 … **6th = 2025**, **7th = 2026**(`INFERRED`). IEEE IPDPSW proceedings. 연도별 편수 `UNVERIFIED` |
| **iWAPT** | 2025, 2026 개최 확인(2026 = **21st**). 2020–2024 연속성 `UNVERIFIED`(번호는 2006년 시작과 연속) |
| **EESP** (Energy Efficiency with Sustainable Performance) | **1st: ISC 2025**(Jun 13; 8편 채택 / 36% 채택률; LNCS 978-3-032-07612-0에 6편 아카이브) · **2nd: ISC 2026**(Jun 26; 19편 중 11편 채택) · **3rd: SC 2026**(Nov 15, Chicago) `PARTIAL`. URL: `ayeshaafzal91.github.io/eesp/` |

### 5.5 워크숍 → 아카이브 승격 lineage (확인된 4건 + 1건)

| # | 워크숍 | → 아카이브 | 비고 |
|---|---|---|---|
| **L-1** | Molan, Borghesi, Beneventi, Guarrasi, Bartolini, *An Explainable Model for Fault Detection in HPC Systems*, **MODA21**, LNCS 12761 | ***RUAD: Unsupervised anomaly detection in HPC systems***, **FGCS 141 (2023)**, `10.1016/j.future.2022.12.001` | 동일 그룹·동일 시스템(CINECA Marconi100). 지도학습 → 라벨 의존 제거. **저널이지 SC/HPDC/IPDPS가 아니다** |
| **L-2** | Seyedkazemi Ardebili 외, *Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems*, **MODA22** | ***Multi-level anomaly prediction in Tier-0 datacenter***, **ACM Computing Frontiers 2022**, `10.1145/3528416.3530864` | detection → prediction. **CF는 중견 아카이브지 SC가 아니다** |
| **L-3** | Ozer, **Netti**, Tafani, Schulz, *Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning*, **MODA20** | **Netti 외, *A Conceptual Framework for HPC Operational Data Analytics*, IEEE CLUSTER 2021**; *Operational Data Analytics in practice*, **Parallel Computing 113 (2022)**; 기반으로 **DCDB Wintermute, HPDC 2020** | **이 분야 최고의 practice→framework→method→taxonomy 궤적**(Netti의 2022 TUM 박사논문으로 귀결). ⚠️ **Netti는 이후 이 분야를 떠났다**(2024–2026 산출물은 위성/비지상 컴퓨팅). **후계자가 없다** |
| **L-4** | (워크숍 기원 `UNVERIFIED`) | *Proctor*(**ISC 2021**, LNCS) → *E2EWatch*(**Euro-Par 2021**) → ***Prodigy*, SC'23 본회의**, `10.1145/3581784.3607076` | BU/Coskun 라인. **이 그룹이 지금 HPC-ODA 2026을 공동 의장한다**(Ayse Coskun) |
| **L-5** | 워크숍 선구자 **NOT FOUND** | **ExaDigiT, SC24**, `10.1109/SC41406.2024.00029` | ORNL 그룹의 워크숍 활동은 ODA BoF(비아카이브)와 HPCSYSPROS(Zenodo only). Woong Shin이 **MODA26에서 "The Past, Current, and Future of HPC ODA" 기조** — 즉 흐름이 아카이브-우선, 워크숍-커뮤니티로 **역방향** |

**명시적 부정 결과.**
- **PIKA(TU Dresden), LLview(JSC), XDMoD Application Kernels(Buffalo), Arbiter(Utah), EMOI(CSCS), CEEMS(CNRS), buildtest(NERSC), Ramble(Google), ORNL ODA dashboard** — 이 중 어느 것에 대해서도 SC/HPDC/IPDPS/Cluster/DSN 정규 논문을 **찾지 못했다**. Arbiter의 유일한 비워크숍 거처는 **PEARC**(practice 컨퍼런스)다.
- **HPCSYSPROS 2020–2025 중 조사된 논문에 추적 가능한 아카이브 후속이 있는 것은 없다. 46편, 승격 0건.**
- **HPCTESTS 2023–2025 중 아카이브 후속이 있는 것은 없다. 10편+, 0건.**

### 5.6 워크숍에서 매년 반복되지만 아카이브 논문이 전혀 없는 문제 (상위 10)

| # | 문제 | 반복 기간 | 아카이브 프레이밍(아무도 안 한 것) |
|---|---|---|---|
| **G1** | 지속적 acceptance testing과 exascale에서의 silent regression 탐지 | 2021–2026, 6년 연속 (FTXS21, HPCSYSPROS22/24, HPCTESTS23/24/25/26, MODA25/26) | *"조용히 저하된 노드 때문에 손실되는 프로덕션 용량 비율은 얼마이고, 특정 테스트 주기가 사주는 탐지 지연은 얼마인가?"* ORNL이 ground truth를 이미 공개했다 |
| **G2** | 사용자에게 비효율을 알려주면 무언가 바뀌는가 | 2023–2026 | 프로덕션에서 job-efficiency 리포팅이 사용자 자원 요청·낭비 node-hour·큐 압력을 바꾸는지의 통제된 before/after 연구. **재료가 TUD와 JSC에 이미 프로덕션으로 존재한다. 생태계 전체에서 가장 명백하게 출판 가능하면서 안 된 연구** |
| **G3** | 사이트 간 운영 텔레메트리 스키마와 그 검증 | 2019–2026, 매년 | metric ontology 정의 → 서로 다른 스택(LDMS/DCDB/Prometheus)의 ≥3개 센터에 구현 → **portable analytic이 유계 정확도 손실로 이전됨을 입증**. Netti CLUSTER'21이 유일한 선행연구이며 개념적이고 cross-site 검증이 없다 |
| **G4** | job failure의 측정 가능한 원인으로서의 configuration drift | 2020–2025, HPCSYSPROS 매년 | 프로덕션 클러스터에서 node-image/config 발산을 계측하고 job failure·성능 분산·티켓 볼륨과 상관. **아무도 정량화한 적이 없다. 어디에도 논문 0편** |
| **G5** | 공유 자원 저하를 실시간으로 원인 job에 귀속 | 2020–2026 | 운영자 확인 인시던트 대비 precision/recall을 갖춘 온라인 인과 귀속. 특성화는 아카이브됨(PDSW→SC); **온라인 귀속은 아님** |
| **G6** | HPC에서의 LLM 기반 운영 로그 분류·RCA | 2023→2026, 가속 중 | 비용·지연 예산 하에서 실제 HPC 인시던트 라벨 코퍼스 대비 LLM/agentic RCA 평가. **2027년에 누군가는 출판한다 — 창은 지금이다** |
| **G7** | HPC 운영 데이터의 안전한 공개(익명화/거버넌스) | 2024–2026 | privacy/utility 트레이드오프 연구. SC25 BoF 설문에서 **공개 ODA 데이터셋 가용성 1.6/5 — 설문 중 최저점**. 논문 0편 |
| **G8** | 고정 용량 하에서의 HPC 특화 carbon-aware 운영 | 2024–2026 | fair-share 제약 하 carbon-aware deferral의 프로덕션 규모 평가, **모델링이 아니라 실측** 탄소로 |
| **G9** | 로그인 노드/공유 서비스 남용 제어를 closed-loop control로 | 2023–2025 | Arbiter 3는 **L7/D5**(배포된 closed-loop 자동 집행)인데 **피어리뷰 아카이브 평가가 한 번도 없다**(false positive율, 사용자 행동 효과, 안정성/진동) |
| **G10** | 운영 정책 변경의 counterfactual 평가 (메타 문제) | 2023–2026 | 모든 L6/L7 결과가 시뮬레이션에서 멈추는 이유. **ExaDigiT(SC24)가 물리를 풀었다. 정책 평가 방법론은 아무도 안 했다** |

**SC25 ODA BoF 설문 (29명 응답) — 정량 근거로 인용 가능:** 사용자는 운영 데이터의 가치를 **4.3/5**로 평가하지만 자신의 활용 역량은 **2.9/5**로 평가한다. 청중 구성은 운영자 17, 연구자 11, **사용자 1명**. 공개 ODA 데이터셋 가용성 **1.6/5**.

### 5.7 워크숍 최상위 개별 논문 (선별)

| # | 논문 | Venue/DOI | 등급 | 왜 중요한가 |
|---|---|---|---|---|
| 1 | **An Operational Data Collecting and Monitoring Platform for Fugaku** — Terai, Yamamoto, Miura, Shoji (RIKEN R-CCS) | MODA21, `10.1007/978-3-030-90539-2_24` | L0–L1 / D4 / P3 | **>150,000 노드, 전체 메트릭 스윕 <20초**. A64FX **redundant core**를 수집에 사용. 10⁵ 노드 텔레메트리의 인용 가능한 규모 기준점 |
| 4 | **Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA** — Winkler, Knüpfer | MODA23, `10.1007/978-3-031-40843-4_22` | L2–L3 / **D4** / **P4** | **>5년 연속 프로덕션 모니터링**, 사용자·관리자 모두 사용. 문헌상 가장 성숙한 프로덕션 job-efficiency 탐지기. **아카이브 버전 없음 — 코퍼스에서 가장 강한 미승격 논문** |
| 3 | **Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems** — Seyedkazemi Ardebili 외 | MODA22, `10.1007/978-3-031-23220-6_18` | L2–L3 / D3 / P3 | **Marconi100의 실제 thermal emergency 사건에 대해 검증** — 주입된 이상이 아니라 실제 설비 사고에 대한 검증은 드물다. 의도적으로 ML이 아닌 operator-auditable 규칙 |
| 9 | **Supporting HPC Users with LLview** — Guimarães, Sankaran, Frings (JSC) | MODA25, `10.1007/978-3-032-07612-0_4` | L1–L2 / **D4** / P3 | JUWELS Cluster+Booster 프로덕션, 오픈소스, **role-based access**(user/support/admin 뷰). 누락된 평가(리포팅이 사용자 행동을 바꾸는가)가 그대로 출판 가능한 연구 |
| 10 | **A Unified I/O Monitoring Framework Using eBPF** — Paipuri (CNRS/IDRIS) | MODA25, `10.1007/978-3-032-07612-0_3` | L0–L1 / D4 / P3 | eBPF로 VFS 커널 함수 추적 → Prometheus. 프로덕션 Lustre에서 IOR 대비 검증. **"Darshan은 AI 워크로드를 못 본다"는 살아있는 미해결 문제** |
| 12 | **What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years** — Siegmann 외 (Stony Brook/SUNY Buffalo) | MODA25, `10.1007/978-3-032-07612-0_5` | L1 / D3 / **P4** | **4년+, 500명+ 사용자.** 코퍼스에서 유일한 다년 종단 운영 연구 |
| 13 | **Heterogeneous Syslog Analysis: There Is Hope** — Quan, Howell, Greenberg (LANL) | HPCSYSPROS23, `10.1145/3624062.3624128` / `10.5281/zenodo.10223395` | L2–L3 / D2–D3 / P3 | **LLM을 로그 분류기로 평가한 초기의 정직한 비교** — 더 설명 가능하지만 계산 비용이 크다. HPC LLM 운영 로그 분류의 유일한 데이터 포인트 |
| 15 | **Experiences Detecting Defective Hardware in Exascale Supercomputers** — Hagerty, Webb, Melesse Vergara, Ezell (ORNL) | HPCTESTS23, SC23 Workshops (article ID `UNVERIFIED`) | L2–L3 / D4 / P3 | exascale에서 silent defect 문제에 대한 결정적 실무자 진술 |
| 18 | **Dynamic Login Node Resource Control and Monitoring with Arbiter 3** — McKay, Forrest, Fischer (Univ. of Utah) | HPCSYSPROS24, `10.5281/zenodo.16541343` | **L7 / D5** / P3 | 코퍼스 전체에서 **진짜로 closed-loop이며 프로덕션 배포된 극소수 시스템 중 하나.** 평가가 출판된 적 없음 |
| 19 | **From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments** — George, Wang, Hanley, Ransom, Bent, Zimmer (ORNL/LANL) | FTXS24, IEEE SC-W 2024 (article ID `UNVERIFIED`) | L3–L5 / D2 / P3 | HPC 디스크 신뢰성은 2020년 이후 아카이브 논문이 없다 (GPU는 ICS'24로 갔다) |
| 11 | **Duration-Informed Workload Scheduler** — Loreti, Leone, Borghesi (UniBo) | MODA25, `10.1007/978-3-032-07612-0_1` | L4→L6 / D2 / P2 | M100 ExaData 트레이스, **평균 대기시간 ~11% 감소**. 시뮬레이션만 — 실제 배포하면 SC/IPDPS 논문이 된다 |
| 8 | **An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads** — Hunhold, Wesner (Univ. of Cologne) | MODA24, `10.1007/978-3-031-73716-9` pp.273–286 | L0 / D1 / P0 | **스케줄러 자체를 system under test로 취급한 유일한 논문** |
| 6 | **A Fast Simulator to Enable HPC Scheduling Strategy Comparisons** — Wilkinson, Jones, Richardson, Dykes, Haus (HPE/UCL) | MODA23, `10.1007/978-3-031-40843-4` pp.320–333 | L6 / D1 / P2 `UNVERIFIED` | "프로덕션을 깨지 않고 운영 정책 변경을 어떻게 평가하는가"라는 미해결 메타 문제를 직접 다룸 |

**주요 언급:** LASSi for ARCHER(MODA20, 다년 Lustre+스케줄러 조인) · Data Center Facility Monitoring with Physics Aware Approach(MODA22, NREL) · Log-Based Identification, Classification, and Behavior Prediction of HPC Applications(HPCSYSPROS20, ANL) · Advancing ODA Standardization Through an Open Source Dashboard(HPCSYSPROS24, ORNL, `10.5281/zenodo.15724831`) · ClusterLog(FTXS22, UNC Charlotte) · Statistical Framework for Two-Party Acceptance Testing(FTXS21) · Beyond the Hype: Uncovering the Real I/O Needs of LLMs(HPCSYSPROS24) · Run your HPC jobs in Eco-Mode(JSSPP24) · Pinpointing Idle-Power Regressions in Linux(EESP25).

---

## 6. CUG의 역할과 한계

### 6.1 CUG은 무엇인가 / 무엇이 아닌가

**CUG(Cray User Group)은 Cray/HPE EX 계열 시스템을 운영하는 센터들의 실무 커뮤니티 학회다.** ORNL, NERSC, LLNL, Sandia, LANL, CSCS, EPCC 등이 자기 시스템의 운영 실태를 수치와 함께 공개하는, 이 분야에서 **가장 밀도 높은 1차 운영 증거의 출처**다. 동시에 **아카이브 피어리뷰 venue가 아니다.**

### 6.2 ⚠️ 검증된 CFP 사실 — CUG "Paper"는 피어리뷰 아카이브 출판이 아니다

CUG 2026 CFP(`https://cug.org/cug-2026-call-for-papers/`)에서 확인된 내용:

- **제출 유형은 네 가지: Paper / Presentation / BoF / Tutorial.**
  - **Paper** = *"full-length abstracts presenting novel results"*, 최종 논문 제출 필요
  - **Presentation** = *"presentation-only… not requiring a final paper"*
- 심사에 대해:
  - 논문은 *"will be considered for publication in a ACM International Conference Proceedings Series"*
  - *"Papers submitted by the due date will be reviewed for the proceeding publication"*
  - *"publication in the proceeding may require an **additional round of reviews**."*

> **→ CUG "Paper"는 채택된 abstract에 작성된 논문이 딸린 것이며, 기본적으로 피어리뷰 아카이브 출판이 아니다.**
> 특정 CUG 2024/2025 논문이 실제로 ACM ICPS에 실렸는지 여부는 **UNKNOWN — 조사 세션에서 확인하지 못했다.**

### 6.3 CUG 커버리지 상태

| 연도 | 상태 |
|---|---|
| CUG 2020 | **PARTIAL.** proceedings는 존재(virtual, 세션 일자 2020년 11월)하나 `at_a_glance` fetch가 "New Special Paper Session" 블록만 반환. 목록 불완전 |
| CUG 2021–2025 | 확보 (개별 PDF 다수 확인). 단 일부 PDF는 **게시되지 않음**: CUG2021 HPE AIOps 논문, CUG2021 Sandia system/application monitoring 논문, CUG2022 Fallout, CUG2023 Slingshot Dashboard 튜토리얼, CUG2024 Swordfish 논문. `PDF NOT POSTED`이지 "존재하지 않음"이 아니다 |
| **CUG 2026** | **NOT FOUND / NOT ACCESSIBLE.** `https://cug.org/proceedings/cug2026_proceedings/` → **404**(2025 폴더가 최신, 타임스탬프 2026-02-23). 라이브 프로그램(`ssl.linklings.net/.../cug2026_program/`)은 robots.txt 차단. `cug.org/cug-2026-technical-program/`은 로지스틱스만. **CUG 2026에 대해 검증된 내용이 전무하다. 어떤 출처의 CUG 2026 주장이든 proceedings 게시 전까지는 미검증으로 취급할 것. 2027년 초 재확인 권장** |

### 6.4 CUG 증거가 뒷받침할 수 있는 것 / 없는 것 (E_cug_vendor.md §6 원문 승계)

#### CAN support — 뒷받침할 수 있다

1. **운영 문제의 존재와 만연.** ORNL이 39,437회 0건 검출 후 스크리닝 방법을 폐기했다는 사실, NERSC가 OST가 25–50% 느린 것을 발견했다는 사실, LLNL/Sandia가 벤더 telemetry API가 100K–1M msg/s에서 실패한다고 보고한 사실 — 이것들은 실제 프로덕션 문제의 신뢰할 만한 1차 증거다. **연구 질문을 *동기화*하는 데 사용하라.**
2. **아키텍처·구성의 ground truth.** 컴포넌트 이름, 데이터 흐름, retention 기본값, 샘플링 주기, API 동작. CUG2025 HPE 튜토리얼은 사실상 HPCM 1.13 모니터링 스택의 공개 명세다.
3. **시스템 설계용 order-of-magnitude 스케일 파라미터.** ORNL 1.3 TB/day, NERSC 2M log msg/s, 300M messages/day, 스위치당 64K counter, PM counter 10 Hz vs 텔레메트리 15초.
4. **다른 데서는 아무도 출판하지 않는 negative result.** *"Fluent Bit was unstable at high throughput"*, *"Graphite downsampling destroyed our long-term analysis"*, *"we do not recommend this algorithm in production"*, *"mTE did not produce significant results"*. 이례적으로 가치가 높고 아카이브 venue에는 거의 나타나지 않는다.
5. **아카이브 제안에 대한 배포 현실 점검.** 예: Indiana University가 오버헤드를 이유로 DCGM을 거부한 것은, ML-for-HPC 논문들의 흔한 가정에 대한 직접적 반증이다.

#### CANNOT support — 뒷받침할 수 없다

1. **어떤 method efficacy 주장도 불가.** CUG 논문은 precision/recall, baseline, ablation, 통계 검정을 거의 보고하지 않는다. Frontier 스크리닝 논문이 이 코퍼스의 최고 수준인데도 설계된 비교가 아니라 원시 개수만 보고한다.
2. **재현성 불가.** 데이터셋은 사실상 공개되지 않는다. 대부분의 CUG 텔레메트리 연구는 구조적으로 재현 불가능하다.
3. **피어리뷰 지위 불가.** CFP 문구가 명시적이다: 채택은 abstract 기반이며 ICPS 출판은 *"may require an additional round of reviews."* **CUG "Paper" 라벨은 SC/HPDC/IPDPS 채택과 동등하지 않다.** 개별 CUG 2024/2025 논문이 ACM ICPS에 도달했는지는 **UNVERIFIED**.
4. **벤더 성능 주장 불가.** 조사된 벤더 항목 11개 중 문서화된 알고리즘 *과* 정량 평가를 모두 갖춘 것은 **1개(CADDY)**뿐이며 그것도 단일 노드 테스트베드다. **피어리뷰 검증을 가진 것 0개. 운영자 관련 성과 지표(precision, recall, alert volume, MTTR delta)를 동반한 프로덕션 평가를 가진 것 0개.**
5. **사이트 간 일반화 불가.** CUG2023 모니터링 논문이 직접 말한다: 포맷 발산 때문에 *"there can't easily be a rule of thumb in one implementation that extends to the other."*
6. **완전성 불가.** 가장 많이 인용되는 아티팩트 몇 개가 아예 게시되지 않았다(§6.3). **"cug.org에서 못 찾았다"로부터 "연구되지 않았다"를 추론하지 말 것.**

### 6.5 실무 규칙

> **CUG은 *practice evidence*로 인용하라** — "ORNL 운영진이 X를 보고한다". **검증된 method 주장은 Crossref로 확인된 아카이브 논문에만 쓰라.** 둘이 어긋나면, 그 어긋남 자체가 논문이다.

### 6.6 CUG 코퍼스가 제공하는, SC 논문 형태의 질문 (§7 원문 순위)

1. **Silent hardware defect에 대한 screening-policy 최적화.** backfill 노드 스크리닝을 sequential design으로 형식화; 목적함수 = node-hour당 결함 발견 수, 검출률이 **1/14,618** 수준일 때. ORNL이 검증용 결과 데이터를 이미 공개했고, **negative result(폐기된 주간 스크린)까지 baseline으로 공개했다.** No close archival work.
2. **Detectability를 제약으로 하는 retention/downsampling 최적화.** HPCM의 1일/7일/7일 기본값을 이기는 것. EPCC의 Graphite regret과 CADDY의 1200× 압축이 양 끝점. **replay된 트레이스만으로 평가 가능.** No close archival work.
3. **Slingshot급 fabric에서 획득비용 하의 counter subset 선택.** 스위치당 64K counter, dump당 0.5초, 사이트들이 임의로 "roughly forty"를 고르고 있다. Monet(NSDI'20)에 부분적 조상.
4. **모니터링 control plane의 backpressure와 graceful degradation.** 실패는 문서화되어 있고(telemetry-api → Kafka rebalancing → boot 실패) 설계 원칙은 없다.
5. **다년 아카이브에 걸친 telemetry schema evolution.** 버전화된 metric semantics + 재처리 비용. **지금 사양을 정하는 시스템에 직접 실행 가능.**
6. **프로덕션 텔레메트리로 검증된 network digital twin** (ns ↔ 15초 간극). ORNL이 스스로 flag했다.
7. **명시적 불확실성을 동반한 cross-source attribution** (10 Hz PM counter vs ~1 Hz 파이프라인 vs Slurm accounting; ms 규모 clock skew). CSCS가 불일치 사례와 불신 진술을 제공했다.
8. **Liquid-cooling/CDU 텔레메트리 anomaly detection의 제대로 된 평가.** 방법은 아카이브적으로 성숙(AAAI'19, ISC'17, ISC'21). **벤더가 이 기능을 평가 없이 출하하고 있기 때문에** 엄밀한 평가 자체가 방어 가능한 기여다.

---

## 7. Publication type 표기 규칙

### 7.1 태그 정의

본 survey 전체가 사용하는 태깅 어휘. 모든 인용 항목에 **정확히 하나**의 publication type 태그를 붙인다.

| 태그 | 정의 | 판정 기준 | 대표 예 |
|---|---|---|---|
| `[SC-TECHNICAL-PAPER]` | SC 본회의 Technical Papers 트랙에 채택된 정규 논문 | **SC의 공식 트랙 라벨이 확인된 경우에만** 사용. §2.4의 한계 때문에 본 census에서 이 태그를 확정적으로 붙일 수 있는 항목은 사실상 없다 | (확정 사례 없음 — 아래 `[SC-MAIN, TRACK-UNKNOWN]` 참조) |
| `[STATE-OF-PRACTICE]` | SC의 State of the Practice 트랙 | 동일하게 트랙 라벨 확인 필요. 내용상 SotP로 보이는 경우 `(content = SotP, TRACK-UNKNOWN)`로 병기 | Frontier: Exploring Exascale (SC23) — 내용상 SotP, 트랙 미확인 |
| `[ARCHIVAL-PEER-REVIEWED]` | 정식 피어리뷰를 거쳐 IEEE/ACM/Springer에 아카이브된 컨퍼런스·저널 논문 | proceedings 볼륨 + DOI 확인 | DCDB Wintermute (HPDC'20); Proctor (ISC'21); ALBADross (Cluster'22 **본트랙**) |
| `[WORKSHOP-PEER-REVIEWED]` | 피어리뷰를 거친 워크숍 논문 | 워크숍 CFP + proceedings 확인. Zenodo 자가아카이브도 여기 | PIKA (MODA23); Arbiter 3 (HPCSYSPROS24); ClusterLog (FTXS22) |
| `[WORKSHOP-IN-PROCEEDINGS]` | **본 conference proceedings의 DOI 공간에 섞여 있는 워크숍 논문** | Cluster 2020–2022 전용 (§3.4) | PIKA `10.1109/cluster49012.2020.00061`; Global Experiences `.00071`; A Conceptual Framework for HPC ODA `10.1109/cluster48925.2021.00086` |
| `[POSTER]` | 포스터 트랙 | 페이지 수(통상 1–2p) + 트랙 확인 | Motivating Regime-Aware User-Profiles for Runtime Prediction (HPDC'26, pp.579–580, `10.1145/3806645.3820074`, 2p) |
| `[BOF]` | Birds-of-a-Feather 세션. **아카이브 없음, 피어리뷰 없음** | — | ODA BoF 2019–2025 전부; CUG Systems Monitoring WG BoF |
| `[PANEL]` | 패널. 비심사, 비아카이브 | — | (본 census에 개별 항목 없음) |
| `[TUTORIAL]` | 튜토리얼. 교육 자료로 심사되며 연구 기여가 아님 | — | Monitoring HPE Cray HPC systems (CUG2025 tut106) |
| `[PRACTITIONER]` | 운영 실무 커뮤니티 발표. abstract 심사 또는 무심사 | CUG `[PAPER]`/`[PRES]` 전부 | STREAM (CUG2023); Frontier defective hardware (CUG2024); EMOI (CUG2024) |
| `[VENDOR]` | 벤더 직원만으로 저술된 발표·문서·제품 문서 | 저자 전원이 벤더 소속 | CADDY (CUG2024); trellis (CUG2021); NVIDIA Mission Control 문서; DDN Insight 페이지 |
| `[TECH-REPORT]` | 기관 기술보고서, arXiv 프리프린트 | 피어리뷰 없음 | NREL/TP-2C00-79712 (2021); arXiv:2408.01552 (Frontier power management, 학술 venue `UNVERIFIED`); AIOpsLab arXiv:2501.06706 (컨퍼런스 venue `UNVERIFIED`) |

### 7.2 적용 규칙

1. **태그는 심사 형태에 대한 사실 진술이지 품질 판정이 아니다.** Arbiter 3는 `[WORKSHOP-PEER-REVIEWED]`이지만 코퍼스에서 몇 안 되는 L7/D5 시스템이다.
2. **`[SC-TECHNICAL-PAPER]`와 `[STATE-OF-PRACTICE]`는 트랙 라벨을 실제로 확인했을 때만 쓴다.** 확인하지 못했으면 `[SC-MAIN, TRACK-UNKNOWN]`으로 쓰고 내용 기반 추정을 괄호로 병기한다. 본 census의 SC 항목은 거의 전부 이 상태다(§2.4).
3. **Cluster 2020–2022 항목은 반드시 본트랙/`[WORKSHOP-IN-PROCEEDINGS]`를 구분한다.** DOI만 보고 "IEEE Cluster 논문"이라고 쓰면 틀린다.
4. **CUG 항목은 `[PRACTITIONER]`가 기본이며, 벤더 단독 저술이면 `[PRACTITIONER][VENDOR]`를 함께 붙인다.** CUG의 `[PAPER]` 라벨을 `[ARCHIVAL-PEER-REVIEWED]`로 승격하지 않는다 (§6.2).
5. **`[VENDOR]` 항목은 method efficacy 근거로 인용하지 않는다.** 엔지니어링 사실(수치, 아키텍처, 실패 모드)로만 인용한다. 유일한 예외적 인용 가치는 CADDY의 압축·지연 표다.
6. **검증 상태 표기는 publication type과 독립적으로 병기한다:** `UNVERIFIED`(확인 실패), `NOT FOUND`(찾았으나 없음), `PARTIAL`(일부만 확인), `NOT YET PUBLISHED`(아직 미발행), `ABSTRACT-UNREAD`(제목/서지만 확인), `PDF NOT POSTED`(존재하나 공개 미게시).
7. **저자 목록을 fetch하지 않은 항목은 인용 전 반드시 재확인한다.** B census의 대부분 항목이 이 상태이며, 기억으로 재구성하지 말 것. ACM HPDC의 일부 제목은 Crossref에서 절단되어 도착한다(**Apollo:**, **Holmes**, **Capri**, **TAC**, **SchedInspector**, **Heterogeneous Systems Resilience**) — **인쇄된 제목이 불완전하므로 ACM DL에서 재취득 필요**.

### 7.3 태깅 예시

```
[ARCHIVAL-PEER-REVIEWED] Aksar, Sencan, Schwaller, Aaziz, Leung, Brandt, Kulis, Coskun.
  "ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems."
  IEEE Cluster 2022 (main track), 10.1109/cluster51413.2022.00048, pp.369-380.

[WORKSHOP-IN-PROCEEDINGS] "PIKA: Center-Wide and Job-Aware Cluster Monitoring."
  HPCMASPA @ IEEE Cluster 2020, 10.1109/cluster49012.2020.00061.
  ※ Cluster 2020 proceedings에 포함되어 있으나 main track이 아님.

[SC-MAIN, TRACK-UNKNOWN] (content = State of the Practice)
  Atchley, Zimmer, Bernholdt, et al. "Frontier: Exploring Exascale." SC23.
  ※ SC per-paper 페이지가 모든 트랙에 "Technical Papers"를 표시하므로 트랙 확정 불가.

[PRACTITIONER] Adamson, Osborne, Lester, Palumbo (ORNL NCCS).
  "STREAM: A Scalable Federated HPC Telemetry Platform." CUG 2023.
  ※ CUG Paper 트랙 = abstract 심사. ACM ICPS 수록 여부 UNVERIFIED.

[PRACTITIONER][VENDOR] Mitra, Ragland, Zambrano, Mallick, Vollmer, Kelley, Mohan (HPE).
  "CADDY: Scalable Summarizations over Voluminous Telemetry Data." CUG 2024.
  ※ 벤더 아티팩트 중 유일하게 알고리즘 + 정량평가를 모두 보유. 단 단일 노드 테스트베드.

[BOF] "Operational Data Analytics: Mind the Gap." SC25 ODA BoF.
  ※ 아카이브 없음. 설문 수치(4.3/5, 2.9/5, 1.6/5)는 인용 가능한 1차 자료.
```

---

## 8. KISTI 입장에서의 venue 전략

### 8.1 사다리 — 무엇을 먼저, 왜

| 단계 | Venue | 시점 | 왜 여기인가 | 필요한 것 | 위험 |
|---|---|---|---|---|---|
| **0단계 (준비)** | 내부 / CUG `[PRACTITIONER]` | 즉시~ | 한강 텔레메트리 감사 결과를 정량화된 운영 사실로 정리. 인용 가능한 1차 근거를 확보. **단, 이것을 연구 실적으로 계상하지 말 것** | 한강 텔레메트리 인벤토리, 볼륨·주기·보존 수치 | CUG은 피어리뷰가 아니다(§6.2). CUG 2026 proceedings는 아직 접근 불가 |
| **1단계 (첫 진입)** | **HPC-ODA 2026 @ SC26** | **2026-08-12 마감 (날짜 `UNVERIFIED`, §5.1)** | **제1회 워크숍**. 8년치 커뮤니티 수요가 눌려 있고 확립된 canon이 없다. **8p full paper, IEEE Xplore 아카이브.** 그리고 결정적으로 — **PC를 LRZ/BU/ORNL/NERSC/HPE가 의장한다. 즉 나중에 SC 제출을 심사할 바로 그 사람들이다** | 한강 운영 데이터 + 정직한 연구 설계 하나 | 1st edition은 심사 기준이 예측 불가. 날짜 불일치 존재 |
| **1단계 대안** | **MODA @ ISC** (2026 이후 "Monitoring, Observability, and Operational Data Analytics") | 매년 6월 | **유일한 장기 피어리뷰 ODA venue.** Springer LNCS 아카이브. 채택 경쟁이 낮다(연 2–5편) | 동일 | **가시성이 낮다.** 2020–2025 통틀어 17편 — 인용 기반이 작다. 승격 lineage도 SC가 아니라 저널(FGCS, ACM CF)로 갔다(§5.5) |
| **1단계 보조** | **JSSPP @ IPDPS** | 매년 | 운영 스케줄링 문제가 실제로 LNCS에 아카이브되는 유일한 W1 venue. 2025년 17편, 2026년 13편으로 물량도 있다 | 스케줄러/큐 데이터 | **LNCS-archival이지만 low-visibility.** SC/IPDPS 본트랙 실적으로 인정되지 않는다 |
| **2단계 (아카이브 진입)** | **IEEE Cluster 본트랙** 또는 **ISC research track** | 1단계 후 1년 | Cluster는 "우리가 만들어 운영했다" 유형(Lassen, Cluster'21)과 사용자 대면 예측 서비스(queue-wait, Cluster'25)를 본트랙에서 받는다. ISC는 BU/Sandia anomaly 계보의 홈이다 | 프로덕션 데이터 + 방법론 + baseline 비교 | ⚠️ **Cluster 2023/2024 본트랙에는 이 주제 논문이 0편이었다**(§3.4). 2025년에 복귀했지만 안정적 채널로 가정하지 말 것. ⚠️ **ISC 연구논문 트랙의 2024–2026 상태가 UNVERIFIED**(§3.5) — 제출 전 Springer 직접 확인 필수 |
| **2단계 대안** | **IPDPS 본트랙** | 매년 | **텔레메트리 기반 workload characterization의 부상하는 중심**. 볼륨이 100–135편으로 가장 크고, 2024–2026에 이 주제가 집중되어 있다 | 동일 | ⚠️ **IPDPS'26 Cankur/Bhatele/NERSC 논문이 한강 GPU 전수조사와 가장 가깝다.** 반드시 차별화 |
| **2단계 (방법론 축이면)** | **HPDC 본트랙** | 매년 | ODA 프레임워크의 prestige outlet | 새로운 analytics 메커니즘 | HPDC 2025 본트랙은 이 주제가 거의 비어 있었다. 진입 장벽이 높다 |
| **3단계 (목표)** | **SC State of the Practice** | SC27 이후 | **novel research를 요구하지 않는다**(§2.2 원문). 한강/KISTI-6 운영 논문의 정식 통로. Frontier(SC23), Fugaku 인센티브(SC24), El Capitan noise(SC25)가 형식 선례 | 프로덕션 배포 + 정직한 운영 기록 + 정량 성과 | 트랙 라벨이 논문에서 보이지 않으므로(§2.4) 대외적으로는 "SC 논문"으로 동일하게 보인다 — 이것은 오히려 장점 |
| **3단계 (목표)** | **SC Technical Papers** | SC27~28 | 최종 목표 | 프로덕션 데이터 + 배포 + 일반화 가능한 방법 + Tier B 반증 통과 | §4.3의 축별 판정을 통과해야 한다 |

### 8.2 1단계를 HPC-ODA 2026으로 잡아야 하는 이유 (검증된 근거)

- **제1회 에디션이다.** `hpc-oda.org/workshop2026/`가 명시적으로 "1st International Workshop on HPC Operational Data Analytics"로 표기하며, "eight years of successful BoF sessions at SC and ISC"를 피어리뷰로 전환한다고 밝힌다.
- **8p full paper / 4p short / 1–2p lightning talk**, **SC26 Workshop Proceedings, IEEE Xplore 아카이브**.
- **조직위:** Michael Ott(LRZ), Ayse Coskun(BU), Jeff Hanson(HPE), Melissa Romanus(NERSC/LBNL), Woong Shin(ORNL), Tim Osborne(ORNL). **PC 30인.**
- **이것이 핵심이다:** Coskun은 Proctor(ISC'21) → ALBADross(Cluster'22) → **Prodigy(SC'23)** 라인의 주인이고, Woong Shin은 SC21 Summit power → SC24 ExaDigiT → **SC26 Best Paper nominee** 라인의 주인이다. **즉 이 워크숍의 PC는 KISTI의 향후 SC 제출을 실제로 심사할 확률이 매우 높은 사람들의 집합이다.** 8년치 눌린 수요 + canon 부재 + 이 PC 구성 = **이 커뮤니티에 진입하는 가장 저렴한 경로.**
- ⚠️ 날짜 불일치가 있다: `/events/`(Nov 16, CFP Jul 31) vs `/workshop2026/`(Nov 20, 마감 Aug 12). **어느 쪽이 맞는지 `UNVERIFIED` — 직접 확인 필요.**

### 8.3 MODA / JSSPP에 대한 정직한 평가

- **MODA는 LNCS-archival이지만 low-visibility다.** 2020–2025 아카이브 챕터 총 17편이 이 분야 피어리뷰 코퍼스의 전부다. 채택 경쟁은 낮지만 인용 기반이 작다.
- **MODA에서 나온 승격 사례는 SC가 아니라 저널로 갔다:** MODA21 → FGCS 141(2023); MODA22 → ACM Computing Frontiers 2022. SC로 직행한 lineage는 없다.
- **2026년 개명("Monitoring, Observability, and Operational Data Analytics")은 커뮤니티가 cloud-SRE 어휘를 채택하고 있다는 신호다.** 2027년에는 observability/tracing/SLO 프레이밍이 잘 받아들여질 것으로 예상된다.
- **JSSPP도 LNCS-archival이지만 low-visibility다.** 운영 스케줄링이 실제로 아카이브되는 유일한 워크숍이지만 SC/IPDPS 본트랙 실적과 동등하게 계상되지 않는다.

### 8.4 하지 말아야 할 것

| 하지 말 것 | 이유 |
|---|---|
| **FTXS를 운영 연구 대상으로 삼기** | SC25에 열리지 않았고 SC26에서 "AI Systems at Scale"로 재범위화되었다. 고전적 HPC resilience 레인이 닫혔다 |
| **ACSOS를 HPC 적용성의 근거로 인용** | 2020–2025 본트랙에 HPC 평가 논문 **0편**(§3.8). 개념 어휘 전용 |
| **CUG "Paper"를 피어리뷰 실적으로 계상** | CFP 문구가 명시적으로 abstract 심사이며 ICPS 출판은 추가 심사가 필요할 수 있다(§6.2) |
| **Cluster 2020–2022 워크숍 논문을 "Cluster 본트랙"으로 인용** | PIKA, Global Experiences, A Conceptual Framework for HPC ODA 등이 여기 해당(§3.4) |
| **"우리는 느린 노드를 탐지한다"로 SC 제출** | Tuncer TPDS'19이 7년 전에 이미 했고, SuperBench(ATC'24)와 NodeSentry(SC'25)가 있다. **탐지가 아니라 "간섭 vs 내재 귀속"만 열려 있다**(§4.3) |
| **"우리는 여러 텔레메트리 소스를 융합한다"를 기여로 제시** | "Too Many Cooks"(ISSRE'25 Best Paper Candidate)가 융합의 수익이 감소하거나 음수라고 실증했다. 어떤 fault class에 어떤 소스가 load-bearing인지 ablation으로 답해야 한다 |
| **"라벨이 적은 상황의 학습 기법"을 기여로 제시** | ISSRE에 6년치 두꺼운 벤치가 있다. incremental로 반려된다. **"HPC에서 라벨이란 무엇이며 우리 것은 얼마나 틀렸나"라는 measurement로 재프레이밍하라** |
| **LLM 에이전트를 단독 축으로 제시** | ENGINEERING_ONLY 판정. AIOpsLab이 평가 하네스를 공급하면서 기준이 올라갔다. (C)나 (F)의 메커니즘을 실어 나를 때만 성립 |

### 8.5 KISTI가 구조적으로 유리한 자리

`B`, `C`, `D`, `E` 네 조사가 독립적으로 같은 결론에 도달한 지점들:

1. **텔레메트리 비용 vs 다운스트림 품질의 joint optimization (축 C).** 7개 축 중 유일한 `STILL_OPEN`. **HPC 사이트만이 전체 텔레메트리 스택(LDMS, RAS, Slurm, Lustre/GPFS, Redfish)을 실제로 통제한다** — 클라우드 AIOps 논문은 플랫폼이 뱉어주는 것만 받는다. 산출물(실제 슈퍼컴퓨터의 측정된 cost/quality Pareto frontier)이 어떤 모델이 이기든 무관하게 오래 간다. **반드시 SuperBench의 Selector 대비 명시적으로 포지셔닝할 것.**
2. **Retention/downsampling을 detectability 제약 하의 최적화로.** HPCM 기본값(Kafka 1일 / OpenSearch 7일 / VictoriaMetrics 7일)이 이길 대상으로 공개되어 있고, EPCC의 Graphite regret과 CADDY의 1200× 압축이 양 끝점을 준다. **replay된 트레이스만으로 평가 가능** — 프로덕션 위험이 없다.
3. **Facility ↔ compute 결합.** 어떤 본트랙에도 thermal/cooling/facility 논문이 없다(§3.9). ExaDigiT(SC24)가 facility 축이 SC에서 보상받는다는 것을 증명했고, **자기 건물을 소유한 센터는 대학 그룹에 대해 구조적 우위를 가진다.**
4. **공개된 현대적 다층 HPC 텔레메트리 코퍼스.** 이 분야는 아직도 2007년 BGL/Thunderbird/Spirit 로그로 벤치마킹한다(Loghub 경유). RAS + 하드웨어 카운터 + interconnect + PFS + 스케줄러 + job outcome을 아우르고 검증된 라벨을 가진 한강급 코퍼스는 **10년간 인용되며 방법론 노후화에 면역이다.** 단, 안전한 공개 방법론 자체가 논문 0편인 미해결 문제다(G7; SC25 BoF 공개 데이터셋 가용성 **1.6/5**).
5. **Deployment depth.** 학계 HPC 운영지능 논문 중 D2를 넘는 것이 거의 없다. **국가 슈퍼컴에서 D3(shadow) 또는 D4(운영자 워크플로)에 도달하는 것 자체가 어떤 모델링 개선보다 강한 주장이다.**
6. **공동저술 구조.** SC census의 관찰: 이 공간은 매년 반복되는 소수 그룹이 소유하는 **작고 식별 가능한 커뮤니티**다(Tiwari/Northeastern, Brandt-Schwaller-Aaziz-Leung/Sandia, Shin-Wang-Karimi-Zimmer-Atchley-Khan/ORNL, Iyer/UIUC, Coskun/BU, Bhatele/UMD). **IPDPS'26 Cankur/Bhatele 논문은 센터(NERSC)가 학계 그룹과 공동저술해 센터 텔레메트리를 최상위 논문으로 만든 구조 — KISTI가 복제해야 할 협업 구조가 정확히 이것이다.**

### 8.6 두 편 계획 — SC가 실제로 작동하는 방식

SC census가 확인한 패턴: **"characterize → act" 아크가 실제로 보상받는다.**

- SC22 "Not All GPUs Are Created Equal"(변동성 측정) → SC24 "PAL"(그 변동성을 스케줄링에 반영)
- SC20 Titan GPU survival → SC25 Story of Two GPUs
- SC21 Summit power characterization → SC24 ExaDigiT digital twin

리뷰어는 **측정 논문을 먼저, 메커니즘 논문을 나중에** 받아들인다.

> **→ 한강에 대한 2편 계획(1년차: characterization, 2년차: mechanism)은 이 venue가 실제로 행동하는 방식과 일치한다.**

부수 관찰: **"Toward Sustainable HPC: …" 제목 프랜차이즈가 작동한다.** SC23(carbon footprint, NEU), SC24(Fugaku 인센티브, RIKEN+Sandia+NEU), SC25 계속(ThirstyFLOPS, Core Hours and Carbon Credits). **지속가능성은 그냥 두면 "practice일 뿐"으로 판정될 운영 논문의 신뢰할 만한 진입로가 되었다.**

---

## 9. 이 문서를 사용할 때의 필수 주의사항 (승계된 caveat 총괄)

| # | 주의 | 영향 범위 |
|---|---|---|
| 1 | **SC 트랙 라벨은 복원 불가.** 모든 SC 논문 페이지가 "Technical Papers Archive"를 표시한다 | §2, §3.1 — SC 항목 거의 전부 `TRACK-UNKNOWN` |
| 2 | **SC26 accepted list는 UNVERIFIED / UNAVAILABLE** (프로그램 사이트 401, ACM DL/IEEE Xplore 403). 확인된 in-scope 논문 1편 | §2.3 |
| 3 | **Cluster 2020–2022의 워크숍 혼입.** 본트랙/`[WORKSHOP-IN-PROCEEDINGS]` 구분 필수 | §3.4, §7.2 |
| 4 | **ISC 연구논문 proceedings 2024–2026은 UNVERIFIED.** "중단되었다"고 쓰지 말 것 | §3.5 |
| 5 | **ACSOS 2020–2025 본트랙에 HPC 평가 논문 0편** (검증된 부정 결과) | §3.8 |
| 6 | **DSN 2020/2021은 PARTIAL** (각 연도 dblp ToC 앞 ~10항목만 검증). 기관 네트워크에서 IEEE Xplore 보완 필요. 예상 누락 3–8편 | §3.6 |
| 7 | **Cluster 2026 / ACSOS 2026 / DSN 2026 / ISSRE 2026 = NOT YET PUBLISHED** | §3 전반 |
| 8 | **HPDC 2026 커버리지 PARTIAL** (~50 레코드만 열거) | §3.2 |
| 9 | **abstract를 읽지 못한 항목이 다수.** B census는 어떤 논문의 abstract도 읽지 못했다 — 평가 규모·프로덕션 배포 주장은 **PDF에서 확인해야 할 가설**로 취급 | §3.2–3.5 |
| 10 | **저자 목록 미fetch 항목 다수.** 기억으로 재구성 금지 | §3 전반 |
| 11 | **Crossref에서 절단된 ACM HPDC 제목:** Apollo:, Holmes, Capri, TAC, SchedInspector, Heterogeneous Systems Resilience | §3.2 |
| 12 | **CUG 2026 = NOT ACCESSIBLE** (404 + robots). 2027년 초 재확인 | §6.3 |
| 13 | **CUG PDF 미게시 5건:** CUG2021 HPE AIOps, CUG2021 Sandia system/application monitoring, CUG2022 Fallout, CUG2023 Slingshot Dashboard 튜토리얼, CUG2024 Swordfish. **"미게시"이지 "없음"이 아니다** | §6.3 |
| 14 | **ICS'24 Summit GPU 논문의 저자 순서가 출처 간 불일치** (`D_workshops.md` vs `H_centers.md`). 인용 전 원문 확인 | §4.2 |
| 15 | **관련연구 작성 전 반드시 확보해서 읽어야 할 미검증 항목:** **Mantis**(ICS 2026, `10.1145/3797905.3800527`, 403 차단), **WisIO**(ICS 2025, `10.1145/3721145.3725742`), HPC ODA Commons(PEARC'26, `10.1145/3785462.3815891`), K4-Serve(PEARC'26, `10.1145/3785462.3815821`). **어느 것이든 판정을 뒤집을 수 있다** | §4.2 |
| 16 | **ACM DL / IEEE Xplore 차단으로 UNVERIFIED인 항목:** Nezha(FSE'23), Sage(ASPLOS'21), Nenya(KDD'22), NVMe SSD Failures in the Field(ATC'23), Mint(ASPLOS'24), Cores that don't count(HotOS'21), Tiwari et al. GPU errors(HPCA'15), Borghesi et al.(AAAI/IAAI'19, TPDS'22), Schroeder & Gibson FAST'07 등 | §4.2 |
| 17 | **제목 정정 (전파할 것):** Gainaru et al. SC 2012 논문의 정확한 제목은 **"Fault prediction under the microscope: a closer look into HPC systems"** (`10.1109/SC.2012.57`). 널리 유통되는 "…a closed-loop approach" 변형은 **틀렸다** | 인용 위생 |
| 18 | **ICPE는 이 census에서 NOT COVERED.** Intel/VAST 등 벤더도 NOT COVERED (WebSearch 예산 소진) | §4.2, §6 |
| 19 | **AI4Sys accepted-paper 목록은 공개되지 않는다** (2023–2025 `UNVERIFIED`) | §5.4 |
| 20 | **HPC-ODA 2026 날짜 불일치 UNVERIFIED** (Nov 16/CFP Jul 31 vs Nov 20/마감 Aug 12) | §5.1, §8.2 |

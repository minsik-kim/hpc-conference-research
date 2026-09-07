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

# 02. 논문 전수조사 (PAPER CENSUS)
## HPC AIOps / Operational Intelligence → SC Regular Paper Research Landscape

**작성일:** 2026-09-06 · **대상:** KISTI HPC 연구자 (한강/KISTI-6 SC Technical Paper 준비)
**원자료:** `A_SC_main.md`(SC 본프로그램), `B_hpdc_ipdps_cluster_isc_acsos.md`, `C_dsn_issre_lineage.md`, `D_workshops.md`, `E_cug_vendor.md`, `F_axes_ABC.md`, `G_axes_DEFG.md`, `H_centers.md`
**정렬 원칙:** venue별이 아니라 **우선순위(Priority)별**. §1 MUST READ → §2 RELEVANT → §3 PERIPHERAL → §4 Workshop/CUG/practice → §5 공개 데이터셋 → §6 집계 → §7 검증 상태.

> **표기 규칙(전 문서 공통)**
> - 제목·저자·venue·DOI·URL은 **영문 원문 그대로** 유지한다. 번역하지 않는다.
> - 원자료가 `UNVERIFIED` / `PARTIAL` / `ABSTRACT-UNREAD` / `NOT FOUND` / `NOT YET PUBLISHED` / `PDF NOT POSTED` 로 표시한 항목은 **그 표시를 그대로 승계**한다.
> - 두 원자료가 같은 논문을 다르게 기술하면 **어느 한쪽을 임의로 채택하지 않고 불일치를 명시**한다 (`⚠불일치`).
> - 이 문서는 새로운 제목·저자·연도·venue·DOI·숫자를 **생성하지 않는다**.

---

## 0. 읽는 법 (taxonomy 요약표)

### 0.1 정본(canonical) 척도 — 이 문서가 기준으로 삼는 정의

| L (지능 단계) | 정의 |
|---|---|
| **L0** | Collection — 텔레메트리 수집·전송·저장 인프라 |
| **L1** | Visualization — 대시보드·리포트·가시화 |
| **L2** | Rule alert — 임계값/규칙 기반 경보 |
| **L3** | Statistical / anomaly detection — 통계·ML 이상탐지 |
| **L4** | Prediction — 장애/성능/전력 등 예측 |
| **L5** | Diagnosis / RCA — 원인 국소화·분류·근본원인 규명 |
| **L6** | Recommendation — 조치 후보 제시(의사결정 지원) |
| **L7** | Closed-loop remediation — 자동 조치 실행(폐루프) |

| D (배치 성숙도) | 정의 |
|---|---|
| **D0** | 개념/합성 데이터만 |
| **D1** | 프로토타입 / 테스트베드 |
| **D2** | 실운영 데이터 오프라인 분석 |
| **D3** | 온라인 / shadow 운전 |
| **D4** | 운영자 워크플로에 편입(operator-facing, 일상 사용) |
| **D5** | 실운영 폐루프 자동 조치 |

| P (기여 성격) | 정의 |
|---|---|
| **P0** | 순수 실무(pure practice) |
| **P1** | 유용한 엔지니어링(useful engineering) |
| **P2** | 실증적 특성화(empirical characterization) |
| **P3** | 실운영에 적용된 연구 방법(research method in production) |
| **P4** | 일반화 가능한 연구 기여(generalizable research contribution) |

| SC-relevance 태그 | 의미 |
|---|---|
| **SC-REGULAR-PRECEDENT** | SC 정규 논문의 직접적 선례. 반드시 인용·차별화 필요 |
| **SC-REGULAR-RELEVANT** | 관련성 높음. 관련연구에서 다뤄야 함 |
| **SC-REGULAR-POTENTIAL** | 잠재적 관련. 필요 시 인용 |
| **PRACTICE-ONLY** | State-of-the-Practice 성격. 연구 근거로 쓰면 안 됨 |
| **PERIPHERAL** | 주변부(클라우드 전용·시뮬레이션 전용·애플리케이션 레벨 등) |

### 0.2 ⚠ 필독 정직성 고지 — 원자료 간 척도 정의가 서로 다르다

**`F_axes_ABC.md`와 `G_axes_DEFG.md`의 두 조사 에이전트는 위 정본과 다른 L/D/P 정의를 각자 문서 서두에 명시하고 사용했다.** 추가로 `C_dsn_issre_lineage.md`와 `D_workshops.md`도 P 척도를 다르게 정의했다. 실제 차이는 다음과 같다.

| 원자료 | L 척도 | D 척도 | P 척도 |
|---|---|---|---|
| `A_SC_main.md` | 정본과 호환(저자 판단이라 명시) | 정본과 호환 | 정본과 호환 |
| `B_hpdc_ipdps_...md` | 정본과 호환(`[A]`=assessed 표시) | 정본과 호환 | 정본과 호환 |
| `C_dsn_issre_...md` | **정본과 동일** | **정본과 동일** | ❌ **portability scale**: P0=단일 시스템/단일 사이트 · P1=한 사이트 다중 시스템 · P2=multi-site 동일 벤더/세대 · P3=cross-vendor/cross-generation 입증 · P4=system-agnostic |
| `D_workshops.md` | 정본과 동일 | 정본과 동일 | ❌ **production-data maturity**: P0=synthetic · P1=single-node/testbed · P2=partial production trace · P3=full production system · P4=multi-system/multi-year production |
| `F_axes_ABC.md` | ❌ **telemetry layer breadth**: L0=없음/파생만 · L1=1개 계층 · L2=2개 · L3=3개 · L4=4개 · L5=5개+스케줄러 포함 · L6=5개+facility(전력/냉각) · L7=full stack(앱 계측+facility) | ≈ 유사하나 D3=online prototype, D4=daily operator tool, D5=institutionalized/multi-site/multi-year | ❌ **production-data realism**: P0=synthetic only · P1=testbed injection · P2=production system injection · P3=real production traces + proxy labels · P4=real production incidents + operator-confirmed ground truth |
| `G_axes_DEFG.md` | 정본과 동일이라 명시 | 정본과 동일이라 명시 | ❌ **production-evidence tier**: P0=sim · P1=testbed/injection · P2=단일 실운영, weeks · P3=단일 실운영, multi-month · P4=multi-system/multi-year production |
| `H_centers.md` | 정본과 동일 | 사용 안 함 (DEPLOYED / PROTOTYPE / ROADMAP 3단계 사용) | 사용 안 함 |

**이 문서의 처리 방식**
1. F/G(및 C/D의 P)에서 가져온 항목은 **방어 가능한 범위에서만 정본으로 재사various매핑**하고 항목에 `[L/D/P re-mapped]`를 붙인다.
2. 재매핑 근거가 불충분하면 그대로 `L/D/P: 원 출처 정의 상이 — 재확인 필요`라고 적는다. **추정으로 채우지 않는다.**
3. **척도를 조용히 섞지 않는다.** 예: F가 Prodigy를 "L3"라 한 것은 "3개 계층(CPU/mem/vmstat)"이라는 뜻이지 정본의 "이상탐지"가 아니다. 우연히 숫자가 같아도 의미가 다르므로 반드시 재도출한다.
4. F의 D3/D4/D5는 정본과 의미가 근접하므로 **D는 대체로 그대로 승계**하되, F가 D5를 "institutionalized/multi-site/multi-year"로 정의한 점(정본 D5=폐루프 자동조치)이 다르므로 **F발 D5는 반드시 재검토** 대상이다.

---

## 1. MUST READ

> KISTI SC 제출물이 **반드시 인용하고, 전문을 읽고, 차별화 논거를 준비해야 하는** 논문군. 총 **41편**(사용자 지정 필수목록 전부 포함). 원자료에서 메타데이터가 확인된 항목만 수록했으며, 확인 실패 항목은 §1.42에 별도 명시한다.

---

### 【A군】 SC 본프로그램 — 최우선 선례 (14편)

---

**M-01 · Live Forensics for HPC Systems: A Case Study on Distributed Storage Systems (Kaleidoscope)**
- **저자:** Jha, Cui, Banerjee, T. Xu, Enos, Showerman, Kalbarczyk, Iyer (UIUC / NCSA)
- **연도/venue:** 2020 | **SC20 main** | TRACK-UNKNOWN (A: "very likely Technical Paper"; SC 개별 논문 페이지는 모든 트랙을 "Technical Papers Archive"로 표기하므로 트랙 라벨 복원 불가)
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** ⚠**불일치** — A: `sc20.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap113.html` · F: `dl.acm 10.5555/3433701.3433787` · E(역참조): `10.1109/sc41405.2020.00069` · G: `par.nsf.gov/servlets/purl/10293041`. **인용 전 하나로 확정 필요.**
- **운영 문제:** 실패·혼잡/과부하의 사전 탐지 + 국소화 + 근본원인 규명을 1분 이내에
- **시스템/구성요소:** Storage (Lustre / Cray Sonexion) + network + telemetry infra
- **데이터 소스:** Blue Waters 실운영 텔레메트리 **2년 이상**
- **방법:** hierarchical domain-guided ML (PGM 기반 국소화 + LOF 기반 진단), near-real-time(<1 min)
- **평가 규모/기간:** Blue Waters(27k노드급). ⚠**불일치** — A: "843 real production issues" · G(D14): "6 MDS, 420 OSS, 17,280 HDDs; 2년 데이터, 3개월 live; 843 operator-resolved ground-truth issues". 세부는 G가 더 상세하고 A와 모순되지 않음.
- **real production data:** **Y** | **actual production deployment:** **Y** (Blue Waters 배치; G는 "3개월 live"로 한정)
- **L5 · D4 · P4** (A 기준, 정본과 호환) / F·G 원표기는 `[L/D/P re-mapped]`: F의 "L3"는 telemetry breadth 의미이므로 폐기, G의 D4/P4는 정본 D4/P4와 정합
- **주 기여:** 99.3% component localization, 95.8% root-cause identification, overhead <0.01%. SC 전 기간을 통틀어 "운영 문제 → 일반화 가능한 RCA 프레임워크"의 가장 정제된 사례
- **핵심 한계:** 단일 시스템; domain-guided 모델 계층이 **분산 스토리지 서브시스템에 한정**; 계층 구조를 전문가가 수작업 설계; GPU/fabric/scheduler/facility 신호 없음; "root cause"는 인과 증명이 아니라 최유력 지시 원인; 타 시스템 이식 입증 없음
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** SC에서 "production ground truth 843건"이라는 **평가 기준선(bar)을 세운 논문**이다. 어떤 RCA 제안도 이 규모의 운영자 확인 라벨과 비교당한다.

---

**M-02 · Prodigy: Toward Unsupervised Anomaly Detection in Production HPC Systems**
- **저자:** Aksar (BU/Sandia), Sencan (BU), Schwaller, Aaziz, Leung, Brandt (Sandia), Kulis, Egele, Coskun (BU)
- **연도/venue:** 2023 | **SC23 main** | TRACK-UNKNOWN (A: "clearly a Technical Paper")
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3581784.3607076` · `sc23.supercomputing.org/.../pap374.html`
- **운영 문제:** 라벨이 존재하지 않는 실운영 HPC에서의 성능 이상 탐지
- **시스템/구성요소:** telemetry infra + node/job level metrics
- **데이터 소스:** Sandia LDMS급 실운영 모니터링 텔레메트리
- **방법:** VAE on TSFRESH features + CoMTE counterfactual explanation; 806→156 metrics 축소; Chi-square top-2000 of 794 TSFRESH features
- **평가 규모/기간:** ⚠**불일치** — A: "Production HPC system; deployed, 88% detection accuracy in production; 0.95 F1 offline" · F(A1): "Eclipse 1,488 nodes + Volta 52; 806→156 metrics @1Hz; ~10 TB/day monitoring cluster; injected anomalies + 1 real Empire I/O case(88%)". F가 88%의 근거를 "1건의 실사례"로 기술 — **A의 '88% in production'보다 훨씬 약한 주장**. 원문 확인 필요.
- **real production data:** **Y** | **deployment:** **Y** (LDMS+DSOS+Grafana+Django 연동)
- **L3 (+L5 설명)** · **D4** · **P4** — F 원표기 `L3/D4/P2`의 L은 breadth 의미이므로 폐기, P2("production system injection")는 정본 P4(일반화 가능한 연구기여)와 **다른 축** → `[L/D/P re-mapped]`
- **주 기여:** "실운영에는 라벨이 없다"는 제약 자체를 연구 기여로 전환. 오프라인 0.95 F1 + 실운영 수치를 함께 보고
- **핵심 한계:** 이상(anomaly)이 대체로 **합성 주입**으로 검증됨; 실운영 정확도는 운영자 확인 사례에 한정; 단일 사이트; network·GPU·filesystem-server·scheduler 텔레메트리 없음; healthy training set 필요; cross-system 검증 없음
- **SC-relevance:** **SC-REGULAR-PRECEDENT** ← A는 이를 "KISTI SC-regular 제출의 단일 최근접 템플릿"으로 지목
- **왜 Must Read:** KISTI가 이상탐지를 제안하면 리뷰어가 첫 번째로 꺼내는 논문이다. **동시에 "탐지기를 또 제안하지 말라"는 근거이기도 하다**(F/G 공통 결론).

---

**M-03 · Effective Node-Level Anomaly Detection in HPC Systems via Coarse-Grained Clustering and Fine-Grained Model Sharing (NodeSentry)**
- **저자:** S. Xia, Y. Sun, X. Pan, Y. Yuan, S. Zhang (Nankai Univ.), S. Hu, L. Tao, Y. Li, J. Feng
- **연도/venue:** 2025 | **SC25 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3712285.3759794` · PDF: `nkcs.iops.ai/wp-content/uploads/2025/10/NodeSentry_to_SC25.pdf`
- **운영 문제:** 노드 수가 매우 크고 job이 계속 바뀌며 패턴이 이질적인 환경에서의 비지도 노드 이상탐지
- **시스템/구성요소:** compute nodes / telemetry metrics
- **데이터 소스:** ⚠**불일치** — A: "Two real-world HPC datasets" (시스템명 미기재) · F/G: **NG-Tianhe**; D1 = 1,294 nodes / 13,379 jobs / 3,014 metrics / 1주 / 106.85M points / anomaly 0.16%, D2 = 30 nodes / 8일 / 0.04%
- **방법:** HAC(coarse-grained job-segment clustering) + Transformer-MoE + WMSE; fine-grained model **sharing**; semantic aggregation + Pearson r≥0.99 pruning으로 **3,014 → 82 metrics**
- **평가 규모/기간:** 위 D1/D2 (1주 + 8일) — **SC 게재작 중 관측 기간이 가장 짧음**
- **real production data:** **Y** | **deployment:** ⚠**불일치** — A: "UNKNOWN" · F: "D3/D4 (Prometheus 15s + Slurm)" · G: "Deployed? No"
- **L3 · D2~D3 · P4** `[L/D/P re-mapped]` (F의 L4=4계층 breadth, G의 P2=단일 실운영 weeks는 각각 정본과 축이 다름)
- **주 기여:** F1 > 0.876, best baseline 대비 **+0.560 F1**, training overhead **−45.69%**; Prodigy/RUAD/ExaMon/BGMM 대비 우위; 코드 + HPC용 clustering-adjustment/anomaly-labeling 도구 공개
- **핵심 한계:** 단일 시스템; **1주 트레이스**; ChaosBlade 주입 기반 검증; 탐지만 수행(계층 국소화·원인·조치 없음); GPU 노드 없음; fabric/Lustre 서버 카운터 없음; labeling 도구의 존재가 반semi-manual ground truth를 시사
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** "비지도 HPC 이상탐지" 라인이 **2025년에도 SC 정규 트랙에서 살아있음**을 증명하는 최신 증거이자, KISTI가 이 라인에 진입할 때의 최근접 경쟁자다. 동시에 metric 축소(3,014→82)를 SC에서 최초로 대규모 제시했으므로 **텔레메트리 비용 축(axis C)의 최강 반론 논거**이기도 하다.

---

**M-04 · Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems**
- **저자:** Levitt, Barella, Zeltner, Musta, Cheney, Espinosa, Franza, **Gerofi** (Intel / Argonne)
- **연도/venue:** 2025 | **SC25 main** | TRACK-UNKNOWN (A: "reads SotP-or-Technical")
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3712285.3759883`
- **운영 문제:** MTBF가 떨어지면서 **MTTR이 가용성을 지배**; 수동 서비싱이 너무 느림
- **시스템/구성요소:** 전 시스템 — GPU, node, logs, telemetry infra, ops workflow
- **데이터 소스:** **Aurora 실운영 event history**(상관된 이벤트)
- **방법:** 이벤트 이력 중앙 메타DB + **fine-grained multi-strike repair policy** + 자동 복구 프레임워크; 장애 통계 기반 실시간 판단
- **평가 규모/기간:** **Aurora (10,624 nodes, 63,744 Intel Max GPUs)**
- **real production data:** **Y** | **deployment:** **Y — Aurora 실운영 중**
- **L7 · D5 · P3/P4**
- **주 기여:** **MTTR 최대 84× 단축**. **본 전수조사 전체에서 유일한 진성 L7/D5 논문**
- **핵심 한계:** 학습된 추론이라기보다 **정책 엔지니어링**; 단일 사이트; "84×"는 수동 baseline 대비
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** "SC는 **탐지만 하는 시스템이 아니라 실제로 조치하는 시스템**도 게재한다"는 유일한 증거. KISTI가 폐루프 자동조치를 주장하려면 이 논문이 기준선이다.

---

**M-05 · Story of Two GPUs: Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs**
- **저자:** S. Cui, Patke, Z. Chen, Ranjan, H. Nguyen, P. M. Cao, S. Jha, Bode, Bauer (UIUC/NCSA), Narayanaswami, Sow (IBM), Di Martino, Kalbarczyk, **R. K. Iyer** (UIUC)
- **연도/venue:** 2025 | **SC25 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3712285.3759821`
- **운영 문제:** 새 GPU 세대는 실제로 더 신뢰성이 좋아지는가
- **시스템/구성요소:** GPU (memory + hardware components), job failures
- **데이터 소스:** NCSA Delta/DeltaAI — **1,056 A100+H100 GPUs, 2.5년, 11.7 million GPU-hours의 오류 데이터**
- **방법:** failure-mode taxonomy, MTBE 분석, 대규모 확장 시 가용성 투영
- **평가 규모/기간:** NCSA Delta (>1,300 PF peak), 2.5년
- **real production data:** **Y** | **deployment:** **N** (분석 + 투영)
- **L3 · D2 · P4**
- **주 기여:** H100 메모리 MTBE가 A100 대비 **3.2× 악화**; 복구 메커니즘이 커진 메모리에 불충분; 대규모에서 GPU 장애 흡수에 **약 5% node overprovisioning 필요**
- **핵심 한계:** 단일 사이트, 혼합 세대 클러스터; 투영은 모델 기반
- **SC-relevance:** **SC-REGULAR-PRECEDENT** — SC20 Titan GPU 연구의 직계 후속
- **왜 Must Read:** 한강이 대규모 GPU 파티션의 오류 로그를 수년 보유한다면 **가장 직접적으로 모방 가능한 패턴**. "운영 데이터 자산 → 과학적 결론"의 최신 표준.

---

**M-06 · GPU Lifetimes on Titan Supercomputer: Survival Analysis and Reliability**
- **저자:** Ostrouchov, Maxwell, Ashraf, Engelmann, Shankar, Rogers (ORNL)
- **연도/venue:** 2020 | **SC20 main** | TRACK-UNKNOWN (A: "reads as a Technical Paper field study")
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/sc41405.2020.00045` (E §R1에서 Crossref 검증) · `sc20.supercomputing.org/.../pap537.html`
- **운영 문제:** 대규모에서 실제로 GPU를 죽이는 요인은 무엇이며, 냉각과 스케줄링이 이를 어떻게 조절하는가
- **시스템/구성요소:** GPU + cooling + scheduler
- **데이터 소스:** **18,688 Titan GPUs, 약 6 생산연도, 100,000 GPU-years 이상의 수명 데이터**
- **방법:** time-between-failures + **통계적 생존분석(survival analysis)**
- **평가 규모/기간:** Cray XK7 Titan, ~6년
- **real production data:** **Y** | **deployment:** N/A (분석)
- **L3** (통계적 특성화, 인과 귀속 측면에서 L5 경계) · **D2** · **P4**
- **주 기여:** GPU 신뢰성이 **냉각 구조상의 위치와 job placement에 매핑되는 방식으로 방열과 강하게 상관**; **데이터와 분석 코드 공개**
- **핵심 한계:** 회고적; 단일 GPU 세대(K20X); placement와 workload의 교락을 완전히 분리하지 못함
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** M-05와 한 계보로 읽어야 한다. **"기술통계 그래프가 아니라 제대로 된 통계(생존분석·MTBE)를 적용하고 데이터를 공개한다"**는 것이 SC가 보상하는 일반화 동작임을 보여준다.

---

**M-07 · Cost-Aware Prediction of Uncorrected DRAM Errors in the Field**
- **저자:** Boixaderas, Zivanovic, Moré, Bartolome, Vicente, Casas, Carpenter, Radojković, Ayguadé (BSC / UPC)
- **연도/venue:** 2020 | **SC20 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `sc20.supercomputing.org/.../pap241.html` (DOI 미기재 — 원자료가 페이지 URL만 확보)
- **운영 문제:** DRAM uncorrected error를 예측해 선제 완화를 촉발
- **시스템/구성요소:** CPU/memory (DRAM), error logs
- **데이터 소스:** **MareNostrum 3 error logs, 실운영 2년**
- **방법:** Random forest 분류기 + **비용-편익 평가 방법론**
- **평가 규모/기간:** MareNostrum 3 (3,056 nodes), 2년
- **real production data:** **Y** | **deployment:** **UNKNOWN** (완화는 모델링됐을 뿐 배치 입증 없음)
- **L4 · D2~D3 · P4**
- **주 기여:** 손실 컴퓨트 시간 최대 **57% 절감(≈21,000 node-hours/yr)**; **F1/precision이 운영 예측기의 올바른 목적함수가 아니라고 논증하고 비용모델로 대체**; 오픈소스
- **핵심 한계:** 단일 머신, 단일 DRAM 세대; 절감은 로그로부터 시뮬레이션된 값이며 실운영 측정치가 아님
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** KISTI가 예측을 제안한다면 **반드시 이 프레이밍을 채택해야 한다**. "우리 분류기가 좋다"를 "우리 운영이 싸진다"로 전환하는 유일한 SC 선례. (참고: B §8은 BSC 그룹의 SC 계열 선행 cost-aware UE 예측 논문의 존재를 `[A: verify before citing]`으로 표시했는데, **본 논문이 그 논문**으로 보인다 — A와 B의 교차 확인으로 해소됨.)

---

**M-08 · A Taxonomy of Error Sources in HPC I/O Machine Learning Models**
- **저자:** Isakov, Currier, del Rosario, Kinsy (ASU); Madireddy, Balaprakash, Carns, Ross (ANL); Lockwood (LBNL)
- **연도/venue:** 2022 | **SC22 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/SC41404.2022.00021` · `sc22.supercomputing.org/.../pap321.html`
- **운영 문제:** **배치된 I/O throughput ML 모델은 왜 실패하는가**
- **시스템/구성요소:** Storage / I/O + ML-for-ops 방법론
- **데이터 소스:** **두 개 주요 HPC 시스템의 multi-year 로그**
- **방법:** 실패 모드 taxonomy (poor application modeling / poor system modeling / inadequate dataset coverage / I/O contention / I/O noise) + 자기 모델의 오차를 모드에 귀속시키는 진단 도구
- **평가 규모/기간:** 2개 실운영 시스템, multi-year
- **real production data:** **Y** | **deployment:** **N/A** (메타 연구)
- **L3 (meta) · D2 · P4**
- **주 기여:** 희소한 **"부정적 결과 / 운영 ML의 인식론"** 논문. A는 이를 "운영 ML이 왜 전이되지 않는가"를 다루는 KISTI 논문에 **가장 유용한 단일 선례**로 지목
- **핵심 한계:** taxonomy가 정성적; 2개 시스템
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** 새 알고리즘 없이 **데이터와 정직성만으로** SC 정규 논문이 성립함을 보여주는 유일한 사례. 신규 진입 그룹에게 레버리지가 가장 크다.

---

**M-09 · A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale (ExaDigiT)**
- **저자:** Brewer, Maiterth, V. Kumar, Wojda, Bouknight, Hines, W. Shin, Greenwood, Grant, Williams, F. Wang (ORNL)
- **연도/venue:** 2024 | **SC24 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/SC41406.2024.00029` (E는 소문자 표기 `10.1109/sc41406.2024.00029`로 동일 DOI 검증)
- **운영 문제:** 액랭식 exascale 시스템의 전력/냉각/스케줄링 결합 거동 예측·최적화
- **시스템/구성요소:** Power + cooling + scheduler + facility
- **데이터 소스:** **Frontier 텔레메트리 6개월분 replay(V&V용)**
- **방법:** 3개 결합 모듈 — resource-allocator & power simulator / transient thermo-fluidic cooling model / AR 가시화
- **평가 규모/기간:** Frontier (9,408 nodes) + 중앙 에너지 플랜트, 6개월 replay
- **real production data:** **Y** | **deployment:** **Y** (오픈소스, ORNL 운영, what-if 연구에 사용)
- **L4 + L6 · D3~D4 · P4**
- **주 기여:** 액랭식 exascale 머신의 **최초 end-to-end 검증 디지털 트윈**; 실무자용 "lessons learned" 명시
- **핵심 한계:** 냉각 모델은 replay로 검증됐을 뿐 **폐루프 제어로 검증되지 않음**; workload 모델이 조악
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** facility↔IT 계층 통합 축의 최강 선례이며, **건물을 소유한 센터가 대학 그룹 대비 구조적 우위를 갖는 유일한 축**임을 입증한다. D §G10(운영 정책의 counterfactual 평가)의 물리 기반도 여기서 나온다.

---

**M-10 · SIREN: Software Identification and Recognition in HPC Systems**
- **저자:** Jakobsche, Robertsén, Jones, Haus (HPE), **Ciorba** (Univ. of Basel)
- **연도/venue:** 2025 | **SC25 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3712285.3759873`
- **운영 문제:** 무엇이 실행됐는지 신뢰성 있게 식별할 수 없으면 애플리케이션별 ODA 자체가 불가능
- **시스템/구성요소:** Telemetry infrastructure / job + process metadata
- **데이터 소스:** **LUMI에서의 opt-in 배치 캠페인**
- **방법:** process-level 메타데이터·환경 수집 + **실행파일의 fuzzy hash**(프라이버시·무결성 보존)
- **평가 규모/기간:** LUMI
- **real production data:** **Y** | **deployment:** **Y** (opt-in 캠페인)
- **L0~L2 · D3~D4 · P4**
- **주 기여:** "job name은 거짓말"이라는, 대부분의 ODA 연구를 조용히 무효화하는 문제를 해결; 반복 실행 인식 + 미지 바이너리의 유사도 식별
- **핵심 한계:** opt-in 커버리지 편향; fuzzy hash가 빌드 변형에 민감
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** **"텔레메트리 수집 인프라 자체가 SC 정규 기여로 인정된다"**는 최선의 증거. 단, 조건은 "타인의 분석을 무효화하는 문제를 푼다"는 것.

---

**M-11 · MCBound: An Online Framework to Characterize and Classify Memory/Compute-bound HPC Jobs**
- **저자:** Antici, Bartolini, Kiziltan, Babaoglu (Univ. Bologna), Kodama (RIKEN)
- **연도/venue:** 2024 | **SC24 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/SC41406.2024.00062`
- **운영 문제:** 사용자 입력 없이 **실행 전에** job의 boundedness를 분류
- **시스템/구성요소:** Scheduler + node counters
- **데이터 소스:** **Fugaku 2.2 million job runs**; 분류는 2024년 2월 job에 적용
- **방법:** 체계적 특성화로 이력에서 **라벨 데이터셋을 자동 생성**한 뒤 온라인 분류기 학습
- **평가 규모/기간:** Fugaku, 220만 job
- **real production data:** **Y** | **deployment:** **Y** (Fugaku용 구현, overhead 무시가능; 이식 가능한 Python 구현)
- **L4 · D3~D4 · P4**
- **주 기여:** F1-macro ≥ 0.89; **"과거 텔레메트리에서 스스로 라벨을 도출한다"** 패턴을 본 전수조사 최대 job 수 규모에서 실행
- **핵심 한계:** 사실상 이진적 taxonomy; 스케줄링 이득은 주장될 뿐 운영에서 입증되지 않음
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** 라벨 부재 문제(axis E)의 **가장 저렴하고 방어 가능한 우회로**를 SC에서 성공시킨 사례.

---

**M-12 · Not All GPUs Are Created Equal: Characterizing Variability in Large-Scale, Accelerator-Rich Systems**
- **저자:** Sinha, Guliani, Jain, Tran, Sinclair (UW-Madison / AMD Research), Venkataraman
- **연도/venue:** 2022 | **SC22 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `sc22.supercomputing.org/.../pap186.html` (DOI 미기재)
- **운영 문제:** 제조 변동과 전력관리 변동이 CPU처럼 GPU에도 영향을 주는가
- **시스템/구성요소:** GPU / power management
- **데이터 소스:** **4개 실운영 클러스터** — Summit(ORNL), Vortex(Sandia), Longhorn(TACC) 모두 V100; Corona(LLNL) MI60. **GPU의 90% 이상 샘플, 100,000 GPU-hours 이상 수집**
- **방법:** 컴포넌트 스트레스 마이크로벤치마크 스위트 + 클러스터 간 통계 비교
- **평가 규모/기간:** 4개 시스템, 멀티벤더
- **real production data:** **Y** (실운영 머신에서의 전용 실행) | **deployment:** **N**
- **L3 · D2 · P4**
- **주 기여:** 명목상 동일한 GPU 간 **평균 32%(최대 72%) 성능 편차** — variability-aware 스케줄링의 실증적 토대(SC24 PAL이 직접 인용)
- **핵심 한계:** 벤치마크 구동이지 실운영 workload 구동이 아님; 2개 GPU 세대
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** "**측정 논문(SC22) → 메커니즘 논문(SC24 PAL)**"이라는 2편 아크가 SC에서 실제로 작동함을 보여주는 표본. A는 이를 한강 2개년 계획(1년차 특성화, 2년차 메커니즘)의 근거로 제시.

---

**M-13 · An In-Depth Analysis of the Slingshot Interconnect**
- **저자:** De Sensi, Di Girolamo (ETH Zurich), McMahon, Roweth (HPE), Hoefler
- **연도/venue:** 2020 | **SC20 main** | TRACK-UNKNOWN
- **publication-type:** `[SC-MAIN-TRACK / ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** ⚠**다중 식별자** — A: `sc20.supercomputing.org/.../pap447.html`, ACM `10.5555/3433701.3433747`, IEEE Xplore doc 9355230 · E: `10.1109/sc41405.2020.00039` · G: arXiv `2008.08886`
- **운영 문제:** 신규 실운영 인터커넥트의 adaptive routing·congestion control 특성화
- **시스템/구성요소:** Network (Slingshot / Rosetta)
- **데이터 소스:** 실제 Slingshot 하드웨어에서의 마이크로벤치마크 + HPC/DC/AI 앱
- **방법:** 실증 측정 + congestion injection 실험
- **평가 규모/기간:** 실 Slingshot 시스템, 정확한 규모 UNKNOWN
- **real production data:** **PARTIAL** (실제 하드웨어·벤더 협업이나 운영 텔레메트리는 아님) | **deployment:** N/A
- **L0~L1 · D2 · P2** (G는 D1/P1로 표기 — `[L/D/P re-mapped]`, ⚠**불일치**)
- **주 기여:** Slingshot congestion 거동에 대한 최초의 독립 특성화. 이후 모든 Slingshot 연구의 기준점
- **핵심 한계:** 벤더 공저; workload-trace가 아닌 벤치마크 구동; 진단 방법 없음
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** 한강이 Slingshot 계열이라면 fabric 관련 모든 주장의 출발점. **동시에 A의 가장 큰 gap 발견 — "2020~2025 SC 본프로그램에 운영 카운터 기반 실운영 Slingshot/Dragonfly 혼잡 진단 논문이 전무하다"**는 사실의 기준선이 된다.

---

**M-14 · From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System**
- **저자:** Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin (**ORNL**)
- **연도/venue:** 2026 | **SC26** | **Best Paper Nominee** (2026-08-13 finalist 발표에서 확인)
- **publication-type:** `[SC-MAIN-TRACK / PENDING — 미개최]`
- **DOI/URL:** **DOI not yet minted.** SC26은 2026-11-15~20 개최 예정이며 **본 문서 작성일(2026-09-06) 기준 미개최·미출판**. 전체 accepted list는 `UNVERIFIED / UNAVAILABLE`(SC26 프로그램 사이트 401, ACM DL·IEEE Xplore 403)
- **운영 문제:** alert fatigue → failure cascade의 인과적 근본원인 규명
- **시스템/구성요소:** telemetry / logs / RCA
- **데이터 소스:** UNKNOWN (초록 미확보)
- **방법:** causal failure cascade discovery
- **평가 규모/기간:** UNKNOWN
- **real production data:** UNKNOWN | **deployment:** UNKNOWN
- **L5 · D-UNKNOWN · P4 (예상)** — **D/P는 논문 공개 전까지 확정 불가**
- **주 기여:** (미공개)
- **핵심 한계:** (미공개)
- **SC-relevance:** **SC-REGULAR-PRECEDENT (pending)**
- **왜 Must Read:** 저자 집합이 M-09(ExaDigiT), SC21 Summit power, SC24 Frontier network cost를 만든 **ORNL 운영 텔레메트리 그룹 그 자체**이며, 그 라인이 이제 **Best-Paper-nominated RCA 논문**을 냈다. KISTI가 RCA 축을 선택하면 이 논문이 2026-11 이후 즉시 최근접 선행연구가 된다. **SC26 개최 직후 최우선 확보 대상.**

---

### 【B군】 HPDC / IPDPS / Cluster / ISC — 아카이벌 선례 (11편)

---

**M-15 · DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems**
- **저자:** Alessio Netti, Micha Müller, Carla Guillen, Michael Ott, Daniele Tafani, Gence Ozer, Martin Schulz (LRZ + TUM) — F는 `author list UNVERIFIED` 표시, B는 Crossref로 확인
- **연도/venue:** 2020 | **HPDC 2020 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3369583.3392674`, pp.101–112 · arXiv `1910.06156`
- **운영 문제:** 센터 규모의 **온라인**, in-band+out-of-band 운영 데이터 분석 프레임워크 부재
- **시스템/구성요소:** whole-center (facility, node, job)
- **데이터 소스:** DCDB 연속 모니터링 스트림
- **방법:** streaming analytics plugin framework (hierarchical, in-band/out-of-band, job- and node-level models); pushers→MQTT→collect agents→Cassandra→Wintermute→Grafana
- **평가 규모/기간:** LRZ 실운영 시스템 (CooLMUC-3 148 nodes, SuperMUC-NG). B는 `[UNVERIFIED scale/duration]`; H는 상세 수치 확보 — query engine overhead **<0.5%**, 메모리 **<25MB**, per-core CPU load **peak 1.2%**, 1,000 synthetic sensor 스케일링 테스트
- **real production data:** **Y** | **deployment:** DCDB는 LRZ 센터 인프라 — B는 `[A] HPDC 세트 중 최강 배치 주장, PDF 확인 필요`
- **L0~L4 (수집→예측을 아우르는 프레임워크) · D4~D5 · P3**
- **주 기여:** 아카이벌 문헌에서 **HPC ODA의 레퍼런스 아키텍처**. Wintermute 케이스스터디 3종: (1) L4 random-forest 전력예측 250ms 간격, 평균 상대오차 **6.2%** (2) L3 per-core CPI/FLOPS/vectorization 특징추출 (3) L3 BGM 클러스터링, 시간 단위 실행
- **핵심 한계:** 프레임워크/엔지니어링 논문이며 일반화 가능한 *방법* 주장은 제한적; **분석 모델 자체는 cross-layer RCA를 제공하지 않음**. ⚠H의 교차확인: Suarez et al. 2025는 LRZ 포함 독일 전 사이트에 대해 *"none of the German sites in this study are using this in production at present"*(ML 기준)라고 명시 → **L3/L4는 프레임워크 내 구현·실증까지이며 ML 기반 운영 의사결정은 production으로 주장되지 않음**
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** ODA를 "인프라"가 아니라 "연구 기여"로 만든 유일한 성공 사례이자, KISTI 파이프라인 설계의 기준 아키텍처.

---

**M-16 · Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data**
- **저자:** Alessio Netti, Daniele Tafani, Michael Ott, Martin Schulz
- **연도/venue:** 2021 | **IPDPS 2021 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/ipdps49936.2021.00010`, pp.2–12
- **운영 문제:** 모니터링 데이터의 양/차원 — 신호를 잃지 않고 텔레메트리를 어떻게 줄일 것인가
- **시스템/구성요소:** center-wide monitoring
- **데이터 소스:** DCDB monitoring streams
- **방법:** correlation 기반 특징 집계/축소
- **평가 규모/기간:** LRZ / Marconi급 `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L0/L1 · D2~D4 · P4**
- **주 기여:** 이 venue군에서 **텔레메트리 축소 논문은 사실상 이것 하나**이며 경쟁자가 없다
- **핵심 한계:** 평가 규모/기간 미확인; 후속 연구가 5년간 없음(B §9.4)
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** 한강의 텔레메트리 볼륨 문제를 정면으로 다루는 유일한 아카이벌 선행연구. **동시에 F §C가 지적하듯 "다운스트림 품질 제약이 걸린 최적화"는 아니어서 gap이 남아 있다.**

---

**M-17 · ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems**
- **저자:** Burak Aksar, Efe Sencan, Benjamin Schwaller, Omar Aaziz, Vitus J. Leung, Jim Brandt, Brian Kulis, Ayse K. Coskun (BU + Sandia). ⚠F는 저자 목록에서 Egele를 제외 — 미세 불일치
- **연도/venue:** 2022 | **IEEE Cluster 2022 main track** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/cluster51413.2022.00048`, pp.369–380 · F: `osti.gov/servlets/purl/2004257`
- **운영 문제:** 실운영 텔레메트리에서 이상을 라벨링하는 비용이 병목
- **시스템/구성요소:** compute nodes, center-wide
- **데이터 소스:** Sandia LDMS 실운영 텔레메트리 (Eclipse/Voltrino급 `[A]`)
- **방법:** active learning으로 라벨링 비용 최소화
- **평가 규모/기간:** Eclipse `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** ⚠**불일치** — B: 미표기 · F: D2(오프라인)
- **L3/L5 · D2~D3 · P4**
- **주 기여:** **28× 적은 라벨**로 동등 F1. 라벨 부족이라는 운영 장애물 자체를 연구 기여로 전환
- **핵심 한계:** 라벨링 효율 문제이지 인과성 문제가 아님; 단일 사이트
- **SC-relevance:** **SC-REGULAR-PRECEDENT** (B는 ★★ "한강에 가장 직접 재사용 가능")
- **⚠ 후속 미확인:** **ALBADross 계열 확장인 "Runtime Performance Anomaly Diagnosis in Production HPC Systems Using Active Learning", IEEE TPDS 2024, `10.1109/TPDS.2024.3365462`는 원자료에서 403으로 본문 확보 실패(`UNVERIFIED`). §7 필독 목록 참조.**
- **왜 Must Read:** 라벨이 0인 상태에서 시작하는 센터가 취할 수 있는 가장 이식성 높은 아이디어.

---

**M-18 · Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems**
- **저자:** Burak Aksar, Yijia Zhang, Emre Ates, Benjamin Schwaller, Omar Aaziz, Vitus J. Leung, Jim Brandt, Manuel Egele, Ayse K. Coskun
- **연도/venue:** 2021 | **ISC High Performance 2021, research paper track (LNCS)** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1007/978-3-030-78713-4_11`, pp.195–214
- **운영 문제:** 라벨이 거의 없는 상태에서의 이상 **진단**(존재 여부가 아니라 어떤 이상인지)
- **시스템/구성요소:** compute nodes
- **데이터 소스:** Sandia 실운영 LDMS 텔레메트리
- **방법:** semi-supervised representation learning + classification
- **평가 규모/기간:** `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L3→L5 · D2~D3 · P4**
- **주 기여:** 탐지에서 **진단(장애 클래스 명명)**으로 이동. 라벨 희소성에서 살아남는 semi-supervised 정식화
- **핵심 한계:** 단일 사이트; 라벨 출처가 주입 기반일 가능성
- **SC-relevance:** **SC-REGULAR-PRECEDENT** (B ★★)
- **왜 Must Read:** BU↔Sandia 축의 계보(Proctor ISC'21 → ALBADross Cluster'22 → Prodigy SC'23 → Refine ISC'25)를 이해하면 **KISTI가 어느 지점에 끼어들 수 있는지**가 보인다.

---

**M-19 · Aarohi: Making Real-Time Node Failure Prediction Feasible**
- **저자:** Anwesha Das, Frank Mueller, Barry Rountree (NCSU + LLNL)
- **연도/venue:** 2020 | **IPDPS 2020 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/ipdps47924.2020.00115`, pp.1092–1101
- **운영 문제:** 장애 예측의 **지연시간** — 추론이 장애보다 빨라야 한다
- **시스템/구성요소:** node
- **데이터 소스:** system logs / RAS `[A]`
- **방법:** lead-time-aware online inference pipeline
- **평가 규모/기간:** 실운영 HPC 로그 코퍼스 `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L4 · D2~D3 · P4**
- **주 기여:** 장애 예측을 **정확도 문제가 아니라 지연시간 문제로 재정의** — 운영이 새 연구 축을 낳은 교과서적 사례
- **핵심 한계:** 로그 기반; 평가 상세 미확인
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **선행/후속:** Desh (HPDC 2018, `10.1145/3208040.3208051`) → Aarohi (IPDPS'20) → Systemic Assessment of Node Failures in HPC Production Platforms (IPDPS 2021, `10.1109/ipdps49936.2021.00035`)
- **왜 Must Read:** "운영자만 알아채는 제약을 연구 축으로 승격"하는 방식 자체가 KISTI의 논문 전략에 그대로 이식 가능하다.

---

**M-20 · Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field**
- **저자:** Isaac Boixaderas, Sergi Moré, Javier Bartolome, David Vicente, Petar Radojković, Paul M. Carpenter, Eduard Ayguadé (BSC + MareNostrum 운영진)
- **연도/venue:** 2024 | **HPDC 2024 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3625549.3658686`, pp.240–252
- **운영 문제:** 예측된 uncorrected DRAM error에 대해 **언제 조치할 것인가**(page offlining / node draining) — 가용성 대 손실작업의 트레이드오프
- **시스템/구성요소:** memory / node health
- **데이터 소스:** 실운영 슈퍼컴퓨터의 field CE+UE logs
- **방법:** 예측 출력 위의 RL 정책
- **평가 규모/기간:** MareNostrum급 field data `[scale/duration UNVERIFIED]`
- **real production data:** **Y** | **deployment:** 논문은 "in the field"로 프레이밍. B는 `[A]` 표시와 함께 **"정책이 실제로 운영자 워크플로를 구동하는지 확인 필요"**라고 명시
- **L4→L7 · D3~D5 · P3~P4** — **D5 주장은 `[A]`(assessed)이며 검증 안 됨**
- **주 기여:** 이 분야를 *예측*에서 ***불확실성 하의 행동***으로 이동. B는 이를 "운영 문제 → 일반화 가능 연구"의 **단일 최고 템플릿**으로 1위 지목
- **핵심 한계:** 단일 벤더/단일 메모리 세대
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★** (B §7 1위)
- **왜 Must Read:** M-07(SC20 cost-aware 예측)의 직계 후속. **운영진이 공저자 목록에 있다는 사실이 "in the field" 주장을 신뢰 가능하게 만든다** — KISTI가 그대로 복제해야 할 저자 구성.

---

**M-21 · AIIO: Using Artificial Intelligence for Job-Level and Automatic I/O Performance Bottleneck Diagnosis**
- **저자:** Bin Dong, Jean Luca Bez, Suren Byna (LBNL / OSU)
- **연도/venue:** 2023 | **HPDC 2023 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1145/3588195.3592986`, pp.155–167
- **운영 문제:** 전문가 해석 없이 job 단위 I/O 병목의 근본원인 진단
- **시스템/구성요소:** parallel I/O stack
- **데이터 소스:** Darshan / DXT job I/O profiles
- **방법:** 엔지니어링된 I/O 특징 위의 지도학습 분류기
- **평가 규모/기간:** NERSC급 Darshan 코퍼스 `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L5 (RCA) · D2~D3 · P4**
- **주 기여:** HPDC에서 가장 깨끗한 L5 사례. 센터가 **이미 갖고 있는 텔레메트리(Darshan)만으로** 구성되며 사용자 대면 서비스로 가는 경로가 명확
- **핵심 한계:** 라벨 출처(provenance) 및 센터 간 일반화 미검증
- **SC-relevance:** **SC-REGULAR-PRECEDENT**
- **왜 Must Read:** "추가 계측 없이 기존 데이터로 L5" — KISTI가 가장 낮은 비용으로 재현할 수 있는 형태.

---

**M-22 · IOAgent: Democratizing Trustworthy HPC I/O Performance Diagnosis Capability via LLMs**
- **저자:** Chris Egersdoerfer, Arnav Sareen, Jean Luca Bez, Suren Byna, Dongkuan DK Xu, Dong Dai
- **연도/venue:** 2025 | **IPDPS 2025 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/ipdps64566.2025.00036`, pp.322–334
- **운영 문제:** I/O 진단 전문성이 사용자 수에 비례해 확장되지 않음; LLM 출력은 신뢰 불가
- **시스템/구성요소:** I/O stack
- **데이터 소스:** Darshan/DXT + tool outputs
- **방법:** grounding/trust 메커니즘을 갖춘 LLM agent
- **평가 규모/기간:** `[UNVERIFIED]`
- **real production data:** UNKNOWN | **deployment:** UNKNOWN
- **L5/L6 · D2~D3 · P4**
- **주 기여:** 이 venue군 최초의 **trustworthiness-aware** LLM-agent 운영 논문
- **핵심 한계:** 평가 규모 미확인
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★** — B가 "the live frontier"로 지목
- **계보:** HPDC'23 short(ChatGPT for PFS logs, `10.1145/3588195.3595943`) → IPDPS'25 IOAgent → IPDPS'26 KORAL(`10.1109/ipdps65963.2026.00085`). **2년 만의 short→full 승격**
- **왜 Must Read:** LLM 축(axis G)에서 SC 정규급으로 인정받은 유일한 형태 — "LLM을 쓴다"가 아니라 **"신뢰성 메커니즘을 시스템 기여로 제시한다"**.

---

**M-23 · Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining**
- **저자:** Baolin Li (Northeastern), Siddharth Samsi, Vijay Gadepally (MIT-LL), Devesh Tiwari (Northeastern)
- **연도/venue:** 2024 | **IPDPS 2024 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/ipdps57955.2024.00037`, pp.337–349
- **운영 문제:** 운영자는 블랙박스 모델로 행동할 수 없다 — GPU 클러스터 텔레메트리에 대한 **해석 가능한 규칙**이 필요
- **시스템/구성요소:** GPU cluster (MIT SuperCloud급)
- **데이터 소스:** 실운영 GPU 모니터링 시계열
- **방법:** association rule mining
- **평가 규모/기간:** 실운영 GPU 클러스터 `[scale/duration UNVERIFIED]`
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L2/L3/L5 · D2~D4 · P3~P4**
- **주 기여:** **operator consumability를 명시적 최적화 대상으로 삼음** — 거의 아무도 넘지 않는 D3→D4 다리
- **핵심 한계:** 평가 규모 미확인
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★** — B가 "한강 GPU 텔레메트리 논문의 최근접 공개 유사물"로 지목
- **왜 Must Read:** F1이 아니라 **운영자 행동가능성**을 최적화한 유일한 사례. KISTI가 D4를 주장하려면 이 형식을 따라야 한다.

---

**M-24 · Characterizing Production GPU Workloads using System-wide Telemetry Data**
- **저자:** Onur Cankur, Brian Austin, Dhruva Kulkarni, Abhinav Bhatele (UMD + NERSC)
- **연도/venue:** 2026 | **IPDPS 2026 main** | `[ARCHIVAL-PEER-REVIEWED]` (Crossref 검증, 게재 완료)
- **DOI/URL:** `10.1109/ipdps65963.2026.00078`, pp.899–912
- **운영 문제:** 상시 시스템 텔레메트리만으로 볼 때 센터 전체에서 GPU job은 실제로 무엇을 하는가
- **시스템/구성요소:** GPU nodes, center-wide
- **데이터 소스:** system-wide GPU telemetry — NERSC Perlmutter급으로 추정 `[system identity A — confirm]`
- **방법:** 대규모 실증 특성화
- **평가 규모/기간:** `[UNVERIFIED]`
- **real production data:** **Y** | **deployment:** N/A
- **L2 · D2 · P2~P3**
- **주 기여:** 센터 전체 GPU workload의 텔레메트리 기반 특성화
- **핵심 한계:** 기술적(descriptive); 예측/진단 모델 없음
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★★**
- **왜 Must Read:** **한강 GPU 텔레메트리 전수조사와 가장 가까운 공개 논문.** KISTI가 쓰는 어떤 것도 이 논문과 차별화되어야 한다. 또한 저자 구성(센터가 학계 그룹과 공저해 센터 텔레메트리를 최상위 논문으로 전환)이 **KISTI가 복제해야 할 협업 구조**라고 B가 명시.

---

**M-25 · The Case of the Elusive Application Performance on Production GPU Supercomputers**
- **저자:** Cunyang Wei, Keshav Pradeep, Abhinav Bhatele (UMD). ⚠F는 저자를 "Wei, Pradeep, Bhatele"로 동일 기재
- **연도/venue:** 2026 | **IPDPS 2026 main** | `[ARCHIVAL-PEER-REVIEWED]` (F는 `UNVERIFIED venue`로 표시했으나 B가 Crossref로 확정)
- **DOI/URL:** `10.1109/ipdps65963.2026.00079`, pp.913–927 · PDF `cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf`
- **운영 문제:** GPU 플래그십에서의 run-to-run 성능 변동
- **시스템/구성요소:** network counters + app profiles + scheduler logs + GPU
- **데이터 소스:** ⚠**세부 불일치 없음, 상호보완** — F: **Perlmutter + Frontier, 761 runs, ~8,100 node-hours, ~10 TB/system, 4 apps** · G: **Perlmutter(1,792 GPU nodes) + Frontier(9,408 nodes), 4개월(2024–25), 761 runs / 8,118 node-hours**
- **방법:** 반복 통제 실행 + network HW counters + XGBoost 귀속
- **평가 규모/기간:** 2개 시스템, 4개월
- **real production data:** **Y** | **deployment:** **N** (연구)
- **L2/L5 · D2 · P4** `[L/D/P re-mapped]` (F의 L5=5계층 breadth 의미)
- **주 기여:** **Frontier 2.6× / Perlmutter 1.4× 변동**; 원인을 compute가 아니라 **network congestion과 "top users"**로 귀속
- **핵심 한계:** 실운영 job이 아닌 **통제 벤치마크 실행**; 저자들이 스스로 밝힌 블로커 — **Rosetta switch counters 접근 불가**; 상관이지 인과 아님; 운영 조치 없음
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★★**
- **왜 Must Read:** G의 결론 — **"GPU 성능 저하가 주원인이라는 프레이밍은 이미 측정되어 반증됐다"**. KISTI가 GPU 열화 중심으로 논문을 짜면 이 논문에 부딪힌다. 반대로 **KISTI가 Slingshot per-port 카운터를 확보할 수 있다면 그것 자체가 최강 경쟁그룹 대비 차별점**(F §A.7).

---

**M-26 · Drill: Log-based Anomaly Detection for Large-scale Storage Systems Using Source Code Analysis**
- **저자:** Di Zhang, Chris Egersdoerfer, Tabassom Mahmud, Mai Zheng, Dong Dai (UNC Charlotte + Iowa State)
- **연도/venue:** 2023 | **IPDPS 2023 main** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** `10.1109/ipdps54959.2023.00028`, pp.189–199
- **운영 문제:** 라벨 없이, 로그를 발생시키는 **소스코드를 의미론적 사전정보로** 사용하는 로그 이상탐지
- **시스템/구성요소:** parallel file system (Lustre급)
- **데이터 소스:** PFS logs + source
- **방법:** static source analysis → log-template semantics → anomaly detection
- **평가 규모/기간:** `[UNVERIFIED]`
- **real production data:** UNKNOWN | **deployment:** UNKNOWN
- **L3 · D1~D2 · P4**
- **주 기여:** 이 시기 로그 이상탐지 아이디어 중 **방법론적으로 가장 독창적** — 라벨 데이터 문제를 우회
- **핵심 한계:** 평가 데이터/규모 미확인
- **SC-relevance:** **SC-REGULAR-PRECEDENT ★**
- **왜 Must Read:** A의 중대한 발견 — **SC 본프로그램에는 2020~2025 로그 분석 논문이 사실상 없다**. 로그 축을 택하려면 이 논문이 아카이벌 기준선이고, 동시에 "SC 리뷰어는 로그 마이닝을 시스템 기여로 보지 않을 수 있다"는 A의 경고를 함께 읽어야 한다.

---

### 【C군】 DSN / ISSRE / OSDI / ATC / FAST / EuroSys / FSE — 방법론 falsifier (11편)

> 이 군의 논문들은 **인용용 지지자료가 아니라 "이미 해결됐다"는 리뷰어 반론의 근거**다. 반드시 선제 대응해야 한다.

---

**M-27 · Time Machine: Generative Real-Time Model For Failure (and Lead Time) Prediction in HPC Systems**
- **저자:** Khalid Ayed Alharthi, Arshad Jhumka, Sheng Di, Lin Gui, Franck Cappello, Simon McIntosh-Smith
- **연도/venue:** 2023 | **DSN 2023, research track (session RT-14 "Potpourri")** | `[ARCHIVAL-PEER-REVIEWED]` (DSN 2023 공식 프로그램으로 ✅검증)
- **DOI/URL:** 원자료에 DOI 미기재 — 프로그램 페이지 기반 검증
- **운영 문제:** RAS 로그로부터 노드/시스템 장애 **및 lead time** 예측
- **시스템/구성요소:** whole-system (node-level RAS)
- **데이터 소스:** HPC RAS logs (Blue Waters / Mira급 공개 로그 코퍼스)
- **방법:** 로그 이벤트 스트림 위 생성형 시퀀스 모델 → next-event + time-to-failure
- **평가 규모/기간:** multi-year 공개 HPC 로그 데이터셋
- **real production data:** **Y** | **deployment:** **N**
- **L4 · D2 · P?** — **P: 원 출처 정의 상이(C는 portability scale, 원표기 P1) — 재확인 필요**
- **주 기여:** 장애와 **lead time의 결합 예측** — lead time이야말로 선제 조치를 가능케 하는 요소
- **핵심 한계:** 오프라인, 로그 전용, cross-system 전이 없음, 조치 루프 없음
- **SC-relevance:** **SC-REGULAR-RELEVANT**(HPC 장애예측 주장 시 필수 인용)
- **왜 Must Read:** C가 "HPC 장애 예측 SC 제출물의 DSN측 최근접 선행연구"로 지목. **반드시 인용하고 차별화해야 한다.**

---

**M-28 · ClusterRCA: An End-to-End Approach for Network Fault Localization and Classification for HPC System**
- **저자:** Yongqian Sun, Xijie Pan, Xiao Xiong, Lei Tao, Jiaju Wang, Shenglin Zhang, Yuan Yuan, Yuqi Li, Kunlin Jian
- **연도/venue:** 2025 | **ISSRE 2025, research track (RS8)** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** 원자료에 DOI 미기재
- **운영 문제:** HPC 클러스터 네트워크 장애의 **국소화 + 분류**
- **시스템/구성요소:** interconnect
- **데이터 소스:** 실운영 HPC 클러스터 네트워크 텔레메트리 + fault records
- **방법:** end-to-end 학습 기반 국소화 + fault-type 분류
- **평가 규모/기간:** UNKNOWN
- **real production data:** **Y** | **deployment:** UNKNOWN
- **L3+L5 · D2 · P?** — **P: 원 출처 정의 상이(C portability, 원표기 P0/P1) — 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT**
- **왜 Must Read:** **"HPC 인터커넥트 RCA" 주장에 대한 최근접 선행연구.** 네트워크 계층에 한해 axis A/D의 신규성을 강하게 제약한다. (저자군은 M-03 NodeSentry와 동일한 Nankai/NKCS 계열 — 이 그룹이 HPC 운영 AI를 SC/ISSRE 양쪽에서 밀고 있다는 점에 주의.)

---

**M-29 · Too Many Cooks: Assessing the Need for Multi-Source Data in Microservice Failure Diagnosis**
- **저자:** Shenglin Zhang, Xiaoyu Feng, Runzhou Wang, Minghua Ma, Wenwei Gu, Yongqian Sun, Zedong Jia, Jinrui Sun, Dan Pei
- **연도/venue:** 2025 | **ISSRE 2025**, **Best Research Paper Candidate** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** 원자료에 DOI 미기재
- **운영 문제:** logs + metrics + traces 융합이 실제로 진단을 개선하는가, 아니면 한 modality로 충분한가
- **핵심 결과:** **multi-source 융합의 수확 체감 또는 역효과**
- **L5 · D2 · P?** — **P: 원 출처 정의 상이(C portability, 원표기 P2) — 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT (NOVELTY HAZARD)**
- **왜 Must Read:** ⚠ **이 논문은 지지 인용이 아니라 위험이다.** "CPU/GPU/network/storage/scheduler 텔레메트리를 융합하는 것이 우리의 기여다"라고 주장하는 순간 이 논문이 반박 무기가 된다. C의 처방: **어떤 fault class에 어떤 소스가 load-bearing한지 ablation으로 선제 답변할 것.**

---

**M-30 · Predictive and Adaptive Failure Mitigation to Avert Production Cloud VM Interruptions (Narya)**
- **저자:** Sebastien Levy, Randolph Yao, Youjiang Wu, Yingnong Dang, Zheng Mu, Tarun Ramani, Naga Govindaraju, Xukun Li, Gil Lapid Shafriri, Murali Chintalapati (Microsoft Azure); Peng Huang (JHU); Pu Zhao, Qingwei Lin (MSR)
- **연도/venue:** 2020 | **OSDI 2020**, pp.1155–1170 | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** `usenix.org/conference/osdi20/presentation/levy`
- **운영 문제:** 예측된 호스트 장애에 조치를 취해 VM 중단을 회피
- **데이터 소스:** Azure multi-layer host signals
- **방법:** 예측 + **온라인 실험 / bandit-RL로 완화 조치 선택**
- **평가 규모/기간:** **실운영 15개월, VM 중단 26% 감소**
- **real production data:** **Y** | **deployment:** **Y (D5)**
- **L4+L6+L7 · D5 · P?** — **P: 원 출처 정의 상이(C portability P1, G production-evidence P4) — 재확인 필요.** 정본 기준으로는 P3~P4로 재매핑 가능하나 두 출처가 상반된 값을 주므로 확정하지 않음
- **SC-relevance:** **SC-REGULAR-RELEVANT (강한 falsifier)**
- **왜 Must Read:** **폐루프 자동 완화(axis F)의 최강 falsifier.** KISTI가 무엇을 제안하든 "왜 이것이 액션 세트만 바꾼 Narya가 아닌가?"라는 질문을 받는다. G의 방어 논거: 클라우드 액션은 싸고 되돌릴 수 있으나 **HPC 액션은 그렇지 않다**(노드 drain은 job을 죽이고, 4,000노드 job의 롤백은 존재하지 않는다).

---

**M-31 · SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation**
- **저자:** Yifan Xiong, Yuting Jiang, Ziyue Yang, Lei Qu, Peng Cheng, Yongqiang Xiong, Lidong Zhou (MSR) + 13 Microsoft 공저자 (F는 전체 목록 기재: Xiong, Jiang, Yang, Qu, G. Zhao, S. Liu, Zhong, Pinzur, J. Zhang, Y. Wang, Jose, Pourreza, Baxter, Datta, Ram, Melton, Chau, Cheng, Y. Xiong, L. Zhou)
- **연도/venue:** 2024 | **USENIX ATC 2024, Best Paper** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** arXiv `2402.06194`; TOCS `10.1145/3767334`
- **운영 문제:** 이중화에 가려진 gray failure를 학습 성능 저하 전에 발견
- **방법:** 벤치마크 스위트 + Validator + **Selector(검증 비용 최적화기)** — 시간 예산 하에서 어떤 검증을 언제 돌릴지 최적화
- **평가 규모/기간:** **수십만 GPU, 2년, Azure**
- **real production data:** **Y** | **deployment:** **Y (D5)**; MTBI 최대 **22.61×** 개선
- **L2+L3+L6+L7 · D5 · P?** — **P: 원 출처 정의 상이(F production-realism P4) — 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT (다중 falsifier)**
- **왜 Must Read:** **세 축을 동시에 위협한다.** (i) axis D의 GPU gray failure, (ii) axis F의 validate→isolate→repair 루프, (iii) **axis C(관측 비용 대 탐지 이득 최적화)에 가장 근접한 정식화**. 단, SuperBench는 **능동 검증(비용=빼앗긴 GPU 시간)**을 최적화할 뿐 **수동 텔레메트리(비용=바이트)**를 최적화하지 않는다 — 이것이 KISTI의 유일한 방어선이다.

---

**M-32 · Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems**
- **저자:** Ruiming Lu, Erci Xu, Yiming Zhang, Fengyi Zhu, Zhaosheng Zhu, Mengtian Wang, Zongpeng Zhu, Guangtao Xue, Jiwu Shu, Minglu Li, Jiesheng Wu (SJTU/Alibaba/Xiamen)
- **연도/venue:** 2023 | **FAST 2023** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** `usenix.org/conference/fast23/presentation/lu`
- **운영 문제:** 클라우드 스토리지의 fail-slow 드라이브 탐지
- **방법:** per-drive latency-vs-load 회귀
- **평가 규모/기간:** **248,000 드라이브 / 10개월**; fail-slow 드라이브 **304개** 발견; 격리로 p99.99 tail latency **48% 절감**; **라벨 데이터셋 공개**(41K normal, 315 verified fail-slow)
- **real production data:** **Y** | **deployment:** **Y**
- **L3+L5+L7 · D4~D5 · P?** — **P: 원 출처 정의 상이(C P1, G P4) — 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT (강한 falsifier)**
- **왜 Must Read:** 장치 수준 fail-slow **탐지는 프로덕션에서 이미 해결된 문제**임을 확정한다. KISTI의 기여는 "탐지"가 아니라 **"귀속(attribution)"**이어야 한다. 또한 검증된 fail-slow ground truth를 공개한 극소수 사례 — 데이터 공개의 가치 근거.

---

**M-33 · Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems**
- **저자:** Haryadi S. Gunawi et al. (16개 기관, **LANL·ANL 포함**)
- **연도/venue:** 2018 | **FAST 2018** (+ ACM TOS 14(3)) | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** `10.1145/3242086` · `usenix.org/conference/fast18/presentation/gunawi`
- **운영 문제:** fail-slow 하드웨어를 1급 장애 모드로 정립
- **방법:** 인시던트 보고 수집 → fault→symptom 변환 및 연쇄의 taxonomy
- **평가 규모/기간:** ⚠**불일치** — C: "101 fail-slow incident reports" · G: "~12개 기관의 인시던트 보고(정확한 수 `UNVERIFIED`, 통상 101건으로 인용됨)"
- **real production data:** **Y** | **deployment:** N/A (연구)
- **L0 (C) / L5 taxonomy (G)** ⚠**불일치** · **D1~D2** · **P?** — **P: 원 출처 정의 상이(C P4=system-agnostic, G P4=multi-system/multi-year) — 우연히 값이 같으나 의미가 다름, 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT (정의적 선행연구)**
- **왜 Must Read:** C의 경고 — **이미 LANL·ANL(즉 HPC) 인시던트를 포함하고 있으므로 "HPC의 fail-slow는 미연구 영역"이라고 주장할 수 없다.**

---

**M-34 · Automatic Root Cause Analysis via Large Language Models for Cloud Incidents (RCACopilot)**
- **저자:** Yinfang Chen, Huaibing Xie, Minghua Ma, Yu Kang, Xin Gao, Liu Shi, Yunjie Cao, Xuedong Gao, Hao Fan, Ming Wen, Jun Zeng, Supriyo Ghosh, Xuchao Zhang, Chaoyun Zhang, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, Tianyin Xu
- **연도/venue:** 2024 | **EuroSys 2024** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** `10.1145/3627703.3629553` · arXiv `2305.15778`
- **운영 문제:** 클라우드 인시던트의 자동 근본원인 분석
- **방법:** 2단계 — handler 기반 **진단 증거 수집**(진짜 시스템 기여) → FastText+temporal retrieval → few-shot CoT GPT-4 범주 예측 + 설명
- **평가 규모/기간:** **653 incidents, Microsoft Transport, 1년.** Micro-F1 **0.766**, Macro-F1 **0.533**, 4.2 s/incident
- **real production data:** **Y** | **deployment:** **Y** — 수집 컴포넌트는 **4년 이상, 30개 이상 MS 팀에 배치**
- **L5+L6 · D4 · P?** — **P: 원 출처 정의 상이(C P1, G P4) — 재확인 필요**
- **SC-relevance:** **SC-REGULAR-RELEVANT (axis G의 기준점)**
- **핵심 한계(저자 명시):** 단일 서비스 평가; **Macro-F1 0.533**으로 희소 범주에 약함(정작 도움이 필요한 범주); 사전 정의된 incident handler 없이는 동작 불가; 자율적이지 않고 권고만 함
- **왜 Must Read:** **지속 가능한 기여는 LLM이 아니라 handler 기반 증거수집 아키텍처였다**(4년 프로덕션). KISTI가 LLM 논문을 쓴다면 이 패턴을 복제해야 한다.

---

**M-35 · L4: Diagnosing Large-scale LLM Training Failures via Automated Log Analysis**
- **저자:** Jiang, Huang, Yu, Chen, Li, Zhong, Feng, Yang, Yang, Lyu
- **연도/venue:** 2025 | **FSE Companion '25 (industry track)** | `[ARCHIVAL-PEER-REVIEWED]` ✅검증
- **DOI/URL:** `10.1145/3696630.3728531`
- **운영 문제:** 대규모 LLM 학습 장애의 진단
- **데이터 소스:** **428건의 실제 LLM-training 장애, Platform-X, 2023-05~2024-04, 평균 941 accelerators, 장애당 평균 16.92 GB 로그**
- **방법:** Drain parsing → 성공 job 대비 cross-job filtering → 공간(IsolationForest across ranks) + 시간(DTW + 3σ across iterations) → fault-pattern library. **LLM을 진단 경로에 사용하지 않음**
- **평가 규모/기간:** 100건 평가셋. F1 **0.873**(R 0.982 / P 0.786) vs LogAnomaly/LogRobust/NeuralLog **0.207–0.366**; faulty-node top-1 **65.8%**, top-5 **80%**
- **인간 기준선:** 평균 진단 시간 **34.7시간**, **41.9%는 24시간 초과**
- **real production data:** **Y** | **deployment:** **Y, 2024-06부터 가동**, SRE에 권고
- **L5 · D4 · P?** — **P: 원 출처 정의 상이(G production-evidence P3) — 재확인 필요**
- **핵심 한계(저자 명시):** **36%의 장애는 로그를 넘어선 multi-modal 데이터(metrics, network traces) 필요**; 10.1%는 로그 증거를 전혀 남기지 않음
- **SC-relevance:** **SC-REGULAR-RELEVANT**
- **왜 Must Read:** ⚠ **이 분야에서 가장 강력한 anti-LLM 논거.** LLM 없이 Drain+IsolationForest+DTW로 LLM 시대 로그 이상탐지 베이스라인을 **압도**했다. KISTI가 LLM 논문을 쓴다면 이것이 비교 대상이며, **34.7시간이라는 측정된 인간 기준선**은 모든 운영 논문이 본받아야 할 평가 설계다.

---

**M-36 · Online Diagnosis of Performance Variation in HPC Systems Using Machine Learning**
- **저자:** Ozan Tuncer, Emre Ates, Yijia Zhang, Ata Turk, Jim M. Brandt, Vitus J. Leung, Manuel Egele, Ayse K. Coskun
- **연도/venue:** ⚠**연도 불일치** — C: **IEEE TPDS 30(4):883–896, 2019** · F: "2018, IEEE TPDS" · G: "2019, IEEE TPDS". **DOI는 세 출처 모두 `10.1109/TPDS.2018.2870403`로 일치**(DOI 접두 연도가 2018이라 혼동 발생 가능). 인용 시 **TPDS vol.30 no.4 (2019)**로 확인 권장
- **publication-type:** `[JOURNAL / ARCHIVAL-PEER-REVIEWED]`
- **운영 문제:** 런타임 성능 이상의 **유형(typed) 진단** — network contention / CPU contention / memory bandwidth / orphan processes
- **시스템/구성요소:** node telemetry (CPU/mem/vmstat/Cray power/**Aries NIC**)
- **데이터 소스:** Volta XC30m, **52 nodes**, 약 4,950회의 4-node run, **721 metrics @1Hz**
- **방법:** 통계 윈도 특징 + KS/Benjamini-Yekutieli 특징선택 + tree ensembles (특징 약 **57% 축소**)
- **평가 규모/기간:** 테스트베드
- **real production data:** **N** (합성 이상 주입) | **deployment:** **N** (F) / Partial (G) ⚠불일치
- **L5 · D1 · P?** — **P: 원 출처 정의 상이(F production-realism P1, G P1) — 재확인 필요.** 정본 기준으로는 P4(일반화 가능한 방법) 재매핑이 방어 가능 `[L/D/P re-mapped]`
- **주 기여:** 98% 탐지, 0.08% false alarm. **HPC 이상 진단의 정본 베이스라인**
- **핵심 한계:** 테스트베드 전용; **합성 이상만 사용**; 미지 앱에서 FA 8–9%; 타 모니터링 인프라로의 일반화는 저자도 미기술
- **SC-relevance:** **SC-REGULAR-RELEVANT (매우 위험한 falsifier)**
- **왜 Must Read:** ⚠ **C의 평가: "이것이 당신의 축이고, HPC에서, 7년 전에 이미 됐다. 인용하고 이기지 못하면 리뷰를 통과하지 못한다."** 선행: Tuncer et al., ISC 2017 Best Paper, `10.1007/978-3-319-58667-0_19`. 후속 계열: E2EWatch (Euro-Par 2021, `10.1007/978-3-030-85665-6_5`).

---

**M-37 · ARGUS: Production-Scale Tracing and Performance Diagnosis for over 10,000-GPU Clusters**
- **저자:** Zhou, Zeng, Chen, Lu, Yang, Ye, Ying, Zhang
- **연도/venue:** 2026 | **arXiv (venue not stated)** | `[PREPRINT]` ✅내용 확인됨
- **DOI/URL:** arXiv `2606.20374`
- **운영 문제:** 10,000 GPU 이상 클러스터의 상시 성능 진단
- **방법:** 계층적 always-on tracing (CPU stacks / framework semantics / GPU kernels), overhead **<2%**, kernel-event **3700× 압축**, **progressive diagnosis**
- **평가 규모/기간:** **>10,000 GPUs, 연속 6개월**
- **real production data:** **Y** | **deployment:** **Y**
- **L5 · D4 · P?** — **P: 원 출처 정의 상이(G production-evidence P3/P4) — 재확인 필요**
- **원인 판별 능력:** compute straggler / **link degradation** / pipeline-bubble amplification / FlashAttention JIT stall / communication-masked compute straggler
- **핵심 한계:** **동기·반복·동질 학습 job을 기준 모델로 가정** — "rank i와 rank j를 iteration k에서 비교"가 성립하는 것은 그 주기성 때문. **Slurm 기반 이질 MPI job, CPU-only job, Lustre, 냉각/전력, cross-job 간섭 귀속, topology/placement 원인 클래스가 전혀 없음**
- **SC-relevance:** **SC-REGULAR-RELEVANT (axis D 최강 falsifier)**
- **왜 Must Read:** G의 경고 — 리뷰어는 **"ARGUS가 이미 10,000 GPU에서 6개월간 다중 원인 fail-slow 진단을 배치했는데, 기계가 한국산이라는 것 말고 무엇이 새로운가?"**라고 묻는다. 답은 **ARGUS가 구조적으로 만들 수 없는 원인 taxonomy**(cross-job 간섭, topology/placement, Lustre, 냉각/전력)와 **주기성 가정이 깨지는 이질 배치 job**에서의 평가여야 한다.

---

### 【D군】 데이터셋 · 평가 방법론 (5편)

---

**M-38 · M100 ExaData: a data collection campaign on CINECA's Marconi100 Tier-0 supercomputer**
- **저자:** Antici, Borghesi, Di Santi, Molan, Seyedkazemi Ardebili, Bartolini et al. (H 기재) — ⚠F는 `author list UNVERIFIED`
- **연도/venue:** 2023 | **Scientific Data 10, 288** | `[JOURNAL-DATA-DESCRIPTOR]`
- **DOI/URL:** `10.1038/s41597-023-02174-3` · Zenodo 인덱스 `zenodo.org/records/10533504` (12개 개별 DOI) · 도구 `gitlab.com/ecs-lab/exadata/`
- **데이터:** ⚠**세부 불일치** — F(B19): "M100, **20 months**, 980 nodes, **261 metrics/node**" · G(E1)/H: "**573 metrics**, 980+ nodes, **934 days (2020-03-09 → 2022-09-28)**, **49.9 TB** uncompressed". H가 원 descriptor 기반이므로 573/934일/49.9TB가 유력하나 **F의 261 metrics/20개월과 병기**
- **소스:** IPMI + Slurm + **Nagios 관리자 경보(약라벨)** + Ganglia + facility(액랭·CRAC·PSU·기상)
- **라이선스:** **CC-BY-4.0**, Parquet/zstd-9
- **핵심 수치:** 논문 자체 검증 — thermal hazard 예측 **F1 = 0.94**(SVC), 비지도 이상탐지 **AUC = 0.57**(RUAD, 단일노드)
- **L0 · D2/D5 · P?** — **P: 원 출처 정의 상이 — 재확인 필요**
- **한계:** sub-second 타이밍 폐기; **이상 라벨이 15분 집계 단위에만 존재**; 사용자/job ID 완전 익명화로 **사용자 행동 분석 불가**; 노드명 무작위화; 모니터링 인프라 자체가 다운된 구간의 결측
- **왜 Must Read:** **AUC 0.57은 본 전수조사 전체에서 가장 정직한 수치**이며, "운영 약라벨은 그대로는 거의 무정보"라는 공개·인용 가능한 자백이다. KISTI의 기대치 설정과 axis E 논거의 앵커.

---

**M-39 · F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems**
- **저자:** Antici, Domke, Yamamoto, Kiziltan, Bartolini (H 기재) — ⚠F는 `authors UNVERIFIED`
- **연도/venue:** 2025 | **Scientific Data** | `[JOURNAL-DATA-DESCRIPTOR]`
- **DOI/URL:** `10.1038/s41597-025-05633-1` · Zenodo `10.5281/zenodo.11467483`
- **데이터:** **약 24 million job executions, 2021-03 ~ 2024-04, 45 features/record, 28 GB, 38개 월별 Parquet 청크**. 제출/시작/완료, cores/memory/nodes/frequency, **per-component power (min/avg/max)**, performance counters와 파생지표, duration, exit codes. 민감 텍스트는 **Sentence-BERT 임베딩으로 비가역 인코딩**
- **클래스 균형:** **21M+ completed vs ~2.5M failed**
- **한계:** A64FX 특화(전이성 불명); per-job water usage 없음; 원본 데이터는 RIKEN 독점, 접근은 기관 협약으로 협상
- **왜 Must Read:** **현존 최대 라벨링 job 코퍼스**이며, M-38(M100)과 함께 **cross-system/cross-generation 연구(axis B)를 무비용으로 가능케 하는 유일한 쌍**이다. 두 데이터셋의 공통분모가 **University of Bologna(Bartolini/Antici) 그룹**이라는 사실 — 즉 "학계 그룹을 센터 데이터에 결합"이 KISTI가 복제할 모델.

---

**M-40 · Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics**
- **저자:** Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu
- **연도/venue:** 2023 | **ISSRE 2023** ⚠(G는 `venue UNVERIFIED, commonly cited as ISSRE 2023`; C는 ISSRE 2023으로 ✅검증) | `[ARCHIVAL-PEER-REVIEWED / DATASET]`
- **DOI/URL:** 원자료에 DOI 미기재
- **데이터:** 사실상의 표준 로그 벤치마크. **BGL / Thunderbird / Spirit 등 2007년대 HPC RAS 로그 포함**
- **계보:** Oliner & Stearley, *What Supercomputers Say: A Study of Five System Logs*, **DSN 2007**, `10.1109/DSN.2007.103` (BGL/Thunderbird/Spirit/Liberty/RedStorm 공개) → He et al., ISSRE 2016 `10.1109/ISSRE.2016.21` → Zhu et al., ICSE-SEIP 2019 `10.1109/ICSE-SEIP.2019.00021` → **Loghub (ISSRE 2023)** → Loghub-2.0 (2024, `UNVERIFIED`)
- **왜 Must Read:** ⚠ **이 분야는 2026년에도 2007년 BGL 로그로 벤치마킹하고 있다.** C의 판단: 이 노후화 자체가 SC 논문의 논거이며, **"현대적 다계층 HPC 텔레메트리 코퍼스의 공개"가 KISTI가 취할 수 있는 가장 내구성 있는 SC 기여**다(Loghub의 인용 수가 데이터셋의 가치를 증명).

---

**M-41 · Towards a Rigorous Evaluation of Time-series Anomaly Detection (point-adjustment 비판)**
- **저자:** Kim, Choi, Jang, Yoon — ⚠G는 `author list UNVERIFIED`
- **연도/venue:** 2022 | **AAAI 2022** | `[ARCHIVAL-PEER-REVIEWED]`
- **DOI/URL:** arXiv `2109.05257` · `ojs.aaai.org/index.php/AAAI/article/view/20680`
- **핵심 결과:** 사실상 모든 딥 TSAD 논문이 쓰는 **point-adjustment 평가 프로토콜이 F1을 심각하게 부풀려, 무작위 점수 탐지기가 SOTA를 이긴다**
- **동반 문헌:** *Multivariate Time Series Anomaly Detection: Fancy Algorithms and Flawed Evaluation Methodology* (2024, `10.1007/978-3-031-68031-1_1`, 독립 재확인); *Did We Actually Fix It?* (2026, arXiv `2607.11969`, 대체 지표의 스트레스 테스트, 내용 `UNVERIFIED`); *Navigating the metric maze* (`10.1007/s10618-023-00988-8`)
- **왜 Must Read:** ⚠ **G의 처방: point-adjusted F1을 명시적으로 거부하고, 고정 alert budget 하에서 보고하며, 이 논문을 인용해 논의하라.** 이를 지키지 않으면 심사에서 평가 방법론만으로 무너진다. 반대로 이를 지키는 것만으로도 대부분의 경쟁 논문 대비 차별화된다.

---

### §1.42 필수목록 대비 확인 결과 (누락·미확인 없음)

사용자가 지정한 41개 필수 항목 전부가 원자료에서 메타데이터와 함께 확인되어 위에 수록되었다. **원자료에 존재하지 않아 창작해야 했던 항목은 없다.** 다만 다음 항목들은 **원자료 자체가 불완전**하다:

| 항목 | 불완전 사유 |
|---|---|
| M-07 Cost-Aware DRAM (SC20) | DOI 미기재(페이지 URL만) |
| M-12 Not All GPUs (SC22) | DOI 미기재(페이지 URL만) |
| M-14 From Alert Fatigue (SC26) | **DOI 미발행, 미개최, 초록 미확보** |
| M-27 Time Machine (DSN23) · M-28 ClusterRCA · M-29 Too Many Cooks · M-40 Loghub | DOI 미기재(프로그램 페이지 기반 검증) |
| M-37 ARGUS | **arXiv preprint, venue 미확정** |
| M-01 Kaleidoscope · M-13 Slingshot | DOI 식별자가 출처마다 상이 |
| M-36 Tuncer TPDS | 연도 표기가 출처마다 상이(2018/2019) |

---

# 2. RELEVANT — 주제별 압축 목록

> 표기: `type` = publication type tag · `SC` = SC-regular relevance (**PRE**=SC-REGULAR-PRECEDENT, **REL**=SC-REGULAR-RELEVANT, **POT**=SC-REGULAR-POTENTIAL, **PRAC**=PRACTICE-ONLY, **PER**=PERIPHERAL)
> ⚠ **B census(HPDC/IPDPS/Cluster/ISC/ACSOS) 항목의 L/D/P·평가규모·배포 여부는 abstract 미독 상태의 *assessment*다.** 인용 전 PDF 확인 필수. 해당 항목은 `[A]`로 표시.

## 2.1 Anomaly detection & diagnosis (HPC telemetry)

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Proctor: A Semi-Supervised Performance Anomaly Diagnosis Framework for Production HPC Systems | 2021 | ISC High Performance | ARCHIVAL | 10.1007/978-3-030-78713-4_11, pp.195–214 | L3→L5 | D2–D3 | P4 | **PRE** | 탐지에서 *진단*(결함 클래스 명명)으로. Sandia LDMS production telemetry |
| E2EWatch: An End-to-End Anomaly Diagnosis Framework for Production HPC Systems | 2021 | Euro-Par | ARCHIVAL | 10.1007/978-3-030-85665-6_5 | L3/L5 | D3 | P2 | REL | Proctor 계열의 운영자 대면 패키징(Grafana 통합). Eclipse 1,488노드, **anomaly는 HPAS 합성 주입** |
| ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems | 2022 | IEEE Cluster | ARCHIVAL | 10.1109/cluster51413.2022.00048, pp.369–380 | L3/L5 | D2–D3 | P4 | **PRE** | label 비용이 곧 기여. 동일 F1에 **label 28배 절감** |
| Refine: A Robust Approach to Unsupervised Anomaly Detection for Production HPC Systems | 2025 | ISC High Performance | ARCHIVAL | bu.edu/peaclab (PDF) | L3 | D2/D3 | P2 | REL | Prodigy의 "깨끗한 학습셋" 가정을 완화(오염된 학습셋 강건성) |
| RUAD: Unsupervised anomaly detection in HPC systems | 2023 | FGCS 141 | JOURNAL | 10.1016/j.future.2022.12.001 · arXiv 2208.13169 | L3 | D2 | P3 | REL | M100 ~10개월. **per-node LSTM autoencoder** — 일반화의 정반대 극. MODA21 워크숍 논문의 아카이벌 후속 |
| An Explainable Model for Fault Detection in HPC Systems | 2021 | MODA (ISC) | WORKSHOP | 10.1007/978-3-030-90539-2_25 | L3 | D2 | P3 | REL | RUAD 계보의 출발점. CINECA Tier-0, 2019-04~07, 관리자 수동 label |
| A semisupervised autoencoder-based approach for anomaly detection in HPC systems | 2019 | Eng. Appl. of AI | JOURNAL | ScienceDirect S0952197619301721 | L3 | D2 | P2 | REL | normal-only 학습. HPC semi-supervised의 정본 baseline |
| Prodigy 이전 계보: Diagnosing Performance Variations in HPC Applications Using ML | 2017 | ISC High Performance | ARCHIVAL | 10.1007/978-3-319-58667-0_19 | L5 | D1 | P1 | REL | 주입 anomaly 유형의 지도 분류. Tuncer 계열 시발점 |
| Harnessing federated learning for anomaly detection in supercomputer nodes | 2025 | FGCS | JOURNAL | S0167739X24004254 | L3 | D2 | P3 | REL | **한 시스템의 노드 간** federated. cross-site가 아님 |
| Detecting Anomalies in Systems for AI Using Hardware Telemetry (Reveal) | 2025 | arXiv 2510.26008 | PREPRINT | arXiv 2510.26008 | L3 | D1 | P1 | POT | ~700 채널→~60 유지, **<1.5% CPU overhead, 14–22 KB/s/host**. 이 공간 최고의 명시적 비용 회계 |
| When GPUs Fail Quietly: Observability-Aware Early Warning Beyond Numeric Telemetry | 2026 | arXiv 2603.28781 | PREPRINT | arXiv 2603.28781 | L3/L4 | D2 | P3 | REL | **모니터링 파이프라인 자체의 열화**(scrape latency, sample loss)를 신호로. GWDG 28 GPU/~353일, 69 인시던트, **Zenodo 공개** |
| A survey of anomaly detection in HPC systems using machine learning | 2026 | CCF THPC 8(3):352–376 | SURVEY | 10.1007/s42514-025-00266-7 | — | — | — | REL | **cross-system generalization을 최상위 open challenge로 지목** — gap 주장 인용용 |

## 2.2 Failure & error prediction

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Aarohi: Making Real-Time Node Failure Prediction Feasible | 2020 | IPDPS | ARCHIVAL | 10.1109/ipdps47924.2020.00115, pp.1092–1101 | L4 | D2–D3 | P4 | **PRE** | 정확도가 아니라 **추론 지연**으로 재프레이밍 |
| Systemic Assessment of Node Failures in HPC Production Platforms | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00035, pp.267–276 | L2 | D2 | P2 | **PRE** | Aarohi를 정당화하는 필드 연구(순서가 역전) |
| Time Machine: Generative Real-Time Model For Failure (and Lead Time) Prediction in HPC Systems | 2023 | DSN | ARCHIVAL | — (프로그램 검증) | L4 | D2 | P1 | **PRE** | 장애 **와 lead time** 동시 예측. HPC 실패예측 SC 제출의 최근접 DSN 선행 |
| An Effective Uncorrectable Memory Error Prediction Framework by Exploiting UPH Indicators | 2025 | IPDPS | ARCHIVAL | 10.1109/ipdps64566.2025.00112, pp.1238–1248 | L4 | D2–D4 | P3 | **PRE** `[A]` | HPDC'24 BSC 논문과 쌍. 메모리 예측 SOTA |
| From Correctable Memory Errors to Uncorrectable Memory Errors: What Error Bits Tell | 2022 | SC22 | TRACK-UNKNOWN | sc22 pap137 | L4 | D2–D3 | P4 | **PRE** | ByteDance 필드. **약화된 ECC라는 아키텍처적 원인**을 지목 |
| Understanding Memory Failures on a Petascale Arm System | 2022 | HPDC | ARCHIVAL | 10.1145/3502181.3531465, pp.84–96 | L0/L2 | D2 | P2 | **PRE** `[A]` | Astra(Arm) 최초 필드 메모리 신뢰성 |
| Understanding the Effects of DRAM Correctable Error Logging at Scale | 2021 | IEEE Cluster | ARCHIVAL | 10.1109/cluster48925.2021.00060, pp.421–432 | L2 | D2–D4 | P2 | **PRE** `[A]` | CE 로깅의 비용/편익 — 운영 결정이 붙은 필드 연구 |
| SEFEE: Lightweight Storage Error Forecasting in Large-Scale Enterprise Storage Systems | 2020 | SC20 | TRACK-UNKNOWN | sc20 pap363 | L4 | D2 | P4 | REL | **학습 불필요 tensor decomposition**. 87 시스템/14,371 디스크/2년, 2,300만+ 이벤트 |
| Proactive SSD Failure Prediction with A Gradient-Guided LSTM-xLSTM Hybrid Model | 2025 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59342.2025.11186457 | L4 | D2–D3 | P3–P4 | REL `[A]` | 장치 고장 예측 |
| Be SMART, Save I/O: A Probabilistic Approach to Avoid Uncorrectable Errors in Storage | 2022 | IEEE Cluster | ARCHIVAL | 10.1109/cluster51413.2022.00038 | L4→L7 | D2 | P3 | REL `[A]` | SMART 기반 선제 회피 |
| Making Disk Failure Predictions SMARTer! | 2020 | FAST | ARCHIVAL | USENIX FAST'20 | L4 | D2 | P2 | REL | 38만 드라이브/64 사이트/2개월, 10일 horizon **F1 0.95 / MCC 0.95**. 불균형 데이터에 **MCC 보고**의 모범 |
| HiMFP: Hierarchical Intelligent Memory Failure Prediction for Cloud Service Reliability | 2023 | DSN | ARCHIVAL | — (프로그램 검증) | L4 | D2 | P1 | REL | cell→bank→DIMM→node 계층 예측 |
| Cordial: Cross-row Failure Prediction Method Based on Bank-level Error Locality for HBMs | 2025 | DSN industry | ARCHIVAL | — | L4 | D2 | P1 | REL | **HBM(=GPU 메모리) 고장 예측 직접 선행** |
| Investigating Memory Failure Prediction Across CPU Architectures | 2024 | DSN industry | ARCHIVAL | — (프로그램 검증) | L4 | D2 | **P3** | **PRE** | ⚠ **하드웨어 고장예측 모델의 아키텍처 간 전이 — axis B 직격탄** |
| Predicting DRAM-Caused Node Unavailability in Hyper-Scale Clouds | 2022 | DSN | ARCHIVAL | — | L4 | D2/D3 | P1 | REL | Alibaba. HPC DRAM→노드 장애 예측의 최근접 클라우드 유사물 |
| Evaluating Forecasting Techniques for Hardware Errors on a Large-scale HPC System | 2026 | MODA (ISC) | WORKSHOP | arXiv 2608.01648 | L2 | D2 | P3 | REL | **Theta 7년치**. 규칙적 오류는 예측 가능, 희소·버스티는 불가. cross-system·비용 미다룸 |
| Reducing False Node Failure Predictions in HPC | 2019 | venue `UNVERIFIED` (HiPC 추정) | UNVERIFIED | ResearchGate | L4 | D1 | P2 | POT | 자동 조치를 막는 FP 문제를 직접 다룸 |

## 2.3 Reliability field studies

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Understanding the Interplay between Hardware Errors and User Job Characteristics on Titan | 2020 | IPDPS | ARCHIVAL | 10.1109/ipdps47924.2020.00028, pp.180–190 | L2 | D2 | P2 | **PRE** | **RAS + job accounting 조인의 정본 템플릿** |
| Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study | 2024 | **ICS'24** | ARCHIVAL | 10.1145/3650200.3656615 | L3 | D2 | P4 | **PRE** | 27,648 V100. DBE가 동일 GPU에 재발하며 **온도가 아니라 지속 전력과 상관** ⚠저자 순서가 출처 간 상이 |
| GPU Reliability Assessment: Insights Across the Abstraction Layers | 2024 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59578.2024.00008 | L3 | D2 | P2 | REL `[A]` | 추상화 계층 간 GPU 신뢰성 |
| Demystifying GPU Reliability: Comparing and Combining Beam Experiments, Fault Simulation, and Profiling | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00037 | L3 | D1–D2 | P2/P4 | REL `[A]` | GPU 신뢰성 방법론 삼각측량 |
| Large-Scale AI Infra Reliability: Challenges, Strategies, and Llama 3 Training Experience | 2025 | DSN industry | ARCHIVAL | — | L0–L4 | D4/D5 | P0 | **PRE** | **16K GPU 규모 GPU 클러스터 신뢰성의 참조 필드 경험 논문** |
| DDR5 DRAM Faults in the Field | 2025 | DSN industry | ARCHIVAL | — | L0 | D2 | P2 | REL | 현세대 메모리 필드 연구 |
| Silent Data Corruptions at Scale / Detecting silent data corruptions in the wild | 2021/2022 | arXiv (Meta) | PREPRINT | arXiv 2102.11245 / 2203.08989 | L0+L3 | D4/D5 | P0 | REL | **Fleetscanner(비운영 테스트) vs Ripple(운영 중 테스트)의 명시적 비용/커버리지 트레이드오프** — axis C 유사 사례 |
| Understanding Recommendation System Robustness Against Silent Data Corruption | 2025 | ISSRE (Best Paper Cand.) | ARCHIVAL | — | L3 | D2 | P3 | REL | SDC 연구가 "발생하는가"에서 "어떤 워크로드가 신경 쓰는가"로 이동 |
| Detecting Silent Data Corruption from Hardware Counters | 2025 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59342.2025.11186479 | L3 | D2 | P3 | REL `[A]` | 하드웨어 counter 기반 SDC 탐지 |
| Blue Waters System and Component Reliability | 2021 | CUG | PAPER (CUG) | cug.org cug2021 pap102 | L2 | D2 | P2 | PRAC | NCSA 시스템 신뢰성 운영 보고 |

## 2.4 Performance variability & network

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| The Case of Performance Variability on Dragonfly-based Systems | 2020 | IPDPS | ARCHIVAL | 10.1109/ipdps47924.2020.00096, pp.896–905 | L2/L5 | D2 | P4 | **PRE** | Bhatele 계보의 출발점. 네트워크 counter + job 배치로 변동성 귀속 |
| The Case of the Elusive Application Performance on Production GPU Supercomputers | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00079, pp.913–927 | L2/L5 | D2 | P4 | **PRE** | Perlmutter+Frontier, **761 runs / 8,118 node-hours / 4개월**. **Frontier 2.6배·Perlmutter 1.4배 변동성**, 원인은 compute가 아니라 네트워크 혼잡·top user. ⚠**Rosetta 스위치 counter 미확보를 저자가 명시** |
| Characterizing Production GPU Workloads using System-wide Telemetry Data | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00078, pp.899–912 | L2 | D2 | P2–P3 | **PRE** `[A]` | UMD+NERSC 공저. **한강 GPU telemetry 센서스와 가장 가까운 발표 유사물 — 반드시 차별화** |
| Quantifying the Impact of Network Congestion on Application Performance and Network Metrics | 2020 | IEEE Cluster | ARCHIVAL | 10.1109/cluster49012.2020.00026, pp.162–168 | L2/L5 | D1–D2 | P1–P4 | **PRE** | Cori에서 통제된 congestor 주입. **ntile stall-to-flit ratio**를 혼잡 지표로 확립 |
| An In-Depth Analysis of the Slingshot Interconnect | 2020 | SC20 | TRACK-UNKNOWN | arXiv 2008.08886 · IEEE 9355230 | L0–L1 | D1–D2 | P1–P2 | **PRE** | Slingshot 최초 독립 특성화. 이후 모든 Slingshot 연구의 참조점 |
| Exploring GPU-to-GPU Communication: Insights into Supercomputer Interconnects | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00039 | L1–L3 | D2 | P2/P4 | **PRE** | Alps·Leonardo·LUMI, **최대 4,096 GPU**. SC20 Slingshot 논문의 다GPU 시대 후속 |
| An Evaluation of the Effect of Network Cost Optimization for Leadership Class Supercomputers | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00037 | L3 | D2 | P2/P4 | **PRE** | Frontier vs Summit. **~30% 비용 효율 우위** — 조달 결정 평가 논문 |
| Study of Workload Interference with Intelligent Routing on Dragonfly | 2022 | SC22 | TRACK-UNKNOWN | 10.1109/SC41404.2022.00025 | L3 | D0–D1 | P4 | REL | **시뮬레이션.** 처리량과 워크로드 공정성을 분리된 목표로 |
| Characterizing the Impact of Congestion in Modern HPC Interconnects | 2026 | arXiv 2604.11432 | PREPRINT | arXiv 2604.11432 | L2 | D1 | P1 | REL | Leonardo/CRESCO8/**LUMI(Slingshot)** 각 256노드. **edge congestion이 지배**, 토폴로지만으로 혼잡 내성 예측 불가 |
| Performance Evaluation of Adaptive Routing on Dragonfly-based Production Systems | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00042 | L2 | D2 | P2 | REL `[A]` | production 네트워크 연구 |
| An Analysis of Performance Variability on Dragonfly+ topology | 2022 | IEEE Cluster (in-proc.) | ARCHIVAL | 10.1109/cluster51413.2022.00061 | L2 | D2 | P2 | REL `[A]` | Dragonfly+ 변동성 |
| Measuring Congestion in High-Performance Datacenter Interconnects (Monet) | 2020 | **NSDI '20** | ARCHIVAL | usenix.org/conference/nsdi20/presentation/jha | L3/L5 | D2 | P3 | **PRE** | Blue Waters Gemini/Aries. **네트워크 counter로 congestion region 탐지 — fabric counter 연구의 최근접 방법론적 조상** |
| Not All GPUs Are Created Equal: Characterizing Variability in Accelerator-Rich Systems | 2022 | SC22 | TRACK-UNKNOWN | sc22 pap186 (DOI 미기재) | L3 | D2 | P4 | **PRE** | Summit/Vortex/Longhorn/Corona 4클러스터, GPU 90%+ 샘플링, 10만+ GPU-시간. **평균 32%·최대 72% 편차** |
| PAL: A Variability-Aware Policy for Scheduling ML Workloads in GPU Clusters | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00032 | L6 | D2 | P4 | REL | SC22 측정을 스케줄링 정책으로 전환 — "측정→메커니즘" 아크의 후반 |
| GVARP: Detecting Performance Variance on Large-Scale Heterogeneous Systems | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00063 | L5 | D1–D2 | P4 | REL | 분산의 *국소화*. 애플리케이션 계측 기반, production 사례 없음 |
| Beyond Thread States: Diagnosing Performance Degradation with eBPF and Thread Dynamics | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00073 | L5 | D3 | P3 | REL `[A]` | 저오버헤드 in-production 진단 |
| Enhancing Performance Insight at Scale: A Heterogeneous Framework for Exascale Diagnostics | 2025/26 | ICS (`UNVERIFIED`) | PREPRINT | arXiv 2605.03561 | L1/L5 | D2 | P1 | POT | HPCToolkit trace의 GPU 가속 질의. Frontier·**Aurora 10만 rank / 1,000노드**, 22개 랙의 Slingshot 혼잡 국소화 |

## 2.5 Storage & I/O

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| HPC I/O Throughput Bottleneck Analysis with Explainable Local Models (Gauge) | 2020 | SC20 | TRACK-UNKNOWN | sc20 pap548 | L5 | D3–D4 | P4 | **PRE** | Theta Darshan 수년치. per-job이 아니라 **job 클러스터 단위 진단**으로 재프레이밍 |
| Systematically Inferring I/O Performance Variability by Examining Repetitive Job Behavior | 2021 | SC21 | TRACK-UNKNOWN | sc21 pap336 | L3 | D2 | P4 | **PRE** | **job 반복성을 무료 label로** — production label 부재 문제에 대한 우아한 답 |
| AIIO: Using AI for Job-Level and Automatic I/O Performance Bottleneck Diagnosis | 2023 | HPDC | ARCHIVAL | 10.1145/3588195.3592986, pp.155–167 | L5 | D2–D3 | P4 | **PRE** `[A]` | HPDC에서 가장 깨끗한 L5 사례. Darshan/DXT만으로 |
| IOAgent: Democratizing Trustworthy HPC I/O Performance Diagnosis Capability via LLMs | 2025 | IPDPS | ARCHIVAL | 10.1109/ipdps64566.2025.00036, pp.322–334 | L5/L6 | D2–D3 | P4 | **PRE** `[A]` | 이 venue군 최초의 **trustworthiness-aware LLM agent** |
| Drill: Log-based Anomaly Detection for Large-scale Storage Systems Using Source Code Analysis | 2023 | IPDPS | ARCHIVAL | 10.1109/ipdps54959.2023.00028, pp.189–199 | L3 | D1–D2 | P4 | **PRE** `[A]` | **로그를 뱉는 소스 코드를 의미론적 prior로** — label 문제 우회. 이 창에서 가장 독창적인 log-AD 아이디어 |
| Towards HPC I/O Performance Prediction through Large-scale Log Analysis | 2020 | HPDC | ARCHIVAL | 10.1145/3369583.3392678, pp.77–88 | L4 | D2 | P3 | REL `[A]` | 센터 규모 로그로 I/O 성능 예측. **한국인 1저자, 한강 I/O 연구의 직접 방법론적 유사물** |
| CanarIO: Sounding the Alarm on IO-Related Performance Degradation | 2020 | IPDPS | ARCHIVAL | 10.1109/ipdps47924.2020.00018, pp.73–83 | L3 | D3 | P4 | **PRE** `[A]` | 경량 canary probe로 공유 파일시스템 경합 온라인 탐지 |
| A Year in the Life of a Parallel File System | 2018 | SC18 | ARCHIVAL | 10.1109/sc.2018.00077 | L2/L3 | D2 | P4 | **PRE** | PDSW→SC 파이프라인의 정본. 스토리지 특성화의 기준 |
| Taming I/O Variation on QoS-Less HPC Storage: What Can Applications Do? | 2020 | SC20 | TRACK-UNKNOWN | sc20 pap175 | L3→L7 | D1 | P3 | REL | Chameleon testbed. 평균 I/O 성능 ×18, 분산 ×60 — production 검증 없음 |
| FaultyRank: A Graph-based Parallel File System Checker | 2023 | IPDPS | ARCHIVAL | 10.1109/ipdps54959.2023.00029 | L5 | D1–D2 | P4 | REL `[A]` | 대규모 스토리지 결함 국소화 |
| Be Aware of Metadata Corruption in Parallel File System: It can be Silent and Catastrophic | 2025 | IPDPS | ARCHIVAL | 10.1109/ipdps64566.2025.00063 | L3 | D2 | P3 | REL `[A]` | PFS 메타데이터 silent corruption |
| Interpreting Write Performance of Supercomputer I/O Systems with Regression Models | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00064 | L4/L5 | D2 | P4 | **PRE** `[A]` | production 로그 기반 해석가능 I/O 모델 |
| Access Patterns and Performance Behaviors of Multi-layer Supercomputer I/O Subsystems under Production Load | 2022 | HPDC | ARCHIVAL | 10.1145/3502181.3531461 | L2 | D2 | P2 | **PRE** `[A]` | production 부하 하 다계층 I/O 특성화 |
| WisIO: Automated I/O Bottleneck Detection with Multi-Perspective Views for HPC Workflows | 2025 | ICS | ARCHIVAL | 10.1145/3721145.3725742 | L3 | — | — | REL | ⚠ **저자·내용 미확인.** 관련연구 작성 전 확보 필수 |
| Tango: A Cross-layer Approach to Managing I/O Interference over Local Ephemeral Storage | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00020 | L6/L7 | D2 | P4 | REL | cross-layer I/O 간섭 관리 |
| Fine-Grained Policy-Driven I/O Sharing for Burst Buffers | 2023 | SC23 | TRACK-UNKNOWN | sc23 pap190 | L6 | D2 | P4 | REL | 스토리지 QoS |
| EquilibrIO: Taming the I/O Tides in High-Performance Computing | 2025 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59342.2025.11186490 | L6/L7 | D2 | P3 | REL `[A]` | I/O 경합 제어 |
| A2FL: Autonomous and Adaptive File Layout in HPC through Real-time Access Pattern Analysis | 2024 | IPDPS | ARCHIVAL | 10.1109/ipdps57955.2024.00051 | L7 | D2 | P4 | REL `[A]` | 시스템 내 닫힌 루프 |
| Drilling Down I/O Bottlenecks with Cross-layer I/O Profile Exploration | 2024 | IPDPS | ARCHIVAL | 10.1109/ipdps57955.2024.00053 | L5 | D2 | P4 | REL `[A]` | cross-layer I/O 프로파일 |
| Capturing Periodic I/O Using Frequency Techniques | 2024 | IPDPS | ARCHIVAL | 10.1109/ipdps57955.2024.00048 | L2/L3 | D2 | P4 | REL `[A]` | I/O telemetry에 신호처리 |
| A Unified I/O Monitoring Framework Using eBPF | 2025 | MODA (ISC) | WORKSHOP | 10.1007/978-3-032-07612-0_3 | L0–L1 | D4 | P3 | **REL(높음)** | VFS 커널 함수 eBPF 추적 → Prometheus. **Darshan이 못 보는 AI/Python 워크로드 커버.** IDRIS production |

## 2.6 Scheduling & workload characterization

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Job Characteristics on Large-Scale Systems: Long-Term Analysis, Quantification and Implications | 2020 | SC20 | TRACK-UNKNOWN | sc20 pap336 | L2→L4 | D2 | P2/P4 | **PRE** | Intrepid+Mira **10년, 75만+ job, 30억+ core-hour**. 스케줄링 통념을 10년 규모로 검증 후 예측기로 전환 |
| Characterization and Prediction of Deep Learning Workloads in Large-Scale GPU Datacenters | 2021 | SC21 | TRACK-UNKNOWN | sc21 pap594 | L2→L6 | D2–D3 | P4 | **PRE** | SenseTime production trace(Helios). 특성화→두 서비스(JCT 최대 6.5배↓, 이용률 +13%). **trace 공개 자체가 커뮤니티 자산이 됨** |
| MCBound: An Online Framework to Characterize and Classify Memory/Compute-bound HPC Jobs | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00062 | L4 | D3–D4 | P4 | **PRE** | Fugaku **220만 job run**. 과거 telemetry에서 자기 label 유도. F1-macro ≥0.89, Fugaku에 구현 |
| Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining | 2024 | IPDPS | ARCHIVAL | 10.1109/ipdps57955.2024.00037, pp.337–349 | L2/L3/L5 | D2–D4 | P3–P4 | **PRE** `[A]` | **운영자 소비가능성을 명시적 목표로.** D3→D4 다리를 건너는 드문 사례 |
| Cross-System Analysis of Job Characterization and Scheduling in Large-Scale Computing Clusters | 2024 | IPDPS | ARCHIVAL | 10.1109/ipdps57955.2024.00069 | L2 | D2 | P2 | **PRE** `[A]` | **이 census에서 사실상 유일한 cross-system 비교 논문** |
| Are We There Yet? Predicting the Queue Wait Times for HPC Jobs | 2025 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59342.2025.11186489 | L4 | D2–D4 | P3 | **PRE** `[A]` | LANL production job 기록. **사용자 대면 예측 서비스 — 센터 산출물이자 논문인 좋은 템플릿** |
| Analyzing Resource Utilization in an HPC System: A Case Study of NERSC's Perlmutter | 2023 | ISC High Performance | ARCHIVAL | 10.1007/978-3-031-32041-5_16 | L2 | D2 | P2 | **PRE** `[A]` | "한강 이용률 센서스" 논문의 직접 ISC 선례 |
| Toward Scalable Resource Management for Supercomputers (ESlurm) | 2022 | SC22 | TRACK-UNKNOWN | sc22 pap373 | L6 | D5 | P3/P4 | REL | **production 배포**, 10만 노드까지 평가. "스케줄러를 다시 만들었고 운영 중"이 SC 게재 가능함을 보여줌 |
| RLScheduler: An Automated HPC Batch Job Scheduler Using Reinforcement Learning | 2020 | SC20 | TRACK-UNKNOWN | sc20 pap573 | L6 | D2 | P4 | REL | trace 기반 RL 스케줄링. ABSTRACT-UNREAD |
| Mirage: Toward Low-interruption Services on Batch GPU Clusters with RL | 2023 | SC23 | TRACK-UNKNOWN | sc23 pap191 | L6 | D2–D3 | P4 | REL | GPU 클러스터 RL 스케줄링 |
| Resource Utilization Aware Job Scheduling to Mitigate Performance Variability | 2022 | IPDPS | ARCHIVAL | 10.1109/ipdps53621.2022.00040 | L4→L6 | D2 | P4 | REL `[A]` | 이용률 telemetry로 변동성 완화 스케줄링 |
| Enhancing HPC Batch Job Scheduling via Imitation Learning-Based Search | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00104 | L6 | D2 | P4 | REL `[A]` | 모방학습 스케줄링 |
| MRSch: Multi-Resource Scheduling for HPC | 2022 | IEEE Cluster | ARCHIVAL | 10.1109/cluster51413.2022.00020 | L6 | D2 | P4 | REL `[A]` | RL 다자원 스케줄링 |
| Improving checkpointing intervals by considering individual job failure probabilities | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00038 | L4→L6 | D1–D2 | P4 | REL `[A]` | 예측→정책 |
| Duration-Informed Workload Scheduler | 2025 | MODA (ISC) | WORKSHOP | 10.1007/978-3-032-07612-0_1 | L4→L6 | D2 | P2 | REL(높음) | M100 ExaData trace. **평균 대기 ~11% 감소**, 시뮬레이션만 — **실제 배포하면 SC/IPDPS 논문** |
| Job Grouping Based Intelligent Resource Prediction Framework | 2025 | JSSPP (IPDPS) | WORKSHOP | LNCS 16210 | L4 | D2 | P2 | REL | BU+Sandia |
| Motivating Regime-Aware User-Profiles for Runtime Prediction in Large-Scale HPC Systems | 2026 | HPDC poster | POSTER | 10.1145/3806645.3820074, pp.579–580 | L4 | D1 | P1 | POT | **2쪽 포스터. 명백한 full-paper 기회** |
| Predicting Job Power Consumption Based on RJMS Submission Data in HPC Systems | 2020 | ISC High Performance | ARCHIVAL | 10.1007/978-3-030-50743-5_4 | L4 | D2 | P3–P4 | REL `[A]` | **제출 시점 메타데이터만으로 예측**(런타임 telemetry 불필요) — 매력적 프레이밍 |

## 2.7 Power · cooling · sustainability

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Revealing Power, Energy, and Thermal Dynamics of a 200PF Pre-Exascale Supercomputer | 2021 | SC21 | TRACK-UNKNOWN | sc21 pap343 | L1–L3 | D2 | P2/P4 | **PRE** | Summit **전 4,626노드, 100+ metric @1Hz, 2020년 전체 + 84만 job + 25만 GPU 장애 로그**. 이후 ORNL SC 논문들의 데이터 자산 |
| Toward Sustainable HPC: In-Production Deployment of Incentive-Based Power Efficiency Mechanism on Fugaku | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00030 | L6→L7 | D5 | P1/P3 | **PRE** | **Fugaku 158,976노드 in-production 정책 개입**("Fugaku Points"). 알고리즘이 아니라 사회기술적 |
| Toward Sustainable HPC: Carbon Footprint Estimation and Environmental Implications | 2023 | SC23 | TRACK-UNKNOWN | sc23 pap129 | L2/L3 | D2 | P4 | REL | 탄소를 1급 운영 지표로. "Toward Sustainable HPC:" 프랜차이즈 시작 |
| Benchmark-driven Models for Energy Analysis and Attribution of GPU-Accelerated Supercomputing | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759815 | L3/L5 | D2 | P4 | REL | 기능단위(FPU/tensor core/int ALU)·메모리계층별 에너지 귀속 |
| ThirstyFLOPS: Water Footprint Modeling and Analysis Toward Sustainable HPC Systems | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759804 | L3/L4 | D1–D2 | P4 | REL | 물 발자국 |
| Core Hours and Carbon Credits: Incentivizing Sustainability in HPC | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759858 | L6 | D2–D3 | P3 | REL | SC24 Fugaku 인센티브의 형제 |
| What does Power Consumption Behavior of HPC Jobs Reveal? | 2020 | IPDPS | ARCHIVAL | 10.1109/ipdps47924.2020.00087 | L2+L4 | D2 | P4 | **PRE** `[A]` | job 전력 특성화 + 예측 |
| Analysis of Cooling Water Temperature Impact on Computing Performance and Energy Consumption | 2020 | IEEE Cluster | ARCHIVAL | 10.1109/cluster49012.2020.00027 | L2 | D2 | P2 | REL `[A]` | **main track에 드문 facility↔compute 결합** |
| Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems | 2022 | MODA (ISC) | WORKSHOP | 10.1007/978-3-031-23220-6_18 | L2–L3 | D3 | P3 | REL(높음) | Marconi100 **실제 열 비상사태로 검증**. 주입이 아닌 실제 facility 인시던트 검증은 이 census에서 희소 |
| Multi-level anomaly prediction in Tier-0 datacenter | 2022 | ACM Computing Frontiers | ARCHIVAL | 10.1145/3528416.3530864 | L3→L4 | D2 | P3 | REL | 위 워크숍 논문의 아카이벌 후속 |
| Data Center Facility Monitoring with Physics Aware Approach | 2022 | MODA (ISC) | WORKSHOP | 10.1007/978-3-031-23220-6 (pp.251–261) | L1–L3 | D2 | P2 | REL | NREL. 물리 인지 facility 모니터링 |
| Exploring the Frontiers of Energy Efficiency using Power Management at System Scale | 2024 | arXiv 2408.01552 | PREPRINT | arXiv 2408.01552 | L6 | D3–D5 | P3 | REL | Frontier 3개월 telemetry, **최대 8.5% / ~1,438 MWh 절감**. ⚠arXiv 외 venue `UNVERIFIED` |
| Accurate and Convenient Energy Measurements for GPUs: NVIDIA GPU's Built-In Power Sensor | 2024 | SC24 | TRACK-UNKNOWN | — | L0 | D2 | P2/P4 | REL | **"전력 telemetry를 믿을 수 있는가"** — 측정 충실도 논문 |
| Energy-aware operation of HPC systems in Germany | 2025 | Frontiers in HPC | JOURNAL | 10.3389/fhpcp.2025.1520207 · arXiv 2411.16204 | L0–L2 | D5 | P0/P2 | **PRE(실무증거)** | **8개 독일 국가센터의 유일한 공개 모니터링 비교표.** 100k–8M metric, 0.1–240s 간격. *"none of the German sites... using [ML] in production"* |
| PowerMorph: Shaping LLM Training for Data Center Demand Response | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00100 | L7 | D2 | P4 | REL `[A]` | 전력망 인지 운영 |
| DPS: Adaptive Power Management for Overprovisioned Systems | 2023 | SC23 | TRACK-UNKNOWN | sc23 pap474 | L7 | D1–D2 | P4 | PER | 공용 클라우드 평가. 제어 방법 |

## 2.8 Telemetry infrastructure & reduction

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems | 2020 | HPDC | ARCHIVAL | 10.1145/3369583.3392674, pp.101–112 · arXiv 1910.06156 | L0–L4 | D4–D5 | P3 | **PRE** | 아카이벌 문헌의 HPC ODA 참조 아키텍처. LRZ production. **프레임워크이지 분석 아님** |
| Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data | 2021 | IPDPS | ARCHIVAL | 10.1109/ipdps49936.2021.00010, pp.2–12 | L0/L1 | D2–D4 | P4 | **PRE** | **이 다섯 venue의 유일한 telemetry reduction 논문. 5년간 후속 없음** |
| Operational Data Analytics in Practice: Experiences from Design to Deployment | 2021/22 | Parallel Computing 113 | JOURNAL | arXiv 2106.14423 · S016781912200045X | L0–L4 | D5 | P3 | **PRE(실무증거)** | **SuperMUC-NG 6,000+노드, 14.5M 센서(6.8M raw), 10s, 2.5 TB Cassandra, 70만→6만 insert/s(~11.7배)**. *"insular ODA solutions"*, *"severe lack of end-to-end experiences"* |
| A Conceptual Framework for HPC Operational Data Analytics | 2021 | IEEE Cluster (HPCMASPA) | WORKSHOP-IN-PROC | 10.1109/cluster48925.2021.00086 | L0/L1 | — | — | PRAC | **ODA 정의 논문. taxonomy 인용용.** cross-site 검증 없음 |
| The Lightweight Distributed Metric Service (LDMS) | 2014 | **SC14** | ARCHIVAL | sandia.gov SC14_Final.pdf | L6 | D5 | P3 | **PRE** | 기질(substrate). **저오버헤드 주장의 원본이며 2014년 시스템 기준** |
| SIREN: Software Identification and Recognition in HPC Systems | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759873 | L0–L2 | D3–D4 | P4 | **PRE** | LUMI opt-in 배포. 실행파일 fuzzy hash로 "job 이름은 거짓말" 문제 해결 |
| Navigating Exascale Operational Data Analytics: From Inundation to Insight | 2024 | SC24 Workshops | WORKSHOP | 10.1109/SCW63240.2024.00226 | L6 | D5 | P3 | **PRE(실무증거)** | **센터가 실제로 무엇을 돌리는지에 대한 이 조사 최고의 논문.** 4.2–4.5 TB/day, 스트림 간 30만 배 |
| STREAM: A Scalable Federated HPC Telemetry Platform | 2023 | CUG (`venue UNVERIFIED`) | TECH-REPORT | OSTI 1995656 | L6 | D5 | P3 | PRAC | **1.3 TB/day, 300M msg/day, 223 topic, 20 PB/5년.** 데이터 축소는 임시방편 |
| Evaluating and Influencing Extreme-Scale Monitoring Implementations | 2023 | CUG | PAPER (CUG) | cug.org cug2023 pap149 | L6 | D5 | P3 | PRAC | **Perlmutter 100K–1M msg/s, Slingshot counter 취득 ~0.5s.** *"no statistically significant adverse effects"*를 **측정 없이 단언** ← 공략 지점 |
| Global Experiences with HPC Operational Data: Measurement, Collection and Analysis | 2019/2020 | ISC / IEEE Cluster(EE HPC SOP) | WORKSHOP-IN-PROC | 10.1109/cluster49012.2020.00071 · IEEE 9229593 | L6 | D5 | P3 | PRAC | **8~9개 top-50 센터가 실제로 무엇을 수집하는지.** 볼륨·rate·샘플링 간격은 정량화하지 않음 |
| Collecting, Monitoring, and Analyzing Facility and Systems Data at NERSC | 2019 | ICPP Workshops | WORKSHOP | 10.1145/3339186.3339213 | L6 | D5 | P3 | PRAC | OMNI. **522억 레코드 / 125 TB / 25,000 pts/s** |
| Event Management and Monitoring Framework for HPC Environments using ServiceNow and Prometheus | 2020 | MEDES '20 | ARCHIVAL | 10.1145/3415958.3433046 | L2/L5/L7(부분) | D5 | P1 | PRAC | **NERSC 규칙 기반 자동 remediation 워크플로 3종 — 이 조사 최강의 closed-loop 실무 증거** |
| PIKA: Center-Wide and Job-Aware Cluster Monitoring | 2020 | IEEE Cluster (HPCMASPA) | WORKSHOP-IN-PROC | 10.1109/cluster49012.2020.00061 | L0/L1 | D5 | P0/P1 | PRAC | TU Dresden. 핵심 ODA 인용 |
| Towards Real-Time Classification of HPC Workloads via Out-of-band Telemetry | 2022 | IEEE Cluster (HPCMASPA) | WORKSHOP-IN-PROC | 10.1109/cluster51413.2022.00078 | L2/L3 | D2 | P2 | REL(높음) | **out-of-band만으로 분류** — 사용자 job을 계측할 수 없는 센터에 매우 중요 |
| Sequence-RTG: Efficient and Production-Ready Pattern Mining in System Log Messages | 2021 | IEEE Cluster (HPCMASPA) | WORKSHOP-IN-PROC | 10.1109/cluster48925.2021.00090 | L2/L3 | D3 | P2 | REL | 로그 템플릿 마이닝, production-ready 프레이밍 |
| Monitoring Large Scale Supercomputers: A Case Study with the Lassen Supercomputer | 2021 | IEEE Cluster (main) | ARCHIVAL | 10.1109/cluster48925.2021.00057, pp.468–480 | L0–L2 | D4–D5 | P0–P2 | **PRE** `[A]` | **"만들었고 운영한다" 원형이 main track에 실렸다는 증거** |
| Bringing Differential Privacy to HPC: Privacy-Preserving Transformations of HPC Traces | 2025 | HPDC | ARCHIVAL | 10.1145/3731545.3731573 | L0 | D2 | P4 | REL `[A]` | **telemetry 공개 문제를 다루는 유일한 논문** |
| Sonata: Query-Driven Streaming Network Telemetry | 2018 | **SIGCOMM** | ARCHIVAL | 10.1145/3230543.3230555 | L1 | D1/D3 | P3 | **PRE(외부)** | ILP query partition + dynamic refinement. **3–7 자릿수 감소** |
| PINT: Probabilistic In-band Network Telemetry | 2020 | **SIGCOMM** | ARCHIVAL | arXiv 2007.03731 | L1 | D1 | P3 | **PRE(외부)** | 패킷당 hard bit budget + **증명된 bound**. 16 bit/packet이 full-INT 품질 |
| AutoSketch: Automatic Sketch-Oriented Compiler for Query-driven Network Telemetry | 2024 | **NSDI** | ARCHIVAL | usenix nsdi24spring_prepub_sun | L1 | D1 | P3 | REL(외부) | 정확도 목표 기반 sketch 선택 |
| The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems | 2023 | **NSDI**, pp.321–339 | ARCHIVAL | usenix | L0 | D1 | P3 | **PRE(외부)** | Retroactive sampling("dash-cam"). **axis C의 가장 중요한 선행** — trace 비용/커버리지는 풀었으나 다채널 telemetry는 아님 |
| Gorilla: A Fast, Scalable, In-Memory Time Series Database | 2015 | **PVLDB 8(12)** | ARCHIVAL | 10.14778/2824032.2824078 | L2 | D5 | P3 | REL(외부) | ~12배 압축. Prometheus/VictoriaMetrics/InfluxDB의 산업 기질. **무손실·하류 무관** |
| fKPISelect: Fault-Injection Based Automated KPI Selection for Multivariate Anomaly Detection | 2023 | ISSRE | ARCHIVAL | — | L3 | D2 | P2 | **REL(높음)** | ⚠ **"어떤 telemetry가 실제로 필요한가"에 가장 가까운 기존 논문. 과소인용 — 반드시 인용** |
| Hardware Telemetry at Scale: A Case Study on SSDs Endurance Monitoring in Datacenters | 2025 | DSN industry | ARCHIVAL | — | L0/L4 | D4 | P1 | REL | **telemetry 비용의 실제 사례 연구**(최적화 정식화는 아님) |
| PALLAS: A Generic Trace Format for Large HPC Trace Analysis | 2025 | IPDPS | ARCHIVAL | 10.1109/ipdps64566.2025.00032 | L0 | D1–D2 | P4 | REL `[A]` | trace 데이터 평면 |
| Pilgrim: Scalable and (Near) Lossless MPI Tracing | 2021 | SC21 | TRACK-UNKNOWN | sc21 pap177 | L0 | D1 | P4 | PER | **SC 본프로그램에서 telemetry 축소의 최근접 유사물 — 단, 시스템이 아니라 애플리케이션 tracing** |
| DFTracer / TraceFlow | 2024 / 2025 | SC24 / SC25 | TRACK-UNKNOWN | — / 10.1145/3712285.3759773 | L0–L1 | D1–D3 | P3–P4 | REL | trace 인프라 (동일 단서) |

## 2.9 Logs

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Exploring Hierarchical Patterns for Alert Aggregation in Supercomputers | 2024 | ISSRE (**Best Paper**) | ARCHIVAL | — (프로그램 검증) | L2→L3 | D2/D4 | P0 | **PRE** | **슈퍼컴퓨터 alert storm 축약이 ISSRE의 live topic임을 증명.** alert/event reduction 프레이밍의 직접 경쟁자 |
| Early Exploration of Using ChatGPT for Log-based Anomaly Detection on PFS Logs | 2023 | HPDC (short) | ARCHIVAL | 10.1145/3588195.3595943 | L3 | D1 | P1 | POT `[A]` | 이 5개 venue 최초의 LLM-for-HPC-logs. **short→full 승격 계보의 시작점** |
| ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection | 2022 | FTXS (SC) | WORKSHOP | IEEE FTXS 2022, pp.1–10 | L3 | D1 | P1–P2 | REL | 로그 템플릿 폭발 문제 직접 공략 |
| Heterogeneous Syslog Analysis: There Is Hope | 2023 | HPCSYSPROS (SC) | WORKSHOP | 10.1145/3624062.3624128 · 10.5281/zenodo.10223395 | L2–L3 | D2–D3 | P3 | **REL(매우 높음)** | LANL. **LLM vs 고전 분류기의 최초의 정직한 비교** — LLM이 더 설명가능하나 더 비쌈. 정량 지표 미보고 |
| Log-Based Identification, Classification, and Behavior Prediction of HPC Applications | 2020 | HPCSYSPROS (SC) | WORKSHOP | GitHub/Zenodo | L2/L4 | D2 | P3 | REL | ANL |
| Semantic-Aware Log Understanding and Analysis | 2024 | HPDC (short) | ARCHIVAL | 10.1145/3625549.3658830 | L3 | D1 | P1 | PRAC `[A]` | EU 프로젝트 세션 |
| LOGAIDER: A Tool for Mining Potential Correlations of HPC Log Events | 2017 | CCGrid (`UNVERIFIED`) | ARCHIVAL | IEEE 7973730 | L2 | D2 | P3 | REL | Mira/BG-Q RAS 로그의 시공간 상관. 고전 HPC log RCA |
| Log-based Anomaly Detection with Deep Learning: How Far Are We? | 2022 | **ICSE** | ARCHIVAL | arXiv 2202.04301 | — | — | — | **REL(경고)** | 현실적(비셔플·라벨잡음) 설정에서 딥 log AD가 붕괴 |
| A comprehensive study of machine learning techniques for log-based anomaly detection | 2025 | EMSE | JOURNAL | arXiv 2307.16714 | — | — | — | REL(경고) | 고전 ML이 종종 DL과 동등 |
| Impact of log parsing on deep learning-based anomaly detection | 2024 | EMSE | JOURNAL | 10.1007/s10664-024-10533-w | — | — | — | REL(경고) | **파서 선택이 모델 선택을 압도** |
| Drain: An Online Log Parsing Approach with Fixed Depth Tree | 2017 | ICWS | ARCHIVAL | 10.1109/ICWS.2017.13 | L0 | — | — | REL | 이 분야 기본 템플릿 추출기. ISSRE 2024–25 LLM 파서 논문의 baseline |
| CFseq: A Framework for Constructing Compression-Friendly Field Sequences for Network Logs | 2025 | IEEE Cluster | ARCHIVAL | 10.1109/cluster59342.2025.11186454 | L0 | D1–D2 | P4 | POT `[A]` | 로그 데이터 축소 |

## 2.10 LLM & agents

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Large Language Models for Anomaly Detection in Computational Workflows: SFT to ICL | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00098 · arXiv 2407.17545 | L3(+L5) | D1–D2 | P4 | **PRE** | **SC 본프로그램 최초의 LLM 이상탐지 논문.** workflow 수준, 벤치마크 데이터셋 한정 |
| STELLAR: Storage Tuning Engine Leveraging LLM Autonomous Reasoning for PFS | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759887 | L6→L7 | D3 | P4 | **PRE** | agentic 루프(파라미터 추출→trace 분석→전략→재실행→피드백). **~5회 시도로 근최적 설정** |
| KORAL: Knowledge Graph Guided LLM Reasoning for SSD Operational Analysis | 2026 | IPDPS | ARCHIVAL | 10.1109/ipdps65963.2026.00085 | L5/L6 | D2 | P4 | **PRE** `[A]` | **2026 프런티어: LLM + 구조화된 운영 지식** |
| Automatic Root Cause Analysis via Large Language Models for Cloud Incidents (RCACopilot) | 2024 | **EuroSys** | ARCHIVAL | 10.1145/3627703.3629553 · arXiv 2305.15778 | L5/L6 | D4 | P4 | **PRE(외부)** | **653 인시던트, Micro-F1 0.766 / Macro-F1 0.533, 4.2s. 수집 컴포넌트는 30팀 4년+.** 진짜 기여는 LLM이 아니라 handler 기반 증거수집 아키텍처 |
| Recommending Root-Cause and Mitigation Steps for Cloud Incidents using LLMs | 2023 | **ICSE** | ARCHIVAL | 10.1109/ICSE48619.2023.00149 · arXiv 2301.03797 | L5/L6 | D2/D4 | P4 | **PRE(외부)** | 4만+ Microsoft 인시던트. 장르를 확립 |
| L4: Diagnosing Large-scale LLM Training Failures via Automated Log Analysis | 2025 | **FSE Companion** | ARCHIVAL | 10.1145/3696630.3728531 | L5 | D4 | P3 | **PRE(외부)** | **428건 실제 장애, 평균 941 accelerator, 평균 진단 34.7h(41.9%는 24h 초과). F1 0.873. 진단 경로에 LLM 미사용** ← 최강 anti-LLM 논거 |
| AIOpsLab: A Holistic Framework to Evaluate AI Agents for Enabling Autonomous Clouds | 2025 | arXiv (MSR) | PREPRINT/BENCHMARK | arXiv 2501.06706 | L3–L7 | D1 | P4 | **REL(외부)** | agentic-ops 주장의 평가 기준. **HPC 등가물 없음** |
| ITBench: Evaluating AI Agents across Diverse Real-World IT Automation Tasks | 2025 | arXiv; ICML poster | BENCHMARK | arXiv 2502.05352 | L3–L7 | — | — | **REL(외부)** | 94 시나리오. **SOTA agent: SRE 13.8% / CISO 25.2% / FinOps 0%** |
| OpsEval: A Comprehensive Benchmark Suite for Evaluating LLMs in IT Operations | 2025 | **FSE** | ARCHIVAL | 10.1145/3696630.3728572 · arXiv 2310.07637 | — | — | — | REL(외부) | 이중언어 IT-ops LLM 벤치마크 |
| How Far Can Root Cause Analysis Go on Real-World Telemetry Data? | 2026 | arXiv 2607.13548 | PREPRINT | arXiv 2607.13548 | L4 | D1 | P3 | **REL(핵심경고)** | **고전 causal discovery(Granger/PC/FCI/LiNGAM/NTLR) 전부 Acc@1 0%.** 최고 LLM 시스템 25.71%. **실패의 65.7%가 reasoning gap** |
| EPIC: Generative AI Platform for Accelerating HPC Operational Data Analytics | 2025 | arXiv 2509.16212 | PREPRINT | arXiv 2509.16212 | L5 | D4 | P3 | REL | **Frontier 50만 job 로그, 배포된 챗봇.** 서술적 분석 26% 정확도 향상, LLM 비용 19배 절감. routing F1 0.77, hallucination 0.33. **RCA 안 함** |
| LLM Agents for Interactive Workflow Provenance: Reference Architecture and Evaluation Methodology | 2025 | SC25 Workshops | WORKSHOP | 10.1145/3731599.3767582 · arXiv 2509.13978 | L5/L6 | D1/D2 | P1 | REL | **DOE 랩의 LLM-agent-for-HPC-data 최근접 연구 — 그리고 workshop 논문이다** |
| FRAGATA: Semantic Retrieval of HPC Support Tickets via Hybrid RAG over 20 Years of RT History | 2026 | Jornadas SARTECO (지역학회) | REGIONAL | arXiv 2604.13721 | L6 | D4 | P3 | PRAC | CESGA 배포. **저자가 정량 평가 없음을 자인** |
| Generating FAQs from Technical Support Tickets using LLMs | 2025 | SC25 Workshops | WORKSHOP | 10.1145/3731599.3767429 | L6 | D2 | P2 | PRAC | HPC 티켓 → FAQ |
| TicketHub: Enabling Actionable Analysis of Support Requests With NLP | 2023 | PEARC | ARCHIVAL(practice) | 10.1145/3569951.3604397 | L1/L5 | D3 | P3 | PRAC | HPC 지원 요청 NLP |
| Large Language Models Can Provide Accurate and Interpretable Incident Triage | 2024 | ISSRE | ARCHIVAL | — | L5/L6 | D2/D4 | P4 | REL(외부) | Microsoft |
| AetherLog: Log-based RCA by Integrating LLMs with Knowledge Graphs | 2025 | ISSRE | ARCHIVAL | — | L5 | D2 | P3 | REL(외부) | LLM+KG |
| What Artificial Intelligence can do for High-Performance Computing systems? | 2025/26 | arXiv 2602.00014 | SURVEY | arXiv 2602.00014 | — | — | — | **REL(gap 근거)** | ~1,800편 스크리닝→74편. *"There is no documented evidence of production-level deployment to date"*, *"without shared benchmarks"* |
| Literature study on Operational Data Analytics frameworks in large-scale computing infrastructures | 2026 | arXiv 2603.19016 | SURVEY | arXiv 2603.19016 | L0–L4 | D3 | P4 | **REL(gap 근거)** | 10개 production ODA 프레임워크 조사. **LLM 통합 0건**, closed-loop *"partially manual"* |

## 2.11 Cross-system generalization & AIOps 방법론

| Title | Yr | Venue | type | DOI/URL | SC | 한 줄 |
|---|---|---|---|---|---|---|
| MetaLog: Generalizable Cross-System Anomaly Detection from Logs with Meta-Learning | 2024 | **ICSE** | ARCHIVAL | 10.1145/3597503.3639205 | **REL(차단)** | cross-system log AD의 정본. **이 lane은 닫혔다** |
| Cross-System Software Log-based Anomaly Detection Using Meta-Learning (CroSysLog) | 2024 | arXiv 2412.15445 | PREPRINT | arXiv 2412.15445 | **REL(차단)** | BGL 4.7M / Thunderbird 211M / Liberty 265M / Spirit 272M. **F1 97.6–99.2%**. 저자 자인: *"only evaluated on supercomputing systems with open datasets"*, 배포·ROI 없음 |
| ZeroLog: Zero-Label Generalizable Cross-System Log-based Anomaly Detection | 2025 | ISSRE | ARCHIVAL | arXiv 2511.05862 | REL(차단) | target label 0으로 |
| LogTransfer: Cross-System Log Anomaly Detection with Transfer Learning | 2020 | ISSRE | ARCHIVAL | — | REL | 이 계열의 초기 |
| Share or Not Share? Towards the Practicability of Deep Models for Unsupervised AD | 2022 | ISSRE (Best Paper Cand.) | ARCHIVAL | — | REL | **"하나의 모델이 여러 시스템을 담당할 수 있는가"를 정확히 물음** |
| Prepared for the Unknown: Adapting AIOps Capacity Forecasting Models to Data Changes | 2025 | ISSRE | ARCHIVAL | — | REL | AIOps 모델의 명시적 concept drift 적응 |
| EvLog: Identifying Anomalous Logs over Software Evolution | 2023 | ISSRE | ARCHIVAL | — | REL | 소프트웨어 버전 간 drift |
| An Empirical Study of the Impact of Data Splitting Decisions on AIOps Solutions | 2021 | **ACM TOSEM** | JOURNAL | 10.1145/3447876 | **REL(치명)** | ⚠ **랜덤 분할이 AIOps 결과를 부풀린다. 시간순 분할을 쓰지 않으면 이 논문 하나로 심사에서 죽는다** |
| Towards a Consistent Interpretation of AIOps Models | 2021 | ACM TOSEM | JOURNAL | 10.1145/3488269 | REL | 해석 불안정성 |
| On the Model Update Strategies for Supervised Learning in AIOps Solutions | 2024 | ACM TOSEM | JOURNAL | 10.1145/3664599 | REL | **재학습 비용이 이미 체계적으로 연구됨** |
| Can we recycle our old models? Model selection mechanisms for AIOps solutions | 2026 | EMSE | JOURNAL | 10.1007/s10664-026-10834-2 | REL | 모델 재사용 경제학 |
| Is Your Anomaly Detector Ready for Change? Adapting AIOps Solutions to the Real World | 2023 | arXiv 2311.10421 | PREPRINT | arXiv 2311.10421 | REL | drift 탐지 + 적응 |
| SeT-Diff: Towards Semantic Foundation Models for HPC Telemetry and Time-Series | 2026 | **ACM Computing Frontiers** | ARCHIVAL | arXiv 2607.22548 | **REL(핵심)** | **M100 20개월/261 metric.** Sentence-BERT 센서 설명 임베딩으로 위치 인덱스 취약성 공략. **cross-system/cross-generation 전이를 평가하지 않는다고 명시** |
| CENTILE: A Telemetry Foundation Model Evaluated by the Decisions It Drives | 2026 | arXiv 2608.01725 | PREPRINT | arXiv 2608.01725 | **REL(위협)** | **의사결정 가치로 평가하는 프레이밍이 이 문헌 최고.** zero-shot 개월 전이, 도메인 간 가중치 전이, mean bounded slowdown 최대 77% 감소. **telemetry 비용 미고려** |
| Towards Practical Machine Learning Frameworks for Performance Diagnostics in Supercomputers | 2023 | AI4Sys (ISC) | WORKSHOP | bu.edu/peaclab AI4Sys_Workshop-1.pdf | **REL(핵심수치)** | ⚠ **이 축의 유일한 측정치: generic model F1 0.726 vs node-specific 0.898 — 한 시스템의 노드 간 0.17 격차.** 3쪽 워크숍 논문 |
| HPC ODA Commons: Community-Governed Contracts and Toolkit for Reproducible ODA | 2026 | **PEARC** | ARCHIVAL(practice) | 10.1145/3785462.3815891 | **REL(확인필수)** | ⚠ schema 이질성을 정면으로. **내용 `INSUFFICIENT_EVIDENCE`(403). 데이터셋 공개 계획이 있다면 먼저 읽을 것** |

## 2.12 Remediation & closed loop

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| Predictive and Adaptive Failure Mitigation to Avert Production Cloud VM Interruptions (Narya) | 2020 | **OSDI**, pp.1155–1170 | ARCHIVAL | usenix osdi20/presentation/levy | L4+L6+L7 | **D5** | P4 | **PRE(외부·최강 falsifier)** | **Azure 15개월, VM 중단 26% 감소.** 예측 + bandit/RL 온라인 실험으로 조치 선택 |
| SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation | 2024 | **USENIX ATC (Best Paper)** | ARCHIVAL | arXiv 2402.06194 · TOCS 10.1145/3767334 | L2+L3+L6+L7 | **D5** | P4 | **PRE(외부·최강 falsifier)** | **수십만 GPU 2년. Selector가 검증 비용 대 탐지 이득 명시 최적화. MTBI 최대 22.61배** |
| Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems | 2023 | **FAST** | ARCHIVAL | usenix fast23/presentation/lu | L3/L5/L7 | D4/D5 | P4 | **PRE(외부)** | 24.8만 드라이브 10개월, fail-slow 304건, **p99.99 48% 감소, 라벨링 데이터셋 공개** |
| IASO: A Fail-Slow Detection and Mitigation Framework for Distributed Storage Services | 2019 | **USENIX ATC** | ARCHIVAL | usenix | L3+L7 | D5 | P4 | **PRE(외부)** | 3.9만 노드 1.5년+. **peer 비교 slow-node 탐지는 production-solved — 기여로 삼을 수 없음** |
| Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems | 2018 | **FAST** + ACM TOS 14(3) | ARCHIVAL | 10.1145/3242086 | L5 | D1/D2 | P4 | **PRE(외부)** | 101건 인시던트 보고서, 16개 기관 **LANL·ANL 포함** → **"HPC의 fail-slow는 미연구"라고 쓸 수 없음** |
| ARGUS: Production-Scale Tracing and Performance Diagnosis for over 10,000-GPU Clusters | 2026 | arXiv (venue 미기재) | PREPRINT | arXiv 2606.20374 | L5 | D4 | P3/P4 | **PRE(외부·최강 falsifier)** | **>1만 GPU 6개월 상시, <2% overhead, 커널이벤트 3700배 압축, progressive 다중원인 판별.** 동기·반복·동질 학습 job 전제 |
| FALCON: Pinpointing and Mitigating Stragglers for Large-Scale Hybrid-Parallel Training | 2024 | arXiv 2410.12588 | PREPRINT | arXiv 2410.12588 | **L7** | **D5** | P3 | **PRE(외부)** | >1만 GPU production. 사람 개입 없는 다단계 완화, **저하 60.1% 감소** |
| LLMPrism: Black-box Performance Diagnosis for Production LLM Training Platforms | 2025 | DSN industry / arXiv | ARCHIVAL/PREPRINT | arXiv 2505.00342 | L5 | D4 | P3 | **PRE(외부)** | **네트워크 flow만으로** job별 학습 timeline 재구성(계측 없이). 0.3% 오차 |
| Understanding Stragglers in Large Model Training Using What-if Analysis | 2025 | arXiv 2505.05713 (venue `UNVERIFIED`) | PREPRINT | arXiv 2505.05713 | L5 | D2 | P3 | REL(외부) | **ByteDance 5개월 trace.** counterfactual what-if로 straggler 영향 정량화 |
| Don't Predict, Prioritize: Rethinking GPU Reliability Assessment (HeaRank) | 2026 | **KDD 2026** | ARCHIVAL | arXiv 2607.15115 | L4→L6 | D4 | P3 | **REL(외부)** | **GPU 장애 *시점*은 예측 불가**(DBE, GPU-Lost는 확률적)라고 주장하고 learning-to-rank로 대체. AUC 0.83, 상위 5%에 장애 64%(기존 21%) |
| Frontier node health checking and state management | 2023 | CUG | PAPER (CUG) | cug.org cug2023 pap151 | L7(규칙) | **D5** | P4 | **PRAC(핵심 baseline)** | **실제로 돌아가는 것.** 685 blade/~6,000만 컴포넌트, MTBF *시간* 단위. **정확도 수치 0.** 안전장치: 자기가 설정한 이유일 때만 자동 resume |
| Multi-stage Approach for Identifying Defective Hardware in Frontier | 2024 | CUG | PAPER (CUG) | cug.org cug2024 pap123 | L3 | D5 | P3 | **PRAC(핵심)** | **약 600만 테스트 누적, 6개월 190만, 고유 실패노드 99개, LAMMPS 1/14,618. 주간 스크린 39,437회 무수확 후 폐기** |
| Orchestrating Fault Prediction with Live Migration and Checkpointing | 2020 | HPDC | ARCHIVAL | 10.1145/3369583.3392672 | L7 | **D0/D1** | P0 | REL(경고) | **순수 SimPy 시뮬레이션이며 예측 정확도를 가정한다.** HPC 계보가 production에 도달하지 못한 증거 |
| Proactive Process-Level Live Migration in HPC Environments | 2008 | **SC08** | ARCHIVAL | 10.5555/1413370.1413414 | L7 | D1 | P1 | REL | HPC proactive migration 계보의 시조 |
| Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field | 2024 | HPDC, pp.240–252 | ARCHIVAL | 10.1145/3625549.3658686 | L4→L7 | D3–D5 | P3/P4 | **PRE** `[A]` | **HPDC/IPDPS/Cluster ~700건 중 사실상 유일한 L7/D5.** 예측→행동. **운영진이 공저자** |
| Can We Trust Auto-Mitigation? Improving Cloud Failure Prediction with Uncertain Positive Learning | 2024 | ISSRE | ARCHIVAL | — | L4+L7 | **D5** | P2 | **REL(경고)** | ⚠ **closed-loop 배포가 ground-truth label을 파괴한다.** "닫힌 루프가 평가를 깬다"도 이미 선점 |
| Safe Remediation as Risk-Constrained Intervention Decision in Microservice Systems | 2026 | arXiv 2607.20005 | PREPRINT | arXiv 2607.20005 | L6/L7 | ? | ? | **REL(확인필수)** | ⚠ **"safe remediation" 정식화의 최근접 명명. 내용 `UNVERIFIED`. F축 프레이밍을 선점했을 수 있다 — 먼저 읽을 것** |
| Just-In-Time Checkpointing: Low Cost Error Recovery from DL Training Failures | 2024 | **EuroSys** | ARCHIVAL | — | L7 | D3/D4 | P2 | REL(외부) | 결정론을 이용해 장애 탐지 시에만 체크포인트 |
| Unicron: Economizing Self-Healing LLM Training at Scale | 2024 | arXiv 2401.00134 | PREPRINT | arXiv 2401.00134 | L7 | D3/D4 | P2/P3 | REL(외부) | in-band 오류탐지 + 비용인지 재구성 |
| FIRM: An Intelligent Fine-grained Resource Management Framework for SLO-Oriented Microservices | 2020 | **OSDI**, pp.805–825 | ARCHIVAL | usenix | L3+L5+L7 | D1/D3 | P3 | **REL(외부·경고)** | ⚠ **"어느 저수준 자원이 병목인지 식별하고 조치한다"는 이미 OSDI 2020 결과다** |
| Dynamic Login Node Resource Control and Monitoring with Arbiter 3 | 2024 | HPCSYSPROS (SC) | WORKSHOP | 10.5281/zenodo.16541343 | **L7** | **D5** | P3 | **REL(높음)** | **production 배포된 closed-loop 강제 시행. 아카이벌 평가가 없다 — 준비된 논문** |
| Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems | 2025 | SC25 | TRACK-UNKNOWN | 10.1145/3712285.3759883 | **L7** | **D5** | P3/P4 | **PRE** | Aurora 10,624노드/63,744 GPU. **MTTR 최대 84배 감소. census 전체 유일의 진짜 L7/D5** |

## 2.13 Digital twin · counterfactual 평가

| Title | Yr | Venue | type | DOI/URL | L | D | P | SC | 한 줄 |
|---|---|---|---|---|---|---|---|---|---|
| A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale (ExaDigiT) | 2024 | SC24 | TRACK-UNKNOWN | 10.1109/SC41406.2024.00029 | L4+L6 | D3–D4 | P4 | **PRE** | **Frontier 6개월 telemetry replay V&V.** 오픈소스. 물리는 풀렸고 정책 평가 방법론은 공백 |
| Towards the Development of an Exascale Network Digital Twin | 2024 | CUG | PAPER (CUG) | cug.org cug2024 pap140 | L4 | D1 | P1 | PRAC(핵심) | ⚠ **시간척도 벽: 스위치 100–350 ns vs telemetry 15초.** 단일 rank replay >30h. **정확도 수치 없음** |
| Causality inference for Digital Twins in GPU Data Centers and Smart Grids | 2025 | CUG | PAPER (CUG) | cug.org cug2025 pap118 | L5 | D2 | P2 | PRAC(핵심) | ⚠ **Summit 3년 27,648 GPU 모니터링 → 사용가능 장애 데이터 127건.** mTE *"did not produce significant results"*, CCM은 127 레코드로 굶음 |
| From Exploration to Explanation: ML-Driven Causal Discovery for Datacenter Reliability (PACE) | 2025 | SC25 Workshops | WORKSHOP | 10.1145/3731599.3767471 | L6 | D2 | P3 | REL(높음) | HPE/ORNL. **HPC venue에서 유일한 명시적 cross-layer causal discovery.** Granger 기반, job 성능 미접촉 |
| A Fast Simulator to Enable HPC Scheduling Strategy Comparisons | 2023 | MODA (ISC) | WORKSHOP | 10.1007/978-3-031-40843-4 (pp.320–333) | L6 | D1 | P2 | REL(높음) | **"production 기계에서 스케줄링 정책을 A/B 테스트할 수 없다"는 메타 문제를 정면으로.** 시뮬레이터 충실도 미검증 |

---

# 3. PERIPHERAL / 참고만

제외 사유별로 묶는다. **논문 수 채우기용으로 census에 넣지 않았다.**

| 논문/그룹 | 제외 사유 |
|---|---|
| ScalAna (SC20), Thicket (HPDC'23), Timemory, GVProf/DrCCTProf/ZeroSpy, Paraver/NSYS2PRV, MemGaze | **애플리케이션 프로파일링** — 진단 방법은 유용하나 운영 telemetry가 아니다 |
| Metis (SC20), Workload Intelligence (SC25), Alioth (IPDPS'23), MAAD (IPDPS'24), FEDGE (IPDPS'24), DDRM, TRACE, GreenK8s, RPTCN, AuTraScale, AlphaR | **클라우드/마이크로서비스 전용** — 단, novelty falsification용 closest work로는 유효 |
| ANT-Man, Alita, Waiting Game, PRESTO, ENSURE, FaaSRank, Understanding/Predicting Serverless Workloads (SC21) | 클라우드 자원관리 |
| HammingMesh, PolarFly, Uno (SC25), Q-adaptive, RELAR | **토폴로지·혼잡제어 *설계*이지 진단이 아님** |
| Runtime-Guided ECC, Unity ECC, COMET, Structural Coding, Druto, Aspis, MILR, PolygraphMR, DLAFI | **아키텍처 resilience / fault injection** — 운영 데이터와 무관 |
| Exploring and Mitigating Failure Behavior of LLM Training Workloads (SC25), Demystifying the Resilience of LLM Inference (SC25) | **fault injection 기반**(30만+ 주입 실험) — 필드 데이터의 정반대 방법론 |
| Chronicles of Astra (SC20), TOSS-2020 (SC20), Iris (SC20), NRE Best Practices (SC21), Frontier: Exploring Exascale (SC23), Fire-Flyer AI-HPC (SC24), JUPITER Benchmark Suite (SC24), ChatHPC (SC25), HPL on Exascale (SC25) | **PRACTICE-ONLY.** 단, **SC SotP 트랙의 형식 선례로서는 매우 중요** — `03` §3.3 참조 |
| Mapping Out the HPC Dependency Chaos (SC22), Minimizing Privilege for HPC Containers (SC21) | 소프트웨어 스택 연구 |
| GUFI (SC22), Xfast (SC23), Lunule | 운영 스토리지 툴링 — PRACTICE/RELEVANT 경계 |
| ACSOS 2020–2025 main track 전체 | ⚠ **6개 판(edition) 전체에서 슈퍼컴퓨터·배치 스케줄러·병렬 파일시스템으로 평가된 main-track 논문 0편.** MAPE-K, self-adaptation, uncertainty, causal RCA의 **개념적 프레이밍으로만** 인용할 것. 개별 유용 항목: Causal Inference Techniques for Microservice Performance Diagnosis (2021, `10.1109/acsos52086.2021.00029`), On Evaluating Self-Adaptive and Self-Healing Systems using Chaos Engineering (2022, `.00018`), Prolego (2023, `.00025`), ClearCausal (2024, `.00039`), **Uncertainty-Driven Monitoring for ML-Based Autonomic Systems (2025, `.00021`)** ← 2025년 가장 이식성 높은 아이디어 |

---

# 4. Workshop / CUG / practice 항목

> **아카이벌 증거와 절대 섞지 말 것.** 상세는 `04_WORKSHOP_AND_CUG_CASES.md`.

## 4.1 Workshop 최강 20편 (요약)

| # | Title | Yr | Workshop | type | DOI/URL | L | D | P | SC |
|---|---|---|---|---|---|---|---|---|---|
| 1 | An Operational Data Collecting and Monitoring Platform for Fugaku | 2021 | MODA | WORKSHOP | 10.1007/978-3-030-90539-2_24 | L0–L1 | D4 | P3 | **높음** — **15만+ 노드 전 metric sweep <20초**. exascale telemetry 규모 baseline |
| 2 | An Explainable Model for Fault Detection in HPC Systems | 2021 | MODA | WORKSHOP | 10.1007/978-3-030-90539-2_25 | L3 | D2 | P3 | 높음 (RUAD로 승격) |
| 3 | Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems | 2022 | MODA | WORKSHOP | 10.1007/978-3-031-23220-6_18 | L2–L3 | D3 | P3 | **높음** — 실제 열 비상사태로 검증 |
| 4 | Automatic Detection of HPC Job Inefficiencies at TU Dresden with PIKA | 2023 | MODA | WORKSHOP | 10.1007/978-3-031-40843-4_22 | L2–L3 | D4 | P4 | **매우 높음** — **5년+ production. 코퍼스 최강의 미승격 논문** |
| 5 | ML-Based Methodology for HPC Facilities Supervision | 2023 | MODA | WORKSHOP | 10.1007/978-3-031-40843-4_23 | L1–L3 | D2 | P2 | 중간 |
| 6 | A Fast Simulator to Enable HPC Scheduling Strategy Comparisons | 2023 | MODA | WORKSHOP | 10.1007/978-3-031-40843-4 pp.320–333 | L6 | D1 | P2 | **높음** — counterfactual 평가 메타문제 |
| 7 | Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository | 2024 | MODA | WORKSHOP(short) | 10.1007/978-3-031-73716-9 pp.287–292 | L0–L1 | D3 | P3 | 중~높음 (거버넌스) |
| 8 | An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads | 2024 | MODA | WORKSHOP | 10.1007/978-3-031-73716-9 pp.273–286 | L0 | D1 | P0 | **높음** — **스케줄러를 피시험 시스템으로 다룬 유일한 논문** |
| 9 | Supporting HPC Users with LLview | 2025 | MODA | WORKSHOP | 10.1007/978-3-032-07612-0_4 | L1–L2 | D4 | P3 | **매우 높음** — JUWELS production, role-based. **행동 변화 측정이 빠진 것이 곧 논문** |
| 10 | A Unified I/O Monitoring Framework Using eBPF | 2025 | MODA | WORKSHOP | 10.1007/978-3-032-07612-0_3 | L0–L1 | D4 | P3 | **매우 높음** — Darshan이 못 보는 AI 워크로드 |
| 11 | Duration-Informed Workload Scheduler | 2025 | MODA | WORKSHOP | 10.1007/978-3-032-07612-0_1 | L4→L6 | D2 | P2 | 높음 — 평균 대기 ~11%↓, 시뮬레이션만 |
| 12 | What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years | 2025 | MODA | WORKSHOP | 10.1007/978-3-032-07612-0_5 | L1 | D3 | P4 | **높음** — **코퍼스 유일의 다년 종단 연구**(4년+, 500+ 사용자) |
| 13 | Heterogeneous Syslog Analysis: There Is Hope | 2023 | HPCSYSPROS | WORKSHOP | 10.1145/3624062.3624128 · zenodo 10223395 | L2–L3 | D2–D3 | P3 | **매우 높음** — LLM 운영 로그 triage의 유일한 HPC 데이터점 |
| 14 | Advancing ODA Standardization Through an Open Source Dashboard | 2024 | HPCSYSPROS | WORKSHOP | 10.5281/zenodo.15724831 | L1 | D3 | P3 | 높음 — 8년 표준화 논의의 유일한 구체 산출물 |
| 15 | Experiences Detecting Defective Hardware in Exascale Supercomputers | 2023 | HPCTESTS | WORKSHOP | SC23 Workshops (article ID `UNVERIFIED`) | L2–L3 | D4 | P3 | **매우 높음** — silent defect 문제의 결정적 실무 진술 |
| 16 | Toward Collaborative Continuous Benchmarking for HPC | 2023 | HPCTESTS | WORKSHOP | SC23 Workshops | L0–L1 | D2 | P2 | 높음 |
| 17 | An Automated Approach to Continuous Acceptance Testing of HPC Systems at NERSC | 2022 | HPCSYSPROS | WORKSHOP | Zenodo (DOI `UNVERIFIED`) | L2 | D4 | P3 | 높음 |
| 18 | Dynamic Login Node Resource Control and Monitoring with Arbiter 3 | 2024 | HPCSYSPROS | WORKSHOP | 10.5281/zenodo.16541343 | **L7** | **D5** | P3 | **높음** — 아카이벌 평가가 없는 production closed-loop |
| 19 | From Failure to Insight: Analyzing Disk Breakdowns in Large-Scale HPC Environments | 2024 | FTXS | WORKSHOP | IEEE SC-W 2024 (article ID `UNVERIFIED`) | L3–L5 | D2 | P3 | **높음** — **HPC 디스크 신뢰성은 2020년 이후 아카이벌 논문 없음** |
| 20 | ClusterLog: Clustering Logs for Effective Log-based Anomaly Detection | 2022 | FTXS | WORKSHOP | IEEE FTXS 2022 pp.1–10 | L3 | D1 | P1–P2 | 중~높음 |

## 4.2 CUG 핵심 artifact

| Title | Yr | Form | URL | 무엇이 증거인가 |
|---|---|---|---|---|
| Multi-stage Approach for Identifying Defective Hardware in Frontier | 2024 | **[PAPER]** | cug2024 pap123 | **코퍼스 최강 정량 운영 논문.** 190만 테스트/99 노드/1:14,618/39,437 무수확 |
| Evaluating and Influencing Extreme-Scale Monitoring Implementations | 2023 | **[PAPER]** | cug2023 pap149 | 100K–1M msg/s 실패, Slingshot 0.5s/switch, "no significant penalty" 무근거 단언 |
| STREAM: A Scalable Federated HPC Telemetry Platform | 2023 | **[PAPER]** | cug2023 pap155 · OSTI 1995656 | 1.3 TB/day, 20 PB/5년, schema drift |
| Frontier Node Health Checking and State Management | 2023 | **[PAPER]** | cug2023 pap151 | **실제 production baseline. 정확도 수치 0** |
| EMOI: CSCS Extensible Monitoring and Observability Infrastructure | 2024 | **[PAPER]** | cug2024 pap113 | job 에너지 5,663,156 J vs Slurm 5,662,307 J; *"Slurm... cannot always be trusted"* |
| CADDY: Scalable Summarizations over Voluminous Telemetry Data | 2024 | **[PAPER][VENDOR]** | cug2024 pap112 | **유일하게 알고리즘+정량평가를 갖춘 벤더 artifact.** 425×/600×/1200× 압축, ingest +32.5%, 단일노드 testbed |
| Towards the Development of an Exascale Network Digital Twin | 2024 | **[PAPER]** | cug2024 pap140 | ns↔15s 시간척도 벽 |
| Nine Months in the life of an all-flash file system | 2024 | **[PAPER]** | cug2024 pap141 | 느린 OST 25–50%↓, 15.1→19.9 GB/s, checksum −17% |
| Causality inference for Digital Twins in GPU Data Centers and Smart Grids | 2025 | **[PAPER]** | cug2025 pap118 | 3년/27,648 GPU → **127 레코드**; mTE 실패 |
| Monitoring HPE Cray HPC systems (tut106) | 2025 | **[TUTORIAL][VENDOR]** | cug2025 tut106 | **HPCM 1.13 스택의 사실상 공개 명세.** 보존 기본값 |
| Monitoring and characterizing GPU usage | 2023 | **[PAPER]** | cug2023 pap139 | DCGM *"too intrusive"* 거부; **GPU util 평균 11%, 53%가 GPU 미사용** |
| Automated service monitoring in the deployment of ARCHER2 | 2022 | **[PAPER]** | cug2022 pap103 · CC:P&E 10.1002/cpe.7892 | **HPL 16.8 → 19.5 PF**; Graphite downsampling 후회 |
| AIOps: Leveraging AI/ML for Anomaly Detection in System Management | 2021 | **[PAPER][VENDOR]** | **PDF 미게시** | ⚠ 가장 많이 인용되는 HPE AIOps CUG artifact가 **공개 열람 불가** |
| trellis — An Analytics Framework for Understanding Slingshot Performance | 2021 | **[PAPER][VENDOR]** | cug2021 pap115 | 30일 raw telemetry *"several petabytes"*. ML은 future work, 정량평가 없음 |
| Large-Scale System Monitoring Experiences and Recommendations | 2018 | **IEEE Cluster** | 10.1109/cluster.2018.00069 | ⚠ **CUG 모니터링 커뮤니티 자신의 아카이벌 크로스오버 — CUG 실무를 peer-review 기여로 전환한 최고의 선례** |

---

# 5. 공개 데이터셋 목록

| 데이터셋 | 규모 / 범위 | 라이선스·접근 | DOI/URL | 최적 용도 | 한계 |
|---|---|---|---|---|---|
| **M100 ExaData** (CINECA Marconi100) | **49.9 TB, 934일(2020-03~2022-09), 573 metric @1s, 980+ 노드.** IPMI + Slurm + **Nagios label** + Ganglia + facility(cooling/CRAC/PSU/weather). Parquet/zstd, PyArrow API | **CC-BY-4.0**, 12개 Zenodo DOI | 10.1038/s41597-023-02174-3 · zenodo.org/records/10533504 · gitlab.com/ecs-lab/exadata | **노드 이상탐지, 열/전력 예측, facility↔IT 상관.** 센서→facility 전 스택을 아우르는 유일한 데이터셋. **C1 decimation 실험의 이상적 기반** | Nagios label이 15분 입도(그 위 분류기 **AUC 0.57**); 사용자 완전 익명화; 1세대(V100) |
| **F-DATA** (Fugaku) | **약 2,400만 job, 2021-03~2024-04, 45 feature, 28 GB, 38 월별 Parquet.** per-component power(min/avg/max), performance counter, exit code | Zenodo | 10.5281/zenodo.11467483 · 10.1038/s41597-025-05633-1 | **현존 최대 라벨링 job 코퍼스.** job 전력 예측, 실패/exit-code 예측, 런타임 추정, memory/compute-bound 분류. **C2의 두 번째 아키텍처** | A64FX 특화(전이성 불명); **21M 성공 vs 2.5M 실패 불균형**; 원본은 RIKEN 독점 |
| **HPC-ODA Dataset Collection** (LRZ) | 1.5 GB, **5개 task segment**(power prediction, fault detection, application classification, infrastructure management, cross-architecture). DCDB + LDMS, 복수 production 시스템 | **CC-BY-4.0** | 10.5281/zenodo.3701440 | **데이터 덤프가 아니라 ODA ML 벤치마크로 설계된 유일한 것.** 방법 비교의 출발점 | 작다(1.5 GB) |
| **OLCF Constellation — Summit power/thermal** | 1 Hz 원시, **10초/1분 평균으로 공개**, 3년에 걸친 5개월(2020-01·08, 2021-02·08, 2022-01), 9,252 CPU + 27,756 GPU | Constellation T&C (Globus). **개방 라이선스 아님 — 파생물 공개 전 확인** | 10.13139/OLCF/1861393 · github.com/at-aaims/summit_power_and_thermal_data | 전력/열 모델링, facility 결합 | 연속 기간이 아님 |
| **OLCF Constellation — Summit GPU DBE snapshots** | 27,648 V100. **NVIDIA XID 장애 기록 + 노드 재부팅 로그 + 스케줄러 기록 + 1 Hz BMC metric** | Constellation T&C | 10.13139/OLCF/1970187 | ⭐ **유일한 공개 GPU-failure-with-telemetry-context 데이터.** GPU 장애 예측·RCA에 직접 사용 가능 | 접근 조건 확인 필요 |
| **OLCF Frontier HPL power** | Top500/Green500 제출 데이터 | OSTI | OSTI 1975494 | 전력 벤치마킹 | 단일 실행 |
| **NREL Eagle supercomputer jobs** | **1,100만+ job, 2018-11~2023-02**, CSV.bz2 + Parquet, 351 MB, 전 필드 문서화 README | **CC-BY-4.0**, 등록 불필요, 직접 다운로드 | data.openei.org/submissions/5860 | 스케줄링, 큐 대기 예측, 워크로드 특성화. **목록 중 진입 장벽 최저 — 이상적 baseline/교육용** | job 수준만 |
| **Fresco** (Purdue Anvil + Conte + TACC Stampede) | **2,090만 job, 75개월(2013–2023), 3개 시스템.** job accounting + CPU/GPU/mem/NFS/block-IO | PEARC'25 | 10.1145/3708035.3736090 | **다중 시스템 job 데이터** — C2에 유용 | **label이 Slurm exit-code taxonomy뿐** |
| **Loghub** | 표준 로그 코퍼스. **BGL / Thunderbird / Spirit 등 2007년대 HPC RAS 로그 포함** | 공개 | (ISSRE 2023; DOI 원자료 미기재) | log AD baseline | ⚠ **2026년에도 2007년 로그로 벤치마킹 중 — 이 노후화 자체가 SC 논문 논거** |
| **ALCF Data Catalog** | **17년, 8개 시스템.** RAS_EVENT + DARSHAN + AUTOPERF | ⚠ **IEEE DataPort 구독 필요** | 10.21227/bhfr-wx19 | 폭이 가장 넓음 | 구독 요구 → "누구나 재현 가능"에서 탈락 |
| **LANL USRC failure data** | 1996–2005, 22개 시스템 9년(Schroeder & Gibson DSN'06 기원) | 공개 | usrc.lanl.gov/data/ | 정본이자 보편 인용 가능 | **pre-GPU, 20년 전** |
| **GWDG GPU incident set** | 7 노드 / 28 GPU, ~353일(2025-02~2026-01), **69건 인시던트 카탈로그(운영자 큐레이션)** + Slurm + NHC 상관 | Zenodo | (arXiv 2603.28781 참조) | ⭐ **운영자 큐레이션 label의 드문 예 — C4 프로토콜 참고** | 28 GPU로 매우 작음 |
| **Helios / SenseTime DL cluster trace** | SC21 논문에 수반 | (원자료에 URL 미기재) | sc21 pap594 | DL 클러스터 스케줄링 | 산업 DL, HPC 배치 아님 |
| **Perseus fail-slow dataset** | 41K normal + **315 verified fail-slow** 드라이브 | FAST'23 | usenix fast23/presentation/lu | **검증된 fail-slow ground truth — D축 baseline** | 클라우드 스토리지 |

**요약 권고 — 재현 가능한 HPC AIOps 연구에 가장 유용한 5종:** ① M100 ExaData ② F-DATA ③ HPC-ODA ④ OLCF Constellation(Summit power/thermal + GPU DBE 쌍) ⑤ NREL Eagle jobs.

---

# 6. 연도별·venue별 집계와 커버리지

## 6.1 SC 본프로그램 (A census, ±2편)

| 연도 | 열거 항목 | **Core** | **Broad** | Core 비중 | 열거 근거 |
|---|---|---|---|---|---|
| SC20 | ~105 | **8** | 14 | ~8% | sc20 proceedings index + Crossref (`10.1109/SC41405.2020`) |
| SC21 | ~110 | **4** | 8 | ~4% | sc21 proceedings index (`10.1145/3458817`) |
| SC22 | ~92 | **4** | 7 | ~4% | sc22 index + Crossref (`10.1109/SC41404.2022`) |
| SC23 | ~99 | **5** | 11 | ~5% | sc23 index (`10.1145/3581784`) |
| SC24 | ~114 | **10** | 17 | ~9% | Crossref (`10.1109/SC41406.2024`) — SC24 사이트 robots 차단 |
| SC25 | ~120 (reproducibility report ~20편 제외) | **12** | 18 | ~10% | Crossref (`10.1145/3712285`) |
| SC26 | 미공개 | ≥1 확인 | UNKNOWN | — | CFP + Best Paper finalist 발표만 |

**Core** = 시스템 운영 데이터/telemetry/신뢰성/이상/RCA/전력·냉각/스케줄러 trace가 주 기여. **Broad** = Core + 인접(trace 기반 워크로드·스케줄링, 스토리지·네트워크 측정, sustainability analytics, 기계 운영 실무 논문).
**추세: 2021–2023 평탄(연 4–5) → 2024–2025 계단식 증가(연 10–12).** 증가분은 거의 전부 (a) GPU/AI 클러스터 신뢰성, (b) power/cooling/carbon/water. **2년 만에 약 2배.**
**SC22의 저점은 열거 오류가 아니다** — 두 독립 열거가 일치했다.

## 6.2 venue별 커버리지 상태

| Venue | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| **SC** 본프로그램 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **PARTIAL / NOT YET PUBLISHED** |
| **HPDC** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ **PARTIAL** (~50 레코드만 열거, rate limit) |
| **IPDPS** main | ✅(121) | ✅(118) | ✅(135) | ✅(108) | ✅(100) | ✅(118) | ✅(115) |
| **IEEE Cluster** | ✅(82)* | ✅(119)* | ✅(83)* | ✅(39) | ✅(47) | ✅(46) | **NOT YET PUBLISHED** |
| **ISC** research track | ✅(27) | ✅(24) | ✅(15) | ✅(20) | ⚠**UNVERIFIED** | ⚠**UNVERIFIED** | ⚠**UNVERIFIED** |
| **DSN** | ⚠**PARTIAL** | ⚠**PARTIAL** | ✅ | ✅ | ✅ | ✅ | **NOT YET PUBLISHED** |
| **ISSRE** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **NOT YET PUBLISHED** |
| **ACSOS** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(~13) | **NOT YET PUBLISHED** |
| **CUG** | ⚠**PARTIAL** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ **NOT ACCESSIBLE**(404 + robots) |

\* **IEEE Cluster 2020–2022 proceedings는 병설 워크숍(HPCMASPA, EE HPC SOP, REX-IO, EA-HPC)을 같은 DOI 공간에 포함한다.** 2023부터 분리. → **PIKA, Global Experiences, LDMS Darshan Connector, out-of-band 분류 등은 *워크숍* 논문이며 "IEEE Cluster main track"으로 인용하면 틀린다.** 이 census에서는 `WORKSHOP-IN-PROC`로 표기.

## 6.3 workshop 개최 상태 (요약)

| Workshop | 상태 |
|---|---|
| **HPC-ODA (SC)** | 2019–2025 **BoF 시리즈** (workshop 아님). **2026 SC26에서 1회차 peer-reviewed workshop** (IEEE Xplore, 8p full/4p short) |
| **MODA (ISC)** | 2020(1st, 3편) · 2021(2nd, 2) · 2022(3rd, 2) · 2023(4th, 3) · 2024(5th, 2 + lightning 4) · 2025(6th, 5) · **2026(7th, 개명: "Monitoring, Observability, and Operational Data Analytics", 5편 발표)**. **2020–2025 아카이벌 챕터 총 17편 — 이것이 ODA라는 이름의 peer-reviewed 코퍼스 전부** |
| **HPCSYSPROS (SC)** | 2020(7) · 2021(6) · 2022(5) · 2023(10, ACM SC-W) · 2024(9, Zenodo만) · 2025(9) · 2026 예정. **총 46편, 아카이벌 승격 추적 0건** |
| **FTXS (SC)** | 2020 ✅ · 2021(11th, 5) · 2022(12th, 5) · 2023(13th, 4 full+3 short) · 2024(**14th**, 4) · **2025 미개최** · 2026 **개명·재범위**("Faults, Trustworthiness, and eXplainability for **AI Systems** at Scale") |
| **HPCTESTS (SC)** | **2020–2022 미존재.** 2023(1st, 5) · 2024(2nd, 5) · 2025(3rd, `UNVERIFIED`) · 2026(4th 예정). OLCF 주도 HPC System Test WG |
| **PMBS / ProTools (SC)** | 매년 2020–2026 개최. 편수 `UNVERIFIED` |
| **PDSW** | 매년. **2023부터 SC-W 통합 proceedings로 편입**(별도 dblp 볼륨 없음). 2026 = 11th |
| **JSSPP (IPDPS)** | 매년, LNCS 아카이벌. 2024(27th, 10편) · 2025(28th, 17) · 2026(29th, 13 예정) |
| **PERMAVOST (HPDC)** | 2021(1st) ~ 2026(6th) |
| **AI4Sys (HPDC)** | 2023(1st, `INFERRED`) · 2024(2nd) · 2025(3rd) · 2026(4th). ⚠ **채택 논문 목록 비공개 — 2023–2025 `UNVERIFIED`** |
| **SNTA (HPDC)** | 2020–2024(7th) 개최, **2025·2026 미개최.** HPDC의 유일한 telemetry 워크숍이 사라짐 |
| **EESP** | 2025 ISC(1st, 8 채택/36%, LNCS 6편) · 2026 ISC(2nd, 19 중 11) · **2026 SC(3rd)** |
| **SC26 신설** | **ECHO**(1st, Edge-Cloud-HPC Operational Continuum), **AgenticAI4HPC'26**(1st), RESDIS(6th), HPF AI/HPC, RISE 2026, Sovereign AI Supercomputing Cloud |

---

# 7. 검증 상태 및 위험 (필독)

## 7.1 구조적 한계 — census 전체에 적용

| # | 한계 | 영향 |
|---|---|---|
| 1 | **ACM DL·IEEE Xplore 403 차단** | **어떤 논문의 abstract도 대량으로 읽지 못했다.** B census(HPDC/IPDPS/Cluster/ISC/ACSOS)의 evaluation scale·production deployment 필드는 **검증된 사실이 아니라 가설**이다. `[A]` 표시 항목 전부 해당 |
| 2 | **SC 논문 페이지가 트랙 라벨 미노출** | **SC 항목 대부분이 `TRACK-UNKNOWN`.** Technical Paper와 State of the Practice를 구분하지 못했다. **"이 논문은 SC Technical Paper였다"고 쓰지 말 것** |
| 3 | **dblp ToC가 WebFetch에서 ~10건 절단**, search API robots 차단 | Crossref/프로그램 페이지로 우회. dblp *record* 페이지(개별 논문)는 정상 |
| 4 | **WebSearch 예산 200/200 소진** | 후반 조사는 Crossref·Semantic Scholar·직접 fetch만. 벤더 감사에서 **Intel·VAST `NOT COVERED`**. **ICPE도 `NOT COVERED`** |
| 5 | **L/D/P 스케일 혼용** | F/G 원자료가 자체 정의를 사용. 재매핑한 항목은 `[L/D/P re-mapped]`, 불가한 항목은 명시. **두 스케일을 섞어 읽지 말 것** |
| 6 | **저자 목록 미fetch 항목 다수** | 기억으로 재구성 금지. 인용 전 확보 |
| 7 | **Crossref에서 절단된 ACM HPDC 제목** | Apollo:, Holmes, Capri, TAC, SchedInspector, Heterogeneous Systems Resilience — **실재하는 DOI이지만 제목이 불완전.** ACM DL에서 재확보 필요 |

## 7.2 개별 항목의 불완전성

| 항목 | 사유 |
|---|---|
| M-07 Cost-Aware DRAM (SC20) · M-12 Not All GPUs (SC22) | DOI 미기재(페이지 URL만) |
| M-14 From Alert Fatigue (SC26) | **DOI 미발행, 미개최, 초록 미확보** |
| M-27 Time Machine · M-28 ClusterRCA · M-29 Too Many Cooks · M-40 Loghub | DOI 미기재(프로그램 페이지 기반 검증) |
| M-37 ARGUS | **arXiv preprint, venue 미확정** |
| M-01 Kaleidoscope · M-13 Slingshot | DOI 식별자가 출처마다 상이 |
| M-36 Tuncer TPDS | 연도 표기가 출처마다 상이(2018/2019) |
| ICS'24 Summit GPU memory corruption | **저자 순서가 출처(D vs H) 간 불일치** |
| Understanding Stragglers What-if Analysis | venue `UNVERIFIED` |
| Exploring the Frontiers of Energy Efficiency (Frontier 전력관리) | **arXiv 외 venue `UNVERIFIED`** |
| Reducing False Node Failure Predictions in HPC | venue `UNVERIFIED`(HiPC 2019 추정) |
| Gray Failure (HotOS'17) · LOGAIDER(CCGrid) · LogTAD(CIKM) | 저자·venue 부분 `UNVERIFIED` |

## 7.3 ⚠ 인용 전 반드시 확보해서 읽어야 할 항목

**어느 것이든 이 조사의 판정을 뒤집을 수 있다.**

| 문헌 | ID | 왜 위험한가 |
|---|---|---|
| **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** (ORNL) | **SC26 Best Paper finalist**, DOI 미발행 | **axis A 정면.** 공개 즉시 확보 |
| **Mantis: Decoding HPC Telemetry Data for Robust System Prediction** | **ICS 2026**, `10.1145/3797905.3800527` | 403. axis B/D/F |
| **Safe Remediation as Risk-Constrained Intervention Decision in Microservice Systems** | arXiv `2607.20005` | **axis F 프레이밍을 선점했을 수 있음** |
| **HPC ODA Commons** | **PEARC'26**, `10.1145/3785462.3815891` | 403. schema/데이터셋 공개 계획 시 필수 |
| **WisIO** | **ICS'25**, `10.1145/3721145.3725742` | 저자·내용 미확인 |
| **ALBADross 후속 / Runtime Performance Anomaly Diagnosis Using Active Learning** | **TPDS 2024**, `10.1109/TPDS.2024.3365462` | 403. axis D/E |
| **K4-Serve** | PEARC'26, `10.1145/3785462.3815821` | 미확인 |
| **Labeling the Invisible: Scalable Framework for Labeling Fail-Slow Failures in Cloud Storage** | FAST(연도 `UNVERIFIED`, '26 추정) | **D+E ground truth gap 정면** |
| Nezha (FSE'23) · Sage (ASPLOS'21) · Nenya (KDD'22) · Mint (ASPLOS'24) · NVMe SSD Failures in the Field (ATC'23) · Cores that don't count (HotOS'21) · Tiwari et al. GPU errors (HPCA'15) · Borghesi et al. (AAAI/IAAI'19, TPDS'22) · Schroeder & Gibson (FAST'07) · Cohen et al. (OSDI'04) · Nagaraj et al. (NSDI'12) | 각 venue | **ACM DL/Xplore 차단으로 전부 `UNVERIFIED`** |

## 7.4 커버리지 구멍

1. **DSN 2020·2021** — 프로그램 페이지 소실/차단, dblp 절단. **in-scope 논문 3–8편 누락 추정.** 기관 네트워크에서 IEEE Xplore로 재조사 권장
2. **ISC research-paper track 2024–2026** — proceedings 미확인. ⚠ **"track이 없어졌다"고 쓰지 말 것.** 확인되지 않았을 뿐이다
3. **IEEE Cluster 2026, ACSOS 2026, DSN 2026, ISSRE 2026** — `NOT YET PUBLISHED`
4. **HPDC 2026** — 볼륨의 약 절반만 열거(rate limit)
5. **CUG 2026** — proceedings 404, 프로그램 robots 차단. **0건 검증.** 2027년 초 재확인
6. **CUG PDF 5건 미게시** — CUG2021 HPE AIOps, CUG2021 Sandia system/application monitoring, CUG2022 Fallout, CUG2023 Slingshot Dashboard tutorial, CUG2024 Swordfish. **"미게시"이지 "없음"이 아니다.** ORNL·Sandia·NERSC 저자는 요청 시 대개 공유한다
7. **AI4Sys 2023–2025 채택 논문 목록 비공개** — 공개 기록의 실질적 공백
8. **벤더 감사에서 Intel·VAST 미포함**

## 7.5 인용 위생 정정 (전파할 것)

> Gainaru, Cappello, Snir, Kramer의 SC 2012 논문의 **정확한 제목은 "Fault prediction under the microscope: a closer look into HPC systems"** (`10.1109/SC.2012.57`). 널리 유통되는 **"…a closed-loop approach" 변형은 틀렸다.**

## 7.6 사후 검증 기록 (2026-09-06, Crossref 직접 조회)

이 census 완성 후, **가장 인용 위험이 큰 항목 6건**을 Crossref API로 직접 재조회했다. Crossref는 심한 rate limit 상태였으므로 전수 검증은 하지 못했다. **6건 전부 기록과 정확히 일치했으며, 그중 2건은 원자료가 `UNVERIFIED`로 표시했던 저자 목록이 확정되었다.**

| DOI | 검증 결과 |
|---|---|
| `10.1145/3581784.3607076` | ✅ **일치.** *Prodigy: Towards Unsupervised Anomaly Detection in Production HPC Systems* — Burak Aksar, Efe Sencan, Benjamin Schwaller, Omar Aaziz, Vitus J. Leung, Jim Brandt, Brian Kulis, Manuel Egele, Ayse K. Coskun · 2023 · *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis* (SC '23) |
| `10.1145/3712285.3759883` | ✅ **일치.** *Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems* — Yonatan Levitt, Richard Barella, Sam Zeltner, Thomas Musta, Lance Cheney, Gustavo Espinosa, Olivier Franza, Balazs Gerofi · 2025 · SC '25 |
| `10.1109/SC41406.2024.00029` | ✅ **일치.** *A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale* — Wesley Brewer, Matthias Maiterth, Vineet Kumar, Rafal Wojda, Sedrick Bouknight, Jesse Hines, Woong Shin, Scott Greenwood, David Grant, Wesley Williams, Feiyi Wang · 2024 · SC24 |
| `10.1145/3369583.3392674` | ✅ **일치 + 저자 확정.** *DCDB Wintermute: Enabling Online and Holistic Operational Data Analytics on HPC Systems* — Alessio Netti, Micha Müller, Carla Guillen, Michael Ott, Daniele Tafani, Gence Ozer, Martin Schulz · 2020 · HPDC '20, **pp.101–112**. (원자료 F는 이 저자 목록을 `UNVERIFIED`로 표시했었다 → **확정**) |
| `10.1109/SC.2012.57` | ✅ **일치 — 제목 정정 확정.** *"Fault prediction under the microscope: A closer look into HPC systems"* — Ana Gainaru, Franck Cappello, Marc Snir, William Kramer · 2012 · SC 2012. **널리 유통되는 "…a closed-loop approach" 변형은 확정적으로 틀렸다.** |
| `10.1038/s41597-023-02174-3` | ✅ **일치 + 저자 확정 + 제목 미세 정정.** 정확한 제목은 *"M100 ExaData: a data collection campaign on **the** CINECA's Marconi100 Tier-0 supercomputer"* — Andrea Borghesi, Carmine Di Santi, Martin Molan, Mohsen Seyedkazemi Ardebili, Alessio Mauri, Massimiliano Guarrasi, Daniela Galetti, Mirko Cestari, Francesco Barchi, Luca Benini, Francesco Beneventi, Andrea Bartolini · 2023 · *Scientific Data*. (원자료 B/F는 저자 목록을 `UNVERIFIED`로 표시했었다 → **확정**) |

**해석.** 표본이 작지만(6/약 200), 무작위가 아니라 **가장 위험한 항목을 골라 검사한 것**이며 **오류율 0**이었다. 이는 census의 서지 계층(제목·저자·연도·venue·DOI)이 신뢰할 만하다는 신호다.
**그러나 이 검증은 서지 계층에만 적용된다.** §7.1의 한계 ①이 여전히 지배적이다 — **evaluation scale, production deployment, L/D/P 등 내용 계층의 상당수는 abstract를 읽지 못한 상태의 assessment이며, 인용 전 PDF 확인이 필요하다.**

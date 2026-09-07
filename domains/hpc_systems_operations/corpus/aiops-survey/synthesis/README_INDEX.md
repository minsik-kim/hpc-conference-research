# HPC AIOps / Operational Intelligence → SC 정규 논문 연구 지형 조사
## 문서 색인 (2026-09-06)

**목적:** 일반적 literature survey가 아니라, 대규모 HPC production 운영의 반복 문제 중 **SC 정규 Technical Paper 수준의 systems research로 발전 가능한 문제**를 식별하는 것.

## 읽는 순서

| 순서 | 문서 | 내용 |
|---|---|---|
| **1** | **`13_VERIFICATION_ROUND2.md`** | **여기서 시작할 것.** 8개 병렬 검증 트랙 회수 결과. `09`의 여러 주장을 재정정하고 순위를 개정했다. 인용 오류 5건 추가, H1a falsified, retention 축은 이중 확인으로 강화, SC26 ORNL 논문 확정 |
| **2** | `09_ADVERSARIAL_NOVELTY_AUDIT.md` | 1차 조사 결과의 반례 탐색·정정. 25개 주장 감사(7 FALSIFIED / 8 약화 / 1 무조건 생존), 인용 오류 3건, KISTI 국내 선행연구. **`13` §4.1의 정정 적용 후 사용** |
| **3** | `10_SC_CANDIDATE_RANKING.md` | 후보 10개 → 최종 4개 + 워크숍 1개. 비교표·순위·각 후보의 "착수하지 말아야 할 가장 강한 이유". **순위는 `13` §3이 최신** |
| **4** | `08_RESEARCH_PRESERVATION_REQUIREMENTS.md` | **운영 의사결정 문서.** 지금 남기지 않으면 영구 소실되는 telemetry/provenance. 저장하면 안 되는 데이터 |
| **5** | `11_INITIAL_EXPERIMENT_DESIGNS.md` | Top 3의 첫 실험 + **폐기 기준** + SC 논문 구조 역설계 |
| **6** | `12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` | 미확보 자료. 각각이 어떤 후보를 죽일 수 있는가. **해소 상태는 `13` §4.1, 신규 항목 W-30~W-38** |

## 1차 조사 문서 (`09` §13의 정정 적용 후 사용)

| 문서 | 내용 |
|---|---|
| `00_SCOPE_AND_METHOD.md` | 범위·분류체계(L0–L7, D0–D5, P0–P4)·증거 규칙·방법 한계 |
| `01_VENUE_MAP.md` | SC 트랙 구조, Tier A/B venue, 워크숍 생태계, CUG의 역할과 한계 |
| `02_PAPER_CENSUS.md` | 논문 전수조사. MUST READ 41편 + 주제별 표 + 공개 데이터셋 |
| `03_SC_REGULAR_PRECEDENTS.md` | SC 본트랙 선례 9편 심층 분석 + 비-SC 벤치마크 10편 |
| `04_WORKSHOP_AND_CUG_CASES.md` | 워크숍/CUG 운영 문제, 18개 사이트 telemetry 데이터 경로, 벤더 주장 감사 |
| `05_RESEARCH_PRACTICE_GAPS.md` | gap 표 G1–G20, 7개 연구축 판정 |
| `06_INITIAL_SC_RESEARCH_CANDIDATES.md` | 초기 후보 C1–C10 (→ `10`에서 압축) |
| `07_ANSWERS_TO_KEY_QUESTIONS.md` | 핵심 질문 10개에 대한 답변 |

## 현재 상태 (2026-09-06, 2차 검증 후)

| 후보 | 판정 | 착수 게이트 |
|---|---|---|
| **F2** 세대 간 telemetry 전이 측정 | `SC-PLAUSIBLE` — **실행 1순위**(데이터 리드타임 0) | ModelX(HPDC'25) 확보 |
| **F1** Telemetry policy / retention 문턱 | `SC-PLAUSIBLE` — 강도 1위이나 조건부 | **SC26 ORNL 초록(2026-09-16)** + subsampling-aware baseline |
| **F3** Label semantics + fail-slow | `SC-STRETCH` | **SC26 ORNL 초록(2026-09-16)** |
| **F4′** 운영 정책 counterfactual 평가 | `SC-STRETCH` (조건부) | Slurm `actor_type` 12개월 축적 |
| **W1** 효율 리포팅 행동 효과 | 워크숍(HPC-ODA 2027) | staggered rollout 설계 |

## 한 문장 결론

문헌 조사로 확인한 것은 어떤 논문을 쓸 수 있는지가 아니라, **어떤 데이터를 지금 남기지 않으면 어떤 논문도 쓸 수 없는지**였다 → `08` §0의 P-1(전해상도 다계층 참조 코퍼스), P-2(Slurm 상태변경 `actor` 필드).

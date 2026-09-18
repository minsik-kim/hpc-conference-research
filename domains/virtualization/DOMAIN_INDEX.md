# DOMAIN_INDEX — virtualization

## 어디서 시작할 것인가

| 목적 | 파일 |
|---|---|
| **처음 읽는다 / 무엇부터 읽을지 모른다** | `synthesis/READING_ROADMAP.md` — 8단계 커리큘럼 + 필수 20편 |
| 이 domain의 목적·범위·증거 규율 | `DOMAIN_CONTEXT.md` |
| 분류 체계와 경계 판정 규칙 | `synthesis/VIRTUALIZATION_TAXONOMY.md` |
| 특정 기술 주제를 판다 | `topics/*.md` (아래 표) |
| 논문 간 계보를 본다 | `synthesis/VIRTUALIZATION_LINEAGES.md` |
| trade-off 구조를 본다 | `synthesis/VIRTUALIZATION_TRADEOFFS.md` |
| 어떤 논문 다음에 무엇을 읽을지 | `synthesis/CROSS_PAPER_RELATIONS.md` |
| 3년 동향 | `synthesis/THREE_YEAR_TRENDS.md` |
| **분류를 신뢰해도 되는가 / 무엇이 약한가** | `synthesis/GLOBAL_AUDIT.md`, `RESEARCH_STATUS.md` |
| venue별 population과 배제 기록 | `census/CENSUS_2024.md`, `CENSUS_2025.md`, `CENSUS_2026.md` |
| 기계 판독용 전체 데이터 | `data/PAPER_CATALOG.csv` (410행), `data/PAPER_RELATIONS.csv` (330행) |
| 원 record (batch 단위) | `batches/*.yaml` |
| 통합 record | `data/MERGED_CORPUS.yaml` |

## Topic 파일

| 파일 | tax | primary | 그중 CORE |
|---|---|---|---|
| `topics/vm_hypervisor.md` | T1 | 13 | 13 |
| `topics/memory_virtualization.md` | T2 | 26 | 14 |
| `topics/io_device_virtualization.md` | T3 | 28 | 18 |
| `topics/migration_checkpoint.md` | T4 | 17 | 11 |
| `topics/container_isolation.md` | T5 | 45 | 27 |
| `topics/accelerator_virtualization.md` | T6 | 41 | 16 |
| `topics/confidential_virtualization.md` | T7 | 33 | 22 |
| `topics/serverless_cloud.md` | T8 | 5 | 0 |
| `topics/resource_management.md` | T9 | 14 | 1 |

각 topic 파일은 동일한 9절 구조를 갖는다:
문제 정의 → mechanism design space → 핵심 논문(P0/P1) → supporting 논문(P2/P3) →
trade-off 구조 → 인접 계층 관계 → 2024→2026 변화 → 읽는 순서 → **증거 한계**.

## ID 규칙

`VIRT-<VENUE><YY>-<NN>` — 예: `VIRT-OSDI26-01`. 한 번 부여된 ID는 재분류·이동·정정
후에도 바뀌지 않으며 재사용되지 않는다 (repository `governance/ID_NAMING_RULES.md`).

## 이 corpus를 인용할 때

`evidence_depth`를 함께 확인하라. `TITLE_ONLY`·`ABSTRACT` 항목은 개념 배치용이며
**논문의 주장으로 인용해서는 안 된다.** 정량 수치는 반드시 hardware/workload/baseline
한정자와 함께 쓴다. 상세는 `RESEARCH_STATUS.md` §3.

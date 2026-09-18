# RESEARCH_STATUS — virtualization domain

작성 기준일: 2026-09-18. 상태: **1차 구축 완료, 잔여 항목 명시**.

## 1. 규모

| 항목 | 수 |
|---|---|
| 검토된 후보 (record 생성) | 410 |
| CORE | 124 |
| SUPPORT | 104 |
| CONTEXT | 134 |
| DROP | 48 |
| 보존 (CORE+SUPPORT+CONTEXT) | 362 |
| 기록된 관계 (relation) | 330 |

연도별: 2024 = 167건 검토 / 137 보존, 2025 = 160 / 148, 2026 = 83 / 77.
우선순위: P0 = 15, P1 = 103, P2 = 116, P3 = 170 (DROP 6건은 우선순위 없음).

## 2. 증거 수준 분포 — 이 corpus의 신뢰도를 읽는 법

| evidence_depth | 건수 | 의미 |
|---|---|---|
| FULL | 60 | 초록·서론·설계·구현·평가·한계까지 |
| DESIGN_EVAL | 132 | 설계와 평가까지 |
| DESIGN | 12 | 설계까지 |
| ABSTRACT_INTRO | 41 | 초록 + 서론 |
| ABSTRACT | 102 | 초록만 |
| TITLE_ONLY | 63 | 제목만 (접근 실패) |

확신도: HIGH 216 / MEDIUM 129 / LOW 65.

**즉 CORE·SUPPORT 판정의 약 절반(192/410)이 설계 수준 이상 근거를 갖는다.**
나머지는 초록 또는 제목 수준이며, 아래 §3에 명시했다.

## 3. 알려진 한계 — 반드시 읽을 것

### 3.1 초록 수준 증거에만 의존하는 CORE 25건

이 논문들은 CORE로 분류되었으나 **설계·평가를 직접 읽지 못했다.** 인용이 필요하면 원문을
직접 확인해야 한다.

- `VIRT-CCGRID24-03` Incorporating Memory Sharing-awareness in Multi-VM Live Migration — CCGrid 2024 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-CCGRID24-04` vASP: Full VM Life-cycle Protection Based on Active Security Processor Architecture — CCGrid 2024 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS24-02` Hoda: a High-performance Open vSwitch Dataplane with Multiple Specialized Data Paths — EuroSys 2024 / 증거 ABSTRACT / 확신도 HIGH
- `VIRT-SOCC24-07` Towards Swap-Free, Continuous Ballooning for Fast, Cloud-Based Virtual Machine Migrations — SoCC 2024 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-ASPLOS25-01` Vela: A Virtualized LLM Training System with GPU Direct RoCE — ASPLOS 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS25-01` FastIOV: Fast Startup of Passthrough Network I/O Virtualization for Secure Containers — EuroSys 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS25-06` Byte vSwitch: A High-Performance Virtual Switch for Cloud Networking — EuroSys 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS25-08` Phantom: Virtualizing Switch Register Resources for Accurate Sketch-based Network Measurement — EuroSys 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-MIDDLEWARE25-02` Full Trust Alchemist: Reforging Attestation for Cloud-based Confidential Workloads — Middleware 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-SOSP25-01` Device-Assisted Live Migration of RDMA Devices — SOSP 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-SOSP25-02` Demeter: A Scalable and Elastic Tiered Memory Solution for Virtualized Cloud via Guest Delegation — SOSP 2025 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-ASPLOS26-03` TEEM³: Core-Independent and Cooperating Trusted Execution Environments — ASPLOS 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-ASPLOS26-04` WorksetEnclave: Towards Optimizing Cold Starts in Confidential Serverless with Workset-Based Enclave Restore — ASPLOS 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-ASPLOS26-06` Detecting Inconsistencies in Arm CCA's Formally Verified Specification — ASPLOS 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-CCGRID26-01` TelePod: Live Migration for Stateful Containers — CCGrid 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-01` CofferOS: Hardening OS-level Virtualization with Rust — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-02` Proteus: Heterogeneous FPGA Virtualization — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-04` Everything You Need to Know About Virtual Machine Live Migration Between Heterogeneous Processors — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-05` Squeezy: Rapid VM Memory Reclamation for Serverless Functions — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-18` Pyramid: A Secure, Resource-Efficient, and Pluggable Kubernetes for Multi-Tenancy — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-EUROSYS26-19` RoPeerTo: A Datacenter-Scale Architecture for Peer-To-Peer DMA between GPUs and FPGAs — EuroSys 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-HPCA26-02` eGPU: Production-Scale Elastic Sharing over 10,000 GPUs — HPCA 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-HPCA26-03` SCALE: Tackling Communication Bottlenecks in Confidential Distributed Machine Learning — HPCA 2026 / 증거 ABSTRACT / 확신도 MEDIUM
- `VIRT-HPCA26-05` DSAssassin: Cross-VM Side-Channel Attacks by Exploiting Intel Data Streaming Accelerator — HPCA 2026 / 증거 ABSTRACT / 확신도 HIGH
- `VIRT-HPDC26-01` Enabling Floating Point Virtualization With Tiny Numbers — HPDC 2026 / 증거 ABSTRACT / 확신도 MEDIUM

### 3.2 전수 열거에 실패한 venue

- **SC 2024** — 공식 사이트가 robots.txt로 `/program/`·`/proceedings/` 전 경로를 차단했고
  ACM DL은 403, dblp도 차단되었다. keyword 검색만으로 5건을 찾았다.
  **SC 2024의 CORE = 0은 실제 부재가 아니라 탐색 한계다. 이 corpus 최대의 recall 공백.**
- **SC 2025** — 총 137편(공식 블로그 확인)이라는 총수만 확보했고 전체 제목 목록은 열거하지
  못했다. 약 12회의 표적 keyword 검색으로 보완했으나 전수 조사보다 recall이 낮다.
- **ASPLOS 2026 / HPDC 2026** — population 미확정. 전자는 공식 페이지의 "167 unique papers"
  주장과 실제 scrape 결과가 불일치하고(복수 submission cycle·복수 proceedings 권),
  후자는 hpdc.org의 TLS 인증서 체인 오류로 프로그램 접근 자체가 불가능했다.

### 3.3 publication_type 미확인 22건

대부분 **SoCC 2024**다. ACM DL 차단으로 full / short / industry / vision track 구분을
확인할 수 없었다. 추정하지 않고 `UNKNOWN`으로 남겼다.

### 3.4 제목 수준에 머문 63건

2차 rescue pass에서도 회수 실패한 항목이다. 전원 `CONTEXT` + `LOW`로 보수적으로 기록했으며,
DROP하지 않았다. 대표적으로 BASK(EuroSys26, Gold OA인데도 ACM DL 봇 차단),
Fault Escaping(ASPLOS26), ConMonitor·Snapipeline·TianMen(SoCC24).

### 3.5 venue별 CORE 비율은 비교 불가

batch마다 "배제한 논문에도 record를 만들었는가"의 정책이 달랐기 때문에 분모가 다르다.
예: CCGrid 2024는 유망 후보에만 record를 만들어 8건 중 5건이 CORE(63%)이고,
MICRO 2024는 배제 논문도 DROP record로 보존해 17건 중 7건이 DROP이다.
**연도별 비교는 유효하나(§GLOBAL_AUDIT Q1), venue별 비교는 이 수치로 하면 안 된다.**

### 3.6 데이터 정합성 — DOI 필드는 재검증 없이 인용하지 말 것

독립 verification pass(12건 표본)에서 **DOI 오류가 확인되었다.** 발견되어 정정된 것:

| id | 잘못된 DOI | 실제로 가리키던 것 | 정정 |
|---|---|---|---|
| `VIRT-CCGRID24-03` | 10.1109/CCGrid59990.2024.00075 | 무관한 논문 (Quantum-Classical Computing 교육) | 10.1109/CCGrid59990.2024.00084 |
| `VIRT-CCGRID24-06` | 10.1109/CCGrid59990.2024.00075 | 위와 동일 | 10.1109/CCGrid59990.2024.00064 |
| `VIRT-ASPLOS24-03` (GMLake) | 10.1145/3620666.3651353 | `VIRT-ASPLOS24-16` (GMT) | 10.1145/3620665.3640423 (Crossref 확인) |

정정 후 전 corpus 재검사 결과: 형식 오류 0건, 중복 DOI 0건, DOI 보유 257/410건.
**그러나 표본 12건 중 2건(약 1/6)에서 DOI 오류가 나왔다는 사실은, 아직 검사하지 않은
나머지 레코드에도 같은 유형의 오류가 있을 수 있음을 뜻한다.**

- 서지 정보를 인용·링크 목적으로 쓰려면 **전수 DOI resolution pass가 선행되어야 한다.**
- 반면 **질적·기구 서술 내용은 표본에서 신뢰할 만한 것으로 확인되었다.** 조작된 mechanism
  서술은 발견되지 않았고, `evidence_depth` 자기 표기는 실제 접근 가능성과 일치했다
  (초록만 접근 가능한 논문이 FULL로 표기된 사례 없음).

기타 verification 지적 사항:
- `VIRT-EUROSYS25-03`(HyperAlloc)의 STREAM 수치 1건이 저자 PDF에서 확인되지 않았다.
  해당 claim에 `[VERIFY: ...]` 경고를 인라인으로 남겼다. 나머지 6건은 축자 일치.
- `VIRT-EUROSYS24-01`(HD-IOV) 저자 목록이 3명+et al.로 축약되어 있다(원 출처는 10명 전원 표기).
- `VIRT-OSDI26-06`(Nixie)의 OSDI 2026 채택 여부는 재확인에서도 공식 프로그램상 확인되지 않았다
  (arXiv에는 존재). 기존 기록의 flag가 유지된다.

전체 verification 결과는 `synthesis/VERIFICATION.md`에 있다.

### 3.7 데이터 정합성 미해결

현재 알려진 미해결 정합성 문제는 없다(위 3건은 정정 완료). 다만 §3.6의 전수 DOI 검증 권고는 유효하다.

## 4. 이번 작업에서 수행한 것

1. repository 상태 확인 (branch `main`, 타 세션 uncommitted 변경 보존)
2. `domains/virtualization/` subtree 신설, 공유 root 파일 미수정
3. 2025–2026 seed population 재검증 (seed label 미사용, 원문 기준 독립 판정)
4. 2024 census 신규 수행 (12 venue)
5. **targeted retrieval rescue pass** — 접근 실패로 TITLE_ONLY였던 37건 재시도, 28건 회수
6. 전역 일관성 감사 (§GLOBAL_AUDIT), 실질 재분류 28건 기록
7. topic 9개 + synthesis 7개 + census 3개 작성
8. `data/PAPER_CATALOG.csv`(410행), `data/PAPER_RELATIONS.csv`(330행) 생성

## 5. 남은 작업

우선순위 순.

1. **SC 2024 / SC 2025 전수 census 재시도.** 다른 네트워크 경로나 DL 접근 권한이 있으면
   가장 먼저 해야 할 일이다. 현재 SC 두 해의 CORE=0은 신뢰할 수 없다.
2. **초록 수준 CORE 25건 심화 독해** (§3.1 목록).
   특히 `VIRT-SOSP25-01`(RDMA device migration)은 mechanism/isolation/state가 전부 UNKNOWN인데
   T3·T4 두 branch의 연결점이라 영향이 크다.
3. **SoCC 2024 publication_type 확정** 22건.
4. **TITLE_ONLY 63건 재시도** (§3.4).
5. **전수 DOI resolution pass** — 표본에서 1/6 오류율이 나왔다(§3.6). 인용 용도로 쓰기 전 필수.
6. batch 1~4(EuroSys25, SOSP25, ASPLOS25, Middleware25, CCGrid25)의 `venue_populations`
   backfill — 해당 agent들이 session limit으로 batch report를 남기지 못했다.
7. `POSSIBLE_EXPANSION` 검토 — NSDI(network virtualization/vSwitch/NFV),
   security venue의 confidential VM 논문, CCGrid 병설 ICFEC.

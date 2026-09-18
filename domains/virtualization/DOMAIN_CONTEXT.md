# DOMAIN_CONTEXT — virtualization

## 이 domain은 무엇인가

2024–2026 virtualization 및 인접 systems research의 landscape다. 목적은 논문을 최소한으로
추리는 것이 **아니다**. 목적은 다음과 같다.

> 하나의 핵심 virtualization paper를 읽을 때, 그 논문의 기술적 배경, 아래/위 계층,
> alternative mechanism, trade-off, 실제 cloud/HPC usage까지 함께 이해할 수 있는
> **reusable knowledge base**.

소유자는 virtualization이 주 연구 분야가 아니며, 부서의 관련 기술과 systems stack을 체계적으로
학습하기 위해 이 corpus를 만든다. 따라서 **broad preservation > aggressive pruning** 이 기본 방침이다.

## 범위

- **기간:** 2024, 2025, 2026 (2026은 2026-09-18 KST 기준 이미 개최된 venue만)
- **venue 12개:**
  - Systems/virtualization — EuroSys, OSDI, SOSP, USENIX ATC, SoCC, ASPLOS
  - HPC/distributed/cloud — SC, HPDC, Middleware, CCGrid
  - Architecture (선별) — HPCA, MICRO
- **출판 기준:** main conference / regular·full / peer-reviewed / archival research paper.
  workshop·poster·demo·short·extended abstract·tutorial·panel·doctoral symposium·invited는 제외하되,
  OSDI Operational Systems 같은 main venue의 별도 archival category는 `OPERATIONAL_REFERENCE`로,
  industry track은 `INDUSTRY_TRACK`으로 **별도 보존**하며 정규 연구 통계에는 섞지 않는다.

## 분류 체계

계층 4단계 — CORE / SUPPORT / CONTEXT / DROP. 기술 taxonomy 10개 — T1~T10.
상세 정의와 경계 판정 규칙은 `synthesis/VIRTUALIZATION_TAXONOMY.md`, 원 브리프는
`evidence/CLASSIFICATION_BRIEF.md`에 있다.

## 논문을 읽는 관점

모든 논문을 키워드가 아니라 **mapping 문제**로 해석한다.

```
Physical Resource  →  Logical Resource Abstraction  →  Workload
```

각 논문에서 다음을 추출한다.
- **Isolation** — 서로 다른 tenant/논리 자원의 보안·성능 간섭을 어떻게 제한하는가
- **Multiplexing** — 하나의 물리 자원을 여러 소비자가 어떻게 나눠 쓰는가
- **Translation/Mediation** — virtualization layer가 어떤 추가 경로를 만드는가
  (예: GVA → GPA → HPA, 또는 Guest → VMM → Device)
- **State** — virtualization state는 어디 있고 migration/checkpoint 시 어떻게 이동하는가
- **Performance trade-off** — 구조적 형태로 (예: passthrough → mediation 비용 하락,
  그러나 isolation·memory management·live migration이 어려워짐)

## 증거 규율

이 domain은 repository의 `governance/ANTI_HALLUCINATION_RULES.md`와
`governance/SOURCE_EVIDENCE_RULES.md`를 따른다. 추가로 이 domain 고유의 규칙:

- 모든 record는 `evidence_depth`를 갖는다:
  `TITLE_ONLY / ABSTRACT / ABSTRACT_INTRO / DESIGN / DESIGN_EVAL / FULL`.
  **이 값은 실제로 읽은 수준이며, 부풀리지 않는다.**
- 제목만으로 최종 분류하지 않는다. 접근 실패 시 `TITLE_ONLY` + `CONTEXT` + `LOW`로 기록하고
  DROP하지 않는다.
- 정량 수치는 hardware/workload/baseline 한정자와 함께 기록한다. 2차 요약에서 숫자를
  전파하지 않는다.
- 기존 corpus(`ai_hpc_systems`, `hpc_quantum`)의 분석 결과는 참고자료이며, 원문 확인 후
  독립 판정한다.

## 기존 corpus와의 관계

| id | 논문 | 겹침 | 처리 |
|---|---|---|---|
| VIRT-OSDI25-04 | Quantum Virtual Machines (HyperQ) | hpc_quantum | `KEEP_CORE_ALREADY_ANALYZED` — QPU 시·공간 multiplexing과 격리라는 virtualization delta만 보강 |
| VIRT-ASPLOS25-01 | Vela: Virtualized LLM Training with GPU Direct RoCE | ai_hpc_systems | `KEEP_CORE_ALREADY_ANALYZED` — VM 내 SR-IOV/GPUDirect RoCE의 I/O virtualization 관점만 보강 |
| VIRT-SOSP25-14 | LithOS | ai_hpc_systems | CORE 유지 |
| VIRT-SOSP25-07 | Aegaeon | ai_hpc_systems | SUPPORT |
| VIRT-EUROSYS25-10, -12 | Faro, Multiplexing DL Workloads | ai_hpc_systems | CONTEXT |
| VIRT-CCGRID25-08 | Choreography and Profiling of Quantum-Classical FaaS Workflows | hpc_quantum | `DROP / already_analysed_no_delta` — 이번 full-paper 재검토에서도 virtualization 기구 기여 없음을 확인, 이전 audit의 REMOVE_DUPLICATE 판정 유지 |

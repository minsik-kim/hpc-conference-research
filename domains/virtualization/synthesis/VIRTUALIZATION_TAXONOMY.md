# VIRTUALIZATION_TAXONOMY — 분류 체계와 적용 결과

## 1. 이 corpus가 쓰는 두 축

분류는 **계층(layer)** 과 **기술 축(taxonomy)** 두 축으로 이루어진다. 둘은 독립이다.

### 축 A — 계층: 이 논문이 나에게 무엇인가

| 계층 | 정의 | 규모 |
|---|---|---|
| **CORE** | virtualization / isolation / virtual-resource abstraction 자체가 주된 기여 | 124 |
| **SUPPORT** | 주된 기여는 아니지만, 어떤 CORE 논문의 설계·trade-off를 더 잘 설명하게 해줌 | 104 |
| **CONTEXT** | virtualized infrastructure를 **사용하는** 상위 시스템/응용 연구 | 134 |
| **DROP** | 보존 가치 없음 (7가지 사유에 한정) | 48 |

판정 질문은 계층마다 다르다.
- CORE: *물리 자원 → 논리 자원 추상화* 를 이 논문이 새로 만들거나 바꾸는가?
- SUPPORT: 이 논문을 알면 **어떤 CORE 논문의 architecture/design choice/trade-off를 더 잘
  설명할 수 있는가?** YES면 보존.
- CONTEXT: 추상화가 왜 필요한지 / multi-tenancy가 어떤 응용 문제를 만드는지 /
  sharing·isolation이 SLO에 어떤 영향을 주는지 / 실제 cloud·HPC가 어떻게 쓰는지 —
  이 중 하나라도 설명하면 보존.
- 애매하면 **DROP하지 않고 CONTEXT로 유지**한다.

### 축 B — 기술 taxonomy: 이 논문이 어느 자원을 다루는가

primary 1개 + 필요 시 secondary 복수.

| tax | 영역 | primary (CORE+SUPPORT) | 그중 CORE |
|---|---|---|---|
| T1 | CPU / machine virtualization (VM, VMM, hypervisor, nested, vCPU) | 13 | 13 |
| T2 | Memory virtualization (guest memory, nested translation, ballooning, dedup, tiering) | 26 | 14 |
| T3 | I/O·device virtualization (IOMMU, SR-IOV, passthrough, virtio, vSwitch, NIC, NVMe, RDMA, SmartNIC, DPU) | 28 | 18 |
| T4 | Migration / checkpoint / state | 17 | 11 |
| T5 | Container / lightweight isolation (namespace·cgroup, microkernel, unikernel, sandbox, Wasm) | 45 | 27 |
| T6 | Accelerator virtualization (GPU, MIG/MPS, FPGA, NPU, accelerator sharing) | 41 | 16 |
| T7 | Confidential / security isolation (confidential VM, trusted I/O, firmware, hypervisor 검증) | 33 | 22 |
| T8 | Serverless / cloud abstraction | 5 | 0 |
| T9 | Resource management / multi-tenancy | 14 | 1 |
| T10 | Boundary / other | 6 | 2 |

## 2. 분포가 말해주는 것

**T5가 가장 크고(45), CORE 비율도 높다(27/45).** 경량 격리는 현재 가장 경쟁이 치열한 영역이며,
5개 계열(microkernel / unikernel / in-process MPK·CHERI / Wasm / VM-backed)이 병렬 경쟁한다.

**T9는 primary 14건인데 secondary가 63건이다.** 이 비대칭 자체가 결론이다. resource management는
**독립 연구 주제라기보다 다른 기여를 가진 논문의 부차적 성격**이다. T9를 primary로 갖는 논문은
거의 전부 SUPPORT 정책 논문이고(CORE는 Mosaic 1건), 진짜 CORE급 자원 관리 기구
(Memstrata, SweetspotVM, OSMOSIS, PeRF, Demeter, Blowfish)는 모두 T1/T2/T3 아래에 있다.

**T8은 primary 5건뿐인데 CORE는 0이다.** serverless 논문이 없어서가 아니라, 분류 정책이
serverless를 **기구**(그 기구의 taxonomy로 감)와 **소비**(CONTEXT로 감)로 갈랐기 때문이다.
T8에 남은 5건은 어느 쪽으로도 환원되지 않는 순수 추상화 논문이다.

**T1은 13건 전부가 CORE다.** 이 영역은 SUPPORT가 성립하기 어렵다 — hypervisor/vCPU를 건드리면
그 자체가 CORE이고, 건드리지 않으면 T1이 아니다.

## 3. 판정이 어려웠던 경계와 이 corpus가 채택한 선

실제로 반복해서 문제가 된 6개 경계다. 재현성을 위해 기록한다.

1. **VM/container 안에서 돌아간다 ≠ virtualization 논문.**
   이것이 가장 흔한 false positive다. 배제 사유 `no_virtualization_relation`(19건)의 다수.

2. **GPU sharing: 기존 MIG/MPS 위 정책 = SUPPORT / 새 virtual GPU abstraction = CORE.**
   SUPPORT 예: Orion, ParvaGPU, ESG, KACE, Tally, FluidFaaS, Priority-Aware GPU Co-Scheduling.
   CORE 예: Nixie(temporal multiplexing 기구), gShare(VM passthrough vGPU),
   gVulkan(API forwarding pooling), PhoenixOS·gCROP(GPU state checkpoint).

3. **container image/build/pull = SUPPORT / isolation boundary 재설계 = CORE.**
   SUPPORT: XaaS Containers, coMtainer, EDDE, BLAFS, FaaSImage.
   CORE: MettEagle, HongMeng, LiteShield, SKernel, uIO, ConMonitor.

4. **serverless: 격리를 싸게 만드는 기구 = CORE/SUPPORT / serverless를 쓰는 시스템 = CONTEXT.**
   기구: Sabre, SURE, Faascale, Squeezy, AlloyStack, Dandelion, Spice, PASS.
   소비: scheduling, workflow, cost, carbon, LLM serving 계열 전부.

5. **disaggregation(CXL/far memory): pool 위에 virtual resource abstraction을 세워야 CORE.**
   CORE: Blowfish, Memstrata, Demeter, Oasis.
   SUPPORT: FineMem, Nomad, Atlas, TrackFM, TECO, PIPM, Cxlalloc.
   DROP: SMART, COAXIAL(스스로 abstraction을 만들지 않는다고 명시).

6. **pure virtual memory = DROP, 단 nested translation·guest physical address space·
   hypervisor 매개 memory를 건드리면 CORE.**
   DROP 12건(Marching Page Walks, OASIS, Learning to Walk, SoftWalker, LATPC, ARIADNE, Avatar,
   SUV, ExtMem, Hydra, FBMM, FlexMem).
   **결정적 대조 사례:** MICRO24 "Elastic Translations"는 위 논문들과 제목·session이 거의
   구분되지 않지만, 전문 확인 결과 KVM nested(stage-2) page table을 직접 관리한다 → CORE 유지.
   **제목만으로 분류했다면 이 논문은 버려졌을 것이다.**

## 4. 배제 사유 분포

| 사유 | 건수 |
|---|---|
| no_virtualization_relation | 19 |
| keyword_false_positive | 13 |
| pure_virtual_memory | 12 |
| publication_criterion | 2 |
| already_analysed_no_delta | 1 |
| generic_application | 1 |

DROP 총 48건은 검토 410건의 12%에 불과하다. 이는 의도된 결과다 —
**aggressive pruning이 아니라 broad preservation**이 이 corpus의 방침이다.

## 5. 출판 유형 분리

정규 연구 통계에 섞지 않고 별도 보존한 항목:

- `OPERATIONAL_REFERENCE` 3건 — OSDI 2026 Operational Systems track
  (What Are You (M)Waiting For / DVLA / Stop Pretending to Be Busy).
  이 중 mwait-sched는 hypervisor 수준 vCPU idle 기구로서 기술적으로는 CORE급이나,
  트랙 구분상 정규 연구 통계에서는 제외된다.
- `INDUSTRY_TRACK` 3건 — eGPU(HPCA26, 1만 GPU 규모 탄력 공유), LightPool(HPCA24),
  Serverful Functions(Middleware24).
- `SHORT_PAPER` 3건 — CPU-Limits kill Performance(SoCC25, vision paper로 확인),
  svc-hook(Middleware25), Incorporating Memory Sharing-awareness(CCGrid24 Doctoral Symposium).
- `UNKNOWN` 22건 — 대부분 SoCC 2024. ACM DL 차단으로 full/short/industry/vision track
  구분을 확인하지 못했다. **추정하지 않고 UNKNOWN으로 남겼다.**

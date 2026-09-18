# READING_ROADMAP — virtualization 학습 커리큘럼

이 문서는 논문 목록이 아니라 **읽는 순서**다. 목표는 "하나의 core virtualization 논문을 읽을 때
그 기술적 배경, 아래/위 계층, 대안 기구, trade-off, 실제 cloud/HPC 사용까지 함께 이해하는 것"이다.

각 논문 뒤의 대괄호는 **실제 확보한 증거 수준**이다. `[FULL]`·`[DESIGN_EVAL]`은 설계와 평가까지
읽은 것이고, `[ABSTRACT]`는 초록 수준에서만 확인한 것이다. **초록 수준 논문은 개념 배치용으로만
쓰고, 인용이 필요하면 원문을 직접 확인해야 한다.**

---

## Stage 1 — VM 기본기: hypervisor, vCPU, guest-host 상호작용

**선행 개념:** privileged/unprivileged mode, trap-and-emulate, VM exit/entry, EPT(2단계 주소 변환)

읽는 이유: 이후 모든 계층이 "guest가 무엇을 알고, host가 무엇을 통제하는가"의 변주다.
이 경계를 먼저 손에 익혀야 T2~T7이 같은 문제의 다른 얼굴로 보인다.

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-EUROSYS25-04 Optimizing Task Scheduling in Cloud VMs with Accurate vCPU Abstraction `[FULL]` | vCPU가 물리 CPU가 아니라는 사실이 guest scheduler를 어떻게 망가뜨리는가. guest-host 정보 비대칭의 교과서적 사례 |
| VIRT-ATC25-02 Accelerating Nested Virtualization with HyperTurtle `[FULL]` | L0/L1/L2 world switch 비용의 해부. nested가 왜 비싼지를 수치로 |
| VIRT-OSDI26-01 JANUS: Cross-World, Cooperative Nested Virtualization `[DESIGN_EVAL]` **P0** | nested virtualization이 성능 문제에서 **보안 container 구현 수단**으로 재해석되는 전환점 |
| VIRT-CCGRID24-01 SweetspotVM `[DESIGN_EVAL]` | CPU oversubscription — 자원을 실제로 "초과 배분"한다는 것의 의미 |
| VIRT-OSDI26-04 Inside Out: A Paradigm Shift In VM Introspection `[DESIGN_EVAL]` | 바깥에서 guest 내부를 관찰하는 문제(semantic gap) |

**핵심 trade-off:** transparency ↔ co-design. guest를 수정하지 않으면 정보가 없고,
수정하면 배포가 어렵다. 이 축은 Stage 2에서 훨씬 날카로워진다.

**인접 관계:** Stage 2는 이 경계 위에 memory를, Stage 3은 device를 얹는다.

---

## Stage 2 — Memory virtualization: guest memory와 회수

**선행 개념:** GVA → GPA → HPA 2단계 변환, EPT/NPT, page pinning, huge page, ballooning

읽는 이유: virtualization에서 가장 활발하게 기구가 교체된 영역이며, Stage 3의 passthrough
문제와 정면으로 충돌하는 지점이다.

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-EUROSYS25-03 HyperAlloc `[FULL]` | **이 corpus의 최대 hub 논문(관계 11개).** ballooning vs free-page-reporting vs virtio-mem vs shared allocator의 설계 공간 전체를 한 논문에서 비교한다. 그리고 device passthrough(IOMMU pinning)가 왜 고전 ballooning을 깨뜨리는지를 보여준다 |
| VIRT-OSDI24-02 Managing Memory Tiers with CXL in Virtualized Environments `[FULL]` **P0** | disaggregation이 virtualization과 만나는 지점. host가 hotness와 배치 권한을 모두 쥐는 설계 |
| VIRT-ATC24-20 Taming Hot Bloat Under Virtualization with HugeScope `[FULL]` | huge page와 EPT가 만드는 낭비. 입자도(granularity) 문제 |
| VIRT-OSDI26-05 Blowfish `[DESIGN_EVAL]` | guest가 추적하고 host가 옮기는 **혼합 권한** 모델 |
| VIRT-OSDI26-03 Compaction-Free Memory Defragmentation (InfiniDefrag) `[DESIGN_EVAL]` | guest physical address space 자체를 자원으로 재정의 |
| VIRT-ASPLOS24-01 Direct Memory Translation for Virtualized Clouds `[FULL]` | 2단계 변환 비용을 하드웨어에서 줄이는 접근 |

**핵심 trade-off:** 회수 속도 ↔ guest 투명성. HyperAlloc은 guest allocator 교체를 요구하고
(빠르지만 침습적), virtio-mem은 투명하지만 느리다. Demeter는 guest에 위임하고 Memstrata는
host가 독점한다. **같은 문제에 대한 권한 배분의 스펙트럼**으로 읽어라.

**인접 관계:** ↓ Stage 1의 EPT 위에 서고, ↑ Stage 8의 serverless memory elasticity로 올라간다.
Stage 3(passthrough)과는 **직접 충돌**한다.

---

## Stage 3 — I/O virtualization: DMA, IOMMU, SR-IOV, passthrough

**선행 개념:** DMA, IOMMU/SMMU, PCIe, SR-IOV PF/VF, virtio, PASID

읽는 이유: virtualization에서 **가장 고전적이고 가장 잘 정의된 trade-off**가 여기 있다.

```
passthrough → software mediation 비용 하락
            → 그러나 isolation, memory management, live migration이 모두 어려워진다
```

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-SOSP24-02 VPRI: Efficient I/O Page Fault Handling `[FULL]` **P0** | passthrough가 강제하는 static pinning이 운영 환경에서 DRAM을 얼마나 낭비하는지를 실측으로 제시. **이 Stage의 문제 정의 논문** |
| VIRT-SOSP24-03 Fast & Safe IO Memory Protection `[FULL]` **P0** | IOMMU 보호를 싸게 만드는 방향 |
| VIRT-OSDI25-01 To PRI or Not To PRI `[DESIGN_EVAL]` **P0** | PCIe PRI/IOPF로 overcommit을 되찾으려는 시도와 그 한계 |
| VIRT-EUROSYS24-01 HD-IOV `[DESIGN_EVAL]` | SR-IOV의 고정 VF 천장을 software-mediated PASID/queue-pair로 돌파 |
| VIRT-ASPLOS26-01 SG-IOV `[DESIGN]` | 같은 천장을 socket 단위 하드웨어 분할로 돌파. HD-IOV의 **후속 계보** |
| VIRT-EUROSYS25-01 FastIOV `[ABSTRACT]` | passthrough의 *시작 지연* 문제(secure container와 결합) |
| VIRT-ATC24-06 OSMOSIS / VIRT-EUROSYS24-04 S-NIC `[DESIGN_EVAL]`/`[FULL]` | SmartNIC multi-tenancy — device 자체가 공유 자원이 될 때 |

**핵심 trade-off:** 위 박스 그대로. 각 논문이 세 부작용(isolation/memory/migration) 중
**어느 쪽을 공격하는지**를 표로 만들며 읽으면 이 Stage가 한 번에 정리된다.

**인접 관계:** ↓ Stage 2의 pinning 문제와 직결, ↑ Stage 4의 device state migration으로 이어진다.

---

## Stage 4 — Migration과 state: 무엇이 "상태"인가

**선행 개념:** pre-copy / post-copy, dirty page tracking, CRIU, device state

읽는 이유: 앞선 세 Stage에서 만든 abstraction이 **옮겨질 수 있는가**를 묻는 단계다.
virtualization state가 어디에 있는지 모르면 migration을 이해할 수 없다.

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-EUROSYS26-04 Everything You Need to Know About VM Live Migration Between Heterogeneous Processors `[ABSTRACT]` **P0** | 이 Stage의 지도 역할. **단, 초록 수준 증거이므로 반드시 원문 확인 필요** |
| VIRT-OSDI26-02 M3U `[DESIGN_EVAL]` | post-copy migration을 대형 VM으로 확장할 때 kernel memory 관리가 병목이 된다는 발견 |
| VIRT-CCGRID24-02 Tackling Memory Footprint Expansion (SLM) `[DESIGN_EVAL]` | migration이 copy-on-write page sharing을 파괴한다 — "상태"의 범위가 생각보다 넓다 |
| VIRT-SOSP25-01 Device-Assisted Live Migration of RDMA Devices `[ABSTRACT]` | passthrough device state를 device 협조로 옮기는 접근. **증거 최약체(mechanism 필드 UNKNOWN)** |
| VIRT-SOSP25-06 PhoenixOS `[DESIGN_EVAL]` | GPU checkpoint/restore — 가속기에도 같은 문제가 반복됨 |
| VIRT-SOCC24-08 PCLive `[DESIGN_EVAL]` | container 복원의 의존성 순서 문제 |

**핵심 trade-off:** state locality ↔ migratability. 상태를 device 가까이 둘수록 빠르지만
옮기기 어렵다. Oasis(SOSP25)는 **migration 자체를 없애는** 세 번째 답(CXL device pooling)이다.

---

## Stage 5 — 경량 격리: container, microkernel, unikernel, sandbox, Wasm

**선행 개념:** namespace/cgroup, seccomp, syscall 경계, MPK, CHERI, Wasm sandbox

읽는 이유: corpus에서 **가장 큰 CORE 집단(45건 중 27건 CORE)** 이며, 5개 계열이 병렬 경쟁 중이다.
승자를 찾지 말고 **각 계열이 무엇을 희생하는지**를 읽어라.

| 논문 | 계열 | 무엇을 가르치는가 |
|---|---|---|
| VIRT-OSDI25-03 MettEagle `[FULL]` **P0** | microkernel | container를 microkernel 위에 올렸을 때의 **비용과 이득을 정량화**. 이 Stage의 기준점 |
| VIRT-OSDI24-03 HongMeng (Microkernel Goes General) `[FULL]` | microkernel | 상용 규모 microkernel의 성능·호환성 |
| VIRT-SOCC24-05 uIO `[DESIGN_EVAL]` | unikernel | unikernel의 확장성 문제와 MPK 기반 해법 |
| VIRT-EUROSYS25-16 Empowering WebAssembly with Thin Kernel Interfaces `[FULL]` | Wasm | Wasm sandbox에 커널 인터페이스를 주는 대가 |
| VIRT-EUROSYS25-17 A Hardware-Software Co-Design for Efficient Secure Containers `[FULL]` | VM-backed | VM 격리 강도를 container 밀도로 얻으려는 시도 |
| VIRT-ATC24-08 Limitations and Opportunities of Modern Hardware Isolation Mechanisms `[DESIGN_EVAL]` | (횡단) | MPK/CHERI 등 하드웨어 격리 기구의 한계를 비교. **계열 간 비교 기준을 제공** |
| VIRT-OSDI25-10 Extending Applications Safely and Efficiently (bpftime) `[FULL]` | in-process | 확장 코드의 격리 — eBPF 계열 |

**핵심 trade-off:** 격리 강도 ↔ 시작 지연 ↔ 호환성. 세 꼭짓점 중 둘만 고를 수 있다는 것이
이 Stage 전체의 구조다.

---

## Stage 6 — 가속기 virtualization: GPU, MIG/MPS, FPGA, NPU

**선행 개념:** CUDA stream, MPS, MIG, GPU context, FPGA shell/partial reconfiguration

읽는 이유: virtualization 기법이 CPU에서 **다른 자원으로 이식되는 과정**을 실시간으로 볼 수 있다.
CPU virtualization의 개념(분할, 선점, 상태 이동, passthrough)이 그대로 반복된다.

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-OSDI26-06 Nixie `[FULL]` **P0** | transparent temporal multiplexing — GPU에 "시분할"을 제대로 구현한다는 것의 의미 |
| VIRT-MICRO24-01 Hardware-Assisted Virtualization of NPUs (vNPU/NeuISA) `[FULL]` **P0** | CPU virtualization의 하드웨어 지원 개념을 NPU로 이식. **가장 명시적인 개념 이식 사례** |
| VIRT-SOCC25-05 Funky `[FULL]` **P0** | FPGA virtualization + orchestration |
| VIRT-HPDC25-01 F3 `[FULL]` **P0** | FPGA를 FaaS 자원으로 — Stage 8과의 다리 |
| VIRT-ATC25-03 Efficient Performance-Aware GPU Sharing via Kernel Space Interception `[DESIGN_EVAL]` | 기존 MIG/MPS 위가 아니라 **kernel 공간에서 가로채는** 접근 |
| VIRT-SOSP25-10 Coyote v2 `[DESIGN_EVAL]` | datacenter FPGA의 추상화 수준을 올리기 |
| VIRT-OSDI25-11 XSched `[DESIGN_EVAL]` | 이종 XPU 선점 스케줄링 — 선점이 왜 어려운가 |

**주의 — 분류 함정:** GPU "공유" 논문 대다수는 CORE가 아니라 SUPPORT다. 기존 MIG/MPS 위에
정책을 얹은 것과, **새로운 virtual GPU abstraction**을 만든 것은 다르다. 이 구분을 의식하며 읽어라.

**인접 관계:** ↓ Stage 3의 passthrough(gShare는 VM passthrough vGPU), ↓ Stage 4의 state
(PhoenixOS), ↑ Stage 8의 serverless GPU.

---

## Stage 7 — Confidential virtualization: 신뢰 경계

**선행 개념:** TEE, enclave, attestation, AMD SEV-SNP, Intel TDX, Arm CCA, TCB

읽는 이유: "격리"가 성능 격리에서 **보안 격리**로 바뀌면 hypervisor 자신이 위협 모델에
포함된다. 앞 Stage의 모든 가정이 재검토된다.

| 논문 | 무엇을 가르치는가 |
|---|---|
| VIRT-OSDI24-04 VeriSMo `[FULL]` **P0** | confidential VM security module의 **형식 검증**. hypervisor를 믿지 않는다는 것의 의미 |
| VIRT-ATC24-22 CPC `[FULL]` **P0** | CVM을 운영(유지보수)한다는 현실 문제 — 신뢰 경계가 불투명해지면 운영이 어려워진다 |
| VIRT-SOSP25-04 The Design and Implementation of a Virtual Firmware Monitor `[DESIGN_EVAL]` **P0** | firmware 계층의 virtualization |
| VIRT-MICRO25-01 ccAI `[DESIGN_EVAL]` | **신뢰 사슬이 PCIe를 넘어 GPU/NPU/FPGA로 확장되는 첫 사례** |
| VIRT-ASPLOS25-02 HyperHammer `[DESIGN_EVAL]` | KVM이 강제하는 격리를 Rowhammer로 깨뜨림 — 공격 관점 |
| VIRT-HPCA26-05 DSAssassin `[ABSTRACT]` | Intel Scalable IOV의 inter-VM 격리를 device TLB로 우회. Stage 3의 가정이 무너지는 지점 |

**핵심 trade-off:** TCB 크기 ↔ 호환성/성능. 신뢰 기반을 줄이면 검증 가능하지만 쓰기 어렵다.

**이 Stage의 구조적 특징:** 정확성 검증 계열 논문들은 서로 계승 관계가 희박하다
(relation graph에서 T7 논문 10편이 고립). **누적적이 아니라 병렬적인 분야**로 읽어야 한다.

---

## Stage 8 — Cloud abstraction: serverless, oversubscription, provisioning

**선행 개념:** cold start, microVM(Firecracker), snapshot/restore, warm pool

읽는 이유: 앞의 모든 기구가 **왜 필요했는지**를 보여주는 수요 측 계층이다.

**반드시 구분할 것:**
- (a) **격리를 싸게 만드는 기구** — 읽을 가치 높음
- (b) **serverless를 소비하는 시스템**(scheduling, workflow, cost, carbon, LLM serving) — 사용 맥락용

| 논문 | 구분 | 무엇을 가르치는가 |
|---|---|---|
| VIRT-OSDI24-01 Sabre `[DESIGN_EVAL]` | (a) | snapshot 압축을 하드웨어로 — cold start의 물리적 한계 |
| VIRT-SOSP25-08 Dandelion `[DESIGN_EVAL]` | (a) | cloud-native 탄력성의 경계 재설계 |
| VIRT-EUROSYS25-14 AlloyStack `[FULL]` | (a) | library OS로 workflow 전체를 한 주소 공간에 |
| VIRT-SOCC24-10 Faascale `[DESIGN]` | (a) | microVM 수직 memory scaling — Stage 2와 직결 |
| VIRT-OSDI26-11 Rethinking Process Snapshots (Spice) `[DESIGN_EVAL]` | (a) | VM이 아니라 **process** 경계 snapshot |
| VIRT-OSDI25-05 Fork in the Road `[DESIGN_EVAL]` | (b→a 경계) | 실제 운영 serverless의 cold start 실측 |

---

# 필수 독서 경로 — 20편

전체 362편을 다 읽을 필요는 없다. **아래 20편이면 virtualization stack 전체의 골격이 선다.**
선정 기준: (1) 각 Stage를 대표할 것, (2) 증거 수준이 확실할 것(대부분 FULL/DESIGN_EVAL),
(3) 다른 논문으로 이어지는 관계 밀도가 높을 것.

| # | id | 논문 | Stage | 증거 |
|---|---|---|---|---|
| 1 | VIRT-EUROSYS25-04 | Accurate vCPU Abstraction | 1 | FULL |
| 2 | VIRT-ATC25-02 | HyperTurtle (nested) | 1 | FULL |
| 3 | VIRT-OSDI26-01 | JANUS (nested + secure container) | 1 | DESIGN_EVAL |
| 4 | **VIRT-EUROSYS25-03** | **HyperAlloc** — corpus 최대 hub | 2 | FULL |
| 5 | VIRT-OSDI24-02 | Memstrata (CXL in virtualized env) | 2 | FULL |
| 6 | VIRT-OSDI26-05 | Blowfish (elastic VM memory) | 2 | DESIGN_EVAL |
| 7 | VIRT-ATC24-20 | HugeScope | 2 | FULL |
| 8 | **VIRT-SOSP24-02** | **VPRI** — passthrough 문제 정의 | 3 | FULL |
| 9 | VIRT-OSDI25-01 | To PRI or Not To PRI | 3 | DESIGN_EVAL |
| 10 | VIRT-EUROSYS24-01 | HD-IOV | 3 | DESIGN_EVAL |
| 11 | VIRT-ASPLOS26-01 | SG-IOV (HD-IOV 후속) | 3 | DESIGN |
| 12 | VIRT-OSDI26-02 | M3U (post-copy migration) | 4 | DESIGN_EVAL |
| 13 | VIRT-SOSP25-06 | PhoenixOS (GPU checkpoint) | 4 | DESIGN_EVAL |
| 14 | **VIRT-OSDI25-03** | **MettEagle** — 경량 격리 비용/이득 정량화 | 5 | FULL |
| 15 | VIRT-EUROSYS25-17 | HW-SW Co-Design for Secure Containers | 5 | FULL |
| 16 | VIRT-ATC24-08 | Limitations of Modern HW Isolation Mechanisms | 5 | DESIGN_EVAL |
| 17 | VIRT-OSDI26-06 | Nixie (GPU temporal multiplexing) | 6 | FULL |
| 18 | VIRT-MICRO24-01 | vNPU/NeuISA (개념 이식) | 6 | FULL |
| 19 | **VIRT-OSDI24-04** | **VeriSMo** — hypervisor를 믿지 않기 | 7 | FULL |
| 20 | VIRT-MICRO25-01 | ccAI (신뢰 경계의 PCIe 확장) | 7 | DESIGN_EVAL |

**추천 순서:** 4 → 8 → 14 → 19 를 먼저 읽어라. 이 네 편이 각각 memory·I/O·격리·신뢰의
**문제 정의**를 담고 있어서, 나머지 16편이 어디에 붙는지가 보인다. 그 다음 Stage 순서대로 진행.

시간이 더 있다면 Stage 8에서 VIRT-OSDI24-01(Sabre)과 VIRT-SOCC24-10(Faascale)을 추가하라 —
앞의 모든 기구가 왜 필요했는지가 수요 측에서 설명된다.

> **주의:** 이 20편은 학습 경로이지 corpus의 축약본이 아니다. SUPPORT·CONTEXT 계층
> (총 238편)은 특정 가지를 깊게 팔 때 내려가기 위해 **그대로 보존되어 있다.**
> 각 topic 파일의 4절(Supporting 논문)이 그 진입점이다.

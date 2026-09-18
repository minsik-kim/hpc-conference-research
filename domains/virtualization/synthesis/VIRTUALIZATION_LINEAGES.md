# Virtualization Lineages (2024–2026 코퍼스)

이 문서는 `PAPER_RELATIONS.csv`에 기록된 330개 관계(relation_type + basis)를 근거로,
228편의 CORE/SUPPORT 논문 중 실제로 같은 문제를 놓고 서로 다른 세대의 메커니즘으로
이어지는 **강한 lineage**만 골라낸 것이다. 각 링크에는 관계 타입과 근거 문장을 함께
표기했다. relation이 명시적 citation/baseline 비교(같은 시스템을 직접 구현·측정하거나,
논문이 명시적으로 선행연구를 프레이밍)에 근거하면 태그를 붙이지 않았고, basis가
"같은 학회/연도/저자 그룹이라 묶었다"는 식의 주제적 군집화에 불과하면 `[INFERENCE]`로
표시했다. 208편이 아니라 60~80편만 다루는 것은 의도된 선택이다 — 나머지는
`CROSS_PAPER_RELATIONS.md`의 "연결이 약한 부분" 절에서 별도로 다룬다.

---

## Lineage A — VM 메모리 탄력성 (ballooning → co-designed allocator → disaggregated tiering)

**공격 대상 문제**: guest-physical memory를 런타임에 늘리고 줄이는 것(VM memory
elasticity)은 hypervisor가 제공하는 가장 오래된 약속 중 하나지만, 기존 메커니즘은
모두 구조적 결함이 있다 — virtio-balloon은 느리고 guest가 swap/OOM에 빠질 위험이
있으며, virtio-mem은 더 빠르지만 자동 회수가 없고, 두 방식 모두 passthrough 장치의
IOMMU pinning과 충돌한다. 이 lineage는 코퍼스에서 **가장 근거가 촘촘한 lineage**다
(HyperAlloc이 combined-degree 11로 코퍼스 전체 1위 hub).

1. **베이스라인(외부 메커니즘)**: virtio-balloon / virtio-mem — 여러 논문이 baseline으로
   직접 구현·측정.
2. **VIRT-EUROSYS25-03 | HyperAlloc (EuroSys25, 2025)** — guest의 Linux buddy allocator를
   LLFree로 교체하고 그 압축된 페이지-프레임 상태를 QEMU monitor에 메모리 매핑해
   guest·hypervisor가 원자적으로 공유. `ALTERNATIVE → virtio-balloon/virtio-mem`
   ("directly implemented and measured as baselines; HyperAlloc replaces the balloon
   device protocol with shared allocator state"). 20GiB VM 기준 회수 처리량
   344.8 GiB/s vs virtio-mem 34 GiB/s vs virtio-balloon 0.95 GiB/s (Intel Xeon Gold 6252 ×2).
   대가는 guest transparency 상실(buddy allocator 교체 필요) — **co-design 갈래의 시작점**.
3. 같은 시기 **다른 해법으로 같은 문제를 공격**하는 형제 논문들 (모두 관계 타입은
   ALTERNATIVE/SAME_BRANCH로 HyperAlloc과 명시적으로 연결됨):
   - **VIRT-SOCC24-07 | Continuous Ballooning (SoCC24, 2024)** — 기존 balloon
     프로토콜은 유지하되 실시간 조율 로직을 추가해 migration 도중에도 안전하게 함.
     `ALTERNATIVE → HyperAlloc` ("two different fixes to the same 'ballooning is
     risky/slow' problem"). 최대 8% 오버헤드로 giant VM(≈600GB) migration을 52%+ 가속.
   - **VIRT-ATC25-14 | Para-ksm (ATC25, 2025)** — 회수가 아니라 same-page merging
     (dedup)으로 footprint를 줄임. `SAME_BRANCH → HyperAlloc` ("complementary points
     in the T2 reclamation design space"). DSA 오프로드로 애플리케이션 슬로다운을
     3.3x→2.1x로 완화.
   - **VIRT-EUROSYS26-05 | Squeezy (EuroSys26, 2026)** — 문제를 microVM 기반
     serverless로 좁혀, guest 내부에서 hotplug된 메모리와 일반 메모리를 분리·수명
     제한. `ALTERNATIVE → HyperAlloc` ("different mechanisms for the same
     overhead_bottleneck"). Sub-second 다중-GB 회수.
   - **VIRT-SOCC24-10 | Faascale (SoCC24, 2024)** — 동일한 "런타임 VM 메모리 탄력성"
     목표를 KVM 풀사이즈 VM이 아니라 Firecracker microVM에 적용(vertical scaling).
     `SAME_BRANCH → HyperAlloc` ("same taxonomy branch (T2), different VM weight class").
4. **Guest 수정 없이 같은 문제를 해결하는 대안 갈래**: **VIRT-OSDI25-01 | VIO
   ("To PRI or Not To PRI", OSDI25, 2025, P0)** — hypervisor 안에서 VirtIO ring을
   proactive하게 snooping해 IOPF를 critical path에서 제거, guest는 완전히 무수정.
   `CONTRASTS_WITH → HyperAlloc` ("HyperAlloc ... treats passthrough as the case that
   breaks classic ballooning; VIO instead keeps the guest completely unmodified and
   solves the same passthrough-vs-overcommitment conflict entirely inside the
   hypervisor"). 실제 300K VM/300 node 프로덕션 배포, 하루 ~120GB 메모리 회수 —
   **transparency vs co-design 트레이드오프의 실증 사례**(`VIRTUALIZATION_TRADEOFFS.md` §4 참조).
5. **Guest-delegated tiering으로의 분기**: **VIRT-SOSP25-02 | Demeter (SOSP25, 2025)** —
   hot/cold 분류·승격을 guest kernel에 완전히 위임하고 hypervisor는 capacity
   arbitration만 담당. `SAME_BRANCH → HyperAlloc` ("both are guest-hypervisor
   cooperative memory mechanisms in the ballooning/virtio-mem lineage" — 코퍼스
   자체가 이 lineage를 명명함). Demeter는 다시 `ALTERNATIVE → VIRT-SOSP25-16`
   (Scalable Far Memory, host-side 완전 처리)와 대비된다("두 opposite answers to
   where memory-expansion policy belongs").
6. **Lineage의 현재 지점**: **VIRT-OSDI26-05 | Blowfish (OSDI26, 2026)** — Demeter의
   "guest에 전체 tiering 위임"과 정면으로 대비된다. guest는 hotness tracking만 하고
   host가 EPT-only 재배치를 subpage 단위로 수행. `CONTRASTS_WITH → Demeter`
   ("Demeter delegates the full tiering pipeline ... at 2MB granularity requiring
   GPT/IOPT updates; Blowfish keeps only hotness tracking in the guest and does all
   data movement/EPT-only reclamation on the host at subpage granularity"). HyperAlloc
   계열 대비 회수/복원 지연 53–60% 감소(14.5us/9.8us vs 36us/21us). Blowfish는 다시
   RDMA far-memory 백엔드 Hermit을 `USES_MECHANISM_FROM`으로 재사용하며,
   `SAME_BRANCH → VIRT-EUROSYS26-08`(MTTM, 멀티테넌트 fast-tier 파티셔닝)과
   "같은 CXL/RDMA-disaggregated-memory stack의 상보적 계층"을 이룬다.
7. **디스어그리게이션으로의 최종 확장**: **VIRT-OSDI25-08 | FineMem (OSDI25, 2025)** —
   guest-physical translation layer 없이 원격 RDMA pool에서 직접 fine-grained 할당.
   `CONTRASTS_WITH → HyperAlloc` ("the same T2 memory-management problem addressed
   with and without a virtualization abstraction" — 즉 이 lineage가 어디서 끝나고
   순수 disaggregation 문제로 넘어가는지의 경계). **VIRT-SOSP25-05 | Oasis (SOSP25,
   2025)**는 메모리가 아니라 PCIe 장치 자체를 CXL 위에 풀링하며
   `SAME_BRANCH → VIRT-SOSP25-16`("both extend a host's resources across a fabric")로
   같은 계열에 합류한다.

**Lineage 강도**: 강함(strong) — 8개 논문이 서로를 직접 인용/측정하며 명시적으로
연결되어 있고, 코퍼스 자체 basis 문장이 "ballooning/virtio-mem lineage"라는 표현을
두 번 사용한다. HyperAlloc(EuroSys25)이 이 lineage의 축이며, Blowfish(OSDI26)가
현재 최전선이다. FineMem/Oasis로의 확장은 `CONTRASTS_WITH`(즉 같은 문제의 경계를
보여주는 대비)이지 직접적 계승은 아니므로 "lineage의 끝"으로 표시했다.

---

## Lineage B — I/O 가상화의 확장성 한계 (SR-IOV VF 천장 → PASID 소프트웨어 매개 → 소켓 단위 하드웨어 파티셔닝)

**공격 대상 문제**: SR-IOV는 물리 함수당 가상 함수(VF) 개수가 하드웨어적으로
고정되어(수백 개 수준) 고밀도 멀티테넌트 호스트의 컨테이너/소켓 수를 감당하지 못한다.

1. **VIRT-EUROSYS24-01 | HD-IOV (EuroSys24, 2024)** — 가상화·자원관리 로직을 하드웨어에서
   분리해 소프트웨어로 옮기고, PCIe PASID로 IOMMU가 격리를 강제하게 함. SR-IOV 대비
   동일 NIC/QAT에서 최대 2.96배 더 많은 가상 장치, 2.9배 빠른 초기화(Intel Sapphire
   Rapids + E810 NIC).
2. **VIRT-ASPLOS26-01 | SG-IOV (ASPLOS26, 2026)** — `PRECURSOR ← HD-IOV`
   ("HD-IOV's software-mediated, PASID/queue-pair-level isolation is a direct
   architectural predecessor to SG-IOV's socket-granular hardware partitioning").
   가상화 단위를 PCIe function에서 **소켓** 단위로 내려, 동일 NIC 하드웨어에서
   3자릿수(three-orders-of-magnitude) 더 높은 가상 엔드포인트 밀도를 확보하면서도
   데이터 경로는 여전히 하드웨어 가속. `ALTERNATIVE → SR-IOV`
   ("explicitly frames its contribution as overcoming SR-IOV's per-NIC
   virtual-function scalability ceiling"). `SAME_BRANCH → VIRT-EUROSYS25-01`
   (FastIOV) — "둘 다 SR-IOV/passthrough가 남긴 컨테이너-스케일 네트워크 I/O
   가상화 문제를 겨냥".
3. **병렬 갈래 — passthrough 자체의 시작 비용**: **VIRT-EUROSYS25-01 | FastIOV
   (EuroSys25, 2025)** — SR-IOV passthrough를 유지한 채 attach 경로의 lock
   분해·DMA mapping 제거·메모리 zeroing 분리로 시작 비용만 낮춤. SR-IOV 활성화
   오버헤드 96.1% 감소, 시작 시간 평균 65.7%/P99 75.4% 감소(공식 abstract 수치).
   `TRADEOFF_PAIR → VIRT-EUROSYS25-03`(HyperAlloc, passthrough 아래서의 memory
   reclaim)와 `TRADEOFF_PAIR → VIRT-EUROSYS25-06`(Byte vSwitch, software-mediated
   대안) — 세 논문이 "passthrough를 선택했을 때 치러야 할 대가"라는 하나의
   trade-off 삼각형을 형성.
4. **저장장치로의 같은 패턴 반복**: **VIRT-HPCA25-01 | NVMePass (HPCA25, 2025)** —
   제어 자원(설정공간·admin queue)은 trap-and-emulate, 데이터 자원(I/O queue·doorbell)은
   passthrough하는 하이브리드. `ALTERNATIVE → SR-IOV/SIOV/FVM`(하드웨어 의존 대안)과
   `ALTERNATIVE → SPDK vhost-NVMe/virtio-blk`(소프트웨어 매개 대안) 양쪽에 명시적으로
   대비됨. 단일 VM IOPS는 VFIO passthrough의 97.6–100.2%를 달성하면서, 200-VM
   밀도에서 SPDK vhost-NVMe 대비 31.4% 낮은 지연.

**Lineage 강도**: 중간(moderate) — HD-IOV→SG-IOV는 `PRECURSOR` 관계로 명시적으로
근거가 있으나 두 단계뿐이고, FastIOV/NVMePass는 "SR-IOV 천장" 문제의 다른 축(시작
지연, 저장장치)을 공격하는 **인접 가지**다. 하나의 단일 직선이라기보다, "SR-IOV의
한계"라는 공통 뿌리에서 갈라진 세 개의 짧은 가지로 보는 것이 정확하다.

---

## Lineage C — GPU 공유의 진화: MPS/MIG 조합 → 커널 수준 가로채기 → 선점 → checkpoint/restore → 풀링

**공격 대상 문제**: 하나의 물리 GPU를 여러 테넌트가 나눠 쓰는 문제는 이 코퍼스에서
가장 넓게 다뤄진 축이다(T6 41편 중 다수가 상호 연결). NVIDIA MIG(정적, GPC 단위,
하드웨어 격리)와 MPS(SM affinity, 약한 격리)가 공통 베이스라인이며, 거의 모든
후속 논문이 이 둘을 직접 구현·측정해 대비한다.

1. **베이스라인**: MIG/MPS(외부 메커니즘) — VIRT-EUROSYS25-07(Bless), VIRT-ATC25-03,
   VIRT-ASPLOS25-03(Tally), VIRT-ASPLOS25-06(Dilu), VIRT-SOSP25-14(LithOS),
   VIRT-SC24-01(ParvaGPU), VIRT-HPDC25-02(FluidFaaS), VIRT-CCGRID25-01,
   VIRT-MIDDLEWARE24-04(Guardian) 등이 모두 이를 baseline으로 직접 측정.
2. **커널 수준 가로채기 단계**: **VIRT-ATC25-03 | Efficient GPU Sharing via
   Kernel-Space Interception (ATC25, 2025)** — CUDA runtime 아래에서 command-buffer를
   가로채 호환성과 격리를 동시에 확보. `CONTRASTS_WITH → MIG/MPS/API-remoting(TGS,
   GaiaGPU, GSlice)`("directly implemented and measured as baselines"). 동일 처리량
   목표 달성에 순수 temporal sharing 대비 32.1% 더 적은 GPU, Best-fit-MIG 대비
   23.1% 더 적은 GPU. `SAME_BRANCH → VIRT-ATC25-05`(GPreempt, "both interpose on the
   GPU driver stack ... below the CUDA runtime").
3. **선점(preemption) 단계**: **VIRT-ATC25-05 | GPreempt (ATC25, 2025)** — 하드웨어
   timeslice 재구성으로 임의(non-idempotent) 커널에 대해 ~40us 선점 지연 달성.
   NVIDIA A100에서 지연-critical 태스크 지연 증가를 무선점 +58.4%→GPreempt +2.4%로
   축소. `SAME_BRANCH → VIRT-OSDI25-11 | XSched (OSDI25, 2025)` — "GPreempt는
   NVIDIA/AMD GPU timeslice 조작에 특화, XSched는 GPU/NPU/ASIC/FPGA 전반으로
   다층 선점 추상화를 일반화"(fixed-priority 스케줄링 시 P99 지연 2.10배 개선).
4. **checkpoint/restore 단계**: **VIRT-SOSP25-06 | PhoenixOS (SOSP25, 2025)** —
   launch argument로부터 커널 버퍼 접근을 추측(speculate)하고 계측으로 검증해
   동시적·투명한 GPU C/R을 제공, stop time ~1ms (stop-the-world 베이스라인 726ms
   대비). `USES_MECHANISM_FROM ← VIRT-SOSP25-07 | Aegaeon` — "Aegaeon의 빠른 모델
   전환은 정확히 PhoenixOS가 일반화한 GPU 상태 저장/복원 primitive를 필요로 한다;
   둘 다 KV cache/디바이스 버퍼를 migratable 단위로 취급."
5. **풀링(pooling) 단계 — lineage의 현재 두 극단**: **VIRT-SOSP25-07 | Aegaeon
   (SOSP25, 2025)** — token 단위(request 단위가 아님) autoscaling으로 GPU를 시간적으로
   재분배, 프로덕션에서 GPU당 최대 7개 모델·fleet 82% 절감. **VIRT-SOSP25-14 | LithOS
   (SOSP25, 2025)** — TPC(sub-GPC) 단위로 투명하게 **공간적** 파티셔닝하며
   atomized preemption 제공, MIG 대비 13배 tail-latency 감소. 두 논문은
   `CONTRASTS_WITH`로 서로를 직접 지목: "LithOS partitions one GPU spatially at TPC
   granularity with hardware-level isolation; Aegaeon multiplexes it temporally at
   token granularity with none — **the two poles of accelerator sharing**."
6. **FPGA로의 구조적 유비**: LithOS는 `SAME_BRANCH → VIRT-SOSP25-10 | Coyote v2
   (SOSP25, 2025)`와도 연결된다 — "both spatially partition an accelerator's fabric
   with per-partition hardware isolation," GPU의 TPC-masking과 FPGA의 shell 기반
   재구성 가능 영역이 동일한 설계 패턴임을 보여준다.
7. **생산 규모로의 확장**: **VIRT-HPCA26-02 | eGPU (HPCA26, 2026)** — 10,000+ GPU
   생산 배포, 최대 8배 GPU 절감·3배 이상 클러스터 이용률. `SAME_BRANCH →
   VIRT-ASPLOS26-02 | gShare (ASPLOS26, 2026)`(VM-passthrough vGPU + 서브-ms
   재할당) — 이 링크의 basis는 "둘 다 2026년 fine-grained GPU-sharing 시스템"이라는
   시기적 묶음이므로 `[INFERENCE]`로 표시한다.
8. **소비자용 GPU로의 별도 가지**: **VIRT-OSDI26-06 | Nixie (OSDI26, 2026, P0)** —
   demand-paged UVM 대신 명시적·조율된 working-set 전체 이전으로 temporal
   multiplexing. `CONTRASTS_WITH → UVM/nvshare/TGS`(명시적 3자 정량 비교, nvshare
   대비 인터랙티브 작업에서 3.1–3.8배 지연 개선) — 독립적인 온-디바이스 소비자 GPU
   갈래로, 데이터센터 계열과는 직접 연결되지 않는다.

**Lineage 강도**: 강함(broad) — 5단계(interception→preemption→checkpoint/restore→
pooling)가 모두 `SAME_BRANCH`/`CONTRASTS_WITH`/`USES_MECHANISM_FROM` 관계로 명시적
근거를 갖고 연결된다. 코퍼스 자체가 "the two poles of accelerator sharing"이라는
문구로 5단계 끝의 분기(Aegaeon vs LithOS)를 스스로 명명한다. 8번(eGPU–gShare)만
`[INFERENCE]`.

---

## Lineage D — Nested virtualization / secure container 비용의 세 가지 답 (가속 vs 회피 vs 협력)

**공격 대상 문제**: 기밀 컨테이너(secure container)가 필요로 하는 nested
virtualization(L0→L1→L2)은 비용이 크다. 코퍼스는 정확히 대립하는 두 해법과, 그
둘을 아우르는 제3세대 아키텍처를 기록한다.

1. **VIRT-ATC25-02 | HyperTurtle (ATC25, 2025)** — L0-L1-L2 world switch를 단축해
   nested virtualization 자체를 빠르게 만듦.
2. **VIRT-EUROSYS25-17 | CKI (EuroSys25, 2025)** — PKS로 guest kernel을 deprivilege해
   nested VMX 경로 자체를 회피. 두 논문은 `TRADEOFF_PAIR`로 서로를 직접 지목:
   "HyperTurtle makes nested virtualization cheaper; CKI avoids the nested VMX path
   altogether. **The two are the opposing answers to the same nested-cloud cost.**"
   CKI는 근접-네이티브 syscall과 1차원 페이징을 얻지만 컨테이너별 연속 물리 메모리
   요구(파편화 비용)를 치른다.
3. **CKI는 다시 `SAME_BRANCH → VIRT-EUROSYS25-05 | Erebor`**(같은 Intel PKS로
   guest kernel을 deprivilege하지만 목적은 secure-container 성능이 아니라 CVM
   내부 데이터 기밀성 — "the two papers bracket what PKS-based intra-kernel
   privilege separation is for").
4. **제3세대 — 협력적 아키텍처**: **VIRT-OSDI26-01 | JANUS (OSDI26, 2026, P0)** —
   VMCS/VMCB 처리·EPT 같은 하드웨어 지원 nested virtualization primitive 위에
   cooperative(협력적) 아키텍처를 구축, PVM과 표준 nested KVM 양쪽을 head-to-head로
   능가함을 실증(`ALTERNATIVE → PVM`). `LAYER_ABOVE → VIRT-EUROSYS26-03 | NecoFuzz
   (EuroSys26, 2026)` — JANUS가 딛고 선 바로 그 VMCS/VMCB 정합성을 NecoFuzz가
   fuzzing으로 검증("JANUS is a cooperative nested-virtualization architecture built
   on the same hardware-assisted nested-virtualization primitives ... that NecoFuzz
   fuzzes for correctness"). 이 역방향 관계는 NecoFuzz 쪽에서 `LAYER_BELOW → JANUS`로
   대칭 기록되어 있다.

**Lineage 강도**: 강함이지만 짧음(short-but-solid) — 4편뿐이나 관계 전부가
직접적 head-to-head 비교(HyperTurtle↔CKI) 또는 계층 관계(JANUS↔NecoFuzz)로
뒷받침된다.

---

## Lineage E — Passthrough 장치 상태의 live migration: 세 가지 탈출구

**공격 대상 문제**: passthrough 장치(NIC, RDMA, GPU)의 내부 상태는 OS가 볼 수
없기 때문에 live migration이 근본적으로 어렵다. 코퍼스는 이 문제에 대한 세 가지
서로 다른 탈출구를 명시적 relation으로 기록한다.

1. **직접 해결(장치의 협조를 받음)**: **VIRT-SOSP25-01 | Device-Assisted Live
   Migration of RDMA Devices (SOSP25, 2025)** — OS가 볼 수 없는 상태를 장치 자신의
   협조로 이동.
2. **더 쉬운 부분집합(host-visible paravirtual 상태)**: **VIRT-OSDI26-02 | M3U
   (OSDI26, 2026)** — VirtIO 상태는 host/software에 보이므로 virtqueue를 사전
   설치해 옮김. `CONTRASTS_WITH ↔ VIRT-SOSP25-01`("M3U pre-installs paravirtual
   (VirtIO) device state before migration ... this paper tackles the strictly harder
   case where the passthrough device's state is opaque to the hypervisor by
   construction, requiring the device's own cooperation").
3. **문제 자체를 회피**: **VIRT-SOSP25-05 | Oasis (SOSP25, 2025)** — 상태를 옮기는
   대신 I/O 상태 자체를 공유 CXL 메모리에 두고 물리 장치의 소유권만 재할당.
   `CONTRASTS_WITH ↔ VIRT-SOSP25-01`("Oasis sidesteps device-state migration
   entirely by keeping all I/O state in shared CXL memory and reassigning physical
   devices, whereas device-assisted live migration attacks the in-device state
   problem directly"). 대가는 4–7us 추가 지연, 전용 busy-polling 코어, PCIe 링크
   장애에 대한 무내성.
4. `VIRT-SOSP25-06 | PhoenixOS`도 `SAME_BRANCH → VIRT-SOSP25-01`로 이 계열에
   합류한다 — "both capture and move device state that the OS cannot see because
   the device bypasses it"(GPU 버전의 같은 문제).

**Lineage 강도**: 강함 — 세 논문이 서로 직접 비교하며 "같은 문제, 세 가지 답"을
스스로 프레이밍한다. 다만 세 답이 서로 대체하는 관계(alternative)이지 시간순
계승(precursor→extension) 관계는 아니라는 점에 유의.

---

## Lineage F — 프로세스 내부 하드웨어 격리 도메인: page-table 트램폴린 → MPK → CHERI capability

**공격 대상 문제**: 신뢰할 수 없는 코드를 별도 프로세스/VM 없이 하나의 주소
공간 안에서 격리하는 문제(in-process isolation)는 세 세대의 하드웨어 primitive를
거쳤다.

1. **Page-table 트램폴린 계열(선례)**: zpoline(ATC23), lazypoline —
   `PRECURSOR ← VIRT-MIDDLEWARE25-01 | K23/Clair Obscur (Middleware25, 2025)`.
   K23은 "reuses zpoline's callq *%rax rewrite and address-0 trampoline but adds
   offline address validation"이라고 명시하며, lazypoline의 우회(prctl)·원자성·
   I-cache 문제를 동기로 열거한다.
2. **MPK 도메인 계열 — 서로 다른 primitive로 같은 문제를 푸는 3파전**:
   - **VIRT-OSDI25-10 | bpftime (OSDI25, 2025)** — MPK 하드웨어 도메인으로 eBPF
     확장을 격리.
   - **VIRT-OSDI25-09 | DeCl (OSDI25, 2025)** — SFI/LFI(소프트웨어 결정론적 계측)로
     임의 네이티브 코드를 격리.
   - **VIRT-OSDI25-15 | Omniglot (OSDI25, 2025)** — MPK + 컴파일타임 스코프 검사로
     Rust에서 호출되는 외부 라이브러리를 격리.
   세 논문은 서로 `CONTRASTS_WITH`로 명시적으로 얽혀 있다: "different mechanisms
   for the same 'confine untrusted code sharing an address space' problem." bpftime은
   `SAME_BRANCH ← VIRT-OSDI25-15`(Omniglot, "both use hardware intra-process
   protection-domain switching (MPK) as a cheap alternative to process isolation").
3. **CHERI capability 계열 — 소비자로의 계층 관계**: **VIRT-SOSP25-11 | CHERIoT RTOS
   (SOSP25, 2025)** — capability 태그·bound으로 fine-grained compartment 제공.
   `LAYER_BELOW → VIRT-SOSP25-08 | Dandelion`("Dandelion's 89 us CHERI backend
   relies on exactly these capability bounds for sandbox isolation")와
   `LAYER_BELOW → VIRT-SOSP25-13 | μFork`("uFork uses CHERI capability tags to
   relocate pointers and to isolate micro-processes within one address space")
   두 소비자를 갖는다. Dandelion의 CHERI 백엔드 콜드스타트는 89us로, 자신이
   `TRADEOFF_PAIR`로 지목한 Firecracker snapshot restore(~120ms)보다 3자릿수
   빠르다 — "Firecracker keeps POSIX and pays snapshot restore cost; Dandelion drops
   POSIX and pays portability cost."

**Lineage 강도**: 중간~강함 — 세대 간(트램폴린→MPK→CHERI) 전환 자체는
`PRECURSOR`/`LAYER_BELOW`로 뒷받침되지만, MPK 세대 내부의 3파전은 계승이 아니라
**동시대의 서로 다른 primitive 선택**이므로 평행선(parallel alternative)으로
읽어야 한다.

---

## 요약: lineage 강도 순위

| Lineage | 편수(핵심) | 근거 강도 | 비고 |
|---|---|---|---|
| A. VM 메모리 탄력성 | 10 | 강함 | HyperAlloc이 corpus 1위 hub(연결도 11) |
| C. GPU 공유 진화 | 12+ | 강함·폭넓음 | 5단계 전부 명시적 관계, `[INFERENCE]` 1건뿐 |
| E. Passthrough 상태 migration | 4 | 강함 | 세 탈출구가 서로를 직접 지목 |
| D. Nested virtualization 비용 | 4 | 강함(짧음) | head-to-head trade-off pair |
| F. 프로세스 내 하드웨어 격리 | 7 | 중간 | 세대 전환은 강함, 세대 내부는 병렬 |
| B. I/O 가상화 확장성(SR-IOV) | 5 | 중간 | 2단계 직선 + 인접 가지 두 개 |

이 6개 lineage에 등장하는 논문은 약 40여 편이며, 나머지 "잘 연결된 60~80편" 범위는
`VIRTUALIZATION_TRADEOFFS.md`와 `CROSS_PAPER_RELATIONS.md`의 TRADEOFF_PAIR/
CONTRASTS_WITH 집합에서 추가로 다룬다.

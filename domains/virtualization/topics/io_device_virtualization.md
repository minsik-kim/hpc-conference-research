# I/O 및 디바이스 가상화 (I/O and Device Virtualization)

## 1. 이 계층이 푸는 문제

이 topic이 다루는 mapping은 Physical Resource(NIC, NVMe SSD, FPGA, PCIe/CXL fabric, RDMA RNIC)를 Logical Abstraction(virtual function, virtio device, virtual queue pair, vFPGA, pooled 논리 디바이스)으로 변환해서 Workload(multi-tenant cloud VM/container의 네트워크·스토리지 I/O, RDMA 기반 HPC/AI 통신, FPGA 가속)에 안전하고 성능 손실 없이 배분하는 것이다. CPU/메모리 가상화(T1/T2)와 달리 I/O 가상화는 항상 "물리 디바이스는 하나인데 tenant는 여럿"이라는 multiplexing 문제와, "guest가 디바이스에 DMA로 직접 접근하면 격리가 깨질 수 있다"는 isolation/mediation 문제를 동시에 진다.

corpus가 보여주는 mapping의 스펙트럼은 다음과 같다.

- **완전 소프트웨어 중개**: virtio/vSwitch가 물리 NIC 위에 논리 포트를 만들어 host CPU가 매 패킷을 처리한다 (VIRT-EUROSYS24-02 Hoda, VIRT-EUROSYS25-06 Byte vSwitch).
- **하드웨어 파티셔닝**: SR-IOV가 물리 NIC/NVMe를 고정된 개수의 Virtual Function으로 쪼개고, guest가 VF에 직접 접근한다 (VIRT-EUROSYS25-01 FastIOV, VIRT-ASPLOS25-01 Vela).
- **소프트웨어 정의 confined VF**: SR-IOV의 고정 VF 개수를 소프트웨어가 흉내내어 PASID/queue-pair 단위로 세분화한다 (VIRT-EUROSYS24-01 HD-IOV, VIRT-ASPLOS26-01 SG-IOV).
- **완전 passthrough**: guest가 물리 디바이스의 큐/DMA를 거의 그대로 가진다 (VIRT-HPCA25-01 NVMePass, VIRT-SOSP24-02 VPRI가 다루는 대상).
- **SmartNIC/DPU offload**: 물리 NIC 자체가 프로그래머블 프로세서를 갖고 있어, 그 프로세서 자원 자체를 가상화 대상으로 삼는다 (VIRT-ATC24-06 OSMOSIS, VIRT-EUROSYS24-04 S-NIC, VIRT-SOSP25-15 Tai Chi, VIRT-EUROSYS26-13 NADINO).

이 다섯 갈래는 "누가 매 I/O 오퍼레이션을 중개하는가"(host CPU software / IOMMU+SR-IOV 하드웨어 / DPU 코어)라는 하나의 축 위에 있고, 이 문서의 section 2·5가 그 축을 따라 구조를 정리한다.

## 2. Mechanism design space

### (a) 소프트웨어 중개 virtio/vSwitch

VIRT-EUROSYS25-06 Byte vSwitch는 ByteDance가 4년 이상 운영한 전용 vSwitch로, 범용 Open vSwitch 대비 최대 3.3배 높은 PPS와 25% 낮은 지연을 보고한다(공식 abstract 수치, ByteDance 프로덕션 환경). VIRT-EUROSYS24-02 Hoda는 OpenFlow 프로그램마다 전용 parser+microflow cache를 컴파일해, 범용 OVS 대비 처리량 1.7배(vanilla OVS 대비), 1.5배(mSwitch 대비)를 보인다. 이 갈래는 하드웨어 변경이 필요 없고 live migration도 자유롭지만, 매 패킷이 host CPU를 거치므로 높은 처리량에서는 CPU가 병목이 된다 — 이것이 이 문서의 "software mediation" 축의 최저비용/최저성능 극단이다.

### (b) SR-IOV VF passthrough

SR-IOV는 물리 NIC/NVMe를 하드웨어가 고정 개수의 VF로 쪼개고 IOMMU가 VF별 DMA를 격리한다. VIRT-ASPLOS25-01 Vela는 GPU passthrough와 RoCE NIC의 SR-IOV VF를 결합해 대규모 LLM 학습에서 GPUDirect RDMA를 guest 안에서 그대로 쓰게 하며, ASPLOS abstract 수치로 500B급 모델·약 1500 GPU 스케일에서 이상적 처리량의 약 80%, 단일-VM 대비 약 70%의 GPU당 FLOPS를 보고한다(관련 arXiv 프리프린트에서는 5% 이하의 가상화 오버헤드도 보고되나 이는 ASPLOS 논문 자체와 저자가 겹치는 별도 문헌임을 밝혀둔다). VIRT-EUROSYS25-01 FastIOV는 secure container(microVM)에서 SR-IOV passthrough를 쓸 때 attach 경로 자체가 비싸다는 것(VF lock 분해, DMA mapping 제거, 메모리 zeroing 분리, guest driver 비동기 초기화)을 공식 abstract 기준 SR-IOV 활성화 오버헤드 96.1% 감소, 종단 시작 시간 평균 65.7%·p99 75.4% 감소로 개선한다. SR-IOV는 isolation이 강하고 데이터 경로가 거의 native지만, VF 개수가 물리적으로 제한되고(수백 개 수준) 시작 비용이 크다.

### (c) Scalable IOV / PASID 기반 소프트웨어 정의 VF

VIRT-EUROSYS24-01 HD-IOV는 SR-IOV의 고정 VF 개수를 깨기 위해 가상화·자원관리 로직을 소프트웨어로 내려, PCIe PASID로 IOMMU가 VF가 아니라 queue-pair 단위로 격리를 강제하게 한다. Intel E810 NIC + on-chip QAT 2.0 가속기에서 SR-IOV 대비 최대 2.96배 많은 virtual device를 지원하고, 초기화 시간은 2.9배 빠른 median을 보였다(HD-IOV artifact 평가, Intel Sapphire Rapids Xeon 기준). VIRT-ASPLOS26-01 SG-IOV는 이 흐름을 극단까지 밀어붙여, 가상화 단위를 PCIe function에서 TCP socket으로 내린다 — Warp Pipe(소켓별 ring buffer)와 Cross-FIFO(포인터 갱신 메시지)로 NVIDIA BlueField-3의 온보드 ARM 코어와 host를 잇고, "SR-IOV는 물리 NIC당 수백 개 VF에서 한계"라는 문제를 3자릿수 개선으로 공략한다(구체 수치는 논문 Section 8 Figure 17-18에 있으나 2차 요약에서는 추출되지 않았다). 이 갈래의 공통점은 하드웨어 VF 개수라는 SR-IOV의 근본 한계를 소프트웨어 인덱싱으로 우회한다는 것이다.

### (d) 완전 passthrough와 그 대가

완전 passthrough(디바이스를 guest에 거의 그대로 노출)는 소프트웨어 중개 비용을 없애지만, 이 corpus의 SOSP 2024 3편이 정확히 그 대가를 계량화한다. VIRT-SOSP24-02 VPRI는 passthrough가 "모든 guest 메모리를 정적으로 pin"해야 한다는 사실이 프로덕션에서 DRAM의 최대 50%를 낭비시킨다는 것을 보이고(Alibaba Cloud 45%의 페이지가 2분 내 cold, 서버의 30%가 매일 50% 이상 cold), PA-BITMAP(4KB당 2비트)과 사이드밴드 page-fault queue로 IOMMU ATS+PRI 없이 NIC IOPF를 99% 이상 줄인다(5000대 프로덕션 VM, 10-15% overcommit). VIRT-SOSP24-03 F&S(Fast & Safe IO Memory Protection)는 strict IOMMU 보호(매 DMA 후 IOVA unmap+IOTLB invalidate)가 20-65%의 처리량 저하를 낳는 이유가 IO 페이지테이블 캐시 미스에 있음을 밝히고, 연속된 256KB IOVA 할당과 선택적 캐시 무효화만으로 IOMMU-off에 근접한 성능을 회복시킨다(Nginx 65-70% 저하, Redis 38-70% 저하가 사실상 해소). VIRT-HPCA25-01 NVMePass는 NVMe 자체를 control-plane(trap-and-emulate)과 data-plane(큐 passthrough)으로 나눠, SR-IOV/SIOV 하드웨어 없이도 단일-VM IOPS가 VFIO passthrough의 97.6-100.2%에 도달하면서(4KB random RW, fio, Intel P4510) 200-VM 밀도에서는 SPDK vhost-NVMe보다 IOPS 45.7% 높고, virtio-blk보다 75.6% 높다.

### (e) SmartNIC/DPU offload — 가상화 대상이 되는 프로그래머블 NIC

이 갈래는 NIC 자체가 하나의 작은 가상화 호스트가 되는 경우다. VIRT-ATC24-06 OSMOSIS는 오픈소스 RISC-V PsPIN 400Gbit/s SmartNIC 위에서 per-flow Flow Management Queue와 Weight-Limited Borrowed Virtual Time(WLBVT) 스케줄러로 SmartNIC 처리 유닛·DMA·egress 대역폭을 공정하게 나누며, IO-set 워크로드에서 최대 83% fairness 개선, 최대 63% flow-completion-time 감소를 보고한다(단일-tenant IO-bound 오버헤드는 2-23%). VIRT-EUROSYS24-04 S-NIC는 반대로 동적 공유를 아예 피하고 locked TLB entry와 메모리 denylist로 함수별 자원을 하드웨어에서 정적으로 분할해, side-channel 없는 격리를 얻는 대신 칩 면적 +8.89%, 전력 +11.45%, 16-function 밀집 시 median IPC 저하 9.44%를 치른다. VIRT-SOSP25-15 Tai Chi는 SmartNIC OS 안에 물리 CPU(데이터 플레인 폴링)와 vCPU(idle 사이클의 컨트롤 플레인)를 통합해, type-1/type-2 가상화가 각각 7%/25.9% 데이터플레인 저하를 내는 것과 달리 0.7% 평균 저하만으로 컨트롤 플레인 처리량 4배·VM 시작 3.1배 개선을 얻는다(Alibaba Cloud 프로덕션 SmartNIC). VIRT-EUROSYS26-13 NADINO는 DPU 상주 off-path DPU Network Engine이 tenant 대신 RDMA queue pair를 조작하게 해 serverless 함수가 직접 RDMA QP를 갖지 못하게 하면서도, host 코어 7개를 절약하고 DPU 코어 2개만 소비해 20.9배 RPS·21배 지연 개선(Online Boutique, 단일노드 NightCore 대비)을 얻는다.

### (f) CXL/PCIe fabric를 통한 디바이스 풀링

VIRT-SOSP25-05 Oasis는 PCIe 스위치($80,000/rack) 없이 non-coherent CXL 2.0 메모리에 I/O 버퍼와 시그널링을 두고, 한 호스트가 소유한 물리 디바이스를 다른 호스트의 frontend driver가 원격으로 쓰게 한다. 두 호스트가 NIC 하나를 공유하면 P99.99 활용도가 18%에서 37%로 개선되지만 4-7us의 추가 지연이 붙고, driver/device를 완전히 신뢰해야 하며 IOMMU를 쓰지 않는다는 점에서 SR-IOV/passthrough보다 약한 격리 모델을 취한다.

## 3. 핵심 논문 (P0/P1)

**VIRT-SOSP24-01 | vSoC (SOSP 2024, CORE P0, FULL/HIGH).** 모바일 SoC는 unified-memory 아키텍처인데 PC/서버 가상화는 modular(디바이스별 독립 메모리) 가정을 깔고 있어, 모바일 에뮬레이터가 guest-host 데이터 복사와 coherence 유지에 발목 잡힌다는 문제를 다룬다. SVM Manager가 64-bit ID로 공유 메모리 영역을 참조시키고, adaptive prefetch engine이 OS-level slack interval(평균 17ms)을 이용해 미리 데이터를 당겨온다. Google Android Emulator 대비 약 57 FPS(경쟁작 31/19/9/7 FPS) 등 큰 개선을 보이지만, 악의적 guest에 대한 격리는 명시적으로 다루지 않는다 — passthrough/virtio 계열의 "모듈형" 가정과 대비되는 사례.

**VIRT-SOSP24-02 | VPRI (SOSP 2024, CORE P0, FULL/HIGH).** passthrough가 강제하는 정적 메모리 pinning이 프로덕션 DRAM을 얼마나 낭비하는지(최대 50%), 그리고 IOMMU ATS+PRI라는 표준 해법이 프로덕션 CPU의 90% 이상에서 지원되지 않는다는 현실을 보인다. PA-BITMAP + 사이드밴드 page-fault queue + device-type-aware dual-LRU(ADP)로 NIC IOPF를 평균 99% 이상 줄이고 DRAM 비용을 최대 15% 절감한다. Trade-off: block device에서는 개선폭이 훨씬 작다(IOPF 감소 36-49% vs NIC 95-97%)고 스스로 밝힌다.

**VIRT-SOSP24-03 | Fast & Safe IO Memory Protection (SOSP 2024, CORE P0, FULL/HIGH).** strict IOMMU 보호의 20-65% 처리량 손실이 IOTLB miss(다단계 페이지테이블 워크)에서 온다는 것을 밝히고, 하드웨어 변경 없이 630 LOC의 OS 변경만으로 연속 256KB IOVA 할당 + 선택적 캐시 무효화로 IOMMU-off에 근접한 성능을 회복한다. VPRI가 "페이지를 아예 안 핀하는" 접근이라면 F&S는 "핀은 하되 보호 비용을 낮추는" 상보적 접근이며, 두 논문은 TRADEOFF_PAIR로 명시적으로 연결된다.

**VIRT-OSDI25-01 | To PRI or Not To PRI (VIO) (OSDI 2025, CORE P0, DESIGN_EVAL/HIGH).** VPRI가 지적한 PRI 하드웨어 미지원 문제(300K VM 프로덕션 기준 80%에서 PRI 불가)를 hypervisor 전용 소프트웨어로 우회한다. IOPA-Snoop이 VirtIO ring command를 미리 검사해 DMA 전에 매핑을 보장하고, Adaptive Lockpage가 2MB 단위로 자주 쓰는 페이지만 pin하며, Elastic Passthrough가 IOPS 임계값(약 100k IOPS)에 따라 snooping 모드와 완전 passthrough 모드를 오간다. 300K VM/300노드 프로덕션에서 하루 약 120GB 메모리를 회수하고 IOPF를 CPU page fault의 1% 미만으로 낮춘다.

**VIRT-ATC24-06 | OSMOSIS (ATC 2024, CORE P1, DESIGN_EVAL/HIGH).** SR-IOV VF를 노출하면서도 성능 격리가 없던 on-path SmartNIC 문제를 하드웨어 Flow Management Queue + WLBVT/WRR 스케줄러로 해결한다. cycle-accurate Verilator 시뮬레이션 기준 IO-set 워크로드에서 fairness 최대 83% 개선, FCT 최대 63% 감소를 보이는 대신 WLBVT 스케줄러는 round robin보다 약 7배 많은 게이트를 쓴다.

**VIRT-ATC24-24 | vFPIO (ATC 2024, CORE P1, FULL/HIGH).** FPGA 가속 I/O 디바이스(SmartNIC, computational storage)가 PCIe/host-DRAM/FPGA HBM/네트워크를 저마다 다른 인터페이스로 노출해 이식성이 떨어지는 문제를, device-agnostic virtual I/O port와 preemptive DMA-transaction 스케줄러로 푼다. Coyote 대비 I/O 재구성 시간이 1.3us(Coyote는 22.7ms) — 약 17,500배 빠르며, 우선순위 격리로 high-priority instance가 1.8배 빠르다.

**VIRT-EUROSYS24-01 | HD-IOV (EuroSys 2024, CORE P1, DESIGN_EVAL/HIGH).** SR-IOV의 고정 VF 개수 한계를 소프트웨어 이관 + PASID 기반 큐페어 격리로 우회한다. 같은 하드웨어에서 SR-IOV 대비 최대 2.96배 많은 virtual device, 2.9배 빠른 초기화를 보이지만 state_mechanism(마이그레이션 처리)은 UNKNOWN으로 남아 있다.

**VIRT-EUROSYS24-02 | Hoda (EuroSys 2024, CORE P1, ABSTRACT/HIGH).** OVS의 "하나의 범용 파이프라인"이 프로그램마다 다른 헤더 필드 요구를 낭비한다는 관찰에서, OpenFlow 프로그램별 전용 parser+microflow cache를 컴파일한다. vanilla OVS 대비 처리량 1.7배, mSwitch 대비 1.5배, 실배포 Nginx 서비스에서 요청처리시간 20% 감소. 단, evidence depth가 ABSTRACT이므로 메커니즘 세부는 깊이 검증되지 않았다.

**VIRT-EUROSYS24-04 | S-NIC (EuroSys 2024, CORE P1, FULL/HIGH).** 상용 SmartNIC이 상호 불신하는 tenant 네트워크 함수와 운영자 관리 OS 사이에 하드웨어 상태·메모리·버스 대역폭을 공유해 패킷 변조·룰셋 탈취·DoS를 유발할 수 있음을 실증하고, locked TLB+memory denylist+시간분할 버스로 완전 정적 파티셔닝을 한다. Diffie-Hellman 기반 원격 attestation까지 포함. T7(기밀 컴퓨팅)과의 다리 역할도 한다.

**VIRT-ASPLOS25-01 | Vela (ASPLOS 2025, CORE P1, ABSTRACT/MEDIUM).** LLM 학습을 위해 GPU passthrough + RoCE NIC SR-IOV VF를 결합하고, VM 정의가 물리 PCIe/NUMA 토폴로지를 그대로 반영하게 해 guest 안에서 GPUDirect RDMA가 동작하게 한다. Trade-off: VM 수준의 유연성(재프로비저닝, 멀티테넌시)을 얻지만 GPU가 passthrough이고 NIC가 VF이므로 live migration과 메모리 overcommit을 구조적으로 포기한다.

**VIRT-EUROSYS25-01 | FastIOV (EuroSys 2025, CORE P1, ABSTRACT/MEDIUM).** secure container(Kata)에서 SR-IOV passthrough의 시작 비용이 서버리스급 워크로드를 막는다는 문제를, VF lock 분해·불필요한 DMA mapping 제거·메모리 zeroing 분리·비동기 guest driver 초기화로 해결한다. 공식 abstract 기준 SR-IOV 활성화 오버헤드 96.1% 감소.

**VIRT-HPCA25-01 | NVMePass (HPCA 2025, CORE P1, DESIGN_EVAL/MEDIUM).** NVMe를 control-plane(trap-emulate)과 data-plane(큐 passthrough)으로 분리해 SR-IOV/SIOV 하드웨어 없이도 VFIO에 근접한 성능과 스펙상 65,535개 큐페어까지의 확장성을 얻는다. 200-VM 밀도에서 SPDK vhost-NVMe보다 지연 31.4% 낮고 IOPS 45.7% 높다.

**VIRT-ASPLOS26-01 | SG-IOV (ASPLOS 2026, CORE P1, DESIGN/MEDIUM).** SR-IOV의 "물리 NIC당 수백 VF" 한계를 socket 단위로 내려, BlueField-3의 온보드 ARM 코어와 host 사이를 Warp Pipe(ring buffer)+Cross-FIFO(포인터 델타)로 잇는다. TCP 기반 stream 소켓을 가정하며, 정량적 벤치마크는 논문 본문에만 있어 이 corpus에서는 검증되지 않았다.

**VIRT-EUROSYS26-13 | NADINO (EuroSys 2026, CORE P1, DESIGN_EVAL/HIGH).** 서버리스 tenant가 RDMA 큐페어를 직접 가질 수 없다는 격리 요구를, DPU 상주 off-path Network Engine이 대신 조작하는 방식으로 푼다. on-path DPU 처리의 최대 1.54배 데이터 이동 오버헤드, 중복 프로토콜 처리로 인한 최대 11.4배 저하를 각각 cross-processor 공유 메모리와 ingress 게이트웨이 통합으로 없애, host 코어 7개를 절약하면서 20.9배 RPS 개선을 얻는다.

**VIRT-ASPLOS25-10 | FleetIO (ASPLOS 2025, SUPPORT P1, DESIGN_EVAL/HIGH).** 하드웨어 격리(전용 flash 채널, 강한 격리·낮은 활용도)와 소프트웨어 격리(공유 채널+token-bucket, 높은 활용도·2배 나쁜 tail latency) 사이의 이분법을, RL 에이전트가 ghost-superblock을 통해 vSSD 간 대역폭을 빌리고 빌려주게 하는 방식으로 완화한다. 하드웨어 격리 대비 저장 활용도 1.30-1.39배, 소프트웨어 격리 대비 P99 tail latency 1.47배 개선.

**VIRT-SOSP25-05 | Oasis (SOSP 2025, SUPPORT P1, DESIGN_EVAL/HIGH).** PCIe 디바이스가 Azure capex의 20-40%, 전력의 13%를 차지하면서도 호스트당 정적으로 프로비저닝돼 유휴화된다는 문제를, CXL 2.0 non-coherent 메모리 위의 frontend/backend driver 분리로 두 호스트가 NIC 하나를 나눠 쓰게 한다. driver/device를 완전히 신뢰해야 하고 IOMMU가 없다는 점이 SR-IOV 계열과의 핵심 차이.

**VIRT-EUROSYS25-03 | HyperAlloc (EuroSys 2025, CORE P1, FULL/HIGH, 주 taxonomy T2).** device passthrough(IOMMU pinning)가 정확히 무엇을 부수는지—고전적 ballooning의 전제인 "언제든 페이지를 회수할 수 있다"는 가정—를 보여주는 논문으로, guest allocator(LLFree)를 hypervisor와 공유해 2MiB 단위로 DMA-safe하게 페이지를 회수·재설치한다. VFIO passthrough NIC 환경에서 회수 처리량 54.6 GiB/s(virtio-mem+VFIO는 17.7 GiB/s)로, passthrough와 memory overcommit의 정면충돌을 소프트웨어로 완화하는 대표 사례.

**VIRT-SOSP25-15 | Tai Chi (SOSP 2025, CORE P1, DESIGN_EVAL/HIGH, 주 taxonomy T1).** SmartNIC의 데이터플레인 CPU가 67.5% 유휴 사이클을 갖고도 컨트롤플레인과 naive하게 공존시키면 I/O SLO가 깨진다는 문제를, type-1/type-2 하이퍼바이저를 쓰지 않고 vCPU를 SmartNIC OS에 네이티브 통합하는 "하이브리드 가상화"로 해결한다. type-1은 7%, type-2(QEMU+KVM)는 25.9% 데이터플레인 저하를 내는 반면 Tai Chi는 0.7%.

## 4. Supporting 논문 (P2/P3)

- **VIRT-ATC24-04 PeRF (P2, DESIGN_EVAL/HIGH)**: RDMA 큐페어를 software-only preemption(16KB sub-message 단위)으로 격리해, SR-IOV/vSwitch 계열과는 다른 "완전 소프트웨어 QoS" 지점을 보여준다. Justitia 대비 message-rate 약 2.04배 개선. OSMOSIS와 SAME_BRANCH.
- **VIRT-HPCA24-09 LightPool (P3, ABSTRACT_INTRO/MEDIUM)**: 로컬 NVMe를 NVMe-oF로 풀링해 Kubernetes가 스케줄하게 하는 스토리지 디스어그리게이션 사례. 새로운 격리 경계는 만들지 않아 T3의 "가상 자원 추상화" 임계값에 딱 걸치는 경계 사례로 읽으면 좋다.
- **VIRT-OSDI24-05 BurstCBS (P2, FULL/HIGH)**: DPU storage agent에서 burstable 블록스토리지가 기본 SLO를 깨는 문제를 FPGA 기반 큐 스케일링 + BIOS 스케줄러로 해결. base-level tenant 지연을 WildCBS 대비 68-85%(BPS-집중 배경) 줄인다.
- **VIRT-EUROSYS25-06 Byte vSwitch (P2, ABSTRACT/MEDIUM)**: ByteDance의 프로덕션 vSwitch 재작성. OVS 대비 최대 3.3배 PPS.
- **VIRT-EUROSYS25-09 Skewness (P2, DESIGN_EVAL/HIGH)**: 60,000 VM/140,000 virtual disk 규모의 프로덕션 트레이싱으로 가상 디스크 경로(큐페어→워커스레드→세그먼트→스토리지노드)의 skew를 정량화. throttle이 자원의 61.6-74.7%가 남아있을 때도 발동한다는 것이 핵심 관찰.
- **VIRT-HPCA25-06 RpcNIC (P2, DESIGN_EVAL/HIGH)**: PCIe-attached SmartNIC에서 RPC (de)serialization을 오프로드. ProtoACC-PCIe 대비 처리시간 2.3배 개선.
- **VIRT-MICRO25-02 CXL-NIC (P2, DESIGN_EVAL/HIGH)**: NIC descriptor ring/메모리를 DMA 대신 CXL.cache/CXL.mem 코히런트 트랜잭션으로 대체. 미래 CXL 기반 vNIC/SR-IOV-over-CXL 설계의 배경.
- **VIRT-MIDDLEWARE25-03 Tiaccoon (P2, ABSTRACT/MEDIUM)**: 컨테이너 네트워크 오버레이가 느리다는 문제를 socket API 인터셉션으로 우회. "정책 평면은 유지하고 가상화된 데이터 경로는 우회한다"는 이 계층의 표준 탈출구를 잘 보여준다.
- **VIRT-SOCC25-20 XpuPod (P2, ABSTRACT_INTRO/MEDIUM)**: 인프라 서비스(서비스 메시 등)를 물리적으로 분리된 DPU로 옮겨 host CPU 경합을 없애는 네임스페이스 분할 접근.
- **VIRT-ASPLOS26-17 CEMU (P2, ABSTRACT_INTRO/MEDIUM)**: QEMU 기반으로 실제 하드웨어보다 더 넓은 범위의 computational storage를 에뮬레이트해 CSD 연구를 가능하게 한다.
- **VIRT-EUROSYS26-19 RoPeerTo (P2, ABSTRACT/MEDIUM)**: GPU-FPGA 간 peer-to-peer DMA를 표준화하는 API. host 우회 시 5.61배 속도, GPU 전력 37.99% 절감(qualifier 불명확).
- **VIRT-EUROSYS26-22 RDMA connection sharing (P3, ABSTRACT_INTRO/MEDIUM)**: HPC에서 프로세스당 RDMA 연결을 공유해 상태 성장을 억제하는 정책 연구. 격리 방식은 UNKNOWN.

인접 T6(가속기 가상화)의 FPGA shell 계열—**VIRT-ASPLOS25-13 Harmonia**(벤더 독립 FPGA shell, shell 코드 재사용 69-93%), **VIRT-SOSP25-10 Coyote v2**(vFPGA당 하드웨어 MMU, HBM까지 400+ GB/s), **VIRT-EUROSYS26-02 Proteus**(ABSTRACT/MEDIUM, 벤더/용량 독립 논리 FPGA)—는 T3의 vFPIO와 함께 "FPGA를 어떻게 device-virtualize하는가"라는 하나의 하위 계보를 이룬다(참고: capability 기반 vFPGA 조합을 다루는 VIRT-OSDI26-07 μShell은 이 corpus에서 T6+T5로 분류되어 T3 입력 파일에는 없으므로 여기서는 제외한다).

## 5. Trade-off 구조

이 계층의 구조적 대립은 다음과 같이 정리된다.

**(1) Software mediation ↔ Isolation/Memory management/Live migration (고전적 passthrough trade-off).** Passthrough는 소프트웨어 중개 비용을 없애지만 그 대가로 세 가지를 동시에 어렵게 만든다.
- *Isolation*: IOMMU strict mode는 안전하지만 20-65% 처리량을 깎는다(VIRT-SOSP24-03 F&S가 정확히 이 비용을 측정). 반대로 격리를 완화하면(overcommit 기능들) VIRT-ASPLOS25-02 HyperHammer가 보여주듯 THP+virtio-mem+vIOMMU 조합이 guest에서 host 물리 메모리 배치를 추론 가능하게 만들어 Rowhammer 공격의 발판이 된다.
- *Memory management*: passthrough는 모든 guest 메모리를 정적으로 pin해야 하고(VIRT-SOSP24-02 VPRI), 이는 DRAM의 최대 50%를 낭비시킨다. VIRT-OSDI25-01(VIO/To-PRI)와 VIRT-EUROSYS25-03(HyperAlloc)은 각각 hypervisor-side snooping과 guest-hypervisor 공유 allocator로 이 문제를 소프트웨어에서 되돌리려는 두 가지 다른 시도다.
- *Live migration*: passthrough된 디바이스의 하드웨어 상태(큐페어, 메모리 등록)는 하이퍼바이저가 볼 수 없다. VIRT-SOSP25-01(Device-Assisted Live Migration of RDMA Devices)이 정확히 이 문제를 제목으로 걸지만, 이 corpus에서는 ABSTRACT 수준 근거만 확보되어 메커니즘이 검증되지 않았다(§9 참조). VIRT-OSDI26-02 M3U는 passthrough 디바이스의 IOPF가 post-copy live migration의 다운타임을 어떻게 늘리는지, 그리고 VirtIO virtqueue 상태를 재개 전에 미리 전송해 이를 줄이는 구체적 해법(다운타임 최대 47.0% 감소)을 보여준다.

**(2) 하드웨어 파티션 개수 ↔ tenant 밀도.** SR-IOV의 VF 개수는 물리적으로 고정돼 "수백 개"에서 막힌다는 것이 VIRT-EUROSYS24-01(HD-IOV)과 VIRT-ASPLOS26-01(SG-IOV)의 공통 출발점이다. 이를 풀기 위해 파티셔닝 granularity를 낮추면(VF → queue-pair → socket) 밀도는 오르지만, 하드웨어 상태를 stateless하게 유지해야 하므로 설계 복잡도와 호스트-디바이스 간 메시지 왕복이 늘어난다.

**(3) 정적 하드웨어 파티셔닝 ↔ 동적 공유 (SmartNIC 갈래의 재현).** VIRT-EUROSYS24-04(S-NIC)의 정적 파티셔닝은 side-channel-free 격리를 주지만 면적/전력/처리량을 희생하고, VIRT-ATC24-06(OSMOSIS)의 동적 공정 스케줄링은 활용도를 높이지만 side-channel 여지를 완전히 지우지는 못한다. VIRT-HPCA26-05(DSAssassin)는 이 우려가 실제임을 증명한다 — Intel Scalable IOV(SIOV)의 공유 DevTLB와 Shared Work Queue를 통해 cross-VM covert channel(17.19 Kbps, 오류율 4.64%)과 키스트로크 추론(F1 최대 98.4%)이 가능함을 보인다. "디바이스 단위 중개(SIOV/PASID)가 격리를 보장한다"는 가정 자체가 마이크로아키텍처 수준에서는 깨질 수 있다는 반례다.

## 6. 인접 계층과의 관계

- **T1(CPU/기계 가상화) 아래로**: VIRT-ATC25-02 HyperTurtle은 nested virtualization(L0/L1/L2)에서 EPT fault·네트워크 정책·프로파일링을 eBPF "hyperupcall"로 L0에서 직접 처리해 EPT fault 지연을 5.26배 줄이며, virtio 네트워킹 오버헤드를 다룬다. VIRT-SOSP24-01(vSoC)와 VIRT-SOSP25-15(Tai Chi)는 각각 모바일 SoC와 SmartNIC이라는 "표준 서버 가상화가 아닌" CPU 가상화 변주다.
- **T2(메모리 가상화)와의 다리**: VIRT-SOSP24-02(VPRI), VIRT-OSDI25-01(VIO), VIRT-EUROSYS25-03(HyperAlloc), VIRT-OSDI25-08(FineMem)이 모두 "passthrough 디바이스가 메모리 overcommit을 얼마나 어렵게 만드는가"라는 동일한 문제를 서로 다른 각도(페이지폴트 회피, hypervisor snooping, 공유 allocator, RDMA 메모리 풀)에서 공략한다.
- **T4(마이그레이션)와의 다리**: VIRT-OSDI26-02(M3U)와 VIRT-SOSP25-01(RDMA live migration, 근거 약함)이 passthrough 디바이스의 live migration 문제를 정면으로 다룬다.
- **T5(컨테이너 격리) 위로**: VIRT-EUROSYS25-01(FastIOV)와 VIRT-ASPLOS26-01(SG-IOV)는 secure container(microVM)가 SR-IOV/소켓 단위 가상화를 쓸 때의 시작 비용을 다룬다. VIRT-ATC25-06 Poby(주 taxonomy T5)는 컨테이너 콜드스타트 이미지 추출을 SmartNIC DRAM으로 파이프라인하는 사례로, T3의 SmartNIC offload 기법이 T5 콜드스타트 문제에 적용된 예다.
- **T6(가속기 가상화)와의 다리**: VIRT-ATC24-24(vFPIO), VIRT-ASPLOS25-13(Harmonia), VIRT-SOSP25-10(Coyote v2), VIRT-EUROSYS26-02(Proteus)가 FPGA를 "I/O 디바이스"이자 "가속기"로 동시에 다루며 두 taxonomy를 잇는다.
- **T7(기밀 컴퓨팅) 위로**: VIRT-EUROSYS24-04(S-NIC)의 attestation, VIRT-MICRO25-01 ccAI(PCIe Security Controller로 신뢰 경계를 PCIe 트랜짓까지 확장), VIRT-EUROSYS25-18 RAKIS(enclave 안에서 XDP/io_uring을 직접 구동), VIRT-HPCA26-05(DSAssassin)가 "I/O 가상화의 신뢰 경계가 CPU를 넘어 PCIe/가속기로 확장될 때 무엇이 깨지는가"를 보여준다.
- **T9(자원관리/멀티테넌시)와의 다리**: 이 문서에 나온 SmartNIC/스토리지 논문 다수(PeRF, OSMOSIS, FleetIO, BurstCBS, Skewness)가 T3+T9 이중 분류로, I/O 가상화 메커니즘 위에서 실제로 QoS/공정성을 어떻게 구현하는지를 보여준다.

## 7. 2024 → 2026 변화

**2024년**: SOSP 2024의 3편(vSoC, VPRI, F&S)이 passthrough의 근본 대가(메모리 pin, IOMMU 보호 비용)를 정밀하게 계량화했고, EuroSys 2024의 HD-IOV·S-NIC이 각각 "SR-IOV VF 개수 한계를 소프트웨어로 우회"와 "SmartNIC을 하드웨어로 완전히 정적 파티셔닝"이라는 대조적인 해법을 냈다. ATC 2024의 OSMOSIS는 SmartNIC 멀티테넌시에 처음으로 하드웨어 검증된 공정 스케줄러를 제시했다.

**2025년**: OSDI 2025의 VIO(To PRI or Not To PRI)가 VPRI의 문제(overcommit-passthrough 충돌)를 PRI 하드웨어 없이 순수 hypervisor 소프트웨어로 풀었고, EuroSys 2025의 HyperAlloc이 대칭적으로 guest-hypervisor 공유 allocator 접근을 냈다 — 같은 문제에 대한 소프트웨어 해법이 한 해 사이에 두 갈래로 성숙했다. SOSP 2025의 Oasis는 디바이스 가상화의 경계를 단일 호스트 밖(CXL을 통한 풀링)으로 넓혔고, Tai Chi는 SmartNIC을 "가상화 대상"에서 "가상화 호스트"로 재정의했다.

**2026년(초기 문헌)**: ASPLOS26의 SG-IOV와 EuroSys26의 NADINO가 가상화 granularity를 PCIe function 이하(소켓, DPU 중개 RDMA)로 더 내렸고, HPCA26의 DSAssassin은 "SIOV/PASID 기반 소프트웨어 정의 격리가 마이크로아키텍처 수준에서 여전히 샐 수 있다"는 반대 방향의 증거를 냈다. 즉 가상화 granularity는 계속 미세화되는 추세가 뚜렷하지만(HD-IOV→SG-IOV, SR-IOV→SIOV), 동시에 그 미세화가 새로운 공유 하드웨어 구조(DevTLB, SWQ)를 통한 격리 회귀 위험을 동반한다는 균형추가 2026년 문헌에서 처음 명시적으로 등장했다. 다만 2026년 표본은 이 문서 기준 약 6-7편(대부분 abstract 단계)에 불과해, 이를 확고한 "3년 추세"로 일반화하기보다는 "관찰된 방향성"으로 제한해 읽어야 한다.

## 8. 읽는 순서 제안

1. **VIRT-SOSP24-02 (VPRI)** — passthrough가 메모리 overcommit과 왜 충돌하는지부터 이해한다.
2. **VIRT-SOSP24-03 (F&S)** — 같은 passthrough 문제의 IOMMU 보호 비용 쪽 짝.
3. **VIRT-OSDI25-01 (VIO)** — 1·2가 제기한 문제의 2025년 순수 소프트웨어 해법.
4. **VIRT-EUROSYS25-03 (HyperAlloc)** — 대칭적인 guest-hypervisor 공유 allocator 접근.
5. **VIRT-EUROSYS24-01 (HD-IOV)** → **VIRT-ASPLOS26-01 (SG-IOV)** — SR-IOV VF 한계를 넘어서는 소프트웨어 정의 granularity의 진화.
6. **VIRT-ATC24-06 (OSMOSIS)** → **VIRT-EUROSYS24-04 (S-NIC)** — SmartNIC 멀티테넌시의 동적/정적 두 극단.
7. **VIRT-SOSP25-15 (Tai Chi)** → **VIRT-EUROSYS26-13 (NADINO)** — SmartNIC/DPU가 가상화 호스트로 진화하는 과정.
8. **VIRT-EUROSYS25-01 (FastIOV)** — 보안 컨테이너에서 passthrough의 시작 비용.
9. **VIRT-SOSP25-05 (Oasis)** — 단일 호스트를 넘어선 디바이스 풀링.
10. **VIRT-ATC24-24 (vFPIO)** — 같은 문제의식을 FPGA로 확장.
11. **VIRT-HPCA26-05 (DSAssassin)** — 소프트웨어 정의 격리가 실패할 수 있다는 반례로 마무리.

## 9. 증거 한계

다음 문헌은 이 corpus에서 abstract 또는 abstract-intro 수준 근거에 머물러 있어, 메커니즘 세부나 수치를 깊이 검증된 것으로 취급하면 안 된다: VIRT-EUROSYS24-02(Hoda), VIRT-ASPLOS25-01(Vela), VIRT-EUROSYS25-01(FastIOV), VIRT-EUROSYS25-06(Byte vSwitch), VIRT-MIDDLEWARE25-03(Tiaccoon), VIRT-SOCC25-20(XpuPod), VIRT-ASPLOS26-17(CEMU), VIRT-EUROSYS26-19(RoPeerTo), VIRT-EUROSYS26-22(RDMA connection sharing), VIRT-HPCA24-09(LightPool), VIRT-EUROSYS26-02(Proteus). 특히 **VIRT-SOSP25-01(Device-Assisted Live Migration of RDMA Devices)**은 문제 제기 자체는 이 계층에서 가장 중요한 미해결 질문 중 하나이지만, isolation_mechanism·multiplexing_mechanism·state_mechanism·overhead_bottleneck·primary_tradeoff가 모두 UNKNOWN으로 남아 있어 제목 이상의 근거가 없다는 점을 강조해 둔다. VIRT-HPCA26-05(DSAssassin)는 confidence는 HIGH이지만 evidence depth 자체는 ABSTRACT이므로, 공격 메커니즘의 개념(DevTLB/SWQ 공유)은 신뢰할 수 있되 세부 구현 디테일은 원 논문 확인이 필요하다. VIRT-ASPLOS26-01(SG-IOV)의 정량적 벤치마크는 원 논문 Section 8에만 있고 이 corpus의 2차 요약에는 추출되지 않았다는 점도 함께 밝혀둔다.

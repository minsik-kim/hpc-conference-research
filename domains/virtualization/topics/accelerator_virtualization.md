# Accelerator Virtualization (T6)

## 1. 이 계층이 푸는 문제

이 topic은 GPU, FPGA, NPU, PIM, QPU 같은 "CPU가 아닌 계산 자원"을 어떻게 여러 워크로드/테넌트에게 안전하고 효율적으로 나눠줄 것인가를 다룬다. Physical Resource → Logical Abstraction → Workload 관점에서 보면:

- **Physical Resource**: 물리적으로 하나뿐인 GPU SM/메모리 컨트롤러, FPGA fabric, NPU의 matrix/vector engine, PIM rank, QPU의 qubit lattice.
- **Logical Abstraction**: vGPU 인스턴스(MIG slice, MPS context, temporal quota), vFPGA(reconfigurable region), vNPU(엔진 비율이 다른 가상 NPU), vPIM(가상 rank), qVM(가상 QPU 영역).
- **Workload**: DNN 학습/추론, 서버리스 함수, 클라우드 게이밍 렌더링, 양자 회로 등.

CPU/메모리 가상화와 달리 가속기에는 하드웨어 지원 preemption, dirty bit, MMU 기반 page fault 같은 전통적 OS 가상화 primitive가 대부분 없다(VIRT-SOSP25-14 LithOS, VIRT-SOSP25-06 PhoenixOS가 명시적으로 지적). 따라서 이 계층의 핵심 문제는 "OS/hypervisor가 CPU에서 공짜로 얻는 가상화 기반(preemption, 주소 변환, state 캡처)을 가속기에서는 처음부터 다시 만들어야 한다"는 것이다. 그 결과 이 corpus는 소프트웨어 인터셉션(API remoting, kernel-space interception, PTX instrumentation)부터 하드웨어 파티셔닝(MIG), 새로운 ISA(NeuISA), 새로운 마이크로커널 스타일 아키텍처(μShell)까지 매우 다양한 해법을 보여준다.

## 2. Mechanism design space

이 corpus가 보여주는 실제 대안 메커니즘들을 비교하면 다음과 같다.

**API forwarding/remoting** (VIRT-ATC24-23 gVulkan): 클라이언트의 API 호출(Vulkan)을 가로채 원격 서버의 여러 물리 GPU에 전달한다. 미수정 애플리케이션과의 호환성이 강점이지만, per-frame 고정 오버헤드가 스케일링 한계를 만든다. VIRT-ATC25-03(kernel-space interception)은 API remoting이 CUDA/Vulkan 버전이 바뀔 때마다 깨진다는 점을 정면으로 지적하며 kernel 레벨 개입으로 이를 우회한다.

**MPS 시간/공간 공유(temporal+spatial sharing)**: NVIDIA MPS는 여러 프로세스가 같은 GPU address space를 공유하게 하는 소프트웨어 메커니즘으로, 격리가 약하다(VIRT-MICRO24-16 Veiled Pathways: MPS 격리는 uncore 채널로 우회 가능; VIRT-ATC25-03: adversarial 상황에서 MPS는 8/8 피해자 프로세스를 crash시킴). 반대로 VIRT-EUROSYS25-07(Bless)처럼 MPS 위에 kernel-squad 단위의 SM 파티셔닝을 얹어 bubble 없는 활용률을 얻는 SUPPORT 계층 연구가 많다.

**MIG 공간 파티셔닝**: 하드웨어가 SM/캐시/메모리 컨트롤러를 물리적으로 분리해 강한 fault isolation을 준다. 그러나 (1) L3 TLB는 파티션 밖에 있어 공유된다(VIRT-MICRO24-07 STAR), (2) 파티션 레이아웃이 고정되어 재구성 비용이 크다(VIRT-CCGRID25-01: 재파티셔닝은 draining이 필요해 tardiness가 증가), (3) 파티션 크기가 이산적이라 내부/외부 파편화가 생긴다(VIRT-SC24-01 ParvaGPU, VIRT-HPDC25-02 FluidFaaS: 선행 연구가 평균 167% 과할당).

**Kernel-level interception**: VIRT-ATC25-03은 ioctl을 가로채 command buffer 페이지의 page-protection을 조작해 MIG 위에 소프트웨어 시간분할 계층을 쌓는다. VIRT-ASPLOS25-03 Tally, VIRT-SOSP25-14 LithOS는 CUDA driver API 레벨에서 인터셉트해 PTX 커널을 block-level slicing/atomization으로 다시 쓴다. 공통적으로 "GPU 벤더가 주지 않는 preemption을 소프트웨어가 커널 변환으로 만들어낸다"는 패턴이다.

**Preemption**: GPU는 하드웨어 preemption이 없거나(REEF류 reset-based) 있어도 느리다(wait-based, ~5ms). VIRT-ATC25-05 GPreempt는 문서화되지 않은 GPU 하드웨어 timeslice 메커니즘을 리버스엔지니어링해 40us급 preemption을 달성했고, VIRT-OSDI25-11 XSched는 이 wait/reset 스펙트럼을 GPU뿐 아니라 NPU/ASIC/FPGA까지 일반화해 3단계 preemption level을 정의했다.

**GPU checkpoint/restore**: VIRT-SOCC24-01(gCROP)과 VIRT-SOSP25-06(PhoenixOS)는 GPU에는 CPU의 dirty bit/copy-on-write가 없다는 문제를 소프트웨어로 재현한다(soft dirty bit, kernel DAG 기반 speculative buffer-access 추적). PhoenixOS는 stop time을 726ms에서 ~1ms로 줄여 live migration까지 가능하게 한다.

**Full vGPU passthrough**: VIRT-ASPLOS26-02(gShare)는 vfio-mdev API를 이용한 VM-passthrough 방식으로 가변 크기 vGPU 슬라이스(128MB-40GB)를 서버리스 VM에 hot-plug한다. Passthrough는 near-native 성능(<1% 손실)을 주지만 hot-plug 자체가 원래 ~700ms 걸리는 문제를 별도로 풀어야 했다.

**FPGA shell 아키텍처**: VIRT-ASPLOS25-13(Harmonia), VIRT-SOSP25-10(Coyote v2), VIRT-SOCC25-05(Funky), VIRT-HPDC25-01(F3), VIRT-OSDI26-07(μShell)는 모두 "shell이 PCIe DMA/MMU를 소유하고 tenant에는 좁은 인터페이스만 노출한다"는 CPU 하이퍼바이저와 동형인 패턴을 따르지만, 격리 단위가 다르다: Coyote v2는 vFPGA당 하드웨어 MMU, Funky/F3는 unikernel+hypercall 매개, μShell은 capability 기반(CEU) 마이크로커널 스타일 모듈 조합이다. Proteus(VIRT-EUROSYS26-02)는 벤더/용량이 다른 이기종 FPGA 풀 위에 하나의 논리적 가속기를 놓으려는 시도지만 abstract 수준 근거만 있다.

**NPU/PIM/QPU 가상화**: VIRT-MICRO24-01(NeuISA/vNPU)은 VLIW 명령을 micro-Tensor Operator로 쪼개 SR-IOV 스타일 passthrough와 하이퍼바이저 스택을 통해 harvestable NPU 멀티테넌시를 만든다(칩 면적 0.04%만 추가). VIRT-MIDDLEWARE24-02(vPIM)는 PIM rank 전체를 통째로 한 VM에 할당하는 방식(아직 sub-rank 공유는 없음)으로 virtio 스타일 프론트/백엔드를 재사용한다. VIRT-OSDI25-04(HyperQ/Quantum VM)와 VIRT-OSDI25-14(QOS)는 QPU를 공간적으로(qubit 버퍼 zone) 그리고 시간적으로(measurement-and-reset) 나누는데, "context switch가 없다"(QRAM 부재)는 근본적 차이를 명시적으로 지적한다.

이 스펙트럼을 정리하면: API remoting은 호환성은 좋지만 확장성 한계, MPS는 유연하지만 격리 약함, MIG는 격리 강하지만 재구성 비용/파편화, kernel interception은 둘의 장점을 소프트웨어로 합성하려는 시도, preemption/checkpoint는 상태 이동성을 얻기 위한 해법, FPGA shell/NPU ISA/QPU scheduling은 GPU 바깥의 가속기에도 같은 문제가 반복됨을 보여준다.

## 3. 핵심 논문 (P0/P1)

**VIRT-MICRO24-01 (NeuISA, MICRO 2024, CORE P0)**: TPUv4급 NPU를 위한 vNPU. VLIW 명령을 micro-Tensor Operator(uTop)로 분해해 ME(matrix)/VE(vector) 슬롯을 컴파일 타임에 워크로드 프로파일에 따라 배분하고, 런타임에 유휴 엔진을 다른 vNPU가 harvest하게 한다. SR-IOV 스타일 passthrough와 IOMMU DMA remapping으로 격리한다. p95 tail latency 1.56배 개선, 하드웨어 오버헤드는 칩의 0.04%에 불과하다. Trade-off: 새로운 ISA 계층과 컴파일러 백엔드가 필요하며, 테넌트 간 ME:VE 수요 비율이 불균형할 때만 이득이 크다.

**VIRT-HPDC25-01 (F3, HPDC 2025, CORE P0)**과 **VIRT-SOCC25-05 (Funky, SoCC 2025, CORE P0)**: 둘 다 F3/Funky 계열로 CPU 코드는 unikernel(IncludeOS/Solo5)에서 실행되고 FPGA 접근은 hypercall로만 매개된다. FPGA Shell이 PCIe DMA/MMU를 정적으로 예약하고 Dynamic Partial Reconfiguration으로 vFPGA 영역을 나눈다. F3는 함수당 28.6배 평균 속도향상(1.6-150.3배)을 보이지만 워크로드 적합성이 갈린다(AES는 CPU AES-NI에 패배). Funky는 Kubernetes 호환 스케줄러/런타임에 preemption·checkpoint/restore를 추가해 OCI 이미지를 28.7배 줄였다. 두 논문은 "CPU 가상화와 똑같은 방식(hypervisor mediation, hypercall, MMU 기반 공간 파티셔닝, 다층 상태 캡처)을 FPGA에 적용한" 거의 이상적인 CORE 사례다.

**VIRT-OSDI26-06 (Nixie, OSDI 2026, CORE P0)**: 소비자 GPU를 위한 투명한 시간 멀티플렉싱. NVIDIA UVM의 demand-paging이 겪는 thrashing(4-12배 slowdown), 단방향 PCIe, 과도한 pinned memory 문제를 해결하기 위해 애플리케이션 전체 working set을 명시적으로 이동시키는 중앙 조정 Daemon을 둔다. Interactive task에서 nvshare 대비 3.1-3.8배 latency 개선. Trade-off: 단일 사용자/동일 UID 신뢰를 가정하며 진짜 멀티테넌트 보안 격리는 아니다. GPU virtualization을 "OS demand-paging에 맡기지 않고 명시적 마이그레이션 계획으로 재구성"한 완결적 사례.

**VIRT-SOSP24-01 (vSoC, SOSP 2024, CORE P0)**: 모바일 SoC는 unified-memory 아키텍처라서 PC/서버식 modular per-device virtualization(virtio/SR-IOV)이 비효율적이라는 것을 보인다. SVM Manager가 64-bit ID로 공유 메모리 영역을 참조하게 해 guest-host 카피를 제거하고, twin hypergraph와 virtual command fence로 cross-device 순서를 보장한다. 인기 앱에서 12-49% FPS 개선, 신규 멀티디바이스 앱에서 최대 9.0배. Trade-off: adversarial guest에 대한 보안 격리가 전혀 없다 — 통합 메모리 가속기 가상화가 격리를 어떻게 희생하는지 보여주는 명확한 사례.

**VIRT-ASPLOS25-13 (Harmonia, ASPLOS 2025, CORE P1)**: 이기종 클라우드 FPGA(벤더/세대 상이)를 위한 tailorable shell. Reusable Building Block으로 shell 코드 66-87%를 절감하고 shell을 69-93% 재사용 가능하게 한다. Douyin에서 수년간 수만 개 FPGA 가속기 운영. Trade-off: 통합 shell이 손수 최적화된 shell보다 3-25.1% 더 많은 fabric을 쓴다.

**VIRT-SOSP25-10 (Coyote v2, SOSP 2025, CORE P1)**: FPGA 개발 노력의 75%가 인프라에 소비된다는 문제의식에서, host DRAM+FPGA HBM에 걸친 공유 가상 메모리, 멀티스레드 스트림 인터페이스(cThreads), RDMA 네트워크 엔드포인트를 갖춘 vFPGA를 제공한다. Reconfiguration을 55-71초(Vivado)에서 kernel-only 51-85ms로 단축. Trade-off: 라우팅 혼잡으로 실질 vFPGA 개수는 8-10개로 제한되고 MMU 매개 변환이 HBM 대역폭 확장을 캡핑한다.

**VIRT-OSDI26-07 (μShell, OSDI 2026, CORE P1)**: 모놀리식 FPGA shell 대신 마이크로커널 스타일 capability(CEU: send/receive/memory gateway) 기반으로 모듈을 조합한다. Coyote v2 대비 reconfiguration 연산 79% 감소, tail latency 28-39% 감소. CPU 마이크로커널의 capability/IPC 격리 철학을 가속기 가상화에 직접 적용한 가장 명확한 사례.

**VIRT-ATC25-03 (kernel-space interception, ATC 2025, CORE P1)**: IGPU(s,t,m) = MIG 공간 슬라이스 + 시간 quota + 메모리 quota. ioctl 가로채기와 page-protection(mprotect_pkey)으로 명령 버퍼 쓰기를 차단해 협조적이지만 커널이 강제하는 시분할을 MIG 위에 얹는다. 동일 처리량 목표 달성에 필요한 GPU 수를 32.1% 줄임. Trade-off: MIG의 실시간 공간 재구성 능력을 잃는다.

**VIRT-SOSP25-14 (LithOS, SOSP 2025, CORE P1)**과 **VIRT-SOCC25-05(gShare 계열)**: LithOS는 CUDA driver API에 드롭인 라이브러리로 개입해 TPC(가장 세밀하면서도 이식 가능한 단위) 수준에서 스케줄링한다. Kernel atomizer가 소스/PTX 접근 없이 커널을 250-500us 단위 atom으로 쪼갠다. MPS 대비 13배 tail latency 감소. Trade-off: 리버스엔지니어링된 QMD 구조체에 의존해 GPU 세대마다 재작업이 필요하고 메모리 대역폭/IO 격리는 다루지 못한다. "GPU 가상화가 왜 어려운지"에 대한 이 corpus의 가장 명료한 진술이다.

**VIRT-SOCC24-01 (gCROP, SoCC 2024, CORE P1)**과 **VIRT-SOSP25-06 (PhoenixOS, SOSP 2025, CORE P1)**: 둘 다 GPU에 CRIU류 dirty-bit/COW가 없다는 근본 제약을 소프트웨어로 재현한다. gCROP은 CPU/GPU 복원을 분리된 주소공간에서 병렬화해 44-97ms 재시작(CRIU 대비 5.5-23.5배). PhoenixOS는 kernel DAG로 버퍼 접근을 추론(speculate)하고 PTX instrumentation으로 검증해 soft dirty bit/soft COW를 만들어 stop time을 726ms→~1ms로 줄이고 GPU live migration(Llama-2-13B downtime 7.9s→0.4s)을 가능케 한다.

**VIRT-ASPLOS26-02 (gShare, ASPLOS 2026, CORE P1)**: vfio-mdev 커널 개입으로 VM-passthrough vGPU 슬라이스를 서버리스 함수에 hot-plug(<1ms, 기존 ~700ms 대비)한다. GPU 사용량 43-63% 절감, SLO 준수 95% 이상. "스케줄러가 아니라 진짜 가상화 계층"의 최신 사례.

**VIRT-OSDI25-04 (HyperQ/Quantum VM, OSDI 2025, CORE P1)**: QPU를 물리적 topology 단위(예: IBM Eagle의 7-qubit unit)로 공간 파티셔닝하고, context switch가 불가능하므로(QRAM 없음) measurement-and-reset으로 시간 공유한다. 처리량 8.4-9.7배, 큐잉 시간 수 시간→수십 초. 고전 가상화 개념(guest interface, 공간 파티션, 시간 멀티플렉싱, fault isolation)이 QPU에서 재현되면서 어디서 비유가 깨지는지(state 저장 불가) 정확히 보여준다.

## 4. Supporting 논문 (P2/P3)

GPU 공유 스케줄러 군: **VIRT-EUROSYS24-03 (Orion)**은 커널 단위 우선순위 스트림으로 7.3배 처리량을 얻지만 보안 격리와 캐시 간섭 모델링이 없다. **VIRT-ASPLOS25-03 (Tally)**는 PTX 레벨 kernel slicing/persistent-thread-block으로 MPS 대비 tail latency를 크게 낮춘다. **VIRT-EUROSYS25-07 (Bless)**는 kernel squad 단위 spatial-temporal 하이브리드로 MIG/MPS/시분할을 모두 능가하는 latency를 보인다. **VIRT-ATC25-05 (GPreempt)**는 undocumented 하드웨어 timeslice를 이용해 40us 이하 preemption을 실현. **VIRT-OSDI25-11 (XSched)**는 GPU/NPU/ASIC/FPGA를 아우르는 통합 preemption API. 읽는 이유: MIG/MPS를 대체하지 않고 그 위/옆에서 스케줄링 정책만 바꾸는 것이 왜 SUPPORT로 분류되는지의 반복적 실례.

MIG/MPS 조합·배치 최적화: **VIRT-SC24-01 (ParvaGPU)**, **VIRT-HPDC25-02 (FluidFaaS)**, **VIRT-CCGRID25-01 (동적 MIG 재파티셔닝)**은 모두 "기존 하드웨어 파티셔닝 기법을 조합/재배치"하는 스케줄링 레이어다. **VIRT-MICRO24-07 (STAR)**는 MIG가 파티션하지 않는 L3 TLB의 sub-entry를 안전하게 공유해 MIG 격리 틀 안에서 성능만 개선한다(30.2% 평균 개선, 1.4% 면적).

GPU 보안/간섭 특성화: **VIRT-MICRO24-16 (Veiled Pathways)**는 MPS/MIG의 "uncore"(DRAM 주파수 스케일링, 코덱 엔진, PCIe)가 여전히 공유되어 covert channel이 된다는 것을 실증한다(MIG를 우회하는 PCIe 채널 6.8kbps). **VIRT-SOCC25-14 (Understanding GPU Resource Interference One Level Deeper)**는 block scheduler/L2/공유메모리 뱅크/IPC 4가지 간섭원을 정량화해 spatial colocation 스케줄러가 왜 예측 불가능한지 설명한다.

서버리스/추론 특화 GPU 멀티플렉싱: **VIRT-ATC24-03 (StreamBox)**는 함수당 풀 컨텍스트 대신 스트림을 줘 시작 지연 98% 절감하지만 신뢰 도메인을 가정한다. **VIRT-ATC25-09 (Torpor)**는 "late binding"으로 GPU 메모리에서 모델을 swap in/out. **VIRT-ASPLOS25-06 (Dilu)**는 LD_PRELOAD 토큰 기반 5ms 단위 SM 재분배. **VIRT-SOSP25-07 (Aegaeon)**은 토큰 단위 autoscaling으로 모델 87% GPU 절감(알리바바 프로덕션). 이들은 모두 MIG/MPS라는 CORE 메커니즘을 소비하는 스케줄링/서빙 계층이다.

기타: **VIRT-ATC24-07(모바일 클라우드 게이밍)**은 vGPU 추상화 없이 화면 영역 기반 공간 분할을 하는 실전 사례. **VIRT-MIDDLEWARE24-04(Guardian)**와 **VIRT-MIDDLEWARE24-06(Menos)**는 각각 PTX bounds-checking과 base-model 공유로 GPU 공간 공유를 안전/효율화한다. **VIRT-ASPLOS24-03(GMLake)**는 단일 프로세스 내 GPU 메모리 조각화를 가상주소 스티칭으로 해결하는, 멀티테넌시가 아닌 VM-개념 재사용 사례. **VIRT-CCGRID26-03/04**는 MPS 우선순위와 AMD SVM oversubscription eviction 정책을 각각 개선한다. **VIRT-EUROSYS26-19 (RoPeerTo)**와 **VIRT-ASPLOS26-03 (TEEM3)**, **VIRT-HPCA26-03 (SCALE)**, **VIRT-MICRO25-01 (ccAI)**는 가속기 간(GPU-FPGA) P2P DMA, 이기종 TEE 합성, confidential GPU 통신, PCIe 레벨 confidential computing 등 "가속기 가상화가 confidential computing/이기종 상호연결로 확장"되는 최신 방향이다.

## 5. Trade-off 구조

- **호환성 vs 확장성**: API remoting(gVulkan)은 미수정 앱 호환성을 얻지만 고정 오버헤드가 스케일링 천장을 만든다.
- **격리 강도 vs 재구성 유연성**: MIG는 하드웨어 fault isolation을 주지만 파티션 변경이 draining을 요구해 비싸다(CCGRID25-01). Kernel interception(ATC25-03)은 시간 유연성을 얻는 대신 MIG의 실시간 공간 재구성을 포기한다.
- **Preemption 속도 vs 일반성**: reset-based는 빠르지만 idempotent 커널에만 안전, wait-based는 일반적이지만 느리다(~5ms). GPreempt/XSched는 하드웨어 특이점을 활용해 이 딜레마를 부분적으로 깬다.
- **상태 이동성 vs 구현 복잡도**: GPU checkpoint/restore(gCROP, PhoenixOS)는 CPU에 있는 dirty bit/COW를 소프트웨어로 재현해야 하며, 이는 speculation과 fallback 경로라는 복잡성을 낳는다.
- **통합 shell의 일반성 vs 자원 비용**: FPGA shell을 벤더/역할에 무관하게 만들수록(Harmonia, Coyote v2, Proteus) fabric 자원을 더 소모한다(3-25%).
- **소프트웨어 안전 검사 vs 처리량**: Guardian의 PTX bounds checking은 안전한 공간 공유를 주지만 4-12% 처리량을 희생한다.
- **가속기 확장 시 신뢰 경계 이동**: 단일 CPU CVM 경계에서 GPU-TEE, 다중 GPU NVLink, 이기종 가속기 조합(ccAI, SCALE, TEEM3)으로 신뢰 경계가 확장될수록 통신 암호화 지연이 새로운 병목이 된다.

## 6. 인접 계층과의 관계

- **T1 (CPU/machine virtualization) 위**: NeuISA와 gShare는 SR-IOV/vfio-mdev passthrough처럼 CPU virtualization에서 온 device-passthrough 패턴을 가속기에 적용한다.
- **T2 (메모리 가상화)와의 다리**: GMLake(가상주소 스티칭), STAR(TLB sub-entry 공유), CCGRID26-04(AMD SVM oversubscription)는 GPU 메모리를 guest-physical 메모리처럼 다룬다.
- **T4 (migration/checkpoint) 위**: gCROP, PhoenixOS, ServerlessLLM(T8)의 model live-migration은 T4의 VM live migration 개념을 가속기 상태로 확장한 것이다.
- **T8 (서버리스) 아래**: F3, Funky, gShare, StreamBox, Torpor, Dilu, FluidFaaS는 T6의 가속기 가상화 메커니즘을 서버리스가 소비하는 다리 논문이다.
- **T9 (자원관리) 위**: Orion, Bless, KACE, ParvaGPU, Priority-Aware Co-Scheduling 등 거의 모든 "GPU 스케줄링" SUPPORT 논문은 T6의 MIG/MPS를 given으로 놓고 배치·우선순위 정책만 얹는다 — T9 파일에서 자세히 다루는 패턴이 T6에서 시작된다.
- **T7 (confidential computing) 위**: ccAI, SCALE, TEEM3는 신뢰 경계를 가속기까지 확장하며 T7의 CVM 개념과 직접 연결된다.

## 7. 2024 → 2026 변화

제안된 시퀀스 "단순 공유 → 공간/시간 파티셔닝 → QoS/격리 → 마이그레이션/preemption → 클라우드/서버리스 추상화"를 이 corpus의 증거로 검증하면:

- **단순 공유 → 파티셔닝**: 2024년 논문들(Orion, Guardian, ParvaGPU, KACE, StreamBox)은 이미 기존 MIG/MPS 위에서 작동하며, "단순 공유"만 다루는 논문은 거의 없다 — MIG/MPS 자체는 corpus 이전부터 존재하는 기술이기 때문이다. 이 부분은 corpus 시작 시점(2024)에 이미 "파티셔닝 이후" 단계에 와 있었다는 뜻이므로, 순서 전체가 처음부터 관찰되지는 않는다.
- **파티셔닝 → QoS/격리**: 이 전환은 뚜렷하다. 2024년은 STAR(TLB sub-entry), Guardian(PTX bounds check), Veiled Pathways(uncore covert channel 발견)처럼 "기존 파티셔닝의 격리 구멍을 메우거나 드러내는" 논문이 많았다. 2025년에는 ATC25-03(kernel interception), Bless, GPreempt, Tally처럼 QoS 보장을 소프트웨어로 강화하는 논문이 집중적으로 등장한다.
- **QoS/격리 → 마이그레이션/preemption**: 2025년 중후반부터(PhoenixOS, GPreempt, XSched, gShare) preemption과 checkpoint/migration이 본격적으로 다뤄진다. PhoenixOS(SOSP25)와 gShare(ASPLOS26)는 이 단계가 2025-2026에 성숙했음을 보여준다.
- **→ 클라우드/서버리스 추상화**: F3(2025), Funky(2025), gShare(2026), Torpor/Dilu(2025)처럼 서버리스향 가속기 가상화는 2025년부터 집중적으로 나타나며, 2026년 eGPU(HPCA26)처럼 10,000+ GPU 규모의 프로덕션 사례로 이어진다.

결론: 제안된 시퀀스는 "파티셔닝→QoS→마이그레이션→서버리스 추상화" 구간에서는 corpus 증거와 대체로 일치하지만, "단순 공유→파티셔닝" 구간은 corpus가 이미 파티셔닝 기술(MIG/MPS)이 존재하는 시점부터 시작하므로 직접 관찰되지 않는다(가정된 선행 단계일 뿐).

**GPU→FPGA/SmartNIC/DPU/NVMe/NPU로의 일반화**는 명확히 관찰된다. 2024년 NeuISA(NPU)와 vPIM(PIM)이 이미 있었지만, FPGA 가상화 논문(Harmonia, Coyote v2, F3, Funky, Proteus, μShell)의 절대다수는 2025-2026년에 집중되어 있다. XSched(OSDI25)는 GPU/NPU/ASIC/FPGA를 하나의 preemption 프레임워크로 명시적으로 통합한 첫 사례이며, RoPeerTo(EuroSys26)는 GPU-FPGA 간 직접 P2P DMA를 다룬다. 양자 컴퓨팅(QPU) 가상화(HyperQ, QOS)도 2025년에 등장해 "가속기 가상화"라는 패턴이 고전적 계산 자원을 넘어 일반화되고 있음을 보여준다. 다만 FPGA/NPU/QPU 각각의 표본 수는 GPU에 비해 훨씬 작으므로(FPGA 6-7편, NPU 1-2편, QPU 2편), 이 일반화가 GPU만큼 성숙했다고 말하기는 이르다 — 특히 NPU/PIM은 2024년 이후 신규 논문이 거의 늘지 않아 표본이 트렌드를 뒷받침하기엔 너무 작다.

## 8. 읽는 순서 제안

1. **VIRT-SOSP25-14 (LithOS)** — GPU 가상화가 왜 근본적으로 어려운지(preemption 없음, dirty bit 없음, coarse partition)에 대한 가장 명료한 진술.
2. **VIRT-ATC25-03 (kernel-space interception)** — MIG(공간)와 소프트웨어 시분할을 결합하는 구체적 메커니즘.
3. **VIRT-ATC25-05 (GPreempt)** 또는 **VIRT-OSDI25-11 (XSched)** — preemption 설계 공간을 GPU 내부에서, 그리고 이기종 가속기로 일반화.
4. **VIRT-SOCC24-01 (gCROP)** → **VIRT-SOSP25-06 (PhoenixOS)** — checkpoint/restore가 어떻게 migration으로 이어지는지.
5. **VIRT-MICRO24-01 (NeuISA)** — GPU 밖에서 같은 문제(NPU)를 ISA 레벨에서 어떻게 푸는지 비교.
6. **VIRT-HPDC25-01 (F3)** → **VIRT-SOSP25-10 (Coyote v2)** → **VIRT-OSDI26-07 (μShell)** — FPGA 가상화가 unikernel/hypercall 방식에서 마이크로커널/capability 방식으로 진화하는 궤적.
7. **VIRT-ASPLOS26-02 (gShare)** — 이 모든 메커니즘이 서버리스 VM 위에서 실제로 어떻게 합쳐지는지의 최신 종합.
8. **VIRT-OSDI25-04 (HyperQ)** — 고전 가상화 개념이 QPU에서 어디까지 성립하고 어디서 깨지는지 확인.

## 9. 증거 한계

다음 논문들은 abstract/제목 수준 근거에 의존하고 있어 주장의 신뢰도가 상대적으로 낮다: **VIRT-SC24-01 (ParvaGPU, ABSTRACT_INTRO/MEDIUM)**, **VIRT-CCGRID25-01 (에너지 효율 MIG 재파티셔닝, ABSTRACT/MEDIUM)**, **VIRT-SOCC25-15 (ZipBatch, ABSTRACT/MEDIUM)**, **VIRT-CCGRID26-03 (Priority-Aware GPU Co-Scheduling, ABSTRACT/MEDIUM)**, **VIRT-CCGRID26-04 (Enhanced SVM, ABSTRACT/MEDIUM)**, **VIRT-EUROSYS26-02 (Proteus, ABSTRACT/MEDIUM)**, **VIRT-HPCA26-02 (eGPU, ABSTRACT/MEDIUM)**, **VIRT-ASPLOS25-01 (Vela, ABSTRACT/MEDIUM — 본문 대신 companion preprint 수치를 인용)**, **VIRT-ASPLOS26-03 (TEEM3, ABSTRACT/MEDIUM)**, **VIRT-EUROSYS26-19 (RoPeerTo, ABSTRACT/MEDIUM)**, **VIRT-HPCA26-03 (SCALE, ABSTRACT/MEDIUM)**. 이 논문들의 숫자(예: eGPU의 "8배 GPU 절감", Proteus의 메커니즘 세부사항)는 abstract 수준에서만 확인되었으므로 isolation_mechanism/state_mechanism이 "UNKNOWN"으로 남아 있는 경우가 많다. 반대로 P0/P1로 분류된 핵심 논문(NeuISA, F3, Funky, Nixie, vSoC, Harmonia, Coyote v2, kernel-space interception, LithOS, gCROP, PhoenixOS, gShare, HyperQ)은 모두 FULL/HIGH 또는 DESIGN_EVAL/HIGH 근거를 가지고 있어 상대적으로 신뢰도가 높다.

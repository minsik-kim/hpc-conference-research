# Serverless / Cloud Abstraction (T8)

## 1. 이 계층이 푸는 문제

서버리스(FaaS)는 "함수 호출마다 격리된 실행 환경을 밀리초 단위로 만들었다 없앴다 할 수 있는가"라는 질문에 대한 답이다. Physical Resource → Logical Abstraction → Workload 관점에서:

- **Physical Resource**: 호스트 CPU 코어, DRAM, NVMe, NIC, (최근에는) GPU.
- **Logical Abstraction**: 컨테이너/microVM/unikernel/Wasm 샌드박스라는 "즉시 만들고 버릴 수 있는 격리 단위", 그리고 그 단위의 warm pool·snapshot·checkpoint 이미지.
- **Workload**: HTTP 요청 처리 함수, DAG 워크플로우, LLM 추론, 배치/스트리밍 잡.

이 계층의 근본적 긴장은 **"격리는 비싸고, 서버리스의 경제성은 그 격리를 값싸게 반복 생성할 수 있다는 가정 위에 서 있다"**는 것이다(VIRT-SOSP25-08 Dandelion: cold start가 최소 8ms 걸려 idle warm sandbox에 실행 중인 함수보다 16배 많은 DRAM을 묶어둔다; VIRT-EUROSYS26-15 DROPS: warm pool 유지비가 Azure Functions 플랫폼의 가장 큰 비용 항목). 따라서 T8의 핵심 연구 문제는 다음 세 가지로 압축된다: (1) 격리 경계 자체를 얼마나 가볍게 만들 수 있는가(unikernel, Wasm, 단일 address space), (2) 이미 만든 격리 상태를 얼마나 빨리 복제/재사용할 수 있는가(snapshot/restore, fork), (3) 그 경계 안에서 자원(메모리, GPU)을 얼마나 탄력적으로 나눌 수 있는가(memory elasticity, GPU resourcing-on-demand).

## 2. Mechanism design space — 격리 경계를 싸게 만드는 것 vs 서버리스를 소비하는 것

이 corpus는 의도적으로 두 가지를 구분한다:

**(a) 서버리스를 가능하게 하는 가상화 메커니즘 (CORE/SUPPORT)** — snapshot/restore, microVM 메모리 탄력성, unikernel/Wasm 런타임 격리, cold-start 기계장치, 프로세스 snapshot, warm pool의 내부 구현. 이들은 "격리 경계 자체" 또는 "그 경계를 값싸게 반복 생성하는 방법"을 다룬다.

**(b) 가상화된 자원을 그저 소비하는 서버리스 시스템 (CONTEXT)** — 스케줄링, 워크플로우, 비용, 탄소, LLM 서빙. 이들은 이미 주어진 샌드박스/컨테이너 경계를 전제로, 그 위에서 무엇을 최적화할지를 다룬다.

무엇이 격리 비용을 값싸게 만드는지 구체적으로 보면:

- **Snapshot/restore (프로세스/VM 경계)**: VIRT-OSDI24-01(Sabre)는 Firecracker microVM 스냅샷을 근접 메모리 하드웨어 가속기로 압축해 복원 속도를 55% 높인다. VIRT-OSDI26-11(Spice/SHELF)은 프로세스 경계 스냅샷을 페이지 단위 interval-tree 인덱스로 저장해 CRIU 대비 7.5배, VM 경계 시스템(REAP/FaaSnap) 대비 9.5배 빠른 복원을 달성하며, "VM 경계에서만 발생하는 비용(guest scheduler의 clock-jump 이후 deferred housekeeping)"과 "프로세스 경계에서만 발생하는 비용(syscall replay량)"을 명확히 분리한다. VIRT-EUROSYS24-05(Pronghorn)는 CRIU 스냅샷 시점을 JIT warm-up 정도에 따라 확률적으로 골라 hot-start 품질을 높인다.
- **MicroVM 메모리 탄력성**: VIRT-SOCC24-10(Faascale)은 guest kernel + Firecracker VMM + host kernel을 모두 수정해 microVM 메모리를 런타임에 hotplug/reclaim한다. VIRT-EUROSYS26-05(Squeezy)는 hotplug된 메모리를 일반 VM 메모리와 분리해 guest kernel이 그 페이지만 빠르게 회수하게 해 재클레임 지연을 order-of-magnitude 줄인다.
- **Unikernel/Wasm 런타임 격리**: VIRT-SOCC24-04(SURE)는 함수당 Unikraft unikernel(QEMU)로 컨테이너 수준 속도에 VM급 격리를 결합한다. VIRT-SOSP25-13(uFork)는 단일 address space OS(SASOS)에서 CHERI capability로 fork를 가능하게 해(3.7배 빠른 fork), address space를 포기한 대가로 잃는 모든 POSIX 속성을 하나씩 되사는 과정을 보여준다. VIRT-SOSP25-08(Dandelion)은 아예 POSIX를 버리고 순수 함수형 DAG 모델을 채택해 4가지 백엔드(CHERI, rWasm, ptrace, KVM-no-guest-kernel) 각각의 cold start를 89us~889us로 낮춘다 — Firecracker의 ~120ms와 대비된다.
- **단일 address space 공유**: VIRT-EUROSYS25-14(AlloyStack)는 워크플로우 내 여러 함수를 스레드로 한 address space에 넣고 Intel MPK로 LibOS와 사용자 코드만 분리한다(cold start 98.5% 감소, 1.3ms). VIRT-SOCC25-01(Hydra)는 GraalVM Native Image로 compiled code cache/heap을 여러 memory isolate가 공유하게 해 함수 밀도 4.47배를 얻는다.
- **디바이스 I/O 경로의 시작 비용**: VIRT-EUROSYS25-01(FastIOV)는 SR-IOV passthrough를 보안 컨테이너(Kata)에서 쓸 때 발생하는 시작 지연을 lock 분해·비동기 초기화로 65.7% 줄인다 — passthrough의 "제어 평면 경직성"이라는 구조적 비용을 정면으로 공략한 사례.
- **가속기(GPU/FPGA)까지 확장된 격리**: VIRT-HPDC25-01(F3)은 unikernel+hypercall로 FPGA를 서버리스에 안전하게 노출한다. VIRT-ASPLOS26-02(gShare)는 vfio-mdev 기반 vGPU passthrough를 hot-plug해 <1ms 재할당을 달성한다. VIRT-ASPLOS26-04(WorksetEnclave)는 SGX enclave의 EPC 전체가 아니라 실제로 touch된 workset만 스냅샷해 confidential 서버리스의 cold start를 1.9-54배 줄인다.
- **DPU/RDMA 기반 데이터 평면**: VIRT-EUROSYS26-13(NADINO)은 테넌트가 RDMA queue pair를 직접 쥐지 못하게 하고 DPU 상주 엔진이 대신 중개하게 해(물리적 신뢰 분리) 20.9배 처리량을 얻는다.

이 모든 것이 "메커니즘"인 이유는 격리 경계 자체(샌드박스의 종류, 상태 캡처/복원 방식, 자원 탄력성 구현)를 바꾸기 때문이다. 반면 아래 CONTEXT 섹션의 논문들은 이 경계를 그대로 두고 그 위에서 스케줄링/배치/비용 정책만 바꾼다.

## 3. 핵심 논문 (P0/P1)

**VIRT-HPDC25-01 (F3, HPDC 2025, CORE P0)**: FPGA를 서버리스 함수에 안전하게 노출하는 근접-이상적 사례. CPU 코드는 unikernel에서 실행되고 FPGA 접근은 vFPGA manager로의 hypercall만 허용된다. 함수당 평균 28.6배 속도향상(1.6-150.3배), cold-boot 오버헤드는 Docker 대비 11.6%. Trade-off: 워크로드 적합성이 갈리고(AES는 CPU AES-NI에 패배), Dynamic Partial Reconfiguration으로 인한 fabric 파편화가 남는다.

**VIRT-SOSP25-08 (Dandelion, SOSP 2025, CORE P1)**: 프로그래밍 모델 자체를 순수 함수·결정적·syscall-free로 바꿔 guest OS/디바이스 에뮬레이션/네트워크 스택을 샌드박스에서 제거한다. 4개의 교체 가능한 백엔드(CHERI capability bound, rWasm→안전한 Rust, ptrace로 제한된 Linux 프로세스, guest kernel 없는 KVM)로 cold start를 89us~889us까지 낮추고, Firecracker의 120ms 스냅샷 복원과 정면 대비시킨다. Trade-off: 기존 POSIX 코드를 DAG로 재작성해야 하며 OLTP·게이밍처럼 상태를 갖는 워크로드는 아예 배제된다.

**VIRT-SOSP24-04 (SigmaOS, SOSP 2024, CORE P1)**: 서버리스(빠른 시작)와 마이크로서비스(장기 실행·상태유지)를 하나의 플랫폼에서 통합한다. sigma-container는 네트워크 네임스페이스/오버레이 파일시스템 설정을 생략하고, sigma-EP라는 불투명 토큰으로 테넌트 간 통신을 구조적으로 차단하며 syscall 표면을 352→67개로 줄인다. Cold start 7.7ms (AWS Lambda 1290ms, Docker 2671ms 대비), 클러스터 전체 처리량 36,650 procs/sec. Trade-off: sigmaOS API로 애플리케이션을 포팅해야 하며 out-of-the-box Linux 호환성이 없다.

**VIRT-SOSP25-13 (uFork, SOSP 2025, CORE P1)**: 단일 address space OS는 가볍지만 정확히 그 이유로 POSIX fork를 지원할 수 없다는 역설을 CHERI capability로 푼다. Copy-on-pointer-access(CoPA)라는 새로운 fault 메커니즘으로 "읽기만 해도 stale 포인터 문제가 생기는" 상황을 해결한다. Fork 지연 54us(CheriBSD 대비 3.7배, VM 기반 SASOS fork 대비 198배), 프로세스당 0.13MB. Trade-off: CHERI 하드웨어와 fault-on-capability-load 기능에 의존한다.

**VIRT-EUROSYS25-14 (AlloyStack, EuroSys 2025, CORE P1)**: 격리 단위를 함수에서 워크플로우로 넓히면 샌드박스 생성과 함수 간 데이터 전달이 모두 "비용"에서 "비발생 사건"으로 바뀐다는 것을 명확히 보여준다. Cold start 1.3ms, 16MB 중간 데이터 전송이 Faastlane-refer 대비 Rust에서 2.6배, C에서 13.2배 빠르다. Trade-off: 워크플로우 내부 격리 강도가 MPK+명령어 블랙리스트로 낮아지고, 함수가 as-std에 맞게 컴파일되거나 WASM이어야 한다.

**VIRT-OSDI24-01 (Sabre, OSDI 2024, CORE P1)**: Firecracker 스냅샷/복원 파이프라인에 근접 메모리 하드웨어 압축을 통합해 스냅샷 크기를 최대 4.5배 줄이고 메모리 복원을 최대 55% 빠르게 한다. VM live-migration/snapshot의 데이터 이동 병목을 알고리즘이 아니라 하드웨어 오프로드로 공략한 사례. Trade-off: 특정 근접 메모리 가속기 하드웨어가 호스트 CPU에 있어야 한다.

**VIRT-SOCC24-10 (Faascale, SoCC 2024, CORE P1)**과 **VIRT-EUROSYS26-05 (Squeezy, EuroSys 2026, CORE P1)**: 둘 다 Firecracker microVM 메모리를 정적 크기에서 탄력적으로 바꾸려는 시도다. Faascale은 guest+VMM+host kernel을 모두 수정하는 조율된 hotplug/reclamation 경로를 만들고, Squeezy는 그 reclamation이 왜 느린지(guest kernel이 hotplug된 페이지를 일반 메모리와 구분하지 못함)를 정확히 짚어 order-of-magnitude 빠른 회수를 달성한다.

**VIRT-EUROSYS25-01 (FastIOV, EuroSys 2025, CORE P1)**: SR-IOV passthrough는 데이터 평면 성능은 최고이지만 제어 평면(디바이스 부착)이 무겁다는 구조적 트레이드오프를 정면으로 공략해, VF 락 분해·불필요한 DMA 매핑 제거·비동기 guest driver 초기화로 시작 지연을 65.7% 줄인다. Passthrough를 포기하지 않고 그 비용만 갚아나가는 접근.

**VIRT-ASPLOS26-02 (gShare, ASPLOS 2026, CORE P1)**과 **VIRT-ASPLOS26-04 (WorksetEnclave, ASPLOS 2026, CORE P1)**: 각각 GPU와 SGX enclave라는, 전통적 서버리스가 다루지 않던 자원까지 "cold start를 빠르게 만드는" 대상으로 확장한다. gShare는 vfio-mdev hot-plug로 GPU 재할당을 <1ms로, WorksetEnclave는 workset 범위로 제한된 EPC 스냅샷으로 confidential serverless cold start를 1.9-54배 줄인다.

**VIRT-EUROSYS26-13 (NADINO, EuroSys 2026, CORE P1)**: SR-IOV류 하드웨어 파티셔닝에서 DPU 매개 소프트웨어 정의 격리로 넘어가는 최신 사례. 테넌트 함수가 RDMA queue pair를 절대 직접 쥐지 못하게 하고, off-path DPU Network Engine이 대신 중개해 20.9배 처리량과 7개 호스트 코어 절약(DPU 코어 2개 소비)을 달성한다.

**VIRT-SOSP25-06 (PhoenixOS, SOSP 2025, CORE P1)**: GPU에는 CPU의 dirty bit/COW가 없어 stop-the-world checkpoint(수백 ms)가 강제된다는 문제를, kernel DAG 기반 speculative buffer-access 추적과 PTX instrumentation 검증으로 해결해 stop time을 ~1ms로 줄이고 GPU live migration(Llama-2-13B downtime 7.9s→0.4s)까지 가능케 한다. 서버리스 GPU 콜드스타트를 최대 82% 줄이는 응용까지 이어진다.

## 4. Supporting 논문 (P2/P3) — 메커니즘 (a)의 나머지, 그리고 CONTEXT (b)

**메커니즘을 보강하는 SUPPORT 논문들**: VIRT-ASPLOS24-05(RainbowCake)와 VIRT-ASPLOS24-06(FaaSMem)은 각각 컨테이너 캐싱과 유휴 페이지 오프로딩으로 warm-keep 비용의 캐싱/회수 두 측면을 다룬다. VIRT-EUROSYS24-06(Desiccant/Frozen Garbage)은 정지(paused)된 컨테이너의 GC가 멈춰 죽은 객체가 쌓이는 문제를 프로파일 기반으로 강제 회수해 최대 6.72배 메모리를 줄인다. VIRT-EUROSYS24-07(RMMAP)은 워크플로우 단계 간 상태 전달을 직렬화 없이 RDMA 페이지 폴트로 처리한다(14-97.8% 지연 감소). VIRT-OSDI25-05(Fork in the Road/AFaaS)는 프로덕션 cold start의 실제 병목을 분해해 제어 경로 RPC/셈, 동시성 하 자원 경합, 사용자 코드 초기화가 샌드박스 부팅 자체보다 크다는 것을 보인다. VIRT-MIDDLEWARE25-04(Roadrunner)와 VIRT-MIDDLEWARE25-05(RUNE)는 Wasm 샌드박스의 데이터 경로/콜드스타트-실행속도 트레이드오프를 다룬다.

읽는 이유: 이들은 CORE 메커니즘(스냅샷, unikernel, LibOS)이 실전에서 왜 그 정도 성능만 내는지의 세부 원인을 채운다.

**GPU를 서버리스에 얹는 SUPPORT 논문들**: VIRT-ATC24-03(StreamBox), VIRT-ATC25-09(Torpor), VIRT-ASPLOS25-06(Dilu), VIRT-ASPLOS25-09(Medusa), VIRT-HPDC25-02(FluidFaaS), VIRT-SOSP25-07(Aegaeon)은 모두 T6의 MIG/MPS 또는 GPU 메모리 스왑을 given으로 놓고 그 위에서 스케줄링/late-binding/materialization 정책을 최적화한다. 예컨대 Torpor는 모델을 host memory에 두었다가 요청이 올 때만 GPU로 옮기는 "late binding"으로 100+ 함수/GPU 밀도를 달성하지만 GPU 가상화 메커니즘 자체를 바꾸지는 않는다.

**보안/취약점 증거**: VIRT-ASPLOS24-10(Everywhere All at Once)은 Google Cloud Run의 "불투명한 배치"가 TSC 지문 인식과 수요 조작으로 100% 확률의 co-location 공격을 가능케 함을 보여, "추상화가 격리를 자동으로 보장하지 않는다"는 corpus 전체의 핵심 논지를 서버리스에서 실증한다.

**CONTEXT — 서버리스를 소비하는 시스템들**: DIGEST_CONTEXT.md에는 40여 편의 P3 CONTEXT 논문이 있으며, 이들은 격리/스냅샷 메커니즘을 전혀 바꾸지 않고 그 위의 문제를 다룬다. 크게 네 갈래로 나뉜다.

1. *콜드스타트 경제학/측정*: VIRT-EUROSYS25-11(Serverless Cold Starts and Where to Find Them)은 실제 콜드스타트에서 가상화 계층이 차지하는 비중의 상한을 제공하고, VIRT-CCGRID25-02(Data Store Event Trigger 특성화)는 '서버리스' 호출의 상당 부분이 격리 비용이 아니라 제어 평면 배관임을 정량화한다. VIRT-HPDC24-04(FaaSRail), VIRT-HPDC24-03(FaaSKeeper)은 실제 FaaS 워크로드 형태(극단적 인기 편중, sub-second 실행)를 문서화해 왜 CORE 메커니즘이 sub-second 침습 최적화에 집중하는지 설명한다.
2. *스케줄링/오케스트레이션*: VIRT-ATC24-01(Jiagu), VIRT-ATC24-02(ALPS), VIRT-CCGRID25-03(Hiku), VIRT-SOSP24-05(Dirigent), VIRT-MIDDLEWARE24-11(하이브리드 OS 스케줄러)은 샌드박스/런타임 경계를 건드리지 않고 그 위의 배치·트리거·풀링 정책을 최적화한다.
3. *비용/탄소/LLM 서빙 맥락*: VIRT-ASPLOS25-07(Litmus), VIRT-SC25-06(GreenMix), VIRT-CCGRID26-06(Green or Fast), VIRT-EUROSYS26-12(Demystifying Serverless Costs), VIRT-ATC25-08(DEEPSERVE), VIRT-MICRO25-03(Chameleon)은 각각 가격 공정성, 에너지, 탄소, 청구 구조, 대규모 LLM 서빙 운영을 다루며 "왜 GPU 공유/메모리 가상화 메커니즘이 필요한가"라는 동기를 제공하지만 메커니즘 자체는 만들지 않는다.
4. *워크플로우/네트워킹/보안 상위 계층*: VIRT-SOSP25-09(Quilt), VIRT-EUROSYS26-09(iRoute), VIRT-EUROSYS26-16(Fix), VIRT-CCGRID26-09(PoliFlow), VIRT-CCGRID26-08(LogLearners), VIRT-CCGRID26-07(Kumo)은 워크플로우 병합, 라우팅, 네트워크 I/O 외부화, 정책 추론, AI 함수 공급망 보안 등을 다루는데 모두 이미 격리된 함수 샌드박스를 전제로 한다.

이들을 읽는 이유는 (a) 메커니즘의 *동기*를 이해하기 위해서다 — 예를 들어 WorksetEnclave(메커니즘)를 읽기 전에 DEEPSERVE나 Chameleon(맥락)을 보면 왜 confidential/GPU 콜드스타트가 실제로 문제가 되는지 체감할 수 있다. 그러나 이들 자체를 가상화 메커니즘으로 인용해서는 안 된다.

## 5. Trade-off 구조

- **격리 범위 확대 vs 비용 감소**: 함수 단위(container-per-function) → 워크플로우 단위(AlloyStack, Hydra) → 순수 함수형 전체(Dandelion)로 격리 단위를 넓힐수록 콜드스타트/데이터전달 비용은 줄지만, 테넌트 간 격리 강도와 프로그래밍 모델 호환성을 희생한다.
- **VM 경계 vs 프로세스 경계 스냅샷**: VM 경계(REAP/FaaSnap)는 강한 격리를 주지만 guest scheduler clock-jump 이후 housekeeping storm(22-79%)을 겪는다. 프로세스 경계(Spice/SHELF)는 그 비용은 없지만 syscall replay 볼륨이라는 별도의 비용을 진다.
- **Passthrough의 데이터 평면 속도 vs 제어 평면 경직성**: SR-IOV passthrough(FastIOV), vGPU passthrough(gShare)는 near-native 성능을 주지만 디바이스 부착/해제 자체가 원래 느리다 — 이 경직성을 갚는 것이 별도 연구 주제가 될 정도다.
- **하드웨어 오프로드 vs 특정 하드웨어 의존**: Sabre의 근접 메모리 압축, NADINO의 DPU 오프로드는 성능은 크게 얻지만 특정 가속기/DPU 벤더 API에 종속된다.
- **경제성(cost) 최적화 vs 메커니즘 개선**: CONTEXT 논문들(Litmus, GreenMix, DEEPSERVE)이 보여주듯, 스케줄링/가격 정책만으로도 상당한 개선이 가능하지만 근본적 콜드스타트 하한은 메커니즘(스냅샷/샌드박스 종류)이 결정한다 — 두 계층은 서로 대체할 수 없고 보완적이다.

## 6. 인접 계층과의 관계

- **T4 (migration/checkpoint) 아래**: Sabre, Pronghorn, Spice/SHELF, PhoenixOS는 모두 T4의 VM/프로세스 checkpoint-restore 개념을 서버리스 콜드스타트 문제에 특화 적용한 것이다.
- **T5 (경량 격리) 아래**: SigmaOS, SURE, Dandelion, AlloyStack, Hydra는 T5의 unikernel/Wasm/컨테이너 격리 스펙트럼을 서버리스 요구(빠른 시작)에 맞춰 재설계한다.
- **T2 (메모리 가상화) 위**: Faascale, Squeezy는 T2의 ballooning/hotplug 개념을 microVM에 특화한 것이며, FaaSMem은 T2의 memory pool/오프로딩 패턴을 재사용한다.
- **T6 (가속기 가상화) 아래**: F3, gShare, WorksetEnclave, Torpor, Dilu, PhoenixOS는 모두 T6 파일에서 다룬 FPGA/GPU/SGX 가상화 메커니즘을 서버리스 콜드스타트/멀티테넌시 문제에 적용한 다리 논문이다.
- **T3 (I/O 가상화) 위**: FastIOV(SR-IOV), NADINO(DPU RDMA), Poby(SmartNIC 이미지 프로비저닝)는 T3의 디바이스 가상화 메커니즘을 서버리스 시작 지연/데이터 평면에 적용한다.
- **T9 (자원관리) 위**: Mosaic(VIRT-MICRO24-17)는 서버리스 오버서브스크립션 환경에서 마이크로아키텍처 상태(L2/TLB/BTB)를 함수별로 태깅해 보존하는 CORE 메커니즘으로, T9에서 자세히 다루는 "오버서브스크립션 하의 QoS" 문제의 CPU 하드웨어 버전이다.

## 7. 2024 → 2026 변화

2024년 논문들은 주로 "기존 컨테이너/microVM 경계를 그대로 두고 캐싱·회수·상태전달을 최적화"하는 데 집중했다(RainbowCake, FaaSMem, Desiccant, RMMAP, Pronghorn, Sabre). 격리 경계 자체를 재설계하는 시도(SigmaOS, SURE, Faascale)도 2024년에 이미 등장했지만, 이때는 "unikernel/LibOS로 VM급 격리를 컨테이너 속도로"라는 단일 축이 중심이었다.

2025년에는 두 가지 확장이 뚜렷하다. 첫째, 격리 단위를 함수에서 워크플로우/프로그래밍모델 전체로 넓히는 근본적 재설계(AlloyStack, Hydra, uFork, Dandelion)가 집중적으로 등장한다 — 이는 "컨테이너를 더 빠르게"가 아니라 "컨테이너라는 단위 자체를 재정의"하는 방향이다. 둘째, 서버리스가 다루는 자원이 CPU/메모리를 넘어 GPU(Torpor, Dilu, Medusa, Aegaeon, FluidFaaS, PhoenixOS)로 명확히 확장된다 — LLM 서빙 수요가 이 전환의 명시적 동인으로 여러 논문에 등장한다.

2026년에는 이 GPU 확장이 가상화 메커니즘 수준으로 완성된다(gShare의 vfio-mdev passthrough, WorksetEnclave의 confidential GPU/enclave 콜드스타트)는 점, 그리고 DPU/RDMA가 서버리스 데이터 평면의 새로운 표준 격리 경계로 떠오른다는 점(NADINO)이 특징적이다. 또한 2026년 CONTEXT 논문(GreenMix, Green or Fast, Demystifying Serverless Costs)이 급증해, 메커니즘이 어느 정도 성숙한 뒤 비용/탄소 최적화라는 상위 계층 관심사로 무게중심이 이동하는 패턴이 보인다. 다만 이 CONTEXT 논문들 다수가 abstract 수준(P3)으로만 확인되어, "메커니즘 성숙 후 맥락 연구 급증"이라는 해석은 억지로 강한 트렌드로 단정하기보다 corpus 수집 패턴(2026년 venue가 상대적으로 더 많이 스캔됨)의 가능성도 배제할 수 없다.

## 8. 읽는 순서 제안

1. **VIRT-EUROSYS25-11 (Serverless Cold Starts and Where to Find Them, CONTEXT)** — 가상화 계층이 실제로 얼마나 콜드스타트에 책임이 있는지 감을 잡는다.
2. **VIRT-OSDI24-01 (Sabre)** → **VIRT-EUROSYS24-05 (Pronghorn)** — 전통적 VM/프로세스 스냅샷 최적화의 출발점.
3. **VIRT-SOSP24-04 (SigmaOS)** → **VIRT-SOCC24-04 (SURE)** — unikernel/경량 격리로 VM급 안전성과 컨테이너급 속도를 동시에 노리는 접근.
4. **VIRT-EUROSYS25-14 (AlloyStack)** → **VIRT-SOSP25-08 (Dandelion)** — 격리 단위를 함수에서 워크플로우/프로그래밍 모델로 넓히는 근본적 재설계.
5. **VIRT-SOSP25-13 (uFork)** — 단일 address space가 무엇을 희생하는지 정밀하게 확인.
6. **VIRT-OSDI26-11 (Spice/SHELF)** — VM 경계 vs 프로세스 경계 스냅샷 비용을 정확히 분리.
7. **VIRT-ATC25-09 (Torpor)** → **VIRT-SOSP25-06 (PhoenixOS)** → **VIRT-ASPLOS26-02 (gShare)** — GPU가 서버리스에 편입되는 순서(스왑 → 체크포인트 → passthrough).
8. **VIRT-EUROSYS26-13 (NADINO)** — DPU/RDMA로 확장되는 최신 데이터 평면 격리.

## 9. 증거 한계

다음은 abstract 수준 근거에 의존하며 세부 메커니즘(특히 isolation_mechanism/overhead_bottleneck)이 "UNKNOWN"으로 남아 있다: **VIRT-OSDI24-08 (ServerlessLLM, ABSTRACT/MEDIUM)**, **VIRT-SOCC24-10 (Faascale, DESIGN/MEDIUM — 논문 본문의 problem statement조차 아티팩트에서 재구성됨)**, **VIRT-MIDDLEWARE24-07 (HORSE, ABSTRACT_INTRO/MEDIUM)**, **VIRT-MIDDLEWARE24-08 (Funclets, ABSTRACT_INTRO/MEDIUM)**, **VIRT-ASPLOS25-09 (Medusa, ABSTRACT/MEDIUM)**, **VIRT-MIDDLEWARE25-05 (RUNE, ABSTRACT/MEDIUM)**, **VIRT-MIDDLEWARE25-06 (FaaSImage, ABSTRACT/MEDIUM)**, **VIRT-EUROSYS25-01 (FastIOV, ABSTRACT/MEDIUM — 수치는 공식 abstract에서만 확인)**, **VIRT-SOCC25-04 (Demeter 대신 오인하지 않도록 주의; T2/T9 소속)**, **VIRT-EUROSYS26-05 (Squeezy, ABSTRACT/MEDIUM)**, **VIRT-ASPLOS26-04 (WorksetEnclave, ABSTRACT/MEDIUM)**, **VIRT-EUROSYS26-15 (DROPS, ABSTRACT/MEDIUM)**. DIGEST_CONTEXT.md에 나열된 CONTEXT 논문 대부분은 P3이며 다수가 "why: UNKNOWN" 또는 "UNKNOWN pending access"로 표시되어 있어 — 이들은 애초에 이 문서의 CONTEXT 서술에서 제목/venue 수준의 신호로만 사용했고, 구체적 메커니즘 주장에는 사용하지 않았다. 반대로 P0/P1 핵심 논문(F3, Dandelion, SigmaOS, uFork, AlloyStack, Sabre, FastIOV, gShare, NADINO, PhoenixOS)은 모두 FULL/HIGH 또는 DESIGN_EVAL/HIGH 근거를 가진다.

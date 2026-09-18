# 마이그레이션/체크포인트/상태 (Migration, Checkpoint, State)

## 1. 이 계층이 푸는 문제

Physical Resource(한 호스트의 CPU/DRAM/디바이스 상태) → Logical Abstraction(다른 호스트로 옮겨지거나 디스크/원격 메모리에 직렬화될 수 있는 "가상화 상태의 스냅샷") → Workload(중단 없이 계속 실행되어야 하는 서비스, 빠르게 시작해야 하는 서버리스 함수, 장애 후 복구되어야 하는 학습 작업)로 이어지는 매핑을 다루는 계층이다. 앞의 T1(CPU)·T2(메모리) 계층이 "가상 자원을 어떻게 만들 것인가"를 다뤘다면, 이 계층은 "그렇게 만든 가상 자원의 상태를 어떻게 포착·이동·재구성할 것인가"를 다룬다. 핵심 질문은 세 가지다. (1) **무엇이 상태인가** — vCPU 레지스터, guest-physical 메모리, 디바이스 내부 상태(RDMA 큐페어, GPU 커널 DAG), 페이지 공유 관계까지 모두 "가상화 상태"에 포함된다. (2) **얼마나 멈춰야 하는가** — pre-copy(먼저 복사하고 나중에 멈춤)와 post-copy(먼저 멈추고 나중에 복사)라는 두 축이 downtime과 총 마이그레이션 시간을 다르게 트레이드오프한다. (3) **얼마나 자주, 어떤 대가로 이 작업을 감수할 수 있는가** — 마이그레이션은 공짜가 아니라 프로덕션에서 예산이 편성되는 희소 자원이다(VIRT-OSDI26-13, DVLA는 하루 평균 810회의 VM 마이그레이션을 "예산"으로 다룬다). T4 코퍼스는 VM 라이브 마이그레이션뿐 아니라 컨테이너 마이그레이션(CRIU 기반), 서버리스 콜드스타트를 위한 스냅샷/복원, GPU 체크포인트/복원까지 "상태를 포착하고 재구성한다"는 동일한 문제가 격리 경계(하이퍼바이저/네임스페이스/프로세스/디바이스)마다 다른 난이도로 반복됨을 보여준다.

## 2. Mechanism design space

**Pre-copy vs post-copy 라이브 마이그레이션**: 고전적 pre-copy(Clark et al., NSDI 2005)는 VM이 계속 실행되는 동안 dirty page를 반복 전송하다가 짧은 정지-후-동기화로 마무리한다. Post-copy는 먼저 목적지에서 재개시키고 필요한 페이지를 그때그때 당겨온다. VIRT-OSDI26-02(M3U)는 고사양 VM(≥64 vCPU, ≥256GB)의 post-copy가 실제로는 네트워크 대역폭이 아니라 커널 MMU 락 경합(dirty-page 추적, HPT/EPT/IOPT 정합성 유지)에 의해 병목이 걸린다는 것을 보이고, 락-프리 1GB 영역 분할과 데이터 복사/페이지테이블 갱신의 분리로 이를 해결한다.

**공유 관계를 보존하는 마이그레이션**: 표준 라이브 마이그레이션은 KSM류로 공유되던 페이지를 목적지에서 각 VM별로 재물질화해 "메모리 풋프린트 팽창"을 일으킨다. VIRT-CCGRID24-02(SLM)는 페이지를 Unique/Duplicate/Dirty로 분류해 중복 페이지는 식별자만 보내고 목적지에서 mmap(MAP_PRIVATE)으로 동일 물리 페이지에 재매핑한다.

**하드웨어 이종성 대응**: VIRT-EUROSYS26-04(MigCheck)는 "같은 ISA, 다른 기능"의 호스트 간 마이그레이션 성공 여부를 실제 마이그레이션 없이 시뮬레이션으로 예측하며, VIRT-CCGRID24-05는 워크로드가 실제로 사용하는 CPU feature만 분석해 과도하게 보수적인 호환성 체크를 완화한다.

**Confidential VM 유지보수의 신뢰 경계 문제**: 일반 VM에서는 하이퍼바이저가 마이그레이션을 자유롭게 수행하지만, confidential VM에서는 하이퍼바이저가 암호화된 guest 메모리를 볼 수 없다. VIRT-ATC24-22(CPC)는 guest-trusted "maintenance vCPU"를 host가 스케줄링해 ballooning/snapshot/migration을 수행하게 하고, AMD SEV-SNP에서는 VMPL을, ARM CCA에서는 Confidential Page-Table Isolation을 사용해 두 플랫폼 모두에서 동작한다.

**디바이스 상태 마이그레이션의 난제**: 소프트웨어 에뮬레이션 디바이스는 하이퍼바이저가 상태를 직접 알지만, passthrough 디바이스(RDMA NIC, GPU)는 상태가 하드웨어 내부에 있어 하이퍼바이저가 볼 수 없다. VIRT-SOSP25-01(RDMA 디바이스 라이브 마이그레이션)은 이 문제를 "디바이스 보조" 방식으로 접근한다고만 확인되며 구체적 메커니즘은 확인되지 않는다. VIRT-SOSP25-06(PhoenixOS)은 GPU에 대해 이 문제를 커널 DAG(노드=커널, 엣지=버퍼 의존성)로 소프트웨어 dirty-bit/copy-on-write를 재구성해 해결한다.

**컨테이너/프로세스 경계 체크포인트**: VM 경계(플랫 guest-physical 주소공간)와 달리 컨테이너의 OS 레벨 상태(네임스페이스, 프로세스 트리, cgroup, 파일디스크립터)는 상호의존적이라 순진한 일괄 복원(one-shot restore)이 매우 느리다. VIRT-SOCC24-08(PCLive)은 이 상태를 의존성 순서대로(전역 상태 먼저, 프로세스별 상태는 반복적으로) 스트리밍 중에 복원한다. VIRT-CCGRID26-01(TelePod)은 CRIU에 pre-copy 반복 전송과 "전송-복원 중첩"을 추가해 VM 라이브 마이그레이션과 유사한 다운타임을 노린다.

**서버리스 콜드스타트를 위한 스냅샷/복원**: 여러 지점에서 서로 다른 트레이드오프를 취한다 — VIRT-OSDI24-01(Sabre)은 하드웨어 압축기로 스냅샷 자체를 작게 만들고, VIRT-ATC24-19(PASS)는 PMEM에 직접 인덱스를 구축해 파일시스템 경유를 없애며, VIRT-EUROSYS24-05(Pronghorn)는 어느 시점의 JIT 워밍업 상태를 스냅샷할지를 확률적으로 선택하고, VIRT-OSDI26-11(Spice/SHELF)은 CRIU의 수천 개 syscall 재현이나 VM 경계의 "지연된 하우스키핑 폭풍" 모두를 피해 커널 프리미티브(spliceVMA)로 스냅샷 파일을 지연 스플라이스한다.

**GPU 체크포인트/복원**: GPU는 페이징이 없어 CPU식 dirty-bit/COW가 존재하지 않는다. VIRT-SOSP25-06(PhoenixOS)의 소프트 dirty-bit·소프트 COW, VIRT-SOCC24-01(gCROP)의 CPU/GPU 상태 병렬·온디맨드 복원, VIRT-ASPLOS25-09(Medusa)의 CUDA 그래프/KV-cache 상태 외부화가 이 문제를 서로 다른 각도에서 공격한다.

**격리 경계를 우회하는 빠른 리셋**: 매 요청마다 완전한 체크포인트/복원을 하는 대신, VIRT-ATC24-14(REWIND)는 "buddy page table"(4KB 리프를 8KB로 확장해 상위 절반에 스냅샷 이전 상태 기록)로 컨테이너를 빠르게 초기 상태로 되돌리고, VIRT-SOSP25-13(µFork)은 CHERI capability로 단일 주소공간 안에서 POSIX fork를 구현한다.

## 3. 핵심 논문 (P0/P1)

**VIRT-EUROSYS26-04 | MigCheck (EuroSys 2026, CORE P0)** — "같은 ISA, 다른 기능(semi-heterogeneous)" 프로세서 간 라이브 마이그레이션 실행 가능성에 대한 최초의 체계적 분석과, 실제 마이그레이션 없이 성공 여부를 예측하는 시뮬레이션 도구 MigCheck를 제시한다. 하드웨어 증설/제거, 하이퍼바이저 업데이트, 플랫폼 구성 변경 시나리오에서 검증되었다. 클라우드 플릿이 시간이 지나며 결코 완전히 동질적이지 않다는 실무적 전제에서 출발해, 모든 라이브 마이그레이션 CORE 논문이 당연시하는 "이 VM이 저 호스트로 이동 가능한가"라는 질문에 정면으로 답하는, 이 브랜치의 우선 추천 논문이다.

**VIRT-ATC24-22 | CPC (ATC 2024, CORE P0)** — confidential VM은 정기적 유지보수(ballooning, 스냅샷, 로깅, 라이브 마이그레이션)가 필요하지만, 오늘날 이는 확장성이 나쁜 firmware-trusted 컴포넌트(AMD Secure Processor)에 의존하거나(ARM CCA는 마이그레이션 솔루션이 없고 Intel TDX는 스냅샷 구현이 없음) 아예 지원되지 않는다. CPC는 각 CVM의 vCPU를 guest vCPU(gvCPU)와 host-invocable vCPU(hvCPU)로 나누고, hvCPU는 host가 활성화할 때만 guest 자신이 작성·신뢰하는 유지보수 모듈("Confidential Procedure Call")을 실행한다. AMD SEV-SNP에서는 VMPL로, ARM CCA에서는 새로 설계한 Confidential Page-Table Isolation(242줄의 RMM 확장)으로 동일한 격리를 구현한다. 메모리 암호화 추출은 AMD Secure Processor 대비 최대 340.61배(AESNI 버전), 라이브 마이그레이션은 최대 55.90배(Vanilla/AMD-SP 대비 2,025.67초 → 36.24초) 빨라진다. 다만 GCM 암호화 자체가 잔여 병목으로 남아 가장 빠른 CPC 변형도 비암호화 VM 마이그레이션보다는 16배 느리다.

**VIRT-OSDI26-02 | M3U (OSDI 2026, CORE P1)** — 고사양(≥64 vCPU, ≥256GB) VM의 post-copy 라이브 마이그레이션이 네트워크 대역폭이 아니라 커널 MMU 락 경합에 의해 병목이 걸린다는 것을 정밀 측정으로 보인다(128GB 워킹셋이 약 3200만 회의 unmap 연산을 유발, 베이스라인은 가용 대역폭의 9.2%만 사용). HPT map/unmap을 가벼운 Present-bit 플래깅으로 대체하고 락-프리 1GB 영역으로 물리 메모리를 분할하며, 데이터 복사와 페이지테이블 정합성 유지를 분리된 스레드로 나눈다(6-8개 병렬 스트림). VirtIO 큐 상태를 재개 전에 미리 설치해 디스크립터 IOPF를 없앤다. 다운타임 최대 47.0% 감소, post-copy 완료 시간 85.8-89.6% 단축, IOPF 98.5% 감소(dual-socket Intel Xeon 8369B, 512GB DDR4, 200Gbps DPU). 대가는 CPU 상태 마이그레이션 자체는 개선하지 않는다는 점과 잔여 1.5%의 IOPF는 guest 투명성을 깨지 않고는 제거할 수 없다는 점.

**VIRT-SOSP25-06 | PhoenixOS (SOSP 2025, CORE P1)** — GPU는 OS 페이징을 우회하므로 CPU 체크포인트/복원이 의존하는 dirty bit와 COW가 존재하지 않아, 기존에는 수백 밀리초의 stop-the-world 방식이 필요했다. PhoenixOS는 CUDA driver API를 인터포즈해 커널 실행 DAG(노드=커널/버퍼, 엣지=읽기/쓰기 의존성)를 유지하고, 커널 launch argument에서 버퍼 접근 집합을 추측한 뒤 오프라인 PTX 바이너리 계측으로 이를 검증해, 소프트 COW·소프트 dirty bit·위상순서 온디맨드 복원을 구현한다. Stop time 약 1ms(stop-the-world 베이스라인의 726ms 대비), Llama-2-13B 다운타임 7.9초→0.4초. 대가는 불투명한 커널(전체의 20% 미만)에 대한 2-21% 계측 오버헤드와 speculative 접근 추측이 실패할 때의 폴백 경로다.

**VIRT-CCGRID24-02 | SLM (CCGrid 2024, CORE P1)** — co-located VM들이 KSM식으로 공유하던 페이지가, 표준 라이브 마이그레이션에서는 각 VM에 대해 개별적으로 재전송·재물질화되어 목적지에서 메모리 풋프린트가 "팽창"하는 문제를 다룬다. 페이지를 Unique/Duplicate(다른 VM 마이그레이션으로 이미 전송됨)/Dirty로 분류하고, 목적지에서 mmap(MAP_PRIVATE)으로 동일 물리 페이지에 재매핑해 원래의 COW 공유 관계를 재구성한다. KVM/QEMU 위에 pre-copy와 post-copy 양쪽에 구현. 총 마이그레이션 시간 최대 59%(pre-copy)/57%(post-copy) 감소, 네트워크 트래픽 최대 62% 감소(Intel Xeon E5-2620 v2, 128GB DRAM, 3대 KVM/QEMU 테스트베드). "상태"라는 개념이 단순히 페이지 내용뿐 아니라 페이지 간 공유 관계까지 포함해야 한다는 것을 보여주는 구체적 사례다.

**VIRT-CCGRID26-01 | TelePod (CCGrid 2026, CORE P1)** — 활성 상태를 가진 컨테이너(데이터베이스, 멀티플레이어 게임 서버)는 상태 없는 컨테이너처럼 파괴 후 재시작할 수 없다. TelePod은 CRIU에 (1) pre-copy 반복 메모리 전송(소스가 계속 실행되며 dirty page를 반복 재전송)과 (2) "전송-복원 중첩"(목적지가 소스의 나머지 dirty page 전송이 끝나기 전에 이미 복원을 시작)을 추가한다. 하이퍼바이저 기반 VM 라이브 마이그레이션과 대등한 다운타임을 주장하며, 일반 VM과 confidential VM 모두에 대해 이를 명시적으로 주장하는 T4-T5 교량 논문이다.

**VIRT-SOCC24-08 | PCLive (SoCC 2024, CORE P1)** — 표준 CRIU 기반 컨테이너 마이그레이션의 "일괄 복원(one-shot restore)"은 전체 메모리 이미지가 도착한 후에야 목적지가 상태를 재구성하기 시작한다. 메모리 상태 처리가 복원 시간의 99.5%를 차지한다는 측정에 기반해, 전역 상태(네임스페이스, 프로세스 트리, cgroup, 파일)를 먼저 재구성하고 프로세스별 상태(메모리, 파일디스크립터)는 pre-copy 라운드마다 반복적으로 재구성한다. 복원 시간 읽기 집약 워크로드 최대 38배 단축, 서비스 다운타임 읽기 집약 2.7배 단축(Redis+YCSB, 1Gbps). 대가는 파이프라인 유지 동안의 추가 CPU/메모리 오버헤드(쓰기 집약 케이스 +4% CPU, +23% 메모리)와 상호의존적 OS 레벨 상태를 올바른 순서로 재구성해야 하는 공학적 복잡도다.

**VIRT-OSDI24-01 | Sabre (OSDI 2024, CORE P1)** — Firecracker microVM 스냅샷 복원이 I/O·CPU에 종속되는 문제를, 소프트웨어 압축이 너무 비싸 쓸 수 없었던 지점에서 데이터센터 CPU 내장 근접메모리 가속기로 (압축/해제를) 오프로드해 해결한다. 스냅샷 압축률 최대 4.5배, 메모리 복원 속도 최대 55% 개선(프로덕션 Firecracker microVM, 다양한 서버리스 애플리케이션). 대가는 특정 근접메모리 가속기 하드웨어에 대한 의존성이다.

**VIRT-ATC24-19 | PASS (ATC 2024, CORE P1)** — 서버리스 콜드스타트 은닉의 표준 기법인 VM 스냅샷팅이 SSD 기반 파일시스템이나 부분 워킹셋 프리페치(FaaSnap)조차 반복적 page fault와 다중 user/kernel 전환을 겪는 문제를, 전체 guest-physical 메모리 이미지를 PMEM에 직접(파일시스템 경유 없이) 스냅샷하고 페이지 정렬 주소 인덱스를 KVM에 사전 등록해 해결한다. SnapStart 실행시간 최대 72% 감소, 최대 동시성 2배(32→64 microVM), 메모리 압박(64GB→2GB) 하에서 FaaSnap 대비 최대 30배 우위(FaaSnap은 2GB 미만에서 아예 실패). 대가는 PMEM 하드웨어 의존성과 현재 microVM에만 범위가 한정된다는 점(컨테이너/유니커널은 향후 과제).

**VIRT-SOCC24-01 | gCROP (SoCC 2024, CORE P1)** — CRIU식 전체 프로세스 체크포인트/복원을 GPU 가속 애플리케이션에 재사용하면, GPU 드라이버/데이터 복구가 CPU 메모리·페이지테이블 복원 뒤에 순차적으로 막히는 "복원 장벽(restorer barrier)" 문제가 생긴다. gCROP은 프레임워크 초기화 직후와 앱 로드 직후 두 지점에서 체크포인트해 프레임워크를 공유하는 앱들 간 콘텐츠 재사용을 극대화하고, 별도의 Restore Server 프로세스가 dma-buf 파일 디스크립터를 임포트해 별도 주소공간에서 GPU 데이터를 비동기 복원하는 동안 메인 프로세스는 mmap 기반 온디맨드 페이징으로 CPU 상태를 복원한다(GPU 버퍼 객체에는 커스텀 GPU page-fault 핸들러 gmmap 사용). CRIU 대비 시작 지연 5.5-23.5배 개선, MobileNet 시작 지연 44-73ms. 대가는 템플릿을 공유하는 인스턴스 간 ASLR이 깨진다는 것(단일 테넌트 내 재사용으로 완화).

**VIRT-ATC24-14 | REWIND (ATC 2024, CORE P1)** — 서버리스 웜 컨테이너 재사용은 빠르지만 상태가 요청 간 지속되어 데이터 유출이나 루트킷 지속성 위험이 있다. 매 요청마다 전체 체크포인트/복원(Groundhog)이나 fork를 하는 대신, 모든 4KB 리프를 8KB로 확장한 "buddy page table"(상위 절반에 스냅샷 이전 상태 기록)로 스냅샷(container 시작 시 COW 적용)과 되감기(rewind, 새/수정 매핑 언맵 후 buddy PTE에서 익명 페이지 복원)를 구현한다. 피크 RSS 오버헤드 단 11%, 스냅샷 생성 최대 0.3ms(Groundhog의 16-59ms 대비), 되감기 시간은 Groundhog의 10.7%. 대가는 두 배로 늘어난 페이지테이블 크기와 파일 기반 페이지 재사용을 프라이버시/부채널 안전을 위해 비활성화해야 한다는 것.

**VIRT-SOSP25-01 | RDMA 디바이스 라이브 마이그레이션 (SOSP 2025, CORE P1, 근거 제한)** — device passthrough(HPC/AI급 성능을 위해 RDMA에 널리 쓰임)는 하드웨어 상태를 guest에 직접 노출해 순수 소프트웨어 라이브 마이그레이션이 전제하는 guest-OS/하드웨어 분리를 깨뜨린다는 문제를 "device-assisted"(RDMA NIC 자체가 마이그레이션에 참여) 방식으로 접근한다고만 확인된다. 구체적 상태 추출 프로토콜, 큐페어/메모리 등록 재구성 방식은 abstract 수준에서 확인되지 않았다. 완전히 읽힌다면 device passthrough의 가장 어려운 미해결 문제 — 하이퍼바이저가 볼 수도 재구성할 수도 없는 하드웨어 상주 디바이스 상태의 마이그레이션 — 에 대한 이 분야의 기준점이 될 가능성이 높다.

**VIRT-SOCC24-07 | 지속적 ballooning (SoCC 2024, CORE P1)** — ballooning은 마이그레이션 속도를 높이고 통합도를 개선하지만 guest의 스와핑이나 OOM을 유발할 위험이 있어, 정확히 그것이 가장 필요한 두 순간(대규모 메모리 스파이크, 진행 중인 라이브 마이그레이션)에는 꺼둬야 했다. 사용자공간 "지속적 ballooning" 프로그램이 balloon driver의 인플레이션/디플레이션을 실시간 조율해 이 두 고위험 순간에도 안전하게 동작하도록 만든다. 최대 8% 오버헤드로 최소 52% 빠른 마이그레이션, 거의 600GB급 VM까지 검증, 무한 순차 마이그레이션에도 스왑/OOM 없음. 월 수만 회 VM을 마이그레이션하는 실제 클라우드 고객 데이터를 제공하는 흔치 않은 프로덕션 사례.

**VIRT-SOCC25-01 | Hydra (SoCC 2025, CORE P1)** — 서버리스 플랫폼이 매 호출마다 전체 가상화 스택(컨테이너/VM + 언어별 런타임)을 유지하는 비용을, GraalVM Native Image로 사전 컴파일한 공유 네이티브 라이브러리와 Truffle 기반 공유 런타임 위의 "메모리 isolate"(전체 프로세스가 아닌 경량 샌드박스)로 낮춘다. Seccomp-bpf와 함수별 분리된 1TB 가상주소 예약을 이용한 커스텀 syscall/메모리 추적 스냅샷 메커니즘이 CRIU식 전체 프로세스 체크포인트보다 훨씬 저렴하게 isolate를 체크포인트/복원한다. 함수 밀도 4.47배, 메모리 사용량 2.1배 감소(OpenWhisk 위 SEBS/Photons 벤치마크). 대가는 격리 세분성(네이티브/비관리 코드는 프로세스 레벨로 폴백)과 미성숙한 다중언어(Python) 성능이다.

## 4. Supporting 논문 (P2/P3)

- **VIRT-EUROSYS24-05 (Pronghorn)** — JIT 워밍업 상태(수백~수천 회 호출이 필요)를 서버리스 인스턴스가 축출될 때 버리지 않고, 요청 시점 확률분포로 체크포인트 타이밍을 샘플링해 스냅샷 풀을 유지. 최대 58% 지연 개선. Sabre와 함께 서버리스 스냅샷 풀의 비용/이득 곡선을 이해하는 데 좋은 출발점.
- **VIRT-HPDC24-02 (DataStates-LLM)** — LLM 학습 체크포인트를 동기 방식(훈련 블로킹) 대신 지연·비동기 GPU→호스트 복사로 겹쳐 처리. 최대 4.2배 처리량, 최대 48배 빠른 체크포인트(30B 파라미터, 고차 데이터병렬). 하이퍼바이저/컨테이너 체크포인트 설계와 직접 비교할 수 있는 ML 프레임워크 계층의 유사 문제.
- **VIRT-MIDDLEWARE24-07 (HORSE)** — 휴면 microVM/함수 샌드박스의 재개 지연을 PPSM 알고리즘으로 최대 142.84배 단축한다고 발표(WIDE lab 발표 수준, 근거 제한).
- **VIRT-ASPLOS25-09 (Medusa)** — 서버리스 LLM 추론의 콜드스타트를 KV-cache 예약과 CUDA 그래프 구성이라는 GPU 특화 초기화 단계까지 재료화(materialize)해 단축. GPU 상태 캡처가 얼마나 드라이버/배치크기 구성에 취약한지 보여주는 사례.
- **VIRT-OSDI25-05 (AFaaS / Fork in the Road)** — 프로덕션 서버리스 콜드스타트 지연의 실제 원인을 분해해, 사전 최적화된 secure-container조차 컨트롤패스 RPC/shim 오버헤드, 동시성 하 자원 경합, 사용자코드 초기화가 병목임을 보인다. VM-fork(Catalyzer 스타일 EPT COW) 기반 계층적 "seed" 트리로 Catalyzer 대비 전체 1.80-8.14배 개선. 콜드스타트 지연 분해가 매우 상세하고 정량적이어서 SUPPORT임에도 필독 가치가 크다.
- **VIRT-OSDI26-11 (Spice/SHELF)** — 디스크 상주 프로세스 이미지를 페이지 순서 재배열 + 구간트리 인덱스로 저장하고, spliceVMA라는 커널 프리미티브로 하나의 VMA가 스냅샷 파일/파일백드 매핑/제로필을 페이지 단위로 지연 결합하게 한다. CRIU 대비 7.5배, VM 경계 시스템(REAP/FaaSnap) 대비 9.5배 빠른 지연. 프로세스 경계 vs VM 경계 각각의 비용 원천(syscall 재현 volume vs guest 가상시계 점프 후 "지연된 하우스키핑 폭풍")을 정밀 분해해, CORE 논문의 오버헤드가 근본적인지 경계 특유의 것인지 가늠하는 좋은 참고점.
- **VIRT-ASPLOS25-03 (Tally)** — GPU 커널 재작성(PTX 레벨 블록 슬라이싱/영속 스레드블록)으로 소프트웨어 선점 지점을 만들어, 하드웨어 선점 없이 우선순위 기반 GPU 시분할을 구현. 왜 GPU가 가상화하기 어려운지 — 선점 지점을 만들려면 커널 자체를 재작성해야 한다는 것 — 를 정량적으로 보여준다.
- **VIRT-SOSP25-07 (Aegaeon)** — 토큰 단위 자동스케일링으로 디코드 스텝 사이에 모델을 교체해, 요청 단위 자동스케일링보다 낮은 동시 활성 모델 수를 유지. 프로덕션(Alibaba Cloud Model Studio)에서 GPU 1,192대→213대(82% 감소). 상태(모델 가중치·KV cache) 이동이 컴퓨트보다 진짜 병목임을 정량화.
- **VIRT-EUROSYS25-02 (VMR2L)**, **VIRT-OSDI26-13 (DVLA)** — 각각 강화학습 기반 VM 재배치(defragmentation을 위해 마이그레이션을 어떻게 예산 내에서 쓰는가)와 VM 수명 인식 배치(장기 VM이 "정체 부채"를 만드는 문제)를 다룬다. DVLA는 프로덕션(Alibaba Cloud, 7개월)에서 하루 평균 810회 마이그레이션을 실제 운영 제약으로 관측한다.
- **VIRT-MIDDLEWARE24-08 (Funclets)**, **VIRT-OSDI24-08 (ServerlessLLM)** — 각각 I/O 집약적 함수 코드를 스토리지 노드로 "마이그레이션"하는 근접 데이터 처리와, LLM 체크포인트의 다단계 로딩/라이브 마이그레이션. 상태 이동 개념이 VM 메모리가 아닌 코드/모델 가중치에도 적용되는 사례.
- **VIRT-ASPLOS25-12 (Coach)**, **VIRT-SOCC25-05 (Funky)** — 각각 라이브 마이그레이션을 오버커밋의 최종 탈출구로 사용하는 사례(T2 파일 참고), FPGA 체크포인트/재개를 CPU 가상화 패턴으로 구현한 사례(T1 파일 참고). 두 편 모두 이 파일의 핵심 주제와 접점이 있지만 본진은 각각 T2/T1·T6에 있다.

## 5. Trade-off 구조

- **Pre-copy vs post-copy**: pre-copy는 실패 시 원본이 살아있어 안전하지만 dirty rate가 높으면 수렴하지 않을 수 있고, post-copy는 총 시간이 짧지만 목적지 실행 중 페이지 fault로 인한 지연(IOPF)이라는 새로운 비용을 만든다(M3U가 이 비용의 정체를 커널 락 경합으로 규명).
- **투명성 vs 속도**: guest/컨테이너를 전혀 건드리지 않는 표준 CRIU/QEMU 마이그레이션은 느리고, guest 협조를 받는 설계(HyperAlloc류, Squeezy, PASS의 PMEM 인덱스)는 빠르지만 배포 가능성이 좁아진다.
- **격리 경계가 깊을수록 상태 포착이 비싸진다**: VM(플랫 guest-physical 주소공간) < 컨테이너(상호의존적 네임스페이스/cgroup/프로세스 트리, PCLive가 99.5%를 메모리 상태 처리로 규명) < GPU(페이징 자체가 없어 dirty-bit/COW를 소프트웨어로 재발명해야 함, PhoenixOS/gCROP) < 신뢰 경계 안(암호화되어 하이퍼바이저가 볼 수 없는 confidential VM, CPC) 순으로 난이도가 증가한다.
- **마이그레이션의 예산화**: 마이그레이션은 무료 자원이 아니다. DVLA는 이를 "순이익 요구조건이 있는 예산"으로, Coach는 "오버커밋 리스크의 탈출구"로, CPC는 "confidential VM에서는 아예 없거나 극도로 느린 연산"으로 각각 다르게 취급한다.
- **재료화(materialization)의 브리틀함**: 콜드스타트를 줄이기 위해 상태를 미리 저장해두는 모든 접근(Medusa의 CUDA 그래프, Sabre의 압축 스냅샷, PASS의 PMEM 인덱스)은 저장된 상태가 특정 드라이버/런타임/배치크기 버전에 결합되어, 그 버전이 바뀌면 재료화된 상태가 무효화된다는 공통 취약점을 갖는다.

## 6. 인접 계층과의 관계

- **아래(T1 CPU 가상화, T2 메모리 가상화)**: 이 계층이 옮기는 "상태"의 대부분은 T1(vCPU 레지스터, VMCS)과 T2(guest-physical 메모리, EPT)가 정의한 바로 그 상태다. CPC(VIRT-ATC24-22)는 T1의 vCPU 추상화를 유지보수 채널로 재활용하고, M3U(VIRT-OSDI26-02)는 T2의 dirty-page 추적 메커니즘의 커널 구현을 재설계한다. JANUS(T1, VIRT-OSDI26-01)의 PML dirty-tracking 결과(Kata-KVM 175.5% 오버헤드 vs Kata-JANUS 거의 무시할 수준)는 이 계층에서 dirty-page 추적 자체가 얼마나 비쌀 수 있는지 보여주는 선행 지표다.
- **T5 컨테이너/경량 격리**: PCLive, TelePod, REWIND, µFork는 모두 컨테이너/프로세스 경계에서의 상태 포착·재구성을 다루며, 이 계층과 T5 사이의 직접적 다리다.
- **T6 가속기 가상화**: PhoenixOS, gCROP, Medusa, Tally는 GPU가 페이징/선점 하드웨어를 갖지 않는다는 사실이 체크포인트/마이그레이션 설계에 어떤 제약을 가하는지 보여준다.
- **T7 confidential computing**: CPC는 신뢰 경계 안에서 마이그레이션이 어떻게 재구성되어야 하는지에 대한 이 코퍼스의 가장 완결된 답이다.
- **T8 서버리스**: Sabre, PASS, Pronghorn, Spice, AFaaS, Hydra는 모두 "콜드스타트 = 상태를 얼마나 빨리 재구성할 수 있는가"라는 동일한 문제를 서버리스 맥락에서 공유한다.
- **T9 자원관리**: VMR2L, DVLA, Coach는 마이그레이션을 배치·오버커밋 정책의 실행 수단으로 소비하는 상위 계층이다.

## 7. 2024 → 2026 변화

작은 표본에 대한 조심스러운 관찰이다. 2024년 논문들은 주로 "특정 경계(컨테이너, confidential VM, GPU)에서 체크포인트/마이그레이션을 최초로 실용적으로 만드는" 데 집중했다(PCLive, CPC, gCROP, REWIND, PASS, Sabre). 2025년에는 GPU 체크포인트가 더 정교해지고(PhoenixOS의 speculative DAG) 콜드스타트 지연의 실제 원인 분해가 깊어졌다(AFaaS). 2026년 표본(MigCheck, M3U, TelePod, Spice)은 "이미 존재하는 메커니즘이 왜, 정확히 어디서 병목이 걸리는가"를 정밀 계측하는 방향(M3U의 커널 락 경합 규명, MigCheck의 사전 실행가능성 예측)으로 이동하는 것으로 보인다. 다만 T4의 2026년 주 논문은 OSDI/EuroSys/CCGrid 소수 편에 국한되어 있어, 이를 확정적인 산업 트렌드로 일반화하는 것은 근거가 부족하다.

## 8. 읽는 순서 제안

1. **VIRT-CCGRID24-02**(SLM, 마이그레이션 중 상태란 페이지 내용뿐 아니라 공유 관계임을 확인) → 2. **VIRT-SOCC24-08**(PCLive, 컨테이너 상태의 상호의존성) → 3. **VIRT-OSDI26-02**(M3U, post-copy의 진짜 병목) → 4. **VIRT-EUROSYS26-04**(MigCheck, 마이그레이션 가능성 예측이라는 실무적 질문) → 5. **VIRT-ATC24-22**(CPC, 신뢰 경계 안에서의 유지보수) → 6. GPU 갈래로 **VIRT-SOCC24-01**(gCROP) → **VIRT-SOSP25-06**(PhoenixOS) → 7. 서버리스 콜드스타트 갈래로 **VIRT-OSDI24-01**(Sabre) → **VIRT-ATC24-19**(PASS) → **VIRT-OSDI26-11**(Spice) → **VIRT-OSDI25-05**(AFaaS, 콜드스타트 지연의 전체 그림).

## 9. 증거 한계

다음 항목은 abstract 또는 abstract_intro 수준 근거에 머물러 있다: VIRT-CCGRID24-03(다중 VM SLM 확장, 메커니즘 대부분 미확인), VIRT-CCGRID24-05(정량치는 확인되나 abstract 수준 서술 다수), VIRT-MIDDLEWARE24-07(HORSE, WIDE lab 발표 수준), VIRT-ASPLOS25-09(Medusa), VIRT-SOSP25-01(RDMA 디바이스 라이브 마이그레이션 — 메커니즘·격리·상태 이전 방식이 모두 "UNKNOWN"으로 기록되어, 문제 설정 외의 어떤 구체적 주장도 이 논문에 귀속시켜서는 안 된다), VIRT-CCGRID26-01(TelePod), VIRT-EUROSYS26-04(MigCheck — 문제의식과 도구의 존재는 확실하나 구체 알고리즘·수치는 미확인), VIRT-MIDDLEWARE24-08(Funclets), VIRT-OSDI24-08(ServerlessLLM, 10-200배라는 수치는 저자 abstract 자체 인용이며 독립적으로 재확인되지 않음), VIRT-SOCC24-07(지속적 ballooning, 정성적 서술은 상세하나 일부 정량치는 abstract 인용). 이들을 인용할 때는 메커니즘의 방향성만 신뢰하고 세부 수치나 알고리즘 디테일은 "확인 안 됨"으로 표시해야 한다.

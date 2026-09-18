# 컨테이너/경량 격리 (Container / Lightweight Isolation)

## 1. 이 계층이 푸는 문제

이 topic은 Physical Resource(CPU core, DRAM)를 Logical Abstraction(process, container, unikernel, sandbox, in-process compartment)으로 나누어 Workload(서버리스 함수, 마이크로서비스, 멀티테넌트 호스팅, 커널 확장)에 배분하는 문제를 다루되, T1(전면적 하드웨어 VM)보다 훨씬 가벼운 격리 단위를 만드는 것이 목표다. 이 corpus가 T5를 45편의 primary 논문으로 채운 이유는, "VM은 안전하지만 무겁고, 프로세스는 가볍지만 커널 하나를 공유한다"는 이분법 사이에 실제로는 최소 8-9개의 서로 다른 메커니즘 계열이 존재하기 때문이다. 이 문서는 venue별이 아니라 **격리 메커니즘 계열**별로 조직해, 학습자가 "무엇으로 경계를 긋는가"라는 설계 공간을 보도록 한다.

## 2. Mechanism design space — isolation strength / overhead / compatibility 삼각형

T5의 corpus는 격리 경계를 아래 계열들로 나눠 보여주며, 각 계열은 "격리 강도", "오버헤드", "호환성(레거시 코드 재사용 가능성)"이라는 세 축 위에서 서로 다른 지점을 차지한다.

**(a) namespace/cgroup (전통 컨테이너).** 하나의 커널을 공유하며 namespace로 뷰를, cgroup으로 자원을 나눈다. 호환성은 최고지만 커널 하나의 메모리 안전성 버그가 모든 tenant의 격리를 깬다. VIRT-SOSP24-04(SigmaOS)는 이 계열을 처음부터 다시 설계해 network-namespace/overlay-filesystem 생성을 sigma-EP 토큰과 클라우드 네이티브 API로 대체하고, syscall 표면을 67개(Docker 352개 대비)로 줄여 콜드스타트를 7.7ms(AWS Lambda 1,290ms, Docker 2,671ms)까지 낮춘다. VIRT-OSDI26-09(vBOIDs)는 cgroup CPU quota가 "시간은 제한하지만 동시 점유 코어 수는 제한하지 않는다"는 결함(2.0-CPU quota 컨테이너가 20ms 동안 100개 코어에 legally burst 가능)을 BOID라는 vCPU 유사 스케줄링 단위로 고쳐, Firecracker microVM에 필적하는 캐시 지역성을 하이퍼바이저 없이 얻는다.

**(b) 마이크로커널/split-kernel.** 격리를 커널 내부의 privilege 경계 또는 완전히 별도의 커널 인스턴스로 옮긴다. VIRT-OSDI24-03(HongMeng)은 IC0/IC1/IC2 세 단계의 격리 강도를 서비스별로 선택하게 해 Linux 호환 API를 유지하면서 앱 시작 17%, context switch 32% 개선을 얻는다. VIRT-OSDI25-03(MettEagle)은 L4Re 마이크로커널의 zero-ambient-authority capability 모델로 seccomp/cgroup/namespace가 낳은 CVE 33건 중 seccomp-bpf 8건 전부·namespace 4/22·cgroup 0/3을 원천적으로 피하지만, TCB는 89,271 SLOC(Linux+containerd+runc는 2,699,812 SLOC)로 30배 작은 대신 파일시스템 stat()이 약 10배 느리다. VIRT-ATC25-01(LiteShield)은 하이퍼바이저 없이 유저스페이스 uKernel 서비스 프로세스로 syscall을 나눠(delegable 142개는 shared-memory IPC, non-delegable 28개는 ptrace) guest-host 인터페이스를 300+에서 22개로 줄인다. VIRT-EUROSYS26-06(SKernel)은 Kata류 monolithic guest kernel과 gVisor류 host-kernel 의존 사이에서 컨테이너별 split kernel slice로 elastic 확장과 격리를 동시에 노린다(ABSTRACT_INTRO 수준 근거).

**(c) unikernel.** 컴파일 타임에 애플리케이션과 커널을 하나의 주소공간으로 특수화해 이미지와 부팅을 최소화한다. VIRT-SOCC24-04(SURE)는 Unikraft+QEMU 기반 함수당 unikernel로 컨테이너급 속도와 VM급 격리를 동시에 노린다(Knative 대비 최대 79배, 저자 자체 수치). VIRT-ASPLOS24-11(Loupe)는 "unikernel이 실제로 얼마나 많은 Linux 기능을 구현해야 하는가"를 동적 분석으로 답해, OSv가 실제 구현한 92개 syscall 중 37개만 있어도 62개 앱이 돌아간다는 것을 보인다 — unikernel 계열의 근본 비용(호환성 계층 구축)을 정량화한다.

**(d) MPK/in-process domain.** 프로세스를 나누지 않고 하드웨어 태그 레지스터(Intel MPK, ARM PAN/TTBR)로 한 주소공간 안에 여러 보호 도메인을 만든다. VIRT-ATC24-08(Limitations of Modern Hardware Isolation Mechanisms)은 MPK/PAC/MTE/Morello-CHERI 네 후보를 동일한 "migrating threads" 모델 위에서 직접 비교해, SPEC 강제 오버헤드가 Intel MPK+CET 0.4%부터 ARM PAC >100%까지 벌어진다는 하중이 큰 비교표를 제공한다. VIRT-MIDDLEWARE24-15(LightZone)은 ARM64에 네이티브 in-process 격리 프리미티브가 없다는 문제를 TTBR 기반(스케일러블, ~490 cycle) + PAN 기반(빠름, ~11-22 cycle, 2-domain 한정) 두 스위칭 방식으로 해결한다.

**(e) SFI/binary rewriting.** 컴파일된 바이너리를 검증해 메모리 접근을 주소 마스킹으로 가둔다. VIRT-ASPLOS24-04(LFI)는 ARM64에서 단일 guard instruction으로 4GiB 샌드박스를 강제해 프로세스 주소공간 하나에 약 65,000개(NaCl의 <3,000개 대비) 샌드박스를 넣는다. VIRT-OSDI25-09(Deterministic Client)는 SFI 위에 결정론적 실행(메터링, bundle-aligned 코드)을 얹어 스마트컨트랙트급 재현성을 얻는다.

**(f) Wasm 기반 격리.** 언어 수준 샌드박스(linear memory)로 이식성과 안전성을 얻지만 표준 POSIX 호환은 별도로 재구축해야 한다. VIRT-EUROSYS25-16(WALI)은 WASI를 재구현하는 대신 Linux syscall ABI를 거의 그대로 Wasm import로 노출해(~137개 syscall, ~2000 LoC) "얼마나 많은 격리 정책이 순수 mechanism이 아니라 policy인가"를 보여준다.

**(g) VM-backed sandbox (microVM).** 하드웨어 가상화를 유지하되 그 무게를 줄인다. VIRT-EUROSYS25-17(CKI, 이 문서에서는 T7과 겹치는 P1)은 EPT/2차원 페이징을 아예 버리고 PKS 세 특권 레벨(host kernel/KSM/deprivileged guest kernel)로 대체해, nested cloud에서 메모리 집약 앱 저하를 28-226%에서 최대 72% 줄인다.

**(h) capability 기반 시스템.** CHERI류 하드웨어 capability로 프로세스 경계 없이 fine-grained 격리를 얻는다. VIRT-SOSP25-13(μFork)은 CHERI 태그 비트로 포인터를 재배치해 단일 주소공간 OS(Unikraft 기반)에서도 POSIX fork를 지원한다(fork 지연 54us, CheriBSD 대비 3.7배).

세 축을 한 문장으로 요약하면: namespace/cgroup은 호환성 최고·격리 최약, 마이크로커널/split-kernel과 capability 계열은 격리 강도와 호환성을 함께 높이려다 엔지니어링/TCB 비용을 지불하며, MPK/SFI/Wasm 계열은 오버헤드를 극단적으로 낮추는 대신 격리 강도(특히 cross-core revocation, 언어적 제약)를 일부 양보한다.

## 3. 핵심 논문 (P0/P1)

### namespace/cgroup 계열

**VIRT-SOSP24-04 | SigmaOS (SOSP 2024, CORE P1, FULL/HIGH).** 서버리스(빠른 시작, 상태 없음)와 마이크로서비스(장시간 실행, 상태 있음, P2P 통신)를 하나의 플랫폼에 담으려는 문제를, sigma-container(네트워크 namespace·overlay FS 생략, 공유 읽기전용 root FS, FUSE 기반 demand-paging)와 sigma-EP(테넌트 범위의 불투명 연결 토큰)로 푼다. Trade-off: sigmaOS API로 포팅해야 하며 out-of-the-box Linux 호환은 포기한다. 콜드스타트 7.7ms, 클러스터 전체 처리량 36,650 procs/sec.

**VIRT-OSDI26-09 | vBOIDs (OSDI 2026, CORE P2, DESIGN_EVAL/HIGH).** cgroup quota가 시간만 제한하고 동시 코어 점유는 제한하지 않는다는 결함을 BOID(스레드를 묶은 vCPU 유사 스케줄링 단위)로 고친다. 스레드가 아니라 BOID를 이동시켜 탐색 공간을 O(threads)에서 O(BOIDs)로 줄이고, Hotel Reservation에서 처리량 최대 3배, 코어 간 마이그레이션을 315.47회/sec/core에서 16.85회로 낮춘다.

### 마이크로커널/split-kernel 계열

**VIRT-OSDI24-03 | HongMeng (OSDI 2024, CORE P1, FULL/HIGH).** 고전 마이크로커널이 빠르지만 Linux 비호환이라는 문제를, 서비스별로 세 가지 격리 등급(IC0 커널공간 공유·IC1 하드웨어 워치포인트/PKS 기반·IC2 완전 유저공간)을 선택하게 해서 푼다. capability 슬롯 대신 address-token(커널 객체를 페이지로 직접 매핑, ~6 cycle vs 526+ cycle)으로 접근 제어 비용을 낮춘다. Trade-off: fork()/clone()은 Linux보다 2.5-4.8배 느리고 capability chain revocation이 없다.

**VIRT-OSDI25-03 | MettEagle (OSDI 2025, CORE P0, FULL/HIGH).** Linux 컨테이너가 기본적으로 갖는 ambient authority를 seccomp/cgroup/namespace로 사후에 깎아내는 대신, L4Re 마이크로커널의 zero-ambient-authority capability로 처음부터 아무 권한도 주지 않는다. TCB 89,271 SLOC(Linux+containerd+runc의 30분의 1), 33건의 고위험 컨테이너 CVE 중 seccomp-bpf 8/8·namespace 4/22·cgroup 0/3을 원천 회피. Trade-off: SPAFS 파일시스템 stat()이 Linux ramfs보다 약 10배 느리고, 64개 동시 실행 시 coarse-grained kernel locking으로 확장성이 떨어진다.

**VIRT-ATC25-01 | LiteShield (ATC 2025, CORE P1, DESIGN_EVAL/HIGH).** 표준 컨테이너의 300+ syscall 공격 표면과 Kata/Firecracker급 VM의 무게 사이에서, syscall을 delegable(142개, shared-memory IPC로 유저스페이스 uKernel 서비스가 처리)과 non-delegable(28개, ptrace로 중재)로 나눠 guest-host 인터페이스를 22개로 줄인다. Redis+YCSB workload B에서 native의 114%에 달하는 처리량을 보이지만, 정적 링크/inline-syscall 바이너리와의 호환성을 잃는다.

**VIRT-ATC25-16 | ASTERINAS (ATC 2025, CORE P1, DESIGN_EVAL/HIGH).** Rust OS 커널이 여전히 하드웨어 접근을 위해 unsafe Rust에 의존해 TCB를 부풀리는 문제를, "OS framework(OSTD)만 unsafe를 허용하고 나머지 서비스는 순수 safe Rust로 작성"하는 framekernel 설계로 푼다. IPC 없이 monolithic 커널 성능(LMbench 1.08x, Redis 1.31x)을 유지하면서 TCB는 75.3 KLoC의 14.0%(Tock 43.8%, Theseus 62.4%)에 불과하다. Trade-off: Rust 컴파일러 자체를 TCB에 포함해야 한다.

**VIRT-EUROSYS26-06 | SKernel (EuroSys 2026, CORE P1, ABSTRACT_INTRO/MEDIUM).** Kata류(강한 격리, 낮은 탄력성)와 gVisor류(host-kernel 의존, 성능 손실) 사이에서 컨테이너마다 독립된 split guest kernel slice를 elastic하게 붙였다 뗀다는 아이디어이나, state_mechanism과 정량적 오버헤드가 이 corpus에서는 확보되지 않았다(§9).

**VIRT-EUROSYS26-01 | CofferOS (EuroSys 2026, CORE P2, ABSTRACT/MEDIUM).** 공유 커널의 메모리 안전성 버그 하나가 모든 tenant 격리를 깨는 문제를, 컨테이너가 닿는 커널 표면 자체를 Rust로 재작성해 완화한다. 두 번째 guest kernel 없이 VM급 격리에 접근하려는 시도이나, 이 corpus 근거로는 정량적 결과가 확인되지 않는다.

### unikernel 계열

**VIRT-SOCC24-04 | SURE (SoCC 2024, CORE P1, ABSTRACT_INTRO/MEDIUM).** 컨테이너 기반 서버리스 격리(gVisor/Knative급)가 VM급 격리를 희생한다는 문제를, Unikraft+QEMU 함수당 unikernel과 DPDK 기반 zero-copy 통신으로 푼다. 저자 자체 수치로 Knative 대비 최대 79배 개선을 보고하나, 이 corpus에서는 독립적으로 검증되지 않았다.

**VIRT-SOCC24-05 | uIO (SoCC 2024, CORE P1, DESIGN_EVAL/HIGH).** unikernel이 컴파일 타임 특수화의 대가로 런타임 확장성(디버깅, 모니터링)을 잃는 문제를, 호스트 프로세스(uIO-fs/uIO-console)와 게스트 내 "uIO context" 스레드로 외부 ELF 객체를 fork/exec 없이 로드·실행하게 한다. MPK 기본 읽기전용 권한 또는 eBPF 샌드박스 인터프리터 중 선택 가능. MPK 격리는 unisolated 대비 1.9% 미만의 오버헤드만 추가한다.

**VIRT-SOCC25-02 | Memory Matters (SoCC 2025, CORE P1, DESIGN_EVAL/HIGH).** 정적으로 컴파일된 unikernel 인스턴스마다 동일한 라이브러리 코드가 중복되는 문제를, Linux KSM의 런타임 스캔(수렴 지연, 타이밍 부채널 위험) 대신 빌드타임에 페이지 동일 청크를 추출해 로드타임에 공유 페이지 풀에서 직접 매핑한다. 128개 FaaS 인스턴스 기준 KSM-quiet 대비 메모리 24-30% 추가 절감, 페이지폴트 3-5배 감소.

### MPK/in-process domain 계열

**VIRT-ATC24-08 | Limitations and Opportunities of Modern Hardware Isolation Mechanisms (ATC 2024, SUPPORT P1, DESIGN_EVAL/HIGH).** MPK/PAC/MTE/Morello-CHERI를 동일한 "private heap + shared exchange heap" 모델 위에서 직접 비교해, 어떤 CORE 샌드박스 논문이 왜 MPK를 골랐는지의 근거표를 제공한다. SPEC 강제 오버헤드 Intel MPK+CET 0.4% vs ARM PAC 100%+; MPK는 cross-core revocation을 지원하지 못한다는 구조적 한계도 명시한다.

**VIRT-MIDDLEWARE24-15 | LightZone (Middleware 2024, CORE P1, DESIGN_EVAL/HIGH).** ARM64에 x86 VMFUNC/MPK급 in-process 격리 프리미티브가 없다는 문제를, TTBR 기반(다중 stage-1 page table, 128+ 도메인, ~490 cycle) + PAN 기반(2-도메인 한정, ~11-22 cycle) 두 스위칭 방식의 혼합으로 해결한다. Nginx 크립토 키 격리에 PAN을 적용하면 처리량 손실 0.91-1.35%.

**VIRT-EUROSYS25-14 | AlloyStack (EuroSys 2025, CORE P1, FULL/HIGH).** 서버리스 워크플로우가 함수마다 콜드스타트를 내고 중간 데이터를 프로세스/VM 경계 너머로 복사하는 문제를, 워크플로우 전체를 하나의 주소공간(WFD)에 스레드로 담고 MPK로 LibOS와 사용자 함수를 나눠 해결한다. 콜드스타트 98.5% 감소(1.3ms), 16MB 중간 데이터 전달이 참조 전달로 대체돼 Rust 기준 2.6배 빠르다. Trade-off: MPK+명령어 블랙리스트가 별도 주소공간보다 약한 격리다.

**VIRT-OSDI25-10 | bpftime (OSDI 2025, CORE P1, FULL/HIGH).** 커널 트랩 기반 eBPF의 uprobe/uretprobe 비용(~2500-3000ns)을 없애기 위해, 기존 eBPF 검증기를 유저스페이스에서 재사용(UbiBPF)하고 Intel MPK 도메인 스위칭(ERIM 스타일)으로 확장을 호스트 프로세스 안에서 격리한다. uprobe 지연 190.02ns(커널 eBPF 대비 13.5배), Nginx 방화벽 플러그인 오버헤드 2%(Lua/Wasm/ERIM 11-12%). Trade-off: Intel MPK 하드웨어에 의존하고 ERIM급 syscall 우회 공격에 노출된다.

**VIRT-OSDI25-15 | Omniglot (OSDI 2025, CORE P1, FULL/HIGH).** 안전한 언어(Rust)가 안전하지 않은 외부(C) 라이브러리를 호출할 때 모든 안전성 보장이 무너지는 문제를, RISC-V PMP(임베디드) 또는 Intel MPK(유저스페이스) 하드웨어 보호 도메인 + 3단계 포인터 검증 파이프라인으로 막는다. libpng 23kB 디코딩(MPK)에서 격리로 인한 오버헤드 +12.7%. Trade-off: MPK 변형은 raw syscall/시그널 핸들러로 탈출 가능하다는 약점을 인정한다.

**VIRT-EUROSYS25-17 | CKI (EuroSys 2025, CORE P1, FULL/HIGH — 주 taxonomy 겹침 T1/T2/T7).** 보안 컨테이너가 범용 VM용 하드웨어 가상화(2차원 페이징, VM exit)를 그대로 물려받아 nested cloud에서 메모리 집약 앱이 28-226% 저하되는 문제를, EPT/VMX를 아예 버리고 PKS 3-privilege(host kernel/KSM/deprivileged guest kernel)로 대체한다. nested page fault 1067ns(HVM-NST 32565ns). Trade-off: PKS가 주소공간당 16개 도메인만 지원해 컨테이너별 연속 물리 메모리가 필요하다(파편화).

**VIRT-MIDDLEWARE25-01 | K23 (Middleware 2025, CORE P1, FULL/HIGH).** syscall interposition이 (a) 일부를 놓치거나 (b) 타깃이 스스로 끌 수 있거나 (c) 잘못 디스어셈블하거나 (d) 너무 느리다는 네 가지 함정 중 어느 하나에 항상 걸린다는 문제를, 오프라인 프로파일링으로 유효한 syscall 주소를 미리 확정한 뒤 온라인에서 그 주소만 선택적으로 재작성(zpoline 스타일)하는 방식으로 해결한다. 매크로벤치마크에서 native의 98.62%를 유지하면서, LD_PRELOAD 제거·prctl 기반 SUD 비활성화라는 두 가지 알려진 우회를 막는다.

### SFI/binary rewriting 계열

**VIRT-ASPLOS24-04 | LFI (ASPLOS 2024, CORE P1, FULL/HIGH).** 하드웨어 가상화/컨테이너의 수천 cycle 컨텍스트 스위치 비용을 피하기 위해, ARM64에서 단일 guard instruction으로 모든 메모리 접근을 4GiB 영역에 가둔다. 주소공간 하나에 약 65,000개 샌드박스(NaCl <3,000개)를 담으면서 SPEC 오버헤드는 6.4-7.3%. Trade-off: 특정 calling convention/guard discipline을 지키는 컴파일된 코드가 필요하다.

**VIRT-OSDI25-09 | Deterministic Client (OSDI 2025, CORE P1, FULL/HIGH).** 스마트컨트랙트급 결정론적 실행을 위해 보통은 Wasm/EVM 같은 포터블 바이트코드+트러스티드 인터프리터를 쓰지만, 이는 오버헤드가 크다. DeCl은 네이티브 x86-64/Arm64 기계어를 로드타임에 결정론적 명령어 부분집합인지 검증하고, LFI를 메모리 격리에 재사용한다(DeCl-LFI). SPEC 오버헤드는 timer 기반 메터링 기준 19.2%(x86-64)로, Wasmtime-fuel의 76.5%보다 훨씬 낮다.

### Wasm 기반 격리

**VIRT-EUROSYS25-16 | WALI (EuroSys 2025, CORE P1, FULL/HIGH).** WASI를 플랫폼마다 재구현해야 하고 여전히 mmap/시그널 등을 지원하지 못하는 문제를, 호스트 syscall ABI를 거의 그대로 Wasm import section에 노출(~137개 syscall, ~2000 LoC)해서 해결한다. per-syscall 오버헤드는 대부분 1% 미만(read 167ns)이지만, Wasm 실행 자체가 native 대비 median 약 2.32배 느리다는 것이 지배적 비용이다. Trade-off: WASI가 노렸던 좁은 capability 표면을 포기하고 정책을 상위 계층으로 넘긴다.

**VIRT-SOSP25-08 | Dandelion (SOSP 2025, CORE P1, DESIGN_EVAL/HIGH).** 서버리스 콜드스타트가 최소 8ms(microVM 스냅샷 로드+네트워크 재수립)라는 문제를, "사용자 코드는 순수·결정적·syscall-free"라는 프로그래밍 모델 변경으로 근본적으로 없앤다 — guest OS 자체가 불필요해진다. 4개의 교체 가능한 백엔드(CHERI capability ~89us, rWasm ~241us, ptrace 프로세스 ~486us, guest kernel 없는 KVM ~889us)로 같은 서비스를 구현해 "guest OS가 실제로 무엇을 비용으로 만드는가"를 정면으로 측정한다. Trade-off: 기존 POSIX 코드를 DAG로 재작성해야 하고 OLTP 같은 상태 유지 워크로드는 배제한다.

### VM-backed sandbox / 서버리스 특화

**VIRT-ATC24-14 | Function REWIND (ATC 2024, CORE P1, DESIGN_EVAL/HIGH).** 웜 컨테이너 재사용이 빠르지만 침입 간 상태가 남아 데이터 누출/루트킷 지속을 허용하는 문제를, 매 4KB 페이지테이블 리프를 8KB(정상 PTE+buddy PTE)로 확장해 스냅샷/되감기를 국소적으로 처리한다. 피크 RSS 오버헤드 11%로 Groundhog(체크포인트/복원)보다 훨씬 가볍다.

**VIRT-SOCC25-01 | Hydra (SoCC 2025, CORE P1, FULL/HIGH).** 서버리스가 매 호출마다 컨테이너/VM + 언어별 런타임 전체 스택 비용을 지불하는 문제를, GraalVM Native Image로 미리 컴파일한 공유 런타임 위에 호출마다 "메모리 isolate"(전체 프로세스가 아니라)를 두는 방식으로 완화한다. 함수 밀도 4.47배, 메모리 2.1배 절감. Trade-off: 네이티브/비관리 코드는 isolate 샌드박싱이 안 돼 프로세스 fallback이 필요하다.

### confidential container (T7 다리)

**VIRT-EUROSYS26-18 | Pyramid (EuroSys 2026, CORE P1, ABSTRACT/MEDIUM).** 하드웨어 TEE급 보안과 Kubernetes급 효율적 멀티테넌시 오케스트레이션을 동시에 얻기 위해, 신뢰 가능한 얇은 Kubernetes 레이어를 신뢰 불가능한 상용 Kubernetes 위에 얹어 tenant 비밀이 스케줄링 레이어에 노출되지 않게 한다. 데이터 플레인 처리량 1.4배(원문 abstract 수준 근거).

## 4. Supporting 논문 (P2/P3)

**컨테이너 이미지/런타임 메커니즘 (SUPPORT — 격리 아키텍처 자체는 바꾸지 않음):**
- **VIRT-ASPLOS24-05 RainbowCake (P2)**: 레이어 단위로 컨테이너 캐시를 부분 공유해 콜드스타트 68%, 메모리 낭비 77% 감소.
- **VIRT-ATC24-15 SimEnc (P3)**: 암호화된 Docker 레이어에서도 유사도 기반 중복 제거를 가능하게 하는 semantic hash 네트워크.
- **VIRT-SOCC25-17 BLAFS (P2)**: 상위 20개 DockerHub 이미지의 60% 이상이 "bloat"라는 관찰에서 출발해, 레이어 구조를 유지하며 미사용 파일을 제거. 콜드스타트 최대 68% 감소.
- **VIRT-MIDDLEWARE25-06 FaaSImage (P2)**: 레이어 fusing과 lazy fetching 두 기존 노선을 개선하는 이미지 매니저.
- **VIRT-SC25-03 XaaS Containers (P2)** / **VIRT-SC25-04 coMtainer (P2)**: HPC 컨테이너가 배포 시점 하드웨어 최적화를 못 받는 문제를, 소스/IR 배포 또는 빌드 provenance 메타데이터 임베딩으로 해결. coMtainer는 generic 이미지가 native 대비 50-72% 느리다는 것(LULESH, x86-64/AArch64)을 정량화한다.
- **VIRT-SC25-05 EDDE (P2)**: 엣지 배포에서 nearest-edge-server 기반 on-demand 파일 페치.
- **VIRT-ATC25-10 On-Demand Container Partitioning (P3)**: 분할 ML 모델 배포를 위한 2DFS 레이어 타입.
- **VIRT-ATC25-06 Poby (P2, 주 taxonomy T3)**: SmartNIC DRAM으로 이미지 다운로드+압축해제를 파이프라인해 콜드스타트 13.2배 개선(containerd 대비).

**커널 확장 격리:**
- **VIRT-SOSP24-06 KFlex (P2, SUPPORT)**: 커널 소유 자원은 eBPF 검증기로, 확장 힙은 런타임 SFI로 나눠 이중 안전성을 확보. Memcached 처리량 1.23-2.83배(eBPF baseline 대비).
- **VIRT-ATC25-17 Rex (P2, SUPPORT)**: eBPF 검증기의 "언어-검증기 격차"를 safe-Rust 하위집합으로 대체. 8코어에서 1.98M RPS로 eBPF-BMC(1.92M RPS)를 근소하게 상회.
- **VIRT-OSDI26-08 vBPF (P2)**: 여러 tenant가 같은 커널 hook에 붙는 eBPF의 O(N) 디스패치 문제를 네임스페이스 기반 O(1) 조회로 해결. 160개 프로그램 부착 시 54배 개선.

**기타:**
- **VIRT-ASPLOS24-11 Loupe (P2, SUPPORT)**: unikernel/LibOS가 실제로 구현해야 할 최소 OS 기능 집합을 동적 분석으로 도출.
- **VIRT-MIDDLEWARE24-09 B-Side (P3, SUPPORT)**: 소스 없이 x86-64 바이너리에서 정밀한 seccomp 화이트리스트를 뽑아내는 정적 분석. 경쟁 도구 대비 syscall 집합이 훨씬 촘촘하다(43개 vs 271/95개).
- **VIRT-MIDDLEWARE24-08 Funclets (P2, SUPPORT)**: Faasm의 Wasm 샌드박스 스레드 모델을 유지하면서 I/O 집약 코드만 스토리지 노드로 마이그레이션.
- **VIRT-MIDDLEWARE25-04 Roadrunner / VIRT-MIDDLEWARE25-05 RUNE (P2, SUPPORT)**: 각각 Wasm linear memory의 zero-copy 데이터 경로, 그리고 컨테이너/Wasm 하이브리드 런타임.
- **VIRT-HPCA24-04 DockerSSD (P2, CORE, 주 taxonomy 겹침 T3)**: Docker+가상 펌웨어를 SSD 임베디드 프로세서 안으로 밀어넣어, "컨테이너 격리 아키텍처는 CORE"라는 규칙이 CPU가 아닌 디바이스에도 적용되는 드문 사례.
- **VIRT-HPCA25-02 SpecMPK (P2, SUPPORT)**: Intel MPK의 WRPKRU 직렬화 비용(실하드웨어 69.76%)을 speculative 실행+카운터 기반 게이팅으로 12.21% 평균 개선.
- **VIRT-CCGRID26-01 TelePod (P1, CORE, ABSTRACT/MEDIUM)**: CRIU를 pre-copy 반복 전송 + 목적지측 겹침 복원으로 확장해 상태 유지 컨테이너의 라이브 마이그레이션을 하이퍼바이저 VM 마이그레이션에 근접시킨다는 주장이나, 정량적 수치는 이 corpus에서 확보되지 않았다.

## 5. Trade-off 구조

**(1) 격리 강도 ↔ 오버헤드/호환성.** 이 계층 전체를 관통하는 단일 구조다: namespace/cgroup(가장 약한 격리, 최고 호환성, 최저 오버헤드) → MPK/SFI/Wasm in-process 격리(중간 격리, 낮은 오버헤드, 언어/컴파일 제약) → 마이크로커널/split-kernel/capability(강한 격리, 일부 성능 손실, 엔지니어링 비용) → VM/microVM(가장 강한 격리, 가장 무거움). VIRT-ATC24-08의 비교표(MPK 0.4% vs PAC 100%+ 오버헤드)와 VIRT-OSDI25-03(MettEagle)의 CVE 회피표(마이크로커널이 33건 중 12건을 원천 차단하지만 TCB는 여전히 89K SLOC)가 이 스펙트럼의 양쪽 끝을 정량적으로 못박는다.

**(2) 격리 단위를 넓히면 성능은 오르지만 격리는 흐려진다.** VIRT-EUROSYS25-14(AlloyStack)가 정확히 이 거래를 보여준다 — 격리 단위를 함수에서 워크플로우로 넓히면 콜드스타트와 데이터 전달이 "비용에서 비이벤트"로 바뀌지만, 워크플로우 내부의 함수 간 격리는 MPK+명령어 블랙리스트 수준으로 약해진다. VIRT-SOCC25-01(Hydra)의 memory isolate, VIRT-MIDDLEWARE25-04(Roadrunner)의 공유 Wasm VM도 동일한 거래를 한다.

**(3) 하드웨어 태그 프리미티브의 근본적 한계.** MPK는 코어당 레지스터라서 cross-core revocation을 지원하지 못하고(VIRT-ATC24-08), WRPKRU 직렬화가 도메인 스위칭 빈도가 높을 때 69.76%까지 비용을 낸다(VIRT-HPCA25-02). ARM에는 아예 x86급 프리미티브가 없어 LightZone처럼 TTBR/PAN을 조합해야 한다. 즉 "저렴한 in-process 격리"는 항상 특정 ISA의 하드웨어 지원 여부에 강하게 의존한다.

**(4) 언어 기반 격리는 컴파일러/툴체인을 TCB에 편입시킨다.** ASTERINAS(safe Rust)와 Rex(safe-Rust eBPF 확장)는 모두 하드웨어 격리 대신 타입 시스템을 경계로 쓰면서, "Rust 컴파일러 자체가 옳다"는 것을 새로운 신뢰 축으로 추가한다. 이는 VIRT-ASPLOS24-02(T7, MIRVerif) 같은 형식 검증 연구가 왜 필요한지를 보여주는 배경이기도 하다.

## 6. 인접 계층과의 관계

- **T1(CPU 가상화) 아래로**: VIRT-EUROSYS25-17(CKI)과 VIRT-OSDI26-01(JANUS, 주 taxonomy T1)이 "보안 컨테이너가 VM용 하드웨어 가상화를 얼마나 필요로 하는가"를 정면으로 묻는다. JANUS는 CPU 이벤트 처리는 L1에, 메모리 변환 권한은 L0에 남겨 world-switch 지연을 KVM 대비 대폭 줄인다(2,700 cycle vs 16,002 cycle). VIRT-SOCC24-10(Faascale, 주 taxonomy T2)은 Firecracker microVM의 메모리를 수직으로 늘리고 줄이는 elasticity를 다뤄, T2의 HyperAlloc/virtio-mem 계보와 T5의 microVM 계보를 잇는다.
- **T2(메모리 가상화)와의 다리**: VIRT-SOSP24-06(KFlex)의 확장 힙, VIRT-SOSP25-13(μFork)의 copy-on-pointer-access가 모두 "격리 단위 안에서 메모리를 어떻게 다루는가"라는 T2의 질문을 컨테이너/unikernel 스케일에서 재현한다.
- **T3(I/O 가상화) 위로**: VIRT-EUROSYS25-01(FastIOV)과 VIRT-ASPLOS26-01(SG-IOV)는 secure container가 SR-IOV/소켓 단위 I/O 가상화를 쓸 때의 시작 비용을 다루며, VIRT-ATC25-06(Poby)은 SmartNIC 오프로드를 콜드스타트 문제에 적용한다.
- **T4(마이그레이션)와의 다리**: VIRT-SOCC24-08(PCLive)과 VIRT-CCGRID26-01(TelePod)이 컨테이너 체크포인트/복원과 라이브 마이그레이션을, VIRT-ATC24-19(Faascale의 자매격인 PASS)가 microVM 스냅스타트를 다룬다.
- **T7(기밀 컴퓨팅)과의 다리**: VIRT-EUROSYS26-18(Pyramid)이 TEE 위에 Kubernetes를 얹고, VIRT-EUROSYS25-05(Erebor, T7 primary)가 기밀 VM *안에서* 서비스 제공자 소프트웨어로부터 격리되는 두 번째 경계를 만들며, VIRT-EUROSYS25-18(RAKIS, T7 primary)이 enclave 안에서 커널 우회 I/O를 다룬다 — 모두 T5의 in-process/microVM 격리 기법을 T7의 신뢰 경계 안에 재적용한 사례다.
- **T9(자원관리)와의 다리**: VIRT-MICRO24-17(Mosaic, T9 primary)은 마이크로아키텍처 자원(L2/TLB/LLC/BTB)을 함수별로 태깅해 서버리스 컨텍스트 스위치 비용을 없애는, MPK/CHERI와는 다른 층위의 "태그 기반 격리"다.

## 7. 2024 → 2026 변화

**2024년**: 이 해의 corpus는 격리 메커니즘 계열을 광범위하게 처음 확립했다 — 마이크로커널 재해석(HongMeng), Wasm 커널 확장(KFlex), 하드웨어 격리 프리미티브 비교(ATC24-08), unikernel의 컴플라이언스 비용 정량화(Loupe), 그리고 컨테이너 이미지/런타임을 격리 아키텍처와 명확히 분리하는 관점(RainbowCake, SimEnc)이 나왔다.

**2025년**: 격리 메커니즘이 급격히 다양해졌다. 마이크로커널 계열이 MettEagle(L4Re capability)과 LiteShield(userspace uKernel)로 두 갈래를 냈고, 언어 기반 격리가 ASTERINAS(전체 커널)와 Rex(커널 확장만)로 갈라졌다. MPK 기반 in-process 격리가 AlloyStack(워크플로우 단위), bpftime(eBPF), Omniglot(FFI)으로 세 방향에 동시에 적용됐고, CHERI capability가 Dandelion(서버리스 백엔드 중 하나)과 μFork(단일 주소공간 fork)로 실제 시스템에 처음 결합됐다. 이 해에 "guest OS가 실제로 무엇을 비용으로 만드는가"(Dandelion)와 "하드웨어 가상화가 보안 컨테이너에 실제로 필요한가"(CKI)라는 두 개의 근본 질문이 명시적으로 제기됐다.

**2026년(초기 문헌)**: split-kernel(SKernel)과 Rust 강화(CofferOS)가 "네임스페이스/cgroup 컨테이너와 VM 샌드박스 사이의 스펙트럼을 좁히려는" 시도를 이어가고, vBPF·vBOIDs는 각각 eBPF와 CPU 스케줄링이라는 기존 메커니즘 자체를 "가상화 대상"으로 재정의한다 — 격리 연구의 초점이 "새 경계를 만드는 것"에서 "기존 공유 메커니즘(cgroup, eBPF hook)을 멀티테넌트에 맞게 재설계하는 것"으로 옮겨가는 조짐이다. 다만 2026년 표본은 이 문서 기준 5편(대부분 ABSTRACT 단계)뿐이라, 이를 확정된 추세로 단정하기보다는 관찰된 방향으로만 적어둔다.

## 8. 읽는 순서 제안

1. **VIRT-ATC24-08 (Limitations of HW Isolation)** — MPK/PAC/MTE/CHERI 네 프리미티브의 좌표계를 먼저 파악한다.
2. **VIRT-ASPLOS24-04 (LFI)** — SFI 계열의 가장 순수한 예로 "격리는 소프트웨어 검증만으로도 가능하다"를 본다.
3. **VIRT-OSDI24-03 (HongMeng)** → **VIRT-OSDI25-03 (MettEagle)** — 마이크로커널이 성능(HongMeng)과 보안 형식화(MettEagle) 두 방향에서 어디까지 갔는지 비교한다.
4. **VIRT-ATC25-01 (LiteShield)** — 하이퍼바이저 없이 VM급 인터페이스 축소를 내는 세 번째 지점.
5. **VIRT-SOCC24-05 (uIO)** → **VIRT-MIDDLEWARE24-15 (LightZone)** — unikernel 내부 in-process 격리와 ARM64 하드웨어 프리미티브를 연결한다.
6. **VIRT-EUROSYS25-14 (AlloyStack)** — 격리 단위를 넓히는 거래를 정면으로 본다.
7. **VIRT-OSDI25-10 (bpftime)** → **VIRT-OSDI25-15 (Omniglot)** — MPK 도메인 스위칭이 서로 다른 문제(커널 확장, FFI)에 어떻게 재사용되는지.
8. **VIRT-SOSP25-08 (Dandelion)** — 네 가지 격리 백엔드를 한 서비스 위에서 직접 비교하는 corpus의 핵심 실험.
9. **VIRT-EUROSYS25-17 (CKI)** — 하드웨어 가상화를 걷어낸 보안 컨테이너.
10. **VIRT-SOSP25-13 (μFork)** — capability 기반 단일 주소공간 OS로 마무리.

## 9. 증거 한계

다음 문헌은 abstract 또는 abstract-intro 수준 근거에 머물러 메커니즘 세부가 이 corpus 안에서 깊이 검증되지 않았다: VIRT-SOCC24-04(SURE), VIRT-EUROSYS26-01(CofferOS), VIRT-EUROSYS26-06(SKernel), VIRT-EUROSYS26-18(Pyramid), VIRT-CCGRID26-01(TelePod), VIRT-EUROSYS26-15(DROPS), VIRT-MIDDLEWARE25-05(RUNE), VIRT-MIDDLEWARE25-06(FaaSImage), VIRT-MIDDLEWARE24-08(Funclets), VIRT-SOCC25-17(BLAFS)의 수치 일부. 특히 **SURE**는 "Knative 대비 최대 79배"라는 수치가 저자 자신의 요약에서만 확인되고 이 corpus가 원문을 통해 독립 검증하지 못했다는 점, **SKernel**은 isolation_mechanism 외 state_mechanism·overhead_bottleneck이 모두 UNKNOWN으로 남아 있다는 점을 강조해 둔다. VIRT-HPCA24-04(DockerSSD)의 수치 다수는 KAIST 보도자료 및 후속 arXiv 확장판에서 온 것이라, 동료심사 원문 수치와 구분해서 읽어야 한다. VIRT-ASPLOS26-01(SG-IOV, 주 taxonomy T3)처럼 이 문서에서 다리로만 언급한 논문들의 세부 수치는 각각의 주 topic 문서(I/O 가상화)에서 별도로 확인해야 한다.

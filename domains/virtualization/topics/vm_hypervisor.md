# CPU/기계 가상화 (VM·Hypervisor)

## 1. 이 계층이 푸는 문제

Physical Resource(CPU core) → Logical Abstraction(vCPU, guest VM, nested guest) → Workload(멀티테넌트 클라우드 인스턴스, 컨테이너, 가속기 워크로드)로 이어지는 매핑을 다루는 계층이다. Hypervisor/VMM은 하나의 물리 CPU 코어를 여러 vCPU로 시분할하면서, 각 vCPU가 마치 독립된 물리 CPU인 것처럼 보이게 trap-and-emulate, VMX/SVM 하드웨어 확장, EPT/NPT 같은 second-level 주소변환을 제공한다. 이 계층이 실제로 풀어야 하는 것은 네 가지다. (1) isolation — guest가 물리 자원이나 다른 guest의 상태를 직접 건드리지 못하게 막는 것, (2) multiplexing — 하나의 물리 코어/자원을 여러 vCPU·테넌트에 나눠주는 것, (3) mediation — guest-virtual → guest-physical → host-physical, 또는 guest → VMM → device로 이어지는 추가 경로를 관리하는 것, (4) state — vCPU 레지스터, VMCS/VMCB, EPT 같은 가상화 상태를 다른 호스트로 옮기거나 검증하는 것이다. T1 코퍼스가 보여주는 흥미로운 점은, 이 "trap-and-emulate + 논리적 자원 분할" 패턴이 CPU뿐 아니라 NPU(VIRT-MICRO24-01), 양자 QPU(VIRT-OSDI25-04), FPGA(VIRT-SOCC25-05), SmartNIC(VIRT-SOSP25-15)에도 그대로 반복된다는 것이다. 즉 "CPU 가상화"는 사실 "trap-and-emulate 기반 자원 분할"이라는 더 일반적인 원리의 한 사례이며, 2024-2026 코퍼스는 이 원리가 새로운 물리 자원마다 재발견되는 과정을 보여준다.

## 2. Mechanism design space

**전 하드웨어 지원 가상화 (VMX/SVM + EPT/NPT)**는 기본값이다. Guest는 거의 네이티브로 실행되지만, nested paging은 guest-virtual→guest-physical→host-physical의 2차원 페이지 워크를 요구해 TLB miss 비용이 크다(VIRT-ASPLOS24-01은 x86에서 최대 24~35회의 순차 메모리 접근이 필요하다고 측정). **Nested virtualization**(L0 호스트, L1 guest hypervisor, L2 guest VM)은 이 비용을 한 겹 더 쌓는다: EPT fault 하나가 비-nested 대비 6배의 world switch를 필요로 한다(VIRT-ATC25-02, HyperTurtle). 이를 줄이는 두 가지 상반된 전략이 있다. 하나는 **협력적 책임 분리**(VIRT-OSDI26-01, JANUS)로, CPU 이벤트 처리는 L1에 맡기고 메모리 변환 권한만 L0가 독점해 world-switch 왕복(16,002 cycle, Intel Xeon Platinum 8475B 측정)을 PVM 수준(2,681 cycle)까지 낮춘다. 다른 하나는 **L0 안에서 검증된 확장 코드를 직접 실행**하는 것(VIRT-ATC25-02, HyperTurtle의 eBPF "hyperupcall")으로, L1을 아예 거치지 않고 EPT fault 처리 지연을 28.39µs에서 5.40µs로 줄인다(약 5.26배).

**Paravirtualization vs 추론 기반 vCPU 노출**도 대비되는 축이다. PVM/XPV/CPS 계열은 guest에 실시간·정확한 vCPU 정보를 파라virtual 채널로 제공하지만 guest 수정이 필요하다. VIRT-EUROSYS25-04는 반대로 guest 수정 없이 vCPU capacity·preemption·topology를 사용자공간에서 추론(vcap/vact/vtop)해 스케줄링 도메인을 재구성하는데, 정확도는 수 초 단위로 느리지만 어떤 클라우드에도 배포 가능하다는 장점을 가진다.

**Trap-and-emulate의 일반화**는 이 코퍼스의 또 다른 축이다. VIRT-SOSP25-04(Miralis)는 RISC-V M-mode 펌웨어 전체를 deprivilege해 가상화하고, VIRT-HPDC25-03/VIRT-HPDC26-01(FPVM, tiny FP)은 부동소수점 명령어를 trap해 임의 정밀도(3비트까지도) 산술로 대체한다. 이는 "가상화의 본질은 guest/host 주소공간이나 hypervisor ring이 아니라 선택적 가로채기+투명한 대체"라는 것을 보여주는 경계 사례다. VIRT-ATC24-21(CrossMapping)은 binary translation에서 메모리 일관성 모델 자체를 가상화 대상으로 다룬다.

**Non-CPU 자원에 동일 패턴 적용**: VIRT-MICRO24-01(NeuISA)은 VLIW NPU 명령어를 micro-Tensor Operator로 분해해 하드웨어/소프트웨어 격리 모드와 동적 하베스팅을 지원하는 vNPU를 만든다. VIRT-OSDI25-04(HyperQ)는 QPU를 공간적으로(격자 topology 매칭 region) 그리고 시간적으로(measurement/reset, 상태 저장이 불가능하므로 context switch 자체가 없음) 나눈다. VIRT-SOCC25-05(Funky)는 unikernel + hypercall 기반으로 FPGA reconfigurable fabric을 spatial partition한다. VIRT-SOSP25-15(Tai Chi)는 SmartNIC OS 안에 vCPU를 통합해 데이터플레인의 idle cycle에 컨트롤플레인을 얹는 하이브리드 가상화를 제안한다.

**Hypervisor correctness 검증**은 별도의 축이다. VIRT-OSDI24-04(VeriSMo)는 machine-model 계층과 구현 계층을 분리해 적대적 hypervisor 하에서도 confidential VM의 안전성을 증명하고, VIRT-SOSP25-03(Ghost in the Android Shell)은 실행 가능한 test-oracle 명세로 production pKVM의 isolation invariant를 검사하며, VIRT-EUROSYS26-03(NecoFuzz)은 VMCS/VMCB 상태를 "valid/invalid 경계 근처"로 생성해 nested virtualization 인터페이스를 퍼징한다. VIRT-ASPLOS26-06은 심지어 "형식 검증된 명세" 자체(Arm CCA RMM)에서도 내부 모순 35건을 찾아낸다 — 구현 검증만으로는 명세 자체의 결함을 잡을 수 없다는 교훈이다.

**VM 없이 vCPU 유사 속성만 흉내내는 경량 대안**도 있다: VIRT-OSDI26-09(vBOIDs)는 컨테이너 스레드를 BOID로 묶어 pinning 수준의 캐시 지역성을 hypervisor 없이 얻고, VIRT-ATC25-01(LiteShield)과 VIRT-EUROSYS26-06(SKernel)은 syscall 인터포지션/split-kernel로 hypervisor 경계를 대체한다.

## 3. 핵심 논문 (P0/P1)

**VIRT-OSDI26-01 | JANUS (OSDI 2026, CORE P0)** — Kata Containers류 secure container의 3단 nested virtualization(L0/L1/L2)에서 CPU 이벤트 처리는 L1 switcher에 맡기고 GPA→HPA 변환 권한은 L0가 독점하는 "cooperative" 모델을 제안한다. 메커니즘은 VMFUNC 기반 trap-free EPTP switching, L1이 L2의 page-table root 변경을 검증하는 shadow-root 구조, Intel #VE 기반 in-guest EPT-violation 처리다. World-switch latency 2,700 cycle(Kata-JANUS) vs 16,002 cycle(Kata-KVM), 8 vCPU에서 멀티프로세스 워크로드 51.8% 개선(Intel Xeon Platinum 8475B, 192 vCPU/384GB 호스트). 대가는 shadow-root 부기 비용과 VMFUNC/#VE 하드웨어 의존성이다.

**VIRT-MICRO24-01 | NPU 가상화 (MICRO 2024, CORE P0)** — TPUv4급 NPU를 위해 VLIW 명령어를 micro-Tensor Operator(uTop)로 분해하고, 스케줄러가 유휴 ME/VE를 다른 vNPU로 동적으로 하베스팅한다. 하드웨어 격리 모드(공간 분할)와 소프트웨어 격리 모드(선점형 시분할)를 모두 지원하며 하드웨어 면적 비용은 TPUv4 칩의 0.04%에 불과하다. p95 tail latency 4.6배 개선(V10 대비, TPUv4급 시뮬레이터, MLPerf v2.1). GPU MIG/MPS의 NPU 버전이라 할 수 있는 사례다.

**VIRT-OSDI24-04 | VeriSMo (OSDI 2024, CORE P0)** — Confidential VM의 in-guest 보안 모듈(VMPL0)이, 언제든 상태를 조작할 수 있는 적대적 hypervisor 아래서도 기밀성·무결성을 지킴을 증명한다. 하드웨어 모델 계층과 구현 계층(Rust ownership + Verus)을 분리한 것이 핵심. Unsafe Rust 블록 32개(AMD/COCONUT SVSM의 150-235개 대비), 검증 시간 약 6분(32코어). 대가는 실행 코드 대비 약 2배의 증명/명세 코드와 #VC 예외·부채널을 모델링하지 않는다는 범위 제한이다.

**VIRT-SOSP24-01 | vSoC (SOSP 2024, CORE P0)** — 모바일 SoC(unified-memory 아키텍처)를 위한 가상 SoC로, 가상 디바이스들이 host-side unified shared-virtual-memory(SVM)를 ID로 참조해 guest-host 복사를 없앤다. Adaptive prefetch(평균 17ms slack interval 활용)와 virtual command fence로 일관성을 관리한다. 신흥 멀티디바이스 앱에서 QEMU-KVM 대비 약 19 FPS→57 FPS. 대가는 적대적 guest에 대한 보안 격리가 전혀 없다는 것 — 협조적 가상 디바이스를 전제한다.

**VIRT-SOSP25-04 | Miralis (SOSP 2025, CORE P0)** — RISC-V M-mode 펌웨어 전체를 사용자 모드로 deprivilege하고 6.2k줄 Rust monitor가 12개 특권 명령어와 84개 CSR을 shadow 상태로 에뮬레이트한다. PMP 우선순위를 강제해 firmware가 monitor 보호 영역을 침범할 수 없게 만들며, 표준 확장(시간 읽기, IPI 등)은 fast-path로 오프로드해 트랩 비용을 상쇄한다. World switch 약 7,000 cycle, fast-path 적용 시 Redis/memcached/MySQL 오버헤드 0-1.2%. Popek-Goldberg trap-and-emulate가 "가장 가상화할 수 없을 것 같은" 특권 레벨에서도 여전히 작동함을 보여준다.

**VIRT-SOCC25-05 | Funky (SoCC 2025, CORE P0)** — unikernel(Funky, IncludeOS/Solo5) + hypercall 매개 접근으로 FPGA를 vFPGA로 가상화한다. 정적 Shell(PCIe DMA/MMU)과 동적 Partial Reconfiguration 영역으로 나뉘며, 3계층 상태 캡처(온칩 로직/FPGA 메모리/VM 상태)로 체크포인트·재개·선점을 지원한다. 네이티브 대비 오버헤드 7.4%, OCI 이미지 크기 28.7배 축소. CPU 가상화의 hypercall·MMU 분할·상태 캡처 패턴이 FPGA에도 그대로 적용될 수 있음을 보여주는 사례다.

**VIRT-EUROSYS26-04 | MigCheck (EuroSys 2026, CORE P0)** — "같은 ISA, 다른 기능(semi-heterogeneous)" 프로세서 간 라이브 마이그레이션의 실행 가능성을 사전에 시뮬레이션으로 예측하는 최초의 체계적 분석. 하드웨어 증설/제거, hypervisor 업데이트, 플랫폼 구성 변경 시나리오에서 검증되었다. 구체적 수치는 abstract 수준에서 확인되지 않으나, "이 VM이 저 호스트로 이동 가능한가"라는 모든 라이브 마이그레이션 논문이 당연시하는 질문에 정면으로 답한다.

**VIRT-CCGRID24-01 | SweetspotVM (CCGrid 2024, CORE P1)** — VM 전체가 아니라 개별 vCPU 단위로 oversubscription 비율을 다르게 설정한다(1.0/1.5/2.6 같은 템플릿). OVHcloud 프로덕션 데이터에서 같은 VM의 vCPU들도 활용률이 크게 다르다는 관찰에서 출발. 프로토타입 평가(EPYC-7662, QEMU/KVM+libvirt, 12시간 트레이스)에서 비-oversubscription 수준 성능을 유지하며 호스팅 비용을 1/3로. Oversubscription vs 성능 보장이라는 고전적 트레이드오프를 VM 단위에서 vCPU 단위로 세분화한 사례.

**VIRT-ATC25-02 | HyperTurtle (ATC 2025, CORE P1)** — L1이 작은 eBPF 프로그램("hyperupcall")을 L0에 등록해, EPT fault·네트워크 정책·프로파일링을 L1을 거치지 않고 L0가 직접 처리하게 한다. eBPF verifier와 bpf_probe_read_hyperupcall로 L1별 메모리 접근을 제한한다. EPT fault latency 5.26배 개선, Kata 컨테이너 부팅 약 27% 단축(4KiB 페이지 기준). 대가는 eBPF 표현력 한계(무제한 루프 불가, huge page 미지원)와 현재는 L2당 L1 하나만 지원한다는 것.

**VIRT-EUROSYS25-04 | 정확한 vCPU 추상화 (EuroSys 2025, CORE P1)** — vCPU가 균일하지 않다는 사실(용량·선점·토폴로지가 실제로는 다름)을 guest 수정 없이 사용자공간 프로브(vcap/vact/vtop)로 추론해 스케줄링 도메인을 재구성한다. Tailbench에서 95th percentile latency가 vCPU 비활성 시간 증가에 따라 최대 20배(2ms→16ms) 증가하는 문제를, 저용량 vCPU를 배치에서 제외해 최대 43% 처리량 개선(Parsec, 16-vCPU VM)으로 완화한다. 파라virtual 설계(XPV/CPS)가 주는 실시간 정확도는 포기하지만 어떤 하이퍼바이저에도 배포 가능하다.

**VIRT-EUROSYS26-03 | NecoFuzz (EuroSys 2026, CORE P1)** — "fuzz-harness VM"을 합성해 L1 guest hypervisor로 부팅시키고 VMCS/VMCB 상태를 valid/invalid 경계 근처로 생성하는 최초의 nested virtualization 전용 퍼저. Bochs 에뮬레이터에서 추출한 검증 로직을 사용한다. KVM에서 48시간 기준 코드 커버리지 84.7%(Intel)/74.2%(AMD) vs Syzkaller의 61.4%/7.0%. Nested virtualization 인터페이스(VMCS/VMCB)의 정확한 구조와 유효성 제약을 이해하는 데 필요한 저수준 설명을 제공한다.

**VIRT-OSDI26-04 | GOODKIT (OSDI 2026, CORE P1)** — VM introspection을 "hypervisor 특권 스누핑"이 아니라 "guest-to-guest, lock을 존중하는 동시성 문제"로 재정의한다. Observer를 target과 같은 VMM 아래 동작하는 일반 guest VM으로 배치하고, target의 커널 자료구조를 보호하는 lock(spinlock/RWlock/mutex)을 동일하게 획득해 전역 pause 없이 일관된 뷰를 얻는다. LibVMI 대비 최대 110배 introspection latency 개선, 단일 observer 오버헤드 최대 1.06배(LibVMI의 5.15-37.6배 대비). 대가는 lock 기반 일관성 모델(RCU 미지원)과 lock을 impersonate하는 observer가 고장 시 target을 방해할 수 있다는 점이다.

**VIRT-OSDI25-04 | Quantum VM/HyperQ (OSDI 2025, CORE P1)** — 클라우드 양자컴퓨터의 QPU 전체를 하나의 프로그램이 독점하는 문제를, qubit 격자를 하드웨어 topology 단위로 공간 분할하고(qVM 간 버퍼 qubit으로 crosstalk 격리) 배치 내에서는 measurement/reset으로 시간 분할한다. IBM Quantum 대비 처리량 8.4-9.7배(all-at-once 도착), 공간 공유는 충실도(fidelity) 손실이 거의 없으나(L1 거리 0.55 vs 0.55) 시간 공유는 노이즈 비용이 있다(0.64). QRAM이 없어 "context switch"가 원천적으로 불가능하다는, 고전적 가상화 개념이 깨지는 지점을 정확히 보여준다.

**VIRT-SOSP25-15 | Tai Chi (SOSP 2025, CORE P1)** — SmartNIC의 물리 CPU가 데이터플레인(폴링)에 쓰이고 99% 시간 동안 67.5%가 유휴임에도, non-preemptible 컨트롤플레인 루틴(최대 67ms)이 이를 막는 문제를, SmartNIC 네이티브 OS 안에 vCPU를 통합해(별도 게스트 OS 없이) 데이터플레인 유휴 cycle에 컨트롤플레인을 얹는 방식으로 푼다. Type-1/type-2 가상화가 각각 7%/25.9% 데이터플레인 저하를 내는 데 비해 Tai Chi는 0.7%(Alibaba Cloud 프로덕션 SmartNIC, 12코어).

**VIRT-ASPLOS24-01 | DMT (ASPLOS 2024, CORE P1, T1+T2 교차)** — Nested paging의 최대 24-35회 순차 메모리 접근을 코어당 16개 레지스터(VMA→물리 Translation-Entry-Area 매핑)로 1회 참조로 축소한다. pvDMT는 하이퍼콜(KVM_HC_ALLOC_TEA)과 읽기전용 gTEA 테이블로 guest가 자신의 TEA만 참조하도록 격리한다. Nested 가상화에서 shadow paging 오버헤드의 39% 제거(Intel Xeon Gold 6138). 가정: 워크로드가 소수의 크고 정적인 VMA를 가진다는 전제이며, 파편화가 심하면 일반 페이지 워크로 폴백한다.

## 4. Supporting 논문 (P2/P3)

- **VIRT-ATC24-21 (CrossMapping)** — binary translation에서 guest ISA 메모리 일관성 모델을 명세 테이블로 형식화해 최소한의 fence만 삽입. Fence 과다 삽입이 런타임의 최대 84.4%를 차지한다는 수치가 인상적이며, 하드웨어 가상화가 우회하는 문제를 소프트웨어 CPU 가상화가 정면으로 다룬다.
- **VIRT-MIDDLEWARE24-03 (PvCC)** — Xen credit scheduler를 마이크로초 단위 timeslice로 수정해 DPDK poll-mode I/O vCPU와 best-effort 테넌트를 edge 데이터센터에서 공존시킴. Timeslice 길이의 latency-throughput 트레이드오프를 정량화.
- **VIRT-HPDC26-01 / VIRT-HPDC25-03 (부동소수점 가상화 짝)** — trap-and-emulate를 명령어 수준 산술 대체에 적용한 짝 논문. 2025편은 큰 정밀도(임의정밀도/posit), 2026편은 3비트까지 작은 정밀도를 다뤄, "가상화"가 방향과 무관하게 일반화됨을 보여줌.
- **VIRT-OSDI26-12 (mwait-sched)** — 하이퍼스케일 클라우드에서 mwait-passthrough가 oversubscription 하에 물리 코어를 독점하는 "숨은 idle 비용" 문제를 결정론적 timer 기반 idle 에뮬레이션으로 해결. Alibaba 소속 저자의 프로덕션 관찰.
- **VIRT-CCGRID24-04 (vASP)**, **VIRT-SOCC24-06 (Rust KVM)**, **VIRT-ASPLOS26-06 (Arm CCA 명세 불일치)** — confidential computing/hypervisor 신뢰 경계를 다루는 보조 논문들. Arm CCA 편은 "형식 검증된 명세"도 명세 자체의 결함(35건, Arm 확인)에서 자유롭지 않음을 보여줘 T7 브랜치 신뢰 시 반드시 참고할 가치가 있다.
- **VIRT-CCGRID24-05 (워크로드 인식 마이그레이션 호환성 탐지)** — CRIU식 전체 CPU-feature 비교의 과도한 보수성을 워크로드가 실제 쓰는 feature만 분석해 완화, spot 인스턴스 가격 16% 개선.
- **VIRT-ATC24-23 (gVulkan)** — API-remoting 방식 GPU 풀링(레이 트레이싱), MIG/MPS류 인실리콘 파티셔닝과 대비되는 지점.
- **VIRT-SOCC24-04 (SURE)** — Unikraft/QEMU 기반 per-function unikernel로 VM급 격리와 컨테이너급 속도를 노림. 근거는 abstract/intro 수준.
- **VIRT-ASPLOS25-01 (Vela)** — LLM 훈련용 VM이 GPUDirect RDMA passthrough를 유지하기 위해 라이브 마이그레이션과 메모리 오버커밋을 포기해야 하는 구조적 트레이드오프를 프로덕션 규모(약 1500 GPU)에서 보여줌.
- **VIRT-MIDDLEWARE25-02 (Full Trust Alchemist)** — confidential VM의 attestation을 boot-time 측정에서 런타임 정책 기반으로 확장(eBPF/LSM).
- **VIRT-SOSP25-01 (RDMA 디바이스 라이브 마이그레이션)** — device passthrough가 노출한 하드웨어 상태(큐페어, 메모리 등록)를 device-assisted 방식으로 마이그레이션한다는 문제 설정만 확인됨; 구체적 메커니즘은 abstract 수준에서 확인 불가(T4 파일 9절 참고).
- **VIRT-SOSP25-08 (Dandelion)** — POSIX를 버리고 순수 함수형 DAG 프로그래밍 모델을 채택해 게스트 OS 자체를 없앰. Cold start를 89µs(CHERI)까지 낮추지만 상태 유지 워크로드는 원천 배제.
- **VIRT-CCGRID26-01 (TelePod)**, **VIRT-EUROSYS26-06 (SKernel)** — 각각 stateful 컨테이너 라이브 마이그레이션(T4 파일에서 본격 다룸)과 split-kernel 아키텍처(컨테이너 격리 스펙트럼의 세 번째 지점).
- **VIRT-ASPLOS26-02 (gShare)**, **VIRT-ASPLOS26-03 (TEEM³)**, **VIRT-ASPLOS26-17 (CEMU)**, **VIRT-OSDI26-09 (vBOIDs)**, **VIRT-OSDI26-13 (DVLA)** — 각각 서버리스 vGPU 핫플러그, 이종 TEE 간 협력 프로토콜, computational storage 에뮬레이션, 컨테이너 스케줄링 추상화, VM 수명 인식 배치 정책을 다루며 모두 abstract 또는 design 수준 근거.
- **VIRT-HPCA24-06 (LibPreemptible)** — hypervisor의 vCPU 선점 정책과 정확히 대응되는 OS-thread 레벨의 하드웨어 지원(UINTR) 선점 메커니즘. vCPU 하베스팅 정책을 이해하는 데 유용한 유사 사례.
- **VIRT-EUROSYS25-02 (VMR2L)**, **VIRT-OSDI25-02 (Kamino)** — 각각 강화학습 기반 VM 재배치(defragmentation)와 캐시 인식 배치(admission-time)로, VM 라이프사이클의 양 끝에서 파편화를 공격.

## 5. Trade-off 구조

- **Nested virtualization**: 계층 분리(L0/L1/L2)로 얻는 재사용성·보안 경계 → world-switch/EPT 재구성 비용. JANUS/HyperTurtle은 이 비용을 "누가 어떤 이벤트를 처리하는가"를 재배치해 줄이지만, 하드웨어 확장(VMFUNC, #VE, eBPF verifier)에 의존하게 된다.
- **Device passthrough**: 소프트웨어 mediation 비용 제거(네이티브에 가까운 I/O) → 메모리 오버커밋·라이브 마이그레이션이 어려워짐(VIRT-ASPLOS25-01의 Vela가 이를 명시적으로 감수).
- **Guest 투명성 vs 정확도**: 추론 기반 vCPU 노출(EUROSYS25-04)은 guest를 건드리지 않지만 초 단위로 느리고, 파라virtual 노출(XPV/CPS)은 실시간이지만 guest 수정이 필요.
- **형식 검증의 보증 vs 공학 비용**: VeriSMo/Ghost Android 모두 몇 개월~수 년의 증명 노력을 대가로 hypervisor 경계의 특정 불변식을 보증하지만, 검증 범위 밖의 결함(측면채널, 미모델링 예외)은 여전히 남는다.
- **Oversubscription 세분화**: VM 단위(SweetspotVM 이전) → vCPU 단위(SweetspotVM) → 자원별(Coach, T2/T9 교차)로 갈수록 밀도는 오르지만 스케줄러/정책 복잡도가 커진다.
- **Trap-and-emulate 일반화**: 임의의 명령어 수준 의미(부동소수점 정밀도, 메모리 일관성 모델)를 가상화할 수 있지만, 트랩 빈도가 곧 오버헤드가 되어 항상 "트랩을 어떻게 줄이는가"라는 이차 문제를 낳는다(FPVM의 trap short-circuiting, CrossMapping의 최소 fence 삽입).

## 6. 인접 계층과의 관계

- **하드웨어/ISA 아래 계층**: VMX/SVM, VMFUNC, Intel #VE, RISC-V PMP, Arm CCA RMM 등 확장이 이 계층의 토대이며, VIRT-ASPLOS26-06과 VIRT-EUROSYS26-03이 그 확장의 명세·구현 결함을 파고든다.
- **T2 메모리 가상화**: JANUS(VIRT-OSDI26-01)는 GPA→HPA 변환을 L0에 넘기는 방식으로 T1과 T2를 직접 잇는 다리이며, HyperAlloc·Demeter·InfiniDefrag 같은 T2의 핵심 논문들이 EPT/nested-paging 계층을 구체적으로 다룬다. DMT(VIRT-ASPLOS24-01)와 Elastic Translations(VIRT-MICRO24-02)는 T1+T2 교차점에서 nested 주소변환 자체를 가속한다.
- **T4 마이그레이션/체크포인트**: MigCheck(VIRT-EUROSYS26-04)와 CPC(VIRT-ATC24-22)는 이 계층의 vCPU/CPU-feature 상태가 어떻게 이동·검증되는지를 다루며, M3U(VIRT-OSDI26-02)는 CPU 가상화 상태(PML dirty-tracking)를 post-copy 마이그레이션과 연결한다.
- **T5 컨테이너/경량 격리**: LiteShield, SKernel, Dandelion, JANUS의 L2(secure container)가 모두 "hypervisor를 어디까지 유지할 것인가"라는 동일한 스펙트럼 위에 있다.
- **T6 가속기 가상화**: NeuISA(NPU), HyperQ(QPU), Funky(FPGA)는 T1의 CPU 가상화 패턴을 다른 물리 자원에 이식한 직계 사례다.
- **T7 confidential computing**: VeriSMo, Miralis, Ghost Android, Arm CCA 명세 검증이 모두 "hypervisor 경계를 어떻게 신뢰할 수 있게 만드는가"라는 질문을 공유한다.
- **T9 자원관리**: SweetspotVM, Coach, Tai Chi, vBOIDs, DVLA는 이 계층이 제공하는 vCPU/코어 추상화를 스케줄링·배치 정책이 어떻게 소비하는지 보여준다.

## 7. 2024 → 2026 변화

표본이 작아 단정적 추세 주장은 조심스럽지만, 코퍼스에서 관찰되는 패턴은 다음과 같다. 2024년 논문들은 하드웨어-소프트웨어 co-design으로 기존 가상화 병목(nested paging, TLB miss)을 직접 가속하는 데 집중했다(DMT, Elastic Translations, NeuISA). 2025-2026년으로 갈수록 (a) nested virtualization의 "책임 재배치"(JANUS, HyperTurtle)와 "정확성 검증"(NecoFuzz, Ghost Android, Arm CCA 명세 검증)이 늘어나고, (b) CPU가 아닌 자원(QPU, FPGA, SmartNIC)에 동일 가상화 패턴을 이식하는 논문이 증가하는 경향이 보인다. 다만 이는 13개 T1 주 논문과 다수의 보조 논문에 근거한 관찰이며, 연도별 표본 수가 고르지 않아(2026년 다수가 abstract 단계 증거) 확정적 트렌드로 보기는 어렵다.

## 8. 읽는 순서 제안

1. **VIRT-EUROSYS25-04**(vCPU가 실제로 무엇을 숨기는지) → 2. **VIRT-ASPLOS24-01**(DMT, nested paging 비용의 정체) → 3. **VIRT-ATC25-02**(HyperTurtle, nested virtualization 비용의 정체) → 4. **VIRT-OSDI26-01**(JANUS, 그 비용을 재설계) → 5. **VIRT-EUROSYS26-03**(NecoFuzz, nested 인터페이스의 정확한 구조) → 6. **VIRT-OSDI24-04**(VeriSMo)와 **VIRT-SOSP25-04**(Miralis)로 confidential/펌웨어 가상화 확장 → 7. **VIRT-MICRO24-01**(NeuISA)·**VIRT-OSDI25-04**(HyperQ)·**VIRT-SOCC25-05**(Funky)로 비-CPU 자원 가상화 → 8. **VIRT-OSDI26-04**(GOODKIT)로 introspection 패러다임 전환 확인.

## 9. 증거 한계

다음 항목들은 abstract 또는 abstract_intro 수준 근거에 머물러 있어, 메커니즘 세부 사항을 깊이 읽은 것으로 취급하면 안 된다: VIRT-MIDDLEWARE24-01(UTwinVM), VIRT-HPDC26-01(tiny FP), VIRT-ASPLOS26-03(TEEM³), VIRT-ASPLOS26-06(Arm CCA 명세 검증, 다만 버그 수치는 확인됨), VIRT-ASPLOS26-17(CEMU), VIRT-CCGRID26-01(TelePod), VIRT-EUROSYS26-04(MigCheck, 문제의식과 도구 존재는 확인되나 구체적 알고리즘·수치는 미확인), VIRT-EUROSYS26-06(SKernel), VIRT-CCGRID24-04(vASP), VIRT-MIDDLEWARE25-02(Full Trust Alchemist), VIRT-ASPLOS25-01(Vela, ASPLOS 버전은 abstract 수준이며 수치 일부는 겹치는 arXiv 프리프린트에서 인용), VIRT-SOCC24-04(SURE). 특히 **VIRT-SOSP25-01(RDMA 디바이스 라이브 마이그레이션)**은 메커니즘·격리·상태 이전 방식이 모두 "UNKNOWN"으로 기록되어 있으며, 문제 설정만 확인 가능하다 — 이 논문을 인용할 때는 반드시 "구체적 기법은 미확인"이라는 단서를 붙여야 한다. VIRT-OSDI26-12(mwait-sched)는 DESIGN/MEDIUM으로 메커니즘 서술은 있으나 정량적 수치가 캡처되지 않았다.

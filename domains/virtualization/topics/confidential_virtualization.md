# 기밀/보안 격리 (Confidential / Security Isolation)

## 1. 이 계층이 푸는 문제

T7이 다루는 mapping은 다른 topic들과 방향이 다르다. T1-T6은 대체로 "물리 자원을 어떻게 나눌 것인가"를 묻지만, T7은 "그 나눔을 강제하는 계층(하이퍼바이저, 호스트 OS, 클라우드 운영자) 자체를 신뢰하지 않을 때 무엇이 남는가"를 묻는다. Physical Resource(CPU core, DRAM, GPU HBM, PCIe/CXL fabric, NIC)는 그대로지만, Logical Abstraction은 "guest에게 격리된 자원 조각"이 아니라 "host/hypervisor로부터도 격리된, attest 가능한 실행 환경"(confidential VM, enclave, virtual firmware monitor)이 된다. Workload는 멀티테넌트 클라우드에서 실행되는 민감한 연산 — 기밀 VM 내부의 일반 애플리케이션, PCIe 건너편 가속기 위의 AI 추론, 임베디드/펌웨어 수준의 신뢰 루트 — 이다.

이 계층의 핵심 긴장은 CLASSIFICATION_BRIEF가 명시하는 "Translation/Mediation" 축이 뒤집힌다는 데 있다: 보통의 가상화는 hypervisor가 guest를 보호하기 위해 중개하지만, 기밀 컴퓨팅에서는 guest(또는 in-guest 보안 모듈)가 오히려 hypervisor로부터 자신을 보호하기 위해 스스로 중개 계층을 세운다(VIRT-OSDI24-04 VeriSMo, VIRT-EUROSYS25-05 Erebor). 그리고 이 경계가 CPU/DRAM에서 시작해 점점 I/O·PCIe·가속기 쪽으로 확장되는 과정이 이 corpus의 2024→2026 흐름에서 가장 뚜렷하게 관찰되는 변화다(§7).

## 2. Mechanism design space — 신뢰 경계는 어디에 그어지는가

### (a) CPU-only confidential VM (SEV-SNP / TDX / Arm CCA)

이 갈래는 하이퍼바이저를 신뢰 경계 밖으로 밀어내되, guest 내부에 남는 특권 계층(security module, VMPL0 코드)은 여전히 신뢰해야 한다는 문제를 다룬다. VIRT-OSDI24-04(VeriSMo)는 이 특권 in-guest 모듈을 "적대적 하이퍼바이저가 언제든 인터럽트하고 하드웨어 상태를 조작할 수 있다"는 가정 아래 형식적으로 검증한다 — machine-model 레이어(비순차 인터럽션에도 기밀성/무결성이 보존됨을 증명)와 구현 레이어(Rust 소유권 + Verus)로 나눈 결과, unsafe Rust 블록이 32개(AMD/COCONUT SVSM은 150-235개)에 불과하다. VIRT-ATC24-22(CPC)는 기밀 VM의 일상적 유지보수(ballooning, snapshot, live migration)가 firmware-trusted 컴포넌트(AMD Secure Processor)에 의존해 VM 수가 늘수록 선형으로 느려진다는 문제(1 VM 1.92M cycles/VM → 8 VM 39.80M cycles/VM)를, guest 자신이 작성하고 host가 스케줄만 하는 "host-invocable vCPU(hvCPU)"로 해결해 VM 수에 무관한 성능(약 3.29M cycles 고정)을 얻는다. 반대편에는 이 경계를 깨는 공격들이 있다: VIRT-ASPLOS25-02(HyperHammer)는 THP+virtio-mem+vIOMMU라는 hypervisor 편의 기능들의 조합이 guest에게 host 물리 주소 배치를 추론하게 해 Rowhammer로 EPT leaf entry를 직접 조작할 수 있음을 보인다.

### (b) Trusted I/O — enclave/CVM 안에서 I/O 경로까지 신뢰 확장

CPU/메모리만 보호하는 TEE는 데이터가 네트워크나 디스크로 나가는 순간 보호가 끊긴다는 문제를 다루는 갈래다. VIRT-EUROSYS25-18(RAKIS)는 enclave 안에서 XDP/io_uring 링을 직접 구동해, 매 syscall마다 발생하는 enclave exit를 데이터 경로에서 제거한다(iperf3 처리량 Gramine-SGX 대비 4.6배). VIRT-EUROSYS25-05(Erebor)는 한 걸음 더 나가, 기밀 VM이 host hypervisor로부터는 보호되지만 그 안에서 실행되는 서비스 제공자 소프트웨어로부터는 보호되지 않는다는 문제를 다룬다 — attested in-guest monitor가 Intel PKS/CET로 커널을 deprivilege해 두 번째 경계를 만든다. VIRT-ATC25-18(TLS+RA)는 이 신뢰 경로를 원격 클라이언트까지 연결하는 문제 — TLS 핸드셱이 실제로 특정 TEE 안에서 끝난다는 것을 증명 — 를 다루며, attestation report 생성 자체가 AMD SEV-SNP 기준 약 6ms, discrete TPM 기준 약 210ms로 하드웨어 신뢰 루트마다 크게 다르다는 것을 정량화한다.

### (c) Accelerator/PCIe trust boundary — 신뢰 경계를 가속기까지 확장

CPU TEE는 GPU/NPU/FPGA를 보호하지 않는다는 문제를 다루는, 이 corpus에서 가장 최근에 성숙한 갈래다. VIRT-MICRO25-01(ccAI)는 PCIe Security Controller(FPGA 프로토타입)가 모든 PCIe 패킷을 4가지 액션(차단/암호화+무결성/무결성만/투명 통과)으로 분류해, 신뢰 경계를 "TVM → 암호화된 PCIe 전송 → 가속기 실행"으로 재정의한다 — 벤더별 로직 없이 NVIDIA A100/RTX4090Ti/T4, Tenstorrent NPU, Enflame GPU를 동시에 지원하며 Llama-2-7b 기준 종단 지연 오버헤드 0.05-5.67%를 보고한다. VIRT-HPCA24-01(Data Enclave)와 VIRT-HPCA24-02(Salus), VIRT-HPCA24-03(Secure Multi-GPU metadata)은 한발 앞서 "enclave/GPU 메모리 보안 메타데이터 자체가 병목이 된다"는 문제를 다뤘고, VIRT-HPCA26-03(SCALE)은 이를 분산 학습의 NVLink collective communication까지 확장해 GPU TEE 체인의 통신 오버헤드를 co-encryption으로 40-70% 줄인다. VIRT-ASPLOS26-03(TEEM3)는 이 흐름을 일반화해 "이종 ISA/가속기마다 다르게 구현된 TEE들이 매번 bespoke 브리지 없이 상호 협력하는 모델"을 제안한다. 그러나 이 확장에는 대가가 따른다: VIRT-HPCA26-05(DSAssassin)는 Intel Scalable IOV(SIOV)가 마련한 디바이스 단위 격리(공유 DSA 가속기의 DevTLB/Shared Work Queue)가 실제로는 VM 간 covert channel(17.19 Kbps)과 키스트로크 추론(F1 최대 98.4%)을 허용한다는 것을 보여, "가속기까지 신뢰 경계를 넓히면 새로운 공유 하드웨어 구조가 새로운 side channel이 된다"는 반례를 남긴다. VIRT-ASPLOS24-08(Pentimento)는 훨씬 더 아래층에서 같은 교훈을 준다 — FPGA의 논리적 wipe(bitstream 재구성)가 BTI(Bias Temperature Instability)로 인한 아날로그 잔상까지는 지우지 못해, AWS F1 인스턴스 8개 중 5개에서 이전 tenant의 AES 키 전체를 복원할 수 있었다.

### (d) Hypervisor/firmware 정확성 검증

TEE 하드웨어 자체나 그 위의 하이퍼바이저가 "명세대로" 동작하는지를 검증하거나 반증하는 갈래다. VIRT-ASPLOS24-02(MIRVerif)는 소프트웨어 enclave 하이퍼바이저(HyperEnclave)의 Rust 페이지테이블 코드를 15계층 refinement proof로 검증해, 얕은 복사로 guest-제어 메모리를 가리키는 실제 버그 한 건을 잡아낸다. VIRT-SOSP25-03(Ghost in the Android Shell)은 프로덕션 pKVM이 "너무 크고 동시적이어서" 완전 검증이 불가능하다는 현실 속에서, 실행 가능한 테스트-오라클 명세로 5건의 치명적 버그를 찾아낸다(런타임 오버헤드 3.2-11.5배로 실배포 불가). VIRT-ASPLOS26-06(Scope)은 한 걸음 더 나가 "구현이 명세를 따르는가"가 아니라 "명세 자체가 내적으로 일관적인가"를 물어, Arm CCA의 형식 검증된 RMM 명세에서 35건의 이전에 알려지지 않은 버그(모두 Arm이 확인)를 찾는다 — "형식 검증됨 = 버그 없음"이 아니라는 것을 이 corpus에서 가장 날카롭게 보여준다. VIRT-EUROSYS26-03(NecoFuzz, 주 taxonomy T1)은 nested virtualization의 VMCS/VMCB 인터페이스 자체를 퍼징해, 유효/무효 경계 근처의 상태를 생성함으로써 KVM에서 Syzkaller 대비 Intel 1.4배·AMD 11.0배의 커버리지를 낸다.

### (e) Firmware virtualization

펌웨어 자체를 격리 대상으로 삼는 갈래다. VIRT-SOSP25-04(Miralis)는 TEE/기밀 VM 보안 모니터가 수만-수십만 줄의 벤더 펌웨어와 같은 특권 레벨에 있다는 문제를, 6.2k줄 Rust 가상 펌웨어 모니터로 펌웨어를 유저모드로 deprivilege해서 해결한다(trap-and-emulate, RISC-V PMP). VIRT-ATC25-15(μEFI)는 유사한 발상을 UEFI 부팅 모듈에 적용해, 각 모듈을 페이지테이블로 분리된 샌드박스에서 실행한다. VIRT-CCGRID24-04(vASP)는 물리 머신용 Active Security Processor를 VM 생애주기 전체(부팅뿐 아니라 실행·종료까지)로 확장한다. VIRT-MICRO24-04(HyperTEE)는 펌웨어가 아니라 TEE 자체의 관리 평면(attestation, 페이지 할당)을 계산 평면과 물리적으로 분리된 코어로 떼어내, 관리 평면이 공유되며 생기는 controlled-channel 공격을 원천 차단한다.

## 3. 핵심 논문 (P0/P1)

**VIRT-OSDI24-04 | VeriSMo (OSDI 2024, CORE P0, FULL/HIGH).** 기밀 VM의 in-guest 보안 모듈이 적대적 하이퍼바이저의 임의 개입 아래에서도 기밀성·무결성·정보흐름 속성을 유지함을 형식적으로 증명한다. TCB는 unsafe Rust 32개 블록(AMD/COCONUT SVSM 150-235개)뿐이며, UnixBench 오버헤드는 baseline Linux 대비 사실상 0%(Hecate는 40% 저하). 검증 과정에서 AMD SVSM이 놓친 페이지-상태-전환 보안 요구사항을 실제로 찾아냈다.

**VIRT-ATC24-22 | CPC (ATC 2024, CORE P0, FULL/HIGH).** 기밀 VM 유지보수(ballooning, snapshot, live migration)가 firmware-trusted 컴포넌트에 의존해 VM 수에 비례해 느려지는 문제를, guest가 작성하고 host가 스케줄만 하는 host-invocable vCPU(hvCPU)로 해결한다. Live migration을 1.02s(암호화 없는 baseline) 대비 2,025.67s 걸리던 AMD-SP 방식에서 36.24s(CPC)로 55.90배 단축한다. AMD SEV-SNP(VMPL)와 Arm CCA(Confidential Page-Table Isolation, RMM 확장) 양쪽에 모두 이식된 드문 cross-platform 설계.

**VIRT-SOSP25-04 | Miralis (SOSP 2025, CORE P0, DESIGN_EVAL/HIGH).** TEE/기밀 VM 보안 모니터가 벤더 펌웨어 전체와 같은 특권 레벨을 공유한다는 문제를, 6.2k줄 Rust 가상 펌웨어 모니터로 펌웨어를 유저모드로 강등시켜 해결한다. RISC-V Sail 모델 기반 Kani 심볼릭 실행으로 코드베이스 43%를 검증해 개발 중 21개 버그를 찾았다. 빠른 경로 오프로딩(시간 읽기, IPI, remote fence)을 적용하면 Redis/memcached/MySQL 오버헤드가 0-1.2%.

**VIRT-ASPLOS24-02 | MIRVerif (ASPLOS 2024, CORE P1, FULL/HIGH).** Rust의 메모리 안전성이 페이지테이블 설정의 논리적 오류(aliasing, covert mapping)까지 막지는 못한다는 문제를, HyperEnclave의 약 2,130줄 메모리 모듈에 대해 15계층 CCAL 스타일 refinement proof를 적용해 검증한다. 약 3인년의 증명 노력으로 실제 보안 버그(얕게 복사된 페이지테이블이 guest 제어 메모리를 가리킴)를 잡아낸다. Trade-off: 77개 함수 중 49개만 검증됐고 나머지 105개 unsafe 블록은 수동 리뷰에 의존한다.

**VIRT-HPCA24-01 | Data Enclave (HPCA 2024, CORE P1, FULL/HIGH).** 기존 enclave TEE가 데이터 생애주기를 단일 enclave에 묶어 정당한 enclave 간 공유를 느리게 만드는 문제를, 데이터 자체를 별도 암호학적으로 격리된 "data enclave" 객체로 만들어 여러 enclave가 N-to-M attach 관계로 직접 접근하게 한다. 생산자-소비자 간 공유 지연이 scalable SGX 대비 최대 2000배 개선(4KB 메시지, gem5). Trade-off: 메모리 컨트롤러에 32-entry 캐시 구조 등 새 하드웨어가 필요하다.

**VIRT-MICRO24-04 | HyperTEE (MICRO 2024, CORE P1, DESIGN_EVAL/HIGH).** SGX/TDX/SEV 모두 enclave 관리 작업(attestation, 페이지 할당)을 신뢰 불가능한 OS/하이퍼바이저 계층에서 실행해 controlled-channel 공격에 노출된다는 문제를, 관리 서브시스템(EMS)을 계산 서브시스템(CS)과 물리적으로 분리된 코어에 둬서 해결한다. FPGA 프로토타입(TSMC 7nm) 기준 enclave 워크로드 오버헤드 평균 2.0%, SoC 면적 오버헤드 1% 미만.

**VIRT-MICRO24-15 | IvLeague (MICRO 2024, CORE P1, DESIGN_EVAL/HIGH).** SGX류 보안 프로세서가 하나의 전역 무결성 트리를 모든 enclave가 공유해, 자신들이 실제로 공유하는 트리 노드의 타이밍만으로 다른 enclave의 비밀(RSA 개인 지수, 91.6% 정확도로 복원되는 MetaLeak 공격)이 샐 수 있음을 보이고, 이를 4,096개의 고정 크기(64MB) TreeLing으로 물리적으로 분할해 막는다. 최적화(IvLeague-Pro) 적용 시 flat tree 대비 오히려 평균 14% 빠르다.

**VIRT-SOCC24-06 | Securing a Multiprocessor KVM Hypervisor with Rust (SoCC 2024, CORE P1, DESIGN_EVAL/HIGH).** 호스트 Linux 커널이 완전히 손상돼도 VM 기밀성/무결성이 유지되게 하려고, KVM 전체를 재작성하는 대신 EL2에서 실행되는 작은 Rust "Rcore"(safe 3.8K + unsafe 0.2K LOC)만 떼어내 모든 VM exit를 가로챈다. 멀티프로세서에서 Rust의 락 없는 생태계 한계를 극복하기 위해 컴파일 타임에 락 순서를 강제하는 KMutex를 직접 만들었다. 대부분 벤치마크에서 mainline KVM 대비 10% 이내 오버헤드.

**VIRT-ASPLOS25-02 | HyperHammer (ASPLOS 2025, CORE P1, DESIGN_EVAL/HIGH).** "완전한 기능을 갖춘 현대 하이퍼바이저에서 guest가 하드웨어 지원 KVM 메모리 격리를 깰 수 있는가"라는 질문에 그렇다고 답한다. THP가 유출하는 host 물리 주소 하위 21비트, virtio-mem을 이용한 page steering, 그리고 단일측 Rowhammer로 leaf EPT entry를 조작해 임의 host 물리 메모리에 대한 쓰기 권한을 얻는다. 방어책은 virtio-mem 요청 크기 검증 또는 THP/virtio-mem overcommit/VFIO-vIOMMU 비활성화. 공격 자체는 며칠(i3: 192일, Xeon: 137일 기대값)이 걸리는 저확률·장기 공격임을 스스로 명시한다.

**VIRT-EUROSYS25-05 | Erebor (EuroSys 2025, CORE P1, FULL/HIGH).** 기밀 VM이 호스트 하이퍼바이저로부터는 보호되지만, 그 안에서 실행되는 서비스 제공자 소프트웨어(예: LLM 추론 서버)로부터는 보호되지 않는다는 문제를 다룬다. attested Erebor-Monitor가 먼저 부팅되고 Linux 커널을 deprivilege해, 모든 MMU 설정 명령을 Intel PKS로 monitor에 위임한다. 애플리케이션 런타임 오버헤드 기하평균 8.1%(llama.cpp 최악 13.15%). Trade-off: VMPL 기반 파티셔닝(Veil, NestedSGX)만큼 세밀한 격리는 아니다.

**VIRT-MICRO25-01 | ccAI (MICRO 2025, CORE P1, DESIGN_EVAL/HIGH).** 기존 기밀 컴퓨팅(SEV/TDX)이 CPU 측 실행만 보호하고 PCIe 버스를 건넌 데이터는 노출된다는 문제를, PCIe Security Controller가 패킷 단위로 4가지 액션(차단/암호화+무결성/무결성만/투명)을 적용해 해결한다. 벤더 드라이버/애플리케이션 변경이 필요 없고 A100/RTX4090Ti/T4/Tenstorrent NPU/Enflame GPU를 동일 컨트롤러로 지원한다. Llama-2-7b 종단 지연 오버헤드 0.05-5.67%. Trade-off: 새 하드웨어 TCB 컴포넌트(FPGA 프로토타입 218.6K ALUT)를 PCIe 경로에 추가해야 하고, 가속기 펌웨어 무결성을 신뢰 공리로 가정한다.

**VIRT-MIDDLEWARE25-02 | Full Trust Alchemist (Middleware 2025, CORE P1, ABSTRACT/MEDIUM).** 기밀 VM의 attestation이 부팅 시점 측정에만 국한된다는 문제를, eBPF+LSM 훅으로 런타임 보안 이벤트를 정책과 대조하는 계층으로 확장한다. AMD SEV-SNP 위에서 소프트웨어 공급망·멀티테넌트 워크로드에 시연됐으나, 성능 수치는 이 corpus에서 확보되지 않았다.

**VIRT-SOSP25-03 | Ghost in the Android Shell (SOSP 2025, CORE P1, DESIGN_EVAL/HIGH).** 프로덕션 pKVM이 완전 검증하기엔 너무 크고 동시적이라는 문제를, 실행 가능한 함수적 정확성 명세("ghost state" — 유한 부분맵)로 완화한다. 5건의 치명적 버그(4건은 pKVM 개발자가 수정)를 찾았지만, 부팅 3.2배·수기 테스트 11.5배 느려져 그대로 배포할 수는 없다는 것을 스스로 인정한다.

**VIRT-ASPLOS26-04 | WorksetEnclave (ASPLOS 2026, CORE P1, ABSTRACT/MEDIUM).** 서버리스 콜드스타트에서 SGX enclave의 시작 지연과 EPC(Enclave Page Cache) 소비가 특히 가혹하다는 문제를, enclave가 실제로 건드린 EPC 페이지 작업집합만 스냅샷/복원하는 방식으로 해결한다. Gramine·Occlum 두 LibOS 모두에 이식돼 시작 시간 1.9-54배 개선을 보고하나(abstract 수준), 세부 벤치마크 조건은 확인되지 않는다.

**VIRT-ASPLOS26-06 | Scope (ASPLOS 2026, CORE P1, ABSTRACT/MEDIUM).** "구현이 명세를 따르는가"가 아니라 "명세 자체가 내적으로 일관적인가"를 물어, Arm CCA의 형식 검증된 RMM 명세를 Verus/SMT로 기계 검증 가능한 모델로 변환하고 규칙 기반 일관성 검사를 적용한다. 35건의 이전에 알려지지 않은, Arm이 모두 확인한 버그(ABI 의미론, 누락된 상태 전이 포함)를 찾아 "형식 검증됨"이 곧 "버그 없음"이 아님을 이 corpus에서 가장 명확히 보여준다.

**VIRT-HPCA26-03 | SCALE (HPCA 2026, CORE P1, ABSTRACT/MEDIUM).** NVIDIA Confidential Computing(CVM이 GPU TEE로 연결됨)이 분산 학습의 collective communication에서 암호화/인증 지연을 특히 심하게 지불한다는 문제를, 유휴 GPU 컴퓨트로 암호화/인증을 오프로드·병렬화해 완화한다. 4개 HGX H100/H200 클러스터 실제 ML 워크로드 기준 통신 관련 보안 오버헤드 40-70% 감소.

**VIRT-HPCA26-05 | DSAssassin (HPCA 2026, CORE P1, ABSTRACT/HIGH).** Intel Scalable IOV(SIOV)가 디바이스 단위 중개로 cross-tenant 위협을 막는다고 여겨졌던 Data Streaming Accelerator(DSA)의 Device TLB와 Shared Work Queue가 실제로는 프로세스/VM 간 격리되지 않음을 리버스엔지니어링으로 밝힌다. covert channel 17.19 Kbps(오류율 4.64%, 기존 최고 대비 5배 빠르고 4배 정확), 웹사이트 핑거프린팅 85.7% 정확도, 키스트로크 추론 F1 최대 98.4%. "디바이스 가상화가 격리를 보장한다"는 가정에 대한 이 corpus의 가장 강력한 반례.

**VIRT-EUROSYS26-03 | NecoFuzz (EuroSys 2026, CORE P1, FULL/HIGH, 주 taxonomy T1).** nested virtualization(L0/L1/L2)의 VMCS/VMCB 인터페이스 자체를 체계적으로 퍼징한 최초 사례로, Bochs 에뮬레이터에서 추출한 검증 로직으로 "유효/무효 경계 근처"의 상태를 생성한다. KVM에서 Syzkaller 대비 Intel 코드커버리지 1.4배(84.7% vs 61.4%), AMD 11.0배(74.2% vs 7.0%) 개선. JANUS(T1) 같은 nested-virt CORE 논문이 딛고 선 낮은 수준의 검증 인프라를 제공한다.

**VIRT-OSDI26-04 | Inside Out / GOODKIT (OSDI 2026, CORE P1, DESIGN_EVAL/HIGH, 주 taxonomy T1).** 기존 VM introspection(LibVMI류)이 타깃 VM을 통째로 멈춰야 일관된 뷰를 얻어 5.15-37.6배 느려진다는 문제를, observer를 타깃과 같은 VMM 아래의 별도 guest VM으로 만들고 타깃 커널 자료구조를 보호하는 락을 관찰자도 똑같이 획득(lock-aware coherence)하게 해서 해결한다. 단일 observer 오버헤드는 OpenSSL 기준 최대 1.06배(LibVMI는 5.15-37.6배). 신뢰 경계 설계라는 점에서 T7과 강하게 겹친다 — 관찰자가 하이퍼바이저에 내장되지 않아 TCB가 커지지 않고, 타깃과도 격리된다.

## 4. Supporting 논문 (P2/P3)

- **VIRT-EUROSYS25-18 RAKIS (P2, CORE)**: enclave 프로그램이 매 syscall마다 enclave exit를 내는 문제를, XDP/XSK 링과 io_uring을 enclave 안에서 직접 구동하는 ~2 KLoC FastPath Module로 해결한다. "RAKIS-certified rings"로 신뢰 인덱스 사본을 enclave 메모리에 유지하며 매 접근을 bounds-check한다. Gramine-SGX 대비 UDP 처리량 4.6배. Trade-off: 데이터 기밀성/무결성 자체는 TLS/터널에 위임하고, TCP 스택은 여전히 호스트 커널에 남는다.
- **VIRT-ASPLOS24-08 Pentimento (P2, SUPPORT)**: FPGA의 논리적 wipe가 BTI 아날로그 잔상까지는 지우지 못해 AWS F1의 8개 인스턴스 중 5개에서 AES 키 전체를 복원. "logical reset = isolation"이라는 가정에 대한 반례.
- **VIRT-CCGRID24-04 vASP (P2, CORE)**: 물리 머신용 Active Security Processor를 VM 전체 생애주기(부팅뿐 아니라 실행·종료)로 확장. 성능 수치는 확보되지 않음.
- **VIRT-HPCA24-02 Salus (P2, SUPPORT)**: GPU HBM과 CXL 확장 메모리 사이 페이지 이동 시 재암호화 비용(최대 2.04배 저하)을 영구 주소 기반 암호화로 제거.
- **VIRT-HPCA24-03 Secure Multi-GPU metadata (P2, SUPPORT)**: GPU 간 인터커넥트 보안 오버헤드(19.5%)를 통신 패턴 인식 동적 pad-table 할당으로 7.9%까지 절감.
- **VIRT-HPCA24-05 Quantum Computer TEE (P2, CORE)**: 아날로그 제어 펄스라는 암호화 불가능한 대상에 TEE 개념을 확장한 독특한 사례.
- **VIRT-MIDDLEWARE24-05 sMVX (P2, SUPPORT)**: 민감한 코드 경로만 이중 실행해 메모리 손상 공격을 탐지, 전체 프로그램 MVX 대비 CPU 20%·메모리 49% 절감.
- **VIRT-MIDDLEWARE24-10 Privagic (P2, SUPPORT)**: 명시적 secure type으로 멀티스레드 C/C++를 SGX enclave와 비enclave로 자동 분할.
- **VIRT-ATC25-15 μEFI (P2, CORE)**: UEFI 부팅 모듈을 페이지테이블 격리 샌드박스에서 실행. 6-모듈 기준 부팅 오버헤드 1.91%.
- **VIRT-ATC25-18 TLS+RA (P2, SUPPORT)**: TLS 핸드셱에 attestation을 직접 결합. attestation 생성 시간이 AMD SEV-SNP ~6ms부터 discrete TPM ~210ms까지 하드웨어 신뢰 루트에 따라 크게 갈린다는 것을 정량화.
- **VIRT-MIDDLEWARE25-12 MVTEE (P2, SUPPORT)**: N개의 다변화된 모델 추론 변형을 각각 다른 TEE(SGX/TDX 혼합 가능)에서 실행하고 별도 monitor TEE가 투표. "TEE는 platform owner로부터는 보호하지만 enclave 내부 소프트웨어 버그로부터는 보호하지 않는다"는 것을 명시적으로 보여준다.
- **VIRT-SOCC25-19 Scylla (P2, SUPPORT)**: enclave 기반(SGX)과 VM 기반(SEV-SNP/TDX/Nitro) 기밀 컴퓨팅을 apples-to-apples로 비교. PHE > SGX > SEV ≈ Nitro ≈ TDX 순으로 성능 순위 제공.
- **VIRT-ASPLOS26-03 TEEM3 (P2, CORE)**: 이종 ISA/가속기별 TEE를 bespoke 브리지 없이 협력시키는 core-independent TEE 모델. ccAI가 다른 각도에서 마주친 문제(가속기 신뢰 확장)의 일반화.
- **VIRT-ASPLOS26-05 Trust-V (P2, SUPPORT)**: TEE의 실행 시 무결성 보장이 at-rest(sealed) 데이터 무결성까지 포함하지 않는다는 흔한 오해를 지적. 보호된 I/O 경로에 최대 3.86배 오버헤드.
- **VIRT-EUROSYS26-20 TrustWeave (P2, SUPPORT)**: TDX의 부팅시 attestation을 IMA+Runtime Measurement Register로 확장해, 멀티클라우드 LLM 에이전트가 런타임에 동적으로 로드하는 컴포넌트까지 측정.
- **VIRT-EUROSYS26-21 TZ-LLM (P3, SUPPORT, ABSTRACT_INTRO/LOW)**: 온디바이스 LLM 가중치를 Arm TrustZone secure world에 보호. 근거가 abstract-intro 수준으로 가장 얇다(§9).
- **VIRT-ASPLOS24-09 LLC side channel (P2, SUPPORT, 주 taxonomy T9)** / **VIRT-ASPLOS24-10 Co-location attacks (P2, SUPPORT, 주 taxonomy T8)**: 클라우드가 "격리는 추상화만으로 충분하다"고 가정한 지점(캐시 공유, 배치 불투명성)이 실제로는 깨진다는 것을 실증 — CORE 격리 메커니즘이 왜 필요한지의 배경.
- **VIRT-MICRO24-16 Veiled Pathways (P2, SUPPORT, 주 taxonomy T6)**: GPU MPS/MIG가 compute/cache/memory controller는 파티션하지만 "uncore"(DRAM 주파수 스케일링, 코덱 엔진, PCIe 링크)는 파티션하지 않아 발생하는 covert channel. MIG의 물리 인스턴스 격리조차 공유 PCIe 링크로 우회된다(6.8 kbps, root 불필요).
- **VIRT-SOSP25-11 CHERIoT RTOS (P2, SUPPORT, 주 taxonomy T10)** / **VIRT-SOSP25-12 TickTock (P2, SUPPORT, 주 taxonomy T10)**: 각각 capability 기반과 MPU 기반 임베디드 격리의 정확성 문제를 다뤄, T7의 검증 계보(MIRVerif, VeriSMo, Scope)와 나란히 놓인다.

## 5. Trade-off 구조

**(1) 신뢰 경계를 좁힐수록(하이퍼바이저 제외) 남은 특권 계층의 검증 부담이 커진다.** CVM은 하이퍼바이저를 신뢰 경계 밖으로 밀어내지만, 그 결과 in-guest 보안 모듈(VMPL0 코드, 펌웨어)이 새로운 단일 장애점이 된다. VIRT-OSDI24-04(VeriSMo)와 VIRT-SOSP25-04(Miralis)는 이 모듈을 형식 검증/deprivilege로 작게 만들어 이 부담을 갚으려 하고, 그 대가는 검증 시간(VeriSMo: 32코어에서 6분)과 트랩 빈도에 비례하는 런타임 비용(Miralis: fast-path 없이 IOzone 10.6%)이다.

**(2) 유지보수 편의 기능 ↔ 새로운 공격 표면.** THP, virtio-mem, vIOMMU 같은 하이퍼바이저 편의 기능은 밀도와 I/O 성능을 위해 존재하지만, VIRT-ASPLOS25-02(HyperHammer)가 보이듯 정확히 그 편의 기능이 guest에게 host 물리 배치를 추론하게 하는 채널이 된다. VIRT-ATC24-22(CPC)는 반대로 "유지보수 자체를 guest-trusted 코드로 옮기면" 이 긴장이 줄어든다는 것을 보여, 같은 문제(CVM 유지보수)에 대한 두 가지 다른 답을 corpus 안에 남긴다.

**(3) 신뢰 경계를 CPU 밖으로 확장할수록(§7) 새로운 공유 하드웨어 구조가 새로운 side channel이 된다.** VIRT-MICRO25-01(ccAI)가 PCIe까지 신뢰를 확장하면, VIRT-HPCA26-05(DSAssassin)가 보이듯 그 확장에 쓰인 공유 메커니즘(SIOV의 DevTLB/SWQ) 자체가 새로운 covert channel이 된다. VIRT-MICRO24-16(Veiled Pathways)의 GPU uncore, VIRT-ASPLOS24-08(Pentimento)의 FPGA 아날로그 잔상도 동일한 패턴 — "파티션한 자원은 안전하지만 파티션 밖에 남은 공유 구조는 안전하지 않다."

**(4) 형식 검증 ↔ 실배포 가능성.** VIRT-ASPLOS24-02(MIRVerif)의 3인년, VIRT-SOSP25-03(Ghost in Android Shell)의 3.2-11.5배 런타임 오버헤드가 보여주듯, 이 계층에서 "완전히 검증됨"과 "프로덕션에 배포 가능함" 사이에는 항상 간극이 있다. VIRT-ASPLOS26-06(Scope)은 이 간극을 한 단계 더 깊게 파고들어, 검증된 명세 자체도 틀릴 수 있다는 것을 보여 "검증"이라는 단어가 주는 안도감에 정면으로 반박한다.

## 6. 인접 계층과의 관계

- **T1(CPU 가상화) 아래로**: VIRT-ASPLOS25-02(HyperHammer)와 VIRT-SOSP25-03(Ghost)이 KVM/pKVM의 EPT 격리를, VIRT-EUROSYS26-03(NecoFuzz)와 VIRT-OSDI26-04(GOODKIT)이 각각 nested virtualization 인터페이스와 VM introspection의 신뢰 경계를 다뤄 T1과 직접 겹친다.
- **T2(메모리 가상화)와의 다리**: VIRT-ASPLOS24-02(MIRVerif)와 VIRT-ASPLOS25-02(HyperHammer)가 모두 EPT/nested paging이라는 T2의 핵심 메커니즘이 T7의 신뢰 경계이기도 하다는 것을 보인다.
- **T3(I/O 가상화)와의 다리**: VIRT-MICRO25-01(ccAI), VIRT-EUROSYS25-18(RAKIS), VIRT-HPCA26-05(DSAssassin), VIRT-EUROSYS24-04(S-NIC, 주 taxonomy T3)가 이 문서의 "trusted I/O"·"accelerator trust boundary" 갈래와 T3의 SmartNIC/scalable-IOV 갈래를 직접 잇는다(자세한 내용은 I/O 가상화 문서 참고).
- **T5(컨테이너 격리) 위로**: VIRT-EUROSYS26-18(Pyramid), VIRT-EUROSYS25-17(CKI), VIRT-EUROSYS25-05(Erebor 자체도 LibOS 기반)가 T5의 경량 격리 기법을 T7의 신뢰 경계 안에 재적용한다(자세한 내용은 컨테이너 격리 문서 참고).
- **T6(가속기 가상화)와의 다리**: VIRT-HPCA24-02(Salus), VIRT-HPCA24-03, VIRT-MICRO24-16(Veiled Pathways)이 GPU 가상화(MIG/MPS)의 보안 측면을 다뤄, T6의 가속기 공유 메커니즘이 T7의 새로운 공격 표면이 되는 경로를 보여준다.
- **T9(자원관리)와의 다리**: VIRT-ASPLOS24-09, VIRT-ASPLOS24-10이 각각 LLC와 FaaS 배치 불투명성을 공격해, 멀티테넌시(T9)가 격리(T7) 없이는 안전하지 않다는 것을 실증한다.

## 7. 2024 → 2026 변화 — 신뢰 경계는 정말 CPU/DRAM에서 I/O·PCIe·가속기로 확장되는가

이 corpus의 증거는 이 방향성을 상당히 명확하게 뒷받침한다.

**2024년**: 압도적으로 CPU/DRAM 중심이다 — VeriSMo(CVM 보안 모듈), CPC(CVM 유지보수), MIRVerif(enclave 페이지테이블), HyperTEE(enclave 관리 평면), IvLeague(무결성 트리), Rcore(KVM). GPU 쪽으로의 확장은 있었지만(Salus, Secure Multi-GPU) 이는 "기밀 컴퓨팅 경계 확장"이 아니라 "GPU 메모리 암호화 자체의 성능 비용"을 다루는 SUPPORT 논문들로, 아직 CPU TEE와 GPU를 하나의 신뢰 체인으로 묶지는 않았다.

**2025년**: 경계가 I/O로 처음 넘어간다. RAKIS(enclave 안에서 커널 우회 I/O), Erebor(CVM 내부의 두 번째 경계), TLS+RA(원격 클라이언트까지 attestation 연결)가 모두 "CPU TEE의 경계를 그 바깥의 데이터 경로로 늘리는" 시도다. 그리고 결정적으로 ccAI(MICRO 2025)가 처음으로 신뢰 경계를 PCIe 트랜짓을 통해 GPU/NPU/FPGA까지 명시적으로 확장한다 — "TVM → 암호화된 PCIe → 가속기 실행"이라는 체인을 하나의 시스템으로 구현한 corpus 내 첫 사례다.

**2026년(초기 문헌)**: 이 확장이 일반화되고 동시에 그 대가가 드러난다. TEEM3가 "이종 가속기 TEE를 어떻게 일반적으로 조합할 것인가"를 아키텍처 문제로 승격시키고, SCALE이 GPU TEE 체인을 다중 GPU NVLink collective communication까지 확장한다. 동시에 DSAssassin이 바로 그 확장에 쓰인 공유 메커니즘(Intel Scalable IOV)이 새로운 cross-VM covert channel이 된다는 것을 실증해, "경계 확장 = 새 공격 표면"이라는 균형추를 corpus에 처음 명시적으로 남긴다.

따라서 **CPU/DRAM → I/O(2025) → PCIe/가속기(2025 말-2026)**라는 확장 방향은 ccAI → TEEM3/SCALE의 계보와 RAKIS → Erebor → TLS+RA의 계보로 비교적 뚜렷하게 뒷받침된다. 다만 표본 크기에 대한 유보가 필요하다: 이 방향성을 직접 보여주는 논문은 연도당 2-4편 수준(2024: 0-1편, 2025: 3편, 2026: 3편)에 불과하고, 2026년 항목 다수가 abstract 수준 근거(TEEM3, SCALE, DSAssassin은 ABSTRACT/ABSTRACT-HIGH)에 머물러 있다. "확장되고 있다"는 방향 자체는 corpus 안에서 일관되지만, 그 속도나 폭까지 정량적으로 일반화하기에는 표본이 작다는 점을 밝혀둔다.

## 8. 읽는 순서 제안

1. **VIRT-OSDI24-04 (VeriSMo)** — 기밀 VM의 in-guest 보안 모듈이 무엇을 증명해야 하는지부터 이해한다.
2. **VIRT-ATC24-22 (CPC)** — 그 모듈이 실제로 해야 하는 일(유지보수)과 그 비용.
3. **VIRT-ASPLOS25-02 (HyperHammer)** — 같은 경계(EPT, virtio-mem)가 공격받으면 무엇이 깨지는지.
4. **VIRT-SOSP25-04 (Miralis)** — 신뢰 경계를 한 단계 더 아래(펌웨어)로 내리는 사례.
5. **VIRT-EUROSYS25-18 (RAKIS)** → **VIRT-EUROSYS25-05 (Erebor)** — 신뢰 경계가 I/O와 enclave 내부로 넓어지는 과정.
6. **VIRT-MICRO25-01 (ccAI)** — 신뢰 경계가 PCIe를 건너 가속기로 넘어가는 결정적 지점.
7. **VIRT-HPCA26-05 (DSAssassin)** — 그 확장이 만들어내는 새 공격 표면.
8. **VIRT-ASPLOS26-06 (Scope)** — "형식 검증됨"의 한계로 마무리.
9. (선택) **VIRT-SOSP25-03 (Ghost in the Android Shell)**과 **VIRT-EUROSYS26-03 (NecoFuzz)** — 검증/퍼징 인프라 자체에 관심 있다면.

## 9. 증거 한계

다음 문헌은 abstract 또는 abstract-intro 수준 근거에 머물러 있어 메커니즘 세부나 수치를 깊이 검증된 것으로 취급하면 안 된다: VIRT-MIDDLEWARE25-02(Full Trust Alchemist), VIRT-ASPLOS26-04(WorksetEnclave), VIRT-ASPLOS26-06(Scope), VIRT-ASPLOS26-03(TEEM3), VIRT-ASPLOS26-05(Trust-V), VIRT-EUROSYS26-20(TrustWeave), VIRT-HPCA26-03(SCALE), VIRT-HPCA26-05(DSAssassin — confidence는 HIGH이나 evidence depth는 ABSTRACT). 특히 **VIRT-EUROSYS26-21(TZ-LLM)**은 evidence depth가 ABSTRACT_INTRO/LOW로 이 corpus 안에서 가장 근거가 얇다 — state_mechanism과 overhead_bottleneck이 모두 확인되지 않았고, trade-off 문장조차 "abstract가 이 지점에서 잘렸다"고 스스로 명시하고 있다. VIRT-CCGRID24-04(vASP)도 overhead_bottleneck이 UNKNOWN으로 남아 있다. 2026년 항목 다수가 이 얕은 근거 수준에 몰려 있다는 점은 §7의 추세 주장에도 그대로 적용되는 유보 사항이다.

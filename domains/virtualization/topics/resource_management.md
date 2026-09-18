# Resource Management / Multi-tenancy (T9)

## 0. 먼저 짚어야 할 구조적 사실

T9는 primary 14편, secondary 63편이다. 이 비율 자체가 하나의 발견이다: **T9는 대부분 다른 논문의 "부차적" 관심사다.** 더 정확히 말하면, T9로 primary 분류된 14편 중 CORE는 단 1편(VIRT-MICRO24-17 Mosaic)뿐이고 나머지 13편은 전부 SUPPORT다. 반대로 이 corpus에서 진짜 CORE 급 자원관리 메커니즘(CXL 메모리 티어링의 Memstrata, VM CPU 오버서브스크립션의 SweetspotVM, vCPU 추상화 정확성, SmartNIC 멀티테넌시의 OSMOSIS, FPGA/GPU 가상화의 Coyote v2·LithOS 등)은 모두 **T1(CPU)·T2(메모리)·T3(I/O)·T6(가속기)를 primary로 갖고 T9를 secondary로만 갖는다.** 즉 "자원관리"는 거의 항상 이미 존재하는 가상화 메커니즘 위에 얹히는 정책 계층이며, 독자적으로 CORE 가상화 기여를 만드는 경우는 드물다. 이 파일은 이 구조를 그대로 따라, T9-primary 14편보다 T9-secondary 중 CORE인 논문들을 중심으로 서술한다.

## 1. 이 계층이 푸는 문제

Physical Resource → Logical Abstraction → Workload 사슬에서 T9는 "이미 만들어진 논리적 자원 단위(vCPU, VM, 가상 디스크, vGPU 슬라이스, virtual switch port)를 실제로 몇 개의 물리 자원에, 어떤 순서로, 얼마나 겹치게 배치할 것인가"를 다룬다. CORE 가상화 논문이 "추상화를 어떻게 만들 것인가"를 답한다면, T9는 "그 추상화를 어떻게 스케줄링/배치/오버서브스크립션할 것인가"를 답한다. 이 둘은 독립적이지 않다 — 예컨대 MIG가 존재하지 않았다면 GPU 배치 스케줄러(ParvaGPU, KACE)도 존재할 수 없고, guest-physical 메모리 가상화가 없었다면 CXL 메모리 티어링(Memstrata, Coach, Demeter)도 정의될 수 없다. T9의 존재 이유는 정확히 이 지점이다: **가상화 메커니즘 하나만으로는 활용률이 나오지 않는다. 그 위에 배치·오버서브스크립션·QoS 정책이 반드시 필요하다.**

## 2. Mechanism design space

**파티셔닝(partitioning)**: 물리 자원을 고정된 경계로 나누는 방식. VIRT-MICRO24-17(Mosaic)은 서버리스 오버서브스크립션 환경에서 L2/L2-TLB/LLC/BTB/분기예측기를 함수별 태그된 "타일"로 하드웨어 파티션해 컨텍스트 스위치 후에도 상태를 보존한다(p99 tail latency 74.6% 감소, 코어 저장공간 1.06% 오버헤드). VIRT-OSDI24-02(Memstrata/CXL 메모리 티어링)는 page coloring으로 로컬 DRAM 라인을 VM별로 분리해 "noisy neighbor"의 480% tail latency 폭증을 6% 미만으로 억제한다. 파티셔닝의 근본 장점은 격리가 하드웨어에 의해 보장된다는 것이고, 근본 단점은 재구성이 비싸고(draining 필요) 파티션 크기가 이산적이라 파편화가 생긴다는 것이다.

**오버서브스크립션(oversubscription)**: 물리 자원보다 많은 논리 자원을 할당하고 통계적으로 겹치지 않기를 기대하는 방식. VIRT-CCGRID24-01(SweetspotVM)은 VM 전체가 아니라 개별 vCPU 단위로 오버서브스크립션 비율을 다르게 설정해(같은 VM 안에서도 vCPU마다 활용률이 크게 다르다는 프로덕션 데이터에 기반) 호스팅 비용을 1/3로 줄이면서 비오버서브스크립션 수준의 성능을 유지한다. VIRT-ASPLOS25-12(Coach)는 CPU뿐 아니라 CPU·메모리·네트워크·스토리지 네 자원 모두를 "보장 할당 + 오버서브스크립션 할당"으로 나누고, VM들의 상보적인 일일 피크 패턴을 이용해 최대 26% 더 많은 VM을 수용한다. 오버서브스크립션의 근본 장점은 활용률이지만, 근본 단점은 예측이 틀렸을 때의 SLO 위반 위험이며 이 위험은 명시적으로 가격에 반영되거나(Coach는 할인된 VM 타입으로 판매) 실시간 완화 메커니즘(페이지 트리밍, live migration)으로 관리되어야 한다.

**간섭 인지 배치(interference-aware placement)**: 이미 실행 중인 워크로드들을 어떻게 재배치할지 결정하는 방식. VIRT-EUROSYS25-02(VMR2L)는 강화학습으로 VM 재배치 결정을 MIP의 50분에서 1초로 줄이면서 최적해의 2.86% 이내에 도달한다. VIRT-OSDI25-02(Kamino)는 VM 할당 요청을 캐시 적중률이 높을 것으로 예측되는 할당 에이전트로 라우팅한다. VIRT-OSDI26-13(DVLA)은 VM 수명 예측을 기반으로 "placement debt"(장기 VM이 섞여 영영 비워지지 않는 머신)를 최소화한다. 이들은 모두 live migration을 "공짜 도구"가 아니라 예산이 정해진 희소 자원으로 다룬다(DVLA: 알리바바 프로덕션에서 하루 평균 810건의 migration, ~40%의 VM은 구조적으로 migration 불가능).

**QoS 강제(enforcement)**: 물리 디바이스 수준에서 공정성/우선순위를 하드웨어·소프트웨어로 강제하는 방식. VIRT-ATC24-06(OSMOSIS)은 SmartNIC 처리 유닛에 Weight-Limited Borrowed Virtual Time과 Physical Memory Protection을 적용해 최대 83% 공정성 개선을 이룬다. VIRT-ATC24-04(PeRF)는 RDMA managed-QP verbs로 하드웨어 변경 없이 소프트웨어만으로 16KB 단위 preemption을 만든다. VIRT-SOSP25-15(Tai Chi)는 SmartNIC OS 내부에 vCPU/pCPU 하이브리드 풀을 통합해 데이터 평면 오버헤드를 type-1(7%)/type-2(25.9%) 가상화 대비 0.7%로 낮춘다. VIRT-OSDI26-12(mwait-sched)는 idle vCPU가 물리 코어를 mwait-passthrough로 독점하는 "숨은 유휴 비용"을 결정론적 타이머 기반 에뮬레이션으로 해결한다.

이 네 축은 서로 배타적이지 않고 조합된다: OSMOSIS는 파티셔닝(FMQ)과 QoS 강제(WLBVT)를 함께 쓰고, Coach는 파티셔닝(guaranteed 부분)과 오버서브스크립션(elastic 부분)을 명시적으로 결합한다.

## 3. 핵심 논문 (P0/P1) — 대부분 T1/T2/T3가 primary인 CORE 논문들

**VIRT-MICRO24-17 (Mosaic, MICRO 2024, CORE P1, T9 primary)**: 유일하게 T9가 primary인 CORE 논문. 서버리스 함수가 작아서(평균 LLC footprint 2.9MB, 가용 15MB) 오버서브스크립션이 필연적인데, 잦은 컨텍스트 스위치가 마이크로아키텍처 상태를 파괴하는 문제를 하드웨어 태그된 "타일"로 해결한다. p99 latency 74.6% 감소, 지속가능 처리량 225% 개선, 저장 오버헤드는 코어의 1.06%. GPU MIG/vGPU 파티셔닝의 CPU 하드웨어 버전이라 할 수 있다.

**VIRT-OSDI24-02 (CXL 메모리 티어링/Memstrata, OSDI 2024, CORE P0, T2 primary)**: Intel Flat Memory Mode가 로컬 DRAM/CXL을 64B 라인 단위로 투명하게 섞을 때, 서로 다른 VM의 페이지가 같은 로컬 메모리 "라인"에서 충돌해 최악 480% tail latency 폭증(Redis p95)을 일으킨다는 것을 발견하고, page coloring으로 VM이 자기 자신하고만 충돌하게 만든다. 6-VM 멀티테넌트 설정에서 최악 슬로우다운을 35%→6% 미만으로 낮춘다. CXL 디스어그리게이션이 왜 "가상화"가 아니라 그 위에 격리 메커니즘을 더해야 진짜 멀티테넌트에 쓸 수 있는지 보여주는 사례.

**VIRT-CCGRID24-01 (SweetspotVM, CCGrid 2024, CORE P1, T1 primary)**: VM 단위가 아니라 개별 vCPU 단위로 오버서브스크립션 비율을 다르게 설정한다는, 놀랍도록 단순하지만 프로덕션 데이터(OVHcloud)에 기반한 통찰. 호스팅 비용을 1/3로 줄이면서 비오버서브스크립션 성능을 유지. 오버서브스크립션의 "전부 아니면 전무" 관행이 왜 최적이 아닌지 정량적으로 보여준다.

**VIRT-EUROSYS25-04 (vCPU 정확한 추상화, EuroSys 2025, CORE P1, T1 primary)**: vCPU는 CPU가 아니다 — 용량이 다르고(steal time), 예측 불가능하게 preemption되며(수 ms), 하이퍼바이저가 바꾼 토폴로지 위에 있다. 세 가지 유저스페이스 프로버(vcap/vact/vtop)로 하이퍼바이저 수정 없이 이 진실을 추론해 guest 스케줄러에 반영한다. Tailbench 95th percentile latency가 preemption latency 증가에 따라 20배까지 증가함을 보이며, 캡처된 정보로 32% 처리량 개선을 달성. "vCPU가 실제로는 무엇인지"에 대한 이 corpus 최고의 설명.

**VIRT-ATC24-06 (OSMOSIS, ATC 2024, CORE P1, T3 primary)**: on-path SmartNIC에서 여러 테넌트의 패킷 처리 커널을 공정하게 스케줄링하는 하드웨어+소프트웨어 통합 설계. Flow Management Queue와 WLBVT로 최대 83% 공정성 개선, 63% flow completion time 감소를 달성한다. 하이퍼바이저가 vCPU/DRAM을 멀티플렉싱하는 것과 정확히 같은 패턴을 프로그래머블 NIC에 적용한 사례.

**VIRT-ATC24-04 (PeRF, ATC 2024, CORE P2, T3 primary)**: RDMA는 원래 단일 테넌트 HPC용으로 설계되어 멀티테넌트 클라우드에서 대역폭 폭주 테넌트가 소규모 메시지 테넌트를 굶길 수 있다. RNIC 펌웨어 변경 없이 host driver에서 ENABLE/WAIT 제어 WR로 16KB 단위 preemption을 구현해 근접 bare-metal 처리량과 작업보존적(work-conserving) 격리를 동시에 얻는다.

**VIRT-SOSP25-02 (Demeter, SOSP 2025, CORE P1, T2 primary)**: 하이퍼바이저는 권한이 있지만 guest의 접근 의미론을 볼 수 없고, guest는 의미론을 알지만 티어 배치 권한이 없다는 "고전적 메모리 가상화 딜레마"를 guest delegation으로 해결한다 — 페이지 hot/cold 분류를 guest 커널에 위임하고 하이퍼바이저는 용량 중재만 담당한다.

**VIRT-OSDI26-05 (Blowfish, OSDI 2026, CORE P1, T2 primary)**: Demeter와 대비되는 접근으로, guest 측 hotness 추적(Fair MGLRU + Subpage Tracker로 THP의 "unfair hotness"/"hot bloat" 문제 해결)과 host 측 데이터 이동(EPT 조작만으로 RDMA far memory에 회수, guest/IO page table은 건드리지 않음)을 분리한다. Reclaim/restore latency를 HyperAlloc 대비 53-60% 낮춘다. VM 메모리 오버커밋 메커니즘이 RDMA 디스어그리게이션 메모리로 어떻게 확장되는지 보여주는 최신 사례.

**VIRT-SOSP25-15 (Tai Chi, SOSP 2025, CORE P1, T1 primary)**: SmartNIC 자체를 가상화 호스트로 만든다. 데이터 평면 물리 CPU와 제어 평면 vCPU를 SmartNIC 네이티브 OS 안에 통합해, type-1(7%)/type-2(25.9%) 가상화 대비 데이터 평면 오버헤드를 0.7%로 낮춘다. DPU가 "가상화의 대상"에서 "가상화를 수행하는 주체"로 바뀌는 지점.

**VIRT-OSDI26-12 (mwait-sched, OSDI 2026, CORE P1, T1 primary)**: mwait-passthrough(거의 bare-metal급 idle 성능)가 1:1 배치에서는 잘 작동하지만 오버서브스크립션 환경에서는 idle vCPU가 물리 코어를 독점해 co-located 워크로드의 latency를 해친다는, "가상화가 존재하는 이유(오버서브스크립션)와 정면충돌하는" 숨은 비용을 결정론적 타이머 에뮬레이션으로 해결한다.

**VIRT-OSDI26-13 (DVLA, OSDI 2026, SUPPORT P2, T9 primary)**: T9-primary 중 유일하게 상세히 다룰 가치가 있는 SUPPORT 논문. VM 수명 예측 드리프트에 적응하는 계층적 예측 모델과 "placement debt" 개념으로, 실시간 예측 정확도가 40%로 떨어져도 이전 최고 기법(LAVA)의 oracle 상한을 능가한다. Live migration을 하루 810건 규모의 예산 제한 자원으로 다루는 프로덕션 현실을 명확히 보여준다.

## 4. Supporting 논문 (P2/P3)

**CPU 스케줄링/오버서브스크립션 보조**: VIRT-HPCA24-06(LibPreemptible)은 Intel UINTR로 커널 우회 preemption을 구현해 5us 단위 quantum에서 Shinjuku 대비 10배 나은 tail latency를 준다 — vCPU/VMM 내부 preemption 정책 설계에 직접 참고가 된다. VIRT-MIDDLEWARE24-03(PvCC)은 Xen credit 스케줄러를 마이크로초 단위로 수정해 DPDK poll-mode 워크로드와 best-effort 테넌트를 안전하게 통합한다. VIRT-OSDI26-08(vBPF)과 VIRT-OSDI26-09(vBOIDs)는 각각 eBPF 네임스페이스와 컨테이너 스레드를 vCPU 유사 단위(BOID)로 묶어 커널 확장/컨테이너 스케줄링에 가상화 패턴(네임스페이스 매개, 이산 슬롯)을 적용한다. VIRT-MIDDLEWARE24-01(UTwinVM)은 하이퍼바이저 패치가 게스트 성능에 미치는 영향을 게스트를 들여다보지 않고(twin 워크로드로) 예측한다.

**GPU 스케줄링**: Orion, ParvaGPU, KACE, Bless, GPreempt, XSched, Tally, LithOS, Aegaeon, Torpor, Dilu, FluidFaaS, BOER, ZipBatch, Priority-Aware Co-Scheduling, GMI-DRL, Resource Multiplexing(PEFT+서빙), Colocating Inference/Training 등은 모두 T6(accelerator_virtualization.md)에서 상세히 다룬다. 이 파일에서 강조할 점은: 이들 거의 전부가 "MIG/MPS라는 이미 존재하는 CORE 가상화 메커니즘을 given으로 놓고 그 위의 배치/우선순위/interference 예측만 최적화한다"는 것 — 이것이 T9의 구조적 특징(대부분 secondary)을 GPU 영역에서 가장 극적으로 보여주는 사례군이다.

**메모리 티어링/오버서브스크립션**: VIRT-SOSP25-16(Scalable Far Memory)은 far-memory 시스템이 코어 수가 늘면 TLB coherence·전역 LRU 경합으로 무너지는 문제를 always-async eviction·파이프라이닝·샤딩으로 해결한다(48 스레드에서 4.2배 처리량). VIRT-EUROSYS26-08(MTTM)은 다중 테넌트 CXL 티어드 메모리에서 fast tier를 동적 재분배한다. VIRT-ASPLOS26-14(PIPM)은 페이지 전체가 아니라 캐시 블록 단위로 hot 데이터만 선택 이동해 1.86배 속도향상을 얻는다 — 디스어그리게이션과 가상화의 경계를 다시 확인시키는 사례. VIRT-MIDDLEWARE25-13(MTAT)는 지연시간 critical 워크로드가 저빈도-고중요 접근 패턴을 갖는다는 점을 짚어 순수 빈도 기반 티어링의 한계를 드러낸다.

**스토리지/네트워크 QoS**: VIRT-ASPLOS25-10(FleetIO)은 이 계층의 핵심 딜레마를 가장 명료하게 정리한다: "하드웨어 파티션(강한 격리, 낮은 활용률) vs 소프트웨어 토큰버킷(높은 활용률, 2배 나쁜 tail latency)" — RL 에이전트가 ghost-superblock 간접 계층으로 vSSD 간 대역폭을 빌려주고 받아, 하드웨어 격리 tail latency의 1.2배 이내에서 소프트웨어 격리에 가까운 활용률을 얻는다. VIRT-OSDI24-05(BurstCBS)는 DPU 상주 storage agent에서 버스트 테넌트가 기본 SLO 테넌트를 침범하지 못하게 하는 프로덕션(Alibaba) 메커니즘이다. VIRT-EUROSYS25-09(Cloud Block Store Skew)는 6만 VM/14만 가상 디스크 규모에서 하이퍼바이저 폴링 스레드·세그먼트·LBA 수준 skew를 실측해, 가상 디스크 경로의 진짜 어려움이 "raw path efficiency"가 아니라 skew와 quota 의미론임을 밝힌다. VIRT-HPCA24-09(LightPool)은 로컬 NVMe를 NVMe-oF로 풀링해 Kubernetes가 스케줄링하게 한다. VIRT-ASPLOS26-11(Morphlux)은 재구성 가능한 포토닉 패브릭으로 torus 인터커넥트 대역폭을 테넌트별로 물리 계층에서 재분배한다.

**VM 배치/마이그레이션 경제성**: VIRT-CCGRID24-05(Workload-Aware Live Migratable Instance Detector)는 CRIU식 보수적 CPU-feature 비교 대신 워크로드가 실제로 쓰는 명령어만 분석해 마이그레이션 가능 목적지를 넓히고 spot 가격을 16% 개선한다. VIRT-ASPLOS24-07(RAP)은 GPU 유휴 시간에 전처리 커널을 채워넣는 예측 기반(하드웨어 격리 아닌) 스케줄링 사례다.

**보안**: VIRT-ASPLOS24-09(LLC Side-Channel)는 클라우드 LLC가 완전히 공유되어 컨테이너 경계를 넘는 정보 유출이 실제로 가능함을 실증한다(ECDSA nonce 81% 복구). VIRT-ASPLOS24-10(Co-Location Attacks)은 FaaS 배치의 불투명성이 TSC 지문 인식으로 완전히 깨질 수 있음을 보인다 — 두 논문 모두 "격리 메커니즘이 있다고 주장하는 것"과 "실제로 격리되는 것" 사이의 간극을 보여주는 T9판 반례다.

## 5. Trade-off 구조

- **파티션 vs 공유(FleetIO의 정식화)**: 하드웨어 파티션은 강한 격리·낮은 활용률, 소프트웨어 공유는 높은 활용률·약한 격리/나쁜 tail latency. 이 corpus 전체(GPU MIG/MPS, vSSD, SmartNIC)에서 반복되는 가장 근본적인 구조.
- **오버서브스크립션 이득 vs SLO 위험**: SweetspotVM/Coach는 비용을 크게 절감하지만 그 위험을 명시적으로 가격에 반영하거나(할인 인스턴스) 실시간 완화(페이지 트리밍, live migration)로 관리해야 한다.
- **결정 지연 vs 최적성**: VMR2L/Kamino는 학습된 정책으로 결정 시간을 분(MIP)에서 초 단위로 줄이지만 몇 %의 최적성을 포기한다 — "너무 늦은 최적해는 최적이 아니다"라는 원칙.
- **마이그레이션을 예산으로 다루기**: DVLA/Coach는 live migration을 공짜 도구가 아니라 순이익 요건이 있는 희소 자원으로 명시적으로 예산화한다.
- **오프라인 프로파일링 비용 vs 온라인 정확도**: KACE, RAP, Dilu류 GPU 스케줄러 전반에서 반복되는 축 — 정밀한 커널 레벨 프로파일링은 정확하지만 오프라인 비용이 든다.
- **파티셔닝 세밀도 vs 재구성 비용**: Mosaic의 하드웨어 타일, MIG의 정적 파티션, Memstrata의 page coloring 모두 세밀할수록 좋지만 세밀할수록 재구성/전환 비용이 커진다.

## 6. 인접 계층과의 관계

- **T1 (CPU 가상화) 아래**: SweetspotVM, EuroSys25-04(vCPU 추상화), Tai Chi, mwait-sched는 모두 T1의 vCPU 스케줄링/preemption 메커니즘 위에서 오버서브스크립션·정확성·유휴 처리를 개선한다.
- **T2 (메모리 가상화) 아래**: Memstrata, Coach, Demeter, Blowfish, Scalable Far Memory, MTTM, PIPM은 전부 T2의 guest-physical 메모리/ballooning/CXL 디스어그리게이션 메커니즘을 given으로 놓고 멀티테넌트 정책을 얹는다.
- **T3 (I/O 가상화) 아래**: OSMOSIS, PeRF, Tai Chi, BurstCBS, FleetIO는 T3의 SR-IOV/DPU/NVMe-oF 메커니즘 위에서 공정성/QoS를 강제한다.
- **T6 (가속기 가상화) 아래**: GPU 스케줄링 논문 전체(Orion~LithOS)는 T6에서 다룬 MIG/MPS/preemption 메커니즘을 소비한다.
- **T4 (migration/checkpoint) 위**: VMR2L, DVLA, Workload-Aware Live Migratable Detector는 T4의 live migration을 "정책 결정의 대상 자원"으로 다룬다.
- **T8 (서버리스) 과의 관계**: Mosaic는 서버리스 오버서브스크립션 환경을 직접 겨냥하며, 다수의 CONTEXT 수준 스케줄링 논문(Jiagu, ALPS, Ursa, Grad, LASSY, SUPLEC, Eva 등, DIGEST_CONTEXT.md)이 T9의 배치/오버서브스크립션 문제를 서버리스/마이크로서비스 맥락에서 반복한다.

## 7. 2024 → 2026 변화

2024년은 개별 자원(NIC, CPU, GPU)마다 QoS 메커니즘을 만드는 단계였다: OSMOSIS(SmartNIC), PeRF(RDMA), SweetspotVM(vCPU), Memstrata(CXL 메모리), Mosaic(마이크로아키텍처 캐시). 이들은 대부분 규칙 기반 또는 하드웨어 기반 정책이다.

2025년부터는 두 가지 변화가 뚜렷하다. 첫째, **여러 자원을 동시에 오버서브스크립션하는 통합 정책**(Coach의 CPU+메모리+네트워크+스토리지 동시 오버서브스크립션)과 **학습 기반 배치**(VMR2L의 RL, Kamino의 지연시간 예측, DVLA의 드리프트 적응 예측)가 본격화된다 — MIP/휴리스틱에서 학습된 정책으로의 전환이 이 구간에서 관찰된다. 둘째, 메모리 티어링이 guest-delegation(Demeter) vs host-driven(Blowfish)이라는 두 갈래로 성숙하며, RDMA 디스어그리게이션 메모리까지 확장된다.

2026년에는 DPU/SmartNIC이 "가상화되는 대상"에서 "자원관리를 수행하는 주체"로 전환되는 사례(Tai Chi, mwait-sched)가 나타나고, "오버서브스크립션의 숨은 비용"(idle vCPU의 mwait 독점)처럼 기존 최적화가 새로운 환경에서 실패하는 것을 짚는 논문이 등장한다. 다만 T9 자체의 표본(특히 2026년 CORE급 논문)은 크지 않으므로, 이 전환이 GPU 스케줄링(T6)만큼 뚜렷한 대규모 트렌드라고 단정하기는 이르다 — 개별 사례(Tai Chi, mwait-sched, Blowfish)로 보는 것이 안전하다.

## 8. 읽는 순서 제안

1. **VIRT-ASPLOS25-10 (FleetIO)** — "파티션 vs 공유"라는 이 계층 전체의 핵심 딜레마를 가장 명료하게 정식화한 논문으로 시작.
2. **VIRT-OSDI24-02 (Memstrata/CXL 메모리 티어링)** — 가상화 메커니즘(guest-physical 메모리) 없이는 정의조차 안 되는 자원관리 문제의 전형.
3. **VIRT-CCGRID24-01 (SweetspotVM)** → **VIRT-EUROSYS25-04 (vCPU 정확한 추상화)** — vCPU 오버서브스크립션의 실제 모습.
4. **VIRT-MICRO24-17 (Mosaic)** — T9에서 유일하게 자체 CORE인 논문으로 하드웨어 파티셔닝의 극한.
5. **VIRT-EUROSYS25-02 (VMR2L)** → **VIRT-OSDI25-02 (Kamino)** → **VIRT-OSDI26-13 (DVLA)** — VM 배치 정책이 MIP에서 학습 기반으로 진화하는 궤적.
6. **VIRT-ATC24-06 (OSMOSIS)** → **VIRT-SOSP25-15 (Tai Chi)** — SmartNIC이 가상화 대상에서 주체로 바뀌는 궤적.
7. **VIRT-SOSP25-02 (Demeter)** ↔ **VIRT-OSDI26-05 (Blowfish)** — guest-delegation vs host-driven 메모리 티어링 설계 철학 비교.
8. (선택) T6의 GPU 스케줄링 시퀀스(Orion → Bless → LithOS)를 함께 읽어 같은 패턴이 가속기에서 반복됨을 확인.

## 9. 증거 한계

다음 논문은 abstract 또는 초록+서론 수준 근거에 의존한다: **VIRT-ASPLOS25-04 (Tela, ABSTRACT/LOW)**, **VIRT-ATC24-12 (UniMem, ABSTRACT_INTRO/MEDIUM)**, **VIRT-HPCA24-09 (LightPool, ABSTRACT_INTRO/MEDIUM)**, **VIRT-MIDDLEWARE24-01 (UTwinVM, ABSTRACT_INTRO/MEDIUM)**, **VIRT-EUROSYS25-06 (Byte vSwitch, ABSTRACT/MEDIUM)**, **VIRT-ASPLOS26-11 (Morphlux, ABSTRACT_INTRO/MEDIUM)**, **VIRT-EUROSYS26-08 (MTTM, ABSTRACT_INTRO/MEDIUM)**, **VIRT-EUROSYS26-15 (DROPS, ABSTRACT/MEDIUM)**, **VIRT-MIDDLEWARE25-02 (Full Trust Alchemist, ABSTRACT/MEDIUM)**, **VIRT-MIDDLEWARE25-03 (Tiaccoon, ABSTRACT/MEDIUM)**, **VIRT-MIDDLEWARE25-13 (MTAT, ABSTRACT/MEDIUM)**, **VIRT-SOSP25-02 (Demeter, ABSTRACT/MEDIUM — 핵심 논문으로 다뤘지만 isolation_mechanism은 "설계로부터 추론, 논문 본문 미검증"으로 명시됨)**, **VIRT-ASPLOS26-14 (PIPM, ABSTRACT_INTRO/MEDIUM)**, **VIRT-CCGRID26-03/04 (Priority-Aware Co-Scheduling, Enhanced SVM, 둘 다 ABSTRACT/MEDIUM)**, **VIRT-EUROSYS26-22 (RDMA Connection Sharing, ABSTRACT_INTRO/MEDIUM)**, **VIRT-HPCA26-02/03 (eGPU, SCALE, 둘 다 ABSTRACT/MEDIUM)**, **VIRT-OSDI26-12 (mwait-sched, DESIGN/MEDIUM)**, **VIRT-SOCC25-20 (XpuPod, ABSTRACT_INTRO/MEDIUM)**. 이들의 숫자와 메커니즘 서술은 초록 수준에서만 확인되었으므로 상대적으로 약한 근거로 취급해야 한다. 또한 DIGEST_CONTEXT.md에 나열된 T9 태그 CONTEXT 논문(CyberStar, HAPPIES, Ursa, Grad, LASSY, SUPLEC, Eva, AutoBurst, INS, Dynamic Idle Resource Leasing at Meta, WDP, REEF 등) 다수는 "why: UNKNOWN"으로만 기록되어 있어 이 문서의 어떤 구체적 주장에도 근거로 사용하지 않았다. 반대로 핵심 논문 절의 Mosaic, Memstrata, SweetspotVM, EuroSys25-04(vCPU), OSMOSIS, PeRF, Tai Chi, Blowfish, DVLA는 모두 FULL/HIGH 또는 DESIGN_EVAL/HIGH 근거를 갖는다.

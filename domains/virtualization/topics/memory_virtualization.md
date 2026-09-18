# 메모리 가상화 (Memory Virtualization)

## 1. 이 계층이 푸는 문제

Physical Resource(DRAM, 그리고 CXL/PMem/NVMe로 확장된 원격 메모리) → Logical Abstraction(guest-physical address space, nested/second-level page table, elastic·tiered 메모리 풀) → Workload(메모리 집약적 클라우드 인스턴스, 서버리스 함수, LLM 학습/추론)로 이어지는 매핑이 이 계층의 대상이다. Guest는 guest-virtual → guest-physical 주소만 알지만, 실제로는 guest-physical → host-physical이라는 hypervisor가 관리하는 두 번째 변환이 하나 더 존재한다(EPT/NPT, nested/2단계 페이지 테이블). 이 계층이 반복적으로 마주치는 문제는 다섯 가지로 요약된다. (1) **번역 비용** — nested paging은 TLB miss 시 최대 24-35회의 순차 메모리 접근을 요구한다(VIRT-ASPLOS24-01). (2) **오버커밋** — 여러 VM에 물리 메모리보다 많은 guest-physical 메모리를 약속하면서도 안전하게 회수(reclaim)해야 한다(ballooning/hotplug 계열). (3) **가시성 격차** — hypervisor는 권한이 있지만 guest의 실제 접근 패턴(hotness)을 모르고, guest는 패턴을 알지만 물리 배치 권한이 없다(VIRT-SOSP25-02, Demeter가 이를 명시적으로 정식화). (4) **이종 계층화** — DRAM/CXL/PMem/NVMe로 확장되는 메모리 계층 사이에서 무엇을 어디에 둘지 결정해야 한다. (5) **중복 제거와 보안** — 여러 VM이 동일한 콘텐츠를 가질 때 이를 공유하면서도(KSM류) 그 공유 메커니즘 자체가 새로운 공격 표면(Rowhammer 등)이 되지 않게 해야 한다.

## 2. Mechanism design space

**Ballooning (virtio-balloon)**: guest 안에 상주하는 드라이버가 "풍선"을 부풀려 페이지를 회수한다. 가장 널리 쓰이지만 느리고(HyperAlloc 측정: 0.95 GiB/s), device passthrough(IOMMU pinning) 아래서는 DMA 안전성이 깨진다.

**Hotplug (virtio-mem)**: 메모리 영역을 통째로 온라인/오프라인시키는 방식. Ballooning보다 빠르지만(34 GiB/s) 자동 회수 능력이 없고, VIRT-ASPLOS25-02(HyperHammer)가 보여주듯 guest가 임의로 해제 요청을 조작해 Rowhammer 공격의 발판(page steering)으로 악용할 수 있다.

**Hypervisor-shared page-frame allocator (VIRT-EUROSYS25-03, HyperAlloc)**: guest의 buddy allocator 자체를 LLFree로 교체해 hypervisor(QEMU monitor)와 포인터 없는 압축 메타데이터를 공유한다. 344.8 GiB/s의 회수 처리량(20 GiB VM 기준)으로 ballooning 대비 362배, virtio-mem 대비 10배 빠르지만, guest의 buddy allocator를 교체해야 하므로 투명성을 희생한다.

**Guest-delegated tiering (VIRT-SOSP25-02, Demeter)**: hotness 분류·승격/강등 정책을 guest 커널에 위임하고 hypervisor는 용량 중재만 담당한다. 반대 극단은 **hypervisor-driven hardware tiering**(VIRT-OSDI24-02, Memstrata)로, Intel Flat Memory Mode가 64B 캐시라인 단위로 DRAM/CXL을 투명하게 매핑하고 페이지 컬러링으로 테넌트 간 간섭을 차단한다. **VIRT-OSDI26-05(Blowfish)**는 이 둘 사이의 제3의 지점으로, hotness 추적은 guest에 두되(MGLRU 기반) 실제 데이터 이동은 host가 EPT 조작만으로(guest/IO 페이지 테이블은 건드리지 않고) RDMA 원격 메모리로 수행한다.

**Sub-huge-page hotness 추적**: VIRT-ATC24-20(HugeScope)과 VIRT-SOCC25-21은 모두 "2MB huge page 전체가 hot으로 오분류되는" 문제를 guest 또는 hypervisor 어느 쪽에서 풀 것인지가 다르다 — HugeScope는 hypervisor 쪽 EPT A/D 비트를 재활용하고, VIRT-SOCC25-21은 guest 쪽에서 흩어진 hot 서브페이지를 huge page로 재응집시킨다.

**중복 제거(deduplication)**: Linux KSM(콘텐츠 스캔+병합)은 CPU를 14-65% 소모한다(VIRT-ATC25-14). Para-ksm은 Intel DSA로 스캔을 오프로드하고 256페이지 배치로 제출 오버헤드를 상쇄한다. VIRT-SOCC25-02(unikernel 로드타임 중복제거)는 아예 런타임 스캔을 없애고 빌드타임에 동일 페이지를 공유 풀에서 매핑한다. VIRT-CCGRID24-02(SLM)는 마이그레이션 도중 이 공유 관계 자체가 깨지지 않도록 페이지를 Unique/Duplicate/Dirty로 분류해 전송한다.

**Passthrough와 오버커밋의 근본적 충돌**: IOMMU ATS/PRI 하드웨어는 20% 미만의 프로덕션 VM에서만 쓸 수 있고(VIRT-OSDI25-01), IOPF 지연은 CPU page fault 대비 3-80배다. VIRT-SOSP24-02(VPRI)와 VIRT-OSDI25-01(VIO)은 각각 사이드밴드 큐와 사전 스누핑(IOPA-Snoop)으로 이 문제를 하드웨어 PRI 없이 소프트웨어로 해결한다.

**GPU/가속기 메모리 가상화**: MIG 같은 공간 분할 위에서도 L3 TLB는 공유되어(VIRT-MICRO24-07, STAR) 서브엔트리 단위 동적 공유가 필요하고, VIRT-ASPLOS24-03(GMLake)은 가상 주소 스티칭으로 GPU 메모리 파편화를 해결하며, VIRT-OSDI26-06(Nixie)은 UVM의 demand-paging 대신 명시적 전체 워킹셋 마이그레이션으로 시간 분할을 구현한다.

**신뢰 경계 위의 메모리 가상화**: VIRT-HPCA24-01(Data Enclave)은 데이터 수명을 enclave 수명에서 분리해 다중 enclave 간 공유를 가능하게 하고, VIRT-ATC24-22(CPC)는 confidential VM 유지보수(ballooning/snapshot/migration) 코드를 guest-trusted 상태로 host가 스케줄링할 수 있게 한다.

## 3. 핵심 논문 (P0/P1)

**VIRT-OSDI24-02 | Memstrata (OSDI 2024, CORE P0)** — Intel Flat Memory Mode(64B 캐시라인 단위 DRAM/CXL 직접매핑 하드웨어 계층화) 위에, 하이퍼바이저가 페이지 컬러링을 얹어 같은 로컬메모리 "라인"에 매핑되는 페이지를 한 VM으로 제한한다. 이는 "노이즈 이웃" 문제 — 페이지 컬러링 없이는 co-resident VM 간 로컬메모리 캐시라인 충돌이 tail latency를 최대 480% 악화시킴(Redis p95, 단일 소켓 6-VM 실험) — 를 구조적으로 차단한다. 랜덤포레스트 이상치 탐지기(L3-miss latency 프록시, r²=0.87)가 5% 슬로우다운 예산을 넘을 위험이 있는 VM에 추가 전용 DRAM 페이지를 동적 재할당한다. 결과: 115개 워크로드 중 82%가 33% 전용 DRAM 만으로 5% 이내 슬로우다운(vs 순수 하드웨어 계층화의 73%), 6-VM 최악 슬로우다운 35%→6% 미만. 대가는 고정 1:1 local:CXL 용량 비율과 6-VM 규모의 단일 소켓 검증에 그친다는 점이다.

**VIRT-EUROSYS25-03 | HyperAlloc (EuroSys 2025, CORE P1)** — guest의 buddy allocator를 LLFree로 교체하고 압축된 포인터-프리 메타데이터를 QEMU monitor 주소공간에 매핑해, guest와 hypervisor가 원자적 연산만으로 페이지 상태(M,R,E,A 튜플)를 공유한다. Hypervisor는 5초마다 유휴 2MiB huge page를 스캔해 EPT/IOMMU에서 언맵한다. 회수 처리량 344.8 GiB/s(20 GiB VM, 2×Intel Xeon Gold 6252) vs virtio-mem 34 GiB/s vs virtio-balloon 0.95 GiB/s. VFIO passthrough 하에서도 DMA-safe하게 54.6 GiB/s를 낸다(virtio-mem+VFIO의 17.7 GiB/s 대비). 대가는 guest 투명성 상실(buddy allocator 교체 필요)과 프레임 재설치 시 QEMU monitor 모드 전환 비용(virtio-mem 대비 약 6% 느림).

**VIRT-SOSP25-02 | Demeter (SOSP 2025, CORE P1)** — hot/cold 페이지 분류와 승격/강등 정책을 guest 커널에 위임하고 hypervisor는 fast-tier 용량 중재만 담당한다. TPP/Nomad/Memtis(guest-side) 및 TPP-H(hypervisor-side) 베이스라인과 비교되었으며, DRAM+Intel Optane PMEM 환경에서 검증되었다. "hypervisor는 권한이 있지만 의미를 모르고, guest는 의미를 알지만 권한이 없다"는 메모리 가상화의 근본 딜레마를 2025년 가장 명료하게 정식화한 논문이다. 구체적 수치는 abstract 수준에서 확인되지 않았다.

**VIRT-OSDI26-05 | Blowfish (OSDI 2026, CORE P1)** — Demeter의 완전 guest-delegation과 달리, hotness 추적은 guest에(Linux MGLRU 확장 - Fair MGLRU + Subpage Tracker로 THP의 "unfair hotness"/"hot bloat" 문제 해결), 실제 데이터 이동은 host가 EPT invalidate + RDMA 전송만으로 수행하고 원격 주소를 EPT의 미사용 비트에 직접 인코딩해 별도 메타데이터 테이블 없이 처리한다. Reclaim/restore latency 14.5µs/9.8µs(HyperAlloc 계열 대비 53%/60% 개선), 5% 이내 슬로우다운으로 회수 가능한 메모리 비율이 HyperAlloc 변형 대비 1.6-6.1배(dual Intel Xeon Gold 6342, 100Gbps InfiniBand). 대가는 guest 협조 가정(비협조 시 host-driven 스와핑으로 폴백)과 경험적으로 튜닝된 파라미터(100ms epoch, 20% threshold).

**VIRT-OSDI26-03 | InfiniDefrag (OSDI 2026, CORE P1)** — guest physical address space를 "거의 무한"하다고 취급해, 파편화된 base page를 데이터 이동 없이 새로 매핑한 연속 GPA 블록과 "교환"한다(Memory Trade, VirtIO 경유). Host 쪽은 buddy allocator를 우회하는 Self-Hosted Remap(약 1µs, mremap의 270µs 대비)으로 응답한다. 극심한 파편화 하에서 Linux THP 대비 처리량 21-105% 개선(YCSB-Redis 21%, Graph500 105%, dual-socket Intel Xeon Gold 6330), defrag 대역폭 약 20GB/s(THP의 0.91GB/s 대비 약 19배). 대가는 GPA 크기에 비례해 커지는 페이지 메타데이터와, guest-physical 주소 지시자가 가상화가 원래 제공하는 간접 계층을 압축 기법이 아닌 회피 기법으로 활용한다는 개념적 재구성이다.

**VIRT-SOCC25-21 | 왜곡된 hot huge page 재응집 (SoCC 2025, CORE P1)** — 흩어진 "skewed hot" 서브페이지를 guest 상주 컴포넌트(Scattered Page Filter + Page Consolidator, 커스텀 syscall)가 조밀한 huge page 영역으로 재배치해, host 계층화 엔진(Memtierd/TPP/AutoNUMA)이 오분류 없이 정확한 신호를 받게 한다. 단일 VM에서 근접메모리 소비 50-70% 절감, 멀티 VM에서 10-13% 성능 개선. Demeter와 짝을 이루는 "hotness 신호 품질을 guest에서 개선"이라는 제3의 설계점.

**VIRT-ASPLOS24-01 | DMT (ASPLOS 2024, CORE P1)** — 코어당 16개 레지스터가 VMA→물리 Translation-Entry-Area를 직접 매핑해 nested paging 워크를 1회 참조로 축소한다. pvDMT는 하이퍼콜(KVM_HC_ALLOC_TEA)과 읽기전용 gTEA 테이블로 guest 격리를 보장한다. Nested 가상화에서 shadow paging 오버헤드의 39% 제거, 애플리케이션 속도 1.48배(4KB, Redis/Memcached/GUPS 등 7개 메모리집약 벤치마크, Intel Xeon Gold 6138). 대가는 소수의 크고 정적인 VMA를 전제한다는 것 — 파편화가 심하면 일반 페이지 워크로 폴백한다.

**VIRT-ATC24-20 | HugeScope (ATC 2024, CORE P1)** — coarse phase(기존 EPT A/D 비트, 분할 없음)로 hot huge page 후보를 찾고 fine phase에서만 분할해 Page Skewness Ratio를 계산한다. EPTE가 구축 후 거의 수정되지 않는다는 사실을 활용해 KVM 함수 11개만 후킹, VM exit을 16GB 워크로드 기준 4.3M+회에서 915회로(4,000배 이상 감소) 줄인다. Tiered memory 배치 최대 61% 개선, 페이지 공유 42.3% 메모리 절감(KSM의 1.28% 대비). 대가는 hypervisor 자신의 swapping/ballooning이 동시에 같은 EPT를 수정할 때의 정합성 예외 처리다.

**VIRT-SOCC24-07 | 지속적 ballooning (SoCC 2024, CORE P1)** — 대규모 메모리 스파이크와 라이브 마이그레이션이라는, 기존에는 ballooning을 끄고 감수해야 했던 두 고위험 순간에도 안전하게 ballooning을 계속 돌릴 수 있게 하는 사용자공간 조정 프로그램. 최대 8% 오버헤드로 최소 52% 빠른 마이그레이션(수백 GB급 VM, 거의 600GB까지 검증), 무한정 순차 마이그레이션에도 스왑/OOM 없음. 실제 클라우드 고객이 월 수만 회 중첩 클라우드 VM을 마이그레이션한다는 흔치 않은 프로덕션 데이터 포인트를 제공한다. 다만 비-오버커밋 배포 환경에 범위가 한정된다.

**VIRT-EUROSYS26-05 | Squeezy (EuroSys 2026, CORE P1)** — hotplug된 메모리를 일반 VM 메모리와 guest allocator 내부에서 분리하고 수명을 제한해, 커널이 hotplug된 페이지만 정확히 식별해 빠르게 회수한다("커널이 어떤 물리 메모리가 hotplug된 것인지 모른다"는 사실이 기존 hot-unplug가 느린 이유임을 명시). 서버리스 워크로드 중 여러 GB를 서브초 단위로 회수(구체 베이스라인 수치는 abstract 수준). HyperAlloc과 나란히 T2의 "회수 지연이 왜 발생하는가"를 설명하는 사례.

**VIRT-ASPLOS25-12 | Coach (ASPLOS 2025, CORE P1, T2+T9)** — CPU/메모리/네트워크/스토리지 각각을 guaranteed(P95 기준, huge page로 물리적으로 백업)와 oversubscribed(zero-size NUMA 노드로 노출되는 가상 주소 풀)로 나눈다. 20초 간격 contention 모니터링(CPU wait/page R/W)이 EWMA/LSTM으로 예측해 페이지 트리밍·풀 확장·라이브 마이그레이션으로 대응한다. 6개의 4시간 윈도우로 정적 할당 대비 메모리 약 15%·CPU 약 20% 절감(단일 24시간 윈도우의 약 8% 대비), 호스트당 최대 26% 더 많은 VM(프로덕션 서버, 160 하이퍼스레드 Intel 코어, 512GB DRAM, 2주간 약 100만 VM Azure 트레이스). 대가는 guaranteed 메모리의 비탄력성(물리적으로 고정 백업되어야 함)과 예측 오차(19-24% 메모리 과할당).

**VIRT-ATC25-14 | Para-ksm (ATC 2025, CORE P1)** — Linux KSM의 memcmp/xxhash 스캔(CPU 14-65% 소모)을 Intel DSA로 오프로드한다. 단순 페이지당 오프로드(DSA-ksm)는 제출 오버헤드 때문에 CPU 대비 2.6-2.7배 느리므로, Para-ksmC는 256개 후보 페이지를 배치로 묶어 red-black tree 재균형이 predecessor/successor를 바꾸지 않는다는 성질을 활용한다. 애플리케이션 슬로우다운을 3.3배(CPU-ksm)에서 2.1배로, CPU 사용률을 48.2%에서 31.0%로 낮춘다. 대가는 순수 DSA 오프로드(DSA-ksm, CPU 7.3%)보다 메모리 절감 누적 속도가 느리다는 것.

**VIRT-ASPLOS25-02 | HyperHammer (ASPLOS 2025, CORE P1)** — "완전한 기능을 갖춘 최신 하이퍼바이저에서도 guest가 KVM 강제 격리를 깰 수 있는가"라는 질문에 THP(hugepage 주소 하위 21비트 노출) → page steering(약 6만 개의 vIOMMU 매핑으로 버디 할당자의 소형 free list 고갈 후 virtio-mem으로 취약 페이지 해제) → single-sided Rowhammer(leaf EPT 엔트리 비트 플립)의 3단계로 답한다. 예상 종단 공격 시간은 137-192일(Intel Core i3-10100/Xeon E-2124, Apacer DDR4-2666 non-ECC). 메모리 오버커밋 편의기능(THP, virtio-mem, vIOMMU/VFIO) 각각이 보안에 어떻게 관여하는지 이해하는 데 가장 좋은 단일 논문이며, 방어책으로 virtio-mem의 guest 요청 검역(quarantine)을 제안한다.

**VIRT-ASPLOS24-03 | GMLake (ASPLOS 2024, CORE P1, T6+T2)** — GPU 저수준 가상 메모리 API로 하나의 논리적 연속 가상주소 범위를 여러 비연속 물리 GPU 메모리 블록에 매핑하는 Virtual Memory Stitching. DNN 프레임워크·메모리 절감 기법(재계산, 오프로딩, LoRA)에 완전히 투명하다. 8개 LLM 모델(NVIDIA A100 80GB)에서 평균 9.2GB(최대 25GB) 메모리 절감, 파편화 평균 15%(최대 33%) 감소. CPU 측 가상/물리 분리 개념을 GPU에 이식한 깔끔한 사례.

**VIRT-OSDI26-06 | Nixie (OSDI 2026, CORE P0, T6+T2)** — 소비자 GPU에서 NVIDIA UVM의 demand-paging이 4-12배 스래싱을 유발하는 문제를, 애플리케이션 전체 워킹셋을 128MB 청크(2MB 블록 단위)로 명시적으로 이동시키는 전이중(full-duplex) PCIe 계획으로 해결한다. CUDA VMM API로 가상주소를 유지해 애플리케이션 무수정. Nvshare 대비 대화형 작업 latency 3.1-3.8배 개선, UVM 대비 핀메모리 사용량 66.8% 감소. 대가는 단일 사용자/동일 UID 신뢰 가정(다중 테넌트 보안 격리 없음)이다.

## 4. Supporting 논문 (P2/P3)

- **VIRT-SOSP24-02 (VPRI)**, **VIRT-OSDI25-01 (VIO/PRI)** — 둘 다 device passthrough의 정적 pinning을 소프트웨어 사이드밴드 메커니즘으로 대체해 메모리 오버커밋을 회복한다. VPRI는 5000대 프로덕션 VM에서 NIC IOPF를 99% 이상 줄였고, VIO는 30만 VM 규모에서 하루 약 120GB를 회수했다. 두 편 모두 "왜 IOMMU ATS/PRI가 실무에서 쓰이지 않는가"를 이해하려면 먼저 읽어야 한다.
- **VIRT-ATC24-22 (CPC)** — confidential VM 유지보수(ballooning/snapshot/migration)를 guest-trusted "maintenance vCPU"로 host가 스케줄링. AMD SEV-SNP(VMPL)와 ARM CCA(Confidential Page-Table Isolation) 양쪽에 구현. 메모리 추출 최대 340배, 라이브 마이그레이션 최대 138배 개선(AMD Secure Processor 베이스라인 대비). T4 파일에서 더 상세히 다룸.
- **VIRT-HPCA24-01 (Data Enclave)** — enclave 수명에서 데이터 수명을 분리해 다중 SGX enclave 간 N:M 공유를 가능하게 함. Inter-enclave 공유 latency 최대 2000배 개선.
- **VIRT-EUROSYS25-05 (Erebor)**, **VIRT-EUROSYS25-17 (CKI)** — confidential VM 내부에 추가 격리 경계(각각 소프트웨어 monitor / PKS 기반)를 두는 두 가지 접근. Erebor는 provider 하이퍼바이저 무수정 배포가 가능하지만 8.1% 오버헤드, CKI는 nested cloud에서 shadow paging/nested EPT 비용을 완전히 제거한다.
- **VIRT-CCGRID24-02 (SLM)**, **VIRT-CCGRID24-03** — 라이브 마이그레이션 중 KSM류 페이지 공유 관계가 깨지는 "메모리 풋프린트 팽창" 문제를 페이지 분류(Unique/Duplicate/Dirty)로 해결. T4 파일에서 본격적으로 다룸.
- **VIRT-MICRO24-07 (STAR)** — MIG의 공간 분할 아래서도 L3 TLB는 공유된다는 사실을 드러내고, 서브엔트리 동적 공유로 30.2% 평균 성능 개선. GPU 가상화 스레숄드 함정(SUPPORT지만 CORE 설계의 빈틈을 메움)의 좋은 예.
- **VIRT-MIDDLEWARE24-02 (vPIM)**, **VIRT-MIDDLEWARE24-06 (Menos)**, **VIRT-CCGRID26-04 (SVM GPU 오버서브스크립션)** — 각각 Processing-in-Memory 가상화(virtio 스타일 프론트/백엔드), 분할 파인튜닝을 위한 GPU 메모리 시간/공간 공유, AMD SVM의 마이그레이션 그래뉼래러티/축출 정책 개선. 모두 GPU/PIM 메모리 가상화의 SUPPORT 계층 사례.
- **VIRT-OSDI25-08 (FineMem)**, **VIRT-OSDI25-13 (Tiered Memory Beyond Hotness)**, **VIRT-SOSP25-16 (Scalable Far Memory)**, **VIRT-ASPLOS26-14/15/16 (PIPM, Cxlalloc, CXL0)** — CXL/원격 메모리 디스어그리게이션의 SUPPORT 계층 논문군. 분류 기준(브리프의 threshold trap)이 명확히 적용된 사례들로, "디스어그리게이션은 그 자체로 가상화가 아니며, guest-facing한 가상 자원 추상화를 세우지 않는 한 SUPPORT"라는 원칙을 반복 확인시켜 준다. 특히 Tiered Memory Beyond Hotness는 hotness가 아니라 Amortized Offcore Latency(AOL = latency/MLP)를 배치 신호로 쓴다는 점에서 CXL/NUMA 계층화 정책의 대안적 기준을 제시한다.
- **VIRT-MIDDLEWARE25-13 (MTAT)**, **VIRT-EUROSYS26-08 (MTTM)** — 멀티테넌트 환경에서 fast-tier 용량을 SLO 클래스별/수요별로 재분배. Blowfish 같은 pooling 메커니즘 위에 필요한 공정성 정책 계층.
- **VIRT-ASPLOS24-12 (TrackFM)**, **VIRT-ATC24-12 (UniMem)**, **VIRT-OSDI24-06 (Nomad)**, **VIRT-OSDI24-07 (Atlas)**, **VIRT-SC24-02 (TECO)** — far-memory/CXL 프로그래밍 모델과 컴파일러 지원 계열. 가상화 CORE 논문의 배경 지식으로 유용하지만 guest-facing 가상 자원 추상화는 없음.
- **VIRT-SOCC24-10 (Faascale)** — Firecracker microVM 메모리 수직 탄력성. 메커니즘 상당 부분이 "UNKNOWN"(원문 미독, 아티팩트 추론)으로 기록되어 있어 신중히 인용해야 한다.
- **VIRT-MIDDLEWARE25-14 (FlexClone)** — VM 디스크 이미지/컨테이너 레이어 바로 아래 계층(파일 클론)의 페이지캐시 중복 문제.

## 5. Trade-off 구조

- **속도 vs 투명성**: HyperAlloc(가장 빠름, guest allocator 교체 필요) → virtio-mem(중간, 자동회수 없음) → virtio-balloon(가장 느림, 완전 표준)으로 이어지는 스펙트럼. 빠를수록 guest 협조/수정 요구가 커진다.
- **오버커밋 vs 보안**: THP/virtio-mem/vIOMMU 같은 편의 기능이 밀도를 높이지만, HyperHammer가 보여주듯 guest에게 물리 배치에 대한 간접적 통제력을 부여해 Rowhammer 같은 공격의 발판이 될 수 있다.
- **권한 vs 의미(semantics)**: hypervisor 주도 계층화(Memstrata)는 안전하지만 guest 접근 패턴을 모르고, guest 위임(Demeter)은 의미는 정확하지만 hypervisor 권한을 내줘야 한다. Blowfish는 "추적은 guest, 이동은 host"로 이 둘을 분리해 절충한다.
- **Passthrough vs 오버커밋**: device passthrough(IOMMU pinning)는 I/O 성능을 위해 정적 메모리 고정을 요구하며, 이는 가상화가 약속하는 메모리 탄력성과 직접 충돌한다(VPRI/VIO가 이 충돌을 소프트웨어로 우회).
- **중복 제거의 비용 이전**: KSM의 CPU 스캔 비용을 하드웨어 가속기(DSA)로 옮기면(Para-ksm) 애플리케이션 슬로우다운은 줄지만 완전히 없어지지는 않고, 빌드타임 중복제거(unikernel dedup)로 옮기면 런타임 비용은 0이 되지만 쓰기 가능한 페이지는 다룰 수 없다.
- **정밀도 vs 오버헤드**: sub-huge-page hotness 추적(HugeScope, SOCC25-21)은 정확할수록 스캔/분할 비용이 커지므로, 두 논문 모두 "필요한 후보만 정밀 조사"하는 2단계 구조를 택한다.

## 6. 인접 계층과의 관계

- **아래(T1 CPU 가상화)**: EPT/nested paging은 CPU 가상화가 제공하는 하드웨어 메커니즘이며, DMT·Elastic Translations는 이 변환 자체를 가속한다. JANUS(VIRT-OSDI26-01)는 GPA→HPA 권한을 L0에 집중시켜 T1과 T2를 직접 연결한다.
- **위(T4 마이그레이션/체크포인트)**: 메모리 상태가 실제로 이동할 때 이 계층의 설계가 그대로 마이그레이션 비용이 된다 — SLM(페이지 공유 보존), Coach·CPC(마이그레이션을 오버커밋의 탈출구로 사용), M3U(T4, dirty-page 추적의 커널 락 병목)가 대표적 다리다.
- **T3 I/O 가상화**: device passthrough와 메모리 오버커밋의 충돌(VPRI, VIO, HyperAlloc의 IOMMU 언맵)이 T2-T3 경계의 핵심 문제다.
- **T6 가속기 가상화**: GPU 메모리(GMLake, Nixie, STAR, Salus)는 CPU 메모리 가상화 개념(가상-물리 분리, TLB, 시간/공간 분할)이 그대로 재적용되는 영역이다.
- **T7 confidential computing**: HyperHammer(공격), VeriSMo/Rust page table 검증(T1 파일 참고), CPC·Erebor·CKI(유지보수·추가 격리)는 모두 메모리 가상화 계층이 신뢰 경계와 어떻게 상호작용하는지를 보여준다.
- **T9 자원관리**: Coach, MTAT, MTTM은 이 계층이 제공하는 계층화·오버커밋 메커니즘 위에 공정성/SLO 정책을 얹는다.

## 7. 2024 → 2026 변화

관찰 가능한 패턴(작은 표본에 대한 조심스러운 서술): 2024년은 ballooning/hotplug의 근본적 한계(속도, DMA 안전성)를 새 메커니즘(HyperAlloc의 공유 allocator, HugeScope의 EPT 재활용)으로 우회하는 데 집중했다. 2025년은 "hotness를 누가 알고 누가 결정하는가"라는 guest-vs-hypervisor 권한 문제를 정면으로 제기했다(Demeter, SOSP 2025). 2026년 표본(Blowfish, InfiniDefrag, SOCC25-21)은 이 이분법을 넘어 "추적은 guest, 이동은 host" 같은 혼합 설계나 "압축 대신 회피"(GPA를 무한대로 취급) 같은 재구성으로 이동하는 것으로 보인다. 다만 T2 2026년 논문은 모두 OSDI/SoCC 소수 편에 국한되어 있어, 이를 산업 전반의 확정적 추세로 일반화하기는 이르다.

## 8. 읽는 순서 제안

1. **VIRT-ASPLOS24-01**(DMT, nested paging 비용의 물리적 실체) → 2. **VIRT-ATC24-20**(HugeScope, huge page hotness의 함정) → 3. **VIRT-EUROSYS25-03**(HyperAlloc, ballooning/hotplug/공유 allocator 삼자 비교) → 4. **VIRT-ASPLOS25-02**(HyperHammer, 오버커밋 편의기능의 보안 대가) → 5. **VIRT-OSDI24-02**(Memstrata, 하드웨어 CXL 계층화+페이지 컬러링) → 6. **VIRT-SOSP25-02**(Demeter, guest-vs-hypervisor 딜레마의 정식화) → 7. **VIRT-OSDI26-05**(Blowfish, 혼합 설계) → 8. **VIRT-OSDI26-03**(InfiniDefrag, GPA를 무한대로 재구성) → 9. GPU 갈래로 **VIRT-ASPLOS24-03**(GMLake) → **VIRT-OSDI26-06**(Nixie).

## 9. 증거 한계

다음 항목은 abstract 수준 근거에 머물러 있다: VIRT-ATC24-12(UniMem), VIRT-OSDI24-06(Nomad), VIRT-OSDI24-07(Atlas), VIRT-SOCC24-07(지속적 ballooning, 정성적 서술은 상세하나 정량치 일부는 abstract 인용), VIRT-SOCC24-10(Faascale, 메커니즘 상당 부분 UNKNOWN), VIRT-MIDDLEWARE25-13(MTAT), VIRT-SOSP25-02(Demeter, 메커니즘은 서술되나 구체 수치 미확인), VIRT-SOCC25-21(수치는 있으나 abstract_intro 수준), VIRT-ASPLOS26-14(PIPM), VIRT-ASPLOS26-15(Cxlalloc), VIRT-ASPLOS26-16(CXL0), VIRT-EUROSYS26-05(Squeezy, 정성적 메커니즘은 명확하나 정량 베이스라인 미확인), VIRT-MIDDLEWARE25-14(FlexClone), VIRT-EUROSYS26-08(MTTM), VIRT-CCGRID26-04(SVM GPU 오버서브스크립션). 이들은 메커니즘의 방향성과 문제의식은 신뢰할 수 있으나, 구체적 수치나 세부 알고리즘을 이 문서에 인용할 때는 "abstract 수준" 단서가 붙어 있음을 유의해야 한다.

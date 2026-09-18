# Cross-Paper Relations Map (2024–2026 코퍼스)

이 문서는 `PAPER_RELATIONS.csv`(330개 관계, 228편 중 186편이 최소 1개 관계에
연루)를 하나의 내비게이션 지도로 정리한 것이다. "이 논문을 막 읽었다면 다음에
무엇을 읽어야 하는가"에 답하도록 구성했다.

---

## 1. Relation-type 분포

| relation_type | 건수 | 의미 |
|---|---:|---|
| SAME_BRANCH | 118 | 같은 설계 공간(T-taxonomy 분기)의 형제 논문 |
| CONTRASTS_WITH | 62 | 같은 문제를 양립 불가능한 방식으로 해결 |
| ALTERNATIVE | 58 | 논문이 직접 baseline으로 구현·측정한 대안 |
| USES_MECHANISM_FROM | 25 | 다른 논문/시스템의 메커니즘을 재사용 |
| LAYER_ABOVE | 21 | 대상 메커니즘 위에 얹힌 정책/시스템 |
| LAYER_BELOW | 18 | 대상 시스템이 의존하는 하위 메커니즘 |
| TRADEOFF_PAIR | 17 | 같은 trade-off의 양 극단에 위치 |
| PRECURSOR | 6 | 시간적으로 선행하는 직계 원류 |
| EXTENSION | 5 | 선행 논문의 명시적 확장/후속판 |
| **합계** | **330** | |

관계의 target 중 121개는 코퍼스 내 다른 `VIRT-...` 논문이고, 130개는 코퍼스 밖의
외부 메커니즘/시스템(virtio-balloon, CRIU, NVIDIA MIG, zpoline, VM pre-copy live
migration(Clark et al., NSDI 2005) 등)이다. 즉 관계의 절반 가까이는 "코퍼스가
스스로 참조하는 표준 베이스라인"을 향한 것이며, 이는 코퍼스가 실제 시스템
문헌으로서 성숙했다는 신호다.

---

## 2. Hub 논문 — 다음에 읽을 진입점

연결도(in-degree + out-degree, VIRT-VIRT 관계만 집계)가 높은 논문일수록 그
설계 공간의 중심 참조점이다. 상위 hub와 "이 논문을 읽었다면 다음"을 정리한다.

| 순위 | 논문 | 연결도(out/in) | 읽은 뒤 다음으로 |
|---|---|---|---|
| 1 | **VIRT-EUROSYS25-03 \| HyperAlloc** (T2) | 11 (3/8) | `VIRTUALIZATION_LINEAGES.md` Lineage A 전체 — Para-ksm(dedup 대안), Continuous Ballooning(안전성 대안), Squeezy/Faascale(microVM 특화), VIO(투명성 대안), FineMem(passthrough 아래 회수의 trade-off 파트너) |
| 2 | **VIRT-SOSP25-08 \| Dandelion** (T5) | 7 (4/3) | CHERIoT RTOS(자신의 하위 메커니즘), μFork(대안), Quilt(위의 정책층), Firecracker(trade-off 상대) |
| 3 | **VIRT-SOSP25-12 \| TickTock** (T10) | 6 (3/3) | Miralis(위의 CVM monitor), Tock(형제 임베디드 OS), Ghost in the Android Shell(형제) |
| 3 | **VIRT-SOSP25-11 \| CHERIoT RTOS** (T10) | 6 (3/3) | Dandelion·μFork(위의 두 소비자), TickTock(대안 격리 접근) |
| 3 | **VIRT-EUROSYS25-01 \| FastIOV** (T3) | 6 (3/3) | HyperAlloc(같은 passthrough 대가의 다른 얼굴), Byte vSwitch(trade-off 상대), SG-IOV(같은 SR-IOV 한계의 형제) |
| 3 | **VIRT-ATC25-03 \| Kernel-Space GPU Interception** (T6) | 6 (2/4) | GPreempt·Torpor(형제), GMI-DRL(대비), MIG/MPS(baseline) — `VIRTUALIZATION_LINEAGES.md` Lineage C 진입점으로 최적 |
| 3 | **VIRT-SOSP25-14 \| LithOS** (T6) | 6 (4/2) | Aegaeon(정반대 극), Coyote v2(FPGA 유비), MIG/MPS(baseline) |
| 3 | **VIRT-SOSP25-10 \| Coyote v2** (T6) | 6 (5/1) | LithOS(GPU 유비), Coyote v1(선행판), AmorphOS/OPTIMUS(대안) |
| 3 | **VIRT-OSDI25-10 \| bpftime** (T5) | 6 (3/3) | DeCl·Omniglot·Rex(형제·대비), ATC25-02(관련 형제) |
| 3 | **VIRT-SOSP25-02 \| Demeter** (T2) | 6 (2/4) | HyperAlloc(같은 lineage), Scalable Far Memory(대안), Blowfish(다음 세대의 대비 대상) |
| 3 | **VIRT-EUROSYS25-17 \| CKI** (T5) | 6 (3/3) | HyperTurtle(정반대 답), Erebor(형제), LiteShield(형제) |
| 3 | **VIRT-ASPLOS25-12 \| Coach** (T2) | 6 (3/3) | Tela·FleetIO(형제), 오버서브스크립션 정책층 |

**읽기 전략**: 이 코퍼스에 처음 들어온다면 (1) T2를 원하면 HyperAlloc, (2) T6/GPU를
원하면 Kernel-Space GPU Interception(ATC25-03) 또는 LithOS, (3) 얇은-격리/T5를
원하면 Dandelion 또는 CKI, (4) 임베디드/저수준 격리를 원하면 CHERIoT RTOS에서
시작하는 것이 가장 많은 형제·대비·계층 링크를 한 번에 얻는 경로다.

---

## 3. Cross-layer bridges (LAYER_ABOVE / LAYER_BELOW)

이 관계는 "메커니즘 논문 → 그것을 소비하는 시스템/정책 논문"을 잇는다. 화살표는
`LAYER_BELOW(메커니즘) → LAYER_ABOVE(소비자)` 방향으로 정리했다.

| 메커니즘(below) | 소비 시스템(above) | 근거 |
|---|---|---|
| VIRT-OSDI25-02 Kamino (admission-time 배치) | VIRT-EUROSYS25-02 VMR2L (재배치) | "attack CPU/host fragmentation from opposite ends of the VM lifecycle" |
| VIRT-OSDI25-05 Fork in the Road (cold-start 요인분해) | VIRT-EUROSYS25-11 (동일 분해를 인용) | 프로덕션 cold-start 구성요소 측정이 후속 최적화의 동기 |
| VIRT-ATC25-06 Poby (SmartNIC 이미지 프로비저닝) | VIRT-OSDI25-05 (cold-start 지배 요인 규명) | "Poby attacks exactly that image-provisioning component" |
| VIRT-EUROSYS25-14 AlloyStack (워크플로 실행 기판) | VIRT-EUROSYS25-13 SeBS-Flow (벤치마크층) | 새 기판을 판정할 벤치마크가 위에 위치 |
| VIRT-EUROSYS25-01 FastIOV (블록/네트워크 attach 지연) | VIRT-EUROSYS25-09 (정상상태 블록 경로 특성화) | 같은 Alibaba-scale I/O 문제의 다른 단면 |
| VIRT-EUROSYS25-07 Bless (GPU 내부 SM 파티셔닝) | VIRT-EUROSYS25-12 (클러스터 전체 SLO 코로케이션) | "Bless decides SM partitioning inside one GPU; this work decides co-location across a GPU cluster" |
| VIRT-SOSP25-11 CHERIoT RTOS (capability 하드웨어) | VIRT-SOSP25-08 Dandelion, VIRT-SOSP25-13 μFork | 둘 다 CHERI bound을 직접 백엔드로 사용 |
| VIRT-SOSP25-04 Miralis (가상 M-mode) | (그 위에 ACE confidential-VM monitor 탑재) | "Miralis hosts ACE as a policy module" |
| VIRT-SOSP25-12 TickTock (PMP 정합성 검증) | VIRT-SOSP25-04 Miralis (그 PMP를 가상화) | "TickTock's bug classes are the correctness burden Miralis inherits" |
| VIRT-OSDI26-01 JANUS (cooperative nested virt) | VIRT-EUROSYS26-03 NecoFuzz (VMCS/VMCB 정합성 fuzzing) | 상호 `LAYER_ABOVE`/`LAYER_BELOW`로 대칭 기록 |
| VIRT-OSDI24-06 Nomad (호스트 단일 계층 페이지 이주) | VIRT-OSDI24-02 (CXL 멀티테넌트 VM 계층 추가) | "adds the multi-tenant/VM isolation layer (page coloring) on top of a similar tiering substrate" |
| VIRT-MIDDLEWARE25-06 FaaSImage (이미지 구체화) | VIRT-MIDDLEWARE25-05 (하이브리드 런타임이 회피하려는 비용) | cold-start 구성요소 하나를 담당 |
| VIRT-CCGRID25-01 (MIG 위 스케줄링) | (NVIDIA MIG 하드웨어, 외부) | "the paper schedules over MIG rather than changing it" |
| VIRT-ASPLOS25-11 (whole-GPU 할당 실태 문서화) | VIRT-ASPLOS25-03 Tally, VIRT-ASPLOS25-06 Dilu | 이들이 개선하려는 "coarse whole-GPU allocation regime"을 규정 |
| VIRT-ASPLOS25-04 Tela (vDisk 배치) | VIRT-ASPLOS25-10 FleetIO (런타임 내 중재) | "FleetIO arbitrates inside one virtualized device at runtime; Tela decides which device a virtual disk lands on" |
| VIRT-ASPLOS25-14 (자원 부족 시 애플리케이션 대응) | VIRT-ASPLOS25-12 Coach (오버서브스크립션 정책) | "Oversubscription creates the capacity risk; cooperative degradation is one way applications absorb it" |
| VIRT-MICRO25-02 (CXL 코히런트 NIC-host 기판) | (미래의 CXL 기반 vNIC/SR-IOV 가상화, 외부) | 아직 존재하지 않는 가상 장치 추상화가 딛고 설 기판만 확립 |
| VIRT-MICRO25-01 ccAI (PCIe 계층 신뢰 확장) | (TDX/SEV-SNP TVM, 외부) | "ccAI assumes an existing TVM protects CPU-side execution and adds the PCIe-to-accelerator leg on top" |

**읽기 팁**: LAYER_BELOW 쪽(메커니즘)을 먼저 읽으면 LAYER_ABOVE 쪽(정책/시스템)의
설계 결정이 왜 그렇게 내려졌는지 설명이 된다. 반대로 LAYER_ABOVE를 먼저 읽었다면
"이 시스템이 당연하게 가정하는 하부 계층이 무엇인지" 확인하는 용도로
LAYER_BELOW 논문을 찾아가면 된다.

---

## 4. TRADEOFF_PAIR 전체 목록 (17건, 중복 방향 제외 13쌍)

| 쌍 | 축 | 상세 |
|---|---|---|
| HyperAlloc (T2) ↔ FastIOV (T3) | passthrough의 두 대가 | 메모리 회수 vs 시작 지연 |
| HyperTurtle ↔ CKI (T5/T1) | nested virt 비용 | 가속 vs 회피 |
| FastIOV ↔ Byte vSwitch (T3) | passthrough vs 소프트웨어 매개 | 네트워크 I/O |
| Dandelion → Firecracker (T5) | POSIX 호환 vs 콜드스타트 | 89us vs ~120ms |
| SoCC25-14 → FluidFaaS (T6/T9) | 소프트 공간공유 불확실성 → 하드웨어 격리 선택 | GPU 간섭 |
| Vela → passthrough vs virtio/vSwitch (T3, 외부) | LLM 트래픽 직결 | live migration 포기 |
| FleetIO → 하드웨어-파티션 vs token-bucket vSSD (T3, 외부) | 스토리지 격리 방식 | 89% 소프트웨어 대역폭 + 1.47배 나은 tail |
| Roadrunner ↔ RUNE (T5) | Wasm 데이터 경로 vs 실행 속도 | 반대 방향 최적화 |
| vBOIDs → Firecracker (T5, 외부) | 스케줄링 추상화 vs guest-kernel 격리 | 최대 3배 처리량 |
| VPRI ↔ F&S (T3) | IOMMU/DMA 경계 3중 trade-off의 두 코너 | 안전성/성능/메모리 탄력성 |
| DMT → EPT/NPT (T2, 외부) | 2D page walk vs 직접 매핑 | 1.28–1.58배 speedup |
| Pentimento → Cloud FPGA logical-wipe (T6, 외부) | 순차 멀티테넌시 비용 vs 잔여 채널 | AWS F1에서 8개 중 5개 인스턴스 키 복구 |
| Guardian → MIG/MPS (T6, 외부) | 소프트웨어 안전 공유 vs 하드웨어 파티션 | 4–12% 오버헤드 |

이 13쌍은 `VIRTUALIZATION_TRADEOFFS.md`의 축 1(4쌍), 축 3(1쌍), 축 5(1쌍),
그리고 개별 사례(Dandelion/Firecracker, vBOIDs/Firecracker, DMT, Pentimento,
Roadrunner/RUNE, VPRI/F&S)로 흡수되어 상세히 다뤄진다.

---

## 5. CONTRASTS_WITH — 같은 문제의 양립 불가능한 답

62건 중 코퍼스 내부(VIRT-VIRT) 쌍만 추려 대표적인 것을 정리한다(외부 대상
25건은 대부분 "baseline과 정면 대비"로 이미 lineage/trade-off 문서에 흡수됨).

**같은 문제를 정반대 메커니즘으로 푸는 강한 대비**:
- **VIRT-SOSP25-07 Aegaeon ↔ VIRT-SOSP25-14 LithOS** — temporal token-level vs
  spatial TPC-level GPU 공유("the two poles of accelerator sharing").
- **VIRT-SOSP25-01 (RDMA 장치 협조 migration) ↔ VIRT-OSDI26-02 M3U** — opaque
  passthrough 상태 vs host-visible paravirtual 상태.
- **VIRT-SOSP25-05 Oasis ↔ VIRT-SOSP25-01** — 상태를 옮기지 않고 CXL로 우회 vs
  상태를 직접 옮김.
- **VIRT-OSDI25-01 VIO ↔ VIRT-EUROSYS25-03 HyperAlloc** — guest 무수정 hypervisor
  snooping vs guest allocator 공동설계.
- **VIRT-OSDI26-05 Blowfish ↔ VIRT-SOSP25-02 Demeter** — 얕은 guest 개입(hotness만)
  vs 깊은 guest 위임(전체 tiering).
- **VIRT-OSDI25-09 DeCl ↔ VIRT-OSDI25-10 bpftime ↔ VIRT-OSDI25-15 Omniglot** —
  SFI/LFI vs MPK 하드웨어 도메인 vs MPK+컴파일타임 스코프, 3파전.
- **VIRT-ATC25-04 GMI-DRL ↔ VIRT-ATC25-03** — 기존 MIG/MPS 인스턴스를 정책으로
  조합 vs 드라이버 아래 새 커널-매개 추상화(IGPU)를 구축.
- **VIRT-CCGRID26-03 (MPS priority) ↔ VIRT-CCGRID26-04 (SVM eviction)** — 새 가상
  GPU 추상화 없이 기존 메커니즘을 개선하는 두 SUPPORT급 접근("two different
  SUPPORT-level improvements to existing GPU virtualization/sharing mechanisms").
- **VIRT-EUROSYS26-01 CofferOS ↔ VIRT-EUROSYS26-06 SKernel** — OS-level
  virtualization을 강화하는 Rust 재작성 vs split-kernel 아키텍처, 같은 2026
  EuroSys secure-container 문제의 다른 답 `[INFERENCE — basis가 같은 세션/문제
  묶음일 뿐 직접 비교 문장은 약함]`.
- **VIRT-MICRO24-16 Veiled Pathways ↔ VIRT-MICRO24-07 STAR** — 둘 다 MIG의 공유
  구조(L3 TLB 등)를 다루지만, STAR는 성능 목적의 파티셔닝 개선이고 Veiled Pathways는
  "MIG가 실제로 파티션하지 못하는 것"(PCIe, codec 엔진, DRAM 주파수 제어)을
  보안 관점에서 폭로 — 같은 하드웨어의 두 상반된 해석.
- **VIRT-EUROSYS24-04 S-NIC ↔ VIRT-HPCA26-05 DSAssassin** — S-NIC의 하드웨어
  격리 주장에 DSAssassin이 Intel DSA를 통한 cross-VM side-channel로 반례를 제시
  (상호 `CONTRASTS_WITH`로 대칭 기록).

**해석 시 주의**: CONTRASTS_WITH 62건 중 다수는 "같은 학회/연도/저자 그룹이라
묶었다"는 얕은 근거(예: CCGrid26-03/04, EuroSys26-01/06)이며, 이 경우 위 목록에
`[INFERENCE]`로 표시했다. 반대로 Aegaeon↔LithOS, Oasis↔SOSP25-01, DeCl↔bpftime
같은 쌍은 논문 자신이 상대를 baseline으로 직접 측정하거나 명시적으로 대립
구도를 서술한 강한 근거를 갖는다.

---

## 6. 연결이 약한 부분 — 실제 발견

228편 중 42편(18%)이 `PAPER_RELATIONS.csv`에 전혀 등장하지 않는다. 이는 무작위로
흩어져 있지 않고 뚜렷한 패턴을 보인다.

- **T7(기밀/보안 격리)이 가장 심하게 고립되어 있다** — 10편이 고립, 그중
  **VIRT-ATC24-22 (CPC, P0)**, **VIRT-OSDI24-04 (VeriSMo, P0)**처럼 우선순위가
  가장 높은 논문들이 포함된다. CVM 정합성/검증 하위분야(VeriSMo, CPC, HPCA26-03
  SCALE, HPCA24-05 quantum TEE, HPCA24-02/03 Salus류)는 각자 독자적인 검증
  기법을 다루면서도 서로를 참조하는 관계가 코퍼스에 기록되지 않았다 — 이는
  이 하위분야가 아직 서로를 인용하며 계보를 형성하기보다 병렬적으로 발전하고
  있음을 시사한다.
- **T8(서버리스/클라우드 추상화)은 표본 자체가 작고(5편) 그중 2편이 고립** —
  Frozen Garbage 회수(EuroSys24-06)와 RDMA 기반 워크플로 상태 전송
  (EuroSys24-07)은 T2/T5 논문들과 명백한 메커니즘 유사성(memory reclamation,
  zero-copy 상태 공유)이 있음에도 코퍼스가 명시적 관계로 기록하지 않았다 — T8
  자체가 이 코퍼스에서 가장 얇게 다뤄진 taxonomy임을 뜻한다.
- **T1(CPU/머신 가상화)의 초기 진입점들이 흩어져 있다** — VIRT-CCGRID24-01
  (SweetspotVM), VIRT-MIDDLEWARE24-01/03(UTwinVM, PvCC), VIRT-ATC24-21
  (CrossMapping), VIRT-OSDI26-12(hyperscale idle 비용)은 vCPU 스케줄링·오버서브
  스크립션이라는 공통 주제를 다루면서도 서로 인용/대비 관계가 기록되지 않았다.
- **디스어그리게이션 하위 라인(ASPLOS26-14/15/16, CXL pod 할당/incremental
  migration/프로그래밍 모델)이 통째로 고립** — Lineage A(VM 메모리 탄력성)와
  주제적으로 인접하지만 관계 데이터가 이들을 연결하지 않는다. 이는 이 세 논문이
  더 순수한 "CXL 프로그래밍 모델" 논문에 가까워 guest-physical memory 가상화라는
  CORE 관심사와 살짝 비껴나 있기 때문일 가능성이 높다(CLASSIFICATION_BRIEF의
  "disaggregation은 virtual resource abstraction을 만들 때만 CORE" 기준과 일치).
- **개별 고립 CORE 논문 중 흥미로운 것들**: VIRT-MICRO24-01(NPU 하드웨어 지원
  가상화, P0)과 VIRT-ATC24-24(vFPIO, FPGA I/O 가상 추상화, P1)는 각자의
  가속기(NPU/FPGA) 가상화에서 상당히 이른 시기의 시스템인데도 후속 논문이
  이들을 직접 계승했다는 관계가 기록되지 않았다 — GPU 가상화만큼 계보가
  촘촘히 형성되지 못한 가속기 종류가 있다는 신호다.

**요약**: "잘 연결된 코퍼스"는 T5(컨테이너/경량 격리, 38편 연루)와 T6(가속기,
37편 연루)이고, "약하게 연결된 코퍼스"는 T7의 정합성/검증 하위분야와 T8
전체다. 독자가 T7 CVM 논문을 읽을 때는 이 지도에 의존하기보다 각 논문을
개별적으로 깊이 읽어야 한다는 뜻이다.

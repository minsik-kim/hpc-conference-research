# Virtualization Trade-offs (2024–2026 코퍼스)

이 문서는 코퍼스 전체를 관통하는 구조적 trade-off 축을 정리한다. 각 축마다
"X → Y를 얻지만 Z를 잃는다" 형태로 정식화하고, 그 축의 양 끝에 실제로 앉아 있는
논문을 `VIRT-...` id와 함께 명시하며, 코퍼스가 기록한 "이 trade-off에서 벗어나려는
시도"를 별도로 짚는다. `PAPER_RELATIONS.csv`의 `TRADEOFF_PAIR`/`CONTRASTS_WITH`
관계에 직접 근거한 항목은 그대로 인용하고, 관계 데이터 없이 여러 레코드의
`tradeoff` 필드만으로 같은 축임을 확인한 경우는 `[구조적 근거만 있음]`으로
표시한다.

---

## 축 1 — Passthrough vs 소프트웨어 매개 (canonical trade-off)

**정식화**: 장치를 guest에 직접 passthrough하면 소프트웨어 매개 비용은 사라지지만
(→ 낮은 지연, 높은 처리량) 격리·메모리 관리·live migration이 모두 어려워진다.

- **Passthrough 극단**: **VIRT-ASPLOS25-01 | Vela (ASPLOS25)** — KVM+SR-IOV+GPUDirect
  RoCE로 LLM 학습 트래픽을 직결. 논문 스스로 `TRADEOFF_PAIR → "device passthrough vs
  software-mediated virtio/vSwitch I/O"`로 명시: "Vela chooses passthrough + SR-IOV
  for performance and thereby forfeits live migration and transparent memory
  management." 오버헤드는 native 대비 ~5%.
- **소프트웨어 매개 극단**: **VIRT-EUROSYS25-06 | Byte vSwitch (EuroSys25)** — OVS를
  완전히 버리고 목적에 맞춘 forwarding engine으로 vSwitch 데이터 경로를 재작성.
  `TRADEOFF_PAIR ↔ VIRT-EUROSYS25-01 | FastIOV`: "Software vSwitch mediation versus
  SR-IOV passthrough are the two ends of the network I/O virtualization trade-off."
- **같은 축의 다른 계층**: **VIRT-EUROSYS25-03 | HyperAlloc**(memory reclaim)과
  **VIRT-EUROSYS25-01 | FastIOV**(startup latency)는 둘 다 "passthrough를 선택한
  대가"를 서로 다른 층위에서 치른다 — `TRADEOFF_PAIR`: "Both are consequences of
  choosing passthrough over software mediation." **VIRT-SOSP24-02 | VPRI**와
  **VIRT-SOSP24-03 | F&S**는 IOMMU/DMA 경계에서 이 축의 세 번째 코너(정적 pinning의
  memory-elasticity 비용)를 공격 — `TRADEOFF_PAIR ↔`: "together they cover
  complementary corners of the passthrough safety/performance/memory-elasticity
  trade-off space."
- **탈출 시도**:
  1. **하이브리드 분할** — **VIRT-HPCA25-01 | NVMePass**: 제어 자원은
     trap-and-emulate, 데이터 자원(I/O queue·doorbell)만 passthrough해 VFIO의
     97.6–100.2% 성능을 유지하면서 control-plane 유연성을 일부 회복.
  2. **호스트 안에서 흉내내기** — **VIRT-OSDI25-01 | VIO**: guest 무수정 상태로
     hypervisor가 proactive snooping해 IOPF를 제거, passthrough의 memory-elasticity
     문제를 해결(300K VM 프로덕션 검증).
  3. **더 촘촘한 하드웨어 파티셔닝** — **VIRT-ASPLOS26-01 | SG-IOV**: passthrough를
     포기하지 않되 가상화 단위를 소켓 단위로 낮춰 밀도 문제 자체를 해소.
  4. **필요할 때만 소유권 이전** — **VIRT-SOSP25-05 | Oasis**: 상태를 CXL 공유
     메모리에 두어 migration 문제를 우회(대가: 4–7us 지연, PCIe 링크 장애 무내성).

---

## 축 2 — 격리 강도 vs 시작 지연 (isolation strength vs startup latency)

**정식화**: 더 강한 격리 경계(별도 커널, 별도 주소공간, 하드웨어 가상화)를 두면
안전하지만 부팅/시작 비용이 커지고, 얕은 격리(공유 커널, 공유 주소공간)는 빠르지만
경계가 약해진다.

- **강한 격리, 느린 시작**: **VIRT-SOCC24-04 | SURE** — 함수당 별도 unikernel VM으로
  VM 수준 격리를 유지하면서도 DPDK zero-copy 데이터 경로로 Knative 대비 최대 79배
  시작 시간 단축을 보고. **VIRT-OSDI25-03 | MettEagle** — L4Re 마이크로커널 위
  capability 기반 zero-ambient-authority 격리로 TCB를 89,271 SLOC까지 줄임(Linux+
  containerd+runc의 2,699,812 SLOC 대비) — 격리는 극단적으로 강해지지만 컨테이너
  추상화 자체를 재구현하는 비용을 치른다.
- **얕은 격리, 빠른 시작**: **VIRT-SOCC24-05 | uIO** — 하나의 주소공간을 MPK
  도메인/eBPF 샌드박스로만 나눠 unikernel의 작은 이미지·빠른 부팅을 유지하되 별도
  프로세스보다 약한 경계를 받아들임(`ALTERNATIVE ↔ VIRT-MIDDLEWARE24-15 | LightZone`
  — "alternative hardware primitives for the same isolation-domain-count/switch-cost
  trade-off"). **VIRT-EUROSYS25-14 | AlloyStack** — 워크플로당 하나의 주소공간을
  공유해 1.3ms 시작을 얻지만 격리는 MPK+명령어 블랙리스트로 약화.
- **중간 지점**: **VIRT-ATC25-01 | LiteShield** — 공유 host kernel을 userspace
  uKernel 서비스로 대체해 hypervisor·guest kernel 없이 VM급 얇은 인터페이스(22
  syscall)를 제공. **VIRT-EUROSYS25-17 | CKI**와 **VIRT-ATC25-02 | HyperTurtle**은
  이 축을 nested-virtualization 맥락에서 정면으로 다투는 `TRADEOFF_PAIR`
  (`VIRTUALIZATION_LINEAGES.md` Lineage D 참조) — 가속이냐 회피냐가 곧 "격리 유지 vs
  시작/실행 비용 절감"의 구체적 형태다.
- **탈출 시도**: microVM 자체의 시작 지연을 별도로 공격하는 하위 갈래 —
  **VIRT-ATC24-19 | SnapStart (지속 메모리 증강 hypervisor)**는 VM 격리를 그대로
  유지한 채 concurrent snapshot 복원으로 시작 지연만 줄이며, `ALTERNATIVE ↔
  VIRT-ATC24-14`(보안·자원효율 특화 대안)와 명시적으로 대비된다. Lineage A의
  Squeezy/Faascale도 "격리(VM 경계)는 그대로 두고 탄력성만 개선"하는 같은 탈출
  전략의 메모리 버전이다.

---

## 축 3 — 공간적(spatial) vs 시간적(temporal) 멀티플렉싱 — GPU 사례

**정식화**: 물리 자원을 공간적으로 쪼개면(예: GPC/TPC 파티션) 하드웨어 수준 격리를
얻지만 파편화와 정적 배분 비효율이 남고, 시간적으로 나누면(스케줄링) 이용률은
높아지지만 격리가 약해지고 전환 지연이 생긴다.

- **공간적 극단**: **VIRT-SOSP25-14 | LithOS** — TPC 단위 투명 파티셔닝 + atomized
  preemption, MIG 대비 13배 tail-latency 감소, 100% high-priority SLO 달성(MPS
  45% 대비). LithOS는 `ALTERNATIVE → MIG`("TPC masking is finer and dynamic where
  MIG is GPC-granular and static")·`ALTERNATIVE → MPS`("MPS shares compute units
  with weak isolation and no priority")로 명시.
- **시간적 극단**: **VIRT-SOSP25-07 | Aegaeon** — token 단위 autoscaling, 프로덕션
  fleet 82% 절감이지만 서브초 전환 정지·메모리 슬랙 의존. LithOS와 Aegaeon은
  `CONTRASTS_WITH`로 서로를 직접 "the two poles of accelerator sharing"이라 부른다
  (Lineage C 참조).
- **중간 지점을 찾으려는 시도들**:
  - **VIRT-HPDC25-02 | FluidFaaS** — 고정된 MIG 파티션 "안에서" 파이프라인 시간
    공유를 함으로써 MIG의 강한 격리는 유지하면서 파편화 손실을 회복
    (`CONTRASTS_WITH ↔ VIRT-SOCC25-14`: "SoCC25-14 shows MPS-style soft spatial
    sharing has unpredictable microarchitectural interference; this paper
    deliberately chooses hardware-isolated MIG to avoid that class of problem, at
    the cost of fixed partition granularity").
  - **VIRT-ASPLOS25-06 | Dilu** — 소프트웨어 SM quota를 탄력적으로 조정해 공간적
    파티셔닝의 유연성 부재를 완화하되 폐쇄형 드라이버를 건드리지 않음.
  - **VIRT-ATC25-12/13** — 서빙(지연-민감)과 학습/파인튜닝(처리량-지향)을 한
    GPU에서 공존시키되 한쪽은 공간(SM/memory handover), 한쪽은 시간(iteration-level
    interleaving)으로 접근 — `SAME_BRANCH`: "contrasted with static partitioning or
    full temporal isolation."
  - **VIRT-SOCC25-14 | Understanding GPU Resource Interference One Level Deeper**는
    "MPS 스타일 소프트 공간 공유가 예측 불가능한 간섭을 낳는 이유"를 미시아키텍처
    수준에서 규명해 `TRADEOFF_PAIR → VIRT-HPDC25-02`(FluidFaaS가 왜 하드웨어
    격리형 MIG를 선택했는지의 동기)로 이어진다 — **이것이 이 축에서 유일하게
    corpus가 `TRADEOFF_PAIR`로 직접 표시한 링크**다.

---

## 축 4 — 투명성(unmodified guest) vs 공동설계(guest cooperation)

**정식화**: guest를 전혀 건드리지 않으면(투명) 배포가 쉽지만 최적화 여지가
제한되고, guest 커널/allocator를 hypervisor와 공동설계하면 수십~수백 배의
성능 이득을 얻지만 guest 이식성과 배포 장벽이 생긴다.

- **투명 극단**: **VIRT-OSDI25-01 | VIO** — guest VirtIO ring을 hypervisor가
  바깥에서 snooping만 함. `CONTRASTS_WITH ↔ VIRT-EUROSYS25-03 | HyperAlloc`:
  "HyperAlloc reclaims VM memory by co-designing the guest allocator with the
  hypervisor ... VIO instead keeps the guest completely unmodified and solves the
  same passthrough-vs-overcommitment conflict entirely inside the hypervisor via
  proactive snooping." **VIRT-ASPLOS25-12 | Coach**도 `ALTERNATIVE → memory
  ballooning`을 명시: "Coach deliberately avoids guest modification, using a
  zero-size NUMA node and page trimming instead of a balloon driver."
- **공동설계 극단**: **VIRT-EUROSYS25-03 | HyperAlloc** — guest buddy allocator를
  LLFree로 교체해 virtio-mem 대비 10배, virtio-balloon 대비 362배 빠른 shrink.
  대가는 "guest transparency의 상실"(코퍼스 tradeoff 필드가 직접 명시). **VIRT-SOSP25-02
  | Demeter** — hot/cold 분류·승격 전체를 guest에 위임해 guest-semantic accuracy를
  얻지만 hypervisor의 배치 권한을 내준다.
- **같은 축 위의 중간 지점**: **VIRT-OSDI26-05 | Blowfish**는 Demeter보다 얕은
  공동설계(guest는 hotness tracking만)를 택해 `CONTRASTS_WITH ↔ Demeter`로 정확히
  이 스펙트럼 위의 위치 차이를 기록한다 — "Blowfish keeps only hotness tracking in
  the guest and does all data movement/EPT-only reclamation on the host," 결과는
  53–60% 낮은 지연.
- **탈출 시도라기보다 스펙트럼 자체**: 이 축은 "탈출"이 아니라 정도(degree)의
  문제로, 코퍼스는 한쪽 끝(VIO)에서 다른 쪽 끝(HyperAlloc/Demeter)까지, 그리고
  중간(Blowfish)까지 세 지점을 모두 명시적 관계로 채워 넣은 드문 축이다.

---

## 축 5 — 하드웨어 파티셔닝 vs 소프트웨어 스케줄링

**정식화**: 하드웨어가 자원을 물리적으로 나누면(MIG, TPC, IOMMU PASID) 격리는
강하지만 재구성이 느리고 세분성이 고정되며, 소프트웨어가 드라이버/커널 수준에서
가로채 스케줄링하면 유연하지만 격리 보증이 약해지고 벤더별 리버스엔지니어링에
의존하게 된다.

- **하드웨어 파티셔닝**: NVIDIA MIG(GPC 단위, 정적), **VIRT-SOSP25-14 | LithOS**의
  TPC masking(더 세밀하지만 여전히 하드웨어 격리).
- **소프트웨어 스케줄링**: **VIRT-EUROSYS24-03 | Orion** — 순수 소프트웨어로
  커널 단위 세밀한 공유를 달성하지만 보안 격리가 전혀 없음. `CONTRASTS_WITH → MIG`:
  "the opposite trade-off point from hardware-partitioned MIG instances." **VIRT-MIDDLEWARE24-04
  | Guardian** — PTX 계측으로 소프트웨어에서 안전한 공유를 구현, `TRADEOFF_PAIR →
  MIG/MPS`: "Guardian achieves it in software (PTX instrumentation) with measured
  4-12% overhead instead of hardware-partitioned isolation." **VIRT-ASPLOS24-07 |
  RAP**는 하드웨어 파티셔닝을 아예 쓰지 않고 순수 비용 모델로 스케줄링,
  `CONTRASTS_WITH → MIG/MPS-based vGPU partitioning`: "RAP explicitly benchmarks
  against and avoids relying on MIG/MPS hardware partitioning, instead using a
  software cost model" — 91–99%의 예측 정확도에 의존하는 대신 하드웨어 보증을
  포기한 극단적 사례.
- **탈출 시도**: **VIRT-ATC25-03**(커널 공간 가로채기로 호환성+격리 동시 확보,
  Lineage C 3단계)가 이 축에서 가장 성공적인 절충으로 기록된다 — "no prior single
  approach had both"라는 표현이 곧 이 축의 두 극단을 동시에 만족시키려는 시도임을
  보여준다.

---

## 축 6 — 신뢰 경계 크기 vs 성능/호환성 (TCB size vs performance/compatibility)

**정식화**: 신뢰 계산 기반(TCB)을 작게 유지하면 검증 가능성과 공격 표면이
줄지만, 기존 생태계와의 호환성이나 성능이 희생된다.

- **작은 TCB 극단**: **VIRT-OSDI25-03 | MettEagle** — 전체 컨테이너 스택을
  89,271 SLOC(Linux+containerd+runc 2,699,812 SLOC 대비)로 축소하지만 fork()가
  2.5–4.8배 느려짐. **VIRT-EUROSYS25-18 | RAKIS** — enclave 내부에서 커널 우회
  링을 직접 구동해 TCB를 2 KLoC로 유지(liburing ~35 KLoC, libxdp+libbpf ~130 KLoC
  대비), 대가는 일부 데이터 기밀성/무결성 보증의 축소.
- **넓은 호환성 극단**: **VIRT-MICRO25-01 | ccAI** — 특정 벤더 GPU Confidential
  Computing 모드(예: NVIDIA H100 CC) 대신 PCIe 계층의 벤더-비의존적 메커니즘으로
  GPU/NPU/FPGA 3개 벤더에 걸친 신뢰 확장을 제공. `CONTRASTS_WITH → GPU
  vendor-specific confidential computing`: "ccAI is explicitly vendor-agnostic ...
  via a PCIe-level mechanism instead of a per-accelerator hardware TEE" — 더 넓은
  적용 범위를 얻는 대신 벤더 특화 TEE만큼 촘촘한 통합은 포기.
- **탈출 시도**: **VIRT-ATC25-16 | ASTERINAS**와 **VIRT-ATC25-15 | μEFI**는
  `SAME_BRANCH`로 묶여 "작은 신뢰 코어 + 샌드박스화된 모듈"이라는 동일 패턴을
  각각 OS 커널 계층(Rust 안전성)과 펌웨어 계층(페이지테이블 샌드박스)에 적용 —
  두 계층에서 독립적으로 같은 절충 전략이 재발명되었다는 점이 흥미롭다.

---

## 축 7 — 상태 지역성(state locality) vs 이주 가능성(migratability)

**정식화**: 장치/가속기 상태를 host가 볼 수 없는 곳(장치 내부, passthrough
경로)에 둘수록 성능은 좋지만 live migration이 근본적으로 어려워지고, 상태를
host-visible한 곳에 두면(paravirtual, 공유 CXL 메모리) 이주는 쉬워지지만 그만큼
성능/제어를 hypervisor 매개에 내준다. 이 축은 `VIRTUALIZATION_LINEAGES.md`
Lineage E와 동일한 근거 집합을 다른 각도(trade-off 축)에서 재구성한 것이다.

- **상태 지역성 극단(이주 어려움)**: **VIRT-SOSP25-01 | Device-Assisted Live
  Migration of RDMA Devices** — 장치 자신의 협조 없이는 opaque 상태를 옮길 수
  없음을 정면으로 인정하고 장치 프로토콜을 확장.
- **이주 가능성 극단(상태를 host-visible하게 유지)**: **VIRT-OSDI26-02 | M3U** —
  VirtIO의 host-visible 특성을 이용해 virtqueue를 사전 설치. `CONTRASTS_WITH ↔
  VIRT-SOSP25-01`: "M3U ... tackles [a case that is] the strictly harder [problem
  for passthrough]"라는 표현이 두 지점의 난이도 차이를 정량 없이도 명확히 한다.
- **완전한 탈출**: **VIRT-SOSP25-05 | Oasis** — 상태를 아예 이동시키지 않고
  공유 CXL 메모리에 상주시켜 소유권만 재할당(대가: 4–7us 지연, 전용 폴링 코어,
  링크 장애 무내성).

---

## 트레이드오프 축 간의 관계

축 1(passthrough)과 축 4(투명성)는 상당 부분 겹친다 — passthrough를 선택하면
guest-physical memory 관리를 위해 결국 축 4의 co-design 쪽으로 밀려나는 경향이
있다(HyperAlloc이 passthrough/IOMMU pinning 하에서도 동작하도록 설계된 것이 그
증거). 축 3(공간/시간 멀티플렉싱)과 축 5(하드웨어/소프트웨어 파티셔닝)도 GPU
사례에서는 사실상 같은 스펙트럼의 두 단면이다(MIG=하드웨어+공간,
Orion=소프트웨어+시간적 세밀함). 반면 축 2(격리-시작지연)와 축 6(TCB-호환성)은
독립적인 축으로, 강한 격리가 반드시 작은 TCB를 의미하지 않는다는 점이 MettEagle
(작은 TCB, 큰 fork 비용)과 SURE(VM급 격리, 상대적으로 큰 TCB지만 빠른 시작)의
대비에서 드러난다.

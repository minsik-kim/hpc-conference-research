# THREE_YEAR_TRENDS — 2024 → 2026 virtualization 연구 동향

근거: 12개 venue, 3년, 검토 410건 / 보존 362건(CORE 124, SUPPORT 104, CONTEXT 134) 기준.

## 0. 이 문서를 읽기 전에 — 표본의 한계

2026년은 **2026-09-18 기준 이미 개최된 venue만** 포함한다. 따라서 2026 표본(83건)은
2024(167건)·2025(160건)보다 구조적으로 작다. 아래에서 비율을 말할 때는 이 점을 감안했고,
표본이 trend를 지지하지 못하는 경우에는 그렇게 적었다. **작은 표본에서 trend를 억지로
만들지 않는 것**이 이 문서의 원칙이다.

또한 §GLOBAL_AUDIT이 기록했듯 SC 2024/2025는 전수 열거에 실패했고 SoCC 2024는 track 구분이
미확인이다. HPC 계열 venue의 2024 수치는 다른 venue보다 신뢰도가 낮다.

taxonomy별 CORE+SUPPORT 분포(primary tag 기준):

| tax | 주제 | 2024 | 2025 | 2026 | 합 |
|---|---|---|---|---|---|
| T1 | CPU/machine virtualization | 4 | 4 | 5 | 13 |
| T2 | memory virtualization | 11 | 9 | 6 | 26 |
| T3 | I/O·device virtualization | 11 | 12 | 5 | 28 |
| T4 | migration/checkpoint/state | 9 | 4 | 4 | 17 |
| T5 | container/lightweight isolation | 15 | 25 | 5 | 45 |
| T6 | accelerator virtualization | 14 | 20 | 7 | 41 |
| T7 | confidential/security isolation | 14 | 11 | 8 | 33 |
| T8 | serverless abstraction | 5 | 0 | 0 | 5 |
| T9 | resource management | 5 | 5 | 4 | 14 |
| T10 | boundary/other | 0 | 6 | 0 | 6 |

---

## 1. 고전 VM/hypervisor 연구는 쇠퇴하지 않았다 — 문제가 이동했다

T1 primary는 3년 내내 4–5건으로 **평평하다**. 절대 수가 적어 "쇠퇴"로 오독하기 쉽지만,
CORE만 보면 4 → 4 → 5로 오히려 2026에 가장 많다. 표본이 작아 증가를 주장하지는 않되,
**감소의 증거는 없다**고는 말할 수 있다.

더 중요한 것은 **무엇에 관한 논문인가가 바뀌었다**는 점이다.

- 2024: 정확성·검증이 중심. VeriSMo(OSDI24, confidential VM security module 검증),
  HongMeng(OSDI24, 상용 microkernel), MIRVerif.
- 2025: nested virtualization 비용과 guest-host 인터페이스 정밀도.
  HyperTurtle(ATC25, nested 가속), "Optimizing Task Scheduling in Cloud VMs with Accurate
  vCPU Abstraction"(EuroSys25), Ghost in the Android Shell(SOSP25, 상용 hypervisor
  test-oracle), HyperHammer(ASPLOS25, KVM 격리 파괴).
- 2026: nested virtualization이 **보안 container의 구현 수단**으로 재등장.
  JANUS(OSDI26, cross-world cooperative nested virtualization for secure containers),
  NecoFuzz(EuroSys26, nested virtualization fuzzing), CofferOS(EuroSys26, Rust).

즉 hypervisor 연구는 "더 빠른 VM"에서 **"검증 가능하고, 중첩 가능하며, container를 담는
그릇으로서의 hypervisor"** 로 이동했다. 이것이 이 corpus가 보여주는 가장 분명한 T1 서사다.

`[FACT_FROM_PAPER]` JANUS·NecoFuzz·HyperTurtle 모두 L0/L1/L2 world-switch 비용을 직접
측정하거나 공격한다. `[INFERENCE]` 이 세 편을 하나의 문제 계보로 묶은 것은 감사자의 판단이다.

## 2. memory virtualization — 권한 배분의 재협상

T2는 11 → 9 → 6으로 수치상 감소하지만, 2026 표본 축소를 감안하면 **감소라고 단정할 수 없다.**
대신 명확한 것은 **기구의 세대 교체**다.

계보(가장 잘 입증된 lineage):

```
virtio-balloon / virtio-mem        (corpus 이전, baseline으로 반복 측정됨)
  → HyperAlloc (EuroSys25)         guest allocator를 hypervisor와 공유
  → Faascale (SoCC24)              microVM 수직 memory scaling
  → Squeezy (EuroSys26)            serverless 함수용 신속 회수
  → Demeter (SOSP25)               guest delegation 기반 tiering
  → Blowfish (OSDI26)              disaggregated memory 위 elastic VM memory
  → InfiniDefrag (OSDI26)          guest physical address space 자체를 무한대로
```

관통하는 축은 **"누가 hotness를 추적하고 누가 배치 권한을 갖는가"** 다.
Memstrata(OSDI24)는 host가 전부 쥐고, Demeter는 guest에 위임하며, Blowfish는 guest가 추적하고
host가 옮기는 혼합이다. `[FACT_FROM_PAPER]` HyperAlloc은 20 GiB VM/19 GiB written pages,
2× Xeon Gold 6252 환경에서 reclaim 344.8 GiB/s로 virtio-mem 34 GiB/s·virtio-balloon
0.95 GiB/s 대비 우위를 보고한다.

동시에 **deduplication이 재부상**했다: Para-ksm(ATC25), BASK(EuroSys26, SmartNIC offloaded KSM),
Hugepage-aware dedup(SoCC25), unikernel load-time dedup(SoCC25). 이는 §3의 passthrough
문제와 맞물린다 — ballooning이 막힌 환경에서 dedup이 대안 회수 경로가 되기 때문이다.

## 3. direct I/O — SR-IOV의 천장과 passthrough 대가의 3가지 회피법

T3는 11 → 12 → 5다. 2026 감소는 표본 축소가 크지만, **문제 구조는 3년 내내 동일**하다.

고전적 trade-off가 corpus 전체에서 가장 반복적으로 확인된다:

```
passthrough  → software mediation 비용 하락
             → 그러나 isolation, memory management, live migration이 모두 어려워진다
```

각 항목에 대한 2024–2026의 공격을 corpus가 모두 담고 있다.

- **memory management 쪽:** VPRI(SOSP24)가 static pinning이 운영 환경에서 DRAM의 최대 50%를
  낭비함을 보이고, To PRI or Not To PRI(OSDI25)는 PCIe PRI/IOPF로 overcommit을 되찾으며,
  HyperAlloc은 IOMMU pinning 하에서도 회수가 가능하도록 allocator를 공유한다.
- **scalability 쪽:** SR-IOV의 고정 VF 수 천장을 HD-IOV(EuroSys24)가 software-mediated
  PASID/queue-pair로, SG-IOV(ASPLOS26)가 socket 단위 하드웨어 분할로 뚫는다.
  `[FACT_FROM_PAPER]` HD-IOV는 2.96배 device density를 보고한다. PRECURSOR 관계로 기록.
- **live migration 쪽:** 3가지 서로 다른 탈출구가 관찰된다 —
  device가 협조하거나(Device-Assisted Live Migration of RDMA Devices, SOSP25),
  host가 보이는 paravirtual 우회로를 두거나(M3U, OSDI26),
  아예 migration을 없애고 CXL로 device를 pooling한다(Oasis, SOSP25).

**동시에 격리 가정이 깨지고 있다.** DSAssassin(HPCA26)은 Intel Scalable IOV가 보장한다는
inter-VM isolation을 device TLB/shared work queue를 통해 우회한다. 즉 I/O virtualization은
성능 문제에서 **보안 문제로 확장되는 중**이다.

## 4. container isolation — namespace/cgroup을 넘어선 것이 확실하다

T5는 15 → 25 → 5다. 2026 수치는 표본 문제이므로, 의미 있는 비교는 2024 대 2025이며
**45건 중 27건이 CORE**로 corpus에서 가장 큰 CORE 집단이다.

질문("namespace/cgroup을 넘어 microkernel/unikernel/split kernel/secure container/Wasm으로
가고 있는가")에 대한 답은 **명확히 그렇다**이며, 근거는 다음 5개 계열이 모두 동시에
존재한다는 사실이다.

1. **microkernel/split-kernel:** HongMeng(OSDI24), MettEagle(OSDI25, 비용·이득 정량화),
   LiteShield(ATC25, userspace μkernel service), SKernel(EuroSys26, split-kernel).
2. **unikernel:** uIO(SoCC24), Memory Matters load-time dedup(SoCC25), SURE(SoCC24).
3. **in-process hardware domain (MPK/CHERI):** AlloyStack(EuroSys25), bpftime(OSDI25),
   Omniglot(OSDI25 best paper), SpecMPK(HPCA25), LightZone(Middleware24, ARM64),
   CHERIoT RTOS(SOSP25).
4. **Wasm:** Empowering WebAssembly with Thin Kernel Interfaces(EuroSys25),
   Roadrunner·WasmEye(Middleware25).
5. **VM-backed secure container:** FastIOV(EuroSys25), "A Hardware-Software Co-Design for
   Efficient Secure Containers"(EuroSys25), JANUS(OSDI26), Erebor(EuroSys25), CofferOS(EuroSys26).

주목할 점은 이들이 **순차적 대체가 아니라 병렬 경쟁**이라는 것이다. 2025–2026에 다섯 계열이
같은 venue에서 동시에 발표된다. corpus는 승자를 보여주지 않는다.

`[INFERENCE]` 다만 방향성은 읽힌다 — 공통 목표는 "VM 수준 격리 강도를 container 수준 시작
지연과 밀도로" 얻는 것이며, 각 계열은 **무엇을 희생할지**만 다르게 고른다(compatibility,
TCB 크기, 이식성, 하드웨어 의존성).

## 5. accelerator virtualization — 제안된 성숙 단계는 부분적으로만 맞다

제시된 가설: `단순 공유 → 공간/시간 분할 → QoS/격리 → migration/preemption → cloud/serverless 추상화`

corpus에 비춘 검증 결과:

- **1단계(단순 공유)는 관측 불가.** MIG/MPS는 corpus 시작 이전에 이미 존재하며, 2024 논문들은
  이미 그 위에서 시작한다. 이 전이는 이 corpus로 확인할 수 없다.
- **2 → 3 (분할 → QoS/격리)은 확인된다.** 2024는 격차를 **드러내는** 논문이 많다
  (STAR, Guardian, Veiled Pathways — MPS/MIG 격리의 취약점). 2025는 그것을 **강화**한다
  (ATC25 kernel-space interception, GPreempt, XSched).
- **3 → 4 → 5 (QoS → migration/preemption → serverless)도 확인된다.**
  PhoenixOS(SOSP25, OS 수준 GPU checkpoint/restore), gCROP(SoCC24),
  Aegaeon(SOSP25, GPU pooling), gShare(ASPLOS26, VM passthrough vGPU),
  F3·Funky(FPGA FaaS), eGPU(HPCA26 industry, 1만 GPU 규모 탄력 공유).

즉 **2단계 이후는 가설대로 진행되지만, 출발점은 가설보다 뒤**다.

**device 일반화**는 실재하나 균일하지 않다.
- GPU: 압도적 다수.
- FPGA: 실질적 계열 형성(vFPIO ATC24, Coyote v2 SOSP25, Funky SoCC25, F3 HPDC25,
  Proteus EuroSys26, μShell OSDI26) — **6–7편으로 두 번째로 성숙한 축**.
- NPU: NeuISA/vNPU(MICRO24) 이후 후속이 거의 없다. **1–2편으로 trend 주장 불가.**
- QPU: HyperQ(OSDI25), QOS(OSDI25) 2편. 흥미롭지만 표본이 없다.
- NVMe/RDMA/SmartNIC: NVMePass(HPCA25), LightPool(HPCA24), OSMOSIS·PeRF(ATC24),
  NADINO(EuroSys26) — 지속적이나 산발적.

## 6. confidential computing — 신뢰 경계가 CPU를 벗어나고 있다

T7은 14 → 11 → 8로 표본 대비 꾸준하며, **방향성은 이 corpus에서 가장 선명한 trend 중 하나**다.

```
2024  CPU/DRAM 중심        VeriSMo, CPC, MIRVerif, HyperTEE, IvLeague
2025  I/O로 확장           RAKIS(SGX 간 고속 I/O), Erebor(untrusted CVM 내 sandbox),
                           ccAI(MICRO25) — PCIe 넘어 GPU/NPU/FPGA로 신뢰 사슬 확장
2026  가속기·상호연결로 일반화  TEEM³, SCALE(CVM + per-GPU TEE + NVLink 간 TEE),
                           동시에 DSAssassin이 그 확장이 만든 새 공격면을 보여줌
```

`[FACT_FROM_PAPER]` ccAI는 신뢰 경계가 PCIe를 넘어 가속기에 이른다고 명시하며, SCALE은
GPU TEE 간 통신 보안 오버헤드를 40–70% 줄인다고 보고한다.

`[INFERENCE]` 단, 이 서사를 직접 지지하는 논문은 **연도당 2–4편**이며 2026 근거는 대부분
abstract 수준이다. 방향성은 말할 수 있으나 정량화는 하지 않는다.

또한 T7 하위 그룹 중 **정확성 검증 계열(VeriSMo, Ghost in the Android Shell, TickTock,
Arm CCA 명세 불일치 탐지, NecoFuzz)** 은 서로 인용·계승 관계가 희박하다. 즉 이 분야는
누적적이라기보다 **병렬적**이다. 이는 relation graph에서 T7 논문 10편이 고립된 것으로도 확인된다.

## 7. serverless — 기구와 소비를 반드시 분리해야 한다

수치상 T8 primary는 2024에 5건, 2025–2026에 0건이다. 이것은 serverless 연구가 사라졌다는
뜻이 **전혀 아니다**. 오히려 반대로, serverless 논문이 corpus에서 가장 많은 축에 속한다.
분류 정책상 대부분이 **CONTEXT**로 갔거나, 기구 논문은 그 기구의 taxonomy(T2/T5/T6)로 갔기 때문이다.

이 구분이 이 corpus가 serverless에 대해 제공하는 핵심 가치다.

- **격리를 싸게 만드는 기구 (읽을 가치 높음):** Sabre(OSDI24), SURE·Faascale(SoCC24),
  Squeezy(EuroSys26), AlloyStack(EuroSys25), Dandelion(SOSP25), Spice(OSDI26, process snapshot),
  PASS(ATC24), Snapipeline·PCLive(SoCC24), FastIOV(EuroSys25).
- **serverless를 소비하는 시스템 (usage context로만):** scheduling, workflow, cost, carbon,
  LLM serving 계열 — EuroSys26 seed의 상당수, CCGrid25/26 대부분, Middleware25 대부분.

2026 EuroSys/CCGrid/HPDC에서 **cost·carbon·billing 분석 논문이 늘어난 것**은 관측되지만,
`[INFERENCE]` 이것이 실제 연구 흐름인지 이번 corpus의 seed 수집 편향인지는 구분할 수 없다.

## 8. 3년을 관통하는 하나의 문장

`[INFERENCE]` corpus 전체를 한 문장으로 요약하면:

> 2024–2026 virtualization 연구는 **"자원을 어떻게 나눌 것인가"에서 "나눈 뒤에도 격리·회수·
> 이동·검증이 가능한가"로** 이동했다.

- 나누기(multiplexing)는 대체로 해결된 문제로 취급된다(MIG/MPS, SR-IOV, cgroup은 baseline).
- 논문들이 실제로 다투는 지점은 그 다음이다: passthrough 후에도 회수할 수 있는가(T2·T3),
  가속기를 나눈 뒤에도 checkpoint·preempt할 수 있는가(T6·T4), container를 빠르게 만든 뒤에도
  격리가 진짜인가(T5·T7), 신뢰 경계를 넓힌 뒤에도 그 경계가 실제로 성립하는가(T7).

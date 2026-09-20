# GLOBAL_AUDIT — 전역 일관성 감사

이 문서는 §18 요구사항에 따라, batch별 초기 분류를 **정답으로 가정하지 않고** corpus 전체를
다시 검토한 결과다. 감사 대상은 12개 venue × 3년(2024–2026), 총 **410건의 검토된 후보**다.

원칙: `initial classification → global-audit classification`. 실질적 재분류는 모두 기록한다.

---

## 0. 감사가 발견한 가장 큰 문제 — access artifact가 trend로 위장하고 있었다

1차 batch 통과 직후 corpus는 다음과 같았다.

```
EuroSys 2024  CORE = 0        EuroSys 2025  CORE = 10      EuroSys 2026  CORE = 8
OSDI    2026  CORE = 2        (그런데 P0는 5건)
```

이 숫자를 그대로 두었다면 "고전적 VM/hypervisor 연구가 2024년에는 EuroSys에서 사라졌다가
2025년에 부활했다"는 **완전히 틀린 trend 결론**이 나왔을 것이다.

실제 원인은 연구 동향이 아니라 **문헌 접근 실패**였다.

- OSDI 2026: 담당 agent가 session limit으로 중단되기 전, 거대한 technical-sessions 목록
  페이지가 fetch 도중 truncate되었다. USENIX는 완전 open-access이므로 논문 자체는 접근
  가능했지만 agent가 거기까지 가지 못했다. 그 결과 VM introspection, nested virtualization,
  post-copy live migration, guest physical address space defragmentation 같은
  **교과서적 CORE 주제 논문 9건이 전부 TITLE_ONLY/CONTEXT/LOW로 기록**되었다.
- EuroSys 2024: ACM DL이 전 경로 403. HD-IOV, Hoda, S-NIC 세 편의 I/O virtualization 논문이
  모두 미회수 상태였다.

**조치:** 감사 전에 targeted retrieval rescue pass를 별도로 수행했다. 37건을 재시도해
**28건을 회수**했다(USENIX presentation-page slug 패턴, 저자 개인 홈페이지 PDF,
GitHub artifact README, Semantic Scholar/OpenAlex abstract API).

rescue 이후:

```
EuroSys 2024  CORE = 3        EuroSys 2025  CORE = 10      EuroSys 2026  CORE = 9
OSDI    2026  CORE = 10
```

이것이 이 감사의 가장 중요한 단일 결과다. **접근 실패를 연구 동향으로 오독하지 않았다.**

---

## 1. 감사 질문별 결과

### Q1. CORE threshold가 venue 간 일관적인가?

rescue 이후 연도별 CORE 비율(DROP 제외한 보존 논문 기준):

| 연도 | 검토 | CORE | SUPPORT | CONTEXT | DROP | 보존 | CORE 비율 |
|---|---|---|---|---|---|---|---|
| 2024 | 167 | 48 | 40 | 49 | 30 | 137 | 35% |
| 2025 | 160 | 46 | 50 | 52 | 12 | 148 | 31% |
| 2026 | 83 | 30 | 14 | 33 | 6 | 77 | 39% |

연도 간 31–39%로 수렴한다. rescue 이전에는 2026이 눈에 띄게 낮았다. **threshold는 현재
연도 간 일관적**이라고 판단한다.

단, **venue별 CORE 비율은 비교 가능한 지표가 아니다.** batch마다 "screen out한 논문에도
record를 만들었는가"가 달랐기 때문이다. 예를 들어 CCGrid 2024는 8건 중 5건이 CORE(63%)인데,
이는 담당 agent가 유망한 후보에만 record를 만들고 나머지는 record 없이 배제했기 때문이다.
반면 MICRO 2024는 17건 중 7건이 DROP record로 명시 보존되었다. **분모가 다르다.**
이 점은 최종 통계 해석 시 반드시 고려해야 한다(§5의 미해결 항목 참조).

### Q2. 초기 batch가 GPU sharing을 virtualization으로 과잉 분류했는가?

아니다. brief의 규칙(기존 MIG/MPS 위에 policy를 얹으면 SUPPORT, 새로운 virtual GPU
abstraction을 만들면 CORE)이 일관되게 적용되었음을 확인했다. 표본 검증:

- SUPPORT로 유지: Orion(EuroSys24, 기존 GPU 위 operator 단위 scheduler),
  ParvaGPU·ESG·RAP(기존 MIG/MPS 조합), Priority-Aware GPU Co-Scheduling(CCGrid26, MPS 위 정책),
  Enhanced SVM(HPDC26, AMD SVM driver 위 eviction 정책), KACE·FluidFaaS·BOER.
- CORE로 승격: gShare(ASPLOS26 — 자체 PDF에서 VM passthrough vGPU 계층 확인),
  Nixie(OSDI26 — transparent temporal multiplexing 기구 자체),
  gVulkan(ATC24 — API forwarding 기반 GPU pooling), PhoenixOS·gCROP(GPU checkpoint/restore).

T6 primary 41건 중 CORE는 16건으로, 무비판적 승격의 징후는 없다.

### Q3. serverless 논문이 CORE/SUPPORT로 과다 유입되었는가?

아니다. 오히려 의도적으로 억제되었다. T8(serverless/cloud abstraction) primary는 CORE+SUPPORT
통틀어 **5건뿐**이고, serverless 논문 대다수는 CONTEXT에 머물렀다. 감사에서 확인한 구분선:

- 격리 경계를 싸게 만드는 **기구**는 CORE/SUPPORT: Sabre, SURE, Faascale, Squeezy,
  AlloyStack, Dandelion, Spice(process snapshot), PASS.
- serverless를 **소비**하는 시스템은 CONTEXT: scheduling, workflow, cost, carbon, LLM serving.

경계 사례 2건은 감사에서 하향 조정된 채로 유지했다: Spice(OSDI26-11)는 VM 경계가 아니라
process 경계의 snapshot이므로 CORE가 아니라 SUPPORT, DVLA(OSDI26-13)는 migration을 black box
lever로만 쓰는 배치 정책이므로 SUPPORT이며 publication_type도 OPERATIONAL_REFERENCE로 정정했다.

### Q4. container runtime 논문과 container isolation 논문이 혼동되었는가?

일부 있었고 **감사에서 수정되었다.** rescue pass에서 SC 2025의 두 건이 재분류되었다.

- coMtainer(SC25-04): CONTEXT → **SUPPORT**. 전문 확인 결과 container image build/metadata
  기구이며 격리 경계를 바꾸지 않는다.
- EDDE(SC25-05): CONTEXT → **SUPPORT**. on-demand edge image pulling으로 역시 runtime 계열.

반대로 격리 구조 자체를 재설계한 논문은 CORE를 유지했다: MettEagle(microkernel 위 container),
HongMeng, LiteShield, SKernel(split-kernel), uIO(unikernel), ConMonitor 계열.
**image/build/pull = SUPPORT, isolation boundary 재설계 = CORE** 라는 선이 현재 corpus 전체에
일관되게 적용되어 있다.

### Q5. pure virtual-memory 논문이 false positive로 남아 있는가?

없다. architecture venue를 중심으로 명시적으로 screen되었고, **DROP 사유 `pure_virtual_memory`
12건**으로 기록되었다. 대표적으로 Marching Page Walks, OASIS, Learning to Walk, SoftWalker,
LATPC, ARIADNE(ASPLOS/MICRO/HPCA 25), Avatar, SUV(MICRO24), ExtMem·Hydra·FBMM·FlexMem(ATC24).

감사에서 특히 중요한 **대조 사례**를 확인했다: MICRO 2024 "Elastic Translations"는 제목과
session이 위 논문들과 사실상 구분되지 않지만, 전문 확인 결과 **KVM nested(stage-2) page table을
직접 관리**하고 virtualized execution 성능을 보고한다. 따라서 brief가 명시한 nested-translation
예외에 해당하여 CORE로 유지했다. 이 한 건이 "제목으로 분류하지 않는다"는 원칙의 실효성을 보여준다.

### Q6. disaggregation과 virtualization이 제대로 분리되었는가?

그렇다. 규칙(disaggregated pool 위에 **virtual resource abstraction**을 세운 경우에만 CORE)이
일관 적용되었다.

- CORE: Blowfish(OSDI26, elastic **VM** memory over disaggregated memory),
  Memstrata/Managing Memory Tiers with CXL **in Virtualized Environments**(OSDI24),
  Demeter(SOSP25, guest delegation), Oasis(SOSP25, PCIe device pooling over CXL).
- SUPPORT: FineMem(OSDI25 — 순수 fine-grained allocator, 확인 후 하향), Nomad, Atlas,
  TrackFM, TECO, PIPM, Cxlalloc, Re-architecting End-host Networking with CXL.
- DROP: SMART, COAXIAL(명시적으로 abstraction을 만들지 않는다고 스스로 밝힘), vCXLGen, CXLMC.

### Q7. application scheduling과 resource virtualization이 구분되었는가?

그렇다. 다만 감사에서 **구조적 발견**이 하나 나왔다. T9(resource management/multi-tenancy)는
primary tag가 14건인데 secondary tag는 63건이다. 즉 **resource management는 대부분 다른 기여를
가진 논문의 부차적 성격**이며, T9를 primary로 갖는 논문은 대체로 SUPPORT 정책 논문이다
(14건 중 CORE는 Mosaic 1건). 진짜 CORE급 resource management 기구
(Memstrata, SweetspotVM, OSMOSIS, PeRF, Demeter, Blowfish, mwait-sched)는 모두 T1/T2/T3 아래에
있고 T9를 secondary로만 갖는다. 이 형태 자체가 유의미한 결론이다.

### Q8. 2024가 2025/26과 같은 기준으로 판정되었는가?

**지금은 그렇다. 그러나 rescue 이전에는 아니었다**(§0). 추가로 확인한 잔여 비대칭:

- SC 2024는 공식 사이트가 robots.txt로 전면 차단되어 **전수 열거가 불가능**했고, keyword
  검색만으로 5건을 찾았다. SC 2024 CORE=0은 **실제 부재가 아니라 탐색 한계**다. 동일하게
  SC 2025도 137편이라는 총수만 확인되고 전체 제목 목록은 열거하지 못했다.
- SoCC 2024는 24건 중 publication_type이 UNKNOWN으로 남은 항목이 12건이다. ACM DL 차단으로
  full/short/industry/vision track 구분을 확인할 수 없었다.

이 두 venue의 통계는 다른 venue와 동일한 신뢰도로 취급해서는 안 된다.

### Q9. 이전 label이 anchoring bias를 만들었는가?

제공된 2025–2026 seed list의 CORE/BROAD/EDGE label은 각 agent에게 전달되지 않았고, seed는
"high-recall 탐색 출발점이며 정답이 아니다"라고 명시되었다. 실제로 seed에 없던 논문이 다수
발견되었고(§4), seed 제목 오류도 정정되었다. 기존 corpus 재사용도 delta 확인용으로만 사용했다.

역방향 bias — 즉 "이전에 CORE였으니 CORE" — 의 징후는 §2의 재분류 목록에서 확인되듯 없다.
28건 중 5건은 오히려 **하향**(CONTEXT → SUPPORT, CONTEXT → DROP)이었다.

---

## 2. 실질적 재분류 기록 (initial → audited)

rescue/audit pass에서 분류 또는 증거 수준이 바뀐 28건.

### 상향 (CONTEXT → CORE), 21건

접근 실패로 TITLE_ONLY였다가 전문/abstract 확보 후 승격된 건이다.

| id | venue | 논문 | 근거 |
|---|---|---|---|
| VIRT-OSDI26-01 | OSDI26 | JANUS | cross-world cooperative nested virtualization 기구 확인 |
| VIRT-OSDI26-02 | OSDI26 | M3U | post-copy live migration의 kernel memory 관리 확인 |
| VIRT-OSDI26-03 | OSDI26 | InfiniDefrag | guest physical address space 재설계 확인 |
| VIRT-OSDI26-04 | OSDI26 | Inside Out (GOODKIT) | VM introspection 재설계 확인 |
| VIRT-OSDI26-05 | OSDI26 | Blowfish | elastic VM memory abstraction 확인 |
| VIRT-OSDI26-07 | OSDI26 | μShell | microkernel 기반 FPGA shell 확인 |
| VIRT-OSDI26-08 | OSDI26 | vBPF | eBPF 가상화 계층 확인 |
| VIRT-OSDI26-09 | OSDI26 | vBOIDs | container용 vCPU 유사 abstraction (경계 판정, §3 참조) |
| VIRT-EUROSYS24-01 | EuroSys24 | HD-IOV | PASID/queue-pair I/O virtualization, artifact 확인 |
| VIRT-EUROSYS24-02 | EuroSys24 | Hoda | OVS dataplane 특화, abstract 확인 |
| VIRT-EUROSYS24-04 | EuroSys24 | S-NIC | SmartNIC hardware isolation, 전문 확인 |
| VIRT-EUROSYS26-13 | EuroSys26 | NADINO | multi-tenant DPU RDMA, preprint 확인 |
| VIRT-HPCA26-03 | HPCA26 | SCALE | CVM + GPU TEE + NVLink 신뢰 경계 확인 |
| VIRT-HPCA26-05 | HPCA26 | DSAssassin | Scalable IOV의 inter-VM isolation 붕괴 확인 |
| VIRT-MIDDLEWARE24-15 | Middleware24 | LightZone | ARM64 in-process isolation, 전문 확인 |
| VIRT-SOCC24-05 | SoCC24 | uIO | unikernel 확장성 기구, 전문 확인 |
| VIRT-SOCC24-06 | SoCC24 | KrustVM | Rust 기반 KVM hypervisor 보안, 전문 확인 |
| VIRT-SOCC24-07 | SoCC24 | Continuous Ballooning | ballooning+migration, 공식 abstract 확인 |
| VIRT-SOCC24-08 | SoCC24 | PCLive | container 복원 pipeline, slides+artifact 확인 |
| VIRT-SOCC24-10 | SoCC24 | Faascale | microVM 수직 memory scaling, artifact 확인 |
| VIRT-SOSP25-01 | SOSP25 | Device-Assisted Live Migration of RDMA Devices | 부분 abstract 확인 |

### 하향 (CONTEXT → SUPPORT), 5건 / (CONTEXT → DROP), 1건 / 증거만 심화, 1건

| id | 변경 | 사유 |
|---|---|---|
| VIRT-OSDI26-11 | CONTEXT → SUPPORT | Spice는 VM이 아니라 **process** 경계 snapshot |
| VIRT-OSDI26-13 | CONTEXT → SUPPORT | DVLA는 migration을 black box로 쓰는 배치 정책 |
| VIRT-SC25-04 | CONTEXT → SUPPORT | coMtainer는 image build 기구(격리 경계 불변) |
| VIRT-SC25-05 | CONTEXT → SUPPORT | EDDE는 image pulling 기구 |
| VIRT-HPCA25-06 | CONTEXT → SUPPORT | RpcNIC는 offload이나 격리 기구는 아님 |
| VIRT-ASPLOS24-17 | CONTEXT → **DROP** | NetRen의 "service migration"은 network 설정 합성이며 VM/container migration과 무관 (`no_virtualization_relation`). 저자 정보도 정정됨 |
| VIRT-HPCA25-05 | 증거 심화 | DPUaudit는 abstract 확보 후에도 CONTEXT 유지(가상 자원 abstraction 없음) |

---

## 3. 감사자가 명시적으로 남기는 경계 판정

다음은 **논쟁 가능한** 판정이며, 이후 재검토가 필요하면 여기부터 보면 된다.

1. **vBOIDs(OSDI26-09) = CORE.** BOID는 container를 위한 명시적 vCPU 유사 abstraction이지만,
   SUPPORT(scheduling 정책)로 볼 여지도 있다. 담당 agent가 borderline으로 자진 신고했다.
2. **HongMeng(SOSP24) = CORE / T5.** VM도 hypervisor도 등장하지 않는 microkernel 논문이다.
   brief가 "microkernel container isolation architecture는 CORE"라고 명시한 조항에 근거했으나,
   이 corpus에서 가장 공격적인 판정이다.
3. **Mosaic(MICRO24) = CORE.** serverless multi-tenancy를 위한 cache/TLB/BTB **하드웨어**
   partitioning이다. "container isolation architecture는 CORE"를 microarchitecture 구조로
   확장 적용한 것이다.
4. **"Virtualization So Light, it Floats!"(HPDC25) = CORE / T10.** floating point 의미론의
   trap-and-emulate이다. 기계 자원 virtualization은 아니지만 **기법이 고전적 CPU
   virtualization과 구조적으로 동일**하다는 근거로 CORE/T10이다. HPDC26 후속작과 EXTENSION
   관계가 확인되었다.
5. **DSAssassin(HPCA26) = CORE.** 공격 논문이다. "VM을 실험 환경으로만 쓰는 공격 논문은 제외"
   규칙에 걸리지만, 이 논문은 **Intel Scalable IOV가 보장한다고 주장하는 inter-VM isolation을
   직접 깨뜨린다**. 따라서 격리 경계에 대한 1차 증거로 간주했다.
6. **CrossMapping(ATC24) = CORE, MEDIUM confidence.** cross-ISA dynamic binary translation을
   소프트웨어 machine virtualization으로 본 판정이다.

## 4. 공급된 seed list에 대한 정정 및 누락

- **seed 제목 오류 정정:** ATC25 "GPreempt" → 공식 "GPREEMPT: GPU Preemptive Scheduling Made
  General and Efficient"; OSDI25 bpftime 항목 → 공식 "Extending Applications Safely and
  Efficiently"; ASPLOS26 Morphlux 제목에서 시스템명 누락; Cremes·Krysha 제목 축약.
  Hydra는 preprint명 "Graalvisor", BOER는 "KACE"로 유통된 이력이 있어 별도 기록했다.
- **seed에 없었으나 발견되어 편입된 주요 논문:** Para-ksm·μEFI·Asterinas·XSched·Omniglot(ATC/OSDI25),
  RAKIS·"A Hardware-Software Co-Design for Efficient Secure Containers"(EuroSys25),
  Confidential Analytics with Scylla·XpuPod/HeteroPod·VLCs(SoCC25),
  Enhanced SVM for GPU Memory Oversubscription(HPDC26) 등.
- **연도 오배정 적발:** ASPLOS 2026 공식 프로그램 페이지에서 수집된 HybridTier와
  "Wave: Offloading Resource Management to SmartNIC Cores"가 DOI 검증 결과 **ASPLOS 2025**
  논문으로 확인되어 제외했다. 같은 유형으로 ASPLOS 2024 프로그램에서 FreePart·Flame·λFS가
  ASPLOS 2023 재발표로 확인되어 제외했다.
- **CCGrid25 quantum-classical FaaS 재검토:** 이전 audit의 REMOVE_DUPLICATE 판정을 재확인했다.
  전문 확인 결과 virtualization 기구 기여가 없어 `DROP / already_analysed_no_delta`로 유지한다.
  반대 증거는 발견되지 않았다.

## 5. 감사가 남기는 미해결 항목

1. **venue별 CORE 비율은 비교 불가.** batch마다 screen-out 논문의 record 생성 정책이 달라
   분모가 다르다. 향후 재실행 시 "배제된 논문도 전부 DROP record로 남긴다"로 통일해야 한다.
2. **SC 2024 / SC 2025는 전수 열거 실패.** SC24는 robots.txt 전면 차단으로 keyword 검색만
   수행했다. 두 해 모두 CORE=0인데 이는 탐색 한계일 가능성이 높다. **corpus 최대의 recall 공백.**
3. **SoCC 2024 publication_type 12건 UNKNOWN.** full/short/industry/vision 구분 미확인.
4. **CORE 25건이 abstract 수준 증거에만 의존.** 목록은 RESEARCH_STATUS.md에 있다.
   특히 SOSP25-01(RDMA device migration)은 mechanism/isolation/state 필드가 UNKNOWN이다.
5. **TITLE_ONLY 63건 잔존.** 2차 rescue에서도 회수 실패한 BASK(EuroSys26),
   Fault Escaping(ASPLOS26), ConMonitor·Snapipeline·TianMen(SoCC24) 등.
6. **HPDC 2026, ASPLOS 2026 population 미확정.** 전자는 사이트 TLS 인증서 오류,
   후자는 공식 페이지의 "167 unique papers" 주장과 실제 scrape 결과가 불일치한다.

해결 기록: VIRT-CCGRID24-03/06의 중복·오류 DOI는 각각
`10.1109/CCGrid59990.2024.00084`와 `10.1109/CCGrid59990.2024.00064`로 정정됐고,
전 corpus 중복 DOI 재검사는 0건이다.

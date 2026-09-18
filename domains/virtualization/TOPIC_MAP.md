# TOPIC_MAP — virtualization

## 계층 지도

```
                    [T8] Serverless / Cloud abstraction
                    [T9] Resource management / Multi-tenancy
                              ↑  소비
    ─────────────────────────────────────────────────────────
                      virtualization 기구
    ─────────────────────────────────────────────────────────
     [T5] Container /        [T6] Accelerator      [T7] Confidential /
          lightweight             virtualization        security isolation
          isolation
              ↑                        ↑                      ↑
     [T1] CPU / machine     [T2] Memory          [T3] I/O·device
          virtualization         virtualization       virtualization
              ↑                        ↑                      ↑
    ─────────────────────────────────────────────────────────
          [T4] Migration / Checkpoint / State  (모든 계층을 가로지름)
    ─────────────────────────────────────────────────────────
                    Physical Resource
              (CPU, DRAM, NIC, GPU, FPGA, NVMe, CXL fabric, QPU)
```

T4는 독립 계층이라기보다 **횡단 관심사**다. T1의 CPU state, T2의 guest memory,
T3의 device state, T5의 container state, T6의 GPU state가 모두 "옮길 수 있는가"라는
같은 질문을 받는다.

## 주요 연결선 (근거 있는 것만)

| 연결 | 내용 | 대표 논문 |
|---|---|---|
| T3 → T2 | passthrough가 강제하는 pinning이 memory 회수를 막는다 | VPRI(SOSP24) → To PRI(OSDI25) → HyperAlloc(EuroSys25) |
| T3 → T4 | passthrough device의 state를 어떻게 옮기는가 | Device-Assisted RDMA Migration(SOSP25), M3U(OSDI26), Oasis(SOSP25, migration 회피) |
| T1 → T5 | nested virtualization이 secure container의 구현 수단이 된다 | HyperTurtle(ATC25) → JANUS(OSDI26) |
| T2 → T8 | VM memory elasticity가 serverless 밀도를 만든다 | HyperAlloc(EuroSys25) ↔ Faascale(SoCC24) ↔ Squeezy(EuroSys26) |
| T6 → T4 | 가속기에도 checkpoint/restore 문제가 반복된다 | PhoenixOS(SOSP25), gCROP(SoCC24) |
| T6 → T8 | 가속기가 serverless 자원이 된다 | F3(HPDC25), Funky(SoCC25), gShare(ASPLOS26) |
| T7 → T3 | 신뢰 경계가 PCIe를 넘어 device로 확장된다 | ccAI(MICRO25), SCALE(HPCA26) |
| T7 ↔ T3 | 그 확장이 새 공격면을 만든다 | DSAssassin(HPCA26)이 Scalable IOV 격리를 우회 |
| T1 → T2 | 2단계 주소 변환 비용 | Direct Memory Translation(ASPLOS24), Elastic Translations(MICRO24) |
| T2 ↔ 분산 | disaggregation 위에 virtual abstraction을 세울 때만 CORE | Memstrata(OSDI24), Demeter(SOSP25), Blowfish(OSDI26) |

## 잘 연결되지 않은 부분 (이것도 결론이다)

- **T7 정확성·검증 계열이 고립되어 있다.** VeriSMo, Ghost in the Android Shell, TickTock,
  Arm CCA 명세 검증, NecoFuzz 등 10편이 서로 인용·계승 관계를 거의 갖지 않는다.
  이 분야는 누적적이라기보다 **병렬적**이다.
- **T8은 자체 규모가 작다**(primary 5). serverless 기구 논문이 각자의 taxonomy로
  흩어졌기 때문이며, 이는 의도된 분류 결과다.
- **T1 진입점 논문들이 흩어져 있다.** SweetspotVM, UTwinVM, PvCC, CrossMapping은 vCPU
  scheduling이라는 공통 주제를 갖지만 상호 참조가 없다.
- **CXL programming-model 논문 3편(ASPLOS26)** 은 memory elasticity 계보와 인접하지만
  전혀 연결되지 않는다. "virtual resource abstraction 없는 순수 disaggregation은 CORE 계보에
  붙지 않는다"는 분류 원칙과 일치하는 결과다.

전체 관계 그래프와 hub 논문은 `synthesis/CROSS_PAPER_RELATIONS.md`에 있다.
최대 hub는 `VIRT-EUROSYS25-03` HyperAlloc(관계 11개)이다.

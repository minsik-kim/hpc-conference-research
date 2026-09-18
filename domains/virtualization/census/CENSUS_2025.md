# CENSUS_2025

2025년 12개 venue census 결과. `population`은 공식 프로그램/proceedings에서 확인한
main-track 논문 수이며, 확인 실패 시 UNKNOWN이다. `examined`는 이 작업에서 개별 record를
생성해 검토한 후보 수다.

| venue | population | 근거 | examined | CORE | SUPPORT | CONTEXT | DROP |
|---|---|---|---|---|---|---|---|
| EuroSys | UNKNOWN | 미기록 | 18 | 10 | 3 | 5 | 0 |
| OSDI | 53 | https://www.usenix.org/sites/default/files/osdi25-contents | 15 | 6 | 6 | 2 | 1 |
| SOSP | UNKNOWN | 미기록 | 17 | 10 | 5 | 2 | 0 |
| ATC | 100 | https://www.usenix.org/sites/default/files/atc25_contents. | 18 | 6 | 9 | 3 | 0 |
| SoCC | 67 | https://acmsocc.org/2025/schedule.html ; cross-checked aga | 23 | 4 | 6 | 11 | 2 |
| ASPLOS | UNKNOWN | 미기록 | 14 | 4 | 5 | 5 | 0 |
| SC | 137 | https://sc25.supercomputing.org/2025/09/you-asked-we-liste | 7 | 0 | 4 | 2 | 1 |
| HPDC | 25 | https://hpdc.sci.utah.edu/2025/program.html | 4 | 2 | 1 | 1 | 0 |
| Middleware | UNKNOWN | 미기록 | 14 | 2 | 7 | 4 | 1 |
| CCGrid | UNKNOWN | 미기록 | 8 | 0 | 1 | 6 | 1 |
| HPCA | 121 | https://hpca-conf.org/2025/main-program/ | 12 | 1 | 2 | 6 | 3 |
| MICRO | 123 | https://www.microarch.org/micro58/program/ | 10 | 1 | 1 | 5 | 3 |
| **합계** | | | **160** | **46** | **50** | **52** | **12** |

## Taxonomy 분포 (CORE+SUPPORT)

| tax | n |
|---|---|
| T1 | 4 |
| T2 | 9 |
| T3 | 12 |
| T4 | 4 |
| T5 | 25 |
| T6 | 20 |
| T7 | 11 |
| T9 | 5 |
| T10 | 6 |

## 2025 CORE 논문 목록

- `VIRT-ASPLOS25-01` **Vela: A Virtualized LLM Training System with GPU Direct RoCE** — ASPLOS / T3 / P1 / 증거 ABSTRACT
- `VIRT-ASPLOS25-02` **HyperHammer: Breaking Free from KVM-Enforced Isolation** — ASPLOS / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-ASPLOS25-12` **Coach: Exploiting Temporal Patterns for All-Resource Oversubscription in Cloud Platforms** — ASPLOS / T2 / P1 / 증거 DESIGN_EVAL
- `VIRT-ASPLOS25-13` **Harmonia: A Unified Framework for Heterogeneous FPGA Acceleration in the Cloud** — ASPLOS / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC25-01` **LITESHIELD: Secure Containers via Lightweight, Composable Userspace μKernel Services** — ATC / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC25-02` **Accelerating Nested Virtualization with HyperTurtle** — ATC / T1 / P1 / 증거 FULL
- `VIRT-ATC25-03` **Efficient Performance-Aware GPU Sharing with Compatibility and Isolation through Kernel Space Interception** — ATC / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC25-14` **Para-ksm: Parallelized Memory Deduplication with Data Streaming Accelerator** — ATC / T2 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC25-15` **μEFI: A Microkernel-Style UEFI with Isolation and Transparency** — ATC / T7 / P2 / 증거 DESIGN_EVAL
- `VIRT-ATC25-16` **ASTERINAS: A Linux ABI-Compatible, Rust-Based Framekernel OS with a Small and Sound TCB** — ATC / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-EUROSYS25-01` **FastIOV: Fast Startup of Passthrough Network I/O Virtualization for Secure Containers** — EuroSys / T3 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS25-03` **HyperAlloc: Efficient VM Memory De/Inflation via Hypervisor-Shared Page-Frame Allocators** — EuroSys / T2 / P1 / 증거 FULL
- `VIRT-EUROSYS25-04` **Optimizing Task Scheduling in Cloud VMs with Accurate vCPU Abstraction** — EuroSys / T1 / P1 / 증거 FULL
- `VIRT-EUROSYS25-05` **Erebor: A Drop-In Sandbox Solution for Private Data Processing in Untrusted Confidential Virtual Machines** — EuroSys / T7 / P1 / 증거 FULL
- `VIRT-EUROSYS25-06` **Byte vSwitch: A High-Performance Virtual Switch for Cloud Networking** — EuroSys / T3 / P2 / 증거 ABSTRACT
- `VIRT-EUROSYS25-08` **Phantom: Virtualizing Switch Register Resources for Accurate Sketch-based Network Measurement** — EuroSys / T10 / P3 / 증거 ABSTRACT
- `VIRT-EUROSYS25-14` **AlloyStack: A Library Operating System for Serverless Workflow Applications** — EuroSys / T5 / P1 / 증거 FULL
- `VIRT-EUROSYS25-16` **Empowering WebAssembly with Thin Kernel Interfaces** — EuroSys / T5 / P1 / 증거 FULL
- `VIRT-EUROSYS25-17` **A Hardware-Software Co-Design for Efficient Secure Containers** — EuroSys / T5 / P1 / 증거 FULL
- `VIRT-EUROSYS25-18` **RAKIS: Secure Fast I/O Primitives Across Trust Boundaries on Intel SGX** — EuroSys / T7 / P2 / 증거 FULL
- `VIRT-HPCA25-01` **NVMePass: A Lightweight, High-performance and Scalable NVMe Virtualization Architecture with I/O Queues Passthrough** — HPCA / T3 / P1 / 증거 DESIGN_EVAL
- `VIRT-HPDC25-01` **F3: An FPGA-accelerated FaaS Framework** — HPDC / T6 / P0 / 증거 FULL
- `VIRT-HPDC25-03` **Virtualization So Light, it Floats! Accelerating Floating Point Virtualization** — HPDC / T10 / P2 / 증거 FULL
- `VIRT-MICRO25-01` **ccAI: A Compatible and Confidential System for AI Computing** — MICRO / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-MIDDLEWARE25-01` **Clair Obscur: The Light and Shadow of System Call Interposition – From Pitfalls to Solutions with K23** — Middleware / T5 / P1 / 증거 FULL
- `VIRT-MIDDLEWARE25-02` **Full Trust Alchemist: Reforging Attestation for Cloud-based Confidential Workloads** — Middleware / T7 / P1 / 증거 ABSTRACT
- `VIRT-OSDI25-01` **To PRI or Not To PRI, That's the Question** — OSDI / T3 / P0 / 증거 DESIGN_EVAL
- `VIRT-OSDI25-03` **MettEagle: Costs and Benefits of Implementing Containers on Microkernels** — OSDI / T5 / P0 / 증거 FULL
- `VIRT-OSDI25-04` **Quantum Virtual Machines** — OSDI / T1 / P1 / 증거 FULL
- `VIRT-OSDI25-09` **Deterministic Client: Enforcing Determinism on Untrusted Machine Code** — OSDI / T5 / P1 / 증거 FULL
- `VIRT-OSDI25-10` **Extending Applications Safely and Efficiently** — OSDI / T5 / P1 / 증거 FULL
- `VIRT-OSDI25-15` **Building Bridges: Safe Interactions with Foreign Languages through Omniglot** — OSDI / T5 / P1 / 증거 FULL
- `VIRT-SOSP25-01` **Device-Assisted Live Migration of RDMA Devices** — SOSP / T4 / P1 / 증거 ABSTRACT
- `VIRT-SOSP25-02` **Demeter: A Scalable and Elastic Tiered Memory Solution for Virtualized Cloud via Guest Delegation** — SOSP / T2 / P1 / 증거 ABSTRACT
- `VIRT-SOSP25-03` **Ghost in the Android Shell: Pragmatic Test-oracle Specification of a Production Hypervisor** — SOSP / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-04` **The Design and Implementation of a Virtual Firmware Monitor** — SOSP / T7 / P0 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-06` **PhoenixOS: Concurrent OS-level GPU Checkpoint and Restore with Validated Speculation** — SOSP / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-08` **Unlocking True Elasticity for the Cloud-Native Era with Dandelion** — SOSP / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-10` **Coyote v2: Raising the Level of Abstraction for Data Center FPGAs** — SOSP / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-13` **μFork: Supporting POSIX fork Within a Single-Address-Space OS** — SOSP / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-14` **LithOS: An Operating System for Efficient Machine Learning on GPUs** — SOSP / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOSP25-15` **Tai Chi: A General High-Efficiency Scheduling Framework for SmartNICs in Hyperscale Clouds** — SOSP / T1 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOCC25-01` **Hydra: Virtualized Multi-Language Runtime for High-Density Serverless Platforms** — SoCC / T5 / P1 / 증거 FULL
- `VIRT-SOCC25-02` **Memory Matters: Load-Time Deduplication for Unikernels** — SoCC / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOCC25-05` **Funky: Cloud-Native FPGA Virtualization and Orchestration** — SoCC / T6 / P0 / 증거 FULL
- `VIRT-SOCC25-21` **Rethinking Tiered Memory Management in Cloud Data Centers** — SoCC / T2 / P1 / 증거 ABSTRACT_INTRO

## 2025 배제(DROP) 기록 — 12건


### already_analysed_no_delta (1건)
- `VIRT-CCGRID25-08` Choreography and Profiling of Quantum-Classical FaaS Workflows on Hybrid Clouds — CCGrid

### keyword_false_positive (1건)
- `VIRT-HPCA25-12` Let-Me-In: (Still) Employing In-pointer Bounds Metadata for Fine-grained GPU Memory Safety — HPCA

### no_virtualization_relation (2건)
- `VIRT-SOCC25-11` Serverless Elasticsearch: the Architecture Transformation from Stateful to Stateless — SoCC
- `VIRT-SC25-07` Bridging the Gap Between Binary and Source Based Package Management in Spack — SC

### publication_criterion (2건)
- `VIRT-SOCC25-07` CPU-Limits kill Performance: Time to rethink Resource Control — SoCC
- `VIRT-MIDDLEWARE25-11` svc-hook: hooking system calls on ARM64 by binary rewriting — Middleware

### pure_virtual_memory (6건)
- `VIRT-OSDI25-12` EMT: An OS Framework for New Memory Translation Architectures — OSDI
- `VIRT-HPCA25-10` Marching Page Walks: Batching and Concurrent Page Table Walks for Enhancing GPU Throughput — HPCA
- `VIRT-HPCA25-11` OASIS: Object-Aware Page Management for Multi-GPU Systems — HPCA
- `VIRT-MICRO25-04` SoftWalker: Supporting Software Page Table Walk for Irregular GPU Applications — MICRO
- `VIRT-MICRO25-05` LATPC: Accelerating GPU Address Translation Using Locality-Aware TLB Prefetching and MSHR Compression — MICRO
- `VIRT-MICRO25-06` Learning to Walk: Architecting Learned Virtual Memory Translation — MICRO

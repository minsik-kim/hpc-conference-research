# CENSUS_2024

2024년 12개 venue census 결과. `population`은 공식 프로그램/proceedings에서 확인한
main-track 논문 수이며, 확인 실패 시 UNKNOWN이다. `examined`는 이 작업에서 개별 record를
생성해 검토한 후보 수다.

| venue | population | 근거 | examined | CORE | SUPPORT | CONTEXT | DROP |
|---|---|---|---|---|---|---|---|
| EuroSys | 71 | https://2024.eurosys.org/accepted-papers.html (cross-check | 9 | 3 | 4 | 1 | 1 |
| OSDI | 43 | https://www.usenix.org/conference/osdi24/technical-session | 12 | 4 | 4 | 2 | 2 |
| SOSP | 43 | https://sigops.org/s/conferences/sosp/2024/accepted.html ( | 9 | 4 | 1 | 3 | 1 |
| ATC | 77 | https://www.usenix.org/sites/default/files/atc24-contents. | 26 | 9 | 5 | 4 | 8 |
| SoCC | 62 | https://acmsocc.org/2024/schedule.html (cross-checked agai | 24 | 7 | 1 | 16 | 0 |
| ASPLOS | UNKNOWN | 미기록 | 21 | 4 | 8 | 4 | 5 |
| SC | UNKNOWN | 미기록 | 5 | 0 | 2 | 2 | 1 |
| HPDC | UNKNOWN | 미기록 | 7 | 0 | 2 | 4 | 1 |
| Middleware | 39 | https://middleware-conf.github.io/2024/program/full-progra | 16 | 4 | 7 | 5 | 0 |
| CCGrid | 67 | dblp.org/db/conf/ccgrid/ccgrid2024.html (page-range analys | 8 | 5 | 0 | 3 | 0 |
| HPCA | 75 | https://www.hpca-conf.org/2024/program/main.php (full sess | 13 | 3 | 4 | 2 | 4 |
| MICRO | 113 | https://microarch.org/micro57/program/ (full session-by-se | 17 | 5 | 2 | 3 | 7 |
| **합계** | | | **167** | **48** | **40** | **49** | **30** |

## Taxonomy 분포 (CORE+SUPPORT)

| tax | n |
|---|---|
| T1 | 4 |
| T2 | 11 |
| T3 | 11 |
| T4 | 9 |
| T5 | 15 |
| T6 | 14 |
| T7 | 14 |
| T8 | 5 |
| T9 | 5 |

## 2024 CORE 논문 목록

- `VIRT-ASPLOS24-01` **Direct Memory Translation for Virtualized Clouds** — ASPLOS / T2 / P1 / 증거 FULL
- `VIRT-ASPLOS24-02` **Verifying Rust Implementation of Page Tables in a Software Enclave Hypervisor** — ASPLOS / T7 / P1 / 증거 FULL
- `VIRT-ASPLOS24-03` **GMLake: Efficient and Transparent GPU Memory Defragmentation for Large-scale DNN Training with Virtual Memory Stitching** — ASPLOS / T6 / P1 / 증거 DESIGN
- `VIRT-ASPLOS24-04` **Lightweight Fault Isolation: Practical, Efficient, and Secure Software Sandboxing** — ASPLOS / T5 / P1 / 증거 FULL
- `VIRT-ATC24-04` **PeRF: Preemption-enabled RDMA Framework** — ATC / T3 / P2 / 증거 DESIGN_EVAL
- `VIRT-ATC24-06` **OSMOSIS: Enabling Multi-Tenancy in Datacenter SmartNICs** — ATC / T3 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC24-14` **A Secure, Fast, and Resource-Efficient Serverless Platform with Function REWIND** — ATC / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC24-19` **Expeditious High-Concurrency MicroVM SnapStart in Persistent Memory with an Augmented Hypervisor** — ATC / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-ATC24-20` **Taming Hot Bloat Under Virtualization with HugeScope** — ATC / T2 / P1 / 증거 FULL
- `VIRT-ATC24-21` **CrossMapping: Harmonizing Memory Consistency in Cross-ISA Binary Translation** — ATC / T1 / P2 / 증거 DESIGN_EVAL
- `VIRT-ATC24-22` **CPC: Flexible, Secure, and Efficient CVM Maintenance with Confidential Procedure Calls** — ATC / T7 / P0 / 증거 FULL
- `VIRT-ATC24-23` **gVulkan: Scalable GPU Pooling for Pixel-Grained Rendering in Ray Tracing** — ATC / T6 / P2 / 증거 DESIGN_EVAL
- `VIRT-ATC24-24` **vFPIO: A Virtual I/O Abstraction for FPGA-accelerated I/O Devices** — ATC / T3 / P1 / 증거 FULL
- `VIRT-CCGRID24-01` **SweetspotVM: Oversubscribing CPU without Sacrificing VM Performance** — CCGrid / T1 / P1 / 증거 DESIGN_EVAL
- `VIRT-CCGRID24-02` **Tackling Memory Footprint Expansion During Live Migration of Virtual Machines** — CCGrid / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-CCGRID24-03` **Incorporating Memory Sharing-awareness in Multi-VM Live Migration** — CCGrid / T4 / P2 / 증거 ABSTRACT
- `VIRT-CCGRID24-04` **vASP: Full VM Life-cycle Protection Based on Active Security Processor Architecture** — CCGrid / T7 / P2 / 증거 ABSTRACT
- `VIRT-CCGRID24-05` **Workload-Aware Live Migratable Cloud Instance Detector** — CCGrid / T4 / P2 / 증거 DESIGN_EVAL
- `VIRT-EUROSYS24-01` **HD-IOV: SW-HW Co-designed I/O Virtualization with Scalability and Flexibility for Hyper-Density Cloud** — EuroSys / T3 / P1 / 증거 DESIGN_EVAL
- `VIRT-EUROSYS24-02` **Hoda: a High-performance Open vSwitch Dataplane with Multiple Specialized Data Paths** — EuroSys / T3 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS24-04` **SmartNIC Security Isolation in the Cloud with S-NIC** — EuroSys / T3 / P1 / 증거 FULL
- `VIRT-HPCA24-01` **Data Enclave: A Data-Centric Trusted Execution Environment** — HPCA / T7 / P1 / 증거 FULL
- `VIRT-HPCA24-04` **DockerSSD: Containerized In-Storage Processing and Hardware Acceleration for Computational SSDs** — HPCA / T5 / P2 / 증거 DESIGN
- `VIRT-HPCA24-05` **A Quantum Computer Trusted Execution Environment** — HPCA / T7 / P2 / 증거 DESIGN
- `VIRT-MICRO24-01` **Hardware-Assisted Virtualization of Neural Processing Units for Cloud Platforms** — MICRO / T6 / P0 / 증거 FULL
- `VIRT-MICRO24-02` **Elastic Translations: Fast virtual memory with multiple translation sizes** — MICRO / T2 / P1 / 증거 DESIGN_EVAL
- `VIRT-MICRO24-04` **HyperTEE: A Decoupled TEE Architecture with Secure Enclave Management** — MICRO / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-MICRO24-15` **IvLeague: Side Channel-resistant Secure Architectures Using Isolated Domains of Dynamic Integrity Trees** — MICRO / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-MICRO24-17` **Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments** — MICRO / T9 / P1 / 증거 FULL
- `VIRT-MIDDLEWARE24-01` **UTwinVM: Reliable hints on the effects of hypervisor updates on VMs in the Cloud** — Middleware / T1 / P2 / 증거 ABSTRACT_INTRO
- `VIRT-MIDDLEWARE24-02` **vPIM: Processing-in-Memory Virtualization** — Middleware / T6 / P2 / 증거 DESIGN_EVAL
- `VIRT-MIDDLEWARE24-03` **PvCC: A vCPU Scheduling Policy for DPDK-applied Systems at Multi-Tenant Edge Data Centers** — Middleware / T1 / P2 / 증거 DESIGN_EVAL
- `VIRT-MIDDLEWARE24-15` **LightZone: Lightweight Hardware-Assisted In-Process Isolation for ARM64** — Middleware / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI24-01` **Sabre: Hardware-Accelerated Snapshot Compression for Serverless MicroVMs** — OSDI / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI24-02` **Managing Memory Tiers with CXL in Virtualized Environments** — OSDI / T2 / P0 / 증거 FULL
- `VIRT-OSDI24-03` **Microkernel Goes General: Performance and Compatibility in the HongMeng Production Microkernel** — OSDI / T5 / P1 / 증거 FULL
- `VIRT-OSDI24-04` **VeriSMo: A Verified Security Module for Confidential VMs** — OSDI / T7 / P0 / 증거 FULL
- `VIRT-SOSP24-01` **vSoC: Efficient Virtual System-on-Chip on Heterogeneous Hardware** — SOSP / T3 / P0 / 증거 FULL
- `VIRT-SOSP24-02` **VPRI: Efficient I/O Page Fault Handling via Software-Hardware Co-Design for IaaS Clouds** — SOSP / T3 / P0 / 증거 FULL
- `VIRT-SOSP24-03` **Fast & Safe IO Memory Protection** — SOSP / T3 / P0 / 증거 FULL
- `VIRT-SOSP24-04` **Unifying serverless and microservice workloads with SigmaOS** — SOSP / T5 / P1 / 증거 FULL
- `VIRT-SOCC24-01` **On-demand and Parallel Checkpoint/Restore for GPU Applications** — SoCC / T6 / P1 / 증거 FULL
- `VIRT-SOCC24-04` **SURE: Secure Unikernels Make Serverless Computing Rapid and Efficient** — SoCC / T5 / P1 / 증거 ABSTRACT_INTRO
- `VIRT-SOCC24-05` **uIO: Lightweight and Extensible Unikernels** — SoCC / T5 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOCC24-06` **Securing a Multiprocessor KVM Hypervisor with Rust** — SoCC / T7 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOCC24-07` **Towards Swap-Free, Continuous Ballooning for Fast, Cloud-Based Virtual Machine Migrations** — SoCC / T2 / P1 / 증거 ABSTRACT
- `VIRT-SOCC24-08` **PCLive: Pipelined Restoration of Application Containers for Reduced Service Downtime** — SoCC / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-SOCC24-10` **Faascale: Scaling MicroVM Vertically for Serverless Computing with Memory Elasticity** — SoCC / T2 / P1 / 증거 DESIGN

## 2024 배제(DROP) 기록 — 30건


### generic_application (1건)
- `VIRT-ASPLOS24-21` Characterizing a Memory Allocator at Warehouse Scale — ASPLOS

### keyword_false_positive (9건)
- `VIRT-EUROSYS24-09` Validating Database System Isolation Level Implementations with Version Certificate Recovery — EuroSys
- `VIRT-OSDI24-11` ACCL+: an FPGA-Based Collective Engine for Distributed Applications — OSDI
- `VIRT-OSDI24-12` Beaver: Practical Partial Snapshots for Distributed Cloud Services — OSDI
- `VIRT-SOSP24-09` Uncovering Nested Data Parallelism and Data Reuse in DNN Computation with FractalTensor — SOSP
- `VIRT-ASPLOS24-18` CC-NIC: a Cache-Coherent Interface to the NIC — ASPLOS
- `VIRT-ASPLOS24-19` Scaling Up Memory Disaggregated Applications with SMART — ASPLOS
- `VIRT-ASPLOS24-20` MemSnap μCheckpoints: A Data Single Level Store for Fearless Persistence — ASPLOS
- `VIRT-SC24-03` COAXIAL: A CXL-Centric Memory System for Scalable Servers — SC
- `VIRT-HPCA24-07` MINOS: Distributed Consistency and Persistency Protocol Implementation & Offloading to SmartNICs — HPCA

### no_virtualization_relation (15건)
- `VIRT-ATC24-09` HydraRPC: RPC in the CXL Era — ATC
- `VIRT-ATC24-13` Metis: Fast Automatic Distributed Training on Heterogeneous GPUs — ATC
- `VIRT-ATC24-17` FBMM: Making Memory Management Extensible With Filesystems — ATC
- `VIRT-ATC24-18` FlexMem: Adaptive Page Profiling and Migration for Tiered Memory — ATC
- `VIRT-ATC24-25` Centimani: Enabling Fast AI Accelerator Selection for DNN Training with a Novel Performance Predictor — ATC
- `VIRT-ASPLOS24-17` NetRen: Service Migration-Driven Network Renascence with Synthesizing Updated Configuration — ASPLOS
- `VIRT-HPDC24-07` IDT: Intelligent Data Placement for Multi-tiered Main Memory with Reinforcement Learning — HPDC
- `VIRT-HPCA24-10` GRIT: Enhancing Multi-GPU Performance with Fine-Grained Dynamic Page Placement — HPCA
- `VIRT-HPCA24-11` RELIEF: Relieving Memory Pressure In SoCs Via Data Movement-Aware Accelerator Scheduling — HPCA
- `VIRT-HPCA24-12` Data Motion Acceleration: Chaining Cross-Domain Multi Accelerators — HPCA
- `VIRT-MICRO24-09` Low-overhead General-purpose Near-Data Processing in CXL Memory Expanders — MICRO
- `VIRT-MICRO24-10` PIM-MMU: A Memory Management Unit for Accelerating Data Transfers in Commercial PIM Systems — MICRO
- `VIRT-MICRO24-11` StarNUMA: Mitigating NUMA Challenges with Memory Pooling — MICRO
- `VIRT-MICRO24-12` NeoMem: Hardware/Software Co-Design for CXL-Native Memory Tiering — MICRO
- `VIRT-MICRO24-13` Demystifying a CXL Type-2 Device: A Heterogeneous Cooperative Computing Perspective — MICRO

### pure_virtual_memory (5건)
- `VIRT-ATC24-10` ExtMem: Enabling Application-Aware Virtual Memory Management for Data-Intensive Applications — ATC
- `VIRT-ATC24-11` Scalable and Effective Page-table and TLB management on NUMA Systems — ATC
- `VIRT-ATC24-26` Every Mapping Counts in Large Amounts: Folio Accounting — ATC
- `VIRT-MICRO24-05` A Case for Speculative Address Translation with Rapid Validation for GPUs — MICRO
- `VIRT-MICRO24-06` SUV: Static analysis guided Unified Virtual Memory — MICRO

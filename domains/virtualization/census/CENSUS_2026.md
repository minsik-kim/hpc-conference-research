# CENSUS_2026

2026년 12개 venue census 결과. `population`은 공식 프로그램/proceedings에서 확인한
main-track 논문 수이며, 확인 실패 시 UNKNOWN이다. `examined`는 이 작업에서 개별 record를
생성해 검토한 후보 수다.

> 2026은 **2026-09-18 KST 기준 이미 개최된 venue만** 포함한다. 미개최 venue는 제외했다.

| venue | population | 근거 | examined | CORE | SUPPORT | CONTEXT | DROP |
|---|---|---|---|---|---|---|---|
| EuroSys | UNKNOWN | 미기록 | 24 | 9 | 5 | 9 | 1 |
| OSDI | UNKNOWN | 미기록 | 14 | 10 | 2 | 2 | 0 |
| SOSP | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| ATC | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| SoCC | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| ASPLOS | UNKNOWN (approximately 167-190; two DOI-distinct proceedings volumes confirmed) | https://www.asplos-conference.org/asplos2026/program/ | 21 | 6 | 5 | 6 | 4 |
| SC | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| HPDC | UNKNOWN | Event metadata via Crossref (HPDC '26: 35th International  | 4 | 1 | 0 | 3 | 0 |
| Middleware | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| CCGrid | 74 | https://ccgrid2026.org/programs.html (full program PDF: ht | 9 | 1 | 2 | 6 | 0 |
| HPCA | 122 | https://dblp.org/db/conf/hpca/hpca2026.html | 11 | 3 | 0 | 7 | 1 |
| MICRO | — | 이번 census에서 후보 없음 또는 미개최 | 0 | 0 | 0 | 0 | 0 |
| **합계** | | | **83** | **30** | **14** | **33** | **6** |

## Taxonomy 분포 (CORE+SUPPORT)

| tax | n |
|---|---|
| T1 | 5 |
| T2 | 6 |
| T3 | 5 |
| T4 | 4 |
| T5 | 5 |
| T6 | 7 |
| T7 | 8 |
| T9 | 4 |

## 2026 CORE 논문 목록

- `VIRT-ASPLOS26-01` **SG-IOV: Socket-Granular I/O Virtualization for SmartNIC-Based Container Networks** — ASPLOS / T3 / P1 / 증거 DESIGN
- `VIRT-ASPLOS26-02` **gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform** — ASPLOS / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-ASPLOS26-03` **TEEM³: Core-Independent and Cooperating Trusted Execution Environments** — ASPLOS / T7 / P2 / 증거 ABSTRACT
- `VIRT-ASPLOS26-04` **WorksetEnclave: Towards Optimizing Cold Starts in Confidential Serverless with Workset-Based Enclave Restore** — ASPLOS / T7 / P1 / 증거 ABSTRACT
- `VIRT-ASPLOS26-06` **Detecting Inconsistencies in Arm CCA's Formally Verified Specification** — ASPLOS / T7 / P1 / 증거 ABSTRACT
- `VIRT-ASPLOS26-17` **CEMU: Enabling Full-System Emulation of Computational Storage beyond Hardware Limits** — ASPLOS / T3 / P2 / 증거 ABSTRACT_INTRO
- `VIRT-CCGRID26-01` **TelePod: Live Migration for Stateful Containers** — CCGrid / T4 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS26-01` **CofferOS: Hardening OS-level Virtualization with Rust** — EuroSys / T5 / P2 / 증거 ABSTRACT
- `VIRT-EUROSYS26-02` **Proteus: Heterogeneous FPGA Virtualization** — EuroSys / T6 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS26-03` **NecoFuzz: Effective Fuzzing of Nested Virtualization via Fuzz-Harness Virtual Machines** — EuroSys / T1 / P1 / 증거 FULL
- `VIRT-EUROSYS26-04` **Everything You Need to Know About Virtual Machine Live Migration Between Heterogeneous Processors** — EuroSys / T4 / P0 / 증거 ABSTRACT
- `VIRT-EUROSYS26-05` **Squeezy: Rapid VM Memory Reclamation for Serverless Functions** — EuroSys / T2 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS26-06` **SKernel: An Elastic and Efficient Secure Container System at Scale with a Split-Kernel Architecture** — EuroSys / T5 / P1 / 증거 ABSTRACT_INTRO
- `VIRT-EUROSYS26-13` **Not A DPU in Name Only! Unleashing RDMA-capable DPUs in Multi-Tenant Serverless Clouds with NADINO** — EuroSys / T3 / P1 / 증거 DESIGN_EVAL
- `VIRT-EUROSYS26-18` **Pyramid: A Secure, Resource-Efficient, and Pluggable Kubernetes for Multi-Tenancy** — EuroSys / T5 / P1 / 증거 ABSTRACT
- `VIRT-EUROSYS26-19` **RoPeerTo: A Datacenter-Scale Architecture for Peer-To-Peer DMA between GPUs and FPGAs** — EuroSys / T3 / P2 / 증거 ABSTRACT
- `VIRT-HPCA26-02` **eGPU: Production-Scale Elastic Sharing over 10,000 GPUs** — HPCA / T6 / P2 / 증거 ABSTRACT
- `VIRT-HPCA26-03` **SCALE: Tackling Communication Bottlenecks in Confidential Distributed Machine Learning** — HPCA / T7 / P1 / 증거 ABSTRACT
- `VIRT-HPCA26-05` **DSAssassin: Cross-VM Side-Channel Attacks by Exploiting Intel Data Streaming Accelerator** — HPCA / T7 / P1 / 증거 ABSTRACT
- `VIRT-HPDC26-01` **Enabling Floating Point Virtualization With Tiny Numbers** — HPDC / T1 / P1 / 증거 ABSTRACT
- `VIRT-OSDI26-01` **JANUS: Cross-World, Cooperative Nested Virtualization for Secure Containers** — OSDI / T1 / P0 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-02` **M3U: Scalable Kernel Memory Management for Efficient Post-copy Live Migration of High-end Virtual Machines** — OSDI / T4 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-03` **Compaction-Free Memory Defragmentation for Virtualization via Infinite Guest Physical Address Space** — OSDI / T2 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-04` **Inside Out: A Paradigm Shift In VM Introspection** — OSDI / T1 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-05` **Blowfish: Elastic Virtual Machine Memory for Disaggregated Memory** — OSDI / T2 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-06` **Nixie: Efficient, Transparent Temporal Multiplexing for Consumer GPUs** — OSDI / T6 / P0 / 증거 FULL
- `VIRT-OSDI26-07` **μShell: A Microkernel-based FPGA Shell Architecture** — OSDI / T6 / P1 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-08` **Virtualizing eBPF with Late-Binding** — OSDI / T5 / P2 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-09` **vBOIDs: Taming Chaos via Coarse-grained Scheduling Abstraction for Containers** — OSDI / T5 / P2 / 증거 DESIGN_EVAL
- `VIRT-OSDI26-12` **What Are You (M)Waiting For: The Hidden Cost of Idle in the Hyperscale Cloud** — OSDI / T1 / P1 / 증거 DESIGN

## 2026 배제(DROP) 기록 — 6건


### keyword_false_positive (3건)
- `VIRT-ASPLOS26-20` Toasty: Speeding Up Network I/O with Cache-Warm Buffers — ASPLOS
- `VIRT-ASPLOS26-21` Hitchhike: Efficient Request Submission via Deferred Enforcement of Address Contiguity — ASPLOS
- `VIRT-EUROSYS26-24` NutCracker: A Compilation Framework for Hybrid DPU Architectures — EuroSys

### no_virtualization_relation (2건)
- `VIRT-ASPLOS26-18` vCXLGen: Automated Synthesis and Verification of CXL Bridges for Heterogeneous Architectures — ASPLOS
- `VIRT-ASPLOS26-19` CXLMC: Model Checking CXL Shared Memory Programs — ASPLOS

### pure_virtual_memory (1건)
- `VIRT-HPCA26-04` ARIADNE: Adaptive UVM Management for Efficient GPU Memory Oversubscription — HPCA

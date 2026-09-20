# GPU_MASTER_INDEX

<!-- Routing index for domains/gpu_systems/corpus/. One row per deep analysis. -->

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-19

## What is indexed here

**85 deep analyses.** A deep analysis exists only where all of the following held: the paper is a
main/regular research paper in a reconstructed venue-year population; its full text was publicly reachable
**and was actually read** across the sections named in each file's `read_depth`; and the GPU-relevance
verdict survived the counterfactual test. Papers that passed the relevance test but failed the full-paper
gate are in [`GPU_PENDING_FULLTEXT.md`](../synthesis/GPU_PENDING_FULLTEXT.md), not here — their absence
from this index says nothing about their value.

Every candidate that was adjudicated, analysed or not, has a row in one of the eleven cluster ledgers
(`corpus/_LEDGER_*.md`). This index is a routing document; per
[`governance/ANTI_HALLUCINATION_RULES.md`](../../../governance/ANTI_HALLUCINATION_RULES.md) it is not the
evidentiary basis for any detailed claim — descend to the corpus file, and from there to the paper or code.

## Counts

| | |
|---|---|
| Deep analyses | 85 |
| of which `CORE_GPU` | 83 |
| of which `RELATED_GPU` (boundary cases, retained and labelled) | 2 |
| `fulltext_state` = `PUBLIC_FULLTEXT` | 85 (all) |
| `prior_corpus_check` = `NO_EXISTING_ANALYSIS` | 64 |
| `prior_corpus_check` = `GPU_DELTA_ANALYSIS` | 7 |
| `prior_corpus_check` = `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` | 14 |
| `EXISTING_CORPUS_DUPLICATE` | 0 |

## Stable IDs

`GPU-<VENUE><YY>-<NN>`. The `GPU-` prefix is the domain-prefixed scheme that
[`governance/ID_NAMING_RULES.md`](../../../governance/ID_NAMING_RULES.md) reserves for new sources; it keeps
these distinct from the `SC24-13`-style IDs of the pending AI/HPC import, which must not be renumbered.
`<NN>` is **not** a rank or a sequence position: the eleven adjudication clusters ran in parallel and were
given disjoint numeric bands so that no ID could be reused. The bands are an artefact of construction and
carry no meaning. IDs are stable and are never reused, even if a paper is later reclassified.

## Index by taxonomy

### A+B — GPU core, warp/SIMT execution, microarchitecture, on-chip interconnect  (8)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) | IPDPS | 2024 | Benchmarking and Dissecting the Nvidia Hopper GPU Architecture | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) | IPDPS | 2026 | Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md) | ISCA | 2024 | GhOST: A GPU Out-of-Order Scheduling Technique for Stall Reduction | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-61`](../corpus/GPU-MICRO24-61--cars-concurrency-aware-register-stacks-gpu-function-calls.md) | MICRO | 2024 | Concurrency-Aware Register Stacks for Efficient GPU Function Calls | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-62`](../corpus/GPU-MICRO24-62--threadfuser-simt-analysis-framework-mimd-programs.md) | MICRO | 2024 | ThreadFuser: A SIMT Analysis Framework for MIMD Programs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md) | MICRO | 2024 | Uncovering Real GPU NoC Characteristics: Implications on Interconnect Architecture | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-64`](../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md) | MICRO | 2024 | Unleashing CPU Potential for Executing GPU Programs through Compiler/Runtime Optimizations | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md) | MICRO | 2025 | Dissecting and Modeling the Architecture of Modern GPU Cores | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### C+D — caches, TLBs, address translation, UVM, oversubscription, multi-GPU memory  (8)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS24-01`](../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md) | ASPLOS | 2024 | GMLake: Efficient and Transparent GPU Memory Defragmentation for Large-scale DNN Training with  | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-HPCA24-01`](../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md) | HPCA | 2024 | GRIT: Enhancing Multi-GPU Performance with Fine-Grained Dynamic Page Placement | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md) | HPCA | 2026 | HDPAT: Hierarchical Distributed Page Address Translation for Wafer-Scale GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) | ICS | 2024 | Shared Virtual Memory: Its Design and Performance Implications for Diverse Applications | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) | ICS | 2025 | DREAM: Device-Driven Efficient Access to Virtual Memory | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) | ISC | 2024 | Porting HPC Applications to AMD Instinct MI300A Using Unified Memory and OpenMP | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-MICRO24-01`](../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md) | MICRO | 2024 | SUV: Static Analysis Guided Unified Virtual Memory | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md) | MICRO | 2024 | STAR: Sub-Entry Sharing-Aware TLB for Multi-Instance GPU | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### E — HBM and data movement, GPU compression, GPU-storage/host I/O  (7)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS25-81`](../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md) | ASPLOS | 2025 | Efficient Lossless Compression of Scientific Floating-Point Data on CPUs and GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md) | ICS | 2025 | Pushing the Limits of GPU Lossy Compression: A Hierarchical Delta Approach (**Aatrox**) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS26-81`](../corpus/GPU-ICS26-81--gpz-gpu-lossy-compressor-particle-data.md) | ICS | 2026 | GPZ: GPU-Accelerated Lossy Compressor for Particle Data | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISCA25-81`](../corpus/GPU-ISCA25-81--ecco-entropy-aware-cache-compression-hbm-bandwidth.md) | ISCA | 2025 | Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-SC24-81`](../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md) | SC | 2024 | cuSZ-*i*: High-Ratio Scientific Lossy Compression on GPUs with Optimized Multi-Level Interpolat | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-82`](../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md) | SC | 2024 | Hydrogen: Contention-Aware Hybrid Memory for Heterogeneous CPU-GPU Architectures | `RELATED_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md) | SC | 2025 | AGILE: Lightweight and Efficient Asynchronous GPU-SSD Integration | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### F — Tensor/Matrix cores, numeric formats, precision emulation  (9)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md) | ASPLOS | 2025 | Virgo: Cluster-level Matrix Unit Integration in GPUs for Scalability and Energy Efficiency | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md) | ISC | 2026 | Accelerating High-Order Finite Element Simulations at Extreme Scale with FP64 Tensor Cores | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md) | PPoPP | 2024 | ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md) | PPoPP | 2025 | FlashSparse: Minimizing Computation Redundancy for Fast Sparse Matrix Multiplications on Tensor | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md) | PPoPP | 2025 | Acc-SpMM: Accelerating General-purpose Sparse Matrix-Matrix Multiplication with GPU Tensor Core | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md) | PPoPP | 2026 | SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md) | PPoPP | 2026 | Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Compu | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md) | SC | 2026 | Double-Precision Matrix Multiplication Emulation via Ozaki-II Scheme with FP8 Quantization | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md) | SC | 2026 | EmuGEMM: Fused Tensor Core Kernels for Precision Emulation in Matrix Multiplication | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### G — sparse and irregular GPU kernels  (7)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS25-107`](../corpus/GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md) | ASPLOS | 2025 | Optimizing Datalog for the GPU (GPUlog) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md) | ASPLOS | 2026 | Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md) | ICS | 2026 | Ocean: Fast Estimation-Based Sparse General Matrix-Matrix Multiplication on GPU | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP26-104`](../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md) | PPoPP | 2026 | Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP26-105`](../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md) | PPoPP | 2026 | DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md) | SC | 2024 | High Performance Unstructured SpMM Computation Using Tensor Cores (SMaT) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-103`](../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md) | SC | 2024 | Mille-feuille: A Tile-Grained Mixed Precision Single-Kernel Conjugate Gradient Solver on GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### H+I — compilers, programming models, IR and lowering, kernel fusion, language-level safety  (7)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS24-142`](../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md) | ASPLOS | 2024 | Towards Unified Analysis of GPU Consistency | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ASPLOS26-141`](../corpus/GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md) | ASPLOS | 2026 | Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ASPLOS26-143`](../corpus/GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md) | ASPLOS | 2026 | CHERI-SIMT: Implementing Capability Memory Protection in GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-HPCA26-144`](../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md) | HPCA | 2026 | FlashFuser: Expanding the Scale of Kernel Fusion for Compute-Intensive Operators via Inter-Core | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS25-145`](../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md) | ICS | 2025 | Taking GPU Programming Models to Task for Performance Portability | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP24-146`](../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md) | PPoPP | 2024 | Gallatin: A General-Purpose GPU Memory Manager | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-147`](../corpus/GPU-SC24-147--ompdart-static-generation-openmp-offload-data-mappings.md) | SC | 2024 | Static Generation of Efficient OpenMP Offload Data Mappings (OMPDart) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### J+K — runtime, task graphs, scheduling, GPU sharing (MIG/MPS/virtualisation)  (6)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS26-163`](../corpus/GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md) | ASPLOS | 2026 | gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ASPLOS26-166`](../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md) | ASPLOS | 2026 | Bullet: Boosting GPU Utilization for LLM Serving via Dynamic Spatial-Temporal Orchestration | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-ICS25-162`](../corpus/GPU-ICS25-162--mustard-device-side-execution-multi-gpu-task-graphs.md) | ICS | 2025 | A Device-Side Execution Model for Multi-GPU Task Graphs (Mustard) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md) | ISC | 2026 | Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP25-164`](../corpus/GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md) | PPoPP | 2025 | SGDRC: Software-Defined Dynamic Resource Control for Concurrent DNN Inference on NVIDIA GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-161`](../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md) | SC | 2024 | ParvaGPU: Efficient Spatial GPU Sharing for Large-Scale DNN Inference in Cloud Environments | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### L+M — multi-GPU interconnect, GPU-aware/GPU-initiated communication, collectives  (9)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS24-21`](../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md) | ASPLOS | 2024 | T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) | ASPLOS | 2026 | MSCCL++: Rethinking GPU Communication Abstractions for AI Inference | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) | HPDC | 2026 | GICC: GPU-Initiated Communication and Coordination Runtime | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-IPDPS26-01`](../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md) | IPDPS | 2026 | From Skew to Symmetry: Node-Interconnect Multi-Path Balancing with Execution-time Planning for  | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md) | IPDPS | 2026 | The Big Send-off: Scalable and Performant Collectives for Deep Learning | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md) | ISC | 2026 | PICO: Performance Insights for Collective Operations | `RELATED_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md) | SC | 2024 | Exploring GPU-to-GPU Communication: Insights into Supercomputer Interconnects | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) | SC | 2026 | Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |
| [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md) | SC | 2026 | NCCLZ: Compression-Enabled GPU Collectives with Decoupled Quantization and Entropy Coding | `CORE_GPU` | `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` |

### N+O — profiling, debugging, simulation, performance modelling; reliability, telemetry, production performance  (9)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-HPCA24-41`](../corpus/GPU-HPCA24-41--gpu-scale-model-simulation.md) | HPCA | 2024 | GPU Scale-Model Simulation | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md) | ICS | 2024 | Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-IPDPS26-41`](../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md) | IPDPS | 2026 | Characterizing Production GPU Workloads using System-wide Telemetry Data | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md) | IPDPS | 2026 | The Case of the Elusive Application Performance on Production GPU Supercomputers | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-MICRO24-41`](../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md) | MICRO | 2024 | Over-Synchronization in GPU Programs (ScopeAdvice) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO25-01`](../corpus/GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md) | MICRO | 2025 | Swift and Trustworthy Large-Scale GPU Simulation with Fine-Grained Error Modeling and Hierarchi | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-41`](../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md) | SC | 2024 | HiRace: Accurate and Fast Data Race Checking for GPU Programs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md) | SC | 2025 | Story of Two GPUs: Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-SC26-41`](../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md) | SC | 2026 | LEO: Tracing GPU Stall Root Causes via Cross-Vendor Backward Slicing | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

### P — power, energy, DVFS, thermal, energy attribution  (7)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS24-186`](../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md) | ASPLOS | 2024 | Characterizing Power Management Opportunities for LLMs in the Cloud (POLCA) | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS26-183`](../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md) | ICS | 2026 | Wattchmen: Watching the Wattchers – High Fidelity, Flexible GPU Energy Modeling | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md) | ISC | 2026 | Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-ISCA26-187`](../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md) | ISCA | 2026 | Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO25-185`](../corpus/GPU-MICRO25-185--distributed-training-power-performance-thermal.md) | MICRO | 2025 | Characterizing the Efficiency of Distributed Training: A Power, Performance, and Thermal Perspe | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md) | SC | 2024 | Accurate and Convenient Energy Measurements for GPUs: A Detailed Study of NVIDIA GPU's Built-In | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |
| [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md) | SC | 2025 | Benchmark-driven Models for Energy Analysis and Attribution of GPU-Accelerated Supercomputing | `CORE_GPU` | `GPU_DELTA_ANALYSIS` |

### Q — fixed-function GPU units repurposed for general computation  (8)

| ID | Venue | Year | Paper | Verdict | Prior-corpus |
|---|---|---|---|---|---|
| [`GPU-ASPLOS25-124`](../corpus/GPU-ASPLOS25-124--treelet-accelerated-ray-tracing-gpus.md) | ASPLOS | 2025 | Treelet Accelerated Ray Tracing on GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-HPCA25-126`](../corpus/GPU-HPCA25-126--vr-pipe-streamlining-graphics-pipeline-volume-rendering.md) | HPCA | 2025 | VR-Pipe: Streamlining Hardware Graphics Pipeline for Volume Rendering | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ICS24-125`](../corpus/GPU-ICS24-125--arkade-knn-non-euclidean-gpu-ray-tracing.md) | ICS | 2024 | Arkade: k-Nearest Neighbor Search With Non-Euclidean Distances using GPU Ray Tracing | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-ISCA25-127`](../corpus/GPU-ISCA25-127--cooprt-bvh-traversal-cooperative-threads.md) | ISCA | 2025 | CoopRT: Accelerating BVH Traversal for Ray Tracing via Cooperative Threads | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md) | MICRO | 2024 | Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-122`](../corpus/GPU-MICRO24-122--tta-generalizing-ray-tracing-accelerators-tree-traversals.md) | MICRO | 2024 | Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-MICRO24-123`](../corpus/GPU-MICRO24-123--libra-memory-bandwidth-locality-aware-parallel-tile-rendering.md) | MICRO | 2024 | LIBRA: Memory Bandwidth- and Locality-Aware Parallel Tile Rendering | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |
| [`GPU-PPoPP25-128`](../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md) | PPoPP | 2025 | LibRTS: A Spatial Indexing Library by Ray Tracing | `CORE_GPU` | `NO_EXISTING_ANALYSIS` |

## Index by venue-year

| Venue-year | Deep analyses | IDs |
|---|---|---|
| ASPLOS 2024 | 4 | [`GPU-ASPLOS24-01`](../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md), [`GPU-ASPLOS24-21`](../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md), [`GPU-ASPLOS24-142`](../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md), [`GPU-ASPLOS24-186`](../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md) |
| ASPLOS 2025 | 4 | [`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md), [`GPU-ASPLOS25-81`](../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md), [`GPU-ASPLOS25-107`](../corpus/GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md), [`GPU-ASPLOS25-124`](../corpus/GPU-ASPLOS25-124--treelet-accelerated-ray-tracing-gpus.md) |
| ASPLOS 2026 | 6 | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md), [`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md), [`GPU-ASPLOS26-141`](../corpus/GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md), [`GPU-ASPLOS26-143`](../corpus/GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md), [`GPU-ASPLOS26-163`](../corpus/GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md), [`GPU-ASPLOS26-166`](../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md) |
| HPCA 2024 | 2 | [`GPU-HPCA24-01`](../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md), [`GPU-HPCA24-41`](../corpus/GPU-HPCA24-41--gpu-scale-model-simulation.md) |
| HPCA 2025 | 1 | [`GPU-HPCA25-126`](../corpus/GPU-HPCA25-126--vr-pipe-streamlining-graphics-pipeline-volume-rendering.md) |
| HPCA 2026 | 2 | [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md), [`GPU-HPCA26-144`](../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md) |
| HPDC 2026 | 1 | [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) |
| ICS 2024 | 3 | [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md), [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md), [`GPU-ICS24-125`](../corpus/GPU-ICS24-125--arkade-knn-non-euclidean-gpu-ray-tracing.md) |
| ICS 2025 | 4 | [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md), [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md), [`GPU-ICS25-145`](../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md), [`GPU-ICS25-162`](../corpus/GPU-ICS25-162--mustard-device-side-execution-multi-gpu-task-graphs.md) |
| ICS 2026 | 3 | [`GPU-ICS26-81`](../corpus/GPU-ICS26-81--gpz-gpu-lossy-compressor-particle-data.md), [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md), [`GPU-ICS26-183`](../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md) |
| IPDPS 2024 | 1 | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| IPDPS 2026 | 5 | [`GPU-IPDPS26-01`](../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md), [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md), [`GPU-IPDPS26-41`](../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md), [`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md), [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) |
| ISC 2024 | 1 | [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) |
| ISC 2026 | 4 | [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md), [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md), [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md), [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md) |
| ISCA 2024 | 1 | [`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md) |
| ISCA 2025 | 2 | [`GPU-ISCA25-81`](../corpus/GPU-ISCA25-81--ecco-entropy-aware-cache-compression-hbm-bandwidth.md), [`GPU-ISCA25-127`](../corpus/GPU-ISCA25-127--cooprt-bvh-traversal-cooperative-threads.md) |
| ISCA 2026 | 1 | [`GPU-ISCA26-187`](../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md) |
| MICRO 2024 | 10 | [`GPU-MICRO24-01`](../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md), [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md), [`GPU-MICRO24-41`](../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md), [`GPU-MICRO24-61`](../corpus/GPU-MICRO24-61--cars-concurrency-aware-register-stacks-gpu-function-calls.md), [`GPU-MICRO24-62`](../corpus/GPU-MICRO24-62--threadfuser-simt-analysis-framework-mimd-programs.md), [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md), [`GPU-MICRO24-64`](../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md), [`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md), [`GPU-MICRO24-122`](../corpus/GPU-MICRO24-122--tta-generalizing-ray-tracing-accelerators-tree-traversals.md), [`GPU-MICRO24-123`](../corpus/GPU-MICRO24-123--libra-memory-bandwidth-locality-aware-parallel-tile-rendering.md) |
| MICRO 2025 | 3 | [`GPU-MICRO25-01`](../corpus/GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md), [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md), [`GPU-MICRO25-185`](../corpus/GPU-MICRO25-185--distributed-training-power-performance-thermal.md) |
| PPoPP 2024 | 2 | [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md), [`GPU-PPoPP24-146`](../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md) |
| PPoPP 2025 | 4 | [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md), [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md), [`GPU-PPoPP25-128`](../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md), [`GPU-PPoPP25-164`](../corpus/GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md) |
| PPoPP 2026 | 4 | [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md), [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md), [`GPU-PPoPP26-104`](../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md), [`GPU-PPoPP26-105`](../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md) |
| SC 2024 | 9 | [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md), [`GPU-SC24-41`](../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md), [`GPU-SC24-81`](../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md), [`GPU-SC24-82`](../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md), [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md), [`GPU-SC24-103`](../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md), [`GPU-SC24-147`](../corpus/GPU-SC24-147--ompdart-static-generation-openmp-offload-data-mappings.md), [`GPU-SC24-161`](../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md), [`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md) |
| SC 2025 | 3 | [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md), [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md), [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md) |
| SC 2026 | 5 | [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md), [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md), [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md), [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md), [`GPU-SC26-41`](../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md) |

## Where to go next

- Venue-year populations and the broad candidate screen: [`../census/`](../census/)
- Every adjudicated candidate, analysed or not: `../corpus/_LEDGER_*.md`
- Topic routing: [`../TOPIC_MAP.md`](../TOPIC_MAP.md) → [`../topics/`](../topics/)
- Lineages: [`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) and the four area lineage documents
- Watchlist: [`GPU_PENDING_FULLTEXT.md`](GPU_PENDING_FULLTEXT.md)
- Overlap with other domains: [`GPU_EXISTING_CORPUS_OVERLAP.md`](GPU_EXISTING_CORPUS_OVERLAP.md)
- How this corpus was built and what it does not claim: [`METHODOLOGY_NOTES.md`](METHODOLOGY_NOTES.md)

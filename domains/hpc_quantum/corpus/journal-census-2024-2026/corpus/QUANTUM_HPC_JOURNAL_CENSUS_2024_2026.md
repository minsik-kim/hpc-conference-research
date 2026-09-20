# QUANTUM_HPC_JOURNAL_CENSUS_2024_2026

**Master census of HPC x Quantum-Computing interface research in eight core journals, 2024-2026.**

Compiled 2026-09-17 (KST). Scope: the eight journals named in the commissioning brief only. 
This is **not** a quantum-computing literature review. Inclusion requires a quantum problem 
**plus** a substantive classical computing / systems / HPC implication (the Three-Gate Test, `governance` note 
and full criteria reproduced in `CENSUS_METHOD.md`).

---

## 0. How to read this document

- **DOI is the primary key.** Every record is identified by DOI; no paper is counted twice.
- **Census year = year of first public availability** where a first-availability date exists 
  (Elsevier online-first, ACM published-online, IEEE Early Access when recorded); otherwise the 
  volume/issue cover year, recorded as `YEAR_BASIS=ISSUE`. Final volume/issue/pages are recorded 
  separately for every paper. **IEEE TQE runs entirely on `YEAR_BASIS=ISSUE`** (v5=2024, v6=2025, 
  v7=2026) because Early Access dates were not obtainable for it; this is a stated limitation, not a choice.
- Only `ORIGINAL_RESEARCH` counts toward the included population. Reviews, surveys, perspectives 
  and special-issue introductions are listed separately and may carry `BIBLIOGRAPHY_HUB`.
- `BORDERLINE` records are **kept, not discarded**, with the argument for and against recorded.
- Per-journal detail, full false-positive logs and the complete per-record analysis live in 
  `CENSUS_FGCS_2024_2026.md`, `CENSUS_TQE_2024_2026.md`, `CENSUS_TQC_TACO_2024_2026.md` and 
  `CENSUS_TC_TCAD_TPDS_JPDC_2024_2026.md`. Corrections made after the first draft are in 
  `VERIFICATION_CHANGELOG.md`.
- Gap vocabulary is restricted to `VENUE_GAP`, `JOURNAL_GAP`, `UNDERREPRESENTED_IN_THIS_CORPUS`, 
  `POSSIBLE_CROSSOVER`, `OPEN_QUESTION`, `INSUFFICIENT_EVIDENCE`. No novelty claim is made anywhere.

---

## 1. Headline result

| Journal | ISSN | Population swept 2024-2026 | Candidates | INCLUDED | of which ORIGINAL_RESEARCH | BORDERLINE | EXCLUDED | Unresolved | Precision of candidate pool |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **FGCS** | 0167-739X | 1567 | 85 | 22 | **20** | 8 | 54 | 0 | 26% |
| **TQE** | 2689-1808 | 254 | 246 | 25 | **25** | 37 | 183 | 0 | 10% |
| **TQC** | 2643-6809 | 97 | 97 | 22 | **20** | 17 | 58 | 0 | 23% |
| **TCAD** | 0278-0070 | 1562 | 68 | 12 | **12** | 12 | 41 | 3 | 18% |
| **TC** | 0018-9340 | 849 | 41 | 6 | **6** | 6 | 28 | 0 | 15% |
| **TACO** | 1544-3566 | 412 | 9 | 4 | **4** | 0 | 5 | 0 | 44% |
| **TPDS** | 1045-9219 | 552 | 10 | 2 | **2** | 0 | 8 | 0 | 20% |
| **JPDC** | 0743-7315 | 388 | 7 | 1 | **0** | 0 | 6 | 0 | 14% |
| **TOTAL** | | **5681** | **563** | **94** | **89** | **80** | **383** | **3** | **17%** |

Three records were placed `OUT_OF_WINDOW` after the verification pass (first public availability 
before 2024-01-01 despite a 2024 issue cover date): FGCS-001 `10.1016/j.future.2023.12.002`, 
TQE-007 `10.1109/tqe.2023.3347106`, TC-001 `10.1109/tc.2021.3066614`. They are retained in the 
per-journal files for audit and excluded from every count above.

### 1.1 Included original research by year

| Journal | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|
| FGCS | 5 | 8 | 7 | **20** |
| TQE | 7 | 12 | 6 | **25** |
| TQC | 7 | 4 | 9 | **20** |
| TCAD | 5 | 6 | 1 | **12** |
| TC | 2 | 2 | 2 | **6** |
| TACO | 1 | 2 | 1 | **4** |
| TPDS | 0 | 0 | 2 | **2** |
| JPDC | 0 | 0 | 0 | **0** |
| **TOTAL** | **27** | **34** | **28** | **89** |

The 2026 figure is a partial year (publications public as of 2026-09-17).

### 1.2 Journals ranked by included original research

1. **TQE** — 25
2. **FGCS** — 20
3. **TQC** — 20
4. **TCAD** — 12
5. **TC** — 6
6. **TACO** — 4
7. **TPDS** — 2
8. **JPDC** — 0

---

## 2. Bottom-up branch taxonomy

Derived from the 89 included original-research papers, not imposed on them. Branches are 
multi-label; the column totals therefore exceed the paper counts.

| Branch | FGCS | TQE | TQC | TCAD | TC | TACO | TPDS | JPDC | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `compiler_mapping_routing` | 7 | 9 | 8 | 7 | 3 | 4 | 0 | 0 | **38** |
| `distributed_gpu_simulation` | 4 | 3 | 7 | 3 | 3 | 0 | 2 | 0 | **22** |
| `benchmarking_performance_modeling` | 5 | 6 | 6 | 1 | 1 | 0 | 1 | 0 | **20** |
| `architecture_control` | 3 | 8 | 3 | 3 | 0 | 0 | 0 | 0 | **17** |
| `quantum_runtime_orchestration` | 6 | 2 | 3 | 2 | 0 | 1 | 0 | 0 | **14** |
| `qpu_scheduling_resource_mgmt` | 6 | 2 | 2 | 1 | 0 | 3 | 0 | 0 | **14** |
| `multi_qpu_distributed_qc` | 2 | 4 | 3 | 2 | 1 | 1 | 0 | 0 | **13** |
| `hpc_qpu_integration` | 5 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | **8** |
| `qec_classical_processing` | 0 | 4 | 3 | 0 | 0 | 1 | 0 | 0 | **8** |
| `hybrid_workflow` | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | **7** |
| `circuit_cutting_reconstruction` | 1 | 3 | 0 | 0 | 0 | 1 | 0 | 0 | **5** |
| `scientific_workflow_application` | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **3** |

### 2.1 Scenario distribution (multi-label, included original research)

| Scenario | Count | Share of 89 papers |
|---|---:|---:|
| `HPC_FOR_Q` | 84 | 94% |
| `Q_IN_HPC` | 23 | 26% |
| `FUTURE_WORKLOAD` | 27 | 30% |
| `Q_FOR_HPC` | 3 | 3% |

---

## 3. Per-paper master census — INCLUDED original research

Ordered by journal, then census year, then DOI.

### FGCS — Future Generation Computer Systems (20 papers)

#### `FGCS-002` QFaaS: A Serverless Function-as-a-Service framework for Quantum computing

- **Bibliographic** — Hoa T. Nguyen et al. · Future Generation Computer Systems 0167-739X · census year **2024** · vol 154 , issue date 2024-05 · pp 281-300
- **DOI** — `10.1016/j.future.2024.01.018` · <https://doi.org/10.1016/j.future.2024.01.018>
- **arXiv** — `2205.14845`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC` · **Branch** — `quantum_runtime_orchestration`, `hybrid_workflow`
- **Gate 1 (classical systems problem)** — Runtime, orchestration and resource management for hybrid quantum-classical functions across heterogeneous backends; containerisation and deployment cost.
- **Gate 2 (HPC/systems technique)** — A serverless middleware/runtime layer (function lifecycle, containerisation, backend selection, DevOps integration) is the core contribution.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Defines a concrete software-stack pattern for delivering QPU access as a managed service alongside classical compute.
- **Quantum problem** — Fragmentation of quantum programming languages (Qiskit, Q#, Cirq, Braket) and provider backends.
- **Classical / HPC problem** — Orchestration, containerisation and lifecycle management of short-lived hybrid functions across multiple execution backends.
- **Mechanism** — Layered serverless architecture: API gateway, function lifecycle manager, containerised hybrid quantum-classical functions, backend-agnostic dispatch to simulators and cloud QPUs.
- **Computational bottleneck** — Backend selection/queueing and classical-quantum round-trip latency in hybrid functions.
- **Evaluation platform / scale** — IBM Quantum and Amazon Braket cloud QPUs plus simulators; containerised deployment. / Two use cases; device sizes INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['end-to-end function execution time', 'deployment/operation workflow feasibility']
- **Major claim (with baseline)** — A unified serverless layer can execute hybrid functions across four SDKs and two providers; BASELINE_UNCLEAR (no quantitative baseline framework comparison stated).
- **Limitation** — Targets cloud QPU providers rather than an on-premise HPC batch system; no HPC scheduler integration reported.
- **Artifact** — PUBLIC_CODE · https://github.com/Cloudslab/qfaas
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-007` Paving the way to hybrid quantum–classical scientific workflows

- **Bibliographic** — Sandeep Suresh Cranganore et al. · Future Generation Computer Systems 0167-739X · census year **2024** · vol 158 , issue date 2024-09 · pp 346-366
- **DOI** — `10.1016/j.future.2024.04.030` · <https://doi.org/10.1016/j.future.2024.04.030>
- **arXiv** — `2404.10389`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q` · **Branch** — `hybrid_workflow`, `scientific_workflow_application`
- **Gate 1 (classical systems problem)** — Mapping workflow components onto heterogeneous resources, and workflow management across the computing continuum - resource allocation and orchestration.
- **Gate 2 (HPC/systems technique)** — Formalisation of hybrid quantum-classical workflows plus a software architecture for a hybrid workflow management system.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Defines how quantum tasks are identified, split out and scheduled next to classical tasks in a scientific workflow engine.
- **Quantum problem** — Identifying which parts of a scientific application are amenable to quantum execution.
- **Classical / HPC problem** — Workflow formalisation, component-to-resource mapping and workflow management across a heterogeneous continuum.
- **Mechanism** — Formal model of hybrid quantum-classical workflows; procedure to identify quantum components and map them to resources; reference software architecture for a hybrid WMS.
- **Computational bottleneck** — Resource mapping and data movement between classical workflow stages and quantum tasks.
- **Evaluation platform / scale** — A real scientific use case (demonstration); concrete machine INSUFFICIENT_EVIDENCE. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — ['qualitative workflow feasibility']
- **Major claim (with baseline)** — Hybrid quantum-classical scientific workflows can be formalised and managed by an extended WMS architecture; BASELINE_UNCLEAR (no quantitative baseline).
- **Limitation** — Architecture-level contribution; no production WMS implementation or performance measurement reported in the abstract.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-014` Performance of algorithms for emerging ion-trap quantum hardware

- **Bibliographic** — Arthur Kurlej et al. · Future Generation Computer Systems 0167-739X · census year **2024** · vol 160 , issue date 2024-11 · pp 654-665
- **DOI** — `10.1016/j.future.2024.06.005` · <https://doi.org/10.1016/j.future.2024.06.005>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `benchmarking_performance_modeling`, `architecture_control`
- **Gate 1 (classical systems problem)** — Runtime and overhead of benchmark applications across architecture variants, and the compilation step that produces them.
- **Gate 2 (HPC/systems technique)** — Architectural simulation plus compilation to target devices used as a quantitative architecture-evaluation methodology - quantum performance modeling.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs how QPU architectural choices change execution time and overhead, i.e. performance and architecture of the accelerator side.
- **Quantum problem** — Performance of benchmark quantum algorithms (including adaptive variational algorithms for chemistry) on ion-trap hardware.
- **Classical / HPC problem** — Architectural simulation and compilation infrastructure needed to estimate runtime/overhead before hardware exists.
- **Mechanism** — Pipeline of benchmark application selection, compilation to candidate ion-trap targets, and architectural simulation to extract runtime and overhead.
- **Computational bottleneck** — Shuttling/connectivity overheads in trapped-ion architectures as exposed by compiled circuits.
- **Evaluation platform / scale** — Architectural simulator for ion-trap devices (simulated, not physical hardware). / INSUFFICIENT_EVIDENCE (qubit counts not stated in retrieved material)
- **Performance metrics** — ['runtime', 'architectural overhead']
- **Major claim (with baseline)** — A benchmark-plus-architectural-simulation methodology can quantitatively separate ion-trap design options; BASELINE_UNCLEAR.
- **Limitation** — Simulation-based architectural estimates; no physical ion-trap measurements reported.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `FGCS-015` Parallel quantum computing simulations via quantum accelerator platform virtualization

- **Bibliographic** — Daniel Claudino et al. · Future Generation Computer Systems 0167-739X · census year **2024** · vol 160 , issue date 2024-11 · pp 264-273
- **DOI** — `10.1016/j.future.2024.06.007` · <https://doi.org/10.1016/j.future.2024.06.007>
- **arXiv** — `2406.03466`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`, `hpc_qpu_integration`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Parallelism and strong scaling across HPC nodes; throughput of large batches of independent circuit executions.
- **Gate 2 (HPC/systems technique)** — Virtualisation of QPUs: an array of virtual QPUs mapped onto classical HPC nodes inside XACC, with GPU-accelerated backends via cuQuantum.
- **Gate 3 (future CPU/GPU/QPU relevance)** — A direct model for how many logical QPU endpoints an HPC system can present, and how shot/circuit batches are distributed.
- **Quantum problem** — Workflows requiring many independent measurements over large sets of slightly different circuits (VQE gradients, circuit learning).
- **Classical / HPC problem** — Distributing an embarrassingly parallel but large circuit-execution workload across HPC nodes and GPUs.
- **Mechanism** — Virtual quantum processing unit array mapped one-to-one onto classical HPC nodes, implemented inside XACC so it is backend-agnostic; GPU simulation through cuQuantum.
- **Computational bottleneck** — Serialised circuit execution and per-circuit simulation cost; memory per node for state-vector simulation.
- **Evaluation platform / scale** — GPU-accelerated HPC platform using the cuQuantum SDK via XACC (specific machine INSUFFICIENT_EVIDENCE). / Strong-scaling study varying qubit count and circuit layer count; node counts INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['strong scaling efficiency', 'time to compute multi-contracted VQE gradients']
- **Major claim (with baseline)** — Strong scaling is demonstrated on two domain-science problems (multi-contracted VQE gradients and data-driven circuit learning); BASELINE_UNCLEAR (speedup ratios not stated in retrieved text).
- **Limitation** — Virtual QPUs are simulators, so results characterise simulation throughput rather than physical QPU sharing.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-018` Integrating quantum computing resources into scientific HPC ecosystems

- **Bibliographic** — Thomas Beck et al. · Future Generation Computer Systems 0167-739X · census year **2024** · vol 161 , issue date 2024-12 · pp 11-25
- **DOI** — `10.1016/j.future.2024.06.058` · <https://doi.org/10.1016/j.future.2024.06.058>
- **arXiv** — `2408.16159`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `hpc_qpu_integration`, `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Resource management, allocation and lifecycle of a QC resource inside an HPC centre; integration of accelerators into existing batch/allocation processes.
- **Gate 2 (HPC/systems technique)** — A hardware-agnostic integration framework that treats the QPU as an HPC accelerator, spanning simulators and physical devices and the centre's lifecycle management.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Explicitly about how a supercomputing facility procures, allocates and operates quantum resources alongside classical ones.
- **Quantum problem** — NISQ noise and device heterogeneity make direct QPU exposure to users impractical.
- **Classical / HPC problem** — Centre-level resource integration: allocation, lifecycle management, user access and the software stack around a non-classical accelerator.
- **Mechanism** — Hardware-agnostic framework layering simulators and physical QPU backends behind an HPC-facing interface, aligned with DOE/ORNL HPC lifecycle management practice.
- **Computational bottleneck** — Integration friction between quantum backends and HPC allocation/scheduling processes.
- **Evaluation platform / scale** — ORNL HPC environment with a spectrum of simulators and hardware technologies. / Centre-scale; concrete node/QPU counts INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['qualitative integration feasibility']
- **Major claim (with baseline)** — A single hardware-agnostic layer can serve both current NISQ devices and future fault-tolerant machines inside an HPC centre; BASELINE_UNCLEAR.
- **Limitation** — Framework and process description; limited quantitative performance evaluation.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-033` MLQM: Machine learning approach for accelerating optimal qubit mapping

- **Bibliographic** — Wenjie Sun et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 173 , issue date 2025-12 · pp 107906
- **DOI** — `10.1016/j.future.2025.107906` · <https://doi.org/10.1016/j.future.2025.107906>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Compilation cost: solving time and memory (search-space size) of exact qubit mapping are the quantities optimised.
- **Gate 2 (HPC/systems technique)** — Classical compilation scalability - search-space pruning and adaptive solver-variable adjustment to make an exact mapping solver tractable.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Compiler throughput and memory are hard constraints on any HPC-hosted quantum software stack.
- **Quantum problem** — Mapping logical circuits onto constrained hardware connectivity without losing solution quality.
- **Classical / HPC problem** — Solving time and memory footprint of the exact (solver-based) mapping formulation.
- **Mechanism** — Global search-space pruning with an ML model plus prior knowledge; data augmentation by gate allocation and qubit rearrangement; local pruning by adaptive dynamic solver-variable adjustment.
- **Computational bottleneck** — Combinatorial blow-up of the exact mapping solver's search space.
- **Evaluation platform / scale** — Classical solver benchmarks (machine specification INSUFFICIENT_EVIDENCE). / Benchmark circuit suite; sizes INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['mapping solving time', 'space complexity', 'solution quality']
- **Major claim (with baseline)** — Average 1.79x solving speedup with 22% space-complexity reduction while maintaining solution quality, measured against state-of-the-art exact mapping approaches (baseline named only as 'state-of-the-art' - partially BASELINE_UNCLEAR).
- **Limitation** — Gains depend on the learned model transferring to unseen circuit/topology combinations; training cost not reported.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `FGCS-036` State of practice: Evaluating GPU performance of state vector and tensor network methods

- **Bibliographic** — Marzio Vallero et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 174 , issue date 2026-01 · pp 107927
- **DOI** — `10.1016/j.future.2025.107927` · <https://doi.org/10.1016/j.future.2025.107927>
- **arXiv** — `2401.06188`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Memory footprint and execution time of quantum circuit simulation, and the scalability limit of top HPC machines for state-vector simulation.
- **Gate 2 (HPC/systems technique)** — Systematic GPU-accelerated simulation benchmarking across state-vector and tensor-network backends (cuStateVec, cupy, cuTensorNet under cuQuantum/qsim).
- **Gate 3 (future CPU/GPU/QPU relevance)** — Establishes where the classical simulation frontier sits, which determines what an HPC system can still verify or replace on the QPU side.
- **Quantum problem** — Simulating large quantum systems classically while NISQ devices remain non-fault-tolerant.
- **Classical / HPC problem** — Exponential memory growth of state-vector simulation and contraction cost of tensor networks on GPU hardware.
- **Mechanism** — Controlled benchmark of three GPU backends (qsim-cusv, qsim-cuda, cutn) across circuit families, measuring time and memory as qubit count and depth scale.
- **Computational bottleneck** — GPU memory capacity for state vectors; contraction cost/ordering for tensor networks.
- **Evaluation platform / scale** — AMD EPYC 7643 48-core CPU, 128 GB RAM, NVIDIA A100 80 GB GPU; NVIDIA cuQuantum with qsim. / Single-node GPU study; qubit counts scaled to the memory limit of an 80 GB A100.
- **Performance metrics** — ['execution time', 'memory footprint', 'scaling with qubit count and depth']
- **Major claim (with baseline)** — Each simulation family saturates for different reasons - state vector on memory, tensor network on contraction structure - so the practical frontier is circuit-dependent; comparison is between the three GPU backends (baseline is stated).
- **Limitation** — Single-node A100 study; multi-node/distributed simulation is not covered.
- **Artifact** — PARTIAL
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-039` MPGP-QOC: Multi-programming and graph-partition-based QOC for QNN inference

- **Bibliographic** — Yiding Liu et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 174 , issue date 2026-01 · pp 107966
- **DOI** — `10.1016/j.future.2025.107966` · <https://doi.org/10.1016/j.future.2025.107966>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Throughput (inference speedup), compilation time, and device occupancy via multi-programming - several devices' worth of work packed onto one QPU.
- **Gate 2 (HPC/systems technique)** — Multi-programming (concurrent circuits on one device, i.e. QPU sharing) combined with graph partitioning and quantum optimal control - a scheduling/compilation systems technique.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly about how a shared QPU is packed and how much classical compilation that costs.
- **Quantum problem** — Slow, pulse-level-inefficient QNN inference on NISQ devices.
- **Classical / HPC problem** — Compilation time of optimal-control pulse synthesis and under-utilisation of a single QPU by one small circuit.
- **Mechanism** — Partition the parameterised circuit graph, apply quantum optimal control per partition, and pack multiple programs concurrently onto the device.
- **Computational bottleneck** — Quantum optimal control compilation cost, which scales badly with circuit size - addressed by partitioning.
- **Evaluation platform / scale** — Existing quantum software/hardware platforms (specific device INSUFFICIENT_EVIDENCE). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — ['inference speedup', 'compilation time reduction', 'inference accuracy']
- **Major claim (with baseline)** — 10.1x average (up to 10.4x) speedup over state-of-the-art QNN inference with up to 6.5x compilation-time reduction and comparable accuracy; the baseline is named only as 'state-of-the-art QNN inference' - partially BASELINE_UNCLEAR.
- **Limitation** — Crosstalk and fidelity consequences of multi-programming are a known risk; accuracy is reported as comparable rather than improved across the board.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-041` Tightly-integrated quantum–classical computing using the QHDL hardware description language

- **Bibliographic** — Gilbert Netzer et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 174 , issue date 2026-01 · pp 107977
- **DOI** — `10.1016/j.future.2025.107977` · <https://doi.org/10.1016/j.future.2025.107977>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `architecture_control`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Latency and timing of classical feedback inside the control loop; compilation and co-simulation cost; modular description of circuits.
- **Gate 2 (HPC/systems technique)** — A hardware description language plus compiler, debugger and co-simulation infrastructure, with classical modules realised at RTL/gate level inside the control system.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Defines the tightly-coupled control-plane layer of the quantum-classical software stack - where classical computation must meet real-time deadlines.
- **Quantum problem** — Measurement-in-the-middle and dynamic circuits require classical computation inside the coherence window.
- **Classical / HPC problem** — Timing-critical classical computation embedded in the control system; modular description and co-simulation of mixed quantum-classical designs.
- **Mechanism** — QHDL language with modular circuit description, a compiler, a debugger and co-simulation; synchronous interfaces to RTL/gate-level classical blocks for precise timing.
- **Computational bottleneck** — Classical feedback latency between measurement and conditional quantum operation.
- **Evaluation platform / scale** — Four use cases: Bell pair circuits, dynamic delay, Quantum Fourier Transform, teleportation; co-simulation infrastructure. / Small demonstration circuits.
- **Performance metrics** — ['timing/coupling behaviour of classical modules', 'expressiveness of the modular description']
- **Major claim (with baseline)** — RTL/gate-level classical modules give coupling performance suitable for current control systems; BASELINE_UNCLEAR (no quantitative baseline language or stack reported).
- **Limitation** — Demonstrated on small circuits; no deployment onto a physical control stack is reported in the retrieved material.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-043` Bridging paradigms: Designing for HPC-Quantum convergence

- **Bibliographic** — Amir Shehata et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 174 , issue date 2026-01 · pp 107980
- **DOI** — `10.1016/j.future.2025.107980` · <https://doi.org/10.1016/j.future.2025.107980>
- **arXiv** — `2503.01787`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `hpc_qpu_integration`, `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Resource management, job scheduling and data movement between classical and quantum resources are named explicitly as the challenges addressed.
- **Gate 2 (HPC/systems technique)** — A full software-stack architecture: quantum gateway interface, standardised resource-management APIs, scheduling mechanisms, Quantum Platform Manager API.
- **Gate 3 (future CPU/GPU/QPU relevance)** — This is the software-stack and scheduling blueprint for a heterogeneous CPU/GPU/QPU facility.
- **Quantum problem** — Heterogeneous, fast-changing QPU backends spanning NISQ and future fault-tolerant devices.
- **Classical / HPC problem** — Resource management, job scheduling and classical-quantum data movement inside an established HPC environment.
- **Mechanism** — Layered, hardware-agnostic stack: quantum gateway interface, Quantum Platform Manager API, standardised resource-management APIs, and scheduling support that preserves existing HPC workflow compatibility.
- **Computational bottleneck** — Scheduling a scarce QPU against classical allocations, and moving data across the classical-quantum boundary.
- **Evaluation platform / scale** — ORNL HPC environment (architecture-level; quantitative evaluation INSUFFICIENT_EVIDENCE). / Centre-scale architecture.
- **Performance metrics** — ['qualitative architectural coverage']
- **Major claim (with baseline)** — A single hardware-agnostic stack can serve both NISQ and fault-tolerant devices while keeping existing HPC workflows working; BASELINE_UNCLEAR (architecture paper, no measured baseline).
- **Limitation** — Design-level contribution; the retrieved text reports no quantitative scheduling or throughput evaluation.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-045` NetQIR: An extension of QIR for distributed quantum computing

- **Bibliographic** — F. Javier Cardama et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 174 , issue date 2026-01 · pp 107989
- **DOI** — `10.1016/j.future.2025.107989` · <https://doi.org/10.1016/j.future.2025.107989>
- **arXiv** — `2408.03712`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Inter-QPU communication, distributed execution and the network/hardware abstraction layer are the explicit subject.
- **Gate 2 (HPC/systems technique)** — An intermediate representation extension with hardware-independent network communication instructions for compilers targeting distributed QPUs.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Defines the compiler/IR layer through which multi-QPU execution would be expressed in a software stack.
- **Quantum problem** — Per-chip qubit limits push toward networking multiple QPUs to run one algorithm.
- **Classical / HPC problem** — Absence of network- and hardware-layer abstraction in existing IRs, forcing hardware-specific distributed code.
- **Mechanism** — NetQIR extends Microsoft's QIR with hardware-independent instruction specifications for inter-QPU communication, in the spirit of a message-passing abstraction.
- **Computational bottleneck** — Inter-QPU communication (entanglement distribution and classical coordination) expressed at compile time.
- **Evaluation platform / scale** — Specification/compiler-infrastructure work; execution evaluation INSUFFICIENT_EVIDENCE. / Specification level.
- **Performance metrics** — ['abstraction coverage of distributed communication primitives']
- **Major claim (with baseline)** — Distributed quantum programs can be expressed at IR level with hardware-independent communication instructions; BASELINE_UNCLEAR (no performance baseline).
- **Limitation** — Specification without reported end-to-end distributed execution measurements.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-055` LuGo: An enhanced quantum phase estimation implementation

- **Bibliographic** — Chao Lu et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 178 , issue date 2026-05 · pp 108270
- **DOI** — `10.1016/j.future.2025.108270` · <https://doi.org/10.1016/j.future.2025.108270>
- **arXiv** — `2503.15439`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_FOR_HPC` · **Branch** — `compiler_mapping_routing`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Classical circuit-generation time is the headline cost reduced, plus gate count and depth; parallelisation is the mechanism.
- **Gate 2 (HPC/systems technique)** — A parallelised circuit-construction framework that removes duplicated sub-circuits - classical compilation/generation scalability.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Circuit generation is a real classical cost in the quantum software stack, particularly for HHL-style workloads driven from a classical application.
- **Quantum problem** — QPE circuit width/depth growth for realistic system matrices, and the fidelity cost that follows.
- **Classical / HPC problem** — Classical time to generate large QPE circuits, which becomes the dominant bottleneck before any execution happens.
- **Mechanism** — LuGo framework: detects and removes duplicated circuit structure and parallelises circuit generation.
- **Computational bottleneck** — Classical circuit-generation time for large unitary decompositions.
- **Evaluation platform / scale** — Ideal quantum simulators; applied to HHL and a Hele-Shaw fluid-flow simulation. / A 2^6 x 2^6 system matrix.
- **Performance metrics** — ['circuit generation time', 'gate count', 'circuit depth', 'fidelity']
- **Major claim (with baseline)** — 50.68x reduction in circuit generation time and over 31x reduction in gates and depth for a 2^6 x 2^6 system matrix, with no fidelity loss on ideal simulators; baseline is the standard (non-LuGo) QPE implementation.
- **Limitation** — Fidelity claim is on ideal simulators, so noise behaviour on hardware is not established.
- **Artifact** — PARTIAL
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `FGCS-057` Efficient and scalable branch-and-bound algorithm for exact qubit allocation

- **Bibliographic** — Jean-Philippe Valois et al. · Future Generation Computer Systems 0167-739X · census year **2025** · vol 179 , issue date 2026-06 · pp 108342
- **DOI** — `10.1016/j.future.2025.108342` · <https://doi.org/10.1016/j.future.2025.108342>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Intra-node and inter-node parallelism, strong scaling on HPC infrastructure, and the runtime of an exact compilation step.
- **Gate 2 (HPC/systems technique)** — A performance-aware parallel and distributed branch-and-bound implementation exploiting 128 cores per node and 64 nodes - core HPC methodology applied to a quantum compilation problem.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly shows how much HPC capacity is needed to push exact quantum compilation to larger circuits.
- **Quantum problem** — Adapting abstract circuits to NISQ connectivity constraints optimally rather than heuristically.
- **Classical / HPC problem** — Severe scalability limits of exact qubit-allocation solvers; parallel search with load balancing across nodes.
- **Mechanism** — Reformulate qubit allocation as a permutation-based quadratic assignment problem; refined sequential branch-and-bound, then a parallel distributed implementation with intra-node and inter-node work distribution (Chapel/PGAS skeletons from the P3D-DFS project).
- **Computational bottleneck** — Exponential search tree of the exact formulation; load imbalance across distributed workers.
- **Evaluation platform / scale** — HPC cluster: up to 128 cores per node intra-node, and 64 nodes / 8192 cores inter-node. / Benchmark circuits up to 26 qubits, versus prior exact limits reported around 16 qubits.
- **Performance metrics** — ['sequential runtime vs prior exact approaches', 'intra-node parallel efficiency', 'inter-node speedup', 'largest circuit solved exactly']
- **Major claim (with baseline)** — The sequential version beats previous exact approaches on 20 of 21 benchmarks; the parallel version reaches over 87% of linear speedup on 128 cores and 74% of ideal speedup on 64 nodes (8192 cores), yielding exact solutions up to 26 qubits - baselines are prior exact qubit-allocation approaches and ideal linear speedup.
- **Limitation** — Exact solving remains exponential; 26 qubits is far below device sizes, so the result bounds the exact approach rather than replacing heuristics.
- **Artifact** — PUBLIC_CODE · https://github.com/Guillaume-Helbecque/P3D-DFS
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-064` HiMA: Hierarchical quantum microarchitecture for qubit-scaling and quantum process-level parallelism

- **Bibliographic** — Qi Zhou et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 182 , issue date 2026-09 · pp 108484
- **DOI** — `10.1016/j.future.2026.108484` · <https://doi.org/10.1016/j.future.2026.108484>
- **arXiv** — `2408.11311`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `architecture_control`, `qpu_scheduling_resource_mgmt`
- **Gate 1 (classical systems problem)** — Process-level parallelism, throughput (CLOPS), control-system scalability to thousands of qubits, and multi-user concurrency.
- **Gate 2 (HPC/systems technique)** — A control microarchitecture: discrete qubit-level operations, hierarchical trigger mechanisms and multiprocessing scheduling - architecture and resource-sharing design.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly about how a QPU is controlled, shared between processes and scaled, which is the QPU-side counterpart to HPC job scheduling.
- **Quantum problem** — Control-electronics complexity and serialised single-program execution limit both qubit scaling and device utilisation.
- **Classical / HPC problem** — Microarchitecture, instruction triggering and multiprocessing scheduling in the classical control plane; utilisation of a scarce shared device.
- **Mechanism** — Three-part hierarchical architecture - discrete qubit-level operations, hierarchical trigger mechanisms, and multiprocessing support enabling hardware-level asynchronous execution of multiple quantum processes.
- **Computational bottleneck** — Control-signal generation and trigger distribution as qubit count grows; device idle time under single-program execution.
- **Evaluation platform / scale** — Implemented for a 102-qubit superconducting processor deployed on a public quantum cloud platform; architecture stated to scale to 6144 qubits. / 102 qubits in deployment; 5-process parallel benchmark; 6144-qubit design target.
- **Performance metrics** — ['speedup under multi-process execution', 'CLOPS (circuit layer operations per second)']
- **Major claim (with baseline)** — Up to 4.89x speedup with a 5-process parallel setup and a 3.55x CLOPS improvement; the baseline is the same system without multiprocessing (single-process execution).
- **Limitation** — Results are for one superconducting platform and one vendor control stack; the 6144-qubit figure is a design projection, not a measurement.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-065` GraMA: A gradient matrix-guided assignment method for solving qubit mapping problems

- **Bibliographic** — Xinyu Piao et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 182 , issue date 2026-09 · pp 108485
- **DOI** — `10.1016/j.future.2026.108485` · <https://doi.org/10.1016/j.future.2026.108485>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Compilation time and computational complexity of qubit mapping as device size and circuit complexity grow; explicitly covers multi-programming scenarios.
- **Gate 2 (HPC/systems technique)** — Classical compilation scalability: replaces iterative combinatorial search and solver calls with a single matrix differentiation.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Compilation latency is a direct cost on a shared QPU pipeline; the multi-programming case ties it to device sharing.
- **Quantum problem** — Assigning logical to physical qubits under connectivity and error constraints on growing NISQ devices.
- **Classical / HPC problem** — Computational complexity and compilation time of solver-based or iterative mapping approaches at scale.
- **Mechanism** — Formulate logic-to-physical mapping as a matrix-form optimisation; compute its gradient by a single matrix differentiation; use the gradient matrix, which encodes physical-qubit centrality against logical-qubit connectivity, to pick the assignment directly.
- **Computational bottleneck** — Iterative combinatorial exploration and optimisation-solver calls in existing mapping methods.
- **Evaluation platform / scale** — Simulation study across circuit benchmarks, including multi-programming and large-scale device models. / Large-scale quantum computer models and multi-programming scenarios; exact device sizes INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['compilation time', 'execution reliability / fidelity of the mapped circuit']
- **Major claim (with baseline)** — Comparable execution reliability at significantly reduced compilation time, including for multi-programming and large devices; the baseline is existing (iterative/solver-based) mapping methods, named generically - partially BASELINE_UNCLEAR.
- **Limitation** — A single-shot analytic assignment gives up the optimality guarantees of exact methods such as FGCS-057.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-073` Universal quantum computer simulation of 50 qubits on Europe’s first exascale supercomputer harnessing its heterogeneous CPU–GPU architecture

- **Bibliographic** — Hans De Raedt et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 183 , issue date 2026-10 · pp 108592
- **DOI** — `10.1016/j.future.2026.108592` · <https://doi.org/10.1016/j.future.2026.108592>
- **arXiv** — `2511.03359`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Memory capacity beyond GPU limits, CPU-GPU interconnect bandwidth, network traffic, and end-to-end runtime - all central to the contribution.
- **Gate 2 (HPC/systems technique)** — Three explicit systems techniques: extending usable memory across the CPU-GPU interconnect into LPDDR5, adaptive data encoding to shrink the state-vector footprint, and an on-the-fly network traffic optimizer.
- **Gate 3 (future CPU/GPU/QPU relevance)** — This is the canonical HPC_FOR_Q result: how an exascale heterogeneous machine is engineered to hold and move a 2^50 state vector.
- **Quantum problem** — Exact universal quantum circuit simulation at 50 qubits, needed as a reference for device validation.
- **Classical / HPC problem** — State-vector memory grows as 2^n and exceeds aggregate GPU memory; all-to-all communication for qubit permutations saturates the network.
- **Mechanism** — JUQCS-50: (1) use high-bandwidth CPU-GPU interconnects and LPDDR5 to extend usable memory past GPU capacity; (2) adaptive data encoding trading precision and compute for memory footprint; (3) an on-the-fly network traffic optimizer.
- **Computational bottleneck** — Aggregate memory capacity and inter-node network traffic for global-qubit operations.
- **Evaluation platform / scale** — JUPITER supercomputer with NVIDIA GH200 superchips (Europe's first exascale system). / 50 qubits; exact node count INSUFFICIENT_EVIDENCE from the retrieved abstract.
- **Performance metrics** — ['qubit count simulated', 'speedup versus previous record', 'memory footprint', 'network traffic']
- **Major claim (with baseline)** — 16.6-fold speedup over the previous 48-qubit record - the baseline is explicitly the earlier JUQCS 48-qubit run on the K computer, so this compares across two different machines and two software generations.
- **Limitation** — Adaptive data encoding trades precision for memory, so results at 50 qubits carry an accuracy caveat relative to full double precision.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-079` Workflow decomposition algorithm for scheduling with quantum annealer-based hybrid solver

- **Bibliographic** — Marcin Kroczek et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 185 , issue date 2026-12 · pp 108686
- **DOI** — `10.1016/j.future.2026.108686` · <https://doi.org/10.1016/j.future.2026.108686>
- **arXiv** — `2506.01567`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_FOR_HPC`, `Q_IN_HPC` · **Branch** — `scientific_workflow_application`, `hybrid_workflow`, `qpu_scheduling_resource_mgmt`
- **Gate 1 (classical systems problem)** — Scientific workflow scheduling under deadlines, solver capacity as the binding resource limit, and decomposition to fit it - scheduling and resource allocation.
- **Gate 2 (HPC/systems technique)** — A decomposition algorithm (series-parallel / TTSP-based) plus workload-weighted deadline distribution that turns an over-sized workflow-scheduling instance into solver-ready subproblems for a hybrid quantum solver.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows concretely how a capacity-limited quantum solver can be slotted into a real workflow-scheduling pipeline, and at what quality cost.
- **Quantum problem** — Limited variable capacity of quantum and hybrid solvers relative to real problem sizes.
- **Classical / HPC problem** — Scheduling scientific workflows (task graphs) onto resources under deadline and cost objectives.
- **Mechanism** — Series-Parallel Workflow Decomposition (SPWD): a two-terminal series-parallel heuristic that splits the workflow graph, plus workload-weighted deadline distribution across the resulting subproblems, each solved by the D-Wave CQM hybrid solver via the QHyper toolchain.
- **Computational bottleneck** — Solver variable-capacity limit; quality loss introduced by decomposition.
- **Evaluation platform / scale** — D-Wave Constrained Quadratic Model hybrid solver; Gurobi as the classical reference; real workflows from WfCommons. / Real-life scientific workflow instances from WfCommons, including instances the undecomposed solver could not handle.
- **Performance metrics** — ['solvable instance size', 'schedule cost versus Gurobi reference']
- **Major claim (with baseline)** — SPWD lets the D-Wave CQM solver handle previously unsolvable instances, at a cost increase of up to 17.5% - the baseline is explicitly the Gurobi reference solution.
- **Limitation** — Decomposition costs up to 17.5% schedule quality, and the comparison shows the classical solver still produces better schedules where it can run.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4

#### `FGCS-080` Three ways to share a QPU: Scheduling strategies for hybrid Quantum-HPC applications

- **Bibliographic** — Marco Cipollini et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 185 , issue date 2026-12 · pp 108699
- **DOI** — `10.1016/j.future.2026.108699` · <https://doi.org/10.1016/j.future.2026.108699>
- **arXiv** — `2604.14955`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `qpu_scheduling_resource_mgmt`, `hpc_qpu_integration`, `hybrid_workflow`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Scheduling, resource allocation, utilisation and execution time on production HPC clusters, with the QPU as the scarce resource.
- **Gate 2 (HPC/systems technique)** — Three concrete systems mechanisms compared head to head: time-based multiplexing, dynamic resource management (malleability), and workflow decomposition.
- **Gate 3 (future CPU/GPU/QPU relevance)** — This is the heterogeneous-scheduling question stated and measured directly.
- **Quantum problem** — QPU scarcity and immature quantum software stacks; mismatch between quantum and classical programming models.
- **Classical / HPC problem** — Standard HPC scheduling mechanisms cannot express a job that holds classical nodes while waiting on a scarce accelerator, wasting classical resources.
- **Mechanism** — Implementation and comparison of three strategies - time-based multiplexing of QPU access, dynamic resource management/malleability that releases classical nodes during quantum phases, and workflow decomposition that splits hybrid jobs into separately schedulable stages.
- **Computational bottleneck** — Classical nodes idling while a job waits on the QPU, and QPU idling between hybrid iterations.
- **Evaluation platform / scale** — Production HPC clusters plus real quantum hardware. / Multiple workload scenarios spanning quantum/classical balance; exact node and QPU counts INSUFFICIENT_EVIDENCE.
- **Performance metrics** — ['classical resource consumption', 'QPU utilisation', 'cluster-level execution time']
- **Major claim (with baseline)** — Malleability and workflow decomposition cut classical resource consumption by up to 45.7% and 64% respectively for balanced hybrid jobs, while time-multiplexing gives the best QPU utilisation and cluster execution time under strong classical-quantum imbalance - the baseline is standard (non-adaptive) HPC scheduling of the same hybrid workloads.
- **Limitation** — The three strategies are complementary rather than dominant, so a production scheduler needs a policy to choose among them, which the paper frames as remaining work.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `FGCS-A02` Closed-loop calculations of electronic structure on a quantum processor and a classical supercomputer at full scale

- **Bibliographic** — Tomonori Shirakawa et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 186 , issue date 2027-01 · pp 108731
- **DOI** — `10.1016/j.future.2026.108731` · <https://doi.org/10.1016/j.future.2026.108731>
- **arXiv** — `2511.00224`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q`, `Q_FOR_HPC`, `FUTURE_WORKLOAD` · **Branch** — `hpc_qpu_integration`, `hybrid_workflow`, `quantum_runtime_orchestration`, `scientific_workflow_application`
- **Gate 1 (classical systems problem)** — Resource orchestration across 152,064 classical nodes and a co-located QPU; the paper's own stated aim is to characterise the scalability and efficiency of hybrid quantum-classical workflows, i.e. scaling, orchestration and communication between the two resources.
- **Gate 2 (HPC/systems technique)** — The contribution is the closed-loop HPC-QPU workflow itself: an on-premises Heron processor coupled to a full supercomputer allocation, with the classical side doing the heavy post-processing at full machine scale. This is quantum accelerator integration into HPC and hybrid workflow orchestration, not a chemistry method paper.
- **Gate 3 (future CPU/GPU/QPU relevance)** — The clearest existing measurement of what full-scale CPU<->QPU coupling costs and how far it scales; it directly informs resource usage, execution and orchestration for heterogeneous facilities.
- **Quantum problem** — Sampling electronic-structure configurations on a Heron processor for chemistry models beyond the reach of exact diagonalization.
- **Classical / HPC problem** — Orchestrating a closed loop between a QPU and an entire supercomputer allocation - dispatching quantum samples, running the classical post-processing across 152,064 nodes, and returning results into the next iteration, at a scale where scheduling and data movement dominate.
- **Mechanism** — Closed-loop quantum-centric supercomputing workflow: an on-premises IBM Heron quantum processor issues samples, the full Fugaku allocation performs the classical solve/post-processing, and the loop iterates. The systems contribution is the orchestration of the two resources at full machine scale.
- **Computational bottleneck** — Classical post-processing of quantum samples, which is what consumes the full-machine allocation; plus the coordination/latency of the QPU-to-supercomputer loop.
- **Evaluation platform / scale** — IBM Heron quantum processor deployed on premises with the supercomputer Fugaku (RIKEN R-CCS). / 152,064 classical Fugaku nodes - the entire machine; Heron qubit count INSUFFICIENT_EVIDENCE from the retrieved abstract.
- **Performance metrics** — ['scale of classical resources orchestrated (node count)', 'accuracy of the approximated electronic structure', 'workflow scalability/efficiency characterisation']
- **Major claim (with baseline)** — The largest electronic-structure computation to date combining quantum and classical HPC, reaching accuracy comparable to some all-classical approximation methods - the baseline is explicitly (a) exact diagonalization, which the chemistry models are stated to exceed, and (b) all-classical approximation methods for the accuracy comparison. No speedup or advantage over the classical methods is claimed, and none should be read in.
- **Limitation** — Accuracy is stated as comparable to, not better than, classical approximation methods, so the result demonstrates orchestration capability rather than quantum advantage. The workflow consumes an entire national supercomputer for one chemistry problem, which bounds its practicality. Per-component timing and the classical/quantum time split are INSUFFICIENT_EVIDENCE from the abstract.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — EXISTENCE_CHECK_SEED ('closed-loop quantum processor + Fugaku work') - confirmed to exist and assessed on its own merits, not admitted because it was seeded. Recovered by the extended cover-date sweep.

#### `FGCS-A03` DistributedEstimator: Distributed training of quantum neural networks via circuit cutting

- **Bibliographic** — Prabhjot Singh et al. · Future Generation Computer Systems 0167-739X · census year **2026** · vol 186 , issue date 2027-01 · pp 108746
- **DOI** — `10.1016/j.future.2026.108746` · <https://doi.org/10.1016/j.future.2026.108746>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `circuit_cutting_reconstruction`, `multi_qpu_distributed_qc`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Per-query time breakdown, parallel execution, exponential subexperiment growth, scaling limits and straggler sensitivity - distributed-execution cost is the measured quantity throughout.
- **Gate 2 (HPC/systems technique)** — Circuit-cutting reconstruction cost treated explicitly as a staged distributed workload, with the pipeline instrumented across partitioning, subexperiment generation, parallel execution and classical reconstruction. 'Circuit-cutting reconstruction cost' is a named INCLUDE shape in Gate 2.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Quantifies which stage of a cut-circuit workload dominates wall-clock time and where it stops scaling - directly informs execution, communication and runtime design for distributed quantum workloads.
- **Quantum problem** — Circuits too large for one device must be cut into independent subcircuits, whose results are then classically reconstructed.
- **Classical / HPC problem** — Classical reconstruction cost, exponential subexperiment fan-out, parallel scheduling of subexperiments and straggler sensitivity in the distributed execution stage.
- **Mechanism** — DistributedEstimator: a cut-aware estimator pipeline that treats circuit cutting as a staged distributed workload, instrumented across partitioning, subexperiment generation, parallel execution and classical reconstruction, with runtime traces collected per stage. Built on qiskit-addon-cutting and qiskit-machine-learning with PyTorch.
- **Computational bottleneck** — Classical reconstruction, measured as the dominant per-query cost (median 53%, 95th percentile 58% at three cuts), and O(9^c) subexperiment growth in the number of cuts.
- **Evaluation platform / scale** — Qiskit circuit-cutting and machine-learning addons with PyTorch; runtime traces on Iris and MNIST classification tasks. / Limited to small qubit counts by the O(9^c) subexperiment growth, as the paper itself reports.
- **Performance metrics** — ['per-query time share by pipeline stage', 'subexperiment count growth O(9^c)', 'scaling limit', 'straggler sensitivity', 'accuracy and robustness preservation']
- **Major claim (with baseline)** — Reconstruction dominates per-query time - median 53% and 95th-percentile 58% at three cuts - and O(9^c) subexperiment growth confines practical experiments to small qubit counts. The baseline is the paper's own uncut / fewer-cut configurations and the per-stage decomposition of its own pipeline; there is no external system baseline, so cross-system comparison is BASELINE_UNCLEAR.
- **Limitation** — The workload is QNN training on Iris and MNIST, which are small ML benchmarks rather than HPC-scale workloads, and the reported scaling limit is a property of circuit cutting itself rather than of the implementation.
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 4
- **Notes** — The coordinator anticipated BORDERLINE / NO_ABSTRACT. The ScienceDirect abstract page resolved on the first attempt, so this is classified on evidence rather than on title. The QML *target* (QNN training) is a documented false-positive class, but the *contribution* is distributed-execution cost measurement of circuit cutting, which is a named Gate 2 INCLUDE shape - so the tension the coordinator flagged resolves to INCLUDED. Recovered by the extended cover-date sweep.

### TQE — IEEE Trans. Quantum Engineering (25 papers)

#### `TQE-013` Parallelizing Quantum Simulation With Decision Diagrams

- **Bibliographic** — Shaowen Li et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-12
- **DOI** — `10.1109/tqe.2024.3364546` · <https://doi.org/10.1109/tqe.2024.3364546>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Memory capacity is the binding limit of classical circuit simulation; the paper targets it directly.
- **Gate 2 (HPC/systems technique)** — Parallelization of decision-diagram simulation (concurrent DD node operations under shared-table synchronization).
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows how the dominant HPC_FOR_Q workload behaves on parallel classical hardware and where its parallel efficiency breaks.
- **Quantum problem** — Simulating quantum state evolution on classical machines for algorithm development and verification.
- **Classical / HPC problem** — Memory capacity is the binding constraint for classical simulation; decision diagrams compress state but their manipulation is hard to parallelize (pointer chasing, shared unique tables, dynamic data structures).
- **Mechanism** — Parallelizes decision-diagram based simulation so that DD node operations are executed concurrently, trading synchronization cost against reduced wall-clock time while retaining the DD memory advantage.
- **Computational bottleneck** — Memory footprint of the state representation; contention/synchronization in shared DD tables limiting parallel speedup.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Simulation runtime/speedup versus sequential DD simulation; specific figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — Parallel decision-diagram simulation improves the scalability of classical quantum circuit simulation relative to a sequential DD simulator.
- **Limitation** — DD efficiency is circuit-structure dependent; speedup does not transfer to circuits whose DD representation does not compress.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-034` Scalable Full-Stack Benchmarks for Quantum Computers

- **Bibliographic** — Jordan Hines et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-12
- **DOI** — `10.1109/tqe.2024.3404502` · <https://doi.org/10.1109/tqe.2024.3404502>
- **arXiv** — `2312.14107`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Classical simulation cost of benchmark verification, which the construction is designed to eliminate.
- **Gate 2 (HPC/systems technique)** — Benchmark-construction methodology that scores compiler plus hardware jointly using only efficient classical computation.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Gives a way to measure a heterogeneous stack, including its classical compilation stage, past the classically simulable regime.
- **Quantum problem** — Assessing the error rate of a processor on circuits of practical interest, including the effect of its own compiler.
- **Classical / HPC problem** — Existing full-stack benchmarks require classical simulation of the benchmarked circuits, which is exponentially costly; the benchmark construction and scoring must instead use only efficient classical computation.
- **Mechanism** — A general construction that turns any set of unitary circuits into a benchmark whose success criterion is computable with efficient classical processing, thereby measuring the integrated performance of the compiler plus the hardware.
- **Computational bottleneck** — Classical simulation cost of verification, removed by construction.
- **Evaluation platform / scale** — Quantum processors (vendor/model not recoverable from the truncated abstract). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Benchmark scores for random circuit families; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — Benchmarks that assess compiler plus hardware jointly can be constructed without classical simulation of the benchmarked circuits.
- **Limitation** — Circuit classes must admit an efficiently checkable structure; the benchmark measures aggregate performance, not error localization.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Verification rebuttal (Gate 2), kept INCLUDED. The systems contribution is not the benchmark scores but the construction itself: the paper's defining constraint is that both the benchmark circuits and their scoring must use only efficient classical computation, which removes the exponential classical-simulation step that every prior full-stack benchmark required. That is a computational-cost-driven methodology, not a device-characterization result. Second, the object measured is explicitly the integrated performance of the processor's classical compilation algorithms together with its low-level operations, so a classical stage of the stack is inside the measurement boundary. Benchmarking infrastructure and quantum performance modeling are named INCLUDE shapes in the criteria, and this record meets both on those grounds rather than on Gate-1 framing alone.

#### `TQE-036` Advanced Shuttle Strategies for Parallel QCCD Architectures

- **Bibliographic** — Weining Dai et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-18
- **DOI** — `10.1109/tqe.2024.3408757` · <https://doi.org/10.1109/tqe.2024.3408757>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `architecture_control`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Execution time is dominated by serialized ion transport; shuttle movements must be planned and parallelized.
- **Gate 2 (HPC/systems technique)** — Architecture/topology and shuttle-scheduling co-design enabling concurrent transport.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows how architecture choices set the throughput a QPU can offer to a host system.
- **Quantum problem** — Trapped-ion scalability is limited by trap capacity, forcing ion shuttling between zones for every non-local operation.
- **Classical / HPC problem** — Shuttle scheduling is an architecture-aware routing/scheduling problem: the compiler must plan parallel ion movements over a topology, and execution time is dominated by this movement schedule.
- **Mechanism** — Introduces trap topologies supporting parallel shuttling together with shuttle-planning strategies that exploit them, evaluated against the linear QCCD baseline.
- **Computational bottleneck** — Serialization of ion transport operations; scheduling of concurrent shuttles without collisions.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Reduction in shuttling operations / execution time versus linear QCCD topologies; exact figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — Parallel-capable QCCD topologies with matched shuttle strategies reduce movement overhead relative to linear QCCD architectures.
- **Limitation** — Topologies are evaluated in simulation; physical feasibility of the proposed trap layouts is assumed.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-038` FASQuiC: Flexible Architecture for Scalable Spin Qubit Control

- **Bibliographic** — Mathieu Toubeix et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-16
- **DOI** — `10.1109/tqe.2024.3409811` · <https://doi.org/10.1109/tqe.2024.3409811>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `architecture_control`
- **Gate 1 (classical systems problem)** — Control channel count, waveform memory and digital feedback latency scale with qubit count.
- **Gate 2 (HPC/systems technique)** — FPGA control architecture (direct digital synthesis, bitstream switching, multichannel synchronization) with a measured latency figure.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Fixes the real-time latency budget (76.8 ns worst case) available to feedback-driven execution models.
- **Quantum problem** — Spin-qubit control requires precise, synchronized, fast-feedback pulse sequences across many channels.
- **Classical / HPC problem** — Control hardware cost, channel count scaling, waveform memory and feedback latency are classical system-design constraints that grow with qubit count.
- **Mechanism** — A direct-digital-synthesis architecture on FPGA generating programmable ramps, frequency combs and arbitrary waveforms at 5 GS/s, with bitstream switching for reconfigurability and synchronized multichannel operation.
- **Computational bottleneck** — Digital feedback latency and per-channel resource cost in the FPGA fabric.
- **Evaluation platform / scale** — FPGA-based control system (FASQuiC). / 5 GS/s generation; multiple synchronized channels (exact count not recoverable from the truncated abstract).
- **Performance metrics** — Worst-case digital feedback latency 76.8 ns; 5 GS/s arbitrary waveform generation. Baseline for the latency figure is not stated in the abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — A reconfigurable FPGA control architecture delivers 5 GS/s multichannel spin-qubit control with worst-case 76.8 ns digital feedback latency.
- **Limitation** — Scalability is argued architecturally; the abstract does not report operation at large channel counts.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-048` BeSnake: A Routing Algorithm for Scalable Spin-Qubit Architectures

- **Bibliographic** — Nikiforos Paraskevopoulos et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-22
- **DOI** — `10.1109/tqe.2024.3429451` · <https://doi.org/10.1109/tqe.2024.3429451>
- **arXiv** — `2403.16090`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Routing compile time is treated as a primary metric alongside routed-circuit execution time.
- **Gate 2 (HPC/systems technique)** — Architecture-aware routing algorithm (BFS over SWAP and shuttle primitives) evaluated on compiler runtime as well as output quality.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Quantifies compilation scalability, the classical cost of preparing work for a QPU, as arrays grow.
- **Quantum problem** — Two-qubit interactions on large spin-qubit arrays require moving qubit state across a constrained topology.
- **Classical / HPC problem** — Routing is a classical compilation problem whose runtime must itself stay tractable as array size grows; the paper treats compiler execution time as a primary metric alongside circuit quality.
- **Mechanism** — beSnake, a BFS-based routing algorithm that chooses between SWAP and shuttle operations to minimize execution time and fidelity loss while keeping routing computation fast.
- **Computational bottleneck** — Compile-time cost of routing search on large architectures.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Routing quality (execution time, fidelity) and routing computation time versus prior SWAP-only methods; exact figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — A BFS-based router that admits shuttle operations improves routed-circuit execution time and fidelity while keeping routing computation fast, relative to SWAP-only routing baselines.
- **Limitation** — Targets spin-qubit architectures specifically; shuttle cost model is architecture-dependent.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-062` FPGA-Based Distributed Union-Find Decoder for Surface Codes

- **Bibliographic** — Namitha Liyanage et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 5 · pp 1-18
- **DOI** — `10.1109/tqe.2024.3467271` · <https://doi.org/10.1109/tqe.2024.3467271>
- **arXiv** — `2406.08491`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `qec_classical_processing`
- **Gate 1 (classical systems problem)** — Decoding latency must stay ahead of syndrome generation or the computation backs up exponentially.
- **Gate 2 (HPC/systems technique)** — Distributed parallel decoder implemented on FPGA with the Helios hybrid tree-grid processing-element architecture.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Sets the latency and hardware-area budget for the classical real-time processor attached to a fault-tolerant QPU.
- **Quantum problem** — Real-time surface-code decoding must keep pace with syndrome generation or the computation suffers exponential backlog slowdown.
- **Classical / HPC problem** — Decoding is a latency-critical classical workload; the paper builds a parallel/distributed hardware architecture and studies its time complexity and resource efficiency.
- **Mechanism** — A distributed Union-Find decoder on an FPGA using the Helios architecture, which organizes parallel processing elements in a hybrid tree-grid structure so that syndrome data is processed locally and merged hierarchically.
- **Computational bottleneck** — Decoding latency per measurement round; parallel resource count scaling as O(d^3); interconnect between processing elements.
- **Evaluation platform / scale** — Xilinx VCU129 FPGA. / Code distances up to d=21 in the latency-optimized configuration; d=51 in the resource-efficient configuration.
- **Performance metrics** — 11.5 ns average decoding time per measurement round at d=21 under 0.1% phenomenological noise; 23.7 ns at d=17 under circuit-level noise; 544 ns per measurement round at d=51 in the resource-optimized configuration. Baseline: prior decoder implementations (the paper claims it is faster than existing implementations).
- **Major claim (with baseline)** — With O(d^3) parallel resources the distributed UF decoder attains sublinear average time complexity in d, with per-round decoding time decreasing as d grows over the measured range.
- **Limitation** — Parallel resource demand grows as O(d^3), so the latency result is bought with FPGA area; noise models are phenomenological/circuit-level simulation rather than live hardware syndromes.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-075` C3-VQA: Cryogenic Counter-Based Coprocessor for Variational Quantum Algorithms

- **Bibliographic** — Yosuke Ueno et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2024** · vol 6 · pp 1-17
- **DOI** — `10.1109/tqe.2024.3521442` · <https://doi.org/10.1109/tqe.2024.3521442>
- **arXiv** — `2409.07847`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `architecture_control`, `hpc_qpu_integration`
- **Gate 1 (classical systems problem)** — Intertemperature wire bandwidth and the cryostat thermal budget bound how many qubits can be wired out.
- **Gate 2 (HPC/systems technique)** — Near-data processing: an in-cryostat SFQ coprocessor performs part of the expectation-value reduction before data crosses the boundary.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs where classical compute should sit in the temperature/data-movement hierarchy of a hybrid machine.
- **Quantum problem** — Variational algorithms require many shots whose measurement results must all be transported out of the cryostat, and every wire carries a passive heat load.
- **Classical / HPC problem** — Thermal budget, interconnect bandwidth and near-data processing: a classic accelerator-placement/data-movement trade-off, here with cooling capacity as the constrained resource.
- **Mechanism** — C3-VQA, a single-flux-quantum coprocessor at the 4 K stage that precomputes part of the expectation-value accumulation for VQAs and buffers intermediates in counters and bit-operation units, so fewer results cross the temperature boundary.
- **Computational bottleneck** — Intertemperature wire bandwidth and the resulting heat dissipation; power of in-cryostat logic.
- **Evaluation platform / scale** — Design-level evaluation with workload analysis of VQA execution (SFQ logic at 4 K). / Case study extrapolated to a 10 000-qubit system.
- **Performance metrics** — 30% reduction in total 4 K heat dissipation under sequential-shot execution and 81% under parallel-shot execution; 87% in a quantum-chemistry case study at 10 000 qubits. Baseline: the same cryogenic system without the coprocessor.
- **Major claim (with baseline)** — Moving part of the expectation-value reduction into ultra-low-power in-cryostat logic reduces 4 K heat dissipation by 30-87% depending on shot execution mode and system size, relative to sending all measurement results out.
- **Limitation** — Evaluation is architectural/analytical rather than a fabricated SFQ chip; benefit is specific to VQA-style workloads with large shot counts.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-078` Benchmarking Quantum Circuit Transformation With QKNOB Circuits

- **Bibliographic** — Sanjiang Li et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-15
- **DOI** — `10.1109/tqe.2025.3527399` · <https://doi.org/10.1109/tqe.2025.3527399>
- **arXiv** — `2301.08932`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `benchmarking_performance_modeling`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Compiler solution quality cannot be interpreted without a tight reference, so compilation cost is unmeasurable in practice.
- **Gate 2 (HPC/systems technique)** — Benchmark construction with built-in near-optimal transformation cost, used to expose optimality gaps of QCT algorithms.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Provides the measurement basis for comparing the compilation stage of competing quantum software stacks.
- **Quantum problem** — Connectivity-constrained hardware requires circuit transformation before execution.
- **Classical / HPC problem** — Compiler evaluation methodology: without knowing the optimum, reported SWAP-count and depth overheads of competing compilers cannot be interpreted; this is a benchmarking-infrastructure problem for a classical compilation stage.
- **Mechanism** — QKNOB constructs benchmark circuits with a built-in transformation of known near-optimal SWAP count and depth overhead, so any compiler's output can be compared to a tight reference.
- **Computational bottleneck** — Compiler search cost and solution quality on constructed instances.
- **Evaluation platform / scale** — State-of-the-art quantum circuit transformation algorithms evaluated on QKNOB circuits. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Optimality gaps in SWAP count and depth for evaluated QCT algorithms; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — Benchmarks with known near-optimal transformation cost give an unbiased comparison of circuit transformation algorithms, revealing optimality gaps that prior benchmark sets could not expose.
- **Limitation** — Constructed circuits may not represent application circuit structure; near-optimality is by construction, not proof of the true optimum.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-090` Quantum Circuit Compilation for Trapped-Ion Processors With the Drive-Through Architecture

- **Bibliographic** — Che-Ming Chang et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-14
- **DOI** — `10.1109/tqe.2025.3548423` · <https://doi.org/10.1109/tqe.2025.3548423>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `architecture_control`
- **Gate 1 (classical systems problem)** — Transport-operation scheduling determines execution time and fidelity on the target architecture.
- **Gate 2 (HPC/systems technique)** — A full compilation flow (mapping, scheduling, transport planning) built for an architecture whose primitive set differs from standard hardware.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows how a change of hardware primitives propagates into the compiler, a recurring issue for heterogeneous back ends.
- **Quantum problem** — A trapped-ion architecture designed to minimize heat generation changes the primitive operation set, so existing compilers do not apply.
- **Classical / HPC problem** — Compilation for an architecture with transport-based primitives requires new mapping, scheduling and routing passes; the classical compiler stage determines achievable fidelity and execution time.
- **Mechanism** — A compilation system tailored to the drive-through architecture that plans transport-gate sequences and schedules ion movement for the target program.
- **Computational bottleneck** — Scheduling of transport operations; compile-time search over movement plans.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Fidelity/execution-time of compiled programs on the drive-through architecture; figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — A compilation flow specific to transport-gate trapped-ion architectures produces executable high-fidelity programs where general-purpose compilers do not apply.
- **Limitation** — Single-architecture study; results are simulation-based.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-098` A Comprehensive Cross-Model Framework for Benchmarking the Performance of Quantum Hamiltonian Simulations

- **Bibliographic** — Avimita Chatterjee et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-26
- **DOI** — `10.1109/tqe.2025.3558090` · <https://doi.org/10.1109/tqe.2025.3558090>
- **arXiv** — `2409.06919`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — The classical reference computation (simulation or exact diagonalization) is the cost that limits benchmarking.
- **Gate 2 (HPC/systems technique)** — A benchmarking framework and software implementation with three reference modes, including mirror circuits that need no classical reference.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Enables performance measurement of a quantum workload when the classical cross-check is no longer affordable.
- **Quantum problem** — Trotterized Hamiltonian evolution is a core workload whose quality on real hardware must be quantified.
- **Classical / HPC problem** — Benchmarking methodology and software framework: three benchmark modes trade off against the classical cost of producing a reference (noiseless simulation, exact diagonalization, or mirror circuits that need no reference).
- **Mechanism** — A cross-model benchmarking framework and software implementation supporting comparison against a noiseless simulator, against exact diagonalization, and via scalable mirror circuits when classical reference is infeasible.
- **Computational bottleneck** — Classical simulation/diagonalization cost of the reference, which is what forces the mirror-circuit mode.
- **Evaluation platform / scale** — Gate-based quantum computers plus classical simulators (specific devices not recoverable from the truncated abstract). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Fidelity/quality metrics per benchmark mode; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — A single framework with three reference modes allows Hamiltonian-simulation benchmarking to extend past the point where classical reference computation is affordable.
- **Limitation** — Mirror-circuit mode measures a proxy for the target workload rather than the workload itself.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-101` Modeling and Performance Evaluation of Hybrid Classical–Quantum Serverless Computing Platforms

- **Bibliographic** — Claudio Cicconetti  · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-13
- **DOI** — `10.1109/tqe.2025.3567322` · <https://doi.org/10.1109/tqe.2025.3567322>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `FUTURE_WORKLOAD` · **Branch** — `hpc_qpu_integration`, `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Queueing, scheduling, resource contention and quality of service for a shared classical-plus-QPU infrastructure.
- **Gate 2 (HPC/systems technique)** — A serverless system model with an analytical/simulation performance evaluation of the hybrid platform under load.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Models QPUs as shared datacenter resources, the core Q_IN_HPC question of how QPU sharing affects user-visible performance.
- **Quantum problem** — Variational and other hybrid algorithms alternate between classical and quantum execution and need tight, low-overhead coupling of the two resources.
- **Classical / HPC problem** — Resource management, queueing, scheduling and quality of service for a shared infrastructure hosting both classical functions and QPUs — a datacenter systems problem.
- **Mechanism** — Defines a system model for a hybrid classical-quantum serverless platform together with an analytical/simulation performance evaluation of its behaviour under load.
- **Computational bottleneck** — Queueing delay and resource contention at the QPU; invocation overheads of the serverless layer.
- **Evaluation platform / scale** — Model-based performance evaluation (analysis and simulation). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Response time / throughput / utilization as functions of system parameters; specific values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — A serverless system model captures the performance trade-offs of hybrid classical-quantum platforms and quantifies how QPU sharing affects user-visible quality of service.
- **Limitation** — Model-based rather than measured on a deployed platform; QPU service-time assumptions drive the results.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-127` End-to-End Workflow for Machine-Learning-Based Qubit Readout With QICK and hls4ml

- **Bibliographic** — Giuseppe Di Guglielmo et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-10
- **DOI** — `10.1109/tqe.2025.3604712` · <https://doi.org/10.1109/tqe.2025.3604712>
- **arXiv** — `2501.14663`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `architecture_control`, `qec_classical_processing`
- **Gate 1 (classical systems problem)** — Real-time inference latency and FPGA resource budget for qubit-state discrimination at scale.
- **Gate 2 (HPC/systems technique)** — Hardware/software codesign toolchain that compiles quantization-aware-trained networks into production control firmware (hls4ml into QICK on RFSoC).
- **Gate 3 (future CPU/GPU/QPU relevance)** — Establishes a reusable pattern for putting classical accelerators inside the control plane, applicable to decoders and feed-forward logic.
- **Quantum problem** — Superconducting qubit readout must classify measurement traces accurately and fast enough for mid-circuit feedback.
- **Classical / HPC problem** — Real-time inference on FPGA under strict latency and resource budgets; an end-to-end hardware/software toolchain from trained model to deployed firmware.
- **Mechanism** — An end-to-end workflow embedding quantization-aware-trained neural networks into the QICK firmware on Xilinx RFSoC FPGAs via hls4ml, with Python APIs from model to bitstream.
- **Computational bottleneck** — Inference latency and FPGA resource (DSP/LUT) usage; readout data rate.
- **Evaluation platform / scale** — Xilinx RFSoC FPGA running QICK; hls4ml toolchain; experimental superconducting qubit readout. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Readout accuracy and inference latency of the deployed model; specific values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — ML-based readout discriminators can be compiled into production quantum-control firmware with latency compatible with real-time operation, demonstrated experimentally.
- **Limitation** — Demonstration scale (number of qubits/channels) is not stated in the abstract; model complexity is bounded by FPGA resources.
- **Artifact** — PARTIAL · https://github.com/openquantumhardware/qick
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-130` Benchmarking the Ability of a Controller to Execute Quantum Error Corrected Non-Clifford Circuits

- **Bibliographic** — Yaniv Kurman et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-14
- **DOI** — `10.1109/tqe.2025.3608053` · <https://doi.org/10.1109/tqe.2025.3608053>
- **arXiv** — `2311.07121`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `qec_classical_processing`, `benchmarking_performance_modeling`, `architecture_control`
- **Gate 1 (classical systems problem)** — Closed-loop mid-circuit latency: readout, decode, decision and feed-forward must fit inside the round budget.
- **Gate 2 (HPC/systems technique)** — A controller-level benchmark suite that exercises the real-time classical subsystem end to end rather than component by component.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Tells us whether a given classical control stack can sustain fault-tolerant execution, which component specifications do not reveal.
- **Quantum problem** — Non-Clifford gates under QEC require modifying the physical gate sequence within the same circuit based on decoding results of earlier measurements.
- **Classical / HPC problem** — Closed-loop latency of the classical control system: measurement readout, decoding, decision and feed-forward must complete inside the coherence/round budget. The contribution is a benchmark for that classical subsystem.
- **Mechanism** — Defines benchmark circuits and metrics that jointly exercise measurement, real-time decoding and conditional gate dispatch, so a controller can be scored end to end rather than component by component.
- **Computational bottleneck** — Mid-circuit decode-to-feed-forward latency; controller throughput for conditional instruction streams.
- **Evaluation platform / scale** — Quantum control system executing QEC circuits (specific hardware not recoverable from the truncated abstract). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Controller latency and success metrics on the proposed benchmarks; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — A controller-level benchmark suite exposes whether a classical control stack can sustain decode-dependent feed-forward, which component-level specifications do not reveal.
- **Limitation** — Benchmarks are tied to particular QEC gadget structures; portability across control architectures needs checking.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-131` Quantum Circuit Optimization and MBQC Scheduling With a Pauli Tracking Library

- **Bibliographic** — Jannis Ruh et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-12
- **DOI** — `10.1109/tqe.2025.3610112` · <https://doi.org/10.1109/tqe.2025.3610112>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `qec_classical_processing`
- **Gate 1 (classical systems problem)** — Classical bookkeeping cost plus the measurement-ordering (precedence) scheduling problem it induces.
- **Gate 2 (HPC/systems technique)** — A Pauli-tracking framework with a software library and a numerical study of the resulting scheduling problem.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Characterizes runtime-layer work the classical stack must perform every shot in measurement-based and error-corrected execution.
- **Quantum problem** — In MBQC and Clifford-implemented error-corrected circuits, byproduct Pauli operators impose a partial order on measurements.
- **Classical / HPC problem** — Classical bookkeeping and scheduling: tracking Pauli frames removes gates from the hardware stream and yields precedence constraints that a scheduler must satisfy; the paper investigates the scheduling problem numerically and ships a software library.
- **Mechanism** — A framework for commuting Pauli operators through Clifford circuits (Pauli tracking), plus an independent software library implementing it for MBQC, with numerical study of the induced scheduling problem.
- **Computational bottleneck** — Classical tracking bookkeeping cost and the measurement-ordering/scheduling search.
- **Evaluation platform / scale** — Numerical study using the accompanying software library. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Reduction in executed Pauli gates and schedule length/depth; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — Pauli tracking both removes Pauli gates from the hardware instruction stream and exposes the measurement-order constraints needed for MBQC scheduling, implemented in a reusable library.
- **Limitation** — Restricted to Clifford-implementable settings; scheduling results are numerical rather than on hardware.
- **Artifact** — PARTIAL
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-132` Exploration of Design Alternatives for Reducing Idle Time in Shor's Algorithm: A Study on Monolithic and Distributed Quantum Systems

- **Bibliographic** — Moritz Schmidt et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-25
- **DOI** — `10.1109/tqe.2025.3610800` · <https://doi.org/10.1109/tqe.2025.3610800>
- **arXiv** — `2503.22564`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Task serialization produces idle time that dominates overall execution time.
- **Gate 2 (HPC/systems technique)** — Static timing analysis plus task reordering for concurrency, evaluated for monolithic and distributed system organizations.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Exposes the schedule structure of a flagship quantum workload and how it changes when the machine is distributed.
- **Quantum problem** — Shor's algorithm implementations are dominated by long sequences of modular-arithmetic tasks with serialization-induced idle qubits.
- **Classical / HPC problem** — Execution-flow scheduling and static timing analysis: identify idle time, reorder tasks for concurrency, and evaluate monolithic versus distributed system organizations — a classic parallel-execution scheduling analysis.
- **Mechanism** — Adopts a mid-level task abstraction of the algorithm, applies static timing analysis to locate idle intervals, and proposes an alternating design that reorders tasks for simultaneous execution while preserving qubit efficiency; extends the analysis to distributed multi-node systems.
- **Computational bottleneck** — Task serialization and resulting qubit idle time; inter-node communication in the distributed variant.
- **Evaluation platform / scale** — Static timing analysis across multiple platform models. / Monolithic and distributed configurations (node counts not recoverable from the truncated abstract).
- **Performance metrics** — Reduction in idle time and overall execution time; the abstract states a substantial reduction but gives no quantified baseline (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — Task-level reordering reduces idle time and overall execution time of Shor's algorithm, with different trade-offs for monolithic versus distributed systems.
- **Limitation** — Analysis is at the timing-model level, not measured on hardware; gains depend on the assumed task latencies.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-137` Network-Assisted Collective Operations for Efficient Distributed Quantum Computing

- **Bibliographic** — Iago Fernández Llovo et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-14
- **DOI** — `10.1109/tqe.2025.3619387` · <https://doi.org/10.1109/tqe.2025.3619387>
- **arXiv** — `2502.19118`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`
- **Gate 1 (classical systems problem)** — Inter-QPU communication cost (Bell pairs and accompanying classical communication) for non-local gates.
- **Gate 2 (HPC/systems technique)** — Collective-operation design borrowed from HPC interconnects: distributed fan-out to a central node instead of pairwise entanglement swapping.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs interconnect topology and collective-operation choices for multi-QPU execution, with an explicit optimality gap of one Bell pair.
- **Quantum problem** — Distributed quantum computing needs non-local gates between QPUs, normally realized with pairwise entanglement and swapping.
- **Classical / HPC problem** — Communication cost and collective-operation design: the paper borrows the fan-out/reduction pattern used by HPC interconnects and quantifies entanglement (i.e. communication) cost as a function of node count.
- **Mechanism** — Distributes a general diagonal gate over any number of nodes via distributed fan-out operations to a central node, requiring only preshared entanglement, local operations and classical communication.
- **Computational bottleneck** — Bell-pair (communication resource) consumption and the classical communication rounds that accompany it.
- **Evaluation platform / scale** — Analytical construction with protocol cost analysis. / Arbitrary node counts; distributed Grover analysed over multiple partitions.
- **Performance metrics** — A general diagonal gate costs one additional Bell pair over the optimum achievable with all-to-all preshared entanglement; distributed Grover's Bell-pair cost grows linearly with the number of Grover iterations and the number of partitions. Baseline: entanglement-swapping-based distribution and the all-to-all-entanglement optimum.
- **Major claim (with baseline)** — Central-node fan-out gives near-optimal communication cost for distributed collective quantum operations (one extra Bell pair for a general diagonal gate) without assuming full connectivity.
- **Limitation** — Assumes a central node and preshared entanglement supply; does not model entanglement generation rate or failure.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-142` Leveraging Quantum Machine Learning Generalization to Significantly Speed up Quantum Compilation

- **Bibliographic** — Alon Kukliansky et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-12
- **DOI** — `10.1109/tqe.2025.3622495` · <https://doi.org/10.1109/tqe.2025.3622495>
- **arXiv** — `2405.12866`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Compiler inner-loop cost: O(4^n) matrix-matrix operations dominate compile time.
- **Gate 2 (HPC/systems technique)** — Replacing the numerical optimizer's linear algebra with O(2^n) sampled circuit simulations inside a production compiler (BQSKit).
- **Gate 3 (future CPU/GPU/QPU relevance)** — Quantifies compilation throughput against a named baseline (average 69x on >8-qubit circuits), the classical stage between an application and a QPU.
- **Quantum problem** — Compilation by numerical instantiation of parameterized circuit templates.
- **Classical / HPC problem** — Compile time and asymptotic cost of the compiler's inner loop: O(4^n) matrix-matrix operations dominate, and the paper replaces them with O(2^n) circuit simulations on sampled inputs.
- **Mechanism** — QFactor-Sample evaluates the objective by simulating the circuit on a set of sample input states rather than forming full unitaries, with the number of samples tied to circuit simplicity; integrated into the BQSKit compiler.
- **Computational bottleneck** — Cost of the numerical optimization inner loop; the sample-count versus accuracy trade-off; interaction with partitioning-based compilation.
- **Evaluation platform / scale** — BQSKit quantum compiler, compared against a state-of-the-art domain-specific optimizer. / Validated on a large circuit set; speedup reported for circuits with more than 8 qubits.
- **Performance metrics** — Average speedup factor of 69 in compile time for circuits with more than 8 qubits, against a state-of-the-art domain-specific optimizer; improved scalability with qubit count.
- **Major claim (with baseline)** — Replacing O(4^n) matrix-matrix operations with O(2^n) sampled circuit simulations gives an average 69x compile-time speedup on >8-qubit circuits relative to the prior domain-specific optimizer.
- **Limitation** — Sampling introduces a hyperparameter (number of samples) requiring tuning; accuracy depends on circuit simplicity.
- **Artifact** — PARTIAL · https://github.com/BQSKit/bqskit
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-143` Optimized Quantum Circuit Partitioning Across Multiple Quantum Processors

- **Bibliographic** — Eneet Kaur et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 6 · pp 1-17
- **DOI** — `10.1109/tqe.2025.3623158` · <https://doi.org/10.1109/tqe.2025.3623158>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `circuit_cutting_reconstruction`
- **Gate 1 (classical systems problem)** — Partitioning work across several processors with an inter-processor communication cost (title-level evidence only).
- **Gate 2 (HPC/systems technique)** — Optimization of circuit partitioning across multiple QPUs, structurally the same as graph partitioning for distributed execution.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Bears directly on how a workload is split across several QPUs; details require full-text retrieval (NO_ABSTRACT).
- **Quantum problem** — A circuit too large for one QPU must be split across several processors.
- **Classical / HPC problem** — Partitioning/placement across compute nodes with an inter-node communication cost — the same optimization shape as classical graph partitioning for distributed execution.
- **Mechanism** — NO_ABSTRACT: mechanism not recoverable. The abstract was not retrieved and the IEEE landing page could not be fetched.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — INSUFFICIENT_EVIDENCE — only the title 'Optimized Quantum Circuit Partitioning Across Multiple Quantum Processors' is available.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-150` Hardware-Aware and Resource-Efficient Circuit Packing and Scheduling on Trapped-Ion Quantum Computers

- **Bibliographic** — Miguel Palma et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2025** · vol 7 · pp 1-15
- **DOI** — `10.1109/tqe.2025.3632540` · <https://doi.org/10.1109/tqe.2025.3632540>
- **arXiv** — `2512.20554`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC` · **Branch** — `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Device utilization and job queueing under single-tenant execution; multi-tenancy is the stated problem.
- **Gate 2 (HPC/systems technique)** — Static scheduling formulated as two-dimensional packing with hardware shuttling constraints, plus balanced scheduling across a module cluster.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Addresses QPU resource management and throughput in a shared service, the scheduling problem a quantum-equipped centre will face.
- **Quantum problem** — Single-tenant execution on quantum cloud services leaves most qubits idle while job queues grow.
- **Classical / HPC problem** — Multi-tenancy, packing and scheduling: static circuit scheduling is formulated as a two-dimensional packing problem with hardware shuttling constraints, and balanced scheduling is extended across a cluster of modules.
- **Mechanism** — CircPack, a hardware-aware packing framework for QCCD trapped-ion devices that solves 2-D packing with shuttling constraints and balances circuits across independent modules.
- **Computational bottleneck** — Device utilization and queue waiting time; shuttling constraints limiting feasible packings; packing search cost.
- **Evaluation platform / scale** — Modular QCCD trapped-ion device models; comparison against superconducting-targeted quantum multiprogramming approaches. / Cluster of independent QCCD modules (module count not stated in the abstract).
- **Performance metrics** — Up to 70.72% better fidelity, 62.67% higher utilization and 32.80% improved layer reduction, measured against superconducting-oriented quantum-multiprogramming baselines.
- **Major claim (with baseline)** — Hardware-aware packing for trapped-ion QCCD devices improves utilization and fidelity over multiprogramming methods designed for superconducting hardware.
- **Limitation** — Static (compile-time) scheduling only; results are simulation-based against baselines built for a different hardware class, so the comparison is partly cross-platform.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-167` Improving Decision Diagram-Based Quantum Circuit Simulation Using Static Variable Ordering and Multinode Ring Communication

- **Bibliographic** — Yusuke Kimura et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol 7 · pp 1-15
- **DOI** — `10.1109/tqe.2026.3654543` · <https://doi.org/10.1109/tqe.2026.3654543>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Memory footprint of the state representation and inter-node communication in distributed simulation.
- **Gate 2 (HPC/systems technique)** — Static variable ordering combined with multinode parallel DD simulation over a ring communication topology.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows how classical quantum-circuit simulation scales across nodes and which communication structure it needs.
- **Quantum problem** — Classical simulation of quantum circuits is required because large machines are scarce and do not expose state vectors.
- **Classical / HPC problem** — Memory-efficient representation plus multinode parallelization: DD processing time depends heavily on variable order, and distributing DD work across nodes requires a communication scheme.
- **Mechanism** — A static variable-ordering method with general applicability, combined with multinode parallel DD simulation using ring communication between nodes.
- **Computational bottleneck** — DD node count as a function of variable order; inter-node communication in the ring topology; memory per node.
- **Evaluation platform / scale** — Multinode classical cluster running a DD-based simulator (node count not recoverable from the truncated abstract). / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Simulation time/memory improvement from ordering and from multinode execution; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — A generally applicable static variable ordering plus ring-based multinode communication improves DD-based simulation time relative to prior ordering heuristics and single-node execution.
- **Limitation** — Static ordering cannot adapt to circuit phases; ring communication may not be the best topology at larger node counts.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-193` Cut&amp;shoot: Distributed Execution of Quantum Circuit Fragments

- **Bibliographic** — Giuseppe Bisicchia et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol (Early Access) · pp 1-14
- **DOI** — `10.1109/tqe.2026.3675340` · <https://doi.org/10.1109/tqe.2026.3675340>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `circuit_cutting_reconstruction`, `quantum_runtime_orchestration`, `hybrid_workflow`
- **Gate 1 (classical systems problem)** — Distributed execution of circuit fragments plus the classical reconstruction cost of recombining them.
- **Gate 2 (HPC/systems technique)** — An orchestration pipeline composing circuit cutting with shot-wise distribution across backends.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Defines a workflow shape that Quantum-HPC middleware must support: fragment dispatch, shot distribution and result aggregation.
- **Quantum problem** — NISQ devices limit qubit count and fidelity, so large circuits must be fragmented and their results recombined.
- **Classical / HPC problem** — Distributed execution and orchestration: the pipeline must dispatch fragments and shot batches to multiple backends and reconstruct the result, which is a workflow/runtime problem with classical reconstruction cost.
- **Mechanism** — Cut&Shoot, a pipeline that composes circuit cutting with shot-wise distribution, orchestrating fragment execution across resources and merging the outcomes.
- **Computational bottleneck** — Classical reconstruction cost of cut circuits; distribution and aggregation of shots across backends.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Fidelity/scalability of the combined pipeline versus cutting or shot distribution alone; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — Combining circuit cutting with shot-wise distribution in a single orchestrated pipeline improves scalability and reliability relative to applying either technique alone.
- **Limitation** — Reconstruction overhead still grows with the number of cuts; evaluation scale not stated in the abstract.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-207` Reducing Maximum Subcircuits Depth in Quantum Circuit Cutting

- **Bibliographic** — Milad Eslaminia et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol 7 · pp 3103209-3103209
- **DOI** — `10.1109/tqe.2026.3690593` · <https://doi.org/10.1109/tqe.2026.3690593>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `circuit_cutting_reconstruction`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Post-mapping subcircuit depth and the search cost of choosing cut placements.
- **Gate 2 (HPC/systems technique)** — A cutting framework coupled to the mapper's cost model so cut selection anticipates routing overhead.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shows how a runtime should plan fragmented execution when the compiler stage, not just qubit count, determines feasibility.
- **Quantum problem** — Circuit cutting lets small devices execute large circuits, but deep subcircuits lose fidelity exponentially with depth.
- **Classical / HPC problem** — Cut selection as a joint cutting-and-mapping cost optimization: the classical cutter must anticipate the mapping/routing overhead that will inflate subcircuit depth.
- **Mechanism** — A circuit-cutting framework that reduces the variance in post-mapping subcircuit depth by taking the target hardware's mapping consequences into account when placing cuts.
- **Computational bottleneck** — Post-mapping subcircuit depth; search cost over cut placements.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Reduction in maximum subcircuit depth and resulting fidelity improvement; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — Cut placement that accounts for post-mapping depth yields shallower worst-case subcircuits than qubit-count-only cutting methods.
- **Limitation** — Adds coupling between the cutter and the mapper, increasing compile-time complexity; sampling overhead of cutting is unchanged.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

#### `TQE-214` ZAP: Zoned Architecture and Performant Compiler for Field-Programmable Atom Array

- **Bibliographic** — Chen Huang et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol 7 · pp 3103619-3103619
- **DOI** — `10.1109/tqe.2026.3696707` · <https://doi.org/10.1109/tqe.2026.3696707>
- **arXiv** — `2411.14037`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `architecture_control`
- **Gate 1 (classical systems problem)** — Compile-time cost of repeated global search over a dynamically reconfigurable architecture.
- **Gate 2 (HPC/systems technique)** — Compiler-architecture codesign: zoned array plus a deterministic single-pass flow combining ASAP scheduling, look-ahead placement and conflict-aware routing.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Demonstrates the compile-time versus quality trade-off that heterogeneous back ends will force on the software stack.
- **Quantum problem** — Field-programmable atom arrays are dynamically reconfigurable, so logical circuits must be mapped onto moving atoms subject to crosstalk and transport constraints.
- **Classical / HPC problem** — Compile time versus solution quality: prior approaches rely on repeated global search; the contribution is a deterministic single-pass compilation flow with scheduling, placement and routing stages.
- **Mechanism** — ZAP partitions the array into storage and entanglement zones and combines hardware-aware as-soon-as-possible separate scheduling, look-ahead placement and conflict-aware routing in one compilation pass.
- **Computational bottleneck** — Compiler search cost (avoided by the single-pass design); atom transport time and crosstalk in the produced schedule.
- **Evaluation platform / scale** — Field-programmable atom array architecture model. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Compile time and circuit-quality metrics versus search-based neutral-atom compilers; the arXiv page could not be parsed, so exact figures are INSUFFICIENT_EVIDENCE (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — A zoned architecture plus a deterministic single-pass compiler avoids repeated global search while controlling crosstalk and transport overhead.
- **Limitation** — Deterministic single-pass compilation trades optimality for speed; results are architecture-model based.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-223` DAG-Aware Gate Fusion for Efficient State-Vector Quantum-Circuit Simulation

- **Bibliographic** — Shangshu Li et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol 7 · pp 1-10
- **DOI** — `10.1109/tqe.2026.3705783` · <https://doi.org/10.1109/tqe.2026.3705783>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — State-vector memory traffic: every gate application traverses the full state array.
- **Gate 2 (HPC/systems technique)** — Dependency-graph (DAG) aware gate fusion that reduces the number of full-array traversals.
- **Gate 3 (future CPU/GPU/QPU relevance)** — A kernel-level memory-bandwidth optimization for the most widely used classical quantum-simulation workload.
- **Quantum problem** — Exact state-vector simulation of quantum circuits for development and validation.
- **Classical / HPC problem** — Memory-bandwidth-bound execution: every gate application traverses the full state vector, so fusing gates into larger operators reduces traversals; choosing which gates may legally fuse is a dependency-graph problem.
- **Mechanism** — A directed-acyclic-graph-aware fusion method that builds fused operators directly from circuit dependencies, exposing fusion opportunities that linear-order heuristics miss.
- **Computational bottleneck** — State-vector memory traffic (number of full-array traversals); fused-operator size versus reuse trade-off.
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — Simulation runtime improvement versus existing heuristic/linear-order fusion; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).
- **Major claim (with baseline)** — DAG-aware fusion finds larger legal fused operators than linear-order heuristics and reduces state-vector traversal cost in exact simulation.
- **Limitation** — Larger fused operators cost more to construct and apply densely; benefit is circuit-structure dependent.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TQE-238` Network-Based Quantum Computing: An Efficient Design Framework for Many-Small-Node Distributed Fault-Tolerant Quantum Computing

- **Bibliographic** — Soshun Naito et al. · IEEE Trans. Quantum Engineering 2689-1808 · census year **2026** · vol 7 · pp 3104632-3104632
- **DOI** — `10.1109/tqe.2026.3722428` · <https://doi.org/10.1109/tqe.2026.3722428>
- **arXiv** — `2601.09374`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `FUTURE_WORKLOAD`, `HPC_FOR_Q` · **Branch** — `multi_qpu_distributed_qc`, `architecture_control`
- **Gate 1 (classical systems problem)** — Inter-node communication requirements and per-node logical-qubit capacity in a scale-out machine.
- **Gate 2 (HPC/systems technique)** — A distributed-system design framework specifying how logical computation is decomposed across many small nodes.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Addresses the scale-out organization of quantum computers, the direct analogue of cluster design in HPC.
- **Quantum problem** — A logical qubit consumes many physical qubits, so a single node may hold very few logical qubits, forcing computation across many small nodes.
- **Classical / HPC problem** — Distributed system design: partitioning logical computation across many small nodes, and the resulting inter-node communication and orchestration requirements.
- **Mechanism** — Network-based quantum computing (NBQC), a design framework for realizing distributed fault-tolerant computation on many small nodes, specifying how logical operations are decomposed across the node network.
- **Computational bottleneck** — Inter-node entanglement/communication requirements; per-node logical-qubit capacity.
- **Evaluation platform / scale** — Design-framework analysis. / Many small nodes each holding one or a few logical qubits.
- **Performance metrics** — Resource and communication requirements of the proposed design; numeric values not recoverable from the truncated abstract.
- **Major claim (with baseline)** — A design framework tailored to one-or-few-logical-qubit nodes makes many-small-node distributed fault-tolerant computing tractable, a regime prior distributed designs did not target.
- **Limitation** — Framework-level; no implementation or runtime evaluation reported in the abstract.
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3

### TQC — ACM Trans. Quantum Computing (20 papers)

#### `TQC-009` Revisiting the Mapping of Quantum Circuits: Entering the Multi-core Era

- **Bibliographic** — Pau Escofet et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 6, iss 1 , issue date 2025-3-31 · pp 1-26
- **DOI** — `10.1145/3655029` · <https://doi.org/10.1145/3655029>
- **arXiv** — `2403.17205`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Inter-core communication volume and execution time when a circuit is partitioned across the cores of a modular quantum processor; mapping is posed as an assignment problem whose cost is communication.
- **Gate 2 (HPC/systems technique)** — Hungarian-algorithm-based qubit-to-core assignment (HQA) plus derived theoretical bounds on non-local communication for random circuits; comparative evaluation against state-of-the-art multi-core mappers.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Supplies a communication-cost model and mapping policy for modular/multi-core QPUs, the interconnect layer any HPC-hosted multi-QPU system will need.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Inter-core communication volume and execution time when a circuit is partitioned across the cores of a modular quantum processor; mapping is posed as an assignment problem whose cost is communication.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Simulation/benchmark circuit suite over multi-core architecture models; INSUFFICIENT_EVIDENCE on specific hardware. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — 4.9x improvement in execution time and 1.6x in non-local communications against the best competing multi-core mapping algorithm (preprint arXiv:2403.17205); comparator is the best prior multi-core mapper, not a single-core baseline.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Appears in the v6 special issue tied to TQC-035 (classical computer engineering). Central multi-core mapping reference for this corpus.

#### `TQC-019` MQT Predictor: Automatic Device Selection with Device-Specific Circuit Compilation for Quantum Computing

- **Bibliographic** — Nils Quetschlich et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 6, iss 1 , issue date 2025-3-31 · pp 1-26
- **DOI** — `10.1145/3673241` · <https://doi.org/10.1145/3673241>
- **arXiv** — `2310.06889`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Choosing a device and a compilation pipeline from a combinatorially growing space of devices, compilers and passes; tool-selection and compilation-flow automation.
- **Gate 2 (HPC/systems technique)** — Learning-based automatic device selection with device-specific compiler construction that mixes passes from several toolchains into one optimized flow (MQT Predictor).
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly addresses the software-stack layer that a heterogeneous CPU/GPU/QPU site would need to route a job to an appropriate backend.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Choosing a device and a compilation pipeline from a combinatorially growing space of devices, compilers and passes; tool-selection and compilation-flow automation.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — MQT Bench circuits over multiple device models; Python/MQT toolchain. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims automated selection plus device-specific compilation outperforming individual off-the-shelf compilers on a figure-of-merit combining expected fidelity and cost; baseline = standard Qiskit/TKET default flows.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — PUBLIC_CODE · https://github.com/cda-tum/mqt-predictor
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Part of the Munich Quantum Toolkit family; a stable, maintained artifact makes it a good reproducibility anchor.

#### `TQC-021` ARQUIN: Architectures for Multinode Superconducting Quantum Computers

- **Bibliographic** — James Ang et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 5, iss 3 , issue date 2024-9-30 · pp 1-59
- **DOI** — `10.1145/3674151` · <https://doi.org/10.1145/3674151>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `architecture_control`, `benchmarking_performance_modeling`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — End-to-end performance of a multinode quantum computer where internode links are two to three orders of magnitude slower and noisier than local gates: interconnect latency, entanglement-distillation overhead, and compiler-level placement across nodes.
- **Gate 2 (HPC/systems technique)** — Full-stack co-design study with a multi-level simulation framework spanning device, network, compiler and application layers; systematic design-space exploration of node-count, link-rate and distillation choices.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Sets out the architectural taxonomy and performance ceilings for multinode QPUs, the structure an HPC centre would integrate as a single logical accelerator.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — End-to-end performance of a multinode quantum computer where internode links are two to three orders of magnitude slower and noisier than local gates: interconnect latency, entanglement-distillation overhead, and compiler-level placement across nodes.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Multi-level simulation stack for superconducting nodes with optical interconnects. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reports achievable performance regimes for early multinode machines and a co-design roadmap balancing entanglement generation, distillation and local architecture; qualitative roadmap rather than a single speedup number, so BASELINE_UNCLEAR for any headline figure.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Large multi-institution (DOE labs, IBM, academia) study; functions as an architecture reference and a citation hub for multinode QC. Tag BIBLIOGRAPHY_HUB-like even though it is original research.

#### `TQC-022` Optimization Applications as Quantum Performance Benchmarks

- **Bibliographic** — Thomas Lubinski et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 5, iss 3 , issue date 2024-9-30 · pp 1-44
- **DOI** — `10.1145/3678184` · <https://doi.org/10.1145/3678184>
- **arXiv** — `2302.02278`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Measuring run-time execution performance against solution quality for optimization workloads on quantum devices, so that time-to-solution can be compared across gate-model and annealing backends.
- **Gate 2 (HPC/systems technique)** — Application-oriented benchmarking framework with a run-time/quality trade-off methodology adapted from classical optimization-algorithm characterization.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Provides a time-to-solution measurement methodology usable when a QPU is one backend among several in a heterogeneous facility.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Measuring run-time execution performance against solution quality for optimization workloads on quantum devices, so that time-to-solution can be compared across gate-model and annealing backends.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Gate-model quantum devices and a quantum annealing device; QED-C benchmark suite lineage. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Characterizes Max-Cut solution quality versus execution time on gate-model devices and an annealer; comparisons are across devices/algorithms rather than against a classical solver baseline, so classical-advantage claims are BASELINE_UNCLEAR.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — PARTIAL · https://github.com/SRI-International/QC-App-Oriented-Benchmarks
- **Conference extension** — RELATED_LINEAGE
- **Deep-dive priority** — 3
- **Notes** — Artifact URL is the known QED-C benchmark repository associated with this author group; treat repo linkage as PARTIAL since the article-specific artifact was not verified. KEPT INCLUDED against the verification pass. Rebuttal: the contribution is not an application accuracy comparison. CRITERIA lists 'quantum performance modeling' as an INCLUDE shape and 'benchmarking_performance_modeling' as a branch, and this paper's stated object is a framework evaluating the trade-off between run-time execution performance and solution quality. Run-time execution performance is wall-clock time, a classical cost quantity, not a quantum resource, so the rule invoked for TQC-066 and TQC-016 does not apply here. The verifier's point that comparisons run across devices and algorithms rather than against a classical solver is a baseline-completeness limitation, already recorded in key_claim_with_baseline, and it bounds what may be concluded about quantum advantage; it does not remove the run-time axis that carries Gate 1 and Gate 2. Excluding it would also be inconsistent with keeping TQC-064 and TQC-072, which are likewise comparative performance studies with internal baselines.

#### `TQC-025` Robust Qubit Mapping Algorithm via Double-Source Optimal Routing on Large Quantum Circuits

- **Bibliographic** — Chin-Yi Cheng et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 5, iss 3 , issue date 2024-9-30 · pp 1-26
- **DOI** — `10.1145/3680291` · <https://doi.org/10.1145/3680291>
- **arXiv** — `2210.01306`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Mapping and routing algorithms failing to scale to circuits with hundreds of qubits; compile-time cost and scheduling of SWAP insertion on large circuits.
- **Gate 2 (HPC/systems technique)** — Duostra: double-source optimal routing for two-qubit gates plus two heuristic schedulers (limitedly exhaustive search and a greedy variant) designed to keep compile time tractable at large circuit sizes.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Compilation scalability is a classical-compute bottleneck in any QPU job pipeline; this quantifies the routing-stage cost at scale.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Mapping and routing algorithms failing to scale to circuits with hundreds of qubits; compile-time cost and scheduling of SWAP insertion on large circuits.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Large benchmark circuits on real-device coupling maps; C++ implementation. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reports improved mapping quality on large circuits versus established routers (SABRE-class heuristics) while remaining tractable; exact figures not in the abstract, so the headline is recorded as BASELINE = prior heuristic mappers.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Explicit classical-scalability framing is what separates this from the gate-count-only mapping papers in the same volume.

#### `TQC-029` Realistic Cost to Execute Practical Quantum Circuits using Direct Clifford+T Lattice Surgery Compilation

- **Bibliographic** — Tyler Leblond et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 5, iss 4 , issue date 2024-12-31 · pp 1-28
- **DOI** — `10.1145/3689826` · <https://doi.org/10.1145/3689826>
- **arXiv** — `2311.10686`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `compiler_mapping_routing`, `qec_classical_processing`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Resource estimation for fault-tolerant execution: magic-state request cadence, distillation throughput, storage sizing, and allocation of lattice-surgery operations to hardware tiles.
- **Gate 2 (HPC/systems technique)** — Two-stage compilation pipeline (logical gates to layout-independent instructions, then to local lattice-surgery instructions with tile allocation) with post-hoc scheduling analysis of magic-state supply and demand.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Quantifies the classical control and resource-management burden of fault-tolerant execution, which determines the size of the classical side of a future HPC-QPU system.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Resource estimation for fault-tolerant execution: magic-state request cadence, distillation throughput, storage sizing, and allocation of lattice-surgery operations to hardware tiles.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Extension of the open-source Lattice Surgery Compiler; benchmark logical circuits. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Produces realistic space-time cost estimates for practical circuits under direct Clifford+T lattice-surgery compilation; improvement is over prior coarse resource-estimation pipelines, not a runtime speedup.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — PARTIAL · https://github.com/latticesurgery-com/lattice-surgery-compiler
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — ORNL-affiliated; bridges compiler work and QEC resource accounting.

#### `TQC-030` Efficient Quantum Circuit Simulation by Tensor Network Methods on Modern GPUs

- **Bibliographic** — Feng Pan et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2024** · vol 5, iss 4 , issue date 2024-12-31 · pp 1-26
- **DOI** — `10.1145/3696465` · <https://doi.org/10.1145/3696465>
- **arXiv** — `2310.03978`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Contraction-path search cost and GPU execution efficiency for tensor-network simulation of large circuits, where state-vector simulation exceeds memory.
- **Gate 2 (HPC/systems technique)** — Conversion of Einstein-summation contractions into GEMM calls to use tensor cores, mixed-precision arithmetic, and contraction-path optimization on modern GPUs.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly a GPU-HPC kernel-engineering contribution serving quantum circuit verification; the archetype of HPC_FOR_Q in this corpus.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Contraction-path search cost and GPU execution efficiency for tensor-network simulation of large circuits, where state-vector simulation exceeds memory.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — NVIDIA A100 GPU; Sycamore random circuit sampling verification workloads. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Sustained >21 TFLOPS on an NVIDIA A100; 3.96x reduction in verification time for 18-cycle Sycamore circuits; 12.5x over state-of-the-art CPU approaches and 4.48x-6.78x over existing GPU methods reported in the literature (preprint arXiv:2310.03978).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Headline figures come from the preprint; the published abstract does not restate them.

#### `TQC-037` Forward and Backward Constrained Bisimulations for Quantum Circuits Using Decision Diagrams

- **Bibliographic** — Lukas Burgholzer et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2025** · vol 6, iss 2 , issue date 2025-6-30 · pp 1-21
- **DOI** — `10.1145/3712711` · <https://doi.org/10.1145/3712711>
- **arXiv** — `2308.09510`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Exponential growth of state representation with qubit count in classical simulation; reducing the size of the represented model while preserving the quantities of interest.
- **Gate 2 (HPC/systems technique)** — Forward and backward constrained bisimulation (lumping) applied over decision-diagram representations, a state-space-reduction technique carried over from Markov-chain and ODE model reduction.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Improves the memory/compute envelope of classical simulators, the workhorse of quantum software development on HPC resources.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Exponential growth of state representation with qubit count in classical simulation; reducing the size of the represented model while preserving the quantities of interest.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Decision-diagram simulator (MQT lineage); benchmark circuit families. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reports reductions in represented state dimension and simulation effort versus unreduced decision-diagram simulation; quantitative factors not in the abstract, BASELINE = plain DD-based simulation.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Burgholzer is an MQT author; likely tooling overlap with MQT DDSIM but not verified.

#### `TQC-051` Lazy Qubit Reordering for Accelerating Parallel State-Vector-based Quantum Circuit Simulation

- **Bibliographic** — Yusuke Teranishi et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2025** · vol 6, iss 4 , issue date 2025-12-31 · pp 1-33
- **DOI** — `10.1145/3748261` · <https://doi.org/10.1145/3748261>
- **arXiv** — `2410.04252`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — All-to-all communication generated by qubit reordering dominates the cost of multi-GPU state-vector simulation; the problem is communication aggregation and scheduling, not quantum physics.
- **Gate 2 (HPC/systems technique)** — Two operation-scheduling methods: an out-of-order approach that delays and aggregates reordering communications, and a time-space-tiling (cache-blocking) arrangement of gate execution order; plus a cluster-topology-aware optimization.
- **Gate 3 (future CPU/GPU/QPU relevance)** — A direct transfer of classical cache-blocking and communication-aggregation technique into the quantum simulation kernel; exemplary HPC_FOR_Q work.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — All-to-all communication generated by qubit reordering dominates the cost of multi-GPU state-vector simulation; the problem is communication aggregation and scheduling, not quantum physics.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — 32-GPU multi-node execution; VQE-oriented simulation workloads. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Up to 54x for quantum state update and up to 606x for expectation-value computation over existing methods, on 32-GPU executions; up to 15% communication reduction in two-layered cluster systems (preprint arXiv:2410.04252). Baseline is stated as 'existing methods' and is not fully specified, so the 606x figure should be treated as BASELINE_UNCLEAR.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — One of the clearest pure-HPC contributions in the TQC population.

#### `TQC-054` DQC-QR: Distributing and Routing Quantum Circuits with Minimum Execution Time

- **Bibliographic** — Ranjani Sundaram et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2025** · vol 6, iss 4 , issue date 2025-12-31 · pp 1-26
- **DOI** — `10.1145/3757069` · <https://doi.org/10.1145/3757069>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Minimizing wall-clock execution time of a circuit distributed over a network of QPUs, where entanglement generation latency competes with qubit decoherence; joint qubit-to-memory mapping and remote-gate routing.
- **Gate 2 (HPC/systems technique)** — Formulation and algorithms for the combined mapping/routing/scheduling problem with execution time as the objective, treating entanglement links as a latency-bounded interconnect resource.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Models a multi-QPU system as a latency-constrained distributed machine, which is the form a multi-node quantum resource in an HPC centre would take.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Minimizing wall-clock execution time of a circuit distributed over a network of QPUs, where entanglement generation latency competes with qubit decoherence; joint qubit-to-memory mapping and remote-gate routing.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Quantum network simulation over benchmark circuits; INSUFFICIENT_EVIDENCE on scale. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims lower execution time than prior distribution schemes; specific factors not in the abstract, BASELINE = prior circuit-distribution/partitioning heuristics.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Distinguishable from the excluded entanglement-routing papers (e.g. TQC-080) because the objective is circuit execution time, not network key/entanglement distribution.

#### `TQC-064` Comparative Benchmarking of Utility-Scale Quantum Emulators

- **Bibliographic** — Anna Leonteva et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2025** · vol 7, iss 2 , issue date 2026-6-30 · pp 1-29
- **DOI** — `10.1145/3776567` · <https://doi.org/10.1145/3776567>
- **arXiv** — `2504.14027`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `benchmarking_performance_modeling`, `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Which classical emulator technology can carry utility-scale circuits (100 to 1024 qubits) within practical CPU time and memory, and where each method fails.
- **Gate 2 (HPC/systems technique)** — Controlled cross-emulator benchmarking of seven simulators spanning tensor networks, MPS, decision diagrams and factorized-ket representations, on CPU hardware, across 13 MQTBench circuits and sizes 4 to 1024 qubits.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Gives an empirical capability envelope for the classical side of quantum workflows; directly usable for provisioning simulation capacity at an HPC site.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Which classical emulator technology can carry utility-scale circuits (100 to 1024 qubits) within practical CPU time and memory, and where each method fails.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — CPU-based hardware; 13 MQTBench circuits, 4 to 1024 qubits; seven emulators. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — MPS-based emulators outperform the other approaches overall, solving 8 of 13 benchmarks up to 1024 qubits; comparison is emulator-versus-emulator on identical circuits and CPU hardware, which is a clean baseline.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Rare head-to-head simulator study in this venue; a good empirical counterweight to the survey TQC-057.

#### `TQC-070` Fast Algorithms and Implementations for Computing the Minimum Distance of Quantum Codes

- **Bibliographic** — Fernando Hernando et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol 7, iss 2 , issue date 2026-6-30 · pp 1-19
- **DOI** — `10.1145/3795877` · <https://doi.org/10.1145/3795877>
- **arXiv** — `2408.10743`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `qec_classical_processing`
- **Gate 1 (classical systems problem)** — Computing the symplectic minimum distance of a stabilizer code is an expensive classical combinatorial computation; the bottleneck is single-node and shared-memory compute time.
- **Gate 2 (HPC/systems technique)** — Three algorithms derived from Brouwer-Zimmermann with implementations for single-core, multicore and shared-memory multiprocessor execution, with a scaling study.
- **Gate 3 (future CPU/GPU/QPU relevance)** — A classical parallel-computing contribution whose consumer is QEC code design; a clean instance of HPC serving the quantum stack outside of simulation.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Computing the symplectic minimum distance of a stabilizer code is an expensive classical combinatorial computation; the bottleneck is single-node and shared-memory compute time.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Single-core, multicore and shared-memory multiprocessor systems. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reports more than one order of magnitude faster time than current state-of-the-art licensed implementations (Magma/GAP-class commercial tools) in the most computationally demanding cases, on single-core, multicore and shared-memory multiprocessors.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — The most conventionally HPC paper in the TQC population by method (parallel combinatorial search, speedup versus licensed tools).

#### `TQC-072` Benchmarking fault-tolerant quantum computing hardware via QLOPS

- **Bibliographic** — Linghang Kong et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol 7, iss 2 , issue date 2026-6-30 · pp 1-14
- **DOI** — `10.1145/3797968` · <https://doi.org/10.1145/3797968>
- **arXiv** — `2507.12024`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `FUTURE_WORKLOAD`, `HPC_FOR_Q` · **Branch** — `benchmarking_performance_modeling`, `qec_classical_processing`
- **Gate 1 (classical systems problem)** — No common framework exists for comparing fault-tolerant schemes across hardware platforms in throughput terms; QLOPS casts the question as logical operations per second, i.e. a rate metric.
- **Gate 2 (HPC/systems technique)** — Definition and application of a throughput metric (Quantum Logical Operations Per Second) plus an evaluation framework that folds code distance, cycle time and resource overhead into a single performance figure.
- **Gate 3 (future CPU/GPU/QPU relevance)** — A throughput metric is the language an HPC centre uses to size and schedule a resource; this makes FTQC schemes comparable in those terms.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — No common framework exists for comparing fault-tolerant schemes across hardware platforms in throughput terms; QLOPS casts the question as logical operations per second, i.e. a rate metric.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Analytical/resource-model evaluation across platform parameter sets. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Proposes QLOPS and applies it across FTQC schemes and hardware platforms; comparisons are between schemes under the new metric, so there is no external baseline.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Performance-modelling inclusion; useful for the FUTURE_WORKLOAD scenario.

#### `TQC-074` QFOR: A Fidelity-aware Orchestrator for Quantum Computing Environments using Deep Reinforcement Learning

- **Bibliographic** — Hoa Nguyen et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3799898` · <https://doi.org/10.1145/3799898>
- **arXiv** — `2508.04974`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `HPC_FOR_Q` · **Branch** — `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Allocating and scheduling quantum tasks across heterogeneous, noisy quantum nodes in a cloud/datacentre setting, balancing execution fidelity against completion time under dynamic conditions.
- **Gate 2 (HPC/systems technique)** — The orchestration problem is modelled as a Markov Decision Process and solved with Proximal Policy Optimisation; a learned scheduler replacing static heuristics.
- **Gate 3 (future CPU/GPU/QPU relevance)** — This is resource management for a pool of QPUs, the layer an HPC batch system would either absorb or interface with.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Allocating and scheduling quantum tasks across heterogeneous, noisy quantum nodes in a cloud/datacentre setting, balancing execution fidelity against completion time under dynamic conditions.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Simulated quantum cloud environment with heterogeneous backend calibration data; INSUFFICIENT_EVIDENCE on real-device deployment. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — 29.5% to 84% improvement in relative fidelity performance over heuristic baselines while maintaining comparable execution times (preprint arXiv:2508.04974). Baseline = heuristic schedulers; the range is wide and workload-dependent.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — ACM Just Accepted (no volume/issue). One of very few genuine scheduling/resource-management papers in the TQC population.

#### `TQC-082` Tracking Affine Subspace with Gaussian Elimination for Adaptive Quantum Circuit Simulation

- **Bibliographic** — Kisung Jin et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol 7, iss 4 , issue date 2026-12-31 · pp 1-22
- **DOI** — `10.1145/3815191` · <https://doi.org/10.1145/3815191>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Sparse simulators win on memory when few basis states carry amplitude but lose on dense states; the systems problem is choosing a representation adaptively to control memory and runtime.
- **Gate 2 (HPC/systems technique)** — Rapid pre-simulation sparsity prediction plus Gaussian elimination on linear constraints to track an affine subspace, switching representation adaptively.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Representation-adaptive simulation is a memory-management technique for the classical simulation service in a quantum software stack.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Sparse simulators win on memory when few basis states carry amplitude but lose on dense states; the systems problem is choosing a representation adaptively to control memory and runtime.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Benchmark circuit suite on CPU; INSUFFICIENT_EVIDENCE on scale. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims retained sparse-simulator efficiency on sparse circuits without the degradation on dense circuits; BASELINE = fixed sparse and fixed state-vector simulators.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Simulation-engine inclusion; single-node, memory-focused.

#### `TQC-089` TREV: Python Library for Efficient Implementations of Variational Quantum Algorithms for Optimization using Tensor Networks

- **Bibliographic** — Keun Jun Park et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3821430` · <https://doi.org/10.1145/3821430>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `distributed_gpu_simulation`, `hybrid_workflow`
- **Gate 1 (classical systems problem)** — Gradient evaluation by the parameter-shift rule dominates VQA simulation runtime, scaling with both parameter count and Hamiltonian term count; the cost is repeated classical contraction and sampling.
- **Gate 2 (HPC/systems technique)** — TREV amortizes contraction and sampling across batched parameter-shift evaluations inside a tensor-ring state representation, i.e. batching and work reuse applied to the classical inner loop.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Targets the classical bottleneck of the hybrid loop, which is where CPU/GPU time is actually consumed in variational workloads.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Gradient evaluation by the parameter-shift rule dominates VQA simulation runtime, scaling with both parameter count and Hamiltonian term count; the cost is repeated classical contraction and sampling.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Python library; tensor-ring simulation of VQA circuits. INSUFFICIENT_EVIDENCE on hardware. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims reduced VQA simulation runtime through batched parameter evaluation; quantitative factors not in the abstract, BASELINE = per-parameter sequential parameter-shift simulation.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Included on the runtime-cost route despite the VQA subject matter: the contribution is the classical evaluation engine, not the ansatz or optimizer.

#### `TQC-091` Efficient Compilation for Shuttling Trapped-Ion Machines via the Position Graph Architectural Abstraction

- **Bibliographic** — Bao Bach et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol 7, iss 4 , issue date 2026-12-31 · pp 1-33
- **DOI** — `10.1145/3831246` · <https://doi.org/10.1145/3831246>
- **arXiv** — `2501.12470`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `architecture_control`
- **Gate 1 (classical systems problem)** — Compilation for shuttling trapped-ion (QCCD) machines, where ion transport and trap-region occupancy dominate; scalable compilation across heterogeneous hardware layouts.
- **Gate 2 (HPC/systems technique)** — A 'position graph' hardware abstraction that unifies several architecture families, enabling one scalable compilation method rather than per-architecture bespoke compilers.
- **Gate 3 (future CPU/GPU/QPU relevance)** — An abstraction layer between compiler and hardware is exactly the portability mechanism a multi-vendor HPC-QPU software stack needs.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Compilation for shuttling trapped-ion (QCCD) machines, where ion transport and trap-region occupancy dominate; scalable compilation across heterogeneous hardware layouts.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Benchmark circuits over modelled QCCD architectures. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims higher-quality and scalable compilation for QCCD architectures versus existing trapped-ion compilation strategies; figures not in the abstract, BASELINE = prior QCCD compilers.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Architecture-abstraction angle makes this stronger than a pure routing heuristic.

#### `TQC-092` FlatDD: Parallel Quantum Circuit Simulation using Decision Diagram and Flat Array

- **Bibliographic** — Shui Jiang et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3833216` · <https://doi.org/10.1145/3833216>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Decision-diagram simulation is memory-efficient on regular circuits but incurs large runtime and memory overhead on irregular ones; pointer-chasing DD structures also parallelize poorly.
- **Gate 2 (HPC/systems technique)** — FlatDD combines DD compression with a flat-array layout (data-layout transformation for locality) and parallelizes the simulation workload, a classical memory-layout plus parallelism contribution.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Improves the throughput and memory behaviour of a widely used simulator class; directly a classical-performance engineering result.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Decision-diagram simulation is memory-efficient on regular circuits but incurs large runtime and memory overhead on irregular ones; pointer-chasing DD structures also parallelize poorly.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Parallel CPU execution; INSUFFICIENT_EVIDENCE on thread/GPU counts. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims combined advantage of DD-based and array-based simulation with parallel speedup; quantitative factors not in the published abstract, BASELINE = DD-only and array-only simulators.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Data-layout and parallelism argument makes this one of the stronger simulation entries in the 2026 cohort.

#### `TQC-094` QASMTrans: An End-to-End QASM Compilation Framework with Pulse Generation for Near-Term Quantum Devices

- **Bibliographic** — Aaron Hoyt et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3837861` · <https://doi.org/10.1145/3837861>
- **arXiv** — `2602.05154`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `compiler_mapping_routing`, `architecture_control`, `hpc_qpu_integration`
- **Gate 1 (classical systems problem)** — Transpilation latency on the critical path of QPU testbed operation: just-in-time compilation must complete fast enough for closed-loop control on systems with tightly coupled FPGAs/CPUs.
- **Gate 2 (HPC/systems technique)** — A self-contained C++ compiler with no external dependencies, engineered for compile-time performance, plus end-to-end lowering to device pulses and direct integration with the QICK control framework.
- **Gate 3 (future CPU/GPU/QPU relevance)** — This is the clearest HPC-QPU integration artifact in the TQC population: classical compile latency, control-plane coupling and closed-loop operation in one pipeline.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Transpilation latency on the critical path of QPU testbed operation: just-in-time compilation must complete fast enough for closed-loop control on systems with tightly coupled FPGAs/CPUs.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — C++ implementation; QPU testbeds with integrated FPGAs/CPUs; QICK control integration. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Published abstract: more than 10x faster compilation than Qiskit on some circuits with similar circuit quality; the preprint states more than 100x on some circuits and up to 12% fidelity improvement from pulse-level optimization. BASELINE = Qiskit transpiler. The two figures differ, so record both and treat the magnitude as circuit-dependent.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — RELATED_LINEAGE
- **Deep-dive priority** — 5
- **Notes** — PNNL/ORNL authorship (Ang Li, Travis Humble). ACM Just Accepted.

#### `TQC-095` How Many Shots Are Enough for a Quantum Circuit?

- **Bibliographic** — Giuseppe Bisicchia et al. · ACM Trans. Quantum Computing 2643-6809 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3841468` · <https://doi.org/10.1145/3841468>
- **arXiv** — `2606.16965`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `quantum_runtime_orchestration`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Shot count is the unit of QPU resource consumption and cost; deciding online when to stop sampling is a runtime resource-allocation decision made without knowledge of the circuit or noise model.
- **Gate 2 (HPC/systems technique)** — IncrementalExecution, an online stopping framework driven by a diminishing-returns criterion on the estimated distribution, operating as a black-box runtime policy.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Shot budgeting is the throughput and cost knob for QPU access in a shared facility; a black-box policy is portable across backends.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Shot count is the unit of QPU resource consumption and cost; deciding online when to stop sampling is a runtime resource-allocation decision made without knowledge of the circuit or noise model.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Simulated and/or cloud backends; INSUFFICIENT_EVIDENCE on specifics. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims reduced shot consumption at a target accuracy versus fixed-shot execution; quantitative factors not in the abstract, BASELINE = fixed shot budgets.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Matches the shot/measurement-orchestration include shape in the criteria.

### TCAD — IEEE Trans. CAD of ICs and Systems (12 papers)

#### `TCAD-010` QuBEC: Boosting Equivalence Checking for Quantum Circuits With QEC Embedding

- **Bibliographic** — Chao Lu et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2024** · vol 43, iss 7 , issue date 2024-7 · pp 2037-2042
- **DOI** — `10.1109/tcad.2024.3361402` · <https://doi.org/10.1109/tcad.2024.3361402>
- **arXiv** — `2309.10728`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Classical verification runtime for quantum circuits; latency of equivalence checking is the reported metric.
- **Gate 2 (HPC/systems technique)** — Decision-diagram data structure engineering (QEC-aware embedding) to make the classical checker scale.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the cost of the classical verification stage in a quantum software stack.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Classical verification runtime for quantum circuits; latency of equivalence checking is the reported metric.
- **Mechanism** — QuBEC: decision-diagram-based equivalence checking that accounts for error-correction redundancy in circuits.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Up to 443x lower verification time on benchmark circuits; BASELINE = existing decision-diagram equivalence-checking techniques (as stated in the abstract).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — arXiv 2309.10728 preprint recorded in the dossier; conference lineage not confirmed from the article itself. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the evidence is the arXiv preprint 2309.10728 only; no conference version was verified.

#### `TCAD-014` QHLS: An HLS Framework to Convert High-Level Descriptions to Quantum Circuits

- **Bibliographic** — Chao Lu et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2024** · vol 43, iss 10 , issue date 2024-10 · pp 3015-3026
- **DOI** — `10.1109/tcad.2024.3391699` · <https://doi.org/10.1109/tcad.2024.3391699>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Programming scalability and automation: manual circuit construction is identified as not scaling and as requiring expert effort.
- **Gate 2 (HPC/systems technique)** — A high-level synthesis toolchain - a classical compiler front end that lowers high-level descriptions to circuits.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the software stack layer of a hybrid system (how applications reach a QPU).
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Programming scalability and automation: manual circuit construction is identified as not scaling and as requiring expert effort.
- **Mechanism** — QHLS: high-level-synthesis framework converting high-level descriptions into quantum circuits.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Automatic generation of circuits from high-level descriptions; quantitative compile-cost evidence not present in the abstract (BASELINE_UNCLEAR).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Included as a software-stack/toolchain contribution; the abstract carries no compile-time measurements, so the systems evidence is qualitative.

#### `TCAD-023` SmartQCache: Fast and Precise Pulse Control With Near-Quantum Cache Design on FPGA

- **Bibliographic** — Liqiang Lu et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2024** · vol 44, iss 5 , issue date 2025-5 · pp 1704-1716
- **DOI** — `10.1109/tcad.2024.3497839` · <https://doi.org/10.1109/tcad.2024.3497839>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `architecture_control`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Latency and computational cost of pulse synthesis; CPU-side synthesis is described as redundant and costly for large circuits, FPGA-side synthesis as inaccurate.
- **Gate 2 (HPC/systems technique)** — Near-quantum cache architecture on FPGA plus a CPU/FPGA work split - a classical memory-hierarchy design in the control path.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs the real-time classical control layer between a host and a QPU.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Latency and computational cost of pulse synthesis; CPU-side synthesis is described as redundant and costly for large circuits, FPGA-side synthesis as inaccurate.
- **Mechanism** — SmartQCache: near-quantum cache design on FPGA with combined compute-in-CPU and all-in-FPGA pulse synthesis for fast, precise pulse control.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Lower synthesis latency with maintained control precision; figures truncated (BASELINE = Qiskit Pulse CPU synthesis and QuMA-style FPGA synthesis).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Strongest control-plane record in TCAD; sits at the classical-hardware/QPU boundary.

#### `TCAD-024` Effective and Efficient Parallel Qubit Mapper

- **Bibliographic** — Hao Fu et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2024** · vol 44, iss 5 , issue date 2025-5 · pp 1774-1787
- **DOI** — `10.1109/tcad.2024.3500784` · <https://doi.org/10.1109/tcad.2024.3500784>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Mapping and routing is described as a time-consuming process; circuit depth and mapper runtime are both targets.
- **Gate 2 (HPC/systems technique)** — Parallel mapper design - explicitly an INCLUDE shape (parallel compiler) in CRITERIA.md.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs compilation throughput in a hybrid stack where compile time competes with device time.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Mapping and routing is described as a time-consuming process; circuit depth and mapper runtime are both targets.
- **Mechanism** — Parallel qubit mapper built on two extracted patterns from existing greedy mappers, targeting circuit depth at reduced mapping time.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Better depth at lower mapping time than compared greedy mappers; figures truncated (BASELINE = existing greedy mappers).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Clearest parallel-compilation record in the four journals.

#### `TCAD-027` Shuttling for Scalable Trapped-Ion Quantum Computers

- **Bibliographic** — Daniel Schoenberger et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2024** · vol 44, iss 6 , issue date 2025-6 · pp 2144-2155
- **DOI** — `10.1109/tcad.2024.3513262` · <https://doi.org/10.1109/tcad.2024.3513262>
- **arXiv** — `2402.14065`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `architecture_control`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Data movement and latency: ion shuttling time inside a QCCD device competes with coherence time.
- **Gate 2 (HPC/systems technique)** — Scheduling/ordering of physical qubit movement across zones in a modular architecture - a data-movement optimisation problem.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs modular/segmented QPU architectures and the movement costs that a compiler and runtime must manage.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Data movement and latency: ion shuttling time inside a QCCD device competes with coherence time.
- **Mechanism** — Shuttling schedules for QCCD trapped-ion architectures that reduce the time qubits spend being moved between memory and processing zones.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reduced shuttling time/overhead versus prior shuttling approaches; figures truncated (BASELINE = existing QCCD shuttling schedulers).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Modular-architecture data movement; the closest TCAD record to a memory-hierarchy problem.

#### `TCAD-030` DasAtom: A Divide-and-Shuttle Atom Approach to Quantum Circuit Transformation

- **Bibliographic** — Yunqi Huang et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 44, iss 8 , issue date 2025-8 · pp 2966-2978
- **DOI** — `10.1109/tcad.2025.3532818` · <https://doi.org/10.1109/tcad.2025.3532818>
- **arXiv** — `2409.03185`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `architecture_control`
- **Gate 1 (classical systems problem)** — Circuit partitioning plus physical movement of atoms - partition size and movement cost are the resource quantities.
- **Gate 2 (HPC/systems technique)** — Divide-and-shuttle compilation: partition the circuit into subcircuits, each with a mapping, and move qubits between partitions.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs architecture-aware compilation for a platform whose qubits are physically relocatable.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Circuit partitioning plus physical movement of atoms - partition size and movement cost are the resource quantities.
- **Mechanism** — DasAtom: divide-and-shuttle circuit transformation for neutral-atom devices exploiting long-range interaction and atom movement.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Better fidelity/transformation cost than compared neutral-atom compilers; figures truncated (BASELINE = existing NA compilation methods).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — arXiv 2409.03185 preprint confirmed to exist by search; no public code repository identified.

#### `TCAD-033` Circuit Partitioning and Transmission Cost Optimization in Distributed Quantum Circuits

- **Bibliographic** — Xinyu Chen et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 44, iss 9 , issue date 2025-9 · pp 3350-3362
- **DOI** — `10.1109/tcad.2025.3547812` · <https://doi.org/10.1109/tcad.2025.3547812>
- **arXiv** — `2407.05953`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Communication complexity: the number of quantum state transmissions between partitions is the optimised quantity.
- **Gate 2 (HPC/systems technique)** — QUBO-based circuit partitioning plus a lookahead method for transmission-cost optimisation.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs multi-QPU distributed execution and its interconnect cost.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Communication complexity: the number of quantum state transmissions between partitions is the optimised quantity.
- **Mechanism** — Circuit partitioning via a QUBO model with lookahead-based transmission-cost optimisation for distributed quantum circuits.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reduced transmission cost versus prior partitioning methods; figures truncated (BASELINE = existing DQC partitioning approaches).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Core multi-QPU communication record in TCAD.

#### `TCAD-043` Computational Performance Bounds Prediction in Quantum Computing With Unstable Noise

- **Bibliographic** — Jinyang Li et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 45, iss 2 , issue date 2026-2 · pp 969-982
- **DOI** — `10.1109/tcad.2025.3592605` · <https://doi.org/10.1109/tcad.2025.3592605>
- **arXiv** — `2507.17043`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `Q_IN_HPC`, `FUTURE_WORKLOAD` · **Branch** — `benchmarking_performance_modeling`, `qpu_scheduling_resource_mgmt`
- **Gate 1 (classical systems problem)** — Performance modelling and job scheduling: the abstract states that quantum-centric supercomputing needs noise characterisation to support system management such as job scheduling.
- **Gate 2 (HPC/systems technique)** — Predictive performance-bound modelling under unstable noise, framed as a system-management input.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs scheduling and job placement in a quantum-centric supercomputing centre.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Performance modelling and job scheduling: the abstract states that quantum-centric supercomputing needs noise characterisation to support system management such as job scheduling.
- **Mechanism** — Method for predicting computational performance bounds (fidelity) of quantum jobs on devices with unstable noise, aimed at supporting device selection and scheduling.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Prediction accuracy of performance bounds across devices/time; figures truncated (BASELINE = existing noise characterisation/fidelity prediction).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — The clearest Q_IN_HPC record in TCAD; explicitly frames itself against quantum-centric supercomputing system management.

#### `TCAD-050` DMapS: End-to-End Qubit Mapping and Routing for Distributed Quantum Computing Architectures

- **Bibliographic** — Tingyu Luo et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 45, iss 5 , issue date 2026-5 · pp 2095-2108
- **DOI** — `10.1109/tcad.2025.3611153` · <https://doi.org/10.1109/tcad.2025.3611153>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Remote communication cost between chips plus intra-chip execution cost; mapping is parallelised across chips.
- **Gate 2 (HPC/systems technique)** — End-to-end mapping and routing algorithms for DQC with a two-stage decomposition and parallel per-chip mapping.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs multi-chip/multi-QPU execution efficiency.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Remote communication cost between chips plus intra-chip execution cost; mapping is parallelised across chips.
- **Mechanism** — DMapS: end-to-end qubit mapping (DMapS-M) and routing for distributed quantum computing architectures, decomposing large circuits and parallelising mapping across chips.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Joint reduction of remote-communication and intra-chip execution cost; figures truncated (BASELINE = prior DQC mapping/routing).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Combines the multi-QPU and parallel-compilation limbs in one record.

#### `TCAD-051` Approximation Methods for Simulation and Equivalence Checking of Noisy Quantum Circuits

- **Bibliographic** — Mingyu Huang et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 45, iss 6 , issue date 2026-6 · pp 2679-2692
- **DOI** — `10.1109/tcad.2025.3623498` · <https://doi.org/10.1109/tcad.2025.3623498>
- **arXiv** — `2503.10340`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — State-space explosion and memory/compute cost of simulating and checking noisy circuits; scalability in qubit count is the stated limit.
- **Gate 2 (HPC/systems technique)** — Tensor-network representation with SVD-based approximation of noise tensors, implemented on Google's TensorNetwork library.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the classical simulation/verification workload that HPC resources must carry for quantum development.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — State-space explosion and memory/compute cost of simulating and checking noisy circuits; scalability in qubit count is the stated limit.
- **Mechanism** — Approximation algorithm using a tensor-network diagram plus SVD to simulate and equivalence-check noisy circuits at larger qubit counts under low noise.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Improved scalability versus exact noisy simulation/equivalence checking; figures truncated (BASELINE = exact density-matrix/decision-diagram methods).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Built on the TensorNetwork Python library; artifact status not verified.

#### `TCAD-057` A Framework for Dynamic Quantum Circuit Execution: Balancing Effectiveness and Efficiency

- **Bibliographic** — Fangzheng Chen et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2025** · vol 45, iss 6 , issue date 2026-6 · pp 2583-2596
- **DOI** — `10.1109/tcad.2025.3626447` · <https://doi.org/10.1109/tcad.2025.3626447>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`, `quantum_runtime_orchestration`
- **Gate 1 (classical systems problem)** — Runtime decision-making: controlled subcircuits are known only after mid-circuit measurement, so mapping/routing decisions must be made under a time budget; the paper frames the trade-off as effectiveness versus efficiency.
- **Gate 2 (HPC/systems technique)** — Execution framework for dynamic circuits spanning compilation and conditional control flow.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the real-time classical control-flow path between measurement and subsequent gate execution.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Runtime decision-making: controlled subcircuits are known only after mid-circuit measurement, so mapping/routing decisions must be made under a time budget; the paper frames the trade-off as effectiveness versus efficiency.
- **Mechanism** — Framework for executing dynamic quantum circuits with mid-circuit measurement and measurement-dependent controlled subcircuits, balancing routing quality against decision cost.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Trade-off between transformation quality and processing time; figures truncated (BASELINE = static mapping/routing applied to dynamic circuits).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Census year 2026 by online-first convention while the issue is 2026-6.

#### `TCAD-062` qfusion-opt: Profile-Informed Gate Scheduling and Fusion Optimization for Accelerating Quantum Circuit Simulation

- **Bibliographic** — Po-Hsuan Huang et al. · IEEE Trans. CAD of ICs and Systems 0278-0070 · census year **2026** · vol (Early Access) , issue date 2026 · pp 1-1
- **DOI** — `10.1109/tcad.2026.3680784` · <https://doi.org/10.1109/tcad.2026.3680784>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Simulation throughput: the title states the goal is accelerating quantum circuit simulation through gate scheduling and fusion.
- **Gate 2 (HPC/systems technique)** — Profile-informed scheduling plus gate fusion, i.e. classical performance optimisation of a simulator kernel.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs how simulation workloads are optimised on classical hardware.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Simulation throughput: the title states the goal is accelerating quantum circuit simulation through gate scheduling and fusion.
- **Mechanism** — qfusion-opt: profile-informed gate scheduling and fusion optimisation for quantum circuit simulation (title evidence only).
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — INSUFFICIENT_EVIDENCE (no abstract retrieved; IEEE and Semantic Scholar returned no abstract).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — NO_ABSTRACT, IEEE Early Access. The title alone settles all three gates (simulation acceleration via scheduling/fusion); target hardware (CPU vs GPU) and measured speedups require the full text.

### TC — IEEE Trans. Computers (6 papers)

#### `TC-004` A Mutual-Influence-Aware Heuristic Method for Quantum Circuit Mapping

- **Bibliographic** — Kui Ye et al. · IEEE Trans. Computers 0018-9340 · census year **2024** · vol 73, iss 12 , issue date 2024-12 · pp 2855-2867
- **DOI** — `10.1109/tc.2024.3441825` · <https://doi.org/10.1109/tc.2024.3441825>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Compilation/preprocessing cost: the stated trade-off is between inserted-gate count and the efficiency (runtime) of the mapping preprocessing stage.
- **Gate 2 (HPC/systems technique)** — Heuristic compiler design: initial-mapping search framework + generator + heuristic mapper, i.e. a classical compilation pipeline with an explicit cost budget.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the classical compilation stage of a CPU-plus-QPU stack, where mapping time is part of job turnaround.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Compilation/preprocessing cost: the stated trade-off is between inserted-gate count and the efficiency (runtime) of the mapping preprocessing stage.
- **Mechanism** — Mutual-influence-aware (MIA) heuristic qubit-mapping method combining an initial-mapping search framework, an initial-mapping generator and a heuristic circuit mapper.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Improved mapping quality and preprocessing efficiency; specific figures BASELINE_UNCLEAR from the abstract.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Included on the compilation-cost limb of Gate 1; the fidelity/gate-count limb alone would have been BORDERLINE.

#### `TC-011` Qu-Trefoil: Large-Scale Quantum Circuit Simulator Working on FPGA With SATA Storages

- **Bibliographic** — Kaijie Wei et al. · IEEE Trans. Computers 0018-9340 · census year **2024** · vol 74, iss 4 , issue date 2025-4 · pp 1306-1321
- **DOI** — `10.1109/tc.2024.3521546` · <https://doi.org/10.1109/tc.2024.3521546>
- **arXiv** — `2608.14285`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Memory capacity and data movement: 2^(n+4) bytes of state vector forces the design out of DRAM onto SATA storage; I/O bandwidth is the binding constraint.
- **Gate 2 (HPC/systems technique)** — Accelerator architecture for state-vector simulation: FPGA datapath plus a storage hierarchy spanning SATA SSDs.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs how large-scale simulation workloads can be served by non-CPU hardware and a deep memory hierarchy.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Memory capacity and data movement: 2^(n+4) bytes of state vector forces the design out of DRAM onto SATA storage; I/O bandwidth is the binding constraint.
- **Mechanism** — Qu-Trefoil: FPGA-based large-scale state-vector quantum circuit simulator using SATA-attached storage to extend simulable qubit count beyond memory capacity.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Extended qubit capacity relative to memory-resident simulation; numeric speedups and the comparison baseline are BASELINE_UNCLEAR from the truncated abstract.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — arXiv id recorded in the dossier as 2608.14285; not verified against the article.

#### `TC-023` AdaptDQC: Adaptive Distributed Quantum Computing With Quantitative Performance Analysis

- **Bibliographic** — Debin Xiang et al. · IEEE Trans. Computers 0018-9340 · census year **2025** · vol 74, iss 10 , issue date 2025-10 · pp 3277-3290
- **DOI** — `10.1109/tc.2025.3586027` · <https://doi.org/10.1109/tc.2025.3586027>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Inter-chip communication volume, partitioning cost and multi-objective performance metrics for distributed quantum computing.
- **Gate 2 (HPC/systems technique)** — Compiler framework with a spatial-temporal graph model of circuits and interconnect architectures; circuit partitioning and chip mapping under hybrid inter-chip-communication architectures.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly addresses multi-QPU/modular execution and its communication cost, a central question for heterogeneous systems.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Inter-chip communication volume, partitioning cost and multi-objective performance metrics for distributed quantum computing.
- **Mechanism** — AdaptDQC: adaptive DQC compiler that models circuits and inter-chip communication architectures in one spatial-temporal graph and optimises partitioning/mapping against configurable objectives.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reports average reductions in communication cost against state-of-the-art DQC compiler frameworks; exact percentages truncated in the dossier abstract (BASELINE = prior DQC compilers).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — One of the two architecture-level distributed-QC papers in TC; quantitative performance analysis of ICC architectures is the distinguishing feature.

#### `TC-030` SuperEncoder: Towards Efficient Neural Approximate Quantum State Preparation

- **Bibliographic** — Yilun Zhao et al. · IEEE Trans. Computers 0018-9340 · census year **2025** · vol 75, iss 3 , issue date 2026-3 · pp 916-927
- **DOI** — `10.1109/tc.2025.3644034` · <https://doi.org/10.1109/tc.2025.3644034>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Classical runtime: the iterative, state-by-state PQC optimisation for approximate state preparation is identified as substantial runtime overhead.
- **Gate 2 (HPC/systems technique)** — A trained neural encoder replaces the per-instance classical optimisation loop, i.e. amortising compilation cost across inputs.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs the cost of the classical side of the software stack when data must be loaded into a QPU repeatedly.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Classical runtime: the iterative, state-by-state PQC optimisation for approximate state preparation is identified as substantial runtime overhead.
- **Mechanism** — SuperEncoder: neural approximate quantum state preparation that generates PQC parameters without per-state iterative optimisation.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reduced state-preparation runtime versus iterative per-state PQC optimisation; magnitude BASELINE_UNCLEAR from the truncated abstract.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — Included on compilation-cost grounds; if the full text is dominated by fidelity comparisons this would move to BORDERLINE.

#### `TC-040` AMARETTO, Accelerating Quantum Algorithm Development With FPGA Emulation

- **Bibliographic** — Christian Conti et al. · IEEE Trans. Computers 0018-9340 · census year **2026** · vol 75, iss 10 , issue date 2026-10 · pp 3544-3555
- **DOI** — `10.1109/tc.2026.3710326` · <https://doi.org/10.1109/tc.2026.3710326>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Simulation time and memory: software simulators are described as time-consuming with exponentially growing memory demand.
- **Gate 2 (HPC/systems technique)** — FPGA hardware emulator as an alternative execution substrate for quantum circuit evaluation.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs accelerator-based offload of the quantum-simulation workload in a heterogeneous facility.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Simulation time and memory: software simulators are described as time-consuming with exponentially growing memory demand.
- **Mechanism** — AMARETTO: FPGA emulator for quantum algorithm development, targeting resource-constrained (low-tier) FPGAs.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Faster and more resource-efficient than software simulation; exact speedup and baseline simulator BASELINE_UNCLEAR from the truncated abstract.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 3
- **Notes** — A preprint with the same system name exists as arXiv 2411.09320 ('AMARETTO: Enabling Efficient Quantum Algorithm Emulation on Low-Tier FPGAs'); relationship to this TC article not confirmed from the article itself, hence RELATED_LINEAGE rather than CONFIRMED_EXTENSION. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the evidence is a same-name arXiv preprint (2411.09320), which is not a conference paper; no conference venue was verified.

#### `TC-041` Quantum at the Edge: Scalable Standalone FPGA Emulator for QAOA–based Weighted-MaxCut

- **Bibliographic** — Seonghyun Choi et al. · IEEE Trans. Computers 0018-9340 · census year **2026** · vol (Early Access) , issue date 2026 · pp 1-14
- **DOI** — `10.1109/tc.2026.3724836` · <https://doi.org/10.1109/tc.2026.3724836>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Scalability and standalone execution of an accelerator that emulates a quantum algorithm; title states scalability as the design goal.
- **Gate 2 (HPC/systems technique)** — FPGA emulator architecture for QAOA-based weighted MaxCut.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Informs edge/standalone accelerator substrates for quantum-algorithm workloads.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Scalability and standalone execution of an accelerator that emulates a quantum algorithm; title states scalability as the design goal.
- **Mechanism** — Standalone FPGA emulator for QAOA-based weighted MaxCut, presented as scalable and edge-deployable (title evidence only).
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — INSUFFICIENT_EVIDENCE (no abstract retrieved).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — NO_ABSTRACT. IEEE Early Access (no volume). Verdict rests on the title alone, which names an FPGA emulator and scalability; full text required to confirm the systems evaluation.

### TACO — ACM Trans. Architecture and Code Optimization (4 papers)

#### `TACO-001` QuCloud+: A Holistic Qubit Mapping Scheme for Single/Multi-programming on 2D/3D NISQ Quantum Computers

- **Bibliographic** — Lei Liu et al. · ACM Trans. Architecture and Code Optimization 1544-3566 · census year **2024** · vol 21, iss 1 , issue date 2024-3-31 · pp 1-27
- **DOI** — `10.1145/3631525` · <https://doi.org/10.1145/3631525>
- **arXiv** — `2207.14483`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Qubit-resource utilization on a shared quantum device: partitioning physical qubits between concurrently running programs, allocating regions under crosstalk constraints, and handling 2D and 3D chip topologies with one mechanism.
- **Gate 2 (HPC/systems technique)** — Multiprogramming resource partitioning by crosstalk-aware community detection, followed by topology-aware allocation and mapping. This is space-sharing of an accelerator, the same problem shape as multi-tenant GPU partitioning.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Device utilization and throughput under multi-tenancy is exactly the resource-management question an HPC centre faces when a QPU becomes a shared resource.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Qubit-resource utilization on a shared quantum device: partitioning physical qubits between concurrently running programs, allocating regions under crosstalk constraints, and handling 2D and 3D chip topologies with one mechanism.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Simulation plus IBM device coupling maps with 2D and 3D topologies. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims improved fidelity and qubit-resource utilization for single and multi-programming workloads versus prior mapping schemes; BASELINE = existing qubit mapping and multi-programming schemes, including the authors' earlier QuCloud.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — RELATED_LINEAGE
- **Deep-dive priority** — 5
- **Notes** — The strongest multi-tenancy/resource-management paper across both journals.

#### `TACO-006` LarQucut: A New Cutting and Mapping Approach for Large-sized Quantum Circuits in Distributed Quantum Computing (DQC) Environments

- **Bibliographic** — Xinglei Dou et al. · ACM Trans. Architecture and Code Optimization 1544-3566 · census year **2025** · vol 22, iss 3 , issue date 2025-9-30 · pp 1-24
- **DOI** — `10.1145/3730585` · <https://doi.org/10.1145/3730585>
- **arXiv** — `2502.21000`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Branch** — `circuit_cutting_reconstruction`, `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Cutting and mapping a circuit that exceeds any single QPU across a set of heterogeneous QPUs, where the number of cuts drives classical reconstruction cost and the mapping drives communication overhead.
- **Gate 2 (HPC/systems technique)** — Cutting strategy that reduces cut count and deliberately avoids fully independent sub-circuits, plus isomorphic sub-circuit detection so that mapping work is reused across identical fragments - a classical work-reuse and partitioning contribution.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Circuit cutting is the mechanism by which a large workload is decomposed across a pool of smaller accelerators; the cost model is classical reconstruction plus inter-QPU communication.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Cutting and mapping a circuit that exceeds any single QPU across a set of heterogeneous QPUs, where the number of cuts drives classical reconstruction cost and the mapping drives communication overhead.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Simulated DQC environment with heterogeneous QPUs; preprint arXiv:2502.21000. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims fewer cuts and lower overall cutting plus computing overhead than prior cutting approaches, with better mapping for diverse QPUs; BASELINE = existing circuit-cutting and DQC mapping methods.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5

#### `TACO-007` Ecmas+: Efficient Circuit Mapping and Scheduling for Surface Code Encoded Circuit on Quantum Cloud Platform

- **Bibliographic** — Mingzheng Zhu et al. · ACM Trans. Architecture and Code Optimization 1544-3566 · census year **2025** · vol 22, iss 3 , issue date 2025-9-30 · pp 1-25
- **DOI** — `10.1145/3760783` · <https://doi.org/10.1145/3760783>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC` · **Branch** — `compiler_mapping_routing`, `qpu_scheduling_resource_mgmt`, `qec_classical_processing`
- **Gate 1 (classical systems problem)** — Space-time cost of executing surface-code-encoded circuits determines the throughput of a shared quantum cloud platform; circuits differ in how much chip parallelism they can exploit, so the compiler must decide how much space to spend to buy time.
- **Gate 2 (HPC/systems technique)** — A Circuit Parallelism Degree metric characterizing exploitable parallelism, used to drive joint mapping and scheduling of surface-code operations with an explicit space-time trade-off and platform-throughput objective.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Framing compilation as a throughput problem for a shared platform is precisely the systems framing this census tracks.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Space-time cost of executing surface-code-encoded circuits determines the throughput of a shared quantum cloud platform; circuits differ in how much chip parallelism they can exploit, so the compiler must decide how much space to spend to buy time.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Surface-code compilation experiments over benchmark circuits and chip models. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Claims reduced space-time cost and higher platform throughput relative to prior surface-code compilation; BASELINE = existing surface-code mapping and scheduling approaches.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — RELATED_LINEAGE
- **Deep-dive priority** — 5
- **Notes** — The only paper across both journals that ties QEC compilation directly to platform throughput.

#### `TACO-009` A System Architecture for Low Latency Multiprogramming Quantum Computing

- **Bibliographic** — Yilun Zhao et al. · ACM Trans. Architecture and Code Optimization 1544-3566 · census year **2026** · vol (Early Access) · pp n/a
- **DOI** — `10.1145/3845611` · <https://doi.org/10.1145/3845611>
- **arXiv** — `2601.01158`
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q`, `Q_IN_HPC`, `FUTURE_WORKLOAD` · **Branch** — `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`, `compiler_mapping_routing`
- **Gate 1 (classical systems problem)** — Online compilation dominates the runtime of multiprogramming quantum systems because executables are device- and region-dependent, which blocks low-latency repeated invocation of quantum services.
- **Gate 2 (HPC/systems technique)** — FLAMENCO moves compilation offline and keeps multiple pre-compiled versions per program: the device is abstracted into compute units, diverse executable versions are generated ahead of time for different qubit regions, and a runtime orchestrator selects among them using fidelity metrics. This is classical multi-versioning plus runtime dispatch, a standard systems pattern.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Separating a slow offline compile from a fast online dispatch is how accelerator services are built in classical systems; this is the clearest transfer of that pattern into QPU serving.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Online compilation dominates the runtime of multiprogramming quantum systems because executables are device- and region-dependent, which blocks low-latency repeated invocation of quantum services.
- **Mechanism** — INSUFFICIENT_EVIDENCE
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — Multiprogramming workloads including repeatedly invoked QNN services; INSUFFICIENT_EVIDENCE on device versus simulation split. / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Over 5x runtime speedup with improved execution fidelity (preprint arXiv:2601.01158). BASELINE = online co-compilation pipelines for multiprogramming quantum computing, which is the right comparator.
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Strongest runtime/serving-architecture paper in the TACO pool.

### TPDS — IEEE Trans. Parallel and Distributed Systems (2 papers)

#### `TPDS-007` Minimizing Communications of Quantum Circuit Simulations on Distributed Systems

- **Bibliographic** — Longshan Xu et al. · IEEE Trans. Parallel and Distributed Systems 1045-9219 · census year **2026** · vol 37, iss 4 , issue date 2026-4 · pp 775-786
- **DOI** — `10.1109/tpds.2026.3652733` · <https://doi.org/10.1109/tpds.2026.3652733>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`, `benchmarking_performance_modeling`
- **Gate 1 (classical systems problem)** — Communication overhead on multi-node distributed systems is identified as the performance bottleneck of full-state simulation; memory capacity forces the distribution.
- **Gate 2 (HPC/systems technique)** — Distributed simulation framework: level-by-level execution with a hybrid scheme that replaces intermediate multi-level communication by a single final merge.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs how a large classical cluster executes the quantum-simulation workload.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Communication overhead on multi-node distributed systems is identified as the performance bottleneck of full-state simulation; memory capacity forces the distribution.
- **Mechanism** — QuanTrans: distributed full-state simulation framework that restructures inter-node communication for circuits with particular structures, reducing communication volume.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reduced communication volume and runtime versus level-by-level distributed simulation; figures truncated (BASELINE = conventional distributed state-vector simulators).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — One of only two TPDS records that pass the gates; both are distributed state-vector simulation and both are census-year 2026.

#### `TPDS-008` Communication-Partition Co-Optimization for Quantum Circuit Simulation on CPU+GPU Clusters

- **Bibliographic** — Chenyang Jiao et al. · IEEE Trans. Parallel and Distributed Systems 1045-9219 · census year **2026** · vol 37, iss 6 , issue date 2026-6 · pp 1280-1294
- **DOI** — `10.1109/tpds.2026.3678345` · <https://doi.org/10.1109/tpds.2026.3678345>
- **Article type** — ORIGINAL_RESEARCH · **Scenario** — `HPC_FOR_Q` · **Branch** — `distributed_gpu_simulation`
- **Gate 1 (classical systems problem)** — Memory footprint, memory-access cost and inter-node data communication dominate over compute; full-data exchange per gate is the stated inefficiency.
- **Gate 2 (HPC/systems technique)** — Co-optimisation of communication and state partitioning on CPU+GPU clusters, exploiting gate-awareness and data locality.
- **Gate 3 (future CPU/GPU/QPU relevance)** — Directly informs heterogeneous CPU+GPU cluster execution of simulation workloads.
- **Quantum problem** — INSUFFICIENT_EVIDENCE
- **Classical / HPC problem** — Memory footprint, memory-access cost and inter-node data communication dominate over compute; full-data exchange per gate is the stated inefficiency.
- **Mechanism** — Communication-partition co-optimisation for state-vector simulation on CPU+GPU clusters, replacing gate-unaware full-data exchange.
- **Computational bottleneck** — INSUFFICIENT_EVIDENCE
- **Evaluation platform / scale** — INSUFFICIENT_EVIDENCE / INSUFFICIENT_EVIDENCE
- **Performance metrics** — INSUFFICIENT_EVIDENCE
- **Major claim (with baseline)** — Reduced communication time versus gate-unaware full-data communication as in QuEST; figures truncated (BASELINE = QuEST-style serial gate execution).
- **Limitation** — INSUFFICIENT_EVIDENCE
- **Artifact** — UNKNOWN
- **Conference extension** — UNKNOWN
- **Deep-dive priority** — 5
- **Notes** — Explicit CPU+GPU cluster target; the strongest heterogeneous-simulation record among the four journals.

### JPDC — J. Parallel and Distributed Computing

**0 included original research papers 2024-2026.** See §5.

---

## 4. Included REVIEW / SURVEY / PERSPECTIVE records (BIBLIOGRAPHY_HUB)

These do **not** count toward the original-research population. They are recorded because they are 
useful predecessor/successor navigation points.

| Journal | Year | DOI | Title | Type |
|---|---:|---|---|---|
| FGCS | 2024 | `10.1016/j.future.2024.04.060` | Quantum-centric supercomputing for materials science: A perspective on challenges and future directions | PERSPECTIVE |
| FGCS | 2026 | `10.1016/j.future.2026.108487` | The role of quantum computing in advancing scientific high-performance computing: A perspective from the ADAC institute | PERSPECTIVE |
| JPDC | 2026 | `10.1016/j.jpdc.2026.105303` | Comprehensive overview of quantum serverless: Elastic integration of quantum and classical computing | REVIEW_SURVEY |
| TQC | 2025 | `10.1145/3743149` | Integration of Quantum Accelerators with High Performance Computing—A Review of Quantum Programming Tools | REVIEW_SURVEY |
| TQC | 2025 | `10.1145/3762672` | Simulation of Quantum Computers: Review and Acceleration Opportunities | REVIEW_SURVEY |

---

## 5. BORDERLINE records

Recorded, not discarded. Each is a paper where one gate is satisfied only weakly. They are excluded 
from the headline counts and are the first place to look if the inclusion boundary is ever moved.

| Journal | Year | DOI | Title | Branch | Why it could be included | Why it is not |
|---|---:|---|---|---|---|---|
| FGCS | 2024 | `10.1016/j.future.2024.06.012` | Assessing and advancing the potential of quantum computing: A NASA case study | benchmarking_performance_modeling | Institution-scale assessment of where QPUs can beat supercomputers; covers algorithms, hardware evaluation and application readiness across a national-lab programme; a useful bibliography hub. | Primary substance is algorithms and application assessment; no scheduling, runtime, orchestration or simulation-systems contribution is evidenced in the abstract. |
| FGCS | 2024 | `10.1016/j.future.2024.107480` | Quantum resource estimation for large scale quantum algorithms | benchmarking_performance_modeling | Quantifies QEC overhead in both qubits and runtime and puts classical and quantum algorithm costs on a common footing - genuine performance/resource modeling for future heterogeneous systems. | Criteria treat 'resource estimates with no systems mechanism' as a false-positive class; the application is cryptanalysis and no classical systems technique is part of the contribution. |
| FGCS | 2025 | `10.1016/j.future.2025.107908` | Is quantum optimization ready? An effort towards neural network compression using adiabatic quantum computing | benchmarking_performance_modeling | A Q_FOR_HPC readiness study on a workload (large-model compression) that is genuinely compute- and memory-bound; asks the placement question directly. | The contribution is an application of adiabatic quantum computing to an optimisation problem; annealer/QUBO application is a documented false-positive class here. |
| FGCS | 2025 | `10.1016/j.future.2025.107934` | Solving combinatorial optimization and machine learning problems on hybrid near-term quantum photonic computers | hpc_qpu_integration, benchmarking_performance_modeling | Explicitly frames photonic QPUs as data-centre accelerators, uses real photonic hardware coupled to GPUs, reports a scaling improvement from a tiling technique, and lists multi-QPU among its keywords. | The headline outcomes are solution quality on optimisation and ML benchmarks; no scheduling, runtime or resource-management mechanism is evidenced. |
| FGCS | 2025 | `10.1016/j.future.2025.107975` | A multiple-circuit approach to quantum resource reduction with application to the quantum lattice Boltzmann method | circuit_cutting_reconstruction, benchmarking_performance_modeling | Uses parallel multi-circuit execution as the mechanism, which maps onto shot/circuit orchestration; targets a canonical HPC workload (CFD). | Core contribution is an algorithm reformulation of QLBM; no classical systems technique or measured systems cost is reported. |
| FGCS | 2025 | `10.1016/j.future.2025.108087` | A hybrid quantum-classical particle-in-cell method for plasma simulations | scientific_workflow_application, hybrid_workflow | A concrete kernel-offload study on a canonical HPC application (PIC plasma simulation) with computational cost measured as a primary outcome; exactly the coupling pattern a heterogeneous centre would face. | The quantum part runs on a PennyLane simulator rather than a QPU, and the mechanism is a hybrid neural-network solver (adjacent to false-positive class 5) rather than a systems technique. |
| FGCS | 2026 | `10.1016/j.future.2025.108095` | Cost-efficient quantum cloud task offloading with quantum-inspired particle swarm optimization | qpu_scheduling_resource_mgmt | The problem addressed - deciding which tasks go to which quantum cloud resource at what cost - is exactly QPU resource allocation, which this corpus cares about. | The mechanism is a quantum-inspired classical metaheuristic (false-positive class 2), and no abstract was retrievable, so the systems substance is unverified. |
| FGCS | 2026 | `10.1016/j.future.2026.108481` | Addressing the minor-embedding problem in quantum annealing and evaluating state-of-the-art algorithm performance | compiler_mapping_routing, benchmarking_performance_modeling | Treats embedding as a compilation/mapping stage and quantifies both its runtime and its downstream effect on solution error - the same shape as included qubit-mapping work (FGCS-033, FGCS-065). | The platform is a quantum annealer (adjacent to false-positive class 2), and the output is an evaluation of an existing tool (Minorminer) rather than a systems mechanism. |
| TC | 2024 | `10.1109/tc.2024.3506861` | Feynman Meets Turing: The Uncomputability of Quantum Gate-Circuit Emulation and Concatenation | compiler_mapping_routing | Constrains what the classical compilation layer can compute at all, which bears on the software stack. | The method is computability theory and no classical systems quantity is measured, so Gate 2 fails. |
| TC | 2025 | `10.1109/tc.2025.3544869` | Towards Effective Local Search for Qubit Mapping | compiler_mapping_routing | Qubit mapping is an NP-hard classical optimisation, and search effort is a classical computation cost. | The reported objective is auxiliary-gate count, a quantum resource; no compile-time or parallelism result is claimed. |
| TC | 2025 | `10.1109/tc.2025.3557965` | RSQC: Recursive Sparse QUBO Construction for Quantum Annealing Machines | compiler_mapping_routing | A classical mapping/compilation framework that determines what problem size fits on the target hardware. | The target is a quantum annealer and the measured quantity is embedding sparsity/problem size, adjacent to false-positive class 2. |
| TC | 2025 | `10.1109/tc.2025.3626469` | Feynman Meets Turing: Computability Aspects of Quantum Compiling Revisited | compiler_mapping_routing | Same limb as TC-010: realisability of compiler functions on digital hardware. | Theoretical result with no classical systems technique or measurement, so Gate 2 fails. |
| TC | 2025 | `10.1109/tc.2025.3643826` | Dynamic Quantum Circuit Compilation | compiler_mapping_routing | Qubit reuse is a resource-allocation mechanism and the compilation task is characterised formally. | The measured quantity is qubit count, a quantum resource; classical compile cost is not reported. |
| TC | 2025 | `10.1109/tc.2025.3645773` | QuanGuard: Error Evolution-Based Fingerprinting for Fraud Detection in Quantum Cloud Services | qpu_scheduling_resource_mgmt, architecture_control | It is the only record in these four journals that engages the quantum-cloud allocation and accounting layer at all, so it remains relevant to QPU resource management as a recorded BORDERLINE. | The reported metric is device-identification accuracy, a classification-accuracy quantity, and the contribution is a fingerprinting technique built from probing-circuit error patterns. The cloud allocation and throughput behaviour is the setting, not a quantity the paper improves, so Gate 2 is not m |
| TCAD | 2024 | `10.1109/tcad.2023.3297972` | Low-Rank Quantum State Preparation | compiler_mapping_routing | Explicitly offloads complexity from the circuit to a classical computer, so classical preprocessing is part of the design. | That classical cost is never measured; the reported quantity is circuit depth. |
| TCAD | 2024 | `10.1109/tcad.2023.3329042` | Small Sampling Overhead Error Mitigation for Quantum Circuits | benchmarking_performance_modeling | Sampling overhead is an execution/throughput cost on the device, and the characterisation reduction is measured. | The contribution is an error-mitigation technique, not a systems technique; Gate 2 is met only indirectly. |
| TCAD | 2024 | `10.1109/tcad.2023.3340608` | Noise Adaptive Quantum Circuit Mapping Using Reinforcement Learning and Graph Neural Network | compiler_mapping_routing | Mapping is a compiler stage and the RL/GNN pipeline is a substantial classical apparatus. | The objective is output fidelity, a quantum resource; no compile-cost or scalability result is claimed. |
| TCAD | 2024 | `10.1109/tcad.2024.3387290` | Efficient Qubit Routing Using a Dynamically Extract-and-Route Framework | compiler_mapping_routing | Routing is a compiler stage with a stated overhead budget. | The overhead measured is inserted gates and fidelity, not compilation time or memory. |
| TCAD | 2024 | `10.1109/tcad.2024.3507580` | CAMEL: Physically Inspired Crosstalk-Aware Mapping and Gate Scheduling for Frequency-Tunable Quantum Chips | compiler_mapping_routing, architecture_control | Crosstalk-aware gate scheduling does govern which operations may execute concurrently, which is an execution-parallelism mechanism worth retaining in the record. | The measured quantity is gate fidelity under parallel two-qubit operation - a quantum resource, not a classical systems quantity. Gate scheduling here is the means to a fidelity objective, so under the decision rule stated in this census (fidelity-objective mapping -> BORDERLINE) it does not pass Ga |
| TCAD | 2024 | `10.1109/tcad.2024.3509794` | PauliForest: Connectivity-Aware Synthesis and Pauli-Oriented Qubit Mapping for Near-Term Quantum Simulation | compiler_mapping_routing | Compiles the Hamiltonian-simulation kernels that dominate many workloads, coupling synthesis with mapping. | The reported quantities are depth and gate count; no compile-cost, parallelism or scheduling result is claimed. |
| TCAD | 2025 | `10.1109/tcad.2025.3570608` | A Divide-And-Conquer Pebbling Strategy for Oracle Synthesis in Quantum Computing | compiler_mapping_routing | The pebble game is a space-time scheduling problem inside the compiler, and the method is presented as scalable. | The resource traded is qubits against gate count, both quantum resources; no classical systems quantity is measured. |
| TCAD | 2025 | `10.1109/tcad.2025.3572021` | Special-Purpose Coherent Optical Quantum Computers Empower Qubit Mapping Optimization in General-Purpose Superconducting Quantum Computing | compiler_mapping_routing, hpc_qpu_integration | The workload being offloaded is a real compilation task for a gate-based QPU, and heterogeneous offload of a compiler stage is systems-relevant; it is recorded rather than excluded so the POSSIBLE_CROSSOVER is not lost. | The accelerator carrying the offloaded work is a QBoson coherent optical Ising machine solving a QUBO, which CRITERIA.md false-positive class 2 names explicitly (Ising machines, QUBO solvers). The measured quantity is qubit-mapping quality on heavy-hex placement, a quantum resource, so Gate 2 is not |
| TCAD | 2025 | `10.1109/tcad.2025.3588457` | HeteroQNN: Enabling Distributed QNN Under Heterogeneous Quantum Devices | multi_qpu_distributed_qc, hybrid_workflow | Distributed training and inference across heterogeneous, intermittently available QPUs is a genuine distributed-execution problem. | The workload is a QNN and the reported metric is model accuracy, which sits in false-positive class 5. |
| TCAD | 2025 | `10.1109/tcad.2025.3600368` | Robust and Optimal Loading of General Classical Data Into Quantum Computers | architecture_control | Data loading is a movement bottleneck on the input path of a quantum accelerator. | The contribution is a circuit-architecture robustness result measured in depth and error propagation, not a classical systems result. |
| TCAD | 2026 | `10.1109/tcad.2026.3656760` | A quantum circuit optimization framework for distributed quantum computing | multi_qpu_distributed_qc, compiler_mapping_routing | Distributed-QC compilation is an INCLUDE shape and the title places the work squarely in it. | NO_ABSTRACT: no communication, partitioning or cost metric can be confirmed, so Gate 1 rests on the title alone. |
| TCAD | 2026 | `10.1109/tcad.2026.3681225` | Advancing Quantum State Preparation Using Decision Diagram with Local Invertible Maps | compiler_mapping_routing, distributed_gpu_simulation | Decision diagrams combined with tensor networks are a classical data structure central to the result. | The reported quantity is circuit complexity; classical runtime or memory scalability is not reported. |
| TQC | 2024 | `10.1145/3636516` | Efficient Syndrome Decoder for Heavy Hexagonal QECC via Machine Learning | qec_classical_processing | Decoding is explicitly in scope, and the criteria list a new decoder algorithm as BORDERLINE. | The reported metric is threshold/accuracy; there is no parallelism, latency budget or accelerator mapping, which is what would move it to INCLUDED. |
| TQC | 2024 | `10.1145/3665335` | Quantum Circuit Cutting for Classical Shadows | circuit_cutting_reconstruction | Circuit-cutting reconstruction cost is a listed include shape. | The cost currency is samples/shots and estimator variance, not classical runtime, memory or parallel reconstruction; no systems implementation. |
| TQC | 2024 | `10.1145/3670417` | Efficient Quantum Circuit Design with a Standard Cell Approach, with an Application to Neutral Atom Quantum Computers | compiler_mapping_routing, architecture_control | The standard-cell abstraction plus layout-aware routing for zoned neutral-atom architectures is architecture-aware mapping, and separating memory, processing and measurement zones is a structural systems idea. | Gate 2 is a methodological analogy to VLSI standard cells; the layout speed-up is recorded BASELINE_UNCLEAR and the reported outputs are circuit layouts and space-time volume, which are quantum resources. My own deep-dive priority was already LOW. |
| TQC | 2024 | `10.1145/3678185` | Utilizing classical programming principles in the Intel Quantum SDK: implementation of quantum lattice Boltzmann method | scientific_workflow_application | Q_FOR_HPC workload plus explicit engagement with a production quantum SDK. | No runtime, memory, scaling or orchestration result; the quantum algorithm is the object of study. |
| TQC | 2024 | `10.1145/3688856` | A Model-Driven Framework for Composition-Based Quantum Circuit Design | quantum_software_engineering | Software stack is an explicit Gate 3 target. | Gate 1 is not met: no computation cost, memory, communication or runtime quantity appears. |
| TQC | 2025 | `10.1145/3705007` | What Quantum Can Learn from Classical Computer Engineering | benchmarking_performance_modeling | The special issue it introduces is explicitly about importing classical computer-engineering practice into quantum system design, and it frames co-design and the multi-core concept; it remains the clearest venue-level signal that TQC hosts classical-systems work (TQC-009 sits in this issue). | Gate 2 fails on my own wording: the contribution is editorial framing, not an HPC/systems/architecture technique. Verifier is correct. Retained as BIBLIOGRAPHY_HUB; article type SPECIAL_ISSUE_INTRO means the original-research count is unaffected. |
| TQC | 2025 | `10.1145/3722119` | Algorithmic Theory of Qubit Routing in the Linear Nearest Neighbor Architectures | compiler_mapping_routing | Compilation cost is an explicit Gate 1 quantity and this paper is entirely about it. | Gate 2 asks for a systems/architecture technique; the method is combinatorial complexity theory with no implementation or measurement. |
| TQC | 2025 | `10.1145/3731251` | Approximate Quantum Compiling for Quantum Simulation: A Tensor Network Based Approach | distributed_gpu_simulation, compiler_mapping_routing | Classical tensor-network compute serving compilation, with an explicit criticism of prior methods' optimization behaviour. | No reported runtime, memory or parallel-scaling measurement; the deliverable is circuit depth for state preparation. |
| TQC | 2025 | `10.1145/3733842` | Line-Graph Qubit Routing | compiler_mapping_routing | Architecture-aware mapping for a named hardware family. | The reported metric is circuit overhead, not compile-time scalability or a systems cost; criteria place gate-count/fidelity-only compilation at BORDERLINE. |
| TQC | 2025 | `10.1145/3737887` | QuL: Programming Library for Computational Cooling of Qubits | quantum_software_engineering, architecture_control | Software-stack artifact in the control layer. | Gate 1 is not met; the subject is a cooling protocol, which is closer to device operation than to classical systems. |
| TQC | 2025 | `10.1145/3763244` | CHARME: A Chain-based Reinforcement Learning Approach for the Minor Embedding Problem | compiler_mapping_routing | Scalability of the embedding computation is named as the motivation, and minor embedding is the annealer analogue of a compile stage. | The scalability claim is motivational; the evaluated quantities are embedding quality and chain structure, not embedding runtime or memory. Decisive point is cross-journal consistency: FGCS-063 addresses the same minor-embedding problem in the same census window, actually measures embedding executio |
| TQC | 2025 | `10.1145/3773909` | FIDDLE: Reinforcement Learning for Quantum Fidelity Enhancement | compiler_mapping_routing | Compiler-stage contribution with a learned classical component and an explicit surrogate-cost argument. | The optimization target is output fidelity, which the criteria place at BORDERLINE or EXCLUDE; no compile-time or scaling result. |
| TQC | 2025 | `10.1145/3779066` | qSIEVE: Efficient qLDPC Memory via Systolic Movement in Atom Arrays | architecture_control, qec_classical_processing | Qubit movement in an atom array is a data-movement and movement-scheduling problem, and the systolic schedule is a genuine dataflow-regularity constraint rather than decoration. | The only measured quantity is qubit overhead at a given logical error rate, which is a quantum resource. Gate 2 rests on an analogy to systolic dataflow with no classical latency, bandwidth, control-throughput or compute measurement attached. Under the rule that a quantum-resource-only measurement d |
| TQC | 2026 | `10.1145/3799888` | Quantum Backtracking in Qrisp Applied to Sudoku Problems | quantum_software_engineering | Software-stack/framework evidence and concrete resource accounting. | Fundamentally a quantum-algorithm implementation study; no classical runtime, memory or orchestration result. |
| TQC | 2026 | `10.1145/3800578` | Unifying Communication Paradigms in Measurement-based Delegated Quantum Computing | multi_qpu_distributed_qc | Communication-paradigm comparison for delegated computation, i.e. offloading structure. | The driving requirement is cryptographic blindness, placing it close to the excluded quantum-cryptography class; no computing-systems cost model. |
| TQC | 2026 | `10.1145/3800943` | It’s Quick to be Square: Fast Quadratisation for Quantum Toolchains | compiler_mapping_routing | Quadratisation is a classical transformation stage in the toolchain and the paper's framing is the cost of that stage rather than the quality of the resulting circuit, which is the distinction this census uses. | The runtime advantage is asserted without figures and without a comparator named beyond 'prior quadratisation methods', so the classical cost argument that carried the inclusion is unverified in the available evidence. The downstream consumer is QUBO preparation for annealing and QAOA toolchains, ad |
| TQC | 2026 | `10.1145/3815169` | QuCheck: A Property-based Testing Framework for Quantum Programs in Qiskit | quantum_software_engineering | Classical software-engineering technique transferred into the quantum stack. | NO_ABSTRACT, so Gate 1 cannot be verified; testing frameworks carry no execution-cost argument by default. |
| TQE | 2024 | `10.1109/tqe.2023.3338970` | Exploiting the Quantum Advantage for Satellite Image Processing: Review and Assessment | benchmarking_performance_modeling, scientific_workflow_application | Explicitly frames an HPC-versus-QPU partitioning decision and uses a classical-simulability criterion to make it. | No classical systems mechanism is built or measured; the substance is an application review of QML for satellite imagery (false-positive class 5 territory). |
| TQE | 2024 | `10.1109/tqe.2023.3343625` | Quantum Vulnerability Analysis to Guide Robust Quantum Computing System Design | benchmarking_performance_modeling | Performance modeling to guide system design is an explicit Gate-3 category; the paper targets system-level design decisions. | The contribution is a noise-characterization metric; no computation cost, parallelism, scheduling or data-movement mechanism. |
| TQE | 2024 | `10.1109/tqe.2024.3374879` | Testing and Debugging Quantum Circuits | benchmarking_performance_modeling | Software-stack contribution; testing/debugging tooling is part of the classical side of the stack. | No Gate-1 quantity is treated substantively (no cost, memory, latency, scaling). |
| TQE | 2024 | `10.1109/tqe.2024.3398410` | Variational Quantum Algorithms for the Allocation of Resources in a Cloud/Edge Architecture | qpu_scheduling_resource_mgmt | The workload is literally scheduling/resource allocation in a heterogeneous computing architecture, a Gate-1 and Gate-3 topic. | The contribution is an optimizer comparison on a QUBO encoding (false-positive class E8); no systems mechanism is contributed. |
| TQE | 2024 | `10.1109/tqe.2024.3401857` | Trellis Decoding for Qudit Stabilizer Codes and Its Application to Qubit Topological Codes | qec_classical_processing | Explicit precompute-versus-online cost split and graph-size (memory) analysis; decoder work is central to QEC classical processing. | Per the QEC rule a decoder algorithm alone is BORDERLINE: no parallel implementation, no accelerator, no scheduling. |
| TQE | 2024 | `10.1109/tqe.2024.3416836` | Optimizing the Electrical Interface for Large-Scale Color-Center Quantum Processors | architecture_control | Scalability of the classical control interface is explicitly the subject; a unit-cell architecture is a systems-architecture contribution. | Largely electronic circuit design for a specific qubit platform, adjacent to false-positive class 6 (control/readout electronics). |
| TQE | 2024 | `10.1109/tqe.2024.3419773` | Convolutional Neural Decoder for Surface Codes | qec_classical_processing | Latency is stated as a target, and ML decoders are the main route to accelerator implementations. | New decoder algorithm only, with no parallel or hardware implementation — BORDERLINE by the explicit QEC rule. |
| TQE | 2024 | `10.1109/tqe.2024.3430215` | Learning a Quantum Computer's Capability | benchmarking_performance_modeling | Scalability against classical simulation cost is the stated driver, and the output informs procurement/usage decisions. | The subject is device error behaviour; no resource, scheduling or execution mechanism is contributed. |
| TQE | 2024 | `10.1109/tqe.2024.3486546` | Hybrid Hamiltonian Simulation Approach for the Analysis of Quantum Error Correction Protocol Robustness | benchmarking_performance_modeling, architecture_control | Simulation-cost motivation plus explicit coupling to classical CMOS control design. | Primarily a device/protocol robustness study; the systems content is a tooling remark rather than a measured result. |
| TQE | 2025 | `10.1109/tqe.2024.3520805` | RSFQ All-Digital Programmable Multitone Generator for Quantum Applications | architecture_control | Explicit system-overhead and scalability framing for the classical control plane. | Superconducting circuit design; closer to false-positive class 6 than to a computing-systems contribution. |
| TQE | 2025 | `10.1109/tqe.2025.3542462` | Generating Shuttling Procedures for Constrained Silicon Quantum Dot Array | compiler_mapping_routing | Compilation/routing automation with a classical search-cost dimension, the same family as the included BeSnake paper. | The systems content (search cost, scalability) is not quantified in the abstract; may be purely a formal-methods result. |
| TQE | 2025 | `10.1109/tqe.2025.3552736` | Emulation of Density Matrix Dynamics With Classical Analog Circuits | distributed_gpu_simulation, architecture_control | Accelerator design for the quantum-simulation workload; Gate-1 'accelerator design' is present. | No scaling, throughput or energy comparison against digital simulation is given, so the systems case is unproven. |
| TQE | 2025 | `10.1109/tqe.2025.3563805` | Runtime–Coherence Tradeoffs for Hybrid Satisfiability Solvers | hybrid_workflow | Parallelism and runtime are treated substantively and tied to a hardware constraint. | The result is an algorithm-complexity analysis; no runtime, scheduler or systems artifact. |
| TQE | 2025 | `10.1109/tqe.2025.3572142` | Q-Gen: A Parameterized Quantum Circuit Generator | benchmarking_performance_modeling | Benchmarking infrastructure is an explicitly relevant TQE sub-area, and the motivation is classical workflow automation. | No Gate-1 resource quantity is analysed; the tool itself carries no performance claim. |
| TQE | 2025 | `10.1109/tqe.2025.3572764` | Reducing Quantum Error Correction Overhead With Versatile Flag-Sharing Syndrome Extraction Circuits | qec_classical_processing | The decoder (lookup-table) design and its memory cost are part of the contribution. | Predominantly syndrome-extraction circuit design — false-positive class E10 (QEC circuit/protocol design). |
| TQE | 2025 | `10.1109/tqe.2025.3574463` | Memory-Optimized Cubic Splines for High-Fidelity Quantum Operations | architecture_control | Controller memory is a genuine Gate-1 resource and the paper targets it explicitly, in the context of control logic moving closer to the qubits to cut feedback latency. | Gate 2 is not met: the contribution is a numerical interpolation scheme for pulse parameters, with no architecture, parallelism, latency or throughput result to establish it as a systems technique. Demoted from INCLUDED during adversarial verification. |
| TQE | 2025 | `10.1109/tqe.2025.3577769` | Improved Belief Propagation Decoding Algorithms for Surface Codes | qec_classical_processing | Explicit time-complexity framing and a decoder that is a candidate for parallel hardware. | New decoder algorithm only — BORDERLINE by the explicit QEC rule. |
| TQE | 2025 | `10.1109/tqe.2025.3595778` | Fault-Tolerant Noise Guessing Decoding of Quantum Random Codes | qec_classical_processing | Computational overhead of decoding is explicitly the framing of the paper. | Decoder algorithm only; no parallelism, accelerator or scheduling contribution. |
| TQE | 2025 | `10.1109/tqe.2025.3620130` | Toward Practical Application of the Quantum Carleman Lattice Boltzmann Method in Industrial CFD Simulations | scientific_workflow_application | Targets a core HPC application and reports resource requirements, informing future-workload projections. | No classical systems mechanism; it is a quantum-algorithm feasibility assessment for a domain problem. |
| TQE | 2025 | `10.1109/tqe.2025.3624658` | A Modular Quantum Network Architecture for Integrating Network Scheduling With Local Program Execution | quantum_runtime_orchestration, multi_qpu_distributed_qc | Scheduling and execution-integration are the substance, and local program execution (computing) is explicitly in scope of the architecture. | The setting is a quantum network delivering entanglement (false-positive class 4); the computing side is an interface, not a workload. |
| TQE | 2025 | `10.1109/tqe.2025.3624699` | Binary Tree Block Encoding of Classical Matrix | compiler_mapping_routing | Compilation time and space are treated as primary resources, which is a Gate-1 quantity. | The main result is a circuit construction with gate/qubit counts; the compilation-cost analysis may be secondary. |
| TQE | 2025 | `10.1109/tqe.2025.3626745` | A Dynamic Testing Strategy With Incremental Learning Model for Quantum Programs | benchmarking_performance_modeling | Software-stack contribution with an explicit execution-cost trade-off. | No HPC/systems technique; execution budget is the only Gate-1 quantity and it is treated statistically. |
| TQE | 2025 | `10.1109/tqe.2025.3636049` | Feynman Meets Turing: Computability Aspects of Exact Circuit Synthesis, Gate Efficiency, and the Spectral Gap Conjecture | compiler_mapping_routing | Concerns the compilation stage and its algorithmic limits, which bear on compiler design. | Pure computability theory; no cost, scaling or implementation content (close to false-positive class 7). |
| TQE | 2025 | `10.1109/tqe.2025.3640361` | Low-Complexity Syndrome-Based Linear Programming Decoding of Quantum LDPC Codes | qec_classical_processing | Explicit complexity/early-stopping mechanism (a compute-budget control) and decoder scheduling flavour. | New decoder algorithm only, evaluated under an idealized noise model — BORDERLINE by the QEC rule. |
| TQE | 2026 | `10.1109/tqe.2025.3649617` | Multiplexed Bilayered Realization of Fault-Tolerant Quantum Computation Over Optically Networked Trapped-Ion Modules | multi_qpu_distributed_qc, architecture_control | Modular and distributed quantum-computing architecture is an explicit INCLUDE shape, and the paper sizes inter-module resources for a computing objective (fault-tolerant MBQC) rather than a communication objective. | The quantity actually optimized is the remote entanglement generation rate against the RHG lattice bond-failure threshold, achieved by photonic multiplexing. That is a quantum-networking physical-layer mechanism (false-positive class 4), not a classical computing-systems contribution: no classical c |
| TQE | 2026 | `10.1109/tqe.2026.3659096` | Encrypted-State Quantum Compilation Scheme Based on Quantum Circuit Obfuscation for Quantum Cloud Platforms | compiler_mapping_routing, quantum_runtime_orchestration | Cloud compilation service design with an overhead trade-off — a systems concern for shared QPU infrastructure. | The contribution is a security scheme; the systems content (overhead) is secondary and unquantified here. |
| TQE | 2026 | `10.1109/tqe.2026.3659400` | A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits | architecture_control | Control systems and classical control hardware are an explicitly relevant TQE sub-area; as a survey it is a useful bibliography hub. | Content is RF/microwave and cryogenic electronics engineering, adjacent to excluded class 6. |
| TQE | 2026 | `10.1109/tqe.2026.3663507` | Parallel Variational Quantum Algorithms With Gradient-Informed Restart to Speed Up Optimization in the Presence of Barren Plateaus | hybrid_workflow | Parallel execution and restart policy are genuine execution-strategy content. | The motivation is barren plateaus, which the criteria exclude; no scheduling or resource-management mechanism. |
| TQE | 2026 | `10.1109/tqe.2026.3668098` | Parameter Analysis and Optimization of Layer Fidelity for Quantum Processor Benchmarking at Scale | benchmarking_performance_modeling | Benchmarking infrastructure at processor scale with an explicit measurement-cost dimension. | The resource optimized is quantum device time, not a classical systems resource; content is device characterization. |
| TQE | 2026 | `10.1109/tqe.2026.3670353` | Rapid Autotuning of a SiGe Quantum Dot Into the Single-Electron Regime With Machine Learning and RF-Reflectometry FPGA-Based Measurements | architecture_control | Real-time FPGA processing plus measurement-count reduction is a throughput/latency contribution in the classical control plane. | The subject matter is device tuning (false-positive class 6); no computing-systems abstraction is produced. |
| TQE | 2026 | `10.1109/tqe.2026.3671723` | Efficient Implementation of Randomized Quantum Algorithms With Dynamic Circuits | quantum_runtime_orchestration | Wall-clock execution time and submission overhead are the optimized quantities — a genuine orchestration concern. | No runtime system or scheduler is built; the mechanism is a circuit-level engineering technique. |
| TQE | 2026 | `10.1109/tqe.2026.3674210` | Beyond Asymptotic Scaling: Comparing Functional Quantum Linear Solvers | benchmarking_performance_modeling | Empirical performance modeling of a kernel central to HPC workloads, explicitly contrasting asymptotics with practice. | Quantum-algorithm resource counting (false-positive class 7) with no classical systems mechanism. |
| TQE | 2026 | `10.1109/tqe.2026.3687237` | Quantum Communication Complexity of Regularized Linear Regression Protocols | multi_qpu_distributed_qc | Communication cost of distributed computation is treated as the central resource. | Purely a communication-complexity result (false-positive class 7); no systems mechanism or measurement. |
| TQE | 2026 | `10.1109/tqe.2026.3697204` | Quantum Computing for Computational Sciences | scientific_workflow_application, benchmarking_performance_modeling | Future-workload projection for HPC application domains, with resource requirements as the organizing axis; useful as a bibliography hub. | Application/algorithm survey with no classical systems mechanism (overlaps false-positive class 3). |
| TQE | 2026 | `10.1109/tqe.2026.3706630` | Multilevel Gate Set Optimization of Quantum Circuits for Partial Differential Equations | compiler_mapping_routing, scientific_workflow_application | Explicit comparison against a production compiler, and the workload is a scientific-computing kernel. | The result is gate-count reduction, which the criteria place at BORDERLINE or EXCLUDE without systems implications. |
| TQE | 2026 | `10.1109/tqe.2026.3710775` | Topological Quantum Compilation Using Mixed-Integer Programming | compiler_mapping_routing | Classical solver cost is the binding constraint on the compilation method — a genuine compilation-scalability question. | Targets topological hardware that is not realized; no measured compile-time scaling reported in the abstract. |
| TQE | 2026 | `10.1109/tqe.2026.3730475` | Noise-model-free versus Bayes-optimal decoding of finite-energy GKP qubits | qec_classical_processing | Decoder algorithm comparison falls under the QEC decoder rule, which makes decoder-only work BORDERLINE rather than excluded. | No abstract was retrieved, so no evidence of parallelism, hardware implementation or classical cost analysis exists. |

---

## 6. Unresolved records

| Journal | Year | DOI | Title | What would resolve it |
|---|---:|---|---|---|
| TCAD | 2026 | `10.1109/tcad.2026.3677771` | Optimizing Unitary Coupled Cluster with Single and Double Kernels for Modern NISQ Architectures | Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3677771). The gates turn on whether the contribution is ansatz design for UCCSD (EXCLUDE under the VQE rule) or architecture-aware kernel compilation with a compile-cost or scheduling result (INCLUDE); the abstract or Section I would settle it. |
| TCAD | 2026 | `10.1109/tcad.2026.3693628` | QDP: Worst-case Fidelity-aware Qubit Mapping and Routing using Dynamic Programming | Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3693628). The gates turn on whether the dynamic-programming mapper reports compilation time/memory scalability alongside worst-case fidelity; an evaluation-section check would settle it. |
| TCAD | 2026 | `10.1109/tcad.2026.3705986` | Online Testing Error Mitigation for Quantum Computers | Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3705986). The gates turn on whether 'online' testing means runtime classical processing with a latency/overhead budget, or offline characterisation reported as fidelity only. |

All 3 are IEEE TCAD Early Access records with no retrievable abstract. They are counted in 
neither the included nor the excluded population.

---

## 7. Artifact / public-code matrix (included original research)

| Status | Count | Share |
|---|---:|---:|
| `UNKNOWN` | 68 | 76% |
| `NO_PUBLIC_ARTIFACT_FOUND` | 11 | 12% |
| `PARTIAL` | 7 | 8% |
| `PUBLIC_CODE` | 3 | 3% |

| Journal | Paper | Artifact | URL |
|---|---|---|---|
| FGCS | QFaaS: A Serverless Function-as-a-Service framework for Quantum comput | `PUBLIC_CODE` | https://github.com/Cloudslab/qfaas |
| FGCS | State of practice: Evaluating GPU performance of state vector and tens | `PARTIAL` |  |
| FGCS | LuGo: An enhanced quantum phase estimation implementation | `PARTIAL` |  |
| FGCS | Efficient and scalable branch-and-bound algorithm for exact qubit allo | `PUBLIC_CODE` | https://github.com/Guillaume-Helbecque/P3D-DFS |
| TQC | MQT Predictor: Automatic Device Selection with Device-Specific Circuit | `PUBLIC_CODE` | https://github.com/cda-tum/mqt-predictor |
| TQC | Optimization Applications as Quantum Performance Benchmarks | `PARTIAL` | https://github.com/SRI-International/QC-App-Oriented-Benchmarks |
| TQC | Realistic Cost to Execute Practical Quantum Circuits using Direct Clif | `PARTIAL` | https://github.com/latticesurgery-com/lattice-surgery-compiler |
| TQE | End-to-End Workflow for Machine-Learning-Based Qubit Readout With QICK | `PARTIAL` | https://github.com/openquantumhardware/qick |
| TQE | Quantum Circuit Optimization and MBQC Scheduling With a Pauli Tracking | `PARTIAL` |  |
| TQE | Leveraging Quantum Machine Learning Generalization to Significantly Sp | `PARTIAL` | https://github.com/BQSKit/bqskit |

**Reading this honestly.** `UNKNOWN` dominates because publisher artifact pages (IEEE Xplore, ACM DL 
badge pages, Elsevier full text) were not reachable from the research environment for most records. 
`UNKNOWN` here means *not checked*, not *no artifact*. This is the single largest evidence limitation 
of the census and is the first thing a follow-up pass should close.

---

## 8. Conference-extension lineage

| Status | Count |
|---|---:|
| `UNKNOWN` | 85 |
| `RELATED_LINEAGE` | 4 |

**Zero `CONFIRMED_EXTENSION` records.** No journal paper in this corpus states, in text reachable from 
this environment, that it is an extended version of a conference paper. Four records carry 
`RELATED_LINEAGE` with stated evidence. Every other record is `UNKNOWN` — which means *not established*, 
not *not an extension*. ACM article pages returned HTTP 403 and IEEE Xplore was unreachable, so the 
front-matter footnotes where such statements normally appear could not be read. Treating any of these 
as independent contributions in a later analysis would be `INSUFFICIENT_EVIDENCE`.

---

## 9. False-positive log

383 candidate records were excluded. The dominant classes, normalised onto the seven canonical 
false-positive classes (per-journal files carry the corpus-local extension classes verbatim):

| Class | Description | FGCS | TQE | TQC | TCAD | TC | TACO | TPDS | JPDC | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `FP1` | Post-quantum cryptography | 9 | 6 | 0 | 11 | 12 | 2 | 3 | 1 | **44** |
| `FP2` | Quantum-inspired classical methods (Ising machines, annealing hardware, QUBO) | 8 | 32 | 2 | 4 | 2 | 0 | 1 | 2 | **51** |
| `FP3` | Classical quantum chemistry / many-body | 2 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | **7** |
| `FP4` | Quantum networking / QKD / quantum internet | 6 | 53 | 1 | 2 | 3 | 0 | 0 | 0 | **65** |
| `FP5` | Quantum machine learning applications | 13 | 15 | 3 | 5 | 2 | 1 | 0 | 1 | **40** |
| `FP6` | Quantum sensing / metrology / device physics / cryo electronics | 0 | 31 | 4 | 9 | 3 | 0 | 0 | 0 | **47** |
| `FP7` | Quantum algorithms / complexity / synthesis with no systems mechanism | 4 | 32 | 21 | 4 | 3 | 0 | 0 | 0 | **64** |
| `FP8` | Circuit synthesis, gate-count-only | 0 | 0 | 11 | 0 | 0 | 0 | 0 | 0 | **11** |
| `FP9` | VQA methodology / ansatz / error mitigation | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | **5** |
| `FP10` | Device characterization / error mitigation | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | **4** |
| `FP11` | PL theory / formal methods | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | **2** |
| `FP12` | Visualization / HCI | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| `FP13` | Non-quantum vocabulary collision | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| `FP14` | Quantum cryptography protocols | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | **4** |
| `OTHER` | Other / unlabelled free-text reason | 12 | 13 | 0 | 6 | 3 | 0 | 0 | 2 | **36** |
| | **TOTAL** | 54 | 183 | 58 | 41 | 28 | 5 | 8 | 6 | **383** |

### 9.1 Which search terms cost the most

- **`quantum` alone is useless as a discriminator in TQE and TQC**, where every article is quantum. 
  In those two journals the discriminating question was not *is it quantum* but *does the paper state 
  a classical cost quantity* (runtime, memory, communication volume, compile time, throughput, 
  utilization) rather than only a quantum-resource quantity (gate count, T-count, depth, fidelity, 
  logical error rate, entanglement rate, shots-to-accuracy).
- **`post-quantum` / `quantum-resistant`** is the dominant false positive in the classical systems 
  journals — 44 records, concentrated in TC (12) and TCAD (11). Any future automated query must 
  negate `post-quantum`, `quantum-resistant`, `lattice-based`, `Kyber`, `Dilithium`, `NTT`, `SPHINCS`, `HQC`.
- **`distributed`, `node`, `scalable`** are actively misleading inside quantum venues: in TQE they 
  overwhelmingly mean *entanglement distribution* and *qubit-count scalability*, not classical 
  distributed execution.
- **`anneal` / `Ising` / `QUBO`** pulls in both quantum annealing applications and purely classical 
  Ising-machine hardware; both are out of scope here and together account for 51 exclusions.
- **`tensor network`, `tensor train`** collides with classical low-rank numerics 
  (FGCS `10.1016/j.future.2026.108709` is the cleanest example: a real TPU/GPU/CPU benchmarking paper 
  with no quantum computer anywhere in it).
- Best-precision terms: `compiler` / `transpilation`, `HPC` / `cloud` / `serverless`, `decoder` / `syndrome`, 
  `statevector` / `decision diagram` / `circuit simulation`.


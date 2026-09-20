# Quantum-HPC Journal Census — ACM TQC and ACM TACO, 2024–2026

Prepared against `/home/claude/jc/CRITERIA.md`. Two journals, 106 records classified in total.

## 1. Scope and method

This is a venue census of the **HPC x quantum-computing interface**, not a quantum-computing literature review. Every record was classified with the Three-Gate test: (1) a real classical systems problem, (2) an HPC/systems/architecture technique as a major part of the contribution, (3) material relevance to future CPU/GPU/HPC to QPU heterogeneous computing.

**Populations.**

| Journal | ISSN | Window | Records classified | Denominator |
|---|---|---|---|---|
| ACM TQC | 2643-6809 / 2643-6817 | 2024–2026 | 97 | Full population minus front matter |
| ACM TACO | 1544-3566 | 2024–2026 | 9 | Quantum-vocabulary candidate pool drawn from a 412-article full-population sweep |

**Census-year convention** (supplied, not re-derived): census year = year of earliest public availability (ACM published-online / Just Accepted date), with the final volume/issue and cover date recorded separately. TQC v5=2024, v6=2025, v7=2026; TACO v21=2024, v22=2025, v23=2026. Records with no volume are ACM Just Accepted.

**Operating discriminator.** Because the entire TQC population is quantum, gate discipline reduces to one question applied to each abstract: *does the paper state a classical cost quantity — runtime, memory, communication volume, compile time, throughput, utilization, scheduling latency — or only a quantum-resource quantity — gate count, T-count, depth, qubit count, fidelity, shots-for-accuracy?* Papers of the second kind were excluded however well executed.

**Evidence discipline.** Abstracts are the primary evidence (700-character captures). Ten records were checked against arXiv abstract pages to fill baseline, artifact and lineage gaps; two ACM DOI fetches returned HTTP 403 and were not retried beyond the second attempt. Three TQC records carry `NO_ABSTRACT` (TQC-078, TQC-081, TQC-083) and are flagged as classified from title and metadata only. Where a claim's comparator could not be established the record says `BASELINE_UNCLEAR`; where a field could not be established it says `INSUFFICIENT_EVIDENCE`. Institutions were not present in the source dossiers and are recorded as `INSUFFICIENT_EVIDENCE` throughout.

**Branch vocabulary.** The CRITERIA starting vocabulary was used as-is, plus three bottom-up additions the corpus required: `classical_simulation_engine` (single-node simulator engineering: decision diagrams, sparse/adaptive representations, tensor-ring evaluation), `parallel_classical_kernel` (a parallel classical computation whose consumer is the quantum stack), and `quantum_software_engineering` (modeling, testing and library tooling).

## 2. Per-year verdict tables

### TQC

| Census year | INCLUDED | BORDERLINE | EXCLUDED | Total | Included original research |
|---|---|---|---|---|---|
| 2024 | 7 | 5 | 22 | 34 | 7 |
| 2025 | 6 | 8 | 18 | 32 | 4 |
| 2026 | 9 | 4 | 18 | 31 | 9 |
| **Total** | **22** | **17** | **58** | **97** | **20** |

Branch frequency (INCLUDED + BORDERLINE): `compiler_mapping_routing` 15, `benchmarking_performance_modeling` 8, `classical_simulation_engine` 8, `architecture_control` 6, `qec_classical_processing` 5, `multi_qpu_distributed_qc` 4, `quantum_runtime_orchestration` 4, `distributed_gpu_simulation` 4, `quantum_software_engineering` 4, `hpc_qpu_integration` 2, `hybrid_workflow` 2, `qpu_scheduling_resource_mgmt` 2, `parallel_classical_kernel` 1, `circuit_cutting_reconstruction` 1, `scientific_workflow_application` 1.

Scenario frequency (INCLUDED + BORDERLINE): `HPC_FOR_Q` 38, `FUTURE_WORKLOAD` 12, `Q_IN_HPC` 4, `Q_FOR_HPC` 1.

### TACO

| Census year | INCLUDED | BORDERLINE | EXCLUDED | Total | Included original research |
|---|---|---|---|---|---|
| 2024 | 1 | 0 | 4 | 5 | 1 |
| 2025 | 2 | 0 | 0 | 2 | 2 |
| 2026 | 1 | 0 | 1 | 2 | 1 |
| **Total** | **4** | **0** | **5** | **9** | **4** |

Branch frequency (INCLUDED + BORDERLINE): `compiler_mapping_routing` 4, `qpu_scheduling_resource_mgmt` 3, `circuit_cutting_reconstruction` 1, `multi_qpu_distributed_qc` 1, `qec_classical_processing` 1, `quantum_runtime_orchestration` 1.

Scenario frequency (INCLUDED + BORDERLINE): `HPC_FOR_Q` 4, `Q_IN_HPC` 3, `FUTURE_WORKLOAD` 2.

## 3. Full records — TQC INCLUDED (22)

20 of these are ORIGINAL_RESEARCH and count toward the included population. Two do not: TQC-048 and TQC-057 (REVIEW_SURVEY), both tagged BIBLIOGRAPHY_HUB. TQC-035 (SPECIAL_ISSUE_INTRO, also BIBLIOGRAPHY_HUB) was demoted to BORDERLINE by adjudication and appears in section 5.

#### TQC-009 — Revisiting the Mapping of Quantum Circuits: Entering the Multi-core Era

- **DOI** `10.1145/3655029` · **census year** 2024 · **v6 i1 pp1-26** · online 2024-03-30 · issue 2025-3-31
- **Lead author** Pau Escofet (+8) · institution INSUFFICIENT_EVIDENCE · arXiv 2403.17205 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Inter-core communication volume and execution time when a circuit is partitioned across the cores of a modular quantum processor; mapping is posed as an assignment problem whose cost is communication.
- **Gate 2 — HPC/systems technique:** Hungarian-algorithm-based qubit-to-core assignment (HQA) plus derived theoretical bounds on non-local communication for random circuits; comparative evaluation against state-of-the-art multi-core mappers.
- **Gate 3 — heterogeneous relevance:** Supplies a communication-cost model and mapping policy for modular/multi-core QPUs, the interconnect layer any HPC-hosted multi-QPU system will need.
- **Key claim + baseline:** 4.9x improvement in execution time and 1.6x in non-local communications against the best competing multi-core mapping algorithm (preprint arXiv:2403.17205); comparator is the best prior multi-core mapper, not a single-core baseline.
- **Evaluation platform:** Simulation/benchmark circuit suite over multi-core architecture models; INSUFFICIENT_EVIDENCE on specific hardware.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Group (UPC Barcelona, Escofet et al.) has prior multi-core mapping conference work; no explicit extension statement located. Do not treat as confirmed.
- **Deep-dive priority:** HIGH
- **Notes:** Appears in the v6 special issue tied to TQC-035 (classical computer engineering). Central multi-core mapping reference for this corpus.

#### TQC-019 — MQT Predictor: Automatic Device Selection with Device-Specific Circuit Compilation for Quantum Computing

- **DOI** `10.1145/3673241` · **census year** 2024 · **v6 i1 pp1-26** · online 2024-06-17 · issue 2025-3-31
- **Lead author** Nils Quetschlich (+2) · institution INSUFFICIENT_EVIDENCE · arXiv 2310.06889 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `compiler_mapping_routing`, `quantum_runtime_orchestration`
- **Gate 1 — classical systems problem:** Choosing a device and a compilation pipeline from a combinatorially growing space of devices, compilers and passes; tool-selection and compilation-flow automation.
- **Gate 2 — HPC/systems technique:** Learning-based automatic device selection with device-specific compiler construction that mixes passes from several toolchains into one optimized flow (MQT Predictor).
- **Gate 3 — heterogeneous relevance:** Directly addresses the software-stack layer that a heterogeneous CPU/GPU/QPU site would need to route a job to an appropriate backend.
- **Key claim + baseline:** Claims automated selection plus device-specific compilation outperforming individual off-the-shelf compilers on a figure-of-merit combining expected fidelity and cost; baseline = standard Qiskit/TKET default flows.
- **Evaluation platform:** MQT Bench circuits over multiple device models; Python/MQT toolchain.
- **Artifact status:** PUBLIC_CODE
- **Artifact URL:** https://github.com/cda-tum/mqt-predictor
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2310.06889 carries no extension statement in the abstract listing.
- **Deep-dive priority:** MEDIUM
- **Notes:** Part of the Munich Quantum Toolkit family; a stable, maintained artifact makes it a good reproducibility anchor.

#### TQC-021 — ARQUIN: Architectures for Multinode Superconducting Quantum Computers

- **DOI** `10.1145/3674151` · **census year** 2024 · **v5 i3 pp1-59** · online 2024-07-26 · issue 2024-9-30
- **Lead author** James Ang (+32) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `multi_qpu_distributed_qc`, `architecture_control`, `benchmarking_performance_modeling`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** End-to-end performance of a multinode quantum computer where internode links are two to three orders of magnitude slower and noisier than local gates: interconnect latency, entanglement-distillation overhead, and compiler-level placement across nodes.
- **Gate 2 — HPC/systems technique:** Full-stack co-design study with a multi-level simulation framework spanning device, network, compiler and application layers; systematic design-space exploration of node-count, link-rate and distillation choices.
- **Gate 3 — heterogeneous relevance:** Sets out the architectural taxonomy and performance ceilings for multinode QPUs, the structure an HPC centre would integrate as a single logical accelerator.
- **Key claim + baseline:** Reports achievable performance regimes for early multinode machines and a co-design roadmap balancing entanglement generation, distillation and local architecture; qualitative roadmap rather than a single speedup number, so BASELINE_UNCLEAR for any headline figure.
- **Evaluation platform:** Multi-level simulation stack for superconducting nodes with optical interconnects.
- **Artifact status:** NO_PUBLIC_ARTIFACT_FOUND
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2212.06167 'Architectures for Multinode Superconducting Quantum Computers' (33 authors, community co-design study). No conference version identified.
- **Deep-dive priority:** HIGH
- **Notes:** Large multi-institution (DOE labs, IBM, academia) study; functions as an architecture reference and a citation hub for multinode QC. Tag BIBLIOGRAPHY_HUB-like even though it is original research.

#### TQC-022 — Optimization Applications as Quantum Performance Benchmarks

- **DOI** `10.1145/3678184` · **census year** 2024 · **v5 i3 pp1-44** · online 2024-07-17 · issue 2024-9-30
- **Lead author** Thomas Lubinski (+6) · institution INSUFFICIENT_EVIDENCE · arXiv 2302.02278 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `benchmarking_performance_modeling`
- **Gate 1 — classical systems problem:** Measuring run-time execution performance against solution quality for optimization workloads on quantum devices, so that time-to-solution can be compared across gate-model and annealing backends.
- **Gate 2 — HPC/systems technique:** Application-oriented benchmarking framework with a run-time/quality trade-off methodology adapted from classical optimization-algorithm characterization.
- **Gate 3 — heterogeneous relevance:** Provides a time-to-solution measurement methodology usable when a QPU is one backend among several in a heterogeneous facility.
- **Key claim + baseline:** Characterizes Max-Cut solution quality versus execution time on gate-model devices and an annealer; comparisons are across devices/algorithms rather than against a classical solver baseline, so classical-advantage claims are BASELINE_UNCLEAR.
- **Evaluation platform:** Gate-model quantum devices and a quantum annealing device; QED-C benchmark suite lineage.
- **Artifact status:** PARTIAL
- **Artifact URL:** https://github.com/SRI-International/QC-App-Oriented-Benchmarks
- **Conference extension:** RELATED_LINEAGE
- **Lineage evidence:** Continues the QED-C application-oriented benchmark series (earlier suite papers by Lubinski et al.); no explicit extension statement.
- **Deep-dive priority:** MEDIUM
- **Notes:** Artifact URL is the known QED-C benchmark repository associated with this author group; treat repo linkage as PARTIAL since the article-specific artifact was not verified. KEPT INCLUDED against the verification pass. Rebuttal: the contribution is not an application accuracy comparison. CRITERIA lists 'quantum performance modeling' as an INCLUDE shape and 'benchmarking_performance_modeling' as a branch, and this paper's stated object is a framework evaluating the trade-off between run-time execution performance and solution quality. Run-time execution performance is wall-clock time, a classical cost quantity, not a quantum resource, so the rule invoked for TQC-066 and TQC-016 does not apply here. The verifier's point that comparisons run across devices and algorithms rather than against a classical solver is a baseline-completeness limitation, already recorded in key_claim_with_baseline, and it bounds what may be concluded about quantum advantage; it does not remove the run-time axis that carries Gate 1 and Gate 2. Excluding it would also be inconsistent with keeping TQC-064 and TQC-072, which are likewise comparative performance studies with internal baselines.

#### TQC-025 — Robust Qubit Mapping Algorithm via Double-Source Optimal Routing on Large Quantum Circuits

- **DOI** `10.1145/3680291` · **census year** 2024 · **v5 i3 pp1-26** · online 2024-08-03 · issue 2024-9-30
- **Lead author** Chin-Yi Cheng (+5) · institution INSUFFICIENT_EVIDENCE · arXiv 2210.01306 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Mapping and routing algorithms failing to scale to circuits with hundreds of qubits; compile-time cost and scheduling of SWAP insertion on large circuits.
- **Gate 2 — HPC/systems technique:** Duostra: double-source optimal routing for two-qubit gates plus two heuristic schedulers (limitedly exhaustive search and a greedy variant) designed to keep compile time tractable at large circuit sizes.
- **Gate 3 — heterogeneous relevance:** Compilation scalability is a classical-compute bottleneck in any QPU job pipeline; this quantifies the routing-stage cost at scale.
- **Key claim + baseline:** Reports improved mapping quality on large circuits versus established routers (SABRE-class heuristics) while remaining tractable; exact figures not in the abstract, so the headline is recorded as BASELINE = prior heuristic mappers.
- **Evaluation platform:** Large benchmark circuits on real-device coupling maps; C++ implementation.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** MEDIUM
- **Notes:** Explicit classical-scalability framing is what separates this from the gate-count-only mapping papers in the same volume.

#### TQC-029 — Realistic Cost to Execute Practical Quantum Circuits using Direct Clifford+T Lattice Surgery Compilation

- **DOI** `10.1145/3689826` · **census year** 2024 · **v5 i4 pp1-28** · online 2024-08-27 · issue 2024-12-31
- **Lead author** Tyler Leblond (+3) · institution INSUFFICIENT_EVIDENCE · arXiv 2311.10686 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `compiler_mapping_routing`, `qec_classical_processing`, `benchmarking_performance_modeling`
- **Gate 1 — classical systems problem:** Resource estimation for fault-tolerant execution: magic-state request cadence, distillation throughput, storage sizing, and allocation of lattice-surgery operations to hardware tiles.
- **Gate 2 — HPC/systems technique:** Two-stage compilation pipeline (logical gates to layout-independent instructions, then to local lattice-surgery instructions with tile allocation) with post-hoc scheduling analysis of magic-state supply and demand.
- **Gate 3 — heterogeneous relevance:** Quantifies the classical control and resource-management burden of fault-tolerant execution, which determines the size of the classical side of a future HPC-QPU system.
- **Key claim + baseline:** Produces realistic space-time cost estimates for practical circuits under direct Clifford+T lattice-surgery compilation; improvement is over prior coarse resource-estimation pipelines, not a runtime speedup.
- **Evaluation platform:** Extension of the open-source Lattice Surgery Compiler; benchmark logical circuits.
- **Artifact status:** PARTIAL
- **Artifact URL:** https://github.com/latticesurgery-com/lattice-surgery-compiler
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Builds on the open-source Lattice Surgery Compiler codebase, which is a tool lineage rather than a conference-paper lineage.
- **Deep-dive priority:** MEDIUM
- **Notes:** ORNL-affiliated; bridges compiler work and QEC resource accounting.

#### TQC-030 — Efficient Quantum Circuit Simulation by Tensor Network Methods on Modern GPUs

- **DOI** `10.1145/3696465` · **census year** 2024 · **v5 i4 pp1-26** · online 2024-09-23 · issue 2024-12-31
- **Lead author** Feng Pan (+4) · institution INSUFFICIENT_EVIDENCE · arXiv 2310.03978 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `distributed_gpu_simulation`, `classical_simulation_engine`
- **Gate 1 — classical systems problem:** Contraction-path search cost and GPU execution efficiency for tensor-network simulation of large circuits, where state-vector simulation exceeds memory.
- **Gate 2 — HPC/systems technique:** Conversion of Einstein-summation contractions into GEMM calls to use tensor cores, mixed-precision arithmetic, and contraction-path optimization on modern GPUs.
- **Gate 3 — heterogeneous relevance:** Directly a GPU-HPC kernel-engineering contribution serving quantum circuit verification; the archetype of HPC_FOR_Q in this corpus.
- **Key claim + baseline:** Sustained >21 TFLOPS on an NVIDIA A100; 3.96x reduction in verification time for 18-cycle Sycamore circuits; 12.5x over state-of-the-art CPU approaches and 4.48x-6.78x over existing GPU methods reported in the literature (preprint arXiv:2310.03978).
- **Evaluation platform:** NVIDIA A100 GPU; Sycamore random circuit sampling verification workloads.
- **Artifact status:** NO_PUBLIC_ARTIFACT_FOUND
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** HIGH
- **Notes:** Headline figures come from the preprint; the published abstract does not restate them.

#### TQC-037 — Forward and Backward Constrained Bisimulations for Quantum Circuits Using Decision Diagrams

- **DOI** `10.1145/3712711` · **census year** 2025 · **v6 i2 pp1-21** · online 2025-01-18 · issue 2025-6-30
- **Lead author** Lukas Burgholzer (+5) · institution INSUFFICIENT_EVIDENCE · arXiv 2308.09510 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `classical_simulation_engine`
- **Gate 1 — classical systems problem:** Exponential growth of state representation with qubit count in classical simulation; reducing the size of the represented model while preserving the quantities of interest.
- **Gate 2 — HPC/systems technique:** Forward and backward constrained bisimulation (lumping) applied over decision-diagram representations, a state-space-reduction technique carried over from Markov-chain and ODE model reduction.
- **Gate 3 — heterogeneous relevance:** Improves the memory/compute envelope of classical simulators, the workhorse of quantum software development on HPC resources.
- **Key claim + baseline:** Reports reductions in represented state dimension and simulation effort versus unreduced decision-diagram simulation; quantitative factors not in the abstract, BASELINE = plain DD-based simulation.
- **Evaluation platform:** Decision-diagram simulator (MQT lineage); benchmark circuit families.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** MEDIUM
- **Notes:** Burgholzer is an MQT author; likely tooling overlap with MQT DDSIM but not verified.

#### TQC-048 — Integration of Quantum Accelerators with High Performance Computing—A Review of Quantum Programming Tools

- **DOI** `10.1145/3743149` · **census year** 2025 · **v6 i3 pp1-46** · online 2025-06-10 · issue 2025-9-30
- **Lead author** Amr Elsharkawy (+11) · institution INSUFFICIENT_EVIDENCE · arXiv 2309.06167 · abstract ABSTRACT_PRESENT
- **Article type:** REVIEW_SURVEY
- **Scenario:** `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `hpc_qpu_integration`, `hybrid_workflow`, `quantum_runtime_orchestration`
- **Gate 1 — classical systems problem:** How a QPU is integrated into an existing HPC infrastructure as an accelerator: programming models, runtime and resource-management layers, scheduling and workflow interfaces.
- **Gate 2 — HPC/systems technique:** Systematic review of quantum programming tools evaluated explicitly against HPC integration requirements (accelerator model, job submission, hybrid execution, software-stack layering).
- **Gate 3 — heterogeneous relevance:** This is the survey that defines the HPC-QPU integration problem statement for the rest of the corpus.
- **Key claim + baseline:** No performance claim; produces a classification of programming tools against HPC-integration criteria.
- **Evaluation platform:** Literature and tool survey.
- **Artifact status:** NO_PUBLIC_ARTIFACT_FOUND
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2309.06167; no conference version identified.
- **Deep-dive priority:** HIGH
- **Notes:** BIBLIOGRAPHY_HUB. TUM/LRZ-affiliated, 12 authors. Does not count toward the original-research population but is the single best entry point for the Q_IN_HPC branch in this venue.
- **Tag:** BIBLIOGRAPHY_HUB

#### TQC-051 — Lazy Qubit Reordering for Accelerating Parallel State-Vector-based Quantum Circuit Simulation

- **DOI** `10.1145/3748261` · **census year** 2025 · **v6 i4 pp1-33** · online 2025-07-12 · issue 2025-12-31
- **Lead author** Yusuke Teranishi (+4) · institution INSUFFICIENT_EVIDENCE · arXiv 2410.04252 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `distributed_gpu_simulation`
- **Gate 1 — classical systems problem:** All-to-all communication generated by qubit reordering dominates the cost of multi-GPU state-vector simulation; the problem is communication aggregation and scheduling, not quantum physics.
- **Gate 2 — HPC/systems technique:** Two operation-scheduling methods: an out-of-order approach that delays and aggregates reordering communications, and a time-space-tiling (cache-blocking) arrangement of gate execution order; plus a cluster-topology-aware optimization.
- **Gate 3 — heterogeneous relevance:** A direct transfer of classical cache-blocking and communication-aggregation technique into the quantum simulation kernel; exemplary HPC_FOR_Q work.
- **Key claim + baseline:** Up to 54x for quantum state update and up to 606x for expectation-value computation over existing methods, on 32-GPU executions; up to 15% communication reduction in two-layered cluster systems (preprint arXiv:2410.04252). Baseline is stated as 'existing methods' and is not fully specified, so the 606x figure should be treated as BASELINE_UNCLEAR.
- **Evaluation platform:** 32-GPU multi-node execution; VQE-oriented simulation workloads.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** HIGH
- **Notes:** One of the clearest pure-HPC contributions in the TQC population.

#### TQC-054 — DQC-QR: Distributing and Routing Quantum Circuits with Minimum Execution Time

- **DOI** `10.1145/3757069` · **census year** 2025 · **v6 i4 pp1-26** · online 2025-07-30 · issue 2025-12-31
- **Lead author** Ranjani Sundaram (+2) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `multi_qpu_distributed_qc`, `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Minimizing wall-clock execution time of a circuit distributed over a network of QPUs, where entanglement generation latency competes with qubit decoherence; joint qubit-to-memory mapping and remote-gate routing.
- **Gate 2 — HPC/systems technique:** Formulation and algorithms for the combined mapping/routing/scheduling problem with execution time as the objective, treating entanglement links as a latency-bounded interconnect resource.
- **Gate 3 — heterogeneous relevance:** Models a multi-QPU system as a latency-constrained distributed machine, which is the form a multi-node quantum resource in an HPC centre would take.
- **Key claim + baseline:** Claims lower execution time than prior distribution schemes; specific factors not in the abstract, BASELINE = prior circuit-distribution/partitioning heuristics.
- **Evaluation platform:** Quantum network simulation over benchmark circuits; INSUFFICIENT_EVIDENCE on scale.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** HIGH
- **Notes:** Distinguishable from the excluded entanglement-routing papers (e.g. TQC-080) because the objective is circuit execution time, not network key/entanglement distribution.

#### TQC-057 — Simulation of Quantum Computers: Review and Acceleration Opportunities

- **DOI** `10.1145/3762672` · **census year** 2025 · **v7 i1 pp1-35** · online 2025-09-11 · issue 2026-3-31
- **Lead author** Alessio Cicero (+4) · institution INSUFFICIENT_EVIDENCE · arXiv 2410.12660 · abstract ABSTRACT_PRESENT
- **Article type:** REVIEW_SURVEY
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `distributed_gpu_simulation`, `classical_simulation_engine`, `benchmarking_performance_modeling`
- **Gate 1 — classical systems problem:** Compute and memory demands of classical quantum-computer simulation, and where acceleration (CPU vectorization, GPU, FPGA, distributed memory) can be applied.
- **Gate 2 — HPC/systems technique:** Review of simulation methods (state vector, tensor network, decision diagram) organized by their computational and memory characteristics, with an explicit acceleration-opportunity analysis.
- **Gate 3 — heterogeneous relevance:** Maps the simulation workload onto classical accelerator options, informing what a quantum-simulation service on an HPC system should look like.
- **Key claim + baseline:** No single performance claim; a structured analysis of acceleration opportunities.
- **Evaluation platform:** Literature survey with method-level cost analysis.
- **Artifact status:** NO_PUBLIC_ARTIFACT_FOUND
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2410.12660.
- **Deep-dive priority:** HIGH
- **Notes:** BIBLIOGRAPHY_HUB. Best survey anchor for the simulation branch; pairs with TQC-064 (emulator benchmarking) and TQC-048 (integration tooling).
- **Tag:** BIBLIOGRAPHY_HUB

#### TQC-064 — Comparative Benchmarking of Utility-Scale Quantum Emulators

- **DOI** `10.1145/3776567` · **census year** 2025 · **v7 i2 pp1-29** · online 2025-11-18 · issue 2026-6-30
- **Lead author** Anna Leonteva (+4) · institution INSUFFICIENT_EVIDENCE · arXiv 2504.14027 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `benchmarking_performance_modeling`, `classical_simulation_engine`
- **Gate 1 — classical systems problem:** Which classical emulator technology can carry utility-scale circuits (100 to 1024 qubits) within practical CPU time and memory, and where each method fails.
- **Gate 2 — HPC/systems technique:** Controlled cross-emulator benchmarking of seven simulators spanning tensor networks, MPS, decision diagrams and factorized-ket representations, on CPU hardware, across 13 MQTBench circuits and sizes 4 to 1024 qubits.
- **Gate 3 — heterogeneous relevance:** Gives an empirical capability envelope for the classical side of quantum workflows; directly usable for provisioning simulation capacity at an HPC site.
- **Key claim + baseline:** MPS-based emulators outperform the other approaches overall, solving 8 of 13 benchmarks up to 1024 qubits; comparison is emulator-versus-emulator on identical circuits and CPU hardware, which is a clean baseline.
- **Evaluation platform:** CPU-based hardware; 13 MQTBench circuits, 4 to 1024 qubits; seven emulators.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2504.14027.
- **Deep-dive priority:** HIGH
- **Notes:** Rare head-to-head simulator study in this venue; a good empirical counterweight to the survey TQC-057.

#### TQC-070 — Fast Algorithms and Implementations for Computing the Minimum Distance of Quantum Codes

- **DOI** `10.1145/3795877` · **census year** 2026 · **v7 i2 pp1-19** · online 2026-4-2 · issue 2026-6-30
- **Lead author** Fernando Hernando (+2) · institution INSUFFICIENT_EVIDENCE · arXiv 2408.10743 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `qec_classical_processing`, `parallel_classical_kernel`
- **Gate 1 — classical systems problem:** Computing the symplectic minimum distance of a stabilizer code is an expensive classical combinatorial computation; the bottleneck is single-node and shared-memory compute time.
- **Gate 2 — HPC/systems technique:** Three algorithms derived from Brouwer-Zimmermann with implementations for single-core, multicore and shared-memory multiprocessor execution, with a scaling study.
- **Gate 3 — heterogeneous relevance:** A classical parallel-computing contribution whose consumer is QEC code design; a clean instance of HPC serving the quantum stack outside of simulation.
- **Key claim + baseline:** Reports more than one order of magnitude faster time than current state-of-the-art licensed implementations (Magma/GAP-class commercial tools) in the most computationally demanding cases, on single-core, multicore and shared-memory multiprocessors.
- **Evaluation platform:** Single-core, multicore and shared-memory multiprocessor systems.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** MEDIUM
- **Notes:** The most conventionally HPC paper in the TQC population by method (parallel combinatorial search, speedup versus licensed tools).

#### TQC-072 — Benchmarking fault-tolerant quantum computing hardware via QLOPS

- **DOI** `10.1145/3797968` · **census year** 2026 · **v7 i2 pp1-14** · online 2026-4-20 · issue 2026-6-30
- **Lead author** Linghang Kong (+2) · institution INSUFFICIENT_EVIDENCE · arXiv 2507.12024 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `FUTURE_WORKLOAD`, `HPC_FOR_Q`
- **Branch:** `benchmarking_performance_modeling`, `qec_classical_processing`
- **Gate 1 — classical systems problem:** No common framework exists for comparing fault-tolerant schemes across hardware platforms in throughput terms; QLOPS casts the question as logical operations per second, i.e. a rate metric.
- **Gate 2 — HPC/systems technique:** Definition and application of a throughput metric (Quantum Logical Operations Per Second) plus an evaluation framework that folds code distance, cycle time and resource overhead into a single performance figure.
- **Gate 3 — heterogeneous relevance:** A throughput metric is the language an HPC centre uses to size and schedule a resource; this makes FTQC schemes comparable in those terms.
- **Key claim + baseline:** Proposes QLOPS and applies it across FTQC schemes and hardware platforms; comparisons are between schemes under the new metric, so there is no external baseline.
- **Evaluation platform:** Analytical/resource-model evaluation across platform parameter sets.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2507.12024.
- **Deep-dive priority:** MEDIUM
- **Notes:** Performance-modelling inclusion; useful for the FUTURE_WORKLOAD scenario.

#### TQC-074 — QFOR: A Fidelity-aware Orchestrator for Quantum Computing Environments using Deep Reinforcement Learning

- **DOI** `10.1145/3799898` · **census year** 2026 · **Just Accepted** · online 2026-3-2 · issue —
- **Lead author** Hoa Nguyen (+2) · institution INSUFFICIENT_EVIDENCE · arXiv 2508.04974 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `Q_IN_HPC`, `HPC_FOR_Q`
- **Branch:** `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`
- **Gate 1 — classical systems problem:** Allocating and scheduling quantum tasks across heterogeneous, noisy quantum nodes in a cloud/datacentre setting, balancing execution fidelity against completion time under dynamic conditions.
- **Gate 2 — HPC/systems technique:** The orchestration problem is modelled as a Markov Decision Process and solved with Proximal Policy Optimisation; a learned scheduler replacing static heuristics.
- **Gate 3 — heterogeneous relevance:** This is resource management for a pool of QPUs, the layer an HPC batch system would either absorb or interface with.
- **Key claim + baseline:** 29.5% to 84% improvement in relative fidelity performance over heuristic baselines while maintaining comparable execution times (preprint arXiv:2508.04974). Baseline = heuristic schedulers; the range is wide and workload-dependent.
- **Evaluation platform:** Simulated quantum cloud environment with heterogeneous backend calibration data; INSUFFICIENT_EVIDENCE on real-device deployment.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** HIGH
- **Notes:** ACM Just Accepted (no volume/issue). One of very few genuine scheduling/resource-management papers in the TQC population.

#### TQC-082 — Tracking Affine Subspace with Gaussian Elimination for Adaptive Quantum Circuit Simulation

- **DOI** `10.1145/3815191` · **census year** 2026 · **v7 i4 pp1-22** · online 2026-8-10 · issue 2026-12-31
- **Lead author** Kisung Jin (+2) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `classical_simulation_engine`
- **Gate 1 — classical systems problem:** Sparse simulators win on memory when few basis states carry amplitude but lose on dense states; the systems problem is choosing a representation adaptively to control memory and runtime.
- **Gate 2 — HPC/systems technique:** Rapid pre-simulation sparsity prediction plus Gaussian elimination on linear constraints to track an affine subspace, switching representation adaptively.
- **Gate 3 — heterogeneous relevance:** Representation-adaptive simulation is a memory-management technique for the classical simulation service in a quantum software stack.
- **Key claim + baseline:** Claims retained sparse-simulator efficiency on sparse circuits without the degradation on dense circuits; BASELINE = fixed sparse and fixed state-vector simulators.
- **Evaluation platform:** Benchmark circuit suite on CPU; INSUFFICIENT_EVIDENCE on scale.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** No evidence located.
- **Deep-dive priority:** MEDIUM
- **Notes:** Simulation-engine inclusion; single-node, memory-focused.

#### TQC-089 — TREV: Python Library for Efficient Implementations of Variational Quantum Algorithms for Optimization using Tensor Networks

- **DOI** `10.1145/3821430` · **census year** 2026 · **Just Accepted** · online 2026-6-22 · issue —
- **Lead author** Keun Jun Park (+2) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `classical_simulation_engine`, `hybrid_workflow`
- **Gate 1 — classical systems problem:** Gradient evaluation by the parameter-shift rule dominates VQA simulation runtime, scaling with both parameter count and Hamiltonian term count; the cost is repeated classical contraction and sampling.
- **Gate 2 — HPC/systems technique:** TREV amortizes contraction and sampling across batched parameter-shift evaluations inside a tensor-ring state representation, i.e. batching and work reuse applied to the classical inner loop.
- **Gate 3 — heterogeneous relevance:** Targets the classical bottleneck of the hybrid loop, which is where CPU/GPU time is actually consumed in variational workloads.
- **Key claim + baseline:** Claims reduced VQA simulation runtime through batched parameter evaluation; quantitative factors not in the abstract, BASELINE = per-parameter sequential parameter-shift simulation.
- **Evaluation platform:** Python library; tensor-ring simulation of VQA circuits. INSUFFICIENT_EVIDENCE on hardware.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** ACM Just Accepted; no evidence located.
- **Deep-dive priority:** MEDIUM
- **Notes:** Included on the runtime-cost route despite the VQA subject matter: the contribution is the classical evaluation engine, not the ansatz or optimizer.

#### TQC-091 — Efficient Compilation for Shuttling Trapped-Ion Machines via the Position Graph Architectural Abstraction

- **DOI** `10.1145/3831246` · **census year** 2026 · **v7 i4 pp1-33** · online 2026-8-24 · issue 2026-12-31
- **Lead author** Bao Bach (+2) · institution INSUFFICIENT_EVIDENCE · arXiv 2501.12470 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `compiler_mapping_routing`, `architecture_control`
- **Gate 1 — classical systems problem:** Compilation for shuttling trapped-ion (QCCD) machines, where ion transport and trap-region occupancy dominate; scalable compilation across heterogeneous hardware layouts.
- **Gate 2 — HPC/systems technique:** A 'position graph' hardware abstraction that unifies several architecture families, enabling one scalable compilation method rather than per-architecture bespoke compilers.
- **Gate 3 — heterogeneous relevance:** An abstraction layer between compiler and hardware is exactly the portability mechanism a multi-vendor HPC-QPU software stack needs.
- **Key claim + baseline:** Claims higher-quality and scalable compilation for QCCD architectures versus existing trapped-ion compilation strategies; figures not in the abstract, BASELINE = prior QCCD compilers.
- **Evaluation platform:** Benchmark circuits over modelled QCCD architectures.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Preprint arXiv:2501.12470.
- **Deep-dive priority:** MEDIUM
- **Notes:** Architecture-abstraction angle makes this stronger than a pure routing heuristic.

#### TQC-092 — FlatDD: Parallel Quantum Circuit Simulation using Decision Diagram and Flat Array

- **DOI** `10.1145/3833216` · **census year** 2026 · **Just Accepted** · online 2026-7-21 · issue —
- **Lead author** Shui Jiang (+6) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`
- **Branch:** `classical_simulation_engine`, `distributed_gpu_simulation`
- **Gate 1 — classical systems problem:** Decision-diagram simulation is memory-efficient on regular circuits but incurs large runtime and memory overhead on irregular ones; pointer-chasing DD structures also parallelize poorly.
- **Gate 2 — HPC/systems technique:** FlatDD combines DD compression with a flat-array layout (data-layout transformation for locality) and parallelizes the simulation workload, a classical memory-layout plus parallelism contribution.
- **Gate 3 — heterogeneous relevance:** Improves the throughput and memory behaviour of a widely used simulator class; directly a classical-performance engineering result.
- **Key claim + baseline:** Claims combined advantage of DD-based and array-based simulation with parallel speedup; quantitative factors not in the published abstract, BASELINE = DD-only and array-only simulators.
- **Evaluation platform:** Parallel CPU execution; INSUFFICIENT_EVIDENCE on thread/GPU counts.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** ACM Just Accepted. Author group (Shui Jiang et al.) publishes DD/EDA work at design-automation venues; a conference predecessor is plausible but NOT confirmed.
- **Deep-dive priority:** HIGH
- **Notes:** Data-layout and parallelism argument makes this one of the stronger simulation entries in the 2026 cohort.

#### TQC-094 — QASMTrans: An End-to-End QASM Compilation Framework with Pulse Generation for Near-Term Quantum Devices

- **DOI** `10.1145/3837861` · **census year** 2026 · **Just Accepted** · online 2026-8-5 · issue —
- **Lead author** Aaron Hoyt (+10) · institution INSUFFICIENT_EVIDENCE · arXiv 2602.05154 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `Q_IN_HPC`
- **Branch:** `compiler_mapping_routing`, `architecture_control`, `hpc_qpu_integration`
- **Gate 1 — classical systems problem:** Transpilation latency on the critical path of QPU testbed operation: just-in-time compilation must complete fast enough for closed-loop control on systems with tightly coupled FPGAs/CPUs.
- **Gate 2 — HPC/systems technique:** A self-contained C++ compiler with no external dependencies, engineered for compile-time performance, plus end-to-end lowering to device pulses and direct integration with the QICK control framework.
- **Gate 3 — heterogeneous relevance:** This is the clearest HPC-QPU integration artifact in the TQC population: classical compile latency, control-plane coupling and closed-loop operation in one pipeline.
- **Key claim + baseline:** Published abstract: more than 10x faster compilation than Qiskit on some circuits with similar circuit quality; the preprint states more than 100x on some circuits and up to 12% fidelity improvement from pulse-level optimization. BASELINE = Qiskit transpiler. The two figures differ, so record both and treat the magnitude as circuit-dependent.
- **Evaluation platform:** C++ implementation; QPU testbeds with integrated FPGAs/CPUs; QICK control integration.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** RELATED_LINEAGE
- **Lineage evidence:** arXiv:2602.05154 carries an explicit note of substantial text overlap with arXiv:2308.07581, the earlier QASMTrans transpiler paper. That is documented lineage but not an explicit 'extended version of' statement for a named conference, so it is recorded as RELATED_LINEAGE rather than CONFIRMED_EXTENSION.
- **Deep-dive priority:** HIGH
- **Notes:** PNNL/ORNL authorship (Ang Li, Travis Humble). ACM Just Accepted.

#### TQC-095 — How Many Shots Are Enough for a Quantum Circuit?

- **DOI** `10.1145/3841468` · **census year** 2026 · **Just Accepted** · online 2026-8-20 · issue —
- **Lead author** Giuseppe Bisicchia (+3) · institution INSUFFICIENT_EVIDENCE · arXiv 2606.16965 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `Q_IN_HPC`
- **Branch:** `quantum_runtime_orchestration`, `benchmarking_performance_modeling`
- **Gate 1 — classical systems problem:** Shot count is the unit of QPU resource consumption and cost; deciding online when to stop sampling is a runtime resource-allocation decision made without knowledge of the circuit or noise model.
- **Gate 2 — HPC/systems technique:** IncrementalExecution, an online stopping framework driven by a diminishing-returns criterion on the estimated distribution, operating as a black-box runtime policy.
- **Gate 3 — heterogeneous relevance:** Shot budgeting is the throughput and cost knob for QPU access in a shared facility; a black-box policy is portable across backends.
- **Key claim + baseline:** Claims reduced shot consumption at a target accuracy versus fixed-shot execution; quantitative factors not in the abstract, BASELINE = fixed shot budgets.
- **Evaluation platform:** Simulated and/or cloud backends; INSUFFICIENT_EVIDENCE on specifics.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** ACM Just Accepted; preprint arXiv:2606.16965.
- **Deep-dive priority:** MEDIUM
- **Notes:** Matches the shot/measurement-orchestration include shape in the criteria.

## 4. Full records — TACO INCLUDED (4)

#### TACO-001 — QuCloud+: A Holistic Qubit Mapping Scheme for Single/Multi-programming on 2D/3D NISQ Quantum Computers

- **DOI** `10.1145/3631525` · **census year** 2024 · **v21 i1 pp1-27** · online 2024-1-18 · issue 2024-3-31
- **Lead author** Lei Liu (+1) · institution INSUFFICIENT_EVIDENCE · arXiv 2207.14483 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `Q_IN_HPC`
- **Branch:** `qpu_scheduling_resource_mgmt`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Qubit-resource utilization on a shared quantum device: partitioning physical qubits between concurrently running programs, allocating regions under crosstalk constraints, and handling 2D and 3D chip topologies with one mechanism.
- **Gate 2 — HPC/systems technique:** Multiprogramming resource partitioning by crosstalk-aware community detection, followed by topology-aware allocation and mapping. This is space-sharing of an accelerator, the same problem shape as multi-tenant GPU partitioning.
- **Gate 3 — heterogeneous relevance:** Device utilization and throughput under multi-tenancy is exactly the resource-management question an HPC centre faces when a QPU becomes a shared resource.
- **Key claim + baseline:** Claims improved fidelity and qubit-resource utilization for single and multi-programming workloads versus prior mapping schemes; BASELINE = existing qubit mapping and multi-programming schemes, including the authors' earlier QuCloud.
- **Evaluation platform:** Simulation plus IBM device coupling maps with 2D and 3D topologies.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** RELATED_LINEAGE
- **Lineage evidence:** The 'plus' naming and shared lead author point to QuCloud (HPCA 2021, Liu and Dou) as the predecessor, and arXiv:2207.14483 carries the QuCloud+ title. The arXiv listing contains no explicit 'extended version of' statement, so this is recorded as RELATED_LINEAGE, not CONFIRMED_EXTENSION.
- **Deep-dive priority:** HIGH
- **Notes:** The strongest multi-tenancy/resource-management paper across both journals.

#### TACO-006 — LarQucut: A New Cutting and Mapping Approach for Large-sized Quantum Circuits in Distributed Quantum Computing (DQC) Environments

- **DOI** `10.1145/3730585` · **census year** 2025 · **v22 i3 pp1-24** · online 2025-04-18 · issue 2025-9-30
- **Lead author** Xinglei Dou (+3) · institution INSUFFICIENT_EVIDENCE · arXiv 2502.21000 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD`
- **Branch:** `circuit_cutting_reconstruction`, `multi_qpu_distributed_qc`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Cutting and mapping a circuit that exceeds any single QPU across a set of heterogeneous QPUs, where the number of cuts drives classical reconstruction cost and the mapping drives communication overhead.
- **Gate 2 — HPC/systems technique:** Cutting strategy that reduces cut count and deliberately avoids fully independent sub-circuits, plus isomorphic sub-circuit detection so that mapping work is reused across identical fragments - a classical work-reuse and partitioning contribution.
- **Gate 3 — heterogeneous relevance:** Circuit cutting is the mechanism by which a large workload is decomposed across a pool of smaller accelerators; the cost model is classical reconstruction plus inter-QPU communication.
- **Key claim + baseline:** Claims fewer cuts and lower overall cutting plus computing overhead than prior cutting approaches, with better mapping for diverse QPUs; BASELINE = existing circuit-cutting and DQC mapping methods.
- **Evaluation platform:** Simulated DQC environment with heterogeneous QPUs; preprint arXiv:2502.21000.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** Same group as TACO-001 (Xinglei Dou is a QuCloud co-author). No explicit conference predecessor located for LarQucut.
- **Deep-dive priority:** HIGH
- **Notes:** —

#### TACO-007 — Ecmas+: Efficient Circuit Mapping and Scheduling for Surface Code Encoded Circuit on Quantum Cloud Platform

- **DOI** `10.1145/3760783` · **census year** 2025 · **v22 i3 pp1-25** · online 2025-08-20 · issue 2025-9-30
- **Lead author** Mingzheng Zhu (+6) · institution INSUFFICIENT_EVIDENCE · arXiv — · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `Q_IN_HPC`
- **Branch:** `compiler_mapping_routing`, `qpu_scheduling_resource_mgmt`, `qec_classical_processing`
- **Gate 1 — classical systems problem:** Space-time cost of executing surface-code-encoded circuits determines the throughput of a shared quantum cloud platform; circuits differ in how much chip parallelism they can exploit, so the compiler must decide how much space to spend to buy time.
- **Gate 2 — HPC/systems technique:** A Circuit Parallelism Degree metric characterizing exploitable parallelism, used to drive joint mapping and scheduling of surface-code operations with an explicit space-time trade-off and platform-throughput objective.
- **Gate 3 — heterogeneous relevance:** Framing compilation as a throughput problem for a shared platform is precisely the systems framing this census tracks.
- **Key claim + baseline:** Claims reduced space-time cost and higher platform throughput relative to prior surface-code compilation; BASELINE = existing surface-code mapping and scheduling approaches.
- **Evaluation platform:** Surface-code compilation experiments over benchmark circuits and chip models.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** RELATED_LINEAGE
- **Lineage evidence:** The 'plus' naming indicates a predecessor named Ecmas by the same group (Mingzheng Zhu et al.). No explicit extension statement could be retrieved - the ACM page returned HTTP 403 on two attempts - so this stays RELATED_LINEAGE.
- **Deep-dive priority:** HIGH
- **Notes:** The only paper across both journals that ties QEC compilation directly to platform throughput.

#### TACO-009 — A System Architecture for Low Latency Multiprogramming Quantum Computing

- **DOI** `10.1145/3845611` · **census year** 2026 · **Just Accepted** · online 2026-09-07 · issue —
- **Lead author** Yilun Zhao (+6) · institution INSUFFICIENT_EVIDENCE · arXiv 2601.01158 · abstract ABSTRACT_PRESENT
- **Article type:** ORIGINAL_RESEARCH
- **Scenario:** `HPC_FOR_Q`, `Q_IN_HPC`, `FUTURE_WORKLOAD`
- **Branch:** `qpu_scheduling_resource_mgmt`, `quantum_runtime_orchestration`, `compiler_mapping_routing`
- **Gate 1 — classical systems problem:** Online compilation dominates the runtime of multiprogramming quantum systems because executables are device- and region-dependent, which blocks low-latency repeated invocation of quantum services.
- **Gate 2 — HPC/systems technique:** FLAMENCO moves compilation offline and keeps multiple pre-compiled versions per program: the device is abstracted into compute units, diverse executable versions are generated ahead of time for different qubit regions, and a runtime orchestrator selects among them using fidelity metrics. This is classical multi-versioning plus runtime dispatch, a standard systems pattern.
- **Gate 3 — heterogeneous relevance:** Separating a slow offline compile from a fast online dispatch is how accelerator services are built in classical systems; this is the clearest transfer of that pattern into QPU serving.
- **Key claim + baseline:** Over 5x runtime speedup with improved execution fidelity (preprint arXiv:2601.01158). BASELINE = online co-compilation pipelines for multiprogramming quantum computing, which is the right comparator.
- **Evaluation platform:** Multiprogramming workloads including repeatedly invoked QNN services; INSUFFICIENT_EVIDENCE on device versus simulation split.
- **Artifact status:** UNKNOWN
- **Artifact URL:** —
- **Conference extension:** UNKNOWN
- **Lineage evidence:** ACM Just Accepted; no predecessor located.
- **Deep-dive priority:** HIGH
- **Notes:** Strongest runtime/serving-architecture paper in the TACO pool.

## 5. BORDERLINE section

An independent adversarial verification pass proposed five demotions from INCLUDED. Four were accepted outright (TQC-035, TQC-066, TQC-077, TQC-016), one was accepted on cross-journal consistency grounds (TQC-059, aligned with FGCS-063, which measures embedding runtime and is itself BORDERLINE), and one was declined with a written rebuttal (TQC-022, retained as INCLUDED; the rebuttal is in its notes field in section 3). Demoted records carry `adjudication: DEMOTED_BY_VERIFICATION_PASS` in the JSON.

TQC: 17 records. TACO: 0. These are recorded, not discarded, and are not counted in the included population.

#### TQC-001 — Efficient Syndrome Decoder for Heavy Hexagonal QECC via Machine Learning

- **DOI** `10.1145/3636516` · 2024 · v5 i1 pp1-27 · online 2024-2-24 · lead author Debasmita Bhoumik (+5) · arXiv 2210.09730
- **Branch:** `qec_classical_processing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Decoding is explicitly in scope, and the criteria list a new decoder algorithm as BORDERLINE.
- **Reasons AGAINST inclusion:** The reported metric is threshold/accuracy; there is no parallelism, latency budget or accelerator mapping, which is what would move it to INCLUDED.
- **Gate 1:** Syndrome decoding is the real-time classical computation inside the QEC loop; this work replaces MWPM with a neural decoder.
- **Gate 2:** Machine-learning decoder plus a subsystem-code decomposition that reduces the decoding problem size.
- **Key claim + baseline:** About 5x higher threshold than MWPM for heavy-hex code under the studied noise models. BASELINE = MWPM decoding accuracy, not decoding latency.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2210.09730.)
- **Notes:** Kept as the reference case for the 'decoder algorithm only' BORDERLINE rule.

#### TQC-014 — Quantum Circuit Cutting for Classical Shadows

- **DOI** `10.1145/3665335` · 2024 · v5 i2 pp1-21 · online 2024-05-21 · lead author Daniel Tzu Shiuan Chen (+2) · arXiv 2212.00761
- **Branch:** `circuit_cutting_reconstruction` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Circuit-cutting reconstruction cost is a listed include shape.
- **Reasons AGAINST inclusion:** The cost currency is samples/shots and estimator variance, not classical runtime, memory or parallel reconstruction; no systems implementation.
- **Gate 1:** Classical reconstruction cost after circuit cutting, expressed as sample complexity for predicting observables from fragment shadows.
- **Gate 2:** Divide-and-conquer reconstruction formula for classical shadows of arbitrarily cut circuits, with sample-complexity analysis when observables factorize across fragments.
- **Key claim + baseline:** Reports reduced sample requirements versus non-factorized reconstruction in the numerical study; BASELINE = standard classical-shadow estimation on the uncut circuit.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2212.00761.)

#### TQC-016 — Efficient Quantum Circuit Design with a Standard Cell Approach, with an Application to Neutral Atom Quantum Computers

- **DOI** `10.1145/3670417` · 2024 · v6 i1 pp1-18 · online 2024-06-08 · lead author Evan Dobbs (+2) · arXiv 2206.04990
- **Branch:** `compiler_mapping_routing`, `architecture_control` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** The standard-cell abstraction plus layout-aware routing for zoned neutral-atom architectures is architecture-aware mapping, and separating memory, processing and measurement zones is a structural systems idea.
- **Reasons AGAINST inclusion:** Gate 2 is a methodological analogy to VLSI standard cells; the layout speed-up is recorded BASELINE_UNCLEAR and the reported outputs are circuit layouts and space-time volume, which are quantum resources. My own deep-dive priority was already LOW.
- **Gate 1:** Layout and routing cost for circuits on zoned neutral-atom architectures with qubit shuttling; layout time for regular circuit structures.
- **Gate 2:** Standard-cell methodology imported from classical VLSI/EDA, enabling layout-aware routing algorithms and separation of memory / processing / measurement zones.
- **Key claim + baseline:** Claims speed-up of layout for regularly structured circuits and applicability to neutral-atom shuttling machines; BASELINE_UNCLEAR (no quantified comparator in the abstract).
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located.)
- **Notes:** Included on the architecture-aware-mapping route; the systems argument is methodological (EDA abstraction) rather than measured. DEMOTED INCLUDED -> BORDERLINE by adjudication. Included originally on the architecture-aware-mapping route, but with no measured classical cost the record does not clear Gate 2 as written.

#### TQC-023 — Utilizing classical programming principles in the Intel Quantum SDK: implementation of quantum lattice Boltzmann method

- **DOI** `10.1145/3678185` · 2024 · v6 i1 pp1-18 · online 2024-07-17 · lead author Tejas Shinde (+5) · arXiv 2407.04311
- **Branch:** `scientific_workflow_application` · **Scenario:** `Q_FOR_HPC`, `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Q_FOR_HPC workload plus explicit engagement with a production quantum SDK.
- **Reasons AGAINST inclusion:** No runtime, memory, scaling or orchestration result; the quantum algorithm is the object of study.
- **Gate 1:** Structuring a quantum implementation of an HPC kernel (lattice Boltzmann) using classical software-engineering practice - modularization, controlled execution of complex algorithms - inside a vendor SDK.
- **Gate 2:** Classical programming principles applied within the Intel Quantum SDK; execution on the SDK state-vector simulator.
- **Key claim + baseline:** No performance comparison against a classical LBM solver is claimed; BASELINE_UNCLEAR.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2407.03970.)

#### TQC-027 — A Model-Driven Framework for Composition-Based Quantum Circuit Design

- **DOI** `10.1145/3688856` · 2024 · v5 i4 pp1-36 · online 2024-08-21 · lead author Felix Gemeinhardt (+3) · arXiv —
- **Branch:** `quantum_software_engineering` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Software stack is an explicit Gate 3 target.
- **Reasons AGAINST inclusion:** Gate 1 is not met: no computation cost, memory, communication or runtime quantity appears.
- **Gate 1:** Development effort and abstraction level in quantum circuit construction; composing circuits from higher-level reusable components.
- **Gate 2:** Model-driven engineering: a modeling language plus a design framework with composition semantics for circuits.
- **Key claim + baseline:** Claims reduced development effort and lower entry barrier; no quantitative systems baseline.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located.)
- **Notes:** Recorded as part of a small quantum-software-engineering cluster in TQC (with TQC-047 and TQC-081).

#### TQC-035 — What Quantum Can Learn from Classical Computer Engineering

- **DOI** `10.1145/3705007` · 2025 · v6 i1 pp1-6 · online 2025-01-14 · lead author Anne Y. Matsuura (+1) · arXiv —
- **Branch:** `benchmarking_performance_modeling` · **Scenario:** `FUTURE_WORKLOAD`, `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** The special issue it introduces is explicitly about importing classical computer-engineering practice into quantum system design, and it frames co-design and the multi-core concept; it remains the clearest venue-level signal that TQC hosts classical-systems work (TQC-009 sits in this issue).
- **Reasons AGAINST inclusion:** Gate 2 fails on my own wording: the contribution is editorial framing, not an HPC/systems/architecture technique. Verifier is correct. Retained as BIBLIOGRAPHY_HUB; article type SPECIAL_ISSUE_INTRO means the original-research count is unaffected.
- **Gate 1:** Frames the transfer of classical computer-engineering practice (hardware/software co-design, the multi-core concept, application-developer requirement capture) into quantum system design.
- **Gate 2:** Editorial framing rather than a technique; introduces a special issue whose theme is exactly the classical-systems-into-quantum direction this census tracks.
- **Key claim + baseline:** No empirical claim (editorial).
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (N/A)
- **Notes:** BIBLIOGRAPHY_HUB. Six pages, Intel Labs authorship. Does NOT count toward the original-research included population, but it is the strongest venue-level signal that TQC deliberately hosts classical-systems-flavoured quantum work (TQC-009 sits in this special issue). DEMOTED INCLUDED -> BORDERLINE by adjudication of the verification pass. My own Gate 2 text ('editorial framing rather than a technique') is a stated Gate 2 failure, so the verdict was inconsistent with the record's own analysis. BIBLIOGRAPHY_HUB retained.

#### TQC-041 — Algorithmic Theory of Qubit Routing in the Linear Nearest Neighbor Architectures

- **DOI** `10.1145/3722119` · 2025 · v6 i3 pp1-17 · online 2025-03-08 · lead author Takehiro Ito (+4) · arXiv —
- **Branch:** `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Compilation cost is an explicit Gate 1 quantity and this paper is entirely about it.
- **Reasons AGAINST inclusion:** Gate 2 asks for a systems/architecture technique; the method is combinatorial complexity theory with no implementation or measurement.
- **Gate 1:** The classical computational complexity of the qubit routing (SWAP minimization) step performed by every quantum compiler.
- **Gate 2:** NP-hardness proof for routing on a path, a fixed-parameter-tractable algorithm parameterized by two-qubit gate count, and further algorithmic results for LNN architectures.
- **Key claim + baseline:** Complexity results; no empirical baseline.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located.)

#### TQC-044 — Approximate Quantum Compiling for Quantum Simulation: A Tensor Network Based Approach

- **DOI** `10.1145/3731251` · 2025 · v6 i3 pp1-15 · online 2025-04-18 · lead author Niall Robertson (+3) · arXiv 2301.08609
- **Branch:** `classical_simulation_engine`, `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Classical tensor-network compute serving compilation, with an explicit criticism of prior methods' optimization behaviour.
- **Reasons AGAINST inclusion:** No reported runtime, memory or parallel-scaling measurement; the deliverable is circuit depth for state preparation.
- **Gate 1:** Classical optimization cost of approximate quantum compiling from matrix product states; prior methods sweep locally over parameter subsets, which is slow and gets stuck.
- **Gate 2:** Whole-circuit parametric optimization using tensor-network (MPS) structure, with an optimization scheme to avoid poor initialization.
- **Key claim + baseline:** Claims better circuits and better-behaved optimization than sweeping MPS-to-circuit methods; BASELINE = local/sweeping AQC approaches.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2301.08609.)

#### TQC-045 — Line-Graph Qubit Routing

- **DOI** `10.1145/3733842` · 2025 · v6 i3 pp1-18 · online 2025-05-02 · lead author Joris Kattemölle (+1) · arXiv —
- **Branch:** `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Architecture-aware mapping for a named hardware family.
- **Reasons AGAINST inclusion:** The reported metric is circuit overhead, not compile-time scalability or a systems cost; criteria place gate-count/fidelity-only compilation at BORDERLINE.
- **Gate 1:** Routing circuits whose interaction graph is a line graph onto heavy coupling graphs, exploiting structure instead of running general-purpose search.
- **Gate 2:** Structure-exploiting deterministic routing construction, benchmarked against general-purpose routers.
- **Key claim + baseline:** Reports outperforming established general-purpose routing methods on kagome/checkerboard/shuriken lattices mapped to heavy-hex, heavy-square and heavy-square-octagon hardware; BASELINE = general-purpose routers, metric is circuit quality.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located.)

#### TQC-047 — QuL: Programming Library for Computational Cooling of Qubits

- **DOI** `10.1145/3737887` · 2025 · v6 i3 pp1-29 · online 2025-05-29 · lead author Giuliano Difranco (+1) · arXiv 2410.13380
- **Branch:** `quantum_software_engineering`, `architecture_control` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Software-stack artifact in the control layer.
- **Reasons AGAINST inclusion:** Gate 1 is not met; the subject is a cooling protocol, which is closer to device operation than to classical systems.
- **Gate 1:** Tooling to generate, analyze and test circuits for computational-cooling protocols, i.e. a programming library in the control/initialization layer.
- **Gate 2:** A programming library with layered interfaces (novice default path, expert-configurable protocol construction).
- **Key claim + baseline:** No performance baseline stated.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2410.13380.)

#### TQC-059 — CHARME: A Chain-based Reinforcement Learning Approach for the Minor Embedding Problem

- **DOI** `10.1145/3763244` · 2025 · v7 i1 pp1-28 · online 2025-10-24 · lead author Hoang Ngo (+5) · arXiv 2406.07124
- **Branch:** `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Scalability of the embedding computation is named as the motivation, and minor embedding is the annealer analogue of a compile stage.
- **Reasons AGAINST inclusion:** The scalability claim is motivational; the evaluated quantities are embedding quality and chain structure, not embedding runtime or memory. Decisive point is cross-journal consistency: FGCS-063 addresses the same minor-embedding problem in the same census window, actually measures embedding execution time, and is still held at BORDERLINE because the platform is an annealer and the contribution is not a systems mechanism. CHARME presents weaker classical-cost evidence than FGCS-063, so it cannot sit higher.
- **Gate 1:** Scalability of the classical minor-embedding computation: existing embedding heuristics degrade as problem graph size grows, and embedding is an NP-hard preprocessing step in the job pipeline.
- **Gate 2:** Reinforcement-learning agent (CHARME) constructing chains for minor embedding, aimed at keeping embedding tractable at larger sizes rather than at improving anneal quality alone.
- **Key claim + baseline:** Claims better scaling behaviour and embedding quality than established heuristic embedders (minorminer-class); precise figures not in the abstract.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located. Same author group as TQC-063 (FIDDLE).)
- **Notes:** Included on the scalable-mapping route; the annealing context makes it a weaker fit than gate-model mapping work. DEMOTED INCLUDED -> BORDERLINE by adjudication, primarily for consistency with FGCS-063 (10.1016/j.future.2026.108481), which measures embedding runtime and is BORDERLINE. Correct DOI for this record is 10.1145/3763244; the verification pass cited 10.1145/3718348, which belongs to TQC-038 (Zylberman, diagonal operators, EXCLUDED).

#### TQC-063 — FIDDLE: Reinforcement Learning for Quantum Fidelity Enhancement

- **DOI** `10.1145/3773909` · 2025 · v7 i1 pp1-28 · online 2025-10-29 · lead author Hoang M. Ngo (+2) · arXiv 2510.15833
- **Branch:** `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Compiler-stage contribution with a learned classical component and an explicit surrogate-cost argument.
- **Reasons AGAINST inclusion:** The optimization target is output fidelity, which the criteria place at BORDERLINE or EXCLUDE; no compile-time or scaling result.
- **Gate 1:** Choosing routing decisions during transpilation to maximize process fidelity, with a surrogate model to avoid expensive fidelity evaluation.
- **Gate 2:** Gaussian-process surrogate plus reinforcement learning in the routing stage of the compiler.
- **Key claim + baseline:** Claims higher process fidelity than existing routing approaches; BASELINE = fidelity-unaware and heuristic routers, metric is fidelity.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2510.15833. Same group as TQC-059 (CHARME).)
- **Notes:** Contrast with TQC-059 by the same group, which is included because its argument is embedding scalability.

#### TQC-066 — qSIEVE: Efficient qLDPC Memory via Systolic Movement in Atom Arrays

- **DOI** `10.1145/3779066` · 2025 · v7 i2 pp1-26 · online 2025-12-12 · lead author Joshua Viszlai (+6) · arXiv 2311.16980
- **Branch:** `architecture_control`, `qec_classical_processing` · **Scenario:** `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **Priority:** MEDIUM
- **Reasons FOR inclusion:** Qubit movement in an atom array is a data-movement and movement-scheduling problem, and the systolic schedule is a genuine dataflow-regularity constraint rather than decoration.
- **Reasons AGAINST inclusion:** The only measured quantity is qubit overhead at a given logical error rate, which is a quantum resource. Gate 2 rests on an analogy to systolic dataflow with no classical latency, bandwidth, control-throughput or compute measurement attached. Under the rule that a quantum-resource-only measurement does not pass Gate 2, the verifier is correct.
- **Gate 1:** Non-local qLDPC codes require long-range interactions; on atom arrays these become physical qubit movement, i.e. a data-movement and movement-scheduling problem with a control cost.
- **Gate 2:** Systolic movement schedule (a classical systolic-array dataflow abstraction) for qLDPC memory in atom arrays, trading movement regularity against control complexity and overhead.
- **Key claim + baseline:** Claims reduced qubit overhead versus surface-code memory at comparable logical error rates, using structured movement instead of arbitrary connectivity; BASELINE = surface-code memory and prior atom-array qLDPC proposals.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2311.16980; the author group (Chicago/EPiQC lineage) publishes heavily at ISCA/ASPLOS/MICRO, so a conference version is plausible but NOT confirmed.)
- **Notes:** Architecture-side inclusion; the classical-systems content is the dataflow/movement-scheduling abstraction. DEMOTED INCLUDED -> BORDERLINE by adjudication. The architecture reading is defensible but unmeasured in classical-systems terms; it would move to INCLUDED if a control-plane cost, movement latency budget or classical scheduling result were reported.

#### TQC-073 — Quantum Backtracking in Qrisp Applied to Sudoku Problems

- **DOI** `10.1145/3799888` · 2026 · v7 i3 pp1-32 · online 2026-7-11 · lead author Raphael Seidel (+6) · arXiv 2402.10060
- **Branch:** `quantum_software_engineering` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Software-stack/framework evidence and concrete resource accounting.
- **Reasons AGAINST inclusion:** Fundamentally a quantum-algorithm implementation study; no classical runtime, memory or orchestration result.
- **Gate 1:** Implementability of quantum backtracking: the step operator and diffuser must be constructed concretely and compiled, with resource counts reported.
- **Gate 2:** Detailed implementation inside the Qrisp high-level quantum programming framework, with resource accounting for controlled diffusers on binary backtracking trees.
- **Key claim + baseline:** Reports gate/resource counts for the implemented step operator; BASELINE = the abstract algorithm specification, not another implementation.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2402.10060.)

#### TQC-075 — Unifying Communication Paradigms in Measurement-based Delegated Quantum Computing

- **DOI** `10.1145/3800578` · 2026 · v7 i3 pp1-19 · online 2026-4-23 · lead author Fabian Wiesner (+2) · arXiv 2506.21988
- **Branch:** `multi_qpu_distributed_qc` · **Scenario:** `FUTURE_WORKLOAD` · **Priority:** LOW
- **Reasons FOR inclusion:** Communication-paradigm comparison for delegated computation, i.e. offloading structure.
- **Reasons AGAINST inclusion:** The driving requirement is cryptographic blindness, placing it close to the excluded quantum-cryptography class; no computing-systems cost model.
- **Gate 1:** How preparation, entangling and measurement stages are split between a weak client and a quantum server, and what each split implies for the communication pattern.
- **Gate 2:** A unified account of the two client/server distribution paradigms in measurement-based delegated quantum computing, comparing their communication and capability requirements.
- **Key claim + baseline:** Unification result rather than a measured improvement; no systems baseline.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2506.21988.)

#### TQC-077 — It’s Quick to be Square: Fast Quadratisation for Quantum Toolchains

- **DOI** `10.1145/3800943` · 2026 · v7 i3 pp1-46 · online 2026-7-11 · lead author Lukas Schmidbauer (+3) · arXiv 2411.19934
- **Branch:** `compiler_mapping_routing` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Quadratisation is a classical transformation stage in the toolchain and the paper's framing is the cost of that stage rather than the quality of the resulting circuit, which is the distinction this census uses.
- **Reasons AGAINST inclusion:** The runtime advantage is asserted without figures and without a comparator named beyond 'prior quadratisation methods', so the classical cost argument that carried the inclusion is unverified in the available evidence. The downstream consumer is QUBO preparation for annealing and QAOA toolchains, adjacent to excluded classes.
- **Gate 1:** Quadratisation (transforming higher-order problem representations into quadratic form) is a classical preprocessing stage in quantum optimisation toolchains whose cost and output structure determine downstream circuit overhead.
- **Gate 2:** Fast quadratisation algorithms positioned as a toolchain transformation stage, with attention to the runtime of the transformation itself and to alignment between problem structure and target hardware structure.
- **Key claim + baseline:** Claims faster quadratisation than established transformation approaches while producing hardware-aligned representations; specific factors not in the abstract, BASELINE = prior quadratisation methods.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (Preprint arXiv:2411.19934.)
- **Notes:** Included because the cost argument is explicitly about the classical transformation stage, not about circuit quality alone. DEMOTED INCLUDED -> BORDERLINE by adjudication. The Gate 1 framing survives but the supporting measurement does not; verified compile-stage timings against a named baseline would restore INCLUDED.

#### TQC-081 — QuCheck: A Property-based Testing Framework for Quantum Programs in Qiskit

- **DOI** `10.1145/3815169` · 2026 · v7 i4 pp1-32 · online 2026-8-10 · lead author Gabriel Pontolillo (+2) · arXiv —
- **Branch:** `quantum_software_engineering` · **Scenario:** `HPC_FOR_Q` · **Priority:** LOW
- **Reasons FOR inclusion:** Classical software-engineering technique transferred into the quantum stack.
- **Reasons AGAINST inclusion:** NO_ABSTRACT, so Gate 1 cannot be verified; testing frameworks carry no execution-cost argument by default.
- **Gate 1:** Testing quantum programs: generating inputs and checking properties of Qiskit programs automatically.
- **Gate 2:** Property-based testing framework (a classical software-engineering technique) applied to quantum programs.
- **Key claim + baseline:** NO_ABSTRACT: no claim could be verified. INSUFFICIENT_EVIDENCE.
- **Artifact:** UNKNOWN · **Conference extension:** UNKNOWN (No evidence located.)
- **Notes:** Classified from title and venue metadata only; flagged NO_ABSTRACT.

## 6. False-positive logs

### TQC — 58 excluded (59.8% of records classified)

| Class | Count | Records |
|---|---|---|
| `FP7_ALGORITHMS_COMPLEXITY` | 21 | TQC-004, TQC-005, TQC-006, TQC-015, TQC-017, TQC-033, TQC-034, TQC-036, TQC-042, TQC-043, TQC-046, TQC-052, TQC-055, TQC-058, TQC-065, TQC-068, TQC-076, TQC-078, TQC-086, TQC-093, TQC-097 |
| `FP8_SYNTHESIS_GATECOUNT_ONLY` | 11 | TQC-002, TQC-011, TQC-018, TQC-020, TQC-031, TQC-038, TQC-049, TQC-050, TQC-053, TQC-069, TQC-085 |
| `FP9_VQA_ANSATZ_PARAMETERIZATION` | 5 | TQC-056, TQC-083, TQC-084, TQC-087, TQC-088 |
| `FP10_DEVICE_CHARACTERIZATION_ERROR_MITIGATION` | 4 | TQC-003, TQC-024, TQC-026, TQC-032 |
| `FP6_SENSING_DEVICE_PHYSICS` | 4 | TQC-008, TQC-028, TQC-060, TQC-071 |
| `FP14_QUANTUM_CRYPTOGRAPHY_PROTOCOLS` | 4 | TQC-039, TQC-040, TQC-062, TQC-096 |
| `FP5_QML_APPLICATIONS` | 3 | TQC-007, TQC-010, TQC-012 |
| `FP2_QUANTUM_INSPIRED_CLASSICAL` | 2 | TQC-013, TQC-079 |
| `FP11_PL_THEORY_FORMAL_METHODS` | 2 | TQC-061, TQC-090 |
| `FP12_VISUALIZATION_HCI` | 1 | TQC-067 |
| `FP4_QUANTUM_NETWORKING_QKD` | 1 | TQC-080 |

| ID | Year | DOI | Title | Type | Reason |
|---|---|---|---|---|---|
| TQC-002 | 2024 | `10.1145/3639062` | Optimal Hadamard Gate Count for Clifford+ T Synthesis of Pauli Rotations Sequences | ORIGINAL_RESEARCH | Clifford+T synthesis; objective is Hadamard/T gate count. No classical computation cost, parallelism or systems mechanism (Gate 1 & 2 fail). |
| TQC-003 | 2024 | `10.1145/3644823` | Quantum Measurement Classification Using Statistical Learning | ORIGINAL_RESEARCH | Statistical classification of readout values to discriminate measured states; device-level estimation quality, no runtime/throughput/scheduling mechanism (Gate 2 fails). |
| TQC-004 | 2024 | `10.1145/3648573` | Hybrid Quantum-classical Search Algorithms | ORIGINAL_RESEARCH | Query-complexity lower bounds for hybrid search; 'hybrid quantum-classical' here is a complexity model, not a computing system (vocabulary trap). |
| TQC-005 | 2024 | `10.1145/3649320` | An Optimal Linear-combination-of-unitaries-based Quantum Linear System Solver | ORIGINAL_RESEARCH | Quantum linear-system solver construction (QSVT/LCU); query/gate complexity only. |
| TQC-006 | 2024 | `10.1145/3655026` | On the Success Probability of Quantum Order Finding | ORIGINAL_RESEARCH | Success-probability analysis of Shor order finding; classical post-processing is arithmetic, not a systems contribution. |
| TQC-007 | 2024 | `10.1145/3655027` | A Characterization of Quantum Generative Models | ORIGINAL_RESEARCH | Comparative study of quantum generative model ansaetze and training methods. |
| TQC-008 | 2024 | `10.1145/3655028` | Optimizing Initial State of Detector Sensors in Quantum Sensor Networks | ORIGINAL_RESEARCH | Quantum sensor network state discrimination; sensing/metrology. |
| TQC-010 | 2024 | `10.1145/3660647` | Q-SupCon: Quantum-Enhanced Supervised Contrastive Learning Architecture within the Representation Learning Framework | ORIGINAL_RESEARCH | Quantum-enhanced supervised contrastive learning architecture; accuracy comparison on a classification task. |
| TQC-011 | 2024 | `10.1145/3663576` | Probabilistic Unitary Synthesis with Optimal Accuracy | ORIGINAL_RESEARCH | Bounds on approximation error/gate length for probabilistic unitary synthesis. |
| TQC-012 | 2024 | `10.1145/3663577` | Lessons from Twenty Years of Quantum Image Processing | REVIEW_SURVEY | Review of quantum image processing; application-domain retrospective with no classical-systems axis. |
| TQC-013 | 2024 | `10.1145/3665281` | Improving the exploitability of Simulated Adiabatic Bifurcation through a flexible and open-source digital architecture | ORIGINAL_RESEARCH | FPGA digital architecture emulating Simulated Adiabatic Bifurcation (Ising machine). Real classical-architecture content but the computation is quantum-inspired classical annealing, explicitly out of scope. |
| TQC-015 | 2024 | `10.1145/3670416` | Switching Time Optimization for Binary Quantum Optimal Control | ORIGINAL_RESEARCH | Binary quantum optimal control via continuous relaxation and rounding heuristics; classical numerical optimization without parallelism, memory or runtime-systems mechanism. |
| TQC-017 | 2024 | `10.1145/3670418` | Learning Quantum Processes and Hamiltonians via the Pauli Transfer Matrix | ORIGINAL_RESEARCH | Learning theory for quantum processes; 'quantum memory' is an information-theoretic resource, not a memory system (vocabulary trap). |
| TQC-018 | 2024 | `10.1145/3673240` | Synthesis Techniques for Fault-tolerant Quantum Circuit Implementation using Clifford+ Z N -group | ORIGINAL_RESEARCH | Fault-tolerant synthesis with Clifford+Z_N; phase-depth/gate-count bounds. |
| TQC-020 | 2024 | `10.1145/3673242` | An Algorithm for Reversible Logic Circuit Synthesis Based on Tensor Decomposition | ORIGINAL_RESEARCH | Reversible-logic synthesis by tensor decomposition; Toffoli-count objective. |
| TQC-024 | 2024 | `10.1145/3680290` | Increasing the Measured Effective Quantum Volume with Zero Noise Extrapolation | ORIGINAL_RESEARCH | Zero-noise extrapolation applied to the quantum volume protocol; error-mitigation effect on a device metric. |
| TQC-026 | 2024 | `10.1145/3682071` | Impact of Unreliable Devices on Stability of Quantum Computations | ORIGINAL_RESEARCH | Device stability/reliability bounds from characterization data; no classical execution mechanism. |
| TQC-028 | 2024 | `10.1145/3688857` | Overdispersion in Gate Tomography: Experiments and Continuous, Two-Scale Random Walk Model on the Bloch Sphere | ORIGINAL_RESEARCH | Random-walk noise model for gate tomography; device noise physics. |
| TQC-031 | 2024 | `10.1145/3700884` | Shallower CNOT Circuits on Realistic Quantum Hardware | ORIGINAL_RESEARCH | CNOT circuit depth upper bounds under limited connectivity; circuit-depth argument only. |
| TQC-032 | 2024 | `10.1145/3700885` | Scalable Experimental Bounds for Entangled Quantum State Fidelities | ORIGINAL_RESEARCH | Fidelity lower bounds for entangled states; measurement-setting sample complexity for characterization, not shot orchestration in an execution stack. |
| TQC-033 | 2024 | `10.1145/3702244` | Improvements to Quantum Interior Point Method for Linear Optimization | ORIGINAL_RESEARCH | Quantum interior point method variant; qubit/gate resource reduction for an algorithm. |
| TQC-034 | 2024 | `10.1145/3706064` | Multimarked Spatial Search by Continuous-Time Quantum Walk | ORIGINAL_RESEARCH | Continuous-time quantum walk spatial search complexity framework. |
| TQC-036 | 2025 | `10.1145/3711935` | Enhancing Quantum Algorithms for Quadratic Unconstrained Binary Optimization via Integer Programming | ORIGINAL_RESEARCH | QUBO decomposition with classical integer programming; algorithmic hybrid, no orchestration/runtime mechanism. |
| TQC-038 | 2025 | `10.1145/3718348` | Efficient Quantum Circuits for Non-Unitary and Unitary Diagonal Operators with Space-Time-Accuracy Trade-Offs | ORIGINAL_RESEARCH | Diagonal-operator circuit constructions; depth/ancilla/accuracy trade-off is a circuit-resource, not a systems, trade-off (vocabulary trap: 'space-time'). |
| TQC-039 | 2025 | `10.1145/3718349` | Hacking Cryptographic Protocols with Advanced Variational Quantum Attacks | ORIGINAL_RESEARCH | Variational quantum attacks on symmetric ciphers; quantum cryptanalysis. |
| TQC-040 | 2025 | `10.1145/3721487` | Non-Interactive and Non-Destructive Zero-Knowledge Proofs on Quantum States and Multi-Party Generation of Authorized Hidden GHZ States | ORIGINAL_RESEARCH | Non-interactive zero-knowledge proofs on quantum states; cryptographic protocol theory. |
| TQC-042 | 2025 | `10.1145/3723153` | Beyond NISQ: The Megaquop Machine | PERSPECTIVE | Perspective on what early error-corrected machines may be used for; application outlook without a classical-systems mechanism. Noted as a venue signal but fails all three gates. |
| TQC-043 | 2025 | `10.1145/3723884` | Quantum Divide and Conquer | ORIGINAL_RESEARCH | Quantum divide-and-conquer query-complexity framework; 'divide and conquer' is algorithmic, not parallel decomposition (vocabulary trap). |
| TQC-046 | 2025 | `10.1145/3736421` | Quantum Algorithms for Discrete Log Require Precise Rotations | ORIGINAL_RESEARCH | Noise sensitivity of Shor discrete-log rotations; algorithm analysis. |
| TQC-049 | 2025 | `10.1145/3743691` | Optimal Toffoli-Depth Quantum Adder | ORIGINAL_RESEARCH | Toffoli-depth optimal quantum adder; arithmetic-circuit depth only. |
| TQC-050 | 2025 | `10.1145/3748260` | Quantum Multiplexer Simplification for State Preparation | ORIGINAL_RESEARCH | Quantum multiplexer simplification for state preparation; CNOT/depth reduction is the contribution, compilation-time gain is secondary and unquantified against a systems baseline. |
| TQC-052 | 2025 | `10.1145/3748666` | Low-depth Amplitude Estimation without Really Trying | ORIGINAL_RESEARCH | Low-depth amplitude estimation; algorithmic precision/depth trade-off. |
| TQC-053 | 2025 | `10.1145/3757068` | Automated Synthesis of Quantum Algorithms via Classical Numerical Techniques | ORIGINAL_RESEARCH | Circuit/algorithm synthesis by classical numerical optimization and linear algebra; no parallelism, memory or scaling mechanism reported. |
| TQC-055 | 2025 | `10.1145/3759156` | Parameterized Complexity of Weighted Local Hamiltonian Problems and the Quantum Exponential Time Hypothesis | ORIGINAL_RESEARCH | Parameterized complexity of weighted local Hamiltonian; complexity classes. |
| TQC-056 | 2025 | `10.1145/3762671` | Variational Quantum Framework for Partial Differential Equation Constrained Optimization | ORIGINAL_RESEARCH | VQLS-based framework for PDE-constrained optimization; Q_FOR_HPC-flavoured application but no classical-systems contribution. |
| TQC-058 | 2025 | `10.1145/3762673` | Kronecker Coefficients in #BQP | ORIGINAL_RESEARCH | Kronecker coefficients in #BQP; complexity theory. |
| TQC-060 | 2025 | `10.1145/3769850` | Near-Heisenberg-limit Quantum Computing | ORIGINAL_RESEARCH | Spin-qubit action/energy experiment near the Heisenberg limit; device physics. |
| TQC-061 | 2025 | `10.1145/3769851` | A Polytime Quantum Programming Language | ORIGINAL_RESEARCH | A quantum programming language with quantum control and bounded recursion characterizing quantum polytime; implicit computational complexity, not a software stack contribution. |
| TQC-062 | 2025 | `10.1145/3773903` | A Cryptographic Perspective on the Verifiability of Quantum Advantage | ORIGINAL_RESEARCH | Cryptographic characterization of verifiable quantum advantage. |
| TQC-065 | 2025 | `10.1145/3778864` | Q-CHOP: Quantum constrained Hamiltonian optimization | ORIGINAL_RESEARCH | Q-CHOP constrained-optimization quantum algorithm. |
| TQC-067 | 2026 | `10.1145/3786463` | Visualizing Quantum Circuits: State Vector Difference Highlighting and the Half-Matrix | ORIGINAL_RESEARCH | Visualization techniques for quantum circuit state vectors; user-interface contribution. |
| TQC-068 | 2026 | `10.1145/3787461` | Quantum Algorithms for Hopcroft's problem | ORIGINAL_RESEARCH | Quantum algorithms for Hopcroft's problem; query/time complexity. |
| TQC-069 | 2026 | `10.1145/3787463` | Toffoli Requires Six Quantum Neighbor Gates | ORIGINAL_RESEARCH | Lower bound on neighbour gates for Toffoli; gate-count theory. |
| TQC-071 | 2026 | `10.1145/3795881` | STQS: A Unified System Architecture for Spatial Temporal Quantum Sensing | ORIGINAL_RESEARCH | Quantum sensing workflow architecture; title says 'system architecture' but the contribution is a sensing scheme and distance metric (vocabulary trap). |
| TQC-076 | 2026 | `10.1145/3800579` | Translation-Invariant Quantum Algorithms for Ordered Search are Optimal | ORIGINAL_RESEARCH | Optimality of translation-invariant ordered-search algorithms. |
| TQC-078 | 2026 | `10.1145/3802819` | The Power of Shallow-depth Toffoli and Qudit Quantum Circuits | ORIGINAL_RESEARCH | NO_ABSTRACT. Title indicates shallow-depth circuit class power (circuit complexity theory). Classified from title only; INSUFFICIENT_EVIDENCE for any systems content. |
| TQC-079 | 2026 | `10.1145/3807447` | Extending Quantum Annealing to Continuous Domains: a Hybrid Method for Quadratic Programming | ORIGINAL_RESEARCH | Hybrid quantum-annealing/simulated-annealing heuristic for quadratic programming; annealing metaheuristic. |
| TQC-080 | 2026 | `10.1145/3811537` | Improved Routing of Multiparty Entanglement over Quantum Networks | ORIGINAL_RESEARCH | Graph-state routing of multipartite entanglement over quantum networks; communication protocol, not distributed computation. |
| TQC-083 | 2026 | `10.1145/3815778` | Iterative Interpolation Schedules for Quantum Approximate Optimization Algorithm | ORIGINAL_RESEARCH | NO_ABSTRACT. Title indicates QAOA parameter-schedule construction; classified from title only. |
| TQC-084 | 2026 | `10.1145/3815786` | Utility-scale Experimental Quantum Computation with Hardware Efficient Ansätze and Calibrated Hamiltonian | ORIGINAL_RESEARCH | Hardware-efficient ansatz with calibrated Hamiltonian; ansatz/ground-state accuracy study. |
| TQC-085 | 2026 | `10.1145/3815787` | Genetic Synthesis of Compact Quaternary Reversible Comparators for Quantum Computing | ORIGINAL_RESEARCH | Genetic-algorithm synthesis of quaternary reversible comparators; gate-count/width objective. |
| TQC-086 | 2026 | `10.1145/3816436` | Quantum Matrix Arithmetics with Hamiltonian Evolution | ORIGINAL_RESEARCH | Quantum matrix arithmetic via Hamiltonian evolution; algorithmic primitives. |
| TQC-087 | 2026 | `10.1145/3821414` | Imposing Constraints on Driver Hamiltonians and Mixing Operators: From Theory to Practical Implementation | ORIGINAL_RESEARCH | Constraint-preserving driver Hamiltonians and mixers for ansatz construction. |
| TQC-088 | 2026 | `10.1145/3821429` | Acc-VQLS: Accelerated Variational Quantum Linear Solver for VSC Simulation | ORIGINAL_RESEARCH | Domain-specific VQLS acceleration for power-converter simulation; circuit/ansatz co-optimization, application accuracy. |
| TQC-090 | 2026 | `10.1145/3830909` | Verification of Quantum Protocols Adopting Physically Admissible Schedulers | ORIGINAL_RESEARCH | Process-calculus verification of quantum protocols; 'schedulers' is a formal-methods nondeterminism resolver, not systems scheduling (vocabulary trap). |
| TQC-093 | 2026 | `10.1145/3837860` | Efficient and Explicit Block Encoding of Finite Difference Discretizations of the Laplacian | ORIGINAL_RESEARCH | Block-encoding construction for the discretized Laplacian; data-input model for quantum linear algebra. |
| TQC-096 | 2026 | `10.1145/3842143` | A general framework for differentially private quantum measurements | ORIGINAL_RESEARCH | Differential privacy framework for quantum measurements; privacy theory. |
| TQC-097 | 2026 | `10.1145/3844137` | Convergence guarantee for linearly-constrained combinatorial optimization with a quantum alternating operator ansatz | ORIGINAL_RESEARCH | Convergence guarantee for constrained QAOA+; algorithm theory. |

### TACO — 5 excluded (55.6% of records classified)

| Class | Count | Records |
|---|---|---|
| `FP1_POST_QUANTUM_CRYPTOGRAPHY` | 2 | TACO-002, TACO-008 |
| `FP13_NON_QUANTUM_VOCABULARY_COLLISION` | 2 | TACO-003, TACO-004 |
| `FP5_QML_APPLICATIONS` | 1 | TACO-005 |

| ID | Year | DOI | Title | Type | Reason |
|---|---|---|---|---|---|
| TACO-002 | 2024 | `10.1145/3659209` | An Example of Parallel Merkle Tree Traversal: Post-Quantum Leighton-Micali Signature on the GPU | ORIGINAL_RESEARCH | GPU-parallel Merkle tree traversal for LMS hash-based signatures. Strong GPU/HPC content but the subject is post-quantum classical cryptography, the dominant false-positive class. |
| TACO-003 | 2024 | `10.1145/3664923` | Fixed-point Encoding and Architecture Exploration for Residue Number Systems | ORIGINAL_RESEARCH | Residue Number System fixed-point encoding and architecture exploration for AI matrix multiply; contains no quantum computing content. |
| TACO-004 | 2024 | `10.1145/3689342` | CoNST: Code Generator for Sparse Tensor Networks | ORIGINAL_RESEARCH | Code generator for classical sparse tensor network contraction; 'tensor network' here is a scientific-computing kernel, not quantum simulation (vocabulary trap). |
| TACO-005 | 2024 | `10.1145/3695872` | Towards High Performance QNNs via Distribution-Based CNOT Gate Reduction | ORIGINAL_RESEARCH | CNOT-gate reduction for quantum neural networks; QML accuracy plus gate-count objective, no classical-systems mechanism. |
| TACO-008 | 2026 | `10.1145/3839362` | Vectorized SVE2 Optimization of the Post-Quantum Signature ML-DSA on ARMv9-A Architecture | ORIGINAL_RESEARCH | SVE2-vectorized ML-DSA on ARMv9-A; post-quantum cryptography implementation. |

### False-positive class definitions

| Class | Definition |
|---|---|
| `FP10_DEVICE_CHARACTERIZATION_ERROR_MITIGATION` | Device benchmarking, tomography, stability, fidelity estimation and error mitigation whose currency is estimation quality. Corpus-specific extension. |
| `FP11_PL_THEORY_FORMAL_METHODS` | Programming-language theory, process calculi and formal verification without a software-stack or execution-cost contribution. Corpus-specific extension. |
| `FP12_VISUALIZATION_HCI` | Visualization and user-interface contributions. Corpus-specific extension. |
| `FP13_NON_QUANTUM_VOCABULARY_COLLISION` | Record entered the candidate pool on shared vocabulary ('tensor network', 'quantum', 'post-quantum') but contains no quantum-computing systems content. Corpus-specific extension. |
| `FP14_QUANTUM_CRYPTOGRAPHY_PROTOCOLS` | Quantum cryptographic protocols, verification of quantum advantage, quantum privacy theory. Corpus-specific extension of CRITERIA class 4. |
| `FP1_POST_QUANTUM_CRYPTOGRAPHY` | Post-quantum cryptography implementation/acceleration (CRITERIA class 1). |
| `FP2_QUANTUM_INSPIRED_CLASSICAL` | Quantum-inspired classical methods: Ising machines, annealing hardware/heuristics, QUBO solvers run classically (CRITERIA class 2). |
| `FP4_QUANTUM_NETWORKING_QKD` | Quantum networking / entanglement routing / QKD without a computing-systems contribution (CRITERIA class 4). |
| `FP5_QML_APPLICATIONS` | Quantum machine learning and quantum-application accuracy studies (CRITERIA class 5). |
| `FP6_SENSING_DEVICE_PHYSICS` | Quantum sensing, metrology, device and materials physics (CRITERIA class 6). |
| `FP7_ALGORITHMS_COMPLEXITY` | Quantum algorithms, query/gate complexity, complexity classes, resource estimates with no systems mechanism (CRITERIA class 7). |
| `FP8_SYNTHESIS_GATECOUNT_ONLY` | Circuit synthesis/optimization whose only argument is gate count, T-count, depth or width. Corpus-specific extension of CRITERIA class 7; the dominant false-positive class in TQC. |
| `FP9_VQA_ANSATZ_PARAMETERIZATION` | Variational ansatz design, parameter schedules, mixers, optimizer or warm-start studies. Corpus-specific extension covering the CRITERIA VQE exclusion rules. |

## 7. Conference-extension lineage

`CONFIRMED_EXTENSION` was recorded for no paper in either journal: no explicit 'extended version of' statement could be retrieved for any candidate. ACM article pages, where such footnotes normally sit, returned HTTP 403 to automated fetches.

| ID | Journal | Title | Verdict | Lineage | Evidence |
|---|---|---|---|---|---|
| TQC-001 | TQC | Efficient Syndrome Decoder for Heavy Hexagonal QECC via Machine Learning | BORDERLINE | UNKNOWN | Preprint arXiv:2210.09730. |
| TQC-009 | TQC | Revisiting the Mapping of Quantum Circuits: Entering the Multi-core Era | INCLUDED | UNKNOWN | Group (UPC Barcelona, Escofet et al.) has prior multi-core mapping conference work; no explicit extension statement located. Do not treat as confirmed. |
| TQC-014 | TQC | Quantum Circuit Cutting for Classical Shadows | BORDERLINE | UNKNOWN | Preprint arXiv:2212.00761. |
| TQC-016 | TQC | Efficient Quantum Circuit Design with a Standard Cell Approach, with an Application to Neutral Atom Quantum Computers | BORDERLINE | UNKNOWN | No evidence located. |
| TQC-019 | TQC | MQT Predictor: Automatic Device Selection with Device-Specific Circuit Compilation for Quantum Computing | INCLUDED | UNKNOWN | Preprint arXiv:2310.06889 carries no extension statement in the abstract listing. |
| TQC-021 | TQC | ARQUIN: Architectures for Multinode Superconducting Quantum Computers | INCLUDED | UNKNOWN | Preprint arXiv:2212.06167 'Architectures for Multinode Superconducting Quantum Computers' (33 authors, community co-design study). No conference version identified. |
| TQC-022 | TQC | Optimization Applications as Quantum Performance Benchmarks | INCLUDED | RELATED_LINEAGE | Continues the QED-C application-oriented benchmark series (earlier suite papers by Lubinski et al.); no explicit extension statement. |
| TQC-023 | TQC | Utilizing classical programming principles in the Intel Quantum SDK: implementation of quantum lattice Boltzmann method | BORDERLINE | UNKNOWN | Preprint arXiv:2407.03970. |
| TQC-025 | TQC | Robust Qubit Mapping Algorithm via Double-Source Optimal Routing on Large Quantum Circuits | INCLUDED | UNKNOWN | No evidence located. |
| TQC-027 | TQC | A Model-Driven Framework for Composition-Based Quantum Circuit Design | BORDERLINE | UNKNOWN | No evidence located. |
| TQC-029 | TQC | Realistic Cost to Execute Practical Quantum Circuits using Direct Clifford+T Lattice Surgery Compilation | INCLUDED | UNKNOWN | Builds on the open-source Lattice Surgery Compiler codebase, which is a tool lineage rather than a conference-paper lineage. |
| TQC-030 | TQC | Efficient Quantum Circuit Simulation by Tensor Network Methods on Modern GPUs | INCLUDED | UNKNOWN | No evidence located. |
| TQC-035 | TQC | What Quantum Can Learn from Classical Computer Engineering | BORDERLINE | UNKNOWN | N/A |
| TQC-037 | TQC | Forward and Backward Constrained Bisimulations for Quantum Circuits Using Decision Diagrams | INCLUDED | UNKNOWN | No evidence located. |
| TQC-041 | TQC | Algorithmic Theory of Qubit Routing in the Linear Nearest Neighbor Architectures | BORDERLINE | UNKNOWN | No evidence located. |
| TQC-044 | TQC | Approximate Quantum Compiling for Quantum Simulation: A Tensor Network Based Approach | BORDERLINE | UNKNOWN | Preprint arXiv:2301.08609. |
| TQC-045 | TQC | Line-Graph Qubit Routing | BORDERLINE | UNKNOWN | No evidence located. |
| TQC-047 | TQC | QuL: Programming Library for Computational Cooling of Qubits | BORDERLINE | UNKNOWN | Preprint arXiv:2410.13380. |
| TQC-048 | TQC | Integration of Quantum Accelerators with High Performance Computing—A Review of Quantum Programming Tools | INCLUDED | UNKNOWN | Preprint arXiv:2309.06167; no conference version identified. |
| TQC-051 | TQC | Lazy Qubit Reordering for Accelerating Parallel State-Vector-based Quantum Circuit Simulation | INCLUDED | UNKNOWN | No evidence located. |
| TQC-054 | TQC | DQC-QR: Distributing and Routing Quantum Circuits with Minimum Execution Time | INCLUDED | UNKNOWN | No evidence located. |
| TQC-057 | TQC | Simulation of Quantum Computers: Review and Acceleration Opportunities | INCLUDED | UNKNOWN | Preprint arXiv:2410.12660. |
| TQC-059 | TQC | CHARME: A Chain-based Reinforcement Learning Approach for the Minor Embedding Problem | BORDERLINE | UNKNOWN | No evidence located. Same author group as TQC-063 (FIDDLE). |
| TQC-063 | TQC | FIDDLE: Reinforcement Learning for Quantum Fidelity Enhancement | BORDERLINE | UNKNOWN | Preprint arXiv:2510.15833. Same group as TQC-059 (CHARME). |
| TQC-064 | TQC | Comparative Benchmarking of Utility-Scale Quantum Emulators | INCLUDED | UNKNOWN | Preprint arXiv:2504.14027. |
| TQC-066 | TQC | qSIEVE: Efficient qLDPC Memory via Systolic Movement in Atom Arrays | BORDERLINE | UNKNOWN | Preprint arXiv:2311.16980; the author group (Chicago/EPiQC lineage) publishes heavily at ISCA/ASPLOS/MICRO, so a conference version is plausible but NOT confirmed. |
| TQC-070 | TQC | Fast Algorithms and Implementations for Computing the Minimum Distance of Quantum Codes | INCLUDED | UNKNOWN | No evidence located. |
| TQC-072 | TQC | Benchmarking fault-tolerant quantum computing hardware via QLOPS | INCLUDED | UNKNOWN | Preprint arXiv:2507.12024. |
| TQC-073 | TQC | Quantum Backtracking in Qrisp Applied to Sudoku Problems | BORDERLINE | UNKNOWN | Preprint arXiv:2402.10060. |
| TQC-074 | TQC | QFOR: A Fidelity-aware Orchestrator for Quantum Computing Environments using Deep Reinforcement Learning | INCLUDED | UNKNOWN | No evidence located. |
| TQC-075 | TQC | Unifying Communication Paradigms in Measurement-based Delegated Quantum Computing | BORDERLINE | UNKNOWN | Preprint arXiv:2506.21988. |
| TQC-077 | TQC | It’s Quick to be Square: Fast Quadratisation for Quantum Toolchains | BORDERLINE | UNKNOWN | Preprint arXiv:2411.19934. |
| TQC-081 | TQC | QuCheck: A Property-based Testing Framework for Quantum Programs in Qiskit | BORDERLINE | UNKNOWN | No evidence located. |
| TQC-082 | TQC | Tracking Affine Subspace with Gaussian Elimination for Adaptive Quantum Circuit Simulation | INCLUDED | UNKNOWN | No evidence located. |
| TQC-089 | TQC | TREV: Python Library for Efficient Implementations of Variational Quantum Algorithms for Optimization using Tensor Networks | INCLUDED | UNKNOWN | ACM Just Accepted; no evidence located. |
| TQC-091 | TQC | Efficient Compilation for Shuttling Trapped-Ion Machines via the Position Graph Architectural Abstraction | INCLUDED | UNKNOWN | Preprint arXiv:2501.12470. |
| TQC-092 | TQC | FlatDD: Parallel Quantum Circuit Simulation using Decision Diagram and Flat Array | INCLUDED | UNKNOWN | ACM Just Accepted. Author group (Shui Jiang et al.) publishes DD/EDA work at design-automation venues; a conference predecessor is plausible but NOT confirmed. |
| TQC-094 | TQC | QASMTrans: An End-to-End QASM Compilation Framework with Pulse Generation for Near-Term Quantum Devices | INCLUDED | RELATED_LINEAGE | arXiv:2602.05154 carries an explicit note of substantial text overlap with arXiv:2308.07581, the earlier QASMTrans transpiler paper. That is documented lineage but not an explicit 'extended version of' statement for a named conference, so it is recorded as RELATED_LINEAGE rather than CONFIRMED_EXTENSION. |
| TQC-095 | TQC | How Many Shots Are Enough for a Quantum Circuit? | INCLUDED | UNKNOWN | ACM Just Accepted; preprint arXiv:2606.16965. |
| TACO-001 | TACO | QuCloud+: A Holistic Qubit Mapping Scheme for Single/Multi-programming on 2D/3D NISQ Quantum Computers | INCLUDED | RELATED_LINEAGE | The 'plus' naming and shared lead author point to QuCloud (HPCA 2021, Liu and Dou) as the predecessor, and arXiv:2207.14483 carries the QuCloud+ title. The arXiv listing contains no explicit 'extended version of' statement, so this is recorded as RELATED_LINEAGE, not CONFIRMED_EXTENSION. |
| TACO-006 | TACO | LarQucut: A New Cutting and Mapping Approach for Large-sized Quantum Circuits in Distributed Quantum Computing (DQC) Environments | INCLUDED | UNKNOWN | Same group as TACO-001 (Xinglei Dou is a QuCloud co-author). No explicit conference predecessor located for LarQucut. |
| TACO-007 | TACO | Ecmas+: Efficient Circuit Mapping and Scheduling for Surface Code Encoded Circuit on Quantum Cloud Platform | INCLUDED | RELATED_LINEAGE | The 'plus' naming indicates a predecessor named Ecmas by the same group (Mingzheng Zhu et al.). No explicit extension statement could be retrieved - the ACM page returned HTTP 403 on two attempts - so this stays RELATED_LINEAGE. |
| TACO-009 | TACO | A System Architecture for Low Latency Multiprogramming Quantum Computing | INCLUDED | UNKNOWN | ACM Just Accepted; no predecessor located. |

## 8. Artifact status

Required for every INCLUDED original-research paper; BORDERLINE records are listed too.

| ID | Journal | Title | Verdict | Artifact status | URL |
|---|---|---|---|---|---|
| TQC-001 | TQC | Efficient Syndrome Decoder for Heavy Hexagonal QECC via Machine Learning | BORDERLINE | UNKNOWN | — |
| TQC-009 | TQC | Revisiting the Mapping of Quantum Circuits: Entering the Multi-core Era | INCLUDED | UNKNOWN | — |
| TQC-014 | TQC | Quantum Circuit Cutting for Classical Shadows | BORDERLINE | UNKNOWN | — |
| TQC-016 | TQC | Efficient Quantum Circuit Design with a Standard Cell Approach, with an Application to Neutral Atom Quantum Computers | BORDERLINE | UNKNOWN | — |
| TQC-019 | TQC | MQT Predictor: Automatic Device Selection with Device-Specific Circuit Compilation for Quantum Computing | INCLUDED | PUBLIC_CODE | https://github.com/cda-tum/mqt-predictor |
| TQC-021 | TQC | ARQUIN: Architectures for Multinode Superconducting Quantum Computers | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| TQC-022 | TQC | Optimization Applications as Quantum Performance Benchmarks | INCLUDED | PARTIAL | https://github.com/SRI-International/QC-App-Oriented-Benchmarks |
| TQC-023 | TQC | Utilizing classical programming principles in the Intel Quantum SDK: implementation of quantum lattice Boltzmann method | BORDERLINE | UNKNOWN | — |
| TQC-025 | TQC | Robust Qubit Mapping Algorithm via Double-Source Optimal Routing on Large Quantum Circuits | INCLUDED | UNKNOWN | — |
| TQC-027 | TQC | A Model-Driven Framework for Composition-Based Quantum Circuit Design | BORDERLINE | UNKNOWN | — |
| TQC-029 | TQC | Realistic Cost to Execute Practical Quantum Circuits using Direct Clifford+T Lattice Surgery Compilation | INCLUDED | PARTIAL | https://github.com/latticesurgery-com/lattice-surgery-compiler |
| TQC-030 | TQC | Efficient Quantum Circuit Simulation by Tensor Network Methods on Modern GPUs | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| TQC-035 | TQC | What Quantum Can Learn from Classical Computer Engineering | BORDERLINE | UNKNOWN | — |
| TQC-037 | TQC | Forward and Backward Constrained Bisimulations for Quantum Circuits Using Decision Diagrams | INCLUDED | UNKNOWN | — |
| TQC-041 | TQC | Algorithmic Theory of Qubit Routing in the Linear Nearest Neighbor Architectures | BORDERLINE | UNKNOWN | — |
| TQC-044 | TQC | Approximate Quantum Compiling for Quantum Simulation: A Tensor Network Based Approach | BORDERLINE | UNKNOWN | — |
| TQC-045 | TQC | Line-Graph Qubit Routing | BORDERLINE | UNKNOWN | — |
| TQC-047 | TQC | QuL: Programming Library for Computational Cooling of Qubits | BORDERLINE | UNKNOWN | — |
| TQC-048 | TQC | Integration of Quantum Accelerators with High Performance Computing—A Review of Quantum Programming Tools | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| TQC-051 | TQC | Lazy Qubit Reordering for Accelerating Parallel State-Vector-based Quantum Circuit Simulation | INCLUDED | UNKNOWN | — |
| TQC-054 | TQC | DQC-QR: Distributing and Routing Quantum Circuits with Minimum Execution Time | INCLUDED | UNKNOWN | — |
| TQC-057 | TQC | Simulation of Quantum Computers: Review and Acceleration Opportunities | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| TQC-059 | TQC | CHARME: A Chain-based Reinforcement Learning Approach for the Minor Embedding Problem | BORDERLINE | UNKNOWN | — |
| TQC-063 | TQC | FIDDLE: Reinforcement Learning for Quantum Fidelity Enhancement | BORDERLINE | UNKNOWN | — |
| TQC-064 | TQC | Comparative Benchmarking of Utility-Scale Quantum Emulators | INCLUDED | UNKNOWN | — |
| TQC-066 | TQC | qSIEVE: Efficient qLDPC Memory via Systolic Movement in Atom Arrays | BORDERLINE | UNKNOWN | — |
| TQC-070 | TQC | Fast Algorithms and Implementations for Computing the Minimum Distance of Quantum Codes | INCLUDED | UNKNOWN | — |
| TQC-072 | TQC | Benchmarking fault-tolerant quantum computing hardware via QLOPS | INCLUDED | UNKNOWN | — |
| TQC-073 | TQC | Quantum Backtracking in Qrisp Applied to Sudoku Problems | BORDERLINE | UNKNOWN | — |
| TQC-074 | TQC | QFOR: A Fidelity-aware Orchestrator for Quantum Computing Environments using Deep Reinforcement Learning | INCLUDED | UNKNOWN | — |
| TQC-075 | TQC | Unifying Communication Paradigms in Measurement-based Delegated Quantum Computing | BORDERLINE | UNKNOWN | — |
| TQC-077 | TQC | It’s Quick to be Square: Fast Quadratisation for Quantum Toolchains | BORDERLINE | UNKNOWN | — |
| TQC-081 | TQC | QuCheck: A Property-based Testing Framework for Quantum Programs in Qiskit | BORDERLINE | UNKNOWN | — |
| TQC-082 | TQC | Tracking Affine Subspace with Gaussian Elimination for Adaptive Quantum Circuit Simulation | INCLUDED | UNKNOWN | — |
| TQC-089 | TQC | TREV: Python Library for Efficient Implementations of Variational Quantum Algorithms for Optimization using Tensor Networks | INCLUDED | UNKNOWN | — |
| TQC-091 | TQC | Efficient Compilation for Shuttling Trapped-Ion Machines via the Position Graph Architectural Abstraction | INCLUDED | UNKNOWN | — |
| TQC-092 | TQC | FlatDD: Parallel Quantum Circuit Simulation using Decision Diagram and Flat Array | INCLUDED | UNKNOWN | — |
| TQC-094 | TQC | QASMTrans: An End-to-End QASM Compilation Framework with Pulse Generation for Near-Term Quantum Devices | INCLUDED | UNKNOWN | — |
| TQC-095 | TQC | How Many Shots Are Enough for a Quantum Circuit? | INCLUDED | UNKNOWN | — |
| TACO-001 | TACO | QuCloud+: A Holistic Qubit Mapping Scheme for Single/Multi-programming on 2D/3D NISQ Quantum Computers | INCLUDED | UNKNOWN | — |
| TACO-006 | TACO | LarQucut: A New Cutting and Mapping Approach for Large-sized Quantum Circuits in Distributed Quantum Computing (DQC) Environments | INCLUDED | UNKNOWN | — |
| TACO-007 | TACO | Ecmas+: Efficient Circuit Mapping and Scheduling for Surface Code Encoded Circuit on Quantum Cloud Platform | INCLUDED | UNKNOWN | — |
| TACO-009 | TACO | A System Architecture for Low Latency Multiprogramming Quantum Computing | INCLUDED | UNKNOWN | — |

Artifact distribution across the 43 INCLUDED + BORDERLINE records: UNKNOWN 36, NO_PUBLIC_ARTIFACT_FOUND 4, PARTIAL 2, PUBLIC_CODE 1.
`UNKNOWN` dominates because artifact availability is not stated in the 700-character abstracts and ACM artifact-badge pages were not reachable; it means not checked, not absent.

## 9. Census-policy judgements

### TQC (ACM Transactions on Quantum Computing) — **SELECTIVE_CENSUS**

- The whole population is quantum, so venue-level screening cannot be skipped: 58 of 97 records (59.8%) fail all three gates and a further 17 sit at BORDERLINE after adjudication of an adversarial verification pass. Sweeping TQC wholesale would import quantum algorithms and complexity theory into an HPC corpus.
- The yield is nevertheless real: 20 original-research INCLUDED records plus two review anchors, concentrated in simulation engines, compilation/mapping with a classical cost argument, multi-core and multi-QPU execution, and scheduling/orchestration.
- TQC carries material that TPDS/TC/TCAD-style venues do not: multinode architecture studies (TQC-021), HPC-QPU integration surveys (TQC-048), emulator benchmarking (TQC-064) and a special issue explicitly about importing classical computer engineering (TQC-035).
- Screening is cheap and reliable here because the discriminator is simple: does the paper state a classical cost quantity (runtime, memory, communication, compile time, throughput, utilization) or only a quantum-resource quantity (gate count, depth, fidelity, shots-for-accuracy)?

**Screening rule for the next sweep.** Screen every TQC record on title plus abstract against the classical-cost discriminator above. Expect to retain roughly one fifth as INCLUDED, with a further sixth at BORDERLINE. Auto-drop the recurring exclusion families: gate-count/depth synthesis, query and circuit complexity, VQA ansatz and parameter schedules, device characterization and error mitigation, quantum cryptography and QKD, sensing and device physics.

**Expected annual yield.** 4 to 9 per census year on the 2024-2026 evidence after adjudication (2024: 7, 2025: 4, 2026: 9)

**Sub-areas to track in TQC going forward.**

- distributed / multi-core / multi-QPU execution and mapping (TQC-009, TQC-021, TQC-054; TQC-066 at BORDERLINE)
- classical simulation engines and their acceleration: state-vector on multi-GPU, tensor network, decision diagram, sparse/adaptive (TQC-030, TQC-037, TQC-051, TQC-082, TQC-092, TQC-089)
- compiler and transpiler work that reports compile time, scalability or toolchain cost, not only circuit quality (TQC-019, TQC-025, TQC-091, TQC-094; TQC-077 at BORDERLINE pending verified timings)
- QPU scheduling, orchestration, shot budgeting and multi-tenancy (TQC-074, TQC-095)
- HPC-QPU integration and programming-tool surveys, plus emulator and FTQC throughput benchmarking (TQC-048, TQC-057, TQC-064, TQC-072)
- classical parallel kernels serving QEC and code design, including decoders that report latency or accelerator mapping (TQC-070; TQC-001 only if latency/hardware analysis appears)

### TACO (ACM Transactions on Architecture and Code Optimization) — **BIBLIOGRAPHY_SENSOR**

- Yield against the full population is very low: the 9 records here were drawn from a 412-article sweep, and only 4 pass the gates, about 1% of TACO's output.
- But the 4 that pass are unusually strong and are not duplicated elsewhere in the corpus: multi-tenancy and qubit-resource partitioning (TACO-001), circuit cutting plus mapping for heterogeneous QPU pools (TACO-006), surface-code compilation framed as platform throughput (TACO-007), and offline multi-version compilation with runtime dispatch (TACO-009).
- The false positives are concentrated and machine-separable: two post-quantum cryptography papers and two pure vocabulary collisions ('tensor network' as a classical kernel, RNS arithmetic). A keyword sweep plus a four-class filter removes 4 of 5 exclusions without human judgement.
- TACO also shows a rising trend: 1 included record in 2024, 2 in 2025, 1 in 2026 so far, with the 2025-2026 items moving from mapping toward runtime and serving architecture.

**Screening rule for the next sweep.** Keep TACO as a low-cost annual keyword sensor on quantum vocabulary, then apply a hard drop for post-quantum cryptography (Kyber, Dilithium, ML-KEM, ML-DSA, LMS, XMSS, SPHINCS+, NTT, lattice) and for classical tensor-network or numeric-representation work. Hand-read only what survives; that is typically 3 to 5 records per year.

**Expected annual yield.** 1 to 2 per census year

## 10. Cross-journal observations

- The two venues are complementary rather than overlapping. TQC supplies simulation engines, multi-core and multi-QPU architecture, compilation, and HPC-integration surveys. TACO supplies the multi-tenancy, throughput and serving-architecture framing — all four TACO inclusions treat the QPU as a shared resource with a utilization or latency target.
- `compiler_mapping_routing` is the largest branch in both (15 in TQC, 4 in TACO), but the two venues cut it differently: TQC mapping papers mostly argue circuit quality and were excluded or held at BORDERLINE, while every TACO mapping paper carries a utilization, throughput or latency objective.
- `Q_FOR_HPC` is the thinnest scenario in the corpus: one BORDERLINE record (TQC-023) across both journals. UNDERREPRESENTED_IN_THIS_CORPUS.
- Post-quantum cryptography behaves exactly as CRITERIA predicts: zero occurrences in TQC, two of five TACO exclusions. It is a TACO-side filter, not a TQC-side one.
- The TQC exclusion profile is instead dominated by `FP7_ALGORITHMS_COMPLEXITY` (21) and `FP8_SYNTHESIS_GATECOUNT_ONLY` (11) — together 32 of 58 exclusions. These two classes are what SCOPE EXPLOSION would look like if the gates were relaxed.
- Vocabulary traps worth noting for any automated screen: 'hybrid quantum-classical' as a complexity model (TQC-004), 'quantum memory' as an information-theoretic resource (TQC-017), 'divide and conquer' as recursion not parallelism (TQC-043), 'schedulers' as formal-methods nondeterminism (TQC-090), 'system architecture' for a sensing scheme (TQC-071), and 'tensor network' as a classical sparse kernel (TACO-004).

# Quantum-HPC Journal Census — TC · TCAD · TPDS · JPDC (2024–2026)

Four-journal census of the HPC × quantum-computing interface, produced against the shared inclusion
criteria in `/home/claude/jc/CRITERIA.md`. Machine-readable records: `TC_records.json`,
`TCAD_records.json`, `TPDS_records.json`, `JPDC_records.json`.

## 1. Scope and method

| Journal | ISSN | Full population swept | Candidate records | Included | of which original research | Borderline | Insufficient evidence | Excluded | Out of window |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TC — IEEE Transactions on Computers | 0018-9340 | 849 | 41 | 6 | 6 | 6 | 0 | 28 | 1 |
| TCAD — IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems | 0278-0070 | 1562 | 68 | 12 | 12 | 12 | 3 | 41 | 0 |
| TPDS — IEEE Transactions on Parallel and Distributed Systems | 1045-9219 | 552 | 10 | 2 | 2 | 0 | 0 | 8 | 0 |
| JPDC — Journal of Parallel and Distributed Computing | 0743-7315 | 388 | 7 | 1 | 0 | 0 | 0 | 6 | 0 |

Inclusion rate against the full swept population: TC 6/849 (0.71%), TCAD 12/1562 (0.77%), TPDS 2/552 (0.36%), JPDC 1/388 (0.26%).

**Method.** Every candidate record was classified for article type and verdict against the three-gate test
(real classical systems problem · HPC/systems/architecture technique as a major part of the contribution ·
material relevance to CPU/GPU/HPC ↔ QPU heterogeneous computing). Excluded records are keyed to a
false-positive class from the criteria file and logged in §6. Census year is the year of first public
availability (IEEE Early Access / Elsevier online-first) as supplied in the dossiers; final volume/issue is
recorded separately, and records without a volume are IEEE Early Access.

**Decision rule applied to compilation work** (the largest single population here, and the one most at risk
of over-inclusion): a mapping/routing/synthesis paper is INCLUDED when its stated objective involves
compilation cost, parallel or distributed compilation, execution scheduling, data movement, or multi-chip
communication; it is BORDERLINE when the objective is output fidelity, gate count, depth or qubit count
alone. This rule is what separates, for example, TCAD-024 (parallel mapper, mapping time) from TCAD-007
(reinforcement-learning mapper, fidelity).

**Evidence discipline.** Dossier abstracts are truncated at 700 characters, so most quantitative claims are
recorded as present-but-unquantified with the baseline named where the abstract names it, and
`BASELINE_UNCLEAR` otherwise. Twenty records carried `*** NO ABSTRACT RETRIEVED ***` (TC 3, TCAD 10, JPDC 7,
TPDS 0); these are flagged `NO_ABSTRACT`, and where such a record is included or borderline its evidence
basis is `TITLE_ONLY_NO_ABSTRACT`. Where a title cannot settle the gates
the verdict is `INSUFFICIENT_EVIDENCE` (TCAD-061, TCAD-064, TCAD-066) rather than a guess. Web retrieval was
attempted for the highest-value gaps: the JPDC quantum-serverless abstract was retrieved from the publisher;
IEEE Early Access pages for TCAD-058/062/064 and TC-041 returned no abstract text (IEEE Xplore blocked;
Semantic Scholar records carry null abstracts), so those remain title-only.

**Branch vocabulary.** Two branches were added to the starting vocabulary because the corpus demanded them:
`fpga_accelerated_simulation` (FPGA/storage-backed simulators and emulators, a TC-specific shape) and
`simulation_verification_scaling` (decision-diagram and tensor-network simulation, equivalence checking and
simulator-kernel optimisation, a TCAD-specific shape distinct from cluster-scale `distributed_gpu_simulation`).

**Verification pass (round 2).** An independent adversarial review prompted four changes, all applied here:
TCAD-057's census year was corrected 2026 -> 2025 (OpenAlex publication_date 2025-10-28; the 2026-06 issue cover
date had been used); TCAD-025, TCAD-038 and TC-031 were demoted INCLUDED -> BORDERLINE on adjudication, each
because its only measured quantity is a quantum resource (fidelity, mapping quality) or a classification
accuracy rather than a classical systems quantity, so Gate 2 is not met; TC-001 was re-marked OUT_OF_WINDOW
(DOI 10.1109/tc.2021.3066614, first public availability 2021, 2024 issue cover date used in error); and four
RELATED_LINEAGE claims resting only on a preprint or a same-journal companion (TC-027, TC-040, TCAD-010,
TCAD-066) were downgraded to UNKNOWN. Every INCLUDED and BORDERLINE record carries canonical `gate1`,
`gate2`, `gate3` fields, BORDERLINE records carry `borderline_reason_for` and `borderline_reason_against`,
and the three INSUFFICIENT_EVIDENCE records carry `what_would_resolve_it`.

**Institutions.** The dossiers supply first author and co-author count but no affiliation, so
`first_author_institution` is recorded as `NOT_IN_DOSSIER` throughout rather than inferred.

## 2. Per-journal, per-year tables

### TC — IEEE Transactions on Computers

| Census year | Candidates | Included | Borderline | Insufficient evidence | Excluded | Out of window |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 11 | 2 | 1 | 0 | 7 | 1 |
| 2025 | 20 | 2 | 5 | 0 | 13 | 0 |
| 2026 | 10 | 2 | 0 | 0 | 8 | 0 |
| **Total** | **41** | **6** | **6** | **0** | **28** | **1** |

Included: TC-004, TC-011, TC-023, TC-030, TC-040, TC-041.
Borderline: TC-010, TC-016, TC-017, TC-027, TC-029, TC-031.

Branch distribution (included + borderline + unresolved): `compiler_mapping_routing` 8, `fpga_accelerated_simulation` 3, `benchmarking_performance_modeling` 1, `multi_qpu_distributed_qc` 1, `qpu_scheduling_resource_mgmt` 1, `architecture_control` 1.

Scenario distribution (included only): `HPC_FOR_Q` 6, `FUTURE_WORKLOAD` 2.

### TCAD — IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems

| Census year | Candidates | Included | Borderline | Insufficient evidence | Excluded | Out of window |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 28 | 5 | 6 | 0 | 17 | 0 |
| 2025 | 28 | 6 | 4 | 0 | 18 | 0 |
| 2026 | 12 | 1 | 2 | 3 | 6 | 0 |
| **Total** | **68** | **12** | **12** | **3** | **41** | **0** |

Included: TCAD-010, TCAD-014, TCAD-023, TCAD-024, TCAD-027, TCAD-030, TCAD-033, TCAD-043, TCAD-050, TCAD-051, TCAD-057, TCAD-062.
Borderline: TCAD-001, TCAD-006, TCAD-007, TCAD-012, TCAD-025, TCAD-026, TCAD-037, TCAD-038, TCAD-040, TCAD-045, TCAD-058, TCAD-063.
Insufficient evidence: TCAD-061, TCAD-064, TCAD-066.

Branch distribution (included + borderline + unresolved): `compiler_mapping_routing` 17, `architecture_control` 5, `simulation_verification_scaling` 4, `multi_qpu_distributed_qc` 4, `benchmarking_performance_modeling` 3, `quantum_runtime_orchestration` 2, `qpu_scheduling_resource_mgmt` 1, `hpc_qpu_integration` 1, `hybrid_workflow` 1.

Scenario distribution (included only): `HPC_FOR_Q` 11, `FUTURE_WORKLOAD` 4, `Q_IN_HPC` 2.

### TPDS — IEEE Transactions on Parallel and Distributed Systems

| Census year | Candidates | Included | Borderline | Insufficient evidence | Excluded | Out of window |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 3 | 0 | 0 | 0 | 3 | 0 |
| 2025 | 3 | 0 | 0 | 0 | 3 | 0 |
| 2026 | 4 | 2 | 0 | 0 | 2 | 0 |
| **Total** | **10** | **2** | **0** | **0** | **8** | **0** |

Included: TPDS-007, TPDS-008.

Branch distribution (included + borderline + unresolved): `distributed_gpu_simulation` 2, `benchmarking_performance_modeling` 1.

Scenario distribution (included only): `HPC_FOR_Q` 2.

### JPDC — Journal of Parallel and Distributed Computing

| Census year | Candidates | Included | Borderline | Insufficient evidence | Excluded | Out of window |
|---|---:|---:|---:|---:|---:|---:|
| 2024 | 1 | 0 | 0 | 0 | 1 | 0 |
| 2025 | 2 | 0 | 0 | 0 | 2 | 0 |
| 2026 | 4 | 1 | 0 | 0 | 3 | 0 |
| **Total** | **7** | **1** | **0** | **0** | **6** | **0** |

Included: JPDC-007.

Branch distribution (included + borderline + unresolved): `hpc_qpu_integration` 1, `quantum_runtime_orchestration` 1, `hybrid_workflow` 1.

Scenario distribution (included only): `Q_IN_HPC` 1, `HPC_FOR_Q` 1.

## 3. Full records — INCLUDED

### TC (6)

#### TC-004 — A Mutual-Influence-Aware Heuristic Method for Quantum Circuit Mapping

- **DOI** `10.1109/tc.2024.3441825` · **census year** 2024 · volume 73, issue 12, pp 2855-2867 · **issue date** 2024-12 · **online first** 2024-08-12
- **First author** Kui Ye (+8 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Compilation/preprocessing cost: the stated trade-off is between inserted-gate count and the efficiency (runtime) of the mapping preprocessing stage.
- **Gate 2 (systems technique):** Heuristic compiler design: initial-mapping search framework + generator + heuristic mapper, i.e. a classical compilation pipeline with an explicit cost budget.
- **Gate 3 (heterogeneous relevance):** Informs the classical compilation stage of a CPU-plus-QPU stack, where mapping time is part of job turnaround.
- **Contribution:** Mutual-influence-aware (MIA) heuristic qubit-mapping method combining an initial-mapping search framework, an initial-mapping generator and a heuristic circuit mapper.
- **Performance claim / baseline:** Improved mapping quality and preprocessing efficiency; specific figures BASELINE_UNCLEAR from the abstract.
- **Evidence basis:** ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** Included on the compilation-cost limb of Gate 1; the fidelity/gate-count limb alone would have been BORDERLINE.

#### TC-011 — Qu-Trefoil: Large-Scale Quantum Circuit Simulator Working on FPGA With SATA Storages

- **DOI** `10.1109/tc.2024.3521546` · **census year** 2024 · volume 74, issue 4, pp 1306-1321 · **issue date** 2025-4 · **online first** 2024-12-23
- **First author** Kaijie Wei (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv `2608.14285`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** fpga_accelerated_simulation, benchmarking_performance_modeling
- **Gate 1 (classical systems problem):** Memory capacity and data movement: 2^(n+4) bytes of state vector forces the design out of DRAM onto SATA storage; I/O bandwidth is the binding constraint.
- **Gate 2 (systems technique):** Accelerator architecture for state-vector simulation: FPGA datapath plus a storage hierarchy spanning SATA SSDs.
- **Gate 3 (heterogeneous relevance):** Directly informs how large-scale simulation workloads can be served by non-CPU hardware and a deep memory hierarchy.
- **Contribution:** Qu-Trefoil: FPGA-based large-scale state-vector quantum circuit simulator using SATA-attached storage to extend simulable qubit count beyond memory capacity.
- **Performance claim / baseline:** Extended qubit capacity relative to memory-resident simulation; numeric speedups and the comparison baseline are BASELINE_UNCLEAR from the truncated abstract.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** arXiv id recorded in the dossier as 2608.14285; not verified against the article.

#### TC-023 — AdaptDQC: Adaptive Distributed Quantum Computing With Quantitative Performance Analysis

- **DOI** `10.1109/tc.2025.3586027` · **census year** 2025 · volume 74, issue 10, pp 3277-3290 · **issue date** 2025-10 · **online first** 2025-07-14
- **First author** Debin Xiang (+7 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch** multi_qpu_distributed_qc, compiler_mapping_routing
- **Gate 1 (classical systems problem):** Inter-chip communication volume, partitioning cost and multi-objective performance metrics for distributed quantum computing.
- **Gate 2 (systems technique):** Compiler framework with a spatial-temporal graph model of circuits and interconnect architectures; circuit partitioning and chip mapping under hybrid inter-chip-communication architectures.
- **Gate 3 (heterogeneous relevance):** Directly addresses multi-QPU/modular execution and its communication cost, a central question for heterogeneous systems.
- **Contribution:** AdaptDQC: adaptive DQC compiler that models circuits and inter-chip communication architectures in one spatial-temporal graph and optimises partitioning/mapping against configurable objectives.
- **Performance claim / baseline:** Reports average reductions in communication cost against state-of-the-art DQC compiler frameworks; exact percentages truncated in the dossier abstract (BASELINE = prior DQC compilers).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** One of the two architecture-level distributed-QC papers in TC; quantitative performance analysis of ICC architectures is the distinguishing feature.

#### TC-030 — SuperEncoder: Towards Efficient Neural Approximate Quantum State Preparation

- **DOI** `10.1109/tc.2025.3644034` · **census year** 2025 · volume 75, issue 3, pp 916-927 · **issue date** 2026-3 · **online first** 2025-12-15
- **First author** Yilun Zhao (+6 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Classical runtime: the iterative, state-by-state PQC optimisation for approximate state preparation is identified as substantial runtime overhead.
- **Gate 2 (systems technique):** A trained neural encoder replaces the per-instance classical optimisation loop, i.e. amortising compilation cost across inputs.
- **Gate 3 (heterogeneous relevance):** Informs the cost of the classical side of the software stack when data must be loaded into a QPU repeatedly.
- **Contribution:** SuperEncoder: neural approximate quantum state preparation that generates PQC parameters without per-state iterative optimisation.
- **Performance claim / baseline:** Reduced state-preparation runtime versus iterative per-state PQC optimisation; magnitude BASELINE_UNCLEAR from the truncated abstract.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** Included on compilation-cost grounds; if the full text is dominated by fidelity comparisons this would move to BORDERLINE.

#### TC-040 — AMARETTO, Accelerating Quantum Algorithm Development With FPGA Emulation

- **DOI** `10.1109/tc.2026.3710326` · **census year** 2026 · volume 75, issue 10, pp 3544-3555 · **issue date** 2026-10 · **online first** 2026-07-07
- **First author** Christian Conti (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** fpga_accelerated_simulation
- **Gate 1 (classical systems problem):** Simulation time and memory: software simulators are described as time-consuming with exponentially growing memory demand.
- **Gate 2 (systems technique):** FPGA hardware emulator as an alternative execution substrate for quantum circuit evaluation.
- **Gate 3 (heterogeneous relevance):** Informs accelerator-based offload of the quantum-simulation workload in a heterogeneous facility.
- **Contribution:** AMARETTO: FPGA emulator for quantum algorithm development, targeting resource-constrained (low-tier) FPGAs.
- **Performance claim / baseline:** Faster and more resource-efficient than software simulation; exact speedup and baseline simulator BASELINE_UNCLEAR from the truncated abstract.
- **Evidence basis:** ABSTRACT_TRUNCATED+WEB_SEARCH
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** A preprint with the same system name exists as arXiv 2411.09320 ('AMARETTO: Enabling Efficient Quantum Algorithm Emulation on Low-Tier FPGAs'); relationship to this TC article not confirmed from the article itself, hence RELATED_LINEAGE rather than CONFIRMED_EXTENSION. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the evidence is a same-name arXiv preprint (2411.09320), which is not a conference paper; no conference venue was verified.

#### TC-041 — Quantum at the Edge: Scalable Standalone FPGA Emulator for QAOA–based Weighted-MaxCut

- **DOI** `10.1109/tc.2026.3724836` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Seonghyun Choi (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** NO_ABSTRACT
- **Scenario** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch** fpga_accelerated_simulation
- **Gate 1 (classical systems problem):** Scalability and standalone execution of an accelerator that emulates a quantum algorithm; title states scalability as the design goal.
- **Gate 2 (systems technique):** FPGA emulator architecture for QAOA-based weighted MaxCut.
- **Gate 3 (heterogeneous relevance):** Informs edge/standalone accelerator substrates for quantum-algorithm workloads.
- **Contribution:** Standalone FPGA emulator for QAOA-based weighted MaxCut, presented as scalable and edge-deployable (title evidence only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE (no abstract retrieved).
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** NO_ABSTRACT. IEEE Early Access (no volume). Verdict rests on the title alone, which names an FPGA emulator and scalability; full text required to confirm the systems evaluation.

### TCAD (12)

#### TCAD-010 — QuBEC: Boosting Equivalence Checking for Quantum Circuits With QEC Embedding

- **DOI** `10.1109/tcad.2024.3361402` · **census year** 2024 · volume 43, issue 7, pp 2037-2042 · **issue date** 2024-7 · **online first** 2024-02-02
- **First author** Chao Lu (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv `2309.10728`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** simulation_verification_scaling
- **Gate 1 (classical systems problem):** Classical verification runtime for quantum circuits; latency of equivalence checking is the reported metric.
- **Gate 2 (systems technique):** Decision-diagram data structure engineering (QEC-aware embedding) to make the classical checker scale.
- **Gate 3 (heterogeneous relevance):** Informs the cost of the classical verification stage in a quantum software stack.
- **Contribution:** QuBEC: decision-diagram-based equivalence checking that accounts for error-correction redundancy in circuits.
- **Performance claim / baseline:** Up to 443x lower verification time on benchmark circuits; BASELINE = existing decision-diagram equivalence-checking techniques (as stated in the abstract).
- **Evidence basis:** ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** arXiv 2309.10728 preprint recorded in the dossier; conference lineage not confirmed from the article itself. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the evidence is the arXiv preprint 2309.10728 only; no conference version was verified.

#### TCAD-014 — QHLS: An HLS Framework to Convert High-Level Descriptions to Quantum Circuits

- **DOI** `10.1109/tcad.2024.3391699` · **census year** 2024 · volume 43, issue 10, pp 3015-3026 · **issue date** 2024-10 · **online first** 2024-04-19
- **First author** Chao Lu (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Programming scalability and automation: manual circuit construction is identified as not scaling and as requiring expert effort.
- **Gate 2 (systems technique):** A high-level synthesis toolchain - a classical compiler front end that lowers high-level descriptions to circuits.
- **Gate 3 (heterogeneous relevance):** Informs the software stack layer of a hybrid system (how applications reach a QPU).
- **Contribution:** QHLS: high-level-synthesis framework converting high-level descriptions into quantum circuits.
- **Performance claim / baseline:** Automatic generation of circuits from high-level descriptions; quantitative compile-cost evidence not present in the abstract (BASELINE_UNCLEAR).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** Included as a software-stack/toolchain contribution; the abstract carries no compile-time measurements, so the systems evidence is qualitative.

#### TCAD-023 — SmartQCache: Fast and Precise Pulse Control With Near-Quantum Cache Design on FPGA

- **DOI** `10.1109/tcad.2024.3497839` · **census year** 2024 · volume 44, issue 5, pp 1704-1716 · **issue date** 2025-5 · **online first** 2024-11-13
- **First author** Liqiang Lu (+5 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, Q_IN_HPC · **Branch** architecture_control, quantum_runtime_orchestration
- **Gate 1 (classical systems problem):** Latency and computational cost of pulse synthesis; CPU-side synthesis is described as redundant and costly for large circuits, FPGA-side synthesis as inaccurate.
- **Gate 2 (systems technique):** Near-quantum cache architecture on FPGA plus a CPU/FPGA work split - a classical memory-hierarchy design in the control path.
- **Gate 3 (heterogeneous relevance):** Directly informs the real-time classical control layer between a host and a QPU.
- **Contribution:** SmartQCache: near-quantum cache design on FPGA with combined compute-in-CPU and all-in-FPGA pulse synthesis for fast, precise pulse control.
- **Performance claim / baseline:** Lower synthesis latency with maintained control precision; figures truncated (BASELINE = Qiskit Pulse CPU synthesis and QuMA-style FPGA synthesis).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Strongest control-plane record in TCAD; sits at the classical-hardware/QPU boundary.

#### TCAD-024 — Effective and Efficient Parallel Qubit Mapper

- **DOI** `10.1109/tcad.2024.3500784` · **census year** 2024 · volume 44, issue 5, pp 1774-1787 · **issue date** 2025-5 · **online first** 2024-11-18
- **First author** Hao Fu (+6 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Mapping and routing is described as a time-consuming process; circuit depth and mapper runtime are both targets.
- **Gate 2 (systems technique):** Parallel mapper design - explicitly an INCLUDE shape (parallel compiler) in CRITERIA.md.
- **Gate 3 (heterogeneous relevance):** Informs compilation throughput in a hybrid stack where compile time competes with device time.
- **Contribution:** Parallel qubit mapper built on two extracted patterns from existing greedy mappers, targeting circuit depth at reduced mapping time.
- **Performance claim / baseline:** Better depth at lower mapping time than compared greedy mappers; figures truncated (BASELINE = existing greedy mappers).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Clearest parallel-compilation record in the four journals.

#### TCAD-027 — Shuttling for Scalable Trapped-Ion Quantum Computers

- **DOI** `10.1109/tcad.2024.3513262` · **census year** 2024 · volume 44, issue 6, pp 2144-2155 · **issue date** 2025-6 · **online first** 2024-12-09
- **First author** Daniel Schoenberger (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv `2402.14065`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch** architecture_control, compiler_mapping_routing
- **Gate 1 (classical systems problem):** Data movement and latency: ion shuttling time inside a QCCD device competes with coherence time.
- **Gate 2 (systems technique):** Scheduling/ordering of physical qubit movement across zones in a modular architecture - a data-movement optimisation problem.
- **Gate 3 (heterogeneous relevance):** Informs modular/segmented QPU architectures and the movement costs that a compiler and runtime must manage.
- **Contribution:** Shuttling schedules for QCCD trapped-ion architectures that reduce the time qubits spend being moved between memory and processing zones.
- **Performance claim / baseline:** Reduced shuttling time/overhead versus prior shuttling approaches; figures truncated (BASELINE = existing QCCD shuttling schedulers).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2402.14065
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** Modular-architecture data movement; the closest TCAD record to a memory-hierarchy problem.

#### TCAD-030 — DasAtom: A Divide-and-Shuttle Atom Approach to Quantum Circuit Transformation

- **DOI** `10.1109/tcad.2025.3532818` · **census year** 2025 · volume 44, issue 8, pp 2966-2978 · **issue date** 2025-8 · **online first** 2025-01-22
- **First author** Yunqi Huang (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv `2409.03185`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing, architecture_control
- **Gate 1 (classical systems problem):** Circuit partitioning plus physical movement of atoms - partition size and movement cost are the resource quantities.
- **Gate 2 (systems technique):** Divide-and-shuttle compilation: partition the circuit into subcircuits, each with a mapping, and move qubits between partitions.
- **Gate 3 (heterogeneous relevance):** Informs architecture-aware compilation for a platform whose qubits are physically relocatable.
- **Contribution:** DasAtom: divide-and-shuttle circuit transformation for neutral-atom devices exploiting long-range interaction and atom movement.
- **Performance claim / baseline:** Better fidelity/transformation cost than compared neutral-atom compilers; figures truncated (BASELINE = existing NA compilation methods).
- **Evidence basis:** ABSTRACT_TRUNCATED+WEB_SEARCH
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2409.03185
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** arXiv 2409.03185 preprint confirmed to exist by search; no public code repository identified.

#### TCAD-033 — Circuit Partitioning and Transmission Cost Optimization in Distributed Quantum Circuits

- **DOI** `10.1109/tcad.2025.3547812` · **census year** 2025 · volume 44, issue 9, pp 3350-3362 · **issue date** 2025-9 · **online first** 2025-03-04
- **First author** Xinyu Chen (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv `2407.05953`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch** multi_qpu_distributed_qc, compiler_mapping_routing
- **Gate 1 (classical systems problem):** Communication complexity: the number of quantum state transmissions between partitions is the optimised quantity.
- **Gate 2 (systems technique):** QUBO-based circuit partitioning plus a lookahead method for transmission-cost optimisation.
- **Gate 3 (heterogeneous relevance):** Directly informs multi-QPU distributed execution and its interconnect cost.
- **Contribution:** Circuit partitioning via a QUBO model with lookahead-based transmission-cost optimisation for distributed quantum circuits.
- **Performance claim / baseline:** Reduced transmission cost versus prior partitioning methods; figures truncated (BASELINE = existing DQC partitioning approaches).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2407.05953
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Core multi-QPU communication record in TCAD.

#### TCAD-043 — Computational Performance Bounds Prediction in Quantum Computing With Unstable Noise

- **DOI** `10.1109/tcad.2025.3592605` · **census year** 2025 · volume 45, issue 2, pp 969-982 · **issue date** 2026-2 · **online first** 2025-07-24
- **First author** Jinyang Li (+5 co-authors) · institution NOT_IN_DOSSIER · arXiv `2507.17043`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** Q_IN_HPC, FUTURE_WORKLOAD · **Branch** benchmarking_performance_modeling, qpu_scheduling_resource_mgmt
- **Gate 1 (classical systems problem):** Performance modelling and job scheduling: the abstract states that quantum-centric supercomputing needs noise characterisation to support system management such as job scheduling.
- **Gate 2 (systems technique):** Predictive performance-bound modelling under unstable noise, framed as a system-management input.
- **Gate 3 (heterogeneous relevance):** Directly informs scheduling and job placement in a quantum-centric supercomputing centre.
- **Contribution:** Method for predicting computational performance bounds (fidelity) of quantum jobs on devices with unstable noise, aimed at supporting device selection and scheduling.
- **Performance claim / baseline:** Prediction accuracy of performance bounds across devices/time; figures truncated (BASELINE = existing noise characterisation/fidelity prediction).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2507.17043
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** The clearest Q_IN_HPC record in TCAD; explicitly frames itself against quantum-centric supercomputing system management.

#### TCAD-050 — DMapS: End-to-End Qubit Mapping and Routing for Distributed Quantum Computing Architectures

- **DOI** `10.1109/tcad.2025.3611153` · **census year** 2025 · volume 45, issue 5, pp 2095-2108 · **issue date** 2026-5 · **online first** 2025-09-17
- **First author** Tingyu Luo (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch** multi_qpu_distributed_qc, compiler_mapping_routing
- **Gate 1 (classical systems problem):** Remote communication cost between chips plus intra-chip execution cost; mapping is parallelised across chips.
- **Gate 2 (systems technique):** End-to-end mapping and routing algorithms for DQC with a two-stage decomposition and parallel per-chip mapping.
- **Gate 3 (heterogeneous relevance):** Directly informs multi-chip/multi-QPU execution efficiency.
- **Contribution:** DMapS: end-to-end qubit mapping (DMapS-M) and routing for distributed quantum computing architectures, decomposing large circuits and parallelising mapping across chips.
- **Performance claim / baseline:** Joint reduction of remote-communication and intra-chip execution cost; figures truncated (BASELINE = prior DQC mapping/routing).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Combines the multi-QPU and parallel-compilation limbs in one record.

#### TCAD-051 — Approximation Methods for Simulation and Equivalence Checking of Noisy Quantum Circuits

- **DOI** `10.1109/tcad.2025.3623498` · **census year** 2025 · volume 45, issue 6, pp 2679-2692 · **issue date** 2026-6 · **online first** 2025-10-20
- **First author** Mingyu Huang (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv `2503.10340`
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** simulation_verification_scaling
- **Gate 1 (classical systems problem):** State-space explosion and memory/compute cost of simulating and checking noisy circuits; scalability in qubit count is the stated limit.
- **Gate 2 (systems technique):** Tensor-network representation with SVD-based approximation of noise tensors, implemented on Google's TensorNetwork library.
- **Gate 3 (heterogeneous relevance):** Informs the classical simulation/verification workload that HPC resources must carry for quantum development.
- **Contribution:** Approximation algorithm using a tensor-network diagram plus SVD to simulate and equivalence-check noisy circuits at larger qubit counts under low noise.
- **Performance claim / baseline:** Improved scalability versus exact noisy simulation/equivalence checking; figures truncated (BASELINE = exact density-matrix/decision-diagram methods).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2503.10340
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Notes:** Built on the TensorNetwork Python library; artifact status not verified.

#### TCAD-057 — A Framework for Dynamic Quantum Circuit Execution: Balancing Effectiveness and Efficiency

- **DOI** `10.1109/tcad.2025.3626447` · **census year** 2025 · volume 45, issue 6, pp 2583-2596 · **issue date** 2026-6 · online-first date not recorded
- **First author** Fangzheng Chen (+5 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing, quantum_runtime_orchestration
- **Gate 1 (classical systems problem):** Runtime decision-making: controlled subcircuits are known only after mid-circuit measurement, so mapping/routing decisions must be made under a time budget; the paper frames the trade-off as effectiveness versus efficiency.
- **Gate 2 (systems technique):** Execution framework for dynamic circuits spanning compilation and conditional control flow.
- **Gate 3 (heterogeneous relevance):** Informs the real-time classical control-flow path between measurement and subsequent gate execution.
- **Contribution:** Framework for executing dynamic quantum circuits with mid-circuit measurement and measurement-dependent controlled subcircuits, balancing routing quality against decision cost.
- **Performance claim / baseline:** Trade-off between transformation quality and processing time; figures truncated (BASELINE = static mapping/routing applied to dynamic circuits).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Census-year correction:** Census year corrected 2026 -> 2025: OpenAlex publication_date 2025-10-28; the 2026-06 issue cover date was used in error.
- **Notes:** Census year 2026 by online-first convention while the issue is 2026-6.

#### TCAD-062 — qfusion-opt: Profile-Informed Gate Scheduling and Fusion Optimization for Accelerating Quantum Circuit Simulation

- **DOI** `10.1109/tcad.2026.3680784` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Po-Hsuan Huang (+6 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** NO_ABSTRACT
- **Scenario** HPC_FOR_Q · **Branch** simulation_verification_scaling
- **Gate 1 (classical systems problem):** Simulation throughput: the title states the goal is accelerating quantum circuit simulation through gate scheduling and fusion.
- **Gate 2 (systems technique):** Profile-informed scheduling plus gate fusion, i.e. classical performance optimisation of a simulator kernel.
- **Gate 3 (heterogeneous relevance):** Informs how simulation workloads are optimised on classical hardware.
- **Contribution:** qfusion-opt: profile-informed gate scheduling and fusion optimisation for quantum circuit simulation (title evidence only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE (no abstract retrieved; IEEE and Semantic Scholar returned no abstract).
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** NO_ABSTRACT, IEEE Early Access. The title alone settles all three gates (simulation acceleration via scheduling/fusion); target hardware (CPU vs GPU) and measured speedups require the full text.

### TPDS (2)

#### TPDS-007 — Minimizing Communications of Quantum Circuit Simulations on Distributed Systems

- **DOI** `10.1109/tpds.2026.3652733` · **census year** 2026 · volume 37, issue 4, pp 775-786 · **issue date** 2026-4 · **online first** 2026-01-12
- **First author** Longshan Xu (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** distributed_gpu_simulation, benchmarking_performance_modeling
- **Gate 1 (classical systems problem):** Communication overhead on multi-node distributed systems is identified as the performance bottleneck of full-state simulation; memory capacity forces the distribution.
- **Gate 2 (systems technique):** Distributed simulation framework: level-by-level execution with a hybrid scheme that replaces intermediate multi-level communication by a single final merge.
- **Gate 3 (heterogeneous relevance):** Directly informs how a large classical cluster executes the quantum-simulation workload.
- **Contribution:** QuanTrans: distributed full-state simulation framework that restructures inter-node communication for circuits with particular structures, reducing communication volume.
- **Performance claim / baseline:** Reduced communication volume and runtime versus level-by-level distributed simulation; figures truncated (BASELINE = conventional distributed state-vector simulators).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** One of only two TPDS records that pass the gates; both are distributed state-vector simulation and both are census-year 2026.

#### TPDS-008 — Communication-Partition Co-Optimization for Quantum Circuit Simulation on CPU+GPU Clusters

- **DOI** `10.1109/tpds.2026.3678345` · **census year** 2026 · volume 37, issue 6, pp 1280-1294 · **issue date** 2026-6 · **online first** 2026-03-30
- **First author** Chenyang Jiao (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INCLUDED · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** distributed_gpu_simulation
- **Gate 1 (classical systems problem):** Memory footprint, memory-access cost and inter-node data communication dominate over compute; full-data exchange per gate is the stated inefficiency.
- **Gate 2 (systems technique):** Co-optimisation of communication and state partitioning on CPU+GPU clusters, exploiting gate-awareness and data locality.
- **Gate 3 (heterogeneous relevance):** Directly informs heterogeneous CPU+GPU cluster execution of simulation workloads.
- **Contribution:** Communication-partition co-optimisation for state-vector simulation on CPU+GPU clusters, replacing gate-unaware full-data exchange.
- **Performance claim / baseline:** Reduced communication time versus gate-unaware full-data communication as in QuEST; figures truncated (BASELINE = QuEST-style serial gate execution).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Explicit CPU+GPU cluster target; the strongest heterogeneous-simulation record among the four journals.

### JPDC (1)

#### JPDC-007 — Comprehensive overview of quantum serverless: Elastic integration of quantum and classical computing

- **DOI** `10.1016/j.jpdc.2026.105303` · **census year** 2026 · volume 216, no issue number, pp 105303 · **issue date** 2026-10 · **online first** 2026-06-22
- **First author** Dimitar Mileski (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** REVIEW_SURVEY · **verdict** INCLUDED · **BIBLIOGRAPHY_HUB** · **abstract** NO_ABSTRACT
- **Scenario** Q_IN_HPC, HPC_FOR_Q · **Branch** hpc_qpu_integration, quantum_runtime_orchestration, hybrid_workflow
- **Gate 1 (classical systems problem):** Queue handling, backend binding, orchestration of classical and quantum stages, near-real-time responsiveness and production maturity are the survey's evaluation axes.
- **Gate 2 (systems technique):** Consolidates a reference architecture for Quantum Serverless and evaluates 18 quantum cloud platforms against a KPI framework covering ecosystem coverage, service operability, queue handling, pricing flexibility, near-real-time readiness and production maturity.
- **Gate 3 (heterogeneous relevance):** Directly informs how QPUs are exposed as managed services alongside classical compute - the middleware layer of heterogeneous systems.
- **Contribution:** Survey of Quantum Serverless: a unified reference architecture plus a KPI-driven evaluation of 18 quantum cloud platforms, concluding that current offerings are best described as a queue-driven hybrid orchestration model rather than a mature cloud-native serverless layer.
- **Performance claim / baseline:** Not applicable (survey). The maturity assessment is the finding; BASELINE = serverless characteristics of classical cloud platforms (FaaS/CaaS, near-real-time responsiveness, production readiness).
- **Evidence basis:** PUBLISHER_PAGE_FETCHED (abstract retrieved from ScienceDirect; the dossier record had NO_ABSTRACT)
- **Artifact:** NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Notes:** Publisher labels it a research article; the content is a survey, so it is classified REVIEW_SURVEY and tagged BIBLIOGRAPHY_HUB. It therefore does not count toward the included original-research population. This is the only JPDC record in three years that addresses quantum-classical orchestration.

## 4. BORDERLINE and unresolved records

### TC (6)

#### TC-010 — Feynman Meets Turing: The Uncomputability of Quantum Gate-Circuit Emulation and Concatenation

- **DOI** `10.1109/tc.2024.3506861` · **census year** 2024 · volume 74, issue 3, pp 1053-1065 · **issue date** 2025-3 · **online first** 2024-11-27
- **First author** Holger Boche (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Addresses whether the classical machines that control quantum hardware can compute circuit emulation/concatenation at all - a computability statement about the compilation stage, not a measured cost.
- **Gate 2 (systems technique):** No HPC/systems technique; the method is computability theory (Turing-machine model).
- **Gate 3 (heterogeneous relevance):** Bears on the software stack in principle (which compiler tasks are algorithmically realisable on digital hardware).
- **Contribution:** Proves uncomputability results for quantum gate-circuit emulation (QGCE) and concatenation (QGCC) on digital hardware.
- **Performance claim / baseline:** Not applicable (theoretical).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Constrains what the classical compilation layer can compute at all, which bears on the software stack.
- **Borderline — reason against:** The method is computability theory and no classical systems quantity is measured, so Gate 2 fails.
- **Notes:** Kept as BORDERLINE because it constrains what the classical compilation layer can do; fails Gate 2 as stated.

#### TC-016 — Towards Effective Local Search for Qubit Mapping

- **DOI** `10.1109/tc.2025.3544869` · **census year** 2025 · volume 74, issue 6, pp 1897-1910 · **issue date** 2025-6 · **online first** 2025-02-21
- **First author** Chuan Luo (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Qubit mapping is framed as an NP-hard optimisation solved by local search; search effort is a classical computation cost but the reported objective is auxiliary-gate count.
- **Gate 2 (systems technique):** Local-search algorithm engineering (mode-aware strategy) rather than a systems/parallelism technique.
- **Gate 3 (heterogeneous relevance):** Weak: informs compiler quality, not resource usage or execution on a heterogeneous system.
- **Contribution:** EffectiveQM: local-search qubit mapping with a mode-aware search strategy to escape local optima.
- **Performance claim / baseline:** Fewer inserted gates than compared mappers; figures truncated (BASELINE = prior qubit-mapping heuristics).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Qubit mapping is an NP-hard classical optimisation, and search effort is a classical computation cost.
- **Borderline — reason against:** The reported objective is auxiliary-gate count, a quantum resource; no compile-time or parallelism result is claimed.
- **Notes:** Gate-count-driven mapping: BORDERLINE per the quantum-compilation rule in CRITERIA.md.

#### TC-017 — RSQC: Recursive Sparse QUBO Construction for Quantum Annealing Machines

- **DOI** `10.1109/tc.2025.3557965` · **census year** 2025 · volume 74, issue 6, pp 2114-2128 · **issue date** 2025-6 · **online first** 2025-04-04
- **First author** Jianwen Luo (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, Q_FOR_HPC · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Problem size that fits on the hardware: dense QUBO topology and complicated weights limit solvable instance size on real annealers.
- **Gate 2 (systems technique):** A classical mapping/compilation framework (recursive constraint decomposition into Boolean gates and small cliques) producing hardware-friendly sparse embeddings.
- **Gate 3 (heterogeneous relevance):** Informs how a quantum annealer can be driven as an accelerator, but the target hardware is an annealer rather than a gate-based QPU in an HPC stack.
- **Contribution:** RSQC: recursive sparse QUBO construction mapping general constraints to sparse, hardware-friendly annealer topologies.
- **Performance claim / baseline:** Larger solvable problem sizes and sparser topologies than existing QUBO mappings; figures truncated (BASELINE = prior QUBO construction methods).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** A classical mapping/compilation framework that determines what problem size fits on the target hardware.
- **Borderline — reason against:** The target is a quantum annealer and the measured quantity is embedding sparsity/problem size, adjacent to false-positive class 2.
- **Notes:** Recorded rather than included: it is annealer-embedding compilation; adjacent to, but not inside, the CPU/GPU-QPU systems question.

#### TC-027 — Feynman Meets Turing: Computability Aspects of Quantum Compiling Revisited

- **DOI** `10.1109/tc.2025.3626469` · **census year** 2025 · volume 75, issue 2, pp 516-526 · **issue date** 2026-2 · **online first** 2025-10-28
- **First author** Yannik N. Böck (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Same limb as TC-010: realisability of compiler functions on digital hardware.
- **Gate 2 (systems technique):** Computability theory, not a systems technique.
- **Gate 3 (heterogeneous relevance):** Bears on the software stack in principle.
- **Contribution:** Proves that quantum compiler functions mapping unitaries to gate-circuit approximations are not digitally computable in general, revisiting Solovay-Kitaev from a computability angle.
- **Performance claim / baseline:** Not applicable (theoretical).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** NO_PUBLIC_ARTIFACT_FOUND
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Same limb as TC-010: realisability of compiler functions on digital hardware.
- **Borderline — reason against:** Theoretical result with no classical systems technique or measurement, so Gate 2 fails.
- **Notes:** Companion to TC-010 ('Feynman Meets Turing' series, same group); lineage is to the earlier TC article, not to a conference. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the only evidence is a companion article in the same journal ('Feynman Meets Turing', TC-010, same group), which is not a prior conference paper.

#### TC-029 — Dynamic Quantum Circuit Compilation

- **DOI** `10.1109/tc.2025.3643826` · **census year** 2025 · volume 75, issue 2, pp 748-759 · **issue date** 2026-2 · **online first** 2025-12-15
- **First author** Kun Fang (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv `2310.11021`
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Qubit resource allocation via reuse; the compilation task is characterised and its optimal strategies analysed, but classical compile cost is not the reported metric.
- **Gate 2 (systems technique):** Graph-based optimisation framework for qubit-reuse compilation.
- **Gate 3 (heterogeneous relevance):** Informs how many physical qubits a workload needs, i.e. resource usage on a shared device.
- **Contribution:** Graph-based framework for dynamic-circuit compilation via qubit reuse, with characterisation of optimal compilation strategies.
- **Performance claim / baseline:** Reduced qubit requirements versus static circuits; figures truncated (BASELINE = static circuit compilation).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2310.11021
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Qubit reuse is a resource-allocation mechanism and the compilation task is characterised formally.
- **Borderline — reason against:** The measured quantity is qubit count, a quantum resource; classical compile cost is not reported.
- **Notes:** arXiv 2310.11021 preprint exists (recorded in the dossier); artifact_url points at the preprint, not at verified code.

#### TC-031 — QuanGuard: Error Evolution-Based Fingerprinting for Fraud Detection in Quantum Cloud Services

- **DOI** `10.1109/tc.2025.3645773` · **census year** 2025 · volume 75, issue 3, pp 1070-1081 · **issue date** 2026-3 · **online first** 2025-12-17
- **First author** Jindi Wu (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** Q_IN_HPC · **Branch** qpu_scheduling_resource_mgmt, architecture_control
- **Gate 1 (classical systems problem):** Resource allocation and scheduling in a quantum cloud: providers reassign jobs across devices to maximise throughput, users pay for specific devices.
- **Gate 2 (systems technique):** A runtime verification mechanism (probing circuits plus device fingerprints) layered on the cloud scheduling/allocation path.
- **Gate 3 (heterogeneous relevance):** Informs QPU resource management, job placement transparency and accounting in shared quantum-cloud infrastructure.
- **Contribution:** QuanGuard: fingerprinting framework that uses device-specific error-evolution patterns from probing circuits to verify which physical device executed a submitted job.
- **Performance claim / baseline:** Identification accuracy of allocated devices; numbers truncated in the dossier abstract (BASELINE_UNCLEAR).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Verdict history:** INCLUDED -> BORDERLINE (verification pass, accepted)
- **Borderline — reason for:** It is the only record in these four journals that engages the quantum-cloud allocation and accounting layer at all, so it remains relevant to QPU resource management as a recorded BORDERLINE.
- **Borderline — reason against:** The reported metric is device-identification accuracy, a classification-accuracy quantity, and the contribution is a fingerprinting technique built from probing-circuit error patterns. The cloud allocation and throughput behaviour is the setting, not a quantity the paper improves, so Gate 2 is not met.
- **Notes:** The only TC record in the corpus that addresses the quantum-cloud service/scheduling layer rather than compilation or simulation. DEMOTED on verification: INCLUDED -> BORDERLINE. Accepted - Gate 1 was carried by framing rather than by a quantity the paper measures.

### TCAD (15)

#### TCAD-001 — Low-Rank Quantum State Preparation

- **DOI** `10.1109/tcad.2023.3297972` · **census year** 2024 · volume 43, issue 1, pp 161-170 · **issue date** 2024-1 · online-first date not recorded
- **First author** Israel F. Araujo (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv `2111.03132`
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Explicitly offloads computational complexity from the circuit to a classical computer, so classical preprocessing cost is part of the design - but that cost is not measured.
- **Gate 2 (systems technique):** Low-rank/Schmidt decomposition preprocessing; a numerical-algorithm contribution rather than a systems one.
- **Gate 3 (heterogeneous relevance):** Weak: informs the classical side of data loading.
- **Contribution:** Low-rank approximation approach to quantum state preparation that trades circuit depth for classical preprocessing.
- **Performance claim / baseline:** Lower circuit depth for approximate preparation; BASELINE = variational/fixed-depth state-preparation methods.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2111.03132
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Explicitly offloads complexity from the circuit to a classical computer, so classical preprocessing is part of the design.
- **Borderline — reason against:** That classical cost is never measured; the reported quantity is circuit depth.
- **Notes:** Classical-offload framing is the only systems limb.

#### TCAD-006 — Small Sampling Overhead Error Mitigation for Quantum Circuits

- **DOI** `10.1109/tcad.2023.3329042` · **census year** 2024 · volume 43, issue 3, pp 826-839 · **issue date** 2024-3 · online-first date not recorded
- **First author** Cheng-Yun Hsieh (+3 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** benchmarking_performance_modeling
- **Gate 1 (classical systems problem):** Sampling overhead (number of circuit executions) grows exponentially with mitigated gate count - an execution/throughput cost on the device.
- **Gate 2 (systems technique):** Error-mitigation technique (parameterised-gate PEC and overhead reduction), not an HPC/systems technique.
- **Gate 3 (heterogeneous relevance):** Informs shot budget and therefore device occupancy, indirectly.
- **Contribution:** Parameterised-gate probabilistic error cancellation plus two approaches to reducing sampling overhead.
- **Performance claim / baseline:** 97%+ reduction in the number of gates requiring characterisation over a thousand random circuits; BASELINE = original PEC requiring full gate characterisation.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Sampling overhead is an execution/throughput cost on the device, and the characterisation reduction is measured.
- **Borderline — reason against:** The contribution is an error-mitigation technique, not a systems technique; Gate 2 is met only indirectly.
- **Notes:** Recorded because shot/sampling cost is a throughput quantity; the contribution itself is error mitigation.

#### TCAD-007 — Noise Adaptive Quantum Circuit Mapping Using Reinforcement Learning and Graph Neural Network

- **DOI** `10.1109/tcad.2023.3340608` · **census year** 2024 · volume 43, issue 5, pp 1374-1386 · **issue date** 2024-5 · online-first date not recorded
- **First author** Vedika Saravanan (+1 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** No stated compile-cost or scalability metric; the objective is output fidelity.
- **Gate 2 (systems technique):** RL agent plus GNN reliability predictor - machine-learning method applied to mapping.
- **Gate 3 (heterogeneous relevance):** Weak.
- **Contribution:** Noise-adaptive mapping where an RL policy is trained against a GNN-based reliability predictor instead of a fixed noise model.
- **Performance claim / baseline:** Improved output fidelity of mapped circuits; BASELINE = noise-aware mapping with static noise models.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Mapping is a compiler stage and the RL/GNN pipeline is a substantial classical apparatus.
- **Borderline — reason against:** The objective is output fidelity, a quantum resource; no compile-cost or scalability result is claimed.
- **Notes:** Fidelity-only mapping: BORDERLINE per the quantum-compilation rule.

#### TCAD-012 — Efficient Qubit Routing Using a Dynamically Extract-and-Route Framework

- **DOI** `10.1109/tcad.2024.3387290` · **census year** 2024 · volume 43, issue 10, pp 2978-2989 · **issue date** 2024-10 · **online first** 2024-04-10
- **First author** Ching-Yao Huang (+1 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** 'Minimal overheads' refers to inserted gates and fidelity, not to compilation time or memory.
- **Gate 2 (systems technique):** Routing heuristic (dynamic extract-and-route), algorithmic rather than systems.
- **Gate 3 (heterogeneous relevance):** Weak.
- **Contribution:** DEAR: dynamically extract-and-route framework coupling initial mapping and routing.
- **Performance claim / baseline:** Fewer additional gates than compared transformation methods; BASELINE = prior circuit-transformation methods.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Routing is a compiler stage with a stated overhead budget.
- **Borderline — reason against:** The overhead measured is inserted gates and fidelity, not compilation time or memory.

#### TCAD-025 — CAMEL: Physically Inspired Crosstalk-Aware Mapping and Gate Scheduling for Frequency-Tunable Quantum Chips

- **DOI** `10.1109/tcad.2024.3507580` · **census year** 2024 · volume 44, issue 5, pp 1968-1980 · **issue date** 2025-5 · **online first** 2024-11-27
- **First author** Bin-Han Lu (+7 co-authors) · institution NOT_IN_DOSSIER · arXiv `2311.18160`
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing, architecture_control
- **Gate 1 (classical systems problem):** Parallel execution of two-qubit gates and the scheduling constraints imposed by crosstalk and decoherence.
- **Gate 2 (systems technique):** Two-step compilation framework: crosstalk-aware mapping plus gate scheduling with pulse compensation.
- **Gate 3 (heterogeneous relevance):** Informs how instruction-level parallelism is scheduled on a QPU, the quantum analogue of execution scheduling.
- **Contribution:** CAMEL: crosstalk-aware mapping and gate scheduling for frequency-tunable superconducting chips, exploiting tunable-coupler physics plus pulse compensation.
- **Performance claim / baseline:** Reduced crosstalk and decoherence effects under parallel two-qubit operation; figures truncated (BASELINE = prior crosstalk mitigation and mapping approaches).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2311.18160
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Verdict history:** INCLUDED -> BORDERLINE (verification pass, accepted)
- **Borderline — reason for:** Crosstalk-aware gate scheduling does govern which operations may execute concurrently, which is an execution-parallelism mechanism worth retaining in the record.
- **Borderline — reason against:** The measured quantity is gate fidelity under parallel two-qubit operation - a quantum resource, not a classical systems quantity. Gate scheduling here is the means to a fidelity objective, so under the decision rule stated in this census (fidelity-objective mapping -> BORDERLINE) it does not pass Gate 2.
- **Notes:** Included on the scheduling/parallel-execution limb; the objective is fidelity, so the systems content is in the scheduler. DEMOTED on verification: INCLUDED -> BORDERLINE. Accepted - the original verdict contradicted this census's own stated rule, which is applied to TCAD-007 and TCAD-012.

#### TCAD-026 — PauliForest: Connectivity-Aware Synthesis and Pauli-Oriented Qubit Mapping for Near-Term Quantum Simulation

- **DOI** `10.1109/tcad.2024.3509794` · **census year** 2024 · volume 44, issue 6, pp 2119-2129 · **issue date** 2025-6 · **online first** 2024-12-02
- **First author** Yongshang Li (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Circuit depth of simulation kernels under connectivity constraints; no compile-cost or parallelism metric stated.
- **Gate 2 (systems technique):** Joint synthesis-plus-mapping algorithm for Pauli-based simulation kernels.
- **Gate 3 (heterogeneous relevance):** Informs compilation of the Hamiltonian-simulation workload, but through circuit quality.
- **Contribution:** PauliForest: connectivity-aware synthesis plus Pauli-oriented qubit mapping for quantum simulation kernels.
- **Performance claim / baseline:** Lower depth/gate count than separate synthesis and mapping; BASELINE = existing synthesis and mapping combinations.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Compiles the Hamiltonian-simulation kernels that dominate many workloads, coupling synthesis with mapping.
- **Borderline — reason against:** The reported quantities are depth and gate count; no compile-cost, parallelism or scheduling result is claimed.

#### TCAD-037 — A Divide-And-Conquer Pebbling Strategy for Oracle Synthesis in Quantum Computing

- **DOI** `10.1109/tcad.2025.3570608` · **census year** 2025 · volume 44, issue 12, pp 4601-4614 · **issue date** 2025-12 · **online first** 2025-05-15
- **First author** Kezhen Zhang (+2 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** Space-time trade-off in compilation: ancilla (memory) usage versus gate count, governed by the reversible pebble game; the method is presented as scalable for large oracles.
- **Gate 2 (systems technique):** Divide-and-conquer strategy over the pebbling schedule - an algorithmic scheduling contribution inside the compiler.
- **Gate 3 (heterogeneous relevance):** Informs qubit-memory usage of compiled workloads.
- **Contribution:** Divide-and-conquer pebbling strategy for hierarchical reversible-logic oracle synthesis.
- **Performance claim / baseline:** Up to 90% reduction in qubits compared with the most qubit-efficient prior method (as stated); gate-count cost described as reasonable.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** The pebble game is a space-time scheduling problem inside the compiler, and the method is presented as scalable.
- **Borderline — reason against:** The resource traded is qubits against gate count, both quantum resources; no classical systems quantity is measured.
- **Notes:** Scheduling/memory trade-off inside synthesis; recorded rather than included because the resource is qubits, not classical systems resources.

#### TCAD-038 — Special-Purpose Coherent Optical Quantum Computers Empower Qubit Mapping Optimization in General-Purpose Superconducting Quantum Computing

- **DOI** `10.1109/tcad.2025.3572021` · **census year** 2025 · volume 45, issue 1, pp 59-68 · **issue date** 2026-1 · **online first** 2025-06-02
- **First author** Xiaohan Yu (+7 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, Q_FOR_HPC · **Branch** compiler_mapping_routing, hpc_qpu_integration
- **Gate 1 (classical systems problem):** Compilation cost: qubit layout mapping is offloaded, as a QUBO, to a special-purpose optimisation machine.
- **Gate 2 (systems technique):** Heterogeneous offload of an EDA/compiler workload to an accelerator (coherent optical Ising machine), with post-processing on the host.
- **Gate 3 (heterogeneous relevance):** A concrete instance of a special-purpose accelerator serving the classical compilation stage of a general-purpose QPU workflow.
- **Contribution:** Formulates qubit layout mapping for IBM heavy-hex topology as a QUBO and solves it on a QBoson 550w coherent optical Ising machine, with classical post-processing.
- **Performance claim / baseline:** Mapping quality relative to conventional solvers on heavy-hex placement; figures truncated (BASELINE = conventional qubit-mapping optimisation).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Verdict history:** INCLUDED -> BORDERLINE (verification pass, accepted)
- **Borderline — reason for:** The workload being offloaded is a real compilation task for a gate-based QPU, and heterogeneous offload of a compiler stage is systems-relevant; it is recorded rather than excluded so the POSSIBLE_CROSSOVER is not lost.
- **Borderline — reason against:** The accelerator carrying the offloaded work is a QBoson coherent optical Ising machine solving a QUBO, which CRITERIA.md false-positive class 2 names explicitly (Ising machines, QUBO solvers). The measured quantity is qubit-mapping quality on heavy-hex placement, a quantum resource, so Gate 2 is not met by a classical systems technique.
- **Notes:** Unusual scenario mix: a special-purpose optimisation machine accelerating the compiler for a gate-based QPU (Q_FOR_HPC applied to an EDA workload). DEMOTED on verification: INCLUDED -> BORDERLINE. Accepted. Every other Ising/annealing record in this corpus sits at BORDERLINE (TC-017) or EXCLUDED (TC-032, TCAD-016, TCAD-060); treating this one as INCLUDED was inconsistent with false-positive class 2.

#### TCAD-040 — HeteroQNN: Enabling Distributed QNN Under Heterogeneous Quantum Devices

- **DOI** `10.1109/tcad.2025.3588457` · **census year** 2025 · volume 45, issue 2, pp 1007-1020 · **issue date** 2026-2 · **online first** 2025-07-11
- **First author** Liqiang Lu (+7 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q, Q_IN_HPC · **Branch** multi_qpu_distributed_qc, hybrid_workflow
- **Gate 1 (classical systems problem):** Distributed training and inference across heterogeneous, intermittently available quantum devices - a distributed-execution and device-heterogeneity problem.
- **Gate 2 (systems technique):** Framework decoupling QNN circuits into uniform representations to support distribution; the workload, however, is a QML model.
- **Gate 3 (heterogeneous relevance):** Informs execution across a pool of heterogeneous QPUs.
- **Contribution:** HeteroQNN: distributed QNN training/inference framework handling device heterogeneity and devices going online/offline.
- **Performance claim / baseline:** Higher accuracy and robustness under heterogeneous distributed execution; BASELINE = single-device and naive distributed QNN training.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Borderline — reason for:** Distributed training and inference across heterogeneous, intermittently available QPUs is a genuine distributed-execution problem.
- **Borderline — reason against:** The workload is a QNN and the reported metric is model accuracy, which sits in false-positive class 5.
- **Notes:** Sits across the QML false-positive class (FP5) and the distributed-execution include shape; recorded as BORDERLINE so the distributed-systems content is not lost and the count is not inflated.

#### TCAD-045 — Robust and Optimal Loading of General Classical Data Into Quantum Computers

- **DOI** `10.1109/tcad.2025.3600368` · **census year** 2025 · volume 45, issue 3, pp 1170-1181 · **issue date** 2026-3 · **online first** 2025-08-19
- **First author** Xiao-Ming Zhang (+0 co-authors) · institution NOT_IN_DOSSIER · arXiv `2411.02782`
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** architecture_control
- **Gate 1 (classical systems problem):** Data loading into a QPU (a data-movement bottleneck) under device imperfection; the design is an architecture (tree-like bucket brigade).
- **Gate 2 (systems technique):** Architectural fan-in structure limiting error propagation; circuit-architecture rather than classical-systems engineering.
- **Gate 3 (heterogeneous relevance):** Informs the input path of quantum accelerators (QRAM-style loading).
- **Contribution:** Bucket-brigade-style fan-in architecture for robust state preparation and block encoding.
- **Performance claim / baseline:** Exponentially improved robustness versus depth-optimal loading methods, at state-of-the-art depth; BASELINE = existing depth-optimal loading protocols.
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2411.02782
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **Borderline — reason for:** Data loading is a movement bottleneck on the input path of a quantum accelerator.
- **Borderline — reason against:** The contribution is a circuit-architecture robustness result measured in depth and error propagation, not a classical systems result.

#### TCAD-058 — A quantum circuit optimization framework for distributed quantum computing

- **DOI** `10.1109/tcad.2026.3656760` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Fengsheng Liu (+6 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** NO_ABSTRACT
- **Scenario** HPC_FOR_Q · **Branch** multi_qpu_distributed_qc, compiler_mapping_routing
- **Gate 1 (classical systems problem):** INSUFFICIENT_EVIDENCE from the title; distributed quantum computing implies partitioning/communication cost but no metric is visible.
- **Gate 2 (systems technique):** A circuit optimisation framework for DQC, i.e. compilation for a multi-chip target (title evidence only).
- **Gate 3 (heterogeneous relevance):** Would inform multi-QPU execution if the framework optimises communication.
- **Contribution:** Quantum circuit optimisation framework for distributed quantum computing (title evidence only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE (no abstract retrieved; Semantic Scholar record carries a null abstract).
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **Borderline — reason for:** Distributed-QC compilation is an INCLUDE shape and the title places the work squarely in it.
- **Borderline — reason against:** NO_ABSTRACT: no communication, partitioning or cost metric can be confirmed, so Gate 1 rests on the title alone.
- **Notes:** NO_ABSTRACT, IEEE Early Access. Held at BORDERLINE rather than INCLUDED because the title does not establish a communication/cost metric. Authors verified via Semantic Scholar (Feng-Sheng Liu et al., Zhengzhou).

#### TCAD-061 — Optimizing Unitary Coupled Cluster with Single and Double Kernels for Modern NISQ Architectures

- **DOI** `10.1109/tcad.2026.3677771` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Yongshang Li (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INSUFFICIENT_EVIDENCE · **abstract** NO_ABSTRACT
- **Scenario** INSUFFICIENT_EVIDENCE · **Branch** INSUFFICIENT_EVIDENCE
- **Gate 1 (classical systems problem):** INSUFFICIENT_EVIDENCE
- **Gate 2 (systems technique):** INSUFFICIENT_EVIDENCE
- **Gate 3 (heterogeneous relevance):** INSUFFICIENT_EVIDENCE
- **Contribution:** Optimisation of unitary coupled-cluster single/double kernels for NISQ architectures (title only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **What would resolve it:** Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3677771). The gates turn on whether the contribution is ansatz design for UCCSD (EXCLUDE under the VQE rule) or architecture-aware kernel compilation with a compile-cost or scheduling result (INCLUDE); the abstract or Section I would settle it.
- **Notes:** NO_ABSTRACT, IEEE Early Access. The title is compatible with both an excluded shape (ansatz design, VQE rule) and an included shape (architecture-aware kernel compilation, cf. TCAD-026 by the same first author). Not resolvable without the full text; no abstract available from IEEE or Semantic Scholar.

#### TCAD-063 — Advancing Quantum State Preparation Using Decision Diagram with Local Invertible Maps

- **DOI** `10.1109/tcad.2026.3681225` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Xin Hong (+5 co-authors) · institution NOT_IN_DOSSIER · arXiv `2507.17170`
- **Article type** ORIGINAL_RESEARCH · **verdict** BORDERLINE · **abstract** ABSTRACT_PRESENT_TRUNCATED_700CHAR
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing, simulation_verification_scaling
- **Gate 1 (classical systems problem):** Compactness of the classical representation (LimTDD decision diagrams combining tensor networks and decision diagrams) drives the synthesis result; classical runtime is not the reported metric.
- **Gate 2 (systems technique):** Decision-diagram data structure used inside a compiler, an INCLUDE-shaped data structure applied to a synthesis rather than a simulation task.
- **Gate 3 (heterogeneous relevance):** Informs the classical data structures underpinning the compilation stage.
- **Contribution:** Family of QSP algorithms parameterised by available ancillas, built on Local Invertible Map Tensor Decision Diagrams.
- **Performance claim / baseline:** Reduced circuit complexity across ancilla regimes; BASELINE = existing QSP algorithms (specific figures truncated).
- **Evidence basis:** ABSTRACT_TRUNCATED
- **Artifact:** UNKNOWN — https://arxiv.org/abs/2507.17170
- **Conference extension:** UNKNOWN · **Deep-dive priority:** MEDIUM
- **Borderline — reason for:** Decision diagrams combined with tensor networks are a classical data structure central to the result.
- **Borderline — reason against:** The reported quantity is circuit complexity; classical runtime or memory scalability is not reported.
- **Notes:** IEEE Early Access; abstract supplied in the dossier despite no volume/issue.

#### TCAD-064 — QDP: Worst-case Fidelity-aware Qubit Mapping and Routing using Dynamic Programming

- **DOI** `10.1109/tcad.2026.3693628` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Shui Jiang (+4 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INSUFFICIENT_EVIDENCE · **abstract** NO_ABSTRACT
- **Scenario** HPC_FOR_Q · **Branch** compiler_mapping_routing
- **Gate 1 (classical systems problem):** INSUFFICIENT_EVIDENCE - the title names worst-case fidelity as the objective and dynamic programming as the method, neither of which settles a classical systems cost.
- **Gate 2 (systems technique):** INSUFFICIENT_EVIDENCE
- **Gate 3 (heterogeneous relevance):** INSUFFICIENT_EVIDENCE
- **Contribution:** QDP: worst-case fidelity-aware qubit mapping and routing using dynamic programming (title only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** HIGH
- **What would resolve it:** Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3693628). The gates turn on whether the dynamic-programming mapper reports compilation time/memory scalability alongside worst-case fidelity; an evaluation-section check would settle it.
- **Notes:** NO_ABSTRACT, IEEE Early Access. Author list verified via Semantic Scholar (Shui Jiang, Wen Cheng, Yi-Hua Chung, Tsung-Yi Ho, Tsung-Wei Huang); abstract field null. Worth a full-text check because that group publishes parallel/GPU CAD algorithms, but group history is not evidence about this article.

#### TCAD-066 — Online Testing Error Mitigation for Quantum Computers

- **DOI** `10.1109/tcad.2026.3705986` · **census year** 2026 · IEEE Early Access (no volume/issue) · **issue date** 2026 · **online first** 2026-01-01
- **First author** Cheng-Yun Hsieh (+1 co-authors) · institution NOT_IN_DOSSIER · arXiv none recorded
- **Article type** ORIGINAL_RESEARCH · **verdict** INSUFFICIENT_EVIDENCE · **abstract** NO_ABSTRACT
- **Scenario** HPC_FOR_Q · **Branch** benchmarking_performance_modeling
- **Gate 1 (classical systems problem):** INSUFFICIENT_EVIDENCE - 'online testing' suggests runtime cost but the title does not state a systems metric.
- **Gate 2 (systems technique):** INSUFFICIENT_EVIDENCE
- **Gate 3 (heterogeneous relevance):** INSUFFICIENT_EVIDENCE
- **Contribution:** Online testing approach to error mitigation for quantum computers (title only).
- **Performance claim / baseline:** INSUFFICIENT_EVIDENCE
- **Evidence basis:** TITLE_ONLY_NO_ABSTRACT
- **Artifact:** UNKNOWN
- **Conference extension:** UNKNOWN · **Deep-dive priority:** LOW
- **What would resolve it:** Full text via IEEE Xplore (DOI 10.1109/tcad.2026.3705986). The gates turn on whether 'online' testing means runtime classical processing with a latency/overhead budget, or offline characterisation reported as fidelity only.
- **Notes:** NO_ABSTRACT, IEEE Early Access. Same first author as TCAD-006 (Cheng-Yun Hsieh), so a thematic continuation of that error-mitigation line is plausible; recorded as RELATED_LINEAGE within the journal, not as a conference extension. Conference lineage downgraded RELATED_LINEAGE -> UNKNOWN: the evidence was shared first authorship with TCAD-006 in the same journal, which is not a conference paper.

### TPDS (0)

No borderline or unresolved records.

### JPDC (0)

No borderline or unresolved records.

## 5. Artifact status

| ID | Journal | Title | Artifact status | Link recorded | arXiv |
|---|---|---|---|---|---|
| TC-004 | TC | A Mutual-Influence-Aware Heuristic Method for Quantum Circuit Mapping | UNKNOWN | — | — |
| TC-010 | TC | Feynman Meets Turing: The Uncomputability of Quantum Gate-Circuit Emul | NO_PUBLIC_ARTIFACT_FOUND | — | — |
| TC-011 | TC | Qu-Trefoil: Large-Scale Quantum Circuit Simulator Working on FPGA With | UNKNOWN | — | 2608.14285 |
| TC-016 | TC | Towards Effective Local Search for Qubit Mapping | UNKNOWN | — | — |
| TC-017 | TC | RSQC: Recursive Sparse QUBO Construction for Quantum Annealing Machine | UNKNOWN | — | — |
| TC-023 | TC | AdaptDQC: Adaptive Distributed Quantum Computing With Quantitative Per | UNKNOWN | — | — |
| TC-027 | TC | Feynman Meets Turing: Computability Aspects of Quantum Compiling Revis | NO_PUBLIC_ARTIFACT_FOUND | — | — |
| TC-029 | TC | Dynamic Quantum Circuit Compilation | UNKNOWN | https://arxiv.org/abs/2310.11021 | 2310.11021 |
| TC-030 | TC | SuperEncoder: Towards Efficient Neural Approximate Quantum State Prepa | UNKNOWN | — | — |
| TC-031 | TC | QuanGuard: Error Evolution-Based Fingerprinting for Fraud Detection in | UNKNOWN | — | — |
| TC-040 | TC | AMARETTO, Accelerating Quantum Algorithm Development With FPGA Emulati | UNKNOWN | — | — |
| TC-041 | TC | Quantum at the Edge: Scalable Standalone FPGA Emulator for QAOA–based  | UNKNOWN | — | — |
| TCAD-001 | TCAD | Low-Rank Quantum State Preparation | UNKNOWN | https://arxiv.org/abs/2111.03132 | 2111.03132 |
| TCAD-006 | TCAD | Small Sampling Overhead Error Mitigation for Quantum Circuits | UNKNOWN | — | — |
| TCAD-007 | TCAD | Noise Adaptive Quantum Circuit Mapping Using Reinforcement Learning an | UNKNOWN | — | — |
| TCAD-010 | TCAD | QuBEC: Boosting Equivalence Checking for Quantum Circuits With QEC Emb | UNKNOWN | — | 2309.10728 |
| TCAD-012 | TCAD | Efficient Qubit Routing Using a Dynamically Extract-and-Route Framewor | UNKNOWN | — | — |
| TCAD-014 | TCAD | QHLS: An HLS Framework to Convert High-Level Descriptions to Quantum C | UNKNOWN | — | — |
| TCAD-023 | TCAD | SmartQCache: Fast and Precise Pulse Control With Near-Quantum Cache De | UNKNOWN | — | — |
| TCAD-024 | TCAD | Effective and Efficient Parallel Qubit Mapper | UNKNOWN | — | — |
| TCAD-025 | TCAD | CAMEL: Physically Inspired Crosstalk-Aware Mapping and Gate Scheduling | UNKNOWN | https://arxiv.org/abs/2311.18160 | 2311.18160 |
| TCAD-026 | TCAD | PauliForest: Connectivity-Aware Synthesis and Pauli-Oriented Qubit Map | UNKNOWN | — | — |
| TCAD-027 | TCAD | Shuttling for Scalable Trapped-Ion Quantum Computers | UNKNOWN | https://arxiv.org/abs/2402.14065 | 2402.14065 |
| TCAD-030 | TCAD | DasAtom: A Divide-and-Shuttle Atom Approach to Quantum Circuit Transfo | UNKNOWN | https://arxiv.org/abs/2409.03185 | 2409.03185 |
| TCAD-033 | TCAD | Circuit Partitioning and Transmission Cost Optimization in Distributed | UNKNOWN | https://arxiv.org/abs/2407.05953 | 2407.05953 |
| TCAD-037 | TCAD | A Divide-And-Conquer Pebbling Strategy for Oracle Synthesis in Quantum | UNKNOWN | — | — |
| TCAD-038 | TCAD | Special-Purpose Coherent Optical Quantum Computers Empower Qubit Mappi | UNKNOWN | — | — |
| TCAD-040 | TCAD | HeteroQNN: Enabling Distributed QNN Under Heterogeneous Quantum Device | UNKNOWN | — | — |
| TCAD-043 | TCAD | Computational Performance Bounds Prediction in Quantum Computing With  | UNKNOWN | https://arxiv.org/abs/2507.17043 | 2507.17043 |
| TCAD-045 | TCAD | Robust and Optimal Loading of General Classical Data Into Quantum Comp | UNKNOWN | https://arxiv.org/abs/2411.02782 | 2411.02782 |
| TCAD-050 | TCAD | DMapS: End-to-End Qubit Mapping and Routing for Distributed Quantum Co | UNKNOWN | — | — |
| TCAD-051 | TCAD | Approximation Methods for Simulation and Equivalence Checking of Noisy | UNKNOWN | https://arxiv.org/abs/2503.10340 | 2503.10340 |
| TCAD-057 | TCAD | A Framework for Dynamic Quantum Circuit Execution: Balancing Effective | UNKNOWN | — | — |
| TCAD-058 | TCAD | A quantum circuit optimization framework for distributed quantum compu | UNKNOWN | — | — |
| TCAD-061 | TCAD | Optimizing Unitary Coupled Cluster with Single and Double Kernels for  | UNKNOWN | — | — |
| TCAD-062 | TCAD | qfusion-opt: Profile-Informed Gate Scheduling and Fusion Optimization  | UNKNOWN | — | — |
| TCAD-063 | TCAD | Advancing Quantum State Preparation Using Decision Diagram with Local  | UNKNOWN | https://arxiv.org/abs/2507.17170 | 2507.17170 |
| TCAD-064 | TCAD | QDP: Worst-case Fidelity-aware Qubit Mapping and Routing using Dynamic | UNKNOWN | — | — |
| TCAD-066 | TCAD | Online Testing Error Mitigation for Quantum Computers | UNKNOWN | — | — |
| TPDS-007 | TPDS | Minimizing Communications of Quantum Circuit Simulations on Distribute | UNKNOWN | — | — |
| TPDS-008 | TPDS | Communication-Partition Co-Optimization for Quantum Circuit Simulation | UNKNOWN | — | — |
| JPDC-007 | JPDC | Comprehensive overview of quantum serverless: Elastic integration of q | NO_PUBLIC_ARTIFACT_FOUND | — | — |

No public code repository was verified for any record in these four journals. `UNKNOWN` means the artifact
was not checkable within the evidence budget; the links recorded are preprints, not code. `NO_PUBLIC_ARTIFACT_FOUND`
is used only for the theory papers and the survey, where no software artifact is expected.

## 6. False-positive logs

### TC — 29 excluded

| Class | Count |
|---|---:|
| FP1_PQC | 12 |
| FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | 3 |
| FP4_QUANTUM_CRYPTO_NETWORKING | 3 |
| FP5_QML_APPLICATION | 2 |
| FP2_QUANTUM_INSPIRED | 2 |
| FP6_DEVICE_PHYSICS | 2 |
| OUT_OF_WINDOW | 1 |
| LEXICAL_FALSE_POSITIVE | 1 |
| OFF_TOPIC_NOT_QUANTUM | 1 |
| FP6_SUPERCONDUCTING_EDA | 1 |
| GATE_COUNT_ONLY | 1 |

Post-quantum cryptography is the dominant false-positive class (13 of 29 exclusions), followed by quantum cryptographic protocols and device/cryogenic modelling. Two exclusions are pure lexical artefacts of the sweep (TC-002 'Entangling' prefetcher, TC-001 adversarial-ML defence).

| ID | Year | DOI | Class | Reason |
|---|---|---|---|---|
| TC-001 | 2024 | `10.1109/tc.2021.3066614` | OUT_OF_WINDOW | First public availability 2021 (DOI 10.1109/tc.2021.3066614); the 2024 issue cover date was used in error, so the record falls outside the 2024-2026 window. Content is also off-topic: adversarial-example defence for DNN authentication systems, no quantum content. |
| TC-002 | 2024 | `10.1109/tc.2023.3337308` | LEXICAL_FALSE_POSITIVE | Classical instruction prefetcher; 'Entangling' is the prefetcher's name, not quantum entanglement. |
| TC-003 | 2024 | `10.1109/tc.2024.3416619` | FP5_QML_APPLICATION | Anti-noise quantum SVM algorithm; accuracy-oriented QML, no classical systems contribution (Gate 1/2 fail). |
| TC-005 | 2024 | `10.1109/tc.2024.3441831` | FP2_QUANTUM_INSPIRED | GPU tensor-core tensor-train primitives for classical big-data/DL; quantum only as an application keyword. POSSIBLE_CROSSOVER to MPS-based simulation, not claimed here. |
| TC-006 | 2024 | `10.1109/tc.2024.3449094` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Quantum circuit for AES with T-depth/qubit resource estimation for cryptanalysis; no classical systems mechanism. |
| TC-007 | 2024 | `10.1109/tc.2024.3457736` | FP1_PQC | GPU implementation of SPHINCS+ post-quantum signatures. |
| TC-008 | 2024 | `10.1109/tc.2024.3477987` | FP1_PQC | GPU-accelerated SSL/TLS cryptographic providers. |
| TC-009 | 2024 | `10.1109/tc.2024.3483631` | FP1_PQC | Kyber/Dilithium assembly optimisation on RISC-V. |
| TC-012 | 2025 | `10.1109/tc.2025.3525614` | FP1_PQC | Quantum-resistant encrypted cross-modal retrieval scheme. |
| TC-013 | 2025 | `10.1109/tc.2025.3533094` | OFF_TOPIC_NOT_QUANTUM | Functional-graph structure of baker's maps in finite-precision arithmetic; quantum mentioned only as prior context. |
| TC-014 | 2025 | `10.1109/tc.2025.3540647` | FP1_PQC | NTRU/Falcon/Hawk post-quantum processor. |
| TC-015 | 2025 | `10.1109/tc.2025.3540649` | FP1_PQC | Lattice-based searchable encryption scheme. |
| TC-018 | 2025 | `10.1109/tc.2025.3557968` | FP4_QUANTUM_CRYPTO_NETWORKING | Quantum secure vector dominance protocol; cryptographic protocol, not a computing-systems contribution. |
| TC-019 | 2025 | `10.1109/tc.2025.3558044` | FP1_PQC | RTL accelerator for HQC KEM. |
| TC-020 | 2025 | `10.1109/tc.2025.3566897` | FP4_QUANTUM_CRYPTO_NETWORKING | Quantum private comparison protocol based on quantum walks. |
| TC-021 | 2025 | `10.1109/tc.2025.3566899` | FP6_DEVICE_PHYSICS | Cryogenic cache delay/power/area modelling in 7nm FinFET at 10K; cryo-CMOS device modelling. POSSIBLE_CROSSOVER to cryogenic control electronics for QPUs, but the contribution is a classical cache model. |
| TC-022 | 2025 | `10.1109/tc.2025.3576934` | FP1_PQC | Dilithium hardware with improved MDC-NTT. |
| TC-024 | 2025 | `10.1109/tc.2025.3590972` | FP1_PQC | NO_ABSTRACT; title settles: high-radix NTT multiplier architecture for lattice cryptography. |
| TC-025 | 2025 | `10.1109/tc.2025.3625044` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Quantum walk search for subset sum with gate-count/depth/width costing; algorithm design. |
| TC-026 | 2025 | `10.1109/tc.2025.3625822` | FP6_SUPERCONDUCTING_EDA | Length-matching placement and routing for RSFQ superconducting logic; physical design of a classical superconducting technology. |
| TC-028 | 2025 | `10.1109/tc.2025.3642981` | GATE_COUNT_ONLY | Circuit optimisation framework targeting qubit count for comparator circuits; no compilation-cost, scalability or systems claim. |
| TC-032 | 2026 | `10.1109/tc.2025.3630119` | FP2_QUANTUM_INSPIRED | Ising-machine hybrid decomposition for combinatorial optimisation; dynamics-based Ising hardware, not a QPU. |
| TC-033 | 2026 | `10.1109/tc.2026.3654037` | FP5_QML_APPLICATION | Quantum federated learning heterogeneity; contribution is an FL training algorithm (personalisation/sporadic participation), not a systems mechanism. |
| TC-034 | 2026 | `10.1109/tc.2026.3654172` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | QUBO formulation/variable reduction for factoring on quantum annealers; problem encoding, no systems contribution. |
| TC-035 | 2026 | `10.1109/tc.2026.3654650` | FP1_PQC | GPU acceleration of SPHINCS+. |
| TC-036 | 2026 | `10.1109/tc.2026.3666827` | FP6_DEVICE_PHYSICS | CNN surrogate model for transistor self-heating at cryogenic temperature; device modelling. |
| TC-037 | 2026 | `10.1109/tc.2026.3671958` | FP1_PQC | Plantard-algorithm NTT architecture for ML-KEM/ML-DSA. |
| TC-038 | 2026 | `10.1109/tc.2026.3688679` | FP4_QUANTUM_CRYPTO_NETWORKING | NO_ABSTRACT; title settles: quantum multiparty key agreement protocol. |
| TC-039 | 2026 | `10.1109/tc.2026.3700228` | FP1_PQC | GPU-parallel HQC implementation. |

### TCAD — 41 excluded

| Class | Count |
|---|---:|
| FP1_PQC | 11 |
| FP6_SUPERCONDUCTING_EDA | 6 |
| FP5_QML_APPLICATION | 5 |
| FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | 4 |
| GATE_COUNT_ONLY | 4 |
| FP2_QUANTUM_INSPIRED | 4 |
| FP6_DEVICE_PHYSICS | 3 |
| FP4_QUANTUM_CRYPTO_NETWORKING | 2 |
| VQE_ANSATZ_RULE | 1 |
| OFF_TOPIC_NOT_QUANTUM | 1 |

Two large out-of-scope populations dominate: post-quantum cryptography and side-channel analysis (16), and superconducting/AQFP/RQFP/SiDB EDA plus device and readout modelling (11). A third cluster is QML feature-selection/classification (6), largely from one recurring author group.

| ID | Year | DOI | Class | Reason |
|---|---|---|---|---|
| TCAD-002 | 2024 | `10.1109/tcad.2023.3311732` | FP6_DEVICE_PHYSICS | Analytical model of RF control-circuit inaccuracies on qubit gate fidelity; control electronics modelling. |
| TCAD-003 | 2024 | `10.1109/tcad.2023.3311734` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Complexity-theoretic bounds on depth/size overhead from qubit connectivity; no classical systems mechanism. POSSIBLE_CROSSOVER to architecture connectivity studies. |
| TCAD-004 | 2024 | `10.1109/tcad.2023.3325974` | GATE_COUNT_ONLY | SAT-oracle synthesis minimising ancilla/gate counts. |
| TCAD-005 | 2024 | `10.1109/tcad.2023.3327102` | GATE_COUNT_ONLY | Decomposition of multicontrolled SU(2) gates; CNOT-count result. |
| TCAD-008 | 2024 | `10.1109/tcad.2023.3345251` | FP5_QML_APPLICATION | Quantum KNN classification with K-value/neighbour selection. |
| TCAD-009 | 2024 | `10.1109/tcad.2024.3355277` | VQE_ANSATZ_RULE | Native-pulse variational ansatz for VQAs; excluded by the VQE rule (new ansatz -> EXCLUDE). |
| TCAD-011 | 2024 | `10.1109/tcad.2024.3382827` | FP4_QUANTUM_CRYPTO_NETWORKING | Security solution for quantum network coding. |
| TCAD-013 | 2024 | `10.1109/tcad.2024.3391690` | FP4_QUANTUM_CRYPTO_NETWORKING | Secure delegated VQA via quantum homomorphic encryption; security protocol, not workload orchestration. |
| TCAD-015 | 2024 | `10.1109/tcad.2024.3394368` | FP6_SUPERCONDUCTING_EDA | Parametric EDA for coplanar-waveguide channel recognition and air-bridge placement on quantum chips; layout automation of quantum hardware. |
| TCAD-016 | 2024 | `10.1109/tcad.2024.3395977` | FP2_QUANTUM_INSPIRED | Ising-model parallel-tempering accelerator architecture. |
| TCAD-017 | 2024 | `10.1109/tcad.2024.3399669` | FP1_PQC | PUF-based Kyber architecture on ARM. |
| TCAD-018 | 2024 | `10.1109/tcad.2024.3434385` | FP6_SUPERCONDUCTING_EDA | AQFP technology mapping/legalisation (buffer and splitter insertion); superconducting classical logic EDA. |
| TCAD-019 | 2024 | `10.1109/tcad.2024.3461573` | FP6_SUPERCONDUCTING_EDA | AQFP buffer/splitter insertion; superconducting classical logic EDA. |
| TCAD-020 | 2024 | `10.1109/tcad.2024.3471905` | GATE_COUNT_ONLY | Linear decomposition of approximate multicontrolled gates; CNOT-count result. |
| TCAD-021 | 2024 | `10.1109/tcad.2024.3471949` | FP5_QML_APPLICATION | QNN robust training against spatial/temporal noise bias; model-accuracy contribution. |
| TCAD-022 | 2024 | `10.1109/tcad.2024.3483670` | FP6_DEVICE_PHYSICS | Analytical readout-fidelity model for superconducting readout chains. |
| TCAD-028 | 2024 | `10.1109/tcad.2024.3518412` | FP1_PQC | Modular adder architecture for ECC/PQC on FPGA. |
| TCAD-029 | 2025 | `10.1109/tcad.2025.3526060` | FP5_QML_APPLICATION | Quantum feature selection with sparse optimisation circuit. |
| TCAD-031 | 2025 | `10.1109/tcad.2025.3539002` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Depth/ancilla bounds for symmetric Boolean function circuits; circuit-complexity result. |
| TCAD-032 | 2025 | `10.1109/tcad.2025.3546884` | FP6_SUPERCONDUCTING_EDA | Cartesian genetic programming synthesis for reversible quantum-flux-parametron logic; superconducting logic EDA. |
| TCAD-034 | 2025 | `10.1109/tcad.2025.3550443` | FP1_PQC | Power side-channel attack on Kyber. |
| TCAD-035 | 2025 | `10.1109/tcad.2025.3567883` | FP2_QUANTUM_INSPIRED | Quantum-inspired ant colony optimisation for multiplier formal verification; classical EDA. |
| TCAD-036 | 2025 | `10.1109/tcad.2025.3570135` | OFF_TOPIC_NOT_QUANTUM | Near-sensor compute-in-memory macro for image denoising; no quantum content. |
| TCAD-039 | 2025 | `10.1109/tcad.2025.3580341` | FP6_SUPERCONDUCTING_EDA | End-to-end EDA flow for superconducting quantum chip design (layout/fabrication oriented). |
| TCAD-041 | 2025 | `10.1109/tcad.2025.3591735` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Quantum circuit for random sampling of permutations; algorithm design. |
| TCAD-042 | 2025 | `10.1109/tcad.2025.3592590` | FP1_PQC | Fault-detection architecture for Montgomery modular multiplication. |
| TCAD-044 | 2025 | `10.1109/tcad.2025.3595834` | FP1_PQC | Hardware generator for FFT/NTT architectures for FHE and PQC. |
| TCAD-046 | 2025 | `10.1109/tcad.2025.3605537` | FP6_DEVICE_PHYSICS | Automatic standard-cell design for silicon dangling-bond (beyond-CMOS) logic. |
| TCAD-047 | 2025 | `10.1109/tcad.2025.3608056` | FP1_PQC | NO_ABSTRACT; title settles: side-channel attack framework against FALCON. |
| TCAD-048 | 2025 | `10.1109/tcad.2025.3610064` | FP1_PQC | Modular addition for FPGA cryptographic operations (ECC/PQC). |
| TCAD-049 | 2025 | `10.1109/tcad.2025.3610581` | FP1_PQC | Non-profiled deep-learning side-channel attack on lattice KEMs. |
| TCAD-052 | 2025 | `10.1109/tcad.2025.3635568` | FP5_QML_APPLICATION | Nonlinear quantum feature selection with multikernel circuits. |
| TCAD-053 | 2025 | `10.1109/tcad.2025.3641533` | FP7_QUANTUM_ALGORITHM_RESOURCE_ESTIMATE | Completeness result for reversible-circuit transformation rules; synthesis theory. |
| TCAD-054 | 2025 | `10.1109/tcad.2025.3642771` | FP1_PQC | Template side-channel attack against Dilithium. |
| TCAD-055 | 2025 | `10.1109/tcad.2025.3650093` | FP5_QML_APPLICATION | Quantum multiview feature selection. |
| TCAD-056 | 2026 | `10.1109/tcad.2025.3611101` | FP2_QUANTUM_INSPIRED | E-graph extraction by simulated annealing and ant colony optimisation; classical synthesis/compiler optimisation, no quantum content. |
| TCAD-059 | 2026 | `10.1109/tcad.2026.3663259` | FP6_SUPERCONDUCTING_EDA | NO_ABSTRACT; title settles: constraint-aware automation for superconducting quantum chip layout design. |
| TCAD-060 | 2026 | `10.1109/tcad.2026.3674833` | FP2_QUANTUM_INSPIRED | NO_ABSTRACT; title settles: Ising-machine-based VLSI placement with annealing. |
| TCAD-065 | 2026 | `10.1109/tcad.2026.3702368` | FP1_PQC | NO_ABSTRACT; title settles: Trojan/fault resilience for NTT hardware. |
| TCAD-067 | 2026 | `10.1109/tcad.2026.3707423` | GATE_COUNT_ONLY | CNOT-count reduction for state preparation and block encoding; circuit-complexity result. |
| TCAD-068 | 2026 | `10.1109/tcad.2026.3710868` | FP1_PQC | NO_ABSTRACT; title settles: configurable hardware accelerator for Kyber. |

### TPDS — 8 excluded

| Class | Count |
|---|---:|
| FP3_CLASSICAL_QUANTUM_CHEMISTRY | 4 |
| FP1_PQC | 3 |
| FP2_QUANTUM_INSPIRED | 1 |

Two clean classes: PQC GPU implementations (3) and classical electronic-structure/many-body HPC (4), plus one classical annealing paper. The 'quantum' keyword in TPDS almost always means quantum chemistry or quantum-resistant cryptography, not a QPU.

| ID | Year | DOI | Class | Reason |
|---|---|---|---|---|
| TPDS-001 | 2024 | `10.1109/tpds.2024.3367319` | FP1_PQC | GPU implementations of Falcon and Mitaka lattice signatures. |
| TPDS-002 | 2024 | `10.1109/tpds.2024.3379734` | FP1_PQC | High-performance Kyber on NVIDIA GPUs. |
| TPDS-003 | 2024 | `10.1109/tpds.2024.3453289` | FP1_PQC | High-throughput GPU Dilithium implementation. |
| TPDS-004 | 2025 | `10.1109/tpds.2025.3557621` | FP3_CLASSICAL_QUANTUM_CHEMISTRY | Plane-wave DFT scaling on the Sunway supercomputer; classical electronic-structure HPC. |
| TPDS-005 | 2025 | `10.1109/tpds.2025.3568360` | FP3_CLASSICAL_QUANTUM_CHEMISTRY | Neural-network quantum states for molecular potential energy surfaces; classical many-body method. |
| TPDS-006 | 2025 | `10.1109/tpds.2025.3620251` | FP3_CLASSICAL_QUANTUM_CHEMISTRY | Large-scale NNQS on Sunway; classical many-body method. |
| TPDS-009 | 2026 | `10.1109/tpds.2026.3705623` | FP3_CLASSICAL_QUANTUM_CHEMISTRY | GPU-cluster optimisation of density functional perturbation theory; classical materials simulation. |
| TPDS-010 | 2026 | `10.1109/tpds.2026.3706438` | FP2_QUANTUM_INSPIRED | Speculative parallel simulated annealing for simulation optimisation; classical metaheuristic, no quantum hardware. |

### JPDC — 6 excluded

| Class | Count |
|---|---:|
| FP2_QUANTUM_INSPIRED | 2 |
| OFF_TOPIC_NOT_QUANTUM | 2 |
| FP5_QML_APPLICATION | 1 |
| FP1_PQC | 1 |

Quantum-inspired metaheuristics and QML/IoT applications account for 4 of 6 exclusions; 2 records contain no quantum content at all. The sweep matched on the word 'quantum' in application framing.

| ID | Year | DOI | Class | Reason |
|---|---|---|---|---|
| JPDC-001 | 2024 | `10.1016/j.jpdc.2024.104920` | FP2_QUANTUM_INSPIRED | NO_ABSTRACT; title settles: quantum-inspired genetic algorithm for cloud workflow scheduling; classical metaheuristic. |
| JPDC-002 | 2025 | `10.1016/j.jpdc.2025.105108` | OFF_TOPIC_NOT_QUANTUM | NO_ABSTRACT; title settles: Winograd convolution code template for a classical accelerator (GCU). |
| JPDC-003 | 2025 | `10.1016/j.jpdc.2025.105133` | FP5_QML_APPLICATION | NO_ABSTRACT; title settles: quantum neural network intrusion detection on IonQ hardware; application accuracy study. |
| JPDC-004 | 2026 | `10.1016/j.jpdc.2026.105267` | FP2_QUANTUM_INSPIRED | NO_ABSTRACT; title settles: quantum-inspired IoT crop-recommendation framework. |
| JPDC-005 | 2026 | `10.1016/j.jpdc.2026.105298` | OFF_TOPIC_NOT_QUANTUM | NO_ABSTRACT; title settles: IoT DDoS detection with CNN, blockchain and homomorphic encryption; no quantum content. |
| JPDC-006 | 2026 | `10.1016/j.jpdc.2026.105302` | FP1_PQC | NO_ABSTRACT; title settles: quantum-resilient cryptographic architectures for cloud-native environments. |

## 7. Branch ownership — who owns which part of the interface

The four journals partition the compilation and simulation work cleanly; the split is by *level of the stack*,
not by topic label.

| Branch | TCAD | TC | TPDS | JPDC |
|---|---|---|---|---|
| Compiler / mapping / routing / scheduling | **Owner.** 7 included records, 9 borderline and 1 unresolved carry this branch: mapping and routing (TCAD-024, TCAD-025, TCAD-057; TCAD-064 unresolved), platform-specific movement (TCAD-027 trapped-ion shuttling, TCAD-030 neutral-atom shuttling), synthesis and toolchain (TCAD-014); crosstalk-aware scheduling (TCAD-025) and compiler offload to an Ising machine (TCAD-038) sit at BORDERLINE after verification. | Peripheral. One heuristic mapper (TC-004), one local-search mapper (borderline, TC-016), and two computability-theory papers about what a compiler can compute at all (TC-010, TC-027). | None. | None. |
| Distributed / multi-QPU compilation | **Co-owner** at circuit level: TCAD-033 (QUBO partitioning, transmission cost), TCAD-050 (end-to-end DQC mapping with parallel per-chip mapping), TCAD-058 (title-only). | **Co-owner** at architecture level: TC-023 AdaptDQC models inter-chip communication architectures and quantifies DQC performance metrics. | None. | None. |
| Quantum circuit simulation | **Owner of the algorithmic/data-structure level**: decision diagrams and equivalence checking (TCAD-010), tensor-network approximation for noisy circuits (TCAD-051), simulator-kernel scheduling and gate fusion (TCAD-062). | **Owner of the accelerator level**: FPGA plus SATA-storage state-vector simulation (TC-011), FPGA emulation (TC-040, TC-041). | **Owner of the cluster level**: inter-node communication minimisation (TPDS-007) and communication-partition co-optimisation on CPU+GPU clusters (TPDS-008). | None. |
| QPU scheduling / resource management | TCAD-043 (performance-bound prediction explicitly framed as input to job scheduling in quantum-centric supercomputing). | TC-031, BORDERLINE (verifying which device a cloud job actually ran on — the accounting side of allocation, measured as identification accuracy). | None. | Covered only descriptively by the JPDC-007 survey. |
| Control plane / runtime | TCAD-023 (near-quantum FPGA cache for pulse synthesis), TCAD-057 (dynamic-circuit execution). | None. | None. | None. |
| HPC-QPU integration / orchestration middleware | Touched by TCAD-043 only. | None. | None. | **Only presence in the corpus**, and it is a survey: JPDC-007 on quantum serverless. |

Readings that follow from the table:

1. **TCAD owns quantum compilation outright.** Every mapping, routing, gate-scheduling, shuttling and
   partitioning record of substance is in TCAD; TC's compilation presence is either architecture-level (DQC)
   or theoretical (computability of compiler functions).
2. **Simulation is split three ways by level**, not contested: TCAD works on the representation (decision
   diagrams, tensor networks, fusion/scheduling inside a simulator), TC works on the hardware substrate
   (FPGA plus storage hierarchy), TPDS works on the cluster (inter-node communication volume and partitioning).
   A census that reads only one of the three will see only one third of the simulation branch.
3. **Distributed QC is the one branch TC and TCAD genuinely share**, and they approach it from opposite ends:
   TCAD-033/TCAD-050 optimise circuits and mappings for a given multi-chip target; TC-023 models the
   inter-chip communication architecture itself and quantifies metrics across architectures.
4. **The orchestration/middleware branch is almost absent** from all four journals. `hpc_qpu_integration`,
   `hybrid_workflow` and `quantum_runtime_orchestration` appear on five records in total (TCAD-023, TCAD-038,
   TCAD-040, TCAD-057, JPDC-007), three of them borderline or survey after the verification pass. This is a
   VENUE_GAP for these four
   journals: that work is evidently published
   elsewhere, and none of these four venues should be relied on as its sensor.
5. **QEC classical processing is entirely absent.** No record in any of the four journals is a QEC decoder,
   syndrome-communication or real-time-decoding paper. `qec_classical_processing` is
   UNDERREPRESENTED_IN_THIS_CORPUS to the point of being empty here, which is a finding about these venues.

## 8. Future census policy judgements

### TC — **SELECTIVE_CENSUS**

Yield: 6 included (6 original research) of 41 candidates, from 849 articles swept.

- 6 of 41 candidates pass (0.7% of the 849-article full population) after the verification pass; the yield is real but thin and concentrated in one shape.
- TC owns hardware-level execution substrates for quantum workloads: FPGA/storage-backed simulators and emulators (TC-011, TC-040, TC-041) and architecture-level distributed QC (TC-023).
- TC also carries the corpus's only quantum-cloud allocation-verification record (TC-031), demoted to BORDERLINE because its measured quantity is device-identification accuracy.
- 28 of 41 candidates are false positives (13 of them post-quantum cryptography) and 1 more is out of window; a keyword sweep on 'quantum' in TC is dominated by PQC hardware and quantum cryptographic protocols.
- Recommended filter for future sweeps: retain accelerator/emulator/simulator, distributed-QC architecture, quantum-cloud resource-management shapes; drop PQC, quantum crypto protocols, cryogenic device modelling, Ising machines and QML up front.

### TCAD — **CORE_CENSUS**

Yield: 12 included (12 original research) of 68 candidates, from 1562 articles swept.

- 12 included plus 12 borderline and 3 unresolved from 68 candidates - the largest absolute yield of the four journals, and the most concentrated single branch in the corpus (compiler_mapping_routing).
- TCAD is the venue of record for quantum compilation: mapping, routing, gate scheduling, shuttling, partitioning for distributed QC, and circuit-level simulation/equivalence checking.
- It also supplies the corpus's control-plane record (TCAD-023 SmartQCache) and its clearest quantum-centric-supercomputing scheduling input (TCAD-043). Two records demoted on verification (TCAD-025 fidelity-objective scheduling, TCAD-038 Ising-machine offload) stay in the census as BORDERLINE.
- CORE_CENSUS must be applied with a hard scope filter: 41 of 68 candidates are out of scope, dominated by PQC/side-channel work (16) and superconducting/AQFP/beyond-CMOS EDA and device modelling (11).
- 2026 Early Access records frequently arrive without abstracts; a TCAD census needs a full-text pass, not an abstract sweep (3 records are unresolved on abstract evidence alone).

### TPDS — **LOW_YIELD**

Yield: 2 included (2 original research) of 10 candidates, from 552 articles swept.

- Low-yield hypothesis CONFIRMED. Candidate pool 10 of 552 articles; 2 pass (0.36% of the full population).
- The two passes are both distributed full-state quantum circuit simulation (TPDS-007 QuanTrans; TPDS-008 communication-partition co-optimisation on CPU+GPU clusters), both census-year 2026.
- The other 8 candidates are 3 PQC GPU implementations, 4 classical electronic-structure/many-body HPC papers (DFT, NNQS, DFPT) and 1 classical simulated-annealing paper - none involve a QPU.
- No TPDS record in 2024 or 2025 passes the gates; there is no QPU scheduling, workflow or runtime work in the pool at all.
- Both 2026 passes appearing in the same year is a signal worth re-testing in the next census, but on two records it remains an OPEN_QUESTION, not a trend.

### JPDC — **BIBLIOGRAPHY_SENSOR**

Yield: 1 included (0 original research) of 7 candidates, from 388 articles swept.

- Low-yield hypothesis CONFIRMED, and more strongly than for TPDS. Candidate pool 7 of 388 articles; 0 original-research papers pass.
- The single inclusion (JPDC-007) is a survey of Quantum Serverless - valuable as a BIBLIOGRAPHY_HUB for the orchestration branch, but it contributes no original systems result.
- The other 6 candidates are quantum-inspired metaheuristics (2), QML/IoT applications (2), a PQC/cloud-security paper and one paper with no quantum content at all.
- All 7 JPDC dossier records arrived with NO_ABSTRACT; verdicts rest on titles, except JPDC-007 whose abstract was retrieved from the publisher.
- Treat JPDC as a sensor: watch it for review/position pieces on quantum-classical integration, do not budget census effort for original research there.

### Low-yield hypothesis for TPDS and JPDC

**TPDS: confirmed.** The candidate pool was 10 records out of 552 articles, and only 2 survive the gates —
both distributed state-vector simulation, both census-year 2026 (TPDS-007 QuanTrans; TPDS-008 CPU+GPU
communication-partition co-optimisation). What the other matches actually were: 3 post-quantum cryptography
GPU implementations (Falcon/Mitaka, Kyber, Dilithium), 4 classical electronic-structure and many-body HPC
papers (plane-wave DFT on Sunway, two neural-network quantum-states papers, DFPT on GPU clusters) and 1
classical speculative simulated-annealing paper. Despite TPDS being a parallel- and distributed-computing
journal, it published no QPU scheduling, workflow, runtime or QEC work in this window. The parallel-computing
subject matter does not by itself produce quantum-HPC content.

**JPDC: confirmed, more strongly.** The candidate pool was 7 records out of 388 articles; zero original
research passes. The one inclusion is a survey (JPDC-007, quantum serverless), retained as a
BIBLIOGRAPHY_HUB for the orchestration branch. The remaining matches were 2 quantum-inspired metaheuristics
(genetic workflow scheduling, crop recommendation), 2 QML/IoT application papers, 1 PQC/cloud-security paper
and 1 paper with no quantum content. All 7 JPDC records lacked abstracts in the dossier, so six verdicts rest
on titles that are unambiguous about their subject matter.

For both journals the correct posture is to keep sweeping — the sweep is cheap and the 2026 TPDS pair shows
the pool is not permanently empty — while budgeting no deep-dive effort against them by default.

---

Counts in this document are exactly the counts in the four JSON files; no journal's count has been rounded up,
and records that could not be settled on the available evidence are recorded as INSUFFICIENT_EVIDENCE rather
than assigned a verdict.

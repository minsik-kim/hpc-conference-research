# Quantum-HPC Journal Census — Shared Inclusion Criteria (2024–2026)

You are performing a **venue census of the HPC × Quantum-Computing interface**, NOT a quantum
computing literature review. Scope discipline is the single most important requirement.

## Core inclusion condition

    Quantum problem  +  SUBSTANTIAL classical computing / systems / HPC implication

"Uses a classical computer" is NOT a classical systems contribution.
Being about a quantum computer is NOT sufficient.

## Three-Gate Test — all three must pass

**Gate 1 — is there a real classical systems problem?**
At least one of these must be present *substantively* (not in passing):
computation cost · parallelism · memory · communication · latency · throughput ·
scheduling · resource allocation · runtime · orchestration · distributed execution ·
scaling · compilation cost · data movement · accelerator design · performance modeling.

**Gate 2 — is an HPC/systems/architecture technique a major part of the contribution?**

INCLUDE shapes: distributed quantum circuit simulation; GPU/multi-GPU simulation;
state-vector / tensor-network / decision-diagram scaling; QPU scheduling; CPU/GPU/QPU
runtime; HPC-QPU workflow; QPU virtualization; multi-QPU execution; QEC decoder
acceleration; real-time QEC classical processing; syndrome bandwidth/compression;
distributed compilation; scalable mapping/routing; compiler classical cost;
circuit-cutting reconstruction cost; shot/measurement orchestration; quantum
performance modeling; modular/distributed QC architecture; quantum accelerator
integration into HPC.

USUALLY EXCLUDE: new ansatz only · VQE optimizer comparison · warm-start/initialization
alone · barren plateau studies · quantum algorithm complexity alone · pure gate-count
improvement with no systems implication · quantum chemistry result only · materials/device
physics · qubit fabrication · pure QEC code theory · new threshold proofs · quantum
networking protocols without systems/computing relevance · quantum advantage proofs ·
application accuracy comparison only.

**Gate 3 — does it help understand future CPU/GPU/HPC ↔ QPU heterogeneous computing?**
It must materially inform one of: resource usage · execution · scheduling · communication ·
runtime · scalability · control · performance · software stack.

If a paper does not clearly pass all three gates, do NOT force it in to grow the corpus.

## BORDERLINE rules (record, do not discard)

QEC: new QEC code → EXCLUDE · new decoder algorithm only → BORDERLINE · parallel decoder →
INCLUDE · GPU/FPGA/ASIC decoder → INCLUDE · decoder scheduling → INCLUDE · syndrome
communication/compression → INCLUDE.

VQE: new ansatz → EXCLUDE · optimizer comparison → EXCLUDE · initialization/warm-start →
EXCLUDE (in this corpus) · distributed shot execution → INCLUDE-able · QPU allocation for
VQE → INCLUDE · hybrid workflow scheduling → INCLUDE.

Quantum compilation: output fidelity / gate count only → BORDERLINE or EXCLUDE ·
classical compilation scalability → INCLUDE · parallel compiler → INCLUDE · distributed
compiler → INCLUDE · architecture-aware mapping with substantial systems implications →
INCLUDE.

## Known dominant false-positive classes (exclude, but LOG them)

1. **Post-quantum cryptography** (Kyber, Dilithium, NTT, SPHINCS+, HQC, lattice, ML-KEM,
   ML-DSA, side-channel attacks on PQC) — the single largest false positive here.
2. **Quantum-inspired classical methods** — Ising machines, simulated/adiabatic annealing
   hardware, QUBO solvers run classically, quantum-inspired PSO/genetic algorithms,
   tensor-train "quantum-inspired" numerics.
3. **Classical quantum chemistry / many-body / transport** — DFT, neural-network quantum
   states, quantum perturbation theory, QMCPACK, CP2K, plane-wave codes.
4. **Quantum networking / QKD / quantum internet** — entanglement routing, repeaters,
   key distribution, quantum secret sharing (exclude unless the contribution is a
   *computing systems* one, e.g. distributed-QC interconnect for computation).
5. **Quantum machine learning applications** — QNN classifiers, quantum federated learning,
   quantum GANs applied to a domain task.
6. **Quantum sensing / metrology / device physics** — NV centers, Rydberg sensors,
   cryo-CMOS readout electronics, fabrication, superconducting materials.
7. **Quantum algorithms / complexity theory** — Grover variants, quantum walks, complexity
   classes, oracle constructions, resource estimates with no systems mechanism.

## Article-type classification (every record)

ORIGINAL_RESEARCH · REVIEW_SURVEY · PERSPECTIVE · EDITORIAL · SPECIAL_ISSUE_INTRO · OTHER
(front matter, index, corrigendum/erratum → OTHER)

Only ORIGINAL_RESEARCH counts toward the included-population count.
A highly relevant REVIEW_SURVEY / PERSPECTIVE may additionally be tagged BIBLIOGRAPHY_HUB.

## Scenario classification (multiple allowed)

- **HPC_FOR_Q** — classical HPC serving quantum computing (simulation, compilation,
  decoding, control).
- **Q_IN_HPC** — a QPU integrated into an HPC centre/system (workflow, scheduling,
  middleware, resource management).
- **Q_FOR_HPC** — quantum used to accelerate a classical HPC workload.
- **FUTURE_WORKLOAD** — analysis/projection of future heterogeneous CPU/GPU/QPU systems.

## Branch (bottom-up; use these as a starting vocabulary, add if the corpus demands)

distributed_gpu_simulation · hpc_qpu_integration · hybrid_workflow ·
qpu_scheduling_resource_mgmt · quantum_runtime_orchestration · multi_qpu_distributed_qc ·
qec_classical_processing · compiler_mapping_routing · circuit_cutting_reconstruction ·
benchmarking_performance_modeling · architecture_control · scientific_workflow_application

## Artifact status (every INCLUDED original research paper)

PUBLIC_CODE · PUBLIC_ARTIFACT · PARTIAL · NO_PUBLIC_ARTIFACT_FOUND · UNKNOWN
(record artifact_url when found; UNKNOWN if you could not check)

## Conference-extension lineage

CONFIRMED_EXTENSION (explicit evidence: "extended version of", same title at a conference,
stated in the paper) · RELATED_LINEAGE (same group/system name, clearly related prior
conference paper) · UNKNOWN (default — do NOT guess).

## FORBIDDEN vocabulary

Never write: novel · unexplored · first · "no one has studied" · research gap.
Allowed instead: VENUE_GAP · JOURNAL_GAP · UNDERREPRESENTED_IN_THIS_CORPUS ·
POSSIBLE_CROSSOVER · OPEN_QUESTION · INSUFFICIENT_EVIDENCE.

## Evidence discipline

- Do not invent facts. If the abstract is insufficient, say INSUFFICIENT_EVIDENCE.
- Do not copy a headline number without its baseline/context. If a speedup figure is
  stated, record what it is measured against; if unclear, write `BASELINE_UNCLEAR`.
- Mark `NO_ABSTRACT` records explicitly rather than guessing from the title.

## Seed anchoring warning

A separate pre-scan suggested certain paper titles exist. Those are EXISTENCE_CHECK_SEED
only. Do not treat them as a whitelist, and exclude them if they fail the gates.

# ISC High Performance 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.

## 1. Population and denominators

| Year | Regular research papers | Method | Count status | 2nd source on the count | Relevant | Share |
|---|---:|---|---|---|---:|---:|
| ISC 2024 (39th) | **24** | `PUBLISHER_TOC_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | No | **6** | 25.0% |
| ISC 2025 (40th) | **28** | `PUBLISHER_TOC_ENUMERATED` | `TOTAL_COUNT_UNVERIFIED` | No | **3** | 10.7% |
| ISC 2026 (41st) | **35** | `PUBLISHER_TOC_ENUMERATED` | `TOTAL_COUNT_UNVERIFIED` | No | **4** (+1 borderline) | 11.4% |

Volumes: IEEE, container title *"ISC High Performance \<year\> Research Paper Proceedings"*, DOI
prefix `10.23919/isc.<year>` `[proceedings]`. Front matter excluded from all three counts. ISC
**workshops** are a separate Springer LNCS volume and are excluded `[inference]`.

**2024 is provably complete**: the DOI article-ID block `10528921–10528945` is perfectly
contiguous, 25 of 25 IDs present. **2026**: IDs `11520450`, `11520473–11520493`, `11520495–11520507`,
`11526944`; the single interior gap `11520494` was directly probed and returns 404, so the blocks
are genuinely contiguous. **2025** recovered 29 records identically in two differently-shaped
queries but its ID blocks are scattered, so completeness cannot be *proved* without the publisher
TOC. IEEE Xplore returned HTTP 418 throughout; the ISC agenda is login-gated, so **session names
are UNKNOWN for every paper** and track assignment is `[inference]` from the CFP.

**Category discipline:** the ISC research-paper CFP defines a **single** paper category (10 pages +
references) `[official-CFP]`. There is no short-paper or WIP category in this track, so no item is
`STATUS_UNCLEAR` and four 8–9-page papers in 2024 are full regular papers, merely shorter.

**Venue scope** `[official-CFP]`: ISC runs a dedicated top-level **Quantum Computing** submission
track — one of six — with its own area chair (2024: Stefan Knecht, AlgorithmiQ). Formally the
strongest quantum scope of any HPC venue in the survey.

## 2. Relevant papers

### ISC 2024 — 6 of 24

**2024-1 · Calibration and Performance Evaluation of a Superconducting Quantum Processor in an HPC Center**
Xiaolong Deng (LRZ) et al., with IQM and TU München · `10.23919/ISC.2024.10528924`, pp. 1–9
· `Q_IN_HPC`, `HPC_FOR_Q` · **REAL_QPU** · Artifact `UNKNOWN` · NISQ · `[proceedings][abstract]`
Standardized automatic calibration procedure for an in-house superconducting QPU, evaluated with
quantum-volume benchmarks plus application-level algorithms and error mitigation.
*Quantum problem:* gate/qubit fidelity drift and the absence of a unified calibration+benchmark
metric set. *HPC problem:* an HPC centre must operate the device as an unattended production
resource — an automated operational pipeline like any other node. *Why ISC:* it is a
facility-operations paper; the contribution is the operating procedure, not the device physics.

**2024-2 · Multithreaded Parallelism for Heterogeneous Clusters of QPUs** (MILQ)
Philipp Seitz, Manuel Geiger, Christian B. Mendl (TU München) · `10.23919/ISC.2024.10528940`,
pp. 1–8 · `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** ·
Artifact **`PUBLIC_CODE`** `https://github.com/qc-tum/milq` · NISQ · `[proceedings][abstract][code]`
Treats heterogeneous QPU backends as *unrelated parallel machines* with differing setup and
processing times, uses circuit cutting to fit circuits onto devices, and schedules a batch with a
MILP; up to 26% makespan improvement.
*Quantum problem:* circuits too wide for individual devices; cutting multiplies execution count.
*HPC problem:* classical makespan minimization over a heterogeneous accelerator pool.
**Code cross-validation** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §8): MILP verified line by
line — PuLP, `LpMinimize` on `c_max` (makespan only), `p_times[job][machine]` confirming unrelated
parallel machines, `s_times[from][to][machine]` sequence-dependent setup, and a per-timestep
**qubit-capacity constraint permitting co-residency** of several circuits on one QPU. Backends are
three 5-qubit Qiskit fake devices under `AerSimulator`. **The 26% baseline is a bin-packing
scheduler**, computed as `(baseline − algorithm)/baseline`. Verdict `CONSISTENT` on the model,
`PARTIAL_MATCH` on the headline (the shipped default run is 5 circuits, 2–3 machines, 1 batch).

**2024-3 · A Tree-Approach Pauli Decomposition Algorithm with Application to Quantum Computing**
Océane Koska (Paris-Saclay / Eviden), Marc Baboulin, Arnaud Gazda · `10.23919/ISC.2024.10528938`,
pp. 1–11 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **classical-only** (sequential + parallel) ·
Artifact `NO_PUBLIC_ARTIFACT_FOUND` · GENERAL · `[proceedings][abstract]`
*Quantum problem:* Pauli-basis decomposition is a mandatory, exponentially expensive pre-step for
Hamiltonian encoding. *HPC problem:* a classical dense-linear-algebra kernel — redundancy
elimination, memory-bounded traversal, shared-memory parallel scaling.

**2024-4 · Evaluation of the Classical Hardware Requirements for Large-Scale Quantum Computations**
Daan Camps, Ermal Rrapaj, Katherine Klymko, Brian Austin, Nicholas J. Wright (NERSC/LBNL) ·
`10.23919/ISC.2024.10528937`, pp. 1–12 · `HPC_FOR_Q`, `FUTURE_WORKLOAD`, `Q_IN_HPC` ·
**ANALYTIC_MODEL** · Artifact `UNKNOWN` · FTQC · `[proceedings][abstract]`
**The most load-bearing single paper at this venue for this project.** Quantifies the *classical*
infrastructure a large-scale surface-code machine needs and identifies syndrome decoding as the
dominant classical workload: logical clock 100–10,000 Hz with modern decoders; a representative
chemistry application running for months; **syndrome data rate 2–500 Gbps depending on
compression**; **real-time decoding needing ~1 petaflop**. Concludes today's classical HPC
infrastructure can meet the bandwidth/latency/compute demands.
*Why ISC:* it expresses quantum error correction in the units an HPC centre procures in — petaflops,
Gbps, latency, watts.

**2024-5 · Hierarchical Multigrid Ansatz for Variational Quantum Algorithms**
Christo Meriwether Keller (NMSU/LANL) et al. · `10.23919/ISC.2024.10528934`, pp. 1–11 ·
`Q_FOR_HPC`, `HPC_FOR_Q` · **SOFTWARE_SIMULATION** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · NISQ
A VQE ansatz built from the classical **multigrid** hierarchy — optimize at successively smaller
qubit counts, reuse parameters as the next initial guess. *Why ISC:* the contribution is framed in
classical numerical-methods vocabulary and targets eigensolver/combinatorial workloads.

**2024-6 · What is Quantum Parallelism, Anyhow?**
Stefano Markidis (KTH), sole author · `10.23919/ISC.2024.10528926`, pp. 1–12 · `FUTURE_WORKLOAD`,
`HPC_FOR_Q` · **ANALYTIC_MODEL** · Artifact `UNKNOWN` · GENERAL
Dataflow diagrams to quantify parallelism in quantum algorithms, then tests whether **Amdahl's and
Gustafson's laws** transfer; concludes they are informative but bounded by interference and by the
classical↔quantum I/O constraint. **Not in the seed list.** Included because it analyses classical
parallel scaling laws and the classical I/O boundary — a systems implication, not pure theory.

### ISC 2025 — 3 of 28

**2025-1 · Towards a Unified Architectural Representation in HPCQC: Extending Sys-Sage for Quantum Technologies**
Durganshu Mishra, Stepan Vanecek (TUM), Jorge Echavarria, Xiaolong Deng, Burak Mete, Laura Schulz
(LRZ), Martin Schulz (TUM) · `10.23919/ISC.2025.11017506`, pp. 1–12 · `Q_IN_HPC`, `HPC_FOR_Q` ·
**classical software contribution exercised against real QPU topology data** ·
Artifact **`PUBLIC_CODE`** (base tool) `https://github.com/stepanvanecek/sys-sage` — that the
quantum extension is merged there is `[inference]` · GENERAL
*Quantum problem:* QPU characteristics are vendor-specific and time-varying (calibration drift),
with no portable way for a mapper or scheduler to read them. *HPC problem:* the classical
`hwloc`-style system-topology discovery and representation problem, extended to a new device class
without forking the data model. *Why ISC:* a systems-software/infrastructure-library paper whose
named beneficiaries are schedulers and mappers.

**2025-2 · Telemetry for Quantum Systems in HPC Centers**
Hossam Ahmed et al. (LRZ QCT, 10 authors) · `10.23919/ISC.2025.11018264`, pp. 1–11 · `Q_IN_HPC` ·
**real deployment** · Artifact `UNKNOWN` · NISQ
*Quantum problem:* moving a device from a shielded lab into a production machine room raises
external noise and degrades stability. *HPC problem:* data-centre telemetry and monitoring
infrastructure — sensor coverage, collection architecture, extensibility, integration with the
centre's existing operational monitoring. *Why ISC:* HPC-centre operations is a long-standing ISC
topic; this applies it to a new device class.

**2025-3 · Quantum-Accelerated Supercomputing Atomistic Simulations for Corrosion Inhibition**
Karim Elgammal (RISE Sweden), Marc Maußner (Infoteam) · `10.23919/ISC.2025.11018263`, pp. 1–10 ·
`Q_FOR_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION + classical HPC DFT**
(no real-QPU claim in the abstract) · Artifact `UNKNOWN` · NISQ · **Not in the seed list**
Hybrid workflow: ML potentials for geometry pre-screening, CP2K DFT at scale, active-space
embedding into a "StatefulAdaptVQE"; binding energies −0.386 eV and −1.279 eV for two triazoles on
aluminium; claimed 5–6× workflow speedup at equal accuracy.

### ISC 2026 — 4 of 35, plus 1 borderline

**2026-1 · Compile-Time Simplification of Classically Controlled Operations in Dynamic Circuits**
Innocenzo Fulginiti, Yanbin Chen, Christian B. Mendl, Helmut Seidl (TUM) ·
`10.23919/ISC.2026.11520473`, pp. 1–12 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **classical-only** ·
Artifact `UNKNOWN` · EARLY_FTQC · **Not in the seed list**
Static analysis plus symbolic execution propagating classical information alongside quantum state,
deriving an IR in which classically-controlled operations become unitary or vanish; ~50% reduction
in classical controls on random dynamic circuits.
*HPC problem:* a compiler/program-analysis problem solved once at compile time on the classical
host instead of per shot at runtime — and a latency problem on the classical control path.
Dynamic circuits with feedforward are the enabling primitive for real-time QEC, which is why this
sits in the same causal chain as the decoder papers at the architecture venues.

**2026-2 · An HPCQC-tailored Approach for Scalable Measurement of Physical Observables**
Salvatore Zammuto, Martin Schulz (TUM) · `10.23919/ISC.2026.11520505`, pp. 1–12 · `Q_IN_HPC`,
`HPC_FOR_Q`, `FUTURE_WORKLOAD` · **evaluation modality UNCLEAR from the abstract — not recorded** ·
Artifact `UNKNOWN` · NISQ→GENERAL
A **hierarchical runtime** making observable measurement a first-class service: workload
management, resource-aware scheduling and device-specific interaction for classical workers,
enabling commutativity-based operator grouping, adaptive shot allocation, variance-aware load
balancing, and stateful circuit caching to avoid recompilation.
*HPC problem:* hierarchical task orchestration, work distribution over classical workers, load
balancing under non-uniform per-task cost, and a compilation cache — i.e. a task runtime.

**2026-3 · A Coevolutionary Framework for Noise-Resistant Quantum Architecture Search**
Jesus Urbaneja et al. (Tohoku University) · `10.23919/ISC.2026.11520504`, pp. 1–11 · `HPC_FOR_Q`,
`FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION with backend-derived noise models** · Artifact `UNKNOWN`
· NISQ (stated) · **Not in the seed list**
Adversarial QAS: a PPO "Architect" trained against an adaptive hardware-aware "Saboteur" that
amplifies backend-derived noise within a budget, under an annealed curriculum.
*HPC problem:* a classical compute-heavy RL search pipeline with repeated noisy circuit evaluation
as the inner loop.

**2026-4 · MonteQ: A Monte Carlo Tree Search Based Quantum Circuit Synthesis Framework**
Mulundano Machiya (UChicago), Matt Menickelly, Paul Hovland, Ji Liu (Argonne) ·
`10.23919/ISC.2026.11520477`, pp. 1–12 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
**ANALYTIC_MODEL / SOFTWARE_SIMULATION** · Artifact **`PUBLIC_CODE`**
`https://github.com/Mulundano/MonteQ` · GENERAL
Two-level synthesis for Hamiltonian simulation: low-level heuristics under an MCTS over orderings
of Pauli rotations, supporting logical and hardware-aware modes.
**Code cross-validation** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §15): verdict `CONSISTENT`.
Search time is a first-class object — `MCTS(..., stop_time, ...)` runs against a **wall-clock budget
in seconds**, and candidates are ranked `(cx_count, depth, size, action_time, circuit)`, i.e. CNOT
count primary, depth as tiebreaker, matching the paper. Reported single-iteration times span
**0.321–64.7 s**, roughly linear in iteration count.
**Number discrepancy, unresolved:** the abstract reports up to 53% (mean 30%) CNOT reduction vs
Rustiq; the paper body reports **51.6% max / 23.5% mean at one iteration** and **60.2% max / 27.2%
mean at 200 iterations**. Both readings are recorded; `INSUFFICIENT_EVIDENCE` on which the abstract
intends. Also: the arXiv id is **2604.19029** (an earlier note citing 2605.11375 was wrong — that id
is TuniQ's).

**2026-B (BORDERLINE, not counted) · An Empirical Evaluation of Quantum-Inspired QUBO Methods for Heterogeneous HPC Workflow Mapping and Scheduling**
Aasish Kumar Sharma (Göttingen), Christian Boehme (GWDG), Julian Kunkel ·
`10.23919/ISC.2026.11520475`, pp. 1–11 · **classical-only**
Benchmarks QUBO schedulers (simulated annealing, multi-attempt SA, layered QAOA-*inspired*
schedules) against MILP, CP-SAT, GA and HEFT. *Against inclusion:* every method executed is
classical — false-positive class 3 — and the headline finding is **negative** for the
quantum-inspired approach (QUBO-SA loses feasibility beyond 15 tasks while classical heuristics
stay robust). *For inclusion:* QUBO formulation of HPC workflow mapping is the canonical on-ramp
for QPU offload, and the penalty-sensitivity and feasibility-ceiling results would transfer.
**Disposition: `BORDERLINE`, excluded from the count, recorded in full.**

## 3. False positives confirmed

| Paper | Year | Why excluded |
|---|---|---|
| Solving Millions of Eigenvectors in Large-Scale Quantum-Many-Body-Theory Computations (`10528945`) | 2024 | Entirely classical: GPU dense eigensolver (cuSOLVERMp), VASP BSE, 7.8 PFLOPS on 4,096 GPUs. **Confirms the prior flag on this paper.** |
| Optimizing Nuclear Configuration Interaction Calculations on GPUs (`11018300`) | 2025 | Classical GPU programming-model comparison for nuclear CI. |
| Performance Evaluation of Vector Annealing on Multiple Nodes (`11018265`) | 2025 | NEC Vector Annealing is a **classical** Ising machine on vector processors. **Confirms the prior flag.** |
| Energy Efficiency in Analog Photonic Processors (`11520497`) | 2026 | Classical analog photonic MAC accelerators for AI. |
| Workload Scheduling on Heterogeneous Devices (`10528933`) | 2024 | Checked because the shape matches a QPU-scheduling paper; platform is CPU+GPU+FPGA, no QPU. |

**Zero post-quantum-cryptography papers appeared in any of the three ISC research-paper volumes** —
worth recording as a venue characteristic, since PQC is the dominant false positive at the
architecture venues.

## 4. What ISC rewards as a contribution

ISC is the only venue in this census whose quantum papers are substantially about **operating a
QPU inside a facility**. Three of the thirteen relevant papers (calibration in an HPC centre,
telemetry, sys-sage topology representation) have no analogue anywhere else in the corpus,
including SC. The second cluster is **classical resource estimation and classical pre/post-
processing** (Camps et al.; tree Pauli decomposition; MonteQ; the dynamic-circuit compiler), and
the third is **scheduling and runtime** (MILQ, the HPCQC observable-measurement runtime).

Notably, ISC accepts papers whose entire contribution is an **operational procedure or a software
library** — not a speedup. That is a materially different acceptance criterion from ISCA/MICRO/HPCA,
and it is the reason the HPC-centre-integration branch exists at ISC and essentially nowhere else.

**Trend across the three years:** the relevant share falls (25.0% → 10.7% → 11.4%) while the
population grows (24 → 28 → 35). The 2024 peak is partly an artifact of a small denominator. The
qualitative shift is from *operations and resource estimation* (2024–2025) toward *compilers,
runtimes and search* (2026) — `OBSERVED_SHIFT`, small sample, not a trend claim.

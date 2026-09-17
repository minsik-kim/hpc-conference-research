# ISCA 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.

## 1. Population and denominators

| Year | Archival main-conference papers | Regular research track | Industry (archival) | Method | Count status | Relevant | Share of research track |
|---|---:|---:|---:|---|---|---:|---:|
| ISCA 2024 (51st, Buenos Aires) | **87** | **83** | 4 | `VOLUME_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | **6** | 7.2% |
| ISCA 2025 (52nd, Tokyo) | **135** | **131** | 4 | `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` (±1 on the research subtotal) | **16** | 12.2% |
| ISCA 2026 (53rd, Raleigh) | **172** | **161** | 11 | `VOLUME_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | **11** | 6.8% |

**2024** — IEEE block `10.1109/ISCA59077.2024.000NN`. Article IDs `00011–00097` = exactly 87 paper
slots, matching the 87 program items **one-for-one in program order**, verified at positions 1, 8,
17–21, 56 and 87; `.00098` is the Author Index and `.00099`/`.00100` 404. Corroborated by the
SIGARCH trip report: 423 submissions, **83 accepted**, 19.6%, **4 industry** → 87. `[proceedings]`

**2026** — IEEE block `10.1109/ISCA66397.2026.000NN`. Paper block `00017–00188` = exactly 172 slots,
matching the program one-for-one at 13 anchor points across the whole volume with a constant +16
offset. Corroborated by the SIGARCH trip report: 850 submissions, **161 accepted** (18.9%), **11
industry** of 27 → 172. `[proceedings]`

**2025** — ACM volume `10.1145/3695053.37XXXXX`. **The contiguity method fails here**: ACM suffixes
are not assigned in program, page or alphabetical order (CoopRT is program position 12 / page 166
but sits at the second-highest suffix). Block bounds probed to `[3730977, 3731119]` ≈ 143 slots for
135 papers plus front matter — which cannot discriminate 135 from 136. The official program,
enumerated twice session by session, gives **131 regular + 4 industry = 135**; a third-party
aggregator reports 132 on the research track. **Unresolved ±1**, recorded rather than papered over.
It does not touch the quantum numerator, which is fully accounted for in three named sessions.

**Industry track** is archival at all three venues — the 2024 industry paper `.00066` sits inside
the same contiguous IEEE paper block with its own pages (848–862), and the same holds structurally
for 2025 and 2026. **No industry-track paper in any year is quantum-related.**

**Venue scope** `[official-CFP]`: quantum was promoted from a sub-clause in 2024 to a standalone
bullet, *"Quantum computer architecture"*, in 2025 and 2026. ISCA 2026 also ran a keynote titled
*"Architecting Hybrid Quantum-Classical Computing for Scale and Fault Tolerance."*

## 2. Relevant papers

### ISCA 2024 — 6 of 83 · Session 3B "Quantum Computing" (5) + Best Paper Session (1)

| # | Paper | DOI `10.1109/ISCA59077.2024.` | pp. | Tags | Modality | Artifact | Regime |
|---|---|---|---|---|---|---|---|
| 1 | **Bosehedral** — compiler optimization for bosonic (Gaussian-boson-sampling) hardware; compact unitary representation, qumode decomposition, logical→physical mapping, tunable probabilistic gate dropout | `00028` | 261–276 | `HPC_FOR_Q` | SOFTWARE_SIMULATION `[inference]` | `UNKNOWN` | NISQ |
| 2 | **Tetris** — Pauli-string IR + synthesis for VQA; −41.3% 2-qubit gates, −37.9% depth, −42.6% duration on molecular benchmarks | `00029` | 277–292 | `HPC_FOR_Q`, `FUTURE_WORKLOAD` | SOFTWARE_SIMULATION `[inference]` | `UNKNOWN` | NISQ |
| 3 | **Atomique** — compiler for reconfigurable neutral-atom arrays; placement and movement scheduling under a new cost model | `00030` | 293–309 | `HPC_FOR_Q` | SOFTWARE_SIMULATION `[inference]` | `UNKNOWN` | NISQ |
| 4 | **Suppressing Correlated Noise via Context-Aware Compiling** (IBM Quantum) — compiler made context-aware to break the independent-error assumption error mitigation relies on | `00031` | 310–324 | `HPC_FOR_Q` | likely REAL_HARDWARE `[inference from all-IBM authorship — NOT verified]` | `UNKNOWN` | NISQ |
| 5 | **A SAT Scalpel for Lattice Surgery** (LaSsynth, UCLA/Google) — SAT encoding of lattice-surgery subroutine synthesis; 8% and 18% spacetime-volume reduction over two hand-designed state-of-the-art subroutines, incl. a T-factory | `00032` | 325–339 | `HPC_FOR_Q`, `FUTURE_WORKLOAD` | SOFTWARE_SIMULATION + SAT solving | `UNKNOWN` | FTQC |
| 6 | **QuTracer** (NC State/Argonne) — Quantum Subset Pauli Checks extending Jigsaw-style subsetting from measurement to gate+measurement errors via circuit cutting and Pauli check sandwiching. **Found outside the quantum session**, in the Best Paper Session | `00018` | 103–117 | `HPC_FOR_Q`, `FUTURE_WORKLOAD` | SOFTWARE_SIMULATION **and REAL_HARDWARE** ("noisy simulations and real device experiments") | `UNKNOWN` | NISQ |

2024 is **entirely compilation and error mitigation**; QuTracer is the only paper using a real QPU,
and the only one found outside the dedicated session.

### ISCA 2025 — 16 of 131 · Sessions 3A "Quantum I", 7C "Quantum II", 8B "Quantum III"

All DOIs `10.1145/3695053.<suffix>`.

**Session 3A — Quantum I**

7. **Hardware-aware Calibration Protocol for Quantum Computers** — `3731036` · `HPC_FOR_Q`,
`Q_IN_HPC` · NISQ. *Quantum:* device parameters drift, so calibration runs continuously and
consumes device time. *HPC:* calibration is a classical experiment-scheduling and
parameter-optimization workload scaling with qubit count — resource management on a shared
accelerator.
8. **Constant-Rate Entanglement Distillation for Fast Quantum Interconnects** (Caltech/MIT/Harvard/
QuEra) — `3731069` · `Q_IN_HPC`, `FUTURE_WORKLOAD` · ANALYTIC_MODEL `[inference]` · EARLY_FTQC/FTQC.
*HPC:* interconnect bandwidth/latency engineering for a multi-node machine — link rate vs fidelity
vs buffering, the quantum analogue of network-fabric design.
9. **S-SYNC: Shuttle and Swap Co-Optimization in Quantum Charge-Coupled Devices** — `3731084`,
arXiv 2505.01316 · `HPC_FOR_Q` · NISQ. *HPC:* joint scheduling/data-movement optimization —
substitutable costs, analogous to migration-vs-remote-access in a NUMA system.
10. **ARTERY: Fast Quantum Feedback using Branch Prediction** (ZJU/PKU) — `3731086` · `HPC_FOR_Q`,
`Q_IN_HPC` · NISQ/EARLY_FTQC. **Imports branch prediction into the real-time control processor** to
speculate on mid-circuit measurement outcomes and hide classical feedback latency inside coherence.
11. **Qtenon: Low-Latency Architecture Integration for Hybrid Quantum-Classical Computing**
(ZJU/ByteDance Seed/SYSU/SJTU) — `3731087`, pp. 299–312 · `Q_IN_HPC`, `HPC_FOR_Q` · NISQ.
**The clearest CPU/QPU heterogeneous-node paper in the three years.** *HPC:* host↔accelerator
integration — where the QPU sits in the memory/IO hierarchy, driver/runtime overhead, offload
granularity; the GPU-offload latency question transplanted to a QPU. Abstract not obtainable
(ACM 403), so the classification rests on title and session.

**Session 7C — Quantum II**

12. **Synchronization for Fault-Tolerant Quantum Computers** (Maurya & Tannu, Wisconsin) —
`3730991`, arXiv 2506.10258 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · SOFTWARE_SIMULATION, circuit-level
noise · FTQC. *Quantum:* logical qubits drift out of phase in their syndrome-generation cycles;
a logical two-qubit operation needs synchronized cycles and stalling the leader accumulates errors.
*HPC:* **a barrier-synchronization / straggler problem** — Passive, Active and Hybrid policies
designed exactly as barrier back-off in a parallel runtime. Active cuts logical error rate up to
2.4×, Hybrid up to 3.4×, and the LER reduction buys **up to 2.2× decoding-latency slack**.
13. **SWIPER: Minimizing FT Quantum Program Latency via Speculative Window Decoding**
(UChicago/Michigan) — `3731022` · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · FTQC ·
Artifact **`PUBLIC_ARTIFACT`** Zenodo `10.5281/zenodo.15102954` + `https://github.com/jviszlai/swiper` (MIT).
Applies **speculation and rollback** so the decoder's latency budget is decoupled from the qubit
reaction deadline; ~40% average application-runtime reduction vs prior parallel window decoders.
Full code cross-validation in `DEEPDIVE_QEC_DECODING.md` §1 — **verdict `CONSISTENT`, with a scope
correction**: d = 13–31 is the *PyMatching latency characterization* range only; the system sweep is
d ∈ {15, 21, 27} and the reaction-time sweep is d = 21 alone.
14. **CaliQEC: In-situ Qubit Calibration for Surface Code QEC** (UCSD/RPI/LANL/PNNL/ORNL/AWS) —
`3731042` · `HPC_FOR_Q`, `Q_IN_HPC` · EARLY_FTQC/FTQC. *HPC:* online maintenance of a running
accelerator without draining it — the quantum analogue of live migration / rolling repair.
15. **Variational Quantum Algorithms in the era of Early Fault Tolerance** (UChicago) — `3731112`,
arXiv 2503.20963 · `FUTURE_WORKLOAD`, `Q_FOR_HPC`, `HPC_FOR_Q` · EARLY_FTQC. Re-costs an entire
workload class: under early fault tolerance the cost model inverts and shot budgets, optimizer
iterations and the classical/quantum work split must be re-derived.
16. **Resource Analysis of Low-Overhead Transversal Architectures for Reconfigurable Atom Arrays**
(QuEra/Harvard/Yale) — `3731039`, arXiv 2505.15907 · `FUTURE_WORKLOAD`, `HPC_FOR_Q`, `Q_FOR_HPC` ·
**ANALYTIC_MODEL + PROJECTED** · FTQC. Headline, with context: **2048-bit RSA factoring with 19
million qubits in 5.6 days at a 1 ms QEC cycle time** — ~50× runtime speed-up over comparable prior
estimates at no space increase. Budgeted resources include **the volume for correlated decoding**,
i.e. the classical decoding workload.
17. **SwitchQNet: Optimizing Distributed Quantum Computing for Quantum Data Centers with Switch
Networks** (UCSD/Cisco) — `3731046` · `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
Artifact **`PUBLIC_ARTIFACT`** `https://zenodo.org/records/15377656` (CC-BY-4.0) · EARLY_FTQC/GENERAL.
*HPC:* datacenter network topology plus routing/scheduling — switch networks vs direct links,
contention, and a compiler that maps circuits onto the fabric.

**Session 8B — Quantum III**

18. **Accelerating Simulation of Quantum Circuits under Noise via Computational Reuse** (UBC/
Wisconsin) — `3730992` · `HPC_FOR_Q` · NISQ. **The most literally "HPC" paper of the 2025 set**:
noisy simulation needs many stochastic trajectories, which share large amounts of redundant
computation; the contribution is memoization/reuse across trajectories.
19. **QPlacer: Frequency-Aware Component Placement for Superconducting Quantum Computers**
(Duke/UCLA/MIT/ASU) — `3730994`, arXiv 2401.17450 · `HPC_FOR_Q` · NISQ/GENERAL ·
**BORDERLINE, included**: this is quantum-hardware EDA (analytical VLSI-style placement under
frequency-crowding constraints) rather than HPC×quantum in the strict sense. Included because the
contribution is a classical optimization/CAD system serving quantum computation; it is not
fabrication or materials work. Flagged so a future pass can revisit the call.
20. **QR-Map: Map-Based Circuit Abstraction for Qubit Reuse Optimization** (Yonsei) — `3731020` ·
`HPC_FOR_Q`, `FUTURE_WORKLOAD` · NISQ. *HPC:* register allocation and liveness analysis with a new
abstraction to make the classical search tractable.
21. **Genesis: A Compiler for Hamiltonian Simulation on Hybrid CV-DV Quantum Computers**
(Rutgers/NC State) — `3731065`, arXiv 2505.13683 · `HPC_FOR_Q`, `Q_FOR_HPC` ·
Artifact **`PUBLIC_CODE`** `https://github.com/ruadapt/Genesis-CVDV-Compiler` · NISQ/GENERAL.
Code cross-validated (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §14, verdict `CONSISTENT`):
ANTLR Hamiltonian DSL, 20 `.ham` benchmarks, Threshold Accepting beating a Christofides routing
baseline by 3–7% (mean 4.8% depth). **Classical compile cost reported and steep** — LiH (4,12),
631 Pauli strings → 20.39 s; C₂ (12,18), 1,884 strings → 1,152.00 s (≈3× input, ≈56× time).
22. **Reinforcement Learning-Guided Graph State Generation in Photonic Quantum Computers**
(Pittsburgh) — `3731085` · `HPC_FOR_Q` · NISQ/GENERAL. *HPC:* a classical RL training/inference
workload substituted for heuristic search over probabilistic fusion sequences.

### ISCA 2026 — 11 of 161 · Sessions 4D "Quantum 1", 8C "Quantum 2", 9C "Quantum 3"

All DOIs `10.1109/ISCA66397.2026.<suffix>`.

23. **Triage: An Adaptive Parallel Window Decoding Scheduler for Real-time FTQC** (HKUST-GZ) —
`00069`, pp. 842–856, arXiv 2605.04459 · `HPC_FOR_Q`, `Q_IN_HPC`, `FUTURE_WORKLOAD` ·
ARCH_SIMULATION (custom Python 3.9 discrete-event simulator) + SOFTWARE_SIMULATION (Stim) · FTQC ·
Artifact `UNKNOWN`.
**The corpus's most developed statement of "decoding as a constrained resource-allocation
problem."** Resource model extracted in `DEEPDIVE_QEC_DECODING.md` §8: a **slice** `S(t,p)` is the
syndrome data from one square logical patch over a d-round cycle; a pool of **M physical decoders
serves N logical qubits with M ≤ N**; decoder latency is modelled `t_decode = A·volume^α` with
**α = 1.17** fitted to PyMatching; the failure mode is **exponential syndrome backlog** when
`τ_dec ≥ τ_gen`; scheduling is an assignment `π: V' → {1..M}` where `V'` must be an **independent
set** in the constraint graph with `|V'| ≤ M_available`, minimizing idle syndrome layers inserted at
Pauli-frame synchronization. **52.6% average LER reduction** vs time-parallel-only window decoding
under resource-constrained scenarios; d = 9 measured, extrapolated to d = 21, p = 3×10⁻³.
24. **Coset Ensemble Decoder for Quantum Error Correction with Algorithm-Hardware Co-Design**
(Imperial/Rutgers) —
`00070`, pp. 857–871, arXiv 2606.11076 · `HPC_FOR_Q` · FTQC ·
Artifact **`PUBLIC_CODE`** `https://github.com/IMSeonL/coset-ensemble-decoder`.
Union-Find-derived ensemble forest exploration approximating coset-level maximum-likelihood
decoding, with **temporal** resource reuse instead of code-distance-proportional spatial growth,
plus multi-bank memory hashing and hierarchical ID mapping. Claimed up to **8.2× fewer LUTs than
*reported* UF-based decoder resources** — note the paper's own wording is "reported", i.e. a
literature-table comparison, not a head-to-head re-synthesis.
**Code cross-validation** (`DEEPDIVE_QEC_DECODING.md` §4, verdict `PARTIAL_MATCH`): the algorithm
and memory system are verifiable (V_M = 22 vertex banks with hash `(x+3y+5z) mod 22`, E_M = 9 edge
banks, bank-conflict detection, a two-level DSU for hierarchical IDs, cycle-accurate decorators),
but **`hardware_code/` contains only `.gitkeep`** — the RTL is promised, not released, so the LUT
claim is **not reproducible-in-principle from this repo**. Modality is therefore
**CYCLE_SIMULATION**, not `FPGA_PROTOTYPE`.
25. **A Streaming Architecture for Quantum Error Syndrome Compression at 4 Kelvin** (Wisconsin) —
`00071`, pp. 872–888 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · FTQC · Artifact `UNKNOWN` ·
**abstract not obtainable; QEC-specific fields UNKNOWN**. *HPC:* a streaming data-compression
datapath under a cryogenic power budget and a hard decoding deadline — the off-chip bandwidth wall,
at 4 K. ⚠ Do **not** confuse with *CryoZip* (arXiv 2606.30805), a different paper by different
authors (Michigan/Brown) on the same topic; CryoZip is not in the ISCA 2026 volume.
26. **Transpiler-Architecture Co-Design to Curb Clifford Costs in FTQC** (UBC/PNNL/UCSD/UT Austin) —
`00072`, pp. 889–904, arXiv 2412.15434 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · FTQC ·
Artifact **`PUBLIC_ARTIFACT`** `https://zenodo.org/records/19449157`.
27. **Kernpiler: Compiler Optimization for Quantum Hamiltonian Simulation with Partial
Trotterization** (Penn/ETH/Yale/USRA/PNNL/UMD/MIT) — `00073`, pp. 905–920, arXiv 2504.07214 ·
`HPC_FOR_Q`, `Q_FOR_HPC` · NISQ/EARLY_FTQC · up to **10× gate and depth reduction**.
28. **Distilling Magic States in the Bicycle Architecture** (Yale/IBM/MIT) — `00148`, pp. 2081–2095 ·
`HPC_FOR_Q`, `FUTURE_WORKLOAD` · FTQC. *HPC:* producer/consumer provisioning — how many distillation
units feed a compute region.
29. **O3LS: Optimizing Lattice Surgery via Automatic Layout Searching and Loose Scheduling**
(HKUST-GZ/NUDT) — `00149`, pp. 2096–2110, arXiv 2604.15099 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · FTQC.
*HPC:* automatic floorplanning plus list scheduling replacing hand-built layouts.
30. **Leveraging Phase Polynomials for Quantum Circuit Optimization** (Rutgers/CMU/Yonsei) —
`00150`, pp. 2111–2126 · `HPC_FOR_Q` · GENERAL.
31. **Unifying Qubit Routing Across Diverse Quantum ISAs via Canonical Representation**
(HKUST/Tsinghua/Edinburgh/Leiden/HKU) — `00162`, pp. 2302–2317 · `HPC_FOR_Q` · NISQ/GENERAL.
*HPC:* the portable-compiler-backend argument (LLVM-style) applied to QPUs — one routing engine
retargeting across superconducting, ion, neutral-atom and photonic ISAs.
32. **TUSQ: Tracking, Uncomputation, and Sampling for Noisy Quantum Simulation** (UChicago) —
`00163`, pp. 2318–2332, arXiv 2508.04880 · `HPC_FOR_Q` · NISQ. Directly comparable to 2025's
Computational Reuse: both cut the *classical simulator's* work for noisy-trajectory evaluation.
33. **Photonic Quantum Computing on Spin Memory Architecture with Tree-Encoded Fusion**
(Edinburgh/UChicago/CUHK/Northwestern) — `00164`, pp. 2333–2348 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
EARLY_FTQC/GENERAL. *HPC:* a memory-hierarchy question — where to buffer quantum state, capacity/
retention vs throughput, and scheduling fusion attempts against memory occupancy.

## 3. Exclusions

**SATIC** (`00165`, pp. 2349–2363, Univ. of Minnesota), despite sitting in the session named
"Quantum 3", is an **Ising-machine compiler on a classical CMOS/oscillator substrate** — confirmed
independently on the authors' lab page, which lists it alongside a coupled-oscillator Ising chip
(Nature Electronics 2025) and an all-to-all CMOS Ising solver (Sci. Rep. 2024). Excluded as
quantum-inspired classical. **This independently reproduces the prior finding that the strict
ISCA 2026 count is 11, not 12.**

Also excluded: DS-ISA, DS-GL, DS-TPU, ReAIM (classical dynamical-system and Ising accelerators);
MD-pipe (ab-initio-accuracy molecular dynamics — classical quantum chemistry); Mirage/LightML/
Shining Light on Silicon Photonic DNN Accelerators (classical integrated photonics); the entire
FHE/ZKP/crypto population across all three years (HEAP, Neo, FAST, Finesse, zkSpeed, GenZA, 2026
Sessions 5C and 7D); WaferBRAIN and the SNN papers.

**FTQCSA 2025** — the Workshop on Fault-Tolerant Quantum Computer System Architecture, held 22 June
2025 at Waseda "in conjunction with ISCA2025", i.e. on the workshop days before the 23–25 June main
program. Its six strongly on-topic talks (including a polylog-time parallel MWPM decoder) were
cross-checked against the complete 135-item main program: **zero leakage**.

**Explicitly checked and not found** at ISCA 2024/2025/2026 across all 394 program titles: any
classical superconducting SFQ/RSFQ processor paper (the class that leaked at MICRO), any quantum
sensing paper, any post-quantum-cryptography paper, any pure device-physics paper. The crypto
papers present are FHE and zero-knowledge, not PQC.

## 4. What ISCA rewards as a contribution

A clean and datable pivot. **2024 is entirely single-QPU compilation and error mitigation.** From
**2025** the profile becomes HPC-shaped: speculation and rollback in the decoding pipeline (SWIPER),
barrier synchronization across logical qubits (Synchronization for FTQC), datacenter interconnect
topology (SwitchQNet), host↔accelerator integration (Qtenon), branch prediction in the control
processor (ARTERY), and classical simulator throughput (Computational Reuse). **2026** consolidates
around the decoder as a *scheduled resource* (Triage), decoder hardware co-design (Coset Ensemble),
the cryogenic bandwidth wall (4 K syndrome compression), and FT compilation cost.

The recurring shape is: **take a classical architecture mechanism and apply it to the quantum
control or correction path.** Speculation, branch prediction, barriers, windows, memory hierarchy,
switch fabrics, canonical IRs — all imported wholesale. That is why this venue reads as the most
directly transferable to HPC of the six, and why its decoder papers are the ones that carry explicit
latency budgets and resource models.

**Relevant-share trajectory:** 7.2% → 12.2% → 6.8%. The 2026 *proportion* falls because the
population grew 27% (135 → 172 archival, or 23% on the research track, 131 → 161, with a fourth
parallel track added) while the quantum sessions stayed at three. In absolute terms the quantum block is stable at 11–16 papers a
year — `OBSERVED_SHIFT` in composition, not in volume.

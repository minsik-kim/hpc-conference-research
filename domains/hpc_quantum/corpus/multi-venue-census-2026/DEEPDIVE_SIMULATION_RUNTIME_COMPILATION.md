# Deep Dive — Simulation, Runtime/Scheduling and Compilation (paper ↔ code cross-validation)

**Performed 2026-09-17.** Fifteen papers; nine repositories cloned and read. Same consistency and
evidence vocabulary as `DEEPDIVE_QEC_DECODING.md`. Zenodo file downloads are egress-blocked
(metadata readable), so Zenodo-only artifacts are recorded from the paper.

---

## Group 1 — Classical quantum-circuit simulation

### 1. C-3PQ (ICS 2026) — `INSUFFICIENT_EVIDENCE` (no artifact exists)
Statevector as a multi-dimensional tensor executed as tensor contractions; dimensions labelled
*local* or *global* by fit to a named memory level, with the graph analysis applied **recursively per
memory level**; partitioning by closeness centrality **`CC(vᵢ) = |RN(vᵢ)| / dist(vᵢ)`** `[paper]`.
Communication is **MPI** using **cray-mpich/8.1.30 GPU-aware collectives** on Perlmutter and Frontier
— *which* collectives is never named, and NCCL/RCCL are not mentioned. Codegen emits **C++, HIP and
CUDA**; stated limitation: the generated CPU code is **scalar** (no SVE/AVX), despite the A64FX
target. **Precision is not stated anywhere readable → `INSUFFICIENT_EVIDENCE`.** No compression.
**Scale:** Perlmutter (A100), Frontier (MI250X), Fugaku (A64FX); **weak scaling 30→36 qubits starting
at 4 GPUs for 30 qubits**; Frontier 30→37 with 4 and 8 GPUs. Baselines named: **Atlas** (SC24),
cuQuantum/Qiskit, SV-Sim; the body says only "competitive with the Atlas framework", and the
abstract's "up to 40% speedup vs a state-of-the-art NVIDIA-specific implementation" is **not restated
with hardware/circuit/scale context** → `PARTIAL` on that number. Classical partitioner cost *is*
reported: under one second for most circuits, ~4 s (`qnn`) and ~55 s (`vqc`).
**No GitHub/Zenodo link in the paper** — the only artifact DOI cited is the *baseline's* (Atlas).
**Term attacked: T_communication** ("Communication will dominate the overall execution time" on
accelerated systems), secondarily T_local_compute via per-target codegen.
**Modality: SOFTWARE_SIMULATION executed on REAL_HARDWARE (three production HPC systems).**

### 2. BMQSim (ICS 2025) — `INSUFFICIENT_EVIDENCE` (no repo), but paper evidence is complete
Statevector, **float64** — explicitly contrasted with cuQuantum's float32-only. Compression is
NVIDIA nvCOMP **bitcomp** plus a GPU log-transform **`b_a = g(b_r) = log2(1 + b_r)`** converting
relative to absolute bounds, at a **10⁻³ point-wise relative error bound**, with sign bitmaps and
pre-scanning. Stage-based partitioning adds gates to a stage until the global-index count hits a
threshold: a **33-qubit QFT goes from 2,673 compression events (one per gate) to 28** (one per stage).
**No MPI**; CUDA streams (2/GPU optimal); multi-GPU is embarrassingly parallel — *"Each GPU handles
partial SV groups and processes them locally without GPU-to-GPU communication."* Two-level GPU↔SSD via
**GPUDirect Storage/cuFile**, costing 0.7% on average.
**Numbers with context:** Xeon Gold 6238R + 2× A4000 (16 GB) + SATA SSD → **42 qubits in GPU memory,
47 with SSD**, vs baselines supporting ~30. Memory reduction is **highly circuit-dependent**:
cat_state 678.61×, ghz 678.52×, bv 424.77×, **QFT only 10.54×** (">10× on average"). Fidelity >0.99
for 24–30-qubit circuits; at 27-qubit QFT 0.998 vs SC19-Sim's 0.665. On 4× A100 NVLink, 28-qubit QFT:
**1.7× (2 GPUs), 2.3× (4 GPUs)** — the paper attributes the cap to **PCIe** and GPU launch overhead.
Built on SV-Sim; **no artifact URL in the paper**.
**Term attacked: T_memory (capacity), purchased with T_local_compute.** It does not attack
communication — it **removes the network from the design entirely**, and the residual PCIe term is
exactly what caps its multi-GPU scaling.

### 3. quEStab (ICS 2026) — `INSUFFICIENT_EVIDENCE`
Abstract only. ACM DL returned 403 on both `/doi/` and `/doi/pdf/` despite the Gold-OA/CC-BY marking,
and no preprint exists. Verified verbatim: extends the **stabilizer tableau** to mixed Clifford and
non-Clifford operations on multi-GPU platforms; **peak memory reduced up to 10,126×** vs statevector;
**up to 30,000 qubits**. **Deliberately not restated as findings:** the two-stage CUDA kernel pipeline
(row-counting vs row-update), the distribution of independent Pauli groups across GPUs, the
128-QASMBench / 78.1%-coverage figure, GPU model, baseline identity, precision, synchronization.
**Term: T_memory, by representation change** — the only simulator here that escapes 2ⁿ rather than
managing it.

### 4. Advancing Full-Stack Acceleration for Schrödinger-Style Quantum Simulation (HPCA 2026) — `INSUFFICIENT_EVIDENCE` on modality
Abstract verbatim confirms: index redirection and pre-compute merging "significantly reduce data
movement and computational complexity"; a **reconfigurable dataflow architecture** with adaptive
memory scheduling and swapping; an end-to-end toolchain; **maximum speedup exceeding 50× over the
GPU-based Qiskit baseline**; target regime **~30 logical qubits**.
**FPGA_PROTOTYPE vs RTL_SYNTHESIS remains unresolved.** Useful negative context: the same six authors'
companion toolchain paper **CAST** (arXiv 2503.19894) is explicitly **CPU/GPU-only** — LLVM IR
vectorization plus a PTX code generator, with no FPGA device names, no LUT/DSP/BRAM and no clock
frequency, reporting 8.03× over Qiskit at 32 qubits (CPU) and 39.3× over cuQuantum at 30 qubits (GPU).
So the HPCA paper's hardware layer is a **new** contribution relative to that toolchain; "reconfigurable"
plus the group's identity leans FPGA `[inference]`, but no board name, resource utilization or
synthesis report was seen, so it is **not asserted**.
**Term: T_memory + T_local_compute.** Single-device; no distributed term.

### 5. DD multi-node with ring communication (IEEE QSW 2024) — `INSUFFICIENT_EVIDENCE` (repo promised, never released)
Representation is **QMDD** as adopted by DDSIM. Node counts restricted to powers of two up to 256;
local qubits node-resident, global qubits force inter-node traffic. **Ring / "bucket relay"**
communication replaces broadcast — measured at **10–20% faster for Shor** and **~6× faster than
broadcast** for random circuits; sub-vectors are distributed by standard MPI during matrix-vector
multiplication. Two SWAP-insertion variants: **v1** preserves qubit order, **v2** minimizes swap count.
**Numbers with context:** Wisteria-O, **A64FX 48 cores @ 2.2 GHz, Tofu Interconnect-D (28 Gbps × 2
lane × 10 port)**. The **26×** is **38-qubit Shor (factoring 511, 400,123 gates) at 256 nodes with
ring + v1 versus single-node, 3,881 s → 147 s** — the same run as the "38-qubit Shor in 147 s" claim.
**Strong scaling, and non-monotonic:** 20-qubit QCBM (761 gates) is fastest at **32–64 nodes** and
*slower* at 128 and 256, because communication overhead overtakes the DD's node sharing.
Artifact: *"We will disclose our GitHub URL after the double-blind review process"* — **no repository
has appeared.**
**Terms attacked: T_communication and, uniquely in this corpus, T_synchronization** — the bucket relay
exists precisely to replace an all-node-synchronizing broadcast with pipelined neighbour exchange.

### 6. Stripping Quantum Decision Diagrams of their Identity (IEEE QSW 2024) — `PARTIAL_MATCH`
**Mechanism verified in merged upstream code** `[code]`. In
`mqt-core/include/mqt-core/dd/Package.hpp`, `Package::makeDDNode` carries the doc comment *"Reuses the
unique-table entry for an existing normalized node and **omits matrix nodes that represent an identity
level**"*, and for matrix nodes after `normalize` executes:
```cpp
// Check if node resembles the identity. If so, skip it.
if ((es[0].p == es[3].p) &&
    (es[0].w.exactlyOne() && es[1].w.exactlyZero() &&
     es[2].w.exactlyZero() && es[3].w.exactlyOne())) {
  auto* ptr = es[0].p;
  memoryManager.returnEntry(*e.p);
  return EdgeType<Node>{ptr, e.w};
}
```
The node is returned to the memory manager and the edge skips a level, so identity levels are never
materialized. Supporting symbols seen: `Edge::isIdentity(bool upToGlobalPhase)`,
`CachedEdge::isIdentity`, `Package::isCloseToIdentity` / `isCloseToIdentityRecursive`,
`reduceAncillae` / `reduceAncillaeRecursion`, plus the recorded invariants *"Missing DD levels
represent identity wires"* and *"Matrix widths include leading identity levels omitted from the DD"*.
`mqt-ddsim` is a thin C++ simulator over this package; the DD machinery lives in `mqt-core`.
**Why `PARTIAL_MATCH`:** the magnitudes (up to **70× runtime**, **3462× node-count reduction**, QFT to
**4,096 qubits**) could not be re-read from the paper body and the merged code ships no benchmark
reproducing them. **Term: T_memory (node count) + T_local_compute.** Single-node throughout.

### A. Simulation bottleneck table

| Paper | Term attacked | Evidence |
|---|---|---|
| **C-3PQ** | **T_communication** (primary), T_local_compute | stated objective "minimizes inter-node data movement"; GPU-aware cray-mpich collectives; per-target codegen |
| **BMQSim** | **T_memory**, paid in **T_local_compute** | bitcomp compression + GPUDirect SSD staging; stage partitioning purely to amortize compression; **no MPI**, "no GPU-to-GPU communication" |
| **quEStab** | **T_memory**, by representation change | 10,126× peak-memory reduction, 30,000 qubits via extended stabilizer tableau |
| **HPCA Schrödinger** | **T_memory + T_local_compute** | index redirection, pre-compute merging, adaptive memory scheduling/swapping; single-device |
| **DD ring (QSW'24)** | **T_communication + T_synchronization** | ring/bucket-relay explicitly replaces broadcast; SWAP insertion reduces global-qubit traffic |
| **Stripping identity** | **T_memory (node count) + T_local_compute** | `makeDDNode` skips identity matrix levels and frees the node |

**The split is clean: only two of six (C-3PQ, DD ring) genuinely attack the communication term, and
they are precisely the two that run on multi-node supercomputers.** The other four attack the memory
term on one device by four different routes — compression, representation, dataflow/scheduling and
structural elision.

---

## Group 2 — Scheduling, runtime, orchestration

### 7. Qoncord (MICRO 2024) — `PARTIAL_MATCH`
Full record and numbers in `CENSUS_MICRO_2024_2026.md`. Code findings: two-phase design confirmed
exactly (COBYLA with `tol=1e-1, rhobeg=1.0` on the low-fidelity backend, then `rhobeg=0.1` seeded
from the exploration optimum); resource model is `QuantumDevice(device_id, fidelity)` with **one FIFO
queue per device**, discrete timestep 1, one job per device; devices are synthetic
(`fidelities = linspace(0.3, 0.9, 10)`, 1,000 jobs); seven policies in `policy.py`; fidelity proxy is
a standard ESP model over Sabre-transpiled circuits. Modality confirmed **SOFTWARE_SIMULATION** —
`FakeKolkata`/`FakeToronto` plus an IonQ-Forte noise profile, **no real QPU execution**.
**Why `PARTIAL_MATCH`:** no single script emits the 17.4× headline; components are individually
reproducible, the composition is not in the repo. **Checklist gaps:** no DAG/task graph, no async
primitive, no reservation or release/reacquisition, no batching, no Slurm, no multi-QPU decomposition.

### 8. MILQ (ISC 2024) — `CONSISTENT` on the model, `PARTIAL_MATCH` on the 26%
MILP verified line by line in `src/scheduling/setup_lp.py` (PuLP): objective
`problem += pulp.lpSum(c_max)` — **pure makespan minimization**; variables `x_ik` (job→machine),
`z_ikt` (job-machine-timestep occupancy), `c_j`, `s_j`, `c_max`. **Unrelated parallel machines
confirmed** by `p_times[job][machine]`; **sequence-dependent setup** by `s_times[from][to][machine]`
with predecessor binaries `y_ijk`, and an extended variant adding `a_ij`, `b_ij`, `d_ijk`, `e_ijlk`.
**Constraint (15) is the interesting one:** `Σ_j z_ikt·job_capacities[j] ≤ machine_capacities[k]` per
timestep — **space-sharing/multi-programming**, several circuits co-resident on one QPU by qubit
count. Solver prefers Gurobi if available, else CBC. Circuit cutting wraps Qiskit's
`circuit_knitting.cutting.partition_problem` with shots hard-coded `2**12` and a `# TODO`.
**Baseline identified:** `src/scheduling/bin_schedule.py`, *"Generate baseline schedules … using
binpacking"*, with improvement computed as `(baseline − algorithm)/baseline × 100`. **So the 26% is
against a bin-packing scheduler**, not FCFS and not a commercial scheduler.
**Modality: SOFTWARE_SIMULATION** — three 5-qubit Qiskit fake devices under `AerSimulator`;
processing time from `transpile(..., scheduling_method="alap").duration`; setup time currently a
constant with an acknowledged TODO. The shipped default run is 5 circuits over 2–3 machines, one
batch, so the scale at which 26% was measured is not pinned by the repo.

### 9. Qonductor (SC 2025) — resource-model comparison
`BinarySchedulingProblem(ElementwiseProblem)` (pymoo) with `n_obj=2`, inputs `execution_times`
(**jobs × backends**), `fidelities` (**jobs × backends**), **`waiting_times` (per backend)**,
`job_sizes`, `backend_sizes`; solved with **NSGA2** plus `PseudoWeights` MCDM and
`StarmapParallelization`; execution-time inputs from a family of estimators (`RegressionEstimator`,
`CalibrationEstimator`, `PolynomialEstimator`, `GateLengthEstimator`, `PassManagerEstimator`,
`ScheduleEstimator`); `TranspilationLevel ∈ {QPU, PROCESSOR_TYPE, PRE_TRANSPILED}`.
**It shares MILQ's abstraction** — a QPU fleet reduced to a **job × backend cost matrix plus a
per-backend capacity** — with two differences that matter: Qonductor carries an explicit **per-backend
queue term** (`waiting_times`) that MILQ has no analogue for (MILQ instead carries sequence-dependent
*setup* times, and Qoncord *simulates* the queue discretely), and Qonductor is **multi-objective**
(time and fidelity as Pareto objectives) where MILQ is single-objective makespan and Qoncord is a
greedy policy. It is also the most reproduction-complete of the three.

### 10. TuniQ (ICS 2026) — `INSUFFICIENT_EVIDENCE` on code (Zenodo blocked), excellent paper evidence
Full record in `CENSUS_ICS_2024_2026.md`. Cost model verbatim:
`R_final = W · clip(log(ESP_rl / ESP_L3)) + φ(w₁·r_gates + w₂·r_depth)` — **W, w₁, w₂ are never given
numerically**, a real gap in an otherwise precise model. MDP state = one-hot stage indicator over
Qiskit's six stages + a **dual encoder** (logical qubit-interaction pre-layout; hardware-aware
post-routing with gate errors, T₁/T₂, connectivity) + global features; action = a Qiskit pass or
`skip` under **dynamic action masking**.
**Classical-cost accounting is the paper's distinguishing feature**, and it is only half complete:
training uses **8 parallel workers**, PPO, 2,048 steps/update, batch 64, over 30 perturbed backend
instances — but **wall-clock training time is not reported**, which is the single number a
"compilation is the HPC bottleneck" argument most needs. Inference "adds less than 1% to total
transpilation time".

### C. Scheduler resource models compared

| | Qoncord (MICRO'24) | MILQ (ISC'24) | Qonductor (SC'25) | TuniQ (ICS'26) |
|---|---|---|---|---|
| Abstraction | 10 synthetic devices, each `(id, fidelity)` | unrelated parallel machines: `p_times[job][machine]`, `s_times[from][to][machine]`, `machine_capacities[k]` | job×backend `execution_times`, `fidelities`; per-backend `waiting_times`, `backend_sizes` | **not a scheduler** — a per-circuit, per-stage pass selector over one backend's calibration |
| Objective | greedy policy: explore on low-fidelity, fine-tune on high-fidelity, tie-break least-loaded | `LpMinimize` on `c_max` — **makespan only** | **bi-objective NSGA2** (time, fidelity) + PseudoWeights | RL reward over ESP, gate and depth ratios |
| Solver | none (hand-coded policies) | PuLP → Gurobi if present, else CBC | pymoo NSGA2, parallelized | MaskablePPO |
| **QPU modeled as** | **a single-server FIFO queue** | **a machine** with sequence-dependent setup and a **qubit-capacity constraint permitting co-residency** | **a machine with an explicit queue attached** | **a noise profile**, not a resource |

**A QPU is never modeled as a memory hierarchy in any of the four.** MILQ's capacity constraint is the
closest thing to an occupancy model, and it is space-sharing, not hierarchy. The three real schedulers
converge on the same job×backend cost matrix and diverge on **where the queue lives** — simulated
(Qoncord), absent and replaced by setup times (MILQ), or a first-class input vector (Qonductor).

---

## Group 3 — Compilation and its classical cost

Records and numbers live in the venue census files; what follows is the cross-validation summary and
the compile-cost-vs-quality classification.

- **MIRAGE** (HPCA 2024) — `CONSISTENT`. Symbols seen: `Mirage(LegacySabreSwap)`, `ParallelMirage`,
  `_get_node_cns`, `MonodromyDepth`, `SabreLayout`, pass managers `CustomLayoutRoutingManager` /
  `Mirage` / `QiskitLevel3`, a hard-coded SWAP monodromy coordinate `[0.25, 0.25, 0.25, −0.75]`, plus
  a `deprecated/` tree preserving earlier CNS variants. Modality **ANALYTIC_MODEL / ARCH_SIMULATION**
  (monodromy polytopes + Haar Monte-Carlo; no QPU).
- **ZAC** (HPCA 2025) — `CONSISTENT`. **Repo is `github.com/UCLA-VAST/ZAC`** (the `UCLAVAST` spelling
  404s). `vmplacer.py` imports `scipy.sparse.csgraph.min_weight_full_bipartite_matching` and calls it at two
  sites (lines 293 and 502), confirming the bipartite-matching claim; `saplacer.py` is the SA initial placer; 7 experiment
  settings and 9 hardware specs ship. Modality **ANALYTIC_MODEL** — fidelity is *computed* from
  `f = f₁^g₁ · f₂^g₂ · f_exc^N_exc · f_tran^N_tran · Π_q(1 − t_q/T₂)` with f₂ = 99.5%, f₁ = 99.97%,
  T₂ = 1.5 s, not measured.
- **DC-MBQC** (HPCA 2026) — `CONSISTENT`, **the tightest paper↔code agreement in the whole set**, with
  one parameter discrepancy (`ubvec_max=1.2` in code vs α_max = 1.5 in the paper). Details in
  `CENSUS_HPCA_2024_2026.md`.
- **Genesis** (ISCA 2025) — `CONSISTENT`. ANTLR grammar `grammar/hamiltonianDSL.g4`, 20 `.ham`
  benchmarks, symbols `apply_rules_list_greedy`, `apply_rules_list_full_search`, `simplify_ops`,
  `StateEnv`, `Mapping`, `make_rectangle_graph`. Threshold Accepting beats a Christofides routing
  baseline by 3–7% (mean **4.8% depth reduction**). **Classical cost is steep and reported:** LiH
  (4,12) with 631 Pauli strings → **20.39 s**; C₂ (12,18) with 1,884 strings → **1,152.00 s** — a ~3×
  input growth for a ~56× time growth. No fidelity reported for final circuits.
- **MonteQ** (ISC 2026) — `CONSISTENT`. Symbols: `MCTS`, `tree_policy`, `rollout_policy`,
  `backpropagate`, `best_solution`, `build_anticommute_dag`, `cx_count`, `pauli_strings_commute`,
  plus Qiskit's `GreedySynthesisClifford` for the tail Clifford. **Search time is a first-class
  object:** `MCTS(..., stop_time, sims, ...)` runs `while current_time < (start_time + stop_time)` —
  a wall-clock budget in seconds — and candidates are ranked `(cx, depth, size, action_time, circuit)`.
  Reported single-iteration times **0.321–64.7 s**, roughly linear in iteration count.
  **arXiv id is 2604.19029**, not 2605.11375 (that id is TuniQ's). Reported reductions vs Rustiq are
  **51.6% max / 23.5% mean** (one iteration, 17 of 18 benchmarks) and **60.2% max / 27.2% mean**
  (200 iterations) — versus the abstract's "up to 53% (mean 30%)"; both readings recorded,
  `INSUFFICIENT_EVIDENCE` on the intended one.

### B. The compile-cost vs circuit-quality split

| Paper | Venue | Output quality reported | Classical compile cost reported | Headline framing |
|---|---|---|---|---|
| MIRAGE | HPCA 2024 | depth −29.58%, SWAP −59.86%, 2Q −16.97% (HHex), infidelity −9% | yes: 64Q QFT **47.9% faster**; no memory/complexity | **quality** |
| ZAC | HPCA 2025 | fidelity 22× (vs Enola) / 13,350× (vs Atomique); 3/7/10% optimality gaps | yes: **<1 s** without SA, 63× vs NALAC; **O(g·n³)** | **quality** |
| DC-MBQC | HPCA 2026 | photon lifetime 7.46×, exec cycles 6.82× (no gates/depth/fidelity) | yes: ~4–5 s vs ~8 s at 100q QFT | **quality** |
| Genesis | ISCA 2025 | depth −4.8% | yes: 20.39 s → 1,152.00 s across a 3× input growth | **quality** |
| MonteQ | ISC 2026 | CNOT −51.6% max / −23.5% mean (1 iter); −60.2% / −27.2% (200 iters) | yes: 0.321–64.7 s; **`stop_time` is an API parameter** | **quality** |
| TuniQ | ICS 2026 | TVD +20% avg; −27% gates, −25% depth at 30–50q | yes: −34% avg, **−68% at 30–50q**, 2–3× at 65q; inference <1% | **both, co-equal** |

**Tally:** HPCA 3/3 quality-headlined; ISCA 1/1 quality-headlined; ISC 1/1 quality-headlined;
ICS 1/1 compile-cost co-headlined.

**Verdict, stated plainly.** The evidence **supports the weak form and refutes the strong form** of
the proposition that these venues reward output quality over compile-time scalability.
*Weak form — these venues put a quality metric in the headline* — **supported**: 5 of 6 papers lead
with a quality metric and relegate compile time to an evaluation subsection.
*Strong form — compile-time scalability is not measured* — **refuted**: **all six report compile
time**, and three of them expose it as a **tunable design parameter** rather than an incidental
measurement (ZAC's SA on/off knob, MonteQ's `stop_time` budget, TuniQ's per-stage inference cost).
What is genuinely thin across all six is **compiler memory and search complexity**: only ZAC states an
asymptotic bound, **none reports compiler memory footprint**, and **none reports parallel or
distributed compilation**. TuniQ is the one paper whose contribution is defined by the classical cost
— and even it does not report training wall-clock time.

*This refines, rather than contradicts, the SC/ASPLOS finding carried in the Phase-1 corpus.* That
finding was about which argument is made **centrally** (SC's 3-of-3 compile-time-scalability arguments
vs ASPLOS's 2-of-10). The present six papers show that at ISCA/HPCA/ICS/ISC compile time is
**routinely measured but rarely the headline** — i.e. the difference between venues is in what earns
the abstract, not in whether the number exists.

### D. Distributed-simulation crossover `[inference]` throughout

- **C-3PQ**: `POSSIBLE_CROSSOVER` at **30 qubits**, since the weak-scaling series *starts* at 4 GPUs
  for 30 qubits and never runs single-device. At complex-double, 2³⁰ amplitudes is ~17.2 GB, which
  fits one 40 GB A100 — so the practical crossover is set by the desire to weak-scale, not by a hard
  capacity wall; and precision is unstated, so the arithmetic cannot be pinned. Communication term =
  redistribution of partitioned tensor dimensions between contraction stages.
- **BMQSim**: deliberately **pushes the crossover past 47 qubits on a single 16 GB GPU** (uncompressed
  complex-double at 42 qubits would be ~70 TB). Its multi-GPU mode has **no inter-GPU communication
  term at all**; the residual term is host↔device **PCIe**, which is exactly what caps it at 2.3× on
  4 GPUs. `POSSIBLE_CROSSOVER` above 47 qubits, unaddressed by the paper.
- **DD ring**: the crossover is **data-dependent, not qubit-count-dependent** — 38-qubit Shor scales
  to 256 nodes (26×) while 20-qubit QCBM **peaks at 32–64 nodes and regresses at 128–256**. The
  governing quantity is DD node sharing. **This is the corpus's one direct measurement of a
  distributed crossover going the wrong way.**
- **quEStab / Stripping identity**: both change the representation so qubit count stops being the
  capacity variable — stabilizer-term count and DD node count take over. Where either would need
  multi-node is `INSUFFICIENT_EVIDENCE` and `UNDEREXPLORED_IN_THIS_CORPUS` respectively.
- **HPCA Schrödinger**: scoped to ~30 logical qubits on one reconfigurable device; distribution is
  `UNDEREXPLORED_IN_THIS_CORPUS`.
- **Cross-cutting `OPEN_QUESTION`:** whether compression (BMQSim) and inter-node partitioning (C-3PQ)
  **compose** — compressed state fragments exchanged over GPU-aware MPI — is not evaluated by any
  paper in this set. BMQSim's design explicitly forgoes the network; C-3PQ's forgoes compression.

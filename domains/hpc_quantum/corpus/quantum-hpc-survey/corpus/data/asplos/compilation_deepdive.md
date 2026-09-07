All ten papers located and read. Nine had arXiv preprints; MorphQPV came from the authors' lab PDF. ACM DL and curl egress are both blocked, so **every full-text fact below is from a preprint or author-hosted PDF**, tagged accordingly — the published versions may differ.

---

# ASPLOS 2024–2026 Quantum Compilation / Mapping / Programming-Model Census

## Sources actually used

| # | Paper | Source read | Tag |
|---|---|---|---|
| 1 | PowerMove | [arXiv:2411.12263v1](https://arxiv.org/html/2411.12263v1) | `[paper-preprint]` |
| 2 | QTurbo | [arXiv:2506.22958v1](https://arxiv.org/html/2506.22958v1) | `[paper-preprint]` |
| 3 | Reducing T Gates | [arXiv:2503.15843v2](https://arxiv.org/pdf/2503.15843v2) | `[paper-preprint]` |
| 4 | ReQISC | [arXiv:2511.06746v2](https://arxiv.org/pdf/2511.06746v2) | `[paper-preprint]` |
| 5 | Borrowing Dirty Qubits | [arXiv:2508.17190](https://arxiv.org/pdf/2508.17190) | `[paper-preprint]` |
| 6 | GUOQ (Fast and Slow) | [arXiv:2411.04104](https://arxiv.org/pdf/2411.04104) | `[paper-preprint]` |
| 7 | One Gate Scheme (AshN) | [arXiv:2312.05652](https://arxiv.org/pdf/2312.05652) | `[paper-preprint]` |
| 8 | OnePerc | [arXiv:2403.01829v1](https://arxiv.org/html/2403.01829v1) | `[paper-preprint]` |
| 9 | Fermihedral | [arXiv:2403.17794v1](https://arxiv.org/html/2403.17794v1) | `[paper-preprint]` |
| 10 | MorphQPV | [fiction-zju.github.io/papers/ASPLOS2024-b.pdf](https://fiction-zju.github.io/papers/ASPLOS2024-b.pdf) | `[paper]` (author-hosted camera-ready) |

Volume mapping cross-checked against your `VOLUME_STRUCTURE.md`: PowerMove's DOI stem `3676642` is 30th-edition Volume 3 — **proceedings year 2025, presented 2026** — your note is correct and it is the only paper here in that position. All others have proceedings year = program year.

**One adjacent paper your list omits:** the Zhejiang group (Siwei Tan et al.) had a *second* ASPLOS 2024 quantum paper, **QuFEM: Fast and Accurate Quantum Readout Calibration Using the Finite Element Method** (`[documentation]`, lab publication page + [github.com/JanusQ/QuFEM](https://github.com/JanusQ/QuFEM)). It is readout calibration, not compilation, so it is out of scope here — but it means this group placed two papers in ASPLOS 2024, which matters for §C.

---

# PART A — PER-PAPER

---

## 1. PowerMove (ASPLOS'25 V3, presented 2026) — DOI 10.1145/3676642.3736128

**1. Research question.** How to compile circuits for neutral-atom machines that have *both* free qubit movement (AOD) *and* the zoned architecture (separate computation / storage zones), given that "fully leveraging these features poses significant compiler challenges, as it requires addressing complexities across gate scheduling, qubit allocation, qubit movement, and inter-zone communication." `[paper-preprint]`

**2. Previous limitation.** Named: **Enola** (SOTA baseline), **Atomique**, **Q-Pilot**, **DPQA / OLSQ-DPQA**, **Geyser**. Two stated failure modes, verbatim: prior work either *"settle[s] for a partially fixed layout [Enola, Atomique, Q-Pilot] or struggle[s] to handle fully dynamic layout transitions in a scalable manner [DPQA, OLSQ-DPQA]"*; and *"Solver-based methods attempt to tackle this space directly, but face scalability issues."* Enola-specific: it *"reverts to the initial layout before transitioning to the next stage"* (wasted movement), and *"Enola's framework does not incorporate a storage zone."*

**3. Core mechanism.** Three coupled passes. (a) **Stage scheduler**: edge-colour the CZ interaction graph into stages, then order stages greedily to minimise inter-zone traffic, scoring successive stages by |Qᵢ \ Qᵢ₊₁| + α|Qᵢ₊₁ \ Qᵢ|. (b) **Continuous router**: transitions directly between consecutive layouts with no intermediate canonical layout — qubits are labelled *static* / *mobile* / *undecided*, non-interacting qubits are parked in the storage zone, and undecided qubits are assigned nearest empty sites. (c) **Coll-Move scheduler**: groups single-qubit movements into AOD-legal collective moves (a conflict is defined as *"the order of x- or y-coordinate of two moving qubits chang[ing] after the movement"*), packs them distance-first, and parallelises across multiple independent AODs.

**4. Compilation-cost argument — PRESENT, and it is in the abstract.** Verbatim abstract: *"execution time improved by up to 3.46x and compilation time reduced by up to 213.5x."* Table 3 reports measured compile times against Enola: QFT-29 **24,116.00 s → 511.97 s (47.1×)**; BV-70 **4,334.5 s → 20.30 s (213.55×)**; QAOA-random-30 1,791.66 s → 193.28 s (9.27×). The complexity claim is verbatim: *"While NAQC compilation optimization for NISQ applications is NP-hard, we address this challenge through a near-linear heuristic algorithm."* Enola's cost is attributed to *"Maximum Independent Set solvers with higher time complexity."* **Caveat:** the DPQA/OLSQ-DPQA scalability claim is *asserted, not measured* — no timeout number is given for the SMT baselines. So this is the SC pattern applied to a heuristic incumbent, not to an exact solver. It also carries a very strong output-quality argument in parallel.

**5. What is optimized.** Output fidelity (decomposed into excitation error, transfer error, decoherence over idle time) and hardware execution time T_exe; compile time as a third, separately-reported axis. Not gate count — the paper notes it adds no two-qubit gates.

**6. Algorithmic approach.** Heuristic + graph algorithms: greedy edge colouring, greedy stage ordering, distance-aware conflict-free bin packing. Explicitly *not* SAT/SMT/ILP.

**7. Bottleneck.** Search-space-bound at the problem level (NP-hard joint scheduling/placement/routing), deliberately converted to compute-bound-but-near-linear by heuristic. `[inference]`

**8. Evaluation.** **SOFTWARE_SIMULATION only** — no hardware. 10–100 qubits, 23 benchmark variants: QAOA (regular-3, regular-4, random), QFT, BV, VQE, QSIM. Fidelity model parameters (Table 1): 1Q 99.99%, CZ 99.5%, excitation 99.75%, transfer 99.9%, transfer duration 15 µs, T₂ = 1.5 s, Rydberg radius ≈6 µm, AOD acceleration 2750 m/s².

**9. Baselines.** **Enola** (primary; version `NOT_FOUND`). Atomique, Q-Pilot, OLSQ-DPQA cited but not run — justified verbatim: *"Enola demonstrates a two-qubit fidelity that is 779 times higher than Atomique and 5806 times higher than Q-Pilot."*

**10. Quantitative results, disambiguated.**
- **Circuit-quality ratios** (simulated fidelity, same simulated machine, same benchmarks): QFT-29 7.12×10⁻⁹ → 5.78×10⁻⁴ (**81,151×**); BV-70 6.92×10⁻⁴ → 0.75 (**1,090×**); QSIM-rand-40 (**35,520×**); QAOA-regular3-30 0.48 → 0.68 (1.42×). Storage zone alone accounts for **313.86× average**. These are enormous because fidelity is multiplicative and the baseline is near zero — a ratio of two simulated fidelities, not a measurement.
- **Simulated execution-time ratios**: 1.11×–3.46× (VQE-50 10,196.5 µs → 5,354.37 µs). Modelled from Table 1 timing parameters, not wall-clock.
- **Wall-clock compile-time speedups**: 3.10×–213.55× (above). Same machine assumed but **CPU/host spec `NOT_FOUND`**.

**11. Hardware evidence.** `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (fidelity and execution time are both computed from Eq. 1 and Table 1, not measured).

**12. Maturity.** `NISQ` — the paper's own words, *"NAQC compilation optimization for NISQ applications."*

**13. Artifact.** `NOT_FOUND`. Verbatim: *"We will open-source our code later to foster further research and collaboration within the community."* No URL, no Zenodo DOI in the preprint. `INSUFFICIENT_EVIDENCE`.

**14. Why ASPLOS.** `[inference]` It is a three-pass compiler with an IR-like stage abstraction, evaluated on compile time, output quality and hardware execution time simultaneously — the classic architecture-conference triple. The zoned-architecture hardware feature is treated as an architectural resource to be scheduled, which is what distinguishes it from a physics-venue movement-optimisation paper.

---

## 2. QTurbo (ASPLOS 2026) — DOI 10.1145/3760250.3762227

**1. Research question.** How to compile programs for *analog* quantum simulators — producing pulse schedules for Hamiltonian simulation — efficiently and robustly.

**2. Previous limitation.** One named baseline: **SimuQ** (Peng et al., POPL 2024). Three stated failure modes, verbatim: *"the equation system used by SimuQ to determine pulse schedules solves all variables simultaneously, inherently leading to a large-scale mixed continuous–binary optimization problem and an exponentially large search space with a very long compilation time"*; *"the length of the compiled analog pulse sequence is not deterministic, usually far from optimal, and can vary unpredictably with different solver conditions"*; and *"In some cases, SimuQ even fails to yield a solution."* SimuQ solves via **SciPy**.

**3. Core mechanism.** QTurbo decomposes SimuQ's monolithic mixed continuous–binary system into a **two-level hierarchy**: one **global linear** equation system plus several **localized mixed** systems. The decomposition is found by treating the variable-dependency structure as a graph — *"the synthesized variables and the amplitude variables serve as nodes, while the arrows between them correspond to edges"* — and taking connected components as independent local subproblems. The global linear system is solved first to fix the synthesized intermediate variables; each local mixed system is then solved independently against those values; an iterative refinement pass bounds error propagation.

**4. Compilation-cost argument — PRESENT AND PRIMARY. This is the closest ASPLOS analogue to the SC pattern.** The measured incumbent-failure table (Table 1, "Limitation of State-of-The-Art", Ising cycle model) is:

| Qubits | 20 | 40 | 60 | 80 | 100 |
|---|---|---|---|---|---|
| SimuQ compile time (s) | 11 | 325 | 2,111 | 8,695 | **23,902** |

23,902 s ≈ 6.6 hours at 100 qubits. QTurbo claims *"around 600× (up to 1600×) acceleration in compilation time."* **Note on wording:** the paper attributes this to an *"exponentially large search space"*; the measured growth 11 s → 23,902 s over a 5× qubit increase is steep but consistent with a high-order polynomial as well. No big-O bound is given for either tool — `NOT_FOUND`.

**5. What is optimized.** Compile time (primary); compiled pulse-sequence length (51%, up to 90% shorter); compilation accuracy (72%, up to 100% improvement); resulting device error.

**6. Algorithmic approach.** Constraint-system decomposition + numerical solving + iterative refinement. It *replaces* a monolithic mixed-integer/continuous solve with a staged one — the same structural move as SC's papers, applied to a numerical rather than combinatorial solver.

**7. Bottleneck.** Search-space-bound in the baseline (joint continuous+binary solve); compute-bound after decomposition. `[inference]`

**8. Evaluation.** **REAL QPU** — QuEra **Aquila** (256-qubit Rydberg). Also simulated scaling to 100 qubits (Ising cycle). Two target systems run on Aquila; exact qubit count, observable and shot count on hardware are **`NOT_FOUND`**. AAIS targets: Rydberg (Aquila) and Heisenberg (superconducting / ion trap).

**9. Baselines.** **SimuQ** only, described as *"the only publicly available prior compilation framework for analog simulators."* Version `NOT_FOUND`.

**10. Quantitative results, disambiguated.**
- **Wall-clock compile-time speedup**: 600× average, 1,600× max, vs SimuQ. Host machine spec `NOT_FOUND`.
- **Output-quality ratios**: 51% (up to 90%) shorter pulse sequences; 72% (up to 100%) compilation-accuracy improvement — both compiler-output metrics, not runtime.
- **Real-device measurement**: 51% average / 94% max error reduction on Aquila. The paper states these *"directly translate into significant noise suppression on real device"*, indicating measurement on hardware.

**11. Hardware evidence.** `REAL_HARDWARE` (QuEra Aquila) for the error-reduction result; `SOFTWARE_SIMULATION` for the 20–100 qubit compile-time scaling.

**12. Maturity.** `NISQ` `[inference]` — the paper never uses NISQ/FTQC terminology, but analog Hamiltonian simulation on Aquila with no error-correction discussion places it squarely near-term.

**13. Artifact.** `NOT_FOUND` — no repository, Zenodo DOI or availability statement in the preprint; targeted searches returned nothing. `INSUFFICIENT_EVIDENCE`.

**14. Why ASPLOS.** Argued substantially by the paper `[paper-preprint]`: it is a compiler-architecture argument (restructure the solve to match the problem's dependency structure) with a wall-clock scalability result and real-hardware validation. `[inference]` This paper would also have been at home at SC — it is the one in this cohort whose argument shape is indistinguishable from PARALLAX's.

---

## 3. Reducing T Gates with Unitary Synthesis / **trasyn** (ASPLOS 2026) — DOI 10.1145/3779212.3790210

**1. Research question.** Verbatim: *"Which IR is better for FT compilation: U3 or Rz?"* — i.e. should fault-tolerant compilation synthesise arbitrary single-qubit unitaries directly, or decompose into three Rz rotations and synthesise each?

**2. Previous limitation.** **gridsynth** (Ross–Selinger) — *"state-of-the-art and is broadly adopted"*, but *"Rz gates represent only a subset of all possible single-qubit unitaries"*, forcing three separate syntheses at ε/3 each. **Synthetiq** — *"simulated-annealing approach struggles to scale to practical error thresholds."* **Solovay–Kitaev** — sequence length O(logᶜ(1/ε)) with c > 3, *"far from the information-theoretic lower bound."* **Fowler enumeration** — *"achieves a lower T gate count than Solovay-Kitaev but suffers from exponential runtime, limiting its practical utility."* Also **BQSKit** and **PyZX** as post-synthesis optimisers.

**3. Core mechanism.** Precompute every unique single-qubit matrix expressible within a fixed T budget (up to 15 T gates). Encode the space of *longer* sequences implicitly as a **matrix product state**: *"constructs a matrix product state (MPS) from short, precomputed gate sequences. This network implicitly represents longer sequences and supports efficient computation of trace distances via structured tensor contractions."* Attach the target unitary, contract, and read the trace values as a joint probability distribution over sequences; sample from it rather than enumerating. Post-process by substituting suboptimal subsequences from a lookup table. The MPS is what lets it go past the #T > 15 enumeration wall.

**4. Compilation-cost argument — PRESENT, but SECONDARY to output quality.** Both arguments are made and they must not be conflated.
- *Against prior tools (measured):* Synthetiq under a **10-minute per-instance limit** on 1,000 random Haar unitaries fails **1 / 931 / 1,000 instances** at ε = 0.1 / 0.01 / 0.001 — *"Synthetiq hits the 10-minute time limit we set and cannot find a solution."* Fowler enumeration is called out for *"exponential runtime."*
- *About its own method:* *"Explicitly enumerating every possible V and calculating all the trace values is time-consuming at compile time and becomes infeasible beyond #T > 15."* The Step-0 precomputation is O(4^#T) and *"took days on an NVIDIA A100 GPU to enumerate unique matrices with 15 T gates"* — a one-time offline cost, amortised across all future syntheses.
- *But the headline is quality.* The abstract's claim is verbatim: *"Compared to GRIDSYNTH-based circuit synthesis, for 187 representative benchmarks, our design reduces the T count by up to 3.5×, and Clifford gates by 7×, resulting in up to 4× improvement in overall circuit infidelity."* Speed appears in the contributions only as *"outperforms state-of-the-art synthesis algorithms."*

**5. What is optimized.** **T-count** (primary), T-depth, Clifford count; under an approximation-error budget (thresholds 10⁻¹ … 10⁻⁵) using D(U,V) = √(1 − |Tr(U†V)|²/N²).

**6. Algorithmic approach.** Exhaustive precomputation + tensor-network (MPS) representation + error-aware probabilistic sampling + lookup-table peephole. A synthesis method, not a solver.

**7. Bottleneck.** Split cleanly: the **offline precomputation is compute-bound and GPU-parallel** (O(4^#T), days on an A100); the **online synthesis is memory/contraction-bound** (O(2^ml) MPS construction, O(2^mkl) sampling). `[inference]`

**8. Evaluation.** **SOFTWARE_SIMULATION** — no quantum hardware. 1,000 random Haar single-qubit unitaries (RQ1); 187 circuits from **Benchpress**, **MQTBench**, **Hamlib**, plus custom QAOA; circuits span 2–592 physical qubits. Classical hardware: NVIDIA A100 GPU, AMD EPYC CPU.

**9. Baselines.** **gridsynth**, **Synthetiq** (error metric modified by the authors to match their Eq. 2 — worth flagging), **BQSKit**, **PyZX**, Qiskit transpiler across 16 settings / 4 optimization levels. Versions `NOT_FOUND` except Qiskit "v1.0+" (stated as implicit).

**10. Quantitative results, disambiguated.**
- **Circuit-quality ratios** — single-qubit synthesis vs gridsynth at ε = 0.001: T-count **3.74× geomean** (range 2.31×–6.12×); Clifford **5.73× geomean** (3.39×–9.41×). Circuit level over 187 benchmarks: T-count **1.38× geomean, 3.5× max**; T-depth 1.45×–1.66× geomean; Clifford 2.44× geomean, 7× max; infidelity 2.07× geomean improvement at logical error 10⁻⁵.
- **Wall-clock synthesis-time ratios**: *"one to two orders of magnitude faster than gridsynth"* at ε = 0.1 and 0.01; *"finishes most instances within seconds"* at 0.001.
- **Timeout counts** (not a ratio): Synthetiq 931/1000 and 1000/1000 failures.
- Same benchmark set and same classical host across tools; the Synthetiq comparison is not apples-to-apples because its error metric was modified.

**11. Hardware evidence.** `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (the infidelity numbers assume logical error rates 10⁻⁵–10⁻⁷; no device).

**12. Maturity.** `EARLY_FTQC`, explicitly. Verbatim: *"T gate is 100× slower compared to physical gates for most QEC codes due to magic state distillation"*; targets *"early fault-tolerant (EFT) systems"* at logical error 10⁻⁵–10⁻⁷.

**13. Artifact.** `PUBLIC_CODE` — **https://github.com/haoty/trasyn**. `[code]` MIT licence; pip-installable as `trasyn`; NumPy core with optional CuPy GPU path (CUDA 11/12); accepts targets as NumPy arrays, U(θ,φ,λ) Euler angles, or a single rotation angle; optional Qiskit integration transpiling to CNOT+U3; configurable non-Clifford budget and an execution-error-aware mode parameterised by logical error rate; README cites the ASPLOS 2026 DOI `10.1145/3779212.3790210` and points to a `paper` branch holding original code and data. Every distinguishing claim of the paper (tensor-based synthesis, GPU acceleration, error-aware synthesis, single-qubit scope) has a matching feature. **`CONSISTENT`.**

**14. Why ASPLOS.** `[inference]` The paper's frame is an **IR-selection question** (U3 vs Rz as the compilation intermediate representation) with a co-design argument tying synthesis error budget to QEC logical error rate — a compiler/architecture argument. A quantum venue would frame the same result as a gate-approximation theorem.

---

## 4. ReQISC (ASPLOS 2026) — DOI 10.1145/3779212.3790208

**1. Research question.** Verbatim framing: *"How can expressive continuous ISAs achieve practical performance gains on real hardware while managing calibration overhead and compilation complexity?"*

**2. Previous limitation.** Their own **AshN** / One Gate Scheme — *"limited to XY coupling."* Google **Sycamore fSim**, **SQiSW**, the **B gate**, **IBM fractional ZZ**, IonQ/Quantinuum continuous gate sets, and *"SU(4) proposals by Chen et al."* Two stated gaps: *"each 2Q gate must be carefully calibrated… presents significant execution challenges"*, and *"Neither gate set transpilation nor numerically optimal synthesis effectively exploits their synthesis potential for real-world program compilation."* The framing sentence is *"theoretically superior ISA may be inferior in practice."*

**3. Core mechanism.** Two halves. **Microarchitecture** (Algorithm 1): map any target SU(4) to Weyl coordinates (x,y,z) via KAK, choose among three execution modes (no-detuning, equal-amplitude ±) to minimise gate duration τ, then solve the resulting transcendental equations numerically (SLSQP + fsolve hybrid) for drive parameters Ω₁, Ω₂, δ — for *arbitrary* coupling Hamiltonians, not just XY. **Compiler**: template-based and hierarchical approximate synthesis with DAG commutation reordering, plus **gate mirroring** (append a SWAP to near-identity gates, resolving the permutation at compile time without adding 2Q gate count) and a **mirroring-aware SABRE** for routing. Calibration is handled by calibrating coupling and drive components separately, then jointly, with process tomography and XEB.

**4. Compilation-cost argument — LARGELY ABSENT; it is an output-quality paper.** There is a compiler-runtime figure (Fig. 16b, latency vs #2Q gates) but its function is defensive, not a scalability claim against prior art: *"ReQISC-Eff is consistently more efficient than TKet (C++ backend) and BQSKit (Rust backend)… ReQISC-Full offers performance competitive with BQSKit"*, and *"Both ReQISC-Eff and ReQISC-Full scale well in their runtime, despite being implemented in Python."* No timeouts, no complexity bound, no claim that any prior tool fails to scale. Numeric runtimes are **not tabulated** — `CONTEXT_NOT_STATED`.

**5. What is optimized.** Pulse duration (time-optimal SU(4) under the given coupling Hamiltonian), 2Q gate count, 2Q depth, program fidelity, SWAP/routing overhead. Secondary: **calibration overhead**, measured as the number of *distinct* SU(4) gates a program needs — an unusual and genuinely architectural cost metric.

**6. Algorithmic approach.** Analytic construction (KAK/Weyl) + numerical root-finding + grid search with two-stage local refinement + approximate synthesis + modified heuristic routing (SABRE).

**7. Bottleneck.** Compute-bound (numerical solving per gate, amortised over a small set of distinct SU(4)s). `[inference]`

**8. Evaluation.** **SOFTWARE_SIMULATION** — noisy QSim with a depolarizing channel scaled to gate duration. **No own real-QPU run**; hardware validation is cited from Chen et al.: *"This is demonstrated on transmons in [14], where various 2Q gates are implemented in high fidelity (on average 99.37%), with optimal gate duration."* 132 circuits, 17 categories (alu, bit_adder, encoding, QFT, QAOA, UCCSD, …), **3–170 qubits**, 9–33,000 two-qubit gates. Couplings modelled: XY (flux-tunable transmons), XX (trapped ions), arbitrary random.

**9. Baselines.** **Qiskit** (O3), **TKET** (PauliSimp + FullPeepholeOptimise), **BQSKit** (full compile, custom {Can, U3} gate set), plus SU(4)-fusion variants of each. Versions `NOT_FOUND`.

**10. Quantitative results, disambiguated.** All **circuit-quality ratios**, same 132-circuit suite, same simulated noise model:
- #2Q reduction: ReQISC-Eff **46.95%**, ReQISC-Full **51.89%** — vs Qiskit 5.34%, TKET 15.91%, BQSKit 7.99%.
- 2Q-depth reduction: 53.43% / 57.5%. Pulse-duration reduction: 68.03% / 71.0%.
- Microarchitecture: average 2Q pulse duration **1.341 g⁻¹** (XY) and 1.178 g⁻¹ (XX) vs **6.664 g⁻¹** for CNOT — the "**4.97×**" is a *per-gate average pulse-duration* ratio for arbitrary SU(4), **not** a whole-circuit number; the whole-circuit figure is the 71%.
- Fidelity: error reduction 2.36× (all-to-all), 3.18× (2D grid), **3.34×** (1D chain) — the 3.34× is topology-constrained simulated error, not a speedup.
- Routing: mirroring-SABRE gives 11.0% / 15.7% #2Q reduction vs standard SABRE on 1D chain / 2D grid.
- Calibration: ReQISC-Eff needs <10 distinct SU(4)s per program; ReQISC-Full <200, with >75% of programs under 20.

**11. Hardware evidence.** `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL`; real-hardware support is **cited from prior work**, not produced here.

**12. Maturity.** `NISQ` primary with forward-looking FTQC. Verbatim: *"Hardware noise presents critical challenges for both noisy intermediate-scale quantum (NISQ) and fault-tolerant application-scale quantum (FASQ) devices"*, and *"For the fault-tolerant regime… pathway to faster and higher-fidelity logical qubits."*

**13. Artifact.** `PUBLIC_ARTIFACT` stated in-paper: **https://zenodo.org/records/18163249**, DOI `10.5281/zenodo.18163249`, Apache 2.0. Described contents `[paper-preprint]`: `regulus/` (Python compiler), `microarch/genAshN/` (Algorithm 1 gate-scheme solver), `benchmarks/` (132 circuits), `artifact/` with Makefile, scripts and notebooks; demo <1 min, full results several hours. **I did not open the Zenodo archive itself** — the description above is the paper's own. `INSUFFICIENT_EVIDENCE` for independent consistency, though the URL is confirmed as stated.

**14. Why ASPLOS.** Argued by the paper `[paper-preprint]` — it is explicitly an **ISA design** paper ("instruction set computers", RISC/CISC framing) that carries the argument all the way down to microarchitecture (pulse solving) and all the way up to an end-to-end compiler with routing, and prices the *calibration* cost of a richer ISA. That vertical span is the ASPLOS move; a physics venue would publish the gate scheme alone.

---

## 5. Borrowing Dirty Qubits in Quantum Programs (ASPLOS 2026) — DOI 10.1145/3779212.3790134

**1. Research question.** What are the correct formal semantics for *borrowing* dirty qubits — *"ancillary qubits that can be borrowed from idle parts of a computation, enabling qubit reuse and reducing the demand for fresh, clean qubits — a resource that is typically scarce in practice"* — and how can safe uncomputation of a borrowed qubit be verified?

**2. Previous limitation.** Named: **Silq**, **Unqomp**, **Quipper**, **Microsoft Q#**'s `borrow` construct, **ReQWIRE**, **Qrisp**. Stated gap, verbatim: *"despite the broad investigation of dirty qubits in quantum algorithms and circuit design, relatively little attention has been given to dirty qubits from a programming language perspective"*, with Q# *"one of the few notable exceptions"* — but Q# has no formal definition or verification of safe uncomputation, leaving *"all potential risks to the programmer."*

**3. Core mechanism.** Extends the **QWhile** language to **QBorrow** with explicit `borrow` / `release`, gives a denotational semantics interpreting programs as sets of quantum operations, and defines *safe uncomputation* as the program acting as the identity on the borrowed qubit. The engineering payoff is a **reduction theorem**: for circuits implementing classical functions (X and multi-controlled NOT only), safe uncomputation is decided by two Boolean formulas per qubit — *"A quantum circuit implementing a classical function safely uncomputes a dirty qubit q if and only if both Boolean formulas (6.1) and (6.2) are unsatisfiable."* Those go to SMT/SAT solvers.

**4. Compilation-cost argument — PRESENT BUT INVERTED, and about the paper's own analysis, not prior art.** It uses solvers and shows *they scale*. Verbatim: *"By leveraging state-of-the-art Satisfiability Modulo Theories (SMT) and Boolean Satisfiability Problem (SAT) solvers such as CVC5 and Bitwuzla, we successfully verify safe uncomputation in practical circuits"*; *"The verification time includes only the duration taken by the SMT solvers to check the satisfiability of the resulting formulas, which constitutes the main performance bottleneck"*; and *"The experimental results demonstrate that our reduction method is both effective and scalable, enabling efficient verification of adder circuits with hundreds of qubits, as the verification overhead grows polynomially with the number of qubits."* For MCX, *"the method can handle instances with thousands of qubits."* **There is no baseline tool and no timeout comparison** — the scalability claim is absolute, not relative.

**5. What is optimized.** **Qubit count** — clean-ancilla demand. The illustrative example (Fig. 3.1) goes from *"five working qubits and two dirty qubits"* to *"five working qubits, without any additional ancillary qubits."* Aggregate qubit-savings across a benchmark suite is **`NOT_FOUND`** — the paper measures verification cost, not savings.

**6. Algorithmic approach.** Program analysis / formal semantics + reduction to Boolean satisfiability; SMT/SAT backend.

**7. Bottleneck.** Search-space-bound, explicitly self-identified: the SMT solve is *"the main performance bottleneck"*, polynomial in practice, NP-hard in the worst case.

**8. Evaluation.** **SOFTWARE only** — no hardware, and no simulation of quantum output either; this is a verification-runtime study. Benchmarks: constant-adder circuits (Häner et al.) and multi-controlled NOT (MCX). Sizes 50 to 1000+ qubits. Machine: *"MacBook Air equipped with an 8-core Apple M3 processor and 24 GB of RAM."* Reported: ~0.1 s for a 50-qubit adder; Figures 6.3–6.4 show the growth curves; **exact wall-clock values beyond that are `NOT_FOUND`** in the preprint text.

**9. Baselines.** **None.** No head-to-head with any other verification tool.

**10. Quantitative results.** Only verification wall-clock times (above) — **not** a circuit-quality ratio and **not** a speedup over anything. Adders to hundreds of qubits, MCX to thousands, polynomial growth. Everything else is qualitative.

**11. Hardware evidence.** `SOFTWARE_SIMULATION` (strictly, classical-solver measurement — no quantum execution at all).

**12. Maturity.** The paper's own framing is `NISQ`: *"quantum hardware in the current Noisy Intermediate-Scale Quantum (NISQ) era offers only a limited number of logical qubits and supports circuits of restricted depth and size."* `[inference]` Note the mismatch: dirty-ancilla borrowing in adders and MCX is a staple of *fault-tolerant* resource estimation, so the technique's natural home is broader than the framing.

**13. Artifact.** `NOT_FOUND` — a C++ implementation with an ANTLR4 frontend and CVC5/Bitwuzla backends is described with CMake build instructions, but no GitHub URL or Zenodo DOI appears in the preprint. `INSUFFICIENT_EVIDENCE`.

**14. Why ASPLOS.** Partly argued `[paper-preprint]`: the paper adds an explicit architectural-applications discussion — *"Single-program optimization… Multi-program scheduling…"* citing QuCloud. `[inference]` Without that section this is a POPL/OOPSLA paper; the qubit-as-scarce-shared-resource and multi-tenant-scheduling angle is what makes it an architecture-venue submission.

---

## 6. Optimizing Quantum Circuits, Fast and Slow / **GUOQ** (ASPLOS 2025) — DOI 10.1145/3669940.3707240

**1. Research question.** Verbatim: *"Can we design an optimization approach that can synergistically combine the powers of optimizing quantum circuits fast, via rewrite rules, and slow, via resynthesis?"*

**2. Previous limitation.** Two classes, each with a stated structural weakness. Rewrite-rule optimisers are *"fast to apply — match a pattern and rewrite it — but inherently only perform local optimizations"*, bounded by pattern size. Resynthesis is *"slow: usually a combinatorial search problem through the space of circuits"* and bounded by qubit count because the unitary is exponential in qubits. Tools named and run: **Qiskit** (level 3), **TKET**, **VOQC**, **BQSKit** (level 4), **QUESO**, **Quartz**, **Quarl**, **PyZX**, **Synthetiq**.

**3. Core mechanism.** A **simulated-annealing** search over a *combined* transformation pool. Each step picks at random both a transformation τ_ε (either a rewrite rule, ε = 0, or a resynthesis call on a ≤3-qubit subcircuit, ε > 0) and a subcircuit to apply it to; improvements are always accepted, regressions accepted with probability exp(−t·ΔCost) at temperature t = 10. A cumulative approximation-error ledger rejects any move that would push total error past ε_f = 10⁻⁸. Resynthesis calls are issued **asynchronously** to hide their latency behind continued rewrite-rule application — the one place the paper does treat compile time as an engineering resource.

**4. Compilation-cost argument — ABSENT. This is an output-quality paper, and it says so by construction.** Every tool including GUOQ is given *"1 hour, 32GB of RAM, and 1 CPU core"* (Quarl additionally gets an A100). The comparison is *what quality do you reach inside a fixed budget*, and Figure 7 plots cost against time within that hour. No tool is reported as timing out; no complexity bound is offered; the headline is verbatim *"guoq reduces two-qubit gate count by 28% on average while the next best tool, Quarl, has an average reduction of 18%."* This is the **anytime-algorithm** framing — compile time is held constant as an experimental control, which is the exact opposite of making it the dependent variable.

**5. What is optimized.** Two configurable objectives. **NISQ**: two-qubit gate count (primary) and circuit fidelity. **FTQC**: T-count primary, CX secondary, with an explicit cost function *2·#T(C) + #CX(C)*. Hard constraint Δ(U_C, U_C′) ≤ 10⁻⁸.

**6. Algorithmic approach.** Simulated annealing over a mixed rewrite/synthesis move set — a stochastic local search, not an exact method and not a learned policy.

**7. Bottleneck.** Search-space-bound with a compute-bound inner loop (each resynthesis call is a small combinatorial search); the asynchrony is a latency-hiding measure. `[inference]`

**8. Evaluation.** **SOFTWARE_SIMULATION / ANALYTIC** — no quantum execution. **247 circuits**, 4–36 qubits, original gate counts ~10 to ~10⁶. Gate sets: ibmq20, ibm-eagle, ionq, Nam, Clifford+T. Fidelity computed from **IBM Washington** calibration data (via Qiskit) and **IonQ Forte** device data — real calibration numbers, simulated outcome.

**9. Baselines.** Qiskit (level 3), TKET, VOQC (Hietala et al. 2021), BQSKit (level 4), QUESO (Xu et al. 2023), Quartz (Xu et al. PLDI 2022), Quarl (Li et al. 2024, GPU), PyZX (Kissinger & van de Wetering 2019), Synthetiq. Exact release versions `NOT_FOUND`.

**10. Quantitative results, disambiguated.** All **circuit-quality ratios** under an equal 1-hour budget:
- Two-qubit gate reduction on ibm-eagle: GUOQ **28% average** vs Quarl 18%, TKET 7%. Win/tie/loss: 233/5/9 vs Qiskit; 198/12/37 vs Quarl (out of 247).
- Fidelity (ibm-eagle calibration): GUOQ beats Qiskit on 220/247, Quarl on 183/247.
- Clifford+T / FTQC: GUOQ better-or-equal on 45% vs PyZX for pure T-count (**PyZX is stronger on T alone**); GUOQ beats Qiskit, BQSKit and Synthetiq on >90%. On CX in Clifford+T, GUOQ beats PyZX on 237/247, and **run on PyZX's output it reduces CX by a further 32% average without increasing T count** — a composition result, not a head-to-head.
- **No wall-clock speedup is claimed anywhere.**

**11. Hardware evidence.** `SOFTWARE_SIMULATION` with real calibration data — closer to `ANALYTIC_MODEL` for the fidelity claims.

**12. Maturity.** `GENERAL` — deliberately dual-target: the same annealer runs a NISQ objective and an FTQC objective by swapping the cost function. This is the hinge paper for §B.

**13. Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — **https://github.com/qqq-wisc/guoq**, Zenodo `10.5281/zenodo.14055562` (Docker image). `[code]` Apache-2.0; built on **QUESO** (separate repo, via `.gitmodules`); resynthesis backends are **BQSKit** (default) and **Synthetiq** (for Clifford+T) via `resynth.py`; Java 21 + Maven 3 + Python 3.8+; directories `benchmarks/`, `evaluation/`, `rules/`, `src/`, plus a `Dockerfile`. README cites ASPLOS 2025 and the paper by name. The rewrite-plus-resynthesis architecture and both named synthesis backends match the paper exactly. **`CONSISTENT`.** (`[code]` note: the README steers users to a wrapper called `wisq`; the annealing loop is inside `src/`, not visible from the landing page — so the annealing claim itself is `INSUFFICIENT_EVIDENCE` at this depth of inspection.)

**14. Why ASPLOS.** `[inference]` The technical content is squarely PL (rewrite rules, equality saturation lineage from Quartz/QUESO), but the framing is architectural: the objective function is parameterised by *device* (ibm-eagle vs ionq vs Clifford+T), fidelity is computed from real calibration data, and the contribution is a tool that targets whatever cost model the hardware imposes. The authors' own lineage runs through PLDI (Quartz) and OOPSLA (QUESO); moving to ASPLOS follows the device-cost-model framing.

---

## 7. One Gate Scheme to Rule Them All / **AshN** (ASPLOS 2024) — DOI 10.1145/3620665.3640386

**1. Research question.** Verbatim: *"whether all two-qubit gates can be realized as native instructions, and if so, whether this can be done via a universal gate scheme."*

**2. Previous limitation.** Fixed gates (**CNOT**, **CZ**, **iSWAP**) require decomposition of arbitrary SU(4); continuous families (**fSim**, **XY**) cover *"a substantial subset of two-qubit gates"* but *"There is still a wide variety of two-qubit gates that are not included."*

**3. Core mechanism.** Not tunable coupling — **time-independent Hamiltonian evolution with tunable microwave drive amplitudes and detunings**. The Hamiltonian is H_R = (g/2)(XX+YY) + Ω₁(XI+IX) + Ω₂(XI−IX) + δ(ZI+IZ) + (h/2)ZZ, with control knobs gate time τ, amplitudes Ω₁ and Ω₂, and detuning δ. The claim is that any two-qubit gate is reachable up to single-qubit rotations without decomposition: *"The AshN scheme can directly realize any two-qubit gate, up to single-qubit rotations, without decomposing it into multiple CNOT operations."* Proofs go through KAK decomposition and Weyl-chamber parameterisation, with several algorithmic variants (AshN-ND, AshN-EA±, AshN-ND-EXT) covering different amplitude/detuning regimes and a bounded-amplitude version at ~10% off optimal time. A side property: the scheme is *"completely impervious to ZZ error"* because the ZZ term can be absorbed into the parameters.

**4. Compilation-cost argument — ABSENT ENTIRELY.** No solver, no search, no compile-time measurement of any kind. The argument is pure output quality: *"Using our gate scheme, we observe marked improvements across various applications… generic n-qubit gate synthesis, quantum volume, and qubit routing."*

**5. What is optimized.** **Two-qubit gate count** (Theorem 3: any 3-qubit gate in ≤11 generic two-qubit gates; asymptotically (23/64)·4ⁿ − (3/2)·2ⁿ, i.e. ¾ of the CNOT count) and **physical gate duration** (average two-qubit interaction time 1.341 g⁻¹).

**6. Algorithmic approach.** **Analytic construction** with explicit constructive algorithms and theorems; numerical evidence supplements the lower-bound claim (6 two-qubit gates numerically sufficient for 3-qubit unitaries, vs the analytic 11).

**7. Bottleneck.** Not applicable in the usual sense — the construction is closed-form. `[inference]` The cost sits in hardware calibration, which this paper does not price (ReQISC later does).

**8. Evaluation.** **SOFTWARE_SIMULATION.** Verbatim: *"AshN has yet to be implemented in hardware."* Cirq simulation of quantum volume on a 2D grid with depolarizing noise 0.1%–1.7%; n = 3, 4 for synthesis counting.

**9. Baselines.** CNOT via flux-tuned CZ (6.664 g⁻¹ average), **SQiSW** (1.736 g⁻¹), iSWAP (4.712 g⁻¹), and quantum Shannon decomposition (QSD) for synthesis counts.

**10. Quantitative results, disambiguated.** All **circuit-quality / physics ratios**, no runtime anywhere:
- Average two-qubit gate time **1.341 g⁻¹** vs SQiSW 1.736 g⁻¹ = **1.29×** shorter; vs CNOT 6.664 g⁻¹ ≈ 4.97×.
- 3-qubit gate count: 11 (analytic) vs 20 for CNOT — **45% reduction**; numerically ~6 vs ~14 — **>50%**.
- Quantum volume: higher heavy-output probability than CNOT and SQiSW under the same simulated noise. Exact HOP values `NOT_FOUND`.

**11. Hardware evidence.** `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (theorems). Explicitly not implemented.

**12. Maturity.** Mixed, leaning `NISQ`: quantum-volume and gate-count gains are near-term, but the paper notes *"The CNOT gate local equivalence class… is most widely used in fault-tolerant computation"* and that AshN reaches CNOT-equivalence in π/(2g) without the SQiSW overhead.

**13. Artifact.** `NOT_FOUND` — no repository or DOI surfaced.

**14. Why ASPLOS.** `[inference]` The framing is the tell: "Complex Yet Reduced Instruction Set" is a deliberate CISC/RISC borrowing, positioning a two-qubit gate family as an **instruction set architecture** question rather than a gate-engineering one, and evaluating it on synthesis, quantum volume and routing rather than on gate fidelity alone. A physics venue would publish the same Hamiltonian result as a pulse-engineering paper without the ISA argument.

---

## 8. OnePerc (ASPLOS 2024) — DOI 10.1145/3620666.3651372

**1. Research question.** Photonic fusion-based computing has native operations that **fail probabilistically** (~75% success), and photons cannot wait — the paper's problem is that *"when fusion failures occur in real-time execution… the resulting state becomes a random graph state deviating from the target structure. Thus the execution needs to be retried until success, which is non-scalable."* Failed fusions are unrecoverable because fusion consumes the photons.

**2. Previous limitation.** One named prior compiler, **OneQ**: *"OneQ translates… graph state into a fusion pattern… However, it overlooks the severe randomness introduced by fusion failures, simply assuming that fusions always succeed."* Under retry-until-success at p = 0.75, even 4-qubit benchmarks need **>10⁶ resource state layers**, and sequential retry violates the photon lifetime.

**3. Core mechanism.** Three layers. The **online pass** performs a *predetermined, concurrent* set of fusions and then exploits **percolation**: *"when the fusion success probability exceeds a threshold, the resulting physical graph state contains a long-range-connected component with a high probability."* A 2D renormalization via path-searching extracts a coarse-grained regular lattice from whatever random connected component actually formed, using disjoint-set structures, and *"this modularity leads to a time complexity of O(1) constrained by the size of modules."* The **FlexLattice IR** then presents that lattice to the rest of the compiler as *deterministic* virtual hardware (2D layers flexibly interconnected in time), so the **offline pass** can do heavy graph-state mapping without ever seeing the randomness. Local complementation removes cyclic irregularities; pipelined feed-forward keeps the correction overhead constant.

**4. Compilation-cost argument — ABSENT as such, but a different computational-cost argument IS made.** No compile-time measurement appears for OnePerc or for OneQ, and no solver is claimed to time out. What *is* argued is a **hard real-time latency budget**: *"the limited lifetime of photons refuses the execution of over-complex algorithms in real-time"*; *"photons can have a lifetime of around 5000 RSG cycles in the delay lines"* at *"time scale ~1 ns for RSG cycles"*. The O(1) modular renormalization exists to fit inside that window. This is a **latency-bound online-algorithm argument**, structurally like a QEC decoder's deadline, and it is *not* the same as SC's compile-time-scalability argument. The headline comparison against OneQ is in **execution resources (#RSL)**, not seconds.

**5. What is optimized.** Number of consumed **resource state layers (#RSL)** — which sets execution time and photon loss — and number of fusions. Secondarily, the size of the extracted virtual lattice (which determines how much offline optimisation room exists).

**6. Algorithmic approach.** Percolation theory + graph algorithms (BFS shortest paths, disjoint sets) + heuristics (predetermined fusion patterns, tunable modular renormalization). **No SAT/SMT/ILP.**

**7. Bottleneck.** **Latency-bound** for the online pass (5,000-cycle photon lifetime is a hard wall); search-space-bound for the offline mapping, whose cost the paper does not analyse — *"The paper provides no explicit computational complexity analysis for the offline mapping algorithm itself."*

**8. Evaluation.** **SOFTWARE_SIMULATION only.** Simulated photonic hardware matching OneQ's model: 4-qubit and 7-qubit star-like resource states, tunable RSL sizes, programmable fusion success rate, hardware up to 240×240 RSLs. Benchmarks: QAOA (maxcut), QFT, ripple-carry adder (RCA), VQE, at **4, 9, 25, 64 qubits**. Fusion success 0.75 (practical) and 0.90 (hyper-advanced).

**9. Baselines.** **OneQ with retry-until-success** — the single baseline. No other compiler compared.

**10. Quantitative results, disambiguated.** All **execution-resource ratios** on the same simulated hardware, none are wall-clock:
- #RSL at p = 0.75: QAOA-4 1,708 → 48 (**35.6×**); VQE-4 1,017 → 23 (**44.2×**); QFT-4, RCA-4 and QAOA-25 all >10⁶ for OneQ vs 210 / 201 / 705 for OnePerc (**>10³×**). OnePerc alone reaches QFT-25 (2,271), RCA-25 (3,252), VQE-25 (759), QAOA-64 (2,787) where OneQ has no reported value.
- Stability: RSLs-per-logical-layer settles at **~3** independent of program size.
- Modular vs non-modular renormalization: modular reaches 60% of the unlimited-time non-modular lattice size, but **2–7× better** under the realistic photon-lifetime constraint — the clearest statement that the binding constraint here is time, not quality.
- Robustness down to fusion success **0.66**.

**11. Hardware evidence.** `SOFTWARE_SIMULATION`.

**12. Maturity.** `UNCLEAR` by the paper's own terms — it uses neither "NISQ" nor "FTQC". `[inference]` Fusion-based photonic computing is inherently a measurement-based / error-corrected architecture, but this paper stops at getting a usable lattice out of a random graph.

**13. Artifact.** `NOT_FOUND` — *"No public repository, code, or DOI is mentioned anywhere in the paper."*

**14. Why ASPLOS.** `[inference]` The contribution is an **IR** (FlexLattice) that separates a nondeterministic hardware layer from a deterministic compiler view — an abstraction-boundary argument, which is the ASPLOS thesis in its purest form. The online/offline split is also a runtime-vs-compile-time partitioning decision, i.e. a systems design choice rather than a physics result.

---

## 9. Fermihedral (ASPLOS 2024) — DOI 10.1145/3620666.3651371

**1. Research question.** Find the *actually optimal* fermion-to-qubit encoding for a **specific target Hamiltonian**, rather than using a Hamiltonian-independent construction.

**2. Previous limitation.** **Jordan–Wigner**, **Bravyi–Kitaev**, **parity**, **ternary-tree** encodings. Verbatim: *"Although some encodings have achieved asymptotically optimal encoding, it is still far from the optimal actual cost because the Hamiltonian of Fermionic systems from various domains can be very different"* — they are *"mainly theoretically constructed in a Hamiltonian-independent manner"* and *"still far from the actual optimal solutions"* despite O(log N) per-operator Pauli weight.

**3. Core mechanism.** Encode the algebraic structure of Majorana operators as SAT. Each Pauli operator becomes **2 Boolean variables** (I=00, X=01, Y=10, Z=11), so a length-N Pauli string is 2N variables. Anticommutativity becomes XOR constraints across operator pairs at every position; algebraic independence becomes XOR-equality-to-identity over all subsets. The objective is **Pauli weight** — either Hamiltonian-independent (sum over 2N Majorana operators) or Hamiltonian-weighted. Optimality is obtained by binary/descending search on the weight bound (Algorithm 1): *"We start from a larger w and gradually reduce w until the SAT solver cannot find a satisfactory solution."*

**4. Compilation-cost argument — PRESENT, BUT POINTED AT ITS OWN METHOD, NOT AT PRIOR ART. This is the exact inversion of the SC pattern.** SC's papers replace an exact solver with something polynomial. Fermihedral *introduces* an exact solver where the incumbents (JW, BK) were closed-form constructions with essentially zero cost, then spends Section 4 mitigating the resulting blow-up. The self-critique is verbatim: *"Scalability is a major concern of SAT as it is NP-complete, and the time-to-solution, even on small scales, is rather long"*, and *"the number of clauses grows exponentially as the number of Fermionic modes increases, which becomes the immediate bottleneck of our framework"* — algebraic independence *"incurs a large overhead by generating 2^(2N) clauses."* Table 3 shows the wall:

| N modes | 2 | 4 | 6 | 8 | 9 | 18 |
|---|---|---|---|---|---|---|
| Vars **with** alg. indep. | 70 | 2,224 | 49,902 | 1,050,544 | **N/A** | N/A |
| Clauses **with** | 459 | 10,926 | 210,064 | 4,283,375 | **N/A** | N/A |
| Vars **without** | 46 | 352 | 1,158 | 2,704 | 3,600 | (to N=18) |
| Clauses **without** | 331 | 3,014 | 10,601 | 25,693 | 36,037 | (to N=18) |

with the caption note *"(N/A denotes that generating the corresponding SAT instance takes over 1 hour.)"* — the full formulation dies at **N = 8**, and dies at *instance generation*, before solving. Note also: *"we exclude the time for the SAT solver to prove that a Pauli weight lower than optimal is unsatisfiable since it usually triggers a fixed timeout termination"* — i.e. UNSAT proofs time out and are excluded from reported times. And *"Time to complete experiments: 1 to 2 weeks."* **Crucially: the paper never compares its construction time against JW/BK construction time.** The argument *against the baselines* is 100% output quality.

**5. What is optimized.** **Pauli weight** (the direct proxy), which flows through to CNOT count, single-qubit gate count and circuit depth.

**6. Algorithmic approach.** Exact **SAT** with iterative bound tightening, plus two documented relaxations: (i) **drop algebraic independence** — justified because *"the probability for our SAT-based framework to generate an invalid encoding without considering the algebraic independence constraints is only 1/4^N"*; (ii) **simulated annealing** over Majorana pairings, applied on top of a SAT-solved Hamiltonian-*independent* encoding, to recover Hamiltonian-dependence without putting the weights in the SAT instance.

**7. Bottleneck.** **Search-space-bound**, self-identified, at two levels: clause *generation* (memory/time, 2^(2N)) precedes clause *solving*. `[code]` The README notes the solver *"uses only one core"* — this is a strictly sequential bottleneck as shipped.

**8. Evaluation.** **REAL QPU** — **IonQ Aria-1** (25 fully-connected trapped-ion qubits) via Amazon Braket, with stated device fidelities 99.99% 1Q / 98.91% 2Q / 98.82% readout. Plus **Qiskit Aer** simulation (Qiskit 1.0.1, Qiskit-nature 0.7.2). Classical host: AMD EPYC, 96 cores @ 2.4 GHz, 768 GB RAM. Benchmarks: molecular electronic structure (H₂ at 4 qubits; N = 4–12), Fermi–Hubbard (3×1 at 6 qubits, 2×2 at 8 qubits; N = 8–18), four-body SYK (N = 3–11).

**9. Baselines.** **Jordan–Wigner** and **Bravyi–Kitaev** as implemented in Qiskit. No other compiler.

**10. Quantitative results, disambiguated.** All **circuit-quality ratios** vs BK unless noted; none is a compile-time comparison:
- Pauli weight: **10–60% reduction** vs BK.
- CNOT count: **15–35% reduction**; single-qubit gates ~20%.
- Circuit depth: **15–60% reduction**.
- Simulated-annealing (approximate) variant: **21.63% average Pauli-weight reduction vs BK**.
- **Real-device H₂ ground-state energy on IonQ Aria-1**: full SAT **−1.56** vs BK −1.54 vs JW −1.49. This is a measured accuracy number on hardware, not a ratio. Shot counts `NOT_FOUND`.

**11. Hardware evidence.** `REAL_HARDWARE` (IonQ Aria-1) for the energy result; `SOFTWARE_SIMULATION` for the gate-count and depth sweeps.

**12. Maturity.** `NISQ` — evaluated on a ~99%-fidelity trapped-ion device with no error-correction discussion.

**13. Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — **https://github.com/acasta-yhliu/fermihedral**, Zenodo `10.5281/zenodo.10854557`, MIT. `[code]` Directories `fermihedral/`, `model/` (Hamiltonian patterns), `data/` (generated data and caches), `archive/`; notebooks `simulation.ipynb`, `singleshot.ipynb`, `hamiltonian-weight.ipynb`; `prepare.py` for environment setup; 91.3% Jupyter / 8.7% Python. README names **kissat** as the solver and advises *"To reduce the time to solve the SAT problems, we recommend to use a CPU with powerful single-core performance since the SAT solver uses only one core"* — matching the paper's single-threaded AMD EPYC setup exactly. Both approximation strategies are present. README carries the ASPLOS 2024 citation and references the IonQ experiments. **`CONSISTENT`.**

**14. Why ASPLOS.** Argued by the paper `[paper-preprint]`, which repeatedly calls itself a *"compilation framework"* and *"compiler framework"* and places fermion-to-qubit encoding as a **compiler pass** in the quantum-simulation toolchain rather than as a representation-theory result. `[inference]` The ASPLOS-ness is the reframing: a physics community treats fermionic encoding as mathematics; this paper treats it as an optimisation pass with a cost model, a solver backend, and an approximate fast path.

---

## 10. MorphQPV (ASPLOS 2024) — DOI 10.1145/3620666.3651360

**1. Research question.** How to verify quantum programs with **quantifiable confidence over the whole input space**, given that *"the superposition state greatly expands the search space for bugs, while the non-duplicability requires massive program executions to probe the program states."*

**2. Previous limitation.** Named: statistical assertions (**Stat**), projection-based measurement (**Proj**, Li et al.), non-destructive discrimination (**NDD**, Liu et al.), symbolic reasoning (**SR**), **Quito** (grid search), and deductive tools **Twist**, **Automa**, **QHL**. The core critique is verbatim: *"Existing assertion works exhibit low confidence in verifying the overall correctness of the program. This limitation arises from the fact that they can only validate the assertion under a small subset of test inputs, without the capability to generalize the validation result to the entire input space."* Concretely: *"Li et al. and Liu et al. only test a single input in each verification"*, and *"Quito applies a grid search on the input space, necessitating 4.8 × 10⁶ program executions to verify an 11-qubit QRAM program."* Also: for a 15-qubit quantum-lock program, prior confidence is *"a mere 0.006% after a single test and only reaches 50% confidence after testing 1.5 × 10⁴ inputs."*

**3. Core mechanism.** Exploit **linearity of quantum evolution** — the paper's "isomorphism": *"A quantum evolution is isomorphic, as the quantum operator is reversible (U⁻¹ = U† or O⁻¹ = O†). A linear isomorphism f satisfies the additivity and homogeneity."* Therefore *"For input represented as the linear combination of sampled inputs ρ_in = Σᵢ αᵢσ_in,ᵢ, tracepoint state ρ_t under this input is ρ_t = Σᵢ αᵢσ_t,ᵢ."* So: execute the program on a *basis* of sampled inputs (Clifford-group states), record tracepoint states, and thereafter predict the tracepoint state for **any** input by decomposition rather than re-execution. On top of that sits an **assume-guarantee contract** over *pairs* of tracepoints — `assert(Tᵢ,Tⱼ) ≡ assume: P₁(ρ_Tᵢ), P₂(ρ_Tⱼ), guarantee: P₃(ρ_Tᵢ,ρ_Tⱼ)` — which lets you state relations between states at *different program points*, something single-state predicates cannot express. Counter-examples are found by **quadratic programming** (Gurobi) over the approximated model, and a Beta-distribution fit turns results into a confidence bound. Note: it is **not** a neural/LSTM approximator, despite the "learning" framing.

**4. Compilation-cost argument — ABSENT. The cost being minimised is QUANTUM EXECUTIONS (shots), not classical compile time.** This is a third distinct cost model. Verbatim headline: *"MorphQPV reduces the number of program executions by 107.9× when verifying the 27-qubit quantum lock algorithm and improves the probability of success by 3.3×–9.9× when debugging five benchmarks."* Classical solve time is reported only to show it is not the problem: *"The quadratic programming solver shows the minimum validation time for programs with less than 12 qubits, which requires less than 12 minutes."*

**5. What is optimized.** **Number of program executions / sampled inputs** on the quantum device (primary); verification confidence (a formal guarantee, Theorem 3); bug-detection success rate. Classical validation time is secondary.

**6. Algorithmic approach.** Program analysis (abstract interpretation via linearity) + constrained optimisation (Gurobi QP for counter-example search) + statistical confidence estimation.

**7. Bottleneck.** **Latency/throughput-bound on the QPU** — the binding cost is device shots, not classical compute. `[inference]` Classical QP is a secondary compute cost.

**8. Evaluation.** **SOFTWARE_SIMULATION** (PennyLane/Qiskit); IBMQ timing estimates are *modelled*, not executed. Benchmarks and sizes: Quantum Lock (QL) 3–27 qubits, QNN 3–9, QEC 3–9, Shor 3–9, XEB 3–9, QRAM 11–21. Bug injection: 100 phase-gate mutations per program.

**9. Baselines.** Stat, Proj, NDD, SR (assertion methods); Quito (test generation); Twist, Automa, QHL (deductive). Versions `NOT_FOUND`.

**10. Quantitative results, disambiguated.** All are **quantum-execution-count or detection-rate** results — none is a classical wall-clock speedup and none is a circuit-quality metric:
- **Execution reduction**: 107.9× on 27-qubit QL (9.3×10⁵ → 8,974 executions); **31,563×** on 21-qubit QRAM vs Quito.
- **Bug-detection success rate**: 9-qubit QL — NDD 0%, Quito 0%, MorphQPV **100%**; 9-qubit QNN — Quito 50%, MorphQPV 100%; 9-qubit QEC — NDD 100%, Quito 0%, MorphQPV 100%.
- **Confidence improvement**: 3.3×–9.9× across five benchmarks.
- **Approximation speedup vs direct simulation**: 74.3× on 10-qubit programs — this one *is* a classical-compute ratio, and is about avoiding simulation, not about compilation.
- **Approximation accuracy**: exact when N_sample = 2^(N_in+1) (Theorem 2). Under simulated noise, accuracy is 13.7% (15-qubit Shor) and 1.6% (15-qubit QNN) with endpoint tracepoints only; adding four intermediate tracepoints lifts QNN from 1.6% to 13.6%. **These are low absolute accuracies and the paper reports them openly.**
- Classical solver time: <12 min for ≤12-qubit programs.

**11. Hardware evidence.** `SOFTWARE_SIMULATION`.

**12. Maturity.** `NISQ` — decoherence and measurement collapse are the modelled obstacles, mitigated with intermediate tracepoints.

**13. Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — **https://github.com/JanusQ/MorphQPV**, artifact-evaluated at Zenodo `10.5281/zenodo.10877687` (`[documentation]` from the lab publication page). `[code]` GPLv3; directories `morphQPV/`, `examples/`, `dataset/`, `data/`, `bugfix/`, `doc/`; API surface matches the paper — `add_tracepoint()` plus assume-guarantee primitives `IsPure()`, `Equal()`, `NotEqual()`; a confidence-estimation model; `main_exp.py` for the full experiments; `evaluation.md` documents artifact evaluation; `morphconfig.md` for configuration. The repo landing page does not itself name ASPLOS 2024 or list the QL/QRAM/QNN benchmarks, and the visible content does not confirm Gurobi. **`PARTIAL_MATCH`** — the distinctive mechanism (tracepoints + assume-guarantee contracts + confidence model) is clearly present; the specific benchmark suite and QP backend are `INSUFFICIENT_EVIDENCE` at this depth.

**14. Why ASPLOS.** `[inference]` The contribution is fundamentally a **cost argument about a scarce shared resource**: quantum device time. Recasting verification as "how few QPU executions buy how much confidence" is a systems-resource framing, not a formal-methods one — and the group's other ASPLOS 2024 paper (QuFEM, readout calibration) shows a consistent strategy of taking formal/statistical machinery and pricing it in device resources.

---

# PART B — CROSS-PAPER SYNTHESIS

---

## A. The compile-time-scalability question — **the headline finding**

**ASPLOS is different from SC, and the difference is stark.**

Your SC baseline: all three SC compilation papers (QFT Kernels, PARALLAX, DQTetris) make compile-time-scalability their central case — SATMAP timing out at 2 hours, DPQA at 24 hours, "our method does not have compilation time as it is an analytical approach." The measured failure of the incumbent exact method *is* the problem statement.

**ASPLOS tally over these ten papers:**

| Argument type | Count | Papers |
|---|---|---|
| **Compile-time scalability is the central case, with measured incumbent failure** | **2** | QTurbo, PowerMove |
| **Compile-time scalability is a real, measured, but *secondary* case behind output quality** | **1** | Reducing T Gates (trasyn) |
| **Output quality is the whole case; compile time is a control, a defensive check, or absent** | **4** | GUOQ, ReQISC, One Gate Scheme, Fermihedral |
| **A different cost model entirely** | **3** | MorphQPV (QPU shots), OnePerc (real-time execution latency), Borrowing Dirty Qubits (its own verification time) |

**2 of 10 clean, 3 of 10 counting the partial. SC was 3 of 3.**

The evidence, paper by paper:

- **QTurbo** — the one paper whose argument is structurally identical to PARALLAX's. Measured incumbent failure: SimuQ at 11 s → 325 s → 2,111 s → 8,695 s → **23,902 s** for 20 → 100 qubits, attributed to *"an exponentially large search space with a very long compilation time"*, with SimuQ sometimes failing outright. Replacement: decompose the monolithic mixed solve into a global linear system plus local mixed systems. Result: 600× average, 1,600× max compile-time acceleration. If you moved this paper to SC, nothing about its argument would need to change.
- **PowerMove** — compile time is in the abstract (*"compilation time reduced by up to 213.5x"*) with a real table (Enola 24,116 s → 512 s on QFT-29; 4,334.5 s → 20.3 s on BV-70) and an explicit complexity claim (*"NP-hard… we address this challenge through a near-linear heuristic algorithm"*). **But note the difference from SC**: the *measured* incumbent is Enola, a MIS-solver-based heuristic, not an exact SMT tool. The claim about actual exact solvers is asserted only — *"Solver-based methods attempt to tackle this space directly, but face scalability issues"* — with no number attached. And the paper's headline result by magnitude is fidelity (up to 81,151×), not compile time.
- **Reducing T Gates** — genuinely measured incumbent failure (Synthetiq: 931/1000 and 1000/1000 timeouts at a 10-minute limit; Fowler enumeration "exponential runtime"; its own brute-force "infeasible beyond #T > 15"), and a real speed claim (1–2 orders of magnitude faster than gridsynth). But the abstract sells **3.5× T-count and 7× Clifford**, and the contributions list mentions speed only in passing. The scalability work exists to *enable* the quality result.
- **GUOQ** is the cleanest counter-example and the most instructive one. It holds compile time **fixed at one hour for every tool** and asks who produces the best circuit inside it. Figure 7 plots quality against time within that hour. Compile time is the experimental *control variable* — the precise inverse of SC's treatment of it as the dependent variable. This is the anytime-optimiser framing, and it is a coherent alternative research programme, not an omission.
- **Fermihedral is the sharpest inversion of the SC pattern in the whole corpus.** SC's move is: an exact solver exists, it times out, replace it with something polynomial. Fermihedral's move is: closed-form constructions (JW, BK) exist and cost nothing to run but give poor output, so **introduce an exact SAT solver** and pay for it — then, because *"Scalability is a major concern of SAT as it is NP-complete, and the time-to-solution, even on small scales, is rather long"*, add two relaxations to get from N = 8 (where instance *generation* alone exceeds an hour) to N = 18. The paper never once compares its construction time to JW's or BK's. In SC's terms, Fermihedral is the paper SATMAP would have been.
- **One Gate Scheme, ReQISC, OnePerc, MorphQPV, Borrowing Dirty Qubits** make no compile-time-vs-prior-art argument at all. ReQISC's Figure 16(b) is a "we're not slower than TKET or BQSKit" check with no tabulated numbers. One Gate Scheme has no runtime measurement of any kind.

**Three distinct non-compile-time cost models appear at ASPLOS that do not appear in SC's compilation cohort at all:**
1. **Quantum device executions / shots** — MorphQPV: 9.3×10⁵ → 8,974 executions, 31,563× vs Quito. The scarce resource is QPU time, not CPU time.
2. **Hard real-time execution latency** — OnePerc: the online pass must fit inside a ~5,000-cycle photon lifetime, forcing an O(1) modular algorithm and *"2–7× improvement over non-modular under realistic time constraints"*. This is the deadline structure of a QEC decoder, applied to a compiler's online half.
3. **Analysis / verification time as its own scaling story** — Borrowing Dirty Qubits: SMT verification of adders to hundreds of qubits and MCX to thousands, *"the verification overhead grows polynomially with the number of qubits"*, with no baseline at all.

**The structural reading `[inference]`:** SC's compilation papers must justify themselves to a *performance* community, so the incumbent's wall-clock failure is the admission ticket. ASPLOS accepts a *design* argument — a better abstraction boundary (OnePerc's FlexLattice IR), a better instruction set (AshN, ReQISC), a better IR choice (U3 vs Rz), better language semantics (QBorrow) — and compile time is then one axis among several rather than the thesis. Where the two venues converge is precisely where the hardware is *analog and continuous* (QTurbo on Aquila, PowerMove on atom movement): there the compiler output is a schedule over continuous parameters, the search is genuinely large, and the argument reverts to SC's shape.

---

## B. NISQ → FTQC shift in compilation

The shift is **real but partial, and it is carried by one group rather than by the field**.

| Year | Paper | Paper's own framing | Optimized quantity | Evidence |
|---|---|---|---|---|
| 2024 | One Gate Scheme | NISQ-lead, FT-aware | 2Q gate count, pulse duration | Quantum volume is the headline app; notes CNOT class is *"most widely used in fault-tolerant computation"* |
| 2024 | OnePerc | Neither term used | #RSL, #fusions | Fusion-based photonics is FT-adjacent by construction, but the paper stops at lattice extraction |
| 2024 | Fermihedral | NISQ | Pauli weight → CNOT, depth | Real run on IonQ Aria-1 at ~99% 2Q fidelity; no QEC discussion |
| 2024 | MorphQPV | NISQ | QPU executions, confidence | *"decoherence/measurement collapse"* mitigations; noisy-simulator accuracy study |
| **2025** | **GUOQ** | **GENERAL — both, by design** | 2Q count **and** T-count | Two objectives in one tool: NISQ (2Q + fidelity on ibm-eagle/ionq) and FTQC (`2·#T + #CX` on Clifford+T) |
| 2026 | Reducing T Gates | **EARLY_FTQC, explicit** | **T-count, T-depth** | *"T gate is 100× slower… due to magic state distillation"*; targets logical error 10⁻⁵–10⁻⁷ |
| 2026 | PowerMove | NISQ, explicit | fidelity, execution time | *"NAQC compilation optimization for NISQ applications is NP-hard"* |
| 2026 | QTurbo | NISQ `[inference]` | compile time, pulse length | Analog Hamiltonian simulation on Aquila; no QEC discussion |
| 2026 | ReQISC | NISQ primary, FASQ secondary | 2Q count, pulse duration | *"both noisy intermediate-scale quantum (NISQ) and fault-tolerant application-scale quantum (FASQ) devices"* |
| 2026 | Borrowing Dirty Qubits | NISQ, explicit | qubit count | *"the current Noisy Intermediate-Scale Quantum (NISQ) era offers only a limited number of logical qubits"* |

**Reading.** In 2024, four of four are NISQ or near-term, optimising gate counts and device fidelity. The pivot is **GUOQ (2025)**, which is the first here to carry a fault-tolerant cost function (`2·#T + #CX`) as a first-class, switchable objective alongside the NISQ one — the same tool, two cost models. By 2026 exactly one paper — **Reducing T Gates** — is unambiguously fault-tolerant in target, metric and framing: magic-state economics, T-count and T-depth as the objective, and a synthesis-error-vs-logical-error-rate co-design (optimal synthesis error scales as √(logical error rate)).

**But three of the five 2026 papers still say NISQ in their own words**, and PowerMove says it in the same sentence as its complexity claim. So within *compilation*, ASPLOS 2026 is majority-NISQ. Two qualifications worth carrying forward:
- **Borrowing Dirty Qubits is framed NISQ but is functionally an FT-resource paper.** Dirty-ancilla borrowing in constant-adders and MCX is standard fault-tolerant resource reduction; the framing lags the technique. `[inference]`
- **ReQISC hedges deliberately**, naming both NISQ and FASQ and arguing a *"pathway to faster and higher-fidelity logical qubits."*

Against your existing QEC deepdive, the picture is that ASPLOS's FTQC weight in 2026 sits overwhelmingly in the **QEC decoder/architecture** cohort (five 2026 papers there), while the compilation cohort has moved only one paper fully across. The compilation track is a **step behind** the QEC track on the NISQ→FTQC transition.

---

## C. Groups and lineage, 2024 → 2026

### Yufei Ding — UCSD (with Cisco, PNNL, ORNL)
**OnePerc (2024, photonic) → PowerMove (2025 V3 / presented 2026, neutral atom).** Shared personnel: **Hezi Zhang** and **Jixuan Ruan** appear on both, with Zhang first on OnePerc and Ruan first on PowerMove — a clean student-succession pattern. Per your QEC deepdive the same group also placed **QECC-Synth** (ASPLOS'25 V1) and **iSwitch/Flexion** (2026), so the group spans compilation and QEC simultaneously.

*Agenda:* compilers for the hardware platforms that are **not** superconducting circuits, each defined by one exotic physical constraint — probabilistic fusion for photonics, free-but-costly atom movement plus zoned layout for neutral atoms. Method is constant across both: **graph algorithms and greedy heuristics, never solvers**; a layered pass structure with an explicit IR or stage abstraction; simulator-only evaluation with a hand-built device model. The 2024→2026 change is what they claim: OnePerc claims execution resources and real-time feasibility; PowerMove adds an explicit compile-time claim to the abstract. Ang Li (PNNL) and Travis Humble (ORNL) joining PowerMove is the group's first national-lab co-authorship in this set.

### Gushu Li — Penn (with AWS, LBNL)
**Fermihedral (2024) → QTurbo (2026).** Shared personnel: **Yuhao Liu**, **Shize Che**, **Junyu Zhou** on both, with Liu first on Fermihedral and Zhou first on QTurbo. Per your QEC deepdive, also **AlphaSyndrome** (2026), which brings in Costin Iancu (LBNL) — and Iancu is on QTurbo too, so LBNL is now a standing collaboration.

*Agenda:* compilation for **physics-simulation workloads** specifically — fermionic Hamiltonians in 2024, analog Hamiltonian simulation in 2026 — and this is the only group here that **runs on real QPUs in both years** (IonQ Aria-1 in 2024, QuEra Aquila in 2026). Lineage back to **Paulihedral** (ASPLOS 2022), same naming convention.

*The interesting reversal:* Fermihedral's contribution is to **install an exact solver** where the field used closed-form constructions. QTurbo's contribution is to **dismantle a monolithic solver** (SimuQ's SciPy solve) into a staged decomposition. The same group argued in opposite directions two years apart — because in 2024 the incumbent was cheap-and-suboptimal and in 2026 it was expensive-and-unreliable. That is a group that follows the cost structure of the problem rather than a methodological commitment.

### Swamit Tannu (+ Aws Albarghouthi) — Wisconsin
**GUOQ (2025) → trasyn (2026).** Shared personnel: **Amanda Xu** on both. Albarghouthi (PL) is on GUOQ but not on trasyn; Tannu (architecture) is on both — the 2026 paper is architecturally-led where the 2025 one was PL-led. Per your QEC deepdive the group also has **PropHunt** (2026).

*Agenda:* circuit optimisation as **search**, moving down the stack. GUOQ *orchestrates existing optimisers* (rewrite rules + BQSKit/Synthetiq resynthesis) with an annealer; trasyn *replaces the bottom-level synthesis primitive itself* with a tensor-network method. Correspondingly the metric moves from dual NISQ/FT to purely FT (T-count, T-depth, magic-state economics), and the compute profile moves from 1 CPU core to an A100. Group lineage runs Quartz (PLDI 2022) → QUESO (OOPSLA 2023) → GUOQ (ASPLOS 2025) → trasyn (ASPLOS 2026) — a walk from PL venues into architecture venues as the cost model became device-specific.

### Alibaba DAMO lineage
**One Gate Scheme (2024) → ReQISC (2026).** Shared personnel: **Dawei Ding**, **Cupjin Huang**, **Jianxin Chen**, **Qi Ye** — four of five 2024 authors reappear. ReQISC explicitly builds on its predecessor: *"Inspired by the AshN scheme [11], which was limited to XY coupling, our scheme accommodates arbitrary coupling Hamiltonians for any quantum processor."*

*Agenda:* the **quantum ISA as an architectural object**, expanded in scope each round. 2024: a single gate scheme for XY-coupled transmons, analytic theorems, no compiler, no hardware. 2026: arbitrary coupling Hamiltonians (XY, XX, random), a full end-to-end compiler (synthesis + mirroring + modified SABRE), a calibration cost model, and a released artifact. The 2026 paper is the same idea *productised* — it answers the objection its own predecessor invited (*"theoretically superior ISA may be inferior in practice"*).

**One observable worth flagging:** the affiliation set shifts substantially between the two papers. In 2024 the authors are DAMO Academy (plus Harvard, Tsinghua); in 2026, per your own author list, they are HKUST, Fudan/SIMIS, Tsinghua and DAMO/Alibaba. `[inference]` — the intellectual line is continuous while the institutional home has dispersed; I have no source confirming *why*, so treat the reason as unknown.

### One-off groups
- **Tsinghua / ISCAS / UTS** (Su, Zhou, Feng, **Mingsheng Ying**) — Borrowing Dirty Qubits. A quantum formal-methods group (Ying is the QWhile/quantum-Hoare-logic lineage) making a single appearance in this cohort, extending their own language framework and reaching for architecture relevance in a closing applications section.
- **Zhejiang University** (Siwei Tan, Liqiang Lu, Jianwei Yin) — MorphQPV **and** QuFEM, two ASPLOS 2024 papers in the same year, plus the JanusQ toolchain and tutorials at HPCA 2025 and ISCA 2026 `[documentation]`. This is the most **tooling-oriented** group in the set: everything lands in one open framework, and they have built a recurring tutorial presence at architecture conferences. They do not appear in ASPLOS 2025 or 2026 compilation.

**Concentration.** Four groups account for **8 of the 10 papers**. Two of those four (UCSD, Penn) also appear in your QEC cohort. This is a small, stable, recurring population — closer to SC's pattern than the paper count alone suggests.

---

## D. What an HPC version of these would look like — `[inference]`, all of it

Everything in this section is my analysis, not any paper's claim. I am describing where parallel or distributed structure is *visible in the algorithms as described*, not making a claim about what should be built.

**Naturally parallel / distributed — the structure is already there in the papers:**

- **Fermihedral's SAT phase** is the most conspicuous. The paper's own bottleneck is clause *generation* at 2^(2N) before solving even starts, the setup is single-threaded on a 96-core AMD EPYC, and the shipped README says outright *"the SAT solver uses only one core"* `[code]`. Two independent parallel structures exist in the algorithm as written: the descending search over Pauli-weight bounds w (Algorithm 1) is a sequence of independent SAT instances, and portfolio/cube-and-conquer parallel SAT is standard practice. Additionally the simulated-annealing relaxation over Majorana pairings is an embarrassingly parallel multi-start. The paper reports *"Time to complete experiments: 1 to 2 weeks"* on one core.
- **trasyn's Step-0 precomputation** — O(4^#T) enumeration of unique matrices, *"took days on an NVIDIA A100 GPU"* for 15 T gates — is a one-time, shareable, embarrassingly parallel build whose product is a static table. It has exactly the shape of a precomputed kernel database: build once at scale, distribute, amortise across every later synthesis call. The MPS contraction and sampling in Steps 1–2 are also standard tensor-network parallel workloads.
- **GUOQ** is a single-solution simulated annealer given 1 CPU core in the evaluation. Parallel-tempering, multi-start and portfolio variants are textbook for annealing, and the paper already dispatches resynthesis calls asynchronously — a latency-hiding structure that generalises to a worker pool over independent subcircuits. Its own experimental design (quality vs a fixed one-hour budget) is precisely the design in which added parallelism converts directly into result quality.
- **Borrowing Dirty Qubits** reduces to *two independent Boolean formulas per qubit*. For a thousand-qubit MCX that is thousands of independent, embarrassingly parallel solver calls. The paper's measurements run on a MacBook Air M3.
- **ReQISC's microarchitecture pass** solves transcendental equations independently per distinct SU(4) gate, and the paper reports <10 distinct gates for ReQISC-Eff and <200 for ReQISC-Full — a small, perfectly independent batch, trivially parallel and cacheable across programs. Its hierarchical synthesis uses grid search with local refinement, which is also parameter-parallel.
- **MorphQPV's sampling phase** executes the program on a basis of Clifford inputs — independent circuits that map directly onto multi-QPU or batched-job execution, which is exactly the resource model an HPC centre hosting quantum devices would present.
- **PowerMove's Coll-Move scheduler** already parallelises movement across multiple independent AOD arrays — parallelism in the *compiled artifact* rather than in the compiler. Its stage partitioning by edge colouring also yields independent per-stage routing subproblems.

**Intrinsically sequential, or where parallelism buys little:**

- **QTurbo's global linear solve** must complete before any localised mixed system can be solved — the two-level hierarchy is a strict dependency. The *local* systems are then mutually independent (they are connected components of the dependency graph), so the parallel structure is fork-join with a serial prologue; Amdahl's law binds on the global solve. The iterative refinement pass adds further serialisation.
- **OnePerc's online pass is sequential by physical necessity.** It runs inside a ~5,000-cycle photon lifetime, and its response depends on which fusions actually succeeded — you cannot speculate ahead of the measurement outcomes. The paper's own answer is spatial modularity giving O(1) per-module cost with disjoint-set structures, which is the only parallelism the deadline permits. Adding classical throughput does not help; only lower latency does.
- **PowerMove's continuous router** is sequential in the same way Promatch's predecoder is (per your QEC deepdive): each layout transition mutates the atom configuration that the next transition is computed against. Stages can be *partitioned* in parallel but not *routed* independently without reconciling boundaries.
- **One Gate Scheme** is a closed-form analytic construction. There is nothing to parallelise, which is the point of it — it is the AshN analogue of QFT Kernels' *"our method does not have compilation time as it is an analytical approach."*
- **GUOQ's and Fermihedral's acceptance chains** are sequential *within* one annealing trajectory; parallelism has to come from running many trajectories, which changes the algorithm's statistics rather than merely speeding it up.

**The one cross-cutting observation.** The papers that would gain most from HPC resources are the ones that currently report single-core or single-workstation setups (Fermihedral on one core for 1–2 weeks; GUOQ on 1 CPU core by experimental design; Borrowing Dirty Qubits on a MacBook Air), and in every one of those the parallel decomposition is already visible in the algorithm as published. The papers whose compile-time arguments are strongest — QTurbo and PowerMove — are the ones that got their speedups by *restructuring the algorithm*, not by adding hardware, and both retain a serial critical path afterwards. Whether that restructuring or added parallelism is the better lever is a question these papers do not measure, because none of them reports a parallel-efficiency or scaling study of its own compiler.

---

## Honest limits of this analysis

1. **No published version was read.** ACM DL returns 403 and curl egress is policy-denied for arxiv.org and api.crossref.org. All content is preprint or author-hosted PDF. Camera-ready versions routinely add or revise evaluation tables.
2. **Full-text extraction was via a summarising fetch tool**, so figure-only values (Fermihedral's Fig. 11 solve times, Borrowing Dirty Qubits' Figs. 6.3–6.4 wall-clock, ReQISC's Fig. 16b runtimes) are `CONTEXT_NOT_STATED` or `NOT_FOUND` rather than reported. Those three gaps all sit on the compile-time axis and would each strengthen or weaken a §A classification at the margin — none would move a paper across the main divide.
3. **Artifacts inspected at landing-page depth only.** I could not use the GitHub API (blocked for this session) and did not open the ReQISC Zenodo archive.
4. **QTurbo's real-hardware experiment is under-specified in the preprint** — qubit count, observable and shot count on Aquila are all `NOT_FOUND`, so the 51%/94% device-error reductions carry less context than they appear to.
5. **Baseline versions are `NOT_FOUND` for essentially every paper in the cohort** (Enola, SimuQ, gridsynth, Synthetiq, Qiskit, TKET, BQSKit, PyZX). This is a corpus-wide reporting weakness, not a research gap in my search.
6. **Two comparisons are not apples-to-apples and the papers say so:** trasyn modified Synthetiq's error metric to match its own Eq. 2, and PowerMove compares only against Enola, citing prior published ratios rather than re-running Atomique and Q-Pilot.

Sources: [PowerMove](https://arxiv.org/abs/2411.12263) · [QTurbo](https://arxiv.org/abs/2506.22958) · [Reducing T Gates](https://arxiv.org/abs/2503.15843) · [ReQISC](https://arxiv.org/abs/2511.06746) · [Borrowing Dirty Qubits](https://arxiv.org/abs/2508.17190) · [GUOQ](https://arxiv.org/abs/2411.04104) · [One Gate Scheme](https://arxiv.org/abs/2312.05652) · [OnePerc](https://arxiv.org/abs/2403.01829) · [Fermihedral](https://arxiv.org/abs/2403.17794) · [MorphQPV PDF](https://fiction-zju.github.io/papers/ASPLOS2024-b.pdf) · [guoq repo](https://github.com/qqq-wisc/guoq) · [trasyn repo](https://github.com/haoty/trasyn) · [fermihedral repo](https://github.com/acasta-yhliu/fermihedral) · [MorphQPV repo](https://github.com/JanusQ/MorphQPV) · [MorphQPV Zenodo](https://zenodo.org/records/10877687)
# Compilation / mapping and the classical cost of quantum algorithms

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **STRONG**. 428 occurrences of "compil-" across the
corpus; a dedicated deep-dive document (`compilation_deepdive.md`); and
the sharpest single ASPLOS-vs-SC comparison in the whole corpus.

## 1. Problem landscape

Quantum compilation (circuit mapping, gate synthesis, routing) has a
classical computational cost — this is the corpus's central case study in
how two venues can accept "the same kind" of paper for structurally
different reasons.

## 2. Key concepts

Compile-time scalability vs. output quality as the thing being optimized;
compile time as a dependent variable vs. an experimental control; exact
(solver-based) vs. heuristic vs. synthesized closed-form compilation.

## 3. Main mechanism families — two argument currencies

**SC's currency: compile-time scalability.** All **3 of 3** SC compilation
papers argue that the incumbent exact method's measured failure *is* the
problem statement — SATMAP measured at 2 hours, DPQA at 24 hours. The fix
in each case is a domain/architecture-specific kernel with a closed-form
or synthesized cost model.

**ASPLOS's currency: mostly output quality.** Of ASPLOS's ten
compilation/mapping papers, only **2** make the compile-time-scalability
argument centrally (QTurbo, PowerMove), with one partial (Reducing T
Gates). **7 argue output quality** (fewer gates, lower depth, better
fidelity) or use an entirely different cost model (QPU shots, hard
real-time execution latency, verification time).

**GUOQ is the cleanest inversion**: its stated protocol allocates each
tool a **1-hour budget "unless otherwise indicated"** (Quarl is an
explicit exception, run on an A100 with 64 GB) and asks who produces the
best circuit inside that budget — compile time as experimental *control*,
the precise opposite of SC's treatment of it as the dependent variable.

## 4. Representative papers

SC: SATMAP, DPQA-based mapping paper (both measured compile-time failure
as the problem). ASPLOS: GUOQ (`PUBLIC_CODE`, ships baseline Docker image
too), QTurbo, PowerMove (both compile-time-centered), Fermihedral
(fermion-to-qubit encoding, SAT-based, single-core 1–2 weeks), trasyn
(T-gate synthesis), Reducing T Gates (partial compile-time argument).

## 5. Historical lineage

Not treated as a single technical lineage in the source the way QEC
decoding is — the compilation branch is organized by *argument type*
(compile-time vs. output-quality) rather than by a technique lineage.

## 6. Implementation families

Predominantly software: Python/C++ solver and search code. GUOQ (Java +
two Docker images); Fermihedral (SAT solver, single-core). **None of the
ten ASPLOS compilation papers reports a parallel-efficiency or scaling
study of its own compiler**, despite several (Fermihedral's SAT search,
GUOQ's anytime search, trasyn's synthesis) being naturally parallel.

## 7. Important disagreements / tensions

This *is* the tension: SC and ASPLOS are shown arguing in fundamentally
different currencies about structurally similar work. The source does not
resolve which currency is "right" — it documents the asymmetry
(`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §10.2, "the sharpest single
result").

## 8. Current limitations

The compilation papers that would gain most from HPC resources are
precisely those reporting single-workstation setups (Fermihedral on one
core for 1–2 weeks; GUOQ on one CPU core by experimental design;
Borrowing Dirty Qubits on a MacBook Air) — an `[inference]` observation in
the source, not a measured claim, and the parallel decomposition each
would need is not evaluated by any paper in the corpus.

## 9. Research questions

Not indexed as a separate `CANDIDATE_QUESTIONS.md` entry — the
compile-time-vs-output-quality asymmetry is treated by the source as a
finding (F4 in the ASPLOS census), not an open question, so it is not
duplicated in the research/ index.

## 10. Deeper lookup paths

`../corpus/quantum-hpc-survey/corpus/data/asplos/compilation_deepdive.md` →
`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §10.2 →
`SC_2024_2025_QUANTUM_HPC_CENSUS.md` §7 (four acceptance pathways).

---

## Phase-2 extension — six-venue census (2026-09-17)

Source: `../corpus/multi-venue-census-2026/DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md`
§B and Group 3, plus every venue census. Descend there for quantitative claims.

**Compilation is the largest branch in the six-venue corpus — ~40 of 102 papers —
and the largest branch at every individual venue.** It is the one contribution
shape legible everywhere: ISCA 15, QSW 10, HPCA 8, ISC 3, ICS 2, MICRO 2.

### The compile-cost vs circuit-quality question, retested

The Phase-1 finding — SC's three compilation papers made a compile-time-scalability
argument 3-of-3, while only 2 of ASPLOS's ten did — was tested against six papers
whose code was read (MIRAGE, ZAC, DC-MBQC, Genesis, MonteQ, TuniQ).

**The weak form is supported; the strong form is refuted.**
*Weak form — these venues put a quality metric in the headline:* **supported**,
5 of 6 lead with fidelity, depth, gate count or cycles and relegate compile time
to an evaluation subsection.
*Strong form — compile-time scalability is not measured:* **refuted**. **All six
report compile time**, and three expose it as a **tunable design parameter** rather
than an incidental measurement — ZAC's SA on/off knob (<1 s without it, 63× vs
NALAC), MonteQ's `stop_time` wall-clock budget as an API argument, and TuniQ's
per-stage inference cost (<1% of transpilation).

So the venue difference is **in what earns the abstract, not in whether the number
exists**. This refines rather than contradicts the Phase-1 result.

**What is genuinely thin across all six:** only ZAC states an asymptotic bound
(O(g·n³)); **none reports compiler memory footprint**; and **none reports parallel
or distributed compilation** — even where the cost is severe. Genesis takes
**20.39 s for a 631-Pauli-string input and 1,152.00 s for 1,884 strings** — a ~3×
input growth for a ~56× time growth — and still runs single-node. Recorded as
`CANDIDATE` M8.

### TuniQ (ICS 2026) is the corpus's clearest "compilation is the HPC bottleneck" paper

An RL agent (MaskablePPO) selects passes per stage of Qiskit's six-stage pipeline.
Reward, verbatim: `R_final = W·clip(log(ESP_rl/ESP_L3)) + φ(w₁·r_gates + w₂·r_depth)`
— **W, w₁ and w₂ are never given numerically**, a real gap in an otherwise precise
model. Results vs Qiskit Level 3: TVD +20% average, compile time −34% average, and
at 30–50 qubits **−68% compile time, −27% gates, −25% depth**, on four IBM Heron
QPUs. Training uses 8 parallel workers — but **training wall-clock is not
reported**, which is the one number the argument most needs.

### Three compilation sub-branches that did not exist in the Phase-1 taxonomy

- **Autotuning** (TuniQ) — pass selection as a search problem over a
  millions-wide space.
- **Dynamic-circuit / classical-control compilation** (ISC 2026, QSW 2026) — the
  compile-side counterpart of real-time QEC: mid-circuit measurement and feedforward
  put the classical control path on the critical timing path, and these papers move
  work to compile time to get it off the per-shot path.
- **Distributed compilation** (DC-MBQC at HPCA 2026, DisMap at QSW 2026) —
  partitioning and inter-QPU layer scheduling against a non-uniform, drifting
  resource topology. DC-MBQC proves its layer-scheduling problem NP-hard by
  reduction from graph bandwidth and reports the tightest paper↔code agreement in
  the whole census.

### Corrections

- **ZAC's 22× is fidelity vs Enola** (with 13,350× vs Atomique) — not "zoned vs
  monolithic". Its repo is `UCLA-VAST/ZAC`; `UCLAVAST/ZAC` 404s.
- **MonteQ's reduction figures differ between abstract and body** (up to 53% /
  mean 30% vs 51.6% max / 23.5% mean at one iteration); both recorded,
  `INSUFFICIENT_EVIDENCE` on the intended reading. Its arXiv id is 2604.19029.
- **DC-MBQC is Peking University + CUHK**, not ICT CAS.

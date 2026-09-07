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

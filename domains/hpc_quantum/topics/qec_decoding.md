# QEC decoding (systems/throughput problem)

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **STRONG**. This is the densest single branch in the
imported corpus — 11 ASPLOS papers (QEC architecture, synthesis, and
decoding combined) plus SC's one QEC *reliability characterization* paper
— and the only branch with both a dedicated deep-dive document and a
dedicated lineage document.

## 1. Problem landscape

Quantum error correction requires a classical decoder to consume syndrome
measurements and identify the most likely error, fast enough to keep pace
with the physical device's syndrome-extraction cycle (`T_decode ≤
T_syndrome_cycle`) — otherwise a backlog accumulates. The imported corpus
treats this as a genuine HPC-shaped problem (latency-bounded,
throughput-bounded, parallelizable, with a hard bandwidth constraint at
the cryogenic boundary) that is nonetheless **absent from SC's main track
in both censused years** — see `../research/CANDIDATE_QUESTIONS.md` entry
G1, a `VENUE_GAP`, not a claimed research gap.

## 2. Key concepts

Minimum-weight perfect matching (MWPM/blossom) vs. union-find vs. belief
propagation as decoding algorithms; surface code vs. qLDPC as the code
family being decoded; the throughput model `T(P) = W/P + C(P)` (work
divided by parallelism, plus a communication/coordination term).

## 3. Main mechanism families — two irreconcilable design philosophies

**Line A (fixed-capacity predecoding)**: the exact matching stage has
**fixed combinatorial capacity** (Hamming weight ≤ 10, 945 matchings —
Astrea-G's capacity, inherited rather than introduced by Promatch), and
progress in code distance *d* comes from shrinking the problem to fit.
Accuracy becomes a tunable; the design cannot absorb more silicon.

**Line B (grow-the-machine)**: keep the algorithm exact and spend **O(d³)
processing units** — one vPU per decoding-graph vertex, one ePU per edge
(Micro Blossom's own notation is O, not Θ). Progress in *d* comes from the
machine growing with the graph, not from approximation.

These fail in **different currencies** — Promatch trades accuracy for
capacity; Micro Blossom trades silicon for exactness — and "which scales
better" has no single answer.
`../corpus/quantum-hpc-survey/corpus/QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`
lines 20–40; `../corpus/quantum-hpc-survey/corpus/data/asplos/qec_deepdive.md`.

## 4. Representative papers

- **Promatch** (ASPLOS'24) — adaptive predecoding, RTL_SYNTHESIS + ANALYTIC_MODEL,
  960 ns is a **top-down allotted budget** derived from the syndrome-cycle
  deadline, not a measurement; artifact is C++/MPI only, **no HDL** despite
  the FPGA claim.
- **Micro Blossom** (ASPLOS'25) — O(d³) parallel processing units,
  FPGA_PROTOTYPE, 0.8 µs **average** (not worst case) measured on a VMK180
  board at 62 MHz; hits a wall at d=15 (867k/900k LUTs); the only paper in
  36 that ships HDL (Scala/SpinalHDL + Rust).
- **AlphaSyndrome** (ASPLOS'26) — syndrome scheduling.
- **HetEC** (ASPLOS'25) — heterogeneous QEC architecture; introduces qLDPC
  as a first-class code family from 2025 onward (`OBSERVED_SHIFT`).

## 5. Historical lineage

Traced in `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`: AFS (HPCA'22, union-find)
→ Astrea/Astrea-G (ISCA'23, exact brute force to d=7 in 456 ns) → Clique
(ISCA'23, predecoder) → **Promatch** (ASPLOS'24) on one side; lookup tables
→ Fusion Blossom (2023) → Helios (FPGA union-find) → **Micro Blossom**
(ASPLOS'25) on the other. The two lines collide directly: Micro Blossom
cites Promatch's approach as producing "more than 13.9× higher logical
error rate" — **but this number is cited outside the parameter range its
source paper actually swept** (Promatch sweeps p = 10⁻⁴–5×10⁻⁴; Micro
Blossom cites the figure at p = 0.1% = 10⁻³). The verification pass in
`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` Appendix A calls this the
strongest finding in the census.

## 6. Implementation families

`RTL_SYNTHESIS` (Promatch), `FPGA_PROTOTYPE` (Micro Blossom), `ANALYTIC_MODEL`
(most full-machine architecture papers). See
`../implementation/ARTIFACT_REGISTRY.md` — no third-party repo was cloned
specifically for QEC decoding verification in this source project (Micro
Blossom's and Promatch's own repositories were read directly, not cloned
into the verification scratch workspace recorded there).

## 7. Important disagreements / tensions

The Promatch/Micro Blossom "maximum vs. average" latency comparison
(`DIFFERENT_METRIC`) and the T1 mis-transfer above are both documented,
tagged tensions, not resolved to a single winner — see
`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §8 for the full T1–T4 tension
table.

## 8. Current limitations

Trapped-ion timing (measurement 400 µs, gates 40 µs) is not analyzed
against either decoder design, both of which anchor to superconducting's
1 µs (`../research/CANDIDATE_QUESTIONS.md` Q1). None of the four qLDPC
papers in the corpus analyzes real-time decoder cost for BP/BP+OSD
decoding (`../research/CANDIDATE_QUESTIONS.md` C5).

## 9. Research questions

See `../research/CANDIDATE_QUESTIONS.md` entries G1, C1, C4, C5, Q1, Q2,
Q3 — all `CANDIDATE` status, none re-falsified during this import.

## 10. Deeper lookup paths

`../corpus/quantum-hpc-survey/corpus/data/asplos/qec_deepdive.md` (full
per-paper analysis) → `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §8 (tension
table) and Appendix A (verification record) → original papers/repos cited
there for implementation-level questions.

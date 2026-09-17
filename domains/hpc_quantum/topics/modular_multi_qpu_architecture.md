# Modular / multi-QPU architecture

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **MODERATE**. A named branch in the source's own
taxonomy (3 ASPLOS papers, 1 SC paper) with a short lineage treatment
inside `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`, but no dedicated deep-dive
document of its own.

## 1. Problem landscape

As single-QPU qubit counts plateau, multiple physical modules must be
interconnected (chiplets, or fully separate QPUs) — raising interconnect
bandwidth, inter-module communication cost, and multi-party protocol
questions that are structurally distributed-systems problems.

## 2. Key concepts

Chiplet interconnect; multi-party distributed primitives (e.g. a
distributed SWAP test); inter-module communication cost as a compilation
objective; natively-distributed vs. single-device framing.

## 3. Main mechanism families

- **Interconnect architecture** — MECH (ASPLOS'24): multi-entry
  communication highway for superconducting quantum chiplets.
- **Multi-party distributed primitive** — COMPAS (ASPLOS'26): a
  distributed multi-party SWAP test for parallel quantum algorithms,
  `PUBLIC_CODE`, evaluated configurations as CLI args.
- **Defect-aware codesign** — the chiplet codesign paper (ASPLOS'24):
  codesign of QEC codes and modular chiplets in the presence of defects.
- **Compilation for distributed architectures** — DQTetris (SC25):
  optimizing quantum circuit mapping to reduce inter-module communications
  in distributed architectures (compilation-only, SC's one paper in this
  branch).

## 4. Representative papers

MECH (ASPLOS'24, `PUBLIC_ARTIFACT`), COMPAS (ASPLOS'26, `PUBLIC_CODE`,
github.com/kunliu7/Distributed-Q-Algo), chiplet codesign paper (ASPLOS'24,
`PARTIAL` artifact), DQTetris (SC25, compilation only).

## 5. Historical lineage

MECH (ASPLOS'24) is read by the source as a precursor to COMPAS
(ASPLOS'26) — `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:191` — though this is
a topical/problem-space connection the source draws, not a claimed
citation lineage between the two papers.

## 6. Implementation families

COMPAS's public code exposes its evaluated configurations directly as CLI
arguments (`[code]`-level confirmation, `CONSISTENT` verdict in the census
artifact matrix).

## 7. Important disagreements / tensions

None recorded between papers in this branch specifically.

## 8. Current limitations

**Both venues are thin here** — ASPLOS 3 papers, SC 1 — recorded as a
`VENUE_GAP` in both directions
(`QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:204`). The source's own
`POSSIBLE_CROSSOVER` reading: this branch is *natively* distributed, so
scale-out requires no reframing, only more machine — see
`../research/CANDIDATE_QUESTIONS.md` entry C2, `CANDIDATE` status only.

## 9. Research questions

See `../research/CANDIDATE_QUESTIONS.md` entries G3, G9, G10, C2.

## 10. Deeper lookup paths

`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §9 (crossover analysis, modular
row) → `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md` (MECH→COMPAS lineage
paragraph) → `SC_2024_2025_QUANTUM_HPC_CENSUS.md` §4.4 (DQTetris entry).

---

## Phase-2 extension — six-venue census (2026-09-17)

Source: `../corpus/multi-venue-census-2026/QUANTUM_HPC_MULTI_VENUE_SYNTHESIS.md`
§5 Q9 and the HPCA/MICRO/ISCA censuses.

**~9 papers across the six venues** (ISCA 2, HPCA 2, MICRO 2, QSW 2, ISC 1),
which upgrades this branch from the Phase-1 "thin at both venues" reading — but
the work is narrower than the branch name suggests.

**What is actually being studied is interconnect and partitioning, not
programming models:**

- **SwitchQNet** (ISCA 2025, UCSD/Cisco) — switch-network topology for quantum
  datacenters: switch fabrics vs direct links, contention, and a compiler mapping
  circuits onto the fabric. The most literal "datacenter network topology" paper in
  the domain. `PUBLIC_ARTIFACT`.
- **Constant-Rate Entanglement Distillation** (ISCA 2025, Caltech/MIT/Harvard/
  QuEra) — link rate vs fidelity vs buffering, i.e. interconnect engineering with a
  fidelity dimension classical fabrics do not have.
- **DC-MBQC** (HPCA 2026) — adaptive graph partitioning (METIS with
  modularity-driven imbalance control) plus inter-QPU layer scheduling, proved
  NP-hard by reduction from graph bandwidth. Evaluated at **4 and 8 QPUs only**.
- **Cyclone** (HPCA 2026) — a ring QCCD topology with lockstep ancilla movement,
  removing roadblocks that serialize qLDPC syndrome extraction; reports that
  **DAC count stays constant** in the ring versus linear in trap count for grids.
- **MUSS-TI** (MICRO 2025) — multi-QCCD trapped-ion scheduling framed explicitly
  as **multi-level memory-hierarchy scheduling**, the authors' own words.
- **Distributed-HISQ** (MICRO 2025) — distributed *control-plane* synchronization
  across multiple controllers on real hardware, which is a different multi-QPU
  problem from circuit partitioning and is easy to conflate with it.

### How far the GPU-cluster analogy holds

`[inference]`, from the corpus rather than from general knowledge: **the analogy
holds well for partitioning and topology and poorly for everything else.** There
is no analogue of a collective-communication library, no analogue of an MPI-like
programming model, and the "network" carries a fidelity dimension with no classical
counterpart — DC-MBQC's objective is *required photon lifetime*, not bandwidth.
Recorded at `[inference]` level only, per the Phase-1 discipline on this analogy.

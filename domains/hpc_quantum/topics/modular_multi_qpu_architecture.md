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

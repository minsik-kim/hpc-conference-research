# multi-venue-census-2026 — ISC · ISCA · ICS · HPCA · MICRO · QSW (2024–2026)

**Phase 2 continuation of the Quantum-HPC venue census, performed 2026-09-17.**
This is a **second source project** inside `domains/hpc_quantum/corpus/`, alongside the imported
`quantum-hpc-survey/` (SC 2024–2025 and ASPLOS 2024–2026, plus the Phase-1 21-venue landscape map).
It is new research output, not an import — which is why it is a separate project directory rather
than an edit to the byte-identically preserved Phase-1 source.

## What is here

| File | What it is |
|---|---|
| `METHODOLOGY.md` | Enumeration method, completeness proofs, inclusion/exclusion rules, evidence discipline, tooling constraints. **Read first.** |
| `CENSUS_ISC_2024_2026.md` | 13 relevant of 87 regular research papers |
| `CENSUS_ISCA_2024_2026.md` | 33 relevant of 375 |
| `CENSUS_ICS_2024_2026.md` | 8 relevant of 230 |
| `CENSUS_HPCA_2024_2026.md` | 17 relevant of 306 |
| `CENSUS_MICRO_2024_2026.md` | 11 relevant of 236; **MICRO-59 `PROGRAM_INCOMPLETE_AS_OF_2026-09-17`** |
| `CENSUS_QSW_2024_2026.md` | 20 relevant of 47 confident regular papers |
| `QUANTUM_HPC_MULTI_VENUE_SYNTHESIS.md` | Cross-venue synthesis: bottom-up taxonomy, branch × venue matrix including SC/ASPLOS, venue contribution shapes, the thirteen questions, crossover analysis, NISQ→FTQC, temporal trend, open questions, next venues |
| `DEEPDIVE_QEC_DECODING.md` | Paper↔code cross-validation of 8 QEC decoder papers (4 repos cloned and read); latency-budget table, decoder-family map, parallelism/crossover analysis, cross-paper contradictions |
| `DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` | Paper↔code cross-validation of 15 simulation, scheduler/runtime and compiler papers (9 repos cloned); simulation bottleneck table, compile-cost-vs-quality split, scheduler resource-model comparison |
| `CORRECTIONS_TO_PHASE1.md` | **Authoritative wherever this census and the Phase-1 documents disagree.** Corrected counts, characterizations and quantitative claims; confirmed Phase-1 findings; new venue-level facts |
| `VERIFICATION_PASS.md` | Independent adversarial audit of this census and what it changed |

## Headline numbers

**1,281 regular research papers screened across 18 venue-years; 102 Quantum-HPC relevant (7.96%).**

| Venue | 2024 | 2025 | 2026 | Total relevant |
|---|---:|---:|---:|---:|
| ISC High Performance | 6 / 24 | 3 / 28 | 4 / 35 | 13 |
| ISCA | 6 / 83 | 16 / 131 | 11 / 161 | 33 |
| ICS | 1 / 45 | 2 / 83 | 5 / 102 | 8 |
| HPCA | 1 / 75 | 7 / 113 | 9 / ~118 | 17 |
| MICRO | 3 / 113 | 8 / 123 | unknown | 11 |
| IEEE QSW | 6 / 13 | 5 / 17 | 9 / 17 | 20 |

## What this census changed

Four counts corrected (**ICS 2024: 0 → 1**, ISC 2024: 5 → 6, HPCA 2026: 8 → 9, ISCA 2026: 12 → 11),
one paper re-characterized after reading its code (**Flag-Proxy Networks is not decoding hardware**),
three attributions fixed, and ten quantitative claims restored to their measurement context. Nineteen
relevant papers were found that the Phase-1 seed list did not name — **two of which have no quantum
vocabulary in their titles at all** and were reachable only by hand-scanning every title in the
enumerated volumes. Full list: `CORRECTIONS_TO_PHASE1.md`.

## Scope limits

`COMPLETE_AS_CURRENT_SOURCE` for the venue-years whose denominators are `TOTAL_COUNT_VERIFIED`
(ISC 2024, ISCA 2024 and 2026, all three ICS years, HPCA 2024 and 2025, MICRO 2024 and 2025, QSW 2024
and 2025 at volume level). **Not** `COMPREHENSIVE_FIELD_COVERAGE`, and not uniformly verified — Known-incomplete: MICRO-59 unpublished; HPCA 2026's denominator
`TOTAL_COUNT_UNVERIFIED` (≥118, per-article pagination defeats page tiling, mirror incomplete by ≥2);
ISCA 2025's research-track subtotal carries a ±1 ambiguity; QSW's regular/short split is unresolvable
in the 7-page boundary band for 2024–2025, and QSW 2026 has no publisher TOC. Absence of a topic here
is `NOT_COVERED`, never evidence that it is unstudied.

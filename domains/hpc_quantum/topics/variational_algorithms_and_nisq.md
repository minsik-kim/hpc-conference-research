# Variational algorithms (VQE), NISQ mitigation, and quantum chemistry — coverage note

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

**Coverage status: PARTIAL_IN_SOURCE.** Read this section before anything
else in this file: **the current HPC-Quantum corpus contains VQE-related
work as part of the systems landscape, but it is not a comprehensive VQE
literature review.** VQE, ansatz, UCC/UCCSD, ADAPT-VQE, and measurement
reduction each appear only as **incidental mentions inside individual
paper analyses** — a benchmark description, a related-work sentence — not
as a researched topic with its own mechanism families, lineage, or
open-question analysis. Do not answer a substantive VQE-methods question
(warm-start, initialization landscape, barren plateaus, gradient
estimation, classical optimizer comparison) from this file or from this
corpus at all — those are `NOT_COVERED` (see `TOPIC_MAP.md` §2). The
user's own active CCSD→UCCSD warm-start research project
(`hpc-quantum-warmstart-paper`, on their own machine) is explicitly **not**
part of this corpus and was not read into it — see
`DOMAIN_CONTEXT.md` and `../corpus/quantum-hpc-survey/SOURCE_MANIFEST.md`
§7.

## 1. Problem landscape

As it appears in this corpus: VQE-family algorithms (variational circuits,
NISQ-era mitigation) are census subjects — papers classified by the two
venue censuses as belonging to the `NISQ` maturity tag and a variational/
mitigation branch — not the object of a dedicated methods survey.

## 2. Key concepts (as used in this corpus, not as a general VQE primer)

- **ansatz** — 6 occurrences, taxonomy/description only.
- **UCC/UCCSD** — 5 occurrences; 4 of the 5 are inside one paper's
  benchmark description: ground-state estimation for molecules (H₂, LiH,
  BeH₂, HF, C₂H₂), spin chains (XXZ, transverse Ising), and MaxCut, under
  SPSA/COBYLA with UCCSD ansätze (`arch_sim_deepdive.md:554,578`).
- **ADAPT-VQE** — exactly 1 mention, listed as a competing technique that
  "truncates terms but adds circuit depth" inside one paper's related work
  (`arch_sim_deepdive.md:544`).
- **measurement reduction / commuting-group tiling** — exactly 1 mention,
  same related-work passage, describing it as adding "complex grouping
  heuristics or increased circuit depth" (`arch_sim_deepdive.md:545`).

## 3. Main mechanism families — as census subjects, not methods

TreeVQA (ASPLOS'26, shot-reduction execution framework), Clapton
(ASPLOS'25, NISQ mitigation, bibliographically 29V4/proceedings-2024,
deferred to presentation in 2025), VarSaw (ASPLOS'24, NISQ
mitigation, proceedings year 2023), Red-QAOA (ASPLOS'24, variational
optimization through circuit reduction), Elivagar (ASPLOS'24, efficient
quantum circuit search for classification), QuFEM (ASPLOS'24, readout
calibration), ProxiML (ASPLOS'24, photonic QML).

## 4. Representative papers

See §3 — these are the corpus's variational/NISQ-tagged papers, analyzed
as venue-census entries (acceptance rationale, artifact status, evidence
grading), not as a survey of variational-algorithm technique.

## 5. Historical lineage

Not established in the source for this topic — no lineage document treats
variational algorithms the way `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`
treats QEC decoding or simulation.

## 6. Implementation families

Elivagar, Red-QAOA, QuFEM are `PUBLIC_CODE`; Clapton, VarSaw are analyzed
primarily from preprints (`[paper-preprint]`).

## 7. Important disagreements / tensions

None recorded specific to this topic.

## 8. What is explicitly excluded from this corpus — quantum chemistry

**Classical quantum chemistry / many-body physics / quantum transport /
neural-network quantum states is documented as the corpus's dominant
false-positive class** — papers titled with quantum-sounding language that
are, on inspection, classical HPC work wearing that title, and are
excluded from both censuses. Examples the source records explicitly:
"Breaking the Million-Electron and 1 EFLOP/s Barriers" (ab initio
molecular dynamics via MP2 potentials) and "Enabling 13K-Atom
Excited-State GW Calculations" — both excluded as classical chemistry, not
counted toward either census's quantum population
(`SC_2024_2025_QUANTUM_HPC_CENSUS.md` Appendix A.1, `QUANTUM_HPC_VENUE_MAP.md`,
`QUANTUM_HPC_RESEARCH_QUEUE.md`). **This means quantum chemistry is
present in this corpus only as an exclusion criterion, never as surveyed
content** — do not answer a quantum-chemistry-workload question from this
corpus.

## 9. Research questions

None indexed for this topic in `../research/CANDIDATE_QUESTIONS.md` — the
source corpus never attempted a VQE-methods gap analysis (see
`../research/CANDIDATE_QUESTIONS.md` §4).

## 10. Deeper lookup paths

For the papers named in §3: their entries in
`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §3–5 and
`../corpus/quantum-hpc-survey/corpus/data/asplos/arch_sim_deepdive.md`. For
VQE methods themselves (initialization, barren plateaus, gradient
estimation): **not in this repository** — this is a `NOT_IN_REPOSITORY`
question, per `governance/ANTI_HALLUCINATION_RULES.md`, not one this file
can route further.

---

## Phase-2 note — six-venue census (2026-09-17)

**Coverage status is unchanged: `PARTIAL_IN_SOURCE`.** The six-venue census
(ISC, ISCA, ICS, HPCA, MICRO, QSW 2024–2026) is a systems/venue census like the
Phase-1 corpus, and it did **not** survey VQE methods either. It adds a handful of
variational papers *as census subjects*, not a literature review:

- **Variational Quantum Algorithms in the era of Early Fault Tolerance**
  (ISCA 2025, UChicago) — the corpus's one paper that explicitly **re-costs the
  VQA workload class across the NISQ→early-FT transition**: under early fault
  tolerance the cost model inverts, and shot budgets, optimizer iterations and the
  classical/quantum work split all have to be re-derived. This is the closest thing
  in the domain to a VQE-methods contribution, and it is a *cost-model* paper.
- **Choco-Q** (HPCA 2025) and its successor **Rasengan** (MICRO 2025) — constrained
  binary optimization via commute and transition Hamiltonians, with circuit-
  complexity reduction as the systems contribution.
- **Qoncord** (MICRO 2024) and **MILQ** (ISC 2024) — VQA/QAOA *scheduling* across
  device fleets; the variational algorithm is the workload, not the subject.
- **Hierarchical Multigrid Ansatz for VQAs** (ISC 2024, NMSU/LANL) — an ansatz
  built from the classical multigrid V-cycle, accepted at an HPC venue because the
  contribution is framed in classical numerical-methods vocabulary.
- **Tetris** (ISCA 2024) — a Pauli-string IR and synthesis passes for VQA circuits.

**What remains `NOT_COVERED` is unchanged**: classical-optimizer studies,
initialization/warm-start methods, barren plateaus and trainability, gradient
estimation, excited-state methods. The six-venue census contains **no** paper on
any of them, which is expected — these are algorithm-methods topics and none of
the six venues publishes them. That absence is `NOT_COVERED`, **not** a
`VENUE_GAP` candidate and **not** evidence that the wider literature is thin
(`governance/ANTI_HALLUCINATION_RULES.md`).

The user's separate `hpc-quantum-warmstart-paper` project was **not** read,
referenced or merged during this census either.

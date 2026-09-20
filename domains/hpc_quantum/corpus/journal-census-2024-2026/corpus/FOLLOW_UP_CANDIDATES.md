# FOLLOW_UP_CANDIDATES — Quantum-HPC Journal Census 2024–2026

Items found during the census that are **out of this task's scope** and are recorded here rather than
acted on. Nothing in this file is a finding, and nothing here authorises widening the census.

**Stop condition observed.** This census covered the eight commissioned journals × 2024–2026 and
nothing else. No additional journal was censused. *Quantum*, *PRX Quantum*, *npj Quantum Information*
and *Quantum Science and Technology* were not touched. No quantum-algorithm landscape was built.
External papers were consulted only to verify a specific fact about an in-scope record.

---

## 1. Evidence gaps that should be closed before the corpus is used for anything load-bearing

| # | Item | Why it matters | Status |
|---|---|---|---|
| F1 | **Artifact status for 68 of 89 included papers is `UNKNOWN`** (= not checked). IEEE Xplore, ACM DL badge pages and Elsevier full text were unreachable from the research environment. | The paper-to-code chain cannot be closed. Any artifact-rate comparison with the SC (64%) or ASPLOS (61%) figures in the conference corpus would be invalid today. | `INSUFFICIENT_EVIDENCE` |
| F2 | **Zero `CONFIRMED_EXTENSION` conference-lineage records.** Publisher front matter, where "an earlier version appeared at …" is printed, could not be read. | Until this is closed the 89 journal papers and the 47 censused conference papers **must not be summed** into one count of independent contributions. | `INSUFFICIENT_EVIDENCE` |
| F3 | **Three TCAD Early Access records unresolved** — `10.1109/tcad.2026.3656760`, `10.1109/tcad.2026.3663259`, `10.1109/tcad.2026.3677771` and related (see `TCAD_records.json`, field `what_would_resolve_it`). No abstract retrievable. | TCAD's 2026 count (1 included) is demonstrably depressed by this, so the apparent 2026 fall at TCAD is not yet a real observation. | `INSUFFICIENT_EVIDENCE` |
| F4 | **`qfusion-opt`** `10.1109/tcad.2026.3680784` — profile-informed gate scheduling and fusion for quantum circuit simulation. Title evidence only. | On its title it is a strong deep-dive candidate; it cannot be classified on the mechanism without full text. | `INSUFFICIENT_EVIDENCE` |
| F5 | **TQE census years rest on the volume cover year** (`YEAR_BASIS=ISSUE`). IEEE Early Access dates were not obtainable for TQE. | TQE's 7/12/6 per-year split is less reliable than the other journals'. One record (`10.1109/tqe.2023.3347106`) was provably outside the window on this basis; others may be. | `INSUFFICIENT_EVIDENCE` |
| F6 | **The secondary vocabulary sweep did not complete** (OpenAlex account budget rate limit) for the narrow terms `statevector`, `tensor network`, `circuit cutting`, `surface code`, `qLDPC`, `decoder`, `syndrome`, `FTQC`, `transpiler`, `QAOA`, `VQE`, `NISQ`, `stabilizer`, `ansatz`. | Recall rests on the primary 21-term title regex plus the OpenAlex title-and-abstract search. No missed record was found in the portion that ran. | open |
| F7 | **Truncated quantitative claims.** Several records carry a performance claim whose figures were cut by 700-character abstract truncation — AdaptDQC, Effective and Efficient Parallel Qubit Mapper, the TPDS communication-partition paper. | Restore from full text before quoting any of them. | open |
| F8 | **FGCS Special Collection Vol I** (`10.1016/j.future.2024.107503`, v163) — editorial body not retrievable; its scope, paper count and membership are unknown. Vol II (15 papers) and Vol III (24 papers) were reconstructed. | The collection is the mechanism behind FGCS's steady yield; one third of it is unmapped. | `INSUFFICIENT_EVIDENCE` |

---

## 2. Method notes for any repeat of this census

| # | Note |
|---|---|
| M1 | **Sweep Elsevier on online-first date, not volume cover date.** FGCS cover dates run ~6 months ahead. A sweep bounded at cover-date 2026-12-31 silently dropped every article first available after 2026-07-17, including an EXISTENCE_CHECK_SEED paper. Extend the window to cover-date +1 year and filter back on first-availability. |
| M2 | **Negate the PQC vocabulary** in any automated query: `post-quantum`, `quantum-resistant`, `lattice-based`, `Kyber`, `Dilithium`, `NTT`, `SPHINCS`, `HQC`, `ML-KEM`, `ML-DSA`, `FALCON`. 44 exclusions, concentrated in TC (12) and TCAD (11). |
| M3 | **Inside quantum-native journals, `distributed`, `node` and `scalable` are misleading** — at TQE they overwhelmingly mean entanglement distribution and qubit-count scalability. Screen on the classical-cost-quantity question instead. |
| M4 | **`tensor network` / `tensor train` collides with classical low-rank numerics.** `10.1016/j.future.2026.108709` is the cleanest example: a genuine TPU/GPU/CPU benchmarking paper with no quantum computer in it. |
| M5 | **Best-precision terms** for a future automated query: `compiler`/`transpilation` (83%), `HPC`/`cloud`/`serverless` (75%), `decoder`/`syndrome` (64%), `statevector`/`decision diagram`/`circuit simulation`. |
| M6 | **Seed-anchoring is a live risk.** All 23 pre-scan seed titles present in the corpus were INCLUDED — 100% against a 17% corpus-wide rate. That is expected but should be re-tested by whoever runs the next census, ideally by screening blind to the seed list. |

---

## 3. Branches and threads observed but not pursued (`FOLLOW_UP_CANDIDATE` only)

| # | Thread | Where it appeared | Why not pursued here |
|---|---|---|---|
| B1 | **Cryogenic classical computing as a systems discipline** — in-cryostat coprocessors, SFQ/RSFQ logic, cryo-CMOS control, thermal budgets at 4 K and mK. | TQE (C3-VQA, RSFQ multitone generator, cryo-CMOS bias generation), TC (Cryo-CACTI), TCAD (AQFP/RQFP EDA). | Mostly device/EDA, which the gates exclude. But C3-VQA shows a systems-shaped subset exists, sitting next to a large excluded population. A targeted, tightly scoped pass would be needed, not a census. |
| B2 | **Quantum serverless / FaaS as a resource-management model.** | FGCS (QFaaS), TQE (hybrid classical–quantum serverless platform modelling), JPDC (quantum serverless survey — the journal's only inclusion), TQC. | Cuts across four journals and is the one thread where JPDC has anything. Coherent enough to be its own branch map. |
| B3 | **Multiprogramming / QPU utilisation as the objective function.** | TACO (all four inclusions), FGCS (MPGP-QOC), TQE (CircPack trapped-ion packing and scheduling). | The frame closest to an HPC centre's own concerns, and it is scattered across journals rather than owned by one. |
| B4 | **Quantum-inspired classical methods as a legitimate HPC topic in their own right.** | 51 exclusions across all eight journals, several of them real parallel-computing papers. | Correctly out of scope for a *quantum computing* interface census. Recorded because the excluded set is large enough to be a literature in itself, and because misreading it as quantum computing is this corpus's second-largest false-positive risk. |
| B5 | **Ising-machine hardware as a QPU-adjacent accelerator.** | TC (SLAM), TCAD (parallel-tempering architecture, Ising placer, coherent optical Ising machine for qubit mapping), TQE (distributed Ising-machine solvers). | Excluded or BORDERLINE by class 2, uniformly. The boundary case worth noting is TCAD `10.1109/tcad.2025.3572021`, where an Ising machine is used to solve the *qubit mapping* problem — an accelerator serving quantum compilation. Recorded BORDERLINE. |
| B6 | **Quantum software engineering** — testing, debugging, property-based testing, program verification. | TQE (testing and debugging quantum circuits, dynamic testing strategy), TQC (QuCheck, model-driven circuit design). | Out of scope under Gate 2 as applied. Present enough across two journals to be a named branch if the scope is ever widened. |

---

## 4. Time-sensitive items

| Date | Item | Action |
|---|---|---|
| continuing | **FGCS volumes 186–187 (cover date 2027-01)** are already publishing 2026 work. | The next census pass must start from FGCS v186, not from a 2027 cover-date boundary. |
| continuing | **IEEE TCAD and TC Early Access queues** carry several quantum records with no abstract yet. | Re-check the three `INSUFFICIENT_EVIDENCE` TCAD records once they reach an issue. |
| Q4 2026 | **FGCS Special Collection Vol III** (24 papers) is still filling. | Ten of its titles were recovered; the rest should be mapped when the volume closes. |
| open | **ACM TQC "Just Accepted" queue** — 11 records with no volume at census time. | These will acquire volume/issue metadata; the DOI is stable, so no double counting will result. |

---

## 5. What this census does **not** license

- It does not license a claim that any topic is unexplored, unaddressed, or a research gap. Every
  observation is `JOURNAL_GAP`, `UNDERREPRESENTED_IN_THIS_CORPUS`, `POSSIBLE_CROSSOVER`,
  `OPEN_QUESTION` or `INSUFFICIENT_EVIDENCE`, and each is `CANDIDATE` status only.
- It does not license extending the venue map's evidence strength. The conference-side counts in
  `QUANTUM_HPC_VENUE_MAP.md` were **not** revised, re-derived or upgraded by this work.
- It does not license summing journal and conference populations (see F2).
- It does not license a census of any journal outside the commissioned eight.

# VERIFICATION CHANGELOG — adversarial audit of the 559-record Quantum-HPC journal census

Auditor: independent verification pass. Date: 2026-09-17.
Machine-readable companion: `verification_corrections.json`.

## Method note

**What was checked.** All 559 records in `data/all_records.json` were re-read programmatically against
`data/pool3.json` (the harvested metadata), the eight dossiers, and the eight per-journal JSON files in
`out/`. The per-journal JSONs, not the merged file, were treated as the source of truth for verdicts and
justifications, because the merge is lossy (see check 6). Every DOI was tested for duplication, every
census year was tested against the recorded online and issue dates, every included record's article type
and gate reasoning was re-read, and every non-empty artifact URL was fetched.

**External verification.** OpenAlex single-work records, the Crossref works and journal endpoints,
arXiv abstract pages, GitHub repository pages and one ScienceDirect article page were used. All six real
artifact repositories were fetched. Census years were externally confirmed for FGCS-001, TQE-007,
TCAD-057, TQE-163, FGCS-058 and FGCS-055/064/039.

**What could not be checked, and why.**
- Direct `curl` to `api.crossref.org` and `api.openalex.org` is refused by the environment's egress policy
  (HTTP 403 on CONNECT); only the WebFetch path works, and both APIs rate-limited list queries (HTTP 429)
  after a few calls. OpenAlex list queries never succeeded. Per-record Early Access dates for the
  15 IEEE records whose DOI year precedes their assigned census year were therefore confirmed for two
  representatives only; the rest rest on the IEEE DOI-year signal and are marked INSUFFICIENT_EVIDENCE.
- Full texts were not read. Gate re-application is therefore against abstracts, recorded gate text and
  recorded claims, which is the same evidence the original pass had.
- Recall of the TC, TCAD, TACO and JPDC candidate pools could not be independently established. Crossref's
  `query.bibliographic` is relevance-ranked and demonstrably incomplete (it misses `10.1145/3631525`,
  a TACO record with "Quantum" in its title), so a negative result there proves nothing.
- Institutions, funding and full-text artifact statements were out of reach throughout.

**Forbidden vocabulary.** This document avoids the terms banned by `CRITERIA.md`.

---

## Check 1 — DOI duplicates

**No discrepancy found.** All 559 DOIs are distinct after case normalisation, within and across journals,
and none is empty. Exact-title and token-Jaccard (>0.7) near-duplicate scans returned nothing.

## Check 2 — Early-access / final-issue double counting

**No discrepancy found.** 35 records carry no volume (IEEE Early Access or ACM Just Accepted). None of
them has an issue-version counterpart elsewhere in the corpus: each maps to a unique DOI, and no DOI,
title or near-title pair spans an Early Access record and a volume record.

## Check 3 — Census-year accuracy

Two separate tests were run.

**(a) Internal consistency (all 559 records).** Where `pool3.json` carries an online date, the assigned
`census_year` equals that date's year in 559/559 cases. 119 records have an online year differing from
their issue year, and in every one of those the census year follows the online year, which is the stated
convention. **No internal discrepancy found.**

**(b) External test of the 37 records with no online date, plus every record whose DOI year precedes its
census year (15 records).** This is where the errors are. Confirmed externally:

| Record | DOI | Recorded | Confirmed first availability | Source |
|---|---|---|---|---|
| FGCS-001 | 10.1016/j.future.2023.12.002 | 2024 | **2023-12-04** | OpenAlex + Crossref `created` |
| TQE-007 | 10.1109/tqe.2023.3347106 | 2024 | **2023-12-26** | OpenAlex `publication_date` |
| TCAD-057 | 10.1109/tcad.2025.3626447 | 2026 | **2025-10-28** | OpenAlex `publication_date` |
| FGCS-058 | 10.1016/j.future.2025.108095 | 2026 | **2025-08-22** | OpenAlex `publication_date` |

FGCS-001 and TQE-007 are **INCLUDED records that fall outside the 2024–2026 window entirely**. TCAD-057
is an INCLUDED record in the wrong year. FGCS-058 is BORDERLINE.

One DOI-year signal was tested and found to be a false alarm: TQE-163 (`10.1109/tqe.2025.3649617`) has
Crossref `created` 2026-01-12, so its 2026 census year is correct. IEEE occasionally reserves a DOI in the
prior year, which is why the remaining DOI-year cases below are recorded as probable rather than confirmed.

Probable but unconfirmed (all EXCLUDED or BORDERLINE, so headline INCLUDED counts are unaffected):
TQE-001 to TQE-006 and TQE-008 (DOI year 2023, assigned 2024); TCAD-001 to TCAD-008 (DOI year 2023,
assigned 2024); TC-001 (**DOI year 2021**, assigned 2024); TC-002 (2023); TC-032 and TCAD-056 (2025,
assigned 2026); TQE-077 (2024, assigned 2025); FGCS-027 and FGCS-028 (2024, assigned 2025).

**Systematic finding.** The TQE sub-census did not apply the first-availability rule at all. 206 of its 246
records carry a placeholder online date of `YYYY-01-01` in `pool3.json`, and `TQE_census.md` states the
convention used was "volume 5 = 2024, volume 6 = 2025, volume 7 = 2026". Every TQE census year is therefore
a volume cover year. For TQE this is usually right, but it is provably wrong for at least eight records and
cannot be relied on for the rest. Ten TCAD records carry the same `2026-01-01` placeholder, but there the
DOI year agrees with the assigned year, so no error follows.

## Check 4 — Article-type misclassification

**No misclassification found.** Every title matching review/survey/perspective/editorial/overview/
lessons/roadmap vocabulary was re-read. All 25 hits carry the right type. Six INCLUDED records are not
ORIGINAL_RESEARCH (FGCS-010 and FGCS-066 PERSPECTIVE, JPDC-007, TQC-048 and TQC-057 REVIEW_SURVEY,
TQC-035 SPECIAL_ISSUE_INTRO), and all six are excluded from the original-research counts in their own
journal summaries and headline tables, which is what `CRITERIA.md` requires. The arithmetic was
re-verified: TQC 27 INCLUDED minus 3 non-original = 24, and the per-year row 8/6/10 sums to 24; JPDC
1 INCLUDED, 0 original research; FGCS 21 INCLUDED, 19 original research.

TQC-035 is separately challenged on gate grounds in check 6, not on article type.

## Check 4b — Erratum / corrigendum / front matter

**No discrepancy found.** One such record exists in the whole corpus: FGCS-060, "Corrigendum to
'Solving combinatorial optimization and machine learning problems on hybrid near-term quantum
processors'" (`10.1016/j.future.2026.108408`), typed OTHER and EXCLUDED. No index or front-matter record
survived into the pools (the per-journal notes state these were removed upstream), and no erratum-type
record is INCLUDED anywhere.

## Check 5 — Is it actually quantum computing?

The INCLUDED set was regex-swept for each named false-positive class over title, abstract, gate text and
claim.

- **Post-quantum cryptography: none.** Zero hits for Kyber/Dilithium/lattice/NTT/SPHINCS/ML-KEM/ML-DSA.
- **Classical quantum chemistry: none.** Zero hits for DFT, NNQS, QMCPACK, CP2K, plane-wave.
- **Quantum sensing / device physics / single-flux-quantum: none.**
- **QKD / quantum networking: none by vocabulary.** One record, TQE-163, is an optically networked
  trapped-ion architecture whose objective is remote entanglement rate; it is challenged in check 6.
- **QML application: one.** FGCS-039 (MPGP-QOC) is a QNN inference framework. Its contribution is
  multi-programming, graph partitioning and compilation cost, so the classification is defensible, but it
  sits on the class-5 boundary and should be read as such.
- **Quantum-inspired / Ising / annealing / QUBO: six.** FGCS-079, TQC-022, TQC-059, TQC-077, TCAD-033,
  TCAD-038. Of these, **TCAD-038 is the clearest class-2 case**: its accelerator is a coherent optical
  Ising machine solving a QUBO. **TQC-059 (CHARME, minor embedding for a quantum annealer) is the clearest
  consistency failure**: FGCS-063, the same minor-embedding problem in the same window, is BORDERLINE.
  TQC-077 (quadratisation) is QUBO problem preparation. FGCS-079 uses a D-Wave hybrid solver as a black
  box but its own contribution is a classical decomposition and deadline-distribution algorithm, so it
  survives. TCAD-033 formulates DQC partitioning as a QUBO solved classically; that is a formulation
  choice, not an Ising-machine paper.

Demotions are proposed in check 7.

## Check 6 — HPC/systems relevance, three gates re-applied adversarially

**A documentation defect, stated up front because it limits this check.**

1. `data/all_records.json` carries `gate1`/`gate2`/`gate3` for **29 of 559 records — FGCS only**. The
   per-journal files store the same content under different names (TCAD: `gate1_classical_systems_problem`;
   TQC and TACO: `classical_systems_problem` / `hpc_technique` / `heterogeneous_relevance`; TC, TPDS and
   JPDC: only in the markdown). The merge kept one spelling and dropped the rest. Anyone reading the
   merged file sees 75 of 104 INCLUDED records with null gate reasoning. **MATERIAL.**
2. **TQE records no gate justification anywhere.** `TQE_records.json` has no gate fields and
   `TQE_census.md` substitutes the sentence "Every entry passed all three gates" plus analysis prose.
   28 INCLUDED records — 27% of the included set — therefore have no auditable gate reasoning at all.
   **MATERIAL.**
3. TC, TPDS and JPDC JSON records also lack gate fields although their markdown has them. MINOR.

**Gate text quality where it exists.** The FGCS, TQC, TACO, TCAD, TC, TPDS and JPDC gate justifications
are, in the large majority, substantive: they name a concrete classical mechanism (Hungarian-algorithm
core assignment, GEMM-on-tensor-cores contraction, cache-blocking, FPGA datapath plus SATA hierarchy,
multi-versioning with runtime dispatch, work-stealing branch-and-bound). Several records volunteer their
own weakness in a `notes` field, for example TC-004 ("Included on the compilation-cost limb of Gate 1;
the fidelity/gate-count limb alone would have been BORDERLINE"). That is good practice and it is recorded.

**Records that pass on Gate 1 framing, on an analogy, or on a fidelity objective.** Twelve proposed
demotions, listed in check 7.

**Records whose gate text restates the abstract.** TC-040 ("FPGA hardware emulator as an alternative
execution substrate") and TC-041 ("FPGA emulator architecture for QAOA-based weighted MaxCut") are
one-line gate justifications with no classical quantity named. TC-041 was classified on the title alone
(`TITLE_ONLY_NO_ABSTRACT`). This audit located its preprint, arXiv:2502.11316, whose abstract reports an
O(N^2) to O(N) complexity reduction, roughly 3x more qubits on mid-tier FPGAs than comparable designs,
and 1.53x to 852x energy savings against software QAOA on embedded processors. **The INCLUDED verdict for
TC-041 is confirmed on evidence**; the record should be updated to carry that arXiv id and abstract rather
than resting on its title. TCAD-062 (`qfusion-opt`) remains title-only and unresolved.

## Check 7 — Proposed removals from the included set

Two records leave the census outright on the window rule, not on the gates:

| Record | Reason |
|---|---|
| **FGCS-001** | First public availability 2023-12-04, outside the window. |
| **TQE-007** | IEEE Early Access 2023-12-26, outside the window. |

Twelve proposed demotions to BORDERLINE, ordered by strength of case. These are proposals; the audit does not apply
them to the headline counts.

| Record | Title | Reason |
|---|---|---|
| TQC-035 | What Quantum Can Learn from Classical Computer Engineering | Its own Gate 2 text reads "Editorial framing rather than a technique" — a stated Gate 2 failure. Keep BIBLIOGRAPHY_HUB. |
| TCAD-038 | Special-Purpose Coherent Optical Quantum Computers Empower Qubit Mapping | The accelerator is a coherent optical Ising machine solving a QUBO: false-positive class 2. |
| TCAD-025 | CAMEL: Crosstalk-Aware Mapping and Gate Scheduling | Recorded claim is reduced crosstalk and decoherence, i.e. a fidelity objective. The TCAD agent's own stated rule sends fidelity-objective mapping to BORDERLINE. |
| TC-031 | QuanGuard: fingerprinting for fraud detection | The contribution is device fingerprinting; the recorded metric is identification accuracy. Gate 1 describes cloud allocation as context, not as a quantity the paper improves. |
| TQC-066 | qSIEVE: qLDPC memory via systolic movement | Objective is qubit overhead at a given logical error rate; Gate 2 rests on an analogy to systolic dataflow. |
| TQE-163 | Multiplexed Bilayered FT-QC over optically networked ion modules | Objective is remote entanglement rate against the RHG threshold: classes 4 and 6. No gate text exists to test. |
| TQC-059 | CHARME: minor embedding | Quantum-annealer embedding. FGCS-063, the same problem in the same window, is BORDERLINE. |
| TQC-022 | Optimization Applications as Quantum Performance Benchmarks | The record states its comparisons are across devices, not against a classical solver baseline. |
| TQC-077 | It's Quick to be Square: Fast Quadratisation | QUBO problem preparation; runtime advantage recorded with no figures and a generic comparator. |
| TQC-016 | Standard Cell Approach for Quantum Circuit Design | Gate 2 is a VLSI analogy; the layout speed-up is BASELINE_UNCLEAR; the record's own priority is LOW. |
| TQE-108 | Memory-Optimized Cubic Splines | Control-electronics waveform memory, adjacent to class 6. |
| TQE-034 | Scalable Full-Stack Benchmarks | The classical content is the avoidance of classical simulation, not a classical systems mechanism. |

If all twelve were accepted, the corrected INCLUDED total would fall from 102 to 90 (original research
96 to 85).

## Check 8 — Conference-extension lineage

**There are no CONFIRMED_EXTENSION claims anywhere in the corpus** — 179 records carry a lineage value and
all are UNKNOWN (170) or RELATED_LINEAGE (9). Nothing needs downgrading from CONFIRMED_EXTENSION.

Of the nine RELATED_LINEAGE records, TQC-022, TQC-094, TACO-001 and TACO-007 carry written evidence, and
two of those explain why they stop short of CONFIRMED_EXTENSION. **Seven carry no evidence at all**:
FGCS-002, FGCS-057, FGCS-073, TC-027, TC-040, TCAD-010, TCAD-066. `CRITERIA.md` requires a named related
prior paper or shared system name for RELATED_LINEAGE, so these should either state their evidence or
fall back to UNKNOWN. MINOR.

## Check 9 — Quantitative claims in the highest-priority included papers

Every numeric token in `major_claim`, `key_claim_with_baseline`, `performance_claim_and_baseline` and
`performance_metrics` was extracted for all 104 INCLUDED records and compared with the dossier abstract.
Nineteen records carry numbers; in seventeen of them the numbers are absent from the 700-character
dossier capture, so each was treated as requiring external confirmation.

**No bare speedup without a baseline was found.** Every numeric claim in the corpus names a comparator or
is explicitly tagged `BASELINE_UNCLEAR`. Two records go further and warn the reader about their own
comparator: FGCS-073 notes that its 16.6-fold figure spans two machines and two software generations, and
TQC-051 marks its 606x figure BASELINE_UNCLEAR.

**No invented number was found.** Four were confirmed against primary sources:

| Record | Recorded | Verified |
|---|---|---|
| FGCS-055 (LuGo) | 50.68x circuit-generation time, >31x gates and depth, baseline standard QPE | arXiv:2503.15439 abstract states exactly these figures against a standard QPE implementation |
| FGCS-064 (HiMA) | 4.89x speedup, 3.55x CLOPS | ScienceDirect abstract states both. The preprint (arXiv:2408.11311) states only 4.89x and a 72-qubit processor; the journal version says 102 qubits and adds 3.55x, so the record follows the journal version correctly |
| FGCS-039 (MPGP-QOC) | 10.1x average, up to 10.4x, up to 6.5x compilation reduction | ScienceDirect abstract states exactly these figures |
| FGCS-073 (JUQCS-50) | 16.6-fold | present verbatim in the dossier abstract |

The remaining numbers (FGCS-033 1.79x/22%, FGCS-057 87%/74%, FGCS-079 17.5%, FGCS-080 45.7%/64%,
TQE-062, TQE-075, TQE-142, TQE-150, TQC-009, TQC-030, TQC-051, TQC-074, TQC-094, TACO-009, TCAD-010) could
not be re-checked within the available request budget and are listed under residual uncertainty. Nothing
in the four verified cases suggests fabrication; the pattern is careful retrieval that was not written
back into the record's evidence trail.

**One process defect.** The records that carry retrieved numbers still show `NO_ABSTRACT` / dossier-only
evidence and record no retrieval source. FGCS-055 and FGCS-064 also show an empty `arxiv` field even
though both have preprints. The numbers are right; the provenance is not recorded.

## Check 10 — Artifact URLs

Sixteen records carry a non-empty `artifact_url`. Six are real repositories; **all six resolve and belong
to their paper**:

| Record | URL | Result |
|---|---|---|
| FGCS-002 | github.com/Cloudslab/qfaas | Resolves. "A Serverless Function-as-a-Service framework for Quantum computing". Correct. |
| FGCS-057 | github.com/Guillaume-Helbecque/P3D-DFS | Resolves. Chapel branch-and-bound skeletons; its publication list names the FGCS qubit-allocation paper. Correct. |
| TQC-019 | github.com/cda-tum/mqt-predictor | Resolves **by redirect** to munich-quantum-toolkit/predictor. Content correct; the URL should be updated. |
| TQC-022 | github.com/SRI-International/QC-App-Oriented-Benchmarks | Resolves. Application-oriented QC benchmark suite. Correct for a PARTIAL status. |
| TQC-029 | github.com/latticesurgery-com/lattice-surgery-compiler | Resolves. Lattice-surgery compiler. Correct. |
| TQE-127 | github.com/openquantumhardware/qick | Resolves. QICK controller framework. Correct for a PARTIAL status (the tool, not the paper's workflow). |
| TQE-142 | github.com/BQSKit/bqskit | Resolves. Berkeley Quantum Synthesis Toolkit. Correct for a PARTIAL status. |

**Two field-misuse findings.**
- **FGCS-079** has `artifact_status: PUBLIC_CODE` with `artifact_url` set to the literal string
  `"UNKNOWN"`, while its own note says the repository URLs were not recoverable. The status should be
  PARTIAL and the URL empty.
- **Ten records** (TCAD-001, TCAD-025, TCAD-027, TCAD-030, TCAD-033, TCAD-043, TCAD-045, TCAD-051,
  TCAD-063, TC-029) put an **arXiv abstract page** in `artifact_url` while carrying
  `artifact_status: UNKNOWN`. A preprint page is not a code or data artifact; those values belong in
  `arxiv_id`.

No artifact needs downgrading to NO_PUBLIC_ARTIFACT_FOUND on grounds of not resolving.

## Check 11 — Seed anchoring

**(a) Presence.** 23 of the 24 seed items are present in the corpus. All 23 are INCLUDED:

FGCS-002 (QFaaS), FGCS-007 (Paving the way), FGCS-015 (quantum accelerator platform virtualization),
FGCS-018 (Integrating QC resources into HPC ecosystems), FGCS-041 (QHDL), FGCS-043 (Bridging paradigms),
FGCS-045 (NetQIR), FGCS-080 (Three ways to share a QPU); TQE-038 (FASQuiC), TQE-078 (QKNOB), TQE-130
(controller benchmarking), TQE-214 (ZAP); TQC-021 (ARQUIN), TQC-019 (MQT Predictor), TQC-054 (DQC-QR),
TQC-009 and TQC-025 (mapping); TPDS-008; TC-011 (Qu-Trefoil), TC-023 (AdaptDQC); TCAD-024 (parallel qubit
mapper), TCAD-062 (qfusion-opt); TACO-001 (QuCloud+), TACO-006 (LarQucut), TACO-007 (Ecmas+).

**One seed is missing from the corpus entirely**: the closed-loop quantum processor plus Fugaku work.
It is `10.1016/j.future.2026.108731`, "Closed-loop calculations of electronic structure on a quantum
processor and a classical supercomputer at full scale", online 2026-07-29, FGCS volume 186. It is listed
as ADDENDUM_CANDIDATE in check 14 and is a direct consequence of the FGCS volume-boundary coverage gap.

**(b) Were seeds waved through?** A 100% inclusion rate for seeds against an 18.6% rate for the corpus is
worth stating plainly, and it is the single strongest signal of anchoring risk in this census. Re-reading
each seed against the gates, the substantively challengeable ones are TQE-038 (spin-qubit control
electronics — but it records a 76.8 ns worst-case digital feedback latency and a reconfigurable FPGA
control architecture, so Gate 1 and Gate 2 hold), TQE-034 and TQE-078 (benchmark construction), and
TCAD-062 (title-only evidence). **No seed was found to have been included on grounds that its verdict
could not otherwise support**, but TQE-034 is among the proposed demotions in check 7 and TCAD-062 is
listed under residual uncertainty.

**(c) Did the census rebuild the population?** Yes, and by a wide margin. 104 INCLUDED records against
24 seed items: **80 of 104 included records (77%) are not seeds**, so the included set is 4.3x the seed
list. Per journal the non-seed share is FGCS 13/21, TQE 24/28, TQC 22/27, TCAD 12/14, TC 5/7, TACO 1/4,
TPDS 1/2, JPDC 1/1. The census also screened 455 records to EXCLUDED or BORDERLINE, which no seed list
could have produced.

## Check 12 — TQE / TQC scope

| Journal | Population screened | INCLUDED | Rate | + BORDERLINE | Rate |
|---|---:|---:|---:|---:|---:|
| TQE | 246 | 28 (27 corrected) | 11.4% | 63 | 25.6% |
| TQC | 97 | 27 | 27.8% | 39 | 40.2% |

TQE's 11.4% retention with a 74.4% outright exclusion rate is consistent with a disciplined screen, and
the excluded set is dominated by exactly the classes `CRITERIA.md` names. **The TQE retained set has not
drifted into general quantum literature.** The retained records that are nearest the boundary and are
named here as requested: **TQE-163** (optically networked trapped-ion modules — device and networking),
**TQE-108** (control-electronics memory), **TQE-038** (spin-qubit control electronics, but latency- and
resource-quantified), **TQE-034** and **TQE-098** (benchmarking methodology for quantum algorithms rather
than a classical systems mechanism). TQE-238, despite the word "network" in its title, is a distributed
fault-tolerant computing design framework and belongs.

TQC's 27.8% is high in absolute terms but TQC is an architecture and systems venue, and its markdown
states an explicit operating discriminator (does the paper state a classical cost quantity, or only a
quantum-resource quantity) that is visible and correctly applied in the excluded set. **No wholesale
drift.** Named boundary cases: **TQC-059** (annealer minor embedding), **TQC-077** (QUBO quadratisation),
**TQC-022** (optimization-application benchmarking), **TQC-066** (qLDPC memory architecture),
**TQC-089** (a VQA library, i.e. class 5 adjacent, retained on its tensor-network batching contribution),
**TQC-016** (design methodology), **TQC-035** (an editorial). Six of these seven are in the proposed
demotion list.

## Check 13 — TPDS and JPDC

All 17 records were re-read individually.

**No inflation.** TPDS's two INCLUDED records — TPDS-007 (QuanTrans, level-by-level distributed
state-vector simulation replacing intermediate communication with a final merge) and TPDS-008
(communication-partition co-optimization on CPU+GPU clusters) — are both unambiguous distributed quantum
circuit simulation work and would pass the gates in any of the eight journals. JPDC's single INCLUDED
record, JPDC-007, is honestly typed REVIEW_SURVEY and correctly contributes **0** to the original-research
count, so JPDC's original-research total is zero and is reported as zero.

**No wrongful exclusion found.** The eight excluded TPDS records are three GPU post-quantum-cryptography
implementations (class 1), four classical electronic-structure and many-body HPC papers — PWDFT-SW, two
NNQS papers, HIP-DFPT (class 3) — and one parallel simulated-annealing paper (class 2). Each is a genuine
HPC contribution with no quantum computing in it, which is precisely the distinction `CRITERIA.md` draws.
The six excluded JPDC records are quantum-inspired metaheuristics, a QNN intrusion-detection application,
a post-quantum cryptography architecture and two records with no quantum content at all.

**One caveat.** TPDS 2024 = 0 and 2025 = 0 INCLUDED are honest numbers, but they rest on a
10-record candidate pool drawn from 552 by title vocabulary. A Crossref bibliographic query for the same
window returned only a subset of the 10 already in the pool and nothing new, which is consistent with but
does not prove full recall. Marked INSUFFICIENT_EVIDENCE below.

## Check 14 — FGCS coverage gap

**Confirmed, and larger than the FGCS agent's note suggested.**

The 81-record FGCS pool stops at `10.1016/j.future.2026.108714`, created 2026-07-17, volume 185
(cover date 2026-12). The Crossref journal listing for ISSN 0167-739X from 2026-07-15 returns 88 items,
and everything from `10.1016/j.future.2026.108710` onward is assigned to **volume 186 or later, whose
cover dates are 2027**. The Crossref sweep window of 2024-01-01..2026-12-31 therefore cut on the volume
cover date, not on availability, and **every FGCS article made publicly available between 2026-07-17 and
2026-12-31 is absent from the pool** — roughly two months of output as of the census date.

Four of those articles are quantum-relevant and are recorded as **ADDENDUM_CANDIDATE** (not classified):

| DOI | Title | Online | Vol |
|---|---|---|---|
| **10.1016/j.future.2026.108731** | Closed-loop calculations of electronic structure on a quantum processor and a classical supercomputer at full scale | 2026-07-29 | 186 |
| **10.1016/j.future.2026.108746** | DistributedEstimator: Distributed training of quantum neural networks via circuit cutting | 2026-08-02 | 186 |
| **10.1016/j.future.2026.108709** | Performance benchmarking of Tensor Trains for quantum-inspired homogenization on TPU, GPU, and CPU architectures | 2026-07-18 | 186 |
| **10.1016/j.future.2026.108754** | Editorial on FGCS special collection on advances in quantum computing Vol III | 2026-08-04 | 186 |

Row one is the missing EXISTENCE_CHECK_SEED from check 11. The editorial's own OpenAlex record shows
publication date 2026-08-04 and 23 cited works, confirming it was publicly available in 2026 despite its
2027 cover date.

The same volume-cover-date cut would affect the other Elsevier journal, JPDC, and should be re-run for
both before any downstream use.

---

## CORRECTIONS TABLE

| record id | DOI | field | recorded value | corrected value | evidence | severity |
|---|---|---|---|---|---|---|
| FGCS-001 | 10.1016/j.future.2023.12.002 | census_year | 2024 | 2023 | OpenAlex publication_date and Crossref `created` both 2023-12-04 | MATERIAL |
| FGCS-001 | 10.1016/j.future.2023.12.002 | in census window | yes (INCLUDED, FGCS 2024) | no — OUT_OF_WINDOW | first availability precedes 2024-01-01 | MATERIAL |
| TQE-007 | 10.1109/tqe.2023.3347106 | census_year | 2024 | 2023 | OpenAlex publication_date 2023-12-26 | MATERIAL |
| TQE-007 | 10.1109/tqe.2023.3347106 | in census window | yes (INCLUDED, TQE 2024) | no — OUT_OF_WINDOW | IEEE Early Access in 2023 | MATERIAL |
| TCAD-057 | 10.1109/tcad.2025.3626447 | census_year | 2026 | 2025 | OpenAlex publication_date 2025-10-28; DOI stem tcad.2025 | MATERIAL |
| TQE (all 246) | — | census_year basis | volume cover year | first public availability | 206/246 online dates are YYYY-01-01 placeholders; convention stated in TQE_census.md | MATERIAL |
| FGCS pool | — | candidate pool coverage | 81 records, ends at online 2026-07-17 | + 4 ADDENDUM_CANDIDATE DOIs in vol 186 | Crossref journal listing for 0167-739X from 2026-07-15 | MATERIAL |
| all_records.json | — | gate1/gate2/gate3 coverage | 29 of 559 (FGCS only) | all 8 journals | field-completeness audit against the 8 per-journal files | MATERIAL |
| TQE (all 246) | — | per-record gate justification | absent | recorded | no gate fields in TQE_records.json; TQE_census.md substitutes a blanket assertion | MATERIAL |
| TQC-035 | 10.1145/3705007 | verdict (proposed) | INCLUDED | BORDERLINE | its own Gate 2 says "editorial framing rather than a technique" | MATERIAL |
| TCAD-038 | — | verdict (proposed) | INCLUDED | BORDERLINE | coherent optical Ising machine solving a QUBO: false-positive class 2 | MATERIAL |
| TCAD-025 | — | verdict (proposed) | INCLUDED | BORDERLINE | fidelity objective; contradicts the TCAD agent's own stated rule | MATERIAL |
| TC-031 | — | verdict (proposed) | INCLUDED | BORDERLINE | fraud-detection fingerprinting; passes on Gate 1 framing alone | MATERIAL |
| TQC-066 | — | verdict (proposed) | INCLUDED | BORDERLINE | qubit-overhead objective; Gate 2 is an analogy | MATERIAL |
| TQE-163 | 10.1109/tqe.2025.3649617 | verdict (proposed) | INCLUDED | BORDERLINE | entanglement-rate objective; classes 4 and 6; no gate text exists | MATERIAL |
| TQC-059 | — | verdict (proposed) | INCLUDED | BORDERLINE | annealer minor embedding; FGCS-063 is BORDERLINE for the same problem | MATERIAL |
| TQC-022 | — | verdict (proposed) | INCLUDED | BORDERLINE | comparisons across devices, not against a classical baseline | MINOR |
| TQC-077 | — | verdict (proposed) | INCLUDED | BORDERLINE | QUBO problem preparation, no quantified comparator | MINOR |
| TQC-016 | — | verdict (proposed) | INCLUDED | BORDERLINE | Gate 2 is a VLSI analogy; BASELINE_UNCLEAR; priority LOW | MINOR |
| TQE-108 | — | verdict (proposed) | INCLUDED | BORDERLINE | control-electronics memory, adjacent to class 6 | MINOR |
| TQE-034 | 10.1109/tqe.2024.3404502 | verdict (proposed) | INCLUDED | BORDERLINE | no classical systems mechanism named | MINOR |
| FGCS-058 | 10.1016/j.future.2025.108095 | census_year | 2026 | 2025 | OpenAlex publication_date 2025-08-22 | MINOR |
| FGCS-027 | 10.1016/j.future.2024.107623 | census_year | 2025 | 2024 | DOI stem j.future.2024; exact date INSUFFICIENT_EVIDENCE | MINOR |
| FGCS-028 | 10.1016/j.future.2024.107646 | census_year | 2025 | 2024 | DOI stem j.future.2024; exact date INSUFFICIENT_EVIDENCE | MINOR |
| TQE-001…006, 008 | 10.1109/tqe.2023.* | census_year | 2024 | 2023 (probable OUT_OF_WINDOW) | IEEE DOI year 2023, confirmed for sibling TQE-007 | MINOR |
| TCAD-001…008 | 10.1109/tcad.2023.* | census_year | 2024 | 2023 (probable OUT_OF_WINDOW) | IEEE DOI year 2023 | MINOR |
| TC-001 | 10.1109/tc.2021.3066614 | census_year | 2024 | 2021 (OUT_OF_WINDOW) | IEEE DOI year 2021; entered only via a 2024-02 issue cover date | MINOR |
| TC-002 | 10.1109/tc.2023.3337308 | census_year | 2024 | 2023 (probable OUT_OF_WINDOW) | IEEE DOI year 2023 | MINOR |
| TC-032 | 10.1109/tc.2025.3630119 | census_year | 2026 | 2025 | IEEE DOI year 2025 | MINOR |
| TCAD-056 | 10.1109/tcad.2025.3611101 | census_year | 2026 | 2025 | IEEE DOI year 2025 | MINOR |
| TQE-077 | 10.1109/tqe.2024.3520805 | census_year | 2025 | 2024 | IEEE DOI year 2024; online date is a volume placeholder | MINOR |
| FGCS-079 | 10.1016/j.future.2026.108686 | artifact_url / status | "UNKNOWN" / PUBLIC_CODE | "" / PARTIAL | a PUBLIC_CODE status with a literal "UNKNOWN" URL is self-contradictory | MINOR |
| TC-041 | 10.1109/tc.2026.3724836 | arxiv_id / abstract_status | none / NO_ABSTRACT | 2502.11316 / abstract available | arXiv:2502.11316 confirms the FPGA emulator's resource, complexity and energy claims | MINOR |
| FGCS-055 | 10.1016/j.future.2025.108270 | arxiv | (empty) | 2503.15439 | preprint confirms the 50.68x and >31x figures and their baseline | MINOR |
| FGCS-064 | 10.1016/j.future.2026.108484 | arxiv | (empty) | 2408.11311 | preprint; note the journal version states 102 qubits and adds the 3.55x CLOPS figure | MINOR |
| FGCS-002, FGCS-057, FGCS-073, TC-027, TC-040, TCAD-010, TCAD-066 | — | conference_extension evidence | RELATED_LINEAGE, no evidence | state evidence or set UNKNOWN | CRITERIA.md requires a named predecessor for RELATED_LINEAGE | MINOR |
| TC, TPDS, JPDC records.json | — | gate fields | absent in JSON, present in markdown | present in both | JSON/markdown divergence | MINOR |
| TCAD-001, 025, 027, 030, 033, 043, 045, 051, 063; TC-029 | — | artifact_url | arXiv abstract page | "" (move to arxiv_id) | a preprint page is not a code or data artifact | COSMETIC |
| all records | — | deep_dive_priority scale | 3/4/5 (FGCS) vs HIGH/MEDIUM/LOW | one scale | the two scales cannot be ranked against each other | COSMETIC |
| TQC-019 | 10.1145/3705194 | artifact_url | github.com/cda-tum/mqt-predictor | github.com/munich-quantum-toolkit/predictor | resolves only by redirect | COSMETIC |

---

## RESIDUAL UNCERTAINTY

All marked INSUFFICIENT_EVIDENCE.

1. **Per-record IEEE Early Access dates** for TQE-001…006/008, TCAD-001…008, TC-002, TC-032, TCAD-056 and
   TQE-077. The IEEE DOI year is a strong signal and was confirmed for two representatives, but Crossref
   and OpenAlex rate-limited before the rest could be checked. TQE-163 shows the signal can mislead.
2. **The remainder of the TQE census years.** Because the volume convention was applied uniformly, no TQE
   census year outside the eight identified above has been positively verified against an availability date.
3. **Fifteen quantitative claims** (FGCS-033, FGCS-057, FGCS-079, FGCS-080, TQE-062, TQE-075, TQE-142,
   TQE-150, TQC-009, TQC-030, TQC-051, TQC-074, TQC-094, TACO-009, TCAD-010) were not re-checked against a
   primary source. None is a bare speedup and all carry a comparator or a BASELINE_UNCLEAR tag; the four
   claims that were checked all held.
4. **TCAD-062 (`qfusion-opt`)** is INCLUDED on title-only evidence, with a one-line Gate 2. It is also a
   seed. Unresolved.
5. **TCAD-058, TCAD-061, TCAD-064, TCAD-066** remain BORDERLINE or INSUFFICIENT_EVIDENCE on title-only
   evidence because IEEE Xplore was unreachable. Not re-attempted here.
6. **Recall of the TC, TCAD, TACO and JPDC candidate pools.** The vocabulary filter plus OpenAlex union
   could not be independently reproduced; Crossref's ranked text search is demonstrably incomplete for
   this purpose.
7. **Whether the JPDC sweep has the same volume-cover-date cut as FGCS.** Both are Elsevier, so it is
   likely, but it was not tested.
8. **The 14 of 24 Vol III special-collection titles** the FGCS agent could not recover. Three of the four
   ADDENDUM_CANDIDATEs above are probably among them, but the mapping was not established.

---

## CORRECTED HEADLINE COUNTS

Applying only the three confirmed census-year corrections (FGCS-001 and TQE-007 out of window;
TCAD-057 2026 → 2025). The twelve proposed demotions are **not** applied.

| Journal | 2024 | 2025 | 2026 | INCLUDED total | of which original research |
|---|---:|---:|---:|---:|---:|
| FGCS | 6 (was 7) | 8 | 6 | **20** (was 21) | **18** (was 19) |
| TQE | 7 (was 8) | 13 | 7 | **27** (was 28) | **27** (was 28) |
| TQC | 8 | 9 | 10 | 27 | 24 |
| TACO | 1 | 2 | 1 | 4 | 4 |
| TPDS | 0 | 0 | 2 | 2 | 2 |
| TC | 2 | 3 | 2 | 7 | 7 |
| JPDC | 0 | 0 | 1 | 1 | 0 |
| TCAD | 6 | 7 (was 6) | 1 (was 2) | 14 | 14 |
| **Total** | **30** (was 32) | **42** (was 41) | **30** (was 31) | **102** (was 104) | **96** (was 98) |

Denominators also move: the TQE screened population falls from 246 to 238 if the seven further 2023
records are confirmed out of window, the TCAD candidate pool from 68 to 60, the TC pool from 41 to 39, and
the FGCS pool from 81 to 80 — while the FGCS pool should *grow* by at least the four ADDENDUM_CANDIDATEs
once the volume-186 gap is closed.

If all twelve proposed demotions in check 7 were accepted, INCLUDED would be **90** and included original
research **85**.

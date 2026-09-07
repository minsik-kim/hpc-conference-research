# ASPLOS 2024–2026 — Quantum-HPC Regular Paper Census

**Phase 3 of the Quantum-HPC Research Landscape**
**Census date: 2026-09-06 (KST)**
**Scope: ASPLOS main-conference regular research papers, 2024 / 2025 / 2026**
**Comparison baseline: `SC_2024_2025_QUANTUM_HPC_CENSUS.md`**

---

## 0. How to read this document

| Tag | Meaning |
|---|---|
| `[official-program]` | Verified against the official ASPLOS technical program |
| `[proceedings]` | Verified against the publisher volume record (Crossref container metadata) |
| `[paper]` | Read from the published paper or an author-hosted camera-ready |
| `[paper-preprint]` | Read from an arXiv preprint — **the published version may differ** |
| `[abstract]` | Only the abstract was obtainable |
| `[code]` | Observed directly in a source repository |
| `[artifact]` | From an artifact package, Zenodo deposit, or AE material |
| `[documentation]` | From a README or project page |
| `[inference]` | My reasoning on top of the above — **never a paper fact** |

Hardware evidence levels: `REAL_HARDWARE` · `FPGA_PROTOTYPE` · `RTL_SYNTHESIS` · `CYCLE_SIMULATION` · `ARCH_SIMULATION` · `SOFTWARE_SIMULATION` · `ANALYTIC_MODEL` · `PROJECTED`.
Maturity: `NISQ` · `EARLY_FTQC` · `FTQC` · `GENERAL` · `UNCLEAR`.
Artifact: `PUBLIC_CODE` · `PUBLIC_ARTIFACT` · `PARTIAL` · `NO_PUBLIC_ARTIFACT_FOUND` · `UNKNOWN`.
Consistency: `CONSISTENT` · `PARTIAL_MATCH` · `MISMATCH` · `INSUFFICIENT_EVIDENCE`.
Trend: `OBSERVED_SHIFT` · `INSUFFICIENT_SAMPLE`. Conflict: `TRUE_CONFLICT` · `DIFFERENT_REGIME` · `DIFFERENT_METRIC` · `INSUFFICIENT_EVIDENCE`.
Absence: **`VENUE_GAP` only.** This document declares no research gap and uses none of "novel", "unexplored", "first".

> **Sourcing.** ACM DL and IEEE Xplore are unreachable from this environment (proxy 403), and `curl` egress is blocked entirely. Bibliographic facts come from the **Crossref REST API**; programs from the official ASPLOS sites; paper content overwhelmingly from **arXiv preprints and author-hosted camera-readies**, each tagged. Two papers (**A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer**, **ACQC**) are abstract-only and their entries are honestly thin.

---

## 1. Executive summary

### 1.1 The corpus

**36 quantum-relevant main-track regular papers** were presented across the three conferences — substantially more than the 9/10/12 that a census built from the published programs finds.

**Two denominators, never mixed.** The **proceedings** denominator rests on a volume enumeration; the **program** denominator is *arithmetic derived from the volume structure plus the deferral rule*, not a count taken from a program page. Block C reports separately what the conferences' own published programs actually show, which for 2024 is less than the whole program (§2.5, limitation 4).

| | ASPLOS 2024 | ASPLOS 2025 | ASPLOS 2026 |
|---|---|---|---|
| **A — Proceedings year** *(bibliographic)* | | | |
| Quantum papers by proceedings year | 15 | 8 | 11 |
| Regular papers in proceedings | 194 | 176 | 152 |
| **Share of proceedings** | **7.7%** | **4.5%** | **7.2%** |
| **B — Program year** *(volume-derived, not counted from a program)* | | | |
| **Quantum papers presented** | **14** | **10** | **12** |
| Papers presented (volume-derived) | ~193 `TOTAL_COUNT_UNVERIFIED` | 184 (derived) | 168 |
| Share of program (derived) | ~7.3% | ~5.4% | ~7.1% |
| **C — What the published program shows** | | | |
| Dedicated quantum sessions | 2 | 2 | 3 (one only half quantum) |
| Quantum papers locatable in the program | 9 of 14 | 10 of 10 | 12 of 12 |
| Program page retrievable in full? | **No — truncates after Session 8C** | Yes | Yes |
| Session placement of the remaining 5 | `STATUS_UNCLEAR` | — | — |
| Papers with public artifact | 12 of 14 (86%) | 5 of 10 (50%) | 7–8 of 12 (58–67%) |

The 2024 program denominator is marked `TOTAL_COUNT_UNVERIFIED` because it is 170 enumerated papers (29th V1–V3) plus the 28th-Volume-4 cohort that fed the 2024 program, whose size was never enumerated in this census. The proceedings row is the series with the firmer basis.

### 1.2 The five findings that matter most

**F1 — ASPLOS defers a whole volume to the next year's program, and this changes every count.**
ASPLOS runs three submission cycles; the **fall cycle is published in a volume branded year N but presented at conference year N+1**. Verbatim from the ASPLOS 2024 CFP: *"Accepted major revisions of the fall cycle will be published as ASPLOS'24 papers but will be presented in ASPLOS'25."* `[official-CFP]` So **Clapton** is bibliographically ASPLOS'24 (29th, Volume 4) but was presented at ASPLOS 2025, and **PowerMove** is ASPLOS'25 (30th, Volume 3) presented at ASPLOS 2026. **Proceedings year and program year are different denominators and must never be mixed.** This document reports both.

**F2 — ASPLOS 2024's quantum population is 14, not the 9 a program-based census finds — a 36% undercount, from two separable causes.**
A census built from the published ASPLOS 2024 program finds **9**, all inside *Session 5D: Quantum Architecture* (5) and *Session 6D: Variational Quantum Computing* (4). A sweep of the volumes finds **14**. The five a program-based census misses are **One Gate Scheme to Rule Them All** (ISA design), **MorphQPV** (verification), **OnePerc** (photonic compilation), **Fermihedral** (fermion-to-qubit encoding) and **Exploiting the Regular Structure… with Permutable Operators** (compilation). `[proceedings]`

Two causes, and they must be kept apart:

1. **The official ASPLOS 2024 program page is incomplete.** It lists sessions 1A–8C and then stops mid-track; no session after 8C appears anywhere on it. `[official-program]` A substantial part of the program is therefore unretrievable, and **none of the five can be located on that page — but neither can they be shown to be absent from the program.** Their session placement is `STATUS_UNCLEAR`.
2. **Permutable Operators is a deferred paper** — 28th ASPLOS Volume 4, proceedings year 2023, presented in 2024 — so no sweep of the 2024-branded volumes would find it either.

**The methodological lesson stands, but it is about instruments rather than sessions: at ASPLOS neither session names nor the conference's own program page is a sufficient census instrument. Only a volume sweep combined with the deferral rule is.** An earlier draft of this census stated that the five "sat outside the two quantum-named sessions"; that was an inference the evidence does not carry, and it has been withdrawn (Appendix A, C1).

**F3 — The quantum share is roughly flat, not rising.**
By proceedings year — the series with the firmer denominator — the shares are **7.7% → 4.5% → 7.2%**. By program year, on volume-derived denominators, they are **~7.3% → ~5.4% → ~7.1%**. Both series are flat with a 2025 dip; neither is a program-page count. A prior reading reported a monotonic rise of 4.7% → 5.6% → 7.9%; that story does not survive the corrected 2024 count. What did change is **composition, not volume** — see §6. `OBSERVED_SHIFT` in composition, `INSUFFICIENT_SAMPLE` for any volume trend.

**F4 — On compilation, ASPLOS and SC argue in fundamentally different currencies.**
SC's three compilation papers were **3 of 3** on compile-time scalability: the incumbent exact method's measured failure (SATMAP at 2 hours, DPQA at 24 hours) *is* the problem statement. Of ASPLOS's ten compilation/mapping papers, **only 2 make that argument centrally** (QTurbo, PowerMove), with one partial (Reducing T Gates). Seven argue **output quality** — fewer gates, lower depth, better fidelity, a better abstraction boundary — or use a different cost model entirely (QPU shots, hard real-time execution latency, verification time). `[paper-preprint]` **GUOQ is the cleanest inversion: its stated protocol is that "*unless otherwise indicated*, we allocated each tool 1 hour," and it asks who produces the best circuit inside that budget — compile time as experimental *control*, the precise opposite of SC's treatment of it as the dependent variable. The hedge is load-bearing and is recorded here rather than smoothed over: Quarl is an explicit exception, run on an A100 with 64 GB, so the budget is a default rather than a uniform constraint.** `[paper-preprint]`

**F5 — ASPLOS's artifact profile is almost identical to SC's, and contains exactly one hardware description in 36 papers.**
22 of 36 have a clearly public artifact (**61%**) against SC's 7 of 11 (**64%**) — statistically indistinguishable, despite ASPLOS running a formal Artifact Evaluation process and SC not requiring one. And of the ~22 artifacts, **~16 are Python or C++ simulation and compiler code.** Two papers make FPGA claims; **only Micro Blossom ships HDL.** Promatch claims a Kintex UltraScale+ synthesis result and publishes only C++/MPI. `[code]` **An architecture conference produces essentially the same artifact profile as an HPC conference: software simulation, not hardware.**

### 1.3 The answer to the census's central question

**ASPLOS accepts a quantum paper when it proposes a mechanism or an abstraction — SC accepts one when it demonstrates a cost.**

Both venues take "quantum as workload, classical systems as contribution." The difference is what discharges the burden of proof. At SC the admission ticket is a **measured cost that falls**: wall-clock, energy-to-solution, communication volume, occupancy, compile time. At ASPLOS the admission ticket is a **designed structure that is better**: an instruction set (AshN, ReQISC), an IR that separates a nondeterministic hardware layer from a deterministic compiler view (OnePerc's FlexLattice), a memory hierarchy (Fat-Tree QRAM, HetEC), a predecoder that filters before an exact stage (Promatch), a processing element per graph vertex (Micro Blossom). Performance numbers support the design; they are rarely the thesis. `[inference]`

The corollary matters for this research programme: **an ASPLOS-shaped contribution does not automatically transfer to SC.** It needs a cost model attached, at a scale where the cost bites.

---

## 2. Methodology

### 2.1 Inclusion

A paper is included if it is an **ASPLOS main-conference regular research paper** presented in 2024, 2025 or 2026 AND concerns quantum computing with architecture/system/computation relevance: quantum architecture; QEC decoding architecture or system; quantum control architecture; quantum compilation with architecture/system contribution; mapping/routing with scalability or performance contribution; quantum simulation acceleration; memory systems for quantum simulation; distributed quantum execution; multi-QPU or modular architecture; QPU virtualization or resource sharing; runtime/system software; hybrid CPU/GPU/QPU architecture; fault-tolerant quantum architecture; architecture support for quantum workloads; performance or reliability modeling; benchmarking.

### 2.2 Exclusion

Structurally excluded: workshops and workshop proceedings, posters, demos, tutorials, panels, invited talks, keynote abstracts, industry-only material, extended abstracts, short papers, non-archival items. Topically excluded: pure device physics, fabrication, pure quantum information theory, pure algorithm papers with no architecture/system/computation implication, chemistry-accuracy-only work, purely mathematical quantum-advantage proofs. Also excluded and tracked separately: post-quantum cryptography, ML *quantization*, classical fault tolerance, and "quantum-inspired" classical methods.

### 2.3 The volume structure — the foundational methodological fact

ASPLOS publishes each year's main conference across **multiple ACM proceedings volumes** corresponding to submission cycles. All are main conference. The fall cycle defers to the next year's program.

| Conf. year | Edition | Volume | DOI stem | Raw items | Non-papers | **Regular papers** | Presented at |
|---|---|---|---|---|---|---|---|
| 2024 | 29th | V1 | `10.1145/3617232` | 28 | 0 | 28 | ASPLOS 2024 |
| 2024 | 29th | V2 | `10.1145/3620665` | 76 | 0 | 76 | ASPLOS 2024 |
| 2024 | 29th | V3 | `10.1145/3620666` | 70 | 4 | 66 | ASPLOS 2024 |
| 2024 | 29th | V4 | `10.1145/3622781` | 24 | 0 | 24 | **ASPLOS 2025** |
| 2025 | 30th | V1 | `10.1145/3669940` | 72 | 0 | 72 | ASPLOS 2025 |
| 2025 | 30th | V2 | `10.1145/3676641` | 88 | 0 | 88 | ASPLOS 2025 |
| 2025 | 30th | V3 | `10.1145/3676642` | 19 | 3 | 16 | **ASPLOS 2026** |
| 2026 | 31st | V1 | `10.1145/3760250` | 20 | 0 | 20 | ASPLOS 2026 |
| 2026 | 31st | V2 | `10.1145/3779212` | 135 | 3 | 132 | ASPLOS 2026 |

`[proceedings]` The chain extends backwards: **28th ASPLOS Volume 4** (`10.1145/3623278`) fed the ASPLOS 2024 program, and contributes two quantum papers (VarSaw, Permutable Operators) whose proceedings year is 2023.

**Totals.** Proceedings year: 2024 = **194**, 2025 = **176**, 2026 = **152**.

Program year is **derived from this table plus the deferral rule, not counted from any program page**: 2025 = **184** (30th V1+V2 = 160, plus 29th V4 = 24) and 2026 = **168** (30th V3 = 16, plus 31st V1+V2 = 152; the official 2026 program page states "167 unique papers" and the one-paper discrepancy is unresolved). **2024 = 170 enumerated (29th V1+V2+V3) plus the 28th-Volume-4 cohort, which this census never enumerated** — hence ≈ **193**, marked `TOTAL_COUNT_UNVERIFIED`. Every program-year share below inherits that status.

There is **no ASPLOS 2026 Volume 3** — the 2026 CFP lists only two cycles. `[official-CFP]`

### 2.4 How completeness was established

**The instrument, stated exactly, because the denominators are only as good as it is.** ACM DL and IEEE Xplore are unreachable from this environment and `curl` egress is blocked, so no byte-exact API retrieval was possible. Volume contents were obtained from the **Crossref REST API** read through `WebFetch` — that is, a summarising read of the JSON response, not a raw download.

Three consequences that a reader must weigh:

1. **Crossref exposes no volume-level item count, and its `container-title` filter is silently ignored** — a query using it returns unrelated results with no error. No count in this census comes from that filter. Counts were built instead from **date-windowed `prefix:10.1145` queries with `cursor=*` deep paging, filtered client-side on the DOI stem** of each volume.
2. **`offset` paging is unstable** — `offset=100` on the 2025-03-30 window re-served two items already returned at `offset=50`. Cursor paging is deterministic and was used throughout.
3. **Item-level records were retained only for the 2024 volumes.** A retained extract of 170 DOIs with page ranges covers 29V2 (76), 29V3 (70) and 29V4 (24) and reconciles exactly. For 29V1 (28), 30V1 (72), 30V2 (88), 30V3 (19), 31V1 (20) and 31V2 (135) the retained extracts are **partial** (70 of 72 for 30V1, 87 of 88 for 30V2, 125 of 135 for 31V2), and those totals rest on the sweep's own reported item count rather than on an enumeration this census can re-display.

**Status of the denominators, therefore: 2024 = enumerated and reconciled; 2025 and 2026 = single-source and should be read as ±a few papers.** Corpus *membership* is on firmer ground than the denominators: every one of the 36 papers has its title and DOI corroborated by at least one non-Crossref source — arXiv, an author or group page, or an official program.

**A contiguity claim corrected in verification.** An earlier draft stated that 29V2 is `3640353–3640428`, "76 items with no gaps." The retained extract shows 76 items but **one gap at `3640398` and one out-of-range DOI, `3640665`** — the count is right, the contiguity claim was not. 29V3 is `3651322–3651387` (66 papers) plus four keynote DOIs `3655589–3655592` = 70 items. 29V4 is `3674167–3674190` less `3674187`, plus `3698899` = 24 items. 30V1 was reported as `3707214–3707287` less two; the retained extract covers only 67 of those, so that range is `[inference]` from the sweep rather than a displayed enumeration.

All titles in every volume were swept against a ~50-term keyword set, not just "quantum".

**Trap avoided:** `10.1145/3818671.*` is the *18th Workshop on General Purpose Processing Using GPU*, which shares ASPLOS 2026's 2026-03-22 publication date. It is not ASPLOS. `[proceedings]`

### 2.5 Limitations — stated plainly

1. **Most paper content is from preprints**, not published versions. Every such fact is tagged `[paper-preprint]`. Where a preprint and a camera-ready were both available (QRCC, MorphQPV, BQSim) they were cross-checked.
2. **Two papers are abstract-only**: *A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer* and *ACQC*. Both are from the same SNU group, both make large architectural claims, and neither is readable from this environment. Their mechanisms have not been inferred.
3. **The ASPLOS 2025 program total of 184 is derived, not counted.** It follows from the volume counts plus the deferral rule (30th V1+V2 = 160, plus 29th V4 = 24), and five spot-checked Volume 4 titles were confirmed on the 2025 program. A direct recount of that program page would be worthwhile.
4. **The ASPLOS 2024 official program page is incomplete.** It lists sessions 1A, 1B … 8C and then stops; nothing after 8C appears, and the last entry is cut off mid-session. Both URL variants (`/main-program/` and `/main-program/index.html`) return the same truncated content. Consequently: (a) the retrievable portion holds roughly 140 papers, which is **not** the 2024 program total and must not be used as a denominator; (b) the session placement of five quantum papers is `STATUS_UNCLEAR` — they cannot be located on the page and cannot be shown absent from the program; (c) their *presence* in the 2024 program rests entirely on the volume sweep plus the deferral rule, which do not depend on the program page.
5. **ASPLOS artifact badge status is not publicly determinable.** The AEC sites state badges are "printed on the papers themselves and available as meta information in the ACM Digital Library" — and nowhere else. With ACM DL blocked, badge status is `UNKNOWN` for all 36 papers. That invisibility is itself a finding (§12).
6. **Figure-only values could not be extracted** for a few papers (Fermihedral's solve times, Borrowing Dirty Qubits' wall-clocks, ReQISC's runtime figure). These are recorded `NOT_FOUND` rather than estimated.

---

## 3. ASPLOS 2024 census — 14 papers

**Sessions** `[official-program]`: the retrievable part of the 2024 program (sessions 1A–8C; the page stops there) contains two quantum-named sessions — *Session 5D: Quantum Architecture* (5 papers) and *Session 6D: Variational Quantum Computing* (4 papers), 9 papers in total. **The five further quantum papers below are established by the volume sweep, not by the program page; where they were scheduled is `STATUS_UNCLEAR`** because the program page truncates before the end of the conference.

| # | Title | DOI | Vol / proc. yr | Branch | Tags | Maturity | Artifact |
|---|---|---|---|---|---|---|---|
| 1 | Codesign of quantum error-correcting codes and modular chiplets in the presence of defects | `10.1145/3620665.3640362` | 29V2 / 2024 | QEC architecture | `HPC_FOR_Q` `FUTURE_WORKLOAD` | `FTQC` | `PARTIAL` |
| 2 | MECH: Multi-Entry Communication Highway for Superconducting Quantum Chiplets | `10.1145/3620665.3640377` | 29V2 / 2024 | interconnect / modular | `Q_IN_HPC` `FUTURE_WORKLOAD` | `EARLY_FTQC` | `PUBLIC_ARTIFACT` |
| 3 | QuFEM: Fast and Accurate Quantum Readout Calibration Using the Finite Element Method | `10.1145/3620665.3640380` | 29V2 / 2024 | calibration / postprocessing | `HPC_FOR_Q` | `NISQ` | `PUBLIC_CODE` |
| 4 | A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer | `10.1145/3620665.3640388` | 29V2 / 2024 | FTQC system architecture | `Q_IN_HPC` `FUTURE_WORKLOAD` | `FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 5 | Elivagar: Efficient Quantum Circuit Search for Classification | `10.1145/3620665.3640354` | 29V2 / 2024 | QML / circuit search | `Q_FOR_HPC` | `NISQ` | `PUBLIC_CODE` |
| 6 | Red-QAOA: Efficient Variational Optimization through Circuit Reduction | `10.1145/3620665.3640363` | 29V2 / 2024 | variational optimization | `Q_FOR_HPC` `FUTURE_WORKLOAD` | `NISQ` | `PUBLIC_CODE` |
| 7 | **One Gate Scheme to Rule Them All** (AshN) | `10.1145/3620665.3640386` | 29V2 / 2024 | ISA / gate set | `HPC_FOR_Q` | `GENERAL` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 8 | Promatch: Extending the Reach of Real-Time QEC with Adaptive Predecoding | `10.1145/3620666.3651339` | 29V3 / 2024 | **QEC decoding** | `HPC_FOR_Q` | `EARLY_FTQC` | `PUBLIC_CODE` |
| 9 | ProxiML: Building Machine Learning Classifiers for Photonic Quantum Computing | `10.1145/3620666.3651367` | 29V3 / 2024 | photonic QML | `Q_FOR_HPC` | `NISQ` | `PUBLIC_ARTIFACT` |
| 10 | **MorphQPV**: Exploiting Isomorphism in Quantum Programs to Facilitate Confident Verification | `10.1145/3620666.3651360` | 29V3 / 2024 | verification | `HPC_FOR_Q` | `NISQ` | `PUBLIC_CODE` |
| 11 | **OnePerc**: A Randomness-aware Compiler for Photonic Quantum Computing | `10.1145/3620666.3651372` | 29V3 / 2024 | photonic compilation | `HPC_FOR_Q` | `GENERAL` | `PUBLIC_ARTIFACT` |
| 12 | **Fermihedral**: On the Optimal Compilation for Fermion-to-Qubit Encoding | `10.1145/3620666.3651371` | 29V3 / 2024 | encoding / compilation | `HPC_FOR_Q` `Q_FOR_HPC` | `GENERAL` | `PUBLIC_CODE` |
| 13 | VarSaw: Application-tailored Measurement Error Mitigation for VQAs | `10.1145/3623278.3624764` | **28V4 / 2023** | measurement mitigation | `HPC_FOR_Q` | `NISQ` | `PUBLIC_CODE` |
| 14 | **Exploiting the Regular Structure of Modern Quantum Architectures… Permutable Operators** | `10.1145/3623278.3624751` | **28V4 / 2023** | compilation | `HPC_FOR_Q` | `NISQ` | `PUBLIC_CODE` |

Papers **7, 10, 11, 12, 14** in bold are those outside the quantum-named sessions.

**Character of the year.** ASPLOS 2024 is the **NISQ-heaviest** of the three. Six of fourteen are variational/QML/mitigation papers (Elivagar, Red-QAOA, VarSaw, ProxiML, plus QuFEM's readout calibration and MorphQPV's verification), which is the profile a prior survey described as "half NISQ variational work with little for a systems builder" — accurate for the visible nine, but it misses that 2024 also carried the corpus's most ambitious system-architecture paper (Million Qubit-Scale) and its first QEC decoder (Promatch).

---

## 4. ASPLOS 2025 census — 10 papers

**Sessions** `[official-program]`: *Session 1B: Quantum Computing* (5) and *Session 7B: Quantum Error Correction* (5). **Every quantum paper this year sits inside a quantum-named session** — the opposite of 2024.

| # | Title | DOI | Vol / proc. yr | Branch | Tags | Maturity | Artifact |
|---|---|---|---|---|---|---|---|
| 1 | FMCC: Flexible Measurement-based Quantum Computation over Cluster State | `10.1145/3622781.3674185` | **29V4 / 2024** | MBQC execution | `HPC_FOR_Q` `FUTURE_WORKLOAD` | `GENERAL` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 2 | QRCC: Evaluating Large Quantum Circuits on Small Quantum Computers through Integrated Qubit Reuse and Circuit Cutting | `10.1145/3622781.3674179` | **29V4 / 2024** | circuit cutting | `HPC_FOR_Q` `Q_IN_HPC` | `NISQ` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 3 | Clapton: Clifford Assisted Problem Transformation for Error Mitigation in VQAs | `10.1145/3622781.3674178` | **29V4 / 2024** | error mitigation | `HPC_FOR_Q` | `NISQ` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 4 | Optimizing Quantum Circuits, Fast and Slow (GUOQ) | `10.1145/3669940.3707240` | 30V1 / 2025 | compilation | `HPC_FOR_Q` | `GENERAL` | `PUBLIC_CODE` |
| 5 | QECC-Synth: A Layout Synthesizer for QEC Codes on Sparse Architectures | `10.1145/3669940.3707236` | 30V1 / 2025 | QEC layout synthesis | `HPC_FOR_Q` | `EARLY_FTQC` | `PUBLIC_ARTIFACT` |
| 6 | **BQSim**: GPU-accelerated Batch Quantum Circuit Simulation using Decision Diagram | `10.1145/3676641.3715984` | 30V2 / 2025 | **GPU simulation** | `HPC_FOR_Q` | `GENERAL` | `PUBLIC_CODE` |
| 7 | Fat-Tree QRAM: A High-Bandwidth Shared Quantum Random Access Memory for Parallel Queries | `10.1145/3676641.3716256` | 30V2 / 2025 | quantum memory architecture | `FUTURE_WORKLOAD` | `FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 8 | HetEC: Architectures for Heterogeneous Quantum Error Correction Codes | `10.1145/3676641.3716001` | 30V2 / 2025 | QEC architecture | `FUTURE_WORKLOAD` | `FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 9 | **Micro Blossom**: Accelerated Minimum-Weight Perfect Matching Decoding for QEC | `10.1145/3676641.3716005` | 30V2 / 2025 | **QEC decoding** | `HPC_FOR_Q` | `EARLY_FTQC` | `PUBLIC_CODE` |
| 10 | RESCQ: Realtime Scheduling for Continuous Angle QEC Architectures | `10.1145/3676641.3716018` | 30V2 / 2025 | realtime scheduling | `Q_IN_HPC` | `EARLY_FTQC` | `PUBLIC_CODE` |

**Character of the year.** The most **HPC-transferable** year, and the one a prior survey correctly identified as such. It carries the corpus's two strongest classical-systems contributions — **BQSim** (GPU decision-diagram simulation) and **Micro Blossom** (FPGA MWPM decoding, the only HDL artifact in 36 papers) — plus circuit cutting (QRCC) and real-time scheduling (RESCQ). It is also the **lowest-share** year (5.4% program / 4.5% proceedings) and the weakest on artifacts (50%), the latter driven entirely by the three deferred 29V4 papers, none of which released code.

---

## 5. ASPLOS 2026 census — 12 papers

**Sessions** `[official-program]`: *Session 1C: Quantum Computing: Compilation* (5), *Session 4C: Quantum Error Correction* (5), *Session 9B: Quantum & Emerging Computing* (**2 of 4 papers are quantum** — the other two, *CHEHAB RL* (FHE) and *CEMU* (computational storage), are not).

| # | Title | DOI | Vol / proc. yr | Branch | Tags | Maturity | Artifact |
|---|---|---|---|---|---|---|---|
| 1 | PowerMove: Optimizing Compilation for Neutral Atom Quantum Computers with Zoned Architecture | `10.1145/3676642.3736128` | **30V3 / 2025** | neutral-atom compilation | `HPC_FOR_Q` | `NISQ`→`GENERAL` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 2 | QTurbo: A Robust and Efficient Compiler for Analog Quantum Simulation | `10.1145/3760250.3762227` | 31V1 / 2026 | analog compilation | `HPC_FOR_Q` `Q_FOR_HPC` | `NISQ` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 3 | Accelerating Computation in Quantum LDPC Code (ACQC) | `10.1145/3779212.3790122` | 31V2 / 2026 | QEC architecture | `FUTURE_WORKLOAD` | `FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 4 | AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling Problem for QEC Codes | `10.1145/3779212.3790123` | 31V2 / 2026 | syndrome-circuit scheduling | `HPC_FOR_Q` | `GENERAL`/`EARLY_FTQC` | `PUBLIC_CODE` |
| 5 | Architecting Scalable Trapped Ion Quantum Computers using Surface Codes | `10.1145/3779212.3790128` | 31V2 / 2026 | FTQC platform architecture | `FUTURE_WORKLOAD` | `EARLY_FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 6 | Borrowing Dirty Qubits in Quantum Programs | `10.1145/3779212.3790134` | 31V2 / 2026 | programming model / analysis | `HPC_FOR_Q` | `GENERAL` | `PARTIAL` |
| 7 | COMPAS: A Distributed Multi-Party SWAP Test for Parallel Quantum Algorithms | `10.1145/3779212.3790143` | 31V2 / 2026 | **distributed execution** | `Q_IN_HPC` `FUTURE_WORKLOAD` | `EARLY_FTQC` | `PUBLIC_CODE` |
| 8 | iSwitch: QEC on Demand via In-Situ Encoding of Bare Qubits for Ion Trap Architectures | `10.1145/3779212.3790177` | 31V2 / 2026 | selective QEC | `FUTURE_WORKLOAD` | `NISQ`→`EARLY_FTQC` | `NO_PUBLIC_ARTIFACT_FOUND` |
| 9 | PropHunt: Automated Optimization of Quantum Syndrome Measurement Circuits | `10.1145/3779212.3790205` | 31V2 / 2026 | syndrome circuits | `HPC_FOR_Q` | `EARLY_FTQC` | `PUBLIC_CODE` |
| 10 | Reconfigurable Quantum Instruction Set Computers (ReQISC) | `10.1145/3779212.3790208` | 31V2 / 2026 | ISA / compilation | `HPC_FOR_Q` | `GENERAL` | `PUBLIC_ARTIFACT` |
| 11 | Reducing T Gates with Unitary Synthesis (trasyn) | `10.1145/3779212.3790210` | 31V2 / 2026 | FT synthesis | `HPC_FOR_Q` | `FTQC` | `PUBLIC_CODE` |
| 12 | TreeVQA: A Tree-Structured Execution Framework for Shot Reduction in VQAs | `10.1145/3779212.3790239` | 31V2 / 2026 | shot reduction / execution | `Q_IN_HPC` `FUTURE_WORKLOAD` | `NISQ` | `PUBLIC_CODE` |

**Character of the year.** The **most fault-tolerance-oriented and the most compiler-oriented**. Five QEC papers, none of which is a decoder design — the QEC work has moved to compile-time synthesis and platform architecture. Five compilation papers. And it is the year the decoder-microarchitecture line **left ASPLOS**: its continuation (SWIPER, Triage, Coset Ensemble) went to ISCA. See §8.

---

## 6. Cross-year evolution

### 6.1 Volume — `INSUFFICIENT_SAMPLE` for any trend

14 → 10 → 12 papers presented; ~7.3% → ~5.4% → ~7.1% on volume-derived program denominators, 7.7% → 4.5% → 7.2% by proceedings year. **On either denominator the corrected numbers do not support a growth narrative.** With n = 14/10/12 and a single venue, the variation is consistent with noise. The one defensible volume statement is that ASPLOS has sustained a **double-digit quantum population every year for three years**, which no HPC venue in this project has done (SC: 7 and 4).

### 6.2 Composition — `OBSERVED_SHIFT`, and this is the real story

| Branch | 2024 | 2025 | 2026 |
|---|---|---|---|
| QEC (decoding + architecture + synthesis) | 2 | 4 | 5 |
| Compilation / mapping / ISA | 4 | 1 | 5 |
| NISQ applications / mitigation / QML | 5 | 2 | 1 |
| System & memory architecture | 2 | 2 | 2 |
| Simulation | 0 | 1 | 0 |
| Distributed / partitioned execution | 1 | 1 | 1 |

Three movements, each defensible from the corpus:

1. **NISQ applications collapsed: 5 → 2 → 1.** Elivagar, Red-QAOA, VarSaw, ProxiML and MorphQPV in 2024 have no 2026 counterpart except TreeVQA. `OBSERVED_SHIFT`.
2. **QEC grew and changed character: 2 → 4 → 5.** But *within* QEC the subject moved off the decoder — 2024–2025 carried the two decoder-microarchitecture papers, 2026 carries none. §8 develops this.
3. **Compilation is bimodal, not growing**: 4 → 1 → 5. The 2025 dip is an artifact of where papers landed in volumes, not a change in interest. `INSUFFICIENT_SAMPLE` for the shape.

### 6.3 NISQ → FTQC transition — `OBSERVED_SHIFT`

Tagged by each paper's own framing:

| Maturity | 2024 | 2025 | 2026 |
|---|---|---|---|
| `NISQ` | 6 | 2 | 2 |
| `EARLY_FTQC` | 1 | 4 | 4 |
| `FTQC` | 2 | 2 | 2 |
| `GENERAL` | 4 | 2 | 4 |

The centre of mass moved from `NISQ` to `EARLY_FTQC` — single-to-few logical qubits, d ≤ 15, error rates at or just below current hardware. **This matters for HPC integration because the two regimes impose different classical requirements:** NISQ VQE is many shallow circuits with a classical optimizer in a slow outer loop, tolerant of latency; FTQC is continuous syndrome decoding under a microsecond deadline plus deep logical circuits. The classical resource attached to a QPU changes shape entirely between them. `[inference]`

A further `OBSERVED_SHIFT` inside QEC: **the code family moved off the surface code.** 2024 is pure surface code; 2025 introduces qLDPC as a first-class object (HetEC's gross code); 2026 is majority-qLDPC. This silently changes the decoder algorithm class from matching to belief propagation — **and none of the qLDPC papers analyses the resulting real-time decoder cost.** `OPEN_QUESTION`.

---

## 7. Bottom-up research taxonomy

Derived from the 36-paper corpus, not imposed on it.

```
ASPLOS Quantum Research (2024–2026), 36 papers
│
├── QEC — 11 papers, the largest branch
│   ├── Decoder microarchitecture ............ 2   Promatch (24), Micro Blossom (25)
│   │     └─ line leaves ASPLOS after 2025 → ISCA
│   ├── Real-time scheduling ................. 1   RESCQ (25)
│   ├── Syndrome-circuit synthesis ........... 2   AlphaSyndrome (26), PropHunt (26)
│   ├── Code layout / mapping ................ 2   QECC-Synth (25), chiplet codesign (24)
│   └── QEC system architecture .............. 4   HetEC (25), ACQC (26), iSwitch (26),
│                                                  Trapped-ion+surface-codes (26)
│
├── Compilation / mapping / ISA — 10 papers
│   ├── Platform-specific compilers .......... 3   OnePerc (24, photonic), PowerMove (26, atoms),
│   │                                              QTurbo (26, analog)
│   ├── General circuit optimization ......... 2   GUOQ (25), Permutable Operators (24)
│   ├── Instruction-set design ............... 2   AshN (24), ReQISC (26)
│   ├── FT resource synthesis ................ 1   trasyn (26)
│   ├── Encoding ............................. 1   Fermihedral (24)
│   └── Programming model / analysis ......... 1   Borrowing Dirty Qubits (26)
│
├── System & memory architecture — 6 papers
│   ├── Modular / chiplet interconnect ....... 1   MECH (24)
│   ├── Full-machine architecture ............ 1   Million Qubit-Scale (24)
│   ├── Quantum memory ....................... 1   Fat-Tree QRAM (25)
│   └── (overlaps QEC architecture above) .... 3
│
├── NISQ applications & mitigation — 6 papers
│   ├── QML / circuit search ................. 2   Elivagar (24), ProxiML (24)
│   ├── Variational optimization ............. 2   Red-QAOA (24), Clapton (25)
│   ├── Measurement mitigation / calibration . 2   VarSaw (24), QuFEM (24)
│   └── Verification ......................... 1   MorphQPV (24)
│
├── Distributed / partitioned execution — 3 papers
│   ├── Circuit cutting + qubit reuse ........ 1   QRCC (25)
│   ├── Multi-party distributed primitive .... 1   COMPAS (26)
│   └── MBQC execution ....................... 1   FMCC (25)
│
├── Execution frameworks — 1 paper ........... 1   TreeVQA (26)
│
└── Classical simulation — 1 paper ........... 1   BQSim (25)
```

**Two structural observations.**
1. **Simulation is nearly absent at ASPLOS — one paper in 36.** At SC it was the largest branch (4 of 11). This is the sharpest single compositional difference between the venues, and it is the mirror image of the QEC asymmetry.
2. **QEC is 11 of 36 (31%)** and touches five distinct sub-branches. At SC, QEC was 1 of 11 and was a *reliability characterization* paper, not a decoding paper.

---

## 8. QEC decoding lineage — the deepest analysis

This section exists because Phase 1 observed that QEC decoding is dense at architecture venues and near-absent at HPC venues. The ASPLOS corpus lets that observation be tested against actual papers.

### 8.1 The finding that complicates the premise

**Within the ASPLOS main track, the decoder-microarchitecture line is exactly two papers, both before 2026.** Promatch (2024) and Micro Blossom (2025). The five QEC papers of ASPLOS 2026 contain **zero decoder-hardware designs** — they are compiler, synthesis, code-layout and platform-architecture papers. `[proceedings]` `[paper-preprint]`

The decoder-acceleration conversation continued, but elsewhere. From Micro Blossom's citation graph, the successor generation is dominated by parallel/windowed/distributed decoding, and it went to **ISCA** (SWIPER 2025, Triage 2026, Coset Ensemble 2026), **EuroSys** (Elastic QEC Decoders), **IEEE QCE**, and **Quantum**/arXiv (Snowflake, a distributed streaming decoder). `[inference]` on citation evidence.

So the accurate statement is not "QEC decoding lives at ASPLOS". It is: **ASPLOS hosted the decoder-microarchitecture line for two years and then it moved on, while ASPLOS's own QEC interest migrated one layer up the toolchain into compile-time synthesis.**

### 8.2 The two lineages, and where they collide

**Line A — capacity-limited exact decoding plus filtering (Georgia Tech, Qureshi/Das).**
LILLIPUT (ASPLOS'22, lookup tables, d=3/5 at 29/42 ns, "tables grow exponentially with the distance") → AFS (HPCA'22, union-find) → Astrea/Astrea-G (ISCA'23, exact brute force to d=7 in 456 ns) and Clique (ISCA'23, predecoder) → **Promatch (ASPLOS'24)**.
Governing idea: the main decoder has **fixed combinatorial capacity** — Hamming weight ≤ 10 and 945 matchings, which are **Astrea-G's capacity, inherited by Promatch rather than introduced by it** — and progress in d comes from *shrinking the problem to fit*. The cost is that accuracy becomes a tunable; the design cannot absorb more silicon.

**Line B — parallel exact MWPM in hardware (Yale, Zhong).**
Parity Blossom & Fusion Blossom (2023) → **Micro Blossom (ASPLOS'25)**, with Helios (the same group's FPGA union-find decoder) as acknowledged inspiration.
Governing idea, the exact opposite: **keep the algorithm exact and spend O(d³) processing units** (the paper's own notation is O, not Θ) — one vPU per vertex, one ePU per edge. Progress in d comes from the machine growing with the graph.

**The collision.** Micro Blossom cites Promatch and rejects Line A explicitly: *"they decode simple syndromes below certain Hamming weights, which implicitly assumes small code sizes and low physical error rates. For example, at d=13 and p=0.1%, their approximation leads to more than 13.9× higher logical error rate."* `[paper-preprint]`

### 8.3 The seven tensions — do not force these into agreement

**T1 — Is approximation acceptable? `DIFFERENT_REGIME`, with a specific mis-transferred number.**
Micro Blossom's "13.9× higher logical error rate at d=13, p=0.1%" is **Promatch's own worst-case figure over its sweep — and that sweep runs p = 10⁻⁴ to 5×10⁻⁴. p = 0.1% = 10⁻³ is outside the range Promatch evaluated.** At Promatch's design point (d=13, p=10⁻⁴), Promatch ‖ Astrea-G reports parity with MWPM (1.0×). The two papers are not disagreeing about the same measurement; a worst-case-over-p number has been transplanted to a p neither paper jointly evaluated. Promatch's degradation with p is real — its own data show 202× for a non-parallel configuration — but this is **not a demonstrated d=13/p=0.1% result for Promatch.** **Anyone citing the 13.9× must state its provenance.**

**T2 — What does "1 µs" mean? `TRUE_CONFLICT` of framing, which then determines the metric.**
Promatch: *"To prevent a backlog of errors, error decoding must be performed in real-time (i.e., within 1µs)"* — a **hard deadline**, with the backlog failure mode. Micro Blossom: *"a soft deadline… making the decoding a soft real-time problem"*, with the penalty modelled continuously as p_L^eff ≈ p_L(1 + L/d), and **the word "backlog" does not appear anywhere in its preprint** (verified by targeted search). `[paper-preprint]`
These are incompatible models of what the machine does while it waits, and they are not reconcilable by measurement. The consequence is methodological and large: **Promatch reports maxima and provisions for the tail; Micro Blossom reports an average.** A reader comparing "960 ns" to "800 ns" is comparing a worst case to an average.

**T3 — Speed-versus-accuracy accounting. `DIFFERENT_METRIC`.**
Micro Blossom argues that at d=21 a union-find decoder with **5× worse logical error rate beats MWPM** once idle errors accumulated during decoding are counted. Promatch's entire premise is that parity with MWPM must be preserved. Same trade-off, different objective functions (LER at the decoder output vs effective LER at the logical qubit). Neither is wrong; **any statement of the form "decoder X is better" must name the objective.**

**T4 — Latency comparability. `DIFFERENT_METRIC` plus a different evidence level.**

| | Promatch | Micro Blossom |
|---|---|---|
| Figure | 960 ns | 800 ns |
| Statistic | **maximum** | **average** |
| Provenance | cycle count × (1/250 MHz); a **top-down allotted budget**, not an observation | **measured on VMK180 board** |
| Clock | 250 MHz (synthesis-achievable) | 62 MHz (implemented) |
| I/O included | not addressed | **yes, all CPU↔accelerator I/O** |
| Accuracy at that number | 1.0× MWPM (‖AG) at p=10⁻⁴ | exactly MWPM |
| **Evidence tag** | `RTL_SYNTHESIS` + `ANALYTIC_MODEL` | `FPGA_PROTOTYPE` |

**These two numbers should never be placed side by side without all six rows.** The evidence-level difference is the largest single quality gap in the corpus.

**T5 — Where d-scaling breaks. `DIFFERENT_REGIME`.**
Micro Blossom gives a hard, dated boundary: at d=15 it needs ≥68 MHz, the FPGA delivers 43 MHz, and 867k of 900k LUTs are consumed — *"beyond the reach of commercially available FPGAs but achievable if the accelerator is implemented in ASIC"* (`PROJECTED`; **no ASIC latency figure is given and none must be reported as achieved**). Promatch has no analogous wall because it never grows with the graph; its limit is accuracy erosion. **The two designs fail in different currencies — silicon versus fidelity — so "which scales better" has no single answer.**

**T6 — What to do about a missed deadline. `DIFFERENT_REGIME`, and the most instructive tension in the corpus.**
RESCQ faces a **100 µs classical computation against a 1 µs cycle — a 100× miss, worse than the gap the decoder papers build hardware to close.** Its response is to run asynchronously every k ∈ {25,50,100,200} cycles and act on stale data. **It proposes no accelerator at all.** `[paper-preprint]`
The distinguishing variable is not the size of the miss; it is **whether the result is on the feedforward critical path.** A stale routing decision costs cycles; a late decode gates a logical T gate and (under Promatch's model) compounds. **This is the cleanest available empirical answer to "why is decoding an architecture problem": it is not the deadline, it is the non-approximability of being late.**

**T7 — Platform. `DIFFERENT_REGIME`, and unremarked by any paper in the corpus.**
Jones & Murali report trapped-ion **measurement at 400 µs** and two-qubit gates at 40 µs. Promatch and Micro Blossom both anchor everything to superconducting's 1 µs. **A 400× budget expansion would move exact MWPM at d=13 comfortably into software on a commodity CPU** — Micro Blossom's own baselines are ~5.1 µs on an M1 Max. No paper in this set makes that observation, and the trapped-ion paper does not discuss decoding at all. `OPEN_QUESTION`: whether decoding is an architecture problem may be a property of the **qubit modality** rather than of QEC.

### 8.4 The workload and computational structure, consolidated

| | Promatch | Micro Blossom | RESCQ |
|---|---|---|---|
| Syndrome rate assumed | 1 µs cycle | 1 µs cycle, "10⁶ times per second" | 1 µs cycle |
| Distances evaluated | d ≤ 13 | d = 3…15 | — |
| Logical qubits | 1 | **1** (stated as a limitation) | 13–420 program qubits |
| Algorithm | predecoder + Astrea-G exact MWPM | exact blossom, primal in SW / dual in HW | MST routing + scheduling |
| Parallelism | filter stages; serial match residue | **O(d³) PUs**, one per vertex/edge | asynchronous, every k cycles |
| Memory | 345 KB path table (monolithic) | 19–34 bits/vPU, 4 bits/ePU (**distributed into fabric**) | — |
| Communication | — | broadcast + **O(log \|E\|)** convergecast tree; PU talks only to neighbours | — |
| Bottleneck | search-space + latency-bound | latency-bound, then **resource-bound** at d=15 | latency-bound (100× miss) |
| Evidence | `RTL_SYNTHESIS` | `FPGA_PROTOTYPE` (+`PROJECTED` ASIC) | `SOFTWARE_SIMULATION` |

**The memory-architecture fork is the deepest technical divide**: Promatch keeps a monolithic 345 KB path table; Micro Blossom distributes state into the fabric with no central table. That single choice determines everything downstream about how each design scales.

### 8.5 Why decoding is an architecture problem — the corpus's own answer

Three properties, all evidenced:
1. **A hard-ish deadline on the feedforward path** — T_decode ≤ T_syndrome_cycle ≈ 1 µs, where lateness is either unbounded backlog (Promatch's model) or a continuous error-rate penalty (Micro Blossom's).
2. **Non-approximability of lateness** — T6's contrast with RESCQ shows the deadline alone is not sufficient to force hardware; being late must be *unrecoverable*.
3. **A graph problem with an irregular serial residue** — the primal phase stayed in software in Micro Blossom; Promatch's matching steps are sequentially dependent because each match mutates the syndrome. **Two independent designs, two different algorithms, the same shape of residue — that is evidence about the problem, not about the implementations.**

---

## 9. Architecture → HPC crossover analysis

**Everything in this section is `[inference]` built on the numbers in §8 and the deep dives. No paper in the corpus makes these claims. No research gap is declared.**

The question is not "could this be scaled out" — almost anything can — but **when does the classical work attached to a quantum machine stop fitting in one accelerator, and what breaks first when it does?** The frame is T(P) = W/P + C(P): work W, exploitable parallelism P, and a communication/synchronization term C(P) that must fit inside a deadline.

### 9.1 QEC decoding — four crossover conditions, in increasing severity

**(1) Logical qubit count with independent patches — the benign case, C(P) ≈ 0.**
Between lattice-surgery operations, distinct logical qubits decode independently. Scaling is replication or time-multiplexing, not latency parallelism — a **throughput** problem, and Micro Blossom already provides the mechanism (pipelining with context-switch depth up to 1024). This makes decoding a *many-accelerator* problem in the trivially parallel sense: closer to a rack of independent NICs than to an HPC job. `POSSIBLE_CROSSOVER`, but not an interesting one.

**(2) Lattice surgery — where independence breaks.**
During a merge, patches' decoding graphs fuse and the decode genuinely spans multiple logical qubits within a window. Micro Blossom names this as required future work: *"dynamic inter-block fusions… governed by an operating system-like controller."* If a merged block's graph exceeds one device, fusion must cross a device boundary **inside** the window, and C(P) enters the inner loop rather than sitting between windows. RESCQ's benchmarks (13–420 program qubits, thousands of CNOTs, each a merge) suggest merges are not rare. `OPEN_QUESTION`: at what (d, logical-qubit-count, merge-frequency) triple does this force a synchronous cross-device exchange inside a window?

**(3) Distance growth past single-device capacity — the genuinely HPC-shaped condition.**
Micro Blossom is at 867k of 900k LUTs at d=15. The chiplet codesign paper's application study uses **d=27**, whose decoding graph is ~9× the vertices of d=13 (vertex count grows cubically in d). If d ≥ 21–27 is required for algorithmic-scale error rates, **one logical qubit's decoding graph does not fit one device**, and partitioning a single graph across devices becomes mandatory — a real C(P) term under a hard deadline. `POSSIBLE_CROSSOVER`, and the most consequential one.

**(4) Bandwidth, before any compute is distributed.**
Micro Blossom's requirement that the control stack *"load and route syndrome data at Terabit/s"* is **the single most HPC-shaped number in the corpus.** Note also that the earlier decoder generation (Clique, Lazy) was motivated substantially by *bandwidth* reduction; Micro Blossom's critique of them is on accuracy, leaving the bandwidth motivation intact and unaddressed by its own design. `OPEN_QUESTION`: is the syndrome data plane a decoder-*placement* problem (cryogenic/near-fridge) or a network problem? No paper in this set addresses decoder placement; Promatch does not mention the cryostat.

### 9.2 What would prevent the transition — do not assume scale-out works

Four obstacles, each evidenced:

- **The budget has no room for a network round trip.** ~1 µs total; ~0.8 µs measured for compute plus local I/O at d=13; controller I/O separately estimated at >0.8 µs. Any multi-node scheme must **pipeline communication across windows rather than synchronize within one** — which is exactly what the speculative/parallel-window line (SWIPER, Triage, Snowflake) does, and which changes the problem from "distribute one decode" into "overlap many decodes and repair speculation."
- **The serial residue.** The primal phase stayed in software; Promatch's matching steps are sequentially dependent. Any distributed variant inherits an irregular, dynamically-allocated, sequentially-dependent phase that neither vectorises nor decomposes cleanly.
- **Exactness has a superlinear worst case** — O(d⁹) even after O(d³)-way parallelisation. Holding LER parity means you cannot escape it by approximating; approximating means accuracy becomes p- and d-dependent in the way T1 documents.
- **Determinism.** Under the hard-deadline reading, a distributed decoder needs bounded *worst-case* communication, not good average communication. Little in commodity interconnect provides that.

### 9.3 Conditions that would make the transition *unnecessary* instead

- **Slower platforms.** Trapped-ion measurement at 400 µs is a ~400× budget expansion (T7). At that budget exact MWPM at d=13 runs in software on one core with three orders of magnitude of margin.
- **Algorithm class change.** The qLDPC turn implies **BP / BP+OSD** rather than matching. Message passing over a sparse factor graph is bulk-synchronous and maps to conventional parallel machines far more naturally than blossom's dynamic forests — but it is iterative with data-dependent convergence, converting a bounded-work problem into an unbounded-iterations one. **None of the four qLDPC papers in this corpus analyses that decoder cost.** `OPEN_QUESTION`.
- **Compile-time offloading.** AlphaSyndrome and PropHunt both reduce the runtime decoder's burden by construction, pushing work from a microsecond-deadline runtime into an hours-long offline MaxSAT/MCTS search. **This is a way of avoiding the scale-out question rather than answering it — and it is where ASPLOS 2026's QEC papers actually went.**

### 9.4 Crossover by branch — summary

| Branch | Current shape | Crossover condition | Verdict |
|---|---|---|---|
| **QEC decoding** | single FPGA/ASIC, 1 logical qubit, d≤15 | d ≥ 21–27 (graph exceeds device) **or** inter-block fusion during lattice surgery | `POSSIBLE_CROSSOVER`, blocked by a ~1 µs budget with no room for a network hop |
| **Quantum simulation** | BQSim: single GPU, batched DD | memory exceeding one GPU; batch too large for device memory | **Already crossed elsewhere** — SC's Atlas (256 GPUs) and PTSBE (4×H100) are the multi-node form. ASPLOS's instance is single-device by design |
| **Compilation** | single-core, minutes-to-hours | instance size where a serial heuristic stops finishing | Naturally parallel for the *search* papers (Fermihedral's SAT, GUOQ's anytime search, trasyn's synthesis); **none of the ten reports a parallel-efficiency or scaling study of its own compiler** |
| **Modular / multi-QPU** | MECH interconnect, COMPAS multi-party | more modules than one interconnect fabric spans | `POSSIBLE_CROSSOVER`; this branch is *natively* distributed and its vocabulary already matches HPC's |
| **Full-machine architecture** | analytic/architectural models (Million Qubit, HetEC, ACQC) | — | These are **already at HPC scale in their assumptions** (10⁷–10¹² physical qubits) but evaluate with models, not machines. The crossover is in *evaluation methodology*, not problem size |

**One cross-cutting observation** `[inference]`: the compilation papers that would gain most from HPC resources are precisely those reporting single-workstation setups (Fermihedral on one core for 1–2 weeks; GUOQ on one CPU core by experimental design; Borrowing Dirty Qubits on a MacBook Air), and in each the parallel decomposition is already visible in the published algorithm. The papers whose compile-time arguments are strongest — QTurbo and PowerMove — got their speedups by **restructuring the algorithm, not by adding hardware**, and both retain a serial critical path. Which lever is better is a question none of these papers measures.

---

## 10. ASPLOS vs SC — the central comparison

### 10.1 The comparison table

| Question | **ASPLOS** | **SC** |
|---|---|---|
| **Dominant contribution** | A designed mechanism or abstraction — an ISA, an IR, a memory hierarchy, a predecoder, a PE-per-vertex accelerator | A measured cost that falls — wall-clock, energy, communication volume, occupancy, compile time |
| **Architecture novelty** | Central and expected; 11 of 36 papers propose hardware or machine organizations | Essentially absent — **zero architecture papers in 11** across two years |
| **Scale requirement** | Modest; single device, 1 logical qubit, d ≤ 15, one GPU. Scale is in the *assumptions* (10⁷ qubits) not the *evaluation* | Central; 256 GPUs, 2,304 A100s, named supercomputers (Perlmutter, Eos) |
| **Real hardware requirement** | Low for quantum hardware (mostly simulated devices); **one FPGA prototype in 36** | Low for QPUs (1 of 11 used one substantively) but **high for classical hardware** — named machines are the norm |
| **Performance evaluation** | Circuit-quality ratios (gate count, depth, T-count, fidelity, LER) dominate; wall-clock is secondary | Wall-clock, speedup, scaling curves, energy-to-solution dominate |
| **System mechanism** | Compiler passes, IRs, ISAs, accelerator microarchitecture, code layout | Runtimes, schedulers, orchestrators, partitioners, communication optimization |
| **Scientific application weight** | Low — one QML branch, shrinking to 1 paper by 2026 | Higher — SC accepted a pure dataset paper (QDockBank) with no classical hardware at all |
| **Code/artifact culture** | 61% (22/36); formal AE with 3 badges, but **badges invisible outside ACM DL**; 1 HDL artifact in 36 | 64% (7/11); no formal AE requirement; artifacts cluster in the systems-heavy papers |

### 10.2 The compilation comparison — the sharpest single result

| | SC | ASPLOS |
|---|---|---|
| Compilation papers | 3 | 10 |
| **Compile-time scalability as the central case** | **3 of 3** | **2 of 10** (QTurbo, PowerMove) |
| Partial / secondary compile-time case | 0 | 1 (trasyn) |
| Output quality is the whole case | 0 | 4 (GUOQ, ReQISC, AshN, Fermihedral) |
| A different cost model entirely | 0 | 3 (MorphQPV: QPU shots; OnePerc: real-time execution latency; Borrowing Dirty Qubits: verification time) |

**QTurbo is the one ASPLOS paper whose argument is structurally identical to SC's PARALLAX.** Measured incumbent failure: SimuQ at 11 s → 325 s → 2,111 s → 8,695 s → **23,902 s** for 20 → 100 qubits, sometimes failing outright; replacement decomposes a monolithic mixed solve into a global linear system plus local mixed systems; result 600× average, 1,600× max compile-time acceleration. *"If you moved this paper to SC, nothing about its argument would need to change."*

**Fermihedral is the sharpest inversion.** SC's move is: an exact solver exists, it times out, replace it with something polynomial. Fermihedral's move is the reverse — closed-form constructions (Jordan-Wigner, Bravyi-Kitaev) exist and cost nothing to run but give poor output, so **introduce an exact SAT solver and pay for it**, then add relaxations to reach N=18. It never compares its construction time to JW's or BK's. **In SC's terms, Fermihedral is the paper SATMAP would have been.**

**Three cost models appear at ASPLOS that do not appear in SC's compilation cohort at all:** QPU executions/shots as the scarce resource (MorphQPV: 9.3×10⁵ → 8,974 executions); hard real-time *execution* latency (OnePerc's online pass must fit inside a ~5,000-cycle photon lifetime — the deadline structure of a QEC decoder applied to a compiler's online half); and analysis/verification time as its own scaling story.

**The structural reading** `[inference]`: SC's compilation papers must justify themselves to a *performance* community, so the incumbent's wall-clock failure is the admission ticket. ASPLOS accepts a *design* argument, and compile time is then one axis among several. **Where the two venues converge is precisely where the hardware is analog and continuous** (QTurbo on QuEra Aquila, PowerMove on atom movement): there the compiler output is a schedule over continuous parameters, the search is genuinely large, and the argument reverts to SC's shape.

### 10.3 Simulation — the mirror-image asymmetry

SC's largest branch (4 of 11) is ASPLOS's smallest (1 of 36), and vice versa for QEC.

**BQSim vs SC's simulation papers.** BQSim is single-GPU, batched decision-diagram simulation; its contribution is a data-structure and batching insight that makes an irregular DD structure GPU-friendly. SC's Atlas is 256 GPUs on Perlmutter with an ILP that minimizes inter-node communication; PTSBE is 4×H100 with 6,668 GPU-hours. **The difference is not quality — it is that SC's simulation contribution is inseparable from the distributed machine, and ASPLOS's is inseparable from the device's memory system.** Communication is the object of optimization at SC; it does not appear in BQSim's argument at all. `[inference]`

### 10.4 Two lists this programme should keep separate

**(a) ASPLOS contributions that would be weak at SC as they stand** `[inference]`:
Instruction-set proposals (AshN, ReQISC) — no cost model at scale. Full-machine architecture papers evaluated by analytic model (Million Qubit-Scale, HetEC, ACQC, Fat-Tree QRAM) — SC expects measurement on a named machine. NISQ mitigation and QML papers (Elivagar, Clapton, VarSaw, ProxiML) — SC's Pathway 4 could admit them only with a scarce-resource-consumption argument, which none makes. Output-quality-only compilation (GUOQ, Fermihedral) — SC would ask for the wall-clock.

**(b) ASPLOS ideas that acquire an SC shape once scale is added** `[inference]`, `POSSIBLE_CROSSOVER` only:
QEC decoding at d ≥ 21–27 or under lattice-surgery fusion, where a single graph exceeds a device (§9.1). The Terabit/s syndrome data plane, which is a data-movement problem at HPC scale before any compute is distributed. Multi-QPU execution (COMPAS, MECH) — natively distributed, and its vocabulary already matches HPC's. Compiler search parallelization for the papers that currently run single-core. **Each of these is a condition, not a claim, and none is asserted as unaddressed.**

---

## 11. Venue gaps — `VENUE_GAP` only

**`VENUE_GAP ≠ RESEARCH_GAP`.** These are branch-presence differences between two venues' main tracks, nothing more.

| Branch | ASPLOS 24–26 | SC 24–25 | Reading |
|---|---|---|---|
| **QEC decoding (systems)** | 2 decoder papers + 9 QEC-adjacent | 0 (1 QEC *reliability characterization*) | Confirms Phase 1's observation, but see §8.1 — the ASPLOS decoder line is only two papers and has since moved to ISCA |
| **Fault-tolerant architecture** | 6+ | 0 | Machines that do not exist; evaluated analytically. SC's evaluation norms may not accommodate this |
| **Control architecture** | present (via QEC/platform papers) | 0 | — |
| **Modular / multi-QPU** | 3 (MECH, COMPAS, chiplet codesign) | 1 (DQTetris, compilation only) | Both venues thin; ASPLOS has the interconnect papers |
| **Quantum networking architecture** | 0 in this corpus | 0 | Neither venue; lives at ICDCS/SIGMETRICS per Phase 1 |
| **Reliability** | 1 (chiplet defects) | 1 (radiation/surface codes) | Both thin, different framings |
| **Distributed / multi-node simulation** | **0** | **4** | The mirror image — SC's densest branch is absent from ASPLOS |
| **Resource management / QPU scheduling** | 1 (RESCQ, real-time not batch) | 1 (Qonductor, cloud orchestration) | Both thin; the *fleet-scheduling* form is at OSDI per Phase 1 |
| **Application / dataset papers** | 0 | 2 (LEXIQL, QDockBank) | SC's Pathway 4 has no ASPLOS equivalent |

**The two gaps worth stating precisely:**
1. **Multi-node quantum simulation is absent from ASPLOS's main track** in this window, while being SC's largest branch. Plausible readings, none chosen: the contribution requires a machine ASPLOS reviewers do not expect; the single-device version is the natural ASPLOS framing; the work is being done and submitted elsewhere.
2. **Dataset and application papers have no ASPLOS analogue.** SC accepted a paper with no classical hardware at all (QDockBank). ASPLOS's boundary appears not to extend that far — every one of the 36 has an identifiable mechanism. `[inference]`

---

## 12. Artifact / code matrix

### 12.1 Summary

**22 of 36 (61%) have a clearly public artifact**; 24 of 36 (67%) counting two `PARTIAL`. SC was 7 of 11 (64%). **The two venues are statistically indistinguishable on artifact rate, despite ASPLOS running a formal Artifact Evaluation process and SC not requiring one.**

By year: **2024 = 12/14 (86%)**, **2025 = 5/10 (50%)**, **2026 = 7–8/12 (58–67%)**. The 2025 dip is driven by composition — the three deferred 29V4 papers (Clapton, QRCC, FMCC) released nothing, and three architecture proposals (Fat-Tree QRAM, HetEC) have no runnable system to deposit.

### 12.2 Artifact by branch — the dominant variable

| Branch | With artifact | Rate |
|---|---|---|
| **QEC decoders / synthesis** | Promatch, Micro Blossom, PropHunt, AlphaSyndrome, RESCQ | **5/5 = 100%** |
| NISQ apps / mitigation / simulation | VarSaw, QuFEM, Elivagar, Red-QAOA, ProxiML, MorphQPV, BQSim, TreeVQA, COMPAS | **9/12 = 75%** |
| Compilers / synthesis | Permutable, MECH, OnePerc, Fermihedral, GUOQ, QECC-Synth, ReQISC, trasyn (+ Borrowing Dirty Qubits partial) | **8/12 = 67%** |
| **Architecture proposals** | only chiplet codesign, and only as a demo | **0/7 clear (1/7 partial)** |

The 0/7 for architecture proposals is a **structural** fact — Million Qubit, Fat-Tree QRAM, HetEC, Trapped-Ion, ACQC and iSwitch all propose machines that do not exist, and their evaluation is an analytic or architectural model. But note the asymmetry: **RESCQ and BQSim show architectural simulators are perfectly depositable when authors treat them as the deliverable.** The 0/7 is a choice about what counts as the artifact, not an impossibility. `[inference]`

### 12.3 What kind of artifacts — the finding that matters more than the rate

Of the ~22 artifacts, **roughly 16 are Python or C++ simulation and compiler code.** The non-Python exceptions: BQSim (C++/CUDA), RESCQ (C++ simulator), GUOQ (Java + two Docker images, shipping the *baseline* too), Promatch (C++/MPI), and Micro Blossom (Scala/SpinalHDL + Rust).

**Exactly one hardware description exists in 36 papers.** Two papers make FPGA claims — Promatch and Micro Blossom — and **only Micro Blossom ships the HDL.** `[code]` Promatch's repository is C++/CMake with **no `.v`, `.sv`, `.vhd`, `.scala` or `.tcl` files at all**; its Kintex UltraScale+ synthesis result (Table 7: 3% LUT, 1% FF, 250 MHz) is not reproducible from the artifact, and its README scopes reproduction to Sections 6.1–6.2 only.

**This is the headline artifact finding: an architecture conference produces essentially the same artifact profile as an HPC conference — software simulation, not hardware.** The venue's identity does not propagate into what its quantum authors release.

### 12.4 Two repositories that diverge from their papers — in opposite directions

**Micro Blossom's README exceeds its paper.** `[code]` `[documentation]` The README claims **"367 ns using Micro Blossom on FPGA (VMK180)"** vs 5.1 µs for Parity Blossom = **"14x reduction"**; **"real-time decoding of at most 110 logical qubits (d=9, p=0.001)"** at **"1 million measurement rounds per second"**; and **"1.4k LUT per logical qubit"** vs Helios's 2.1k. **None of 367 ns, 110 logical qubits, 1M rounds/s, or 1.4k LUT/logical-qubit appears in the arXiv v1**, which instead states *"Micro Blossom as reported here supports a single logical qubit."*
Characterization: **not a contradiction — a different, more favourable operating point plus a scope extension.** 367 ns is at d=9; 0.8 µs is at d=13, and latency grows with distance, so both are consistent numbers about different configurations with different baselines. The materially divergent item is **110 logical qubits**, which extends past the paper's own single-logical-qubit caveat into a multiplexing regime the paper does not evaluate. **Anyone citing "367 ns" or "110 logical qubits" is citing the repository, not the peer-reviewed paper, and should say so.**

**Promatch's repository is weaker than its paper** — the FPGA synthesis claim has no corresponding artifact (above).

Together these show that **repo-level cross-checking changes the reading of a hardware claim in both directions**, and that AE badges would not catch either: *Artifacts Functional* asks whether the artifact does what the artifact says, not whether it covers every claim in the paper. `[inference]`

### 12.5 ASPLOS Artifact Evaluation — process and visibility

`[documentation]` **Three badges, not four**: *Artifact Available*, *Artifact Functional* (2024 wording: "Artifact Evaluated — Functional"), *Results Reproduced* (2026 wording: "Results Replicated"). **There is no "Reusable" badge at ASPLOS.**
**AE is voluntary in all three years**, verbatim and identically worded across the 2024/2025/2026 AEC sites: *"Note that this submission is voluntary and will not influence the final decision regarding the papers."*
**Badge status per paper is not publicly determinable outside ACM DL** — the AEC sites state badges are "printed on the papers themselves and available as meta information in the ACM Digital Library", and no AEC report, statistics, or badged-paper list is published for any year. **Badge status is therefore `UNKNOWN` for all 36 papers, and that invisibility is itself a finding.**
Usable proxies for AE participation, all verified: an Artifact Appendix in the preprint (MECH, Red-QAOA, OnePerc, Borrowing Dirty Qubits, AlphaSyndrome); an AE-named release tag (Fermihedral `v1.0.0-AE`, PropHunt `v0.1 "ASPLOS Artifact Evaluation"`); a Zenodo record self-labelled for AE (ReQISC "(for ASPLOS'26 AE)"). **≥9 of 36 show positive evidence of AE participation — a floor, not a rate.**

> **Search caution for future censuses:** three groups deposit on Zenodo without linking it from the preprint (QECC-Synth, ProxiML, and effectively OnePerc, whose link lives only in the accepted version's appendix on NSF PAR). **A search that reads only preprints undercounts ASPLOS's artifact rate by roughly 3 papers — about 8 percentage points.**

### 12.6 The matrix

| Paper | Yr | Status | URL | Verdict |
|---|---|---|---|---|
| Micro Blossom | 25 | `PUBLIC_CODE` | github.com/yuewuo/micro-blossom | **`CONSISTENT`** — only real HDL artifact in the corpus |
| BQSim | 25 | `PUBLIC_CODE` | github.com/IDEA-CUHK/BQSim | **`CONSISTENT`** — C++/CUDA, DDs, 16 MQT-Bench circuits, baselines included |
| GUOQ | 25 | `PUBLIC_CODE` | github.com/qqq-wisc/guoq + Zenodo 14055562 | **`CONSISTENT`** — ships baseline Docker image too |
| RESCQ | 25 | `PUBLIC_CODE` | github.com/5ayam5/Realtime-Scheduling-… + Zenodo 14769159 | **`CONSISTENT`** |
| AlphaSyndrome | 26 | `PUBLIC_CODE` | github.com/acasta-yhliu/asyndrome + Zenodo 18291927 | **`CONSISTENT`** |
| PropHunt | 26 | `PUBLIC_CODE` | github.com/jviszlai/PropHunt + Zenodo 17945387 | **`CONSISTENT`** — release tagged for AE |
| COMPAS | 26 | `PUBLIC_CODE` | github.com/kunliu7/Distributed-Q-Algo | **`CONSISTENT`** — evaluated configs are CLI args |
| TreeVQA | 26 | `PUBLIC_CODE` | github.com/isaachyw/TreeVQA + Zenodo 17945742 | **`CONSISTENT`** |
| Fermihedral | 24 | `PUBLIC_CODE` | github.com/acasta-yhliu/fermihedral | **`CONSISTENT`** — release `v1.0.0-AE` |
| MorphQPV | 24 | `PUBLIC_CODE` | github.com/JanusQ/MorphQPV + Zenodo 10877687 | **`CONSISTENT`** |
| Red-QAOA | 24 | `PUBLIC_CODE` | github.com/meng-ubc/Red-QAOA | **`CONSISTENT`** |
| Elivagar | 24 | `PUBLIC_CODE` | github.com/SashwatAnagolum/Elivagar | **`CONSISTENT`** |
| MECH | 24 | `PUBLIC_ARTIFACT` | Zenodo 10.5281/zenodo.10544117 | **`CONSISTENT`** |
| Promatch | 24 | `PUBLIC_CODE` | github.com/nargesalavi/Promatch | **`PARTIAL_MATCH`** — **no HDL for the FPGA claim** |
| trasyn | 26 | `PUBLIC_CODE` | github.com/haoty/trasyn | `PARTIAL_MATCH` — no benchmark/eval scripts |
| QuFEM | 24 | `PUBLIC_CODE` | github.com/JanusQ/QuFEM | `PARTIAL_MATCH` |
| VarSaw | 24 | `PUBLIC_CODE` | github.com/siddharthdangwal/VarSaw | `PARTIAL_MATCH` |
| Permutable Operators | 24 | `PUBLIC_CODE` | github.com/ata-pattern/ata-pattern | `PARTIAL_MATCH` — only the small-circuit solver |
| Chiplet codesign | 24 | `PARTIAL` | github.com/SophLin/superstabilizer_demo | `PARTIAL_MATCH` — demo only |
| QECC-Synth | 25 | `PUBLIC_ARTIFACT` | Zenodo 14061096 | `INSUFFICIENT_EVIDENCE` — 1.7 GB, not linked from preprint |
| OnePerc | 24 | `PUBLIC_ARTIFACT` | Zenodo 10799879 | `INSUFFICIENT_EVIDENCE` |
| ProxiML | 24 | `PUBLIC_ARTIFACT` | Zenodo 10791711 | `INSUFFICIENT_EVIDENCE` — 896.7 MB zip |
| ReQISC | 26 | `PUBLIC_ARTIFACT` | Zenodo 18163249 | `INSUFFICIENT_EVIDENCE` — author field "Anonymous" |
| Borrowing Dirty Qubits | 26 | `PARTIAL` | — | `INSUFFICIENT_EVIDENCE` — Artifact Appendix with **no URL or DOI** |
| Million Qubit-Scale · Fat-Tree QRAM · HetEC · Clapton · QRCC · FMCC · PowerMove · QTurbo · ACQC · Trapped-Ion · iSwitch · AshN | — | `NO_PUBLIC_ARTIFACT_FOUND` | — | — |

`NO_PUBLIC_ARTIFACT_FOUND` means all five search steps were exhausted, **not** that code does not exist. PowerMove states *"We will open-source our code later"* — not yet delivered as of this census.

> **False-attribution warnings.** TreeVQA's repo vendors a `clapton` module (shared co-author Gokul Ravi) — this is **not** Clapton's own artifact. And arXiv 2510.19442 ("Accelerating Fault-Tolerant Quantum Computation with Good qLDPC Codes", Zhang/Zhu/Li) is **not** ACQC (Cho/Jeong et al., SNU) despite near-identical titling.

---

## 13. Recommended deep-dive papers

Selected by: representativeness of a branch; influence on later work; recency; public artifact; substantial systems contribution; HPC-extension potential; and value as an SC comparison. Six papers, with the reason for each.

### 1. **Micro Blossom** (ASPLOS 2025) — the corpus's single most important paper for this programme
**Why:** the only paper in 36 with a *measured* hardware result and a shippable hardware description; the cleanest speed-at-equal-accuracy claim in the corpus (logically equivalent to exact MWPM, verified against a known exact decoder); and the source of the corpus's most HPC-shaped number, the **Terabit/s** syndrome data plane.
**Mechanism to learn:** O(d³) processing units — one vPU per decoding-graph vertex, one ePU per edge — with a broadcast/convergecast tree of O(log|E|) depth, primal phase in software and dual phase in fabric, and round-wise fusion for streaming. The memory design is the deep lesson: **state distributed into the fabric (19–34 bits/vPU) rather than a monolithic table**, which is what lets it scale with the graph.
**Evidence:** `FPGA_PROTOTYPE` (Xilinx Versal VMK180, 62 MHz, measured, **I/O included**), with `PROJECTED` for the ASIC remark. Artifact `CONSISTENT`.
**Watch for:** 0.8 µs is an **average**, not a worst case; the d=15 wall (needs ≥68 MHz, delivers 43 MHz, 867k/900k LUTs); the 8× is **not a like-for-like comparison** — Micro Blossom's own figure includes all CPU↔accelerator I/O while the baseline's latency excludes the baseline's own I/O, which the paper transparently notes (the asymmetry works against Micro Blossom, but it is still an asymmetry); and the README's extra claims (§12.4).

### 2. **Promatch** (ASPLOS 2024) — the counter-design, and required for reading Micro Blossom
**Why:** it is the other half of the field's central design argument (shrink the problem vs grow the machine), and reading the two together is the only way to see that the "13.9×" figure is a mis-transferred number (§8.3 T1).
**Mechanism to learn:** adaptive predecoding — filter syndromes so the exact stage's fixed combinatorial capacity (Hamming weight ≤ 10, 945 matchings — Astrea-G's, inherited) suffices; a 345 KB monolithic path table.
**Evidence:** `RTL_SYNTHESIS` + `ANALYTIC_MODEL` — the 960 ns is a cycle count divided by an assumed 250 MHz, **not a measurement**, and it originates as a *budget allotted top-down* from the syndrome-cycle deadline rather than as an observed latency. Artifact `PARTIAL_MATCH`: **the FPGA claim has no HDL.**

### 3. **BQSim** (ASPLOS 2025) — the one simulation paper, and the direct SC comparison
**Why:** it is the only ASPLOS quantum-simulation paper in 36, and comparing it against SC's Atlas and PTSBE is the cleanest way to see how the two venues frame an identical class of contribution (§10.3).
**Mechanism to learn:** batching many circuits against a shared decision-diagram representation on GPU; making an irregular, pointer-heavy DD structure GPU-friendly; BQCS-aware gate fusion and task-graph execution.
**Evidence:** `REAL_HARDWARE` (classical GPU), `SOFTWARE_SIMULATION` (quantum). Artifact `CONSISTENT` — C++/CUDA with both Qiskit and cuQuantum baselines in-repo.

### 4. **QTurbo** (ASPLOS 2026) — the one ASPLOS compilation paper that argues like an SC paper
**Why:** it is the single existence proof that an SC-shaped compile-time-scalability argument is publishable at ASPLOS, which makes it the template for anyone trying to move work between the two venues.
**Mechanism to learn:** decomposing a monolithic mixed solve into a global linear system plus local mixed systems; measured incumbent failure (SimuQ 11 s → 23,902 s across 20→100 qubits).
**Evidence:** `REAL_HARDWARE` (QuEra Aquila) for the error result; `SOFTWARE_SIMULATION` for the compile-time scaling. Artifact `NO_PUBLIC_ARTIFACT_FOUND`.

### 5. **RESCQ** (ASPLOS 2025) — the negative control for the whole QEC-architecture thesis
**Why:** it faces a **100× deadline miss** — worse than the gap the decoder papers build hardware to close — and responds with asynchrony and stale data rather than an accelerator. It is the cleanest available evidence that **the deadline alone does not make a problem an architecture problem; non-approximability of lateness does** (§8.3 T6, §8.5).
**Mechanism to learn:** running the classical computation every k ∈ {25,50,100,200} cycles and acting on stale routing decisions.
**Evidence:** `SOFTWARE_SIMULATION`. Artifact `CONSISTENT`.

### 6. **COMPAS** (ASPLOS 2026) — the natively distributed branch
**Why:** a distributed multi-party primitive is the one ASPLOS branch whose vocabulary already matches HPC's, and it is the most plausible near-term crossover candidate that is not QEC.
**Mechanism to learn:** distributing a SWAP test across parties; teledata vs telegate methods; analytical fidelity bounds.
**Evidence:** `SOFTWARE_SIMULATION`. Artifact `CONSISTENT` — evaluated configurations appear directly as CLI arguments, with SLURM batch scripts.

**Deliberately not recommended:** the two abstract-only papers (Million Qubit-Scale, ACQC) — not readable; the NISQ mitigation cluster (VarSaw, Clapton, ProxiML) — least transferable to HPC systems work; and AshN/ReQISC — instruction-set design with no cost model to learn from.

---

## 14. False positives and borderline cases

### 14.1 Excluded — vocabulary collisions

| Paper | DOI | Why considered | Why excluded |
|---|---|---|---|
| **It Takes Two to Entangle** | `10.1145/3779212.3790178` | "Entangle" in the title; the single most quantum-sounding title in all ten volumes | NYU + ByteDance **distributed-systems/LLM** paper. No quantum affiliation among authors; no quantum terminology in the record; references are model parallelism and distributed DL. Session 5A "Generative Model Serving". **The only metaphorical use of a quantum keyword in the corpus** |
| Efficient Microsecond-scale Blind Scheduling with Tiny Quanta | `10.1145/3620665.3640381` | "Quanta" | Scheduling *quanta* (time slices), not quantum |
| MVQ: …Masked Vector Quantization | `10.1145/3669940.3707268` | "Quantization" | DNN numeric quantization |
| COMET: Towards Practical W4A4KV4 LLMs Serving | `10.1145/3676641.3716252` | "Quantization" | LLM numeric quantization |
| M²XFP: A Metadata-Augmented Microscaling Data Format | `10.1145/3779212.3790185` | "Quantization" | Numeric format |
| SNIP: Adaptive Mixed Precision for Subbyte LLM Training | `10.1145/3779212.3790223` | Mixed precision | Not quantum |
| MoC-System: Fault Tolerance for Sparse MoE Training | `10.1145/3676641.3716006` | "Fault tolerance" | Classical fault tolerance |
| Fault Escaping: DPU Platform with Mutual Assisted VM Recovery | `10.1145/3676642.3736124` | "Fault" | Classical fault tolerance |
| PrioriFI: More Informed Fault Injection for Edge Neural Networks | `10.1145/3779212.3790204` | "Fault injection" | Classical FI — note SC's Surface Codes paper *was* a quantum FI paper, so this is a genuine near-miss |
| TiNA: Tiered Network Buffer Architecture for Chiplet-based CPUs | `10.1145/3760250.3762224` | "Chiplet" — MECH is a quantum chiplet paper | Classical chiplets |
| Compositional AI Beyond LLMs: Neuro-Symbolic-Probabilistic Architectures | `10.1145/3760250.3762235` | "Probabilistic" | Not quantum |
| CHEHAB RL; CEMU | (Session 9B) | Sit **inside** the session named "Quantum & Emerging Computing" | FHE optimization and computational-storage emulation. **The session-name trap, ASPLOS 2026 edition** — 2 of 4 papers in a quantum-named session are not quantum |

### 14.2 Borderline — included, with the argument against recorded

| Paper | Case for | Case against |
|---|---|---|
| **Fat-Tree QRAM** (25) | A memory-architecture paper — bandwidth, parallel queries, a fat-tree topology; squarely `FUTURE_WORKLOAD` | QRAM is a hypothetical device; nothing is built, and the evaluation is analytic. Kept because the *architecture* reasoning is exactly what an HPC memory-systems researcher would recognize |
| **Borrowing Dirty Qubits** (26) | A programming-model and program-analysis contribution with an SMT scaling story | Closer to PL than to systems; its cost model is its own verification time. Kept as `BORDERLINE` |
| **MorphQPV** (24) | Verification with a real cost model — QPU executions reduced 9.3×10⁵ → 8,974 | Verification is not obviously architecture. Kept because the scarce resource it optimizes (QPU shots) is a genuine Quantum-HPC resource |
| **Elivagar / ProxiML** (24) | Circuit search and classifier construction for real device constraints | Nearest to pure QML; minimal systems content. Kept for completeness of the NISQ branch, flagged as least transferable |
| **iSwitch** (26) | Selective encoding as a NISQ→FTQC transition mechanism, with architecture implications | Device/ion-trap-specific. Kept |
| **AshN / ReQISC** | Instruction-set design is architecture in the most literal sense | No cost model, no compile-time or wall-clock argument. Kept, and flagged in §10.4(a) as weak for SC |

### 14.3 The near-miss that is *not* in this corpus

**VarSaw and Permutable Operators are in the 28th ASPLOS Volume 4** (proceedings year **2023**), presented at ASPLOS 2024. They are counted in the ASPLOS 2024 **program** but fall outside the 2024–2026 **proceedings** window. Both are reported; the distinction is stated everywhere they appear.

---

## 15. Implications for the ICS and HPCA censuses

### 15.1 Which venue next — recommend **HPCA**

The research queue currently puts ISC then ISCA ahead of HPCA, with ICS in Wave 2. **This census argues for moving HPCA ahead of ICS**, for three reasons:

1. **HPCA is the natural control for the ASPLOS result.** The single sharpest finding here is that ASPLOS's quantum papers argue *design*, not *cost* (§10.1). HPCA is the architecture venue whose name most explicitly claims performance ("High-Performance Computer Architecture"), so it is the direct test of whether that is an ASPLOS trait or an architecture-community trait. Phase 1 found HPCA went from **one** main-track quantum paper in 2024 to two dedicated sessions in 2025 and 2026 — a sharper change than ASPLOS's, and it needs the same volume-level scrutiny this census applied.
2. **The QEC decoder line is where HPCA can settle a question this census opened.** §8.1 found the ASPLOS decoder line is two papers and then moves to ISCA. Phase 1 identified HPCA 2026's *"Fully Parallelized BP Decoding for QLDPC Codes"* (NC State/PNNL, **with public code**) and a cryogenic predecoder (Pinball). Those are precisely the qLDPC/BP decoders whose real-time cost **no paper in the ASPLOS corpus analyses** (§9.3). HPCA is where that gap in the ASPLOS record can be filled with evidence.
3. **ICS's value is higher after both architecture venues are done.** ICS is an HPC venue; reading it against SC alone is less informative than reading it against SC *plus* a completed architecture picture.

### 15.2 Questions to carry into HPCA specifically

1. **Apply the volume check first.** Does HPCA have an ASPLOS-style multi-volume or deferred-presentation structure? If not, its counts are simpler — but verify rather than assume, because this census's largest methodological finding came from that structure.
2. **Do not census from session names, and do not trust a program page to be complete.** A program-based census of ASPLOS 2024 finds 9 of its 14 quantum papers — the page truncates after Session 8C, so the other five have no locatable session and cannot be shown absent either (`STATUS_UNCLEAR`). In the opposite direction, ASPLOS 2026 put 2 non-quantum papers inside a quantum-named session. Sweep the volumes, and apply the deferral rule.
3. **Run the compile-time-argument tally** (§10.2) on HPCA's compilation papers. SC = 3/3, ASPLOS = 2/10. A third data point turns a two-venue contrast into a pattern.
4. **Check the hardware evidence level of every headline latency.** This census found a `RTL_SYNTHESIS` number (960 ns) and an `FPGA_PROTOTYPE` number (800 ns) being compared across papers as if commensurable, one a maximum and the other an average. HPCA will have more hardware claims than ASPLOS; the same discipline is required.
5. **Test the decoder-lineage finding.** Does HPCA carry the parallel/windowed decoder line that left ASPLOS after 2025? If ISCA and HPCA both do, the ASPLOS departure is a venue-preference finding rather than a field-wide one.
6. **Check artifact rate and artifact *kind*.** ASPLOS: 61%, with exactly one HDL artifact in 36. If HPCA — a more hardware-centric venue — also produces almost no HDL, that is a field-level observation about quantum-architecture reproducibility.

### 15.3 Questions for ICS when it comes

1. ICS 2026 ran a five-paper session named "Quantum Computing" (Phase 1) — **larger than either SC year.** Is ICS becoming the HPC venue where this work lands?
2. Does ICS's quantum work look like SC's (cost arguments, multi-node) or like ASPLOS's (mechanism arguments, single-device)? ICS sits between them institutionally and is the natural place to see which norm dominates.
3. Phase 1 found ICS's CFP barely mentions quantum while its program has a dedicated session — the inverse of the CC/PPoPP pattern. Verify against the proceedings.

### 15.4 A methodological note to carry forward

**Two denominators, always.** This census had to distinguish proceedings year from program year, and the difference is 16–24 papers per year. Any venue with multiple submission cycles may have the same structure. **Report both, and never mix them.**

---

## 16. Sources

All URLs checked 2026-09-06.

**Volume structure and enumeration**
[Crossref REST API](https://api.crossref.org/) (all volume enumeration, container-titles, page ranges, author lists) · [ASPLOS 2024 CFP — the deferral rule, verbatim](https://www.asplos-conference.org/asplos2024/cfp/index.html) · [ASPLOS 2025 CFP](https://www.asplos-conference.org/asplos2025/cfp.html) · [ASPLOS 2026 CFP](https://www.asplos-conference.org/asplos2026/cfp/index.html) · [SIGARCH — Evaluating the New ASPLOS Review Process (submission statistics)](https://www.sigarch.org/evaluating-the-new-asplos-review-process/) · [dblp: ASPLOS](https://dblp.org/db/conf/asplos/index.html)

**Official programs**
[ASPLOS 2024 main program](https://www.asplos-conference.org/asplos2024/main-program/index.html) *(truncates after Session 8C)* · [ASPLOS 2025 program](https://www.asplos-conference.org/asplos2025/program.html) *(note: the trailing-slash URL `asplos2025/program/` serves the 2026 program)* · [ASPLOS 2026 program](https://www.asplos-conference.org/asplos2026/program/index.html)

**Artifact Evaluation**
[ASPLOS'24 AEC](https://sites.google.com/view/asplos24aec/home) · [ASPLOS'25 AEC](https://sites.google.com/view/asplos25aec/home) · [ASPLOS'26 AEC](https://sites.google.com/view/asplos26aec/home)

**QEC decoding and architecture**
[Micro Blossom arXiv:2502.14787](https://arxiv.org/abs/2502.14787) · [micro-blossom repo](https://github.com/yuewuo/micro-blossom) · [Promatch repo](https://github.com/nargesalavi/Promatch) · [chiplet codesign arXiv:2305.00138](https://arxiv.org/html/2305.00138v3) · [superstabilizer_demo](https://github.com/SophLin/superstabilizer_demo) · [HetEC arXiv:2411.03202](https://arxiv.org/html/2411.03202v1) · [QECC-Synth Zenodo 14061096](https://zenodo.org/records/14061096) · [AlphaSyndrome repo](https://github.com/acasta-yhliu/asyndrome) · [PropHunt repo](https://github.com/jviszlai/PropHunt) · [PropHunt Zenodo](https://zenodo.org/records/17945386) · [RESCQ repo](https://github.com/5ayam5/Realtime-Scheduling-for-Continuous-Angle-QEC-Architectures) · [Flexion/iSwitch arXiv:2504.16303](https://arxiv.org/html/2504.16303v1) · [Trapped-ion arXiv:2510.23519](https://arxiv.org/html/2510.23519)

**Simulation, architecture, distributed execution**
[BQSim repo](https://github.com/IDEA-CUHK/BQSim) · [BQSim published PDF (author-hosted)](https://tsung-wei-huang.github.io/papers/2025-asplos.pdf) · [MECH arXiv:2305.05149](https://arxiv.org/pdf/2305.05149) · [MECH Zenodo 10544117](https://zenodo.org/records/10544117) · [Fat-Tree QRAM arXiv:2502.06767](https://arxiv.org/html/2502.06767v1) · [COMPAS arXiv:2511.23434](https://arxiv.org/html/2511.23434v2) · [COMPAS repo](https://github.com/kunliu7/Distributed-Q-Algo) · [QRCC arXiv:2312.10298](https://arxiv.org/html/2312.10298v3) · [QRCC camera-ready](https://xzt102.github.io/publications/QRCC_ASPLOS2024.pdf) · [TreeVQA repo](https://github.com/isaachyw/TreeVQA) · [FMCC PDF](https://people.cs.pitt.edu/~zhangyt/research/fmcc.asplos.24b.pdf)

**Compilation**
[PowerMove arXiv:2411.12263](https://arxiv.org/abs/2411.12263) · [QTurbo arXiv:2506.22958](https://arxiv.org/html/2506.22958v1) · [trasyn arXiv:2503.15843](https://arxiv.org/pdf/2503.15843v2) · [trasyn repo](https://github.com/haoty/trasyn) · [ReQISC arXiv:2511.06746](https://arxiv.org/pdf/2511.06746v2) · [ReQISC Zenodo 18163249](https://zenodo.org/records/18163249) · [Borrowing Dirty Qubits arXiv:2508.17190](https://arxiv.org/pdf/2508.17190) · [GUOQ arXiv:2411.04104](https://arxiv.org/pdf/2411.04104) · [guoq repo](https://github.com/qqq-wisc/guoq) · [GUOQ Zenodo 14055562](https://zenodo.org/records/14055562) · [AshN arXiv:2312.05652](https://arxiv.org/pdf/2312.05652) · [OnePerc arXiv:2403.01829](https://arxiv.org/html/2403.01829v1) · [OnePerc Zenodo 10799879](https://zenodo.org/records/10799879) · [Fermihedral arXiv:2403.17794](https://arxiv.org/html/2403.17794v1) · [fermihedral repo](https://github.com/acasta-yhliu/fermihedral) · [MorphQPV camera-ready](https://fiction-zju.github.io/papers/ASPLOS2024-b.pdf) · [MorphQPV repo](https://github.com/JanusQ/MorphQPV)

**NISQ applications**
[VarSaw arXiv:2306.06027](https://arxiv.org/abs/2306.06027) · [VarSaw repo](https://github.com/siddharthdangwal/VarSaw) · [Red-QAOA arXiv:2407.14490](https://arxiv.org/html/2407.14490v1) · [Red-QAOA repo](https://github.com/meng-ubc/Red-QAOA) · [Elivagar repo](https://github.com/SashwatAnagolum/Elivagar) · [Clapton arXiv:2406.15721](https://arxiv.org/html/2406.15721v1) · [QuFEM repo](https://github.com/JanusQ/QuFEM) · [ProxiML Zenodo 10791710](https://zenodo.org/records/10791710) · [ata-pattern repo](https://github.com/ata-pattern/ata-pattern)

**Group pages consulted**
[SNU-HPCS repositories](https://github.com/orgs/SNU-HPCS/repositories) · [SNU HPCS ASPLOS 2026 news](https://hpcs.snu.ac.kr/two-papers-are-accepted-to-asplos-2026/) · [Yongshan Ding publications](https://www.yongshanding.com/publications.html) · [Xulong Tang publications](https://xzt102.github.io/publications.html) · [FICTION-ZJU publications](https://fiction-zju.github.io/publication/) · [Gushu Li publications](https://sites.google.com/view/gushuli/publication)

---

## Appendix A — Verification pass record

**Draft and verification were separated deliberately.** The census in §§1–16 was written first. It was then handed to an independent adversarial verification pass whose brief was to attack, not confirm: re-derive every headline number from primary sources, and report any claim the evidence does not carry. This appendix records what that pass found, because a census that reports only its conclusions and not its own error rate is asking to be trusted on faith.

**Result: 23 claims tested, 18 confirmed unchanged, 5 corrected.** Two of the five were material.

### A.1 Corrections applied

| # | Severity | Claim as drafted | What the evidence actually supports | Where fixed |
|---|---|---|---|---|
| **C1** | **Material** | "5 of its 14 quantum papers **sat outside the two quantum-named sessions**" — presented as an established program fact, and used to make the 2024 undercount a story about session naming. | The five **cannot be located on the ASPLOS 2024 program page, and cannot be shown absent from the program either**, because that page truncates after Session 8C. Session placement is `STATUS_UNCLEAR`. The undercount is real (9 vs 14) but has two causes: an incomplete program page, and one deferred paper (Permutable Operators, 28V4/2023). | §1.1, F2, §3 |
| **C2** | **Material** | "Papers presented (program) \| ~193" listed in a program row, and program shares of 7.3% / 5.4% / 7.1% presented alongside proceedings shares as if equally grounded. | ~193 is **volume arithmetic**, not a program count: 170 enumerated (29th V1–V3) plus an un-enumerated 28th-V4 cohort. Marked `TOTAL_COUNT_UNVERIFIED`. The table now separates *proceedings* (firmer), *program* (derived) and *what the published program shows* (block C). This was the same conflation the census warns against in its own F1. | §1.1, F3, §2.3, §6.1 |
| **C3** | Provenance | "per-volume item counts reconcile exactly … DOI suffix ranges are contiguous and were verified." | Crossref exposes **no volume-level item count**, and its `container-title` filter is **silently ignored** — no count may be taken from it. Counts came from date-windowed prefix queries with `cursor=*`, filtered client-side on DOI stem, read through `WebFetch`. Item-level records were retained **only for the 2024 volumes**; 2025/2026 totals are single-source. Also, 29V2 is *not* gap-free: 76 items with a gap at `3640398` and an out-of-range `3640665`. | §2.4 |
| **C4** | Minor | "GUOQ … holds compile time fixed at one hour for every tool." | The paper says "***unless otherwise indicated***, we allocated each tool 1 hour," and Quarl is an explicit exception (A100, 64 GB). A default, not a uniform constraint. The F4 argument survives; the hedge is now recorded. | F4 |
| **C5** | Minor | Micro Blossom "Θ(d³) processing units"; "8× lower latency". | The paper writes **O(d³)**, not Θ. And the 8× compares Micro Blossom's **I/O-inclusive** latency against an **I/O-exclusive** baseline — an asymmetry the paper notes, working against Micro Blossom, but an asymmetry. | §8, §13 |
| **C6** | Minor | Promatch's "fixed combinatorial capacity (Hamming weight ≤ 10, 945 matchings)"; "960 ns". | That capacity is **Astrea-G's**, inherited by Promatch rather than introduced by it. The 960 ns is a **top-down allotted budget** derived from the syndrome-cycle deadline, then divided by an assumed 250 MHz — not an observation. | §8, §13 |

### A.2 A correction the verification pass itself needed

The verification pass proposed replacing the 2024 program share with **9 / ~140 ≈ 6.4%**, taking ~140 as the program total. That figure comes from the *same truncated page* — it counts sessions 1A–8C only. Adopting it would have replaced one error with another. The census therefore reports **no counted 2024 program denominator at all**, marks the derived one `TOTAL_COUNT_UNVERIFIED`, and leans on the proceedings series instead. Recorded here because a verification pass is not automatically right either.

### A.3 Claims tested and confirmed unchanged

The deferral rule and its verbatim CFP quotation; all nine container-title↔volume mappings; the absence of an ASPLOS 2026 Volume 3; the year assignments of Clapton, PowerMove and VarSaw; ASPLOS 2025 = 10 quantum papers, all locatable in-session; ASPLOS 2026 = 12 across three sessions, with CHEHAB and CEMU correctly excluded as non-quantum; every Micro Blossom measurement (0.8 µs average, 62 MHz, VMK180, 867k/900k LUTs at d=15); **the T1 mis-transfer** — Promatch's sweep runs at p = 10⁻⁴–5×10⁻⁴ while Micro Blossom cites its 13.9× figure at p = 0.1% = 10⁻³, outside the swept range (the verification pass called this the strongest finding in the census, and it stands); RESCQ's 100× claim; QTurbo's SimuQ timings; the Micro Blossom README exceeding its paper; Promatch's repository containing no HDL despite an FPGA synthesis claim; the three AE badge levels being voluntary and publicly invisible; the artifact spot-checks; "It Takes Two to Entangle" being a non-quantum false positive; and the existence of ISCA successor papers.

### A.4 What remains unresolved

- **ASPLOS 2024 program total and session map** — the official page is truncated and no complete alternative was reachable (ACM DL blocked, DBLP's API disallowed by `robots.txt`, its HTML fetch partial). `TOTAL_COUNT_UNVERIFIED`.
- **28th ASPLOS Volume 4 size** — never enumerated; it is a component of the 2024 program denominator.
- **The 2026 one-paper discrepancy** — 168 derived versus "167 unique papers" on the official program page.
- **Artifact badge status for all 36 papers** — `UNKNOWN`; ACM DL is the only publisher of that metadata.
- **Two abstract-only papers** — *A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer* and *ACQC*. Their mechanisms are not inferred.

**Standing rule for this project, reinforced by this pass:** where a program-derived and a proceedings-derived number both exist, name which one is being used, in the same sentence as the number.

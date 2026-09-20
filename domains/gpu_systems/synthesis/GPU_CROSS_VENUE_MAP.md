# GPU_CROSS_VENUE_MAP — how ten venues treat GPU work, argued from this corpus

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (census + ledger + deep-analysis pass over
SC, ICS, IPDPS, ISC, HPDC, PPoPP, ASPLOS, ISCA, MICRO, HPCA — 2024, 2025, 2026)

Scope: what each venue counts as a GPU contribution, and on what kind of
evidence, **derived from this repository's own census files
(`../census/*.md`), its eleven verdict ledgers (`../corpus/_LEDGER_*.md`) and
its 85 deep analyses (`../corpus/GPU-*.md`)** — not from venue reputation.

---

## 0. Three completeness notions, kept apart

**Population completeness ≠ public full-text completeness ≠ field
comprehensiveness.** These are three different properties and this document
never uses one as evidence for another.

- **Population completeness** is whether this corpus reconstructed a
  venue-year's *denominator* — the list of main-track research papers. It is
  recorded per venue-year as `COMPLETE_CENSUS` / `PARTIAL_CENSUS` / `BLOCKED`
  plus an `enumeration completeness` of `EXACT` / `APPROXIMATE` /
  `UNVERIFIED_TOTAL`. It says nothing about whether any paper could be read.
- **Public full-text completeness** is whether a paper's text was reachable
  *from this environment*. `dl.acm.org` returns 403 here, `ieeexplore.ieee.org`
  returns 418, and `dblp.org` and `par.nsf.gov` are robots-blocked. A paper
  that is formally open access and unreachable here is recorded
  `PENDING_FULLTEXT`, **not** `CLOSED_ACCESS`. This is an access-path property
  of this workspace. **It is not a property of the venue, the publisher's
  licence, or the paper.**
- **Field comprehensiveness** is whether the ten venues, over three years,
  contain the GPU-systems field. **This corpus makes no such claim and cannot.**
  GPU work also appears at OSDI, SOSP, PLDI, POPL, CGO, VLDB, SIGMOD, PACT,
  ISPASS, EuroSys and elsewhere; several of those venues appear *in this
  corpus only as citation targets* (§4). One paper was excluded outright for
  being at CGO rather than one of the ten (Proteus).

A sentence in this document that reports a denominator is about the first. A
sentence that reports what was read is about the second. No sentence here
claims the third, and **no share or rate computed below should be read as a
statement about the field.**

---

## 1. The thirty venue-years

### 1.1 How each column was derived

| Column | Derivation |
|---|---|
| **Official population** | The `official population count (main/regular research papers)` row of `../census/<VENUE>_<YEAR>.md`, verbatim. |
| **Census status** | The `census_status` front-matter field of the same file. |
| **Enum.** | The `enumeration completeness` field: `EXACT` / `APPROX` / `UNVER` (`UNVERIFIED_TOTAL`). |
| **Broad GPU candidates** | Count of numbered rows in §2 ("Broad GPU candidates (STEP B)") of that census file. Row numbering was checked to be contiguous 1..N in **all thirty** files, so the count equals the maximum row index. |
| **Confirmed CORE_GPU** | Distinct papers with a `CORE_GPU` verdict in `../corpus/_LEDGER_*.md`, matched to a venue-year by the ledgers' own `Venue/Year` column, **deduplicated across ledgers** by normalised title (25 papers are adjudicated in more than one ledger; the strongest verdict wins). |
| **Deep analyses** | Count of `../corpus/GPU-<VENUE><YY>-*.md` files, from the filename's stable ID. |

Three derivation caveats, stated rather than hidden:

1. **`../corpus/_LEDGER_compiler_programming.md` omits the `Verdict` column
   from every data row** — its three tables have nine cells against a ten-cell
   header. Those rows cannot be read as verdicts. Where such a row carries a
   deep-analysis file, the full-paper gate implies `CORE_GPU` and it is counted
   in a separate **`+gate`** column. **Eighteen further rows from that ledger
   have no recoverable verdict and are counted nowhere** — so every CORE_GPU
   figure below is a **lower bound**, and the affected venue-years are ASPLOS
   2025 (2), SC 2024 (3), PPoPP 2026 (4), HPCA 2026 (1), HPDC 2026 (1),
   ICS 2024/2025/2026 (1 each), PPoPP 2024/2025 (1 each), ASPLOS 2026 (0 after
   dedup), MICRO 2024 (1).
2. **CORE_GPU counts are adjudications, not a filtered acceptance set.** No
   paper was excluded in the tensor-core or sparse clusters at all; a
   `CORE_GPU` verdict means "this contribution depends on a named GPU-specific
   property", which is a different question from "this is a GPU paper".
3. **Deep analyses are not a subset of confirmed CORE_GPU.** Two of the 85 are
   `RELATED_GPU` and were analysed anyway —
   `../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md`
   and `../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md`
   (the latter re-adjudicated from full text and **confirmed** `RELATED_GPU`,
   not overturned). This is why ISC 2026 shows 4 deep analyses against 3
   confirmed CORE_GPU.

### 1.2 The table

| Venue-year | Official population | Census status | Enum. | Broad GPU candidates | Confirmed CORE_GPU | +gate | Deep analyses |
|---|---|---|---|---|---|---|---|
| ASPLOS 2024 | 194 | `PARTIAL_CENSUS` | EXACT (29V4) | 15 | 7 | +1 | 4 |
| ASPLOS 2025 | 176 | `PARTIAL_CENSUS` | UNVER | 23 | 9 | — | 4 |
| ASPLOS 2026 | 152 | `PARTIAL_CENSUS` | UNVER | 28 | 11 | +1 | 6 |
| HPCA 2024 | 75 | `COMPLETE_CENSUS` | EXACT | 9 | 5 | — | 2 |
| HPCA 2025 | 113 | `COMPLETE_CENSUS` | EXACT | 14 | 10 | — | 1 |
| HPCA 2026 | **UNKNOWN** (three mutually inconsistent sources) | `PARTIAL_CENSUS` | APPROX | 16 | 8 | +1 | 2 |
| HPDC 2024 | 26 | `COMPLETE_CENSUS` | EXACT | 14 | 2 | — | 0 |
| HPDC 2025 | 25 | `COMPLETE_CENSUS` | EXACT | 8 | 3 | — | 0 |
| HPDC 2026 | 40 | `COMPLETE_CENSUS` | EXACT | 23 | 3 | — | 1 |
| ICS 2024 | 45 | `COMPLETE_CENSUS` | EXACT | 13 | 6 | — | 3 |
| ICS 2025 | 83 | `COMPLETE_CENSUS` | EXACT | 27 | 8 | +1 | 4 |
| ICS 2026 | 102 | `COMPLETE_CENSUS` | EXACT | 33 | 9 | — | 3 |
| IPDPS 2024 | 88 | `COMPLETE_CENSUS` | EXACT | 11 | 3 | — | 1 |
| IPDPS 2025 | 105 (official statement) | `PARTIAL_CENSUS` | APPROX | 15 | 5 | — | 0 |
| IPDPS 2026 | 101 (third-party attested only) | `PARTIAL_CENSUS` | UNVER | 9 | 8 | — | 5 |
| ISC 2024 | 24 | `COMPLETE_CENSUS` | EXACT | 8 | 3 | — | 1 |
| ISC 2025 | 28 | `COMPLETE_CENSUS` | EXACT | 11 | 1 | — | 0 |
| ISC 2026 | 13 (official statistic) | `PARTIAL_CENSUS` | UNVER | 6 | 3 | — | 4 |
| ISCA 2024 | 83 | `COMPLETE_CENSUS` | EXACT | 9 | 3 | — | 1 |
| ISCA 2025 | 131 | `COMPLETE_CENSUS` | EXACT | 20 | 14 | — | 2 |
| ISCA 2026 | 161 | `COMPLETE_CENSUS` | EXACT | 21 | 15 | — | 1 |
| MICRO 2024 | 113 | `COMPLETE_CENSUS` | EXACT | 20 | 16 | — | 10 |
| MICRO 2025 | 123 | `COMPLETE_CENSUS` | EXACT | 12 | 11 | — | 3 |
| MICRO 2026 | **UNKNOWN** (no public main-program) | `PARTIAL_CENSUS` | UNVER | 1 | 0 | — | 0 |
| PPoPP 2024 | 32 | `COMPLETE_CENSUS` | EXACT | 14 | 5 | — | 2 |
| PPoPP 2025 | 38 | `COMPLETE_CENSUS` | EXACT | 23 | 10 | — | 4 |
| PPoPP 2026 | 51 | `COMPLETE_CENSUS` | EXACT | 25 | 12 | — | 4 |
| SC 2024 | 99 | `COMPLETE_CENSUS` | EXACT | 49 | 15 | +1 | 9 |
| SC 2025 | 133 (printed in the main volume) | `COMPLETE_CENSUS` | EXACT (printed) | 60 | 16 | — | 3 |
| SC 2026 | **UNKNOWN** (no official accepted-paper list) | `PARTIAL_CENSUS` | UNVER | 14 | 10 | — | 5 |
| **TOTAL** | **2,354 across 27 of 30 venue-years** | 20 complete / 10 partial / 0 blocked | — | **551** | **231** | **+5** | **85** |

**Reading the totals.** The population total is **2,354 over 27 venue-years**;
**HPCA 2026, MICRO 2026 and SC 2026 have no reconstructed denominator at all**,
so no repository-wide "GPU share of all papers" figure is computable and none
is given. Across all thirty venue-years the ledgers adjudicated **351 distinct
papers** (352 including one CGO 2025 row that is `EXCLUDE`, out of population):
**231 `CORE_GPU` + 5 `CORE_GPU` by the full-paper gate, 45 `RELATED_GPU`, 50
`UNRESOLVED`, 3 `EXCLUDE`, 18 with no recoverable verdict cell.**

**Approximate counts, named.** HPCA 2026's population is `APPROXIMATE` from
three mutually inconsistent sources; IPDPS 2025's 105 is an official statement
not an enumeration; IPDPS 2026's 101 is third-party attested only; ISC 2026's
13 is an official statistic that the census marks `UNVERIFIED_TOTAL`; SC 2025's
133 is `EXACT` **for the printed main volume**. Any ratio involving those rows
rests on an incomplete or unverified denominator and is labelled so wherever
it appears below.

---

## 2. Evidence-type split per venue

Derived by reading each deep analysis's evaluation platform — the
`Simulated or measured?` line where the cluster used it (the fixed-function
cluster did, systematically), and otherwise §12.11 "why it is faster/slower"
and §12.12 "hardware generation dependence", which name the parts. Categories:
**MEAS** = executed on real GPU silicon; **SIM** = simulator, RTL or FPGA model
only; **SIM+MEAS** = a hybrid the analysis explains; **PROD** = production
fleet or cluster telemetry; **NO GPU** = no GPU executed anywhere in the
evaluation. **n = the 85 deep analyses only** — this is not the adjudicated
351, and it inherits the access asymmetry of §3.

| Venue | n | MEAS | SIM | SIM+MEAS | PROD | NO GPU |
|---|---|---|---|---|---|---|
| PPoPP | 10 | 10 | 0 | 0 | 0 | 0 |
| ISC | 5 | 5 | 0 | 0 | 0 | 0 |
| SC | 17 | 15 | 1 | 0 | 1 | 0 |
| ICS | 10 | 9 | 0 | 0 | 1 | 0 |
| IPDPS | 6 | 4 | 0 | 0 | 2 | 0 |
| HPDC | 1 | 1 | 0 | 0 | 0 | 0 |
| ASPLOS | 14 | 8 | 4 | 0 | 1 | 1 |
| MICRO | 13 | 4 | 6 | 2 | 0 | 1 |
| HPCA | 5 | 1 | 4 | 0 | 0 | 0 |
| ISCA | 4 | 1 | 3 | 0 | 0 | 0 |
| **Total** | **85** | **58** | **18** | **2** | **5** | **2** |

**The split is almost categorical.** Across **SC, ICS, IPDPS, ISC, HPDC and
PPoPP — 49 analyses — 48 are on real hardware** (44 MEAS + 4 PROD) and
**exactly one is simulated**: `../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md`
(zsim, an integrated-GPU model), **which is also one of the two papers whose
verdict is `RELATED_GPU`.** Across **ISCA, MICRO and HPCA — 22 analyses — 15
involve a simulator** (13 SIM + 2 SIM+MEAS), 6 are measured and 1 executes no
GPU.

**Production/fleet studies are concentrated and few: five in total** —
`../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md` (27,756 V100s on
Summit), `../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md`
(Delta/DeltaAI), `../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md`
and `../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md`
(Perlmutter and Frontier), and `../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md`
(an Azure fleet with facility PDU telemetry). **Four of the five are at
HPC venues; the fifth, POLCA, is the only ASPLOS paper in the corpus with
fleet-scale telemetry, and its fleet is a cloud provider's, not a centre's.**

**Two papers execute no GPU at all and both are still `CORE_GPU`, for stated
reasons.** `../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md`
verifies on "an Ubuntu 22.04.4 LTS machine … 11th Gen Intel Core i5-1135G7"
`[paper]` — every added `.cat` construct is GPU-only.
`../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md`
measures two Intel Gold 6226R and a Fujitsu A64FX `[paper]`; its subject is
GPU-source-code properties. Counting them as "GPU evaluations" would be wrong;
counting them out of the corpus would also be wrong.

**One caveat that cuts against over-reading this table.** MEAS and SIM are not
equally easy to reach through a paywall. The measured venues are also the
venues with the better author-PDF culture in this corpus (§3), so part of the
contrast is the contrast of §3 seen from the other side. What the table
establishes is the evidence type **of the 85 papers that were read**, and the
regularity is strong enough (48/49 vs 15/22) that access asymmetry is unlikely
to explain all of it — but that last clause is `[inference]`, not a
measurement.

---

## 3. Access asymmetry — a methodological caveat, not a finding about the field

Derived by tallying the `Access state` column across all eleven ledgers,
deduplicated by normalised title the same way as §1 (n = 352 distinct
adjudicated papers, including the one CGO row).

| Venue | adjudicated | PUBLIC_FULLTEXT | % full | CLOSED_ACCESS | PENDING_FULLTEXT | ABSTRACT_ONLY | ARTIFACT_ONLY |
|---|---|---|---|---|---|---|---|
| ASPLOS | 41 | 21 | 51% | 8 | 1 | 5 | 4 |
| MICRO | 34 | 14 | 41% | 11 | 2 | 1 | 2 |
| ISC | 13 | 5 | 38% | 6 | 1 | 1 | 0 |
| IPDPS | 21 | 7 | 33% | 9 | 0 | 5 | 0 |
| PPoPP | 40 | 13 | 32% | 17 | 1 | 5 | 3 |
| SC | 69 | 21 | 30% | 15 | 9 | 14 | 7 |
| HPCA | 29 | 8 | 28% | 17 | 0 | 3 | 1 |
| ISCA | 41 | 11 | 27% | 17 | 6 | 5 | 2 |
| ICS | 44 | 11 | 25% | 26 | 2 | 5 | 0 |
| HPDC | 19 | 1 | **5%** | 10 | 0 | 8 | 0 |
| **Total** | **352** | **112** | **32%** | **136** | **22** | **52** | **19** |

(11 further rows carry a composite or non-standard access state and are not
assigned to a column.)

**What this is.** `dl.acm.org` → 403, `ieeexplore.ieee.org` → 418,
`dblp.org` and `par.nsf.gov` robots-blocked, `arxiv.org/search`,
`export.arxiv.org` and `web.archive.org` unavailable; `arxiv.org/abs/`,
`arxiv.org/html/<id>vN`, author and institution PDFs, conference-hosted
proceedings PDFs and GitHub over Bash all work. **Two identifier-specific rate
limits also shaped the pass**: arXiv `2609.07912` returned HTTP 429 on eight
attempts across four URL forms while other IDs fetched normally, and
`2606.29775`'s `/html/` and `/pdf/` paths returned 429 five times while
`/abs/` succeeded — so **SMART-MIG is `PUBLIC_FULLTEXT` by access state but
`ABSTRACT_ONLY` by evidence read.**

**What this is not.** It is **not** a statement about which venues publish
openly. Several ISCA 2025, SC 2025 and MICRO 2025 papers here are **genuinely
open access, some CC BY, and simply unreachable from this workspace** — they
are `PENDING_FULLTEXT`, not `CLOSED_ACCESS`, and the ledgers say so per row.
See `GPU_PENDING_FULLTEXT.md`.

**The effect on this corpus's shape, stated plainly.**

1. **HPDC is nearly invisible: 1 of 19 adjudicated papers readable (5%), and
   one deep analysis across three years.** Anything this corpus says about
   HPDC is one paper wide. That is an artefact of this workspace.
2. **ICS has the highest absolute `CLOSED_ACCESS` count (26 of 44)** and yet
   contributes 10 deep analyses, because the readable ones were readable
   through conference-hosted proceedings PDFs
   (`hpcrl.github.io/ICS2025-webpage/...`). Venue-level openness and
   *this* pass's reach are not the same variable.
3. **Author-PDF culture, not venue, predicts readability within a topic.**
   `../corpus/_LEDGER_sparse_irregular.md` §3 is explicit: that cluster read
   **7 of 45 papers (16%)** against the tensor-core cluster's 9 of 42, and
   "the difference is not venue mix but **author-PDF culture** — every one of
   the four author-PDF successes here came from two labs that post their own
   papers."
4. **Depth is unevenly distributed and partly by accident.** MICRO 2024 has
   **10** deep analyses — more than any other venue-year and 12% of the whole
   corpus — while HPDC 2024, HPDC 2025, IPDPS 2025, ISC 2025 and MICRO 2026
   have **none**. Reading MICRO 2024's prominence here as a statement about
   MICRO 2024 would conflate public full-text completeness with field
   comprehensiveness.
5. **Four papers were watchlisted with their mechanism recovered from source
   code alone**, and the gate forbids deep-analysing them: Triton-Sanitizer
   (ASPLOS 2026), GCStack+GCScaler (ISCA 2025, `PUBLIC_ARTIFACT_ONLY`), *pkdb*
   (SC 2026), and SMART-MIG (IPDPS 2026). A verdict from an abstract or an
   artifact **may not** justify a deep analysis
   (`../../../governance/ANTI_HALLUCINATION_RULES.md`).
6. **Three seeds could not be shown to exist** and must not be carried forward
   as papers: *GPU Faults Across Cloud Providers* (SC 2026), *SigmaTrace*
   (SC 2026), *Attention, Watch Your Progress* (MICRO 2026). **One analysed
   paper's venue is unverified**: LEO is filed as `GPU-SC26-41` on public full
   text, but the census records `NOT_FOUND` in every official SC26 source and
   the arXiv record carries no venue comment — it is treated as a **preprint**,
   and no SC-level claim in this document rests on it.

---

## 4. What each venue recognises as a GPU contribution

### 4.1 SC / ICS / IPDPS / ISC — the contribution is a measured system on named silicon

The evidence is §2 (48 of 49 analyses on real hardware) plus the shape of what
those papers contribute. Three regularities:

- **The machine is named, and named machines recur**: Summit, Frontier,
  Perlmutter, Delta/DeltaAI, Alps, LUMI-G, Leonardo, MareNostrum 5, Polaris.
  `../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md`
  and `../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md`
  are *about* named machines' interconnects; `../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md`
  scales to 9,216 GH200 on Alps.
- **Characterisation is a first-class contribution.** ICS 2024 accepted both a
  fleet failure study (`GPU-ICS24-01`) and an AMD SVM oversubscription study
  whose product is a recommendation list rather than a mechanism
  (`../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md`).
  IPDPS accepted two companion production studies in the same year (§5, B4).
- **Cross-vendor evaluation is normal here and rare elsewhere.**
  `../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md`
  spans five systems and two vendors;
  `../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md`
  spans four process nodes and two vendors *by construction*;
  `../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md`
  builds per-vendor ISA decoders for three vendors.

### 4.2 ISCA / MICRO / HPCA — the contribution is a mechanism, and the baseline is a model

**15 of 22 analyses involve a simulator** (§2), and the simulator choice is
itself a research position — Accel-Sim/GPGPU-Sim, MGPUSim, Vulkan-Sim, Emerald,
TEAPOT, MacSim, zsim all appear. Consequences visible in the corpus:

- **The baseline machine is frequently one that does not exist.** HSU
  (`../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md`)
  models an RT unit inside a **Volta V100 configuration — a part with no RT
  cores at all**. Virgo (`../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md`)
  compares against the authors' own **RTL abstractions** of Volta-, Ampere- and
  Hopper-style integration, not against those parts.
- **Area and power are synthesis estimates**, and this corpus never restates
  them as measurements (`../../../governance/SOURCE_EVIDENCE_RULES.md`).
- **The venues' own strongest papers now dispute the model.**
  `../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md` measures
  the Accel-Sim baseline at **34.03% MAPE against a real RTX A6000** and finds
  real cores use compiler control bits with **no operand collector**;
  `../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md` finds
  the real NoC is a hierarchical crossbar, not the simulated mesh, and places
  prior GPU-NoC proposals on a plane where the modelled bottleneck does not
  exist. **The strongest correction to the architecture venues' evidence base
  came from inside those venues.**

### 4.3 Where PPoPP and ASPLOS sit

**PPoPP sits with the HPC venues on evidence and with nobody in particular on
subject.** **10 of 10 PPoPP analyses are measured on real silicon — the only
venue in the corpus with no simulated paper at all.** Its subjects range from
tensor-core stencils to device-side allocators to DFS work stealing. Its
population is small (32 / 38 / 51) and its broad-candidate rate is high
(14 / 23 / 25 candidates), i.e. **a large fraction of PPoPP is GPU-facing** —
though the 2024 and 2025 denominators are `COMPLETE_CENSUS`/`EXACT`, so that
ratio is at least well-founded on the population side.

**ASPLOS is the only genuinely mixed venue in the corpus: 8 MEAS, 4 SIM,
1 PROD, 1 NO-GPU.** It is the only venue that holds, in three consecutive
years, a cloud fleet study (POLCA), a formal consistency model verified on a
laptop CPU (`GPU-ASPLOS24-142`), an FPGA capability-hardware prototype
(`../corpus/GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md`),
a near-memory-compute architecture proposal (`../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md`),
and measured production systems (GMLake, MSCCL++, gShare, Bullet, Tilus).
It also has the corpus's **highest full-text reachability (51%)**.

### 4.4 The bridging claim, and why this corpus rejects it

The assumption this pass was given — that **PPoPP and ASPLOS bridge the HPC and
architecture communities** — is **not supported by the citations the compiler
cluster read.** The evidence, each item a citation base a paper reports for
itself, recorded in the analyses' §12.14 and summarised in
`../topics/compiler_programming.md` §5:

- **SC / OSDI / SOSP → HPCA.** `../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md`
  names Halide (PLDI), TVM (OSDI'18), Ansor (OSDI'20), AStitch (ASPLOS 2022),
  BOLT (MLSys'22), TASO (SOSP'19), Chimera (HPCA 2023), **MCFuser (SC'24)**,
  T10 (SOSP 2024) `[paper]`. **An HPCA paper importing from SC, OSDI and SOSP**
  — and the SC'24 → HPCA'26 link is a verified, paper-internal citation, not an
  inference.
- **PL and formal methods → ASPLOS.** `../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md`
  names Alglave, Lustig, Wickerson and Donaldson, and the analysis records:
  "**venues of those cited works, as the paper reports them: PLDI, POPL, CAV,
  TACAS** — i.e. the citation base of this ASPLOS paper is a
  programming-languages/formal-methods base, **not an architecture base**"
  `[paper]`.
- **Databases and parallel computing → PPoPP.** `../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md`
  reports a cited venue set of **IPDPS, PPoPP, ICS, VLDB, SIGMOD, HPEC** —
  "a parallel-computing *plus database* citation base, with **no ISCA/MICRO/HPCA
  presence**" `[paper]`.
- **Two further non-architecture citation bases at HPC venues**, which is what
  makes the pattern a pattern rather than two anecdotes:
  `../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md`
  reports **P3HPC workshop, SC workshops, IPDPS, CCGrid** with "essentially no
  ISCA/MICRO/HPCA presence", and
  `../corpus/GPU-SC24-147--ompdart-static-generation-openmp-offload-data-mappings.md`
  reports **ISPASS, Euro-Par, IEEE VLSI transactions** — "again a
  non-architecture citation base" `[paper, both]`.

**What the evidence rests on, stated exactly.** These are **five papers' own
reported citation bases**, read at full text in one cluster
(`../corpus/_LEDGER_compiler_programming.md`), plus one verified cross-venue
citation link (MCFuser SC'24 → FlashFuser HPCA'26). It is **not** a bibliometric
study, and it does **not** show that PPoPP and ASPLOS never cite architecture
venues. What it shows is that **in the papers this corpus actually read, the
traffic into the architecture venues comes from systems venues (SC, OSDI,
SOSP), while PPoPP and ASPLOS import from programming languages, formal methods
and data management.** The bridging role was assumed; the citations do not
carry it. Recorded as a finding about **this corpus's read set**, with the
`[paper]` evidence named, per `../../../governance/ANTI_HALLUCINATION_RULES.md`.

Two corroborating observations from other clusters, consistent but not part of
the compiler cluster's evidence: `../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md`
(SC 2024) has "a memory-systems citation neighbourhood, not a GPU-architecture
one, which is itself evidence for the [`RELATED_GPU`] verdict" `[paper]`; and
`../corpus/_LEDGER_sparse_irregular.md` §7.4 verified that two sparse papers
(one SC, one ICS) cite **no** RT-unit architecture work at all.

---

## 5. Blind spots the corpus revealed

### 5.1 Same venue, same year, same problem, no citation

Four cases, graded by how the non-citation was established.

**B1 — PPoPP 2025: FlashSparse and Acc-SpMM. `SUPPORTED`, stated in both
analyses.** `../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md`
and `../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md`
both exploit the MMA's `n = 8` operand asymmetry for SpMM on Tensor Cores, and
each analysis records "**Neither cites the other** (both are same-cycle)"
`[paper, both]`. The corpus reads the convergence as evidence that the `n = 8`
observation was the field's obvious next step — which is the charitable
reading, and it is also the reading that makes the absence informative.

**B2 — ICS 2025: Aatrox and ghZCCL. `SUPPORTED`, by targeted full-text query.**
`../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md` is
a GPU error-bounded lossy compressor; **ghZCCL is a GPU-compression-in-collective
paper at the same venue and year**. "A targeted check for gZCCL, hZCCL, ghZCCL
and NCCL-based compression found none" in Aatrox `[paper]`. The same negative
result holds for cuSZ-i (SC 2024) and GPZ (ICS 2026), and the reverse direction
was checked on `../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md`,
which cites gZCCL/ghZCCL/COCCL and **no standalone GPU compressor**. Authors
overlap heavily across both sides — **two disjoint citation practices, not two
disjoint groups of people** (`../corpus/_LEDGER_data_movement_compression.md` §D.4).

**B3 — SC 2024: three compression papers in one volume, one problem, no
contact.** The volume holds **cuSZ-i** (`../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md`,
ratio branch), **cuSZp2** (speed branch, `10.1109/SC41406.2024.00021`), and the
compression-in-collective line's **hZCCL** and **DLRM dual-level adaptive lossy
compression**. Same-cycle papers cannot cite each other, so the informative
part is the *sustained* absence: **no citation traffic in either direction**
between the standalone and collective lines was found in any year checked
`[paper, verified on five papers]`. **Correction to carry**: cuSZ-i's §12.14
identifies cuSZp2 as `GPU-SC24-82`; that stable ID belongs to Hydrogen, and
**cuSZp2 has no corpus file**. Do not follow that cross-reference.

**B4 — IPDPS 2026: NIMBLE and PCCL, and separately the two production
companions. Graded `[inference]` for the first, `SUPPORTED` for the second.**
`../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md` and
`../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md`
are recorded as "same venue and year, both target the gap between available and
achieved GPU-cluster bandwidth" — NIMBLE re-plans *paths*, PCCL re-plans
*algorithms* — and **the analyses record no citation link in either
direction**; what is *verified* is narrower: PCCL's related work has **no
comparison with MSCCL and no comparison with GPU-initiated/NVSHMEM approaches**
`[paper]`. By contrast `../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md`
and `../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md`
are the **same group at the same venue and are complementary by construction**
— that pair is a venue strength, recorded here so the two cases are not
confused.

**B5 — MICRO 2024: HSU and TTA, twins in session 7B.** Same session, same
thesis ("generalise the RT unit"), **different RT hardware baseline** (AMD
RDNA3-style software stack vs NVIDIA-style hardware stack), different
simulator. The analyses record them as twins with **no citation link in either
direction** — consistent with same-cycle submission. Graded `[inference]` on
the non-citation; what is `SUPPORTED` is that their numbers are not comparable
(`../topics/fixed_function_repurposing.md` §7, T2).

### 5.2 Cross-venue blind spots the corpus also revealed

Not same-venue, but they bear on how the venues relate:

- **SC 2024 and MICRO 2024 published exact duals that do not cite each other.**
  `../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md` (under-synchronisation)
  and `../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md`
  (over-synchronisation) "analyse the same programs over the same CUDA scope
  lattice and cite the same baselines", and **HiRace is absent from
  ScopeAdvice's related-work list** while HiRace's related work does not mention
  over-synchronisation `[paper, both]`. Their independent characterisations of
  iGUARD are mutually consistent, which strengthens both.
- **ASPLOS 2025 and ICS 2026 solved the same GPU constraint one year apart
  "apparently without contact"** — the unknown-output-size problem, exactly
  (GPUlog's two-pass join) versus probabilistically (Ocean's HyperLogLog) — and
  **a general device-side allocator that would subsume both (Gallatin,
  PPoPP 2024) is in this corpus and cited by neither**
  (`../corpus/_LEDGER_sparse_irregular.md` §7.2).
- **The RT branch and the rasterisation branch of category Q do not cite each
  other in any venue**: VR-Pipe (HPCA 2025) cites **no** RT-core repurposing
  work at all, verified by targeted query, and no RT paper read here cites
  VR-Pipe, RoCC or DEFCON (`../corpus/_LEDGER_fixed_function_repurposing.md` §4.3).
- **ICS 2026's SpGEMM paper contains none of "ray tracing", "RT core", "RT
  unit", "BVH", "RTSpMSpM" or "LibRTS"** — while **RTSpMSpM (ISCA 2025) is
  sparse matrix multiplication on the RT unit** (`../corpus/_LEDGER_sparse_irregular.md` §7.4).

### 5.3 A blind spot about venues themselves

Three venue-years have **no reconstructed population at all** (HPCA 2026,
MICRO 2026, SC 2026), and MICRO 2026 yielded **one** broad candidate. The
corpus cannot say whether MICRO 2026 is thin on GPU work or simply not yet
public — **and it should not be asked to**. That is a population-completeness
statement, and converting it into a claim about the venue would be exactly the
conflation §0 forbids.

---

## 6. Deeper lookup paths

`../census/<VENUE>_<YEAR>.md` for a denominator, its evidence and its seed
reconciliation → `../corpus/_LEDGER_<cluster>.md` for a verdict, its access
state and what was actually read → `../corpus/GPU-*.md` for the mechanism,
the numbers and their hardware/workload/baseline qualifiers → the paper.
Sibling syntheses: `GPU_TOPIC_LINEAGES.md`, `GPU_HARDWARE_GENERATION_MAP.md`,
`GPU_COMMUNICATION_STACK.md`, `GPU_TENSOR_CORE_LINEAGE.md`,
`GPU_MEMORY_LINEAGE.md`, `GPU_PENDING_FULLTEXT.md`,
`GPU_EXISTING_CORPUS_OVERLAP.md`.
Topic layer: `../topics/`.

**Standing caveat for every count in this document.**
`../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` — an ~80-paper AI/HPC
corpus exists outside this repository, is not imported, and **nothing about its
content may be asserted, including venues, counts or coverage**. Many rows in
the communication, compiler, runtime, power and data-movement clusters carry
`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` for that reason
(`GPU_EXISTING_CORPUS_OVERLAP.md`). Absence from this repository is not
evidence of novelty.

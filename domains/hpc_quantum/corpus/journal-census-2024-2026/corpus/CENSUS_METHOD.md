# CENSUS_METHOD — Quantum-HPC Journal Census 2024–2026

How the eight-journal census was built, exactly, so it can be audited and repeated.

---

## 1. Scope

Eight journals, 2024–2026, publications publicly available as of **2026-09-17**:

| | Journal | ISSN used |
|---|---|---|
| 1 | Future Generation Computer Systems (FGCS) | 0167-739X |
| 2 | IEEE Transactions on Quantum Engineering (TQE) | 2689-1808 |
| 3 | ACM Transactions on Quantum Computing (TQC) | 2643-6809 |
| 4 | IEEE Transactions on Parallel and Distributed Systems (TPDS) | 1045-9219 |
| 5 | IEEE Transactions on Computers (TC) | 0018-9340 |
| 6 | IEEE Transactions on CAD of ICs and Systems (TCAD) | 0278-0070 |
| 7 | ACM Transactions on Architecture and Code Optimization (TACO) | 1544-3566 |
| 8 | Journal of Parallel and Distributed Computing (JPDC) | 0743-7315 |

Explicitly **not** censused, by instruction: *Quantum*, *PRX Quantum*, *npj Quantum Information*,
*Quantum Science and Technology*, and any other journal. No venue was added to the list during the work.

---

## 2. Population enumeration

**Primary source — Crossref REST.** For each ISSN, the complete set of `journal-article` records with
a Crossref `published` date in 2024-01-01 … 2026-12-31 was enumerated by cursor pagination
(`/journals/{issn}/works?filter=from-pub-date:…,until-pub-date:…&rows=1000&cursor=*`), selecting DOI,
title, type, published, volume, issue, page and author. This is a *full population* sweep, not a
keyword search, and it is what gives the denominators:

| Journal | Articles enumerated |
|---|---:|
| FGCS | 1,567 (+ 423 in the supplementary window, see §2.2) |
| TQE | 254 |
| TQC | 97 |
| TACO | 412 |
| TPDS | 552 |
| TC | 849 |
| TCAD | 1,562 |
| JPDC | 388 |
| **Total** | **5,681** |

**Secondary source — OpenAlex.** For each journal, `title_and_abstract.search:(quantum OR qubit OR
QPU)` filtered by source id and publication year. This catches papers whose *abstract* carries the
vocabulary but whose *title* does not, and supplies first-availability dates for Elsevier and IEEE.

**Candidate pool = union of (Crossref title-regex hits) and (OpenAlex title+abstract hits).**
For **TQE and TQC the full population was screened**, not a keyword subset, because both journals are
entirely quantum and a vocabulary filter would have been meaningless.

### 2.1 Search vocabulary

Title regex applied to the Crossref population:

```
quantum · qubit · QPU · statevector · state vector · tensor network · circuit cutting ·
surface code · qLDPC · syndrome · FTQC · NISQ · transpil· · QAOA · VQE · stabilizer ·
ansatz · entangl· · anneal· · QEC · Ising
```

A secondary sweep over narrower terms (`statevector`, `tensor network`, `circuit cutting`,
`surface code`, `qLDPC`, `decoder`, `syndrome`, `FTQC`, `transpiler`, `QAOA`, `VQE`, `NISQ`,
`stabilizer`, `ansatz`) was attempted to catch papers carrying none of `quantum`/`qubit`/`QPU`.
It was **not completed** — the OpenAlex account budget rate-limited it. Recorded as a recall
limitation; no such record was found in the portion that did run.

### 2.2 The Elsevier cover-date correction

Elsevier volume cover dates run roughly **six months ahead** of the online-first date (FGCS volume 174
has cover date 2026-01 and contains papers first available in mid-2025). Crossref's `published` field
for Elsevier is the **cover** date, so a sweep bounded at cover-date 2026-12-31 silently drops every
article first available in the second half of 2026 (volumes 186–187, cover date 2027-01).

This was caught by the verification pass. A supplementary sweep to cover-date **2027-12-31**, filtered
back to first-availability ≤ 2026-09-17, recovered **four** missing FGCS records and **zero** missing
JPDC records. One of the four is an EXISTENCE_CHECK_SEED paper
(`10.1016/j.future.2026.108731`, the Heron + Fugaku closed-loop work).

**Any repeat of this census must sweep Elsevier on online-first date, not cover date.**

### 2.3 Abstracts

Abstracts were retrieved in batch from the Semantic Scholar Graph API (`/paper/batch`, DOI keys) and,
where absent, from OpenAlex inverted indexes. Twenty candidate records had no retrievable abstract
from any source and are flagged `NO_ABSTRACT`; those were screened on title plus targeted retrieval
(DOI redirect → publisher abstract page, or the arXiv abstract page where an arXiv id existed).
Abstracts were truncated to 700–900 characters for the screening pass.

---

## 3. Paper identity and the census year

**DOI is the primary key.** Every record is identified by DOI; no DOI appears twice. Early-access and
final-issue versions of the same paper share a DOI and are therefore one record by construction.
The verification pass confirmed zero DOI duplicates and zero early-access/issue double counts.

**Census year = year of first public availability** where a first-availability date exists:

| Publisher | Source of the date | Basis |
|---|---|---|
| Elsevier (FGCS, JPDC) | OpenAlex `publication_date` = online-first | `YEAR_BASIS=ONLINE` |
| ACM (TQC, TACO) | Crossref `published-online` | `YEAR_BASIS=ONLINE` |
| IEEE (TC, TCAD, TPDS) | OpenAlex `publication_date` = Early Access where recorded | `YEAR_BASIS=ONLINE` |
| IEEE (TQE) | volume cover year (v5=2024, v6=2025, v7=2026) | **`YEAR_BASIS=ISSUE`** — Early Access dates were not obtainable for TQE from any source used |

For every record the **final volume, issue, pages and issue cover date are recorded separately**, so
the census can be re-derived on a volume-year basis if that convention is preferred. Records with no
volume are IEEE Early Access or ACM Just Accepted and are flagged.

Three records proved to be outside the window on this basis and were moved to `OUT_OF_WINDOW`:
`10.1016/j.future.2023.12.002` (FGCS, first available 2023-12-04),
`10.1109/tqe.2023.3347106` (TQE, 2023-12-26),
`10.1109/tc.2021.3066614` (TC, a 2021 paper in a 2024 issue).

---

## 4. The Three-Gate Inclusion Test

The full criteria, as given to every screener, are reproduced in `CENSUS_CRITERIA.md`. In brief, a
paper is included only if it satisfies all three:

1. **Gate 1** — a substantive classical systems problem is present (computation cost, parallelism,
   memory, communication, latency, throughput, scheduling, resource allocation, runtime,
   orchestration, distributed execution, scaling, compilation cost, data movement, accelerator design,
   performance modeling).
2. **Gate 2** — an HPC / systems / architecture technique is a major part of the contribution.
3. **Gate 3** — the paper materially informs future CPU/GPU/HPC ↔ QPU heterogeneous computing.

*Using* a classical computer is not a classical systems contribution. Being about a quantum computer
is not sufficient.

**The operative discriminator inside the quantum-native journals.** Because every TQE and TQC article
is quantum, no quantum-side term discriminates. The question applied to every abstract was: *does the
paper state a classical cost quantity* (runtime, memory, communication volume, compile time,
throughput, utilisation) *or only a quantum-resource quantity* (gate count, T-count, depth, fidelity,
logical error rate, entanglement rate, shots-to-accuracy)? Papers of the second kind were excluded
regardless of quality.

Papers satisfying a gate only weakly were recorded `BORDERLINE`, with the argument for and against,
not discarded. Every `INCLUDED` and `BORDERLINE` record carries per-record `gate1`/`gate2`/`gate3`
justifications.

---

## 5. Article-type separation

Every record is typed `ORIGINAL_RESEARCH` · `REVIEW_SURVEY` · `PERSPECTIVE` · `EDITORIAL` ·
`SPECIAL_ISSUE_INTRO` · `OTHER`. **Only `ORIGINAL_RESEARCH` counts toward the included population.**
Highly relevant reviews and perspectives are retained and tagged `BIBLIOGRAPHY_HUB`. Corrigenda,
front matter and volume indexes are typed `OTHER` and excluded.

---

## 6. Screening procedure

1. Candidate pool built per journal (§2), with metadata and abstract.
2. Four independent screening passes, one per journal group, each reading 100% of its dossier and
   classifying **every** record — not only the ones it intended to include.
3. Targeted full-text/preprint retrieval for the highest-priority records to fill mechanism, scale,
   metrics, baseline and artifact fields.
4. An **independent adversarial verification pass** (§7) by a screener that had not produced any of
   the classifications.
5. Corrections applied by the original screeners, each adjudicating the challenges to its own work
   and permitted to rebut in writing.

---

## 7. Verification pass

Thirteen required checks plus one coverage check, recorded in full in `VERIFICATION_CHANGELOG.md`:
DOI duplicates · early-access/issue double counting · year accuracy · original research vs
review/editorial · erratum and front matter · is it actually a quantum-computing paper · HPC/systems
relevance re-tested adversarially on every included record · false positives still in the included
set · conference-extension lineage evidence · quantitative claims and their baselines · artifact URL
resolution · seed-anchoring bias · TQE/TQC scope explosion · TPDS/JPDC inflation · plus a
population-recall check that found the Elsevier cover-date gap in §2.2.

**Outcome:** 67 corrections, of which 15 material. Three records moved to `OUT_OF_WINDOW`; one census
year corrected; four records added after the recall gap was closed; twelve demotions proposed, of
which ten were accepted and two kept with written rebuttals; per-record gate justifications added
where they were missing.

---

## 8. Known limitations, stated plainly

1. **Artifact status is `UNKNOWN` for 46 of 89 included original-research papers.** IEEE Xplore, ACM
   DL badge pages and Elsevier full text were not reachable. `UNKNOWN` = *not checked*.
2. **Zero `CONFIRMED_EXTENSION` conference-lineage records**, because publisher front matter could
   not be read. The journal and conference corpora must therefore **not be summed** into one count of
   independent contributions.
3. **TQE runs on `YEAR_BASIS=ISSUE`**; its per-year split is less reliable than the other journals'.
4. **Three TCAD Early Access records remain `INSUFFICIENT_EVIDENCE`** (no abstract retrievable).
   TCAD's 2026 count is depressed by this.
5. **The secondary vocabulary sweep did not complete** (API rate limit), so recall rests on the
   primary 21-term vocabulary plus the OpenAlex abstract search.
6. **2026 is a partial year** (to 2026-09-17).
7. **Seed-anchoring risk is recorded, not eliminated:** all 23 pre-scan seed titles present in the
   corpus are INCLUDED, a 100% rate against 17% corpus-wide. 78% of included papers are non-seed.
8. **Direct HTTP access to Crossref and OpenAlex was blocked by the research environment's egress
   policy**; all metadata was retrieved through a browser session, and rate limits truncated some
   queries.

---

## 9. Reproducibility

Machine-readable outputs, one per journal, each containing **every** classified record (not only the
included ones) with its verdict, gate justifications, analysis fields and exclusion reason:
`FGCS_records.json`, `TQE_records.json`, `TQC_records.json`, `TACO_records.json`, `TC_records.json`,
`TCAD_records.json`, `TPDS_records.json`, `JPDC_records.json`, plus the merged `all_records.json`
(563 records) and `verification_corrections.json`.

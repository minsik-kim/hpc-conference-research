# SOURCE_MANIFEST — `journal-census-2024-2026`

Source project: **Quantum-HPC Core Journal Census, 2024–2026.**
Produced 2026-09-17 (KST) inside this repository, for the `hpc_quantum` domain.

## What this project is

A full-population census of the HPC × quantum-computing interface in **eight core journals** over
**2024–2026**, built to extend the domain's existing conference corpus (`quantum-hpc-survey`) onto the
journal axis. It is **not** a quantum-computing literature review, and it covers **only** the eight
journals named in the commissioning brief.

| Journal | ISSN | Articles swept | Included original research |
|---|---|---:|---:|
| Future Generation Computer Systems | 0167-739X | 1,567 (+423 supplementary window) | 20 |
| IEEE Trans. Quantum Engineering | 2689-1808 | 254 | 25 |
| ACM Trans. Quantum Computing | 2643-6809 | 97 | 20 |
| IEEE Trans. CAD of ICs and Systems | 0278-0070 | 1,562 | 12 |
| IEEE Trans. Computers | 0018-9340 | 849 | 6 |
| ACM Trans. Architecture and Code Optimization | 1544-3566 | 412 | 4 |
| IEEE Trans. Parallel and Distributed Systems | 1045-9219 | 552 | 2 |
| J. Parallel and Distributed Computing | 0743-7315 | 388 | 0 |
| **Total** | | **5,681** | **89** |

563 candidate records classified · 94 included (89 original research, 5 review/perspective) ·
80 borderline · 383 excluded · 3 unresolved · 3 out of window.

## Provenance and evidence basis

- **Population enumeration:** Crossref REST, full-population cursor pagination by ISSN, 2024-01-01 …
  2026-12-31 (plus a supplementary Elsevier window to cover-date 2027-12-31 — see `CENSUS_METHOD.md`
  §2.2). Union with an OpenAlex `title_and_abstract.search` query per journal and year.
- **Abstracts:** Semantic Scholar Graph API batch endpoint, with OpenAlex inverted indexes as
  fallback. Twenty records had no retrievable abstract and are flagged `NO_ABSTRACT`.
- **Targeted retrieval:** DOI redirect → publisher abstract page, arXiv abstract pages, GitHub
  repository pages, for the highest-priority records only.
- **Screening:** four independent passes, one per journal group, each reading 100% of its dossier and
  classifying every record.
- **Verification:** one independent adversarial pass over 14 checks, then correction by the original
  screeners, each permitted to rebut in writing. 67 corrections, 15 material. Full record in
  `corpus/VERIFICATION_CHANGELOG.md`.

**Everything was gathered during this project.** No content was imported from, or merged with, the
`quantum-hpc-survey` source project; that corpus is used as *context* only, and none of its counts,
evidence tags or conclusions were revised, re-derived or upgraded here.

## Files

| Path | What it is |
|---|---|
| `corpus/QUANTUM_HPC_JOURNAL_MAP.md` | Comparative map of the eight journals: role, yield, branches, conference correspondence, future census policy |
| `corpus/QUANTUM_HPC_JOURNAL_CENSUS_2024_2026.md` | Master census — every included original-research record in full, plus borderline, bibliography hubs, artifact matrix, conference-extension status and the false-positive log |
| `corpus/QUANTUM_HPC_JOURNAL_CONFERENCE_CROSSWALK.md` | Branch-by-branch correspondence against the SC and ASPLOS censuses and the 21-venue map |
| `corpus/CENSUS_FGCS_2024_2026.md` | FGCS detail, including the reconstruction of the three quantum Special Collection volumes |
| `corpus/CENSUS_TQE_2024_2026.md` | TQE detail — full 246-record population screen |
| `corpus/CENSUS_TQC_TACO_2024_2026.md` | TQC (full 97-record population screen) and TACO detail |
| `corpus/CENSUS_TC_TCAD_TPDS_JPDC_2024_2026.md` | TC, TCAD, TPDS and JPDC detail, with the branch-ownership analysis |
| `corpus/JOURNAL_DEEP_DIVE_CANDIDATES.md` | 18 selected papers for a Phase-3 deep dive, with selection reasons and what must be closed first |
| `corpus/FOLLOW_UP_CANDIDATES.md` | Out-of-scope threads, evidence gaps and method notes; `CANDIDATE` status only |
| `corpus/CENSUS_METHOD.md` | How the census was built, and its stated limitations |
| `corpus/CENSUS_CRITERIA.md` | The Three-Gate Inclusion Test as issued to every screener, verbatim |
| `corpus/VERIFICATION_CHANGELOG.md` | The independent verification pass: 14 checks, corrections table, residual uncertainty |
| `corpus/data/<J>_records.json` | Machine-readable: **every** classified record per journal, included and excluded alike, with verdict, gate justifications, analysis fields and exclusion reason |
| `corpus/data/all_records.json` | Merged 563-record view with normalised field names |
| `corpus/data/verification_corrections.json` | Machine-readable corrections from the verification pass |

## Evidence limitations carried by this project

Stated in full in `corpus/CENSUS_METHOD.md` §8. The four that most constrain use:

1. **Artifact status is `UNKNOWN` for 68 of 89 included papers** — publisher artifact pages were not
   reachable. `UNKNOWN` means *not checked*, never *no artifact*. No artifact-rate comparison with the
   conference corpus's SC (64%) / ASPLOS (61%) figures is valid on this evidence.
2. **Zero `CONFIRMED_EXTENSION` conference-lineage records** — publisher front matter could not be
   read. **The journal and conference populations must not be summed** into one count of independent
   contributions.
3. **IEEE TQE runs on `YEAR_BASIS=ISSUE`** (volume cover year), because Early Access dates were not
   obtainable for it; its per-year split is weaker than the other journals'.
4. **Three TCAD Early Access records are `INSUFFICIENT_EVIDENCE`**, which depresses TCAD's 2026 count.

## Gap vocabulary

This project makes **no novelty claim and identifies no research gap**. Observations are recorded only
as `JOURNAL_GAP`, `VENUE_GAP`, `UNDERREPRESENTED_IN_THIS_CORPUS`, `POSSIBLE_CROSSOVER`,
`OPEN_QUESTION` or `INSUFFICIENT_EVIDENCE`, all at `CANDIDATE` status, per
`governance/RESEARCH_GAP_RULES.md`.

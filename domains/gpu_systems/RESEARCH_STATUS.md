# RESEARCH_STATUS — GPU Systems

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-19

Domain status: **PARTIAL**

## What "PARTIAL" means here, precisely

Three different completeness claims are involved and only the first is strong.

| Claim | Status | Basis |
|---|---|---|
| **Population completeness** — the venue-year paper lists are the real ones | **Strong for 27 of 30 venue-years** | Official proceedings, official programs or publisher volumes, with the source class recorded per venue-year |
| **Public full-text completeness** — the candidates could be read | **Uneven** | 85 read in full; 202 on the watchlist, 27 of them open access but unreachable from this environment |
| **Field comprehensiveness** — this is what GPU research looks like | **Not claimed** | Ten venues, three years, main tracks only. Journals, workshops, TOPLAS/TACO-class venues, arXiv-only work and industry publication are all outside the frame |

`COMPLETE_AS_CENSUSED` is not `COMPREHENSIVE_FIELD_COVERAGE`. This domain is
closer to the former.

## Census status by venue-year

21 `COMPLETE_CENSUS`, 9 `PARTIAL_CENSUS`, 0 `BLOCKED`.

| Venue | 2024 | 2025 | 2026 |
|---|---|---|---|
| SC | 99 · complete | 133 printed / 137 announced · complete (discrepancy unresolved) | **UNKNOWN · partial** |
| ISCA | 83 · complete | 131 · complete | 161 · complete |
| MICRO | 113 · complete | 123 · complete | **UNKNOWN · partial** |
| HPCA | 75 · complete | 113 · complete | **UNKNOWN · partial** (119/113/123 conflict) |
| PPoPP | 32 · complete | 38 · complete | 51 · complete |
| ASPLOS | 194 · partial | 176 · partial | 152 · partial |
| ICS | 45 · complete | 83 · complete | 102 · complete |
| IPDPS | 88 · complete | 105 · partial | 101 · partial (third-party only) |
| HPDC | 26 · complete | 25 · complete | 40 · complete |
| ISC | 24 · complete | 28 · complete | 13 · partial |

Total reconstructed population: **2,354** across the 27 venue-years that have a
denominator.

The ASPLOS years are `PARTIAL_CENSUS` for a different reason from the others:
the volume counts are publisher-verified, but the title-to-volume join is
incomplete (71% / 85% / effectively complete screening coverage respectively),
and the officially stated "167 unique papers" for 2026 does not reconcile with
the volume sums. The counts are sound; the attribution of individual titles to
volumes is not.

## What has been done

1. **STEP A — population reconstruction.** 30 venue-years, with source class,
   enumeration completeness, excluded non-regular classes and their counts,
   and paper-type-mixing notes. Written to `census/`.
2. **STEP B — broad screening over the whole population.** 551 candidates.
   Keyword lists ordered the review; they never decided it. Papers with no GPU
   term in the title but a central GPU mechanism were pulled in, and
   keyword-bearing non-candidates were recorded with a reason.
3. **Seed reconciliation.** The human pre-scan's seed list was treated as a
   recall aid and checked against each population. Results in each census §5.
4. **STEP C — full-text gate and relevance adjudication.** Eleven clusters,
   each producing a verdict ledger with access state, evidence actually read,
   the counterfactual answer, verdict and rationale for every assigned paper.
5. **Deep analyses.** 85, each following the 12.1–12.14 template, each with a
   recorded `read_depth`, each labelling `[paper]` / `[code]` / `[artifact]` /
   `[reconstruction]` / `[inference]`. 25 artifact repositories were cloned and
   pinned by commit hash.
6. **Synthesis.** Master index, five lineage documents, cross-venue map,
   overlap registry, watchlist, methodology notes, and the twelve integration
   questions answered from corpus evidence.

## What has NOT been done

- **No `git push`.** Per `governance/CONFERENCE_IMPORT_WORKFLOW.md`, push is a
  separate, explicitly authorised action. The work is on the local branch
  `gpu-corpus-2024-2026`.
- **No catalog entry.** `catalog/papers.yaml` and the validator/index scripts
  that `CONFERENCE_IMPORT_WORKFLOW.md` steps 5–7 refer to do not yet exist in
  this repository (`scripts/README.md` is a placeholder). The steps are
  recorded as outstanding rather than faked.
- **No research-gap promotion.** `OPEN_QUESTIONS.md` records observations at
  `CANDIDATE` status only. None has been through the own-corpus cross-check,
  closest-work search, external targeted search and novelty falsification that
  `governance/RESEARCH_GAP_RULES.md` requires before an observation becomes a
  research question.
- **No de-duplication against the AI/HPC corpus**, which is not in this
  repository. 99 papers are on the worklist for when it is imported.
- **No workshop, journal or arXiv-only coverage.** Main tracks only, by design.

## Known evidence gaps — do not close these without new work

- SC 2026 and MICRO 2026 main-program populations (both venues were still
  ahead of the corpus's build date).
- HPCA 2026's population (three inconsistent sourced figures).
- SC 2025's 137-versus-133-versus-144 discrepancy.
- 27 papers stated to be open access but unreachable from the build
  environment — this is a tooling gap that a different network path would
  close immediately.
- 15 seed-derived titles whose existence no source could confirm.
- The Tensor-Core numeric-format branch (Avant-Garde, MXBLAS, MXFFP) has no
  deep analysis, so the fourth stage of that area's progression could not be
  tested.
- No power-sensor sampling-window characterisation exists for **any** AMD GPU,
  in this corpus or, as far as its papers report, anywhere.
- No CDNA MFMA cross-generation characterisation numbers exist in the corpus;
  the one cross-generation matrix-unit study is NVIDIA-only.

## Maintenance

When a new venue-year is added, follow
`governance/CONFERENCE_IMPORT_WORKFLOW.md` and
`governance/TOPIC_UPDATE_WORKFLOW.md`: reconstruct the population first,
screen the whole population, apply the full-paper gate, and update **only** the
topic and synthesis documents the new sources actually change. Re-check the
watchlist in `synthesis/GPU_PENDING_FULLTEXT.md` first — several entries there
are expected to become reachable with time rather than with effort.

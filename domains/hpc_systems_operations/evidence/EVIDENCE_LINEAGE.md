# EVIDENCE_LINEAGE.md — hpc_systems_operations

Routing document only — it records **which corpus document supersedes which** and does not restate or re-derive any finding. Per `governance/KNOWLEDGE_BASE_RULES.md`, superseded documents are never deleted or edited; this file is the pointer layer that keeps GPT/readers from citing an overturned claim as current.

## Chain 1 — synthesis correction chain

```
synthesis/00_SCOPE_AND_METHOD.md
synthesis/01_VENUE_MAP.md
synthesis/02_PAPER_CENSUS.md              }  initial synthesis (00–07)
synthesis/03_SC_REGULAR_PRECEDENTS.md     }
synthesis/04_WORKSHOP_AND_CUG_CASES.md    }
synthesis/05_RESEARCH_PRACTICE_GAPS.md    }
synthesis/06_INITIAL_SC_RESEARCH_CANDIDATES.md
synthesis/07_ANSWERS_TO_KEY_QUESTIONS.md
        │
        ▼  adversarially audited by
synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md
        │
        ▼  corrected/revised by
synthesis/13_VERIFICATION_ROUND2.md   ← CURRENT AUTHORITY for anything it addresses
```

**Rule:** for any claim in `00`–`07`, check whether `09` audited it, and whether `13` in turn revised `09`'s finding. `13` wins over `09`; `09` wins over `00`–`07`. Where `13` is silent on a claim, `09`'s finding (if any) stands; where both are silent, the original `00`–`07` claim stands as unaudited synthesis (not as verified fact — see `governance/ANTI_HALLUCINATION_RULES.md` grounding states).

`synthesis/10_SC_CANDIDATE_RANKING.md` (first ranking of the 10 candidates from `06`) is itself revised by `13_VERIFICATION_ROUND2.md`'s updated ranking — treat `13` as authoritative for candidate verdicts, `10` as the superseded first pass.

## Chain 2 — raw-evidence verification chain

```
raw/A_SC_main.md
raw/B_hpdc_ipdps_cluster_isc_acsos.md
raw/C_dsn_issre_lineage.md          }  initial census (A–H)
raw/D_workshops.md                  }
raw/E_cug_vendor.md                 }
raw/F_axes_ABC.md                   }
raw/G_axes_DEFG.md                  }
raw/H_centers.md                    }
        │
        ▼  independently re-checked by
raw/V1_db_retention_sweep.md
raw/V2_sc26_ornl.md
raw/V3_pika_tuncer.md          ← revises PIKA / Tuncer characterization first stated in F/G
raw/V4_hindsight_suffbench.md
raw/V5_fdi_sensor_placement.md
raw/V6_lcopt_centile_setdiff.md   ← revises LC-Opt / CENTILE / SeT-Diff characterization first stated in F/G
raw/V7_nonenglish_indices.md
raw/V8_grey_isc.md
```

**Rule:** for the specific systems/claims each `V` document addresses (named in its title), the `V` document is authoritative over the corresponding `A`–`H` claim. For everything `A`–`H` covers that no `V` document re-examined, `A`–`H` remains the only evidence and should be treated as **unverified initial census**, not as independently confirmed.

## Practical routing for a contested or quantitative claim

1. Identify which topic file (`topics/*.md`) and which synthesis/raw document the claim traces to.
2. Check this file for whether that document sits upstream of a later document in either chain.
3. If yes, read the later document's actual finding before answering — do not answer from the earlier document alone.
4. If the later document is silent on that specific claim, the earlier document's finding stands, but should be reported with its original evidence-confidence tag (`STRONG-EVIDENCE` / `SUPPORTED` / `CENSUS-DEPENDENT` / `ZERO-CLAIM` / `PARTIAL-COVERAGE` / `NEEDS-VERIFICATION` / `SPECULATIVE`), never upgraded.

This file will need an update only when a *new* verification document is added to the corpus (which is a `TOPIC_UPDATE_WORKFLOW.md`/`CONFERENCE_IMPORT_WORKFLOW.md` event, not a routine edit) — it is not meant to be re-derived from scratch each time.

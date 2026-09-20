# METHODOLOGY_NOTES — how this corpus was built, and what it does not claim

last_updated: 2026-09-19
knowledge_as_of: 2026-09-19

## The design decision that shaped everything

This corpus was built **population-first**. For each of 30 venue-years the
official main/regular research-paper list was reconstructed before any GPU
question was asked; only then was the whole population screened. The
alternative — start from a list of promising titles, search for them, read the
abstracts, declare them GPU papers — produces a plausible corpus that cannot
say what it missed. A human pre-scan supplied a seed list of candidate titles;
it was used **only** to test recall against the reconstructed populations, and
its reconciliation is recorded in each census file's §5.

That decision has a cost, and the cost is visible in the output: reconstructing
populations is where most of the failures are, and three venue-years ended with
no denominator at all.

## The pipeline

```
STEP A  official population, with source class and enumeration completeness
   ↓
STEP B  broad screen over the ENTIRE population (keywords order review, never decide)
   ↓
        seed reconciliation — does the pre-scan's list survive contact with the population?
   ↓
STEP C  access-state resolution → full-paper reading → counterfactual test → verdict
   ↓
        full-paper gate: no deep analysis from an abstract or an artifact alone
   ↓
        deep analysis (12.1–12.14), with read_depth recorded
   ↓
        taxonomy, topics, lineages verified against the papers' own citations
```

## The counterfactual test, and what it actually separated

> If a generic accelerator or a CPU were used instead, would the core
> contribution be substantially the same?

Applied to every candidate, with the answer recorded. In practice one criterion
did most of the separating, and it is worth stating because it is reusable:
**does the contribution's own output artefact cross the GPU boundary, or is the
GPU-specific work delegated to a layer below it?** A retargetable tensor
compiler that emits PTX delegates; a language whose type system names the MMA
register-fragment layout does not.

A second discriminator emerged in the sparse and graph clusters: **does the
paper's headline metric have a CPU meaning?** "Kernel count reduced to 1.10%",
"synchronisation was >30% of baseline", "30.18× over prior GPU work against
1.37× over CPU" are GPU-specific claims. "Fewer iterations", "less
communication volume" are not.

The test produced more `RELATED_GPU` verdicts in sparse linear algebra and
graph analytics than elsewhere, which is what one would expect of fields with
large algorithm-first literatures. That asymmetry is a property of the fields,
not a calibration drift — each cluster recorded its reasoning so the calibration
can be audited.

## The full-paper gate

A `CORE_GPU` verdict could be reached from an abstract. **A deep analysis could
not.** Analyses record in `read_depth` which sections were actually read;
papers that failed the gate went to `GPU_PENDING_FULLTEXT.md` regardless of how
interesting they looked. Several of the corpus's most valuable-looking
candidates are on that watchlist, including one where the artifact was cloned
and read but the paper text was unreachable — the artifact evidence is
recorded, the analysis is not written.

This gate is the main reason the corpus has 85 analyses rather than 200, and it
is the reason the 85 can be trusted.

## Where the numbers come from, and what they can carry

| Number | Value | What it rests on |
|---|---|---|
| Venue-years censused | 30 | official proceedings / programs / publisher volumes, source class recorded per file |
| Population reconstructed | 2,354 across 27 venue-years | sum of per-venue-year counts; three venue-years have no denominator |
| Broad GPU candidates | 551 | numbered §2 rows across the 30 census files |
| Distinct papers adjudicated | ~351 | cluster ledgers, de-duplicated across clusters |
| Deep analyses | 85 | one file each, all `PUBLIC_FULLTEXT`, all read |
| Watchlist | 202 | ledger rows that passed relevance and failed the gate |

**No repository-wide "GPU share of venue" is computed anywhere in this domain.**
Three venue-years have no denominator, several populations are `APPROXIMATE`,
and ASPLOS's title-to-volume join is incomplete. A share computed over that
would look authoritative and be wrong.

## Parallel construction and its artefacts

Eleven adjudication clusters ran concurrently. Two consequences are visible in
the output and are not defects to be tidied away:

- **Stable-ID bands.** Clusters were given disjoint `<NN>` ranges so no ID
  could be reused. The bands carry no meaning; `GPU-SC24-181` is not the 181st
  SC 2024 paper. One genuine collision occurred and was resolved in favour of
  the first writer, with the loser reissued — recorded in both ledgers.
- **Cross-cluster corrections.** Clusters found errors in each other's rows
  (an access state, a verdict, a discharged watchlist item) and in this
  project's own census files. These were applied as **amendments** that keep
  the original reasoning visible, per `governance/KNOWLEDGE_BASE_RULES.md`
  rule 7, not as rewrites.

## What was deliberately not done

- **Nothing was reconstructed from recollection of the literature.** Where a
  source could not be reached, the record says so.
- **No lineage was asserted from plausibility.** Every edge in the lineage
  documents carries `[paper]`, `[author-overlap]`, `[inference]` or
  `NOT_CITED`. The appendix of expected lineages supplied with the task was
  treated as a hypothesis to test, and several of its links did not survive.
- **No research gap was promoted.** Everything in `OPEN_QUESTIONS.md` is
  `CANDIDATE`.
- **No claim was made about the un-imported AI/HPC corpus.** For 99 papers,
  duplication is `NOT DETERMINED`.
- **No `git push`.** Push is a separately authorised action.

## Known method weaknesses

1. **Access shaped the sample.** Venues and groups that post preprints and
   author PDFs are over-represented among the 85. This is a property of the
   corpus, not of the field, and `GPU_CROSS_VENUE_MAP.md` says so where it
   would otherwise be mistaken for a finding.
2. **Screening was title- and abstract-level where abstracts were reachable at
   all.** Several venues publish titles and authors only. Those judgments are
   tagged `[title-only]` in the census files; a few were later overturned by
   full text, which is evidence that others may be wrong in the same way.
3. **Non-citation claims rest on targeted queries**, not on full bibliometrics.
   `NOT_CITED` means "checked, and not found" over a defined query set, which
   is stronger than silence and weaker than a citation-graph analysis.
4. **Two analyses carry a `RELATED_GPU` verdict.** They were written before
   re-adjudication settled and are retained as labelled boundary cases rather
   than deleted.
5. **One cluster ledger omits its verdict column** from its data rows, so
   `CORE_GPU` totals derived from the ledgers are lower bounds. This is flagged
   where the number is used.

## Reproducing or extending this

`census/_CENSUS_TEMPLATE.md`, `corpus/_ANALYSIS_TEMPLATE.md` and
`corpus/_VERDICT_LEDGER_TEMPLATE.md` are the three contracts. A new venue-year
follows `governance/CONFERENCE_IMPORT_WORKFLOW.md`; a new source updates only
the topics it actually changes, per `governance/TOPIC_UPDATE_WORKFLOW.md`. The
first thing to re-run is not a new venue but the watchlist: 27 of its entries
are open-access papers that a different network path would make readable
immediately.

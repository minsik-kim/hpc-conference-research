# KNOWLEDGE_BASE_RULES

These are the operating principles for this repository. Every domain,
topic, synthesis, and governance document inherits them.

1. **Corpus is evidence-oriented and append-oriented.** `corpus/` holds
   source-level analyses; new sources are added, existing ones are not
   rewritten to "read better."
2. **Synthesis and topic documents are living documents.** `synthesis/` and
   `topics/` are expected to change as new sources are added — but only the
   topics actually affected by a given new source (see
   `TOPIC_UPDATE_WORKFLOW.md`).
3. **Generated files must not be edited manually.** Any file marked
   `<!-- GENERATED — DO NOT EDIT MANUALLY -->` is rebuilt by its generating
   script, never hand-edited.
4. **Stable source IDs must not be reused.** See `ID_NAMING_RULES.md`.
5. **Original source/evidence has priority over compressed summaries.** A
   `DOMAIN_CONTEXT.md` or `TOPIC_MAP.md` is a routing document, not a final
   authority — see `ANTI_HALLUCINATION_RULES.md`.
6. **Do not silently reconcile conflicts.** When two sources disagree, or a
   synthesis document and a corpus entry disagree, record the disagreement
   (e.g. in a domain's `CROSS_PAPER_TENSIONS.md`-style synthesis file)
   rather than picking one silently.
7. **Do not delete historical research decisions merely because they
   changed.** Superseded research questions, gaps, or claims are marked
   with a status (see `RESEARCH_GAP_RULES.md`), not removed.
8. **Use git history for versioning rather than creating `_v2`/`_v3`
   files**, unless a historical snapshot is being intentionally preserved
   (in which case its relationship to the current canonical file must be
   stated explicitly — see `VERSIONING_CHANGELOG_RULES.md`).

## Priority order for any structural or migration work in this repository

```
preservation > structural migration > indexing > stylistic cleanup
```

Never rewrite existing analysis content "to read better" as a side effect
of a structural change.

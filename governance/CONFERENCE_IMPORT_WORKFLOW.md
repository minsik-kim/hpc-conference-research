# CONFERENCE_IMPORT_WORKFLOW

Standard workflow when a new conference or source set is added to a
domain's `corpus/`:

1. Verify official full population (the complete accepted-paper list for
   that venue/year).
2. Screen (apply the domain's inclusion criteria).
3. Add the selected corpus entries.
4. Preserve or assign stable IDs (see `ID_NAMING_RULES.md`).
5. Update the domain's catalog entry (`catalog/papers.yaml` or
   domain-local equivalent).
6. Run the validator (`scripts/validate_catalog.py` once it exists for
   this repository).
7. Rebuild generated indexes (`scripts/build_indexes.py` once it exists).
8. Identify affected topics.
9. Update only the affected topic/synthesis documents (see
   `TOPIC_UPDATE_WORKFLOW.md`) — do not rewrite unaffected topics.
10. Update precursor/lineage synthesis documents if the new sources change
    them.
11. Re-falsify any research questions the new sources bear on (see
    `RESEARCH_GAP_RULES.md`).
12. Update the domain's `DOMAIN_CONTEXT.md`.
13. Update the domain's `CHANGELOG.md`.
14. Local commit.

No step in this workflow includes a `git push`; push is a separate,
explicitly authorized action.

# CHANGELOG — GPU Systems

## 2026-09-18 → 2026-09-19 — Domain created and built in one pass

The `gpu_systems` domain did not previously exist. It was created and
populated in a single construction pass on the branch `gpu-corpus-2024-2026`,
from public sources only. No prior corpus was imported into it.

Added:

- `census/` — 30 venue-year files for SC, ISCA, MICRO, HPCA, PPoPP, ASPLOS,
  ICS, IPDPS, HPDC and ISC × 2024–2026, plus `_CENSUS_TEMPLATE.md`. Each
  records the official main/regular population with its source class and
  enumeration completeness, the excluded non-regular classes and their counts,
  a broad GPU screen over the whole population, keyword-bearing non-candidates
  with reasons, candidates with no GPU term in the title, and seed
  reconciliation. 21 `COMPLETE_CENSUS`, 9 `PARTIAL_CENSUS`, 0 `BLOCKED`;
  2,354 papers reconstructed across the 27 venue-years that have a denominator.
- `corpus/` — 85 deep analyses following `_ANALYSIS_TEMPLATE.md`, and 11
  cluster verdict ledgers following `_VERDICT_LEDGER_TEMPLATE.md`. Every
  analysis records `read_depth`; every ledger row records access state,
  evidence actually read, the counterfactual answer, the verdict and a
  rationale.
- `topics/` — 12 topic files following `templates/TOPIC.template.md`.
- `synthesis/` — `GPU_MASTER_INDEX.md`, `GPU_TOPIC_LINEAGES.md`,
  `GPU_HARDWARE_GENERATION_MAP.md`, `GPU_COMMUNICATION_STACK.md`,
  `GPU_MEMORY_LINEAGE.md`, `GPU_TENSOR_CORE_LINEAGE.md`,
  `GPU_CROSS_VENUE_MAP.md`, `GPU_EXISTING_CORPUS_OVERLAP.md`,
  `GPU_PENDING_FULLTEXT.md`, `GPU_INTEGRATION_QUESTIONS.md`,
  `METHODOLOGY_NOTES.md`.
- `evidence/README.md`, `implementation/ARTIFACT_REGISTRY.md` (25 third-party
  repositories pinned by commit hash), `research/CANDIDATE_QUESTIONS.md`.
- `DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`, `RESEARCH_STATUS.md`,
  `OPEN_QUESTIONS.md`, this file.

Changed (outside this domain):

- Root `MASTER_INDEX.md`, `GLOBAL_CONTEXT.md`, `README.md` — fourth domain
  registered.
- Root `GLOBAL_CHANGELOG.md` — the domain-prefixed stable-ID decision recorded
  with its effective date, as `governance/ID_NAMING_RULES.md` requires.
- `domains/hpc_systems_operations/` — **not modified.** Seven
  `GPU_DELTA_ANALYSIS` files in this domain state what that corpus already
  holds and add only GPU-specific depth; two of them correct errors in the
  prior record (a wrong final author, and two open flags on a census entry)
  by recording the correction here rather than editing that corpus.

New taxonomy category:

- **Q — fixed-function GPU units repurposed for general computation** was added
  to the A–P taxonomy during the work, defined by mechanism rather than by
  workload. The evidence and the argument are in
  `topics/fixed_function_repurposing.md`.

Closed questions: none. Nothing in `OPEN_QUESTIONS.md` has been through the
falsification pipeline in `governance/RESEARCH_GAP_RULES.md`; every item is
`CANDIDATE`.

New questions: 16 `CANDIDATE` observations, grouped as unresolved
contradictions, verified structural absences, methodological gaps, and
falsified expectations worth recording so they are not re-proposed.

Revalidated: the seed candidate list supplied with the task was checked against
every reconstructed population rather than taken as given. Several seed items
were shown to be misfiled by year, several were abbreviated working titles
resolved to official ones, and 15 could not be verified to exist at all.

Outstanding, recorded rather than skipped:

- `catalog/papers.yaml` and the validator/index scripts that
  `governance/CONFERENCE_IMPORT_WORKFLOW.md` steps 5–7 call for do not exist in
  this repository for any domain, so those steps were not performed.
- No `git push`. Push is a separately authorised action.
- De-duplication against `domains/ai_hpc_systems/` cannot be done until that
  corpus is imported; 99 papers are on the worklist.

Notes on method:

- Eleven adjudication clusters ran in parallel over disjoint stable-ID bands so
  that no ID could be reused. One genuine collision occurred and was resolved
  in favour of the first writer; the loser was reissued and all references
  updated, with the decision recorded in both ledgers.
- Cross-cluster corrections were applied as **amendments** that keep the
  original reasoning visible, per `governance/KNOWLEDGE_BASE_RULES.md` rule 7.
- Two deep analyses carry a `RELATED_GPU` verdict. They are retained as
  labelled boundary cases and excluded from `CORE_GPU` counts.

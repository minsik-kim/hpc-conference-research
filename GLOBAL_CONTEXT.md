# GLOBAL_CONTEXT

<!-- Top-level entry point for any GPT/Claude session opening this repository. -->

## Purpose of this repository

This repository is a grounded external-memory knowledge base for
research-assisted learning across multiple, parallel research landscapes.
It is read, not authored from memory: a session working here should treat
its actual file contents and git history as the source of truth, and should
not reconstruct or infer content that is not present.

## The three domains

| Domain | Path | Status |
|---|---|---|
| AI/HPC Systems | `domains/ai_hpc_systems/` | `EXTERNAL_IMPORT_PENDING` |
| HPC Systems & Operations | `domains/hpc_systems_operations/` | `STRUCTURE_ONLY` |
| HPC & Quantum | `domains/hpc_quantum/` | `STRUCTURE_ONLY` |

## Current data availability

This repository currently contains **structure and governance only**. No
paper corpus, synthesis, or evidence-audit content has been imported for any
domain. Where a domain's real-world corpus is known to exist elsewhere but
has not yet been brought into this repository, its status is
`EXTERNAL_IMPORT_PENDING` rather than `STRUCTURE_ONLY` (which means no known
corpus exists yet at all). Neither status is a license to fill the domain
with generic or recalled knowledge — see `governance/ANTI_HALLUCINATION_RULES.md`.

## Grounding policy

- Accuracy is more important than completeness.
- Do not invent missing facts.
- Distinguish supported facts from inference.
- For detailed, quantitative, or contested claims, retrieve the deepest
  canonical source available — do not answer from this file or a
  `DOMAIN_CONTEXT.md` alone.
- If evidence is insufficient, report `UNKNOWN` or `NOT_IN_REPOSITORY`.
- Do not infer novelty, or the absence of prior work, from this repository's
  own incompleteness.

## How to retrieve deeper information

```
GLOBAL_CONTEXT
      ↓
Domain selection (this table, or MASTER_INDEX.md)
      ↓
domains/<domain>/DOMAIN_CONTEXT.md
      ↓
TOPIC_MAP.md / topics/<topic>.md
      ↓
synthesis/ (cross-source synthesis documents)
      ↓
corpus/ (individual source analyses)
      ↓
original paper / artifact / code, when the question requires it
```

See `governance/GPT_RETRIEVAL_GUIDE.md` for the full retrieval workflow by
question type.

## Governance files

All rules governing how this repository is built, trusted, and extended
live in `governance/`:

- `KNOWLEDGE_BASE_RULES.md` — core operating principles
- `SOURCE_EVIDENCE_RULES.md` — provenance hierarchy and publication-type rules
- `ANTI_HALLUCINATION_RULES.md` — grounding states and mandatory principles
- `ID_NAMING_RULES.md` — stable source ID policy
- `CONFERENCE_IMPORT_WORKFLOW.md` — how a new conference/source set is added
- `TOPIC_UPDATE_WORKFLOW.md` — how one new source updates topics
- `RESEARCH_GAP_RULES.md` — how a research gap is proposed and falsified
- `VERSIONING_CHANGELOG_RULES.md` — versioning and changelog conventions
- `GPT_RETRIEVAL_GUIDE.md` — the retrieval workflow for a new session

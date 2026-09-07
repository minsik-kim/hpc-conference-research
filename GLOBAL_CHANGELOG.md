# GLOBAL_CHANGELOG

Repository-wide changes only. Domain-local changes belong in each domain's
own `CHANGELOG.md`.

## 2026-09-07 — Repository bootstrap

Added:
- Root context/index files (`README.md`, `GLOBAL_CONTEXT.md`,
  `MASTER_INDEX.md`, this file)
- Full `governance/` rule set (knowledge-base rules, source-evidence rules,
  anti-hallucination rules, ID naming, conference-import workflow,
  topic-update workflow, research-gap rules, versioning rules, GPT
  retrieval guide)
- Empty domain scaffolding for `ai_hpc_systems`, `hpc_systems_operations`,
  `hpc_quantum` (`DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`,
  `RESEARCH_STATUS.md`, `OPEN_QUESTIONS.md`, `CHANGELOG.md` each)
- `catalog/` schema placeholder (no `papers.yaml` yet)
- `scripts/`, `templates/` placeholders

Changed: n/a (first commit)

Closed questions: n/a

New questions: n/a

Revalidated: n/a

Notes:
- No content was imported in this bootstrap. The known ~80-paper AI/HPC
  systems corpus and its synthesis/evidence documents exist in a separate,
  external workspace and are recorded as `EXTERNAL_IMPORT_PENDING` — they
  will be brought in during a dedicated import step, not reconstructed from
  memory or general knowledge.
- No GitHub push was performed as part of this bootstrap.

## 2026-09-07 — HPC & Quantum: first domain content import

The `hpc_quantum` domain moved from `STRUCTURE_ONLY` to `PARTIAL`: its
first source project (`quantum-hpc-survey` — SC 2024–2025 and ASPLOS
2024–2026 regular-paper venue censuses, a 21-venue landscape map, and
QEC/simulation/compilation lineage synthesis, 39 files) was imported
byte-identically from a previously staged and integrity-verified copy.
See `domains/hpc_quantum/CHANGELOG.md` for the full per-file breakdown.
`ai_hpc_systems` and `hpc_systems_operations` are unchanged by this entry.

Root files touched: `README.md`, `GLOBAL_CONTEXT.md`, `MASTER_INDEX.md` —
in each, only the `hpc_quantum` row/bullet was edited; the other two
domains' rows/bullets were left exactly as they were.

No GitHub push was performed as part of this import.

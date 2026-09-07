# SOURCE_TYPE_MAPPING.md — hpc_systems_operations

Translation layer only. The corpus tags individual external citations in-place using its own taxonomy (defined in `corpus/aiops-survey/synthesis/00_SCOPE_AND_METHOD.md` and used throughout). **This file maps that taxonomy onto this repository's `governance/SOURCE_EVIDENCE_RULES.md` vocabulary for use in new canonical-layer prose (topic files, this domain's context/index files). It does not change, re-tag, or touch any tag inside the original 31 documents.**

| Corpus in-place tag | Governance equivalent (`SOURCE_EVIDENCE_RULES.md`) | Canonical-layer shorthand | Notes |
|---|---|---|---|
| `SC-TECHNICAL-PAPER` | `ARCHIVAL_MAIN_PAPER` | `[ARCHIVAL]` | SC's main technical-paper track is archival peer-reviewed |
| `ARCHIVAL-PEER-REVIEWED` | `ARCHIVAL_MAIN_PAPER` | `[ARCHIVAL]` | |
| `WORKSHOP-PEER-REVIEWED` | `WORKSHOP_PAPER` | `[WORKSHOP]` | |
| `POSTER` | `POSTER` | `[POSTER]` | |
| `BOF` | *(not in base governance list — domain-specific extension)* | `[BOF]` | Birds-of-a-Feather session; not peer-reviewed, practitioner-facing |
| `PANEL` | *(not in base governance list — domain-specific extension)* | `[PANEL]` | Panel discussion; opinion/discussion, not a reviewed result |
| `TUTORIAL` | `TUTORIAL` (via `AUTHOR_PRESENTATION`-class) | `[TUTORIAL]` | |
| `PRACTITIONER` | `AUTHOR_PRESENTATION` or `TECH_REPORT` (depends on artifact — talk vs. written report) | `[PRACTITIONER]` | Choose based on the corpus's own description of the artifact type |
| `CUG` | `AUTHOR_PRESENTATION` / `TECH_REPORT` (CUG has no formal peer review) | `[PRACTITIONER]` | CUG (Cray/HPE User Group) presentations are practitioner-facing, not peer-reviewed |
| `VENDOR` | `VENDOR_DOCUMENTATION` | `[VENDOR]` | |
| `TECH-REPORT` | `TECH_REPORT` | `[TECH-REPORT]` | |
| `STATE-OF-PRACTICE` | *(descriptive category, not a governance publication type — describes content, not venue)* | `[PRACTITIONER]` (when sourced from a practitioner artifact) | Use the underlying artifact's actual venue/type tag when available |
| *(center's own self-reported architecture, e.g. `raw/H_centers.md`)* | Closest to `AUTHOR_PRESENTATION` / `official-web` / `documentation` in the provenance-kind hierarchy | `[PRACTITIONER]` | Production/practitioner evidence about one site, not a general research result |

**`BOF` and `PANEL` are domain-specific extensions of the base governance taxonomy**, documented here rather than silently folded into an existing category, since a BoF/panel statement carries materially less evidentiary weight than a reviewed paper and should not be presented as such.

This mapping applies only to **new prose written in this domain's canonical layer** (topic files, `DOMAIN_CONTEXT.md`, etc.). When quoting or characterizing a specific in-corpus tag, prefer citing the original tag as written in the source document over the shorthand, and use the shorthand only as an at-a-glance label.

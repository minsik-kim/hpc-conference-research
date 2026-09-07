# evidence/ — HPC & Quantum

**No new evidence audit was performed during import.** This directory
routes to the evidence-grading conventions and verification records that
already exist inside the imported source project, per
`governance/SOURCE_EVIDENCE_RULES.md` and
`governance/ANTI_HALLUCINATION_RULES.md`.

## Evidence tags used by this domain's corpus (counts as imported)

`[inference]` 117 · `[paper]` 86 · `[official-CFP]` 77 ·
`[paper-preprint]` 72 · `[official-program]` 71 · `[proceedings]` 70 ·
`[code]` 45 · `[abstract]` 25 · `[documentation]` 21 · `[artifact]` 8 ·
`[reconstruction]` 2.

Uncertainty markers preserved exactly: `STATUS_UNCLEAR` (16),
`TOTAL_COUNT_UNVERIFIED` (10), `NOT_FOUND` (114),
`INSUFFICIENT_EVIDENCE` (20). **None of these was promoted or demoted
during import** — a `[paper-preprint]` claim was not relabeled `[paper]`,
an `[inference]` was not relabeled a confirmed fact, and no
`STATUS_UNCLEAR` item was silently resolved.

## Where the verification records live

Both censuses in this corpus were drafted and then independently
verified, with the verification pass recorded inside the same document:

- ASPLOS census — `../corpus/quantum-hpc-survey/corpus/ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`,
  **Appendix A** ("Verification pass record"): 23 claims tested, 18
  confirmed unchanged, 5 corrected (2 material — a proceedings-vs-program
  denominator conflation).
- SC census — `../corpus/quantum-hpc-survey/corpus/SC_2024_2025_QUANTUM_HPC_CENSUS.md`,
  **Appendix D** ("Verification pass record").
- A pre-verification draft of the ASPLOS census is preserved at
  `../corpus/quantum-hpc-survey/working-evidence/CENSUS.pre-verification.bak`
  as the audit trail for Appendix A — it is not a competing current
  version.

## Known evidence limitations carried forward, unresolved

Abstract-only papers (2, ASPLOS), closed-access papers (2, SC), artifact
badge status `UNKNOWN` for all 36 ASPLOS papers (ACM DL was unreachable
from the source research environment), single-source 2025/2026 ASPLOS
volume item counts, and the ASPLOS 2024 program-page truncation
(`STATUS_UNCLEAR` session placement for 5 papers). Full detail:
`../corpus/quantum-hpc-survey/SOURCE_MANIFEST.md` §4.

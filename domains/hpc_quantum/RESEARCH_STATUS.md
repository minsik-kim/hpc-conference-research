# RESEARCH_STATUS — HPC & Quantum

Status: **PARTIAL**

## What is actually complete

**`COMPLETE_AS_CURRENT_SOURCE`**: the `quantum-hpc-survey` source project
(39 files) has been imported into this repository byte-identically from
its staged copy, with no content rewritten, merged, or deduplicated. Within
that project, two full-population regular-paper censuses are themselves
complete as research artifacts: SC 2024–2025 (11 papers) and ASPLOS
2024–2026 (36 papers), each independently verified by a separate
adversarial verification pass (see `evidence/README.md`).

**This is not `COMPREHENSIVE_FIELD_COVERAGE`.** The HPC-Quantum literature
has not been exhaustively surveyed. Specifically still queued and not yet
performed, per the source's own `QUANTUM_HPC_RESEARCH_QUEUE.md`: ISC,
ISCA, HPCA, MICRO, and ICS regular-paper censuses. The source's own venue
map's ISCA/MICRO/HPCA counts were produced by a program-based counting
method that the ASPLOS census later showed undercounts real populations —
those figures are flagged as unverified lower bounds in the source itself,
not corrected during this import (`governance/KNOWLEDGE_BASE_RULES.md` —
preservation over silent reconciliation).

## Known incomplete / pending areas — carried over from the source, not resolved here

1. ASPLOS 2024 program total and five papers' session placement —
   `TOTAL_COUNT_UNVERIFIED` / `STATUS_UNCLEAR`.
2. 28th ASPLOS Volume 4 size — never enumerated.
3. ASPLOS 2026 one-paper discrepancy (168 derived vs. "167 unique" on the
   official page).
4. Artifact badge status for all 36 ASPLOS papers — `UNKNOWN` (ACM DL
   unreachable from the source research environment).
5. Two ASPLOS papers are abstract-only (*A Fault-Tolerant Million
   Qubit-Scale Distributed Quantum Computer*, *ACQC*) — mechanisms not
   inferred.
6. Two SC papers are closed-access (LEXIQL, DQTetris) — entries are
   honestly thin.
7. 2025/2026 ASPLOS volume item counts are single-source (item-level
   records were retained only for the 2024 volumes).
8. MICRO-59 program was unpublished as of the source's last check
   (2026-09-06).
9. ISC, ISCA, HPCA, MICRO, ICS censuses — queued, not performed.

**No web search or new literature research was performed during this
import to close any of these.** They are recorded exactly as the source
recorded them.

## Import-specific notes

- The nine third-party upstream Git repositories used by the source
  project for artifact verification (~800 MB) were **not** copied into
  this repository. Their remotes and HEAD commits are preserved as
  provenance in `implementation/ARTIFACT_REGISTRY.md` — see that file to
  reproduce any of them.
- The user's own `hpc-quantum-warmstart-paper` research project was **not**
  read, referenced, or merged into this domain during import.
- Evidence tags and uncertainty markers (`[inference]`, `[paper]`,
  `STATUS_UNCLEAR`, `TOTAL_COUNT_UNVERIFIED`, `NOT_FOUND`, etc.) were
  preserved exactly as found — none was upgraded or downgraded during
  import. See `evidence/README.md`.
- Research-gap vocabulary (`VENUE_GAP`, `POSSIBLE_CROSSOVER`,
  `OPEN_QUESTION`) was indexed with pointers, not re-evaluated. See
  `research/CANDIDATE_QUESTIONS.md` and `governance/RESEARCH_GAP_RULES.md`.

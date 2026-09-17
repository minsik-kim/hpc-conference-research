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

---

## Evidence conventions and limitations — six-venue census (2026-09-17)

Source project: `../corpus/multi-venue-census-2026/`. Full statement:
that project's `METHODOLOGY.md` §6 and §8–9, and `VERIFICATION_PASS.md`.

### What this census added to the domain's evidence discipline

**Two completeness proofs, with a documented negative result.** *Page-range
tiling* — enumerate every TOC entry with its page range and verify the ranges tile
the volume with zero gaps and zero overlaps — is the strongest available and was
used for ICS (all years), HPCA 2024/2025, MICRO 2024/2025 and QSW 2024/2025.
*DOI-block contiguity* works for **IEEE** volumes, where article IDs follow program
order exactly (verified at 13 anchor points for ISCA 2026), and **fails for ACM**
volumes, where suffixes are not ordered by page or program position — interior
"gaps" resolve to already-enumerated papers. **Do not reuse DOI contiguity on ACM.**

**Modality is recorded per paper** (`REAL_QPU` / `REAL_HARDWARE` /
`FPGA_PROTOTYPE` / `RTL_SYNTHESIS` / `CYCLE_SIMULATION` / `ARCH_SIMULATION` /
`SOFTWARE_SIMULATION` / `ANALYTIC_MODEL` / `PROJECTED`) because it is routinely
mistaken at architecture venues — Pinball is RTL synthesis with cryo-recharacterized
cells, not silicon; gladiator is synthesis only, not a running prototype; Coset's
FPGA claim rests on unreleased RTL.

**`NO_PUBLIC_ARTIFACT_FOUND` was used only after an actual search**; where tooling
failed the record says `UNKNOWN`. Neither means "no code exists".

### Known limitations carried forward

1. **MICRO-59 (2026) unpublished** at census time —
   `PROGRAM_INCOMPLETE_AS_OF_2026-09-17`, four independent probes. Largest open item.
2. **HPCA 2026 denominator `TOTAL_COUNT_UNVERIFIED`, ≥118** — per-article
   pagination defeats page tiling; the publisher-TOC mirror is incomplete by at
   least two (non-quantum) papers.
3. **ISCA 2025 research-track subtotal ±1** (131 program-verified vs 132 from a
   third-party aggregator). Does not affect the numerator.
4. **QSW's regular/short split is unresolvable in the 7-page boundary band** —
   SERVICES allows unlimited reference pages above the main-content limit for both
   categories, so a 7-page total is genuinely ambiguous; this covers 3 of 17 (2024)
   and 6 of 28 (2025) main-track items. **QSW 2026 has no reachable publisher TOC.**
5. **ACM DL (403) and IEEE Xplore (418) were unreachable throughout**, leaving
   several abstracts `INSUFFICIENT_EVIDENCE` rather than recorded — including
   papers marked Gold OA. **Zenodo file downloads were egress-blocked**, so two
   archived artifacts were confirmed to exist but not inspected.
6. **Page summarizers fabricated content twice** during enumeration (three
   plausible-sounding but non-existent paper titles, and a self-contradictory
   total). Both were caught and discarded, which is why every count in that project
   rests on per-entry enumeration plus a second independent source shape, never on
   a reported total.

### Evidence-quality finding worth carrying

**Only 8 of 102 relevant papers touch real quantum hardware.** Everything else is
simulation, synthesis, cycle modelling or analytic projection. This bounds what any
claim in the conference corpus can rest on, and it is a property of the field
rather than of the census.

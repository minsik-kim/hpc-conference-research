# Benchmarking, artifact status, and reproducibility discipline

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **STRONG**. 302 occurrences of "artifact" across the
corpus; both censuses maintain a dedicated artifact/code matrix as a
first-class section (SC census §9, ASPLOS census §12), and this is the
one topic where the two venues are compared on a like-for-like,
numerically verified basis.

## 1. Problem landscape

Public code/artifact availability, and whether a paper's repository
actually supports its published claims, is treated in this corpus as a
first-class evidence question — not an afterthought. The censuses
distinguish `NO_PUBLIC_ARTIFACT_FOUND` from "no code exists" (the former
means only that a public artifact was not located, not that none exists).

## 2. Key concepts

`PUBLIC_CODE` / `PUBLIC_ARTIFACT` / `PARTIAL` / `NO_PUBLIC_ARTIFACT_FOUND`
/ `UNKNOWN` artifact-status vocabulary; `CONSISTENT` / `PARTIAL_MATCH` /
`MISMATCH` / `INSUFFICIENT_EVIDENCE` cross-check verdicts (repository vs.
paper claim); Artifact Evaluation (AE) badges as a formal process distinct
from a paper simply having public code.

## 3. Main mechanism families / findings

- **Artifact rates are statistically indistinguishable between venues**:
  SC 7 of 11 (64%) vs. ASPLOS 22 of 36 (61%) — **despite ASPLOS running a
  formal Artifact Evaluation process and SC not requiring one.** Process
  does not move the rate.
- **Artifact *kind* is nearly identical too**: of ASPLOS's ~22 artifacts,
  ~16 are Python/C++ simulation or compiler code. **Exactly one of 36
  ASPLOS papers ships a hardware description** (Micro Blossom,
  Scala/SpinalHDL). Promatch claims an FPGA synthesis result but publishes
  only C++/MPI — no HDL.
- **AE badges are voluntary and publicly invisible.** The ASPLOS AEC sites
  state badges are "printed on the papers themselves and available as
  meta information in the ACM Digital Library" and nowhere else — with ACM
  DL unreachable from the source research environment, badge status is
  `UNKNOWN` for all 36 ASPLOS papers. This invisibility is itself recorded
  as a finding, not merely a limitation.
- **Repository-vs-paper divergence goes both directions.** Micro Blossom's
  README exceeds its paper's claims (367 ns and 110 logical qubits appear
  in the README but not the paper); Promatch's repository is *weaker* than
  its paper (no HDL for the FPGA claim the paper makes).

## 4. Representative papers

Micro Blossom (README-exceeds-paper case), Promatch (repo-weaker-than-paper
case), GUOQ (ships baseline Docker image alongside its own — a positive
reproducibility example), Qonductor (preprint-vs-published title/framing
divergence, caught by direct comparison — see §7).

## 5. Historical lineage

Not applicable — this is a cross-cutting evidence-discipline topic, not a
technique lineage.

## 6. Implementation families

Both censuses performed direct code inspection (`[code]`-tagged) rather
than trusting README claims alone — e.g. Atlas's repository was read down
to specific function signatures and NCCL/MPI call sites (see
`quantum_simulation_distributed_gpu.md` §6).

## 7. Important disagreements / tensions

**Preprint-vs-published divergence is not hypothetical**: the SC census
directly compared Qonductor's arXiv preprint against its published SC25
PDF and found a title divergence (arXiv v1: *"Orchestrating Quantum Cloud
Environments with Qonductor"*) — cited by the source as direct evidence
that its own preprint-caveat is not merely theoretical
(`SC_2024_2025_QUANTUM_HPC_CENSUS.md:125,163`).

## 8. Current limitations

Two ASPLOS papers are abstract-only (mechanisms not inferred); two SC
papers are closed-access (LEXIQL, DQTetris — entries are honestly thin).
Artifact badge status is `UNKNOWN`, not `NONE`, for all 36 ASPLOS papers —
this is an evidence-access limitation of the source research environment,
not a finding that ASPLOS papers lack badges.

## 9. Research questions

Not indexed in `../research/CANDIDATE_QUESTIONS.md` — the artifact-rate
and artifact-kind findings are treated by the source as established
findings (F5 in the ASPLOS census), not open questions.

## 10. Deeper lookup paths

`SC_2024_2025_QUANTUM_HPC_CENSUS.md` §9 (artifact matrix) →
`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §12 (artifact matrix, AE process
and visibility subsection 12.5) → individual repositories listed in
`../implementation/ARTIFACT_REGISTRY.md` for reproduction.

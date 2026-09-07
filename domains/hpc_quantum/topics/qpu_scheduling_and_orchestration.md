# QPU scheduling and cloud/fleet orchestration

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **MODERATE**. 117 occurrences of "scheduling" across the
corpus, but concentrated in a small number of named papers rather than a
dedicated deep-dive document. Quantum workflow systems / hybrid runtime
are folded into this topic file rather than given a separate one, since
the source's own coverage of that adjacent area is itself only a
`VENUE_GAP` observation, not a researched branch.

## 1. Problem landscape

Two distinct problems appear under this heading in the source: (a)
real-time QEC scheduling (a hard-deadline systems problem, covered more
fully in `qec_decoding.md`), and (b) fleet-level/cloud orchestration of
QPU jobs across a shared resource pool (a batch/queueing problem closer to
classical HPC job scheduling).

## 2. Key concepts

Real-time vs. batch scheduling; cloud orchestration of a heterogeneous QPU
fleet; fleet imbalance characterization; hybrid CPU/GPU/QPU execution
model.

## 3. Main mechanism families

- **Cloud orchestration** — Qonductor (SC25): a cloud orchestrator for
  quantum computing; its headline evaluation runs on eight Qiskit
  FakeBackends, with real IBM devices used only to build a training
  dataset and characterize fleet imbalance. The source flags the widely
  quotable "evaluated on 7,000+ real quantum runs" as precise but easy to
  misread (`SC_2024_2025_QUANTUM_HPC_CENSUS.md:84`).
- **Real-time QEC scheduling** — RESCQ (ASPLOS'25): real-time, not batch;
  see `qec_decoding.md` for decoding-specific detail.

## 4. Representative papers

Qonductor (SC25, `PUBLIC_CODE`, resource management / orchestration —
`Q_IN_HPC`), RESCQ (ASPLOS'25).

## 5. Historical lineage

Not established as a lineage in the source — Qonductor is explicitly
noted as arriving "once" at SC (SC25), with the source marking whether it
represents the start of a branch or a one-off as `INSUFFICIENT_SAMPLE`
(`../research/CANDIDATE_QUESTIONS.md` entry G6).

## 6. Implementation families

Qonductor's repository was cross-checked against both its arXiv preprint
and its published SC25 PDF — the source records a **preprint-vs-published
divergence** (title differs: arXiv v1 is *"Orchestrating Quantum Cloud
Environments with Qonductor"*).

## 7. Important disagreements / tensions

None recorded between papers in this topic; the source's own caution
(evaluation-methodology legibility of the "7,000+ real quantum runs"
figure) is a within-paper evidence-quality note, not a cross-paper
tension.

## 8. Current limitations

Hybrid CPU/GPU/QPU runtime and execution model is recorded as a
`VENUE_GAP` absent from SC's main track (the source's Phase-1 map places
this work at OSDI instead — QOS, HyperQ, qTPU) — see
`../research/CANDIDATE_QUESTIONS.md` entry G4. Quantum workflow systems
more broadly are `PARTIAL_IN_SOURCE` per `TOPIC_MAP.md` — mentioned as a
venue-gap observation, not researched as a technical topic in this corpus.

## 9. Research questions

See `../research/CANDIDATE_QUESTIONS.md` entries G4, G6, G7, G8.

## 10. Deeper lookup paths

`SC_2024_2025_QUANTUM_HPC_CENSUS.md` §4.1 (Qonductor full entry) → §8
(venue-gap table, rows on hybrid runtime, scheduling, programming models,
HPC-centre integration) → `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` RESCQ
entry.

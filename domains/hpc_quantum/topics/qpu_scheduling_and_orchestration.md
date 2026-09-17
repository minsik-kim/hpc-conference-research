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

---

## Phase-2 extension — six-venue census (2026-09-17)

Source: `../corpus/multi-venue-census-2026/DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md`
§C and Group 2. Descend there for quantitative claims.

**The branch is thin everywhere and fragmenting rather than converging** — ~10
papers across the six venues (12 including SC's Qonductor and ASPLOS's RESCQ),
against 1,281 screened papers. Distribution: QSW 4, ISC 2, ISCA 2, ICS 1, MICRO 1,
HPCA 0.

### The three real schedulers share one abstraction and differ on where the queue lives

Code-level comparison of **Qoncord** (MICRO 2024), **MILQ** (ISC 2024) and
**Qonductor** (SC 2025) shows all three reduce a QPU fleet to a **job × backend
cost matrix plus a per-backend capacity** — the classical *unrelated parallel
machines* abstraction. They diverge on the queue and the objective:

| | Qoncord | MILQ | Qonductor |
|---|---|---|---|
| QPU modelled as | a **single-server FIFO queue** with a stochastic fidelity draw | a **machine** with sequence-dependent setup and a qubit-capacity constraint permitting **co-residency** | a **machine with an explicit queue attached** (`waiting_times` as a first-class input) |
| Objective | greedy two-phase policy (explore low-fidelity, fine-tune high-fidelity) | `LpMinimize` on makespan only | **bi-objective NSGA2** (time and fidelity, resolved by pseudo-weights) |
| Solver | hand-coded policies | PuLP → Gurobi/CBC | pymoo NSGA2 |

**A QPU is never modelled as a memory hierarchy in any of them.** MILQ's
per-timestep qubit-capacity constraint is the closest thing to an occupancy model,
and it is space-sharing, not hierarchy.

### Two findings that bound how this branch can be used

**No scheduler integrates with a real batch system.** Slurm appears in no
scheduler's code or evaluation anywhere in the census. QSW 2026's **qScheduler** —
a hybrid **reservation-plus-dispatch** design, i.e. the Slurm-shaped idea — is the
closest thing to an HPC-centre batch scheduler in the corpus, **and its artifact
URL 404s**. Recorded as `CANDIDATE` M7.

**Evaluation is synthetic.** Qoncord's 17.4× is wall-clock including queue delays
against a single-device high-fidelity baseline, over **10 synthetic devices with
simulated noise models and no real QPU execution**, and no shipped script emits the
headline. MILQ's 26% is against a **bin-packing** baseline on three 5-qubit Qiskit
fake devices.

### New in this corpus: runtime work that is not fleet scheduling

- **Qtenon** (ISCA 2025) — host↔QPU integration latency: where the QPU sits in the
  memory/IO hierarchy, driver overhead, offload granularity. The GPU-offload
  question transplanted to a QPU.
- **ARTERY** (ISCA 2025) — **branch prediction** imported into the real-time
  control processor to hide classical feedback latency inside coherence.
- **The ISC 2026 HPCQC observable-measurement runtime** — a hierarchical runtime
  making shot distribution a load-balancing problem over classical workers, with
  variance-aware balancing and a compilation cache. A genuinely new sub-branch.
- **Distributed-HISQ** (MICRO 2025) — a control ISA plus a booking-based
  synchronization protocol, evaluated on **real hardware driving a 66-qubit chip**:
  the strongest evaluation anywhere in the census.

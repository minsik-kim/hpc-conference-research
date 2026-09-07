# Quantum simulation — GPU-accelerated and distributed

last_updated: 2026-09-07
last_checked: 2026-09-07
knowledge_as_of: source corpus imported 2026-09-06/07 (SC 2024–2025, ASPLOS 2024–2026)

Coverage status: **STRONG**. 305 occurrences of "simulation" across the
corpus; the branch has a dedicated deep-dive document
(`arch_sim_deepdive.md`) and is the branch the two censuses compare most
directly against each other, because it is SC's largest branch (4 of 11)
and ASPLOS's smallest (1 of 36) — an exact mirror image of the QEC
asymmetry (`QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:121`).

## 1. Problem landscape

Classical simulation of quantum circuits is memory- and communication-
bound: a full statevector or decision-diagram representation can exceed
one device's memory, forcing partitioning across GPUs/nodes and
introducing a communication cost for cross-partition (global-qubit) gates.

## 2. Key concepts

Statevector vs. decision-diagram (DD) representation; local vs. global
qubits; hierarchical multi-GPU partitioning; batched circuit execution;
tensor-network / random-circuit sampling as an alternative simulation
strategy.

## 3. Main mechanism families

- **Batched decision-diagram simulation, single GPU** — BQSim (ASPLOS'25):
  a data-structure and batching insight, not a distributed-scale claim.
- **Hierarchical multi-GPU partitioning** — Atlas (SC24): three-level
  hierarchy (local / regional / global qubits) solved via an ILP
  formulation (PuLP), with an explicit DP variant and stage-count ILP;
  code-verified (`[code]`) to use MPI+NCCL collective all-to-all for
  cross-node statevector shuffle.
- **Neutral-atom compiler under hardware constraints** — Parallax (SC24).
- **Tensor-network / MPS simulation at scale** — "Realizing Quantum Kernel
  Models at Scale with Matrix Product State Simulation" (SC24).
- **Pre-trajectory sampling for noisy data generation at scale** — PTSBE
  (SC25).

## 4. Representative papers

BQSim (ASPLOS'25, `PUBLIC_CODE`, C++/CUDA, 16 MQT-Bench circuits with
baselines included); Atlas (SC24, `PUBLIC_ARTIFACT`, code-verified MPI+NCCL
implementation, ILP scheduler in a Quartz submodule); Parallax (SC24);
PTSBE (SC25); the Matrix Product State paper (SC24).

## 5. Historical lineage

BQSim (ASPLOS'25) and Atlas (SC24) are read by the source as **the same
class of contribution, framed by two different scarcities**: BQSim's
scarce resource is device memory and DD irregularity; Atlas's is
inter-node communication (`QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:107-119`).
This is presented as an analogy the source draws, not a claimed lineage
between the two papers' authors.

## 6. Implementation families

`PUBLIC_CODE` cross-checked directly against source (`[code]` tag): Atlas's
repository was read down to specific symbols
(`compute_qubit_layout_with_ilp`, `get_local_swaps_from_previous_stage`,
`ncclGroupStart`/`all2all`/`ncclGroupEnd`, `MPI_Bcast` for NCCL bootstrap)
— see `../implementation/ARTIFACT_REGISTRY.md` for the `atlas`,
`atlas-artifact`, and `quartz` repository provenance (remote + HEAD
commit; not copied into this repository).

## 7. Important disagreements / tensions

None recorded between simulation papers themselves in the source; the
tension recorded is structural — this branch is a `VENUE_GAP` in both
directions simultaneously (SC's largest branch, ASPLOS's near-absent one)
— see `../research/CANDIDATE_QUESTIONS.md` entry G2.

## 8. Current limitations

The source explicitly reads BQSim-to-Atlas-scale generalization as
**"already crossed elsewhere"** (i.e., the crossover this branch might
represent is judged to already exist at SC) rather than an open crossover
— see `../research/CANDIDATE_QUESTIONS.md` entry C3, still `CANDIDATE`
status, not independently confirmed.

## 9. Research questions

See `../research/CANDIDATE_QUESTIONS.md` entries G2, C3.

## 10. Deeper lookup paths

`corpus/quantum-hpc-survey/corpus/data/asplos/arch_sim_deepdive.md` →
`SC_2024_2025_QUANTUM_HPC_CENSUS.md` §3.5–3.7 (Atlas, MPS, Sycamore
entries) → original repositories listed in `../implementation/ARTIFACT_REGISTRY.md`.

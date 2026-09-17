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

`../corpus/quantum-hpc-survey/corpus/data/asplos/arch_sim_deepdive.md` →
`SC_2024_2025_QUANTUM_HPC_CENSUS.md` §3.5–3.7 (Atlas, MPS, Sycamore
entries) → original repositories listed in `../implementation/ARTIFACT_REGISTRY.md`.

---

## Phase-2 extension — six-venue census (2026-09-17)

Source: `../corpus/multi-venue-census-2026/DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md`
Group 1 and §A. Descend there for any quantitative claim.

**~10 papers across ICS (4), QSW (3), ISCA (2) and HPCA (1). MICRO published no
classical-simulation quantum paper in either censused year** — a real structural
difference from ASPLOS, ISCA and ICS, verified by whole-volume scan.

### The central finding: this branch is mostly *memory* work, not *communication* work

Of the six simulation papers cross-validated against their code, **four attack the
memory term on a single device** by four different routes — lossy compression
(BMQSim: nvCOMP bitcomp plus a GPU log-transform, 42 qubits in 16 GB and 47 with
SSD staging), representation change (quEStab: extended stabilizer tableau, peak
memory down up to 10,126×, circuits to 30,000 qubits), dataflow and adaptive
memory scheduling (the HPCA 2026 Schrödinger accelerator, >50× over a GPU Qiskit
baseline), and structural elision (MQT identity-level stripping).

**Only two attack communication, and they are precisely the two that run on
multi-node supercomputers:** C-3PQ (closeness-centrality partitioning, MPI with
GPU-aware cray-mpich collectives, weak-scaled 30→37 qubits on Perlmutter, Frontier
and Fugaku) and the QSW 2024 decision-diagram ring simulator (bucket-relay ring
replacing broadcast on 256 A64FX nodes of Wisteria-O).

**BMQSim's "multi-GPU" mode has no inter-GPU communication at all** — each GPU
processes partial state-vector groups locally — and caps at **2.3× on 4 GPUs**,
PCIe-bound. This is worth holding onto: the vocabulary of multi-GPU simulation
does not imply a communication term is being addressed.

### The one measured negative crossover in the domain

The DD ring simulator's **26×** is specifically **38-qubit Shor at 256 nodes vs
single-node** (3,881 s → 147 s). The same paper reports **20-qubit QCBM peaking at
32–64 nodes and getting *slower* at 128 and 256** — communication overhead
overtaking the decision diagram's node sharing. **The crossover is data-dependent,
not qubit-count-dependent**, and this is the corpus's only direct measurement of
distributed scaling going the wrong way (`CANDIDATE` M6).

### Artifact asymmetry worth noting

**Every multi-node simulation paper in this branch has no public artifact** —
C-3PQ, BMQSim, quEStab and the DD ring simulator alike; the QSW paper explicitly
promised a URL after review that never appeared. The branch whose results are most
reproducible-in-principle publishes the least code, the inverse of the QEC branch.

Open candidate M5: whether compression (BMQSim) and inter-node partitioning
(C-3PQ) **compose** is evaluated by no paper — each design forgoes what the other
does. See `../research/CANDIDATE_QUESTIONS.md` §5.

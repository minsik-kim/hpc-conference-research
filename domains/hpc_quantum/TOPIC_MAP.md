# TOPIC_MAP — HPC & Quantum

Status: **PARTIAL** — routing table reflects one imported source project
(`corpus/quantum-hpc-survey/`), measured directly against its files at
import time. Not a claim about the wider literature.

## 1. Status vocabulary (defined here; used consistently below)

- **STRONG** — a named branch in the source's own taxonomy, with a
  dedicated deep-dive or lineage document and multiple representative
  papers analyzed in depth.
- **MODERATE** — a named branch with several representative papers but no
  dedicated deep-dive document; coverage is real but shallower.
- **PARTIAL** — mentioned only incidentally inside individual paper
  analyses (a handful of occurrences), not itself a researched topic.
- **NOT_COVERED** — zero or near-zero occurrences in the source; no topic
  file exists for it. This means *absent from this workspace*, not *absent
  from the literature* (`governance/ANTI_HALLUCINATION_RULES.md`).

## 2. Routing table

| Topic | Coverage | Topic file | Representative source files | Representative mechanisms/papers |
|---|---|---|---|---|
| QEC decoding (systems/throughput problem) | **STRONG** | `topics/qec_decoding.md` | `qec_deepdive.md`, `ASPLOS_…_CENSUS.md` §8, `ARCHITECTURE_LINEAGES.md` | Promatch (fixed-capacity predecoding), Micro Blossom (O(d³) growing-machine decoder), AlphaSyndrome, HetEC |
| Quantum simulation — GPU/distributed | **STRONG** | `topics/quantum_simulation_distributed_gpu.md` | `arch_sim_deepdive.md`, both censuses | BQSim (batched decision-diagram, single GPU), Atlas (hierarchical multi-GPU partitioning), Parallax, PTSBE |
| Compilation / mapping and its classical cost | **STRONG** | `topics/compilation_and_classical_cost.md` | `compilation_deepdive.md`, `ASPLOS_…_CENSUS.md` §10.2 | GUOQ, QTurbo, PowerMove, Fermihedral, trasyn |
| Benchmarking / artifact & reproducibility discipline | **STRONG** | `topics/benchmarking_and_artifacts.md` | both censuses' artifact matrices (§9/§12) | Artifact rate comparison (SC 64% vs ASPLOS 61%), AE badge invisibility, one HDL artifact in 36 papers |
| QPU scheduling / cloud & fleet orchestration | **MODERATE** | `topics/qpu_scheduling_and_orchestration.md` | SC census §4.1, ASPLOS RESCQ entry | Qonductor (cloud orchestrator), RESCQ (real-time QEC scheduling) |
| Modular / multi-QPU architecture | **MODERATE** | `topics/modular_multi_qpu_architecture.md` | `ASPLOS_…_CENSUS.md` §9, `ARCHITECTURE_LINEAGES.md` | MECH, COMPAS, chiplet codesign, DQTetris |
| VQE / variational algorithms / NISQ mitigation | **PARTIAL** | `topics/variational_algorithms_and_nisq.md` | incidental mentions inside `arch_sim_deepdive.md` and both censuses | TreeVQA, Clapton, VarSaw, Red-QAOA, Elivagar (as census subjects, not a VQE methods review) |
| ansatz | **PARTIAL** | *(covered inside `variational_algorithms_and_nisq.md`)* | 6 occurrences, taxonomy/description only | — |
| UCC / UCCSD | **PARTIAL** | *(covered inside `variational_algorithms_and_nisq.md`)* | 5 occurrences, 4 inside one paper's benchmark description (H₂/LiH/BeH₂ under SPSA/COBYLA) | — |
| ADAPT-VQE | **PARTIAL** | *(covered inside `variational_algorithms_and_nisq.md`)* | exactly 1 mention, `arch_sim_deepdive.md:544`, related-work context | — |
| measurement reduction / commuting-group tiling | **PARTIAL** | *(covered inside `variational_algorithms_and_nisq.md`)* | exactly 1 mention, `arch_sim_deepdive.md:545` | — |
| Quantum chemistry (classical QC/many-body/DFT/NNQS) | **NOT_COVERED as a topic — PRESENT as an exclusion criterion** | *(covered inside `variational_algorithms_and_nisq.md`, "what is excluded")* | SC census Appendix A.1, venue map, research queue | Documented as the corpus's dominant false-positive class; excluded, not surveyed |
| Hybrid quantum-classical cost (compile-time currency, four-pathway acceptance model) | **STRONG** | *(covered inside `topics/compilation_and_classical_cost.md`)* | SC census §7, ASPLOS census §10 | SC's 3-of-3 compile-time-scalability argument vs ASPLOS's 2-of-10 |
| Quantum workflow systems / hybrid runtime | **PARTIAL** | *(covered inside `topics/qpu_scheduling_and_orchestration.md`)* | SC census §8 venue-gap table | Hybrid CPU/GPU/QPU runtime named as a `VENUE_GAP` at SC (found at OSDI instead per the source's Phase 1 map) |
| Classical optimizer studies | `NOT_COVERED` | — | 0 occurrences beyond generic "optimization" | — |
| Initialization / warm-start | `NOT_COVERED` | — | 1 occurrence total, unrelated context | — |
| Barren plateaus / trainability | `NOT_COVERED` | — | 0 occurrences | — |
| Gradient estimation (parameter-shift etc.) | `NOT_COVERED` | — | all "gradient" hits are classical conjugate-gradient solvers in program tables — unrelated | — |
| Excited-state methods | `NOT_COVERED` | — | 1 occurrence, itself a false-positive exclusion example (a GW excited-state HPC paper excluded as classical chemistry) | — |

## 3. What this table is not

This is a routing table over **one imported source project**, not a claim
about HPC-Quantum research as a whole. A `NOT_COVERED` row means this
repository currently has nothing to retrieve on that subtopic — it must
never be read as "this subtopic does not exist" or "no gap analysis is
needed" (`governance/ANTI_HALLUCINATION_RULES.md`,
`governance/RESEARCH_GAP_RULES.md`).

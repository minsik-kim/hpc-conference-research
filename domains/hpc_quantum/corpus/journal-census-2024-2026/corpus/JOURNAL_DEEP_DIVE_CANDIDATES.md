# JOURNAL_DEEP_DIVE_CANDIDATES

**Which of the 89 included journal papers are worth a full Phase-3 deep dive, and why.**

Compiled 2026-09-17 (KST), after the census and its verification pass. This is a **selection**, not
the deep dives themselves — deep reading is a separate phase, as it was for the conference corpus.

Selection criteria, applied in this order: branch representativeness · strength of the classical
systems contribution · substantial scale in the evaluation · a mechanism that has no equivalent in
the existing SC/ASPLOS corpus, or a direct comparison to one that does · public artifact ·
relevance to a future CPU/GPU/QPU heterogeneous system. **Eighteen papers. The list was not padded to
a target number**, and papers were dropped from it where the census could only record
`INSUFFICIENT_EVIDENCE` for the mechanism.

---

## Tier 1 — read these first (6)

These six are the papers that change what this domain can say about HPC-centre quantum integration.

### 1. Closed-loop calculations of electronic structure on a quantum processor and a classical supercomputer at full scale
`10.1016/j.future.2026.108731` · FGCS · 2026 · v186 · Shirakawa et al. (21 authors) · arXiv 2511.00224
**Why.** An on-premises IBM Heron QPU in a closed loop with the **entire 152,064-node Fugaku
allocation**. It is the only paper in the corpus that puts a real QPU and a full-scale named
supercomputer in the same measured workflow, and it is the single best answer to the question
"how much real QPU + HPC coupling actually exists". Read for the orchestration design and the
scalability characterisation of the hybrid loop, **not** for the chemistry result.
Artifact `NO_PUBLIC_ARTIFACT_FOUND`. Deep-dive priority 5.

### 2. Three ways to share a QPU: Scheduling strategies for hybrid Quantum-HPC applications
`10.1016/j.future.2026.108699` · FGCS · 2026 · v185 · Cipollini et al. (24 authors) · arXiv 2604.14955
**Why.** Three implemented strategies compared head to head on production clusters with real QPUs:
time-multiplexed QPU access, dynamic resource management with malleability, and workflow
decomposition. Reported classical-resource reductions of up to 45.7% and 64% respectively, with
time-multiplexing best for QPU utilisation. This is the closest thing in the corpus to an operational
answer for a computing centre, and `qpu_scheduling_resource_mgmt` is the branch that is nearly absent
from both censused conferences (1 paper at SC, 1 at ASPLOS). Artifact `UNKNOWN`. Priority 5.

### 3. Universal quantum computer simulation of 50 qubits on Europe's first exascale supercomputer
`10.1016/j.future.2026.108592` · FGCS · 2026 · v183
**Why.** JUQCS-50 on JUPITER: CPU–GPU interconnect and LPDDR5 used to push usable memory past GPU
capacity, plus adaptive data encoding trading precision for reach. Reports a 16.6× speedup, with the
baseline explicitly the earlier 48-qubit JUQCS run on the K computer — **note that this compares two
machines and two software generations, not one optimisation**. The direct journal counterpart to SC's
Atlas and Surpassing Sycamore. Priority 5.

### 4. FPGA-Based Distributed Union-Find Decoder for Surface Codes
`10.1109/tqe.2024.3467271` · TQE · 2024 · v5
**Why.** The corpus's canonical QEC-classical-processing paper and the only hardware decoder in all
eight journals. Helios hybrid tree-grid processing elements on a Xilinx VCU129; 11.5 ns average
decoding time per measurement round at d=21 under phenomenological noise, 23.7 ns at d=17 under
circuit-level noise, 544 ns/round at d=51 in the resource-optimised configuration; O(d³) parallel
resources buy sublinear average time complexity in d. This is the paper to read against ASPLOS's
Micro Blossom and Promatch, and it is the evidence for the `JOURNAL_GAP` observation that no
classical-systems journal publishes this work. Priority 5.

### 5. C3-VQA: Cryogenic Counter-Based Coprocessor for Variational Quantum Algorithms
`10.1109/tqe.2024.3521442` · TQE · 2025 · v6
**Why.** A classical coprocessor placed **inside the cryostat**, with a 30–87% reduction in 4 K heat
dissipation against no coprocessor. It is the cleanest example in the corpus of the classical side of
a quantum machine being designed against a physical budget (thermal, not just latency), which is the
constraint an HPC systems person will not have priced in. Priority 5.

### 6. Efficient and scalable branch-and-bound algorithm for exact qubit allocation
`10.1016/j.future.2025.108342` · FGCS · 2025 · v179 · **PUBLIC_CODE** github.com/Guillaume-Helbecque/P3D-DFS
**Why.** The one paper in the corpus that argues exactly like an SC compilation paper *and* ships
code: qubit allocation reformulated as a permutation-based quadratic assignment problem, a refined
sequential branch-and-bound, then a distributed parallel implementation reaching **>87% of linear
speedup on 128 cores and 74% of ideal speedup on 64 nodes (8,192 cores)**, beating previous exact
approaches on 20 of 21 benchmarks. The paper-to-code chain can be closed. Priority 5.

---

## Tier 2 — branch representatives (8)

### 7. Network-Assisted Collective Operations for Efficient Distributed Quantum Computing
`10.1109/tqe.2025.3619387` · TQE · 2025 · v6
The most HPC-shaped paper in a quantum-native journal — collective operations, transplanted. Read
against the multi-QPU thread at ASPLOS (COMPAS, MECH).

### 8. ARQUIN: Architectures for Multinode Superconducting Quantum Computers
`10.1145/3674151` · TQC · 2024 · v5 i3
The corpus's reference multinode-architecture study; a co-design roadmap balancing entanglement
generation, distillation and local architecture rather than a single speedup number
(`BASELINE_UNCLEAR` by construction). The journal anchor for `multi_qpu_distributed_qc`.

### 9. Lazy Qubit Reordering for Accelerating Parallel State-Vector-based Quantum Circuit Simulation
`10.1145/3748261` · TQC · 2025 · v6 i4 · arXiv 2410.04252
Up to 54× for state update and 606× for expectation-value computation on **32-GPU** executions, plus
up to 15% communication reduction on two-layered clusters. The engine-level counterpart to TPDS's
cluster-level work; check the baselines carefully, the two numbers are measured differently.

### 10. Communication-Partition Co-Optimization for Quantum Circuit Simulation on CPU+GPU Clusters
`10.1109/tpds.2026.3678345` · TPDS · 2026 · v37 i6
One of only two TPDS papers in three years, and the cluster-level member of the simulation stack:
replaces gate-unaware full-data exchange (QuEST-style) with communication-partition co-optimisation.
Read together with `10.1109/tpds.2026.3652733` (Minimizing Communications of Quantum Circuit
Simulations on Distributed Systems, same year).

### 11. QuCloud+: A Holistic Qubit Mapping Scheme for Single/Multi-programming on 2D/3D NISQ Quantum Computers
`10.1145/3631525` · TACO · 2024 · v21 i1 · `RELATED_LINEAGE` to QuCloud (HPCA 2021)
The multiprogramming frame — a QPU as a shared machine with utilisation as the objective — which is
the frame a supercomputing centre will recognise immediately. Also the corpus's clearest lineage case
to test the conference-extension question against.

### 12. AdaptDQC: Adaptive Distributed Quantum Computing With Quantitative Performance Analysis
`10.1109/tc.2025.3586027` · TC · 2025 · v74 i10
Models circuits and inter-chip communication architecture in one spatial-temporal graph. The
architecture-level distributed-QC record, and the bridge between TC's substrate work and TCAD's
compilation work.

### 13. Effective and Efficient Parallel Qubit Mapper
`10.1109/tcad.2024.3500784` · TCAD · 2024 · v44 i5
The branch owner's representative: a **parallel** mapper whose objective is mapping time as well as
depth — the discriminator that separates it from the fidelity-objective mapping papers TCAD publishes
in bulk.

### 14. ZAP: Zoned Architecture and Performant Compiler for Field-Programmable Atom Array
`10.1109/tqe.2026.3696707` · TQE · 2026 · v7
Compiler/architecture co-design for neutral atoms. The direct journal counterpart to SC's PARALLAX
and ASPLOS's PowerMove; useful for testing whether the compile-time-scalability argument travels into
journal form.

---

## Tier 3 — read for a specific comparison (4)

### 15. Integrating quantum computing resources into scientific HPC ecosystems
`10.1016/j.future.2024.06.058` · FGCS · 2024 · v161
### 16. Bridging paradigms: Designing for HPC-Quantum convergence
`10.1016/j.future.2025.107980` · FGCS · 2025 · v174
Read as a pair. Both are hardware-agnostic HPC-centre stack designs (gateway interface, platform
manager API, resource-management APIs, scheduler support), both `BASELINE_UNCLEAR` because neither is
a measured paper. Their value is that they state what an HPC centre thinks the integration problem
*is* — which is the framing no conference paper in the existing corpus supplies.

### 17. HiMA: Hierarchical quantum microarchitecture for qubit-scaling and quantum process-level parallelism
`10.1016/j.future.2026.108484` · FGCS · 2026 · v182 · arXiv 2408.11311
Up to 4.89× speedup with a 5-process parallel setup and 3.55× CLOPS improvement, baseline the same
system single-process, **on a deployed 102-qubit processor**. Process-level parallelism on a real
machine is a shape that does not appear in the conference corpus at all.

### 18. Integration of Quantum Accelerators with High Performance Computing — A Review of Quantum Programming Tools
`10.1145/3743149` · TQC · 2025 · v6 i3 · `BIBLIOGRAPHY_HUB`
Not original research and not counted in any population figure, but it is the best single navigation
document for the HPC-QPU software-stack literature and the fastest route to predecessor work.
Pair with `10.1145/3762672` (Simulation of Quantum Computers: Review and Acceleration Opportunities).

---

## Deliberately not selected

- **Papers whose only measured quantity is a quantum resource.** Several strong compilation papers in
  TCAD and TQC report gate count, depth or fidelity only. They are in the census; they will not teach
  a systems reader anything about classical cost.
- **`qfusion-opt`** (`10.1109/tcad.2026.3680784`) is exactly the kind of paper this list wants —
  profile-informed gate scheduling and fusion for simulation — but the census could only reach its
  title. It is `INSUFFICIENT_EVIDENCE`, and it heads the follow-up list rather than this one.
- **TQE's benchmarking cluster** (QKNOB circuits, QEC controller benchmarking, cross-model Hamiltonian
  simulation benchmarking) is real and useful, but it is infrastructure rather than mechanism; read it
  when building an evaluation, not when mapping the landscape.

---

## Before any deep dive, close these

1. **Artifact status.** 68 of 89 included papers are `artifact_status: UNKNOWN`, meaning *not checked*
   — IEEE Xplore, ACM DL badge pages and Elsevier full text were unreachable. Ten repositories are
   confirmed. The paper-to-code chain cannot be closed for most of this list until that is fixed.
2. **Conference-extension lineage.** Zero `CONFIRMED_EXTENSION` records. Until publisher front matter
   is read, a deep dive risks analysing a journal paper as an independent contribution when it is an
   extension of a conference paper already in the corpus.
3. **Truncated quantitative claims.** Several records carry a claim whose figures were cut by abstract
   truncation (`AdaptDQC`, `Effective and Efficient Parallel Qubit Mapper`, the TPDS
   communication-partition paper). Restore the numbers from full text before quoting any of them.

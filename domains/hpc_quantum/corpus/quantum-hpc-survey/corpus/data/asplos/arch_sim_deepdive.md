I have gathered the material. Here is the analysis.

---

# ASPLOS 2024–2026: HPC-Transferable Quantum Papers — Deep Technical Census

## Sourcing note (read first)

ACM DL is blocked (403 on `/doi/` and `/doi/pdf/`); direct `curl` egress is blocked entirely (proxy `connect_rejected`, so `tsung-wei-huang.github.io` and GitHub raw were reachable only through WebFetch). Source tags:

| Paper | Best source obtained | Tag |
|---|---|---|
| 1 BQSim | **Author-hosted PDF of the published ASPLOS'25 version** (`tsung-wei-huang.github.io/papers/2025-asplos.pdf`) + repo files | `[paper]` `[code]` |
| 2 Million-Qubit (SNU) | **Verbatim abstract only** (Semantic Scholar). Unpaywall: `is_oa: false`, `oa_status: closed`, `oa_locations: []`. No arXiv preprint, no repo in the SNU-HPCS GitHub org | `[abstract]` |
| 3 MECH | arXiv 2305.05149 full text | `[paper-preprint]` |
| 4 Fat-Tree QRAM | arXiv 2502.06767v1 full text | `[paper-preprint]` |
| 5 ACQC | **Verbatim abstract only**. Unpaywall: `is_oa: true`, `oa_status: gold`, but `url_for_pdf: null` — the only OA location is ACM DL itself, which is blocked here | `[abstract]` |
| 6 COMPAS | arXiv 2511.23434v2 full text + repo README | `[paper-preprint]` `[code]` |
| 7 QRCC | arXiv 2312.10298v3 **and** the published camera-ready PDF (`xzt102.github.io/publications/QRCC_ASPLOS2024.pdf`) — cross-checked | `[paper-preprint]` `[paper]` |
| 8 TreeVQA | arXiv 2512.12068 full text + repo README | `[paper-preprint]` `[code]` |

**Two papers (2 and 5) are abstract-only.** Both are from the same SNU group, both make large architectural claims, and neither is independently readable from this environment. I have not inferred their mechanisms.

Volume mapping cross-checked against your `VOLUME_STRUCTURE.md`: BQSim + Fat-Tree QRAM = `3676641` (ASPLOS'25 V2); Million-Qubit + MECH = `3620665` (ASPLOS'24 V2); ACQC + COMPAS + TreeVQA = `3779212` (ASPLOS'26 V2); **QRCC = `3622781` (29th, V4) — proceedings year 2024, presented at ASPLOS 2025**, the one paper in this set where the two denominators diverge.

---

# PART A — PER-PAPER ANALYSIS

---

## 1. BQSim (ASPLOS 2025, DOI 10.1145/3676641.3715984)

Shui Jiang, Yi-Hua Chung, Chih-Chun Chang, Tsung-Yi Ho, Tsung-Wei Huang — CUHK / UW–Madison. **Source is the published version**, not a preprint. `[paper]`

### 1. Research question
Not "simulate one big circuit faster." **Batch Quantum Circuit Simulation (BQCS)**: run *many different input state vectors* through *one fixed circuit*. The paper's framing verbatim: existing simulators focus on "strong scaling within a single input (i.e., state vector)" and therefore leave "substantial data parallelism in BQCS" on the table. Motivating workloads are verification, testing, and state analysis, where "hundreds to thousands of batches of inputs" are fed through the same circuit. `[paper]`

### 2. Previous limitation
Three named baselines, each with a specific stated defect `[paper]`:
- **cuQuantum** — GPU-accelerated and has a batched API (`custatevecApplyMatrixBatched`), but "does not fuse gates," so it pays gate-by-gate.
- **Qiskit Aer** — fuses, but "gate fusion is limited to array-based gate matrix representation, which computes redundant zeros and repeated sub-matrices." The fused matrix is stored dense and grows as 4^k.
- **FlatDD** (ICPP'24, the DD state of the art) — "limited to CPU-only parallelism." The general claim: "all DD-based QCS works are limited to CPU parallelism."

So the gap is a *representation/hardware mismatch*: the compact representation (DD) lives on the CPU, and the fast hardware (GPU) only accepts dense arrays.

### 3. Core idea
Use the decision diagram **as a compiler-side compression format for fused gate matrices**, then lower it to a GPU-friendly sparse format (ELL) and run the batch as a sparse matrix–matrix product. The DD never touches the runtime data path.

### 4. Quantum-side problem
Applying a unitary to a state vector, exactly, with no truncation or approximation. Circuits are 6–21 qubits from MQT-Bench (VQE, QNN, portfolio optimization, TSP, routing, graph state, quantum supremacy). There is no new quantum algorithm, no physics, and no fidelity knob — the quantum content is entirely the workload.

### 5. Architecture/system problem
This is the substance of the paper, and it is four separable classical problems:
1. **Arithmetic waste.** Dense fused-gate application computes zeros. BQSim's cost model is literally `#MAC` (multiply-accumulate count), with a gate's cost defined as "the maximum number of non-zero elements per row (NZR) of the gate matrix." Reported #MAC reduction: **10.76× vs cuQuantum, 3.85× vs Qiskit Aer, 1.23× vs FlatDD.** `[paper]`
2. **Irregular pointer structure vs SIMT.** A DD is a pointer-chasing DAG; a GPU wants coalesced, regular access. This is the classic irregular-graph-on-GPU problem.
3. **Host↔device bandwidth.** 51,200 state vectors (200 batches × 256) must stream across PCIe. This is what caps the design.
4. **Kernel launch overhead.** Thousands of small kernel calls per batch.

### 6. Main mechanism
**What is batched:** the *state vectors*, not the gates. The BQCS kernel is "an ELL-based spMM kernel, where the gate matrix, represented in ELL, multiplies a matrix that represents a batch of state vectors" — so a batch is a dense 2ⁿ × B matrix and the fused gate is the sparse operand. `[paper]`

**How the DD is represented on GPU:** the DD is used for the *gate matrix*, not the state. Settled by the mechanism sentence: "we introduce a novel gate-fusion algorithm that reduces the amount of BQCS computation by leveraging DD to explore gate matrix sparsity and regularity." On-device it is two flat arrays: "each edge contains a weight and a pointer to the node it connects to, while each node contains its qubit level and pointers to four outgoing edges," with null pointers as sentinels for the constant-one node and constant-zero edge. `[paper]` The repo confirms this literally as `GPU_DD_edge` / `GPU_DD_node`, with `dd_nodes[node_ptr].qubit`, `dd_nodes[node_ptr].outgoing_DD_edge_ptr[child_idx]`, `dd_edges[edge_ptr].w`, `const_zero_edge`, `const_one_node`. `[code]`

**How the irregular structure is made GPU-friendly — the DD→ELL conversion.** This is the largest single contributor to the speedup. Algorithm 1 launches **one block per matrix row, with threads equal to qubit count**; each block walks the DD by **iterative-stack DFS** (recursion is explicitly avoided as GPU-hostile) and emits exactly one ELL row — values into the ELL value matrix, column indices into a parallel index matrix. ELL is chosen over CSR/COO on a measured property: NZR is near-uniform across rows, with Table 1 giving coefficient of variation **0 for VQE, QNN and TSP, and 0.0328 for quantum supremacy**. A hybrid policy picks CPU or GPU conversion by DD edge count, threshold **τ = 2000**. `[paper]` The repo has `dd_extract_matrix` and a warp-parallel `dd_extract_matrix_warp`, plus `conversion_edge_thresh = 2000` and a `DDELL_GPU` / `DDELL_CPU` / `DDELL_Mixed` enum. `[code]`

**Memory management.** Four persistent device buffers `D[0]–D[3]`: `D[0],D[1]` hold input/output for even-indexed batches, `D[2],D[3]` for odd-indexed, so kernel execution on one parity overlaps H2D/D2H transfer on the other. The whole thing is expressed as a task graph with dependencies and handed to a GPU runtime — "By delegating the scheduling of task graph to a GPU runtime, such as CUDA Graph" — to kill repetitive launch overhead. `[paper]` The repo shows exactly four buffers (`for (int buf = 0; buf < 4; buf++)`) over `h_batch` (pinned) / `d_batch` (device), built with Taskflow (`tf::Executor`, `tf::cudaFlow`, `tf::cudaTask`, `tf::cudaStream`). `[code]`

**What limits batch size.** Verbatim: "When the batch size is large, the data movement reaches memory bandwidth limit." Speedup plateaus at **B = 1024**. `[paper]`

### 7. Parallelism type
**Data-parallel** (across the batch dimension — the primary axis), plus **task-parallel/pipeline-parallel** at the host level (the 4-buffer task graph overlapping compute and transfer), plus **graph-level** parallelism inside the conversion step (block-per-row DFS over the DD). Single GPU, single node throughout.

### 8. Computational bottleneck
**Bandwidth-bound**, on the paper's own evidence. The saturation is explicitly attributed to reaching the "memory bandwidth limit"; the fix for arithmetic waste (fusion + ELL) is what removes the compute-bound regime and exposes the bandwidth one. Secondary evidence: the whole 4-buffer design exists to hide transfer, and power drops 27.17–52.76% on the GPU — a signature of the GPU no longer being arithmetic-saturated. Before the optimizations, the baseline regime is **compute-bound** (redundant zero MACs).

### 9. Evaluation setup
**One node.** 16 × Intel i7-11700 cores @ 2.50 GHz, **one NVIDIA RTX A6000 (48 GB)**, 128 GB RAM. `[paper]` Software simulation only, no quantum hardware. 16 medium/large MQT-Bench circuits: **6–21 qubits, 32–1406 gates**. Workload: **200 input batches × 256 state vectors = 51,200 state vectors.** Runs exceeding 24 hours are terminated.

`[inference]` — arithmetic that explains the 48 GB requirement: at 21 qubits a state vector is 2²¹ amplitudes; at complex128 that is 33.55 MB, so 256 per batch × 4 buffers ≈ **34.4 GB**, which fits 48 GB but not much less. **Precision is `CONTEXT_NOT_STATED` in the paper** — at complex64 the same figure is ~17.2 GB. The same arithmetic implies the **B = 1024 scaling sweep cannot have been run at 21 qubits** (4 × 1024 × 33.55 MB ≈ 137 GB); consistent with the paper, which reports that sweep for VQE n=16 and QNN n=17 only.

### 10. Baseline
- **cuQuantum**, driven through `custatevecApplyMatrixBatched` — i.e. its *native* batched path. Version `NOT_FOUND` in the paper; the artifact pins CUDA 12.6 + cuQuantum SDK. `[code]`
- **Qiskit Aer GPU 0.15.0** / Qiskit 1.2.0, 8 processes. (Versions from the artifact appendix, not the main text.)
- **FlatDD**, 16 CPU threads per process. Version `NOT_FOUND`.

### 11. Quantitative results — with context

| Number | Full context |
|---|---|
| **3.25× vs cuQuantum** (avg) | **Same GPU, same problem, end-to-end** including gate fusion and DD→ELL conversion. **This is the fair headline number.** Precision parity `CONTEXT_NOT_STATED`. |
| **159.06× vs Qiskit Aer** | Same GPU (Aer-GPU, 8 processes). `[inference]` — framework overhead almost certainly dominates here, as in Atlas's 2,126×-vs-Qiskit figure; not a partitioning/kernel result. |
| **311.42× vs FlatDD** | **NOT same hardware.** FlatDD is CPU-only, 16 threads, vs one A6000. This is a GPU-vs-CPU number and should never be quoted as a DD-algorithm speedup. |
| Per-circuit vs cuQuantum: QNN n=17 **10.17×**; Portfolio n=18 **5.13×**; VQE n=16 **2.46×**; Routing n=6 **1.65×** | Same GPU, end-to-end. Speedup rises with qubit count and gate count — consistent with fusion having more to compress. |
| Ablation: fusion **1.39–6.73×**, DD→ELL conversion **5.55–35.08×**, task graph **1.46–1.73×** | Component-wise. **The conversion, not the fusion, is the dominant term.** |
| **407.42× vs cuQuantum+B** (kernel-only) | cuQuantum fed *BQSim's own* aggressively fused gates. **This is not "BQSim is 407× faster than cuQuantum."** It measures cuQuantum's dense representation choking on large fused matrices — i.e. it shows the fusion policy is only viable when paired with a sparse kernel. |
| **3.62× vs cuQuantum+Q** (kernel-only) | cuQuantum with Qiskit-style fusion. **This is the apples-to-apples kernel number** and it is close to the 3.25× end-to-end figure — internally consistent. |
| #MAC reduction **10.76× / 3.85× / 1.23×** | vs cuQuantum / Qiskit Aer / FlatDD. An analytic operation count, not a runtime. |
| Power: GPU **27.17–52.76%** lower, CPU+GPU **15.29–41.93%** lower | vs cuQuantum, same node. |
| Scaling: VQE n=16 **2.16× at B=32 → 2.52× at B=512**, plateau at B=1024; QNN n=17 **6× at B=32 → 9.59× at B=1024** | Speedup vs cuQuantum as a function of batch size. |
| Preprocessing: **16.20% (fusion) + 41.31% (conversion)** of total runtime | For 21-qubit QNN at **only 10 batches**. Amortizes toward zero at the evaluated 200 batches. **This is the honest caveat and the paper states it.** |

### 12. Hardware evidence level
`SOFTWARE_SIMULATION` — the artifact is a classical simulator; the measurements are real wall-clock measurements on real silicon (one A6000). Nothing is modelled or projected. **This is the only paper in the set whose reported numbers are measured end-to-end on hardware that exists.**

### 13. Maturity framing
`GENERAL`. The paper is technology-agnostic — it never commits to NISQ or FTQC, because a batch simulator is useful in both regimes.

### 14. Acknowledged limitations
(a) Batch-size saturation at bandwidth. (b) Qubit-count ceiling at 21 in the results, with multi-GPU offered as the answer but **not evaluated**. (c) τ has "no universally optimal value" and is parameterized per application. (d) Preprocessing overhead is significant at small batch counts.

### 15. Artifact — `CONSISTENT`
**https://github.com/IDEA-CUHK/BQSim** (MIT). C++/CUDA + Python/shell. Dependencies: CUDA 12.6 + cuQuantum SDK, GCC 12.3.0, NVCC 12.6, CMake 3.22.1, Eigen3, OpenMP, Python 3.10.12, Qiskit Aer GPU 0.15.0, Qiskit 1.2.0. README states the hardware floor: "a CUDA-enabled GPU with at least 48 GB of memory." `[code]`

Observations from files I opened `[code]`:
- `apps/BQSim.cu` (~95 lines) is a thin driver over `include/QBatchSimulator.hpp`; it includes `dd/Export.hpp` (mqt-core DD headers), instantiates `QBatchSimulator<dd::DDPackageConfig>`, exposes `batch_size` / `num_batch` / `nDim` and a `ddell_conversion` mode selector, and emits JSON stats.
- `include/QBatchSimulator.hpp` contains the actual mechanism. **Five `__global__` kernels**: `replicate`, `initial_check`, `dd_extract_matrix`, `dd_extract_matrix_warp`, `run_fused_gate`.
- **ELL is literal**: `fused_gate_val` + `fused_gate_indices` + `num_non_zero`, with `run_fused_gate` iterating over `num_non_zero` per row — i.e. the ELL spMM described in the paper.
- **GPU DD is literal**: `GPU_DD_edge` / `GPU_DD_node` with `.qubit`, `outgoing_DD_edge_ptr[child_idx]` (four children), `.w` weights, `const_zero_edge` / `const_one_node`.
- **Batching is literal**: `h_batch` pinned host / `d_batch` device, **exactly four buffers** (`for (int buf = 0; buf < 4; buf++)`), Taskflow `tf::Executor` / `tf::cudaFlow` / `tf::cudaTask` / `tf::cudaStream`.
- **Constants match the paper**: `conversion_edge_thresh = 2000` (the paper's τ), plus `MAX_LEV`, `MAX_DECODED_MACS`, `WARP_SIZE`, `WARPS_PER_BLOCK`.
- Fusion: `CircuitOptimizer::GateFusion`, `qc::FusedGate` carrying `num_mac`, `num_nodes`, `num_edges` — the paper's #MAC cost model, instrumented.
- **Evaluated configs present**: 16 `.qasm` circuits matching Table 2 (`dnn_n17/19/21`, `vqe_n12/14/16`, `portfolio_vqe_n16/17/18`, `graph_state_n16/18/20`, `tsp_n9/16`, `routing_n6/12`, `supremacy_n12`), per-baseline scripts (`bqsim.sh`, `cuquantum.sh`, `qiskit-aer.sh`, `flatdd.sh`, `overall.sh` ≈ 4 days; `export_fused_gates.sh` + `cuquantum_plus_bq.sh` for the §4.5 fusion-transplant experiment), a Dockerfile, and a vendored `cuquantum_test/` harness with `cu_qbatch.hpp` / `naive.hpp` / `naive_dmav.hpp` baselines.
- **Note**: `apps/DDSIM.cpp` and `apps/FlatDD.cpp` are the baseline drivers, so the FlatDD comparison is reproducible in-tree.
- **No multi-GPU code observed** — consistent with multi-GPU being future work in the paper.

Every named mechanism is visibly implemented, with the paper's own constants. Verdict **`CONSISTENT`**.

### 16. HPC-scale question `[inference]`
BQSim stops being a single-accelerator problem at the point where **one batch no longer fits device memory**, and the arithmetic above puts that near n ≈ 21–22 at B = 256 with 4 buffers on 48 GB, since per-batch footprint is 4 · B · 2ⁿ · sizeof(complex). Two distinct scaling axes exist and they have different communication terms: **scaling B is embarrassingly parallel** — different state vectors never interact, so a multi-GPU version needs only a scatter of inputs and a gather of results, with no inter-GPU exchange during the sweep, and would be bounded by host bandwidth and by the cost of replicating the (small) ELL gate stream to every device. **Scaling n is not** — splitting a single 2ⁿ state vector across devices reintroduces exactly the global-qubit all-to-all that Atlas exists to minimize. The paper's own "leveraging multiple GPUs" sentence is the first axis, which is the cheap one. Open questions at facility scale: whether the ELL representation stays compact when NZR uniformity fails (the paper's own CV data covers only structured benchmarks, with supremacy already at CV = 0.0328); whether the DD→ELL conversion — currently 41.31% of runtime at 10 batches — becomes a serial bottleneck when it must be replicated or broadcast across many devices; and whether a bandwidth-bound single-GPU kernel retains any headroom once PCIe is shared across GPUs in a node.

---

## 2. A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer (ASPLOS 2024, DOI 10.1145/3620665.3640388)

Junpyo Kim, Dongmoon Min, Jungmin Cho, Hyeonseong Jeong, Ilkwon Byun, Junhyuk Choi, Juwon Hong, Jangwoo Kim — SNU HPCS Lab. **`[abstract]` ONLY** — closed access, no preprint, no artifact repository.

### 1. Research question
How to make error correction work across **multiple dilution refrigerators (DRs)**. Verbatim: "Modern large-scale quantum computers integrate multiple quantum computers located in dilution refrigerators (DR) to overcome each DR's unscaling cooling budget."

### 2. Previous limitation
Not named at the system level in the abstract. The stated defect is generic: the "baseline error handling mechanism" becomes "ineffective by increasing the number of gate operations and the inter-DR communication latency to decode and correct errors." Named prior systems `NOT_FOUND`.

### 3. Core idea
Two co-designed pieces: (i) "a low-overhead multi-DR error syndrome measurement (ESM) sequence to reduce both the number of gate operations and the error rate"; (ii) "a scalable multi-DR error decoding unit (EDU) architecture to maximize both the decoding speed and accuracy." Described as "SW-HW co-design."

### 4. Quantum-side problem
Fault-tolerant QEC at ~10⁶ physical qubits, where syndrome extraction must cross DR boundaries over "slow and erroneous inter-DR entanglement."

### 5. Architecture/system problem
Verbatim, the two costs the paper attacks are **gate-operation count** and **inter-DR communication latency**, under a hard **cooling-power budget per DR** — a per-chassis thermal envelope forcing partitioning, which is structurally the same constraint as a rack power cap. The decoder side is a **latency + accuracy** problem: an EDU whose decode must keep up across DRs. The claimed **685× EDU latency** improvement implies the baseline EDU was the binding constraint. Quantitative detail beyond the four headline ratios: `NOT_FOUND`.

### 6. Main mechanism
`NOT_FOUND` beyond the abstract's two sentences. I will not reconstruct it.

### 7. Parallelism type
**Distributed** (multi-DR), `[inference]` from the title and the multi-DR framing. Internal decoder parallelism `NOT_FOUND`.

### 8. Computational bottleneck
`[inference]`, clearly labelled: the abstract's own emphasis is **latency-bound** (ESM latency, EDU latency, inter-DR communication latency) with a **communication** term across DRs. The 6.1 × 10¹⁰× accuracy figure suggests the baseline was also **accuracy-limited** in a way that compounds with latency. Not established from paper text.

### 9. Evaluation setup
**This is the critical unknown, and I could not resolve it.** The abstract's only methodological sentence is: "With our scheme applied to **assumed** voltage-scaled CMOS and **mature** ERSFQ technologies, we successfully build a fault-tolerant million qubit-scale quantum computer." The words "assumed" and "mature" are the paper's own, and they are the strongest available evidence that the control-electronics technology is **projected, not measured**.

`[documentation]` The lab's own research page describes the project as proposing "a distributed fault-tolerant quantum computer architecture **by using our modeling tools**," and lists those tools as **CryoModel** (cryogenic performance modelling), **XQsim** (cross-technology quantum-control system simulator, ISCA'22), and **QIsim** (quantum-control interface modelling, ISCA'23), all open-sourced under `github.com/SNU-HPCS`. `[inference]` — the ASPLOS'24 evaluation is therefore very likely an **architectural simulation plus analytic cryogenic/technology model** built on that stack. **I could not confirm this from the paper and it must not be reported as paper fact.**

### 10. Baseline
"the baseline error handling mechanism" and "baseline" multi-DR system — **unnamed**. `NOT_FOUND`.

### 11. Quantitative results
All four headline numbers, verbatim and with the context that is available:

| Metric | Improvement | Context |
|---|---|---|
| ESM latency | **3.7×** | vs unnamed baseline. `CONTEXT_NOT_STATED` |
| ESM errors | **2.4×** | vs unnamed baseline. `CONTEXT_NOT_STATED` |
| EDU latency | **685×** | vs unnamed baseline. `CONTEXT_NOT_STATED` |
| EDU accuracy | **6.1 × 10¹⁰×** | vs unnamed baseline. `CONTEXT_NOT_STATED` |

Same hardware / same problem size / precision / end-to-end vs kernel-only: **all `CONTEXT_NOT_STATED`.** A 6.1 × 10¹⁰× accuracy ratio is a logical-error-rate ratio rather than a speedup, and without the paper it cannot be normalized.

### 12. Hardware evidence level
**`PROJECTED`**, with `ARCH_SIMULATION` + `ANALYTIC_MODEL` as the likely underlying method `[inference]`. The determination rests on the abstract's own "assumed voltage-scaled CMOS and mature ERSFQ technologies." **Nothing here was measured on a quantum device; the machine does not exist.** The honest statement for the census is: *the evaluation methodology could not be established from any public source.* That is itself a finding — a paper titled "million qubit-scale" whose method is not publicly inspectable.

### 13. Maturity framing
`FTQC` — explicitly fault-tolerant, million-qubit, magic-state-era scale.

### 14. Limitations acknowledged
`NOT_FOUND` (abstract only).

### 15. Artifact
**`NOT_FOUND`.** No repository in the 13-repo SNU-HPCS org (which does contain XQsim, QIsim, CryoModel, and repos for their MICRO/HPCA/ASPLOS'26 papers — so the group *does* release code, making this absence notable). Unpaywall: closed.

### 16. HPC-scale question `[inference]`
This paper begins where the others end: it is already multi-chassis by construction. The classical-systems reading is a **partitioned real-time control plane under a per-chassis power cap** — each DR is a node with a cooling budget, and the syndrome stream must be decoded within the code cycle while crossing node boundaries. The term that would dominate at scale is the **inter-DR link**: entanglement generation between DRs is orders of magnitude slower and noisier than intra-DR gates, so the ratio of cross-DR to intra-DR syndrome traffic sets the achievable partition, exactly as bisection bandwidth sets it for a domain-decomposed solver. Conditions under which this stops being tractable: when logical operations require lattice surgery spanning a DR boundary at a rate exceeding the entanglement supply; when the aggregate syndrome bandwidth off the cold stage exceeds the cabling budget (a constraint the cryogenic-control literature quantifies but this abstract does not); and when EDU decode latency plus round-trip inter-DR latency exceeds one code cycle, at which point the backlog is unbounded. Open question for the census: whether the 685× EDU latency figure is measured against a serial software decoder or an architectural baseline, since that single choice determines whether the result is a decoder-architecture contribution or a modelling artifact.

---

## 3. MECH (ASPLOS 2024, DOI 10.1145/3620665.3640377)

Hezi Zhang, Keyi Yin (UCSD), Anbang Wu (UCSB), Hassan Shapourian, Alireza Shabani (Cisco Quantum Lab), Yufei Ding (UCSD). Source: arXiv **2305.05149**. `[paper-preprint]` — the published version may differ.

### 1. Research question
Once a superconducting machine is built from **chiplets** rather than one monolithic die, how do you compile programs onto it without paying enormous SWAP-routing depth across sparse, low-fidelity cross-chip links?

### 2. Previous limitation
- **Monolithic compilers (Qiskit, optimization level 3)** — "rely on insertion of SWAP gates to route qubits"; "routing paths of qubits increase with the scale of computing"; "qubits may route back and forth if they are involved in multiple gates."
- **Distributed-QC compilers** — assume "all-to-all connectivity among different processors" and "easy access to dedicated communication qubits," assumptions that "are not applicable to the chiplet architecture."

### 3. Core idea
Reserve a fraction of physical qubits as a static **"communication highway"** — consecutive ancilla paths spanning chiplets — and buy program concurrency with them: "trading ancillary qubit resources for program concurrency."

### 4. Quantum-side problem
Chiplet-specific physics: cross-chip CNOT fidelity is worse than on-chip by a measured IBM-derived ratio **p_cross/p_on = 7.4**; measurement error ratio **p_meas/p_on = 2.2**; measurement latency modelled as **depth 2**. Cross-chip links are also sparser.

### 5. Architecture/system problem
This is a **network-on-chip / interconnect provisioning problem** in almost pure form:
- **Latency**: routing depth grows with machine diameter — "significant latency that soon becomes intolerable."
- **Bandwidth/contention**: the highway is a shared resource; gates contend for path segments, resolved by temporal and spatial sharing.
- **Resource provisioning tradeoff**: highway qubits are overhead. Measured optimum is **~25% of qubits as highway**; actual overhead in the main results is **13.6–19.4%**, and it *falls* as machines grow.
- **Search-space**: entrance assignment per data qubit × path allocation per gate component × shuttle timing.

### 6. Main mechanism
The highway is a "roughly mesh-like" lattice of ancilla paths laid so "horizontal and vertical paths ensure that they encounter the cross-chip links at the boundaries," with sparse patterns to save qubits and dense patterns "around critical positions." GHZ states along the highway are prepared in **constant time** by a measurement-based route — prepare an n-qubit cluster state in parallel, measure half, project the rest into an n/2-GHZ state — rather than by chaining, whose "latency is proportional to the number of entangled ancillary qubits." The execution model is hybrid: "computation on the ancillary qubits is performed in a measurement-based manner" while "computation on the regular qubits remains in the purely gate-based manner." Consuming pre-established GHZ states via 1-qubit measurements enables "simultaneous execution of control gates that share the same control qubit." Compilation is **two-level greedy routing**: *local routing* sends each data qubit to a nearby highway entrance by shortest path, choosing the entrance that minimizes earliest execution time, processing data qubits in ascending order of distance; *highway routing* assigns each gate component the path occupying "the least number of additional highway qubits," using shortest-path search with **zero edge weight on already-reserved segments** so paths merge, and prioritizing gates in descending order of component count. Not an ILP — explicitly greedy/constructive with no optimality guarantee.

### 7. Parallelism type
**Circuit-level / graph-level**, with the mechanism itself being a **spatial-parallelism enabler**: the highway converts sequential SWAP chains into concurrent gate execution "regardless of the distances among the involved qubits." The compiler is a classical single-machine program.

### 8. Computational bottleneck
For the *quantum machine being designed*: **latency-bound** with a **communication** term — the entire contribution is depth reduction (geomean **70.8%**) versus a much smaller gate-count reduction (geomean **18.1%**), which says the target was time, not work. For the *compiler itself*: **search-space-bound**, handled by greedy heuristics rather than solved.

### 9. Evaluation setup
Custom Python/Jupyter compiler; **no quantum hardware**; classical host is an Intel CPU with up to 32 GB RAM. Benchmarks: **QFT, QAOA (random maxcut), VQE (full-entanglement ansatz), Bernstein-Vazirani**, at **261–630 data qubits**. Machines: chiplet arrays **2×2 to 3×4**, chiplet size **6×6 to 9×9**, total **196–729 qubits**. Coupling structures: square, hexagon, heavy-square, heavy-hexagon. Error model is parametric with IBM-derived ratios (above).

### 10. Baseline
**Qiskit at optimization level 3**, applied to the same chiplet coupling maps. Version `NOT_FOUND`.

### 11. Quantitative results — with context
All results are **compiler-output metrics** (circuit depth, effective CNOT count) computed on the same benchmark and same chiplet topology as the Qiskit baseline. Nothing is executed. Main table is a **3×3 array of 6×6–9×9 chiplets**.

| Result | Context |
|---|---|
| Depth: QFT-261 **61.1%** (19,282 → 7,504); QAOA-261 **55.6%** (14,837 → 6,586); VQE-261 **56.9%** (15,725 → 6,784); BV-261 **92.6%** (418 → 31); QFT-630 **73.3%** (90,535 → 24,138) | vs Qiskit L3, same topology. **Geomean 70.8%** |
| Effective CNOT: QFT-261 **33.3%** (325,236 → 216,771); QAOA-261 **25.1%**; VQE-630 only **5.4%** (1,370,750 → 1,296,846) | **Geomean 18.1%.** The gap between 70.8% depth and 18.1% CNOT is the whole story: this buys parallelism, not work reduction |
| Highway qubit overhead **13.6–19.4%** | Falls as machine size grows |
| Scalability: QFT depth improvement ~55% at 2×2 of 7×7 → ~65% at 3×4 of 7×7 | "improvement also increases as the number of chiplets increases" |
| Sensitivity: benefit stays positive up to **measurement latency depth 20**, up to **measurement-error ratio 5**, and grows with cross-chip error ratio, positive **for ratios larger than 4** | Parametric sweeps, not measurements |
| Optimal highway fraction ≈ **25%** | Beyond that overhead dominates |

### 12. Hardware evidence level
**`ANALYTIC_MODEL` + `SOFTWARE_SIMULATION`** (compiler-output metrics under a parametric error model). Not `ARCH_SIMULATION` in the cycle-accurate sense — there is no machine model executing anything. The paper is explicit that "simulated error rates" are used and results are "not validated on real hardware."

### 13. Maturity framing
**`NISQ`**, stated by the authors: "this computing scale remains a considerable distance from reaching the real-world fault-tolerant quantum computing"; "1-10 thousand physical qubits could accommodate only several long-lived logical qubits"; "gate error rates are still above the fault-tolerant threshold."

### 14. Acknowledged limitations
Qubit overhead 13.6–19.4%; CNOT reduction collapses on large circuits (VQE-630: 5.4%) and "decreases with the chiplet size"; greedy routing with no optimality guarantee; gate aggregation limited to commutable gates; simulated error rates only; single baseline (Qiskit L3); "slight deviation is expected in the reproduction."

### 15. Artifact
**Zenodo DOI `10.5281/zenodo.10544117`** `[paper-preprint]`. Python + Jupyter notebooks. **I did not open this artifact** — no GitHub mirror surfaced and Zenodo was not reachable in the time available. Verdict: **`INSUFFICIENT_EVIDENCE`** (an artifact is claimed with a resolvable DOI, but I make no claim about its contents).

### 16. HPC-scale question `[inference]`
MECH is *already* the multi-node paper in miniature — chiplets are nodes and cross-chip links are the interconnect, with an explicit 7.4× cost asymmetry that is the quantum analogue of an intra-node/inter-node bandwidth cliff. The reserved-highway idea is recognizably **circuit-switched provisioning**: dedicate a fixed fraction of the fabric to communication rather than routing packet-by-packet, and the reported 25% optimum is a provisioning ratio of exactly the kind interconnect designers tune. Where this stops being a single-device concern: the *compiler* is a serial greedy program run on one CPU with 32 GB, and its inputs at 630 data qubits already produce 1.37M-gate circuits — the conditions under which compilation itself becomes the bottleneck are when the entrance-assignment and path-allocation searches must run over 10⁴–10⁵ qubit fabrics, where the greedy ordering (ascending distance, descending component count) is a global sequential dependence that does not obviously decompose. The other open question is whether the depth-vs-CNOT divergence persists: at 630 qubits the CNOT saving is already down to 5.4%, so the mechanism's value is entirely in concurrency, and concurrency gains are bounded by highway contention rather than by qubit count.

---

## 4. Fat-Tree QRAM (ASPLOS 2025, DOI 10.1145/3676641.3716256)

Shifan Xu, Alvin Lu, Yongshan Ding — Yale. Source: arXiv **2502.06767v1**. `[paper-preprint]`

### 1. Research question
QRAM answers address queries in superposition. The binary-tree bucket-brigade design serves **one query at a time**: "BB QRAM is not capable of processing multiple queries in parallel. This limitation is intrinsic to the binary tree structure." How do you build a QRAM that many concurrent processes can share?

### 2. Previous limitation
Named prior architectures: **Bucket-Brigade QRAM** (Giovannetti et al. 2008), **Fanout QRAM** (Nielsen & Chuang 2010), **Select-Swap QRAM** (Low et al. 2024). Also relevant lineage: the same group's *Systems Architecture for Quantum Random Access Memory* (MICRO 2023). The specific defect: "A single query occupies all O(N) quantum routers for the entire duration," and with *p* parallel processes "BB QRAM must execute them sequentially," giving **O(p log N)** latency. The root is the sole escape route — a single-port memory.

### 3. Core idea
Replicate routers where contention is highest. Routers at level *i* are duplicated **(n − i − 1)** times, indexed **(i, j, k)** — level, node position, copy — so the tree is *fat* near the root and thin near the leaves, exactly inverting where BB QRAM serializes.

### 4. Quantum-side problem
Preserving the noise resilience that makes bucket-brigade attractive. BB's infidelity is **O(ε log² N)** because entanglement stays limited; Fat-Tree claims the same **O(log² N ε)** scaling, which is the paper's central correctness claim.

### 5. Architecture/system problem
This is a **memory-bandwidth and port-contention** problem stated in classical terms and solved with a classical topology. The paper names its own analogy: the design "resembles a Fat-Tree that is commonly seen in classical computing and networking systems," citing Leiserson 1985 — while noting the routing direction differs ("qubits are routed from root to leaf in QRAM, as opposed to communicating among leaf memory cells"). The concrete terms are: **contention** (one root port), **bandwidth** (queries per unit time), **pipelining depth**, and **wire/planarity constraints** — inter-node wires decrease from **n at root to 1 at leaves**, and the on-chip layout requires a **thickness-2 chip, "two edge-disjoint layers"** with **Through-Silicon-Vias**, because the graph is bi-planar but not planar.

### 6. Main mechanism
Router duplication turns the tree into "a composition of multiple sub-component QRAMs of varying sizes," so *k*-th query occupies a different copy at each level and queries flow simultaneously. The paper distinguishes its scheme from the prior one explicitly: "Fat-Tree QRAM introduces **query-level pipelining**, unlike **bit-level pipelining** of BB QRAMs." Execution alternates **gate steps** (CSWAP operations, 4 circuit layers each) with **swap steps** (1 layer), where swap steps handle both the transition between sub-component QRAMs of increasing size during address loading and the data-retrieval path. Per query this is approximately **8 log N + swap overhead** circuit layers. Total routers **2N − 2 − n** versus **N** for BB — roughly 2× — while total qubits stay **O(N)**. Connectivity required is "bi-planar nearest-neighbor" rather than all-to-all. The headline capability: **"pipelines O(log N) independent queries to a size-N memory in O(log N) time,"** replacing sequential O(p log N).

### 7. Parallelism type
**Pipeline-parallel** at the query level, over a **graph-level** (tree) topology. Not data-parallel, not distributed — this is one memory device.

### 8. Computational bottleneck
The baseline is **bandwidth-bound / contention-bound**, and that is precisely what is attacked: the entire contribution is throughput (queries per unit time) at fixed asymptotic qubit cost. Latency per individual query is unchanged at O(log N); only throughput improves. The residual bottleneck the paper flags is **classical**: "Additional time for classical memory swap might be required for executing multiple distinct queries."

### 9. Evaluation setup
**Analytic.** Resource-estimation formulas and circuit-depth analysis. **No quantum simulator was used for the main results** — no Stim, no Qiskit, no Cirq surfaced in the text I could read. Figures illustrate small instances: **N = 8** (Fig. 2), **N = 32** (Figs. 3, 4). Hardware target is superconducting: cavities encoding qubits, transmons coupled to cavities for **native CSWAP**, tunable couplers and beam splitters, coaxial wires for inter-node links, TSVs for the two-layer on-chip variant. Gate times: `NOT_FOUND`. Noise model: a single per-operation error rate ε feeding the asymptotic infidelity bound.

### 10. Baseline
**Bucket-Brigade QRAM** (Giovannetti et al. 2008), executed sequentially for *p* queries. Secondary: Fanout QRAM, Select-Swap QRAM.

### 11. Quantitative results — with context
Everything is **asymptotic**, not measured. Same problem size, same error model, same qubit-count order — but no wall clock, no fidelity simulation, no hardware.

| Metric | Fat-Tree | BB QRAM |
|---|---|---|
| Queries served | **O(log N)** independent queries in **O(log N)** time | *p* queries in **O(p log N)** time |
| Qubits | **O(N)** | **O(N)** |
| Routers | **2N − 2 − n** (~2× overhead) | **N** |
| Infidelity | **O(log² N · ε)** | **O(ε log² N)** |
| Bandwidth | ~**log N ×** higher than sequential BB | baseline |

Absolute bandwidth values, hardware-utilization percentages, space-time-volume-per-query numbers, and the numeric outcomes of the noise-resilience / virtual-distillation / error-correction sections (8.1–8.3): **`NOT_FOUND`** in the version I could read. The paper introduces "space-time volume per query, hardware utilization, and memory access rate" as metrics but I could not extract numeric values for them.

### 12. Hardware evidence level
**`ANALYTIC_MODEL`.** This is the purest analytic paper in the set: complexity classes, router counts, and layer counts, with a hardware-implementation proposal sketched but not simulated. Nothing was measured, and no architectural simulator was run.

### 13. Maturity framing
`EARLY_FTQC` / `FTQC` — the paper discusses noise resilience, virtual distillation, and error-corrected queries as separate regimes, and its interest in ε-scaling only makes sense in a fault-tolerant setting.

### 14. Acknowledged limitations
"More compact on-chip designs have stricter topology constraints to avoid crossing inter-connecting wires"; the thickness-2 chip requirement is "more complex than single-layer"; "additional time for classical memory swap might be required"; and the design "can be generalized to any technology platform that supports native CSWAP operations" — i.e. it is gate-set dependent.

### 15. Artifact
**`NOT_FOUND`.** No repository or Zenodo DOI appears in the preprint, and targeted searching surfaced none. Verdict: **`INSUFFICIENT_EVIDENCE`** — consistent with an analytic paper.

### 16. HPC-scale question `[inference]`
This is a shared-memory-contention paper, and the classical reading is direct: BB QRAM is a **single-ported memory**, Fat-Tree QRAM is a **multi-banked/multi-ported** one, and the 2× router cost is the area price of the extra ports — the same trade a cache designer makes. The conditions under which the design's own terms would dominate: the fat-tree's advantage is **log N** concurrent queries, so it saturates when the number of requesting processes p exceeds log N, at which point queueing returns and the memory is again the serialization point — the interesting regime is p ≫ log N, which the paper does not treat. Physically, the term that grows fastest is **wiring**: inter-node wire count is n at the root, so the root's fan-out scales with address width while the chip is constrained to two edge-disjoint layers, making the root a literal bisection-bandwidth constraint. And because the paper is asymptotic, the open question with the most leverage is whether the constant factors — the 4-layer gate step, the 1-layer swap step, and the classical memory-swap time it flags but does not quantify — leave any throughput advantage once a concrete cycle time is fixed.

---

## 5. ACQC — Accelerating Computation in Quantum LDPC Code (ASPLOS 2026, DOI 10.1145/3779212.3790122)

Jungmin Cho, Hyeonseong Jeong, Junpyo Kim, Junhyuk Choi, Juwon Hong, Jangwoo Kim — SNU HPCS Lab. **`[abstract]` ONLY.** Gold OA per Unpaywall, but the only OA location is ACM DL, which is blocked here (`url_for_pdf: null`). No arXiv preprint exists.

### 1. Research question
qLDPC codes save an order of magnitude in qubits versus surface codes, but "as qLDPC codes support only a limited set of operations, they require programs to be decomposed into many qLDPC-supported operations. This **prohibitively increases the execution time of FTQC applications to tens of days**." The question is how to recover the time.

### 2. Previous limitation
"the baseline qLDPC code FTQC" and "the surface code FTQC" — **unnamed**. Named prior systems: `NOT_FOUND`.

### 3. Core idea
A three-part software–hardware co-design: (i) "a novel decomposition–layout co-design that significantly reduces execution time **at the cost of qubit overhead**"; (ii) recovering that overhead "by exploiting characteristics of qLDPC codes and our decomposition technique"; (iii) "reduce the qubit overhead of magic state distillation by designing an optimal qLDPC code layout."

### 4. Quantum-side problem
qLDPC codes have a restricted native gate set; arbitrary logical circuits must be decomposed into supported operations, and magic-state distillation supplies the non-Clifford resources.

### 5. Architecture/system problem
Stated as a clean **time–space tradeoff**: decomposition choice determines execution time, layout determines qubit count, and the two are coupled — which is why they are co-optimized rather than solved in sequence. The "tens of days" figure makes this a **latency/throughput** problem at application scale, and the 18.3× qubit-reduction claim makes the competing axis **capacity**. Whether this is formulated as a search problem, and if so what the search space is: `NOT_FOUND`.

### 6. Main mechanism
`NOT_FOUND` beyond the abstract's three sentences. I will not reconstruct it.

### 7. Parallelism type
`NOT_FOUND`. `[inference]` — decomposition-into-many-operations plus layout is structurally a scheduling-and-placement problem, which would make it **circuit-level / graph-level**; this is not established.

### 8. Computational bottleneck
`[inference]` from the abstract's own framing: **latency-bound** at the application level (tens of days of execution), traded against **capacity** (qubit overhead). The compile-time search cost is `NOT_FOUND`.

### 9. Evaluation setup
The one methodological sentence, verbatim and unambiguous: **"As there is currently no available hardware for qLDPC codes, we evaluate ACQC with a comprehensive simulation."** Simulator name, code family (bivariate bicycle? lifted product?), physical error rate, cycle time, benchmark applications and their sizes: **all `NOT_FOUND`.**

### 10. Baseline
Two, both unnamed: "the baseline qLDPC code FTQC" and "the surface code FTQC."

### 11. Quantitative results
| Metric | Value | Context |
|---|---|---|
| Speedup | **4.4×** | "over the baseline qLDPC code FTQC," **on average**. Baseline unnamed. `CONTEXT_NOT_STATED` |
| Qubit reduction | **18.3×** | "over the surface code FTQC," **on average**. Note this is a *different baseline* from the speedup — the two headline numbers are measured against two different systems and cannot be combined |

Same problem size / precision / end-to-end vs component: **all `CONTEXT_NOT_STATED`.**

### 12. Hardware evidence level
**`SOFTWARE_SIMULATION` or `ARCH_SIMULATION`** — the abstract commits to "comprehensive simulation" and explicitly rules out hardware ("there is currently no available hardware for qLDPC codes"), but does not say which kind. Given the group's tooling I would lean `ARCH_SIMULATION` `[inference]`, but **the distinction cannot be resolved from public sources.**

### 13. Maturity framing
**`FTQC`** — stated in the first sentence.

### 14. Acknowledged limitations
`NOT_FOUND` (abstract only).

### 15. Artifact
**`NOT_FOUND`.** No repository in the SNU-HPCS org. Verdict `INSUFFICIENT_EVIDENCE`.

### 16. HPC-scale question `[inference]`
The recognizable classical problem is **instruction selection plus placement under a capacity constraint** — decompose a program into a restricted ISA, lay the result out in a fixed resource, and co-optimize the two because the decomposition determines the layout pressure. The condition under which this leaves a single device is set by the paper's own tradeoff: the decomposition "significantly reduces execution time **at the cost of qubit overhead**," so as applications grow, the qubit overhead is the term that forces partitioning across modules, and at that point the layout problem acquires a cut-cost term the abstract gives no evidence of modelling. The other open question, carried over from your QEC census: qLDPC implies belief-propagation-class decoding rather than matching, which is iterative with data-dependent convergence — an unbounded-iteration workload under a hard real-time deadline — and there is no public evidence either way about whether ACQC models that cost.

---

## 6. COMPAS (ASPLOS 2026, DOI 10.1145/3779212.3790143)

Brayden Goldstein-Gelb (Brown), Kun Liu (Yale), John M. Martyn (PNNL; Harvard), Hengyun Zhou (QuEra), Yongshan Ding (Yale), Yuan Liu (NC State). Source: arXiv **2511.23434v2**. `[paper-preprint]`

### 1. Research question
Estimate the **multivariate trace** tr(ρ₁ρ₂…ρ_k) — the k-party generalization of the SWAP test's overlap estimate — when the k states live on **k different QPUs** and no single chip can hold them all. Framing: "the limited number of qubits per chip remains a critical bottleneck."

### 2. Previous limitation
- **Quek et al. (2024)** achieved constant circuit depth but forced a choice: either **increase circuit depth to O(k)** while keeping the GHZ control register at ⌈k/2⌉ qubits, or **keep depth constant but inflate the GHZ width to ⌈k/2⌉·n** — a factor-n blowup in the entangled control register.
- **Naive distribution**: placing the k states on k QPUs in a line and teleporting qubits costs **(n/k + n − 1)·(n − n/k)/2 = O(n²) Bell pairs**.

### 3. Core idea
Exploit the fact that in the multi-party SWAP test "each of the k states interacts with **at most two others**." Order the states in an interleaved **1, k, 2, k−1, …** pattern so all interactions are between adjacent neighbours in a line topology, then implement each pairwise controlled-SWAP either by gate teleportation (**telegate**) or by data teleportation (**teledata**), and flatten the shared-control Toffolis into constant-depth **Fanout** gates.

### 4. Quantum-side problem
Multivariate trace estimation is the primitive behind entanglement-spectrum measurement, virtual distillation, and related quantities. The circuit is: prepare a ⌈k/2⌉-qubit GHZ control state; two rounds of CSWAPs on the ρᵢ; measure the GHZ register in the X basis.

### 5. Architecture/system problem
This is a **distributed-systems paper about communication volume, depth, and synchronization**, and it is unusually explicit about all three:
- **Communication cost** is the object of optimization: **telegate 2 + 6n** Bell pairs, **teledata 2 + 4n** Bell pairs, versus the naive **O(n²)**. Asymptotically **O(nk)** across the whole system — linear in width, linear in parties, rather than quadratic.
- **Latency**: total depth **91 (teledata) / 99 (telegate)** circuit layers, and critically **constant, independent of k**. Stated goal: "runtime is not slowed down by communication between nodes, thereby enabling true parallelism at scale."
- **Synchronization**: the modular decomposition "improves synchronization and parallelism, because preparation can happen in parallel across different modules."
- **Topology**: line.
- **The scaling wall is a noise-budget inequality**, which is the most useful number in the paper: to hold total infidelity below ε you need **k ≤ O(ε / (n·p))**, where p is Bell-pair error.

### 6. Main mechanism
Distributed GHZ preparation replaces inter-QPU CNOTs with their telegate counterparts. Each two-party CSWAP is decomposed as CNOT + Toffoli + CNOT; in the **telegate** design the remote CNOTs become teleported gates consuming 2n Bell pairs per round, while in the **teledata** design (the recommended one) Bob teleports ρⱼ to Alice, Alice does the CSWAP locally, and the result is teleported back, also 2n Bell pairs per round. The depth win comes from eliminating sequential Toffoli execution: two shared-control Toffolis are commuted and merged into a **Fanout gate of constant depth 7** including measurements, using one |0⟩ ancilla per target. Ancilla cost is n (telegate, reused across rounds) or 2n (teledata). Total system fidelity is composed multiplicatively — **F_tot ≥ (1 − 3p/4)^O(nk)**, which by Bernoulli gives **≥ 1 − 3pnk/4**, and inverting that inequality is where k ≤ O(ε/(np)) comes from.

### 7. Parallelism type
**Distributed** (k QPUs), with **circuit-level** concurrency inside each party and constant-depth **pipeline** structure across the line.

### 8. Computational bottleneck
**Bandwidth-bound in the entanglement supply, and noise-limited rather than time-limited.** The paper's own data settle this: depth is constant in k (so not latency-bound), Bell-pair consumption is linear in nk (the growing term), and the binding constraint is stated as an inequality on k in terms of the Bell-pair error rate. Concretely: "with n=100 qubits per QPU, the LP code allows for up to **k=5 QPUs** before the infidelity due to Bell pair noise surpasses ε=10⁻³." Five nodes. That is the scale limit, and it is set by link quality, not by compute.

### 9. Evaluation setup
**Qiskit shot-based simulator** and **Stim**. **No real hardware.** Fanout error characterization at **4, 6, 8 target qubits**, **100,000 shots per simulation**. CSWAP evaluated by exhaustive simulation over all computational-basis inputs when 2^(2n+1) ≤ 300, and by **300 randomly sampled basis states** above that. Full-circuit density-matrix simulation is stated to be impractical, so system fidelity is composed from component error rates. Noise model: depolarizing **p/10** on 1q gates, **p** on 2q gates, measurement error **p**, for **p ∈ {0.001, 0.003, 0.005}**.

### 10. Baseline
**Quek et al. (2024)** (the non-distributed constant-depth multivariate trace estimation protocol) and the **naive teleportation-based distribution** costing O(n²) Bell pairs. Within the paper, telegate and teledata are compared against each other.

### 11. Quantitative results — with context
All numbers are **simulated**, from a component-composition model, on the noise parameters above.

| Result | Context |
|---|---|
| Bell pairs: **2 + 4n** (teledata) vs **2 + 6n** (telegate) vs **O(n²)** naive | Analytic counts, per full protocol |
| Depth: **91** (teledata) / **99** (telegate), **constant in k** | Circuit layers, analytic |
| Ancilla: **2n** (teledata) / **n** (telegate); memory estimate **14n + 6** incl. 3× distillation factor | Analytic |
| Telegate fidelity averages **0.84% lower** than teledata | Simulated CSWAP fidelity, averaged over the swept n and p₂q |
| 4-target Fanout, p=0.001: dominant error **ZIIII 0.35%**; at p=0.005: **ZIIII 1.64%** | Stim/Qiskit, 100k shots |
| GHZ fidelity "decreases linearly in n" | Simulated |
| F_CNOT ≥ **1 − 3p/4**; F_Toffoli ≥ **1 − 3p/4**; F_teledata ≥ **1 − p/2** | Analytic bounds under Bell-pair depolarization |
| **k ≤ O(ε/(np))**; concretely **k = 5** at n=100, ε=10⁻³ with distillation | The operative scaling limit |

### 12. Hardware evidence level
**`SOFTWARE_SIMULATION` + `ANALYTIC_MODEL`.** Stim/Qiskit for components; analytic composition for the system, because the full circuit is too large to simulate. No hardware.

### 13. Maturity framing
**`NISQ`** — the evaluation module is literally named `dqalgo.nisq.*` in the artifact, the error rates are near-term, and the paper cites current remote-entanglement rates as the limiter. It gestures at error correction as future work.

### 14. Acknowledged limitations
Full-circuit fidelity is "computationally prohibitive," so system fidelity is composed rather than simulated; "distributing over more QPUs comes at the cost of a lower fidelity, unless Bell pair noise is significantly reduced"; current remote entanglement between neutral-atom or trapped-ion qubits "only achieves rates of a few hundred Hz with entangling fidelities in the high 90%"; distillation overhead is not fully costed; the authors call for "a more in-depth analysis including error correction and Bell pair distillation overhead" and for "detailed study of quantum network topology and connectivity, location of the Bell pair generation nodes."

### 15. Artifact — `CONSISTENT`
**https://github.com/kunliu7/Distributed-Q-Algo** (MIT). `[code]` Python 3.12; dependencies include **Stim**, pytest, Jupyter, plus a Mathematica component for analytic verification. Directories `/src`, `/scripts`, `/tests`, `/notebooks/vis`, `/data`, `/mathematica`, plus **`slurm_script_EXAMPLE.sh`** — a cluster job template. The named mechanisms are present as named modules and scripts: `dqalgo.nisq.fanouts.BaumerFanoutBuilder` (the constant-depth Fanout), and evaluation drivers `eval_nisq_ghz_prep.py`, `eval_nisq_cswap.py`, `eval_nisq_teleport.py`, `eval_nisq_telegate.py`, `eval_nisq_teleported_cnots.py`, with **telegate vs teledata selectable via a `--method` flag** on the CSWAP evaluation — matching the paper's two designs. Figure-generation is mapped one-to-one: `generate_ghz_graph.py` → Fig. 9(a), `generate_cswap_graph.py` → 9(b), `generate_overall_error_graphs.py` → 9(c), `asymptotics_graphs.py` → Fig. 10. Runtime documented as ~5 hours on an M1 MacBook Pro, largest task (`n_trgts=5`, telegate) "about 4 hours," <40 MB disk. I did not open the `.py` sources themselves, so the verdict rests on the README's module/script naming and the figure mapping.

### 16. HPC-scale question `[inference]`
COMPAS is the one paper here whose contribution is already stated in distributed-systems vocabulary, and its own answer to "at what scale does this break" is unusually crisp: **k ≤ O(ε/(np))**, which at realistic parameters is **five nodes**. That is the number worth carrying into the census, because it says the limiting resource is not qubits or depth but **link fidelity** — the quantum analogue of a network whose error rate, not its bandwidth or latency, caps the machine size. The communication term that dominates is Bell-pair consumption at O(nk), and since distillation multiplies that by roughly 3× (visible in the 14n + 6 memory estimate), the effective link demand is ~12n per pair of adjacent parties. Conditions worth watching: whether the line topology survives — the interleaving trick is what makes interactions nearest-neighbour, and a topology with different diameter would change the Bell-pair count; whether entanglement generation at "a few hundred Hz" can ever sit under a constant-depth protocol whose gates run at MHz, which is a **rate mismatch of four to five orders of magnitude** between the interconnect and the compute; and how the k ≤ O(ε/(np)) bound moves once error correction is layered on, since that is exactly the analysis the authors defer.

---

## 7. QRCC (29th ASPLOS Volume 4 — proceedings 2024, presented ASPLOS 2025; DOI 10.1145/3622781.3674179)

Aditya Pawar, Yingheng Li, Zewei Mo, Yanan Guo, Xulong Tang, Youtao Zhang, Jun Yang — U Pittsburgh. Sources: arXiv **2312.10298v3** and the **published camera-ready PDF**, cross-checked. `[paper-preprint]` `[paper]`

### 1. Research question
Run an N-qubit circuit on a D-qubit device (N > D) while minimizing the **classical post-processing** bill and keeping fidelity. "the size of quantum circuits that can be run with high fidelity is constrained by the limited quantity and quality of physical qubits."

### 2. Previous limitation
- **CutQC** — wire cutting formulated as **MIP with non-linear quadratic constraints**; introduces "one extra qubit (initialization qubit) after each cut, which may artificially increase the total number of physical qubits required"; and "cannot find a solution if the device size D is small." In the evaluation it **times out at 1800 s** on several QFT cases and returns "No Solution" on multiple N=50 instances.
- **CaQR** — qubit reuse via mid-circuit measure-and-reset; "the effectiveness of qubit reuse diminishes as the circuits grow larger — only a few qubits can delay their operations enough to start after some other qubits have finished."
- **Gate cutting** — "has not been fully explored" and "not been well-studied at the circuit level."
- **Sequential composition of CutQC then CaQR** — measurably worse than joint optimization: QFT(N=15, D=7) gives **44 cuts sequentially vs 20 cuts jointly**.

### 3. Core idea
Put wire cutting, gate cutting, and qubit reuse in **one ILP** over a layered DAG, so that reuse opportunities created by a cut are visible to the cut-placement decision rather than discovered afterwards: "wire cuts in the circuit enlarge qubit-reuse opportunities, which in turn help to eliminate unnecessary cuts."

### 4. Quantum-side problem
Quasi-probability decomposition: a cut wire is reconstructed from 4 measurement bases × 4 initialization states; a cut two-qubit gate decomposes into **6** subcircuit instances. Fidelity is governed by the number of two-qubit gates in the largest subcircuit.

### 5. Architecture/system problem
Two distinct classical costs, and the paper treats both:
- **Search-space explosion at compile time.** ILP decision variables per gate per subcircuit per layer, giving **O(N × depth)** constraint variables; the authors had to insert identity gates *selectively* because naive layering "slows down the solver."
- **Exponential classical post-processing at run time — this is the real one.** Reconstruction costs **O(4^k · 6^m)** for k wire cuts and m gate cuts. The memory distinction is sharp: recovering a **probability vector costs O(2^(N+2k))**, whereas an **expectation value costs O(2^(2k))**. At N=50 the probability vector alone is petabyte-scale. Their own worst case: ERD(N=300, D=200, p=0.02) needs **O(4^52 · 6^104)** — explicitly labelled intractable.
- The ILP's objective **linearizes the exponential**: rather than optimize 4^k·6^m directly, it minimizes **α·#WireCuts + β·#GateCuts** with **α = 3.25, β = 4.2**, coefficients chosen to "preserve relative ordering for k < 240 cuts."

### 6. Main mechanism
The circuit becomes a **QR-aware layered DAG** with all qubits aligned across layers, padded with dummy identity gates so "each qubit goes through the same number of quantum operations," and with 1q and 2q gates distinguished so reuse is detectable. The ILP's binary variables are V_{x,c} (2q gate x in subcircuit c), S_{x,c} (1q gate), WS/WT/WB_x (wire-cut locations), G_x (gate-cut indicator), and GT/GB_{x,c} (gate-cut halves). The device constraint is per-layer: Q_{c,l} = Σ(gates in subcircuit c at layer l) ≤ D. Disjunctive constraints forbid W-cutting and G-cutting the same gate; connectivity between neighbouring gates is enforced through absolute-value linearization. The objective is **Min[δ·PPCost + (1−δ)·CError]**, where CError tracks the maximum 2q-gate count in any subcircuit as a fidelity proxy via a per-circuit auto-tuned linear function. **δ is the exposed knob**: δ=1.0 (QRCC-C) minimizes post-processing only; δ=0.75 (QRCC-B) trades ~nothing in cuts for a large fidelity gain. For reconstruction the paper adds an **approximate recursive divide-and-conquer (ARP)** that partitions into 4 subcircuits, capping the vector space at 2³⁰ regardless of N and making the overhead depend on the *maximum cuts between adjacent subcircuit pairs* rather than the total.

### 7. Parallelism type
**Circuit-level partitioning** (the subcircuits are independent jobs) with **data-parallel / embarrassingly-parallel** subcircuit execution, and a **task-parallel tree reduction** in the ARP reconstruction. The ILP solve itself is a single Gurobi instance.

### 8. Computational bottleneck
**Search-space-bound at compile time, and memory-bound at reconstruction time** — and the paper's own words say the crossover happens: at N=300, D=200, the solution "contains large numbers of wire cuts and gate cuts, indicating that **the bottleneck has shifted to the post-processing overhead**." Compile-time evidence: CutQC's MIP hits the 1800 s ceiling where QRCC's ILP finishes in ≤20 s. Reconstruction evidence: O(2^(N+2k)) memory for probability vectors, petabytes at N=50.

### 9. Evaluation setup
**Solver**: Gurobi (2023). **Host CPU model, core count, RAM, OS: `NOT_FOUND` in both the preprint and the published camera-ready** — I checked the camera-ready specifically for this and it is absent. Timeout 1800 s.
**Real quantum hardware**: **IBM Lagos, 7 qubits**, via IBM Cloud — median CNOT error **8.25 × 10⁻³**, single-qubit/√x error **2.6 × 10⁻⁴**, 1.7 connections per qubit.
**Simulation**: Qiskit state-vector; shot-based at **16,384 shots per run, 10 runs averaged**.
**Benchmarks** — probability-distribution group (wire cuts only): QFT (N≤30), AQFT (N≤40), SPM/Google supremacy (N≤42), ADD ripple-carry adder (N≤40). Expectation-value group (wire + gate cuts): REG m-regular graphs, ERD Erdős–Rényi, BAR Barabási–Albert (all N≤50), Hamiltonian simulation on 2D Ising/XY/Heisenberg lattices (N≤49), VQE hydrogen chain (N≤50). Scalability study reaches **N=300, D=200**. Device sizes **D ∈ {7, 16, 20, 24, 27}**.

### 10. Baseline
**CutQC** (wire cutting, MIP) — the primary named baseline. **CaQR** (qubit reuse) and the **sequential CutQC-then-CaQR** composition. Direct 7-qubit device execution as the fidelity reference. Versions `NOT_FOUND`.

### 11. Quantitative results — with context
Cut-count and solver-time results are **same problem, same device size, same solver, same timeout** — well controlled. Fidelity results are on **real hardware**, but at tiny scale.

| Result | Context |
|---|---|
| **29%** (QRCC-C) / **24%** (QRCC-B) fewer cuts than CutQC, average | Wire-cutting benchmarks, same N and D. Best case QFT(N=30, D=27): **81%** (32 → 6 cuts). Worst: AQFT, negligible |
| **41%** (W-cut only) / **44%** (W+G-cut) fewer effective cuts | Expectation-value benchmarks vs CutQC. ERD-50 saves **8.45×** post-processing (24 → 22.46 effective cuts) — note effective cuts are a log-scale quantity, so 1.5 "cuts" is 8.45× work |
| Example QFT(N=30, D=24): CutQC 4 subcircuits/52 cuts/max-2q 276 → QRCC-C 2 subcircuits/12 cuts/max-2q 414 → QRCC-B 4 subcircuits/30 cuts/max-2q 146 | Shows the δ knob explicitly trading cuts against fidelity: **48%** max-2q reduction |
| Solver time **58% faster** than CutQC on average; QFT cases **1800 s → ≤20 s** | Same Gurobi, same timeout. Attributed to linear vs quadratic constraints. SPM(20,7) 11.7 s → 6.21 s; ADD(22,7) 148.5 s → 19.70 s |
| **Real hardware, REG(m=2), N=7, D=4**: state-vector truth −0.0349; direct 7-qubit device −0.0078 (**22.3%** accuracy); QRCC 4-qubit + post-processing −0.0355 (**98.3%**); shot-based sim −0.0323 (92%) | **The only real-hardware result in this entire 8-paper set.** IBM Lagos. Cause given: 3 CNOTs per subcircuit vs 16 in the original. **N=7 is a very small demonstration** and should not be read as validating the N=300 analysis |
| δ sweep: δ=0.2 gives **+30% cuts** but **52%** better max-2q; δ=0.75 chosen as "negligible impact on #cuts but large improvement on #MS" | Same benchmarks |
| Scalability: REG(m=3, N=200, D=150) QRCC 19 W-cuts vs CutQC 21; REG(m=4, N=300, D=200) QRCC 61 W + 6 G vs CutQC 75 W | Solver output only, not executed |

### 12. Hardware evidence level
**`REAL_HARDWARE`** (IBM Lagos, 7 qubits) for the single fidelity data point, **`SOFTWARE_SIMULATION`** for the shot-based results, and **`ANALYTIC_MODEL`** for everything above N=27 — the N=50 to N=300 studies are solver outputs and complexity formulas, with no execution. The honest composite tag is `REAL_HARDWARE` at N=7 only; the paper's scale claims are analytic.

### 13. Maturity framing
**`NISQ`** — the entire premise is small, noisy devices, mid-circuit measurement availability, and fidelity that degrades with 2q-gate count.

### 14. Acknowledged limitations
Post-processing "increases exponentially with the number of cuts" — unavoidable; gate cutting works only for expectation values, not full distributions; qubit reuse "diminishes on large sparse circuits"; the ERD(N=300) case is **O(4^52 · 6^104)**, infeasible even with QRCC; ILP constraint-generation memory forced selective identity-gate insertion; mid-circuit measure-and-reset is not universally supported.

### 15. Artifact
**`NOT_FOUND`.** No GitHub, Zenodo, or supplementary URL appears in the preprint **or** the published camera-ready — I checked both specifically. Verdict `INSUFFICIENT_EVIDENCE`. This is the one paper in the set that is both heavily quantitative and entirely unreproducible.

### 16. HPC-scale question `[inference]`
QRCC is the paper here whose bottleneck is *already* classical HPC, and it is one of the few in this corpus where the quantum device is the cheap part. Two distinct scaling regimes: **subcircuit execution is embarrassingly parallel** — 4^k·6^m independent jobs with no communication, a textbook high-throughput workload that would map onto a batch queue without modification, and notably the *same* workload shape that BQSim's batch simulator is built to absorb. **Reconstruction is not** — it is a tree of Kronecker products whose intermediate tensors are the memory term, and O(2^(N+2k)) is the quantity that decides whether it fits in a node, a node's DRAM plus NVMe, or nothing at all. The ARP scheme's cap at 2³⁰ elements is exactly a blocking/tiling decision, and the recursion into 4 subcircuits is a divide-and-conquer whose communication term is the boundary cuts between adjacent partitions — structurally the same quantity that governs domain decomposition. Conditions worth stating: the point at which this leaves one node is when 2^(N+2k) complex amplitudes exceed node memory, which at complex128 is around N+2k ≈ 36 for a 1 TB node; above that the open question is whether the reconstruction tree's boundary-cut traffic is small enough to distribute, since ARP's own guarantee is phrased in terms of the *maximum* cuts between adjacent subcircuit pairs — the same max-vs-total distinction that separates good from bad partitionings in a parallel solver. The compile-time side has its own limit: a single Gurobi instance on an unstated machine, with the paper already reporting 1800 s ceilings for the baseline.

---

## 8. TreeVQA (ASPLOS 2026, DOI 10.1145/3779212.3790239)

Yuewen Hou, Dhanvi Bharadwaj, Gokul Subramanian Ravi — U Michigan. Source: arXiv **2512.12068**. `[paper-preprint]`

### 1. Research question
VQA shot cost. Three multiplicative factors: thousands of iterations, thousands of Pauli terms per Hamiltonian, and thousands of *tasks* in a real application. The concrete number: estimating the NH₃ ground state (12 qubits) "can require up to **5.5 × 10⁸ execution shots**... approximately **564 hours** of runtime on typical cloud-based quantum devices, incurring monetary expenses on the order of **$5868k**." The governing formula is N_overall = T × N_evals-per-iter × N_per-eval, with N_per-eval ≈ (Σ|c_j|)²/ε² giving 10⁶–10⁸ shots per evaluation.

### 2. Previous limitation
- **Classical initialization** (incl. **CAFQA**) — "success is often limited and problem dependent." CAFQA reaches 95.5% initialization accuracy on LiH and TreeVQA still helps on top of it.
- **Error mitigation (ZNE, PEC, measurement mitigation)** — makes it worse: can "amplify the shot count of a 100-qubit VQA task by approximately 1000×."
- **ADAPT-VQE** — truncates terms but adds circuit depth.
- **Measurement reduction / commuting-group tiling** — "complex grouping heuristics or increased circuit depth."
- **Meta-VQE** — "the only prior work explicitly targeting multi-task VQE," but "it lacks the dynamic monitoring and adaptive splitting mechanisms."

The gap is specific: every prior method optimizes *one* VQA task. Nobody amortizes across the *set* of related tasks a real workflow submits.

### 3. Core idea
Treat a batch of related VQA tasks as one job that **progressively splits**. Start with all tasks in one cluster optimizing a single averaged "mixed Hamiltonian"; split a cluster only when its members' optimization trajectories demonstrably diverge; children inherit parent parameters as a warm start. Justified by the adiabatic theorem: if H₁ is deformed slowly into a nearby H₂, ψ₁ evolves smoothly into ψ₂ — so nearby Hamiltonians can share optimization work.

### 4. Quantum-side problem
Ground-state estimation for molecules (H₂, LiH, BeH₂, HF, C₂H₂), spin chains (XXZ, transverse Ising), and MaxCut, under SPSA/COBYLA with UCCSD and hardware-efficient ansätze.

### 5. Architecture/system problem
This is **work amortization across a job set under a global resource budget** — the QPU-shot equivalent of batching queries to share computation:
- The resource is a **global shot budget S_max** managed by a Central Controller.
- The mechanism is **sharing an expensive evaluation across many consumers** until sharing stops paying.
- The split decision is a **runtime monitoring problem**: sliding-window linear regression on the loss curve, triggering when `|slope_t| < ε_split` (mixed optimization stalled) or `∃i : slope_i,t > 0` (some member is now getting worse). The paper is careful that this is cheap — it "incurs only a linear classical computational cost, not a quantum execution cost."
- Partitioning is **spectral clustering** on an RBF kernel of ℓ₁ distances between padded Pauli-coefficient vectors: d(Hᵢ,Hⱼ) = Σ_k |c_ik − c_jk|, S_ij = exp(−d²/2σ²) with σ the median pairwise distance.
- **Honest reading of the parallelism**: the paper allocates shots to clusters **sequentially** and does not exploit inter-branch parallelism. The tree is a *work-sharing* structure, not a parallel-execution structure.

### 6. Main mechanism
The mixed Hamiltonian is a coefficient-space average over the cluster, H_mixed = (1/N)Σᵢ Hᵢ^padded = Σ_k [(1/N)Σᵢ c_ik] P_k, with missing Pauli terms zero-padded so all members share one term basis — this is what lets one circuit evaluation serve every task in the cluster. Optimization proceeds on that representative landscape with SPSA. After a warmup, loss slopes are tracked per-cluster and per-member over a sliding window of W values; when the cluster's own slope flattens or any member's slope turns positive, the cluster splits by spectral clustering on the similarity matrix, and both children inherit θ_C from the parent (θ_C1 = θ_C2 = θ_C). Recursion continues until convergence or budget exhaustion. At the end each Hamiltonian is scored against **all** final cluster states and the best is kept — "computationally efficient because each cluster already logs the expectation values."

### 7. Parallelism type
**Task-parallel in structure but not in execution.** The tree is a task DAG over VQA jobs and the branches are independent, but the paper schedules them sequentially against one shot budget. The real mechanism is closer to **work sharing / redundancy elimination** than to parallelism. `[inference]` — the branches are trivially parallelizable and the artifact ships SLURM support, but the paper reports no parallel-execution result.

### 8. Computational bottleneck
**Throughput-bound on a shared, metered resource** — which in this taxonomy is closest to **bandwidth-bound**, where the scarce bandwidth is QPU shots per unit time and per dollar. Justified from the paper's own accounting: the entire contribution is measured in shots, never in wall-clock or FLOPs, and the motivating figure is 564 hours / $5.868M of *device time*, not classical compute. The classical side is explicitly asserted to be cheap (linear-cost slope monitoring, logged expectation values for recombination).

### 9. Evaluation setup
**Qiskit AerSimulator.** Noiseless runs use the statevector simulator; realistic runs use the **density-matrix simulator with device-calibrated noise models** from **IBM Hanoi, Cairo, Mumbai, Kolkata, Auckland** — calibrated models, **not the devices themselves**. Large systems use **PauliPropagation** for C₂H₂ and the 25-site Ising chain. **No real hardware.**

| Benchmark | Terms | Qubits | Tasks |
|---|---|---|---|
| H₂ (UCCSD) | 15 | 4 | 5 |
| LiH | 496 | 12 | 10 |
| BeH₂ | 810 | 14 | 10 |
| HF | 631 | 12 | 10 |
| C₂H₂ | 5945 | 28 | 10 |
| Transverse Ising | — | 25 sites / **50 qubits** | 10 |
| MaxCut (IEEE 14-bus) | — | 14 | 10 |
| XXZ chain | varies | varies | varies |

Shots: **N_per-eval = 4096 × (number of Pauli terms)**, identical for baseline and TreeVQA. Iterations typically **16,000–30,000** (H₂ converges in ~300). Optimizers SPSA (primary) and COBYLA; Red-QAOA and CAFQA for initialization comparisons.

### 10. Baseline
**Independent VQA execution per task with equal shot allocation** — i.e. the same optimizer, same ansatz, same shots-per-evaluation, run once per task with no sharing. Also compared against **CAFQA** initialization and **Meta-VQE** conceptually.

### 11. Quantitative results — with context
All results are **simulated**, **same shots-per-evaluation for baseline and TreeVQA**, and quoted **at matched target accuracy** (the paper's framing is "shots to reach a given fidelity").

| Result | Context |
|---|---|
| **25.9× average**, **>100×** on large-scale problems | "at the same target accuracy" — this is the correct comparison and the paper states it |
| HF: **~34.7× at 98% fidelity** (4 × 10⁹ vs ~1.5 × 10¹¹ shots) | Simulated. LiH, BeH₂, XXZ typically 30–40× |
| Precision sweep: **5–10×** at coarse precision → **80–100×** at fine → **>250×** at highest | Mechanism explanation given: "higher precision creates more subproblems with highly similar Hamiltonians." **The gain is a function of task-set similarity, not of TreeVQA per se** |
| Noisy device-calibrated models, LiH, 5-layer ansatz: Hanoi **12.0×**, Cairo **17.0×**, Mumbai **12.1×**, Kolkata **24.8×**, Auckland **14.7×** | **Calibrated noise models, not the devices.** Gains roughly halve versus noiseless |
| CAFQA integration: recovers **30%** of the residual gap using **7.3× (1.8 × 10¹⁰) fewer shots** | On LiH from CAFQA's 95.5% start |
| COBYLA: **2.5×–13×** | Lower than SPSA — optimizer-dependent |
| QAOA: **>20×** for similar instances, **>10×** as variance rises | Requires ma-QAOA, not standard QAOA |
| 1% depolarizing noise: "advantages marginally reduced... continues to deliver substantial shot savings" | No number given for this case |
| H₂: smaller savings | Small problem, little to share |

### 12. Hardware evidence level
**`SOFTWARE_SIMULATION`.** Qiskit Aer statevector and density-matrix, plus PauliPropagation for the largest cases. The IBM backend names appear only as **calibrated noise models**; nothing ran on a device.

### 13. Maturity framing
**`NISQ`** — variational algorithms, shot budgets, device noise models, no error correction anywhere.

### 14. Acknowledged limitations
Hyperparameter sensitivity — window size optimal at "~0.01%–0.02% of total iterations," splitting threshold "application-dependent," and split timing "crucial" (too early wastes shots, too late overfits); problem-dependence — "In the XXZ model, slow convergence causes TreeVQA to split tasks aggressively, slightly reducing its relative advantage"; diminishing returns when classical initialization already works; noise "deforms the VQA optimization landscape and introduces additional local minima," hurting both; QAOA needs a modified (multi-angle) ansatz because standard QAOA's 2p parameters give too little splitting granularity; C₂H₂ was under-evaluated "due to runtime constraints."

### 15. Artifact — `PARTIAL_MATCH`
**https://github.com/isaachyw/TreeVQA**, stated in the paper. `[code]` Python ≥3.12 with a **Julia** component via `juliacall`, `uv` for dependency management, LaTeX for plots. Module layout maps onto the paper: `TreeVQA/application/` (molecules, Ising, MaxCut), `TreeVQA/optimizer/` ("COBYLA, SPSA with TreeVQA" — i.e. the optimizers are TreeVQA-aware, matching the paper's plug-and-play claim), `TreeVQA/vqa/` ("VQE cluster execution utilities" — the cluster abstraction is real), `TreeVQA/clapton/` (Clifford-based circuit optimization, consistent with the CAFQA comparison), plus `config/` with COBYLA/SPSA/noisy variants, `ground-state/`, `plot_util/`. Entry points `main.py`, `batch_ne.py`, `single_vqe.py` (the baseline). Reproduction is a four-script pipeline: `0_setup.sh` (~5 min), `1_ground_truth.sh` (~1 h), `2_minimal_example.sh` (~10 min), `3_analysis_plot.sh` (~5 min). **Notably for this census, the main experiments require a cluster**: `python3 batch_ne.py config/your-config.json --slurm`, with `./concurrent_*.sh` generation for local runs — so the artifact is HPC-aware even though the paper reports no parallel-execution result.

Why `PARTIAL_MATCH` rather than `CONSISTENT`: the README documents the pipeline and the cluster abstraction but **does not describe the core algorithmic mechanism** — I found no README-level evidence of the spectral clustering, the mixed-Hamiltonian averaging, or the slope-based split trigger, and **I did not open the `.py` sources**. The directory named `TreeVQA/vqa/` "cluster execution utilities" is suggestive but is not the same as having read the splitting code. The gap is in my verification, not necessarily in the artifact.

### 16. HPC-scale question `[inference]`
TreeVQA is the paper in this set whose shape most resembles an HPC workflow manager: a set of related jobs, a shared budget, a controller deciding when to stop sharing work and fork. It is *already* not a single-device problem in structure — the artifact's SLURM path says so — but the paper's execution model is sequential, so the interesting question is what happens when the tree is actually run in parallel. The term that would dominate is **not communication** but **load imbalance**: branches split at data-dependent times, so cluster sizes become uneven and the tree is irregular and dynamic, which is the classic dynamic-task-graph scheduling problem rather than a bulk-synchronous one. Conditions worth stating: the benefit is a function of *inter-task similarity*, which the paper's own precision sweep demonstrates (5–10× → 250× as tasks get more similar), so at HPC scale the meaningful question is what the similarity distribution of a real workflow's task set looks like — a parameter-scan over molecular geometries is highly similar, a heterogeneous campaign is not. Second, the recombination step scores every Hamiltonian against every final cluster state, which is O(tasks × clusters) in logged expectation values — cheap at 10 tasks, worth checking at 10⁴. Third, the shot budget is a *shared metered resource across users*, which makes the controller a scheduling-policy question (fairness, preemption, backfill) that the single-user framing does not raise.

---

# PART B — CROSS-PAPER SYNTHESIS

## 1. The SNU lineage: paper 2 (2024) → paper 5 (2026)

Both papers are abstract-only to me, so this comparison is at the level of framing and stated claims, and I flag it as such.

**What stayed the same.** The group's method signature is unchanged: a **SW–HW co-design** framing, a **named subsystem** to optimize, an **unnamed "baseline"**, headline results as **bare ratios with no stated context**, and an evaluation that is a **simulation of a machine that does not exist**. In 2024: "Our multi-DR error handling SW-HW co-design improves the ESM latency, ESM errors, EDU latency, and EDU accuracy by 3.7 times, 2.4 times, 685 times, and 6.1 · 10¹⁰ times." In 2026: "ACQC achieves 4.4× speedup over the baseline qLDPC code FTQC and 18.3× qubit reduction over the surface code FTQC on average." Neither abstract names a prior system. Neither states problem size, precision, or whether numbers are end-to-end.

**What changed — four shifts, all in the same direction.**

*(a) From building a bigger machine to running programs on a smaller one.* The 2024 paper's object is the **machine**: DRs, cooling budgets, inter-DR entanglement, control electronics, and the closing claim is literally "we successfully build a fault-tolerant million qubit-scale quantum computer." The 2026 paper's object is the **program**: decomposition into supported operations, layout, magic-state distillation. The 2024 abstract's units are latency and error rate; the 2026 abstract's units are execution time and qubit count.

*(b) From surface-code assumptions to qLDPC.* This mirrors the shift your QEC census already documented across the whole ASPLOS corpus — 2024 pure surface code, 2026 majority qLDPC. The SNU group made the same move, and the stated motivation is capacity: qLDPC needs "an order of magnitude fewer qubits."

*(c) The bottleneck inverted.* In 2024 the enemy was **latency** — ESM latency, EDU latency, inter-DR communication latency; the 685× and 6.1 × 10¹⁰× figures are decoder-side. In 2026 the enemy is **execution time at the application level** — "tens of days" — and the decoder does not appear in the abstract at all. The group moved from *can we correct errors fast enough* to *can we finish the program this decade*. Consistent with the corpus-wide migration your QEC census identified: runtime hardware in 2024–25, compile-time synthesis in 2026.

*(d) The technology assumption became less load-bearing, and the honesty got sharper.* 2024 rests on "**assumed** voltage-scaled CMOS and **mature** ERSFQ technologies" — an explicit projection about superconducting control electronics that do not exist. 2026 says something much more checkable: "**As there is currently no available hardware for qLDPC codes, we evaluate ACQC with a comprehensive simulation.**" That sentence is a clearer statement of evidence level than anything in the 2024 abstract, even though both are simulations.

**One thing that did not improve:** neither paper released an artifact, despite the group maintaining a 13-repo GitHub org that *does* contain XQsim, QIsim, CryoModel, and code for their MICRO and ASPLOS'26 BCI papers. The group releases tools and withholds the quantum-architecture papers built on them. For a census tracking reproducibility norms, that pattern is worth recording precisely because it is not a capacity problem.

## 2. BQSim versus SC's simulation papers (Atlas, SC24; PTSBE, SC25)

This is the sharpest venue contrast available, because all three are GPU quantum-simulation papers and all three are batching/partitioning contributions.

| | **BQSim** (ASPLOS'25) | **Atlas** (SC24) | **PTSBE** (SC25) |
|---|---|---|---|
| Hardware | **1 × RTX A6000 (48 GB)**, 1 node | **Up to 256 A100s on Perlmutter** (named machine) | **4 × H100 (80 GB)** on **NVIDIA Eos DGX SuperPOD**; 4,445 + 2,223 H100-hours |
| Scale | 6–21 qubits | 28–36 qubits | 35 qubits (statevector), 85 qubits (tensornet) |
| Communication | **Absent** — no inter-device transfer exists in the design | **The entire contribution** — ILP minimizes it with c=3 inter-node weighting | **Absent by design** — `PTSBESample.h:420`: "PTSBE is simulator-only so no multi-QPU distribution is used" |
| Scaling study | Batch-size sweep on one GPU (B=32→1024) | **Weak scaling 1→256 GPUs**: Atlas grows 13.7×, HyQuas 267.9× | Batch-size efficiency curve; node counts `NOT_FOUND` |
| What is batched | **Input state vectors** through a fixed circuit | Nothing — one state vector, partitioned | **Noise trajectories**; shots drawn in bulk per prepared statevector |
| Contribution type | Representation lowering (DD→ELL) + fusion cost model + host-side pipelining | **Communication-optimal partitioning** (ILP with proven minimum stage count) | **Amortizing statevector preparation across a shot batch** |
| Precision stated | No — `CONTEXT_NOT_STATED` | No — `CONTEXT_NOT_STATED` (though the code has a compile-time switch) | Not established |
| Artifact | `CONSISTENT`, complete, in-tree baselines | `CONSISTENT`, strongest in the SC census (code + artifact repo + Zenodo, AD/AE reviewed) | `CONSISTENT` for mechanism; **experiments not reproducible** — upstreamed into CUDA-Q with no paper harness |

**The framing difference, stated plainly.**

*What counts as the contribution.* At SC, the contribution is **how the work is spread across a machine**. Atlas contains, by design, no quantum algorithm, no physics, no approximation — the census's own note is that "remove the HPC contribution and *nothing remains*." Its most convincing single number is a **communication-scaling** number (13.7× vs 267.9× growth to 256 GPUs), not a kernel number. At ASPLOS, BQSim's contribution is **how a data structure is made to fit an execution model** — an irregular pointer DAG lowered to ELL so a SIMT machine can eat it, with a cost model (#MAC) driving the fusion that produces it. That is a compiler/representation contribution, and its most convincing number is an ablation (DD→ELL worth 5.55–35.08×), not a scaling curve. **ASPLOS rewards the mechanism; SC rewards the scaling behaviour of the mechanism.**

*The role of communication.* This is the cleanest split. Atlas *is* a communication paper — the ILP exists to weight inter-node movement and push all of it to stage boundaries. BQSim has **no communication term at all**: state vectors in a batch never interact, so the design's only data-movement concern is host↔device PCIe, handled with four buffers and a task graph. Interestingly, **PTSBE sits on BQSim's side of this line, not Atlas's** — it too is single-node-shaped (4 GPUs, no multi-QPU distribution) and its contribution is also batch amortization. So the split is not simply venue; it is *problem shape*. Both BQSim and PTSBE found an axis of the simulation problem that is embarrassingly parallel (independent inputs; independent trajectories) and exploited it without ever needing an interconnect. Atlas took the axis that is not (one state vector, split across devices) and made communication the object.

*Scale, and what the venue demands of it.* SC papers in this corpus run on **named facilities** — Perlmutter, Eos — and report GPU-hours and scaling curves. BQSim runs on **one workstation-class GPU** and reports a batch-size sweep. Neither is wrong for its venue, but the consequence for your census is concrete: **BQSim's multi-GPU claim is unevaluated** ("BQSim can scale to larger qubit counts by adjusting batch sizes and leveraging multiple GPUs"), and the repository contains no multi-GPU code. At SC that sentence would have had to be an experiment. The reciprocal observation is equally real: PTSBE's headline 10⁶× is a **shots/second efficiency ratio against its own unbatched mode**, not a fixed-workload wall-clock speedup — SC's facility norms did not prevent a context-heavy headline number, and BQSim's 3.25× vs cuQuantum on the same GPU is, in isolation, the better-controlled comparison of the two.

*One more asymmetry worth recording.* BQSim's baseline set is **three named systems with an in-tree harness for each** (`cuquantum.sh`, `qiskit-aer.sh`, `flatdd.sh`, plus `apps/DDSIM.cpp` and `apps/FlatDD.cpp`), and it includes the unusual step of transplanting its own fused gates into the competitor (`cuquantum_plus_bq.sh`) to isolate representation from kernel. Atlas's fair-comparison control (disabling DRAM offloading to match baselines) is the SC equivalent. Both are good practice; the ASPLOS version is at the level of *representation*, the SC version at the level of *memory hierarchy*.

## 3. Evidence levels: what fraction is real hardware?

| # | Paper | Evidence level | What was actually measured |
|---|---|---|---|
| 1 | **BQSim** | `SOFTWARE_SIMULATION` | **Real wall-clock on real silicon** (1 × A6000). The simulated thing is quantum; the measurement is genuine |
| 2 | **Million-Qubit** | **`PROJECTED`** (likely `ARCH_SIMULATION` + `ANALYTIC_MODEL` `[inference]`) | Nothing measurable is publicly established. "Assumed voltage-scaled CMOS and mature ERSFQ" |
| 3 | **MECH** | `ANALYTIC_MODEL` + `SOFTWARE_SIMULATION` | Compiler output metrics (depth, CNOT count) under a parametric error model. No execution |
| 4 | **Fat-Tree QRAM** | **`ANALYTIC_MODEL`** | Complexity classes, router counts, circuit layers. No simulator run at all |
| 5 | **ACQC** | `SOFTWARE_SIMULATION` or `ARCH_SIMULATION` (undetermined) | "Comprehensive simulation," unspecified |
| 6 | **COMPAS** | `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` | Stim/Qiskit on circuit *components*; system fidelity composed analytically because the full circuit is too big |
| 7 | **QRCC** | **`REAL_HARDWARE`** (N=7) + `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (N>27) | **IBM Lagos, 7 qubits** — the only quantum-hardware execution in the set. Everything above N=27 is solver output |
| 8 | **TreeVQA** | `SOFTWARE_SIMULATION` | Qiskit Aer; IBM backend names are **calibrated noise models**, not devices |

**Counting.** Quantum hardware executed: **1 of 8 (QRCC)**, and only at N=7 with D=4 — a demonstration, not a validation of its N=300 analysis. Classical hardware measured with a wall clock: **2 of 8** (BQSim end-to-end; QRCC's Gurobi solve times, though on an unstated host). **Purely analytic or projected: 2 of 8** (Fat-Tree QRAM, Million-Qubit). **Simulation-only: the remaining 4.** Papers 2, 3, 4 and 5 are all architecture proposals for machines that do not exist, and their numbers are model outputs.

**Versus SC's norms.** The SC census in your corpus has Atlas on **Perlmutter** (named facility, 256 A100s, weak- and strong-scaling), PTSBE on **NVIDIA Eos** (named facility, GPU-hour budget reported), and the practice of naming the machine and reporting node counts is close to universal there. Here, **only BQSim names its hardware in a way that lets you reason about the result**, and even it does not state precision. Two papers do not name their compute host at all: **QRCC's CPU model, cores and RAM are absent from both the preprint and the published camera-ready**, and MECH reports only "Intel CPU, up to 32 GB RAM."

The important qualification, and I want to be careful here: **this is a difference in what the two venues are for, not a quality gap.** ASPLOS accepts architecture proposals for hardware that does not yet exist — that is the point of the venue, and the surface-code and qLDPC machines these papers target are a decade out. SC's papers run on real supercomputers because SC's subject *is* the supercomputer. The finding for your census is not "ASPLOS is weaker"; it is that **the two venues place the burden of proof at different points**: SC requires that the *machine* be real and the workload may be artificial; ASPLOS permits the *machine* to be hypothetical provided the *mechanism* is precisely specified. BQSim is interesting precisely because it satisfies both — a real measurement of a real mechanism on real silicon — and it is the only paper here that does.

A secondary reproducibility observation: **artifacts are 3 of 8 verified** (BQSim `CONSISTENT`, COMPAS `CONSISTENT`, TreeVQA `PARTIAL_MATCH`), **1 claimed but unopened** (MECH's Zenodo DOI), and **4 with none** (Million-Qubit, Fat-Tree QRAM, ACQC, QRCC). ACQC is nominally Gold open access yet has no PDF outside ACM DL — open-access status and actual retrievability came apart.

## 4. Multi-node extension potential `[inference]` — all of this section is inference

**Natural multi-node extension, cheap communication term:**

- **BQSim (batch axis)** — the strongest case. State vectors in a batch never interact, so distribution is scatter-inputs / gather-results with no exchange during the sweep. The only replicated object is the ELL gate stream, which is small. The paper's own future-work sentence is exactly this axis. Communication term: broadcast of the fused-gate ELL structure, plus H2D bandwidth per device. **Note this would be a throughput contribution, not a capacity one** — it does not let you simulate more qubits, only more inputs.
- **QRCC (subcircuit execution)** — 4^k·6^m independent jobs, zero inter-job communication. This is a batch-queue workload as-is. Its reconstruction phase is the part that resists: a Kronecker-product tree with O(2^(N+2k)) intermediates, where ARP's recursive partitioning already reframes the cost in terms of *maximum cuts between adjacent partitions* — a bisection-style quantity.
- **TreeVQA** — the branches are independent by construction and the artifact already ships SLURM support; the paper simply does not run them in parallel. The obstacle is **load imbalance from data-dependent splitting**, not communication.
- **COMPAS** — already distributed; the question is not whether it extends but **how far**, and the paper answers: k ≤ O(ε/(np)), ≈5 nodes at n=100, ε=10⁻³. Extension is blocked by link fidelity, not by design.

**Intrinsically single-device, or where "multi-node" is the wrong frame:**

- **Fat-Tree QRAM** — this is one memory device. Its whole contribution is *internal* topology. A "distributed QRAM" would be a different paper with a different cost model; nothing here extends.
- **BQSim (qubit axis)** — splitting one 2ⁿ state vector across devices reintroduces the global-qubit all-to-all that Atlas exists to solve, and BQSim has no mechanism for it. **The batch axis and the qubit axis are not the same extension** and should not be conflated when the paper's future-work sentence mentions both in one breath.
- **MECH** — the *compiled machine* is already multi-chiplet, but the *compiler* is a serial greedy program whose orderings (ascending distance for entrances, descending component count for gates) are global sequential dependences. Parallelizing the compiler is the open problem, not distributing the machine.
- **Million-Qubit (paper 2)** — inverted case: it is *born* multi-node (multi-DR) and there is no single-device version. The interesting question is the opposite one — what the minimum viable node count is, and whether the inter-DR entanglement rate can sustain the syndrome traffic.
- **ACQC** — undetermined from the abstract. Its stated time/qubit tradeoff implies a partitioning pressure at scale, but there is no public evidence about whether cut cost is modelled.

**The pattern worth carrying into the census.** Sort these eight by whether communication appears in the cost model at all, and you get a clean split: **COMPAS, MECH, and the Million-Qubit paper make communication the object of optimization** (Bell pairs, cross-chip links, inter-DR latency) — these are the SC-shaped ones by the criterion your own census uses. **BQSim, QRCC's execution phase, and TreeVQA found axes where communication is absent**, and their contributions are correspondingly about representation, search, and work-sharing. **Fat-Tree QRAM and ACQC are capacity/topology papers where the relevant term is space, not messages.** The papers most likely to transfer to an HPC setting without reformulation are the ones in the second group — precisely because their parallelism is trivial and their real bottlenecks (memory footprint, reconstruction tensors, load imbalance) are ordinary HPC problems wearing quantum clothing.

---

## Sources

[BQSim published PDF](https://tsung-wei-huang.github.io/papers/2025-asplos.pdf) · [BQSim ACM record](https://dl.acm.org/doi/10.1145/3676641.3715984) · [BQSim code](https://github.com/IDEA-CUHK/BQSim) · [Million-Qubit ACM record](https://dl.acm.org/doi/10.1145/3620665.3640388) · [SNU HPCS publications](https://hpcs.snu.ac.kr/publications/) · [SNU HPCS quantum research page](https://hpcs.snu.ac.kr/research/cryogenic-and-quantum-computing/) · [SNU-HPCS GitHub org](https://github.com/SNU-HPCS) · [MECH arXiv abs](https://arxiv.org/abs/2305.05149) · [MECH arXiv PDF](https://arxiv.org/pdf/2305.05149) · [Fat-Tree QRAM arXiv](https://arxiv.org/abs/2502.06767) · [Fat-Tree QRAM HTML](https://arxiv.org/html/2502.06767v1) · [ACQC ACM record](https://dl.acm.org/doi/10.1145/3779212.3790122) · [ACQC INSPIRE](https://inspirehep.net/literature/3131971) · [COMPAS arXiv HTML](https://arxiv.org/html/2511.23434v2) · [COMPAS ACM record](https://dl.acm.org/doi/abs/10.1145/3779212.3790143) · [COMPAS code](https://github.com/kunliu7/Distributed-Q-Algo) · [QRCC arXiv](https://arxiv.org/abs/2312.10298) · [QRCC camera-ready PDF](https://xzt102.github.io/publications/QRCC_ASPLOS2024.pdf) · [TreeVQA arXiv](https://arxiv.org/abs/2512.12068) · [TreeVQA HTML](https://arxiv.org/html/2512.12068) · [TreeVQA code](https://github.com/isaachyw/TreeVQA) · [Systems Architecture for QRAM, MICRO'23](https://dl.acm.org/doi/10.1145/3613424.3614270) · [Yongshan Ding publications](https://www.yongshanding.com/publications.html) · [Gokul Ravi publications](https://gsravi.engin.umich.edu/publications/)
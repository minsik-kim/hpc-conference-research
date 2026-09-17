# ACM ICS 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.

## 1. Population and denominators

| Year | Regular papers | Volume | Page span | Method | Count status | Corroboration | Relevant | Share |
|---|---:|---|---|---|---|---|---:|---:|
| ICS 2024 (38th, Kyoto) | **45** | `10.1145/3650200` | 1–561 | `VOLUME_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | 3 sources | **1** | 2.2% |
| ICS 2025 (39th, Salt Lake City) | **83** | `10.1145/3721145` | 1–~1247 | `VOLUME_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | 2 sources | **2** | 2.4% |
| ICS 2026 (40th) | **102** (+3 keynote abstracts = 105 TOC entries) | `10.1145/3797905` | 4–1362 | `VOLUME_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | 2 sources | **5** | 4.9% |

**Completeness proof — page-range tiling.** For each year the TOC was enumerated *with page ranges*
and the ranges tile the volume with zero gaps and zero overlaps: 2024's 45 entries tile **1–561**
exactly (leaving no room for a 46th paper); 2025's entries 1–82 tile **1–1233** with entry 83
beginning at 1234, confirmed by the official program's Memory Systems session; 2026's 105 entries
tile **1–1362**, of which entries 1–3 are one-page keynote abstracts (Wu/Meta, Grosser/Cambridge,
Hadade/ECMWF) confirmed as keynotes by the program, leaving **102** regular papers on pp. 4–1362.

**DOI-contiguity was attempted and found unreliable here** — a documented negative result. ACM
article-IDs in these volumes are not assigned in page order and are split across non-contiguous
blocks (quEStab at p. 1296 is `.3816723` while EZCache at p. 1310 is `.3807838`), so gap probing
produces false "extra paper" signals. Every probed ID resolved to an already-enumerated paper, which
is a useful *negative* check but cannot prove completeness. Page tiling is the load-bearing evidence.

A page-summarizing model returned three different totals for the same ICS 2024 page (45, 50, 51);
only per-entry enumeration with page ranges is trustworthy. The workshops volume `10.1145/3774895`
is a separate volume and is excluded.

## 2. The ICS 2024 correction — the headline finding of this venue

**Prior work recorded ICS 2024 as "none found by keyword sweep" — explicitly not a hand-counted
zero. The hand count is 1, not 0.**

**2024-1 · Minimizing Coherence Errors via Dynamic Decoupling**
Soheil Khadirsharbiyani, Movahhed Sadeghi (Penn State), Mostafa Eghbali Zarch (NC State),
Mahmut Kandemir (Penn State) · `10.1145/3650200.3656617`, pp. 164–175 ·
**Session 5A "Reliability, Dependability and Availability"** — not a quantum session ·
`HPC_FOR_Q` · NISQ · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · `[proceedings][official-program][abstract]`

Characterizes the device **once**, then inserts X-Y-X-Y dynamic-decoupling sequences into circuit
idle windows sized by computed per-qubit slack, instead of running many trial circuit variants.
*Quantum problem:* decoherence accumulates on idle ("hole") qubits because of uneven gate durations
and connectivity constraints; DD pulses suppress it at the cost of added gate error.
*HPC problem:* prior DD methods require executing many circuit versions to find the best
configuration — an expensive characterization search. This reformulates it as one-shot system
characterization plus static slack analysis over a dependence schedule, **cutting characterization
experiments by 89%**. PST gains 1.15×/1.1×/1.2× at small/medium/large scale vs state of the art,
1.6× vs no-DD, 1.4× vs existing DD baselines; Qiskit + QASMBench.
Real-QPU execution is strongly implied by the PST metric and the characterization-experiment count
but the evaluation section could not be read (ACM DL 403) — recorded as `[inference]`, not fact.

**Why a keyword sweep missed it:** neither the title nor the session name contains "quantum" — the
paper is named after its technique. It was found only by hand-scanning every title in the enumerated
volume. This is the concrete justification for the full-population method.

## 3. Relevant papers, 2025 and 2026

### ICS 2025 — 2 of 83

**2025-1 · BMQSim: Overcoming Memory Constraints in Quantum Circuit Simulation with a High-Fidelity
Compression Framework** — Boyuan Zhang (Indiana) et al. with UCAS, PNNL, ICT-CAS ·
`10.1145/3721145.3725747`, pp. 689–704, **Best Papers session**, arXiv 2410.14088 · `HPC_FOR_Q` ·
**SOFTWARE_SIMULATION** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · GENERAL

Lossy-compresses the statevector in GPU memory under point-wise relative error control, with
circuit-stage partitioning to amortize compression cost.
**Simulation detail** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §2): statevector, **float64**
(contrasted with cuQuantum's float32-only); compression via NVIDIA nvCOMP **bitcomp** with a GPU
log-transform `b_a = log2(1 + b_r)` converting relative to absolute bounds, operating at a
**10⁻³ point-wise relative error bound**; stage partitioning takes a 33-qubit QFT from **2,673
compression events (one per gate) to 28** (one per stage); **no MPI** — CUDA streams, and multi-GPU
mode is embarrassingly parallel with *no GPU-to-GPU communication*; two-level GPU↔SSD via
**GPUDirect Storage/cuFile**, costing 0.7% on average.
**Numbers with context:** on a Xeon Gold 6238R + 2× A4000 (16 GB) + SATA SSD, **42 qubits in GPU
memory and 47 with SSD backing**, versus baselines supporting ~30. Memory reduction is strongly
circuit-dependent — **cat_state 678.61×, ghz 678.52×, bv 424.77×, but QFT only 10.54×** (">10× on
average"). Fidelity >0.99 for 24–30-qubit circuits; at 27-qubit QFT, 0.998 vs SC19-Sim's 0.665.
On 4× A100 NVLink, 28-qubit QFT scales **1.7× (2 GPUs), 2.3× (4 GPUs)** — the paper attributes the
cap to **PCIe** and GPU launch overhead.
*Which term it attacks:* **T_memory (capacity), purchased with T_local_compute.** It does not attack
communication — it removes the network from the design entirely, and the residual PCIe term is what
limits its multi-GPU scaling.

**2025-2 · OpaQue: Program Output Obfuscation for Quantum Software Circuits in Quantum Clouds** —
Tirthak Patel (Rice), Aditya Ranjan, Daniel Silver (Northeastern), Harshitta Gandhi, William Cutler
(Oxford), Devesh Tiwari (Northeastern) · `10.1145/3721145.3725771`, pp. 1079–1091, Potpourri
session · `Q_IN_HPC` · **REAL_QPU** (IBM Lagos 7q, Toronto 27q, Washington 127q; plus Aer noisy and
ideal simulation; 4–128 qubits, hardware runs to 32) · Artifact **`PUBLIC_ARTIFACT`**
`https://zenodo.org/doi/10.5281/zenodo.10896069` · NISQ

*Quantum problem:* obfuscating gates must not wreck fidelity on noisy devices and must be invertible
in the measurement-distribution domain. *HPC problem:* confidentiality of a workload executed on a
shared, untrusted remote accelerator, plus the classical encode/decode cost — the classic
multi-tenancy and remote-offload security problem, with a QPU as the accelerator.

### ICS 2026 — 5 of 102, all in the dedicated **Quantum Computing** session

Session verified independently: Thursday 9 July 2026, 15:30–17:10, chair Miquel Moretó, exactly 5
papers, **proceedings pp. 1296–1362** — matching the page tiling exactly.

**2026-1 · quEStab: Towards Scalable Quantum Circuit Simulation on Multi-GPU using an Extended
Stabilizer Formalism** — Hyunjoon Shin, Seokhyeon Lee, Myeongjin Kwak, Yongtae Kim (Kyungpook
National University) · `10.1145/3797905.3816723`, pp. 1296–1309 · `HPC_FOR_Q` ·
**SOFTWARE_SIMULATION** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · GENERAL
Extends the stabilizer tableau to mixed Clifford/non-Clifford circuits and distributes independent
Pauli groups across GPUs, with a two-stage CUDA kernel pipeline separating row-counting from
row-updates. Verified verbatim from the abstract: peak memory reduced **up to 10,126×** vs
statevector, circuits **up to 30,000 qubits**, 128 QASMBench circuits at 78.1% coverage.
**Evidence limitation:** the ACM record is marked Gold OA/CC-BY but ACM DL returned 403 to every
request, and no preprint exists — so the kernel-pipeline design, the GPU model, the baseline
identity, precision, synchronization and the strong/weak-scaling mode are all `INSUFFICIENT_EVIDENCE`
and are deliberately not restated as findings.
*Which term it attacks:* **T_memory, by representation change** — the only simulator in this corpus
that escapes 2ⁿ rather than managing it.

**2026-2 · EZCache: A Hierarchical Memory System for Zoned Neutral Atom Quantum Computers** —
Jiayi Zhong (ECNU), Yuxin Deng (SHUFE/ECNU), Hui Jiang (CQUPT), Jiacheng Feng (Pittsburgh) ·
`10.1145/3797905.3807838`, pp. 1310–1321 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
**SOFTWARE_SIMULATION / compiler-level** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · regime `UNCLEAR`
Treats the dark region of the entangling zone as a **capacity-limited cache tier** for idle qubits,
with reuse-window residency and look-ahead parking, cutting long-distance atom shuttling.
*HPC problem:* literally a cache-replacement and data-placement problem — a fast tier with limited
capacity, reuse-distance prediction from near-future access patterns, and look-ahead prefetch across
parallel operations. **Arguably the purest "HPC framing of a quantum problem" in the whole census.**
+18.1% fidelity vs PowerMove, +64.2% vs ZAC, −52.4% movement.

**2026-3 · TuniQ: Autotuning Compilation Passes for Quantum Workloads at Scale for Effectiveness and
Efficiency** — Mohammad Abrarul Hasanat (**University of Utah**), Jason Ludmir (Rice), Tirthak Patel
(Rice), Rohan Basu Roy (Utah) · `10.1145/3797905.3807862`, pp. 1322–1336, arXiv 2605.11375 ·
`HPC_FOR_Q`, `Q_IN_HPC` · **REAL_QPU** + SOFTWARE_SIMULATION · Artifact **`PUBLIC_ARTIFACT`**
`https://zenodo.org/records/19969999` · NISQ
*(Affiliation correction: prior work attributed TuniQ to Rice; it is a Utah–Rice collaboration with
the first author at Utah.)*

**The clearest "classical compilation is itself the HPC bottleneck" paper in the corpus.** A
MaskablePPO agent selects transpiler passes per stage of Qiskit's six-stage pipeline, adapting to
circuit, backend and live calibration.
**Cost model** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §10), verbatim:
`R_final = W·clip(log(ESP_rl / ESP_L3)) + φ(w₁·r_gates + w₂·r_depth)` — **the numeric values of
W, w₁, w₂ are not given in the paper**, a real gap in an otherwise precise model. State = one-hot
stage indicator + a dual encoder (logical qubit-interaction pre-layout; hardware-aware post-routing
with gate errors, T₁/T₂, connectivity) + global features; action = a Qiskit pass or `skip` under
dynamic action masking.
**Numbers with context** (baseline throughout = Qiskit Level 3, fidelity-optimized): TVD improves
**20% on average**; compilation time drops **34% on average**; at **30–50 qubits (QFT, QPE):
−68% compilation time, −27% gates, −25% depth**; at 65 qubits with a transferred pass sequence,
−40% gates, −50% depth, 2–3× faster compilation; zero-shot transfer to Torino/Fez up to −67%
compile time. Hardware: IBM **Torino (133q Heron r1), Fez (156q r2), Kingston (133q r2), Pittsburgh
(156q r3)**, 8,192 shots; controlled sweeps on **8 NVIDIA H200 GPUs**, Aer density-matrix, 16,384
shots. Training: 8 parallel workers, PPO, 2,048 steps/update, batch 64, over 30 perturbed backend
instances — **but training wall-clock time is not reported**, which is the one number the
"compilation is the bottleneck" argument most needs. Inference adds **<1%** to transpilation time.
The paper reports an honest counterexample: on QUARK Cardinality it *increases* compile time by
selecting LookaheadSwap, buying 20% better TVD.

**2026-4 · C-3PQ: A Closeness Centrality-based Circuit Partitioner for Quantum Simulations** —
Doru Thom Popovici, Mauro Del Ben, Katherine Klymko, Daan Camps, Anastasiia Butko (LBNL),
Harlin Lee (UNC), Naoki Yoshioka, Nobuyasu Ito (RIKEN R-CCS) · `10.1145/3797905.3807864`,
pp. 1337–1349, arXiv 2509.14098 · `HPC_FOR_Q` · **SOFTWARE_SIMULATION on REAL_HARDWARE** ·
Artifact `NO_PUBLIC_ARTIFACT_FOUND` · GENERAL

Statevector laid out as a multi-dimensional tensor executed as chains of tensor contractions;
partitioning ranks gates by **closeness centrality** `CC(v) = |RN(v)| / dist(v)`, applied
**recursively per memory level**, labelling dimensions local or global by fit; a code generator
emits **C++, CUDA and HIP**.
**Communication:** MPI, using **cray-mpich/8.1.30 GPU-aware collectives** on Perlmutter and Frontier
(which collectives is never named; no NCCL/RCCL). Stated limitation: the generated CPU code is
**scalar** — no SVE/AVX intrinsics despite the A64FX target. Precision is not stated anywhere
readable → `INSUFFICIENT_EVIDENCE`.
**Scale:** Perlmutter (A100), Frontier (MI250X), Fugaku (A64FX); **30–37 qubits**; **weak scaling**,
starting at **4 GPUs for 30 qubits** — it never runs single-device. Classical partitioner cost is
reported: under one second for most circuits, ~4 s and ~55 s for `qnn` and `vqc`. The abstract's
"up to 40% speedup vs a state-of-the-art NVIDIA-specific implementation" is **not restated with
hardware/circuit/scale context in the readable body** → `PARTIAL` on that number; the body says only
"competitive with the Atlas framework".
*Which term it attacks:* **T_communication** — the paper's own framing is that communication
dominates on accelerated systems.

**2026-5 · Diagonal-Budgeted Trotterization for Efficient Quantum Hamiltonian Simulation** —
Srikar Chundury, Blake Burgstahler, Jiajia Li, Frank Mueller (NC State), In-Saeng Suh (ORNL) ·
`10.1145/3797905.3807869`, pp. 1350–1362, arXiv 2606.16959 · `HPC_FOR_Q`, `Q_FOR_HPC`,
`FUTURE_WORKLOAD` · **classical simulation only** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · GENERAL
Decomposes Hamiltonians into factors preserving diagonal sparsity under a fidelity budget, with a
custom diagonal-sparse data structure (tool: HamSim), hand-optimized C++/CUDA kernels, SIMD and
multithreading. **182–1,269× on CPU** and **up to 178× on GPU** for **12–16 qubit** systems at
near-perfect fidelity. MPI/distributed and strong/weak scaling are not reported.

## 4. Exclusions

| Paper | Year | Why excluded |
|---|---|---|
| **Parallel Quadratic Selected Inversion in Quantum Transport Simulation** (ETH/TU Braunschweig/USI), pp. 1284–1295, `.3807841` | 2026 | **Verified twice**: the official program places it in **"Numerical & Scientific Kernels"**, not the quantum session (the page adjacency is coincidental), and the preprint confirms classical NEGF device simulation — distributed selected inversion of block-tridiagonal-arrowhead matrices, 5.2× over PARDISO, on Xeon/GH200. **Confirms the prior flag.** |
| **SpinTune: Improving the Reliability of Quantum Sensor Networks** (Rice), pp. 986–999, `.3807861` | 2026 | Genuinely quantum, and its abstract even frames sensors as components of hybrid quantum-classical HPC — but it is unambiguously **quantum sensing**: RL-discovered adaptive DD sequences on a Carbon-13 spin-bath model with an AC-magnetometry sensitivity metric (+80%), validated on QuEra Aquila via Braket. No parallelism, scaling, resource-management, memory or communication contribution; its official session is "Resilience and Error Detection". **Excluded, logged as sensing. Confirms the prior flag.** |
| Graph Convolutional Network Acceleration Using Adiabatic Superconductor Josephson Devices | 2025 | **AQFP is classical** superconducting digital logic. |
| JBSA: A Bit-Serial Accelerator … Using Superconducting SFQ Logic | 2025 | **SFQ is classical.** |
| Efficient Privacy Computing session (MegaZK, SumcheckPIM, GPIR, FHE transformer inference, CipherSkip) | 2026 | ZKP/PIR/FHE on classical hardware; not PQC-vs-Shor work, no quantum computation. |
| NEOCNN (2024), ROCKET (2025) | 2024/25 | Classical optical/photonic accelerators. |

**Workshop note, recorded for a future decision:** ICS 2024 co-located the **International Workshop
on Quantum Classical Cooperative Computing (QCCC)** and ICS 2026 the **PhysQ** workshop. Both are
highly on-topic for this domain and both are **out of scope** under the regular-paper-only rule.
If the project's scope ever widens to workshops, these are probably the densest Quantum-HPC venues
in the ICS orbit.

No `STATUS_UNCLEAR` items: all 230 regular papers across the three years were cleanly classifiable,
and the only non-regular TOC entries (three one-page keynote abstracts in 2026) are unambiguous.

## 5. What ICS rewards as a contribution

ICS accepts quantum work **when and only when it is shaped like an existing ICS paper**. The five
2026 papers map one-to-one onto ICS's own standing categories: a multi-GPU parallel data structure
(quEStab), a memory hierarchy with reuse-distance prediction (EZCache), compiler autotuning over a
huge search space (TuniQ), communication-avoiding partitioning with performance-portable codegen
(C-3PQ), and a sparse kernel with SIMD/GPU optimization (Diagonal-Budgeted Trotterization). BMQSim
(2025) is a GPU lossy-compression and memory-hierarchy paper of exactly the kind ICS publishes
constantly, and it won a Best Paper slot. The ICS 2024 paper was accepted into a **reliability**
session, not a quantum one.

That is a sharply different filter from the architecture venues: ICS does not reward a *machine
proposal*, it rewards a *kernel, data structure or scheduling technique with measured scaling*.
The trajectory 1 → 2 → 5 (2.2% → 2.4% → 4.9%) with a dedicated session appearing only in 2026 makes
ICS the fastest-rising HPC venue in this census, and the one whose acceptance criteria most closely
resemble SC's.

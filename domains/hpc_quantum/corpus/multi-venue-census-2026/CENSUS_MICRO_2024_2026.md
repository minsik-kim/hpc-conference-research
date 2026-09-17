# MICRO 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.

## 1. Population and denominators

| Year | Proceedings | Regular main-track papers | Method | Count status | Corroboration | Relevant | Share |
|---|---|---:|---|---|---|---:|---:|
| MICRO-57 / 2024 (Austin) | IEEE, `10.1109/MICRO61859.2024.*` | **113** | `VOLUME_ENUMERATED` + `PUBLISHER_TOC_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | 2 shapes agree exactly | **3** | 2.7% |
| MICRO-58 / 2025 (Seoul) | ACM, `10.1145/3725843` | **123** | `VOLUME_ENUMERATED` + `PUBLISHER_TOC_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | 2 shapes agree exactly | **8** | 6.5% |
| MICRO-59 / 2026 | not yet published | **UNKNOWN** | — | **`PROGRAM_INCOMPLETE_AS_OF_2026-09-17`** | n/a | **UNKNOWN** | — |

**2024** — 115 researchr entries minus 2 front-matter items = **113 papers**, whose page ranges tile
**1–1705 with zero gaps and zero overlaps**. The official program independently sums to **113**
across 32 technical sessions (1A–11C), excluding keynotes, panels, posters, the PhD Forum and the
SRC. Exact agreement.

**2025** — **123 entries**, all research papers, tiling **1–1881 with zero gaps and zero overlaps**.
The official program sums to **123** across 33 sessions. Exact agreement. (Session letters 3D, 8D and
9D do not exist — those slots ran fewer parallel tracks; consistent, not a gap.)

**Non-archival items excluded:** MICRO 2024's PhD Forum Lightning Session and Student Research
Competition, neither of which appears in the page-tiled volume. **Neither 2024 nor 2025 had an
industry track.** MICRO-59 announces an **inaugural Industry Track** separate from the regular track,
which will need its own status decision when those proceedings appear.

### MICRO-59 (2026) publication status — precise, as of 2026-09-17

**Not public.** Four independent probes: (1) `microarch.org/micro59/` is live and is genuinely the
2026 site, but its **Program menu contains only "Workshops & Tutorials"** — no accepted-papers or
main-program link; (2) the site states **Author Notification 7 July 2026** and **camera-ready due
11 September 2026**, i.e. six days before this census; (3) `researchr.org/publication/micro-2026`
returns **404** — no publisher TOC mirrored; (4) a targeted search returned only CFP, submission and
artifact-evaluation pages. **No entries invented.** This closes the Phase-1 note
`PROGRAM_INCOMPLETE_AS_OF_2026-09-06` by re-verifying it eleven days later and finding it unchanged.

*Tooling caveat recorded:* one fetch of the trailing-slash directory `microarch.org/micro59/program/`
returned MICRO **2025** content — a server/fetcher fallback to the micro58 program. Always verify the
year stated in the page header.

**Venue scope** `[official-CFP]`: MICRO has carried a standalone *"Quantum computing"* bullet in all
three years — the longest-standing explicit quantum scope among the architecture venues.

## 2. Relevant papers

### MICRO 2024 — 3 of 113 · all in **Session 5B: Quantum** (Tue 5 Nov, chair Yunong Shi, AWS)

**1 · Flag-Proxy Networks: Overcoming the Architectural, Scheduling and Decoding Obstacles of Quantum
LDPC Codes** — Suhas Vittal (Georgia Tech), Ali Javadi-Abhari, Andrew W. Cross, Lev S. Bishop (IBM),
Moinuddin Qureshi (Georgia Tech) · `10.1109/MICRO61859.2024.00059`, pp. 718–734, arXiv 2409.14283 ·
`HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** (Stim) · Artifact **`PUBLIC_ARTIFACT`**
Zenodo `10.5281/zenodo.13325358` (MIT) · FTQC

An architecture of **flag and proxy qubits** making hyperbolic surface and color qLDPC codes
implementable at degree-4 connectivity, plus a syndrome-extraction scheduler and two flag-aware
decoders.
**★ Characterization correction, verified in code.** This paper circulates in the Phase-1 map as
"QLDPC **decoding hardware**". It is not. Cross-validation against the first author's framework
(`github.com/suhaskvittal/qontra`, on which the artifact is built) found **zero HDL** — no `.v`,
`.sv`, `.vhd`, `.xdc` or `.tcl` anywhere — and decoders implemented purely in software
(`src/qontra/decoder/{mwpm,pymatching,restriction,mobius,concat_mwpm,chromobius,neural}.cpp`) over
modified Stim and PyMatching. The "hardware" is a **qubit connectivity architecture**: in
`include/protean/network.h` the qubit roles are an enum `{ data, xparity, zparity, flag, proxy }`
with `add_proxy` documented as *"The proxy qubit splits the edge between the two input qubits"*.
**It should be reclassified as architecture + scheduling, not decoding hardware**
(`DEEPDIVE_QEC_DECODING.md` §7).
**Numbers with context:** degree-4 FPNs of hyperbolic surface and hyperbolic color codes are
**2.9× and 5.5× more space-efficient** (physical qubits per logical qubit) than the **d = 5 planar
surface code**, at *comparable* logical error rates to their planar counterparts, with the advantage
growing with distance. Distances: hyperbolic surface d = 3–12, hyperbolic color d = 4–12, baselines
d = 5 and d = 7 planar. Circuit-level noise with 1q 0.1p, 2q p, measurement p plus T₁/T₂, at
p ∈ [5×10⁻⁴, 10⁻³]. **No decoder latency, throughput, LUT, area or power numbers — there is no
hardware decoder.**

**2 · Qoncord: A Multi-Device Job Scheduling Framework for Variational Quantum Algorithms** —
Meng Wang (UBC), Poulami Das (UT Austin), Prashant J. Nair (UBC) · `10.1109/MICRO61859.2024.00060`,
pp. 735–749, arXiv 2409.12432 · `Q_IN_HPC`, `HPC_FOR_Q` · **SOFTWARE_SIMULATION + ANALYTIC_MODEL** ·
Artifact **`PUBLIC_CODE`** `https://github.com/meng-ubc/Qoncord` (MIT) · NISQ

Splits VQA training into a noise-tolerant exploratory phase on cheap/busy low-fidelity QPUs and a
fine-tuning phase on high-fidelity QPUs, cutting queueing delay and wasted restarts.
**Code cross-validation** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §7, verdict `PARTIAL_MATCH`):
the two-phase design is confirmed exactly — exploration is `minimize(exp_fun_lf, ..., method='COBYLA',
tol=1e-1, rhobeg=1.0)`, fine-tuning is `minimize(exp_fun_hf, qoncord_intermediate['x'][i], ...,
rhobeg=0.1)` seeded from the exploration optimum. **Resource model:** `QuantumDevice(device_id,
fidelity)` with `current_job`, `time_remaining`, `is_idle()`, `advance_time()`, one **FIFO queue per
device**, discrete timestep 1, one job per device — i.e. **a QPU is modelled as a single-server FIFO
queue with a stochastic fidelity draw**. Devices are synthetic (`fidelities = linspace(0.3, 0.9, 10)`,
1,000 jobs). Seven policies in `policy.py`; `qoncord` hard-codes the low-fidelity subset `[6,7,8]`
for runtime jobs while `best_fidelity` uses the top three, matching the paper's framing.
**Modality confirmed:** `FakeKolkata`/`FakeToronto` plus an IonQ-Forte noise profile —
**no real QPU execution anywhere**.
**Numbers with context:** **17.4× faster** = wall-clock including queue delays for comparable-quality
solutions vs the single-device high-fidelity-only baseline; **13.3% better solutions** = approximation
ratio at an equal time budget vs the same baseline. Backends: kolkata 1.091% 2q / 1.22% readout;
toronto 2.083% / 4.48%; IonQ-Forte 0.74% / 0.5%. Benchmarks: 7-, 9-, 14-qubit QAOA max-cut on
Erdős–Rényi graphs at 1–3 layers, and 4-qubit UCCSD VQE for H₂.
**Why `PARTIAL_MATCH`:** no single script emits 17.4× — the queue simulator emits makespan/vacancy/
fidelity/throughput, the VQE/QAOA scripts emit `nfev` and approximation ratios, and the composition
script is not in the repo. Reproducible-in-principle per component, not end-to-end.
**Checklist gaps:** no DAG/task graph, no async primitive, no reservation or release/reacquisition,
no batching, no Slurm, no multi-QPU decomposition of a single circuit.

**3 · Surf-Deformer: Mitigating Dynamic Defects on Surface Code via Adaptive Deformation** —
Keyi Yin (UCSD), Xiang Fang (UCSB), Travis S. Humble (ORNL), Ang Li (PNNL), Yunong Shi (AWS),
Yufei Ding (UCSD) · `10.1109/MICRO61859.2024.00061`, pp. 750–764, arXiv 2405.06941 (v2/v3 retitled
*FlexiSCD*) · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** (Stim + PyMatching) ·
Artifact **`PUBLIC_ARTIFACT`** `https://zenodo.org/records/13751243` · FTQC · **not in the seed list**

Code-deformation framework built from primitive gauge-transformation instructions that adaptively
reshapes the surface-code lattice around transient defects, plus a layout keeping logical operations
executable during deformation.
*HPC problem:* compile-time/run-time **reconfiguration and resource allocation** — fault-tolerant
remapping and defect-aware floorplanning while maintaining lattice-surgery routing throughput.
**Numbers with context:** decoder PyMatching (MWPM); distances d = 19, 21, 23, 25, 27 chosen to meet
1% and 0.1% retry-risk targets; uniform circuit-level **p = 10⁻³**; defect model taken from cosmic-ray
experimental data — exponential arrival at **λ = 1/(26 × 10 s)**, ≈24 adjacent qubits affected, event
lasting ≈25,000 QEC cycles and raising local error rates to ≈50%. **35×–70× reduction in end-to-end
program failure rate vs ASC-S** under that defect model, and **≈50% of the qubit resources of Q3DE**
for the same failure-rate target. Benchmarks: Simon (400–900 qubits), Ripple-Carry Adder (225–729),
QFT (25–100 qubits, 20 layers), Grover (9–16).

### MICRO 2025 — 8 of 123 · Sessions **3C: Quantum-1** and **4C: Quantum-2** (Mon 20 Oct)

DOIs `10.1145/3725843.<suffix>`.

**1 · LANCER: Low-Overhead, Accurate, and Non-Destructive Calibration for Real-World Fault-Tolerant
Quantum Applications** — Junpyo Kim et al. (SNU, with SKKU) · `3756026`, pp. 547–563 · `HPC_FOR_Q`,
`FUTURE_WORKLOAD` · **ARCH_SIMULATION / ANALYTIC_MODEL `[inference]`** · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · FTQC · **not in the seed list**
Periodically stalls an FTQC program, **migrates live logical states into idle qubits**, recalibrates
the vacated qubits non-destructively, and hides the stall inside the idle time of fault-tolerant
gates. *HPC problem:* checkpoint/migration plus maintenance scheduling — live migration to spare
resources with the maintenance window hidden in existing pipeline bubbles, directly analogous to
online DRAM scrubbing or rolling VM maintenance. **95× larger programs (in gate count) executable
under drift, at 4.3% latency and 4.0% qubit overhead.** The evaluation platform is not named in any
reachable source, so the modality tag is inferred and flagged.

**2 · Distributed-HISQ: A Distributed Quantum Control Architecture** — Yilun Zhao (ICT CAS) et al.
with NUDT, Greatwall Quantum Lab, ECNU, Hefei National Laboratory/USTC · `3756048`, pp. 564–578,
arXiv 2509.04798 · `Q_IN_HPC`, `HPC_FOR_Q` · **REAL_HARDWARE + REAL_QPU** · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · NISQ

**The strongest evaluation in this entire census.** A hardware-agnostic quantum control ISA (HISQ)
plus **BISP**, a booking-based synchronization protocol, implemented on the commercial **DQCtrl**
distributed control system driving a superconducting chip with **66 qubits and 110 couplers**.
*Quantum problem:* control feedback loops have non-deterministic latency, and past one controller's
capacity multiple controllers must stay cycle-accurately synchronized or fidelity collapses.
*HPC problem, two distinct ones:* **distributed synchronization under non-deterministic latency** —
lock-step barriers waste cycles, demand-driven signalling stalls, and BISP is a reservation protocol
that can reach zero-cycle overhead; and **ISA design**, decoupling the instruction set from
quantum-operation semantics so one microarchitecture covers many control schemes.
**Numbers with context:** vs a lock-step scheme, **22.8% reduction in average program execution time**
and **≈5× reduction in infidelity**, on the 66-qubit DQCtrl system. Calibration on real qubits
measured T₁ = 9.9 µs at 4.62 GHz. FPGA resources: control board **4,155 LUTs, 75 BRAM, 6,392 FFs**;
readout board **2,435 LUTs, 45 BRAM, 3,192 FFs**. Stack: Quingo + an MLIR-based compiler.

**3 · Accurate Leakage Speculation for Quantum Error Correction** (system name **gladiator**) —
Chaithanya Naik Mude, Swamit S. Tannu (Wisconsin–Madison) · `3756053`, pp. 579–594, arXiv 2510.25661
· `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **RTL_SYNTHESIS + SOFTWARE_SIMULATION** · Artifact
**`PUBLIC_ARTIFACT`** Zenodo `10.5281/zenodo.16735148` · EARLY_FTQC/FTQC

A code-aware, calibrated error-propagation graph classifies each syndrome in nanoseconds and fires a
leakage-reduction circuit only when the pattern is provably leakage-dominated, replacing ERASER's
fixed heuristic.
*Quantum problem:* qubits leak out of the computational subspace; leakage corrupts all subsequent
syndrome measurements, spreads to neighbours, and is **invisible on data qubits** because they are
never measured during a QEC cycle. LRCs are themselves noisy and slow, so false positives inflate
both cycle time and logical error rate.
*HPC problem:* a hard-real-time **classification/speculation** problem in the QEC control loop —
accuracy vs misspeculation cost vs area, in MICRO's native vocabulary.
**QEC detail — the most complete in this census** (`DEEPDIVE_QEC_DECODING.md` §5, all verified
verbatim from the paper): applicable to surface, color and qLDPC (HGP, Balanced Product Cyclic)
codes; surface-code **d = 5, 7, 9, 11, 13, 17, 25**, 6.6.6 triangular color code d = 5, 19;
**p = 10⁻³ and 10⁻⁴** with leakage ratio **lr ∈ {0.01, 0.1, 1.0}**; **latency budget ≤ 100 ns**
("approximately the latency of four CNOTs on superconducting platforms"); **achieved classification
latency 1 ns**; **10 LUTs per data qubit**, and **only 70 LUTs to cover all 625 data qubits at
d = 25**; **17×–80× less resource than ERASER across d = 5→25**; eliminates up to 3× (avg 2×)
unnecessary LRCs; 1.7×–3.9× speedup; **16% logical-error-rate reduction**. Synthesis on a **Kintex
UltraScale+ xcku3p-ffvd900-3-e** — **synthesis only, explicitly not silicon and not a running
prototype in the loop with a QPU**; ERASER's design was re-synthesized for larger distances for a
fair comparison. Decoder-agnostic by design: it is a leakage *pre*-classifier, not paired with a
named decoder.
**Internal-consistency note worth carrying:** "10 LUTs per data qubit" and "70 LUTs for 625 data
qubits at d = 25" reconcile **only** via ~100× time-multiplexing (`10 × ⌈625/100⌉ = 70`), i.e. 10
LUTs serve 100 data qubits, each evaluated in 1 ns inside the 100 ns budget. A reader taking the
per-qubit figure literally would compute 6,250 LUTs.

**4 · YOUTIAO: Hybrid Multiplexing with Dynamic Qubit Grouping for Low-cost and Scalable Quantum
Wiring** — Wuwei Tian et al. (ZJU) · `3756061`, pp. 595–608 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
**REAL_HARDWARE (measured device data) + ANALYTIC_MODEL / ARCH_SIMULATION** · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · GENERAL
Frequency-division multiplexing for XY-control and readout lines, time-division for Z-control, with
qubit layout co-optimized against multiplexed channel allocation. *HPC problem:* an **I/O pin/wire-
count and routing problem** — the classic pin-limitation and routing-area problem of chip packaging,
with a channel-allocation component (TDM serialization must hide inside naturally non-parallel
operations or it lengthens circuit depth). **67.7% reduction in cryostat-level coaxial wiring
complexity**, 23% less on-chip routing area, 1q fidelity retained at 99.98%, only 5% extra circuit
latency vs a partial-multiplexing system. Experiments use data collected from self-developed Xmon
chips feeding a crosstalk and wiring-cost model — **not an end-to-end demonstration on a re-wired
cryostat**; treat the architecture as `PROJECTED` from measured device parameters `[inference]`.

**5 · Vegapunk: Accurate and Fast Decoding for Quantum LDPC Codes with Online Hierarchical Algorithm
and Sparse Accelerator** — Kaiwen Zhou et al. (ZJU, with SJTU) · `3756084`, pp. 719–732 ·
`HPC_FOR_Q`, `FUTURE_WORKLOAD` · **FPGA_PROTOTYPE** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` ·
EARLY_FTQC/FTQC
*(Full subtitle recovered here; the Phase-1 title string omitted it.)*
An offline SMT-based decoupling step maximizing check-matrix sparsity, an online greedy hierarchical
decoder, and a sparsity-exploiting FPGA accelerator.
*HPC problem:* **sparse linear algebra under a hard real-time deadline** — decoding is solving a
large sparse system; the offline SMT pass is a compiler/preprocessing stage restructuring the matrix
for sparsity and parallelism, and the hardware is a domain-specific sparse accelerator exploiting
exactly that structure.
**Numbers with context:** real-time target **< 1 µs**, met across 12 qLDPC code types on a
**Xilinx Alveo U50 at 250 MHz** in HLS C++. Bivariate-bicycle latencies: [[72,12,6]] **720 ns**,
[[90,8,10]] 732 ns, [[108,8,10]] 732 ns, [[144,12,12]] 732 ns, [[288,12,18]] 780 ns,
[[784,24,24]] **840 ns** (avg **756 ns**). Hypergraph-product: [[162,2,4]] **264 ns** through
[[882,48,8]] 526 ns (avg **412 ns**). **147.6× average vs BP+LSD** and **13.9× average vs BPGD**
over those 12 codes on that board; logical error rates **on par with BP+OSD**; accuracy-threshold
improvement 2.53× vs BP+LSD and 7.11× vs BPGD. LUT/area/power figures, absolute error rates and
syndrome bandwidth are **not stated** in any reachable source → `UNKNOWN`. Room-temperature FPGA;
no cryogenic claim. All claims remain `[paper]`-only — no artifact was found.

**6 · OneAdapt: Resource-Adaptive Compilation of Measurement-Based Quantum Computing for Photonic
Hardware** — Hezi Zhang et al. (UCSD, with PNNL/UW and ORNL) · `3756100`, pp. 733–748,
arXiv 2504.17116 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION / ANALYTIC_MODEL** ·
Artifact `NO_PUBLIC_ARTIFACT_FOUND` · EARLY_FTQC/FTQC · **not in the seed list**
⚠ **Three different titles in circulation.** Official program: *"Resource-adaptive Compilation of
Photonic One-way Quantum Computing"*; proceedings: as above; arXiv: *"OneAdapt: Adaptive Compilation
for Resource-Constrained Photonic One-Way Quantum Computing"*. **The proceedings title is
authoritative.**
*HPC problem:* compiler/IR design and scheduling under resource constraints — depth reduction,
**temporal-edge-length bounding** (a delay-line/buffer-depth pressure constraint directly analogous
to register allocation), and 2-D footprint reduction. **3.68× 1-D depth reduction vs the FlexLattice
IR compiler; 3.56× vs the cluster-state IR compiler**, or alternatively a large 2-D reduction
(8×8 → 3×3 for 64-qubit programs); **2.87×** when combined with QEC for photonic FTQC.

**7 · MUSS-TI: Multi-level Shuttle Scheduling for Large-Scale Entanglement Module Linked Trapped-Ion**
— Xian Wu, Chenghong Zhu, Xin Wang (HKUST-GZ), Jingbo Wang (BAQIS) · `3756129`, pp. 749–763,
arXiv 2509.25988 · `HPC_FOR_Q`, `Q_IN_HPC`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** (custom
Python 3.9 simulator on a single workstation) · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · NISQ/EARLY_FTQC
A compiler for photonically-interconnected multi-QCCD machines that **explicitly borrows multi-level
memory scheduling from classical architecture** — the authors state the approach is "inspired by
multi-level memory scheduling in classical computing," treating gate / storage / entanglement-module
zones as hierarchy levels with different access costs.
**Numbers with context:** shuttle-operation reductions of **41.74%** (30–32 qubits), **73.38% avg**
(117–128 qubits) and **59.82% avg** (256–299 qubits), with execution-time improvements 58.9% / 64.9%
/ 60.3%. Baselines: the Murali et al. (2020) QCCD simulator, Dai et al. (2024) shuttle-reduction
compilation, and the Munich Quantum Toolkit scalable-QCCD compiler. Benchmarks 30–299 qubits,
31–4,376 two-qubit gates.

**8 · Rasengan: A Transition Hamiltonian-based Approximation Algorithm for Solving Constrained Binary
Optimization Problems** — Qifan Jiang et al. (ZJU, with SJTU, PKU, ICT CAS) · `3756107`, pp. 764–777
· `Q_FOR_HPC`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** (DDSIM decision-diagram backend on CPU;
`qiskit-aer-gpu` used mainly to accelerate the HEA/QAOA *baselines*) · Artifact
**`PUBLIC_ARTIFACT`** `https://github.com/JanusQ/rasengan` (MIT) + Zenodo `16732034` · NISQ ·
**not in the seed list**
⚠ **This is MICRO 2025's "no quantum vocabulary in the title" paper** — nothing in the title says
quantum. It was found by hand-scanning every title in the volume and then confirmed via the official
program's Session 4C: Quantum-2 placement, not by any keyword.
Instead of shrinking the search space it *expands* it from one feasible solution via a transition
Hamiltonian, keeping evolution inside the feasible subspace, with three circuit-complexity reductions
(simplification/pruning, segmented execution, solution purification). Successor to the same group's
Choco-Q (HPCA 2025). Reproduction takes ≈40 h on dual AMD EPYC 9554 or ≈25 h with an H100.
**Exact quantitative results are `UNKNOWN`**: Semantic Scholar returned a paraphrase rather than the
verbatim abstract, ACM DL is 403, and no preprint exists. The qualitative claim (accuracy and
circuit-efficiency improvement over HEA and QAOA baselines across 20 benchmark problems × 100 cases)
is recorded; **the numbers are deliberately left blank rather than guessed.**

### MICRO 2026 — `PROGRAM_INCOMPLETE_AS_OF_2026-09-17`, no records.

## 3. Exclusions

| Paper | Year | Why excluded |
|---|---|---|
| **SuperCore: An Ultra-Fast Superconducting Processor for Cryogenic Applications** (SNU/Kyushu/Nagoya), `00112`, pp. 1532–1547, Session 11A | 2024 | **Classical, not quantum.** An in-order **CPU** in SFQ superconducting *digital* logic — pipeline-depth minimization, stall/flush and RAW-stall fixes, compared against **in-order CMOS processors running at 4 K** (11× over the SFQ baseline; 6× and up to 193× lower power vs 4 K CMOS). Quantum computing appears only as a downstream customer of cryogenic compute. **Prior flag confirmed.** |
| **SuperSFQ: A Hardware Design to Realize High-Frequency Superconducting Processors** (same group), `3756024`, pp. 995–1010, Session 5D "Superconducting Systems" | 2025 | **Classical, not quantum.** A clocking scheme plus synchronizer and architectural guidelines for general-purpose SFQ CPUs (up to 62.5× higher frequency, 34.4% JJ overhead). No qubits, no quantum state, no QEC. **Prior flag confirmed.** Note MICRO 2025 itself gives superconducting *classical* logic its own session, separate from Quantum-1/Quantum-2 — **the venue draws the same line this census does.** |
| **SOPHIE: A Scalable Recurrent Ising Machine Using Optically Addressed Phase Change Memory**, `00113`, pp. 1548–1561, same session as SuperCore | 2024 | Classical analog optimizer (2.5D optical + PCM). Baselines are photonic Ising machines and FPGAs, not QPUs. Quantum-inspired classical. |
| Polymorphic Error Correction (2024, Session 2C) | 2024 | Classical DRAM/memory ECC. `[inference]` from session placement. |
| DS-TIDE (2025) | 2025 | Classical dynamical-system solver. `[inference]` from title and placement. |
| Athena, Trinity/UFC, HAWK, Ironman, SmartPIR, ZKP and crypto-kernel papers | both | FHE / oblivious transfer / ZKP / classical cryptography. |
| PhD Forum Lightning Session, SRC presentations, Keynote I | 2024 | Non-archival / invited. |

**"No classical-simulation quantum papers at MICRO" — CONFIRMED for both 2024 and 2025.** No paper in
either volume is about classical simulation of quantum circuits. Stim, Qiskit, DDSIM and PyMatching
appear only as *evaluation tooling* inside papers whose contribution lies elsewhere. This is a real
structural difference from ASPLOS, ISCA and ICS, and it holds.

**No `STATUS_UNCLEAR` items** across the 236 enumerated 2024+2025 papers.

## 4. What MICRO rewards as a contribution

MICRO's quantum work sits **closest to the hardware** of the four architecture venues, and the
evidence supports that characterization strongly. Of the 11 relevant papers: one is a control **ISA
plus distributed synchronization protocol on real hardware driving a real 66-qubit chip**
(Distributed-HISQ); one is a **sparse FPGA decoder accelerator** (Vegapunk); one is a **hard-real-time
speculation classifier with LUT budgets** (gladiator); one is a **cryostat wiring and multiplexing**
paper (YOUTIAO); one is **multi-level zone scheduling** (MUSS-TI) and one is **adaptive code deformation and
resource reallocation around transient defects** (Surf-Deformer).

The vocabulary MICRO rewards is precision/recall of a predictor, misspeculation cost, per-qubit LUT
budget, nanosecond decision latency, pin count, routing area, wiring cost. Two of the eleven papers
report **FPGA resource numbers** (Distributed-HISQ and gladiator — Vegapunk's are `UNKNOWN`), and one
reports **measured real-QPU calibration data** — a far
higher hardware-evidence rate than any other venue in this census.

The counterpart is that MICRO publishes **no classical simulation work at all**, and its scheduling
papers (Qoncord, MUSS-TI) are framed as device-fleet or zone-hierarchy problems rather than as
HPC-centre resource management.

Relevant share 2.7% → 6.5% → unknown; absolute 3 → 8 → unknown. **MICRO-59 is the single largest
open item in this census** and should be re-checked once its program publishes (late Sept/Oct 2026),
including the status of its new Industry Track.

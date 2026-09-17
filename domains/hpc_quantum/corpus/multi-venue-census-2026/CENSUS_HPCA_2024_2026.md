# HPCA 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.

## 1. Population and denominators

| Year | TOC entries | Best-of-CAL (excluded) | Industry (archival) | Regular archival | Research track only | Method | Count status | Relevant | Share (research track) |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| HPCA 2024 (30th, Edinburgh) | 81 | 3 | 3 | **78** | **75** | `VOLUME_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | **1** | 1.3% |
| HPCA 2025 (31st, Las Vegas) | 121 | 3 | 5 | **118** | **113** | `VOLUME_ENUMERATED` + `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` | **7** | 6.2% |
| HPCA 2026 (32nd, Sydney) | ≥118 (mirror shows 116) | none found | not identified | **118 (best estimate)** | **118** | `PUBLISHER_TOC_ENUMERATED` + partial `PROGRAM_ENUMERATED` | **`TOTAL_COUNT_UNVERIFIED`** | **9** | ~7.6% |

**2024** — page ranges tile 1–1198; six entries returned per-article pagination instead of volume
pagination and those six unknowns exactly account for the six gaps. The official program independently
yields 33 + 33 + 15 = **81**, and 81 − 3 Best-of-CAL − 3 industry = **75** research-track papers.

**2025** — 116 mirror entries tile **1–1692 with zero gaps and zero overlaps**; the official program
yields 51 + 42 + 28 = **121**, and the five program entries after the last mirror entry are exactly
NearFetch (11B) plus the four 11C papers, so 116 + 5 = 121. The publisher print TOC (IEEE catalog
CFP25013-POD) independently confirms the volume's last paper ends at p. 1751.

**2026 — the one weak denominator in this census, reported honestly.** HPCA 2026 moved to the
researchr platform and its proceedings use **per-article pagination**, so the page-tiling proof is
*structurally impossible* for this year. The publisher-TOC mirror shows 116 entries, but the official
main-conference track contains **two papers absent from the mirror** — *Conduit* and
*Count2Multiply* — and Count2Multiply's existence in the proceedings is confirmed via IEEE Xplore
document 11408436. So the mirror is incomplete and the true count is **≥118**. Monday's program is
fully enumerated (13 sessions × 4 = 52, all present in the mirror); Tuesday and Wednesday truncate
under every fetch formulation attempted. **Neither missing paper is quantum-related**, so the
numerator is unaffected. No Best-of-CAL session and no single-page entry appears in the 2026 TOC —
the track appears dropped, but Tuesday/Wednesday are unverified.

**Venue scope** `[official-CFP]`: the weakest explicit quantum scope of the four architecture venues
despite the name — quantum is always bundled ("Quantum/Superconducting computing" 2024 →
"Quantum, Superconducting and Emerging technologies" 2025 → "Architectures using quantum,
superconducting, and emerging technologies" 2026).

## 2. ★ The Best-of-CAL determination

**Best of CAL is an invited re-presentation track of already-published IEEE Computer Architecture
Letters papers, not main-track regular papers.** Confirmed structurally: HPCA 2024 Session 5C and
HPCA 2025 Session 3B each contain three items occupying **exactly one page each** in the proceedings
(2024: pp. 613, 614, 615; 2025: pp. 321, 322, 323) — one-page abstracts, not full papers.

**The paper this affects:**

> **A Quantum Computer Trusted Execution Environment** — Trochatos, Xu, Deshpande, Lu, Ding, Szefer
> (Yale). HPCA 2024, **Session 5C "Best of CAL"**, **page 613 — a single page**,
> DOI `10.1109/HPCA57654.2024.00051`. **EXCLUDED.**
>
> It is topically squarely in scope — a QPU trusted-execution environment is `Q_IN_HPC` work on
> QPU-as-shared-resource — and it is precisely why a naive keyword census reports **2** quantum
> papers for HPCA 2024 instead of **1**. But it is an invited one-page re-presentation of a paper
> originally published in IEEE Computer Architecture Letters. **The prior warning is confirmed
> exactly: HPCA 2024's quantum count is 1, not 2.**

**Industry track:** for 2024 and 2025 the industry papers occupy full multi-page ranges (2024:
970–1011; 2025: 1201–1274) and are bibliographically indistinguishable from research papers, so they
are counted in the regular denominator with the research-track-only figure reported alongside. None
is quantum-related.

## 3. Relevant papers

### HPCA 2024 — 1 of 78 archival (75 research-track) · **no dedicated quantum session existed**

**MIRAGE: Quantum Circuit Decomposition and Routing Collaborative Design Using Mirror Gates** —
Evan McKinney, Michael Hatridge, Alex K. Jones (Pittsburgh) · `10.1109/HPCA57654.2024.00060`,
pp. 704–718, **Session 6B "Emerging Technology"**, arXiv 2308.03874 · `HPC_FOR_Q` ·
**ANALYTIC_MODEL / ARCH_SIMULATION** (monodromy polytopes + Haar Monte-Carlo; no QPU) ·
Artifact **`PUBLIC_CODE`** `https://github.com/Pitt-JonesLab/mirror-gates` · NISQ

Co-designs two-qubit-gate decomposition with SWAP routing by exploiting **mirror gates** — the same
physical iSWAP-family interaction with reversed outputs — to cut true circuit depth rather than SWAP
count alone.
**Numbers with context:** **29.58% average / 32.09% weighted-average depth reduction** and
**59.86% SWAP reduction** on a **6×6 square lattice** vs **Qiskit SABRE**, over 15 QASMBench/MQTBench
circuits at 11–30 qubits and 18–720 two-qubit gates; on 57-qubit Heavy-Hex, 16.97% average 2-qubit
gate reduction; total gate count essentially unchanged (+0.4%); approximate decomposition cuts
infidelity ~9%.
**Classical compile cost** is reported but framed as *no regression*: a 64-qubit QFT transpiles
**47.9% faster** than Qiskit. Code cross-validated (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §11,
verdict `CONSISTENT`): `Mirage(LegacySabreSwap)`, `ParallelMirage`, the CNS substitution entry point
`_get_node_cns`, `MonodromyDepth` as cost function, and a `deprecated/` tree preserving earlier CNS
variants — genuine research lineage.

### HPCA 2025 — 7 of 118 archival (113 research-track) · Sessions 2A "Quantum Slots – 1" and 3A "Quantum Slots – 2"

All seven sit in the two dedicated sessions; a whole-TOC hand-scan found no quantum paper outside
them. DOIs `10.1109/HPCA61900.2025.<suffix>`.

1. **ZAC — Reuse-Aware Compilation for Zoned Quantum Architectures Based on Neutral Atoms**
(Wan-Hsuan Lin, Daniel Bochen Tan, Jason Cong, UCLA) · `00021`, pp. 127–142, arXiv 2411.11784 ·
`HPC_FOR_Q` · **ANALYTIC_MODEL** (fidelity computed from a stated model, not measured) ·
Artifact **`PUBLIC_CODE`** — note the repo is **`https://github.com/UCLA-VAST/ZAC`** (an earlier
note citing `UCLAVAST/ZAC` 404s) · NISQ
*HPC problem:* data placement + instruction scheduling + reuse — essentially scratchpad allocation
with movement cost, delivered with an architecture specification and an IR (**ZAIR**) so one compiler
retargets different zone layouts.
**Numbers with context — correcting a looser earlier statement:** the paper's 22× figure is
**fidelity vs Enola**, with **13,350× vs Atomique**, on QASMBench circuits of 14–98 qubits and
41–630 gates; optimality gaps are 3% (movement), 7% (placement), 10% (reuse). Classical cost is a
tunable knob: disabling the initial-mapping optimization solves every instance in **<1 s**, giving
63× speedup and 3.6× better fidelity vs NALAC; intermediate placement is **O(g·n³)**.
2. **HATT: Hamiltonian Adaptive Ternary Tree for Optimizing Fermion-to-Qubit Mapping**
(Penn/LBNL/AWS) · `00022`, pp. 143–157, arXiv 2409.02010 · `HPC_FOR_Q`, `Q_FOR_HPC`,
`FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION + REAL_QPU** (IonQ) · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · NISQ. Builds the fermion-to-qubit encoding from the target Hamiltonian;
**5–25% reduction in Pauli weight, gate count and depth**, and the systems contribution is reducing
the construction algorithm from **O(N⁴) to O(N³)**. *Title note:* the proceedings say "Hamiltonian
**Adaptive** Ternary Tree" while the official program prints "Hamiltonian **Aware**" — a real
program↔proceedings discrepancy.
3. **QuCLEAR: Clifford Extraction and Absorption for Quantum Circuit Optimization** (Argonne/
UChicago) · `00023`, pp. 158–172, arXiv 2408.13316 · `HPC_FOR_Q`, `Q_FOR_HPC` ·
**SOFTWARE_SIMULATION** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · NISQ.
*HPC problem:* an explicit **quantum/classical work-partitioning** decision — Clifford circuits are
classically simulable (Gottesman–Knill), so the compiler offloads that portion to the classical host
and shrinks the quantum instruction stream. Up to **77.7% CNOT reduction** and **84.1% entangling-
depth reduction** vs state-of-the-art optimization on quantum-simulation benchmarks.
4. **Interleaved Logical Qubits in Atom Arrays** (UChicago/UT Austin) · `00030`, pp. 261–274 ·
`Q_IN_HPC`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · FTQC.
Argues atom *movement* imposes an unavoidable speed limit on neutral-atom FTQC and proposes a
movement-free architecture of interleaved surface-code patches with transversal CNOTs plus
"interleaved lattice surgery" routing channels. **~3× compute-time reduction in high-parallelism
regimes**, and the interleaving advantage survives a **1–3× increase in two-qubit gate error rates**.
5. **Choco-Q: Commute Hamiltonian-based QAOA for Constrained Binary Optimization** (ZJU) · `00031`,
pp. 275–289, arXiv 2503.23941 · `Q_FOR_HPC`, `HPC_FOR_Q` · **SOFTWARE_SIMULATION** ·
Artifact **`PUBLIC_ARTIFACT`** `https://github.com/JanusQ/Choco-Q` + Zenodo 14250942 · NISQ.
**>235× algorithmic improvement in finding the optimum** and **4.69× end-to-end acceleration** vs
prior QAOA designs; the three optimizations are linear-time classical compiler passes.
6. **BOSS: Blocking algorithm for optimizing shuttling scheduling in Ion Trap** (HKUST-GZ
`[inference]`) · `00032`, pp. 290–303, arXiv 2412.03443 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` ·
**SOFTWARE_SIMULATION / ANALYTIC_MODEL** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · NISQ.
Group gates into blocks so each ion configuration serves many gates before rearrangement — directly
analogous to tiling/blocking for data-movement minimization. **Max 96.1% reduction in shuttles** on
applications with up to 4,000+ two-qubit gates at 64–78 qubits.
7. **LSQCA: Resource-Efficient Load/Store Architecture for Limited-Scale FTQC** (U. Tokyo/NTT/RIKEN/
Kyushu) · `00033`, pp. 304–320, arXiv 2412.20486 · `Q_IN_HPC`, `FUTURE_WORKLOAD` ·
**ARCH_SIMULATION / ANALYTIC_MODEL** · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · EARLY_FTQC.
**The most architecture-native quantum paper in this census.** Imports the load/store and
memory-hierarchy abstraction into FTQC floorplanning: small **Computational Registers** plus dense
**Scan-Access Memory**, trading unit-time random access for variable-latency access. *Quantum
problem:* state-of-the-art lattice-surgery floorplans spend **50% of patch area** on routing space so
any logical qubit is reachable in unit time. *Result with context:* in a resource-restricted setting
a benchmark reaches **~90% memory density at a 5% execution-time increase**, versus a conventional
floorplan capped at 50% density. It also performs **static analysis of quantum programs** to find
access locality in memory-reference timestamps — exactly as a classical compiler would.

### HPCA 2026 — 9 of ~118 (`TOTAL_COUNT_UNVERIFIED`, ≥118) · Sessions "Quantum Computing Architecture" (4) and "Quantum Compilation and Simulation" (4), **plus one outside both**

DOIs `10.1109/HPCA68181.2026.<suffix>`.

1. **Fully Parallelized BP Decoding for Quantum LDPC Codes Can Outperform BP-OSD** (NC State/PNNL) ·
`11408621`, arXiv 2507.00254 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** ·
Artifact **`PUBLIC_CODE`** `https://github.com/Dies-Irae/BP-SF` · FTQC.
**The clearest "sequential bottleneck → parallel work" argument in the entire corpus.** BP alone
fails on qLDPC codes because of degeneracy and short cycles; the standard fix, BP-OSD, restores
accuracy via ordered-statistics post-processing built on **Gaussian elimination — inherently
sequential and cubic**, which is the parallelization barrier of the real-time decoding loop. BP-SF
replaces it with speculative **syndrome flipping**: monitor bit-level oscillation during BP, generate
candidate flip vectors, decode each modified syndrome **independently** with short-depth BP.
**Code cross-validation** (`DEEPDIVE_QEC_DECODING.md` §3, verdict `CONSISTENT`): each worker builds
its own `BpDecoder` and there is **no cross-candidate data dependency** — the only inter-worker
communication is chunk distribution plus a `solution_found_event` early-abort flag. **Parallel degree
is bounded**: with the shipped `[[144,12,12]]` settings (`topk=50, w_min=1, w_max=10, n_sample=10`)
there are **at most 100 candidates**. Latency is **wall-clock CPU**, measured per sample.
**Numbers with context:** on **[[144,12,12]]** BB code, average latency **~70% of BP-OSD** at one
process; parallelizing post-processing across 8 processes cuts average latency a further **55%** and
maximum latency to as low as **18%** of the single-process implementation. LER comparable to or
better than BP-OSD. Two caveats found in code: the GPU path (`gpu_est.py`) iterates candidates
**sequentially** despite using a batch-capable decoder, and parallel vs serial modes are **not
semantically identical** (serial returns the lowest-weight converging candidate, parallel returns
whichever converges first in wall-clock), which the repo does not control for.
2. **Pinball: A Cryogenic Predecoder for Surface Code Decoding Under Circuit-Level Noise**
(Michigan) · `11408464`, arXiv 2512.09807 · `HPC_FOR_Q`, `Q_IN_HPC` · **RTL_SYNTHESIS**
(22 nm FDSOI with cryo-recharacterized standard cells, synthesis + place-and-route — **not fabricated
silicon**) **+ SOFTWARE_SIMULATION** · Artifact **`PUBLIC_CODE`** `https://github.com/aknapen/Pinball`
· FTQC. *(Title note: the paper says "Surface Code Decoding", not "QEC Decoding".)*
Filters common surface-code errors inside the 4 K stage, modelling **circuit-level** noise and error
propagation rather than the phenomenological noise prior predecoders assumed.
**Code cross-validation** (`DEEPDIVE_QEC_DECODING.md` §2, verdict `PARTIAL_MATCH`): the **nine
sequential pipeline stages are confirmed in RTL**, comment-delimited — measurement (time-like), four
bulk data-error stages, two spacetime stages, a **hook**-error stage, and edge data errors; **O(d²)
scaling confirmed structurally** (`NUM_ROWS = d+1`, `NUM_COLS = (d−1)/2` → `(d²−1)/2` ancillas, one
stabilizer basis); the Python model executes the same error classes in the same order. **But the
entire hardware-claims half is absent from the repo** — no power model, no area model, no bandwidth
accounting, no Promatch baseline — so 0.56 mW, 22.2×, 67.4×, 3780.72×, 32.58× and the 2,668-logical-
qubit figure are **not reproducible-in-principle from this artifact**.
**Measurement context, correcting two headline numbers that circulate without qualifiers:**
**3780.72× syndrome-bandwidth reduction is at d = 5, p = 10⁻⁴** vs no predecoding — *not* at d = 21
and *not* at p = 10⁻³. **32.58× lower logical error rate than Promatch is at d = 11, p = 5×10⁻⁴**
(with a companion 5× against Promatch‖Astrea-G). The ~6-orders-of-magnitude figure is vs **Clique**,
the prior state-of-the-art *cryogenic* predecoder. Noise is **SI1000**, not uniform depolarizing,
which matters for any cross-paper comparison. Distances 3–21 odd, p swept 10⁻⁴–10⁻².
Peak power **< 0.56 mW**; under a **1.5 W 4 K budget, up to 2,668 logical qubits at d = 21**.
*(A possible internal inconsistency: the abstract says 32.58× where one body sentence read 32.38×.
The abstract value is recorded as authoritative; `INSUFFICIENT_EVIDENCE` on which is correct.)*
3. **Cyclone: Efficient and Highly Parallel QCCD Architectural Codesigns for Fault-Tolerant Quantum
Memory** (Duke/UT Austin) · `11408498`, arXiv 2511.15910 · `Q_IN_HPC`, `HPC_FOR_Q`,
`FUTURE_WORKLOAD` · **ARCH_SIMULATION** (QCCDSim) + SOFTWARE_SIMULATION · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · FTQC.
Replaces the 2-D grid QCCD layout with a **ring in which ancilla qubits move in lockstep**, removing
trap-to-trap roadblocks that serialize the naturally parallel syndrome extraction of high-rate qLDPC
codes. Codes: hypergraph product **[[225,9,6]]**, **[[625,25,8]]**, bivariate bicycle
**[[144,12,12]]**; p swept **10⁻⁴–10⁻³**. Up to **2 orders of magnitude** LER improvement for HGP and
**3 orders** for BB vs the grid codesign; **4× execution speedup**, 2× fewer traps and ancillas,
**~20× overall spacetime improvement**. Reports classical control scaling too: **DAC count stays
constant** in the ring versus linear in trap count for grids.
4. **TraceQ: Trace-Based Reconstruction of Quantum Circuit Dataflow in Surface-Code FTQC**
(Yale/UChicago/Cornell/Northwestern) · `11408545`, arXiv 2508.14533 · `Q_IN_HPC`, `HPC_FOR_Q` ·
**SOFTWARE_SIMULATION** (600 randomized synthetic FT circuits, 28 subroutine circuits, three
layouts) · Artifact **`PARTIAL`** (code promised in the preprint, no URL) · FTQC.
Defines lattice-surgery patch activity as an **access trace** and reconstructs the logical circuit's
dataflow from it — memory-access-trace analysis transplanted wholesale, framed as a side channel,
with profiling/telemetry of FTQC execution as the constructive use.
5. **DC-MBQC: A Distributed Compilation Framework for Measurement-Based Quantum Computing**
(**Peking University + CUHK** — *correcting a prior attribution to ICT CAS*) · `11408612`,
arXiv 2601.00214 · `Q_IN_HPC`, `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **ARCH_SIMULATION / ANALYTIC_MODEL**
· Artifact **`PUBLIC_CODE`** `https://github.com/qfcwj/DC-MBQC` · NISQ/GENERAL.
**The corpus's clearest distributed-compilation paper.** Code cross-validated
(`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §13, verdict `CONSISTENT` — the tightest paper↔code
agreement in the whole set): `adaptive_partition(..., window_size=3, delta_threshold=0.01, ...)`
calls METIS in a loop, scoring partitions by NetworkX modularity and adjusting the imbalance
parameter ×1.02 / ÷1.02 against a sliding-window modularity delta, with a ×1.1 kick when a subgraph
disconnects; `delta_threshold=0.01` matches the paper's ε_Q = 0.01 exactly, and the BDIR annealer's
`max_steps=20, initial_temp=10.0, cooling_rate=0.95` matches I_max = 20, T₀ = 10, α = 0.95 exactly.
**One discrepancy:** the code's `ubvec_max=1.2` vs the paper's stated α_max = 1.5. Layer scheduling
is proved NP-hard by reduction from graph bandwidth. Cut edges become `Connector` objects restored by
inter-layer fusion with ancillary photons under a classical heralding signal, concurrency capped at
K_max = 4. *(Portability note: `third_party/metis.dll` — the repo states experiments were verified on
Windows only.)*
**Numbers with context:** **7.46× photon-lifetime improvement** = 81-qubit QFT, **8 fully-connected
QPUs**, 4-star resource states, vs OneQ (993 → 133 cycles); **6.82× execution-time speedup** =
144-qubit VQE, same configuration, vs OneQ (1,016 → 149 cycles); vs OneAdapt at 8 QPUs, 5.74×
execution and 4.33× lifetime. Only 4- and 8-QPU configurations are evaluated. Classical compile cost
is reported: ~4–5 s vs OneQ's ~8 s for 100-qubit QFT. **No gate count, depth or end-to-end fidelity
is reported.**
6. **Toward Scalable Gate-Level Parallelism on Trapped-Ion Processors with Racetrack Electrodes**
(Yonsei/Rutgers) · `11408608` · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **ARCH_SIMULATION** (in-house
runtime emulator modelled on Quantinuum H2-1) · Artifact `NO_PUBLIC_ARTIFACT_FOUND` · NISQ.
Shows that **adding zones to a racetrack trapped-ion processor can *hurt* runtime** under existing
scheduling, because track length raises ion-circulation overhead faster than zones raise parallelism
— a scaling-anomaly result with a scheduling/topology fix (near-gate prioritization, shortcut paths,
unitary decomposition for zone utilization). ⚠ **Evidence caveat:** no preprint exists under the
HPCA title; the numbers here come from arXiv 2601.08930 **"Plutarch"**, which has an identical
six-author list in identical order and an identical subject — treated as the same work `[inference]`,
high confidence but not certain. Under that source, vs the **Rolodex** baseline: 71% runtime
reduction on 32-qubit VQE; QAOA training 41.38 h → 14.07 h; 19.73% lower infidelity; 32% runtime
reduction on Steane-code fault-tolerant workloads; 48.99% lower shuttling cost from a non-uniform
layout.
7. **D'ArQ: A QOC Framework with Causality-Aware Grouping and Basis Selection** (Yonsei
`[inference]`) · `11408534` · `HPC_FOR_Q` · **SOFTWARE_SIMULATION / ANALYTIC_MODEL** · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · NISQ. Two classical-compiler contributions: a **correctness** fix
(greedy gate grouping can violate dependency order; the fix is DAG-based grouping with per-group
mergeability) and a **compile-time** fix (a pre-computed pulse library plus cost-model-driven
analytic-basis selection — memoization plus cost-based pass selection). Built on GOAT rather than
GRAPE. Vs PAQOC: up to **22.8% lower circuit latency** and **56.8% lower compilation time**.
8. **CLINE: Improving Control Flow Compilation of Quantum Programs with Control Line Encoding**
(SJTU/ZJU) · `11408609` · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION** · Artifact
`UNKNOWN` · EARLY_FTQC/FTQC. Merges *non-adjacent* multi-controlled gates by flipping control-line
polarity. Oracle circuits implementing control flow can be **up to 99% of total gate count**; cutting
**T count** directly cuts magic-state distillation demand. Average **54.7% CX** and **56.8% T** cost
reduction.
9. **Advancing Full-Stack Acceleration for Schrödinger-Style Quantum Simulation** (Imperial College
London) · `11408466` · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **modality unresolved — see below** ·
Artifact `NO_PUBLIC_ARTIFACT_FOUND` · EARLY_FTQC/GENERAL · **NOT IN THE SEED LIST, and outside both
dedicated quantum sessions** (it sits in a Tuesday/Wednesday session that could not be enumerated).
Algorithm/software/hardware co-design for statevector simulation at the ~30-logical-qubit validation
regime: **index redirection** and **pre-compute merging** to cut data movement and complexity, a
**reconfigurable dataflow architecture** with adaptive memory scheduling and swapping, and a
toolchain exploring both. **Maximum speedup exceeding 50× over a GPU-based Qiskit baseline.**
**Modality is `INSUFFICIENT_EVIDENCE` between FPGA_PROTOTYPE and RTL_SYNTHESIS**: no board name, no
LUT/DSP/BRAM figures and no synthesis report could be obtained. The same six authors' companion
toolchain paper **CAST** (arXiv 2503.19894) is explicitly **CPU/GPU-only** (LLVM IR vectorization
plus a PTX code generator), so the HPCA paper's hardware layer is a new contribution relative to it;
"reconfigurable" plus the group's identity leans FPGA `[inference]`, but that is not asserted.
This paper was found only by hand-scanning the full TOC — **it is the 9th paper the seed count
missed.**

## 4. Exclusions

Classical superconducting logic was specifically scanned for across all three years: **no HPCA
2024/2025/2026 main-track paper is an SFQ/RSFQ/AQFP paper.** The closest brush is **Pinball**, which
*discusses* SFQ only to criticize prior cryogenic predecoders for using it and to propose cryogenic
CMOS instead — a paper a keyword census could mishandle in either direction.

Excluded false positives: **SACHI** (2024, an all-digital near-memory Ising architecture, in the
*same session* as MIRAGE), **Efficient Optimization with Encoded Ising Models** (2025), **PROCA**
(2025, probabilistic/stochastic computing), a **PN-Free Digital 3-SAT Accelerator** (2026) — all
quantum-inspired classical; **Morphling** (2024), five FHE papers plus LegoZK (2025), **HERO-Sign**
(SPHINCS+), an **NTT accelerator**, UniFHE, CROPHE, Peregrine, zkPHIRE, IVE, Conflux (2026) — all
post-quantum/FHE/ZKP cryptography; REASON, RPU, ESTroM, CogSys — classical AI accelerators.

**A pure name-collision false positive worth recording:** **QuCo** (HPCA 2026) — *"Efficient and
Flexible Hardware-Driven Automatic Configuration of Tile Transfers in GPUs"* — begins with "Qu" and
trips every quantum keyword filter while containing **zero quantum content**. Caught only by reading
every title.

## 5. What HPCA rewards as a contribution

HPCA is the **latest bloomer** of the four architecture venues and the one whose quantum track is
most visibly *constructed*: 1 paper and no session in 2024, then two dedicated sessions in each of
2025 and 2026. Prior work's warning holds — **HPCA 2024 must not be cited as evidence of an
established quantum track.**

What gets in is architecture-native framing: a memory hierarchy (LSQCA, EZCache's HPCA analogue),
a load/store ISA, a cache-like reuse argument (ZAC), a topology/parallelism scaling anomaly
(racetrack), an access-trace side channel (TraceQ), a power- and bandwidth-constrained accelerator
under a thermal cap (Pinball), and a sequential-to-parallel algorithm restructuring with a latency
consequence (BP-SF). 2026 is where HPCA becomes genuinely useful to this project: **two of the
corpus's most transferable public artifacts (BP-SF, Pinball) and its clearest distributed-compilation
paper (DC-MBQC) are all HPCA 2026.**

Relevant share 1.3% → 6.2% → ~7.6%; absolute 1 → 7 → 9.

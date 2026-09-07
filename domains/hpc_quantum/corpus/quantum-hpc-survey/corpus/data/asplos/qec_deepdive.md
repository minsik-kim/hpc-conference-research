I have gathered the material. Writing up the census now.

---

# ASPLOS 2024–2026 QEC Decoding & Architecture Census — Deep Technical Analysis

## Sourcing note (read first)

ACM DL is blocked from this environment (403 on both `/doi/` and `/doi/pdf/`); `curl` egress is blocked entirely (proxy `connect_rejected`). **Every full-text fact below comes from the arXiv HTML preprint**, tagged `[paper-preprint]` to distinguish it from the published ASPLOS version, which I could not read. Metadata-only sources are tagged `[abstract]`. Repository observations are `[code]`.

Volume mapping cross-checked against your `VOLUME_STRUCTURE.md`: Promatch = 3620666 (ASPLOS'24 V3); Micro Blossom / RESCQ / HetEC = 3676641 (ASPLOS'25 V2); QECC-Synth = 3669940 (ASPLOS'25 V1); Chiplet codesign = 3620665 (ASPLOS'24 V2); the five 2026 papers = 3779212 (ASPLOS'26 V2). None fall in the fall-cycle volumes (3622781, 3676642), so proceedings year = presentation year for all eleven.

**Two author-list corrections to your brief** (both verified):
- **AlphaSyndrome** is *not* Yuwei Jin et al. It is Yuhao Liu, Ethan Decker, Kean Chen, Shuohao Ping, Junyu Zhou, Gushu Li (Penn); Justin Kalloor, Mathias Weiden (UC Berkeley); Yunong Shi (AWS/Michigan); Ali Javadi-Abhari (IBM Research); Costin Iancu (LBNL). `[paper-preprint]`
- **"Accelerating Computation in Quantum LDPC Code"** is Jungmin Cho, Hyeonseong Jeong, Junpyo Kim, Junhyuk Choi, Juwon Hong, Jangwoo Kim (SNU HPCS Lab) — not "Jaewoong Cho / Hanseul Jeong". The system is named **ACQC**. `[abstract]` (Semantic Scholar + INSPIRE + lab page)
- **iSwitch**'s preprint (arXiv 2504.16303) is titled **"Flexion"** and carries one extra author (Ang Li, PNNL) not on the ACM author list. `[paper-preprint]` vs `[abstract]`

---

# PART A — PER-PAPER ANALYSIS

---

## 1. Promatch (ASPLOS 2024, DOI 10.1145/3620666.3651339)

Alavisamani, Vittal, Ayanzadeh, Das, Qureshi — Georgia Tech / UT Austin.
Source: arXiv **2404.03136v1** (4 Apr 2024), full HTML. `[paper-preprint]`

### Workload structure

| Quantity | Value | Source |
|---|---|---|
| Syndrome generation rate | one round per **~1 µs**, superconducting | `[paper-preprint]` |
| Code distances | **d = 11, 13** (baseline RT-MWPM ceiling was d=9) | `[paper-preprint]` |
| Logical qubits | **1** (single-patch memory experiment) | `[inference]` from evaluation setup |
| Decoding window | one syndrome round at a time; no sliding/overlapping window scheme discussed | `[paper-preprint]` |
| Streaming vs batch | **Streaming**, per-round, with memory prefetch overlap | `[paper-preprint]` |
| Latency budget | **960 ns** total (240 cycles @ 250 MHz), 10 cycles reserved for Astrea-G comparison | `[paper-preprint]` |
| Throughput | 10⁶ syndromes/s implied; **no off-fridge bandwidth number given** | `NOT_FOUND` |

Verbatim, the constraint:

> "To prevent a backlog of errors, error decoding must be performed in real-time (i.e., within 1µs on superconducting machines)."

> "quantum fault-tolerance will likely require a worst case latency of 1µs to avoid unnecessarily stalling the quantum computer."

Note the word **"worst case"** — Promatch commits to a hard deadline, and every latency it reports is a max as well as an average. This is load-bearing for the cross-paper comparison.

### Computational structure

- **Algorithm class**: greedy, locality-aware **predecoder** feeding a brute-force exact **MWPM** main decoder (Astrea). Not itself a matching algorithm — a *syndrome-modifying filter* that reduces Hamming weight (HW) of the syndrome until the main decoder's combinatorial capacity is reached.
- The capacity wall it exists to work around: Astrea decodes syndromes with **HW ≤ 10** exactly; "the number of possible matchings for syndromes of Hamming weight 10 is 945", and "the exponential growth of number of matchings when HW increases … makes applying brute-force method impossible for d > 7". `[paper-preprint]`
- **Four-step pipeline**, ordered by risk: (1) isolated pairs; (2) neighbouring flipped bits that do not create singletons (degree-1 preferred, then lowest weight); (3) match existing singletons via shortest path / highest-probability error chain; (4) as step 2 but permitting singleton creation. `[paper-preprint]`
- **Adaptive coverage** — the mechanism that makes this an architecture paper rather than an algorithms paper: "After each matching that Promatch applies, it checks if the main decoder can decode the modified syndrome in the remaining time. If yes, it gives the syndrome to the main decoder. If not, Promatch predecodes more bits." Target output HW is **6, 8 or 10**. `[paper-preprint]`
- **Parallelism**: (a) *within step 1*, "all these candidates can be applied to the syndrome simultaneously"; steps 2–4 are strictly serial, one pair at a time; (b) a **4-stage pipeline** for candidate identification (degree check → singleton check → candidate-register placement → weight compare); (c) **module-level concurrency** — Promatch and Astrea-G run as two independent decoders whose outputs are compared in the final 10 cycles.
- **Working set** `[paper-preprint]`: edge table **3.6 KB** (d=11) / **6 KB** (d=13); path table **129 KB** (d=11) / **345 KB** (d=13), with paths bucketed "into four groups as Promatch is not sensitive to the exact weight". Plus per-vertex degree and dependency arrays. Path table growth 129→345 KB for d 11→13 is the memory scaling signal (roughly d⁴-ish in this range).
- **Synchronization**: sequential dependence between steps 2–4 is the fundamental limiter — each match mutates the syndrome, so the next candidate evaluation depends on the previous.

### Architecture rationale — why not a CPU

> "the worst-case latencies are still a few hundred microseconds to milliseconds" (software MWPM)

> "To achieve the required decoding speed, the decoding algorithms need to be implementable on hardware, such as FPGA"

The gap is ~2–3 orders of magnitude against a hard 1 µs. The paper does **not** discuss syndrome bandwidth off the fridge, nor cryogenic placement of the decoder. `NOT_FOUND` for both.

### Scaling analysis, T(P) = W/P + C(P)

- **W**: work is proportional to edges traversed in the decoding subgraph, summed over predecoding rounds. It scales with syndrome HW, which grows roughly with the number of detectors ~ d³ times p. The path table grows superlinearly (129 KB → 345 KB for d 11→13).
- **P**: parallelism is *small and bounded*. Only step 1 is data-parallel; the pipeline is 4 stages deep. Promatch does not parallelize over the graph. Its scaling strategy is orthogonal — **reduce W to fit the main decoder's fixed capacity**, not increase P.
- **C(P)**: essentially zero, because P is essentially one. That is exactly why Promatch fits in 3% of a Kintex LUT budget. The cost of this design point is that it cannot go faster by adding hardware; it can only go further in d by predecoding more aggressively, which trades accuracy.

### Hardware evidence level — the critical distinction

`RTL_SYNTHESIS` + `ANALYTIC_MODEL` (latency) + `SOFTWARE_SIMULATION` (accuracy). **Not** `FPGA_PROTOTYPE`.

- Synthesis: "We synthesize Promatch on a Kintex UltraScale+ FPGA." Table 7 reports **3% LUT, 1% FF, 250 MHz** — *utilization and achievable frequency only*.
- The nanosecond figures are **derived**, not measured: "we estimated the number of consumed cycles for each syndrome by summing the edge numbers in the decoding subgraphs across all predecoding rounds prior to sending the syndrome to the main decoder", then multiplied by the 4 ns period implied by 250 MHz. `[paper-preprint]`
- **This must not be reported as a measured latency.** There is no board execution, no post-implementation timing trace, and no syndrome stream driven through real logic.
- LER numbers come from **Stim** with rare-event sampling.

### Quantitative results, with context

All at **p = 10⁻⁴, uniform circuit-level noise, Stim**, d=13 (`[paper-preprint]`):

| Decoder | LER | × vs MWPM |
|---|---|---|
| MWPM (ideal, software) | 3.4 × 10⁻¹⁵ | 1× |
| **Promatch ‖ Astrea-G** | **3.4 × 10⁻¹⁵** | **1×** |
| Promatch + Astrea | 2.6 × 10⁻¹⁴ | 7.7× |
| Astrea-G alone | 1.4 × 10⁻¹³ | 43× |
| Smith et al. ‖ Astrea-G | 1.5 × 10⁻¹⁴ | 4.5× |
| Smith et al. + Astrea | 6.9 × 10⁻¹¹ | 20,412× |

At d=11, Clique + Astrea gives 2.2 × 10⁻⁵ (**10⁸×** worse) — the predecoder-coverage failure mode.

Swept over p = 10⁻⁴ → 5×10⁻⁴: "Promatch maintains an LER within 5.9× to 202× of MWPM's LER for d=11 and 13"; "Promatch ‖ AG remains in 1.1× and 13.9× of MWPM's LER for distance 11 and 13". **The 13.9× is the worst point of the sweep, at p = 5×10⁻⁴ — remember this number; Micro Blossom re-uses it at a different p.**

Latency, all cycle-count-derived:

| | d=11 | d=13 |
|---|---|---|
| Predecode only, max (Table 4) | 824 ns | **928 ns** |
| Predecode only, avg | 68.2 ns | 70.0 ns |
| Predecode + main decoder, max (Table 5) | 904 ns | **960 ns** |
| Predecode + main decoder, avg | 524.2 ns | 526.0 ns |

The 960 ns max is not an outcome but a **cap** — the adaptive controller stops predecoding when the residual budget will not cover the main decoder. The avg/max ratio (526 vs 960) shows the design is provisioned for the tail, consistent with its hard-deadline framing.

Coverage: "99.56% and 99.83% of samples require only Step 1 of the algorithm" (d=11, d=13). The expensive steps 2–4 are tail events.

Comparison hygiene: same distance ✓, same p ✓, same noise model ✓, same simulator ✓, LER held constant only for the `Promatch ‖ Astrea-G` configuration ✓ — that is the configuration to cite when claiming parity. `Promatch + Astrea` alone is **7.7× worse LER at d=13**, so it is *not* straightforwardly faster-at-equal-quality.

### Artifact — verdict `PARTIAL_MATCH`

`github.com/nargesalavi/Promatch` `[code]`
- C++17 + CMake ≥ 3.20.2 + OpenMPI; Apache-2.0. Directories: `PromatchPredecoder/{src,include}`, `quarch/blossom5`, `quarch/dramsim2`, `quarch/dramsim3`, `scripts/`.
- README targets reproduction of "Section 6.1 (Table 2 and Table 3 on Logical Error Rates) and Section 6.2 (Figure 14 and Figure 15 on Error Rate Sensitivity Analysis up to 5×10⁻⁴)". Requires ~120 cores, ~2 GB/core.
- **No `.v`, `.sv`, `.vhd`, `.scala`, or `.tcl` anywhere in the tree** (checked via GitHub tree API). The Kintex synthesis (Table 7) and the 250 MHz figure are therefore **not reproducible from the public artifact**.
- Presence of `dramsim2`/`dramsim3` with DDR3/DDR4/HBM `.ini` configs indicates the memory subsystem was modelled in simulation, consistent with the cycle-estimate methodology.
- Verdict: the **accuracy** claims are backed by the artifact; the **hardware** claims are not.

### Framing tag: `EARLY_FTQC`

Single logical qubit, d≤13, p = 10⁻⁴–5×10⁻⁴ (below present superconducting hardware). Motivation is stated as applications needing "<10⁻¹²" error rates. No logical-qubit-count target given.

---

## 2. Micro Blossom (ASPLOS 2025, DOI 10.1145/3676641.3716005)

Yue Wu, Namitha Liyanage, Lin Zhong — Yale.
Source: arXiv **2502.14787v1** (20 Feb 2025), comments field says "to be published in ASPLOS 2025". `[paper-preprint]`

### Workload structure

| Quantity | Value | Source |
|---|---|---|
| Syndrome rate | "potentially measured 10⁶ times per second"; "measurement cycle of 1 µs" | `[paper-preprint]` |
| Distances | **d = 3, 5, 7, 9, 11, 13, 15** | `[paper-preprint]` |
| Physical error rates | p = 0.1%, 0.3%, 1%, 3%, and up to 0.499 for stress | `[paper-preprint]` |
| Logical qubits | **1** — stated as a limitation | `[paper-preprint]` |
| Decoding graph, d=13 | **1,274 vertices, 5,629 edges**; |V| = Θ(d³) | `[paper-preprint]` |
| Window | **round-wise fusion** — "the decoder only needs to focus on a constant number of recent measurement rounds" | `[paper-preprint]` |
| Streaming vs batch | **Streaming** (incremental fusion); batch also evaluated as a configuration | `[paper-preprint]` |
| Latency budget | "within a microsecond … in the case of implementing fault-tolerant logical T̂ gates" | `[paper-preprint]` |

### Architecture rationale — note the framing shift

Micro Blossom **does not use the word "backlog"** anywhere in the preprint (verified by targeted search). It frames the constraint as a **soft** deadline:

> "Nontrivial fault-tolerant quantum computing requires feedforward from the decoder with a soft deadline [35], making the decoding a soft real-time problem. The soft deadline comes from implementing logical non-Clifford gates … While waiting for the decoded readout, the target qubit accumulates more logical errors. … If the decoding latency is L measured in the number of stabilizer measurement cycles, then the logical error rate of the target qubit effectively becomes roughly p_L^MWPM(1+L/d). Taking d=21 surface code with 1 µs measurement cycle as an example, the effective logical error rate is 34 p_L^MWPM for Fusion Blossom, and 5 p_L^MWPM for the faster but less accurate Union-Find decoder. In this case, although Union-Find decoding has 5x more logical errors than MWPM decoding, it causes fewer logical errors when including latency-induced idle errors."

This is a genuinely different formulation of the same physical problem: latency is converted into an *error-rate penalty* p_L^eff = p_L(1 + L/d) rather than a cliff. It licenses reporting **average** latency, which Promatch's framing would not.

### Computational structure

- **Algorithm class**: exact **MWPM / blossom**, partitioned by phase. "Micro Blossom implements the primal phase of the blossom algorithm in software that flexibly handles complex data structures. It implements the dual phase in the programmable accelerator." Software = ARM Cortex-A72 in the Versal PS; hardware = programmable logic.
- **Parallelism**: the finest available — "The accelerator associates a vPU for each vertex and an ePU for each edge in the decoding graph, achieving the finest possible parallelism." **O(d³) processing units.** Explicitly contrasted: "Fusion Blossom is effective to coarse-grained parallelism and Parity Blossom and Sparse Blossom do not exploit parallelism at all."
- **Memory**: 19–34 bits per vPU, 4 bits per ePU; 66 kb FPGA block memory at d=13. The working set is *distributed into the fabric* — there is no monolithic table like Promatch's 345 KB path table. This is the architectural fork between the two papers.
- **Communication**: "Each instruction is first broadcast to all PUs", results "convergecasted into a single response" through trees with **O(log|E|)** aggregation latency; "Each PU only talks to its immediate neighbors on the decoding graph." So C(P) inside one chip is a log-depth reduction tree plus nearest-neighbour mesh traffic.
- Pipelining for throughput, not latency: "While adding pipeline does not reduce the decoding latency, it improves decoding throughput by allowing the accelerator to multiplex across multiple independent decoding tasks" — context-switch depth up to 1024.

### Scaling analysis

Stated complexity results (abstract, `[paper-preprint]`):
- Worst case: **O(d¹²) → O(d⁹)**
- Average: **O(p·d³⁺¹) → O(p²·d²⁺¹)** for p ≪ 1

So W shrinks in exponent by using O(d³) PUs — sublinear speedup in P, which is what the log-depth convergecast and the residual serial primal phase cost you.

**Resource scaling is the wall**: O(d³·polylog d) LUTs — 156k (d=9) → 553k (d=13) → **867k of 900k available (d=15)**. And frequency degrades monotonically with d: 170 / 141 / 107 / 93 / 77 / 62 / 43 MHz for d = 3…15. The two curves cross:

> "To achieve sub-µs decoding latency at d=15, the clock frequency must be at least 68 MHz to catch up with the O(p²d²+1) decoding time scaling. This clock frequency is beyond the reach of commercially available FPGAs but achievable if the accelerator is implemented in ASIC."

At d=15 the prototype achieves 43 MHz and needs 68 MHz. **d=15 is where this design point fails on FPGA** — a concrete, dated boundary.

### Hardware evidence level

`FPGA_PROTOTYPE` (measured), with `PROJECTED` for the ASIC remark. This is the strongest evidence level in the set — but with three precise qualifications:

1. **The 0.8 µs is measured on the board**: Xilinx **Versal VMK180**, ARM Cortex-A72 PS, internal **64-bit AXI4** bus, 62 MHz PL. "Measured at d=13 and p=0.1%, the prototype achieves an average decoding latency of 0.8 µs at a moderate clock frequency of 62 MHz." It **includes I/O**: "the evaluation of Micro Blossom includes all I/O latency between the CPU and the accelerator." Sample volume: "each accumulating 1000 logical errors (2.5 × 10⁸ samples)".
2. **It is an average, not a worst case.** Tail behaviour is reported instead through a "k-tolerant cutoff latency" defined by P(L ≥ L_cutoff^k) = k·p_L. No single worst-case nanosecond number is given for d=13. `NOT_FOUND` for a measured worst case.
3. **The syndromes are simulated, not from a quantum device.** Circuit-level noise per Stim-style model; the 1 µs cycle is an assumption. Not `REAL_HARDWARE` in the quantum sense.

**One asymmetry worth flagging in the 8× claim**: "We note that we only evaluate the CPU wall time in the baseline evaluation, excluding the I/O latency to the quantum controller, which is typically more than 0.8 µs." Micro Blossom's number includes its own I/O; the software baseline's number excludes I/O that the paper itself estimates at >0.8 µs. The 8× is therefore *conservative* as an end-to-end system comparison and *not* a like-for-like kernel comparison. The paper is transparent about this.

### Quantitative results, with context

- **8×** shorter latency than Sparse Blossom (Higgott & Gidney), "for the same code distance and noise model", d=13, p=0.1%. `[paper-preprint]`
- **17×** vs Parity Blossom (on Apple M1 Max), decomposed in the ablation as parallel dual phase **2.0×**, parallel primal phase **4.2×**, round-wise fusion **2.0×**.
- Latency vs d at p=0.1% (Fig. 9): ≈0.06 / 0.09 / 0.15 / 0.25 / 0.4 / 0.8 µs for d = 3/5/7/9/11/13; d=15 exceeds 1 µs at 62 MHz.
- **Accuracy is held exactly constant**: "Micro Blossom is logically equivalent to them [Parity Blossom and Sparse Blossom]"; verified "by comparing its results with those of a known exact MWPM decoder". This is the cleanest speed-at-equal-quality claim in the whole set — the comparison does not need an accuracy asterisk.
- Caveat the paper volunteers: "Micro Blossom runs at a lower clock frequency and includes I/O latency, and thus has a larger latency floor than the software baseline" — i.e. at small d the FPGA can lose.

### Scale-out relevant statements

> "We note that Micro Blossom as reported here supports a single logical qubit."

To extend it, the paper names three requirements: an "operating system-like controller [to] dynamically configure the decoder to handle a dynamic decoding graph with growing rounds of measurements in a streaming manner"; support for "dynamic inter-block fusions, which complements the intra-block fusion"; and a data plane where "the quantum control stack must interface with the decoder efficiently to load and route syndrome data at **Terabit/s**."

That Terabit/s figure is the single most HPC-shaped number in the corpus.

### Artifact — verdict `CONSISTENT`

`github.com/yuewuo/micro-blossom` `[code]`, MIT, ~672 commits.
- **Scala/SpinalHDL** hardware generator under `src/fpga/` (subdirs confirmed: `Xilinx/`, `microblossom/`, `utils/`, `yosys/`), producing AXI4-interfaced Verilog via `MicroBlossomBusGenerator`; decoding graph supplied as JSON. **Rust** CPU-side implementation.
- `benchmark/hardware/` contains real-board flows: `decoding_speed/{circuit_level_batch,circuit_level_fusion,circuit_level_no_offloading,circuit_level_software}/run.py`, `bram_speed/run.py`, `frequency_optimization/axi4_with_small_code/run.py`, `resource_estimate/`. The `no_offloading` directory corresponds to the ablation.
- Evaluated configs appear as data files: `d_3.txt … d_15.txt`, error rates `p0.0001`–`p0.01`. VMK180 named explicitly.
- The parallel/hardware claims are **visibly implemented** — HDL generator, board scripts, and per-distance configs all present. This is the one artifact in the set where the hardware claim is independently checkable.
- **Discrepancy to record**: the README carries performance claims **absent from the arXiv v1 paper** — "367 ns on FPGA … 14x reduction" at d=9/p=0.001, "152k LUT", "1.4k LUT per logical qubit" vs "Helios at 2.1k LUT per logical qubit", and "real-time decoding of at most 110 logical qubits (d=9, p=0.001) while achieving the throughput requirement of 1 million measurement rounds per second". I searched the preprint for "110", "1.4k LUT", "million measurement rounds" — **none occur**. The paper instead says it "supports a single logical qubit". Treat the 110-logical-qubit figure as a `[code]`/`[documentation]` claim about *throughput multiplexing capacity*, not a paper result, and note it may reflect post-publication work.

### Framing tag: `EARLY_FTQC`

Single logical qubit, d ≤ 15, p = 0.1% (roughly current hardware), motivated by the logical T gate.

---

## 3. RESCQ (ASPLOS 2025, DOI 10.1145/3676641.3716018)

Sanjay Sethi, Jonathan M. Baker — UT Austin.
Source: arXiv **2408.14708v2**. `[paper-preprint]`

RESCQ is in this census but is **not a decoder paper**. It is a real-time *resource-scheduling* paper, and it is the most interesting one for the HPC question precisely because its classical computation misses its deadline by 100× and it does not build hardware.

### Workload structure

- **Continuous-angle QEC**: instead of discrete T states, produce arbitrary small-angle rotation states |m_θ⟩. Baseline is the **STAR** architecture (Akahoshi et al.). Preparation is **repeat-until-success**: "injection of |m_θ⟩ has a fixed success rate of 50%", E[# injections] = 2. Expected preparation ≈ 8.4 cycles worst case.
- **Lattice surgery cycle ≈ 1 µs**; a distance-d patch performs "d rounds of syndrome measurements in every lattice surgery cycle".
- **d ∈ {3,5,7,9,11}**, primary results at **d=7, p = 10⁻⁴**.
- Program scale: 24 benchmarks from QASMBench/SupermarQ, **13 → 420 qubits**; largest has 6,384 Rz and 6,510 CNOT gates. Ancilla grids evaluated up to 1000×1000.

### The real-time constraint — a different one

The classical inner loop is a **minimum spanning tree** over "a weighted undirected graph of the grid with the qubits as the nodes, and the edge weights as the maximum of the activity between the neighbouring qubits", where activity = "the ratio of the number of cycles the ancilla qubit was active in the last c cycles" (c = 100). The MST picks CNOT routing paths through ancillas least likely to be busy.

Verbatim:

> "Based on realistic grid sizes and estimates from MST computation time on modern CPUs (MacBook Air machine with M2 chip), it takes about 100µs to compute the MST."

> "Since a lattice surgery cycle takes about 1µs, the time taken to compute the MST is τ_MST = 100 lattice surgery cycles."

**This is a 100× deadline miss on exactly the same 1 µs clock that Promatch and Micro Blossom build hardware to meet.** RESCQ's answer is not acceleration:

> "The MST is computed asynchronously and does not stall quantum execution"

It recomputes every k ∈ {25, 50, 100, 200} cycles and runs on stale MST data in between. **No dedicated hardware, FPGA, or classical controller is proposed** — I searched for it; the paper "addresses *what* the scheduler must compute but leaves the classical substrate implicit."

That asymmetry — decoding gets custom silicon, scheduling gets staleness tolerance — is the single sharpest datum in this census about *what makes a quantum classical-compute problem an architecture problem*. It is not the deadline. It is whether the answer is on the feedforward critical path.

### Per-cycle decision structure

Per lattice surgery cycle the scheduler must: select among **16 candidate routing paths** minimising expected completion; allocate free ancillas to |m_θ⟩ preparation and reclaim on failure; and prioritise gate enqueueing. Algorithm 1 minimises `MAX(startTime, expFreeTime)` over path qubits. These per-cycle decisions are cheap; only the MST is expensive, and only the MST is made stale.

### Hardware evidence level

`SOFTWARE_SIMULATION` + `ARCH_SIMULATION`, with the 100 µs MST figure being an `ANALYTIC_MODEL`/measured-on-a-laptop estimate. **No hardware of any kind.** Custom C++ simulator (CMake + Boost), Qiskit for compilation, symbolic execution with per-seed randomised RUS outcomes.

### Quantitative results

- **2× geometric-mean reduction in cycle count** vs baselines, at d=7, p=10⁻⁴.
- Baselines: greedy path selection and **AutoBraid**; architectural baseline is STAR.
- Under maximal grid compression: **1.65×** average improvement.
- Latency distribution: ">50% of the CNOT gates in RESCQ take 2 cycles and more than 90% take 6 or less cycles", vs AutoBraid concentrating at 5 and 8 cycles.
- Decoding is referenced only as a resource, not modelled: "These resources include classical bandwidth for decoding [28]".

### Artifact — verdict `CONSISTENT`

`github.com/5ayam5/Realtime-Scheduling-for-Continuous-Angle-QEC-Architectures`, archived at **Zenodo 10.5281/zenodo.14769159**, MIT. `[code]` C++ simulator + Python post-processing; `circuits/`, `config/`, `postprocess/`, `scripts/`, `simulator/`; three schedulers implemented (RESCQ, static, autobraid); `run_all.sh` batch driver; `basic_test.cfg`. No HDL — and none is claimed, so the artifact matches the claims exactly.

### Framing tag: `EARLY_FTQC`

Explicit: "near-term FTQC regime, where we have about 1-2 orders of magnitude improvement in the logical error rates"; "near and intermediate term demonstrations of QEC".

---

## 4. HetEC (ASPLOS 2025, DOI 10.1145/3676641.3716001)

Samuel Stein et al. (PNNL/Yale/IBM/Princeton/UCSD/UW). Source: arXiv **2411.03202v2**, titled "Architectures for Heterogeneous Quantum Error Correction Codes". `[paper-preprint]`

- **Proposal**: a von-Neumann split — "the computer into a processing unit composed of surface code blocks, a memory unit composed of gross code blocks, and an ancilla bus that transfers quantum information between them". Surface code for universal computation, **gross code [[144,12,12]]** (rate 1/24) for memory, **103-qubit ancilla bus** between them. Gross-code logical qubits accessed via automorphism permutation through one probe qubit.
- **Decoding**: essentially absent. One passing mention — "all stabilizers are measured, and this information decoded". No decoder latency, no real-time constraint, no decoder hardware. Note the irony: the gross code requires **BP+OSD**, a much harder real-time target than MWPM, and the architecture's clock is defined as one measurement cycle with decoding abstracted away.
- **Parameters**: gross threshold 0.65%, surface threshold 0.7%; p = 10⁻³, 10⁻⁴ simulated, 10⁻⁵ fitted.
- **Evidence**: `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (two-step logical-error-rate substitution into circuit-level estimates; error rates partly imported from prior work). No hardware.
- **Results**: "physical qubit reductions of up to 6.42× … at the cost of up to a 3.43× increase in execution time". Across benchmarks: 7.81× average physical qubit reduction, 1.99× LER increase, 2.53× logical-cycle increase. Example (28-qubit adder): 13,369 → 1,746 physical qubits.
- **Framing**: `FTQC`.

---

## 5. QECC-Synth (ASPLOS 2025, DOI 10.1145/3669940.3707236)

Keyi Yin, Hezi Zhang, Xiang Fang, Yunong Shi, Travis S. Humble, Ang Li, Yufei Ding. Source: arXiv **2308.06428v4** (preprint title: "…on Sparse **Hardware** Architectures"). `[paper-preprint]`

- **Problem**: map error-syndrome-measurement circuits onto hardware whose connectivity is sparser than the code demands — "the mismatch between code topology and hardware architecture"; surface codes want degree-4, real hardware offers degree-2/3. Optimises (a) extra CNOTs from ancilla-bridge construction and (b) circuit depth.
- **Method**: **MaxSAT** — "By translating code structures, hardware architectures, and mapping/scheduling conditions into Boolean constraints, we frame these optimization problems into MaxSAT framework, solvable by SAT solvers." Two-stage. Solver runtime/timeout: `NOT_FOUND` in the preprint HTML I could read.
- **Decoding / real-time**: **not discussed at all.** This is a compile-time problem; its "latency" is solver wall-clock, with no deadline.
- **Results**: vs Sabre, "average reduction of 74.9% and 26.5% in extra CNOT gate counts"; vs SATmap, "34.7% and 55.5% in circuit depth"; vs Surf-Stitch, "10% fewer extra CNOT gates and 38.5% shallower circuits". Baselines "frequently fail to provide solutions for special QEC codes and hardware setups and exceed memory limits for large-scale problems."
- **Evidence**: `SOFTWARE_SIMULATION` (solver + circuit metrics). No hardware.
- **Framing**: `EARLY_FTQC` with NISQ-era hardware constraints (degree-2/3 devices, defective qubits).

---

## 6. Codesign of QEC codes and modular chiplets in the presence of defects (ASPLOS 2024, DOI 10.1145/3620665.3640362)

Lin, Viszlai, Smith, Ravi, Yuan, Chong, Brown (UChicago / Infleqtion / MIT CSAIL / IBM Quantum). Source: arXiv **2305.00138v3**. `[paper-preprint]`

- **Proposal**: combine chiplet-level post-selection (discard bad chiplets before integration) with **super-stabilizer measurements** that adapt the code around defective qubits, so partially-defective chiplets remain usable.
- **Decoding**: `NOT_FOUND` as a subject. Only "Using the error syndrome, we can obtain a correction to recover encoded information using minimum-weight perfect-matching algorithm", stated as background. The paper does not analyse how super-stabilizers deform the matching graph or what that costs a real-time decoder — which is the natural bridge to the decoder papers and is simply not taken.
- **Parameters**: d = 3, 5, 9, 15, 17, **27**; chiplet sizes l ∈ {9,11,13,15,17,33,39}; defect rates 0.1–2%; physical error rates 5×10⁻⁴–2×10⁻³. Application case: a 226 × 63 grid of d=27 patches, ~25 billion surface-code cycles.
- **Evidence**: `SOFTWARE_SIMULATION` — Stim + Monte Carlo, fit to LER = β(Np)^(αd).
- **Results**: "at a defect rate of 1% the resource overhead can be reduced to below 3X and 6X respectively for the two defect models", against a defect-intolerant modular baseline at "45X and more than 10⁵ X". Shor's-algorithm case at 0.1% defects: 1.58× overhead / 94.5% yield vs 71.32× / 1.4%. Physical qubit counts span 2.1×10⁷ to 7.6×10¹².
- **Framing**: `FTQC` — this is the only paper in the set whose qubit counts reach 10⁷–10¹².

---

## 7. AlphaSyndrome (ASPLOS 2026, DOI 10.1145/3779212.3790123)

Liu, Decker, Chen, Ping, Zhou, Li (Penn); Kalloor, Weiden (Berkeley); Shi (AWS/Michigan); Javadi-Abhari (IBM); Iancu (LBNL). Source: arXiv **2601.12509v2**. `[paper-preprint]`

- **Problem**: gate ordering/parallelism inside syndrome-measurement rounds. Different schedules give "distinct error-propagation paths under realistic noise, leading to large variations in logical error rate", and "repeated syndrome-measurement cycles dominate its spacetime and hardware cost".
- **Method**: **Monte Carlo Tree Search** with decoder-in-the-loop reward — "guided by code structure and decoder feedback". Two objectives: keep error patterns far from logical operators, and inside "the decoder's correctable region". 4,000–8,000 MCTS iterations per step; run on two Intel Xeon 6960P (72 cores each).
- **Decoder relevance — the reason this paper matters to the census**: it is *decoder-aware at compile time*. Verbatim: "hardware platforms usually put strict time constraints on how long a decoder can execute to decode one round of syndrome measurement results", and hence "a classical decoder can only employ a heuristic algorithm to solve this NP-hard decoding problem with an approximate solution." It optimises the circuit so a fast approximate decoder does well — the inverse of Promatch's move (make the syndrome easier, not the decoder stronger). But it **cites no hardware-decoder paper**: no Promatch, no Micro Blossom, no Astrea, no Clique. Its decoder references are Sparse Blossom, BP-OSD, hypergraph union-find, and foundational coding theory.
- **Codes**: rotated surface d=3–9; hexagonal colour [[7,1,2]]–[[61,1,9]]; square-octagonal colour [[7,1,3]]–[[49,1,9]]; hyperbolic surface [[30,8,3]]–[[80,18,5]]; hyperbolic colour [[24,8,4]]–[[40,16,4]]; defective surface [[25,2,5]], [[41,2,7]]; bivariate bicycle [[72,12,6]]. Decoders swept: MWPM, BP-OSD, hypergraph UF.
- **Evidence**: `SOFTWARE_SIMULATION` — Stim, IBM Brisbane device parameters (CNOT depolarizing p = 0.0074, idle p = 0.0052).
- **Results**: "reduces logical error rates by 80.6% on average (up to 96.2%)" vs lowest-depth baselines; matches Google's hand-crafted surface-code schedules; beats IBM's bivariate-bicycle schedule by 44% with BP-OSD; "reduces the required space–time volume by 20-90%".
- **Framing**: `GENERAL` / `EARLY_FTQC` — code-family-agnostic, current-device noise parameters, fault-tolerant codes.

---

## 8. PropHunt (ASPLOS 2026, DOI 10.1145/3779212.3790205)

Viszlai (UChicago), Maurya, Tannu (Wisconsin), Martonosi (Princeton), Chong (UChicago). **Author list as given in your brief is confirmed.** Source: arXiv **2601.17580v1**. `[paper-preprint]`

- **Problem**: same target as AlphaSyndrome — syndrome-measurement circuit quality — but from an error-propagation-analysis angle rather than search-over-schedules. "optimize SM circuits based on modifying error propagation to minimize ambiguity, directly addressing logical error rate."
- **Method**: build circuit-level decoding graphs → identify *ambiguous error subgraphs* (identical syndrome, different logical effect) → encode minimum-weight logical errors as **MaxSAT** (Z3 preprocessing + Loandra, 360 s timeout) → enumerate CNOT reorder/reschedule candidates → apply verified changes iteratively.
- **Decoding / real-time**: `NOT_FOUND`. Decoders appear only as evaluation instruments: "Decoding for surface codes was performed using PyMatching, and decoding for LP and RQT codes was performed using BP-LSD."
- **Codes**: surface [[9,1,3]], [[25,1,5]], [[49,1,7]], [[81,1,9]]; lifted-product [[39,3,3]], [[54,11,4]]; random quantum Tanner [[108,18,4]], [[60,2,6]].
- **Evidence**: `SOFTWARE_SIMULATION` — Stim; 48 Intel Xeon Silver 4116 cores.
- **Results**: on surface codes, "produces SM circuits that match the performance of well-known, hand-designed circuits" (parity, not improvement — an honest result); on LP/RQT codes, "2.5x-4x lower logical error rates compared to a standard coloration circuit at a physical error rate of 0.1%" (baseline: Tremblay et al. 2022 coloration). Hook-ZNE application: "3x-6x error reduction compared to Distance-Scaling ZNE".
- **Artifact**: `github.com/jviszlai/PropHunt`, Zenodo **10.5281/zenodo.17945386**, Docker + Makefile, ~8–12 h to run. Claimed but not inspected by me — I did not open this repository, so no verdict beyond `INSUFFICIENT_EVIDENCE` on artifact-vs-claim consistency.
- **Framing**: `EARLY_FTQC` / `GENERAL`.

---

## 9. ACQC — "Accelerating Computation in Quantum LDPC Code" (ASPLOS 2026, DOI 10.1145/3779212.3790122)

Jungmin Cho, Hyeonseong Jeong, Junpyo Kim, Junhyuk Choi, Juwon Hong, Jangwoo Kim — SNU HPCS Lab. **`[abstract]` ONLY.** No arXiv preprint exists (searched several ways); ACM DL is blocked; the lab and author pages list it as "to appear" with no PDF. Metadata via Semantic Scholar and INSPIRE.

- **Claim**: qLDPC codes need "an order of magnitude fewer qubits than widely used surface codes" but have operational limits complicating program execution. **ACQC** is a software–hardware co-design with three parts: decomposition–layout co-optimisation, qLDPC-specific overhead reduction, and magic-state-distillation layout optimisation.
- **Results**: "4.4× speedup over the baseline qLDPC code FTQC and 18.3× qubit reduction over the surface code" (average).
- **Decoding**: unknown. The abstract gives no indication of decoder treatment, and I will not infer one. `NOT_FOUND`.
- **Evidence level**: cannot be determined from the abstract. Given the group's prior work (QIsim, XQsim, CryoCore, "A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer" ASPLOS 2024), `ARCH_SIMULATION` is plausible but is `[inference]` only, not established.
- **Framing**: `FTQC` `[abstract]`.
- Note: it is open access (GOLD, CC-BY) on ACM DL, so it is retrievable from an unblocked network — worth a second pass for the census.

---

## 10. iSwitch (ASPLOS 2026, DOI 10.1145/3779212.3790177)

Keyi Yin, Xiang Fang, Zhuo Chen, David Hayes, Eneet Kaur, Reza Nejabati, Hartmut Haeffner, Wes Campbell, Eric Hudson, Jens Palsberg, Travis S. Humble, Yufei Ding (UCSD / Quantinuum / Cisco Quantum Lab / Berkeley / UCLA / ORNL). ACM author list `[abstract]`; content from arXiv **2504.16303**, which is titled **"Flexion"** and additionally lists Ang Li (PNNL). `[paper-preprint]` — **the preprint and published versions differ in title and author list, so treat content mapping with care.**

- **Proposal**: don't encode everything. Keep qubits *bare* for single-qubit gates (ion-trap 1Q error ≈ 1×10⁻⁶) and encode into surface-code logical qubits only for two-qubit gates (2Q MS error ≈ 1×10⁻³). Requires "low-noise conversion between bare and logical qubits" at runtime, "without post-selection or pre-initialized states".
- **Decoding**: one relevant sentence — "These random values do not compromise subsequent QEC operations and can be handled using standard stabilizer frame updates or corrected via efficient gauge-fixing decoders." No latency, no real-time analysis. `NOT_FOUND` for wall-clock decoder treatment; also `NOT_FOUND` for shuttle/stabilizer cycle times.
- **Parameters**: surface d = 5, 7, 9; a d=9 T gate ≈ 2,000 physical qubits; MSD-Logical baseline 30 logical qubits × 2d² at d=9 = 4,860 physical qubits. Benchmarks: Ising, Heisenberg (n=30), H₂O, BeH₂ under UCCSD.
- **Evidence**: `SOFTWARE_SIMULATION` — Qiskit-Aer density matrix (≤10 qubits, Nelder-Mead) and Stim + PyMatching (larger, Clifford ansatz, genetic algorithm pop. 64). No hardware.
- **Results**: "8.0x performance improvement across various EFT applications over NISQ execution"; "15.5x improvement over standard FTQC under the same qubit budget"; Clifford+T decomposition depth overhead 14.9× average, up to 27.8×.
- **Artifact**: `NOT_FOUND` in the preprint.
- **Framing**: explicitly the **`NISQ`→`EARLY_FTQC` transition** — its two baselines are literally named "NISQ-Bare" and "MSD-Logical".

---

## 11. Architecting Scalable Trapped Ion Quantum Computers using Surface Codes (ASPLOS 2026, DOI 10.1145/3779212.3790128)

**Scott Jones and Prakash Murali, University of Cambridge** (your brief guessed "Sam Jones" — it is Scott Jones). Source: arXiv **2510.23519v1**. `[paper-preprint]`

- **Proposal**: how QCCD trapped-ion machines should be built to run surface codes, via a topology-aware compiler. Headline architectural finding: "small traps of two ions are surprisingly ideal from both a performance-optimal and hardware-efficiency standpoint", against the prior expectation of 20–30-ion traps.
- **The number that matters most to this census**: QCCD operation timings — **two-qubit gates 40 µs, measurement 400 µs, routing 5–100 µs**. Compare Promatch's and Micro Blossom's 1 µs superconducting cycle. That is a **~400× larger decoding budget**, and it changes the answer to the census's central question for this platform.
- **Decoding**: `NOT_FOUND`. The paper does not discuss decoders, decoder latency, or real-time decoding — despite operating in exactly the regime where the constraint most plausibly relaxes. Stim is used only for logical-error-rate evaluation.
- **Parameters**: d = 2–20; 2d²−1 physical qubits per logical qubit (d=4 → 31 qubits; d=7 → 49 physical qubits cited for the code block).
- **Evidence**: `SOFTWARE_SIMULATION` + `ARCH_SIMULATION` — custom compiler + Stim with trapped-ion noise models.
- **Results**: "outperforms existing QCCD compilers by an average of 3.8X in terms of logical clock speed" vs Murali et al. 2020 and Saki et al. 2022.
- **Framing**: `EARLY_FTQC`.

---

# PART B — CROSS-PAPER SYNTHESIS

## 1. Lineage

The decoder work in this window is two distinct lines that meet exactly once.

**Line A — capacity-limited exact decoding + filtering (Georgia Tech / Qureshi–Das).**
`LILLIPUT (ASPLOS'22, lookup tables, d=3/5 at 29/42 ns, "tables grow exponentially with the distance")` → `AFS (HPCA'22, union-find)` → `Astrea / Astrea-G (ISCA'23: exact brute force to d=7 in 456 ns; greedy to d=9 in 1 µs)` and `Clique (ISCA'23, predecoder)` → **`Promatch (ASPLOS'24)`**. Parallel influences it names: Smith et al. predecoding, Chamberland et al. neural predecoding, NEO-QEC. `[paper-preprint]`

The line's governing idea is that the main decoder has a **fixed combinatorial capacity** (HW ≤ 10, 945 matchings), and progress in d comes from *shrinking the problem to fit*, not from growing the machine. Promatch is the most refined statement of that idea. Its cost is that accuracy becomes a tunable, and the design cannot absorb more silicon.

**Line B — parallel exact MWPM in hardware (Yale / Zhong).**
`Parity Blossom & Fusion Blossom (2023)` → **`Micro Blossom (ASPLOS'25)`**, with `Helios` (Liyanage et al., the FPGA union-find decoder from the same group) as acknowledged inspiration: "We are inspired by Helios [25], a low-latency UF decoder implemented on FPGA."

The governing idea is the opposite: **keep the algorithm exact and spend O(d³) processing units.** Progress in d comes from the machine growing with the graph.

**The junction.** Micro Blossom cites Promatch **[3]** and rejects Line A explicitly:

> "Astrea [38] and Promatch [3] are hardware-accelerated MWPM decoders that achieve roughly the same accuracy of MWPM decoding under certain conditions. They decode simple syndromes below certain Hamming weights, which implicitly assumes small code sizes and low physical error rates. For example, at d=13 and p=0.1%, their approximation leads to more than 13.9× higher logical error rate [3]."

and in the introduction: "Many have resorted to less accurate decoders that approximate MWPM decoding [3], causing 1.7x [25] or even 13.9x [3] more logical errors at code distance d = 13 and physical error rate p = 0.1%."

Promatch does **not** cite Micro Blossom (Promatch predates it by ten months) and does not discuss sliding- or parallel-window decoding at all.

**Where the line runs after Micro Blossom — and out of ASPLOS.** From the citation graph of Micro Blossom (27 citing works), the successor generation is dominated by *parallel/windowed/distributed* decoding and *scale-out* concerns, and almost none of it lands in ASPLOS main track:

- **SWIPER: Minimizing Fault-Tolerant Quantum Program Latency via Speculative Window Decoding** — ISCA 2025
- **Triage: An Adaptive Parallel Window Decoding Scheduler for Real-Time Fault-Tolerant Quantum Computation** — ISCA 2026
- **Coset Ensemble Decoder for QEC with Algorithm-Hardware Co-Design** — ISCA 2026
- **Snowflake: A Distributed Streaming Decoder** — Quantum, 2024
- **A Case for Elastic Quantum Error Correction Decoders** — EuroSys 2024
- **A Scalable FPGA Architecture for Real-Time Decoding of Quantum LDPC Codes Using GARI**; **Low Latency GNN Accelerator for QEC**; **Lottery BP: Unlocking Quantum Error Decoding at Scale**; **A Scalable Open-Source QEC System with Sub-Microsecond Decoding-Feedback Latency**; **Network-Integrated Decoding System for Real-Time QEC with Lattice Surgery** (IEEE QCE 2025); **Stream Decoding with Confidence Scores at Room and Cryogenic Temperatures**; **decoder-bench** (IISWC 2025)

**The structural observation for your census**: within ASPLOS main track, the decoder-microarchitecture line is **two papers, both before 2026**. The five ASPLOS 2026 QEC papers (AlphaSyndrome, PropHunt, ACQC, iSwitch, trapped-ion) contain **zero decoder-hardware designs**; they are compiler, synthesis, code-layout and platform-architecture papers. Two of them (AlphaSyndrome, PropHunt) are *about* syndrome extraction circuits and are therefore decoder-adjacent, but AlphaSyndrome cites no hardware decoder at all and PropHunt treats decoders purely as evaluation instruments. The decoder-acceleration conversation moved to ISCA and to arXiv/Quantum between ASPLOS'25 and ASPLOS'26.

A separate, non-intersecting branch: **RESCQ** (real-time scheduling) and the layout/code papers (**QECC-Synth**, **chiplet codesign**, **HetEC**, **ACQC**). None of these cites the decoder line, and the decoder line does not cite them. The chiplet codesign paper is the most conspicuous non-connection: super-stabilizers deform the matching graph, which is a direct input to any MWPM decoder's cost model, and neither side takes the link.

## 2. Tensions

**T1 — Promatch vs Micro Blossom on whether approximation is acceptable. → `DIFFERENT_REGIME`, with a specific mis-transfer.**

Micro Blossom asserts Promatch's approximation costs "more than 13.9× higher logical error rate" **at d=13 and p=0.1%**. But 13.9× is Promatch's *own* worst-case figure over its sweep, and that sweep is **p = 10⁻⁴ to 5×10⁻⁴**. **p = 0.1% = 10⁻³ is outside the range Promatch evaluated.** At the operating point Promatch designs for (d=13, p=10⁻⁴), Promatch ‖ Astrea-G reports **3.4 × 10⁻¹⁵ = 1.0× MWPM**, i.e. parity. So the two papers are not disagreeing about the same measurement: Micro Blossom transplants a worst-case-over-p number to a p neither paper jointly evaluated. This is not a fabricated criticism — Promatch's degradation with p is real and its own data show 202× for the non-parallel configuration — but it is **not** a demonstrated d=13/p=0.1% result for Promatch. Classify as different-regime, and note the number's provenance whenever either paper is cited.

**T2 — What "1 µs" means: hard deadline vs soft deadline. → `TRUE_CONFLICT` (of framing, which determines the metric).**

Promatch: "To prevent a backlog of errors, error decoding must be performed in real-time (i.e., within 1µs)"; "worst case latency of 1µs". Micro Blossom: "a soft deadline … making the decoding a soft real-time problem", with **no occurrence of the word "backlog" anywhere in the preprint** (verified by search), and the penalty modelled continuously as p_L^eff = p_L(1 + L/d).

These are incompatible accounts of the same physics, and they are not reconcilable by measurement — they are different models of what the quantum machine does while it waits. The consequence is methodological and large: **Promatch reports maxima (960 ns) and provisions for the tail; Micro Blossom reports an average (0.8 µs) and characterises the tail only through a probability-weighted cutoff.** A reader comparing "960 ns" to "800 ns" is comparing a worst case to an average. Under Promatch's model, Micro Blossom's d=13 result does not establish that the deadline is met; under Micro Blossom's model, Promatch's tail provisioning is over-engineering that costs accuracy. Both positions are internally coherent.

**T3 — Speed-vs-accuracy accounting. → `DIFFERENT_METRIC`.**

Micro Blossom argues that at d=21 a union-find decoder with **5× worse LER beats MWPM** once idle errors during decoding are counted. Promatch's entire premise is that LER parity with MWPM must be preserved. These are the same trade-off evaluated with different objective functions (LER at the decoder output vs effective LER at the logical qubit). Neither is wrong; they cannot be ranked without fixing the objective. Any census statement of the form "decoder X is better" needs the objective named.

**T4 — Latency comparability across the two papers. → `DIFFERENT_METRIC` + different evidence level.**

| | Promatch | Micro Blossom |
|---|---|---|
| Figure | 960 ns | 800 ns |
| Statistic | **maximum** | **average** |
| Provenance | cycle count × (1/250 MHz) | **measured on VMK180** |
| Clock | 250 MHz (synthesis-achievable) | 62 MHz (implemented) |
| I/O included | not addressed | **yes, all CPU↔accelerator I/O** |
| Accuracy at that number | 1.0× MWPM (‖ AG) at p=10⁻⁴ | exactly MWPM |
| Evidence tag | `RTL_SYNTHESIS` + `ANALYTIC_MODEL` | `FPGA_PROTOTYPE` |

These two numbers should never be placed side by side without all six rows. The evidence-level difference is the largest single quality gap in this corpus.

**T5 — Where d-scaling breaks. → `DIFFERENT_REGIME`.**

Micro Blossom gives a hard, dated boundary: d=15 needs ≥68 MHz, the FPGA delivers 43 MHz, 867k of 900k LUTs consumed — "beyond the reach of commercially available FPGAs but achievable if the accelerator is implemented in ASIC" (`PROJECTED`; no ASIC latency figure is given, so this must not be reported as an achieved result). Promatch has no analogous wall because it never grows with the graph — its limit is instead accuracy erosion as it predecodes more aggressively at larger d and higher p. The two designs fail in different currencies (silicon vs fidelity), so "which scales better" has no single answer.

**T6 — RESCQ vs the decoder papers on how to handle a missed deadline. → `DIFFERENT_REGIME`, and the most instructive one.**

RESCQ has a 100 µs classical computation against a 1 µs cycle — a **100× miss**, worse than the gap the decoder papers build hardware to close. Its response is to run the computation asynchronously every k ∈ {25,50,100,200} cycles and act on stale data. It proposes **no accelerator at all**. The distinguishing variable is not the size of the miss; it is whether the result is on the **feedforward critical path**. A stale routing MST costs cycles; a late decode gates a logical T gate and (under Promatch's model) compounds. This is the cleanest available empirical answer to "why is decoding an architecture problem" — it is not the deadline, it is the non-approximability of being late.

**T7 — Platform. → `DIFFERENT_REGIME`, unremarked by any paper.**

Jones & Murali give trapped-ion **measurement at 400 µs** and 2Q gates at 40 µs. Promatch and Micro Blossom both anchor everything to superconducting's 1 µs. A 400× budget expansion would move d=13 exact MWPM comfortably into software on a commodity CPU (Micro Blossom's own baselines are 5.1 µs on an M1 Max for Parity Blossom, ~6.4 µs implied for Sparse Blossom at the 8× ratio). **No paper in this set makes that observation**, and the trapped-ion paper does not discuss decoding at all.

## 3. The architecture-vs-HPC question — `[inference]`, clearly labelled

Everything in this section is my analysis built on the numbers above, not any paper's claim.

### The T(P) = W/P + C(P) picture as the corpus leaves it

**W.** Per logical qubit, per d-round window, the decoding graph is Θ(d³) vertices and O(d³) edges (Micro Blossom, d=13 → 1,274 vertices / 5,629 edges, `[paper-preprint]`). Algorithmic work above that is superlinear: exact blossom is O(d¹²) worst case, reduced to O(d⁹) by Micro Blossom's parallelisation, with average O(p²d²⁺¹). Across a machine, W multiplies by logical qubit count, which the corpus does not evaluate above **one** in either decoder paper.

**P.** Micro Blossom's O(d³) PUs is one-per-vertex and one-per-edge — the finest decomposition the decoding graph admits. **Intra-logical-qubit spatial parallelism is therefore essentially exhausted at this design point**, and the residual serial component is the primal phase, which stays in software on the ARM core because it needs dynamic data structures. That is a classic Amdahl residue and it is *architectural*, not incidental: the irregular, pointer-chasing part of blossom resisted the fabric. Promatch sits at the opposite extreme, P ≈ 1, and buys its latency by shrinking W instead.

The parallelism that remains unexploited in these two papers is **across windows** (SWIPER, Triage, Snowflake in the citation graph) and **across logical qubits**.

**C(P).** Inside one chip, Micro Blossom's cost is broadcast + O(log|E|) convergecast over trees, plus nearest-neighbour mesh traffic. The measured 0.8 µs already includes CPU↔FPGA AXI I/O, and the paper notes I/O to a real quantum controller is "typically more than 0.8 µs" on its own. **This is the crux**: at a 1 µs budget with sub-µs already consumed by compute-plus-local-I/O, the headroom for any additional communication term is on the order of a couple hundred nanoseconds. A single short-reach serial hop plus a switch traversal is comparable to or larger than that headroom.

### Conditions under which decoding could stop being a single-accelerator problem

I see four, in increasing order of how badly they break the current design point:

1. **Logical qubit count, with independent patches — the benign case.** Between lattice-surgery operations, distinct logical qubits' decoding problems are independent. Scaling here is *replication or time-multiplexing*, not latency parallelism: it is a throughput problem, and Micro Blossom already provides the mechanism (pipelining with context-switch depth 1024, "improves decoding throughput by allowing the accelerator to multiplex across multiple independent decoding tasks"). This would make decoding a *many-accelerator* problem in the trivially parallel sense — closer to a rack of independent NICs than to an HPC job. C(P) ≈ 0. This is also the regime the micro-blossom README's "at most 110 logical qubits (d=9, p=0.001) while achieving the throughput requirement of 1 million measurement rounds per second" claim appears to describe — but note that claim is `[code]` only and contradicts the paper's own "supports a single logical qubit."

2. **Lattice surgery — where independence breaks.** During a merge, patches' decoding graphs fuse and the decode problem genuinely spans multiple logical qubits within a window. Micro Blossom names this as required future work: "dynamic inter-block fusions, which complements the intra-block fusion", governed by "an operating system-like controller". If a merged block's graph exceeds one device's capacity, the fusion must cross a device boundary *inside* the window, and C(P) enters the inner loop rather than sitting between windows. RESCQ's benchmarks (13–420 program qubits, thousands of CNOTs, each a lattice-surgery merge) indicate merges are not rare events.

3. **Distance growth past single-device capacity.** Micro Blossom is at 867k of 900k LUTs at d=15 on the largest board it used. The chiplet codesign paper's application study uses **d=27**. If d≥21–27 is required for algorithmic-scale error rates, one logical qubit's decoding graph (Θ(d³): d=27 is ~9× the vertices of d=13) does not fit one device, and partitioning a *single* logical qubit's graph across devices becomes mandatory. That is the point at which the problem acquires a real C(P) term with a hard deadline — a genuinely HPC-shaped structure.

4. **Bandwidth.** Micro Blossom's "load and route syndrome data at Terabit/s" is the only aggregate-bandwidth figure in the corpus, and it points at a data-movement problem of HPC scale even before any compute is distributed. Note also that the earlier decoder generation (Clique, Lazy) was motivated substantially by *bandwidth* reduction rather than latency; Micro Blossom's critique of them is on accuracy, leaving the bandwidth motivation intact and unaddressed by its own design.

### What would prevent the transition — the C(P) term against the budget

- **The budget itself.** ~1 µs total; ~0.8 µs measured for compute + local I/O at d=13; controller I/O separately estimated at >0.8 µs. There is no room for a network round trip inside a window at superconducting rates. Any multi-node scheme must therefore make cross-node communication *pipelined across windows* rather than *synchronous within* one — which is precisely what the speculative/parallel-window line (SWIPER, Triage, Snowflake) is doing, and which changes the problem from "distribute one decode" to "overlap many decodes and repair speculation".
- **The serial residue.** The primal phase stayed in software. Any distributed variant inherits an irregular, dynamically-allocated, sequentially-dependent phase that neither vectorises nor decomposes cleanly. Promatch's steps 2–4 have the identical property (each match mutates the syndrome, so the next candidate depends on the previous). Two independent designs, two different algorithms, the same shape of residue — that is evidence about the problem, not about the implementations.
- **Exactness has superlinear worst case.** O(d⁹) even after Θ(d³)-way parallelisation. Holding LER parity (Micro Blossom's whole value proposition) means you cannot escape this by approximating; approximating (Promatch's route) means the accuracy becomes p- and d-dependent in the way Micro Blossom criticises.
- **Determinism requirements.** Under Promatch's hard-deadline model, a distributed decoder needs bounded *worst-case* communication, not good average communication. Almost nothing in commodity interconnect gives that.

### The conditions that would make it easy instead

- **Slower platforms.** Trapped-ion measurement at **400 µs** (Jones & Murali) is a ~400× budget expansion. At that budget, exact MWPM at d=13 runs in software on one core with three orders of magnitude of margin, and even a distributed decoder has ample room for C(P). Whether decoding is an architecture problem may be a property of the *qubit modality* rather than of QEC.
- **Algorithm class change.** The qLDPC papers here (HetEC's gross code, PropHunt's LP/RQT codes, AlphaSyndrome's bivariate bicycle, ACQC) imply **BP / BP+OSD** rather than matching. Message passing over a sparse factor graph is bulk-synchronous and maps to conventional parallel machines far more naturally than blossom's dynamic forests — but it is iterative with data-dependent convergence, which converts a bounded-work problem into an unbounded-iterations one. None of these four papers analyses that decoder cost; HetEC in particular adopts the gross code and abstracts decoding into a fixed "logical clock speed".
- **Compile-time offloading.** AlphaSyndrome and PropHunt both reduce the runtime decoder's burden by construction — AlphaSyndrome explicitly optimises for "the decoder's correctable region" under "strict time constraints". Pushing work from the microsecond-deadline runtime into an hours-long offline MaxSAT/MCTS search is a way of *avoiding* the scale-out question rather than answering it, and it is where ASPLOS 2026's QEC papers actually went.

### Open questions this corpus leaves stated but not settled

- At what (d, logical-qubit-count, merge-frequency) triple does inter-block fusion force a cross-device synchronous exchange inside a decoding window?
- What is the worst-case, not average, latency of a parallel-window scheme, and does it satisfy the hard-deadline reading of the constraint or only the soft-deadline reading?
- Is the Terabit/s syndrome data plane a decoder-placement problem (cryogenic/near-fridge) or a network problem? No paper in this set addresses decoder placement; Promatch does not mention the cryostat at all.
- Does the accuracy penalty of approximation (Promatch's route) scale better or worse than the silicon penalty of exactness (Micro Blossom's route) as d goes to 21–27? Both papers stop below that.
- How do the super-stabilizers of the chiplet codesign paper change the decoding graph's cost, and what does that do to either decoder's budget?

## 4. NISQ vs FTQC framing, and the 2024 → 2026 shift

| # | Paper | Year | Tag | Basis |
|---|---|---|---|---|
| 1 | Promatch | 2024 | `EARLY_FTQC` | 1 logical qubit, d≤13, p=10⁻⁴–5×10⁻⁴ (below current hw), motivated by <10⁻¹² application targets |
| 2 | Micro Blossom | 2025 | `EARLY_FTQC` | 1 logical qubit ("as reported here supports a single logical qubit"), d≤15, p=0.1%, logical T̂ gate motivation |
| 3 | RESCQ | 2025 | `EARLY_FTQC` | explicit: "near-term FTQC regime, where we have about 1-2 orders of magnitude improvement in the logical error rates" |
| 4 | HetEC | 2025 | `FTQC` | full algorithm execution, 10³–10⁴ physical qubits, gross-code memory hierarchy |
| 5 | QECC-Synth | 2025 | `EARLY_FTQC` (NISQ hardware constraints) | targets degree-2/3 real devices and defective qubits; small codes |
| 6 | Chiplet codesign | 2024 | `FTQC` | d up to 27, Shor's algorithm, 2.1×10⁷–7.6×10¹² physical qubits, ~25 billion cycles |
| 7 | AlphaSyndrome | 2026 | `GENERAL` / `EARLY_FTQC` | code-family-agnostic; IBM Brisbane current-device noise; fault-tolerant code families |
| 8 | PropHunt | 2026 | `EARLY_FTQC` / `GENERAL` | small-to-mid codes, qLDPC families, circuit-level p=0.1% |
| 9 | ACQC | 2026 | `FTQC` `[abstract]` | qLDPC FTQC baseline, magic state distillation |
| 10 | iSwitch | 2026 | `NISQ` → `EARLY_FTQC` transition | baselines literally named "NISQ-Bare" and "MSD-Logical"; selective encoding is the transition mechanism |
| 11 | Trapped ion + surface codes | 2026 | `EARLY_FTQC` | d 2–20, hardware-limited QCCD, logical clock speed as the metric |

**The shift, 2024 → 2026.** Three movements are visible and they are not the same movement.

- **Subject matter moved off the decoder.** 2024–2025 ASPLOS carried the two decoder-microarchitecture papers plus one real-time-scheduling paper. ASPLOS 2026's five QEC papers contain no decoder design; the decoder-acceleration line continued at ISCA (SWIPER'25, Triage'26, Coset Ensemble'26), EuroSys, IEEE QCE, and arXiv.
- **Code family moved off the surface code.** 2024 is pure surface code (Promatch, chiplet codesign). 2025 introduces qLDPC as a first-class object (HetEC's gross code). 2026 is majority-qLDPC (ACQC, and both AlphaSyndrome and PropHunt evaluate LP/RQT/bivariate-bicycle families alongside surface). This matters for the census's central question because it silently changes the decoder algorithm class from matching to belief propagation, **without any of these papers analysing the resulting real-time decoder cost.**
- **The abstraction level moved earlier in the toolchain.** 2024–2025: runtime hardware (Promatch's FPGA, Micro Blossom's accelerator, RESCQ's runtime scheduler). 2026: compile-time synthesis (AlphaSyndrome's MCTS, PropHunt's MaxSAT, QECC-Synth's MaxSAT, ACQC's layout co-design). The deadline pressure did not go away; the response migrated from meeting it with hardware to reducing it at compile time.

Framing-wise, no paper in the set is `NISQ`-only, and only iSwitch and QECC-Насynth anchor to present-day devices. The centre of mass is `EARLY_FTQC`: single-to-few logical qubits, d ≤ 15, error rates at or just below current hardware. The two `FTQC` papers (chiplet codesign, HetEC/ACQC) are the ones that reason about 10⁷+ physical qubits — and they are exactly the ones that do not model decoding.

---

## Evidence-level summary table

| Paper | Headline claim | Evidence tag(s) | Caveat |
|---|---|---|---|
| Promatch | "960 ns worst case at d=13"; LER 3.4×10⁻¹⁵ = MWPM parity | `RTL_SYNTHESIS` (utilization/freq) + `ANALYTIC_MODEL` (ns from cycle counts × 4 ns) + `SOFTWARE_SIMULATION` (LER, Stim) | **Not a measured latency.** No board execution. No HDL in public artifact. Parity holds only for the `‖ Astrea-G` config and only at p=10⁻⁴ |
| Micro Blossom | "0.8 µs average at d=13, p=0.1%, 8× vs Sparse Blossom" | `FPGA_PROTOTYPE` (measured on VMK180, includes CPU↔FPGA I/O) + `SOFTWARE_SIMULATION` (syndromes from noise model, not a quantum device) + `PROJECTED` (ASIC remark) | **Average, not worst case.** Software baseline excludes controller I/O the paper estimates at >0.8 µs. Single logical qubit |
| RESCQ | "2× geomean cycle count" | `ARCH_SIMULATION` + `SOFTWARE_SIMULATION`; 100 µs MST is a laptop measurement / `ANALYTIC_MODEL` | No hardware proposed or built |
| HetEC | "6.42× physical qubit reduction, 3.43× time" | `SOFTWARE_SIMULATION` + `ANALYTIC_MODEL` (two-step LER substitution; some LERs imported) | Decoding not modelled |
| QECC-Synth | "74.9% fewer extra CNOTs vs Sabre" | `SOFTWARE_SIMULATION` (MaxSAT + circuit metrics) | Compile-time only |
| Chiplet codesign | "<3×/6× overhead at 1% defects" | `SOFTWARE_SIMULATION` (Stim + Monte Carlo + fitted ansatz) | Decoder cost of super-stabilizers not analysed |
| AlphaSyndrome | "80.6% average LER reduction" | `SOFTWARE_SIMULATION` (Stim, IBM Brisbane params) | Decoder-aware but cites no hardware decoder |
| PropHunt | "2.5–4× lower LER on LP/RQT"; parity on surface | `SOFTWARE_SIMULATION` (Stim, PyMatching/BP-LSD) | Artifact exists but I did not inspect it |
| ACQC | "4.4× speedup, 18.3× qubit reduction" | **undetermined** — `[abstract]` only | No preprint; ACM DL blocked; open access, retrievable elsewhere |
| iSwitch | "8.0× vs NISQ, 15.5× vs MSD-Logical" | `SOFTWARE_SIMULATION` (Qiskit-Aer + Stim/PyMatching) | Preprint titled "Flexion", differing author list |
| Trapped ion | "3.8× logical clock speed" | `SOFTWARE_SIMULATION` + `ARCH_SIMULATION` (Stim + custom compiler) | No decoding discussion despite 400 µs measurement budget |

**The one distinction to carry forward above all others**: Promatch's 960 ns is a cycle-count projection at an assumed 250 MHz; Micro Blossom's 800 ns is a measured board average at 62 MHz including I/O. Everything else in the corpus is software simulation.

Sources: [Promatch arXiv](https://arxiv.org/abs/2404.03136) · [Promatch HTML](https://arxiv.org/html/2404.03136v1) · [Promatch code](https://github.com/nargesalavi/Promatch) · [Micro Blossom arXiv](https://arxiv.org/abs/2502.14787) · [Micro Blossom HTML](https://arxiv.org/html/2502.14787v1) · [micro-blossom code](https://github.com/yuewuo/micro-blossom) · [RESCQ arXiv](https://arxiv.org/abs/2408.14708) · [RESCQ code](https://github.com/5ayam5/Realtime-Scheduling-for-Continuous-Angle-QEC-Architectures) · [HetEC arXiv](https://arxiv.org/pdf/2411.03202) · [QECC-Synth arXiv](https://arxiv.org/abs/2308.06428) · [Chiplet codesign arXiv](https://arxiv.org/abs/2305.00138) · [AlphaSyndrome arXiv](https://arxiv.org/html/2601.12509v2) · [PropHunt arXiv](https://arxiv.org/abs/2601.17580) · [iSwitch/Flexion arXiv](https://arxiv.org/abs/2504.16303) · [Trapped ion arXiv](https://arxiv.org/abs/2510.23519) · [ACQC ACM record](https://dl.acm.org/doi/10.1145/3779212.3790122) · [SNU HPCS publications](https://hpcs.snu.ac.kr/publications/)
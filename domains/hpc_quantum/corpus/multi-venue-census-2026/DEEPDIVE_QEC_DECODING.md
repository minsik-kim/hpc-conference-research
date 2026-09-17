# Deep Dive — QEC Decoding as a Classical Workload (paper ↔ code cross-validation)

**Performed 2026-09-17.** Eight papers from ISCA, MICRO, HPCA (2024–2026), four with repositories
cloned and read. Consistency vocabulary: `CONSISTENT` / `PARTIAL_MATCH` / `MISMATCH` /
`INSUFFICIENT_EVIDENCE`. Evidence tags: `[paper]` `[code]` `[artifact]` `[documentation]`
`[reconstruction]` `[inference]`.

**Access limits:** Zenodo *file* downloads are egress-blocked (record metadata readable), so
gladiator's and Flag-Proxy Networks' archived artifacts were not read; IEEE/ACM/dblp blocked as usual.

## 1. SWIPER (ISCA 2025) — `CONSISTENT`, with a scope correction

**Repo:** `github.com/jviszlai/swiper`, Python; the `swiper/` package is 3,677 LOC in total, of which
3,271 sit in `decoder_manager.py`,
`device_manager.py`, `window_manager.py`, `window_builder.py`, `lattice_surgery_schedule.py`,
`predictor.py`, `simulator.py`; `artifact/` holds six experiment drivers plus pre-generated data and
figures; five pytest modules. `run_analysis.py` regenerates every data figure from shipped data in
~5 min; full regeneration needs a SLURM cluster (~3,000 jobs). **Reproducible-in-principle: yes.**

**The central methodological finding** `[code]`: **SWIPER-SIM is a round-level discrete-event
simulator, not a syndrome-level decoding simulator.** The main loop never calls a decoder. PyMatching
latency is measured *offline* (`artifact/run_pymatching_latencies.py`: `d_range = [13..31]`,
`p = 1e-3`, `stim.Circuit.generated("surface_code:rotated_memory_z", ...)`, 10,000 shots, timed on an
M1 MacBook Pro), and speculation success is **stochastically modeled** inside `DecoderManager.step()`
rather than computed from syndromes. Predictor accuracy is measured separately and fed in as the
scalar `speculation_accuracy`.

**This supports inner-decoder-agnosticism more strongly than the paper's own phrasing.** The inner
decoder enters only as a latency distribution or a lambda: `run_reaction_time_evals.py` passes
`[f'lambda volume: volume*{fac}' for fac in np.geomspace(0.1, 10, 10)]`, matching the project page's
stated model `t_dec(v) = r·v/d²` with `fac = r/d²`. PyMatching 2 is the *characterized* inner decoder,
not an inline component.

**Speculation/rollback matches the branch-prediction analogy concretely** `[code]`: `DecoderTask`
carries `completed_speculation`, `speculation_start_time`, `used_parent_speculations`,
`speculation_modifiers`; on a miss, `poison_policy ∈ {'successors','descendants'}` selects the blast
radius and `_reset_decode_task()` / `_reset_speculate_task()` perform the rollback; correlated failure
is modeled by multiplying adjacent faces' modifiers by `missed_speculation_modifier` (default 1.4);
rollback is DAG-based via `networkx`.

**★ Scope correction to carry forward.** **d = 13–31 is the PyMatching latency-characterization range
only.** The full SWIPER-SIM benchmark sweep is `'distance': [15, 21, 27]` and the reaction-time sweep
is **d = 21 alone**. Any statement that SWIPER "evaluates d = 13 to 31" is wrong.

The **60 ns constant-time predictor / AMD Vivado behavioral simulation** is
`INSUFFICIENT_EVIDENCE at code level`: no HDL, `.xpr` or Vivado scripts exist in the repo. But
`artifact/data/fpga_data.json` ships the synthesis *results* — `ds = [3,5,7,9,13,17,21,25,27]`,
`luts = [1226, 5931, 23540, 50264, 106684, 323497, 698745, 1194324, 1534392]`, `regs = [500 … 126308]`
— compared in `plot_7()` against hardcoded **Helios** (d = 9,13,17,21; LUTs 52,111 → 898,715) and
**Micro-Blossom** (d = 3–15; LUTs 4,000 → 867,000) literature tables. The 60 ns figure itself is not
in the repo.

The **"relaxes the 1 µs requirement, tolerates 2–5× longer decoder latency at equal reaction time"**
claim is `PARTIAL_MATCH`: the apparatus is unambiguously present (a 100× geometric sweep of decoder
latency at fixed d = 21 against `'sliding'`, `'parallel'` and `'aligned'` scheduling), so the claim is
extractable from shipped data, but the paper body could not be fetched and the "2–5×" figure was not
independently confirmed.

**Modality:** ARCH_SIMULATION (round-level discrete-event) + SOFTWARE_SIMULATION (offline Stim/
PyMatching characterization) + RTL_SYNTHESIS (predictor LUT/register data, results only).

## 2. Pinball (HPCA 2026) — `PARTIAL_MATCH`

**Title correction:** *"A Cryogenic Predecoder for **Surface Code** Decoding Under Circuit-Level
Noise"* — not "QEC Decoding".

**Repo:** `github.com/aknapen/Pinball`, 57 files. Two SystemVerilog files — `verilog/pinball.sv`
(669 lines) and `verilog/leaf_decode.sv` (21 lines) — plus a Python model (`src/predecoders.py`, 625
lines), four experiment drivers, and 40 `.pkl` metadata files under `metadata/d={3…21}/`.
**No plotting scripts, no synthesis scripts, no testbench, no constraints files.**

**Verified in RTL** `[code]`:
- **Nine sequential pipeline stages — CONFIRMED**, comment-delimited: (1) measurement error
  (time-like); (2–5) bulk data errors in four directions; (6–7) top-right/top-left **spacetime**
  checks; (8) **hook** errors; (9) edge data errors. This corroborates the circuit-level-noise claim
  directly.
- **O(d²) scaling — CONFIRMED structurally:** `NUM_ROWS = CODE_DISTANCE+1`,
  `NUM_COLS = (CODE_DISTANCE−1)/2` → `(d²−1)/2` ancillas, i.e. one stabilizer basis of a rotated
  surface code. **A full deployment covering both bases doubles this.**
- The primitive is genuinely trivial — `assign correction[i] = center_in * neighbor_in;` then
  `center_out = center_in ^ correction` — a two-stage combinational AND/XOR cell replicated by
  `generate` blocks, consistent with "lightweight cryogenic logic".
- The Python model executes the same error classes in the same order (`_clear_measurement_errors` →
  `_clear_bulk_data_errors` → `_clear_spacetime_errors` → `_clear_hook_errors` →
  `_clear_edge_data_errors`), giving strong model↔RTL agreement.

**Two code-level observations, reported without overclaiming** `[code]`: (1) in the current-syndrome
`always_ff` block of `pinball.sv`, an `if … else` spans two statements without `begin`/`end`, which
*appears* to be a syntax error — no Verilog toolchain was available to confirm, so this is flagged as
an observation, not a finding; (2) `Pinball.decode()` hardcodes `iscomplex = 0` while the RTL drives a
real `complex_out`, a model/RTL divergence in the complex-syndrome escape path.

**The hardware-claims half is absent from the repo.** A full-repo grep for
`bandwidth|promatch|power|mW|nm|4 K|LUT|area|throughput` returns **only README prose**. There is no
power model, no area model, no bandwidth accounting and no Promatch baseline. **0.56 mW, 22.2×, 67.4×,
3780.72×, 32.58× and the 2,668-logical-qubit figure are therefore not reproducible-in-principle from
this artifact.** What *is* reproducible: logical-error-rate comparison (Pinball+MWPM vs Clique+MWPM vs
MWPM-only), L1 statistics, chain-length distribution, error-frequency distribution.

**★ Measurement context — two headline numbers circulate without their qualifiers** `[paper]`:
- **3780.72× syndrome-bandwidth reduction is at d = 5, p = 10⁻⁴** versus no predecoding. *Not* at
  d = 21, *not* at p = 10⁻³. (At d = 3 Pinball achieves full coverage.)
- **32.58× lower logical error rate than Promatch is at d = 11, p = 5×10⁻⁴**, with a companion 5×
  against Promatch‖Astrea-G. The abstract says 32.58× where one body sentence read 32.38×;
  `INSUFFICIENT_EVIDENCE` on which is correct — the abstract value is recorded as authoritative.
- The ~6-orders-of-magnitude figure is versus **Clique**, the prior state-of-the-art *cryogenic*
  predecoder.

**Noise model** `[code]`: `SI1000NoiseModel(p)` from `qLDPC==0.2.6` over
`stim.Circuit.generated("surface_code:rotated_memory_x", ...)`, PyMatching 2.3.1, stim 1.15.0.
**SI1000, not uniform depolarizing** — this matters for every cross-paper comparison.

**RTL synthesis, not silicon — CONFIRMED** `[paper]`: standard cells were re-characterized with a
commercial 4 K device model, after which synthesis, placement and routing were performed.
**Modality: RTL_SYNTHESIS (hardware claims) + SOFTWARE_SIMULATION (accuracy claims).**

## 3. BP-SF (HPCA 2026) — `CONSISTENT`; the cleanest sequential→parallel evidence in the corpus

**Repo:** `github.com/Dies-Irae/BP-SF`, 32 files. `mybp.py` (322 LOC, the decoder), `benchmark.py`
(timing harness), `gpu_est.py`, `codes_q.py` (BB code construction), `build_circuit.py` (circuit-level
Stim + `dem_to_check_matrices`), `plots.ipynb`, shell drivers. `minimal_bp_decoder/` is a **modified
fork of `quantumgizmos/ldpc`** whose key addition is exposing `bpd.oscillation_counts`.
**Reproducible-in-principle: yes**, at the cost of days on 16 cores.

**Is the post-processing genuinely embarrassingly parallel? YES** `[code]`. In `decode_worker(...)`
each worker builds its **own** `BpDecoder` and then, per candidate:
`test_syndrome = compute_syndrome_sparse(pcm_csc, test_pos)` →
`new_syndrome = np.remainder(syndrome + test_syndrome, 2)` → `decoded = bpd.decode(new_syndrome)`.
**No cross-candidate data dependency.** The only inter-worker communication is chunk distribution over
`input_queue` plus `solution_found_event`, a pure early-abort optimization. This is a real replacement
of BP-OSD's sequential Gaussian elimination with independent parallel work.

**Parallel degree is bounded** `[code]`: `candidates = np.argsort(oscillation_counts)[-topk:]` then
`all_combs = [sample_n_choose_k(candidates, w, n_sample) for w in range(w_min, w_max+1)]`. With the
shipped `[[144,12,12]]` settings (`topk=50, w_min=1, w_max=10, n_sample=10`) that is **at most 100
candidate flip vectors**; for `[[72,12,6]]` (`topk=20, w_max=4, n_sample=5`) it is ≤20.

**Latency is wall-clock, single-sample, CPU** `[code]`: `benchmark.py::test_sample` wraps each
individual decode in `time.time()`. So "~70% of BP-OSD" is **BP-SF at 1 process vs `ldpc` BP-OSD**,
and "55% average / 18% max" are **8 processes vs 1 process**. Not modeled, not cycle-counted.

**Two caveats the code reveals** `[code]`: (1) `gpu_est.py` does **not** measure parallel GPU decoding
— it constructs a batch-capable `nv-qldpc-decoder` with `bp_batch_size=1000` but then iterates
candidates **sequentially**, and drops samples where the NVIDIA and CPU decoders disagree on
convergence from the timing average; (2) **parallel and serial modes are not semantically identical**
— serial scans candidates in ascending weight and returns the first converging one, parallel returns
whichever worker converges first in wall-clock, which need not be the lowest-weight candidate, so LER
at P = 8 and P = 1 can differ slightly and the repo does not control for it.

**Context** `[code]`: BB codes `[[72,12,6]]`, `[[144,12,12]]`, `[[288,12,18]]`, plus coprime-BB
`[[126,12,10]]` and `[[154,6,16]]`; p ∈ {1e-4 … 1e-2}; `max_iter=100`, `bp_method="ms"` (min-sum);
circuit-level noise, `num_repeat = d`, z-basis. Headline claims are `[[144,12,12]]`-specific.

## 4. Coset Ensemble Decoder for Quantum Error Correction (ISCA 2026) — `PARTIAL_MATCH`

**Repo:** `github.com/IMSeonL/coset-ensemble-decoder`, 60 files, **all Python**.
**★ `hardware_code/` contains only `.gitkeep`**, and the README states *"Verilog RTL will be released
in `hardware_code/` soon"* and *"No GPU, FPGA, or quantum hardware required."* **The 8.2× LUT
reduction is therefore not reproducible-in-principle from this repo** — and the paper's own wording is
careful: "compared with **reported** UF-based decoder resources", i.e. a literature-table comparison,
not a head-to-head re-synthesis. **Modality is CYCLE_SIMULATION, not FPGA_PROTOTYPE.**

**Temporal reuse — CONFIRMED in structure, with a caveat in the accounting** `[code]`. The ensemble
loop re-invokes one modeled spanning-tree module and one peeling module **sequentially**
`num_candidates` times — temporal reuse, not spatial replication. **However**, cycle accounting
reports `max_ST_cycle = max(...)` and `max_Peeling_cycle = max(...)` **across** candidates, not the
sum. If hardware truly reuses one module across 24 candidates, total latency should be the sum (or a
pipelined equivalent). Reporting the max is the accounting a *spatially parallel* array would use.
Without the paper body this is `PARTIAL_MATCH` / `OPEN_QUESTION`, possibly resolved by a pipelining
assumption the paper states and the code does not encode.

**Multi-bank memory hashing — CONFIRMED** `[code]`, concretely and numba-JIT: vertices in
**`V_M = 22`** banks under `bank_hash(x,y,z) = (1·x + 3·y + 5·z) % 22` with a precomputed
`V_ADDR_LUT` and `V_MAX_PER_BANK = 188`; edges in **`E_M = 9`** banks hashed `x % 9`; conflict
detection via `has_duplicate_banks`; concurrent-access primitives `vertex_read_with_neighbors_jit`
and `vertex_write_with_neighbors_jit`. "Hierarchical ID mapping" is `group_union(...)`, a two-level
cluster-ID → group-ID DSU with explicit modeled latency. Pipeline stalls are tracked
(`num_stalls`, `cluster_stalls`, `cluster_busy`).

**Scaling limit visible in code** `[code]`: `V_L_MAX = 16`, `V_R_MAX = 16` are module-level constants
sizing the bank tables — consistent with the L = 3–11 evaluation but not extensible without editing.

**Context** `[code]`: `--list_size 24` (24 ensemble candidates) in all run scripts; L ∈ {3,5,7,9,11};
p ∈ {0.0005 … 0.0015}; Stim circuit-level depolarizing; 60K–40M shots per point. Randomized priority
functions make exact numeric reproduction impossible **by design** — the README asks reviewers to
verify *ordering* (UF > Ours ≥ MWPM), not values. Helios and Micro-Blossom latency baselines are
**hardcoded published tables**, not re-runs. `software/peeling_efficient.py` is **0 bytes** despite
being listed in the project tree and gated by a config flag.

## 5. gladiator (MICRO 2025) — `CONSISTENT` at paper level, `INSUFFICIENT_EVIDENCE` at code level

Zenodo `10.5281/zenodo.16735148` confirmed to exist (single file `GLADIATOR-Artifact.zip`, 12.2 MB),
but **file download is egress-blocked**, so the code was not read.

All numeric claims verified verbatim from the arXiv HTML `[paper]`: **≤100 ns budget** ("leakage
detection must complete for all d² data qubits within 100 ns — the approximate latency of four CNOTs
on superconducting platforms like Google's"); **1 ns** evaluation; **at most 10 LUTs per data qubit**;
**70 LUTs at d = 25 for 625 data qubits** via `LUTs_total = 10 × ⌈d²/100⌉`; **17×–80× less resource
than ERASER across d = 5→25**; up to 3× (avg 2×) fewer unnecessary LRCs; 1.7–3.9× speedup; 16%
relative LER reduction; d ∈ {5,7,9,11,13,17,19,25}, p ∈ {10⁻³, 10⁻⁴}, leakage ratio
lr ∈ {0.01, 0.1, 1.0}. **FPGA synthesis only — confirmed**: same Kintex UltraScale+
xcku3p-ffvd900-3-e as ERASER, whose design was **re-synthesized** for larger distances for fairness.
Built by modifying the ERASER artifact; Stim's Tableau simulator extended for leakage.

**Internal-consistency note worth carrying** `[inference]`: "10 LUTs per data qubit" and "70 LUTs for
all 625 data qubits at d = 25" reconcile **only** via ~100× time-multiplexing — 10 LUTs serving 100
data qubits, each evaluated in 1 ns inside the 100 ns budget. Consistent, but only under that reading;
taken literally the per-qubit figure would give 6,250 LUTs.

## 6. Vegapunk (MICRO 2025) — `INSUFFICIENT_EVIDENCE` (no artifact)

Re-check confirms no public artifact: the authors' JanusQ GitHub organization hosts `rasengan`,
`Choco-Q`, `qldpcCircuit` and `QuCT-Micro2023` but **no Vegapunk repository**; `api.github.com` was
unreachable through the proxy, so this is `NO_PUBLIC_ARTIFACT_FOUND`, not proof of absence.
**Full title recovered**, including the subtitle the Phase-1 record omitted: *"…with Online
Hierarchical Algorithm and Sparse Accelerator"*. All performance claims remain `[paper]`-only.
Per-code latencies, speedups and baselines are recorded in `CENSUS_MICRO_2024_2026.md`.

## 7. Flag-Proxy Networks (MICRO 2024) — `CONSISTENT` with the corrective characterization

**The "QLDPC decoding hardware" label is wrong and should be corrected wherever it appears.**
The Zenodo artifact (`10.5281/zenodo.13325358`, `fpns_micro24.tar.gz`, 18.6 MB, MIT) could not be
downloaded, so the first author's framework `github.com/suhaskvittal/qontra` — on which the artifact
is built — was cloned instead `[code]`:
- **Zero HDL.** A repo-wide search for `*.v`, `*.sv`, `*.vhd`, `*.xdc`, `*.tcl` returns **nothing**.
  It is C++20 + CMake + OpenMPI with **modified Stim and modified PyMatching vendored**.
- Decoders are software: `src/qontra/decoder/{mwpm,pymatching,restriction,mobius,concat_mwpm,
  chromobius,neural}.cpp` — **MWPM and restriction, exactly as the census asserts.**
- The FPN architecture is in `src/protean/network/{physical,raw}.cpp` and `scheduler.cpp`, where
  qubit roles are an enum `{ data, xparity, zparity, flag, proxy }` and `add_proxy` is documented as
  *"The proxy qubit splits the edge between the two input qubits"* / *"Reduces connectivity by adding
  proxy qubits."*

So the "hardware" is a **qubit connectivity architecture** plus a greedy syndrome-extraction
**scheduler**, and all reported results are software simulation. *Caveat:* `qontra` is the authors'
general framework, not literally the archived artifact; it corroborates the characterization rather
than being the artifact itself `[code]` `[inference]`.

## 8. Triage (ISCA 2026) — resource model extracted, `[paper]` throughout

- **Slice** = the spatio-temporal unit: *"A slice S(t,p) represents the syndrome data generated from a
  single square logical patch at position p during a d-rounds syndrome measurement cycle t."*
- **Decoder pool** = **M physical decoders servicing N logical qubits, M ≤ N**; each decoder processes
  one slice at a time.
- **Decoder latency model**: `t_decode = A · volume^α` with **α = 1.17**, empirically fitted to
  PyMatching. Decoders are additionally parameterized by a speed relative to syndrome generation;
  configurations tested are **0.8 (slow)** and **1.8 (fast)**.
- **Backlog condition**: `τ_dec < τ_gen` must hold or syndrome backlog grows **exponentially** and
  logical operations stall.
- **Scheduling formulation**: assignment `π: V' → {1..M}` of pending slices to available decoders,
  subject to (a) `V'` being an **independent set** in the constraint graph and (b)
  `|V'| ≤ M_available`; objective = minimize total idle syndrome layers inserted when synchronizing
  Pauli frames at critical operations.
- **Dual mode**: a cost-efficient heuristic scheduler in steady state plus a **priority-aware
  emergency mode** resolving the **causal cone** of a critical operation.
- **Context**: d = 9 Monte Carlo extrapolated to d = 21; p = 3×10⁻³ depolarizing; circuit-level noise
  via Stim; 15 application benchmarks at T-gate density 7.69–49.61%. **52.6% average LER reduction**
  vs time-parallel-only window decoding under resource-constrained scenarios.
- **Modality**: ARCH_SIMULATION (custom Python 3.9 discrete-event simulator) + SOFTWARE_SIMULATION.

## A. Decoding latency budget table

| Paper | T_decode (stated) | Cycle budget | Syndrome rate / bandwidth | Code distance | Hardware target |
|---|---|---|---|---|---|
| SWIPER | modeled `t_dec(v) = r·v/d²` rounds; PyMatching measured at d = 13–31, p = 1e-3 | 1 µs per round asserted as the conventional requirement, which the paper's thesis relaxes | `UNKNOWN` | 13–31 (characterization); 15/21/27 (system); **21 (primary)** | room-temp decoder pool; predictor LUT/reg data only |
| Pinball | pipeline occupancy **max 800 ns over 9 clock cycles**; **100 ns** allocated to predecoding (10% of budget) | **1 µs** per round (superconducting) | up to **3780.72× reduction** at d = 5, p = 1e-4 vs no predecoding; **absolute rate UNKNOWN** | 3–21 odd | 22 nm FDSOI, 4 K-recharacterized cells, synth + P&R; peak < 0.56 mW; **1.5 W 4 K budget → 2,668 logical qubits at d = 21** |
| BP-SF | wall-clock ms-scale CPU; ~70% of BP-OSD at P=1; −55% avg, −82% max at P=8 | not stated | `UNKNOWN` | `[[144,12,12]]` etc. (qLDPC — no surface-code d) | CPU multiprocessing; GPU path sequential |
| Coset Ensemble | modeled cycles; "sub-microsecond" per README; absolute ns `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | L = 3–11 | FPGA claimed; **RTL not released** |
| gladiator | **1 ns** per classification | **100 ns** ("four CNOTs") | `UNKNOWN` | 5–25 | Kintex UltraScale+, **synthesis only**; 70 LUTs at d = 25 |
| Vegapunk | 720–840 ns BB (avg 756), 264–526 ns HP (avg 412) | sub-µs target | `UNKNOWN` | qLDPC (BB, HP) | Alveo U50 @ 250 MHz, HLS C++ |
| Flag-Proxy Networks | **none — no hardware decoder** | — | — | hyperbolic d = 3–12 vs d = 5 planar | none (software) |
| Triage | `t_decode = A·volume^1.17` fitted to PyMatching; decoder speeds 0.8× and 1.8× relative to syndrome generation | condition `τ_dec < τ_gen`; absolute τ_round `UNKNOWN` | `UNKNOWN` (modeled as slices/round) | d = 9 measured, 21 extrapolated | **M decoders for N logical qubits, M ≤ N** |

**`UNDEREXPLORED_IN_THIS_CORPUS`: no paper states a syndrome bandwidth in absolute units (bits/s).**
Every bandwidth claim in the corpus is a ratio. The bandwidth axis of the "QEC decoding is an HPC
problem" thesis therefore **cannot be quantified from this corpus alone** — the one absolute figure
available anywhere in the domain is ISC 2024's **2–500 Gbps** estimate (Camps et al.), which comes
from a resource-estimation paper, not a decoder paper.

## B. Decoder algorithm family map

| Paper | Venue / Year | Families | Code family |
|---|---|---|---|
| Flag-Proxy Networks | MICRO 2024 | MWPM, **restriction** | hyperbolic surface + color |
| SWIPER | ISCA 2025 | **windowed + speculative**; MWPM (PyMatching 2) as pluggable inner | surface / lattice surgery |
| gladiator | MICRO 2025 | **speculation/classification** (leakage, not syndrome decoding); decoder-agnostic | surface, color, qLDPC |
| Vegapunk | MICRO 2025 | **BP + hierarchical**, sparse accelerator; baselines BP+LSD, BPGD, BP+OSD | **qLDPC** (BB, HP) |
| BP-SF | HPCA 2026 | **BP + parallel speculative post-processing** (Chase-style), replacing BP-OSD | **qLDPC** (BB, coprime-BB) |
| Pinball | HPCA 2026 | **predecoder** (cryogenic), MWPM as second level | surface |
| Coset Ensemble | ISCA 2026 | **union-find + ensemble** (coset-level approximate ML) | surface + toric + repetition |
| Triage | ISCA 2026 | **windowed + scheduling layer** over a decoder pool | surface / lattice surgery |

**The qLDPC turn is real but partial, and it is simultaneously an algorithm-family turn.** MICRO 2025
(Vegapunk) and HPCA 2026 (BP-SF) are squarely qLDPC decoding, and **both target BP-family algorithms
rather than matching** — because matching does not apply to general qLDPC codes. Meanwhile ISCA
2025/2026 (SWIPER, Coset, Triage) and HPCA 2026 (Pinball) remain surface-code. **The corpus is
bimodal, not migrated**: surface-code work concentrates on latency, scheduling and the cryogenic
boundary; qLDPC work on algorithmic throughput. `[inference]`

## C. Parallelism and crossover, per decoder family

Marked `[inference]` except where a number is cited. **Permitted vocabulary only** —
no gap is declared.

**MWPM / windowed (SWIPER, Triage).** Parallelism is spatio-temporal window decomposition; the work
unit is a window or a slice (one logical patch × d rounds). The synchronization term is explicit and
is the heart of both papers: windows form a **DAG of data dependencies**, so a distributed deployment
pays dependency-resolution latency between adjacent windows plus Pauli-frame synchronization at
critical operations. SWIPER converts the dependency wait into speculation-plus-rollback, where the
rollback blast radius is a tunable `poison_policy` `[code]` — **that blast radius is the distributed-
system communication term**, and SWIPER measures its cost directly. **`POSSIBLE_CROSSOVER`:** Triage
states the single-pool breaking condition as `τ_dec < τ_gen` with exponential backlog beyond it, and
with **α = 1.17 > 1** per-window volume growth outruns decoder speed — so the crossover to a larger
pool is driven by the **super-linear exponent**, not by qubit count alone.
**`UNDEREXPLORED_IN_THIS_CORPUS`:** none of these papers models inter-decoder *network* latency;
decoders are a pool with zero interconnect cost.

**Predecoder (Pinball).** Parallelism is fully spatial and local — `(d²−1)/2` leaf primitives
replicated by `generate`, each an AND/XOR on a stabilizer and one neighbour across 9 pipeline stages
`[code]`. There is **no synchronization term inside the predecoder at all**; it is embarrassingly
parallel by construction, which is exactly why it fits at 4 K. The binding constraint is **power and
bandwidth**, not parallelism. **`POSSIBLE_CROSSOVER`:** 1.5 W ÷ 0.56 mW ≈ 2,679, so the stated
**2,668 logical qubits at d = 21** is essentially the 4 K power budget divided by per-unit peak power
— meaning **the cryogenic tier saturates at a logical-qubit count, not at a code distance.** Past that
point one needs a second cryostat or a second power domain, and the syndrome stream is partitioned
across physical boundaries by construction. **This is the clearest hard physical boundary in the
corpus.**

**BP / BP-OSD (BP-SF, Vegapunk).** BP itself is parallel across check/variable nodes with a
communication-heavy message exchange per iteration — fine-grained, and a poor fit for distribution.
BP-SF's contribution sits one level up: its post-processing parallelism is **coarse-grained and
near-communication-free**, at most ~100 independent candidate decodes for `[[144,12,12]]`, each a
complete self-contained BP run on a locally-derived syndrome, with a first-to-finish flag as the only
synchronization `[code]`. **This is the corpus's best candidate for a genuinely distributable decoding
workload** — per-candidate payload is one syndrome vector and the reduction is an argmin.
**`POSSIBLE_CROSSOVER`:** the parallel degree is bounded at `(w_max − w_min + 1) × n_sample` = 100,
so throughput saturates at ~100 workers; beyond that, scaling must come from batching independent
*syndromes*, not candidates. **`OPEN_QUESTION`:** whether the P = 8 result — 55% lower average latency, with maximum latency
falling to as low as 18% of the single-process implementation — continues toward P = 100, and how the parallel-vs-serial candidate-ordering semantics affect
LER at high P — the repo does not test it.

**Union-find / ensemble (Coset).** Two orthogonal axes: cluster growth (irregular pointer-chasing,
poor for distribution) and ensemble candidates (24 independent forest explorations, embarrassingly
parallel like BP-SF's). The paper deliberately trades the *second* axis for area via temporal reuse —
the opposite of the distributed direction. **`OPEN_QUESTION`:** temporal reuse converts area into
latency, so the point at which one must return to spatial replication (or multiple devices) is where
`num_candidates × per-candidate latency` exceeds the round budget — but the repo's max-over-candidates
accounting does not expose that number, so it is `INSUFFICIENT_EVIDENCE` here.

**Two distinct crossover mechanisms are visible, and they are not the same thing:**
1. a **bandwidth/power crossover at the cryogenic boundary**, quantified only by Pinball
   (2,668 logical qubits at 1.5 W, d = 21);
2. a **throughput/backlog crossover at the decoder pool**, quantified only by Triage
   (`τ_dec < τ_gen`, α = 1.17).
SWIPER and BP-SF each attack a *latency* term rather than a crossover.

## D. Contradictions between papers

| # | Items | Classification | Basis |
|---|---|---|---|
| 1 | Pinball's 32.58× vs Promatch, against Promatch's own positioning | `DIFFERENT_REGIME` | Pinball's figure is at d = 11, p = 5×10⁻⁴ under **SI1000** noise, and Pinball's own abstract concedes it operates "under much stricter power and area constraints". Different thermal domain, noise model and (d,p) point. **Not a ranking.** |
| 2 | Pinball abstract "32.58×" vs one body sentence "32.38×" | `INSUFFICIENT_EVIDENCE` | Single fetch disagreement, not re-verified. Use the abstract value with the caveat. |
| 3 | Coset "sub-microsecond" vs Vegapunk "720–840 ns / 264–526 ns" vs Pinball "800 ns over 9 cycles" | `DIFFERENT_METRIC` **and** `DIFFERENT_REGIME` | Modeled cycles on surface/toric at L ≤ 11, versus HLS on an Alveo U50 at 250 MHz on qLDPC, versus a 22 nm FDSOI predecoder pipeline occupancy at 4 K on surface codes. Different codes, silicon and definitions of "latency". **These three numbers must not be ranked.** |
| 4 | Coset's README "lowest latency, sub-microsecond" vs its own max-over-candidates cycle accounting | `INSUFFICIENT_EVIDENCE` | Either the paper assumes pipelining the code does not encode, or the reported latency understates temporal reuse by up to 24×. Unresolvable without the paper body. |
| 5 | Coset and SWIPER both cite Helios and Micro-Blossom | `DIFFERENT_METRIC` | Coset compares *latency* against published tables; SWIPER compares *LUT/register counts* against hardcoded arrays. Two papers citing the same baselines on different axes with no shared measurement — a trap for any index keyed on baseline name. |
| 6 | BP-SF "~70% of BP-OSD" vs Vegapunk "147.6× vs BP+LSD, 13.9× vs BPGD" | `DIFFERENT_METRIC` / `DIFFERENT_REGIME` | CPU wall-clock Python timing on `[[144,12,12]]` versus FPGA at 250 MHz against different baselines. No shared baseline, no shared hardware. |
| 7 | "Flag-Proxy Networks is qLDPC decoding hardware" | **`TRUE_CONFLICT` with the source material** | FPN has no hardware decoder of any kind; the codebase contains zero HDL and implements MWPM and restriction decoders in C++ `[code]`. The circulating characterization is wrong. |
| 8 | SWIPER "relaxes the 1 µs requirement" vs Pinball's and Triage's binding budgets | `DIFFERENT_REGIME` | Three different quantities that all happen to be expressible in microseconds: SWIPER relaxes *per-window decoder latency* at equal **reaction time**; Pinball's 1 µs is a *per-round* budget for the cryogenic bandwidth path; Triage's is a *throughput/backlog* condition. **Keep them in separate columns** — which is why Table A separates T_decode, cycle budget and bandwidth. |

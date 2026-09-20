# GPU-HPCA24-41 — GPU Scale-Model Simulation

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `N — profiling, debugging, correctness checking, simulation & performance modelling`
secondary_topics: `GPU cache hierarchy & memory bandwidth scaling; multi-chiplet GPU; strong/weak scaling`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — author-hosted PDF (users.elis.ugent.be/~leeckhou/papers/hpca2024.pdf) read for authors/affiliation, motivation and the critique of prior simulation-acceleration and CPU scale-model work, the proportional-scaling construction with the concrete Table I configuration, all three extrapolation formulas (pre-cliff, cliff, post-cliff) with their variable definitions, the Accel-Sim evaluation configuration, the 21+6 benchmark classification by scaling behaviour, the strong- and weak-scaling accuracy tables against four regression baselines, the multi-chiplet case study, the simulation speedups, and the stated assumptions and failure cases. NOT read line-by-line: individual figure captions and the full related-work reference list.`

## 12.1 Bibliographic facts

- Official title: *GPU Scale-Model Simulation* [paper]. `CONFIRMED_IN_POPULATION` — official title is exactly this, Session 10B "GPU" (`census/HPCA_2024.md` §5).
- Authors: **Hossein SeyyedAghaei, Mahmood Naderan-Tahan, Lieven Eeckhout** — Ghent University, Belgium [paper]. Single institution.
- Venue: HPCA 2024, Session 10B. DOI: UNKNOWN (census records UNKNOWN; official program page `https://www.hpca-conf.org/2024/program/main.php`).
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: author-hosted PDF `https://users.elis.ugent.be/~leeckhou/papers/hpca2024.pdf` [official-web].
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

If you cannot simulate a large GPU — either because it is too slow or because no simulation model of the target exists — can you simulate two *small, proportionally scaled-down* GPUs and extrapolate to the large one accurately, given that GPU workloads scale sub-linearly, linearly and super-linearly and therefore defeat any single regression law? [paper]

## 12.3 GPU/HPC problem translation

- **Compute.** The scaled quantity is SM count; the predicted quantity is IPC.
- **Memory.** The paper's real subject is the *shared* memory hierarchy: LLC capacity, NoC bisection bandwidth, off-chip memory bandwidth and memory-controller count all scale with SM count, and the non-linearity that breaks naive extrapolation is a **cache-capacity cliff**.
- **Scheduling.** Only implicitly, through thread-block occupancy per SM (held constant by construction).
- **Communication / synchronization.** NOT_IN_PAPER for inter-GPU; the NoC is modelled as a bandwidth parameter, and a multi-chiplet case study is included.

## 12.4 Why the problem exists (down to hardware root cause)

- **Scale growth.** "Nvidia's Fermi GPU (2010) with 16 SMs to the Hopper H100 (2022) with 144 SMs," with caches and off-chip bandwidth growing alongside — 3 TB/s versus 192 GB/s historically [paper]. Cycle-level simulation of realistic workloads at that size "becomes impractical or even infeasible."
- **Prior acceleration techniques all presuppose a target model.** Workload sampling (Principal Kernel Analysis, TBPoint, Photon), reduced/synthetic inputs, and FPGA-accelerated simulation each "implicitly assumes access to a simulation model of the target system, which might not be available" [paper]. This is the sharpest framing in the paper and the reason it is not merely another speedup technique: it addresses the case where the target does not exist as a model at all.
- **Why CPU scale-model work does not transfer.** Prior scale-model work targeted CPUs with a "one-size-fits-all regression approach" (logarithmic regression). The paper shows this fails on GPUs because "different GPU workloads exhibit vastly different scaling behavior: while some workloads scale linearly, others scale sub-linearly, or even super-linearly" [paper]. Logarithmic regression's 69% average / 86% maximum error on the 128-SM target is the evidence.
- **The hardware root cause of super-linearity — the cliff.** As the scale model grows, LLC capacity grows proportionally; at some size the workload's footprint suddenly fits, the miss rate drops sharply, and memory stalls largely disappear. Performance then improves *faster* than SM count. That discontinuity is a property of the GPU's shared LLC relative to working-set size, and no smooth regression law can represent it `[inference from the paper's three-region construction]`.

## 12.5 Mathematical / performance model

This is the paper's contribution: a **per-workload, three-region extrapolation** driven by the workload's own miss-rate curve, rather than a fitted law.

**Correction factor** — measures how the two scale models actually scaled relative to ideal [paper]:

```
C_{sm,L/S} = ( IPC_{sm,L} / IPC_{sm,S} ) / ( L / S )
```

`IPC_{sm,L}` and `IPC_{sm,S}` are the largest and smallest scale models' IPC; `L/S` is their size ratio (2× in this work). `C = 1` means perfectly linear scaling; `C > 1` super-linear; `C < 1` sub-linear. The whole method turns on measuring `C` empirically per workload instead of assuming a functional form.

**Region 1 — pre-cliff** (miss-rate curve flat; footprint does not fit at any modelled size) [paper]:

```
IPC_{ts,T} = IPC_{sm,L} * (T / L) * C_{sm,L/S}
```

i.e. scale ideally from the largest scale model, then apply the measured correction. "Assumes performance continues to scale as it did for the smaller scale models."

**Region 2 — cliff** (the footprint newly fits; memory stalls are eliminated) [paper]:

```
IPC_{ts,T} = IPC_{sm,L} * (T / L) * 1 / ( 1 - f_{mem,sm,L} )
```

where `f_{mem,sm,L}` is "the fraction of time an SM in the largest scale model is unable to fetch an instruction because all available warps are waiting for data."

This term is the most GPU-specific object in the paper. It is not a cache miss rate — it is the fraction of cycles in which **every resident warp on the SM is blocked on memory**, i.e. the point at which the SM's latency-hiding capacity through multithreading is exhausted. `1/(1 - f_mem)` is exactly the speedup obtained if those fully-stalled cycles vanish. On a CPU the analogous quantity would be a memory-stall fraction of a single thread; on a GPU it is a statement about warp-level parallelism being insufficient to cover the latency, and it can only be measured, not derived from the miss rate.

**Region 3 — post-cliff** (miss rate re-stabilised beyond the cliff) [paper]:

```
IPC_{ts,T} = IPC_{s,K} * (T / K) * C_{sm,L/S}
```

where `K` is the smallest system size beyond the cliff. Prediction restarts from the first post-cliff point so the discontinuity is not extrapolated through.

**Inputs required.** Two cycle-level scale-model simulations (8-SM and 16-SM), plus a miss-rate curve per workload, plus `f_mem` when a cliff is detected. Miss-rate curves come from functional simulation and reuse-distance analysis — cheaper than cycle-level simulation, but not free (12.13).

## 12.6 Data layout and ownership

**The scaling rule: shared resources scale, per-SM resources do not.** "When scaling the number of cores in a multi-core system for example, shared cache capacity, the on-chip interconnection network bandwidth, and the off-chip memory bandwidth should be scaled proportionally," while "a component that does not change when scaling system size … is kept unchanged" — specifically per-SM L1, scratchpad, and functional units [paper].

Table I, the concrete construction (128-SM target → 8-SM scale model, 1/16) [paper]:

| Component | Target (128 SM) | Scale model (8 SM) | Ratio |
|---|---|---|---|
| SMs | 128 | 8 | 1/16 |
| LLC (L2) | 34 MB | 2.125 MB | 1/16 |
| NoC bisection BW | 2,696 GB/s | 168.5 GB/s | 1/16 |
| Memory BW | 2,320 GB/s | 145 GB/s | 1/16 |
| Memory controllers | 16 | 1 | 1/16 |

Ownership mapping:

| Level | Scaled? |
|---|---|
| thread / warp | **no** — 32 threads/warp, 48 warps/SM held constant |
| thread block | **no** — per-SM occupancy unchanged |
| SM | **yes** — this is the scaling variable |
| L1 / scratchpad (per-SM) | **no** — 48 KB L1, 6-way, unchanged |
| L2 / LLC (shared) | **yes** — proportionally |
| NoC (shared) | **yes** — proportionally |
| memory controllers / HBM BW (shared) | **yes** — proportionally |
| chiplet | **yes**, in the multi-chiplet case study |

The justification for proportional scaling is stated as an invariance: because shared resources scale with system size, "the relative impact of the memory accesses remains constant irrespective of system size" [paper]. Per-SM bandwidth and per-SM LLC share are held fixed, so an SM in the scale model sees the same memory environment as an SM in the target — the mechanism by which a small model can stand in for a large one.

## 12.7 Pseudo code

`[reconstruction]` of the described method:

```
# inputs: target size T, two scale-model sizes S < L (here 8 and 16), workload w
# 1. build scale models by proportional reduction of SHARED resources only
for size in {S, L}:
    cfg[size] <- target_config with
                   SMs              = size
                   LLC              = target.LLC   * size / T
                   NoC_bisection_BW = target.NoC   * size / T
                   memory_BW        = target.memBW * size / T
                   mem_controllers  = target.MCs   * size / T
                   per-SM L1, scratchpad, FUs  = UNCHANGED

# 2. cycle-level simulate both scale models
IPC_S <- accel_sim(w, cfg[S]);  IPC_L <- accel_sim(w, cfg[L])
C     <- (IPC_L / IPC_S) / (L / S)                     # correction factor

# 3. miss-rate curve over LLC capacity (functional sim + reuse-distance analysis)
mrc <- miss_rate_curve(w)
region <- classify(mrc, T)        # PRE_CLIFF | CLIFF | POST_CLIFF
                                  # at most one cliff assumed

# 4. extrapolate
if region == PRE_CLIFF:
    IPC_T <- IPC_L * (T / L) * C
elif region == CLIFF:
    f_mem <- fraction of cycles in the L-model where ALL resident warps
             are waiting on data (measured in the scale-model simulation)
    IPC_T <- IPC_L * (T / L) * 1 / (1 - f_mem)
else:  # POST_CLIFF
    K     <- smallest modelled size beyond the cliff
    IPC_T <- IPC_K * (T / K) * C
```

Note the practical wrinkle the paper concedes: when a cliff is detected, `f_mem` "must be extracted from scale model simulation" and the method "requires manual specification" of it [paper] — so the cliff path is not fully automatic.

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact repository identified. Named dependency: **Accel-Sim**, "a validated GPU modeling framework" operating at cycle level [paper]. Baseline 128-SM target configuration as simulated [paper]:

- SM clock 1.0 GHz
- 48 warps/SM × 32 threads/warp = 1,536 threads/SM
- L1: 48 KB per SM, 6-way associative
- L2 (LLC): 34 MB total, **64 slices, 64-way per slice**
- DRAM bandwidth 2.3 TB/s
- NoC: crossbar, 2.7 TB/s bisection

## 12.9 Kernel execution

Kernel/thread-block/warp structure is held **invariant** by construction — that is the method's premise, not an omission. A warp is 32 threads and an SM hosts 48 warps in every model [paper].

What varies with scale is how many thread blocks are resident machine-wide and hence how the shared hierarchy is pressured. The execution-level quantity the model actually needs is `f_mem`: the fraction of cycles in which an SM cannot issue because *all* resident warps await data [paper]. This is a direct statement about the adequacy of warp-level parallelism as a latency-hiding mechanism, and it is the only place the model reaches inside the SM.

Benchmark classification by scaling behaviour (21 strong-scaling benchmarks from Rodinia, Polybench, Parboil, CUDA SDK, MLPerf Inference) [paper]:

| Class | Benchmarks |
|---|---|
| **Super-linear** (7) | dct, fwt, bp, va, as, lu, st |
| **Sub-linear** (5) | bfs, unet, sradv2, gr, btree |
| **Linear** (9) | pf, res50, res34, ht, at, gemm, 2mm, lbm, bs |

Weak scaling used a 6-benchmark subset with scalable inputs: bfs, bp, btree, bs, as, va [paper].

That 7/5/9 split is the paper's empirical justification for rejecting a single regression law: no one law can fit three qualitatively different behaviours, and the classes are not predictable from benchmark provenance (`gemm` and `res50` scale linearly; `bfs` sub-linearly; `dct` super-linearly).

## 12.10 Memory traffic

Traffic is not measured directly; it is *scaled*, and the scaling fidelity is the method's validity condition. Three shared-resource quantities move together with SM count: LLC capacity (34 MB → 2.125 MB), NoC bisection bandwidth (2,696 → 168.5 GB/s), and memory bandwidth (2,320 → 145 GB/s), with memory controllers 16 → 1 [paper].

The **16 → 1 memory-controller reduction is the most fragile part of the construction** `[inference]`. Bandwidth scales cleanly as a number, but a single memory controller cannot reproduce the bank-level parallelism, channel interleaving, and request-scheduling behaviour of sixteen. The paper does not analyse this; it scales the count and validates end-to-end accuracy. The observed sensitivity to scale-model choice (12.11) may partly originate here.

The **miss-rate curve** is the object that carries memory behaviour into the model. Its shape determines the region (pre-cliff / cliff / post-cliff), and generating it requires functional simulation plus reuse-distance analysis [paper].

## 12.11 Why it is faster/slower (decomposed cause)

**Accuracy — strong scaling, 128-SM target predicted from 8-SM and 16-SM scale models** [paper]:

| Method | Average error | Max error |
|---|---|---|
| **Scale-model simulation** | **4%** | **17%** |
| Power-law regression | 12% | 55% |
| Linear regression | 17% | 68% |
| Proportional scaling | 22% | 113% |
| Logarithmic regression | 69% | 86% |

**Strong scaling, 64-SM target** [paper]:

| Method | Average error | Max error |
|---|---|---|
| **Scale-model simulation** | **3.5%** | **13%** |
| Power-law regression | 4% | 13% |
| Linear regression | 6% | 23% |
| Proportional scaling | 10% | 52% |
| Logarithmic regression | 48% | 55% |

**At the 64-SM target, power-law regression matches scale-model simulation almost exactly (4% vs 3.5% average, 13% vs 13% max).** The method's advantage appears only when extrapolating further — 8/16 → 128 is a 8–16× extrapolation, where power law degrades to 12%/55% and scale-model holds at 4%/17%. The value is in *extrapolation reach*, not in accuracy per se.

**Weak scaling, 128-SM target, 6 scalable benchmarks** [paper]: 1.7% average, 4.5% max error — much better than strong scaling, because weak scaling keeps per-SM work constant and so does not stress the cliff mechanism `[inference]`.

**Speedup** [paper]: **9.3×** for predicting 128-SM performance versus simulating the 8-SM and 16-SM scale models. Note carefully what the denominator is — this is the cost of simulating the two scale models versus simulating the 128-SM target directly. The speedup is modest compared with sampling methods (cf. `GPU-MICRO25-01`'s 3× to 31,719×) because the two techniques reduce different costs: scale-model reduces *machine size*, sampling reduces *instruction count*. They are orthogonal and in principle composable; neither paper says so.

**Multi-chiplet case study** [paper]: 4- and 8-chiplet scale models predicting a 16-chiplet system (64 SMs/chiplet, **1,024 SMs total**). Weak scaling, 6 benchmarks — scale-model 2.5% average / 4.3% max; power-law 3.7%/8%; linear 4.7%/9%. Speedup 2.2× average, up to 2.8×. The 1,024-SM prediction is the most forward-looking result: it is roughly 7× a Hopper H100's 144 SMs, i.e. the method is being aimed at machines that do not exist yet — which is exactly the "no model of the target available" motivation.

**Sensitivity — the decomposed weakness** [paper]: switching the scale models from 8/16-SM to 16/32-SM makes errors *worse*, not better: **bfs 56%, fwt 39%, gr 30%** for the 128-SM target. Larger scale models should intuitively give better predictions. That they do not means the correction factor `C` is being measured across a size range that straddles a cliff or a regime change for those workloads `[inference]` — the paper reports the sensitivity without explaining it, and it is the most concerning result in the evaluation because it means scale-model selection is a tuning decision with no stated rule.

## 12.12 Hardware generation dependence

- No real GPU is used. Everything is Accel-Sim; the target is a synthetic 128-SM configuration with 34 MB LLC and 2.3 TB/s DRAM [paper], resembling a Hopper-class part without being one.
- The generational framing is explicit: Fermi 16 SMs (2010) → Hopper H100 144 SMs (2022) [paper].
- **The binding dependence is per-SM architecture, not size.** "If a next-generation target has different per-SM architecture, the methodology requires constructing new scale models with matching per-SM resources" [paper]. So the method extrapolates across *size* within a microarchitecture generation, never across generations. Scale-model simulation cannot answer "how would this workload run on next year's SM."
- Stated non-transfer cases: differing LLC policies, NoC topologies, or memory-controller designs between target and scale model break the construction [paper].
- The multi-chiplet result shows the method extends to a scaling axis (chiplet count) beyond SM count [paper], which matters as GPUs become multi-die.

## 12.13 Limitations

Stated assumptions and failure cases [paper]:
1. **Proportional scaling must hold** — scale models are proportionally reduced with per-SM configuration unchanged.
2. **Per-SM architecture must match** the target; a new per-SM design requires new scale models.
3. **At most one cliff.** "While in theory there could be multiple cliffs … we did not observe this behavior … we hence assume at most one cliff without loss of generality." Extending to multiple cliffs is explicitly future work.
4. **Cliff handling needs `f_mem` extracted from the scale-model simulation** and "manual specification" — the cliff path is semi-automatic.
5. **Sensitivity to scale-model selection** — 16/32-SM models produce 56% (bfs), 39% (fwt), 30% (gr) errors at the 128-SM target.
6. **Miss-rate-curve overhead** — still requires functional simulation and reuse-distance analysis, even if far cheaper than cycle-level simulation.
7. Cannot handle non-proportional differences in LLC policy, NoC topology, or memory-controller design.

Observed by this analysis:
8. **No artifact**, so the method is not directly reproducible.
9. **No validation against real silicon.** Accuracy is measured against full Accel-Sim simulation of the target, so the result is "faithful to the simulator," not "faithful to a GPU." Accel-Sim's own validation error is not compounded into the reported 4%.
10. **The 16 → 1 memory-controller reduction** preserves aggregate bandwidth but not bank/channel parallelism; unanalysed (12.10).
11. **Strong-scaling advantage over power-law regression is small at 64 SMs** (3.5% vs 4%); the case rests on longer extrapolations.
12. **Weak-scaling results use only 6 benchmarks**, versus 21 for strong scaling, so the excellent 1.7% weak-scaling figure rests on a much smaller sample.

## 12.14 Relation to prior corpus

- **Prior corpus:** `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Scale-Model Simulation" returns only `domains/gpu_systems/census/HPCA_2024.md` (a census row).
- **Prior work named and critiqued in the paper** [paper]: workload sampling — **Principal Kernel Analysis**, **TBPoint**, **Photon**; reduced/synthetic inputs; FPGA-accelerated simulation; and prior **CPU scale-model** work using logarithmic regression, which the paper shows fails on GPUs (69% average error).
- **Verified overlap with `GPU-MICRO25-01`:** both papers name **Principal Kernel Analysis / PKA**, **TBPoint** and **Photon** as the prior sampling art. The two papers therefore share a literature and partition the problem: STEM+ROOT reduces *which and how many kernels* are simulated; Scale-Model Simulation reduces *how large a machine* is simulated. Composing them is unexamined by either. See `_LEDGER_profiling_reliability.md`.
- **Complementary within this cluster:** *GRASP: Fine-grained and Adaptive Sampled Simulation for GPU Performance Modeling* (ICS 2026), *HyFiSS: A Hybrid Fidelity Stall-Aware Simulator for GPGPUs* (MICRO 2024), *TrioSim* (ISCA 2025), and *GCStack+GCScaler* (ISCA 2025) are the adjacent simulation/modelling works in the verdict-only list. *GCStack+GCScaler* is the closest in spirit — it also predicts alternative GPU designs from an interval model rather than by full simulation (its `GCoM` lineage), and it is by the same intellectual tradition as Eeckhout's interval-analysis work.
- **Contrast with measurement-based approaches:** `GPU-SC26-41` (LEO) reaches the same goal — understanding GPU stalls — by sampling real hardware, and pays a ~10% measurement overhead instead of a simulation cost. Scale-Model's distinguishing claim is that it works when *no target hardware and no target model exist*, which no measurement method can match.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The paper exists precisely *because* the pre-existing CPU scale-model methodology fails on GPUs: one-size-fits-all logarithmic regression, adequate for CPUs, produces 69% average and 86% maximum error on a 128-SM GPU target, because GPU workloads split into super-linear (7), linear (9) and sub-linear (5) scaling classes. The scaling variable is the **SM count**, the invariants held fixed are **per-SM warp slots (48 warps × 32 threads), L1 and scratchpad**, and the quantities scaled are the GPU's **shared L2/LLC (34 MB across 64 slices), NoC bisection bandwidth, HBM bandwidth and memory-controller count**. The cliff term `1/(1 - f_mem)` is defined as the fraction of cycles in which *all resident warps on an SM* are waiting on data — a statement about warp-level-parallelism latency hiding that has no single-thread CPU analogue. The evaluation runs entirely in Accel-Sim, a GPU simulator, and the forward-looking case study scales chiplet count to 1,024 SMs.

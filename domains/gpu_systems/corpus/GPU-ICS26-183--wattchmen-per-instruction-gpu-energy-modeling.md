# GPU-ICS26-183 — Wattchmen: Watching the Wattchers – High Fidelity, Flexible GPU Energy Modeling

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `N — performance/energy modelling; C — instruction-level GPU execution (SASS)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2603.26435v1) — authors/affiliations, abstract, motivation and the AccelWattch-brittleness argument, background on vendor power tooling, the microbenchmark design, the constant/static/dynamic energy decomposition, the linear system and non-negative solve, the three coverage mechanisms (scaling, grouping, bucketing), the measurement chain, all four evaluation clusters, the MAPE tables per SKU, the Direct-vs-Pred ablation, both case studies, the five stated limitations, and the related-work section. NOT read line-by-line: the per-microbenchmark assembly listings and the full figure set.`

---

## 12.1 Bibliographic facts

- Official title: *Wattchmen: Watching the Wattchers – High Fidelity, Flexible GPU Energy Modeling* [paper].
- Authors: **Brandon Tran** (Univ. of Wisconsin–Madison), **Matthias Maiterth** (NVIDIA; formerly ORNL), **Woong Shin** (ORNL), **Matthew D. Sinclair** (UW–Madison), **Shivaram Venkataraman** (UW–Madison) [paper].
- Venue: **ICS 2026** (40th ACM International Conference on Supercomputing), Session **S04 Energy & Sustainability** (`census/ICS_2026.md:42`). DOI `10.1145/3797905.3800514` [official-web].
- Publication type: `ARCHIVAL_MAIN_PAPER`; full text read as `PREPRINT` (arXiv `2603.26435v1`).
- Census note: the ICS 2026 census recorded the author only as "B. Tran et al." and did not have the preprint. **Corrected here**: full author list and arXiv ID above.
- Artifact: `NOT_FOUND_AFTER_SEARCH` — no repository is named in the preprint text that was read.

## 12.2 Core question (one sentence)

Can per-SASS-instruction GPU energy be recovered by solving a linear system over hand-written microbenchmarks, accurately enough to survive a change of architecture, cooling medium and TDP without re-deriving the model? [paper]

## 12.3 GPU/HPC problem translation

- **Compute.** The model's unit of account is the **SASS instruction with its modifiers** — `F2F.F64.F32` is a different energy from `F2F.F32.F16`, `HMMA.STEP` sequences are aggregated, `STG.E.EF.64` and `STG.E.64` are grouped.
- **Memory.** Memory instruction energy is conditioned on **cache hit rates**: a load charged 90 % at L1 energy and 10 % at the next level down, per profiled hit ratio.
- **Scheduling/operations.** The stated purpose is attribution for power-aware scheduling and for finding energy bugs in application code.

## 12.4 Why the problem exists (hardware root cause)

Two gaps, one modelling and one instrumental [paper]:

1. **Vendor tooling stops at the device.** NVML and `rocm-smi` give system-level GPU power/energy and "no detailed, instruction-level granularity information". You can see that a kernel cost 12 J; you cannot see that 40 % of it was an accidental FP64 conversion.
2. **Prior models are brittle to the environment, not to the architecture.** AccelWattch reports 16 % MAPE on its own V100 hardware but the authors measure **32 % MAPE for AccelWattch on a CloudLab V100** — same architecture, different deployment. The stated cause is that AccelWattch is "not flexible enough to handle variations in architecture and operational conditions", i.e. cooling, TDP and memory configuration are first-order and unmodelled. Prior per-instruction work covers compute (Arafa et al.) or the memory hierarchy (Delestrac et al.) but **none covers control-flow instructions**; ML-based models (Wu et al.; Alavani et al.) are accurate at kernel granularity but cannot explain *which* optimisation helped.

## 12.5 Mathematical model

**Decomposition** [paper]:

```
E_dynamic = E_measured − P_const · T_exec − P_static · T_exec
```

`P_static` comes from idle-GPU measurement; `P_const` from steady-state floor.

**The linear system.** For microbenchmark *i* containing counts of *n* instruction classes:

```
E_dynamic,i = Σ_j  count_{i,j} · energy_j
```

solved across all 90 microbenchmarks with a **non-negative** linear solver so that no instruction is assigned negative energy. The authors report the **residual remains zero**, which they take as support for the linearity assumption [paper].

**Prediction.**

```
E_app = (P_const + P_static)·T_exec  +  Σ_j count_j · energy_j
```

with memory terms selected per cache level by profiled hit rate.

**The insight that makes the solve work** is that each microbenchmark contains ancillary instructions (loop control, address arithmetic) that are the *target* of some other microbenchmark — so the system is over-determined rather than requiring perfect isolation of one instruction at a time.

**Three coverage mechanisms** for instructions never directly measured [paper]:
- **Scaling** — extrapolate an unmeasured data width from measured widths of the same memory op.
- **Grouping** — accumulate minor-modifier variants and multi-step sequences under one group energy.
- **Bucketing** — assign an unknown instruction the mean energy of a microarchitecturally similar bucket (their example: `R2UR` bucketed with the integer-ALU ops `MOV`, `LOP3.LUT`).

## 12.6 Data layout and ownership

Not a data-layout paper. The ownership hierarchy that matters is **instruction → SM → GPU**: each of the 90 microbenchmarks is written to **saturate all SMs and all SIMT lanes**, so that per-instruction energy is separated from shared-resource overhead rather than measured on a partly idle device [paper]. This is also the model's main structural weakness (see 12.13).

## 12.7 Pseudo code

`[reconstruction]`:

```
# Training (once per GPU SKU + deployment)
P_static <- measure idle GPU
for b in 90 microbenchmarks (inline asm, targeted SASS op, all SMs saturated):
    run to steady state; discard startup; take MEDIAN power over repeated runs
    cool the GPU between runs
    counts[b] <- Nsight Compute SASS opcode histogram (modifiers retained)
    E_dyn[b]  <- NVML energy counter − (P_const + P_static)·T_exec
energy[] <- nonneg_lstsq(counts, E_dyn)
extend energy[] by scaling / grouping / bucketing

# Prediction (per application)
profile app: T_exec, SASS opcode counts, cache hit rates
E_pred = (P_const + P_static)·T_exec + Σ counts_j · energy_j(hit-rate-selected)
```

## 12.8 Real implementation

No artifact repository located (`NOT_FOUND_AFTER_SEARCH`), so **no `[code]` evidence is available for this paper** and no symbols are asserted. Tool chain per the paper [paper]: **NVIDIA Nsight Compute** for SASS opcode counts with modifiers retained; **NVML** energy counter as ground truth and NVML power samples as a cross-check; CUDA **11.0** on V100 and **12.0** on A100/H100; microbenchmarks written in **inlined assembly**.

## 12.9 Kernel execution

Each microbenchmark is a loop-unrolled body of one targeted SASS instruction plus unavoidable loop/address instructions, launched at full occupancy so every SM and SIMT lane is active; steady state is reached after a brief startup ramp (the paper's Figure 4 example settles at ~**150 W**, a V100-class figure that should not be reused without that qualifier) [paper].

## 12.10 Memory traffic

Handled as a *charging rule*, not a traffic model: the same load instruction is assigned L1, L2 or HBM energy in proportion to its profiled hit rates. There is no model of queueing, row-buffer behaviour or coalescing — which is precisely where `GPU-SC25-184`'s pJ/bit-per-level parameterisation is the stronger treatment.

## 12.11 Why it is more accurate (decomposed cause)

Accuracy figures, each with its SKU and cooling qualifier [paper] — MAPE over 16 workloads:

| Platform | AccelWattch | Guser | Wattchmen-Direct | **Wattchmen-Pred** |
|---|---|---|---|---|
| **V100, air-cooled (CloudLab, 12 GPUs)** | 32 % | 25 % | 19 % | **14 %** |
| **V100, water-cooled (Summit)** | 17 % † | — | 15 % | **14 %** |
| **A100, air-cooled (Lonestar6, 252 GPUs)** | — | — | 13 % (70 % instruction coverage) | **11 % (93 % coverage)** |
| **H100, air-cooled (Lonestar6, 8 GPUs)** | — | — | 16 % (66 % coverage) | **12 % (92 % coverage)** |

† The paper is unusually honest here: AccelWattch's *better* number on water-cooled Summit is **serendipitous** — its predictions are unchanged because it is unaware of cooling, and the measured ground truth simply fell. Carry that caveat; the 17 % is not evidence AccelWattch handles Summit.

Cause decomposition:
1. **Retraining on the deployment, not just the architecture,** absorbs cooling, TDP and memory-configuration differences into `P_const`/`P_static` and the per-instruction constants. This is the whole answer to the AccelWattch brittleness.
2. **Coverage mechanisms are worth 4–6 MAPE points** — Direct→Pred lifts coverage from 66–80 % to 92–93 %. On **H100 the gap is largest (16 %→12 %) because the new `HGMMA` Tensor-Core instructions were never directly measured** and are reached only by bucketing. That is a hardware-generation-specific accuracy hole, not a modelling detail.
3. **Actionability.** Backprop: **16 %** energy reduction after Wattchmen's `F2F.F64.F32` profile exposed an accidental double→float initialisation. QMCPACK: **35–36 %** energy reduction after a mixed-precision bug producing unnecessary function calls was removed, with the model's predicted reduction **within 1 % of the measured one**. These are the strongest results in the paper: a model that predicts the *delta* from a source change to within a point is doing something a kernel-level ML regressor cannot.

## 12.12 Hardware generation dependence

Retrained per SKU and per deployment: V100 (air and water), A100, H100. Generation dependence shows up structurally as **instruction coverage**: 70 % direct coverage on A100 but only 66 % on H100 because of new Tensor-Core opcodes. Every new Tensor-Core generation reopens the coverage hole until new microbenchmarks are written.

## 12.13 Limitations (authors' own, plus review)

1. **Microbenchmarks saturate all SMs; real applications do not.** A full sweep of activity levels would improve accuracy but explodes the design space. This is the largest unmodelled term — occupancy.
2. Per-instruction isolation is imperfect in a deep pipeline; dark silicon, occupancy and latency hiding blur attribution.
3. **NVML granularity is the accuracy floor** — explicitly acknowledged for short kernels.
4. Compiler sensitivity: CUDA 11.0 vs 12.0 silently changes emitted SASS, so retraining is entangled with toolchain version.
5. Thermal variability mitigated by median-of-runs and inter-run cooling, but not modelled.

**Review-side.** The ground truth is **NVML's own energy counter**, validated only against **NVML's own integrated power samples** (<1 % difference) [paper]. There is **no wall meter, PDU or oscilloscope anywhere in this paper.** Read against `GPU-SC24-181` — which shows that on an A100/H100 the power field observes 25 ms out of every 100 ms and carries a random ±5 % per-board gain error — a 14 %/11 %/12 % MAPE is being measured against a reference whose own error bar is not established. The authors' `<1 %` agreement between the counter and the integrated samples shows those two NVML paths are consistent with each other; it does not establish either against physical truth.

## 12.14 Relation to prior corpus

- **Cites `GPU-ICS24-01`.** The related-work section cites **"Oles et al. (2024) on Volta static power (~80 W)"** [paper] — that is the Summit GPU-memory-corruption paper already in this corpus. **Lineage verified from the paper's own citation**: the Summit study is being used by later power-modelling work as a source of V100 static-power calibration, which is a use its authors did not foreground.
- **Trained partly on Summit's 27,648 water-cooled V100s** — the same machine and the same GPU population as `GPU-ICS24-01`. The two papers therefore share a testbed: one measures why those GPUs' memory fails under power swings, the other measures what their instructions cost in Joules.
- **Baselines Guser (Shan et al., HPCA 2024)** — which is on this cluster's verdict-only list. Wattchmen reimplements Guser as `max power × execution time` and measures it at **25 % MAPE on an air-cooled V100** [paper]; it criticises Guser for lacking control-flow and static-energy accounting. This is the only quantitative external assessment of Guser available to this cluster.
- **Complementary to `GPU-SC25-184`.** Both are microbenchmark-parameterised additive energy models validated on real applications. Wattchmen's unit is the **SASS instruction**; LBNL's is the **functional unit and memory level in pJ/bit and pJ/FLOP**, with a control-vs-datapath split. Wattchmen is finer but NVIDIA-only and occupancy-blind; LBNL is coarser but cross-vendor and four-generation. Neither cites the other in what was read.
- **Depends on, but does not cite, `GPU-SC24-181`.** The stated NVML-granularity limitation is exactly the phenomenon Yang et al. quantified.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The model's unit of account is the **NVIDIA SASS instruction with its modifiers**, recovered from Nsight Compute, with coverage mechanisms written against specific GPU opcodes (`HMMA.STEP`, `HGMMA`, `STG.E.EF.64`, `R2UR`, `F2F.F64.F32`); microbenchmarks are constructed to saturate **all SMs and SIMT lanes** so that per-instruction energy separates from GPU shared-resource overhead; and the ground truth is the **NVML** energy counter, whose coarse granularity the authors name as their accuracy floor. None of this survives translation to a CPU or an unnamed accelerator.

verdict: `CORE_GPU`

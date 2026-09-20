# GPU-SC25-184 — Benchmark-driven Models for Energy Analysis and Attribution of GPU-Accelerated Supercomputing

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `N — performance/energy modelling (Roofline lineage); E — memory hierarchy energy`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the open-access eScholarship PDF (escholarship.org/content/qt6189368s/qt6189368s.pdf, CC BY 4.0) — authors/affiliations/DOI, motivation, the measurement chain, the three microbenchmark families, the zero-vs-random control/datapath separation, the memory-level subtraction identities, Equations 1-5 and the TDP min(), the per-GPU energy-parameter table, all four GPU configurations, the five validation applications, the attribution breakdowns, the constant-power/DRAM-refresh analysis, the eight stated limitations, and related work. NOT read line-by-line: every figure panel and the full appendix.`

---

## PRIOR-ANALYSIS DELTA NOTICE (task §4)

`domains/hpc_systems_operations/` (imported) holds two shallow records:
- `raw/A_SC_main.md:218` — an `S25-9` heading only.
- `synthesis/02_PAPER_CENSUS.md:968` — one census row: DOI, `L3/L5 · D2 · P4 · REL`, and the Korean one-liner *"기능단위(FPU/tensor core/int ALU)·메모리계층별 에너지 귀속"* (energy attribution by functional unit and memory level) — i.e. a restatement of the title.

Neither record read the paper. **This is a `GPU_DELTA_ANALYSIS`**; the measurement chain, the zero-vs-random method, the equations, the pJ/bit and pJ/FLOP table, the 1 Hz sampling limitation and the AMD-throttling confound are all new to this repository.

---

## 12.1 Bibliographic facts

- Official title: *Benchmark-driven Models for Energy Analysis and Attribution of GPU-Accelerated Supercomputing* [paper].
- Authors, all **Lawrence Berkeley National Laboratory**: **Oscar Antepara\***, Zhengji Zhao, Brian Austin, Nan Ding, Leonid Oliker, Nicholas J. Wright, **Samuel Williams\*** (\* equal contribution) [paper].
- Venue: **SC '25**, 16–21 November 2025, St. Louis, MO. **pp. 888–904.** DOI `10.1145/3712285.3759815` [paper]. Licence **CC BY 4.0**, which is why the eScholarship copy is a legitimate full text.
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Note the author overlap with this cluster's ISC lineage: **Zhengji Zhao** and **Nicholas J. Wright** are also the authors of *Maximizing Power-Constrained Supercomputing Throughput* (ISC 2025) and co-authors on the NERSC Cori/Perlmutter power-trends work (ISC 2024) and the ISC 2026 GPU power-prediction seed. This is a single NERSC/LBNL programme, not four unrelated papers.
- Artifact: `NOT_FOUND_AFTER_SEARCH` — none named in the text read.

## 12.2 Core question (one sentence)

What does a Joule actually buy on a modern GPU — how much goes to moving bits at each level of the hierarchy, how much to arithmetic in each functional unit, and how much is pure control overhead that does no useful work? [paper]

## 12.3 GPU/HPC problem translation

- **Memory.** The dominant result is a **pJ/bit** figure per level (L1, L2, HBM) and the finding that off-chip movement is 3–8× costlier per bit than on-chip.
- **Compute.** A **pJ/FLOP** figure per functional unit, separating **vector FPU** from **matrix/Tensor-Core FPU** and separating precisions.
- **Control vs datapath.** The paper's distinctive axis: how much energy is instruction fetch/decode/dispatch and register-file plumbing versus the switching of the actual data bits.
- **Scheduling/operations.** Motivated explicitly by power-constrained facility operation — GPUs are stated to be **up to 80 % of node power**.

## 12.4 Why the problem exists (hardware root cause)

Energy per operation is not published by vendors and is not separable from a single power reading. Two hardware facts make it recoverable [paper]:

1. **Datapath energy is data-dependent.** CMOS switching energy depends on how many bits toggle. Feeding **all-zero** operands exercises instruction fetch, decode, dispatch and the control plane while the datapath carries no switching activity; feeding **random** operands exercises both. The **difference is the datapath**; the **zero-data measurement is the control plane**. The method is credited to Lucas et al. (2016, ALUPower) and Bhalachandra et al. (2022).
2. **Memory levels are separable by working-set sizing.** A benchmark whose working set fits L1, then L2, then spills to HBM, yields nested totals that subtract.

## 12.5 Mathematical model

**Base model (Eq. 1)** [paper]:

```
P = min( TDP ,  P_const + e_L1·BW_L1 + e_L2·BW_L2 + e_HBM·BW_HBM + e_FPU·PERF )
```

The `min(TDP, ·)` is doing real work: it is how the model reproduces the *flattening* of measured power under a power cap, i.e. it models the GPU's own hardware power-capping controller clamping frequency.

**Eq. 2** replicates this for `X ∈ {C, C+D}` (control-only from zero data; control+datapath from random data). **Eq. 3** splits the FPU term into **V**ector and **M**atrix units with separate rates. **Eqs. 4–5** extract parameters by least squares over the Mixbench arithmetic-intensity sweep, solving the extremes (high and low AI) to avoid non-physical negative coefficients.

**Memory-level subtraction identities** [paper]:

```
e_L2  = e_{L2+L1}      − e_L1
e_HBM = e_{HBM+L2+L1}  − e_L2 − e_L1
```

## 12.6 Data layout and ownership

Four GPUs across two vendors and four process nodes [paper]:

| GPU | System | SMs/CUs | LLC | Memory | Process | TDP |
|---|---|---|---|---|---|---|
| NVIDIA **A100** | Perlmutter (NERSC) | 108 SM | 40 MB L2 | 40 GB HBM2e, 1.5 TB/s | TSMC N7 | 400 W |
| NVIDIA **GH200** | ATE testbed (NERSC) | 132 SM | 50 MB L2 | 96 GB HBM3, 4 TB/s | TSMC N4 | 900 W |
| AMD **MI250X** (1 GCD) | Frontier (ORNL) | 110 CU | 8 MB L2 | 32 GB HBM, 1.6 TB/s per GCD | TSMC N6 | ~280 W effective GCD (560 W full GPU) |
| AMD **MI300A** | AMD Accelerator Cloud | 228 CU (XCD) | 256 MB LLC | 128 GB HBM3, 5.3 TB/s | TSMC N5 | 550 W |

Note the MI250X entry is a **single GCD**, and the paper flags that AMD documents only the **package** TDP — a measured single-GCD draw of 350 W exceeds the half-package 280 W, forcing a model adjustment. That is the same package-level-attribution wall `GPU-ISC26-182` hits from the sensor side.

## 12.7 Pseudo code

`[reconstruction]`:

```
for each GPU:
  P_const <- idle power
  for data in {ZERO, RANDOM}:                       # random initialised in [1.0, 2.0] with a -2.0
      Mixbench AI sweep      -> (BW, PERF, P) -> lstsq -> e^data_{HBM+L2+L1}, e^data_VFPU
      GPU-cache (fits L1)    -> e^data_L1
      GPU-cache (fits L2)    -> e^data_{L2+L1}
      vendor GEMM (FP64/FP32/TF32/FP16) -> subtract memory energy -> e^data_MFPU
  e_L2  = e_{L2+L1} - e_L1 ; e_HBM = e_{HBM+L2+L1} - e_L2 - e_L1
  datapath = (C+D) - C
# Application attribution
profile app (Nsight Compute / ROCm Profiler) -> BW_L1, BW_L2, BW_HBM, PERF_VFPU, PERF_MFPU
predict P by Eq.3; decompose into constant / control / datapath per term
```

## 12.8 Real implementation

No artifact located (`NOT_FOUND_AFTER_SEARCH`), so **no `[code]` evidence**; no symbols asserted. Tooling per the paper [paper]:

- **Power:** `nvidia-smi` on NVIDIA and `amd-smi` on AMD, both at a **one-second sampling rate**.
- **Counters:** **NSight Compute** (NVIDIA) and **ROCm Profiler** (AMD) for bandwidth, FLOP rate and cache hit patterns.
- **Microbenchmarks:** **Mixbench** (arithmetic-intensity sweep, 1..n polynomial ops per memory reference), **GPU-cache** (NHR@FAU, working sets sized to L1/L2), and vendor GEMMs — **cuBLAS** on NVIDIA, **CoralGemm/hipBLAS** on AMD — in FP64/FP32/TF32/FP16.
- **Random-data initialisation detail:** values in **1.0–2.0 with a −2.0 constant**, chosen to prevent underflow/overflow along long multiply-accumulate chains so that the "random" case stays numerically meaningful [paper].
- **Ground truth:** **none external.** No PDU, wall meter or oscilloscope; validation is model-vs-vendor-sensor.

## 12.9 Kernel execution

Kernel granularity only. Power is aligned to kernel intervals via profiler timestamps, and at 1 Hz sampling that alignment is necessarily coarse — see 12.13.

## 12.10 Memory traffic

This is the paper's strongest axis. Measured energy per bit, **per GPU, whole-stack (control + datapath) figures** [paper]:

| GPU | HBM (pJ/bit) | L2 (pJ/bit) | L1 (pJ/bit) | V-FP64 (pJ/FLOP) | M-FP16 (pJ/FLOP) |
|---|---|---|---|---|---|
| A100 | 13.11 | 4.71 | 1.59 | 28.50 | 0.70 |
| GH200 | 11.68 | 4.87 | 1.45 | 23.60 | 0.52 |
| MI250X (GCD) | 13.64 | 2.82 | 1.54 | 15.73 | 1.60 |
| MI300A | 14.72 | 1.39 | 2.11 | 11.47 | 0.46 |

Derived facts, each carrying its qualifier:
- **Off-chip is 3–8× costlier per bit than on-chip caching**, across all four GPUs.
- **Control is 50–75 % of data-movement energy**; the **datapath — the actual bit movement — is only 8–35 % of HBM energy.** This is the paper's most striking single result: most of what an "HBM access" costs is not moving the bits.
- **Matrix FP16 is roughly an order of magnitude cheaper per FLOP than vector FP64** (0.46–1.60 vs 11.47–28.50 pJ/FLOP).
- **Constant (idle) power 54–88 W**, attributed largely to **DRAM refresh**: assuming a 32 ms refresh cycle at ~4–5 pJ/bit predicts 40–50 W for 40 GB of HBM, which matches measurement. MI250X shows ~60 % higher constant power, attributed to larger memory capacity.
- **Across N7→N6→N5→N4, datapath energy scales well but control energy improvement plateaus** — i.e. the part of the bill that does no useful work is the part that is not shrinking.

## 12.11 Why it works (decomposed cause)

1. **The zero/random subtraction is a physical, not statistical, separator** — it exploits CMOS switching activity directly, so the control/datapath split needs no fitted latent variable.
2. **Over-determination from the AI sweep** lets the least-squares solve be taken at the extremes, which is what keeps coefficients physical (non-negative).
3. **The `min(TDP, ·)` clamp is why the model tracks real hardware**, reproducing measured power plateaus and the "rounded Roofline" shape on MI300A.
4. **Application validation** on A100 across MILC (QUDA lattice QCD), BerkeleyGW Epsilon and Sigma (OpenACC many-body perturbation theory), LAMMPS via EXAALT (Kokkos), and **GPT-NeoX** (125 M params, 200 training steps): constant power ~15 % of total; **control power often >50 %**; data movement 40–60 % of total for MILC, BerkeleyGW-Epsilon and GPT-NeoX; compute-bound kernels (BerkeleyGW-Sigma, LAMMPS) put 50–70 % in FP64 vector plus integer ops.

## 12.12 Hardware generation dependence

Four process nodes and two vendors by construction (N7 A100 → N6 MI250X → N5 MI300A → N4 GH200). The paper's comparative claim — that datapath energy scales with process while control energy plateaus — is only sayable because the same measurement was repeated on four parts.

## 12.13 Limitations (authors' own, plus review)

1. **1 Hz power sampling** — no sub-second transient resolution; kernel-invocation overhead and context switching blur attribution.
2. **No external power meter**; entirely dependent on the vendor on-chip PMU, with no assessment of systematic offset or calibration drift.
3. The TDP model assumes all energy terms scale equally under DVFS, which need not hold.
4. **MI250X single-GCD vs package-TDP mismatch** forces an adjustment that introduces inaccuracy near machine balance.
5. **AMD thermal throttling confounds the zero-vs-random separation on MI250X and MI300A** — the method works cleanly on NVIDIA but not on AMD.
6. The application model assumes randomly distributed data; **real datapath power can exceed the prediction (worst-case switching) or fall below it (all zeros)**.
7. Scope is a single GPU's kernels: **no inter-GPU, CPU–GPU or inter-node communication energy**.
8. The GEMM matrix-energy figure is a residual after subtracting modelled memory energy, so profiling error in bandwidth propagates into it.

**Review-side, and it is the same point twice.** Limitations 1 and 2 together mean the entire pJ/bit and pJ/FLOP table rests on `nvidia-smi`/`amd-smi` sampled at **1 Hz**. `GPU-SC24-181` establishes that on an A100 the underlying sensor observes **25 ms of every 100 ms** and carries a random **±5 %** per-board gain error; `GPU-ISC26-182` establishes that the AMD power field is an **undocumented moving average**. Steady-state microbenchmark measurement is the *best* case for such a sensor — long, flat, repeated — so the parameters are probably sound, but the ±5 % board-to-board gain error is not removed by any amount of averaging and is not in the paper's error budget. Limitation 5 (AMD throttling) is, read against `GPU-ISC26-182`, an expected consequence of observing a throttling device through a filtered field at 1 Hz.

## 12.14 Relation to prior corpus

- **This is the missing mechanism behind the corpus's Hopper `wgmma` finding.** `GPU-IPDPS24-61` reports that Hopper `wgmma` throughput depends on input matrix *contents* — all-zero data drawing **<200 W at >95 % of peak** while random data hits **350 W and drops the clock below the whitepaper figure** on an H800. This paper's control/datapath decomposition is exactly that effect, isolated deliberately and quantified: the datapath is **8–35 % of HBM energy** and the rest is content-independent control. Two labs, two purposes, one physics. **Lineage verified from this paper's own citations**: Lucas et al. 2016 (ALUPower) first observed data-dependent power on older NVIDIA GPUs; Bhalachandra et al. 2022 confirmed it on modern GPUs and supplied the random-vs-zero methodology this paper adopts; Gregersen et al. 2025 report input-dependent power on contemporary GPUs. The microbenchmarking paper's observation is not an isolated curiosity — it sits on a nine-year measurement lineage.
  - **Consequence for this corpus, stated as an inference:** any GPU power or energy number measured with a benchmark that uses zero-filled or constant-filled input buffers is a *lower bound* on the real datapath energy, potentially by the full datapath fraction `[inference, grounded in this paper's 8–35 % datapath share and the wgmma 200 W/350 W gap]`.
- **Complementary to `GPU-ICS26-183` (Wattchmen).** Same genus — microbenchmark-parameterised additive energy model, application-validated — different unit of account: functional unit and memory level (pJ/bit, pJ/FLOP, control vs datapath, four GPUs, two vendors) versus SASS instruction with modifiers (finer, NVIDIA-only, occupancy-blind). Neither cites the other in what was read; together they are the two halves of a cross-vendor instruction-and-hierarchy energy model that nobody has yet assembled.
- **Same programme as this cluster's NERSC ISC papers** (Zhao, Wright) — see 12.1.
- **Roofline lineage, from the paper's own citations**: Williams et al. 2009 (Roofline) and Choi et al. 2013 (energy-based analogues); DRAM-side, Chatterjee et al. 2017 and O'Connor et al. 2017 (FGDRAM); Kogge & Shalf 2013 for exascale energy forecasts, which the authors distinguish as *theoretical* against their own empirical multi-generation measurement.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The model is parameterised per **GPU memory level (L1 / L2 / HBM)** and per **GPU functional unit (vector FPU vs matrix/Tensor-Core FPU, per precision)**, extracted with GPU-specific microbenchmarks (Mixbench, GPU-cache, cuBLAS/hipBLAS GEMM) read through `nvidia-smi`/`amd-smi`; the `min(TDP, ·)` term models the **GPU's own hardware power-capping controller** clamping clocks; and the single largest reported obstacle — AMD thermal throttling breaking the zero-vs-random separation on MI250X/MI300A — is a property of those GPUs' power/thermal controllers.

verdict: `CORE_GPU`

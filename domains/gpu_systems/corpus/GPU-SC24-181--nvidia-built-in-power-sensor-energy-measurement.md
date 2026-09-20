# GPU-SC24-181 — Accurate and Convenient Energy Measurements for GPUs: A Detailed Study of NVIDIA GPU's Built-In Power Sensor

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` (via the authors' arXiv preprint of the same work, see 12.1)
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `N — measurement methodology & instrumentation; O — telemetry trustworthiness`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2312.02741v2) — title/authors/affiliation, abstract, motivation, the external-instrument description (ElmorLabs PMD: ADC, ranges, sampling), the nvidia-smi/NVML query-field semantics, the square-wave microbenchmark design, the aliasing experiment and Nelder-Mead window recovery, per-architecture update-period and averaging-window results, the transient-response taxonomy, the steady-state proportional-error result, the GPU population table, the Grace Hopper section, the three "good practice" mitigations with their before/after error figures, the stated limitations, and related work. PLUS [code] inspection of the artifact at pinned commit ab12c0606775e38872501de8a5cf57ca0e863fa1. NOT read line-by-line: the full figure set and the per-model appendix tables.`

---

## PRIOR-ANALYSIS DELTA NOTICE (task §4)

`domains/hpc_systems_operations/` **is an imported corpus** and already mentions this paper twice, both times shallowly:

- `corpus/aiops-survey/raw/A_SC_main.md:184` — **`S24-12`**, graded `ABSTRACT-UNREAD`, `L0 · D2 · P2/P4 · SC-REGULAR-RELEVANT`, with the one-line characterisation *"Telemetry-infrastructure/measurement-fidelity paper — directly relevant to 'can you trust your power telemetry'"*.
- `corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md:977` — a census row repeating the same framing in Korean.

Neither record read the paper. Both omit: the instrument, the sampling rates, the numbers, the per-architecture window table, the Grace Hopper regression, and the mitigation recipe. **This file is therefore a `GPU_DELTA_ANALYSIS` against a shallow operations row**, and everything below §12.1 is new to this repository.

`domains/gpu_systems/census/SC_2024.md:44` is this project's own STEP A/B row and records `NOT_FOUND_AFTER_SEARCH (no arXiv...)`. **That census statement is now corrected** — see 12.1.

---

## 12.1 Bibliographic facts

- Official title: *Accurate and Convenient Energy Measurements for GPUs: A Detailed Study of NVIDIA GPU's Built-In Power Sensor* [paper].
- Authors: **Zeyu Yang, Karel Adámek, Wesley Armour**, Department of Engineering Science, University of Oxford, UK [paper]. Contact `zeyu.yang@eng.ox.ac.uk` [README].
- Venue: **SC '24**, pp. **307–323**, IEEE Computer Society. DOI `10.1109/SC41406.2024.00028` [paper, README].
- Publication type: `ARCHIVAL_MAIN_PAPER`. The full text used here is its `PREPRINT`.
- **Access-path correction (important).** The SC census recorded "no arXiv". In fact the work **is** on arXiv, *under a different title*: **arXiv `2312.02741`, "Part-time Power Measurements: nvidia-smi's Lack of Attention"** [official-web]. The identity of the two is established by three independent links, not by resemblance:
  1. the Semantic Scholar record for DOI `10.1109/SC41406.2024.00028` returns `"ArXiv": "2312.02741"` and `"DBLP": "conf/sc/YangAA24"` [official-web];
  2. the same three authors in the same order [paper];
  3. the published abstract's distinctive numbers — *"over 70 different GPUs across 12 architectural generations"*, *"on the A100 and H100 GPUs only 25% of the runtime is sampled"*, *"reduce the energy measurement error by an average of 35%"* — appear verbatim in the preprint [paper].
  Per `SOURCE_EVIDENCE_RULES`, everything below is tagged `[paper]` as preprint evidence for the archival paper; where the two could in principle differ (title, exact section numbering) that is flagged.
- Artifact: `https://github.com/JimZeyuYang/GPU_Power_Benchmark`, MIT, Zenodo DOI `10.5281/zenodo.13313030` [README]. Inspected at pinned commit **`ab12c0606775e38872501de8a5cf57ca0e863fa1`** [code].

## 12.2 Core question (one sentence)

What, mechanically, is the number that `nvidia-smi`/NVML calls GPU power — at what cadence is it produced, over what window is it averaged, how much of the elapsed time does it actually observe, and how wrong is the energy you integrate from it? [paper]

## 12.3 GPU/HPC problem translation

- **Measurement, not compute.** The object of study is the GPU's own on-board power-sensing and reporting path, not a kernel.
- **Scheduling/operations consequence.** Every power-capping, DVFS and energy-accounting decision in this cluster — and every `Joules per X` number in the wider corpus — is downstream of this signal.
- **Compute (as stimulus only).** A dependent-arithmetic CUDA kernel is used purely as a square-wave power source with controllable amplitude (via SM occupancy) and period.

## 12.4 Why the problem exists (hardware root cause)

The reported value is not a sample of instantaneous power. It is the output of a chain with three independent, undocumented time constants [paper]:

1. **The analogue sensing and the GPU's own transient response.** Board power does not step; the observed rise is instantaneous on some generations and multi-hundred-millisecond on others.
2. **A boxcar (moving-average) filter of length `W`** applied inside the firmware/driver.
3. **A publication period `T`** at which NVML makes a new value visible.

The paper's central structural finding is that **`W` and `T` decoupled in the modern generations**: on older parts `W = T` (the filter is contiguous, so all elapsed time is observed), but on A100 and H100 `W = 25 ms` while `T = 100 ms` [paper]. The filter is therefore a *duty-cycled* observer: **75 % of wall-clock time is never inside any averaging window at all.** Anything the GPU does in that 75 % is invisible, and whether a burst lands inside or outside the window is set by an alignment the user cannot control (it depends on boot timing) [paper].

Two further root causes:
- **Query-field semantics differ by generation.** `power.draw` returns an instantaneous reading on pre-Ampere parts but a **1-second average** on Ampere and later; `power.draw.average` (Ampere except GA100, and later) is the 1 s average; `power.draw.instant` is the latest instantaneous reading [paper]. A script written for a V100 silently changes meaning on an A100.
- **Steady-state error is proportional, not fixed.** NVIDIA documents ±5 W; the measurement shows **≈ ±5 %**, with an almost perfectly linear nvidia-smi-vs-PMD relation (**R² > 0.999**) whose gradient and offset vary randomly between physically identical boards [paper].

## 12.5 Mathematical / performance model

The window is recovered by **deliberate aliasing**, not by documentation [paper] [code]:

1. Drive the GPU with a square wave whose period is a rational fraction of the measured update period `T`. The artifact uses exactly `aliasing_ratios = [1/2, 2/3, 3/4, 4/5, 6/5, 5/4, 4/3]` [code, `source/GPU_pwr_benchmark.py:30`].
2. Record `nvidia-smi` and the external PMD simultaneously.
3. Build a boxcar-averaging **emulator** of the sensor with window size `W` as the free parameter, drive it with the PMD trace, and minimise the MSE between emulated and observed `nvidia-smi` power.
4. Optimise `W` by **Nelder–Mead**, initialised at half the update period — the artifact literally initialises `init_vars = [self.pwr_update_freq/2, self.nvsmi_smp_pd/2]` [code, line 1247] and sweeps candidate windows `range(1, pwr_update_freq+10, 2)` [code, line 1287].
5. Repeat **32 times per ratio** (`self.repetitions = 32` [code, line 25]) and report the distribution.

This is the paper's real methodological contribution: the averaging window of a closed-source sensor is identified by *system identification against an external reference*, with the GPU itself as the excitation source.

## 12.6 Data layout and ownership

Not a data-layout paper. The relevant hierarchy is the **measurement** hierarchy [paper]:

| Level | What exists | Observability |
|---|---|---|
| Shunt on the 6/8-pin PCIe power connectors | true board current | external only (PMD) |
| PCIe x16 slot rail | additional board current | external only, via a modified PCIe riser |
| 3.3 V rail | ~10 W | **unmeasured** (stated limitation) |
| On-board sensor → firmware boxcar `W` | filtered power | NVML |
| NVML publication period `T` | one value per `T` | `nvidia-smi` |
| Per-SM / per-HBM-stack | — | **not exposed at all** |

Amplitude is controlled by activating a chosen **percentage of SMs** (0–100 %), which is the only power-domain granularity the GPU offers a user [paper]; the artifact's Experiment 1 sweeps `range(0, 101, 20)` % load [code, line 359].

## 12.7 Pseudo code

Sensor-window identification (reconstructed from the paper's description and the artifact's control flow) `[reconstruction]`:

```
T  <- find_pwr_update_freq()            # median inter-update spacing of nvidia-smi timestamps  [code]
g,c <- find_scale_parameter()           # linear fit niters <-> kernel duration (ms)            [code]
for r in {1/2, 2/3, 3/4, 4/5, 6/5, 5/4, 4/3}:        # [code]
    period <- round(r * T)
    for rep in 1..32:                                 # [code]
        run square wave: period ms high / period ms low, 100% SMs, 4000/period cycles
        log nvidia-smi (timestamp, util, pstate, temp, clocks.current.sm, power.draw*)  # [code]
        log PMD over /dev/ttyUSB0                                                        # [code]
W* <- argmin_W  MSE( boxcar(PMD_trace, W) , nvidia_smi_trace )   # Nelder-Mead, init W = T/2
```

## 12.8 Real implementation

Pinned commit `ab12c0606775e38872501de8a5cf57ca0e863fa1` [code]. Verified symbols only:

- **External instrument path.** `source/PMD.cpp` opens `/dev/ttyUSB0` (`open_serial_port()`), configures 8N1 with `cfsetispeed/cfsetospeed(B115200)`, and authenticates the device by a 17-byte handshake whose expected reply is the literal string **`"ElmorLabs PMD-USB"`** (`handshake()`); `change_baud_rate()`, `config_cont_tx()` and a `pthread` logger `logSerialPort()` implement continuous streaming [code]. The Python side decodes **18 bytes per sample** as **nine `uint16`** values (`struct.unpack('<HHHHHHHHH', sample)`) [code, `GPU_pwr_benchmark.py:658–676`]. This is a genuine, inspectable external-ground-truth path, which is what separates this paper from every model-only power paper in this cluster.
- **GPU-side query.** `--query-gpu=timestamp,utilization.gpu,pstate,temperature.gpu,clocks.current.sm,` plus whichever of `power.draw`, `power.draw.average`, `power.draw.instant` the driver advertises; availability is probed with `nvidia-smi --help-query-gpu` and the fields are de-duplicated at runtime — if `power.draw` is bit-identical to `power.draw.average` the code stops treating it as separate [code, lines 138–318]. That de-duplication is itself evidence for the paper's claim that the field's meaning changes across generations.
- **Stimulus kernel.** `my_first_kernel` in `source/benchmark_load.cu` is a `#pragma unroll` loop of a *dependent* arithmetic chain `x[tid] *= 2; x[tid] += 2; x[tid] /= 2; x[tid] -= 1;` [code]. The paper describes the high state as a "data-dependent chain of vector FMA operations" [paper]; the committed kernel is a mul/add/div/sub chain that is net-identity, so the operand value does not drift over the loop. That is the right design here — it holds the *data* constant so that only the *timing* varies, which is exactly the confound that `GPU-SC25-184` (benchmark-driven energy models) and the corpus's Hopper `wgmma` finding show would otherwise contaminate the power level.
- **CPU-side cross-check.** `_sample_cpu()` polls `/sys/class/thermal/thermal_zone{0..13}/temp` and `psutil.cpu_percent()` at a 10 ms cadence [code, lines ~331–346].

`NOT_INSPECTED`: the plotting/post-processing path beyond the symbols quoted, and the `tests/` CUDA-sample applications.

## 12.9 Kernel execution

Kernel → thread block → warp is used only as a power dial: occupancy across SMs sets amplitude, unrolled dependent FMA-like chains prevent ILP from shortening the high state, and chain length is calibrated to milliseconds by a linear regression of `niters` against measured duration (`_find_scale_parameter`, which doubles `niter` until the kernel exceeds 1000 ms and then fits) [paper] [code].

## 12.10 Memory traffic

NOT_IN_PAPER as a subject. The kernel touches one `float` per thread and is deliberately register/L1-resident so that power is set by arithmetic activity rather than HBM traffic `[inference]`.

## 12.11 Why the measurement is wrong (decomposed cause)

Four distinct error sources, each separately demonstrated [paper]:

1. **Duty-cycled observation.** `W < T` on Ampere/Hopper ⇒ 75 % of runtime unobserved. For a 100 ms kernel only 25 ms is sampled, and reported energy swings with the unknowable phase alignment.
2. **Window-vs-period lag.** With a 100 ms boxcar and a 100 ms period, the value you read now describes activity from ~100 ms ago — so naive time-alignment of power against a kernel timeline is wrong by a whole period.
3. **Transient-response class.** Four behaviours were observed: instant GPU rise with delayed reporting; gradual multi-hundred-ms GPU rise; a **1-second linear lag** on `power.draw.average` (Ampere+); and a ~200 ms logarithmic growth confined to Kepler/Maxwell.
4. **Proportional gain error.** ±5 % per board, random across identical SKUs. On a 700 W part that is ±35 W; the paper scales this to **≈ $1 M/year of accounting error in a 10,000-GPU facility** [paper] — carry the qualifiers, this is an extrapolation from the per-board gain error, not a measured facility bill.

**Per-architecture result table** (all figures [paper]; each is a property of the named architecture, not of GPUs in general):

| Architecture / part | Update period `T` | Averaging window `W` | Consequence |
|---|---|---|---|
| Fermi | no measurement / estimation-based | — | unusable |
| Kepler, Maxwell | 20 ms | — (logarithmic ~200 ms response) | legacy behaviour |
| Pascal, Volta | 20 ms | 10 ms | `W = T/2` |
| Turing | 100 ms | 100 ms | `W = T`, contiguous |
| **A100 (Ampere)** | **100 ms** | **25 ms** | **75 % unobserved** |
| **H100 (Hopper), `instant`** | **100 ms** | **25 ms** | **75 % unobserved** |
| H100, `average` | 100 ms | 1 s | heavy smoothing |
| GTX 1080 Ti | 20 ms | 10 ms | — |
| RTX 3090 | 100 ms | 100 ms | `W = T` |
| **GH200** | **100 ms** | **20 ms GPU / 10 ms CPU** | **80 % of GPU and 90 % of CPU activity overlooked**; `instant` conflates GPU + CPU + (presumably) DRAM |

**Mitigation result** [paper]: naive measurement gives **39.27 % average energy error (up to ~70 % worst case)**; the three-part "good practice" protocol — (i) ≥ 32 consecutive iterations or ≥ 5 s, with 8 evenly spaced controlled delays when `W < T`; (ii) 4 separate trials with randomised inter-trial delays; (iii) discard rise-time repetitions and time-shift to realign — brings it to **4.89 % (σ = 0.25 %)**. That is the "35 % average / 65 % best-case reduction" of the abstract. Applying the measured per-board steady-state gradient/offset as a calibration removes essentially all remaining time-domain error, leaving only the irreducible ±5 % component tolerance.

## 12.12 Hardware generation dependence

Total. This is the rare paper whose *entire* result set is a generation table, and the direction of travel is **backwards**: Turing had a contiguous `W = T = 100 ms`; A100, H100 and GH200 all sample a shrinking fraction of the period (25 %, 25 %, 20 %). Population: **70+ physical GPUs, 25+ models, 12 architectural generations (Fermi→Hopper)**, across Tesla/Quadro/GeForce, PCIe/SXM/mobile, including 5× RTX 3090 (4 Dell, 1 EVGA), 10× H100 (8 university cluster, 2 cloud), 10× A100 (2 SXM4-40GB, 4 PCIe-40GB, 4 immersion-cooled PCIe-80GB) [paper]. The multiple-samples-per-model design is what licenses the claim that the gain error is *board-to-board random* rather than *model-systematic*.

## 12.13 Limitations (the authors' own)

1. Cannot cover all 1000+ variants; representative sampling only.
2. The PMD does not measure the **3.3 V rail** — possible ~10 W underestimate of true board power.
3. PMD vendor software is Windows-only; custom firmware was needed to reach the 5 kHz stream.
4. **Grace Hopper `instant` conflates GPU, CPU and presumably DRAM**, so the GH200 numbers are confounded at source; ACPI power there shows >100 W fluctuations with unexplained discrete noise.
5. No user control over the sensor window's phase — alignment depends on boot timing, so the mitigation is statistical (randomised delays), not deterministic.
6. Graphics workloads (SPECViewPerf) omitted.

**Reviewer-side limitation not stated by the authors:** every number is `nvidia-smi`-vs-PMD. The PMD's own 12-bit ADC (0–200 A at ±0.5 A) is a coarse current reference at low load; the ±5 % proportional error is therefore an *upper bound on disagreement*, not a certified GPU-sensor error `[inference]`.

## 12.14 Relation to prior corpus

- **`GPU-ICS24-01` (Summit GPU memory corruption) — the strongest link in this corpus.** That paper's headline causal claim is that DBEs track the **15-minute power *range*** (a swing of ~33 W), p = 0.00056 after Šidák correction, on **V100**. V100 is a **20 ms period / 10 ms window** part, i.e. `W = T/2` — half the elapsed time is unobserved. A power *range* statistic computed from a duty-cycled sensor is a **lower bound** on the true swing: excursions that fall in the unobserved half are simply missing. This paper does not weaken the Summit finding — it strengthens its direction while making its magnitude untrustworthy. **Any future re-analysis of power-swing-vs-reliability on Ampere or Hopper telemetry must correct for `W/T = 0.25` or it will systematically understate the swing** `[inference, grounded in both papers' measured quantities]`.
- **`GPU-IPDPS24-61` (Hopper microbenchmarking) — direct methodological dependence.** That paper reports `wgmma` drawing **<200 W on all-zero inputs at >95 % of peak vs 350 W on random data, with the clock falling below the whitepaper figure** on an H800. Those are H100-family `nvidia-smi` numbers, i.e. produced by a **25 ms-in-100 ms** observer. The *direction* (zeros cheap, random expensive) is robust because it is a large steady-state difference; the *absolute* 200 W and 350 W figures inherit the ±5 % proportional error and any phase misalignment during the throttling transient.
- **Precursor / competing.** Burtscher et al. 2014 (3× Tesla K20, 15 ms sampling, "capacitor charging" distortion), Aslan et al. 2022 (embedded TX2/Xavier), Fahad et al. 2019 (K40/P100 vs WattsUp, up to 73 % energy error), Sen et al. 2018 (K20c vs a 3 kHz PowerInsight meter), Jay et al. 2023 (8× V100 DGX, qualitative tool comparison) [paper]. This paper's claimed advance is scale (70+ GPUs, 12 generations) and reverse-engineering the whole chain rather than grading the output.
- **Follow-up inside this cluster.** `GPU-ISC26-182` does the equivalent job for AMD and independently rediscovers the same failure mode (undocumented moving-average filtering) with a different workaround (differentiate the energy counter rather than characterise the filter). `GPU-ICS26-183` (Wattchmen) and `GPU-SC25-184` (benchmark-driven models) both *build on* NVML as ground truth and both name its granularity as their own accuracy floor.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution *is* the NVML/`nvidia-smi` sensor's own averaging behaviour and update latency — the discovery that the boxcar window `W` and the publication period `T` are different numbers on Ampere/Hopper/Grace-Hopper, the per-architecture `W`/`T` table, the generation-dependent semantics of the `power.draw*` query fields, and a mitigation protocol written against those specific values. Nothing here transfers to RAPL, to an AMD GPU (whose filter `GPU-ISC26-182` shows is undocumented in a *different* way), or to any "generic accelerator with a power sensor".

verdict: `CORE_GPU`

# GPU-ISC26-182 — Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `N — measurement methodology, tracing & instrumentation (Score-P/PAPI/OTF2)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2604.06056v2) — authors/affiliations, abstract, motivation, the sensor inventory and their electrical scope, the four formalised sensor dimensions (update interval, delay/response/recovery, confidence window with its equation, aliasing), the energy-counter differentiation method, the Score-P/PAPI/APAPI integration and the OTF2 path, fastotf2, both machine configurations, the square-wave and application workloads, the quantitative results, the stated limitations, and the (thin) related-work pointers. PLUS [code] inspection of the fastotf2 artifact at pinned commit 32b85fe8e62e68ecd1d913e82f66c514604fe564. NOT read line-by-line: the full figure set and the per-node distribution plots.`

---

## PRIOR-ANALYSIS DELTA NOTICE (task §4)

`domains/hpc_systems_operations/` **is imported** and already holds a **substantive** record of this paper — the deepest pre-existing record of any paper in this cluster:

- `corpus/aiops-survey/raw/V8_grey_isc.md:27` and `:213` — a `FULL-TEXT` grade, the full author list, affiliations (UT / HPE / AMD / ORNL), **DOI `10.23919/isc.2026.11520492`**, arXiv `2604.06056v2`, both testbeds (Frontier 128 nodes / 512 MI250X; Portage 128 nodes / 512 MI300A), the sources (`rocm-smi`/`amd-smi` + Cray PM counters via sysfs), the **<1 % overhead** claim, and the observation that there is *no Redfish and no fabric telemetry*.
- `synthesis/13_VERIFICATION_ROUND2.md:200` adds the sharpest existing critique: the 1 ms vs 100 ms fidelity argument compares **two rates that are intrinsic to their respective sources, not a swept configuration** — so the paper never isolates rate from sensor.

**What this file adds:** the mechanism rather than the inventory — the four formalised sensor dimensions and the confidence-window equation; *why* the energy counter beats the power field (undocumented moving-average filtering); the electrical scope of the Cray PM tap and its 5 %/1 % validation and 30 W NIC offset; the per-package (not per-GCD) attribution ceiling; the `[code]` state of the fastotf2 artifact; and the cross-vendor comparison against `GPU-SC24-181`, which the operations record does not attempt.

The ISC 2026 census row (`census/ISC_2026.md:55`) is this project's own STEP A/B row; it records `MEMBERSHIP_UNVERIFIED` for ISC 2026 research-track status. The operations corpus supplies a DOI (`10.23919/isc.2026.11520492`) consistent with the ISC 2026 series, which raises but does not close that question — **membership remains `MEMBERSHIP_UNVERIFIED` here**, since no official ISC 2026 program page was reachable.

---

## 12.1 Bibliographic facts

- Official title: *Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes* [paper].
- Authors: **Adam McDaniel, Michael Jantz** (Univ. of Tennessee / UT-Battelle); **Ashesh Sharma, Steve Abbott, Steven Martin, Shreyas Khandekar, Brandon Neth** (HPE); **Bruno Villasenor Alvarez** (AMD); **Aditya Kashi, Wael Elwasif, Oscar Hernandez** (ORNL) [paper]. Affiliation mapping for Villasenor Alvarez is `[inference]` from the operations-corpus record, which lists AMD among the institutions; the arXiv HTML footnote block did not resolve it.
- Venue: ISC High Performance 2026, research track (`MEMBERSHIP_UNVERIFIED`). DOI `10.23919/isc.2026.11520492` [official-web, via the imported operations corpus].
- Publication type: `ARCHIVAL_MAIN_PAPER` (full text read as `PREPRINT`, arXiv `2604.06056v2`).
- Artifact: `https://github.com/hpc-ai-adv-dev/fastotf2`, inspected at pinned commit **`32b85fe8e62e68ecd1d913e82f66c514604fe564`** [code].

## 12.2 Core question (one sentence)

On AMD exascale nodes that expose several power/energy sensors with different electrical scope, cadence and filtering, over which time intervals is an attribution of energy to a program phase actually defensible? [paper]

## 12.3 GPU/HPC problem translation

- **Measurement + scheduling.** The deliverable is a *rule* for when a measurement may be attributed to a phase, plus the tooling that enforces it.
- **Compute.** The application results are a mixed-precision-vs-FP64 energy comparison (rocHPL vs rocHPL-MxP, HPG-MxP), i.e. a statement about what Matrix-Core precision choice costs in Joules.
- **Memory.** MI300A's unified HBM3 removes the host-to-device copy, which is part of why the APU's sensor topology differs from the discrete MI250X's.

## 12.4 Why the problem exists (hardware root cause)

Two sensors, two electrical taps, two clocks, one undocumented filter [paper]:

1. **On-chip (`rocm-smi` / `amd-smi`).** Reports power **and a cumulative energy counter** at **1 ms** granularity on MI250X and MI300A. The **power** field is a *running average with undocumented filtering*; the **energy** counter is not filtered in the same way. MI300A additionally offers a native 1 ms power mode.
2. **Off-chip (Cray PM counters, via Linux sysfs).** Node- and per-GPU-package power/energy refreshing every **100 ms**. Crucially the paper states *what it is electrically*: a measurement of input power **before the final point-of-load voltage conversions**, validated to **within 5 % on Frontier and 1 % on Portage**, and carrying platform-specific static offsets — notably **30 W attributable to NICs on Portage** (APUs 0 and 2 share NIC rails).
3. **Three independent clocks.** Sensor measurement, driver refresh and tool sampling each run on their own timebase; NTP reduces but does not remove sub-millisecond skew.

The consequence is that a 1 ms number and a 100 ms number for "the same" GPU are not two resolutions of one quantity — they are two different quantities measured at two different points in the power-delivery network.

## 12.5 Mathematical / performance model

Two formal objects, both new to this repository [paper]:

**(a) Power reconstruction by differentiating the energy counter.**

```
P_inst(i) ≈ ( E(i) − E(i−1) ) / Δt          with Δt = 1 ms
```

This is the paper's central trick and it is a *bypass*, not a correction: rather than characterise the undocumented moving-average filter on the power field (which is what `GPU-SC24-181` does for NVIDIA), it refuses to use the filtered field at all and differentiates the counter instead, which "reveals short transients that moving-average sensors smooth out" [paper]. Validated by checking that the steady-state mean of `P_inst` matches the averaged sensor value, and cross-checked on MI300A against its native 1 ms power mode.

**(b) The confidence window.** For a phase spanning `[t_s, t_e]`:

```
W_conf = [ t_s + t_d + t_r ,  t_e − t_d − t_f ]
```

with `t_d` the delay between the true power-state change and the first observable update, `t_r` the 10–90 % rise time, and `t_f` the 90–10 % recovery time [paper]. Outside `W_conf` the samples describe the *sensor's* transition, not the program's. This is the paper's real contribution: a falsifiable statement about which samples are allowed to be attributed, expressed in sensor-measured constants.

Four sensor dimensions are characterised to populate it: **update interval** (native cadence vs tool-observable cadence — explicitly distinguished), **delay / response / recovery**, **aliasing** (undersampling produces smoothed or oscillatory artefacts), and **power-excursion capture** (whether brief overshoots above the sustained level are clipped or filtered away).

## 12.6 Data layout and ownership

| Level | Frontier (EX235a) | Portage (EX255a) |
|---|---|---|
| Node | 1× AMD EPYC 7A53 (64 Zen3) + **4× MI250X** | **4× MI300A APU** |
| Accelerator package | MI250X = **2 GCDs**, 64 GB HBM2e each (128 GB) | MI300A = 24 Zen4 cores + **228 CUs** + **128 GB unified HBM3** |
| Power cap | **560 W** (TDP) per MI250X | **550 W** per APU |
| Observed clock | ~**1240 MHz** average during rocHPL | ~**1015 MHz** average during rocHPL |
| Interconnect | HPE Slingshot 200 Gbps, 4 Cassini NICs | same |
| Scale used | **128 nodes / 512 MI250X** | **128 nodes / 512 MI300A** |
| Software | HPE Cray PE, **ROCm 6.4.1** | same |

**Attribution ceiling (stated limitation):** `rocm-smi` reports **aggregate values for the whole package** — the full MI250X (both GCDs) or the whole MI300A (CPU cores *and* GPU CUs together). **Per-GCD and CPU-vs-GPU-within-APU attribution is not observable**, which is a hard limit on how "fine-grained" this can get on an APU.

## 12.7 Pseudo code

`[reconstruction]` from the paper's described procedure:

```
# Phase 1 — characterise the sensor, per platform
for each sensor S in {rocm-smi energy, rocm-smi power, Cray PM}:
    run square-wave kernel: alternate TDP-level FP64 vector-FMA burst / idle,
        user-set duration and iteration count, MPI-synchronised across all GPUs of the node
    measure update_interval(S)        # native vs tool-observable, distribution over 512 devices
    measure t_d, t_r, t_f (S)         # delay, 10-90% rise, 90-10% recovery
    detect aliasing(S) at workload periods approaching the update interval

# Phase 2 — attribute
P_inst[i] = (E[i] - E[i-1]) / dt                      # dt = 1 ms
apply static offsets (e.g. -30 W for NIC-sharing APUs on Portage)
for each Score-P region R:
    W_conf = [R.start + t_d + t_r , R.end - t_d - t_f]
    if W_conf non-empty: energy(R) = integral of P_inst over W_conf
    else:                energy(R) = UNATTRIBUTABLE
```

## 12.8 Real implementation

- **PAPI/Score-P path** [paper]: the `rocm-smi` PAPI component was **extended** to expose the 1 ms **energy** sensors on MI250X and both energy and power on MI300A; Cray PM sensors were added as further PAPI components readable from user space; **Async PAPI (APAPI)** samples each component in a dedicated thread, one per node per component, so the application threads are not perturbed. All streams share one tool timebase and are written to **OTF2**. Overhead **below 1 %**, *conditional on reserving extra cores for the sampling threads* — carry that condition, it is the whole basis of the number.
- **fastotf2** [code], pinned commit `32b85fe8e62e68ecd1d913e82f66c514604fe564`. The repository is a **Chapel** (Mason) project; the tool is `apps/FastOTF2Converter` with modules `CallGraphModule.chpl`, `ConverterDefReaders.chpl`, `ConverterEvtReaders.chpl`, `ConverterGroupMap.chpl`, `Strategy_LocBlock.chpl`, `ConverterWriters.chpl` and `ConverterTimings.chpl`; output formats are **CSV** (seconds) and **Parquet** (nanoseconds); prebuilt containers are published at `ghcr.io/hpc-ai-adv-dev/fastotf2/fastotf2-converter` with OFI/libfabric-CXI images documented for Apptainer on HPC fabrics [code, `README.md`]. **Discrepancy worth recording:** the paper claims "an order-of-magnitude speedup" over the Python `otf2` module; the repository README claims **"40 times faster"** [code]. Neither figure carries a stated trace size or node count, so neither is a portable fact. `NOT_INSPECTED`: the Chapel sources themselves beyond their filenames and the README's interface description.
- **No public artifact** for the sensor-characterisation square-wave kernel or the PAPI component patches was located — `NOT_FOUND_AFTER_SEARCH`.

## 12.9 Kernel execution

The square-wave stimulus is a **double-precision vector FMA** kernel calibrated to draw TDP-level power, exercising bandwidth and compute together, with MPI synchronisation so all GPUs in the node transition simultaneously [paper]. Note the structural similarity to `GPU-SC24-181`'s square wave — two groups, two vendors, independently converging on "drive the device with a square wave and identify the sensor" as the only available method.

## 12.10 Memory traffic

Not a memory-traffic paper. Relevant only in that MI300A's unified HBM3 removes explicit host↔device transfers, and that the FP64 stimulus is chosen to load HBM as well as the FP64 pipes [paper].

## 12.11 Why the result matters (decomposed cause)

1. **The 1 ms/100 ms gap is a Nyquist problem, and the paper says so.** Cray PM at 100 ms aliases any workload whose activity period is below ~200 ms; `rocm-smi` at 1 ms captures the transients but is still filtered.
2. **The filter is defeated, not modelled.** Differentiating the energy counter is strictly more robust than fitting a window, because it needs no knowledge of the filter — but it also means the paper never learns *what* the filter is, so an AMD analogue of `GPU-SC24-181`'s `W`/`T` table still does not exist for any AMD part. **That is the most important open question this cluster can name.**
3. **The confidence window turns "fine-grained" into a testable predicate.** A phase shorter than `t_d + t_r + t_f` has an *empty* window and is declared unattributable rather than silently reported.
4. **Application result** [paper]: on **Frontier (128 nodes, 512 MI250X)**, **rocHPL-MxP reduces node energy by 79 % relative to FP64 rocHPL**, and **HPG-MxP reduces node energy by 31 %** relative to its full-precision run. Carry all three qualifiers — these are *node* energy (not GPU-only), on MI250X at a 560 W cap, for those two benchmarks. The phase-level attribution then separates how much of that came from shorter runtime versus lower instantaneous power, which is the thing the aggregate number cannot tell you.

## 12.12 Hardware generation dependence

Two AMD generations with genuinely different sensor topologies: **MI250X** (discrete, dual-GCD, package-aggregated reporting) and **MI300A** (APU, unified HBM3, CPU+GPU in one package and therefore in one power number, but with a *native* 1 ms power mode the MI250X lacks). The 30 W NIC offset is Portage-specific and explicitly declared non-generalisable.

## 12.13 Limitations (authors' own)

1. `rocm-smi` power fields use **undocumented moving-average filters** on both parts; the window and algorithm remain unknown.
2. Reporting is **package-level**; no per-GCD, and on MI300A no CPU-vs-GPU split.
3. Three asynchronous clocks; NTP reduces but does not eliminate sub-millisecond drift.
4. The confidence window needs `t_d`, `t_r`, `t_f` known a priori, and **short phases may have an empty window**.
5. The 30 W Portage NIC offset needs per-system characterisation.
6. Cray PM at 100 ms aliases sub-200 ms activity.

**Critiques not made by the authors.** (a) As the imported operations corpus already notes, **1 ms and 100 ms are properties of two different sensors, never swept independently** — the paper cannot separate "higher rate" from "different electrical tap". (b) There is **no external ground truth at all** — no wall meter, PDU or oscilloscope; the Cray PM tap is validated "to within 5 %/1 %" but the paper does not say against what. (c) The <1 % overhead holds only with reserved cores, i.e. it is paid in capacity, not eliminated.

## 12.14 Relation to prior corpus

- **`GPU-SC24-181` — the cross-vendor twin, and the two do not cite each other.** Both drive a square wave and interrogate the vendor sensor; both find an undocumented moving average; both find the tool-visible cadence differs from the native cadence. They then diverge: Yang et al. *identify* the NVIDIA boxcar window by aliasing and Nelder–Mead against an **external** ElmorLabs PMD, and can therefore state `W = 25 ms, T = 100 ms` for A100/H100. McDaniel et al. *bypass* the AMD filter via the energy counter and validate only **sensor-against-sensor**. The AMD-side related-work discussion is thin and does not engage the NVIDIA sensor-characterisation literature [paper]. **Finding for this cluster: AMD and NVIDIA power measurement are *not* being treated as the same problem, and no `W`/`T` table exists for any AMD GPU.**
- **`GPU-SC25-184` (LBNL benchmark-driven energy models)** measures MI250X **and** MI300A with `amd-smi` at **1 Hz** — three orders of magnitude coarser than this paper's 1 ms — and reports that **AMD thermal throttling confounds its zero-vs-random datapath separation on exactly those two parts**. Read together, the LBNL confound is a predictable consequence of sampling a throttling device at 1 Hz, and this paper supplies the instrument that would resolve it.
- **`GPU-ICS24-01` (Summit).** The power-swing-vs-DBE result depends on a *swing* statistic. This paper is the AMD-side demonstration that swings below the sensor's response time are structurally unrecoverable from filtered power fields, and that differentiating an energy counter recovers them.
- **Complementary, not competing**, with `GPU-ICS26-183` (Wattchmen): Wattchmen models instruction energy and uses NVML as truth; this paper does not model at all, it fixes the truth.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution is built out of AMD-specific sensor facts — the `rocm-smi`/`amd-smi` 1 ms cumulative-energy counter and its undocumented power-field filter, the Cray PM tap sitting before the final point-of-load conversion with a platform-specific 30 W NIC offset, package-level aggregation that hides MI250X's two GCDs and merges MI300A's CPU and GPU into one number, and MI300A's native 1 ms power mode. The confidence-window equation is generic in form but is parameterised entirely by those measured device constants.

verdict: `CORE_GPU`

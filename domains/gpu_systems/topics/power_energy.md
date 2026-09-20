# GPU power, energy, DVFS, thermal behaviour and energy attribution (taxonomy P)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **STRONG, and the strongest thing it produces is a warning
about its own instruments.** Seven deep analyses (taxonomy `P`), all
`CORE_GPU`, all measured on real silicon. Verdict ledger:
`../corpus/_LEDGER_power_energy.md`. Four of the seven are
`GPU_DELTA_ANALYSIS` against the imported `../../hpc_systems_operations/`
corpus and open with an explicit delta notice.

## 1. Problem landscape

Almost everything published about GPU power is measured with the GPU's own
sensor, and the corpus's first paper here is about what that sensor actually
does. The topic therefore has an unusual shape: a **metrology** layer
(what does the number mean?), an **attribution** layer (which instruction,
functional unit or job spent the Joule?), and a **control** layer (what can be
capped, reallocated or throttled?) — and the metrology layer undercuts parts of
the other two.

`../corpus/_LEDGER_power_energy.md` applies the counterfactual strictly: three
papers whose subject is GPU power but whose *mechanism* treats the GPU as a
black box with a frequency knob — **throttLL'eM, EVeREST and TAPAS** — are
`RELATED_GPU` and **not deep-analysed, even where the full text was read.**

## 2. Key concepts

NVML / `nvidia-smi` `power.draw` vs `power.draw.average`; the sensor's
**boxcar averaging window `W` and reporting period `T`**, and `W < T` as a
duty-cycle problem; AMD `rocm-smi` at 1 ms vs Cray PM at 100 ms, and the
energy counter as a filter bypass; external ground truth (a PMD) vs
sensor-against-sensor validation; per-instruction (SASS) vs per-functional-unit
(pJ/bit, pJ/FLOP) energy models; **control power vs datapath power**; TDP
clamping and the "rounded Roofline"; power capping latency; positional thermal
imbalance in an air-cooled chassis; power as a *shared, unpartitioned* resource
across a node.

## 3. Main mechanism families

**Family P1 — characterise the instrument.**
`../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md`
(NVIDIA) and
`../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md`
(AMD).

**Family P2 — build an additive energy model from microbenchmarks.**
`../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md`
(unit = the SASS instruction) and
`../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md`
(unit = the functional unit and memory level).

**Family P3 — characterise thermal and power behaviour at cluster scale.**
`../corpus/GPU-MICRO25-185--distributed-training-power-performance-thermal.md`
and `../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md`.

**Family P4 — exploit an imbalance you have just measured.**
`../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md`.

## 4. Representative papers

- **Accurate and Convenient Energy Measurements for GPUs** (SC 2024) —
  **MEASURED**, and **the only paper in this topic with a real external ground
  truth** (an ElmorLabs PMD). Four separately demonstrated error sources
  `[paper]`: **duty-cycled observation** — `W < T` on Ampere/Hopper means
  **75% of runtime is unobserved**, so for a 100 ms kernel only 25 ms is
  sampled and reported energy swings with an unknowable phase alignment;
  **window-vs-period lag** — with a 100 ms boxcar and a 100 ms period, the
  value read now describes activity from ~100 ms ago; **four distinct transient
  response classes**, including a **1-second linear lag on
  `power.draw.average` (Ampere+)**; and **±5% proportional gain error per
  board, random across identical SKUs** — on a 700 W part, ±35 W. The paper
  scales that to **≈$1 M/year of accounting error in a 10,000-GPU facility**;
  **carry the qualifier — that is an extrapolation from the per-board gain
  error, not a measured facility bill.** Establishes `W = 25 ms, T = 100 ms`
  for A100/H100.
- **Fine-grained power and energy attribution on AMD GPU/APU** (ISC 2026) —
  **MEASURED** on **MI250X** (discrete, dual-GCD, package-aggregated
  reporting) and **MI300A** (APU — CPU and GPU in **one** power number, but
  with a *native* 1 ms power mode the MI250X lacks). The 1 ms/100 ms gap is a
  **Nyquist problem**: Cray PM at 100 ms aliases any workload whose activity
  period is below ~200 ms. The filter is **defeated, not modelled** —
  differentiating the energy counter needs no knowledge of the filter, but the
  paper therefore never learns what the filter is, so **no `W`/`T` table exists
  for any AMD part** `[paper]`. Application result on **Frontier (128 nodes,
  512 MI250X)**: **rocHPL-MxP reduces node energy by 79% relative to FP64
  rocHPL**, **HPG-MxP by 31%** — *node* energy, on MI250X at a 560 W cap, for
  those applications. The 30 W NIC offset is Portage-specific and **explicitly
  declared non-generalisable**.
- **Wattchmen** (ICS 2026) — **MEASURED**, MAPE over 16 workloads, each figure
  with its SKU *and cooling* qualifier `[paper]`: **V100 air-cooled (CloudLab,
  12 GPUs)** — AccelWattch 32%, Guser 25%, Wattchmen-Direct 19%,
  **Wattchmen-Pred 14%**; **V100 water-cooled (Summit)** — AccelWattch 17%,
  Wattchmen-Direct 15%, **Pred 14%**; **A100 air-cooled (Lonestar6, 252
  GPUs)** — Direct 13% at 70% instruction coverage, **Pred 11% at 93%
  coverage**. Generation dependence shows up as **instruction coverage: 70% on
  A100 but 66% on H100**, because of new Tensor-Core opcodes — **every new
  Tensor-Core generation reopens the coverage hole**.
- **Benchmark-driven energy attribution** (SC 2025) — **MEASURED** across
  **four process nodes and two vendors by construction: N7 A100 → N6 MI250X →
  N5 MI300A → N4 GH200**. The zero/random subtraction is a **physical, not
  statistical, separator** — it exploits CMOS switching activity directly.
  Application validation on A100 across MILC (QUDA), BerkeleyGW Epsilon and
  Sigma, LAMMPS via EXAALT, and **GPT-NeoX (125 M params, 200 training
  steps)**: constant power **~15% of total**; **control power often >50%**;
  data movement **40–60% of total** for MILC and BerkeleyGW `[paper]`.
- **Distributed training power, performance and thermal** (MICRO 2025) —
  **MEASURED** on **air-cooled 32–64-GPU clusters** across three SKUs and two
  vendors (H100, H200, MI250). **Up to 27% temperature differential between
  rear and front GPUs** on HGX H100/H200; **5–10 °C intra-package skew** on
  MI250; **rear GPUs show no clear cooldown periods** `[paper]`. Throttling
  scales with pipeline depth (PP16–32 throttle more, TP-heavy less);
  compute–communication overlap **consistently increases** peak temperature;
  activation recomputation **cuts both ways** — reducing throttling in deep-PP
  GPT3-175B and *increasing* it in data-parallel Llama3-70B. **The results are
  chassis-dependent as much as GPU-dependent** and would not transfer to
  direct-liquid-cooled H100 or MI300A nodes.
- **POLCA** (ASPLOS 2024) — **PRODUCTION FLEET + MEASURED**, A100 40/80 GB,
  with facility-level PDU telemetry at row granularity. **Inference clusters
  leave ~20% of provisioned power unused; training clusters ~3%** (peak power
  utilisation **79% vs 97%**; max 2-second spike **11.8% over 40 s inference vs
  37.5% over 2 s training**) `[paper]`. **Input length drives peak power;
  output length does not** — raising the prompt 256 → 8192 tokens pushes peak
  power sharply up while mean power stays flat. Frequency reduction buys power
  superlinearly: **up to 20% peak power for at most ~7% performance loss** on
  inference; GPT-NeoX loses *no* performance at ~13% peak reduction while
  BLOOM-176B loses 5% at the same setting. At iteration boundaries **power
  falls to 75% of TDP (RoBERTa), 50% (GPT-NeoX) and 20% (Flan-T5, the idle
  floor)**, coherently across thousands of GPUs. Result: **30% more servers in
  a 40-server row** within SLOs, with **zero powerbrake events across a
  six-week trace** against 10¹–10⁴ for baseline policies.
- **Lit Silicon** (ISCA 2026) — **MEASURED only on AMD MI300X**, 8-GPU nodes,
  Llama 3.1 8B / Mistral 7B under FSDP. Three mitigations `[paper]`: **GPU-Red**
  (lower the cap on leaders only, which were burning power to wait) — **0%
  throughput change, −4% power**; **GPU-Realloc** (move power from leaders to
  the straggler under a fixed node cap) — **+3% throughput, 0% power**;
  **CPU-Slosh** (harvest CPU power — only **13.5% of CPU cores are utilised**
  during training) — **+4% throughput, +3% power**. The authors' claim that the
  effect "theoretically applies to all systems with multiple devices in a node,
  where per-device DVFS is equipped" **is a hypothesis, not a measurement**,
  and this corpus treats it as such.

## 5. Historical lineage

- **Data-dependent GPU power is a nine-year measurement lineage, not a
  curiosity**, verified from the SC 2025 paper's own citations: Lucas et al.
  2016 (ALUPower) → Bhalachandra et al. 2022 (confirmed on modern GPUs, and the
  source of the random-vs-zero methodology) → Gregersen et al. 2025 → the SC
  2025 control/datapath decomposition `[paper]`. The corpus's Hopper
  microbenchmarking paper
  (`../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md`)
  independently observes the same effect from the throughput side: **zero
  inputs under 200 W at >95% of peak; random inputs at the 350 W limit with the
  clock below the 1620 MHz whitepaper figure**.
- **Sensor characterisation is a two-vendor, non-converging line**: SC 2024
  (NVIDIA, external PMD, `W`/`T` recovered by aliasing and Nelder–Mead) and
  ISC 2026 (AMD, energy-counter differentiation, filter bypassed not
  characterised). **They do not cite each other** (§7, T2).
- Two arXiv preprints carry **different titles from their published versions**,
  recorded so no future pass re-runs the search: SC '24 = arXiv **2312.02741**
  *"Part-time Power Measurements: nvidia-smi's Lack of Attention"*; ASPLOS '24
  = arXiv **2308.12908** *"POLCA: Power Oversubscription in LLM Cloud
  Providers"*. Generation detail: `../synthesis/GPU_HARDWARE_GENERATION_MAP.md`.

## 6. Implementation families

All seven are `REAL_SILICON`; **there is no simulator paper among this topic's
deep analyses.** Instrumentation is the real axis, and
`../corpus/_LEDGER_power_energy.md` §2 tabulates it per paper (sensor, sampling
rate, averaging behaviour, external ground truth). Two papers combine fleet
telemetry with instrumented runs (POLCA, and the reliability-side papers in
`reliability_operations.md`).

## 7. Important disagreements / tensions

**T1 — the topic's own instrument audit, and it is damning.** Of ten papers
with any instrumentation record in `../corpus/_LEDGER_power_energy.md` §2,
**exactly one has a real external ground truth** — and it is the paper whose
whole subject is the sensor. One more has facility-level PDU telemetry. **The
remaining eight validate a GPU power number against a GPU power sensor, or do
not say what they measured with at all. Three papers — one of them an ISCA 2026
paper whose headline claim is a 4% power saving — do not disclose their sensor,
their sampling rate, or both.**

**T2 — AMD and NVIDIA power measurement are not being treated as the same
problem, and the two characterisation papers do not cite each other.** Both
drive a square wave and interrogate the vendor sensor; both find an
undocumented moving average; both find the tool-visible cadence differs from
the native cadence. They then diverge: the NVIDIA paper **identifies** the
boxcar window against an **external** PMD and can state `W = 25 ms, T = 100 ms`;
the AMD paper **bypasses** the filter and validates **sensor-against-sensor**
only `[paper, both]`. **Finding: no `W`/`T` table exists for any AMD GPU.**

**T3 — the two energy models are the two halves of a thing nobody has
assembled, and neither cites the other.** Wattchmen's unit is the **SASS
instruction** — finer, but NVIDIA-only and occupancy-blind; the SC 2025 model's
unit is the **functional unit and memory level in pJ/bit and pJ/FLOP** with a
control-vs-datapath split — coarser, but cross-vendor and four-generation
`[paper, both]`. Wattchmen also **depends on, but does not cite,** the SC 2024
sensor paper: its stated NVML-granularity limitation *is* the phenomenon that
paper quantified.

**T4 — a consequence for every power number in this corpus, stated as an
inference.** Because the datapath is **8–35% of HBM energy** and the rest is
content-independent control, **any GPU power or energy number measured with a
benchmark that uses zero-filled or constant-filled input buffers is a lower
bound on the real datapath energy** — potentially by the full datapath
fraction. `[inference, grounded in the SC 2025 paper's 8–35% datapath share and
the Hopper 200 W/350 W gap]`.

**T5 — power is a shared, unpartitioned resource, and three papers say so from
three directions.** `../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md`
shows **MIG does not partition power** — a co-tenant that pushes the device
into throttling slows every instance. Lit Silicon shows the *same* coupling
across a node and turns it into a 3–4% gain. POLCA shows it at rack scale, as
coherent iteration-boundary swings across thousands of GPUs. **None of the
three frames it as the same phenomenon.**

**T6 — a cross-topic bridge neither side made.** POLCA measures training power
falling to **20–75% of TDP at every iteration boundary, coherently across
thousands of GPUs**;
`../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md` measures **≈33 W
short-term power swings as the covariate that predicts GPU double-bit memory
errors** on V100, with temperature insignificant. **Neither paper cites the
other.** Together they suggest synchronous distributed training is a
power-swing *generator* — `[inference, grounded in both papers' measured
quantities]`, not a finding either paper makes.

## 8. Current limitations

**Bounded by disclosure, not only by access — and that is this topic's
distinctive limitation.** T1 is not fixable by fetching more PDFs: the sensor
provenance is missing from the papers themselves.

**Bounded by full-text access** in the usual way: `dl.acm.org` → 403,
`ieeexplore.ieee.org` → 418, `dblp.org` and `escholarship.org/search/`
robots-disallowed, `api.semanticscholar.org` worked once then rate-limited
(429). Several ACM/IEEE-only papers are `CLOSED_ACCESS` **as an access-path
fact about this environment, not a claim about their licence**
(`../synthesis/GPU_PENDING_FULLTEXT.md`).

Other bounded areas:
- **Lit Silicon is one part on one vendor** (MI300X). Its generalisation claim
  is explicitly a hypothesis. Note also that MI300A reports power **per
  package**, mixing CPU and GPU — which would make CPU-Slosh accounting harder
  to audit on an APU than on the discrete part used here.
- **Thermal results are chassis results.** Everything in MICRO 2025 is
  air-cooled; there is **no direct-liquid-cooled arm** anywhere in this topic.
- **Every LLM-serving power paper carries `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`**
  because `../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`, and **no claim
  is made about what that corpus holds**
  (`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).
- The two imported operations topic files
  (`../../hpc_systems_operations/topics/power_cooling.md` and
  `../../hpc_systems_operations/topics/gpu_operations.md`) state plainly that their coverage is
  **predominantly practitioner/vendor** with "no dedicated power/cooling
  research-audit document". They create **no duplication** with this topic and
  **no claim here contradicts them**.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. Produce the AMD `W`/`T` table (T2). It requires an external PMD on an
   MI250X/MI300A and nobody in this corpus has run that experiment.
2. Compose T3's two models into one cross-vendor instruction-and-hierarchy
   energy model. Both halves exist; the join does not.
3. Test T6 directly: instrument iteration-boundary power swings on a fleet with
   RAS logging and check the covariate Summit found. This needs one machine
   that does both, and the corpus names none.
4. Re-run any headline power number from this corpus with random rather than
   zero-filled inputs (T4) and report the delta.

## 10. Deeper lookup paths

`../corpus/_LEDGER_power_energy.md` — **§2 the instrumentation-chain roll-up**
(the single most useful table this cluster produces; `NOT_STATED` means the
paper does not say), §3 the `GPU_DELTA_ANALYSIS` record against the imported
operations corpus, §4 the seven cross-cluster census corrections this pass made
→ the seven analyses above → the papers and their artifacts.
Cross-topic: `reliability_operations.md` (T6's other half, and the
counter-stability hazard), `runtime_scheduling.md` (T5's MIG evidence),
`gpu_core_execution.md` (data-dependent matrix-instruction throughput, the
same physics from the performance side).

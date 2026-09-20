# GPU faults, telemetry and production performance (taxonomy O)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **SMALL BUT DENSE — four deep analyses, and all four are
production/fleet studies on named machines.** Taxonomy `O`. Verdict ledger:
`../corpus/_LEDGER_profiling_reliability.md` (shared with
`profiling_debugging.md`, taxonomy `N`).
All four are `GPU_DELTA_ANALYSIS` against pre-existing but shallow records in
the imported `../../hpc_systems_operations/` corpus; each file opens with an
explicit delta notice.

## 1. Problem landscape

This is the only topic in the GPU corpus where **every deep analysis is
measured on a production fleet rather than on a testbed or a simulator**:
Summit (27,756 V100s), Delta/DeltaAI (A100 and GH200), Perlmutter (A100) and
Frontier (MI250X). That gives it a kind of evidence no other topic has, and a
corresponding fragility — the population is whatever those four centres ran.

The topic's two halves turn out to constrain each other. **Reliability** work
establishes that GPU memory fails in device- and budget-specific ways.
**Production performance** work then shows that measurable GPU degradation
**does not reach application runtime**. Together they set a bar that any
"GPU health telemetry predicts slowdown" claim must now clear (§7, T3).

## 2. Key concepts

Single- and double-bit errors (SBE/DBE) in HBM; XID codes 48 / 63 / 64;
**page retirement** (Volta, 64-entry table) vs **row remapping** (Ampere and
Hopper, 512-row cap) as the repair mechanism, and page-retirement failure
(PRF) vs remap failure as its exhaustion; GSP (GPU System Processor) firmware;
MTBE per GPU vs per GB; DCGM fields and the `GPU_UTIL` vs `SM_ACTV` semantic
trap; temporal imbalance within a job; exclusive allocation and GPU stranding;
Spearman correlation as a falsification instrument; NIC counters
(`rh:sct/spt_timeouts`) and dragonfly placement.

## 3. Main mechanism families

**Family O1 — fleet-scale failure characterisation of one GPU generation.**
`../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md` (Volta/HBM2).

**Family O2 — cross-generation resilience comparison.**
`../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md`
(A100/HBM2e vs H100/HBM3 as GH200).

**Family O3 — observational telemetry over a whole job population, no
control.** `../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md`.

**Family O4 — controlled repeated runs of a few applications, no population
coverage.** `../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md`.

O3 and O4 are **the same group, same venue, complementary by construction**,
and the corpus says so: "this paper is observational over the whole job
population with no control, its companion is controlled repeated runs of four
applications with no population coverage" `[paper, GPU-IPDPS26-41 §12.14]`.

## 4. Representative papers

- **Understanding GPU Memory Corruption at Extreme Scale: the Summit Case
  Study** (ICS 2024) — **PRODUCTION FLEET**: NVIDIA **Tesla V100, 16 GB HBM2,
  6 per IBM AC922 node**, 27,756 GPUs. Decomposes corruption into four
  separable causes `[paper]`: **per-device predisposition** (manufacturing
  variability plus accumulated lifetime activity) determines *which* GPUs can
  fail — **112 of 28,000, one accounting for 10.5%**; **short-term power
  transients** (**≈33 W swings over 15 minutes**) determine *when* a
  predisposed device fails, **not steady-state temperature** (≈1.5 °C,
  insignificant; p = 0.00056 Šidák-corrected for the power effect); **workload
  arithmetic mix** correlates at application level (4 of 5 susceptible
  applications use mixed precision); and **driver/OS software** determines the
  *observed* failure rate independent of hardware. The first is a property of
  the device, the third of the workload, the fourth of the measurement stack —
  "conflating them is exactly the error the paper is written to prevent."
- **A Story of Two GPUs** (SC 2025) — **PRODUCTION FLEET**: A100 (40 GB HBM2e,
  4-way and 8-way SXM/PCIe nodes) vs H100 (96 GB HBM3, delivered as **GH200
  Grace-Hopper Superchips** with NVLink-C2C) `[paper, v4]`. Three independent
  effects `[paper]`: a **capacity effect** (2.4× more HBM per GPU) that
  accounts for most of the regression — visible as the gap between **3.2× lower
  per-GPU MTBE** and **only 24% lower per-GB**; a **technology effect** (HBM3
  signalling voltage, more stacks, worse thermal path) as the residual ~24%
  per-GB; and a **mitigation-budget effect** — the **512-row remap cap is
  unchanged from Ampere to Hopper** (64 on pre-Ampere), which turns a
  manageable per-GB degradation into *observed remap failures*. **The third
  effect is a design decision, not physics, and is the paper's actionable
  finding.**
- **Production GPU Workloads and System Telemetry** (IPDPS 2026) —
  **PRODUCTION FLEET**: **Perlmutter**, NVIDIA **A100** 40 GB and 80 GB, 4 per
  node, NVLink 3.0, PCIe 4.0, AMD EPYC 7763 host; **one month, March 2025,
  75,703 jobs** `[paper]`. Decomposes low observed utilisation into four
  separable causes: **allocation granularity** (exclusive 4-GPU node allocation
  strands GPUs — **12% of 4-GPU jobs used one GPU**); **scaling loss**
  (utilisation falls from ~47% at 33–512 GPUs to **~20% median at ≥512 GPUs**);
  **burstiness, not slowness** (temporal imbalance above 0.70 in **66.3%** of
  low-utilisation jobs); and **pipeline mismatch** (**44% of jobs use the FP64
  pipe only**, leaving the tensor pipe dark; tensor-using jobs show 50% mean
  utilisation against 36% for FP64-only). **Single-vendor by construction** —
  DCGM is NVIDIA-only.
- **The Case of the Elusive Application Performance** (IPDPS 2026) —
  **PRODUCTION, CONTROLLED**: **Perlmutter (A100)** and **Frontier (MI250X,
  CDNA2, 2 GCDs per package)**, both on **HPE Slingshot-11, 3-hop dragonfly,
  Cassini NICs** `[paper]`. Tests five candidate causes of run-to-run
  variability and disposes of each: **slow individual GPUs — REJECTED** (real
  heterogeneity exists, **up to 28% system-wide on Perlmutter, 12% per-GCD on
  Frontier**, but **Spearman 0.07–0.08** against slowest-1%/10%/30% GPU counts);
  **dragonfly placement — REJECTED** (0.33 and 0.08); **network contention from
  concurrent jobs — ACCEPTED** (top-user node occupancy correlates 0.55–0.60;
  ≥7% AMG2023 degradation above ~300 top-user nodes); **NIC-level loss and
  backpressure — ACCEPTED and predictive** (Direction Accuracy **collapses to
  chance** when NIC counters are removed); **host communication software —
  ACCEPTED and remediable** (the libfabric 1.20.1 regression fixed on
  **14 January 2025** measurably reduced AMG2023 variability). Variance instead
  sits in GPU-resident collectives — **NCCL/RCCL `Allreduce` up to 24× slower
  on Frontier**.

## 5. Historical lineage

- **A three-generation series on one failure mechanism, verified from the
  papers' own XID vocabulary (48/63/64)**: GDDR (Kepler/Titan era, cited)
  → **HBM2 (Volta/Summit,** `GPU-ICS24-01`**)** → **HBM2e/HBM3 (Ampere/Hopper,**
  `GPU-SC25-01`**)**. The repair mechanism changes under it: 64-entry page
  retirement → 512-row remapping. **A PRF on Volta and an XID 64 remap failure
  on Ampere are analogous but not identical events** `[paper]`.
- **A per-generation prediction the corpus can state and not yet test**: unless
  the spare-row budget scales with capacity, the regression worsens on
  larger-HBM parts — which is exactly what *Microbenchmarking NVIDIA's
  Blackwell Architecture* (`../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md`,
  B200 vs H200) is positioned to test `[../corpus/_LEDGER_profiling_reliability.md §5.3]`.
- **Predecessor within the operations corpus**: *The Case of Performance
  Variability on Dragonfly-based Systems* (Bhatele et al., IPDPS 2020) — the
  same question one architecture generation earlier, on CPU-era machines.
  Recorded as `[inference]` from the operations corpus, **not verified from
  `GPU-IPDPS26-42`'s own reference list**.
- Generation-dependence detail: `../synthesis/GPU_HARDWARE_GENERATION_MAP.md`.

## 6. Implementation families

All four are `PRODUCTION_TELEMETRY` studies. Instrumentation differs and the
difference matters: DCGM + LDMS + Slurm over a whole job population (O3); a
purpose-built **per-GPU FP16 GEMM instrument** plus NIC counters and a
gradient-boosted attribution model (O4); centre RAS logs and XID streams
(O1, O2). **There is no simulator and no vendor-supplied model in this topic.**

## 7. Important disagreements / tensions

**T1 — the two reliability papers disagree about the binding constraint, and
both are right about their own machine.** Summit locates it in **per-device
predisposition plus short-term power swings** (≈33 W, p = 0.00056
Šidák-corrected; temperature level insignificant at ≈1.5 °C), explicitly
overturning the Titan-era cooling-geometry account. Delta locates it in the
**unchanged 512-row repair budget**. Same XID vocabulary, different mechanism,
different generation `[paper, both]`. Neither is a refutation of the other and
the corpus does not resolve them to a single story.

**T2 — three independent papers establish that a software change can move a
hardware counter by orders of magnitude.** `GPU-ICS24-01` reports a **RHEL 8
update on 18 August 2021 correlating with a 170-fold increase in
page-retirement-failure counts** from 1 September 2021. `GPU-SC25-01`'s authors
**refuse to attribute H100's zero observed NVLink errors to hardware
improvement**, because they cannot rule out "potential changes in NVLink error
logging mechanisms" `[paper, v4]`. `GPU-IPDPS26-42` documents the libfabric
1.20.1 regression and its dated fix. **This is a standing methodological hazard
for any longitudinal GPU-fleet study**, and it is the strongest
corpus-internal reason to distrust a counter trend line.

**T3 — production performance research has already falsified the
GPU-degradation story, which constrains what reliability telemetry may
claim.** `GPU-IPDPS26-42` builds the instrument, measures real device
heterogeneity (28% system-wide on Perlmutter; 12% per-GCD on Frontier), and
shows it **does not reach application runtime** (Spearman 0.07 and 0.08,
unchanged at 10% and 30% thresholds). **Any claim that GPU health telemetry
predicts application slowdown must now clear this bar.** The prior operations
corpus reached the same conclusion from a different angle
`[../../hpc_systems_operations/ ... 02_PAPER_CENSUS.md M-25]`.

**T4 — the corpus's own architecture-facing finding, and it points away from
where the silicon is going.** `GPU-IPDPS26-41` finds **44% of jobs are FP64-only
and the tensor pipe is idle for most of the population** on Perlmutter.
That is the production-side counterpart to the architecture-level question of
whether Tensor Cores are the right area investment — and it sits beside
`../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md`'s
finding that **`tcgen05.mma` has no FP64 support** and that TMEM "does not
benefit scientific HPC workloads directly". The two are not in citation
contact; the juxtaposition is `[inference]`.

**T5 — a cross-topic bridge neither side made.** `GPU-ICS24-01`'s power-swing
finding and `../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md`'s
measurement that training power falls to **20–75% of TDP at every iteration
boundary, coherently across thousands of GPUs**, measure the same physical
phenomenon from opposite sides. **Neither paper cites the other.** Together
they suggest synchronous distributed training is a power-swing *generator*, and
that such swings are the covariate Summit found predicts memory failure
— `[inference, grounded in both papers' measured quantities]`, not a finding
either paper makes.

## 8. Current limitations

**This topic is bounded by which machines publish, not by full-text access —
and that is a different and sharper limitation.** Four analyses, four centres:
OLCF Summit, NCSA Delta/DeltaAI, NERSC Perlmutter, OLCF Frontier. There is **no
cloud-fleet study and no non-US-centre study** among the deep analyses. A
per-GPU or per-GB failure rate from this corpus is a statement about those
machines' populations, procurements and software stacks.

Specific bounded areas:
- **Counter access is a binding vendor dependence.** `GPU-IPDPS26-42` had
  Cassini NIC counters but **Rosetta switch counters were not available** — the
  analysis stops at the endpoint because the fabric interior is closed
  `[paper]`. No amount of further reading fixes this.
- **O3 is single-vendor** because DCGM is NVIDIA-only; there is no AMD or Intel
  arm to its population study.
- **Existence unverified, do not carry forward as real papers**: *GPU Faults
  Across Cloud Providers* (SC 2026 seed) and *SigmaTrace* (SC 2026 seed), both
  census `NOT_FOUND`. The first is precisely the cloud-fleet study this topic
  lacks, and it may not exist.
- **Verdict genuinely unresolved (4)** in the shared ledger: *GVARP* (SC 2024),
  *Demystifying the Resilience of LLM Inference* (SC 2025), *ATTNChecker*
  (PPoPP 2025), plus the two non-existent seeds.
- Two further papers would owe a `GPU_DELTA_ANALYSIS` if ever analysed:
  *Fine-grained Automated Failure Management* (substantive prior analysis at
  `raw/A_SC_main.md` **S25-1**) and *Interpretable Analysis of Production GPU
  Clusters* (`02_PAPER_CENSUS.md` **M-23**)
  (`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).

**A generalisation warning the papers themselves give**: Summit's authors argue
their *physical* findings are "likely to manifest in other HBM2 GPUs" — **that
is a claim about HBM2, not about Ampere or Hopper** `[paper]`. `GPU-IPDPS26-41`
separates what transfers (the `GPU_UTIL` vs `SM_ACTV` trap, the 10-second
sampling floor, exclusive-allocation stranding — properties of the
DCGM/LDMS/Slurm stack) from what does not (the Ampere-specific pipe
decomposition, the 40 GB vs 80 GB finding specific to Perlmutter's split
procurement).

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. Does the spare-row-budget prediction (§5) hold on B200? The corpus has the
   measurement vehicle and not the measurement.
2. T5 is a testable joint hypothesis across two venues and two communities:
   are iteration-boundary power swings in synchronous training the covariate
   Summit found? Neither paper's data alone can answer it.
3. Given T3, what *would* a predictive GPU-health signal look like? The
   corpus's strongest predictor of application variability is a **NIC counter**,
   not a GPU one.

## 10. Deeper lookup paths

`../corpus/_LEDGER_profiling_reliability.md` — §2.4 and §2.5 (the reliability
and production-telemetry verdict-only tables), §4 the `GPU_DELTA_ANALYSIS`
record, **§5.3, §5.4 and §5.7** (the HBM repair-budget bridge, the falsified
degradation story, the counter-stability warnings), §6 the watchlist →
the four analyses above, each of which opens with its delta notice against
`../../hpc_systems_operations/` → the papers.
Cross-topic: `profiling_debugging.md` (the `N` half of the same ledger),
`power_energy.md` (the power-swing side of T5 and the sensor-provenance
question), `memory_virtualization.md` (HBM as capacity rather than as a failure
population).

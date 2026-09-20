# GPU-ICS24-01 — Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `O — reliability, telemetry & production GPU performance`
secondary_topics: `GPU memory hierarchy (HBM2 ECC, page retirement); survival analysis on production telemetry`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — author-hosted PDF (christian-engelmann.de/publications/oles24understanding.pdf) read for authors/venue/DOI, Summit configuration, XID and telemetry data sources, released dataset DOI, the numbered Findings, the DBE distribution and streak analysis, the power-vs-temperature statistical result with p-values, the Cox-regression application analysis, HBM2/ECC/page-retirement mechanism description, operational implications and the authors' stated limitations. NOT read line-by-line: the full figure set, the complete Findings list beyond those quoted, and the related-work section.`

---

## PRIOR-ANALYSIS DELTA NOTICE (mandatory, per task §4)

An existing document in this repository mentions this paper, but **only as a one-line census row and as lineage evidence** — not as a substantive analysis. This file is therefore a **GPU_DELTA_ANALYSIS** written against a shallow pre-existing record.

What already exists, in `domains/hpc_systems_operations/corpus/aiops-survey/`:
- `synthesis/02_PAPER_CENSUS.md` — a single table row: *"27,648 V100. DBE가 동일 GPU에 재발하며 온도가 아니라 지속 전력과 상관"* (DBEs recur on the same GPU and correlate with sustained power, not temperature), with the DOI, plus a flag that author order differs between sources.
- `raw/D_workshops.md` — cites it as the *archival promotion* target proving that GPU reliability work escapes workshops into archival venues, with a parenthetical *"(27,648 V100s; DBEs recur on the same GPUs; correlated with sustained power, not temperature)"*.
- `raw/H_centers.md` — a bibliography line under OLCF center evidence.
- `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` — places it at the end of the verified OLCF lineage: Titan GPU records → SC20 *GPU Lifetimes on Titan* → Summit XID/DBE dataset release `10.13139/OLCF/1970187` → this ICS'24 paper.

**Author-order discrepancy resolved.** The operations corpus flags that sources disagree on author order (it lists "Shin, Oles, Schmedding, Ostrouchov, Smirni, Wang" in one place and "Schmedding, Shin, Oles, Ostrouchov, Smirni, Wang" in another). The paper itself gives: **Vladyslav Oles (ORNL), Anna Schmedding (William & Mary), George Ostrouchov (ORNL), Woong Shin (ORNL), Evgenia Smirni (William & Mary), Christian Engelmann (ORNL)** [paper]. Note that *Engelmann*, not *Wang*, is the final author — both prior records are wrong on the last author.

**What this file adds beyond the pre-existing record:** the actual mechanism (SECDED on HBM2, the *page-retirement* table and its 64-page cap, which is a different and weaker mechanism than the row remapping of Ampere/Hopper); the precise statistical result behind "power not temperature" including the effect size and corrected p-value; the page-retirement-failure finding and the RHEL8 software-induced 170-fold PRF increase, which the prior record omits entirely; the spatial-locality and GPU-slot result; and the mixed-precision application finding.

---

## 12.1 Bibliographic facts

- Official title: *Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study* [paper]. `CONFIRMED_IN_POPULATION` as entry 16 of the official ICS 2024 accepted-papers page, Session 5A "Reliability, Dependability and Availability" (`census/ICS_2024.md`).
- Authors: Vladyslav Oles (ORNL), Anna Schmedding (William & Mary), George Ostrouchov (ORNL), Woong Shin (ORNL), Evgenia Smirni (William & Mary), Christian Engelmann (ORNL) [paper].
- Venue: ICS '24, 38th ACM International Conference on Supercomputing, June 4–7 2024, Kyoto, Japan. DOI `10.1145/3650200.3656615` [paper].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: author-hosted PDF `https://christian-engelmann.de/publications/oles24understanding.pdf` [official-web]. An author slide deck also exists at `…/oles24understanding.ppt.pdf` — that would be `[author-presentation]` evidence and was not used here.
- **Released dataset:** `https://doi.org/10.13139/OLCF/1970187`, released April 2023, containing GPU error logs, node boot logs, per-node job-scheduler history, and snapshot datasets [paper]. This is a genuine public GPU-reliability data asset.

## 12.2 Core question (one sentence)

On a 27,000-GPU HBM2 machine, what actually precipitates uncorrectable GPU memory corruption — is it a random per-bit process, a thermal effect, a per-GPU predisposition, or an application-driven one? [paper]

## 12.3 GPU/HPC problem translation

- **Memory.** Squarely a GPU memory-hierarchy reliability problem: HBM2 ECC (SECDED), double-bit errors, and the driver's page-retirement machinery.
- **Compute/power.** The causal finding is a *power-dynamics* finding — DBEs track short-term power *swings*, which are a proxy for burst compute/memory intensity on the SMs.
- **Scheduling.** The actionable output is scheduling/operations policy: which GPUs are predisposed, and which project/user combinations induce failures.
- **Communication / synchronization.** NOT_IN_PAPER.

## 12.4 Why the problem exists (down to hardware root cause)

- **ECC scope.** V100 HBM2 uses **SECDED** — Single Error Correction, Double Error Detection. Single-bit errors are corrected on read; double-bit errors are *detected but not corrected* [paper]. So a DBE is by construction an uncorrectable event, and the only remaining defence is to stop using the affected memory.
- **The repair mechanism on Volta is page retirement, not row remapping.** The NVIDIA driver supports dynamic page retirement ("offlining") after a DBE, or after two SBEs at the same address. The **retirement table holds up to 64 memory pages**; exceeding it produces page-retirement failures (PRFs). Failed pages are mapped out only on the next GPU reattachment/reboot, i.e. repair requires a reinit. Temporary storage for offlined locations is 192–600 entries depending on GPU model [paper].
  - This is the key architectural difference from `GPU-SC25-01`: Volta retires *pages* with a 64-entry budget; Ampere/Hopper remap *rows* with a 512-row budget. The two papers are measuring the same failure class through two different generations of repair hardware.
- **Physical mechanism hypothesis.** The authors propose "charge leakage to a neighboring memory cell, especially under extreme temperatures or intensive memory access," in a 3D-stacked HBM2 device whose density is noted as relevant [paper]. They explicitly decline to claim causality (see 12.13).

## 12.5 Mathematical / performance model

Three statistical instruments, not a performance model [paper]:

1. **Independence thresholding for streaks.** Successive DBEs on the same unit within 5 days are treated as a single dependent episode; beyond that they are counted as independent.
2. **Multiple-comparison-corrected hypothesis testing.** The 15-minute power range prior to a DBE is the most significant covariate, **p = 0.00056 after Šidák correction** [paper]. Reporting a corrected p-value across many candidate covariates is what makes the "power not temperature" claim credible rather than a data-dredging artifact.
3. **Cox proportional-hazards regression** over user/project combinations, identifying DBE-susceptible applications.

Predictive framing: lifetime aggregate features on already-susceptible units reach **ROC AUC 0.84**, versus **0.53** — essentially chance — on the general GPU population [paper]. The honest reading is that DBEs are predictable *only conditional on a GPU having already declared itself*, which is a statement about predisposition rather than about prediction.

## 12.6 Data layout and ownership

Summit configuration [paper]:
- **4,626 IBM AC922 nodes** in 257 cabinets, 18 nodes per cabinet, 8×37 grid floor layout.
- **6 NVIDIA Tesla V100 per node**, 16 GB **HBM2** each, 2 IBM POWER9 CPUs per node.
- Total GPUs: the paper's §2.1 says **27,756** while its abstract says **27,648** [paper]. Both figures appear in the document; the discrepancy is in the paper, not introduced here. 4,626 × 6 = 27,756, so 27,756 is the arithmetically consistent one and 27,648 (= 4,608 × 6) presumably reflects a compute-node count excluding some nodes `[inference]`. **The prior operations-corpus row cites 27,648 without noting the discrepancy.**
- Interconnect: not detailed in this paper (NOT_IN_PAPER — despite Summit's NVLink 2.0 / NVSwitch-less topology being well known, the paper does not use it).
- **Observation window: 1 January 2020 – 17 May 2022 (~2.5 years)** [paper]. Total GPU-hours: NOT_IN_PAPER — the paper does not state an aggregate GPU-hour figure. (Contrast `GPU-SC25-01`, which does.)

Failure-locality mapping onto the hierarchy [paper]:

| Level | What is observed |
|---|---|
| HBM2 bank / row / stack | **Not resolvable** — "errors localized only to GPU/node, not bank/row/stack" (stated limitation) |
| memory page | the retirement unit; 64-page table cap; PRF on exhaustion |
| GPU | the unit of predisposition — 112 of ~28,000 GPUs carried all 295 DBEs |
| GPU slot within node | slots **2 and 3**, the geometrically central placements, show statistically *lower* DBE susceptibility in streaks |
| node / cabinet | cabinet and node-height location show **no** significant correlation with error rates |
| job / project | 5 user–project combinations are DBE-susceptible; 10 project–user combinations cause 97% of PRFs |

Data sources [paper]:
- Per-GPU power and thermal telemetry at **1 Hz** — 268 billion rows compressed to 16 TB.
- Per-node job-scheduler allocation history (recorded at the end of every job).
- Node reboot logs, used to map GPU PCIe bus IDs to serial numbers — this is what makes per-physical-GPU tracking possible across reboots.
- NVIDIA GPU XID error log, ~3 million rows. XIDs used: **48** (DBE), **63** (page retirement event, PRE), **64** (page retirement failure, PRF) [paper].

## 12.7 Pseudo code

The analysis pipeline `[reconstruction]` from the paper's described method:

```
# 1. identity resolution across reboots
gpu_serial(node, pcie_bus, t) <- lookup from reboot logs   # GPUs move slots over 2.5y

# 2. episode / streak segmentation
for each gpu, for successive DBEs at times t_i, t_{i+1}:
    if t_{i+1} - t_i <= 5 days:  same (dependent) streak
    else:                        independent event

# 3. snapshot construction
for each independent DBE at time t on gpu g:
    window <- telemetry[g, t-15min : t]         # 1 Hz power + memory temperature
    features <- (power_range, power_mean, memtemp_range, memtemp_mean,
                 lifetime_activity_aggregates, job_context)
    label <- DBE
# negative snapshots drawn from non-DBE (gpu, t) pairs

# 4. test each covariate; correct for multiple comparisons (Sidak)
# 5. Cox proportional hazards over (user, project) strata
```

## 12.8 Real implementation

No analysis-software artifact is claimed. `NOT_INSPECTED` — no repository identified. What *is* released is the **dataset**, DOI `10.13139/OLCF/1970187` [paper].

## 12.9 Kernel execution

NOT_IN_PAPER at kernel/warp granularity — and this is a substantive limitation the authors themselves raise. They note the "lack of granular memory-operation intensity data," observing that "a job using more GPU memory will have a higher likelihood of catching a DBE due to invoking a larger number of ECC checks" [paper]. That is, the exposure denominator is unknown: they cannot distinguish "this job stresses memory" from "this job merely touches more of it."

The one execution-level finding that does survive is the mixed-precision one: **"Out of 5 identified HPC applications on Summit with statistically significant DBE susceptibility, at least 4 use mixed-precision arithmetic"** (Finding 11) [paper]. This is the paper's closest approach to an architectural cause — plausibly Tensor-Core-driven burst HBM traffic and burst power, consistent with the power-swing finding `[inference]`. The paper does not make the Tensor Core connection itself.

## 12.10 Memory traffic

Findings, with qualifiers (Summit, 27,756 V100s, HBM2, Jan 2020 – May 2022) [paper]:

**DBE occurrence**
- 295 DBEs total, on 112 GPUs of ~28,000.
- System-wide mean time between DBE events: **70.7 hours**.
- Top offending GPU alone: **10.5% of all DBEs**.
- Temporal clustering (Finding 2): "DBEs often occur on the same GPU within days, hours, or even minutes from one another, resulting in DBE streaks that can last for weeks." **Median inter-DBE time on the same unit is 20 hours, against a mean of ~20 days** — the median/mean gap is the streak signature.
- Finding 3: nearly half of independent DBEs occur with **no GPU utilization in the current job**. Corruption surfaces on read, not necessarily under load.
- Finding 10: prior DBEs predispose a GPU to recurrence, and predisposition is *more informative than short-term telemetry*.
- Finding 8: susceptibility increases with lifetime activity frequency/intensity; manufacturing variability is hypothesised as a contributor.

**Power versus temperature (the headline)**
- 15-minute power *range* before a DBE is the most significant variable, p = 0.00056 (Šidák-corrected), with DBEs associated with **≈33 W higher power fluctuation** [paper].
- Memory temperature range differs by only **≈1.5 °C**; high lifetime temperatures are **not** a significant DBE factor.
- Finding 6: "DBEs are associated with recent intensive GPU utilization characterized by substantial changes in power intake over short periods of time. The association with elevated temperatures is minor and likely a consequence of the above."
- **This is a direct contradiction of the received wisdom from the Titan-era literature, where cooling geometry and thermals were the governing variable.** It is *swing*, not level, and power, not temperature.

**Page-retirement failures — absent from the prior corpus record entirely**
- Finding 1: **97% of 35,554 PRFs trace to 10 project–user combinations within 113 jobs** [paper]. PRFs are overwhelmingly application-induced, not hardware-driven.
- A **Red Hat Enterprise Linux 8 OS update on 18 August 2021 correlates with a 170-fold increase in PRF counts from 1 September 2021** [paper]. A software change moved a hardware-reliability counter by two orders of magnitude — a strong caution against reading XID counter series across software boundaries, and a direct methodological warning for `GPU-SC25-01`'s "zero NVLink errors on H100" (which its own authors also refuse to attribute, on the same grounds).

**Spatial structure**
- GPU slots 2 and 3 (central placements) show statistically lower DBE susceptibility in streaks; cabinet and node-height show no significant correlation [paper]. So there *is* an intra-node geometric effect but not a machine-room-scale one.

## 12.11 Why it is faster/slower (decomposed cause)

Not a performance paper. The decomposed causal account of memory corruption is:
1. **Per-device predisposition** (manufacturing variability + accumulated lifetime activity) determines *which* GPUs can fail at all — 112 of 28,000, one accounting for 10.5% [paper].
2. **Short-term power transients** (≈33 W swings over 15 min) determine *when* a predisposed device fails — not steady-state temperature [paper].
3. **Workload arithmetic mix** correlates with susceptibility at the application level (4 of 5 susceptible applications use mixed precision) [paper].
4. **Driver/OS software** determines the *observed* failure rate of the repair path independent of hardware (the 170× PRF jump after RHEL8) [paper].

Effects (1) and (2) are properties of the device; (3) is a property of the workload; (4) is an artifact of the measurement stack. Conflating them is exactly the error the paper is written to prevent.

## 12.12 Hardware generation dependence

- Hardware: NVIDIA **Tesla V100** (Volta), 16 GB **HBM2**, 6 per IBM AC922 node [paper].
- The paper states it is "the first study addressing DBEs in HBM2 units at scale," contrasting with prior work on **Kepler GPUs with GDDR memory** [paper]. So the generational series in the literature is GDDR (Kepler/Titan) → HBM2 (Volta/Summit, this paper) → HBM2e/HBM3 (Ampere/Hopper, `GPU-SC25-01`).
- Repair-mechanism dependence is sharp and is the main reason results do not transfer mechanically: Volta's 64-entry **page-retirement** table versus Ampere/Hopper's 512-row **remapping** budget. A PRF on Volta and an XID 64 row-remap failure on Ampere are analogous but not identical events.
- The authors argue for portability of the *physical* findings: they are "likely to manifest in other HBM2 GPUs" given their low-level physical nature [paper]. That is a claim about HBM2, not about Ampere or Hopper.

## 12.13 Limitations

Stated by the authors [paper]:
1. "Rarity of DBEs together with the unavailability of temporal SBE data for Summit has been a significant impediment" — no SBE time series, so the SBE→DBE precursor question cannot be asked.
2. Missing telemetry: **30% of expected observations absent**; 2–21% missing values within power/thermal measurements.
3. No memory-operation-intensity data, so DBE likelihood cannot be normalised by actual ECC-check volume (see 12.9).
4. **No intra-HBM spatial locality** — errors resolve to GPU/node only, not bank/row/stack. The 3D-stack physical hypothesis therefore cannot be tested against location.
5. No causality: "Establishing causality in GPU memory corruption would require more data or a controlled testing environment."

Observed by this analysis:
6. Internal inconsistency in the GPU count (27,756 in §2.1 vs 27,648 in the abstract) [paper].
7. The 0.84 ROC AUC applies only to already-susceptible units; on the general population the model is at chance (0.53). The predictive claim is much narrower than it first reads.
8. No software artifact for the analysis pipeline, so the survival/Cox analysis is not directly reproducible even though the data are public.

## 12.14 Relation to prior corpus

- **Prior corpus:** `GPU_DELTA_ANALYSIS`. Pre-existing record is a census row plus lineage mentions (see delta notice). Not rewritten here; corrected on author order and on the GPU-count discrepancy.
- **Successor / same measurement, later generation:** `GPU-SC25-01` (*Story of Two GPUs*, SC 2025). Same XID vocabulary (48/63/64), same failure class, two generations later. The pair forms the most useful cross-generation comparison available in this cluster, and they **disagree in emphasis**: Summit locates the binding constraint in per-device predisposition plus power transients on a 64-page retirement budget; the Delta paper locates it in a 512-row remap budget that failed to scale with a 2.4× HBM capacity increase. Neither refutes the other — Summit had capacity headroom in its repair table relative to its fault rate; Delta's H100 did not.
- **Lineage (per the operations corpus, `[inference]` not `[paper]`):** ORNL Titan operational records → SC20 *GPU Lifetimes on Titan* → Summit XID/DBE dataset release → this paper. The operations corpus marks this chain `VERIFIED` on its own evidence.
- **Contradicts prior received wisdom:** the Titan-era conclusion that GPU lifetime is governed by cooling geometry and job placement. This paper finds temperature *level* insignificant (≈1.5 °C effect) and power *swing* dominant (≈33 W, p = 0.00056) [paper].
- **Complementary (verdict-only in this cluster):** *DRUTO: Upper-Bounding Silent Data Corruption Vulnerability in GPU Applications* (IPDPS 2024) and *Demystifying the Resilience of Large Language Model Inference* (SC 2025) address the software-visible consequences of exactly these uncorrected errors. See `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The study's mechanism is the NVIDIA GPU memory-repair path specifically — XID 48/63/64, the driver's dynamic page-retirement table with its 64-page cap, and SECDED over 3D-stacked HBM2 — and its central covariate is per-GPU power telemetry at 1 Hz from a 6-GPU-per-node accelerator node. A CPU DRAM field study would measure MCE correctable/uncorrectable counters and OS page offlining, and would neither have a per-device page-retirement budget to exhaust nor a 33 W burst-power signal from SM/Tensor-Core activity. The mixed-precision-application susceptibility finding is likewise meaningful only on a device with mixed-precision arithmetic units driving burst HBM traffic.

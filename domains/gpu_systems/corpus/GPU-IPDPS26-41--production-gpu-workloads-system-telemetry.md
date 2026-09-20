# GPU-IPDPS26-41 — Characterizing Production GPU Workloads using System-wide Telemetry Data

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `O — reliability, telemetry & production GPU performance`
secondary_topics: `N (performance characterisation); GPU memory hierarchy (HBM capacity & bandwidth counters); Tensor Core utilisation; job scheduling`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — official author PDF (cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026c.pdf) read for authors/affiliations, system configuration, telemetry stack and sampling, the complete DCGM counter list with the authors' own definitions, utilisation-by-job-size results, FP-pipeline intersection analysis, HBM capacity-request findings, roofline compute/memory-bound split, spatial and temporal imbalance metrics, counter correlations, and the stated limitations. NOT read line-by-line: individual figure captions and the related-work section.`

---

## PRIOR-ANALYSIS DELTA NOTICE (mandatory, per task §4)

An existing document in this repository analyses this paper **from an HPC-operations/AIOps benchmarking angle**. This file is a **GPU-specific delta**.

What already exists, in `domains/hpc_systems_operations/corpus/aiops-survey/`:
- `synthesis/02_PAPER_CENSUS.md` entry **M-24** — authors (Cankur, Austin, Kulkarni, Bhatele; UMD + NERSC), venue and DOI `10.1109/ipdps65963.2026.00078` pp. 899–912, the operational question ("center-wide, what do GPU jobs actually do as seen only from always-on telemetry"), method ("large-scale empirical characterization"), a maturity grading (L2 · D2 · P2–P3), the judgement that the contribution is descriptive with *no predictive or diagnostic model*, and its strategic role as the closest published analogue to a national-centre GPU telemetry census.
- `raw/B_hpdc_ipdps_cluster_isc_acsos.md` — the same, plus the collaboration-structure observation.
- `synthesis/03_SC_REGULAR_PRECEDENTS.md` — cites the UMD+NERSC co-authorship as a template.

**Two UNKNOWNs in the pre-existing record are resolved by this reading.** M-24 records the data source as *"system-wide GPU telemetry — NERSC Perlmutter급으로 추정 `[system identity A — confirm]`"* (Perlmutter-class, **inferred**, flagged for confirmation) and the evaluation scale/duration as `[UNVERIFIED]`. The paper states both explicitly: the system **is Perlmutter**, and the window is **1 March – 1 April 2025, 75,703 jobs, 10-second sampling** [paper]. Both flags can be closed.

**What this file adds:** the counter-level substrate — the exact DCGM fields and the authors' own definitions of each, which determine what the study can and cannot see; the FP64/FP32/FP16/Tensor pipe-activity intersection analysis; the HBM-capacity-request mismatch; the roofline-based compute/memory-bound split and its energy consequence; and the spatial (intra-node, across 4 GPUs) and temporal imbalance metrics, including the finding that 12% of 4-GPU jobs never touched three of their GPUs. None of this is in the prior record.

---

## 12.1 Bibliographic facts

- Official title: *Characterizing Production GPU Workloads using System-wide Telemetry Data* [paper]. `CONFIRMED_IN_POPULATION` verbatim (`census/IPDPS_2026.md` §5).
- Authors: Onur Cankur (University of Maryland, College Park), Brian Austin (NERSC, Lawrence Berkeley National Laboratory), Dhruva Kulkarni (NERSC, LBNL), Abhinav Bhatele (University of Maryland, College Park) [paper].
- Venue: IPDPS 2026. DOI `10.1109/ipdps65963.2026.00078`, pp. 899–912 [per the `hpc_systems_operations` corpus, which recorded it from Crossref; the census records the DOI as UNKNOWN].
- Publication type: `ARCHIVAL_MAIN_PAPER`. Preprint: arXiv `2502.18680`.
- Public full text: official author PDF `https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026c.pdf` [official-web].
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). The monitoring data itself **cannot be released** — see 12.13.

## 12.2 Core question (one sentence)

Using only the always-on, administrator-configured telemetry a centre already collects — no code-level profiling, no user cooperation — what can be established about how a leadership GPU machine's entire job population actually uses its GPUs? [paper]

## 12.3 GPU/HPC problem translation

- **Compute.** The core axis: which arithmetic pipelines production jobs actually exercise (FP64 vs FP32 vs FP16 vs Tensor), and how busy the SMs are.
- **Memory.** Two distinct memory findings — HBM *bandwidth* activity (used to classify jobs compute- vs memory-bound) and HBM *capacity* (jobs requesting 80 GB parts they do not need).
- **Scheduling.** The strongest operational finding is an allocation-policy one: exclusive node allocation means 4 GPUs are charged whether or not they are used, and 12% of 4-GPU jobs used only one.
- **Communication.** Present but secondary: NVLink and PCIe rate counters are collected; no topology or congestion analysis (contrast `GPU-IPDPS26-42`).
- **Synchronization.** NOT_IN_PAPER — the 10-second sampling floor makes it unobservable.

## 12.4 Why the problem exists (down to hardware root cause)

The problem is a *measurement-access* problem rooted in what GPU hardware exposes to an always-on collector, and the paper is unusually explicit about its own instrument's limits:

- DCGM exposes **aggregate, time-averaged activity fractions per pipeline**, not instruction counts or stall reasons. `SM_ACTV` is the "fraction of time at least one warp was active, averaged over all multiprocessors" [paper] — so a kernel with one resident warp per SM and a kernel saturating occupancy are indistinguishable in this counter. This is why the study can say *whether* the tensor pipe was busy but not *how efficiently*.
- The **10-second sampling interval** "is set by system administrators and cannot be changed by users, so brief spikes may be missed" [paper]. Any per-kernel or per-iteration structure is aliased away.
- The distinction between `GPU_UTIL` ("fraction of time during which at least one kernel was executing") and `SM_ACTV` is itself the hardware root cause of the most common misreading of GPU utilisation: a GPU can report high `GPU_UTIL` while almost no SM work is happening, because *a* kernel is resident [paper].
- **Exclusive node allocation** on a 4-GPU-per-node machine means the schedulable unit is the node, not the GPU — so a single-GPU job idles three A100s by construction [paper]. That is a policy/hardware-packaging interaction, not user error.

## 12.5 Mathematical / performance model

The paper is descriptive, not model-building (the prior corpus record correctly notes "no predictive or diagnostic model"). Its quantitative instruments are:

1. **A roofline-style classification** dividing jobs into compute-bound and memory-bound using the relation between compute-pipe activity and DRAM activity [paper]. Result: **81% memory-bound, 19% compute-bound** (Perlmutter, 75,703 jobs, March 2025).
2. **Spatial imbalance** — a per-job scalar over the GPUs in the allocation, capturing how unevenly work is spread across the 4 GPUs of a node and across nodes. Reported on a 0–1 scale (peak 0.78 for low-utilisation jobs) [paper]. The exact formula is NOT_IN_PAPER as read; treat the metric definition as UNKNOWN beyond its range and interpretation.
3. **Temporal imbalance** — the same style of scalar over a job's time series, capturing burstiness [paper].
4. **Pearson-style counter correlation** against `GPU_UTIL` [paper].

## 12.6 Data layout and ownership

System: **Perlmutter (NERSC)** [paper]:
- **1,792 GPU nodes** (plus 3,072 CPU-only nodes).
- **4 NVIDIA A100 per node**; **1,536 nodes with 40 GB HBM per GPU**, **256 nodes with 80 GB HBM per GPU**.
- Host CPU: **AMD EPYC 7763**; 256 GB DDR4 per node.
- Intra-node: **third-generation NVLink, 4 links between each pair of GPUs, 25 GB/s per direction per link**; **PCIe 4.0** to CPUs and NICs.

Telemetry stack [paper]:
- **LDMS** (Lightweight Distributed Metric Service) as the system-wide collector.
- **NVIDIA DCGM** plugin for GPU counters.
- Retrieval via the **Prometheus API** (for LDMS) and **Slurm `sacct`** (for job records).
- **Sampling interval: 10 seconds.**
- **Window: 1 March – 1 April 2025** (one month).
- **75,703 jobs** after cleaning and preprocessing.

The counter set, with the authors' own definitions [paper] — this is the substrate the prior record omits:

| Counter | Authors' definition |
|---|---|
| `GPU_UTIL` | "Fraction of time during which at least one kernel was executing" |
| `SM_ACTV` | "Fraction of time at least one warp was active, averaged over all multiprocessors" |
| `FP16_ACTV` | "Fraction of cycles the FP16 (half-precision) pipe was active" |
| `FP32_ACTV` | "Fraction of cycles the FP32 (single-precision and integer) pipe was active" |
| `FP64_ACTV` | "Fraction of cycles the FP64 (double-precision) pipe was active" |
| `TNSR_ACTV` | "Fraction of cycles the tensor pipe was active" |
| `DRAM_ACTV` | "Fraction of cycles where data was sent to or received from device memory" |
| `HBM_USED` | "Absolute amount high-bandwidth memory (HBM) capacity used (MB)" |
| `NVLINK_TX` / `NVLINK_RX` | "Rate of data transmitted/received over NVLink, not including protocol headers, in bytes per second" |
| `PCIE_TX` / `PCIE_RX` | "Rate of data transmitted/received over PCIe, including both protocol headers and data payloads" |
| `TOTAL_ENG` | "Total energy consumption for the GPU in mJ since the driver was last reloaded" |
| `GPU_TEMP` | "Current temperature readings for the device, in degrees Celsius" |

Note the NVLink/PCIe asymmetry the authors flag: NVLink rates **exclude** protocol headers, PCIe rates **include** them. These two counters are therefore not directly comparable, which matters for any attempt to reason about the CPU↔GPU versus GPU↔GPU data path from this data.

Ownership hierarchy as the data resolves it:
- **warp** — only via `SM_ACTV`'s "at least one warp active"; individual warps invisible.
- **SM** — only as an average over all SMs.
- **GPU** — the finest real unit of observation.
- **node** — 4 GPUs; the allocation unit.
- **job** — `sacct` joins telemetry to jobs; 75,703 of them.
- **cluster** — 1,792 GPU nodes = 7,168 A100s.

## 12.7 Pseudo code

`[reconstruction]` of the described pipeline:

```
# 1. join telemetry to jobs
jobs  <- sacct(window = 2025-03-01 .. 2025-04-01)         # nodes, GPUs, times, size
series<- prometheus_query(LDMS/DCGM counters, step = 10s)  # per-GPU time series
for j in jobs:
    j.gpus <- allocated GPUs
    j.ts   <- series[j.gpus, j.start : j.end]
clean/preprocess -> 75,703 jobs

# 2. per-job aggregation
for j in jobs:
    for c in counters: j.mean[c], j.peak[c] <- aggregate(j.ts[c])
    j.compute_bound <- roofline_classify(j.mean[FP*_ACTV, TNSR_ACTV], j.mean[DRAM_ACTV])
    j.spatial_imbalance  <- imbalance across j.gpus of mean GPU_UTIL
    j.temporal_imbalance <- imbalance across time of aggregate GPU_UTIL

# 3. population analysis
group by job size (GPUs): 1, 2-32, 33-512, >=512
intersect job sets by which FP pipes were ever active   # UpSet-style
correlate every counter against GPU_UTIL
```

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact repository identified (`census/IPDPS_2026.md` records `NOT_FOUND_AFTER_SEARCH`). The tooling is the standard LDMS + DCGM + Prometheus + Slurm stack rather than new software, and the data cannot be released (12.13).

## 12.9 Kernel execution

Deliberately out of scope, and the authors say so: the investigation "intentionally focuses on what can be inferred from production monitoring without code-level profiling, so function call paths and thread-level behavior are not captured" [paper].

What survives at execution granularity is the **pipeline-occupancy** picture, which is genuinely architectural [paper] (Perlmutter, 75,703 jobs, March 2025):
- **FP64-only jobs: 33,675 jobs = 44% of all jobs, mean `GPU_UTIL` 36%.** The largest single behavioural class on an A100 machine runs double-precision only — i.e. uses neither the Tensor Cores nor reduced precision.
- **Tensor+FP64: 13,721 jobs = 18%, mean `GPU_UTIL` 50%.** Tensor-using jobs show markedly higher utilisation.
- **FP16: 178 jobs across the entire dataset.** Half precision is essentially absent from this population.

The FP64-dominance finding is the most consequential architectural result in the paper: on a machine whose A100s were procured partly for their Tensor Core throughput, 44% of jobs touch only the FP64 pipe, and the tensor pipe's users are a minority with measurably better utilisation.

## 12.10 Memory traffic

All numbers: Perlmutter, 4×A100 per node, 75,703 jobs, 1 March – 1 April 2025, 10 s sampling [paper].

**Bandwidth / boundedness**
- **81% of jobs are memory-bound; 19% compute-bound** by the roofline criterion.
- Energy consequence: "Memory-bound jobs tend to consume more energy than compute-bound jobs at comparable GPU-hours." HBM traffic, not arithmetic, is where the machine's energy goes for most of its workload.

**Capacity**
- Among jobs *explicitly requesting* the 80 GB A100 nodes, **55% peak at or below 50% of HBM capacity and "should fit on a 40 GB GPU."** Only **17%** use 90–100% of capacity.
- This is a procurement/scheduling misallocation of a scarce resource: 256 of 1,792 nodes carry 80 GB parts, and most jobs asking for them do not need them.

**Utilisation by job size**
- Peak at intermediate scale: **33–512 GPUs, ~47–48% mean `GPU_UTIL`**.
- Falls sharply at the largest scale: **≥512 GPUs, ~20% median**.
- Small single-node jobs: **38% median**, below the 45% of moderate sizes.
- The shape is an inverted U: both very small and very large jobs use the GPUs poorly, for different reasons (allocation granularity at the small end, scaling loss at the large end `[inference]`).

**Imbalance — the intra-node GPU story**
- Low-utilisation jobs show high **spatial** imbalance (peak 0.78); high-utilisation jobs cluster tightly at low imbalance (**97.1% below 0.30**).
- **"12% of all 4-GPU jobs never used three of their GPUs"** — attributed by the authors to exclusive node allocation. Three quarters of the accelerator capacity on those nodes is charged and idle.
- **Temporal** imbalance separates the same populations: **88.9% of high-utilisation jobs below 0.30**, versus **66.3% of low-utilisation jobs above 0.70**. Low-utilisation jobs are not uniformly slow — they are bursty.

**Counter correlations against `GPU_UTIL`**
- GPU power **0.78**, GPU temperature **0.77**, SM activity **0.76** [paper].
- Power correlates with utilisation slightly *better* than SM activity does — i.e. on this machine, power telemetry is as good a utilisation proxy as the SM counter. In compute-bound jobs utilisation aligns primarily with compute activity; in memory-bound jobs both compute and memory activity matter.

## 12.11 Why it is faster/slower (decomposed cause)

The paper does not optimise anything, but its results decompose *low observed GPU utilisation* on a production machine into four separable causes, which is its real analytical contribution:

1. **Allocation granularity** — exclusive 4-GPU node allocation strands GPUs that no job ever touches (12% of 4-GPU jobs used one GPU).
2. **Scaling loss** — utilisation collapses from ~47% at 33–512 GPUs to ~20% median at ≥512 GPUs.
3. **Burstiness, not slowness** — temporal imbalance above 0.70 in 66.3% of low-utilisation jobs: the GPU is idle between phases rather than uniformly underused.
4. **Pipeline mismatch** — 44% of jobs use the FP64 pipe only, leaving the tensor pipe dark; tensor-using jobs show 50% mean utilisation against 36% for FP64-only.

Causes 1 and 2 are scheduling/system properties; 3 and 4 are application properties. An operator can act on 1 immediately (finer-grained allocation or MIG partitioning `[inference]` — the paper does not discuss MIG) and on 2 and 3 only through user engagement.

## 12.12 Hardware generation dependence

- Hardware: **NVIDIA A100** (Ampere), 40 GB and 80 GB HBM variants, 4 per node, NVLink 3.0, PCIe 4.0, AMD EPYC 7763 host [paper].
- Generation-dependent in two respects that limit transfer:
  - The **FP64/FP32/FP16/Tensor pipe split** is an Ampere-specific counter decomposition. On Hopper and later the tensor pipe subsumes more precisions (FP8, and transformer-engine paths), so `TNSR_ACTV` would mean something different `[inference]`.
  - The **40 GB vs 80 GB capacity finding** is specific to Perlmutter's split procurement; the *method* transfers, the number does not.
- Generation-*independent*: the `GPU_UTIL` vs `SM_ACTV` semantic trap, the 10-second sampling floor, and the exclusive-allocation stranding are properties of the DCGM/LDMS/Slurm stack rather than of Ampere, and will recur on any DCGM-monitored machine.
- The paper is **single-vendor**: DCGM is NVIDIA-only, so there is no AMD/Intel arm. Contrast `GPU-IPDPS26-42`, which covers both Perlmutter and Frontier.

## 12.13 Limitations

Stated by the authors [paper]:
1. **Sampling resolution** — 10 s, administrator-set, user-unchangeable; "brief spikes may be missed."
2. **Scope** — no code-level profiling, so "function call paths and thread-level behavior are not captured."
3. **Portability** — "comparable job-level telemetry is hard to obtain across sites due to access permissions and monitoring differences."
4. **Data cannot be shared publicly** (collected at a US DOE facility) — so the study is not independently reproducible.
5. **Temporal window** — "one month of Perlmutter DCGM data sampled every 10 seconds," which may not capture seasonal variation.
The authors name higher-frequency traces, cross-site validation, and complementary code-level profiling as future work.

Observed by this analysis:
6. **Descriptive only** — no predictive or diagnostic model, as the prior operations-corpus record already judged. Correlations are reported; no causal claim is made.
7. The spatial/temporal imbalance metric definitions are not recoverable from the reading performed; the metrics are interpretable but not reproducible from this document. UNKNOWN.
8. `SM_ACTV`'s "at least one warp active, averaged over all SMs" definition means no occupancy conclusion can be drawn from this data, which bounds how far the "81% memory-bound" classification can be pushed.

## 12.14 Relation to prior corpus

- **Prior corpus:** `GPU_DELTA_ANALYSIS`; see the delta notice. Two `[UNVERIFIED]`/`[confirm]` flags in `synthesis/02_PAPER_CENSUS.md` M-24 are now closed (system = Perlmutter; window = one month, March 2025; 75,703 jobs).
- **Companion paper, same group, same venue:** `GPU-IPDPS26-42` (*The Case of the Elusive Application Performance on Production GPU Supercomputers*, Wei/Pradeep/Bhatele, IPDPS 2026 `.00079`, pp. 913–927). The two are complementary by construction and should be read as a pair: this paper is **observational over the whole job population with no control**, its companion is **controlled repeated runs of four applications with no population coverage**. This paper finds most jobs memory-bound and poorly utilised; the companion finds that run-to-run *variability* is not attributable to the GPUs at all. Together they say: the GPUs are underused, but that underuse is not what makes performance unpredictable.
- **Complementary (verdict-only in this cluster):** *Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining* (IPDPS 2024) is the closest methodological neighbour — same data class, but optimising operator-actionable rules rather than characterisation. *SMART-MIG* (IPDPS 2026) is the scheduling response to the stranding finding. See `_LEDGER_profiling_reliability.md`.
- **Architecture bridge:** this paper's finding that 44% of jobs are FP64-only and that the tensor pipe is idle for most of the population is the production-side counterpart to the architecture-level question of whether Tensor Cores are the right area investment — see the cross-paper findings in `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The study's entire observational instrument is the NVIDIA DCGM counter set, and its findings are statements about GPU-specific microarchitectural structures: per-precision pipe activity (`FP16/FP32/FP64/TNSR_ACTV`) that exists because the SM has separate arithmetic pipelines including Tensor Cores, `SM_ACTV` defined over *warps* active per multiprocessor, HBM capacity and DRAM-activity counters, and NVLink-versus-PCIe rate counters. The headline results — 44% of jobs FP64-only with the tensor pipe dark, 55% of 80 GB-requesting jobs fitting in 40 GB of HBM, and 12% of 4-GPU jobs stranding three GPUs under exclusive node allocation — are each meaningless without a multi-GPU-per-node accelerator with per-precision pipes and on-package memory. This is not an anomaly-detection method applied to a machine that happens to have GPUs; the counters and the conclusions are GPU-architectural throughout.

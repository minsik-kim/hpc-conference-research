# GPU-IPDPS26-42 — The Case of the Elusive Application Performance on Production GPU Supercomputers

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `O — reliability, telemetry & production GPU performance`
secondary_topics: `N (performance attribution / profiling); multi-GPU collective communication; NIC & interconnect counters; GPU-to-GPU data path`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — official author PDF (cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf) read for authors/affiliations, both system configurations, the full application/run table, node-hours and window, the Cassini NIC counter table with descriptions, the profiling tooling (mpiP, PyTorch Profiler, HTA), the micro-benchmark harness, the Spearman and XGBoost attribution method with MAPE/Direction-Accuracy metrics, per-system variability results, the GPU-vs-network attribution argument, feature importances, and the stated limitations including the inaccessible-counter admission. NOT read line-by-line: individual figure captions and the related-work section.`

---

## PRIOR-ANALYSIS DELTA NOTICE (mandatory, per task §4)

An existing document in this repository analyses this paper **from an HPC-operations/performance-variability angle, in some depth**. This file is a **GPU-specific delta** and does not restate it.

What already exists, in `domains/hpc_systems_operations/corpus/aiops-survey/`:
- `synthesis/02_PAPER_CENSUS.md` entry **M-25** — authors (Wei, Pradeep, Bhatele; UMD), venue/DOI `10.1109/ipdps65963.2026.00079` pp. 913–927, the operational problem (run-to-run variability on GPU flagships), the data sources at a high level ("network counters + app profiles + scheduler logs + GPU"), the scale (**Perlmutter 1,792 GPU nodes + Frontier 9,408 nodes, 4 months 2024–25, 761 runs / 8,118 node-hours, 4 apps, ~10 TB/system**), the method ("repeated controlled runs + network HW counters + XGBoost attribution"), the headline results (**Frontier 2.6× / Perlmutter 1.4× variability**, cause attributed to network congestion and "top users" rather than compute), the limits (controlled benchmark runs not real production jobs; **authors' own admission that Rosetta switch counters were inaccessible**; correlation not causation; no operational action), and a strategic reading that *"the framing that GPU degradation is the main cause has already been measured and falsified."*
- `raw/B_hpdc_ipdps_cluster_isc_acsos.md`, `raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md` — the same facts, and the IPDPS'20 Dragonfly → IPDPS'26 lineage.
- `synthesis/03_SC_REGULAR_PRECEDENTS.md` — treats the IPDPS'20/IPDPS'26 pair as a single venue-strategy lineage.

**What this file adds:** everything on the GPU side of the measurement, which the prior record compresses into the single word "GPU". Specifically: the *GEMM micro-benchmark harness* that is the paper's actual GPU instrument and the per-GPU / intra-node / system-wide variability numbers it produces; the correlation test that *falsifies* the slow-GPU hypothesis, with its coefficients; the GPU-collective decomposition (NCCL vs RCCL Allreduce) that locates the variability in the GPU-to-GPU data path rather than in the GPUs; the A100-vs-MI250X GCD asymmetry between the two machines; and the fact that the two systems' variability has different dominant NIC features. The prior record's "cause is network, not compute" summary is correct but does not record *how* the GPU side was excluded, which is the reusable methodological contribution.

---

## 12.1 Bibliographic facts

- Official title: *The Case of the Elusive Application Performance on Production GPU Supercomputers* [paper]. `CONFIRMED_IN_POPULATION` verbatim (`census/IPDPS_2026.md` §5).
- Authors: Cunyang Wei, Keshav Pradeep, Abhinav Bhatele — Department of Computer Science, University of Maryland, College Park, MD 20742 [paper].
- Venue: IPDPS 2026. DOI `10.1109/ipdps65963.2026.00079`, pp. 913–927 [per the `hpc_systems_operations` corpus, recorded from Crossref; the census records the DOI as UNKNOWN].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: official author PDF `https://www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf` [official-web].
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). The paper references an artifact item "A6" describing ~10 TB of raw data per system [paper].

## 12.2 Core question (one sentence)

On two production GPU flagships, how much does the same application's runtime vary from run to run, and can that variability be attributed — with a predictive model, not just correlation — to the GPUs, to job placement, or to the interconnect? [paper]

## 12.3 GPU/HPC problem translation

- **Communication.** This is fundamentally a communication paper, and the GPU relevance is concentrated here: the variability lands on **GPU-resident collectives** (NCCL/RCCL Allreduce) crossing the NIC/PCIe boundary out of the GPU.
- **Compute.** The GPU compute axis is tested and *excluded* — this is the paper's most valuable negative result.
- **Scheduling.** Job placement across dragonfly groups is tested and also largely excluded; concurrent "top users" occupancy is not.
- **Memory.** Not an axis. HBM behaviour is not instrumented.
- **Synchronization.** Present indirectly, via which MPI routines absorb the variance (`Allreduce`, `Test`, `Waitall`).

## 12.4 Why the problem exists (down to hardware root cause)

The paper establishes, by elimination, that the root cause is not in the GPU:

- **GPUs do vary, but not enough and not in the right place.** A per-GPU FP16 GEMM micro-benchmark shows every GPU has "some variability in performance (within a 2.5% window) compared to their best recorded execution time," and "individual GPU performance remains relatively stable" [paper]. Yet system-wide spread reaches 28% on Perlmutter, and even *within a single node* the four A100s differ by up to 10% (worst case 17%) [paper]. So there is real per-device heterogeneity — it simply does not propagate to application runtime.
- **The falsification test.** The authors correlate application runtime against the number of GPUs in a job's allocation that fall in the **system-wide slowest 1%**, obtaining Spearman coefficients of **0.07 (Perlmutter) and 0.08 (Frontier)**, and "observed the same weak correlation when extending this to the slowest 10% and 30% of GPUs" [paper]. Their conclusion: "performance variability likely stems from other factors, such as network congestion, rather than slower GPUs."
- **Where it actually lives.** "Performance variability arises primarily due to slowdowns in collective communication, in particular, Allreduce, Test, and Waitall routines. Some routines exhibit long-tail effects" [paper]. On a GPU machine these collectives are GPU-buffer-resident and traverse GPU→NIC over PCIe and then the Slingshot fabric — so the failure is in the GPU *data path*, not in the GPU.
- **The mechanism at the NIC.** The counters that correlate positively with runtime are `rh:sct_timeouts` and `rh:spt_timeouts` — "retry events and response timeouts triggered by packet loss." The authors' reading: "frequent retries and cancellations disrupt steady data flow" [paper].
- **A software root cause is also demonstrated.** A routine Frontier maintenance on **14 January 2025** upgraded Slingshot Host Software and fixed "a known performance regression in libfabric 1.20.1," producing "a significant reduction in AMG2023 variability" [paper]. Part of what looks like hardware variability was a host-software bug in the GPU-adjacent communication stack.

## 12.5 Mathematical / performance model

Two-stage, and the paper is explicit that stage one is insufficient [paper]:

1. **Spearman rank correlation** between application runtime and NIC counter mean/max values (heatmap, Fig. 11). The authors state plainly that "analyzing NIC counters in isolation may not fully capture the complexities of variability."
2. **XGBoost regression** on runtime, 90/10 train/test split. Features: job placement, GEMM performance, MPI/NCCL-RCCL Allreduce proxy measurements, and NIC counters (mean/min/max per node). Feature importance by impurity reduction.

Two evaluation metrics, the second unusual and worth reusing:
- **MAPE** (mean absolute percentage error): ~5–20% on Perlmutter, similar with slightly higher error on some Frontier applications [paper].
- **Direction Accuracy (DA)** — "checks whether the model correctly predicted trends — specifically, whether it recognizes when performance is improving or declining compared to a previous state," with a tolerance ε (e.g. ε = 0.02) [paper]. DA stays "close to 1.0 when NIC counters are included" and "sometimes falls to chance-level performance" without them.

The DA-with-versus-without-NIC-counters contrast is the paper's actual evidential core: it shows the NIC counters are not merely correlated but *necessary* to predict the direction of change. Note the epistemic limit — this establishes predictive sufficiency, not causation, as the prior operations-corpus record also observes.

## 12.6 Data layout and ownership

**Perlmutter (NERSC)** [paper]: 4,864 total nodes, 1,792 GPU-accelerated; **4 NVIDIA A100 per node (40 GB or 80 GB HBM2)**; 64-core AMD EPYC 7763 Milan host; **HPE Slingshot-11, 3-hop dragonfly**; 4 NICs per node at 25 GB/s each = 100 GB/s aggregate.

**Frontier (OLCF)** [paper]: 9,408 compute nodes; **4 AMD Instinct MI250X per node, each a 2-die package = 8 GCDs per node, 64 GB HBM2e per GCD**; 64-core AMD EPYC Trento host; **HPE Slingshot-11, 3-hop dragonfly**; 4 NICs at 25 GB/s each = 100 GB/s bidirectional.

**The two machines are not symmetric at the GPU level, and this matters.** A Perlmutter node presents 4 addressable A100s; a Frontier node presents 8 addressable GCDs from 4 physical MI250X packages. Any per-"GPU" comparison between them is comparing a whole A100 against half an MI250X. The paper handles this by using per-device GEMM normalised to each device's own best time [paper], which is the right control, but it means the 28%-versus-15% system-wide spread figures are not directly comparable across the two machines `[inference]`.

**Runs** — 64 nodes per job on both systems [paper]:

| Application | System | Input | Jobs |
|---|---|---|---|
| AMG2023 | Perlmutter | `-P 4 8 8 -n 128 64 64` | 104 |
| AMG2023 | Frontier | `-P 8 8 8 -n 128 64 64` | 168 |
| MILC | Perlmutter | nx 40 ny 160 nz 320 nt 320 | 78 |
| MILC | Frontier | nx 80 ny 160 nz 320 nt 320 | 38 |
| DeepCAM | Perlmutter | max epochs 8, local batch size 2 | 67 |
| DeepCAM | Frontier | max epochs 4, local batch size 2 | 109 |
| nanoGPT | Perlmutter | model size 20B, iters 30, batch size 8 | 94 |
| nanoGPT | Frontier | model size 20B, iters 30, batch size 8 | 103 |

Totals reconcile exactly: 343 Perlmutter + 418 Frontier = **761 jobs** [paper]. (An additional numeric field "512" appears alongside the Frontier nanoGPT row in the source table; it is most likely a sequence-length or per-run configuration column rather than a job count, since 103 is the value required for the 418 total `[inference]`.)

- **~8,118.7 node-hours** total; application execution ~7,610 minutes (~127 h); micro-benchmarks a further ~3,805 minutes (~63.4 h, 4,185.3 node-hours) [paper].
- **Window: four months in 2024–2025**, specifically **23 December 2024 – 12 April 2025** per the Fig. 1 timeline [paper].
- **~10 TB raw data per system** [paper].
- Run type: **production-*like* controlled benchmark runs, not production jobs.** Configurations match the NERSC-10 and OLCF-6 benchmark specifications, and the developers of AMG2023, nanoGPT and MILC confirmed the "setup aligns with configurations in production runs" [paper]. This is the paper's central methodological trade-off — it buys a controlled comparison at the cost of population validity (and is exactly the complement of `GPU-IPDPS26-41`, which buys population validity at the cost of control).

**NIC counters — Cray Cassini** [paper], with the paper's descriptions:

| Counter | Description |
|---|---|
| `rh:sct_timeouts` | response timeouts that trigger retries |
| `rh:spt_timeouts` | retry handler: packet loss events |
| `hni_rx_paused_0/1` | cycles where the receive path is paused |
| `hni_tx_paused_0/1` | cycles where the transmit path is paused |
| `lpe_net_match_request_0` | messages matched on request list |
| `lpe_net_match_priority_0` | messages matched on default priority list |
| `lpe_net_match_overflow_0` | messages matched in overflow buffer |
| `atu_cache_hit_base_page_size_0` | address-translation cache hits, base page size |
| `atu_cache_hit_derivative1_page_size_0` | ATU cache hits, derivative-1 page size |
| `parbs_tarb_pi_posted_pkts` | PCIe packets on the posted path |
| `parbs_tarb_pi_posted_blocked_cnt` | cycles the posted path is blocked |
| `parbs_tarb_pi_non_posted_blocked_cnt` | cycles the non-posted path is blocked |

Recording: NIC counters are read at **`MPI_Init`** and **`MPI_Finalize`** per process, so each job yields a start/end delta, not a time series [paper]. The `parbs_*` counters are PCIe-side, i.e. they observe the **GPU↔NIC hop** specifically — the one segment of the path that is on the GPU data path rather than in the fabric.

Profiling and analysis tooling [paper]:
- HPC applications (AMG2023, MILC): **mpiP**, with `MPI_Pcontrol` used "to capture MPI data exclusively from the main execution loop, thereby excluding initialization and I/O overheads."
- AI applications (DeepCAM, nanoGPT): **PyTorch Profiler**, capturing CPU and GPU operations, operation times, memory consumption, and compute–communication overlap.
- **HTA (Holistic Trace Analysis)**, with the authors' own modification: "we modified the HTA source code to enable" detailed **RCCL** breakdowns. HTA did not support AMD's collective library; they extended it.
- Scheduler/placement: Slurm `sacct`, giving node allocations, dragonfly-group mapping, and concurrent-job identification.

Micro-benchmark harness, run **before each application run** [paper]:
- **FP16 GEMM** — per-GPU peak-performance probe.
- **`MPI_Allreduce`** at 1 KB, 2 KB, …, 1 MB.
- **NCCL / RCCL `Allreduce`** at 16 MB, 32 MB, …, 2 GB. This is the GPU-native collective probe and the direct analogue of the MPI one.

## 12.7 Pseudo code

`[reconstruction]` of the per-run harness and the attribution stage:

```
# --- per job, 64 nodes, on both systems ---
for run in 1..N:
    submit(64 nodes)
    record slurm placement, dragonfly groups, concurrent jobs   # sacct
    gemm_fp16_per_gpu()                                         # GPU probe
    mpi_allreduce(1KB .. 1MB)                                   # host-path collective
    xccl_allreduce(16MB .. 2GB)                                 # NCCL on NVIDIA / RCCL on AMD
    nic_counters_start <- read_cassini()                        # at MPI_Init
    run application (mpiP for AMG/MILC; PyTorch Profiler + HTA for DeepCAM/nanoGPT)
    nic_counters_end   <- read_cassini()                        # at MPI_Finalize
    delta_counters     <- end - start

# --- attribution ---
# stage 1: rank correlation, judged insufficient by the authors
spearman(runtime, {mean,max} of each NIC counter)
# the GPU-exclusion test:
slow_gpu_count <- |{gpus in allocation} ∩ {system-wide slowest 1%}|
spearman(runtime, slow_gpu_count)      # -> 0.07 / 0.08; repeat for 10%, 30%

# stage 2:
features <- placement ∪ gemm ∪ allreduce_proxies ∪ nic_counters{mean,min,max per node}
model    <- XGBoost(features -> runtime), 90/10 split
report MAPE, DirectionAccuracy(eps=0.02); ablate NIC counters out and re-measure DA
```

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact repository identified (`census/IPDPS_2026.md` records `NOT_FOUND_AFTER_SEARCH`). One concrete software contribution is stated but not located: a modification to **HTA** to produce RCCL breakdowns [paper]. Whether that modification was upstreamed is UNKNOWN.

## 12.9 Kernel execution

Not instrumented at warp or SM granularity. The paper's finest GPU-side resolution is:
- **per-device FP16 GEMM throughput** (a whole-device probe), and
- **PyTorch-Profiler-level GPU operations** with compute–communication overlap for the two AI applications [paper].

The GPU-collective decomposition is where the execution-level evidence actually lies, and it is striking [paper] (64-node jobs, Dec 2024 – Apr 2025):
- **AMG2023** — communication is **74% of runtime on Perlmutter, 84% on Frontier**; slowest runs show **40% more** communication time.
- **MILC** — communication **53–56%** of runtime; slowest runs **50% higher on Perlmutter, 122% higher on Frontier**.
- **DeepCAM** — `Allreduce` takes **up to 4× longer on Perlmutter and up to 24× longer on Frontier** in the slowest runs.
- **nanoGPT** — `Allreduce` **3× slower** in the worst Perlmutter cases; "consistent performance" on Frontier.

The 24× Frontier DeepCAM `Allreduce` tail is the single largest effect in the paper, and it is an RCCL/fabric effect on a GPU-resident collective, not a compute effect.

## 12.10 Memory traffic

HBM traffic is not instrumented. The relevant data path is GPU→PCIe→NIC→Slingshot→NIC→PCIe→GPU, and the paper observes three points on it: the GPU end (GEMM, XCCL Allreduce), the PCIe hop (`parbs_*` posted/non-posted blocked counters), and the fabric end (`hni_*_paused`, `rh:*_timeouts`, `lpe_net_match_*`, `atu_cache_hit_*`).

Variability results, with qualifiers — 64-node jobs, four months, Dec 2024 – Apr 2025 [paper]:

| Quantity | Perlmutter (4×A100/node) | Frontier (8 GCD/node, MI250X) |
|---|---|---|
| max application variability | **1.4×** (nanoGPT); 1.3× (AMG2023) | **2.6×** (DeepCAM); 1.8× (MILC, outliers to 3.2×) |
| GEMM spread, system-wide | up to **28%** (12% after outlier removal on 40 GB A100; 5% on 80 GB A100) | up to **15%** (extreme outliers 16%) |
| GEMM spread within one node | up to **10%** (worst case 17%) | NOT_IN_PAPER |
| GEMM spread per individual GPU | within a **2.5%** window | up to **12%** normalised to the same GPU |
| runtime vs slowest-1%-GPU count | Spearman **0.07** | Spearman **0.08** |

Two GPU-level observations that the prior corpus record does not carry:
1. **The 40 GB and 80 GB A100 populations on Perlmutter have different variability** (12% vs 5% after outlier removal) [paper]. The memory-capacity variant correlates with compute-throughput consistency — plausibly a binning or thermal-envelope difference `[inference]`; the paper does not explain it.
2. **Frontier's per-GPU spread (12%) is larger than Perlmutter's (2.5%) while its system-wide spread (15%) is smaller than Perlmutter's (28%).** The MI250X GCDs are individually less repeatable but more homogeneous as a population than the A100s. This is a real architectural contrast and is not drawn out in the paper.

Contention and placement [paper]:
- **"Top users"** — degradation of at least **7% for AMG2023 on Perlmutter when top users collectively occupy over 300 nodes**; similar pattern with different thresholds on Frontier; Spearman **0.55 and 0.60** respectively. Far stronger than any GPU-side correlation.
- **Dragonfly placement does not matter.** nanoGPT and DeepCAM runtimes do not correlate with the number of dragonfly groups spanned — Spearman **0.33** and **0.08**. Authors' conclusion: "Dragonfly topology implementations … maintain high performance and scalability, even when computational tasks are allocated to a large number of dragonfly groups." A second useful negative result.

Feature importance diverges between the machines [paper]:
- **Perlmutter:** `hni_rx_paused_0_mean` and `allreduce_2GB` dominate — "NIC congestion and system network congestion are strong predictors."
- **Frontier:** `lpe_net_match_request_0_mean`, `atu_cache_hit_derivative1_page_size_0_mean`, `hni_rx_paused_0_mean`, and `parbs_tarb_pi_non_posted_blocked_cnt_mean` dominate — "all three describe data movement across the system … uneven load with respect to data handling drives runtime variability."

That Frontier's set includes a **PCIe non-posted-blocked** counter and an **address-translation-cache** counter, while Perlmutter's does not, points at the GPU↔NIC hop and address translation as Frontier-specific pressure points `[inference]` — the paper reports the importances but does not interpret them this way.

## 12.11 Why it is faster/slower (decomposed cause)

The paper decomposes run-to-run variability into five candidate causes and disposes of each:

1. **Slow individual GPUs — REJECTED.** Real heterogeneity exists (up to 28% system-wide on Perlmutter) but does not reach runtime: Spearman 0.07–0.08 against slowest-1%/10%/30% GPU counts [paper].
2. **Job placement across dragonfly groups — REJECTED.** Spearman 0.33 and 0.08 [paper].
3. **Network contention from concurrent jobs — ACCEPTED.** Top-user node occupancy correlates at 0.55–0.60; ≥7% AMG2023 degradation above ~300 top-user nodes [paper].
4. **NIC-level loss and backpressure — ACCEPTED and predictive.** `rh:sct/spt_timeouts` correlate positively; Direction Accuracy collapses to chance when NIC counters are removed [paper].
5. **Host communication software — ACCEPTED, and remediable.** The libfabric 1.20.1 regression fixed on 14 Jan 2025 measurably reduced AMG2023 variability [paper].

The result lands on GPU collectives as the *locus* (up to 84% of AMG2023 runtime is communication; DeepCAM `Allreduce` up to 24× slower on Frontier) with the *cause* upstream of the GPU in the NIC/fabric/host-software stack.

## 12.12 Hardware generation dependence

- Two vendors, two generations: **NVIDIA A100** (Ampere, 40/80 GB HBM2, NVLink 3.0 intra-node) and **AMD Instinct MI250X** (CDNA2, 2 GCDs per package, 64 GB HBM2e per GCD, Infinity Fabric intra-package) [paper]. Both on **HPE Slingshot-11** 3-hop dragonfly with Cassini NICs.
- The *method* is architecture-independent: per-device GEMM normalised to each device's own best, plus NIC counters, plus a gradient-boosted attribution model. It ported from NVIDIA to AMD within the paper, requiring only an HTA extension for RCCL [paper].
- The *findings* are generation-dependent in ways the paper documents: different dominant NIC features per system, different per-GPU versus population spread structure, and a Frontier-only software regression. The A100 40 GB versus 80 GB variability difference is a within-generation binning effect.
- **Counter access is the binding generation/vendor dependence.** Cassini NIC counters were available; **Rosetta switch counters were not** (12.13). The analysis stops at the endpoint because the fabric interior is closed.

## 12.13 Limitations

Stated by the authors [paper]:
1. **The decisive one — no switch counters.** "We suspect this discrepancy might arise because we lack access to network router (Rosetta) counters within the system," offered as the explanation for residual prediction error. The model can see both endpoints and not the fabric interior. (The prior operations-corpus record correctly flags this as the authors' own blocker.)
2. **Truncated AI profiling.** "Profiling the entire execution of AI applications generates hundreds of GB of logs per run," so profiling was limited to five iterations after ten warmup iterations — and consequently "variability depicted in this section might differ from the overall variability shown in Figure 1."
3. **Thin MILC training data on Frontier.** After a Frontier system update MILC stopped converging (reported to OLCF); the Frontier MILC prediction model was trained on **seven runs with another seven for testing** [paper]. Note this is the *model's* training set, not the 38 MILC Frontier jobs collected overall; the XGBoost result for Frontier MILC rests on a very small sample.
4. Correlation analysis alone gave "limited insights"; NIC counters had to be put into the model.
5. Outliers were removed from distribution figures (reinstated in later sections).
6. The AMG2023 Frontier results are reported only for the post-14-January-2025 period, to keep the analysis consistent across a software change.

Observed by this analysis:
7. **Controlled runs, not production jobs** — four applications, fixed 64-node size, fixed inputs. Population validity is absent by design; `GPU-IPDPS26-41` supplies it.
8. **Single job size.** Every run is 64 nodes, so nothing is established about how variability scales — which is the question an operator most wants answered.
9. NIC counters are start/end deltas read at `MPI_Init`/`MPI_Finalize`, so within-run temporal structure of congestion is unavailable; a run cannot be split into congested and quiet phases.
10. Predictive sufficiency is demonstrated (Direction Accuracy ≈ 1.0 with NIC counters, chance without); causation is not, as the prior record also notes.

## 12.14 Relation to prior corpus

- **Prior corpus:** `GPU_DELTA_ANALYSIS`; see the delta notice. The operations-angle analysis in `hpc_systems_operations/corpus/aiops-survey/{synthesis/02_PAPER_CENSUS.md M-25, raw/B, raw/F, raw/G, synthesis/03_SC_REGULAR_PRECEDENTS.md}` is not rewritten.
- **Companion paper, same group, same venue:** `GPU-IPDPS26-41`. Read as a pair — see that file's §12.14. This paper is the controlled arm; that one is the observational arm.
- **Precursor (per the operations corpus, `[inference]` not verified from this paper's own reference list):** *The Case of Performance Variability on Dragonfly-based Systems*, Bhatele et al., IPDPS 2020 — the same question one architecture generation earlier, on CPU-era Dragonfly machines.
- **Directly relevant negative result for this cluster:** the GPU-exclusion test here constrains what `GPU-SC25-01`-style reliability work can claim about *performance*. Degraded-but-alive GPUs are real (28% GEMM spread system-wide on Perlmutter) and yet do not explain application variability (Spearman 0.07–0.08). Any argument that GPU health telemetry predicts application slowdown has to clear this bar.
- **Complementary (verdict-only in this cluster):** *GVARP: Detecting Performance Variance on Large-Scale Heterogeneous Systems* (SC 2024) localises variance by application instrumentation rather than by system counters; *Uncovering Real GPU NoC Characteristics* (MICRO 2024) and *Debunking the CUDA Myth* (ISCA 2025) supply the architecture-side measurements of the GPU interconnect this paper treats as a black box. See `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO — but this is the closest call among the production-performance papers in this cluster, and the reasoning matters.**

verdict_basis: The attribution machinery (repeated runs, NIC counters, XGBoost, Direction Accuracy) is architecture-neutral and is a direct descendant of the authors' CPU-era Dragonfly work, so on method alone this would be borderline. What makes it CORE_GPU is that the paper's substantive contribution is a *GPU-specific falsification*: it builds a per-GPU FP16 GEMM instrument, establishes genuine A100 and MI250X device heterogeneity (28% system-wide on Perlmutter, 12% per-GCD on Frontier), and then shows that heterogeneity does not reach application runtime (Spearman 0.07–0.08), relocating the variance into GPU-resident collectives — NCCL on NVIDIA and RCCL on AMD, with up to 24× `Allreduce` inflation on Frontier — and into the GPU↔NIC PCIe hop visible in the `parbs_*` posted/non-posted counters. That claim cannot be made, or even posed, without multi-GPU-per-node accelerators, vendor-specific collective libraries, and the GPU-to-NIC data path. A CPU study of the same two machines would have no GEMM-heterogeneity arm, no NCCL/RCCL decomposition, and no GCD-versus-whole-device asymmetry.

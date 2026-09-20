# GPU-SC25-01 — Story of Two GPUs: Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `GPU_DELTA_ANALYSIS`
primary_topic: `O — reliability, telemetry & production GPU performance`
secondary_topics: `N (failure-mode taxonomy from production telemetry); GPU memory hierarchy (HBM ECC); NVLink/GPU interconnect reliability`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_VIA_TWO_VERSIONS — arXiv 2503.11901 v1 HTML read in full for authors, system description, data pipeline, error taxonomy, per-XID MTBE/persistence tables, propagation analysis, job-impact tables, and hardware-mechanism explanations; arXiv v4 HTML (current, matching the SC25 camera-ready title) read for the A100-vs-H100 comparison, per-GPU and per-GB MTBE, component-improvement table, HBM3 explanation, availability projection, and limitations. NOT read line-by-line: the v4 related-work section and the full emulation-model derivation.`

---

## PRIOR-ANALYSIS DELTA NOTICE (mandatory, per task §4)

**An existing analysis of this paper already exists in this repository, from an HPC-operations/AIOps angle.** This file is a **GPU-specific delta** and does not restate what the existing documents hold.

The pre-existing analysis is in `domains/hpc_systems_operations/corpus/aiops-survey/`:
- `raw/A_SC_main.md` entry **S25-2** — authors, DOI `10.1145/3712285.3759821`, the framing question ("does the new GPU generation actually get more reliable?"), the data asset (*"Delta/DeltaAI: 1,056 A100+H100 GPUs, 2.5 years, 11.7 million GPU-hours of error data"*), the method (failure-mode taxonomy, MTBE analysis, availability projection), the headline results (*H100 memory MTBE 3.2× worse than A100*; *~5% node overprovisioning needed*), and the limits (one site, mixed-generation cluster, model-based projection).
- `synthesis/02_PAPER_CENSUS.md` entry **M-05** — the same facts in census form, plus publication-type tagging.
- `synthesis/03_SC_REGULAR_PRECEDENTS.md` **§P4** — reads SC20 *GPU Lifetimes on Titan* → SC25 *Story of Two GPUs* as a single lineage, and uses it as a venue-strategy precedent.
- `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` — places it in the UIUC/Iyer group lineage (SC20 Kaleidoscope → SC25).

**What the existing analysis does NOT hold, and what this file therefore adds:** the GPU-architectural substrate. Specifically: which on-package and on-die GPU units the XID codes actually name (GSP, PMU, MMU, NVLink, HBM row-remap engine); the HBM2e-vs-HBM3 capacity/spare-row argument that explains *why* the 3.2× regression exists; the error-*propagation* graph between GPU units; the per-GB normalisation that partly deflates the 3.2× headline; the GH200 NVLink-C2C packaging confound; and the fact that the widely cited "1,056 GPUs / 2.5 years" figure is an aggregate over two very unequal observation windows. The existing analysis also records the window as a flat "2.5 years" for both generations, which this file corrects.

---

## 12.1 Bibliographic facts

- Official title: *Story of Two GPUs: Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs* [paper]. The census records that the seed list had "A Story of Two GPUs" with a leading article; the official title has none (`census/SC_2025.md` §5).
- Venue: SC 2025, DOI `10.1145/3712285.3759821`, pp. 1145–1164 [census; DOI corroborated independently by `hpc_systems_operations` corpus].
- Authors (v1 [paper]): Shengkun Cui, Archit Patke, Ziheng Chen, Aditya Ranjan (all UIUC, equal contribution), Hung Nguyen, Phuong Cao (UIUC), Saurabh Jha (IBM Research), Brett Bode, Gregory Bauer (NCSA/UIUC), Chandra Narayanaswami, Daby Sow (IBM Research), Catello Di Martino (Nokia Bell Labs, São Paulo), Zbigniew T. Kalbarczyk, Ravishankar K. Iyer (UIUC).
- Publication type: `ARCHIVAL_MAIN_PAPER`, with a `PREPRINT` chain on arXiv.
- **Version discrepancy — record this.** arXiv `2503.11901` v1 (2025-03-14) is titled *"Characterizing GPU Resilience and Impact on AI/HPC Systems"* and describes a **Delta-only** fleet of **1,168 GPUs (400 A40, 448 A100, 320 H100)** across 286 GPU nodes, with H100 data explicitly too thin to analyse [paper, v1]. The current version (v4, 2025-12-10) is titled *"Story of Two GPUs…"* and describes **1,056 GPUs (448 A100 + 608 H100)** [paper, v4]. Versions v2 (2025-03-24) and v3 (2025-06-28) lie between [official-web, arXiv abs listing]. The census independently recorded that the "earlier version [was] titled *Characterizing GPU Resilience and Impact on AI/HPC Systems*" (`census/SC_2025.md`), which this reading confirms. **The A40 GPUs present in v1 are absent from the v4 fleet count**; do not mix v1 and v4 numbers.

## 12.2 Core question (one sentence)

Across a production academic AI cluster, does the Hopper generation actually deliver better resilience than Ampere — and the answer is split: markedly better for on-package control/interconnect hardware, materially *worse* for HBM memory, because memory capacity per GPU grew 2.4× while the row-remapping spare-row budget did not grow at all. [paper, v4]

## 12.3 GPU/HPC problem translation

- **Memory.** The central finding is a memory-hierarchy finding: HBM3 at 96 GB/GPU versus HBM2e at 40 GB/GPU, with an unchanged 512-row remap cap [paper, v4].
- **Communication.** NVLink error counts and their inter-GPU propagation are a first-class axis: 1,922 NVLink errors on A100 with 42% inter-GPU propagation, **zero observed on the H100/GH200 fleet** [paper, v4].
- **Compute/scheduling.** The consequence is expressed as a scheduling/capacity-planning quantity: node-availability → required overprovisioning [paper, v4].
- **Synchronization.** Not a synchronization paper.

## 12.4 Why the problem exists (down to hardware root cause)

The paper's causal chain for the memory regression is explicit and is the most valuable GPU-architectural content in it [paper, v4]:

1. **Capacity.** 96 GB HBM3 per H100 versus 40 GB HBM2e per A100 = 2.4× more cells, hence proportionally more exposure to bit flips per GPU-hour.
2. **Physics.** HBM3 uses a *lower signalling voltage*, increasing susceptibility; and more die stacks worsen heat dissipation.
3. **Recovery budget did not scale.** Row remapping — described as the "primary mechanism to mitigate DBE for Ampere and Hopper GPUs" [paper, v1] — is "capped at the same 512 rows" on both A100 and H100 [paper, v4]. So the *mitigation* capacity is flat while the *fault* population grew 2.4×. This is the mechanism behind the headline.
4. **Consequence.** H100 shows a significantly lower per-node MTBE for row-remapping *events* (i.e. remapping fires more often) and **8 row-remapping failures on H100 during its short early-operation window versus none on A100 over a far longer window** [paper, v4].

For the Ampere-side mechanism detail, v1 is the better source [paper, v1]:
- HBM SBEs are corrected by ECC and are not logged; DBEs surface as **XID 48**.
- **XID 63** = row remapping event (spare row substituted; requires GPU reset). NVIDIA Ampere supports up to 512 row remappings, "vs 64 in prior generations."
- **XID 64** = row remapping failure — "all available spare rows for that memory bank are exhausted."
- **XID 94** = *contained* memory error: containment succeeded by "terminat[ing] user processes using faulty memory address," GPU stays operable, no reset.
- **XID 95** = *uncontained* memory error: containment failed, GPU/node reboot required.
- **XID 119** = GSP RPC timeout. The **GSP (GPU System Processor)** is "a coprocessor on-board that offloads driver tasks from CPU," managing GPU initialization. This is the newest unit and the most fragile: 99% of GSP errors put the GPU in an error state, and recovery needs a full node reboot (one case up to 23 hours). The paper notes "AWS recommends disabling GSP for stability over performance benefits."
- **XID 122** = PMU SPI communication error. The **PMU (Power Management Unit)** "regulates frequency, voltage, and power of GPU based on temperature and power cap," communicating over SPI; failure means core and memory clocks cannot be changed.
- **XID 31** = MMU error (invalid access, driver/hardware bug, or bad PMU communication).
- **XID 74** = NVLink error. NVLink uses CRCs on flow-control digits and data and retries "from the last-known good packet."

## 12.5 Mathematical / performance model

Two quantitative instruments [paper]:

1. **MTBE (mean time between errors)**, reported in three normalisations that must not be conflated:
   - *system-wide* node-hours,
   - *per-node* node-hours,
   - *per-GPU* hours, and (v4 only) *per-GB* hours.
2. **Availability → overprovisioning projection** by *emulation* [paper, v4] — the paper's word. It is a model-based extrapolation from measured per-node availability to job-level availability at larger scale, not a measurement at that larger scale.

## 12.6 Data layout and ownership

Mapping the error taxonomy onto the hierarchy [paper]:

| Level | Units / failures observed |
|---|---|
| HBM cell / row / bank | SBE (corrected, unlogged), DBE = XID 48; spare-row pool per bank, 512-row cap |
| GPU die | MMU (XID 31), GSP (XID 119), PMU (XID 122), containment logic (XID 94/95), row-remap engine (XID 63/64) |
| GPU package | "GPU fallen off bus" (XID 79) |
| Intra-node GPU↔GPU | NVLink (XID 74); on GH200, additionally NVLink-C2C CPU↔GPU |
| Node | 4-way / 8-way A100 nodes; 4-way GH200 nodes; reboot is the recovery unit for XID 95/119 |
| Cluster | 1,056 GPUs; Slingshot 11 (400 Gbps+); shared Lustre |

Fleet composition and windows, **v4** [paper, v4]:
- A100 partition: 106 nodes (4-way and 8-way) = **448 A100**, 40 GB HBM2e each; window **895 days, Oct 2022 – Mar 2025**; **9.6M GPU-hours**.
- H100 partition: 152 nodes of 4-way **GH200 Grace-Hopper Superchips** = **608 H100**, 96 GB HBM3 each; window **146 days, Oct 2024 – Mar 2025**; **2.1M GPU-hours**.
- Combined: 1,056 GPUs, 11.7M GPU-hours.

**This is the single most important qualifier in the paper and it is absent from the existing operations-corpus entry, which records a flat "2.5 years" for the whole fleet.** The A100 window is 6.1× longer than the H100 window. Every H100 rate is estimated from 146 days of a partition still in early operation.

Data sources [paper, v1]: 202 GB of system logs from all compute nodes; XID messages extracted by regex; the Slurm scheduler database (start/end, nodes, resources, status, exit codes, command lines). Coalescing: identical errors from the same GPU within a 5-second window are grouped (Algorithm 1); propagation correlation uses Δt = 5 s; persistence capped at 1 day. XIDs 13 (general software error) and 43 (reset channel verification) were **excluded** [paper, v1].

## 12.7 Pseudo code

The paper's Algorithm 1 is an error-coalescing pass `[reconstruction]` of its described behaviour [paper, v1]:

```
for each XID record r in chronological order:
    key <- (r.gpu_serial, r.xid_code)
    if key has an open episode e and r.t - e.last_t <= 5 seconds:
        e.last_t <- r.t                      # extend episode
    else:
        close any open episode for key
        open new episode e(key, first_t=r.t, last_t=r.t)
    # persistence = last_t - first_t, truncated at 1 day

# propagation: for ordered pair (A,B) of XID types on the same GPU or
# on GPUs sharing a node, count episodes of B beginning within 5 s of A
```

## 12.8 Real implementation

No software artifact is claimed. `NOT_INSPECTED` — no repository was identified for this paper. The existing operations-corpus documents note that the SC20 Titan predecessor released data and code (`olcf/TitanGPULife`) and that OLCF released a Summit XID/DBE dataset, but make no such claim for this paper.

## 12.9 Kernel execution

NOT_IN_PAPER. This is a fleet-telemetry study; it does not instrument or model kernel/thread-block/warp execution. Its only contact with the execution model is at the job level: 69.86% of jobs used a single GPU, 27.31% used 2–4, and 2.83% used more than 4 [paper, v1] — i.e. the fleet's workload is overwhelmingly *not* large multi-GPU, which bounds how much NVLink and multi-GPU propagation could matter for observed job failures.

## 12.10 Memory traffic

Not a traffic study. The memory-hierarchy content is the fault/recovery path, quantified as follows.

**Ampere fleet (A100/A40), 855-day v1 window** [paper, v1] — MTBE in node-hours and per-node node-hours:

| Error (XID) | Count | System MTBE | Per-node MTBE | Persistence mean / P50 / P95 (s) |
|---|---|---|---|---|
| Uncontained memory (95) | 38,905 | 0.53 | 2.17 | 860.24 / 75.22 / 340.69 |
| MMU (31) | 18,876 | 1.09 | 4.48 | 2.85 / 2.80 / 5.80 |
| NVLink (74) | 2,987 | 6.87 | 28.28 | 0.76 / 0.24 / 1.18 |
| GSP RPC timeout (119) | 2,136 | 9.61 | 39.55 | 12.14 / 0.03 / 100.85 |
| Row remap event (63) | 95 | 216 | 889.17 | 0.12 / 0.12 / 0.12 |
| Row remap failure (64) | 35 | 586.29 | 2413.45 | 8.88 / 2.90 / 26.65 |
| DBE (48) | 32 | 641.25 | 2639.71 | 0.14 / 0.12 / 0.24 |

Two structural facts follow. First, **GPU memory is ~30× more reliable than GPU hardware by MTBE** on the Ampere fleet (combined hardware 800 node-hours vs combined memory 26,093 node-hours) [paper, v1] — i.e. on Ampere the control/interconnect logic, not HBM, was the dominant failure source. Second, the frequency ranking is dominated by **containment failure**, not by raw bit errors: 38,905 uncontained-memory events versus 32 DBEs. And that count is heavily concentrated — "over 90% originated from a few GPUs" (4 GPUs; one GPU alone accounted for 99% of events), most during the testing phase, and those GPUs were replaced [paper, v1]. **Any use of the 38,905 figure without this concentration caveat is a misreading.**

**A100 vs H100 memory, v4** [paper, v4] — per-GPU MTBE for uncorrectable ECC memory errors:

| Normalisation | A100 (40 GB HBM2e, 895 d) | H100 (96 GB HBM3, 146 d) | Ratio |
|---|---|---|---|
| per-GPU MTBE | 283,271 h | 88,768 h | **3.2× lower on H100** |
| per-GB MTBE | ~11.3 M h/GB | ~8.5 M h/GB | **24% lower on H100** |

The per-GB row matters: roughly three-quarters of the 3.2× per-GPU regression is explained by simply having 2.4× more memory per GPU, and only ~24% is a per-bit-capacity degradation. The paper reports both; secondary citations of the paper generally report only the 3.2×.

**A100 vs H100 hardware, v4** [paper, v4]:

| Component | A100 | H100 | Direction |
|---|---|---|---|
| GSP (119) | 3,857 errors, 6 h system MTBE | 3 errors, 1,168 h system MTBE | dramatically improved |
| PMU SPI (122) | 77 errors | 0 | eliminated in window |
| NVLink (74) | 1,922 errors, 42% inter-GPU propagation | 0 observed | eliminated in window |
| MMU (31) | 8,863 errors; PMU→MMU propagation 88% | 1,737 errors; no PMU→MMU path | ~80% fewer |

Recovery efficacy: considering both uncorrectable-memory recovery paths (row-remap event, and containment after a remap failure), "the impact of uncorrectable memory errors was alleviated 92% of the time on H100" [paper, v4]. The v1 Ampere-fleet equivalents were: row-remapping success 50%, containment-after-remap-failure success 43%, aggregate DBE mitigation 70.6% [paper, v1].

**Propagation structure (Ampere fleet)** [paper, v1] — this is the part with no analogue in the existing operations-corpus entry:
- PMU (122) → MMU (31) with 82% probability, mean propagation 0.05 s.
- GSP (119) → GPU error state with 99% probability.
- NVLink (74): 16% of events affect multiple GPUs, 5% affect 4 or more; intra-GPU recurrence 66%, spread to a neighbouring GPU 14%, terminal 20%.

## 12.11 Why it is faster/slower (decomposed cause)

Not a performance paper. The decomposed causal claim is the resilience one, and it decomposes cleanly into three independent effects [paper, v4]:
1. **Capacity effect** (2.4× more HBM per GPU) — accounts for most of the per-GPU memory regression; visible as the gap between the 3.2× per-GPU and 24% per-GB numbers.
2. **Technology effect** (HBM3 lower signalling voltage, more stacks, worse thermal path) — the residual ~24% per-GB degradation.
3. **Mitigation-budget effect** (512-row remap cap unchanged) — turns a manageable per-GB degradation into *observed remap failures*, since the spare-row pool is consumed faster relative to the fault population. This third effect is a design decision, not physics, and is the paper's actionable finding.

Against these, the Hopper generation's *logic* resilience improved, which the authors attribute to maturation of the GSP firmware/detection path and (implicitly) to the GH200 packaging removing the discrete NVLink topology that generated A100's NVLink errors `[inference]` — the authors themselves decline to attribute the NVLink zero (see 12.13).

## 12.12 Hardware generation dependence

Maximally generation-dependent — the paper *is* a generation comparison. Key dependencies:
- A100 = 40 GB HBM2e, discrete SXM/PCIe nodes in 4-way and 8-way configurations [paper, v4].
- H100 = 96 GB HBM3, delivered as **GH200 Grace-Hopper Superchips**, with the H100 "tightly coupled to NVIDIA Grace CPUs via NVLink-C2C" [paper, v4]. This is a packaging change, not only a GPU change, and the authors flag it as a confound (12.13).
- Row-remap cap: 512 rows on both Ampere and Hopper; 64 on pre-Ampere parts [paper, v1 + v4]. This makes the paper's mechanism directly applicable to reasoning about Blackwell-class parts with larger HBM: the argument predicts the regression worsens unless the spare-row budget scales with capacity `[inference]`.
- The GSP is an Ampere-and-later unit; its near-elimination between A100 and H100 is a firmware/driver maturity effect, so it is a *deployment-time* dependence as much as a silicon-generation one `[inference]`.

## 12.13 Limitations

Stated by the authors [paper, v4]:
1. **Unequal windows** — 146 days of H100 versus 895 days of A100, "limiting statistical confidence."
2. **Packaging confound** — GH200's NVLink-C2C CPU–GPU integration means "differences in CPU–GPU integration may lead to variations in resilience characteristics"; H100-vs-A100 is not a clean silicon comparison.
3. **The NVLink zero is not confirmed as a hardware improvement** — the authors cannot rule out "potential changes in NVLink error logging mechanisms." A zero in a log is not a zero in the hardware.
4. Application-level recovery is "largely ineffective" except for MMU and NVLink errors.
5. No direct comparison with Blue Waters / Titan / Summit, because those used older GPU generations "lacking latest resilience [mechanisms] central to our study."

Observed by this analysis:
6. Single site, single vendor, and a fleet whose job mix is 70% single-GPU [paper, v1] — so the NVLink and multi-GPU propagation findings rest on a small slice of the workload.
7. The uncontained-memory-error count is dominated by 4 GPUs, 1 of which produced 99% of events, mostly during a testing phase [paper, v1]. Rate statistics built on it describe a few bad parts, not the fleet.
8. The overprovisioning projection is emulation-based [paper, v4]; the "over $1 million per month" cost figure depends on an unstated pricing assumption and should not be reused as a portable fact.
9. Version drift: fleet composition, title, and headline claims changed materially between v1 and v4 (see 12.1). Any citation must name the version.

## 12.14 Relation to prior corpus

- **Prior corpus:** `GPU_DELTA_ANALYSIS` — see the delta notice at the top. The operations-angle analysis in `hpc_systems_operations/corpus/aiops-survey/{raw/A_SC_main.md S25-2, synthesis/02_PAPER_CENSUS.md M-05, synthesis/03_SC_REGULAR_PRECEDENTS.md §P4, synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md}` is not rewritten here.
- **Precursor (verified from the paper's own text):** the authors explicitly position against Blue Waters, Titan and Summit studies as prior-generation [paper, v4]. The SC20 *GPU Lifetimes on Titan* lineage is asserted by the operations corpus, not by the paper text I read; treat the lineage claim as `[inference]` from the operations corpus rather than `[paper]`.
- **Directly complementary in this cluster, and the key architecture bridge:** `GPU-ICS24-01` (*Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study*) is the Volta/HBM2 predecessor of exactly this measurement, using the same XID vocabulary (48/63/64) on 27,756 V100s. The two together give a three-generation HBM2 → HBM2e → HBM3 series on the same failure mechanism, and they *disagree in emphasis*: Summit finds DBE recurrence concentrated on individual GPUs and correlated with short-term power swings rather than temperature, while this paper finds the binding constraint to be the unchanged spare-row budget. See `GPU-ICS24-01` §12.14.
- **Complementary (verdict-only in this cluster):** *Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems* (SC 2025, Aurora/Intel Max GPUs) is the closed-loop remediation counterpart; *Demystifying the Resilience of Large Language Model Inference* (SC 2025) and *GPU Faults Across Cloud Providers* (SC 2026 seed) are adjacent. See `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: Every mechanism in the paper is a GPU-specific failure mode named by a GPU-specific telemetry vocabulary: NVIDIA XID codes for the GSP coprocessor, the PMU SPI link, the GPU MMU, NVLink CRC retry, and the HBM row-remapping engine with its 512-spare-row budget and its contained/uncontained containment states. The central finding — that a generation's memory resilience regressed because HBM capacity per GPU grew 2.4× while the row-remap spare pool stayed at 512 rows — has no CPU analogue, since it is a property of the GPU's on-die DRAM repair mechanism. A CPU DRAM field study would use MCE/CE-UE counters and page offlining, and would produce neither the GSP/PMU/NVLink taxonomy nor the row-remap-budget argument.

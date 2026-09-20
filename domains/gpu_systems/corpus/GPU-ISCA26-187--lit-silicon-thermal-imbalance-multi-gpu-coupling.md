# GPU-ISCA26-187 — Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `Multi-GPU execution & collectives; straggler behaviour in synchronous training`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2511.09861v2) — authors/affiliations, abstract, motivation, the temperature/frequency profiling result, the four-phase coupling mechanism, the overlap-ratio and lead-value metrics and their algorithms, the three mitigation use cases with their algorithms, both testbed nodes, the full sensitivity study (aggregation, window, max adjustment, power-cap initialisation, warm-up, precision, batch/sequence length, node variability), the model-accuracy check, the five stated limitations, and related work. NOT read line-by-line: every figure panel and the analytical model's derivation.`

---

## CROSS-CLUSTER NOTE

This paper carries a **watchlist row in `_LEDGER_core_execution.md:88`** from this project's own STEP C pass, with a *provisional, title-and-census-level* verdict of `RELATED_GPU` and the note "thermal/power at multi-GPU scope, not core execution". That row explicitly marked itself as provisional and not deep-analysable. **With the full text read, the verdict is corrected to `CORE_GPU`** (see the counterfactual record) and the paper is analysed here, in its correct cluster. The core-execution ledger's instinct was right on one point and should be recorded: it flagged this paper as a *confound for instruction-throughput measurement*, which the full text confirms — per-GPU DVFS makes two nominally identical GPUs in the same node run at frequencies differing by **1.062×**.

## 12.1 Bibliographic facts

- Official title: *Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs* [paper].
- Authors: **Marco Kurzynski** (University of Central Florida), **Shaizeen Aga** (Advanced Micro Devices, Inc.), **Di Wu** (University of Central Florida) [paper].
- Venue: **ISCA 2026**, session **9D Sustainability and Energy Efficiency** (`census/ISCA_2026.md:51`). DOI `UNKNOWN`.
- Publication type: `ARCHIVAL_MAIN_PAPER`; read as `PREPRINT`, arXiv **`2511.09861v2`**.
- **Census correction:** `census/ISCA_2026.md` recorded authors `UNKNOWN` and `NOT_FOUND_AFTER_SEARCH` for a preprint. Both are now resolved — authors above, arXiv `2511.09861`.
- Artifact: `NOT_FOUND_AFTER_SEARCH`. The implementation is stated as *"~200 lines of PyTorch code with no GPU kernel rewrites"* [paper]; no repository is named in the text read, so **no `[code]` evidence and no symbols are asserted**.

## 12.2 Core question (one sentence)

Why do eight identical GPUs in one node, running identical work, diverge into persistent "leader" and "straggler" roles — and can the divergence be removed by moving power between them rather than by changing the code? [paper]

## 12.3 GPU/HPC problem translation

- **Thermal/power.** Per-GPU DVFS responding to per-GPU temperature is the independent variable.
- **Synchronization.** Synchronous FSDP training turns a frequency difference into a wait.
- **Compute/communication.** Concurrent computation–communication (**C3**) — overlapping collective and compute kernels on one device — is the second half of the coupling.
- **Scheduling.** The mitigation is a node-level power *allocator*, not a scheduler of work.

## 12.4 Why the problem exists (hardware root cause)

The paper's claim is that two independently benign mechanisms combine into a stable pathology [paper]:

1. **Per-device DVFS makes nominally identical GPUs physically unequal.** Profiling across one node found the highest GPU temperature at **1.155×** the lowest and the highest frequency at **1.062×** the lowest, with temperature rank and frequency-throttling rank correlated. This is the same class of finding as `GPU-MICRO25-185`'s chassis-position thermal skew, reached on different hardware (AMD MI300X rather than air-cooled HGX).
2. **C3 makes kernel duration depend on how much contention a GPU is experiencing.** When a communication kernel and a compute kernel share a device's compute and memory resources, each slows the other — so a GPU that is *behind* is, paradoxically, sometimes *faster per kernel* because its overlap is lower.

**The four-phase coupling, per training iteration** [paper]:

| Phase | What happens |
|---|---|
| ① | All GPUs start synchronised; variation is minimal. |
| ② | Variation accumulates layer by layer. Leaders (cooler, higher frequency) run faster on **constant-overlap** kernels (0 % or 100 % overlap), building a "lead value". |
| ③ | The straggler's communication starts late, so it has **less concurrent contention** and now runs *faster* than the leaders on **varying-overlap** kernels. Leaders wait longer. |
| ④ | Lead gains and lag gains balance; the node reaches an equilibrium in which **leaders idle at the iteration boundary**, burning power to wait. |

The effect is therefore self-stabilising rather than self-correcting: the system finds an equilibrium that wastes power on the leaders instead of eliminating the imbalance.

**Magnitude:** C3 alone changes GPU kernel runtime by **18.9 % on average and up to 40.0 %** [paper]. Leaders reach an overlap ratio of **52.7 %**, **1.8×** the straggler's **29.6 %**. On constant-overlap kernels the straggler is **5–10 % slower**; on varying-overlap kernels it is **1.5× faster** — the contradiction that makes the coupling visible.

## 12.5 Mathematical / performance model

Two constructed metrics plus an analytical power/throughput model [paper]:

- **Overlap ratio** — weighted average of the fraction of each computation kernel's duration that overlaps a communication kernel.
- **Lead value** (`LeadValueDetect`, Algorithm 1) — for each kernel, `max(start timestamp over GPUs) − (this GPU's start timestamp)`, then aggregated per GPU. `sum` is the default aggregation (chosen because it keeps penalising a GPU even at equilibrium); `max` and `last` converge to the same outcome.
- Association between overlap ratio and kernel duration is assessed by **Pearson correlation and cosine similarity**, reported as "high degrees of correlation for most kernels and GPUs" — **no numeric coefficient is given in the text**, so none is quoted here.
- **Model accuracy is asymmetric and the authors say so:** predicted **power is within ≤1 %** of measurement, but predicted **throughput is about 2× the measured value** — the model captures the diminishing-returns trend but overestimates magnitude, attributed to omitting temperature and voltage variation. **Only the power side of this model should be reused.**

## 12.6 Data layout and ownership

| Level | Configuration [paper] |
|---|---|
| Node | **2 nodes**, each **8× AMD Instinct MI300X** + **2× AMD EPYC 9684X** |
| GPU power cap range swept | **500–700 W** per GPU |
| Node CPU power budget (CPU-Slosh) | **10–50 W** reallocated |
| Cooling | **not specified** in the paper |
| Workloads | Llama 3.1 8B (default), Mistral 7B v0.1; PyTorch **FSDP v1 and FSDP2** |
| Precision | **bf16** (default) and **fp8** via Transformer Engine |
| Shape | batch 1/2/4 (default 2), sequence 4K (default)/8K |
| Protocol | 1000 iterations per experiment, 50-iteration warm-up (default) |

**Node-to-node variability is itself a result:** Node 0 has *multiple* stragglers, which limits how much power can be taken off the leaders; Node 1 shows a clean single-straggler pattern [paper]. Two nodes of the same SKU do not have the same thermal personality.

## 12.7 Pseudo code

`[reconstruction]` of the three algorithms as described:

```
# Algorithm 1 — detection
every `sampling_period` (default 10) iterations, over a window (default 3):
    for each kernel k: lead[g][k] = max_over_g'(start[g'][k]) - start[g][k]
    lead[g] = sum_k lead[g][k]              # default aggregation

# Algorithm 2 — IncPowerGpu
normalise lead[] ; delta_power[g] ∝ lead[g] , clamped to max_adjustment (5..30 W)
decay the adjustment across iterations to avoid overshoot

# Algorithm 3 — AdjPowerNode
apply delta_power[]; if node budget exceeded, scale all GPUs down uniformly
never exceed per-GPU TDP
```

## 12.8 Real implementation

No artifact located. Stated implementation: **~200 lines of PyTorch**, no GPU kernel rewrites, sitting as a node-level power-management layer *orthogonal* to GPU-level and cluster-level power policies [paper]. The control actuator is **per-GPU power capping** (the cap value, not a locked clock) — worth noting against `GPU-ASPLOS24-186`, which argues power capping is *reactive* and therefore the weaker lever; here reactivity is acceptable because the target is a steady-state frequency equilibrium over hundreds of iterations, not a sub-second spike.

## 12.9 Kernel execution

The unit of analysis is the **kernel**, classified by its overlap behaviour: *constant-overlap* kernels (0 % or 100 % overlapped with communication) versus *varying-overlap* kernels. That classification is what makes the straggler's apparent speed-up legible rather than contradictory [paper].

## 12.10 Memory traffic

Not instrumented. Memory-resource contention between concurrent compute and communication kernels is named as one of the two shared resources driving C3 interference, but no bandwidth measurement is reported [paper].

## 12.11 Findings and mitigation (decomposed cause)

Three mitigations, all on **8× MI300X** nodes running Llama 3.1 8B / Mistral 7B under FSDP [paper]:

| Use case | Mechanism | Throughput | Power |
|---|---|---|---|
| **GPU-Red** | lower the cap on **leaders only** — they were burning power to wait | **0 %** (unchanged) | **−4 %** |
| **GPU-Realloc** | move power from leaders to the straggler under a fixed node cap | **+3 %** | **0 %** |
| **CPU-Slosh** | harvest CPU power — only **13.5 % of CPU cores are utilised** during training — and give it to the GPUs | **+4 %** | **+3 %** |

Sensitivity results that matter for reuse [paper]:
- **Power-cap initialisation is the most influential parameter**, but the *converged* power distribution is reusable across frameworks and models — i.e. the node's thermal personality is a stable property, learnable once.
- Warm-up length (3–50 iterations) barely matters; immediate adjustment is recommended.
- **The effect is almost equally present in bf16 and fp8** — it is not an artefact of one precision.
- 4 % power saving and 2.5–3.5 % throughput gains hold across batch sizes and sequence lengths.

The paper's headline cost figure — *"4% power saving translates to over $147 million saved annually"* across 6 GW of AMD GPU deployment at $0.14/kWh — is an extrapolation from a two-node measurement to a fleet, and must be carried with that qualifier.

## 12.12 Hardware generation dependence

Measured only on **AMD MI300X**. The authors state the effect *"theoretically applies to all systems with multiple devices in a node, where per-device DVFS is equipped"* — that is a hypothesis, not a measurement, and this corpus should treat it as such. Note that MI300X is also the subject of the SC 2025 CDNA3 characterisation paper (watchlisted in this cluster), and that `GPU-ISC26-182` shows MI300A reports power **per package**, mixing CPU and GPU — a reporting property that would make the CPU-Slosh accounting harder to audit on an APU than on the discrete MI300X used here.

## 12.13 Limitations (authors' own, plus review)

1. Validated on **MI300X only**; other vendors and accelerators are future work.
2. **Single-node scope**; cluster-scale impact unknown.
3. Not integrated with inference frameworks (vLLM and KV-cache serving named as the obvious next target).
4. More aggressive 4-bit precision unstudied.
5. Algorithm 3 never exceeds TDP, but **long-term reliability under sustained re-allocated power caps is not empirically validated**.

**Review-side, and it is the weak point of an otherwise careful paper.** The **instrumentation chain is not disclosed**. The paper reports per-GPU temperature and frequency and per-GPU power, but names **no sensor, no query interface (`rocm-smi`/`amd-smi`/SMI-lib), no sampling rate and no averaging treatment**, and uses **no external ground truth** (no PDU, wall meter or thermal camera). Its only stated cadence — "sampling period 10 iterations, window 3 iterations" — is the *control loop's* period, not the sensor's. Read against `GPU-ISC26-182`, which establishes that AMD's `rocm-smi`/`amd-smi` **power** field is an **undocumented running average** while the **energy counter** is the trustworthy 1 ms source, the 4 % power saving and the ≤1 % power-model accuracy are being claimed against a reference whose filtering is unknown. The *relative* comparison (leader vs straggler on the same node, same sensor) is robust to a shared filter; the *absolute* 4 % and the $147 M extrapolation are not `[inference, grounded in GPU-ISC26-182's measured AMD sensor properties]`.

## 12.14 Relation to prior corpus

- **Cites `GPU-ASPLOS24-186` (POLCA).** The related-work section names *Patel et al. (2024), "Characterizing Power Management Opportunities for LLMs in the Cloud"* [paper] — **lineage verified from this paper's own citation.** The relationship is a genuine inversion: POLCA takes power *away* from GPUs at row scale to fit a facility budget; Lit Silicon moves power *between* GPUs inside one node to remove a synchronisation loss. Both are frequency/power-cap actuators; they operate at different levels and are compatible, and Lit Silicon explicitly positions itself as *orthogonal* to cluster-level policy.
- **Converges with `GPU-MICRO25-185` on the same physical fact from opposite vendors.** Georgia Tech measured **up to 27 % temperature differential between rear and front GPUs** in air-cooled NVIDIA HGX nodes and **5–10 °C intra-package skew on MI250**, and showed the hotter GPUs throttle their clocks. UCF/AMD measured **1.155× temperature and 1.062× frequency spread** across an 8-GPU MI300X node and showed it produces persistent stragglers. **Two independent groups, two vendors, two chassis types, one conclusion: GPUs in a node are not interchangeable, and the difference is thermal.** Neither paper cites the other. Lit Silicon adds the part MICRO'25 does not have — the *mechanism* by which the thermal difference converts into a synchronisation equilibrium, and a fix.
- **`GPU-ICS24-01` (Summit).** The straggler/leader equilibrium described here means a subset of GPUs in every node repeatedly ramps and idles at iteration boundaries — the power-swing signature Summit associated with GPU memory double-bit errors. **`GPU-ASPLOS24-186` independently measures those boundary dips at 20–75 % of TDP.** Lit Silicon's `GPU-Red` mitigation, which lowers leader caps so they stop ramping and waiting, would as a side effect *reduce* that swing. Nobody has tested this `[inference, grounded in the three papers' measured quantities — asserted by none of them]`.
- **Related-work lineage from this paper's own citations:** Agrawal et al. 2025 (ConCCL — DMA engines to offload communication and cut compute interference); Chung et al. 2024 (reducing energy bloat in large-model training via straggler mitigation); Wang et al. 2025 (analytical performance/power model with fine-grained DVFS for AI accelerators).

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The effect is created by **per-GPU DVFS reacting to per-GPU die temperature inside one node** (measured spread: 1.155× temperature, 1.062× frequency across 8 MI300X) interacting with **concurrent computation–communication on a single GPU's shared compute and memory resources** — i.e. a collective kernel and a compute kernel contending on the same SMs/CUs, which is a GPU execution property with no CPU analogue. The mitigation actuates **per-GPU power caps** and the observed gains are 4 % power / 3–4 % throughput on that specific hardware.

verdict: `CORE_GPU`

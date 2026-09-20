# GPU-ASPLOS24-186 — Characterizing Power Management Opportunities for LLMs in the Cloud (POLCA)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` + `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `O — production cluster telemetry; facility power provisioning`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER. Primary read: the arXiv preprint PDF (arxiv.org/pdf/2308.12908) — motivation, testbeds, DCGM methodology, prompt-vs-token power phases, input/batch/output sweeps, production-trace characterisation, training power swings, frequency-vs-power-capping comparison, the POLCA two-threshold policy, the simulator, the oversubscription result, limitations and related work. Then the ARCHIVAL ASPLOS'24 PDF (microsoft.com/en-us/research/wp-content/uploads/2024/03/GPU_Power_ASPLOS_24.pdf) was fetched and used to verbatim-confirm the ten load-bearing facts listed in 12.1. NOT read line-by-line in the archival version: the full figure set and the simulator's internals.`

---

## PRIOR-CORPUS NOTE

No existing analysis here. **`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` (not imported)** and is the natural home of the LLM-serving power literature — **no claim is made about its contents**; flag `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. This paper is analysed here because its subject is the **GPU's own power-capping and frequency-capping control path and its latencies**, which is taxonomy P, not LLM serving policy.

`domains/gpu_systems/census/ASPLOS_2024.md:107` lists it in Session **4C: Power and Energy** with GPU centrality `UNRESOLVED` from title alone. **Resolved here: `CORE_GPU`.** Also resolved: authors and the public PDF, which the census recorded as `NOT_SEARCHED`.

## 12.1 Bibliographic facts

- Official title: *Characterizing Power Management Opportunities for LLMs in the Cloud* [paper, official-web].
- Authors: **Pratyush Patel, Esha Choukse, Chaojie Zhang, Íñigo Goiri, Brijesh Warrier, Nithish Mahalingam, Ricardo Bianchini** (Microsoft Azure Research and collaborators) [official-web].
- Venue: **ASPLOS 2024**, April 2024, Session 4C "Power and Energy". DOI `UNKNOWN` — the Microsoft Research publication page does not give one and `dl.acm.org` is unreachable here.
- Publication type: `ARCHIVAL_MAIN_PAPER`. Public archival PDF hosted by Microsoft Research (URL in `read_depth`).
- **Title/preprint linkage, stated explicitly because it matters.** The arXiv preprint `2308.12908` is titled ***POLCA: Power Oversubscription in LLM Cloud Providers*** with the **same seven authors in the same order** [official-web]; the ASPLOS paper's framework is named POLCA and its abstract carries the same "30% more servers" claim [official-web, MSR publication page]. The ten facts below were re-verified **verbatim against the archival ASPLOS PDF**, so nothing load-bearing in this file rests on the preprint alone except where marked.
- **Verbatim-confirmed against the archival PDF** [paper]: (a) *"We run DCGM at a 100ms interval to capture the power draw, utilization, compute / memory activity, and other performance counters on each GPU"*; (b) *"two NVIDIA DGX A100 virtual machines with 8×A100-40GB and 8×A100-80GB GPUs respectively"*; (c) *"a six-week power consumption trace between June 21st to August 2nd 2023 from the production inference cluster"*, 40 servers, one row of racks; (d) training peak power utilisation **97 %** with *"Max. power spike in 2s 37.5%"*, inference **79 %** with *"Max. power spike in 40s (OOB capping latency) – 11.8%"*; (e) **T1 = 80 %** → low-priority capped to **1275 MHz**; **T2 = 89 %** → low-priority **1110 MHz**, then high-priority **1305 MHz**; (f) *"Power brake is a faster OOB lever that brings all GPUs down to almost a halt within 5 seconds"* with *"OOB control latency 40s"*; (g) *"we add 30% more servers … to stay strictly within the workload SLOs"*, with *"<1% P50 latency impact"* for high-priority; (h) *"Power capping is reactive and triggers when power exceeds a set threshold"* while *"Frequency locking reduces overall power on demand with minimal performance loss"*; (i) iteration-boundary dips — RoBERTa *"at 75% of the TDP"*, GPT-NeoX *"drops down to 50%"*, Flan-T5 *"goes down all the way to 20%"*; (j) *"CPUs provide interfaces like IPMI (OOB) and RAPL (IB), which serve as a fast and reliable mechanisms"* contrasted with GPU controls being *"much slower and may take up to 40 seconds to execute"*.
- Preprint-only figures used below and marked as such: the powerbrake target frequency **288 MHz**, and the A100 control ranges (power cap 100–400 W, SM clock 0.2–1.4 GHz) `[paper, preprint]`.
- Artifact: `NOT_FOUND_AFTER_SEARCH`.

## 12.2 Core question (one sentence)

Given how much power an LLM GPU cluster actually draws and how fast the GPU's power controls can respond, how much of the provisioned facility power can be safely oversubscribed? [paper]

## 12.3 GPU/HPC problem translation

- **Power control path.** The object of study is the **GPU's own capping machinery** and, decisively, **its latency**.
- **Scheduling.** A two-threshold, two-priority frequency-capping policy driven by row-level PDU telemetry.
- **Compute.** LLM inference's prefill (compute-bound, parallel over all prompt tokens) and decode (sequential, KV-cache-served) phases have different power signatures, which is the source of the headroom.

## 12.4 Why the problem exists (hardware root cause)

This is the paper's real contribution to this cluster, and it is a statement about GPU hardware, not about LLMs [paper]:

1. **GPU power capping is *reactive*.** A power cap triggers *after* power crosses the threshold. The prefill phase's power spike therefore **escapes the cap entirely** — spikes last **< 1 second** and *"often go beyond GPU's TDP values"*. Frequency locking is *proactive* — it prevents the spike — but pays performance throughout execution, not just at the spike.
2. **The out-of-band control path is slow.** Row power managers read PDU telemetry and reach each server's BMC over NVIDIA's **SMBPBI** interface; **OOB frequency capping takes up to 40 s**, and the emergency **powerbrake** (all GPUs to near-halt, `288 MHz` `[preprint]`) takes **5 s**. A UPS failure must be survived in ~10 s, so powerbrake is the only lever that fits.
3. **In-band control is unavailable in this deployment model.** Direct Device Access (DDA) GPU passthrough into customer VMs means the platform cannot use the in-band driver path at all; it is stuck with the slow OOB one.
4. **The GPU has no RAPL.** The paper states the contrast directly (fact (j) above): CPUs have IPMI out-of-band and **RAPL** in-band as *fast and reliable*; the GPU equivalents are *"much slower"*. **This is the cleanest statement in the whole cluster of why GPU power management is not a re-run of CPU power management.**

The policy's design constant follows mechanically: T2 = 89 % is chosen so that the **11.8 % maximum spike over a 40 s window** — i.e. over exactly one OOB command latency — still fits under 100 %.

## 12.5 Mathematical / performance model

No analytic model. The control law is a hysteretic two-threshold state machine [paper]:

```
p <- normalised row power from PDU
if p > 100%: powerbrake all GPUs                      # 5 s
elif p > T2 (89%): cap LP GPUs to 1110 MHz
                   if still above: cap HP GPUs to 1305 MHz
elif p > T1 (80%): cap LP GPUs to 1275 MHz            # A100 base clock
uncap with 5% hysteresis (below 75% for T1, below 84% for T2)
```

Note **1275 MHz is the A100's base frequency** — T1's action is "stop boosting low-priority work", which is why it costs almost nothing.

## 12.6 Data layout and ownership

| Level | What is measured / controlled |
|---|---|
| GPU | DCGM at **100 ms**: power draw, utilisation, compute/memory activity, counters |
| Server (8 GPUs) | BMC, reached over **SMBPBI**; GPUs are ~**50 % of server power** `[preprint]` |
| Row of racks (40 servers) | **PDU** telemetry — the control input |
| Facility | provisioned power budget; UPS ride-through ~10 s |

Testbeds: two **DGX A100** VMs, **8×A100-40GB** (training) and **8×A100-80GB** (inference), dual-socket AMD Rome, PCIe 4.0, NVLink 3.0 `[preprint for the CPU/interconnect detail]`. Models: RoBERTa (encoder), GPT-NeoX-20B / OPT-30B / BLOOM-176B (decoder), Flan-T5-XXL (encoder-decoder).

## 12.7 Pseudo code

See 12.5 — the paper's Algorithm 1 is reproduced there in condensed form `[reconstruction]` of its control flow.

## 12.8 Real implementation

No artifact. Verified tool chain [paper]: **NVIDIA DCGM at 100 ms** for per-GPU telemetry; `nvidia-smi` for the in-band control sweeps during characterisation (power caps in the **325–400 W** subset of a **100–400 W** range, SM clocks in the **1.1–1.4 GHz** subset of a **0.2–1.4 GHz** range) `[preprint]`; **SMBPBI** out-of-band for production control; a discrete-event simulator for the oversubscription evaluation, whose synthetic replication of the production trace matches it to within **3 % MAPE** `[preprint]`.

## 12.9 Kernel execution

Not resolved to kernels. The execution unit that matters is the **inference phase**: prefill processes all prompt tokens in parallel and is compute-intensive; decode is sequential and KV-cache-served and draws *"stable, lower power"* [paper].

## 12.10 Memory traffic

Not instrumented directly. Implied: the KV cache is what makes decode memory-bound and therefore low-power, and batch size raises peak power because it enlarges the prefill computation [paper].

## 12.11 Findings (decomposed cause)

All figures are **A100** (40 GB or 80 GB as noted) unless stated:

1. **Inference clusters leave ~20 % of provisioned power unused; training clusters leave ~3 %.** Peak power utilisation **79 % vs 97 %**; max 2-second spike **11.8 % (inference, over 40 s) vs 37.5 % (training, over 2 s)** [paper]. Inference power is diurnal; training power swings coherently every few seconds.
2. **Input length drives peak power; output length does not.** Raising the prompt from 256 to 8192 tokens pushes peak power up sharply (approaching the TDP ratio for BLOOM-176B at 8192) while **mean power stays low and flat**; output length changes latency linearly but *"does not affect the peak and mean power"* [paper]. **This is the cleanest available demonstration that mean GPU power is a poor proxy for provisioning.**
3. **Frequency reduction buys power superlinearly.** Up to **20 % peak power reduction for at most ~7 % performance loss** on inference; GPT-NeoX loses *no* performance at ~13 % peak power reduction while BLOOM-176B loses 5 % at the same setting [paper]. For training, ~20 % peak power for ~10 % performance loss on Flan-T5 and GPT-NeoX.
4. **Training power swings are large, coherent and synchronisation-driven.** At iteration boundaries power falls to **75 % of TDP (RoBERTa)**, **50 % (GPT-NeoX)** and **20 % (Flan-T5 — the GPUs' idle power)**, and the paper warns these *"will be correlated across thousands of GPUs working on the same training job, potentially causing challenges in the power delivery infrastructure"* [paper].
5. **Result:** T1 = 80 %, T2 = 89 % permits **30 % more servers in a 40-server row** (i.e. +12 servers) within SLOs — high-priority throughput within 1 % of baseline, low-priority within 2 % — and **zero powerbrake events across the six-week trace**, against 10¹–10⁴ events for baseline policies `[preprint for the event counts]`.

## 12.12 Hardware generation dependence

Entirely **A100**. The authors name single-vendor evaluation as a limitation. Every constant in the policy — 1275 MHz base clock, 1305/1110 MHz cap points, 288 MHz powerbrake, the 40 s and 5 s OOB latencies, the 400 W cap range — is an A100-and-SMBPBI constant and must be re-derived for H100, MI300 or anything else.

## 12.13 Limitations (authors' own, plus review)

1. Training oversubscription is *"tricky"* because swings are correlated across thousands of GPUs.
2. OOB latencies (40 s / 5 s) bound responsiveness; only powerbrake fits the ~10 s UPS window.
3. DDA virtualisation blocks in-band control, forcing reliance on SMBPBI.
4. Model churn requires periodic retuning of T1, T2 and the cap frequencies, against a 4–6 year hardware lifetime.
5. Two priority classes is a coarse abstraction of heterogeneous latency requirements.
6. Production numbers are normalised and confidential, limiting reproducibility.
7. **NVIDIA A100 only**; other vendors unexplored.

**Review-side.** The whole characterisation is **DCGM at 100 ms**, and DCGM sits on the same NVML power path that `GPU-SC24-181` measured. On **A100** that path publishes every **100 ms** while its boxcar observes only **25 ms** of each period. Polling DCGM at exactly 100 ms therefore does **not** yield 100 ms-resolved power — it yields one 25 ms-wide observation per 100 ms, with an uncontrolled phase. The paper's most important quantity is a **sub-second peak** (prefill spikes *"< 1 second"*), which is precisely the regime that sampling destroys. **Reported peak power and spike percentages are therefore lower bounds**, and the real headroom for oversubscription may be smaller than 20 % `[inference, grounded in GPU-SC24-181's measured W = 25 ms / T = 100 ms for A100 and this paper's own sub-second spike duration]`. This does not overturn the paper — the policy is built around a slow 40 s control loop, for which 100 ms sampling is ample — but it does mean the *characterisation* figures and the *control* figures have very different error bars, and the paper treats them alike.

## 12.14 Relation to prior corpus

- **`GPU-ICS24-01` (Summit) — a direct, quantitative bridge.** Summit established that GPU double-bit memory errors correlate with short-term **power swings** (~33 W range over 15 minutes on V100), not temperature. This paper measures the *same physical phenomenon from the supply side* on a different machine class and names it as an infrastructure hazard: training power falling to **20–75 % of TDP at every iteration boundary, coherently across thousands of GPUs**. Neither paper cites the other. Together they say that synchronous distributed training is a **power-swing generator**, and that such swings are the covariate Summit found predicts memory failure `[inference, grounded in both papers' measured quantities]`.
- **`GPU-MICRO25-185`** reaches the same place from the software side — microbatch size past its optimum produces bursty execution and peak power excursions — and adds the thermal consequence. POLCA supplies the facility-side cost of those excursions and the reason they cannot be capped away: **the cap is reactive and the OOB loop is 40 s**.
- **`GPU-SC24-181`** is the measurement-fidelity precondition for everything in 12.11 (see 12.13).
- **`GPU-SC25-184`** supplies the complementary physics: prefill is compute-and-datapath-heavy while decode is control-heavy and cache-served, which is *why* their power signatures differ.
- **Related-work lineage from this paper's own citations** (selected, GPU-specific): Patki et al. 2019 comparing GPU power capping against frequency capping; Peres 2013 reverse-engineering GPU power management; Sinha et al. 2022 on GPU variability at scale; Jahanshahi et al. 2020 (GPU-NEST) on multi-GPU inference-server energy — note **A. Jahanshahi is also first author of the ICS 2026 grid-regulation paper on this cluster's verdict-only list**; You et al. 2023 (Zeus), which is the measurement library `GPU-MICRO25-185` later modifies.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution turns on properties of **the GPU's own hardware power-capping controller and its control path** — that the power cap is *reactive* so sub-second prefill spikes exceed TDP before it engages, that out-of-band frequency capping over **SMBPBI** takes up to **40 s** and powerbrake **5 s**, that DDA passthrough removes the in-band path entirely, and that the GPU has **no RAPL equivalent** (the paper makes that contrast explicitly). Every threshold in POLCA is derived from those latencies, and the cap frequencies are A100 clock-domain constants.

verdict: `CORE_GPU`

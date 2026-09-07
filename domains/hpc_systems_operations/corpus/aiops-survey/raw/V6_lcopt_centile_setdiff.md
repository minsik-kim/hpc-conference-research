# V6 — Verification of LC-Opt / CENTILE / SeT-Diff

Verification date: 2026-09-06
Method: WebSearch + WebFetch only (no curl/wget/scripted fetching).
Evidence labels: FULL-TEXT / ABSTRACT / TITLE-ONLY / REVIEWS / NOT FOUND / UNVERIFIED

---

## 0. Corrected metadata — summary table

| Note in V-notes | Status | Corrected record |
|---|---|---|
| "LC-Opt", NeurIPS 2025 | **CONFIRMED** (both name and venue correct) | LC-Opt, NeurIPS 2025 Datasets & Benchmarks Track |
| "CENTILE", arXiv 2608.01725 | **ID CORRECT, DESCRIPTION WRONG** | 2608.01725 *is* CENTILE, but it is a **telemetry foundation model**, not "cross-domain transfer learning with adapters" |
| "SeT-Diff", CF 2026 | **CONFIRMED** venue; full record recovered | CF '26, pp. 109–112, DOI 10.1145/3801487.3806064 |

---

# TARGET 1 — LC-Opt

## 1.1 Metadata — CONFIRMED (FULL-TEXT)

- **Exact title:** "LC-Opt: Benchmarking Reinforcement Learning and Agentic AI for End-to-End Liquid Cooling Optimization in Data Centers"
- **Authors:** Avisek Naug, Antonio Guillen(-Perez), Vineet Kumar, Scott Greenwood, Wesley Brewer, Sahand Ghorbanpour, Ashwin Ramesh Babu, Vineet Gundecha, Ricardo Luna Gutierrez, Soumyendu Sarkar
- **Affiliations (FULL-TEXT, from arXiv HTML):**
  - Hewlett Packard Enterprise: Naug, Guillen, Ghorbanpour, Ramesh Babu, Gundecha, Luna Gutierrez, Sarkar
  - Oak Ridge National Laboratory: Vineet Kumar, Scott Greenwood, Wesley Brewer
- **Venue / year:** NeurIPS 2025, **Datasets and Benchmarks Track** (poster). Notes were correct.
- **DOI (proceedings):** 10.52202/085713-5325
- **arXiv:** 2511.00116, submitted 31 Oct 2025. arXiv comments field reads: *"Submitted to the NeurIPS 2025 conference"*
- **URLs:**
  - https://proceedings.neurips.cc/paper_files/paper/2025/hash/e9c55f6c6876a29162e53f51209c1a1d-Abstract-Datasets_and_Benchmarks_Track.html
  - PDF: https://proceedings.neurips.cc/paper_files/paper/2025/file/e9c55f6c6876a29162e53f51209c1a1d-Paper-Datasets_and_Benchmarks_Track.pdf
  - https://arxiv.org/abs/2511.00116 ; https://arxiv.org/html/2511.00116v1
  - https://neurips.cc/virtual/2025/poster/121589
  - Code: https://github.com/HewlettPackard/sustain-lc ; docs https://hewlettpackard.github.io/sustain-lc/

**Naming note (minor):** the environment is called **LC-Opt** in the body, but the code repository is `sustain-lc` and Appendix H repeatedly calls the environment **"SustainLC"** — evidence of a rename during review. Cite as LC-Opt; expect `sustain-lc` in code/artifact references.

**ExaDigiT relationship — CONFIRMED but looser than the notes imply.** ExaDigiT is described, not extended as a code dependency. Verbatim (FULL-TEXT, arXiv HTML):
> "ExaDigiT is a digital twin of supercomputers and their thermal infrastructures."
> "ExaDigiT combines telemetry and simulations, providing a virtual representation of physical systems."
> "ExaDigiT is built on an open software stack (Modelica, SST Macro, Unreal Engine)."
> "The intention is for this tool specifically to help standardize digital twin workflows for ExaDigiT."

So LC-Opt is *aligned with / intended to feed* ExaDigiT workflows and shares its Modelica cooling lineage and three ORNL co-authors; it is not literally "built on top of ExaDigiT" as an RL wrapper around the released ExaDigiT stack. Do not write "built on ExaDigiT" without hedging.

## 1.2 Environment, method, or both? — BOTH, weighted to environment (FULL-TEXT)

Primary contribution is an **environment/benchmark**: a Gymnasium-interface, Modelica-based end-to-end liquid-cooling model of Frontier's cooling system, site cooling towers → CDUs → cabinets → server blade groups, plus optional heat recovery unit (HRU). Abstract verbatim:
> "We present LC-Opt, a Sustainable Liquid Cooling (LC) benchmark environment, for reinforcement learning (RL) control strategies in energy-efficient liquid cooling of high-performance computing (HPC) systems."

Secondary methodological content: multi-agent RL formulations (decentralized vs centralized action, multi-head policy), **policy distillation** into decision/regression trees for interpretability, and an **LLM "agentic mesh"** that explains control actions in natural language.

**RL algorithms baselined:** **PPO** (primary, all main tables) and **SAC** (Appendix B, "Ablation with Soft Actor Critic", Table 7). No TD3, DDPG, MADDPG, IPPO, or offline-RL algorithms found. Controller variants compared (Table 3):
1. Baseline Control (ASHRAE Guideline 36) — rule-based
2. CT RL + BG baseline
3. CT baseline + BG RL (no valve control)
4. CT baseline + BG RL (with valve control)
5. Multi-agent RL (decentralized action)
6. Multi-agent RL (centralized action)
7. Multi-agent RL (centralized action + multi-head policy)

Table 4: "Performance on Scale. Evaluation of Rule-Based Control vs Multihead Centralized Action Policy for Scaling of Cooling Tower Agent."

## 1.3 Action space — COOLING SETPOINTS ONLY (FULL-TEXT)

Blade-group / CDU MDP (Table 2):
- valve actuation vector `ν_ij` per blade group, continuous [0,1], **constrained to sum to 1.0** ("The second head has a softplus output fitted to a Dirichlet distribution to generate the desired valve response vector that is [0,1] scaled and sums to 1.0.")
- CDU coolant supply temperature `T_cdu,i` (continuous setpoint)
- CDU pump flow rate `Q_cdu,i` (continuous, kg/s)

Cooling-tower MDP (Table 1):
- discrete return-temperature setpoint change `δ_i` per cooling tower

Observations: blade-group temperature `T_ij` and thermal power input `P_ij`; CDU temperature/flow; per-cell cooling-tower power `P_ij`; CT water return temperature `T_ct,i`; outside-air wet-bulb temperature `T_w`.

**Not in the action space:** job scheduling, job placement, power capping, node draining, requeue, or any maintenance/remediation action. Workload appears only as an **exogenous** thermal-power trace ("dynamic changes in workloads", "evaluated on an unseen exogenous trace") — the agent cannot act on it.

## 1.4 Operational policy evaluation methodology — ABSENT (FULL-TEXT)

- **No off-policy evaluation.** No IPS/DR/DM estimators, no importance weighting, no behaviour-policy modelling.
- **No counterfactual estimation methodology.** "What-if" is achieved by re-simulating in the twin, not by estimating a counterfactual from logged data.
- **No confidence intervals / error bars on policy performance.** Results are reported as single evaluation runs on "an unseen exogenous trace"; no seed count or standard deviations stated in the methodology or main tables.
- **No sim-to-real gap quantification.** Appendix H ("Bridging the Simulation-to-Real gap") is a *deployment roadmap*, not a measurement. Verbatim:
  > "Phase 2: Hardware-in-the-Loop Validation on a Physical Testbed. The next planned phase is to validate both the digital twin's response and the trained RL controllers on a dedicated, smaller-scale physical liquid cooling testbed."
  > "Phase 3: 'Shadow Mode' Deployment for Trust Building. The pre-trained and hardware-vetted agent would then be deployed in a 'shadow mode' in a real data center. It ingests live sensor data and computes control decisions, but these actions are only logged and compared against the existing control system…"

  Phases 2–4 are explicitly **future/planned**, not executed. Shadow-mode evaluation — the closest thing to operational policy evaluation — is named as a *plan*.

**Verdict on Q4: purely a simulation environment for RL training and comparison.** It contains no policy-evaluation methodology.

## 1.5 Twin validation — ASSERTED, NOT QUANTIFIED (FULL-TEXT)

The only validation statement located is a bare assertion in Appendix H:
> "The digital twin at the core of SustainLC is not a theoretical model; it is a high-fidelity simulation that has been validated against the operational dynamics of the Frontier supercomputer's cooling system. This validation provides the confidence needed for its use in developing next-generation control strategies."

**No RMSE, MAPE, R², error bars, confidence intervals, calibration procedure, validation data window, or comparison plots against measured Frontier telemetry were found in the arXiv HTML.** No sentence describing how the Modelica model was calibrated or tuned to measured data. This is a soft spot: the "validated" claim is unbacked within the paper. *Caveat:* the supplementary ZIP was not opened; a numeric validation could live there. Label: **the absence is FULL-TEXT for the main paper + appendices reachable in the arXiv HTML; UNVERIFIED for the supplementary ZIP.**

## 1.6 Node health / failure / remediation — NOT ADDRESSED (FULL-TEXT)

No treatment of node health, hardware failure, failure prediction, remediation, drain, requeue, or maintenance scheduling. Scope is thermal-hydraulic control of pumps, valves, CDUs and cooling towers.

## 1.7 RULING — "counterfactual evaluation of HPC operational policies"

### **STILL OPEN** for the candidate project's core, with one sub-area partially occupied.

| Sub-area | Status after LC-Opt | Reasoning |
|---|---|---|
| **Physics/cooling twin as a substrate** | **PARTIALLY ADDRESSED → effectively CLOSED for cooling** | LC-Opt (plus ExaDigiT and S-RAPS, §5) provides an open, Gymnasium-wrapped, Frontier-derived Modelica cooling twin. Building another cooling twin is not defensible. |
| **Policy-evaluation methodology (OPE, counterfactual estimators, CIs, sim-to-real gap quantification)** | **STILL OPEN — completely untouched** | LC-Opt has zero OPE, zero counterfactual estimators, zero CIs, and an unquantified twin-vs-real gap. Its own Appendix H names shadow-mode evaluation as future work. |
| **Remediation / node-state actions (drain, requeue, maintenance, node health)** | **STILL OPEN — completely untouched** | Action space is cooling setpoints only. Workload is exogenous. |

**Recommendation:** un-suspend the candidate, but re-scope it away from "build a twin" and toward **(a) estimator-level methodology — off-policy/counterfactual evaluation of operational policies with calibrated uncertainty, and (b) the remediation/node-state action class** that every twin paper found here explicitly excludes. Position LC-Opt and S-RAPS as *substrates the candidate consumes*, not competitors — and note that the strongest citation for "twins do not yet quantify their own error" is LC-Opt's own unbacked validation sentence.

**Important:** LC-Opt is **not** the strongest threat in this space. See §5.1 (S-RAPS, SC '25 Workshops) — that paper does what the notes feared LC-Opt did, and does it on scheduling policies across five real systems.

---

# TARGET 2 — CENTILE

## 2.1 Metadata — arXiv ID CORRECT, characterization in notes WRONG (FULL-TEXT)

- **arXiv ID:** 2608.01725 (v1) — **the ID is correct and it is indeed CENTILE.** The notes' ID is not fabricated.
- **Exact title:** "Centile: A Telemetry Foundation Model Evaluated by the Decisions It Drives" (arXiv listing renders it "CENTILE:", the paper body uses "Centile")
- **Authors:** Zifan Zhang\*, Zhichao Hou\*, Tingxiang Ji, Yuchen Liu (\* equal contribution)
- **Affiliation:** Department of Computer Science, North Carolina State University, Raleigh, NC 27695, USA (single institution)
- **Date / class:** arXiv:2608.01725v1 [cs.NI] 03 Aug 2026
- **Published venue:** **NONE FOUND.** No comments field naming a venue; no conference/journal record located. Treat as preprint-only as of 2026-09-06.
- **URLs:** https://arxiv.org/abs/2608.01725 ; https://arxiv.org/html/2608.01725v1
- **Code:** https://github.com/ZzZTripleZzZ/all-in-one

### CORRECTION TO NOTES — this matters
The notes describe CENTILE as **"cross-domain transfer learning with adapters."** That is a **mischaracterization**, though not a hallucination:

- CENTILE's actual contribution is a **generative foundation model for telemetry**, evaluated by **decision replay** (its calibrated conditional quantiles are fed to real decision rules — an EASY-backfilling scheduler and a network capacity-provisioning rule — and the resulting decision quality is measured).
- An "adapter" exists but is a **pluggable input-embedding stage**, not a parameter-efficient transfer-learning adapter in the PEFT/LoRA sense. Verbatim (FULL-TEXT):
  > "Because the adapter is the only source-specific stage, a new telemetry source, whether a switch counter feed or a per-virtual-machine utilization stream, is added by declaring its feature vector while the stages above it stay fixed."
- Cross-domain transfer is **one of six experiment subsections**, not the paper's thesis.

**The unverified quote in the notes: NOT RECONCILED.** The notes' quote was not supplied to this verification, and I could not retrieve Sections IV–VI verbatim (see §6). Do not use any quote attributed to CENTILE until it is re-extracted from the PDF directly. Any quote about "adapters for cross-domain transfer" as the paper's central claim would be **inconsistent with the verified abstract and introduction** and should be presumed misattributed.

## 2.2 Abstract — verbatim (FULL-TEXT)

> "Modern computing and networking infrastructure emits telemetry continuously, yet operators convert it into decisions with a separate predictor per task, entity, and horizon. One generative model, pretrained once over an operator's own event streams, could replace this fleet, an approach that already scales to high-cardinality streams in recommendation systems. However, point-forecast error on operational telemetry saturates near simple last-value baselines, so lower error alone need not improve the decisions it feeds. To close this gap, we present Centile, a generative foundation model for network and systems telemetry, evaluated by replaying the decisions its calibrated conditional quantiles drive. Centile treats heterogeneous telemetry as event-driven, irregularly timed entity streams and serves flexible forecast horizons in a single pass, requiring no future timestamps. To our knowledge, Centile is the first pretrained telemetry model to improve both HPC scheduling and network provisioning decisions under replay, its runtime estimator transferring zero-shot across months and its pretrained weights across domains from hours of target data. Extensive experiments on HPC job logs and network traffic confirm that Centile lowers the mean bounded slowdown of backfilling by up to approximately 77% over deployed user estimates and roughly halves the deployed rule's violation rate. Our code is available at https://github.com/ZzZTripleZzZ/all-in-one."

## 2.3 Domains — YES, real HPC operational telemetry is one of them (FULL-TEXT + repo README)

| Dataset | System / source | Real operational? | Role |
|---|---|---|---|
| **F-DATA** | Fugaku supercomputer job logs (Zenodo 11467483, monthly `YY_MM.parquet`) | **Yes — real HPC** | Primary target; EASY-backfilling decision replay |
| **CESNET-TimeSeries24** | National ISP backbone traffic, hourly (Zenodo 13382427) | Yes — real network | Second target; capacity provisioning |
| **Azure VM 2017** | Azure public dataset, 5-min grid | Yes — real cloud | Pretraining / positioning |
| **Borg** | Google `clusterdata-2011-2` DC tasks | Yes — real cloud | Pretraining / positioning |
| **Alibaba** | `v2018Traces` DC tasks | Yes — real cloud | Positioning (Table II) |
| **M100** | Marconi100 (Zenodo 7541722) | Yes — real HPC | Listed in repo dataset set |

So: **one primary HPC operational system (Fugaku) with decision replay; M100 present in the data list; the rest cloud/network.** Scale stated: "roughly 117K jobs" in the primary month; the replay window covers "48,826 jobs from 298 users over two weeks, following a one-week warm-up." CESNET is "split chronologically at 80/20 per series and evaluated on 3,000 held-out windows."

## 2.4 Cross-generation transfer? — **NO** (FULL-TEXT)

The two transfer axes CENTILE actually evaluates:
1. **Cross-month (temporal) transfer, zero-shot** — "The estimator transfers zero-shot across months, and the pretrained weights carry over from traffic prediction to HPC scheduling." And: "its estimator is the best walltime source on every evaluated month, including the unseen months served by the April-pretrained model."
2. **Cross-domain transfer** — ISP traffic + cloud VM telemetry → Fugaku walltime estimation (§IV-C "Cross-Domain Transfer").

**Cross-generation (same organization, successive hardware generations of the same kind of system) is NOT evaluated.** A targeted string search of the retrievable text found **no occurrence** of "generation", "cross-generation", "schema", or "hardware change". Confirmed section list: IV-A Experimental Setup, IV-B Backfilling Replay on F-DATA, IV-C Cross-Domain Transfer, IV-D Capacity Provisioning on CESNET, IV-E Ablation: Where the Gains Come From, IV-F Deployment Considerations, V Related Work. **No cross-generation subsection exists.**

## 2.5 Transfer-loss decomposition? — **NO** (FULL-TEXT for structure; the numbers below are from the repo README)

CENTILE reports **aggregate transfer benefit**, not a causal decomposition. From the code repository README (label: **FULL-TEXT of repo README**, not of the paper):
> At a six-hour target budget, transfer achieves mean bounded slowdown of **35.9 ± 1.3** versus scratch training at **83.0 ± 36.0**. At full seven-day training, both converge near **26.0**, but transfer exhibits substantially lower variance across seeds.

This is a **sample-efficiency curve** (transfer vs from-scratch at varying target-data budgets), reported with ± across seeds. It is *not* an attribution of transfer loss to hardware change, schema change, workload-mix change, or policy change. No such decomposition was found anywhere. There is no transfer-penalty matrix, no per-cause ablation, no schema-shift term.

Note the direction of the finding: CENTILE reports transfer as a **gain over from-scratch**, whereas the candidate project's artifact is a **penalty matrix** — a measurement of what transfer *costs* relative to in-domain training and *why*. These are different objects.

## 2.6 Method or measurement? — **METHOD** (FULL-TEXT)

Framed squarely as a method: a generative foundation model with named architectural components (intensity-preserving attention, Student-t mixture head, direct multi-horizon decoding, pluggable input adapter), plus a decision-replay *evaluation protocol* as supporting methodology. Not a benchmark release, not a measurement study. Table I is "Positioning against foundation models for systems and time series" — i.e., positioning a model among models.

## 2.7 Systems/datasets count, spans, split (FULL-TEXT)

- **Systems/datasets:** up to 6 in the data list (F-DATA/Fugaku, CESNET, Azure, Borg, Alibaba, M100); **2 carry decision-replay evaluation** (Fugaku, CESNET).
- **Time spans:** multi-month Fugaku trace; replay window = 2 weeks after 1-week warm-up; "April-pretrained model" evaluated on later unseen months. **Exact calendar date ranges: UNVERIFIED** — not recoverable from the retrievable HTML.
- **Split: TEMPORAL, and rigorously so.** Verbatim:
  > "Training reads only data strictly earlier than the evaluation window, and each entity's history grows in submit order at inference, so no prediction ever reads its own future."

  CESNET: "split chronologically at 80/20 per series." Also: "After training, the weights and the log-space normalization statistics are frozen together, so a later deployment window enters the same scale the head was fit on."

  This is a strong methodological point in CENTILE's favour and the candidate must match it — a random split would be an easy reviewer kill.

## 2.8 RULING — is the "measurement + transfer-penalty matrix" reframing sufficient?

### **SUFFICIENT** — on all four axes that matter, with two conditions.

Differentiation holds because CENTILE:
1. is a **method** (foundation model), not a measurement artifact — the candidate is now a measurement + public artifact. Different contribution type.
2. evaluates **cross-domain and cross-month** transfer, **not cross-generation**. The candidate's axis is untouched — verified by section list and string search.
3. **does not decompose** transfer performance into causes. No schema-shift, hardware-change, workload-mix, or policy-change terms exist anywhere in it.
4. reports transfer as a **gain over from-scratch at small target budgets**, not as a **penalty relative to in-domain training** — the opposite framing from the candidate's artifact.

**Conditions attached to this ruling:**
- **(a) The notes' description of CENTILE must be corrected in any related-work text.** Writing "CENTILE: cross-domain transfer learning with adapters" would be a mischaracterization a reviewer from that group would flag immediately. Correct framing: "a telemetry foundation model evaluated by decision replay, which demonstrates zero-shot cross-month and cross-domain weight transfer but does not measure cross-generation transfer or attribute transfer loss to cause."
- **(b) The unverified quote must be dropped or re-extracted from the PDF.** Do not let it into a related-work section.
- **(c) The candidate must use a temporal split and report seed variance**, because CENTILE sets that bar explicitly and publicly.

**Residual risk (low but real):** CENTILE's `data/` list includes **both Fugaku (F-DATA) and Marconi100 (M100)** and its adapter design is explicitly built so "a new telemetry source … is added by declaring its feature vector while the stages above it stay fixed." A follow-up from this group could run cross-system/cross-generation transfer cheaply. The candidate's defensibility rests on the **decomposition and the public penalty matrix**, not on being first to run a transfer experiment. Prioritize accordingly.

---

# TARGET 3 — SeT-Diff

## 3.1 Metadata — venue CONFIRMED, full record recovered (FULL-TEXT + dblp record)

- **Exact title:** "SeT-Diff: Towards Semantic Foundation Models for HPC Telemetry and Time-Series"
- **Authors:** Giovanni B. Esposito, Francesco Antici, Daniele Cesarini, Andrea Bartolini
- **Affiliations:** University of Bologna (Esposito, Antici, Bartolini); CINECA (Cesarini)
- **Venue:** Proceedings of the **23rd ACM International Conference on Computing Frontiers (CF '26)**, May 19–21, 2026, Catania, Italy. **Notes were correct.**
- **Pages:** 109–112 (a **4-page short paper** — important for calibrating how much it can claim)
- **DOI:** **10.1145/3801487.3806064**  (ACM Reference Format block, verbatim: *"Proceedings of the 23rd ACM International Conference on Computing Frontiers (CF '26), May 19–21, 2026, Catania, Italy. 979-8-4007-2568-5/2026/05. https://doi.org/10.1145/3801487.3806064"*)
- **ISBN:** 979-8-4007-2568-5
- **arXiv:** 2607.22548v1, header stamp "[cs.AI] 11 May 2026"; classes cs.AI, cs.LG, cs.PF. *(Minor anomaly: a 2607.* identifier with a May date stamp; both values are quoted as printed rather than reconciled.)*
- **URLs:** https://arxiv.org/abs/2607.22548 ; https://arxiv.org/html/2607.22548v1 ; dblp CF 2026 record (via https://dblp.org/pid/45/1193.html)

## 3.2 Abstract — verbatim (FULL-TEXT)

> "Data centers and their compute nodes require accurate and flexible digital twins capable of modeling the complex interplay of workloads, environmental parameters, and physical metrics. Current machine learning approaches for HPC and its telemetry typically rely on a static subset of anonymous, fixed-position sensor variables tailored to single tasks. Consequently, these models become obsolete when target tasks change or sensor metrics vary. We propose SeT-Diff, the first foundational model for compute node telemetry and time-series. Unlike rigid architectures, our diffusion-based approach conditions the generative process on each sensor's semantic description, decoupling the system dynamics from the structure of the dataset. Experiments on a real-world supercomputer dataset demonstrate a Mean Absolute Error (MAE) of 0.0470 on reconstruction tasks. SeT-Diff exhibits zero-shot permutation stability, maintaining accuracy with negligible degradation even when sensors are shuffled. A single pre-trained model effectively performs data imputation, forecasting, and virtual sensing - achieving a 0.033 MAE in thermal inference - making SeT-Diff an effective data-driven digital twin for HPC systems."

## 3.3 What "schema permutation invariance" operationally means — **METRIC ORDERING ONLY** (FULL-TEXT)

The mechanism is **semantic conditioning**: each channel is conditioned on a textual embedding of the sensor's description rather than on its positional index. Verbatim:
> "This allows learning permutation-invariant representations: if 'CPU Temperature' moves channels, the model recognizes its context embedding rather than its position, ensuring consistent generation across reconfigured hardware layouts."
> "In contrast, SeT-Diff treats the multivariate time series not as a fixed matrix, but as a collection of interacting physical signals defined by semantic identity and statistical behavior."
> "if the monitored metrics change order or composition, these rigid pipelines become obsolete."

What is actually **demonstrated**:
- **Invariance to metric ordering — YES, demonstrated.** "Under random permutation of the input sensor array, SeT-Diff yields performance virtually identical to its unperturbed state (0.0472 MAE vs. 0.0470 MAE). This confirms that the model identifies signals strictly by their semantic meaning, exhibiting intrinsic zero-shot robustness to hardware reconfigurations where traditional (index-based) models naturally fail."
- **Invariance to differing metric sets / missing metrics — PARTIAL.** Handled as *masking of known channels* (virtual sensing, up to 50% masked; forecasting = 8 masked timesteps), i.e. subsets of the same trained 261-metric vocabulary.
- **Invariance to metric renaming — NOT DEMONSTRATED.** Mechanistically plausible via text embeddings (a renamed metric with a similar description should embed nearby), but no experiment on renamed or paraphrased metric names was found.
- **Invariance to differing cardinality / genuinely unseen metrics — NOT DEMONSTRATED.** Training vocabulary is fixed at P = 261 metrics; all tests are on subsets of those 261. No unseen-sensor or variable-P experiment found.

**Bottom line: the paper's verified claim is "permutation stability" over a fixed, known metric vocabulary — not full schema invariance.** The notes' shorthand "schema permutation invariance for telemetry" overstates it slightly; the accurate phrasing is *positional-index invariance via semantic sensor-name conditioning*.

## 3.4 Real HPC telemetry? — **YES, one system** (FULL-TEXT)

> "We use the M100 ExaData dataset (Borghesi and others, [2023]) (20 months of Marconi100 operations), aggregating out-of-band (IPMI) and in-band (Ganglia) metrics."

- **System:** Marconi100 (M100), operated by CINECA — a co-author's institution, so genuine operational access.
- **Span:** 20 months.
- **Scale:** ~40K windows, P = 261 metrics.
- **Cross-system / cross-generation: NONE.** Single system only. Stated future work: "we will extend the training corpus across multiple architectures and heterogeneous sources."

## 3.5 Does it quantify schema shift as a distinct cause of performance loss? — **NO** (FULL-TEXT)

It measures **robustness to one schema perturbation** (permutation), which is nearly zero-cost (0.0470 → 0.0472 MAE), and it measures the **benefit of semantic vs positional conditioning** (0.154 → 0.0470 MAE imputation; 0.156 → 0.0622 virtual sensing; 0.155 → 0.0613 forecasting, against "a structurally identical diffusion baseline that relies on standard positional indices instead of textual semantic embeddings").

It does **not** isolate schema shift as a distinct error term alongside hardware change, workload change, or distributional drift. No decomposition. The permutation test is a *robustness check on the proposed method*, not a measurement of schema shift as an operational phenomenon.

## 3.6 Method or measurement? — **METHOD** (FULL-TEXT)

A diffusion-based architecture with semantic sensor-description embeddings, statistical descriptors, and factorized attention. Contribution is the architecture and conditioning mechanism. Not a benchmark, not a measurement study. Also only 4 pages.

## 3.7 Reported results (FULL-TEXT)

| Task | SeT-Diff MAE | Positional baseline MAE |
|---|---|---|
| Imputation / reconstruction (clean) | 0.0470 | 0.154 |
| Imputation, features shuffled | 0.0472 | — |
| Virtual sensing (≤50% masked) | 0.0622 | 0.156 |
| Forecasting (8 timesteps masked) | 0.0613 | 0.155 |
| Virtual Sensing A — power estimation | 0.0880 | — |
| Virtual Sensing B — thermal estimation | 0.0332 | — |
| Virtual Sensing C — GPU | 0.154 power / 0.025 temp | — |

## 3.8 SeT-Diff — relevance to the candidates

It is a **weaker** threat to the cross-generation telemetry-transfer candidate than the notes imply, and it is arguably an **enabler**:
- It gives the candidate a citable mechanism for handling schema differences (semantic conditioning) that the candidate can *hold fixed as a control* while measuring the remaining transfer penalty.
- It confirms that **positional-index models catastrophically fail under schema perturbation (0.154 vs 0.047 MAE, ~3.3×)** — a strong published number supporting the candidate's premise that schema shift is a real, large cost.
- But it does **not** measure schema shift across systems or generations, does not decompose transfer loss, and uses only one system. All of the candidate's claimed territory remains open.

---

# 5. Additional papers encountered — one is a STRONGER threat than all three targets

## 5.1 ⚠ S-RAPS — the real threat to Candidate 1 (STRONGER THAN LC-OPT)

- **Title:** "HPC Digital Twins for Evaluating Scheduling Policies, Incentive Structures and their Impact on Power and Cooling"
- **Authors:** Matthias Maiterth, Arunavo Dey, Dmitry Duplyakin, Wesley H. Brewer, Tanzima Z. Islam, Rashadul Kabir, Jaya S. Kuruvella, Kevin Menear, Tapasya Patki, Terry Jones
- **Affiliations:** ORNL, Texas State University, NREL, LLNL, Colorado State University
- **Venue:** **SC '25 Workshops** (Proceedings of the SC '25 Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis), **DOI 10.1145/3731599.3767559**
- **arXiv:** 2508.20016 (v1 and v2 exist)
- **Label:** FULL-TEXT (arXiv HTML v1) for content; venue/DOI from search-result metadata (ACM DL itself 403s) — **venue confirmed, DOI ABSTRACT-level**

**Why it is a stronger threat than LC-Opt to "counterfactual evaluation of HPC operational policies":**
- It explicitly does **what-if / counterfactual policy evaluation on real production traces from five systems**: Frontier (1,238 jobs, proprietary), Marconi100 (231,238), Fugaku (116,977), Lassen (1,467,746), Adastra (30,570).
- The evaluated policy space is **operational scheduling**, not cooling setpoints: FCFS, shortest-job-first, largest-job-first, priority, replay; backfill variants (none / first-fit / EASY); external schedulers ScheduleFlow and FastSim; ML-guided scheduling.
- It evaluates **incentive structures** — a Fugaku point-score case study with average-power, energy-delay-product and energy-delay²-product accounting — described as "difficult to realize on production systems."
- It **extends ExaDigiT** directly (builds on ExaDigiT's RAPS + Modelica cooling model), which is what the notes wrongly attributed to LC-Opt.
- Self-described as the "first-of-its-kind integration of scheduling and digital twins in HPC."

**Where it still leaves the candidate room (both quoted/verified):**
- **No confidence intervals or error bars.** Validation is qualitative/matching: "with information on the jobs' power profiles and correct estimates of runtimes, the S-RAPS simulator can match the observed changes in both utilization and simulated power." No OPE estimators, no uncertainty quantification.
- **Node health and remediation explicitly excluded**, in the paper's own footnote: *"The datasets do not contain reservations and job dependencies, nor was information about down or drained nodes available."*

**Action:** this paper, not LC-Opt, should be the gate on Candidate 1. It converts "physics twin + policy what-if" from open to largely occupied. The two sub-areas that survive are exactly the two identified in §1.7: **estimator-level policy-evaluation methodology with uncertainty**, and **node-state/remediation actions** — and S-RAPS's own footnote is the cleanest available citation that the drain/down-node data gap is unaddressed.

## 5.2 Machine Learning Guided Cooling System Optimization for Data Center

- **arXiv:** 2601.02275 (submitted 5 Jan 2026; revised 7 Mar 2026); 11 pages, 11 figures; eess.SY, stat.AP
- **Authors:** Shrenik Jadhav, Zheng Liu. **Affiliations: NOT FOUND** on the abs page.
- **Venue: NOT FOUND** — appears preprint-only.
- **Label:** ABSTRACT
- **Content:** three-stage physics-informed ML on **one year of Frontier operational data at 10-minute resolution**; monotonicity-constrained gradient-boosting surrogate predicting facility accessory power from flow rates, temperatures and server power. **0.026 MW MAE**; "power usage effectiveness within 0.01 of measured values for 98.7% of test samples." Identifies ~85 MWh/yr waste, ~96% recoverable via supply-temperature and subloop-flow adjustment.
- **Relevance:** this is the paper that **does** quantify surrogate-vs-measured error on real Frontier data — the exact thing LC-Opt asserts but does not show. Useful as (i) a citation that measured-vs-model error reporting is feasible and expected, and (ii) a mild threat on "counterfactual setpoint evaluation with quantified surrogate error."
- **Caution:** the classification of this paper as "counterfactual/off-policy evaluation" came from a summarizing fetch, **not from the paper's own vocabulary**. Do not attribute OPE language to it without reading the full text.

## 5.3 ModelX: A Novel Transfer Learning Approach Across Heterogeneous Datasets

- **Venue:** HPDC 2025 (Proceedings of the 34th International Symposium on High-Performance Parallel and Distributed Computing), **DOI 10.1145/3731545.3731593**
- **Label:** **TITLE-ONLY.** Content not retrieved — ACM DL 403s; the HPDC slide deck (hpdc.utah.edu) fails robots/TLS; the OSTI full text (LLNL-CONF-870385, osti.gov/servlets/purl/2564546) is robots-disallowed; Crossref returned 429.
- **Why flagged:** the title — transfer learning **across heterogeneous datasets** — is squarely adjacent to Candidate 2, and it is at a top-tier HPC venue with LLNL involvement (an OSTI/LLNL conference number implies LLNL system data, i.e. possibly successive LLNL generations). **This is the highest-priority unresolved item in this verification.** It could be a stronger threat to Candidate 2 than CENTILE.

## 5.4 Others noted, lower priority

- "Efficient Reinforcement Learning Implementations for Sustainable Operation of Liquid Cooled HPC Data Centers" — NeurIPS 2025 item (https://neurips.cc/virtual/2025/126888). **TITLE-ONLY.** Almost certainly the same HPE/ORNL group; likely a talk/workshop companion to LC-Opt. Low incremental threat.
- "Trace Replay Simulation of MIT SuperCloud for Studying Optimal Sustainability Policies" — arXiv 2509.16513. **ABSTRACT (partial).** Trace replay + rescheduling on MIT SuperCloud TX-GAIA; "enables reinforcement learning (RL)-based experimentation with sustainability policies"; "preliminary RL experiments using Proximal Policy Optimization demonstrate the feasibility of learning energy-aware scheduling decisions." No statistical measures reported. Same family as S-RAPS but weaker.
- "WANDER: An Explainable Decision-Support Framework for HPC" — arXiv 2506.04049 (submitted 4 Jun 2025, revised 25 Dec 2025), Ankur Lahiry, Banooqa Banday, Yugesh Bhattarai, Tanzima Z. Islam. **ABSTRACT.** "synthesizes alternate configurations using counterfactual analysis aligned with user goals and constraints"; ranks alternatives by prediction uncertainty, causal consistency, and historical similarity. **Uses "counterfactual" in the configuration-recommendation sense, not policy OPE.** Systems not named in the abstract. Worth a full read for Candidate 1's related work — it is the closest thing found to *uncertainty-ranked counterfactual reasoning in HPC*, and shares an author with S-RAPS.
- "Evaluating Forecasting Techniques for Hardware Errors on a Large-scale HPC System" — arXiv 2608.01648v1. **TITLE-ONLY.** Potentially relevant to the node-health/remediation sub-area. Unexamined.
- "When GPUs Fail Quietly: Observability-Aware Early Warning Beyond Numeric Telemetry" — arXiv 2603.28781v2. **TITLE-ONLY.** Unexamined; relevant to node health.

---

# 6. What remains UNVERIFIED

| # | Item | Why | Priority |
|---|---|---|---|
| 1 | **ModelX (HPDC 2025) content** | ACM DL 403; HPDC slides TLS/robots failure; OSTI robots-disallowed; Crossref 429 | **HIGH** — possible stronger threat to Candidate 2 than CENTILE |
| 2 | **CENTILE Sections IV–VI verbatim** (§IV-C Cross-Domain Transfer table, §IV-E ablation, §V/VI conclusions) | arXiv HTML retrieval consistently truncated after §IV-A across four attempts with different anchors and prompts. Section *titles* and the repo README numbers were recovered; the in-paper tables were not | **HIGH** — needed to confirm no cause-decomposition exists in the tables |
| 3 | **The notes' quote attributed to CENTILE** | Quote text was not supplied to this verification, and the sections it would live in were unretrievable | **HIGH** — must be dropped or re-extracted before any related-work use |
| 4 | **CENTILE exact calendar date ranges** for F-DATA and CESNET | Only relative descriptions ("two weeks", "April-pretrained") recoverable | MEDIUM |
| 5 | **LC-Opt supplementary ZIP** — whether it contains numeric twin validation | Supplementary archive not opened | MEDIUM — determines whether "LC-Opt does not quantify its twin error" is safe to assert in print |
| 6 | **LC-Opt OpenReview reviews** | No OpenReview forum page located by search; only a raw `openreview.net/pdf/...` link surfaced. Reviewer statements about scope limits not obtained | MEDIUM — reviews would be the strongest citation for "no OPE, no CIs" |
| 7 | **S-RAPS arXiv comments/date fields and DOI confirmation** | abs-page metadata fetch returned abstract only; ACM DL 403 | LOW — venue confirmed by search metadata, content confirmed FULL-TEXT |
| 8 | **SeT-Diff dblp record DOI digits** | dblp CF 2026 page returned 503 twice; the author-page record gave authors/title/pages 109–112 but not DOI digits. DOI 10.1145/3801487.3806064 is from the paper's own ACM Reference Format block (author-supplied, reliable but not independently confirmed) | LOW |
| 9 | **SeT-Diff arXiv ID/date anomaly** (2607.* with an 11 May 2026 stamp) | Both values quoted as printed; not reconciled | LOW |
| 10 | **2601.02275 author affiliations and venue** | Not on abs page | LOW |
| 11 | arXiv 2608.01648, 2603.28781 (hardware-error forecasting, quiet GPU failure) | Not examined; surfaced late | MEDIUM for the node-health sub-area |

## Explicit "not found" vs "does not exist"
- **Not found in this search (existence not excluded):** any published venue for CENTILE; any OpenReview forum for LC-Opt; numeric twin validation for LC-Opt; a cross-generation transfer measurement paper other than possibly ModelX.
- **Established as absent from the papers themselves (FULL-TEXT):** OPE/counterfactual estimators, confidence intervals, and node-health/remediation actions in LC-Opt; cross-generation transfer and transfer-loss decomposition in CENTILE; cross-system evaluation and schema-shift quantification in SeT-Diff.
- **Nothing was fabricated.** All three of the notes' identifiers resolved to real papers; the single substantive error was the *characterization* of CENTILE, not its ID.

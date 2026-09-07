# V4 — Falsification audit: Hindsight (NSDI'23) & TelemetrySuffBench (arXiv 2608.07899)

Audit date: 2026-09-06. Tools: WebSearch + WebFetch only.
Evidence labels: **FULL-TEXT** (read paper body/PDF) / **ABSTRACT** / **TITLE-ONLY** / **NOT FOUND** / **UNVERIFIED**.

Hypotheses under test:
- **H1** — downsampling telemetry degrades root-cause diagnosis faster than it degrades anomaly detection.
- **H1a** (novel core) — the mechanism is loss of *temporal ordering / inter-layer lag*, not loss of amplitude.

---

## 1. TARGET 1 — Hindsight

### Identification — **FULL-TEXT**, verified

- **Title:** "The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems"
- **Authors / affiliations:** Lei Zhang (Emory University *and* Princeton University); Zhiqiang Xie (Max Planck Institute for Software Systems); Vaastav Anand (MPI-SWS); Ymir Vigfusson (Emory University); Jonathan Mace (MPI-SWS)
- **Venue:** 20th USENIX Symposium on Networked Systems Design and Implementation (NSDI '23)
- **PDF:** https://www.usenix.org/system/files/nsdi23-zhang-lei.pdf
- **Landing page:** https://www.usenix.org/conference/nsdi23/presentation/zhang-lei
- **Preprint:** https://arxiv.org/abs/2202.05769 (also https://ar5iv.arxiv.org/html/2202.05769)
- **Mirror:** https://pure.mpg.de/rest/items/item_3477936_3/component/file_3513151/content

Abstract, verbatim fragments: *"Today's distributed tracing frameworks are ill-equipped to troubleshoot rare edge-case requests. The crux of the problem is a trade-off between specificity and overhead."* … Hindsight implements *"a retroactive sampling abstraction: instead of eagerly ingesting and processing traces, Hindsight lazily retrieves trace data only after symptoms of a problem are detected."*

### The seven questions

**Q1 — Decision variable: binary keep/discard, or resolution tiers?**
**BINARY. No resolution dimension.** — **FULL-TEXT**
A trigger causes retrieval of the *whole* trace slice: *"Each agent contacted will set aside its slice of data belonging to the traceId, and asynchronously send it to the backend collector."*
Decisive verbatim line against any partial-detail notion: *"Agents do this atomically at the granularity of a trace; there is no point in only dropping part of a trace."*
Note the axis Hindsight *does* move on: it decouples *generation* from *retention* — trace data is always generated at full detail (nanosecond tracepoints, >200 MB/s per node) and held in a local buffer; only the *retention* decision is deferred. So the "level of detail" is fixed at maximum and the only variable is keep-or-drop.

**Q2 — Retention as a function of data age?**
**Partially yes, but as LRU eviction, not tiering or coarsening.** — **FULL-TEXT**
There is an explicit age concept: *"to expire trace data for the least-recently-seen request. We call the implicit time duration between generating data and overwriting it the event horizon."*
Eviction policy: *"Agents will evict traces when the index exceeds a threshold of buffer pool capacity (default 80%) by removing the least-recently used untriggered traceId."*
Typical event horizon ≈ 1 minute at a 1 GB buffer pool; *"with a 100 MB buffer pool, coherence surpasses 90% with up to 3s delay."*
**There is no rollup, no downsampling, no progressive coarsening, no multi-tier storage.** Data is full-resolution then deleted. This is a cliff, not a gradient — which is exactly the design space H1 opens up.

**Q3 — Metrics or only traces/spans?**
**Traces/spans only. Metrics appear solely as trigger inputs, never as retained data.** — **FULL-TEXT**
*"Applications record trace data (e.g. events, spans) using Hindsight's tracepoint client API."*
Metrics feed the trigger predicate: *"PercentileTrigger(p): Clients call addSample(traceID, measurement). Trigger fires for measurements >percentile p."* The measurements themselves are not stored in the buffer pool.

**Q4 — Downstream diagnosis / root-cause quality evaluated?**
**NO.** — **FULL-TEXT**
Evaluation metrics are: coherent edge-case trace capture rate (%), network bandwidth (MB/s), end-to-end latency and throughput (req/s), per-tracepoint API overhead (ns), breadcrumb traversal time (ms), event horizon (delay tolerance). There is **no** measurement of whether captured traces actually resolved a diagnosis, and no MTTR or localization-accuracy metric.

**Q5 — Temporal ordering or lag information discussed?**
**Essentially no.** — **FULL-TEXT**
Timing appears only as systems-engineering latency: trigger propagation (*"in the majority of cases a machine should learn of a trigger within a matter of seconds or milliseconds"*) and breadcrumb traversal (~86 ms under overload). There is no treatment of ordering or lag as *diagnostic information*, and no analysis of lag effects on diagnosis accuracy.

**Q6 — Cost model?**
**Memory, network bandwidth, CPU. No storage-over-time / retention-cost model.** — **FULL-TEXT**
Reported: 7.9–8.6 ns per tracepoint; application latency impact *"<3.5%"* at 100% tracing with *">200 MB/s of trace data per node"*; 55 GB/s peak write throughput; network bandwidth 2.6 MB/s (Hindsight) vs 78 MB/s (tail-sampling); ~0.3 CPU cores per agent; default 1 GB buffer pool per agent.
The cost axis is **instantaneous** (bytes/s, cores, RAM), not **integrated over retention horizon**. No $/GB-month, no capacity-planning model.

**Q7 — Follow-on work adding a resolution dimension?**
**NOT FOUND.** — searched; see limits below.
Author pages and searches surfaced no follow-on adding granularity tiers. Jonathan Mace's 2023+ output includes Blueprint (SOSP 2023), Antipode (SOSP 2023), a qualitative interview study of distributed-tracing visualisation (IEEE TVCG 2023) — none introduce a resolution/level-of-detail axis. Adjacent trace-sampling work found: Sifter (Las Casas et al.), TraceMesh (https://arxiv.org/pdf/2406.06975), "Trace Sampling 2.0: Code Knowledge Enhanced Span-level Sampling for Distributed Tracing" (https://arxiv.org/html/2509.13852v1). **Trace Sampling 2.0 is span-level rather than trace-level and is the closest thing to a granularity dimension found — it is only TITLE/URL-verified here and should be read before the related-work section is finalized.** Note that even span-level selection is still keep/discard of discrete records, not resolution of a numeric time series. dblp record for Vaastav Anand (https://dblp.org/pid/228/5717.html) timed out twice — **UNVERIFIED** by that route.

### Ruling on the characterization

> *"Hindsight is the closest published work to treating retention as a decision variable, but it is traces and binary keep/discard rather than resolution."*

**VERIFIED — accurate as stated, and strengthened by the full text.** Hindsight does treat retention as a deferred decision variable (its central contribution), and the decision is unambiguously binary and whole-trace, on traces/spans only, with metrics used merely as trigger predicates. The paper's own sentence *"there is no point in only dropping part of a trace"* is a direct, quotable disclaimer of the resolution axis. One refinement worth making in the write-up: Hindsight's cost axis is instantaneous overhead, not storage-over-time, and it never evaluates diagnosis quality — so it leaves *both* of H1's dependent variables (diagnosis quality) and cost framings (integrated retention cost) untouched.

---

## 2. TARGET 2 — TelemetrySuffBench

### Identification — **ABSTRACT + FULL-TEXT (HTML)**, verified twice

**The arXiv ID IS CORRECT.** arXiv 2608.07899 resolves to a paper actually named TelemetrySuffBench.

- **Title:** "TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?"
- **Authors:** Yuxuan Zhu, Peng Pu
- **Affiliations:** **NOT FOUND** — not surfaced on the abs page or in the HTML render I read. **UNVERIFIED.**
- **Submitted:** 8 August 2026
- **Comments field:** "10 pages, 3 figures, 4 tables"
- **Published venue:** none stated — **NOT FOUND** (arXiv preprint only, as of 2026-09-06)
- **abs:** https://arxiv.org/abs/2608.07899 · **HTML:** https://arxiv.org/html/2608.07899v1
- **Artifact:** https://anonymous.4open.science/r/TelemetrySuffBench-E635/README.md (anonymized link, i.e. likely under double-blind review somewhere)

**CRITICAL SCOPE FINDING:** this is **LLM-agent telemetry**, not HPC / infrastructure metrics. Its "traces" are agent execution steps (tool calls, handoffs, verifier events) in instrumented workflows, and its "models" are frontier LLMs used as diagnosticians. It is not a numeric-time-series paper at all.

Abstract, verbatim (from https://arxiv.org/abs/2608.07899):

> "Agent systems increasingly expose execution traces, yet telemetry that reveals a failure may still be inadequate for identifying where that failure originated. We introduce TelemetrySuffBench, a controlled benchmark that separates failure detection, fault-origin localization, and safe abstention under insufficient evidence. The benchmark constructs canonical multi-component traces with delayed-binding faults and renders them as paired coarse views, seven-factor telemetry masks, and exact-equal ambiguous origin pairs. We evaluate five frontier language models using unified protocols, explicit candidate sets, invalid-output accounting, subgroup analyses, and a frozen blind holdout. With full telemetry, origin-step Top-1 accuracy ranges from 33.8% to 97.2% across models. Metadata, OpenTelemetry-compatible, and OpenInference-compatible views retain 99.5% to 100% detection F1 while limiting origin-step accuracy to at most 0.5%, exposing a robust detection-localization gap. Factor ablations further show that removing decision content reduces origin-step accuracy to zero for every model, while provenance removal also causes large model-dependent losses. On rich ambiguous inputs that require abstention, evidence gating reduces unsupported unique-origin answers by 12.5 to 48.6 percentage points for three models, whereas two models still answer every case, revealing strong model dependence in safe abstention. Results on the frozen holdout reproduce the central pattern within the same generator family. These findings show that terminal status can support detection, whereas reliable causal attribution requires explicit decision-to-provenance links and abstention safeguards that remain effective across models. The dataset and benchmark implementation are available at https://anonymous.4open.science/r/TelemetrySuffBench-E635/README.md."

### The eight questions

**Q1 — ID, title, authors, date, venue.** See above. ID correct; venue none.

**Q2 — Synthetic, simulated, or real?**
**SYNTHETIC, deterministically generated.** — **FULL-TEXT**
*"TelemetrySuffBench is generated deterministically from instrumented, stateful workflows."*
Fault injection mechanism: *"To construct a fault, the generator injects a globally valid but task-inconsistent reference at a selected origin component while leaving the immediate concrete target unchanged."*
Scale: 312 canonical traces (96 clean, 216 fault, across 108 matched pairs), three domains (tickets, documents, orders), nine workflow components.
**No real operational telemetry.**

**Q3 — What exactly is varied?**
Two orthogonal axes, both **semantic field-set reduction**: — **FULL-TEXT**
*Six coarse views:* Full, Content-redacted, Metadata, Structural, OpenTelemetry-compatible, OpenInference-compatible.
*Seven telemetry masking factors (Table I):*
- **I** — identity and event semantics (actor identity, component type, tool name)
- **D** — decision and latent-reference content (symbolic reference, binding kind)
- **P** — registry and provenance mappings (reference registry, provenance documents)
- **R** — propagation and handoff relations (parent/dependency edges, memory links)
- **S** — tool inputs and state transitions (arguments, results, retrieval queries)
- **V** — observation and verifier evidence (expected/actual values)
- **T** — terminal failure status (event status, exception text)
Number of metrics, noise level and observation window are **not** the varied axes.

**Q4 — Does it vary temporal resolution?**
**NO.** — **FULL-TEXT, verified by two independent term-level passes over https://arxiv.org/html/2608.07899v1**
- "sampling" / "sampling rate" / "downsampl" / "frequency" / "timestamp" / "temporal" — **no occurrences** in the relevant sense (none at all for most).
- "resolution" — one occurrence, non-temporal (source-revision pinning).
- "interval" — one occurrence, "cluster-bootstrap intervals" (statistical CIs).
- "granularity" — appears as *"coarse- and fine-grained localization"*, i.e. diagnostic precision, not temporal granularity.
- **"coarse" in "paired coarse views" means semantically reduced field sets, NOT temporally coarsened.** This is the single most important disambiguation in this audit, and it was confirmed on a dedicated verification pass.

**Q5 — Does it analyze temporal ordering, lag, or cascade order as the mechanism?**
**NO.** — **FULL-TEXT**
"lag" — not found. "ordering" — not found. "order"/"sequence" appear as *"ordered event sequence"*, i.e. the logical/causal structure of the workflow, not as a manipulated or measured variable. No Granger causality, no cross-correlation lag, no cascade-order analysis.
The paper's own mechanism claim is **semantic, not temporal**: it defines five annotated causal stages — *"origin, activation, first visible deviation, symptom, and terminal"* — and attributes the localization failure to removal of **decision content** and **provenance mappings**. Verbatim from the abstract: *"reliable causal attribution requires explicit decision-to-provenance links."* That is a content-sufficiency mechanism (which field must be present), categorically different from H1a's timing mechanism (whether the sample interval preserves inter-layer lag).

**Q6 — Cost axis?**
**NO cost axis in the relevant sense.** — **FULL-TEXT**
No bytes, no token counts, no storage, no collection overhead, no retention cost is measured for the different telemetry views. The only monetary figure is experiment cost: *"Reproducing the complete experiment costs approximately US$2,400 in model API charges."* That is an evaluation expense, not a telemetry cost model.

**Q7 — Reported numbers, verbatim.**
From the abstract (https://arxiv.org/abs/2608.07899):
> "With full telemetry, origin-step Top-1 accuracy ranges from 33.8% to 97.2% across models."
> "Metadata, OpenTelemetry-compatible, and OpenInference-compatible views retain 99.5% to 100% detection F1 while limiting origin-step accuracy to at most 0.5%, exposing a robust detection-localization gap."
> "Factor ablations further show that removing decision content reduces origin-step accuracy to zero for every model, while provenance removal also causes large model-dependent losses."
> "evidence gating reduces unsupported unique-origin answers by 12.5 to 48.6 percentage points for three models"
From Table II (**FULL-TEXT**, via HTML render): full telemetry — detection F1 99.3%–100.0%; origin-step Top-1 33.8%–97.2%.

**CORRECTION TO THE SECOND-HAND NOTES.** The notes said "detection F1 of roughly 99.5–100% versus origin-step identification accuracy of ≤0.5%." Both numbers are real and verbatim, **but they do not describe the same condition as claimed.** The ≤0.5% origin accuracy holds *only under the restricted metadata/OTel/OpenInference views*. Under **full** telemetry, origin-step accuracy is **33.8%–97.2%** — up to 97.2%, i.e. localization is largely *solvable* when the right fields are present. Citing "99.5–100% detection vs ≤0.5% localization" as an unconditional finding would misrepresent the paper.

**Q8 — Baselines and models.**
Five frontier LLMs: GPT-5.5, GPT-5.6 Sol, DeepSeek-V4-Pro, Claude Opus 5, Qwen 3.7 Max. — **FULL-TEXT**
Protocol controls: unified prompting protocols, explicit candidate sets, invalid-output accounting, subgroup analyses, frozen blind holdout. There are no classical (non-LLM) RCA baselines.

### Rulings

**Does it damage H1? — PARTIAL.**
It independently corroborates the *existence and robustness* of a detection-vs-localization asymmetry, with strong numbers, in a controlled setting. That is real prior art for the *phenomenon*, and H1 can no longer be presented as an unexamined question — it must be positioned as "known qualitatively in agent traces; unquantified along the resolution axis in HPC metrics." But it does **not** damage the H1 *as stated*, because H1 is about **downsampling** (temporal resolution) and this paper varies **field masking** (semantic content) — a different independent variable, on a different data type (agent event traces vs numeric multi-layer time series), with no cost axis. Two of H1's three defining elements are absent.

**Does it kill H1a? — NO.**
Definitively not, and this is the audit's cleanest result. The paper contains no lag, no ordering manipulation, no temporal-resolution variation, and it advances a *competing* mechanism (missing decision-to-provenance links). H1a's mechanism is untouched by it. Two independent full-text term sweeps agree.

**Is the arXiv ID correct? — YES.** 2608.07899 = TelemetrySuffBench, exactly as the notes claimed. Title and general thesis check out; the *numbers* were mis-attributed across conditions (see Q7).

---

## 3. Causal discovery under subsampling / temporal aggregation — THE DECISIVE SECTION

This is where H1a is in real trouble. Two distinct literatures — econometrics (since 1971) and ML causal structure learning (since ~2013) — already establish that downsampling destroys lag-based causal identifiability.

### 3a. ML causal structure learning

**Mesochronal Structure Learning** — Plis, Danks, Yang. UAI 2015. https://www.auai.org/uai2015/proceedings/papers/302.pdf — **FULL-TEXT**
Affiliations: Plis & Yang (Mind Research Network & University of New Mexico); Danks (Dept. of Philosophy, CMU).
Abstract, verbatim: *"Standard time series structure learning algorithms assume that the measurement timescale is approximately the same as the timescale of the underlying (causal) system. In many scientific contexts, however, this assumption is violated: the measurement timescale can be substantially slower than the system timescale (so intermediate time series datapoints will be missing). This assumption violation can lead to significant learning errors."*
**The single most damaging quote found in this entire audit** — body text, verbatim: *"an apparent A → B connection at τM can be consistent with any possible connection at τS: A → B, A ← B, or no connection at all."*
That is H1a's mechanism — downsampling destroys the *direction and ordering* of inter-signal influence — stated explicitly in 2015. The algorithm outputs *"an equivalence class (possibly a singleton) of possible G₁"*; *"for densities up to 35%, the overwhelming majority of the equivalence classes are singletons"*, with classes growing at higher densities.

**Discovering Temporal Causal Relations from Subsampled Data** — Mingming Gong, Kun Zhang, Bernhard Schölkopf, Dacheng Tao, Philipp Geiger. ICML 2015 (PMLR v37). https://proceedings.mlr.press/v37/gongb15.html — **ABSTRACT (verbatim, full)**
> "Granger causal analysis has been an important tool for causal analysis for time series in various fields, including neuroscience and economics, and recently it has been extended to include instantaneous effects between the time series to explain the contemporaneous dependence in the residuals. In this paper, we assume that the time series at the true causal frequency follow the vector autoregressive model. We show that when the data resolution becomes lower due to subsampling, neither the original Granger causal analysis nor the extended one is able to discover the underlying causal relations. We then aim to answer the following question: can we estimate the temporal causal relations at the right causal frequency from the subsampled data? Traditionally this suffers from the identifiability problems: under the Gaussianity assumption of the data, the solutions are generally not unique. We prove that, however, if the noise terms are non-Gaussian, the underlying model for the high frequency data is identifiable from subsampled data under mild conditions. We then propose an Expectation-Maximization (EM) approach and a variational inference approach to recover temporal causal relations from such subsampled data. Experimental results on both simulated and real data are reported to illustrate the performance of the proposed approaches."

This paper is doubly consequential for H1a:
1. *"when the data resolution becomes lower due to subsampling, neither the original Granger causal analysis nor the extended one is able to discover the underlying causal relations"* — **H1a's claim, verbatim, from 2015.**
2. *"if the noise terms are non-Gaussian, the underlying model for the high frequency data is identifiable from subsampled data under mild conditions"* — a **partial refutation of H1a's inevitability**. The lag information is not irrecoverably destroyed; it is destroyed *for standard estimators* and recoverable by a non-Gaussian latent-variable estimator. Any H1a experiment that downsamples and then applies naive Granger/cross-correlation is measuring estimator fragility, not information loss, and a reviewer who knows this paper will say so.

**Rate-Agnostic (Causal) Structure Learning** — Sergey Plis, David Danks, Cynthia Freeman, Vince Calhoun. NIPS 2015. https://papers.nips.cc/paper/5689-rate-agnostic-causal-structure-learning — **ABSTRACT (verbatim, full)**
> "Causal structure learning from time series data is a major scientific challenge. Existing algorithms assume that measurements occur sufficiently quickly; more precisely, they assume that the system and measurement timescales are approximately equal. In many scientific domains, however, measurements occur at a significantly slower rate than the underlying system changes. Moreover, the size of the mismatch between timescales is often unknown. This paper provides three distinct causal structure learning algorithms, all of which discover all dynamic graphs that could explain the observed measurement data as arising from undersampling at some rate. That is, these algorithms all learn causal structure without assuming any particular relation between the measurement and system timescales; they are thus rate-agnostic. We apply these algorithms to data from simulations. The results provide insight into the challenge of undersampling."

**Causal Discovery from Subsampled Time Series Data by Constraint Optimization** — Antti Hyttinen (HIIT / Univ. Helsinki), Sergey Plis (Mind Research Network & Univ. New Mexico), Matti Järvisalo (HIIT / Univ. Helsinki), Frederick Eberhardt (Caltech), David Danks (CMU Philosophy). arXiv 1602.07970; PGM 2016 (PMLR); PubMed 28203316. https://www.arxiv.org/pdf/1602.07970 — **FULL-TEXT (partial)**
Abstract, verbatim: *"This paper focuses on causal structure estimation from time series data in which measurements are obtained at a coarser timescale than the causal timescale of the underlying system. Previous work has shown that such subsampling can lead to significant errors about the system's causal structure if not properly taken into account."*
Key underdetermination result, verbatim: *"the causal structure G₁ at the system timescale is in general underdetermined, even when the subsampling rate u is known and small."*
(Exact venue string — PGM 2016 vs journal-of-record — is **UNVERIFIED**; the PubMed record page would not render.)

**Causal Discovery from Temporally Aggregated Time Series** — Mingming Gong, Kun Zhang, Bernhard Schölkopf, Clark Glymour, Dacheng Tao. UAI 2017. https://www.auai.org/uai2017/proceedings/papers/269.pdf — **FULL-TEXT (partial)**
Covers *aggregation* (averaging/summing k consecutive observations) rather than *systematic sampling* — i.e. the "mean over a 60 s window" case, which is precisely what HPC telemetry rollup actually does, so this is the closest formal analogue to the H1 intervention.
Verbatim claims extracted: recovering high-frequency causality from aggregated data is *"a very hard problem due to information loss in the aggregation process"*; *"temporal aggregation can lead to errors in the estimated causal relations"*; Granger causal results *"heavily depend on temporal aggregation"*; and again the identifiability escape hatch — *"the causal structure at the causal frequency is identifiable from aggregated time series"* under independent non-Gaussian noise with known aggregation factor k. Aggregation turns a VAR into a VARMA, making estimation *"both statistically and computationally harder."*

**Causal Learning through Deliberate Undersampling** — Kseniya Solovyeva, David Danks, Mohammadsajad Abavisani, Sergey Plis. CLeaR 2023 (2nd Conference on Causal Learning and Reasoning), PMLR v213:1–13. https://openreview.net/pdf?id=vfUSpAFyEC — **ABSTRACT + partial FULL-TEXT**
**A direct counterexample to a monotone reading of H1a.** The paper shows *"we can gain additional information about the causal structure by measuring more slowly than our current instruments"* — certain graphs exhibit non-monotonic undersampling, where combining measurements at a slower rate coprime with the original rate *shrinks* the equivalence class of candidate causal structures. If H1a is phrased as "coarser resolution monotonically destroys lag/causal information," this paper refutes it in the general graph-theoretic setting.

**Related, TITLE/ABSTRACT-only:** Causal Discovery from Subsampled Time Series with Proxy Variables — Liu, Sun et al., https://arxiv.org/abs/2305.05276; Danks & Plis, "Learning Causal Structure from Undersampled Time Series," NIPS 2013 Causality Workshop (the origin paper of this line — **TITLE-ONLY**; PhilPapers and KiltHub both returned 403, Semantic Scholar returned no body).

### 3b. Econometrics — the same result, decades earlier

- **Breitung & Swanson (2002)**, "Temporal aggregation and spurious instantaneous causality in multiple time series models," *Journal of Time Series Analysis* — https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-9892.00284 — **TITLE-ONLY** (Wiley not fetched). The title alone states the mechanism.
- **Marcellino (1999)** — *"Marcellino shows that Granger non-causality is generally not invariant to temporal aggregation."* — **quoted at ABSTRACT/FULL-TEXT depth via** Rajaguru, O'Neill & Abeysinghe (2018), *Econometrics* 6(2):31, https://mdpi.com/2225-1146/6/2/31/htm
- **Sims (1971)** — *"Sims warns that aggregation could result in a spurious causal relationship."* — same source, same depth.
- **Wei (1982)** — *"Wei using Geweke linear decomposition demonstrates for the stationary variables that systematic sampling preserves the one-sided causal relationship."* — same source. Important nuance: for *stationary* series, plain systematic sampling can *preserve* causal direction.
- **Rajaguru, O'Neill & Abeysinghe (2018)**, "Does Systematic Sampling Preserve Granger Causality with an Application to High Frequency Financial Data?", *Econometrics* 6(2):31 — **FULL-TEXT (abstract + lit review)**. Abstract, verbatim: *"A number of studies document that temporal aggregation has distorting effects on causal inference and systematic sampling of stationary variables preserves the direction of causality. Contrary to the stationary case, this paper shows for the bivariate VAR(1) system that systematic sampling induces spurious bi-directional Granger causality among the variables if the uni-directional causality runs from a non-stationary series to either a stationary or a non-stationary series."*
- Secondary corroboration with a worked empirical example (oil → gasoline prices reversing direction under weekly/monthly aggregation) and a citation list (Sims 1971; Wei 1982; Christiano & Eichenbaum 1987; Marcellino 1999; Breitung & Swanson 2002; Gulasekaran & Abeysinghe 2002; Toda & Yamamoto 1995): https://davegiles.blogspot.com/2014/07/the-econometrics-of-temporal_16.html — **FULL-TEXT (blog, secondary)**

### Ruling on H1a

**H1a is NOT NOVEL as a general claim. Verdict: the general form is established prior art, ~55 years deep, in two literatures.**

Specifically, the following are already published and must not be claimed as contributions:
1. Downsampling/aggregation breaks Granger-style causal inference (Sims 1971 → Marcellino 1999 → Breitung & Swanson 2002 → Gong et al. ICML 2015).
2. The mechanism is loss of ordering/direction identifiability, not amplitude (Plis/Danks/Yang UAI 2015: *"an apparent A → B connection at τM can be consistent with any possible connection at τS: A → B, A ← B, or no connection at all."*).
3. The formal object is an equivalence class of system-timescale structures consistent with the coarse measurement (Plis et al. NIPS 2015; Hyttinen et al. 2016).

Worse than non-novelty, there are two **active threats** an informed reviewer will raise:
- **Recoverability.** Gong et al. (2015, 2017) prove lag structure *is* identifiable from subsampled/aggregated data under non-Gaussian noise. So "downsampling destroys lag information" is false as an information-theoretic statement; it is true only relative to a naive estimator. An H1a experiment must therefore either (a) use a subsampling-aware estimator as a baseline and show it still fails at operational resolutions, or (b) reframe the claim as being about *estimator-realizable* diagnosis under operational constraints.
- **Non-monotonicity.** Solovyeva et al. (CLeaR 2023) show coarser measurement can *increase* causal information. Any monotone "resolution ↓ ⇒ diagnosability ↓" curve claim is refutable in principle.

**What survives, and in what narrowed form.** The defensible residual contribution is *not* the mechanism but its **operational instantiation and quantification**:
- The asymmetry has never been measured on **real multi-layer HPC telemetry** (job/node/network/storage/power) with actual cross-layer fault cascades. The causal-discovery literature uses simulations, fMRI and economic series; TelemetrySuffBench uses synthetic agent traces.
- No one has coupled the identifiability loss to a **cost axis** — bytes/node/day, storage-over-time, $/GB-month. Hindsight's cost model is instantaneous overhead; TelemetrySuffBench has none; the causal-discovery literature has none at all. **The cost axis is the cleanest unclaimed ground in this whole audit.**
- No one has produced a **resolution-vs-diagnosability curve with an operating point** — i.e. "at what sampling interval does cross-layer cascade-order recovery collapse, and what does buying that resolution cost per node per year." That is an engineering-decision artifact the theory literature does not provide and does not want to provide.
- The **detection-vs-diagnosis asymmetry specifically as a function of temporal resolution** (as opposed to field masking) appears unmeasured — no paper found does this.

Recommended reframing: drop any claim to discovering the mechanism; cite Plis/Danks and Gong/Zhang as *the* established basis; position the contribution as **"the first cost-aware, real-telemetry quantification of the resolution threshold at which cross-layer cascade-order recovery collapses in HPC operations, and the resulting retention-policy design point."** Under that framing H1a becomes a *hypothesis inherited from theory and tested in a new regime with a new dependent variable* — which is a legitimate and defensible systems contribution, but it is not a novel mechanism claim.

---

## 4. Other near-neighbours

| Work | Where | Relation to H1 / H1a | Depth |
|---|---|---|---|
| Hindsight (Zhang et al.) | NSDI '23 | Retention as decision variable; binary keep/discard of traces; no resolution, no diagnosis metric, no storage-over-time | FULL-TEXT |
| TelemetrySuffBench (Zhu & Pu) | arXiv 2608.07899 | Detection-vs-localization asymmetry confirmed, but via semantic field masking on synthetic LLM-agent traces; no time resolution, no lag, no cost | FULL-TEXT |
| Plis, Danks, Yang — Mesochronal Structure Learning | UAI 2015 | **Closest to H1a.** Undersampling makes direction/ordering unidentifiable; explicit A→B / A←B / none collapse | FULL-TEXT |
| Gong, Zhang, Schölkopf, Tao, Geiger | ICML 2015 | Subsampling defeats Granger analysis; identifiable under non-Gaussian noise — both supports and threatens H1a | ABSTRACT (verbatim) |
| Gong, Zhang, Schölkopf, Glymour, Tao | UAI 2017 | Same for temporal *aggregation* (= HPC rollup); VAR→VARMA; identifiable under non-Gaussianity | FULL-TEXT (partial) |
| Plis, Danks, Freeman, Calhoun — Rate-Agnostic | NIPS 2015 | Learns all graphs consistent with undersampling at unknown rate; formalizes underdetermination | ABSTRACT (verbatim) |
| Hyttinen, Plis, Järvisalo, Eberhardt, Danks | arXiv 1602.07970 / PGM 2016 | System-timescale structure *"in general underdetermined, even when the subsampling rate u is known and small"* | FULL-TEXT (partial) |
| Solovyeva, Danks, Abavisani, Plis — Deliberate Undersampling | CLeaR 2023 | **Counterexample:** slower measurement can *add* causal information; refutes monotone H1a | ABSTRACT + partial |
| Rajaguru, O'Neill, Abeysinghe | Econometrics 6(2):31, 2018 | Systematic sampling induces spurious bi-directional Granger causality (non-stationary case); reviews Sims/Wei/Marcellino | FULL-TEXT |
| Breitung & Swanson | JTSA 2002 | Temporal aggregation ⇒ spurious instantaneous causality | TITLE-ONLY |
| Marcellino 1999; Sims 1971; Wei 1982 | econometrics | Granger non-causality not invariant to aggregation; aggregation ⇒ spurious causality; systematic sampling preserves direction for stationary vars | quoted via Rajaguru et al. 2018 |
| Liu, Sun et al. — Proxy Variables | arXiv 2305.05276 | Causal discovery from subsampled series via proxies | TITLE/ABSTRACT |
| Danks & Plis | NIPS 2013 Causality Wksp | Origin paper of the undersampling line | TITLE-ONLY (403s) |
| Trace Sampling 2.0 | arXiv 2509.13852 | Span-level (not trace-level) sampling — closest thing to a granularity axis in tracing | TITLE-ONLY |
| TraceMesh | arXiv 2406.06975 | Streaming trace sampling; still keep/discard | TITLE-ONLY |
| Sifter (Las Casas et al.) | SoCC 2019 | Trace sampling without feature engineering; keep/discard | TITLE-ONLY |
| Mai et al. — Impact of Packet Sampling on Anomaly Detection Metrics | IMC 2006 (via IEEE 4086338) | Sampling-rate effect on **detection only**; no diagnosis arm — the asymmetry is exactly what it does not test | TITLE-ONLY |
| FDI / model-based diagnosis: detectability vs isolability; sensor placement under budget | control-theory literature | **Structural analogue of H1 + cost axis, decades old.** Detectability≠isolability is textbook; sensor placement for isolability under budget constraints exists | TITLE-ONLY |

**Flag on the last row:** the fault-detection-and-isolation literature's *detectability vs isolability* distinction is essentially H1 in control-theoretic dress, and "sensor placement for fault diagnosis performance maximization under budgetary constraints" is the cost axis. This was surfaced only by search-result titles and **must be read properly before H1 is framed as novel.** It is the second-biggest unexamined threat after the causal-discovery line.

---

## 5. What remains unverified

1. **TelemetrySuffBench author affiliations** — not surfaced on abs page or HTML render. NOT FOUND.
2. **TelemetrySuffBench peer-review status** — anonymous.4open.science artifact link implies an active double-blind submission; venue unknown.
3. **Table III–IV of TelemetrySuffBench** (per-factor ablation detail) — not read line-by-line; the seven-factor list and headline numbers are verified, the per-model per-factor cells are not.
4. **Hindsight follow-on work** — dblp record https://dblp.org/pid/228/5717.html timed out twice; forward-citation sweep was search-based, not a systematic citation-graph query. "No follow-on with a resolution dimension" = **not found in this search**, not "does not exist."
5. **Trace Sampling 2.0 (arXiv 2509.13852)** — TITLE-ONLY. Span-level sampling is the nearest thing to a granularity axis in the tracing line; needs a full read.
6. **Breitung & Swanson (2002)** — TITLE-ONLY; Wiley not fetched. Claim rests on the title plus Rajaguru et al.'s characterization.
7. **Danks & Plis (2013)** origin paper — TITLE-ONLY; PhilPapers 403, KiltHub 403, Semantic Scholar returned no body.
8. **Hyttinen et al. venue string** — PGM 2016 / PMLR assumed but not confirmed; PubMed record page would not render.
9. **Gong et al. UAI 2017 abstract** — I have verbatim body/claim quotes from the auai.org PDF but not a verbatim complete abstract (PMC blocked by CAPTCHA).
10. **FDI / detectability-vs-isolability and sensor-placement-under-budget literature** — TITLE-ONLY across the board. Highest-priority remaining reading.
11. **HPC-specific resolution-vs-diagnosis work** — searched (LDMS, THAPI, CUG/SC monitoring papers); nothing found that varies sampling interval and measures diagnosis quality. Genuinely appears to be a gap, but this is "not found in this search."
12. **ACM DL / IEEE Xplore-only items** were not retrievable (403 by constraint), so any such work is under-sampled in this audit.

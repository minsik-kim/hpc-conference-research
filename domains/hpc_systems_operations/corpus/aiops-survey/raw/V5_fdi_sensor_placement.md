# V5 — FDI / Model-Based Diagnosis / Diagnosability-Theory Novelty Audit

**Audit target.** Telemetry policy π = {(m_i, f_i, r_i(τ))} — per-metric collect/rate/retention-resolution — minimizing multi-resource cost (collector CPU, network, storage, query, application perturbation) subject to detection accuracy ≥ α, detection latency ≤ δ, root-cause diagnosis quality ≥ β.

**Claimed novelty being stress-tested.** That prior art uses (i) binary sensor presence as the only decision variable, (ii) cost = number/price of sensors, (iii) quality = binary structural isolability, and (iv) requires an analytical plant model.

**Date of audit:** 2026-09-06. **Tooling:** WebSearch + WebFetch only. IEEE Xplore / ACM DL / ScienceDirect abstract pages returned 403 or ROBOTS_DISALLOWED and were not retried; routes used were the Fault Diagnosis Toolbox site and readthedocs, Linköping (LiU) staff publication pages and DiVA full texts, UPC/IRI Barcelona repository records, University of Luxembourg (orbilu) IFAC preprint mirrors, PMC, Springer, SAGE, arXiv, and one Crossref call.

**Evidence labels used:** FULL-TEXT / ABSTRACT / DOCUMENTATION / TITLE-ONLY / NOT FOUND / UNVERIFIED.

---

## 1. Corrected citations — the Rosich / Krysander & Frisk / Toolbox trio

### 1.1 Rosich, SAFEPROCESS 2012 — **CONFIRMED, and note it is a single-author paper**

> **A. Rosich (2012). "Sensor Placement for Fault Detection and Isolation based on Structural Models." 8th IFAC Symposium on Fault Detection, Supervision and Safety of Technical Processes (SAFEPROCESS 2012), Mexico City, Mexico, 29–31 August 2012, pp. 391–396. DOI: 10.3182/20120829-3-MX-2028.00161**

Affiliation: Institut de Robòtica i Informàtica Industrial (CSIC-UPC), Barcelona.
Label: **FULL-TEXT** (preprint PDF at https://orbilu.uni.lu/bitstream/10993/4479/1/0161.pdf) + **DOCUMENTATION** (repository record, https://www.iri.upc.edu/publications/show/1345).

Every element of the metadata-level note checks out verbatim:

- Specification notation — verbatim: *"Diagnosis specifications are feasible as long as D ⊆ Dmax and I ⊆ Imax."*
- Staging — verbatim: *"First, the detectability problem is solved. And then, based on the obtained results, the isolability problem is solved."*
- Problem 3 — verbatim: *"Given a structural model M of the process, a set of candidate sensors S to be installed in the process and the required diagnosis specifications, D and I, defined from the set of process faults F, find all minimal sensors configurations S′ ⊆ S such that diagnosis specifications are fulfilled within the model M ∪ MS′."*

Two corrections to how it must be cited: **no co-authors** (the note's implicit Rosich-et-al framing is wrong — Sarrate and Nejjari are on a *different* SAFEPROCESS 2012 paper, §4.1 below), and **it has no cost model at all** — it enumerates *all minimal* sensor configurations, with no optimization criterion. Sampling rate and retention appear nowhere in it (checked explicitly).

Do **not** confuse this with **Rosich, A., Frisk, E., Åslund, J., Sarrate, R., & Nejjari, F. (2012). "Fault Diagnosis Based on Causal Computations." IEEE Trans. SMC-A 42(2):371–381. DOI: 10.1109/TSMCA.2011.2164063** — a different Rosich 2012 paper, not about sensor placement specifications.

### 1.2 Krysander & Frisk, 2008 — **CONFIRMED exactly as noted**

> **Krysander, M., & Frisk, E. (2008). "Sensor Placement for Fault Diagnosis." IEEE Transactions on Systems, Man, and Cybernetics — Part A: Systems and Humans, 38(6):1398–1410. DOI: 10.1109/TSMCA.2008.2003968**

Label: **DOCUMENTATION** — triple-corroborated by three independent LiU-hosted sources: the toolbox reference list (https://faultdiagnosistoolbox.github.io/references/), Erik Frisk's institutional publication list (https://staff.gitlab-pages.liu.se/publications/en/liu/isy/fs/erifr93/), and the LiU PhD diagnosis course reading list (https://www.fs.isy.liu.se/Edu/Courses/DocDiagnos/kursmaterial.html). Full text not obtained (IEEE 403).

The companion paper the field cites alongside it, and which supplies the cleanest verbatim statement of the detectability/isolability relation:

> **Frisk, E., Krysander, M., & Åslund, J. (2009). "Sensor placement for fault isolation in linear differential-algebraic systems." Automatica 45(2):364–371. DOI: 10.1016/j.automatica.2008.08.013**

Label: **FULL-TEXT** (https://www.fs.isy.liu.se/Edu/Courses/DocDiagnos/CourseMaterial/linsensplace.pdf).

Also in the lineage: **Frisk, E. & Krysander, M. (2007). "Sensor placement for maximum fault isolability." 18th International Workshop on Principles of Diagnosis (DX-07), pp. 106–113.** Label: DOCUMENTATION.

### 1.3 Fault Diagnosis Toolbox — **CONFIRMED, both function names exact**

> **Frisk, E., Krysander, M., & Jung, D. (2017). "A Toolbox for Analysis and Design of Model Based Diagnosis Systems for Large Scale Models." IFAC World Congress, Toulouse, France. DOI: 10.1016/j.ifacol.2017.08.504**

This is the toolbox's own designated primary citation. Both function names in the note are correct, verbatim from the API documentation (https://faultdiagnosistoolbox.readthedocs.io/en/latest/faultdiagnosistoolbox.html):

- `SensorPlacementDetectability()` — *"Compute all minimal sensor sets that achieves maximal fault detectability of the faults in the model."*
- `SensorPlacementIsolability()` — *"Compute all minimal sensor sets that achieves maximal fault isolability of the faults in the model."* Takes an optional isolability specification as a 0/1 matrix.

Supporting API: `PossibleSensorLocations()`, `SensorLocationsWithFaults()`, `AddSensors()`.
The toolbox attributes its sensor-placement analysis to **Krysander & Frisk (2008)** and **Frisk, Krysander & Åslund (2009)**.
Label: **DOCUMENTATION**. Python port: https://github.com/faultdiagnosistoolbox/pyfaultdiagnosistoolbox. (The `www.fs.isy.liu.se/Software/FaultDiagnosisToolbox/user-manual.pdf` URL is dead — 404; use the readthedocs API page or https://faultdiagnosistoolbox.github.io/_releases/user-manual_2018-12-09.pdf.)

**Verdict on the trio: all three citations are essentially correct. Two fixes — Rosich 2012 is single-author, and the toolbox's primary citation is Frisk/Krysander/Jung IFAC WC 2017, not the 2008 paper.**

---

## 2. Question verdicts

### Q1 — Detectability/isolability separation: **CLOSED (foundational, settled since 2008–09)**

The separation is not merely established, it is *definitional* in this literature. Frisk, Krysander & Åslund, Automatica 2009, p. 366, **FULL-TEXT**:

> Definition 2: *"Fault fi is detectable in (1) if O(fi) ⊄ O(NF)"*
> Definition 3: *"Fault fi is isolable from fault fj in (1) if O(fi) ⊄ O(fj)"*
> and explicitly: *"Detection is a special case of isolation, i.e. a fault is detectable if the fault is isolable from the no-fault mode"*

Sarrate, Nejjari & Rosich, SAFEPROCESS 2012, **FULL-TEXT** (https://orbilu.uni.lu/bitstream/10993/4493/1/0233.pdf), same content in structural/MSO terms:

> *"A fault fj ∈ F is detectable if there exists at least one MSO set ωi ∈ ΩS such that vij = 1."*
> *"a fault fj1 is isolable from a fault fj2 if there exists at least one MSO set ωi ∈ ΩS such that vij1 = 1 ∧ vij2 = 0."*

The isolability condition is strictly the stronger requirement (it demands a *signature-separating* redundancy relation, not merely a fault-sensitive one), and both the Rosich 2012 staged algorithm and the toolbox's two distinct functions exist precisely because the two specifications yield different minimal sensor sets.

**Consequence for the audit:** the HPC formulation must *not* present the detection-vs-diagnosis distinction (α/δ vs β) as its own contribution. It is 2008-vintage prior art. It may only claim a new *instantiation* of that distinction (statistical anomaly detection vs statistical root-cause localization, on non-structural data).

### Q2 — Sampling rate as a decision variable: **PARTIALLY ADDRESSED — the closest work trades rate against isolation quality but never optimizes rate**

I found no work in FDI/diagnosability that makes per-sensor sampling frequency a **decision variable** in a constrained optimization over diagnosability. What exists, and how far each falls short:

**(a) Strongest adjacent result — event-triggered *isolation***

> **Li, S., Sauter, D., & Xu, B. (2011). "Fault Isolation Filter for Networked Control System with Event-Triggered Sampling Scheme." Sensors 11(1):557–572. DOI: 10.3390/s110100557**

Label: **FULL-TEXT** (https://ncbi.nlm.nih.gov/pmc/articles/PMC3274084). Verbatim abstract:

> *"In this paper, the sensor data is transmitted only when the absolute value of difference between the current sensor value and the previously transmitted one is greater than the given threshold value. Based on this send-on-delta scheme which is one of the event-triggered sampling strategies, a modified fault isolation filter for a discrete-time networked control system with multiple faults is then implemented by a particular form of the Kalman filter. The proposed fault isolation filter improves the resource utilization with graceful fault estimation performance degradation."*

This is the single closest hit to Q2 in the entire search: it is *isolation* (not just detection), and it explicitly trades **transmission/sampling rate against isolation performance** ("improves the resource utilization with graceful fault estimation performance degradation"; empirically 34–42% fewer transmissions). **But**: the threshold δᵢ is *given* — set heuristically as *"x-fold of the maximal amplitude"* of the measurement — and the filter is then designed to accommodate it. There is **no cost model, no budget, no constrained optimization, and no per-sensor rate allocation**. Rate is a knob whose consequences are analyzed, not a variable that is solved for.

**(b) Multirate FDI — rate is a plant constraint, not a design choice**

> **Qiu, A., Shi, J., & Wang, S. (2013). "Fault Detection for Dynamic Systems based on Multirate Sampling." International Journal of Online Engineering (iJOE) 9(6). DOI: 10.3991/ijoe.v9i6.3130**

Label: **FULL-TEXT**. Verbatim: *"the sampling rates of different sensors may not be equal due to numerous reasons such as hardware constraints and physical property of measurable variables."* Heterogeneous rates are treated as an **imposed constraint the detector must cope with**, not as a choice. Detection only, no isolation, no cost model for sampling faster. The wider multirate-FDI family (Hᵢ/H∞ and parity-space designs for multirate sampled-data systems, mostly on IEEE Xplore — TITLE-ONLY here) has the same posture.

**(c) Event-/self-triggered control and estimation — rate *is* optimized, but for the wrong objective**

The bandwidth-constrained sensor-scheduling literature (deep-RL sensor scheduling for remote state estimation; transmission scheduling via approximate dynamic programming; time-and-event-triggered hybrid schemes) genuinely optimizes transmission rate under a communication budget — but the objective is **state-estimation error or control performance**, never diagnosis or isolation quality. Label: **TITLE-ONLY / ABSTRACT**. The event-triggered *FDI* branch (Hᵢ/H∞ event-triggered fault detection; parity-space optimal event-triggered fault detection, Qiu, IET CTA 2021 — 403, TITLE-ONLY; interval-observer event-triggered detection) optimizes **detector gains and triggering thresholds for a detection performance index**, not a per-metric rate allocation under a resource budget.

**Verdict: the qualitative rate-vs-diagnosis-quality tradeoff is known and has been demonstrated (Li/Sauter/Xu 2011). Casting f_i as a decision variable in a cost-minimizing, diagnosability-constrained program is NOT done in this literature.** Do not claim the tradeoff is unrecognized; claim the *optimization* is unformulated.

### Q3 — Retention / data age as a decision variable: **STILL OPEN (no FDI hits whatsoever)**

Searches on "measurement retention diagnosis", "historical data retention fault diagnosis", "diagnostic data archiving fidelity", and "post-mortem diagnosability" returned **zero** FDI/control-engineering results. The retention queries returned only generic IT/GDPR compliance material (ZenGRC, Druva, Drata, Oracle ZFS docs) and software-engineering post-mortem practice (Bjørnson et al., "Improving the effectiveness of root cause analysis in post mortem analysis"), none of which formulates retention as a diagnosability decision variable.

I also checked the three most-likely-to-contain-it full texts explicitly for the terms: Rosich SAFEPROCESS 2012 (*"Neither sampling rate nor data retention appears anywhere in this document"*), Sarrate/Nejjari/Rosich SAFEPROCESS 2012 (same), Frisk/Krysander/Åslund Automatica 2009 (*"Neither sampling rate nor retention appear in this paper"*), and Eriksson's licentiate thesis (no discussion).

**Verdict: STILL OPEN.** The structural reason is sound and worth stating in related work: FDI assumes a *streaming online observer* reading current measurements. Data age is not in its ontology — there is nothing to retain, because the residual is evaluated at time t. Label: **NOT FOUND** (searched, absent — distinct from proven nonexistent).

### Q4 — Cost models: **PARTIALLY ADDRESSED — rich per-sensor economic costs, zero data-volume costs**

The strongest budget-constrained formulation with a stated cost semantics:

> **Sarrate, R., Nejjari, F., & Rosich, A. (2012). "Model-based optimal sensor placement approaches to fuel cell stack system fault diagnosis." 8th IFAC SAFEPROCESS, Mexico City, pp. 96–101. DOI: 10.3182/20120829-3-MX-2028.00233**

Label: **FULL-TEXT** (https://orbilu.uni.lu/bitstream/10993/4493/1/0233.pdf). Verbatim problem statement — note how closely it rhymes with the HPC formulation's *shape*:

> *"GIVEN A set of candidate sensors S, a sensor cost function C(·), a set of model equations M, a fault detectability specification FD and a fault isolability specification FI, FIND the minimum cost sensor configuration S∗ ⊆ S, such that the fault diagnosis specifications are fulfilled."*

And verbatim on what cost *means*:

> *"Such cost can comprise different concepts such as the purchase price, the maintenance price, the sensor reliability or the measurement precision, for instance."*
> *"[costs are] dimensionless and have been assigned according to the ease of installation and the price of their corresponding sensors."*

Solved three ways: incremental search, heuristic search, and **binary integer linear programming**.

Other budget-constrained formulations:

- **Rostek, K. (2016). "Optimal Sensor Placement Under Budgetary Constraints." In Kowalczuk, Z. (ed.), *Advanced and Intelligent Computations in Diagnosis and Control*, pp. 77–88. DOI: 10.1007/978-3-319-23180-8_6** — **ABSTRACT**. Inverts the program: *"maximizes diagnosability and isolability, while not exceeding the budgetary constraint"*, via Binary Diagnostic Matrix + branch-and-bound, on a fuel cell stack. The cost structure is not specified in the accessible preview. **UNVERIFIED** on cost detail.
- **Sarrate, R., Nejjari, F., & Rosich, A. (2012). "Sensor placement for fault diagnosis performance maximization in distribution networks." 20th Mediterranean Conference on Control and Automation (MED), Barcelona, pp. 110–115. DOI: 10.1109/MED.2012.6265623** — **ABSTRACT/DOCUMENTATION**. Cardinality constraint (sensor count budget), diagnosability maximized. Water-network leak localization.
- **Chaleshtori, A. E., & Aghaie, A. "A new framework of sensor selection for developing a fault detection system based on data-envelopment analysis."** arXiv:2403.20006, **FULL-TEXT** (HTML). The most *multi-component* cost model found: *purchase, installation, replacement, disassembly, and inspection costs*, tabulated in dollars across 4 sensors and 9 load conditions, used as a DEA input. Detection only (healthy vs. broken tooth), no isolation.

**On the two citations in the notes:**

- *"Optimal test and sensor selection for active fault diagnosis using integer programming"* — the title **exists** in *Control Engineering Practice*, ScienceDirect PII **S0959152420302419** (consistent with a 2020 CEP article). Landing page was **ROBOTS_DISALLOWED**; authors, volume, pages and DOI **could not be retrieved**. Label: **TITLE-ONLY / UNVERIFIED — do not cite until authors and DOI are confirmed.**
- *"Optimal Sensor Selection for Active Fault Diagnosis using Test Information Criteria"* — the title **exists** in *IFAC-PapersOnLine*, ScienceDirect PII **S2405896319301788** (consistent with 2019). Landing page **ROBOTS_DISALLOWED**; authors and DOI **not retrieved**. Label: **TITLE-ONLY / UNVERIFIED — same warning.**

Both are almost certainly real (the PIIs and journals match the notes), but neither is citable yet. Recommended resolution route: Crossref bibliographic query, or the DTU/Aalborg institutional repository — active fault diagnosis with test selection is a Danish-school topic.

**Verdict on cost: PARTIALLY ADDRESSED.** Cost is genuinely a first-class, weighted, budget-constrained object here — price, maintenance, reliability, precision, installation ease, purchase/replacement/inspection, cardinality. But **nothing resembling bytes/second, storage-TB-months, query cost, or observer-induced perturbation of the monitored system appears anywhere.** The cost is the *capital cost of an instrument*, never the *marginal cost of a byte*. That distinction is the surviving contribution, and it must be stated at exactly that resolution — not as "prior work only counts sensors," which is demonstrably false.

### Q5 — Quality metrics: **CLOSED. Continuous statistical diagnosis quality is a mature, 15-year sub-branch — and it has already been used to drive sensor placement**

This is the most damaging finding of the audit. The claim that quality is "binary structural isolability" is **false as stated**. The Linköping group built exactly the quantitative alternative, and then plugged it into sensor placement.

Foundational:

- **Eriksson, D., Krysander, M., & Frisk, E. (2011). "Quantitative Stochastic Fault Diagnosability Analysis." 50th IEEE CDC / ECC, pp. 1563–1569. DOI: 10.1109/CDC.2011.6160362** — DOCUMENTATION.
- **Eriksson, D., Frisk, E., & Krysander, M. (2013). "A method for quantitative fault diagnosability analysis of stochastic linear descriptor models." Automatica 49(6):1591–1600. DOI: 10.1016/j.automatica.2013.02.045** — DOCUMENTATION (Automatica landing page 403).
- **Jung, D., Frisk, E., & Krysander, M. (2015). "Quantitative isolability analysis of different fault modes." 9th IFAC SAFEPROCESS, pp. 1275–1282. DOI: 10.1016/j.ifacol.2015.09.701** — **FULL-TEXT** (https://www.vehicular.isy.liu.se/Publications/Articles/IFACSP_15_DJ_EF_MK.pdf). Metric is Kullback–Leibler-divergence-based *distinguishability*; verbatim: *"Expected distinguishability Di,j of a fault mode fi from a fault mode fj, where the distribution of fault time profile θ given fi has the pdf qi θ, is defined as Di,j = Eqi θ [Di,j(θ)]."* And the motivating critique, verbatim: deterministic diagnosability analysis *"only give yes/no answers"*, which matters because *"it is not certain that a solution will fulfill the given quantitative fault detection and isolation performance requirements in practice due to model uncertainties and measurement noise."*
- **Åslund, J., Frisk, E., & Krysander, M. (2019). "Asymptotic behavior of a fault diagnosis performance measure for linear systems." Automatica 106:143–149. DOI: 10.1016/j.automatica.2019.04.041** — DOCUMENTATION.

Extensions found (ABSTRACT/TITLE-ONLY): *"A Method for Quantitative Fault Diagnosability Analysis of Systems with Probabilistic Sensor Faults"* (Int. J. Control, Automation and Systems, DOI 10.1007/s12555-018-0319-z); *"Data-driven method for the quantitative fault diagnosability analysis of dynamic systems"* (Fu et al., IET Control Theory & Applications, 2019, DOI 10.1049/iet-cta.2018.5378 — 403, TITLE-ONLY); *"Evaluation of Aero-engine Fault Diagnosability Under Multi-source Uncertainty"* (Int. J. Aeronautical and Space Sciences, 2025, DOI 10.1007/s42405-025-00944-4); **Kong, Ç.-W., McMahon, J., & Lahijanian, M. (2025). "Bayesian Diagnosability and Active Fault Identification." arXiv:2509.04708** — **ABSTRACT**, verbatim: *"Our approach hinges on a new quantitative diagnosability definition, revealing when passive fault identification (FID) is fundamentally limited by the given control sequence."*

Also relevant, using a non-structural performance metric with a Bayesian Belief Network: **Reeves, J., Remenyte-Prescott, R., & Andrews, J. (2019). "Sensor selection for fault diagnostics using performance metric." Proc. IMechE Part O: J. Risk and Reliability 233(4). DOI: 10.1177/1748006X18804690** — ABSTRACT.

**Verdict: CLOSED.** Continuous, probabilistic, information-theoretic diagnosis quality is standard equipment in this field, and the field itself published the critique of binary structural quality. The related-work section must cite Eriksson 2013 and Jung 2015 and concede this outright.

### Q6 — Model requirement: **PARTIALLY ADDRESSED — the requirement is real and near-universal, and no mature model-free *sensor-placement-for-isolability* branch was found**

The model requirement is confirmed unambiguously across every sensor-placement paper examined. Rosich 2012's Problem 3 begins *"Given a structural model M of the process…"*. Sarrate 2012's problem statement requires *"a set of model equations M"*. Raju, Bakirtzis & Topcu, "Sensor Placement for Online Fault Diagnosis," arXiv:2211.11741 (**FULL-TEXT**) requires *"a tuple (SYS,COMP), where SYS is a model (description) of the system"* in first-order logic encoded in Answer Set Programming. The machinery is exactly the structural apparatus named in the audit brief: bipartite graphs over equations and variables, Dulmage–Mendelsohn decomposition, and **MSO (minimal structurally overdetermined) sets** — MSOs are the explicit currency of the detectability/isolability conditions in Sarrate 2012, and the toolbox's founding algorithm is Krysander, Åslund & Nyberg (2008), *"An Efficient Algorithm for Finding Minimal Over-constrained Sub-systems for Model-based Diagnosis,"* IEEE Trans. SMC-A 38(1), DOI 10.1109/TSMCA.2007.909555.

**Is there a model-free branch?** Two things exist, and neither closes the gap:

1. **Model-free fault *diagnosis*** — yes, mature (CNN/deep-learning diagnosis from raw sensor data; *"Proximal-based recursive implementation for model-free data-driven fault diagnosis,"* Automatica 2024, PII S0005109824001493, TITLE-ONLY). But this classifies faults given a fixed sensor set; it does **not** select sensors.
2. **Data-driven sensor selection** — thin, and detection-only. The DEA paper (arXiv:2403.20006) selects sensors by classifier accuracy/AUC against a dollar cost — genuinely model-free selection — but only two classes (healthy vs. broken tooth), i.e. **detection, not isolation**.

The most honest boundary case, and one a reviewer may raise:

> **Jung, D., & Axelsson, D. (2024). "A Study on Redundancy and Intrinsic Dimension for Data-Driven Fault Diagnosis." DX 2024 (35th Int. Conf. on Principles of Diagnosis and Resilient Systems). DOI: 10.4230/OASIcs.DX.2024.4** — **FULL-TEXT** (open access, Dagstuhl OASIcs).

Verbatim: *"In model-based diagnosis, the ability construct fault detectors depends on analytical redundancy properties. While analytical redundancy is a model property, it describes the diagnosability properties of the system. In this work, the connection between analytical redundancy and the distribution of observations from the system on low-dimensional manifolds in the observation space is studied. It is shown that the intrinsic dimension can be used to identify signal combinations that can be used for constructing residual generators."* This selects **signal combinations from data** rather than sensors from a model — the closest thing to model-free diagnosability design — but it still reasons *about* analytical redundancy, and it does not do placement or cost optimization.

Also worth naming as the data-driven-diagnosability adjacent work: **Lundgren, A., & Jung, D. (2022). "Data-driven fault diagnosis analysis and open-set classification of time-series data." Control Engineering Practice 121:105006. DOI: 10.1016/j.conengprac.2021.105006**; and **Mohammadi, A., Krysander, M., & Jung, D. (2025). "Consistency-based diagnosis using data-driven residuals and limited training data." Control Engineering Practice 159:106283. DOI: 10.1016/j.conengprac.2025.106283**. Both DOCUMENTATION.

**Verdict: PARTIALLY ADDRESSED.** The model-requirement defense survives for *placement/policy design under an isolability constraint*, which is the relevant claim — but it is weakening year over year, and the defense must be phrased precisely (see §5).

---

## 3. The strongest single paper a hostile reviewer would cite

> **Eriksson, D., Krysander, M., & Frisk, E. (2012). "Using quantitative diagnosability analysis for optimal sensor placement." Proceedings of the 8th IFAC Symposium on Fault Detection, Supervision and Safety of Technical Processes (SAFEPROCESS 2012), Mexico City, pp. 940–945. DOI: 10.3182/20120829-3-MX-2028.00196**

Label: **FULL-TEXT via containing thesis** — it is Paper B of Daniel Eriksson's licentiate thesis, *"Diagnosability analysis and FDI system design for uncertain systems,"* Linköping Studies in Science and Technology, Thesis No. 1584, open full text at https://liu.diva-portal.org/smash/get/diva2:610541/FULLTEXT02.pdf. (Metadata independently corroborated on Daniel Jung's LiU publication list.)

**This is the paper to worry about, because it is structurally isomorphic to the HPC formulation minus the temporal variables.** Verbatim from the thesis:

> *"The sensor placement problem is formulated as an optimization problem, where required fault detectability and isolability performance is taken into consideration by using minimum required diagnosability performance as a constraint."*
> *"[the goal is finding] the cheapest set of sensors that achieves a required fault diagnosability performance"*
> *"Results show that the required diagnosability performance greatly affects which sensors to use, which is not captured if not model uncertainties and measurement noise are taken into consideration"*

**What it covers — and this is exactly the claimed novelty structure:**
- Minimize **cost** (explicitly "cheapest set", i.e. weighted price, not merely count)
- Subject to a **continuous, statistical, non-binary quality constraint** — KL-divergence-based distinguishability, with a *minimum required performance level* as the constraint
- Separate **detectability and isolability** performance requirements (the α-vs-β split)
- Solved by greedy search over sensor sets

**What it does not cover:**
- **No sampling frequency.** Sensors are present-or-absent; there is no f_i.
- **No retention or data age.** Nothing about r_i(τ); no notion of stored measurements at reduced fidelity.
- **No detection-latency constraint.** No δ. (Detection *delay* appears in the adjacent Bayesian-diagnosability work, arXiv:2509.04708, but not as a constraint in a placement program.)
- **No multi-resource cost decomposition.** Cost is a scalar per-sensor price, not a vector over collector CPU / network / storage / query / perturbation.
- **No observer-perturbation term.** In FDI, measuring is free of side effects on the plant — the HPC case's application-perturbation cost has no analogue at all.
- **Requires a stochastic model** — linear descriptor form with specified noise distributions. Not applicable to a supercomputer.
- **Faults are a small, enumerated, pre-specified set** with known fault-mode distributions; no open-set / unknown-fault regime.

A reviewer citing this will say: *"the optimization structure — minimize instrumentation cost subject to a quantitative detectability and isolability performance floor — is Eriksson et al., SAFEPROCESS 2012."* The correct answer is that the *decision space* and the *cost vector* differ, not the constraint-optimization idea. Anticipate it explicitly and cite it in the first paragraph of related work.

Secondary hostile citation, for the "quality is not binary" point specifically: **Jung, Dong, Frisk, Krysander & Biswas (2020). "Sensor selection for fault diagnosis in uncertain systems." International Journal of Control 93(3):629–639. DOI: 10.1080/00207179.2018.1484171** (metadata Crossref-confirmed; abstract not retrieved — SAGE/T&F 403 — **UNVERIFIED** on method detail).

---

## 4. Verdict on the three claimed gaps

| Claimed gap | Verdict | Basis |
|---|---|---|
| **Sampling rate f_i as a decision variable** | **SURVIVES, narrowed** | No FDI work optimizes per-metric rate under a diagnosability constraint. But the rate-vs-isolation-quality tradeoff is *known and demonstrated* (Li, Sauter & Xu 2011, Sensors, event-triggered isolation filter), and rate *is* optimized in the estimation/control-oriented event-triggered literature. Claim the formulation, never the insight. |
| **Retention / data age r_i(τ) as a decision variable** | **SURVIVES, strongest of the three** | Zero hits across six query families; explicitly absent from four full texts checked term-by-term. Structural explanation available: FDI is an online streaming-observer paradigm in which data age has no ontological place. This is the cleanest novelty claim in the whole formulation. |
| **Continuous statistical diagnosis quality** | **DEAD** | Falsified by a 15-year sub-branch (Eriksson CDC 2011; Eriksson et al. Automatica 2013; Jung et al. SAFEPROCESS 2015; Åslund et al. Automatica 2019; Kong et al. 2025), and specifically by Eriksson et al. SAFEPROCESS 2012, which uses continuous quality *as the constraint in a cost-minimizing sensor placement program*. Retract this claim. |

**Corollary — the cost claim, which the brief bundled into "cost = number/price of sensors":** that characterization is **too weak to defend** and should be restated. Prior cost models include purchase price, maintenance, reliability, precision, installation ease, replacement/disassembly/inspection cost, and hard budget constraints. What is genuinely absent is **data-volume cost** — bytes/s, storage-TB-months, query cost — and **observer-induced perturbation of the monitored system**. Claim *that*.

---

## 5. Verdict on the model-requirement defense

**The defense holds, but only in a precisely-worded form.**

What is solidly true: every sensor-placement-for-diagnosability method examined requires an analytical or structural plant model — a set of equations, its bipartite structure graph, DM decomposition, and MSO sets. This is not incidental; the detectability and isolability *conditions themselves* are stated over MSO sets (Sarrate 2012, verbatim in §2/Q1). A supercomputer has no such equation set, so the machinery cannot be transplanted. Even the most modern formulation found (Raju/Bakirtzis/Topcu 2022, ASP-based) needs a first-order-logic system description.

What weakens it: model-free fault *diagnosis* is mature; data-driven *quantitative diagnosability analysis* exists (Fu et al., IET CTA 2019); data-driven sensor *selection* exists for detection (DEA, arXiv:2403.20006); and Jung & Axelsson (DX 2024) explicitly attacks the boundary by recovering redundancy structure from the intrinsic dimension of observation data rather than from equations. A reviewer could argue the trajectory is toward model-free placement.

**Recommended phrasing.** Do not claim "these methods require a model, therefore HPC needs an empirical approach" — too broad, and DX 2024 is a counterexample in spirit. Claim instead: *no existing method selects a monitoring configuration under an isolability/diagnosis-quality constraint without an analytical or structural model of the system; the data-driven branch either fixes the sensor set and learns a classifier, or selects sensors against a detection-accuracy objective only (two-class), and no data-driven method treats fault isolation quality as a constraint on a cost-minimizing configuration choice.* That statement is supported by everything found here, and cite Jung & Axelsson 2024 as the nearest attempt so the reviewer sees it was considered.

---

## 6. What remains unverified

1. **Both Q4 notes citations.** *"Optimal test and sensor selection for active fault diagnosis using integer programming"* (CEP, PII S0959152420302419) and *"Optimal Sensor Selection for Active Fault Diagnosis using Test Information Criteria"* (IFAC-PapersOnLine, PII S2405896319301788): titles and journals confirmed to exist, **authors, year, volume, pages, DOI not retrieved** (ScienceDirect ROBOTS_DISALLOWED). **TITLE-ONLY — not citable.** Resolve via Crossref bibliographic query or a Danish institutional repository.
2. **Krysander & Frisk 2008 full text** never obtained (IEEE 403). Metadata is triple-corroborated; the *verbatim* detectability/isolability statements in this report come from the 2009 Automatica companion instead. If a verbatim quote from the 2008 paper is needed, try the LiU DiVA record.
3. **Eriksson et al. SAFEPROCESS 2012 (§3) — exact mathematical program not obtained.** All quotes are the thesis's own summary of its Paper B, not the paper's equations. Whether its cost function is scalar price or a weighted vector, and the exact form of the distinguishability constraint, are **UNVERIFIED**. Given this is the strongest hostile citation, retrieve the thesis's Paper B section in full before writing related work.
4. **Jung, Dong, Frisk, Krysander & Biswas 2020 (IJC)** — metadata Crossref-confirmed, abstract and method **UNVERIFIED** (T&F 403). This may be an even closer match to the HPC formulation than Eriksson 2012; worth resolving via DiVA (record diva2:806672 — both DiVA hosts returned ROBOTS_DISALLOWED in this session; retry later or use a different route).
5. **Rostek 2016 cost structure** — whether its "budgetary constraint" is monetary, cardinality, or abstract weight is **UNVERIFIED** (Springer preview only).
6. **Qiu 2021 IET CTA "Parity space-based optimal event-triggered fault detection"** — 403, **TITLE-ONLY**. This is the one remaining paper that could plausibly optimize triggering rate against a detection performance index in a constrained form; it should be read before finalizing the Q2 verdict.
7. **Q2/Q3 negatives are "not found in this search," not proofs of nonexistence.** IEEE Xplore and ACM DL were entirely inaccessible, and much of the event-triggered FDI and multirate FDI corpus lives there. The Q3 negative is strong (six unrelated query families, four term-level full-text checks); the Q2 negative is moderate and would benefit from one pass through IEEE-indexed event-triggered FDI titles.
8. **Discrete-event-systems diagnosability** (Sampath/Lafortune lineage, and e.g. *"Diagnosability and attack detection for discrete event systems under sensor attacks,"* DEDS 2024) was **not surveyed**. It is a separate diagnosability tradition with its own sensor-selection results and its own notion of diagnosability-within-bounded-delay — which is closer to the δ latency constraint than anything in the continuous-FDI literature. **Recommend a follow-up audit pass on DES diagnosability**; it is the most likely remaining source of a surprise.

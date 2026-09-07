# V3 Falsification Check — PIKA (IEEE Cluster 2020) and Tuncer et al. (IEEE TPDS 2019)

Audit date: 2026-09-06
Tooling: WebSearch + WebFetch only. IEEE Xplore and ACM DL not attempted (known 403).
Evidence labels: FULL-TEXT / ABSTRACT / TITLE-ONLY / INDIRECT (quoted in citing or author-side work) / NOT FOUND / UNVERIFIED

---

## TARGET 1 — PIKA

### Bibliographic record (settled)

- **Title:** "PIKA: Center-Wide and Job-Aware Cluster Monitoring"
- **Authors:** Robert Dietrich, Frank Winkler, Andreas Knüpfer, Wolfgang E. Nagel (all TU Dresden, Center for Information Services and High Performance Computing / ZIH)
- **Pages:** 424–432
- **Venue string in indexes:** 2020 IEEE International Conference on Cluster Computing (CLUSTER), Kobe, Japan, 14–17 September 2020
- **DOI:** 10.1109/CLUSTER49012.2020.00061
- **dblp key:** conf/cluster/DietrichWKN20
- **OA status:** closed. OpenAlex `best_oa_location` = null; Semantic Scholar `openAccessPdf.url` = "" .
- Evidence: **FULL-TEXT of metadata** (Crossref record, OpenAlex record, dblp record, Semantic Scholar record all agree). Paper body itself: **NOT FOUND / INSUFFICIENT ACCESS**.

Sources:
- https://api.crossref.org/works/10.1109/cluster49012.2020.00061
- https://api.openalex.org/works/doi:10.1109/cluster49012.2020.00061
- https://dblp.org/rec/conf/cluster/DietrichWKN20.html
- https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/cluster49012.2020.00061

### Abstract (verbatim, ABSTRACT)

From the Semantic Scholar record:

> "Nowadays, performance optimization is more or less an established procedure in high-performance computing (HPC) centers. To sustainably increase compute efficiency of such systems, we need to increase the awareness of efficiency on both the operator's and the users' side. Therefore, we propose an infrastructure for continuous monitoring and analysis, which automatically characterizes HPC jobs and provides a systematic approach to identify underperforming compute jobs with optimization potential. The recorded metadata and time-series data can be visualized live at runtime or post-mortem and are eventually stored for long-term analysis. The monitoring has a negligible overhead on the compute nodes and neither influences nor limits the user applications."

Note: the overhead claim in the abstract is **qualitative** ("negligible"). No number, no benchmark, no node count, no rate appears in the abstract.

### Q1 — How many distinct sampling rates / collection intervals?

**Answer: two fixed intervals, split by metric class (30 s and 60 s), both described as "adjustable". No evidence of a sampling-rate sweep or comparison of rates.**
Evidence depth: **INDIRECT (author-side artifacts) + NOT FOUND for the paper body.**

Author-side evidence, from a 2021 BoF deck carrying the *exact paper title* ("PIKA: Center-Wide and Job-Aware Cluster Monitoring"), hosted at hps.vi4io.org:
> CPU counters are "collected with LIKWID[2] every 60s*"; "All other metrics are collected every 30s*"; "* adjustable"
Source: https://hps.vi4io.org/_media/events/2021/21-bof-analyzing-pika.pdf

Official ZIH deployment documentation:
> "Most metrics are recorded every 30 seconds except IPC, FLOPS, Main Memory Bandwidth and Power Consumption. The latter are determined every 60 seconds."
Source: https://compendium.hpc.tu-dresden.de/software/pika/

VI-HPS 44th Tuning Workshop deck (Frank Winkler):
> "Sampled every 30 seconds" (metric timeline vectors incl. CPU/GPU load, memory usage, I/O bandwidth and metadata)
Source: https://www.vi-hps.org/cms/upload/material/tw44/PIKA-CIDS-VIHPS.pdf

Interpretation: this is a **static design split by metric cost** (hardware-counter metrics are cheaper to read at 60 s), not a swept experimental variable. Nothing in any reachable source shows PIKA *evaluating* two or more rates against each other.

### Q2 — Does it collect GPU metrics?

**Answer: YES. GPU Usage, GPU Memory Utilization, GPU Power Consumption, GPU Temperature, sourced from NVML, at the 30 s interval, per GPU device.**
Evidence depth: **INDIRECT (author-side artifacts), high confidence.**

- VI-HPS deck: GPU Usage / GPU Memory Utilization / GPU Power Consumption / GPU Temperature, "Data source: NVML", collected via a collectd plugin. https://www.vi-hps.org/cms/upload/material/tw44/PIKA-CIDS-VIHPS.pdf
- ZIH booth page (Dietrich et al. cited with pp. 424–432): same four GPU metrics listed. https://booth.zih.tu-dresden.de/?page_id=46
- ZIH compendium: all GPU metrics at 30 s, per GPU device. https://compendium.hpc.tu-dresden.de/software/pika/

Caveat: these are 2021–2024 artifacts describing the *deployed* system. Whether the 2020 paper itself already documented the GPU/NVML plugin is **UNVERIFIED** (probable, given Taurus's GPU partitions and the collectd-plugin architecture, but not confirmed from the paper).

### Q3 — Does it measure application runtime overhead / perturbation?

**Answer: A qualitative claim of negligible overhead is made in the abstract. No quantitative perturbation measurement — no magnitude, benchmark, node count, or per-rate figure — could be located in any reachable source. Whether the paper body contains an overhead table or measurement is CANNOT DETERMINE.**
Evidence depth: **ABSTRACT for the qualitative claim; NOT FOUND / INSUFFICIENT ACCESS for any number.**

- Abstract: "The monitoring has a negligible overhead on the compute nodes and neither influences nor limits the user applications."
- 2021 BoF deck (same title): "Monitoring overhead is negligible"; monitoring "Can also be disabled (#SBATCH –no-monitoring)". No numbers, no benchmarks, no node counts.
- 2022 NHR workshop deck (Winkler, PIKA Overview): contains **no** overhead statement or numbers at all. https://hpc.fau.de/files/2022/07/NHR-Workshop2022-Frank-Winkler-PIKA_Overview.pdf
- ZIH compendium: only a relative, unquantified remark that counter-combination metrics "are a combination of different hardware counters, which leads to a higher measurement overhead."

No reachable source attributes any *numeric* overhead figure to the PIKA 2020 paper. No citing work found that quotes one.

### Q4 — Downstream analysis quality as a function of sampling rate or aggregation window?

**Answer: No evidence of any such study. The 2023 follow-up, which is the paper that actually does the detection/diagnosis work, uses fixed heuristics and thresholds derived from operational experience, with no rate- or window-sensitivity analysis.**
Evidence depth: **ABSTRACT (follow-up) + NOT FOUND (2020 paper).**

Follow-up: Frank Winkler, Andreas Knüpfer, "Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA", ISC High Performance 2023 workshops, LNCS vol. 13999, pp. 295–306, DOI 10.1007/978-3-031-40843-4_22. Abstract verbatim in part:
> "All parameters and thresholds are derived from experience and tuned to detect the most severe cases in the average job mix. The heuristics range from simple cases that compare against appropriate thresholds to more sophisticated tests with some pre-processing."
Source: https://link.springer.com/chapter/10.1007/978-3-031-40843-4_22
This abstract contains no mention of sampling interval, collection rate, aggregation window sensitivity, or overhead.

### Q5 — Exact title, authors, page range

See Bibliographic record above. **FULL-TEXT (metadata).**

### Q6 — Main-track or workshop?

**Answer: WORKSHOP. It is an HPCMASPA 2020 paper — the Workshop on Monitoring and Analysis for High Performance Computing Systems Plus Applications — held in conjunction with IEEE Cluster 2020 and bundled into the main CLUSTER 2020 proceedings volume (hence the 10.1109/CLUSTER49012.2020.* DOI prefix and pp. 424–432).**
Evidence depth: **INDIRECT, two independent author-side sources, decisive.**

1. ProPE project publication list (ProPE, DFG grant NA711/15-1, is the project that funded PIKA; the page is maintained by the consortium), verbatim:
> "R. Dietrich, F. Winkler, A. Knüpfer and W. Nagel: PIKA: Center-Wide and Job-Aware Cluster Monitoring. Proc. HPCMASPA 2020, Workshop on Monitoring and Analysis for High Performance Computing Systems Plus Applications, September 14, 2020, Kobe, Japan. Held in conjunction with IEEE Cluster 2020. DOI: 10.1109/CLUSTER49012.2020.00061"
Source: https://blogs.fau.de/prope/publications/

2. The authors' own 2023 follow-up cites it as reference [5] with the venue given as:
> "PIKA: center-wide and job-aware cluster monitoring. In: Workshop on Monitoring and Analysis for High Performance Computing Systems Plus Applications."
Source (reference list mirror): https://ouci.dntb.gov.ua/en/works/7pYXpAe4/

Note: HPCMASPA is the IEEE-Cluster-co-located workshop of that name. Do **not** confuse it with MODA, which is the ISC-HPC-co-located workshop (MODA20 was 25 June 2020, Frankfurt, with ISC HPC 2020 — https://hpc.dmi.unibas.ch/research/moda/). The task brief's "MODA 2023 follow-up" is in fact an ISC 2023 workshop paper (LNCS 13999), a different series from HPCMASPA.

### PIKA ruling

Does PIKA kill a claim that "no HPC paper measures GPU-era monitoring perturbation at multiple sampling rates"?

**NO.**

Rationale: PIKA does collect GPU metrics (NVML), and it does run two different collection intervals (30 s / 60 s). But (a) the two intervals are a fixed design split by metric class, not an evaluated variable — no reachable source shows PIKA comparing rates; (b) its overhead claim is qualitative ("negligible") in the abstract with no located magnitude, benchmark, node count, or per-rate figure; (c) there is no downstream analysis-quality-versus-rate study anywhere in PIKA or its 2023 follow-up. Additionally, it is a **workshop** paper (HPCMASPA 2020), not main-track IEEE Cluster, which lowers its weight as a counterexample.

Residual risk (stated honestly): the paper body is **not accessible**, and an abstract that asserts negligible overhead plausibly backs it with *some* measurement in the evaluation section. If that measurement turns out to be quantitative and taken at both 30 s and 60 s including GPU plugins, the claim would need softening. So the ruling is NO on the multi-rate-sweep and downstream-quality elements (high confidence), with **CANNOT DETERMINE** on the narrower sub-question "does the paper body report any quantitative overhead number at all."

Recommended defensive rewording of the claim: "no HPC paper reports a *quantitative* GPU-era monitoring perturbation study *across multiple evaluated sampling rates* with a downstream analysis-quality axis" — PIKA does not threaten that form.

---

## TARGET 2 — Tuncer et al.

### Q1 — Exact titles, authors, venues, years, DOIs, volume/pages

**Journal version (the TPDS paper):** FULL-TEXT
- **Title:** "Online Diagnosis of Performance Variation in HPC Systems Using Machine Learning"
- **Authors:** Ozan Tuncer, Emre Ates, Yijia Zhang, Ata Turk, Jim Brandt, Vitus J. Leung, Manuel Egele, Ayse K. Coskun
- **Venue:** IEEE Transactions on Parallel and Distributed Systems, **vol. 30, no. 4, pp. 883–896, April 2019**
- **DOI:** 10.1109/TPDS.2018.2870403
- Open full text: https://www.bu.edu/peaclab/files/2019/03/08466019.pdf (published version, PeacLab)
  and https://emreates.github.io/publications/tuncer_TPDS18.pdf (author copy)
- Also indexed at OSTI: https://www.osti.gov/biblio/1474092

**Earlier conference version (distinct paper):** FULL-TEXT
- **Title:** "Diagnosing Performance Variations in HPC Applications Using Machine Learning"
- **Authors:** Ozan Tuncer, Emre Ates, Yijia Zhang, Ata Turk, Jim Brandt, Vitus J. Leung, Manuel Egele, Ayse K. Coskun
- **Venue:** ISC High Performance 2017, LNCS vol. 10266, **pp. 355–373**, June 2017
- **DOI:** 10.1007/978-3-319-58667-0_19
- Award: **Gauss Award** (per PeacLab publication list)
- Open full text: https://www.bu.edu/peaclab/files/2020/01/isc.pdf

Bibliographic source (verbatim entries): https://www.bu.edu/peaclab/publications/

Distinction: the ISC 2017 paper does offline classification of whole application runs on two testbeds; the TPDS 2019 paper generalizes it to **online** sliding-window detection and diagnosis, adds statistical feature selection with an FDR control, a confidence-threshold mechanism, and generalization experiments (unknown applications, unknown configurations, unknown/low anomaly intensities).

### Q2 — Fixed monitoring sampling interval

**Answer: 1 second, fixed, throughout the TPDS paper.** In the ISC 2017 paper, 1 s on the Cray testbed and 5 s on the second (cloud) testbed — i.e. two testbeds with different native rates, not a swept parameter.
Evidence depth: **FULL-TEXT.**

TPDS verbatim:
> "At every second, LDMS collects 721 metrics in five categories"
> "State-of-the-art monitoring tools such as LDMS collect data with a sampling period of one second while using less than 0.1 percent of a core"

ISC 2017 verbatim:
> "At every second, LDMS collects 721 different metrics" (Volta)
> "Every 5 s, this infrastructure collects 53 metrics" (MOC)

### Q3 — Which variable(s) are swept in the sensitivity analysis?

**Answer: WINDOW SIZE is the swept temporal variable in TPDS. The sampling interval is not swept in TPDS.**
Evidence depth: **FULL-TEXT.**

TPDS verbatim:
> "Fig. 2 shows the impact of window size on the overall F-score of baseline algorithms as well as our proposed framework with three different classifiers."
> "Based on the results in Figs. 2 and 3, we conclude that a 45-second window size is a reasonable choice to accurately detect our target anomalies while keeping the detection delay low."

Confirmed swept variables in TPDS:
1. **Sliding-window size W** (seconds) — the headline sensitivity sweep; chosen default 45 s. Range on the figure x-axis spans roughly 10–90 s. *(The exact tick list is UNVERIFIED — PDF-to-text extraction of the Fig. 2 axis returned inconsistent lists across attempts (10/20/30/45/60/90 vs 10/15/20/30/45/60/90). Only the 45 s default and the "impact of window size" framing are quoted verbatim.)*
2. **False Discovery Rate (FDR) target** for statistical feature selection — swept across a range up to ~10%.
3. **Confidence threshold C** — swept, traded off as false-alarm rate vs miss rate.
4. **Anomaly intensity** — training/testing on disjoint intensity sets (20/50/100% for training; 2/5/10% held out as "low intensity").
5. **Unknown input configurations** — models trained excluding 1 or 2 application configurations.
6. **Unknown applications** — leave-one-application-out validation.
7. **Application scale** — 4-node vs 32-node runs.
8. **Classifier choice** — decision tree, random forest, AdaBoost, plus baselines.

Note: "number of windows" is not a swept variable; windows slide continuously at 1 s granularity. Training-set *size* is not swept in TPDS as a sensitivity axis (it is discussed as a factor in the ISC paper's cross-testbed comparison).

### Q4 — Is the sampling interval swept? (the potentially damaging finding)

**TPDS 2019: NO.** The interval is fixed at 1 s; no figure, table, or sentence varies the collection period. Evidence depth: **FULL-TEXT** (targeted search for "collection period", "sampling period", "sampling rate", "5 s", "coarser", "granularity" returned only the two fixed-rate sentences quoted in Q2).

**ISC 2017: PARTIALLY — one two-point remark, in prose only.** Evidence depth: **FULL-TEXT.**

Verbatim, Section 6.1 ("Anomaly Detection and Classification"):
> "We also measure the impact of data collection period by increasing it to 5 s; however, the impact on classification accuracy is negligible."

Characterization: this is **not a sensitivity sweep**. It is a single 1 s → 5 s check, appearing inside a discussion of why the cloud testbed (MOC, native 5 s rate) scored lower than the Cray testbed (Volta, 1 s) — the authors eliminate candidate explanations (metric-set size, dataset size, collection period) in prose. Quality metric: classification accuracy / F-score. **No figure or table reports it, and no numeric delta is given** — only the word "negligible".

Implication for the audit: if the existing claim is "the sensitivity study varies window size, not sampling rate", that claim **survives for the TPDS 2019 paper**, cleanly. But it must not be extended to the ISC 2017 conference version without qualification: that paper does contain a one-sentence, two-point, prose-only, unquantified remark on the collection period. The honest framing is that neither paper contains a *sampling-rate sensitivity study*; the ISC version contains a passing robustness remark at a single alternative rate.

### Q5 — Any cost/overhead axis?

**Answer: YES — but it is computational/storage cost of the *analysis*, not a monitoring-collection cost sweep, and it is not crossed with sampling rate.** Expectation of "no" is therefore only partly correct.
Evidence depth: **FULL-TEXT.**

TPDS reports (Table 4 and surrounding text):
- Feature generation/selection training cost on the order of days; model training 7 minutes (decision tree) to 138 minutes (AdaBoost).
- Runtime inference cost: "Detecting and diagnosing anomalies in a single sliding window of a single node with AdaBoost and random forest takes approximately 13ms using a single thread"
- Model storage: 25 KB (decision tree) to 4 MB (random forest).
- Collection cost is cited, not measured: "State-of-the-art monitoring tools such as LDMS collect data with a sampling period of one second while using less than 0.1 percent of a core"

ISC 2017 gives a per-node normalized figure:
> "11 ms single-thread computational overhead per second...translates into 11/48 = 0.23ms computational overhead per second (0.02%) on Volta servers."

No network-bandwidth axis, no storage-volume-versus-rate axis, and no overhead-versus-sampling-rate curve in either paper.

### Q6 — Are GPUs involved?

**Answer: NO. The word GPU does not appear in either paper.** Both testbeds are CPU-only; all 721 (Volta) / 53 (MOC) metrics are CPU, memory, network, filesystem and Cray-interconnect metrics.
Evidence depth: **FULL-TEXT (verified by targeted search in both PDFs).**

### Q7 — Testbeds, and injected vs naturally observed anomalies

**Answer: injected (synthetic), on CPU-only testbeds.**
Evidence depth: **FULL-TEXT.**

- TPDS 2019: **Volta**, a Cray XC30m testbed supercomputer at Sandia National Laboratories, 52 compute nodes. Anomalies are synthetic: "To evaluate our approach with controlled experiments, we design synthetic anomalies that mimic commonly observed performance anomalies." Named injectors include `dcopy`, `dial`, `leak`, `memeater`, `linkclog`.
- ISC 2017: two testbeds — **Volta** (Cray XC30m, 52 nodes, Sandia) and **MOC**, the Massachusetts Open Cloud (Beowulf-like cluster). "Synthetic anomalies" injected into individual nodes.
- No naturally-occurring/production-labelled anomaly dataset is used in either paper. (The related HPAS anomaly suite from the same group is at https://github.com/peaclab/HPAS.)

### Tuncer ruling

Is the swept variable window size or sampling interval?

**WINDOW** — for the IEEE TPDS 2019 paper, which is the paper the claim concerns. The sensitivity study sweeps the sliding-window size (default chosen: 45 s) at a fixed 1 s sampling interval; the sampling interval is never varied there.

Qualification that must travel with this ruling: the **ISC 2017 conference version** contains one prose sentence checking a 5 s collection period against 1 s and calling the accuracy impact "negligible" — no figure, no number. That is a robustness remark, not a sampling-rate sensitivity study, but a reviewer who reads the conference version will find it, so any claim of the form "sampling rate is never touched by this line of work" should be narrowed to "no sampling-rate sensitivity *study* exists; the only datapoint is an unquantified 1 s vs 5 s prose remark in the ISC 2017 version."

---

## Access log

| Route | Target | Result |
|---|---|---|
| Crossref API `/works/10.1109/cluster49012.2020.00061` | PIKA metadata | WORKED — title, authors, pages 424–432, event Kobe Japan |
| OpenAlex record API (DOI) | PIKA metadata + OA | WORKED — authors with ZIH affiliations, pages, `best_oa_location` null (closed) |
| Semantic Scholar Graph API record (DOI) | PIKA abstract | WORKED (after one 429, retried later) — full abstract, `openAccessPdf.url` empty |
| Semantic Scholar HTML paper page | PIKA | Returned empty body to WebFetch |
| dblp record `rec/conf/cluster/DietrichWKN20.html` | PIKA | WORKED — title, authors, CLUSTER 2020, pp. 424–432 |
| dblp `rec/....xml` | PIKA | BLOCKED — robots.txt disallowed |
| dblp `db/conf/cluster/cluster2020.html` | session heading for PIKA | PARTIAL — page truncated by fetcher before reaching PIKA; only main-track session names visible ("Best Papers", "Performance Characterization and Scheduling", "Architecture and Network Support for HPC Workloads") plus a "Workshops" section |
| blogs.fau.de/prope/publications (ProPE project) | PIKA venue | **WORKED — decisive: HPCMASPA 2020 workshop, in conjunction with IEEE Cluster 2020, matching DOI** |
| ouci.dntb.gov.ua work page for the 2023 follow-up | PIKA reference string | WORKED — follow-up's own ref [5] gives the MODA/HPCMASPA-style workshop venue |
| hps.vi4io.org 2021 BoF deck (exact paper title) | PIKA rates + overhead | WORKED — 60 s LIKWID / 30 s others, both "adjustable"; "Monitoring overhead is negligible" (no numbers) |
| vi-hps.org TW44 deck (Winkler) | PIKA metrics + GPU | WORKED — GPU metrics via NVML, 30 s sampling, collectd plugins |
| compendium.hpc.tu-dresden.de/software/pika | PIKA rates + GPU | WORKED — verbatim 30 s / 60 s split, GPU metrics at 30 s per device |
| hpc.fau.de NHR-Workshop2022 Winkler PIKA deck | PIKA overhead | WORKED — GPU metrics via NVML confirmed; **no** interval and **no** overhead numbers |
| booth.zih.tu-dresden.de PIKA page | PIKA metrics | WORKED — GPU metrics listed; no rates, no overhead numbers |
| link.springer.com chapter 10.1007/978-3-031-40843-4_22 | 2023 follow-up | WORKED — full abstract; no sampling/overhead/GPU content |
| ResearchGate PIKA publication page | PIKA full text | BLOCKED — 429 on both attempts |
| core.ac.uk search | PIKA full text | BLOCKED — robots.txt disallowed |
| scholar.archive.org search | PIKA full text | BLOCKED — Archive.org rate limit |
| computer.org CSDL CLUSTER 2020 TOC | PIKA session | FAILED — page returned only metadata/verification shell, no TOC content |
| qucosa / TU Dresden FIS searches (via WebSearch) | PIKA full text | NOT FOUND — no repository copy surfaced |
| IEEE Xplore, ACM DL | both targets | NOT ATTEMPTED per constraints (known 403) |
| bu.edu/peaclab/publications | Tuncer bibliography | WORKED — verbatim entries for both versions, with PDF links |
| bu.edu/peaclab/files/2019/03/08466019.pdf | TPDS 2019 full text | **WORKED — full text, published version** |
| emreates.github.io/publications/tuncer_TPDS18.pdf | TPDS author copy | WORKED — full text, corroborates the above |
| bu.edu/peaclab/files/2020/01/isc.pdf | ISC 2017 full text | **WORKED — full text** |
| hpc.dmi.unibas.ch/research/moda | MODA editions | WORKED — MODA is ISC-co-located; MODA20 = 25 Jun 2020 Frankfurt, so ≠ the IEEE Cluster venue |

## What would settle the remaining gaps

Only the PIKA questions Q3 (quantitative overhead) and, at full rigour, Q1/Q2 as stated *in the paper* remain open. In priority order:

1. **Library request / ILL for the 9-page PDF** of DOI 10.1109/CLUSTER49012.2020.00061 (IEEE CLUSTER 2020 proceedings, pp. 424–432). This is the single step that closes everything. KISTI holds IEEE Xplore access at many institutions — a direct institutional Xplore session (not reachable from this environment) would resolve it in minutes.
2. **Email the corresponding author** — Frank Winkler (TU Dresden ZIH; contact is offered on https://booth.zih.tu-dresden.de/?page_id=46) — asking specifically: does the HPCMASPA 2020 paper report a *measured* overhead number, and if so on which benchmarks, node counts, and at which of the 30 s / 60 s intervals, including the NVML GPU plugin? Author-side confirmation would be citable as personal communication.
3. **HPCMASPA 2020 workshop website / SC-adjacent mirrors** for an author-hosted preprint or the presentation slides specific to that talk (the 2021 BoF deck found here is a different, later talk that reuses the paper title).
4. **Retry ResearchGate** (https://www.researchgate.net/publication/346596503) after the 429 window clears — the authors may have uploaded the full text there.
5. If the goal is only to protect the survey claim, **no further access is needed**: reword the claim to require an *evaluated* multi-rate perturbation measurement with a downstream analysis-quality axis. PIKA demonstrably lacks the downstream-quality axis (its own 2023 follow-up uses experience-tuned fixed thresholds), and it is a workshop paper.

For Tuncer, nothing is unresolved. The only soft spot is the exact x-axis tick list of TPDS Fig. 2 (window sizes), which PDF text extraction renders inconsistently; if the exact list is needed for a table, read Fig. 2 visually from https://www.bu.edu/peaclab/files/2019/03/08466019.pdf. The load-bearing values — 1 s fixed sampling, 45 s chosen window — are quoted verbatim and secure.

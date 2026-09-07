# V1 — Falsification Sweep: "TSDB retention/rollup resolution as a decision variable, measured against downstream analytics quality"

Sweep date: 2026-09-06
Tooling: WebSearch + WebFetch only. ACM DL and IEEE Xplore not attempted/blocked (403).
Author: V1 sub-agent (DB-venue sweep)

---

## 1. VERDICT

**`NO COUNTEREXAMPLE FOUND IN THIS SWEEP`** — with one **project-threatening partial** that the parent MUST adjudicate.

No paper was found that satisfies all four criteria simultaneously. However:

> ### ⚠️ ADJUDICATION REQUIRED: CAMEO (EDBT 2026)
> **CAMEO satisfies criteria 1, 2, and 3 fully. It fails criterion 4 only on the dataset domain.**
> It varies a downsampling ratio as an independent variable and plots **anomaly detection accuracy** and **forecasting accuracy** as functions of that ratio — in a peer-reviewed DB venue. Its data is univariate energy/environmental/UCR sensor series, **not** operational IT/HPC monitoring telemetry.
>
> If the parent's criterion 4 is read loosely ("comparable sensor streams"), **CAMEO is a counterexample and the project as literally claimed is dead**. If read strictly (operational monitoring telemetry / multivariate ops metrics), the claim survives but must be **narrowed** to say so explicitly — the generic form "nobody varies data reduction and measures detection accuracy" is **false**.

**Secondary finding that also constrains the claim:** the *methodology* (vary a data-maintenance budget → measure anomaly-detection quality on real VM telemetry) already exists in PVLDB via **RALF (PVLDB 17)**, on Azure VM telemetry. Its independent variable is a feature-refresh budget, not stored-history resolution — but a reviewer will cite it.

I can only conclude `NO COUNTEREXAMPLE FOUND IN THIS SWEEP`. I cannot and do not conclude `NO SUCH WORK EXISTS`.

---

## 2. The strongest candidate, in full

### CAMEO — the one that nearly kills it

| Field | Value |
|---|---|
| Title | *CAMEO: Autocorrelation-Preserving Line Simplification for Lossy Time Series Compression* |
| Venue | **EDBT 2026** (peer-reviewed, archival) |
| Open URL | https://openproceedings.org/2026/conf/edbt/paper-21.pdf |
| Preprint | arXiv:2501.14432 — https://arxiv.org/html/2501.14432v1 |
| Evidence depth | **FULL-TEXT** (read via arXiv HTML + EDBT PDF) |

**Criterion-by-criterion:**

| # | Criterion | Verdict | Basis |
|---|---|---|---|
| 1 | Downsampling ratio varied as IV | **SATISFIED** | Compression ratios varied "from 2 (half the points sampled) to 10 (only 1000 points sampled)", and up to 100x. Line simplification = point removal = downsampling. |
| 2 | Downstream analytical quality measured | **SATISFIED** | Anomaly detection accuracy (UCR-score, Matrix Profile detector) **and** forecasting accuracy (STL-ARIMA, STL-ETS, LSTM, DHR-ARIMA, Holt-Winters). |
| 3 | Peer-reviewed archival | **SATISFIED** | EDBT 2026. |
| 4 | Operational/monitoring telemetry or comparable multivariate sensor streams | **PARTIAL / FAILS** | ElecPower, MinTemp, Pedestrian, UKElecDem, AUSElecDem, Humidity, IRBioTemp, SolarPower + UCR anomaly archive (250 series). Sensor streams, but **univariate** and **not IT/HPC operational telemetry**. |

**Verbatim evidence (from arXiv:2501.14432 full text):**

- Figure caption: *"Figure 13: (left) Impact on the Anomaly Detection Accuracy as the Compression Ratio Increases."*
- Figure caption: *"Figure 12: Impact on Forecasting Accuracy of CAMEO and Baselines as the Compression Ratio Increases under Different Configuration, Quality Metrics, and Time Series."*
- Anomaly detection setup: *"For the first hypothesis, we use the UCR dataset [93] consisting of 250 time series and the Matrix Profile (MP) algorithm [95]."* … *"We measure the accuracy using the UCR-score [93], where higher scores indicate better detection."*
- Compression range: *"from 2 (half the points sampled) to 10 (only 1000 points sampled)"*
- From EDBT PDF: *"CAMEO consistently preserves forecasting accuracy, even under aggressive compression of 100x"*; *"CAMEO preserves the UCR score more effectively than lossy compression baselines, achieving a compression ratio of ≈ 28x while minimally impacting accuracy."*

**Why it is still not a clean counterexample:**
1. Dataset domain (criterion 4) — no operational IT/HPC monitoring telemetry; no multivariate ops metrics.
2. **Framing.** Confirmed via full text: the paper does **not** frame reduction as a retention/storage-lifecycle policy. There is no age-based tiering, no rollup schedule, no retention horizon. The decision variable is an ACF/PACF error bound inside a compressor, not "what resolution do we keep 30-day-old metrics at".
3. Downstream quality is used as a **validation that the compressor is safe**, not as the objective being optimized against a storage budget.

**Residual novelty this leaves open:** retention/rollup as an *age-tiered operational policy* decision variable, on *multivariate operational telemetry*, with *detection latency* and *root-cause/diagnosis quality* (not just detection accuracy and forecast error) as outcomes. None of those three were found together anywhere.

---

## 3. Near-misses table

Ordered by how close they come. All are legitimate related-work citations.

| Paper | Venue / Year | What it does | Which criterion it FAILS | Evidence depth |
|---|---|---|---|---|
| **CAMEO** | EDBT 2026 | Varies compression (downsampling) ratio; measures anomaly-detection UCR-score + forecasting accuracy | **4 only** (univariate energy/env/UCR data, not ops telemetry); also no retention-policy framing | FULL-TEXT |
| **RALF: Accuracy-Aware Scheduling for Feature Store Maintenance** | PVLDB 17 (2024) | Varies **update budget** + scheduling policy; measures downstream **anomaly-detection model error (MASE)** on **Azure VM telemetry** + Yahoo Webscope S5 | **1** — IV is feature-refresh/freshness budget, not stored-history resolution. Confirmed full-text: *"The paper does not discuss reducing the resolution of stored historical time series."* | FULL-TEXT |
| **Multivariate time series collaborative compression for monitoring systems…** (Miao, Li, Pan) | *J. Cloud Computing* 2024, doi 10.1186/s13677-023-00579-4 | Lossy compressed-sensing compression of **cloud monitoring metrics** (CPU load, memory, TCP segments, context switches — "KID" dataset, 4 weeks); reports anomaly-detection Precision/Recall/F1 on reconstructed vs original | **1** — anomaly detection F1 measured at a **single 30% compression ratio only**, not as a function of the reduction level. Compression ratio *is* swept, but never crossed with detection quality. Also not a DB venue. | ABSTRACT + partial FULL-TEXT via Springer |
| **Chronix: Long Term Storage and Retrieval Technology for Anomaly Detection in Operational Data** | USENIX FAST 2017 | Storage engine explicitly built *for* anomaly detection on operational data; "functionally-lossless" (drops/approximates timestamps, never values) | **1 and 2** — no retention/resolution sweep; evaluation is storage footprint, memory, retrieval and query time only. **Asserts** fidelity matters instead of measuring it: *"Chronix never drops the exact values of the data points. They always matter in the domain of anomaly detection."* — **the single best quote for the gap** | FULL-TEXT |
| **Continuous decaying of telco big data with data postdiction (TBD-DP / CTBD-DP)** | *GeoInformatica* 2019 | **Age-based retention/decay is the decision variable** — FIFO-amnesia (by tuple age), SPATIAL-amnesia, UNIFORM-amnesia; on ~10GB real telco network trace | **2** — measures only **reconstruction accuracy** + storage saved ("saves an order of magnitude storage space while maintaining a high accuracy on the recovered data"). Reconstruction error is explicitly excluded by criterion 2. | ABSTRACT + evaluation summary |
| **A Database System with Amnesia** (Kersten, Sidirourgos) | CIDR 2017 | Vision + evaluation of deliberate forgetting strategies (FIFO, uniform, anterograde, area-based, query-based "rot") | **2** — evaluation is range-query miss counts and AVG-aggregate error only; no anomaly detection, diagnosis, or ops task. Conceptually the purest "retention as decision variable" paper in a DB venue. | FULL-TEXT |
| **Remembering the Forgotten: Clustering, Outlier Detection, and Accuracy Tuning in a Postdiction Pipeline** | ADBIS 2023 | Orders outlier detection / clustering / ML in a data-decay pipeline; trades storage vs recovery accuracy | **2 and 4** — outlier detection is a *pipeline component*, not the measured outcome; outcome is recovery accuracy. Healthcare (cardiovascular) dataset. | ABSTRACT |
| **Lindorm TSDB** | PVLDB 16 (2023) | Has BOTH pre-downsampling AND in-database ML anomaly detection — but never crosses them. Downsampling assessed by query latency (−80%) and storage (+8%); Lindorm ML anomaly detection assessed by **training/inference wall-clock time only** | **1 and 2** | FULL-TEXT |
| **Monarch** (Google) | PVLDB 13 (2020) | Retention/downsampling described as a rich user-configurable policy surface | **1 and 2** — config feature, not IV; evaluation is scale, throughput, query latency percentiles | FULL-TEXT |
| **Gorilla** (Facebook) | PVLDB 8 (2015) | Fixed 26h in-memory retention; describes ODS time-based roll-up as "lossy compression that reduces data granularity" | **1 and 2** — retention fixed, never varied; evaluation is query latency (73x), throughput (14x), compression (12x) | FULL-TEXT |
| **ModelarDB** | PVLDB 11 (2018) | **Error bound varied 0/1/5/10%** — a real data-fidelity IV | **2** — outcomes are storage size, ingestion rate, query time, compression ratio, model-selection distribution. No downstream analytics task. | FULL-TEXT |
| **Timon** (SIGMOD 2020) | SIGMOD 2020 | Timestamped event DB for telemetry; production case studies mention anomaly detection and correlation analysis | **1 and 2** — no retention sweep; evaluation is write throughput and query latency vs InfluxDB/HBase/Beringei/BtrDB. Analytical functions demonstrated but never quantified | FULL-TEXT |
| **PromSketch: Approximation-First Timeseries Query at Scale** | PVLDB 18 (2025) | Sketch-based approximate caching for Prometheus/VictoriaMetrics rule (alerting) queries | **1 and 2** — sketch params fixed (k_KLL=256, k_EH=50); measures query latency, throughput, memory, MRE/KS-test error, cost. **Has no rollup/retention/downsampling knob at all.** Anomaly detection appears only as motivation citations | FULL-TEXT |
| **Mach: A Pluggable Metrics Storage Engine for the Age of Observability** | CIDR 2022 | Metrics storage engine; mentions age-based tiering to ClickHouse / S3 Glacier and fixed-point precision reduction | **1 and 2** — presented as config options; evaluation is write/read throughput and scalability only | FULL-TEXT |
| **An Experimental Evaluation of Anomaly Detection in Time Series** (Zhang et al.) | PVLDB 17 (2024) | Large factorial benchmark of TSAD methods | **1** — **confirmed the words "granularity", "resolution", "sampling rate", "downsampling", "interval" do not appear.** Varies datasets, anomaly rate (5–25%), data size (1k–100k), dimensions, anomaly patterns, window/slide size, anomaly length, thresholds — **but never temporal resolution.** This is a strong positive signal for the gap: the field's own reference benchmark omits the factor. | FULL-TEXT |
| **SEER / TSM-Bench** | PVLDB 17 / PVLDB 16 | TSDB benchmarking toolkit; includes a downsampling query (Q4) | **1 and 2** — Q4 is a workload shape, not a swept variable; measures latency, throughput, ingestion, compression | FULL-TEXT (SEER) |
| **Peregreen** | USENIX ATC 2020 | Multi-resolution/sketch index over historical time series | **1 and 2** — evaluation is upload (3M entries/s) and extraction (48M entries/s) throughput | ABSTRACT |
| **Mai et al., "Is Sampled Data Sufficient for Anomaly Detection?"** | ACM IMC 2006 | **The methodological precedent.** Varies 4 sampling methods × sampling interval N ∈ {10,20,50,100,200,500,1000}; measures volume-anomaly detection counts and port-scan Success/False-Negative/False-Positive ratios | **1 and 4 (partially)** — IV is *capture-time packet/flow sampling*, not TSDB retention/rollup; data is Tier-1 backbone packet traces, not metrics-store telemetry. Not a DB venue. **But this is the closest methodological ancestor and a reviewer will demand it be cited.** | FULL-TEXT |
| **Brauckhoff et al., "Impact of Packet Sampling on Anomaly Detection Metrics"** | ACM IMC 2006 | Companion result on how sampling distorts anomaly-detection metrics | Same as above | TITLE + open PDF located (https://conferences.sigcomm.org/imc/2006/papers/p16-brauckhoff.pdf), not read in full |
| **"Understanding and Evaluating the Impact of Sampling on Anomaly Detection Techniques"** | IEEE conference, IEEE Xplore doc 4086338. Venue believed MILCOM 2006 — **UNVERIFIED** (Xplore blocked) | Sampling → anomaly detection impact, network domain | Same class as above | TITLE-ONLY |
| **Sifter** (SoCC 2019), **Sieve**, **TracePicker**, **Tracezip**, **Hindsight**-class trace work | SoCC / EuroSys / etc. | Biased/optimization-based **trace** sampling and trace compression | **1 and 4** — IV is ingest-time trace sampling policy, data is distributed traces not metrics; outcomes are representativeness/overhead, not detection accuracy | TITLE-ONLY / snippet |
| **Self-adjusting log observability for cloud native applications** | IBM Research (venue UNVERIFIED) | Adaptive log verbosity | **1, 2, 4** — logs, and outcome is overhead/coverage | TITLE-ONLY |
| Temporal-aggregation information-loss theory (e.g. *A Spectral Measure for the Information Loss of Temporal Aggregation*, J. Stat. Theory Pract. 2020; *A review of temporal aggregation and systematic sampling on time-series analysis*, J. Accounting Lit. 2025) | Statistics / econometrics | Quantifies information loss from temporal aggregation analytically | **2 and 4** — no ops task, no telemetry. Useful as theoretical grounding for *why* rollup should hurt detection | TITLE + ABSTRACT snippet |

---

## 4. Named-system verification table

All beliefs the parent held were **verified as correct** except that Lindorm TSDB turned out to be a much closer near-miss than expected (it has both halves in one paper and still never joins them).

| System | Archival paper? | Venue/Year | Varies retention/rollup/resolution as IV? | Measures downstream analytical quality? | Evidence depth |
|---|---|---|---|---|---|
| **Monarch** | Yes | PVLDB 13, 2020 | **No** — user-configurable policy only | **No** — scale, throughput, query latency | FULL-TEXT |
| **Gorilla** | Yes | PVLDB 8, 2015 | **No** — 26h fixed; ODS roll-up described only | **No** — latency, throughput, compression | FULL-TEXT |
| **ByteSeries** | Yes | ACM SoCC 2020, doi 10.1145/3419111.3421289 | **UNVERIFIED** — ACM DL 403, ResearchGate 429. No open PDF found | **UNVERIFIED** | TITLE-ONLY |
| **TimeUnion** | Yes | ACM SIGMOD 2022, doi 10.1145/3514221.3526175 | **UNVERIFIED** — ACM DL 403; Semantic Scholar page returned empty content | **UNVERIFIED** | TITLE-ONLY |
| **ModelarDB** | Yes | PVLDB 11, 2018 | **Partially** — error bound 0/1/5/10% is a fidelity IV, but not a retention/rollup schedule | **No** — storage, ingestion, query time, compression | FULL-TEXT |
| **Timon** | Yes | SIGMOD 2020 | **No** | **No** — write throughput, query latency; analytics shown as case studies only | FULL-TEXT |
| **Lindorm TSDB** | Yes | PVLDB 16, 2023 | **No** — pre-downsampling is a feature; its effect measured as latency/storage | **No** — has in-DB anomaly detection but measures only train/inference **time** | FULL-TEXT |
| **BTrDB** | Yes | USENIX FAST 2016 | **No** — resolution is a fixed parameter (K=64 k-ary tree); multi-resolution is architecture, not a swept variable | **No** — 53M insert/s, 119M query/s, 2.9x compression, 95.93% cache hit; has an event-detection service but *"no formal evaluation of detection quality is provided"* | **FULL-TEXT** |
| **Peregreen** | Yes | USENIX ATC 2020 | **No** | **No** — upload/extraction throughput | ABSTRACT |
| **Chronix** | Yes | USENIX FAST 2017 | **No** | **No** — and it *asserts* value fidelity is necessary for anomaly detection without measuring it | FULL-TEXT |
| **Apache IoTDB** | Yes | PVLDB 13, 2020 (+ "Improving Time Series Data Compression in Apache IoTDB", PVLDB 18) | **No** (not examined in depth) | **No** (not examined in depth) | TITLE-ONLY |
| **Apache Druid** | Yes | SIGMOD 2014 (just before window) | **Not examined** | **Not examined** | TITLE-ONLY |
| **Pinot** | Yes | SIGMOD 2018 | **Not examined** | **Not examined** | TITLE-ONLY |
| **Goku** (Pinterest) | Yes | PVLDB 18(2), 2024, p503 — https://www.vldb.org/pvldb/vol18/p503-sanghavi.pdf | **No** — fully specified age-tiered rollup policy as a *fixed design choice*: *"we store the most recent 24 hours of data in-memory (GokuS) which is tier 0 for us, the last recent 80 days of data that is tier 1 to 4 in nodes with SSD storage, and 80 days to 384 days of data that is tier 5 in HDD based storage nodes."* | **No** — write throughput, read latency percentiles, annual infrastructure cost vs OpenTSDB | **FULL-TEXT** |
| **Heracles**, **ForestTI**, **AdpDM**, **STsCache**, **TSCache**, **Blink-hash**, **DecLog** | Yes (various PVLDB/PACMMOD) | 2021–2025 | **No** (storage/index/cache performance papers by title and abstract framing) | **No** | TITLE-ONLY |
| **Khronos** | Yes | CIKM 2023 | **Not examined** — indexing framework for perf-monitoring TSDBs | **Not examined** | TITLE-ONLY |
| **InfluxDB / InfluxDB IOx** | **No archival peer-reviewed paper found** | — | n/a | n/a | Search-level |
| **TimescaleDB** | **No archival peer-reviewed paper found** | — | n/a | n/a | Search-level |
| **VictoriaMetrics** | **No archival peer-reviewed paper found** | — | n/a | n/a | Search-level |
| **M3DB** | **No archival peer-reviewed paper found** | — | n/a | n/a | Search-level |
| **Thanos / Cortex** | **No archival peer-reviewed paper found** | — | n/a | n/a | Search-level |

Note: for the five vendor systems above I found only documentation and engineering blogs. Absence here is `NOT FOUND`, not proof of non-existence.

---

## 5. Venue coverage log

| Venue | Years | How enumerated | Complete? | What blocked me |
|---|---|---|---|---|
| **PVLDB / VLDB** | 2015–2026 (vols 8–19) | (a) `vldb.org/pvldb/volXX/pNNNN-*.pdf` direct fetches for every candidate identified; (b) site-restricted WebSearch on `vldb.org` with TSDB/monitoring/downsampling/anomaly query axes; (c) dblp journal pages `dblp.org/db/journals/pvldb/pvldbNN.html` | **PARTIAL** | `vldb.org/pvldb/volumes/NN/` index pages contain **only front-matter links, no titles** — the parent's assumption that these bulk-enumerate is **incorrect** for recent volumes. dblp journal pages fetch fine but WebFetch's summarizer **silently truncates**: the vol-16 fetch returned only 1 time-series title while I independently know vol 16 contains Lindorm TSDB, TSM-Bench and Blink-hash. So dblp-via-WebFetch is **not reliable for exhaustive enumeration**. Coverage of PVLDB is therefore keyword-driven, not exhaustive. |
| **SIGMOD / PACMMOD** | 2015–2026 | Targeted WebSearch by system name and topic; `2022.sigmod.org` accepted-list located but not systematically walked | **PARTIAL** | ACM DL 403 for all PACMMOD/SIGMOD full texts. Timon reached only via an author's institutional copy (users.cs.utah.edu). TimeUnion full text unreachable. |
| **ICDE** | 2015–2026 | Topic WebSearch only | **WEAK / MOSTLY UNCOVERED** | IEEE Xplore 403 with no open mirror. ICDE has no open-proceedings equivalent. **This is the largest coverage hole.** |
| **EDBT** | 2015–2026 | Site-restricted WebSearch on `openproceedings.org` across multiple query axes; direct PDF fetches | **PARTIAL but productive** | openproceedings.org fully open — this is how CAMEO was found. Not walked year-by-year exhaustively. |
| **CIDR** | 2015–2026 | dblp `conf/cidr` index for edition list; site-restricted search on `cidrdb.org`; direct PDF fetches (Kersten 2017, Mach 2022) | **PARTIAL** | `cidrdb.org/cidr2024/papers.html` returns 404 — the per-year path shape differs by year. Per-year paper lists not individually walked. |
| **SoCC** | secondary | Topic + system-name search | **WEAK** | ACM DL 403; ByteSeries unreachable |
| **USENIX ATC / FAST / NSDI** | secondary | usenix.org direct (fully open) | **PARTIAL, good depth where attempted** | usenix.org is reliable — Chronix and Peregreen retrieved here. Not systematically swept. |
| **EuroSys / OSDI** | secondary | Only via a third-party survey of observability papers 2015–2025 (eunomia.dev) | **WEAK** | Second-hand enumeration; titles not individually verified |
| **IEEE BigData, CIKM** | secondary | Not swept | **NOT COVERED** | Time; IEEE blocked |
| **Adjacent journals** | — | Followed leads into *J. Cloud Computing*, *GeoInformatica*, ADBIS, *J. Stat. Theory Pract.* | Opportunistic | Springer requires following a 302 with a cookie-error URL; that route works |

**Tooling notes for future sweeps (corrections to the brief):**
- `vldb.org/pvldb/volumes/NN/` does **not** list paper titles. Use site-restricted WebSearch on `vldb.org` instead — it surfaces the direct `pNNNN-author.pdf` files, which fetch reliably and are full text.
- dblp `db/journals/...` and `db/conf/...` pages are fetchable but WebFetch's summarizing model truncates long lists. Treat as lead generation, never as enumeration.
- openproceedings.org and usenix.org are the two most reliable full-text sources.
- Springer/link.springer.com works if you re-issue the fetch against the 302 target including the `?code=…&error=cookies_not_supported` query string.
- ResearchGate returns 429. Semantic Scholar paper pages returned empty content. crossref not needed and not used.

---

## 6. What remains unsearched (honest list)

1. **ICDE 2015–2026 — essentially uncovered.** IEEE Xplore is 403 and ICDE has no open proceedings. Any counterexample published at ICDE would have been missed. **This is the single biggest hole.** Suggested route: author homepages, arXiv, and per-year ICDE program pages if any are open.
2. **ByteSeries (SoCC 2020) and TimeUnion (SIGMOD 2022)** — verified only at title level; no open copy exists on any route I could reach (ACM DL 403, ResearchGate 429, Semantic Scholar page empty, no author-homepage copy, no arXiv preprint). Both are the exact class of system that could contain a rollup sensitivity study. **Goku was subsequently resolved to full text and is negative** (see named-system table). Priority: institutional library access or emailing the authors.
3. **Systematic year-by-year walk of SIGMOD, EDBT, and CIDR accepted-paper lists.** My coverage was keyword-driven. A title-level walk of ~12 years × 4 venues would firm up the "systematic" claim considerably and is cheap for EDBT/CIDR (both fully open).
4. **PVLDB exhaustive title enumeration.** Because dblp summarization truncated, I cannot claim I saw every PVLDB title 2015–2026. Recommend fetching each `dblp.org/db/journals/pvldb/pvldbNN.html` with a *narrow* prompt (e.g. ask only for titles containing one specific keyword, one keyword per call) to defeat truncation.
5. **CIKM and IEEE BigData** — not swept at all. CIKM in particular hosts applied monitoring/AIOps work (Khronos was found there incidentally).
6. **AIOps-specific venues outside the brief** — ISSRE, DSN, ICSE/FSE, Middleware, ICPE, ACSOS. A "how does metric granularity affect RCA" paper is arguably *more* likely in ISSRE/DSN than in a DB venue. The parent's other sweep files (C_dsn_issre_lineage.md) may already cover this — **the DB-venue result should not be read as covering it.**
7. **Detection latency as an outcome** — I probed this axis directly and found nothing archival, only vendor content. But my probing was search-phrase-based; no venue was enumerated specifically for it.
8. **Root-cause / diagnosis quality as an outcome under varied resolution** — nothing found in any venue. This appears to be the emptiest cell in the whole matrix and is the strongest residual novelty claim.
9. **Non-English literature** and **thesis/dissertation literature** — not searched.
10. **The eunomia.dev observability survey's paper list** was used second-hand; individual titles (Sieve, Snoopy, Canopy, TraceSplitter, Mirage, DMon) were not verified against their actual papers.

---

## 7. What this sweep positively establishes (for the related-work section)

Four findings are worth writing up regardless of the verdict:

1. **The field's own reference benchmark omits the factor.** *An Experimental Evaluation of Anomaly Detection in Time Series* (PVLDB 17) varies eight experimental factors and confirmed-by-full-text does not contain the words "granularity", "resolution", "sampling rate", "downsampling", or "interval". Temporal resolution is not on the community's list of things that might affect TSAD performance.

2. **The TSDB systems literature asserts the fidelity requirement rather than measuring it.** Chronix (FAST 2017) is the cleanest instance: *"Chronix never drops the exact values of the data points. They always matter in the domain of anomaly detection."* A whole storage design is justified by an unmeasured claim.

3. **The archetype of the pattern the claim describes: Goku (PVLDB 18, 2024).** Goku specifies an age-tiered retention policy in complete detail — 24h in-memory, 80 days on SSD across tiers 1–4, 80–384 days on HDD at tier 5 — and defines both mechanisms by name (*"Rollup is a write time data aggregation process that summarizes and stores time series data at higher levels of granularity"*; *"Downsampling reduces data granularity by aggregating datapoints over larger intervals"*). It then evaluates write throughput, read latency and annual infrastructure cost. The tier boundaries are stated as given. Nothing in the paper asks whether 384 days at HDD-tier granularity is enough to detect or diagnose anything. **This is the cleanest single citation for the gap.**

4. **The two halves exist in the same papers and are never joined.** Lindorm TSDB (PVLDB 16) ships pre-downsampling *and* in-database anomaly detection, evaluates the first by latency/storage and the second by wall-clock time, and never crosses them. That is the gap in a single citation.

Counterweight to be honest about: **CAMEO (EDBT 2026) and RALF (PVLDB 17) show the DB community is beginning to measure downstream analytical quality against data-management decision variables.** The window for a "nobody has ever done this" framing is closing. A framing built on *operational multivariate telemetry* + *age-tiered retention policy* + *detection latency and diagnosis quality* is defensible; a framing built on "data reduction vs. detection accuracy has never been measured" is not.

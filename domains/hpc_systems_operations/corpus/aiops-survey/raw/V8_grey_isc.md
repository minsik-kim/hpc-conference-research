# V8 — Grey/Workshop Literature on Monitoring Overhead + ISC Research Track 2024–2026

Compiled 2026-09-06. Tooling: WebSearch + WebFetch only. ACM DL / IEEE Xplore not attempted (403).
Evidence labels: `FULL-TEXT` / `ABSTRACT` / `TITLE-ONLY` / `SLIDES` / `PROGRAM-ONLY` / `METADATA` / `NOT FOUND` / `UNVERIFIED`.

---

## 0. Verdict on the narrowed GPU-overhead claim

**Claim under test:**
> "No HPC paper reports a *quantitative* monitoring-perturbation study *across multiple evaluated sampling rates* on a system with GPU (DCGM/NVML), BMC/Redfish, and high-speed-fabric telemetry, with a downstream analysis-quality axis."

**VERDICT: SURVIVES** — but it is now a *conjunction* claim held together by three independent legs, and each leg is individually broken by a different paper found in this sweep. No single work found has more than two of the four required properties (multi-rate quantitative overhead / GPU / BMC+fabric / quality axis). Two of the three strongest challengers post-date the audit's cutoff.

### The three strongest challengers

**(1) Chen, Qian, Chien, Zilberman — "Detecting Anomalies in Systems for AI Using Hardware Telemetry" (Reveal), University of Oxford, arXiv 2510.26008v2** — `FULL-TEXT`
- **Breaks the "multi-rate quantitative overhead with GPU telemetry" leg outright.** Verbatim: *"overhead decreases as the sampling interval increases: from ~1.2-1.4% at 100 ms to below 0.6% at 600 ms"*; *"under 2% across all settings and becomes negligible at moderate intervals"*. Default interval *"100 ms (configurable)"*. Window configs tested: 3 s/1 s (default), 1.5 s/0.5 s, 5 s/2 s. Storage: *"approximately 42–43 KB/s"* worst case, *"14–22 KB/s"* filtered (*"~1.2–1.9 GB/day per host"*).
- **Does NOT measure application perturbation** — only collector CPU utilisation. Confirmed on re-read: no statement that end-to-end application slowdown was measured. This is strictly weaker than DCDB/SC'19 on the perturbation axis.
- GPU telemetry: **yes**, but via `nvidia-smi` (utilisation, memory, power draw, ECC error rates), not the DCGM API.
- **No BMC/Redfish. No fabric/switch telemetry** (InfiniBand HDR100 present in hardware; no switch counters collected). Network signals are host-side only (`/proc/net/dev`, `nstat`, `ss`).
- Scale is tiny: HPC Cluster 1 = 2 nodes × 2 V100; HPC Cluster 2 = 1 node × 4 H100; local cluster = 9 servers / 99 containers. Not a production HPC system.
- Quality axis: window-granularity table shows *"hit-rate byCount mean 0.92, median 1.0"* stability across window configs, but **no accuracy-vs-sampling-rate curve**.
- Venue: arXiv preprint (Oct 2025). No venue footnote found. Also circulates as "Detecting Anomalies in Machine Learning Infrastructure via Hardware Telemetry" (ResearchGate).
- URL: https://arxiv.org/html/2510.26008v2

**(2) McDaniel, Jantz, Sharma, Abbott, Martin, Khandekar, Neth, Villasenor Alvarez, Kashi, Elwasif, Hernandez — "Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes", ISC High Performance 2026 research track, DOI 10.23919/isc.2026.11520492, arXiv 2604.06056v2** — `FULL-TEXT`
- **Breaks the "GPU-era production exascale + quantified overhead + fidelity-vs-rate reasoning" leg.**
- Overhead **measured**: *"The measured instrumentation overhead for collecting Score-P traces and polling PAPI counters is below 1%, provided that additional cores are reserved for each Score-P plugin's sampling thread."*
- Two distinct temporal granularities: on-chip `rocm-smi` sensors refresh at *"1 ms granularity"*; Cray Power Management counters *"refresh every 100 ms"*. **These are source-native rates, not a swept configuration** — no per-rate overhead table.
- Quality-vs-resolution reasoning present: deriving power as ΔE/Δt at 1 ms reveals *"short transients that moving-average sensors smooth out"*. This is the closest thing found to a fidelity-vs-rate axis on GPU-era hardware, but it is an accuracy argument, not a downstream-analysis-quality sweep.
- Telemetry: AMD GPU/APU on-chip (rocm-smi → amd-smi), node-level Cray PM counters via sysfs. **No Redfish. No fabric switch telemetry.**
- Scale: Frontier, 128 nodes / 512 MI250X; Portage, 128 nodes / 512 MI300A.
- URL: https://arxiv.org/html/2604.06056v2

**(3) Barry, Brandt, Gentile, Morrone, Roman, Scott, Shoga, Tucker — "Evaluating and Influencing Extreme-Scale Monitoring Implementations", CUG 2023 (LLNL-CONF-847852)** — `FULL-TEXT`
- **Breaks the "GPU + Redfish + fabric telemetry all present on one system" leg** — it is the only work found where all three telemetry classes co-exist.
- GPU: *"rdc_sampler – metrics for AMD GPUs"*; samplers listed for El Capitan include *"dcgm, rdc_sampler"*.
- Fabric: *"The slingshot_metrics sampler reports on a configurable set of Slingshot NIC counters. Of the potentially hundreds of counters, the sampler defaults to using a set of roughly forty."* and *"The LDMS slingshot-sited slingshot_switch sampler currently uses as its data source the HPE-provided dump_counters binary."*
- Redfish: *"hardware metrics collectors (hms-hmcollector) listen to Redfish connections and publish the hardware data to Kafka."*
- **Overhead is ASSERTED, not quantified.** Verbatim: *"Over the past decade we have proven that we can expose reasonably large quantities of such data on a fine-grained cadence (order of 1 second) with no statistically significant adverse effects on system or application performance (e.g., [1])."* and *"…while incurring no statistically significant performance penalty."* The citation is to prior CPU-era work.
- Rates are stated as defaults, not swept: *"Sampling intervals for all metric sets are 10 seconds by default but can be modified."*; El Capitan: *"Most of the samplers are currently configured to sample on a five second interval"* with some *"set to a much slower rate."*
- The one hard cost number is a *collection* cost, not a perturbation cost: *"There are over a thousand counters per port and over 64K total port counters per switch. The execution time to retrieve the full set of metrics is about half a second including nominal time for the ldmsd to parse the output and populate a metric set."*
- No node counts, no benchmarks, no quality axis.
- URLs: https://cug.org/proceedings/cug2023_proceedings/includes/files/pap149s2-file1.pdf ; OSTI mirror https://www.osti.gov/servlets/purl/1973194

### What this means for the claim's wording
The claim as worded survives. However it now survives *narrowly and by conjunction*: the honest formulation after this sweep is that **the multi-rate quantitative-overhead literature and the GPU+BMC+fabric telemetry-coverage literature are disjoint sets**, and no work in either set carries a downstream analysis-quality-versus-rate axis. Recommend restating the claim in exactly those terms rather than as a single negative existential, and explicitly citing Chen et al. and McDaniel et al. as the near misses so the claim cannot be read as ignorance of them.

**One caution on the "no HPC paper" phrasing:** Chen et al. is arXiv-only and is framed as an ML-infrastructure/cloud paper, so calling it "not an HPC paper" is defensible but contestable — two of its three testbeds are described as HPC clusters. If the audit wants the claim to be unarguable, add "peer-reviewed" and "production-scale."

---

## 1. Overhead-study comparison table

| Study | Venue / year | Hardware generation | # rates evaluated | GPU telemetry | BMC/Redfish | Fabric/switch | Perturbation: measured vs asserted | Quality axis vs rate | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| Agelastos et al., LDMS | SC'14 | CPU-era | multiple (per audit, not re-verified) | no | no | Gemini/Aries-era | measured | no | (prior audit) |
| Netti et al., DCDB | SC'19 | Skylake/Haswell/KNL | 25 configs, 100 ms–1 s | **no** (future work) | partial (IPMI/BMC via plugin) | no | **measured** (collector CPU 0.69–4.14%; up to 9% app slowdown) | no | (prior audit) |
| PIKA | HPCMASPA 2020 | GPU present (NVML) | 2 fixed (30 s / 60 s) | yes | no | no | **asserted** ("negligible") | no | (prior audit) |
| **Netti et al., DCDB Wintermute** | **HPDC 2020** | **KNL (Xeon Phi 7210-F), CooLMUC-3, 148 nodes** | **rates appear at 125 ms / 250 ms / 500 ms / 1 s / 10 s across case studies; overhead reported per case study, not swept as a single overhead experiment** | **NO — no NVML/DCGM anywhere; plugins are Perfevent, SysFS, ProcFS, OPA** | no | **yes (Intel OPA plugin)** | **measured**: *"Overhead is below 0.5% in all cases"* (query engine); *"the additional overhead of performing regression on top of standard monitoring was below 0.1% and thus negligible"*; *"always lower than 0.5% for both the HPL benchmark and the Coral-2 applications executed on 32 nodes"*; *"Average per-core CPU load of the Pusher is mostly uniform and peaks at 1.2%. Likewise, memory usage never exceeds 25MB."* | partial — power-prediction error reported at 125 ms (10.4%) and 500 ms (6.7%) vs 250 ms baseline, i.e. **an accuracy-vs-rate result exists, but CPU-era and no GPU** | `FULL-TEXT` arXiv 1910.06156v2 |
| **Chen, Qian, Chien, Zilberman — Reveal** | **arXiv 2510.26008 (preprint, Oct 2025)** | **V100 / H100 / EPYC; 2 + 1 + 9 nodes** | **multiple: 100 ms → 600 ms sweep; 3 window configs** | **yes (nvidia-smi)** | **no** | **no** | **measured — collector CPU only** (1.2–1.4% @100 ms → <0.6% @600 ms); **app slowdown NOT measured** | no (window-granularity stability only) | `FULL-TEXT` |
| **McDaniel et al.** | **ISC 2026 research track** | **MI250X (Frontier) / MI300A (Portage), 128 nodes each** | **2 native granularities (1 ms rocm-smi, 100 ms Cray PM); not swept** | **yes (rocm-smi/amd-smi)** | node Cray PM via sysfs; **not Redfish** | **no** | **measured** (<1% instrumentation overhead, with reserved cores caveat) | partial (1 ms reveals transients that averaged sensors smooth out) | `FULL-TEXT` arXiv 2604.06056v2 |
| **Barry, Brandt, Gentile, Morrone, Roman, Scott, Shoga, Tucker** | **CUG 2023** | **El Capitan / Perlmutter / Cori — GPU-era** | **defaults only (10 s default; 5 s on El Capitan); no sweep** | **yes (dcgm + rdc_sampler)** | **yes (Redfish via hms-hmcollector → Kafka)** | **yes (Slingshot NIC + switch samplers)** | **ASSERTED** ("no statistically significant adverse effects") | no | `FULL-TEXT` |
| Darzi, Pareja, Bharadwaj — Host-Side Telemetry | arXiv 2510.16946 (Oct 2025) | 4× A100, **single node**, testbed | 100 Hz eBPF + 10 Hz NVML chosen; Fig 2(a) plots overhead vs latency across eBPF rates but **specific alternative rates are not enumerated in the text** | yes (NVML) | no | **explicitly no** — *"operates without requiring cluster-wide fabric instrumentation"* | measured — collector CPU: *"1.21% CPU overhead at 100Hz sampling"*, latency ~5.1 s; other configs 0.3% / 2.3% / 1.1% | partial: detection *latency* vs rate, not detection *accuracy* vs rate | `FULL-TEXT` |
| Cankur, Kulkarni, Austin, Bhatele — Characterizing Production GPU Workloads | arXiv 2502.18680v2 | Perlmutter, 1,792 GPU nodes (A100) | **1 fixed** — *"configure the DCGM plugin to sample counters every 10 seconds on Perlmutter"*; *"users cannot change this rate"* | yes (13 DCGM counters) | no | no (NVLink/PCIe only) | **not reported** | no | `FULL-TEXT` |
| Bidollahkhani, Nordsiek, Kunkel — When GPUs Fail Quietly | arXiv 2603.28781 (Mar 2026, preprint) | GWDG, 7 GPU nodes / 28 GPUs, 353 days | **1** — *"median native sampling interval is approximately 600 s, consistent with the Prometheus scrape interval"* | yes (DCGM exporter) | no | no | **not reported** | no | `FULL-TEXT` |
| Beneventi, Libri, Bartolini, Benini — "ExaMon: Exascale Holistic Monitoring" (ANTAREX book ch. 9) | book chapter, year not stated in PDF | D.A.V.I.D.E., 45 nodes, IBM Power8 | config parameter `dT` only; **no rates evaluated** | **not addressed** | not addressed | not addressed | **not reported** | no | `FULL-TEXT` |
| Antici/Borghesi et al. — M100 ExaData | Scientific Data 10 (2023), s41597-023-02174-3 | Marconi100, *"all 980+ computing nodes"* (V100 GPUs) | *"The vast majority of metrics have timestamps expressed with the precision of one second"*; Nagios at *"15-minutes frequency"*; **no rate comparison** | yes (GPU usage; `gpu0_core_temp (IPMI)` — tool not named) | yes (IPMI) | **no InfiniBand/fabric switch counters mentioned** | **not reported** | no | `FULL-TEXT` (nature.com; PMC blocked by CAPTCHA) |
| Benini/CSCS et al. — EMOI | CUG 2024 | Alps: *"approximately 10000 Grace-Hopper GH200, in addition to the pre-existing 1000 nodes"* | *"default collection rate of 10 Hz"* for aggregate power/energy; telemetry *"around 1Hz"*; **rate discrepancy discussed, not swept for overhead** | pm_counters `accel[0,1,2,3] energy`; DCGM/NVML not named | not discussed | Kafka topic `cray-fabric-telemetry` named; **no counter list, no rate, no limits** | **not reported** | no | `FULL-TEXT` |
| Mitra et al. — CADDY | CUG 2024 | Hotlum, HPE Cray EX, 1024 nodes | rates not compared; ingest *"300K telemetry events recorded per minute"* | **no** | no | **yes** — 4 Slingshot counters (rxBW, txBW, rxCongestion, txCongestion) over *"8 groups, each containing 8 switches, which in-turn contain 64 ports each"* | ingest cost measured: *"Population of in-memory data with Caddy is slower compared to that of our current live mode (32.5%)"*; compression *"~425x, 600x, and 1200x"* at 10/15/30-min bins; query 355 ms → 151–268 ms | **no** — summarization level vs analysis quality not measured | `FULL-TEXT` |
| Srinivasan, Mallick, Maschhoff, Ayyalasomayajula — trellis | CUG 2021 | "Shandy", *"a 1024-node Cray EX developmental system"*; *"8 groups, with 16 switches per group, and 128 nodes connected at each group"* | **1** — *"captured at 1 Hz sampling rate"* | no | no | yes — *"received bandwidth - rxBW, transmitted bandwidth - txBW and average frames blocked per second – rxBlocked"* | **not reported** | no | `FULL-TEXT` |
| Friese, Marsden, Schulz — Application-Focused HPC Network Monitoring | ISC 2025 research track, DOI 10.23919/isc.2025.11018302 | multiple HPC systems (unnamed in abstract) | not stated in abstract | no | no | libfabric-layer per-process RDMA (host-side, not switch) | **ASSERTED in abstract** — *"low overhead"*, *"minimal overhead"*; full text not obtained (Xplore 403, no preprint found) | no | `ABSTRACT` (via OpenAlex) |
| Paipuri — A Unified I/O Monitoring Framework Using eBPF | MODA25 / LNCS 16091 ch. 3, DOI 10.1007/978-3-032-07612-0_3 | IDRIS/CNRS | not stated | no | no | no | **ASSERTED** — *"The results indicate that there is negligible overhead in using the framework"* | no | `ABSTRACT` (paywalled) |

### Notable negative results from the sweep
- **Wintermute is NOT a GPU-era challenger.** It has an Omni-Path fabric plugin and a genuine accuracy-vs-rate result (power-prediction error 10.4% @125 ms, 6.7% @500 ms), but there is **no mention of NVML, DCGM, or GPU metrics anywhere in the paper**, and the hardware is KNL. It strengthens the claim rather than weakening it: the one paper with both a fabric plugin and an accuracy-vs-rate axis has no GPUs.
- **ExaMon does not supply GPU-era overhead numbers.** The founding-lineage book chapter reports none; the M100 ExaData paper (Marconi100, a V100 machine) reports none either. The Marconi100 line of ExaMon papers is a **dead end for this axis**, contrary to the audit's expectation.
- **Dagstuhl Seminar 23171** ("Driving HPC Operations With Holistic Monitoring and Operational Data Analytics", DagRep 13(4):98) contains **no discussion of monitoring overhead, perturbation, sampling-rate/cost trade-offs, or GPU/fabric telemetry availability**. The nearest statement is under §10.2 challenges: *"Effective feedback and response hooks are limited or require privileged access."* This is itself a useful audit datum: the community's own agenda-setting document does not name overhead quantification as an open problem.
- **MODA25 keynote (Neuwirth, "Redefining HPC Observability")** — no overhead, sampling-rate, or literature-gap statements. `SLIDES`.
- **No Prometheus / node_exporter / DCGM-exporter overhead study in a peer-reviewed or workshop HPC venue was found.** Searches returned only vendor documentation (docs.nvidia.com), cloud-provider how-to guides, and blog posts. `NOT FOUND` — distinguish from "does not exist": Xplore and ACM DL were unreachable, and the Kubernetes/cloud-observability literature was not systematically swept.
- **No collectd/Telegraf-in-HPC overhead paper found.** `NOT FOUND`.

---

## 2. Slingshot switch-counter availability — verbatim site statements

**(a) LDMS `slingshot_switch` sampler — mechanism, counter volume, retrieval cost.** Barry/Brandt/Gentile/Morrone/Roman/Scott/Shoga/Tucker, CUG 2023, https://cug.org/proceedings/cug2023_proceedings/includes/files/pap149s2-file1.pdf :
> "The LDMS slingshot-sited slingshot_switch sampler currently uses as its data source the HPE-provided dump_counters binary."

> "There are over a thousand counters per port and over 64K total port counters per switch."

> "The execution time to retrieve the full set of metrics is about half a second including nominal time for the ldmsd to parse the output and populate a metric set."

> "We would like to work with HPE to identify more efficient port counter access mechanisms."

**(b) NIC-side counters and default subsetting** (same paper):
> "The slingshot_metrics sampler reports on a configurable set of Slingshot NIC counters. Of the potentially hundreds of counters, the sampler defaults to using a set of roughly forty."

**Interpretation:** switch counters are *obtainable* but at coarse cost. 64K counters/switch at ~0.5 s per full retrieval sets a hard floor: a full-fidelity switch sweep cannot run much faster than ~2 Hz per switch on this mechanism, and the paper's own authors ask HPE for a better path. The forty-of-hundreds NIC default is the practical operating point.

**(c) CSM/SMA fabric telemetry pipeline — Longley & Sollom, "Monitoring, Tuning, and Troubleshooting a CSM system", CUG 2024 tutorial** (`SLIDES`, https://cug.org/proceedings/cug2024_proceedings/includes/files/tut109s2-file1.pdf):
- Fabric metrics named: *"rxPausePercent, txPausePercent, rxCongestion"*, plus routing errors, hard errors, bit error rates (BER), port state and port-flap detection, rx/tx bandwidth.
- Transport: *"a common message bus (Kafka), persistence, and minimal UI infrastructure"*; topic *"cray-fabric-perftelemetry"*.
- Dashboards: *"About 20 included dashboards"* covering *"fabric telemetry, fabric performance telemetry, fabric critical telemetry, and fabric switch hardware telemetry"* — i.e. **switch hardware telemetry is a first-class exposed category, not an unavailable one**.
- Redfish/BMC sensors: *"temperature, voltage, power, energy, fan, pressure"* from ChassisBMC, NodeBMC and RouterBMC; example command `sat sensors -x [xname] -t NodeBMC -b 2 --timeout 10 --topic cray-telemetry-temperature`. Note `RouterBMC` — the switch BMC is an exposed sensor source.

**(d) CSCS/Alps — EMOI, CUG 2024** (`FULL-TEXT`): Kafka topic `cray-fabric-telemetry` is consumed, but the paper gives **no counter list, no rate and no stated limitation**.

**(e) trellis, CUG 2021** (`FULL-TEXT`, HPE): per-port switch statistics *"received bandwidth - rxBW, transmitted bandwidth - txBW and average frames blocked per second – rxBlocked"*, *"captured at 1 Hz sampling rate"* on a 1024-node Cray EX with 8 groups × 16 switches. **No statement of any counter being unavailable.**

**(f) CADDY, CUG 2024** (`FULL-TEXT`, HPE): four switch counters (rxBW, txBW, rxCongestion, txCongestion) across 8 groups × 8 switches × 64 ports; ingest *"300K telemetry events recorded per minute"*.

**(g) Not found:** **no site statement anywhere in the CUG material reached that a site was unable to obtain Slingshot switch counters.** The constraint reported is *retrieval cost and counter-set breadth*, not access denial. `NOT FOUND` for the "cannot obtain" case — with the caveat that only the CUG 2021/2023/2024/2025 monitoring tracks were swept and the CUG 2020, 2022 and 2026 tracks were not exhausted.

**(h) HPE Slingshot Host Software Administration Guide, "Telemetry Metrics and Counters" page** (support.hpe.com docDisplay) — **fetch returned an empty JS shell**. `NOT FOUND` / blocked. This is the authoritative counter list and remains unread.

**(i) Related ISC 2026 finding:** "Characterizing the Impact of Congestion in Modern HPC Interconnects" (Piarulli, Faltelli, Pleiter, Sivalingam, Zhang, Zhao, Turisini, Iannone, Artigiani, De Sensi — Sapienza / ENEA / Groningen / Huawei / CINECA; DOI 10.23919/isc.2026.11526944, arXiv 2604.11432) studies congestion on Leonardo, CRESCO8, LUMI (256 nodes each), HAICGU and a Nanjing lab system — but **collects no switch or NIC counters at all**; the method is victim/aggressor benchmark injection. It contains **no statement on switch-counter availability**. Relevant to the feasibility question as evidence that a 2026 multi-site interconnect study chose *not* to rely on switch counters.

---

## 3. Workshop series map

| Series | Editions verified | Co-located with | Where published | Archival? | Accessibility | Evidence |
|---|---|---|---|---|---|---|
| **HPCMASPA** (Monitoring and Analysis for HPC Systems Plus Applications) | 2014 Madrid, 2015 Chicago, 2016 Chicago, 2017 Honolulu, 2018 Belfast, 2019 Albuquerque, 2020 Kobe/virtual, 2021 Portland/virtual, 2022 Heidelberg, 2023 Santa Fe — from the series index page. **2024 edition evidenced indirectly**: "Evolving Large Scale HPC Monitoring & Analysis to Track Modern Dynamic Environments" (Shoga, Brandt, Schwaller, Tucker) appears in the IEEE Cluster 2024 Workshops proceedings under an "HPC Monitoring & Analysis" heading. **2025: UNVERIFIED** — no HPCMASPA heading found in the IEEE Cluster 2025 Workshops TOC reachable via dblp (fetch truncated), no 2025 site found. | IEEE Cluster | IEEE Cluster / CLUSTER Workshops proceedings (IEEE Xplore) | **Archival** | **Poor** — index and per-year Google Sites carry no paper lists; papers are behind Xplore (403). Individual papers findable only via dblp `conf/cluster/clusterw*` TOCs, which truncate under WebFetch. | `PROGRAM-ONLY` (series index https://sites.google.com/site/hpcmaspa/); `TITLE-ONLY` for the 2024 paper |
| **MODA** (Monitoring and Operational Data Analytics) | **6 editions, all verified**: MODA20 (1st, ISC 2020, Frankfurt), MODA21 (2nd, ISC 2021 digital), MODA22 (3rd, ISC 2022 Hamburg), MODA23 (4th, ISC 2023 Hamburg), MODA24 (5th, ISC 2024 Hamburg), MODA25 (6th, ISC 2025 Hamburg) | ISC High Performance | **Springer LNCS ISC "International Workshops, Revised Selected Papers"** volumes: LNCS **12321** (2020), **12761** (2021), **13387** (2022), **13999** (2023), **15058** (2024), **16091** (2025) | **Archival** | **Good** — Springer TOCs fetchable; chapter abstracts readable; full text paywalled | `FULL-TEXT` TOCs |
| **HPC-ODA** | **BoF series, not a workshop, until 2026**: SC19, ISC21, SC21, SC22, ISC23, SC23, ISC24, SC24, SC25. The **1st peer-reviewed HPC-ODA workshop is at SC26 (Chicago, 16 Nov 2026)** — submission deadline was 31 Jul 2026, so **as of today it has not yet been held and has no proceedings**. | SC and ISC | none yet (BoFs are non-archival); SC26 workshop proceedings TBD | **Non-archival to date** | Site lists events only; no BoF slides indexed on the events page | `PROGRAM-ONLY` (https://hpc-oda-org.pages.dev/events/) |
| **LDMSCON** (LDMS Users Group Conference) | **2019 Orlando, 2020 virtual, 2021 virtual, 2022 virtual, 2023, 2024 (Boston, 11–13 June), 2025** — the OVIS-HPC docs index and the LDMSCON archive page together give 2019–2025. **The audit's belief of a 2015 start is NOT supported**: the archive's earliest entry is 2019. | standalone (Sandia/OVIS community) | **Nothing** — no proceedings | **Non-archival** | **Mixed.** 2022/2023/2024/2025 sites carry tutorial recordings and downloadable tutorial bundles (`ldmscon2024_directory.zip`, `ldmscon2023_directory.zip`). But the LDMSCON2024 program page lists **titles only, no speakers**, its Presentations page is a **"TBA" placeholder**, and the actual schedule is embedded in a **Google Drawing that WebFetch cannot read**. | `PROGRAM-ONLY` |

### Full MODA chapter census (all 6 editions — 17 chapters, matching the audit's estimate)

**MODA20 — LNCS 12321, "1st International Workshop on Monitoring and Data Analytics"** (3):
1. Application IO Analysis with Lustre Monitoring Using LASSi for ARCHER — Karthee Sivalingam, Harvey Richardson (255–266)
2. AI-Driven Holistic Approach to Energy Efficient HPC — Robert Tracey, Lan Hoang, Felix Subelet, Vadim Elisseev (267–279)
3. Characterizing HPC Performance Variation with Monitoring and Unsupervised Learning — Gence Ozer, Alessio Netti, Daniele Tafani, Martin Schulz (280–292)

**MODA21 — LNCS 12761, "Second International Workshop on MODA"** (2):
4. An Operational Data Collecting and Monitoring Platform for Fugaku: System Overviews and Case Studies in the Prelaunch Service Period — Masaaki Terai, Keiji Yamamoto, Shin'ichi Miura, Fumiyoshi Shoji (365–377)
5. An Explainable Model for Fault Detection in HPC Systems — Martin Molan, Andrea Borghesi, Francesco Beneventi, Massimiliano Guarrasi, Andrea Bartolini (378–391)

**MODA22 — LNCS 13387, "3rd ISC HPC International Workshop on MODA"** (2):
6. Data Center Facility Monitoring with Physics Aware Approach — Hilary Egan, Avi Purkayastha, David Sickinger (251–261)
7. Rule-Based Thermal Anomaly Detection for Tier-0 HPC Systems — Mohsen Seyedkazemi Ardebili, Andrea Bartolini, Andrea Acquaviva, Luca Benini (262–276)

**MODA23 — LNCS 13999** (3):
8. Automatic Detection of HPC Job Inefficiencies at TU Dresden's HPC Center with PIKA — Frank Winkler, Andreas Knüpfer (295–306)
9. ML-Based Methodology for HPC Facilities Supervision — Laetitia Anton, Sophie Willemot, Sebastien Gougeaud, Soraya Zertal (307–319)
10. A Fast Simulator to Enable HPC Scheduling Strategy Comparisons — Alex Wilkinson, Jess Jones, Harvey Richardson, Tim Dykes, Utz-Uwe Haus (320–333)

**MODA24 — LNCS 15058, "5th ISC HPC International Workshop on MODA"** (2):
11. An Exascale Slurm Testing and Evaluation Environment Utilising Generated DAG Workloads — Laslo Hunhold, Stefan Wesner (273–286)
12. Challenges for Monitoring and Data Analytics in a Leadership Public Data Repository — Patrick M. Widener, Alex May, Tatiyanna Singleton, Olga Kuchar (287–292)

**MODA25 — LNCS 16091, "6th ISC HPC International Workshop on MODA"** (5):
13. Duration-Informed Workload Scheduler — Daniela Loreti, Davide Leone, Andrea Borghesi (3–14)
14. Monitoring Energy Consumption of Workloads on HPC Vega — Teo Prica, Aleš Zamuda (15–27)
15. A Unified I/O Monitoring Framework Using eBPF — Mahendra Paipuri (28–39)
16. Supporting HPC Users with LLview — Filipe Souza Mendes Guimarães, Aravind Sankaran, Wolfgang Frings (40–51)
17. What Time Taught Us: Monitoring a Computing Technology Testbed Across Multiple Years — Eva Siegmann, David Carlson, Nikolay A. Simakov, Anthony Curtis, Alan Calder, Robert J. Harrison (52–63)

**None of the 17 MODA chapters is a multi-rate monitoring-overhead study.** The closest is #15 (eBPF I/O), which asserts *"negligible overhead"* without numbers or a rate sweep.

---

## 4. ISC High Performance research track, 2024–2026

### 4.0 CRITICAL CORRECTION to the audit's venue model
**ISC research papers stopped being published as Springer LNCS after 2023.** From 2024 onward the research track is published as:
> "ISC High Performance 2024 Research Paper Proceedings (39th International Conference), Hamburg, Germany, May 12-16, 2024. **Prometeus GmbH / IEEE** 2024, ISBN **978-3-9826336-0-2**"
> "ISC High Performance 2025 Research Paper Proceedings (40th International Conference), Hamburg, Germany, June 10-13, 2025. Prometeus GmbH / IEEE 2025, ISBN **978-3-9826336-1-9**"
> "ISC High Performance 2026 Research Paper Proceedings (41st International Conference), ISC High Performance 2026, Hamburg, Germany, June 22-26, 2026. Prometeus GmbH / IEEE 2026, ISBN **978-3-9826336-2-6**"
(verbatim from dblp `db/conf/supercomputer/`, `FULL-TEXT`)

DOIs carry the prefix `10.23919/isc.<year>.<id>` and land on IEEE Xplore. **The Springer LNCS "ISC High Performance <year> International Workshops, Revised Selected Papers" volumes still exist but contain only workshop chapters, not research-track papers.** Any census that looks for ISC 2024+ research papers in Springer LNCS will find zero and must not conclude the track was empty. Enumeration was completed via **Crossref** on the `10.23919/isc.<year>` DOI prefix, cross-checked against dblp TOCs.

### 4.1 Per-year coverage statement

| Year | Edition | Proceedings | ISBN | Research papers | Enumeration completeness |
|---|---|---|---|---|---|
| 2024 | 39th | ISC HP 2024 Research Paper Proceedings, Prometeus GmbH / IEEE | 978-3-9826336-0-2 | **24** (25 Crossref items incl. one "Front Matter") | **COMPLETE.** Crossref returned 25 items on prefix `10.23919/isc.2024`; dblp TOC independently returned 23 titles, all present in the Crossref set. The Crossref set adds "Workload Scheduling on Heterogeneous Devices" (10.23919/isc.2024.10528933), which the dblp fetch truncated away. |
| 2025 | 40th | ISC HP 2025 Research Paper Proceedings, Prometeus GmbH / IEEE | 978-3-9826336-1-9 | **28** (29 Crossref items incl. "Front Matter") | **COMPLETE.** Crossref prefix `10.23919/isc.2025`. dblp fetch truncated at 11 titles; all 11 are in the Crossref set. |
| 2026 | 41st | ISC HP 2026 Research Paper Proceedings, Prometeus GmbH / IEEE | 978-3-9826336-2-6 | **35** (36 Crossref items incl. "Front Matter") | **COMPLETE.** Crossref prefix `10.23919/isc.2026`. dblp fetch truncated at 10 titles; all 10 are in the Crossref set. |

Note: the ISC **workshops** volumes for these years (LNCS 15058 / 16091 and 10.1007/978-3-031-73716-9) hold 35 and 54 chapters respectively and are a separate corpus — do not merge counts.

### 4.2 Relevant research-track papers (ops / monitoring / telemetry / ODA / reliability / anomaly / RCA / power-energy-cooling / scheduling analytics)

#### ISC 2024 — 4 of 24 relevant
| Title | Authors | Affiliations | DOI | Relevance / content | Evidence |
|---|---|---|---|---|---|
| Power Consumption Trends in Supercomputers: A Study of NERSC's Cori and Perlmutter Machines | Ermal Rrapaj, Sridutt Bhalachandra, Zhengji Zhao, Brian Austin, Hai Ah Nam, Nicholas J. Wright | LBNL/NERSC | 10.23919/isc.2024.10528943 | **Power/energy analytics on a GPU system.** Longitudinal power-consumption study across a CPU-era (Cori) and a GPU-era (Perlmutter, A100) machine. Directly on the power-analytics axis; full text not obtained. | `TITLE-ONLY` + `METADATA` |
| EcoFreq: Compute with Cheaper, Cleaner Energy via Carbon-Aware Power Scaling | Oleksiy M. Kozlov, Alexandros Stamatakis | Heidelberg Institute for Theoretical Studies (per dblp author record; not independently confirmed) | 10.23919/isc.2024.10528928 | Carbon/energy-aware power scaling — energy analytics + control. | `TITLE-ONLY` |
| TinyProf: Towards Continuous Performance Introspection through Scalable Parallel I/O | Ke Fan, Suraj Kesavan, Steve Petruzza, Sidharth Kumar | Univ. of Alabama at Birmingham / Utah State (per dblp; not independently confirmed) | 10.23919/isc.2024.10528932 | **Continuous performance introspection** — closest ISC 2024 paper to the monitoring-infrastructure axis. Worth a full-text pass for any overhead numbers; not obtained here. | `TITLE-ONLY` |
| Workload Scheduling on Heterogeneous Devices | not obtained | not obtained | 10.23919/isc.2024.10528933 | Scheduling analytics. Present in Crossref, absent from the truncated dblp fetch. | `TITLE-ONLY` |
| *(marginal)* Calibration and Performance Evaluation of a Superconducting Quantum Processor in an HPC Center | Xiaolong Deng, Stefan Pogorzalek, Florian Vigneau, Ping Yang, Martin Schulz, Laura Brandon Schulz | TUM / LRZ | 10.23919/isc.2024.10528924 | Operational characterisation of an accelerator inside an HPC centre; only tangentially on the ops-telemetry axis. | `TITLE-ONLY` |

#### ISC 2025 — 8 of 28 relevant
| Title | Authors | Affiliations | DOI | Relevance / content | Evidence |
|---|---|---|---|---|---|
| **Refine: A Robust Approach to Unsupervised Anomaly Detection for Production HPC Systems** | Efe Sencan, Yin-Ching Lee, Connor Casey, Benjamin Schwaller, Vitus J. Leung, Jim Brandt, Brian Kulis, Manuel Egele, Ayse K. Coskun | Boston University; Sandia National Laboratories | 10.23919/isc.2025.11018307 | **Most relevant ISC 2025 paper.** VAE-based unsupervised anomaly detection robust to contaminated training data. LDMS telemetry at **1 Hz**; 806 metrics on Eclipse, 721 on Volta, reduced to 156 node-level metrics. Eclipse = 1,488 nodes / 53,568 cores; Volta = 52-node Cray XC30m. **No GPU telemetry** — authors state *"extending Refine's applicability to a broader range of real-world workloads, including GPU-accelerated applications, is an important direction."* **No overhead reported. No rate comparison.** | `FULL-TEXT` (author copy: https://www.bu.edu/peaclab/files/2025/04/Refine_ISC-HPC_camera_ready-version.pdf) |
| **Application-Focused HPC Network Monitoring** | Philipp A. Friese, Olivier Marsden, Martin Schulz | Technical University of Munich; European Centre for Medium-Range Weather Forecasts | 10.23919/isc.2025.11018302 | **Fabric/network monitoring.** libfabric-layer tool giving *"per-process monitoring"* of RDMA communication, *"model agnostic"*, production-capable. Overhead **asserted** as *"low overhead"* / *"minimal overhead"* across multiple HPC systems; **no numbers obtained** (Xplore 403, no preprint located). Host-side, **not switch counters**. | `ABSTRACT` (OpenAlex) |
| Telemetry for Quantum Systems in HPC Centers | Hossam Ahmed, Burak Mete, Helmut Heller, Matthew Tovey, Xiaolong Deng, Asim Zulfiqar, Muhammad Nufail Farooqi, Mahmoud Abuzayed, Martin Schulz, Laura Brandon Schulz | TUM / LRZ | 10.23919/isc.2025.11018264 | **Telemetry infrastructure** — extends HPC-centre monitoring to QPUs. Relevant as a telemetry-architecture paper; classical-side rates/overhead not obtained. | `TITLE-ONLY` |
| Energy-Efficient GPU Allocation and Frequency Management in Exascale Computing Systems | not obtained | not obtained | 10.23919/isc.2025.11018306 | Power/energy analytics + GPU control on exascale systems. | `TITLE-ONLY` |
| Maximizing Power-Constrained Supercomputing Throughput | not obtained | not obtained | 10.23919/isc.2025.11017728 | Power-constrained scheduling/throughput analytics. | `TITLE-ONLY` |
| Job Scheduler-Driven Power Gateway for High Performance Computing | not obtained | not obtained | 10.23919/isc.2025.11018319 | Scheduler↔power-infrastructure coupling — ops control loop. | `TITLE-ONLY` |
| UoPC: A User-Based Online Framework to Predict Job Power Consumption in HPC Systems | not obtained | not obtained | 10.23919/isc.2025.11017729 | **Online power prediction from operational data** — ODA/prediction axis. | `TITLE-ONLY` |
| *(marginal)* A Performance Analysis of Task Scheduling for UQ Workflows on HPC Systems | Chung Ming Loi, Anne Reinarz, Linus Seelinger, William Hornsby, James Buchanan, Mikkel Bue Lykkegaard | Durham Univ. et al. (per dblp) | 10.23919/isc.2025.11018268 | Scheduling analytics for workflows; application-level rather than system-ops. arXiv 2503.22645. | `TITLE-ONLY` |

#### ISC 2026 — 9 of 35 relevant (the richest year on this axis by a wide margin)
| Title | Authors | Affiliations | DOI | Relevance / content | Evidence |
|---|---|---|---|---|---|
| **Fine-Grained Power and Energy Attribution on AMD GPU/APU-Based Exascale Nodes** | Adam McDaniel, Michael Jantz, Ashesh Sharma, Steve Abbott, Steven Martin, Shreyas Khandekar, Brandon Neth, Bruno Villasenor Alvarez, Aditya Kashi, Wael Elwasif, Oscar Hernandez | Univ. of Tennessee; HPE; AMD; ORNL (UT-Battelle notice on manuscript) | 10.23919/isc.2026.11520492 | **See §0 challenger (2).** GPU-era exascale power/energy telemetry with a **measured <1% instrumentation overhead** and a 1 ms vs 100 ms fidelity argument. Frontier 128 nodes / 512 MI250X; Portage 128 nodes / 512 MI300A. Sources: rocm-smi/amd-smi + Cray PM counters via sysfs. No Redfish, no fabric. | `FULL-TEXT` arXiv 2604.06056v2 |
| **Characterizing the Impact of Congestion in Modern HPC Interconnects** | Lorenzo Piarulli, Marco Faltelli, Dirk Pleiter, Karthee Sivalingam, Dancheng Zhang, Kexue Zhao, Matteo Turisini, Francesco Iannone, Aldo Artigiani, Daniele De Sensi | Sapienza Univ. of Rome; ENEA; OEHI/Univ. of Groningen; Huawei; CINECA | 10.23919/isc.2026.11526944 | **Interconnect/congestion characterisation across 5 systems** (Leonardo 256 nodes, CRESCO8 256, LUMI 256, HAICGU 4–10, Nanjing lab 8). Method is victim/aggressor benchmark injection — **no NIC or switch counters collected, no overhead statement**. Notable for the feasibility question: a 2026 multi-site fabric study that deliberately avoided switch telemetry. | `FULL-TEXT` arXiv 2604.11432v1 |
| **Instruction-Tuned LLMs for Parsing and Mining Unstructured Logs on Leadership HPC Systems** | Ahmad Maroof Karimi, Jong Youl Choi, Charles Cao, Awais Khan | ORNL (OLCF; DE-AC05-00OR22725) | 10.23919/isc.2026.11520489 | **Log analytics / RCA on a leadership system.** Instruction-tuned LLMs for unstructured log parsing and mining. arXiv 2604.05168. | `TITLE-ONLY` + `METADATA` (arXiv abs fetch hit a 429; not re-read) |
| **EPIC: Accelerating Iterative Analytics in HPC Operations with Orchestrated Multi-Agent Systems** | Ahmad Maroof Karimi, Woong Shin, Jesse Hines, Tirthankar Ghosal, Naw Safrin Sattar, Feiyi Wang | ORNL | 10.23919/isc.2026.11520478 | **Directly an operational-data-analytics paper** — agentic orchestration for iterative HPC-operations analytics. Highest-relevance ISC 2026 ODA paper. | `TITLE-ONLY` |
| **Understanding Large-Scale HPC System Behavior Through Cluster-Based Visual Analytics** | Allison Austin, Shilpika, Yan To Linus Lam, Yun-Hsin Kuo, Venkatram Vishwanath, Michael E. Papka, Kwan-Liu Ma | Argonne National Laboratory; Univ. of California, Davis (per author set) | 10.23919/isc.2026.11520496 | **System-behaviour analytics from operational data**, visual-analytics framing. | `TITLE-ONLY` |
| **A Dynamic GPU Power Prediction Framework for Production HPC Applications** | Fatih Acun, Zhengji Zhao, Ermal Rrapaj, Brian Austin, Ayse K. Coskun, Nicholas J. Wright | Boston University; LBNL/NERSC | 10.23919/isc.2026.11520502 | **GPU power prediction on a production system** (NERSC lineage → almost certainly Perlmutter). Power analytics + GPU telemetry; a likely place to look for DCGM sampling-rate discussion. **Recommended for a follow-up full-text pass.** | `TITLE-ONLY` |
| **Icicle: Scalable Metadata Indexing and Real-Time Monitoring for HPC File Systems** | Haochen Pan, Ryan Chard, Song Young Oh, Maxime Gonthier, Valérie Hayot-Sasson, Geoffrey Lentner, Joe Bottigliero, Rachana Ananthakrishnan, Kyle Chard, Ian Foster | Univ. of Chicago; Argonne; Purdue (per author set) | 10.23919/isc.2026.11520501 | **Real-time monitoring** of file-system metadata at scale — monitoring-infrastructure axis (storage tier). | `TITLE-ONLY` |
| A Scheduler System for Interactive Visualization on HPC Resources | Ali Zamani, Yathu Sivarajah, Maciej Cytowski, Ugo Varetto | Pawsey Supercomputing Research Centre (per author set) | 10.23919/isc.2026.11520479 | Scheduling systems/analytics for interactive workloads. | `TITLE-ONLY` |
| An Empirical Evaluation of Quantum-Inspired QUBO Methods for Heterogeneous HPC Workflow Mapping and Scheduling | not obtained | not obtained | 10.23919/isc.2026.11520475 | Scheduling analytics (mapping/scheduling optimisation). | `TITLE-ONLY` |
| *(marginal)* VoltanaLLM: Energy-Efficient and SLO-Aware Disaggregated LLM Serving via Adaptive Frequency Control and State-Space Routing | not obtained | not obtained | 10.23919/isc.2026.11520495 | Energy analytics + frequency control, but LLM-serving rather than HPC operations. | `TITLE-ONLY` |
| *(marginal)* Training Foundation Models on a Full-Stack AMD Platform: Compute, Networking, and System Design | not obtained | not obtained | 10.23919/isc.2026.11520488 | System/network design experience report; may contain operational telemetry. | `TITLE-ONLY` |

**Trend worth recording for the audit:** ISC's research track went from 4/24 relevant (2024) to 8/28 (2025) to 9/35 (2026), with 2026 adding two ORNL operations-analytics papers (EPIC, log mining) and a GPU power-prediction paper — i.e. **the ops/ODA topic is now established in ISC's archival research track, not only in its workshops.** Any claim that ISC lacks ops-analytics research papers is no longer true for 2025–2026.

---

## 5. What remains unsearched or blocked

**Hard-blocked:**
1. **IEEE Xplore** (403) — all HPCMASPA papers, all ISC 2024–2026 research-paper full texts. Only Crossref/OpenAlex metadata and author preprints were reachable. The two highest-value unread full texts are **"Application-Focused HPC Network Monitoring"** (ISC 2025 — asserts low overhead; needs its numbers checked) and **"A Dynamic GPU Power Prediction Framework for Production HPC Applications"** (ISC 2026).
2. **ACM DL** (403, not attempted) — HPDC 2020 Wintermute canonical version (worked around via arXiv 1910.06156v2, which is the v2 preprint, not the camera-ready; the overhead numbers quoted here are from the preprint).
3. **support.hpe.com** — the "Telemetry Metrics and Counters" page of the HPE Slingshot Host Software Administration Guide returned an empty JS shell. **This is the authoritative Slingshot counter list and remains unread.** It is the single most valuable remaining target for the Slingshot feasibility question.
4. **computer.org CSDL** — JS-rendered; the IEEE Cluster 2025 Workshops TOC could not be read, so **whether HPCMASPA 2025 happened is UNVERIFIED**.
5. **PMC** (pmc.ncbi.nlm.nih.gov) — CAPTCHA. Worked around via nature.com for M100 ExaData.
6. **dblp TOC pages truncate under WebFetch** at roughly 10–23 entries regardless of prompt, and `?view=bibtex` plus the `dblp.uni-trier.de` mirror are robots-disallowed intermittently. Crossref DOI-prefix queries were the reliable substitute. **Recommend Crossref-prefix enumeration as the standard method for any future ISC-year census.**
7. **isc-hpc.com attendee-manual and 2025.isc-hpc.com/program/** — HTTP 401. No ISC program-site enumeration was possible.

**Not exhausted (searched but not swept to completion):**
8. **CUG 2020, 2022 and 2026 proceedings** — only 2021, 2023, 2024, 2025 monitoring tracks were swept. CUG 2026 would have been held mid-2026 and may contain newer Slingshot 400 telemetry material; the CUG 2025 paper "The HPE Slingshot 400 Expedition" (Azgomi, Roweth, Faanes, Treger) was identified but **not read**, and is a plausible source of counter-availability statements for the next-generation fabric.
9. **HPCMASPA per-paper enumeration for any year.** The series index gives locations only. A complete HPCMASPA census requires Xplore or per-year agenda pages that the Google Sites do not expose.
10. **LDMSCON talk-level content for every year.** The 2024 schedule is inside an unreadable Google Drawing and the Presentations page is a "TBA" placeholder; 2019–2023 and 2025 sites were not individually opened. **No GPU-era multi-rate overhead talk was found, but LDMSCON is the most likely remaining home for one** — it is the venue where LDMS overhead is discussed by practitioners, and it is non-archival, so absence of a search hit is weak evidence. Recommend a human pass over the LDMSCON 2023–2025 tutorial bundles.
11. **Kubernetes/cloud-observability literature on DCGM-exporter and Prometheus overhead.** Only vendor docs and blogs surfaced. If the audit wants to close the "Prometheus/DCGM-exporter overhead" sub-question properly, that corpus (SoCC, Middleware, IEEE Cloud, USENIX ATC) needs its own sweep.
12. **`collectd` / Telegraf overhead in HPC** — `NOT FOUND` in this sweep; not exhaustively searched.
13. **ExaMon's DATE 2017 founding paper** was **not located as a DATE paper.** The searches surfaced the ANTAREX book chapter (Beneventi, Libri, Bartolini, Benini, "Chapter 9. ExaMon: Exascale Holistic Monitoring") and the ExaMon project site and GitHub, plus follow-ups (M100 ExaData; "Continuous learning of HPC infrastructure models…"; "Paving the Way Toward Energy-Aware and Automated Datacentre", ICPP-W 2019 — the last two **unread**, ACM DL blocked). **The audit's "DATE 2017 origin" belief is UNVERIFIED** — treat as unconfirmed rather than false.
14. **arXiv 2510.27664 (Kestrel)** — "Rethinking Telemetry Design for Fine-Grained Anomaly …" is about **5G user planes and datacenter networks with programmable switches**, not HPC. It reports *"10% better detection accuracy"* while *"reducing export bandwidth by 10x"* — a genuine quality-vs-telemetry-budget result, but out of the HPC scope of the claim. Metadata (authors, date) not obtained. Flagged in case the audit wants a cross-domain comparison point.
15. **"When GPUs Fail Quietly"** (arXiv 2603.28781, Bidollahkhani, Nordsiek, Kunkel, GWDG) is a preprint with **no venue found** — worth re-checking later in 2026 for a venue, as it is squarely on the GPU-failure-prediction axis (7 GPU nodes / 28 GPUs / 353 days, DCGM exporter at ~600 s scrape interval).

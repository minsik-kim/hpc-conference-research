# Corrections to the Phase-1 Venue Map and Research Queue

**Compiled 2026-09-17** by the six-venue Phase-2 census.

## 0. Why this file exists instead of edits to the Phase-1 documents

The Phase-1 source project (`../quantum-hpc-survey/`) was imported into this repository
**byte-identically**, and `domains/hpc_quantum/RESEARCH_STATUS.md`, `SOURCE_MANIFEST.md` and
`STAGING_CHECKSUMS.sha256` all assert that property. Editing those files in place would silently
invalidate the checksums and the preservation claim, which `governance/KNOWLEDGE_BASE_RULES.md`
ranks above structural tidiness ("preservation > structural migration > indexing > stylistic
cleanup").

**So the Phase-1 files are left untouched, and this file is the authority wherever the two disagree.**
The domain-level retrieval layer (`TOPIC_MAP.md`, `RESEARCH_STATUS.md`, `DOMAIN_CONTEXT.md`,
`topics/*.md`, `implementation/ARTIFACT_REGISTRY.md`, `research/CANDIDATE_QUESTIONS.md`) has been
updated to point here, and `domains/hpc_quantum/CHANGELOG.md` records the supersession.

## 1. Corrected counts

| Venue-year | Phase-1 figure | Census figure | Basis |
|---|---:|---:|---|
| **ICS 2024** | **0** ("none found by keyword sweep", explicitly not a counted zero) | **1** | *Minimizing Coherence Errors via Dynamic Decoupling*, `10.1145/3650200.3656617`, pp. 164–175, Session 5A "Reliability, Dependability and Availability". Found by hand-scanning all 45 titles in the page-tiled volume. **Neither its title nor its session name contains "quantum"** — it is named after its technique. |
| **ISC 2024** | 5 | **6** | Independent reconstruction of the 24-paper volume. The extra paper is *What is Quantum Parallelism, Anyhow?* (Markidis, KTH), a judgement call recorded with its reasoning in `CENSUS_ISC_2024_2026.md`. |
| **HPCA 2026** | 8 | **9** | *Advancing Full-Stack Acceleration for Schrödinger-Style Quantum Simulation* (Imperial), `10.1109/HPCA68181.2026.11408466`, sits **outside both dedicated quantum sessions** and was missed by a session-based sweep. |
| **ISCA 2026** | 12 (with a note that the strict count is 11) | **11** | **SATIC** independently confirmed to be a **classical CMOS/oscillator Ising-machine compiler**, despite sitting in the session named "Quantum 3". The Phase-1 note was right; this census confirms it from the authors' own publication list. |
| ISCA 2024 / 2025 | 6 / 16 | **6 / 16** | Independently reproduced. |
| HPCA 2024 / 2025 | 1 / 7 | **1 / 7** | Independently reproduced, including the Best-of-CAL exclusion that keeps 2024 at 1 rather than 2. |
| MICRO 2024 / 2025 | 3 / 8 | **3 / 8** | Independently reproduced. |
| ICS 2025 / 2026 | 2 / 5 | **2 / 5** | Independently reproduced. |
| ISC 2025 / 2026 | 3 / 4 | **3 / 4** | Independently reproduced (2026 also yields one `BORDERLINE`). |

**Denominators are new information in every case.** Phase 1 recorded relevant-paper counts but not
verified populations; this census supplies both, with method and verification tags. Notably, the
Phase-1 venue map's ISCA/MICRO/HPCA counts were flagged in the source itself as produced by a
program-based method that the ASPLOS census showed undercounts. **For the relevant-paper numerator
that method turns out to have held up well** — four of six venues reproduce exactly. The undercount
risk was real for *denominators*, not for the quantum subsets, which are small and concentrated in
named sessions.

## 2. Corrected characterizations

**★ Flag-Proxy Networks (MICRO 2024) is not "QLDPC decoding hardware".**
Phase 1 describes MICRO's quantum work as including "QLDPC decoding hardware (Vegapunk …;
Flag-Proxy Networks, Georgia Tech/IBM)". Vegapunk is indeed a decoder accelerator. **Flag-Proxy
Networks is not.** Code cross-validation against the first author's framework found **zero HDL** —
no `.v`, `.sv`, `.vhd`, `.xdc` or `.tcl` anywhere — and decoders implemented purely in software
(`src/qontra/decoder/{mwpm,pymatching,restriction,…}.cpp`) over modified Stim and PyMatching. The
"hardware" in FPN is a **qubit connectivity architecture** (degree reduction via flag and proxy
qubits, `enum class type { data, xparity, zparity, flag, proxy }`) plus a greedy syndrome-extraction
scheduler. It should be classified as **architecture + scheduling, evaluated by software simulation**.
See `DEEPDIVE_QEC_DECODING.md` §7.

**DC-MBQC (HPCA 2026) is Peking University + CUHK, not ICT CAS.** Phase 1 attributes it to ICT CAS.
Bibliographic sources give Yecheng Xue, Rui Yang, Tongyang Li (PKU) and Zhiding Liang (CUHK).

**TuniQ (ICS 2026) is a Utah–Rice collaboration, not Rice.** First author Mohammad Abrarul Hasanat
and co-author Rohan Basu Roy are at the University of Utah.

**Vegapunk's full title includes a subtitle the Phase-1 record omits:** *"…with Online Hierarchical
Algorithm and Sparse Accelerator"*.

**Pinball's title is "…for Surface Code Decoding Under Circuit-Level Noise"**, not "QEC Decoding".

**HATT (HPCA 2025) has a real program↔proceedings title discrepancy:** the proceedings say
"Hamiltonian **Adaptive** Ternary Tree", the official program prints "Hamiltonian **Aware**".

**OneAdapt (MICRO 2025) circulates under three different titles** — program, proceedings and arXiv all
differ. The proceedings title is authoritative: *"OneAdapt: Resource-Adaptive Compilation of
Measurement-Based Quantum Computing for Photonic Hardware"*.

## 3. Corrected or contextualized quantitative claims

These are numbers that circulate in the domain without the qualifiers that make them meaningful.
`governance/SOURCE_EVIDENCE_RULES.md` requires the qualifiers to travel with the number.

| Claim as circulated | Correct statement |
|---|---|
| Pinball reduces syndrome bandwidth **3780.72×** | **at d = 5, p = 10⁻⁴**, versus no predecoding. Not at d = 21, not at p = 10⁻³. |
| Pinball achieves **32.58×** lower logical error rate than Promatch | **at d = 11, p = 5×10⁻⁴**, under **SI1000** noise, and under far stricter power and area constraints. (The abstract says 32.58×; one body sentence read 32.38× — `INSUFFICIENT_EVIDENCE` on which is correct.) |
| SWIPER evaluates **d = 13 to 31** | d = 13–31 is the **PyMatching latency-characterization** range. The system benchmark sweep is **d ∈ {15, 21, 27}** and the reaction-time sweep is **d = 21 alone**. |
| ZAC improves fidelity **22×** | 22× is **versus Enola**; the paper also reports **13,350× versus Atomique**. An earlier note framed the 22× as "zoned vs monolithic architectures", which is not the paper's comparison. |
| MonteQ cuts CNOTs by up to **53% (mean 30%)** vs Rustiq | the abstract's figure; the paper body reports **51.6% max / 23.5% mean** at one iteration and **60.2% / 27.2%** at 200 iterations. Both recorded; `INSUFFICIENT_EVIDENCE` on the intended reading. Also the arXiv id is **2604.19029**, not 2605.11375. |
| Qoncord is **17.4×** faster | wall-clock including queue delays, for comparable-quality solutions, versus a single-device high-fidelity-only baseline, under a 1,000-job synthetic workload on **10 synthetic devices with simulated noise models — no real QPU execution**. |
| MILQ improves makespan by **26%** | versus a **bin-packing** baseline scheduler, on three 5-qubit Qiskit fake devices. |
| gladiator needs **10 LUTs per data qubit** and **70 LUTs at d = 25** | both are true only together with ~**100× time-multiplexing** (`10 × ⌈625/100⌉ = 70`): 10 LUTs serve 100 data qubits, each evaluated in 1 ns inside the 100 ns budget. Read literally, the per-qubit figure would imply 6,250 LUTs. |
| Coset Ensemble Decoder achieves **8.2× fewer LUTs** on FPGA | versus **reported** UF-decoder resources in the literature, not a head-to-head re-synthesis — and **the repo's `hardware_code/` is empty (`.gitkeep` only)**, so the claim is not reproducible from the artifact. Its modality is **CYCLE_SIMULATION**, not FPGA_PROTOTYPE. |
| The DD ring simulator is **26×** faster | **38-qubit Shor, 256 nodes, ring + SWAP-variant v1, versus single-node** (3,881 s → 147 s). The same paper reports 20-qubit QCBM getting **slower** beyond 64 nodes. |

## 4. Confirmed Phase-1 findings (no change)

- **HPCA 2024 is a non-year**: 1 main-track quantum paper, no dedicated session, and the "Best of CAL"
  trap does inflate it to 2 if not excluded. Confirmed exactly.
- **SuperCore (MICRO 2024) and SuperSFQ (MICRO 2025) are classical superconducting processors**, not
  quantum. Confirmed from both abstracts. MICRO 2025 itself runs a separate "Superconducting Systems"
  session, so the venue draws the same line.
- **MICRO has no classical-simulation quantum papers** in 2024 or 2025. Confirmed by whole-volume scan.
- **ICS 2026's "Parallel Quadratic Selected Inversion in Quantum Transport Simulation" is classical
  NEGF** and is not in the quantum session. Confirmed twice.
- **ICS 2026's SpinTune is quantum sensing**, not quantum computing. Confirmed; excluded and logged.
- **ISC 2024's VASP eigensolver paper and ISC 2025's vector-annealing paper** are false positives.
  Confirmed.
- **FTQCSA 2025 is a workshop co-located with ISCA 2025**; zero leakage into the main program.
  Confirmed against the full 135-item program.
- **MICRO-59 (2026) program was not public** as of 2026-09-06. **Re-verified 2026-09-17: still not
  public**, with camera-ready due 11 September 2026 — six days before this census. Four independent
  probes.

## 5. New venue-level facts Phase 1 did not have

- **ISCA's industry track is archival** at all three venues (industry papers occupy full page ranges
  inside the same proceedings block); so is HPCA's in 2024–2025. No industry paper in either venue is
  quantum-related.
- **HPCA 2026 uses per-article pagination**, which makes page-tiling verification structurally
  impossible for that year, and its publisher-TOC mirror is **incomplete by at least two papers**.
- **ACM article-ID contiguity is not a valid completeness proof** — suffixes are not ordered by page
  or program position. It works for IEEE volumes (ISC, ISCA 2024/2026), where IDs follow program
  order exactly.
- **IEEE QSW's category structure differs in every year**: invited-symposium papers bound into the
  *front* of the 2024 volume; four non-QSW sibling-conference papers bound into the *back* of the 2025
  volume; explicit `QSW_REG_`/`QSW_SHT_` program IDs in 2026. And the **7-page boundary band is
  irreducibly ambiguous** between regular and short, covering up to a fifth of the population.

# Independent Verification Pass — multi-venue-census-2026

**Performed 2026-09-17, after the census drafts were complete**, as a separate adversarial audit
rather than a final formality. Instruction to the auditor was explicit: *find errors, not
confirmation; a pass that finds nothing is more likely lazy than correct.*

## Coverage

All 12 census files read in full; both Phase-1 comparison censuses (SC 2024–2025, ASPLOS 2024–2026)
read for the cross-venue claims; **12 DOIs independently resolved**; **22 GitHub repositories, 1
GitLab project and 4 Zenodo records probed**; **11 specific code claims re-verified directly in the
cloned repositories**; a full forbidden-vocabulary grep; and every arithmetic aggregate recomputed.

## Material errors found and fixed

| # | Error | Fix applied |
|---|---|---|
| **1** | **QSW 2024's regular-paper denominator was wrong.** The row read 21 volume items = 18 main-track + 4 excluded, which is arithmetically impossible (18 + 4 = 22 ≠ 21). Re-enumeration under the census's own banding rule gives REGULAR **13**, not 14. | Denominator 14 → **13**; QSW total 48 → **47**; **census total 1,282 → 1,281**; 2024 rate 43% → 46%; QSW overall 41.7% → 42.6%; the quantum-SE exclusion table 14/8/57% → 13/7/54% and total 48/28/≈58% → 47/27/≈57%; "3 of 18 main-track items" → "3 of 17". The 7.96% headline survives (102/1281 = 7.96%). |
| **2** | **The SC cell in the QEC row was a bare `0`, dropping a qualifier the Phase-1 census insists on.** SC's own census records one *QEC reliability characterization* paper (SC24's surface-code radiation study) and is explicit that SC takes reliability characterization but not decoder systems. Since the synthesis's own taxonomy counts MICRO's Surf-Deformer (defect tolerance) inside QEC, consistency requires the SC cell to carry the same qualifier. This sat directly under the corpus's most load-bearing finding. | Cell → **"0 decoder papers (1 QEC reliability characterization)"**; note 2 and candidate M9 rewritten to carry the qualifier; the ASPLOS cell additionally split to note that its decoder-microarchitecture line is only two papers (Promatch 2024, Micro Blossom 2025) and has since moved to ISCA. |
| **3** | Genesis benchmark count: "19 `.ham` benchmarks". `find` returns **20**. | Corrected in two files. |
| **4** | ZAC: "calls `min_weight_full_bipartite_matching` at four sites". Actually one import and **two call sites** (lines 293, 502). | Corrected. |
| **5** | MICRO: "three of the eleven papers report FPGA resource numbers". Only **two** do (Distributed-HISQ, gladiator) — the census's own Vegapunk entry marks its resource figures `UNKNOWN`. | Corrected in the MICRO census and the synthesis. |
| **6** | Artifact tally: QSW counted 4/20, but one of the four (Stripping QDD) is the boundary-band paper explicitly excluded from the 20 — the numerator counted a paper outside its denominator. | QSW 3/20; **total 25 → 24 of 102**. |
| **7** | ISCA: "the population grew 20% (135 → 172)". Actually **+27.4%** archival, +22.9% research-track. | Corrected with both figures. |
| **8** | Synthesis: "dedicated quantum sessions went from two venues in 2024 to four in 2026", but the table above it lists **three** (ISCA, HPCA, ICS) with MICRO-59 unknown. | Corrected to three, with MICRO-59 explicitly unresolved. |
| **9** | The scheduling-branch count appeared three ways (11 / eleven / a matrix summing to 10 for six venues, 12 with SC and ASPLOS), and "1–4 papers per venue" was false for HPCA (0). | Standardized to **10 across the six venues censused here, 12 including SC and ASPLOS**; range corrected to 0–4. |
| **10** | BP-SF: "the 55%-average / **18%-max latency reduction**". The source says maximum latency falls **to** 18% of the single-process implementation — an 82% reduction. | Rephrased in the deep dive and in candidate M4. |

## Overstatements corrected

- **The simulation generalization now carries its denominator.** "Memory, for four of six papers …
  the field's simulation work is overwhelmingly single-device memory engineering" generalized from the
  deep-dived subset to the field. The six are 6 of ~10 simulation papers, one of which is outside the
  102; the four not deep-dived attack redundant compute rather than memory. The claim is now scoped to
  the deep-dived subset with the corpus-wide ratio marked `INSUFFICIENT_EVIDENCE`.
- **The ASPLOS year basis is now declared.** ASPLOS's 36 is a *program-year* count (14/10/12); its
  proceedings-year count is 34. The Phase-1 census forbids mixing the two denominators, and the
  eight-venue aggregate did mix them silently. Declared inline.
- **The "verified denominators" claim is now precise.** Three denominators inside the 1,281 are
  `TOTAL_COUNT_UNVERIFIED` (HPCA 2026 is **≥118** and enters as 118; ISCA 2025 carries ±1; QSW 2026
  has no publisher TOC), so the total is stated with its one-sided uncertainty in README, METHODOLOGY
  and the synthesis.
- **QSW 2024's three boundary-band items are now all named** (TSP encodings, Stripping QDD, AdvQuNN),
  so a reader can audit the relevance call rather than only the one that was discussed.
- **Titles abbreviated in a document that corrects others' titles** were expanded: Coset Ensemble
  Decoder ("for Quantum Error Correction", not "for QEC"), Q-Profile ("the Quantum Approximate
  Optimization Algorithm"), and the QSW WIP item ("Software Development Kit").
- **HPCA section headings** now label which denominator they use (archival vs research-track), and
  HPCA 2026's is tagged `TOTAL_COUNT_UNVERIFIED` at point of use.
- **MICRO's summary** no longer classes Surf-Deformer as shuttle/zone scheduling, and the synthesis no
  longer lists Flag-Proxy Networks among decoding artifacts three paragraphs after establishing that
  it is not a decoding paper.
- **SWIPER's LOC figure** now distinguishes the 3,677-line package from the 3,271 lines in the seven
  named files.

## What the audit confirmed as sound

**Bibliographic layer — clean.** All 12 DOIs resolved exactly on title, authors, year, venue and page
range; **none failed and none resolved to a different paper.** Two resolutions independently confirmed
census claims: `10.1109/HPCA57654.2024.00051` returns **pp. 613–613, a single page**, confirming the
Best-of-CAL exclusion that keeps HPCA 2024 at 1 rather than 2; and
`10.1109/HPCA68181.2026.11408466` returns **pp. 1–15**, confirming HPCA 2026's per-article pagination
and therefore why page-tiling verification is structurally impossible that year.

**Code cross-validation — all 11 re-checked claims confirmed**, including the load-bearing negative
ones: Coset's `hardware_code/` contains **only `.gitkeep`** and the repo has zero `.v/.sv/.vhd/.tcl/
.xdc`; `qontra` contains **zero HDL** and its seven decoder `.cpp` files are exactly as listed, with
`enum class type { data, xparity, zparity, flag, proxy }` verbatim; Pinball has **no power, area or
bandwidth model and no Promatch baseline**, and its nine comment-delimited pipeline stages appear in
the exact claimed order. SWIPER's `fpga_data.json` LUT and register arrays match the quoted values
**digit for digit**. BP-SF's shipped `[[144,12,12]]` invocation uses exactly the defaults that give
the ≤100-candidate bound. DC-MBQC's `ubvec_max=1.2` / `max_steps=20` / `initial_temp=10.0` /
`cooling_rate=0.95` and `third_party/metis.dll` are all verbatim, including the flagged
code-vs-paper α discrepancy.

**URL validity.** All 21 cited GitHub repositories, the GitLab project and the `mqt-predictor` branch
resolve. **`abhishek-nautiyal97/qScheduler` 404s — confirmed**, as the census states.
**`UCLA-VAST/ZAC` resolves while `UCLAVAST/ZAC` 404s — confirmed.** Zenodo records 19969999, 19449157
and 15377656 exist and match; 19969999 independently confirms the TuniQ Utah–Rice affiliation
correction.

**Arithmetic.** Every per-venue sum, the 23/41/38 = 102 column totals, every rate cell, the taxonomy↔
matrix reconciliation, the regime tags summing to 102, and the derived figures (1.5 W ÷ 0.56 mW ≈
2,679; 2³⁰×16 B ≈ 17.2 GB; 2⁴²×16 B ≈ 70 TB; (w_max−w_min+1)×n_sample = 100; 10×⌈625/100⌉ = 70) all
recomputed sound.

**Phase-1 cross-claims.** SC total 11 (7+4) and ASPLOS 36 confirmed; ASPLOS compilation 10, QEC 11 as
largest branch, simulation 1, scheduling 1, distributed 3 all confirmed; and **"SC's 3-of-3
compile-time-scalability arguments vs ASPLOS's 2-of-10" verified verbatim** against the ASPLOS
census's own finding F4.

**QSW 2025 fully re-derived independently** and found exactly correct: 32 entries, perfect tiling of
pp. 1–280 with the two corrupt-metadata entries in the 48–59 and 104–115 gaps; REGULAR 17, BOUNDARY 6,
SHORT 5, WIP 0; the four back-bound non-QSW papers at pp. 257–280 exactly as described.

**Gap-language discipline — clean.** "unexplored" 0 hits. "research gap" 3 hits, all negations.
"novel" 1 hit, in the process name "novelty-falsification pass". All 26 "first" hits are "first
author", "first-class", "first page", "first-to-finish", "first-order", "Read first" — **no priority
claim anywhere**. No absence is upgraded into a claimed gap; superlatives are consistently
corpus-scoped.

**Seed anchoring — no sign of it.** The four corrections move in both directions (three up, one down);
four venue-years reproduce the Phase-1 numerators exactly; and both "no quantum vocabulary in the
title" discoveries are real, confirmed independently via OpenAlex. Notably **the one denominator error
appears at QSW — the venue with no seed list at all** — which is consistent with error-by-fatigue
rather than anchoring.

## What could not be verified

- **FTQCSA 2025's workshop status and the zero-leakage check** — the workshop site is behind a Google
  login wall. The claim is plausible and self-consistent, and the other two claimed exclusions
  (HPCA Best-of-CAL, QSW 2024's symposium block) were independently confirmed, but this one rests on
  the census's own reading.
- **Abstract-level content for papers the census itself marks `INSUFFICIENT_EVIDENCE`** (quEStab's
  kernel design, Rasengan's numbers, ISCA 2026's 4 K syndrome-compression paper, the QSW 2026 nine) —
  ACM DL and IEEE Xplore remain 403/418. The auditor could confirm only that the abstention is
  appropriate, not the underlying facts.
- **ISC 2025's 28-paper denominator and HPCA 2026's ≥118** — no reachable second source; both are
  already flagged `TOTAL_COUNT_UNVERIFIED`.
- **Paper bodies behind the quantitative-context corrections** (Pinball's d=5/p=10⁻⁴ figure, ZAC's 22×
  vs Enola, MonteQ's abstract-vs-body split) — the auditor verified the code-side halves only.
- `doi.org/api/handles`, `api.semanticscholar.org` and `api.crossref.org` were all egress-blocked for
  the auditor; every DOI check went through `api.openalex.org` instead.

## Assessment

The audit's own summary: the code cross-validation layer withstood eleven targeted attempts to break
it and yielded two small errors; the bibliographic layer was clean at twelve of twelve DOIs; **the
damage was concentrated in counting and aggregation** — one real denominator error, one dropped
Phase-1 qualifier on the flagship finding, and six smaller tally inconsistencies.

All ten material errors and all seven overstatements are fixed in the files as committed. This
document is the record of what was wrong before the fix.

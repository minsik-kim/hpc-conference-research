# Multi-Venue Quantum-HPC Census — Methodology

**Census performed:** 2026-09-17 (KST). **Scope:** ISC High Performance, ISCA, ICS, HPCA, MICRO,
IEEE QSW — 2024, 2025, 2026. **Phase:** Phase 2 continuation (SC and ASPLOS were censused
2026-09-06 and live in `../quantum-hpc-survey/`).

## 1. What this project is

A **full-population regular-paper census**, not a keyword survey. For every venue-year the
complete main-track regular-paper population (the denominator) was reconstructed *before* any
quantum screening, then the Quantum-HPC-relevant subset was selected from it. This is the method
the ASPLOS census forced on the project after program-based counting was shown to undercount
real volumes.

The research question behind it: *at the boundary between HPC and quantum computing, which
computational, architectural, runtime, scheduling, parallelism and performance problems are
forming — and which of today's architecture problems become HPC problems at future scale?*

## 2. Enumeration method and its tags

Every venue-year carries three tags:

- **Enumeration method** — `VOLUME_ENUMERATED` / `PUBLISHER_TOC_ENUMERATED` / `PROGRAM_ENUMERATED`
- **Count status** — `TOTAL_COUNT_VERIFIED` / `TOTAL_COUNT_UNVERIFIED`
- **Publication status** where relevant — e.g. `PROGRAM_INCOMPLETE_AS_OF_<date>`

Two completeness proofs were used, and the difference matters:

**Page-range tiling (strongest).** Enumerate every TOC entry *with its page range* and verify the
ranges tile the volume from first page to last with zero gaps and zero overlaps. A gap-free tiling
leaves no room for an unlisted paper. This worked for ICS (all three years), HPCA 2024/2025,
MICRO 2024/2025, ISC (all three years via DOI-block contiguity) and QSW 2024/2025.

**DOI-block contiguity (venue-dependent).** Probe the publisher's article-ID block for contiguity
and directly probe interior gaps to see whether they 404. This worked for IEEE volumes (ISC, ISCA
2024/2026) where article IDs are assigned *in program order*. It **fails for ACM volumes**: ACM
article-ID suffixes are not ordered by page or program position, and interior "gaps" resolve to
already-enumerated papers. Recorded as a negative methodological result; do not reuse it on ACM.

Where neither proof was available (ISCA 2025, HPCA 2026, QSW 2026, MICRO-59) the count is
`TOTAL_COUNT_UNVERIFIED` and the residual ambiguity is stated in the census file.

## 3. Inclusion — regular/full main-conference research papers only

Excluded by category: workshop papers, short papers, posters, demos, work-in-progress, invited
talks, panels, tutorials, keynotes, doctoral symposia, abstract-only items, non-archival
presentations, **invited re-presentation tracks** (HPCA "Best of CAL"), and **invited symposium
papers bound into a main volume** (QSW 2024's QSWUtil block).

Industry tracks were judged per venue rather than assumed: at **ISCA** and **HPCA** the industry
papers occupy full page ranges inside the same proceedings block as research papers and are
therefore archival — both totals are reported separately. **MICRO 2024/2025** had no industry
track. No industry-track paper in any venue-year was quantum-related, so this choice does not move
any numerator.

Status unclear → `STATUS_UNCLEAR`, and **not** counted in the regular-paper total.

## 4. Relevance — four scenario tags, multiple allowed

- `HPC_FOR_Q` — classical HPC serving quantum computation (simulation, QEC decoding, compilation,
  mapping/routing, circuit cutting, classical pre/post-processing)
- `Q_IN_HPC` — QPU as a heterogeneous HPC resource (runtime, scheduling, resource management,
  multi-QPU, workflow, virtualization, telemetry, HPC-centre integration, characterization)
- `Q_FOR_HPC` — quantum algorithms that would change scientific/HPC workloads
- `FUTURE_WORKLOAD` — work that substantially changes parallelism, circuit/shot count, depth,
  classical compute/memory requirement, communication, synchronization or latency

## 5. Exclusion — the recurring false-positive classes

1. **Post-quantum cryptography / FHE / ZKP / PIR.** Dense at ISCA, HPCA and MICRO.
2. **Classical quantum chemistry, many-body, quantum transport, NNQS** — classical HPC wearing a
   quantum-sounding title. Confirmed hits: ISC 2024 VASP eigensolver, ISC 2025 nuclear CI,
   ICS 2026 quantum-transport NEGF.
3. **"Quantum-inspired" classical methods** — Ising machines, vector/simulated annealing, classical
   QUBO solvers. Confirmed hits: ISCA 2026 SATIC, ISCA 2024 ReAIM, HPCA 2024 SACHI, HPCA 2025/2026
   Ising and SAT accelerators, MICRO 2024 SOPHIE, ISC 2025 vector annealing.
4. **Classical superconducting logic** — SFQ / RSFQ / AQFP and cryo-CMOS are *classical* digital
   logic, not quantum computing. Confirmed hits: MICRO 2024 SuperCore, MICRO 2025 SuperSFQ,
   ICS 2025 Josephson GCN accelerator and JBSA. MICRO 2025 itself draws this line, running a
   "Superconducting Systems" session separate from Quantum-1/Quantum-2.
5. **Quantum sensing** (distinct from quantum computing). Confirmed hit: ICS 2026 SpinTune.

Also excluded: pure device physics, fabrication/materials, and pure quantum information theory
with no systems implication.

## 6. Evidence discipline

Evidence tags: `[proceedings]` `[official-program]` `[official-CFP]` `[paper]` `[abstract]`
`[code]` `[artifact]` `[documentation]` `[reconstruction]` `[inference]`.

Artifact status: `PUBLIC_CODE` / `PUBLIC_ARTIFACT` / `PARTIAL` / `NO_PUBLIC_ARTIFACT_FOUND` /
`UNKNOWN`. **`NO_PUBLIC_ARTIFACT_FOUND` was used only after an actual search**; where the search
tooling failed the record says `UNKNOWN`. Neither means "no code exists".

Evaluation modality is recorded explicitly, because at architecture venues it is frequently
mistaken: `REAL_QPU` / `REAL_HARDWARE` / `FPGA_PROTOTYPE` / `RTL_SYNTHESIS` / `CYCLE_SIMULATION` /
`ARCH_SIMULATION` / `SOFTWARE_SIMULATION` / `ANALYTIC_MODEL` / `PROJECTED`.

**Every quantitative claim is recorded with its measurement context** — baseline, scale, code
distance, physical error rate, noise model, hardware. A number without its qualifiers is not a
portable fact and is not recorded as one.

## 7. Seed-list discipline

A prior exploratory pass (Phase 1, `../quantum-hpc-survey/corpus/QUANTUM_HPC_VENUE_MAP.md`) had
produced candidate titles and expected counts for ISC, ISCA, ICS, HPCA and MICRO. Those were
treated as `DISCOVERY_SEED_ONLY` — never as a whitelist, a complete list, or ground truth. Every
venue population was reconstructed independently and every subset re-selected independently, and
final counts were computed before comparison with the seed. QSW had no seed list at all.

The discipline paid: **19 relevant papers were found that the seed list did not name**, and three
seed-derived figures were corrected (see `CORRECTIONS_TO_PHASE1.md`). Two of the new finds have no
quantum vocabulary in their titles at all — ICS 2024's *Minimizing Coherence Errors via Dynamic
Decoupling* and MICRO 2025's *Rasengan* — and were reachable only by hand-scanning every title in
the enumerated volume. That is the concrete argument against keyword-driven census.

## 8. Tooling constraints encountered (recorded for reproducibility)

- **dblp.org** — robots-disallowed; unusable.
- **IEEE Xplore** — HTTP 418 to every request; never usable.
- **ACM Digital Library** — HTTP 403 on `/doi/`, `/doi/abs/`, `/doi/pdf/`, `/doi/proceedings/`.
  This blocked several abstracts, including papers marked Gold OA.
- **api.crossref.org** — worked for one pass, egress-blocked (403 CONNECT) in others. Unreliable.
- **researchr.org/publication/<venue>-<year>** — mirrors publisher TOCs, not robots-blocked, and
  the single most valuable source. **Must be queried for a per-entry enumeration with page ranges,
  never for a count**: page summarizers returned three different totals for one page, and in two
  documented cases **fabricated plausible-sounding paper titles** that do not exist. Every count in
  this census therefore rests on enumeration plus a second independent source shape.
- **Official conference sites** — excellent and underused; the authoritative source for session
  names, and for QSW 2026 the authoritative source for paper *category*.
- **api.semanticscholar.org** DOI lookups worked (verbatim abstracts); **api.openalex.org** DOI
  lookups worked but rate-limited hard and sometimes returned paraphrased abstracts.
- **arxiv.org/html/<id>** worked and is far better than `/abs/` for methodology; the arXiv API is
  robots-blocked.
- **Zenodo** — record metadata readable, **file downloads egress-blocked**, so several artifacts
  could be confirmed to exist but not inspected.
- **GitHub `git clone`** — worked, and was used for the code cross-validation deep dives.

## 9. What this census does not claim

`COMPLETE_AS_CURRENT_SOURCE` for the venue-years it enumerates with `TOTAL_COUNT_VERIFIED`
denominators; the rest are marked `TOTAL_COUNT_UNVERIFIED` in their census files and the aggregate
(1,281 papers screened) inherits that one-sided uncertainty.
**Not** `COMPREHENSIVE_FIELD_COVERAGE`. Venues still uncensused are listed in
`../quantum-hpc-survey/corpus/QUANTUM_HPC_RESEARCH_QUEUE.md`. Absence of a topic from this corpus
is `NOT_COVERED`, never evidence that the topic is unstudied
(`governance/ANTI_HALLUCINATION_RULES.md`).

No research gap is declared anywhere in this census. The permitted vocabulary is `VENUE_GAP`,
`POSSIBLE_CROSSOVER`, `OPEN_QUESTION`, `UNDEREXPLORED_IN_THIS_CORPUS`, `INSUFFICIENT_EVIDENCE`
(`governance/RESEARCH_GAP_RULES.md`).

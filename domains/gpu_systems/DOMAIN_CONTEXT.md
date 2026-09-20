# DOMAIN_CONTEXT — GPU Systems

Status: **PARTIAL** — a full 30-venue-year population census with a complete
broad screen, and 85 full-paper deep analyses. Coverage is bounded by public
full-text access, not by the screen. See `RESEARCH_STATUS.md`.

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-19

## Scope

GPU systems research 2024–2026, as distinct from research that *uses* GPUs.
The boundary is the whole point of this domain: a paper belongs here when its
core contribution depends on a GPU-specific property — SIMT execution,
warp/wavefront scheduling, the GPU memory hierarchy and its page-fault path,
matrix-unit operand semantics, CUDA/HIP semantics, GPU resource partitioning,
NVLink/xGMI/GPUDirect data paths, GPU-specific failure modes — and not merely
because the evaluation ran on a GPU.

Eleven venues' worth of that question was asked over ten conferences
(SC, ISCA, MICRO, HPCA, PPoPP, ASPLOS, ICS, IPDPS, HPDC, ISC) × three years
(2024, 2025, 2026).

## What this corpus actually is

**A population-first census with a full-paper gate**, not a keyword harvest.
For each venue-year the official main/regular research-paper population was
reconstructed first; the whole population was then screened for GPU relevance;
the screen's candidates were then put through a counterfactual test; and only
papers whose full text was publicly reachable **and was actually read** were
given a deep analysis. The reading depth of each analysis is recorded in its
own `read_depth` field.

Three numbers that must never be conflated, and are kept apart everywhere in
this domain:

```
population completeness        — did we reconstruct the venue's real paper list?
  ≠ public full-text completeness — could we read the papers in it?
    ≠ field comprehensiveness     — is this what GPU research looks like?
```

This domain is strong on the first, uneven on the second, and makes **no
claim at all** on the third.

## Current coverage

| | |
|---|---|
| Venue-years censused | 30 (21 `COMPLETE_CENSUS`, 9 `PARTIAL_CENSUS`, 0 `BLOCKED`) |
| Official population reconstructed | 2,354 main/regular papers across 27 venue-years |
| Venue-years with no reconstructable denominator | 3 — HPCA 2026, MICRO 2026, SC 2026 |
| Broad GPU candidates screened | 551 |
| Candidates adjudicated with a recorded verdict | ~351 distinct papers |
| Deep analyses (full text read) | **85** |
| Watchlist (candidate, full-paper gate not met) | 202 |

The three venue-years without a denominator are not failures of effort: SC 2026
and MICRO 2026 had not published an enumerable main program by 2026-09-18, and
HPCA 2026 had three mutually inconsistent sourced figures (119 / 113 / 123)
that no reachable source reconciled. They are recorded as `PARTIAL_CENSUS` with
the exact obstruction named, and **no repository-wide GPU share is computed**,
because the denominator does not exist.

## Core mental model

Four things this corpus established that a reader should carry into any
question routed here.

1. **The screen's hard cases are not at the edges, they are in the middle.**
   The counterfactual test — *would the contribution survive on a generic
   accelerator or a CPU?* — separated cleanly on one criterion that recurs
   across clusters: does the contribution's own output artefact cross the GPU
   boundary, or is the GPU-specific work delegated to a layer below it? A
   retargetable tensor compiler that emits PTX is `RELATED_GPU`; a language
   whose type system names the MMA register-fragment layout is `CORE_GPU`.

2. **Several expected progressions are not progressions.** The corpus checked
   lineages against the papers' own related work and citations, and found that
   the GPU-communication ladder (GPU-aware MPI → device-initiated → symmetric
   memory → GPU-resident control) is a taxonomy of coexisting mechanisms
   rather than a traversed sequence, and that the Tensor-Core story is three
   largely disjoint citation branches meeting in one characterisation paper.
   These negatives are recorded as findings, not smoothed away. See
   `synthesis/GPU_TOPIC_LINEAGES.md` §"Progressions the corpus does NOT support".

3. **Mutual non-citation is endemic and measurable.** Exact duals published at
   the same venue in the same year that do not cite each other; four
   mutually non-citing GPU-compression communities with heavy author overlap;
   a sparse-GPU community and a ray-tracing-unit community that do not cite
   each other in either direction, verified by targeted query. Where the
   corpus verified an absence it is tagged `NOT_CITED`, which is a stronger
   claim than silence.

4. **The evidence base differs sharply by venue, and one venue's own papers
   dispute it.** Across SC/ICS/IPDPS/ISC/HPDC/PPoPP, 48 of 49 analyses rest on
   real hardware; across ISCA/MICRO/HPCA, 15 of 22 involve a simulator. The
   sharpest correction to the simulated line came from inside MICRO, where a
   measurement study puts the standard simulator baseline at 34.03% MAPE
   against a real RTX A6000 and finds real cores have no operand collectors.

## Major topic families

Twelve topic files, one per taxonomy area, in `topics/`. See `TOPIC_MAP.md`
for the routing table with per-topic evidence counts. Category **Q —
fixed-function GPU units repurposed for general computation** was **added
during this work** because the evidence demanded it: the papers that put
BVH-traversal, texture and rasterisation hardware to non-graphics use share
no application domain and no resource, so scattering them through A/B would
have destroyed the pattern. That decision and its evidence are argued in
`topics/fixed_function_repurposing.md`.

## Representative sources

The corpus's own strongest documents, by area: the modern-GPU-core dissection
and the Blackwell/Hopper microbenchmark pair (A/B); the unified-memory
control-path trio spanning both vendors (C/D); the compression
output-placement chain (E); the three Tensor-Core branches and the
cross-generation matrix-unit characterisation (F); the SpMM format chain (G);
the tile-language and consistency-model pair (H/I); the MIG-versus-software
partitioning fork (J/K); the two-axis communication map (L/M); the
stall-attribution and production-telemetry line (N/O); the NVML sampling-window
study (P); and the RT-unit generalisation papers (Q).

## Key synthesis documents

- `synthesis/GPU_MASTER_INDEX.md` — every deep analysis, by taxonomy and by venue-year
- `synthesis/GPU_TOPIC_LINEAGES.md` — verified lineages and verified non-lineages
- `synthesis/GPU_HARDWARE_GENERATION_MAP.md` — what changed per generation, and the unresolved tensions
- `synthesis/GPU_COMMUNICATION_STACK.md` — the initiation × fabric map
- `synthesis/GPU_MEMORY_LINEAGE.md` — page walk → UVM → oversubscription → migration → multi-GPU
- `synthesis/GPU_TENSOR_CORE_LINEAGE.md` — the three disjoint branches
- `synthesis/GPU_CROSS_VENUE_MAP.md` — how the ten venues differ, argued from this census
- `synthesis/GPU_EXISTING_CORPUS_OVERLAP.md` — the de-duplication registry
- `synthesis/GPU_PENDING_FULLTEXT.md` — the watchlist
- `synthesis/GPU_INTEGRATION_QUESTIONS.md` — the twelve cross-cutting questions, answered from corpus evidence only
- `synthesis/METHODOLOGY_NOTES.md` — how this was built and what it does not claim

## Evidence limitations

Read these before treating any absence here as meaningful.

- **Publisher access shaped this corpus.** `dl.acm.org` returned 403,
  `ieeexplore.ieee.org` returned 418, and `dblp.org`, `par.nsf.gov` and
  `ssl.linklings.net` were robots-disallowed from the build environment. 27
  watchlist papers are recorded as **open access but unreachable from here** —
  that is a tooling limit, not a licence one, and not a judgement on the paper.
- **Full-text reachability is not uniform across venues**, so the shape of
  this corpus partly reflects who posts preprints and author PDFs. ASPLOS is
  the most reachable venue in the corpus at roughly 51%.
- **Abstract-only verdicts exist and are labelled.** They were allowed to
  decide relevance but never to justify a deep analysis.
- **Two deep analyses carry a `RELATED_GPU` verdict** (PICO, Hydrogen). They
  were written before or during re-adjudication and are retained as
  documented boundary cases, clearly labelled, rather than deleted — see
  `governance/KNOWLEDGE_BASE_RULES.md` rule 7. They are excluded from
  `CORE_GPU` counts.
- **SC 2025 has an unresolved population discrepancy**: 137 papers officially
  announced as accepted, 133 regular papers printed in the main volume, 144
  printed items in total. All three figures are recorded; none is preferred.
- **Several seed titles could not be verified to exist at all** (10 SC 2026,
  4 MICRO 2026, 1 ISC 2026). They are listed under "Existence unverified" and
  are neither cited nor treated as refuted.
- **`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`.** An ~80-paper
  AI/HPC corpus with GPU communication, memory/offload, compiler/kernel and
  serving coverage exists outside this repository and is not imported. For 99
  papers here, duplication against it is recorded as **NOT DETERMINED** —
  never as absent. Importing that corpus requires a de-duplication pass first.

## Retrieval instructions

Do not answer a quantitative, mechanism, hardware-configuration,
GPU-initiated-versus-host-initiated, code-symbol or novelty question from this
file, from `TOPIC_MAP.md`, or from a `topics/*.md` file. Descend:

```
DOMAIN_CONTEXT → TOPIC_MAP → topics/<topic>.md → synthesis/<document>.md
  → corpus/GPU-<ID>--<slug>.md → the paper, or the pinned artifact commit
```

Two domain-specific cautions. **Keep hardware generations apart** — Hopper's
TMA/`wgmma`/distributed shared memory, Blackwell's TMEM/`tcgen05`, CDNA3's
unified physical memory on MI300A and CDNA2's MI250X are not interchangeable,
and several corpus findings are generation-specific. **Keep a number with its
qualifiers** — a compression ratio without its dataset and error bound, a
sparse speedup without its matrix suite and baseline library version, or a
power figure without its sensor and sampling rate is not a portable fact, and
this domain records several cases where dropping the qualifier would produce a
false comparison.

## Where to look next

- For topic questions: `TOPIC_MAP.md` → `topics/<topic>.md`
- For a specific paper: `synthesis/GPU_MASTER_INDEX.md` → `corpus/<ID>--<slug>.md`
- For a venue-year's population and screen: `census/<VENUE>_<YEAR>.md`
- For every adjudicated candidate, analysed or not: `corpus/_LEDGER_*.md`
- For research questions: `OPEN_QUESTIONS.md` → `research/CANDIDATE_QUESTIONS.md`
- For third-party code provenance: `implementation/ARTIFACT_REGISTRY.md`
- For coverage and import status: `RESEARCH_STATUS.md`

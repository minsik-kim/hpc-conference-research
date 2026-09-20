# OPEN_QUESTIONS — GPU Systems

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-19

## Status vocabulary and the bar for promotion

Per [`governance/RESEARCH_GAP_RULES.md`](../../governance/RESEARCH_GAP_RULES.md),
an observation is not a research gap. **Every item below is `CANDIDATE`.** None
has been through the own-corpus cross-check, closest-work search, external
targeted literature search and novelty falsification the pipeline requires.
"Not found in this corpus" is never by itself grounds for promotion, and this
corpus's own coverage is bounded by publisher access (see `RESEARCH_STATUS.md`),
which makes its silences especially weak evidence.

Items are grouped by what kind of thing they are, because that determines what
would settle them.

## A. Contradictions the corpus found and did not resolve

These are the strongest items here: two pieces of published evidence that do
not sit together, both read in full.

**A1 · What a GPU issue stage actually is.** `CANDIDATE`.
An ISCA 2024 out-of-order issue proposal is built on a simulator core model
with a scoreboard and operand collectors; a MICRO 2025 measurement study puts
that baseline at 34.03% MAPE against a real RTX A6000 and finds real
Turing-to-Blackwell cores use compiler control bits and have no operand
collectors. Neither evaluates the other. What would settle it: re-evaluating
the issue proposal on the measured core model.
→ [`../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md`](corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md),
[`../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md`](corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)

**A2 · Blackwell FP64 matrix throughput.** `CANDIDATE`.
One cross-generation characterisation reports a B200 FP64 matrix regression
against H200; an ISC 2026 FEM paper measures working FP64 DMMA on GB200 and
does not mention any reduction. Different products, unreconciled by either.
Load-bearing, because it decides whether precision emulation is a necessity or
an option.

**A3 · Symmetric memory.** `CANDIDATE`.
An ASPLOS 2026 paper reports finding no implementation where NVSHMEM beats
NCCL for collectives; an SC 2026 paper adopts PGAS as a core principle one
cycle later and reports the former's multicast hanging on GB200. Opposite
conclusions, close in time, on overlapping hardware.

**A4 · MIG isolation.** `CANDIDATE`.
MIG's isolation is shown porous in two independently published ways — an
unpartitioned L3 TLB and an unpartitioned power/clock domain — by papers that
do not cite each other, and both falsify an assumption that the MIG-scheduling
papers make. What would settle it: a single study measuring both channels on
one device.

## B. Structural absences the corpus verified

Verified `NOT_CITED` relationships, not mere silences.

**B1 · Four mutually non-citing GPU-compression communities**, despite heavy
author overlap: standalone scientific compressors, compression inside
collectives, hardware cache compression, and lossless floating-point
compression. `CANDIDATE`. The interesting question is not who is right but
whether the output-placement cost the standalone line measures is the same
cost the in-collective line pays.

**B2 · The sparse-GPU community does not cite the ray-tracing-unit
community**, in either direction, verified by targeted query on two papers'
full text and reference lists. `CANDIDATE`. Sharpened by the observation that
the authors of a bit-matrix-unit BFS paper wrote a DFS paper a year later
using no matrix unit at all.

**B3 · Language-level GPU correctness is three literatures that do not cite
each other**: consistency models, spatial memory safety, and dynamic
race/over-synchronisation detection. `CANDIDATE`.

**B4 · Exact duals at the same venue and year that do not cite each other** —
an under-synchronisation detector and an over-synchronisation detector at
SC 2024 and MICRO 2024 with the same programs and the same baselines; two
SpMM papers in the same PPoPP 2025 session independently deriving the same
operand-swap insight. `CANDIDATE`, and partly explained by same-cycle
publication, which is why the sustained multi-year version (B1) is the
stronger item.

## C. Methodological gaps the corpus exposed

**C1 · Rooflines are essentially absent from the GPU compression
literature.** `CANDIDATE`. Exactly one paper in that cluster reports
achieved-versus-peak bandwidth, and only for one stage. Most papers do not
establish what their throughput is bounded by.

**C2 · Power instrumentation validates a GPU sensor against a GPU sensor.**
`CANDIDATE`. Of ten corpus papers with an instrumentation record, one has a
real external ground truth; three disclose no sensor or no sampling rate while
reporting percentage-level results. The one paper that characterised NVML's
boxcar sampling window is cited by none of the papers that depend on that
sensor.

**C3 · No AMD equivalent of that sampling-window characterisation exists.**
`CANDIDATE`. One AMD attribution paper independently rediscovers an
undocumented filter and bypasses it rather than characterising it.

**C4 · GPU-sharing schools are never compared on the same silicon.**
`CANDIDATE`. Hardware partitioning is studied on parts that have MIG; software
partitioning on parts that do not. The comparison that would decide between
them has not been run.

**C5 · Two top-tier papers depend on an unsupported driver interface** whose
own header describes it as co-opting debug logic, with no discussion of
removal risk. `CANDIDATE` — this is a reproducibility question, not a
correctness one.

## D. Falsified expectations worth recording

Not gaps; the opposite. Recorded so that nobody re-proposes them.

**D1 · GPU health telemetry does not predict application slowdown.** Real
per-device heterogeneity exists at fleet scale, but the rank correlation to
runtime is ~0.07–0.08. Any proposal that assumes otherwise must clear this
first. `LIKELY_CLOSED` as an assumption, `STILL_OPEN` as a question about
which signals *would* predict.

**D2 · The GPU-communication ladder is not a ladder.** Initiation placement is
determined by the fabric crossed, not by the year. Proposals framed as
"advancing to the next stage" should be reframed.

**D3 · The Tensor-Core progression is not one chain.** Three branches that
largely do not cite each other; a survey framed as a single lineage would be
wrong.

## E. Questions this corpus is structurally unable to answer

Recorded so that its silence is not read as evidence.

- Anything about workshop, journal or arXiv-only GPU research.
- Whether the AI/HPC corpus already covers 99 of these papers — `NOT
  DETERMINED` until that corpus is imported.
- The content of the 27 open-access papers unreachable from the build
  environment, and of the 15 seed titles whose existence is unverified.
- Any GPU-share-of-venue trend, for the three venue-years with no denominator.

## Where these came from

Each item traces to a cluster ledger's cross-paper findings section or to a
deep analysis's §12.13/§12.14. `research/CANDIDATE_QUESTIONS.md` holds the
per-item pointers. Nothing here was generated from general knowledge of the
field.

# evidence/ — GPU Systems

How claims in this domain are graded, and what the grading cannot reach.

## Evidence tags in use

Per [`governance/SOURCE_EVIDENCE_RULES.md`](../../../governance/SOURCE_EVIDENCE_RULES.md).
Counts across `corpus/`, `synthesis/` and `topics/` at 2026-09-19:

`[paper]` 3241 · `[code]` 424 · `[inference]` 198 · `[reconstruction]` 91 ·
`[README]` 94 · `[official-web]` 77 · `[artifact]` 11 ·
`[author-presentation]` 10 · `[documentation]` 4.

The `[paper]`-to-`[inference]` ratio is the point of the exercise: this domain
is built on read papers, and the places where it reasons beyond them are
marked. `[reconstruction]` is used for pseudo-code and for symbol names that
were rebuilt rather than read.

One evidence-class trap was caught and is worth repeating: an author's slide
deck found at a paper-like URL is `[author-presentation]`, not `[paper]`, and
numbers that appear only in the deck are labelled as such even when they concern
the same work.

## Uncertainty markers

Preserved exactly, never promoted:

`UNKNOWN` 1557 · `NOT_FOUND_AFTER_SEARCH` 699 · `NOT_SEARCHED` 359 ·
`NOT_IN_PAPER` 249 · `NOT_INSPECTED` 127 · `NOT_ESTABLISHED` 71 ·
`MEMBERSHIP_UNVERIFIED` 37 · `NOT_CITED` 34 · `PARTIALLY_READ` 5.

Three of these carry meanings that are easy to blur and are kept distinct:

- `NOT_FOUND_AFTER_SEARCH` — searched, nothing found.
- `NOT_SEARCHED` — deliberately not searched, usually a budget decision. A
  re-runnable gap, **not** a negative result.
- `NOT_CITED` — a citation relationship was checked and found absent. This is a
  positive finding about the literature, not an absence of effort.

`MEMBERSHIP_UNVERIFIED` marks a paper whose venue attribution could not be
corroborated from an official source — most often an SC 2026 or ISC 2026 item
known only from a preprint.

## Publication-type classification

Population reconstruction excluded, and counted separately where visible:
workshops, posters, tutorials, demos, BoFs, keynotes, panels, PhD forums,
ACM SRC, industry tracks, Best-of-CAL sessions, Gordon Bell finalists and
Reproducibility/Artifact reports. Each census file records what it excluded and
with what count. A workshop paper is never treated as evidence of a gap in
main-track coverage.

## Access limitations that shaped this domain

These are environment limits, not licence limits, and several affect papers
that are open access:

- `dl.acm.org` → HTTP 403 for every URL form tried, including publisher PDF
  paths that other records describe as open.
- `ieeexplore.ieee.org` → HTTP 418.
- `dblp.org`, `par.nsf.gov`, `ssl.linklings.net`, `web.archive.org`,
  `arxiv.org/search`, `export.arxiv.org` → robots-disallowed or blocked.
- `api.crossref.org`, `api.openalex.org`, `api.semanticscholar.org` → HTTP 429.
- `arxiv.org/abs/` and `arxiv.org/html/` worked, with intermittent 429s that
  cost two papers their deep analysis.

Consequence: **27 watchlist papers are stated to be open access and were still
unreachable.** `synthesis/GPU_PENDING_FULLTEXT.md` lists them under "Blocked by
tooling, not by licence". A reader on a different network should treat those as
one fetch away, not as closed.

## Deep-source requirement

`governance/ANTI_HALLUCINATION_RULES.md` names question types that may not be
answered from a compressed context. Two of them bite hardest here:
**GPU-initiated versus host-initiated distinctions** — answered in this domain
only from the paper or the pinned code, and left `UNKNOWN` for 30 communication
rows rather than inferred from an abstract — and **implementation-specific
questions**, answered only from a cloned repository at a pinned commit.

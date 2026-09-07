# SOURCE_EVIDENCE_RULES

## Provenance hierarchy

When citing or grounding a claim, record which of these evidence kinds it
rests on, most authoritative first:

```
[paper]
[artifact]
[code]
[author-presentation]
[README]
[official-web]
[documentation]
[reconstruction]
[inference]
```

## Publication-type classification

Every corpus entry records its publication type — these are not
interchangeable evidence:

```
ARCHIVAL_MAIN_PAPER
WORKSHOP_PAPER
POSTER
BOF
TUTORIAL
AUTHOR_PRESENTATION
TECH_REPORT
PREPRINT
VENDOR_DOCUMENTATION
```

## Rules

- **Presentation evidence must not be silently attributed to the paper.**
  A claim made only in a talk/slides is `[author-presentation]` evidence,
  not `[paper]` evidence, even about the same work.
- **Workshop work must not be classified as a missed main-conference
  paper.** A `WORKSHOP_PAPER` is not evidence of a gap in
  `ARCHIVAL_MAIN_PAPER` coverage.
- **Vendor documentation is not peer-reviewed evidence.**
  `VENDOR_DOCUMENTATION` is useful for implementation detail but must be
  labeled as such, not upgraded to paper-level evidence.
- **Quantitative claims must retain hardware/workload/baseline
  qualifiers.** A number without its measurement context is not a portable
  fact — restate the qualifiers whenever the number is reused.
- **Implementation details require code/artifact evidence when
  available.** Prefer `[code]`/`[artifact]` over `[inference]` from an
  architecture description whenever the code/artifact exists.

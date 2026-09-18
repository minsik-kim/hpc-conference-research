# Per-paper record schema (domains/virtualization)

Every candidate you examine produces exactly one YAML record. Emit a list under
key `papers:`. Use `UNKNOWN` (literal) when evidence is insufficient — never guess.

```yaml
- id: VIRT-<VENUE><YY>-<NN>        # e.g. VIRT-EUROSYS25-03 ; NN = your order within the venue
  title: <official title, exactly as the proceedings prints it>
  title_correction: <null | "seed list said: <old>">   # record silently-corrected seed titles
  authors: [<first author>, <...>]   # full list if cheap; at minimum first 3 + "et al."
  venue: <EuroSys|OSDI|SOSP|ATC|SoCC|ASPLOS|SC|HPDC|Middleware|CCGrid|HPCA|MICRO>
  year: <2024|2025|2026>
  publication_type: ARCHIVAL_MAIN_PAPER | OPERATIONAL_REFERENCE | INDUSTRY_TRACK |
                    WORKSHOP_PAPER | POSTER | SHORT_PAPER | TECH_REPORT | PREPRINT | UNKNOWN
  doi: <doi or UNKNOWN>
  official_url: <proceedings/program URL or UNKNOWN>
  fullpaper_source: <URL of the PDF/HTML you actually read, or UNKNOWN>
  classification: CORE | SUPPORT | CONTEXT | DROP
  classification_note: <one sentence: the decisive evidence for this layer>
  drop_reason: <null | one of: no_virtualization_relation | keyword_false_positive |
                pure_virtual_memory | publication_criterion | duplicate |
                already_analysed_no_delta | generic_application>
  taxonomy_primary: T1..T10
  taxonomy_secondary: [T..]
  physical_resource: <CPU core | DRAM | NIC | GPU | FPGA | NVMe | PCIe/CXL fabric | QPU | switch ASIC | UNKNOWN>
  logical_abstraction: <what the paper hands the workload>
  problem: <one sentence>
  mechanism: <1-3 sentences, concrete>
  isolation_mechanism: <how interference/security is bounded, or N/A>
  multiplexing_mechanism: <how one physical resource is shared, or N/A>
  state_mechanism: <where virtualization state lives + how it moves, or N/A>
  overhead_bottleneck: <the dominant cost the paper identifies>
  primary_tradeoff: <X -> gains Y but costs Z ; use the paper's own framing>
  quantitative_claims: [<"metric: value (hardware/workload/baseline qualifiers)">]  # only numbers you read in the paper
  why_useful_for_learning: <one sentence: what a virtualization learner gets from it>
  priority: P0 | P1 | P2 | P3
  related: [<other record ids or paper titles>]
  relations: [{type: PRECURSOR|EXTENSION|ALTERNATIVE|SAME_BRANCH|LAYER_ABOVE|LAYER_BELOW|TRADEOFF_PAIR|USES_MECHANISM_FROM|CONTRASTS_WITH, target: <id/title>, basis: <evidence>}]
  existing_corpus_overlap: <null | ai_hpc_systems | hpc_quantum | both>
  previous_analysis_depth: <null | "analysed in <corpus>: <what it covered>">
  evidence_depth: TITLE_ONLY | ABSTRACT | ABSTRACT_INTRO | DESIGN | DESIGN_EVAL | FULL
  evidence_kinds: [paper|artifact|code|official-web|documentation|preprint|program-only]
  confidence: HIGH | MEDIUM | LOW
  notes: <null | anything the orchestrator must know: ambiguity, access failure, etc.>
```

## Hard rules
1. `evidence_depth` must be the truth about what you actually read. If you only got the
   abstract, say ABSTRACT. Never claim DESIGN_EVAL or FULL unless you read those sections.
2. Never classify from the title. If you could not get past the title, emit the record with
   `evidence_depth: TITLE_ONLY`, `confidence: LOW`, and classification `CONTEXT` (not DROP),
   plus a note saying access failed.
3. Never copy a CORE/BROAD/EDGE label from the seed list. Decide independently.
4. Quantitative claims must be read from the paper and carry their qualifiers, or be omitted.
5. Ambiguous -> CONTEXT, never DROP.
6. DROP only for the seven listed reasons.
7. Record corrections, don't apply them silently: wrong seed titles go in `title_correction`;
   papers missing from the seed list that you find in the official program go in the batch
   report's `possible_omissions` with evidence.

## Batch report (separate YAML doc, same file, after `papers:`)
```yaml
venue_populations:
  - venue: EuroSys
    year: 2025
    official_source: <URL>
    main_track_paper_count: <N or UNKNOWN>
    count_basis: <how you counted / why UNKNOWN>
possible_omissions: [{title:, venue:, year:, why_relevant:, evidence:}]
possible_expansion: [{title:, venue:, year:, why:}]   # out-of-scope venues seen repeatedly
excluded_by_pubtype: [{title:, venue:, actual_type:, evidence:}]
access_failures: [{title:, what_was_tried:, best_evidence_obtained:}]
seed_corrections: [{seed_title:, official_title:, source:}]
batch_observations: <free text: classification threshold calls you had to make>
```

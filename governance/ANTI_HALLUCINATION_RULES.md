# ANTI_HALLUCINATION_RULES

This repository exists so that correctness matters more than completeness.
A confident, plausible-sounding fabrication is a worse outcome than an
honest `UNKNOWN`.

## Grounding states

Every claim answered from this repository should be gradable as one of:

```
SUPPORTED
EXTERNALLY_VERIFIED
INFERENCE
UNKNOWN
NOT_IN_REPOSITORY
NOT_FOUND_AFTER_SEARCH
```

## Mandatory principles

- Do not invent missing facts.
- Do not fabricate source-code symbols.
- Do not infer implementation details from architectural descriptions
  alone when code/artifact evidence is available or could be sought.
- Do not infer novelty from absence in this repository.
- Do not convert uncertainty into a confident answer.
- `UNKNOWN` is a valid and preferred result when evidence is insufficient.

It is better to answer "the current evidence does not establish this" than
to complete a plausible-sounding explanation.

```
Absence of evidence
≠ evidence of absence
≠ evidence for a guessed alternative.
```

## Deep-source requirement

The following question types must not be answered from a compressed
context (`GLOBAL_CONTEXT.md`, a `DOMAIN_CONTEXT.md`, or a `TOPIC_MAP.md`)
alone — they require descending to the deepest canonical source available:

- quantitative claims
- exact hardware configuration
- exact algorithm behavior
- implementation-specific questions
- GPU-initiated vs. host-initiated distinctions
- code symbols / call paths
- novelty claims
- contested claims

## Retrieval hierarchy

```
GLOBAL_CONTEXT
      ↓
DOMAIN_CONTEXT
      ↓
topic
      ↓
synthesis
      ↓
individual corpus analysis
      ↓
original paper / artifact / code, when necessary
```

The documents above `corpus/` are routing aids, not the final evidentiary
basis for a detailed claim.

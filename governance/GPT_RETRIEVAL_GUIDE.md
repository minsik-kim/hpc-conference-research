# GPT_RETRIEVAL_GUIDE

Standard workflow for a new GPT/Claude session reading this repository.

## Broad question

```
GLOBAL_CONTEXT
  → DOMAIN_CONTEXT
  → TOPIC_MAP
```

## Topic question

```
DOMAIN_CONTEXT
  → topics/<topic>.md
  → relevant synthesis document(s)
```

## Paper-specific question

```
catalog ID
  → individual corpus paper analysis
  → original source/code, if the question requires it (see
    ANTI_HALLUCINATION_RULES.md "Deep-source requirement")
```

## Research-gap question

```
OPEN_QUESTIONS.md
  → domain research-gap map
  → novelty falsification record
  → supporting corpus entries
```

## Governing principle

**Never answer a detailed factual question solely from `GLOBAL_CONTEXT`
when a deeper canonical source exists.** Routing documents (`GLOBAL_CONTEXT`,
`DOMAIN_CONTEXT`, `TOPIC_MAP`) exist to point at the next file, not to
serve as the final evidentiary basis for a specific claim.

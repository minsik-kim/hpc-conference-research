# operational_llm_agents.md

## Scope

Operational use of LLMs/agents in HPC systems operations (e.g., log summarization, incident copiloting, agentic remediation). 20/31 corpus files reference this topic — but this is the topic most heavily subjected to the corpus's own adversarial novelty audit, precisely because overclaiming novelty/capability in this area is a known risk the corpus itself was built to guard against.

## Operational problem

Whether and how LLMs/agents can be usefully and reliably inserted into operational workflows (log triage, incident summarization, remediation suggestion) without introducing new failure modes (hallucinated diagnoses, unsafe automated actions) worse than the problem they aim to solve.

## Research evidence currently in corpus

- `corpus/aiops-survey/synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` [internal adversarial audit] — directly audits novelty claims in this area from the initial synthesis (`00`–`07`).
- `corpus/aiops-survey/synthesis/13_VERIFICATION_ROUND2.md` [internal verification — **current authority**] — corrects/revises specific items first raised in `09` for this topic.

## Production/practitioner evidence currently in corpus

Practitioner/vendor claims about operational-LLM products appear within the CUG/vendor material (`raw/E_cug_vendor.md` [VENDOR]) and are, per the corpus's own discipline, treated with particular skepticism until independently checked — a vendor claiming an "AI-powered ops agent" is `[VENDOR]` evidence, not an independently verified research result, until `09`/`13` say otherwise for that specific claim.

## Known methods (generic domain background)

Log-summarization and RAG-style incident-copilot approaches are the common practitioner framings in this space generally; whether the corpus's own audit finds a specific such claim `CLOSED` (genuinely addressed), `PARTIALLY_ADDRESSED`, `STILL_OPEN`, `ENGINEERING_ONLY`, or `INSUFFICIENT_EVIDENCE` must be read from `09`/`13` directly.

## Research-practice gap

This topic is where the corpus's novelty-falsification discipline matters most — see `research/RESEARCH_GAPS_AND_CANDIDATES.md` and `evidence/EVIDENCE_LINEAGE.md` before treating any operational-LLM claim in this domain as a settled research contribution.

## Evidence limitations

Given the topic's overclaim risk, treat any characterization not traceable to `09` or `13`'s actual verdict as unverified. Do not upgrade a vendor demo or a BoF talk about an "AI ops agent" to a research finding.

## Canonical deeper sources

`synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md`, `synthesis/13_VERIFICATION_ROUND2.md`, `raw/E_cug_vendor.md`.

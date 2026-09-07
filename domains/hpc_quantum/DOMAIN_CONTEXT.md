# DOMAIN_CONTEXT — HPC & Quantum

Status: **PARTIAL** (one imported source project; real coverage below is
uneven across the domain's anticipated scope — see `TOPIC_MAP.md`)

## Scope

`hpc_quantum` is **not** an unbounded quantum-computing domain. Its scope is
the HPC × quantum-computing interface and hybrid-computing research
landscape: VQE/variational algorithms, quantum chemistry workloads, hybrid
quantum-classical workflows, HPC-QPU integration, QPU scheduling/resource
management, distributed quantum simulation, GPU-accelerated quantum
simulation, quantum workflow systems, benchmarking/performance, and the
classical/HPC cost of quantum algorithms. VQE is one topic branch inside
this domain, not the domain itself.

## Current coverage — what this corpus actually is

This domain currently holds **one imported source project**: a
**Quantum-HPC systems research *venue census / research-landscape corpus***
(`corpus/quantum-hpc-survey/`), covering SC 2024–2025 and ASPLOS 2024–2026
main-track regular papers, plus a 21-venue landscape map. It answers *"which
conferences accept what as an HPC contribution in quantum computing, and
why"* — it is **not** a comprehensive VQE or quantum-algorithms literature
review, and it should not be treated as one.

**Strongly covered** (see `TOPIC_MAP.md` for the full table): QEC decoding
as a systems/throughput problem, GPU-accelerated and distributed quantum
circuit simulation, quantum compilation and its classical cost, artifact/
reproducibility discipline. **Moderately covered:** QPU scheduling and
cloud/fleet orchestration, modular/multi-QPU architecture. **Partially
covered, as incidental mentions inside individual paper analyses rather
than a researched topic:** VQE, ansatz, UCC/UCCSD, ADAPT-VQE, measurement
reduction. **Present only as a documented exclusion criterion:** classical
quantum chemistry / many-body physics (the corpus's own dominant
false-positive class — see `topics/variational_algorithms_and_nisq.md`).
**Not present in this workspace at all:** classical-optimizer studies,
initialization/warm-start methods, barren plateaus/trainability, gradient-
estimation methods, excited-state methods. Absence here is `NOT_COVERED`,
not evidence that these topics are unstudied in the wider literature (see
`governance/ANTI_HALLUCINATION_RULES.md`).

## Current corpus status

**One source project imported**, `quantum-hpc-survey`
(`corpus/quantum-hpc-survey/`): 39 files (11 curated corpus documents + 28
raw working-evidence extracts), preserved byte-identically from the staged
import — see that project's own `SOURCE_MANIFEST.md` and
`SOURCE_INVENTORY.md` for full provenance, and `STAGING_CHECKSUMS.sha256`
for the staging-time integrity record.

A separate, unrelated project on the user's own machine
(`hpc-quantum-warmstart-paper`, a CCSD→UCCSD initialization research
project and its own JCTC manuscript) is **not** part of this corpus and was
**not imported**. It is a live research project with its own repository,
not a literature source for this knowledge base. If it is ever cited as
supporting evidence for a claim in this domain, that must be a deliberate,
separately-recorded decision — not an automatic merge.

**`COMPLETE_AS_CURRENT_SOURCE` (this one source project is fully and
faithfully imported) is not the same claim as `COMPREHENSIVE_FIELD_COVERAGE`
(the HPC-Quantum literature has been exhaustively surveyed). This domain is
the former, not the latter.** See `RESEARCH_STATUS.md`.

## Core mental model

The imported corpus's central finding: HPC venues (SC) and architecture
venues (ASPLOS) recognize different things as an "HPC contribution" in
quantum-adjacent work. SC's four acceptance pathways — HPC *is* the
contribution; HPC makes a quantum claim possible; HPC is the cost model of
compilation; HPC is the scarce resource consumed — contrast with ASPLOS's
broader tolerance for analytically-evaluated future architectures and
output-quality-only compilation arguments. See
`corpus/quantum-hpc-survey/corpus/SC_2024_2025_QUANTUM_HPC_CENSUS.md` §7
and `corpus/quantum-hpc-survey/corpus/ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`
§10 for the primary treatment; do not re-derive this from this file alone.

## Major topic families

See `TOPIC_MAP.md` for the full routing table with coverage status. Topic
files that exist: `topics/qec_decoding.md`,
`topics/quantum_simulation_distributed_gpu.md`,
`topics/compilation_and_classical_cost.md`,
`topics/qpu_scheduling_and_orchestration.md`,
`topics/modular_multi_qpu_architecture.md`,
`topics/variational_algorithms_and_nisq.md`,
`topics/benchmarking_and_artifacts.md`. No topic file was created for a
scope item with no coverage in this corpus (see `TOPIC_MAP.md` §3).

## Representative sources

Two full-population regular-paper censuses (SC 2024–2025, 11 papers; ASPLOS
2024–2026, 36 papers), a 21-venue landscape map covering 2024–2026, and a
research queue tracking which venues are censused vs. still pending. Full
list and provenance: `corpus/quantum-hpc-survey/SOURCE_INVENTORY.md`.

## Key synthesis documents

Already exist inside the imported source and were **not rewritten** — see
`synthesis/README.md` for the routing pointer to their canonical location:
`QUANTUM_HPC_VENUE_MAP.md`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`,
`QUANTUM_HPC_RESEARCH_QUEUE.md`, and the two venue censuses themselves
(each contains its own internal cross-year/cross-branch synthesis).

## Current research questions

Not newly generated during this import. The source corpus's own
`VENUE_GAP` / `POSSIBLE_CROSSOVER` / `OPEN_QUESTION` observations are
indexed, with pointers, in `research/CANDIDATE_QUESTIONS.md` and summarized
in `OPEN_QUESTIONS.md`. None has been independently re-falsified during
this import — see `governance/RESEARCH_GAP_RULES.md`.

## Evidence limitations

The imported corpus grades its own claims (`[paper]`, `[paper-preprint]`,
`[code]`, `[official-CFP]`, `[official-program]`, `[proceedings]`,
`[abstract]`, `[documentation]`, `[artifact]`, `[inference]`,
`[reconstruction]`) and records unresolved items explicitly
(`TOTAL_COUNT_UNVERIFIED`, `STATUS_UNCLEAR`, `NOT_FOUND`). These gradings
and unresolved markers were preserved exactly, not promoted. See
`evidence/README.md` for the full list of known limitations carried
forward from the source (abstract-only papers, closed-access papers,
unknown artifact-badge status, single-source denominators, unpublished
MICRO-59 program, and the ISC/ISCA/HPCA/MICRO/ICS censuses that remain
queued but not performed).

## Retrieval instructions

Do not answer a detailed quantitative, mechanism, or contested claim from
this file, `TOPIC_MAP.md`, or a `topics/*.md` file alone — descend to the
cited corpus document (`corpus/quantum-hpc-survey/corpus/...`) per
`governance/ANTI_HALLUCINATION_RULES.md`'s deep-source requirement. Do not
answer a VQE/quantum-algorithms question as if this corpus were a
comprehensive review of that field — it is a systems/venue census in which
VQE appears only as census subject matter.

## Where to look next

- For topic questions: `TOPIC_MAP.md` → `topics/<topic>.md`
- For individual paper/venue detail: `corpus/quantum-hpc-survey/corpus/...`
- For raw provenance/extraction evidence: `corpus/quantum-hpc-survey/working-evidence/...`
- For research questions: `OPEN_QUESTIONS.md` → `research/CANDIDATE_QUESTIONS.md`
- For third-party code/artifact provenance: `implementation/ARTIFACT_REGISTRY.md`
- For import/coverage status: `RESEARCH_STATUS.md`

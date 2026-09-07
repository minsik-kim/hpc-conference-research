# DOMAIN_CONTEXT — HPC & Quantum

Status: **STRUCTURE_ONLY — CONTENT NOT YET IMPORTED**

## Scope

`hpc_quantum` is **not** an unbounded quantum-computing domain. Its scope is
the HPC × quantum-computing interface and hybrid-computing research
landscape:

- VQE / variational algorithms
- quantum chemistry workloads
- hybrid quantum-classical workflows
- HPC-QPU integration
- QPU scheduling / resource management
- distributed quantum simulation
- GPU-accelerated quantum simulation
- quantum workflow systems
- benchmarking / performance
- classical / HPC cost of quantum algorithms

VQE is one topic branch inside this domain, e.g.:

```
HPC & Quantum
└── VQE
    ├── UCCSD
    ├── initialization / warm-start
    ├── classical optimization
    ├── CCSD trajectory
    └── hybrid classical-quantum cost
```

## Current coverage

None imported into this repository yet.

## Current corpus status

No literature corpus has been imported into this domain. Separate,
unrelated git repositories on the user's own machine
(`hpc-quantum-warmstart`, `hpc-quantum-warmstart-paper`) contain an active
CCSD→UCCSD initialization research project and its JCTC manuscript — those
are a research project's own working repositories, not a literature corpus
for this knowledge base, and are explicitly out of scope for import here
unless a future, separate decision says otherwise. Do not treat this
domain as populated based on that project's existence.

## Core mental model

Not established.

## Major topic families

Anticipated (not yet created) topic files: `topics/vqe.md`,
`topics/variational_algorithms.md`, `topics/quantum_chemistry.md`,
`topics/hybrid_quantum_classical.md`, `topics/hpc_qpu_integration.md`,
`topics/distributed_quantum_simulation.md`, `topics/quantum_workflows.md`,
`topics/benchmarking.md`, `topics/resource_management.md`.

## Representative sources

None.

## Key synthesis documents

None.

## Current research questions

None recorded — see `OPEN_QUESTIONS.md`.

## Evidence limitations

This domain has no evidence base. Any question in this scope should be
reported as `NOT_IN_REPOSITORY`.

## Retrieval instructions

Do not answer HPC-quantum/VQE questions from this file or from general
knowledge. Report `NOT_IN_REPOSITORY` / `STRUCTURE_ONLY`.

## Where to look next

Nothing to route to yet. Once content exists: `RESEARCH_STATUS.md` for
import status, `TOPIC_MAP.md` for topic routing, `corpus/` for individual
source detail, `OPEN_QUESTIONS.md` and `research/` for research questions,
`implementation/` for implementation resources.

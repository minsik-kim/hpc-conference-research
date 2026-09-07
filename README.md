# hpc-conference-research — Research Landscape Knowledge Base

## Purpose

A grounded, external-memory research repository for interactive AI-assisted
learning and research. It is designed to be read by Claude/GPT sessions as
a canonical knowledge source — not regenerated from a model's training data,
and not completed by guessing where evidence is thin.

## Domains

- **AI/HPC Systems** (`domains/ai_hpc_systems/`) — distributed training, GPU
  communication/collectives, MoE, long-context attention, parallelism,
  runtime, network/fabric, memory/offload/CXL, GPU compiler/kernel, serving,
  performance analysis. Status: `EXTERNAL_IMPORT_PENDING` (an ~80-paper
  conference corpus and synthesis exist in a separate workspace and are not
  yet imported here — see `domains/ai_hpc_systems/DOMAIN_CONTEXT.md`).
- **HPC Systems & Operations** (`domains/hpc_systems_operations/`) —
  production HPC operations, telemetry, monitoring, observability, AIOps,
  anomaly detection, failure prediction, RCA, scheduler/network/storage/GPU
  operations, power/cooling, automated remediation. Status: `STRUCTURE_ONLY`.
- **HPC & Quantum** (`domains/hpc_quantum/`) — the HPC × quantum-computing
  interface: VQE/ansatz/UCC-UCCSD, quantum chemistry workloads, hybrid
  quantum-classical workflows, HPC-QPU integration, distributed/GPU-
  accelerated quantum simulation, quantum workflow systems, benchmarking,
  and the classical/HPC cost of quantum algorithms. VQE is a topic inside
  this domain, not a top-level domain. Status: `STRUCTURE_ONLY`.

## Principles

- Evidence before inference.
- `UNKNOWN` / `NOT_IN_REPOSITORY` is a valid and preferred answer over a
  fabricated one.
- Canonical-source retrieval: never stop at a compressed summary when a
  deeper source exists for a detailed or contested claim.
- Stable source IDs, never reused.
- Synthesis and topic documents are living documents; corpus/evidence
  documents are append-oriented.
- Git history is the versioning mechanism — not `_v2`/`_v3` filename forks
  (unless a historical snapshot is deliberately preserved).

## Start here

`GLOBAL_CONTEXT.md`

## Current state (this repository)

This repository was bootstrapped as a **structure-only** knowledge base.
No conference corpus, synthesis, or evidence content has been imported yet.
The existing ~80-paper AI/HPC systems corpus and its synthesis/audit
documents live in a separate external workspace and are pending import in a
future session — see `GLOBAL_CHANGELOG.md` and each domain's
`DOMAIN_CONTEXT.md` for exact status.

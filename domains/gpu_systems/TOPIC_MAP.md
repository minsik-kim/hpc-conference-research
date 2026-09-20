# TOPIC_MAP — GPU Systems

<!-- Routing only. Do not put findings here; they belong in topics/ and synthesis/. -->

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-19

## How to use this file

Pick the topic, then read `topics/<topic>.md`, then descend to the corpus files
it cites. This file is a routing aid and, per
[`governance/ANTI_HALLUCINATION_RULES.md`](../../governance/ANTI_HALLUCINATION_RULES.md),
never the evidentiary basis for a detailed claim.

A topic file exists only where the corpus holds real, grep-verifiable evidence
— the rule this repository already applies in `hpc_systems_operations`. "Own
members" counts the deep analyses whose primary topic is that area; "cites"
counts the distinct corpus files the topic file draws on, including ones owned
by a neighbouring topic.

## Topic routing table

| Topic | Taxonomy | Own members | Cites | Coverage |
|---|---|---|---|---|
| [`topics/gpu_core_execution.md`](topics/gpu_core_execution.md) | A + B | 8 | 10 | Warp/SIMT execution, instruction issue, register files, schedulers, on-chip interconnect, chiplet/MCM. Mixed measured and simulated; the measured papers dispute the simulated baseline. |
| [`topics/memory_virtualization.md`](topics/memory_virtualization.md) | C + D | 8 | 8 | Caches, TLBs, address translation, UVM, oversubscription, migration, multi-GPU memory. Both vendors represented. |
| [`topics/data_movement_compression.md`](topics/data_movement_compression.md) | E | 7 | 9 | HBM and data movement, GPU lossy/lossless compression, GPU–storage and GPU–host I/O. **Thin sub-area:** the GPU–storage path rests on one paper. |
| [`topics/tensor_cores.md`](topics/tensor_cores.md) | F | 9 | 12 | Matrix units, numeric formats, precision emulation, matrix units for non-GEMM kernels. **Gap:** the numeric-format branch has no deep analysis. |
| [`topics/sparse_irregular.md`](topics/sparse_irregular.md) | G | 7 | 8 | Sparse and irregular GPU kernels, formats, load balancing, graph workloads. |
| [`topics/compiler_programming.md`](topics/compiler_programming.md) | H + I | 7 | 12 | Compilers, programming models, IR and lowering, kernel fusion, memory models, language-level safety. |
| [`topics/runtime_scheduling.md`](topics/runtime_scheduling.md) | J + K | 6 | 7 | Runtime, task graphs, scheduling, GPU sharing, MIG/MPS/virtualisation. **Thin sub-area:** taxonomy J (task graphs) rests on one paper. |
| [`topics/multi_gpu_communication.md`](topics/multi_gpu_communication.md) | L + M | 9 | 10 | Interconnect and data paths, GPU-aware and GPU-initiated communication, collectives. |
| [`topics/profiling_debugging.md`](topics/profiling_debugging.md) | N | 5 | 8 | Profiling, debugging, correctness checking, simulation, performance modelling. |
| [`topics/reliability_operations.md`](topics/reliability_operations.md) | O | 4 | 6 | GPU faults, ECC/row remapping, telemetry, production performance and variability. |
| [`topics/power_energy.md`](topics/power_energy.md) | P | 7 | 10 | Power, energy, DVFS, thermal behaviour, energy attribution and its instrumentation. |
| [`topics/fixed_function_repurposing.md`](topics/fixed_function_repurposing.md) | Q | 8 | 8 | RT cores, texture and rasterisation hardware used for general computation. **Category added during this work**; the file argues why. |

Own members sum to 85, the full set of deep analyses. Every corpus file is
cited by at least one topic file.

## Taxonomy as used here

The initial taxonomy was A–P. Two changes were made against evidence and are
recorded rather than silently applied:

- **Q was added** — fixed-function GPU units repurposed for general
  computation. Defined by mechanism, not by workload: obtaining
  non-original-purpose value from a unit whose function is frozen in silicon
  for graphics, either by reformulating the problem into its fixed predicate
  (software mapping) or by widening that predicate at minimum marginal area
  (hardware generalisation). Its members share no application domain, so A/B
  would have scattered them.
- **Pairs were merged for routing** where the corpus showed no clean seam:
  A with B, C with D, H with I, J with K, L with M, N with O. The pairs remain
  distinguishable inside each topic file and in each analysis's
  `primary_topic`; the merge is a routing convenience, not a claim that the
  distinctions are empty.

## Cross-topic routes

Several findings sit between topics. Follow these rather than duplicating them:

- MIG isolation is discussed in **runtime_scheduling** (the partitioning
  schools) and in **memory_virtualization** (the unpartitioned L3 TLB) and in
  **power_energy** (the unpartitioned power/clock domain). The three together
  are what the finding is.
- Page-table walking on the ray-tracing accelerator belongs to both
  **memory_virtualization** (verdict of record) and
  **fixed_function_repurposing** (mechanism family). That it cross-cuts is
  itself the argument for category Q.
- Compression appears in **data_movement_compression** (standalone
  compressors) and **multi_gpu_communication** (compression inside
  collectives). The corpus verified these are separate, mutually non-citing
  communities — do not merge them.
- Device-resident control appears in **multi_gpu_communication** (GICC),
  **memory_virtualization** (DREAM), **runtime_scheduling** (device-side task
  graphs) and **data_movement_compression** (GPU-initiated NVMe). The host
  being removed from four control paths it historically owned is one story
  told in four topic files.

## Not covered

No topic file was created for these, because the corpus has no deep-analysis
evidence for them, only ledger rows: GPU security and side channels as a field
in its own right (several papers were screened and adjudicated but none
survived to a deep analysis); homomorphic encryption on GPUs (a large 2026
cohort, entirely behind publisher access); and mobile/edge GPU architecture
beyond the two rendering papers in category Q. Absence here is `NOT_COVERED`,
not evidence that these are unstudied — see
[`governance/ANTI_HALLUCINATION_RULES.md`](../../governance/ANTI_HALLUCINATION_RULES.md).

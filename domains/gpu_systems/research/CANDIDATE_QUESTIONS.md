# CANDIDATE_QUESTIONS — GPU Systems

last_updated: 2026-09-19

Every item is `CANDIDATE` status. See `../OPEN_QUESTIONS.md` for the items
themselves and `../../../governance/RESEARCH_GAP_RULES.md` for why none has
been promoted: no own-corpus cross-check, closest-work search, external
targeted search or novelty falsification has been performed for any of them.

This file exists to record **where each observation came from**, so that a
later falsification pass starts from evidence rather than from the claim.

| Item | Source of the observation | What would have to be done first |
|---|---|---|
| A1 issue-stage model | `../corpus/_LEDGER_core_execution.md` cross-paper findings §1; both analyses' §12.14 | Re-evaluate the proposal on the measured core model; check whether either group has since responded |
| A2 Blackwell FP64 | `../corpus/_LEDGER_tensor_cores.md` finding (b); `../synthesis/GPU_HARDWARE_GENERATION_MAP.md` | Establish whether the two figures refer to the same silicon; find vendor documentation |
| A3 symmetric memory | `../corpus/_LEDGER_multi_gpu_communication.md` finding 2 | Check for a later paper resolving it; both claims are version- and hardware-specific |
| A4 MIG isolation | `../corpus/_LEDGER_runtime_sharing.md` finding 3, joining a memory-cluster and an ISC 2026 result | A single-device study measuring both channels |
| B1 compression communities | `../corpus/_LEDGER_data_movement_compression.md` finding 4, verified in both directions | Full bibliometric check rather than targeted query |
| B2 sparse ↔ RT-unit | `../corpus/_LEDGER_sparse_irregular.md` finding 4, targeted query on two papers | Widen the query set; check the RT-unit side symmetrically |
| B3 correctness literatures | `../corpus/_LEDGER_compiler_programming.md` finding 5 | Include PL venues outside this corpus's ten |
| B4 same-cycle duals | `../corpus/_LEDGER_profiling_reliability.md` finding 2; `../corpus/_LEDGER_tensor_cores.md` finding (c) | Check the following year's versions, where citation would be possible |
| C1 missing rooflines | `../corpus/_LEDGER_data_movement_compression.md` finding 2 | Confirm across the unread compression papers before generalising |
| C2 power ground truth | `../corpus/_LEDGER_power_energy.md` finding 1 and its instrumentation roll-up | Confirm the non-citation of the sampling-window study across a wider set |
| C3 no AMD sensor study | `../corpus/_LEDGER_power_energy.md` finding 2 | Search AMD-specific venues outside this corpus's ten |
| C4 sharing schools | `../corpus/_LEDGER_runtime_sharing.md` finding 1 | Establish whether any paper does compare them |
| C5 unsupported driver interface | `../corpus/_LEDGER_runtime_sharing.md` finding 2, read from the artifact's own header | Check the interface's current status upstream |
| D1 telemetry vs slowdown | `../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md` | Nothing — this is a published falsification, not a gap |
| D2 communication ladder | `../synthesis/GPU_COMMUNICATION_STACK.md` | Nothing — recorded so it is not re-proposed |
| D3 Tensor-Core progression | `../synthesis/GPU_TENSOR_CORE_LINEAGE.md` | Nothing — recorded so it is not re-proposed |

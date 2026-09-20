# GPU core and warp/SIMT execution (taxonomy A/B)

last_updated: 2026-09-18
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **STRONG for 2024–2026, and unusually self-contradictory.**
Eight deep analyses (`A` = 7, `B` = 1), all `CORE_GPU`, all `PUBLIC_FULLTEXT`.
Verdict ledger: `../corpus/_LEDGER_core_execution.md`.
Scope: warp/wavefront execution, SIMT pipelines, instruction issue, register
files, warp schedulers, on-chip interconnect, chiplet/MCM.

> Taxonomy note: the letters `A`/`B` come from this pass's cluster assignment.
> **No A–Q taxonomy file exists in this repository** — `NOT_IN_REPOSITORY`, as
> `../corpus/_LEDGER_core_execution.md` states in its own header.

## 1. Problem landscape

A GPU core issues one instruction per warp per scheduler cycle from the head of
an instruction buffer, resolves dependences through some mechanism, reads
operands through some staging structure, and hides latency by switching among
resident warps. Every one of those four clauses is contested inside this
corpus, and the contest is not between the papers and the field — it is
between the corpus's own simulator-based papers and its own real-silicon
dissections.

The 2024→2026 direction of travel recorded in `../corpus/_LEDGER_core_execution.md`
§3.2 is from **proposing mechanisms in simulation** toward **measuring what
vendors already shipped**. `SUPPORTED`, and it is the most useful single fact
this topic carries: a 2024 simulator result and a 2026 microbenchmark result
about "the GPU core" are not commensurable evidence.

## 2. Key concepts

Warp / wavefront; SIMT lanes and control-flow divergence; instruction buffer
and issue eligibility; **scoreboard vs compiler-set control bits** as the
dependence mechanism; **operand collector** as an operand-staging structure;
register-file banking, ports and a register-file cache; ABI-forced register
spill/fill to local memory; occupancy as warps-resident-per-SM; matrix
instruction **issue scope** (warp / warp-group / warp again); the on-chip
network between SMs and L2 slices, and the partition/GPC/TPC/CPC hierarchy
built on top of it.

## 3. Main mechanism families

**Family 1 — widen what a warp may issue, without a CPU out-of-order core.**
GhOST (`../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md`)
evaluates the ready condition over up to **8 buffered instructions per warp**
instead of only the head, with no renaming, no reorder buffer, no load-store
queue and no branch speculation `[paper]`.

**Family 2 — move a cost out of the memory path and into the register file.**
CARS (`../corpus/GPU-MICRO24-61--cars-concurrency-aware-register-stacks-gpu-function-calls.md`)
keeps the function-call stack in the register file rather than paying the ABI's
callee-saved spill traffic `[paper]`.

**Family 3 — measure the shipped part and correct the model.**
`../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md`,
`../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md`,
`../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md` and
`../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md`.
This family is the corpus's largest in this topic and its conclusions are
what put the first two families in doubt.

**Family 4 — take SIMT off the GPU.**
`../corpus/GPU-MICRO24-62--threadfuser-simt-analysis-framework-mimd-programs.md`
projects what SIMT efficiency an unmodified MIMD CPU binary would have;
`../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md`
runs already-written GPU kernels on CPUs and undoes the GPU-specific source
properties. Both treat SIMT as a *property of a program*, not of a chip.

## 4. Representative papers

- **GhOST** (ISCA 2024) — `../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md`.
  **SIMULATED** (Accel-Sim, SASS traces). Geomean **6.9% on an RTX 2060S
  configuration (32 warps/SM max)** vs **5% on an RTX 3070 configuration
  (48 warps/SM max)** — benefit is *inversely* correlated with occupancy
  `[paper]`. Stall reduction 22–94% across benchmarks. The limit study puts
  unbounded renaming at **15.1%** against GhOST's realised 6.9% `[paper]`.
  Its most transferable result is methodological: re-measured **on SASS**,
  the predecessor LOOG shows a **16.5% geomean slowdown**, worst case 0.35×,
  where the original LOOG paper reported a 16% speedup **on PTX** `[paper]`.
- **CARS** (MICRO 2024) — `../corpus/GPU-MICRO24-61--cars-concurrency-aware-register-stacks-gpu-function-calls.md`.
  **SIMULATED** (Accel-Sim + AccelWattch, V100 configuration, 22 apps).
  Geomean **1.26×** performance, **1.28×** energy efficiency `[paper]`.
  Measures **40.4% of in-core L1D accesses on a V100 configuration** as ABI
  register traffic, and shows an idealised *unlimited-register* machine
  recovers only **1.06×** — the cost is the memory *instructions*, not
  capacity `[paper]`. On an **RTX 3070 (Ampere) configuration** MST gets
  **1.21×** against **3.82×** on V100, because Ampere's occupancy constraints
  force the Low-watermark policy `[paper]`.
- **Dissecting and Modeling Modern GPU Cores** (MICRO 2025) —
  `../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md`.
  **SIM + MEAS** (measurement used to fix the simulator). Measures the
  Accel-Sim baseline at **34.03% MAPE against a real RTX A6000** and finds
  real Turing/Ampere/Blackwell cores use **compiler control bits, not a
  scoreboard**, with **no operand collector units** `[paper]`. Control bits
  cost **0.09% of the register file**; a 63-consumer scoreboard costs
  **2.28%** `[paper]`.
- **Uncovering Real GPU NoC Characteristics** (MICRO 2024) —
  `../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md`.
  **MEASURED** on A100/H100 by SM pinning and correlation clustering. Finds a
  hierarchical crossbar, not the simulated 2D mesh; near-uniform per-SM
  bandwidth to each L2 slice (σ = 0.147 per SM, 0.06 per GPC); latency
  non-uniformity up to **70%** and roughly **2×** for crossing the A100/H100
  central partition; an A100 far-partition bandwidth penalty of **≈26 vs
  ≈39.5 GB/s at low SM counts that vanishes at about 8 SMs** `[paper]`.
- **Hopper microbenchmarking** (IPDPS 2024) — `../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md`.
  **MEASURED**. `wgmma` with `m64nNk16` shapes reaches **>95% of peak** while
  `mma`'s `m16n8k16`/`m16n8k8` shapes average **62.9%** — instruction *shape*,
  not the tensor core, is the limiter `[paper]`. **H800 is up to 13× faster
  than A100/RTX 4090 on 16-bit DPX** `[paper]`.
- **Blackwell B200 microbenchmarking** (IPDPS 2026) — `../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md`.
  **MEASURED**, B200 against an H200 baseline: FP64 DGEMM **36.3 vs 18.9
  TFLOP/s (1.92×)**, FP16 tensor **1929.6 vs 1515.2 TFLOP/s (1.27×)**,
  GPT-1.3B training **14,363 vs 9,240 tok/s (1.55×)** `[paper]`. States that
  Accel-Sim and GCoM **cannot** model TMEM or the decompression engine
  `[paper, via ../corpus/_LEDGER_core_execution.md §3.2]`.
- **ThreadFuser** (MICRO 2024) — `../corpus/GPU-MICRO24-62--threadfuser-simt-analysis-framework-mimd-programs.md`.
  Projections from x86 traces onto an RTX 3070 configuration; the
  HDSearch-midtier case study moves SIMT efficiency from **7% to 90% while
  retaining 93% search accuracy** by fixing the result count to 10 `[paper]`.
  Honest failure mode: at `-O2`/`-O3` the analyser *overestimates* efficiency,
  because GCC unrolling and jump tables make the x86 trace look more uniform
  than the SIMT execution would be `[paper]`.
- **Unleashing CPU Potential** (MICRO 2024) — `../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md`.
  **No GPU is executed at any point** `[paper]`. Geomean **20.84% on two Intel
  Gold 6226R** and **16.10% on a Fujitsu A64FX**; tail-block adaptive
  synchronisation is worth **25.23% on ARM and ≈0 on x86**, because x86 has
  masked load/store and A64FX does not `[paper]`.

## 5. Historical lineage

Two lineages are verified from the papers' own text in
`../corpus/_LEDGER_core_execution.md` §3:

**Matrix-instruction issue scope widened, then narrowed.** Warp-scope `mma`
(Ampere/Ada) → **warp-group** `wgmma` (Hopper, 128 threads, **128 cycles at
`m64n256k16`**) → back to **warp-scope** `tcgen05.mma` (Blackwell B200,
**11.4 cycles at `m256n256k16`**), with the removal of warp-group
synchronisation named as a cause of the latency drop. Accumulator placement
moved the other way: register file → register file → **TMEM**. Visible only by
reading `GPU-IPDPS24-61` and `GPU-IPDPS26-61` together `[paper, both]`.

**Out-of-order GPU issue**: LOOG (PTX-evaluated) → GhOST (SASS-evaluated,
diagnoses LOOG's failure as *operand-collector congestion*) → and then
`GPU-MICRO25-61` reports that real cores have no operand collector at all.
The lineage ends in a contradiction rather than a synthesis (see §7).

## 6. Implementation families

`SIMULATOR` (Accel-Sim / GPGPU-Sim / AccelWattch / MGPUSim): GhOST, CARS,
ThreadFuser's projections. `REAL_SILICON_DISSECTION`: the GPU NoC paper,
Hopper, Blackwell B200, and `GPU-MICRO25-61` (which uses measurement *to fix*
the simulator). `CPU_ONLY`: `GPU-MICRO24-64`. Per
`../../../governance/SOURCE_EVIDENCE_RULES.md`, simulated area and power figures in
this topic are never reported as measured.

## 7. Important disagreements / tensions

**T1 — the core model itself is contested, and neither side evaluated against
the other.** `SUPPORTED`, recorded verbatim in
`../corpus/_LEDGER_core_execution.md` §3.1. GhOST builds on Accel-Sim's
scoreboard-plus-operand-collector core and diagnoses LOOG's failure as
operand-collector congestion. `GPU-MICRO25-61` measures that same baseline at
**34.03% MAPE against a real RTX A6000** and finds real cores use compiler
control bits and have **no operand collector units** — because a compiler-set
stall counter requires statically known issue-to-writeback latency, which an
operand collector would destroy. **Any future work in this topic must state
which core model it assumes.** The same tension applies to the unread
*Warped-Compaction* (HPCA 2025, `CLOSED_ACCESS` in the ledger).

**T2 — simulated GPU NoCs and real GPU NoCs are wrong in opposite
directions.** `GPU-MICRO24-63`: simulated meshes are *slower* than real
hierarchical crossbars (up to 2.4× throughput spread under round-robin
arbitration on a 6×6 mesh, against near-uniform real per-SM bandwidth), **and**
simulated GPUs miss a real cost — up to 70% latency non-uniformity and a ~2×
central-partition crossing penalty that no idealised model charges `[paper]`.
A GPU-NoC proposal evaluated only in simulation may be solving a
simulator artefact.

**T3 — one fact in this topic is corroborated twice by different methods, and
it is worth more than the rest.** Partitioned-L2 non-uniformity: measured by
SM pinning and correlation clustering (~200 vs ~400 cycles across an A100/H100
partition, plus TPC/GPC and an undocumented **CPC** level on H100) in
`GPU-MICRO24-63`, and by p-chase (near/far hit **208 / 356.6 cycles on A100**,
**258 / 414.1 on H800**) in the Hopper line. Different methods, same structure
`[../corpus/_LEDGER_core_execution.md §3.4]`.

**T4 — power is an unlisted confound under every instruction-throughput number
here.** `GPU-IPDPS24-61` shows H800 `wgmma` throughput depends on the
*contents* of the input matrices: zero-initialised inputs draw **under 200 W**
and reach **>95% of peak**; random inputs hit the **350 W** limit and drop the
clock below the **1620 MHz** whitepaper figure `[paper]`. The paper reports
matrix throughput as `Total_OPS / Duration` rather than in cycles precisely to
expose this. **A Hopper matrix-throughput number reported without its input
distribution is not reproducible.**

## 8. Current limitations

**Access, not the field, bounds this topic.** Of the papers adjudicated in
`../corpus/_LEDGER_core_execution.md`, the following are `CLOSED_ACCESS` *in
this environment* with no preprint found — WASP (HPCA'24), Warped-Compaction
(HPCA'25), Atomic Cache (MICRO'24), CPElide (MICRO'24), LRM-GPU (HPCA'26),
NearFetch (HPCA'25), sCROOGe (ISCA'26), DICE (ISCA'26), Ghost Arbitration
(MICRO'24), Veiled Pathways (MICRO'24), Big Integer Multiplication (MICRO'24),
Lit Silicon (ISCA'26, later obtained and analysed by the power cluster as
`../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md`).
LazyGPU and UGPU (both ISCA'25) are **open access on ACM DL and still
unreachable from here** — `PENDING_FULLTEXT`, not `CLOSED_ACCESS`. That is an
access-path fact about this environment, not a statement about licence.

Consequence: the **chiplet/MCM half of taxonomy B is effectively absent**. One
deep analysis covers `B` (the NoC characterisation paper), and it is
single-die. Multi-die interconnect appears in this corpus only through
`../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md`
(translation, not the core) and `../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md`
(thermal). **Do not read that absence as a gap in the field**
(`../../../governance/ANTI_HALLUCINATION_RULES.md`).

**Existence unverified**: *Attention, Watch Your Progress: Balancing Warp
Specialized GPU Pipelines* (MICRO 2026 seed) reproduced as `NOT_FOUND`;
recorded `UNRESOLVED` and **not to be cited as an attested paper**.

## 9. Research questions

Derived, and flagged as `INFERENCE`, from the tensions above — none has been
falsified against the corpus:

1. Does GhOST's 6.9% survive on a control-bit core with no operand collector?
   Neither paper answers, and the two evaluations are one year apart. (T1)
2. Register spill/fill became a first-class GPU cost in 2024 on two independent
   MICRO papers (`GPU-MICRO24-61` measures 40.4% of in-core L1D accesses as ABI
   traffic on a V100 configuration; `GPU-MICRO24-62` names CPU-compiler
   register allocation causing "unnecessary spills/fills" under SIMT). Does the
   compiler-managed register-file *cache* that `GPU-MICRO25-61` found in real
   Turing/Ampere silicon already absorb it? Neither cites the other.
3. What should a GPU-NoC proposal be evaluated on, given T2?

## 10. Deeper lookup paths

`../corpus/_LEDGER_core_execution.md` (verdicts, access states, §3 cluster
observations, §4 blocked items) → the individual analyses cited above → the
papers' own artifacts where a commit is pinned in §12.8 of each analysis.
For anything quantitative, hardware-configuration-specific, or contested,
descend to the corpus file and then to the paper — not to this file
(`../../../governance/ANTI_HALLUCINATION_RULES.md`, "Deep-source requirement").

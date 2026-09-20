# Multi-GPU interconnect, GPU-aware and GPU-initiated communication, and collectives (taxonomy L/M)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **STRONG, and it overturns the framing it was given.**
Nine deep analyses (`L` = 2, `M` = 7). Verdict ledger:
`../corpus/_LEDGER_multi_gpu_communication.md`; stack-level synthesis:
`../synthesis/GPU_COMMUNICATION_STACK.md`.

## 1. Problem landscape

The organising question this cluster was set — is the field traversing a
progression from *GPU-aware MPI → device-initiated communication → symmetric
memory → GPU-resident collective control*? — is answered in the ledger as
**NOT SUPPORTED as a progression** (§7, T1). What the citations do support is a
**two-axis map**: *who initiates* (host-driven / device-triggered /
device-resident) × *which fabric is crossed* (intra-node peer-mapped /
intra-node switch / scale-out RDMA) — and **the fabric axis, not the year,
predicts the initiation axis**.

The second thing this corpus establishes, independently and from three
directions, is that **vendor defaults are not the best choice** (§7, T3).

## 2. Key concepts

Control placement: **host-driven**, **GPU-triggered** (the host pre-stages
bounded work; the GPU rings a doorbell) and **device-resident** (kernels build
work-queue elements themselves) — a distinction GICC coins because it needed
it; NVLink / NVSwitch / xGMI / Infinity Fabric / PCIe / Slingshot / InfiniBand
as distinct fabrics; symmetric memory and PGAS/SHMEM; in-fabric reduction
(`multimem.ld_reduce`, `multimem.red.release.sys.add.u64`, NVLink SHARP);
LL / LL128 flag-in-data protocols; GPUDirect Async Kernel-Initiated (GDAKI);
ring vs recursive-doubling/halving vs tree algorithm families; goodput vs
latency by transfer size; speed-of-light (SoL) bounds.

## 3. Main mechanism families

**Family L1 — measure the fabric, then plan against what you measured.**
`../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md`
(characterisation) and
`../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md`
(execution-time multipath planning).

**Family M1 — overlap compute and collective without software synchronisation.**
`../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md`
(a hardware tracker; store completion in a tracked range *is* the readiness
signal).

**Family M2 — give the programmer better primitives than a monolithic library.**
`../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md`.

**Family M3 — move coordination, not data, onto the device.**
`../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md`.

**Family M4 — change the algorithm, stay host-initiated.**
`../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md`
(PCCL: hierarchical recursive doubling/halving).

**Family M5 — delete the barrier inside a scale-up domain.**
`../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md`.

**Family M6 — send fewer bytes.**
`../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md`.

**Family M7 — benchmark the whole space so the others can be adjudicated.**
`../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md`.

## 4. Representative papers

- **Exploring GPU-to-GPU Communication** (SC 2024) — **MEASURED** on
  **Alps, LUMI-G and Leonardo**. Its substantive result is that **the direction
  of the MPI-vs-NCCL answer flips between operation class and system**
  `[paper]`: GPU-aware MPI beats NCCL for intra-node point-to-point on Leonardo
  (4× A100, NVLink 3.0 + PCIe Gen4) by up to **2×** at medium sizes; beats RCCL
  for small intra-node collectives on LUMI-G (MI250X GCDs, Infinity Fabric) by
  up to **3×**; beats NCCL for inter-node point-to-point by **up to one order
  of magnitude on small transfers**; **but NCCL wins intra-node collectives on
  Alps and Leonardo at all transfer sizes**. RCCL delivers **less than half**
  GPU-aware MPI's goodput on the specific GPU0↔GPU5 GCD pair on LUMI-G,
  attributed to a bandwidth-estimation defect. Placement sensitivity is
  system-dependent: ~**2×** average latency increase across Dragonfly+ groups
  on Leonardo (InfiniBand HDR, 23 groups) versus **<30% latency and <1%
  goodput** on Alps/LUMI-G (Slingshot-11). NCCL sustains ~**75% alltoall
  efficiency to 1,024 GPUs** on Alps and Leonardo.
- **NIMBLE** (IPDPS 2026) — **MEASURED** on **H100-SXM4 nodes, fully connected
  NVLink 4, four NDR400 InfiniBand rails per node, 2–8 nodes**. **Intra-node
  2.3× higher bandwidth vs single-path: 120 GB/s → 278.2 GB/s** `[paper]`.
  Honest scoping: performance merely **matches** baselines under balanced
  traffic, and **multi-pathing is disabled for messages ≤1 MB** — "a
  skew-and-large-message technique, not a general improvement".
- **T3** (ASPLOS 2024) — **SIMULATED**, stated 6% modelling error.
  **30% geomean (max 47%) speedup on communication-heavy sublayers** for
  Mega-GPT-2 and T-NLG at **TP=8 and TP=16** `[paper]`. Requires
  **compute-enhanced / near-memory-compute memory** that the paper itself says
  "is not yet standard in production GPUs", plus a new programmable tracker and
  a new memory-controller arbitration policy. **NVLink generation, switch
  topology and per-link bandwidth are `UNKNOWN` in the read text** — a genuine
  gap relative to every measured paper in this topic.
- **MSCCL++** (ASPLOS 2026) — **MEASURED** on A100/H100/GB200-class parts.
  AllReduce on single-node **A100-40G (8 GPUs, NVLink 3.0, no NVSwitch)**: up
  to **3.5× vs NCCL** and **2.1× vs MSCCL** for ≤1 MB (1 KB: **9.5 µs → 5.0 µs,
  47% latency reduction**); up to **1.6× / 1.4×** for ≥1 MB `[paper]`. Where it
  is *not* faster: **DSL-generated algorithms average 3% slower than
  hand-written and up to 18% worse in corner cases**. In-switch reduction read
  in the artifact as `multimem.red.release.sys.add.u64`
  (`include/mscclpp/semaphore_device.hpp:174`) `[code]`.
- **GICC** (HPDC 2026) — **MEASURED** on **GH200 / H200 / MI250X** across
  mlx5 InfiniBand and HPE Slingshot CXI. Coins **"GPU-triggered rather than
  GPU-initiated"** because the *same runtime* is device-resident on mlx5
  (kernels build work-queue elements and ring the User Access Region doorbell)
  and only device-*triggered* on CXI (the host pre-stages bounded operations in
  a **256-entry Deferred Work Queue against a 2047-counter budget**; the GPU
  merely rings a doorbell) `[paper]`. **Carries its own negative result:
  GASNet-EX beats GICC on single-message active-message latency — 3.45 µs vs
  11.76 µs on InfiniBand** `[paper, Table 3]`. Canonical Cannon matmul shows
  minimal benefit; the OFI path retains a host monitor thread at ~1 µs per
  operation.
- **PCCL / The Big Send-off** (IPDPS 2026) — **MEASURED** at scale.
  **All-gather, 256–512 MB per GPU: up to 33× vs RCCL on Frontier at 2,048
  MI250X GCDs**; **up to 5.7× vs NCCL on Perlmutter at 2,048 A100s** `[paper]`.
  **The asymmetry is the finding**: all-reduce on Perlmutter gains only ~1.3×
  because NCCL already uses log-latency tree algorithms there — the improvement
  is specific to collectives where the vendor offers **only ring**. Fully
  host-initiated.
- **PICO** (ISC 2026) — **MEASURED** on **Leonardo, LUMI and MareNostrum 5**.
  Default algorithm ≠ best algorithm: **30–40% typical loss, up to 5× worst
  case**; **`UCX_MAX_RNDV_RAILS` 2→4 changes allreduce performance by >2× at
  2,048 nodes**; buffer management is **~50% of allreduce runtime on Leonardo**
  at ≥1 MiB `[paper]`. *Carry the provenance split*: the census/official
  abstract additionally reports "reductions in training times of up to 44%",
  and **that figure was not found in the arXiv text read here**, so it is
  `[census]` `[official-web]` evidence, not `[paper]`.
- **Every Microsecond Matters** (SC 2026) — **MEASURED** on **GB200**.
  Derives `L_SoL = 2·L_L2_RTT + L_remote_store = 1.404 µs` on two GB200 and
  measures barriers at **>1 µs, ~40% of a 5 µs small-message AllReduce**
  `[paper]`. Overhead reduced to within **7% of the absolute SoL lower bound at
  2 GPUs**, but **~70% above SoL at 64 GPUs** — the gap widens with scale.
  vLLM long-context decode (100–200k input, 16K output, batch 8) on GB200:
  **7–13%** end-to-end. Device-resident via GDAKI. Reports **MSCCL++'s
  multicast variant hanging on GB200**, excluded from comparison.
- **NCCLZ** (SC 2026) — **MEASURED** on **Polaris (ANL): 4× A100 per node, AMD
  EPYC Milan, NVLink intra-node, HPE Slingshot inter-node, 2–32 nodes**,
  against **unmodified NCCL 2.28.3**: **up to 9.65× over NCCL, up to 3.34× over
  a prior compression-assisted collective** `[paper]`. **Minimal benefit for
  latency-dominated messages ≤64 KiB.** Deliberately host-enqueued
  (`ncclAllReduce` preserved).

## 5. Historical lineage

Not a progression (§7, T1). What the citations *do* support
(`../corpus/_LEDGER_multi_gpu_communication.md` §E, and
`../synthesis/GPU_COMMUNICATION_STACK.md`):

- **A scale-up / scale-out split.** Inside an NVLink domain, device-resident
  control is routine and the remaining cost is **microseconds of
  synchronisation**. Across a scale-out fabric, host or hardware mediation
  persists and the remaining costs are **bandwidth and algorithm selection**.
- **A real convergence on in-fabric reduction, orthogonal to who initiates** —
  MSCCL++ SwitchChannel, *Every Microsecond Matters*' NVLS
  (`multimem.ld_reduce`), and three ISCA/HPCA 2026 in-switch-computing papers.
  **The branch with the strongest cross-venue agreement in this topic.**
- **A multi-rail line at one lab**: OSU NOWLAB's multi-rail-aware MPI work
  (ISC 2024 → IPDPS 2025 → IPDPS 2026) with NIMBLE as its
  execution-time-planning branch `[census]`.
- **A compression-in-collectives line** — gZCCL (ICS 2024), hZCCL (SC 2024),
  ghZCCL (ICS 2025), COCCL (PPoPP 2026) → NCCLZ (SC 2026) — which
  `data_movement_compression.md` shows has **no citation traffic with the
  standalone-compressor line in either direction**.

## 6. Implementation families

Eight of nine are `REAL_SILICON`; **T3 is the only simulated paper**, and it is
also the only one proposing hardware that does not exist in production.
`[code]` was inspected for MSCCL++. Control placement was **never inferred from
an abstract** — per `../../../governance/ANTI_HALLUCINATION_RULES.md`,
GPU-initiated vs host-initiated distinctions require the paper or the code, and
every `ABSTRACT_ONLY` / `CLOSED_ACCESS` row carries `UNKNOWN` for control
placement without exception.

## 7. Important disagreements / tensions

**T1 — the progression narrative is not supported, on four kinds of
counter-evidence, all `[paper]`**
(`../corpus/_LEDGER_multi_gpu_communication.md` §E):
1. **The stages coexist in the same venue-years, and the newest papers are not
   the most device-resident.** IPDPS 2026 contains both NIMBLE (device-resident
   data path asserted) and PCCL (fully host-initiated MPI + vendor libraries at
   2,048 GPUs). SC 2026 contains both *Every Microsecond Matters* (device-
   resident via GDAKI) and NCCLZ (host-enqueued, deliberately). If this were a
   progression the 2026 host-driven papers would be rearguard work — and PCCL
   reports **up to 168× over RCCL for reduce-scatter at 2,048 MI250X GCDs**.
2. **The symmetric-memory "stage" is actively contested.** MSCCL++
   (ASPLOS 2026): "We could not find any implementation where NVSHMEM
   outperforms NCCL (or MSCCL++) for collective communication." T3
   (ASPLOS 2024): NVSHMEM "requires explicit synchronization and doesn't
   automatically orchestrate collective progress." *Every Microsecond Matters*
   (SC 2026) does the opposite, adopting PGAS/symmetric memory as a core design
   principle — and then reports MSCCL++'s multicast hanging on GB200. **Two
   papers one venue-cycle apart reach opposite conclusions about the same
   mechanism.**
3. **Control placement is a property of the fabric, not of the calendar.**
   GICC is device-resident on mlx5 and device-*triggered* on CXI — **a single
   paper occupying two "stages" at once, depending on which link is crossed.**
   MSCCL++ reports the same constraint from the other side.
4. **The most recent large-scale collectives paper does not engage the
   device-initiated line at all.** PCCL has **no comparison with MSCCL, no
   comparison with GPU-initiated/NVSHMEM approaches, and no discussion of
   kernel-resident collective implementations**. PICO, the field's most capable
   collective-benchmarking framework here, supports **only MPI, NCCL and
   RCCL** — no SHMEM/NVSHMEM backend, so it **cannot measure a device-initiated
   path at all**.

**T2 — the scale-up gap widens with scale, which cuts against the scale-up
story's own optimism.** *Every Microsecond Matters* is within **7% of SoL at 2
GPUs** and **~70% above SoL at 64** `[paper]`. The technique that gets closest
at 2 GPUs (LL flag-in-data) **halves bandwidth**, and **ring AllReduce still
needs explicit barriers** because of inter-step dependencies — so the barrier
deletion does not generalise to ring.

**T3 — vendor defaults are not the best choice, corroborated three ways.**
The SC 2024 interconnect study (MPI beats NCCL by up to an order of magnitude
on small inter-node transfers; RCCL below half of GPU-aware MPI on a specific
MI250X GCD pair), PICO (defaults typically **30–40% off optimal, worst case
1/5 of optimal**, on Leonardo/LUMI/MareNostrum 5), and PCCL (NCCL/RCCL offer
only ring for all-gather/reduce-scatter, giving latency linear in endpoint
count). Three independent measurements on different machines.

**T4 — same venue, same year, two papers on the achieved-vs-available
bandwidth gap, and the analyses record no citation link in either direction.**
NIMBLE re-plans *paths* at execution time on NVLink-4 + multi-rail NDR400;
PCCL re-plans *algorithms* hierarchically on Slingshot-11. Both IPDPS 2026.
`[inference]` on the non-citation: what is **verified** is that PCCL's related
work engages neither MSCCL nor the device-initiated line `[paper]`.

**T5 — the storage path is easier than the network path.** MSCCL++ records that
**GPU-initiated RDMA is not supported** and inter-node transfers need a host
proxy, while `../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md`
achieves fully device-resident NVMe control. The asymmetry is mechanical
(MMIO doorbells vs a driver-mediated work-queue protocol), not a maturity gap.

## 8. Current limitations

**Every row in this cluster carries `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`** —
`../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and is known to hold an
~80-paper AI/HPC corpus with GPU communication/collectives coverage. **No claim
of non-duplication is made for any paper in this topic**
(`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).

**Bounded by full-text access**: `dl.acm.org` → 403 and
`ieeexplore.ieee.org` → 418 from this environment, so several papers the census
marks as having an open publisher PDF are nonetheless `CLOSED_ACCESS` *as
determined here* — an access-path limitation, not a statement about licence
(`../synthesis/GPU_PENDING_FULLTEXT.md`). **Six rows are `UNRESOLVED`**, all
cases where the title alone does not decide GPU residency and the census itself
flags relevance as inferred; two of them (a direct-connect schedule and a
non-uniform all-to-all) are **plausibly not GPU papers at all**, since an
all-to-all schedule for a direct-connect topology is a graph-theoretic result
that holds for any endpoint type.

**Bounded by the tooling, not by access:** T1.4 — PICO cannot measure a
device-initiated path, so the corpus has **no head-to-head benchmark across the
initiation axis**. That is a gap in the instruments, and no further retrieval
fixes it.

**One number is `[census]`/`[official-web]`, not `[paper]`**: PICO's "up to 44%
training-time reduction". Do not promote it.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. What would a benchmark that spans the initiation axis measure? PICO is the
   natural host and lacks the backend (T1.4).
2. Does the SoL gap at 64 GPUs (T2) close with in-fabric reduction, or is it
   a different bottleneck? *Every Microsecond Matters* says multicast is "the
   best option there" but does not decompose the remaining ~70%.
3. T3 is stable across three systems and two vendors. Is the defaults problem a
   library-engineering problem or an information problem — i.e. would the
   libraries pick better if they could measure what PICO measures at runtime?

## 10. Deeper lookup paths

`../corpus/_LEDGER_multi_gpu_communication.md` — the control-placement
vocabulary, §C summary counts (derived by tallying, not estimated), §D the
control-placement roll-up, §E the four-part answer to the progression question
and its recommended two-axis replacement → `../synthesis/GPU_COMMUNICATION_STACK.md`
→ the nine analyses above → the pinned artifacts in each §12.8.
Cross-topic: `data_movement_compression.md` (the non-citing standalone
compressor line), `compiler_programming.md` (FlashFuser's all-reduce *inside*
one GPU's thread-block cluster — the same vocabulary at a third scale),
`power_energy.md` (thermal coupling across a multi-GPU node).

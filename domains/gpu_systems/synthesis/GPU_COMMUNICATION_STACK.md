# GPU_COMMUNICATION_STACK — the two-axis map that replaces the linear progression

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
source: `_LEDGER_multi_gpu_communication.md` (40 assigned papers, 9 deep analyses)
plus `_LEDGER_data_movement_compression.md` §D.6 for the storage path.

---

## 1. Why this document is a map and not a timeline

The multi-GPU cluster was asked whether the field had traversed
**GPU-aware MPI → device-initiated communication → symmetric memory →
GPU-resident collective control**. Its answer, from the papers' own related work:
**NOT SUPPORTED as a progression.** It is a real taxonomy of mechanisms; it is not
a sequence the field has walked.

The cluster's recommended replacement, adopted here as this document's spine:

> Replace the linear progression with a **two-axis map** — *who initiates*
> (host-driven / device-triggered / device-resident) x *which fabric is crossed*
> (intra-node NVLink or xGMI / PCIe / inter-node RDMA fabric) — and record that
> **the fabric axis, not the year, predicts the initiation axis.**

### 1.1 Control-placement vocabulary (used exactly as the ledger defines it)

| Term | Meaning |
|---|---|
| `host-driven` | CPU enqueues the operation; stream-ordered; host or host proxy thread posts to the NIC |
| `device-triggered` | Hardware (tracker, NIC counter + pre-staged work) initiates; neither host nor a kernel issues the operation |
| `device-resident` | A GPU kernel itself issues the put/get or posts the work-queue element |
| `UNKNOWN` | **Not established from the paper or the code — never guessed** |

**The `UNKNOWN` rule is load-bearing.** Per
`governance/ANTI_HALLUCINATION_RULES.md`, GPU-initiated vs host-initiated
distinctions are on the deep-source list and may not be answered from a
compressed context. **Control placement was never inferred from an abstract.**
Of 40 assigned papers, control placement was **established for 10** and is
`UNKNOWN` for **30**. That ratio is the honest state of the evidence and it is
reproduced rather than smoothed.

---

## 2. The map

Rows are initiation; columns are the fabric crossed. A paper appears in more than
one cell when it occupies more than one cell — which several do, and that is the
point.

### 2.1 Papers with a deep analysis in the corpus

| | **Intra-node peer-mapped (NVLink / xGMI)** | **Intra-node switch (NVSwitch / NVLink SHARP)** | **PCIe** | **Inter-node RDMA (IB / Slingshot-CXI)** |
|---|---|---|---|---|
| **`device-resident`** | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) **MemoryChannel** — thread-level in-kernel put/signal/wait over peer-mapped stores, 16-byte atomic write consistency `[paper]` `[code]` | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) **SwitchChannel** — `multimem.red.release.sys.add.u64` inline PTX, read in the artifact at `include/mscclpp/semaphore_device.hpp:174` `[code]`; [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) NVLS `multimem.ld_reduce` | — | [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) via **GDAKI** over CUDA VMM symmetric memory `[paper]`; [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) **on mlx5 InfiniBand only** — kernels build WQEs and ring the UAR doorbell `[paper]` |
| **`device-triggered`** | [`GPU-ASPLOS24-21`](../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md) **T3** — a programmable hardware tracker on the producer's stores fires pre-programmed DMA commands; no host, no kernel sync in the overlapped phase. *Fabric modelled as a ring; NVLink generation, switch topology and per-link bandwidth are **`UNKNOWN`** in the read text* | — | — | [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) **on OFI/CXI (Slingshot-11)** — host pre-stages bounded ops in a 256-entry Deferred Work Queue against a 2047-counter budget; the GPU only rings a doorbell. The paper's own term: **"GPU-triggered rather than GPU-initiated"** `[paper]` |
| **`host-driven`** | [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md) (all measured paths; NVSHMEM and device-side put/get explicitly **not** evaluated); [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md) PCCL — GPU-resident *reduction arithmetic*, host-driven *orchestration* | [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md) PICO — **and it cannot observe anything else**: backends are MPI/NCCL/RCCL only | [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md) measures PCIe Gen4 as a parallel intra-node path on Leonardo | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) **PortChannel / all inter-node RDMA** — `port_channel_device.hpp:75` pushes a FIFO trigger, `src/core/ib.cc:399` calls `ibv_post_send` `[code]`; [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md) NCCLZ initiation (device-resident *codec*, host-driven *initiation*); [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md) PCCL |
| **`device-resident` (paper-asserted, code-unverified)** | [`GPU-IPDPS26-01`](../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md) NIMBLE — "CUDA-aware GPU kernel-based RDMA pipelining"; GPU kernels orchestrate multi-hop forwarding "without host intervention", explicitly contrasted with "host-driven MPI enqueue". **No artifact, no published kernel structure, no device-side API named** (no NVSHMEM/IBGDA/GDAKI). The planner itself is host-side | — | — | [`GPU-IPDPS26-01`](../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md) — same caveat; rail-matched GPU→NIC bindings over four NDR400 rails, H100-SXM4 / NVLink 4, 2–8 nodes |

**Two papers occupy two initiation rows at once, and that is the cluster's
decisive observation.** MSCCL++ is device-resident intra-node and host-driven
inter-node, in one codebase. GICC is device-resident on mlx5 InfiniBand and
device-triggered on CXI, in one runtime. **A "stage" that a single paper occupies
twice is not a stage.**

### 2.2 Papers established only at code or artifact depth (no deep analysis permitted)

| Paper | Placement | Evidence |
|---|---|---|
| **aCG** (SC 2025, CPU- and GPU-initiated CG on large GPU clusters) | **both, and separated in the code.** `device-resident`: `nvshmemx_double_put_signal_nbi_block` called from inside CG kernels at `acg/cg-kernels-cuda.cu:728,743,844,859,1421,1436,1492,1507,1595,1610`, `nvshmem_quiet()` at `:759,874,1452,1522,1625`, plus in-kernel `nvshmemx_double_sum_reduce_block/_warp`. `host-driven`: `nvshmemx_double_put_signal_on_stream` + `nvshmemx_sync_all_on_stream` + `nvshmemx_signal_wait_until_on_stream` at `acg/halo.cu:219,227,234`, and `nvshmemx_double_sum_reduce_on_stream` at `acg/comm-nvshmem.cu:282` | `[code]` @ `f68ccb4ebd97122927c3812f8d5c88f633b3a877`; `[README]` states the distinction verbatim |
| **TCCL** (ASPLOS 2024, PCIe GPU clusters) | **`UNKNOWN` for the paper's framing** (no paper text obtained). The code shows NCCL transport selection, i.e. host-configured: `TCCL_TRANSPORT_TYPE_{P2P,SHM,NET}` (`src/include/tccl.h:20-22`) chosen at `src/tccl/tccl.cc:265-405`. Its transfer taxonomy at `tccl.h:71-83` — `GPU_{READ,WRITE}_{CPUMEM,GPUMEM}_{KERNEL,MEMCPY}` (0–7) plus `{GPU,CPU}_{GPU,CPU}_INTER` (8–11) — makes the kernel-vs-DMA-memcpy axis explicit, **but that is a copy-engine choice, not device-initiated control** | `[code]` @ `351d064856e322ec6e4546808e7d1e433d24f941`; `[official-web]` |
| **GPUs All Grown-Up** (ISCA 2025, fully device-driven SpMV via GPU Work Graphs) | **`UNKNOWN`.** The project page describes device-driven *work scheduling*, not inter-GPU communication. On the evidence read this is a single-GPU device-resident *control* paper, not a multi-GPU communication paper | `[official-web]` only |

aCG is **the strongest code-level evidence in the whole cluster for the
host-vs-device initiation distinction** — the same solver carries both paths in
one tree — and it is exactly the paper for which the full-paper gate fails
(`PUBLIC_ARTIFACT_ONLY`; ACM DOI → 403, no public preprint found).

### 2.3 Everything else: `UNKNOWN`, and why that is the correct entry

**All 30 remaining assigned papers carry `UNKNOWN` for control placement**,
because none was read at full-paper or code depth. They are named here so the map
is complete, grouped by sub-branch. **No row in this subsection may be used to
assert a lineage edge.**

- **In-fabric / in-switch reduction** (strongest cross-venue agreement in the
  cluster): *Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs*
  (ISCA 2026), *Towards Compute-Aware In-Switch Computing for LLMs
  Tensor-Parallelism on Multi-GPU Systems* (HPCA 2026), *RoCC: Harnessing Raster
  Operations Pipeline for Efficient Tensor Collective Communication* (ISCA 2026),
  *Network-Offloaded Bandwidth-Optimal Broadcast and Allgather for Distributed AI*
  (SC 2024).
- **Compression in collectives**: gZCCL (ICS 2024), hZCCL (SC 2024), ghZCCL
  (ICS 2025), COCCL (PPoPP 2026), *Casting Compression for GPU-Aware MPI
  Collectives* (IPDPS 2026), *Accelerating MPI AllReduce … GPU-Based Compression
  Schemes* (ISC 2024), *Compression-Aware Gradient Splitting* (HPCA 2026,
  `UNRESOLVED`).
- **Multi-rail / hierarchical MPI**: *Multi-Rail-Aware Hierarchical MPI
  Reduce-Scatter and Allgather* (IPDPS 2026, `UNRESOLVED`), *Unified Designs of
  Multi-rail-aware MPI Allreduce and Alltoall Across Diverse GPU and Interconnect
  Systems* (IPDPS 2025), *ROCm-Aware Leader-based Designs for MPI Neighbourhood
  Collectives* (ISC 2024).
- **Symmetric / shared GPU memory**: *Harnessing Inter-GPU Shared Memory for
  Seamless MoE Communication-Computation Fusion* (PPoPP 2025) — the closest
  verdict-only paper to this cluster's symmetric-memory axis, and establishing its
  placement is flagged the highest priority; *CXL-CCL: Inter-Node Collective
  GPU-Communication Using a CXL Shared Memory Pool* (ICS 2026) — the cluster's
  only non-NVLink/non-IB shared-memory substrate; *Aqua: Network-Accelerated
  Memory Offloading for LLMs in Scale-Up GPU Domains* (ASPLOS 2025) — the scale-up
  fabric repurposed as a memory-expansion path rather than a collective path.
- **Compute/collective fusion**: *Optimizing Distributed ML Communication with
  Fused Computation-Collective Operations* (SC 2024), *MoE-Hub* (ISCA 2026),
  *Chimera: Communication Fusion for Hybrid Parallelism* (ISCA 2025,
  `UNRESOLVED`).
- **Topology and fabric**: *NetCrafter: Tailoring Network Traffic for Non-Uniform
  Bandwidth Multi-GPU Systems* (ISCA 2025), *Rail Optimized PCIe Topologies for
  LLMs* (ISC 2025), HiCCL (IPDPS 2025, `UNRESOLVED`), CommBench (ICS 2024),
  *Communication-Avoiding SpGEMM via Trident Partitioning on Hierarchical GPU
  Interconnect* (ICS 2026).
- **Diagnosis**: *CCL-D* (PPoPP 2026, `RELATED_GPU`) — relevant precisely because
  [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md)
  and [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md)
  both independently report NCCL/RCCL hangs at scale.
- **Possibly not GPU papers at all** (`UNRESOLVED`; the census itself flags the
  relevance as inferred): *Efficient all-to-all Collective Communication Schedules
  for Direct-connect Topologies* (HPDC 2024), *Parameterized Algorithms for
  Non-uniform All-to-all* (HPDC 2025). An all-to-all schedule for a direct-connect
  topology is a graph-theoretic result that holds for any endpoint type.

---

## 3. The fabric axis predicts the initiation axis

This is the substantive claim the map exists to carry, and it is reached
**independently from two directions by two papers**.

**From the runtime side** — [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md):
the *same runtime* is `device-resident` on mlx5 InfiniBand (kernels construct
work-queue elements and ring the User Access Region doorbell) and only
`device-triggered` on HPE Slingshot's CXI provider (the host pre-stages bounded
operations in a 256-entry Deferred Work Queue against a 2047-counter budget; the
GPU merely rings a doorbell; a host monitor thread drives libfabric progress at
~1 µs/op). GICC coins **"GPU-triggered rather than GPU-initiated"** for exactly
this `[paper]`. Its related-work table classifies the field *by fabric* `[paper]`:
NVSHMEM — GPU-initiated on InfiniBand, host-mediated on Slingshot/OFI, with no
GPU-driven barriers or collectives there; rocSHMEM — the same limitation; NCCL —
GPU-initiated on IB, host-driven on OFI, and focused on collective *algorithms*
rather than kernel-level synchronization; GPU-aware MPI — entirely
host-orchestrated; GASNet-EX — CPU-driven RMA. Evaluated on Tioga (MI250X,
Slingshot-11, ≤64 GPUs) and Maple (GH200, IB HDR, 2 nodes): the **runtime** is not
vendor-locked; the **fabric** is what changes the mechanism.

**From the library side** — [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md):
"Current hardware interconnects require a CPU thread to initiate the data
transfer" `[paper]`, and GPU-initiated RDMA is **not supported** — confirmed at
code (`port_channel_device.hpp:75` pushes a FIFO trigger; `src/core/ib.cc:399`
calls `ibv_post_send`) — while the same library is fully device-resident
intra-node.

**Inside an NVLink domain, device-resident control is routine; across a scale-out
fabric it is fabric-conditional.** That sentence, not a year, is the organising
fact.

**The corollary the corpus supports narrowly**: a genuine split between
**scale-up** and **scale-out** regimes with *different residual cost structures*.
Inside an NVLink domain the remaining costs are microseconds of synchronization —
[`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md)
derives `L_SoL = 2·L_L2_RTT + L_remote_store` = **1.404 µs on two GB200**, measures
barriers at >1 µs (~40% of a 5 µs small-message AllReduce), and reaches within 7%
of SoL at 2 GPUs but ~70% above it at 64. Across a scale-out fabric the remaining
costs are bandwidth and algorithm selection.

---

## 4. In-fabric reduction — a real convergence, orthogonal to who initiates

This branch has the **strongest cross-venue agreement in the cluster**, and it
must not be confused with device initiation. A switch that reduces is not a GPU
that initiates.

| Mechanism | Where read | File |
|---|---|---|
| `multimem.red.release.sys.add.u64` (MSCCL++ SwitchChannel) | inline PTX in the artifact at `include/mscclpp/semaphore_device.hpp:174` `[code]` | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) |
| `multimem.ld_reduce` (NVLS multicast) | `[paper]` | [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) |
| **LL128-atomic** — requires NVLink to guarantee *cache-line-granular atomic addition*; the paper restricts the algorithm to FP32/FP16 (where vectorized atomics exist) and to addition only | `[paper]` | [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) |
| Three in-switch-computing papers (ISCA 2026 x2, HPCA 2026) | `[census]` only — placement `UNKNOWN` | — (watchlist) |
| Network-offloaded broadcast/allgather (SC 2024) | `[census]` only | — (watchlist) |

Hardware precondition, stated: SwitchChannel requires **NVSwitch with NVLink
SHARP and the `multimem` instruction family — H100-class and later**; it is
unavailable on the A100 and MI300X nodes MSCCL++ evaluates `[paper]` `[code]`.

**One sub-branch sits on a category boundary**: *RoCC* (ISCA 2026) repurposes the
**Raster Operations Pipeline** — a fixed-function *graphics* unit — for tensor
collectives. It is simultaneously a communication paper and a member of the
fixed-function-repurposing category
([`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §5). Placement `UNKNOWN`;
abstract-only.

---

## 5. Symmetric memory is contested, not passed through

**Two papers one venue-cycle apart reach opposite conclusions about the same
mechanism.** This is the clearest single refutation of the progression narrative
and it is reproduced at full strength.

- **Against.** [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md)
  (ASPLOS 2026): *"We could not find any implementation where NVSHMEM outperforms
  NCCL (or MSCCL++) for collective communication."* `[paper]` An explicit
  rejection of the symmetric-memory route, not an adoption of it.
- **Against, earlier and for a different reason.**
  [`GPU-ASPLOS24-21`](../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md)
  (ASPLOS 2024): NVSHMEM *"requires explicit synchronization and doesn't
  automatically orchestrate collective progress"* `[paper]`. T3 treats symmetric
  memory as **insufficient**, not as a step to build on.
- **For.** [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md)
  (SC 2026) adopts PGAS/symmetric memory as a **core design principle**, cites the
  SHMEM lineage, and builds on CUDA VMM symmetric memory plus GDAKI — **and then
  reports that MSCCL++'s multicast variant hung on GB200 and had to be excluded
  from the comparison** `[paper]`. An adversarial data point in the other
  direction.

`NOT_ESTABLISHED`: nothing in the corpus resolves which position is right. The
disagreement is live as of SC 2026.

---

## 6. "Vendor defaults are wrong" — independently corroborated three times

This is the one substantive finding in the area that **three separate papers reach
on different systems**, and it holds regardless of where control sits.

| Paper | Systems | Finding, with its qualifiers |
|---|---|---|
| [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md) | Alps (H100 / Slingshot-11), Leonardo (A100 / IB-HDR), LUMI-G (MI250X / Slingshot-11) | **MPI beats NCCL by up to an order of magnitude on small inter-node transfers**; **RCCL falls below half of GPU-aware MPI on a specific MI250X GCD pair**; the MPI-vs-NCCL/RCCL ordering **flips by operation class and by system**, so it does not transfer |
| [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md) | Leonardo, LUMI, MareNostrum 5 | **Defaults typically 30–40% off optimal, worst case 1/5 of optimal**; a transport rail parameter (`UCX_MAX_RNDV_RAILS`, default 2, tested to 4) worth **>2x**; cost-model-equivalent algorithms differing on real hardware; **GPU-buffer staging cost isolated at ~50% of allreduce runtime at ≥1 MiB on Leonardo** |
| [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md) | Frontier (2,048 MI250X GCDs), Perlmutter (2,048 A100s), both Slingshot-11 | **NCCL/RCCL offer only ring for all-gather and reduce-scatter**, giving latency linear in endpoint count; PCCL reports up to **168x over RCCL for reduce-scatter at 2,048 MI250X GCDs on Frontier** |

Independent corroboration of NCCL/RCCL **unreliability** at scale also exists:
[`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md)
found NCCL/RCCL alltoall benchmarks stalling at 512+ GPUs; PCCL independently
reports RCCL unreliability at scale `[paper, both]`.

**Verified citation edges in this sub-thread:**

- [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md)
  → [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md):
  `[paper]`, **`EXTERNALLY_VERIFIED`**. The corpus recorded this `UNKNOWN` (the
  read pass reported it both as an omission and as bibliography entry [12]).
  Settled against the arXiv HTML of `2508.16809v1`: PICO carries it as reference
  **[12]** — De Sensi, Pichetti, Vella, De Matteis, Ren, Fusco, Turisini,
  Cesarini, Lust, Trivedi, Roweth, Spiga, Di Girolamo, Hoefler, SC'24. Shared
  author Daniele De Sensi. **The `UNKNOWN` in the corpus file should be updated.**
- [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md)
  → **CommBench** (ICS 2024): `[paper]`. PICO credits it as "a significant step
  toward extensibility" with a library-agnostic API, then faults its minimal
  metadata logging, its steep learning curve, and its assumption of
  one-process-per-GPU execution. The cluster's clearest benchmark-lineage
  relation. PICO also critiques **nccl-tests** as NCCL-locked — relevant because
  NCCLZ and PCCL both report against nccl-tests-style baselines.
- [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md)
  → **HiCCL** (IPDPS 2025): `[paper]`. PCCL states HiCCL "achieves gains at
  smaller node counts but falls below vendor libraries at larger node counts".
  Third-party evidence that HiCCL is a GPU collective library, but **not** a
  substitute for reading it — HiCCL remains `UNRESOLVED`.
- [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md)
  → **gZCCL / ghZCCL / COCCL**: `[paper]`. NCCLZ identifies gZCCL's specific
  weakness (**error propagation in reduction operations**), ghZCCL's homomorphic
  compression as avoiding that but "lack[ing] efficiency for all workloads", and
  COCCL as integrating lightweight quantization into NCCL APIs but omitting
  entropy coding and being unable to switch between scientific and AI
  compressors. **hZCCL (SC 2024) was not confirmed cited** — `UNKNOWN`, not
  `NOT_CITED`.
- [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md)
  is the **baseline supplier** for four later papers that each argue against
  NCCL/RCCL defaults — MSCCL++, *Every Microsecond Matters*, NIMBLE and PCCL —
  because it quantifies the gap first. Only the PICO edge is a verified citation;
  the rest is `[inference]` from the four papers' shared premise.

---

## 7. The verified negatives

Reproduced in full because they are the area's principal results.

1. **The linear progression is NOT SUPPORTED.** The stages coexist in the same
   venue-years and the newest papers are not the most device-resident. IPDPS 2026
   holds both NIMBLE (device-resident asserted) and PCCL (fully host-initiated at
   2,048 GPUs). SC 2026 holds both *Every Microsecond Matters* (device-resident
   via GDAKI) and NCCLZ (host-enqueued `ncclAllReduce`, **preserved
   deliberately** — NCCLZ "follows NCCL's native host-side proxy model" and does
   not replace `ncclAllReduce`). If this were a progression, the 2026 host-driven
   papers would be rearguard work; they are not.
2. **PCCL's related work contains no MSCCL, no GPU-initiated/NVSHMEM comparison,
   and no discussion of kernel-resident collective implementations or device-side
   algorithm selection** `[paper]`. `NOT_CITED`. A progression narrative requires
   later work to cite and build on the earlier stage; the 2026 host-driven work
   largely does not engage it.
3. **PICO cannot observe a device-initiated path at all** — backends are MPI,
   NCCL and RCCL only; there is no SHMEM/NVSHMEM backend `[paper]`. The field's
   most capable collective-benchmarking framework is structurally blind to the
   stage the progression claims the field has reached.
4. **Control placement is fabric-conditional, not calendar-conditional** (§3).
   A single paper occupies two "stages" at once depending on which link is
   crossed.
5. **T3 positions *against* symmetric memory rather than building on it**
   `[paper]`. T3 and MSCCL++ share an identical diagnosis — NCCL cannot fuse with
   compute — and reach **opposite remedies**: T3 adds hardware so the *existing*
   software need not change; MSCCL++ changes the software so no hardware is
   needed. **Both cannot be "the" answer.**
6. **T3's fabric is `UNKNOWN`** — NVLink generation, switch topology and per-link
   bandwidth are not specified in the read text, and T3 is simulated only
   (extended Accel-Sim, 6% error) on non-production compute-enhanced memory. This
   is a genuine gap relative to every measured paper in the cluster, and it means
   the cluster's only pure device-triggered design **cannot be placed on the
   fabric axis at all**.

---

## 8. GPU-initiated **storage** I/O is further along than GPU-initiated networking

A cross-cluster finding, from `_LEDGER_data_movement_compression.md` §D.6 read
against the communication ledger.

| Path | Strongest device-resident result | What the CPU still does |
|---|---|---|
| **Storage (NVMe)** | [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md) **AGILE** — a GPU thread writes an NVMe Submission Queue Entry and rings the doorbell; a persistent GPU daemon kernel reaps the Completion Queue | **Nothing.** The CPU is in neither the control path nor the data path |
| **Network (RDMA)** | [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) via GDAKI inside an NVLink domain; [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) on mlx5 only | On CXI the host pre-stages a Deferred Work Queue and a monitor thread drives libfabric progress at ~1 µs/op. In MSCCL++ a CPU thread is required for **all** inter-node transfers |

**Why — the mechanism, not a metaphor:** **NVMe doorbells are plain MMIO registers
mappable into the GPU's address space, whereas RDMA verbs require a
driver-mediated work-queue protocol.** `[inference]`, but strongly supported by
the two papers side by side: MSCCL++ states the hardware requires a CPU thread
for RDMA, and AGILE achieves on the storage path exactly what MSCCL++ says cannot
be done on the network path.

The mlx5 case is the exception that confirms the rule. GICC shows that where the
NIC *does* expose its submission doorbell to a kernel (the mlx5 User Access
Region), a kernel *can* post directly; where it does not (CXI), it cannot.
**In both the storage and the network case the determining factor is whether the
device's submission doorbell is mappable into GPU address space.**

**Caveats that must travel with AGILE's result**: a single SKU — **RTX 5000 Ada, a
*workstation* card**, with no A100/H100/MI300 result, and the design leans on BAR1
capacity; **BAR1 must be enlarged beyond the typical 128 MB via a vendor tool**
`[README]`; **IOMMU must be disabled** `[README]`, a security-relevant
configuration unacceptable in many production and multi-tenant settings and *not*
listed as a limitation in the read text; and the tree ships separate driver builds
for Linux 6.8.0 and 6.17.0 `[code]`, evidence that the NVMe/GPU driver interface
is not stable across kernels. NVMe itself (SQ/CQ, phase bit, CID) is a
vendor-neutral standard, so the protocol logic would port; the GPU-side mechanisms
(warp ballot, BAR1 peer-to-peer, persistent daemon kernel) are SIMT-specific but
not NVIDIA-specific in principle `[inference]`.

**The other two storage variants, for completeness**: *Phoenix* (SC 2025,
artifact-only) refactors the host-driven GPUDirect Storage stack to remove the
bounce buffer rather than bypassing it; *OS2G* (ASPLOS 2025, unread) routes
through a DPU. AGILE bypasses GDS entirely and vendors a **BaM NVMe driver**
in-tree (`driver/bam_nvme_driver-linux-6.8.0/`) `[code]`, i.e. its baseline is
built from source — unusually good comparative hygiene.

---

## 9. Adjacent device-resident control, for orientation

Not communication papers, but the same architectural move — removing the host from
a control path it historically owned — applied to other resources. Reading them
together is the strongest cross-cluster lineage claim available, and it is
`[inference]` from three separately-read papers, **not** a citation chain.

| Resource | Paper | Mechanism |
|---|---|---|
| Communication | [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) | kernel posts WQEs / rings doorbells |
| Memory | [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) | warps run the fault handler and update device-side page tables |
| Scheduling | [`GPU-ICS25-162`](../corpus/GPU-ICS25-162--mustard-device-side-execution-multi-gpu-task-graphs.md) | device-side CUDA graph launch (CUDA 12-era, 120-graph cap) + NVSHMEM multi-GPU atomics; a persistent kernel for the *scheduler only*, explicitly rejecting the megakernel style |
| Storage | [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md) | GPU writes NVMe SQE, GPU daemon reaps CQ |

One further adjacency: [`GPU-HPCA26-144`](../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md)
(FlashFuser) performs an **all-reduce inside a single GPU's thread-block cluster**
over Hopper distributed shared memory, with a TMA-based `dsm_reduce_scatter`. The
same algorithmic vocabulary now appears at two scales — inside one GPU and across
a fabric. Worth noting; **not** a citation link to the collective line.

---

## 10. What this document cannot tell you

- **Control placement for 30 of 40 assigned papers.** `UNKNOWN`, by rule. The
  highest-value single resolution would be *Harnessing Inter-GPU Shared Memory for
  Seamless MoE Communication-Computation Fusion* (PPoPP 2025), which sits squarely
  on the symmetric-memory axis.
- **Whether symmetric memory is the right route.** `NOT_ESTABLISHED` (§5).
- **T3's fabric.** `UNKNOWN` (§7.6).
- **Whether the three in-switch-computing papers (ISCA 2026 x2, HPCA 2026) form a
  citing sub-branch or three independent arrivals.** No full text was reached for
  any of them. `NOT_ESTABLISHED`.
- **Whether NIMBLE's device-residency claim survives code inspection.** The paper
  asserts it; no artifact exists and no device-side API is named. `UNKNOWN`.
- **Duplication against an external corpus.** `domains/ai_hpc_systems/` is
  `EXTERNAL_IMPORT_PENDING`: an ~80-paper AI/HPC corpus with GPU
  communication/collectives coverage is known to exist outside this repository and
  is **not imported**. Many papers here plausibly belong to it. **No claim of
  non-duplication is made for any row.**

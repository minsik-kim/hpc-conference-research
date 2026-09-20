# GPU runtime, task graphs, scheduling, GPU sharing, MIG/MPS and virtualisation (taxonomy J/K)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD on sharing, THIN on task graphs.** Six deep analyses
(the cluster's `161–166` ID band) — **five on sharing/partitioning (`K`) and
exactly one on task graphs and runtime (`J`)**. Verdict ledger:
`../corpus/_LEDGER_runtime_sharing.md`.

## 1. Problem landscape

`../corpus/_LEDGER_runtime_sharing.md` calls this "the cluster most prone to
false positives, because scheduling *GPU jobs* is usually not *GPU research*",
and applies a rule without exception: a queueing, bin-packing, forecasting or
fairness policy over resources that happen to be accelerators is
`RELATED_GPU`; a mechanism that manipulates **SM / TPC / CTA / MIG / MPS /
channel / driver** structure, or depends on a GPU-specific property
(non-preemptive kernels, the kernel-launch boundary, wave quantisation, a fixed
partition lattice, a closed driver interface), is `CORE_GPU`.

Under that rule the topic is about one thing: **where the partition boundary is
drawn, and what leaks across it.** Every paper here draws it somewhere
different, and the corpus's central finding is that **no mechanism provides
complete isolation**.

## 2. Key concepts

MIG as a fixed lattice of legal profiles and placement slots, reconfigurable
only when idle; MPS as thread-slice partitioning with no VRAM-bandwidth
isolation; temporal multiplexing / time slicing; `libsmctrl` — a
reverse-engineered co-option of CUDA driver debug logic — as the software
school's shared dependency; TPC/SM masking; memory-channel colouring;
VFIO/mdev vGPU and kernel-space interception; non-preemptive kernels and the
kernel-launch boundary as the only schedulable instant; wave quantisation;
prefill/decode phase separation; device-side CUDA graph launch and its
120-graph cap; device-side work stealing from a persistent scheduler.

## 3. Main mechanism families — five schools, forked by hardware availability

**Hardware lattice (where MIG exists).**
`../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md`
accepts MIG's lattice and solves the packing problem;
`../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md`
characterises what the lattice does and does not deliver on real HPC codes.

**Software spatial partitioning (where MIG does not exist).**
`../corpus/GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md`
(TPC masking + memory-channel colouring) and
`../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md`
(SM partitioning between LLM prefill and decode). **Both depend on
`libsmctrl`.**

**Below CUDA, in the kernel driver.**
`../corpus/GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md` gives
up spatial sharing entirely and time-slices arbitrarily sized vGPU slices for
untrusted, unmodifiable tenants.

**Device-side runtime (`J`).**
`../corpus/GPU-ICS25-162--mustard-device-side-execution-multi-gpu-task-graphs.md`
moves multi-GPU task-graph execution onto the devices themselves.

## 4. Representative papers

- **ParvaGPU** (SC 2024) — **MEASURED** (A100/H100). Makes **no kernel
  faster**; it reduces the **number of GPUs required to serve a fixed SLO
  set**, by three separable mechanisms: `argmax trp/size` rather than
  `argmax trp` as the objective (which is what stops the configurator
  defaulting to 7-GPC instances) `[code]`; residual absorption by a single
  differently-sized instance; and placement-aware best-fit plus a splitting
  pass `[paper]`. Honest cost: profiling is one-off per model per GPU over a
  **5 × 8 × 3 grid** `[README]`, and **MIG reconfiguration is destructive** —
  the artifact's reconfiguration script tears down all instances and kills MPS
  before re-creating them `[code, commit 5f3de1e…]`.
- **Taming GPU Underutilization with MIG** (ISC 2026) — **MEASURED** on
  **H100** (and MI300A/Grace Hopper context). Gains come from filling
  otherwise-idle SMs — **NekRS 12–25% occupancy, LAMMPS 40%, hotspot 60%** on
  the full GPU — and from reclaiming stranded memory (**20–60% reduction in
  memory underutilisation in seven cases**) `[paper]`. **The finding that
  distinguishes it: MIG does not partition power.** Because the power/clock
  domain is device-wide, a co-tenant that pushes the GPU into throttling slows
  **every** instance.
- **SGDRC** (PPoPP 2025) — **MEASURED** on **Tesla P40** and **RTX A2000** —
  precisely the parts MIG cannot serve. Against **Orion** on P40: "improves
  overall throughput by up to **1.47×** and BE job throughput by up to
  **2.36×**", at **99.0% average SLO attainment** `[paper]`. The decomposition
  matters more than the numbers: **the LS gain comes from the memory side, not
  the compute side** — the channel-isolation ablation alone moves LS p99 by
  **28.7% / 47.5% average on P40 / A2000**, so compute masking alone does not
  fix tail latency. Costs paid: an extra copy of every memory-bound BE tensor,
  **8 cycles per rewritten access**, 2.9% SPT overhead, and **a one-month
  per-GPU reverse-engineering campaign** `[paper]`.
- **Bullet** (ASPLOS 2026) — **MEASURED** (A100/H100). Headline
  throughput/goodput tables were **NOT_READ**, so **no speedup number is
  asserted**. What is established is the mechanism and the cost of what it
  replaces: chunked prefill degrades from **71% → 61% efficiency across
  successive chunks**, final chunk **1.9×** the first, **1.13× / 1.86%**-class
  latency inflation at 1k/2k chunk sizes `[paper]`. Adds **a hard dependency on
  an undocumented driver debug path with a CUDA ≤ 12.6 ceiling** `[code]`
  `[README]`, and leaves memory-system contention **unmanaged by design**.
- **gShare** (ASPLOS 2026) — **MEASURED** (A100). The saving is a **residency**
  saving, not a throughput saving: **43–63% GPU-usage reduction** from not
  keeping idle tenants resident, made possible by arbitrarily sized slices plus
  sub-millisecond hot-plug/snapshot re-admission `[paper]`. Kernel-space
  interception is why the overhead is small — proxy-based approaches cost
  **7–61% fluctuation and 10s–100s ms**. Honest scoping, to be carried: it
  "performs particularly well in environments with a large number of tenant
  functions and sparse request arrival patterns", and is **slower on any
  workload whose kernels neither fill the SMs nor fit in 20 ms** `[paper]`.
- **Mustard** (ICS 2025) — **MEASURED**, but **no performance number was read**
  and none is asserted here. It exists because a capability arrived, not
  because an algorithm was invented: the paper is explicit that device-side
  atomics did not span GPUs until "NVSHMEM bridged the gap by introducing
  multi-GPU atomics" `[paper]`. Requires **device-side CUDA graph launch (a
  CUDA 12-era feature) and its 120-graph cap**, which makes coarsening
  mandatory — the paper calls that "the most important and restraining"
  limitation `[paper]`.

## 5. Historical lineage

This topic has **no single lineage**; it has a fork, and
`../corpus/_LEDGER_runtime_sharing.md` states the answer to the convergence
question directly:

> **GPU sharing research is not converging on one mechanism. It has forked by
> hardware availability.**

- Where MIG exists (A100/H100 and successors): ParvaGPU → BOER (SC 2025, the
  direct successor at the same venue) → SMART-MIG (IPDPS 2026), plus the ISC
  2026 characterisation.
- Where MIG does not exist (Pascal, Turing, consumer and mid-range parts):
  `libsmctrl` → SGDRC (PPoPP 2025) and Bullet (ASPLOS 2026).
- Where tenants are untrusted and unmodifiable: gShare goes below CUDA into the
  kernel driver and gives up spatial sharing.
- Device-side runtime: NVSHMEM multi-GPU atomics + device-side CUDA graph
  launch → Mustard. Related but separately owned: **CUDASTF** (SC 2024), whose
  implementation ships as `cudax::stf` inside NVIDIA CCCL `[documentation]` and
  which the compiler cluster owns as a row.

Wider chains: `../synthesis/GPU_TOPIC_LINEAGES.md`.

## 6. Implementation families

All six are `REAL_SILICON`; there is **no simulator paper among this topic's
deep analyses**. Three carry inspected `[code]`. Two — SGDRC and Bullet —
depend on **`libsmctrl`, a reverse-engineered co-option of CUDA driver debug
logic pinned at CUDA ≤ 12.6**. That is **a single point of failure for two
top-tier systems papers, and neither paper discusses what happens when NVIDIA
removes it** `[../corpus/_LEDGER_runtime_sharing.md]`.

## 7. Important disagreements / tensions

**T1 — the schools' assessments of each other, in their own words, not this
repository's editorialising** (`../corpus/_LEDGER_runtime_sharing.md`):
- *Software school on MIG*: SGDRC — MIG "is available only in a few flagship
  GPUs … its granularity is too coarse … and can only reconfigure the
  allocation when it is idle" `[paper]`.
- *Software school on MPS*: SGDRC — MPS "statically partitions GPUs at the
  thread slice level and **cannot isolate VRAM bandwidth**, resulting in
  unmanaged contention" `[paper]`. Bullet ships MPS support but "replaced [it]
  with libsmctrl for dynamic control" `[paper]`.
- *Temporal school on itself*: gShare concedes "GPU virtualization is actually
  a temporal GPU sharing technology", risking underutilisation "if kernels
  cannot fill all SM cores" `[paper]`.
- *Hardware school on software sharing*: ParvaGPU justifies MIG on the grounds
  that under MPS "internal GPU resources such as caches and memory controllers
  are shared among workloads … lead[ing] to interference issues" `[paper]`.
  **Its baseline set contains no software-partitioning system.**

**T2 — no mechanism here provides complete isolation, and the corpus can name
two leaks by measurement.**
`../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md` shows **MIG
does not partition the last-level TLB**; the ISC 2026 paper shows **MIG does
not partition power**. Both are channels *below* the advertised partition
boundary. SGDRC's own answer — memory-channel colouring — is a third such
channel addressed in software, and SGDRC's ablation shows it is the one that
actually moves tail latency.

**T3 — the forks are essentially untested against each other.** SGDRC evaluates
on GPUs that **have no MIG** (P40, RTX A2000); ParvaGPU and the ISC 2026
characterisation evaluate on GPUs that **do**; gShare compares only against
FaaS caching systems. **No paper in this topic evaluates its mechanism against
a mechanism from a different school on the same silicon.** SGDRC states that
A100/H100 would "require slight adaptation".

**T4 — ParvaGPU and SGDRC are the exact opposite design choice and do not cite
each other.** ParvaGPU accepts the lattice and solves packing; SGDRC rejects
the lattice as too coarse and unavailable and rebuilds partitioning in
software. SGDRC's critique of MIG is **independently corroborated by ParvaGPU's
own artifact** `[code]`, which is a stronger form of agreement than a citation.

**T5 — a runtime capability, not a research idea, is what unblocked `J`.**
Mustard exists because multi-GPU device-side atomics arrived; it is bounded by
a **120-subgraph driver cap**. The most restraining limit in this topic's only
task-graph paper is a vendor constant.

## 8. Current limitations

**Coverage of `J` (runtime and task graphs) is thin and should be read as
thin.** One deep analysis, with **no performance number read**. CUDASTF (SC
2024), the other obvious member, is `CLOSED_ACCESS` here — its author page
carries an abstract but no PDF, `ieeexplore.ieee.org` → 418 and `dl.acm.org`
→ 403 — so it is a watchlist row owned by the compiler cluster. **Nothing in
this corpus supports a general statement about GPU task-graph runtimes.**

**Access, and one specific rate-limit, bound the sharing half.**
`arxiv.org/html/2606.29775v1` and `/pdf/` returned **HTTP 429 on five separate
attempts** while `/abs/` succeeded, so **SMART-MIG is `PUBLIC_FULLTEXT` by
access state but `ABSTRACT_ONLY` by evidence read** — under the gate it gets a
verdict and a watchlist entry, not an analysis. The same 429 wall blocked a
planned deep analysis of **Dilu** (ASPLOS 2025). Watchlist in the ledger's own
priority order: **µShare** (HPCA 2026, would resolve the limitation both
software-partitioning papers concede), SMART-MIG, Dilu, **BOER** (SC 2025),
**LEGO** (HPCA 2026, the only graphics/compute co-location case),
**ElasticRoom** (HPDC 2024), **AGIO** (ASPLOS 2026, `UNRESOLVED`).

**No `GPU_DELTA_ANALYSIS` is owed by any paper here** — the imported
`../../hpc_systems_operations/topics/gpu_operations.md` and
`../../hpc_systems_operations/topics/scheduling_resource_management.md` were read in full and grepped for
`MIG`, `MPS`, `GPU sharing`, `co-locat`, `spatial`: **zero hits**. Every
LLM-serving / DL-serving / serverless row carries
`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` for the pending `../../ai_hpc_systems/`
corpus, and **no claim is made about what that corpus contains**
(`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. T3 is a directly testable gap: run SGDRC's channel colouring and MIG on the
   same A100 with the same tenants. No paper in the corpus does.
2. What replaces `libsmctrl` if NVIDIA closes the debug path? Two top-tier
   papers depend on it and neither discusses it (§6).
3. If MIG partitions neither the last-level TLB nor power (T2), what *is* the
   isolation guarantee a MIG SLO rests on? The ISC 2026 paper raises the power
   channel; nothing in the corpus quantifies the combined effect.

## 10. Deeper lookup paths

`../corpus/_LEDGER_runtime_sharing.md` — the isolation-mechanism roll-up
(the cluster's central finding), "What each school says about the others'
isolation guarantees" (quoted, not paraphrased), the convergence answer, and
the priority-ordered watchlist → the six analyses above → the pinned artifacts
in each §12.8.
Cross-topic: `memory_virtualization.md` (STAR, the TLB leak),
`power_energy.md` (the power leak, and Lit Silicon's multi-GPU thermal
coupling), `compiler_programming.md` (CUDASTF).

# GPU_TOPIC_LINEAGES — cross-year lineage synthesis for the GPU corpus

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
corpus: `domains/gpu_systems/corpus/` — 85 deep analyses, 11 cluster ledgers
governs: `governance/ANTI_HALLUCINATION_RULES.md`, `governance/SOURCE_EVIDENCE_RULES.md`

---

## 0. How to read this document

This is a **routing-and-reasoning document**, not a survey. It records which
lineage edges the corpus can actually support and which it cannot.

**Evidence tag on every edge:**

| Tag | Meaning |
|---|---|
| `[paper]` | The later paper cites the earlier one, and the citation was read in the paper's own related work or reference list. |
| `[author-overlap]` | Shared authors between two papers, verified from both author lists. **This is weaker than `[paper]`** — a group working on two things is not a citation chain. |
| `[inference]` | This synthesis's reading, from two or more separately-read papers. Never a citation claim. |
| `NOT_CITED` | **Verified absence.** A targeted check of the later paper's related work / reference list found the earlier work absent. This is a first-class result. |
| `UNKNOWN` | Not established; not guessed. |
| `NOT_ESTABLISHED` | The corpus is silent on a question a reader would reasonably ask. |

**Four rules applied throughout.**

1. A plausible-looking progression is not a lineage. Where an expected
   progression fails, §9 records it as a finding of equal standing.
2. Every quantitative claim keeps its hardware / workload / baseline qualifier.
3. Where a paper's own claim is reproduced it is marked as the authors' claim,
   not verified here.
4. Papers reached only at census / abstract / title depth are **not** used to
   assert an edge. Several clusters hold large watchlists for exactly this
   reason; watchlist items appear here only as named gaps.

**One externally verified correction is folded in.** `GPU-ISC26-01` (PICO)
recorded the question "does PICO cite the SC 2024 interconnect study?" as
`UNKNOWN`. Settled here against the arXiv HTML of `2508.16809v1`: **PICO cites
it as reference [12]** (De Sensi, Pichetti, Vella, De Matteis, Ren, Fusco,
Turisini, Cesarini, Lust, Trivedi, Roweth, Spiga, Di Girolamo, Hoefler, SC'24).
That edge is upgraded from `UNKNOWN` to `[paper]` and graded
`EXTERNALLY_VERIFIED`. The corresponding row in
[`../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md)
should be updated.

**Companion documents.** Four areas are large enough to have their own file and
are summarised here only at the branch-point level:
- [`GPU_MEMORY_LINEAGE.md`](GPU_MEMORY_LINEAGE.md) — virtual memory / UVM / I/O paths
- [`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) — multi-GPU communication
- [`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md) — matrix units
- [`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) — per-generation facts

---

## 1. GPU virtual memory and address translation

Full treatment in [`GPU_MEMORY_LINEAGE.md`](GPU_MEMORY_LINEAGE.md). Branch
structure and verified edges only, here.

### 1.1 The verified chain

```
Bhattacharjee et al. (shared last-level TLB, CPU)
        |  [paper, cited by HDPAT]
        v
Trans-FW / IDYLL / SnakeByte (Li et al. 2023, GPU translation)
        |  [paper, cited by GRIT and by HDPAT]
        v
Barre Chord (ISCA 2024, page-walk-queue coalescing)   Valkyrie (inter-TLB locality)
        |  [paper] HDPAT cites and beats both, quantitatively
        v
HDPAT (HPCA 2026, wafer-scale, per-GPM GMMUs)
```
Anchor: [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md).
HDPAT→Barre Chord is the **cleanest single citation edge in the translation
branch** and it points from an in-corpus analysis to a paper the memory cluster
holds on its watchlist (no full text reachable).

Parallel, and **not** joined to that chain by any verified citation:

```
MASK (Ausavarungnirun et al., multi-app GPU TLB)
        |  [paper] STAR cites it and reports +25% average over it
        v
STAR (MICRO 2024, sub-entry sharing under MIG)
```
Anchor: [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md).
STAR↔HDPAT: **NOT_CITED in either direction** (verified from both papers'
related work). They share a *strategy* — reclaim existing translation capacity
rather than provision more — but not a citation.

### 1.2 The branch point that matters

The strategy split, established by reading three papers' framings against each
other, is **provision more translation bandwidth** vs **reclaim what exists**:

| Paper | Contended resource | Reclaimed from |
|---|---|---|
| [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md) STAR | 16-sub-entry L3 TLB entry | the other MIG tenant's unused sub-entries |
| [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md) HDPAT | walker throughput vs 16 IOMMU walkers | idle per-chiplet GMMUs |
| Heliostat (ISCA 2025, **watchlist**, abstract only) | translation bandwidth | the ray-tracing accelerator |

Heliostat's abstract states the same framing HDPAT uses — prior work "focused on
better utilizing the provided translation bandwidth" whereas the goal is to
"fundamentally increase" it `[official-web: yonsei.elsevierpure.com]`.
**No citation link between HDPAT and Heliostat was verified** — `UNKNOWN`.

### 1.3 Author-cluster lineages (weaker evidence, labelled as such)

- Yueqi Wang, Bingyao Li, Aamer Jaleel, Jun Yang, Xulong Tang co-author both
  GRIT (HPCA 2024) and STAR (MICRO 2024) `[author-overlap]`, verified from both
  author lists. Yueqi Wang is also first author of **OASIS** (HPCA 2025,
  watchlist) — the multi-GPU placement successor. `[author-overlap]`
- Won Woo Ro co-authors **TTA** (MICRO 2024, RT-unit generalisation),
  **Heliostat** (ISCA 2025, page walks on the RT unit), **Marching Page Walks**
  and **LATPC**. `[author-overlap]` — this is the single densest author bridge
  between two otherwise non-citing branches of the corpus.

---

## 2. Sparse GPU kernels

Source: `_LEDGER_sparse_irregular.md` §7, plus the analyses.

### 2.1 The verified SpMM chain — and it is a real chain

```
TC-GNN, VectorSparse, CLASP, Magicube, DTC-SpMM   (all 16x1 granularity)
        |  [paper] cited and benchmarked by both PPoPP'25 papers
        v
SMaT (SC 2024)        -- fixes the block AT the m16n8k16 operand shape,
  |                      attacks TILE COUNT by Jaccard row clustering
  |  [paper] precursor
  v
FlashSparse (PPoPP 2025) -- attacks TILE SHAPE: A*B=(B^T A^T)^T exploits n=8,
  |                          halves blocking to 8x1, removes 43% of MMA calls
  |                       Acc-SpMM (PPoPP 2025) -- attacks the SCHEDULE
  v
Insum (ASPLOS 2026)   -- attacks the SOURCE LANGUAGE, reaches the same MMA
                         through Triton's tl.dot
```
Anchors: [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md),
[`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md),
[`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md),
[`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md).

**All four run dense MMA on dense blocks.** None uses 2:4 Sparse-Tensor-Core
metadata. SMaT's text states this explicitly: the block format is BCSR with
`m16n8k16` and "not NVIDIA's structured 2:4 sparsity format introduced in
Ampere" `[paper]`. See [`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md) §5
for why conflating these is a category error.

**Branch point inside the chain**: FlashSparse ↔ Acc-SpMM are the same PPoPP
2025 session (S8 Tensor Cores), independently found the same operand-swap
insight, and `NOT_CITED` in either direction (same submission cycle).

### 2.2 The verified divergence: SpMM and SpGEMM went different ways

This is the sparse cluster's principal finding and it rests on a targeted
full-text query, not on topical reading.

- **SpGEMM has no matrix unit in it at all.** Ocean (ICS 2026) **does not
  contain the strings "Tensor Core", "MMA" or "tensor core" anywhere in its text
  or references** `[paper, verified by targeted query]`. Its related work names
  cuSPARSE, spECK, OpSparse, TileSpGEMM, HSMU-SpGEMM, MOSparse, AC-SpGEMM and
  Bellavita's Trident partitioning.
  Anchor: [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md).
- Cause, stated mechanically: SpMM's output pattern is known, so a format can be
  designed to feed a fixed instruction. SpGEMM's output pattern is unknown, and
  **no matrix unit helps with an unknown output pattern**. SpGEMM therefore
  stayed an atomics-allocation-and-scheduling problem.

### 2.3 The unpredictable-output-size problem, solved three times without contact

| Paper | Answer | Cost it pays |
|---|---|---|
| INFINEL (PPoPP 2024, unread) | chunked / over-allocated output | UNKNOWN |
| [`GPU-ASPLOS25-107`](../corpus/GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md) GPUlog | exact two-pass join (count, allocate, recompute) | doubled outer-relation reads; the paper's own limitation 5 |
| [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md) Ocean | probabilistic estimate (HyperLogLog + `atomicMax`) + overflow fallback kernel | 0.3–1.2% overflow rows; 2.2x peak memory; matrix `JP` fails |

[`GPU-PPoPP24-146`](../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md)
(Gallatin) is the general-purpose device-side allocator that would subsume all
three. **None of them uses it, and neither read paper cites Gallatin or
INFINEL** — `NOT_CITED`. GPUlog uses RAPIDS RMM; Ocean uses fixed geometric
binning.

### 2.4 Load imbalance, and the PPoPP 2026 convergence

Three independent PPoPP 2026 papers answer irregular-search load imbalance with
dynamic work redistribution:
[`GPU-PPoPP26-105`](../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md)
(hierarchical work stealing; the inter-block tier alone is worth 25.94x–38.41x in
its own ablation), Root-Down Exposure / RDMCE (1.25–5.38x over prior GPU MCE,
unread), and
[`GPU-PPoPP26-104`](../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md)
(host-side priority aggregation; kernel count to 1.10%/1.48% of baseline).
Two of the three are the same lab; RDMCE is not. This is convergence on a
**method**, not a citation chain — `[inference]` plus `[author-overlap]`.

### 2.5 Verified lab lineage (`[author-overlap]`, verified from read PDFs)

SSSLab / China University of Petroleum-Beijing (Weifeng Liu, Zhou Jin):
DASP (SC 2023) → PanguLU (SC 2023) → AmgT + Mille-feuille (SC 2024) → Cubie +
DiggerBees + Trojan Horse (PPoPP 2026).
Anchors in corpus: [`GPU-SC24-103`](../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md),
[`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md),
[`GPU-PPoPP26-104`](../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md),
[`GPU-PPoPP26-105`](../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md).
**Internal tension worth keeping:** DASP is a baseline that beats SMaT by ~28x on
`dc2` (2.5 GFLOP/s vs 69.1 GFLOP/s, SuiteSparse `dc2`, A100) — a same-family
baseline defeating a matrix-unit method on a power-law block distribution.

---

## 3. Matrix-unit exploitation

Full treatment in [`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md).

The headline, stated here so it is not missed: the expected progression
**scientific kernels → sparse kernels → precision emulation → new numeric
formats is NOT one citation chain.** It is three largely disjoint branches that
meet in exactly one paper,
[`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
(Cubie), whose reference list is the only place in the corpus where the stencil,
sparse and emulation literatures appear together. See §9.6.

---

## 4. GPU communication

Full treatment in [`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md).

The headline: the progression **GPU-aware MPI → device-initiated communication →
symmetric memory → GPU-resident collective control is NOT SUPPORTED as a
progression** by the papers' own related work. It is a real taxonomy of
mechanisms, and the corpus's recommended replacement is a two-axis map of *who
initiates* x *which fabric is crossed*, with the finding that the **fabric axis,
not the calendar, predicts the initiation axis**. See §9.1.

---

## 5. Fixed-function-unit repurposing

Source: `_LEDGER_fixed_function_repurposing.md` §4.

### 5.1 The verified chain — this branch has the corpus's best citation evidence

```
Wald et al. 2019 "RTX Beyond Ray Tracing"   <- named by Arkade as the first non-graphics use [paper]
        |
Zellmann 2020 (graph drawing) ; Evangelou 2021 (radius search)
        |
RTNN (Zhu 2022) ; RT-DBSCAN, TrueKNN (Nagarajan 2023) ; RTIndeX (2023)
        |
   +----+----------------------------------------------+
   |                                                    |
SOFTWARE BRANCH (no hardware change)              HARDWARE BRANCH (widen the predicate)
Arkade (ICS 2024) ---- [paper] cited by HSU ---->  HSU (MICRO 2024, AMD RDNA3-style datapath)
RayJoin (ICS 2024)                                 TTA/TTA+ (MICRO 2024, NVIDIA-style RTA)
RT-BarnesHut (PPoPP 2025)                                |
LibRTS (PPoPP 2025) -- [paper] cites BOTH MICRO'24 ----->|
RTSpMSpM (ISCA 2025)                                     |
X-HD (ICS 2026)                                          |
        \                                                |
         \-- Heliostat (ISCA 2025): the same move applied to the GPU PAGE TABLE
                                                         |
RENDERING-PIPELINE SUPPORT (characterise the unit, then improve it for graphics)
Chou treelet prefetcher (MICRO 2023) -> Treelet (ASPLOS 2025) -- [paper] cites TTA+HSU
CoopRT (ISCA 2025) -- [paper] cites TTA+HSU -> TTP (ISCA 2026) -- [paper] cites TTA+HSU+Heliostat+LibRTS+Arkade
```

Anchors: [`GPU-ICS24-125`](../corpus/GPU-ICS24-125--arkade-knn-non-euclidean-gpu-ray-tracing.md),
[`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md),
[`GPU-MICRO24-122`](../corpus/GPU-MICRO24-122--tta-generalizing-ray-tracing-accelerators-tree-traversals.md),
[`GPU-PPoPP25-128`](../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md),
[`GPU-ASPLOS25-124`](../corpus/GPU-ASPLOS25-124--treelet-accelerated-ray-tracing-gpus.md),
[`GPU-ISCA25-127`](../corpus/GPU-ISCA25-127--cooprt-bvh-traversal-cooperative-threads.md).

The forward citation is exact and worth quoting because it is the strongest
single edge in the corpus. Treelet's conclusion `[paper]`: "With proposals from
Ha et al. [14] and Barnes et al. [6] that extend ray tracing accelerators in GPUs
to support more general tree traversal workloads, we believe the hardware
modifications and treelet queue optimizations in this work in conjunction [could]
accelerate general tree traversal workloads on GPUs as well." Ha et al. [14] =
TTA; Barnes et al. [6] = HSU.

### 5.2 The verified non-edge inside the category

**The RT branch and the rasterisation branch do not cite each other.**
[`GPU-HPCA25-126`](../corpus/GPU-HPCA25-126--vr-pipe-streamlining-graphics-pipeline-volume-rendering.md)
(VR-Pipe) cites **no** RT-core repurposing work at all `[paper — verified by
targeted query]`, and no RT paper read in the corpus cites VR-Pipe, RoCC or
DEFCON. `NOT_CITED`, both directions. The category is real in **mechanism** —
the same move recurs on the RT core, the ROP/stencil and the texture unit — but
it is **not yet self-aware across units**.

### 5.3 The measurement caveat that must travel with this branch

The two halves' headline numbers are **not comparable and must never share a
table column**: the software branch measures real silicon (RTX 3090, RTX 4060 Ti)
against SIMT baselines and reports 10x–100x; the hardware branch simulates
(Accel-Sim V100, Vulkan-Sim 8–30 SM scale models, Emerald) against an
*already-RT-accelerated* baseline and reports 1.1x–2.5x. Worse, the two MICRO
2024 papers do not model the same RT hardware: **HSU generalises an AMD
RDNA3-style datapath where software owns the traversal stack; TTA generalises an
NVIDIA-style RTA where hardware owns it.** Their numbers must not be compared
directly.

---

## 6. Profiling, simulation and performance modelling

Source: `_LEDGER_profiling_reliability.md` §5, `_LEDGER_core_execution.md` §3.

### 6.1 Verified edges

- **GPA is the hub.** LEO names GPA as the work that "pioneered backward slicing
  for GPUs, but GPA supports only NVIDIA GPUs and cannot trace memory access
  dependencies through synchronization instructions such as AMD's `s_waitcnt`"
  `[paper]`; ScopeAdvice independently lists GPA among the instruction-level
  tools it complements `[paper]`. A 2024 synchronization-scope tool and a 2026
  cross-vendor stall slicer converge on one ancestor.
  Anchors: [`GPU-SC26-41`](../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md),
  [`GPU-MICRO24-41`](../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md).
- **LEO → DeepContext** `[paper]`: LEO names DeepContext and PASTA as
  cross-platform tools that "lack instruction-level root-cause analysis", and
  positions itself one abstraction level below DeepContext (ASPLOS 2026).
- **Stated gap → filled gap, across two venues** `[paper]`:
  [`GPU-ICS25-145`](../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md)
  concludes "Line-level stall attribution is a crucial capability missing from
  Omniperf"; that is precisely what LEO builds. This rests on both papers' own
  text, not on topical adjacency.
- **MICRO'24 NoC dissection → MICRO'25 core dissection** `[paper]`:
  [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)
  lists "Jin et al. (2024)" — [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md) —
  among the reverse-engineering works it builds on. Real-GPU NoC dissection →
  real-GPU core dissection, both correcting Accel-Sim, one year apart.
- **Shared sampling literature** `[paper, both]`:
  [`GPU-MICRO25-01`](../corpus/GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md) and
  [`GPU-HPCA24-41`](../corpus/GPU-HPCA24-41--gpu-scale-model-simulation.md) both name
  **Principal Kernel Analysis, TBPoint and Photon** as the prior art.

### 6.2 Branch point: the two halves of simulation cost were never composed

STEM+ROOT reduces *how many kernel invocations* are simulated (3x to 31,719x,
depending on kernel-call multiplicity); Scale-Model Simulation reduces *how large
a machine* is simulated (9.3x, and it is the only method that works when no model
of the target exists at all). They share a literature and reduce orthogonal
costs. **Neither paper mentions composing them, and nothing in either design
forbids it** — `[inference]`.

Carry this caveat with STEM's headline: **the contribution is bounded error, not
speed.** Photon is 1.54x faster on the CASIO suite at 9.85% error against STEM's
0.36% `[paper]`. The 31,719x figure is meaningless without its error column.

### 6.3 The live disagreement about what a GPU issue stage is

[`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md)
(GhOST) adds out-of-order issue on top of Accel-Sim's scoreboard-plus-
operand-collector core and diagnoses its predecessor LOOG's failure as
*operand-collector congestion*.
[`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)
measures that same baseline at **34.03% MAPE against a real RTX A6000** and finds
that real Turing/Ampere/Blackwell cores use **compiler-set control bits, not a
scoreboard**, and have **no operand collector units at all**. The two papers are
in direct tension about what the issue stage *is*. **Neither evaluates against
the other** — GhOST predates, and the interaction is unevaluated. `NOT_CITED`.

### 6.4 The best-corroborated microarchitectural fact in the corpus

Two independent 2024 papers converge on partitioned-L2 non-uniformity by
different methods: [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md)
by SM pinning + correlation clustering (~200 vs ~400 cycles across an A100/H100
partition, plus the TPC/GPC hierarchy and an undocumented **CPC** level on H100),
and [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md)
by p-chase (near/far hit 208 / 356.6 cycles on A100; 258 / 414.1 cycles on H800).
Different methods, same structure. `[inference]`, from two measured papers.

---

## 7. Power and energy

Source: `_LEDGER_power_energy.md` §2.

### 7.1 Verified edges

- **[`GPU-ICS26-183`](../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md)
  cites [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md)** `[paper]`
  — Wattchmen's related work cites "Oles et al. (2024) on Volta static power
  (~80 W)". A reliability paper is being used by later power-modelling work as a
  V100 static-power calibration source, a use its own authors did not foreground.
- **[`GPU-ISCA26-187`](../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md)
  cites [`GPU-ASPLOS24-186`](../corpus/GPU-ASPLOS24-186--polca-power-management-opportunities-llms-cloud.md)** `[paper]`
  — Lit Silicon's related work names *Patel et al. (2024), "Characterizing Power
  Management Opportunities for LLMs in the Cloud"*. The relationship is an
  inversion, not a continuation: POLCA takes power *away* from GPUs at row scale
  to fit a facility budget; Lit Silicon moves power *between* GPUs inside one
  node to remove a synchronisation loss. Lit Silicon positions itself as
  orthogonal to cluster-level policy.
- **Nine-year data-dependence lineage, from the paper's own citations** `[paper]`:
  Lucas et al. 2016 (ALUPower) → Bhalachandra et al. 2022 (random-vs-zero
  methodology, adopted) → Gregersen et al. 2025, cited in
  [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md).

### 7.2 Convergences without citation (`[inference]`, both directions verified)

- **The cross-vendor sensor twins do not cite each other.**
  [`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md)
  and [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md)
  both drive a square wave, both find an undocumented moving average, both find
  the tool-visible cadence differs from the native cadence — then diverge.
  Yang et al. *identify* the NVIDIA boxcar by aliasing and Nelder–Mead against an
  **external ElmorLabs PMD-USB**, and can state `W = 25 ms, T = 100 ms` for
  A100/H100. McDaniel et al. *bypass* the AMD filter by differentiating the
  energy counter, and validate only sensor-against-sensor. `NOT_CITED`.
  **Finding: AMD and NVIDIA power measurement are not being treated as the same
  problem, and no `W`/`T` table exists for any AMD GPU.** `NOT_ESTABLISHED`.
- **Thermal non-interchangeability, two vendors, two chassis, one conclusion.**
  [`GPU-MICRO25-185`](../corpus/GPU-MICRO25-185--distributed-training-power-performance-thermal.md)
  measures up to 27% temperature differential between rear and front GPUs in
  air-cooled NVIDIA HGX nodes and 5–10 °C intra-package skew on MI250;
  [`GPU-ISCA26-187`](../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md)
  measures 1.155x temperature and 1.062x frequency spread across an 8-GPU MI300X
  node and shows it produces persistent stragglers. **Neither cites the other.**
  `NOT_CITED`. Lit Silicon adds the *mechanism* by which thermal difference
  becomes a synchronisation equilibrium.

### 7.3 The methodological finding that governs every number in this area

Of ten papers in the cluster with any instrumentation record, **exactly one has a
real external ground truth** ([`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md),
and it is the paper whose whole subject is the sensor). One more (POLCA) has
row-level PDU telemetry. The remaining eight validate a GPU power number against
a GPU power sensor, or do not say what they measured with. **Three papers — one
of them an ISCA 2026 paper whose headline is a 4% power saving — disclose neither
their sensor nor their sampling rate.** See
[`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §7.

---

## 8. GPU sharing

Source: `_LEDGER_runtime_sharing.md`.

### 8.1 There is no chain here; there is a fork by hardware availability

The corpus's answer to "is GPU sharing converging on one mechanism?" is **no —
it forked, and the forks are untested against each other.**

| Boundary drawn in | Mechanism | Quantum | Reconfiguration | Paper | Leaks through |
|---|---|---|---|---|---|
| Silicon partition | MIG (+ compute instances) | A100: 1/2/3/4/7 GPCs (5 and 6 illegal); H100 96 GB: 16/32/60/64/132 SMs | **offline only** | [`GPU-SC24-161`](../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md), [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md) | last-level TLB; device-wide power/clock domain |
| Process multiplexing | MPS | client process | daemon restart | baseline in the above | caches, memory controllers, VRAM bandwidth |
| SM/TPC masking (software) | `libsmctrl` TPC bitmask | 1 TPC = 2 SMs | microseconds | [`GPU-PPoPP25-164`](../corpus/GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md), [`GPU-ASPLOS26-166`](../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md) | memory system, unless separately coloured |
| VRAM channel colouring | shadow page table + modified `nvidia-uvm` | 2 KiB sectors | at LS-activity boundaries | [`GPU-PPoPP25-164`](../corpus/GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md) only | needs kernel source; closed vendor libraries excluded |
| Kernel driver (mediated device) | `vfio-mdev` vGPU, 57 intercepted ioctls | memory slice 128 MB–40 GB; compute = whole GPU | hot-plug ~700 ms → <1 ms | [`GPU-ASPLOS26-163`](../corpus/GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md) | everything spatial |
| Time only | round-robin channel activation, 20 ms period | whole GPU | period boundary | [`GPU-ASPLOS26-163`](../corpus/GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md) | SM occupancy entirely |

### 8.2 The two independent falsifications of MIG isolation

- **Translation path.** [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md)
  shows the last-level TLB is **not** partitioned across MIG instances; co-running
  tenants lose **40% on average versus running alone** (A100, MGPUSim, three
  tenants at (3g,2g,2g)/(3g,3g), 64 KB pages).
- **Power/clock path.** [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md)
  measures the H100 96 GB lattice directly and finds a residual **power-throttling**
  cross-instance channel.

Together: **MIG isolates SMs and memory slices, but not the L3 TLB and not the
power/clock domain.** That pair is the strongest statement this corpus can make
about the limits of hardware GPU partitioning. Neither paper cites ParvaGPU and
ParvaGPU cites neither of them — `NOT_CITED` in all directions; the pairing is
this corpus's contribution, not the field's.

### 8.3 Isolation-strength ordering (`[inference]`, from the analyses read together)

`MIG > TPC-mask + channel-colouring (SGDRC) > TPC-mask alone (Bullet) >
time-slicing (gShare)` — **and every one of them leaks somewhere.**

### 8.4 The single point of failure nobody discusses

Both software-partitioning papers depend on **`libsmctrl`**, which "co-opts
preexisting debug logic in the CUDA driver library" and is pinned at **CUDA ≤
12.6**. Two top-tier systems papers rest on one reverse-engineered, undocumented
driver path, **and neither discusses what happens when NVIDIA removes it** —
`NOT_ESTABLISHED`.

---

## 9. Progressions the corpus does NOT support

Every item here is a **verified negative**: an expected progression that the
papers' own citations do not support, established by reading the later work's
related work and finding the earlier work absent, or by finding the later work
contradicting rather than building on the earlier.

### 9.1 "GPU-aware MPI → device-initiated → symmetric memory → GPU-resident collectives"

**NOT SUPPORTED as a progression.** Four kinds of `[paper]` counter-evidence:

1. **The stages coexist in the same venue-years, and the newest papers are not
   the most device-resident.** IPDPS 2026 contains both
   [`GPU-IPDPS26-01`](../corpus/GPU-IPDPS26-01--nimble-skew-to-symmetry-multipath-balancing.md)
   (device-resident data path, paper-asserted) and
   [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md)
   (fully host-initiated MPI + vendor libraries at 2,048 GPUs). SC 2026 contains
   both [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md)
   (device-resident via GDAKI) and
   [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md)
   (host-enqueued `ncclAllReduce`, preserved deliberately). If this were a
   progression the 2026 host-driven papers would be rearguard work; PCCL reports
   up to **168x over RCCL for reduce-scatter at 2,048 MI250X GCDs on Frontier**.
2. **The symmetric-memory "stage" is contested, not passed through.** See §9.2.
3. **Control placement is a property of the fabric, not the calendar.** See §9.3.
4. **The most recent large-scale collectives paper does not cite the
   device-initiated line at all.** See §9.4.

### 9.2 "Symmetric memory is a settled step the field built on"

**NOT SUPPORTED — two papers one venue-cycle apart reach opposite conclusions.**
- [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md)
  (MSCCL++, ASPLOS 2026) states: "We could not find any implementation where
  NVSHMEM outperforms NCCL (or MSCCL++) for collective communication" `[paper]`.
  An explicit rejection.
- [`GPU-ASPLOS24-21`](../corpus/GPU-ASPLOS24-21--t3-transparent-tracking-triggering-compute-collective-overlap.md)
  (T3, ASPLOS 2024) argues NVSHMEM "requires explicit synchronization and doesn't
  automatically orchestrate collective progress" `[paper]` — treats symmetric
  memory as insufficient, not as a step to build on.
- [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md)
  (SC 2026) does the opposite: adopts PGAS/symmetric memory as a core design
  principle and cites the SHMEM lineage — **and then reports that MSCCL++'s
  multicast variant hung on GB200 and had to be excluded from comparison**
  `[paper]`.

This is a live disagreement, not a succession.

### 9.3 "Device-initiated communication is a generation of the field"

**NOT SUPPORTED — it is a property of the fabric.**
[`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md)
is decisive: the *same runtime* is device-resident on mlx5 InfiniBand (kernels
build work-queue elements and ring the User Access Region doorbell) and only
device-*triggered* on HPE Slingshot's CXI provider (the host pre-stages bounded
operations in a 256-entry Deferred Work Queue against a 2047-counter budget; the
GPU merely rings a doorbell). GICC coins **"GPU-triggered rather than
GPU-initiated"** for exactly this `[paper]`. MSCCL++ reports the same constraint
from the other side — "Current hardware interconnects require a CPU thread to
initiate the data transfer" — and does not support GPU-initiated RDMA at all,
while being fully device-resident for intra-node MemoryChannel/SwitchChannel
`[paper]` `[code]`. **A single paper occupies two "stages" at once, depending on
which link is crossed.**

### 9.4 "Large-scale collectives work builds on the device-initiated line"

**NOT SUPPORTED — verified absence.**
[`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md)
(PCCL, IPDPS 2026) has **no comparison with MSCCL, no comparison with
GPU-initiated/NVSHMEM approaches, and no discussion of kernel-resident collective
implementations or device-side algorithm selection** `[paper]`. `NOT_CITED`.
Likewise [`GPU-ISC26-01`](../corpus/GPU-ISC26-01--pico-performance-insights-collective-operations.md)
(PICO), the field's most capable collective-benchmarking framework, supports
**only MPI, NCCL and RCCL** — no SHMEM/NVSHMEM backend — and therefore *cannot
observe* a device-initiated path at all.

### 9.5 "Sparse GPU work is converging on matrix-unit exploitation"

**NOT SUPPORTED — it split.** SpMM converged on matrix-unit exploitation via
format design; SpGEMM, sparse solvers and graph workloads converged on load
balancing and synchronisation with no matrix unit in sight (§2.2). The sharpest
single data point: **Niu and Casas wrote BerryBees (PPoPP 2025, BFS on bit Tensor
Cores) and then DiggerBees (PPoPP 2026, DFS with no matrix unit at all)**
`[author-overlap]` + `[paper, DiggerBees uses BerryBees as a baseline]`. The same
authors declining to reuse the matrix unit one year later is the strongest
available evidence that this community does not regard fixed-function-unit
repurposing as the general answer to irregularity.

### 9.6 "Matrix-unit work is one chain: scientific → sparse → emulation → formats"

**NOT SUPPORTED — three largely disjoint branches.** Full argument in
[`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md) §1–§4. The stencil
branch, the sparse branch and the emulation branch each have a clean internal
citation chain and essentially no citation traffic between them; the only paper
whose reference list contains all three is
[`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
(Cubie), and it is a characterisation paper, not a member of any branch.

### 9.7 "The sparse-kernel community engages the RT-unit repurposing line"

**NOT SUPPORTED — verified absence in both read papers.** SMaT (SC 2024) was
queried against its entire text and references for "ray tracing", "RT core",
"RT unit", "BVH", "RTSpMSpM", "LibRTS": **no hits on any of the six**. Ocean
(ICS 2026): **no hits on any of the six** `[paper, targeted query]`. `NOT_CITED`.

### 9.8 "Fixed-function repurposing is one self-aware community"

**NOT SUPPORTED across units.** The RT branch and the rasterisation branch do not
cite each other in either direction (§5.2). The category is real in mechanism —
the same move recurs on the RT core, the ROP/stencil and the texture unit — but a
survey that asserted a unified community would be overstating the citations.

### 9.9 "GPU race detection and over-synchronization analysis are one line"

**NOT SUPPORTED — the exact duals do not cite each other.**
[`GPU-SC24-41`](../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md) (HiRace,
SC 2024) and [`GPU-MICRO24-41`](../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md)
(ScopeAdvice, MICRO 2024) analyse the same programs over the same CUDA scope
lattice and cite the same baselines (iGUARD, compute-sanitizer), yet **HiRace is
absent from ScopeAdvice's related work and ScopeAdvice's problem is absent from
HiRace's** `[paper, both]`. `NOT_CITED`. Their independent characterisations of
iGUARD are mutually consistent (27–649x vs ">30x average with outliers to
~1000x"), which strengthens both and makes the absence more striking.

### 9.10 "GPU compression is one field"

**NOT SUPPORTED — four mutually non-citing communities working on the same GPU
problem**, verified in both directions for each pair:
1. **Error-bounded lossy (SZ family)** — [`GPU-SC24-81`](../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md),
   [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md),
   [`GPU-ICS26-81`](../corpus/GPU-ICS26-81--gpz-gpu-lossy-compressor-particle-data.md).
2. **Compression-in-collectives** — [`GPU-SC26-22`](../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md)
   (cites gZCCL/ghZCCL/COCCL and **no standalone GPU compressor**).
3. **Hardware cache compression** — [`GPU-ISCA25-81`](../corpus/GPU-ISCA25-81--ecco-entropy-aware-cache-compression-hbm-bandwidth.md)
   (cites BDI, Buddy Compression, GIST, JPEG-ACT, the LLM-quantization
   literature; **no SZ-family work**).
4. **Lossless FP** — [`GPU-ASPLOS25-81`](../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md)
   (compares against 18 compressors and **cites none of cuSZ, cuSZp, cuSZp2,
   FZ-GPU or cuZFP**).
**Authors overlap heavily** — Sheng Di, Franck Cappello, Jiajun Huang and
Xiaodong Yu appear on both sides of the (1)/(2) split. So this is not two
disjoint groups of people; it is two disjoint citation practices. Recorded as an
observation about the literature, with no claim about intent.

### 9.11 "GPU health telemetry predicts application slowdown"

**FALSIFIED, not merely uncited.**
[`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md)
builds a per-GPU FP16 GEMM instrument, measures real device heterogeneity (up to
**28% spread system-wide on Perlmutter's A100s**; 12% per-GCD on Frontier's
MI250X) — and then shows it does **not** reach application runtime: **Spearman
0.07 and 0.08** against the count of slowest-1% GPUs in an allocation, unchanged
at the 10% and 30% thresholds `[paper]`. Any argument that GPU health telemetry
predicts application slowdown must now clear this bar. The variance instead sits
in GPU-resident collectives (NCCL/RCCL `Allreduce` up to 24x slower on Frontier)
and in NIC/PCIe counters.

### 9.12 "A GPU generation's scale-model can answer next-generation questions"

**NOT SUPPORTED by its own author.**
[`GPU-HPCA24-41`](../corpus/GPU-HPCA24-41--gpu-scale-model-simulation.md) states
the binding dependence is per-SM architecture, not size: "If a next-generation
target has different per-SM architecture, the methodology requires constructing
new scale models with matching per-SM resources" `[paper]`. The method
extrapolates across *size within a microarchitecture generation* and never across
generations.

### 9.13 "The unified-memory characterisation line and the unified-memory mechanism line are one literature"

**NOT SUPPORTED, but a shared ancestor exists.** SUV
([`GPU-MICRO24-01`](../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md),
NVIDIA-mechanism side) and the AMD SVM study
([`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md),
characterisation side) do **not** cite each other — `NOT_CITED`. But both cite
**Ganguly et al.** as foundational UVM characterisation/prefetching work
`[paper, both]`. That shared ancestor is a real, citation-grounded connection;
a direct edge is not.

### 9.14 Negatives that are recorded but not resolvable from the corpus

- **SPIDER/SPTCStencil (PPoPP 2026) vs SparStencil (SC 2025).** Same problem,
  same mechanism (Sparse Tensor Cores for stencils via a structured-sparsity
  transform), one venue cycle apart. **The SPTCStencil text read does not cite
  SparStencil** while claiming to be "the first to harness SpTCs for acceleration
  beyond deep learning domains" `[paper]`. Priority and independence:
  **`UNRESOLVED`** — SparStencil has no reachable full text. This is a
  `NOT_CITED` whose *meaning* is undetermined; it is recorded, not adjudicated.
- **hZCCL (SC 2024) in NCCLZ's related work.** NCCLZ cites gZCCL, ghZCCL and
  COCCL by name; hZCCL was **not confirmed cited** in the read text —
  `UNKNOWN`, not `NOT_CITED`.

---

## 10. Where the corpus is silent

Recorded so a reader does not mistake silence for absence of a phenomenon.

- **No `W`/`T` sensor-window table exists for any AMD GPU.** `NOT_ESTABLISHED`.
- **No paper in the GPU-sharing cluster evaluates its mechanism against a
  mechanism from a different school on the same silicon.** SGDRC evaluates on
  GPUs with no MIG (Tesla P40, RTX A2000); ParvaGPU and the ISC 2026
  characterisation evaluate on GPUs that have it; gShare compares only against
  FaaS caching systems. `NOT_ESTABLISHED`.
- **Whether native FP64 matrix throughput or FP64 emulation is the right bet** is
  the live question of the matrix-unit area and the corpus contains papers on
  both sides that do not reconcile. See
  [`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §6.1.
  `NOT_ESTABLISHED`.
- **Whether STEM+ROOT and Scale-Model Simulation compose.** `NOT_ESTABLISHED`.
- **What bounds GPU compressor throughput.** Of the compression papers read at
  full text, exactly one reports an achieved-vs-peak bandwidth figure (GPZ, one
  stage only). Rooflines, occupancy figures and achieved-bandwidth measurements
  are essentially absent from this literature. GPZ's own anomaly is unexplained
  by its authors: compression barely moves from RTX 4090 to H100 (598 → 616 GB/s)
  while decompression rises 651 → 1091 GB/s, so H100 compression is *not*
  bandwidth-bound and **nothing says what it is bound by**. `NOT_ESTABLISHED`.
- **What happens to SGDRC and Bullet when NVIDIA removes `libsmctrl`.**
  `NOT_ESTABLISHED`.

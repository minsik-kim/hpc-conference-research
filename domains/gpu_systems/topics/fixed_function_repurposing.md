# Fixed-function GPU units repurposed for general computation (taxonomy Q)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **STRONG, and this category did not exist when the pass
began.** Eight deep analyses, all `CORE_GPU`, all `PUBLIC_FULLTEXT`. Verdict
ledger: `../corpus/_LEDGER_fixed_function_repurposing.md`.

## 0. Why this topic exists at all

**Category `Q` was added during this work because the evidence demanded it.**
It was not in the initial taxonomy sketch. `../corpus/_LEDGER_fixed_function_repurposing.md`
§4 sets out the argument and the evidence, and the conclusion it reaches is
specific: **yes, it is a real category, but it must be defined by *mechanism*,
not by workload — and it has two branches plus a supporting literature that
must not be folded into it.**

The evidence, as the ledger records it:

1. **The papers cite each other across the software/hardware divide, in both
   directions.** `../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md`
   (HSU) cites Arkade, RTIndeX, RTNN, Zellmann, Morrical, Wald and Evangelou as
   the reformulate-as-ray-casting predecessors it exists to replace `[paper]`.
   `../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md`
   (LibRTS) cites **both** MICRO 2024 hardware papers by name and positions
   them as complementary hardware research `[paper]`.
   `../corpus/GPU-ASPLOS25-124--treelet-accelerated-ray-tracing-gpus.md` closes
   by naming "Ha et al. [14] and Barnes et al. [6]" as works that "extend ray
   tracing accelerators in GPUs to support more general tree traversal
   workloads" `[paper]`. **TTP (ISCA 2026) enumerates the category explicitly**
   under a "non-graphics RT-core uses" heading — Heliostat, LibRTS, TTA,
   Arkade `[paper, TTP]`. A prefetcher paper listing those four together is the
   strongest single piece of evidence that **the category is legible from
   inside the RT-architecture community rather than imposed from outside.**
2. **The same mechanism recurs on three different fixed-function units** — RT
   core (HSU, TTA, Arkade, LibRTS, RT-BarnesHut, RTSpMSpM, X-HD, Heliostat);
   **ROP / rasteriser / stencil** (VR-Pipe, RoCC, Gaussian Blending Unit);
   **texture unit** (DEFCON, TMModel). If the category were really "RT cores",
   the ROP and texture instances would be unexplained.
3. **It has a stable internal structure that predicts the papers' shape** — the
   HW/SW split (§3), which is a consequence of the defining constraint: the
   unit is fixed, so you either bend the problem or you open the unit.

## 1. Problem landscape

A GPU carries silicon whose function is frozen for graphics. Its value to a
general-purpose programmer is not what it computes but **what it is**: a
divergence-tolerant datapath that resolves one level of a spatial hierarchy per
instruction, or a ROP that blends and tests at the fragment rate, or a texture
unit that filters. The work in this topic obtains non-original-purpose value
from such a unit in one of exactly two ways — and the corpus's central caution
is that **the two ways produce numbers that are not comparable** (§7, T1).

## 2. Key concepts

RT core / ray accelerator / BVH traversal unit, and the **AMD-style datapath
(software owns the traversal stack) vs NVIDIA-style RTA (hardware owns it)**
distinction, which is load-bearing; ray-AABB and ray-triangle predicates as the
fixed interface; encode-as-geometry (e.g. RTIndeX representing 32/64-bit
integer keys as **288-bit triangle primitives**); treelets and traversal-stack
locality; SIMT efficiency under divergence; ROP / Z-stencil / blend and early
termination; tile-based deferred rendering; OptiX as the only API route to the
RT core on NVIDIA parts.

## 3. Main mechanism families — the category's spine

**Branch A — software mapping.** Reformulate a general-purpose problem into the
unit's fixed predicate, on shipping hardware, with **no hardware change**:
`../corpus/GPU-ICS24-125--arkade-knn-non-euclidean-gpu-ray-tracing.md` (k-NN
under L1 / L-∞ / cosine) and
`../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md`
(spatial indexing).

**Branch B — hardware generalisation.** Widen the predicate at minimum marginal
area: `../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md`
(three new instructions on an AMD-style datapath) and
`../corpus/GPU-MICRO24-122--tta-generalizing-ray-tracing-accelerators-tree-traversals.md`
(reconfigurable OP-unit network plus a Vulkan API extension, on an NVIDIA-style
RTA).

**Sub-collection Q0 — rendering-pipeline characterisation**, kept **labelled
and separate**: `../corpus/GPU-ASPLOS25-124--treelet-accelerated-ray-tracing-gpus.md`,
`../corpus/GPU-ISCA25-127--cooprt-bvh-traversal-cooperative-threads.md`,
`../corpus/GPU-MICRO24-123--libra-memory-bandwidth-locality-aware-parallel-tile-rendering.md`,
and `../corpus/GPU-HPCA25-126--vr-pipe-streamlining-graphics-pipeline-volume-rendering.md`
(which straddles — it repurposes the stencil MSB as a termination flag, so it
is a member of the ROP branch, while being a rendering paper). These are
graphics for graphics' sake, **but they are kept because the repurposing
papers' central claims are only quantified here** — Treelet's 0.37 SIMT
efficiency and CoopRT's 30–70% idle lanes are the numbers that keep the
repurposing literature honest.

## 4. Representative papers

- **Arkade** (ICS 2024) — **MEASURED** on an **RTX 4060 Ti, OptiX 7.5** (an
  RTX 4070 Ti also in the setup), seven datasets (Gowalla 1.27M … Gbif 8.48M),
  10K queries each, BVH built once, 5-run averages `[paper]`. Against
  **Treelogy** (GPU exact k-d tree): **L1 1.6×–160.9×**, **L-∞ 4.8×–200×**,
  **cosine 2.9×–97×**. But **against FastRNN, the prior RT-core method, the
  margin is 1.3×–33.1× (L1) and 3.2×–15.6× (L-∞)** — an order of magnitude
  less. **The RT core supplies most of the win; Arkade's contribution is the
  non-L2 metric support.** Every figure is a measured wall-clock ratio on the
  named part against the named baseline on the named datasets.
- **LibRTS** (PPoPP 2025) — **MEASURED** on an **RTX 3090, OptiX 8.0, CUDA
  12.3, FP32**, six real geospatial datasets (USCounty 12.2K … OSMParks 11.5M
  polygons) `[paper]`. Point query **74.4×–302.1× over CPU baselines** and up
  to **85.1× over GPU LBVH**; range-contains **1.9×–94.0× over LBVH**;
  range-intersects **≤2.3× at 0.01% selectivity rising to 11.0× at 1.0%**;
  point-in-polygon **1.9× / 1.1× / 3.8×** over RayJoin on the three larger
  datasets. **The cleanest isolation of the RT core anywhere in this corpus:
  LBVH is the same algorithm in software on the same GPU, and the gap to it is
  the fixed-function traversal.** Ray Multicast alone is worth **7.8×** on
  USCensus (k=1 at 24.26 ms vs k=16 at 3.1 ms).
- **HSU** (MICRO 2024) — **SIMULATED**: Accel-Sim with GPGPU-Sim 4.0, an
  **80-SM Volta V100 configuration with 1 RT unit per SM** — i.e. a GPU that in
  reality **has no RT cores at all**; the RT unit is a modelled addition
  `[paper]`. Against that same simulated GPU without HSU: **BVH-NN 33.9%,
  GGNN 24.8% (7.8%–41% by dataset), FLANN 16.4%, B-Tree 13.5%**. The sharpest
  comparison is like-for-like against the previous generation of the same idea:
  an HSU re-implementation of **RTIndeX's B-tree lookup gains 36.6% with a 9:1
  memory advantage** from storing native keys instead of 288-bit triangles.
  Area **+37% of the baseline RT datapath**, dynamic power Euclidean 79 mW /
  Angular 67 mW — **synthesis estimates, not measured silicon**. Artifact
  `github.com/purdue-aalp/rayflex` @ `de9d80c1e1a0a3a1d776f265bfe224b8eea0e183`
  exposes **four** opcodes and **no `KEY_COMPARE` / B-tree opcode** `[code]` —
  whether the RTL predates or omits that mode is **`UNKNOWN`** and must not be
  asserted either way.
- **TTA** (MICRO 2024) — **SIMULATED** in Vulkan-Sim on an **8-SM
  configuration; no real GPU was benchmarked** `[paper]`. Versus CUDA on the
  general-purpose cores: **B-Tree up to 5.4× (geomean 2.4×)**; **B+-Tree only
  ~1.2×**, explicitly because B+-trees have **less divergence to remove**.
- **Treelet Accelerated Ray Tracing** (ASPLOS 2025) — **SIMULATED**,
  Vulkan-Sim, **16-SM scale model**, LumiBench at 256×256 / 1 spp / 3 bounces.
  **95% average speedup (~1.95×), up to 2.55×**, and **43% over the prior
  treelet-prefetching work** `[paper]`. Candid ablation: **naive treelets are
  5% *slower* than baseline.**
- **CoopRT** (ISCA 2025) — **SIMULATED** in Vulkan-sim 2.0 on an
  **`SM75_RTX2060` (Turing, 1st-generation RT cores)** configuration, LumiBench
  16 scenes. **Geomean 2.15×, max 5.11×** — **and power increases 2.02× on
  average**, with EDP improving 2.29× `[paper]`. **The power figure must always
  accompany the speedup**: this design buys performance by activating idle
  hardware.
- **VR-Pipe** (HPCA 2025) — **SIMULATED** in Emerald (gem5 + GPGPU-Sim) on a
  modelled 1-GPC, 16-SIMT-core, 612 MHz GPU with a 2-quads/cycle RGBA16F ROP;
  **two real parts appear in specific, limited roles** (a Jetson AGX Orin in
  30 W mode for frequency and energy measurement, an RTX 3090 for motivation)
  `[paper]`. Hardware early termination alone **1.80× average (1.55–2.04×
  per-scene)**; quad merging alone **up to 1.49×**; together **2.07× average,
  up to 2.78×**; end-to-end **2.05× over software CUDA rendering** and **1.60×
  over the hardware OpenGL baseline**; energy efficiency on AGX Orin **1.65×
  average, up to 2.15×**.
- **LIBRA** (MICRO 2024) — **SIMULATED** in TEAPOT + McPAT + DRAMsim3 on a
  modelled **ARM Valhall-like mobile GPU, 800 MHz, 22 nm, Full HD with 32×32
  tiles**; **no real GPU was measured** `[paper]`. Parallel tile rendering alone
  **13.2% speedup / 5.5% energy**; plus the temperature scheduler and supertiles
  **+7.7% / +3.7%**; total **20.9% (FPS +11.4%, peak 44.5% on Candy Crush
  Saga)** and **9.2% energy (peak 20.5%)**. Convincing negative control: on
  compute-intensive, low-memory-activity games the scheduler contributes only
  **1.7%** of an 11.6% total — exactly as predicted if its mechanism is
  DRAM-demand smoothing. Scaling is **non-monotone** (3 raster units 31.3%,
  4 units 28.8%): the design has a sweet spot.

## 5. Historical lineage

Verified from the papers' own citations
(`../corpus/_LEDGER_fixed_function_repurposing.md` §4.3); wider chains in
`../synthesis/GPU_TOPIC_LINEAGES.md`.

```
Wald et al. 2019 "RTX Beyond Ray Tracing"        <- named by Arkade as the first non-graphics use
   |
Zellmann 2020 (graph drawing) ; Evangelou 2021 (radius search)
   |
RTNN (2022) ; RT-DBSCAN, RT-kNNS Unbound/TrueKNN (2023) ; RTIndeX (2023)
   |                                                \
SOFTWARE BRANCH                                      HARDWARE BRANCH
Arkade (ICS 2024) ------- cited by HSU ----------->  HSU (MICRO 2024, AMD-style datapath)
RayJoin (ICS 2024)                                   TTA/TTA+ (MICRO 2024, NVIDIA-style RTA)
RT-BarnesHut (PPoPP 2025)                                 |
LibRTS (PPoPP 2025) -- cites BOTH MICRO 2024 papers ----->|
RTSpMSpM (ISCA 2025) ; X-HD (ICS 2026)                    |
   \                                                      |
    \-- Heliostat (ISCA 2025): the same move applied to the GPU PAGE TABLE
                                                          |
Q0 RENDERING SUPPORT: Chou treelet prefetcher (MICRO 2023) -> Treelet (ASPLOS 2025)
   CoopRT (ISCA 2025) -> TTP (ISCA 2026) ; RayN (MICRO 2025, RT traversal into HBM logic)
```

**Two lineage findings worth recording precisely:**

- **Heliostat belongs to this line, on three independent attachments**: its
  mechanism is the software branch's move applied to the page table; its
  co-author **Won Woo Ro also co-authors TTA**; and **TTP independently lists
  it beside LibRTS, TTA and Arkade** `[paper, TTP]`. Its *verdict of record*
  correctly sits in `../corpus/_LEDGER_memory_virtualization.md`
  (`CORE_GPU` / `ABSTRACT_ONLY`) — **which is the clearest evidence that
  category Q cross-cuts the existing clusters rather than replacing them.**
- **The RT branch and the rasterisation branch do not cite each other.**
  VR-Pipe cites **no** RT-core repurposing work at all `[paper — verified by
  targeted query]`, and no RT paper read here cites VR-Pipe, RoCC or DEFCON.
  **The category is real in mechanism but not yet self-aware across units.** A
  survey asserting a unified "fixed-function repurposing" community would be
  overstating what the citations support.

## 6. Implementation families

**The HW/SW split is the implementation split, and it is almost perfectly
correlated with the evaluation method** — which is §7's T1. Software-mapping
papers are `REAL_SILICON` (RTX 3090, RTX 4060 Ti) via **OptiX**; hardware
papers are `SIMULATOR` (Accel-Sim/GPGPU-Sim V100, Vulkan-Sim 8–30 SM scale
models, Emerald, TEAPOT) with synthesis-based area and energy. HSU ships RTL
(`rayflex`, Chisel/Scala, verilator 4.038) `[code]`. All simulated area and
power figures in this topic are **never** reported as measured
(`../../../governance/SOURCE_EVIDENCE_RULES.md`).

## 7. Important disagreements / tensions

**T1 — the two branches' headline numbers are systematically non-comparable,
and no table should place them in the same column.** The ledger states this as
a standing caution for whoever writes the synthesis: **the software branch
measures real silicon against SIMT baselines and reports 10×–100×; the hardware
branch simulates against an *already-RT-accelerated* baseline and reports
1.1×–2.5×.** They are not measuring the same thing. This file's §4 shows it
directly: LibRTS reports up to 302.1× (RTX 3090 vs CPU) and 85.1× (vs software
LBVH on the same GPU), while HSU reports 33.9% and TTA 2.4× geomean — both
against a simulated GPU that already has the unit.

**T2 — even the two hardware papers must not be compared to each other.**
**HSU generalises an AMD RDNA3-style datapath where software owns the traversal
stack; TTA generalises an NVIDIA-style RTA where hardware owns it** `[paper,
both]`. Different baseline machine, different mechanism, different simulator.
They are twins in the same MICRO 2024 session 7B with the same thesis, and the
analyses record **no citation link in either direction** — consistent with
same-cycle submission, and stated here as what the corpus records rather than
as a verified non-citation.

**T3 — the category's own value proposition is contested from inside Q0.**
Treelet's ablation finds **naive treelets are 5% slower than baseline**;
CoopRT's speedup comes with a **2.02× power increase**; LIBRA's raster-unit
scaling is **non-monotone**. The rendering papers are the ones quantifying how
much headroom the RT/ROP path actually has, and their numbers are less
flattering than the repurposing papers' are.

**T4 — a software mapping can be beaten by another software mapping more
easily than by hardware.** Arkade's honest disclosure: against SIMT k-d trees
it wins by up to 200×; **against FastRNN, the prior RT-core method, by
1.3×–33.1×** `[paper]`. The unit supplies most of the win in both cases. Any
claim of the form "repurposing the RT core gives N×" must state whether the
baseline was SIMT or another repurposing.

**T5 — a structural parallel that argues for a cross-cutting method axis, not a
merge.** The tensor-core cluster's FlashSparse and Acc-SpMM reshape sparse
algebra to fit the MMA instruction's fixed operand extents **with no hardware
change** — precisely as Arkade and LibRTS reshape search to fit the ray-AABB
predicate. `../corpus/_LEDGER_fixed_function_repurposing.md` §4.2 calls this
"the strongest structural confirmation" that Q is a method, and is explicit
that it is **an argument for a cross-cutting axis, not for merging the two**:
the units, the constraints and the communities differ.

**T6 — the community that would benefit most does not cite this one.**
`../corpus/_LEDGER_sparse_irregular.md` §7.4 verified by targeted full-text
query that SMaT and Ocean contain **none** of "ray tracing", "RT core", "RT
unit", "BVH", "RTSpMSpM" or "LibRTS" — while **RTSpMSpM (ISCA 2025) is sparse
matrix multiplication on the RT unit.**

## 8. Current limitations

**The category's boundary rests partly on papers that could not be read.**
`../corpus/_LEDGER_fixed_function_repurposing.md` §4.4 lists as *in* the
category several works with no deep analysis here — RT-BarnesHut, RTSpMSpM,
X-HD, RoCC, DEFCON, TMModel, Rethinking Collision Detection — and admits
**GauTracer and GRTX only conditionally, "if their baseline is confirmed to be
a GPU RT core"**. Of the eight deep analyses, **six are the Q0 rendering
sub-collection or the hardware branch; only two are software-mapping papers.**
The branch that produces the large numbers is the branch this corpus read
least.

**Bounded by full-text access.** `dl.acm.org` → 403, `ieeexplore.ieee.org`
→ 418, `dblp.org` and `par.nsf.gov` robots-blocked, `arxiv.org/search` and
`web.archive.org` unavailable. Several papers here are **genuinely open access
on ACM DL and unreachable from this environment** — recorded
`PENDING_FULLTEXT`, **not** `CLOSED_ACCESS`
(`../synthesis/GPU_PENDING_FULLTEXT.md`). Specifically, **Heliostat is
`ABSTRACT_ONLY`** — the single most important cross-cutting data point in §5
could not be read.

**Bounded by a deliberate scope decision, not by access**: GSCore, the Gaussian
Blending Unit and the dedicated 3DGS accelerators are **out**, because they
*build* hardware rather than repurpose it. GSCore is kept as the value
contrast — it beats VR-Pipe on performance and loses on generality, **by
VR-Pipe's own admission**. ARC and Interleaved Bitstream Execution are routed
to the SIMT/atomics and sparse clusters as SIMT-pipeline mechanisms in
rendering clothing.

**One artifact-level `UNKNOWN` to preserve**: HSU's released RTL has no
key-compare opcode (§4). The paper describes it as reusing stage-3 comparators
with no new functional units, which is consistent with a control-mode rather
than a datapath variant — **but the artifact does not corroborate it, and
neither reading may be asserted** (`../../../governance/ANTI_HALLUCINATION_RULES.md`).

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. What is the right baseline for a hardware-generalisation paper? T1 says the
   two branches are non-comparable; nothing in the corpus proposes a common
   yardstick, and HSU's RTIndeX re-implementation is the only like-for-like
   comparison anyone ran.
2. Does the ROP/texture branch have an HSU — i.e. a hardware generalisation of
   a non-RT fixed-function unit? The corpus holds software mappings (RoCC,
   DEFCON) and no read hardware counterpart, and the two branches do not cite
   each other (§5).
3. T6 is a directly checkable gap: would the SpGEMM community's
   unknown-output-size problem (see `sparse_irregular.md` §7, T1) yield to an
   RT-unit formulation, given that RTSpMSpM exists and is invisible to them?

## 10. Deeper lookup paths

`../corpus/_LEDGER_fixed_function_repurposing.md` — §1–§3 the three verdict
tables with their `HW/SW` and `S/M` columns, **§4 the taxonomy finding**
(4.1 the evidence, 4.2 why it is not a sub-case of a workload or resource
category, 4.3 the verified lineage and its two findings, 4.4 the recommended
definition with explicit in/out boundaries and the non-comparability caution)
→ the eight analyses above → the pinned artifacts in each §12.8.
Cross-topic: `tensor_cores.md` (the structural parallel, T5),
`memory_virtualization.md` (Heliostat's verdict of record),
`sparse_irregular.md` (the non-citing community, T6),
`multi_gpu_communication.md` (RoCC, the ROP-for-collectives case).

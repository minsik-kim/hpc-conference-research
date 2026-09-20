# GPU-MICRO24-121 — Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — fixed-function GPU units repurposed for general computation (RT unit datapath generalisation)`
secondary_topics: `GPU microarchitecture (ISA extension); nearest-neighbour search / ANN; B-tree key-value lookup; SIMT divergence; RTL artifact (RayFlex)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author-hosted PDF (engineering.purdue.edu/tgrogers/publication/barnes-micro-2024/barnes-micro-2024.pdf) — introduction/motivation, background on the RT-unit datapath and AMD RDNA3 IMAGE_INTERSECT_RAY baseline, Table I instruction set, the 9-stage unified datapath and per-stage functional-unit additions, multi-beat/accumulate operand mechanism, evaluation setup (Accel-Sim + GPGPU-Sim 4.0, V100 config, Table II datasets), Figures 8-13 results and ablations, area/power section VI-K, limitations as stated, related work. PLUS artifact inspection: github.com/purdue-aalp/rayflex @ de9d80c1e1a0a3a1d776f265bfe224b8eea0e183.`

## 12.1 Bibliographic facts

- Title: **Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration** [paper]
- Venue: **MICRO 2024** (57th IEEE/ACM International Symposium on Microarchitecture), session **7B GPU Microarchitecture II** [official-program, census `MICRO_2024.md` row 15]. The author-hosted PDF does not itself print the venue banner; venue is taken from the census/program row and from the artifact `README.md` citation block, which names "2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)" [README].
- Authors and affiliation [paper]: **Aaron Barnes, Fangjia Shen, Timothy G. Rogers** — Elmore Family School of Electrical and Computer Engineering, Purdue University, West Lafayette, IN, USA.
- DOI: `UNKNOWN` (census records only IEEE Xplore document 10764676; `ieeexplore.ieee.org` returns HTTP 418 from this environment).
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: **https://github.com/purdue-aalp/rayflex**, cloned and pinned at commit `de9d80c1e1a0a3a1d776f265bfe224b8eea0e183` [code]. The repository is the **RTL (Chisel) ray-tracer datapath**, not the Accel-Sim model; its `README.md` asks users to cite both this MICRO 2024 paper and a follow-on ISPASS 2025 paper "RayFlex: An Open-Source RTL Implementation of the Hardware Ray Tracer Datapath" (Shen, Barnes, Nallathambi, Rogers) [README].
- Proposed unit name: **HSU — Hierarchical Search Unit** [paper].

## 12.2 Core question (one sentence)

If the GPU ray-tracing unit's value is not "ray tracing" but a **fixed-function, divergence-tolerant datapath that resolves one level of a spatial hierarchy per instruction**, can that datapath be widened with a handful of extra adders so the *same* unit also answers Euclidean-distance, angular-distance and key-comparison queries — turning it into a general **hierarchical search** engine rather than a graphics unit that general-purpose programmers must lie to?

## 12.3 GPU/HPC problem translation

- **Compute.** The RT unit already performs, per instruction, either one ray-triangle intersection or up to **four ray-box intersections** [paper, baseline from the AMD RDNA3 ISA's single `IMAGE_INTERSECT_RAY` instruction]. That is a CISC-scale amount of arithmetic per instruction issue. The paper's observation is that "the search-and-compute software pattern is not limited to ray tracing applications" [paper], so the same per-instruction density can serve k-d trees, hierarchical ANN graphs and B-trees.
- **Memory.** HSU instructions are memory-hungry: the paper reports HSU distance instructions "tend to miss L1 cache", and that the CISC nature of the instruction *reduces* L1D accesses by coalescing what would otherwise be many scalar loads (most prominent in BVH-NN) [paper, Figure 12].
- **Synchronization.** None added at the warp level; the unit is accessed through an **8-entry warp buffer** and a round-robin arbiter for multi-beat instructions [paper].
- **Scheduling.** Multi-beat: for a point dimensionality `n` larger than the pipeline width, the compiler emits `ceil(n/16)` Euclidean instructions and a **round-robin arbiter enforces sequential scheduling** of the beats, with an `accumulate` operand carrying the running sum [paper].
- **Communication.** Single-GPU, single-SM-local unit (1 RT/HSU unit per SM). `NOT_IN_PAPER` for multi-GPU.

## 12.4 Why the problem exists (hardware root cause)

Three root causes, all named by the paper [paper]:

1. **Access is gated by a graphics API.** RT units are "mired by a highly specialized graphics API", so a CUDA programmer cannot reach them without reformulating the problem as ray casting. The paper draws the explicit analogy to **pre-CUDA GPGPU**, where scientists had to express computation as texture-mapped triangles.
2. **The fixed-function datapath is shaped for one geometry.** A ray-box test is a *slab* intersection; a ray-triangle test is a *watertight* edge-equation test. Neither computes `sum (q_i - c_i)^2` over an arbitrary dimensionality, and neither compares an integer key against a separator array. Prior repurposing work therefore had to **encode non-geometric data as geometry** — the paper's most concrete example is RTIndeX, which represents 32/64-bit integer keys as **288-bit triangle primitives**, a 9:1 storage blow-up the paper measures against [paper].
3. **SIMT cores are the wrong substrate for the search half.** The value of the RT unit is that it gives "high throughput in thread-divergent workloads" and completes a whole intersection test "in a single instruction" [paper]; a SIMT reimplementation reintroduces the divergence.

## 12.5 Mathematical / performance model

- **Euclidean mode** [paper, Eq. 1]: `d^2(q,c) = sum_i (q_i - c_i)^2`, evaluated **16-wide** per instruction (`POINT_EUCLID`). For dimensionality `n`, `ceil(n/16)` beats with an accumulate operand.
- **Angular mode** (`POINT_ANGULAR`) [paper]: **8-wide**; returns a **dot-product sum** and a **squared-norm sum** so that `cos(theta)` is completed in software afterwards. The unit deliberately does **not** do the division/reciprocal.
- **Key-compare mode** (`KEY_COMPARE`) [paper]: compares a query key against up to **36 separator values** of a B-tree internal node and returns a **bit vector**.
- **Baseline mode** (`RAY_INTERSECT`) [paper]: one ray-triangle **or** four ray-box tests.
- The pipeline widths (16 for Euclidean, 8 for Angular) are not arbitrary: they are "selected for maximal functional unit reuse" against the existing ray-triangle/ray-box multipliers and adders [paper].

## 12.6 Data layout and ownership

- **thread → warp**: a warp issues an HSU instruction; per-ray/per-query state lives in an **8-entry warp buffer** inside the unit [paper].
- **unit → SM**: **1 RT/HSU unit per SM**, in an **80-SM Volta V100-like configuration with 4 sub-cores per SM** [paper, simulator config].
- **data structure ownership**: the four structures HSU targets [paper] are **B-trees** (key-value stores), **BVHs** (3D ray tracing), **k-d trees** (N-dimensional point search) and **hierarchical graphs** (high-dimension ANN). Crucially the *points are stored natively* — HSU's 9:1 memory advantage over RTIndeX comes from storing an integer key as an integer rather than as a 288-bit triangle [paper].
- **GPU → node → cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- baseline RT unit (AMD RDNA3-style), as the paper describes it ----  [paper]
RAY_INTERSECT(ray, node_ptr) -> {hit, prim_id, t}      # 1 ray-triangle OR 4 ray-box

# ---- HSU additions, Table I ----                                        [paper]
POINT_EUCLID(q[0:16], c[0:16], accum) -> partial_sum   # 16-wide  sum (q_i-c_i)^2
POINT_ANGULAR(q[0:8],  c[0:8],  accum) -> (dot_sum, norm_sum)   # 8-wide
KEY_COMPARE(key, separators[0:36])     -> bitvector    # B-tree internal node

# ---- multi-beat for n-dimensional points ----                           [paper]
acc = 0
for beat in range(ceil(n/16)):                          # compiler-generated
    acc = POINT_EUCLID(q[16*beat : 16*beat+16],
                       c[16*beat : 16*beat+16], acc)    # round-robin arbitered
d2 = acc
```

`ceil(n/16)`, the `accum` operand and the round-robin arbiter are the paper's [paper]; the loop skeleton is `[reconstruction]`.

## 12.8 Real implementation

The artifact `github.com/purdue-aalp/rayflex` @ `de9d80c1e1a0a3a1d776f265bfe224b8eea0e183` is a **Chisel/Scala RTL** implementation of the datapath, tested with **verilator 4.038** and **sbt 1.8 / mill 0.10.12** [README]. Real symbols read from the tree [code]:

- `src/main/scala/raytracer_datapath/UnifiedDatapath.scala` — `class UnifiedDatapath(p: RaytracerParams) extends Module`, with `val _max_stage_count = 12`, `val _box_plurality`, `_rounding_rule = consts.round_near_even`, `_tininess_rule = consts.tininess_beforeRounding`, and a `stage_functions` array of per-stage closures. Functional units instantiated per stage include `AddRecFN(8,24)`, `MulRecFN(8,24)`, `CompareRecFN(8,24)` (a `Seq.fill(4)` comparator list) and `QuadSortRecFN`.
- `src/main/scala/raytracer_datapath/IOSpec.scala` — `object UnifiedDatapathOpCode extends ChiselEnum` with exactly four values: **`OpTriangle`, `OpQuadbox`, `OpEuclidean`, `OpAngular`**. Bundles: `class Ray`, `class AABB`, `class Triangle`, `class RayBoxPair`, `class CombinedRayBoxTriangleBundle` (carrying `val opcode = UnifiedDatapathOpCode()`), `class ExtendedPipelineBundle`, `class AngularJobBundle`.
- `src/test/scala/raytracer_datapath/raytracer_gold/SW_Data.scala` — `object SW_Opcode extends Enumeration` with `SW_OpTriangle = Value(0)`, `SW_OpQuadbox = Value(1)`, `SW_OpEuclidean = Value(2)`, `SW_OpAngular = Value(3)`; generators `get_euclidean_job_seq_from_vec_pair`, `get_angular_job_seq_from_vec_pair`.
- Datapath outputs observed in the testbench: `euclidean_accumulator`, `euclidean_reset_accum`, `angular_dot_product`, `angular_norm` [code, `Datapath_test.scala`].

**Finding worth recording**: the public RTL exposes **four** opcodes. There is **no `KEY_COMPARE` / B-tree opcode in the released RTL** [code — verified by enumerating `UnifiedDatapathOpCode` and `SW_Opcode`]. The paper describes key-compare mode as reusing the stage-3 ray-box comparators with **no new functional units** [paper], which is consistent with it being a control-mode rather than a datapath variant, but the artifact does not corroborate it. Whether the shipped RTL simply predates or omits that mode is `UNKNOWN`; it must not be asserted either way.

Note also the *naming discrepancy to respect*: the paper's Table I instruction names are `RAY_INTERSECT` / `POINT_EUCLID` / `POINT_ANGULAR` / `KEY_COMPARE` [paper]; the RTL's opcode names are `OpTriangle` / `OpQuadbox` / `OpEuclidean` / `OpAngular` [code]. Do not merge the two vocabularies.

## 12.9 Kernel execution

kernel → thread block → warp → **HSU instruction**. The interesting level is the instruction: a single HSU instruction replaces what on SIMT cores is a loop of loads, subtracts, multiplies and a reduction. For dimensionality above the pipeline width, the *compiler* — not the hardware — emits the beat sequence, and the unit's round-robin arbiter serialises beats from different warps [paper]. Programmers reach the unit through "a CUDA library providing optimized algorithms and data structures that make use of the HSU hardware" [paper], i.e. the intended interface is a library, not raw intrinsics.

## 12.10 Memory traffic

- **L1D**: reduced by CISC coalescing — one HSU instruction fetches operands that would otherwise be many separate loads; the effect is "most prominent in BVH-NN" [paper, Figure 12].
- **L1/L2 miss behaviour is dimensionality-dependent**: "high-dimension applications exhibit high L1/L2 miss rates; lower-dimension applications have better cache utilization" [paper, Figure 13].
- **Warp-buffer pressure**: buffers larger than 8 entries "can reduce L1 hit rates for non-HSU instructions by saturating MSHR" [paper, Figure 11] — i.e. the unit competes with the SM's own memory path.
- HBM/DRAM breakdown: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Speedups, **all simulated on an Accel-Sim/GPGPU-Sim 4.0 Volta V100 configuration (80 SMs, 4 sub-cores/SM, 1 RT unit/SM, 8-entry warp buffer)**, versus the same simulated GPU without HSU [paper, Figure 9]:

| Application | Structure | Speedup (avg) |
|---|---|---|
| **BVH-NN** (custom, based on RTNN) | binary BVH | **33.9%** |
| **GGNN** | hierarchical ANN graph, 65–960 dims | **24.8%** (7.8%–41% by dataset) |
| **FLANN** | k-d tree (LBVH used in evaluation) | **16.4%** |
| **B-Tree** (Rodinia) | B-tree, 1M and 10K keys | **13.5%** |

The ordering is itself the causal story: gain tracks **the fraction of the kernel that the new instructions absorb**. BVH-NN is highest because ray-box tests dominate it; B-Tree is lowest because key-compare "reuses comparators with minimal instruction reduction benefit" [paper].

Separate, and the sharpest comparison in the paper: an **HSU re-implementation of RTIndeX's B-tree key-value lookup achieves 36.6% speedup over the baseline RT unit**, with a **9:1 memory advantage** from storing native keys instead of 288-bit triangle primitives [paper]. That is a like-for-like measurement against the *previous generation of this very idea* (encode-as-geometry), not against SIMT.

Dataset-level evidence that the mechanism, not the benchmark, explains the gain [paper]: Glove200 (angular) ~40% with GGNN; SIFT1M (Euclidean) ~32% with BVH-NN; **Deep1B (96D) only 7.8%, because the kernel becomes memory-bound once HSU removes the arithmetic**.

**Area and power — SIMULATED/SYNTHESISED, NOT MEASURED** [paper, §VI-K]: total datapath area increase **37% of the baseline RT datapath**, with the paper's own qualifier that "the datapath is a small fraction of the entire RT unit". Dynamic power: Ray-Box **+10 mW**, Ray-Triangle **+8 mW**; Euclidean **79 mW**, Angular **67 mW** (the latter "only 5 mW more than ray-box baseline"). Per-stage additions are small: **two extra adders in stage 3; one each in stages 5, 8 and 9** [paper].

## 12.12 Hardware generation dependence

- **The baseline RT-unit model is AMD RDNA3**, cited via its ISA's single `IMAGE_INTERSECT_RAY` instruction, in which **software manages the traversal stack** [paper]. This must not be conflated with NVIDIA RT cores, where traversal-stack management is in hardware and the ISA is undocumented. This is a genuine and load-bearing distinction for this cluster: HSU's premise (a register-file-fed, software-stack datapath with one CISC instruction) is the **AMD ray-accelerator** model, whereas Heliostat, TTA and Treelet are built on the NVIDIA-style hardware-state-machine RTA model.
- **The simulated GPU is a Volta V100 configuration in Accel-Sim/GPGPU-Sim 4.0** [paper] — i.e. a GPU that in reality has **no RT cores at all**. The RT unit is a modelled addition. Do not report this as a Turing/Ampere/Ada/Blackwell RT-core result.
- **No real GPU is executed.** Simulation only [paper].
- Generation-specific RT features (SER, OMM/DMM, Ada 3rd-gen, Blackwell 4th-gen) are not involved. `NOT_IN_PAPER`.

## 12.13 Limitations

Stated or directly supported by the paper [paper]:
1. **Nothing becomes compute-bound.** Roofline analysis (Figure 8) shows no workload reaches full HSU utilisation; kernels stay memory-bound or priority-queue-bound.
2. **The BVH-NN case under-uses the hardware**: binary trees exercise only one of the four ray-box lanes.
3. **k-d trees are deliberately not accelerated** in the split-plane comparison: "Due to its poor computational density we chose not to accelerate this portion."
4. **B-tree gain is structurally small** — comparator reuse yields little instruction reduction.
5. **Priority-queue management in GGNN is not accelerated** and its cost "is highly dependent upon application search parameters".
6. **Memory interference**: HSU distance instructions miss L1, and large warp buffers degrade non-HSU instructions.
7. **Programmability is improved but not solved** — a CUDA library or manual intrinsics are still required.
- `[inference]` The RTL artifact's missing key-compare opcode means the B-tree mode's hardware cost is the least independently corroborated part of the design.
- `[inference]` Because the baseline is AMD-style (software stack), the *stack-management* advantage that NVIDIA-style RTAs supply is outside HSU's scope; TTA (`GPU-MICRO24-122`) addresses exactly that and reaches much larger B-tree speedups.

## 12.14 Relation to prior corpus

- **Twin paper, same session**: `GPU-MICRO24-122` (TTA, Ha et al.) — same MICRO 2024 session 7B, same thesis ("generalise the RT unit"), different baseline (NVIDIA-style RTA with hardware stack vs AMD-style datapath) and different mechanism (reconfigurable OP units and a programming interface vs new fixed instructions). These two are the **root of category Q's hardware branch** and cite the same software-repurposing lineage.
- **Cited downstream by** `GPU-ASPLOS25-124` (Treelet Accelerated Ray Tracing), which names "Barnes et al. [6]" alongside "Ha et al. [14]" as the works that "extend ray tracing accelerators in GPUs to support more general tree traversal workloads" [paper, Treelet conclusion]. This is verified forward lineage within the corpus.
- **Supersedes-by-measurement**: the software-mapping line (RTNN, RTIndeX, RT-DBSCAN, Arkade = `GPU-ICS24-125`). HSU measures itself against an RTIndeX re-implementation and wins 36.6% with a 9:1 memory advantage [paper].
- **Complementary, cross-cluster**: Heliostat (ISCA 2025, page-table walks on the RT accelerator), adjudicated `CORE_GPU`/`ABSTRACT_ONLY` in `_LEDGER_memory_virtualization.md`. Heliostat is the same idea applied to a *system* structure (the page table) rather than an application data structure; HSU/TTA's existence is what makes that credible.
- **Contrast within the corpus**: the tensor-core cluster (`GPU-PPoPP25-01`, `GPU-PPoPP25-02`, `GPU-PPoPP26-01`) repurposes a *dense arithmetic* fixed-function unit by algebraic reshaping and proposes **no hardware change**; HSU repurposes an *irregular-traversal* fixed-function unit and **does** propose a hardware change. The pair is the clearest evidence that "repurposing a fixed-function unit" is a method, not a topic.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT unit were replaced by ordinary SIMT cores?** No. The paper's own framing is that the RT unit supplies two things SIMT cores do not: (a) **high throughput under thread divergence**, and (b) **a fixed-function datapath that completes an entire ray-box or ray-triangle test in one instruction** [paper]. HSU's additions are explicitly *reuses* of that datapath's existing multipliers, adders and comparators — the 16-wide Euclidean and 8-wide Angular widths were chosen "for maximal functional unit reuse", and key-compare adds **no new functional units at all** [paper]. On SIMT cores the same arithmetic is available but the instruction density, the divergence tolerance and the near-zero marginal area (2 adders in stage 3, 1 each in stages 5/8/9) all vanish; there is no contribution left.

**Hardware change or software mapping?** **HARDWARE CHANGE** — three new instructions and per-stage functional-unit additions to the RT datapath, with an RTL artifact.

**Simulated or measured?** **SIMULATED** — Accel-Sim with GPGPU-Sim 4.0, Volta V100 configuration, 80 SMs, 1 RT unit/SM. Area and power are synthesis/model estimates, **not measured silicon**. No real GPU was executed.

verdict_basis: The contribution is a datapath extension to the GPU ray-tracing unit, evaluated as a modelled RT unit inside an Accel-Sim GPU, and its economy depends entirely on reusing the RT datapath's existing floating-point functional units. Neither the mechanism nor its cost argument exists outside a GPU RT unit.

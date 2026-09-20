# GPU-PPoPP25-128 — LibRTS: A Spatial Indexing Library by Ray Tracing

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — fixed-function GPU units repurposed for general computation (software mapping onto shipping RT cores)`
secondary_topics: `spatial indexing / spatial databases; BVH as a mutable index; load balancing on OptiX; point-in-polygon; OptiX instancing (GAS/IAS)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author-hosted PDF (gengl.me/public/publications/ppopp25.pdf) — introduction/motivation, background on rays/AABB/BVH/GAS/IAS/OptiX shader model and BVH refitting, the three query mappings including Theorem 1 and the diagonal encoding, Ray Multicast and its cost model, the mutability design (insertion via IAS, deletion via degenerate AABBs), evaluation setup with CPU and GPU baselines and six real datasets, §6.5 ablation on k, update-sensitivity study, point-in-polygon application, related work. PLUS artifact inspection: github.com/RTSpatial/RTSpatial @ 52509e8022abeab722f5a9a89d1917e8b481defe.`

## 12.1 Bibliographic facts

- Title: **LibRTS: A Spatial Indexing Library by Ray Tracing** [paper]
- Venue: **PPoPP '25** — 30th Symposium on Principles and Practice of Parallel Programming, **March 1–5, 2025, Las Vegas, NV** [paper, printed on the PDF]. Session **S9 Concurrent Data Structures and Synchronization II** [official-program, census `PPoPP_2025.md` row 19].
- Authors and affiliations [paper]: **Liang Geng** (The Ohio State University), **Rubao Lee** (Freelance, Columbus, Ohio), **Xiaodong Zhang** (The Ohio State University).
- DOI: **`10.1145/3710848.3710850`** [official-web, from search results].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: **https://github.com/RTSpatial/RTSpatial**, cloned and pinned at commit `52509e8022abeab722f5a9a89d1917e8b481defe` [code].

## 12.2 Core question (one sentence)

Every prior RT-core repurposing result is a one-off reduction that "requires carefully adapting the original problem into an RT workload" and expertise in two domains at once — so can a **general, mutable spatial index library** be built on the RT core, supporting point, range-contains and range-intersects queries plus insert/update/delete, so that application programmers get the hardware's benefit without ever writing a shader?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's premise is stated as two facts [paper]: "(1) The BVH accelerated by RT cores serves as a fast spatial index" and "(2) spatial workloads naturally resemble rendering tasks, as both operate on 2D/3D geometric data." Spatial indexing is the *least* contorted of all the repurposings in this cluster — the data really is geometry.
- **Memory.** The index *is* the BVH, built and owned by OptiX. Nothing is duplicated.
- **Synchronization.** OptiX's programming model forbids the usual tools: "the unavailability of shared memory and block synchronization instructions", and it is "a single-ray programming model, where the shaders are executed on a single thread for each ray" [paper]. Every design decision downstream is shaped by that constraint.
- **Scheduling.** The single-ray model creates the paper's hardest problem — **load imbalance** under skewed geometric distributions, where some threads hit thousands of primitives and others none. The answer is **Ray Multicast** (§12.5).
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

The constraints the RT core imposes, all stated by the paper [paper]:

- **Only one predicate exists**: ray-AABB intersection, with two valid cases — origin outside and the ray crossing a boundary with `t_min <= t_hit <= t_max`, **or origin inside the AABB regardless of whether the ray crosses it**. That second case is the hinge of the whole design: it is what lets a *point* be tested for containment.
- **The BVH is nearly immutable**: "OptiX allows the user to update the coordinates of primitives in a constructed BVH, called BVH refitting", and "updating a BVH is up to three times faster than rebuilding" — but **"inserting or deleting from a BVH is not supported"** [paper]. A database index that cannot be inserted into is not an index; this is the gap LibRTS has to engineer around.
- **The shader model is single-ray, with no shared memory and no block synchronisation** [paper] — so classic GPU load-balancing (persistent threads, work queues in shared memory) is unavailable.
- **RT cores arrived with Turing** and "the ray-primitive performance has doubled with each new generation of GPUs" [paper] — the paper's stated reason the approach gets better over time rather than worse.

## 12.5 Mathematical / performance model

**Mapping 1 — Point query.** `Contains(r, p)` iff `x_min <= x <= x_max AND y_min <= y <= y_max`. Encode each query point as a **short ray with origin at the point, arbitrary direction, `t_min = 0`, `t_max = FLT_MIN`** [paper]. The near-zero extent means only "origin inside the AABB" can produce a hit, minimising the false positives that case 1 would generate; the **IsIntersection shader** then evaluates `Contains` explicitly to filter any that remain.

**Mapping 2 — Range-contains.** `Contains(r1, r2)` requires full containment. **Reduction**: "if `Contains(r, s)` is true, then the center point `s_c` of rectangle `s` must also lie within `r`" — so cast rays from rectangle **centres** (a point query) and filter candidates with the full predicate [paper].

**Mapping 3 — Range-intersects (the paper's sharpest idea).** **Theorem 1** [paper]: "if `Intersects(r1, r2)` is true, then either the diagonal of `r2` intersects `r1`, or the anti-diagonal of `r1` intersects `r2`, or both." A diagonal runs `(x_min, y_max) → (x_max, y_min)`; the anti-diagonal runs `(x_min, y_min) → (x_max, y_max)`. A line **segment** is then encoded exactly as a ray by setting **origin `O = p1`, direction `d = p2 − p1`, `t_min = 0`, `t_max = 1`**, so `R(0) = p1` and `R(1) = p2` [paper]. Two passes — **forward casting** (diagonals of the query set into the BVH of the indexed set) and **backward casting** (anti-diagonals of the indexed set into the BVH of the query set) — with **deduplication** by checking whether the anti-diagonal of `R` intersects `S`, in which case the pair is kept only from the forward pass. Complexity **O(|R|·log|S| + |S|·log|R|)**.

**Load balancing — Ray Multicast.** Split `N` primitives into `k` sets placed in **non-overlapping sub-spaces** (e.g. x-ranges `[0,1)`, `[1,2)`, `[2,3)`), and duplicate each ray into `k` rays with matching x-offsets; each ray then meets at most `|N|/k` primitives [paper]. Cost model [paper]:

```
C = (1 - w) * C_R + w * C_I
C_R = |R| * k * log(|N|)        # ray casting cost, grows with k
C_I = |N| * |R| * s / k         # intersection cost, shrinks with k;  s = selectivity
```

`s` is estimated by sampling; the optimal `k` is found by exhaustive search over powers of two (powers of two for warp efficiency) [paper].

**Mutability.** Insertion uses OptiX **instancing**: new geometries go into separate **GAS**es, an **IAS** links them with identity SRT matrices, and only the lightweight IAS is rebuilt; a global primitive index is recovered in O(1) from a prefix-sum array plus `optixGetInstanceId` [paper]. Update uses **refitting**. **Deletion** is done by making the AABB degenerate — "we set the `x_min` and `x_max` of AABBs to the same value" — then refitting, so the rectangle can no longer be hit [paper].

## 12.6 Data layout and ownership

- **rectangle/polygon → AABB → BVH leaf**; **GAS** = per-batch BVH; **IAS** = the instance structure linking GASes with SRT matrices [paper].
- **query point → short ray (`t_max = FLT_MIN`)**; **query rectangle → diagonal ray (`t_max = 1`)** [paper].
- **primitive → global index**: prefix-sum array `A[i] = A[i-1] + I` plus `optixGetInstanceId` [paper].
- **k sub-spaces → x-coordinate ranges**: the multicast partition is literally a translation in the coordinate system, exploiting that the BVH indexes whatever coordinates it is given [paper].
- **Precision**: **FP32**, "due to limited FP64 units in RTX GPUs" [paper]. The artifact's own TODO list corroborates this as unfinished work: "Test and validate double-precision computations" [code, `README.md`].
- **node → cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- point query ----                                               [paper]
ray = Ray(origin = p, direction = arbitrary, t_min = 0, t_max = FLT_MIN)
optixTrace(ray)                       # RT core: BVH traversal + ray-AABB test
# IsIntersection shader:
    if Contains(rect, p): report()    # filters the "origin outside" case

# ---- range-intersects, two passes (Theorem 1) ----                  [paper]
forward:  for s in S: cast_ray(origin = s.diagonal_start,
                               dir = s.diagonal_end - s.diagonal_start,
                               t_min = 0, t_max = 1)  into BVH(R)
backward: for r in R: cast_ray(along r.anti_diagonal, t_min = 0, t_max = 1) into BVH(S)
dedup:    keep a backward hit only if r's anti-diagonal does NOT intersect s

# ---- ray multicast ----                                             [paper]
place primitive set N_j in sub-space x in [j, j+1)      for j = 0..k-1
for each query ray R: emit R_0..R_{k-1} with x-offsets 0..k-1
choose k = argmin (1-w)*|R|*k*log|N| + w*|N|*|R|*s/k    # s by sampling, k a power of 2

# ---- mutation ----                                                  [paper]
insert: new batch -> new GAS ; rebuild IAS only (identity SRT)
update: refit BVH with new coordinates
delete: set AABB x_min = x_max (degenerate) ; refit
```

`FLT_MIN`, `t_max = 1`, Theorem 1, Ray Multicast, the cost model, `optixGetInstanceId`, GAS/IAS and the degenerate-AABB deletion are the paper's [paper]; `optixTrace` and the loop spelling are `[reconstruction]` — the paper's shader vocabulary is RG / IS / AH / CH / MS.

## 12.8 Real implementation

Artifact `github.com/RTSpatial/RTSpatial` @ `52509e8022abeab722f5a9a89d1917e8b481defe` [code]. Verified facts from the tree:

- **Dependencies, stated in `README.md`** [code]: **CMake 3.27+**, **NVIDIA OptiX 8.0**, **NVIDIA CUDA 12+**, **NVIDIA Driver 535+**; gflags for the example, googletest for unit tests. Linux only. These corroborate the paper's OptiX 8.0 / CUDA 12.3 setup.
- **Layout** [code]: `include/rtspatial/` with `rtspatial.h`, `spatial_index.cuh`, and subdirectories `default_handlers/`, `details/`, `geom/`, `utils/`; `examples/spatial_index.cu` and `wkt_loader.h`; `cmake/FindOptiX.cmake` and `cmake/nvcuda_compile_module.cmake` (the OptiX shader-module compile rule); `dataset/box/` and `dataset/point/` with `uniform_1000.wkt` and `gaussian_1000.wkt`; `expr/run_synthetic.sh`.
- **The `README.md` abstract matches the paper's** and states the same headline numbers: "speedups of up to 85.1x for point queries, 94.0x for range-contains queries, and 11.0x for range-intersects queries… point-in-polygon testing, LibRTS also surpasses the state-of-the-art RT method by up to 3.8x" [README].
- **The artifact's own TODO list is a limitations disclosure** [code, `README.md`]: "Add support for 3D geometries", "Implement line-box intersection queries", "Test and validate double-precision computations", "Optimize query performance under high update loads". **The first item means the shipped library is 2D**, and the last corroborates the paper's update-sensitivity finding. None of the paper's 3D claims should be read onto this code.

No function-level symbols beyond the file names above are asserted; the headers were not opened.

## 12.9 Kernel execution

OptiX launch → **RayGen (RG)** shader ("the entry point of an RT program, where rays are cast, transferring the control from SMs to RT cores") → hardware BVH traversal → **IsIntersection (IS)** ("invoked if a ray potentially hits an AABB"), with **AnyHit (AH)**, **ClosestHit (CH)** and **Miss (MS)** as the other callbacks [paper]. The sentence "transferring the control from SMs to RT cores" is the cleanest statement in this whole cluster of what the software-mapping branch is doing: the SM *hands off* the traversal and gets called back.

Note the execution-level consequence of the single-ray model: because there is no shared memory and no block sync in a shader, the library cannot balance load *inside* the traversal. Ray Multicast balances it *before* the traversal, by changing the geometry. That is a distinctly RT-shaped solution.

## 12.10 Memory traffic

`NOT_IN_PAPER` at the cache level. Indirect evidence the paper does supply [paper]:
- **LBVH (a software-emulated linear BVH on the same GPU, used specifically to isolate the RT cores' contribution) "underperforms Boost on large datasets due to poor cache behavior under heavy BVH traversal"** — i.e. the RT core's advantage is partly a memory-system advantage, not only an arithmetic one. This LBVH control is methodologically the most valuable thing in the paper for this cluster, because it separates "BVH is a good index" from "the RT core is good at walking a BVH".
- Memory footprint is discussed only via a failure: **EUParks had to be subsetted** because RayJoin exhausted memory [paper].

## 12.11 Why it is faster/slower (decomposed cause)

All results are **measured on real hardware**: **NVIDIA RTX 3090** with **OptiX 8.0** and **CUDA 12.3**, FP32; CPU baselines on a server with **two AMD EPYC 7713 (128 cores total)** [paper].

Datasets, real geospatial data from ArcGIS Hub and OpenStreetMap converted to bounding rectangles [paper]: USCounty 12.2K, USCensus 248.9K, USWater 463.6K, EUParks 1.9M (subset), OSMLakes 8.3M, OSMParks 11.5M polygons; plus Spider-generated synthetic data for scalability.

Baselines [paper] — **CPU**: Boost (R-tree), CGAL (k-d tree), ParGeo (multicore k-d tree), GLIN (learned index). **GPU**: **LBVH** (software-emulated linear BVH — the RT-core isolation control), cuSpatial (octree), **RayJoin** (the state-of-the-art RT-core spatial-join method, the authors' own prior work).

| Query | Best result | Against |
|---|---|---|
| Point | **74.4x–302.1x** | CPU baselines (best CPU: Boost R-tree) |
| Point | up to **85.1x** | GPU LBVH (OSMLakes) |
| Range-contains | **1.9x–94.0x** | GPU LBVH (peak on OSMParks) |
| Range-intersects, 0.01% selectivity | <= **2.3x** | Boost |
| Range-intersects, 0.1% | up to **6.8x** | best baseline (USWater) |
| Range-intersects, 1.0% | up to **11.0x** | best baseline (USCensus) |
| Point-in-polygon | **1.9x, 1.1x, 3.8x** | RayJoin, on the three larger datasets |

**Every number carries its qualifier: RTX 3090, OptiX 8.0, CUDA 12.3, FP32, the named dataset, the named baseline, index construction excluded except for range-intersects.**

Decomposed causes:
1. **The RT core, not the BVH.** LibRTS beats **LBVH — the same algorithm in software on the same GPU — by up to 85.1x / 94.0x**. That gap is the RT core's fixed-function traversal and ray-AABB throughput, isolated.
2. **Ray Multicast is the second-largest single factor** [paper, §6.5]: on USCensus, **k=1 takes 24.26 ms and k=16 takes 3.1 ms — a 7.8x speedup from load balancing alone**. The cost model's predicted `k` "closely match[es] empirically optimal k" at **<1% prediction overhead**.
3. **Selectivity governs range-intersects**: the advantage widens from <=2.3x at 0.01% to 11.0x at 1.0%, because the two-pass ray-casting overhead is amortised over more real work.
4. **Against RayJoin, the win is a representation win**, not a hardware win: RayJoin spends **98.7% of its runtime building the BVH** because it expands polygons into line segments, while LibRTS indexes bounding boxes [paper]. RayJoin is faster on the small USCounty dataset.

Mutation performance [paper]: index construction **3.7–4.5x faster than LBVH** on large datasets; **1.4M inserts/second** (1K batch); **49.5M deletes/second** (1K batch) — deletion is two orders of magnitude cheaper than insertion because it is a refit of a degenerate box, not a new GAS.

Time breakdown for range-intersects (50K queries, 0.1% selectivity) [paper]: backward cast ~60–80%, forward cast ~10–20%, BVH build ~5–10%, k prediction <1%.

## 12.12 Hardware generation dependence

- **Measured on NVIDIA RTX 3090 (Ampere, 2nd-generation RT cores)** with **OptiX 8.0**, **CUDA 12.3**, **FP32** [paper]. The artifact independently requires **OptiX 8.0, CUDA 12+, driver 535+** [code].
- The paper notes RT cores began with **Turing** and that "the ray-primitive performance has doubled with each new generation" [paper] — an argument that the approach scales forward, but **no Ada or Blackwell part is measured**. `NOT_IN_PAPER`.
- **FP32 only**, "due to limited FP64 units in RTX GPUs" [paper]; the artifact lists FP64 validation as unfinished [code]. For a spatial database this is a correctness-relevant constraint, not a performance footnote.
- **No AMD ray accelerator.** `NOT_IN_PAPER`.
- **The shipped library is 2D** [code, TODO: "Add support for 3D geometries"]. The paper's mappings are presented in 2D (diagonals of rectangles).
- **OptiX opacity is total**: "Cannot disable hardware acceleration for direct comparison" — hence the LBVH software proxy [paper].

## 12.13 Limitations

Acknowledged in the paper, though not under a limitations heading [paper]:
1. **BVH quality degrades under refitting**; update ratios above 0.2% may need a full rebuild. Measured: at **0.02%** updates, point query slows **44%**, range-contains **39%**, range-intersects **3%**; at **0.2%**, point/range-contains slow **2.3–2.4x**; beyond 2–20% there is no further degradation because traversal already dominates.
2. **FP32 only.**
3. **OptiX cannot be told to bypass the RT cores**, so the isolation control is a software LBVH proxy rather than the same code on the same path.
4. **Range-intersects is the expensive case** — two passes, 2x ray-casting cost.
5. **Dataset subsetting** was needed for the RayJoin comparison (memory exhaustion).
6. **Generality has a boundary the paper states honestly**: spatial workloads benefit most, and "non-spatial data requires encoding into 3D primitives, incurring additional computational and storage overhead" — which is precisely the RTIndeX-style cost that `GPU-MICRO24-121` (HSU) measures at 9:1.
- `[inference]` Ray Multicast's `k` is chosen per query batch from a sampled selectivity estimate; adversarial or rapidly shifting distributions would defeat the estimate, and no such study was located.

## 12.14 Relation to prior corpus

- **This is the "library" milestone of category Q's software branch** — the point at which RT-core repurposing stops being a per-paper reduction and becomes reusable infrastructure with mutation support. `GPU-ICS24-125` (Arkade) generalises across *metrics*; LibRTS generalises across *queries and updates*.
- **Verified citation lineage — LibRTS cites both MICRO 2024 hardware papers** [paper, related work]: "Ha et al. [25] … Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs, MICRO 2024" (= `GPU-MICRO24-122`, TTA) and "Barnes et al. [7] … Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration, MICRO 2024" (= `GPU-MICRO24-121`, HSU), positioning them as **complementary hardware research** while LibRTS works within current hardware. **This is the cleanest single piece of evidence that the software branch and the hardware branch of category Q see themselves as one line.**
- **LibRTS's related work is the fullest genealogy of the software branch found in this pass** [paper]: neighbour search — Evangelou et al., **RTNN**, **TrueKNN**, **JUNO**, **Arkade** (= `GPU-ICS24-125`); databases — **RTIndeX**, **RTScan**, **cgRX** (RTIndeX generalised with updates), **RT-DBSCAN**, Meneses et al. (range minimum queries); spatial — Wald et al. (tet-mesh point location, unstructured mesh), **Laass** (point-in-polygon by 3D transformation), **RayJoin**; scientific computing — Salmon et al. (Monte Carlo particle transport), Maul et al. (X-ray synthesis), Zhao et al. (particle simulation).
- **Cited forward**: TTP (ISCA 2026, Tozlu/Naithani/Zhou) lists "Geng et al., PPoPP '25: Spatial indexing (LibRTS)" among non-graphics RT-core uses, alongside Heliostat and Mandarapu et al. [paper, TTP related work]. **A graphics-prefetcher paper enumerating LibRTS as part of the field is forward evidence that category Q is legible from inside the RT-architecture community.**
- **Same authors, adjacent papers**: RayJoin (ICS 2024, the baseline here) and **X-HD** (ICS 2026, Hausdorff distance on RT cores — on this cluster's verdict list, full text read; see the ledger). X-HD cites LibRTS.
- **Contrast with the tensor-core cluster**: LibRTS is to the RT core what a BLAS library is to the tensor core — the moment the fixed-function unit acquires a general-purpose software interface. No equivalent exists yet on the RT side for non-spatial data, and the paper says why.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT cores were replaced by ordinary SIMT cores?** No, and this paper supplies the best *controlled* evidence for that answer anywhere in the cluster: **LBVH is the same linear-BVH index implemented in software on the same RTX 3090, and LibRTS beats it by up to 85.1x (point) and 94.0x (range-contains)**. The BVH data structure is held constant; only the traversal hardware changes. What the RT core supplies is **hardware BVH traversal with fixed-function ray-AABB intersection throughput, reached by handing control from the SM to the RT core at the RayGen shader**, plus the "origin inside the AABB counts as a hit" semantics that makes a containment test a ray cast at all. Every engineering decision in the paper is a negotiation with that hardware's constraints — `t_max = FLT_MIN` to suppress boundary hits, `t_max = 1` to turn a ray into a segment, Ray Multicast because the single-ray shader model forbids shared memory and block sync, degenerate AABBs because OptiX will not delete a primitive, FP32 because RTX parts are FP64-poor. None of these exist without the unit.

**Hardware change or software mapping?** **SOFTWARE MAPPING ONLY.** LibRTS modifies no hardware; it reformulates spatial predicates into ray-AABB intersections within existing OptiX semantics, and solves load balancing (Ray Multicast) and mutability (GAS/IAS instancing, refitting, degenerate-AABB deletion) purely in software.

**Simulated or measured?** **MEASURED** — NVIDIA RTX 3090, OptiX 8.0, CUDA 12.3, FP32, six real geospatial datasets (12.2K–11.5M polygons) plus Spider synthetics, against four CPU and three GPU baselines. No simulator anywhere. Together with `GPU-ICS24-125` (Arkade, RTX 4060 Ti), this is one of the two load-bearing measured results in a cluster otherwise dominated by simulation.

verdict_basis: The contribution is a spatial index whose data structure *is* the OptiX BVH and whose query execution *is* hardware ray-AABB intersection on GPU RT cores, measured on a real RTX 3090 against a software-BVH control on the same GPU. Its 85.1x/94.0x margin over that control is a direct measurement of the fixed-function unit's contribution, and nothing in the design survives its removal.

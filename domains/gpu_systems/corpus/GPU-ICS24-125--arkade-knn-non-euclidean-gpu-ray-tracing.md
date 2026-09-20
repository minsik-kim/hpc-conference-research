# GPU-ICS24-125 — Arkade: k-Nearest Neighbor Search With Non-Euclidean Distances using GPU Ray Tracing

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — fixed-function GPU units repurposed for general computation (software mapping onto shipping RT cores)`
secondary_topics: `k-nearest-neighbour search; spatial indexing; OptiX programming model; non-Euclidean metrics; irregular GPU algorithms`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2311.09168v2) — introduction/motivation, background on RT cores and OptiX and user-defined geometries, the Filter-Refine reduction, the Monotone Transformation reduction, evaluation setup with datasets and baselines, Tables 2-4 results, Figures 6-7 breakdown and sensitivity, stated limitations, related work §7.1 and §7.2.`

## 12.1 Bibliographic facts

- Title: **Arkade: k-Nearest Neighbor Search With Non-Euclidean Distances using GPU Ray Tracing** [paper]
- Venue: **ICS '24** — 38th ACM International Conference on Supercomputing, **June 4–7, 2024, Kyoto, Japan** [paper, printed in the arXiv HTML]. Census records it in session 2 (Best Paper Nominees) and notes a **BEST PAPER AWARD** [official-program, census `ICS_2024.md`].
- Authors and affiliation, all Purdue University, West Lafayette, IN [paper]: **Durga Mandarapu, Artem Pelenitsyn, Vani Nagarajan, Milind Kulkarni**. (The census row gives the first author as "Durga Keerthi Mandarapu"; the paper byline reads "Durga Mandarapu". Recorded, not reconciled.)
- DOI: **`10.1145/3650200.3656601`** [official-web, from the unpaywall/ACM records surfaced in search].
- arXiv: **2311.09168** (v2 read). Publication type of the arXiv item: `PREPRINT` of the `ARCHIVAL_MAIN_PAPER`.
- Artifact: none stated in the read text; census `NOT_SEARCHED`. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

RT cores can only answer one question — "does this ray hit this axis-aligned bounding box?" — and prior RT-accelerated k-NN is therefore welded to the L2 metric because an L2 ball is a sphere; so can k-NN under **L1, L-infinity, general L-p and cosine/angular** distances be reduced to that one question, by *changing the geometry* (Filter-Refine) or by *changing the data* (Monotone Transformation)?

## 12.3 GPU/HPC problem translation

- **Compute.** The reduction inverts the query: instead of searching around the query, the index builds **an r-ball around every data point** and launches a **point ray** (a ray "whose length is a very small positive number") from every query point [paper]. A hit means the query lies inside that data point's ball. All tree descent is thus performed by the RT core.
- **Memory.** The BVH is built and owned by OptiX; the paper's measured cost driver is the **number of ray-AABB intersections per query**, which is reported per dataset (Table 4): roughly **26–3K for L-infinity** versus **~10K–20K for cosine**, the latter inflated because normalisation concentrates points on a unit sphere [paper].
- **Synchronization.** k-nearest is maintained in a **heap in the refine phase on shader cores** [paper].
- **Scheduling.** Radius selection is iterative: the paper adopts **TrueKNN's adaptive radius doubling**, "iteratively increasing the radius until all query points find their k neighbors", with a **BVH refit** per round. Round counts vary sharply (Kitti4M needs **8 rounds**, Randnet **1**) and dominate some runtimes [paper, Table 4].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- **The RT core's geometry is the only interface.** As the paper puts it, "The BVH built by the RT architecture is not accessible nor programmable… during the traversal, the Optix interface notifies the user only when a successful ray-AABB intersection occurs" [paper]. The hardware admits exactly one predicate: ray vs AABB.
- **Hence the metric lock-in.** Prior RT k-NN (RT-kNN, TrueKNN) is "inherently tied to L2 distances" because "the RT cores arrange objects in a scene according to the Euclidean distance" [paper]. The paper is explicit that this is not a fixable approximation: "one cannot merely use L2 nearest neighbor as a proxy for other distance functions" — Euclidean proximity says nothing about angular distance.
- **The consequence for applications** is real, not academic: street-map routing needs Manhattan distance; astronomy needs angular distance [paper].
- **Dimensionality is hard-capped at 3.** "This paper confines its scope to 2- and 3-dimensional spaces because RT cores operate solely within these dimensions" [paper]. That is a property of the fixed-function unit, not of the algorithm.

## 12.5 Mathematical / performance model

**Reduction 1 — Filter-Refine (FR)** [paper]. Generalises the RT-kNN reduction by replacing the *sphere* with the r-ball of the target metric:

| Metric | r-ball geometry (2D / 3D) |
|---|---|
| L2 | circle / sphere (the prior work's case) |
| L1 | square rhombus / square bi-pyramid |
| L-infinity | square / cube |
| general L-p | morphs between sphere and cube |

Each such object is enclosed in a **tight AABB** centred at the data point; OptiX builds the BVH over the AABBs; a point ray from `q` is launched; the RT core reports AABB hits (**filter**); shader cores then compute `D(a,q)` exactly and keep it if `D(a,q) <= r` (**refine**), maintaining a heap of the k closest.

The paper's own framing of the generalisation: "RT-kNN ships spheres to RT cores because an r, L2-ball is exactly a sphere. Similarly, for a distance D, we need to build geometric objects customized to the distance function" [paper].

**Reduction 2 — Monotone Transformation (MT)** [paper]. When the r-ball is too large for FR to be selective — the cosine case — apply a transformation `f` such that ordering under `D` is preserved by ordering under L2 on transformed points. For cosine: `f(a) = a / ||a||`. Points land on the unit sphere and L2 distance is monotone in angular distance; the paper notes the relation is **negative** (larger cosine distance ↔ smaller L2 distance). Then run FR with L2.

## 12.6 Data layout and ownership

- **data point → AABB → BVH leaf**: one AABB per data point, enclosing the metric's r-ball [paper].
- **query point → point ray**: one near-zero-length ray per query, launched from RayGen [paper].
- **RT core**: owns BVH traversal and ray-AABB tests; **shader cores** own the refine-phase exact distance computation and the k-heap [paper].
- **thread → warp → SM → GPU**: the paper does not give a thread-mapping breakdown. `NOT_IN_PAPER`.
- **GPU memory**: Arkade **saturates a 12 GB GPU at 70M points**, where FAISS and Treelogy reach 100M [paper] — the AABB-per-point representation is the cost.

## 12.7 Pseudo code

```
# ---- build (host + OptiX) ----                                    [paper]
for a in dataset:
    ball  = r_ball_of_metric(D, center = a, radius = r)   # rhombus / cube / sphere ...
    aabb  = tight_AABB(ball)
    aabbs.append(aabb)
bvh = optix_build(aabbs)                                   # BVH opaque to the user

# ---- search, TrueKNN-style adaptive radius ----                   [paper]
while some query still lacks k neighbours:
    for q in queries:                                      # RayGen program
        trace(point_ray(origin = q, length = epsilon))     # RT core does the filter
        # Intersection / any-hit program per reported AABB:
        for a in reported_AABBs:                           # refine, on shader cores
            if D(a, q) <= r: heap_push(q, a)
    r = 2 * r                                              # radius doubling
    bvh = optix_refit(aabbs_with_new_r)                    # refit cost per round

# ---- cosine: monotone transformation first ----                   [paper]
dataset = [a / norm(a) for a in dataset];  queries = [q / norm(q) for q in queries]
# then run the L2 case above
```

`RayGen`, `Intersection`, "point ray", the r-ball geometries, filter/refine and the radius-doubling strategy are the paper's [paper]; the loop skeleton and `optix_refit` spelling are `[reconstruction]`.

## 12.8 Real implementation

`NOT_INSPECTED` — no repository is stated in the read text. Interface facts from the paper only [paper]: **OptiX 7.5**, accessed through an "Optix Wrapper Library"; the OptiX kernels named are **RayGen** ("creates rays with user-specified parameters such as the origin, direction, and length") and **Intersection** (the user-defined custom-geometry test). **No `rtcore` PTX intrinsic, no `optixTrace` spelling and no any-hit/closest-hit program name is asserted here** — the read text does not supply them, and they must not be invented.

## 12.9 Kernel execution

OptiX launch → RayGen program per query → hardware BVH traversal (RT core) → Intersection program per reported AABB (shader cores) → heap update. The division of labour is the whole design: **the RT core runs the filter, the SIMT cores run the refine**. The paper's runtime breakdown (Figure 6, L-infinity) confirms the split is lopsided in the intended direction: the **filter phase dominates** and is proportional to BVH quality and ray-AABB intersection count, while the **refine phase is negligible** — "most overhead is tree traversal, not distance computation".

## 12.10 Memory traffic

`NOT_IN_PAPER` at the cache-level. The paper gives a **proxy** for memory work — ray-AABB intersections per query [paper, Table 4] — and notes that the profiling tools cannot go further: "Available Nvidia profilers cannot differentiate RT cores from shader cores", so RT-core saturation is unknown [paper]. This is an important honest limitation for the whole software-mapping branch of category Q: **on shipping hardware the repurposers cannot see the unit they are using.**

## 12.11 Why it is faster/slower (decomposed cause)

All results are **measured on real hardware**: an **NVIDIA GeForce RTX 4060 Ti** (an Ada Lovelace part), with an RTX 4070 Ti (12 GB) also mentioned in the setup, using **OptiX 7.5**; BVH built once, all queries searched 5 times and averaged [paper].

Datasets [paper]: Gowalla (1.27M, 3D), Glove 3D (1.18M, 3D, PCA projection of 25D embeddings), Manuscript (2.15M, 3D), Cali OSM (4.20M, 2D), Kitti (4.0M, 3D), Randnet (6.82M, 3D), Gbif (8.48M, 3D); 10K queries each.

Baselines [paper]: **SCANN** (CPU, quantisation-based approximate, recall 0.99), **Treelogy** (GPU exact k-d tree, modified to support L-p and cosine), **FAISS** (GPU, IVFFlatL2), and **FastRNN** (the prior RT-core k-NN work, extended via the inclusion property for non-L2).

| Metric | vs Treelogy (GPU k-d tree) | vs FastRNN (prior RT) | vs FAISS (GPU) | vs SCANN (CPU) |
|---|---|---|---|---|
| **L1** | 1.6x – 160.9x | 1.3x – 33.1x | — | — |
| **L-infinity** | 4.8x – 200x | 3.2x – 15.6x | — | — |
| **Cosine** | 2.9x – 97x | — | 2.2x – 63.6x | 793.7x – 23,187.9x |

**Every one of these is a measured wall-clock ratio on an RTX 4060 Ti with OptiX 7.5 against the named baseline on the named dataset set — the qualifiers travel with the number.**

The decomposed cause is not arithmetic: the filter phase dominates and its cost tracks ray-AABB intersection count [paper, Figure 6, Table 4]. Arkade wins because the RT core walks the hierarchy in fixed-function hardware while the k-d-tree baselines walk it in divergent SIMT code — and it wins *more* where the baseline's divergence is worse (the paper notes speedups are **not monotone in dataset size**: "Arkade's speedups on these datasets are very different" despite similar cardinality).

The sharpest caveat against over-claiming is the paper's own: against **FastRNN**, the prior RT-core method, the margin is **1.3x–33.1x (L1)** and **3.2x–15.6x (L-infinity)** — an order of magnitude less than against SIMT k-d trees. The RT core supplies most of the win; Arkade's contribution is making the *right metric* reachable through it.

## 12.12 Hardware generation dependence

- **Measured on NVIDIA GeForce RTX 4060 Ti** (Ada Lovelace, **3rd-generation RT cores**) with **OptiX 7.5**; an RTX 4070 Ti with 12 GB is also referenced in the setup [paper]. **The paper does not name the RT-core generation or invoke any Ada-specific RT feature (SER, OMM, DMM)** — the mechanism uses only custom AABB geometry and user Intersection programs, available since Turing. Do not attribute the result to a generation-specific feature. `NOT_IN_PAPER`.
- **No AMD ray accelerator evaluation.** `NOT_IN_PAPER`.
- **The 2D/3D cap is a hardware property**, not a design choice: "RT cores operate solely within these dimensions" [paper]. This is the single most important generation-dependence fact in the software-mapping branch — every application that is natively high-dimensional must be projected down (Glove 3D is a PCA projection of 25D embeddings) before the hardware will take it.

## 12.13 Limitations

Stated by the paper [paper]:
1. **2D/3D only** — a hard RT-core limit.
2. **Radius selection is unsolved**: "Selecting an optimal radius is a challenging task… arbitrary choice of radius might result in poor performance." The adaptive-doubling workaround costs refit rounds (up to 8 for Kitti4M).
3. **BVH opacity** — construction and traversal are not visible or controllable.
4. **Profiling blindness** — NVIDIA profilers cannot separate RT-core from shader-core time, so RT-core saturation is unknown.
5. **Jaccard distance is not supported**: "we do not have a way to perform set operations using RT architecture yet."
6. **Memory scaling** — out of memory at 70M points on 12 GB, where baselines reach 100M.
7. **Speedup versus FAISS degrades as k grows** (Figure 7a) and slightly at 10M+ points (Figure 7b); the paper's defence is that build time stays far cheaper.
- `[inference]` No ablation isolates the gain from tight custom AABBs versus the prior over-approximating sphere-plus-inclusion-property approach; the paper notes this comparison is absent.

## 12.14 Relation to prior corpus

- **This is the canonical software-mapping paper of category Q**: it changes no hardware, uses shipping RT cores through OptiX, and its entire intellectual content is a *reduction* from a general-purpose problem to the one predicate the fixed-function unit implements.
- **Its related work is the cluster's genealogy, verified from the paper's own §7.1** [paper]: Wald et al. 2019 ("RTX Beyond Ray Tracing"), named as "first to use RT cores to accelerate non-ray tracing applications"; Zellmann et al. 2020 (force-directed graph drawing); Evangelou et al. 2021 (fast radius search); Zhu 2022 (**RTNN**); Nagarajan & Kulkarni 2023 (**RT-DBSCAN**); Nagarajan, Mandarapu & Kulkarni 2023 (**RT-kNNS Unbound / TrueKNN**). **RTIndeX is not cited by name in what was read** — recorded as an absence, not asserted either way.
- **Cited upward by the hardware branch**: `GPU-MICRO24-121` (HSU) cites "Mandarapu et al. [38]" — this paper — in its related work as one of the reformulate-as-ray-casting predecessors it aims to replace [paper, HSU]. **This is a verified backward citation link from the MICRO 2024 hardware generalisation to this ICS 2024 software mapping**, in the same institution (Purdue: Kulkarni's group and Rogers's group).
- **Same research line as** RT-BarnesHut (PPoPP 2025, Vani Nagarajan et al. — a co-author here) and LibRTS (PPoPP 2025).
- **Contrast with the tensor-core cluster**: `GPU-PPoPP25-01` (FlashSparse) and `GPU-PPoPP25-02` (Acc-SpMM) are the same *method* — software-only reshaping of a problem to fit a fixed-function unit's one operation — applied to the MMA instruction instead of the ray-AABB test. The structural parallel is exact and is the main argument for treating "fixed-function repurposing" as a method that cuts across topics.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT cores were replaced by ordinary SIMT cores?** No, and in a very literal sense: the contribution *is* the reduction to the RT core's single predicate. What the RT core supplies that SIMT cores do not is **hardware BVH traversal and ray-AABB intersection throughput under total ray incoherence** — the divergent tree descent that makes the Treelogy k-d-tree GPU baseline 4.8x–200x slower on L-infinity is executed in fixed-function hardware with no warp divergence. Every constraint the design bends around (2D/3D only; opaque, unprogrammable BVH; results reported only on AABB hit; no set operations; invisible to the profiler) is a constraint of that unit. Run it on SIMT cores and there is no reason to build r-balls, no reason to invert the query, and nothing left of the paper.

**Hardware change or software mapping?** **SOFTWARE MAPPING ONLY.** "This is entirely a software mapping onto existing NVIDIA RT cores… No hardware modifications are proposed or required" [paper]. Two reductions (Filter-Refine, Monotone Transformation) expressed through OptiX custom geometries and Intersection programs.

**Simulated or measured?** **MEASURED** — NVIDIA GeForce RTX 4060 Ti, OptiX 7.5, seven real datasets, four baselines, 5-run averages. No simulator. This makes Arkade one of the few load-bearing *measured* data points in a cluster otherwise dominated by simulation.

verdict_basis: The contribution is a reduction of non-Euclidean k-NN to the ray-AABB intersection predicate implemented by NVIDIA GPU RT cores, measured on a real RTX 4060 Ti through OptiX; its design, its limits (2D/3D, opaque BVH, no set operations) and its speedups are all consequences of that specific GPU fixed-function unit.

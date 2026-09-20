# GPU-ASPLOS25-124 — Treelet Accelerated Ray Tracing on GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — fixed-function GPU units repurposed/restructured (RT-unit microarchitecture; the rendering-pipeline paper that motivates the generalisation line)`
secondary_topics: `GPU cache locality; SIMT efficiency and warp repacking; CTA scheduling and context virtualisation; scale-model GPU simulation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author-hosted PDF (people.ece.ubc.ca/aamodt/publications/papers/chou.asplos2025.pdf) — introduction/motivation with L1 miss-rate characterisation, background on the Vulkan-Sim RT unit and the treelet concept with its prior history, Figure 3 added structures and their bit-level sizing, the three-phase traversal-mode state machine, Table 1 simulated configuration, LumiBench evaluation, Figures 10-17 results/ablations/energy, limitations as stated, related work and conclusion.`

## 12.1 Bibliographic facts

- Title: **Treelet Accelerated Ray Tracing on GPUs** [paper]
- Venue: **ASPLOS '25** — 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, **March 30 – April 3, 2025, Rotterdam, Netherlands** [paper, printed on the PDF]. Session 3B / volume 30V2 [official-program, census `ASPLOS_2025.md`].
- Authors and affiliation [paper]: **Yuan Hsi Chou, Tor M. Aamodt** — University of British Columbia, Vancouver, Canada.
- DOI: **`10.1145/3676641.3716279`** [official-program / publisher-proceedings, via census `ASPLOS_2025.md`].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

The GPU RT unit's traversal is **ray-stationary** — each ray walks the BVH on its own, so the L1 sees a scattered stream of node fetches (58% average, up to 70% miss rate) and SIMT efficiency collapses to 0.37; can the unit be made to run **treelet-stationary** instead — fetch a cache-sized subtree once, queue up every ray that wants it, and process them together — without the unbounded ray storage that killed the idea in 2010?

## 12.3 GPU/HPC problem translation

- **Compute.** SIMT efficiency in the baseline RT unit is **0.37**; with warp repacking it reaches **0.82** [paper, Figure 13]. The compute problem is not arithmetic throughput but *lane occupancy* during traversal.
- **Memory.** The headline characterisation: "average L1 miss rate is 58% and reaches as high as 70%, implying caches are ineffective at capturing BVH node locality" [paper]. Rays are "incoherent (or lack locality), traversing through different parts of the BVH tree, and causing memory divergence" [paper].
- **Synchronization.** The treelet-stationary phase needs somewhere to park rays that are waiting for their treelet's turn. The paper's answer is **ray virtualisation**: ray state is spilled to a reserved L2 region and the owning CTA is descheduled, then reinjected.
- **Scheduling.** Two schedulers now interact: the RT unit's own treelet selection, and the GPU's **CTA scheduler**, which the RT unit is given a **new path to** so it can inject ready-to-resume CTAs.
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- The RT unit as modelled [paper, baseline in Vulkan-Sim]: a **warp buffer** storing per-ray "ray ID, ray origin and direction, and its status" plus "current traversal stack and treelet stack"; a **memory scheduler** that "pushes a BVH address to the memory access queue"; a **response FIFO** returning fetched data; **fixed-function intersection units**; and an L1/L2/DRAM hierarchy. The unit processes warps from the warp buffer **cyclically**.
- That design is ray-stationary by construction: the unit's unit-of-work is a ray, so the node stream it generates is the union of many independent random walks. No cache of realistic size captures it.
- **What a treelet is** [paper]: "a subdivision of the BVH tree into smaller subtrees" sized to fit in cache; nodes of one colour in the paper's figure belong to one treelet.
- **Why the 2010 idea did not transfer** [paper]: Aila et al. proposed treelets and reported **50–75% memory-traffic reduction**, but "did not consider nor simulate memory latency"; Shkurko et al. implemented them on a **custom MIMD architecture** with two predictable data streams; and the closest GPU attempt, Chou et al.'s **treelet-based prefetcher**, achieved **30% speedup** but **43.5% of its prefetches went unused**, wasting bandwidth. The gap this paper fills is doing treelets on a real GPU RT-unit organisation, where ray storage is bounded and latency is modelled.

## 12.5 Mathematical / performance model

The design is a state machine over three traversal modes [paper]:

1. **Initial phase — ray stationary.** Conventional traversal until a divergence threshold is exceeded.
2. **Treelet stationary.** Rays are grouped into per-treelet queues; a whole treelet is fetched into L1 and every queued ray is processed before switching treelets.
3. **Final phase — ray stationary with warp repacking.** When the largest treelet queue falls below a threshold, underpopulated queues are merged and processed ray-stationary, with repacking to restore lane occupancy.

Sizing, stated to the bit [paper]:
- **Treelet Count Table** — treelet address **19 bits** + ray count **12 bits**, **max 600 entries**, **2.2 KB**, held in the RT unit.
- **Treelet Queue Table** — a hash table **in the L1 cache**, treelet address plus up to **32 ray IDs** per entry: **(19 + 32 x 12 bits) x 128 entries = 6.29 KB**.
- **Reserved L2 section** for virtualised ray state: **32 B per ray** (origin, direction, tmin, tmax).

## 12.6 Data layout and ownership

- **ray → warp buffer**: ray ID, origin, direction, status, traversal stack, treelet stack [paper]. Note the **warp buffer size is 1** in the simulated configuration [paper, Table 1] — i.e. this is a latency-sensitive, not a throughput-hiding, baseline.
- **ray → L2 reserved region**: 32 B of virtualised ray state when the ray is parked [paper].
- **treelet → L1**: the whole treelet is resident during its stationary phase; L1 miss rate drops "as low as 9%" in that phase versus ~60% in the ray-stationary baseline [paper, Figure 11, LANDS scene].
- **RT unit → CTA scheduler**: a new path lets the RT unit reinject ready-to-resume CTAs [paper].
- **node → cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- three-phase traversal mode switching ----                   [paper]
mode = RAY_STATIONARY
while rays remain:
    if mode == RAY_STATIONARY and divergence > threshold:
        mode = TREELET_STATIONARY
    if mode == TREELET_STATIONARY:
        t = select_treelet(TreeletCountTable)          # highest ray count
        fetch_treelet_into_L1(t)
        for ray_id in TreeletQueueTable[t]:            # up to 32 per entry
            resume(ray_id)                             # un-virtualise from L2
            intersect(ray_id, t)
        if largest_queue_size < threshold:
            merge_underpopulated_queues()
            mode = RAY_STATIONARY_WITH_REPACK
    if mode == RAY_STATIONARY_WITH_REPACK:
        warp = repack_active_rays(threshold = 22)      # 22-thread threshold
        intersect_warp(warp)
```

`Treelet Count Table`, `Treelet Queue Table`, `Treelet Controller`, the 22-thread repack threshold and the three phases are the paper's [paper]; the loop structure and helper names are `[reconstruction]`.

## 12.8 Real implementation

`NOT_INSPECTED`. No artifact URL was located (census: `NOT_FOUND_AFTER_SEARCH`). The simulator is **Vulkan-Sim**, "a cycle-based simulator that models the Vulkan ray tracing pipeline and RT unit architecture", which the paper reports as **95.7% correlated** to real GPU hardware [paper]. No source symbols are asserted.

## 12.9 Kernel execution

kernel → CTA → warp → ray → RT-unit traversal step. The novel execution-level move is that the **CTA is no longer the unit of residency**: a CTA whose rays are all parked in treelet queues can be descheduled, its ray state spilled to the reserved L2 region, and later reinjected by the RT unit through the new RT-unit-to-CTA-scheduler path. This is a **GPU context-virtualisation mechanism driven by a fixed-function unit**, which is the feature of the paper most relevant to category Q: the fixed-function unit is given authority over the SM's scheduling.

## 12.10 Memory traffic

- **L1**: baseline ~60% miss rate; **as low as 9%** during the treelet-stationary phase; rising to **75–80%** in the underpopulated-treelet phase [paper, Figure 11, LANDS].
- **L2**: 128 KB, 16-way, 187-cycle latency in the model; a reserved section holds 32 B/ray of virtualised state [paper, Table 1].
- **Structure overhead**: 2.2 KB (count table, in the RT unit) + 6.29 KB (queue table, in L1) [paper].
- **Energy**: **60% savings** versus baseline, of which **ray virtualisation consumes 11% of total design energy** [paper, Figure 17]. Simulator/model estimate, not measured.

## 12.11 Why it is faster/slower (decomposed cause)

All results are **simulated in Vulkan-Sim on the 16-SM scale-model configuration of Table 1**; **no real GPU was benchmarked** [paper].

**Headline** [paper, Figure 10]: virtualised treelet queues give **on average 95% speedup (~1.95x)** over the baseline GPU, **up to 2.55x** "under usage scenarios comparable to video games", and **outperform the prior treelet-prefetching work by 43%**.

The ablation is unusually candid about where the gain is *not* [paper]:
1. **Naive treelets are worse than nothing**: 5% *slower* than baseline (Figure 12).
2. **Grouping underpopulated queues** turns that into an **8x speedup over the naive implementation** — still inadequate alone.
3. **Warp repacking is the decisive component** (Figure 13): without it, **5% slowdown**; at a 16-thread threshold, **84% speedup**; at 22 threads, **95% speedup**. SIMT efficiency 0.37 → 0.82.
4. **Ray virtualisation costs 10%** on its own, from CTA state save/restore (Figure 16).
5. **The treelet-stationary phase handles a minority of the work**: up to 52% of ray intersections, **average 15%** (Figures 14–15). Most cycles remain ray-stationary.

So the decomposed cause is: the locality mechanism (treelets) creates the *opportunity*, but the realised speedup is dominated by the **occupancy** mechanism (warp repacking) that the treelet queues make possible. Reporting "treelets give 95%" without that decomposition would misattribute the effect.

Scene-level controls [paper]: SPNZA gains less because its SIMT efficiency is already high; CHSNT gains less because its baseline L1 miss rate is already low. Both confirm the mechanism.

## 12.12 Hardware generation dependence

- Modelled RT unit is the **Vulkan-Sim RTA** — warp buffer, memory scheduler, response FIFO, fixed-function intersection units [paper]. **No NVIDIA RT-core generation is named** (not Turing 1st-gen, Ampere 2nd-gen, Ada 3rd-gen with SER/OMM/DMM, nor Blackwell 4th-gen). Do not attribute to a generation. `NOT_IN_PAPER`.
- **Explicitly a scale model**: 16 SMs, **L1 16 KB** (fully associative, 39-cycle), **L2 128 KB** (16-way, 187-cycle), **warp buffer size 1**, core/L2 1365 MHz, memory 3500 MHz [paper, Table 1]. The paper itself flags the gap: "While modern GPUs feature much larger sizes than what we simulate (128 KB L1, 72 MB L2 for RTX 4090 GPU)". **The RTX 4090 is named only as the scale reference, not as an evaluated part.**
- Note the corpus link: `GPU-HPCA24-41` (GPU scale-model simulation) is the methodological justification this paper leans on; its assumptions bound how far these numbers travel.
- Benchmarks: **LumiBench**, 14 path-traced scenes, **13.18 MB – 1,868.95 MB** BVH size, **144.1K – 20.6M triangles**, rendered at **256x256, 1 spp, 3 max bounces** [paper]. That resolution/sampling is very low; the "comparable to video games" claim attaches to a subset, not to the 256x256 default.
- API compatibility is asserted for **Vulkan and DXR** [paper], but the treelet traversal order depends on the prior Chou et al. implementation and is not native to either API.

## 12.13 Limitations

Stated or directly supported [paper]:
1. **Treelet stationary is the minority mode** — average 15% of ray intersections; most cycles are ray-stationary because rays diverge.
2. **Scene-dependent**: SPNZA (already high SIMT efficiency) and CHSNT (already low L1 miss rate) benefit little.
3. **Ray virtualisation costs 10%** and 11% of energy.
4. **Scale-model simulation** far below RTX 4090 cache sizes, acknowledged by the authors.
5. **Secondary rays are the hard case**: "most rays in the ray stationary phase are secondary rays, which there are less of compared to primary rays, making it harder to populate treelet queues."
6. **Incomplete API integration** — treelet traversal order inherited from prior work, not native to Vulkan/DXR.
- `[inference]` The 600-entry count table and 128-entry queue table are fixed structures; scenes with many more live treelets than that would degrade, and no sensitivity study on those capacities was located.

## 12.14 Relation to prior corpus

- **This is the rendering-pipeline paper that anchors the cluster's other end.** It is *not* a repurposing paper: it accelerates ray tracing for ray tracing's sake. Its relevance to category Q is that it (a) characterises exactly what the RT unit's memory and occupancy behaviour is, which is the raw material every repurposing paper trades on, and (b) states the connection itself.
- **Verified forward lineage, in the paper's own words** [paper, conclusion]: "With proposals from Ha et al. [14] and Barnes et al. [6] that extend ray tracing accelerators in GPUs to support more general tree traversal workloads, we believe the hardware modifications and treelet queue optimizations in this work in conjunction to accelerate general tree traversal workloads on GPUs as well." Ha et al. [14] is `GPU-MICRO24-122` (TTA); Barnes et al. [6] is `GPU-MICRO24-121` (HSU). **This single sentence is the strongest in-corpus evidence that the MICRO 2024 generalisation papers are recognised as a line by the graphics-architecture community itself.**
- **Also cites the software-mapping branch** [paper]: RT-DBSCAN, RTIndeX, RTNN, described as "reformulating their algorithms to fit the ray tracing pipeline" — but only in the conclusion, as future applications.
- **Same group**: Tor Aamodt (UBC) co-authors both this and TTA; Yuan Hsi Chou is a co-author of TTA. The lineage is institutional as well as citational.
- **Methodological dependency**: `GPU-HPCA24-41` (scale-model GPU simulation).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT unit were replaced by ordinary SIMT cores?** No. Every structure the paper adds is defined relative to RT-unit-specific hardware: the **Treelet Count Table** lives in the RT unit; the **Treelet Controller** is a state machine over the RT unit's traversal modes; the **warp buffer** (holding traversal stack and treelet stack) is the thing being drained and repacked; and the new **RT-unit-to-CTA-scheduler path** only makes sense because a fixed-function unit, not a warp, is deciding when work is ready. The measured effects — SIMT efficiency 0.37 → 0.82, L1 miss 60% → 9% during the treelet phase — are properties of the RT unit's node-fetch stream. A SIMT reimplementation would have to rebuild the traversal loop in software, which is exactly the baseline the RTA exists to beat.

**Hardware change or software mapping?** **HARDWARE CHANGE** — three new RT-unit structures (Treelet Count Table, Treelet Queue Table, Treelet Controller), an L1 hash-table allocation, a reserved L2 region, a new datapath from the RT unit to the CTA scheduler, and warp-repacking logic inside the RT unit. Software compatibility with Vulkan/DXR is claimed, but the contribution is microarchitectural.

**Simulated or measured?** **SIMULATED** — Vulkan-Sim, 16-SM scale model (Table 1), LumiBench at 256x256/1 spp/3 bounces. The 95.7% correlation figure is the simulator's reported fidelity, not a measurement of this design. Energy figures are model estimates. **The RTX 4090 appears only as a cache-size reference point, never as an evaluated device.**

verdict_basis: The contribution consists of structures added inside the GPU ray-tracing unit and a new control path from that unit to the GPU's CTA scheduler, evaluated in a cycle-level GPU RT-unit simulator. Its benefit is measured in SIMT efficiency and L1 behaviour of the RT unit's BVH node stream — quantities that exist only in a GPU with an RT unit.

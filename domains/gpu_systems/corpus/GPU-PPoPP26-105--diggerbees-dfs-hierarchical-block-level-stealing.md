# GPU-PPoPP26-105 — DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — Graph / irregular GPU workloads (traversal, work stealing, load balancing)`
secondary_topics: `G — sparse/irregular kernel design; GPU memory-hierarchy-aware data structures; atomics and work-stealing protocols; Hopper asynchronous copy (TMA)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author PDF (https://www.ssslab.cn/assets/papers/2026-niu-DiggerBees.pdf) — title/authors/affiliations, abstract, introduction and the three stated GPU-mapping challenges, the HotRing/ColdSeg two-level stack with capacities and the four operations, the warp-level execution model, the intra-block stealing protocol (victim selection, atomicCAS reservation, local transfer) and the inter-block protocol (power-of-two-choices victim block, victim warp, reservation, remote transfer), the synchronisation primitives, the full evaluation setup (CPU + A100 + H100, CUDA 12.8, 234 SuiteSparse graphs, five baselines), MTEPS methodology, headline results, the four-stage v1-v4 ablation, the load-balance and parameter-sensitivity studies, the stated limitations, and related work. Abstract cross-checked against the official PPoPP 2026 TOC.`

## 12.1 Bibliographic facts

- Title: **DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs** [paper]
- Venue: **PPoPP 2026**, 31 Jan – 4 Feb 2026, Sydney [paper]. DOI **`10.1145/3774934.3786457`** [paper].
- Authors [paper]: **Yuyao Niu, Yuechen Lu, Weifeng Liu, Marc Casas**. Affiliations: **Barcelona Supercomputing Center** (Spain); **China University of Petroleum-Beijing** (China); **Universitat Politècnica de Catalunya** (Spain).
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Full text used: `https://www.ssslab.cn/assets/papers/2026-niu-DiggerBees.pdf` [paper].
- Artifact: none located. `NOT_INSPECTED`. No source symbols asserted.
- Note on authorship lineage: **Yuyao Niu and Marc Casas** are also the authors of **BerryBees** (PPoPP 2025, bit-Tensor-Core BFS), which appears here as a *baseline*. The naming is deliberate.

## 12.2 Core question (one sentence)

DFS is the one classical graph primitive that has never had a good GPU implementation, because its stack is sequential, deep and unbounded — so can a **two-level stack split across shared and global memory** plus **two tiers of work stealing (intra-block and inter-block)** make unordered parallel DFS not merely feasible but faster than tuned GPU **BFS** on deep, narrow graphs?

## 12.3 GPU/HPC problem translation

- **Compute.** Not the bottleneck; DFS is pointer-chasing.
- **Memory.** The first stated challenge: traversal "can demand megabytes of stack space", far beyond the tens-to-hundreds of KB of shared memory per SM [paper]. The two-level stack is the direct answer.
- **Synchronization.** The design's minimalism here is its most interesting property: **"The only global synchronization is `atomicCAS` on the visited array"** [paper] during normal traversal. All other atomics belong to the stealing protocol.
- **Dependency.** DFS's stack dependency is broken by dropping lexicographic ordering — the traversal is *unordered* DFS, which "avoids lexicographic constraints and can achieve close-to-linear work efficiency under ideal conditions" [paper]. This is an algorithmic relaxation that makes the GPU mapping legal at all.
- **Load imbalance.** The dominant concern and the paper's headline mechanism. Measured: coefficient of variation reduced by **>50%** versus random victim selection (`amazon`: **2.48 → 0.72**), and a **3.44× variance reduction** from the two-choice load-aware block selection [paper].

## 12.4 Why the problem exists (hardware root cause)

Three challenges, as the paper states them [paper]:
1. **Memory bottleneck** — the stack does not fit in shared memory; global memory has the capacity but not the latency.
2. **Intra-block inefficiency** — thread-private stacks cause **warp divergence** (each thread walking a different path diverges the SIMT lanes); a block-shared stack instead costs atomics and synchronisation.
3. **Inter-block scalability** — irregular DFS work cannot be statically partitioned across SMs.

The design resolves (2) by a choice that is worth stating precisely: **each warp owns one stack and all 32 threads follow the same path**, so "all 32 threads in a warp follow the same path, eliminating warp divergence" [paper]. The warp, not the thread, is the unit of traversal. That trades lane-level parallelism (32 lanes cooperating on one vertex's edge list) for zero divergence — the classic SIMT bargain, made explicitly.

## 12.5 Mathematical / performance model

No analytic model. The design constants and the measured balance metrics are the quantitative content [paper]:

- **HotRing**: circular buffer, **128 entries**, shared memory, holding ⟨vertex, offset⟩ pairs; push/pop in O(1) by modulo arithmetic. Footprint: `hot_vertex` + `hot_offset` = **128 entries × 4 bytes = 512 B per warp** [paper].
- **ColdSeg**: global memory pool, **`nv/nw` entries per warp** (`nv` vertices, `nw` warps).
- **Stealing thresholds**: `hot_cutoff = 32` (intra-block), `cold_cutoff = 64` (inter-block); a thief reserves **half the cutoff** (`hot_cutoff/2`, `cold_cutoff/2`) [paper].
- **Balance metric**: coefficient of variation, >50% reduction vs random victim selection; `amazon` 2.48 → 0.72 [paper].
- **Scaling check**: H100/A100 speedup **1.33×** for DiggerBees vs **1.18×** for NVG-DFS, against a **22.2% SM count increase** (108 → 132) [paper]. DiggerBees tracks the SM increase; the baseline does not.

## 12.6 Data layout and ownership

- **thread**: no private state of consequence; all 32 lanes of a warp walk the same path [paper].
- **warp**: owns one **HotRing** (shared memory, 128 entries, 512 B) and one **ColdSeg** (global memory, `nv/nw` entries). Four operations: fast push/pop on HotRing; **flush** (batch from HotRing tail → ColdSeg top when full); **refill** (batch from ColdSeg → HotRing when empty) [paper].
- **block**: many warps; **one leader warp per block** handles *all* inter-block communication, "reducing contention" [paper]. A **32-bit mask in shared memory** tracks per-warp active/idle state [paper].
- **grid**: up to **132 blocks — one per H100 SM** [paper].
- **global**: `visited` array, atomically accessed.
- **Async copy**: flush and refill use **`cp_async_bulk` / `cuda::memcpy_async` with TMA**, worth **≈5% speedup on H100** [paper]. A small but explicitly Hopper-specific number.
- **node/cluster**: single GPU. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- per warp ---                                                [paper]
while not global_termination:
    if hotring.empty():
        if not coldseg.empty(): refill(hotring, coldseg)   # cp_async_bulk / TMA
        else: mark_idle(warp_mask)                          # 32-bit shared mask

    v, off = hotring.pop()
    for u in neighbours(v, off):
        if atomicCAS(visited[u], 0, 1) == 0:                # ONLY global sync in traversal
            hotring.push(u, 0)
            if hotring.full(): flush(hotring, coldseg)

# --- intra-block stealing, when this warp is idle ---            [paper]
victim = argmax_over_block_peers(hotring_count) if count > hot_cutoff(=32)
reserved = atomicCAS(victim.hotring.tail, ...)              # reserve hot_cutoff/2
copy(reserved -> my.hotring); mark_active(warp_mask)

# --- inter-block stealing, when the whole block is idle ---      [paper]
# leader warp only
b1, b2 = sample_two_random_active_blocks()                  # power-of-two choices
victim_block = heavier_of(b1, b2)                           # load-aware
victim_warp  = argmax_over(victim_block, coldseg_count)     # threshold cold_cutoff(=64)
reserved = atomicCAS(victim_warp.coldseg.bottom, ...)       # reserve cold_cutoff/2
__threadfence()                                             # global consistency
copy(reserved -> leader.hotring)                            # async copy
```

`HotRing`, `ColdSeg`, flush, refill, `hot_cutoff`, `cold_cutoff`, `atomicCAS`, `__threadfence()`, `__threadfence_block()`, the 32-bit warp mask, the leader warp, and the power-of-two-choices victim selection are all the paper's [paper]. `global_termination`, `argmax_over_block_peers` are `[reconstruction]` names.

## 12.8 Real implementation

`NOT_INSPECTED`. No artifact URL located [paper]. No source symbols asserted.

Instruction/API-level facts, from the paper only [paper]: `atomicCAS` (work reservation and `visited`), `__threadfence_block()` (intra-block visibility), `__threadfence()` (global consistency), and **`cp_async_bulk` / `cuda::memcpy_async` with TMA** for flush/refill on H100. Software: **CUDA v12.8, driver v570.153.02**.

## 12.9 Kernel execution

kernel → block (one per SM, up to 132 on H100) → warp (the unit of traversal; owner of a HotRing/ColdSeg pair) → 32 lanes walking one path together. The paper does not claim a "persistent kernel" in those words but the structure is one: "warps perform DFS, steal intra-block when idle, and blocks steal inter-block when empty, until global termination" [paper]. Recorded as the paper describes it; the label *persistent kernel* is `[inference]` and flagged as such.

The three-tier idleness escalation is the design's spine: a warp first refills from its own ColdSeg, then steals within its block through shared memory, then — only through its block's leader warp — steals across blocks through global memory. Each tier is cheaper than the next, and the thresholds (32, 64) set when to escalate.

## 12.10 Memory traffic

- **HotRing in shared memory** absorbs the frequent push/pop; **ColdSeg in global memory** absorbs depth. This is a deliberate latency/capacity split: "leverages the GPU memory hierarchy to provide low-latency access for frequent operations and sufficient capacity for deep traversals" [paper].
- **Flush/refill are batched**, not per-element, and use asynchronous bulk copy (TMA on H100), worth ≈5% [paper].
- **`visited` array** is the only globally contended structure in steady-state traversal.
- No L1/L2/HBM counter breakdown, no bandwidth numbers. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Setup, all qualifiers carried** [paper]: **NVIDIA H100** (Hopper, 132 SMs, 64 GB, 2.02 TB/s) and **NVIDIA A100** (Ampere, 108 SMs, 80 GB, 1.94 TB/s), **CUDA v12.8**, driver **v570.153.02**; CPU baselines on **Intel Xeon Max 9462** (64 cores, 2×64 GB HBM, 1 TB/s). Graph suite: **234 graphs from the SuiteSparse Matrix Collection** — 151 DIMACS10, 68 SNAP, 15 LAW — spanning **0.08 MB to 43.61 GB**; 12 representative graphs analysed in detail. Metric: **MTEPS**, 64 source vertices from the **GAP benchmark suite**, geometric mean.

Baselines by name [paper]: **CKL-PDFS** (2008, CPU work-stealing DFS), **ACR-PDFS** (2015, CPU parallel unordered DFS), **NVG-DFS** (2017, GPU BFS-style lexicographic DFS), **Gunrock** (2016, GPU BFS framework), **BerryBees** (2025, GPU BFS).

Results [paper]:
- vs **CKL-PDFS**: **1.37×** avg (up to 6.24×)
- vs **ACR-PDFS**: **1.83×** avg (up to 12.44×)
- vs **NVG-DFS**: **30.18×** avg (up to 1841.68×)
- vs BFS: **12.12× faster on `euro_osm`** than the best BFS; **3.70× slower on `ljournal`**
- Robustness: all 234 graphs complete; **NVG-DFS fails on 44 graphs** from memory overhead.

Ablation, four progressive versions [paper, Figure 8]:
- **v1** 1-level stack, 1 block, intra-block stealing — baseline
- **v2** 2-level stack, 1 block — **+45%** average throughput. *Cause: the memory-hierarchy split alone.*
- **v3** 2-level, 66 blocks, intra+inter — **25.94×–38.41×**. *Cause: inter-block stealing; this is where almost everything comes from.*
- **v4** 2-level, 132 blocks — **+67–82%** further on most graphs; small graphs plateau.

Parameter sensitivity [paper, Figure 10]: defaults (32, 64) near-optimal; too-small thresholds raise atomic contention, too-large ones reduce stealing reactivity; **performance is more sensitive to `cold_cutoff`** — i.e. to the inter-block tier, consistent with v3 carrying the gain.

## 12.12 Hardware generation dependence

- **Cross-generation evidence is unusually good**: A100 *and* H100, with an explicit scaling check (1.33× DiggerBees vs 1.18× NVG-DFS against a 22.2% SM increase) showing the design tracks SM count [paper].
- **One Hopper-specific dependence**: `cp_async_bulk` / TMA for flush and refill, worth **≈5% on H100** [paper]. Honestly small — the paper does not oversell it.
- Block count is tied to SM count (132 on H100). The design is therefore occupancy-shaped but not instruction-shaped: no MMA, no matrix unit, nothing precision-specific.

## 12.13 Limitations

Stated by the paper [paper]:
1. **Topology-dependent** — DFS underperforms BFS on shallow, wide, low-diameter graphs (social networks); the `ljournal` 3.70× loss is reported, not hidden.
2. **No lexicographic ordering** — the trees produced are valid but unordered; applications needing strict DFS order cannot use this.
3. **Synchronisation overhead** — inter-block `atomicCAS` and `__threadfence()` remain the residual bottleneck.
4. **ColdSeg memory overhead** — `nv/nw` per warp allocated up front; large graphs may struggle.

## 12.14 Relation to prior corpus

- **Same laboratory** as `GPU-SC24-103` (Mille-feuille) and `GPU-PPoPP26-104` (Trojan Horse) — SSSLab/CUPB with **Weifeng Liu** — and same authors as **BerryBees** (PPoPP 2025), which the tensor-cores ledger records as `CORE_GPU` on the bit-MMA path and which is a *baseline here*. Niu/Casas thus appear on both sides of the "use the matrix unit for graphs" question: BerryBees does BFS on bit Tensor Cores; DiggerBees does DFS with no matrix unit at all. **That is direct evidence that the graph-on-GPU community does not regard matrix-unit exploitation as the general answer.**
- **Complementary to** `GPU-PPoPP26-104` (Trojan Horse): device-side runtime stealing vs host-side ahead-of-time priority aggregation, same lab, same proceedings.
- **Contrast with** `GPU-PPoPP26-02` (Cubie, same lab), which characterises where matrix units help; DiggerBees is a data point for "not here".
- Adjacent to `GPU-MICRO24-41` (over-synchronisation in GPU programs).
- `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: Every one of the three design decisions is a named GPU property. (i) The **warp is the traversal unit and all 32 lanes follow one path** — a direct response to SIMT divergence that has no CPU meaning; on a CPU each thread would simply walk its own path. (ii) The stack is **split across shared memory (HotRing, 512 B/warp) and global memory (ColdSeg)** specifically because the GPU's low-latency on-chip store is capacity-bounded at tens of KB per SM while the high-capacity store is high-latency — the 45% v1→v2 ablation step isolates exactly this. (iii) The stealing protocol is built from `atomicCAS` reservations, `__threadfence_block()`/`__threadfence()` visibility, a 32-bit shared warp mask and a **leader warp per block** to keep global-memory contention off the other warps; and flush/refill ride Hopper's `cp_async_bulk`/TMA. CPU work-stealing DFS already existed (CKL-PDFS 2008, ACR-PDFS 2015, both baselines here) and DiggerBees beats them by only 1.37×/1.83× — the paper's real result is the **30.18× over the previous GPU DFS**, i.e. the contribution is precisely the GPU mapping and nothing else.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Load imbalance — claimed and established, strongly.** Coefficient of variation halved (`amazon` 2.48 → 0.72), 3.44× variance reduction from two-choice selection, and the v2→v3 ablation step (25.94×–38.41×) attributes the bulk of the speedup to inter-block stealing.
- **Memory — claimed and established.** The v1→v2 step isolates the two-level stack at +45%.
- **Dependency — claimed and addressed by relaxation**, not by a mechanism: unordered DFS drops the lexicographic constraint. The paper is explicit about the cost (limitation 2).
- **Synchronisation — claimed, partially established.** Minimised by design (one `atomicCAS` on `visited` in steady state; leader-warp funnelling), but the paper itself lists residual inter-block atomic/fence cost as an open limitation.
- **Compute — not a claim.**

verdict: `CORE_GPU`

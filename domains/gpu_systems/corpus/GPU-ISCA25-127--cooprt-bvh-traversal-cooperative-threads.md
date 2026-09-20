# GPU-ISCA25-127 — CoopRT: Accelerating BVH Traversal for Ray Tracing via Cooperative Threads

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — RT-unit microarchitecture (rendering-pipeline branch: the papers that characterise what the RT unit supplies)`
secondary_topics: `SIMT divergence and load balancing; work stealing in hardware; warp buffer / traversal stack microarchitecture; memory bandwidth utilisation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author-hosted PDF (hzhou.wordpress.ncsu.edu/files/2025/05/coopRT_isca25.pdf) — introduction/motivation and Figure 1 trace_ray stall characterisation, background on BVH/DFS traversal and the Vulkan-sim RT-unit model, the Load Balancing Unit and Algorithm 2, the min_thit synchronisation logic and multiplexor/crossbar network, evaluation setup (Vulkan-sim 2.0, SM75_RTX2060 config), Figures 9-19 results and ablations (subwarp sizing Table 3, warp-buffer comparison, shader-type variation, mobile configuration), limitations, related work.`

## 12.1 Bibliographic facts

- Title: **CoopRT: Accelerating BVH Traversal for Ray Tracing via Cooperative Threads** [paper]
- Venue: **ISCA '25** — 52nd Annual International Symposium on Computer Architecture, **June 21–25, 2025, Tokyo, Japan** [paper, printed on the PDF]. Session **1C "GPUs & Ray Tracing"** [official-program, census `ISCA_2025.md`] — the same session as Heliostat.
- Authors and affiliation [paper]: **Yavuz Selim Tozlu, Huiyang Zhou** — North Carolina State University, Raleigh, NC, USA.
- DOI: **`10.1145/3695053.3731118`** [publisher-proceedings, census].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: `https://zenodo.org/records/15103378` [official-web, from search]. **NOT_INSPECTED.**
- Author talk video: `https://www.youtube.com/watch?v=jIgJLOMId9c` [official-web, census]. **NOT_VIEWED** — no `[author-presentation]` claim is made here.

## 12.2 Core question (one sentence)

Inside an RT unit a warp's 32 rays traverse wildly different BVH paths, so most lanes sit idle waiting for the one long-running ray — can the **idle threads steal node addresses off the busy threads' traversal stacks** and help traverse *someone else's ray*, turning intra-warp divergence from a loss into extra parallelism, entirely in hardware and invisibly to software?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's diagnosis: "most of the stalls are due to the `trace_ray` instructions" [paper, Figure 1], caused by two distinct kinds of waste — **inactive threads** (rays that terminated early) and **early-finishing threads** (rays that completed traversal before their warp-mates). Baseline active-thread fraction during tracing is **30–70% depending on scene** [paper, Figure 10].
- **Memory.** "BVH traversals are memory-bound, dominated by reading tree nodes, with little computation needed mainly for intersection tests and coordinate transformations" [paper]. CoopRT therefore *converts idle lanes into memory-level parallelism*, which is why it raises bandwidth use so sharply (below) and why bandwidth becomes its own limit.
- **Synchronization.** This is the subtle part. A helper thread traversing someone else's ray may find a hit, and that hit must update the **main thread's `min_thit`** (closest-hit distance). The paper implements this with **AND/OR gate logic** so that multiple threads' results are ORed and only valid, closer hits update the main thread's `min_thit` [paper].
- **Scheduling.** A new per-SM **Load Balancing Unit (LBU)** pairs one idle thread (helper) with one busy thread (main) and, **each cycle, moves one node address from the main thread's stack to the helper's stack** [paper].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- The RT unit, as modelled [paper]: a specialised execution lane operating **at warp granularity**, with "a warp buffer which keeps the ray data and traversal stack for each thread". Each cycle one warp is selected, memory requests are served, intersection tests are performed, and results update `min_thit`. Crucially, **"the per-thread traversal stack stores the addresses of the nodes instead of the node data itself"** — that representation is what makes stealing cheap: moving one *address* is a few bytes, not a node.
- The scene is a BVH of AABBs walked depth-first; the modelled baseline assumes a **6-ary tree** (up to 6 children per node) [paper].
- The root cause is therefore structural and specific: the RT unit inherits the warp as its unit of scheduling, but a ray is the unit of work, and the two have wildly different lifetimes. Nothing in the baseline lets a finished lane contribute.

## 12.5 Mathematical / performance model

No closed-form model; the design is an algorithm plus a datapath [paper, Algorithm 2]:

```
each thread t:  main_tid[t] = t           # 5-bit field in the warp buffer
loop:
    if stack[t] is empty:
        find a busy thread b (non-empty stack)      # LBU pairs helper<-main
        addr = pop(stack[b])                        # one address moved per cycle
        main_tid[t] = main_tid[b]                   # inherit whose ray this is
        push(stack[t], addr)
    node = pop(stack[t])
    do DFS step for ray main_tid[t], using that ray's properties
      and that ray's min_thit
    on primitive hit: OR result into min_thit[main_tid[t]]   # AND/OR gate network
until all stacks empty
```

`main_tid`, the stack-empty flag, the LBU, the one-address-per-cycle transfer and the OR-based `min_thit` update are the paper's [paper]; the loop spelling is `[reconstruction]` of Algorithm 2.

## 12.6 Data layout and ownership

- **thread → warp buffer entry**: ray data + traversal stack, plus two new fields — a **5-bit `main_tid`** and a **stack-empty flag** [paper]. Five bits is exactly enough to name one of 32 lanes; the field width is the design's statement that helping is intra-warp only.
- **ray → `min_thit`**: owned by the main thread, written by any of its helpers through the OR network [paper].
- **stack → LBU → stack**: node **addresses** migrate; node *data* does not [paper].
- **routing**: per-thread **multiplexors** route the stack top-of-stack from the LBU to the selected helper threads; a **crossbar** (or several smaller crossbars in the subwarp variants) connects math-unit outputs to the main thread's `min_thit` [paper]. **This crossbar is the design's area cost and the reason subwarp variants exist.**
- **SM → GPU**: **30 SMs, 1 RT unit per SM, max 4 warps in the RT unit's warp buffer, 1365 MHz core clock** [paper].
- **node → cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

See §12.5 — the algorithm is short enough that it is the model.

## 12.8 Real implementation

`NOT_INSPECTED`. A Zenodo artifact exists (`zenodo.org/records/15103378`) but was not fetched in this pass; no source symbols are asserted. The simulator is **Vulkan-sim 2.0**, "a cycle-level GPU simulator built on GPGPUsim", modified in **both the functional and the timing simulator** to model CoopRT [paper].

## 12.9 Kernel execution

The execution hierarchy is unchanged above the RT unit — kernel → CTA → warp → `trace_ray`. What changes is *inside* the instruction: a single `trace_ray` now has lanes working on **other lanes' rays**, tracked by `main_tid`. The paper is explicit that this is "transparent to the software" and "requires no changes to the programming model" [paper]. That property is worth flagging for this cluster: it is a hardware change with **zero** software surface, the opposite extreme from TTA (`GPU-MICRO24-122`), which changes the Vulkan API.

## 12.10 Memory traffic

- **L2 bandwidth: up to 5.7x increase**; **DRAM bandwidth: up to 5.5x increase** [paper, Figure 12]. These are *increases* and they are the mechanism, not a side effect: idle lanes become outstanding node fetches.
- Caches in the model: **L1 64 KB, L2 3 MB, DRAM 3500 MHz** [paper].
- On a **mobile configuration (8 SMs, 4 memory channels)**, DRAM utilisation rises from **44% to 85.3%** and the speedup is **1.8x** [paper, Figure 18] — i.e. the mechanism still works when bandwidth-constrained, but the headroom it exploits is smaller.
- The paper flags the corresponding risk directly: CoopRT "increases memory request rate, potentially causing contention" [paper].

## 12.11 Why it is faster/slower (decomposed cause)

All results are **simulated in Vulkan-sim 2.0** on the **SM75_RTX2060** configuration (30 SMs, 1 RT unit/SM, 4-entry warp buffer, 64 KB L1, 3 MB L2) [paper]. **No real GPU was executed.** Benchmarks: **LumiBench**, 16 scenes, **256x256 for 13 scenes and 128x128 for 2 (car, robot)**, 1 sample per pixel, with path-tracing (PT), ambient-occlusion (AO) and shadow (SH) shaders [paper].

**Headline** [paper, Figure 9]: **geometric mean 2.15x speedup**, **maximum 5.11x** (scene crnvl). **Power increases 2.02x on average**; **EDP improves 2.29x**. The power figure must always accompany the speedup — this design buys performance by activating idle hardware, so power goes up almost as much as performance does.

The causal chain is confirmed by four independent controls in the paper:

1. **Thread utilisation** [Figure 10, 11]: baseline 30–70% active; on the bath scene utilisation rises **30.5% → 94.6%**. The mechanism does what it claims.
2. **Divergence dependence** [Figure 17]: **path tracing 2.15x** (high divergence), **ambient occlusion 1.42x** (moderate), **shadow 1.28x** (low). Gain tracks divergence monotonically — the cleanest single piece of evidence that the effect is divergence recovery.
3. **Scene coherence** [Figure 9]: crnvl/fox/party (high divergence) 3–5x; spnza (coherent rays) ~1.3x.
4. **Slowest-warp latency** [Figure 14]: **0.46x of baseline**, versus 0.62x for the alternative of simply enlarging the warp buffer.

**The decisive comparison** [paper, Figure 13]: a **32-entry warp buffer without CoopRT gives 1.64x**, while **CoopRT with the baseline 4-entry buffer gives 2.15x**. So the gain is genuinely from *sharing work between lanes*, not merely from having more rays in flight — a distinction that a less careful paper would have left ambiguous.

**Area/subwarp ablation** [paper, Table 3, Figure 19] — synthesised areas, not measured silicon:

| Variant | Speedup | Area |
|---|---|---|
| Full warp (32) | 2.15x | 13,347 um^2 |
| Subwarp 16 | 2.09x | 13,104 um^2 (−1.8%) |
| Subwarp 8 | 1.97x | 12,661 um^2 (−5.1%) |
| Subwarp 4 | 1.72x | 12,055 um^2 (−9.7%) |

The area curve is flat and the speedup curve is not, which is the paper's argument for the full-warp crossbar.

## 12.12 Hardware generation dependence

- **The modelled configuration is `SM75_RTX2060`** — i.e. an **NVIDIA Turing** part, **1st-generation RT cores**, as supplied by Vulkan-sim [paper]. The paper itself flags this as a limitation: "RTX2060 architecture from 2019". **Do not generalise these numbers to Ampere, Ada or Blackwell RT cores.**
- **No real GPU was executed**; simulation only.
- The mechanism depends on **per-thread traversal stacks holding node addresses** and on the RT unit operating at warp granularity. It would not apply unchanged to an AMD-style ray accelerator where the traversal stack is managed in software by the shader — there the "stealing" would be a software transformation, not a hardware one. `[inference]`, flagged.
- A **mobile configuration** (8 SMs, 4 memory channels) is also evaluated: **1.8x** [paper, Figure 18].
- Resolution is capped at **256x256** by simulator time/memory limits, with two scenes at 128x128 [paper].

## 12.13 Limitations

Stated or directly supported [paper]:
1. **Simulation only**, on a 2019-era RTX 2060 model.
2. **Resolution capped at 256x256** (two scenes at 128x128) by simulator constraints.
3. **Power cost is large**: 2.02x average power increase. EDP still improves (2.29x), but this is not a free lunch.
4. **Memory bandwidth saturation** — the mechanism works by generating more concurrent requests, so it can run into contention; the enlarged-warp-buffer alternative competes on similar ground at higher area.
5. **Shared `min_thit` bottleneck**: only one response per cycle from the FIFO, so multiple helpers cannot update in parallel without more bandwidth or atomics.
6. **Coherent scenes gain little** (spnza ~1.3x); the technique needs divergence to exist.
7. **Not combined with prefetching**: the paper acknowledges a treelet prefetcher could be combined but does not evaluate it, noting bandwidth-saturation interactions would need care.
- `[inference]` Helping is strictly intra-warp (5-bit `main_tid`); a warp in which *all* rays finish early gets no benefit and must wait for the next warp.

## 12.14 Relation to prior corpus

- **This is a rendering-pipeline paper, not a repurposing paper** — it accelerates ray tracing for ray tracing. It earns its place in this cluster because it isolates, and then fixes, one of the two properties every repurposing paper relies on: **the RT unit's behaviour under ray divergence**. If a repurposing paper claims the RT unit "tolerates divergence", CoopRT quantifies how much of that tolerance is actually leaving 30–70% of lanes idle.
- **Verified citation lineage — CoopRT cites both MICRO 2024 generalisation papers** [paper, related work]: "Ha et al. [26] … Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs, MICRO '24" (= `GPU-MICRO24-122`) and "Barnes et al. [11] … Extending GPU Ray-Tracing Units for Hierarchical Search Acceleration, MICRO '24" (= `GPU-MICRO24-121`). It also cites **RTNN (Zhu 2022)** as non-graphics repurposing. **A pure graphics-microarchitecture paper at ISCA 2025 citing both hardware-generalisation papers is direct evidence that the generalisation line is recognised as part of the RT-unit architecture conversation, not a side branch.**
- **Cites the treelet line**: Chou et al. MICRO '23 (treelet prefetcher) — the precursor to `GPU-ASPLOS25-124`; Aila & Karras; Wald's active thread compaction; Liu et al. intersection-prediction caching [paper].
- **Same ISCA 2025 session (1C, "GPUs & Ray Tracing") as Heliostat**, which is adjudicated `CORE_GPU`/`ABSTRACT_ONLY` in `_LEDGER_memory_virtualization.md`. That session pairing — "make the RT unit faster at ray tracing" next to "make the RT unit do page-table walks" — is itself a taxonomy data point.
- **Direct follow-on by the same group**: TTP (ISCA 2026, Tozlu, Naithani, Zhou), which prefetches BVH nodes from the traversal stacks and explicitly compares against the treelet prefetcher. TTP's related work cites Heliostat, LibRTS, Ha et al., Barnes et al. and Mandarapu et al. — see the ledger.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT unit were replaced by ordinary SIMT cores?** No. Every element of CoopRT is defined on RT-unit structures: the **warp buffer** holding per-thread ray data and traversal stacks (extended with `main_tid` and a stack-empty flag); the **per-thread traversal stack of node addresses**, whose address-only representation is what makes one-per-cycle stealing cheap; the **`min_thit` register** and the AND/OR network that lets a helper's hit update another ray's closest-hit distance; and the **multiplexor/crossbar network** between the RT unit's math units and those registers. What the RT unit supplies that SIMT cores do not is precisely the thing being load-balanced: a **hardware traversal state machine with per-lane hardware stacks that runs independently of the SM's instruction stream**. On SIMT cores the traversal loop is software, the "stack" is registers or local memory, and intra-warp work stealing would be a software transformation with none of this paper's content (no LBU, no crossbar, no hardware `min_thit` merge). The divergence-proportional result (PT 2.15x / AO 1.42x / SH 1.28x) confirms the effect is specific to the hardware traversal unit's idle-lane problem.

**Hardware change or software mapping?** **HARDWARE CHANGE, with no software surface at all** — a new per-SM Load Balancing Unit, two new warp-buffer fields, `min_thit` OR-merge logic and a multiplexor/crossbar network; "transparent to the software", "requires no changes to the programming model" [paper]. Among the cluster's hardware papers this is the one with the smallest programmer-visible footprint.

**Simulated or measured?** **SIMULATED** — Vulkan-sim 2.0, `SM75_RTX2060` configuration (Turing, 1st-generation RT cores), LumiBench at 256x256 (two scenes at 128x128), 1 spp. Area figures (13,347 um^2 full-warp) are synthesis estimates; power and EDP are model output. No real GPU SKU was executed.

verdict_basis: The contribution is a load-balancing unit and datapath added inside the GPU ray-tracing unit, operating on its per-thread hardware traversal stacks, warp buffer and closest-hit registers. Its benefit is measured as recovered RT-unit lane utilisation (30.5% to 94.6% on one scene) — a quantity that only exists because a GPU RT unit schedules rays at warp granularity.

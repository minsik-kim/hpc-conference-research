# GPU-MICRO24-123 — LIBRA: Memory Bandwidth- and Locality-Aware Parallel Tile Rendering

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — graphics fixed-function pipeline microarchitecture (rasteriser/ROP replication and scheduling), rendering-pipeline branch`
secondary_topics: `mobile GPU / Tile-Based Rendering; memory-bandwidth scheduling; cache locality; energy efficiency`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via institutional repository PDF (upcommons.upc.edu/bitstream/handle/2117/426555/LIBRA_MICRO_2024_camera_ready.pdf) — introduction/motivation and Figure 1 raster/geometry split, Figure 3 baseline TBR pipeline and its fixed-function blocks, Table I baseline configuration, the dual-Raster-Unit design, the temperature-based tile scheduler and supertile mechanism, Figure 10 adaptive decision logic, evaluation setup and the 32-game benchmark set, Figures 11-19 results/ablations/sensitivity, related-work novelty claims. Explicit targeted check for non-graphics/general-purpose compute claims: none found.`

## 12.1 Bibliographic facts

- Title: **LIBRA: Memory Bandwidth- and Locality-Aware Parallel Tile Rendering** [paper]
- Venue: **MICRO 2024**, session **7B GPU Microarchitecture II** [official-program, census `MICRO_2024.md` row 17] — the same session as `GPU-MICRO24-121` (HSU) and `GPU-MICRO24-122` (TTA).
- Authors and affiliations [paper]: **Aurora Tomás** (UPC), **Juan L. Aragón** (Universidad de Murcia), **Joan-Manuel Parcerisa** (UPC), **Antonio González** (UPC).
- DOI: **`10.1109/MICRO61859.2024.00081`** [publisher-proceedings, census].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

In a Tile-Based Rendering mobile GPU, throwing more shader cores at one Raster Unit does not help because the raster pipeline is fed one tile at a time — so can the raster pipeline itself be **replicated** (two Raster Units of four cores instead of one of eight) and then scheduled so that a **memory-hot** tile and a **memory-cold** tile are always in flight together, spreading DRAM demand in time instead of stacking it into peaks?

## 12.3 GPU/HPC problem translation

- **Compute.** The raster process consumes **88%** of execution time in the baseline, geometry the rest [paper, Figure 1]. Adding cores to a single Raster Unit under-utilises them when a tile does not contain enough work.
- **Memory.** This is the paper's centre of gravity. Parallel tile rendering means "more cores are sending requests in parallel, which may lead to a memory bottleneck" [paper]. Note the design goal precisely: **temporal smoothing, not reduction** — main-memory access counts are essentially unchanged (up to 20% for one game) [paper].
- **Synchronization.** Each Raster Unit gets its **own** Early Z-Test, Rasterizer, Blending unit, Color Buffer, Z-Buffer and texture caches; only L2 and the memory controller are shared [paper]. That replication is what removes the cross-tile ordering constraint.
- **Scheduling.** Two scheduling decisions: **which tiles run concurrently** (hot/cold pairing) and **in what spatial order** (Z-order within supertiles). Both are adaptive per frame.
- **Communication.** Single-GPU mobile part. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

The baseline TBR pipeline, with its fixed-function blocks named as the paper names them [paper, Figure 3]:

- **Geometry pipeline**: Vertex Fetcher → Vertex Stage → Primitive Assembly → Clipping & Culling.
- **Tiling engine**: **Polygon List Builder** (bins primitives into tiles) → **Tile Fetcher** (retrieves per-tile primitive lists from the **Parameter Buffer**).
- **Raster pipeline**: **Rasterizer** (determines overlapped pixels, emits fragments/quads) → **Early Z-Test** (against a tile-sized on-chip **Z-Buffer**) → **Fragment Stage** (shader cores) → **Late Z-Test** (if depth writes occur) → **Blending Unit** (tile-sized on-chip **Color Buffer**) → **Flushing Unit** (writes the Color Buffer out to the Frame Buffer in main memory).
- **Memory hierarchy**: private L1s (Vertex, Tile, per-core Texture caches), shared L2, LPDDR4 main memory.

The root cause is structural: the **tile-sized on-chip Z-Buffer and Color Buffer are what make TBR bandwidth-efficient in the first place**, and they are per-Raster-Unit resources. One Raster Unit therefore means one tile in flight, and a tile that is memory-hungry monopolises DRAM while its cores idle. Replicating the Raster Unit replicates those buffers — which is why the design costs area in fixed-function blocks, not in shaders.

## 12.5 Mathematical / performance model

- **Tile temperature** [paper]: a tile is classified **hot** or **cold** by its **ratio of DRAM accesses to instruction count**, predicted from the **previous frame's statistics** — i.e. the model is frame-to-frame coherence, not a within-frame estimate.
- **Scheduling rule**: alternately assign hot and cold tiles to the two Raster Units, so that two high-demand tiles are never co-resident [paper].
- **Supertiles** [paper]: tiles are grouped into **2x2, 4x4, 8x8 or 16x16** blocks; within a supertile, Z-order traversal is preserved, which is what keeps texture locality from being destroyed by the temperature ordering. Supertile size is **re-chosen per frame** against a performance-variation threshold of **0.25%**.
- **Adaptive ordering** [paper, Figure 10]: fall back to plain Z-order when the **texture cache hit ratio exceeds 80%**, or when the performance change exceeds **3%**; otherwise use the temperature-aware order.
- **Scaling rule for more units** [paper, Figure 18]: **1 Raster Unit for hot tiles, the remainder for cold tiles.**

## 12.6 Data layout and ownership

- **primitive → tile**: Polygon List Builder writes per-tile primitive lists into the **Parameter Buffer** in main memory; the Tile Fetcher reads them back [paper].
- **tile → Raster Unit**: a tile is owned end-to-end by one Raster Unit, including its on-chip Z-Buffer and Color Buffer; the Flushing Unit writes the Color Buffer to the Frame Buffer [paper].
- **tile → supertile**: 2x2 … 16x16 groups, Z-ordered internally [paper].
- **statistics**: a **~4 KB on-chip buffer** holds per-supertile DRAM-access and instruction counts, plus **a simple FSM** for the decision logic; total **less than 0.2% of the L2 area** [paper].
- **frame N-1 → frame N**: the temperature prediction crosses frames. This is the design's only cross-invocation state and its main fragility.
- **GPU → node → cluster**: not applicable, mobile single-GPU. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- per frame, adaptive ordering decision (Figure 10) ----          [paper]
if texture_cache_hit_ratio > 0.80:            order = Z_ORDER
elif abs(perf_change) > 0.03:                 order = toggle(order)
else:                                         order = TEMPERATURE_AWARE

if perf_variation < 0.0025:                   supertile_size = grow(supertile_size)
else:                                         supertile_size = shrink(supertile_size)

# ---- tile dispatch ----                                             [paper]
for supertile in traverse(frame, order):
    for tile in z_order(supertile):
        temp = hot_or_cold(prev_frame_stats[tile])   # DRAM accesses / instructions
        unit = RASTER_UNIT_0 if temp == HOT else RASTER_UNIT_1
        dispatch(tile, unit)     # alternate so a hot and a cold tile are co-resident
```

The 0.80 / 0.03 / 0.0025 thresholds, the DRAM-accesses-per-instruction temperature metric, the supertile sizes and the "1 unit for hot, rest for cold" scaling rule are the paper's [paper]; loop structure and helper names are `[reconstruction]`.

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact located. The evaluation infrastructure is named in the paper [paper]: **TEAPOT**, a cycle-accurate mobile-GPU simulator framework, with **McPAT** for energy and **DRAMsim3** for DRAM timing/energy. No source symbols are asserted.

## 12.9 Kernel execution

There is no CUDA kernel here — the unit of work is a **tile**, dispatched through a fixed-function raster pipeline. The relevant hierarchy is frame → supertile → tile → quad/fragment → shader-core thread. The architectural change is one level above the shader core: the *pipeline that feeds* the shader cores is duplicated, and the scheduling decision (which tile goes where) is made by an FSM reading a 4 KB statistics buffer, not by a warp scheduler. This is precisely why the paper belongs in category Q's rendering-pipeline branch: the contribution lives in fixed-function graphics hardware and its scheduler.

## 12.10 Memory traffic

- **Main-memory accesses: essentially unchanged** — "No significant reduction (up to 20% for CCS), as design goal is temporal smoothing, not reduction" [paper]. This is the most important and most easily misquoted result in the paper.
- **Texture latency: 13.5% average reduction** (up to 40% on some apps) [paper].
- **Texture cache hit ratio: +10.6% average** (up to +40%) [paper].
- **L1 block replication: 32.5% average reduction** versus naive parallel tile rendering — i.e. the supertile mechanism is specifically repairing the duplication that replicating the Raster Unit would otherwise cause in the per-core texture caches [paper].
- L2/DRAM byte-level breakdown: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

All results are **simulated in TEAPOT + McPAT + DRAMsim3** on a modelled **ARM Valhall-like mobile GPU**: **800 MHz, 1 V, 22 nm, L2 2 MB 8-way 18-cycle, per-core texture cache 32 KB 4-way, LPDDR4 at 1.2 GHz with 50–100 cycle latency, Full HD 1920x1080 with 32x32-pixel tiles** [paper, Table I]. **No real GPU was measured.** Benchmarks: **32 commercial Android games** from Google Play (2D: Candy Crush Saga, Jetpack Joyride; 2.5D: Among Us, Hot Wheels Race Off; 3D: Subway Surfers, Counter Strike), 25-frame sequences, per-frame memory footprint 0.7–27.5 MB [paper].

The design is cleanly decomposed and the paper reports both halves [paper]:

| Component | Speedup | Energy reduction |
|---|---|---|
| **Parallel Tile Rendering alone** (2 Raster Units x 4 cores vs 1 x 8) | **13.2%** | **5.5%** |
| **+ temperature scheduler and supertiles** | **+7.7%** | **+3.7%** |
| **LIBRA total** | **20.9%** (FPS +11.4%; peak 44.5% on Candy Crush Saga) | **9.2%** (peak 20.5%) |

Within the scheduler's 7.7%, a further split [paper, Figure 16]: static supertiles alone give 0.6% / 2.1% / 2.8% / 3.2% for 2x2 / 4x4 / 8x8 / 16x16, while **dynamic supertile resizing gives ~7%** — the paper's conclusion is that roughly **half the scheduler benefit comes from dynamic sizing and half from the tile ordering**.

The negative control is convincing [paper, Figure 17]: on **compute-intensive, low-memory-activity games**, total speedup is 11.6% of which **PTR contributes 9.9% and the scheduler only 1.7%** — exactly as predicted if the scheduler's mechanism is DRAM-demand smoothing. The scheduler does not help when memory is not the bottleneck, and it does not hurt.

Scaling [paper, Figure 18]: **3 Raster Units → 31.3%**, **4 → 28.8%** — non-monotone, i.e. the design has a sweet spot and over-replication costs more than it buys.

## 12.12 Hardware generation dependence

- Modelled on a **modern ARM Valhall mobile GPU** at **22 nm**, **LPDDR4**, Full HD with 32x32 tiles [paper, Table I]. **No NVIDIA/AMD desktop part, no RT cores, no tensor cores** are involved anywhere in this paper.
- **Tile-Based Rendering is the architectural premise** — the paper states TBR is "the predominant architecture in mobile GPUs" [paper, quoted in census `MICRO_2024.md` §4]. On an immediate-mode desktop GPU without tile-sized on-chip Z/Color buffers, the replication argument does not transfer as stated. `[inference]`, flagged as such.
- **Simulation only**; energy is McPAT + DRAMsim3 modelling, **not measured power**.
- The design is generation-agnostic within TBR: nothing depends on a specific Valhall feature, only on the presence of a Raster Unit with tile-sized buffers. `[inference]`.

## 12.13 Limitations

The paper does not have a limitations section; the following are supported by its own text and results [paper], with inferences marked:
1. **Depends on frame-to-frame coherence** for temperature prediction; failure modes under scene cuts or fast camera motion are not quantified.
2. **Only the raster stage benefits** — geometry is the other ~12% of Figure 1's split.
3. **Mobile TBR scope only**; desktop/compute applicability is not evaluated.
4. **Temperature ordering fights locality by construction** — it deliberately co-schedules spatially distant tiles; supertiles are the repair, and two games (Gra, RoK) show only marginal scheduler gains in Figure 11.
5. **Non-monotone scaling** — 4 Raster Units are worse than 3.
6. `[inference]` Power-of-two supertile sizes are a coarse quantisation of a continuous locality/temperature trade-off.
7. `[inference]` The design assumes cold tiles exist; a uniformly hot frame has nothing to pair.

## 12.14 Relation to prior corpus

- **This is the cluster's pure-graphics anchor and its most important negative case for category Q.** Targeted check: **the paper makes no claim about general-purpose or non-graphics compute** [paper — verified by explicit query]. It repurposes nothing; it redesigns the graphics pipeline for graphics.
- **Same MICRO 2024 session (7B) as `GPU-MICRO24-121` (HSU) and `GPU-MICRO24-122` (TTA)** — which is itself evidence about how the community organises this material: the program committee placed "generalise the RT unit for search" and "replicate the raster unit for rendering" in one session called GPU Microarchitecture. The unifying object is the **fixed-function GPU pipeline**, not the application.
- **Novelty claims the paper makes** [paper]: "To the best of our knowledge, this is the first work exploring parallel tile rendering on GPUs" (multiple Raster Units in one Raster Pipeline), and "no previous studies have investigated the memory sensitivity of graphics applications… our work is the first to explore new policies on mobile GPUs for balancing the memory bandwidth". Recorded as the authors' claims, not verified here.
- **Author-level link to the memory-virtualisation cluster**: `_LEDGER_memory_virtualization.md` notes the ISCA 2026 duplication-centric multi-GPU memory-management paper shares an author trio with LIBRA. Recorded as-is from that ledger.
- **Complementary to** `GPU-HPCA25-126` (VR-Pipe): both modify fixed-function per-fragment hardware (LIBRA replicates the Raster Unit including Blending and Z; VR-Pipe adds early-termination and quad-merging logic to ZROP/CROP), but VR-Pipe does so to serve a **non-mesh, radiance-field workload**, which is the crossing point into category Q proper.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the raster/ROP hardware were replaced by ordinary SIMT cores?** No, and the reason is unusually concrete. The contribution *is* a fixed-function block-replication decision: two Raster Units, each with its **own Early Z-Test, Rasterizer, Blending Unit, tile-sized Color Buffer and Z-Buffer**. What that fixed-function hardware supplies that SIMT cores do not is (a) **the tile-sized on-chip Z/Color buffers** that make TBR bandwidth-efficient and that must be duplicated to run two tiles at once, (b) **the rasteriser's coverage determination and the ROP's ordered blend path**, and (c) **the Early-Z occlusion cull** that decides how much work a tile actually costs. The hot/cold metric itself — DRAM accesses per instruction, per tile, carried across frames — is only definable because a *tile* is the hardware's unit of work. On SIMT cores there are no tiles, no per-tile on-chip framebuffers, and nothing to replicate.

**Hardware change or software mapping?** **HARDWARE CHANGE** — structural replication of the Raster Unit, plus a ~4 KB statistics buffer and an FSM (together <0.2% of L2 area). No API or application change is required.

**Simulated or measured?** **SIMULATED** — TEAPOT with McPAT (energy) and DRAMsim3 (DRAM), modelling an ARM Valhall-like mobile GPU at 22 nm (Table I), over 25-frame traces of 32 Android games. Energy numbers are model output, not measured power. No real GPU SKU was executed.

verdict_basis: The contribution replicates and re-schedules the GPU's fixed-function raster pipeline — rasteriser, Early-Z, Blending Unit and the tile-sized on-chip Z/Color buffers of a Tile-Based Rendering mobile GPU — and its hot/cold metric is defined per tile, a unit that exists only because that hardware exists. Nothing in it is portable to a CPU or a generic accelerator.

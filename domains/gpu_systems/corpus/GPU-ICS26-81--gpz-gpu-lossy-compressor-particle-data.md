# GPU-ICS26-81 — GPZ: GPU-Accelerated Lossy Compressor for Particle Data

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `E HBM & data movement / GPU lossy compression`
secondary_topics: `E compression in the data path; B GPU kernel & memory-hierarchy design`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2508.10305v1) read in three targeted passes: (1) title/authors/abstract/introduction/motivation; (2) the four-stage pipeline design, register/occupancy/synchronization discussion, evaluation setup, throughput, ratio, ablation, limitations; (3) background and related work, venue and artifact status. No artifact repository is named in the paper and none was inspected.`

## 12.1 Bibliographic facts
- Title: *GPZ: GPU-Accelerated Lossy Compressor for Particle Data* `[paper]`.
- Authors and affiliations `[paper]`: Ruoyu Li, Zhuoxun Yang (Florida State University); Jinyang Liu (University of Houston); Guanpeng Li, Yafan Huang (University of Iowa); Sheng Di (University of Chicago / Argonne National Laboratory); Jiannan Tian (Oakland University); Hanqi Guo (The Ohio State University); Kai Zhao, Longtao Zhang (Florida State University); Jiajun Huang (UC Riverside); Xin Liang (University of Kentucky); Franck Cappello (University of Chicago / Argonne National Laboratory).
- Venue: **ICS 2026**, session S14 "Data Analytics & Compression", per `domains/gpu_systems/census/ICS_2026.md` row 16 `[census]`. **The paper text itself does not state a venue** `[paper]` — the ICS 2026 assignment rests on the census row, which rests on the official program.
- arXiv 2508.10305 (v1 read). Publication type of the read source: `PREPRINT`.
- Artifact: **none named in the paper** `[paper]`. `NOT_INSPECTED`.
- Note on the author set: this is largely the **cuSZ/cuSZp/cuSZ-i community itself** (Di, Cappello, Tian, Huang×2, Liu, Zhao, Liang) — GPZ is an in-family branch into a data type the family's structured-grid predictors do not fit, not an outside challenger.

## 12.2 Core question (one sentence)
Can an error-bounded lossy compressor for *irregular particle* data reach near-HBM-bandwidth throughput on a GPU, given that particle data lacks the spatial coherence that structured-grid predictors (Lorenzo, interpolation) rely on and that the ratio-improving steps used by cuSZ and cuSZ-i are exactly the steps that do not parallelise? `[paper]`

## 12.3 GPU/HPC problem translation
- **Compute**: quantization and a per-block sort. The sort is the unusual element — GPZ buys compressibility by *reordering* rather than by predicting.
- **Memory**: the dominant axis. The paper's own ablation attributes a 1.6× throughput difference to coalescing alone, and the final stage is explicitly measured against peak HBM bandwidth.
- **Synchronization**: the design's stated differentiator. Variable-length block outputs must be compacted, and GPZ removes inter-block synchronization from the critical path where its predecessor used `__threadfence()`.
- **Communication**: single-GPU. No multi-GPU or interconnect element.
- **Scheduling**: occupancy is managed explicitly via `-maxregcount` per GPU SKU.

## 12.4 Why the problem exists
Root causes the paper names `[paper]`:
1. **Particle data is intrinsically less compressible by correlation.** "Particle datasets typically exhibit nonuniform distributions and limited spatial and temporal coherence"; "Lossy schemes often exploit spatial or temporal correlation, but such correlation is limited in particle data compared to structured meshes."
2. **CPU-shaped pipelines do not map.** "Traditional compression methods optimized for sequential CPU pipelines fail to leverage the massive, fine-grained parallelism and specialized memory hierarchies on GPUs."
3. **The ratio/throughput trade-off has a named hardware mechanism.** "Complex decorrelation schemes can enhance compression ratios but incur throughput degradation due to **additional data transfers, synchronization barriers, and increased register pressure**." This is the cleanest statement in the cluster of *why* high-ratio GPU compression is slow, and all three terms are GPU-hardware terms.
4. **The specific indictment of the ratio branch.** cuSZ and cuSZ-i "add sophisticated steps, such as huffman coding and cubic interpolation prediction, to increase the compression ratios. However such steps **either require CPU-side processing or cannot be fully parallelized**, which severely degrade the performance in practice." The "require CPU-side processing" clause is a direct hit on cuSZ-i's ~200 µs CPU codebook build (see `GPU-SC24-81` §12.11).

## 12.5 Mathematical / performance model
No closed-form model. The quantitative design objects `[paper]`:
- Quantization maps a coordinate to a segment identifier and offset: `m·segId + segOffset = (p − boundary.min)/(2×eb)` applied per axis, then linearized. `eb` is the user error bound; the `2×eb` denominator is the standard error-bounded quantization interval.
- Shared-memory budget: **7.36 KB** per block for 32-bit intermediates, **11.36 KB** for 64-bit.
- Register cap: **168 registers/thread on RTX 4090 and L4, 128 on H100**, set via `-maxregcount`.
- Sort granularity: **32 points per thread**, chosen for "optimal balance of compression ratio and processing speed".
- The one measured bandwidth figure: compaction reaches **809 GB/s on RTX 4090** against that card's **1008 GB/s** peak — ~80%.

## 12.6 Data layout and ownership
- **particle → block**: particles are divided into fixed-size blocks; **one CUDA thread block per particle block, with 32 threads — i.e. one warp per block** `[paper]`. The paper's justification is that "one warp per block mapping ensures high GPU occupancy". This is the same single-warp-block choice as cuSZp (`cmp_tblock_size = 32`, "Fixed to 32, cannot be modified") `[code]` — an inherited family convention.
- **thread → points**: 32 points per thread in the sort stage.
- **warp**: the min/max reduction is two-stage — "first within each thread, then across threads in a warp" using `__shfl_down_sync` `[paper]`. Register-level, no shared memory.
- **block → shared memory**: shared-memory footprint is *adjusted at runtime* based on the maximum segment-ID bit-width, deliberately kept small so as to "enlarge the effective L1 cache" `[paper]`. This is an explicit trade of occupancy-limiting scratchpad against L1 capacity, a GPU-specific tuning axis with no CPU analogue.
- **grid → global**: variable-length per-block outputs, resolved by a device-level prefix-sum kernel and a final copy.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only stage names and primitives the paper prints `[paper]`:
```
# ---- Stage 1: Spatial Quantization ----   (1 warp per particle block)
per-thread min/max over its points
warp min/max reduction via __shfl_down_sync          # registers only
for each axis:  m*segId + segOffset = (p - boundary.min) / (2*eb)
linearize (segId_x, segId_y, segId_z) -> segId

# ---- Stage 2: Spatial Sorting ----
cub::BlockRadixSort over (segId) within the block only    # no global sort
    # 32 points per thread; shared-memory footprint sized by max segId bit-width

# ---- Stage 3: Encoding ----
run-length coding:
    (a) detect transition flags with warp primitives
    (b) prefix-sum -> pointer construction
    (c) parallel slot writing
delta coding over the unique sorted segment IDs
bit-plane / fixed-length coding: strip leading zeros

# ---- Stage 4: Compacting ----
(1) warp/block writes its variable-length output to global memory
(2) a SEPARATE device-level prefix-sum kernel computes global offsets
(3) a final copy kernel moves data to its offset
# NOTE: this is a 3-kernel decomposition, NOT a fused single kernel with
#       decoupled look-back. The paper's stated reason: it "eliminates
#       inter-block synchronization from the critical execution path",
#       unlike a predecessor that used __threadfence().
```

## 12.8 Real implementation
**No repository is named in the paper** `[paper]`. `NOT_INSPECTED` — no GPZ source was read and no GPZ symbol is asserted here.
The only library symbol the paper itself prints is **CUB's `BlockRadixSort`** and the CUDA intrinsics `__shfl_down_sync` / `__shfl_sync` / `__syncthreads` / `__threadfence` (the last two in the negative, as things GPZ avoids) `[paper]`. The compiler flag `-maxregcount` is named with its per-SKU values `[paper]`.
Cross-reference `[code]`: the `__threadfence()`-based single-kernel compaction GPZ is reacting against is readable in `github.com/szcompressor/cuSZp` @ `16e164762fe67785f498a44bae7984058a7a6952` (the cuSZp2 tag), `src/cuSZp_kernels_f32.cu:186-239`, where a decoupled-look-back chained scan uses `flag[warp]` with status values 1 and 2 separated by `__threadfence()`. GPZ does not name cuSZp2's mechanism in this text, so the identification of "predecessor using `__threadfence()`" with cuSZp2 is `[inference]`, well-supported but not paper-asserted.

## 12.9 Kernel execution
- **kernel count**: at least four stages, with compaction alone decomposed into three kernels (write / device prefix-sum / copy) `[paper]`. GPZ is therefore explicitly **not** a single fused kernel — a deliberate reversal of the cuSZp lineage's defining choice.
- **thread block**: 32 threads = 1 warp.
- **warp**: all intra-block reduction and communication is warp-level. The paper states the rule directly: "Eliminate most uses of `__syncthreads()` when assigning values to shared memory" and use `__shfl_sync` instead for "direct register-level communication". With a 32-thread block, `__syncthreads()` is redundant with warp-implicit synchrony, so this is a correctness-preserving removal — but the paper frames it as a throughput optimization.
- **instruction**: two named instruction-level optimizations `[paper]` — (i) **division/modulo elimination**, "80% instruction reduction via bitwise ops", and (ii) FMA use and scheduling to reduce warp divergence; loop unrolling applied only to loops under 32 iterations "to reduce branch divergence and increase instruction-level parallelism while controlling register usage".

## 12.10 Memory traffic
- **Stage 1–3** operate on a block resident in registers plus a small shared-memory workspace (7.36/11.36 KB). Keeping that footprint small is justified in L1-capacity terms, not occupancy terms.
- **Stage 4** is the traffic-dominant stage and the only one the paper characterises in bandwidth terms: **809 GB/s measured on RTX 4090 (peak 1008 GB/s)**, i.e. ~80% of peak `[paper]`.
- **Coalescing** is quantified: memory coalescing gives "1.6× throughput gain vs. strided access" (Table 3) `[paper]`.
- **What the throughput is bounded by**: **partially established, and this is the strongest evidence in the cluster.** For the compaction stage the paper gives an achieved-vs-peak HBM bandwidth figure (809/1008 GB/s on RTX 4090) and frames the whole design as approaching the memory-bandwidth roof. For the end-to-end pipeline it does **not** give an achieved-bandwidth figure, so the claim "GPZ is HBM-bandwidth-bound end to end" is `[inference]`, not `[paper]`. Two corroborating structural facts: H100 (3.35 TB/s HBM) yields 616 GB/s compression / 1091 GB/s decompression while RTX 4090 (1008 GB/s) yields 598/651 — decompression scales with bandwidth (1091/651 ≈ 1.68 against a 3.3× bandwidth ratio) while **compression barely moves at all (616 vs 598)**, which indicates compression is *not* bandwidth-bound on H100 and has hit a different limit. The paper does not remark on this. Recorded as an open question, `UNKNOWN`.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Sorting substitutes for prediction.** Particle data has no exploitable stencil; GPZ instead makes it compressible by sorting within a block so that run-length and delta coding have something to bite on. The sort is `cub::BlockRadixSort` and is **block-local**, so it never needs a global sort.
2. **Compaction off the critical path.** Splitting the variable-length compaction into write → device prefix-sum → copy removes the inter-block dependency that a fused single-kernel decoupled-look-back scan creates. The cost is extra HBM traffic (the data is written twice); the benefit is that no block ever spins waiting on a predecessor's flag. GPZ pays bandwidth to buy away a synchronization stall — the exact inverse of cuSZp2's trade.
3. **Register-level everything.** Warp-only reductions via `__shfl_down_sync`, `__syncthreads()` removed, register count capped per SKU to avoid spills.
4. **Instruction-level arithmetic reduction**: division/modulo replaced with bitwise operations, an 80% instruction-count reduction in that path.
5. **Where it loses**: in three cases GPZ achieves **7–23% lower compression ratio than cuSZ**, while being **3–6× faster** `[paper]`.

Ablation, cumulative, **RTX 4090** `[paper]`: baseline **89 GB/s compression / 102 GB/s decompression** → all optimizations **588 / 656 GB/s**, i.e. ~6.6× and ~6.4×. This is a very large share of the result attributable to micro-optimization rather than to the algorithm.

Numbers with full qualifiers `[paper]`:
- Hardware: **RTX 4090 (24 GB, 1008 GB/s, 128 SMs, 2520 MHz)**, **H100 SXM (80 GB, 3.35 TB/s, 132 SMs, 1980 MHz)**, **L4 (24 GB, 300 GB/s, 58 SMs, 2040 MHz)**.
- Datasets: **USGS/3DEP 734M particles; OuterRim (HACC) 84M; NewWorlds (HACC) 144M; WarpX 273M; LAMMPS 67M; XGC Poincaré 13M**.
- Error bounds: **1e-4, 1e-3, 1e-2**.
- Baselines: **cuSZp2, PFPL, FZ-GPU, cuSZ, cuSZ-i**.
- Throughput (average): **L4 169/181 GB/s; RTX 4090 598/651 GB/s; H100 616/1091 GB/s** (compression/decompression).
- Compression ratio at **eb 1e-2**: **USGS 219.42** (best baseline ~30.5); **OuterRim 219.41** vs 152.36 (PFPL); **NewWorlds 204.79** vs 81.30; **XGC Poincaré 42.32** vs 5.53.
- Headline: "up to 8× higher end-to-end throughput" while also improving ratio.

## 12.12 Hardware generation dependence
- Three SKUs across three tiers: **Ada consumer (RTX 4090), Hopper datacenter (H100 SXM), Ada datacenter-inference (L4)** — the widest SKU spread of any compressor in this cluster `[paper]`.
- Register cap is **SKU-specific** (168 on RTX 4090/L4, 128 on H100) `[paper]`, i.e. the tuning does not transfer across generations without re-tuning.
- The compression-vs-decompression scaling divergence on H100 (§12.10) means the design's headroom is generation-dependent in a way the paper does not analyse.
- No AMD or Intel GPU result. The design uses only portable primitives (warp shuffle, CUB radix sort, bitwise arithmetic) so a HIP port is plausible, but this is `[inference]`, not claimed.

## 12.13 Limitations
Author-stated `[paper]`:
1. Scope is the **particle position (coordinate) field** only, "rather than all attributes".
2. The ratio/throughput trade-off is acknowledged as fundamental; three cases give 7–23% lower ratio than cuSZ.
3. Future work is in-situ integration into simulation frameworks.

Baseline-robustness observations the paper reports, which are findings in their own right `[paper]`:
- "PFPL fails on datasets exceeding 2 GB"
- "**cuSZp2 produces verification errors on H100**"
- "FZ-GPU and cuSZ could not handle our largest files"
- "**cuSZ-i lacks 1D data support**"

Recorded additionally from this reading:
5. **No artifact.** For a paper whose result is ~6.6× from micro-optimizations, the absence of code is a serious reproducibility gap.
6. **No end-to-end achieved-bandwidth figure**; only the compaction stage is characterised against peak.
7. **The H100 compression plateau is unexplained** (§12.10).
8. **Venue is not stated in the paper**; ICS 2026 rests on the census row.

## 12.14 Relation to prior corpus
- `NO_EXISTING_ANALYSIS`. `[repo-grep]` hits for "GPZ" were confined to `domains/gpu_systems/census/ICS_2026.md`.
- **Competes with, and measures against, `GPU-SC24-81` (cuSZ-i)** — GPZ names cuSZ-i's CPU-side and non-parallelisable steps as the reason the ratio branch is slow, and reports that cuSZ-i cannot handle 1D data at all.
- **Inverts cuSZp2's core mechanism.** cuSZp2 fuses everything into one kernel and pays for it with a `__threadfence()`-separated decoupled-look-back chained scan `[code]`; GPZ un-fuses the compaction into three kernels specifically to take that dependency off the critical path. Both claim the same virtue (no synchronization stall) by opposite means.
- **Lineage from the paper's own citations** `[paper]`: cuSZ = "the GPU version of the SZ2 algorithm… lorenzo method for decorrelation and Huffman for coding"; FZ-GPU = "inspired by cuSZ… kernel fusion and replacing Huffman coding by bit shuffle"; cuSZ-i = "interpolation-based prediction to significantly improve compression ratio and quality over Lorenzo-based methods"; cuSZp2 = "an ultra-fast GPU error-bounded lossy compressor" with plain and outlier modes; PFPL = "bit-for-bit identical compressed streams on CPUs and GPUs". Also named but not evaluated: Draco, XTC, MDZ, LCP, SPERR.
- **No compression-in-collective work is cited.** A targeted pass found no gZCCL, hZCCL, ghZCCL or NCCL-compression reference `[paper]`. Combined with the same negative result for Aatrox (`GPU-ICS25-81`) and for cuSZ-i (`GPU-SC24-81`), and with `GPU-SC26-22` (NCCLZ) citing gZCCL/ghZCCL/COCCL but no standalone GPU compressor, this establishes the two lines as **separate citation communities despite overlapping authorship**.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** Every load-bearing element is a GPU-hardware artifact, and unusually the paper says so itself:
1. **The problem statement is GPU-hardware-specific.** The ratio/throughput tension is attributed to "additional data transfers, **synchronization barriers**, and **increased register pressure**" — a sentence that is meaningless on a CPU.
2. **One warp per thread block (32 threads)** is the unit of ownership, chosen for occupancy. The block-local `cub::BlockRadixSort` is only viable because a block is a warp and the sort stays in registers/scratchpad.
3. **Warp-shuffle min/max reduction** (`__shfl_down_sync`) and the deliberate removal of `__syncthreads()` in favour of `__shfl_sync` are register-file mechanisms with no CPU equivalent.
4. **Shared memory is deliberately under-allocated to enlarge the effective L1** — a trade that exists only where scratchpad and L1 share a physical SRAM, i.e. on NVIDIA SMs.
5. **The compaction redesign is purely about GPU block-scheduling semantics**: a decoupled-look-back scan makes block *k* wait on block *k−1*, which on a GPU risks deadlock-adjacent stalls under non-guaranteed co-residency; splitting into three kernels replaces that with two implicit grid-wide barriers. A CPU has no such hazard.
6. **Register capping via `-maxregcount`, per SKU**, to avoid spills without losing occupancy.

The qualification worth recording: the *algorithm* — quantize, sort, RLE, delta, bit-pack — would work on a CPU and would compress equally well. What would not survive is the throughput, and throughput is the paper's headline. That is exactly the strict-counterfactual boundary this cluster is meant to police, and GPZ falls on the CORE side because its ratio result also depends on GPU-shaped choices (block-local sort, block-sized run lengths).

verdict_basis: The design is organised end-to-end around warp-as-thread-block ownership, register-file communication, scratchpad-vs-L1 capacity trading, register-pressure caps, and the elimination of an inter-block scan dependency from the critical path — and the paper itself attributes the ratio/throughput tension to synchronization barriers and register pressure specifically.

## What the throughput is bounded by
**Partially established — the best-evidenced case in this cluster, but incomplete.** The compaction stage is measured at **809 GB/s against 1008 GB/s peak on RTX 4090 (~80%)**, so that stage is HBM-bandwidth-bound and the paper establishes it `[paper]`. End-to-end there is no achieved-bandwidth or roofline figure. Moreover the cross-SKU numbers contradict a simple bandwidth-bound story for compression: moving from RTX 4090 (1008 GB/s) to H100 (3.35 TB/s) raises decompression 651 → 1091 GB/s but compression only 598 → 616 GB/s, so **compression on H100 is bound by something other than HBM bandwidth — plausibly the block-local radix sort or register-pressure-limited occupancy — and the paper neither reports nor explains it.** `UNKNOWN`.

# GPU-PPoPP25-02 — Acc-SpMM: Accelerating General-purpose Sparse Matrix-Matrix Multiplication with GPU Tensor Cores

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `F — Tensor/Matrix cores; matrix units for non-GEMM kernels (sparse)`
secondary_topics: `sparse storage formats; reordering; asynchronous copy pipelines; load balancing`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML — introduction/motivation (three named obstacles), §3.1 overview and Figure 1 (four components), data-affinity reordering, BitTCF format, least-bubble double-buffer pipeline, adaptive sparsity-aware load balancing with the IBD metric, evaluation setup, results across three GPUs, per-component ablation, future work, related work.`

## 12.1 Bibliographic facts

- Title: **Acc-SpMM: Accelerating General-purpose Sparse Matrix-Matrix Multiplication with GPU Tensor Cores** [paper]
- Venue: **PPoPP 2025**, session "S8 Tensor Cores" [official-web: `https://ppopp25.sigplan.org/details/PPoPP-2025-Main-Conference-1/39/x`]
- DOI: `UNKNOWN` (census; `dl.acm.org` 403 from this environment)
- Publication type: `ARCHIVAL_MAIN_PAPER`; arXiv:2501.09251 is a `PREPRINT` of the same work
- Authors [paper]: **joint first authors Haisha Zhao and San Li**; corresponding author **Jue Wang**. Affiliations as listed: Computer Network Information Center, Chinese Academy of Sciences (Beijing); University of Chinese Academy of Sciences (Beijing); Renmin University of China (Beijing); Hangzhou Dianzi University (Hangzhou, Zhejiang) [paper].
- Full text used: `https://arxiv.org/html/2501.09251v1` [paper]
- Artifact: **no repository URL is provided in the paper** [paper — verified by targeted query]; census records `NOT_FOUND_AFTER_SEARCH`. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Tensor Cores are dense units and sparse matrices are not; rather than attacking one mismatch, can a *general-purpose* SpMM be built by simultaneously fixing the storage format, the block density (via reordering), the memory pipeline, and the load imbalance — so that Tensor Cores stay fed across arbitrary SuiteSparse matrices rather than only on graph-shaped ones?

## 12.3 GPU/HPC problem translation

The paper states three obstacles, which map directly onto the GPU resource axes [paper]:

- **Memory (format).** Existing sparse formats have "either low compression efficiency or high overhead"; the irregular access they induce into the dense matrix reduces both TC block density and locality.
- **Compute (unit mismatch).** "TCs are designed to operate on dense data, which may not be a natural match for sparse data operations." Reordering can raise block density but its own cost must be balanced against the gain.
- **Scheduling / pipeline.** "Current memory access optimization methods are relatively simple and inefficient, often characterized by low memory bandwidth or lots of pipeline bubbles" — Tensor Cores idle during global-memory access.
- **Synchronization.** The pipeline uses `cp.async` with `WaitGroup()` synchronisation and transaction barriers [paper].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- **Fixed dense MMA tile.** The `m16n8k8` MMA consumes a dense 8×8 sub-tile of the sparse operand regardless of how few non-zeros it holds; TC block *density* is therefore the direct determinant of useful FLOP fraction. Reordering exists solely to raise that density.
- **Operand-slot asymmetry, again.** The paper performs a "swapped mma" — swapping left- and right-hand matrices "for improved partitioning into 8×8 TC blocks" [paper]. This is the *same* structural observation as FlashSparse's swap-and-transpose, reached independently in the same PPoPP session (see §12.14).
- **Asynchronous-copy latency must be hidden or the MMA pipe stalls.** The sparse kernel has three concurrent streams to fetch (sparse values, indices, dense matrix B), so a single-buffered `cp.async` pipeline leaves bubbles. Hence a "least bubble double-buffers pipeline" [paper].
- **Row-window work is power-law distributed.** Non-zeros per row window vary by orders of magnitude on real matrices, so a static TC-block→thread-block assignment leaves SMs idle; hence the IBD-driven dynamic reallocation [paper].

## 12.5 Mathematical / performance model

- **BitTCF storage cost** [paper]: total storage is **`(⌈M/8⌉ + NumTCBlock × 11 + 2) × 4` bytes**, where `M` is the number of rows. This is a closed-form model, which is why the 8-row window (`⌈M/8⌉`) is visible in it — the format is built around the 8-row TC block.
- **Compression result** [paper]: **16.12% higher compression ratio than CSR**. *Qualifier: the paper's matrix set, BitTCF vs CSR.*
- **Reordering complexity** [paper]: the data-affinity-based reordering is a **graph-modularity-based algorithm with O(n log n) complexity**.
- **Load-balancing model** [paper]: an **imbalance degree (IBD)** metric drives dynamic reallocation of TC blocks across thread blocks, in a performance model that "incorporat[es] write-back costs" — i.e. the model prices not just the compute imbalance but the cost of the extra output write-backs that splitting a row window incurs.
- No accuracy/error model; the arithmetic is TF32 MMA with FP32 accumulation, and no numerical analysis is presented. `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

**BitTCF format — four arrays** [paper]:
- `RowWindowOffset` — offset of the starting TC block per row window; **`⌈M/8⌉ + 1` elements**
- `TCOffset` — offset of the starting non-zero per TC block; **`NumTCBlock + 1` elements**
- `SparseAToB` — the original column indices; **`NumTCBlock × 8` elements**
- `TCLocalBit` — a **`uint64`** per TC block "to represent the local position of each nnz in each TC block, where 1 indicates a nnz and 0 denotes a zero element"

The `TCLocalBit` design is the crux: an 8×8 TC block has exactly **64 positions**, so a single `uint64` is an exact bitmap of the block's occupancy. The per-block cost is then `1 (uint64 = 2 words) + 8 (SparseAToB) + 1 (TCOffset) = 11` words, which is precisely the `NumTCBlock × 11` term in the storage model. **This is the clearest example in the cluster of a sparse format designed around a matrix instruction's tile size rather than around the matrix.** `[inference]` for the 8×8-and-64-bit correspondence being the design rationale; the `uint64` and the 11-word accounting are `[paper]`.

Ownership hierarchy:
- **thread / lane**: holds its `m16n8k8` TF32 fragment slice; decodes its position from `TCLocalBit`.
- **warp**: issues the swapped `m16n8k8` MMA over an 8×8 sparse TC block and the corresponding dense tile.
- **thread block**: owns a set of TC blocks, **dynamically reassigned** by the IBD-driven balancer; runs the double-buffered `cp.async` pipeline over sparse values, indices and dense B [paper].
- **SM / GPU**: three evaluated parts (§12.12).
- **node / cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- host preprocessing ----                                     [paper] §3.1
A_reord = data_affinity_reorder(A)          # graph-modularity based, O(n log n)  [paper]
BitTCF  = build_bittcf(A_reord)             # RowWindowOffset, TCOffset,
                                            # SparseAToB, TCLocalBit (uint64/block)
plan    = balance_by_ibd(BitTCF)            # imbalance-degree metric + write-back
                                            # cost model  [paper]

# ---- device kernel, per thread block ----
for stage in pipeline_stages(plan.my_tc_blocks):                  # [reconstruction]
    # least-bubble double buffer: three concurrent async streams   [paper]
    cp_async(buf[stage%2].valsA,  BitTCF.Values,     ...)
    cp_async(buf[stage%2].idx,    BitTCF.SparseAToB, ...)
    cp_async(buf[stage%2].tileB,  B, ...)
    WaitGroup(1)                                                   # [paper]
    blk = buf[(stage-1)%2]
    for tc_block in blk:
        mask = blk.TCLocalBit[tc_block]        # uint64 bitmap of the 8x8 block [paper]
        # "swapped mma": left/right operands exchanged for 8x8 partitioning  [paper]
        acc = mma_m16n8k8_tf32(frag_dense(blk.tileB),
                               frag_sparse(blk.valsA, mask), acc)
write_back(C, acc)                            # priced in the balancing model  [paper]
```

`pipeline_stages`, `frag_dense`, `frag_sparse`, `buf` are `[reconstruction]`; `cp.async`, `WaitGroup()`, `m16n8k8`, TF32, the swapped mma, the four BitTCF array names and `TCLocalBit`'s uint64 semantics are the paper's [paper].

## 12.8 Real implementation

`NOT_INSPECTED`. No repository URL in the paper [paper — verified]; census found none. No source symbols asserted.

Instruction-level facts from the paper [paper]:
- MMA shape **`m16n8k8`** as the primary configuration, with **`m16n8k4`** also mentioned as available; datatype **TF32** (with FP32 accumulation implied by the TF32 MMA contract).
- "Swapped mma" — left and right operands exchanged to partition into 8×8 TC blocks.
- **`cp.async`** for asynchronous global→shared transfers, with **`WaitGroup()`** synchronisation and transaction barriers.
- BitTCF builds on a prior format the paper calls **ME-TCF**, using `uint64` bit-packing.

## 12.9 Kernel execution

kernel → thread block (variable TC-block set, assigned by the IBD balancer; runs the double-buffered `cp.async` pipeline) → warp (issues swapped `m16n8k8` TF32 MMA) → instruction (`cp.async` + `WaitGroup` + `mma`, with `TCLocalBit` decode in the integer pipe). The distinguishing execution feature relative to FlashSparse is the **explicit software pipeline**: three async copy streams double-buffered against the MMA stream, whose purpose is to keep the Tensor Core issuing while the memory system works.

## 12.10 Memory traffic

- **Format footprint**: BitTCF is **16.12% more compressed than CSR** [paper]. The `uint64` bitmap replaces explicit per-non-zero local indices.
- **global → shared**: `cp.async` for three streams (sparse values, `SparseAToB` indices, dense B tiles), double-buffered to remove pipeline bubbles [paper].
- **Cache behaviour**: the paper reports **cache policy control** as an ablated component that "boosted L1/L2 hit rates" [paper] — the only paper in this cluster to name explicit cache-policy control as a component. The specific mechanism (e.g. `__ldg`/`discard`/`L2 persistence`/`cp.async` cache hints) was **not** identified in the text read — `UNKNOWN`.
- **Locality via reordering**: the data-affinity reordering "enhanc[es] TC block density and cache locality" [paper].
- No byte-level traffic counts. `NOT_IN_PAPER`.
- Multi-GPU: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Headline results, with hardware/baseline qualifiers** [paper]:
- Evaluation: **414 SuiteSparse matrices** plus **10 representative real-world (power-law / GNN) matrices**. Dense-matrix column counts **N = 128, 256, 512**, precision **TF32**. Baselines: **cuSPARSE** (the reference line), **TC-GNN-SpMM**, **DTC-SpMM**, **SparseTIR**, **Sputnik**, **cuSPARSELt**.
- **RTX 4090 (Ada Lovelace)**: average **2.52×** over cuSPARSE, max **5.11×** (for "type-2" matrices).
- **A800 (Ampere) 80 GB PCIe**: average **1.91×**, max **4.68×**.
- **H100 (Hopper) 80 GB SXM**: average **1.58×**, max **3.60×**.
- Part specifications as tabulated by the paper: RTX 4090 82.6 TFLOPS TF32 / 1008 GB/s; A800 156 TFLOPS / 1935 GB/s; H100 494.7 TFLOPS / 3.35 TB/s.

**The most informative pattern in these numbers is that the speedup over cuSPARSE *decreases* with newer, higher-bandwidth parts: 2.52× (RTX 4090, 1008 GB/s) → 1.91× (A800, 1935 GB/s) → 1.58× (H100, 3.35 TB/s).** `[inference]` This is consistent with Acc-SpMM's gains being substantially *memory-pipeline* gains: as HBM bandwidth rises relative to compute, there is less bubble to remove, and cuSPARSE's CUDA-core path suffers less. The paper does not offer this interpretation, so the attribution is inference — but the monotone trend across three parts is in the paper's own data.

**Per-component ablation** (H100, feature dimension 128) [paper] — note the paper reports these *qualitatively* per component rather than as isolated multipliers:
1. **BitTCF compression** — improved storage and reduced data movement.
2. **Data-affinity reordering** — enhanced TC block density and cache locality.
3. **Cache policy control** — boosted L1/L2 hit rates.
4. **Pipeline optimisation** — "greater impact on type-2 matrices through bubble reduction".
5. **Load balancing** — "significantly enhancing the model's accuracy and improving load balancing effectiveness".
**This is the paper's weakest evidential point**: five components are ablated but the ablation is reported without separated speedup multipliers in the text read, so the relative contribution of each cause cannot be stated. Contrast FlashSparse, which gives numeric per-component speedups. Recorded as a gap: **`PARTIALLY_QUANTIFIED_ABLATION`**.

## 12.12 Hardware generation dependence

- **Three generations measured, and the paper keeps them separate**: **Ada Lovelace (RTX 4090)**, **Ampere (A800 80 GB PCIe)**, **Hopper (H100 80 GB SXM)**. The A800 is the export-restricted A100 derivative; its 156 TFLOPS TF32 figure is as the paper tabulates.
- The mechanism uses only the **warp-level `mma.m16n8k8`** path plus **`cp.async`**, both available from **Ampere** onward. `cp.async` is an Ampere feature; on pre-Ampere parts the pipeline component would not exist.
- **No Hopper-specific features**: no `wgmma`, no TMA, no distributed shared memory / thread-block clusters. So the H100 result is a warp-level kernel on a warpgroup-capable part — `[inference]` part of why H100 shows the *smallest* relative gain.
- **Blackwell (`tcgen05`, TMEM)**: not evaluated. `NOT_IN_PAPER`.
- **Sparse Tensor Cores (2:4)** are **not** used — cuSPARSELt appears only as a *baseline*. Acc-SpMM runs dense MMA on 8×8 blocks. Do not classify it as structured-sparsity-hardware work.
- **No AMD CDNA (MFMA)**. `NOT_IN_PAPER`.

## 12.13 Limitations

Stated as future work by the paper [paper]:
1. "Reorder columns of the sparse matrix while simultaneously reordering rows of the dense matrix, further improving cache hit rates" — i.e. the reordering is currently one-sided.
2. "Optimize the implementation of reordering algorithm to reduce overhead" — the `O(n log n)` modularity reordering has a cost the paper wants to reduce.
3. DGL integration for practical GNN deployment is planned, i.e. **no end-to-end framework integration exists yet** (contrast FlashSparse, which reports DGL/PyG end-to-end numbers).
- `[inference]` The reordering is a preprocessing pass whose amortisation depends on how many SpMM calls reuse the same matrix; for a single SpMM it may not pay. The paper does not report reordering time against kernel time in what was read.
- `[inference]` `TCLocalBit`'s `uint64` exactly covers an 8×8 block; a different MMA tile size would need a different word width, so the format is tied to this instruction shape.
- The ablation is not numerically separated (§12.11). `PARTIALLY_QUANTIFIED_ABLATION`.

## 12.14 Relation to prior corpus

- **Same-session sibling and closest competitor**: `GPU-PPoPP25-01` (FlashSparse), also PPoPP 2025 "S8 Tensor Cores". **The convergent-evolution finding**: both papers independently identify that exchanging the MMA's left and right operands enables **8×8** rather than 16-row sparse blocking. FlashSparse calls it "swap-and-transpose" and derives it from `A×B = (BᵀAᵀ)ᵀ` with `n=8`; Acc-SpMM calls it a "swapped mma … for improved partitioning into 8×8 TC blocks". **Neither cites the other** (same submission cycle). They then diverge: FlashSparse invests in granularity + coalescing + a leaner format; Acc-SpMM invests in reordering + bitmap format + async pipeline + load balancing. Neither is a duplicate of the other, and the pair is the best available evidence that the `n=8` operand asymmetry was the field's obvious 2024/25 opportunity.
- **Direct precursors, cited and benchmarked** [paper]: **TC-GNN** ("first GNN framework on TCs"), **VectorSparse** ("evolution of Sputnik for locality"), **CLASP** ("column-vector pruning"), **Magicube** ("low-precision integer optimization"), **DTC-SpMM** ("previous state-of-the-art with reordering and pipelining"). BitTCF is stated to build on a prior format **ME-TCF**.
- **Positioning** [paper]: Acc-SpMM claims to combine "systematic optimizations across algorithm level, memory access patterns, and instruction-level parallelism that prior works left unexploited" — i.e. it positions as breadth, not a single insight.
- **Cross-venue note**: the census's IPDPS 2026 file records that a search for a Tensor-Core SpGEMM/SpMM paper at IPDPS 2026 surfaced Acc-SpMM as prior-venue work, confirming its role as a reference point.
- **Watchlist neighbours**: BRP-SpMM (IPDPS 2025), High Performance Unstructured SpMM Using Tensor Cores (SC 2024), Bridging the Gap between Unstructured SpMM and Structured Sparse Tensor Cores (SC 2025), Exploiting Efficient Mapping and Pipelined Execution for SpMV on Tensor Cores (PPoPP 2026), Uni-STC (HPCA 2026).
- Prior corpus check: in-repo hits for "Acc-SpMM" are in `domains/gpu_systems/census/PPoPP_2025.md` (its own census row) and `domains/gpu_systems/census/IPDPS_2026.md` (a cross-reference in a not-found note). `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: Three of the four components are defined by GPU matrix-unit and GPU-memory mechanics. The **BitTCF** format's `TCLocalBit` is a single `uint64` bitmap precisely because an `m16n8k8`-derived TC block has exactly 64 positions, and the whole storage model `(⌈M/8⌉ + NumTCBlock×11 + 2)×4` bytes is expressed in terms of the instruction's 8-row window. The **"swapped mma"** exists only to exploit the MMA operand slots' asymmetric extents so the sparse operand can be partitioned into 8×8 blocks. The **least-bubble double-buffer pipeline** is built on Ampere-and-later **`cp.async`** with `WaitGroup()` and transaction barriers, overlapping three async global→shared streams against warp-level MMA issue. Only the data-affinity reordering (graph modularity, `O(n log n)`) is device-agnostic in itself, and even its objective function — maximise 8×8 TC-block density — is defined by the matrix instruction's tile. On a CPU there is no fixed 8×8 matrix tile to densify, no `cp.async`/shared-memory staging to double-buffer, and no operand-slot asymmetry to swap.

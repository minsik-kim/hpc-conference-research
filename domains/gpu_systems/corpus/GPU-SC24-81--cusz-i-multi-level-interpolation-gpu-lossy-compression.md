# GPU-SC24-81 — cuSZ-*i*: High-Ratio Scientific Lossy Compression on GPUs with Optimized Multi-Level Interpolation

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `E HBM & data movement / GPU lossy compression`
secondary_topics: `E compression in the data path; B GPU kernel & memory-hierarchy design`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v3 (arxiv.org/html/2312.05492v3) read in three targeted passes: (1) title/authors/abstract/introduction/background; (2) design — G-Interp predictor, block & anchor structure, spline selection, auto-tuning, Huffman changes, Bitcomp-Lossless integration; (3) evaluation setup, results, ablation, limitations, related work. Plus artifact inspection of github.com/JLiu-1/cusz-I @ 91e1bc546716f436a7781a96a3034696d1dc85b1.`

## 12.1 Bibliographic facts
- Title: *cuSZ-i: High-Ratio Scientific Lossy Compression on GPUs with Optimized Multi-Level Interpolation* `[paper]`. The census row and the ACM/IEEE title render it `CUSZ-i`; the artifact README renders it `cuSZ-i`. Both recorded.
- Authors `[paper]`: Jinyang Liu, Jiannan Tian, Shixun Wu, Sheng Di, Boyuan Zhang, Robert Underwood, Yafan Huang, Jiajun Huang, Kai Zhao, Guanpeng Li, Dingwen Tao, Zizhong Chen, Franck Cappello.
- Affiliations `[paper]`: UC Riverside; Indiana University Bloomington; SKLP/ICT Chinese Academy of Sciences; Argonne National Laboratory; University of Iowa; Florida State University.
- Venue: **SC 2024**, DOI `10.1109/SC41406.2024.00019` `[census]`.
- arXiv 2312.05492 (v3 read).
- Artifact `[artifact]`: `github.com/JLiu-1/cusz-I` @ `91e1bc546716f436a7781a96a3034696d1dc85b1` — a **fork of pSZ/cuSZ**, self-described in `README.md` as "SC '24 Research Paper Snapshot" and "part of the research paper artifacts". A second artifact repo `github.com/jtian0/24_SC_artifacts` is named by the README for reproduction — `NOT_INSPECTED`.
- Publication type: `ARCHIVAL_MAIN_PAPER`; the read source is the `PREPRINT`.

## 12.2 Core question (one sentence)
Can the interpolation-based prediction that gives CPU compressors (SZ3/QoZ) their compression-ratio advantage over Lorenzo prediction be restructured so that it runs at GPU-competitive throughput, rather than at the ~0.23 GB/s of the CPU implementation? `[paper]`

## 12.3 GPU/HPC problem translation
- **Compute**: prediction is a stencil-like arithmetic pass; the CPU interpolator is sequential along each dimension, so the translation problem is *finding independent work* inside a dependency-carrying multi-level interpolation.
- **Memory**: the dominant constraint. Interpolation at stride 4/2/1 is a strided access pattern, which is the worst case for HBM coalescing; the design's chunk and thread-block shapes exist to fix this.
- **Synchronization**: interpolation levels are strictly ordered (finer levels read coarser-level reconstructions), so the design must express level ordering *within a thread block* and never across blocks.
- **Communication**: single-GPU. A distributed data-transfer case study (ThetaGPU ↔ Purdue Anvil, ~1 GB/s Globus) is the only multi-node element.
- **Scheduling**: a profiling/auto-tuning pre-pass chooses spline order and dimension order per dataset.

## 12.4 Why the problem exists
Root causes the paper names `[paper]`:
1. **Lorenzo prediction is inaccurate.** "the Lorenzo data predictor leveraged by CUSZ, cuSZp, and cuSZx have been proven to be inaccurate in many cases." Because GPU compressors adopted Lorenzo for its locality, their compression ratio is structurally capped.
2. **The gap is quantified**: cuSZ "has achieved the highest compression ratio among existing GPU-based compressors" but "typically only reaches about 10% to 30%" of CPU SZ3's ratio.
3. **Direct porting fails.** "CPU-based interpolation data predictors are slow (e.g., 0.23 GB/s) and cannot directly be ported to GPU platforms."
4. **The lossless stage is the second cap.** "Most high-ratio lossless encoders in existing error-bounded lossy compressors only show poor throughputs on GPU platforms"; "sophisticated dictionary-based encoders are either limited in throughput (e.g., GPU-LZ) or compression ratio on GPU."

The hardware root cause of (3), as the design makes explicit, is that a naive GPU interpolation has **non-coalescing loads/stores** at stride 4/2 and **dependent traversal stages** that would require inter-block synchronization if chunks were large. The paper's three named challenges are exactly "Non-coalescing", "Dependent traversal stages", and "Finer interpolation depends on coarser interpolation levels". `[paper]`

## 12.5 Mathematical / performance model
No closed-form throughput model. The quantitative design objects are `[paper]`:
- Four interpolation splines, printed with exact coefficients:
  - linear (2 neighbours): `p_n = 0.5·x_{n-1} + 0.5·x_{n+1}`
  - quadratic (3 neighbours): `p_n = -1/8·x_{n-3} + 6/8·x_{n-1} + 3/8·x_{n+1}`
  - cubic not-a-knot and cubic natural, with coefficients `(-1/16, 9/16, 9/16, -1/16)` and `(-3/40, 23/40, 23/40, -3/40)` respectively.
  > Caveat recorded verbatim: as rendered in the HTML, both cubic forms print `x_{n-3}` for the fourth term where a symmetric stencil would require `x_{n+3}`. This is treated as a rendering/typo artifact of the source and is **not** asserted as the paper's intended formula — `UNKNOWN`.
- An **error-bound reduction factor α**, set by a piecewise-linear function of the value-range-relative error bound ε: α = 2.0 for ε ≥ 1e-1, descending through 1.75 / 1.5 / 1.25 to α = 1.0 for ε < 1e-5, with linear interpolation inside each decade `[paper]`. **Confirmed at `[code]`**: `src/kernel/spline3.cu` declares exactly `a1=2.0; a2=1.75; a3=1.5; a4=1.25; a5=1; e1=1e-1; e2=1e-2; e3=1e-3; e4=1e-4;` inside the `intp_param.auto_tuning>0` branch of `spline_construct`.
- **Anchor density**: "approximately 1 of 512 elements becomes anchor points to preserve" in 3D `[paper]` — i.e. the storage overhead of breaking the cross-chunk dependency is ~0.2%.

## 12.6 Data layout and ownership
- **element → chunk**: 3D `8×8×8`; 2D `16×16`; 1D `512` elements `[paper]`.
- **chunk → thread block**: "A thread block corresponds to four basic blocks of 8×8×8 elements", giving the `32×8×8` data footprint per block `[paper]`. **Confirmed at `[code]`**: the compression kernel is `cusz::c_spline3d_infprecis_32x8x8data` and the decompression kernel `cusz::x_spline3d_infprecis_32x8x8data` (`src/kernel/detail/spline3.inl:83,106`); `spline_construct` in `src/kernel/spline3.cu` builds `grid_dim = dim3(div(l3.x, BLOCK*4), div(l3.y, BLOCK), div(l3.z, BLOCK))` with `constexpr auto BLOCK = 8`, i.e. one block per 32×8×8 region.
- **shared-memory workspace**: the paper says each block works over "9×9×9 elements in total" (the 8³ chunk plus a borrowed halo of anchors). **At `[code]` the actual declaration is wider and padded**: `__shared__ struct { T data[9][9][33]; T ectrl[9][9][33]; } shmem;` (`spline3.inl:1402-1405`), i.e. `9×9×33` for both the data and the quant-code (`ectrl`) planes — the `33` rather than `32` is a bank-conflict padding on the fastest-varying axis. The paper's "9×9×9" is the per-basic-block view; the code's `9×9×33` is the per-thread-block view covering four basic blocks. Both recorded; the code is authoritative.
- **block shape**: `DEFAULT_LINEAR_BLOCK_SIZE = 384` threads, flat, with grid-stride loops over `33*9*9` elements (`spline3.inl:50-52, 211, 281`) `[code]`. 384 threads = 12 warps; the comment at `:281` notes `NUM_ITERS = 33*9*9/LINEAR_BLOCK_SIZE + 1` = "11 iterations".
- **anchors**: one vertex per chunk is an anchor; "7 other anchor points…borrowed from the surrounding chunks" `[paper]`. Anchors are stored losslessly and are what makes each block independent.
- **outliers**: quant-codes outside the central range are gathered "using the stream compaction technique" `[paper]`; at `[code]` this is the `CompactVal`/`CompactIdx`/`CompactNum` triple passed into the kernel (`spline3.inl:1379-1391`) backed by `mem/compact.hh`.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only names that appear in the paper `[paper]` or the artifact `[code]`:
```
# ---- host, once per dataset ----
profile: c_spline3d_profiling_16x16x16data / c_spline3d_profiling_data_2   # [code] real kernel names
         # samples a 4x4x4 sub-grid (3D); 2 cubic-spline tests per dimension = 6 tests  [paper]
         -> per-dimension choice of cubic spline (lower interpolation error wins)
         -> dimension ordering: least-smooth dimension first, smoothest last
alpha  = piecewise_linear(eps)      # 2.0 .. 1.0   [paper][code]

# ---- device, compression ----
grid = (ceil(nx/32), ceil(ny/8), ceil(nz/8)); block = 384 threads     # [code]
kernel c_spline3d_infprecis_32x8x8data:
    load 9 x 9 x 33 data tile into __shared__ (padded 33)             # [code]
    load borrowed anchors from neighbouring chunks                     # [paper]
    for stride in (4, 2, 1):                                           # [paper]
        for dim in chosen_dimension_order:
            # all points on this level along this dim are independent
            predict with the selected spline; quantize against eb
            write quant-code to s_ectrl; reconstruct in place
        __syncthreads()      # level ordering is INTRA-block only
    gather |q| >= r  as outliers via stream compaction (CompactVal/Idx/Num)  # [code]

# ---- lossless stage ----
histogram  (histsp: thread-private p_hist[K], K = 2R+1, atomicAdd into __shared__ s_hist)  # [code]
Huffman codebook built on the CPU, ~200 us end-to-end                 # [paper]
Huffman encode on GPU
optionally: NVIDIA Bitcomp-Lossless as a second lossless pass          # [paper]
```

## 12.8 Real implementation
Artifact `github.com/JLiu-1/cusz-I` @ `91e1bc546716f436a7781a96a3034696d1dc85b1` `[code]`. Symbols verified by reading, not inferred:
- `src/kernel/detail/spline3.inl` — header credits "Jinyang Liu, Shixun Wu, Jiannan Tian". Kernels declared at `:62,69,83,106` and defined at `:1287,1332,1379,1479`:
  `cusz::c_spline3d_profiling_16x16x16data`, `cusz::c_spline3d_profiling_data_2`,
  `cusz::c_spline3d_infprecis_32x8x8data`, `cusz::x_spline3d_infprecis_32x8x8data`.
- `constexpr int BLOCK8 = 8; constexpr int BLOCK32 = 32; constexpr int DEFAULT_LINEAR_BLOCK_SIZE = 384;` (`spline3.inl:50-52`).
- Shared memory: `__shared__ struct { T data[9][9][33]; T ectrl[9][9][33]; } shmem;` (`spline3.inl:1402-1405`).
- Bounds predicate at `spline3.inl:157,160` uses `BIX*BLOCK32+x`, `BIY*BLOCK8+y`, `BIZ*BLOCK8+z` — direct evidence of the 32×8×8 block-to-data mapping.
- `src/kernel/spline3.cu` — `spline_construct(...)` with `INTERPOLATION_PARAMS &intp_param`; grid built as above; α table literal as above.
- `src/kernel/detail/histsp.cu_hip.inl` — the "thread-private buffer" optimisation the paper describes is real and readable: `template <typename T, typename FQ = uint32_t, int K = 5>`, `static_assert(K % 2 == 1)`, `constexpr auto R = (K-1)/2`, `FQ p_hist[K] = {0};` in registers, `extern __shared__ FQ s_hist[];`, and a single `atomicAdd(&s_hist[(int)offset + i - R], p_hist[i])` reduction at `:81`. The guard `if (2*abs(sym) < K)` at `:49` is exactly the "central top-k quant-codes" test.
- Portability: the tree carries `.cu_hip.inl` (CUDA/HIP), `.dp.inl` (SYCL/oneAPI) and `.seq.inl` (sequential) variants of every kernel, plus `detail/warp_compat.dp.inl` and `wave32.{cu_hip,dp}.inl`. **This is a portability-layered codebase, not CUDA-only** `[code]` — relevant to the counterfactual below.
- **Bitcomp/nvcomp**: a repo-wide grep for `bitcomp|Bitcomp|nvcomp` in this tree returned **no hits** `[code]`. The Bitcomp-Lossless second pass described in the paper is therefore **not present in this artifact snapshot**; it is presumably applied in the separate `24_SC_artifacts` repo or as an external library call. Recorded as `NOT_INSPECTED` / not-in-this-tree, **not** as absent from the work.

## 12.9 Kernel execution
- **kernel**: `c_spline3d_infprecis_32x8x8data` (compress) / `x_spline3d_infprecis_32x8x8data` (decompress), preceded by up to two profiling kernels launched on a `dim3(1,1,1)` grid (`auto_tuning_grid_dim` in `spline3.cu`) `[code]`.
- **thread block**: 384 threads (flat `LINEAR_BLOCK_SIZE`), covering a 32×8×8 data region = four 8×8×8 basic blocks `[code]`.
- **warp**: 12 warps per block. The paper's coalescing argument — organise "as 32 × 8 × 8 (x = 32)" — is precisely that the fastest-varying extent equals the warp width, so a level-0 load is one 32-lane contiguous request `[paper]`. No warp-level primitive (`__shfl`, ballot) appears in `spline3.inl`; the interpolation is shared-memory-mediated, not shuffle-mediated `[code]`.
- **instruction**: the `histsp` histogram is the one place with register-resident accumulation (`p_hist[K]` with `K = 5`) followed by a single shared-memory `atomicAdd` per bin `[code]`.
- **level ordering**: `__syncthreads()`-granularity inside a block. There is **no grid-wide synchronization and no cooperative-groups grid sync** — the anchor-borrowing scheme exists specifically so that levels can be ordered within a block only.

## 12.10 Memory traffic
- **HBM → shared**: one tile load of `9×9×33` `T` plus the anchor halo per block. The `33` padding avoids shared-memory bank conflicts on the x axis `[code]` `[inference]` for the *reason*; the padding itself is `[code]`.
- **inside shared**: all three interpolation levels (stride 4 → 2 → 1) run against `shmem.data` / `shmem.ectrl` without returning to HBM. This is the central memory-hierarchy claim: the multi-level dependency chain is resolved entirely in shared memory, at the cost of ~0.2% anchor storage.
- **shared → HBM**: quant codes (`ectrl`), anchors, and a compacted outlier list.
- **second pass**: histogram, then GPU Huffman, then (optionally) Bitcomp-Lossless — each an additional full read/write of a progressively smaller stream.
- **what the throughput is bounded by**: the paper does **not** establish a bound with a roofline or a bandwidth-utilisation measurement. What it reports is *relative*: on A100 at ε=1e-2, cuSZ-i compression runs at ~60% of cuSZ's rate and decompression at ~80–90%; on A40, ~70–80% and near-parity respectively `[paper]`. The structural reason given is that G-Interp does strictly more arithmetic and more shared-memory traffic per element than Lorenzo, and that the codebook build is a ~200 µs CPU excursion `[paper]`. So: **compression throughput is bounded by the predictor's shared-memory/arithmetic cost plus a fixed CPU codebook latency, not by HBM bandwidth — and the paper does not demonstrate this, it is `[inference]` from the reported ratios and the design.** This is a real evidentiary gap and is recorded as such.

## 12.11 Why it is faster/slower (decomposed cause)
cuSZ-i is deliberately **slower** than its GPU predecessors and buys compression ratio with that time.
- **Ratio gain, cause 1 — prediction accuracy.** Multi-level spline interpolation concentrates the quant-code histogram far more tightly than Lorenzo, which is what makes the subsequent Huffman stage cheap and the outlier list short. The paper states the effect as "a much smaller r• than Lorenzo" `[paper]`.
- **Ratio gain, cause 2 — a second lossless pass.** Huffman cannot go below one bit per symbol; a heavily concentrated symbol stream therefore still contains "continuous 0x00 bytes" of repeated-pattern redundancy that a pattern-cancelling coder can remove. Bitcomp-Lossless is that coder `[paper]`.
- **Throughput loss, cause 1 — more work per element**: three interpolation levels × three dimensions vs. one Lorenzo pass.
- **Throughput loss, cause 2 — a CPU excursion**: the Huffman codebook build was *moved off* the GPU to the CPU (~200 µs) `[paper]`. This is an unusual direction of travel and is a deliberate trade: the codebook is tiny and the GPU tree-build was evidently not worth its cost once the histogram became concentrated.
- **Throughput loss recovered, partly**: the `histsp` thread-private-buffer trick "significantly decreases the transaction between threads' register files and the shared memory buffer" `[paper]`, confirmed at `[code]` as `p_hist[K]` in registers with one `atomicAdd` per bin.

Numbers, each with its qualifiers `[paper]`:
- Hardware: **NVIDIA A100 80 GB (1555 GB/s, 19.49 TFLOPS)** and **NVIDIA A40 48 GB (695.8 GB/s, 37.42 TFLOPS)**, on ALCF ThetaGPU, Purdue RCAC Anvil and ANL-JLSE.
- Datasets: **JHTDB 512³ (5 GB, 10 fields), Miranda 256×384×384 (1 GB, 7), Nyx 512³ (3.1 GB, 6), QMCPack 288×115×69×69 (612 MB, 1), RTM 449×449×235 (6.5 GB, 37), S3D 500³ (5.1 GB, 11)**.
- Error bounds: value-range-relative **1e-2, 1e-3, 1e-4**.
- Baselines: **cuSZ, cuSZp, cuSZx, cuZFP, FZ-GPU**, with CPU **QoZ** as the quality reference.
- Compression ratio **without** Bitcomp-Lossless: **3.0–30.2×**, "10% to 30% advantages over the second-best".
- Compression ratio **with** Bitcomp-Lossless: **13.3–256.0×**, headline "**476% advantage over the second-best**" — this is the abstract's number and it is the *Bitcomp-enabled, low-bit-rate* case, not the predictor alone.
- Quality at matched ratio: **JHTDB 70.2 dB (cuSZ-i) vs ~62 dB (cuZFP) at CR≈27**; **S3D 81.3 dB vs 37.8 dB (cuZFP)** at the same ratio.
- Case study: ThetaGPU ↔ Purdue Anvil over Globus at ~1 GB/s, transfer time reduced **~30–40%** vs the second-best compressor at a target PSNR.

## 12.12 Hardware generation dependence
- Evaluated on **A100 and A40 only** — both Ampere. No Hopper, no Blackwell, no AMD, no Intel result is reported `[paper]`.
- The A100-vs-A40 pair is informative and the paper effectively uses it as one: A40 has ~45% of A100's HBM bandwidth but ~1.9× its FP32 throughput, and cuSZ-i's *relative* penalty against cuSZ is **smaller** on A40 (~70–80% vs ~60% on compression). That is consistent with cuSZ-i being more compute/shared-memory bound and cuSZ more bandwidth bound — but the paper does not draw this inference and no counter is reported, so it is `[inference]`.
- **Ecosystem dependence is author-acknowledged**: the lossless module "is partially dependent on the NVIDIA GPU ecosystem" `[paper]` — Bitcomp is an NVIDIA nvCOMP component and has no AMD or Intel equivalent.
- Against that, the artifact carries HIP and SYCL kernel variants throughout `[code]`, so the *predictor* is portable even though the *lossless second pass* is not.

## 12.13 Limitations
Author-stated `[paper]`:
1. "Compression speeds are slower than other GPU-based compressors."
2. "Interpolation-based prediction still has lower accuracy than CPU-based interpolators" — the GPU restructuring (small chunks, anchors) costs accuracy relative to SZ3/QoZ.
3. "Lossless module involves CPU and is partially dependent on the NVIDIA GPU ecosystem."
4. Huffman codebook building on the CPU adds ~200 µs.

Recorded additionally from this reading:
5. **No throughput-bound analysis.** Neither achieved HBM bandwidth nor occupancy nor a roofline is reported, so "what limits cuSZ-i" is not established by the paper.
6. **Ampere-only evaluation.**
7. **Bitcomp-Lossless is absent from the inspected artifact tree**, so the headline 476% figure is not reproducible from this snapshot alone.
8. The cubic-spline coefficient rendering in the HTML source is internally inconsistent (see 12.5) — flagged, not corrected.

## 12.14 Relation to prior corpus
- `NO_EXISTING_ANALYSIS` — repo-wide grep found cuSZ/cuSZp only in `domains/gpu_systems/census/SC_2024.md` (this project's own STEP A/B rows) and in a raw SC24 TOC dump under `domains/hpc_quantum/.../corpus/data/sc24_main.tsv` (existence evidence only). `[repo-grep]`
- **This is the ratio-side root of the cluster.** Its direct competitor within the same SC 2024 volume is **cuSZp2** (`10.1109/SC41406.2024.00021`; **no stable ID in this corpus** — the full-paper gate was not met, so it is a watchlist row in [`_LEDGER_data_movement_compression.md`](_LEDGER_data_movement_compression.md). An earlier draft of this file gave it `GPU-SC24-82`, which is held by Hydrogen; corrected 2026-09-19), which takes the opposite position on the same trade-off: cuSZ-i maximises ratio at ~60% of cuSZ's throughput; cuSZp2 maximises throughput. They are the two endpoints the 2025–2026 papers try to collapse.
- **Lineage established from the paper's own citations** `[paper]`: cuSZ [16,17] → cuSZx [18], FZ-GPU [19], cuSZp [20] as the speed branch; cuZFP [21] as the independent transform branch; MGARD-X CUDA backend [27] excluded for low throughput. On the CPU side SZ3 and **QoZ** ("the state-of-the-art CPU-SZ variant in terms of rate-distortion") are the quality references. The artifact README adds an author-authored family tree naming "cuSZ (Tian et al., '20, '21)", "FZ-GPU (Zhang, Tian et al., '23)", "SZp-CUDA/GSZ (Huang et al., '23, '24)", "cuSZ+ (hi-ratio) (Tian et al., '21)" and "QoZ-like methods (Liu et al., '22)" `[README]`.
- **The compression-in-the-collective line is absent.** Neither gZCCL/hZCCL/ghZCCL nor any NCCL-integrated compressor appears in the related work as read. Cross-checked against `GPU-SC26-22` (NCCLZ), which cites gZCCL/ghZCCL/COCCL but **not** cuSZ-i. On the evidence of both papers' reference lists these are **two separate communities** with overlapping author sets (Sheng Di, Franck Cappello, Jiajun Huang appear on both sides) but no citation traffic in either direction. Recorded as a finding, not as an assertion about intent.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** The contribution is not "interpolation compression" — that already existed on the CPU as SZ3/QoZ and is explicitly the starting point. The contribution is the *restructuring* of it, and every element of that restructuring is a GPU-hardware artifact:
1. **Chunking to 8×8×8 with borrowed anchors exists to avoid inter-block synchronization.** A CPU implementation has no such constraint — it interpolates the whole array level by level and needs no anchors at all. The ~0.2% anchor overhead and the accuracy loss versus SZ3 are the price of the GPU's lack of cheap global sync, and the paper names "dependent traversal stages" as one of its three challenges.
2. **The 32×8×8 thread-block shape is chosen so the fastest-varying extent equals the warp width**, making a strided interpolation level coalesce into full-width HBM transactions. `x = 32` is not a tuning constant, it is the warp.
3. **The whole multi-level dependency chain is resolved in shared memory** — `__shared__ T data[9][9][33]` with `33` padding for bank conflicts `[code]`. Fitting the working set in LDS is the design's load-bearing assumption; on a CPU the equivalent is a cache-blocking choice with no correctness consequence.
4. **The histogram optimisation is a register-file-vs-shared-memory trade** (`p_hist[5]` in registers, one `atomicAdd` per bin) `[code]` — meaningless without a register file that is per-thread and a shared scratchpad that is per-block.
5. **The Huffman codebook was moved to the CPU** precisely because a GPU tree build was not worth its cost — a GPU-specific negative design decision.

**Qualification, recorded honestly**: the artifact contains HIP and SYCL variants of every kernel `[code]`, so "GPU-specific" here means *SIMT-with-scratchpad-specific*, not CUDA-specific. The one genuinely NVIDIA-locked element is the Bitcomp-Lossless second pass, which is also the element responsible for the headline 476% figure.

verdict_basis: The design's every structural choice — anchor-based chunk independence to avoid grid-wide sync, `x=32` for warp-width coalescing, a padded shared-memory tile holding the entire level chain, register-resident histogram partials — is dictated by SIMT scratchpad hardware; the algorithm it starts from (SZ3/QoZ interpolation) is CPU work that the paper states cannot be ported directly.

## What the throughput is bounded by
**Not established by the paper.** `[inference]` from the design and the A100-vs-A40 relative results: shared-memory traffic and arithmetic in the three-level predictor, plus a fixed ~200 µs CPU codebook latency — not HBM bandwidth. The paper reports only ratios against cuSZ (A100: ~60% compression, ~80–90% decompression; A40: ~70–80%, near-parity) and never an absolute bandwidth utilisation, occupancy figure, or roofline.

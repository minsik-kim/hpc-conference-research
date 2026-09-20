# GPU-PPoPP26-01 — SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `F — Tensor/Matrix cores, numeric formats, precision emulation, matrix units for non-GEMM kernels`
secondary_topics: `G — scientific kernels on GPUs (stencil); sparsity / structured-sparsity metadata`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the arXiv HTML rendering of arXiv:2506.22035 — Introduction, Background and Motivation (incl. §2.3 redundancy quantification), System Design (§3.2.2 structured sparsification three steps; kernel/tiling/packing detail), Evaluation, Related Work, Conclusion. **IMPORTANT CAVEAT (see §12.1): the readable HTML is the v1/v2 text titled "SPTCStencil"; the v3 PDF carrying the "SPIDER" title did not render as HTML.** Ablation: NOT_IN_PAPER. Limitations: NOT_IN_PAPER (explicit section absent).`

## 12.1 Bibliographic facts

- Official (PPoPP 2026) title: **SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping** [official-web: `https://ppopp26.sigplan.org/details/PPoPP-2026-papers/4/x`, session "Stencil and Sparse Matrix Computation"]
- DOI: `10.1145/3774934.3786414` [official-web; corroborated by the arXiv `/abs/` page's DOI field]
- Authors: Qiqi Gu, Chenpeng Wu, Heng Shi, Jianguo Yao [official-web]. The preprint's own author block reads: Qiqi Gu (Shanghai Jiao Tong University), Heng Shi (Shanghai Enflame Technology Co. Ltd; SJTU), Chenpeng Wu (SJTU), Jianguo Yao (SJTU) [paper].
- Publication type: `ARCHIVAL_MAIN_PAPER` (PPoPP 2026); the arXiv item is a `PREPRINT` of the same work.
- **Version / title discrepancy, recorded explicitly.** arXiv:2506.22035 has three versions: v1 (2025-06-27), v2 (2025-07-07), v3 (2025-12-15) [official-web, `/abs/` page]. The `/abs/` page's current title is **SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping**, and its abstract names "ahead-of-time strided swapping applied to kernel matrices and runtime row-swapping for input data" and "6.20× outperformance over vendor library cuDNN and 2.00× over SOTA Tensor Core-based approaches" [official-web].
  The rendered HTML at `arxiv.org/html/2506.22035v3` serves a document titled **"SPTCStencil: Using Sparse Tensor Cores for Stencil Computation"**, whose abstract names the system SPTCStencil and reports the *same* numbers ("5.46× and Tensor Core-based approaches by 2.00× on average"; "SPTCStencil delivers average speedups of 6.20× over cuDNN") [paper]. A direct query confirmed the string "SPIDER" does **not** appear anywhere in the rendered HTML [paper].
  **Conclusion recorded:** the readable full text is the earlier, SPTCStencil-titled text of substantively the same work; the v3 PDF did not render. All content below is attributed to that readable text. The name "SPIDER" and the phrase "runtime row-swapping" are attributed to the `/abs/` metadata only. **Any claim that is v3-only has NOT been read.**
- Full text used: `https://arxiv.org/html/2506.22035v3` (served the SPTCStencil text) [paper]
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED` — no source code read.

## 12.2 Core question (one sentence)

The padding zeros that a stencil→GEMM lowering necessarily introduces have been treated as waste to be *minimised*; can they instead be treated as *exploitable structured sparsity*, so that NVIDIA's Sparse Tensor Core (which physically skips zeros under a 2:4 pattern) does the skipping in hardware?

## 12.3 GPU/HPC problem translation

- **Compute.** Prior Tensor-Core stencil systems all run a *dense* MMA over a matrix that is mostly padding. The paper quantifies the resulting waste for Box-2D3R, as a multiple of the theoretical-minimum computation: **ConvStencil ≈2.12×, LoRAStencil ≈2.94×, TCStencil ≈5.85×** [paper, §2.3]. *Qualifier: Box-2D3R stencil, ratio to theoretical minimum, the authors' own accounting.*
- **Memory.** The same padding is loaded from shared memory into registers and occupies fragment registers; the paper's packing optimisations target exactly that.
- **Synchronization.** The 2:4 sparse MMA requires a *compressed* value matrix plus a *metadata* matrix in a hardware-mandated per-thread register arrangement; producing both without a separate permutation pass is the coordination problem.
- **Scheduling.** Three-level tiling (block / warp / MMA) as in a dense GEMM kernel.
- **Communication.** Single-node, four A100 GPUs in the test platform but no inter-GPU mechanism described. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- The Sparse Tensor Core on Ampere and later accepts operands only in the **2:4 structured** form: at most two non-zeros in every contiguous group of four elements along the reduction dimension, with a 2-bit-per-element positional metadata encoding. Sparsity that is *present* but *not* in this form buys nothing [paper].
- A stencil lowered to matrix form produces a kernel matrix whose non-zeros are *strided*, not 2:4-conformant: the transformed kernel matrix has sparsity ratio `(2r+1)/(2r+L)` for radius `r` and reduction extent `L` [paper, §3.2.2 Step ①]. The pattern is regular but its stride does not align to the 4-element groups the hardware inspects.
- Therefore the hardware cannot skip the zeros, and every prior system paid for them densely. The root cause is the *granularity and alignment* of the sparse-MMA metadata contract, not the amount of sparsity.

## 12.5 Mathematical / performance model

- **Sparsity condition** [paper, §3.2.2 Step ①]: the transformed kernel matrix's sparsity ratio is `(2r+1)/(2r+L)`. To reach the ≥50% sparsity the 2:4 unit requires, the paper sets `L = 2r + 2` (even), which the authors describe as balancing sparsity exploitation against hardware utilisation.
- **Strided swapping (the transform)** [paper, §3.2.2 Step ②]: permute columns of the kernel matrix by swapping odd-indexed column `j` with column `j + (2r + 2)`, leaving even-indexed columns in place. The paper's claim: after this permutation "every contiguous 4-element segment contains at most two non-zero values, exactly satisfying the 2:4 sparse pattern required for SpTC acceleration."
- **Cost argument**: because the permutation acts on the *reduction* dimension, the corresponding input-side reordering can be folded into the address arithmetic of the load, so the paper claims a "zero-cost row swap strategy that guarantees correctness without introducing additional overhead" [paper].
- No closed-form throughput or error model is given. `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

- **thread**: for the `mma.sp` `m16n8k16` FP16 form, "each thread manages four `.f16` elements in two `.f16x2` registers" [paper]. The paper gives an explicit thread→row mapping for the input operand B:
  `offset_row = 2·(lane_id mod 4) + 4·i + (i mod 2)` [paper]
  and states that the row swap across successive SpTC invocations adds `+16·(−1)^k` for even-indexed elements `i` and `0` otherwise [paper]. *These are the paper's formulas as rendered; the index conventions for `i` and `k` were not fully legible in the fetched rendering — treat the exact indexing as `[paper]`-quoted rather than re-derived.*
- **warp**: owns a warp tile `A_w × B_w` in registers and issues the sparse MMA. Metadata is **packed across four consecutive MMA invocations** because the metadata operand is read by only a subset of lanes; concatenating four invocations' metadata means the otherwise-idle lanes' loads are not wasted [paper].
- **block/workgroup**: owns the block tile `A_b × B_b` staged from global to shared memory [paper, three-level tiling: block-level global→shared, warp-level shared→register, MMA-level register].
- **SM/CU**: A100 SM with dedicated Sparse Tensor Cores [paper].
- **GPU / node**: four A100-80GB PCIe in the platform; no multi-GPU algorithm. `NOT_IN_PAPER`.
- **Compressed-operand layout**: after strided swapping, the kernel matrix is compressed to (a) a **value matrix** holding the surviving non-zeros (the paper's worked example: "E0G0 becomes EG") and (b) a **metadata matrix** of 2-bit positions. Segments containing a single non-zero **keep one zero placeholder** in the value matrix so the compressed width is uniform [paper, §3.2.2 Step ③].
- **Kernel-matrix packing**: the kernel matrix is packed so that the non-contiguous fragment layout aligns with GPU cache lines, giving contiguous per-thread access [paper].

## 12.7 Pseudo code

```
# ---- ahead of time (host / compile time) ----
L = 2*r + 2                                          # [paper] Step 1
K_perm = swap_columns(K_matrix, odd j <-> j + (2r+2)) # [paper] Step 2, "strided swapping"
K_val, K_meta = compress_2to4(K_perm)                 # [paper] Step 3
K_val  = pack_for_cacheline(K_val)                    # [paper] kernel-matrix packing
K_meta = concat_metadata(K_meta, groups_of=4)         # [paper] metadata packing

# ---- device kernel, per thread block ----
for block_tile in output_grid:                        # [reconstruction]
    smem_B = load_global_to_shared(input, block_tile) # block-level tiling  [paper]
    __syncthreads()
    for warp_tile in block_tile:                      # warp-level tiling   [paper]
        # row swap folded into the load address, no separate pass
        regB = load_shared_to_reg(smem_B,
                 row = 2*(lane%4) + 4*i + (i%2) + swap_delta(i,k))   # [paper]
        acc  = mma_sp_m16n8k16_f16(K_val, K_meta, regB, acc)         # [paper]
    store(output, acc)
```

`swap_delta` is `[reconstruction]` naming of the `+16·(−1)^k` term the paper states.

## 12.8 Real implementation

`NOT_INSPECTED`. No public repository located (census: `NOT_FOUND_AFTER_SEARCH`). No source symbols asserted. The instruction-level facts taken from the paper text are: the sparse MMA used is **`mma.sp` with shape `m16n8k16`** in **FP16**, with `m8n8k4` referenced for smaller-radius configurations [paper]. Whether the kernel reaches this via inline PTX `mma.sp.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32` or via a library wrapper was not stated in the rendered text — `UNKNOWN`. No mention of `ldmatrix` or `cp.async` was found in the rendering — `NOT_IN_PAPER`.

## 12.9 Kernel execution

kernel → thread block (block tile staged global→shared) → warp (warp tile shared→register; issues `mma.sp` `m16n8k16`) → instruction (the sparse MMA plus the fused address arithmetic implementing the row swap). The distinguishing instruction-level fact is that the *correctness-preserving permutation is not an instruction at all*: it is absorbed into the shared→register load offset, so the instruction stream contains no permute/shuffle for it [paper].

## 12.10 Memory traffic

- **global → shared**: block-level tiling; no traffic numbers given for this level. `NOT_IN_PAPER`.
- **shared → register**: the row swap is realised here, at zero extra instruction cost per the paper's claim [paper].
- **register → Sparse Tensor Core**: the compressed value matrix occupies **half** the fragment registers a dense operand would, plus the metadata registers — this is the mechanism by which the padding zeros stop consuming register-file capacity and MMA cycles. The paper does not give a register-count budget. `NOT_IN_PAPER`.
- No L1/L2/HBM breakdown is reported. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Decomposed causes, as the paper argues them:

1. **Halved MMA count for the same stencil.** The 2:4 unit performs the same logical `m16n8k16` product while physically consuming a k-extent of 8 non-zeros per group of 16 — the padding zeros that ConvStencil/LoRAStencil/TCStencil multiply by are never issued. This is the primary cause and is a *hardware skip*, not a software pruning.
2. **Free permutation.** The transform that makes (1) legal costs nothing at runtime because it is folded into load addressing; a naive implementation would have paid a shuffle or an extra shared-memory round trip.
3. **Metadata amortisation.** Concatenating metadata across four MMA invocations converts the sparse unit's partial-lane metadata read into a fully-utilised load.
4. **Cache-line-aligned kernel packing** makes the compressed value matrix's fragment reads contiguous.

Headline results, with qualifiers [paper]: on **NVIDIA A100-80GB PCIe (Ampere), CUDA 12.8, cuDNN 9.8.0**, over 1D stencils (radius 1–2) and 2D star/box stencils (radius 1–3): **6.20× average over cuDNN**, **4.71× over DRStencil**, **3.13× over TCStencil**, **1.88× over ConvStencil**, **1.63× over LoRAStencil**, **1.35× over FlashFFTStencil**; summarised in the abstract as "5.46×" over CUDA-core approaches and "2.00× on average" over Tensor-Core approaches. Brick was **not** among the baselines in this paper.

`[inference]` The gap over ConvStencil (1.88×) is larger than the ≈2.12× redundancy figure the paper attributes to ConvStencil would naively predict for a pure redundancy fix, which is consistent with the packing and metadata optimisations contributing on top of the sparse skip — but the paper provides **no ablation** to separate these, so this attribution is inference, not measurement.

## 12.12 Hardware generation dependence

**Ampere-and-later, and in practice Ampere-measured.** The mechanism requires a Sparse Tensor Core with the 2:4 metadata contract, which NVIDIA introduced with **Ampere**; the paper states the evaluation GPUs "employ the Ampere architecture, which features dedicated SpTCs" [paper]. The instruction used is `mma.sp` `m16n8k16` in **FP16** — note this is *not* the FP64 path, so unlike ConvStencil this work does **not** deliver FP64 stencil accuracy. Precision-versus-baseline discussion: `NOT_IN_PAPER` in the rendering read.

No Hopper (`wgmma`/TMA) or Blackwell (TMEM, 5th-gen Tensor Core, FP6/FP4) measurement or discussion appears. Do not generalise the 2:4 group alignment arithmetic (`L = 2r+2`, the `j ↔ j+(2r+2)` swap) to any unit with a different structured-sparsity granularity — the constants are specific to 2-in-4.

## 12.13 Limitations

- No explicit limitations or future-work section. `NOT_IN_PAPER`.
- **Stated weakness**: performance at smaller problem sizes underperforms some baselines because the tiling configurations are chosen to favour large-scale workloads [paper].
- **No ablation study.** The paper presents no systematic isolation of tiling vs zero-cost row swapping vs data packing [paper — verified absent].
- `[inference]` `L = 2r + 2` forces an even reduction extent tied to the stencil radius; stencil shapes whose natural reduction extent is odd or much larger than `2r+2` are not obviously covered.
- `[inference]` The design assumes the *kernel* matrix is the sparse operand and is known ahead of time (weights fixed). Variable-coefficient stencils, where the sparse operand changes per grid point, are not addressed.
- FP16-only precision is a substantive limitation for scientific stencils; the paper does not report accuracy against an FP64 reference in the text read. `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Direct successor** to `GPU-PPoPP24-01` (ConvStencil), which it cites as [11] and benchmarks against; it reframes ConvStencil's *residual* padding as the resource to exploit.
- **Cites and competes with** LoRAStencil (SC 2024, [49] in this paper), TCStencil ([28], described as the "pioneering" transform), and FlashFFTStencil (PPoPP 2025, [19]) — all three on this cluster's watchlist.
- **Sibling work by overlapping authors**: *Do We Need Tensor Cores for Stencil Computations?* (SC 2026, Qiqi Gu, Chenpeng Wu, Jianguo Yao, Heng Shi + Haibing Guan; official SC26 Best Student Paper nominee) is from the same group and directly interrogates the premise of this line — watchlist item, no public full text.
- **Competing/parallel**: SparStencil (SC 2025, "Retargeting Sparse Tensor Cores to Scientific Stencil Computations via Structured Sparsity Transformation") attacks the *same* problem — Sparse Tensor Cores for stencils via a structured-sparsity transform — at an earlier venue. The two are strong candidates for a priority/independence question, which **cannot be settled here**: SparStencil has no public full text reachable from this environment, and the SPTCStencil text read does **not** cite it. Recorded as `UNRESOLVED`.
- **Self-claim**: "the first to harness SpTCs for acceleration beyond deep learning domains" [paper]. Given SparStencil (SC 2025) and BerryBees (PPoPP 2025, bit-tensor-core BFS), this claim should be treated as the authors' and **not verified** here.
- Prior corpus check: repository hits for "SPTCStencil" and "2506.22035" are confined to `domains/gpu_systems/census/PPoPP_2026.md` (census rows). `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The entire contribution is a constructive answer to the **2:4 structured-sparsity metadata contract of NVIDIA's Sparse Tensor Core**. The design constant `L = 2r + 2` and the permutation `j ↔ j + (2r + 2)` exist solely to make every contiguous *4-element* group contain at most *2* non-zeros — change the group size and the whole transform is void. The compressed-value-plus-2-bit-metadata pair, the placeholder zero kept in singleton segments to hold the compressed width uniform, the `mma.sp` `m16n8k16` per-thread register arrangement ("four `.f16` elements in two `.f16x2` registers"), the folding of the row permutation into the shared→register load offset, and the packing of metadata across four MMA invocations to occupy the lanes that would otherwise not read metadata — all are properties of warp-cooperative sparse-MMA operand semantics with nothing to correspond to on a CPU or a generic accelerator.

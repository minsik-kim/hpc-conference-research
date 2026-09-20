# GPU-SC26-02 — EmuGEMM: Fused Tensor Core Kernels for Precision Emulation in Matrix Multiplication

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` in-repo; `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` for the un-imported AI/HPC corpus
primary_topic: `F — Tensor/Matrix cores, numeric formats, precision emulation`
secondary_topics: `kernel fusion; Hopper wgmma / Blackwell tcgen05 + TMEM; complex arithmetic (3M)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML — Introduction/motivation, background on Ozaki Schemes I and II, §III-A interleaved layout, §III-B EmuGEMM-I persistent kernel, §IV EmuGEMM-II fused modular reduction and CRT-3M complex, §V evaluation setup and results incl. §V-A implementation, §VI related work. §V-G is referenced as a limitations location but its content was not legible in the rendering — recorded as partially read.`

## 12.1 Bibliographic facts

- Title: **EmuGEMM: Fused Tensor Core Kernels for Precision Emulation in Matrix Multiplication** [paper]
- Authors: Denghui Lu, Alexander Maeder, Mathieu Luisier, Alexandros Nikolaos Ziogas [paper]. Affiliations are not listed in the rendered preprint text — `NOT_IN_PAPER`. (`[inference]` Luisier and Ziogas are associated with ETH Zürich in the broader literature; this is **not** a paper-level statement and is not used as evidence anywhere below.)
- Preprint: arXiv:2606.25453v1, **24 June 2026** [paper]
- Venue: seeded as **SC 2026**. Census records `SC26_MEMBERSHIP_UNVERIFIED`; no confirming program page or DOI was reachable. **Venue membership `UNVERIFIED`**; publication type as read: `PREPRINT`.
- Artifact/code: `UNKNOWN` (census) — none located, none inspected. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Ozaki-style FP64 emulation is arithmetically sound but its implementations launch one low-precision GEMM per slice or per modulus and round-trip every intermediate through global memory — can the whole decomposition be **fused into a single Tensor Core kernel** so operands are loaded once and intermediates never leave the chip?

## 12.3 GPU/HPC problem translation

- **Compute.** Emulation replaces one FP64 GEMM with `p(p+1)/2` slice-pair products (Scheme I) or `p` modular products (Scheme II). The arithmetic is cheap on integer Tensor Cores; the *orchestration* is not.
- **Memory.** This is the paper's identified bottleneck, stated verbatim: "intermediate results are repeatedly materialized in global memory, making data movement the dominant bottleneck" [paper]. The complexity argument: separate kernels per slice product force operand reloads scaling as **O(p²)** memory transactions where **O(p)** suffices [paper].
- **Synchronization.** Fusing `p(p+1)/2` products into one kernel means all partial accumulators must be live simultaneously on-chip, and the final reconstruction (shift-and-add for Scheme I; CRT for Scheme II) becomes an *in-register epilogue* rather than a separate kernel — this is the synchronisation restructuring.
- **Scheduling.** A **persistent kernel** with a *triangular* MMA schedule over `p` accumulators [paper].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- **Accumulator capacity is the binding constraint, and it moved.** On Hopper (SM90) `wgmma.mma_async` takes operand tiles from shared memory but keeps accumulators **in the register file**; on Blackwell (SM100) `tcgen05.mma` takes operands from shared memory and keeps accumulators in **TMEM, "a dedicated on-chip storage for accumulator data"** [paper, §V-A]. Holding `p` simultaneous accumulators is therefore a register-pressure problem on Hopper and a TMEM-capacity problem on Blackwell. This generational difference is what makes the fusion feasible at a useful `p` on Blackwell.
- **Scheme II adds a second round trip.** The INT32→INT8 modular reduction between the GEMM and the next stage is, in prior implementations, a separate kernel — so each modulus pays a global-memory round trip, "tripled under complex arithmetic via the 3M method" [paper].
- **Tile shapes are fixed by the instruction.** `wgmma` on SM90 is used with `tM = 64, tK = 32`, configurable `tN`; `tcgen05` on SM100 with `tM = 128, tK = 32`, configurable `tN` — both INT8×INT8→INT32 [paper, §V-A]. Any slice-storage layout that does not align to these tile extents costs a data-movement pass, which is exactly what §III-A removes.

## 12.5 Mathematical / performance model

- **Scheme I** splits FP64 operands into `p` mantissa slices; the product needs the upper-triangular set of slice pairs, `p(p+1)/2` products, reconstructed by shifting and adding [paper].
- **Scheme II** uses `p` independent modular (CRT) GEMMs [paper] — the same scheme as `GPU-SC26-01`.
- **The paper's central complexity claim** [paper]: with `p` slices, naive per-product kernels require **O(p²)** total slice loads; fusing reduces this to **O(p)** by loading each slice once and materialising intermediates on-chip. This is a *traffic* model, not a FLOP model — the arithmetic count is unchanged.
- **Complex arithmetic**: the **3M** method (3 real multiplications instead of 4) is implemented as a CRT-based fused GEMM on integer Tensor Cores "with error-free outputs during the multiplication stage" [paper, §IV].
- No error bound or accuracy theorem is stated in the rendering read — `NOT_IN_PAPER`. Accuracy is handled comparatively ("at comparable accuracy" to cuBLAS TF32).

## 12.6 Data layout and ownership

- **Global memory layout — the paper's §III-A contribution.** An **interleaved layout** co-designs "the decomposed slices' global memory layout to align with the MMU's tile dimensions without extra data movement", which is what permits all `p(p+1)/2` products in one kernel [paper]. The paper describes this layout as **format-agnostic**, applicable to any Ozaki-style decomposition — i.e. it is a reusable result, not a one-off.
- **shared memory**: holds the operand tiles for both `wgmma` (SM90) and `tcgen05` (SM100) [paper, §V-A].
- **accumulators**:
  - SM90 / Hopper: `p` on-chip accumulators in the **register file** [paper].
  - SM100 / Blackwell: accumulators in **TMEM** [paper].
- **warp / warpgroup**: `wgmma.mma_async` is a *warpgroup*-level (128-thread) instruction on Hopper; `tcgen05.mma` is the Blackwell successor. The epilogue is explicitly **in-register**: "an in-register shift-reduce epilogue that reconstructs the output without further global memory traffic" [paper, §III-B].
- **block / SM**: one persistent CTA per SM class of schedule (the paper says "persistent kernel"; the exact CTA-to-SM mapping was not stated in the rendering — `NOT_IN_PAPER`).
- **node / cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- EmuGEMM-I (Scheme I), one persistent kernel  [paper] §III-B ----
# A, B pre-decomposed into p slices, stored in the INTERLEAVED layout
# whose stride matches (tM, tK) of the target MMA          [paper] §III-A
persistent_kernel EmuGEMM_I(A_slices, B_slices, C, p):
    acc[0..p-1] = 0                   # on-chip: RF on SM90, TMEM on SM100  [paper]
    for tile_k in K_tiles:                                     # [reconstruction]
        smem_A, smem_B = load_tiles(A_slices, B_slices, tile_k) # loaded ONCE -> O(p)
        for (i, j) in triangular_pairs(p):                      # i+j <= p-1  [paper]
            acc[i+j] = mma_int8(smem_A[i], smem_B[j], acc[i+j]) # wgmma / tcgen05
    C = shift_reduce_in_register(acc)   # [paper] "in-register shift-reduce epilogue"

# ---- EmuGEMM-II (Scheme II) ----                            [paper] §IV
fused_kernel EmuGEMM_II(A_mod, B_mod, C, moduli):
    for l in moduli:
        acc = mma_int8(A_mod[l], B_mod[l], 0)        # INT32 accumulate
        Cl  = mod_reduce_int32_to_int8(acc)          # FUSED, no global round trip [paper]
        crt_accumulate(C, Cl, l)
# complex: CRT-based 3M as a fused GEMM on integer TCs        [paper] §IV
```

`triangular_pairs`, `shift_reduce_in_register`, `crt_accumulate` are `[reconstruction]` names; the *concepts* "triangular MMA schedule over p on-chip accumulators", "in-register shift-reduce epilogue", "INT32-to-INT8 modular reduction directly into the GEMM" are the paper's own wording [paper].

## 12.8 Real implementation

`NOT_INSPECTED`. No repository was located (census: `UNKNOWN`; none stated in the text read). No source symbols are asserted.

Instruction-level facts taken from the paper [paper, §V-A]:
- **SM90 (Hopper)**: `wgmma.mma_async`, INT8×INT8→INT32, `tM = 64`, `tK = 32`, configurable `tN`; operands in SMEM, accumulators in the register file.
- **SM100 (Blackwell)**: `tcgen05.mma`, INT8×INT8→INT32, `tM = 128`, `tK = 32`, configurable `tN`; operands in SMEM, accumulators in TMEM.
- No mention of TMA, `cp.async.bulk`, or `ldmatrix` was found in the rendering — `NOT_IN_PAPER`. (`[inference]` a `wgmma`-based persistent kernel on Hopper would ordinarily use TMA for the SMEM fill, but the paper as read does not say so, so it is not asserted.)

## 12.9 Kernel execution

kernel (single persistent launch replacing `p(p+1)/2` or `p` launches) → CTA → **warpgroup** (the unit that issues `wgmma`/`tcgen05`) → instruction. The decisive execution-level change is the removal of *kernel-launch and global-memory* boundaries between the products: the loop over slice pairs or moduli moves from the host's launch stream into the device's instruction stream, and the reconstruction moves from a separate reduction kernel into the epilogue of the same kernel.

## 12.10 Memory traffic

- **global → shared**: each slice/modulus operand tile is loaded **once** per K-tile rather than once per product — the O(p²) → O(p) claim [paper].
- **shared → MMA operand**: direct, per the `wgmma`/`tcgen05` operand-from-SMEM contract [paper].
- **accumulator**: never leaves the chip until the epilogue; on SM100 it lives in TMEM [paper].
- **global write**: once, after the in-register (Scheme I) or fused-CRT (Scheme II) reconstruction [paper].
- For Scheme II, the eliminated traffic is named specifically: "per-modulus global memory round-trips" for the INT32→INT8 reduction, "tripled under complex arithmetic via the 3M method" [paper].
- No measured byte counts or cache hit rates are given. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Decomposed causes:
1. **Operand-load amortisation** (O(p²) → O(p)): the dominant cause for Scheme I, where the triangular product set re-reads the same slices many times in a per-product-kernel implementation.
2. **Elimination of the modular-reduction round trip** (Scheme II): removes `p` (or `3p` for complex) global-memory passes.
3. **Layout alignment**: the interleaved global layout matches `(tM, tK)`, so no transpose/repack pass is needed to feed the MMA — this is what makes (1) and (2) *possible*, not merely faster.
4. **Accumulator residency**: `p` accumulators held in RF (SM90) or TMEM (SM100); on SM100 TMEM is a dedicated accumulator store, which relieves the register pressure that would otherwise cap `p`.

**Measured results, with hardware qualifiers** [paper, §V]:
- Platforms: **NVIDIA GH200 (Hopper, SM90)** and **NVIDIA B200 (Blackwell, SM100)**. Baselines: cuBLAS native DGEMM, cuBLAS TF32, cuBLAS INT8 GEMM, cuBLAS ZGEMM (complex), and "cuBLAS Scheme I emulation".
- **EmuGEMM-I throughput**: up to **1,639 TOP/s on Hopper (83% of INT8 peak)** and **3,654 TOP/s on Blackwell (81% of peak)**. *Qualifier: integer-op throughput of the emulation kernel, as a fraction of the part's INT8 matrix peak — not an FP64-equivalent FLOP/s number.*
- **Versus cuBLAS TF32 at comparable accuracy**: **1.4× on Hopper**, **1.7× on Blackwell**.
- **EmuGEMM-II with 3M complex versus cuBLAS ZGEMM**: up to **2.3× on Hopper**, **5.5× on Blackwell**.
- The fact that the *fraction of INT8 peak* is ~81–83% on both generations is the paper's strongest evidence that the fused kernel is no longer data-movement-bound — that is the intended reading of those numbers.

## 12.12 Hardware generation dependence

Sharply generation-dependent, and the paper keeps the two apart correctly:
- **Hopper / SM90 / GH200**: `wgmma.mma_async`, `tM=64, tK=32`, accumulators in the **register file**. 1,639 TOP/s, 83% of INT8 peak; 1.4× cuBLAS TF32; up to 2.3× ZGEMM.
- **Blackwell / SM100 / B200**: `tcgen05.mma`, `tM=128, tK=32`, accumulators in **TMEM**. 3,654 TOP/s, 81% of peak; 1.7× cuBLAS TF32; up to 5.5× ZGEMM.
- The `tM` doubling (64 → 128) and the RF→TMEM accumulator relocation are both hard generational facts that change the fusion's feasibility envelope. **Do not restate a Hopper number as a Blackwell number or vice versa.**
- Ampere (A100) is **not** evaluated; `wgmma`/`tcgen05` do not exist there, so the design does not transfer to Ampere as written. No AMD CDNA (MFMA) evaluation. `NOT_IN_PAPER`.

## 12.13 Limitations

- §V-G is referenced as the limitations location but its content was **not legible** in the rendering read. **`PARTIALLY_READ` — the paper's own limitations are not faithfully recorded here.** This is the one gate this analysis does not fully clear; it should be revisited against the PDF.
- `[inference]` `p` is bounded by on-chip accumulator capacity (RF on SM90, TMEM on SM100). A slice count large enough for very high emulated precision would exceed it and force partial fusion; the paper does not state the ceiling.
- `[inference]` The interleaved global layout must be produced by the decomposition step, so an application feeding EmuGEMM from an arbitrary FP64 buffer pays a one-time repack the paper's O(p) accounting does not obviously include.
- No artifact located, so none of the above can be checked in code.
- No accuracy theorem; accuracy is asserted comparatively against cuBLAS TF32. `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Complementary sibling** to `GPU-SC26-01` (Ozaki-II with FP8 quantization). The division of labour is clean and is the single most useful cross-paper observation in this cluster: `GPU-SC26-01` asks *which number format and which moduli* and then calls `cublasGemmEx`; EmuGEMM takes the scheme as given and asks *how to write the kernel*. EmuGEMM's related work cites "Ozaki et al.", "Uchino et al." and recent "cuBLAS integration" work as the implementations it optimises [paper, §VI] — i.e. it cites `GPU-SC26-01`'s authors.
- **Competing with** cuBLAS's own FP64-emulation path ("cuBLAS Scheme I emulation", a measured baseline) — so this is a case of academic work benchmarking against a *vendor-shipped* emulation feature, which did not exist a generation earlier.
- **Precursor line** cited: Ozaki Schemes I and II; OzIMMU appears in the sibling paper's citations for the same lineage.
- **Watchlist adjacency**: M3XU (SC 2024) is the earliest item in this cluster's emulation line; MXBLAS (SC 2025) and MXFFP (ISCA 2026) sit on the *format* side of the same story.
- **External-corpus caveat**: `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`; a fused-Tensor-Core-kernel paper is plausibly in that ~80-paper corpus, so no duplication claim is asserted. In-repo hits for "EmuGEMM" are confined to `domains/gpu_systems/census/SC_2026.md`. `NO_EXISTING_ANALYSIS` in-repo.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution is a kernel-level restructuring whose every constraint comes from named GPU matrix-unit mechanics: the operand-from-shared-memory / accumulator-placement contracts of `wgmma.mma_async` on SM90 versus `tcgen05.mma` on SM100 (register file versus **TMEM**), the fixed MMA tile extents `tM=64, tK=32` (Hopper) and `tM=128, tK=32` (Blackwell) that the interleaved global layout is designed to align to, the INT8×INT8→INT32 accumulate type that makes the modular reduction fusable in the first place, warpgroup-level cooperative issue, and an in-register shift-reduce epilogue that exists only because the accumulators are warp-private on-chip state. On a CPU the emulation would be a library call sequence with a cache, not a fused warpgroup kernel, and the O(p²)→O(p) result would be a blocking-and-tiling observation rather than a matrix-unit one.

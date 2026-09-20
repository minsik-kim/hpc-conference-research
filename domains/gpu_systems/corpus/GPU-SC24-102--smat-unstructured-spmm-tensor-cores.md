# GPU-SC24-102 — High Performance Unstructured SpMM Computation Using Tensor Cores (SMaT)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (a **verdict-only row** for this paper already exists in `domains/gpu_systems/corpus/_LEDGER_tensor_cores.md`, recorded there as `PUBLIC_FULLTEXT`, "not fetched (capacity)", `CORE_GPU`, watchlist. This file is the first deep analysis; no corpus analysis file existed.)
primary_topic: `G — Sparse/irregular GPU kernels (SpMM, formats, reordering)`
secondary_topics: `F — Tensor/Matrix cores (dense MMA on blocks, NOT 2:4 SpTC); blocked-CSR format design; row reordering/clustering; load balancing`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2408.11551v1) — title/authors/affiliations, introduction and motivation, BCSR/blocking definition, the Sylos Labini Jaccard-clustering preprocessing, Algorithm 1 warp-level execution model, the MMA/LDMATRIX/memcpy_async kernel detail, the linear performance model, evaluation setup (A100, CUDA 12.0, driver, gcc), the 9-matrix SuiteSparse suite with sizes and sparsities, synthetic band matrices, all baselines, the C/B/T optimisation breakdown, the preprocessing block-reduction numbers, the explicitly stated limitation on dc2, and related work. NO DEDICATED FUTURE-WORK SECTION — recorded as NOT_IN_PAPER.`

## 12.1 Bibliographic facts

- Title: **High Performance Unstructured SpMM Computation Using Tensor Cores** [paper]. The system is named **SMaT** — "(S)parse (Ma)trix Matrix (T)ensor Core-accelerated" [paper].
- Venue: **SC 2024**. DOI `10.1109/SC41406.2024.00060` [census: `domains/gpu_systems/census/SC_2024.md`]. `ieeexplore.ieee.org` returns 418 from this environment, so the DOI was not dereferenced.
- Authors and affiliations [paper]: **Patrik Okanovic** (ETH Zurich, Dept. of Computer Science), **Maciej Besta** (ETH Zurich), **Grzegorz Kwasniewski** (ETH Zurich), **Flavio Vella** (University of Trento, Faculty of Engineering), **Paolo Sylos Labini** (Free University of Bozen-Bolzano, Faculty of Engineering), **Torsten Hoefler** (ETH Zurich).
- Publication type: `ARCHIVAL_MAIN_PAPER`; arXiv 2408.11551 is a `PREPRINT` of the same work.
- Full text used: `https://arxiv.org/html/2408.11551v1` [paper]. Author PDF also recorded by the census: `http://www.unixer.de/publications/img/okanovic-sc24-high.pdf` (not needed).
- Artifact: census records `UNKNOWN`; no repository URL was located in the fetched text. `NOT_INSPECTED`. No source symbols asserted.

## 12.2 Core question (one sentence)

Can *unstructured* sparse matrices — the SuiteSparse kind, with no ML-style structure to exploit — be made to run on the dense Tensor Core datapath by (i) blocking into MMA-shaped dense tiles, (ii) permuting rows so fewer such tiles are needed, and (iii) writing a low-level MMA/`LDMATRIX`/async-copy kernel, and which of those three actually carries the speedup?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's framing is a *wasted-unit* argument: "the computational power of dense matrix units, which are common in most high-performance hardware configurations, still remains untapped" [paper]. SpMM in CSR runs on CUDA cores while the Tensor Cores idle.
- **Memory.** BCSR stores every element of a block "even if some of them are zeros" [paper], so the memory cost is set by *block count*, not non-zero count — which is precisely what the preprocessing minimises.
- **Synchronization.** Warp-internal only; each warp owns one output block. No grid-wide synchronisation. `NOT_IN_PAPER` beyond that.
- **Scheduling / load imbalance.** This is where the paper is unusually honest: the schedule is a **static 2D parallel decomposition**, and the paper states that `dc2` is "especially ill-suited for SMaT's execution model with static 2D parallel schedule" [paper]. Reordering is credited with reducing the per-row block-count standard deviation on `mip1` by **8.4×** [paper].
- **Communication.** Single GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- The `mma` instruction consumes a **fixed-shape dense register fragment**. For FP16 the paper uses **`m16n8k16`**, and therefore fixes the storage block at **16×8** — "For FP16, we use the block size 16×8, corresponding to the M16N8K16 instruction" [paper]. The block shape is *dictated by the instruction*, not chosen for the matrix.
- Consequently every zero that happens to land inside a 16×8 tile is multiplied anyway. The number of such tiles is a function of how the non-zeros are *arranged*, which is why a **row permutation** is a legitimate performance lever: it does not change the matrix, only the tile count.
- The second root cause is the register-fill path: fragments must arrive in the exact lane-to-element layout the MMA expects. `LDMATRIX` exists for that; the paper uses **`LDMATRIX_X2`** (2 registers, 8×8 FP16) and **`LDMATRIX_X4`** (4 registers, 16×8 FP16), which "load into registers in the required format", avoiding register-to-register shuffling [paper].
- The third is the global→shared path: `cuda::memcpy_async` "can be used to directly transfer data from global memory to shared memory using DMA engines without involving registers" [paper], which is what lets the block load overlap the MMA.

## 12.5 Mathematical / performance model

- **Blocking definition** [paper]: the matrix is cut into "submatrices of fixed size h × w. Each block is assumed to be dense, that is, all h·w values are stored explicitly, even if some of them are zeros."
- **Linear performance model** [paper]: `T_tot = T_e · n_e + T_init`, with `T_e` the single-MMA time and `n_e` the number of blocks. Figure 2 validates it. This model is the paper's justification for the whole preprocessing stage: **runtime is linear in block count**, so minimising block count is minimising runtime.
- **Preprocessing objective** [paper]: Sylos Labini's algorithm "clusters similar rows together" by **Jaccard similarity**, minimising zero padding inside blocks. Measured block-count reduction **1.3× (`cant`) to 2.4× (`cop20k_A`)** [paper].
- **Design choice recorded** [paper]: **row-only permutation** was chosen over row+column, because the column-permutation overhead was not justified.
- **The paper's own punchline about its model** [paper]: "low-level kernel optimizations can play a more important role than even an optimal preprocessing algorithm" — the Tensor Core API change alone gives "10 times", the optimised kernel **22× over naive**, while the best preprocessing gives at most 2.4× fewer blocks.

## 12.6 Data layout and ownership

- **lane**: `LDMATRIX_X2`/`X4` place the 8×8 / 16×8 FP16 fragment into the lanes' registers in MMA order [paper].
- **warp**: "Each warp is responsible for the calculation of a submatrix of matrix C such that the dimensions correspond to the dimensions of the TC" [paper] — **one output block per warp**. The kernel iterates "only over non-zero blocks" via `rowPtr`/`col`, Algorithm 1: "for blocks in bcsrVals[row] do" [paper].
- **block/SM**: "bottom-up 2D parallelism to maximize the utilization of GPU hardware resources" [paper]. Static, which is the source of the `dc2` failure.
- **BCSR arrays** [paper], three of them: `rowPtr` (block-row offsets), `col` (block-column indices), `val` (h·w consecutive entries per block).
- **shared memory**: destination of `cuda::memcpy_async` collective warp loads, staged for `LDMATRIX` [paper]. Byte budget / bank-conflict discussion: `NOT_IN_PAPER`.
- **GPU**: NVIDIA A100-SXM4-40GB (Ampere) [paper].
- **node/cluster**: single GPU. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- offline preprocessing ---                                   [paper]
P = jaccard_cluster_rows(A)          # Sylos Labini's algorithm; row-only
A' = permute_rows(A, P)
BCSR = to_blocked_csr(A', h=16, w=8) # block shape fixed by m16n8k16

# --- kernel, one output C-block per warp ---                     [paper] Alg. 1
for row in block_rows:                       # 2D static schedule
  acc = 0
  for blk in bcsrVals[row]:                  # non-zero blocks only
      memcpy_async(smem_A, BCSR.val[blk])    # cuda::memcpy_async, DMA, bypasses regs
      memcpy_async(smem_B, B[BCSR.col[blk]])
      fragA = LDMATRIX_X4(smem_A)            # 16x8 FP16 into registers
      fragB = LDMATRIX_X2(smem_B)            # 8x8  FP16
      acc   = HMMA16816(fragA, fragB, acc)   # mma.m16n8k16
  store(C, row, acc)
```

`HMMA16816`, `LDMATRIX_X2`, `LDMATRIX_X4`, `cuda::memcpy_async`, `rowPtr`, `col`, `val`, `bcsrVals` are the paper's own names [paper]. `jaccard_cluster_rows`, `to_blocked_csr` are `[reconstruction]` labels for stages the paper describes but does not name in code.

## 12.8 Real implementation

`NOT_INSPECTED`. No repository URL located in the fetched text; the census records `UNKNOWN`. No source symbols are asserted.

Instruction-level facts, from the paper only [paper]: `mma.m16n8k16` FP16 (Listing 1 shows the PTX-level `HMMA16816` macro), `LDMATRIX_X2` and `LDMATRIX_X4`, `cuda::memcpy_async`. Whether `cp.async` is used directly or only via the `cuda::memcpy_async` wrapper is `UNKNOWN` and is not guessed.

## 12.9 Kernel execution

kernel → thread block (2D static tile of `C`) → warp (one `C` sub-block matching the TC output shape) → `mma.m16n8k16` instruction. The distinctive execution property is that **the sparse structure is consumed entirely by the block-index arrays before the warp starts**: inside a warp there is no sparsity at all, only a dense loop over `rowPtr`/`col`. That is what makes the MMA legal and also what makes the schedule fragile on skewed matrices — a warp's work is proportional to its block-row's block count, with no redistribution.

## 12.10 Memory traffic

- **global → shared**: `cuda::memcpy_async` via DMA engines, "without involving registers", enabling overlap of computation and data movement [paper].
- **shared → register**: `LDMATRIX_X2`/`X4`, in MMA fragment order, avoiding intermediate register-to-register moves [paper].
- **stored bytes**: BCSR stores `h·w` values per non-zero block including the zeros. Preprocessing cuts block count **1.3×–2.4×** [paper], which is simultaneously a memory-traffic and a compute reduction because `T_tot ∝ n_e`.
- No L1/L2/HBM counter breakdown. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

The paper's C/B/T breakdown, which is what makes this paper worth reading rather than its speedup table [paper]:

1. **C — asynchronous loads (`cuda::memcpy_async`)**: modest gains.
2. **B — BCSR pointer arrays to skip empty blocks**: incremental.
3. **T — Tensor Core MMA API**: **≈10×**; the fully optimised kernel is **22× over naive**.
4. **Preprocessing (Jaccard clustering)**: block count down 1.3×–2.4×; `mip1` per-row block-count standard deviation down **8.4×**.

So the causal ranking is explicit and, unusually, *contradicts the paper's own title emphasis*: the low-level kernel work dominates the algorithmic reordering.

**Headline results, all three qualifiers carried** — **NVIDIA A100-SXM4-40GB**, **CUDA 12.0 / cuSPARSE 12.0 / nvcc 12.0 / gcc 12.3.0 / driver 530.30.02** [paper]:

- Matrix suite (9 SuiteSparse matrices) [paper]: `mip1` (66K×66K, 10.4M nnz, 99.76% sparse), `conf5_4-8x8` (49K, 1.9M, 99.92%), `cant` (62K, 4M, 99.89%), `pdb1HYS` (36K, 4.3M, 99.67%), `rma10` (46.8K, 2.3M, 99.89%), `cop20k_A` (121K, 2.6M, 99.98%), `consph` (83K, 6M, 99.91%), `shipsec1` (140K, 7.8M, 99.96%), `dc2` (116K, 766K, 99.99%). Plus synthetic band matrices 16,384×16,384 with bandwidth 64–16,384.
- Baselines [paper]: **cuSPARSE v12.0** (CSR), **DASP** (an SpMV library, run as batched SpMV with N=8), **Magicube** (int16 mixed precision, ML-oriented), **cuBLAS** (dense reference, sparsity-scaled FLOP/s).
- Results: up to **125.48× over cuSPARSE v12.0** (`mip1`, A100); **7.34× over DASP** best case; **51.23× over Magicube** best case; **geometric mean 7.71×**. On synthetic band matrices up to **2,445× over cuSPARSE** (16k×16k, N=128). On `cop20k_A` with N=1,000: **8.60× over cuSPARSE, 4.24× over DASP, 1.73× over Magicube**.
- **The most interesting number in the paper**: SMaT **outperforms cuBLAS at 78% sparsity**, where prior work put the crossover near 99.9%; in the fully dense case it is only **2.3× slower than cuBLAS** [paper]. That is a statement about where the sparse/dense boundary now sits on a Tensor-Core GPU.
- **The honest negative**: on `dc2`, SMaT achieves **2.5 GFLOP/s versus DASP's 69.1 GFLOP/s** [paper] — a ~28× *loss*, caused by 99.994% sparsity plus a power-law block-per-row distribution against a static schedule.

## 12.12 Hardware generation dependence

- The block shape **16×8 is not a tuning parameter; it is the `m16n8k16` operand shape** [paper]. Any generation change to the MMA shape changes the format.
- Evaluated on **A100 (Ampere) only** [paper]. Hopper's TMA / `wgmma` path is not exercised; the async-copy mechanism used is the Ampere-era `cuda::memcpy_async`.
- FP16 only for the MMA path; other precisions would change the block shape. `NOT_IN_PAPER` for FP64/TF32 variants.

## 12.13 Limitations

Stated by the paper [paper]:
- `dc2` is "especially ill-suited for SMaT's execution model with static 2D parallel schedule"; "SMaT's schedule is sensitive to highly skewed distribution of blocks per row." This is a **load-imbalance limitation the paper does not solve** — it mitigates it with reordering and then reports the residual failure.
- Magicube runs out of memory beyond the 9 SuiteSparse matrices, which is why the suite is small.
- **The suite is 9 matrices.** Contrast FlashSparse (`GPU-PPoPP25-01`), which reports on 515. A 9-matrix suite cannot establish a geometric-mean claim about SuiteSparse.
- No explicit future-work section. `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Direct precursor** to `GPU-PPoPP25-01` (FlashSparse) and `GPU-PPoPP25-02` (Acc-SpMM). All three put unstructured sparsity on the dense MMA path by blocking; SMaT (2024) fixes the block at the instruction shape and attacks the *tile count* with reordering, whereas FlashSparse (2025) attacks the *tile shape* by swapping operands to exploit `n=8`, and Acc-SpMM attacks the *schedule*.
- **Confirms the `_LEDGER_tensor_cores.md` distinction**: SMaT uses **dense MMA on dense blocks, not 2:4 Sparse-Tensor-Core metadata** — verified explicitly in the fetched text: the block format is BCSR with `m16n8k16`, and "not NVIDIA's structured 2:4 sparsity format introduced in Ampere" [paper]. SMaT therefore belongs with FlashSparse/Acc-SpMM/Insum, **not** with SPIDER / Bridging the Gap / N:M reordering / Coruscant / Uni-STC.
- **Competing with** DASP (SC 2023, the SSSLab group whose Mille-feuille is `GPU-SC24-103` in this cluster) — SMaT uses DASP as a baseline and loses to it on `dc2`. That is a real, citable tension between two SC-era Tensor-Core sparse lines.
- The tensor-cores ledger already carries a verdict row for this paper (`CORE_GPU`, watchlist, "not fetched"). This file **upgrades that row from provisional to read**; the verdict is unchanged.
- No prior analysis file existed. `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The block shape is **not chosen — it is the `m16n8k16` MMA operand shape**, and the whole format, the whole preprocessing objective (minimise the number of 16×8 tiles) and the whole performance model (`T_tot = T_e·n_e + T_init`) are downstream of that instruction. The fragment-fill path (`LDMATRIX_X2`/`X4` delivering the exact lane-to-element layout the MMA demands) and the global→shared DMA path (`cuda::memcpy_async` bypassing registers) are GPU register-file and memory-hierarchy mechanisms with no CPU analogue. A CPU blocked-SpMM would choose its block shape from cache-line and SIMD width, giving a different format and a different reordering objective.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Compute — claimed and established.** The T-step of the breakdown isolates the MMA at ≈10×; the linear model ties runtime to block count and the reordering result confirms it.
- **Memory — claimed and established.** `memcpy_async` and `LDMATRIX` are measured as the C-step, and the block-count reduction is simultaneously a traffic reduction.
- **Load imbalance — claimed, ADDRESSED ONLY PARTIALLY, AND THE PAPER SAYS SO.** Reordering cuts `mip1`'s block-count standard deviation 8.4×, but the static 2D schedule still loses 28× to DASP on `dc2`. The claim is *not* established in general; the paper's candour about this is what makes the failure usable evidence.
- **Synchronisation — not claimed.**
- **Dependency — not applicable.**

verdict: `CORE_GPU`

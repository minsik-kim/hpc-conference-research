# GPU-SC24-103 — Mille-feuille: A Tile-Grained Mixed Precision Single-Kernel Conjugate Gradient Solver on GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (a **verdict-only row** exists in `domains/gpu_systems/corpus/_LEDGER_tensor_cores.md`, recorded there as `CLOSED_ACCESS (effectively)` and `RELATED_GPU` on title/census evidence, with cluster-F membership `UNRESOLVED`. **This file corrects both**: the author PDF is reachable, and on the full text the verdict is `CORE_GPU` for cluster G. The tensor-cores ledger's reasoning was right — the mechanism is *not* the matrix unit — it simply lacked the text.)
primary_topic: `G — Sparse/irregular GPU kernels (sparse iterative solvers, tiled sparse formats)`
secondary_topics: `mixed precision (FP64/FP32/FP16/FP8); persistent single-kernel execution and software grid synchronisation; SpMV; SpTRSV preconditioning; AMD/NVIDIA portability`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author PDF (https://www.ssslab.cn/assets/papers/2024-yang-Millefeuille-final.pdf) — abstract, introduction and the three motivating findings (Figures 1, 2, 4), the two-level tiled format and its arrays, the per-nonzero precision-selection criterion, the single-kernel design with the d_s/d_d/d_a dependency arrays and the four execution steps A-D, Algorithms 4 and 5 (partial-convergence detection and on-chip precision conversion), the SpTRSV recursive-block preconditioner, evaluation setup (A100 + MI210, CUDA 12.0, ROCm 5.7.3, 230 SPD + 686 nonsymmetric SuiteSparse matrices), all four baselines with versions, headline and preconditioned results, the Figure 11 mixed-precision ablation, Table II/Figure 12 convergence impact, Figure 13 memory overhead, the stated limitations, and related work.`

## 12.1 Bibliographic facts

- Title: **Mille-feuille: A Tile-Grained Mixed Precision Single-Kernel Conjugate Gradient Solver on GPUs** [paper]
- Venue: **SC 2024**. DOI `10.1109/SC41406.2024.00064` [census: `domains/gpu_systems/census/SC_2024.md`]. `ieeexplore.ieee.org` returns 418 here; the DOI was not dereferenced.
- Authors [paper]: **Dechuang Yang, Yuxuan Zhao, Yiduo Niu, Weile Jia, En Shao, Weifeng Liu, Guangming Tan, Zhou Jin**.
- Affiliations [paper]: **Super Scientific Software Laboratory (SSSLab), Dept. of CST, China University of Petroleum-Beijing**; **State Key Lab of Processors, Institute of Computing Technology, CAS**; **University of Chinese Academy of Sciences**.
- Publication type: `ARCHIVAL_MAIN_PAPER`. The author PDF is the same work.
- Full text used: `https://www.ssslab.cn/assets/papers/2024-yang-Millefeuille-final.pdf` [paper].
- Artifact: `https://github.com/SuperScientificSoftwareLaboratory/Mille-feuille` [census, README-level]. **`NOT_INSPECTED`** — not cloned in this pass. No source symbols are asserted; the array names below (`d_s`, `d_d`, `d_a`, `TilePrec`, …) are the **paper's** names [paper], not code symbols.

## 12.2 Core question (one sentence)

If a Krylov solver's per-iteration cost is set by three things the literature usually treats separately — the precision at which each *piece* of the matrix must be stored, the kernel-launch/synchronisation boundary between SpMV, dot and AXPY, and the fact that different *elements of the solution* converge at different rates — can all three be attacked at once by making the whole iteration a single persistent kernel over a tiled format whose per-tile precision is demoted at runtime as the corresponding vector segment converges?

## 12.3 GPU/HPC problem translation

- **Compute.** Low-precision storage reduces bytes, not FLOPs on the CUDA-core path; the paper's compute win comes from **bypass** — tiles whose corresponding vector segment has fallen below `ε·10⁻³` are skipped entirely, "no multiplication, no atomicAdd" [paper].
- **Memory.** The dominant axis. SpMV is bandwidth-bound; per-nonzero precision selection (FP64→FP32→FP16→FP8 under a `10⁻¹⁵` loss threshold) directly cuts the bytes streamed per iteration [paper].
- **Synchronization.** The paper's Figure 2 finding: **inter-kernel synchronisation consumes over 30% of runtime** in a cuSPARSE/cuBLAS-style multi-kernel CG [paper]. This is the single largest structural claim in the paper.
- **Dependency.** CG has a strict per-iteration dependency chain SpMV → dot → scale → AXPY. Collapsing it into one kernel means the dependency must be enforced *inside* the kernel, which is what the three dependency arrays do.
- **Load imbalance.** Tiles are distributed to warps "balancing both nonzero count and tile count" [paper] — addressed, but with a heuristic rather than a measured imbalance study.
- **Communication.** Single GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- A CUDA kernel launch is a **grid-wide serialisation point**: nothing in iteration `j+1` may start until every block of iteration `j` has retired. For CG, whose per-iteration work on a small matrix is short, that boundary is a large fraction of the iteration. The paper measures it at >30% [paper].
- The obvious fix, a cooperative-groups grid barrier, is **deliberately not used**: "The design avoids `__grid_sync()` by using busy-wait loops on atomic counters. This is less efficient than true grid-wide barriers but portable across older GPU architectures without grid-sync support" [paper]. That is a real, recorded engineering trade — and it is also the origin of the paper's atomic-contention limitation.
- A persistent kernel requires the *whole* working set to stay resident. On A100 that means ~100 KB of shared memory per SM [paper], which is why the single-kernel mode has a hard applicability ceiling at **~10⁶ non-zeros**, above which the solver falls back to multi-kernel [paper].
- Precision demotion is only safe *late* in the iteration, because the elements of `p_j` that are small contribute negligibly to the next SpMV [paper, Figure 4]. This is a numerical-analysis fact being used as a hardware lever.

## 12.5 Mathematical / performance model

- **Per-nonzero precision criterion** [paper]: for each non-zero, compare FP32/FP16/FP8 representations against FP64 and keep the **lowest precision whose loss stays below `10⁻¹⁵`** (chosen to match FP64 decimal precision).
- **Partial-convergence thresholds** [paper, Algorithm 4]: `p_j` is split into segments of **16 elements** (matching tile width). Per segment, a 4-entry flag array counts elements in the bands
  `[ε·10⁻³, ε·10⁻²)` → FP8 candidate; `[ε·10⁻², ε·10⁻¹)` → FP16; `[ε·10⁻¹, ε)` → FP32; `[ε, ∞)` → FP64 (unchanged). **All 16 elements** of a segment must fall in a band for the demotion to fire. Below `ε·10⁻³` the segment is **bypassed**.
- **Effective tile precision** [paper, Algorithm 5]: `prec(tile) = min(TilePrec[i], vis_flag[col_idx])` — the tile is cast *in shared memory*, once, then reused.
- **Memory overhead of the format** [paper, Figure 13]: **≈1.04× versus plain CSR**, from the tile metadata and `RowIndex` arrays.
- **Convergence cost** [paper, Table II]: mixed precision needs **1.06× more iterations on average, 1.47× worst case**, but wall-clock still improves — e.g. `mesh3e1`: 53 vs 36 iterations yet **2.89× faster** (1.19 ms vs 3.44 ms).

## 12.6 Data layout and ownership

Two-level format [paper]:
- **Inter-tile (COO-style)**: `TileRowidx`, `TileColidx`, `TilePrec` (encoded FP64=4, FP32=3, FP16=1, FP8=2, bypass=0), `TileNnz` (offsets into per-tile non-zero counts), `Nonrow` (offsets into non-empty-row tracking).
- **Intra-tile (CSR-style)**: `CsrRowptr`, `CsrColidx`, `Val` — **`Val` is four separate arrays, one per precision** — and `RowIndex`, which "maps non-empty rows within a tile, avoiding empty row traversal during SpMV".
- **warp**: owns a set of tiles, assigned by the load-balancing heuristic; within a tile, threads accumulate CSR rows and use `atomicAdd` into the result vector [paper].
- **shared memory**: non-zeros that fit (~100 KB/SM on A100) are pre-loaded **once before the kernel launch and reused across all iterations** [paper]. Precision conversion happens here, with **no global round-trip** [paper].
- **global memory**: overflow tiles, plus the three dependency arrays `d_s[tilenumA]`, `d_d[1]`, `d_a[1]` [paper].
- **GPU**: NVIDIA A100 (6912 CUDA cores @ 1410 MHz, 40 GB, 1555 GB/s) and **AMD MI210 (CDNA2, 6656 stream processors @ 1700 MHz, 64 GB, 1638 GB/s)** [paper].
- **node/cluster**: single GPU. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# One persistent kernel; all warps loop over CG iterations.        [paper] Steps A-D
preload_tiles_to_shared()                    # once, before launch

while not converged:
  # --- Step A: SpMV over tiles ---
  for tile in my_tiles:
      prec = min(TilePrec[tile], vis_flag[col_seg(tile)])   # Alg. 5
      if prec == BYPASS: continue                            # skip entirely
      cast_in_shared(tile, prec)                             # once per demotion
      spmv_tile(tile)                                        # atomicAdd into y
      if lane == 0: atomicSub(d_s[row_tile(tile)], 1)
  while d_s[warp_id] != 0: __threadfence()                   # busy-wait, no grid.sync

  # --- Step B: dot product (mu, p_j) ---
  partial = warp_dot(...); shared_reduce(partial)
  if lane == 0: atomicSub(d_d[0], 1)
  while d_d[0] != 0: __threadfence()

  # --- Step C: dot product (r_{j+1}, r_{j+1}) for beta ---
  if lane == 0: atomicAdd(d_d[0], 1)
  while d_d[0] != warp_num: __threadfence()

  # --- Step D: AXPY on x, r, p; then detect convergence ---
  axpy(...); detect_segment_precision(p, vis_flag)           # Alg. 4, 16-elem segs
  if lane == 0: atomicSub(d_a[0], 1)
  while d_a[0] != 0: __threadfence()
```

`d_s`, `d_d`, `d_a`, `TilePrec`, `vis_flag`, `RowIndex`, Steps A–D, Algorithms 4 and 5, the 16-element segment and the `warp_num` comparison are all the paper's [paper]. `col_seg`, `cast_in_shared`, `spmv_tile` are `[reconstruction]` names for described but unnamed operations.

## 12.8 Real implementation

`NOT_INSPECTED`. The artifact `github.com/SuperScientificSoftwareLaboratory/Mille-feuille` exists [census] but was not cloned in this pass; **no code symbol is asserted**. Everything named above is a paper-level name [paper].

Software stack as the paper states it [paper]: **CUDA 12.0, cuSPARSE v12.0, cuBLAS v12.0**; **ROCm 5.7.3, hipSPARSE v2.3.8, hipBLAS v2.3.8**. A HIP version of the solver exists and is evaluated.

## 12.9 Kernel execution

kernel (one, persistent, for the whole solve) → thread block → warp (owner of a tile set and of one segment of each vector) → instruction. The execution-level novelty is that **the iteration's dependency graph is enforced by atomics and busy-waits inside a single kernel**, not by kernel boundaries. Note the asymmetry in how the two dot products synchronise: Step B **decrements** `d_d[0]` to zero, Step C **increments** it back to `warp_num` [paper] — a ping-pong that avoids having to re-initialise the counter between the two reductions.

## 12.10 Memory traffic

- **HBM → shared, once per solve** for tiles that fit; thereafter the SpMV reads shared memory every iteration [paper]. For a 1000-iteration solve on a small matrix this is the dominant saving and is *not* separately quantified — `NOT_IN_PAPER`.
- **Bytes per non-zero** fall with precision demotion; the four separate `Val` arrays mean a demoted tile is read from the narrower array, not masked.
- **Bypass** removes both the read and the `atomicAdd` for converged columns [paper].
- **Format overhead** 1.04× over CSR [paper, Figure 13].
- No L1/L2 counter breakdown. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Headline results, all qualifiers carried** — **NVIDIA A100 (CUDA 12.0)** and **AMD MI210 (ROCm 5.7.3)**; **230 SPD SuiteSparse matrices for CG, 686 nonsymmetric/indefinite SuiteSparse matrices for BiCGSTAB**, ~10³ to ~10⁸ non-zeros; stopping criterion relative residual `< 10⁻¹⁰` or 1000 iterations; RHS = `A·1`, `x₀ = 0`; baselines run FP64 throughout [paper]:

| Solver | vs cuSPARSE 12.0 | vs hipSPARSE 2.3.8 | vs PETSc 3.20 | vs Ginkgo 1.7.0 |
|---|---|---|---|---|
| CG | **3.03×** avg (up to 8.77×) | 2.68× avg (up to 7.14×) | **5.37×** avg (up to 16.54×) | 4.36× avg (up to 15.69×) |
| BiCGSTAB | 2.65× avg (up to 7.51×) | 2.32× avg (up to 6.63×) | 3.57× avg (up to 16.64×) | 3.78× avg (up to 11.73×) |
| PCG | 3.82× avg (up to 40.38×) | 3.47× avg (up to 47.75×) | — | — |
| PBiCGSTAB | 1.79× avg (up to 45.63×) | 1.63× avg (up to 44.34×) | — | — |

Decomposed cause [paper]:
1. **Synchronisation removal** — the >30% of baseline runtime spent between kernels. Best speedups land on matrices where the baseline's synchronisation share exceeded 50% (`bcsstm22`, `mhdb416` named). **This is the dominant cause and it is a GPU-structural one.**
2. **Mixed precision alone** — Figure 11, 24 representative matrices: **1.54×–1.65×** on matrices with high low-precision ratio (`torso2`, `shallow_water1`); only **1.03×–1.15×** where precision diversity is moderate (`t2dal_bci`), because conversion overhead eats the bit-width gain; **1.35×** on `rajat24` driven by bypass.
3. **Partial-convergence demotion/bypass** — folded into (2) in the paper's measurement; not isolated. `NOT_IN_PAPER` as a standalone number.
4. **Working against all of the above**: 1.06× more iterations on average [paper, Table II].

## 12.12 Hardware generation dependence

- **Deliberately generation-*independent* in one specific way**: `__grid_sync()` is avoided for portability to GPUs without cooperative-groups grid sync [paper]. That choice is why the paper runs unchanged on **AMD MI210** — a genuinely cross-vendor result, which is rare in this cluster.
- **Generation-*dependent* in another**: the ~10⁶-non-zero ceiling for single-kernel mode is a function of **shared memory per SM (~100 KB on A100)** [paper]. On a GPU with a larger on-chip budget the ceiling moves.
- FP8 storage is used as a *storage* format with conversion in shared memory; the paper does not claim FP8 arithmetic units. No Tensor Core / matrix unit is used anywhere — confirming the tensor-cores ledger's suspicion.

## 12.13 Limitations

Stated by the paper [paper]:
1. **Shared-memory saturation** — single-kernel mode needs ≤~10⁶ non-zeros; larger matrices revert to multi-kernel, losing the paper's main advantage. Figures 8–9 show the transition.
2. **Convergence variation** — mixed precision changes the trajectory; some matrices need more iterations.
3. **Atomic contention** — busy-wait synchronisation without grid sync, plus `atomicAdd` on `d_s`/`d_d`/`d_a`, serialises under high contention.
4. **Heuristic thresholds** — the `ε·10⁻¹/10⁻²/10⁻³` bands are fixed heuristics.
5. **Preconditioning scales worse** — PCG/PBiCGSTAB average 1.63×–3.82× versus 2.68×–5.37× unpreconditioned, which limits the method exactly where preconditioning is required (ill-conditioned systems).

## 12.14 Relation to prior corpus

- **Corrects `_LEDGER_tensor_cores.md`.** That ledger recorded Mille-feuille as `CLOSED_ACCESS (effectively)` / `RELATED_GPU`, with cluster-F membership `UNRESOLVED`, and reasoned from the title that "the named mechanisms are single-kernel persistence and tile-grained precision" rather than the matrix unit. **The full text confirms that reasoning exactly** — no Tensor Core appears anywhere — but the access state was wrong (the author PDF is reachable at `ssslab.cn`) and, read in cluster G rather than cluster F, the verdict is `CORE_GPU`: persistent-kernel grid synchronisation and shared-memory-resident tiles are GPU-specific mechanisms even though matrix units are not involved.
- **Same group as** `GPU-PPoPP26-104` (Trojan Horse, SSSLab/CUPB, Weifeng Liu) and as DASP (SC 2023), which is a *baseline in* `GPU-SC24-102` (SMaT). The SSSLab line — DASP → AmgT → Mille-feuille → PanguLU → Trojan Horse — is one of the two or three most productive sparse-GPU groups in this corpus.
- **Complementary to** `GPU-SC24-102` (SMaT): both are SC 2024 sparse-GPU papers, but SMaT moves sparsity onto the matrix unit while Mille-feuille removes kernel boundaries; they address different bottleneck classes and could compose.
- **Contrast with** `GPU-MICRO24-41` (over-synchronisation in GPU programs), which studies exactly the cost Mille-feuille's Finding 2 measures. Complementary; different method (study vs solver).
- `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The largest measured component of the speedup is the elimination of **CUDA kernel-launch boundaries** — a grid-wide serialisation that exists because a GPU kernel's completion is the only implicit global barrier. Replacing it required an explicit software grid barrier built from `atomicSub`/`atomicAdd` on global counters plus `__threadfence()` busy-waits, chosen over `__grid_sync()` for portability [paper]. On a CPU there is no such boundary and the entire Finding-2 motivation disappears. The second GPU-specific property is that the solver's speed depends on the **matrix tiles staying resident in per-SM shared memory for the whole solve**, which is what sets the ~10⁶-non-zero applicability ceiling.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Synchronisation — claimed and established.** Figure 2 measures >30% of baseline runtime; the best speedups correlate with baseline synchronisation share >50%.
- **Memory — claimed and established.** Figure 11 isolates mixed precision at 1.03×–1.65× depending on the matrix's precision diversity, and honestly reports where it does *not* help.
- **Dependency — claimed and addressed.** The CG dependency chain is enforced in-kernel by `d_s`/`d_d`/`d_a`; the mechanism is described in full. Not separately quantified against a grid-sync alternative — `NOT_IN_PAPER`.
- **Compute — partially claimed** via bypass, but bypass is measured only inside the mixed-precision ablation, not on its own.
- **Load imbalance — claimed weakly.** Tiles are distributed balancing both count and non-zero count, but no imbalance measurement is given. **Not established.**

verdict: `CORE_GPU`

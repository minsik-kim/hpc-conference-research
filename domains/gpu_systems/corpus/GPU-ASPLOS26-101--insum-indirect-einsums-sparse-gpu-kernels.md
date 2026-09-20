# GPU-ASPLOS26-101 — Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `G — Sparse/irregular GPU kernels (SpMM, sparse convolution, formats)`
secondary_topics: `compiler/DSL for GPU kernels; sparse storage format design; Tensor Core code generation; Triton/TorchInductor code generation; H (graph/irregular) overlap via sparse convolution and equivariant tensor products`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2510.17505v1) — introduction/motivation, indirect-Einsum definition and the format-agnostic -> format-conscious conversion, GroupCOO and BlockGroupCOO format definitions and the group-size derivation, the Insum compiler lowering to PyTorch FX, the TorchInductor ops.dot / lazy-broadcasting extensions, evaluation setup and four case studies, the Figure 13 ablation, Table 3 compilation overhead, related work. NO DEDICATED LIMITATIONS SECTION EXISTS — recorded as NOT_IN_PAPER, not filled in.`

## 12.1 Bibliographic facts

- Title: **Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums** [paper]
- Venue: **ASPLOS 2026**; census records session `2C: GPU Systems & Scheduling`, proceedings volume `31V2` [census: `domains/gpu_systems/census/ASPLOS_2026.md`]
- DOI: `10.1145/3779212.3790176` [census; `dl.acm.org` returns 403 from this environment so the DOI was not dereferenced]
- Authors [paper, arXiv 2510.17505]: **Jaeyeon Won, Willow Ahrens, Joel S. Emer, Saman Amarasinghe**. Affiliations: **NOT_STATED in the fetched arXiv abstract page** — `UNKNOWN`, not inferred.
- Publication type: `ARCHIVAL_MAIN_PAPER`; the arXiv item (2510.17505, submitted 2025-10-20) is a `PREPRINT` of the same work.
- Full text used: `https://arxiv.org/html/2510.17505v1` [paper]. A second host is recorded by the census: `https://spice.cs.umd.edu/proceedings/5_Insum.pdf` (not fetched).
- Artifact: **no repository URL was located on the arXiv abstract page or in the fetched HTML** [paper]. `NOT_INSPECTED`. No source symbols are asserted below.

## 12.2 Core question (one sentence)

Can a *single-line* Einsum expression, extended only with the ability to index one tensor by the values of another ("indirect Einsum"), serve as the whole source language for high-performance sparse GPU kernels — with the sparse *format* pushed entirely into the index tensors, so that an existing dense tensor compiler (TorchInductor/Triton) produces one fused gather→MMA→scatter kernel?

## 12.3 GPU/HPC problem translation

- **Compute.** The thing being recovered is Tensor Core occupancy for sparse operands. The paper's stated obstacle is not the sparsity itself but the *compiler*: "TorchInductor defaults to hand-optimized matrix multiplication templates that prevent fusion with gather/scatter operations, generating three separate Triton kernels instead of one" [paper]. So the compute problem is that the MMA path and the indirection path cannot be co-scheduled.
- **Memory.** Indirect access (gather of `B` rows at `AK` positions, scatter-accumulate of `C` rows at `AM` positions) is the dominant cost the format is designed against; the group-size derivation is explicitly a **minimisation of the number of gathers and scatters** [paper].
- **Synchronization.** Scatter-accumulate to a shared output row is resolved "through summation" [paper]; the ablation attributes part of the grouping win to "fewer atomics" [paper, Figure 13 description]. So the target is atomic contention on `C`.
- **Scheduling.** Group size `g` is the tunable that trades per-group work against indirection count; rounded to powers of two "for Triton backend alignment" [paper].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- Two facts about the machine collide. (i) The Tensor Core MMA consumes **dense, statically shaped register fragments**; a compiler can only emit `tl.dot` if the loop nest has fixed, compile-time bounds. (ii) A sparse format's per-row non-zero count is **data-dependent**, so the natural loop bound is dynamic. Einsum, by construction, has fixed bounds — which is exactly why the paper can hand the expression to a dense compiler.
- GroupCOO exists to reconcile these: grouping "maintain[s] fixed loop bounds required by Einsum" [paper] while still not paying ELL's full padding.
- The second root cause is on the *software* side of the hardware boundary: TorchInductor "eagerly broadcasts" all loop variables, which forces "explicit reshape and transpose before `tl.dot`" [paper]. Reshape/transpose of a register fragment is real work on a GPU because the fragment layout is fixed by the instruction, so the fix (lazy broadcasting) is a layout fix, not a bookkeeping fix.

## 12.5 Mathematical / performance model

- **Indirect Einsum, definition** [paper]: an Einsum extended to allow "indexing via values from other tensors", e.g. `C_{X_i} = A_{Y_i,j} * B_j`.
- **COO SpMM as an indirect Einsum** [paper]: with values `AV`, row coordinates `AM`, column coordinates `AK`,
  `C_{AM_p, n} = AV_p * B_{AK_p, n}` — the right-hand side is a **gather**, the left-hand side a **scatter-accumulate**.
- **GroupCOO SpMM** [paper]: `C_{AM_p, n} = AV_{p,q} * B_{AK_{p,q}, n}`, `p` = group, `q` = position in group; `AV` has shape `[num_groups, group_size, ...]`.
- **BlockGroupCOO SpMM** [paper]: `C_{AM_p, bm, n} = AV_{p,q,bm,bk} * B_{AK_{p,q}, bk, n}`, `AV` shape `[num_groups, group_size, bM, bK]`.
- **Format lattice** [paper]: group size 1 ⇒ COO; group size = max non-zeros per row ⇒ ELL. GroupCOO is the interior of that interval.
- **Optimal group size** [paper]: minimising indirect accesses gives `g* ≈ sqrt(S / n)` with `S` the total non-zeros and `n` the number of rows; rounded to a power of two in practice.
- **Compiler size** [paper]: Insum ≈ **500 LoC**, TorchInductor modifications ≈ **800 LoC**.
- **Code-size claim** [paper]: **202×–4491× reduction** versus hand-written implementations (the two endpoints are TorchBSR at 202 LoC of Triton and TorchSparse at 4,491 LoC of CUDA).

## 12.6 Data layout and ownership

- **tensor-level**: `AV` / `AM` / `AK` are ordinary dense tensors. The whole point is that **the format lives in the index tensors, not in the kernel** — "maps the data and metadata of sparse tensor formats onto dense tensor operations through indirect indexing" [paper].
- **group (`p`) and within-group (`q`)**: `AM` stores one row coordinate per *group*, reused across `q`; `AK` stores a column coordinate per non-zero. This is the storage saving over COO.
- **block (`bm`,`bk`)**: BlockGroupCOO's inner dense block is what becomes the MMA fragment.
- **thread → warp → block mapping**: **NOT_IN_PAPER.** The fetched text states no explicit thread/warp map; the mapping is delegated to Triton's tiling of the `ops.dot` loop nest. This is recorded as `UNKNOWN` and is *not* reconstructed — it is a genuine gap in the paper for this cluster's purposes.
- **GPU**: RTX 3090 (24 GB, Ampere) [paper].
- **node/cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- the entire user-facing "kernel" for blocked grouped SpMM ---   [paper]
C[AM[p], bm, n] += AV[p, q, bm, bk] * B[AK[p, q], bk, n]

# --- Insum lowering, three steps ---                                [paper]
# 1. gather RHS indirections
Atmp = torch.index_select(A, dim=1, index=E)      # or torch.gather
# 2. dense einsum
Ctmp = torch.einsum("yr,rx->yx", Atmp, B)
# 3. scatter LHS indirections
C.index_add_(dim=0, index=D, source=Ctmp)

# --- TorchInductor extension: force the MMA path ---                [paper]
for y:
  for x:
    for r:
      ops.dot(C[y, x], A[y, r], B[r, x])          # lowers to tl.dot
```

`ops.dot`, `tl.dot`, `torch.index_select`, `torch.gather`, `torch.einsum`, `index_add_` are the paper's own names [paper]. Nothing here is `[reconstruction]` except the loop ordering, which the paper prints in this form.

## 12.8 Real implementation

`NOT_INSPECTED`. No repository URL was located [paper]. The only version pin the paper gives is a **patched PyTorch at commit `e8304f0`** [paper] — recorded as the paper states it; the commit was not resolved against any repository from this environment, so nothing is asserted about its contents.

Implementation facts asserted only on the paper's own text: the backend is **Triton** reached through **PyTorch FX graphs**; the two extensions are an **`ops.dot` IR node** mapping to **`tl.dot`**, and **lazy broadcasting** which keeps loop variables 1-D (`[RBLOCK,]`) and broadcasts on demand (`r[None,:]` when loading `B`, `r[:,None]` when loading `A`) [paper]. No PTX, no `ldmatrix`, no `cp.async` is mentioned — `NOT_IN_PAPER`.

## 12.9 Kernel execution

kernel → (Triton-chosen) program/block → warp → `tl.dot` instruction. The execution-level novelty is negative rather than positive: the paper's contribution is **removing a compiler-imposed kernel boundary**. Without the extension the pipeline is three Triton kernels (gather, matmul-template, scatter); with it, one. The fusion win is measured separately in the ablation as **+2.6×**, attributed to "eliminat[ing] intermediate materialization" [paper, Figure 13] — i.e. the intermediate `Atmp`/`Ctmp` never reach HBM.

## 12.10 Memory traffic

- **HBM round-trips removed**: the three-kernel form materialises the gathered operand and the matmul result in global memory; the fused form does not [paper].
- **Index traffic**: GroupCOO stores one row coordinate per group instead of one per non-zero [paper]; the `g* ≈ sqrt(S/n)` derivation is a direct minimisation of gather+scatter count [paper].
- **Atomic traffic**: grouping is credited with "reduced memory, fewer atomics" in the ablation [paper].
- No L1/L2/HBM byte-level breakdown is given. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

The Figure 13 ablation on **structured SpMM** (4096×4096, 32×32 dense blocks, RTX 3090) decomposes it [paper]:

1. **COO baseline** — reference.
2. **+ Grouping** → **≈8×**. Cause: fewer indirect accesses and fewer atomics.
3. **+ Blocking** → **≈20×** cumulative. Cause: the dense inner block is what makes `tl.dot` (Tensor Core) legal at all.
4. **+ Tensor Core fusion** → **+2.6×**. Cause: removing the intermediate materialisation between gather, matmul and scatter.
5. **+ Lazy broadcasting** → further gains, reported qualitatively as memory-efficiency [paper].

**Headline results, with all three qualifiers carried** [paper] — all on a single **NVIDIA RTX 3090 (Ampere, 24 GB)**, patched PyTorch `e8304f0`, Triton backend:

| Workload | Suite / dataset | Baseline (as named by the paper) | Speedup |
|---|---|---|---|
| Structured SpMM | 4096×4096, 32×32 dense blocks | TorchBSR (202 LoC Triton) | **1.95×** |
| Unstructured SpMM | **TC-GNN matrix set** | **cuSPARSE** (version `NOT_IN_PAPER`) | **1.20×** |
| Point-cloud sparse convolution | **S3DIS Area 6**, 5 cm voxel quantisation, 128 channels | **TorchSparse** (4,491 LoC CUDA) | **1.14×** |
| Equivariant tensor product | batch 10,000, varying `ℓ_max` | **e3nn** | up to **8.3×** |

Compiler comparisons: **TACO** and **SparseTIR**; compilation/runtime figures for point-cloud convolution [paper, Table 3]: Insum compile 9.9 s + autotune 4.9 s, format conversion 0.55 ms, runtime **0.47 ms**; TACO 0.01 s compile / **253.53 ms** runtime; SparseTIR 0.32 s compile / **1.05 ms** runtime.

**Honest reading of the magnitudes**: against *hand-written expert kernels* the wins are modest (1.14×–1.95×); against *other compilers* they are large. The abstract's "1.14× to 3.81×" range is the paper's own framing of the hand-written comparison [paper]. The 8.3× over e3nn is against a library, not a tuned GPU kernel.

## 12.12 Hardware generation dependence

- Evaluated on **one SKU only: RTX 3090 (Ampere)** [paper]. No H100/Ada/Blackwell results, no AMD. Generalisation across generations is therefore **untested**; this is the single biggest evidential weakness for a paper whose mechanism is Tensor Core code generation.
- The mechanism itself is generation-portable in principle because it emits `tl.dot` and lets Triton choose the MMA shape — but the paper does not demonstrate that. `INFERENCE`, flagged as such.
- Group size is rounded to powers of two "for Triton backend alignment" [paper], so the tuning surface is tied to the backend, not to a named MMA shape.

## 12.13 Limitations

**No dedicated limitations or future-work section exists in the paper** [paper — verified against the fetched HTML]. What can be stated as limitation-shaped evidence *from the paper's own text and numbers*:

- The thread/warp/shared-memory mapping is never specified; all GPU-level scheduling is delegated to Triton. For this cluster that means the paper contributes a *format and a lowering*, not a GPU kernel design.
- Compilation cost is high relative to the competitors it beats at runtime: 9.9 s + 4.9 s autotune vs TACO's 0.01 s [paper, Table 3].
- Single GPU, single SKU, single vendor.
- Load balancing across groups is not addressed. GroupCOO gives *fixed* group size, which is a padding cost on power-law matrices; the paper does not report a padding-overhead measurement. `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Complementary / orthogonal to** `GPU-PPoPP25-01` (FlashSparse) and `GPU-PPoPP25-02` (Acc-SpMM): those hand-design a Tensor-Core SpMM kernel and a sparse format against a *named* MMA shape; Insum hand-designs *no kernel at all* and reaches the matrix unit through `tl.dot`. Insum's BlockGroupCOO and FlashSparse's ME-BCRS are both "store dense blocks, index them indirectly" formats, reached from opposite directions (compiler vs kernel).
- **Same side of the `_LEDGER_tensor_cores.md` distinction as FlashSparse/Acc-SpMM**: Insum runs **dense MMA on dense blocks** (`tl.dot` on `bM×bK` blocks). It does **not** use 2:4 Sparse-Tensor-Core metadata. It therefore belongs with FlashSparse/Acc-SpMM, not with SPIDER / Bridging the Gap / Coruscant / Uni-STC.
- **Competing with** the compiler line it names: TACO, Finch, mlir-sparse, COMET, SparseTIR [paper]. Willow Ahrens is an author of both Finch and this paper, so the Finch relation is a continuation, not a rivalry.
- No existing corpus file covers Insum or indirect Einsums. `NO_EXISTING_ANALYSIS`.
- `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`; an ASPLOS 2026 compiler paper could plausibly sit in it. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — nothing asserted.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — but by a narrower margin than the other papers in this cluster.**

verdict_basis: The *notation* (indirect Einsum) is machine-independent and would work on a CPU. What is GPU-specific is the entire second half of the paper: the contribution only pays off because (a) the dense inner block of BlockGroupCOO is chosen so a **Tensor Core `tl.dot`** becomes legal, (b) the **lazy-broadcasting** fix exists solely to avoid register-fragment reshape/transpose against the MMA's fixed operand layout, and (c) the **fusion** win (+2.6×) is the removal of an HBM round-trip between three GPU kernels. Strip the matrix unit and the register-fragment layout constraint and points (a)–(c) all vanish, leaving a CPU sparse compiler — which is what TACO already is, and which the paper explicitly positions against ("[existing sparse compilers] target CPUs primarily, rarely producing high-performance GPU code" [paper]).

**Bottleneck classes claimed and established** (of compute / memory / dependency / synchronisation / load imbalance):
- **Memory — claimed and established.** The `g* = sqrt(S/n)` derivation and the ≈8× grouping ablation step are both indirection-count arguments, measured.
- **Compute — claimed and established.** The blocking step (≈20× cumulative) is explicitly "enables Tensor Core".
- **Synchronisation — claimed, weakly established.** "Fewer atomics" is asserted in the ablation narrative but not separated from the memory effect by a dedicated measurement.
- **Load imbalance — NOT CLAIMED and NOT ADDRESSED.** Fixed group size is an imbalance-agnostic design; this is the paper's clearest gap versus RoDe / Acc-SpMM-style row-decomposition work.
- **Dependency — not applicable.**

verdict: `CORE_GPU`

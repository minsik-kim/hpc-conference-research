# Tensor Cores, matrix units, numeric formats and precision emulation (taxonomy F)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **STRONG.** Nine deep analyses (taxonomy `F`), all
`CORE_GPU`, all `PUBLIC_FULLTEXT`. Verdict ledger:
`../corpus/_LEDGER_tensor_cores.md`, which records **no paper excluded** in
this cluster: naming a Tensor Core / Matrix Core / MXU / Sparse Tensor Core /
microscaling format in a title is a reliable indicator of a GPU matrix-unit
mechanism. Lineage detail: `../synthesis/GPU_TENSOR_CORE_LINEAGE.md`.

## 1. Problem landscape

A matrix unit is a fixed-shape, fixed-precision multiplier that the rest of the
machine must be bent to fit. Everything in this topic follows from that:
the unit's operand extents (`m16n8k16`, `m64nNk16`, `m256n256k16`) are the real
interface, and a paper's contribution is almost always a *reshaping* — of a
stencil, of a sparse matrix, of a double-precision product, or of the unit's
own integration into the core.

The corpus splits the topic three ways. **Reshape the problem** (stencils,
sparse algebra) with no hardware change. **Reshape the arithmetic** (Ozaki-style
emulation of FP64 on FP8/INT8 pipes). **Reshape the integration** (Virgo moves
the matrix unit out of the SIMT core to a cluster). A fourth, growing group
just **characterises** the unit so the other three can be argued about.

## 2. Key concepts

`mma` / `wgmma` / `tcgen05.mma` and their **issue scope** (warp → warp-group →
warp); MMA fragment shape and operand extents; **dense MMA on dense blocks vs
2:4 Sparse-Tensor-Core metadata** — the distinction this cluster's ledger
insists on and which the sparse ledger preserves; accumulator placement
(register file → TMEM); FP8 / FP4 / TF32 / microscaling formats; Ozaki-scheme
splitting and modular reconstruction; DMMA (FP64 matrix instructions);
input-tile vs output-tile utilisation as a taxonomy of non-GEMM uses.

## 3. Main mechanism families

**Family F1 — lower a non-GEMM kernel onto dense MMA.**
`../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md`
(stencil → matmul);
`../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md`
and `../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md`
(SpMM). No hardware change.

**Family F2 — use the *sparse* unit's metadata, not just the dense one.**
`../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md`
is the corpus's clearest 2:4-metadata paper: the padding zeros that the dense
lowerings multiply by are **never issued**.

**Family F3 — emulate a precision the unit does not have.**
`../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md`
(FP8 vs INT8 for DGEMM emulation) and
`../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md`
(fusing the emulation's product set into one kernel).

**Family F4 — use the FP64 matrix instruction the hardware already has.**
`../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md`.

**Family F5 — change where the unit sits.**
`../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md` decouples the
matrix unit from the SIMT core and gives it its own accumulator SRAM.

**Family F6 — characterise the unit so families F1–F5 can be adjudicated.**
`../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md`.

## 4. Representative papers

- **ConvStencil** (PPoPP 2024) — **MEASURED**. The per-cause breakdown is the
  point, per benchmark (Heat-1D / Box-2D9P / Box-3D27P): **implicit
  stencil2row +22% / +170% / +67%**; **the Tensor Core path itself +76% / +68%
  / +44%**; padding +1% / +14% / +10%; dirty-bits padding +4% / +19% / +13%
  `[paper]`. The layout work, not the matrix unit, is the dominant cause for 2D
  box stencils.
- **FlashSparse** (PPoPP 2025) — **MEASURED** on **H100 PCIe** and **RTX 4090**,
  **515 matrices** (500 SuiteSparse with >10k rows/cols and >100k non-zeros,
  plus 15 graph datasets). Swap-and-transpose alone (8×1 instead of 16×1
  granularity): **1.89× average, up to 3.44× for SpMM**; **2.61× average, up to
  3.85× for SDDMM**, **on H100** `[paper]`. Memory-efficient thread mapping
  alone: **1.34× average on H100, 1.18× average on RTX 4090** — it matters
  *more* on H100. ME-BCRS is a **memory-footprint** result (11.72% average, up
  to 50%), not a speedup.
- **Acc-SpMM** (PPoPP 2025) — **MEASURED** on **RTX 4090 (82.6 TFLOPS TF32 /
  1008 GB/s)**, **A800 80 GB PCIe (156 TFLOPS / 1935 GB/s)** and **H100 80 GB
  SXM (494.7 TFLOPS / 3.35 TB/s)**, 414 SuiteSparse + 10 power-law matrices,
  N = 128/256/512, TF32. Average over cuSPARSE: **2.52× (RTX 4090, max 5.11×)
  → 1.91× (A800, max 4.68×) → 1.58× (H100, max 3.60×)** `[paper]`. **The
  speedup falls as HBM bandwidth rises**, which is consistent with the gains
  being substantially memory-pipeline gains `[inference, stated as such in the
  analysis]`.
- **SPIDER / SpTCStencil** (PPoPP 2026) — **MEASURED** on **A100-80GB PCIe,
  CUDA 12.8, cuDNN 9.8.0**, 1D stencils (radius 1–2) and 2D star/box (radius
  1–3): **6.20× over cuDNN, 4.71× over DRStencil, 3.13× over TCStencil, 1.88×
  over ConvStencil, 1.63× over LoRAStencil, 1.35× over FlashFFTStencil**
  `[paper]`. The mechanism is a **hardware skip**, not a software pruning.
- **CuBie** (PPoPP 2026) — **MEASURED** across **A100 / H200 / B200**. Builds a
  2×2 taxonomy (input-tile × output-tile utilisation) and then runs two
  ablations that a bare speedup number would have hidden `[paper]`:
  CUDA-core-vs-Tensor-Core retention is **~40–60% for Quadrant I** (GEMM, PiC,
  FFT, Stencil), **<40% for Quadrants II–III** (Scan, Reduction — the
  constant-operand trick has no CUDA-core analogue) and **60–90% for Quadrant
  IV** (BFS, GEMV, SpMV, SpGEMM — memory-bound). Removing the MMU-induced
  redundancy gives Scan/Reduction **0.34–0.79×** — *the redundant computation
  is itself beneficial* — while SpMV gets **1.0–1.2×**, i.e. the matrix-unit
  formulation is arguably a net loss there. Energy-delay-product reductions
  (geomean, H200 focus): **Quadrant I ~64%, II–III ~36%, IV ~80%**, with TC
  often drawing **>400 W instantaneous** but for much shorter duration.
  Accuracy: **TC and CC are numerically identical at FP64**, but the *MMU
  formulation* changes summation order — SpMV's redundancy-removed version is
  **1–2 orders of magnitude worse** (2.0E-08 vs 7.1E-10).
- **FP64 Tensor Cores for high-order FEM** (ISC 2026) — **MEASURED** on
  **GB200** and **GH200**, 540M DOF, single GPU, Table VI `[paper]`: PA
  baseline 23.78 / 18.73 GDOF/s → DMMA PA 33.72 / 25.27 → Fused PA 29.28 /
  24.04 → **DMMA Fused PA 46.60 / 36.15**, i.e. **≈1.96× (GB200) and ≈1.93×
  (GH200)**. Energy per DOF **+72% (GB200)** and **+83% (GH200)**. *The
  analysis explicitly rejects an earlier summarisation that reported "83%
  (GB200) and 27% (GH200)" as inconsistent with Table VI.* Extreme scale on
  **Alps at CSCS**: weak scaling 36 → 2,304 nodes (144 → 9,216 GH200), largest
  problem **~9.28 trillion DOF**.
- **Ozaki II / FP8 DGEMM emulation** (SC 2026) — **MEASURED** on RTX 4090
  Laptop, RTX 5080, **AMD Radeon RX 9070 XT**, GH200, GB10 and **B200 SXM**,
  `m=n=k` 1024–16384. Argues against FP8 and for INT8 on four decomposed
  grounds: **3 FP8 GEMMs per modulus vs 1 INT8 GEMM** (Karatsuba
  reconstruction), **≈2× workspace**, **FP8's 4 exponent bits carry no
  information** in a fixed-point scheme, and **FP32 accumulation forces
  `k ≤ 2^16`-class blocking** `[paper]`.
- **EmuGEMM** (SC 2026) — **MEASURED** on **GH200 (SM90)** and **B200
  (SM100)**. Up to **1,639 TOP/s on Hopper (83% of INT8 peak)** and **3,654
  TOP/s on Blackwell (81% of peak)** — *integer-op throughput of the emulation
  kernel as a fraction of the part's INT8 matrix peak, **not** an
  FP64-equivalent FLOP/s number* `[paper]`. Accumulator residency moves from RF
  (SM90) to **TMEM** (SM100), which is what relieves the register pressure that
  would otherwise cap the product count `p`.
- **Virgo** (ASPLOS 2025) — **SIMULATED/SYNTHESISED, no NVIDIA silicon at all.**
  The "Volta-style", "Ampere-style" and "Hopper-style" baselines are the
  authors' **RTL abstractions** at 8 lanes/warp and 400 MHz on a 16 nm PDK, on
  a **Vortex** RISC-V GPGPU plus **Gemmini** `[paper]`. **Active on-chip power
  −67.3% vs Ampere-style and −24.2% vs Hopper-style; energy −80.3% and
  −32.5%** — all Virgo-vs-*model*. MAC utilisation **86.5% vs Hopper-style
  77.0%** for 1024×1024 GEMM, and **65.7% vs Ampere-style 35.1%** for
  FlashAttention-3. Most of the saving is in the **SIMT core, not in the MACs**.

## 5. Historical lineage

Two lineages verified from the papers' own text; the full chains are in
`../synthesis/GPU_TENSOR_CORE_LINEAGE.md`.

**Dense-MMA-on-blocks for SpMM**, end to end from read text
(`../corpus/_LEDGER_sparse_irregular.md` §7.1): **SMaT (SC 2024)** fixes the
block at the `m16n8k16` operand shape and attacks *tile count* →
**FlashSparse (PPoPP 2025)** attacks *tile shape* by exploiting `n = 8` →
**Acc-SpMM (PPoPP 2025)** attacks the *schedule* → **Insum (ASPLOS 2026)**
attacks the *source language*. All four run **dense MMA on dense blocks, not
2:4 metadata** — a distinction this cluster's ledger introduced and the sparse
cluster confirmed from full text.

**Stencil-on-matrix-unit**: TCStencil → ConvStencil (PPoPP 2024) →
LoRAStencil (SC 2024) → FlashFFTStencil → **SPIDER (PPoPP 2026)**, which is
the first to leave the dense path for the 2:4 sparse unit `[paper, SPIDER's
own baseline list]`.

**Issue scope and accumulator placement** moved in opposite directions across
three generations — warp `mma` → warp-group `wgmma` → warp `tcgen05.mma`, and
register file → register file → **TMEM**. Visible only by reading
`../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md` and
`../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md`
together; EmuGEMM is the corpus's evidence that a software design *changes* in
response (`tcgen05.mma` accumulating in TMEM on SM100).

## 6. Implementation families

`REAL_SILICON` with public artifacts: ConvStencil, FlashSparse, Acc-SpMM,
SPIDER, CuBie, Ozaki II, EmuGEMM, the ISC 2026 FEM work. `RTL_SYNTHESIS` on an
open-source GPGPU substrate: Virgo (Chisel, Vortex + Gemmini). Virgo's power
and energy numbers are **RTL/synthesis estimates against RTL baselines**, and
this file never restates them as measurements of V100/A100/H100.

## 7. Important disagreements / tensions

**T1 — "SpMM on Tensor Cores" names two incompatible mechanisms.** FlashSparse,
Acc-SpMM, SMaT and Insum run **dense MMA on denser blocks**; SPIDER, "Bridging
the Gap", N:M reordering, Coruscant and Uni-STC use **actual 2:4 Sparse-Tensor-
Core metadata**. `../corpus/_LEDGER_tensor_cores.md` introduced the distinction
and `../corpus/_LEDGER_sparse_irregular.md` §5 corrected two of its own rows
from read full text to preserve it. A survey that merges the two would be
comparing a *format* result with a *hardware skip* result.

**T2 — FP8 is the newer pipe and the corpus's FP64-emulation paper argues
against it.** Ozaki II gives FP8 access to a **30× faster matrix pipe on B300
tabulated specs (4500 TFLOP/s vs 150 TOP/s INT8)** and still concludes INT8
wins, for four separately measured reasons (§4). This is a live disagreement
with the general direction of vendor investment, argued from measurement.

**T3 — the matrix unit's "redundant" work is sometimes the point, and
sometimes a net loss.** CuBie's two ablations disagree with each other by
quadrant: for Scan/Reduction, removing the MMU-induced redundancy gives
**0.34–0.79×** (the unit does the redundant work for free); for SpMV it gives
**1.0–1.2×** (the formulation was a net loss). And removing it *hurts accuracy*
on SpMV by 1–2 orders of magnitude, because the redundancy was acting as a more
stable summation order `[paper]`. "Should I use the matrix unit for X" has no
single answer in this corpus.

**T4 — a matrix-unit speedup shrinks as the part gets better.** Acc-SpMM's
cuSPARSE advantage falls **2.52× → 1.91× → 1.58×** as HBM bandwidth rises
**1008 GB/s → 1935 GB/s → 3.35 TB/s** `[paper]`. Any matrix-unit sparse result
quoted without its part is close to meaningless.

**T5 — the graph-on-matrix-unit question is answered "no" by the same
authors.** `../corpus/_LEDGER_sparse_irregular.md` records that **BerryBees**
(PPoPP 2025) does BFS on bit Tensor Cores, and that **Niu and Casas — the same
authors — wrote DiggerBees one year later using no matrix unit at all** for DFS
(`../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md`).
CuBie, from the same lab, places BFS/SpGEMM in the quadrant where the unit
helps least. Direct evidence that this community does not regard matrix-unit
exploitation as the general answer to irregularity.

**T6 — Virgo is contemporaneous with, and not a claim about, Blackwell.** It
does not address TMA, TMEM or thread-block clusters, treating them as
"orthogonal concerns" `[paper]`. Real silicon has since moved part-way toward
its accumulator-disaggregation argument (TMEM), but **the paper makes no claim
about Blackwell and none should be inferred**
(`../../../governance/ANTI_HALLUCINATION_RULES.md`).

## 8. Current limitations

**Bounded by full-text access, and the ledger says where.** Several SC 2025 /
ISCA 2025 / MICRO 2025 papers in this cluster are **genuinely open access (some
CC BY) and unreachable from this environment**; they are recorded
`PENDING_FULLTEXT`, **not** `CLOSED_ACCESS`, with the reason stated per row.
`dl.acm.org` → 403, `ieeexplore.ieee.org` → 418, `dblp.org` robots-blocked.
That is an access-path fact about this environment, not a statement about
licence — see `../synthesis/GPU_PENDING_FULLTEXT.md`.

The concrete consequences:
- The **2:4-metadata branch has one deep analysis** (SPIDER). Its siblings —
  Bridging the Gap (SC 2025), Coruscant (MICRO 2025), Uni-STC (HPCA 2026),
  N:M reordering — are verdict-only. T1 therefore rests on one read paper on
  one side and four on the other.
- Of the cluster's verdicts, **five are `RELATED_GPU`** and all five are
  *application*-led papers (LLM serving, KV cache, attention, a CG solver) that
  use the matrix unit without contributing a matrix-unit mechanism; **seven are
  `UNRESOLVED`**, split between unverifiable titles (2) and papers where
  GPU-vs-custom-unit could not be established from the title alone (5)
  (`../corpus/_LEDGER_tensor_cores.md` §4).
- One **ID collision** was reconciled centrally on 2026-09-18: `GPU-ISC26-01`
  was held by two files; PICO (first writer) keeps it and the ISC 2026
  FP64-Tensor-Core paper was reissued as `GPU-ISC26-02`.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. Does the dense-MMA line (T1) survive on a part where 2:4 metadata is cheap?
   SPIDER is the only read data point and it is A100-only.
2. Ozaki II's case against FP8 rests partly on **FP32 accumulation forcing
   `k ≤ 2^16`-class blocking**. Does Blackwell's TMEM accumulator change the
   arithmetic of that argument? EmuGEMM shows TMEM changes the *design* but
   does not answer the format question.
3. CuBie's Quadrant IV (BFS, GEMV, SpMV, SpGEMM) retains 60–90% on CUDA cores.
   What, if anything, justifies matrix-unit work there — and does the accuracy
   effect in T3 count as a reason on its own?

## 10. Deeper lookup paths

`../corpus/_LEDGER_tensor_cores.md` (verdicts, access states, §3 access
summary, §4 verdict summary, §5 ID record) → the nine analyses above →
`../synthesis/GPU_TENSOR_CORE_LINEAGE.md` for the full chains →
the papers and their pinned artifacts.
Cross-topic: `sparse_irregular.md` (which owns SMaT, Insum and the
no-matrix-unit counter-evidence), `gpu_core_execution.md` (issue scope and
accumulator placement across generations),
`fixed_function_repurposing.md` (the structural parallel: reshaping a problem
to fit a frozen unit's predicate, with no hardware change).

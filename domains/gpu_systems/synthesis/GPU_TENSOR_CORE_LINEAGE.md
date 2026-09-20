# GPU_TENSOR_CORE_LINEAGE — three disjoint branches, one meeting point

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
source: `_LEDGER_tensor_cores.md` (42 assigned papers, 10 priority, 9 deep
analyses) and `_LEDGER_sparse_irregular.md` §5 and §7.1.

---

## 0. The central finding

The expected progression is:

```
scientific kernels -> sparse kernels -> precision emulation -> new numeric formats
```

**This is not one citation chain. It is three largely disjoint branches, and they
meet in exactly one paper.**

```
  BRANCH A                    BRANCH B                     BRANCH C
  Scientific / non-GEMM       Sparse kernels               Precision emulation
  kernels on the matrix unit  on the matrix unit           on the matrix unit
        |                           |                             |
  TCStencil                   TC-GNN, VectorSparse,          M3XU (SC 2024)
     -> ConvStencil              CLASP, Magicube,                 |
     -> LoRAStencil              DTC-SpMM                    Ozaki I / Ozaki II,
     -> FlashFFTStencil            -> SMaT                    OzIMMU, INT8-Ozaki
     -> SparStencil / SPIDER       -> FlashSparse | Acc-SpMM       |
     (+ FP64 FEM; BerryBees;       -> Insum                  -> Ozaki-II FP8 (SC'26)
      tcFFT; TCU-Scan;             (+ the separate 2:4          | EmuGEMM (SC'26)
      QR / tridiagonalisation)      SpTC sub-branch)             |
        |                           |                             |
        +---------------------------+-----------------------------+
                                    |
                    GPU-PPoPP26-02 (Cubie, PPoPP 2026)
              the ONE paper whose reference list contains all three
```

**The evidence for disjointness is the reference lists themselves.** Read
FlashSparse's related work and you find TC-GNN, DTC-SpMM and cuSPARSELt — no
Ozaki, no stencil work. Read EmuGEMM's and you find Ozaki, Uchino and cuBLAS
emulation — no SpMM, no stencils. Read ConvStencil's and its only named prior art
is TCStencil. Each branch cites its own ancestors and essentially nothing across.

**The meeting point is a characterisation paper, not a member.**
[`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
(Cubie) cites, in one reference list `[paper]`: ConvStencil [11], LoRAStencil
[101] (its stencil baseline), FlashFFTStencil [28]; tcFFT [41] (its FFT
baseline), FFT & NTT on tensor cores [23, 75]; DASP [51] (its SpMV),
**AmgT-SpGEMM [53]** (its SpGEMM), BerryBees [59] (its BFS), general sparse GEMM
[44, 79, 98]; TCU-Scan and TCU-Reduction [17]; QR via Householder [39] and
tridiagonalisation [87]; prior characterisation by Domke et al. [21], Markidis et
al. [54] and Schieffer et al. [77, 78] on **AMD matrix cores**; and, in its
forward-looking FP64 discussion, the Ozaki-scheme line. Cubie is the integrative
node **because it is a benchmark suite**, which is a different kind of object from
the papers it cites.

**A fourth branch — numeric formats — is named in the expected progression but is
almost entirely unreachable.** Avant-Garde (ISCA 2025, GPU microarchitecture for
FP8 and Microscaling formats) is `PENDING_FULLTEXT` / abstract-only; MXBLAS
(SC 2025) is `PENDING_FULLTEXT`; MXFFP (ISCA 2026) is `CLOSED_ACCESS` and
`UNRESOLVED`. **No deep analysis exists for any of them**, so no edge into or out
of the format branch can be asserted. `NOT_ESTABLISHED`. The one author-level
thread is that **Dongho Ha and Won Woo Ro co-author both Avant-Garde and MXFFP**
`[author-overlap]` — which the tensor-cores ledger correctly labels as "an
inference about the authors, not evidence about this paper."

---

## 1. Branch A — scientific and non-GEMM kernels on the matrix unit

### 1.1 The verified chain

```
TCStencil — "the only work that applies Tensor Cores to stencil computation"
            (ConvStencil's own statement of its only prior art) [paper]
        |
        v
ConvStencil (PPoPP 2024, Best Paper) — stencil -> GEMM by dual tessellation
        |  [paper] SPIDER cites it as [11] and benchmarks against it;
        |          Cubie cites it as [11] for the stencil pattern
        |
        +--> LoRAStencil (SC 2024) — low-rank decomposition exploiting symmetry
        |       [paper] SPIDER cites it as [49] and measures it at ~2.94x the
        |       theoretical-minimum computation for Box-2D3R; Cubie's stencil baseline [101]
        |
        +--> FlashFFTStencil (PPoPP 2025) — FFT route, raising arithmetic intensity
        |       [paper] SPIDER cites it as [19] and measures itself 1.35x faster —
        |       i.e. it is the current TC-stencil performance reference point
        |
        +--> SparStencil (SC 2025) ... SPIDER (PPoPP 2026)   [see §5.3: NOT_CITED, UNRESOLVED]
```

Anchors: [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md),
[`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md).

This is the **tightest citation chain in the whole tensor-core area** — five
members, each citing and quantitatively measuring against its predecessors.

### 1.2 The non-stencil members of the branch, and what they contribute

- [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md)
  — high-order FEM on **native FP64 `m8n8k4` DMMA**, validated to **9,216 GH200 on
  Alps**. Its mechanism is the one that most sharply defines the branch: it uses
  the FP64 Tensor Core as a **shared-memory-traffic-reduction device
  (9,000 → 1,960 bytes)** rather than for arithmetic throughput, exploiting
  warp-cooperative operand sharing ("each element loaded only once among the
  threads in a warp"), with explicit `f_m/f_n/f_k` thread-to-fragment maps, a
  `[0,2,1,3,4,5,6,7]` bank-conflict permutation, per-lane shared-memory address
  tables, and hand-written PTX in place of CUTLASS/cuBLAS.
- **BerryBees** (PPoPP 2025, watchlist) — BFS frontier expansion as Boolean matrix
  products on the **bit** `mma m8n8k128` path (XOR-popcount semantics). Cubie uses
  it as its BFS baseline and reports BFS at **2.6–3.0x** via that instruction
  `[paper, Cubie]`. This is the clearest case of a matrix unit used for a
  genuinely non-arithmetic kernel.
- Named by Cubie but with no corpus analysis: tcFFT, TCU-Scan/TCU-Reduction, QR
  via Householder, tridiagonalisation, FFT & NTT on tensor cores.

### 1.3 The branch's own internal negative

The same authors who put BFS on bit Tensor Cores (Niu, Casas — BerryBees,
PPoPP 2025) wrote **DiggerBees one year later using no matrix unit at all** for
DFS, and used BerryBees as a *baseline*
([`GPU-PPoPP26-105`](../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md))
`[author-overlap]` + `[paper]`. **The graph-on-GPU community does not regard
matrix-unit exploitation as the general answer to irregularity**, and the evidence
is the same people declining to reuse it.

The branch's premise is also under direct interrogation from inside: **"Do We Need
Tensor Cores for Stencil Computations?"** (SC 2026, Best Student Paper nominee) is
by the **same SJTU group as SPIDER** `[author-overlap]`. It is the single most
important watchlist item for this area and has no public full text.
`NOT_ESTABLISHED`.

---

## 2. Branch B — sparse kernels on the matrix unit

### 2.1 The verified chain

```
TC-GNN ("first GNN framework on TCs") ; VectorSparse ("evolution of Sputnik for
locality") ; CLASP ("column-vector pruning") ; Magicube ("low-precision integer
optimization") ; DTC-SpMM ("previous state-of-the-art with reordering and
pipelining") — all 16x1 granularity
        |  [paper] cited AND benchmarked by both PPoPP'25 papers
        v
SMaT (SC 2024)        — fixes the block AT the m16n8k16 operand shape;
  |                      attacks TILE COUNT by Jaccard row clustering
  |  [paper] direct precursor
  v
FlashSparse (PPoPP 2025)   ||   Acc-SpMM (PPoPP 2025)     [NOT_CITED — see §2.3]
  attacks TILE SHAPE            attacks the SCHEDULE
  |
  v
Insum (ASPLOS 2026)   — attacks the SOURCE LANGUAGE, reaching the same MMA
                        through Triton's tl.dot; hand-designs no kernel at all
```

Anchors: [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md),
[`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md),
[`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md),
[`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md).

Insum's relation to the two PPoPP'25 papers is **orthogonal, not successive**:
Insum's BlockGroupCOO and FlashSparse's ME-BCRS are both "store dense blocks,
index them indirectly" formats **reached from opposite directions** — compiler
versus kernel `[inference]`. Insum's own competing line is a compiler line: TACO,
Finch, mlir-sparse, COMET, SparseTIR `[paper]`. Willow Ahrens authors both Finch
and Insum, so the Finch relation is a continuation rather than a rivalry
`[author-overlap]`.

### 2.2 The branch's own contested internal edge

**SMaT loses to DASP on `dc2`** — 2.5 GFLOP/s against DASP's 69.1 GFLOP/s, a ~28x
gap `[paper]`, SuiteSparse `dc2`. DASP (SC 2023) is a non-matrix-unit SSSLab
method that SMaT uses as a baseline. A *static* schedule, however well the matrix
is reordered first, still loses by ~28x on a power-law block distribution. This is
a real, citable tension between two SC-era Tensor-Core-adjacent sparse lines and
it belongs with any citation of SMaT.

A second internal signal, from Acc-SpMM's own three-generation table: **speedup
over cuSPARSE *falls* with newer, higher-bandwidth parts — 2.52x on RTX 4090,
1.91x on A800, 1.58x on H100** `[paper]`.

### 2.3 Convergent independent discovery: the operand swap

**This is the most important lineage fact in the branch, and it is a non-citation.**

[`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md)
(FlashSparse) and [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md)
(Acc-SpMM) appeared in the **same PPoPP 2025 session — "S8 Tensor Cores"** — over
the same SuiteSparse corpus against the same baselines (cuSPARSE, TC-GNN,
DTC-SpMM), and **independently identified the same insight**:

- **FlashSparse** calls it **swap-and-transpose** and derives it from
  `A x B = (Bᵀ Aᵀ)ᵀ`: because the `mma.m16n8k*` family has asymmetric extents
  `m = 16` and `n = 8`, swapping the operands lets the sparse blocking drop from
  16x1 to **8x1**, removing **43% of MMA invocations**; a column shuffle then makes
  8 lanes coalesce into one 32-byte transaction `[paper]`.
- **Acc-SpMM** calls it a **"swapped mma … for improved partitioning into 8x8 TC
  blocks"** `[paper]`.

**Neither cites the other** — `NOT_CITED`, same submission cycle.

Two consequences worth keeping separate:

1. **What the convergence means.** That the `n = 8` operand asymmetry was the
   field's *obvious* next opportunity in 2024/25. Two groups reaching it
   simultaneously is stronger evidence for that than either paper's own novelty
   claim.
2. **They are not duplicates.** Having found the same primitive they then diverge
   completely: FlashSparse invests in granularity + coalescing + a leaner format
   (ME-BCRS); Acc-SpMM invests in reordering + a bitmap format + an async
   `cp.async` double-buffered pipeline + IBD load balancing, and positions itself
   as *breadth* ("systematic optimizations across algorithm level, memory access
   patterns, and instruction-level parallelism that prior works left
   unexploited") rather than as a single insight `[paper]`.

### 2.4 Sparse formats are designed around instruction tile sizes

Across the branch the storage format is not an independent design choice — **it is
a function of the MMA instruction's fixed extents.** This is what makes the branch
a branch.

| Paper | Format | The instruction fact that fixes it |
|---|---|---|
| [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md) SMaT | BCSR with a 16x8 block | **"The block shape 16x8 is not a tuning parameter; it is the `m16n8k16` operand shape"** `[paper]`. Any generation change to the MMA shape changes the format |
| [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md) FlashSparse | ME-BCRS, 8x1 vector granularity | defined relative to the instruction's `k` extent, after the swap exposes `n = 8` |
| [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md) Acc-SpMM | BitTCF; `TCLocalBit` is **one `uint64`** | because **an 8x8 TC block has exactly 64 positions**. Storage model `(⌈M/8⌉ + NumTCBlock x 11 + 2) x 4` bytes, written in the instruction's 8-row window `[paper]` |
| [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md) SPIDER | 2:4 group alignment, `L = 2r+2`, column swap `j ↔ j+(2r+2)` | the 2:4 **metadata contract**: "≤2 non-zeros per 4-element group", plus the `mma.sp m16n8k16` per-thread `.f16x2` register layout `[paper]` |
| [`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md) Insum | BlockGroupCOO | the exception that proves the rule: it names *no* MMA shape, because `tl.dot` lets Triton choose one. Group size is rounded to powers of two "for Triton backend alignment" — tied to the backend, not to a named shape `[paper]` |

**The practical consequence**: every format in this branch except Insum's is a
generation-coupled artefact. SMaT says so in one sentence.

---

## 3. Branch C — precision emulation

### 3.1 The hardware regression that drives the branch

The emulation branch exists because **vendors are withdrawing the precisions it
replaces.** Two independent measurements, from two papers:

- **Native FP64 matrix throughput is regressing.**
  [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
  measures **B200 at ~30 TFLOP/s FP64 against H200's ~67 TFLOP/s** and warns this
  "may directly undermine FP64 MMU adoption", calling for architectural roadmaps to
  "preserve and materially strengthen FP64 MMU capability". *Qualifier: that
  paper's own Figure 12, FP64 matrix-unit throughput, B200 vs H200.*
- **INT8 matrix throughput is being withdrawn in favour of FP8.**
  [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md)
  tabulates **B300 (Blackwell Ultra) at 150 TOP/s INT8 against 4500 TFLOP/s FP8**.
  *Qualifier: the paper's Table I, vendor specifications as tabulated —* **B300 was
  not measured**, and no measured B300 number may be reported from that paper. On
  the **measured** B200, INT8-Ozaki-II is ~2.1x faster than FP8-Ozaki-II at 16384³
  (137–138 vs 61–65 TFLOP/s), so the *pivot* is a specification-driven forecast,
  not yet a measured inversion.

**The Cubie measurement is the strongest available corroboration that FP64
emulation on low-precision matrix engines is becoming *necessary* rather than
merely clever** — and it comes from a different paper than the emulation papers
themselves, which is what gives it force. It is also the subject of an unresolved
tension with the FP64-FEM paper; see §6.1.

### 3.2 The verified chain, and the branch's own split

```
M3XU (SC 2024) — high-precision and complex GEMM from low-precision MXUs
   [the earliest item in this branch; CLOSED_ACCESS, watchlist,
    and "MXU" may denote a non-GPU matrix unit — GPU centrality UNVERIFIED]
        |
Ozaki Schemes I and II ; OzIMMU ; INT8-based Ozaki implementations ;
FP16/FP8 emulation via Ozaki-I
        |  [paper] cited by BOTH SC 2026 papers
        +------------------------------+
        |                              |
GPU-SC26-01 (Ozaki-II + FP8)      GPU-SC26-02 (EmuGEMM)
the NUMERICS track                the KERNEL-ENGINEERING track
"which number format and          "how to write the kernel":
 which moduli", then calls         one fused warpgroup kernel replacing
 cublasGemmEx                      a sequence of vendor GEMM launches
        ^                              |
        +---- [paper] EmuGEMM cites "Ozaki et al." and "Uchino et al."
              — i.e. it cites the authors of GPU-SC26-01 as the
                implementations it optimises
```

Anchors: [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md),
[`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md).

**The split into a numerics track and a kernel-engineering track is the branch's
defining structure**, and the two papers state their division of labour cleanly
enough that it is a finding rather than an observation.

Two further facts worth carrying:

- **EmuGEMM benchmarks against a *vendor-shipped* emulation feature** —
  "cuBLAS Scheme I emulation" is a measured baseline. Academic work benchmarking
  against a vendor emulation path is new; that feature did not exist a generation
  earlier `[paper]`.
- **EmuGEMM's O(p²) → O(p) operand-load result is a direct consequence of
  accumulator placement.** Fusing is feasible at all because the accumulators
  live somewhere the epilogue can reach: the register file at SM90
  (`wgmma.mma_async`, `tM=64, tK=32`) and TMEM at SM100 (`tcgen05.mma`,
  `tM=128, tK=32`). Numbers, with their qualifiers `[paper]`: **GH200/SM90 —
  1,639 TOP/s = 83% of INT8 peak, 1.4x cuBLAS TF32, up to 2.3x ZGEMM**;
  **B200/SM100 — 3,654 TOP/s = 81% of peak, 1.7x cuBLAS TF32, up to 5.5x ZGEMM**.
  **Do not restate a Hopper number as a Blackwell number or vice versa.** Ampere
  is not evaluated and the design does not transfer there as written — neither
  `wgmma` nor `tcgen05` exists on A100.

### 3.3 The hardware facts the branch is built on

- **FP8_E4M3 exact-integer range and representational holes**; **FP32 (not INT32)
  MMA accumulation forces `k ≤ 2^16`** `[paper]`,
  [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md).
- **INT8 x INT8 → INT32 accumulate type is what makes modular reduction fusable**
  `[paper]`, [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md).
- **CDNA-era FP8 is a different variant**: the artifact's HIP branch is
  `HIP_R_8F_E4M3_FNUZ`, not E4M3 `[code]`. And `arch == 90` (SM90) and
  `arch == 121` special-cases in the batching logic are direct evidence that
  workspace batching had to be **tuned per generation** `[code]`.
- **The one AMD part measured by the Ozaki-II paper is a Radeon RX 9070 XT
  (RDNA-class consumer), not a CDNA3 MI300.** MI300X/MI325X/MI350X/MI355X are
  named as *targets* only. **Do not claim MI300X emulation measurements from that
  paper** `[paper]`.

---

## 4. The architecture side: the one paper that proposes changing the contract

Every kernel-level paper in all three branches takes the fragment shape and the
register-anchored operand contract as **given** and works around it.
[`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md)
(Virgo) is the only assigned paper that proposes **changing** it — a cluster-level
matrix unit with a dedicated accumulator SRAM, 2-D (bank x subbank) shared-memory
banking, unaligned-lane filtering and split read/write paths.

Its cited prior work, from its own related work `[paper]`: Tensor Core
microarchitecture studies ([34], [39], [10]), **Gemmini** [21], **Vortex** [42],
register-pressure mitigation (**INTERPRET** [30], **Duplo** [29]) and decoupled
access/execute [38]. Self-claim, recorded as the authors' and not verified: "the
first effort to integrate a matrix unit at the core cluster".

**The generation-hygiene warning that must travel with Virgo**: its
"Volta-style", "Ampere-style" and "Hopper-style" baselines are the authors' **RTL
abstractions** at 8 lanes/warp and 400 MHz on a 16 nm PDK — **not** measurements of
V100, A100 or H100. Every Virgo comparative number is Virgo-vs-*model*. It
explicitly does **not** address TMA, TMEM or thread-block clusters, treating them
as orthogonal `[paper]`. Note the irony and do not overread it: **Blackwell's TMEM
is a dedicated on-chip accumulator store, i.e. real silicon has since moved
part-way toward Virgo's accumulator-disaggregation argument.** Virgo and that
Blackwell feature are contemporaneous; **Virgo makes no claim about Blackwell and
none should be inferred.**

Architecture neighbours with no reachable full text: *Cooperative Warp Execution
in Tensor Core for RISC-V GPGPU* (HPCA 2025 — the closest neighbour, attacking
warp-cooperative *issue* where Virgo attacks cluster-level *disaggregation*),
*Uni-STC* (HPCA 2026 — generalising the 2:4-only metadata contract that every
software SpTC paper has to work around; **Cubie cites Uni-STC in its future-work
discussion**, corroborating relevance), *Coruscant* (MICRO 2025, GPU-kernel /
Sparse-Tensor-Core co-design, artifact public and uninspected).

---

## 5. Two distinctions the corpus insists on

### 5.1 Fragment-shape mismatch: two opposite resolutions

Every kernel that maps a non-GEMM operation onto a matrix unit hits the same
obstacle — **the target operation's natural shape does not fill the fragment.**
Two papers in this corpus resolve it in **opposite** directions, and the contrast
is the single clearest design-space axis in the area.

| | [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md) ConvStencil | [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md) FP64 FEM |
|---|---|---|
| Instruction | A100 FP64 `m8n8k4` | A100/H100-class FP64 `m8n8k4` (GH200, GB200) |
| The mismatch | the natural stencil use fills **n = 1 of n = 8**, i.e. 12.5% | a `25x5x4` element block into `m8n8k4` |
| Resolution | **Reshape the algorithm.** Dual tessellation fills **7/8 of the n extent**, taking utilisation 12.5% → 87.5% | **Accept the padding waste** and buy warp-level operand sharing instead — each element loaded only once among the warp's threads |
| What is bought | arithmetic efficiency | **shared-memory traffic: 9,000 → 1,960 bytes** |
| What is paid | layout work — the measured 4-way breakdown shows the *layout*, not the Tensor Core, is the dominant cost | wasted matrix-unit arithmetic |

Both are FP64 `m8n8k4` papers on structured-grid/PDE kernels, hitting the same
obstacle, resolving it oppositely. **Neither is wrong; they optimise different
scarce resources.** The `12.5% → 87.5%` figure is arithmetic on the **A100 FP64
shape** and does not generalise: on a generation where the FP64 matrix shape
differs, or where FP64 matrix-to-vector throughput ratio differs, both the
baseline fraction and the dual-tessellation payoff change. ConvStencil contains no
H100/H200 or B200 measurement, no `wgmma`, no TMA, no TMEM.

### 5.2 Dense MMA on dense blocks is NOT the Sparse Tensor Core

**This is the distinction most likely to be conflated, and the corpus checks it
per paper rather than assuming it.**

| Paper | Which path | Verification |
|---|---|---|
| [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md) SMaT | **dense MMA on dense blocks** | BCSR with `m16n8k16`, and the text states it is "not NVIDIA's structured 2:4 sparsity format introduced in Ampere" `[paper, verified in the fetched text]` |
| [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md) FlashSparse | **dense MMA on denser 8x8 blocks** | "a granularity result, not a structured-sparsity-hardware result". **cuSPARSELt appears only as a baseline** |
| [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md) Acc-SpMM | **dense MMA on 8x8 blocks** | 2:4 SpTCs not used; cuSPARSELt is a baseline only |
| [`GPU-ASPLOS26-101`](../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md) Insum | **dense MMA on dense blocks** | `tl.dot` on `bM x bK` blocks; no 2:4 metadata |
| [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md) SPIDER | **true 2:4 Sparse Tensor Core** | `mma.sp m16n8k16` in **FP16**; the `L = 2r+2` and `j ↔ j+(2r+2)` constants exist *only* to satisfy the 2:4 metadata contract |
| Bridging the Gap (SC 2025), N:M Graph Reordering (PPoPP 2025), Coruscant (MICRO 2025), Uni-STC (HPCA 2026) | **true 2:4 / N:M SpTC** | title/census level; watchlist |

**Why the conflation matters and is not pedantry.** The two groups differ in three
load-bearing ways:
1. **Hardware requirement.** The dense-MMA group runs on any part with the
   `mma.m16n8k*` family; the SpTC group requires **Ampere or later**, because 2:4
   Sparse Tensor Cores were introduced there.
2. **The design object.** The dense-MMA group is doing *granularity and layout*
   engineering — how small a dense block can you make the sparsity fit into. The
   SpTC group is doing *metadata-contract conformance* — how do you make an
   arbitrary sparsity pattern satisfy "≤2 non-zeros per 4-element group".
3. **What generalises.** SPIDER's group-alignment arithmetic is specific to
   **2-in-4** and must not be carried to a unit with a different structured-
   sparsity granularity; FlashSparse's operand-swap argument is specific to
   **`m = 16`, `n = 8`** and must not be carried to a unit with symmetric extents.

A precision note on the same axis: **SPIDER's `mma.sp` path is FP16, not FP64** —
so unlike ConvStencil it does **not** deliver FP64 stencil accuracy, and its
precision-versus-baseline discussion is `NOT_IN_PAPER` in the rendering read.

### 5.3 A third distinction, recorded rather than resolved

SPIDER's self-claim — "the first to harness SpTCs for acceleration beyond deep
learning domains" `[paper]` — is **the authors' claim and is not verified here**,
given **SparStencil** (SC 2025, the same problem and same mechanism one venue
cycle earlier) and **BerryBees** (PPoPP 2025, bit-tensor-core BFS). The SPTCStencil
text read **does not cite SparStencil** — `NOT_CITED` — but SparStencil has no
reachable full text, so priority and independence are **`UNRESOLVED`**. This is a
verified absence whose *meaning* is undetermined; it is recorded, not adjudicated.

There is also a **title/text discrepancy** on this paper that must not be smoothed:
arXiv `2506.22035` `/abs/` shows the **SPIDER** title, but `arxiv.org/html/
2506.22035v3` serves the **SPTCStencil**-titled text, in which the string "SPIDER"
does not occur (verified). Headline numbers are the same in both abstracts.

---

## 6. Tensions the area found and did not resolve

### 6.1 Is FP64 on the matrix unit dying or working?

Three papers, two positions, **no reconciliation**:

- **Dying.** [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
  measures **B200 ~30 TFLOP/s FP64 matrix against H200 ~67 TFLOP/s** and warns it
  may undermine FP64 MMU adoption.
- **Dying, and therefore emulate.** [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md)
  and [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md)
  assume FP64 must be emulated and build the kernels to do it.
- **Working.** [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md)
  runs **working FP64 DMMA on GB200**, reports higher absolute GDOF/s than GH200,
  and **does not discuss any reduction or removal of FP64 Tensor Core capability
  on Blackwell** — verified by targeted query `[paper]`. Its *lower MDOF/W* on
  GB200 is attributed by its own authors to three other causes: higher idle GPU
  power, a 4% higher clock, and much higher bandwidth and low-precision throughput
  that these kernels do not use. That paper explicitly places itself **opposite**
  the emulation line — citing the Ozaki scheme [35,36] and choosing the *native*
  FP64 matrix unit instead.

**The two measurements are on different products — B200 SXM versus GB200
Superchip — and neither paper reconciles them. Do not merge them.** Whether native
FP64 DMMA or emulated FP64 is the right bet is precisely the area's live question.
`NOT_ESTABLISHED`.

### 6.2 The matrix-instruction issue scope reversed

`mma` (warp, Ampere/Ada) → `wgmma` (warp-**group**, Hopper: 128 threads, 128
cycles at `m64n256k16` on H800 PCIe) → `tcgen05.mma` (warp again, Blackwell B200:
11.4 cycles at `m256n256k16`), while accumulator placement moved monotonically
register file → register file → **TMEM**. Visible only by reading
[`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md)
and [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md)
together `[paper, both]`. **No paper explains why the issue scope reversed** —
`NOT_ESTABLISHED`. Full treatment in
[`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §6.2.

The consequence for this area is concrete: **the entire warp-level `mma.m16n8k*`
sparse branch uses no Hopper-specific feature at all** — no `wgmma`, no TMA, no
DSM — so an H100 result from FlashSparse, Acc-SpMM or SMaT is a warp-level kernel
on a warpgroup-capable part. `[inference]`, and part of why H100 shows the
*smallest* relative gain in Acc-SpMM's three-generation table.

### 6.3 Cubie's own counter-check on a branch it does not belong to

Cubie independently finds that **SpMV is the one Quadrant-IV pattern where
*removing* the MMU-induced redundancy improves performance** — its CC-E variant
runs 1.0–1.2x the TC variant `[paper]`. That is a direct check on the premise of
the PPoPP 2026 *SpMV on Tensor Cores* paper (watchlist, no full text). Recorded so
whoever reads that paper applies it.

---

## 7. Verified negatives in this area

1. **The four-stage progression is three disjoint branches** (§0). The strongest
   statement of it is the reference lists: each branch cites its own ancestors and
   essentially nothing across.
2. **FlashSparse ↔ Acc-SpMM: `NOT_CITED`** (§2.3), same session, same insight.
3. **SPTCStencil/SPIDER ↔ SparStencil: `NOT_CITED`, meaning `UNRESOLVED`** (§5.3).
4. **The dense-MMA group and the 2:4 SpTC group are not one line** (§5.2) —
   verified per paper, including an explicit in-text disclaimer in SMaT.
5. **Cubie is NVIDIA-only.** Its introduction names AMD Matrix Core, Intel
   XMX/AMX, ARM SME and Google TPU, but **the evaluation is NVIDIA-only** (A100,
   H200, B200) `[paper]`. The census's seed note claiming NVIDIA/AMD/Intel vendor
   coverage **is not supported by the paper and is corrected in the analysis.**
   There are **no CDNA2/CDNA3 MFMA numbers anywhere in this corpus**;
   FlashSparse, Acc-SpMM, SMaT, SPIDER and ConvStencil each record
   `NOT_IN_PAPER` for AMD. `NOT_ESTABLISHED`.
6. **The graph community declined the matrix unit** (§1.3) — BerryBees authors,
   one year later, with no matrix unit and BerryBees as a baseline.
7. **SpGEMM never joined this area at all.** Ocean (ICS 2026) **contains none of
   the strings "Tensor Core", "MMA" or "tensor core" in its text or references**
   `[paper, targeted query]`,
   [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md).
   SpMM converged on the matrix unit; SpGEMM stayed an
   atomics-allocation-and-scheduling problem, because **no matrix unit helps with
   an unknown output pattern.**
8. **Mille-feuille is not a matrix-unit paper**, despite sitting in the ledger
   under suspicion. The full text confirms **no Tensor Core appears anywhere**;
   its GPU-specific mechanisms are persistent-kernel grid synchronisation and
   tile-grained precision selection `[paper]`,
   [`GPU-SC24-103`](../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md).
   The ledger's title-level reasoning was right; its access state was wrong.
9. **Two seed titles do not exist.** *Pushing the Limits of Structured Sparse GEMM
   on Hopper GPUs* (SC 2026) and *Complex Tensor Core* (MICRO 2026) both returned
   `NOT_FOUND_AFTER_SEARCH` across two independent passes. Existence unverified —
   and per `governance/ANTI_HALLUCINATION_RULES.md`, **absence in an
   incompletely-enumerated population is weak evidence**, so these are recorded as
   possibly-mistaken seeds, not as refuted.

---

## 8. Where this area is silent

- **The numeric-format branch.** No deep analysis exists for Avant-Garde, MXBLAS
  or MXFFP. The fourth stage of the expected progression **cannot be tested
  against citations at all.** `NOT_ESTABLISHED`.
- **Whether the TC-stencil line's premise holds.** *Do We Need Tensor Cores for
  Stencil Computations?* (SC 2026, same group as SPIDER) interrogates exactly that
  and has no public full text. The single highest-value watchlist item for this
  area. `NOT_ESTABLISHED`.
- **Whether native or emulated FP64 is the right bet** (§6.1). `NOT_ESTABLISHED`.
- **Why the matrix-instruction issue scope reversed** (§6.2). `NOT_ESTABLISHED`.
- **Whether FlashSparse is among Cubie's "general sparse GEMM [44, 79, 98]"
  citations.** Not individually identifiable in the reference numbers read.
  `UNRESOLVED`.
- **LUT Tensor Core (ISCA 2025) and Neo (ISCA 2025, FHE)**: both `UNRESOLVED`
  because GPU-Tensor-Core-versus-standalone-accelerator could not be established.
  LUT Tensor Core's full text is public (arXiv 2408.06003) and is flagged as a
  **cheap resolution**.
- **AMD and Intel matrix units, entirely.** `NOT_ESTABLISHED` (§7.5).
- **Duplication against an external corpus.** `domains/ai_hpc_systems/` is
  `EXTERNAL_IMPORT_PENDING`. Virgo, MXBLAS, LiquidGEMM, BitDecoding,
  FlashAttention-T and the emulation papers are all plausible members. **No
  duplication claim is asserted for any of them.**

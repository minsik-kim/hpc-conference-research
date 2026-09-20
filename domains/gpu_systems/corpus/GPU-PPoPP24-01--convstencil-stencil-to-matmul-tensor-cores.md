# GPU-PPoPP24-01 — ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `F — Tensor/Matrix cores, numeric formats, precision emulation, matrix units for non-GEMM kernels`
secondary_topics: `G — scientific kernels on GPUs (stencil / structured-grid); memory-hierarchy / shared-memory layout`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER — introduction/motivation, background (§2 incl. §2.3 three challenges), design (§3: stencil2row, dual tessellation, kernel fusion, lookup table, dirty-bits padding), performance/utilisation model (Eq. 5-6, Eq. 14), evaluation setup and results, performance breakdown/ablation, related work. Limitations section: NOT_IN_PAPER (no explicit limitations/future-work section located). Read via the author-hosted Microsoft Research PDF.`

## 12.1 Bibliographic facts

- Official title: **ConvStencil: Transform Stencil Computation to Matrix Multiplication on Tensor Cores** [paper]
- Venue: PPoPP 2024 (29th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming); **Best Paper Award** per the official program listing [official-web]
- DOI: `10.1145/3627535.3638476` [official-web]
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Authors and affiliations [paper]: Yuetao Chen (Microsoft Research, Beijing), Kun Li (Microsoft Research, Beijing; corresponding), Yuhao Wang (Microsoft Research; USTC Hefei), Donglin Bai (Microsoft Research), Lei Wang (Microsoft Research; UCAS), Lingxiao Ma (Microsoft Research), Liang Yuan (Chinese Academy of Sciences), Yunquan Zhang (Chinese Academy of Sciences), Ting Cao (Microsoft Research), Mao Yang (Microsoft Research)
- Full text used: `https://www.microsoft.com/en-us/research/wp-content/uploads/2024/04/ppopp24_ConvStencil.pdf` — author/institution-hosted PDF [paper]
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` — the census recorded no artifact URL and none was located here. `NOT_INSPECTED` — no source code was read for this paper.
- Disambiguation: arXiv 2310.16298 was surfaced in an earlier census pass as a possible preprint. Its `/abs/` page describes "a novel stencil algorithm leveraging vector outer products" evaluated "on a simulator" and does **not** mention ConvStencil, Tensor Cores, or a stencil→matrix-multiplication transformation [official-web]. **It is a different paper.** No arXiv preprint of ConvStencil was located.

## 12.2 Core question (one sentence)

Can a stencil sweep — a memory-bound, low-arithmetic-intensity structured-grid update — be rewritten as a sequence of *dense FP64 Tensor Core* matrix multiplications without paying the memory blow-up and the operand-shape waste that a naive im2row/GEMM formulation incurs?

## 12.3 GPU/HPC problem translation

- **Compute.** A stencil is a weighted sum over a neighbourhood. Written as GEMM it becomes a matrix–*vector* product: one "kernel" (the weight set) and one "channel". On A100 the only FP64 Tensor Core MMA shape is `m8n8k4`, so a matrix-vector formulation fills 1 of 8 columns of the right operand — "7/8 columns of the matrix being multiplied on the right are wasted" [paper, §2.3, Challenge 2].
- **Memory.** The classical im2row/im2col lowering materialises one row per output point, replicating every input point once per kernel tap. The paper reports the resulting matrix is "several times or even dozens of times larger than the original input", which is fatal because stencils need FP64 and the staging buffer must live in shared memory [paper, §2.3, Challenge 1].
- **Synchronization.** Within a thread block, the layout transformation itself is the synchronising step: data must be laid into shared memory in a Tensor-Core-fragment-compatible order before any warp issues an MMA.
- **Scheduling.** Layout transformation on the GPU introduces per-thread integer division/modulus for offset computation and conditional branches to guard boundaries, producing warp divergence and shared-memory bank conflicts [paper, §2.3, Challenge 3].
- **Communication.** Single-GPU work; no inter-GPU path is described. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

Three distinct hardware facts, each named by the paper [paper]:

1. **Fixed FP64 MMA shape.** A100's FP64 Tensor Core path exposes exactly one asymmetric shape, `m8n8k4`. A stencil's natural formulation has n=1. The n dimension of the hardware operand is therefore structurally under-filled. This is a *shape* mismatch, not a bandwidth one.
2. **Shared memory capacity, not bandwidth, caps the lowering.** im2row's expansion factor multiplies an FP64 working set that already has to fit a 164 KB-class SM shared-memory budget. The paper's response (§3.1) is to never materialise the expanded matrix at all.
3. **Shared-memory banking and the SIMT integer pipeline.** The address arithmetic that maps a grid point to its im2row row involves division and modulus; issuing these per thread per element consumes the same issue slots the MMA pipeline needs, and the resulting addresses collide in shared-memory banks.

## 12.5 Mathematical / performance model

- **Memory-footprint model** [paper]: stencil2row reduces the expansion relative to im2row by a factor of `2 / ((n_kernel + 1) × n_kernel)`, where `n_kernel` is the kernel (tap-set) extent. Reported reductions: **70.0%–96.4%** across the tested stencil shapes, with 96.43% for Box-2D49P. *Qualifier: memory footprint of the transformed matrix, relative to an im2row lowering of the same stencil, not a measured DRAM-traffic number.*
- **Utilisation claim** [paper]: dual tessellation raises FP64 Tensor Core utilisation from **12.5%** (= 1/8, the n=1-in-n=8 case) to **87.5%** (= 7/8). This is an operand-occupancy fraction of the `m8n8k4` fragment, not an achieved-FLOP/s fraction of peak.
- **Compute-time model** [paper, Eq. 14]:
  `T_compute = [ 2mn / (8 (n_kernel + 1)) ] × ⌈ n_kernel² / 4 ⌉ × CPI_tcu / (f × N_tcu)`
  with `m, n` the tile extents, `f` the clock, `N_tcu` the number of Tensor Core units, `CPI_tcu` the cycles per MMA. The paper uses it to argue ConvStencil issues strictly fewer MMAs than a GEMM-based convolution lowering of the same stencil.
- No error/accuracy model is given; the computation is exact FP64 throughout (the FP64 Tensor Core path is bit-equivalent to FP64 FMA for these operand shapes) — this is the key differentiator against TCStencil. Explicit numerical-error analysis: `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

- **thread**: computes its own pointer offsets by *table lookup* rather than by division/modulus; loads FP64 elements from global memory and writes them into the shared-memory stencil2row staging area, including writing *dirty* (unused) values into padding slots so that no conditional branch is needed [paper, §3.3].
- **warp**: is the unit that issues `m8n8k4` FP64 MMA. The paper's dual tessellation assigns each warp a tile of Stencil2row Matrix A (multiplied by lower-triangular weight matrices → "vitrolite A") and a tile of Stencil2row Matrix B (upper-triangular weights → "vitrolite B"); the two half-results are summed ("tessellation") to yield final outputs [paper, §3.2].
- **block/workgroup**: owns the shared-memory stencil2row region. Crucially the expanded matrix is *never* fully built: the mapping functions (Eq. 5–6) are applied while data streams from global to shared memory, so the block materialises only two *smaller* matrices (A and B), exploiting the observation that "data sequencing in redundant rows has been already stored beyond the redundant rows" [paper, §3.1].
- **SM/CU**: A100 SM, 4 Tensor Cores per SM, 108 SMs [paper].
- **GPU / node / cluster**: single A100. `NOT_IN_PAPER`.

## 12.7 Pseudo code

Reconstructed control flow; the bracketed names are the paper's own component names, the loop variables are `[reconstruction]`.

```
# host side
offsets = build_lookup_table(stencil_shape, tile, padding)   # [paper] "Lookup Table"
W_A, W_B = build_triangular_weight_matrices(stencil_weights)  # [paper] lower/upper triangular

# device kernel, per thread block
for tile in grid_tiles:                                       # [reconstruction]
    # implicit stencil2row: transform while loading
    for e in my_elements(tile):                               # [reconstruction]
        o = offsets[e]                                        # [paper] no div/mod, no branch
        smem_S2R[o] = global_in[addr(e)]                      # dirty bits land in padding
    __syncthreads()

    # Dual Tessellation  [paper] §3.2
    vitrolite_A = mma_m8n8k4_fp64(smem_S2R.A_tile, W_A)       # [paper] Step 1
    vitrolite_B = mma_m8n8k4_fp64(smem_S2R.B_tile, W_B)       # [paper] Step 2
    out_tile    = vitrolite_A + vitrolite_B                   # [paper] Step 3 "tessellation"

    store(global_out, out_tile)
```

For kernel shapes with too few columns to fill a fragment, the paper "temporally fuse[s] some stencil kernels", e.g. converting Box-2D9P into Box-2D49P [paper, §3.2 Kernel Fusion]. Note this is *temporal* fusion of successive stencil applications into a wider effective tap-set, not operator fusion in the deep-learning sense.

## 12.8 Real implementation

`NOT_INSPECTED`. No public repository was located (census: `NOT_FOUND_AFTER_SEARCH`; no artifact URL in the paper text read). No source symbols are asserted here. The only instruction-level fact taken from the paper is the use of the FP64 `8 × 8 × 4` MMA on A100 [paper]; whether it is reached through `wmma::mma_sync`, inline `mma.sync.aligned.m8n8k4.f64`, or a library was not stated in the text read — `UNKNOWN`.

## 12.9 Kernel execution

kernel → thread block (owns the shared-memory stencil2row staging region and the lookup table in constant/global memory) → warp (issues the FP64 `m8n8k4` MMA pair for vitrolite A and vitrolite B) → instruction. The paper's explicit instruction-level intervention is *removal* of instructions from the non-MMA path: integer division/modulus replaced by a precomputed table read, and conditional branches removed by mapping unused data into padding ("dirty bits padding") so every lane executes the same straight-line store [paper, §3.3].

## 12.10 Memory traffic

- **global → shared**: the paper reports a **44.0% reduction in non-coalesced global memory accesses** relative to TCStencil [paper]. *Qualifier: A100, ConvStencil vs TCStencil, profiler-derived.*
- **shared ↔ register**: **63.5% reduction in bank conflicts per request** relative to TCStencil [paper], attributed to the padding scheme changing the element-to-bank mapping.
- **register ↔ Tensor Core**: operands are staged into the `m8n8k4` FP64 fragment from registers; the dual-tessellation layout is what keeps 7/8 of the n dimension occupied.
- **L1/L2/HBM decomposition**: `NOT_IN_PAPER` at the cache-level granularity; the paper reports the two profiler metrics above rather than a full traffic breakdown.
- **Multi-GPU path**: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

The measured performance breakdown [paper] separates four causes, in order of contribution and reported per benchmark (Heat-1D / Box-2D9P / Box-3D27P):

1. **Implicit stencil2row** (avoid materialising the expanded matrix): +22% / +170% / +67%. The dominant cause for 2D box stencils, where im2row expansion is worst.
2. **Introducing the Tensor Core path** on top of that layout: +76% / +68% / +44%. Note this is *second*, not first — the layout work is what makes the Tensor Core path affordable at all.
3. **Padding** (bank-conflict removal): +1% / +14% / +10%.
4. **Dirty-bits padding** (branch removal on top of padding): +4% / +19% / +13%.

So the speedup is not "we put the stencil on Tensor Cores"; it is "we found a lowering whose shared-memory footprint fits and whose fragment occupancy is 7/8, and then removed the SIMT-side integer and branch overhead that the lowering introduced". Cause 1 is a capacity/traffic effect, cause 2 an arithmetic-throughput effect, causes 3–4 are issue-slot and bank-port effects.

Headline results, with qualifiers [paper]: on A100 (CUDA 12.2, AMD EPYC 7V13 host), across Heat-1D, 1D5P, Heat-2D, Box-2D9P, Star-2D13P, Box-2D49P, Heat-3D, Box-3D27P — **2.89× minimum to 42.62× maximum vs cuDNN** (cuDNN convolution API, channel=1, `FWD_IMPLICIT_PRECOMP_GEMM`), **2.77× average vs Brick**, **2.02× average vs DRStencil**. AMOS was given 1,000 search trials. **TCStencil results were divided by 4 by the authors to account for FP16→FP64 conversion**, which is an authors' normalisation, not a measured FP64 TCStencil number — treat any ConvStencil-vs-TCStencil ratio as adjusted, not directly measured.

## 12.12 Hardware generation dependence

**Ampere / A100-specific in its concrete form.** The `12.5% → 87.5%` utilisation argument is arithmetic on the *A100 FP64 shape* `m8n8k4`: the 1/8 baseline is literally "n=1 of n=8". On a generation where the FP64 matrix shape differs, or where FP64 matrix throughput relative to FP64 vector throughput differs, both the baseline fraction and the dual-tessellation payoff change. The paper's own peak reference is A100's 19.5 TFLOP/s FP64 [paper].

Do **not** generalise this to Hopper or Blackwell from this paper: it contains no H100/H200 or B200 measurement, no `wgmma`, no TMA, no TMEM. (Independent evidence within this cluster — the PPoPP'26 MMU characterisation paper — reports that Blackwell B200's FP64 matrix throughput *regresses* relative to Hopper H200, which would change this paper's cost model on Blackwell; that is that paper's finding, not ConvStencil's.)

## 12.13 Limitations

- No explicit limitations or future-work section was located in the PDF read — `NOT_IN_PAPER`. The following are constraints visible in the design, marked as such:
- `[inference]` The lookup table is built on the host for a *fixed* stencil shape, tile size and padding; a new shape requires a new table. The paper frames this as cheap but does not quantify table-build cost or memory.
- `[inference]` Kernel fusion (Box-2D9P → Box-2D49P) changes the numerical operator being applied per kernel launch; the paper does not discuss how this interacts with boundary conditions or with non-constant coefficients.
- `[paper]` The utilisation ceiling is 87.5%, not 100%: one of the eight n-columns remains structurally unused.
- Variable-coefficient / non-constant-weight stencils and unstructured meshes: `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Precursor to** the PPoPP'26 SpTC-stencil work (`GPU-PPoPP26-01`), which cites ConvStencil as the memory-redundancy-reducing baseline and measures ConvStencil at ≈2.12× the theoretical-minimum computation for Box-2D3R [that paper's measurement, not ConvStencil's].
- **Competing/complementary with** LoRAStencil (SC 2024, low-rank adaptation of stencils on Tensor Cores) and FlashFFTStencil (PPoPP 2025, FFT route to stencils on TCUs) — both on this cluster's watchlist, both cited as Tensor-Core stencil alternatives by later papers in this cluster.
- **Successor line:** ConvStencil's own stated only-prior-art is TCStencil ("the only work that applies Tensor Cores to stencil computation" [paper]); ConvStencil's FP64 result is what makes subsequent Tensor-Core stencil work take FP64 seriously.
- **Input to** the PPoPP'26 MMU characterisation study (`GPU-PPoPP26-02`), which cites ConvStencil as reference [11] for the stencil pattern.
- Prior corpus check: the only repository hits for "ConvStencil" are in `domains/gpu_systems/census/PPoPP_2024.md` (STEP A/B census rows). No existing analysis. `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: Every one of the paper's three design components is a response to a named GPU matrix-unit property. Dual tessellation exists *only* because A100's FP64 Tensor Core exposes the single fixed fragment shape `m8n8k4` with n=8 — the triangular weight-matrix pair is constructed precisely to fill 7 of those 8 operand columns, and the "12.5% → 87.5%" claim is arithmetic on that fragment shape. Implicit stencil2row is a *shared-memory-capacity* transform: it exists because the FP64 staging buffer must fit an SM's shared memory. Dirty-bits padding is a shared-memory *bank*-mapping and warp-divergence fix, and the lookup table removes integer-pipeline pressure that competes with MMA issue. A CPU with a matrix extension of a different shape, or a generic accelerator without a 32-lane warp sharing one banked scratchpad, would not need — and could not use — any of these. This is Tensor Core research, not "we ran a GEMM on Tensor Cores".

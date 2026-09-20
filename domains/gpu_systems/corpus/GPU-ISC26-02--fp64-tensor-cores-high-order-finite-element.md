# GPU-ISC26-02 — Accelerating High-Order Finite Element Simulations at Extreme Scale with FP64 Tensor Cores

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` (arXiv preprint; publisher version and venue membership `UNVERIFIED`)
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `F — Tensor/Matrix cores; matrix units for non-GEMM scientific kernels (FP64 DMMA)`
secondary_topics: `G — scientific kernels on GPUs (high-order FEM, sum factorisation); extreme-scale weak/strong scaling; energy efficiency`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML v2 — introduction/motivation, §II application and discretisation (incl. §II-C), §III method (§III-A bottleneck analysis, §III-C/§III-D bank-conflict elimination and index reordering, §III-E shape mismatch, §III-F why direct PTX over CUTLASS/cuBLAS, §III-G loop fusion), §IV evaluation (§IV-A GH200 vs GB200), Tables I–VII, scaling study, related work, limitations/future work.`

## 12.1 Bibliographic facts

- Title: **Accelerating High-Order Finite Element Simulations at Extreme Scale with FP64 Tensor Cores** [paper]
- Authors: Jiqun Tu, Ian Karlin, John Camier, Veselin Dobrev, Tzanio Kolev, Stefan Henneking, Omar Ghattas [paper]
- Affiliations (as rendered): NVIDIA Corporation; Queen's University; Lawrence Livermore National Laboratory; The University of Texas at Austin [paper]. Report number **LLNL-PROC-2014338** appears in the document header [paper].
- Preprint: arXiv:2603.09038 (HTML v2 read) [paper]
- **Venue: `UNVERIFIED`.** Seeded as ISC 2026; the census records `MEMBERSHIP_UNVERIFIED` with no official ISC 2026 program page reachable. **The paper text itself contains no venue declaration** [paper — verified by targeted query]. A WebFetch summariser once volunteered "SC '25", which is *not* supported by the document; that attribution is rejected here. The `/abs/` page returned empty markdown on two attempts, so the Comments field could not be read. Publication type as read: `PREPRINT` / `TECH_REPORT` (LLNL-PROC number).
- Related-application provenance: the paper describes the tsunami digital twin that it states won the **2025 Gordon Bell Prize** [paper]; that prize attaches to the application work cited as [13], not necessarily to this paper. Recorded as the paper's statement, not as this paper's award.
- Artifact: `NOT_SEARCHED` in the census; none stated in the text read beyond "Integration of optimizations into public MFEM repository 'currently under review'" [paper]. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

High-order finite element operator application decomposes by sum factorisation into batched **tiny** dense contractions (order O(10), e.g. 25×5×4) that are shared-memory-bandwidth-bound, not FP64-FLOP-bound — can the FP64 Tensor Core (`m8n8k4` DMMA) be used not for its arithmetic throughput but for its *data-sharing* property, that each operand element is loaded once per warp instead of once per thread?

## 12.3 GPU/HPC problem translation

- **Compute.** The FEM operator is applied as `G^T B^T D B G` [paper, Eq. 1], with `P` (parallel communication), `G` (mesh topology), `B` (basis functions), `D` (physics). Sum factorisation, `B_{abc,ijk} = B^{1d}_{ai} B^{1d}_{bj} B^{1d}_{ck}`, turns the 3D operator into a sequence of 1D contractions, i.e. batched small GEMMs of shapes like **25×5×4** [paper].
- **Memory — the actual bottleneck, and the paper says so explicitly.** §III-A: "it is the shared memory bandwidth, not the FP64 compute FLOP/s, that limits the performance of the kernel." The baseline kernel achieves only **~0.11 FLOP/byte** [paper]. Profiling: **"L1: Data Pipe Lsu Wavefronts" at 97%** while **"SM: Pipe Fp64 Cycles Active" at only 14%** [paper, Table I]. The cause is redundant loading: "the same input matrix elements in A and B are loaded by multiple threads" [paper].
- **Synchronization.** Bank-conflict-free shared-memory layouts and index reorderings are the intra-warp coordination content (§III-C, §III-D).
- **Scheduling.** Loop fusion (§III-G) merges operators into one kernel to halve precomputed-data memory.
- **Communication.** Extreme scale: `P` is the parallel-communication operator; weak scaling 36→2,304 nodes on Alps [paper].

## 12.4 Why the problem exists (hardware root cause)

1. **Warp-level operand sharing is the DMMA's real asset here.** The paper's mechanism sentence: with the `m8n8k4` DMMA, "each matrix element in A and B is loaded only once among the threads in a warp" [paper]. On the vector-FP64 path, each thread independently loads the operands it needs, multiplying shared-memory traffic. So the Tensor Core is being used as a **traffic-reduction device**, which is the opposite of the usual motivation and is the most interesting single fact in this paper.
2. **Shape mismatch is the price.** The target multiplies are `m=25, n=5, k=4`; the instruction is `m8n8k4`. §III-E states the consequence directly: these "do not match m8n8k4 DMMA instruction shape, causing wasting a large percentage of the computation due to mismatch" [paper]. The paper accepts wasted MACs to buy reduced shared-memory traffic — a legitimate trade only because the kernel was bandwidth-bound to begin with.
3. **Shared-memory banking.** Getting each element loaded once per warp requires a precise lane→address map; naive maps collide in banks. §III-C/§III-D handle this with explicit lane-to-address tables (Tables III–V) and a "cyclic order" tensor-index reordering that ensures the summation index is "always the fastest-changing index" [paper].
4. **Library granularity is too coarse.** §III-F justifies hand-written PTX DMMA over CUTLASS/cuBLAS: "our small O(10) matrices require precise control for custom thread-to-fragment mappings and bank conflict elimination"; CUTLASS targets larger GEMMs, and "the majority of the shared memory bandwidth and FLOP/s would be wasted on the padding" [paper].

## 12.5 Mathematical / performance model

- **Operator form** [paper, Eq. 1]: `A = P^T G^T B^T D B G P`, applied matrix-free (partial assembly, "PA").
- **Sum factorisation** [paper]: `B_{abc,ijk} = B^{1d}_{ai} B^{1d}_{bj} B^{1d}_{ck}`, giving three sequential 1D contractions per operator application.
- **Fusion algebra** [paper, §III-G]: the fused operator is written `K_fused = B_test^T D B_trial G_trial G_trial^T B_trial^T D^T B_test` and then reorganised to `K_fused = B_test^T B_trial^T D D^T B_trial B_test`, which the paper states achieves a **twofold reduction in precomputed (PA) data** memory.
- **Fragment index maps** [paper, §III-C]: for the 25×5×4 multiply mapped onto four warps,
  `f_m : m_i → m_p = m_i + w × 8` (w = warp index)
  `f_n : n_i → n_p` with a selective reordering to `[0,2,1,3,4,5,6,7]`
  `f_k : k_i → k_p = k_i`
  The `f_n` permutation is the bank-conflict fix made explicit.
- **Traffic model result** [paper]: shared-memory traffic for the reference case drops from **9,000 bytes to 1,960 bytes**, a **4.6× reduction**. *Qualifier: the paper's reference 25×5×4 case, shared-memory bytes per operator application.*
- No error model; the computation is FP64 throughout and the DMMA path is the exact-FP64 matrix path. `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

- **thread / lane**: holds its DMMA fragment slice per the `m8n8k4` FP64 register layout; its shared-memory addresses come from the explicit lane-to-address maps in Tables III–V [paper].
- **warp**: the ownership unit that matters. A warp collectively performs the contraction such that each A and B element is loaded **once per warp** [paper]. Four warps cooperate on the 25×5×4 target via `f_m : m_p = m_i + w × 8`, i.e. the m dimension is partitioned across warps in strides of 8 (the instruction's m extent) — 4 × 8 = 32 ≥ 25, so ~22% of the m rows are padding.
- **block / workgroup**: owns the shared-memory staging of `B^{1d}`, the element data and the precomputed `D`; the "cyclic order" index reordering ensures the summation index is fastest-changing so that consecutive lanes hit consecutive banks [paper].
- **SM/CU**: GH200's H100 GPU (96 GB HBM3, 34 TFLOP/s FP64 vector, **67 TFLOP/s FP64 tensor-core peak**) and GB200's Blackwell GPU [paper].
- **GPU → node**: 4 GH200 Superchips per Alps node [paper].
- **node → cluster**: Alps at CSCS, 2,688 nodes, HPE Slingshot-11 dragonfly; theoretical peak 574.8 PFLOP/s, achieved 434.9 PFLOP/s, **#8 on the TOP500 November 2025 list** [paper].

## 12.7 Pseudo code

```
# matrix-free high-order FEM operator, one element batch, per thread block
# [paper] Eq.1: A = P^T G^T B^T D B G P ; sum factorization -> 3 x 1D contractions

load_to_shared(B1d, elem_dofs, D_pa)        # [paper] cyclic-order index layout:
                                            # summation index is fastest-changing (III-D)
__syncthreads()

# each of 4 warps takes an 8-row slice of the m=25 dimension
w = warp_id()
for each 1D direction in (x, y, z):                          # [reconstruction]
    m_p = m_i + w * 8                                        # [paper] f_m
    n_p = permute(n_i, [0,2,1,3,4,5,6,7])                    # [paper] f_n  (bank conflicts)
    k_p = k_i                                                # [paper] f_k
    acc = dmma_m8n8k4_fp64(frag_A(m_p,k_p), frag_B(k_p,n_p), acc)   # direct PTX (III-F)

# [paper] III-G: fused operator, reorganized to halve precomputed data
#   K_fused = B_test^T B_trial^T D D^T B_trial B_test
store(out, acc)
```

`permute`, `frag_A`, `frag_B` are `[reconstruction]` names; the index maps `f_m/f_n/f_k`, the `[0,2,1,3,4,5,6,7]` reordering, the `m8n8k4` DMMA and the fused-operator algebra are the paper's [paper].

## 12.8 Real implementation

`NOT_INSPECTED`. No artifact repository was located; the paper states MFEM integration is "currently under review" [paper]. No source symbols asserted.

Facts from the paper about the implementation [paper]:
- The DMMA is issued via **direct CUDA PTX**, deliberately not CUTLASS or cuBLAS, for the reasons in §III-F. The instruction is the FP64 **`m8n8k4` DMMA**.
- Software stack: **MFEM** (high-order Galerkin discretisation with sum factorisation) as the host library, with **HYPRE** [16], **SUNDIALS** [17] and **PETSc** [18] as integrated solvers, and a low-order-refined GPU-accelerated multigrid preconditioner [21]. Discretisation: **4th-order H¹-conforming pressure, 3rd-order L²-conforming velocity components**; time integration **explicit 4th-order Runge–Kutta**.
- libCEED and Laghos are **not** mentioned in the text read, despite the PA/matrix-free methodology's CEED lineage [paper — verified absent].

## 12.9 Kernel execution

kernel → thread block (owns the shared-memory staging with the cyclic index order) → **warp** (four warps per contraction; each issues `m8n8k4` FP64 DMMA over its 8-row m slice) → instruction (hand-written PTX DMMA plus the table-driven address computation). The distinguishing execution fact is that the warp, not the thread, is the operand-loading unit — that is the entire performance argument.

## 12.10 Memory traffic

- **shared memory** is the critical level. Baseline: **97% LSU wavefront utilisation, 14% FP64 pipe active** [paper, Table I]. After DMMA: **84% shared memory, 54% DMMA pipe utilisation, 1.5× cycle reduction** [paper, Table II]. **Note that shared memory is *still* at 84% after the optimisation — it remains the bottleneck** [paper, stated as a limitation].
- **Traffic reduction**: 9,000 → 1,960 bytes for the reference case (**4.6×**) [paper].
- **Precomputed (PA) data**: halved by the fused-operator reorganisation [paper, §III-G].
- **register ↔ shared**: the lane-to-address tables (III–V) and the `f_n` permutation are what make these accesses bank-conflict-free.
- **HBM / L2**: not decomposed. `NOT_IN_PAPER`.
- **Inter-node**: Slingshot-11 dragonfly; scaling efficiency is reported (§12.11) but no message-size or bandwidth analysis. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Two separable causes, and the paper's Table VI isolates them cleanly — this is a genuine 2×2 ablation.

**Table VI, 540M DOF, single GPU** [paper]:

| Kernel version | GB200 GDOF/s | GH200 GDOF/s | GB200 MDOF/W | GH200 MDOF/W |
|---|---|---|---|---|
| PA (baseline) | 23.78 | 18.73 | 26.60 | 28.65 |
| DMMA PA | 33.72 | 25.27 | 31.37 | 36.51 |
| Fused PA | 29.28 | 24.04 | 36.41 | 40.14 |
| **DMMA Fused PA** | **46.60** | **36.15** | **45.70** | **52.42** |

- **Cause 1 — DMMA alone**: the warp-level operand sharing cuts shared-memory traffic 4.6×, giving **~35–59% kernel speedup** (GB200 23.78→33.72 = +42%; GH200 18.73→25.27 = +35%) [paper].
- **Cause 2 — fusion alone**: halves precomputed data, giving GB200 +23%, GH200 +28% [derived from Table VI].
- **Together**: **≈2× overall** (GB200 23.78→46.60 = 1.96×; GH200 18.73→36.15 = 1.93×) — i.e. the two causes are close to multiplicative, because they relieve the *same* bottleneck from two directions (fewer bytes per contraction; fewer contractions' worth of stored coefficients).
- **Energy per DOF**: GH200 28.65→52.42 MDOF/W = **+83%**; GB200 26.60→45.70 = **+72%** [derived from Table VI]. **Note**: an earlier summarisation of this paper reported "83% (GB200) and 27% (GH200)"; that is inconsistent with Table VI and is rejected. Use the table-derived figures with their GPU qualifier.

**Extreme-scale results, with qualifiers** [paper, Table VII]: on **Alps at CSCS** (2,688 nodes × 4 GH200): weak scaling **36 → 2,304 nodes (144 → 9,216 GH200)**, a 64× node increase, with near-linear efficiency; largest problem **~9.28 trillion DOF**, averaging **~1.01 billion DOF per GPU**; strong scaling from a ~145-billion-DOF, 36-node baseline to full system at **86–91% efficiency**.

## 12.12 Hardware generation dependence

- **GH200 (Grace Hopper)**: 72 Arm cores + H100, 96 GB HBM3, **34 TFLOP/s FP64 vector, 67 TFLOP/s FP64 tensor-core peak** [paper]. This 2× vector→tensor FP64 ratio is what makes the DMMA path attractive on Hopper.
- **GB200 (Grace Blackwell)**: described as having higher clock frequency and memory bandwidth [paper]. Higher absolute GDOF/s but **lower MDOF/W than GH200 for the same kernels**, which the paper attributes to three causes it states explicitly: "(1) GB200 has higher idle GPU power, (2) GB200 runs at a 4% higher clock frequency … and (3) GB200 has much higher memory bandwidth and tensor core performance for lower precisions (FP16, BF16, FP8, FP6 and FP4), while the kernels of interest here do not make high utilizations of any of these compute resources" [paper, §IV-A].
- **The paper does NOT discuss any reduction or removal of FP64 Tensor Core capability on Blackwell** [paper — verified by targeted query]. Its GB200 results are presented as working DMMA. **Do not merge this with the PPoPP'26 characterisation paper's separate finding that B200 FP64 matrix throughput is ~30 TFLOP/s against H200's ~67** — that is a different paper's measurement on a different part (B200 SXM vs GB200 Superchip) and the two are not reconciled by either paper. Recorded as an **open tension** in this cluster, not as a settled fact.
- **Ampere (A100)** appears only in the related work (Cui et al. [12] on A100; the CEED-MS40 report [37] on A100/MI250X) [paper]. No AMD measurement in this paper.

## 12.13 Limitations

Stated by the paper [paper]:
- **Shape mismatch**: `m=25, n=5, k=4` against `m8n8k4` "wast[es] a large percentage of the computation" (§III-E).
- **Shared memory is still the bottleneck after optimisation**: 84% utilisation vs 54% DMMA pipe (Table II).
- **Application-specific discretisation**: "larger performance gains than the ones presented here could likely be achieved if the operators were discretized … to best fit the tensor-core architecture" (§II-C) — i.e. the numerics were not co-designed with the instruction shape.
- **Future work**: **cuBLASDx** as a potential future alternative to hand-written PTX; MFEM upstreaming under review.
- `[inference]` The whole approach depends on FP64 tensor-core peak exceeding FP64 vector peak on the target part. On a part where that ratio is 1:1 or inverted, the shape-mismatch waste would no longer be affordable. The paper does not analyse this sensitivity.
- `[inference]` The lane-to-address tables and `[0,2,1,3,4,5,6,7]` permutation are hand-derived for one operator/order combination; generality across orders and element types is not demonstrated in the text read.

## 12.14 Relation to prior corpus

- **Cited prior work** [paper]: **Ozaki scheme [35,36]** for emulating FP64 with integer cores, and vendor libraries (cuBLAS, HPL) — so this paper explicitly places itself opposite the emulation line: rather than emulate FP64 on low-precision units, it uses the *native* FP64 matrix unit. Also cited: recent small-matrix FP64 direct-programming studies on stencils and FEM benchmarks [11,34]; **Cui et al. [12]** accelerating "tensor-product operations" on A100; the **CEED-MS40 report [37]** on high-order FEM acceleration on A100/MI250X.
- **Self-claim** [paper]: "To the best of our knowledge, this is the first example of using directly programmed FP64 tensor cores in a complex, PDE-based HPC application", with the emphasis on production-MFEM integration and a full tsunami digital twin rather than a benchmark. The authors' claim; not verified here.
- **Direct methodological sibling** to `GPU-PPoPP24-01` (ConvStencil): both use the A100/H100-class **FP64 `m8n8k4`** matrix instruction for a non-GEMM structured-grid/PDE kernel, both hit the *same* obstacle (the target operation's natural shape does not fill the fragment), and they resolve it oppositely — ConvStencil reshapes the *algorithm* (dual tessellation) to fill 7/8 of the n extent, while this paper accepts the padding waste and buys warp-level operand sharing instead. That contrast is the single clearest design-space axis in this cluster.
- **Complementary to** `GPU-PPoPP26-02` (Cubie), which measures "Stencil 1.7–2.3×" and places structured-grid patterns in Quadrant I; this paper is the extreme-scale application instance of the same pattern class.
- **Opposed in strategy to** `GPU-SC26-01` and `GPU-SC26-02`, which assume FP64 must be emulated. Whether native FP64 DMMA or emulated FP64 is the right bet is precisely the cluster's live question, and these three papers are on opposite sides of it.
- Prior corpus check: in-repo hits for `2603.09038` are confined to `domains/gpu_systems/census/ISC_2026.md`. `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution is *specifically* the exploitation of warp-cooperative operand semantics in NVIDIA's FP64 `m8n8k4` DMMA: the performance comes not from matrix throughput but from the fact that "each matrix element in A and B is loaded only once among the threads in a warp", which cuts shared-memory traffic 9,000→1,960 bytes for the reference contraction. Everything around it is matrix-unit-specific engineering — explicit thread-to-fragment index maps `f_m : m_p = m_i + w×8`, `f_n` permuted to `[0,2,1,3,4,5,6,7]`, `f_k` identity; per-lane shared-memory address tables to eliminate bank conflicts; a cyclic tensor-index reordering forcing the summation index fastest-changing; and hand-written PTX DMMA chosen over CUTLASS/cuBLAS because those libraries' tile granularity would waste the shared-memory bandwidth on padding. A CPU has neither a banked per-SM scratchpad nor a 32-lane warp that shares one matrix fragment, so the mechanism has no counterpart. Note the paper *pays* in wasted MACs (25×5×4 into `m8n8k4`) to buy this, which is the inverse of the usual Tensor Core motivation and reinforces that the contribution is about operand delivery, not arithmetic.

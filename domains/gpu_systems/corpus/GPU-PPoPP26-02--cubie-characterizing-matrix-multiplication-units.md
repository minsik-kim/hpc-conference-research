# GPU-PPoPP26-02 — Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `F — Tensor/Matrix cores; matrix units for non-GEMM kernels (characterization)`
secondary_topics: `G — scientific kernels on GPUs; benchmarking methodology; energy; FP64 numerics`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the author-hosted PDF — introduction, §3 The Cubie Benchmark Suite, §4 Categorization of MMU Utilization Patterns, §5 Experimental Design incl. §5.2 Algorithmic Implementation Variants, §6 Performance of MMUs, §7 Power and Energy Efficiency, §8 Floating-point Accuracy, §9 Performance Model, limitations/threats, related work.`

## 12.1 Bibliographic facts

- Title: **Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing** [paper]
- Venue: **PPoPP '26** (31st ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming), January 2026 [paper]
- DOI: `10.1145/3774934.3786456` [official-web / census; corroborated via the ACM PDF URL form]
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Authors and affiliations [paper]: Yuechen Lu (SSSLab, Dept. of Computer Science and Technology, China University of Petroleum-Beijing), Hongwei Zeng (same), Marc Casas (Barcelona Supercomputing Center; Universitat Politècnica de Catalunya), Weifeng Liu (China University of Petroleum-Beijing)
- Full text used: `https://www.ssslab.cn/assets/papers/2026-lu-Cubie.pdf` — author-hosted PDF [paper]
- Artifact: `https://zenodo.org/records/17725527` [census/official-web]. **`NOT_INSPECTED`** — the Zenodo record was not downloaded or read in this pass; no code symbols are asserted.
- Named deliverable: the benchmark suite is called **Cubie** [paper].

## 12.2 Core question (one sentence)

Prior work has shown, kernel by kernel, that a matrix multiplication unit *can* accelerate a non-GEMM scientific kernel — but is there a systematic account of *which* parallel patterns benefit, by how much, at what energy cost, and at what loss of numerical accuracy, across three GPU generations?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper asks how much of an observed MMU speedup is genuinely the matrix unit and how much is the *algorithmic restructuring* done to reach it. Its instrument for separating these is the three-variant methodology in §12.5/§12.7.
- **Memory.** The categorisation in §4 is fundamentally about how much of the MMA's fixed input and output tiles a pattern can actually fill — an operand-occupancy question, which then determines whether the kernel is bandwidth- or compute-limited.
- **Synchronization / scheduling.** Not the object of study; the paper measures kernels, not schedulers. `NOT_IN_PAPER`.
- **Communication.** Single-GPU throughout; "all measurements … are conducted on a single physical GPU for each GPU type" [paper].

## 12.4 Why the problem exists (hardware root cause)

- An MMA instruction has **fixed input and output tile extents**. A pattern whose natural data shape does not fill those tiles either pads (wasting MACs) or must be algebraically restructured to fill them (changing the operation count and the rounding behaviour). The paper's §4 quadrants are precisely a taxonomy of *which tile* goes unfilled.
- Some patterns can fill the operand tiles with **constants** (triangular-ones or all-ones matrices for scan and reduction) that "do not require loading from global memory" [paper] — so for those, the MMU's benefit is partly that the operand never crosses the memory hierarchy at all.
- Root cause of the accuracy finding: a matrix unit and a vector unit at the same precision give the *same* result for the *same* operation sequence, but the restructuring needed to use the matrix unit changes the operation sequence — hence "algorithmic transformations for MMU utilization can induce significant numerical deviations" [paper, §8].
- Root cause of the paper's forward-looking warning: FP64 matrix throughput is a *design choice per generation*, and it has been reduced (§12.12).

## 12.5 Mathematical / performance model

**§9 performance model — a cache-aware roofline** [paper]:
- Ceilings on H200: **L1 cache 34 TB/s**, **DRAM 4 TB/s**, **FP64 peak 66.9 TFLOP/s tensor / 33.5 TFLOP/s CUDA core**. *Qualifier: H200 in a GH200 platform.*
- Quadrant I (GEMM, FFT, Stencil, PiC) spans high arithmetic intensity; GEMM is compute-bound but below peak.
- Quadrants II–III (Scan, Reduction) sit at **~0.1 FLOP/byte** and are cache-friendly; notably their **TC versions exceed the DRAM bandwidth ceiling**, which is the roofline's way of exposing that the constant operands are served from cache/registers, not DRAM.
- Quadrant IV sits at **0.1–3 FLOP/byte**, memory-bound; the TC variants approach the bandwidth limit more closely than the baselines.
- The paper's stated model-level insight: "adapting data layouts and algorithms for MMUs fundamentally alters memory access patterns" [paper] — i.e. the roofline *position* of a kernel is not invariant under MMU porting, which is the reason a naive before/after speedup is uninterpretable.

**Measurement protocol** [paper]: most benchmarks run **100 warm-up iterations then 1000 timed executions**, arithmetic mean reported; power via **NVML `nvmlDeviceGetPowerUsage()`**; accuracy against a **naive serial CPU implementation** as ground truth.

## 12.6 Data layout and ownership

The paper is a characterisation study; layout is described per-kernel rather than designed. Ownership facts as read:

- **warp**: the unit issuing the MMA. The instructions used are the **FP64 `wmma` `m8n8k4`** for most kernels and **`mma_m8n8k128`** for the bit-operation BFS kernel [paper]. *Note the second is a bit/integer MMA shape — the BFS kernel is in the bit-tensor-core family, not the FP64 family.*
- **Constant-operand ownership (Quadrants II–III)**: scan uses upper-triangular-ones and lower-triangular-ones matrices; reduction uses matrices with a single row or column of ones. These constants "do not require loading from global memory" [paper] — so the operand tile is owned by registers/immediates rather than by the memory hierarchy.
- **Output-tile ownership**: the paper's key layout observation is asymmetry. Quadrant III (reduction) "utilizes only a small portion of the output matrix, specifically a single row or element"; Quadrant IV "takes full input A and B but only partial output C" [paper]. So for a large class of scientific patterns, the waste is in the *accumulator*, not the operands.
- **block / SM / GPU**: not characterised at the ownership level beyond the per-kernel implementations. `NOT_IN_PAPER`.

## 12.7 Pseudo code

The paper's methodological instrument, which is the reusable part:

```
# [paper] §5.2 Algorithmic Implementation Variants — three (to four) variants per kernel
TC    : performs the FP computation mainly with tensor-core MMA 64-bit instructions
CC    : replaces the tensor-core MMA with CUDA-core computation, KEEPING identical
        data structures and algorithmic settings
CC-E  : additionally ELIMINATES the redundant/useless operations that the
        tensor-core MMA formulation introduced
```

The discriminating logic, which is why this design is worth recording:
- `TC / CC` isolates **the matrix unit itself** (same algorithm, same layout, different execution unit).
- `TC / CC-E` isolates **the algorithmic restructuring** (the MMU formulation's redundant work removed).
- A speedup that survives `TC vs CC` is a hardware win; one that vanishes under `TC vs CC-E` was an algorithm win that did not need the matrix unit. This is exactly the counterfactual discipline this cluster's verdicts require, applied as an experimental method.

## 12.8 Real implementation

`NOT_INSPECTED`. The artifact is `https://zenodo.org/records/17725527` [official-web] but was not downloaded in this pass; no code symbols, file names or kernel identifiers from it are asserted.

Instruction-level facts from the paper only [paper]: FP64 `wmma` **`m8n8k4`** for most Cubie kernels; **`mma_m8n8k128`** for BFS bit operations. Cubie's per-kernel baselines are named third-party implementations — **DASP** for SpMV, **AmgT-SpGEMM** for SpGEMM, **BerryBees** for BFS, **LoRAStencil** for stencil, **tcFFT** for FFT, **TCU-Scan/TCU-Reduction** for scan and reduction [paper]. `[inference]` this means Cubie is partly an *integration* of the existing Tensor-Core-scientific-kernel literature into one suite, which is itself the cleanest available evidence about that literature's shape.

## 12.9 Kernel execution

kernel → thread block → warp (issues `wmma m8n8k4` FP64, or `mma m8n8k128` for bit-BFS) → instruction. No new execution mechanism is proposed. The study's execution-level contribution is the **CC / CC-E ablation of the instruction choice itself**: holding block/warp decomposition and data structures fixed while swapping the MMA for CUDA-core arithmetic.

## 12.10 Memory traffic

Traffic is characterised through the cache-aware roofline rather than counted [paper]:
- L1 34 TB/s and DRAM 4 TB/s ceilings on H200 bound the analysis.
- Scan and Reduction TC variants **exceed the DRAM ceiling** — the operands are constants served on-chip.
- Quadrant IV kernels (BFS, GEMV, SpMV, SpGEMM) are memory-bound at 0.1–3 FLOP/byte; TC variants sit *closer* to the bandwidth roof than their baselines, which is the mechanism behind their speedups (better traffic efficiency, not more FLOP/s).
- No per-level byte counts. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

This paper's whole point is the decomposition, so the findings are recorded as the paper's own quadrant structure.

**§4 categorisation** (2D: input-tile utilisation × output-tile utilisation) [paper]:
- **Quadrant I — full input, full output**: GEMM, Particle-in-Cell (PiC), FFT, Stencil.
- **Quadrant II — partial input, full output**: Scan (constant triangular/all-ones operands).
- **Quadrant III — partial input, partial output**: Reduction (constant operands; a single output row or element used).
- **Quadrant IV — full input, partial output**: BFS, GEMV, SpMV, SpGEMM — all memory-bound.

**§6 performance, TC vs baseline** (A100 / H200 / B200 ranges) [paper]:
- Quadrant I: GEMM **3.1–3.2×**, Stencil **1.7–2.3×**, PiC **1.2–1.5×**, **FFT 0.5–0.6× (it *underperforms*)**.
- Quadrant II Scan **1.3–1.8×**; Quadrant III Reduction **1.3–1.6×**.
- Quadrant IV: BFS **2.6–3.0×**, SpGEMM **2.5–3.2×**, SpMV **1.7–2.8×**, GEMV **1.0–1.2×**.

**§6 CC vs TC — isolating the matrix unit** [paper]: Quadrant I retains ~40–60% of performance on CUDA cores; Quadrants II–III retain **<40%** (they depend most on the MMU, because the constant-operand trick has no CUDA-core analogue); Quadrant IV retains **60–90%** (memory-bound, so the execution unit matters least).

**§6 CC-E vs TC — removing the MMU-induced redundancy** [paper]: Scan/Reduction **0.34–0.79×** — i.e. *the redundant computation the MMU formulation introduces is itself beneficial*, because the matrix unit performs it for free; SpMV **1.0–1.2×** — removing redundancy *improves* on the TC version; BFS/SpGEMM comparable.

**These two ablations together are the paper's most important result**: for Quadrant II–III the matrix unit is doing genuine work that CUDA cores cannot replicate, while for SpMV the MMU formulation is arguably a net loss once its redundancy is removed. A bare speedup number would have hidden both.

**§7 power and energy (H200 focus)** [paper]: TC often draws **>400 W** instantaneous — *higher* power than the baseline — but for much shorter duration. Energy-delay-product reductions, geometric mean: **Quadrant I ~64%**, **Quadrants II–III ~36%**, **Quadrant IV ~80%**. Worked example (Stencil, H200): baseline **15 s @ 470 W** vs TC **5.5 s @ 450 W**, giving **65% energy reduction and 88% EDP reduction**.

**§8 accuracy** [paper, Table 6]:
- **TC and CC are numerically identical**: "tensor core and CUDA core provide equivalent numerical accuracy" — so the matrix unit itself is not the source of error at FP64.
- Quadrant I shows the largest TC-vs-baseline error (FFT **7.5E-17 vs 4.8E-18**, i.e. ~15× worse).
- Quadrant IV: **CC-E can be 1–2 orders of magnitude *worse* than TC** (SpMV **2.0E-08 vs 7.1E-10**) — the MMU formulation's "redundant" work was acting as a more stable summation order.
- SpGEMM and PiC: negligible differences.

## 12.12 Hardware generation dependence

The paper is explicitly a three-generation study and its generational finding is the single most consequential item in this cluster.

- **Hardware covered: NVIDIA A100 (Ampere) PCIe, H200 (Hopper, in a GH200 platform), B200 (Blackwell)** [paper].
- **AMD Matrix Core and Intel XMX/AMX are NOT evaluated.** The introduction mentions "AMD's Matrix Core, Intel's XMX and AMX, as well as ARM's SME and Google TPU", but the evaluation is NVIDIA-only [paper]. The authors justify the scope: NVIDIA "provides a well-defined and widely used MMU programming interface, and tensor cores have served as the basis for most prior work on MMU-accelerated scientific computing" [paper]. **The census's seed note claiming NVIDIA/AMD/Intel vendor coverage is therefore not supported by the paper; corrected here.**
- **The FP64 matrix-throughput regression** [paper, Figure 12]: Blackwell **B200 ~30 TFLOP/s FP64** against Hopper **H200 ~67 TFLOP/s FP64**. The authors warn this "may directly undermine FP64 MMU adoption" and call for architectural roadmaps to "preserve and materially strengthen FP64 MMU capability". *Qualifier: the paper's own figure, FP64 matrix-unit throughput, B200 vs H200.*
  This is the corroborating evidence for why the precision-emulation papers in this cluster exist at all: if native FP64 matrix throughput is being withdrawn, emulating FP64 on INT8/FP8 matrix engines stops being a curiosity and becomes the only way to keep matrix-unit FP64 performance.
- No CDNA2/CDNA3 (MI250X/MI300X) numbers. No GH200 NVLink-C2C mechanism study (the H200 is simply hosted in a GH200 platform). `NOT_IN_PAPER`.

## 12.13 Limitations

Stated by the paper [paper]:
1. **Single-device evaluation** — one physical GPU per type, to avoid manufacturing variability; the authors note this limits generalisability.
2. **Compiler-assistance gap** — "A deeper question is whether MMU accelerability can be inferred … before such transformations. Addressing this question requires linking algorithmic structure to MMU execution semantics, likely with compiler assistance."
3. **GEMM is not fully optimised** — "advanced optimizations such as those in cuBLAS" are excluded for simplicity, so the 3.1–3.2× GEMM figure is not a cuBLAS-class number.
4. **The categorisation is post-hoc** — it is "derived from MMU adapted kernels" and characterises "MMU behavior in the transformed code space"; pre-transformation inference of MMU suitability is open.
5. The FP64 regression is flagged as a threat to the whole research direction rather than as a property of the measurements.
- Future directions the paper implies: linking algorithmic properties to MMU suitability before transformation; explaining why FFT underperforms despite high arithmetic intensity; sparse-specialised tensor cores (it cites Uni-STC and TSTC designs) [paper].
- `[inference]` Because Cubie's kernels are largely third-party implementations of varying maturity (DASP, AmgT, BerryBees, LoRAStencil, tcFFT, TCU-Scan), cross-pattern comparisons partly reflect implementation effort, not only pattern suitability. The paper's own GEMM caveat (#3) is an admission of exactly this for one kernel.

## 12.14 Relation to prior corpus

This paper is the **integrative node** of the whole cluster, and its citation graph is the best available evidence for the cluster's lineage. Cited tensor-core scientific-kernel work [paper]:
- **Stencil**: ConvStencil [11] (= `GPU-PPoPP24-01`), LoRAStencil [101] (used as Cubie's stencil baseline), FlashFFTStencil [28].
- **FFT / signal processing**: tcFFT [41] (Cubie baseline), FFT & NTT on tensor cores [23, 75].
- **Sparse**: DASP [51] (Cubie's SpMV), **AmgT-SpGEMM [53]** (Cubie's SpGEMM — the SC 2024 algebraic-multigrid paper on this cluster's watchlist), BerryBees [59] (Cubie's BFS — PPoPP 2025 bit-tensor-core BFS, watchlist), general sparse GEMM [44, 79, 98].
- **Scan / reduction**: TCU-Scan and TCU-Reduction [17].
- **Dense factorisation**: QR via Householder [39], tridiagonalisation [87] on tensor cores.
- **Prior characterisation**: Domke et al. [21] "Matrix engines for high performance computing: Paragon or grasping?"; Markidis et al. [54] on tensor-core programmability/performance/precision; Schieffer et al. [77, 78] on **AMD matrix cores** characterisation.
- **Emulation lineage**: the paper's forward-looking FP64 discussion connects to the Ozaki-scheme line (`GPU-SC26-01`, `GPU-SC26-02`).
- **Positioning** [paper]: "existing studies examine MMUs mainly in machine learning or isolated GEMM settings" and "current GPU benchmark suites (Rodinia, SHOC) remain designed for vector-based execution without support for evaluating MMU-based operations". Cubie covers **seven Berkeley Dwarfs** (vs five in prior suites), evaluates **five features** (performance, power, energy, precision, memory) vs three–four, and uses **PCA on architectural metrics** to argue broader behavioural diversity than Rodinia/SHOC.
- Prior corpus check: in-repo hits for `3786456` are confined to `domains/gpu_systems/census/PPoPP_2026.md`. `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The object of study is the GPU matrix unit's instruction contract itself — the fixed FP64 `wmma m8n8k4` and bit `mma m8n8k128` tile extents, and which of their input and output tiles a given parallel pattern can fill (the §4 quadrants are literally a taxonomy of operand- and accumulator-tile occupancy). The CC and CC-E variants are defined as *replacing the tensor-core MMA with CUDA-core computation on the same GPU*, so the experiment cannot be run on a CPU at all. The headline generational finding — that Blackwell B200 delivers ~30 TFLOP/s FP64 on the matrix unit against H200's ~67 — is a statement about GPU matrix-unit datapath provisioning with no CPU analogue. This is a characterisation study, not a mechanism paper, but it is a characterisation *of* the matrix unit, which is squarely in scope.

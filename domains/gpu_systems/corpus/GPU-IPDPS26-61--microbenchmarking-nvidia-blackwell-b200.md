# GPU-IPDPS26-61 — Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (cross-listed: this paper is a **watchlist row** in the sibling cluster's `_LEDGER_profiling_reliability.md`, which records `CORE_GPU` from title+census evidence and explicitly no deep analysis; this file is the first analysis of it)
primary_topic: `A — GPU core / instruction issue and execution: matrix-instruction issue scope, single-instruction latency, operand staging` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `F — Tensor/Matrix cores and numeric formats (FP4/FP6/FP8) — overlaps the tensor-cores cluster; N — microbenchmark methodology and the simulator gap for Blackwell`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` + `ARTIFACT` — abstract, motivation, methodology (SKUs, software stack, pointer-chase and dependency-chain microbenchmarks, Nsight/NVML/CUTLASS-disassembly tooling), TMEM characterisation, `tcgen05` instruction semantics and SI-LAT tables, precision throughput table, CTA-pair scheduling, decompression-engine tables, STREAM/DGEMM/LLM case studies, B200-vs-H200 comparison, limitations, related work. Artifact `github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark` cloned at commit `91411b53aebaa4733477f22bde576b5182c669fc`; read `README.md`, top-level tree, `results/` layout, `tests/tensor-core/standalone/` file list.

## 12.1 Bibliographic facts

- **Title** [paper]: *Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis*. The sibling ledger records a subtitle discrepancy ("Architecture Analysis" on the author slide deck vs "Architectural" on arXiv/Zenodo); arXiv v3 and the artifact agree on "Architectural".
- **Authors** [paper]: Aaron Jarmusch, Sunita Chandrasekaran — Department of Computer and Information Sciences, University of Delaware, Newark, US. The artifact `README.md` lists Jarmusch as author and Chandrasekaran as advisor [README].
- **Venue**: **IPDPS 2026**, stated in the artifact's `README.md` ("Conference: IEEE IPDPS 2026") [README] and in the census row. The arXiv record itself carries **no venue comment field** (verified) — venue evidence here is `[README]` + census, not `[paper]`.
- **arXiv** [official-web]: `2512.02189`; v1 2025-12-01, v3 2026-03-02; cs.AR; **CC BY 4.0**.
- **Artifact** [artifact]: `github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark` @ `91411b53aebaa4733477f22bde576b5182c669fc`. The sibling ledger also records a Zenodo deposit `zenodo.org/records/18716313`, artifact DOI `10.5281/zenodo.18716313` (not fetched here).
- **Publication type**: `PREPRINT` for the arXiv text; `ARCHIVAL_MAIN_PAPER` for the IPDPS 2026 version, whose camera-ready text was not read. Claims below are from the arXiv v3 text.
- **Internal inconsistency worth recording**: the paper's limitations say the code could not be shared "due to double-blind", and the README's quick-start clones a *different* URL (`github.com/UD-CRPL/microbench-blackwell.git`) from the repository that actually hosts it. The artifact clearly post-dates the submission. [paper] / [README]

## 12.2 Core question (one sentence)

What are the instruction-level latency, issue-scope and operand-staging characteristics of Blackwell's 5th-generation matrix pipeline, its new Tensor Memory, and its decompression engine — measured on a B200, against an H200 baseline? [paper]

## 12.3 GPU/HPC problem translation

**Compute** and **scheduling** at the instruction-issue level, plus a **memory** contribution (a new on-SM storage tier).

The paper's framing is a timing gap: "systematic methodologies for quantifying these improvements lag behind hardware development cycles", leaving "instruction latency, pipeline depth, cache interaction, and saturation" unknown for Blackwell [paper]. It is a characterisation paper, not a design paper.

**Cluster placement caveat**: a large fraction of the content is matrix-unit and numeric-format material that belongs to the tensor-cores cluster (taxonomy F). The reason it is analysed *here* is the **issue-scope finding** — `tcgen05.mma` is a warp-scope instruction where Hopper's `wgmma` was warpgroup-scope — and the **operand-staging finding** — TMEM displaces the register file as the accumulator home. Both are core-execution changes.

## 12.4 Why the problem exists (hardware root cause)

[paper] Blackwell changes the contract between a warp and the matrix pipeline in two ways:

1. **Issue scope shrinks.** Hopper's `wgmma` is issued by a **warp group of 128 threads** and is warp-group-synchronous. Blackwell's `tcgen05.mma` is issued at **warp scope (32 threads)**, and "each thread independently issues MMA operations", eliminating warp-level synchronisation overhead.
2. **Accumulators move out of the register file.** A new per-SM structure, **Tensor Memory (TMEM)**, holds the accumulators and intermediates, addressed by a lane–column scheme rather than as registers. New instructions `tcgen05.alloc`, `tcgen05.cp`, `tcgen05.ld`, `tcgen05.st` replace the `cp.async.bulk` / `ldmatrix` / `ld.shared` staging path.

The consequence the paper draws is a datapath one: measured latency is nearly constant across tile shapes, which it reads as "a spatial array design rather than Hopper-style temporal pipelining."

## 12.5 Mathematical / performance model

No analytic model. The quantitative contribution is a measured latency/throughput characterisation. **Every number below is measured on real silicon** — B200 for Blackwell, H200 for Hopper — via dependency-chain microbenchmarks with `clock64` cycle counting, 100 iterations after a 10-iteration warm-up [paper].

Single-instruction latency (SI-LAT):

| Instruction | Tile shape | Issue scope | SI-LAT (cycles) | SKU |
|---|---|---|---|---|
| `wgmma` | m64n64k16 | warp group (128 threads) | 32.0 | H200 |
| `wgmma` | m64n256k16 | warp group | 128.0 | H200 |
| `tcgen05.mma` | m64n64k16 | warp (32 threads) | 11.0 | B200 |
| `tcgen05.mma` | m256n256k16 | warp | 11.4 | B200 |

**The structural result is the second column against the fourth**: on Hopper, SI-LAT scales with the n extent (32.0 → 128.0 as n goes 64 → 256); on Blackwell it does not (11.0 → 11.4 as n goes 64 → 256, at 4× the m extent as well). The paper reports 2.9–11.2× lower single-instruction latency.

Latency vs throughput across precisions (m64n8k16, B200) [paper]:

| Input / accumulator | SI-LAT (cycles) | Throughput |
|---|---|---|
| FP16 / FP16 | 11.2 | 964.8 TFLOP/s |
| FP16 / FP32 | 11.5 | 482.4 TFLOP/s |
| FP8 / FP32 | 12.1 | 1912.8 TFLOP/s |
| FP6 / FP16 | 12.3 | 2567.2 TFLOP/s |
| FP4 / FP16 | 12.6 | 3850.1 TFLOP/s |
| INT8 / INT32 | 11.9 | 3928.5 TOP/s |

The derived claim: throughput varies by **8.2×** while latency varies by only **1.12×**, therefore "throughput scaling is achieved through increased parallelism (wider datapaths) rather than deeper pipelining" [paper]. A second derived claim: FP16 inputs with an FP32 accumulator halve throughput (964.8 → 482.4 TFLOP/s) at essentially unchanged latency, so **the accumulator datapath, not the multiply array, is the limiter**.

## 12.6 Data layout and ownership

- **thread → warp**: `tcgen05.mma` is issued at warp scope. This is the reversal of Hopper, where the unit of matrix issue was the 128-thread warp group [paper].
- **warp → TMEM**: TMEM is **256 KB per SM**, structured as **512 columns × 128 lanes of 32-bit cells**, addressed lane-column [paper]. Optimal tile is **64×64 elements** (4 KB in FP8), which the paper says fills the 1024-bit interface; tiles below 32×32 underutilise it and tiles above 128×128 can trigger multi-phase transfers. Read bandwidth **16 TB/s per SM**.
- **CTA pair → TPC**: a new scheduling construct — "two Cooperative Thread Arrays (CTAs) with adjacent ranks share operands, reducing redundant data movement", with each CTA pair mapped to a **TPC** with a dedicated intra-TPC communication network [paper]. This is a *block-level* operand-sharing mechanism, new in this generation.
- **register file**: the paper's treatment is inferential, not measured — TMEM reduces register pressure by holding accumulators instead of the RF, with shared memory still an operand source for `tcgen05.mma`. **No register-file capacity, banking or port measurement is reported.** `NOT_IN_PAPER`.

## 12.7 Pseudo code

Reconstructed measurement kernels; PTX mnemonics are the paper's/NVIDIA's, harness names are `[reconstruction]`.

```
# --- SI-LAT via accumulator-carried dependency chain --------------------- [paper]
warm_up(10 iterations)
t0 = clock64()
for i in 1..N:                       # each op depends on the previous accumulator
    tcgen05.mma  D, A, B, D          # B200 ; warp scope
    # or, on H200:  wgmma.mma_async  D, A, B, D    # warp-group scope, 128 threads
t1 = clock64()
SI_LAT = (t1 - t0) / N               # 100 iterations, median reported

# --- throughput via independent issue ------------------------------------ [paper]
issue independent MMAs with no carried dependency -> saturation throughput

# --- memory latency ------------------------------------------------------- [paper]
pointer chase: dependent loads, no overlap    # p-chase

# --- TMEM staging --------------------------------------------------------- [paper]
tcgen05.alloc  tmem_desc                # reserve TMEM columns
tcgen05.cp     tmem <- smem             # asynchronous bulk copy into TMEM
tcgen05.mma    tmem_acc, A, B, tmem_acc # accumulate in TMEM, not in RF
tcgen05.ld     regs <- tmem             # only at the end of the chain
```

The paper's chained-operation claim rests on the last block: keeping intermediates in TMEM across a chain of matrix operations avoids "approximately 12 TB/s of data movement per SM" [paper] — a rate, i.e. avoided traffic per unit time at full utilisation, not a volume.

## 12.8 Real implementation

[artifact] `github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark` @ `91411b53aebaa4733477f22bde576b5182c669fc`.

- Top level: `Makefile`, `run-all.sh`, `requirements.txt`, `CITATION.cff`, `scripts/`, `tests/`, `results/` [code, tree].
- `tests/` contains `tcgen05.mma/`, `tensor-core/`, `tensor_benchmark/`, `memory/`, `case-studies/`, `test_benchmarks.sh` [code].
- `tests/tensor-core/standalone/` holds the per-precision SASS-verification sources: `tcgen05_sass_fp16.cu`, `tcgen05_sass_fp8.cu`, `tcgen05_sass_fp4.cu`, `tcgen05_sass_fp64_attempt.cu`, plus `latency_dependent_chain.cu`, `build_and_disasm.sh` and `generate_throughput_precision.py` [code]. **`latency_dependent_chain.cu` is the harness behind the SI-LAT table**, and the `_attempt` suffix on the FP64 file matches the paper's stated limitation that `tcgen05.mma` has no FP64 support.
- `results/` carries raw logs from both platforms: `results/b200/` and `results/h200/`, plus `results/tcgen05_analysis.log`, `results/tmem_analysis.log`, `results/tensor_core_results.csv`, and per-format decompression logs under `results/b200/DE/` (`format-{ans,bitcomp,cascade,deflate,gdeflate,gzip,lz4,snappy,zstd}.txt`, `pipeline-depth.txt`) [code].
- `results/b200/DisTensorCore/` contains `A100-ILP{1..8}.txt` [code] — **A100 data present in the artifact that the paper does not discuss**; do not treat it as part of the paper's evidence.
- `scripts/`: `generate_figures.py`, `generate_tables.py`, `parse_de_log.py`, `plot_decompression.py`, `process_results.py`, `run_de_benchmarks.sh`, `run_pipeline_depth_sweep.sh` [code].
- The README's setup instructions require **CUDA Toolkit 13.1+ and nvCOMP** [README], whereas the paper's methodology states **CUDA 12.6 / nvcc 12.6 / driver 560.x** [paper]. The artifact was evidently re-targeted after the measurements. **Numbers in this file are attributable to the CUDA 12.6 stack the paper names, not to the artifact's CUDA 13.1+ instructions.**
- `results/tmem_analysis.log` was opened; its head is only a banner line (`=== B200 TMEM Analysis ===`). Contents beyond that: `NOT_INSPECTED`.

## 12.9 Kernel execution

The kernel → block → warp → instruction path changes at two points on Blackwell [paper]:

1. **Block level**: CTA pairs with adjacent ranks share operands within a TPC over a dedicated network. This is operand sharing *between* thread blocks, which did not previously exist.
2. **Warp level**: matrix issue returns to warp scope. On Hopper a matrix operation required assembling a 128-thread warp group and synchronising it; on Blackwell a 32-thread warp issues `tcgen05.mma` directly. The paper attributes part of the SI-LAT reduction to removing that synchronisation.

Note the SASS mapping the paper reports [paper]: FP4 compiles to **OMMA**, FP6 to **QMMA**, verified by CUTLASS disassembly. These are SASS mnemonics observed by the authors, not documented ISA — `[paper]`, corroborated by the artifact's `tcgen05_sass_*.cu` + `build_and_disasm.sh` pair [code].

## 12.10 Memory traffic

Register ↔ TMEM ↔ shared memory is the new middle of the hierarchy. TMEM at 256 KB/SM and 16 TB/s read bandwidth sits between the register file and shared memory in role: it is where accumulators live across a chain of matrix ops, so results never round-trip to registers [paper].

**TMEM access latency is not reported** — the paper says a pointer-chase methodology was used but does not give TMEM latency values [paper]. `NOT_IN_PAPER`. This is a real gap for anyone trying to model TMEM.

Off-chip [paper, B200]: **STREAM Triad 4.14 TB/s** on 4–16 GB arrays, which is **51.8% of the 8 TB/s peak**. The paper flags the array-size restriction as a limitation (larger arrays needed 192+ GB of device memory it did not have), so the 51.8% figure is not a saturated-working-set measurement.

The **decompression engine** is a separate on-package data path. Measured on 100 MB datasets with 64 KB chunks [paper, B200]: output throughput 83.83 GB/s (GZIP) up to 539.21 GB/s (ANS); latency 0.194–1.251 ms; input bandwidth 42.00–173.23 GB/s. The structural finding: **decompressed output throughput is the limiter, not compressed-input bandwidth or DE compute**, with output holding at ~170–220 GB/s across data patterns while input bandwidth scales as 1/C for compression ratio C. Pipeline depth grows with chunk size (32 KB → depth 1, 55.84 GB/s peak; 64 KB → depth 2, 71.70 GB/s; 128–256 KB → depth 8, 87.67–112.10 GB/s), saturating at batch sizes 256–1024.

## 12.11 Why it is faster/slower (decomposed cause)

B200 versus H200, measured [paper]:

| Metric | B200 | H200 | Ratio |
|---|---|---|---|
| FP64 DGEMM | 36.3 TFLOP/s | 18.9 TFLOP/s | 1.92× |
| FP16 tensor | 1929.6 TFLOP/s | 1515.2 TFLOP/s | 1.27× |
| FP8 inference, Mistral-7B | 57,125 tok/s | 49,200 tok/s | 1.16× |
| GPT-1.3B training | 14,363 tok/s | 9,240 tok/s | 1.55× |
| ResNet-50 training | 2,928 img/s | 1,580 img/s | 1.85× |

Causes the paper attributes:
1. **Wider datapaths, not deeper pipelines** — 8.2× throughput spread against 1.12× latency spread across precisions.
2. **Accumulator width is the throughput limiter** — FP32 accumulation halves FP16 throughput at unchanged latency.
3. **Issue-scope reduction** removes warp-group synchronisation from the matrix path.
4. **FP64 does not benefit from any of this.** `tcgen05.mma` has no FP64 support; the 1.92× DGEMM gain comes from separate doubled FP64 units, and TMEM "does not benefit scientific HPC workloads directly" [paper]. **This is the single most important caveat for HPC readers**: the Blackwell matrix story and the FP64 story are disjoint.
5. Energy: 32% better efficiency than H200 on the training workloads [paper] — measured with NVML at 10 ms sampling.

**Accuracy cost, stated**: FP4 incurs an average **8.2% perplexity degradation**, requiring per-layer precision selection [paper]. A throughput number at FP4 is not comparable to one at FP8 without this.

## 12.12 Hardware generation dependence

- **Measured on real silicon**: NVIDIA **B200** (datacenter Blackwell) and **H200** (Hopper). CUDA 12.6, nvcc 12.6, driver 560.x, cuBLAS/cuBLASLt, PyTorch 2.4, Transformer Engine [paper].
- **This is datacenter Blackwell**, and must not be merged with consumer/workstation Blackwell results. In particular `GPU-MICRO25-61` (Huerta et al.) validates a core model against an **RTX 5070 Ti**, a GB20x consumer part with no TMEM, no `tcgen05` and no decompression engine in evidence. The two Blackwell datasets describe different products.
- Equally, `tcgen05`/TMEM findings must not be applied to Hopper (`wgmma`, accumulators in the register file) and Hopper's TMA/DSM must not be carried onto Blackwell without evidence.
- No AMD part appears.

## 12.13 Limitations

Stated [paper]:
- **`tcgen05.mma` has no FP64 support**; FP64 uses separate doubled units and TMEM gives scientific HPC no direct benefit.
- **STREAM limited to 4–16 GB arrays** for lack of 192+ GB device memory, so the 51.8%-of-peak figure is working-set-limited.
- **The simulation gap is not closed**: "Detailed architectural information required for accurate simulation remain unknown"; neither Accel-Sim nor GCoM models TMEM or the DE. The paper produces measurements, not a model.
- **Software ecosystem immaturity** — CUDA 13.0 gives only preliminary TMEM/CTA support.
- **FP4 accuracy cost** of 8.2% average perplexity degradation.
- Code sharing was blocked at submission time (superseded — see §12.8).

`[inference]`, not stated: **TMEM access latency is never reported**, though the methodology claims p-chase was applied. Without it, TMEM's position relative to the register file and shared memory in the latency hierarchy is unestablished, and the "16 TB/s read bandwidth" figure cannot be converted into an operand-supply model. Also, SI-LAT measured by an accumulator-carried dependency chain measures *dependent* issue-to-use latency; it is not the pipeline depth, and the paper's inference of "spatial array rather than temporal pipelining" from constant SI-LAT is an interpretation, not a measurement.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS` — but **cross-listed**: `domains/gpu_systems/corpus/_LEDGER_profiling_reliability.md` line 129 carries this paper as a `CORE_GPU` watchlist row reached from title + census evidence only, explicitly marked "Both full text and artifact are public and unexamined… → watchlist, priority", with no deep-analysis file. That ledger also supplies the Zenodo artifact DOI `10.5281/zenodo.18716313`. **This file discharges that watchlist item.** The sibling ledger's row should be updated to point here.
- **Direct generational successor to** `GPU-IPDPS24-61` (Luo et al., Hopper dissection, IPDPS 2024). Same venue, same method family (microbenchmark dissection of a new NVIDIA generation), two years apart, and the H200 baseline here is the part that paper's H800 measurements describe. Together they are the IPDPS Hopper→Blackwell characterisation line.
- **Complementary and in tension with** `GPU-MICRO25-61`: both report Blackwell results, on different products (B200 vs RTX 5070 Ti) with different methods (measurement-only vs measurement-into-simulator). MICRO'25 builds a Blackwell *model* at 17.41% MAPE; this paper says a Blackwell model of TMEM/DE is not yet possible. Both are correct — MICRO'25 models a consumer part without those units.
- **Overlaps the tensor-cores cluster**: `GPU-SC26-02` (EmuGEMM) already contrasts `wgmma.mma_async` (SM90, accumulators in the register file) with `tcgen05.mma` (SM100, accumulators in TMEM) from the kernel-author side; `GPU-PPoPP26-02` (Cubie) characterises matrix units across A100/H200/B200. This paper supplies the *measured instruction-level* basis those papers assume. **The accumulator-placement claim is now corroborated from two independent directions.**
- **Precursors cited** [paper]: the Tesla/Fermi memory-and-cache microbenchmark line; Kepler/Pascal/Maxwell warp-scheduling and instruction-latency work; Turing–Hopper mixed-precision and tensor-core studies; Accel-Sim and GCoM as the simulation frameworks that cannot yet model Blackwell.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The paper's central results are statements about the **issue scope of a warp**. Its headline structural finding is that matrix issue moved from **warp-group scope (128 threads, `wgmma`, synchronous)** on Hopper to **warp scope (32 threads, `tcgen05.mma`)** on Blackwell, with the removal of warp-group synchronisation named as a cause of the 2.9–11.2× SI-LAT reduction — a claim that presupposes warps, warp groups and their synchronisation semantics. The second finding, **TMEM**, is a per-SM operand store that exists specifically to take accumulators out of the per-warp register file; its geometry (512 columns × 128 lanes, lane-column addressed, 64×64 optimal tile filling a 1024-bit interface) is expressed in the lane coordinates of a SIMT datapath. The third, **CTA-pair operand sharing mapped to a TPC**, is a thread-block-scheduling construct. Even the measurement method is GPU-specific (`clock64` dependency chains at warp scope, SASS verification of PTX-to-OMMA/QMMA mapping). A generic matrix accelerator would have no warps, no warp groups and no CTA pairs, and the paper would have nothing to report.

verdict: `CORE_GPU`

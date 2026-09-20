# GPU-ASPLOS25-81 — Efficient Lossless Compression of Scientific Floating-Point Data on CPUs and GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `E GPU lossless compression / HBM & data movement`
secondary_topics: `E compression in the data path; B GPU kernel & memory-hierarchy design`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `Author-hosted PDF (userweb.cs.txstate.edu/~burtscher/papers/asplos25.pdf) read in two targeted passes: (1) title/authors/abstract, introduction and motivation, the four algorithms and every transformation component, chunking, and the full GPU implementation description; (2) evaluation — GPU and CPU SKUs, software versions, datasets, the 18 baselines, ratios and throughputs, limitations, related work and citation check. Plus artifact inspection of github.com/burtscher/FPcompress @ 97f037249bd28682bfd83462ea1129e14df36d81.`

## 12.1 Bibliographic facts
- Title: *Efficient Lossless Compression of Scientific Floating-Point Data on CPUs and GPUs* `[paper]`.
- Authors and affiliations `[paper]`: Noushin Azami, Alex Fallin, Martin Burtscher — Department of Computer Science, Texas State University.
- Venue: **ASPLOS 2025**, Session 4C, DOI `10.1145/3669940.3707280` `[census]`.
- Artifact `[artifact]` `[paper]`: `github.com/burtscher/FPcompress` @ `97f037249bd28682bfd83462ea1129e14df36d81`; the paper also gives an artifact DOI `10.5281/zenodo.14061031`; BSD 3-Clause.
- Publication type: `ARCHIVAL_MAIN_PAPER`; the read source is an author-hosted copy — `[paper]` evidence.

## 12.2 Core question (one sentence)
Can a *lossless* floating-point compressor escape the field's standing trade-off — "almost all compressors that compress well only deliver low speeds, and almost all compressors that compress and decompress quickly only deliver low compression ratios" `[paper]` — by composing a small set of reversible integer transformations that each parallelise cleanly, and by implementing that composition identically on CPU and GPU?

## 12.3 GPU/HPC problem translation
- **Compute**: reversible bit-level transforms (difference, bit transposition, zero/repetition elimination, a finite-context predictor). Cheap arithmetic; the cost is data movement and offset bookkeeping.
- **Memory**: the chunk size is chosen *by the memory hierarchy*: "chunks of 16 kilobytes… so that we can fit two chunk buffers in the GPU's shared memory and the CPU's L1 data cache" `[paper]`. One number serves both machines; this is the paper's cleanest design statement.
- **Synchronization**: the two hard points are (a) the prefix sums inside a chunk and (b) the global write-offset chain across chunks. The paper names its solution to (b) by its literature name.
- **Communication**: single GPU.
- **Scheduling**: chunks are handed to thread blocks dynamically through a global atomic counter — a persistent-block pattern, visible at `[code]`.

## 12.4 Why the problem exists
Root causes the paper names `[paper]`:
1. **Compression is only useful at both ends.** "data compression can help, but only if the compression ratio is sufficiently high" *and* "only if the compression throughput is high enough for real-time operation".
2. **The trade-off is empirical and near-universal** across the 18 compressors surveyed.
3. **Lossy compression is unacceptable for some domains**: "lossy compression could introduce errors that affect the validity of the scientific findings" in computational physics, climate modelling and medical imaging. This is why the paper sits outside the SZ/ZFP error-bounded line entirely.
4. **The representational insight that makes it tractable**: the algorithms "process single-precision floating-point values as 32-bit integers, and… double-precision floating-point values as 64-bit integers to guarantee lossless operation. Note that they do **not** convert… the floating-point values to integers. Instead, they treat the IEEE 754 floating-point word as an integer word." Every subsequent transform is an exactly invertible integer operation, so losslessness is structural rather than proved.

## 12.5 Mathematical / performance model
No closed-form model. The exact design objects `[paper]`:
- **Four algorithms**, two per precision, one tuned for speed and one for ratio:
  - `SPspeed`: **DIFFMS → MPLG**
  - `DPspeed`: **DIFFMS → MPLG**
  - `SPratio`: **DIFFMS → BIT → RZE**
  - `DPratio`: **FCM → DIFFMS → RAZE → RARE**
- **DIFFMS** (difference, magnitude-sign): consecutive-value integer difference — "Computing the integer difference turns these exponents into values that cluster around zero" — followed by a two's-complement→magnitude-sign conversion written explicitly as **`(data << 1) ^ (data >> 31)`** (arithmetic right shift replicating the sign bit).
- **MPLG** with an enhancement: "If the maximum has no leading zeros, which renders MPLG ineffective, we apply another two's-complement to magnitude-sign conversion to the values in the chunk."
- **BIT**: bit transposition — "the first bit of every value together, then all second bits", producing "long runs of zero values, which are typically followed by gradually more random values".
- **RZE**: a bitmap where "each bit corresponds to a byte in the input. A cleared bit indicates that the corresponding byte is zero", **compressed recursively**: "the original bitmap of **16384 bits** is reduced to **2048**, then **256**, and ultimately **32** bits" (each level an 8× reduction).
- **FCM** (finite context method, `DPratio` only): "an array of pairs… The first element of each pair is a hash of the three prior input values"; pairs are **sorted** to find matching values for predictive encoding.
- **RAZE**: adaptive — "treats the upper bits of each double separately from the lower bits and only applies RZE to the top *k* bits while always keeping the bottom 64−*k* bits", and "automatically finds the optimal *k*… computes what the compressed size would be for each of the **64** counts, selects the *k* that minimizes the size". An exhaustive 64-way search per chunk, which is only affordable because it is data-parallel.
- **RARE**: as RAZE, but tests "whether the top *k* bits are **the same as in the prior value**" rather than all-zero.
- **Chunk size 16 KB**, universal (except FCM). **Confirmed at `[code]`**: `static const int CS = 1024 * 16;  // chunk size (in bytes) [must be multiple of 8]` (`single_src/speed-compressor-single.cu:43`).

## 12.6 Data layout and ownership
- **value → integer word**: an IEEE 754 word reinterpreted, never converted.
- **values → chunk**: 16 KB, sized to hold **two** buffers in GPU shared memory *and* in a CPU L1D. **Confirmed at `[code]`**: `__shared__ long long chunk[2 * (CS / sizeof(long long)) + 4 + 17];` with `in`, `out` and `temp` pointers carved out of it at `speed-compressor-single.cu:157-163` — a double buffer plus scratch, exactly as described.
- **chunk → thread block**: "the chunks are assigned to the **thread blocks** rather than the individual threads" on the GPU `[paper]` (on the CPU a chunk goes to a thread). **Confirmed at `[code]`**: chunks are claimed dynamically via `if (tid == WS) chunk[last] = atomicAdd(&g_chunk_counter, 1);` (`:176`) inside a loop over chunks (`:172`) — a persistent-block work-stealing pattern, with `g_chunk_counter` a `__device__` global (`:102`).
- **bits → lanes (BIT stage)**: the transposition is a warp-width butterfly. "We take advantage of fast CUDA shuffle operations to exchange data between the threads in a warp (**without accessing memory**) to implement the bit transposition in **log₂(32) = 5 steps**" `[paper]`. **Confirmed at `[code]`**: `components/d_BIT_4.h` contains exactly five `__shfl_xor_sync(~0, a, N)` calls with `N = 16, 8, 4, 2, 1` (`:56,59,62,70,78`, repeated for the inverse at `:109-131`).
- **bytes → threads (RZE stage)**: "The RZE encoder assigns **multiples of 8 consecutive bytes** to each thread. The threads then check if the bytes are zero and set the needed bits in the bitmap", then "all threads compute a **block-wide parallel prefix sum** on these counts. Finally, they output their non-zero bytes at the location determined by the prefix sum" `[paper]`.
- **chunk → global output offset**: the variable-length problem. "We use **Merrill and Garland's variable look-back strategy** to quickly communicate the write position to the next thread block" `[paper]`. **Confirmed at `[code]`**: `propagate_carry(const int value, const int chunkID, volatile int* const __restrict__ fullcarry, int* const __restrict__ s_fullc)` at `speed-compressor-single.cu:111`, with the special case `if (chunkID == 0)` (`:113`), the negated-value "aggregate available" encoding `fullcarry[chunkID] = -value;` (`:119`), a lane-indexed look-back `const int cidm1ml = chunkID - 1 - lane;` (`:124`), and the resolved inclusive prefix `fullcarry[chunkID] = fullc + value;` (`:145`).

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only names printed in the paper `[paper]` or read in the artifact `[code]`:
```
CS = 16384                                  # bytes; two buffers fit GPU shared memory AND CPU L1D
__shared__ long long chunk[2*(CS/8) + 4 + 17];      # [code] in | out | temp
in, out, temp = carve(chunk)

while true:                                 # persistent blocks
    if tid == WS: chunk[last] = atomicAdd(&g_chunk_counter, 1)   # [code] dynamic chunk claim
    __syncthreads()
    chunkID = chunk[last]; base = chunkID * CS
    if chunkID >= chunks: break
    load min(CS, insize - base) bytes into `in`
    __syncthreads()

    # ---- transformation pipeline (SPratio shown) ----
    DIFFMS:  d = x[i] - x[i-1];  d = (d << 1) ^ (d >> 31)   # magnitude-sign
             (decode side: block-level parallel prefix sum over warp primitives)
    BIT:     5 butterfly steps, __shfl_xor_sync(~0, a, {16,8,4,2,1})   # [code] no memory traffic
    RZE:     each thread owns a multiple of 8 consecutive bytes
             set bitmap bits for non-zero bytes
             block-wide parallel prefix sum over per-thread non-zero counts
             each thread writes its non-zero bytes at its prefix-sum offset
             recurse on the bitmap: 16384 -> 2048 -> 256 -> 32 bits

    # ---- global placement ----
    propagate_carry(csize, chunkID, fullcarry, s_fullc)   # [code]
        # Merrill & Garland variable look-back:
        #   chunkID 0 publishes the inclusive prefix directly
        #   others publish -value  (aggregate available)
        #   a warp looks back at fullcarry[chunkID-1-lane] until an inclusive prefix is found
    write the compressed chunk at its resolved offset
```

## 12.8 Real implementation
Artifact `github.com/burtscher/FPcompress` @ `97f037249bd28682bfd83462ea1129e14df36d81` `[code]`. The tree is organised exactly as the paper's compositional story implies — one header per transformation, with `h_` (host/CPU) and `d_` (device/GPU) variants of each:
- `components/`: `h_DIFFMS_4.h`/`d_DIFFMS_4.h`, `h_DIFFMS_8.h`/`d_DIFFMS_8.h`, `h_BIT_4.h`/`d_BIT_4.h`, `h_RZE_1.h`/`d_RZE_1.h`, `d_RZEa_1.h`, `h_RAZE_8.h`/`d_RAZE_8.h`, `h_RARE_8.h`/`d_RARE_8.h`, `h_HCLOG_4.h`/`d_HCLOG_4.h`, `h_HCLOG_8.h`/`d_HCLOG_8.h`, `d_HCLOGa_4.h`, plus `components/include/` with the shared `*_zero_elimination.h` and `*_repetition_elimination.h` headers.
- `preprocessors/`: `h_FCMp_8.h`, `d_FCMp_8.h` — FCM appears only in the `_8` (double-precision) form, matching `DPratio` being the only algorithm that uses it.
- `single_src/`: `speed-compressor-single.cu`, `speed-decompressor-single.cu`, `ratio-compressor-single.cu`, `ratio-decompressor-single.cu`; `double_src/` the same four for doubles. **Compressor and decompressor are separate translation units**, i.e. separate kernels — this is not a single fused kernel in the cuSZp sense.
- **`HCLOG` is a component name present in the code that the read text does not explain** — the paper's pipeline figure names MPLG where the code calls the stage `HCLOG` (`d_HCLOG_4(csize, in, out, temp, fullcarry[chunkID], chunkID)` at `speed-compressor-single.cu:198`). The relationship between MPLG and HCLOG is **`UNKNOWN`** and is not guessed.
- Reproduction harness in-tree: `get_inputs_single.py`, `get_inputs_double.py`, `run_experiments_single.py`, `run_experiments_double.py`, `compile.py`, `chart_single.py`, `chart_double.py`.

## 12.9 Kernel execution
- **kernels**: separate compress and decompress kernels per algorithm per precision (8 `.cu` files) `[code]`. **Not fused.**
- **thread block**: owns one 16 KB chunk at a time and loops, claiming the next chunk with a global `atomicAdd` — a persistent/work-stealing grid rather than a one-block-per-chunk launch `[code]`.
- **warp**: the load-bearing level. Three distinct warp mechanisms appear:
  1. **Butterfly transpose** — 5 `__shfl_xor_sync` steps, explicitly "without accessing memory" `[paper]` `[code]`.
  2. **Block-wide prefix sums** "that utilize warp-level primitives and shared memory" for DIFFMS decoding and RZE placement `[paper]`.
  3. **Warp-parallel look-back** across chunk IDs in `propagate_carry`, indexed `chunkID - 1 - lane` `[code]` — one lane per predecessor, so the look-back examines 32 predecessors per step.
- **instruction**: `(data << 1) ^ (data >> 31)` for the magnitude-sign conversion `[paper]`; the RAZE/RARE 64-way *k* search is a data-parallel scan over 64 candidate split points `[paper]`.
- **FCM decode** uses a pointer-jumping / union-find-style path compression: "If the distance is non-zero, the thread subtracts the distance from the index and tries again… the threads tend to not iterate often because **other threads shorten the 'chains' continuously**" `[paper]` — a genuinely parallel formulation of a sequential predictor chain, and the most interesting algorithmic move in the paper.

## 12.10 Memory traffic
- **The chunk never leaves shared memory between stages**: "the encoder and decoder keep all chunk data in **shared memory between transformations** to minimize accesses to the relatively slow main memory" `[paper]`. This is the same architectural principle as cuSZ-i's `9×9×33` tile (`GPU-SC24-81`) and Aatrox's register-resident layers (`GPU-ICS25-81`) — keep the multi-stage pipeline on-chip and touch HBM once in, once out.
- **The BIT stage generates zero memory traffic at all** — the transpose happens entirely in the register file via `__shfl_xor_sync` `[paper]` `[code]`. A shared-memory transpose would have been the obvious implementation; using shuffles instead removes the traffic and the bank-conflict problem together.
- **16 KB × 2 buffers** is the shared-memory budget per block, plus 4+17 `long long` of scratch `[code]`. On an SM with 100–164 KB of shared memory that admits roughly 2–4 concurrent blocks — an occupancy consequence the paper does not discuss (`UNKNOWN`).
- **What the throughput is bounded by**: **`NOT_ESTABLISHED` explicitly, but the numbers strongly indicate HBM bandwidth and the paper comes closest of any in this cluster to saying so.** `SPspeed` compresses at **518 GB/s** and decompresses at **~500 GB/s** on an **RTX 4090 (1008 GB/s peak HBM)** `[paper]`. Compression must read the input and write the output; at a 1.41 ratio the traffic is roughly `1 + 1/1.41 ≈ 1.71` bytes moved per input byte, so 518 GB/s of input corresponds to ~886 GB/s of HBM traffic — **~88% of the RTX 4090's peak**. That arithmetic is `[inference]` (the paper reports neither achieved bandwidth nor a roofline), but it is the tightest bound-to-peak argument available anywhere in this cluster and it says `SPspeed` is essentially at the memory roof. `SPratio`, `DPratio` and anything involving FCM's **sort** are a different story and no comparable analysis is possible — `UNKNOWN`.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Every stage is a reversible integer transform with a data-parallel formulation.** Nothing in the pipeline is an entropy coder with a serial codeword dependency — which is exactly what makes cuSZ-i pay a CPU codebook excursion and what makes Ecco need speculative decoders. The ratio comes from *composition* of cheap transforms rather than from one expensive one.
2. **Everything stays on-chip between stages.** One HBM read, one HBM write, N transforms in between.
3. **The transpose is free.** Five register-file butterfly steps instead of a shared-memory transpose.
4. **Variable-length placement is solved with the standard single-pass technique** (Merrill–Garland look-back) rather than a separate scan kernel. Contrast `GPU-ICS26-81` (GPZ), which deliberately un-fuses the equivalent step into three kernels.
5. **Adaptivity is affordable because it is parallel.** RAZE evaluates all 64 candidate split points per chunk; a serial implementation would never do this.
6. **Where it costs**: `DPratio` requires a **sort** in FCM, and the paper notes "DPratio decompression substantially faster than compression (**no sorting required**)" `[paper]` — a clean asymmetry, the sort being the one non-streaming stage.
7. **Where it does not work**: "we do not expect our algorithms to compress non-smooth data particularly well" `[paper]`.

Numbers with full qualifiers `[paper]`:
- GPUs: **NVIDIA RTX 4090 (Lovelace, 24 GB, 16,384 PEs, 128 SMs)** and **NVIDIA A100 (Ampere, 40 GB, 6,912 PEs, 108 SMs)**.
- CPUs: **AMD Ryzen Threadripper 2950X (16 HT cores, 48 GB)**; **dual Intel Xeon Gold 6226R (2×16 cores, 64 GB)**.
- Software: **CUDA 12.0, NVIDIA driver 525.85.05, GCC 12.2.1**.
- Datasets: **90 single-precision files from 7 scientific domains** and **20 double-precision files from 5 domains**, from **SDRBench** plus supplementary data (climate, molecular dynamics, cosmology named).
- **18 baselines**: GPU — ANS, Bitcomp, Cascaded, Deflate, Gdeflate, GFC, LZ4, MPC, Snappy, ZSTD(GPU); CPU — Bzip2, FPC, FPzip, Gzip, pFPC, SPDP, ZFP, ZSTD(CPU); hybrid — Ndzip.
- **`SPspeed` on RTX 4090: compression ratio 1.41, 518 GB/s compression, ~500 GB/s decompression.** All three qualifiers present.
- `SPspeed` on the Ryzen: **75× faster compression and 55× faster decompression than FPzip**, with CPU throughputs in MB/s — "orders of magnitude slower than GPU".
- Headline: "our implementations outperform most of the 18 compressors… in compression ratio, compression throughput, **and** decompression throughput".

## 12.12 Hardware generation dependence
- **Two NVIDIA generations (Lovelace RTX 4090, Ampere A100)** plus **two CPU vendors** `[paper]` — the broadest cross-device evaluation in this cluster after GPZ.
- **Warp width 32 is baked into the BIT stage**: 5 butterfly steps is `log₂(32)`. On AMD's 64-lane wavefront this becomes 6 steps and the transposition's data layout changes. The code is CUDA-only (`.cu`, `__shfl_xor_sync`) with no HIP or SYCL variant in the tree `[code]`.
- **The 16 KB chunk is co-designed for both a GPU shared-memory budget and a CPU L1D** — a portability choice that constrains both targets. If either changed materially the constant would have to move.
- **Lossless, so there is no accuracy dimension to trade** across generations — the same bitstream is produced everywhere. This is a real portability advantage over every lossy compressor in this cluster.

## 12.13 Limitations
Author-stated `[paper]`:
1. "we do not expect our algorithms to compress non-smooth data particularly well" — the design targets spatially coherent simulation output.
2. `DPratio` compression is slowed by FCM's sort (stated as an asymmetry rather than framed as a limitation).

Recorded additionally from this reading:
3. **No achieved-bandwidth, occupancy or roofline figure**, despite `SPspeed` apparently running near the HBM roof (§12.10).
4. **Compression ratios are modest by scientific-compression standards** — `SPspeed` is 1.41 — because this is lossless. Direct comparison with the lossy numbers elsewhere in this cluster (cuSZ-i 13.3–256×, GPZ 219× on USGS) is **meaningless and must not be made**.
5. **CUDA-only implementation**; no AMD or Intel GPU result.
6. **The code names a stage `HCLOG` that the read text calls MPLG**; the relationship is `UNKNOWN`.
7. **No shared-memory-occupancy analysis** for a design that consumes 32 KB+ of scratchpad per block.

## 12.14 Relation to prior corpus
- `NO_EXISTING_ANALYSIS`. `[repo-grep]` hits were confined to `domains/gpu_systems/census/ASPLOS_2025.md`.
- **A fourth, separate community — and the citation evidence is unusually clean.** The paper compares against 18 compressors and **cites none of cuSZ, cuSZp, cuSZp2, FZ-GPU or cuZFP** `[paper]`. Its GPU baselines are the **nvCOMP** suite (ANS, Bitcomp, Cascaded, Deflate, Gdeflate, LZ4, Snappy, ZSTD), **GFC**, **MPC** and **ndzip-gpu** — the general-purpose and lossless-FP lineage, not the error-bounded lossy lineage. Symmetrically, none of cuSZ-i, Aatrox or GPZ cites this work. So the cluster contains at least **four non-communicating citation communities**: error-bounded lossy (SZ family), compression-in-collectives (gZCCL/NCCLZ), hardware cache compression (Ecco), and lossless FP (this paper + ndzip + nvCOMP).
- **But the *techniques* converge, and this paper is the proof.** It independently arrives at: 16 KB chunks sized to shared memory (cf. cuSZ-i's `9×9×33` tile); keeping the whole multi-stage pipeline on-chip; warp-shuffle communication instead of shared memory; and **Merrill–Garland variable look-back for variable-length output placement** — which is the *same algorithm* that cuSZp2 implements as `flag[]` + `__threadfence()` `[code]` and that Aatrox measures at 32.8% of compression time `[paper]`. **This paper is the only one in the cluster that names the technique by its literature name**, which retrospectively identifies what cuSZp2/Aatrox/GPZ are all doing or avoiding.
- **The one bridge to the lossy line is Bitcomp**: it is a baseline here and it is cuSZ-i's second lossless pass (`GPU-SC24-81` §12.8). Both papers use the same NVIDIA component from opposite directions.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — but this is the closest call among the compression papers in this cluster, and the reasoning is recorded in full because the title itself ("on CPUs and GPUs") is exactly the portability construction the strict test is meant to catch.**

The case for YES: the four algorithms are the same on both machines; the transformations are device-neutral integer operations; the paper genuinely delivers one design on two architectures.

The case for NO, which prevails:
1. **The single most important design constant is set by GPU shared memory.** 16 KB was chosen "so that we can fit **two chunk buffers in the GPU's shared memory** and the CPU's L1 data cache" `[paper]`. The GPU constraint is named first and is the tighter one; the CPU L1D is simply large enough to agree. The algorithm's fundamental unit of parallelism is a GPU scratchpad budget.
2. **The parallelisation is structurally different, not merely scaled.** "the chunks are assigned to the **thread blocks** rather than the individual threads" `[paper]` — on the CPU a chunk is one thread's serial work; on the GPU a chunk is 32+ threads cooperating. Every stage therefore needed a *new parallel formulation*: block-wide prefix sums for DIFFMS decode and RZE placement, a butterfly transpose for BIT, and a pointer-jumping union-find for FCM decode. These are not ports.
3. **BIT is a pure warp-register construction** — 5 `__shfl_xor_sync` steps "without accessing memory" `[paper]` `[code]`. There is no CPU counterpart; a CPU bit transpose is a cache-blocked memory operation.
4. **The FCM decoder's parallel form exists only because of massive thread counts**: it relies on "other threads shorten[ing] the 'chains' continuously" `[paper]`. That is a work-efficiency argument that requires thousands of concurrent workers.
5. **Merrill–Garland look-back exists solely because a GPU grid has no cheap global barrier.** A CPU implementation computes chunk offsets with a trivial serial scan. The `propagate_carry` warp-parallel look-back at `[code]` `speed-compressor-single.cu:111-145` has no reason to exist on a CPU.
6. **The results are not comparable across the two targets**: GPU throughput is in GB/s (518 GB/s), CPU throughput in MB/s, "orders of magnitude slower" `[paper]`. The paper's headline claim — beating 18 compressors on ratio *and* both throughputs — is a GPU claim.

verdict_basis: The chunk size is set by the GPU shared-memory budget; chunks are owned by thread blocks rather than threads, forcing a genuinely new parallel formulation of every stage (block-wide prefix sums, a 5-step `__shfl_xor_sync` butterfly transpose that touches no memory, a pointer-jumping parallel FCM decode); and the cross-chunk variable-length placement uses Merrill–Garland look-back, a technique that exists only because a GPU grid lacks a cheap global barrier.

## What the throughput is bounded by
**`NOT_ESTABLISHED` by the paper, but the tightest inferable case in this cluster.** `SPspeed` reports **518 GB/s compression / ~500 GB/s decompression at ratio 1.41 on an RTX 4090 (1008 GB/s peak HBM)** over 90 single-precision SDRBench files `[paper]`. Compression moves roughly `1 + 1/1.41 ≈ 1.71` bytes of HBM traffic per input byte, so 518 GB/s of input implies **~886 GB/s of HBM traffic, ~88% of peak** — i.e. `SPspeed` is essentially at the memory roof. **That arithmetic is `[inference]`; the paper reports no achieved bandwidth, occupancy or roofline.** For `SPratio` and especially `DPratio` the bound is different and unquantified: `DPratio` contains a **sort** inside FCM, which the paper identifies as the reason its compression is substantially slower than its decompression — `UNKNOWN`.

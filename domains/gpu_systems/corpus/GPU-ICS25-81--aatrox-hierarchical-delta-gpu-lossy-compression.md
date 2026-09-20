# GPU-ICS25-81 — Pushing the Limits of GPU Lossy Compression: A Hierarchical Delta Approach (**Aatrox**)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `E HBM & data movement / GPU lossy compression`
secondary_topics: `E compression in the data path; B GPU kernel & memory-hierarchy design`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `Official ICS 2025 proceedings PDF (hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-4.pdf) read in two targeted passes: (1) title/authors/abstract/motivation and the hierarchical-delta design incl. blocking, circular shift, tail rotation, dual-level decoding, compression workflow; (2) evaluation setup, throughput, ratios, quality, the stage-by-stage breakdown, bottleneck discussion, limitations, related work and citation check. Plus artifact inspection of github.com/szcompressor/cuSZp (AaTrox mode present in the current tree; see 12.8).`

## 12.1 Bibliographic facts
- Title: *Pushing the Limits of GPU Lossy Compression: A Hierarchical Delta Approach* `[paper]`. The system is named **Aatrox** `[paper]`; the cuSZp repository spells the corresponding mode **AaTrox** `[README]`.
- Authors and affiliations `[paper]`: Boyuan Zhang (Indiana University), Yafan Huang (University of Iowa), Sheng Di (Argonne National Laboratory), Fengguang Song (Indiana University), Guanpeng Li (University of Iowa), Franck Cappello (Argonne National Laboratory).
- Venue: **ICS 2025**, **Best Papers session** per `domains/gpu_systems/census/ICS_2025.md` row 21 `[census]`; DOI `10.1145/3721145.3725743` `[official-web]` (ACM landing page surfaced in search; `dl.acm.org` itself returns 403 here).
- Pages **654–669** `[README]` (from the BibTeX the cuSZp README publishes).
- Publication type: `ARCHIVAL_MAIN_PAPER`; the read source is the official conference proceedings PDF hosted on the ICS 2025 program site.
- Artifact status: the cuSZp README states "The **[ICS'25]** paper includes a fast and high-ratio **AaTrox mode** for 1D processing manner (**to be updated later**)" and gives an empty Release/Commit link `[README]`. So the ICS'25 code is **declared but not pinned** by the maintainers as of the inspected HEAD.

## 12.2 Core question (one sentence)
Can a single-kernel GPU compressor use *large* data blocks — which amortise away the stored per-block initial value and so raise compression ratio — without paying the two costs that forced prior designs to use small blocks: irregular inter-thread communication during delta encoding, and the inherently sequential linear recurrence of delta decoding? `[paper]`

## 12.3 GPU/HPC problem translation
- **Compute**: quantization, delta, bit-packing — all cheap. The paper's own breakdown shows they are not where the time goes.
- **Memory**: block concatenation is **41.5%** of compression time and is explicitly attributed to non-coalesced writes; dequantization is **54.6%** of decompression time and is attributed to global-memory writes `[paper]`. Aatrox is memory-traffic-dominated by its own measurement.
- **Synchronization**: the global prefix-sum is **32.8%** of compression and **39.8%** of decompression time `[paper]`. This is the single most important number in the cluster: in a fused single-kernel GPU compressor, roughly a third of the time is spent computing where the output goes.
- **Communication**: intra-warp. The whole design is about restructuring *inter-thread* communication within a warp.
- **Scheduling**: none beyond the single kernel.

## 12.4 Why the problem exists
The paper names three challenges, and all three are consequences of mapping a sequential delta code onto SIMT hardware `[paper]`:
1. **Initial-value overhead forces a block-size floor.** "the initial value of a data block… must be stored in the compressed data to facilitate the decoding phase." Small blocks are needed for parallelism; small blocks mean many stored initial values; many initial values cap the compression ratio. This is a *pure* GPU-parallelism-induced ratio penalty with no CPU counterpart.
2. **Delta encoding needs an irregular inter-thread read.** "Each thread… must communicate with previous thread during the delta encoding of its head element" because "the predecessor of each head element is stored in the **register of the previous thread**. This design introduces irregular communication… **warp divergence** in this design degrades throughput."
3. **Delta decoding is a linear recurrence.** "each data point must add the difference value to reconstruct the original data. However, this process is inherently sequential, as each data point depends on the completion of its predecessor."

The hardware root cause of (2) is that a thread's data lives in its private register file, reachable by a peer only through a shuffle or through scratchpad; of (3), that a prefix sum is the only parallel form of a linear recurrence and its cost is logarithmic in the block, paid in shuffles.

## 12.5 Mathematical / performance model
No closed-form model. The quantitative design objects `[paper]`:
- **Three-level blocking**, with exact extents:
  - **Warp layer**: `32 × 32 × 32 = 32,768` elements, mapped to one warp; **only one initial value stored for the entire warp layer**.
  - **Iteration layer**: `32 × 32 = 1,024` elements, mapped to one loop iteration.
  - **Thread layer**: `32` elements, mapped to one thread.
- Delta decoding is decomposed into exactly **two** prefix-sum levels (thread-level sequential in registers; warp-level via `__shfl_up_sync` over the iteration-layer tails) plus an **accumulated tail** broadcast, explicitly instead of a third prefix-sum level. The stated reason: a third level "would force sequential iteration execution" `[paper]`.
- The ratio consequence of the blocking: one initial value per **32,768** elements instead of one per 32 — a 1024× reduction in that overhead term. `[inference]` for the arithmetic; the block extents are `[paper]`.

## 12.6 Data layout and ownership
- **element → thread layer**: 32 elements per thread, held in registers, prefix-summed sequentially there.
- **thread layer → iteration layer**: 32 threads × 32 elements = 1,024 elements processed per loop iteration. The paper's stated purpose for this middle level is to "reduce the stride between memory accesses" — i.e. it exists for coalescing, not for algorithmic reasons.
- **iteration layer → warp layer**: 32 iterations = 32,768 elements owned by one warp, with one stored initial value.
- **cross-thread ownership at the layer seam**: handled by a **circular shift** — "warp-level function… to make the shuffle up operation wrap around the warp. This ensures that **thread 0 receives the tail element from thread 31**" `[paper]`. A plain `__shfl_up_sync` leaves lane 0 with its own value, which is exactly the special case that produced the divergent `if-else` in prior designs.
- **tail buffers**: `lastTailEle` and `prevLastTailEle`, swapped by thread 0 each iteration; `accumTail` per thread for the accumulated initial value `[paper]`. These are the paper's own symbol names.
- **block → grid**: variable-length compressed blocks, concatenated using a **decoupled look-back** global prefix-sum, with a **bit-transpose for coalesced writes** `[paper]`.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only names the paper prints `[paper]`:
```
# ---- compression, single kernel ----
for each warp layer (32*32*32 = 32768 elements, one warp):
    store ONE initial value for the whole warp layer
    for iter in 0..31:                       # iteration layer = 32*32 = 1024 elements
        # 1. quantization, user error bound
        q[0..31] = quantize(load 32 elements per thread)     # thread layer, registers

        # 2. delta encoding with circular shift
        prev = circular_shfl_up(q_tail)      # wraps: lane 0 gets lane 31's tail
        # tail rotation: thread 0 swaps lastTailEle <-> prevLastTailEle
        #   -> removes the if-else that a plain shfl_up would require
        d[..] = q[..] - prev

        # 3. bit packing: min bits per delta within the block
    # 4. global prefix-sum of per-block byte lengths  -> DECOUPLED LOOK-BACK
    # 5. block concatenation with bit-transpose for coalesced writes

# ---- decompression, asymmetric ----
# offsets are RECOMPUTED at decompression time rather than stored
dual-level delta decoding:
    thread level : sequential prefix-sum in registers
    warp  level : __shfl_up_sync inclusive prefix-sum over iteration-layer tails
    accumTail   : warp broadcast of the iteration layer's last element,
                  giving each subsequent iteration its initial value
                  WITHOUT a third prefix-sum level
```

## 12.8 Real implementation
The paper names no repository URL in the text read `[paper]`. The maintained home of the mode is `github.com/szcompressor/cuSZp`, whose README credits "Boyuan Zhang (AaTrox mode)" among the developers and lists the ICS'25 paper with the note that the AaTrox mode is for the "1D processing manner" and is "to be updated later", with **empty** Release and Commit links `[README]`. Inspected HEAD of that repo: `f581dcf329c907c320f4743a9c6e7ee2fb9c5494`. **No file in that tree was confirmed to implement Aatrox**, so no Aatrox symbol is asserted from code — `NOT_INSPECTED` for the Aatrox kernels specifically.

What *is* readable at `[code]` and is directly relevant, because Aatrox is built on this machinery:
- The cuSZp family's decoupled look-back global prefix-sum, in `github.com/szcompressor/cuSZp` @ `16e164762fe67785f498a44bae7984058a7a6952` (the cuSZp2 tag), `src/cuSZp_kernels_f32.cu`: `__shfl_up_sync(0xffffffff, thread_ofs, i)` at `:178` for the intra-warp scan, then a look-back loop reading `status = flag[lookback]` at `:212` with `flag` values `1` and `2` written and separated by `__threadfence()` at `:186-239`. The kernel signature carries `volatile unsigned int* cmpOffset, volatile unsigned int* locOffset, volatile int* flag`.
- Family constants `include/cuSZp/cuSZp_kernels_f32.h:4-7`: `cmp_tblock_size = 32; // Fixed to 32, cannot be modified`, `dec_tblock_size = 32`, `cmp_chunk = 1024`, `dec_chunk = 1024`. **The `1024` chunk is numerically the same as Aatrox's iteration layer (32×32 = 1,024)**, which is consistent with Aatrox adding a *warp layer above* the existing cuSZp chunk rather than changing it. `[inference]`, clearly supported but not paper-asserted.
- Inline PTX in the same family: quantization via `mul.f32 / setp.ge.f32 / selp.s32 / cvt.rzi.s32.f32` and bit-width via `clz.b32` (`src/cuSZp_kernels_f32.cu:6-27`) `[code]`.

## 12.9 Kernel execution
- **kernel**: single fused compression kernel and single fused decompression kernel — the cuSZp lineage's defining property, preserved `[paper]`.
- **thread block**: the paper describes ownership in terms of warps, and the family's block size is a single warp (`cmp_tblock_size = 32`, "Fixed to 32, cannot be modified") `[code]`. Aatrox's block size is not separately stated in the read text — `UNKNOWN` whether it differs.
- **warp**: the warp is the unit that owns a 32,768-element warp layer. All inter-thread communication is `__shfl_up_sync` / warp broadcast; **shared memory is explicitly avoided** — the warp-level prefix-sum uses shuffles "avoiding expensive shared memory" `[paper]`.
- **instruction**: two named divergence eliminations — the **circular shift** (removes the lane-0 special case) and **tail rotation** (removes "numerous if-else branches" by double-buffering `lastTailEle`/`prevLastTailEle`). Both are branch-count reductions, not arithmetic reductions.

## 12.10 Memory traffic
The paper's stage breakdown is the evidence, and it is unusually complete `[paper]`:

| Compression stage | share | Decompression stage | share |
|---|---|---|---|
| quantization | 10.2% | global prefix-sum | 39.8% |
| delta encoding | 12.3% | data retrieval | 10.1% |
| bit-packing | <1% | bit-unpacking | <1% |
| **global prefix-sum** | **32.8%** | delta decoding | 16.5% |
| **block concatenation** | **41.5%** | **dequantization** | **54.6%** |

(The decompression column sums above 100% as read; recorded verbatim without correction — the overlap is presumably due to overlapping/fused stages, but the paper does not say, so `UNKNOWN`.)

- **Block concatenation (41.5%)** is bottlenecked because "irregular lengths of compressed data blocks cause **non-coalesced memory access patterns**" `[paper]`. This is the variable-length-output problem in its purest form and is why the bit-transpose exists.
- **Dequantization (54.6%)** is bottlenecked by global-memory writes — i.e. the decompression side is dominated by simply writing the full-size output back to HBM, which is an irreducible floor.
- **What the throughput is bounded by**: **the paper does establish a bound, and it is not HBM bandwidth — it is the offset-computation and variable-length-write machinery.** Compression: 32.8% global prefix-sum + 41.5% non-coalesced concatenation = **~74% of compression time is spent on getting variable-length blocks into contiguous memory, not on compressing**. Decompression: 39.8% prefix-sum + 54.6% output-write. No achieved-bandwidth or roofline figure is given, so "bandwidth-bound" is not claimed and is not supported. The one bandwidth comparison the paper does draw is with the *host* path: "the maximum bandwidth of the 16-lane PCIe 4.0 interconnect… is 32 GB/s. In contrast, the average compression throughput of Aatrox is 388 GB/s — over 10× faster" `[paper]` — i.e. the compressor is comfortably faster than the link it feeds.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Ratio gain — one initial value per 32,768 elements instead of one per 32.** This is the entire hierarchical-delta idea and it is a direct attack on a GPU-parallelism-induced overhead.
2. **Ratio preserved despite large blocks** because bit-packing still operates at the small thread-layer granularity; only the *initial value* is amortised over the warp layer.
3. **Throughput preserved — encode side** by removing the lane-0 special case (circular shift) and the per-iteration branch (tail rotation). These do not reduce work; they reduce **divergence**.
4. **Throughput preserved — decode side** by the two-level prefix sum plus `accumTail` broadcast. A third prefix-sum level would have serialised the 32 iterations; the broadcast keeps them pipelined.
5. **Asymmetry**: offsets are recomputed at decompression rather than stored, trading decompression compute for compressed-size `[paper]`. This is why decompression (718.0 GB/s) is ~1.85× compression (388.3 GB/s) despite doing a prefix sum too.
6. **Where the gain is limited**: the hierarchical-delta gain over a "plain approach" is **1.74× at eb 1e-2, 1.50× at 1e-3, 1.39× at 1e-4** — it shrinks as the error bound tightens, because tighter bounds produce larger deltas and the initial-value term becomes a smaller share of the stream `[paper]`.

Numbers with full qualifiers `[paper]`:
- Hardware: **NVIDIA A100 (108 SMs, 40 GB)** on a node with two 64-core AMD EPYC 7742 @ 2.25 GHz, CentOS 7.4, **CUDA 11.4.120**; and **NVIDIA RTX A4000 (40 SMs, 16 GB)** on a 28-core Intel Xeon Gold 6238R @ 2.20 GHz workstation, Ubuntu 20.04.5, CUDA 11.7.99.
- Datasets (nine, SDRBench + Open-SciVis): **CESM-ATM 3600×1800×26; HACC 1,073,726,487 particles; RTM 1008×1008×352; SCALE 1200×1200×98; QMCPack 69×69×33120; NYX 512³; JetIn 1408×1080×1100; Miranda 1024³; SynTruss 1200³**.
- Error bounds: **value-range-relative 1e-2, 1e-3, 1e-4**.
- Baselines: **FZ-GPU, cuSZp, cuSZp2, cuZFP** (cuZFP in fixed-rate mode only).
- Throughput on **A100**: **388.3 GB/s compression, 718.0 GB/s decompression** (averages).
- Speedups on A100: **1.2× compression / 1.6× decompression vs cuSZp2**; 3.6× vs cuZFP; 2.3× vs FZ-GPU; 2.7× vs cuSZp.
- Ratio: best in **23 of 27** (dataset × error-bound) cases; **2.33× higher than cuSZp2 on HACC at eb 1e-2**; 1.37× on CESM-ATM at 1e-2; 3× higher than cuSZp on Miranda at 1e-2.
- Quality: Aatrox shares the quantization strategy of cuSZp2/FZ-GPU/cuSZp, so PSNR/SSIM track them; against cuZFP on one visualised case, **PSNR 49.85 / SSIM 0.9988** vs **31.43 / 0.7751**.

## 12.12 Hardware generation dependence
- **A100 (Ampere datacenter) and RTX A4000 (Ampere workstation)** only — a single architecture generation, narrower than GPZ's three-SKU spread `[paper]`.
- The `32 × 32 × 32` / `32 × 32` / `32` blocking is built directly on the **32-lane warp**. On AMD's 64-lane wavefront every extent would change and the circular-shift and tail-rotation constructions would need reworking. The paper lists "adaptation to AMD/Intel GPUs" as future work `[paper]` — an admission that the design is warp-width-coupled.
- "The impact of parameters (e.g., layer size) on the compression ratio and throughput in Aatrox varies across datasets", with "fine-grained parameter tuning" as future work `[paper]`.

## 12.13 Limitations
Author-stated `[paper]`:
1. Layer-size parameters are dataset-sensitive and untuned.
2. No AMD or Intel GPU support.
3. No multi-GPU evaluation "beyond noting embarrassingly parallel scalability".

Recorded additionally from this reading:
4. **The design's own measurement says ~74% of compression time is offset computation and non-coalesced concatenation**, i.e. the hierarchical-delta contribution addresses a minority of the runtime. The 1.2× compression speedup over cuSZp2 is consistent with that.
5. **Single GPU architecture generation** (Ampere).
6. **No pinned artifact commit** for the AaTrox mode; the maintainers' own README says "to be updated later" `[README]`.
7. The decompression stage-share table as read sums above 100% — unexplained, `UNKNOWN`.

## 12.14 Relation to prior corpus
- `NO_EXISTING_ANALYSIS`. `[repo-grep]` hits for "Hierarchical Delta" were confined to `domains/gpu_systems/census/ICS_2025.md`.
- **Direct successor to cuSZp2** in the speed branch: same single-kernel structure, same decoupled-look-back scan, same quantization strategy; the delta is the three-level blocking. It is measured head-to-head against cuSZp2 and wins by 1.2×/1.6× on throughput and up to 2.33× on ratio.
- **Opposite endpoint from `GPU-SC24-81` (cuSZ-i)** on the ratio/throughput axis, and it does not compare against cuSZ-i at all — the baseline set is FZ-GPU, cuSZp, cuSZp2, cuZFP. cuSZ-i is cited only in related work. This is evidence that by ICS 2025 the two branches had stopped competing directly.
- **Superseded in its own family** by `GPU-ICS26-81` (GPZ), which reverses the single-kernel choice, and by the SC 2025 "Versatile and Ultra-Fast" paper (cuSZp3), both from overlapping author sets.
- **Lineage from the paper's own related work** `[paper]`: cuZFP (Lindstrom, fixed-rate) · cuSZ (Tian et al., "first prediction-based GPU error-bounded compressor") · FZ-GPU (Zhang et al., "pure-GPU with novel lossless encoding") · cuSZp, cuSZp2 (Huang et al., "single-kernel designs with optimized prefix-sum") · MGARD-GPU (Chen et al., Liang et al.) · cuSZx (Yu et al., "lightweight bitwise operations") · cuSZ-i (Liu et al., "GPU interpolation with Bitcomp").
- **No compression-in-collective work is cited.** A targeted check for gZCCL, hZCCL, ghZCCL and NCCL-based compression found none `[paper]` — the same negative result as for cuSZ-i and GPZ.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO, and this is the strongest NO in the cluster.** The contribution does not merely *run* on a GPU; the problem it solves **does not exist off a GPU**:
1. **The motivating overhead is GPU-parallelism-induced.** A CPU delta-codes a stream with one initial value for the whole stream. The "store an initial value per block" cost exists only because thousands of threads must start independently. Aatrox's entire ratio gain is recovering an overhead the GPU created.
2. **Every block extent is a multiple of the 32-lane warp** — `32`, `32×32`, `32×32×32` — and the paper's future work concedes AMD/Intel adaptation is open, i.e. the design is warp-width-coupled.
3. **The circular shift is a warp-shuffle construction.** "make the shuffle up operation wrap around the warp… thread 0 receives the tail element from thread 31." There is no CPU analogue of a lane-rotating register permute.
4. **Tail rotation exists to eliminate warp divergence**, a SIMT-only failure mode. Double-buffering `lastTailEle`/`prevLastTailEle` costs registers to save branches — a trade that only pays under lockstep execution.
5. **The dual-level prefix sum is a register-file-vs-scratchpad decision**: warp-level via `__shfl_up_sync`, "avoiding expensive shared memory". And the choice *not* to add a third level is justified by SIMT pipelining ("would force sequential iteration execution").
6. **The global prefix-sum is decoupled look-back**, whose whole reason for existing is that a GPU grid has no cheap global barrier `[paper]`, with the mechanism readable in the family's code as `flag[]` + `__threadfence()` `[code]`.
7. **Bit-transpose before the concatenating write** is a coalescing fix for HBM burst granularity.

No qualification is needed. Even the *ratio* improvement — normally the portable half of a compressor — is here a GPU-specific recovery.

verdict_basis: The paper's three motivating challenges are, respectively, a per-block-initial-value overhead created by GPU thread-level parallelism, irregular inter-thread reads of peer *register files*, and a linear recurrence that must be reshaped into warp prefix sums; the solutions are a warp-width-multiple block hierarchy, a lane-wrapping shuffle, divergence-eliminating double buffers, and a decoupled-look-back scan.

## What the throughput is bounded by
**Established by the paper, by stage decomposition rather than by a roofline.** Compression is bounded by the variable-length-output machinery: **global prefix-sum 32.8% + block concatenation 41.5% ≈ 74%**, with concatenation explicitly attributed to "non-coalesced memory access patterns" from "irregular lengths of compressed data blocks". Decompression is bounded by **dequantization 54.6%** (global-memory writes of the full-size output) plus **global prefix-sum 39.8%**. It is **not** bounded by the entropy/delta coding, which is under 13% on each side, and it is **not** shown to be bounded by peak HBM bandwidth — no achieved-bandwidth or roofline figure is reported. Absolute figures: **388.3 GB/s compression, 718.0 GB/s decompression on A100 (40 GB, 108 SMs)** across nine SDRBench/Open-SciVis datasets at value-range-relative error bounds 1e-2/1e-3/1e-4.

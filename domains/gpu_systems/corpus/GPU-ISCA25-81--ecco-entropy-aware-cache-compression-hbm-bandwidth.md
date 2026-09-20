# GPU-ISCA25-81 — Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `E HBM & data movement / compression in the data path`
secondary_topics: `E GPU lossy compression; GPU memory hierarchy (L1/L2/HBM)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2505.06901v1) read in three targeted passes: (1) title/authors/affiliations/abstract/introduction/background and the compression target; (2) design — group-wise non-uniform quantization with shared k-means patterns, clipped/padded Huffman, the parallel decoding pipeline, placement in the memory hierarchy, area/power; (3) evaluation — simulator and validation, GPU configuration, models, baselines, results, accuracy, ablation, limitations, related work.`

## 12.1 Bibliographic facts
- Title: *Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression* `[paper]`.
- Authors and affiliations `[paper]`: Feng Cheng, Cong Guo, Chiyue Wei, Junyao Zhang, Changchun Zhou, Hai "Helen" Li, Yiran Chen (Duke University); Edward Hanson, Jiaqi Zhang, Xiaoxiao Liu (Advanced Micro Devices, Inc.).
- Venue: **ISCA 2025** — the paper prints it: "Proceedings of the 52nd Annual International Symposium on Computer Architecture (ISCA '25), June 21–25, 2025, Tokyo, Japan" `[paper]`. DOI `10.1145/3695053.3731024` `[census]`.
- arXiv 2505.06901 (v1 read). Publication type: `ARCHIVAL_MAIN_PAPER`; read source is the `PREPRINT`.
- Artifact: none named in the read text. `NOT_INSPECTED`.
- **`prior_corpus_check` note**: this is an LLM-inference architecture paper and plausibly belongs to the `EXTERNAL_IMPORT_PENDING` ~80-paper AI/HPC corpus under `domains/ai_hpc_systems/`. Repo-wide grep found "Ecco" only in `domains/gpu_systems/census/ISCA_2025.md`. **No claim of non-duplication is made.** `[repo-grep]`

## 12.2 Core question (one sentence)
Can a compressor be placed *inside the GPU memory hierarchy* — between L1 and L2 on the read path and between L2 and HBM on the write path — such that it delivers both bandwidth and capacity amplification for LLM inference, given that any such compressor must decode at L2 throughput and therefore cannot use a conventional sequential entropy decoder? `[paper]`

## 12.3 GPU/HPC problem translation
- **Memory**: this is a pure memory-hierarchy paper. The object is HBM bandwidth and capacity, and the mechanism lives in the cache hierarchy.
- **Compute**: the compressor/decompressor are fixed-function hardware blocks, not kernels. No SM cycles are consumed.
- **Synchronization**: none — transparency to the SM is the design goal.
- **Communication**: none (single GPU).
- **Scheduling**: none.
- **Why it is in this cluster**: it is the clearest instance in the corpus of *compression in the data path* as opposed to compression as an application-level pass. Every other compression paper in this cluster runs as a CUDA kernel the programmer invokes; Ecco runs below the ISA.

## 12.4 Why the problem exists
Root causes the paper's framing rests on `[paper]`:
1. **LLM decoding is memory-bandwidth-bound.** The evaluation is confined to the decoding phase precisely because it is bandwidth-bound; the prefill phase is excluded as "compute-bound, negligible execution time".
2. **HBM capacity limits model and KV-cache size**, hence the 4× capacity claim.
3. **Software quantization does not fix the traffic problem at the right layer.** AWQ, SmoothQuant, GPTQ, QuaRot etc. change the tensor format the kernel sees; Ecco keeps the SM's view and changes what crosses L2↔HBM.
4. **The hardware root cause that makes this hard**: an entropy coder is inherently serial — codeword *n*'s position depends on codewords 0..*n*−1. A GPU L2 sustains **5120 bytes per clock cycle** `[paper]`; a sequential Huffman decoder is orders of magnitude off that. The paper's own framing is that its parallel decoder reduces latency "by two orders of magnitude compared to traditional sequential Huffman". **This is the same variable-length-decoding problem that Aatrox (`GPU-ICS25-81`) and cuSZp2 solve in software with warp shuffles and decoupled look-back — solved here in silicon instead.**

## 12.5 Mathematical / performance model
No closed-form model; the design is specified by exact parameters `[paper]`:
- **Group sizes**: **128 data elements per group** for weights and KV cache; **64 data points per group** for activations.
- **Target precisions**: **4 bits/point at 128 points/group** (weights, KV cache); **8 bits/point at 64 points/group** (activations).
- **Clustering**: "activation-aware k-means clustering with **15 clusters** is performed on the remaining 127 values" (the group maximum is reserved); then "a second k-means clustering with **S** clusters is applied to the k-means patterns across all groups".
- **Chosen configuration**: **S = 64, H = 4**, from a design-space exploration. The compressor further reduces "the number of shared k-means patterns … from 64 to 16".
- **Scale factor**: "the absolute maximum value within each group is identified and normalized using a per-tensor FP16-to-FP8 scale factor"; that maximum "is assigned index 15".
- **Huffman**: **H = 4 codebooks, each with 16 codes**; code length **restricted to 2–8 bits** "to enable efficient decoding"; **log₂H = 2 bits per group** to record which codebook was used.
- **Block target**: compressed block **64 bytes** (one cache line); minimum threshold **32 bytes** (one sector).
- **Padding**: "each padded value occupies **15 bits**, with **7 bits for location information and 8 bits for the FP8 value**", filling from the second-largest absolute value downward.
- **Clipping**: excess is simply clipped; measured clipping ratio **below 0.04%** for projection layers.
- **Latency**: decompressor **28 clock cycles** pipelined; compressor **62 cycles**.
- **Replication**: **20×**, "aligning their throughput with the L2 cache's peak throughput of 5120 bytes per clock cycle".

## 12.6 Data layout and ownership
This paper's ownership hierarchy is *not* thread→warp→block; it is a hardware-datapath hierarchy, and that is itself the point.
- **data element → group**: 128 (weights/KV) or 64 (activations) elements share one scale factor, one k-means pattern index and one Huffman codebook selector.
- **group → compressed block**: 64 bytes, i.e. exactly one cache line, with a 32-byte (one-sector) floor. Aligning the compression unit to the **cache line and sector granularity** is what lets compressed data be addressed without an indirection table.
- **decoder → sub-decoder**: **64 Huffman decoders in parallel** over overlapping sections; **each decoder contains 8 sub-decoders** that process "the same 15-bit data chunk but starting at different positions (0 to 7)". Each decoder "processes 8 bits of its group ensuring decoding of at least one and at most four data points".
- **merge tree**: a data concatenator "merges the outputs of every two neighboring decoders over **six stages** in a tree-like manner" (2⁶ = 64, matching the 64 decoders) until "only a single result remains".
- **placement in the hierarchy** `[paper]`: **decompressor between the L1 data cache and the L2 cache**; **compressor between the L2 cache and HBM**. So L2 holds *compressed* lines — which is how the capacity gain reaches both L2 and HBM — and the SM sees uncompressed data.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only the paper's parameters and stage names `[paper]`:
```
# ---- compress: L2 -> HBM, 62 cycles, off the critical path ----
for each group (128 elements for weights/KV, 64 for activations):
    amax = max(|x|)                        # index 15, stored as the scale factor
    normalize by a per-tensor FP16->FP8 scale factor
    idx[i] = nearest of 15 activation-aware k-means centroids   # 4 bits
    pattern = nearest of S=64 shared k-means patterns           # reduced to 16 in the compressor
    cb = select 1 of H=4 Huffman codebooks                      # 2 bits recorded per group
    bits = huffman_encode(idx, cb)                              # code lengths restricted to 2..8 bits
    if len(bits) < 64 B:  pad with (7-bit location, 8-bit FP8) = 15-bit entries,
                          largest-magnitude first
    if len(bits) > 64 B:  clip the excess                       # measured < 0.04% on projections
    emit a 64-byte block  (floor: 32 B = one sector)

# ---- decompress: HBM -> L2 -> L1, 28 cycles, ON the critical path ----
# 64 parallel Huffman decoders over OVERLAPPING sections
for d in 0..63:
    for s in 0..7:                        # 8 sub-decoders per decoder
        speculatively decode the same 15-bit chunk starting at bit offset s
    # each decoder yields >=1 and <=4 data points from its 8 bits
# 6-stage binary merge tree resolves which speculative start was correct
#   and concatenates -> one result
# the whole block is replicated 20x to match 5120 B/cycle L2 throughput
```

## 12.8 Real implementation
**No software artifact.** The implementation is RTL synthesised with **Synopsys Design Compiler using ARM standard cells at 28 nm, scaled to 7 nm** `[paper]`. `NOT_INSPECTED` — no RTL or code was read, and no module name is asserted.
The performance evaluation is **simulated**: "Modified **Accel-Sim** and **GPGPU-Sim 4.0** with **NVBit 1.7.1**" for trace extraction, with "simulation error … within 10% of the real GPU performance", correlated against real A100 hardware and cuBLAS/CUTLASS benchmarks `[paper]`.
**This is a simulation + synthesis paper, not a measured-hardware paper.** Every speedup below is a simulator result; every area and power number is a synthesis result. Recorded prominently because the rest of this cluster reports measurements on real GPUs.

## 12.9 Kernel execution
`NOT_APPLICABLE` in the usual sense — Ecco adds no kernel. The relevant execution facts `[paper]`:
- The decompressor sits on the **L1↔L2 path** and therefore on the SM's load critical path, at **28 pipelined cycles**. This latency is added to every L2 hit and every HBM fill that the SM consumes.
- The compressor sits on the **L2↔HBM path** at **62 cycles**, which the paper places off the critical path (writebacks and evictions are not latency-critical).
- Both are replicated **20×** to sustain **5120 B/cycle**.
- **Transparency**: no change to the SM, no change to the ISA, no change to kernel code. This is the property that distinguishes Ecco from every other compressor in this cluster.

## 12.10 Memory traffic
- **HBM traffic** falls by the compression factor (4× for weights/KV at 4 bits from FP16; 2× for activations at 8 bits). The paper reports two hardware variants, "4×" and "2×", with separate area and power figures — consistent with two compression ratios being supported.
- **L2 capacity** is amplified because L2 holds compressed lines.
- **No additional memory transactions** are introduced: compression is "on-the-fly … without requiring additional memory transactions" `[paper]`. This is the key differentiator against a software compressor, which must read the uncompressed data and write the compressed data as separate HBM passes — the exact cost that dominates Aatrox (74% of compression time in offset computation and concatenation, `GPU-ICS25-81`).
- **Granularity alignment**: 64-byte blocks with a 32-byte sector floor means a compressed line still maps to whole sectors, so HBM burst granularity is respected and no gather is needed.
- **What the throughput is bounded by**: **the paper establishes the design constraint explicitly and meets it by construction.** The binding requirement is that decompression must sustain **5120 bytes/cycle**, the A100 L2's peak throughput; Ecco meets it by replicating a 28-cycle pipelined decoder **20×**. So the compressor is *not* the bottleneck by design — the system remains bounded by HBM bandwidth, which is what the compression ratio then relieves. This is the one paper in the cluster where the throughput bound is a *specification* rather than a measurement, and it is honestly stated as such.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Fewer HBM bytes per token.** LLM decoding is bandwidth-bound; a 4× reduction in weight and KV-cache traffic translates close to directly into speedup.
2. **Larger effective L2** because L2 lines are compressed — a second-order bandwidth win (more hits) on top of the first-order HBM win.
3. **Entropy coding, not just quantization, is what buys the ratio.** Group-wise non-uniform quantization to 15 centroids plus Huffman over those indices extracts redundancy that uniform quantization leaves on the table; this is why Ecco beats AWQ/SmoothQuant/Olive at comparable or better accuracy.
4. **The decoder is parallel by speculation, not by parallel-friendly coding.** 8 sub-decoders per decoder try all 8 possible bit-offsets simultaneously, and a 6-stage merge tree resolves which was right. This is a pure area-for-latency trade — exactly the move a software implementation cannot make, because a GPU thread cannot afford to speculate 8 ways. It is the architectural counterpart to Aatrox's warp-shuffle prefix sum and cuSZp2's decoupled look-back.
5. **Code-length clipping to 2–8 bits** bounds the speculation fan-out: with a maximum 8-bit codeword, 8 starting offsets cover every possibility within a byte.
6. **Where it loses** `[paper]`: **Grouped-Query Attention models show reduced speedup** (Mistral-7B, LLaMA2-70B) "because GQA converts memory-bound GEMVs into compute-bound GEMMs" — i.e. Ecco's benefit evaporates exactly where the workload stops being bandwidth-bound. This is an honest and important limitation, and it generalises: every compression-in-the-data-path scheme is worth nothing on a compute-bound phase.

Numbers with full qualifiers `[paper]`, all **simulated on a modelled NVIDIA A100 (Ampere) in modified Accel-Sim / GPGPU-Sim 4.0, traces via NVBit 1.7.1, stated simulation error within 10%**:
- Models: **LLaMA 7B/13B/30B/65B, LLaMA-2 7B/13B/70B, Mistral-7B, LLaMA-3.1-8B-Instruct**; decoding phase only, **batch sizes 1–64, sequence lengths 1K–4K**.
- Baselines: **AWQ, SmoothQuant (W8A8), Olive, GPTQ-R, QuaRot, QoQ, TensorRT-LLM FP16**; configurations **W4A16** and **W4A8KV4**.
- Speedups: **up to 2.9× vs AWQ; 2.4× vs Olive; 1.8× vs SmoothQuant; average 2.9× vs FP16**.
- Capacity: **nearly 4×**.
- Accuracy: WikiText-2 perplexity best among baselines in W4A8KV4 across LLaMA/LLaMA-2 7B–70B; **slightly worse than AWQ on LLaMA-7B in W4A16**. Zero-shot: **71.49% average on LLaMA-2-13B vs 69.01% for QuaRot**.
- Padding/clipping: projection layers **<0.04% clipping, ~0.7% padding**; **K-cache 7.11%** and **V-cache 2.19%** padding.
- Area (synthesised 28 nm → scaled 7 nm, against an **826 mm² A100 die**): decompressor 4× **3.19 mm²**, decompressor 2× **0.57**, compressor 4× **0.91**, compressor 2× **0.44**; **total 5.11 mm², <1%**.
- Power: **7.36 W total**, "less than 10% of the A100's idle power of 82 W at 1410 MHz".

## 12.12 Hardware generation dependence
- Modelled on **A100 (Ampere)** only, with the design tied to A100-specific numbers: **L2 peak 5120 B/cycle**, **826 mm² die**, **82 W idle at 1410 MHz** `[paper]`. The 20× replication factor is derived from the A100 L2 throughput and would have to change on any other part.
- **NVIDIA A100 already has lossless cache compression** and the paper cites it in related work `[paper]` — so Ecco is proposing to replace/augment an existing hardware mechanism, not to introduce compression to a GPU that lacks it. The paper does not report a head-to-head against A100's native compression — a notable gap, recorded as `UNKNOWN`.
- The design is **not** tied to any NVIDIA-specific instruction; it is a datapath block and would port to any GPU with an L1/L2/HBM hierarchy. The AMD co-authorship is consistent with that.
- Requires hardware change, so it is unavailable on any shipping GPU — the strongest generation dependence of all.

## 12.13 Limitations
Author-stated `[paper]`:
1. **GQA models show reduced speedup** because GQA turns memory-bound GEMVs into compute-bound GEMMs.
2. **Prefill phase not evaluated** (compute-bound, negligible time).
3. **Simulation limited to ≤4K sequence length** due to simulator speed.

Recorded additionally from this reading:
4. **Everything is simulated or synthesised; nothing is measured on hardware.** The 10% simulator-error claim is the only validation.
5. **No comparison against A100's own lossless cache compression**, which the paper itself cites as prior art.
6. **Lossy in a way software quantization baselines are not uniformly**: clipping discards data outright when a block overflows. The measured 0.04% clipping is on projection layers; **K-cache padding at 7.11%** indicates the KV cache behaves very differently, and no clipping rate for KV is reported — `UNKNOWN`.
7. **No artifact.**
8. The 28-cycle decompressor sits on the L1↔L2 critical path; the paper does not report the end-to-end latency sensitivity of cache-hit-bound phases to that addition — `UNKNOWN`.

## 12.14 Relation to prior corpus
- `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — see 12.1. `[repo-grep]`
- **The architectural counterpoint to the whole SZ-family branch of this cluster.** cuSZ-i, Aatrox, GPZ and cuSZp2 all solve variable-length encoding *in software*, and all four are limited by it: Aatrox measures 32.8% of compression time in the global prefix sum and 41.5% in non-coalesced concatenation; GPZ un-fuses its compaction into three kernels to escape the same dependency; cuSZ-i moves its Huffman codebook build to the CPU. Ecco shows what the same problem costs when you are allowed to spend silicon: **8-way speculative sub-decoders and a 6-stage merge tree, 5.11 mm² and 7.36 W, under 1% of an A100 die**. Reading them together gives the cluster its sharpest finding — see the ledger.
- **Distinct from the scientific-compression line in target and in citation graph**: Ecco's related work is BDI, Buddy Compression, GIST, JPEG-ACT, A100 lossless cache compression, and the LLM quantization literature (AWQ, SmoothQuant, GPTQ, QuaRot). **It cites no SZ-family compressor** `[paper]`. Symmetrically, none of the SZ-family papers read here cites Ecco or any hardware cache compressor. A **third separate community**, alongside the standalone-compressor line and the compression-in-collectives line.
- **Complementary to `GPU-SC26-22` (NCCLZ)**: NCCLZ removes bytes from the inter-node wire; Ecco removes bytes from the L2↔HBM path. Neither cites the other.
- **Relevant to the memory cluster's `_LEDGER_memory_virtualization.md`** (Buddy Compression is a capacity-expansion technique of the kind that ledger tracks), but this analysis makes no claim about that ledger's contents.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — and this is the cleanest NO in the cluster, though for a different reason than the software compressors.**
1. **The design constraint that shapes everything is a GPU L2 number**: 5120 bytes per clock cycle. The 20× replication factor is derived from it, and the entire "parallel Huffman" contribution exists only because a conventional decoder cannot come near it. On a CPU, an L2 sustains tens of bytes per cycle and a sequential Huffman decoder is adequate.
2. **The placement is in the GPU cache hierarchy**: decompressor between L1D and L2, compressor between L2 and HBM. These are GPU structures with GPU-specific sizes and bandwidths.
3. **The block granularity is the GPU cache line and sector** (64 B target, 32 B floor), which is what avoids an indirection table.
4. **The motivating workload behaviour is GPU-specific**: LLM decoding is memory-bound *on a GPU* because the GPU has enormous FLOPs relative to HBM bandwidth. The paper's own GQA limitation proves the point — when the arithmetic intensity rises, the contribution's value collapses.
5. **The 8-way speculative decode is an area-for-latency trade that only pays at GPU bandwidths.** At CPU cache bandwidths you would not spend 8× the decoder area to save cycles.

**Qualification, recorded honestly**: the *algorithm* — group-wise non-uniform quantization with shared k-means patterns and length-limited Huffman — is a data-format idea and would compress equally well anywhere. And the hardware block is not NVIDIA-specific; it would drop into an AMD or Intel GPU. So "GPU-specific" here means *GPU-memory-hierarchy-specific*, not vendor-specific. That is still squarely a NO under this cluster's strict test, because the contribution is not the format — it is a decoder that keeps up with a GPU L2 and sits transparently inside a GPU's cache hierarchy.

verdict_basis: The contribution is a fixed-function compressor/decompressor placed between L1D/L2 and L2/HBM whose entire architecture — 64 parallel decoders, 8-way speculative sub-decoders, a 6-stage merge tree, 20× replication, 64-byte/32-byte block granularity — is dimensioned to the A100 L2's 5120 B/cycle throughput and to GPU cache-line and sector granularity.

## What the throughput is bounded by
**Established, as a design specification rather than a measurement.** The decompressor is required to sustain the **A100 L2's peak 5120 bytes/cycle**, and meets it by replicating a **28-cycle pipelined** decoder **20×**; the compressor (**62 cycles**) is placed off the critical path. The compressor is therefore explicitly *not* the bottleneck — the system stays **HBM-bandwidth-bound**, and Ecco's value is exactly the reduction in HBM bytes (4× for 4-bit weights/KV, 2× for 8-bit activations). The paper's own GQA limitation confirms the bound from the other direction: where GQA converts memory-bound GEMVs into compute-bound GEMMs, the speedup falls away. All of this is simulated (modified Accel-Sim / GPGPU-Sim 4.0, NVBit 1.7.1, stated error within 10%) and synthesised (Synopsys DC, ARM 28 nm scaled to 7 nm); **none of it is measured on hardware**.

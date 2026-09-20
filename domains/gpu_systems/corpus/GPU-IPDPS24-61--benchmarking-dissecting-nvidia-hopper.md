# GPU-IPDPS24-61 — Benchmarking and Dissecting the Nvidia Hopper GPU Architecture

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — GPU core / instruction execution: instruction latency and throughput, matrix-instruction issue scope, inter-SM data paths` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `F — Tensor cores and numeric formats (FP8, sparse mma) — overlaps the tensor-cores cluster; memory-hierarchy characterisation; N — microbenchmark methodology`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` (conference version, arXiv v1) **plus** `FULL_PAPER` of the extended journal version — conference v1 (arXiv 2402.13499): SKU table, p-chase methodology, memory-hierarchy latency/throughput tables, mma and wgmma latency/throughput tables, DPX results, DSM latency/throughput and cluster-size study, Transformer Engine and LLM case studies, limitations, related work. Extended version (arXiv 2501.12084v2): additionally the partitioned-L2 near/far latency analysis and the TMA characterisation. **The two versions are kept distinct throughout — see §12.1.**

## 12.1 Bibliographic facts

- **Title** [paper]: *Benchmarking and Dissecting the Nvidia Hopper GPU Architecture*.
- **Venue** [census]: IPDPS 2024. `ARCHIVAL_MAIN_PAPER`. The arXiv record's comments field carries no venue statement (verified) — venue is from `domains/gpu_systems/census/IPDPS_2024.md`.
- **Authors, conference version** [paper, arXiv 2402.13499v1, submitted 2024-02-21]: Weile Luo, Ruibo Fan, Zeyu Li, Dayou Du, Qiang Wang, Xiaowen Chu.
- **Extended version** [paper, arXiv 2501.12084v2]: *Dissecting the NVIDIA Hopper Architecture through Microbenchmarking and Multiple Level Analysis* — same group **plus Hongyuan Liu**; affiliations HKUST (Guangzhou) and Harbin Institute of Technology, Shenzhen. `PREPRINT` / journal extension.
- **DOI**: `UNKNOWN` for the IPDPS version (`ieeexplore` → 418, not retried).
- **Artifact**: none located. `NOT_INSPECTED`.
- **CORRECTION recorded for this cluster's task assignment**: arXiv `2501.12084` was assigned as the source for *"Dissecting and Modeling the Architecture of Modern GPU Cores"* (MICRO 2025). It is not that paper — it is this group's Hopper extension. The MICRO 2025 paper is analysed at `GPU-MICRO25-61` from the UPCommons PDF.
- **Version-attribution rule used in this file**: numbers are tagged to the version they came from. Mixing them would misattribute the partitioned-L2 and TMA findings, which are in the extension, to the IPDPS 2024 paper.

## 12.2 Core question (one sentence)

What are the measured instruction latencies, throughputs and memory-hierarchy characteristics of Hopper's three genuinely new capabilities — asynchronous warp-group matrix instructions (`wgmma`) with FP8, the DPX instruction set, and distributed shared memory across a thread-block cluster — relative to Ampere and Ada? [paper]

## 12.3 GPU/HPC problem translation

**Compute** and **communication**, established by measurement.

The framing is documentation scarcity: "detailed implementation and performance specifics remain undisclosed in existing literature" [paper], so architects and kernel authors cannot decide when Hopper's new instructions are worth using. The paper's claim to novelty is "the first attempt to demystify the tensor core performance and programming instruction sets unique to Hopper GPUs."

Within this cluster the relevant contributions are: (a) **matrix-instruction issue scope** — `wgmma` is issued by a warp *group* of four warps, a change from warp-scope `mma`; (b) **a new inter-SM data path** — distributed shared memory over the SM-to-SM network; (c) **instruction-level latency/throughput tables** for CUDA-core and matrix instructions.

## 12.4 Why the problem exists (hardware root cause)

[paper] Hopper changes three contracts at once:

1. **Matrix issue becomes warp-group and asynchronous.** `mma` is synchronous, issued per warp. `wgmma` is asynchronous and issued by a warp group of **four warps (128 threads)** on one SM. Operands can come from shared memory (**SS** mode) or from the register file (**RS** mode) — a distinction with measurable consequences.
2. **Shared memory becomes addressable across SMs.** The thread-block **cluster** lets "threads from one thread block to access shared memory of another block", mapped in CUDA C via `cluster.map_shared_rank(SMEM, DST_BLOCK_RANK)`. This creates a communication path that never existed: SM→SM without going through L2.
3. **DPX becomes hardware.** On Ampere and Ada, DPX is software-emulated; on Hopper it has hardware support.

The paper also identifies a root cause that is *not* microarchitectural: **power**. `wgmma` throughput depends on the *contents* of the input matrices, because random data pushes the H800 into its 350 W limit and the clock drops [paper]. This is the finding most likely to invalidate a naive benchmark.

## 12.5 Mathematical / performance model

No analytic model; a measured characterisation. **All numbers are measured on real silicon.**

Devices [paper, conference version, Table III]: **H800 PCIe** (Hopper, CC 9.0, 114 SMs × 128 cores/SM, 80 GB HBM2e); **RTX 4090** (Ada, CC 8.9, 128 SMs × 128 cores/SM, 24 GB GDDR6X); **A100 PCIe** (Ampere, CC 8.0, 108 SMs × 64 cores/SM, 40 GB HBM2e). Software: RTX 4090 on driver 530.30.02 / CUDA 12.1; A100 and H800 on driver 535.104.05 / CUDA 12.2.

Memory-hierarchy latency, clock cycles [paper, conference version, Table IV]:

| Level | RTX 4090 | A100 | H800 |
|---|---|---|---|
| L1 | 43.4 | 37.9 | 40.7 |
| Shared memory | 30.1 | 29.0 | 29.0 |
| L2 | 273.0 | 261.5 | 263.0 |
| Global | 541.5 | 466.3 | 478.8 |

Throughput [paper, conference version, Table V]: L1 `FP32.v4` 121.2 / 106.8 / **124.1** byte/clk/SM; L2 `FP32.v4` 1708.0 / 2007.9 / **3942.4** byte/clk — H800's L2 is 2.6× RTX 4090 and 2.2× A100. L2-to-global bandwidth ratio: 4.67× (RTX 4090), 2.01× (A100), 4.23× (H800).

Matrix instructions, `mma` [paper, conference version, Table VII]:

| Type | A100 | RTX 4090 | H800 |
|---|---|---|---|
| FP16 `m16n8k16` dense | 24.6 cyc / 310.6 TFLOP/s | 24.6 cyc / 357.6 TFLOP/s | 24.1 cyc / 494.4 TFLOP/s |
| FP16 `m16n8k16` sparse | 24.5 cyc / 622.8 TFLOP/s | 24.5 cyc / 711.8 TFLOP/s | 24.0 cyc / 722.8 TFLOP/s |
| INT8 `m16n8k32` dense | 26.0 cyc / 607.6 TOP/s | 24.5 cyc / 711.7 TOP/s | 24.0 cyc / 977.9 TOP/s |

**`mma` on Hopper reaches only an average 62.9% of theoretical peak** [paper].

Matrix instructions, `wgmma` (Hopper only) [paper, conference version, Table VIII], with zero-initialised inputs:

| Instruction | Latency (SS) | Throughput (SS) | Throughput (RS) |
|---|---|---|---|
| FP16 `m64n256k16` | 128.0 cyc | 729.3 TFLOP/s | 729.2 TFLOP/s |
| FP8 `m64n256k32` | 128.0 cyc | 1448.4 TFLOP/s | 1448.0 TFLOP/s |
| INT8 `m64n256k32` | 128.0 cyc | 1448.7 TFLOP/s | 1447.9 TFLOP/s |

**With zero-initialised matrices, `wgmma` exceeds 95% of theoretical peak; with random initialisation it degrades through power throttling at the 350 W limit** [paper]. The 62.9%-vs-95% contrast between `mma` and `wgmma` is the paper's central instruction-selection result.

From the **extended version only** [paper, arXiv 2501.12084v2]:
- `wgmma` latency is 128 cycles for **dense** and **144 cycles in SS mode vs 128 in RS mode** for **sparse**; when `N < 64` throughput falls and SS latency exceeds RS, because "as N decreases, the computational density of `wgmma` instructions gradually diminishes, making it challenging to conceal the latency associated with shared memory access."
- Partitioned L2 on A100/H800: near-partition hit 208 / 258 cycles; far-partition hit 356.6 / 414.1; near-partition miss 474.9 / 555.5; far-partition miss 622.7 / 743.7 (A100 / H800). GPCs are organised into two partitions aligned with the L2 structure.
- TMA: "Ampere's asynchronous copies require all threads to calculate the address of their own memory accesses. However, Hopper's TMA takes care of everything." TMA access is ≈170 cycles higher than a regular access, attributed to TMA-unit overhead and synchronisation waits, despite bypassing L1.
- Power: under continuous `wgmma`, core frequency drops below the 1620 MHz whitepaper figure at the 350 W limit; zero-initialised inputs draw under 200 W while random inputs throttle immediately.

## 12.6 Data layout and ownership

- **thread → warp → warp group**: `mma` is issued per warp (32 threads); `wgmma` per **warp group of four warps on one SM** [paper]. This is the ownership change that makes Hopper's matrix path different from Ampere's.
- **operand source**: SS (shared memory) vs RS (register file) modes for `wgmma`. At large N the two are indistinguishable in throughput; at N < 64 SS is worse [paper, extended version]. So the register file remains the lower-latency operand source when there is not enough arithmetic to hide the shared-memory access.
- **thread block → cluster → GPC**: the cluster is a new level between thread block and grid, mapping to a **GPC**, within which any block can address any other block's shared memory via `cluster.map_shared_rank` [paper].
- **GPC → L2 partition** [paper, extended version]: GPCs are organised into two partitions aligned with the two L2 partitions. *(Compare `GPU-MICRO24-63`, which measures the same partition structure on A100/H100 by an independent method and adds the TPC/CPC levels.)*

## 12.7 Pseudo code

Reconstructed measurement harnesses; PTX mnemonics and the SS/RS mode names are the paper's/NVIDIA's.

```
# --- memory latency: p-chase ---------------------------------------------- [paper]
# L1: load through with the `ca` modifier to populate L1, then chase with one thread
ld.global.ca  r, [p]      ...   # warm L1
t0 = clock(); chase dependent loads; t1 = clock()
# L2: same with the `cg` modifier (bypass L1)
# shared memory: chase within __shared__

# --- mma latency ---------------------------------------------------------- [paper]
# ONE synchronous mma per warp per SM, 1024 repetitions
# "completion latency" = issuance -> result availability
# throughput reported as Total_OPS / Duration, NOT as cycles,
#   deliberately, to avoid clock-frequency variation   <-- important, see power finding

# --- wgmma latency -------------------------------------------------------- [paper]
# ONE asynchronous wgmma per warp GROUP (4 warps) on one SM
# repeat for SS (operands from shared memory) and RS (operands from registers)
# repeat for zero-initialised and random-initialised inputs   <-- power sensitivity

# --- DSM throughput ------------------------------------------------------- [paper]
# ring-based copy across the blocks of a cluster
for cluster_size in {2, 4, ...}:
    each block copies from map_shared_rank(SMEM, (rank+1) % cluster_size)

# --- DPX -------------------------------------------------------------------[paper]
# latency: single-thread dependent iteration
# throughput: block-level, sweeping the number of blocks against the SM count
```

The choice to report matrix throughput as `Total_OPS / Duration` rather than in cycles is methodologically load-bearing: it is what allowed the authors to *see* the power-induced frequency drop instead of being misled by it.

## 12.8 Real implementation

No artifact located; **no `[code]` evidence — do not attribute symbols.**

Methodology is PTX-level microbenchmarks with **SASS disassembly validation** [paper], run on the three real SKUs with the drivers/CUDA versions in §12.5.

## 12.9 Kernel execution

The kernel → cluster → block → warp-group → warp → instruction path on Hopper, as measured:

- A **thread block cluster** is a new scheduling unit mapped to a GPC; its size is a tunable with a real optimum. For a histogram application the best cluster size depends on block size: **CS = 4 for 128-thread blocks, CS = 2 for 512-thread blocks** [paper].
- A **warp group** of 4 warps is the issue unit for `wgmma`.
- **DPX throughput is proportional to the number of blocks while blocks < SM count, peaking when the block count is an integer multiple of the SM count** [paper] — direct evidence that DPX acceleration is per-SM hardware, inferred from the block-count sweep rather than from documentation.
- **INT4 has no Hopper tensor-core path**: "On Hopper, INT4 `mma` instructions are compiled into a series of IMAD instructions, which eventually run on the CUDA cores" [paper]. A silent fallback, discovered by disassembly.

## 12.10 Memory traffic

Latency and bandwidth per level are in §12.5. Two structural results:

- **SM-to-SM network latency is 180 cycles, a 32% reduction versus the L2 cache** [paper]. This is the quantity that justifies distributed shared memory: it is a genuinely new tier between shared memory (29 cycles) and L2 (263 cycles) on H800.
- **DSM ring-copy throughput peaks at ≈3.27 TB/s at cluster size 2, falling to 2.65 TB/s at cluster size 4** [paper]. The trade-off is stated plainly: "As more blocks in the cluster compete for SM-to-SM bandwidth, the overall throughput gets lower… While larger cluster size reduces data movement latency for more blocks, it intensifies throughput competition." **Bigger clusters are not better.**

From the extended version [paper, 2501.12084v2]: TMA costs ≈170 extra cycles relative to a regular access despite bypassing L1, attributed to TMA-unit overhead and synchronisation.

## 12.11 Why it is faster/slower (decomposed cause)

1. **`wgmma` beats `mma` on Hopper for a structural reason**: the wider warp-group instruction with `m64nNk16` shapes (N = 16, 32, 64, 128, 256, …) supplies enough arithmetic per issue to reach >95% of peak, while `mma`'s fixed `m16n8k16`/`m16n8k8` shapes average 62.9%. Instruction *shape*, not the tensor core, is the limiter for `mma`.
2. **Operand source matters only at low arithmetic density**: SS and RS are equal at N ≥ 64 but SS is worse below it, because shared-memory access latency stops being hidden [paper, extended version].
3. **Power is a first-class performance variable.** Zero inputs draw under 200 W; random inputs hit 350 W and drop the clock below the 1620 MHz whitepaper figure [paper, extended version]. **Any Hopper matrix-throughput number reported without stating the input distribution is not reproducible.** This is the single most transferable methodological finding in the paper.
4. **DPX gains come from hardware, not code**: H800 is up to **13×** faster than A100/RTX 4090 on 16-bit DPX operations, whose near-identical A100/RTX 4090 results confirm software emulation on both [paper].
5. **The application-level gains are smaller than the instruction-level ones**, and the paper says why. For `te.Linear` at small matrix sizes the FP8 *conversion* overhead exceeds the GEMM itself; FP8 only beats FP16 in `te.TransformerLayer` when hidden size > 4096, and never reaches 2× because Softmax/GeLU are not quantised and flash-attention is in use. For decode-only LLM inference (Llama-3B, Llama-2-7B/13B, input 128 / output 128 / batch 8) the model is **memory-bound**, "so the computational advantages of FP8 Tensor Cores are not significant" [paper]. On llama-3B, H800 FP32 reaches 679.45 tok/s versus BF16's 624.10 — **FP32 beats BF16**, which only makes sense under a memory-bound regime.

## 12.12 Hardware generation dependence

- **Measured on real silicon**: H800 PCIe (Hopper), RTX 4090 (Ada), A100 PCIe (Ampere). No simulation anywhere.
- **H800, not H100.** The H800 is the export-restricted Hopper variant; its interconnect and some throughput characteristics differ from H100. Do not restate these numbers as H100 numbers.
- Hopper-only features characterised: `wgmma`, FP8 tensor cores, DPX hardware, thread block clusters and distributed shared memory, TMA (extension only), partitioned L2 (extension; A100 also partitioned).
- **Blackwell is entirely out of scope.** `tcgen05`, TMEM and 5th-generation tensor cores do not appear. See `GPU-IPDPS26-61` for the Blackwell counterpart; that paper's B200/H200 results and this paper's H800 results are different products and must not be merged.
- Ada (RTX 4090) appears only as a comparison point and has no DSM, no `wgmma` and no DPX hardware.

## 12.13 Limitations

Stated [paper]:
- **LLM workloads use short sequences** (input 128, output 128, batch 8); longer sequences would change the memory-boundedness conclusion.
- **Power throttling limits generalisability** of the `wgmma` random-initialisation results.
- **Sparse `mma` underutilises the sparse tensor cores** on Hopper.
- **Transformer Engine coverage is incomplete** — no optimal support for mainstream decode-only causal language models, and Softmax/GeLU are unquantised.
- **INT4 has no tensor-core path** on Hopper (falls back to IMAD on CUDA cores).
- **DSM analysis rests on a single application pattern** (histogram); generalisation to other SM-to-SM communication patterns is unclear.

`[inference]`, not stated: the memory-hierarchy latencies are p-chase single-thread figures at zero contention, i.e. floors. The DSM 180-cycle figure and the 3.27 TB/s peak are likewise measured with a specific ring pattern; other patterns would contend differently, which the paper itself flags.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Hopper GPU Architecture" returns `domains/gpu_systems/census/IPDPS_2024.md` and an incidental hit in `_LEDGER_profiling_reliability.md`.
- **Direct generational predecessor of** `GPU-IPDPS26-61` (Microbenchmarking NVIDIA's Blackwell Architecture, IPDPS 2026). Same venue, same method, two years apart. The matrix-issue-scope story runs continuously through them: warp-scope `mma` (Ampere/Ada) → **warp-group** `wgmma` (Hopper, 128 cycles at `m64n256k16`) → back to **warp-scope** `tcgen05.mma` (Blackwell B200, 11.4 cycles at `m256n256k16`). **The issue unit widened and then narrowed again in two generations** — a lineage only visible by reading the two IPDPS papers together.
- **Independent corroboration**: `GPU-MICRO24-63` (Jin et al., real GPU NoC) measures the same A100/H100 L2-partition structure by an entirely different method (SM pinning + correlation clustering rather than p-chase), and adds the TPC/GPC/CPC hierarchy. The extended version's near/far L2 latencies and MICRO'24's ~200-vs-~400-cycle partition figures agree in structure. **Two independent 2024 papers converge on partitioned-L2 non-uniformity as a first-class Hopper/Ampere property.**
- **Cited by** `GPU-MICRO25-61`, whose related work lists "Shoushtary et al. (2024) — Hopper DPX" alongside this line of dissection work [paper, MICRO'25 related work].
- **Complementary within the tensor-cores cluster**: `GPU-PPoPP26-02` (Cubie) characterises matrix units across A100/H200/B200 at the *kernel-pattern* level; `GPU-SC26-02` (EmuGEMM) uses `wgmma.mma_async` at SM90 in anger. This paper supplies the measured instruction latency/throughput both rely on.
- **Precursors cited** [paper]: Jia et al. and Yan et al. (Volta/Turing dissection), Markidis et al. and Martineau et al. (WMMA API limitations), Fasi et al. and Sun et al. (SASS-level low-precision numeric behaviour). The paper positions itself as extending Sun et al.'s `mma`/`mma.sp` analysis from Ampere/Turing to Hopper.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The measured quantities are defined by SIMT structure at every level. (a) `wgmma` is characterised **per warp group of four warps on one SM**, and the SS-vs-RS comparison is a statement about whether operands come from shared memory or from the per-warp **register file** — both concepts require warps. (b) The **thread block cluster** and **distributed shared memory** are the paper's newest object: the 180-cycle SM-to-SM latency and the cluster-size trade-off (3.27 TB/s at CS=2 falling to 2.65 TB/s at CS=4) describe a network between **streaming multiprocessors** sharing **scratchpad** address space, which exists on no other machine. (c) The DPX conclusion — that acceleration is per-SM — is derived from throughput being proportional to **block count up to the SM count** and peaking at integer multiples of it, a purely GPU occupancy argument. (d) The memory hierarchy measured is L1 / **shared memory** / L2 / global with an `%smid`-free p-chase using the CUDA `ca`/`cg` cache modifiers. (e) Even the power finding is GPU-specific: a 350 W part whose clock drops under sustained matrix issue is a throughput-processor phenomenon. Nothing here survives translation to a CPU or a generic accelerator.

verdict: `CORE_GPU`

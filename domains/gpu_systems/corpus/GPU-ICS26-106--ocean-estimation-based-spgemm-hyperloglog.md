# GPU-ICS26-106 — Ocean: Fast Estimation-Based Sparse General Matrix-Matrix Multiplication on GPU

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT` (both read)
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `G — Sparse/irregular GPU kernels (SpGEMM, output-size estimation, accumulator design)`
secondary_topics: `probabilistic sketching (HyperLogLog) on GPU; shared-memory vs global-memory atomics; device-side allocation for unpredictable output size; binning/load balancing`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2604.19004v1) — abstract, introduction and the 28%-symbolic-cost motivation, the HyperLogLog construct-and-merge design and precision configuration, the cost-prediction step (expansion ratio / compression ratio / Table 1 workflow selection), the hybrid accumulator taxonomy, the split hash-table design and its atomics argument, the binning strategy, Gustavson mapping, overflow fallback, evaluation setup (Perlmutter A100 + DeltaAI H100), matrix suites, all baselines, headline numbers, the V1-V4 ablation, memory-overhead result, stated limitations and future work, related work. PLUS ARTIFACT CODE READ (see 12.8).`

## 12.1 Bibliographic facts

- Title: **Ocean: Fast Estimation-Based Sparse General Matrix-Matrix Multiplication on GPU** [paper] (rendered "OCEAN" in the arXiv HTML body)
- Venue: **ICS 2026** ("Proceedings of the 40th ACM International Conference on Supercomputing"), session `S20 Sparse & Tensor Kernels` [census: `domains/gpu_systems/census/ICS_2026.md`]. DOI **`10.1145/3797905.3807868`** [official-web, from the search result's canonical `doi.org` link].
- Authors [paper]: **Yifan Li** and **Giulia Guidi**, **Cornell University, Ithaca, NY, USA**. (The census row recorded "Y. Li, G. Guidi" — confirmed.)
- Publication type: `ARCHIVAL_MAIN_PAPER`; arXiv 2604.19004 is a `PREPRINT` of the same work.
- Full text used: `https://arxiv.org/html/2604.19004v1` [paper].
- Artifact: **`https://github.com/CornellHPC/Ocean-SpGEMM`** [paper, stated in the text]. **INSPECTED**, pinned at commit **`cb093963f6e45d9deabf7848bc05a538af796315`** [code].

## 12.2 Core question (one sentence)

GPU SpGEMM has for a decade paid an exact **symbolic pass** to learn each output row's non-zero count before allocating an accumulator — so what if that pass is replaced by a **probabilistic cardinality estimate (HyperLogLog)** that is wrong ~10% of the time, with a fallback kernel to catch the rows where the estimate was too small?

## 12.3 GPU/HPC problem translation

- **Compute.** The symbolic pass is pure overhead by construction: it produces "only one value per output row" yet "takes an average of **28%** of the total runtime in spECK" [paper]. Removing it is the entire thesis.
- **Memory.** Two distinct memory problems. (a) **Allocation**: the output size is unknown before execution, and "allocating the exact scratchpad memory needed for each row is impractical in GPU programming", so implementations "predefine multiple kernel configurations with fixed scratchpad sizes" [paper]. (b) **Placement**: where the hash table's indices and values live.
- **Synchronization.** The paper's sharpest hardware observation: "atomic operations on shared memory for FP64 data types are not natively supported on NVIDIA GPUs and are compiled into compare-and-swap loops", whereas global atomics are "fire-and-forget hardware instructions" [paper]. This inverts the usual shared-memory-is-always-better intuition and is the basis of the split hash table.
- **Load imbalance.** Handled by **binning**: rows are assigned pre-launch to kernel configurations by estimated size, with configurations "progress[ing] geometrically: each uses half the resources of the previous", picking "the configuration that requires the fewest resources for a given row" [paper]. Residual balancing is delegated to the hardware block scheduler.
- **Communication.** Single GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- An SpGEMM accumulator must be **sized before the kernel launches**, because shared memory is allocated per block at launch and is capped at ~96–128 KB per SM [paper]. On a CPU one would simply `realloc`. The symbolic pass exists purely to satisfy that GPU constraint.
- HyperLogLog is chosen not for statistical elegance but for three *hardware* reasons the paper states [paper]: constant memory regardless of non-zero count; bounded error at a small register count; and — decisively — "sketch updates avoid compare-and-swap operations and can be implemented using **`atomicMax`**". A sketch update that is a single hardware atomic, not a CAS loop, is what makes the estimate cheaper than the thing it replaces.
- Merging is free in the same sense: "Combining multiple HLL sketches only requires taking the element-wise maximum across corresponding registers, provided the same hash function is used" [paper]. So a row of `C` is estimated by `atomicMax`-merging the sketches of the `B` rows that row of `A` touches — a *reduction*, which GPUs do well, replacing a *set union with deduplication*, which they do badly.
- The FP64 shared-atomic gap is a real microarchitectural fact and the paper exploits it directly.

## 12.5 Mathematical / performance model

- **Symbolic cost being removed** [paper]: **28% of total runtime on average in spECK**.
- **HLL precision** [paper]: **32 registers per sketch when input expansion ratio < 48, else 64**. Measured relative error ≈ **0.13 / 0.10 / 0.07** for 32 / 64 / 128 registers.
- **Workflow-selection rule** [paper, Table 1]:
  - average intermediate products **< 64** → **upper-bound estimation**
  - **ER ≥ 8 AND sampled CR ≥ 8** → **HLL estimation**
  - otherwise → **exact symbolic**
  where **ER** = intermediate products / nnz(A), **CR** = intermediate products / nnz(C). Symbolic is preferred when ER falls below ¼ of the register count.
- **Sampling cost** [paper]: HLL sketch construction is `O(nnz_B)`; only **3% of A's rows** are sampled for CR; the analysis step costs **~3%** of runtime (reported as 7% total analysis overhead with 2% HLL sampling in the ablation section — the paper gives both framings; both are recorded, neither is reconciled here).
- **Overflow rate** [paper]: **0.3%–1.2% of rows**, depending on register count — i.e. the probabilistic bet loses about one time in a hundred and the fallback kernel pays for it.

## 12.6 Data layout and ownership

- **thread / warp**: Gustavson's algorithm — "The outer loop traverses the nonzeros in the corresponding row of A, and the inner loop traverses the row of B associated with each of these nonzeros" [paper]. Threads within a block collaboratively insert into the accumulator.
- **block**: "Thread blocks are typically assigned one output row each" [paper]. The HLL construction kernel is **limited to 32 threads (1 warp) per block**, with the code carrying the author's own caveat "May not be the best efficiency" [code: `kernels/HLL.cuh`].
- **shared memory**: holds the accumulator **indices**. Confirmed in code: `struct SymbolicHashmap` carries the member **`ids_shared`** [code: `kernels/Hashmap.cuh:128-130`].
- **global memory**: holds the accumulator **values**. This is the split hash-table contribution, justified by "The indices serve as element identifiers and must be read, compared, and swapped using atomic operations during insertion, while values are only involved in `atomicAdd` operations" [paper]. Claimed benefit: rows "3× longer" can be handled [paper].
- **accumulator types**, three, each with several fixed configurations [paper]: **hash** (medium rows), **dense** (narrow column-index range), **ESC — Expand–Sort–Compact** (very short rows). All three exist as separate files in the artifact [code: `kernels/AccumulatorHash.cuh`, `AccumulatorDense.cuh`, `AccumulatorESC.cuh`].
- **GPU**: NVIDIA A100 40 GB (Perlmutter) and NVIDIA H100 96 GB (NCSA DeltaAI) [paper].
- **node/cluster**: single GPU per measurement. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- phase 0: analysis (~3% of runtime) ---                      [paper] Table 1
ER = intermediate_products / nnz(A)
sample 3% of A's rows; merge their HLL sketches -> sampled CR
if avg_intermediate_products < 64:  workflow = UPPER_BOUND
elif ER >= 8 and sampled_CR >= 8:   workflow = HLL
else:                               workflow = SYMBOLIC   # the classic exact pass

# --- phase 1 (HLL workflow): construct one sketch per row of B --- [code] HLL.cuh
hllConstruct<logPrecision>(B):                 # 1 warp per block
    idx  = hashed_value & ((1<<logPrecision)-1)
    item = __clz(hashed_value) + 1             # leading-zero rank
    atomicMax(&scratch[idx], item)             # NO compare-and-swap

# --- phase 2: estimate each row of C by merging B's sketches ---  [paper]
est[i] = hll_estimate( elementwise_max over { sketch[k] : k in cols(A[i,:]) } )

# --- phase 3: bin rows to kernel configurations ---               [paper]
#   configurations halve resources geometrically; pick the smallest that fits est[i]

# --- phase 4: numeric, split hash table ---                       [code] Hashmap.cuh
#   ids in shared memory, values in global memory
old = atomicCAS(ids + map_id, HASH_UNUSED, id)     # linear probing
atomicAdd(values + map_id, a_value * b_value)      # fire-and-forget global atomic

# --- phase 5: overflow fallback + compaction ---                  [paper]
#   one extra kernel, largest dense configuration, handles arbitrarily long rows
#   then compact into contiguous CSR
```

`hllConstruct`, `hllAdd`, `atomicMax`, `__clz`, `atomicCAS`, `HASH_UNUSED`, `ids_shared`, `SymbolicHashmap`, `NumericHashmap` are **real symbols read from the artifact** [code]. `est`, `hll_estimate`, the phase numbering and the binning loop are `[reconstruction]` presentation of the paper's prose.

## 12.8 Real implementation

**INSPECTED.** Repository `https://github.com/CornellHPC/Ocean-SpGEMM`, pinned at commit **`cb093963f6e45d9deabf7848bc05a538af796315`** [code].

Files present [code]: `src/main.cu`; `kernels/{HLL.cuh, MurmurHash.cuh, Hashmap.cuh, AccumulatorHash.cuh, AccumulatorDense.cuh, AccumulatorESC.cuh, AccumulatorCommon.cuh, Analysis.cuh, Epilogue.cuh, SpGEMM.cuh, Wrappers.cuh, DeviceCommon.cuh}`; `include/{Common.h, CSR.h, Utils.h, Json.hpp}`.

Symbols and facts verified against the source, not inferred:
- **`hllAdd`** [code: `kernels/HLL.cuh`] computes `idx = hashed_value & mask`, `item = __clz(hashed_value) + 1`, clamps `item` to `(32 - logPrecision) + 1`, then `atomicMax(&scratch[idx], item)`. **Confirms the paper's claim that sketch updates need no CAS.**
- The scratch array is `uint32_t` with an explicit in-source reason: *"uint32_t is used for scratch because CUDA does not support atomic operations on uint8_t."* [code: `kernels/HLL.cuh`, comment]. This is an *additional* GPU-atomics constraint the paper does not state — the sketch registers are 4× wider than HyperLogLog needs, purely because of the atomic-width rule.
- **`hllConstruct`** is `__global__`, templated on `logPrecision`, and carries the in-source comment *"This kernel is limited to 32 threads (1 warp) per block. May not be the best efficiency"* [code].
- Hash map structs [code: `kernels/Hashmap.cuh`]: **`NumericHashmap`** (members `ids`, `values`, `occupancy`), **`WarpNumericHashmap`**, **`SymbolicHashmap`** (member **`ids_shared`**), **`WarpSymbolicHashmap`**, **`FlexSymbolicHashmap`**. Insertion is open addressing with linear probing via `atomicCAS(ids + map_id, HASH_UNUSED, id)`; accumulation via `atomicAdd(values + map_id, val)`.
- The hash function in use is trivial — `hashKernel(id) { return id * 11; }` — with an in-source note *"can change to murmurhash"* [code: `kernels/Hashmap.cuh`], even though `MurmurHash.cuh` exists in the tree. **The paper's text does not disclose which hash the numeric accumulator uses**; the code says the simple multiplicative one is the default path.
- Warp-level primitives present: `__shfl_down_sync(0xffffffff, …)` and `__shfl_up_sync` for reductions and scans [code: `kernels/AccumulatorDense.cuh`], plus `__syncwarp()` with the in-source comment *"This should not be necessary without independent thread scheduling"* [code] — a Volta+ ITS dependence stated in the source and **not** in the paper.
- Overflow bookkeeping is device-side: `atomicAdd(out_num_overflow_rows, 1)` and `atomicAdd(out_overflow_buffer_allocated, add_num)` [code: `kernels/AccumulatorDense.cuh`], i.e. the fallback list is built on the device without host involvement.
- **NOT verified**: no `cp.async` / `memcpy_async` / TMA use was found in `kernels/` [code — targeted grep returned none]. Recorded as an absence in the inspected tree, not as a claim about the paper.

## 12.9 Kernel execution

kernel → block (usually one output row; one warp for `hllConstruct`) → warp (shuffle-based reductions/scans) → atomic instruction. The interesting execution property is that **the kernel launch configuration is itself the output of a probabilistic estimate**. Binning is a pre-launch decision made from `est[i]`, so an estimation error is not a numerical error but a *resource* error, repaired by a second kernel. The design converts an accuracy problem into a scheduling problem — which is only a good trade because the GPU cannot resize shared memory mid-kernel.

## 12.10 Memory traffic

- **Symbolic-pass traffic eliminated** on the HLL path: the exact pass re-reads all of `A` and `B`'s index structure. HLL replaces that with `O(nnz_B)` sketch construction plus a per-row merge [paper].
- **Split placement**: indices in shared memory (CAS-heavy, latency-critical), values in global memory (`atomicAdd`-only, fire-and-forget) [paper, confirmed by `ids_shared` in `SymbolicHashmap` and `values` in `NumericHashmap` — code].
- **Cost of the trade**: peak GPU memory **≈2.2×**, because output allocation is non-consecutive and needs a compaction pass; **one matrix (`JP`) failed on A100 for this reason** [paper]. This is a genuine, reported failure.
- No L1/L2/HBM counter breakdown. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Setup, all qualifiers carried** [paper]: **NERSC Perlmutter** — AMD EPYC 7763, 4× **NVIDIA A100 40 GB**, SUSE Linux, **CUDA 12.9**; **NCSA DeltaAI** — ARM host, 4× **NVIDIA H100 96 GB**, SUSE Linux, **CUDA 12.4**. Matrix suite: **SuiteSparse**, **337 square matrices** (≥100M FLOPs for `A·A` or `A·Aᵀ`) and **64 rectangular** (≤10B non-zeros, ≥100M FLOPs for `A·Aᵀ`).

Baselines [paper]: **cuSPARSE** (version `NOT_IN_PAPER`), **spECK**, **OpSparse**, **TileSpGEMM**, **HSMU-SpGEMM**. **MOSparse excluded — not open source** [paper].

Results [paper]:
- **A100, 337 square matrices**: geometric-mean **1.4× over spECK, 2.6× over OpSparse, 3.5× over TileSpGEMM, 2.0× over HSMU-SpGEMM**; best on **86%** of matrices; **63.23 GFLOP/s** mean vs spECK's **46.2 GFLOP/s**.
- **H100**: **1.6× over spECK** on square matrices.
- **Negative case reported**: `torso1` at **0.55×** — a 45% slowdown, disclosed.

Ablation V1→V4 [paper]:
- **V2 estimation-based workflow**: **1.30×** (on selected matrices) — the dominant cause, and it is exactly the 28% symbolic pass being removed.
- **V3 assisted kernels**: +1.04×
- **V4 hybrid accumulators**: +1.06×
- **Overall V1→V4: 1.25×**

The honest reading: the *headline* 1.4× over spECK and the *ablation* 1.25× end-to-end are consistent with a mechanism whose ceiling is the 28% symbolic share. The paper does not oversell beyond its own measured bound.

## 12.12 Hardware generation dependence

- **Two generations, A100 and H100, with different CUDA versions (12.9 / 12.4)** [paper] — better than single-SKU papers in this cluster.
- The central hardware dependence is **not** generational but **datatype-specific**: the FP64 shared-memory-atomic gap. If a future GPU adds native FP64 shared atomics, the split hash table's justification weakens. The paper's own framing ("global atomic latency is only 2–4× higher than shared in general" [paper]) makes the design a *ratio* bet, not an absolute one.
- Code-level: `__syncwarp()` with the comment about independent thread scheduling ties the implementation to Volta-and-later semantics [code].
- No MMA / Tensor Core anywhere. This is a **CUDA-core, atomics-and-scheduling** paper.

## 12.13 Limitations

Stated by the paper [paper]:
1. **Memory overhead ~2.2× peak** on constrained devices; matrix `JP` failed on A100. Suggested future fix: symbolic-fallback detection.
2. **Robustness on throughput-bound cases** — `torso1` at 0.55×.
3. Fine-grained kernel performance prediction is future work.
4. Extension to other sparse primitives is future work.

Visible from the code but not stated in the paper [code, flagged as such]:
5. The HLL construction kernel runs at **one warp per block**, with the author's own "may not be the best efficiency" comment — so the estimation path itself is not fully optimised.
6. The numeric hash uses `id * 11`, not MurmurHash, despite `MurmurHash.cuh` being present. Collision behaviour under adversarial column-index distributions is therefore not what the paper's "same hash function" framing might suggest for the *accumulator* (the framing applies to the *sketches*).

## 12.14 Relation to prior corpus

- **Competing with** `HSMU-SpGEMM` (HPCA 2025), which is a verdict-only paper in this same cluster ledger and is one of Ocean's baselines (Ocean 2.0× faster, 337 square SuiteSparse matrices, A100). Ocean is therefore direct external evidence that HSMU-SpGEMM is a real, current SpGEMM baseline.
- **Orthogonal to the Tensor-Core sparse line** (`GPU-PPoPP25-01` FlashSparse, `GPU-PPoPP25-02` Acc-SpMM, `GPU-SC24-102` SMaT, `GPU-ASPLOS26-101` Insum): those are all SpMM (sparse × *dense*) on the matrix unit. Ocean is SpGEMM (sparse × *sparse*), where the output pattern is unknown and no matrix unit helps. **The two problems have diverged mechanically**: SpMM has become a matrix-unit-and-format problem, SpGEMM has stayed an atomics-allocation-and-scheduling problem. That divergence is one of this cluster's main findings.
- **Complementary to** `GPU-PPoPP26-104` (Trojan Horse) and `GPU-PPoPP26-105` (DiggerBees): all three address device-side handling of work whose size is not known in advance.
- `NO_EXISTING_ANALYSIS`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The problem being solved exists only because **shared memory is allocated per block at kernel launch and cannot be resized**, which is why an exact symbolic pass was ever necessary; on a CPU one reallocates and the 28% disappears. The *solution* is chosen for two named GPU properties: (i) HLL sketch updates are a single **`atomicMax`** rather than a CAS loop, so the estimate is cheaper than the exact count — and the artifact shows the sketch is widened to `uint32_t` purely because *"CUDA does not support atomic operations on uint8_t"* [code]; (ii) the split hash table places indices in shared memory and values in global memory because **FP64 shared-memory atomics are emulated as CAS loops on NVIDIA GPUs while global atomics are hardware fire-and-forget** [paper]. Both are statements about a specific memory system's atomic implementation and have no CPU analogue.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Compute — claimed and established.** The 28% symbolic share is measured in spECK and the V2 ablation step (1.30×) recovers close to its bound.
- **Synchronisation — claimed and established.** The CAS-loop-vs-hardware-atomic argument drives both the HLL choice and the split hash table; the code confirms `atomicMax` / `atomicCAS` / `atomicAdd` usage exactly as described.
- **Memory — claimed and PARTIALLY ESTABLISHED, with a reported cost.** The accumulator placement is a memory-system argument, but the workflow *costs* 2.2× peak memory and loses one matrix. The paper is candid about this.
- **Load imbalance — claimed, weakly established.** Geometric binning by estimated size plus reliance on the hardware block scheduler; no imbalance metric is reported. `NOT_IN_PAPER`.
- **Dependency — not applicable.**

verdict: `CORE_GPU`

# GPU-ASPLOS24-01 — GMLake: Efficient and Transparent GPU Memory Defragmentation for Large-scale DNN Training with Virtual Memory Stitching

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `D — GPU virtual memory management (device-side virtual/physical decoupling, allocator-level defragmentation)` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `LLM/DNN training memory systems; CUDA driver VMM API semantics`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation with Observations 1-3; background (PyTorch best-fit-with-coalescing caching allocator, splitting/merging, CUDA low-level VMM API set, Table 1 VMM overhead breakdown); design (virtual memory stitching, pPool/pBlock and sPool/sBlock, Algorithm 1's four allocation states S1-S4, Alloc/Split/Stitch/BestFit/StitchFree, fragmentation limit, LRU GC, convergence argument); implementation (LoC, PyTorch integration, transparency); evaluation setup; results incl. per-model and scaling figures; VMM overhead amortization (Fig. 14 convergence); author-stated limitations; related work. Read via two targeted full-text passes over arXiv HTML v1.`

## 12.1 Bibliographic facts

- Title: *GMLake: Efficient and Transparent GPU Memory Defragmentation for Large-scale DNN Training with Virtual Memory Stitching* `[paper]`
- Authors: Cong Guo, Rui Zhang, Jiale Xu, Jingwen Leng, Zihan Liu, Ziyu Huang, Minyi Guo, Hao Wu, Shouren Zhao, Junping Zhao, Ke Zhang `[paper]` — per-author affiliations were not resolvable from the arXiv abstract page (`UNKNOWN`); the artifact is hosted under Ant Group's `glake` repository `[README/official-web]`.
- Venue: ASPLOS 2024 (29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems), Volume 2, Session 8B "Memory: Address Translation and Tiering" `[official-program, via census/ASPLOS_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER` (analysed from the `PREPRINT` arXiv v1; see note below)
- DOI: `10.1145/3620665.3640423` `[publisher-proceedings, via census/ASPLOS_2024.md]`
- Full text used: https://arxiv.org/html/2401.08156v1 — **v1 only exists**, submitted 16 January 2024. `[paper]` Because only the preprint was reachable (`dl.acm.org` returns 403 here), all claims below are from the preprint; where the camera-ready differs this analysis cannot detect it. Evidence class for text is therefore `[paper]` at `PREPRINT` fidelity.
- Artifact/code: https://github.com/intelligent-machine-learning/glake (GMLake subdirectory) `[official-web/README, per the arXiv page]`. **NOT cloned or inspected in this pass** → all code-level detail is `NOT_INSPECTED`; the API names below are the paper's own citations of the CUDA driver API, not symbols read from the repository.

## 12.2 Core question (one sentence)

PyTorch's caching allocator defragments by *splitting and coalescing physically contiguous blocks*, which fails when memory-reduction techniques make allocation sizes irregular — so can the CUDA low-level virtual-memory-management API be used to give a tensor one contiguous *virtual* range backed by several non-contiguous *physical* chunks, cheaply enough to be on by default? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** The entire contribution. The resource is GPU HBM capacity lost to fragmentation, and the lever is the virtual→physical mapping. `[paper]`
- **Compute.** Only as a constraint: the mechanism must not cost throughput. The paper's blocking observation is that bypassing the caching allocator and calling the native allocator directly gives "9.7× lower throughput than the original PyTorch allocator." `[paper]`
- **Communication.** Indirect but load-bearing: distributed training is what *creates* the irregularity. For OPT-13B, memory utilisation "declines to 76%" at 16 GPUs, from above 90% on a single GPU. `[paper]`
- **Scheduling.** Exploited, not changed: the design's amortisation argument rests on DNN training's *iteration periodicity*.
- **Synchronization.** `NOT_IN_PAPER` as a first-order concern.

## 12.4 Why the problem exists (hardware root cause)

1. **A caching allocator exists because the native GPU allocator is slow.** Frameworks cache device memory to avoid native API calls; the measured penalty for not caching is 9.7× throughput. `[paper]` So the allocator cannot simply free and re-allocate to defragment.
2. **The caching allocator's only defragmentation tool is physical contiguity.** PyTorch uses best-fit-with-coalescing: best-fit search, *splitting* an oversized block into two bidirectionally linked blocks, marking blocks inactive on free without calling the GPU, and *merging* adjacent inactive blocks. `[paper]` Both splitting and merging require the blocks to be *adjacent in the physical allocation*, so a request larger than any single free block fails even when total free bytes suffice: "the memory pool cannot hold Block 6 because the size of Block 6 is larger than Block 5, which cannot be exploited and becomes fragmented." `[paper]`
3. **Memory-reduction techniques destroy allocation regularity.** Observation 1: recomputation, offloading, distributed partitioning and LoRA "directly correlate with increased fragmentation." Quantified: GPT-NeoX-20B with these optimisations shows "76 thousand allocations with 85 MB on average" versus a baseline "46 thousand allocations with 93 MB on average" — more allocations, smaller and more varied. `[paper]` Regular transformer training (same-shaped layers) is exactly the case best-fit-with-coalescing handles well, which is why the problem only appeared with the optimisation stack.
4. **Observation 2: GPU scaling amplifies it** — utilisation falls from >90% (1 GPU) to 76% (16 GPUs) for OPT-13B. `[paper]`
5. **Observation 3: the obvious fix is prohibitively expensive as-is.** CUDA's low-level VMM API can map non-contiguous physical chunks into one virtual range, but at 2 MB chunk granularity a 2 GB allocation costs **115.4×** native `cuMalloc`, decomposed as `cuMemCreate` **18.1×** and `cuMemSetAccess` **96.8×**. `[paper]` The root cause of the design is therefore not "can virtual memory help" but "how is `cuMemSetAccess` amortised."

The hardware-level fact underneath all of this: the GPU MMU can map a contiguous virtual range onto scattered physical chunks at the 2 MB granularity the VMM API exposes, and *multiple* virtual mappings to the same physical chunk are permitted — which is what makes stitching without unmapping possible. `[paper]`

## 12.5 Mathematical / performance model

No analytic model. The quantitative structure is a cost table plus an amortisation argument.

**Cost (Table 1, 2 GB allocation)** `[paper]`:

| API | at 2 MB chunks | at larger chunks |
|---|---|---|
| `cuMemCreate` | 18.1× native `cuMalloc` | 0.89× at 128 MB chunks |
| `cuMemSetAccess` | 96.8× | 0.7× at 1024 MB chunks |
| **total** | **115.4×** | — |

*(The fetched summary also reported a "~1.5× overhead" figure for 2 MB chunks; that reading is inconsistent with the 115.4× total and is **not asserted here** — `UNKNOWN`.)*

**Amortisation argument** `[paper]`: "each iteration processes identical model parameters and input data sizes. Therefore, after a few iterations, GMLake will no longer execute [S2, S3, S4]. GMLake will only utilize the exact match strategy for the remainder of the training." Freed sBlocks are retained rather than destroyed: "When the sBlock is freed, we still keep it presence. Next time when the same sBlock needs to be created, it can directly reuse the previously created sBlock." Convergence is measured at **four iterations** (Figure 14). `[paper]`

**Policy constants** `[paper]`: uniform **2 MB** physical chunk granularity; allocations **< 2 MB** fall back to PyTorch's native splitting (stated to be rare in LLMs); **fragmentation limit of 128 MB** as the minimum block size for stitching/splitting; LRU garbage collection (`StitchFree`) releasing least-recently-used sBlocks when the sPool exceeds a threshold — the threshold value itself is `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

Two-tier pool `[paper]`:

- **pPool / pBlock — physical ownership.** "The pBlock, serving as the primitive block, represents the smallest unit accessible to high-level tensors." pPool is "a sorted set to store the pBlocks," sorted by size descending. A pBlock owns actual GPU physical chunks at 2 MB granularity.
- **sPool / sBlock — virtual ownership.** "The stitched block structure … integrates multiple pBlocks." An sBlock "remaps virtual memory to all physical chunks of the pointed pBlocks." A single pBlock may be referenced by *multiple* sBlocks, i.e. soft-link semantics rather than exclusive ownership. Activity propagates upward: "if even one pBlock is active, all corresponding sBlocks are labeled as active." `[paper]`

Mapped onto the template's hierarchy:
- **thread → warp → block → SM:** untouched; GMLake operates entirely above the kernel.
- **GPU:** the allocator's scope. One GPU's HBM, one virtual address space, one pPool/sPool pair. `[inference]` — the paper does not describe cross-GPU pool sharing.
- **node / cluster:** 8× A100-80 GB per node over NVLink; multi-node is two such servers over RDMA. `[paper]` GMLake's relevance to these tiers is that DeepSpeed/FSDP/Colossal-AI partitioning is what generates the irregular allocations; GMLake itself is per-GPU.

The critical ownership subtlety: **the virtual address is the unit handed to the tensor, and it is decoupled from physical ownership.** A tensor's contiguity requirement is satisfied in the virtual address space only. `[paper]`

## 12.7 Pseudo code

State names S1–S4, function names `Alloc`/`Split`/`Stitch`/`BestFit`/`StitchFree`, the pools and the CUDA API names are `[paper]`; statement-level shape is `[reconstruction]` of Algorithm 1 as described.

```
allocate(size):                                        # Algorithm 1  [paper]
  state, cands = BestFit(sPool, pPool, size)           # [paper]

  if state == S1:      # exact match                    [paper]
      return cands[0]  # the only state that allocates an sBlock  [paper]

  elif state == S2:    # single pBlock larger than size  [paper]
      p_lo, p_hi = Split(cands[0], size)               # [paper]
      s = Stitch([p_hi, another_pBlock])               # remainder is stitched  [paper]
      sPool.insert(s)
      return p_lo

  elif state == S3:    # multiple pBlocks               [paper]
      chosen = greedy_collect(cands, size)             # [paper]
      if last(chosen) oversized: Split(last(chosen))   # [paper]
      s = Stitch(chosen)                               # cuMemMap each chunk into one VA  [paper]
      sPool.insert(s)
      return s

  else:                # S4: insufficient blocks        [paper]
      p_new = Alloc(size)   # cuMemAddressReserve + cuMemCreate + cuMemMap + cuMemSetAccess  [paper]
      pPool.insert(p_new)
      optionally Stitch(p_new with remaining fragments) # [paper]
      return p_new

free(block):                                            # [paper]
  mark inactive ; keep sBlock resident in sPool         # [paper] -> enables S1 reuse
  if sPool_capacity > threshold: StitchFree()            # LRU eviction of sBlocks  [paper]
```

`Stitch` is the mechanism proper: it "can stitch together multiple pBlocks into a single sBlock," using `cuMemMap` **without unmapping the originals**, because multiple virtual→physical mappings to the same chunk are allowed. `[paper]` `Split` differs from PyTorch's split in kind, not degree: it "divides pBlock into two new pBlocks with remapped physical chunks," whereas BFC splits a contiguous region. `[paper]`

## 12.8 Real implementation

- **~5,000 lines of C++**, integrated into PyTorch's caching allocator, for **PyTorch 1.13.1 and 2.0**. `[paper]`
- Integration point: "We implement the GMLake on the low level of the DL framework and replace the original memory allocation API of DNN training." `[paper]`
- Transparency: "completely transparent to the DNN models and memory reduction techniques"; user code needs no modification. `[paper]`
- CUDA driver API functions the paper names: `cuMemAddressReserve` ("reserves a virtual memory address for the new memory allocation"), `cuMemCreate` ("allocates physical memory chunks on GPU"), `cuMemMap` ("maps the physical handle to the reserved address"), `cuMemSetAccess` ("a special function to make the map available"), and the deallocation counterparts `cuMemUnmap`, `cuMemAddressFree`, `cuMemRelease`. `[paper]`
- **Repository exists** (github.com/intelligent-machine-learning/glake, GMLake subdirectory) but **was not cloned in this pass**. No commit hash, file path, class or function from the repository is asserted: `NOT_INSPECTED`. The names above are the paper's citations of NVIDIA's API, not GMLake source symbols.

## 12.9 Kernel execution

GMLake does not participate in kernel → thread-block → warp → instruction execution. Its effect on execution is second-order and worth stating precisely `[inference]` from the paper's own claims:

- A tensor allocated from a stitched sBlock is addressed through one contiguous virtual range, so kernels index it exactly as before; the scatter is absorbed by the GPU MMU's page mapping. `[paper]` (design intent) The paper reports throughput parity or better (Figure 13) and does **not** report a per-kernel bandwidth or TLB-pressure measurement, so any claim that stitching costs nothing in the memory pipeline would be unsupported — the paper does not measure TLB reach or page-walk effects of scattered backing. That is a genuine gap: `NOT_IN_PAPER`.
- The one execution-visible cost is allocator-path latency on the first few iterations (S2/S3/S4 invoke VMM calls), which converges to S1-only after ~4 iterations. `[paper]`

## 12.10 Memory traffic

GMLake does not move data. It changes *which physical chunks a virtual range maps to*, so the register ↔ shared ↔ L1 ↔ L2 ↔ HBM path is unchanged and no host↔device traffic is added. `[inference]` — the paper makes no traffic claim, and this follows from the fact that `Stitch` remaps rather than copies. `[paper]`

Where memory traffic *is* affected indirectly: by fitting the working set in HBM, GMLake avoids the OOM that would otherwise force a smaller batch or more offloading (host↔device traffic). The paper reports it "enables training with batch sizes that cause OOM on vanilla PyTorch." `[paper]`

No DRAM-bandwidth, L2-hit-rate or TLB numbers are reported → `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed)

The primary metric is capacity, not speed. Decomposition `[paper]`:

1. **Capacity recovered by removing the contiguity requirement.** Average **9.2 GB** saved, up to **25 GB** on A100-80 GB, across the evaluated LLMs; fragmentation ratio down **15% on average, up to 33%**. `[paper]`
2. **Scaling behaviour is the clearest evidence of the mechanism.** From 1 to 16 GPUs, PyTorch's fragmentation grows from ~10% to ~24% while GMLake holds ~10% (Figure 11). `[paper]` This is precisely the regime where ZeRO-3/FSDP partitioning makes allocation sizes irregular, so the fact that GMLake is flat is the mechanism working as theorised.
3. **Named per-scenario results with their qualifiers** `[paper]`: OPT-13B with LoRA + recomputation, ~24% utilisation improvement (5–10 GB saved); GPT-NeoX-20B at 16 GPUs, 23% utilisation gain (17 GB saved); peak utilisation held above ~90% versus baseline 76% at 16 GPUs.
4. **Throughput is preserved because the expensive API calls are eliminated after warm-up, not made faster.** `cuMemSetAccess` at 96.8× native is only paid while S2/S3/S4 fire; convergence to S1 at ~4 iterations removes it. `[paper]` In some large-batch cases GMLake is *faster* than PyTorch, attributed to reduced allocation/deallocation overhead. `[paper]`
5. **Why the 2 MB chunk choice matters causally.** Small chunks maximise defragmentation flexibility but multiply the number of `cuMemCreate`/`cuMemSetAccess` calls (hence 115.4× at 2 MB); large chunks cheapen the API but coarsen the granularity. The 128 MB fragmentation limit is the second-order guard, keeping the allocator from stitching tiny pieces and inflating sPool search cost. `[paper]`
6. **Where it degrades:** "when DNN training exhibits an extremely irregular pattern, it may generate numerous small blocks leading to frequent splits and stitches, causing early attainment of the limitation," and excessive stitching "can impair the efficiency of the GMLake allocator" through sPool search cost. `[paper]`

## 12.12 Hardware generation dependence

- **Requires the CUDA low-level VMM API** (`cuMemCreate`/`cuMemMap`/`cuMemSetAccess`/`cuMemAddressReserve`), which the paper dates to roughly 2020. `[paper]` This is a driver/CUDA-version dependence, not only a silicon one.
- **Requires GPU MMU support for multiple virtual mappings onto the same physical chunk**, since `Stitch` maps without unmapping. `[paper]`
- **Requires the 2 MB physical-chunk granularity** the VMM API exposes; the design's fallback for sub-2 MB allocations is PyTorch's original splitting. `[paper]`
- Evaluated exclusively on **NVIDIA A100-80 GB** (8 per node over NVLink; two such nodes over RDMA) with **CUDA 11.4, cuDNN 8.5**, Intel Xeon Platinum 8369B hosts with 1 TB DRAM. `[paper]` Generalisation to V100/H100 is listed by the authors as unaddressed. `[paper]`
- **AMD/HIP portability is not discussed** → `NOT_IN_PAPER`. (HIP has analogous virtual-memory-management entry points, but the paper makes no such claim and none is asserted here.)

## 12.13 Limitations

Author-stated `[paper]`:
1. 2 MB chunk overhead is "considerable" and is mitigated by data-structure and stitching-strategy design rather than removed; sub-2 MB allocations revert to PyTorch splitting and can still fragment within that range.
2. Extremely irregular allocation patterns generate many small blocks, frequent splits and stitches, and early attainment of the fragmentation limit.
3. sPool capacity management: excessive stitching impairs allocator search efficiency; LRU eviction is triggered but no guarantee against pathological behaviour is claimed.
4. Evaluation focuses on fine-tuning; pre-training patterns may differ.
5. Single hardware target (A100); V100/H100 generalisation not addressed.
6. Transformer models only; CNNs/RNNs not discussed.
7. No comparison against compaction- or copy-based garbage-collection alternatives in practice.

Observed here, not claimed `[inference]`:
8. **No measurement of the memory-system consequences of scattered backing.** Stitching gives virtual contiguity over physically scattered 2 MB chunks; the paper reports throughput parity but no TLB-reach, page-walk or achieved-bandwidth data. On a GPU where large-page/TLB reach matters, this is the natural place for a hidden cost, and it is unmeasured.
9. **No sensitivity sweeps** for the sPool LRU threshold, the 128 MB fragmentation limit, or the 2 MB chunk size as a swept parameter (the chunk size appears only in the overhead table).
10. **Analysed from the preprint**, not the ACM camera-ready (`dl.acm.org` 403 here); camera-ready differences are undetectable from this evidence.

## 12.14 Relation to prior corpus

- `prior_corpus_check`: **`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`.** GMLake is an LLM-training memory-systems paper and therefore plausibly belongs to the ~80-paper AI/HPC systems corpus that `domains/ai_hpc_systems/` records as `EXTERNAL_IMPORT_PENDING` and that is **not** present in this repository. This analysis therefore makes **no claim** as to whether an analysis of GMLake already exists there. Within *this* repository, the only hits for "GMLake" are `domains/gpu_systems/census/ASPLOS_2024.md`, the ASPLOS program evidence dump, and a raw proceedings TOC dump under `domains/hpc_quantum/.../working-evidence/p000.txt` — none is an analysis.
- **Lineage verified from GMLake's own related work** `[paper]`: the paper distinguishes itself from **vLLM** (tensor-level virtual memory for self-attention padding — "GMLake works on a unique memory scope for DNN training, which is different from the vLLM and vMalloc/CUDA VMM"), from **raw CUDA VMM / vMalloc** (pool-unaware primitives), and from the **PyTorch/TensorFlow BFC allocator** (splitting-based). It positions **ZeRO-Offload**, **DeepSpeed ZeRO-3**, **LoRA** and **gradient checkpointing/recomputation** as orthogonal techniques whose irregular allocation behaviour *motivates* GMLake rather than competing with it.
- Note on a prior-art expectation: SUV's related work (`GPU-MICRO24-01`) cites **DeepUM, Sentinel, SwapAdvisor, Capuchin, G10** as the DNN-specialised UVM/offload line. GMLake's related work as read does **not** name those systems, so no citation link is asserted in either direction — this is a difference in framing (allocator-level defragmentation vs migration/offload scheduling), verified only from each paper's own related-work section.
- **Complementary within this cluster:** GMLake and SUV both decide *what occupies HBM* but at different layers and with different mechanisms — GMLake changes the virtual→physical mapping so the same bytes fit, SUV changes which bytes are resident at all. Neither cites the other. `[inference]`
- `EXISTING_CORPUS_DUPLICATE`: **cannot be determined** for the external corpus (see above); **no** within this repository.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — but this is the weakest NO in this cluster, and the reasoning matters.** The *concept* (map a contiguous virtual range onto non-contiguous physical memory to defeat fragmentation) is generic; on a CPU, `mmap`/`MAP_FIXED` over anonymous pages has provided it for decades, and CPU allocators do not have GMLake's problem because the OS already virtualises their address space.

The GPU-specific properties the contribution actually depends on, all `[paper]`:
1. **The framework caching allocator exists because the GPU native allocator is 9.7× slower on throughput**, so the "just free and re-allocate" escape a CPU allocator has is closed.
2. **GPU device memory was, until the CUDA VMM API, allocated as physically-and-virtually contiguous units** — the virtual/physical decoupling GMLake needs is a recent *CUDA driver* capability at a fixed **2 MB** chunk granularity, and the design is shaped entirely around that granularity and around `cuMemSetAccess` costing 96.8× native `cuMalloc` at it.
3. **Multiple virtual mappings to one physical GPU chunk** is the specific GPU MMU permission that makes `Stitch` non-destructive.
4. The fragmentation is produced by **GPU-resident DNN training** under GPU memory-reduction techniques (recomputation, ZeRO-Offload, ZeRO-3 across NVLink-connected A100s, LoRA), and the capacity being reclaimed is **HBM on an 80 GB A100**.

verdict_basis: the contribution depends on CUDA's GPU virtual-memory-management API semantics (2 MB chunk granularity, `cuMemSetAccess` cost, multiple VA→PA mappings) and on the GPU framework caching-allocator regime that exists because native GPU allocation is prohibitively slow; the general idea of virtual-to-physical remapping is not GPU-specific, but the mechanism, its cost structure and the problem instance are. Verdict `CORE_GPU`, with the honest caveat that this is a GPU-software-stack contribution rather than a GPU-microarchitecture one.

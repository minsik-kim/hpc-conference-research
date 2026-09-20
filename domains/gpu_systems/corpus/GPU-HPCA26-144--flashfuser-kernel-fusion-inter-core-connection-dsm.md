# GPU-HPCA26-144 — FlashFuser: Expanding the Scale of Kernel Fusion for Compute-Intensive Operators via Inter-Core Connection

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`; also `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — an LLM/CNN operator-fusion compiler is squarely the kind of item the pending `domains/ai_hpc_systems/` AI/HPC corpus is stated to contain; **nothing is asserted** about whether it is duplicated there
primary_topic: `I — kernel fusion and code generation`
secondary_topics: `H — compiler scheduling / search-space design; Hopper thread-block clusters and distributed shared memory; TMA and mbarrier; CUTLASS code generation; LLM inference operator chains`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2512.12949v1), read in two passes — (a) title/authors/affiliations, introduction and the SMEM-capacity motivation, the DSM/"inter-core connection" hardware substrate and its explicit identification as NVIDIA H100, the fusion scope (GEMM chains, convolution chains via im2col, gated FFN), the dsm_comm primitive family, the Dataflow Analyzer (Algorithm 1), the Fusion Search Engine cost model and five pruning rules (Algorithm 2), the Python front-end / CUDA+CUTLASS back-end split; (b) evaluation — H100 SXM host, software stack versions, baselines, model/workload list, headline speedups, the Figure 15 ablation, the discussion of architecture-generality and of where the end-to-end gains vanish, and the related-work table with venues. NO DEDICATED LIMITATIONS SECTION EXISTS — the paper's constraints are stated inside the evaluation discussion; recorded as such, not fabricated.`

## 12.1 Bibliographic facts

- Title: **FlashFuser: Expanding the Scale of Kernel Fusion for Compute-Intensive Operators via Inter-Core Connection** [paper].
- Venue: **HPCA 2026** [census: `domains/gpu_systems/census/HPCA_2026.md`, row 11, IEEE article number **11408495**]. The arXiv HTML does not itself state the venue [paper] — venue rests on census evidence.
- Authors [paper]: **Ziyu Huang, Yangjie Zhou, Zihan Liu, Xinhao Luo, Yijia Diao, Minyi Guo, Yu Feng, Chen Zhang, Jidong Zhai, Anbang Wu, Jingwen Leng**. Affiliations [paper]: **Shanghai Jiao Tong University; Shanghai Qi Zhi Institute; Tsinghua University; National University of Singapore**. Per-author affiliation mapping was not resolvable from the fetched HTML — `UNKNOWN`, not guessed.
- arXiv: **2512.12949**.
- Artifact: `NOT_FOUND_AFTER_SEARCH` [census]. No repository was located; `NOT_INSPECTED`; **no source symbols are asserted** in this file.
- Publication type: `ARCHIVAL_MAIN_PAPER` (+ `PREPRINT` arXiv 2512.12949).

## 12.2 Core question (one sentence)

Kernel fusion for compute-intensive operator chains has always been capped by the shared memory of **one** SM — when the intermediate tensor does not fit, fusion is abandoned and the chain round-trips through global memory; can Hopper's **distributed shared memory (DSM)**, which lets the SMEMs of the SMs in a thread-block cluster address one another, be turned into a *compiler-visible* memory tier so that the fusible working set becomes cluster-sized rather than SM-sized?

## 12.3 GPU/HPC problem translation

- **Memory.** The stated hard constraint: SMEM is **227 KB per SM on an H100** [paper], and "when the intermediate results exceed the limited capacity (such as FFN), the fusion fails" [paper]. Existing systems — the paper names **cuBLAS, CUTLASS, SGLang, Chimera, BOLT** — "typically handle smaller operator chains by placing intermediate results in the shared memory (SMEM) or registers of a single SM" [paper].
- **Compute.** The motivating imbalance, quantified by the paper: **peak compute on H100 rose 3.3× over A100 while memory bandwidth rose only 1.5×** [paper]. Fusion is therefore the lever that matters, and its reach is what is being extended.
- **Communication.** This is what makes the paper unusual for a fusion paper: the fused kernel must now perform *collective* operations **between SMs inside a cluster**. The paper introduces `dsm_all_exchange` (cluster-wide accumulation along K), `dsm_shuffle` (intra-cluster redistribution), `dsm_reduce_scatter` (two-level: intra-cluster then inter-cluster via TMA) [paper]. A GEMM-chain compiler has acquired an all-reduce.
- **Synchronization.** Many-to-many inter-block coordination is implemented with **TMA and `mbarrier`** [paper].
- **Scheduling.** The search space grows from ≈10⁴ (SMEM-only) to ≈10⁶ with DSM [paper]; the cluster shape is a new set of schedule variables `cls_m, cls_n, cls_k, cls_l` [paper].

## 12.4 Why the problem exists (hardware root cause)

1. **SMEM is per-SM and small.** 227 KB on H100 [paper]. An FFN intermediate for a realistic hidden size does not fit, so the fusion boundary falls exactly where LLM inference needs it most.
2. **Global memory is the only alternative tier below it — until Hopper.** The paper places DSM as an intermediate: "The SMEMs of different SMs can be connected via DSM, which is also considered an **L1.5 cache**" [paper]. Global memory on H100 is quoted at **2 TB/s to 3 TB/s** [paper]; DSM bandwidth is "variable depending on cluster size, with lower latency than off-chip memory for most configurations" [paper]. The existence of a tier between SMEM and HBM is a *Hopper-generation* fact, and it is the paper's entire premise.
3. **Cluster size is hardware-bounded.** One of the five pruning rules is a "Cluster size constraints (product ≤ 16 on H100)" [paper] — i.e. the compiler's search space is directly shaped by an architectural limit on thread-block clusters.
4. **Compute/bandwidth divergence** (3.3× vs 1.5× [paper]) is why the fusion boundary keeps mattering more each generation.

## 12.5 Mathematical / performance model

- **Cost model, minimax over memory levels** [paper]:
  `min { max_l C_l }`, where `C_l = V_l / B_l` — data volume at level `l` divided by that level's bandwidth. The objective is the *bottleneck* tier, not total traffic. Levels are register → SMEM → DSM → L2/global.
- **Dataflow Analyzer (Algorithm 1)** [paper]: iterates tensor dimensions in **reverse schedule order**, greedily places reused tensors across cache levels, computes per-level transferred volume from the tiling strategy, and emits a concrete **spilling plan** plus total data-movement volume. Its three decision axes: **Loop Schedule** (nesting order; spatial vs temporal partitioning of M, N, K, L), **Tile Selection** (cluster-level and block-level tile sizes), **Resource Mapping** (which tier holds each tensor).
- **Search-space size** [paper]: DSM-inclusive raw space **2.75 × 10¹³**; after the five pruning rules, **≈1.15 × 10⁶**. (The paper also states ≈10⁶ with DSM vs ≈10⁴ SMEM-only as the shape of the growth.)
- **The five pruning rules** [paper]: (i) divisible tile sizes (hardware alignment); (ii) cluster-size product ≤ 16 on H100; (iii) activation ordering — accumulation in the innermost loop; (iv) dependency constraints ruling out impossible spatial partitions; (v) memory-capacity limits — no tensor may exceed its lowest spillable level.
- **Search algorithm (Algorithm 2)** [paper]: enumerate → prune → cost-estimate via the Dataflow Analyzer → keep top-K → **profile the best K on real hardware** → select. So the model is a *filter*, not the final arbiter — a hybrid analytical/measured scheme.
- **Cluster shape variables** [paper]: `cls_m, cls_n, cls_k, cls_l`, determining how blocks partition work and how many participate in each communication phase.

## 12.6 Data layout and ownership

The hierarchy is the contribution, so it is worth stating level by level as the paper defines it:

- **thread / warp**: not a named object in the scheduling model; intra-tile work is delegated to **CUTLASS** [paper].
- **thread block**: owns a block-level tile; block-level tile sizes are one of the three Tile Selection axes [paper].
- **thread-block cluster (the new level)**: up to **16 blocks on H100** [paper]; owns a cluster-level tile; its shape is `(cls_m, cls_n, cls_k, cls_l)`. The cluster's *aggregate* SMEM is the "expanded on-chip memory pool" — "by interconnecting the SMEM of multiple SMs, it creates what can be viewed as an expanded on-chip memory pool" [paper].
- **SM**: holds one block's SMEM, which is simultaneously a private scratchpad and a slice of the cluster pool. This dual role is what the Dataflow Analyzer has to reason about.
- **memory tiers, in the analyzer's order** [paper]: register → SMEM → **DSM** → L2/global.
- **GPU**: one H100 SXM [paper].
- **node**: dual-socket Intel Xeon Platinum 8468 (96 cores, 2.10 GHz) host [paper].
- **cluster (machine)**: single-GPU evaluation. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- the DSM communication primitives, names as printed --------  [paper]
dsm_all_exchange(...)     # cluster-wide accumulation (all-reduce) along K
dsm_shuffle(...)          # intra-cluster data redistribution during compute
dsm_reduce_scatter(...)   # two-level: intra-cluster, then inter-cluster via TMA
# all parameterised by (cls_m, cls_n, cls_k, cls_l)

# --- Algorithm 1: Dataflow Analyzer (shape as described) -------  [paper]
for dim in reversed(schedule_order):
    for tensor in reused_tensors(dim):
        level = lowest_tier_that_fits(tensor, {reg, smem, dsm, l2_global})
        plan[tensor] = level
        V[level] += transferred_volume(tensor, tiling)
return plan, V

# --- Algorithm 2: Fusion Search Engine (shape as described) ----  [paper]
cands = enumerate(loop_schedule x tile_sizes x resource_mapping)   # 2.75e13
cands = prune(cands, rules 1..5)                                   # ~1.15e6
for c in cands:
    plan, V = DataflowAnalyzer(c)
    cost[c] = max_l ( V[l] / B[l] )          # minimax bottleneck tier
best = profile_on_hardware(top_k(cands, by=cost))
```

`[reconstruction]` applies to the loop shapes only; `dsm_all_exchange`, `dsm_shuffle`, `dsm_reduce_scatter`, `cls_m/n/k/l`, the rule set and the minimax objective are printed in the paper.

## 12.8 Real implementation

- **Front-end: Python** — search engine, cost model, pruning; outputs top-K scheduling configurations [paper].
- **Back-end: CUDA / CUTLASS** — code generation "translates the selected plan into fused kernels, realizing the dataflow analyzer's spilling decisions and implementing `dsm_comm` primitives using NVIDIA's **Tensor Memory Accelerator (TMA)** and **`mbarrier`** synchronization for many-to-many inter-block coordination" [paper].
- **Fusion scope** [paper]: GEMM chains (consecutive matmuls in FFN), convolution chains (converted to GEMM via **im2col**), and gated FFN structures such as **SwiGLU** with branched computation.
- **No repository located**; `NOT_INSPECTED`. **No symbol, pass name, or file path is asserted.** This is the principal evidentiary weakness of this entry relative to `GPU-ASPLOS26-141` and `GPU-ASPLOS26-143`, both of which had inspectable code.

## 12.9 Kernel execution

- **kernel**: one fused kernel replaces an operator chain that previously launched several. The kernel-launch boundary being *removed* is part of the win, but the paper does not separate launch overhead from memory traffic — `NOT_IN_PAPER`.
- **thread-block cluster**: the execution unit that did not exist before Hopper. Blocks in a cluster are co-resident by construction, which is what makes a *blocking* inter-block collective (`dsm_all_exchange`) safe at all — an ordinary inter-block barrier on a GPU can deadlock because co-residency is not guaranteed. The paper does not spell this out; the reasoning is `[inference]` from the cluster mechanism and is flagged as such.
- **thread block → warp → instruction**: delegated to CUTLASS; the paper's scheduling model stops at the block [paper].
- **TMA** carries the inter-cluster half of `dsm_reduce_scatter` and the global↔shared bulk copies [paper].

## 12.10 Memory traffic

- **The traffic claim, with its qualifier**: "**58% reduction in memory access**" versus PyTorch, measured as global memory traffic on H100 [paper].
- **Tier structure**: intermediates "spill progressively across register, SMEM, and DSM tiers rather than falling back to global memory" [paper]. The word *progressively* is the mechanism: the analyzer does not make a binary fits/does-not-fit decision but a per-tensor placement.
- **DSM bandwidth is cluster-size-dependent** [paper], so the cost model's `B_l` for the DSM tier is itself a function of the schedule — a coupling the minimax objective has to absorb.
- **Measured with Nsight Compute 2025.2.0** [paper].
- Per-level measured volumes are not tabulated in the fetched text beyond the 58% figure. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

From the paper's own ablation (Figure 15), the decomposition is unusually clean:

| Configuration | Speedup vs no-fusion baseline [paper] |
|---|---|
| Dataflow Analyzer only (`DA`, SMEM/global only) | **1.52×** |
| `dsm_comm` + Dataflow Analyzer, random configuration (`DC+DA`) | **2.11×** |
| Full system (`All`) | **3.29×** |

Read as causes:

1. **Better placement within the classical hierarchy alone** buys 1.52× — i.e. a third of the gain is *not* about DSM at all, but about the reverse-order greedy spilling plan.
2. **Making DSM addressable** buys the step to 2.11× even with a *random* schedule — the tier itself, not the search, is worth ~1.39× on top.
3. **The search engine** (pruning + minimax cost model + top-K hardware profiling) buys the step to 3.29×, ~1.56× on top of that.
4. **Where it does not help**: 70B-class models are "primarily compute-bound, thus offering limited room for kernel-level optimization" [paper, Figure 16a], and end-to-end gain decays as batch size grows (**1.16× average for batch 1–32** on larger models [paper]). The honest reading is that FlashFuser's regime is memory-bound decode-side chains, not compute-bound prefill.

Headline numbers, each with qualifiers as the paper states them [paper, all on H100 SXM]: **3.3× kernel speedup** against highly-tuned libraries (cuBLAS/TensorRT, average across workloads); **4.1×** against state-of-the-art compilers (Chimera, peak kernel); per-class averages **4.6×** on GEMM chains and **6.4×** on convolution chains against Chimera; **1.24× end-to-end** within SGLang.

## 12.12 Hardware generation dependence

- **Strongly Hopper-bound, and the paper knows it.** DSM (thread-block clusters) is a Hopper feature; the cluster-size ≤16 pruning rule, the 227 KB SMEM figure, the 2–3 TB/s global bandwidth, and the TMA-based `dsm_reduce_scatter` are all H100 facts [paper].
- The paper's generality claim is explicitly hedged: "While our evaluation is conducted on the NVIDIA H100, the proposed fusion strategy is not limited to a specific architecture" [paper]. For mesh architectures (Cerebras WSE) it sketches a neighbourhood-based shuffle/reduce mapping that is **untested** [paper].
- Pre-Hopper NVIDIA GPUs (A100 and earlier) have no DSM, so on those the system degenerates to the `DA`-only configuration — which the ablation prices at 1.52× rather than 3.29× [paper, inference from Figure 15].

## 12.13 Limitations

**No dedicated limitations section exists**; the following are stated inside the evaluation/discussion [paper]:

- H100-specific evaluation, with generality asserted but not demonstrated; the Cerebras mapping is a sketch.
- Compute-bound regimes (70B+ models) offer "limited room for kernel-level optimization".
- End-to-end benefit decays with batch size (1.16× average, batch 1–32, larger models).
- The search requires **on-hardware profiling of the top-K candidates** [paper, Algorithm 2] — so tuning is not purely analytical and its cost is not reported in the fetched text (`NOT_IN_PAPER`).
- Per-tier measured traffic beyond the aggregate 58% figure is not reported.
- No artifact located, so none of the above is independently checkable from code.
- **Baseline-version gap, recorded as a weakness of the evidence**: TVM 0.9 is used [paper] while CUDA 12.4 / PyTorch 2.6 / Triton 3.2 are current-generation — TVM 0.9 predates the H100 support that a fair TVM baseline would need. The paper does not address this.

## 12.14 Relation to prior corpus

- **Complementary to `GPU-ASPLOS26-141` (Tilus)**: Tilus provides the *language* in which a cluster-scoped, TMA-driven kernel could be written by hand (its IR contains `ClusterSyncThreadsInst`, `CopyAsyncBulkGlobalToClusterSharedInst`, `MapSharedAddrInst` at commit `4597cd5` [code]); FlashFuser provides the *search* that decides what such a kernel should be. Neither cites the other, but they are the two halves of the same 2026 development.
- **Directly related to MCFuser (SC 2024)** — adjudicated `RELATED_GPU` in [`_LEDGER_compiler_programming.md`](_LEDGER_compiler_programming.md) and therefore **carrying no stable ID and no deep analysis in this corpus** (an earlier draft of this file cited a non-existent `GPU-SC24-145`; corrected 2026-09-19) — FlashFuser cites MCFuser as "SC24" prior work in its related-work table [paper]. That is a verified, paper-internal citation link between an SC paper and an HPCA paper, and it is one of the concrete data points for this cluster's lineage question.
- **Complementary to the collective-communication cluster** (`GPU-SC26-21`, `GPU-SC26-22`, `GPU-ASPLOS26-01` MSCCL++): FlashFuser performs an *all-reduce inside a single GPU's cluster*, so the same algorithmic vocabulary now appears at two scales.
- **Prior work the paper names, with venues as it reports them** [paper]: Halide (PLDI), TVM (OSDI'18), Ansor (OSDI'20), AStitch (**ASPLOS 2022**), BOLT (MLSys'22), TASO (SOSP'19), **Chimera (HPCA 2023)**, Welder (OSDI'23), **MCFuser (SC'24)**, **T10 (SOSP 2024 — DSM on the Graphcore IPU)**, WaferLLM (arXiv, Cerebras), ClusterFusion (arXiv 2025, hand-written DSM kernels with no compiler), Fusion Stitching (arXiv).
- `NO_EXISTING_ANALYSIS`; `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` flagged for the pending AI/HPC import.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: **framework → kernel**, with code generation through **CUDA/CUTLASS**. It is a schedule-search compiler that sits above CUTLASS and below the serving framework (SGLang); it does not define a language and does not emit PTX directly.

verdict_basis: The contribution is the promotion of **Hopper distributed shared memory** — the thread-block cluster's cross-SM SMEM window, bounded at 16 blocks on H100 — to a first-class, compiler-schedulable memory tier between SMEM and L2, together with three collective primitives (`dsm_all_exchange`, `dsm_shuffle`, `dsm_reduce_scatter`) realised on **TMA** and **`mbarrier`** [paper]. The pruning rules, the cost model's tier list and the schedule variables `cls_m/n/k/l` are all statements about that specific hardware object. The paper's own ablation shows that stripping DSM out leaves 1.52× of 3.29× [paper, Figure 15] — so more than half the contribution evaporates without the GPU feature. This is **not** the borderline case of a retargetable tensor compiler that happens to emit PTX: the schedule space itself is defined by a Hopper-only interconnect. The residual `DA`-only component *is* generic, and that is exactly the part the ablation prices separately.

verdict: `CORE_GPU`

# GPU-ICS24-02 — Shared Virtual Memory: Its Design and Performance Implications for Diverse Applications

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `D — GPU unified/shared virtual memory, oversubscription, page migration` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `AMD ROCm/HMM driver internals; oversubscription characterization methodology`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background on SVM vs UVM design space incl. Table 1 comparison; methodology (platform, ROCm/amdgpu versions, Systemtap instrumentation points, DOS definition); characterization results (three application categories, Fig. 5 cost breakdown, Fig. 7 migration/eviction profiles, fault-filtering statistics); Section 4.1 SVM-aware algorithm design and Section 4.2 driver design recommendations; author-stated limitations and future work; related work. Read via two targeted full-text passes over arXiv HTML v1.`

## 12.1 Bibliographic facts

- Title: *Shared Virtual Memory: Its Design and Performance Implications for Diverse Applications* `[paper]`
- Authors: Bennett Cooper (Clemson University), Thomas R. W. Scogland (Lawrence Livermore National Laboratory), Rong Ge (Clemson University) `[paper]`
- Venue: ICS 2024 (38th ACM International Conference on Supercomputing), Session 2 "Best Paper Nominees" — recorded as **Best Paper Runner-Up** `[official-program, via census/ICS_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER` (analysed from the `PREPRINT` arXiv v1)
- DOI: `10.1145/3650200.3656608` `[publisher-proceedings — DOI string surfaced by search result titles for dl.acm.org and dx.doi.org records; the ACM page itself is unreachable here (403)]`
- Full text used: https://arxiv.org/html/2405.06811v1 `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` → `NOT_INSPECTED`.
- Note: this paper is a **characterization study**, not a mechanism proposal. The template sections below are answered accordingly; several mechanism-oriented sections are legitimately `NOT_IN_PAPER`.

## 12.2 Core question (one sentence)

NVIDIA UVM has been studied extensively but AMD's Shared Virtual Memory — which is the unified-memory path on Frontier and El Capitan and which is built on the Linux kernel's **Heterogeneous Memory Management (HMM)** rather than on a vendor-specific subsystem — has not; so what is SVM's actual design, and what are the root causes of the performance collapse applications suffer under it? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** Primary axis: GPU HBM capacity versus application footprint, mediated by a fault-and-migrate driver. The paper's control variable is **Degree of Oversubscription (DOS) = used_size / available_size × 100**, swept from ~78% to **156%**. `[paper]`
- **Communication.** Host↔device movement over **36 GB/s bidirectional Infinity Fabric** (intra-GPU link 200 GB/s). The paper's most consequential finding is that this leg is *not* where most of the time goes. `[paper]`
- **Compute.** Degradation is reported as normalised throughput; the SIMT pipeline is stalled by driver work, not by transfer bandwidth.
- **Scheduling.** SVM's *range* granularity is effectively an implicit prefetch scheduler, and the paper's argument is that it is scheduled wrongly for some access patterns. `[paper]`
- **Synchronization.** Not a first-order concern, but fault *serialisation* is: "SVM receives a single fault each time and handles it immediately," with no batching. `[paper]`

## 12.4 Why the problem exists (hardware root cause)

This is the paper's real contribution, and the causes are architectural rather than incidental.

1. **SVM's management unit is a *range*, not a page.** SVM manages memory in ranges, typically **1 GB-aligned**, sized **4 KB–1 GB**, and "a single fault can trigger an entire range migration" — ranges can comprise up to **256 K pages**. `[paper]` This makes the driver an *unconditional aggressive prefetcher* at range granularity. Beneficial when HBM is not oversubscribed; catastrophic when it is, because a range migration can evict data that is still live.
2. **Faults are not batched.** Table 1's comparison is the sharpest statement of the SVM/UVM design divergence `[paper]`:

   | Feature | SVM | UVM |
   |---|---|---|
   | Fault batching | No (single fault at a time) | Yes (up to 256 faults) |
   | UM (de)allocation unit | Range [4 KB – 1 GB] | VABlock (2 MB) |
   | Migration unit | Range | Page (64 KB without prefetch; VABlock with prefetch) |
   | Eviction unit | Range | VABlock |
   | Eviction policy | Least Recently Faulted | *not stated in the read text* |

   The consequence the paper draws: single-fault handling gives "faster turnaround" and lets duplicates be detected, but it overloads the driver "with fault interrupts, even after some faults are filtered." `[paper]`
3. **Duplicate faults dominate the raw fault stream.** "Duplicate faults typically dominate, representing 97–99% of the total faults generated by a kernel," filtered through a content-addressable-memory buffer; only "serviceable" faults trigger migration, and "one serviceable fault per range typically suffices." `[paper]` This is a direct consequence of SIMT: thousands of threads in flight fault on the same page essentially simultaneously, so the *fault rate* is a warp-concurrency artefact, not an access-pattern artefact.
4. **The eviction policy is Least Recently Faulted, not least recently used.** `[paper]` The paper names the failure mode: the LRF policy "may evict the most intensely reused data, further exacerbating thrashing." A range that was faulted in early and then *reused heavily without further faults* looks stale to LRF precisely because it is resident and working.
5. **Therefore the dominant cost is driver bookkeeping, not data movement.** Without oversubscription, "the actual data movement across the host and device memory domains only accounts for less than half of the overall cost." `[paper]` The three largest components are `cpu_update`, `SDMA_setup` and `alloc`, together "roughly 76% of the overall cost." `[paper]` Under oversubscription, `alloc` — which *includes eviction* — "increases the most and becomes dominant across the applications," and for SGEMM its slope "surpass[es] the others by orders of magnitude." `[paper]`

Root cause in one sentence: a range-granular, non-batching, least-recently-*faulted* driver built for hardware generality (HMM) collides with GPU workloads whose fault streams are massively duplicated and whose reuse is invisible to a fault-based recency metric.

## 12.5 Mathematical / performance model

The paper gives no analytic model. Its quantitative apparatus is:

- **DOS = used_size / available_size × 100**, swept up to 156. `[paper]`
- A **five-component cost decomposition** traced by Systemtap `[paper]`: `cpu_unmap` (collect/unmap host pages), `SDMA_setup` (System DMA mapping and command issue), `alloc` (device VRAM allocation, including eviction), `cpu_update` (host page-table updates after migration), `misc` (metadata, non-overlapped copy, cleanup).
- A **three-category taxonomy of oversubscription response**, which functions as the paper's predictive claim `[paper]`:
  - **Category I** (STREAM, Conv2d, BFS): moderate, roughly linear degradation as DOS rises.
  - **Category II** (Jacobi2d): a cliff at DOS ≥ 100, then a plateau — approximately 40% of baseline throughput at DOS = 109.
  - **Category III** (SGEMM, MVT, GESUMMV): near-total collapse above DOS = 100.
- The discriminating property, stated as the qualifier on the whole taxonomy: whether the application exhibits "temporal patterns involving data reuse" or "spatial patterns with small amounts distributed across ranges." `[paper]` Both are pathological for range-granular management — the first because reuse without faults defeats LRF, the second because a small touched amount drags a whole range across the link.

Per-application slope structure reported `[paper]`: STREAM shows two linear segments with a slight slope increase after oversubscription; Jacobi2D shows three segments with the steepest slope when oversubscribed by under 10%; SGEMM shows dramatic escalation in the oversubscribed segment.

## 12.6 Data layout and ownership

- **thread → warp → CU:** the origin of the duplicated fault stream; 97–99% of faults are duplicates filtered in a CAM buffer. `[paper]`
- **GPU (one compute die of an MI250X, 64 GB HBM2E):** the capacity under contention. `[paper]`
- **Range — the ownership unit that defines this paper.** 4 KB–1 GB, 1 GB-aligned, up to 256 K pages; migration, eviction and (de)allocation all happen at range granularity. `[paper]` Compare UVM's VABlock at 2 MB: the granularity ratio between the two vendors' management units is up to ~512× at the top end, which is why insights do not transfer — the paper says so explicitly: "SVM has a distinct design from UVM, and the insights derived for UVM may not be directly applicable to SVM." `[paper]`
- **Host (64-core AMD 7A53 EPYC, 512 GB DDR4):** the overflow tier and the location of the HMM page tables that `cpu_update` maintains. `[paper]`
- **node:** one node of LLNL's **Tioga**, architecture-matched to Frontier. `[paper]`
- **cluster:** out of scope — single-die measurements only. `[paper]`

## 12.7 Pseudo code

The paper describes driver behaviour, not an algorithm it proposes. The following is a `[reconstruction]` of the SVM fault-service path from the paper's prose; every named component is `[paper]`.

```
# SVM fault service, as characterized (NOT a proposal by the paper)
on_gpu_tlb_miss_xnack(vaddr):                      # [paper]: XNACK / retry-fault signalling
    f = fault(vaddr)
    if CAM_buffer.contains_recent(f):              # [paper]
        drop(f)                                    # 97-99% of faults land here
        return
    # serviceable fault, handled immediately, NOT batched            [paper]
    r = range_of(vaddr)                            # [paper] 4KB..1GB, 1GB-aligned
    while not fits(r, free_vram):                  # [paper]
        victim = least_recently_faulted_range()    # [paper] LRF, not LRU
        evict(victim)                              # cost accounted to `alloc`   [paper]
    cpu_unmap(r)                                   # [paper]
    SDMA_setup(r) ; sdma_copy(r)                   # [paper]
    alloc_vram(r)                                  # [paper]
    cpu_update(page_tables_for(r))                 # [paper] largest component when not oversubscribed
```

The instrumentation-side pseudo code is the paper's actual method: Systemtap probes on the five named SVM driver functions, timing each. `[paper]`

## 12.8 Real implementation

Nothing is implemented by the authors; the object of study is the shipped stack. What is pinned `[paper]`:

- **ROCm 5.4.0**
- **amdgpu 6.3.6**
- Tri-Lab Operating System Stack v4
- GPU memory alignment: 1 GB
- **Systemtap** used to "dynamically instrument and trace the SVM driver functions," with the five probe categories named in 12.5.
- Hardware: one compute die of an **AMD Instinct MI250X** (64 GB HBM2E), **64-core AMD 7A53 EPYC** host, 512 GB DDR4, 36 GB/s bidirectional host–GPU Infinity Fabric, 200 GB/s intra-GPU.

No source repository, patch or commit is claimed; the authors did not modify the driver in the read text. `NOT_INSPECTED` at the code level — the driver function names above are the paper's, and no ROCm source file was read in this pass.

## 12.9 Kernel execution

The paper does not modify kernel execution. Two execution-level facts it establishes are important for the cluster:

1. **The fault stream's magnitude is a SIMT artefact.** 97–99% duplicate faults arise because many concurrently resident warps reference the same unmapped page at once; the CAM filter exists to absorb exactly this. `[paper]` Any GPU unified-memory design must handle a fault *storm* per touched page, not a fault.
2. **One serviceable fault per range is enough to move up to 256 K pages.** `[paper]` So the ratio between the granularity of the *signal* (one warp's access) and the granularity of the *response* (a range) is up to five orders of magnitude. That asymmetry is the paper's core mechanical insight.

Kernel-level metrics (occupancy, stall reasons, achieved bandwidth) are `NOT_IN_PAPER`.

## 12.10 Memory traffic

Path: register ↔ LDS/L1 ↔ L2 ↔ **HBM2E (64 GB on the measured die)** ↔ **Infinity Fabric 36 GB/s bidirectional** ↔ host DDR4 (512 GB). Intra-GPU (die-to-die) link: 200 GB/s. `[paper]`

The headline traffic finding is negative and useful: **the link is not the bottleneck.** Without oversubscription, actual host↔device data movement is "less than half of the overall cost," while `cpu_update` (host page-table maintenance) is the single largest component, followed by `SDMA_setup` and `alloc` — 76% combined. `[paper]` Under oversubscription the added traffic is *redundant* traffic: thrashing cases where "data migrated but evicted before use must be migrated again" raise migration counts by "orders of magnitude." `[paper]`

Absolute byte counts and achieved link utilisation are `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed)

There is no proposal to speed up, so this section decomposes the *slowdown* `[paper]`:

1. **Range-granular migration as unconditional prefetch.** One serviceable fault pulls up to 256 K pages. Below DOS 100 this is a win (bulk transfer, few faults). Above DOS 100 it is the thrash engine, because every pull may evict something live.
2. **LRF eviction is blind to reuse.** A range faulted in early and then reused heavily without further faults is a prime LRF victim. The authors state the policy "may evict the most intensely reused data." `[paper]` This is the mechanism behind Category III's collapse: SGEMM, MVT and GESUMMV have intensive reuse.
3. **`alloc` dominates under pressure because eviction is charged to it.** `[paper]` The slope explosion for SGEMM is eviction cost, not copy cost.
4. **No fault batching means driver interrupt load scales with the fault storm**, even after 97–99% duplicate filtering. `[paper]`
5. **Category II's cliff-then-plateau** (Jacobi2d, ~40% at DOS = 109) is consistent with a working set that stops fitting at a threshold and then reaches a stable thrash rate; the steepest slope is in the first 10% of oversubscription. `[paper]`
6. **Spatial scatter is the second pathology:** "successive accesses … of small amount of data … distributed across ranges" rapidly exhausts GPU memory because each small touch costs a whole range. `[paper]`

What the paper offers instead of a mechanism — its recommendations, which are the actionable product `[paper]`:
- **To application/algorithm developers:** identify temporal reuse patterns (nested loops, repeated traversals) and structure allocations accordingly; avoid spatially scattered small accesses across ranges. Case studies show gains "by up to orders of magnitude" from SVM-aware algorithm design (Section 4.1).
- **To driver implementers (Section 4.2):** reduce range size to limit prefetch overhead for temporally reused data; replace Least Recently Faulted with a smarter eviction policy; coordinate with HMM to handle distributed spatial patterns more gracefully.

## 12.12 Hardware generation dependence

- **AMD-specific and HMM-specific.** SVM "interfaces with the Linux kernel's Heterogeneous Memory Management (HMM) … designed for broader hardware compatibility," which the paper contrasts with UVM being "developed for NVIDIA's specific hardware … for performance, optimization, and efficiency." `[paper]` The generality/performance trade-off is the paper's framing of *why* SVM behaves as it does.
- **Measured on one compute die of an MI250X (CDNA 2)**, ROCm 5.4.0, amdgpu 6.3.6, on Tioga (Frontier-matched). `[paper]` Results are therefore tied to that ROCm generation's range-management and LRF policies, both of which are software and could change between ROCm releases. `[inference]`
- **1 GB GPU memory alignment** is a stated platform property that directly sets the range geometry. `[paper]`
- The paper notes HMM "is still in development," so its findings are explicitly a snapshot of a moving target. `[paper]`
- **Contrast point for the cluster:** on MI300A the same vendor removes the entire migration path by making host and device memory physically unified — see `GPU-ISC24-01`, which measures ">65% of the time … spent in page migrations" on discrete GPUs and zero on the APU. The two papers together bracket AMD's unified-memory story: SVM characterises the discrete-GPU cost, MI300A removes it architecturally. No citation link between the two was verified. `[inference]`

## 12.13 Limitations

Author-stated `[paper]`:
1. Performance data limited to DOS ≤ 156 "by the long time needed to gather experimental results."
2. Testing confined to one compute die of the MI250X.
3. BFP/BFS behaviour depends on "input graph and … start node"; a specific random graph (10% edges) was used.
4. Limited application set: "examined over a dozen applications but only included those with complete data across different problem sizes" — eight are reported (STREAM, Conv2d, Jacobi2d, BFS, SGEMM, SYR2K, MVT, GESUMMV).
5. Eviction-policy analysis hampered by limited information about the driver's internals.

Future work the authors name `[paper]`: SVM-aware algorithm design; possible augmentations to SVM's design; SVM-aware library implementations, motivated by the expectation that "various accelerators and devices are expected to interface with Linux HMM."

Observed here, not claimed `[inference]`:
6. **No head-to-head measurement against NVIDIA UVM.** Table 1 is a design comparison drawn from documentation and prior work, not a side-by-side experiment, so claims about relative SVM/UVM performance cannot be made from this paper.
7. **The recommendations are not implemented or evaluated as driver changes** — "reduce range size" and "replace LRF" are proposals, and their benefit is not quantified. This is the natural follow-on work and is exactly what ARIADNE (HPCA 2026) and Forest (ISCA 2025) appear to occupy in the UVM setting; neither was reachable to verify.
8. Analysed from the arXiv preprint rather than the ACM camera-ready (`dl.acm.org` 403 here).

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. Repository grep for the exact/normalised title and "Shared Virtual Memory: Its Design" returned only `domains/gpu_systems/census/ICS_2024.md`. (The census had flagged this paper's GPU centrality as `[TITLE-ONLY]`/UNVERIFIED because no abstract was reachable in STEP B; the arXiv full text **resolves that**: it is a GPU unified-memory characterization study on AMD Instinct hardware.)
- **Gap claim verified from the paper's own text:** "To the best of our knowledge, this work is the first in-depth and comprehensive study of SVM technology," justified by "SVM has a distinct design from UVM, and the insights derived for UVM may not be directly applicable to SVM." `[paper]`
- **Lineage verified from the paper's related work** `[paper]`: prior NVIDIA UVM studies by **Ganguly et al. (2019)**, **Li et al. (2019)**, **Chang et al. (2021)**, **Allen & Ge (2021a, 2021b)** and **Kim et al. (2020)**; oversubscription-degradation studies by **Landaverde et al. (2014)**, **Knap & Czarnul (2019)** and **Yu et al. (2019)**.
- **Verified shared ancestor with SUV:** both this paper and SUV (`GPU-MICRO24-01`) cite **Ganguly et al.** as foundational UVM characterization/prefetching work, and SUV additionally cites **Chien et al.** and **Tyler & Ge** in the same "provide insights into UVM, but not mechanisms" bucket that Allen & Ge occupy here. `[paper]` (both papers' related work) That is a real, citation-grounded connection between the AMD-characterization line and the NVIDIA-mechanism line in this cluster.
- **Complementary:** SUV attacks the semantic blindness of the *NVIDIA* UVM driver with compiler information; this paper diagnoses the analogous blindness in *AMD* SVM as a granularity-and-recency-metric problem. Neither cites the other.
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the object of study is **AMD GPU Shared Virtual Memory** in the ROCm/amdgpu driver, i.e. a GPU unified-memory subsystem, and the measured internals (`cpu_unmap`, `SDMA_setup`, `alloc`, `cpu_update`) are that driver's functions; (b) the fault behaviour being characterised is a **GPU fault storm** — 97–99% duplicate faults arising because thousands of concurrently resident SIMT threads reference the same unmapped page, which is why a CAM filter is needed at all; (c) the cost being paid is migration across the **host↔GPU Infinity Fabric** into **HBM2E**, and the capacity under contention is GPU HBM; (d) the whole taxonomy is indexed by **GPU memory oversubscription** (DOS), a condition defined by GPU HBM capacity.

verdict_basis: the study's subject is the AMD GPU SVM/HMM demand-paging path — its range granularity, single-fault handling, Least-Recently-Faulted eviction and driver cost decomposition — measured on MI250X HBM under GPU memory oversubscription; none of this exists without a GPU unified-memory subsystem and GPU-scale concurrent fault generation.

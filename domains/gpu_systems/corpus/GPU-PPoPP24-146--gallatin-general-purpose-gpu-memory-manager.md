# GPU-PPoPP24-146 — Gallatin: A General-Purpose GPU Memory Manager

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — GPU programming-model runtime: device-side dynamic memory management`
secondary_topics: `lock-free concurrent data structures on GPUs; warp-cooperative (coalesced-group) algorithms; fragmentation and memory utilisation; dynamic graph workloads`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the author-hosted PDF (https://prashantpandey.github.io/uploads/ppopp24-final274.pdf), read in two passes — (a) title/authors/affiliation/venue, motivation and the array-vs-linked-list dichotomy in prior allocators, the van Emde Boas tree and its 64-bit GPU adaptation, the three-tier segment/block/slice hierarchy, warp-cooperative coalescing, the per-SM block buffer, fragmentation and variable-size handling; (b) evaluation — GPU SKU, the baseline allocator families and their variants, the benchmark set including the Orkut graph workload, headline speedups, the memory-utilisation trade-off, repository URLs, related-work venues. PLUS [code] inspection of https://github.com/saltsystemslab/gallatin @ f65a085414527c95c7197b724c90cb9740f105dc. No explicit future-work section exists — recorded as such.`

## 12.1 Bibliographic facts

- Title: **Gallatin: A General-Purpose GPU Memory Manager** [paper].
- Venue: **PPoPP '24** — "29th ACM SIGPLAN Annual Symposium on Principles and Practice of Parallel Programming, March 2–6, 2024, Edinburgh, United Kingdom" [paper].
- DOI: `10.1145/3627535.3638499` [`official-web`, from the publisher landing page; `dl.acm.org` is 403 here and was not dereferenced].
- Authors and affiliation [paper]: **Hunter McCoy** and **Prashant Pandey**, **University of Utah**.
- Artifacts [paper, verbatim]: code `https://github.com/saltsystemslab/gallatin`; benchmarks `https://github.com/saltsystemslab/memmansurvey`; archive `https://zenodo.org/records/10475796`. **Code inspected** at commit **`f65a085414527c95c7197b724c90cb9740f105dc`** [code]. The benchmark repository and the Zenodo archive are `NOT_INSPECTED`.
- Publication type: `ARCHIVAL_MAIN_PAPER`.

## 12.2 Core question (one sentence)

GPU dynamic allocators have all been forced to pick a side — array-based (fast, parallel, but the maximum allocation is capped by a fixed region) or linked-list (any size, but serialising and pointer-chasing) — and the state of the art therefore ships **six and five specialised variants** respectively [paper]; can a **single** allocator using a GPU-adapted **van Emde Boas tree** be simultaneously general-purpose (any size), lock-free, and faster than every specialised variant?

## 12.3 GPU/HPC problem translation

- **Synchronization.** This is the crux. A GPU allocator is hit by up to 2²⁰ concurrent threads [paper, scaling test]; any structure requiring a lock or a multi-word update serialises catastrophically. The paper's design decision follows directly: constrain every vEB node to **64 bits** so that "every vEB node operation" executes "in one atomic operation" [paper], deliberately **sacrificing the theoretical O(log log u) bound** to obtain lock-freedom.
- **Compute.** Allocation cost is dominated by atomic contention, not arithmetic. The countermeasure is warp-level batching (12.6).
- **Memory.** Three concerns at once: external fragmentation (addressed by a total-order successor search over segments), internal fragmentation (addressed by the slice tier), and utilisation (where the design deliberately loses — see 12.13).
- **Scheduling.** The per-SM block buffer ties allocation locality to the **streaming multiprocessor** the requesting warp is running on [paper] — the allocator is aware of where on the chip the caller is.
- **Communication.** Single-GPU, device-side. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- **The GPU's atomic granularity sets the data-structure design.** A 64-bit compare-and-swap is the widest lock-free primitive available per thread; a classical vEB node (summary + min + max + child pointers) does not fit. Hence the paper's node is stripped to a summary bit array only, "removing min/max values" [paper]. The algorithmic structure is chosen by the ISA's atomic width — a textbook example of the hardware dictating the abstraction.
- **Massive concurrency makes even a correct lock-free structure slow if every thread issues its own atomic.** Root cause of the warp-cooperative layer: "When multiple threads in the same warp request an allocation of the same size, we can group these requests and satisfy them simultaneously using a single atomic instruction" [paper]. The 32× reduction in atomic traffic is a direct consequence of SIMT lockstep.
- **The prior art's split** is itself a hardware artefact: arrays are fast on a GPU because they are coalescible and index-addressable; linked lists are slow because pointer chasing is uncoalescible. The paper reports that "the only functioning GPU allocator capable of supporting allocations of any size is the CUDA allocator", which is "often several orders of magnitude slower" [paper].

## 12.5 Mathematical / performance model

- **van Emde Boas tree** over universe `U = {0,…,u−1}`, supporting `insertion(x)`, `delete(x)`, `query(x)`, `succ(x)`, `pred(x)` in **O(log log u)** in the classical form [paper].
- **GPU adaptation** [paper]: nodes constrained to **64 bits**, holding only a summary bit array (one bit per child); min/max removed. The O(log log u) bound is explicitly given up in exchange for single-atomic node operations.
- **Three tiers and their sizes** [paper]:
  - **Segments — 16 MB**, tracked by one segment tree (one bit per segment).
  - **Blocks — 4 KB to 16 MB, power-of-two**, one **block tree per block size**.
  - **Slices — 16 B to 4096 B**; "Each block contains **4096 slices** equally sized to be 1/4096-th of the block size"; a slice malloc/free is "one atomic operation on a 32-bit machine word".
- **Total-order invariant on segments** [paper]: the successor search enforces that "the kth segment can only be allocated if all segments < k are allocated" — this is what bounds external fragmentation.
- **Large allocations** [paper]: served by **predecessor** search from the end of the segment tree, reserving the front for small allocations; "If `treeId ≥ numBlockTrees`, `treeId − numBlockTrees` segments are allocated from the end of the segment tree and returned as one allocation."
- **Block buffer sizing** [paper]: for the smallest slice size the buffer holds "one block pointer for every streaming multiprocessor", **halving at each larger size tier** and floored at four blocks. `[code]` confirms the halving-with-cutoff loop verbatim in `boot_shared_block_container_one_thread` at commit `f65a085`: `max_smid = max_smid/2; if (max_smid < cutoff) max_smid = cutoff;`.
- No closed-form throughput model is given. `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

- **thread**: issues a `malloc`/`free`. For slices, one thread's operation is one 32-bit atomic [paper].
- **warp (the key level)**: `cooperative_groups::coalesced_threads` identifies the subset of active threads requesting the same size; "the leader performs allocation and distributes addresses", amortising the atomic across the group [paper]. `[code]` confirms `cg::coalesced_group warp_team = cg::coalesced_threads();` and `cg::coalesced_group full_warp_team = cg::coalesced_threads();` at four distinct sites in `include/gallatin/allocators/gallatin.cuh`, commit `f65a085`.
- **SM (streaming multiprocessor)**: the block buffer "map[s] streaming multiprocessors to live blocks" [paper]. `[code]` at `f65a085` shows the repository has since refined the key: a comment in `gallatin.cuh` reads "Each pinned slot is keyed by `(smid ^ warp_in_block ^ blockIdx)`" — i.e. the live version keys the pinned slot on SM id **combined with warp and block index**, not on SM id alone. **This is `[code]` evidence about the repository's current state and is explicitly *not* attributed to the paper.** `include/gallatin/allocators/shared_block_storage.cuh` and `include/gallatin/data_structs/smid_ring_queue.cuh` are the corresponding sources.
- **Per-segment hand-out**: blocks are distributed from "a constant-size per-segment **ring queue**" [paper]. `[code]`: `include/gallatin/data_structs/ring_queue.cuh` and `smid_ring_queue.cuh` exist at `f65a085`.
- **GPU**: NVIDIA **A40**, 48 GB DRAM, 10,752 CUDA cores [paper].
- **node / cluster**: single GPU. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- slice allocation, warp-cooperative -------------------------  [paper]
malloc(size):
    warp_team = cg::coalesced_threads()          # threads still active here
    if all threads in warp_team request the same size class:
        leader = warp_team.thread_rank() == 0
        if leader:
            blk = block_buffer[ smid() ]          # per-SM pinned live block
            base = atomicOr(blk.slice_bitmap, mask_for(warp_team.size()))
        base = warp_team.shfl(base, 0)            # distribute to the group
        return base + warp_team.thread_rank() * slice_size
    # otherwise fall through to per-thread path

# --- tier escalation -------------------------------------------  [paper]
get_block(size_class):
    seg = find_formatted_segment(size_class)
    if seg is None:
        seg = segment_tree.succ(0)               # total-order: lowest free
        format(seg, size_class)                  # 16 MB -> blocks
    return seg.ring_queue.pop()

# --- large allocation ------------------------------------------  [paper]
if treeId >= numBlockTrees:
    n = treeId - numBlockTrees
    return segment_tree.pred_alloc_from_end(n)   # contiguous, from the top
```

`[reconstruction]` applies to the code shape and to `atomicOr`/`shfl` spellings. The names `coalesced_threads`, the ring queue, the segment/block/slice tiers, the successor/predecessor searches and the `treeId ≥ numBlockTrees` rule are printed in the paper; `cg::coalesced_threads` is confirmed in `[code]` at `f65a085`.

## 12.8 Real implementation

Repository `https://github.com/saltsystemslab/gallatin` @ **`f65a085414527c95c7197b724c90cb9740f105dc`** [code]. Verified files and symbols only:

- `include/gallatin/allocators/veb.cuh` — the van Emde Boas tree; included by `memory_table.cuh`.
- `include/gallatin/allocators/gallatin.cuh` — header comment reads "Gallatin is a generic vEB-based GPU allocator that allows for individual…"; declares `veb_tree *segment_tree;` and `veb_tree **sub_trees`, the boot kernels `boot_segment_trees(veb_tree **segment_trees, …, int num_trees)` and `boot_shared_block_container_one_thread(allocator*, uint16_t max_tree_id, int max_smid, int cutoff)`, `assert_empty(veb_tree ** segment_trees, int num_trees)`, `using sub_tree_type = veb_tree;`, the sentinel `veb_tree::fail()`, and `static_assert(bytes_per_segment >= biggest*4096);` — the last confirming the paper's 4096-slices-per-block constant at the type level.
- `include/gallatin/allocators/block.cuh`, `memory_table.cuh`, `shared_block_storage.cuh`, `global_allocator.cuh`, `alloc_utils.cuh`, `murmurhash.cuh`, `timer.cuh`.
- `include/gallatin/data_structs/` contains a substantial library built *on* the allocator — `hash_table.cuh`, `extendible_ht.cuh`, `coop_ext_ht.cuh`, `chaining_table.cuh`, `queue.cuh`, `ring_queue.cuh`, `smid_ring_queue.cuh`, `block_queue.cuh`, `fixed_vector.cuh`, `custring.cuh`, `log.cuh`, `dev_host_queue.cuh`. **The repository is broader than the paper**: these dynamic data structures are not part of the paper's evaluation as read, and no claim is made that they are.
- `alloc_utils.cuh` carries a comment about a thread that "initializes a Block/segment/vEB bit and another thread (often on a different …)" — i.e. cross-thread initialisation races are handled explicitly.

`NOT_INSPECTED`: `memmansurvey` benchmark repository; Zenodo archive.

## 12.9 Kernel execution

- **kernel**: Gallatin is a *device-side* allocator — `malloc`/`free` are called from inside user kernels, not from the host. Boot kernels (`boot_segment_trees`, `boot_shared_block_container_one_thread`) run once at initialisation [code, `f65a085`].
- **thread block**: not a first-class level of the allocator; the SM is. (This is unusual and worth noting: the block buffer is keyed on SM, so two blocks resident on the same SM share a pinned block.)
- **warp**: the batching unit, via coalesced groups [paper, code].
- **instruction**: the design's unit of cost is *one atomic*. Slice alloc/free = one 32-bit atomic; each vEB node operation = one 64-bit atomic [paper].
- **scaling**: threads swept from **2⁰ to 2²⁰** [paper].

## 12.10 Memory traffic

- **Atomic traffic is the traffic that matters**, and warp coalescing cuts it by up to the warp width for same-size requests [paper].
- **Locality**: the per-SM block buffer keeps a warp's allocations inside a block that is already "live" for that SM, so consecutive allocations from one SM are contiguous [paper]. "When exhausted, the thread that took the last allocation replaces the block" [paper] — replacement is performed by the unlucky thread, not by a background agent, which keeps the structure lock-free.
- **Fragmentation as traffic**: the total-order segment invariant keeps allocated segments packed at the low end and large allocations at the high end [paper].
- **L1/L2/HBM decomposition**: not reported. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Headline numbers, each with its qualifier [paper, all on **NVIDIA A40, 48 GB**]:

- "up to **374×** faster on single-sized allocations and up to **264×** faster on mixed-size allocations" (vs the baseline allocator families below).
- "up to **254×** faster than the next-best allocator as the number of threads increases" (scaling test, up to 2²⁰ threads).
- Graph workload (**Orkut**, 3.07 M vertices, 234.37 M edges): "**1.5×** faster than the state-of-the-art for bulk insertions" and "**3×** faster than the next-best allocator for all graph expansion tests".

Decomposed causes:

1. **Single-atomic node operations.** Trading the O(log log u) bound for a 64-bit node is what removes locks entirely [paper]. Contention, not asymptotics, is the binding constraint at 2²⁰ threads.
2. **Warp coalescing** amortises one atomic over up to 32 same-size requests [paper, code].
3. **Per-SM block buffer** removes a tree traversal from the common path [paper].
4. **A single structure spanning 16 B to arbitrary sizes** removes the variant-selection problem — the paper's framing is that prior allocators force applications "to select variants that perform poorly under changing workloads" [paper]. Note the shape of the graph result: **1.5×–3×**, far below the 374× microbenchmark figure. The honest reading is that the microbenchmark measures allocator contention in isolation while the graph workload measures an application where allocation is one cost among many.
5. **Where it loses**: memory utilisation **89.1% vs Ouroboros's 98.8%** [paper], attributed to the wavefront/block-buffering strategy — the per-SM pinned blocks are reserved but not fully used. Fragmentation is "slightly above specialized Ouroboros allocators" [paper]. This is a deliberate, stated trade of space for time.

## 12.12 Hardware generation dependence

- Evaluated on a single SKU: **NVIDIA A40 (Ampere), 48 GB, 10,752 CUDA cores** [paper]. No cross-generation study, and CUDA version is not stated in the fetched text — `UNKNOWN`.
- Design dependencies that are generation-portable within CUDA: 32-bit and 64-bit device atomics; `cooperative_groups::coalesced_threads`; `%smid`. All are long-standing CUDA facilities, so the design is not tied to a specific architecture generation.
- The **per-SM** buffer sizing depends on the SM count, which is a per-SKU constant the boot kernel takes as `max_smid` [code, `f65a085`] — so retargeting is parametric, not structural.
- No AMD/HIP port is described. `NOT_IN_PAPER`.

## 12.13 Limitations

The paper gives **no explicit limitations or future-work section**; the following are stated as trade-offs inside the evaluation [paper]:

- **Memory utilisation is materially worse than the best baseline**: 89.1% vs Ouroboros 98.8% — nearly 10% of the device's memory is not available to the application.
- **Fragmentation is slightly worse** than the specialised Ouroboros variants.
- **Single GPU, single SKU** (A40); CUDA version unrecorded.
- **The vEB adaptation gives up its own asymptotic guarantee** — the O(log log u) bound does not hold for the 64-bit node form [paper]. Worst-case behaviour is therefore not characterised.
- The application-level evidence is one graph dataset (Orkut) [paper]; the 374×/264× figures are microbenchmarks and must never be restated without that qualifier.
- `[code]` at `f65a085` shows the repository has advanced past the paper (the `(smid ^ warp_in_block ^ blockIdx)` keying, and a large `data_structs/` library) — so the code is not a faithful snapshot of the evaluated system.

## 12.14 Relation to prior corpus

- **Complementary to the memory/virtualisation cluster**, which is about *host-side* and *driver-side* memory management — `GPU-ASPLOS24-01` (GMLake, VM stitching against fragmentation), `GPU-MICRO24-01` (SUV, static-analysis-guided UVM), `GPU-ICS25-01` (DREAM), `GPU-HPCA24-01` (GRIT page placement). Gallatin is the *device-side* counterpart: allocation issued from inside a running kernel. Notably, **GMLake and Gallatin both attack fragmentation but at opposite ends of the stack** — GMLake stitches virtual memory under a framework's caching allocator; Gallatin restructures the in-kernel allocator itself. Neither cites the other.
- **Complementary to `GPU-PPoPP26-105` (DiggerBees, DFS with hierarchical block-level stealing)** and to the sparse/irregular cluster generally: dynamic, irregular workloads are exactly Gallatin's motivating case.
- **Prior allocators the paper compares against** [paper]: the **CUDA allocator**; **Ouroboros** (variants C-S, C-VA, C-VL, P-S, P-VA, P-VL); **RegEff** (variants C, CF, CM, CFM); **ScatterAlloc**; **XMalloc**; **Halloc** is named in the motivation. None has a corpus file.
- **Cited venue set as the paper reports it** [paper]: **IPDPS, PPoPP, ICS, VLDB, SIGMOD, HPEC** — i.e. a parallel-computing *plus database* citation base, with **no ISCA/MICRO/HPCA presence**. That is a meaningful data point for this cluster's lineage question: PPoPP work of this kind draws on SC/ICS/IPDPS and on the data-management community, not on the architecture community.
- `NO_EXISTING_ANALYSIS`. Not an AI/HPC-import candidate (no ML content).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: **library/runtime**, called from **CUDA** device code. It is a device-side `malloc`/`free` implementation — below the framework, above the driver, and inside the kernel.

verdict_basis: Two of the three load-bearing design decisions are dictated by GPU execution, not by concurrency in general. (i) **The vEB node is shrunk to 64 bits, and its asymptotic bound deliberately abandoned, so that each node operation is a single device atomic** [paper] — a CPU vEB tree has no such pressure and would keep min/max. (ii) **Allocation is warp-cooperative**: `cooperative_groups::coalesced_threads` batches same-size requests from the lanes of one warp behind one atomic and the leader broadcasts the addresses [paper; `cg::coalesced_threads` confirmed at four sites in `gallatin.cuh`, commit `f65a085`] — this construct exists only because SIMT lanes issue their requests in lockstep. (iii) The block buffer is keyed on the **streaming multiprocessor** [paper], i.e. the allocator's locality policy is written in terms of the GPU's physical core. A CPU malloc with per-core arenas is superficially analogous but shares none of these mechanisms: there is no lane-lockstep batching and no 64-bit-atomic constraint forcing the data structure's shape. The contribution is the recovery of a general-purpose allocator under GPU atomic and SIMT constraints.

verdict: `CORE_GPU`

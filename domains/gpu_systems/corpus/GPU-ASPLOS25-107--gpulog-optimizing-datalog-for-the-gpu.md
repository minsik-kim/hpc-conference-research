# GPU-ASPLOS25-107 — Optimizing Datalog for the GPU (GPUlog)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — Irregular GPU workloads (relational algebra, fixpoint iteration, deduplication)`
secondary_topics: `G — sparse/irregular data-structure design; device-side memory management for unpredictable output size; hash tables and atomics on GPU; Thrust/CUB primitive composition; CUDA/HIP portability`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author PDF (https://thomas.gilray.org/pdf/datalog-gpu.pdf) — title/authors/affiliations, abstract, the HISA three-layer structure, the semi-naive fixpoint pipeline (Figure 3) with Full/Delta/New, the n-way join materialisation rewrite, Eager Buffer Management, the strided thread mapping, Algorithm 1 (sorted index construction), Algorithm 2 (hash insertion with AtomicCAS), Algorithm 3 (two-pass join), the named Thrust primitives, RMM memory pooling, evaluation setup (H100/A100/MI250/MI50, CUDA 11.8, cuDF 23.10), dataset edge counts, all baselines, headline numbers, the merge-bottleneck breakdown, the seven stated limitations (§6.5, §6.6, conclusion), and related work. Cross-read against the arXiv preprint (2311.02206v3), which carries the DIFFERENT TITLE "Modern Datalog on the GPU" and the system name GDLog — see 12.1.`

## 12.1 Bibliographic facts

- Published title: **Optimizing Datalog for the GPU** [paper — author PDF]. System name in the published paper: **GPUlog** [paper].
- **Title/name discrepancy, recorded not resolved**: arXiv 2311.02206 (v3) carries the title **"Modern Datalog on the GPU"** and names the system **GDLog** [paper — arXiv HTML read separately]. The author sets match (Yihao Sun, Ahmedur Rahman Shovon, Thomas Gilray, Sidharth Kumar, Kristopher Micinski) and the designs match (HISA, semi-naïve fixpoint, n-way materialisation, eager buffer management), so these are **the same work under two titles**; the census lists both URLs against one row. All facts below are cited from the **author PDF of the published version** unless stated.
- Venue: **ASPLOS 2025**, proceedings volume `30V1` [census: `domains/gpu_systems/census/ASPLOS_2025.md`]. DOI **`10.1145/3669940.3707274`** [census].
- Authors and affiliations [paper]: **Yihao Sun** (Syracuse University), **Ahmedur Rahman Shovon** (University of Illinois Chicago), **Thomas Gilray** (Washington State University), **Sidharth Kumar** (University of Illinois Chicago), **Kristopher Micinski** (Syracuse University).
- Publication type: `ARCHIVAL_MAIN_PAPER`; arXiv 2311.02206 is a `PREPRINT` (under a different title).
- Full text used: `https://thomas.gilray.org/pdf/datalog-gpu.pdf` [paper].
- Artifact: census records `NOT_FOUND_AFTER_SEARCH`. `NOT_INSPECTED`. No source symbols asserted; the names below (`HISA`, `Tmp`, `AtomicCAS`, `Thrust Stable Sort`, RMM) are the paper's own.

## 12.2 Core question (one sentence)

Datalog's fixpoint loop is an *irregular* workload — repeated joins producing outputs of unpredictable size, each requiring deduplication against a growing relation — so what data structure lets a GPU do incremental range-indexed relational algebra without giving up coalesced access, and where does the time actually go once you have it?

## 12.3 GPU/HPC problem translation

- **Compute.** Joins and sorts. The n-way join rewrite exists purely to keep lanes busy: materialising the intermediate "ensur[es] that all available threads are actively engaged in computation, effectively eliminating any idle time" [paper].
- **Memory.** The paper's own final verdict on itself: Datalog performance "remains **memory-bound**" [paper]. HISA's data array is row-major and contiguous specifically "enabling coalesced memory access" [paper].
- **Synchronization.** Hash-table insertion is lock-free via **`AtomicCAS`** (Algorithm 2, line 7 for single-writer semantics; lines 9–14 for the race when tuples share join columns) [paper].
- **Dependency.** The semi-naïve fixpoint is inherently sequential *across* iterations (Delta of iteration `i` feeds iteration `i+1`); parallelism exists only *within* an iteration. The paper does not attempt to break that.
- **Load imbalance.** Addressed by the **strided** thread mapping (each thread takes `threadID + stride × iteration`, stride "32 times the number of stream processors") and by the n-way materialisation [paper].
- **Communication.** Single GPU by design; multi-GPU is explicitly future work [paper]. (A follow-up, "Multi-node Multi-GPU Datalog", ICS 2025, by Shovon et al., appears in this cluster's verdict-only list.)

## 12.4 Why the problem exists (hardware root cause)

- The CPU baseline's bottleneck is stated and measured: in Soufflé-style engines "tuple insertion into the full relation, taking up **77.8%** of the runtime, is a major bottleneck" [paper — arXiv version], because B-tree/trie insertion serialises. A GPU has the threads to fix that, but only if the relation is a *dense, sortable array* rather than a pointer structure.
- That is the whole HISA argument: pointer-chasing index structures are the right asymptotics and the wrong memory system. HISA "combines the algorithmic benefits of incremental range-indexed relations with the raw computation throughput of operations over dense data structures" [paper].
- The second root cause is the one this cluster keeps meeting: **join output size is not known before the join runs**. GPUlog answers it with a **two-pass join** (compute size, allocate, recompute) plus **Eager Buffer Management** to amortise allocation — which is the same allocate-before-you-know problem that `GPU-ICS26-106` (Ocean) answers with HyperLogLog estimation and that `GPU-PPoPP24-…` INFINEL-class work answers with device-side dynamic allocation.
- The third: merging Delta into Full requires a **parallel path merge** over sorted arrays, which needs a buffer of the combined size pre-allocated. The paper measures this at **42% of total runtime** [paper].

## 12.5 Mathematical / performance model

No analytic model. The quantitative structure is a runtime decomposition and a set of design constants [paper]:

- **Merge Delta/Full = 42% of total runtime** — after all the optimisations, the dominant cost is not the join but the deduplicating merge.
- **Recommended stride = 32 × (number of stream processors)** — i.e. 32 tuples in flight per SP.
- **EBM buffer size** = full tuple size + `k` × delta tuple size, trading memory for allocation frequency; worth **up to 3×** on long-tail queries (`usroads`) [paper].
- Sorted index construction is an **LSD radix-style stable sort**: "stable sort based on the least significant column (rightmost) of the tuple and progress[ing] towards sorting by the most significant column (leftmost)" [paper].

## 12.6 Data layout and ownership

**HISA — three layers** [paper]:
1. **Data array** — row-major, contiguous, k-ary tuples; the coalescing layer.
2. **Sorted index array** — tuple indices in lexicographic order with **join columns first**, then the rest. Built by repeated stable sorts, least-significant column first.
3. **Open-addressing hash table** — maps the hash of the join columns to **the smallest index in the sorted index array** for that key; **linear probing**; inserted in parallel under `AtomicCAS`.

The pairing of (3) and (2) is the design's core: the hash gives O(1) entry into a *range*, and the sort makes the range contiguous so the scan is coalesced. Neither alone would do.

- **thread**: owns one outer tuple per stride step; performs one hash lookup then a linear range scan until the join columns diverge [paper, Algorithm 3].
- **warp / block**: `NOT_IN_PAPER` — the paper works at thread-and-stride granularity and delegates the rest to Thrust/CUB. No shared-memory tiling, no warp-shuffle mechanism is described. This is a real gap for kernel-level analysis.
- **relation versions**: **Full / Delta / New**, the classic semi-naïve triple [paper, Figure 3].
- **memory pool**: **RMM (RAPIDS Memory Manager)** on CUDA; **manual pooling on HIP** [paper].
- **GPUs**: H100 PCIe 80 GB, A100 PCIe, AMD MI250 64 GB, AMD MI50 32 GB [paper].
- **node/cluster**: single GPU. Multi-GPU explicitly future work [paper].

## 12.7 Pseudo code

```
# --- HISA index construction ---                          [paper] Algorithm 1
reordered = Thrust_Transform(tuples, join_columns_first)     # lines 1-5
sorted_idx = Thrust_Stable_Sort(reordered, LSD -> MSD)       # lines 7-10

# --- hash table insertion, parallel ---                    [paper] Algorithm 2
h = hash(join_columns(t)); slot = h % TABLE_SIZE
while true:                                                  # linear probing
    old = AtomicCAS(table[slot].key, EMPTY, h)               # line 7
    if old == EMPTY or old == h:
        AtomicCAS-update(table[slot].value, min_index)       # lines 9-14
        break
    slot = (slot + 1) % TABLE_SIZE

# --- two-pass join ---                                     [paper] Algorithm 3
for i in range(threadID, |outer|, stride):        # stride = 32 x num_SPs
    start = hash_lookup(inner.table, join_cols(outer[i]))     # pass 1: O(1)
    j = start
    while join_cols(inner.sorted_idx[j]) == join_cols(outer[i]):   # pass 2: range scan
        emit(outer[i], inner[j]); j += 1
# (run once to COUNT, allocate, then run again to WRITE)

# --- semi-naive fixpoint ---                               [paper] Figure 3
while Delta not empty:
    New   = relational_algebra(Delta, Full)
    Delta = New - Full                 # set difference, via sort + unique
    Full  = Thrust_Path_Merge(Full, Delta)    # 42% of runtime
    New   = {}
```

`HISA`, `Full`/`Delta`/`New`, `AtomicCAS`, `Thrust Transform`, `Thrust Stable Sort`, `Thrust Path Merge`, the stride rule and the two-pass join are all the paper's [paper]. `hash_lookup`, `emit`, `TABLE_SIZE` are `[reconstruction]` names.

## 12.8 Real implementation

`NOT_INSPECTED`. Census records `NOT_FOUND_AFTER_SEARCH` for an artifact; none was located here. **No source symbols are asserted.**

Library-level facts stated by the paper [paper]: **Thrust** `Transform`, `Stable Sort` and `Path Merge`; **`AtomicCAS`**; **RMM (RAPIDS Memory Manager)** on CUDA with manual pooling on HIP; **CUDA Toolkit 11.8**; **cuDF 23.10** (as a baseline, not a dependency). A HIP port exists and is evaluated.

## 12.9 Kernel execution

kernel → grid-strided thread loop over the outer relation → per-thread hash probe + range scan. The notable *absence* is warp-level cooperation: the design is thread-parallel and library-composed, not warp-cooperative. Everything that is normally warp-level in a GPU sparse kernel (shuffle reductions, shared-memory staging, cooperative fragment loads) is delegated to Thrust/CUB primitives. That makes GPUlog a **data-structure-and-pipeline** paper rather than a kernel-microarchitecture paper — which is worth recording precisely, because it is the opposite end of this cluster from DiggerBees (`GPU-PPoPP26-105`), which is all protocol and no library.

## 12.10 Memory traffic

- **Coalescing** is the explicit purpose of HISA's row-major dense data array [paper].
- **The two-pass join doubles the read traffic** over the outer relation: "Unpredictable output sizes force compute-then-allocate-then-recompute pattern" [paper, limitation 5]. This is the price of not having device-side resizable allocation.
- **The merge dominates**: path merge over Full+Delta requires a pre-allocated combined-size buffer and costs **42% of runtime** [paper, §6.5].
- **EBM** removes per-iteration allocation at a memory cost (arXiv version quantifies ≈**1.35× memory overhead for up to 3× speedup**; the published PDF states the 3× on `usroads` without the 1.35× figure — the 1.35× is therefore cited as `[paper — arXiv version]`).
- No L1/L2/HBM breakdown. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

**Setup, all qualifiers carried** [paper]: **NVIDIA H100 PCIe 80 GB** + 64-core AMD EPYC 7713; **NVIDIA A100 PCIe** + 32-core Intel Xeon Gold 6338; **AMD MI250 64 GB** (dual EPYC 7713) and **AMD MI50 32 GB** (dual EPYC 7742). **CUDA 11.8**, **cuDF 23.10**, HIP backend. Datasets with edge counts: `com-dblp` 1.91B, `fe_ocean` 1.67B, `vsp_finan` 910M, `Gnutella31` 884M, `fe_body` 156M, `SF.cedge` 80M — from SNAP, SuiteSparse and road networks; plus program-analysis benchmarks `httpd`, `Linux`, `PostgreSQL`.

Baselines [paper]: **Soufflé** (CPU, compiled to C++, gcc -O3, 32 cores), **GPUJoin** (GPU join for reachability), **cuDF v23.10**.

Results [paper]:
- **45× over Soufflé** on PostgreSQL CSPA (H100 vs EPYC 7543P). Across CSPA: `httpd` **37.2×**, `Linux` **34.5×**, `PostgreSQL` **44.9×**.
- **5–6× over GPUJoin** on reachability (`fe_body` 6×).
- **7× over cuDF 23.10** on Same Generation.
- GPUlog avoids OOM on graphs where GPUJoin and cuDF fail [paper, Tables 2–3].
- **3× from Eager Buffer Management alone** on the longest-tail query (`usroads`).

Decomposed cause:
1. **Replacing serialised B-tree/trie insertion with sort+merge over dense arrays** — the structural win against Soufflé, and the reason the CPU-vs-GPU gap is 35–45× rather than the ~10× a raw-throughput argument would predict.
2. **HISA's hash+sorted-range pairing** — O(1) entry into a coalesced range scan.
3. **n-way materialisation** — removes lane idling in multi-join rules.
4. **EBM** — removes per-iteration allocation (3× on tail queries).
5. **Working against all of it**: the 42% merge cost and the doubled outer-relation read from the two-pass join.

## 12.12 Hardware generation dependence

- **Four GPUs across two vendors** (H100, A100, MI250, MI50) [paper] — strong coverage for this cluster.
- **But the cross-vendor result is a negative one**, and honestly reported: the HIP port does not match CUDA "due to missing libraries such as RMM", and on MI250 "only half of the compute resources … can be utilized" because of the dual-chiplet packaging when running as a single GPU [paper]. This is one of the clearest statements in this corpus that **CUDA-ecosystem library availability, not the ISA, is what makes a GPU port portable**.
- No MMA, no matrix unit, no precision-specific feature. Generation dependence is via Thrust/CUB and RMM, i.e. software.

## 12.13 Limitations

Stated by the paper [paper]:
1. **Single GPU**; multi-GPU/multi-node is future work.
2. **HIP performance gap** (missing RMM equivalent).
3. **MI250 dual-chiplet underutilisation** — half the compute unused in single-GPU mode.
4. **Merge bottleneck** — 42% of runtime; path merge needs a pre-allocated combined-size buffer.
5. **Two-pass join cost** — unpredictable output size forces compute-then-allocate-then-recompute.
6. **No monotonic aggregation** yet.
7. **Deduplication overhead** still measurable; workload remains memory-bound.

## 12.14 Relation to prior corpus

- **Shares its central hardware problem with `GPU-ICS26-106` (Ocean)**: both must allocate a GPU buffer for an output whose size is unknown until the computation runs. Ocean *estimates* it probabilistically (HyperLogLog, 0.3–1.2% overflow, fallback kernel); GPUlog *computes it exactly* with a two-pass join and names that as limitation 5. **These are two different answers to the same GPU constraint, published one year apart in different communities, apparently without contact.** That is one of this cluster's more useful cross-paper observations.
- **Precursor to** "Multi-node Multi-GPU Datalog" (ICS 2025, Shovon et al.), a verdict-only row in this cluster's ledger — the same group taking the explicitly-stated future work.
- **Contrast with** `GPU-PPoPP26-105` (DiggerBees): both are irregular graph-shaped GPU workloads, but GPUlog composes library primitives (Thrust/CUB/RMM) while DiggerBees writes a warp-level stealing protocol from atomics and fences. Opposite ends of the implementation-style spectrum within the same bottleneck class.
- No matrix unit involved — belongs with Ocean, Mille-feuille, Trojan Horse and DiggerBees on the **non-matrix-unit** side of this cluster.
- `NO_EXISTING_ANALYSIS`. `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`; an ASPLOS 2025 paper could plausibly appear there — `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`, nothing asserted.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The contribution *is* a data-structure redesign forced by GPU memory behaviour. CPU Datalog engines already have the right asymptotics with B-trees and Bries; HISA replaces them with a dense row-major array plus a sorted index plus an open-addressing hash table **specifically because pointer-chasing does not coalesce and lock-based insertion does not scale past 8–16 threads**, while sort/merge/scan do. Three further mechanisms are GPU-only: lock-free hash insertion under **`AtomicCAS`** with linear probing; the **grid-strided** thread mapping with a stride tied to the stream-processor count; and the **two-pass join with Eager Buffer Management**, which exists solely because a GPU kernel cannot grow an allocation mid-flight. The paper's own cross-vendor finding — that the HIP port suffers for want of **RMM** — is further evidence that the contribution lives in the GPU memory-management layer, not in the algorithm.

**Bottleneck classes claimed and established** (compute / memory / dependency / synchronisation / load imbalance):
- **Memory — claimed and established.** Coalescing is HISA's stated design goal; the 42% merge measurement and the paper's own "remains memory-bound" conclusion establish where the traffic is.
- **Synchronisation — claimed and established.** Lock-free `AtomicCAS` insertion replaces the CPU engine's serialised insertion, which the paper measures at 77.8% of CPU runtime.
- **Load imbalance — claimed and established.** The n-way materialisation rewrite is introduced explicitly to remove idle threads, with the `Tmp(b,x)` rewrite shown concretely.
- **Compute — secondary.** Raw throughput is assumed, not argued.
- **Dependency — acknowledged, NOT addressed.** The semi-naïve fixpoint's cross-iteration dependency is left intact; parallelism is intra-iteration only. The paper does not claim otherwise.

verdict: `CORE_GPU`

# GPU-HPCA26-01 — HDPAT: Hierarchical Distributed Page Address Translation for Wafer-Scale GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `C — GPU address translation / TLB / page-walk hierarchy` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `D — multi-GPU / multi-chiplet memory management; wafer-scale and MCM GPU organization`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background (wafer-scale GPM organization, mesh, per-GPM translation hierarchy, centralized IOMMU); characterization observations O1-O4 (Figs. 3-8); design (concentric hierarchical caching, clustering and rotation with the two modulo rules, Redirection Table, proactive PTE delivery, translation flow); scope statement on migration/shootdown; evaluation setup (Table I config, Table II 14 benchmarks); baselines incl. Trans-FW, Valkyrie, Barre Chord, ideal IOMMU; results (Figs. 14-17); ablation (component contributions Fig. 15, prefetch depth Fig. 18, redirection table vs TLB Fig. 19, page size Fig. 20, GPU config Fig. 21, wafer scaling Fig. 22); area/power; limitations; related work. Read via two targeted full-text passes over the sarchlab.org PDF.`

## 12.1 Bibliographic facts

- Title: *HDPAT: Hierarchical Distributed Page Address Translation for Wafer-Scale GPUs* `[paper]`
- Authors: Daoxuan Xu (William & Mary), Ying Li (William & Mary), Yuwei Sun (UIUC), Jie Ren (William & Mary), Yifan Sun (William & Mary) `[paper]`
- Venue: HPCA 2026, main conference `[official-web, via census/HPCA_2026.md — https://2026.hpca-conf.org/track/hpca-2026-main-conference]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- DOI: `UNKNOWN` — not retrieved; none asserted.
- Full text used: https://sarchlab.org/hdpat_hpca_2026.pdf (group-hosted PDF; sarchlab is Yifan Sun's group, the same group that maintains MGPUSim/Akita) `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` for an HDPAT-specific repository → `NOT_INSPECTED`. (The simulator MGPUSim is public, but no HDPAT branch/commit was located, so no code claim is made.)

## 12.2 Core question (one sentence)

A wafer-scale GPU is dozens of GPU Processing Modules on a mesh with a single CPU-hosted IOMMU at the centre; when every GPM's local translation hierarchy misses, all those misses converge on that one IOMMU across a multi-hop network — can the *already present but underused* per-GPM GMMUs be turned into a distributed, geometry-aware translation cache so the IOMMU stops being the serialisation point? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory / translation.** Primary axis: translation *throughput* and *latency* rather than data placement. The paper explicitly excludes page migration from scope. `[paper]`
- **Communication.** Central to the mechanism: mesh topology (768 GB/s per link, **32 cycles per hop**) means translation cost is a function of *hop count*, and hop count is a function of a GPM's physical position on the wafer. `[paper]`
- **Compute.** 48 GPMs × 32 CUs at 1.0 GHz generate the concurrency that overwhelms 16 IOMMU walkers; Figure 4 shows ~700 pending translation requests in SPMV at 48 GPMs versus a minimal backlog on a 4-GPM MCM. `[paper]`
- **Scheduling.** Only as a modelling assumption: "our experiments evenly partition both memory buffers and kernel threads among the GPMs." `[paper]`
- **Synchronization.** Deliberately out of scope: no GPU-to-GPU page migration, therefore no page shutdown, therefore TLB shootdown is limited to memory-free and is not evaluated. `[paper]` This is a real scope boundary, not an omission (see 12.13).

## 12.4 Why the problem exists (hardware root cause)

The paper's four observations are the root-cause chain, and they are unusually well separated.

1. **O1 — the centralised IOMMU is a hard throughput wall.** "Conventional IOMMUs handle 1–4 GPUs adequately, wafer-scale systems generate translation requests that overwhelm the IOMMU." `[paper]` The baseline IOMMU has **16 page-table walkers at 500-cycle latency**; the latency breakdown (Figure 3) shows "pre-queue delay constitutes the largest single component" for SPMV — i.e. the dominant cost is *waiting to be walked*, not walking. Two different idealisations (1-cycle IOMMU latency; 4096 walkers at unchanged latency) give **5.45× and 4.96×** speedup respectively `[paper]`, which is the paper's evidence that latency reduction and parallelism increase are near-interchangeable remedies — the signature of a queueing bottleneck.
2. **Scaling the walker count is not available.** "Physical constraints (e.g. die size, energy) prevent simply scaling up the number of page table walkers in proportion to the increased GPM count." `[paper]`
3. **O2 — wafer geometry creates a translation-service gradient.** "Centrally located GPMs exhibit lower execution times"; central GPMs finish **2–4% faster** because they are fewer hops from the CPU-hosted IOMMU, while peripheral GPMs "incur significantly higher hop counts." `[paper]` The consequence the paper exploits: central GPMs are *underutilised*, so they are the natural place to put translation caches.
4. **O3 — translation reuse exists but with wildly varying reuse distance.** AES and RELU trigger one IOMMU request per page; BT and FWT re-request repeatedly; reuse distances span **10 to >100k** accesses. `[paper]` The authors draw the design consequence explicitly: DRAM-based caching with LRU may be suboptimal for this distribution.
5. **O4 — translation requests have spatial locality.** "10% to 30% of future translation requests target virtual addresses in close proximity," strongest in AES, FWS and MM. `[paper]` This licenses PTE prefetching.

The composite root cause: a translation architecture designed for a single IOMMU serving a handful of GPUs, placed on a substrate where request concurrency scales with GPM count and service latency scales with physical distance.

## 12.5 Mathematical / performance model

No closed-form performance model. The design's one piece of real mathematics is the placement function that decides *which* GPM caches a given PTE `[paper]`:

```
ID_cluster = VPN mod  N_c            # which quadrant-based cluster   [paper]
ID_local   = floor(VPN / N_c) mod N_g   # which GPM inside that cluster  [paper]
```
with the invariant that "HDPAT enforces that each PTE appears exactly once per concentric layer." `[paper]` The wafer is partitioned "into four quadrant-based clusters to keep each caching layer within one hop of the next inner layer." `[paper]`

- **C** = the maximum number of caching attempts before the request reaches the IOMMU; **C = 2** is the default, tunable via driver/firmware. `[paper]`
- **Rotation**: with C = 2, "the cluster and local ID counting begin from the GPM located 180 degrees from the original starting point," which the paper states "ensures that there is always a nearby chiplet that can provide translation caching" regardless of the requester's quadrant. `[paper]`
- **Prefetch depth**: when the IOMMU walker resolves VPN *N*, it also fetches PTEs for **VPN *N* … *N*+3**. `[paper]`
- **Redirection Table**: 1024 entries, LRU, holding only {process ID, VPN, GPM ID}; the paper argues it is "nearly twice as space-efficient" than a TLB because a TLB also stores additional metadata. `[paper]`

## 12.6 Data layout and ownership

- **thread → warp → CU:** 32 CUs per GPM at 1.0 GHz. `[paper]`
- **GPM (the chiplet, and the unit of everything in this paper):** its own L1 vector/scalar/instruction caches (16 KB, 4-way), L2 (4 MB, 16-way), L1 TLB (1 set, 32-way, 4 cycles), L2 TLB (64 sets, 32-way, 32 cycles), a **Cuckoo filter**, a last-level TLB, a **GMMU with 8 page-table walkers at 100 cycles × 5 levels = 500 cycles**, and **8 GB HBM**. `[paper]` Each GPM is described as "an independent GPU with multiple Compute Units and a two-level cache hierarchy." `[paper]`
- **Concentric layer (HDPAT's new ownership tier):** GPMs are grouped "into concentric layers based on their distance from the central IOMMU," and each layer holds at most one copy of any PTE. `[paper]` This is the paper's structural novelty — ownership of a translation is assigned by a hash of the VPN *and* by ring position, so a peripheral GPM's miss walks inward layer by layer.
- **Cluster:** four quadrant-based clusters per layer, chosen so each caching layer is within one hop of the next inner layer. `[paper]`
- **Wafer / IOMMU:** the CPU sits at the network centre, holds the global page table, and owns the 1024-entry Redirection Table. `[paper]`
- **Memory model:** "zero-copy memory management model." `[paper]` Memory buffers and kernel threads are evenly partitioned across GPMs in the experiments. `[paper]`

## 12.7 Pseudo code

Structure names, the two modulo rules, C, prefetch depth and the flow are `[paper]`; statement-level shape is `[reconstruction]`.

```
translate(vpn, requester_gpm):                              # [paper]: flow text
  # 1. local hierarchy
  hit = L1_TLB -> L2_TLB -> CuckooFilter -> LL_TLB -> GMMU_walkers   # [paper]
  if hit: return

  # 2. peer (concentric) caching, C attempts, issued CONCURRENTLY
  targets = []
  for layer in concentric_layers(C=2):                      # [paper]
      c = vpn mod  N_c                                      # [paper]
      l = (vpn / N_c) mod N_g                               # [paper]
      targets.append(gpm_of(layer, cluster=c, local=l, rotation=layer))  # [paper]
  # "sent concurrently to all concentric layers, and the earliest response is returned"  [paper]
  r = race(query(t, vpn) for t in targets)
  if r.hit: return r

  # 3. IOMMU
  if RedirectionTable.contains(vpn):                        # [paper] 1024 entries, LRU
      redirect to the recorded GPM      # avoids a redundant page-table walk  [paper]
  else:
      pte = IOMMU_walk(vpn)                                 # [paper] 16 walkers, 500 cyc
      prefetch PTEs for vpn+1 .. vpn+3                      # [paper] O4-driven
      push pte and prefetched PTEs to the inner/middle-layer auxiliary GPMs  # [paper]
      RedirectionTable.insert(vpn -> gpm_ids)               # [paper]
  return pte
```

## 12.8 Real implementation

- Simulated in **MGPUSim**, chosen because it "has built-in high-fidelity modeling of the address translation process." `[paper]` The PDF is hosted by sarchlab.org, the group that develops MGPUSim/Akita — so the simulator is a first-party tool for these authors. `[official-web]`
- **Redirection Table** cost, at 7 nm: **0.034 mm², 0.16 W**, i.e. **0.02% area and 0.09% power** relative to the CPU tile (141.2 mm², 170 W TDP). `[paper]`
- **Cuckoo filters** are stated to be already present in the baseline (attributed to prior work), so no additional area is quantified for them. `[paper]`
- No HDPAT source repository was located → no commit hash, file path or symbol is asserted; `NOT_INSPECTED`.

## 12.9 Kernel execution

HDPAT does not modify kernels: "existing GPU applications run without modifications, as the underlying runtime and driver manage the mapping of data and kernel threads across GPMs." `[paper]` The execution-level effects are:

- A remote translation becomes a **concurrent multicast race** rather than a single long trip: requests go to all concentric layers at once and the earliest response wins. `[paper]` This converts a latency problem into a bandwidth problem, which the mesh can absorb — measured extra network traffic is **0.82%**. `[paper]`
- Warps that would have queued behind the IOMMU's 16 walkers instead hit a peer GPM's GMMU. **42.1% of translations are offloaded** from the IOMMU, and **58% of non-cold requests** are served from peer GPM caches. `[paper]`
- Translation round-trip time drops **41% on average**. `[paper]`

## 12.10 Memory traffic

Path per GPM: register ↔ L1 (16 KB) ↔ L2 (4 MB) ↔ local HBM (8 GB, 1.23 TB/s aggregate) ↔ **mesh (768 GB/s per link, 32 cycles/hop)** ↔ peer GPM HBM or the central CPU/IOMMU. `[paper]`

HDPAT adds two new traffic classes on the mesh — peer translation queries (multiplied by C, raced) and pushed PTE deliveries — and removes IOMMU-bound traffic. Net measured overhead: **0.82% additional traffic**. `[paper]` Prefetch accuracy is **65.55%** at depth 4. `[paper]` The design's key efficiency claim is that a Redirection Table hit avoids a *redundant page-table walk* entirely — i.e. it removes page-table memory references, not just latency. `[paper]`

## 12.11 Why it is faster/slower (decomposed)

The ablation (Figure 15) is the clearest part of the paper and it decomposes the 1.57× cleanly `[paper]`:

| Increment | Speedup |
|---|---|
| Routing-based caching (check GPMs along the route) | no improvement — "repeated attempts penalty" |
| Concentric caching alone | marginal |
| Distributed caching, unbalanced | 1.08× |
| + clustering and rotation | 1.13× |
| + redirection table | 1.18× |
| + prefetching | 1.17× |
| **All combined (HDPAT)** | **1.57×** |

Causal reading:
1. **Naïve peer caching fails** because each extra hop-and-probe adds latency without raising hit probability — the paper measures this as "no improvement" for routing-based caching. `[paper]` The fix is *concurrency* (race all layers) plus *determinism* (a VPN maps to exactly one GPM per layer), which is what clustering gives.
2. **Rotation fixes a geometric unfairness.** Without it, a GPM's nearest cache depends on which quadrant it sits in; rotation guarantees every GPM has a nearby caching source. `[paper]`
3. **The Redirection Table removes duplicate walks, not duplicate latency.** It is the only component that can make the IOMMU skip a walk it would otherwise perform. At equal area it beats a 512-entry TLB by **1.27×**, for two named reasons: it stores only process ID + VPN + GPM ID, and it has no MSHR blocking. `[paper]`
4. **Prefetching converts O4's spatial locality into pre-placed capacity**, 65.55% accurate at depth 4; depth 1 gives 1.40×, depth 4 gives 1.57×, depth 8 gives 1.59% more (1.59×) at increased GMMU pressure. `[paper]`
5. **Per-benchmark spread is explained by reuse distance (O3).** PR reaches **5.1×** (strong temporal reuse); MT gains almost nothing (**<1.15×**) because its reuse distances exceed cache capacity; BT reaches 1.85× from spatial locality captured locally. `[paper]`
6. **It is orthogonal to page-size optimisation**: ~50% advantage maintained from 4 KB to 32 KB pages. `[paper]`
7. **It scales with the memory system, not against it**: 1.49× geomean on a 7×12 wafer; per-GPU-model, 1.57× on MI100-class, 1.47–1.50× on MI200/MI300-class, **2.36–2.52× on H100/H200-class** — the paper's reading is that larger memory systems benefit more. `[paper]`

## 12.12 Hardware generation dependence

- **Requires a wafer-scale / many-chiplet GPU** where each chiplet already has its own GMMU with page-table walkers. The whole idea is repurposing those. `[paper]`
- **Requires a centralised IOMMU holding the global page table** as the fallback, plus the ability to add a 1024-entry Redirection Table beside it. `[paper]`
- **Requires GMMUs able to serve peer translation requests** — i.e. a GMMU must accept a query from another GPM, which is not a stock capability. `[inference]`
- **Requires a mesh NoC** with enough spare bandwidth to absorb C-way raced queries; measured overhead 0.82% at 768 GB/s per link. `[paper]`
- Assumes the **Cuckoo filter** stage already exists in the per-GPM hierarchy (attributed to prior work). `[paper]`
- Assumes **zero-copy** memory management and **no GPU-to-GPU page migration**. `[paper]` A generation that introduces wafer-scale page migration would require the shootdown analysis the paper explicitly omits.
- Generalisation is characterised across MI100/MI200/MI300 and H100/H200-class configurations and across 7×7 and 7×12 wafers. `[paper]`

## 12.13 Limitations

Author-stated `[paper]`:
1. **Page migration out of scope**, hence no page shutdown; the only stated shootdown need is freeing memory, judged negligible and not evaluated. This is the largest scope boundary: a wafer-scale system that does migrate pages would need cross-layer PTE invalidation, and the paper describes no coherence protocol for its distributed PTE copies.
2. Benchmarks were scaled to fit the simulator; a "size invariance" check (Figure 13) is offered as justification for using smaller problems as proxies.
3. **LLM workloads not evaluated**; the authors acknowledge modern LLM footprints dwarf the evaluated 8 MB–2,048 MB range and argue the suite still stresses the memory system.
4. Clustering/rotation complexity is asserted to be "straightforward" via precomputed tables and bit operations, with no formal critical-path analysis.
5. Redirection table fixed at 1024 entries with LRU only; no table-size sweep or replacement-policy comparison.

Observed here, not claimed `[inference]`:
6. **No cache-coherence semantics for the distributed PTEs.** The one-copy-per-layer invariant is a *placement* rule, not a coherence protocol; correctness under any PTE mutation (permission change, migration, unmap) is unaddressed because migration is excluded.
7. **C = 2 is a default, not a swept parameter.** The paper states C is tunable and explains why 2 balances caching-GPM count against proximity, but no C-sweep figure is reported.
8. Single simulator, developed by the same group — no cross-simulator or hardware validation.

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. Repository grep for the exact/normalised title and "Hierarchical Distributed Page Address Translation" returned only `domains/gpu_systems/census/HPCA_2026.md`.
- **Lineage verified from HDPAT's own related work** `[paper]`:
  - **Bhattacharjee et al.** — shared last-level TLB across CPU cores; HDPAT positions itself as extending TLB sharing to multi-GPU with hierarchical geometry.
  - **Trans-FW** (Li et al.) — remote forwarding via the page-walk queue; HDPAT's stated delta is inter-GPU hierarchy, clustering and prefetch rather than intra-GPU reuse. Compared quantitatively.
  - **Valkyrie** — exploits inter-TLB locality but misses still reach the IOMMU. Compared quantitatively.
  - **Barre Chord** (ISCA 2024) — page-walk-queue coalescing; HDPAT's delta is concentric caching, rotation and redirection. Compared quantitatively. *This is a verified citation link from HDPAT to a paper on this cluster's own verdict-only list.*
  - **Griffin** — page migration, declared out of scope.
  - **IDYLL** — TLB sharing with spilling; not directly compared, but named; HDPAT claims no spill overhead because it uses a dedicated redirection table.
  - **Cuckoo filter** — reused, explicitly not novel to HDPAT.
- **Competing/complementary within this cluster:** STAR (`GPU-MICRO24-02`) shares HDPAT's strategy of *reclaiming existing translation capacity rather than adding it*, but its contended resource is a MIG-shared sub-entry array inside one chip, whereas HDPAT's is walker throughput across a wafer. Heliostat (ISCA 2025, watchlist) is the third variant of the same strategy — repurposing the ray-tracing accelerator to perform page-table walks; its abstract states the same framing HDPAT uses, that prior work "focused on better utilizing the provided translation bandwidth" whereas the goal is to "fundamentally increase the translation bandwidth." `[official-web: yonsei.elsevierpure.com abstract for Heliostat]` No citation link between HDPAT and Heliostat was verified.
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the resource being repurposed is the **per-GPM GMMU with its page-table walkers**, a GPU MMU structure that exists once per chiplet only because each chiplet is itself a GPU; (b) the bottleneck exists because 48 GPMs × 32 CUs of SIMT concurrency emit translation requests faster than 16 IOMMU walkers can retire them (~700 pending requests in SPMV), a request-concurrency regime produced by the GPU execution model; (c) the placement rule is built on wafer-scale GPU geometry — concentric layers relative to the central CPU/IOMMU, quadrant clusters within one hop, 32 cycles per mesh hop; (d) the assumed memory model is GPU zero-copy with per-GPM HBM, and the evaluated configurations are named GPU products (MI100/MI200/MI300, H100/H200).

verdict_basis: HDPAT's mechanism is the redistribution of GPU page-walk work across per-chiplet GPU MMUs on a wafer-scale GPU mesh, motivated by a request-concurrency-versus-walker-throughput imbalance specific to massively multithreaded GPU execution; a CPU has neither the per-chiplet GMMU to repurpose nor the concurrency that saturates the IOMMU.

# GPU-HPCA24-01 — GRIT: Enhancing Multi-GPU Performance with Fine-Grained Dynamic Page Placement

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `D — multi-GPU memory management / page placement / page migration` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `C — GPU address translation (PTE format extension, page-walk-time updates); UVM page-fault path`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background (multi-GPU UVM, on-touch migration, access-counter migration, page duplication, granularity); three characterization observations; design (Fault-Aware Initiator, PA-Table, PA-Cache, Neighboring-Aware Prediction, PTE scheme bits, full execution flow of Fig. 16); evaluation setup (Table I config, Table II benchmarks); baselines incl. Griffin, GPS, Trans-FW, ideal; results (Figs. 17-19, latency breakdown Fig. 3); sensitivity and ablation (fault threshold, GPU count 2/8/16, 2 MB pages, component contributions Fig. 20); DNN workloads; author-stated limitations; related work. Read via two targeted full-text passes over the public NSF-PAR copy.`

## 12.1 Bibliographic facts

- Title: *GRIT: Enhancing Multi-GPU Performance with Fine-Grained Dynamic Page Placement* `[paper]`
- Authors: Yueqi Wang, Bingyao Li (University of Pittsburgh), Aamer Jaleel (NVIDIA), Jun Yang, Xulong Tang (University of Pittsburgh) `[paper]`
- Venue: HPCA 2024, Session 10B "GPU" `[official-program, via census/HPCA_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- DOI: `UNKNOWN`. The census records IEEE Xplore article id 10476474; `ieeexplore.ieee.org` is unreachable here (HTTP 418) and no DOI string was retrieved. No DOI asserted.
- Full text used: https://par.nsf.gov/servlets/purl/10506536 (NSF Public Access Repository accepted manuscript) `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` → `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

In a multi-GPU system there are three established ways to place a page that more than one GPU touches — migrate it on touch, leave it remote and migrate only after an access counter fires, or duplicate it — and the paper's claim is that the right choice varies not just per application but *per page and per execution phase of that page*, so the question is how to pick per page, per phase, at negligible cost. `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** Per-page residency and replication decisions across N GPU HBMs plus host DRAM, under UVM's universal-pointer model. `[paper]`
- **Communication.** The cost being traded is NUMA distance over NVLink: modelled at **300 GB/s inter-GPU (NVLink-v2)** and **32 GB/s CPU–GPU (PCIe-v4)**. Migration moves bytes once and pays nothing after; remote access pays per access; duplication pays N× bytes plus invalidation on write. `[paper]`
- **Compute.** Warps stall on page faults, on remote-access latency, and on write-collapse invalidation — the paper's Figure 3 decomposes latency into exactly these components per scheme. `[paper]`
- **Scheduling.** GRIT does not schedule work; it reacts to the fault *events* the scheduler's memory accesses generate. `[paper]`
- **Synchronization.** Write-collapse (invalidating all replicas of a duplicated page on any write) is the coherence-like cost that bounds duplication. `[paper]`

## 12.4 Why the problem exists (hardware root cause)

1. **Three schemes, three different hardware costs, no dominant one.** On-touch migration makes access local but, when two GPUs alternate on the same page, produces ping-pong migrations. Access-counter migration (NVIDIA Volta and newer) "establishes the address translation to a remote physical page in its local page table" and counts remote accesses per 64 KB page group, migrating at a threshold of e.g. 256 — so it pays 256 remote accesses plus "frequent page table entry invalidations" before it acts. Duplication gives every reader a local replica but any write triggers page write-collapse and invalidation of all replicas across GPUs. `[paper]`
2. **Sharing behaviour is not a per-application constant.** The paper's Observation 1 identifies two sharing classes — *producer–consumer shared* (GPU A in one interval, GPU B in another; favours on-touch migration) and *all-shared* (several GPUs throughout; favours access-counter migration) — and shows a single page changes class mid-run: "the same page in ST shows the all-shared pattern during intervals 0–5 and becomes the PC-shared pattern during intervals 25–30." `[paper]` A per-application or even per-page-static policy therefore cannot be right for the whole run.
3. **Read/write mix decides whether duplication is viable, and it also drifts.** Observation 2: "Page duplication does not always yield benefits for read-write intensive applications," because "the overheads of page write-collapse can be expensive," and these attributes vary over time within a page. `[paper]`
4. **Detecting all this by polling is too expensive on a GPU.** This is the design-forcing constraint. Periodic monitoring (the paper attributes interval-triggered migration to Griffin's Dynamic Page Classification) needs per-GPU tracking state and cross-GPU communication. GRIT's response is to reuse an event the hardware already generates: "We employ the page fault as an indicator to trigger the page placement scheme change … without incurring additional storage and interconnection overhead." `[paper]`
5. **Page-table walks are a free ride for metadata updates.** GRIT updates its attribute table and the PTE scheme bits *during* the walk that the fault already forces, so the metadata update is not an extra memory access. `[paper]` This is the specific hardware fact that makes the design cheap.

## 12.5 Mathematical / performance model

No analytic model. The decision rule is a small state machine over two observables `[paper]`:

- **Fault counter** per page, 2 bits, values 0–3, incremented on each fault; at a threshold of **4** an interrupt triggers scheme re-evaluation. `[paper]` Fault *type* carries the signal: a local page fault means the page is being touched by multiple GPUs; a page *protection* fault means a write to a shared page. `[paper]`
- **Read/Write bit** per page, 1 bit, set to 1 on first write and sticky thereafter. `[paper]`

Decision at threshold, stated to depend solely on the R/W bit `[paper]`:
```
read-only page   -> Page Duplication
read-write page  -> Access-Counter-Based Migration
private page     -> (never reaches threshold; one initial fault, then local)
```
Grouping rule (Neighboring-Aware Prediction): if **more than half of eight consecutive pages** prefer the same new scheme, they are promoted to a page group with a unified scheme. `[paper]`

PA-Table entry: 45-bit VPN + 1-bit R/W + 2-bit fault counter = **48 bits**, total overhead **0.15% of the application memory footprint**. `[paper]` PA-Cache: 64 entries, 4-way, write-allocate/write-back, indexed by the low 4 bits of the VPN, **352 bytes**, **0.04% of L1 cache area**. `[paper]`

## 12.6 Data layout and ownership

- **thread → warp → CU:** unchanged; GRIT does not touch the kernel.
- **GPU (64 CUs at 1.0 GHz in the model):** owns a local page table into which either a local physical page or a *remote* physical page can be mapped (that remote mapping is exactly what access-counter migration relies on). `[paper]`
- **Page group hierarchy** — GRIT's distinctive ownership unit, encoded in **PTE bits 52–53** `[paper]`:
  - `00` = a single 4 KB page
  - `01` = 8 pages (32 KB)
  - `10` = 64 pages (256 KB)
  - `11` = 512 pages (2 MB)
  When one page inside a group changes scheme, the group is **downgraded** (e.g. a 64-page group becomes eight 8-page subgroups). `[paper]` So the granularity is adaptive in both directions: promote on agreement, split on disagreement.
- **Scheme bits** occupy **PTE bits 9–10**: `01` on-touch migration, `10` access-counter migration, `11` page duplication — carried in both the centralised and the GPU-local page tables. `[paper]`
- **CPU side:** the PA-Table lives in host memory under the UVM driver; the PA-Cache is the hardware accelerator for its lookups. `[paper]`
- **node:** 4 GPUs baseline (2, 8, 16 also evaluated), DRAM sized to **70% of the application's memory footprint**. `[paper]`

## 12.7 Pseudo code

Component names, bit positions, thresholds and the flow of Figure 16 are `[paper]`; statement-level shape is `[reconstruction]`.

```
on_fault(page p, fault_type t):                       # [paper]: Fig. 16 flow
    # (1) metadata update rides the page-table walk
    parallel_with(page_table_walk(p)):                # [paper]
        e = PA_Cache.lookup_or_fill(p.vpn)            # [paper] 64-entry 4-way
        if t == PROTECTION_FAULT: e.rw = 1            # [paper] sticky
        e.fault_count = min(e.fault_count + 1, 3)     # [paper] 2-bit

    if e.fault_count < THRESHOLD(=4):                 # [paper]
        s = read_scheme_bits(centralised_PTE(p))      # [paper] PTE bits 9-10
        if s was set by Neighboring-Aware Prediction:  # [paper]
            apply_scheme(p, s)                        # early adoption, no threshold wait
        else:
            apply_current_scheme(p)
    else:                                             # [paper]
        s_new = DUPLICATION if e.rw == 0 else ACCESS_COUNTER   # [paper]
        write_scheme_bits(centralised_PTE(p), s_new)  # [paper]
        write_scheme_bits(gpu_local_PTE(p),  s_new)   # [paper]
        NeighboringAwarePrediction(p, s_new)          # [paper]

NeighboringAwarePrediction(p, s_new):                  # [paper]
    window = 8 consecutive pages around p              # [paper]
    if count(prefer s_new in window) > 4:              # [paper] "more than half"
        promote_to_group(window, s_new)                # group bits 52-53  [paper]
    # runs in background during page table walks       # [paper]
```

## 12.8 Real implementation

- Simulated: **MGPUSim** (2019), described by the authors as an industry-validated multi-GPU simulator. All three baseline placement schemes were implemented inside it. `[paper]`
- PA-Cache area is derived as 0.04% of L1 cache area; PA-Table overhead as 0.15% of application footprint. `[paper]` No CACTI node is stated for GRIT's structures → `NOT_IN_PAPER`.
- No public artifact was located → no code symbols, file paths or commits asserted; `NOT_INSPECTED`.

## 12.9 Kernel execution

GRIT never enters the kernel → thread-block → warp → instruction path directly. Its entry point is the fault, and its two latency-hiding tricks are execution-level `[paper]`:

1. **Metadata update overlapped with the page-table walk.** The PA-Table/PA-Cache update happens in parallel with the walk the fault already requires, so the GPU is stalled no longer than the walk itself.
2. **Prediction runs in the background** during page-table walks, "avoiding blocking GPU execution," and its result is adopted on the *next* fault for a neighbouring page without that page having to reach the fault threshold. `[paper]`

There is a measurable warm-up cost: BFS shows a "slight performance drop (2%)" because the scheme starts at on-touch migration and must discover a better one. `[paper]`

## 12.10 Memory traffic

Path: register ↔ L1 (16 KB vector / 16 KB scalar / 32 KB instruction) ↔ L2 (256 KB per GPU) ↔ local HBM ↔ **NVLink-v2 at 300 GB/s** to a peer GPU's HBM ↔ **PCIe-v4 at 32 GB/s** to host DRAM. `[paper]` TLBs: L1 32 entries/32-way/1 cycle; L2 512 entries/16-way/10 cycles; GMMU with 8 shared walkers at 100 cycles per level. `[paper]`

GRIT reshapes traffic on the inter-GPU leg by choosing, per page, between bulk migration, per-access remote traffic, and N-way replication traffic plus invalidation traffic. Measured fault reductions at the 4-GPU baseline: **39% fewer faults than on-touch, 55% fewer than access-counter, 16% fewer than duplication**. `[paper]` Figure 3's latency decomposition names the four traffic-cost components explicitly: page-migration, remote-access, write-collapse, page-duplication. `[paper]` Absolute NVLink byte counts are not reported → `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed)

1. **It removes the worst case of each scheme rather than optimising one scheme.** The headline numbers are against *uniform* policies, on 8 applications at 4 GPUs with DRAM at 70% of footprint: **60% over on-touch, 49% over access-counter, 29% over duplication**. `[paper]` Each of those baselines is beaten on the pages where it was pathological — ping-pong for on-touch, 256 remote accesses for the counter, write-collapse for duplication.
2. **Event-driven beats interval-driven.** Against Griffin's Dynamic Page Classification, which "triggers page migration at predefined time interval," GRIT is **27% better** (and 16% against full Griffin including Asynchronous Compute Unit Draining). `[paper]` The cause is latency of detection: a fault is a same-instant signal, an interval boundary is up to one interval late.
3. **Spatial prediction converts a reactive rule into a proactive one.** Component ablation: PA-Table alone **31%**, PA-Table + PA-Cache **47%**, PA-Table + Neighboring-Aware Prediction **44%**; full GRIT 60%. `[paper]` So the cache (removing lookup bandwidth contention) and the predictor (removing the threshold wait) each contribute roughly as much as the base mechanism.
4. **Threshold 4 is where detection accuracy stops paying.** 2 → 53%, 4 → 60%, 8 → 59%, 16 → 48%. `[paper]` Too low misclassifies on noise; too high delays the switch.
5. **Why it is *not* faster in specific cases.** The gap to the `Ideal` bound stays large for ST, BS and C2D, and the paper gives the reason with numbers: those applications have **99%, 56% and 42% shared read-write pages** respectively. `[paper]` GRIT's rule sends read-write shared pages to access-counter migration, which still pays remote accesses — the paper has no scheme that makes a shared read-write page cheap.
6. **Large pages hurt it.** With 2 MB pages the improvement falls from 60% to **23%**, attributed to "more frequent false sharing" and mixed read/write attributes inside one page. `[paper]` This is the direct cost of a per-page R/W bit when the page gets big.
7. **Scaling erodes the advantage.** 2 GPUs: 40/37/11%; 8 GPUs: 38/35/26%; 16 GPUs: 27/26/23% (vs on-touch / counter / duplication). `[paper]` Authors' reason: "as more GPUs increase … pages become more frequently shared," so migration overhead dominates regardless of scheme.

## 12.12 Hardware generation dependence

- **Requires hardware access counters** with remote-access tracking at 64 KB page-group granularity and a migration threshold (the paper cites 256, attributing the mechanism to "NVIDIA Volta and newer"). `[paper]`
- **Requires page duplication support** for read-only pages with write-collapse/invalidation, and **requires remote physical mappings in a GPU-local page table**. `[paper]`
- **Requires free PTE bits**: 2 bits at positions 9–10 for the scheme and 2 bits at 52–53 for the group size. `[paper]` This is an architectural ask, not a software-only change.
- **Requires a hardware PA-Cache** (64 entries, 4-way) in the translation path, updated during walks. `[paper]`
- Evaluated with NVLink-v2 class inter-GPU bandwidth (300 GB/s) and PCIe-v4 host attach (32 GB/s), 4 GPUs baseline. `[paper]` Results are reported as a function of GPU count and page size, so the generation sensitivity is at least partly characterised.

## 12.13 Limitations

Author-stated `[paper]`:
1. Shared **read-write** pages remain unsolved — the residual gap to ideal for ST/BS/C2D is attributed to their 99%/56%/42% shared read-write page fractions.
2. With 2 MB pages, page attributes become mixed within one page, forcing compromise schemes; benefit drops to 23%.
3. Diminishing returns with GPU count (27/26/23% at 16 GPUs).
4. Non-zero overheads: PA-Table 0.15% of application memory; PA-Cache 0.04% of L1 area.
5. Start-up cost: 2% drop on BFS while the scheme is being discovered.

Observed here, not claimed `[inference]`:
6. **Simulation-only** (MGPUSim); the PTE-bit and PA-Cache requirements are not validated in hardware.
7. The decision rule at threshold is a **single bit** (R/W). The characterization identifies producer–consumer vs all-shared sharing classes as distinct and time-varying, but the final rule does not read a sharing-class observable — it routes all read-write shared pages to access-counter migration. This is a simplification the paper does not discuss, and it plausibly explains limitation (1).
8. No **fairness / multi-tenant** analysis; GRIT assumes one application spanning the GPUs.

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. Repository grep for the exact/normalised title, "Fine-Grained Dynamic Page Placement" and first author + distinctive term returned only `domains/gpu_systems/census/HPCA_2024.md`.
- **Principal competing prior work, compared quantitatively in the paper:** **Griffin** (Baruah et al., 2020) — Dynamic Page Classification + Asynchronous Compute Unit Draining; GRIT is 27% better than Griffin-DPC alone and 16% better than full Griffin, with the stated mechanism difference being event-driven vs interval-driven triggering. `[paper]` Also **GPS** (Muthukrishnan et al., 2021) — peer-to-peer publish/subscribe; GRIT 15% better, and GPS is reported to have a "34% higher page oversubscription rate." `[paper]` Also **first-touch** (54% better) and **Griffin-DPC + Trans-FW** (18% better). `[paper]`
- **Verified lineage from the paper's own related work:** **Trans-FW** (Li et al., 2023), **IDYLL** and **SnakeByte** (Li et al., 2023) — the authors' own prior GPU translation work; **CARVE** (Young et al., 2018) for caching remote data in GPU memory; **Thermostat** (Agarwal & Wenisch, 2017) for hot/cold page detection in hybrid memory; **Ganguly et al. (2019/2020)** tree-based neighbourhood prefetching, declared orthogonal and shown to be additive (+23% when combined). `[paper]`
- **Verified author lineage inside this cluster:** Yueqi Wang, Bingyao Li, Aamer Jaleel, Jun Yang and Xulong Tang co-author both GRIT (HPCA 2024) and STAR (MICRO 2024, `GPU-MICRO24-02`). `[paper]` (both author lists) The same first author (Yueqi Wang) appears on **OASIS: Object-Aware Page Management for Multi-GPU Systems** (HPCA 2025), which is the direct successor line for multi-GPU page management in this cluster — that paper is on the watchlist (no public full text reached). `[official-web, via census/HPCA_2025.md]`
- **Downstream in this cluster (not verified as citing GRIT):** the ISCA 2026 multi-GPU page-management cluster — LIBRA (coordinated multi-GPU page prefetcher), "Coarse-Grained Duplication First, Fine-Grained Deduplication Later," and "Reducing Page Faults via Invalidation-based Mapping Propagation" — attacks the same three-way placement trade-off (duplication, deduplication, mapping propagation) that GRIT frames. No citation relationship was verified because those papers' full texts were not reachable. `[inference]`
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the three schemes being arbitrated are GPU-specific mechanisms — UVM on-touch migration, **NVIDIA hardware access counters** with a 64 KB page-group remote-access threshold, and GPU read-only page duplication with write-collapse; (b) the trigger signal is the **GPU page fault / page protection fault** delivered through the UVM driver, and the latency-hiding trick is overlapping metadata update with the **GPU page-table walk**; (c) the cost model is NUMA distance over **NVLink** between peer GPU HBMs; (d) the design consumes spare bits in the **GPU-local and centralised GPU page tables** and adds a hardware PA-Cache in the GPU translation path.

verdict_basis: GRIT arbitrates among three placement mechanisms that exist only in the GPU UVM stack (on-touch migration, GPU access-counter migration, GPU page duplication with write-collapse), triggered by GPU page faults and piggybacked on GPU page-table walks over an NVLink-connected multi-GPU memory hierarchy.

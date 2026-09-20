# GPU-MICRO24-02 — STAR: Sub-Entry Sharing-Aware TLB for Multi-Instance GPU

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `C — GPU caches, TLBs and address translation` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `GPU resource partitioning / multi-tenancy (MIG); GPU MMU and page-walk structures`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background (three-level GPU TLB hierarchy, sub-entry structure, MIG partitioning, page-walk path); characterization of sub-entry utilization under isolation and co-running; design (sequential and stride layouts, AIB, eligibility rules, state transitions, Algorithms 1 and 2); hardware overhead/CACTI; evaluation methodology (MGPUSim modifications, W1–W11 and W12–W18); baselines incl. MASK and four capacity-restructuring alternatives; sensitivity studies (sharing degree, layout, tenant count, 2 MB pages, static partitioning); related work. Read via two targeted full-text passes over the author-hosted PDF.`

## 12.1 Bibliographic facts

- Title: *STAR: Sub-Entry Sharing-Aware TLB for Multi-Instance GPU* `[paper]`
- Authors: Bingyao Li, Yueqi Wang, Tianyu Wang (University of Pittsburgh), Lieven Eeckhout (Ghent University), Jun Yang (University of Pittsburgh), Aamer Jaleel (NVIDIA), Xulong Tang (University of Pittsburgh) `[paper]`
- Venue: MICRO 2024 (MICRO-57), Session 3A "GPU Microarchitecture I" `[official-program, via census/MICRO_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- DOI: `10.1109/MICRO61859.2024.00031` `[publisher-proceedings, via census/MICRO_2024.md]`
- Full text used: https://users.elis.ugent.be/~leeckhou/papers/MICRO2024-STAR.pdf (author-hosted). A second public copy is recorded at https://par.nsf.gov/servlets/purl/10580567 (not fetched; the Ghent copy sufficed). `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` → implementation symbols `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

NVIDIA's Multi-Instance GPU partitions SMs, memory and the lower TLB levels but leaves the last-level (L3) TLB shared across instances; given that each L3 entry is a 16-sub-entry coalesced translation and that co-running tenants evict each other's entries before those sub-entries fill, can two tenants' base addresses be made to *share* one physical L3 entry's sub-entry array? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory / translation.** Primary axis: the effective reach of a fixed-capacity shared last-level TLB under multi-tenancy. `[paper]`
- **Scheduling / partitioning.** MIG is spatial partitioning; STAR is about the one resource MIG failed to partition. The paper reports that in multi-tenant workloads applications lose on average **40%** performance versus running alone, and in workload W1 (three high-MPKI applications) an average **48%** drop. `[paper]`
- **Compute.** Indirect: an L3 TLB miss costs a page-table walk (8 shared walkers, 100 cycles per level in the modelled configuration), stalling the warp's memory pipeline. `[paper]`
- **Communication / synchronization.** `NOT_IN_PAPER` as first-order concerns.

## 12.4 Why the problem exists (hardware root cause)

The root cause is a mismatch between the *granularity of a coalesced TLB entry* and the *lifetime of that entry under interference*.

1. **GPU last-level TLB entries are coarse by design.** In the modelled Ampere-like hierarchy, an L2 or L3 TLB entry holds **16 sub-entries**, each mapping one page; the 16 pages "fall within an aligned range of either 1 MB or 32 MB in size" for 64 KB and 2 MB pages respectively. `[paper]` This coalescing is what gives a 1024-entry L3 TLB its reach: it is effectively 16,384 translations *if* sub-entries fill.
2. **MIG does not partition the L3 TLB.** "The L3 TLB in today's GPUs (e.g. NVIDIA's Ampere generations) remains shared across all instances in MIG-supported GPUs." `[paper]` L1 TLBs (16 entries, TPC-shared) and L2 TLBs (128 entries, GPC-shared) follow the instance boundary; the L3 does not.
3. **Interference truncates sub-entry fill.** This is the paper's central measurement. A tenant's entry is allocated when its first page in the aligned range is translated, and the remaining 15 sub-entries fill only as that tenant touches more pages in the range. Co-runner pressure evicts the entry first. Quantified: for ATAX in W1, "73.4% of its TLB entries are evicted when less than half of the sub-entries are used, even though there are no evictions when run in isolation." `[paper]`
4. **The truncation is access-pattern-dependent, in a structured way.** Under isolation, streaming codes (FFT, FIR) approach full sub-entry utilisation before eviction; a stride code (MT) evicts "most TLB entries … with only four sub-entry occupied"; a blocked code (ST) evicts "nearly 50% of the TLB entries … when only half of the sub-entries are utilized." `[paper]` So the wasted sub-entries are not randomly scattered — they are contiguous-tail waste for sequential fill and periodic holes for strided fill. That structure is exactly what STAR's two layouts exploit.
5. **Naïve capacity restructuring does not work.** Halving sub-entries and doubling sets/ways changes the aligned-range reach or the comparator count; the paper's own alternative "Half-Sub-Double-Way-Para" costs a **78.8% area increase** over the original L3 TLB. `[paper]` The waste must therefore be reclaimed *within* the existing entry geometry.

## 12.5 Mathematical / performance model

No analytic performance model is given. The design is expressed as a re-interpretation of the sub-entry index field `[paper]`:

- Baseline: a 4-bit sub-entry index selects one of 16 sub-entries under a single base address.
- STAR: the index is split into an *n*-bit index plus an **Address Identify Bit (AIB)**. With two-base sharing, each base address receives **8 sub-entries**. `[paper]`
- **Sequential layout:** "we allocate the first half of the sub-entries to the first base address and the second half to the second base address"; the first bit of the sub-entry index is the AIB. `[paper]`
- **Stride layout:** "if the occupied sub-entries show stride access patterns, the sub-entries are interleavedly allocated between the two base addresses according to the stride size"; the first three bits identify sub-entry position and the first bit distinguishes the two addresses. `[paper]`
- A 2-bit **layout field** per entry encodes the state: `00` non-shared, `01` sequential, `10` stride. `[paper]`

**Storage arithmetic, stated by the paper** (per L3 TLB entry): 2 bits layout + 16 bits (1 AIB per sub-entry) + 30 bits second base address + 2 bits valid/dirty for the second base = **50 bits per entry**. `[paper]` CACTI at 22 nm gives **1.4% area** over the original L3 TLB, **+0.3% dynamic power**, **+5.3% leakage power**. `[paper]`

Latency: the second-base comparison adds "conservatively 10 cycles" to the modelled 40-cycle L3 lookup, i.e. 50 cycles when both bases must be checked. `[paper]`

## 12.6 Data layout and ownership

- **thread → warp → TPC:** L1 TLB is 16 entries, 16-way, 1-cycle, shared between the two SMs of a TPC. `[paper]` Ownership here is per-TPC and therefore strictly within one MIG instance.
- **GPC:** L2 TLB, 128 entries, 8-way, 16 sub-entries per entry, 10-cycle, GPC-shared. `[paper]` Still within an instance. Each instance also has its own GMMU with page-walk cache, queue, walker threads and page tables in the authors' model. `[paper]`
- **GPU:** L3 TLB, 1024 entries, 8-way, 16 sub-entries per entry, 40-cycle, **shared across all MIG instances** — the contended resource. `[paper]` Eight page-table walkers per GPU, 100 cycles per level, 128-entry shared page-walk cache. `[paper]`
- **Instance (MIG slice):** 5 GB DRAM per partition slice; L2 data cache 2 MB per slice; instance geometries evaluated are (3g, 2g, 2g) and (3g, 3g). `[paper]`
- STAR's unit of ownership change is **one L3 entry's sub-entry array**, which after sharing is jointly owned by two base addresses that may belong to two different *processes*. `[paper]` The pairing policy deliberately prefers same-process pairing: it "prefer[s] to pair the incoming base address with an existing entry from the same process because access patterns within the same process tend to be similar." `[paper]`

## 12.7 Pseudo code

Mechanism names, field names, eligibility conditions and the two algorithms' roles are `[paper]`; the statement-level shape is `[reconstruction]`.

```
# Lookup (Algorithm 1)                                    # [paper]: role
lookup(vpn, pid):
  e = set[index(vpn)]  ; probe ways                        # [paper]
  if e.layout == 00:                                       # non-shared  [paper]
      compare base vs vpn_base ; select sub_entry[vpn[3:0]]
  elif e.layout == 01:                                     # sequential  [paper]
      sub = vpn_index_low3 ; aib = first_bit                # [paper]
  elif e.layout == 10:                                     # stride      [paper]
      sub = vpn_index_high3 ; aib = first_bit               # [paper]
  hit iff base_match(aib) and sub_entry[sub].valid and AIB field matches   # [paper]

# Insertion (Algorithm 2)                                 # [paper]: role
insert(vpn, pid):
  if base_address_present(vpn): 
      determine layout from current occupancy pattern      # [paper]
      fill sub-entry
  else:
      # sharing eligibility                                # [paper]
      cand = entries with (<8 sub-entries used) and (exactly one base resident)
      cand = prefer_same_process(cand)                     # [paper]
      if cand non-empty: convert to shared (set layout, second base, AIBs)
      else:              LRU_evict_and_allocate()          # [paper]

# Reversion                                                # [paper]
on_fill(e, base b):
  if all 8 sub-entries of b are utilized:
      make entry exclusive to b            # demand signal for that process  [paper]
```

## 12.8 Real implementation

- Simulated, not built: **MGPUSim**, "substantially modified" by the authors to model MIG. `[paper]` Modifications the paper names: per-instance cache/memory/SM configurations for different instance sizes; a shared L3 TLB with sub-entries and L2 TLB sub-entry support; per-instance GMMUs with page-walk cache, queue, walker threads and page tables. `[paper]`
- Hardware cost is an analytical CACTI 22 nm estimate (1.4% L3 TLB area), not an RTL result. `[paper]`
- No public artifact was located (`NOT_FOUND_AFTER_SEARCH`) → no code symbols, commits or file paths are asserted; `NOT_INSPECTED`.

## 12.9 Kernel execution

STAR is invisible to the kernel → thread-block → warp → instruction pipeline; it changes only the hit rate of an L3 TLB lookup that sits behind the L1/L2 TLB miss path. `[paper]` The execution-level consequence the paper measures is a reduction in page-table walks proportional to the L3 hit-rate gain (**+32.8% average L3 hit rate** across workloads), with a per-application performance effect that depends on that application's L2-TLB MPKI class. `[paper]`

Two execution-level details matter for correctness of interpretation:
- The instance's own GMMU and walkers are private, so a shared-L3 miss serialises on *per-instance* walker resources, not on a global one. `[paper]`
- The added second-base comparison lengthens the L3 lookup itself (40 → up to 50 cycles), so STAR trades a longer hit latency for many fewer walks. `[paper]` The net is positive in the reported results but this is the mechanism's intrinsic tension.

## 12.10 Memory traffic

STAR does not move data; it removes *page-table* memory traffic. The relevant path is: L1 TLB (TPC) → L2 TLB (GPC) → L3 TLB (GPU, shared) → page-walk cache (128 entries) → page-table levels in memory via 8 walkers at 100 cycles/level. `[paper]` Every additional L3 hit removes one walk, i.e. up to several dependent memory references. The paper reports the walk reduction as "directly proportional to hit rate gains" rather than as an independent count. `[paper]` No DRAM-bandwidth or interconnect numbers are given for page-table traffic → `NOT_IN_PAPER`.

Page size matters to traffic reach: the default modelled page size is **64 KB**, which the paper identifies as the MIG default. `[paper]`

## 12.11 Why it is faster/slower (decomposed)

1. **Reclaimed sub-entry capacity, not added capacity.** The gain comes from occupying sub-entries that would have been evicted unused. Measured: **+31.4% average sub-entry utilisation at eviction**, **+32.8% average L3 hit rate**. `[paper]`
2. **Layout matching is the enabling trick, and it is separable.** Sequential layout alone gives 19.2% average improvement; stride layout alone 19.7%; the combination 28.7%. `[paper]` The superadditivity is because workload mixes contain both fill patterns, so each layout covers entries the other cannot.
3. **Pairing by process exploits pattern similarity.** Same-process pairing is preferred precisely because two ranges of one application are more likely to share a fill pattern, so the single per-entry layout choice fits both. `[paper]`
4. **Dynamic reversion protects the growing tenant.** When one base fills all 8 of its sub-entries, the entry becomes exclusive to it — the design reads that as a demand signal rather than continuing to constrain it. `[paper]`
5. **Fairness improves, not just throughput.** Per-application degradation under multi-tenancy falls from 40% (baseline) to **26.1%** average. `[paper]` This is the more meaningful metric for a MIG paper, since MIG exists to give tenants predictable service.
6. **Where it is slower / flat.** Low-MPKI mixes gain least (12% for LLL-class W11), because there was little L3 pressure to reclaim. `[paper]` Four-base sharing *loses* against two-base (22.7% vs 28.7%) due to more conflict evictions and longer lookup, at 3.6% area. `[paper]` With 2 MB pages the gain falls to 10% average, because large pages already extend reach. `[paper]` Adding tenants erodes the gain: 14.6% (4 apps), 15.3% (5 apps), 12.1% (6 apps), attributed to smaller per-instance L2 TLBs and intensified L3 contention. `[paper]`

## 12.12 Hardware generation dependence

- **Requires sub-entry (coalesced multi-page) TLB entries** at the last level. The paper anchors this to "NVIDIA's Ampere generations" with 16 sub-entries per L2/L3 entry. `[paper]` A TLB without sub-entry coalescing has no waste of this shape and STAR has nothing to reclaim. `[inference]`
- **Requires MIG-style spatial partitioning in which the last-level TLB is left shared.** `[paper]` If a future generation partitions or replicates the L3 TLB, the motivating interference disappears. `[inference]`
- **Page-size dependent:** the benefit is 28.7% at 64 KB pages (the MIG default per the paper) but 10% at 2 MB. `[paper]`
- **Tenant-count dependent:** evaluated principally at three tenants in (3g,2g,2g) / (3g,3g); benefit declines to 12.1% at six co-runners. `[paper]`
- Area/power figures are for a **22 nm** CACTI model. `[paper]`

## 12.13 Limitations

The paper has no dedicated limitations section. Constraints it does state, in context `[paper]`:
1. Sharing degree capped at two bases to bound comparators and latency; four-base sharing regresses by ~6 percentage points and costs 3.6% area.
2. Layout prediction can be wrong — "the mechanism that determines which layout to use may not accurately predict the most effective layout for the upcoming second base address," and the first base's pattern forces the layout on the second.
3. Lookup latency grows by a conservatively modelled 10 cycles on the 40-cycle L3 path.
4. Benefit concentrated in high-MPKI mixes; LLL mixes gain ~12%.
5. Benefit shrinks with 2 MB pages (10%) and with more tenants (12.1% at six apps).
6. Static way-partitioning alone *degrades* performance by 6.8%; STAR on top of it recovers 14% over static partitioning — i.e. the two are not substitutes.

Observed here, not claimed by the paper `[inference]`:
7. Results are **simulation-only** (modified MGPUSim) with an analytical CACTI area model; there is no silicon or FPGA validation, and MIG behaviour is modelled by the authors rather than measured on a MIG-capable device.
8. Sharing an L3 entry's sub-entry array **across processes** is a cross-tenant structural coupling on a feature whose purpose is isolation. The paper addresses performance interference and prefers same-process pairing, but does not analyse whether cross-tenant sharing of entry state creates a side channel. This is an open question, not a demonstrated flaw.

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. Repository grep for the exact/normalised title, "Sub-Entry Sharing-Aware TLB", the DOI and first author + distinctive term returned only `domains/gpu_systems/census/MICRO_2024.md`.
- **Closest competing prior work, named and compared by the paper:** **MASK** (Ausavarungnirun et al.) — TLB-Fill Tokens and L2-miss-rate-aware entry allocation for multi-application GPUs. STAR's stated distinction: MASK "helps little with TLB sub-entry utilization," because it arbitrates *entries*, not the sub-entry array inside an entry. STAR reports 25% average improvement over MASK. `[paper]`
- **Precursors named for the layout idea:** range TLBs and clustered TLBs (Park et al. 2017; Pham et al. 2012, 2014). STAR's stated distinction is that these assume a single application's consistent sequential/stride pattern, whereas "co-running applications often have varied and unpredictable access patterns." `[paper]`
- **Precursor named for multi-GPU TLB sharing:** Li et al. 2021 (sharing- and spilling-aware TLB for multi-GPU) — "not MIG-specific." `[paper]`
- **Also named:** TLB speculation (Barr et al. 2011; Bhattacharjee 2017); large/super-page management (Ausavarungnirun et al. 2017; Panwar et al. 2018); page-walk optimisation (Barr et al. 2010; Gandhi et al. 2014; Shin et al. 2018), declared orthogonal. `[paper]`
- **Verified author lineage inside this cluster:** Bingyao Li, Yueqi Wang, Aamer Jaleel, Jun Yang and Xulong Tang are co-authors of both STAR (MICRO 2024) and GRIT (HPCA 2024, `GPU-HPCA24-01`) — the same Pittsburgh+NVIDIA group attacking the translation layer and the placement layer in the same year. `[paper]` (both author lists) GRIT's related work additionally cites **IDYLL** and **SnakeByte** (Li et al. 2023) as this group's own earlier GPU-translation work. `[paper]` (GRIT)
- **Complementary, same layer, later:** HDPAT (`GPU-HPCA26-01`) also distributes translation capacity rather than adding it, but across wafer-scale chiplets rather than across MIG tenants; HDPAT's related work names **Bhattacharjee et al.**'s shared last-level TLB as its own ancestor. `[paper]` (HDPAT) No citation link between STAR and HDPAT was verified.
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the reclaimed resource is the 16-sub-entry coalesced last-level GPU TLB entry, a GPU-specific structure whose 1 MB / 32 MB aligned reach exists because thousands of SIMT threads stream over large aligned ranges; (b) the interference being fixed is created by **NVIDIA MIG** spatial partitioning, which partitions SMs, memory and L1/L2 TLBs but leaves the L3 TLB shared — a GPU resource-partitioning artefact with no CPU counterpart; (c) the fill-pattern taxonomy STAR exploits (streaming / stride / blocked sub-entry occupancy) is a property of GPU kernel access patterns across TPC- and GPC-scoped TLBs; (d) the modelled miss cost is a GPU page-table walk on per-instance GMMU walkers.

verdict_basis: STAR's mechanism is defined entirely in terms of GPU sub-entry-coalesced last-level TLB geometry and MIG's failure to partition that structure; on a CPU TLB, which has no 16-page sub-entry array and no MIG-style instance partitioning, there is no underutilised sub-entry capacity to share.

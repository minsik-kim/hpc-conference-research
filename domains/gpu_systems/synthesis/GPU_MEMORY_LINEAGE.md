# GPU_MEMORY_LINEAGE — page walking to multi-GPU remote memory, tested against the citations

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
source: `_LEDGER_memory_virtualization.md` (taxonomy C + D) and the eight deep
analyses it produced, plus `_LEDGER_data_movement_compression.md` §D.6 for the
I/O-path branch.

---

## 0. The expected progression, and what survives contact with the citations

The progression this document was asked to test:

```
page walking -> UVM management -> oversubscription -> migration -> prefetch -> multi-GPU remote memory
```

**Verdict: this is a real *problem decomposition* and a partly real *citation
chain*, but it is not one line.** What the citations support is:

- **A clean, verified chain inside the translation layer** (§2), which does not
  touch UVM policy at all.
- **A clean, verified chain inside the UVM/oversubscription layer** (§3), which
  does not touch translation at all.
- **A verified multi-GPU placement line** (§4) that grows out of the UVM layer,
  not out of the translation layer.
- **No verified citation edge joining the translation chain to the UVM chain.**
  SUV and STAR are the same venue and the same year, attack GPU virtual-memory
  cost at two different layers, and **no citation relationship was verified in
  either direction** `NOT_CITED`.

The prefetch stage in particular is **not a stage**. Prefetch appears as a
*component* inside papers at every other stage — HDPAT's 4-deep PTE prefetch,
SUV's span prefetch, UVM's 60 KB speculative prefetch, GRIT's neighbouring-aware
prediction — and the one paper whose whole subject is multi-GPU page prefetching
(LIBRA, ISCA 2026) has no reachable full text. As an independent stage:
`NOT_ESTABLISHED`.

**Evidence tags** are as defined in
[`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §0.

---

## 1. The finding that reorganises the whole area: the control path, not the data path

This is the cluster's central substantive result, and its strength comes from
being reached **independently on both vendors, by three papers, with no verified
citation link among them**.

| Paper | Vendor / part | Decomposition measured |
|---|---|---|
| [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) DREAM | NVIDIA V100 32 GB, PCIe 3, ConnectX-5/6 | **"Host involvement overheads during the page fault are around 7x higher than the transfer time at 64 KB page size"** `[paper, Fig. 2]`. The slide deck gives 12 µs data migration against 88 µs control path at 64 KB — `[author-presentation]`, **not** paper evidence, and labelled as such |
| [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) SVM study | AMD MI250X (CDNA2), one compute die, ROCm 5.4.0, on Tioga | Driver bookkeeping — `cpu_update`, `SDMA_setup`, `alloc` — **exceeds data movement** under oversubscription `[paper]`. `alloc` dominates under pressure because eviction is charged to it |
| [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) MI300A porting | AMD discrete GPUs, from the application side | **">65% of the time … spent in page migrations: updating GPU tables and copying the data"** `[paper]` |

**Three papers, two vendors, one root cause.** `[inference]` — **no citation links
among these three were verified**; this is a convergence of independent evidence,
recorded as such rather than as a lineage.

The structural reason DREAM gives is worth keeping because it explains why the
cost cannot be tuned away: *"The UVM driver manages separate page tables in GPU
and host memory, serializing fault processing and preventing parallel handling"*
`[paper]`. **A GPU generates faults with thousands of threads in parallel; a
driver consumes them on one CPU control path. The asymmetry cannot be closed by
making the driver faster.**

### 1.1 The three distinct responses

The corpus contains exactly three answers to that finding, and they are
mechanically different rather than incremental.

| Response | Paper | What it does | What it gives up |
|---|---|---|---|
| **Feed the driver better information** | [`GPU-MICRO24-01`](../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md) SUV | Keeps the host driver; supplies compiler-derived access semantics (density, working-set size, per-iteration span) through a patched NVIDIA UVM driver so *fewer faults occur*. 37–100% fewer page faults at 50% oversubscription; 20% geomean speedup even at **zero** oversubscription, i.e. part of the benefit is pure fault-path avoidance | Anything it must label `Unknown` falls back to the baseline access-counter machinery — pointer-chasing codes inherit baseline behaviour |
| **Remove the host from the fault path** | [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) DREAM | Relocates demand paging into kernel code run by warps: `__match_any_sync` over the active mask for intra-warp fault coalescing, GPU threads post RDMA work requests, device-side page-table update, `dream_ptr`, Little's-Law QP sizing. Request concurrency ≈ 84 SMs x 16 warps ≈ 1,344 in flight | Requires Volta-or-newer Tesla-class full-BAR P2P (a T4's 256 MB BAR is explicitly insufficient), a modifiable mlx5 send path, **IOMMU disabled and ACS disabled** `[README]` |
| **Delete the mechanism** | [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) MI300A | Unified *physical* memory: "any memory allocator including `hipMalloc` will allocate unified memory" `[paper]`. There is no migration to make cheap. Production OpenFOAM ported with O(100) lines by deleting `map` clauses and explicit copies | Requires an APU. "Unified memory addressing is not available on all CPU + GPU platforms" `[paper]` |

**The second response's own premise has an expiry date, and the paper says so.**
DREAM's related work names **Grace-Hopper with NVLink-C2C coherence** as the
hardware alternative that would obviate the NIC detour, noting it "requires new
CPU design" `[paper]`. On a coherent CPU–GPU part the RDMA indirection is
unnecessary — so DREAM's value is highest on commodity PCIe-attached systems
`[inference]`. That is the same architectural move as response three, arriving
from the NVIDIA side.

---

## 2. Verified chain: the translation layer

```
Bhattacharjee et al. — shared last-level TLB across CPU cores
        |  [paper] named by HDPAT as its own ancestor
        v
Trans-FW / IDYLL / SnakeByte (Li et al. 2023)        Valkyrie (inter-TLB locality)
        |  [paper] cited and quantitatively           |  [paper] cited and
        |          compared by HDPAT                  |          compared by HDPAT
        v                                             v
Barre Chord (ISCA 2024) — page-walk-queue coalescing, "leverages pending requests"
        |  [paper] HDPAT cites it, describes it, and beats it quantitatively
        v
HDPAT (HPCA 2026) — concentric caching across per-GPM GMMUs, VPN-hashed
                    one-copy-per-layer rule, IOMMU Redirection Table (1024 entries),
                    4-deep proactive PTE delivery
```

Anchor: [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md).
**HDPAT → Barre Chord is the cleanest single citation edge in this area**, and it
points from an in-corpus analysis to a paper the memory cluster holds on its
watchlist with no reachable full text (IEEE Xplore 418). HDPAT also names
**Griffin** (page migration) and declares it out of scope, and reuses a **Cuckoo
filter** stage that it explicitly states is not novel to it.

A parallel, separately-rooted chain:

```
MASK (Ausavarungnirun et al.) — TLB-Fill Tokens, L2-miss-rate-aware entry allocation
        |  [paper] STAR cites it; STAR's stated distinction is that MASK
        |          arbitrates ENTRIES, not the sub-entry array inside an entry
        v
STAR (MICRO 2024) — +25% average over MASK
```
Plus, named by STAR as precursors for the layout idea: range TLBs and clustered
TLBs (Park et al. 2017; Pham et al. 2012, 2014), with the stated distinction that
those assume a *single* application's consistent sequential/stride pattern whereas
"co-running applications often have varied and unpredictable access patterns";
multi-GPU TLB sharing (Li et al. 2021), "not MIG-specific"; and TLB speculation
and large-page management, declared orthogonal `[paper]`.
Anchor: [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md).

**Verified non-edge:** **STAR ↔ HDPAT, `NOT_CITED` in both directions.** They
share a *strategy* (§2.1) but not a citation.

### 2.1 "Reclaim existing translation capacity rather than provision more"

The strategy is real, it recurs three times, and the third instance names the
framing explicitly.

| Paper | Contended resource | Capacity reclaimed from | Status |
|---|---|---|---|
| [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md) STAR | a 16-sub-entry coalesced L3 TLB entry, left unpartitioned by MIG | the other MIG tenant's unused sub-entries, via a layout bit + Address Identify Bit | analysed |
| [`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md) HDPAT | walker throughput: SIMT request concurrency against **16 IOMMU walkers** | idle per-chiplet GMMUs on a wafer-scale mesh | analysed |
| **Heliostat** (ISCA 2025) | translation *bandwidth* | the **ray-tracing accelerator**, exploiting the operational similarity between BVH traversal and multi-level page-table walks | **watchlist, abstract only** |

Heliostat's abstract states the same framing HDPAT uses — prior work "focused on
better utilizing the provided translation bandwidth" whereas the goal is to
"fundamentally increase the translation bandwidth"
`[official-web: yonsei.elsevierpure.com]`. Reported: 1.93x / 1.92x / 1.66x over
baseline and two state-of-the-art schemes, Heliostat+ a further 1.23x, at 1.53% of
the area and 5.8% of the power of an overprovisioned comparable solution — **all
`[official-web]`, abstract-level, not `[paper]`**.

**No citation link between HDPAT and Heliostat was verified** — `UNKNOWN`.

**Heliostat is the clearest evidence in the corpus that categories cross-cut.**
Its verdict of record sits in this cluster (it is a GPU-virtual-memory paper) and
it is simultaneously a member of the fixed-function-repurposing category, where
it is attached three independent ways: its mechanism is that category's
signature move applied to the page table; its co-author Won Woo Ro also co-authors
TTA (`[author-overlap]`); and **TTP (ISCA 2026) independently lists it beside
LibRTS, TTA and Arkade under "non-graphics RT-core uses"** `[paper, TTP]`. See
[`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §5.

---

## 3. Verified chain: UVM management, oversubscription, migration

### 3.1 The verified shared ancestor, and the verified non-edge

- **Shared ancestor, verified from both papers' related work** `[paper, both]`:
  [`GPU-MICRO24-01`](../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md)
  (SUV) and [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md)
  (the AMD SVM study) both cite **Ganguly et al.** as foundational UVM
  characterization/prefetching work. SUV additionally cites **Chien et al.** and
  **Tyler & Ge** in the same "provide insights into UVM, but not mechanisms"
  bucket that **Allen & Ge** occupy in the SVM study. That is a real,
  citation-grounded connection between the AMD-characterization line and the
  NVIDIA-mechanism line.
- **Verified non-edge:** SUV ↔ the SVM study, `NOT_CITED` in either direction.
- The SVM study's own lineage, from its related work `[paper]`: prior NVIDIA UVM
  studies by Ganguly et al. (2019), Li et al. (2019), Chang et al. (2021),
  Allen & Ge (2021a, 2021b), Kim et al. (2020); oversubscription-degradation
  studies by Landaverde et al. (2014), Knap & Czarnul (2019), Yu et al. (2019).
- SUV's own precursor, named by the paper `[paper]`: **Li & Chapman, SC '19** —
  "the only prior work … used static analysis for UVM", for OpenMP. SUV's three
  stated deltas: density-not-count; reuse-distance inadequacy for CUDA's
  fewer/larger kernels; obliviousness to temporal and iterative patterns.
- **Gap claim, verified from the SVM paper's own text** `[paper]`: "To the best of
  our knowledge, this work is the first in-depth and comprehensive study of SVM
  technology", justified by "SVM has a distinct design from UVM, and the insights
  derived for UVM may not be directly applicable to SVM". Recorded as the authors'
  claim.

### 3.2 Management granularity is the hidden control variable

The single most transferable mechanical insight in this area, and it is the
variable that most cross-vendor comparisons silently get wrong.

| System | Management unit | Consequence |
|---|---|---|
| **NVIDIA UVM** | 4 KB base page; **60 KB speculative prefetch**; **2 MB VABlock** eviction | `[paper]`, [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) |
| **AMD SVM** | a **range**: 4 KB–1 GB, **1 GB-aligned**, up to **256 K pages**; migration, eviction and (de)allocation all happen at range granularity | `[paper]`, [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) |
| **GRIT** | per-page, per-phase, with a 64 KB page-*group* for access counters | `[paper]`, [`GPU-HPCA24-01`](../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md) |
| **GMLake** | 2 MB physical chunks stitched into one virtual range | `[paper]`, [`GPU-ASPLOS24-01`](../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md) |

**The granularity ratio between the two vendors' management units is up to ~512x
at the top end, and the SVM paper says explicitly that this is why insights do not
transfer** `[paper]`.

The mechanical statement, in the SVM paper's own terms: **one serviceable fault is
enough to move up to 256 K pages.** So the ratio between the granularity of the
*signal* (one warp's access) and the granularity of the *response* (a whole range)
is **up to five orders of magnitude** `[paper]`. That makes the driver an
*unconditional aggressive prefetcher* — beneficial when HBM is not oversubscribed,
catastrophic when it is, because a range migration can evict data that is still
live. The second pathology follows from the same fact: "successive accesses … of
small amount of data … distributed across ranges" rapidly exhausts GPU memory,
because each small touch costs a whole range `[paper]`.

DREAM's small-page result is the mirror image of this, and it is a *consequence*
of §1, not an independent win: **UVM must amortise a ~7x control overhead, which
is why it uses 60 KB prefetch and 2 MB eviction blocks; DREAM can afford 4 KB
because its per-request cost is a work-request post.** Both the small-request
bandwidth result and the 1.8x I/O-amplification result follow from the same
mechanism change `[inference]`, from the paper's own numbers.

### 3.3 Recency metrics that cannot see reuse

AMD SVM evicts by **Least Recently *Faulted*, not Least Recently Used**
`[paper]`. The paper names the failure mode itself: the LRF policy "may evict the
most intensely reused data, further exacerbating thrashing."

The mechanism is exact and worth stating precisely, because it is
counter-intuitive: **a range that was faulted in early and then reused heavily
*without further faults* looks stale to LRF precisely because it is resident and
working.** Reuse generates no faults, so reuse is invisible to a fault-recency
metric. This is the measured mechanism behind the collapse of the study's
Category III workloads — **SGEMM, MVT and GESUMMV, all of which have intensive
reuse** `[paper]`.

The discriminating property the paper places on the whole taxonomy: whether an
application exhibits "temporal patterns involving data reuse" or "spatial patterns
with small amounts distributed across ranges" `[paper]`. **Both are pathological
for range-granular management** — the first because reuse without faults defeats
LRF, the second because a small touch drags a whole range across the link.

The paper's recommendations are proposals, **not implemented or evaluated as
driver changes**, and their benefit is not quantified `[paper]`: reduce range size;
replace LRF with a smarter eviction policy; coordinate with HMM for distributed
spatial patterns. The natural follow-on work is exactly what **ARIADNE**
(HPCA 2026) and **Forest** (ISCA 2025) appear to occupy in the UVM setting;
neither was reachable to verify. `NOT_ESTABLISHED`.

**A closing hygiene note on this sub-branch:** SUV attacks the semantic blindness
of the *NVIDIA* UVM driver with compiler information; the SVM study diagnoses the
analogous blindness in *AMD* SVM as a **granularity-and-recency-metric** problem.
Same disease, two vendors, two diagnoses, no citation between them.

---

## 4. Verified chain and branch point: multi-GPU remote memory and placement

### 4.1 GRIT's verified lineage, from its own related work

```
Griffin (Baruah et al. 2020)   — Dynamic Page Classification + Async CU Draining
GPS (Muthukrishnan et al. 2021) — peer-to-peer publish/subscribe
Trans-FW / IDYLL / SnakeByte (Li et al. 2023) — the authors' own prior GPU translation work
CARVE (Young et al. 2018)      — caching remote data in GPU memory
Thermostat (Agarwal & Wenisch 2017) — hot/cold detection in hybrid memory
Ganguly et al. (2019/2020)     — tree-based neighbourhood prefetching
        |  all [paper], all named in GRIT's related work
        v
GRIT (HPCA 2024) — per-page, per-phase arbitration among migration / remote access / duplication
```
Anchor: [`GPU-HPCA24-01`](../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md).

Quantitative comparisons, with their qualifiers `[paper]`: GRIT is **27% better
than Griffin-DPC alone**, **16% better than full Griffin** (stated mechanism
difference: event-driven versus interval-driven triggering), **15% better than
GPS** (which is reported to have a 34% higher page-oversubscription rate), **54%
better than first-touch**, and **18% better than Griffin-DPC + Trans-FW**.
Ganguly et al.'s prefetching is declared orthogonal and shown to be **additive
(+23% when combined)**. Evaluated with NVLink-v2-class inter-GPU bandwidth
(300 GB/s), PCIe-v4 host attach (32 GB/s), 4 GPUs baseline.

GRIT's hardware asks are architectural, not software-only, and should travel with
any citation of it `[paper]`: hardware access counters with remote-access tracking
at 64 KB page-group granularity (threshold 256, attributed by GRIT to "NVIDIA
Volta and newer"); page duplication for read-only pages with write-collapse /
invalidation; remote physical mappings in a GPU-local page table; **free PTE bits
at positions 9–10 (scheme) and 52–53 (group size)**; and a 64-entry, 4-way
hardware PA-Cache in the translation path.

### 4.2 The verified author-cluster lineages

These are `[author-overlap]`, verified from the papers' own author lists, and they
are **weaker than citations** — recorded as such.

- **Pittsburgh + NVIDIA placement/translation group.** Yueqi Wang, Bingyao Li,
  Aamer Jaleel, Jun Yang and Xulong Tang co-author **both** GRIT (HPCA 2024) and
  STAR (MICRO 2024) — the same group attacking the *placement* layer and the
  *translation* layer in the same year. GRIT's related work additionally cites
  **IDYLL** and **SnakeByte** (Li et al. 2023) as this group's own earlier GPU
  translation work `[paper]`. The same first author (Yueqi Wang) appears on
  **OASIS: Object-Aware Page Management for Multi-GPU Systems** (HPCA 2025), the
  direct successor line — raising the placement decision from the page to the
  object. OASIS is on the watchlist with no reachable full text
  `[official-web, via census/HPCA_2025.md]`.
- **Yonsei / Won Woo Ro translation group.** Won Woo Ro co-authors **TTA**
  (MICRO 2024), **Heliostat** (ISCA 2025), **Marching Page Walks** (HPCA 2025),
  **LATPC** (MICRO 2025) and **Reducing Page Faults via Invalidation-based Mapping
  Propagation** (ISCA 2026). **Yuan Feng** co-authors **Barre Chord** (ISCA 2024),
  **Heliostat** and **Forest** (ISCA 2025). This is the densest author bridge in
  the corpus between the RT-unit branch and the translation branch.
- **Sungkyunkwan group.** Seokin Hong's group produces **SoftWalker** (MICRO 2025,
  software page-table walk on GPU warps) and **Leveraging Chiplet-Locality for
  Efficient Memory Mapping in MCM GPUs** (MICRO 2025) — the translation layer and
  the physical-address-mapping layer on the same MCM substrate HDPAT and Barre
  Chord address.
- **A third author trio** — Xiangyue Huang, Yanan Guo, Yuanchao Xu — holds three
  of the four ISCA 2026 multi-GPU memory papers (**LIBRA**, **Coarse-Grained
  Duplication First, Fine-Grained Deduplication Later**, and the MICRO 2025 **GPU
  Cache Eviction Priority Hints** paper).

### 4.3 The downstream frontier, and why no edge is asserted to it

The four ISCA 2026 multi-GPU memory papers — LIBRA (coordinated multi-GPU page
prefetcher), *Coarse-Grained Duplication First, Fine-Grained Deduplication Later*,
*Reducing Page Faults via Invalidation-based Mapping Propagation*, and
*Observability-aided GPU Memory Oversubscription* — collectively attack the same
three-way placement trade-off (duplication, deduplication, mapping propagation)
that GRIT frames. **No citation relationship was verified, because no full text
was reachable for any of them.** `[inference]` only. The
duplication-centric paper is notable in shape: it takes as the *default* the
duplication-versus-migration trade-off that GRIT arbitrates as one option among
three.

**Naming hazard recorded by the census and carried here:** the ISCA 2026
**LIBRA** (multi-GPU page prefetcher) is unrelated to the MICRO 2024
[`GPU-MICRO24-123`](../corpus/GPU-MICRO24-123--libra-memory-bandwidth-locality-aware-parallel-tile-rendering.md)
**LIBRA** (memory-bandwidth- and locality-aware parallel tile rendering). Do not
merge them.

---

## 5. The BaM branch: GPU-initiated access to memory that is not GPU memory

A verified citation edge that produces two independent descendants.

```
BaM — GPU-initiated high-throughput NVM access
   |  [paper] DREAM cites it; DREAM's stated distinction is TARGET
   |          (host/system memory rather than NVM)
   +---------------------------+
   |                           |
DREAM (ICS 2025)            GMT (ASPLOS 2024) — "GMT is built on top of BaM" [README]
GPU -> host memory          GPU-orchestrated 3-tier GPU / host / SSD hierarchy
via an RNIC                 with a device-side TLB and a least-squares reuse predictor
```

Anchor: [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md).
The GMT side is `[code]` + `[official-web: pure.psu.edu]` only — the artifact was
cloned and inspected at commit `2f139b0d01791812e8f2d5aaa8c8cfd176f2d2ee`, showing
a device-side TLB (`struct tlb_entry` l.205, `struct tlb` l.246,
`struct bam_ptr_tlb` l.393 in `include/page_cache.h`), a ticketed padded host ring
buffer, and `class LinearRegression::get_ls_solution` fitted over
(virtual-timestamp-distance, reuse-distance) sample pairs — i.e. the
reuse-prediction insertion policy its abstract describes. **The paper text is not
reachable (ACM 403), so no deep analysis was permitted and no claim rests on the
paper.** Reported from the abstract `[official-web]`: 50% over BaM (2-tier) and
over 350% over host-CPU-orchestrated HMM (3-tier) on a real platform.

**DREAM and GMT are two independent descendants of the BaM GPU-initiated-access
line**, one reaching host memory via an RNIC and one building a GPU-orchestrated
three-tier hierarchy. DREAM's other named precursors, from its own related work
`[paper]`: **HMM** (distinguished as requiring OS involvement with no speculative
prefetch), **DRAGON** (NVM via OS-level eviction), **GPUrdma** and **GPUnet**
(GPU-side networking, not virtual-memory management), **FaRM** and **AIFM**
(CPU-side far memory over RDMA), **ActivePointers** (memory-map abstractions for
device storage, no oversubscription support), **Subway** (manual graph
partitioning; DREAM 1.12–1.89x faster) and **RAPIDS** (1.5–2.5x).

---

## 6. The related branch: GPU–storage and GPU–host I/O paths

This is a *related branch*, not a stage of the memory chain: it shares the
device-resident-control move with DREAM but its object is an I/O path rather than
a page table.

| Design | Control placement | Mechanism |
|---|---|---|
| [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md) **AGILE** | fully `device-resident` | A GPU thread writes an NVMe Submission Queue Entry and rings the doorbell; a persistent GPU daemon kernel reaps the Completion Queue. **The CPU is in neither the control path nor the data path** |
| **Phoenix** (SC 2025, artifact-only) | host-driven, refactored | Removes the bounce buffer from the GPUDirect Storage path rather than bypassing it |
| **OS2G** (ASPLOS 2025, unread) | `UNKNOWN` | Routes through a DPU |
| **GMT** (ASPLOS 2024, artifact-only) | GPU-orchestrated | 3-tier GPU / host / SSD, device-side TLB, reuse-prediction insertion |

**The structural finding, and the reason this branch is ahead of the networking
branch:** AGILE achieves on the storage path exactly what
[`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md)
states cannot be done on the network path ("Current hardware interconnects require
a CPU thread to initiate the data transfer"; GPU-initiated RDMA not supported).
**The reason is that NVMe doorbells are plain MMIO registers mappable into the
GPU's address space, whereas RDMA verbs require a driver-mediated work-queue
protocol** — `[inference]`, but strongly supported by the two papers side by side.
Full treatment in [`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) §8.

**AGILE's caveats travel with it**: a single SKU (RTX 5000 Ada, a *workstation*
card, no A100/H100/MI300 result); **BAR1 must be enlarged beyond the typical
128 MB via a vendor tool** `[README]`; **IOMMU must be disabled** `[README]`,
which is not listed as a limitation in the read text; and separate driver builds
for Linux 6.8.0 and 6.17.0 `[code]`.

Note the shared platform constraint across this whole branch: **DREAM also
requires IOMMU disabled and ACS disabled** `[README]`. Two independent
device-resident designs both require turning off the isolation mechanism that
multi-tenant deployments depend on. Neither paper treats this as a limitation.
That is a corpus-level observation `[inference]`, asserted by neither.

---

## 7. The allocator layer, and why it sits beside rather than inside the chain

[`GPU-ASPLOS24-01`](../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md)
(GMLake) and [`GPU-PPoPP24-146`](../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md)
(Gallatin) both attack fragmentation and **neither cites the other**
`NOT_CITED` — they are at opposite ends of the stack. GMLake stitches
non-contiguous 2 MB physical chunks into one virtual range beneath a framework's
caching allocator, so a tensor no longer needs physical contiguity; Gallatin
restructures the *in-kernel* allocator itself, i.e. allocation issued from inside
a running kernel.

GMLake's lineage, verified from its own related work `[paper]`: it distinguishes
itself from **vLLM** (tensor-level virtual memory for self-attention padding —
"GMLake works on a unique memory scope for DNN training, which is different from
the vLLM and vMalloc/CUDA VMM"), from **raw CUDA VMM / vMalloc** (pool-unaware
primitives), and from the **PyTorch/TensorFlow BFC allocator** (splitting-based).
It positions ZeRO-Offload, DeepSpeed ZeRO-3, LoRA and gradient checkpointing as
*orthogonal* techniques whose irregular allocation behaviour motivates it.

**A prior-art expectation that does not hold:** SUV's related work cites
**DeepUM, Sentinel, SwapAdvisor, Capuchin, G10** as the DNN-specialised UVM/offload
line. **GMLake's related work as read does not name any of them** `NOT_CITED`, so
no citation link is asserted in either direction. This is a difference in framing
— allocator-level defragmentation versus migration/offload scheduling — verified
only from each paper's own related-work section.

GMLake and SUV both decide *what occupies HBM*, at different layers and by
different mechanisms: **GMLake changes the virtual→physical mapping so the same
bytes fit; SUV changes which bytes are resident at all.** Neither cites the other
`[inference]`.

---

## 8. Verified negatives in this area

1. **SUV ↔ STAR: `NOT_CITED`.** Same venue, same year, the two halves of GPU
   virtual-memory cost (placement and translation), no citation either way.
2. **SUV ↔ the AMD SVM study: `NOT_CITED`** — but they share a verified ancestor
   in Ganguly et al. `[paper, both]` (§3.1).
3. **STAR ↔ HDPAT: `NOT_CITED`**, despite sharing the "reclaim rather than
   provision" strategy (§2.1).
4. **HDPAT ↔ Heliostat: `UNKNOWN`** — the framings match almost verbatim, but only
   Heliostat's abstract was read, so no edge is asserted.
5. **GMLake ↔ Gallatin: `NOT_CITED`** (§7). **GMLake ↔ the DeepUM/Capuchin/G10
   line: `NOT_CITED`** as read (§7).
6. **DREAM ↔ SVM study ↔ MI300A porting: no citation links verified** among the
   three papers that independently establish the control-path result (§1).
7. **The ISCA 2026 multi-GPU frontier: no edges asserted** to GRIT or to each
   other, because no full text was reachable (§4.3).
8. **`GPU-SC24-82` (Hydrogen) is not a discrete-GPU memory paper.** The memory
   cluster's abstract-only row was re-adjudicated on full text and the
   `RELATED_GPU` verdict **confirmed, not upgraded**: the GPU is an integrated
   Xe-LPG-class iGPU (96 EUs) sharing a 16 MB LLC, the HBM2E is the fast tier of a
   *CPU-shared* two-tier main memory rather than device-private GPU memory, and
   only GPU memory *traces* are simulated in zsim — so there is no GPU
   microarchitectural behaviour in the model for the mechanism to key on
   `[paper]`, [`GPU-SC24-82`](../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md).
   Its relevance to this area is **structural analogy, not transfer.**

---

## 9. Where this area is silent

- **Prefetch as an independent stage.** `NOT_ESTABLISHED` (§0).
- **Whether reducing SVM range size and replacing LRF actually help.** The SVM
  study proposes both and evaluates neither. ARIADNE (HPCA 2026) and Forest
  (ISCA 2025) appear to occupy exactly that question and neither is reachable.
  `NOT_ESTABLISHED`.
- **HELM** (SC 2025, *Characterizing Unified Memory Accesses to Improve GPU
  Performance under Memory Oversubscription*) is the **highest-value unresolved
  item in the area** — a characterisation-plus-mechanism paper on the central
  axis, which would pair directly with the AMD SVM study and with SUV. Not even
  an abstract was obtained; authors `UNKNOWN`. `NOT_ESTABLISHED`.
- **Whether MI300A's unified physical memory changes the *allocation and copy
  path* question rather than just deleting it.** *One Memory-Many Paths*
  (IPDPS 2026, Best Paper Finalist) is the direct follow-on to
  [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md)
  and has no reachable PDF. `NOT_ESTABLISHED`.
- **MI300A hardware specifications** (CU/XCD counts, HBM3 capacity, bandwidth,
  Infinity Cache, TDP) are `NOT_IN_PAPER` in the one MI300A analysis and were
  deliberately not filled in from vendor documentation.
- **Cross-vendor transfer of any oversubscription result.** The ~512x management-
  granularity ratio (§3.2) means UVM insights and SVM insights are not
  interchangeable, and the SVM paper says so in its own words.

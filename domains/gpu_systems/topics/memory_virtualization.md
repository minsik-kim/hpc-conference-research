# GPU caches, TLBs, address translation and virtual memory (taxonomy C/D)

last_updated: 2026-09-18
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD.** Eight deep analyses (`C` = 2, `D` = 6), seven
`CORE_GPU` and one `RELATED_GPU` re-adjudicated from full text. Verdict
ledger: `../corpus/_LEDGER_memory_virtualization.md`.
Scope: caches, TLBs, address translation, GPU virtual memory, UVM/SVM,
oversubscription, page migration, multi-GPU memory management.

## 1. Problem landscape

A GPU's virtual-memory machinery was built for a device that is fed by a host,
and every paper here is a consequence of that assumption breaking. The corpus
splits the consequence three ways: **translation capacity** is too small and
now has to be shared (`C`); **placement** decisions are made reactively by a
driver that cannot see program semantics (`D`); and on an APU the whole
migration path **disappears**, which is the topic's own strongest
counterfactual.

The recurring physical fact underneath is that a GPU page fault is a
host-serviced round trip of tens of microseconds, so every mechanism here is
either "do not fault", "fault more cheaply", or "make the fault mean
something".

## 2. Key concepts

Page fault and demand paging; UVM (NVIDIA) vs SVM (AMD, HMM-based) — **not the
same design**, as `../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md`
insists; oversubscription and the degree-of-oversubscription (DOS) sweep;
range-granular vs page-granular migration; Least-Recently-Faulted eviction;
access counters; page duplication vs migration vs remote access; last-level
TLB and its **sub-entry** array; MIG as a partition that does *not* partition
translation; the CUDA VMM API's virtual/physical decoupling
(`cuMemCreate` / `cuMemMap` / `cuMemSetAccess`).

## 3. Main mechanism families

**Family C1 — reclaim translation capacity you already paid for.**
STAR (`../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md`) lets
two bases share one shared-L3-TLB entry's **8 sub-entries**, matching the
entry's layout (sequential or stride) to the tenants' fill patterns `[paper]`.

**Family C2 — distribute translation instead of enlarging it.**
HDPAT (`../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md`)
spreads translation caching across GPU modules with clustering, rotation, a
redirection table and prefetching `[paper]`.

**Family D1 — give the placement decision information the driver lacks.**
SUV (`../corpus/GPU-MICRO24-01--suv-static-analysis-guided-uvm.md`) supplies
*compile-time* structure semantics; GRIT
(`../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md`)
supplies a *runtime* per-page read/write bit and a spatial predictor.

**Family D2 — change the virtual→physical mapping so the same bytes fit.**
GMLake (`../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md`)
stitches non-contiguous physical chunks under a framework's caching allocator
through the CUDA VMM API.

**Family D3 — take the host out of the fault path entirely.**
DREAM (`../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md`)
has the device post its own work requests over RDMA.

**Family D4 — remove the problem in hardware.**
`../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md`
reports an MI300A APU where CPU and GPU share physical memory and the
migration term goes to zero.

**Family D5 — characterise the failure rather than fix it.**
`../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md`
is an AMD SVM oversubscription study whose product is a recommendation list,
not a mechanism.

## 4. Representative papers

- **STAR** (MICRO 2024) — **SIMULATED** (MGPUSim + RTL/FPGA for the added
  structures). **+31.4% average sub-entry utilisation at eviction** and
  **+32.8% average L3 hit rate**; sequential layout alone **19.2%**, stride
  layout alone **19.7%**, combination **28.7%**; per-application degradation
  under multi-tenancy falls from **40% to 26.1%**; **25% average improvement
  over MASK** `[paper]`. Shows **MIG does not partition the last-level TLB**.
- **HDPAT** (HPCA 2026) — **SIMULATED** (MGPUSim). The ablation decomposes a
  **1.57×** end-to-end gain: routing-based caching alone gives *no*
  improvement ("repeated attempts penalty"); unbalanced distributed caching
  1.08×; + clustering and rotation 1.13×; + redirection table 1.18×;
  + prefetching 1.17×; all combined **1.57×** `[paper]`.
- **GRIT** (HPCA 2024) — **SIMULATED** (MGPUSim). Against *uniform* policies
  on 8 applications at 4 GPUs with DRAM at 70% of footprint: **60% over
  on-touch, 49% over access-counter, 29% over duplication**; **27% over
  Griffin's Dynamic Page Classification** and **16% over full Griffin**
  `[paper]`.
- **SUV** (MICRO 2024) — **MEASURED** on one GPU only: **RTX 3090, 24 GB
  (Ampere)** with an AMD Ryzen 7950X host over **PCIe 4.0 x16**, with an
  authors' driver patch `[paper]`. **37–100% fewer page faults at 50%
  oversubscription**; **20% geomean speedup at zero oversubscription** — i.e.
  part of the benefit is fault-path avoidance independent of capacity pressure
  `[paper]`.
- **GMLake** (ASPLOS 2024) — **MEASURED** (A100-80GB and V100 class).
  Average **9.2 GB** saved, up to **25 GB** on A100-80GB; fragmentation ratio
  down **15% on average, up to 33%**. From 1 to 16 GPUs PyTorch's fragmentation
  grows **~10% → ~24%** while GMLake holds **~10%** `[paper]`. Implementation
  is `NOT_INSPECTED` — the artifact was not cloned
  (`../corpus/_LEDGER_memory_virtualization.md`).
- **DREAM** (ICS 2025) — **MEASURED** (V100 + NICs). The control path was
  **~7× the transfer cost at 64 KB pages**, and removing it is what makes
  4 KB granularity affordable `[paper]`. Graph analytics on SuiteSparse/GAP
  (3.61 B–6.67 B edges, 4 KB pages): **1.4×** over `cudaMemAdvise`-tuned UVM
  for BFS, **1.5×** for CC. The most important result is predictability, not
  speed: across the oversubscription sweep **UVM slows by 4–10×** on graphs
  while **DREAM stays at a consistent 1.5–2.5× slowdown** `[paper]`.
- **MI300A + OpenMP unified memory** (ISC 2024) — **MEASURED**. On
  HPC_motorbike Large, 34 M cells, 20 time-steps: **MI300A vs x86+H100-SXM
  = 4×**, **vs x86+MI210 = 5×**, and **1 MI300A with 1 CPU core vs a
  single-socket 64-core Zen 4 = 2×** `[paper]`. The paper quantifies page
  migration at **>65% of discrete-GPU time for this benchmark** `[paper]`.
  Carry the qualifier: this is **cross-vendor and cross-toolchain**
  (ROCm-6.0/clang-17 vs CUDA-12.2.2/clang-18) and the paper does not decompose
  compiler quality out of the 4× `[inference, stated as such in the analysis]`.
- **AMD SVM study** (ICS 2024) — **MEASURED** on MI250X/MI300A. Diagnoses
  range-granular migration as *unconditional prefetch* (one serviceable fault
  pulls up to **256 K pages**) and LRF eviction as blind to reuse `[paper]`.

## 5. Historical lineage

Verified from the papers' own related work, not from topical adjacency:

- **Translation**: Bhattacharjee et al. (shared last-level TLB across CPU
  cores) → Trans-FW, Valkyrie, Barre Chord (ISCA 2024), IDYLL → **HDPAT**
  `[paper, HDPAT]`. On the multi-tenant side: MASK (Ausavarungnirun et al.),
  range/clustered TLBs (Pham 2012/2014, Park 2017) → **STAR** `[paper, STAR]`.
- **Placement**: Ganguly et al. tree-based prefetching and Griffin (Baruah
  2020) and GPS (Muthukrishnan 2021) → **GRIT**; Li & Chapman (SC 2019, the
  only prior static-analysis-for-UVM work) → **SUV** `[paper, both]`.
- **Author lineage, verified from both author lists**: Yueqi Wang, Bingyao Li,
  Aamer Jaleel, Jun Yang and Xulong Tang co-author **both** GRIT (HPCA 2024)
  and STAR (MICRO 2024) — one Pittsburgh+NVIDIA group attacking the placement
  layer and the translation layer in the same year `[paper, both]`.
- **Device-driven access**: BaM → DREAM (verified citation link) `[paper]`.

## 6. Implementation families

`SIMULATOR` (MGPUSim): STAR, HDPAT, GRIT. `REAL_SILICON` with a patched
driver: SUV. `REAL_SILICON` production stack: GMLake, DREAM, the AMD SVM
study, the MI300A porting paper. STAR additionally carries RTL/FPGA area
estimates — **simulated area, never reported as measured**.

## 7. Important disagreements / tensions

**T1 — large pages erode both halves of this topic, and two independent papers
measure it.** GRIT's improvement falls from **60% to 23% with 2 MB pages**,
attributed to more frequent false sharing and mixed read/write attributes
inside one page `[paper]`. STAR's gain falls from **28.7% to 10% average with
2 MB pages**, because large pages already extend reach `[paper]`. Different
mechanisms, different venues, same direction. Neither paper cites the other.

**T2 — NVIDIA UVM and AMD SVM are diagnosed with incompatible vocabularies and
the two lines do not meet.** SUV attacks *semantic blindness* in the NVIDIA
driver with compiler information; the ICS 2024 SVM study attacks *range
granularity plus a recency metric* in AMD's HMM-based path. **Neither cites the
other** `[paper, both analyses' §12.14]`. A reader who takes a UVM result as an
SVM result is making an error the corpus explicitly warns against.

**T3 — GMLake and SUV both decide what occupies HBM and neither cites the
other.** GMLake changes the virtual→physical mapping so the same bytes fit;
SUV changes which bytes are resident at all. GMLake's related work does not
name the DNN-specialised UVM/offload line (DeepUM, Sentinel, SwapAdvisor,
Capuchin, G10) that SUV's does `[paper, both]`. Recorded as a difference of
framing, with **no claim about intent**.

**T4 — scaling erodes GRIT's advantage and the paper says so.** 2 GPUs:
40/37/11%; 8 GPUs: 38/35/26%; 16 GPUs: **27/26/23%** against
on-touch/counter/duplication, because "as more GPUs increase … pages become
more frequently shared" `[paper]`. HDPAT's answer at wafer scale is to
distribute translation rather than placement — but **no citation link between
STAR and HDPAT was verified**, and none should be asserted.

**T5 — the topic's own counterfactual.** If an APU removes >65% of discrete-GPU
time on one benchmark (`GPU-ISC24-01`), then every migration-policy result in
families D1–D3 is a result about *discrete* GPUs on PCIe. SUV's evaluation is
explicitly PCIe-attached and the analysis flags that far-fault costs differ on
an NVLink/C2C-attached host `[inference, in the SUV analysis]`.

## 8. Current limitations

**Bounded by full-text access, not by the field.** In this environment
`dl.acm.org` returns 403 (re-verified this pass on the HELM `doi/full` URL),
`ieeexplore.ieee.org` returns 418, `dblp.org` and `par.nsf.gov` are
robots-blocked. `../corpus/_LEDGER_memory_virtualization.md` therefore uses
`PENDING_FULLTEXT` where an open-access publisher URL was *observed* but the
host is blocked here, and `CLOSED_ACCESS` only where no public copy was
located at all. **This is an access-path limitation, not a statement about any
paper's licence.**

Specific bounded areas:
- **Heliostat** (ISCA 2025, RT accelerator used for page-table walks) is
  `CORE_GPU` / `ABSTRACT_ONLY` in this ledger. It is the clearest evidence that
  this topic and `fixed_function_repurposing.md` cross-cut — and it could not
  be read. See `../corpus/_LEDGER_fixed_function_repurposing.md` §4.3.
- **Multi-GPU page management post-2024** (OASIS, HPCA 2025; the ISCA 2026
  LIBRA / duplication-then-deduplication / invalidation-based-mapping cluster)
  is named in `GPU-HPCA24-01` §12.14 as the successor line and has **no deep
  analysis** here.
- **GMLake's implementation** is `NOT_INSPECTED`; its artifact
  (`github.com/intelligent-machine-learning/glake`) was not cloned.
- Five rows carry `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` because
  `../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`: GMLake, HELM (SC 2025),
  Hydrogen (SC 2024), the MI300A porting paper, One Memory-Many Paths
  (IPDPS 2026). **No claim of non-duplication is made for any of them.**

## 9. Research questions

`INFERENCE`, derived from §7 and not falsified against the corpus:

1. Does any mechanism here survive a 2 MB page? Two independent measurements
   say the gain roughly halves or worse (T1); no paper in the corpus proposes
   a placement or sub-entry mechanism designed *for* large pages.
2. GRIT has no scheme that makes a shared read-write page cheap, and names
   ST/BS/C2D at **99%/56%/42% shared read-write pages** as the cases where it
   stays far from its own `Ideal` bound `[paper]`. Is that a policy gap or a
   hardware one?
3. Is the MI300A result (D4) a general answer or a benchmark-specific one? The
   corpus has exactly one APU data point and it is not decomposed.

## 10. Deeper lookup paths

`../corpus/_LEDGER_memory_virtualization.md` (verdicts, access states,
watchlist in expected-value order, ID-collision record) → the eight analyses
above → the papers and, where §12.8 pins a commit, their artifacts.
Cross-topic: `fixed_function_repurposing.md` for Heliostat;
`runtime_scheduling.md` for what MIG does and does not partition;
`data_movement_compression.md` for the GPU–storage path that DREAM's
device-driven design parallels.

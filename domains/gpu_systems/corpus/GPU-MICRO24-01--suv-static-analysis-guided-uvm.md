# GPU-MICRO24-01 — SUV: Static Analysis Guided Unified Virtual Memory

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `D — GPU virtual memory / UVM / oversubscription / page migration` *(letter per this cluster's task assignment; the repository contains no A–Q taxonomy file — `NOT_IN_REPOSITORY`)*
secondary_topics: `compiler/static analysis for GPU memory management; GPU driver runtime policy`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background (UVM fault path, tree-based prefetching, access counters); design (SUV-Kern, SUV-Host, SUV-Mgmt, driver extensions incl. Algorithms 1 and 2); implementation (LoC breakdown); evaluation setup; results incl. per-application and page-fault figures; comparisons vs TBP/AC/SC; zero-oversubscription case; author-stated limitations; related work. Read via two targeted full-text passes over the author-hosted camera-ready PDF. NOT read at the level of individual figure axes.`

## 12.1 Bibliographic facts

- Title: *SUV: Static Analysis Guided Unified Virtual Memory* `[paper]`
- Authors: Pratheek B (Indian Institute of Science, Bengaluru), Guilherme Cox (NVIDIA, Santa Clara), Jan Vesely (NVIDIA, Westford), Arkaprava Basu (Indian Institute of Science, Bengaluru) `[paper]`
- Venue: MICRO 2024 (MICRO-57), Session 3A "GPU Microarchitecture I" `[official-program, via census/MICRO_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- DOI: `UNKNOWN` — the census records the IEEE Xplore document id 10764479 but no DOI string was retrieved; `ieeexplore.ieee.org` is unreachable from this environment (HTTP 418). No DOI is asserted here.
- Full text used: https://www.csa.iisc.ac.in/~arkapravab/papers/MICRO24_SUV.pdf (author-hosted camera-ready) `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` — no repository link was located. Implementation symbols below are therefore `NOT_INSPECTED` at the code level.

## 12.2 Core question (one sentence)

Can a compiler that statically reasons about *which* GPU data structures are accessed *how densely, in what phase, and over what per-iteration address span* supply the UVM driver with enough semantic information to place and migrate pages proactively, instead of letting the driver react to page faults after the fact? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** The dominant axis. UVM lets a CUDA program address a footprint larger than GPU HBM, at the price of demand migration between HBM and host DRAM over PCIe. The paper's target regime is *memory oversubscription*: application footprint exceeds HBM. `[paper]`
- **Compute.** Indirect: warps stall on far faults, so the compute pipeline is idled by the memory-management path rather than by arithmetic. `[paper]`
- **Communication.** PCIe 4.0 x16 host↔device traffic is both a cost metric and a thrash symptom; SUV reports 81% less PCIe traffic than the SC baseline and 77% less than access-counter migration, both at 50% oversubscription on an RTX 3090 / Ryzen 7950X system. `[paper]`
- **Scheduling.** SUV's per-kernel policy hook runs at kernel-launch boundaries and its prefetch hook at host-loop iteration boundaries, i.e. it schedules *data* against the host program's kernel-launch schedule. `[paper]`
- **Synchronization.** `NOT_IN_PAPER` as a first-order concern.

## 12.4 Why the problem exists (hardware root cause)

1. **A GPU far fault is a host-CPU round trip.** When an SM's memory pipeline misses in the TLB and the page-table walk finds no valid mapping, the GPU raises a fault that is serviced by the UVM driver *on the host CPU*, which then migrates the page. The paper states the on-demand migration path costs "tens of microseconds of delay." `[paper]` That is three to four orders of magnitude above an HBM access, so a single fault stalls thousands of warp-cycles' worth of work.
2. **The driver has no semantics, only addresses.** The eviction and prefetch machinery sees virtual page numbers and fault addresses. It cannot distinguish a small, hot index array from a large, streamed matrix. Under oversubscription this produces the paper's named failure mode: the system "thrashes the HBM by repeatedly migrating pages back and forth between the HBM and the DRAM." `[paper]`
3. **Existing prefetch heuristics are structurally local.** Tree-Based Prefetching (TBP) builds a complete binary tree per 2 MB region and, when a subtree's HBM-resident fraction crosses a threshold (default 50%), prefetches the rest of that subtree. `[paper]` This is a *density-within-2 MB* heuristic; it cannot express "this whole 3 GB array should never be resident."
4. **Access counters are reactive by construction.** NVIDIA's hardware access counters track remote accesses for a few regions and migrate when a counter crosses a threshold (default 256). `[paper]` The 256 remote accesses that trigger the migration have already been paid at DRAM latency.
5. **CUDA kernel shape defeats reuse-distance analysis.** The paper's critique of the one prior static-analysis UVM work (SC '19, Li & Chapman, targeting OpenMP) is that reuse distance is "insufficient for typical CUDA" because CUDA programs have *fewer, larger* kernels whereas the OpenMP codes had many small ones. `[paper]` This is a GPU-programming-model root cause, not a general compiler one.

## 12.5 Mathematical / performance model

SUV does not present a closed-form performance model. It defines three *metrics* that its injected host code computes, and a policy that consumes them. `[paper]`

- **Access density** = "number of GPU memory accesses to it, divided by its size", per data structure. `[paper]` The essential departure from prior work is the division by size: prior work used total access count, which the paper argues "underutilizes HBM" because a huge structure with many total accesses wins over a small structure with far more accesses per byte. `[paper]`
- **Working Set Size (WSS)** = the fraction of a data structure "likely to be accessed by concurrently executing threadblocks." `[paper]` This is a *concurrency-scoped* footprint: it depends on how many thread blocks are resident at once, not on the whole grid.
- **Span** = for an iteratively launched kernel, "the range of address offsets accessed by memop in an iteration." `[paper]`

Policy thresholds reported: WSS classification fraction 0.5; a "temporal density" threshold of 5/4, described as "empirically determined using a micro-benchmark"; prefetch spans below 2 MB are batched across iterations to amortise prefetch cost. `[paper]` No sensitivity sweep is shown for any of these — see 12.13. Any cost model beyond this would be `[reconstruction]` and is not asserted.

## 12.6 Data layout and ownership

- **thread → warp:** memops are analysed per static instruction; the expression tree for a memop is a function of `threadIdx`/`blockIdx`-derived terms, loop induction variables and branch conditions. `[paper]`
- **block/workgroup → SM:** WSS is defined against the set of *concurrently executing* thread blocks, so the unit of "hot working set" is the resident-block cohort on the GPU, not the grid. `[paper]` This is the layer at which SUV decides "reserve HBM equal to WSS and let the rest fault in."
- **GPU (HBM):** the allocation unit of SUV's policy. Structures are *pinned on HBM* (`suvPinOnGPU`, removed from LRU eviction), *pinned on host DRAM* (`suvPinOnHost`), or left on the on-demand fault path. `[paper]`
- **node (host DRAM + PCIe):** the overflow tier. Everything not granted HBM residency lives here and is reached either by migration or by pinned-host mapping.
- **cluster:** `NOT_IN_PAPER` — SUV is single-GPU.

Ownership is decided by SUV-Mgmt before each kernel launch, per Algorithm 1: HBM capacity is first apportioned to `Unknown` structures in proportion to their footprint; the remainder are sorted by descending access density; `Temporal` structures with high density get an HBM reservation equal to their WSS with on-demand migration enabled inside it; remaining high-density structures are pinned on HBM and low-density ones on host DRAM; `Iterative` structures are allowed to prefetch. `[paper]`

## 12.7 Pseudo code

Component names, driver call names, classification labels and the two algorithms' roles are `[paper]`; the statement-level shape below is `[reconstruction]` of Algorithms 1 and 2 as described.

```
# --- compile time ---
SUV-Kern(kernel LLVM IR):                        # [paper]: names + outputs
  for each memop in kernel:
    build expression_tree(memop)                 # [paper]
    record enclosing loops, branch conditions     # [paper]
    if address depends on a loaded value:
      mark data_structure as Unknown              # [paper]: pointer-chase
  emit per-memop file(expression trees, data structures, loops, branches)  # [paper]

SUV-Host(host LLVM IR):                          # [paper]
  locate allocations, kernel launches, grid/block dims       # [paper]
  locate iteratively launched kernels + induction variables  # [paper]
  map kernel arguments -> virtual memory regions             # [paper]
  inject IR that, at run time, computes:
      access_density(ds), WSS(ds), span(memop, iteration)    # [paper]
  classify each ds in {Density, Temporal, Unknown, Iterative}  # [paper]

# --- run time, before each kernel launch (Algorithm 1) ---   # [reconstruction] of [paper] text
SUV-Mgmt_per_kernel(structures, hbm_capacity):
  give Unknown structures HBM share proportional to footprint  # [paper]
  for ds in sort_by_access_density_descending(rest):           # [paper]
    if ds.class == Temporal and ds.density high:
      reserve hbm(ds.WSS); enable on-demand migration for ds   # [paper]
    elif ds.density high:  suvPinOnGPU(ds)                     # [paper]
    else:                  suvPinOnHost(ds)                    # [paper]
    if ds.class == Iterative: allow_prefetch(ds)               # [paper]

# --- run time, per host-loop iteration (Algorithm 2) ---      # [reconstruction] of [paper] text
SUV-Mgmt_per_iteration(i):
  for memop with iteration-dependent address:                  # [paper]
    cudaPrefetchAsync(span(memop, i))                          # [paper]
  evict data of iteration i-1 back to host DRAM                # [paper]
```

Driver interface actually named by the paper: `suvPinOnGPU`, `suvPinOnHost`, an on-demand-migration mode that removes policy overrides, the pre-existing `cudaPrefetchAsync`, and `suvEnableAccessCounter` / `suvSetNoMigrateRegion` for the hybrid access-counter fallback. `[paper]`

## 12.8 Real implementation

- Compiler passes built on **LLVM 15.0**. `[paper]`
- Driver work is a modification of the **NVIDIA open-source UVM Linux driver, version 525**, with CUDA 11.8. `[paper]`
- Size: approximately **3,350 lines** total — "3000 LLVM + 200 management + 150 driver." `[paper]` The distribution is itself informative: almost all the engineering is the static analysis; the driver change is a thin pinning/prefetch API.
- Compilation cost: **~5 s added** to compile time, described by the authors as a one-time cost. `[paper]`
- **No repository was found** (`NOT_FOUND_AFTER_SEARCH`). All symbols above are the paper's own names; no source file, function signature or commit was inspected → `NOT_INSPECTED`.

## 12.9 Kernel execution

SUV does not change kernel code generation, warp scheduling or instruction selection; it changes what is resident when a kernel runs. `[paper]` The two execution-level hooks are:

- **kernel-launch granularity:** Algorithm 1 runs *before* each launch, so placement is re-decided per kernel, which matters because different kernels in the same program touch the same structures with different densities. `[paper]`
- **host-iteration granularity:** Algorithm 2 runs per host-loop iteration for iteratively launched kernels, issuing prefetches for the next iteration's span and evicting the previous iteration's data. `[paper]`

The effect at the warp level is the removal of far-fault stalls: page faults drop 37–100% across applications at 50% oversubscription on the RTX 3090 platform. `[paper]` The paper does not report warp-occupancy or stall-cycle breakdowns, so a claim about specific warp-scheduler behaviour would be `[inference]` and is not made.

## 12.10 Memory traffic

Path: register ↔ L1/shared ↔ L2 ↔ **HBM (24 GB on the RTX 3090 used)** ↔ **PCIe 4.0 x16** ↔ host DRAM. `[paper]`

SUV acts only on the HBM↔DRAM leg, in three ways: (i) removing pages from that leg entirely by pinning low-density structures on the host and serving them by remote access rather than migration; (ii) pinning high-density structures in HBM so they never cross it; (iii) replacing fault-driven single-page crossings with explicit span prefetches. Measured consequence, all at 50% oversubscription on RTX 3090 / Ryzen 7950X / PCIe 4.0 x16: **81% less PCIe traffic than SC** and **77% less than access-counter migration**. `[paper]` The register↔shared↔L1↔L2 legs are untouched. `[inference]` from the fact that no kernel-code transformation is reported.

## 12.11 Why it is faster/slower (decomposed)

Decomposition of the gain, each element grounded in the paper:

1. **Fault elimination, not fault acceleration.** 37–100% fewer page faults at 50% oversubscription. Each avoided fault removes a tens-of-microseconds host-serviced round trip. `[paper]`
2. **Density-normalised capacity allocation.** Sorting by accesses-per-byte rather than accesses means HBM bytes go to the structures with the highest return per byte. The paper attributes 2DC's 43% speedup specifically to access-density-guided pinning. `[paper]`
3. **Reservation rather than residency for phased data.** For `Temporal` structures, only the WSS is reserved and the rest is allowed to fault, which avoids paying for whole-structure residency while still keeping the concurrent block cohort's slice local. MM, GMM and HEL are named as benefiting from this. `[paper]`
4. **Span prefetch converts demand faults into bulk transfers.** DTG gains 21% at 50% oversubscription from iterative prefetching. `[paper]` The win is per-transfer overhead amortisation, which is why spans under 2 MB are batched across iterations. `[paper]`
5. **Thrash avoidance.** FW, MVT and FDT show "manifold slowdowns" under baseline UVM; SUV makes them viable. `[paper]` These are the cases where the baseline's reactive loop had no fixed point.
6. **A residual win even without oversubscription:** 20% geomean speedup at zero oversubscription, from proactively pinning and thus never faulting at all. `[paper]` This is important evidence that part of the benefit is *fault-path avoidance*, independent of capacity pressure.

Where SUV cannot be faster: any structure it must label `Unknown` falls back to the same reactive access-counter machinery, so pointer-chasing codes inherit the baseline's behaviour. `[paper]`

## 12.12 Hardware generation dependence

- Requires a GPU/driver generation with **UVM page-fault-based migration** (Pascal onwards, in NVIDIA's line) — the whole mechanism is a policy layer over that fault path. `[inference]` from the paper's use of the 525 UVM driver and fault semantics; the paper does not enumerate supported generations.
- Requires **hardware access counters** for its `Unknown` fallback: the paper describes NVIDIA access counters that "track the number of remote accesses to a few memory regions" and migrate when a counter crosses a threshold (default 256), and compares against that scheme as baseline `AC`. `[paper]` The generation in which that feature appears is *not* stated by SUV; GRIT (`GPU-HPCA24-01`) attributes access-counter-based migration to "NVIDIA Volta and newer" `[paper, GRIT]`, and that attribution is recorded here as GRIT's, not SUV's. Without counters, SUV's fallback path degrades to plain demand paging. `[inference]`
- Requires `cudaPrefetchAsync` and the ability to pin ranges and disable LRU eviction for them; the latter is added by the authors' driver patch, i.e. it is not stock functionality. `[paper]`
- Evaluated on exactly one GPU: **RTX 3090, 24 GB (Ampere)**, with an AMD Ryzen 7950X host over PCIe 4.0 x16. `[paper]` The authors list single-GPU-model evaluation as a limitation. `[paper]` Notably the platform is *PCIe*, not NVLink-attached; on an NVLink/C2C-attached host the far-fault and remote-access costs differ, and the paper does not evaluate that. `[inference]`

## 12.13 Limitations

Author-stated `[paper]`:
1. Pointer-chase / indirect access patterns are not statically analysable; such structures are labelled `Unknown` and handed to hardware access counters.
2. Data-dependent loop bounds unknown even at kernel-launch time prevent density/pattern computation; those structures fall back to access-counters only.
3. Data-dependent branch conditions cannot be evaluated, "potentially overestimating the access density."
4. Closed-source kernel libraries (cuDNN named) have no source for SUV-Kern; the proposed mitigation is library-developer-supplied wrapper metadata, i.e. a split-responsibility model.
5. Evaluation on a single GPU model; portability not demonstrated.
6. ~5 s added compile time.

Observed by this analysis, not claimed by the paper `[inference]`:
7. **No published sensitivity sweeps** for the WSS fraction (0.5), the temporal-density threshold (5/4) or the 2 MB prefetch-batching span, despite these being policy-critical. The temporal threshold is described as empirically tuned on a micro-benchmark, which leaves open how workload-specific the tuning is.
8. **No formal ablation section**, so the per-mechanism contribution (pinning vs WSS reservation vs iterative prefetch vs counter fallback) is not separated; only per-application narratives attribute gains to individual mechanisms.
9. SUV is compared against TBP, access counters and the SC '19 static-analysis work, but **not** against the DNN-specialised systems (DeepUM, G10, Capuchin, SwapAdvisor, Sentinel) it cites; the paper's stated reason is that those "leverage idiosyncrasies of DNN training that are not generally applicable." `[paper]`

## 12.14 Relation to prior corpus

- `prior_corpus_check`: `NO_EXISTING_ANALYSIS`. A whole-repository grep for the exact and normalised titles, for "Static Analysis Guided Unified Virtual Memory", and for first-author + distinctive term returned only `domains/gpu_systems/census/MICRO_2024.md` (a STEP-B screening row). No analysis existed.
- **Precursor named by the paper:** Li & Chapman, SC '19 — "the only prior work … used static analysis for UVM," for OpenMP. SUV's three stated deltas are density-not-count, reuse-distance inadequacy for CUDA's fewer/larger kernels, and obliviousness to temporal and iterative patterns. `[paper]`
- **Competing (same cluster, same year/venue):** STAR (`GPU-MICRO24-02`) also attacks GPU virtual-memory cost at MICRO 2024 but at the *translation* layer (shared L3 TLB under MIG) rather than the *placement* layer. The two are orthogonal: SUV changes which pages are resident; STAR changes how many translations a shared TLB can hold. No citation relationship was verified in either direction.
- **Complementary within this cluster:** GRIT (`GPU-HPCA24-01`) solves the sibling problem in the multi-GPU setting — per-page choice among migration/remote-access/duplication — and, like SUV, uses page faults as a cheap signal; but GRIT's decision input is a runtime-observed read/write bit, whereas SUV's is compile-time-derived semantics. Both cite Ganguly et al. tree-based prefetching as the reactive baseline to beat. `[paper]` (both papers)
- **Complementary, different layer:** the ICS 2024 SVM study (`GPU-ICS24-02`) measures the same oversubscription cliff on AMD's HMM-based SVM and finds the driver's *range* granularity to be the analogue of the semantic-blindness SUV attacks. Neither paper cites the other (SUV predates publication of neither is asserted — no citation link was verified). `[inference]`
- `EXISTING_CORPUS_DUPLICATE`: no.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the cost SUV removes is the *GPU far-fault* path, in which a device-side fault is serviced by the host CPU's UVM driver at tens of microseconds — a CPU's own page fault is serviced locally and is orders of magnitude cheaper, so the optimisation target does not exist; (b) the WSS metric is defined over *concurrently executing thread blocks*, a SIMT-occupancy concept with no CPU analogue; (c) the paper's explicit argument against reusing the prior OpenMP static-analysis approach is that CUDA has *fewer, larger* kernels, i.e. the analysis design is shaped by the GPU kernel-launch model; (d) the fallback path depends on NVIDIA GPU *hardware access counters* and the implementation is a patch to the NVIDIA UVM driver.

verdict_basis: SUV depends on the GPU UVM page-fault/migration path, GPU hardware access counters, and a working-set notion scoped to concurrently resident thread blocks; none of these exist on a CPU or on a generic accelerator without a fault-driven unified-memory subsystem.

# GPU-ISC24-01 — Porting HPC Applications to AMD Instinct MI300A Using Unified Memory and OpenMP

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `D — unified memory on an APU: page-migration elimination, allocator/placement semantics` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `OpenMP target offload programming model; production CFD (OpenFOAM) porting practice`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background on MI300A and the unified-physical-memory vs unified-virtual-memory distinction; porting methodology incl. the OpenMP directives used, the 'requires unified_shared_memory' declaration, declare target, the adaptive if(target:) cut-off, and the allocator statements (Listings 4-6 as described); results Table 1 and Figs. 5-6 with the page-migration profiling claim; stated limitations and ongoing work; related work. Read via two targeted full-text passes over arXiv HTML v1. NOT read: per-listing source line detail beyond what the two passes reported.`

## 12.1 Bibliographic facts

- Title: *Porting HPC Applications to AMD Instinct™ MI300A Using Unified Memory and OpenMP®* `[paper]` (the census records the title without the trademark marks)
- Authors: Mark Olesen, Simone Bnà, Nicholas Malaya, Suyash Tandon, Leopold Grinberg, Gheorghe-Teodor Bercea, Carlo Bertoli `[paper]`
- Affiliations: Advanced Micro Devices Inc. (Austin, USA); OpenCFD Ltd. (Berkshire, UK); CINECA SuperComputing Applications and Innovations Department (Bologna, Italy) — the paper does not map each author to one affiliation in the read text, so no per-author attribution is asserted. `[paper]`
- **Discrepancy noted:** `domains/gpu_systems/census/ISC_2024.md` lists this paper as "Suyash Tandon et al. (AMD)" with Tandon as the *speaker*; the arXiv author list places Mark Olesen first. The census row is a program/speaker record, the arXiv list is the paper's byline. Both are recorded; neither is corrected in the census by this analysis.
- Venue: ISC High Performance 2024, Research Paper Session "Programming Models for Heterogeneous Systems" `[official-program, via census/ISC_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER` (analysed from the `PREPRINT` arXiv v1). Per the census, ISC 2024 research papers were published open access by **IEEE** (not Springer LNCS) — that publisher note is `[official-web, via census/ISC_2024.md]`.
- DOI: `UNKNOWN` — none retrieved; none asserted.
- Full text used: https://arxiv.org/html/2405.00436v1 `[paper]`
- Artifact/code: the paper states the unified-memory OpenFOAM implementation is "currently accessible through GitHub" with an ongoing effort to upstream it, but **no repository URL was captured in the read text and none was located**. `NOT_FOUND_AFTER_SEARCH` → `NOT_INSPECTED`. No file, symbol or commit from any repository is asserted.

## 12.2 Core question (one sentence)

If host and device share the *same physical* memory, does the unified-memory programming model finally become usable for a million-line production HPC code — i.e. can OpenMP `target` offload with `requires unified_shared_memory` replace explicit data management without paying the page-migration cost that makes unified memory slow on discrete GPUs? `[paper]`

## 12.3 GPU/HPC problem translation

- **Memory.** The central axis, and the paper's claim is architectural: on a discrete GPU, unified *virtual* memory "requires page migrations"; MI300A implements unified *physical* memory, which "completely removes the overhead of page migrations." `[paper]`
- **Communication.** Eliminated rather than optimised: there is no host↔device copy to schedule because there is no second physical memory. `[paper]`
- **Compute.** The offload decision becomes per-loop and size-dependent, handled by an OpenMP `if(target:...)` clause against a cut-off. `[paper]`
- **Scheduling.** Only loop-level: `target teams distribute parallel for` over the CFD solver's loops. `[paper]`
- **Synchronization.** `NOT_IN_PAPER` as a first-order concern.
- **Productivity as a first-class metric.** The paper's strongest quantitative claim in this axis: "O(100) lines of code modification" against a codebase the abstract describes as roughly a million lines. `[paper]`

## 12.4 Why the problem exists (hardware root cause)

1. **On a discrete GPU, unified memory means demand migration.** The paper's measured consequence: "On dGPUs, more than 65% of the time is spent in page migrations: updating GPU tables and copying the data between host and device," for the HPC_motorbike benchmark (Large, 34 M cells). `[paper]` Two distinct costs are named in that sentence — *page-table updates* and *data copies* — which matches the cost decomposition the ICS 2024 SVM study found independently (`GPU-ICS24-02`: `cpu_update` largest when not oversubscribed, data movement under half the cost).
2. **Discrete-GPU unified memory on AMD goes through HMM.** The paper states dGPU systems use "Heterogeneous Memory Management (HMM) to allow the GPU to address the system memory." `[paper]` So the 65% is the cost of the HMM fault-and-migrate path, not of PCIe bandwidth alone.
3. **MI300A removes the second physical memory.** It integrates AMD "Zen 4" EPYC CPU cores with third-generation CDNA compute units over a **unified physical memory** with HBM3, so "GPU threads emit loads and stores with the host pointer values as the base address" with no explicit data movement. `[paper]` There is no page to migrate because there is no other place for the page to be.
4. **The allocator consequence is the practically important one.** "On MI300A any memory allocator including `hipMalloc` will allocate unified memory, i.e. memory accessible by any compute element"; "the default C++ vector allocator can now be used"; memory from "standard OS allocators such as `mmap`, `sbrk`" works. `[paper]` This is what makes a million-line C++ code portable with O(100) line changes — the existing allocators stop being a problem.
5. **The residual root cause the paper cannot remove:** code, unlike data, is not unified — "code that has been compiled for the host cannot be executed on a GPU device." `[paper]` Hence `declare target` markup is still required for functions called inside kernels whose implementations are not visible at compile time.

## 12.5 Mathematical / performance model

No performance model. The one decision rule the paper formalises is the offload cut-off `[paper]`:

```
#pragma omp target teams distribute parallel for if(target: loop_len > TARGET_CUT_OFF)
```

i.e. a static threshold on loop length below which the loop runs on the host cores instead of being offloaded. The value of `TARGET_CUT_OFF` and any sensitivity study for it are `NOT_IN_PAPER`.

Figure of merit: "average time of execution per time-step (in sec.)". `[paper]`

## 12.6 Data layout and ownership

This is where the APU changes the model, so the hierarchy is worth stating carefully.

- **thread → wavefront → CU:** third-generation CDNA compute units. Exact CU count is **`NOT_IN_PAPER`** (the read text does not give it). `[paper]`
- **XCD / CCD counts, HBM3 capacity, memory bandwidth, Infinity Cache size, TDP, APUs per node:** all **`NOT_IN_PAPER`**. The paper "emphasizes unified physical memory but omits standard spec sheets." The only numeric hardware figure given for a comparison system is a "single-socket (64-cores) AMD EPYC 'Zen'4 CPU". `[paper]` No MI300A specification numbers are asserted here from vendor documentation, because that would be `VENDOR_DOCUMENTATION` evidence smuggled into a `[paper]` claim.
- **APU (MI300A) — the ownership unit that matters.** Host and device own *the same* physical pages. A host pointer is directly dereferenceable by GPU threads. `[paper]` The template's "host DRAM ↔ device HBM" distinction collapses here.
- **Program-stack vs heap detail the paper calls out:** unified-memory handling "includes program stack variables `dx` and `dy` and the host pointers they encapsulate for the vector data, which is allocated on the heap." `[paper]` That is, both the small stack-resident descriptor objects and the large heap arrays they point to must be reachable from the device — which on MI300A they are, without `map` clauses.
- **NUMA / first-touch page placement:** **`NOT_IN_PAPER`.** The read text does not discuss first-touch placement across the APU's memory controllers. For a shared-physical-memory APU this is exactly where a performance subtlety would live, and the paper does not address it.
- **node / cluster:** single-APU results only; multi-node scaling is listed as future work. `[paper]`

## 12.7 Pseudo code

All directives, clauses and the cut-off idiom are `[paper]`; the arrangement below is `[reconstruction]` of the porting recipe as described (Listings 4–6).

```
// once, per translation unit / program                         [paper]
#pragma omp requires unified_shared_memory
// -> compiler "maps pointers ... as zero-sized array sections", so no map clauses [paper]

// a hot loop in the CFD solver                                  [paper]
#pragma omp target teams distribute parallel for \
        if(target: loop_len > TARGET_CUT_OFF)                    // [paper]
for (label i = 0; i < loop_len; ++i) { ...; }

// any function called from inside a kernel whose body is not visible here  [paper]
#pragma omp declare target
inline scalar preconditionHelper(...);
#pragma omp end declare target

// allocation: nothing special is required                        [paper]
std::vector<scalar> v(n);        // default C++ allocator is fine on MI300A
scalar* p = (scalar*)malloc(...); // mmap/sbrk-backed memory is device-accessible
// hipMalloc also yields unified memory on MI300A
```

Removed relative to a discrete-GPU port: explicit `map(to:/from:/tofrom:)` clauses and the explicit host↔device copies they imply. `[paper]`

## 12.8 Real implementation

- **Application:** OpenFOAM, a production CFD library the paper characterises as roughly 1 M lines. `[paper]`
- **Loops/kernels ported, as named:** the momentum predictor solve, the pressure Poisson solve, the velocity field correction, the turbulence transport equations (described as lines 10, 19, 32 and 37 of a `simpleFoam`-style driver), plus the **PBiCGStab** linear-solver loops and the **DILUPreconditioner** implementation. `[paper]`
- **Change size:** O(100) lines. `[paper]`
- **Toolchain:** **ROCm-6.0**, **amdclang++ (clang-17.0)**, **OpenMP 5.2** (with references to 4.0/4.5/5.0). The paper states "ROCm supports the requirement and its implementation is based on AMDGPU Unified Memory support." CUDA comparison systems used **CUDA-12.2.2, clang-18.0**. `[paper]`
- **`HSA_XNACK` setting: `NOT_IN_PAPER`.** This is a notable omission — on discrete AMD GPUs `HSA_XNACK` is the switch that enables retry-fault-based unified memory, and the paper does not state whether or how it was set for the dGPU comparison runs. Any claim about it would be `[inference]` and is not made.
- **Upstreaming status:** "There is an ongoing effort to upstream our unified memory implementation in OpenFOAM (currently accessible through GitHub) to official repository." `[paper]` No URL captured; `NOT_INSPECTED`.

## 12.9 Kernel execution

Kernels are generated by the OpenMP compiler from `target teams distribute parallel for` regions, so the kernel → team → wavefront → instruction mapping is the compiler's. `[paper]` The two execution-level decisions the porting team retained are:

1. **Where to run a loop at all**, via the `if(target: loop_len > TARGET_CUT_OFF)` clause — small loops stay on the Zen 4 cores rather than paying kernel-launch cost for little work. `[paper]` On an APU this choice is cheap precisely because no data has to follow the decision.
2. **What code is callable from a kernel**, via `declare target`. `[paper]`

No occupancy, wavefront-scheduling or stall-reason data is reported → `NOT_IN_PAPER`.

## 12.10 Memory traffic

On MI300A there is no host↔device leg to characterise: "unified physical memory shared between CPU and GPU eliminates data replication," and page migration is removed entirely. `[paper]` The register ↔ LDS ↔ L1 ↔ L2 ↔ HBM3 path is untouched by the port.

The traffic claim that carries the paper is about the *baseline*, not the target: on discrete GPUs (MI210 over PCIe 4.0, A100-80GB SXM, H100-SXM), "more than 65% of the time is spent in page migrations: updating GPU tables and copying the data between host and device," for HPC_motorbike Large (34 M cells). `[paper]`

**Methodological caveat, important for grounding:** the measurement method behind the 65% figure is **not described** — no profiling tool (rocprof, Nsight, custom instrumentation) and no data-collection methodology is given; the paper states profiling "reveals" this. `[paper]` The number should therefore be reused only with the full qualifier "as reported by the authors' unspecified profiling of HPC_motorbike Large (34 M cells) on discrete GPUs," and not treated as a reproducible measurement.

## 12.11 Why it is faster/slower (decomposed)

Reported results, with their qualifiers `[paper]`:

- Benchmark: **HPC_motorbike, Large, 34 M cells, 20 time-steps**, figure of merit = average seconds per time-step.
- Configurations: MI300A (ROCm-6.0); x86 + MI210 (PCIe 4.0, ROCm-6.0); x86 + A100-80GB SXM (CUDA-12.2.2); x86 + H100-SXM (CUDA-12.2.2).
- **MI300A vs x86+H100-SXM: 4× speedup. MI300A vs x86+MI210: 5× speedup.** `[paper]`
- **1 MI300A with 1 CPU-core vs a single-socket Zen 4 CPU (64 cores): 2× better.** `[paper]`
- Multi-process: "tests with 3–6 CPU-cores per APU gives 2× better performance," though the reported figures use a single CPU core "for clarity." `[paper]`

Causal decomposition:
1. **The dominant term removed is the page-migration path**, quantified at >65% of dGPU time for this benchmark. `[paper]` If 65% of time is migration and migration goes to zero, the remaining work alone bounds the speedup near 3×; the reported 4× against H100 implies additional differences (different vendor, different memory system, different compiler) that the paper does **not** decompose. This is an `[inference]` about the arithmetic, not a paper claim, and it means the 4× is *not* attributable to unified physical memory alone.
2. **The comparison is cross-vendor and cross-toolchain.** MI300A on ROCm-6.0/clang-17 versus H100 on CUDA-12.2.2/clang-18, with the same OpenMP source. Compiler-quality and kernel-quality differences are not isolated. `[inference]`
3. **The CPU-baseline comparison is the cleanest one**: same physical memory, same node, 1 core + APU versus 64 cores. `[paper]`
4. **Productivity is the second, independent result** and does not depend on the timing comparison at all: O(100) lines against ~1 M, with explicit `map` clauses and copies deleted rather than rewritten. `[paper]`

## 12.12 Hardware generation dependence

- **Strictly requires an APU with unified *physical* memory** — MI300A specifically, where "any memory allocator including `hipMalloc` will allocate unified memory." `[paper]` On a discrete GPU the same source compiles but goes back through HMM migration, which is the ≥65% cost.
- **Requires ROCm-6.0-era OpenMP support** for `requires unified_shared_memory` with pointers "mapped … as zero-sized array sections." `[paper]`
- Authors state plainly: "Unified memory addressing is not available on all CPU + GPU platforms." `[paper]`
- MI300A hardware specification numbers (CU/XCD counts, HBM3 capacity, bandwidth, Infinity Cache, TDP) are **`NOT_IN_PAPER`** and are deliberately not filled in from vendor documentation here.

## 12.13 Limitations

Author-stated `[paper]`:
1. "Unified memory addressing is not available on all CPU + GPU platforms."
2. Prior work on discrete systems was "associated with higher than expected overheads."
3. Functions whose implementations are not visible at compile time require manual `declare target` markup.
4. Code is not unified even though data is: "code that has been compiled for the host cannot be executed on a GPU device."
5. The authors situate their contribution against a literature where "the majority of work has leveraged benchmarks and mini-apps," i.e. they claim novelty in applying this to a production code — implicitly conceding that prior unified-memory OpenMP evidence was small-scale.
6. Upstreaming to the official OpenFOAM repository is incomplete.

Observed here, not claimed `[inference]`:
7. **The 65% page-migration figure has no stated measurement methodology** — no tool, no counters, no procedure. It is the load-bearing motivation number of the paper.
8. **`HSA_XNACK` is never mentioned**, so the exact unified-memory mode of the discrete-GPU baselines is unspecified. On AMD dGPUs this materially changes the fault path.
9. **No MI300A hardware specification table**, so the results cannot be normalised per-CU, per-GB/s or per-watt against the H100/A100/MI210 comparison systems.
10. **Cross-vendor, cross-toolchain comparison is not decomposed**, so the 4×/5× figures conflate unified physical memory with vendor, compiler and memory-system differences.
11. **No first-touch / NUMA page-placement analysis** on the APU's shared memory, which is the most likely site of residual performance sensitivity on this class of hardware.
12. Single benchmark (HPC_motorbike) and single application (OpenFOAM); single APU, no multi-node scaling.
13. Analysed from the arXiv preprint; the IEEE open-access camera-ready was not reachable (`ieeexplore.ieee.org` HTTP 418 here).

## 12.14 Relation to prior corpus

- `prior_corpus_check`: **`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`.** This is an ISC High Performance research paper about porting a production HPC application, and therefore plausibly belongs to the ~80-paper AI/HPC systems corpus recorded as `EXTERNAL_IMPORT_PENDING` under `domains/ai_hpc_systems/` and absent from this repository. No claim is made as to whether an analysis exists there. Within *this* repository the only hit is `domains/gpu_systems/census/ISC_2024.md`.
- **Lineage verified from the paper's own related work** `[paper]`: **Mishra et al. (2017)**, "Benchmarking and evaluating unified memory for OpenMP GPU offloading"; **Martineau & McIntosh-Smith (2017)** on OpenMP 4.5 portability across Intel, IBM and NVIDIA; **Grinberg, Bertolli & Haque (2017)**, "Hands on with OpenMP 4.5 and unified memory" on IBM hybrid systems — note Grinberg and Bertolli (as Bercea/Bertoli) are also authors here, so this is a direct continuation of that line by the same people. Frameworks/libraries named: OpenMP, OpenACC, HIP, CUDA, PETSc, Ginkgo, **Kokkos** (memory abstraction) and **Umpire** (memory management). OpenFOAM GPU precedents named: **Jasiński (2015)** GPU fork; **Mills et al. (2021)** PETSc interface.
- **Directly complementary within this cluster, and the more important pairing:** the ICS 2024 AMD SVM characterization (`GPU-ICS24-02`) measures the *same vendor's discrete-GPU* unified-memory path and finds, independently, that host page-table maintenance (`cpu_update`) plus DMA setup plus allocation dominate over actual data movement. This paper's ">65% in page migrations: updating GPU tables and copying the data" is the same decomposition seen from the application side. Together they make the cluster's clearest architectural argument: on AMD discrete GPUs the unified-memory cost is *driver bookkeeping*, and MI300A's answer is to delete the mechanism rather than tune it. **No citation link between the two papers was verified** — this is a convergence of independent evidence, stated as `[inference]`.
- **Related watchlist item:** *One Memory-Many Paths: Early Experiences with Allocation and Data Copy Strategies on MI300A* (IPDPS 2026, OSU NOWLAB, Best Paper Finalist) is the direct follow-on question — which allocation and copy path to choose on MI300A — and no public full text was reachable. `[official-web, via census/IPDPS_2026.md]`
- `EXISTING_CORPUS_DUPLICATE`: **cannot be determined** for the external corpus; **no** within this repository.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** `[paper]`-grounded reasons: (a) the contribution is defined by the difference between GPU unified *virtual* memory (which "requires page migrations" and costs >65% of runtime on the evaluated dGPUs) and the MI300A APU's unified *physical* memory — a GPU-memory-architecture distinction; (b) the enabling semantics are GPU-specific: `#pragma omp requires unified_shared_memory` as implemented by ROCm on "AMDGPU Unified Memory support," and the fact that `hipMalloc` and even `mmap`/`sbrk` memory becomes device-accessible; (c) the residual porting work exists because **GPU code**, unlike data, is not unified, forcing `declare target`; (d) the baselines against which the result is claimed are named GPU products (MI210, A100-80GB SXM, H100-SXM) running the same OpenMP offload source.

verdict_basis: the contribution rests on the GPU/APU memory-architecture difference between migration-based GPU unified virtual memory and MI300A's shared physical memory, expressed through ROCm's AMDGPU unified-memory implementation of OpenMP `requires unified_shared_memory`; on a CPU there is no offload target, no migration path and therefore no contribution. Verdict `CORE_GPU`, noting that this is an application-porting and programming-model paper rather than a GPU mechanism design.

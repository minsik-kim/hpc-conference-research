# GPU compilers, programming models, JIT, IR and lowering, kernel fusion and code generation, GPU memory models and correctness tooling at the language level — GPU relevance verdict ledger

cluster: taxonomy `H` (compilers / programming models / IR / lowering) and `I` (kernel fusion / code generation), with the language-level memory-model and memory-safety tooling that belongs with them
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
stable_id_band: `GPU-<VENUE><YY>-141` .. `-159` (assigned by STEP C cluster brief; IDs are never reused)

Verdicts are `CORE_GPU` / `RELATED_GPU` / `EXCLUDE` / `UNRESOLVED`.
Access states are `PUBLIC_FULLTEXT` / `CLOSED_ACCESS` / `PENDING_FULLTEXT` /
`PUBLIC_ARTIFACT_ONLY` / `ABSTRACT_ONLY`.
`evidence_read` records what was actually read — a verdict reached from an
abstract says `ABSTRACT_ONLY` and may **not** be used to justify a deep analysis.

**Counterfactual answer** records: "If a generic accelerator or a CPU were used
instead, would the core contribution be substantially the same?" A `NO` must
name the GPU-specific property the design depends on. **The strict form of the
test governs this cluster**: a compiler can be GPU-*targeted* without being
GPU-*specific*. A retargetable tensor compiler that happens to emit PTX is
`RELATED_GPU`, not `CORE_GPU`.

**Stack level** records where the contribution lives:
`source language` → `framework` → `C/C++` → `CUDA/HIP/Triton` → `kernel` →
`PTX/ISA` → `library/runtime`.

**Tooling constraints that shaped the access states** (do not re-derive):
`dl.acm.org` → 403 (including its "open PDF" paths), `ieeexplore.ieee.org` → 418,
`dblp.org` → robots-blocked, `par.nsf.gov` → robots-disallowed,
`arxiv.org/search` / `export.arxiv.org` / `web.archive.org` → unavailable.
`arxiv.org/html/<id>vN` and author/institution PDFs work. GitHub is reachable
from Bash, so several `CLOSED_ACCESS` papers still have inspected `[code]`.

**Standing caveat — `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`.**
`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`: an ~80-paper AI/HPC
corpus outside this repository that is explicitly stated to include "GPU
compiler/kernel" work. A large fraction of this cluster plausibly belongs to it.
Every deep-learning-facing compiler/fusion paper below is therefore flagged
`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`, and **nothing is asserted** about whether
it is in fact duplicated there. Absence from this repository is not evidence of
novelty (`governance/ANTI_HALLUCINATION_RULES.md`).

---

## Priority papers

| Paper | Venue/Year | Stable ID | Access state | Evidence read | Stack level | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|---|---|
| Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation | ASPLOS 2026 | `GPU-ASPLOS26-141` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via arXiv HTML 2504.12984v1 (preprint titled *A Virtual Machine for Arbitrary Low-Precision GPGPU Computation in LLM Serving*) + `[code]` github.com/NVIDIA/tilus @ `4597cd5ba3f24501ba411cefa61a76fd9d3ba2c8` | source language → kernel (lowers via Hidet IR → CUDA C → nvcc) | `NO` | The layout monoid over `local`/`spatial` exists to name the register-fragment map a tensor-core `mma` imposes (paper's own example `local(2,1).spatial(8,4).local(1,2)`); the semantic unit is the CUDA thread block ("SIMB") and the IR surfaces `cp.async`/TMA/`mbarrier`/`tcgen05` one-to-one. | `GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md` |
| Towards Unified Analysis of GPU Consistency | ASPLOS 2024 (29V4; presented 2025) | `GPU-ASPLOS24-142` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via author PDF hernanponcedeleon.github.io/pdfs/asplos2024.pdf | PTX/ISA (reached from CUDA and SPIR-V/OpenCL) | `NO` | Every added `.cat` construct is GPU-only — scopes (CTA/GPU/SYS, Subgroup/Workgroup/Queue-family/Device; `sr`,`scta`,`ssg`,`swg`,`sqf`), proxies (`GEN`/`TEX`/`SUR`/`CON` and morally-strong condition ms2), storage classes `SC0`/`SC1`, availability/visibility `AV`/`VIS`. That the checker runs on a CPU is irrelevant; the object formalised is the GPU consistency spec. | `GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md` |
| CHERI-SIMT: Implementing Capability Memory Protection in GPUs | ASPLOS 2026 | `GPU-ASPLOS26-143` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via authors' Cambridge PDF + `[code]` github.com/CTSRD-CHERI/SIMTight @ `6248c9b727d1f32280997492ecb0179d045eb674` | C/C++ → PTX/ISA → SIMT microarchitecture (CHERI-LLVM + 33 RISC-V CHERI instructions + register-file design) | `NO` | The enabler is warp-granular value regularity: capability *metadata* is uniform/affine across 32 lanes while addresses are not, so the metadata register file scalarises into the SRF; plus a lane-shared bounds unit (<1% dynamic) and an Active-Thread-Selection PC exemption. On a CPU, CHERI already costs a plain 2× with no scalarisation to recover. | `GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md` |
| FlashFuser: Expanding the Scale of Kernel Fusion for Compute-Intensive Operators via Inter-Core Connection | HPCA 2026 | `GPU-HPCA26-144` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via arXiv HTML 2512.12949v1; no artifact located (`NOT_INSPECTED`) | framework → kernel (CUDA/CUTLASS codegen) | `NO` | Promotes Hopper **distributed shared memory** (thread-block clusters, ≤16 blocks on H100) to a compiler-schedulable tier between SMEM and L2, with `dsm_all_exchange`/`dsm_shuffle`/`dsm_reduce_scatter` on TMA + `mbarrier`. Its own ablation prices the non-DSM residue at 1.52× of 3.29×, so >half the contribution is the GPU feature. | `GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md` |
| Taking GPU Programming Models to Task for Performance Portability | ICS 2025 | `GPU-ICS25-145` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via ICS 2025 proceedings PDF (hpcrl.github.io/ICS2025-webpage/…/ics25-63.pdf); arXiv 2402.08950 is the preprint; no artifact located | source language → framework (Kokkos/RAJA/SYCL/OpenMP/OpenACC) → CUDA/HIP → kernel | `NO` | The P∥ metric is generic, but every root cause the paper isolates is GPU-architectural: registers per thread and spilling, occupancy and eligible-warp counts, barrier warp stalls, compiler-chosen threads-per-block, in-kernel dynamic shared memory, and warp-shuffle primitives as the correct reduction lowering. | `GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md` |
| Gallatin: A General-Purpose GPU Memory Manager | PPoPP 2024 | `GPU-PPoPP24-146` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via author PDF (prashantpandey.github.io/uploads/ppopp24-final274.pdf) + `[code]` github.com/saltsystemslab/gallatin @ `f65a085414527c95c7197b724c90cb9740f105dc` | library/runtime, called from CUDA device code | `NO` | The vEB node is shrunk to 64 bits — abandoning its O(log log u) bound — so each node op is one device atomic; allocation is batched per-warp via `cooperative_groups::coalesced_threads`; the block buffer is keyed on the streaming multiprocessor. All three are SIMT/atomic-width constraints with no CPU analogue. | `GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md` |

---

## Priority papers that did not clear the full-paper gate

These were assigned as priority items but **no full text was reachable from this
environment**. The gate in the cluster brief is explicit: *abstract-only or
artifact-only ⇒ verdict allowed, deep analysis NOT allowed*. All four are
**watchlisted**.

| Paper | Venue/Year | Stable ID | Access state | Evidence read | Stack level | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|---|---|
| Triton-Sanitizer: A Fast and Device-Agnostic Memory Sanitizer for Triton with Rich Diagnostic Context | ASPLOS 2026 | — (none assigned; no deep analysis) | `ABSTRACT_ONLY` + `PUBLIC_ARTIFACT_ONLY` | Full abstract verbatim via hgpu.org/?p=30696 and the authors' page jokeren.tech; `dl.acm.org/doi/pdf/10.1145/3779212.3790241` returns **403** despite the census recording it as an open publisher PDF. `[code]` github.com/Deep-Learning-Profiling-Tools/triton-viz @ `203b0c7cbb35448d53f3cf5359db55e0d4fb3522` — contains `triton_viz/clients/sanitizer/{sanitizer,report,range_summary,data}.py`, `triton_viz/clients/symbolic_engine.py`, `triton_viz/clients/race_detector/{race_detector,hb_solver}.py`, `triton_viz/core/{patch,symbolic_metadata,masked_load_store}.py` and frontends for `triton`, `gluon`, `nki` | source language (Triton) → kernel; a sanitizer that works on Triton tile semantics *instead of* instrumenting PTX/SASS | `NO (abstract-level)` | Abstract: "leverages **Triton's tile-oriented semantics** to construct symbolic expressions for memory addresses and masks, verifies them with an SMT solver, and selectively falls back to eager simulation for indirect accesses", avoiding "per-access instrumentation"; the named baseline is **compute-sanitizer**, which instruments "every memory instruction in low-level IRs or binaries". Reported: 24 previously unknown errors across seven Triton repositories, 8 upstreamed; 1.07×–14.66× (avg 1.62×) vs compute-sanitizer. **The answer is provisional — reached from the abstract plus the group's repository, not from the paper.** | none — `WATCHLIST` |
| CUDASTF: Bridging the Gap Between CUDA and Task Parallelism | SC 2024 | — | `CLOSED_ACCESS` | Bibliographic record + abstract fragments from the author's page mgarland.org/papers/2024/cudastf/ (no PDF linked there); `ieeexplore.ieee.org` → 418 and `dl.acm.org` → 403, both per standing tooling constraints, not retried. Implementation is public as `cudax::stf` inside NVIDIA CCCL (`nvidia.github.io/cccl/cudax/stf.html`) — `[documentation]`, `NOT_INSPECTED` | library/runtime over CUDA (C++ header library; sequential-task-flow over CUDA streams/graphs) | `NO (abstract/venue-level)` | Author-page abstract: a C++ Sequential Task Flow layer "over CUDA" with data-driven dependencies for single- and multi-GPU programs; reported "up to a 1.8x improvement over the **cuSolverMg** library on Cholesky decomposition" and "**CUDA Graphs** improve performance by up to 30%" on single-GPU. The named mechanisms — CUDA streams/events, CUDA Graphs, the host/device launch split — are GPU runtime objects, so `NO` is likely; but it rests on an abstract, so it is provisional. | none — `WATCHLIST` |
| CKTI: A Domain-Specific Compiler for Lowering CUDA Kernels to Triton-IR | ICS 2026 | — | `CLOSED_ACCESS` | Title and **DOI `10.1145/3797905.3800551`** recovered by search (this is a **census correction** — `domains/gpu_systems/census/ICS_2026.md` row 3 records the DOI as `UNKNOWN`). No preprint, author PDF or artifact located. Abstract not read | `CUDA/HIP/Triton` → `CUDA/HIP/Triton` — a source-to-source lowering *between* two GPU kernel languages | `NO (title-level)` | Both the source and the target of the translation are GPU kernel languages (CUDA; Triton-IR), so the artefact cannot exist off a GPU. **`UNRESOLVED` on the evidence actually read** — the title alone cannot establish what the compiler does or why. | none — `WATCHLIST`, highest priority of the four |
| MCFuser: High-Performance and Rapid Fusion of Memory-Bound Compute-Intensive Operators | SC 2024 | — | `PUBLIC_FULLTEXT` | `FULL_PAPER` via arXiv HTML 2506.22169v1 — read in full (motivation and the MBCI operator class, tiling expressions with deep vs flat tiling, the L/C/S memory primitives and DAG-based redundant-access removal, four pruning rules, the closed-form cost model, the evolutionary search, the TVM front-end / Triton back-end split, evaluation, ablation) | framework → CUDA/Triton (TVM Relay/TIR front-end, Triton back-end emitting PTX) | **`YES`** | **The strict test fails here.** The contributions — an enlarged fusion search space (deep *and* flat tiling), DAG-based elimination of redundant memory statements, and a closed-form analytical cost model replacing Ansor's ML-guided search — are stated over an abstract loop/tile/scratchpad machine. Every genuinely GPU-specific decision (coalescing, vectorisation, **tensor-core scheduling**, shared-memory management, PTX emission) is explicitly **delegated to Triton**; MCFuser's own model touches the GPU only through a shared-memory capacity bound, tile sizes as multiples of 16, and an `α = (N_block + N_SM)/N_block` wave-quantisation factor. This is the brief's stated `RELATED_GPU` shape: a retargetable fusion compiler that happens to emit PTX. | none — deep analysis **withheld by verdict**, not by access |

---

## Verdict-only papers

Resolved to an access state and a verdict. Deep analysis was performed only
where the full paper was read **and** the verdict is `CORE_GPU`; every other row
is verdict-only by the gate, by the verdict, or by capacity. Rows whose evidence
is a title or a census line are marked `UNRESOLVED` rather than given a
speculative verdict.

| Paper | Venue/Year | Stable ID | Access state | Evidence read | Stack level | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|---|---|
| Static Generation of Efficient OpenMP Offload Data Mappings (**OMPDart**) | SC 2024 | `GPU-SC24-147` | `PUBLIC_FULLTEXT` | `FULL_PAPER` via arXiv HTML 2406.13881v1; Zenodo artifact `zenodo.org/records/12562040` located but `NOT_INSPECTED` | C/C++ → framework (OpenMP target offload); Clang/LLVM source-to-source | `NO` (**boundary**) | Its output artefact *is* the host/device data-movement program (`map`/`update`/`target data`) and its analysis state is "variable validity in each memory space"; on a single-address-space machine it computes nothing. Counter-argument recorded in the file: nothing is GPU- as opposed to accelerator-specific, and no intra-kernel reasoning exists at all. | `GPU-SC24-147--ompdart-static-generation-openmp-offload-data-mappings.md` |
| Composing Distributed Computations Through Task and Kernel Fusion (**Diffuse**) | ASPLOS 2025 | — | `PUBLIC_FULLTEXT` | `FULL_PAPER` via author PDF lightsighter.org/pdfs/Legate_Kernel_Fusion___ASPLOS_2025.pdf (arXiv 2406.18109); DOI `10.1145/3669940.3707216`, 30V1 | framework → MLIR → {NVPTX kernel, OpenMP CPU} | **`YES`** | Scale-free IR over Stores/Partitions/IndexTasks plus four communication constraints (launch-domain-equivalence, true-, anti-dependence, reduction), then MLIR `memref`/`affine`/`arith` loop fusion lowered to **either** NVPTX **or** OpenMP CPU code. Evaluation is GPU-only (1–128 A100, NVLink, 8 NICs; geomean 1.86×, range 0.93×–10.7×) but the paper "does not separately isolate GPU-specific benefits" and the mechanism is a distributed-task-graph analysis. Textbook `RELATED_GPU`. | none |
| cuJSON: A Highly Parallel JSON Parser for GPUs | ASPLOS 2026 | — | `PUBLIC_ARTIFACT_ONLY` | Census row only (31V1, `10.1145/3760250.3762222`); `dl.acm.org` 403; no preprint located. Repository github.com/AutomataLab/cuJSON exists (`NOT_CLONED` — no capacity) | kernel (data-parallel parsing) | `NO (title/census-level)` | Census describes "warp-level tokenisation and structural-index construction" — a warp-granular mechanism — so `NO` is likely, but nothing beyond the title and the census line was read. Deep analysis **not permitted** by the gate. | none — `WATCHLIST` |
| Interactive Debugger for Performance Portable Python HPC Kernels (**pkdb**) | SC 2026 (`SC26_MEMBERSHIP_UNVERIFIED` per census) | — | `PENDING_FULLTEXT` + `PUBLIC_ARTIFACT_ONLY` | **arXiv 2609.07912 could not be fetched — five attempts across `/abs` and `/html` all returned HTTP 429.** The profiling cluster reported the same failure; this is now independently confirmed twice and should be treated as a standing blocker, not retried. `[README]` + `[code]` github.com/EngineeringSoftware/pkdb @ `abbe687eb81686edecd158ceea52684b7e6ac8b2`: README states "Artifact for SC'26. Interactive debugger for PyKokkos kernels", enabling "breakpoints, stepping, continuation, and variable inspection while preserving actual on-device execution without source modification", plus "(i) live code evaluation, (ii) kernel call-site substitution, and (iii) concurrent kernel comparison"; the prerequisite table maps target **OpenMP→gdb, Cuda→cuda-gdb, HIP→rocgdb**; tree contains `pkdb/`, `pykokkos/` (a modified PyKokkos), `benchmarks/`, `examples/`, `report/` | source language (Python/PyKokkos) → CUDA/HIP → kernel, via the vendor device debuggers | `NO (README-level)` | It drives **cuda-gdb** and **rocgdb** to debug a Python kernel *while it executes on the device*, so the artefact is built on GPU debugger interfaces. Provisional: reached from the README and repository layout, **not** from the paper. Deep analysis **not permitted** by the gate. | none — `WATCHLIST`, high priority: the arXiv blocker is the only obstacle |
| Dynamic Detection of Inefficient Data Mapping Patterns in Heterogeneous OpenMP Applications | PPoPP 2026 | — | `PENDING_FULLTEXT` | **arXiv preprint located: `2601.12713`** (this is a **census correction** — `domains/gpu_systems/census/PPoPP_2026.md` records the artifact/preprint as `NOT_FOUND_AFTER_SEARCH`). The fetch returned HTTP 429 and was not retried. Census notes the abstract "speaks of 'accelerators' and OMPT tracing generically; **no GPU, CUDA or vendor device is named**" | framework (OpenMP runtime / OMPT tracing) | `UNRESOLVED` | Dynamic sibling of OMPDart (`GPU-SC24-147`) — same object (offload data mappings), opposite method (runtime tracing vs static analysis). Whether a GPU-specific mechanism is central is `UNKNOWN`; census records GPU centrality as PARTIAL/unnamed. Re-screen once arXiv 2601.12713 is reachable. | none — `WATCHLIST` |
| ParDiff: Efficiently Parallelizing Reverse-Mode Automatic Differentiation with Direct Indexing | PPoPP 2026 | — | `CLOSED_ACCESS` (paper) + `PUBLIC_ARTIFACT_ONLY` | Census row (paper `3786444`-adjacent id `3786418`, Parallel Algorithms session); abstract not read. `[code]` github.com/roastduck/FreeTensor @ `dba04df4994610c70c7f9696d5c4c7619cd5050a` — tree carries `src/autograd/`, `src/codegen/`, `src/cutlass_micro_kernel_property.cc`, and **parallel `cuda-mkl-dev` / `clang-mkl-dev` Dockerfiles plus `with-cuda.toml` and `with-mkl.toml`**, i.e. a CPU (MKL) backend and a CUDA backend of equal standing | framework → {CUDA kernel, CPU} | **`YES` (provisional)** | Census records the abstract as naming "multi-core CPUs and GPUs"; the host compiler (FreeTensor) is demonstrably dual-backend at commit `dba04df`. A reverse-mode-AD parallelisation scheme with direct indexing is a dataflow transformation, not a GPU mechanism. `RELATED_GPU` pending the abstract. | none |
| FlashTensor: Optimizing Tensor Programs by Leveraging Fine-grained Tensor Property | PPoPP 2025 | — | `CLOSED_ACCESS` | Census row only; `dl.acm.org` 403, no preprint located. Census: "Title has no GPU term; abstract names H100 and A100 GPUs" | framework → kernel (tensor-program optimiser) | `UNRESOLVED` | Naming H100/A100 as evaluation hardware does not establish a GPU-specific *mechanism* — precisely the `RELATED_GPU` trap this cluster's strict test is designed to catch. No verdict on the evidence read. | none — `WATCHLIST` |
| MetaAttention: A Unified and Performant Attention Framework Across Hardware Backends | PPoPP 2026 | — | `CLOSED_ACCESS` | Census row only. Census, verbatim: "**Abstract names no device** — listed as a candidate on title/venue-section grounds only" | framework → kernel (multi-backend attention) | `UNRESOLVED` | "Across Hardware Backends" in the title is an explicit claim of *retargetability*, which under this cluster's strict test points toward `RELATED_GPU` — but an unread abstract cannot settle it either way. | none — `WATCHLIST` |
| ConCo: Optimizing Compilation of Concurrent Tensor Programs on Shared GPU | ICS 2025 | — | `CLOSED_ACCESS` | Census row only (Optimizing Compilation session); no preprint located | framework → kernel/runtime (co-scheduling of concurrent tensor programs) | `UNRESOLVED` | "Shared GPU" concurrency implies SM partitioning / co-residency reasoning, which would be GPU-specific — but this is inference from a title. No verdict. | none — `WATCHLIST` |
| A Sample-Free Compilation Framework for Efficient Dynamic Tensor Computation | SC 2025 | — | `CLOSED_ACCESS` | Census row only (`10.1145/3712285.3759779`); `dl.acm.org` 403; no preprint located | framework → kernel (tensor compiler; cost model without measurement sampling) | `UNRESOLVED` | "Sample-free" indicates an analytical cost model replacing profiling search — the same shape as MCFuser, which this cluster judged `RELATED_GPU`. Suggestive only; no verdict on a title. | none — `WATCHLIST` |
| Accelerated Auto-Tuning of GPU Kernels for Tensor Computations | ICS 2024 | — | `CLOSED_ACCESS` | Census row only (Chendi Li, Yufan Xu, Sina Mahdipour Saravani, P. Sadayappan; session 9B — Software Design for Accelerators) | framework → kernel (autotuner) | `UNRESOLVED` | An autotuner's search is usually device-agnostic with GPU-specific search *bounds*; that is the `RELATED_GPU` shape, but the title alone cannot establish it. | none — `WATCHLIST` |
| A Holistic Approach to Automatic Mixed-Precision Code Generation and Tuning for Affine Programs | PPoPP 2024 | — | `CLOSED_ACCESS` | Census row only (`10.1145/3627535.3638484`). Census, verbatim: abstract "names 'programming models on CPUs and GPUs' (GPU centrality PARTIAL)" | source → C/C++ (polyhedral/affine mixed-precision codegen) | **`YES` (provisional)** | A polyhedral mixed-precision tuner that explicitly targets both CPUs and GPUs is retargetable by construction; `RELATED_GPU` unless the full text shows a GPU-specific numeric mechanism (e.g. tensor-core format selection). Provisional — census-level only. | none |
| HPAC-ML: A Programming Model for Embedding ML Surrogates in Scientific Applications | SC 2024 | — | `CLOSED_ACCESS` | Census row only (`10.1109/SC41406.2024.00078`); census tag is `[title-inference]` | source language → framework (pragma-based surrogate substitution) | `UNRESOLVED` | A directive-level programming model for swapping a physics kernel for an ML surrogate; device offload is incidental to the abstraction. Likely `RELATED_GPU`, but no evidence beyond the title was read. | none — `WATCHLIST` |
| SYCL++: Unified Programming for Heterogeneous Supercomputers at Scale | HPDC 2026 | — | `CLOSED_ACCESS` | Census row only; census marks it **TITLE-ONLY / UNVERIFIED** and its GPU relevance "**Inferred; unverified**" | source language → framework (SYCL dialect/extension) | `UNRESOLVED` | "Unified … Heterogeneous … at Scale" is an explicit portability claim, the `RELATED_GPU` shape; but the census itself refuses to verify the row. No verdict. | none — `WATCHLIST` |
| Moirae: Generating High-Performance Composite Stencil Programs with Global Optimizations | SC 2024 | — | `CLOSED_ACCESS` | Census row only (`10.1109/SC41406.2024.00026`); census tag `[title-inference]`, "GPU backend plausible but unverified" | framework → kernel (stencil DSL / codegen) | `UNRESOLVED` | Stencil compilers are classically dual-target (CPU vector + GPU). Whether Moirae's "global optimizations" rest on shared memory / warp structure is `UNKNOWN`. Compare `GPU-PPoPP24-01` (ConvStencil) and `GPU-PPoPP26-01` (SpTCStencil), both of which *are* `CORE_GPU` because they target the matrix unit — Moirae has no such claim in its title. | none — `WATCHLIST` |
| HERO-Sign: Hierarchical Tuning and Efficient Compiler-Time GPU Optimizations for SPHINCS+ | HPCA 2026 | — | `CLOSED_ACCESS` | Census row only (Yaoyun Zhou et al.; main conference; DOI `UNKNOWN`, artifact `NOT_FOUND_AFTER_SEARCH`) | framework → kernel (compile-time GPU optimisation for a post-quantum signature scheme) | `NO (title-level)` | The title states "**GPU Optimizations**" as the contribution and the venue is HPCA; a hash-based signature scheme's GPU implementation turns on warp-level hash scheduling and occupancy. `NO` is likely but is **title-level only** — recorded as provisional, not as a resolved verdict. | none — `WATCHLIST` |
| A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs | MICRO 2024 | — | `CLOSED_ACCESS` | Census row only (Zhuoran Ji et al.; session 3B Security: Accelerators and Cryptography; `ieeexplore.ieee.org` 418 per standing constraint). Census note: "CUDA-level scheduling is the mechanism" | CUDA → kernel (big-integer multiply scheduling) | `NO (census-level)` | Census records CUDA-level instruction scheduling as the mechanism, and big-integer multiply on a GPU turns on register pressure and carry-propagation across lanes. Provisional; abstract not read. | none — `WATCHLIST` |
| **Proteus JIT** — *Proteus: Portable Runtime Optimization of GPU Kernel Execution with Just-in-Time Compilation* | **CGO 2025**, *not* ISC 2026 | — | n/a — **correction only, not analysed** | Census correction, carried verbatim from `domains/gpu_systems/census/ISC_2026.md`: `NOT_IN_MAIN_POPULATION` as an ISC 2026 paper. The work is Georgakoudis, Parasyris, Beckingsale (LLNL), **23rd ACM/IEEE International Symposium on Code Generation and Optimization (CGO), March 2025, DOI `10.1145/3696443.3708939`** | — | — | **`EXCLUDE` (out of population)** | CGO is not one of this project's target venues. The correction is recorded here so the cluster's record and the census agree; **no analysis performed**, per the cluster brief. Note in passing: the same LLNL authors (Georgakoudis, Parasyris) are co-authors of `GPU-ICS25-145`. | none |
| GMLake | ASPLOS 2024 | `GPU-ASPLOS24-01` | — | — | — | — | already analysed | Skipped per the cluster brief; see `GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md`. | `GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md` |

---

## Stable IDs used by this cluster

`GPU-ASPLOS26-141`, `GPU-ASPLOS24-142`, `GPU-ASPLOS26-143`, `GPU-HPCA26-144`,
`GPU-ICS25-145`, `GPU-PPoPP24-146`, `GPU-SC24-147`.

Unused from the assigned band 141–159: **148–159**. No ID was reused; IDs were
assigned only to papers that received a deep-analysis file, so the band is not
burned on verdict-only rows.

## Census corrections produced by this cluster

1. `domains/gpu_systems/census/ICS_2026.md` row 3 (**CKTI**): DOI is
   `10.1145/3797905.3800551`, recorded there as `UNKNOWN`.
2. `domains/gpu_systems/census/PPoPP_2026.md` (**Dynamic Detection of
   Inefficient Data Mapping Patterns…**): an arXiv preprint exists,
   **2601.12713**; recorded there as `NOT_FOUND_AFTER_SEARCH`.
3. `domains/gpu_systems/census/ASPLOS_2026.md` row 9 (**Triton-Sanitizer**):
   the listed "open PDF on publisher" `dl.acm.org/doi/pdf/10.1145/3779212.3790241`
   returns **403** from this environment; it is not a usable full-text route.
   A full verbatim abstract is available at `hgpu.org/?p=30696`, and the author
   affiliation is **George Mason University**.
4. `domains/gpu_systems/census/ASPLOS_2026.md` row 8 (**Tilus**): the arXiv
   preprint 2504.12984 carries a **different title** —
   *A Virtual Machine for Arbitrary Low-Precision GPGPU Computation in LLM
   Serving*. Authors: Yaoyao Ding, Bohan Hou, Xiao Zhang, Allan Lin,
   Tianqi Chen, Cody Yu Hao, Yida Wang, Gennady Pekhimenko.
5. `domains/gpu_systems/census/SC_2024.md` row 14 (**MCFuser**): an arXiv
   preprint exists, **2506.22169**; authors Zheng Zhang, Donglin Yang (NVIDIA),
   Xiaobo Zhou (Univ. of Macau), Dazhao Cheng (Wuhan Univ., corresponding).
6. `domains/gpu_systems/census/SC_2024.md` row 15 (**OMPDart**): preprint
   **arXiv 2406.13881**; artifact **`zenodo.org/records/12562040`**.
7. `domains/gpu_systems/census/ICS_2025.md` row 22: full-text PDF is reachable at
   `hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-63.pdf`;
   preprint arXiv **2402.08950**; DOI `10.1145/3721145.3730423`.
8. `domains/gpu_systems/census/ASPLOS_2025.md` row 9 (**Composing Distributed
   Computations…**): the system is named **Diffuse**; full text at
   `lightsighter.org/pdfs/Legate_Kernel_Fusion___ASPLOS_2025.pdf`, preprint
   arXiv **2406.18109**.

# GPU-MICRO24-64 — Unleashing CPU Potential for Executing GPU Programs through Compiler/Runtime Optimizations

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT` (artifact is the **baseline** framework, not this paper's optimisations — see §12.8)
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — SIMT execution model as an object of translation: thread-block/warp/barrier semantics, divergence, coalescing` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `Compiler/runtime for GPU programming models; CPU-side execution of CUDA; heterogeneous resource utilisation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` + `CODE (of the baseline framework)` — motivation (idle-CPU argument, named CPU SKUs), background (flat collapsing, selective replication, Polly's affinity failure), all four optimisations with their pattern-matching conditions, evaluation setup (2× Intel Gold 6226R and ARM A64FX, 16 applications, three baselines with versions/commit), per-optimisation and combined results, hardware-counter evidence, limitations, related work. Code: `github.com/cupbop/CuPBoP` cloned at `508bd62e928bea3b5f0633c8fa63b5f42f3b4da0`; read `README.md`, `compilation/` tree, `KernelTranslation/include/cpu/*.h`.

## 12.1 Bibliographic facts

- **Title** [paper]: *Unleashing CPU Potential for Executing GPU Programs through Compiler/Runtime Optimizations*. (Census renders "Through"; the PDF renders "through". Same paper.)
- **Venue** [census]: MICRO 2024, Session 2B "Compiler Techniques/Optimizations". `ARCHIVAL_MAIN_PAPER`. The NSF-PAR PDF does not print the venue.
- **DOI**: `UNKNOWN`. Census gives `ieeexplore.ieee.org/document/10764678/` (→ 418, not retried).
- **Authors** [paper]: Ruobing Han, Jisheng Zhao, Hyesoon Kim — Georgia Institute of Technology, Atlanta, USA. (Census agrees.)
- **Access** [official-web]: NSF Public Access Repository PDF `par.nsf.gov/servlets/purl/10576251`, fetched 2026-09-18.
- **Artifact** [artifact]: `github.com/cupbop/CuPBoP` @ `508bd62e928bea3b5f0633c8fa63b5f42f3b4da0`.

## 12.2 Core question (one sentence)

Once a CUDA kernel has been mechanically flattened into CPU loops, what makes the result slow — and can the *GPU-specific* properties baked into the source (coalesced access, runtime block sizes, tail-block guards, one-block-per-thread mapping) be systematically undone so that ordinary CPU compiler optimisations start working again? [paper]

## 12.3 GPU/HPC problem translation

**Scheduling** and **memory locality**, expressed as a compiler/runtime problem.

The motivating observation is a resource-utilisation one: users "waiting for hours to have GPU devices scheduled while many CPUs remain idle" [paper], with CPU parts named (Intel Gold 6423N, 28 cores; AMD EPYC 9654, 96 cores; Fujitsu A64FX) as having capacity "comparable to GPUs."

**Important scope note for this cluster**: no GPU hardware is used anywhere in this paper. It contains **no GPU measurement and no GPU microarchitecture finding**. Its relevance here is that the *SIMT execution model* — blocks, warps, `__syncthreads`, coalesced access, grid/block dimensions — is the object being transformed, and each optimisation is defined by reversing a GPU-specific property. A reader looking for GPU hardware data should not come here.

## 12.4 Why the problem exists (hardware root cause)

[paper] The baseline technique is **flat collapsing** (MCUDA, POCL, CuPBoP, DPC++): a CUDA block becomes a CPU function run by a CPU thread; CUDA threads within the block become iterations of a "flat loop"; shared memory becomes a thread-local array; each `__syncthreads` splits the body into another sequential flat loop; thread-local variables are "selectively replicated" into arrays indexed by thread id.

The resulting code is pathological for CPU compilers on four counts, each traceable to a GPU property:

1. **Coalescing inverted.** A GPU kernel is written so that adjacent threads touch adjacent addresses; after flat collapsing, the inner loop is over threads, so each iteration jumps by a stride. What was perfect spatial locality on a GPU becomes a strided scatter on a CPU.
2. **Block size is a runtime value.** It is passed from the host module at launch, so the flat loops are dynamic loops with non-constant trip counts; the thread-index computation needs DIV/REM.
3. **Tail-block guards contaminate every block.** The `if (idx < n)` pattern that only matters in the last block is applied to all blocks, forcing masked load/store.
4. **Selective replication defeats dependence analysis.** LLVM Polly reports "The array subscript of 's' is not affine", blocking polyhedral optimisation entirely [paper].

## 12.5 Mathematical / performance model

No analytic model. The four optimisations and their measured contributions [paper] — all on **CPUs**, median of 7 runs, at `-O3`:

| Optimisation | What it reverses | Applies to | Gain |
|---|---|---|---|
| **Anti-coalescing transformation** | GPU memory coalescing | 4 of 16 apps | 24.46% (x86) |
| **Block size invariant analysis** | runtime-variable block size | 9 of 16 apps | 14.18% (x86) |
| **Tail block adaptive synchronization** | universal tail guards | 4 of 16 apps | 25.23% (ARM) |
| **GPU-block dynamic tiling** | 1 block : 1 CPU thread mapping | 3 of 16 apps | 53.46% |

Overall: **20.84% over the state-of-the-art baseline on x86, 16.10% on ARM**; 47.39% and 51.46% faster than MCUDA and DPC++ respectively [paper].

The anti-coalescing transformation is a loop interchange with a correctness argument:

```
before:  flat_loop(tid) { original_loop(index += stride) { A[index] } }
after:   original_loop      { flat_loop(tid) { A[linear index] } }
```
Enabled by *inserting a barrier* into the original CUDA loop so that flat collapsing is forced to generate the inner flat loop. Applicability is decided by a three-part pattern match [paper]: (1) a loop construct exists, (2) the stride is linear in the block dimensions, (3) the memory access is linear in the loop induction variable and the thread index. Loops are wrapped in `do-while` constructs with activation guards to preserve barrier correctness, and the paper gives a proof that iteration counts are identical.

Dynamic tiling is a runtime hill-climb [paper]: start with `blocks_per_thread = (grid_size × block_size) / num_CPU_cores`, then iteratively increase the tile and measure until no further improvement.

## 12.6 Data layout and ownership

The mapping the paper manipulates:

```
CUDA grid          -> parallel loop over CPU threads
CUDA thread block  -> a CPU function invocation   (baseline: 1 block : 1 CPU thread)
                   -> N blocks : 1 CPU thread     (this paper: dynamic tiling)
CUDA thread        -> one iteration of a "flat loop"
__syncthreads()    -> a split point between two sequential flat loops
__shared__ memory  -> a thread-local CPU array
thread-local var   -> an array indexed by thread id (selective replication)
```

The hardware asymmetry the tiling optimisation exists to bridge is quantified in the paper [paper]: a GPU SM at ~180 GFLOP/s with 192 KB of L1+shared, versus a CPU core at ~230 GFLOP/s with 2 MB of L2. A GPU block is sized for the first; running one per CPU core underuses the second.

## 12.7 Pseudo code

```
# --- Block size invariant analysis --------------------------------------- [paper]
# inter-procedural constant propagation over the HOST module
sizes = collect_launch_block_dims(host_module)      # cudaLaunchKernel arguments
if sizes are static constants:
    emit wrapper:
        switch (blockDim) {
          case s1: kernel_specialised_s1(...);      # DIV/REM -> SHIFT/AND
          ...
          default: kernel_generic(...);             # runtime path retained
        }
# effect: trip counts become constant -> vectoriser cost model now accepts the loop

# --- Tail block adaptive synchronization --------------------------------- [paper]
for each branch condition c in the kernel:
    if c depends only on grid/block dims AND diverges only in the LAST block:
        remove c from the non-tail specialisation
        keep  c in the tail specialisation
# effect: non-tail blocks need no masked load/store -> plain SIMD on ARM

# --- GPU-block dynamic tiling (runtime) ----------------------------------- [paper]
t = (grid_size * block_size) / num_CPU_cores
loop over repeated launches of a similar kernel:
    measure(t); t' = increase(t); measure(t')
    keep the better; stop when no improvement            # hill climbing
```

## 12.8 Real implementation

[artifact] `github.com/cupbop/CuPBoP` @ `508bd62e928bea3b5f0633c8fa63b5f42f3b4da0`.

**Important**: the paper evaluates against "**CuPBoP (commit fd5681)**" as the state-of-the-art *baseline* [paper], and the cloned repository is the CuPBoP framework itself. Grepping the tree for the paper's four optimisations returns **nothing**: no match for `coalesc`, none for `tiling`, and no pass corresponding to block-size-invariant analysis or tail-block adaptive synchronisation [code, verified]. **The public repository is the baseline framework, not this paper's optimised compiler.** Do not attribute the four optimisations to any symbol in it.

What the repository *does* contain, and what it establishes about the baseline [code]:

- `compilation/KernelTranslation/src/cpu/`: `generate_cpu_format.cpp`, `init.cpp`, `insert_sync.cpp`, `handle_sync.cpp`, `insert_warp_loop.cpp`, `warp_func.cpp`, `memory_hierarchy.cpp`, `performance.cpp`, `tool.cpp`.
- Declared entry points [code, headers]: `void insert_warp_loop(llvm::Module *M);`, `void split_block_by_sync(llvm::Module *M);`, `void handle_warp_vote(llvm::Module *M);`, `void handle_warp_shfl(llvm::Module *M);`, `void performance_optimization(llvm::Module *M);`.
  - `split_block_by_sync` is flat collapsing's barrier handling — **a `__syncthreads` literally becomes a basic-block split**, confirming the paper's description in code.
  - `handle_warp_vote` and `handle_warp_shfl` are the warp-level primitives (`__ballot`/`__any`/`__all`, `__shfl`) lowered explicitly; these are the COX-style extension the related work names.
  - `insert_warp_loop` is the warp-granularity loop construction.
- `compilation/HostTranslation/src/cpu/`: `RemoveMetadata.cpp`, `RemoveCudaBuiltin.cpp`, `ReplaceKernelArgs.cpp`, `ReplaceCudaBuiltin.cpp`, `ReplaceConstantMemory.cpp` — the host-side rewriting the paper's cross-module analysis depends on.
- `runtime/threadPool/` — the CPU thread pool that dynamic tiling would target.
- Prerequisites [README]: **LLVM 14.0.1** and a CUDA toolkit (needed only to produce NVVM/LLVM IR; "CuPBoP does not require NVIDIA GPUs"). Backends named: x86, AArch64, RISC-V, with Vortex (a RISC-V GPU) in progress.

## 12.9 Kernel execution

There is no GPU kernel execution. The kernel → block → warp → thread hierarchy is *realised* as loop nests, and the paper's contribution is choosing the nest order and specialising its bounds. The one place warps survive as a concept is `insert_warp_loop` / `handle_warp_vote` / `handle_warp_shfl` in the baseline framework [code] — warp-level primitives have no CPU equivalent and must be emulated across a group of 32 loop iterations.

## 12.10 Memory traffic

The anti-coalescing transformation is a locality fix, and the paper backs it with hardware counters [paper, Intel Gold 6226R]: for **Histogram**, the LLC hit rate rises to **72.2%**, against **90.83%** measured on a GPU for the same access pattern — i.e. the transformation closes part, not all, of the gap.

Vectorisation evidence [paper]:
- **2DCONV**: 23.1 M AVX instructions with block-size invariant analysis, **0 without**.
- **JACOB1D** on ARM A64FX: 92.3 M SIMD instructions with tail-block adaptive synchronisation, **24.4 K without**.

These two counter pairs are the cleanest causal evidence in the paper — they show the optimisations do not speed up existing vector code, they *enable* vectorisation that was previously rejected outright.

## 12.11 Why it is faster/slower (decomposed cause)

1. **Anti-coalescing (24.46%, 4 apps)**: converts a strided inner loop into a contiguous one. Pure spatial locality.
2. **Block size invariant analysis (14.18%, 9 apps)**: two effects — DIV/REM → SHIFT/AND for power-of-two block sizes, and constant trip counts that let the vectoriser's cost model accept the loop. The 2DCONV 0→23.1 M AVX figure shows the second effect dominates.
3. **Tail block adaptive synchronization (25.23% on ARM, ~0 on x86)**: **architecture-conditional by construction**. x86 has masked load/store, so removing the guard buys little; ARM A64FX does not, so removing it is the difference between SIMD and scalar. This is the paper's clearest demonstration that the right transformation depends on the *target*, not only on the source.
4. **GPU-block dynamic tiling (53.46%, 3 apps)**: the largest per-application effect. On FIR the tiling collapses 128 CPU threads to 8, a **75.98%** gain attributed to reduced synchronisation overhead [paper]. The cause is not locality but the elimination of per-block synchronisation and context switching for lightweight kernels.

The overall geomean (20.84% x86 / 16.10% ARM) is modest because each optimisation fires on only 3–9 of 16 applications.

## 12.12 Hardware generation dependence

- **CPUs measured** [paper]: two **Intel Gold 6226R** (x86) and one **Fujitsu ARM A64FX**. Real hardware, measured.
- **CPU SKUs cited in the motivation only, not measured**: Intel Gold 6423N, AMD EPYC 9654.
- **No GPU is used at any point.** The one GPU number in the paper — a 90.83% LLC hit rate for Histogram — is a reference point whose GPU SKU is not identified in what was read (`UNKNOWN`) and should not be reused.
- The x86/ARM split is load-bearing (masked load/store presence), so results do not transfer between the two. RISC-V is a supported backend of the framework [README] but is not evaluated in the paper.
- Baseline versions are pinned and should be quoted with the numbers: MCUDA v1.0.1, DPC++ v2024.0.2, CuPBoP commit `fd5681` [paper].

## 12.13 Limitations

Stated [paper]:
- Each optimisation has a narrow applicability predicate: anti-coalescing needs a global-memory coalescing pattern; block-size invariant analysis needs statically determinable block sizes in the host program; tail-block adaptive synchronisation only handles conditionals that diverge at the tail block; dynamic tiling needs **repeated launches of similar kernels** to hill-climb against.
- **Unsupported CUDA constructs**: C++ syntax, dynamic shared memory, texture memory, **atomic instructions**, and integer grid/block size types. **Manual preprocessing was required for many benchmarks.**
- Requires module-level inter-procedural analysis, which the paper notes is hard in modular compilation infrastructure; transformations are LLVM-IR specific.
- "GPU-to-CPU solutions are error-prone", and only "CUDA benchmarks that can be successfully migrated" were evaluated — i.e. the 16-application set is survivorship-filtered.

`[inference]`, not stated: excluding atomics excludes the entire class of kernels that rely on GPU scoped atomics and relaxed memory-model semantics, which is where the SIMT→MIMD translation is hardest. The reported speedups therefore characterise the tractable subset.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep for "CuPBoP" returns only `domains/gpu_systems/census/MICRO_2024.md`.
- **Mirror image, same conference**: `GPU-MICRO24-62` (ThreadFuser) analyses MIMD CPU programs under a SIMT model; this paper executes SIMT programs on MIMD CPUs. **Both appeared at MICRO 2024** and both treat the SIMT execution model as a translatable artefact rather than as hardware. Read together they show the SIMT/MIMD boundary itself became a 2024 research object.
- **Complementary**: `GPU-MICRO24-41` (over-synchronization in GPU programs) studies the cost of `__syncthreads` on GPUs; here `__syncthreads` is the construct that forces flat collapsing to emit an extra sequential loop, so barrier density is a cost on both sides of the translation. `[inference]` — neither paper cites the other.
- **Precursors cited** [paper]: **MCUDA** (2008, originator of flat collapsing), POCL and SYCL CPU backends, **COX** (extends flat collapsing to warp-level functions — the `handle_warp_vote`/`handle_warp_shfl` line in the artifact), Ocelot, **CuPBoP** itself, Cumulus (CUDA→C++ source translation), OCCA and Kokkos (library abstractions with JIT, to which the authors say their optimisations also apply), Majeti et al. 2014 (AoS/SoA data transformation), and the inverse direction PPCG / OpenMP-to-GPU.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO** — with an explicit caveat that the *execution target* here is a CPU.

verdict_basis: The paper's target is a CPU, but its *subject* is the CUDA/SIMT execution model, and every one of the four optimisations is defined as the reversal of a specific GPU property; none of them has a statement without SIMT. (a) **Anti-coalescing** exists only because GPU kernels are written for warp-level memory coalescing — it is an optimisation whose entire content is "undo the thing the programmer did for the GPU." (b) **Block size invariant analysis** exists because `blockDim` is a launch-time value in the CUDA grid/block launch contract; without `cudaLaunchKernel`-style dimensions there is no runtime-variable trip count to specialise. (c) **Tail block adaptive synchronization** exists because CUDA's grid/block decomposition generates the `idx < n` guard in every block; the transformation's applicability predicate is literally "diverges only at the tail *block*". (d) **GPU-block dynamic tiling** re-maps thread *blocks* to CPU threads and is justified by an explicit SM-vs-core resource comparison. (e) The baseline machinery the paper builds on is barrier splitting at `__syncthreads`, warp-loop insertion, and explicit lowering of warp vote and shuffle primitives — all verified as named passes in the artifact. Replace the GPU programming model with a generic accelerator's and there is nothing left to transform. **Recorded caveat**: this entry contributes no GPU hardware evidence; it should not be cited for any claim about GPU microarchitecture.

verdict: `CORE_GPU`

# GPU-MICRO24-62 — ThreadFuser: A SIMT Analysis Framework for MIMD Programs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — SIMT execution model: warp formation, control-flow divergence and reconvergence, memory divergence` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `N — GPU simulation and performance modelling / cross-architecture prediction; B — intra-warp synchronisation (lock serialisation under SIMT)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` — motivation (developer and architect framings), background (warp formation, divergence, IPDOM/SIMT stack), framework design (PIN tracer, DCFG construction and merge, IPDOM analysis, warp formation, SIMT-stack simulation, coalescing model, lock handling, x86→RISC translation), evaluation setup (Accel-Sim with RTX 3070 config, H100 validation, 36 workloads, PIN 3.15, GCC O0–O3), correlation results, warp-width study, HDSearch case study, microservice findings, limitations, related work. **No artifact/code repository located — `NOT_INSPECTED`.**

## 12.1 Bibliographic facts

- **Title** [paper]: *ThreadFuser: A SIMT Analysis Framework for MIMD Programs*.
- **Venue** [census]: MICRO 2024, Session 7B "GPU Microarchitecture II". `ARCHIVAL_MAIN_PAPER`. The PDF does not print the venue; venue from `domains/gpu_systems/census/MICRO_2024.md` and the publication path `tgrogers/publication/alawneh-micro-2024/`.
- **Authors** [paper]: Ahmad Alawneh, Ni Kang, Mahmoud Khairy, Timothy G. Rogers — Elmore Family School of ECE, Purdue University. (Census agrees.)
- **DOI**: `UNKNOWN`. Census gives `ieeexplore.ieee.org/document/10764650/` (→ 418, not retried).
- **Access** [official-web]: author PDF `engineering.purdue.edu/tgrogers/publication/alawneh-micro-2024/alawneh-micro-2024.pdf`, fetched 2026-09-18.
- **Artifact**: `NOT_FOUND_AFTER_SEARCH` per census; none located here. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Given an arbitrary unmodified MIMD CPU binary (pthreads/OpenMP), how much SIMT efficiency would it have if its threads were fused into warps — computed without porting it to CUDA? [paper]

## 12.3 GPU/HPC problem translation

This is a **methodology** paper whose object is the **SIMT execution model** itself. It serves two constituencies the paper names explicitly [paper]:

- **developers**, who face "significant effort that may or may not result in improved performance versus the CPU" when porting, i.e. a high activation energy with an unknown payoff;
- **architects**, who lack SIMT benchmarks outside graphics/HPC/ML and therefore cannot "examine the impact of SIMT hardware on any CPU binary".

The quantity produced is control-flow divergence and memory divergence under a chosen warp width — the two structural costs of SIMT — plus, via Accel-Sim, a cycle-level speedup projection.

## 12.4 Why the problem exists (hardware root cause)

[paper] SIMT hardware executes a warp's threads in lockstep on a SIMD unit. When threads take different paths at a branch, "current SIMT architectures execute all control paths… sequentially", each with its own active mask, reconverging at the **immediate post-dominator** basic block via the **SIMT stack**. Lanes masked off during a divergent path are lost throughput.

The reason an analysis framework is needed rather than a rule of thumb: divergence is a *dynamic, input-dependent* property of the program's control-flow graph, not a static one. The paper's HDSearch case study is the clean demonstration — the divergence is caused by a data-dependent kd-tree traversal returning different result counts per thread, invisible in the source.

A second, independent source of loss is **memory divergence**: a warp's 32 lanes issue 32 addresses which must be coalesced into cache-line transactions. The paper identifies two structural causes in CPU code [paper]: **private per-thread stacks** (inherently non-contiguous across threads) and **scattered heap allocation** by general-purpose allocators.

## 12.5 Mathematical / performance model

The central metric [paper]:

```
SIMT efficiency = (# instructions executed by all threads)
                  / (# instructions executed in lock-step  ×  WarpSize)
```

i.e. the fraction of SIMD lanes doing useful work. Warp width is configurable at **8, 16 or 32**.

The memory model coalesces the addresses accessed within a warp into **32-byte cache-line transactions** and reports transactions per x86 instruction, separating **stack** from **heap** accesses [paper].

A refinement that matters for fidelity: ThreadFuser builds a **separate DCFG per function**, with a virtual basic block at each function's end, forcing divergent threads to converge at function boundaries. The paper's stated reason is that a whole-program DCFG yields "overly conservative reconvergence points" — real GPUs reconverge at function exit. [paper]

Validation is against real hardware by two statistics [paper]: mean absolute error (MAE) and Pearson correlation.

| Metric | GCC opt level | Correlation vs NVIDIA H100 | MAE |
|---|---|---|---|
| SIMT efficiency | O0 | 1.0 | 7% |
| SIMT efficiency | O1 | 1.0 | 3% |
| SIMT efficiency | O2/O3 | 0.99 | 4% |
| Memory transactions | O0 | 0.99–0.96 range | 30% |
| Memory transactions | O1 | " | 17% |
| Memory transactions | O2/O3 | " | 27–31% |

Error distribution for SIMT efficiency: standard deviation ≈ 6%, average error ≈ 4%, ~83% of samples within one standard deviation [paper].

**Control-flow efficiency is predicted far better than memory behaviour** (3–7% vs 17–31% MAE). That asymmetry is the honest reading of the framework's accuracy.

## 12.6 Data layout and ownership

- **thread (x86) → warp**: the fusion step. The tracer emits per-thread x86 traces; the analyser batches threads into warps of configurable width using a configurable batching algorithm [paper]. This is *the* mapping the framework invents — CPU threads have no warp affiliation.
- **warp → SIMT stack**: each warp carries a simulated SIMT stack; divergence pushes taken/not-taken entries with distinct active masks; reconvergence pops at the IPDOM.
- **warp → memory**: lanes' addresses coalesced into 32 B transactions.
- **block/SM/GPU**: supplied by Accel-Sim when the generated warp traces are fed to it, configured as an **RTX 3070**. ThreadFuser itself does not model the block or SM.
- **Locks** [paper]: the tracer records every lock acquire/release with its address. Threads in a warp contending for the **same** lock are serialised by pushing multiple SIMT-stack entries; threads taking **different** locks proceed in parallel. So a mutex is modelled as a divergence event, which is exactly what it becomes under SIMT.

## 12.7 Pseudo code

Reconstructed; component names (Tracer, Analyzer, DCFG, IPDOM, SIMT efficiency) are the paper's.

```
# --- Tracer: Intel PIN 3.15 ---------------------------------------------- [paper]
instrument before each basic block:
    emit(thread_id, bb_addr, n_instructions)
    for each memory instruction: emit(thread_id, addr, size)
    emit calls, returns, lock_acquire(addr), lock_release(addr)
# overhead: 2-6x native CPU execution time

# --- Analyzer ------------------------------------------------------------- [paper]
per_thread_dcfg = {t: build_dcfg(trace[t]) for t in threads}
dcfg            = merge(per_thread_dcfg)                  # unified graph
dcfg            = split_per_function(dcfg)                # + virtual exit BB
ipdom           = immediate_post_dominators(dcfg)

warps = form_warps(threads, width in {8,16,32}, batching_algorithm)

for w in warps:
    stack = SIMTStack()
    replay w's threads in lock-step:
        on divergent branch:  push(taken, mask_t); push(not_taken, mask_nt)
        on reaching ipdom[b]: pop and reconverge
        on same-lock contention within w: push one stack entry per contender  # serialise
        on memory op: transactions += coalesce(addresses(active lanes), 32 bytes)

report SIMT_efficiency, memory transactions, per-function breakdown

# --- Simulator hand-off --------------------------------------------------- [paper]
x86_CISC -> RISC-like ops     # e.g. "add with memory operand" -> load ; add
emit warp-level trace in Accel-Sim trace format
```

## 12.8 Real implementation

No public artifact located; census records `NOT_FOUND_AFTER_SEARCH`. **No `[code]` evidence — do not attribute symbols.**

Toolchain as stated [paper]:
- **Intel PIN 3.15** for tracing, on an **Intel Xeon E5-2630** (20 cores).
- **GCC** at O0–O3 with SSE vectorisation enabled for compute-intensive applications.
- **Accel-Sim** for cycle-level simulation, configured as an **NVIDIA RTX 3070**. Version/commit `UNKNOWN`.
- **CUDA 12.3 / NVCC -O3** for the GPU baselines used in correlation.
- **NVIDIA Nsight Compute** for hardware metrics; the paper mentions profiling on a **Volta** GPU for hardware metrics and **H100 (Hopper)** for the accuracy correlation. These are two different real parts used for two different purposes — do not merge them.

## 12.9 Kernel execution

There is no kernel. That is the paper's point: it manufactures a kernel-equivalent from a CPU binary. The manufactured hierarchy is thread → warp (width 8/16/32) → Accel-Sim's block/SM model.

**Warp-width finding** [paper]: as warp size grows 8 → 16 → 32, SIMT efficiency generally declines, and the magnitude of the decline sorts the workloads.

- High-efficiency workloads (N-body, MD5): **under 5% variation** across warp sizes.
- Low-efficiency workloads (Pigz, BFS): **up to 18% variation** — e.g. Pigz at 18% efficiency with 8-thread warps vs 10% with 32-thread warps.

The implication the paper draws is a hardware one: irregular workloads would benefit from narrower warps. **This is the paper's most architecturally actionable result** and is the reason it belongs in a core-execution cluster rather than a tooling one.

## 12.10 Memory traffic

Modelled at one level only: lane addresses → 32 B transactions, split stack vs heap [paper]. The findings:

- Workloads show substantial memory divergence from **private per-thread stacks** and **scattered heap allocation**.
- Remedies the paper suggests (not evaluated): AoS→SoA restructuring, GPU-aware allocators, compiler support.
- Prediction accuracy here is the framework's weak axis (17% MAE at O1, 27–31% at O2/O3), attributed to GCC's register allocation differing from what a SIMT target needs.

Below the coalescing step, the cache/HBM path comes from Accel-Sim's RTX 3070 configuration, not from ThreadFuser.

## 12.11 Why it is faster/slower (decomposed cause)

The framework produces *projections*, so "faster" means projected GPU speedup versus the CPU baseline [paper, Accel-Sim, RTX 3070 configuration]:

- Range across 36 workloads: **under 5× to 15–20×**.
- High-SIMT-efficiency applications (N-body, MD5) project consistent speedups, including on previously unseen applications.
- Low-efficiency applications (Pigz, BFS-Rodinia) project modest speedups — correctly flagging them as bad porting targets.
- **Microservices average 78% control-flow efficiency** [paper], which the paper reads as evidence of untapped SIMT potential in a domain never before considered a GPU target.

The **HDSearch-midtier case study** is the causal demonstration [paper]: initial SIMT efficiency **7%**; per-function analysis localises it to `getPointID`, at 6% efficiency, diverging because of data-dependent kd-tree traversal; fixing the result count to 10 for all threads raises efficiency to **90%** while retaining **93% search accuracy**. The framework's value is here — not the number, but the *attribution to a named function and a named cause*.

**Where the analysis degrades**: at O2/O3 the analyser *overestimates* efficiency, because GCC's loop unrolling and jump tables make the x86 trace look more uniform than the corresponding SIMT execution would be [paper]. So the tool is optimistic exactly where compilers are most aggressive.

**Lock serialisation** [paper]: with intra-warp locking simulated, microservice efficiency falls but stays relatively high, because fine-grained locking over independent requests rarely puts two contenders in one warp. Skipped instructions (lock spinning, I/O) are about **10%**.

## 12.12 Hardware generation dependence

- **Validation target**: NVIDIA **H100 (Hopper)** for the SIMT-efficiency and memory-divergence correlation — **real hardware measurement**.
- **Simulation target**: **RTX 3070 (Ampere)** configuration in Accel-Sim — **simulated**. Speedup projections are simulated, correlations are against measured H100.
- **Hardware metrics** additionally profiled on a **Volta** GPU with Nsight Compute.
- Three different NVIDIA generations appear in three different roles. Do not restate any single number without saying which part it came from.
- The framework is generation-agnostic by construction: it models warp width, IPDOM reconvergence and 32 B coalescing, all of which have been stable across NVIDIA generations. It models **no** Hopper-specific feature — no TMA, no wgmma, no distributed shared memory, no thread-block clusters — despite validating against an H100. Tensor cores and shared memory are explicitly *out* of scope (see limitations).
- AMD wavefronts (width 64) are not evaluated, though the paper's configurable warp width would accommodate them in principle. `[inference]`

## 12.13 Limitations

Stated [paper]:
- **No GPU-specific optimisation is assumed.** ThreadFuser predicts the as-is port; it "does not directly project the potential performance possible if the programmer is willing to invest the effort" in shared memory or tensor cores. Projections are therefore lower bounds on a well-optimised port, and not comparable to hand-tuned CUDA.
- **ISA/compiler mismatch.** The input is x86-optimised code, and "some of the assumptions made by the compiler could be sub-optimal for a SIMT design" — notably register allocation unaware of the GPU's large multi-threaded register file, producing unnecessary spills/fills. (The paper reframes this as an opportunity for hardware/software co-design study.)
- **Optimisation-level sensitivity**: memory-divergence MAE 17% at O1 vs 27–31% at O3, so estimates are not portable across compiler configurations.
- **Reconvergence choice for serialised lock holders** is one of the unlock pairs; other choices would give different control-flow efficiency, and the exploration is deferred.
- **Not useful for regular code**: for optimised GEMM-like kernels, roofline analysis is more appropriate because "optimized library kernels already exist".
- **33% execution-time overhead** for the simulator-based detailed analysis (tracing itself is 2–6× native).

`[inference]`, not stated: the framework fuses threads that in the CPU program were independent OS threads with their own stacks and no expectation of lockstep; fusing them assumes the *number of software threads* is the right parallelism to map to lanes. For workloads whose thread count is tuned to core count rather than to data parallelism, this may misstate the achievable warp occupancy. The paper's thread counts do range from 128 (Pigz, MD5) to 42K (Nearest Neighbors), which partly addresses this, but no sensitivity study is given.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep finds "ThreadFuser" only in `domains/gpu_systems/census/MICRO_2024.md`.
- **Sibling paper, same group, same venue**: `GPU-MICRO24-61` (CARS / Concurrency-Aware Register Stacks) shares authors Alawneh, Kang and Rogers. ThreadFuser's ISA-mismatch limitation ("register allocation unaware of SIMT's large multi-threaded register file, potentially causing unnecessary spills/fills") is the same pathology CARS attacks in hardware. Reading them together: the Purdue group published, in one MICRO, both a diagnosis tool that surfaces register spill/fill as a SIMT cost and a microarchitectural fix for it.
- **Complementary, opposite direction**: `GPU-MICRO24-64` (CuPBoP, Unleashing CPU Potential for Executing GPU Programs) runs CUDA on CPUs; ThreadFuser evaluates CPU programs under SIMT. The two bracket the same MIMD↔SIMT translation question from either side, in the same conference.
- **Complementary**: `GPU-MICRO25-61` supplies the modern core model that a SIMT-projection framework would need for cycle accuracy; ThreadFuser uses stock Accel-Sim, whose core model MICRO'25 measures at 34.03% MAPE against real Ampere hardware. `[inference]` — this bounds ThreadFuser's cycle-level projections independently of ThreadFuser's own error analysis; the paper does not discuss it.
- **Precursors cited** [paper]: **XAPP** (the closest prior work — ML-based single-threaded CPU→GPU speedup prediction from 16 profile properties, 26.9% execution-time error vs ThreadFuser's 33% average, but limited to existing GPU architectures and single-threaded input); GPUMech (Zhou et al., interval analysis); Hong & Kim's integrated power/performance model; Wu et al. 2015; Zhang et al. 2011; profiling tools GPA, CUDAAdvisor, CUDA Flux; server-SIMT studies by Agrawal et al., Hetherington et al.; **SIMT-X** (Tino et al., out-of-order pipelines integrated with SIMT for OpenMP); **GPU First** (Tian et al. 2023, compiler-based CPU-code-on-GPU limited to OpenMP).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The framework computes a quantity that only exists on SIMT hardware. Every modelled mechanism is GPU-specific: **warp formation** at configurable width (the batching of independent MIMD threads into lockstep groups has no meaning on a CPU or on a generic dataflow accelerator), **IPDOM reconvergence via a simulated SIMT stack** with per-path active masks, **32-byte intra-warp coalescing** across lanes, and **lock contention modelled as divergence** — a mutex becomes a stack push precisely because lanes cannot independently spin. The headline metric, SIMT efficiency = useful-lane-work / (lockstep instructions × WarpSize), is undefined without a warp. The architecturally actionable output — that irregular workloads lose up to 18 percentage points of efficiency going from 8-wide to 32-wide warps — is a statement about SIMD lane-array width under divergence. A CPU-side framework producing the same traces would answer a different question entirely (it would answer "is this parallel?", not "does this diverge?").

verdict: `CORE_GPU`

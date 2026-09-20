# GPU-MICRO24-41 — Over-Synchronization in GPU Programs (ScopeAdvice)

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `N — profiling, debugging, correctness checking, simulation & performance modelling`
secondary_topics: `GPU memory consistency model (PTX scopes); NVBit/SASS dynamic instrumentation; L1/L2 coherence; performance tooling`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — author-hosted PDF (csa.iisc.ac.in/~arkapravab/papers/MICRO24_ScopeAdvice.pdf) read for authors/venue, the scope/cost motivation, the three over-synchronization variants, the trace model and windowing scheme, the NVBit instrumentation and per-location metadata layout, Rules 1-3 and the detection algorithm, the PTX-memory-model validity argument, the full evaluation (hardware, benchmark table with instance counts, speedup and stall-cycle table, the four-stage overhead breakdown, memory overhead), limitations, and related work. NOT read line-by-line: individual figure captions and the complete reference list. NOTE: this paper was assigned as VERDICT-ONLY; it is deep-analysed here because full text was obtained and spare capacity existed, per the task's standing permission.`

## 12.1 Bibliographic facts

- Official title: *Over-Synchronization in GPU Programs* [paper]. Tool name: **ScopeAdvice** [paper] (the author PDF filename is `MICRO24_ScopeAdvice.pdf`).
- Authors: **Ajay Nayak**, **Arkaprava Basu** — Indian Institute of Science, Bengaluru, India [paper]. Two authors.
- Venue: MICRO 2024, Session **5C "Debugging Correctness/Performance"** [census]. IEEE Xplore document 10764471 (`census/MICRO_2024.md`).
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: author-hosted PDF `https://www.csa.iisc.ac.in/~arkapravab/papers/MICRO24_ScopeAdvice.pdf` [official-web].
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Every GPU correctness tool looks for *too little* synchronization (data races); this paper asks the dual question — how often do expert CUDA programmers use a *wider memory scope than necessary*, what does that cost on real hardware, and can a dynamic tool find those instances soundly enough to act on? [paper]

## 12.3 GPU/HPC problem translation

- **Synchronization.** The paper's entire subject: the choice of scope on fences and atomics.
- **Memory.** The *cost* of that choice is a cache-hierarchy cost — a device-scoped fence forces an L1 flush on the writer and an L1 invalidate on the reader, because the GPU's L1 is incoherent by design.
- **Compute.** The benefit is measured as recovered SM issue cycles: the paper reports fence *stall cycles* before and after.
- **Communication / scheduling.** NOT_IN_PAPER beyond the system-scope (CPU–GPU) case, which is acknowledged as incompletely covered.

## 12.4 Why the problem exists (down to hardware root cause)

This paper has the cleanest hardware root cause in the cluster, and it is a cache-coherence one [paper]:

- **The GPU L1 is private per SM and *incoherent by design*; the L2 is shared and coherent.** That single architectural fact generates the whole scope hierarchy.
- Therefore the cost of a fence is a function of its scope:

| Scope | CUDA construct | Visibility | What the hardware must do |
|---|---|---|---|
| block / CTA | `__threadfence_block()` | within a threadblock | nothing to L1 — the block's threads share one (incoherent) L1, so it is already consistent among them |
| device / GPU | `__threadfence()` (the default) | all blocks in the grid | **flush L1 to L2** on the writer; **invalidate L1** on the reader |
| system | `__threadfence_system()` | across GPUs and CPUs | widest, most expensive |

- **Measured cost of that difference: on an NVIDIA RTX 3090, the block-scope fence is 21× faster than the device-scope fence** [paper]. This is the number the whole paper rests on — scope is not a documentation nicety, it is a 21× primitive-cost difference.
- **Why programmers over-scope anyway** [paper]: (i) under-scoping is a *data race* — a correctness bug — while over-scoping is merely slow, so the safe default is asymmetric; and (ii) the GPU memory model has "subtle semantics of related memory operations" that interact with compiler optimizations, so the optimal scope is genuinely hard to determine. Note `__threadfence()` — the *device* scope — is the unqualified default spelling, so the safe choice is also the syntactically shortest one.
- **Evidence that experts get this wrong:** over-synchronizations were found "in popular CUDA libraries written by experts (e.g., cuML)" [paper].

## 12.5 Mathematical / performance model

Not a performance model but a **formal soundness argument against the PTX memory model**, which is what distinguishes this from a heuristic optimizer [paper].

CUDA has no formal memory model, but all CUDA lowers to **PTX**, which does. The argument uses PTX's own vocabulary [paper]:
- **morally strong** — memory operations from different threads on the same address whose scope includes both threads;
- **data race (PTX §8.6.1)** — conflicting operations (at least one a write) that are neither morally strong nor ordered; always disallowed;
- **program order**, **observation order** (a read returns a value written by another thread), **synchronization order** (scope-induced ordering).

Worked validity argument for Variant 1 [paper]: in the optimized code all memory operations are volatile (hence system-scoped, hence morally strong), so no data race is possible; fences F1 and F2 preserve program order; and the observation order `W1 → F1 → W2 → R1 → F2 → R2` guarantees the consumer reads the latest produced value **even though F2 has been narrowed to block scope**.

The structure of the claim is important: the *visibility* guarantee is supplied by the cache-bypassing access itself (volatile / device-scoped atomic), so the fence only has to supply *ordering* — and ordering is cheap at block scope. Separating visibility from ordering is the paper's real insight.

The three detection rules [paper], quoted:

> **Rule 1** — "Given two operations, `rdSkipL1(t1, x)` and `wrV(t2, x)`, such that t1 belongs to threadblock b1, t2 belongs to threadblock b2, and b1 != b2, then: (1) the fence identified by `getPrevSync(t1, rdSkipL1)` should be block-scoped, (2) the fence identified by `getNextSync(t2, wrV)` should be device-scoped unless the `wrV` is due to a device-scoped `atm`."

> **Rule 2** — "Given two operations `rd(t1, x)` and `wr(t2, x)`, such that t1 belongs to threadblock b1, t2 belongs to threadblock b2, and b1 == b2, then: (1) the fence identified by `getPrevSync(t1, rd)` should be block-scoped, (2) the fence identified by `getNextSync(t2, wr)` should be block-scoped."

> **Rule 3** — "If a block, device or a system-scoped fence that was found over-synchronized following Rule 1 or 2 is an immediate neighbor to a barrier in the source code, then the fence is redundant."

Rule 3 exploits a specific CUDA semantic: **`__syncthreads()` already carries block-scoped fence semantics**, so a block-scoped fence adjacent to a barrier is pure overhead [paper].

## 12.6 Data layout and ownership

**Trace model** — the alphabet of observed events [paper]:

| Event | Meaning |
|---|---|
| `rd(t, x)` | thread t reads address x |
| `rdSkipL1(t, x)` | thread t reads x **bypassing L1** (volatile, or device-scoped atomic) |
| `wr(t, x)` | thread t writes x |
| `wrV(t, x)` | thread t writes to a volatile address |
| `atm(t, x, scope)` | thread t performs a scoped atomic RMW on x |
| `fence(t)` | thread t executes a device-scoped fence |

**Windowing.** Code is divided into windows with fences as sentinels; every memory operation is tagged with its window's `FenceId`. Two helpers relate operations to fences: `getPrevSync(t, read)` returns the fence preceding a thread's read, `getNextSync(t, write)` the fence following a thread's write [paper].

**Per-location metadata, per 4-byte location** (the paper's Figure 8) [paper]:

| Field | Purpose |
|---|---|
| `Valid` | location was accessed |
| `Store` | location was written |
| `MultiBlock` | **accessed by threads from different threadblocks** |
| `BlockId` | threadblock of the last accessing thread |
| `Count` | dynamic instance counter, used by the trace-filtering optimization |

The `MultiBlock` bit is the decision variable, and `BlockId` is how it is computed: compare the current accessor's block against the stored one, and set `MultiBlock` on a mismatch `[reconstruction]`. This is a markedly cheaper abstraction than a race detector's — it does not need to know *which* blocks shared, only *whether* more than one did.

**Fence tracking.** Rather than track every dynamic fence instance, a **2-D bit vector indexed `FenceId × ThreadId`** records which threads executed which fences; the size, `#unique_fences × #threads` bits, is known before kernel launch [paper]. Static fence count is small, so this is cheap.

Ownership mapping:

| Level | Represented as |
|---|---|
| thread | `ThreadId` in the trace and the fence bit vector |
| warp | not represented (warp-level scope is not one of CUDA's fence scopes) |
| threadblock / CTA | `BlockId` + the `MultiBlock` bit — **the decision unit** |
| grid / device | the default fence scope being questioned |
| system (CPU+GPU) | recognised but acknowledged as incompletely covered |
| 4-byte memory location | the metadata unit |

## 12.7 Pseudo code

The detection algorithm, as printed in the paper's Figure 10 [paper]:

```
detect(memTrace, memMetadata, fences) -> list[fenceId]:
    osd = fences                       // assume ALL fences over-synchronized
    for each address in globalAddressesAllocated:
        if (address.Store AND address.MultiBlock):
            for each instruction I accessing address:
                if (I.Load AND NOT isVolatileLd(I)):
                    // a normal (L1-caching) cross-block load genuinely needs
                    // the wider scope -> exonerate that fence
                    osd.remove(getPrevSync(I.ThreadId, I.WindowId))
                if (I.Store AND NOT isDevAtomic(I)):
                    osd.remove(getNextSync(I.ThreadId, I.WindowId))
    return osd
```

The algorithm is **assume-guilty-then-exonerate**: every fence starts on the over-synchronized list and is removed only when evidence of genuine need appears. That polarity is what makes it unsound in the classical sense on a single input (an unexercised path never produces exonerating evidence) — and it is exactly why the authors require agreement across multiple inputs (12.13).

The three-branch decision, restated [paper]:
- `MultiBlock` **unset** → sharing is intra-block only → block scope suffices (Rule 2).
- `MultiBlock` **set** AND reads skip L1 (volatile or device-scoped atomic) → visibility already guaranteed by the access itself → block-scoped fence suffices for ordering (Rule 1).
- otherwise → device scope is genuinely necessary.

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact repository identified. The instrumentation mechanism is described in enough detail to record precisely [paper]:

- **NVIDIA NVBit** instruments CUDA kernels at the **SASS** (GPU assembly) level. *Note the contrast with `GPU-SC24-41` (HiRace), which deliberately avoided NVBit in favour of Clang source rewriting, citing NVBit's deprecation and per-architecture fragility. The two papers, at adjacent 2024 venues, make opposite instrumentation bets.*
- **Static phase:** the code is scanned; each static fence receives a `FenceId` (from 0, incremented per fence); all memory instructions are tagged with the current `FenceId` (i.e. their window).
- **Dynamic phase:** instrumented loads, stores and atomics emit trace units carrying thread ID, operation type, address, and window ID.
- **Address-space filtering** uses **`isspacep.global`** to exclude non-global accesses (scratchpad/shared memory, registers) [paper] — a real PTX predicate instruction, and the mechanism by which the tool restricts itself to the memory that fence scope governs.
- **Volatility and atomic scope are recovered from distinguishable compiler opcodes** — the paper names **`LDG.SYS`** for volatile loads [paper]. This is the crucial trick: the tool does not need source-level type information, because `nvcc` encodes volatility and scope into the SASS opcode/modifier, so a SASS-level tool can read the programmer's scope intent directly off the instruction stream.
- Runtime parameters used in evaluation: 768 buffers, 12 CPU analysis threads, sampling bound = 15, `inGPUTraces = 2` [paper].
- Metadata is held in **Unified Virtual Memory (UVM)** to avoid exhausting GPU memory [paper].

## 12.9 Kernel execution

- **kernel → thread block → thread** is the axis that matters; the warp level is *absent by construction* because CUDA's fence scopes are block/device/system, with no warp-scoped fence.
- The consequence of over-synchronization at instruction level is SM issue stalls, and the paper measures this directly with **fence stall cycles** before and after the fix (see 12.11). That is the right metric: it attributes the recovered time to the fence rather than to the change in aggregate runtime.
- Concurrency scale is visible in the memory-overhead discussion: cuML ran with **492 concurrent threadblocks** [paper], which is what makes the fence bit vector and sampling metadata large.

## 12.10 Memory traffic

The traffic effect is the L1 flush/invalidate pair that a device-scoped fence compels, and it is avoided entirely at block scope [paper]. The paper does not report bytes; it reports the consequence in stall cycles and in primitive cost (21× on RTX 3090).

**Over-synchronization instances found** (RTX 3090, CUDA 11.2) [paper]:

| Application | Source | Variant | Count |
|---|---|---|---|
| cuML (CU) | cuML library | Variant 1 (volatile) | 3 |
| String sort (ST) | cudpp | Variant 2 | 10 |
| Compress (CP) | cudpp | Variant 2 | 2 |
| Matrix multiply (MM) | ScoR | Variant 1 (V) + Variant 3 | 3 (**synthetic**) |
| Sgemm (GE) | cuBLAS | Variant 2 | 1 (**unvalidated — closed source**) |
| Unbalanced tree (UT) | ScoR | Variant 1 (volatile) | 2 |
| Unbalanced tree atomic (UT-A) | modified ScoR | Variant 1 (device atomic) | 2 (**synthetic**) |
| Stencil (SC) | reference [42] | Variant 3 | 2 (**synthetic**) |
| Reduction, Hash table, Parallel linear recurrence, Parallel merge | various | none | **0 (negative controls)** |

Two things to keep with these counts. First, **four of the eight positive cases are synthetic or unvalidated**; the genuinely-found-in-the-wild instances are cuML (3), String sort (10), Compress (2) and Unbalanced tree (2). Second, the **four negative controls returning zero** are as important as the positives — they are the evidence for the no-false-positives claim.

The three variants [paper]:
- **Variant 1 — wide scope with cache-bypassing loads.** A `volatile` access or a device-scoped atomic RMW already guarantees visibility; the wide fence scope adds only redundant visibility, so block scope suffices for ordering.
- **Variant 2 — redundant fences adjacent to barriers.** `__syncthreads()` already implies a block-scoped fence.
- **Variant 3 — intra-block lock/unlock routines** implemented with device-scoped operations when the communicating threads are all in one block.

## 12.11 Why it is faster/slower (decomposed cause)

**Speedups after removing over-synchronizations, with the stall-cycle attribution** (RTX 3090, CUDA 11.2) [paper]:

| Application | Speedup | Fence stall cycles, original | Fence stall cycles, modified |
|---|---|---|---|
| Matrix multiply (synthetic) | **54%** | 4.4 | 0.13 |
| Stencil (synthetic) | 50% | 2.8 | 0 |
| **cuML** (real library) | **37%** | 24.8 | 14.5 |
| **String sort** (real library) | **29%** | 6.7 | 0 |
| Unbalanced tree | 17% | 2.3 | 0.8 |
| Unbalanced tree atomic (synthetic) | 11% | 2.2 | 0.7 |
| Compress | **0%** | 0 | 0 |

The causal chain is fully decomposed and is the paper's strongest evidential move: **speedup tracks the reduction in fence stall cycles, and where there were no fence stalls there is no speedup.** Compress had 10 detected instances but 0 stall cycles and therefore 0% gain — the tool found real over-synchronization that did not matter. That is an honest negative result and it sharpens the claim: over-synchronization is a performance bug only when the fence is on a hot path.

The largest real-code win, cuML at 37%, is also the one where stall cycles are *not* driven to zero (24.8 → 14.5) — the remaining fences are genuinely necessary.

*Caution on aggregate figures:* the paper's own summary framing quotes a range up to 55% and an average around 20–30%, while the per-application table above tops out at 54% (matrix multiply, synthetic). Use the table. The honest headline is: **29–37% on real library code, 0% where fences were not hot.**

**Cost side — the overhead reduction is a four-stage story** [paper], normalized to uninstrumented execution:

| Configuration | Overhead range |
|---|---|
| Naive (no optimizations) | 10,349× (UT) – 12,611× (RD) |
| + Para (12 CPU threads, 768 buffers) | 570× (UT) – 2,345× (RD) |
| + Sampling (1/15 random after first instance) | 162× (MM) – 1,445× (RD) |
| **ScopeAdvice (sampling + trace filtering)** | **29× (Compress) – 522× (PL)**, median ~150–160× |

Overhead attribution [paper]: **NVBit itself contributes ~64% of the total** — "orthogonal; improvements in NVBit could help" — CPU-side trace analysis up to 25% (worst in String sort), with GPU↔CPU communication reduced by the parallelism and sampling stages. Memory overhead is typically 2–4× of the application footprint (metadata 1× per 4 bytes; fence trace up to 2.48× on cuML; trace filtering 2×), held in UVM [paper].

That NVBit accounts for ~64% of a 29–522× slowdown is a direct quantitative vindication of HiRace's opposite design choice — and neither paper cites the other.

## 12.12 Hardware generation dependence

- Hardware: a single **NVIDIA RTX 3090** (Ampere, consumer), 16-core host, 128 GB DRAM, **CUDA 11.2**, driver **v470** [paper]. Like HiRace, this is a consumer part — no A100/H100/MI250X result.
- The 21× block-vs-device fence cost ratio is an RTX 3090 measurement and must not be reused for datacenter parts without requalification. It is the load-bearing number in the motivation.
- **Dependence on SASS opcode encoding.** The tool recovers volatility and atomic scope from opcodes such as `LDG.SYS` [paper]. Opcode spellings and modifier encodings change between SASS generations, so this decoding is per-architecture maintenance — the same liability as `GPU-SC26-41` (LEO) carries for its barrier-bit decoding, and the same one `GPU-SC24-41` (HiRace) avoided.
- **Generation-independent core:** the block/device/system scope hierarchy and the incoherent-L1/coherent-L2 split are stable features of the CUDA programming model and the PTX memory model, so the *rules* should survive generations even as the instrumentation needs updating `[inference]`.
- Not evaluated on AMD. HIP has an analogous scope hierarchy `[inference]`; the paper makes no portability claim.

## 12.13 Limitations

Stated by the authors [paper]:
1. **Input-dependent false positives.** A fence reported as over-synchronized for one input may be necessary for another — especially with small inputs exercising few threadblocks (which falsely suggests intra-block sharing) or data-dependent control flow. Mitigation: run with multiple test inputs and report only if **all** inputs agree; with **CLFuzz** fuzzing integration, coverage improves. This is inherent to the assume-guilty algorithm polarity (12.7).
2. **Static analysis is inadequate**, which is why the tool is dynamic: "index analysis techniques for determining memory accesses fall short for kernels with complex access patterns (e.g., input-dependent indexing)."
3. **29–522× overhead** makes it an offline development-time tool, not a production profiler.
4. **Variant coverage may be incomplete** — Variant 1 with device-scoped atomics (UT-A) was **synthetic**, not found in studied real code.
5. **Formal validation is scoped to the three identified variants** and does not comprehensively cover CPU–GPU (system-scope) synchronization, multi-GPU scenarios, or compiler optimizations beyond documented volatility semantics.

Observed by this analysis:
6. **Single consumer GPU** (RTX 3090), CUDA 11.2, driver v470 — an aging toolchain even at publication, and no datacenter-GPU validation.
7. **Four of eight positive cases are synthetic or unvalidated**; the cuBLAS Sgemm instance could not be validated because the source is closed.
8. **No artifact**, so neither the rules nor the overhead figures are reproducible.
9. The paper's summary framing (up to 55%, average 20–30%) is not reconcilable with its own per-application table (max 54%, and that case synthetic); prefer the table.
10. No warp-scope treatment — correct given CUDA's fence scopes, but it means cooperative-groups and async-barrier patterns on Ampere/Hopper are outside the analysis `[inference]`.

## 12.14 Relation to prior corpus

- **Prior corpus:** `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Over-Synchronization" returns only `domains/gpu_systems/census/MICRO_2024.md` (a census row).
- **The dual of `GPU-SC24-41` (HiRace), and a verified non-citation.** ScopeAdvice's related work names **iGUARD** (with overhead **27–649×**), **BARRACUDA** (~**3700×**), **SCORD**, and **compute-sanitizer racecheck** as the race-detection art, and states the goals are orthogonal: those tools find *under*-synchronization, ScopeAdvice finds *over*-synchronization [paper]. **HiRace is not among them** — the two papers appeared at MICRO 2024 and SC 2024 respectively, address exactly complementary halves of one problem (too little versus too much synchronization over the same CUDA scope lattice), instrument the same programs, and cite the same baselines (iGUARD, compute-sanitizer), yet neither cites the other. This is a real, checkable gap in the 2024 literature and the clearest citation-level finding in this cluster.
- **Quantitative cross-check between the two:** ScopeAdvice cites iGUARD at 27–649× overhead; HiRace measures iGUARD at "more than 30× slowdown" on average with outliers to ~1000× [paper, HiRace]. The two independent characterisations are consistent, which strengthens both.
- **Memory-model foundation, named by the paper:** **Lustig et al.** on the formal PTX memory model is cited as the basis of the soundness argument; **Sinclair et al.** and **Alsop et al.** for GPU consistency-model proposals [paper]. This links directly to *Towards Unified Analysis of GPU Consistency* (ASPLOS 2024/29V4, in this cluster's verdict-only list), which axiomatically unifies PTX/Vulkan/scoped GPU models — i.e. the formal work that a tool like ScopeAdvice consumes.
- **Profiling tools it positions against, all in or adjacent to this cluster** [paper]: **Nsight** ("minimal actionable advice"), **ValueExpert**, **GVProf**, **DRGPUM**, **GPA**, **CudaAdvisor**, **Cuda Flux**. **GPA is also LEO's named precursor** (`GPU-SC26-41` §12.14) — so GPA is cited independently by both the MICRO 2024 scope tool and the 2026 cross-vendor stall slicer, making it a genuine hub of the GPU performance-advisory literature.
- **Also cited:** **Synccheck** (incorrect barrier usage) and **remote-scope promotion** (a hardware proposal for dynamic scope adjustment, versus ScopeAdvice's software approach) [paper].
- **Complementary within this cluster:** *RedSan* (SC 2025) and *Triton-Sanitizer* (ASPLOS 2026) are the sanitizer neighbours; `GPU-SC26-41` (LEO) attributes stalls without asking whether the synchronization causing them was necessary — a natural composition neither paper makes. See `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The contribution is defined entirely by CUDA's scoped memory model and by the GPU's incoherent-L1/coherent-L2 cache organisation. The three scopes analysed — `__threadfence_block()`, `__threadfence()`, `__threadfence_system()` — exist because a threadblock's threads share one private incoherent L1 while cross-block visibility requires an L1 flush and invalidate, and the measured 21× cost gap between block and device scope on an RTX 3090 is that cache behaviour. The decision variable is the `MultiBlock` bit over CUDA *threadblocks*; the soundness argument is discharged against the **PTX** memory model's morally-strong/observation-order relations; the instrumentation reads GPU SASS opcodes (`LDG.SYS`) and the PTX `isspacep.global` predicate; and Rule 3 depends on `__syncthreads()` carrying implicit block-scoped fence semantics. A CPU has coherent caches and no programmer-selected fence scope hierarchy of this kind, so neither the bug class nor the 21× incentive to fix it exists there.

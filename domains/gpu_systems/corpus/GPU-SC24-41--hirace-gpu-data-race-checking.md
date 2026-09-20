# GPU-SC24-41 — HiRace: Accurate and Fast Data Race Checking for GPU Programs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `N — profiling, debugging, correctness checking, simulation & performance modelling`
secondary_topics: `GPU memory consistency / scoped synchronization; dynamic binary & source instrumentation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_VIA_TWO_TARGETED_PASSES — author PDF (userweb.cs.txstate.edu/~mb92/papers/sc24.pdf) read for (a) authors/motivation/prior-tool critique/shadow-state design/FSM/instrumentation and (b) evaluation hardware, benchmark suites, accuracy tables, slowdown, memory overhead, limitations, related work, artifact URL. Artifact repository cloned and read at commit 44a935f90acfe43c6178b2187ea84c9ab0c01450. NOT read line-by-line: the Murphi formal-verification appendix, and the full 1200-row transition table (read as source arrays, not as prose).`

## 12.1 Bibliographic facts

- Official title: *HiRace: Accurate and Fast Data Race Checking for GPU Programs* [paper]. The census records a seed-list title with a hyphen ("Data-Race"); the official title has no hyphen (`domains/gpu_systems/census/SC_2024.md` §5).
- Authors: John Jacobson (Kahlert School of Computing, University of Utah), Martin Burtscher (Department of Computer Science, Texas State University), Ganesh Gopalakrishnan (Kahlert School of Computing, University of Utah) [paper].
- Venue: SC 2024. DOI `10.1109/SC41406.2024.00042` [census, corroborated by SC24 program page `pap649`].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: author PDF `https://userweb.cs.txstate.edu/~mb92/papers/sc24.pdf`; NSF PAR mirror `https://par.nsf.gov/servlets/purl/10583102` [official-web].
- Artifact: `https://github.com/JohnJacobsonIII/HiRace-Artifact-SC24`, stated in the paper [paper], cloned at commit `44a935f90acfe43c6178b2187ea84c9ab0c01450` [code].

## 12.2 Core question (one sentence)

Can a GPU data-race detector be simultaneously *complete* over global and shared memory and cheap enough to run routinely, by replacing per-access vector-clock/access-record history with a fixed-width finite-state abstraction over the GPU thread hierarchy? [paper]

## 12.3 GPU/HPC problem translation

- **Synchronization.** This is primarily a synchronization-semantics problem. The contribution is an abstraction of *happens-before within the bulk-synchronous GPU hierarchy*: rather than tracking which threads accessed an address, HiRace tracks the smallest thread-group scope that is guaranteed to have synchronized. [paper]
- **Memory.** Secondarily a memory-capacity problem: prior dynamic detectors could not afford shadow metadata over full device memory, so NVIDIA's `compute-sanitizer racecheck` restricts itself to block-shared memory [paper].
- **Compute.** The per-access instrumentation cost lands on the SM issue path (a table lookup plus an atomic CAS retry loop per monitored access), which is what the slowdown figures measure [paper] [code].

## 12.4 Why the problem exists (hardware root cause)

- GPU races are latent under low optimization and manifest under higher optimization: the paper states race-afflicted programs "may appear to work normally under low compiler optimization levels but misbehave when optimized," producing "out of thin air" values [paper].
- The hardware root cause of the *tooling* difficulty is capacity, not semantics: CPU-derived FastTrack-style detection needs per-address access records, and at full HBM/device-memory scale this does not fit. IGUARD's record size forces it to "track only a single prior accessor," so records are evicted and multi-reader patterns (paper's Listing 5) are missed [paper].
- NVIDIA's `compute-sanitizer racecheck` "does not check for data races occurring within the GPU global memory space, presumably due to an inability to scale to full device memory" [paper] — i.e. the vendor tool's scope restriction is itself a consequence of device-memory size.
- A second root cause is the synchronization hierarchy itself: GPU barriers are *scoped* (`__syncwarp` ⊂ `__syncthreads` ⊂ implicit kernel-boundary device sync), so "synchronized" is not a single relation but a lattice over warp/block/grid. Any detector that flattens this either loses precision or must carry per-thread clocks. [paper]

## 12.5 Mathematical / performance model

HiRace is not a closed-form performance model; its formal object is a finite-state machine. The state space is enumerated in the source as:

```
TRANSITION_COUNT = 1200 = 25 states x 4 memory actions x 3 sync levels x 4 thread relations
```
[code: `src/hirace/HiRace.h` line 39 and its comment]

- 25 states [code: `INIT`=0 … `RACE`=24].
- 4 memory actions: `R`, `W`, `BA` (block-scoped atomic), `GA` (grid/global-scoped atomic) [code].
- 3 sync levels: `UNSYNC`, `WARPSYNC`, `BLOCKSYNC` [code].
- 4 thread relations: `SAMETHREAD`, `SAMEWARP`, `SAMEBLOCK`, `SAMEGRID` [code].

The paper's own state count and transition count (25 states, 1200 transitions) agree with the source exactly [paper] [code]. The paper additionally decomposes the 25 states as 4 read-tracking, 7 write-tracking, 12 atomic-tracking, plus initial and race states [paper].

Transition lookup is a single index into a flat array formed by concatenating the state with the transition label [paper], i.e. `next = TABLE[state*48 + action*12 + sync*4 + rel]` `[reconstruction]` — the source stores the table as a flat array whose comment ordering is `STATE|ACTION|SYNC|REL` [code], so the stride constants are inferred from that ordering and are `[reconstruction]`, not quoted.

The correctness argument is model checking, not analysis: the paper reports formal verification of the FSM via the **Murphi** model checker [paper].

## 12.6 Data layout and ownership

The shadow word is exactly 64 bits and its field widths sum to 64 [code: `src/hirace/HiRace.h` lines 85–107]:

| Field | Macro | Bits | Meaning |
|---|---|---|---|
| Thread id within block | `TID_BITS` | 10 | identifies prior accessor thread (up to 1024 threads/block) |
| Block id | `BLOCK_BITS` | 15 | identifies prior accessor block |
| FSM state | `STATE_BITS` | 5 | one of the 25 ISM states |
| Block-barrier clock | `BCOUNT_BITS` | 16 | `__syncthreads` count witnessed |
| Warp-barrier clock | `WCOUNT_BITS` | 10 | `__syncwarp` count witnessed |
| Shadow/wrapper index | `SWIDX_BITS` | 8 | which monitored data structure |
| **total** | `SHADOW_SIZE` | **64** | 8 bytes per monitored address |

Ownership maps onto the hierarchy as follows [paper] [code]:
- **thread** — `TID`+`BLOCK` name the single prior accessor; `SAMETHREAD` relation.
- **warp** — `WCOUNT` is a warp-scalar clock advanced by `__syncwarp`; `SAMEWARP` relation; `WARPSYNC` level.
- **block/workgroup** — `BCOUNT` is a block-scalar clock advanced by `__syncthreads`; `SAMEBLOCK` relation; `BLOCKSYNC` level.
- **grid/GPU** — `SAMEGRID` relation; grid-wide synchronization is only the implicit kernel boundary in the model the paper targets.
- **node / cluster** — NOT_IN_PAPER. HiRace is single-kernel, single-GPU; there is no multi-GPU or multi-node component.

The design insight the paper states explicitly is that it "equates threads to the largest possible hierarchical thread group," i.e. the state abstracts *which* threads read to *at what scope* reads have occurred — hence `READ` → `WREAD` → `BREAD` → `GREAD` as the read set widens from one thread to warp to block to grid [paper] [code].

The 10-bit `TID` and 15-bit `BLOCK` fields are a real capacity bound: blocks larger than 1024 threads or grids larger than 32768 blocks cannot be represented in the default layout `[inference from code field widths]`. The paper does not state this bound; it states only that the shadow width is "configurable" [paper].

## 12.7 Pseudo code

The paper's Algorithm 1 is a lock-free CAS retry loop. Names below are the paper's [paper]; the `__` prefixed macros are actual code symbols [code].

```
// per monitored access, on device
repeat
  oShadow <- ATOMICREAD(sAddr)                  // 64-bit shadow word
  (oTid, oBlock, oState, oBC, oWC) <- unpack(oShadow)   // GET_TID/GET_BLOCK/GET_STATE/GET_BCOUNT/GET_WCOUNT [code]
  tRel  <- COMPARETIDS(tid, oTid)               // -> SAMETHREAD|SAMEWARP|SAMEBLOCK|SAMEGRID
  sRel  <- CHECKSYNC(bc, oBC, wc, oWC)          // -> UNSYNC|WARPSYNC|BLOCKSYNC
  trans <- GETTRANS(oState, access, sRel, tRel) // access in {R,W,BA,GA}
  nState<- STATEMACHINELOOKUP(trans)            // single flat-array lookup
  nShadow <- pack(tid, block, nState, bc, wc, swidx)
until ATOMICCAS(sAddr, oShadow, nShadow)
if nState == RACE then report
```

`CHECKSYNC` compares the accessing thread's own barrier counters against those stored in the shadow word: if the stored block clock is older than the accessor's, a `__syncthreads` separates the two accesses and the pair is block-synchronized `[reconstruction]` — the paper describes the clocks as "hierarchical synchronization counters" and the source keeps `__hr_bcount`/`__hr_wcount` per thread [paper] [code: `HIRACE_SET_DATA_GLOBAL` passes `&__hr_bcount, &__hr_wcount, &__hr_swidx`].

## 12.8 Real implementation

Repository `https://github.com/JohnJacobsonIII/HiRace-Artifact-SC24`, commit `44a935f90acfe43c6178b2187ea84c9ab0c01450` [code].

Verified structure:
- `src/clang/CudaRW.cpp` (275 lines), `src/clang/CudaRWMain.cpp`, `src/clang/include/CudaRW.h` — the Clang LibTooling source-rewriting pass. This confirms the paper's claim that instrumentation is source-to-source through "Clang's source rewriting API" rather than NVBit or a PTX pass [paper] [code].
- `src/hirace/HiRace.h` (1633 lines) — the FSM: state macros `INIT`(0), `READ`(1), `WRITE`(2), `WREAD`(3), `BREAD`(4), `GREAD`(5), `WSYNC`(6), `BSYNC`(7), `MR_WSYNC`(8), `BWSYNC`(9), `B_MR_BSYNC`(10), `W_MR_BWSYNC`(11), `BATOM_B`(12), `WSYNC_ATOM`(13), `BATOM_W`(14), `WSYNC_ATOM_M`(15), `GATOM_G`(16), `BSYNC_ATOM`(17), `BATOM`(18), `GATOM_B`(19), `BSYNC_ATOM_B`(20), `GATOM`(21), `GATOM_W`(22), `BSYNC_ATOM_W`(23), `RACE`(24) [code]. Accessors `get_tid`, `get_block`, `get_state`, `get_bcount`, `get_wcount` are `__device__` functions [code].
- `src/hirace/HiRaceDataWrap.h` (525 lines) — the `HiRaceDataWrap<TYPE>` templated wrapper class the paper describes, which overrides the subscript operator and atomic/sync functions [paper] [code].
- `src/hirace/HiRaceWrappers.h` (30 lines) — the user-facing macros `HIRACE_SHADOW_DECL`, `HIRACE_MALLOC` (`cudaMalloc` of `SIZE * sizeof(hr_shadowt)`), `HIRACE_MEMSET`, `HIRACE_CUDA_FREE`, `HIRACE_WRAP_DATA`, `HIRACE_SET_DATA_GLOBAL` [code]. `HIRACE_SET_DATA_GLOBAL` passes `Scope::Global`, confirming an explicit scope enum in the wrapper [code].
- `HiRace_FSM_State_Transitions.xlsx` — the transition table as a spreadsheet [code].
- `iGUARD-SOSP21/` — the IGUARD baseline is vendored into the artifact, so the head-to-head comparison is reproducible [code].
- `indigo/indigo_sources/…` — the Indigo generated CUDA kernels, with filenames encoding the injected bug kind: `…_boundsBug.cu`, `…_atomicBug.cu`, `…_boundsBug_atomicBug.cu`, and pattern/variant tokens `_persistent`, `_last`, `_reverse`, `_cond` [code]. This is direct evidence of how the 580-kernel suite is constructed combinatorially.
- A `RACECHECK` compile-time switch exists in `HiRace.h` (line 183/198), i.e. the header can be built in a racecheck-comparison mode [code].

## 12.9 Kernel execution

- **kernel** — instrumentation is per-kernel-launch; shadow memory is allocated host-side before launch (`HIRACE_MALLOC`) and zeroed (`HIRACE_MEMSET`), so state `INIT`=0 is the memset value [code]. Implicit device synchronization at the kernel boundary is the grid-level happens-before edge [paper].
- **thread block** — `__syncthreads` advances the per-thread `bcount`; the `BLOCKSYNC` sync level and `SAMEBLOCK` relation are what make an intra-block write-after-read legal [paper] [code].
- **warp** — `__syncwarp` (including mask variants) and warp-voting primitives advance `wcount`; the paper states "all variations of syncthreads, syncwarps, and warp-voting primitives" are supported [paper]. Crucially, *masked* warp sync is called out as a limitation: "masked warp synchronization primitives may be used to implement non-hierarchical barrier points, which are not amenable to representation within HiRace's FSM" [paper]. This is the sharpest boundary of the abstraction — it is exactly the case where the sync relation stops being a lattice over full thread groups.
- **instruction** — each instrumented load/store/atomic becomes: one shadow read, one relation computation, one table lookup, one CAS, retried on contention [paper] [code].

## 12.10 Memory traffic

- **register ↔ shared/L1** — the FSM table is a flat array; the paper does not state whether it resides in constant, shared, or global memory. NOT_IN_PAPER.
- **L1/L2 ↔ HBM** — the dominant added traffic is the 8-byte shadow word per monitored address, read and CAS-written on every monitored access. This doubles-plus the request count on the monitored data stream and adds an atomic (serializing at the L2 atomic units) `[inference]`.
- **Capacity.** 8 bytes of shadow per monitored address, versus the state of the art's 16 bytes for two prior accessors [paper]. The paper reports running "all of our tests with less than half of the memory overhead of IGUARD" [paper]. The halving is a direct consequence of the abstraction: a fixed-width state replaces a variable-length accessor set.
- **Multi-GPU path** — NOT_IN_PAPER; no NVLink/PCIe component.

## 12.11 Why it is faster/slower (decomposed cause)

HiRace is faster than IGUARD for three separable reasons, all stated or verifiable:

1. **Constant-width metadata, no eviction logic.** A fixed 64-bit state means no access-record table, no eviction policy, and no associative search of prior accessors. IGUARD's per-address record is large enough that it can hold only one prior accessor and must evict [paper]. Eliminating the eviction path removes both the memory traffic and the control divergence around it `[inference]`.
2. **One table lookup instead of a clock comparison loop.** The transition is a single flat-array index [paper], rather than a vector-clock comparison whose cost grows with the tracked thread set.
3. **Source-level instrumentation instead of binary instrumentation.** HiRace instruments through Clang source rewriting, so the injected code is compiled and optimized *with* the kernel by `nvcc`; IGUARD depends on NVBit, which the paper notes is "deprecated" for its purposes and which injects at the SASS level after optimization [paper] [code]. Register allocation and scheduling of the check code can therefore be interleaved with the application's, which binary instrumentation cannot do `[inference]`.

Against `compute-sanitizer racecheck` the comparison is not primarily speed but scope: racecheck found 92/346 injected races at every input size because it only inspects block-shared memory, so global-memory races are structurally invisible to it [paper].

The residual slowdown (see 12.12) is the CAS retry loop: every monitored access is an atomic read-modify-write on a shadow word, so threads in a warp touching the same shadow line serialize `[inference]`.

## 12.12 Hardware generation dependence

- Evaluation hardware: a single **NVIDIA GeForce RTX 2070 Super** (Turing; the paper does not print the compute capability), host **AMD Ryzen 5 3600**, **CUDA 11.7**, **Ubuntu 22.04** [paper]. This is a consumer Turing part, not a datacenter GPU — no A100/H100/MI250X result is reported. Any claim about HiRace's overhead on HBM-equipped datacenter GPUs is unsupported by this paper.
- The design is generation-dependent in one important way and generation-*independent* in another:
  - Dependent: the 10-bit `TID` / 15-bit `BLOCK` fields encode a maximum block and grid shape [code] `[inference]`; and the abstraction assumes the bulk-synchronous scoped-barrier model. Features that break that model — masked warp sync, and by extension the more flexible `cooperative_groups` tiles and async barriers of Ampere/Hopper — are outside the FSM [paper].
  - Independent: because instrumentation is at Clang source level rather than on SASS, HiRace does not need per-architecture SASS decoders. The paper makes exactly this argument against IGUARD, which is "incompatible with NVIDIA architectures released since its publication" [paper]. This is a genuine portability advantage of the source-rewriting choice.
- Cooperative groups: the paper calls them "conceptually the same" but states they were not explicitly tested [paper]. Treat cooperative-groups support as UNKNOWN.
- Dynamic parallelism, CUDA streams, multi-GPU, CUDA graphs, unified memory: no explicit support statement in the FSM design [paper]. Record as NOT_IN_PAPER rather than as unsupported.

## 12.13 Limitations

Stated by the authors [paper]:
1. Lock-based synchronization and release-acquire communication are *not* improved over prior art; HiRace falls back to traditional methods (lock tables) for these.
2. Masked warp-synchronization primitives create non-hierarchical barriers that the FSM cannot represent.
3. Barrier-clock overflow: if a thread witnesses more barriers than `BCOUNT`/`WCOUNT` can hold, the user must widen the shadow word.
4. Dynamic-analysis incompleteness: data-dependent control flow means the tool only sees races on paths the inputs drive. The paper's own numbers show this — on 5-node graphs only 182/346 races were found, and the authors attribute every miss to control flow not reaching the buggy code [paper].

Observed by this analysis:
5. Single consumer-GPU evaluation (RTX 2070 Super) [paper]. No datacenter-GPU or multi-GPU result.
6. The completeness claim is relative to *injected* races in a generated suite, not to races in unmodified production HPC applications. The real-application portion (Rodinia SRAD/Backprop/Gaussian; cuda-samples Black Scholes, ConvolutionFFT2d, FastWalshTransform) found no races, so it measures overhead, not detection [paper].
7. The 10-bit/15-bit shadow field widths bound block and grid size in the default build `[inference from code]`; the paper states only that width is configurable.

## 12.14 Relation to prior corpus

- **Prior corpus:** `NO_EXISTING_ANALYSIS`. Repository-wide grep for "HiRace" returns only `domains/gpu_systems/census/SC_2024.md` (a census row) and `domains/hpc_quantum/corpus/quantum-hpc-survey/corpus/data/sc24_main.tsv` (a raw TOC dump, existence evidence only, explicitly not an analysis per the task's §4 rule). No substantive prior analysis exists.
- **Competing / superseded:** IGUARD (SOSP 2021) is the direct competitor and is vendored in the artifact [code]. `compute-sanitizer racecheck` is the vendor baseline. PUG and GPU-Verify are the static-analysis alternatives, criticised for false alarms; Faial/FaialAA is named as a static approach whose handling of irregular codes is "as yet unknown" [paper].
- **Complementary within this cluster:** *RedSan* (SC 2025, a redundant memory-instruction sanitizer for GPU programs) and *Triton-Sanitizer* (ASPLOS 2026) occupy the same GPU-sanitizer niche; *Over-Synchronization in GPU Programs / ScopeAdvice* (MICRO 2024) and *Towards Unified Analysis of GPU Consistency* (ASPLOS 2024) attack the inverse problem — too much synchronization, and the formal semantics of GPU scopes that HiRace's sync lattice informally assumes. See `_LEDGER_profiling_reliability.md`.
- **Precursor:** the Indigo suite is Burtscher-group infrastructure reused here as the bug corpus [code: `indigo/indigo_sources/`].

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The contribution *is* an abstraction of the GPU's scoped, hierarchical barrier semantics — the FSM's axes are literally `{UNSYNC, WARPSYNC, BLOCKSYNC}` × `{SAMETHREAD, SAMEWARP, SAMEBLOCK, SAMEGRID}` [code], i.e. the SIMT thread hierarchy and CUDA's scoped atomics (`BA` block-scoped vs `GA` grid-scoped) are the state space itself. On a CPU the standard solution (FastTrack vector clocks) is what HiRace explicitly replaces, and the motivating capacity constraint — that per-accessor records cannot cover full device memory, which is why NVIDIA's own tool checks only block-shared memory — is a property of GPU device-memory scale and the shared-memory/global-memory split. Remove warps, scoped barriers, and the shared/global distinction and there is no contribution left.

# GPU-SC26-41 — LEO: Tracing GPU Stall Root Causes via Cross-Vendor Backward Slicing

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `N — profiling, debugging, correctness checking, simulation & performance modelling`
secondary_topics: `GPU stall taxonomy; SASS/ISA-level analysis; PC sampling; cross-vendor (NVIDIA/AMD/Intel) portability`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_VIA_TWO_TARGETED_PASSES — arXiv 2604.20032 v1 HTML read for (a) title/authors/affiliations/abstract, motivation, the five-phase workflow, the CCT dependency-graph design, instrumentation substrate, evaluation platforms and workload list, and limitations; and (b) the per-vendor synchronization-mechanism modelling (s_waitcnt vmcnt/lgkmcnt, NVIDIA barrier bits B1-B6, Intel SWSB/SBID), the four pruning stages, the inverse-distance blame formula, the per-vendor PC-sampling stall taxonomies, overhead and analysis-time figures, the per-workload speedup table, and the related-work positioning. NOT read line-by-line: individual case-study narratives beyond the optimizations named in the speedup table. VENUE NOT ESTABLISHED — see 12.1.`

## 12.1 Bibliographic facts

- Official title: *LEO: Tracing GPU Stall Root Causes via Cross-Vendor Backward Slicing* [paper].
- Authors: **Yuning Xia, John Mellor-Crummey** — Rice University, Houston, TX, USA [paper]. Two authors only.
- **Venue: UNRESOLVED.** The arXiv record carries **no venue comment** [paper]. The census records the title as `NOT_FOUND` in any official SC26 source and marks SC26 membership `UNVERIFIED` (`census/SC_2026.md` rows 9 and §5). The task assigned it as "SC 2026"; that attribution is **not corroborated by any source available in this environment.** Treat the venue as `UNKNOWN` and the publication type as `PREPRINT` until an official SC26 program entry is found.
- Public full text: `https://arxiv.org/abs/2604.20032`; HTML `https://arxiv.org/html/2604.20032v1` (v2 also exists per the census). `arxiv.org/pdf/2604.20032` returned no machine-readable text in this environment; the `/abs/` page likewise returned nothing extractable. The `/html/2604.20032v1` path is the only one that yielded content — record this for future retrieval.
- Artifact: `NOT_FOUND_AFTER_SEARCH`. No repository is named in the material read. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Vendor GPU profilers report *where* a warp stalled and under which stall category, but not *which earlier instruction caused it* — so can instruction-level backward slicing over disassembled machine code recover the causing instruction, and do so uniformly across NVIDIA, AMD and Intel GPUs whose synchronization hardware is entirely different? [paper]

## 12.3 GPU/HPC problem translation

- **Compute.** The object of analysis is the SM/CU issue pipeline: which instruction's latency was not hidden, and by which producer.
- **Synchronization.** The paper's distinguishing technical content is synchronization modelling — AMD's explicit software-managed wait counters, NVIDIA's scoreboard barrier bits, Intel's software scoreboard tokens. These are *compiler-inserted* dependency declarations, and LEO reads them as ground truth.
- **Memory.** Memory dependencies are the main stall source traced, but through the register/scoreboard dependency graph rather than through cache-hierarchy counters.
- **Communication / scheduling.** NOT_IN_PAPER. Single-GPU, single-kernel scope.

## 12.4 Why the problem exists (down to hardware root cause)

- **A stall reason is a symptom, not a cause.** Vendor tools "show *where* stalls occur but not *why*," reporting "per-instruction stall distributions without identifying which earlier instructions caused observed stalls" [paper]. Knowing an instruction stalled on "memory dependency" does not say which load to move, prefetch, or tile.
- **The hardware root cause of the difficulty is that GPUs express dependencies in three incompatible ways**, none of which is a conventional out-of-order scoreboard recoverable by uniform dataflow analysis [paper]:
  - **AMD** uses explicit `s_waitcnt` instructions carrying counter arguments — `vmcnt(N)` for vector-memory operations and `lgkmcnt` for LDS/constant operations. The wait is a *count of outstanding operations to drain*, not a named register dependency, so recovering "which load am I waiting for" requires counting backwards through the issue stream.
  - **NVIDIA** encodes hardware barriers **B1–B6** in SASS instruction control fields via `Control.read`/`Control.write` bits. A consumer waits on a barrier mask; the producer sets a barrier. The dependency is real but lives in instruction control bits, not in the opcode.
  - **Intel** Xe-HPC uses a software scoreboard with **SBID 0–31** tokens; instructions carry `dst_wait`/`src_wait` directives naming an SBID that some earlier `send` set.
- Because these are compiler-inserted and compiler-verified, LEO treats edges derived from them as authoritative: synchronization-traced edges "bypass opcode and latency pruning" [paper]. That is the key design consequence of the hardware difference — the analysis trusts the compiler's own dependency declaration over its own heuristics.
- **PC sampling is statistical**, so "cold instructions receive few samples" [paper] — the measurement substrate is inherently sparse.

## 12.5 Mathematical / performance model

The blame-attribution rule is the paper's one closed-form expression (its Equation 1) [paper]:

```
blame_i = S_j * ( R_i^dist * R_i^eff * R_i^isu * R_i^match )
               / SUM_k ( R_k^dist * R_k^eff * R_k^isu * R_k^match )
```

where `S_j` is the stall sample count at the stalled (consumer) instruction `j`, and the four factors are [paper]:

| Factor | Definition | Rationale (paper's words) |
|---|---|---|
| `R_i^dist = d_min / d_i` | inverse distance | "Closer instructions receive more blame, as they have less opportunity to hide latency." |
| `R_i^eff = e_min / e_i` | inverse efficiency | "Less efficient instructions (e.g., uncoalesced memory accesses) receive more blame." |
| `R_i^isu = n_i / SUM_k n_k` | issue share | "Instructions executed more frequently receive proportionally more blame." |
| `R_i^match` | stall-type match | "Weights each edge by how well its dependency type … matches the destination's hardware-reported stall breakdown." |

The stall samples at a consumer are thus distributed multiplicatively over candidate producers and normalised. The formula is a **heuristic** and the authors say so — "inverse-distance weighting is heuristic; branch probability modeling is absent" [paper]. There is no probabilistic or queueing model behind it; the `R^dist` factor is a proxy for latency-hiding opportunity, not a computation of it.

Note `R_i^eff` is architecturally meaningful: memory-access *efficiency* (e.g. coalescing) is a GPU-specific per-instruction quantity, and using it as a blame weight encodes the assumption that an uncoalesced access is a likelier culprit than a coalesced one at equal distance.

## 12.6 Data layout and ownership

LEO's data structure is a **Calling Context Tree (CCT) dependency graph** built from disassembled machine code [paper]. The ownership mapping is unusual for this cluster because the analysis is *static structure annotated with sampled dynamic weights*:

| Level | What LEO holds |
|---|---|
| instruction | node in the dependency graph; carries PC-sample stall counts, execution count, efficiency |
| basic block / CFG | control-flow paths used by latency pruning |
| function / calling context | the CCT provides context-sensitive attribution |
| warp / wavefront | **implicit only** — stalls are per-instruction aggregates over sampled warps; individual warps are not tracked |
| SM / CU | not represented |
| GPU | one per measurement; three vendors compared side by side |
| node / cluster | NOT_IN_PAPER |

Edge types are typed by provenance [paper]: ordinary register **RAW** edges, plus the three synchronization-derived classes `mem_waitcnt` (AMD), `mem_barrier` (NVIDIA), `mem_swsb` (Intel).

Instruction representation: **disassembled machine code**, explicitly "rather than higher-level representations" — **NVIDIA SASS**, **AMD RDNA** (as named in the source; the evaluated part is MI300A/CDNA3, so the ISA family naming in the abstract and the evaluated hardware are not perfectly aligned — record as a minor internal inconsistency), and **Intel Xe ISA** [paper].

## 12.7 Pseudo code

The five-phase workflow [paper], with the internals of phases 3–5 `[reconstruction]`:

```
# Phase 1 — data collection
binary   <- extract device image
disasm   <- nvdisasm | llvm-objdump | GED            # per vendor
profile  <- PC samples with per-instruction stall breakdown

# Phase 2 — binary analysis
cfg <- build control-flow graph per function; build CCT

# Phase 3 — dependency graph
for each instruction c (consumer):
    for each source register r of c:
        add RAW edges from reaching definitions of r
    if c is a wait instruction:
        case AMD  's_waitcnt vmcnt(N)':
            # M = total outstanding count at this point
            # drain the (M - N) OLDEST pending memory ops
            scan backward, stopping at an epoch boundary where a prior
              s_waitcnt already drained the counter
            add mem_waitcnt edges to those ops
        case AMD  'lgkmcnt(N)':  same, over LDS/constant ops
        case NVIDIA barrier wait mask:
            scan backward for instructions setting a matching barrier B1..B6
              (Control.read / Control.write bits)
            add mem_barrier edges
        case INTEL 'dst_wait/src_wait SBID T':
            scan backward for the send that set SBID T
            add mem_swsb edge

# Phase 4 — four-stage pruning (synchronization edges are EXEMPT from 1 and 3)
prune_opcode:    drop edges whose producer type cannot explain the consumer's
                 stall profile (e.g. compute producer, memory-only stall profile)
prune_barrier:   (NVIDIA only) drop edge if producer sets a barrier the
                 consumer does not wait on
prune_latency:   walk CFG paths producer -> consumer accumulating
                   control.stall cycles (NVIDIA) or instruction counts (AMD/Intel);
                 drop the edge if accumulated issue cycles exceed the producer's
                   latency threshold on ALL CFG paths
prune_exec:      (optional) drop edges from instructions with zero execution count

# Phase 5 — blame attribution
for each stalled consumer j with S_j samples:
    distribute S_j over surviving producers by Equation 1
```

The AMD `s_waitcnt` handling is the single most architecture-specific piece of logic in the tool and is what the authors claim no prior GPU slicer had: GPA "cannot trace memory access dependencies through synchronization instructions such as AMD's `s_waitcnt`" [paper].

## 12.8 Real implementation

No artifact repository identified — `NOT_INSPECTED`. The stated software substrate, however, is specific and checkable [paper]:

- **HPCToolkit**, via its `hpcanalysis` API, provides the cross-vendor PC-sampling infrastructure. LEO is built on HPCToolkit rather than beside it; Mellor-Crummey is the HPCToolkit lead, so this is the group's own substrate.
- **NVIDIA CUPTI** — used for the Activity API; stall taxonomy of **13 categories**, with a latency-versus-total-sample distinction available on compute capability 6.0+.
- **AMD ROCprofiler-SDK** — stochastic sampling mode; **10+** stall categories.
- **Intel Level Zero metrics** — EU stall sampling; **8** categories.
- Disassemblers: **`nvdisasm`** (NVIDIA), **`llvm-objdump`** (AMD), **GED** (Intel).

No symbol names beyond these API/tool names were read; do not attribute internal LEO symbols.

## 12.9 Kernel execution

- **kernel → instruction** is the axis LEO actually resolves; **thread block and warp are not modelled**. Stall samples are per-instruction aggregates, so LEO answers "which instruction caused this instruction to wait" and not "which warp diverged" or "why occupancy is low."
- The **latency-pruning** stage is where the execution model enters: on NVIDIA it accumulates `control.stall` cycles along CFG paths — i.e. it reads the *compiler's own static stall-cycle hints in the SASS control field* — whereas on AMD and Intel it falls back to counting instructions [paper]. This is an asymmetry in fidelity, not just in syntax: the NVIDIA path uses a real cycle budget, the other two use an instruction-count proxy `[inference]`.
- Because synchronization edges bypass latency pruning, the wait-instruction path does not depend on that proxy [paper] — which is presumably why the authors exempted them.

## 12.10 Memory traffic

LEO does not measure traffic. It reaches memory behaviour through two indirect channels [paper]:
1. the `R^eff` blame factor, which encodes per-instruction access efficiency (coalescing), and
2. the memory-dependency stall categories in each vendor's PC-sampling taxonomy.

The *optimizations* LEO's analyses led to are, however, almost entirely memory-hierarchy optimizations, which is indirect evidence that the memory path is where its diagnoses land [paper]: "Tile elldat into (SMEM/LDS/SLM)" for LTIMES, "Precompute basis in regs" for MASS3DEA, `ldg float4` vectorised loads and scalar broadcasts for miniBUDE, and a RAJA iteration-order swap (Zone ↔ Group) for Kripke LTimes. Register promotion, scratchpad tiling, vector-width widening, and loop-order change — the classic GPU memory-hierarchy toolkit.

## 12.11 Why it is faster/slower (decomposed cause)

LEO itself is a post-mortem analyzer: it "performs post mortem analysis of previously collected profiles and therefore adds no runtime overhead" [paper]. Its costs and benefits decompose as:

**Cost side** [paper]:
- Measurement overhead: **~10% on AMD** at HPCToolkit's default sampling frequency; **~10% on Intel** at the shortest recommended sampling period of 100 μs. **NVIDIA overhead is not given as a percentage**; instead the authors flag a distortion: "NVIDIA's Activity API serializes kernel execution, potentially distorting measurements." That is a correctness caveat, not a cost figure, and it means NVIDIA measurements are taken under a modified execution regime.
- Analysis time: **3–10 s per kernel on one CPU core** (3.6 s for RAJAPerf on AMD; 8.1 s for QuickSilver on NVIDIA); NVIDIA tensor-core kernels with **>8,000 edges took about 60 s** [paper]. The tensor-core blow-up is the scaling weak point — dense tensor-core code generates far more dependency edges.

**Benefit side** — and this is where the claim must be read carefully. The reported **geometric-mean speedups are 1.73× (NVIDIA GH200), 1.74× (AMD MI300A), 1.82× (Intel PVC)** over 21 workloads [paper]. But the authors state that "speedup evaluation uses expert-designed optimizations informed by LEO analysis" [paper]. **The speedup measures what an expert achieved with LEO's guidance, not what LEO achieved.** There is no control arm in which the same experts optimised the same kernels without LEO. The honest claim is that LEO's diagnoses were actionable, not that they were necessary.

Selected per-workload results, with the optimization applied [paper]:

| Workload | Optimization | NVIDIA GH200 | AMD MI300A | Intel Max 1100 |
|---|---|---|---|---|
| Kripke LTimes | swap Zone ↔ Group iteration order (RAJA) | 11.67× | 1.90× | N/A |
| LTIMES | tile `elldat` into SMEM/LDS/SLM | 5.02× | 4.00× | 3.01× |
| MASS3DEA | precompute basis in registers | 3.66× | 2.51× | 10.32× |
| PRESSURE | fuse 2 kernels | 2.55× | 2.06× | 1.84× |
| miniBUDE | `ldg float4`, scalar broadcasts, USM | 2.20× | 1.20× | 1.03× |

The cross-vendor spread within a single optimization is itself informative: MASS3DEA's register-promotion gains 10.32× on Intel but 2.51× on AMD; miniBUDE's vectorisation gains 2.20× on NVIDIA but 1.03× on Intel. The same root cause has very different magnitude per architecture `[inference]` — the paper reports the numbers without drawing this out.

## 12.12 Hardware generation dependence

This is the most explicitly multi-vendor paper in the cluster. Evaluation platforms [paper]:
- **AMD MI300A** — CDNA3, **228 CUs**, **5.3 TB/s** memory bandwidth.
- **NVIDIA GH200** — Hopper, **132 SMs**, **4.0 TB/s**.
- **Intel GPU Max 1100** — Xe-HPC, **56 Xe-cores**, **1.23 TB/s**.

Dependence structure:
- **Per-vendor synchronization decoding is hard-wired** — `s_waitcnt`/`vmcnt`/`lgkmcnt`, B1–B6 barrier control bits, SBID 0–31. A new ISA needs new decoding logic. This is the maintenance liability of the SASS/ISA-level choice, and the mirror image of `GPU-SC24-41` (HiRace), which deliberately instrumented at Clang source level precisely to avoid per-architecture decoders.
- **Per-vendor disassemblers** (`nvdisasm`, `llvm-objdump`, GED) are external dependencies.
- **Stall taxonomies differ in size and definition** (13 / 10+ / 8 categories). The authors concede the taxonomies "overlap conceptually (memory, synchronization, dependencies)" but that "their definitions differ, requiring LEO to map vendor-specific stall reasons to a common dependency classification" — and, importantly, **"explicit unified taxonomy is not detailed in the text"** [paper]. So the cross-vendor claim rests on a mapping the paper does not fully publish. That is a real gap in the central contribution and should be recorded as UNKNOWN.
- **Latency pruning is higher-fidelity on NVIDIA** (real `control.stall` cycles) than on AMD/Intel (instruction counts) [paper].

## 12.13 Limitations

Stated by the authors [paper]:
1. **Register dataflow only** — "pointer-chasing and indirect memory operations may hide root causes." A dependency through memory rather than through a register is invisible.
2. **Heuristic blame** — inverse-distance weighting is a heuristic; **branch probability modeling is absent**, so CFG paths are not weighted by likelihood.
3. **PC-sampling sparsity** — cold instructions receive few samples.
4. **NVIDIA Activity API serializes kernel execution**, potentially distorting measurements.
5. **Speedups come from expert optimizations informed by LEO**, not from LEO alone.
6. **No ground-truth validation of individual dependency chains** — "evaluation relies on case studies and downstream performance improvements." No dependency chain is independently verified as correct.

Observed by this analysis:
7. **The unified cross-vendor stall taxonomy — the paper's headline claim — is not spelled out in the text** [paper]. UNKNOWN.
8. **No artifact identified**, so neither the slicer nor the mapping is reproducible.
9. **Venue unverified** (12.1); the census could not place it in any official SC26 source.
10. **Analysis cost scales badly with tensor-core density** (60 s for >8,000-edge kernels versus 3–10 s typical), which is precisely the kernel class that matters most for current AI workloads.
11. Minor internal inconsistency: the abstract/ISA discussion names **AMD RDNA** while the evaluated part is **MI300A (CDNA3)**.

## 12.14 Relation to prior corpus

- **Prior corpus:** `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Backward Slicing" and for the arXiv ID `2604.20032` returns only `domains/gpu_systems/census/SC_2026.md`. ("LEO" alone matches many census files as a substring of unrelated words and is not evidence.)
- **Direct precursor, named by the paper itself:** **GPA (GPU Performance Advisor)**, which "pioneered backward slicing for GPUs, but GPA supports only NVIDIA GPUs and cannot trace memory access dependencies through synchronization instructions such as AMD's `s_waitcnt`" [paper]. LEO's delta over GPA is exactly (a) multi-vendor and (b) synchronization-aware tracing.
- **Substrate:** HPCToolkit [paper].
- **Compared against:** NVIDIA Nsight Compute, AMD `rocprofv3`, Intel VTune/unitrace — all criticised as showing where but not why [paper].
- **Verified citation link into this cluster's verdict-only set:** LEO explicitly names **DeepContext** and **PASTA** as cross-platform tools that "lack instruction-level root-cause analysis" [paper]. *DeepContext: A Context-aware, Cross-platform, Cross-framework Tool for Performance Profiling and Analysis* is an ASPLOS 2026 paper in this cluster's verdict-only list — so LEO (arXiv 2026-04) and DeepContext (ASPLOS 2026) are a verified citing pair, and LEO positions itself one level *below* DeepContext in abstraction (instruction-level root cause versus context-aware cross-framework profiling).
- **Complementary within this cluster:** `GPU-MICRO25-01` (STEM+ROOT) and `GPU-HPCA24-41` (GPU Scale-Model Simulation) attack the same "GPU performance analysis is too expensive" problem from the simulation side; LEO attacks it from the hardware-measurement side. *GCStack+GCScaler* (ISCA 2025, `PUBLIC_ARTIFACT_ONLY`, watchlisted) is the closest relative of all — it builds a fine-grained stall-cycle taxonomy in a *simulator*, where LEO builds one from *real hardware PC samples*. See `_LEDGER_profiling_reliability.md` for the cross-paper stall-taxonomy comparison.
- **Methodological contrast with `GPU-SC24-41`:** LEO instruments at the vendor ISA level and therefore needs per-architecture decoders; HiRace instruments at Clang source level and therefore does not. The two papers make opposite engineering bets on the same portability problem, and each names the other bet's cost.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The contribution is a dependency-graph construction that decodes GPU-specific, compiler-managed synchronization hardware — AMD `s_waitcnt` with its `vmcnt`/`lgkmcnt` outstanding-operation counters, NVIDIA's B1–B6 scoreboard barrier bits carried in SASS instruction control fields with their `Control.read`/`Control.write` flags and `control.stall` cycle hints, and Intel's SWSB `SBID` tokens — and that consumes per-vendor GPU PC-sampling stall taxonomies (CUPTI's 13 categories, ROCprofiler-SDK's 10+, Level Zero EU stall sampling's 8). None of these mechanisms exists on a CPU, where dependencies are resolved by hardware out-of-order scoreboards and no `s_waitcnt`-style software wait counter has to be reverse-counted. Prior machine-code slicing work on CPUs (Cifuentes & Fraboulet; Srinivasan & Reps, both cited) did not face this problem at all, which is precisely why the paper exists.

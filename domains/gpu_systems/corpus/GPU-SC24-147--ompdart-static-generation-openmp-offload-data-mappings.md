# GPU-SC24-147 — Static Generation of Efficient OpenMP Offload Data Mappings (OMPDart)

gpu_relevance: `CORE_GPU` (**boundary case — see the counterfactual record; this is the weakest `CORE_GPU` in this cluster and the reasoning is stated explicitly rather than assumed**)
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — GPU programming models and compilers: OpenMP target offload, static generation of host/device data mappings`
secondary_topics: `Clang/LLVM static analysis (AST-CFG, interprocedural, data-flow, array bounds); host-device transfer minimisation; correctness of hand-written map clauses`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2406.13881v1), read in two passes — (a) title/authors/affiliations, motivation and why hand-writing map clauses is error-prone, the tool's name and hybrid AST-CFG representation, the five analysis passes (parsing/access classification, interprocedural, data-flow, array access pattern, rewriter) and the OpenMP constructs emitted; (b) evaluation — GPU SKU, CUDA and Clang versions, the nine Rodinia/HeCBench applications, the three compared versions, speedups and transfer reductions, the correctness check and its one exception, the stated limitations and future work, related work. The arXiv HTML does not print the venue — venue rests on census evidence.`

## 12.1 Bibliographic facts

- Title: **Static Generation of Efficient OpenMP Offload Data Mappings** [paper]. The tool is named **OMPDart** ("OpenMP Data Reduction Tool") [paper].
- Venue: **SC 2024**, DOI `10.1109/SC41406.2024.00041` [census: `domains/gpu_systems/census/SC_2024.md`, row 15]. The arXiv HTML does not state the venue [paper] — venue is `[census]` evidence.
- Authors, all **Department of Computer Science, Iowa State University, Ames, Iowa, USA** [paper]: **Luke Marzen, Akash Dutta, Ali Jannesari**.
- Preprint: **arXiv 2406.13881** (the version read). Artifact: **Zenodo `https://zenodo.org/records/12562040`** ("SC24 Artifact: OMPDart"), surfaced by search — `NOT_INSPECTED`; **no source symbols are asserted below**.
- Publication type: `ARCHIVAL_MAIN_PAPER` (+ `PREPRINT` arXiv 2406.13881).

## 12.2 Core question (one sentence)

OpenMP's *implicit* data-mapping rules move an array to the device and back at every `target` region, and writing the explicit `map`/`update` clauses that avoid this requires the programmer to "keep a mental model of data validity and lifetime spanning multiple data environments" [paper] — can a purely static Clang/LLVM analysis generate those clauses automatically, and do so well enough to match or beat the expert-written mappings shipped with Rodinia and HeCBench?

## 12.3 GPU/HPC problem translation

- **Communication (host↔device).** This *is* the paper. "the implicit OpenMP data-mapping rules often result in redundant data transfer, which can be a bottleneck for program performance" [paper]. The optimised resource is PCIe/NVLink traffic between host DRAM and device HBM.
- **Memory.** Two disjoint address spaces with independently-valid copies of the same array. The analysis's state is exactly "variable validity in each memory space" [paper].
- **Compute.** Untouched — OMPDart does not change kernels, only the data environment around them. This is worth stating plainly because it is what bounds the paper's GPU depth.
- **Synchronization.** Only through the ordering of `update to`/`update from` relative to `target` regions. `NOT_IN_PAPER` beyond that.
- **Scheduling.** `NOT_IN_PAPER`.

## 12.4 Why the problem exists (root cause)

- **The hardware root cause is the discrete device memory space.** A GPU's HBM is not the host's DRAM; every live array must exist in both and the runtime cannot know which copy is current without programmer annotation. OpenMP's defaults therefore choose the *safe* option — copy in, copy out, every region.
- **The language root cause** is that the `map` clause's scope is the `target` region, while the *correct* scope for a long-lived array is the whole function or loop nest. OMPDart's answer is structural: it "creates [a] single `target data` region per function encompassing all kernels" [paper], so the array's residency outlives any one kernel.
- **The human root cause**, which the paper leads with: hand-optimisation is "laborious and error-prone", demonstrated "through examples where programmers inadvertently introduce correctness bugs when attempting hand-optimization" [paper]. The paper's own results bear this out — it beats the expert mappings on LULESH (12.11).
- **The analysis root cause**: deciding which transfers are necessary is a true-dependence (RAW) question across two memory spaces, and the paper is explicit that it is undecidable in general — its related-work section reaches for "Rice's Theorem, Halting Problem … establishing inherent static analysis limitations" [paper]. Hence the conservative fallbacks in 12.13.

## 12.5 Mathematical / performance model

No analytical performance model. The formal content is a **data-flow analysis**, and it is recorded as such:

- **Representation**: a **hybrid AST-CFG** — "Clang/LLVM toolchain: **LibTooling**" parses C/C++ to an AST; a **CFG** is built per function; "Each CFG node links to corresponding AST representation, enabling both structural hierarchy and control flow analysis" [paper]. The hybrid exists because `map` clauses must be *placed at source syntax* while validity must be computed over *control flow*.
- **Five passes, as named by the paper** [paper]:
  1. **Parsing & Memory Access Classification** (§IV-B) — accesses classified as read, write, read/write, or **unknown**; per-function CFGs built.
  2. **Interprocedural Analysis** (§IV-C) — iterative over call sites, modelling global-variable and pointer-parameter access, "Appl[ying] maximally pessimistic assumptions about callee behavior".
  3. **Data-Flow Analysis** (§IV-D) — forward traversal tracking "variable validity in each memory space"; identifies **true (RAW) dependencies requiring communication**; creates one `target data` region per function; picks insertion points for `map` and `update`.
  4. **Array Access Pattern Analysis** (§IV-E) — bounds analysis extended to nested loops; **Algorithm 1** identifies "the outermost loop affecting array indexing", which is where an `update` can be hoisted to.
  5. **Rewriter** (§IV-F) — consolidates directives by insertion point and emits source.
- **Emitted constructs** [paper, Table II]: `map(to:)`, `map(from:)`, `map(tofrom:)`, `map(alloc:)`, `update to()`, `update from()`, `firstprivate()` (for scalars).

## 12.6 Data layout and ownership

The ownership hierarchy this paper reasons about is **not** the intra-GPU one; it is the two-memory-space one, and that is the honest way to record it:

- **host memory space**: holds the authoritative copy unless a `target` region has written the device copy.
- **device memory space (GPU HBM)**: holds a copy whose validity interval the analysis computes.
- **the `target data` region**: the *lifetime* object OMPDart synthesises, one per function, so that a device allocation spans all kernels in that function rather than one [paper].
- **array sub-ranges**: the array-access-pattern pass narrows `update` clauses to the bounds actually touched, hoisted to the outermost loop that affects the index [paper, Algorithm 1].
- **thread / warp / block / SM**: **`NOT_IN_PAPER`.** OMPDart performs no intra-kernel reasoning whatsoever. Stated plainly because it is central to the counterfactual discussion below.
- **GPU**: NVIDIA **A100** [paper].
- **node / cluster**: single device; no multi-GPU or MPI dimension. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- what the analysis computes, conceptually ---------------------  [paper]
# state: for each variable v, validity[v] in {host, device, both, unknown}

for each function f:
    cfg = build_CFG(f); ast = parse(f)            # LibTooling; hybrid AST-CFG
    classify_accesses(ast)                        # read | write | rw | unknown
    interprocedural_fixpoint()                    # pessimistic on unknown callees

    for node in forward_traversal(cfg):           # data-flow, §IV-D
        if node is a target region:
            for v read on device and valid only on host:
                emit  update to(v[lo:hi])         # bounds from §IV-E
            for v written on device:
                validity[v] = device
        if node reads v on host and validity[v] == device:
            emit  update from(v[lo:hi])

    wrap all target regions of f in ONE  #pragma omp target data map(...)
    rewriter.consolidate_and_emit()               # §IV-F
```

`[reconstruction]` applies to the loop shape. Pass names, section numbers, the validity-per-memory-space formulation, the one-`target data`-region-per-function rule, Algorithm 1's role, and the emitted clause list are printed in the paper.

## 12.8 Real implementation

- Built on **Clang/LLVM LibTooling** [paper]; operates as a **source-to-source** rewriter on C/C++ with OpenMP `target` directives.
- Compiled and evaluated with **Clang 17.0.4**, **CUDA 11.8.89**, on **NVIDIA A100** [paper].
- Artifact exists on Zenodo (`https://zenodo.org/records/12562040`) but was **`NOT_INSPECTED`**; no repository was cloned and **no symbols, pass class names or file paths are asserted**. This entry is `[paper]`-only on implementation, unlike `GPU-ASPLOS26-141`, `GPU-ASPLOS26-143` and `GPU-PPoPP24-146`.

## 12.9 Kernel execution

`NOT_IN_PAPER` at every level below the kernel. OMPDart does not alter kernel bodies, launch geometry, or any intra-kernel structure; the `target` region's contents are passed through unchanged. The only execution-level object it manipulates is the **`target data` region**, i.e. the device-residency scope surrounding one or more kernel launches.

## 12.10 Memory traffic

This is the paper's only measured quantity, and the numbers are large and highly variable — the qualifiers matter more than usual:

- **Per-benchmark data-transfer reductions**, on NVIDIA A100 with Clang 17.0.4 / CUDA 11.8.89, versus the **implicit** OpenMP mappings [paper]: **1010×, 400×, 2×, 65×, 23×, 1.2×, 2×, 20×**.
- **Data-transfer wall time**, geometric mean **5.1×** better than unoptimised [paper].
- **LULESH**: "**85% reduction in data transfer** and a **1.6× speedup** over **expert-defined** mappings" [paper] — the strongest result in the paper, because the comparison point is a hand-tuned mapping, not the naive default.
- The spread from 1.2× to 1010× is the signature of this problem class: when the implicit rule re-copies a large array per iteration, removing it is unbounded; when the program already had few transfers, there is nothing to win.
- No intra-GPU traffic decomposition (register/shared/L1/L2/HBM). `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Headline [paper, NVIDIA A100, nine applications from Rodinia and HeCBench]: geometric mean **2.8× over the default implicit data mapping rules** and **1.05× over the expert-defined mappings**; per-benchmark range **1.01× to 16×** over unoptimised.

Decomposed:

1. **Residency hoisting.** One `target data` region per function keeps arrays resident across every kernel in that function, collapsing N copy-in/copy-out pairs into one [paper]. This is the dominant effect and explains the 1010×/400× outliers.
2. **RAW-only transfers.** Only true dependencies across the memory-space boundary produce an `update` [paper]; anti- and output-dependencies within one space are free.
3. **Bounds-narrowed updates.** The array-access-pattern pass restricts an `update` to the touched sub-range and hoists it to the outermost index-affecting loop [paper, Algorithm 1] — this is what lets OMPDart *beat* experts on LULESH rather than merely match them.
4. **Where it barely helps**: the 1.01× and 1.2× cases — programs whose implicit mappings were already near-minimal.
5. **The 1.05× over experts is the real headline.** A geometric mean of 1.05× against hand-written mappings, with a single-benchmark high of 1.6× (LULESH), means the win is *parity plus removed effort and removed bugs*, not raw speed. The paper's correctness result reinforces this: all nine outputs matched the expert implementations [paper].

## 12.12 Hardware generation dependence

- **Single SKU**: NVIDIA A100, CUDA 11.8.89, Clang 17.0.4 [paper]. No AMD, no Intel, no cross-generation study.
- **The analysis itself is generation-independent** — it manipulates OpenMP source, not PTX. Re-targeting to MI300A or PVC requires only an OpenMP offload compiler, and nothing in the described design would change. This is simultaneously the tool's strength and the reason its GPU verdict is a boundary call (below).
- Notably, **unified/shared memory changes the premise entirely**: on an APU-style device with a single address space (cf. `GPU-ISC24-01`, MI300A unified memory), the transfers OMPDart removes do not exist. The paper does not discuss this. `NOT_IN_PAPER` — recorded as a scope question, not as a criticism of an unmade claim.

## 12.13 Limitations

Stated by the paper [paper]:

- **Single translation unit only**; external functions get "conservative, worst-case assumptions".
- **Array access analysis is implemented for `for` loops only** — `while`/`do` loops fall back.
- **Pointer aliasing** is handled conservatively; "single element array accesses [are] conservatively assumed to be the access of the entire array" — which can defeat the bounds narrowing that produces the best results.
- **Cannot detect deliberate staleness.** `backprop` "required manual adjustment to preserve intentional stale-data usage" [paper] — i.e. one of nine benchmarks needed human intervention, because a correct-by-dependence answer is not always the intended one.
- **No comparison against the closest prior tools.** "No direct comparisons with OMPSan, OmpMemOpt, or DawnCC were conducted" [paper]. This is a real evidentiary gap: the baselines are the implicit rules and the expert mappings, not competing automation.
- Static analysis is undecidable in general, which the paper acknowledges directly [paper].

## 12.14 Relation to prior corpus

- **Directly complementary to `GPU-ISC24-01` (Porting HPC applications to MI300A with unified memory and OpenMP)**: that paper's setting — unified memory — is the one in which OMPDart's optimisation target disappears. Read together they bracket the OpenMP-offload data-movement question from both sides of the unified-memory transition.
- **Complementary to `GPU-ICS25-145` (Taking GPU Programming Models to Task)**: that paper finds OpenMP offload scoring worst on the compute-bound kernel for intra-kernel codegen reasons; OMPDart attacks the orthogonal, inter-kernel data-movement axis of the same programming model. Neither cites the other, but together they show the two independent ways OpenMP offload loses performance.
- **Complementary to the memory-virtualisation cluster** (`GPU-MICRO24-01` SUV, `GPU-ICS25-01` DREAM, `GPU-ASPLOS24-01` GMLake): those move data automatically at the *system* level; OMPDart eliminates the moves at the *source* level. SUV in particular (static-analysis-guided UVM) is the closest neighbour in the corpus — static analysis serving device data placement — and the pair is worth a targeted comparison in any synthesis.
- **Prior tools the paper names** [paper]: Mishra et al. (2020) data-mapping tool limited to same-function kernels; **OpenMP Advisor** (Mishra et al. 2023, ML-based directive prediction); Guo et al. (2023) compile-time unused-array-segment filtering, whose techniques OMPDart extends; **OMPSan** (2019, static correctness verification of map clauses); **OmpMemOpt** (2020, lazy code motion for redundancy elimination). **Cited venue set as reported: ISPASS, Euro-Par, IEEE VLSI transactions** — plus foundational computability references. Again a non-architecture citation base.
- `NO_EXISTING_ANALYSIS`. Not an AI/HPC-import candidate.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO — but this is the closest call in the cluster, and the counter-argument is recorded rather than suppressed.**

**Stack level of the contribution**: **C/C++ → framework (OpenMP target offload)**, realised as a Clang/LLVM source-to-source pass. It never descends to CUDA, PTX or the kernel.

verdict_basis: The contribution's *output artefact* is the host/device data-movement program — `map(to:)`, `map(from:)`, `map(alloc:)`, `update to()`, `update from()` and a synthesised `target data` residency scope. The analysis state is "variable validity in **each memory space**" [paper]. Both the problem and the solution are constituted by **the host/device runtime split and the discrete device memory space** — the property the cluster brief names explicitly as an admissible basis for `NO`. On a CPU there is one address space, so the analysis computes nothing and the emitted clauses have no meaning; the paper's entire measured quantity (1.2×–1010× reductions in transferred bytes) ceases to exist.

**The counter-argument, stated honestly**: nothing in OMPDart is specific to a *GPU* as opposed to any discrete-memory accelerator — no warp, no shared memory, no occupancy, no PTX, no kernel-internal reasoning at all (12.9 is `NOT_IN_PAPER` throughout). An FPGA or DSP offload target would exercise the same analysis unchanged, and a unified-memory device would nullify it. A reviewer applying the strictest possible reading could land on `RELATED_GPU`.

**Why `CORE_GPU` is nonetheless the recorded verdict, and how it stays consistent with this cluster's `RELATED_GPU` calls**: the line drawn throughout this ledger is *where the contribution's own artefact sits relative to the GPU boundary*. MCFuser (SC 2024) was recorded `RELATED_GPU` because it hands every GPU-boundary decision — coalescing, vectorisation, tensor-core scheduling, shared-memory management, PTX emission — to Triton, and its own output is a generic loop schedule. OMPDart's own output **is** the device data-movement code; there is no lower layer to which the GPU-specific part has been delegated.

verdict: `CORE_GPU` (boundary; recorded with the counter-argument above)

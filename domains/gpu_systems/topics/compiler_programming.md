# GPU compilers, programming models, IR and lowering, kernel fusion, and language-level memory models and safety (taxonomy H/I)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD, with the sharpest counterfactual test in the corpus.**
Seven deep analyses (the cluster's `141–147` ID band). Verdict ledger:
`../corpus/_LEDGER_compiler_programming.md`.
Scope: compilers, programming models, JIT, IR and lowering, kernel fusion and
code generation (`H`/`I`), plus the language-level memory-model and
memory-safety tooling that belongs with them.

> Ledger defect to know about before using it: **every data row in
> `../corpus/_LEDGER_compiler_programming.md`'s three verdict tables has nine
> cells against a ten-cell header — the `Verdict` column is absent from the
> rows.** Verdicts for that cluster must therefore be taken from the
> full-paper gate (a deep-analysis file implies `CORE_GPU` on read full text)
> or from a sibling ledger, not read off the table. Recorded here so no reader
> silently mis-parses it.

## 1. Problem landscape

A compiler can be GPU-*targeted* without being GPU-*specific*, and this topic
exists at that boundary. `../corpus/_LEDGER_compiler_programming.md` applies
the strict form of the counterfactual for exactly this reason: **a retargetable
tensor compiler that happens to emit PTX is `RELATED_GPU`, not `CORE_GPU`.**
What survives the test is work whose contribution names a GPU-specific
property — an MMA fragment layout, a scope lattice, distributed shared memory,
warp-granular value regularity, the host/device data-movement boundary, or a
device-side allocation that a kernel issues while running.

The ledger records **where in the stack** each contribution lives, which is the
topic's real organising axis: `source language` → `framework` → `C/C++` →
`CUDA/HIP/Triton` → `kernel` → `PTX/ISA` → `library/runtime`.

## 2. Key concepts

Tile-level abstraction and the layout algebra that names an MMA operand map;
sub-byte and non-power-of-two data widths; software pipelining as something a
primitive set either can or cannot express; kernel fusion across the
*inter-core* boundary (Hopper thread-block clusters and distributed shared
memory); scoped memory consistency (CTA / GPU / system) and `.cat`-style
axiomatic models; capabilities and spatial memory safety under SIMT;
performance portability and the P∥ metric; OpenMP `target data` regions,
`map` clauses and RAW dependence across the host/device boundary; device-side
dynamic allocation from inside a running kernel.

## 3. Main mechanism families

**Family H1 — replace the tile language.**
`../corpus/GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md`
concludes Triton's abstraction is the obstacle for low-precision work and
supplies a layout monoid over `local`/`spatial` instead.

**Family H2 — formalise what the hardware promises.**
`../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md`
gives one framework for PTX and Vulkan consistency and verifies with SMT.

**Family H3 — make the language enforce safety in silicon.**
`../corpus/GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md`.

**Family I1 — fuse across a boundary that only just became fusable.**
`../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md`
searches for fusions that use Hopper distributed shared memory.

**Family H4 — measure what a programming model actually reaches.**
`../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md`.

**Family H5 — supply a runtime primitive the language assumes exists.**
`../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md`
(device-side `malloc` issued from inside a kernel).

**Family H6 — generate the data-movement program statically.**
`../corpus/GPU-SC24-147--ompdart-static-generation-openmp-offload-data-mappings.md`.

## 4. Representative papers

- **Tilus** (ASPLOS 2026) — **MEASURED** (A100 / H100 / L40 class). Decomposed
  rather than headlined: removal of a shared-memory layout conversion for
  sub-byte weights via `Reinterpret` on a raw-byte load; expressibility of
  software pipelining that Ladder's primitive set **cannot express** — so part
  of the gap against Ladder is not a better schedule but *the existence* of a
  schedule; direct emission of the MMA fragment layout; and **native
  non-power-of-two widths (3/5/6/7), which are coverage, not speedup** — Ladder
  is restricted to power-of-two widths and Tilus's own paper calls those widths
  "an open problem" `[paper]`. Against **Marlin**, a hand-written expert
  kernel, the margin is **1.03×** — i.e. **generality at hand-written
  performance, not a large win** `[paper]`. The IR at commit `4597cd5` contains
  `ClusterSyncThreadsInst`, `CopyAsyncBulkGlobalToClusterSharedInst` and
  `MapSharedAddrInst` `[code]`.
- **Towards Unified Analysis of GPU Consistency** (ASPLOS 2024) —
  **NO GPU IS EXECUTED.** The verification host is stated plainly: "Ubuntu
  22.04.4 LTS … 11th Gen Intel Core i5-1135G7 … 16 GB of RAM" `[paper]`. That
  does not weaken the `CORE_GPU` verdict — every added `.cat` construct is
  GPU-only (CTA/GPU/system scopes) — and it is a fact the corpus states rather
  than hides. Results: Dartagnan's running time "grows **linearly** w.r.t. the
  number of threads" where the Alloy tools "exhibited **exponential** growth",
  *on the paper's litmus suites, on that host* `[paper, Figure 15]`; coverage
  **106 PTX v6.0 tests and 110 Vulkan tests** versus "roughly one-third" for
  the Alloy tools `[paper, Table 5]`. Bound to **model versions, not silicon
  generations** — PTX v6.0 and v7.5; `UNKNOWN` beyond v7.5.
- **CHERI-SIMT** (ASPLOS 2026) — **FPGA PROTOTYPE, not a commercial GPU**:
  SIMTight on Stratix-10, 14 NoCL kernels, CHERI-Clang, with `[code]`
  `github.com/CTSRD-CHERI/SIMTight` @ `6248c9b727d1f32280997492ecb0179d045eb674`.
  **1.6% geomean execution-time overhead** `[paper]`. The enabler is
  **warp-granular value regularity**: capability *metadata* is uniform across
  32 lanes while addresses are not, so metadata scalarises into the scalar
  register file; bounds queries/sets are **<1% of dynamic instructions**, so
  one lane-shared bounds unit costs almost nothing; the null-value optimisation
  drives **13 of 14 kernels to zero vector-register-file metadata usage**
  `[paper, Figure 10]`. **On a CPU, CHERI already costs a plain 2× with no
  scalarisation to recover** — that contrast is the counterfactual.
- **FlashFuser** (HPCA 2026) — **MEASURED** (A100 / H100). Ablation against a
  no-fusion baseline: **Dataflow Analyzer only 1.52×** → **`dsm_comm` +
  Dataflow Analyzer at a random configuration 2.11×** → **full system 3.29×**
  `[paper]`. Performs an **all-reduce inside a single GPU's thread-block
  cluster**, so the collective vocabulary now appears at two scales.
- **Taking GPU Programming Models to Task** (ICS 2025) — **MEASURED** across
  five systems (NVIDIA and AMD; A100/H100/MI250X-class, Frontier and Aurora
  among them). P∥ across five applications: **SYCL 0.91 (BabelStream dot) –
  0.97 (su3_bench)**; **RAJA 0.67 (miniBUDE) – 0.99 (XSBench)**; **Kokkos 0.80
  (CloverLeaf) – 0.99 (XSBench)** `[paper]`. Its conclusion — "line-level stall
  attribution is a crucial capability missing from Omniperf" — is precisely the
  capability that `../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md`
  later builds; **this is the strongest cross-corpus link the cluster produced
  and it rests on the papers' own text, not on topical inference.**
- **Gallatin** (PPoPP 2024) — **MEASURED**, all on an **NVIDIA A40, 48 GB**:
  "up to **374×** faster on single-sized allocations", "up to **264×** on
  mixed-size", "up to **254×** faster than the next-best allocator as thread
  count increases" (to 2²⁰ threads); on **Orkut** (3.07 M vertices, 234.37 M
  edges) **1.5×** for bulk insertions and **3×** for graph expansion `[paper]`.
  The van Emde Boas node is shrunk to **64 bits**, abandoning its O(log log n)
  asymptotics for a single-word atomic — a GPU-shaped trade.
- **OMPDart** (SC 2024) — **MEASURED** on an **A100**, nine Rodinia/HeCBench
  applications. Geometric mean **2.8× over the default implicit data-mapping
  rules** and **1.05× over expert-defined mappings**, per-benchmark **1.01×–16×**
  over unoptimised `[paper]`. Residency hoisting is the dominant effect;
  bounds-narrowed `update`s are what let it **beat** experts on LULESH rather
  than merely match them. Preprint arXiv 2406.13881; artifact
  `zenodo.org/records/12562040` `[official-web]`.

## 5. Historical lineage

The citation bases this cluster read are its most transferable finding, and
they are the evidence behind the cross-venue map's traffic claim
(`../synthesis/GPU_CROSS_VENUE_MAP.md`). Recorded per paper, **with venues as
each paper itself reports them**:

- **FlashFuser (HPCA 2026)** names Halide (PLDI), TVM (OSDI'18), Ansor
  (OSDI'20), AStitch (ASPLOS 2022), BOLT (MLSys'22), TASO (SOSP'19), Chimera
  (HPCA 2023), **MCFuser (SC'24)**, T10 (SOSP 2024), WaferLLM and
  ClusterFusion (arXiv) `[paper]`. An HPCA paper importing from SC, OSDI and
  SOSP.
- **GPU Consistency (ASPLOS 2024)** names Alglave et al., Lustig et al.,
  Wickerson et al., Donaldson et al. — **"venues of those cited works, as the
  paper reports them: PLDI, POPL, CAV, TACAS"**, i.e. a
  programming-languages/formal-methods base, **not an architecture base**
  `[paper]`.
- **Gallatin (PPoPP 2024)** reports a cited venue set of **IPDPS, PPoPP, ICS,
  VLDB, SIGMOD, HPEC** — parallel computing **plus data management**, with
  **no ISCA/MICRO/HPCA presence at all** `[paper]`.
- **Taking GPU Programming Models to Task (ICS 2025)** reports **P3HPC
  workshop, SC workshops, IPDPS, CCGrid** — "essentially no ISCA/MICRO/HPCA
  presence" `[paper]`.
- **OMPDart (SC 2024)** reports **ISPASS, Euro-Par, IEEE VLSI transactions** —
  "again a non-architecture citation base" `[paper]`.
- **CHERI-SIMT (ASPLOS 2026)** names GPUShield, Futhark ("6% average
  performance overhead due to bounds checking on GPUs"), SkePU, Descend and
  Rust-CUDA, and **explicitly does not cite cuCatch or compute-sanitizer**
  `[paper, as read]`.

Wider chains: `../synthesis/GPU_TOPIC_LINEAGES.md`.

## 6. Implementation families

`REAL_SILICON` with public artifacts: Tilus (pinned commit), FlashFuser,
Gallatin, OMPDart (Zenodo artifact), the ICS 2025 portability study.
`FPGA_PROTOTYPE` on an open-source SIMT core: CHERI-SIMT (pinned commit).
`CPU_HOST_VERIFICATION_ONLY`: the GPU-consistency paper. Note that GitHub was
reachable from Bash in this pass even where the publisher was not, so several
`CLOSED_ACCESS` rows in this cluster nonetheless carry inspected `[code]`.

## 7. Important disagreements / tensions

**T1 — where the tile abstraction should sit is an open 2025–26 argument
between two papers in the same corpus.** Insum
(`../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md`)
pushes sparsity into index tensors and **reuses TorchInductor/Triton largely
unchanged**; Tilus concludes **Triton's abstraction is the obstacle and
replaces the language**. Read together they are the clearest statement in this
corpus of that argument, and neither resolves it.

**T2 — Tilus and FlashFuser are the two halves of one 2026 development and
neither cites the other.** Tilus provides the *language* in which a
cluster-scoped, TMA-driven kernel could be written by hand; FlashFuser provides
the *search* that decides what such a kernel should be `[paper, both §12.14]`.

**T3 — two independent ways OpenMP offload loses performance, discovered
separately.** The ICS 2025 study finds OpenMP offload scoring worst on the
compute-bound kernel for **intra-kernel code-generation** reasons; OMPDart
attacks the orthogonal **inter-kernel data-movement** axis of the same model.
**Neither cites the other.**

**T4 — OMPDart's target disappears under unified memory.**
`../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md`
is the setting in which OMPDart's optimisation has nothing to optimise. The
two bracket the OpenMP-offload data-movement question from both sides of the
unified-memory transition — a tension between a *compiler* result and a
*hardware* result, not between two compilers.

**T5 — GPU correctness splits into two halves that barely meet.** CHERI-SIMT
(static-by-construction spatial safety, in hardware) and the GPU-consistency
work (what values may be read) versus the dynamic concurrency tools
`../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md` and
`../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md`. The
consistency paper is a *dependency* of the dynamic tools, not merely adjacent:
a tool that advises weakening a scope (ScopeAdvice) is only sound with respect
to a model of the kind formalised there. Whether either dynamic tool is sound
against that model is not established in this corpus.

**T6 — a ledger defect, recorded rather than smoothed.** See the note under the
header: this cluster's tables omit the `Verdict` column from every data row.
Downstream counts that read verdicts off the table will undercount this
cluster; `../synthesis/GPU_CROSS_VENUE_MAP.md` handles it explicitly.

## 8. Current limitations

**Bounded by full-text access, and by one un-imported corpus.**
- `dl.acm.org` → 403 (including its "open PDF" paths), `ieeexplore.ieee.org`
  → 418, `dblp.org` and `par.nsf.gov` robots-blocked. **Four priority papers
  did not clear the full-paper gate and are watchlisted** rather than analysed
  — the gate is explicit: *abstract-only or artifact-only ⇒ verdict allowed,
  deep analysis NOT allowed*. Among them **Triton-Sanitizer** (ASPLOS 2026),
  whose census-recorded "open publisher PDF" returns 403 here, and whose
  mechanism was recovered only from a verbatim abstract plus `[code]`
  `triton-viz` @ `203b0c7cbb35448d53f3cf5359db55e0d4fb3522`. **This is an
  access-path limitation, not a statement about licence**
  (`../synthesis/GPU_PENDING_FULLTEXT.md`).
- **`../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`** — an ~80-paper
  AI/HPC corpus outside this repository, explicitly stated to include "GPU
  compiler/kernel" work. **A large fraction of this topic plausibly belongs to
  it**, every deep-learning-facing compiler/fusion paper is flagged
  `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`, and **nothing is asserted** about
  duplication. Absence from this repository is not evidence of novelty
  (`../../../governance/ANTI_HALLUCINATION_RULES.md`;
  `../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).
- **MCFuser (SC 2024)** is cited by FlashFuser as a verified SC→HPCA citation
  link but has **no corpus file** — it is a verdict-only row. A cross-reference
  to `GPU-SC24-145` appearing in one analysis is **not a corpus file** and
  should not be followed.
- JIT compilation is essentially absent: **Proteus** turned out to be **CGO
  2025, not ISC 2026**, and CGO is outside this project's venue set, so it is
  `EXCLUDE` (out of population) rather than analysed.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. T1 has no experiment. Is there a workload on which "sparsity in the index
   tensor, dense compiler unchanged" and "replace the tile language" can be
   measured against each other?
2. Does CHERI-SIMT's warp-granular metadata-uniformity argument hold on a
   commercial SIMT core with a real scalar register file, or is the 1.6%
   an artefact of SIMTight's proportions? The corpus has one FPGA data point.
3. T4: which OpenMP-offload compiler results in this corpus survive on an APU?

## 10. Deeper lookup paths

`../corpus/_LEDGER_compiler_programming.md` — the three verdict tables (with
the missing-verdict-column caveat above), the four gate failures, and the
**eight census corrections** this cluster produced (DOIs, preprint IDs, a
changed arXiv title for Tilus, author affiliations) → the seven analyses above
→ the pinned artifacts in each §12.8.
Cross-topic: `tensor_cores.md` (what Tilus's layout algebra exists to name),
`sparse_irregular.md` (Gallatin's unused-general-solution finding, and Insum),
`profiling_debugging.md` (the ICS 2025 → SC 2026 tooling-gap link, and the
dynamic half of T5), `runtime_scheduling.md` (CUDASTF's task-graph row).

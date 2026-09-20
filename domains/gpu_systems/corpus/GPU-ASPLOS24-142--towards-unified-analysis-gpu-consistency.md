# GPU-ASPLOS24-142 — Towards Unified Analysis of GPU Consistency

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — GPU memory consistency models and correctness tooling at the language/ISA level`
secondary_topics: `formal verification (bounded model checking, SMT); PTX and Vulkan/SPIR-V semantics; scoped synchronization; liveness of spin loops; GPU programming-model correctness`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the first author-group PDF (https://hernanponcedeleon.github.io/pdfs/asplos2024.pdf), read in three passes — (a) title/authors/affiliations/venue, motivation, the critique of Alloy-based prototypes; (b) the .cat extensions (new base relations Table 1, new event tags Table 2, morally-strong definition Figure 4, the PTX and Vulkan axioms), the front-ends and program representation, the liveness/spinloop encoding and its forward-progress assumption, the SMT encoding and relation-bounding static analysis (Tables 3 and 4); (c) evaluation — test suites and counts, host machine, Alloy and GPUVerify comparisons, Table 5 supported-test counts, Figure 15 scaling, the two discovered model bugs, limitations/future work, related work. Mirror https://researchportal.helsinki.fi/files/646149224/Towards.pdf NOT fetched (the author PDF sufficed).`

## 12.1 Bibliographic facts

- Title: **Towards Unified Analysis of GPU Consistency** [paper].
- Venue: **ASPLOS '24** — "29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS '24), April 27–May 1, 2024, La Jolla, CA, USA" [paper, title block].
- DOI: `10.1145/3622781.3674174`, volume **29V4** [census: `domains/gpu_systems/census/ASPLOS_2024.md`]. **Recorded oddity, carried from the census**: 29V4 is a *deferred* volume — the census notes this paper is not on the 2024 program page and was presented at ASPLOS 2025. Its proceedings year is 2024; that is the year used for the stable ID.
- Authors and affiliations [paper]: **Haining Tong** (University of Helsinki, Finland), **Natalia Gavrilenko** (Huawei Dresden Research Center, Germany), **Hernán Ponce de León** (Huawei Dresden Research Center, Germany), **Keijo Heljanko** (University of Helsinki and Helsinki Institute for Information Technology, Finland).
- Artifact: the census records `NOT_FOUND_AFTER_SEARCH` for a repository. The work is delivered as an extension to the **Dartagnan** verifier [paper]; no repository URL was read in the fetched PDF, and none is asserted. `NOT_INSPECTED`.
- Publication type: `ARCHIVAL_MAIN_PAPER`.

## 12.2 Core question (one sentence)

Can the two industrially-deployed GPU memory consistency models — NVIDIA's **PTX** (v6.0 and v7.5) and Khronos's **Vulkan** — be expressed in one axiomatic framework (the `.cat` language) extended with the GPU-specific notions that CPU models never needed (scopes, proxies, storage classes, availability/visibility), and then analysed by a single bounded-model-checking tool that scales to real programs and can also decide **liveness**, rather than by per-model Alloy prototypes?

## 12.3 GPU/HPC problem translation

- **Synchronization.** This is the whole paper. The object of study is the GPU's *scoped* synchronization: PTX defines **three scopes — CTA, GPU, SYS**; Vulkan defines **four — Subgroup, Workgroup, Queue family, Device** [paper]. Correctness of a fence or an atomic depends on whether two operations are "in scope" of one another, a relation with no CPU analogue.
- **Memory.** Vulkan's model additionally requires **availability and visibility** chains (event tags `AV`, `VIS`, `SEMAV`, `SEMVIS` [paper, Table 2]) — i.e. the model exposes the cache hierarchy's write-back/invalidate semantics in the *language* memory model. PTX exposes **proxies** (`GEN`, `TEX`, `SUR`, `CON` [paper, Table 2]) — separate access paths to the same memory through different hardware units.
- **Compute / scheduling.** Enters only through the **forward-progress** assumption needed for liveness: the paper observes "Computations are split into sub-tasks and then assigned to workgroups. Not all workgroups might execute concurrently" [paper].
- **Communication.** Inter-thread, intra-device; no multi-GPU or network layer. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (root cause)

- **The hardware root cause of scopes** is that a GPU's coherence is not uniform: threads in a CTA share an L1/scratchpad, threads across the device share L2, and the system scope reaches the host. Making the *cheapest sufficient* fence expressible requires the memory model to name those levels — hence CTA/GPU/SYS and Subgroup/Workgroup/Queue-family/Device.
- **The root cause of proxies** is that the same address can be reached through the generic path, the texture unit, the surface unit or the constant path, and those paths are not automatically coherent — so the model must forbid reasoning about two accesses as if they were ordered when they use different proxies. The paper's formal condition makes this explicit: two operations are morally-strong only if "(ms2) they are in the same proxy" [paper, Figure 4, lines 9–12].
- **The root cause of the tooling gap** is stated directly: existing Alloy-based prototypes "lack support for real GPU programming APIs, cannot handle control flow instructions, do not verify liveness properties, and exhibit poor scalability" [paper], and "The first models were written in .cat. However, those only covered basic features of GPUs and their tool support has been discontinued" [paper]. So the research gap is *not* that the models were unknown — they were published — but that nothing could execute them on real code.
- The paper's own framing of the human cost: "interpreting them still requires a level of expertise that escapes most developers, and the current tool support is insufficient" [paper].

## 12.5 Mathematical / formal model

This paper's "performance model" is an axiomatic semantics; it is recorded as such.

- **Framework**: the `.cat` domain-specific language for axiomatic consistency models, "enhance[d] … with new GPU specific features" [paper].
- **New base relations** [paper, Table 1]: `sr` ("Events within the same scope"), `scta` (CTA scope), `ssg` / `swg` / `sqf` (subgroup / workgroup / queue-family scopes), `vloc` ("same virtual address"), `syncbar` ("matching barrier IDs"). For PTX specifically, `sync_barrier` (defined as "a partial order") and `sync_fence` ("morally strong SC fences").
- **New event tags** [paper, Table 2]: memory ordering `ACQ`, `REL`, `RLX`; scope `SG`, `WG`, `QF`, `DV`; PTX proxies `GEN`, `SUR`, `TEX`, `CON`; Vulkan storage classes `SC0`, `SC1`; cache-control `AV`, `VIS`, `SEMAV`, `SEMVIS`.
- **Morally-strong (PTX v7.5)** [paper, Figure 4, lines 9–12], verbatim structure: two operations are morally strong iff
  - `(ms1)` "they are in program order or each operation is strong", **and**
  - `(ms2)` "they are in the same proxy", **and**
  - `(ms3)` "if both are memory operations, then they overlap completely".
- **PTX coherence axiom** [paper]: `empty ((([W]; cause; [W]) & loc) \ co)` — coherence expressed through the `cause` relation rather than a primitive happens-before.
- **Vulkan consistency axiom** [paper]: `acyclic (locord | rf | fr | asmo)`, with a **non-transitive** happens-before that "requir[es] availability-visibility chains" [paper].
- **Liveness / spinloop detection** [paper]: "For each thread, we start by detecting when a spinloop reads from the maximal event in coherence order, and the read value does not break the looping condition."
- **Progress assumption** [paper]: "a forward progress model where whenever a thread becomes enabled, it will eventually be scheduled", explicitly acknowledged to admit "false negatives about liveness violations".
- **Decision procedure**: bounded model checking with an SMT encoding; relation bounds are narrowed by static analysis — "alias analysis can identify pairs that do not access the same location in any execution, allowing us to remove these pairs from the upper bounds of the `rf` and `co` relations" [paper]. `sr`'s bound "contain[s] all non-mutually exclusive events where the scopes of the instructions match", using predicates `visibleFrom` and `mayAlias` [paper, Table 3].
- **Encoding of ordering** [paper, Table 4]: for `sync_fence`, "we introduce a clock variable for each fence event and enforce the ordering of those clock variables"; **`co` is a partial order enforced by clock variables in PTX but a total order in Vulkan** — a concrete, model-level asymmetry between the two vendors' specifications.

## 12.6 Data layout and ownership (hierarchy)

The hierarchy here is a *scope lattice*, not a data layout, and the two vendors' lattices do not align — which is precisely what the unification has to absorb:

| Level | PTX name [paper] | Vulkan name [paper] |
|---|---|---|
| sub-warp / warp | — | **Subgroup** (`ssg`, tag `SG`) |
| thread block | **CTA** (`scta`) | **Workgroup** (`swg`, tag `WG`) |
| device | **GPU** | **Device** (tag `DV`) |
| queue / system | **SYS** | **Queue family** (`sqf`, tag `QF`) |

- PTX has **no subgroup/warp scope** in this table; Vulkan has **no direct SYS analogue** but a queue-family level. The generic relation `sr` ("events within the same scope") is the construct that lets one `.cat` file range over either lattice [paper].
- Vulkan additionally layers **storage classes** `SC0`/`SC1` [paper, Table 2] — an orthogonal axis to scope.
- PTX layers **proxies** orthogonally instead [paper, Table 2].
- Address identity is itself a GPU concern here: `vloc` ("same virtual address") is a *separate* relation from ordinary same-location [paper].

## 12.7 Pseudo code

```
# --- litmus program representation [paper] ---
# first line of each thread column places the thread in the GPU hierarchy,
# "e.g., which workgroup the thread belongs to"
#   instructions used: ld, st, cbar (control barrier), bne, goto

T0 @ (workgroup=0)        T1 @ (workgroup=1)
  st  x, 1                  ld  r1, y
  cbar 0                    bne r1, 0, spin
  st  y, 1                  ld  r2, x

# --- the analysis pipeline [paper] ---
front_end  in { PTX pseudo-asm, Vulkan pseudo-asm, real SPIR-V subset }
           # OpenCL kernels reachable via clspv -> SPIR-V
model      := cat_file            # Ptx v6.0 | Ptx v7.5 | Vulkan
bounds     := static_analysis(program)      # alias analysis narrows rf, co;
                                            # scope match narrows sr
formula    := smt_encode(program, model, bounds)
             # sync_fence: a clock variable per fence event, ordered
             # co: partial order (Ptx) / total order (Vulkan)
result     := smt_solve(formula)            # safety, and liveness via spinloops
```

All construct names above are as printed in the paper. `[reconstruction]` applies only to the illustrative litmus body, not to the instruction names or the pipeline.

## 12.8 Real implementation

- The models are "translated and integrated … into the **Dartagnan** verification tool" [paper]. Dartagnan is a pre-existing bounded model checker; the contribution is the GPU extension, not the checker.
- **Three new front-ends** were added [paper, verbatim]: "two for the pseudo-assembly-like syntax … one for Ptx and one for Vulkan, and one for a subset of real **Spir-V** assembly." The tool "accepts disassembled SPIR-V and can compile OpenCL kernels via **clspv**" [paper].
- **No repository was located and none is asserted.** `NOT_INSPECTED` — no source symbols are claimed below or above. (Contrast `GPU-ASPLOS26-141`, where `[code]` evidence was available.)

## 12.9 Kernel execution

Not a performance paper; the relevant execution structure is the *model's* view of execution.

- **thread**: the unit carrying program order; each thread declares its position in the hierarchy on its first litmus line [paper].
- **warp / subgroup**: a first-class scope in **Vulkan only** (`ssg`, `SG`) [paper]. Its absence from PTX's scope set is a real modelling asymmetry.
- **thread block / CTA / workgroup**: `scta` / `swg` [paper]; also where `cbar` (control barrier) and `syncbar` ("matching barrier IDs") act.
- **barrier divergence** is explicitly **not** supported [paper, limitations] — i.e. the tool assumes barriers are reached uniformly, which is itself a GPU-specific hazard left unmodelled.
- **instruction**: `ld`, `st`, `cbar`, `bne`, `goto` in the pseudo-assembly [paper].

## 12.10 Memory traffic

No measured memory traffic — this is a verification paper. What it does expose is that **Vulkan's model makes cache traffic semantically visible**: availability (`AV`, `SEMAV`) and visibility (`VIS`, `SEMVIS`) tags, and a happens-before that is non-transitive without an availability–visibility chain [paper]. PTX instead hides the caches and exposes **proxies** (`GEN`, `TEX`, `SUR`, `CON`) — separate hardware access paths. These are two different decisions about how much of the memory hierarchy a language model should expose, and the paper's unification has to carry both.

## 12.11 Why it is faster/slower (decomposed cause)

The performance claim is about the *verifier*, and the cause is decomposed as follows:

1. **SMT + relation bounding instead of Alloy's relational enumeration.** Dartagnan "encodes program semantics as satisfiability modulo theories (SMT) formulas and employs static analysis techniques to compute relation bounds, dramatically reducing formula size" [paper].
2. **Alias analysis prunes `rf` and `co` upper bounds** [paper] — the single named source of formula compaction.
3. **Scope-match pruning of `sr`** [paper, Table 3] — a GPU-specific pruning opportunity that has no CPU counterpart.
4. **Consequence, measured**: "the running time of Dartagnan only grows linearly w.r.t. the number of threads", whereas the Alloy tools "exhibited exponential growth" [paper, Figure 15]. Restated with its qualifier: *linear vs exponential in thread count, on the paper's litmus suites, on an 11th-Gen Intel Core i5-1135G7 host*.
5. **Coverage, measured**: Table 5 — Dartagnan supports **106 PTX v6.0 tests and 110 Vulkan tests**, versus "roughly one-third" for the Alloy tools [paper].

## 12.12 Hardware generation dependence

- The work is bound to **model versions**, not silicon generations: **PTX v6.0 and PTX v7.5** [paper], and the Khronos Vulkan memory model.
- The distinction matters: PTX v7.5 introduced the morally-strong formulation the paper formalises, so the analysis is version-specific in a way that will need revision as PTX evolves. The paper does not claim coverage of later PTX versions; `UNKNOWN` beyond v7.5.
- No dependence on a particular NVIDIA architecture generation is claimed, and none should be inferred — the model is an ISA-level contract, not a microarchitecture.
- **Verification host** [paper]: "Ubuntu 22.04.4 LTS machine equipped with an 11th Gen Intel(R) Core(TM) i5-1135G7 processor (2.40 GHz, 8 cores) and 16 GB of RAM." **No GPU is used in the evaluation** — a fact that must be stated plainly and does not weaken the GPU verdict (see the counterfactual record).

## 12.13 Limitations

Stated by the paper:

- **Progress model.** The forward-progress assumption yields "false negatives about liveness violations" [paper]; real GPUs give no such guarantee across workgroups — "Not all workgroups might execute concurrently" [paper].
- **Scopes are absent from the liveness encoding.** "The lack of consideration for scopes in the liveness encoding is more problematic. In its current form, a spinloop reading-from a co-maximal event which is not in scope is considered a bug" [paper] — i.e. liveness can report a false positive for exactly the scoped case the rest of the paper is about. The stated plan is to move the liveness definition into the `.cat` model itself.
- **Unsupported features** [paper]: floating-point variables; **barrier divergence**; dynamic references in GPU code; exchange operations in spinloops ("requires extending the underlying theory of liveness").
- **Litmus-test generation** for GPU-specific features is future work [paper] — so coverage of the models is bounded by hand-written and ported suites.
- **Bounded** model checking: results are relative to the unrolling bound. (Implicit in BMC; the paper states BMC is the technique [paper].)

## 12.14 Relation to prior corpus

- **Complementary, at the specification layer, to the two dynamic race/synchronization tools already in the corpus**: `GPU-SC24-41` (HiRace, GPU data-race checking) and `GPU-MICRO24-41` (Over-Synchronization in GPU Programs / ScopeAdvice). Those two *observe* executions; this paper *defines what an execution is allowed to do*. In particular, a tool that advises weakening a scope (ScopeAdvice) is only sound with respect to a model of the kind formalised here — the pairing is a genuine dependency, not a thematic one.
- **Complementary to `GPU-ASPLOS26-141` (Tilus)** only in the abstract sense that both live at the language/ISA boundary; no shared mechanism.
- **Precursor relationship claimed by the paper itself**: earlier `.cat` GPU models whose "tool support has been discontinued", and the Alloy-based PTX v7.5 and Vulkan tools it compares against [paper]. Named prior lines: Alglave et al. (weak consistency, litmus testing), Lustig et al. (formal PTX), Wickerson et al. (GPU concurrency), Donaldson et al. (GPU verification, incl. GPUVerify as a compared baseline) [paper]. **Venues of those cited works, as the paper reports them: PLDI, POPL, CAV, TACAS** — i.e. the citation base of this ASPLOS paper is a *programming-languages/formal-methods* base, not an architecture base.
- `NO_EXISTING_ANALYSIS` in `domains/gpu_systems/corpus/`. Not a plausible member of the pending `domains/ai_hpc_systems/` AI/HPC import (no ML content).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: **PTX/ISA**, reached from `CUDA/HIP/Triton` and from SPIR-V/OpenCL. Specifically: the ISA-level memory-model contract, plus the front-ends that accept PTX and SPIR-V assembly. Not a library, not a compiler pass.

verdict_basis: Every construct the paper adds to `.cat` exists because GPUs have them and CPUs do not — **scopes** (PTX CTA/GPU/SYS; Vulkan Subgroup/Workgroup/Queue-family/Device, relations `sr`, `scta`, `ssg`, `swg`, `sqf`), **proxies** (`GEN`, `TEX`, `SUR`, `CON`, and the morally-strong condition `(ms2)` that two operations must be in the same proxy), **storage classes** (`SC0`, `SC1`), and **availability/visibility** (`AV`, `VIS`, `SEMAV`, `SEMVIS`) with a non-transitive happens-before [paper]. The formalised objects *are* the CUDA/Vulkan scoped memory model. That the model checker itself runs on an Intel CPU is irrelevant to the test: the artefact under analysis, and the entire novelty, is the GPU's consistency specification. A CPU memory model carries none of these axes, so the contribution would not merely be weaker — it would be empty.

verdict: `CORE_GPU`

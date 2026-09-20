# GPU-ASPLOS26-141 — Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (also `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — a low-precision LLM-serving kernel compiler is exactly the kind of item `domains/ai_hpc_systems/` is said to hold; nothing is asserted about whether it is duplicated there)
primary_topic: `H — GPU compilers, programming models, IR and lowering`
secondary_topics: `I — kernel fusion / code generation; F — Tensor Cores and low-precision numeric formats; quantized LLM serving; register/shared-memory layout algebra`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (https://arxiv.org/html/2504.12984v1), read in three passes — (a) title/authors/affiliations, introduction and motivation, the critique of Triton and Ladder; (b) language design: SIMB programming model, the three variable classes, the layout algebra and its two primitives, the thread-block-level instruction set, the arbitrary-bit-width type family; (c) compilation pipeline to Hidet IR and nvcc, runtime/binary management, evaluation setup (GPU SKUs, driver, CUDA, baseline versions), headline speedups, protocol, and scope limitations. PLUS [code] inspection of https://github.com/NVIDIA/tilus at commit 4597cd5ba3f24501ba411cefa61a76fd9d3ba2c8. A dedicated numbered ablation section was NOT located in the fetched HTML — recorded NOT_IN_PAPER rather than reconstructed.`

## 12.1 Bibliographic facts

- Venue title (official, ASPLOS 2026): **Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation** [census: `domains/gpu_systems/census/ASPLOS_2026.md`, row 8, session `5A: Generative Model Serving`, volume 31V1].
- **Title discrepancy, recorded not resolved**: the arXiv preprint 2504.12984 is titled **"A Virtual Machine for Arbitrary Low-Precision GPGPU Computation in LLM Serving"** [paper, arXiv HTML v1]. The ASPLOS camera-ready was retitled. Both refer to the same system, which the preprint itself names **Tilus**. Treat the preprint as `PREPRINT` evidence for an `ARCHIVAL_MAIN_PAPER`.
- DOI: `10.1145/3760250.3762219` [census; `dl.acm.org` is 403 from this environment, so the DOI was not dereferenced].
- Authors and affiliations [paper, arXiv HTML v1]: **Yaoyao Ding** (University of Toronto; CentML Inc.; Vector Institute), **Bohan Hou** (Carnegie Mellon University), **Xiao Zhang** (University of Toronto), **Allan Lin** (University of Waterloo), **Tianqi Chen** (Carnegie Mellon University), **Cody Yu Hao** (Anyscale), **Yida Wang** (Amazon), **Gennady Pekhimenko** (University of Toronto).
- Artifact: **https://github.com/NVIDIA/tilus** — inspected at commit `4597cd5ba3f24501ba411cefa61a76fd9d3ba2c8` [code]. Zenodo artifact `https://zenodo.org/records/16756860` recorded by the census, **NOT_INSPECTED**.
- Publication type: `ARCHIVAL_MAIN_PAPER` (+ `PREPRINT` arXiv 2504.12984).

## 12.2 Core question (one sentence)

Can a GPU kernel language whose *unit of programming is the thread block* rather than the thread — with registers, shared memory and global memory as explicit, separately-typed tensor scopes, and with element-to-thread placement expressed as a composable layout algebra — generate competitive matrix-multiply kernels for **arbitrary** integer/float bit widths from 1 to 8, including the hardware-unfriendly widths 3, 5, 6 and 7 that neither Triton nor power-of-two-restricted Ladder can express?

## 12.3 GPU/HPC problem translation

- **Compute.** Quantized LLM GEMM is a *dequantize-then-MMA* pipeline. The MMA instruction consumes a fixed register fragment of a standard type (fp16/bf16/int8), so every non-standard weight type must be unpacked into that fragment. The paper's compute problem is that when the bit width is not a power of two, the unpack is not a shift-and-mask on an aligned lane — the element boundaries straddle machine words.
- **Memory.** The dominant cost in decode-stage quantized GEMM is streaming the quantized weight from global memory; the language's purpose is to let the programmer load that weight **as raw bytes** and reinterpret it in place, rather than materialising a widened copy. The paper states Triton "does not expose the GPU memory hierarchy, limiting programmers' control over data loading" [paper].
- **Synchronization.** The SIMB model makes the thread block the semantic unit, so intra-block synchronization is implicit at instruction boundaries rather than being written by the programmer; software pipelining (which Ladder's primitives "cannot express" [paper]) is the construct that requires explicit async-copy/barrier control.
- **Scheduling.** Layout choice *is* the scheduling decision: a layout fixes which thread owns which element, hence which MMA fragment shape and which shared-memory access pattern arise.
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- The Tensor Core `mma` instruction imposes a **fixed register-fragment layout**: a specific (thread, local-index) → (row, col) map per instruction shape and type. The paper's Figure 3 layout is given as `local(2, 1).spatial(8, 4).local(1, 2)` [paper] — i.e. the hardware's fragment map is exactly an element of the paper's layout monoid. This is the root cause of the whole design: the language's central type-level object is the shape of a hardware instruction's operand.
- The second root cause is the **byte-addressed register/shared-memory word**. A 5-bit or 6-bit element does not tile a 32-bit register lane; loading it as its declared type would force a shared-memory staging pass with a layout conversion. Tilus's answer is `Reinterpret`, "zero-cost conversion between compatible tensor types maintaining same bit distribution" [paper]: load as `uint8`, reinterpret to the true low-precision type, and only then `Cast`.
- Triton's abstraction boundary is the cause of its failure here: Triton exposes tiles but not *scopes*, so the programmer cannot say "this tile lives in registers with this thread map, that one lives in shared memory". The paper reports Triton "lacks native support for low precision data types like uint4" [paper].

## 12.5 Mathematical / performance model

- **Layout, definition** [paper]: a layout is "a function f that maps a thread index t and a local index i within that thread to the logical index f(t,i) of the corresponding tensor element."
- **Two primitives** [paper]:
  - `local(n1, n2)` — "stores all tile elements within single threads" (elements are *replicated in the local dimension*, i.e. one thread holds an n1×n2 block).
  - `spatial(n1, n2)` — "distributes elements across multiple threads, each holding one element."
- **Composition**: an operator (written `⊙` in the paper, `.` in the concrete syntax) under which layouts form a **monoid** — the paper states associativity with identity and proves the monoid property [paper]. `[code]` confirms this is `RegisterLayout.__mul__`, which dispatches to `tilus.ir.layout.ops.register_ops.compose` at commit `4597cd5`.
- **Worked instance** [paper]: `local(2, 1).spatial(8, 4).local(1, 2)` denotes the tensor-core instruction operand layout of Figure 3.
- **Type family** [paper]: "signed integers, unsigned integers, and floating-point numbers with 1 to 8 bits" — concretely `int2`–`int8`, `uint1`–`uint8`, and configurable `float3`–`float8`.
- **No closed-form cost model is presented.** The paper does not give an analytical performance model; scheduling is expressed, not predicted. Recorded `NOT_IN_PAPER`.
- **System size** [paper]: "around 20K lines of Python and C++ code."

## 12.6 Data layout and ownership

- **thread**: holds the `local(...)` modes of a register tensor. `[code]` `RegisterLayout` carries `shape`, `mode_shape`, `spatial_modes`, `local_modes` — the split between per-thread and across-thread ownership is literally two field tuples of the layout dataclass (`python/tilus/ir/layout/register_layout.py`, commit `4597cd5`).
- **warp**: the `spatial(...)` modes whose extent divides 32 land within a warp; the paper's Figure-3 example `spatial(8, 4)` is 32 threads, i.e. exactly one warp, because that is the MMA fragment's thread count [paper + inference on the arithmetic].
- **thread block (the SIMB unit)**: the whole semantic unit of a Tilus instruction. The paper names the model **"Single-Instruction-Multiple-Block (SIMB)"**, "operating at the granularity of entire thread blocks rather than individual threads" [paper].
- **memory scopes as types**: a *tensor variable* carries "shape, element type, memory scope, and layout" [paper]. `[code]` confirms three distinct layout classes exist as separate modules — `register_layout.py`, `shared_layout.py`, `global_layout.py`, plus `tmem_layout.py` for Blackwell tensor memory (commit `4597cd5`).
- **cluster**: not in the paper's description, but `[code]` at commit `4597cd5` contains `ClusterSyncThreadsInst`, `CopyAsyncBulkGlobalToClusterSharedInst`, `MapSharedAddrInst` — i.e. the open-source system has since grown Hopper distributed-shared-memory support. **This is `[code]` evidence about the repository, not `[paper]` evidence about the ASPLOS paper.**
- **GPU**: L40S (48 GiB) primary; A100 and H100 for cross-platform validation [paper].
- **node/cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- the thread-block-level instruction set named in the paper ---   [paper]
LoadGlobal / StoreGlobal      # global <-> register or shared
Reinterpret                   # zero-cost retype, same bit distribution
Cast                          # value-converting retype
Mma                           # tensor-core matrix-multiply-accumulate

# --- the low-precision weight path the paper describes ---           [paper]
w_bytes = LoadGlobal(Wq, dtype=uint8, layout=<packed>)  # raw bytes, no widening
w_lp    = Reinterpret(w_bytes, dtype=uint5)             # free: same bits
w_f16   = Cast(w_lp, dtype=float16)                     # the only real work
acc     = Mma(a_f16, w_f16, acc)                        # fragment layout fixed by ISA

# --- layout construction ---                                         [paper]
frag = local(2, 1) . spatial(8, 4) . local(1, 2)   # == Figure 3 tensor-core layout
```

Names above are as printed in the paper. Their concrete repository spellings differ — see 12.8.

## 12.8 Real implementation

Repository `https://github.com/NVIDIA/tilus`, commit **`4597cd5ba3f24501ba411cefa61a76fd9d3ba2c8`** [code]. Verified symbols only:

- **Layout algebra**: `python/tilus/ir/layout/ops/register_ops.py` defines `spatial(*shape, ranks=None)`, `local(*shape, ranks=None)`, `column_spatial(*shape)`, `column_local(*shape)`. `RegisterLayout` (`register_layout.py`) is a frozen dataclass with fields `shape`, `mode_shape`, `spatial_modes`, `local_modes`, and `__mul__` → `compose`.
- **Pass pipeline**, `python/tilus/transforms/__init__.py`, in the order listed there: `declare_to_let_pass`, `let_propagation_pass`, `lower_assume_pass`, `lower_param_only_expr_pass`, `analyze_scalar_pass`, `lower_print_tmemory_tensor_pass`, **`layout_inference_pass`**, **`lower_load_store_pass`**, **`layout_inference_pass`** (run a second time), `bound_aware_simplify_pass`, `analyze_scalar_pass`, `dead_code_elimination_pass`.
  - The fact that `layout_inference_pass` runs **twice, straddling `lower_load_store_pass`**, is the most informative single detail in the pipeline: lowering a load/store introduces new register tensors whose layouts are not yet constrained, so inference must be re-run. [code]
- **Generic instruction set**, `python/tilus/ir/instructions/generic.py`: `AllocateRegisterInst`, `LoadGlobalInst`, `StoreGlobalInst`, `LoadSharedInst`, `StoreSharedInst`, `StoreSharedScatterInst`, `StoreGlobalScatterInst`, `SliceRegisterInst`, `CastInst`, `ElementwiseUnaryInst`, `ElementwiseBinaryInst`, `WhereInst`, `ReduceInst`, `ScanInst`, `ShuffleDownInst`, `ShuffleUpInst`, `ViewInst`, `SqueezeInst`, `UnsqueezeInst`, `PrintTensorInst`.
- **CUDA-specific instructions**, `python/tilus/ir/instructions/cuda/`: `DotInst` (`mma_dot.py`), `SimtDotInst` (`simt_dot.py`), `CopyAsyncInst` / `CopyAsyncCommitGroupInst` / `CopyAsyncWaitGroupInst` (`cp_async.py`), `CopyAsyncBulkGlobalToSharedInst` / `...GlobalToClusterSharedInst` / `...SharedToGlobalInst` (`cp_async_bulk.py`), `CopyAsyncTensorGlobalToSharedInst` / `CopyAsyncTensorSharedToGlobalInst` (`cp_async_tensor.py` — the TMA path), `AllocBarrierInst` / `ArriveBarrierInst` / `ArriveExpectTxBarrierInst` / `WaitBarrierInst` (`mbarrier.py`), `Tcgen05AllocInst` / `Tcgen05LoadInst` / `Tcgen05StoreInst` / `Tcgen05SliceInst` / `Tcgen05ViewInst` (`tcgen05.py`), `AtomicSharedInst` / `AtomicGlobalInst`, `LockSemaphoreInst` / `ReleaseSemaphoreInst`, `ClusterLaunchControlTryCancelInst` (`clc.py`), `MapSharedAddrInst` (`mapa.py`).
  - The instruction set is a **one-to-one surface for named PTX asynchronous-copy and tensor-core facilities** (`cp.async`, `cp.async.bulk`, `cp.async.bulk.tensor`/TMA, `mbarrier`, `tcgen05`). This is the strongest single piece of evidence for the counterfactual answer below. [code]
- **Layout inference machinery**: `python/tilus/ir/layout/inference/` with `inference_rules/` and `validation_rules/` subtrees, including an `inference_rules/tcgen05/` directory. [code]
- **Hidet vendoring**: `python/tilus/hidet/` — the Hidet IR, its `transforms/`, `backend/`, `ir/primitives/cuda/` and `drivers/` are vendored inside the Tilus tree, matching the paper's statement that Tilus lowers to "Hidet IR, … a CUDA C-like intermediate representation" and then emits "CUDA C code from Hidet IR … compiled into a hardware binary using the nvcc compiler" [paper + code].
- **Runtime**: `python/tilus/runtime/compiled_program.py` — corresponds to the paper's "runtime system manages dynamically loaded binaries and provides the execution environment" [paper + code].

`NOT_INSPECTED`: the Zenodo artifact; the benchmark scripts; any Blackwell results.

## 12.9 Kernel execution

- **kernel**: one Tilus function compiles to one CUDA kernel; the paper gives no persistent-kernel or megakernel structure. `NOT_IN_PAPER` beyond that.
- **thread block**: the SIMB unit. Every Tilus instruction is a *thread-block-collective* operation; the compiler, not the programmer, decides the per-thread expansion via the layout attached to each tensor [paper].
- **warp**: appears only through layouts whose `spatial` extent is 32 (the MMA fragment) and through `ShuffleDownInst`/`ShuffleUpInst` [code], which are warp-shuffle primitives. The paper does not make the warp a named language object — this is a real design difference from CUDA and is worth recording precisely: **Tilus's semantic unit is the block, and the warp survives only inside layouts**.
- **instruction**: `DotInst` (tensor-core MMA) vs `SimtDotInst` (non-tensor-core FMA path) are separate IR nodes [code], i.e. the choice of using the tensor core is an explicit IR-level fact, not a backend heuristic.

## 12.10 Memory traffic

- **global → register, bypassing a widening step.** The paper's central traffic claim is that the quantized weight is read at its packed width and reinterpreted in registers, "eliminating the shared-memory layout conversions required by Triton" [paper]. So the saved traffic is a **shared-memory round trip**, not a global-memory one: the bytes read from HBM are the same either way; what Tilus removes is store-to-shared + load-from-shared + the layout shuffle between them.
- **register ↔ shared**: explicit via `LoadSharedInst`/`StoreSharedInst` and the scatter variants [code].
- **global → shared asynchronously**: `cp.async` and TMA are first-class instructions [code], which is what makes software pipelining expressible — the specific capability the paper says Ladder's primitives lack [paper].
- **L1/L2/HBM**: the paper presents no cache-level traffic decomposition. `NOT_IN_PAPER`.
- **multi-GPU**: none. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Decomposed, not attributed to the headline number:

1. **Removal of a shared-memory layout conversion** for sub-byte weights, via `Reinterpret` on a raw-byte load [paper]. This is the mechanism the paper itself names against Triton.
2. **Expressibility of software pipelining**, which Ladder's primitive set cannot express [paper]. Against Ladder, therefore, part of the gap is not a better schedule but *the existence* of a schedule.
3. **Direct emission of the MMA fragment layout.** Because the layout algebra can name the instruction's own operand map, no reshape/transpose of register fragments is needed to feed `Mma`.
4. **Native non-power-of-two widths.** Against Ladder, which is "restricted to data types with bit widths that are powers of two" [paper], widths 3/5/6/7 are not a speedup at all — they are coverage. The paper frames this as "an open problem" for those widths [paper].
5. Against **Marlin** the reported margin is **1.03×** [paper] — i.e. essentially parity with a hand-written expert kernel. The honest reading is that Tilus's claim is *generality at hand-written performance*, not a large win over the best specialised kernel.

## 12.12 Hardware generation dependence

- Evaluated on **L40S (Ada), A100 (Ampere), H100 (Hopper)** [paper]; primary numbers are L40S with driver 565.57.01 and CUDA 12.6.3 [paper].
- The *design* is bound to NVIDIA specifically: the layout algebra exists to name `mma` fragment maps, and the lowering target is Hidet IR → CUDA C → **nvcc** [paper]. There is no AMD/HIP path described.
- `[code]` at commit `4597cd5` shows generation-specific instruction families that postdate or extend the paper: `tcgen05*` (Blackwell tensor memory) and cluster/TMA instructions (Hopper). The presence of `tmem_layout.py` and `inference_rules/tcgen05/` means the layout algebra was extensible to a *new memory scope* introduced by a new GPU generation — a genuine architectural claim, and it is `[code]` evidence only.

## 12.13 Limitations

- **Scope**: the evaluation is quantized matrix multiplication only; the paper states the framework supports other operations "in principle" but does not evaluate them [paper].
- **Vendor lock**: NVIDIA/nvcc only, as above.
- **No cost model / no autotuner described.** The paper explicitly enables autotuning for the *baselines* ("Auto-tuning for Triton and Ladder was enabled" [paper]) but does not describe Tilus's own tuning mechanism. Whether Tilus's reported numbers come from hand-chosen or searched schedules is **UNKNOWN** from the fetched text.
- **No dedicated ablation section was located** in the fetched HTML. `NOT_IN_PAPER` — not reconstructed.
- **Single-GPU only.**
- The margin over the best hand-written baseline (Marlin, 1.03× [paper, L40S]) is small enough that the practical claim rests on coverage rather than peak speed.

## 12.14 Relation to prior corpus

- **Complementary to `GPU-ASPLOS26-101` (Insum).** Both are "push the format/precision into a type-level object so a dense compiler can still emit the MMA" designs, but from opposite ends: Insum pushes *sparsity* into index tensors and reuses TorchInductor/Triton unchanged-ish; Tilus concludes Triton's abstraction is the obstacle and replaces the language. Read together they are the clearest statement in this corpus of the 2025–26 argument about *where* the tile abstraction should sit.
- **Complementary to the tensor-core cluster** (`GPU-PPoPP26-02` CuBie, `GPU-SC26-01` Ozaki II, `GPU-SC26-02` EmuGEMM): those characterise or emulate precision on the matrix unit; Tilus is the language layer that would express them.
- **Competing with** Triton and Ladder/BitBLAS as named in the paper [paper]; neither has a corpus file.
- **No existing duplicate** in `domains/gpu_systems/corpus/`.
- `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and is stated to include GPU compiler/kernel work; **no claim is made** about whether Tilus appears there.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: **source language → kernel**, i.e. a new tier *between* the framework and CUDA/Triton, lowering through Hidet IR to CUDA C and thence PTX via nvcc. It is not a framework-level graph compiler and not a PTX-level tool.

verdict_basis: The language's central semantic object — the layout monoid over `local`/`spatial` — exists to *name the register-fragment map that a tensor-core `mma` instruction imposes*, and the paper's own worked example (`local(2,1).spatial(8,4).local(1,2)`) is a hardware fragment layout [paper]. The programming model's unit is the CUDA thread block ("SIMB"), and the instruction set surfaces `cp.async`, `cp.async.bulk.tensor` (TMA), `mbarrier` and `tcgen05` one-to-one [code, commit `4597cd5`]. Shared memory is a first-class, separately-typed scope whose elimination for the weight path is the stated performance mechanism. On a CPU or a generic accelerator without a fixed-fragment matrix instruction, an explicit scratchpad and a warp-granular thread map, there is nothing left for the layout algebra to denote. This is **not** a retargetable tensor compiler that happens to emit PTX; the abstraction is co-designed with one ISA's operand layouts.

verdict: `CORE_GPU`

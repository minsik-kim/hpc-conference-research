# GPU-ASPLOS26-143 — CHERI-SIMT: Implementing Capability Memory Protection in GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — GPU programming-model / toolchain-level memory safety (compiler + ISA + SIMT microarchitecture co-design)`
secondary_topics: `GPU memory safety and correctness tooling; register-file scalarisation; SIMT datapath microarchitecture; RISC-V CHERI ISA extension; FPGA soft-GPU prototyping`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the authors' Cambridge PDF (https://www.cl.cam.ac.uk/~tmj32/papers/docs/naylor26-asplos.pdf), read in two passes — (a) title/authors/affiliation/venue, introduction and threat motivation, the prior-work dismissal of CHERI for GPUs, the register-file design (dual register files, SRF/VRF compression, shared VRF, null-value optimisation), CHERI Concentrate bounds, the 33-instruction ISA extension, fast-path vs shared-function-unit split, PCC/Active-Thread-Selection restriction, compiler/toolchain changes, memory-subsystem and tag handling; (b) evaluation — FPGA board and SIMTight configuration, clock, the 14 NoCL kernels, CHERI-Clang, area/ALM numbers, register-file storage overheads, 1.6% execution-time overhead, the Rust comparison, Figure 10 null-value-optimisation effect, limitations, related work. PLUS [code] inspection of https://github.com/CTSRD-CHERI/SIMTight @ 6248c9b727d1f32280997492ecb0179d045eb674.`

## 12.1 Bibliographic facts

- Title: **CHERI-SIMT: Implementing Capability Memory Protection in GPUs** [paper, title line].
  - **Title discrepancy, recorded**: the ASPLOS 2026 program page renders the subtitle "…in GPGPUs"; the ACM record and the authors' own PDF say "…in GPUs" [census: `domains/gpu_systems/census/ASPLOS_2026.md`]. Publisher form taken as official; the authors' PDF agrees.
- Venue: **ASPLOS '26**, "31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems, March 22–26, 2026, Pittsburgh, PA, USA" [paper]. Volume **31V1**; DOI `10.1145/3760250.3762234` [census]. `dl.acm.org` is 403 here, so the DOI was not dereferenced.
- Authors, all **University of Cambridge, Cambridge, United Kingdom** [paper]: **Matthew Naylor, Alexandre Joannou, A. Theodore Markettos, Paul Metzger, Simon W. Moore, Timothy M. Jones**.
- Repository inspected: **https://github.com/CTSRD-CHERI/SIMTight** at commit **`6248c9b727d1f32280997492ecb0179d045eb674`** [code]. The census flags this as "the same group's SIMT platform; **not stated as the paper's artifact**" — that caveat is carried here, and every `[code]` claim below is a claim about the repository at that commit, **not** an assertion that it is the paper's artifact.
- Publication type: `ARCHIVAL_MAIN_PAPER`.

## 12.2 Core question (one sentence)

Can CHERI capability memory protection — which doubles pointer width and was therefore dismissed as unaffordable for GPUs because it would "double the already-large register-file cost" [paper] — be made cheap in a SIMT machine by exploiting the fact that *capability metadata is far more uniform across a warp's lanes than the addresses are*, so that the new metadata register file compresses away almost entirely?

## 12.3 GPU/HPC problem translation

- **Memory.** The problem is spatial memory safety of GPU pointers. The paper's motivating evidence: prior work documents "buffer overflows in a set of 175 GPU applications", and such exploits lead to "data corruption on the stack and heap, control-flow hijacking, code injection, and arbitrary code execution" [paper].
- **Compute / datapath.** The cost centre is the **register file**, which on a GPU is the largest on-chip SRAM structure. Doubling register width for 64-bit capabilities plus a tag bit is the thing that must be avoided.
- **Synchronization.** Not the subject. `NOT_IN_PAPER` beyond tag-controller atomicity (below).
- **Scheduling.** Enters at one specific point: **Active Thread Selection** must compare per-thread PCs; extending PCs to 65-bit PCCs would put capability metadata in the scheduler's critical comparison. The paper's "static PC metadata restriction" makes PC metadata invariant per kernel so the scheduler need not check it [paper].
- **Communication.** Single SM; no inter-GPU aspect. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- **Root cause of the cost**: a CHERI capability is a 64-bit value plus a 1-bit validity tag, against a 32-bit baseline register. On a machine with a 2,048-entry register file per SM replicated across 32 lanes, that is a direct doubling of the dominant SRAM.
- **Root cause of the opportunity — and this is the paper's entire insight**: SIMT threads execute in lockstep over *structured* data. The paper names it "**value regularity in SIMT workloads**": lanes' capability **metadata** (bounds, permissions, object type) is typically identical across a warp even when the **addresses** differ, because all lanes are indexing into the *same* buffer. So the metadata vector is uniform, or affine (base+stride), exactly when the address vector is not.
- **Root cause of the null-value problem**: most registers do not hold pointers at all. When a register holds an integer or float, its metadata is a constant null. A warp that mixes pointer and non-pointer lanes would break naive uniformity detection — hence the **null-value optimisation (NVO)**, "a bitmask allowing partially uniform vectors to remain compressed despite null overwrites" [paper].
- **Root cause of the slow-path split**: bounds *manipulation* (`CGetBase`, `CGetLen`, `CSetBounds`) needs a decoder for the compressed bounds format, which is expensive per lane. The paper measures these at **"<1% frequency"** [paper, Figure 6], which is what licenses moving them to a shared unit.

## 12.5 Mathematical / performance model

No closed-form analytical model; the paper is an area/overhead measurement. The quantities it reports, each restated with its qualifier:

- **Bounds encoding**: "CHERI Concentrate" — "a 32-bit lower bound and 33-bit upper bound encoded in 15 bits in floating-point-like format" [paper].
- **Register width**: 32 bits → **65 bits** (64-bit capability + 1 tag bit) [paper].
- **Register-file storage, baseline scalarisation**: "55% storage reduction" with a 3/8-size VRF [paper, SIMTight baseline].
- **Register-file storage, CHERI**: capability metadata costs "14% of the total register-file storage"; "7% overhead" forecast with compiler support; "below 3.5%" estimated for a full GPU [paper]. The last two are **projections, not measurements** — recorded as such.
- **Logic area (Stratix-10 ALMs, one SIMTight SM)** [paper]: baseline **126,753**; CHERI unoptimised **166,796** (+40,043); CHERI optimised **149,356** (+22,603), a **"44%"** reduction of the overhead. Per-lane cost **"708 ALMs per vector lane, comparable to … an additional multiplier (567 ALMs)"**.
- **Clock**: 180 MHz baseline → **181 MHz** with CHERI [paper] — i.e. no frequency penalty on this FPGA.
- **Execution time**: **"1.6% on average"** (geometric mean) over the 14 NoCL kernels on the DE10-Pro Stratix-10 SIMTight SM [paper]. Memory-access overhead **"2.2%"** in the 3/8-VRF configuration [paper].
- **Software-safety comparison** [paper]: Rust software bounds checking **34%** overhead; total Rust overhead **46%** — on the same platform/benchmarks. This is the number that carries the paper's argument.

## 12.6 Data layout and ownership

- **thread / lane**: each lane holds a 65-bit capability (64-bit value + tag) when uncompressed. The fast-path capability operations — **`setAddr`, `isAccessInBounds`, `fromMem`, `toMem`** — are "implemented per vector lane using **CheriCapLib** functions" [paper]. `[code]` confirms `CHERI.CapLib` is imported by `src/Core/SIMT.hs` at commit `6248c9b` — the paper's `CheriCapLib` and the repository's `CHERI.CapLib` are the same library.
- **warp**: the unit over which metadata uniformity is detected. "Both compressed register files detect uniform metadata vectors at runtime using comparators; uniform/affine metadata compresses to base+stride pairs in the **SRF**; non-compressible vectors allocate in a constrained **VRF**" [paper]. `[code]`: `inc/Config.h` at commit `6248c9b` carries `SIMTEnableRegFileScalarisation`, `SIMTEnableAffineScalarisation`, `SIMTEnableCapRegFileScalarisation`, `SIMTRegFilePreventScalarDetection` — i.e. scalarisation of the *ordinary* register file and of the *capability* register file are independently configurable knobs in the hardware description.
- **register files, two of them**: "A 32-bit general-purpose register file (unchanged) plus a new **33-bit 'capability-metadata register file'** storing only metadata, separate from addresses" [paper]. `[code]`: `SIMTRegFileSize 2048` and `SIMTCapRegFileSize 2048` are separate configuration constants at commit `6248c9b`, confirming two distinct files.
- **shared VRF**: "general-purpose and metadata register files share a single VRF to eliminate fragmentation, accepting serialized (one-cycle stall) access when both uncompressed data and metadata are needed" [paper].
- **SM**: one SIMTight SM, **"64 warps per SM and 32 threads per warp providing 2,048 threads per SM"** [paper]. `[code]` `inc/Config.h` at `6248c9b`: `SIMTLanes 32`, `SIMTWarps 64` — exact agreement.
- **scratchpad**: "On-chip scratchpad banks extended from 32 to **33 bits** to store capability tag bits" [paper]. `[code]`: `SIMTSRAMBanks 16` at `6248c9b`.
- **off-chip**: "Tag bits (1 per 64-bit value): stored in reserved off-chip region; tag controller provides atomic access illusion" [paper]. `[code]`: `EnableTaggedMem` is a `Config.h` setting documented as "Needed for CHERI" at `6248c9b`.
- **GPU / node / cluster**: single SM only — see 12.13.

## 12.7 Pseudo code

```
# --- the split that makes CHERI affordable in SIMT ---            [paper]
# per-lane FAST PATH (frequent, from CheriCapLib):
    setAddr(cap, addr)
    isAccessInBounds(cap, addr, width)
    fromMem(word_pair) / toMem(cap)

# SHARED-FUNCTION UNIT slow path (<1% dynamic frequency, Figure 6):
    CGetBase(cap)  CGetLen(cap)  CSetBounds(cap, len)
    # requests from the 32 lanes are serialised through one unit

# --- metadata register file write, conceptually ---               [paper]
write_cap_meta(warp, reg, meta_vector):
    if all_equal(meta_vector) or is_affine(meta_vector):
        SRF[warp][reg] = (base, stride)          # compressed
    else if NVO and non_null_lanes_uniform(meta_vector):
        SRF[warp][reg] = (uniform_meta, null_mask)   # still compressed
    else:
        VRF.allocate(warp, reg) = meta_vector    # the expensive case
```

`[reconstruction]` applies to the code shape only. The instruction and function names (`setAddr`, `isAccessInBounds`, `fromMem`, `toMem`, `CGetBase`, `CGetLen`, `CSetBounds`, `CIncOffset`, `CSetAddr`, `CLC`, `CSC`) are printed in the paper.

## 12.8 Real implementation

- **Base platform**: **SIMTight**, a RISC-V SIMT soft-GPU [paper], repository `https://github.com/CTSRD-CHERI/SIMTight` @ `6248c9b727d1f32280997492ecb0179d045eb674` [code]. Verified at that commit:
  - `src/Core/SIMT.hs` (497 lines) imports `Pebbles.Instructions.RV32_IxCHERI`, `Pebbles.Memory.CapSerDes`, `CHERI.CapLib`.
  - It carries a `simtCoreEnableCHERI :: Bool` configuration field, an `enCHERI` parameter on `makeSIMTExecuteStage`, and **two distinct execute functions selected by that flag**: `executeIxCHERIWithSharedBoundsUnit` and `executeIxCHERI`. The first is gated on `SIMTUseSharedBoundsUnit == 1`. **This is the fast-path / shared-function-unit split of the paper, present verbatim in the hardware description.**
  - `makeCapMemReqSerialiser` and `CapMemReq` / `toCapMemReq` implement the paper's "64-bit capability accesses … as two inseparable 32-bit 'multi-flit' accesses".
  - `inc/Config.h` knobs: `EnableCHERI`, `EnableTaggedMem` ("Needed for CHERI"), `SIMTEnableCapRegFileScalarisation`, `SIMTCapRegFileSize 2048`, `SIMTUseSharedBoundsUnit`, `SIMTEnableRegFileScalarisation`, `SIMTEnableAffineScalarisation`, `SIMTRegFilePreventScalarDetection`, `SIMTLanes 32`, `SIMTWarps 64`, `SIMTSRAMBanks 16`, and `UseClang` ("Currently required if CHERI enabled").
  - `apps/Samples/` contains `VecAdd`, `Histogram`, `Reduce`, `Scan`, `Transpose`, `MatVecMul`, `MatMul`, `BitonicSortSmall`, `BitonicSortLarge`, `SparseMatVecMul` — the same benchmark names the paper evaluates.
  - `rust/` and `cheri-tools/` directories exist, consistent with the paper's Rust comparison and CHERI toolchain.
  - **`pebbles/` is an empty directory at this clone** (a git submodule not fetched with `--depth 1`); the Pebbles library's contents are therefore `NOT_INSPECTED`.
- **ISA**: "Extends RISC-V `rv32ima_zfinx` with **33 CHERI instructions** (Figure 4), including capability arithmetic (`CIncOffset`, `CSetAddr`), bounds manipulation (`CSetBounds`), and load/store operations (`CLC`, `CSC`)" [paper].
- **Compiler/toolchain** [paper]: benchmarks "recompiled with **CHERI-LLVM (Clang 13 fork)** without source modification", `-O2`. Three toolchain-level facts, each significant:
  1. The compiler "disabled **scalar evolution of pointers**" — unsupported in CHERI-RISC-V. This is a real optimisation lost.
  2. "Aggressive function **inlining of `kernel()` methods**" reduces overhead from double-sized stack-pointer accesses.
  3. Only the **NoCL library**, not the benchmarks, was modified, to set stack and allocation bounds; "compiler automatically lowers C/C++ pointers to capabilities".

## 12.9 Kernel execution

- **kernel → warp → lane** is the structure the whole design rides on. The compression decision is made **per warp, per register**, by runtime comparators over the 32 lanes' metadata [paper].
- **Active Thread Selection**: the warp scheduler's PC comparison. Because PCC metadata is made "invariant per kernel" by the **static PC metadata restriction**, the scheduler compares only addresses, "avoiding per-thread bounds checks" [paper]. This is the cleanest example in the paper of a security mechanism being shaped by a *scheduler's* critical path.
- **instruction**: 33 added CHERI instructions; capability memory accesses take **2 cycles** (multi-flit) [paper].
- **divergence**: `SIMTLogMaxNestLevel 5` at `[code]` commit `6248c9b` indicates a nesting-depth-bounded reconvergence stack; the paper does not connect divergence to the capability design. `NOT_IN_PAPER`.

## 12.10 Memory traffic

- **register ↔ SRF/VRF**: the design's whole point is that most capability metadata never reaches the VRF at all. "With the null-value optimisation, only the **BlkStencil** benchmark uses space in the VRF for capability metadata" [paper, Figure 10] — a strikingly strong result: for 13 of 14 kernels, metadata is entirely scalar.
- **scratchpad**: banks widened 32→33 bits for tags [paper].
- **off-chip / DRAM**: capability loads/stores are 2×32-bit multi-flit accesses; tag bits live in a reserved off-chip region behind a tag controller [paper]. Measured DRAM bandwidth impact: "minimal" [paper]; memory-access overhead 2.2% in the 3/8-VRF configuration [paper].
- **L1/L2 decomposition**: not reported. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

The overhead is 1.6% (geomean, 14 NoCL kernels, SIMTight on Stratix-10) [paper]; decomposed, the reasons it is *not* larger:

1. **Metadata uniformity.** Lanes share bounds because they index the same buffer; the SRF absorbs it. Without this the register file would double.
2. **Null-value optimisation.** Non-pointer registers have constant-null metadata; the bitmask keeps mixed vectors compressed, which is what drives 13/14 kernels to zero VRF metadata usage [paper, Figure 10].
3. **Frequency-based instruction placement.** Bounds queries/sets are <1% of dynamic instructions [paper, Figure 6], so serialising them across 32 lanes in one shared unit costs almost nothing while removing 32 copies of the bounds decoder.
4. **Scheduler exemption.** Static PC metadata keeps capability checks off the Active-Thread-Selection path [paper].
5. **Shared VRF** removes fragmentation between the two register files, at the price of a one-cycle stall only when both uncompressed data *and* uncompressed metadata are needed — a case the compression makes rare [paper].
6. **The cost that remains** is the 2-cycle multi-flit capability access and the doubled stack-pointer traffic, which the compiler mitigates by inlining `kernel()` [paper].

Against the software alternative: Rust's bounds checking costs **34%** on the same platform [paper] — the hardware approach is ~20× cheaper in time on this evidence, which is the paper's central comparative claim.

## 12.12 Hardware generation dependence

- **Not an NVIDIA/AMD result.** The evaluation is an **FPGA soft GPU**: "Terasic DE10-Pro development board with a Stratix-10 FPGA holding a single SIMTight SM" [paper], 180/181 MHz. Area is reported in Altera **ALMs**, not in a commercial process. Numbers are therefore not transferable to a shipping GPU without the paper's own projection ("below 3.5%" full-GPU register-file overhead [paper]) — which is explicitly an estimate.
- **ISA generation dependence** is on **RISC-V `rv32ima_zfinx` + CHERI**, not on a PTX or RDNA generation. The design would need re-derivation for a 64-bit-address commercial GPU: the paper's 32-bit base is what makes the 65-bit capability a 2× rather than 1.5× step.
- `[code]` at commit `6248c9b` shows CHERI as a build-time configuration of a single SoC, with `de10-pro` and `de10-pro-e` board directories — consistent with, and no broader than, the paper's claim.

## 12.13 Limitations

- **Single SM.** Stated by the paper: "The main limitation of SIMTight is that it currently supports only a single SM" [paper] — which directly bounds the memory-subsystem and tag-controller results, since inter-SM coherence of tags is untested.
- **FPGA, not silicon.** Area in ALMs and a 180 MHz clock; the full-GPU register-file figure is a projection.
- **A lost compiler optimisation**: scalar evolution of pointers is disabled under CHERI-RISC-V [paper].
- **Threat model is spatial only.** The conclusion notes "the much-broader threat model supported by CHERI would be interesting to explore in the context of GPUs" [paper] — i.e. temporal safety and compartmentalisation are future work, not delivered.
- **Benchmarks are 14 NoCL kernels**, a small in-house suite, not CUDA/HIP applications. Generalisation to real CUDA codebases is untested.
- **The 7% and 3.5% register-file figures require compiler support that does not yet exist** [paper].

## 12.14 Relation to prior corpus

- **Competing/adjacent, at a different layer, to `GPU-SC24-41` (HiRace) and `GPU-MICRO24-41` (Over-Synchronization/ScopeAdvice)**: those are dynamic *concurrency* correctness tools; this is static-by-construction *spatial memory* safety in hardware. Together they mark the two halves of GPU correctness tooling in this corpus.
- **Complementary to `GPU-ASPLOS24-142` (Towards Unified Analysis of GPU Consistency)**: consistency (what values may be read) vs capability (which addresses may be touched). Neither subsumes the other, and the pairing is the cleanest statement in this cluster of how much of GPU correctness is *not* about performance.
- **Precursors the paper itself names** [paper]: **GPUShield** (bounds table using the top 16 bits of a 64-bit pointer; "average execution-time overhead of 0.8%"; limitations — no dynamic allocation, no referential integrity); high-level safe languages **Futhark** ("6% average performance overhead due to bounds checking on GPUs") and **SkePU**; **Descend** ("safe low-level language for GPU programming" using views, "harder to write" than CUDA); **Rust-CUDA** ("early stages and does not yet present any performance analysis"). The paper explicitly does **not** cite cuCatch or compute-sanitizer [paper, as read].
- `NO_EXISTING_ANALYSIS`. Not a plausible member of the pending `domains/ai_hpc_systems/` import (no ML content).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: it spans **C/C++ → PTX/ISA → hardware**. Concretely: an unmodified C/C++ source level (compiler auto-lowers pointers to capabilities), a **CHERI-LLVM** compiler change, a **33-instruction RISC-V ISA extension**, and a **SIMT register-file and execute-stage microarchitecture**. The contribution's centre of gravity is the ISA/microarchitecture end, not the language end.

verdict_basis: The enabling insight is a property of the SIMT execution model itself — **capability metadata is uniform or affine across the 32 lanes of a warp because all lanes index the same buffer**, so the metadata register file scalarises into an SRF while the address vector stays in the VRF [paper; `[code]` `SIMTEnableCapRegFileScalarisation`, `SIMTEnableAffineScalarisation` at commit `6248c9b`]. Every quantitative claim in the paper is a claim about warp-granular value regularity, per-lane fast paths versus a **lane-shared** bounds unit used <1% of the time, and the **Active Thread Selection** warp scheduler's PC comparison. On a CPU, CHERI is already deployed and costs a straightforward 2× pointer width with no scalarisation opportunity — the entire contribution *is* the SIMT-specific recovery of that cost. On a generic accelerator without lockstep lanes over a shared register file, the compression has nothing to compress.

verdict: `CORE_GPU`

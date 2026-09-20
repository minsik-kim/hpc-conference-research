# GPU-ASPLOS25-01 — Virgo: Cluster-level Matrix Unit Integration in GPUs for Scalability and Energy Efficiency

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` in-repo; `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` for the un-imported AI/HPC corpus
primary_topic: `F — Tensor/Matrix cores (microarchitectural integration)`
secondary_topics: `GPU microarchitecture; shared-memory banking; energy efficiency; open-source RISC-V GPGPU`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the author-hosted (Berkeley) PDF — motivation, background on per-core Tensor Core integration, Virgo microarchitecture (disaggregated matrix unit, accumulator memory, 2D shared-memory banking, MMIO interface, async execution model), baseline RTL models (Volta/Ampere/Hopper-style), methodology (Chisel/Chipyard, 16nm synthesis, Joules, VCS), Table 2 configuration, evaluation (GEMM + FlashAttention-3), component power breakdown, area, related work. Future-work section: NOT_IN_PAPER. Plus [code] inspection of the artifact at a pinned commit.`

## 12.1 Bibliographic facts

- Title: **Virgo: Cluster-level Matrix Unit Integration in GPUs for Scalability and Energy Efficiency** [paper]
- Venue: **ASPLOS '25**, 30 March – 3 April 2025, Rotterdam, Netherlands [paper]; census session `30V2`
- DOI: `10.1145/3676641.3716281` [official-web]
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Authors and affiliations [paper]: Hansung Kim (UC Berkeley), Ruohan Richard Yan (UC Berkeley), Joshua You (UC Berkeley), Tieliang Vamber Yang (NVIDIA Corporation, Santa Clara, CA), Yakun Sophia Shao (UC Berkeley)
- Full texts: `https://people.eecs.berkeley.edu/~ysshao/assets/papers/virgo-asplos2025.pdf` [paper]; arXiv:2408.12073 [official-web]
- Artifact: `https://github.com/ucb-bar/virgo` — inspected. Pinned commit **`dd03a7c87895a937ecbde30daf8aeddb583ec144`** (`Thu Jun 12 12:56:25 2025 -0700`, "Update README.md") [code]. A companion kernel repository `https://github.com/ucb-bar/virgo-kernels` is named in the README [README] but was **not** cloned or read — `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Tensor Cores have always been integrated *inside* the SIMT core, with operands and accumulators anchored to the per-warp register file — is that coupling, rather than the matrix arithmetic itself, what caps tile size, occupancy and energy efficiency, and what happens if the matrix unit is moved out to the **core cluster (SM) level** with its own accumulator SRAM and a direct path to shared memory?

## 12.3 GPU/HPC problem translation

- **Compute.** With operands and accumulators register-file-resident, tile sizes stay small (the paper cites 8×8 and 16×16), so a large GEMM is expressed as a very large number of small MMA instructions. Virgo's cluster unit issues **one launch command per tile operation** for tiles up to **128×64×128**, with a hardware FSM walking the (i, j, k) loop nest [paper].
- **Memory.** The paper's core claim is that the register file is the wrong storage for matrix accumulators: it is multi-banked for divergent scatter/gather, whereas a matrix accumulator needs only "regular contiguous accesses" — so a dedicated **single-banked accumulator SRAM** is both simpler and lower-energy per access [paper].
- **Synchronization.** Moving the unit out of the core turns synchronous, warp-blocking MMA into **asynchronous** operation: a warp issues a matrix op and immediately proceeds to unrelated work (prefetching the next tile, computing an activation). Completion is polled. Cluster-wide barrier logic was added to Vortex for this [paper].
- **Scheduling.** The warp scheduler was modified for asynchronous matrix-unit commands, plus store fencing [paper].
- **Communication.** Intra-cluster only: a dedicated interconnect from cluster shared memory to the matrix unit, plus an optional DMA engine for global→shared/accumulator transfers without core involvement. No multi-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

The paper isolates two linked root causes [paper]:

1. **Register-file pressure.** "Contemporary GEMM kernels exhibit high register pressure as they require extensive use of register file space to store multiple input and accumulator data." The consequences named are "decreased kernel occupancy or frequent register spills to stack memory in Tensor Core-accelerated GEMM kernels". Because occupancy is what hides latency in *fused* kernels (attention, epilogues), this is not a GEMM-only cost.
2. **Instruction and address-generation energy.** Small tiles ⇒ many instructions ⇒ energy spent "in instruction scheduling and address generation, rather than in actual computation".
3. **Operand decoupling alone is insufficient.** The paper's sharpest architectural observation: even with Hopper-style operand decoupling (operands sourced from SMEM), "the Tensor Core still remains physically coupled to the SIMT core, preventing data sharing across matrix units", and per-core accumulators remain register-file-bound. So the *accumulator* side, not the operand side, is the residual bottleneck. This is the gap Virgo targets.

## 12.5 Mathematical / performance model

The paper does not present a closed-form analytic model; it is an RTL-measured microarchitecture study. The quantitative framework is:

- **Energy** = (total active power − idle baseline power) × RTL-measured cycle latency. The paper justifies subtracting idle power because "idle power is highly implementation-dependent" [paper].
- **MAC utilisation** = fraction of cycles the MAC array is active, extracted from cycle-accurate traces [paper].
- **Memory footprint** measured as shared-memory reads [paper].
- Reported derived quantity: **shared-memory data reuse improved 44%** for the unified cluster-level design versus the operand-decoupled (Hopper-style) design [paper].

## 12.6 Data layout and ownership

- **thread / lane**: 8 lanes per warp in the Vortex-based SIMT core [paper, Table 2]. Lanes issue narrow 4-byte shared-memory requests.
- **warp**: 8 warps per core [paper, Table 2]. A warp *launches* a matrix operation via an MMIO store and then runs ahead; it does **not** own matrix operands in its registers.
- **cluster (the new level)**: owns
  - the **matrix unit** (Gemmini-based systolic array, configured "16 × 16 FP16 / 8 × 8 FP32", operations up to 128×64×128) [paper];
  - the **accumulator memory**, a dedicated single-banked SRAM attached to the matrix unit, replacing register-file accumulators [paper];
  - **128 KB shared memory, 4 banks, 8–16 subbanks** [paper, Table 2], with a novel **two-dimensional banking** scheme (banks × subbanks) so that wide systolic-array accesses of `4n` bytes (n = 16) and narrow 4-byte SIMT lane requests can proceed concurrently. Unaligned SIMT accesses are "selectively filter[ed] out" and serialised to reduce crossbar complexity; **separate read and write paths** prevent producer–consumer conflicts (e.g. DMA filling while cores post-process) [paper].
  - an optional **DMA engine** copying tiles global→SMEM or global→accumulator memory without core involvement [paper].
- **Code corroboration of the banking** [code, `src/main/scala/radiance/tile/VirgoSharedMemComponents.scala`]: `val smemBanks = smemKey.numBanks`; `val smemSubbanks = smemWidth / wordSize`; the connection matrix is built over the tuple `(banks, subbanks, gemminis)` and separately `(banks, subbanks, tc client)`; alignment handling is explicit (`fAligned`, `filterRange`, `numLaneDupes = max(1, smemSubbanks / numLanes)`). The dedicated nodes `AlignFilterNode.scala` and `RWSplitterNode.scala` exist in `src/main/scala/radiance/memory/` — matching the paper's "selectively filter out unaligned accesses" and "separate read and write paths" [code].
- **SM/CU → GPU**: 1 cluster with 8 cores (Volta/Ampere baselines) or 4 cores (Hopper baseline); 16 KB L1 I-cache and 16 KB L1 D-cache per core; 512 KB shared L2 [paper, Table 2].
- **node / cluster (system)**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

Software view, using the paper's named MMIO operations:

```
# per warp, software pipelined  [paper]
virgo_dma_load(tile_next, global_ptr, addr_gen_params)   # async, no core involvement
virgo_compute(smem_tile_cur)                             # kick off MMA on cluster unit
... unrelated instructions: prefetch, activation, epilogue math ...
virgo_fence()                                            # poll completion
virgo_dma_store(global_ptr_out, accumulator_mem)
```

Hardware view:

```
# inside the cluster matrix unit  [paper]
on virgo_compute(tile):
    FSM iterates (i, j, k) over the tile dimensions up to 128 x 64 x 128
    operands streamed from cluster SMEM over the dedicated interconnect
    partial sums accumulate in the single-banked ACCUMULATOR MEMORY
    signal done -> visible via the busy register
```

`[code]` The RTL side of that interface is a **register map**, not new ISA: `src/main/scala/radiance/tile/GemminiTile.scala` defines
`0x00 -> Seq(RegField.w(32, gemminiCommandReg(_, _)))`, rs1 LSB/MSB at `0x08`, rs2 LSB/MSB at `0x10`, `0x20 -> Seq(RegField.r(32, gemminiBusyReg(_)))`, `0x28 -> Seq(RegField.r(32, gemminiRunningLoopsReg(_)))`. So a `virgo_compute` is a 32-bit store to offset 0 with operands staged in the rs1/rs2 registers, and `virgo_fence` is a read of the busy register. **The `virgo_*` names are the paper's software-level names [paper]; the register offsets and `RegField` symbols above are from the RTL [code]. The kernel repository that would contain the `virgo_*` macros was not inspected.**

## 12.8 Real implementation

Repository `https://github.com/ucb-bar/virgo`, pinned commit `dd03a7c87895a937ecbde30daf8aeddb583ec144` [code]. Verified structure — note the RTL namespace is `radiance`, not `virgo`:

- `src/main/scala/radiance/tile/RadianceCluster.scala` — top-level Virgo cluster definition [README, code]
- `src/main/scala/radiance/tile/RadianceSharedMem.scala`, `VirgoSharedMemComponents.scala` — shared memory + interconnect [code]
- `src/main/scala/radiance/tile/GemminiTile.scala` — Gemmini-based matrix unit and its **MMIO** register map (offsets quoted in §12.7) [code]
- `src/main/scala/radiance/tile/VortexCore.scala` — Chisel wrapper for the Vortex SIMT core [code]
- `src/main/scala/radiance/tile/Barrier.scala` — cluster-wide barrier synchroniser [code]
- `src/main/scala/radiance/core/TensorCoreDecoupled.scala` — **the Hopper-style baseline** Tensor Core, i.e. the *comparison* design is in the artifact too, with `case class TensorTilingParams(...)`, `val numWarps: Int`, and `val half: Boolean // input datatype is FP16 if true, FP32 if false` [code]. `src/main/scala/radiance/core/TensorDPU.scala` is the datapath unit; both have unit tests under `src/test/scala/radiance/` [code].
- `src/main/scala/radiance/memory/Coalescing.scala` — memory coalescer; `AlignFilterNode.scala`, `RWSplitterNode.scala`, `DoubleOutXbar.scala`, `SyncMem.scala` — the banking/alignment machinery [code]
- The README states Gemmini's **RoCC interface was replaced with TileLink** and that the unit interfaces "directly with cluster shared memory instead of private scratchpad", retaining accumulator memory — consistent with the paper [README, paper].
- Full-SoC evaluation requires the `virgo` branch of Chipyard, per the README [README].

## 12.9 Kernel execution

kernel → thread block → warp → instruction, but with the matrix path *detached*:
- A warp's instruction stream contains **loads and stores to an MMIO address region**, not matrix instructions. The paper is explicit: the design "does not require modification of the ISA and the core microarchitecture: the core controls the matrix unit simply by issuing regular loads and stores to a specific memory address region" [paper].
- The matrix unit then runs an internal FSM over the full (i, j, k) nest, so **one** issued command covers what would be many `HMMA`/`wgmma` instructions on a coupled design.
- Baseline models for comparison, all implemented in RTL [paper]: **Volta-style** (tightly coupled, per-core, 8×8 tiles from the register file, 2 cycles per HMMA instruction, 32 FP16 MACs/cycle); **Ampere-style** (same unit plus a dedicated global→shared DMA engine); **Hopper-style** (operand-decoupled access/execute, 16×16×32 tiles, operands from SMEM but accumulators in registers, 64 FP16 MACs/cycle).

## 12.10 Memory traffic

- **global → SMEM / accumulator memory**: via the DMA engine, without occupying core issue slots [paper].
- **SMEM → matrix unit**: over a dedicated cluster interconnect, in wide `4n`-byte (n=16) accesses, concurrent with narrow 4-byte SIMT lane traffic thanks to 2D banking [paper].
- **accumulator**: stays in the single-banked accumulator SRAM for the whole tile; never touches the register file. This is the traffic path that the paper argues is both the energy and the occupancy win [paper].
- **Reuse**: unified cluster-level design improves shared-memory data reuse by **44%** versus operand-decoupled designs [paper]. *Qualifier: RTL-simulated, Virgo vs Hopper-style baseline, on the paper's GEMM/FA3 workloads.*
- **register ↔ L1 ↔ L2 ↔ HBM**: L1 16 KB I/D per core, L2 512 KB shared [paper, Table 2]; no HBM model is described beyond the memory system of the Chipyard SoC. `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

The paper's headline is **not** a speedup; it is power, energy and utilisation. Decomposed causes [paper]:
1. **Instruction-count collapse.** One launch command per large tile instead of thousands of small MMA instructions removes core-side issue, scheduling and address-generation work. The component power breakdown shows "core power dominates overall consumption" and that Virgo reduces core issue/ALU stage power — i.e. **most of the saving is in the SIMT core, not in the MACs.**
2. **Cheaper accumulator storage.** A single-banked SRAM supporting only contiguous access costs less energy per access than a multi-banked register file built for divergent scatter/gather.
3. **Higher MAC occupancy.** 86.5% MAC utilisation for 1024×1024 GEMM versus Hopper-style 77.0%; for FlashAttention-3, 65.7% versus Ampere-style 35.1% — the FA3 gap is the larger one, consistent with the register-pressure-hurts-fused-kernels argument.
4. **Concurrency in shared memory.** 2D banking lets the systolic array and the SIMT lanes hit SMEM at the same time instead of serialising.

**Measured results, with baseline qualifiers** [paper]:
- **Active on-chip power**: **−67.3% vs Ampere-style** and **−24.2% vs Hopper-style** core-coupled RTL baselines.
- **Energy**: **−80.3% vs Ampere-style**, **−32.5% vs Hopper-style**.
- **FlashAttention-3**: 65.7% MAC utilisation vs Ampere-style 35.1%, with **50.6% energy reduction**.
- **Area**: **0.1% smaller SoC area than the Volta-style design; 3.0% larger than the Hopper-style design**. The 2D banking itself costs **9.6% area overhead** (of the shared-memory block).
- **Methodology qualifiers that must travel with every number above**: Chisel/Chipyard SoC, synthesised to gate level on a **commercial 16 nm PDK at 400 MHz**; power from **Cadence Joules** (active = total − idle); RTL simulation with **Synopsys VCS** (the paper notes Verilator fails); kernels compiled with Vortex's LLVM toolchain. Workloads: FP16 GEMM at 256³, 512³, 1024³, and **FlashAttention-3 at sequence length 1024, single head, batch 1, FP32 with a Taylor approximation for `exp`**.

## 12.12 Hardware generation dependence

This paper is unusual in the cluster: it does **not** run on real NVIDIA silicon at all. Generation hygiene therefore cuts a different way.

- The "Volta-style", "Ampere-style" and "Hopper-style" baselines are the authors' **RTL abstractions** of those generations' integration styles, at 8 lanes/warp and 400 MHz on a 16 nm PDK — **not** measurements of V100, A100 or H100. Every comparative number above is Virgo-vs-*model*, and must be quoted that way.
- What the paper models faithfully and says so: Hopper's `wgmma`-style operand decoupling from shared memory, with accumulators still register-file-bound [paper].
- What the paper explicitly does **not** address: **TMA**, **TMEM**, and **thread-block clusters / distributed shared memory**; it "treat[s] these as orthogonal concerns" [paper]. This matters: Blackwell's TMEM is a dedicated on-chip accumulator store, i.e. real silicon has since moved part-way toward Virgo's accumulator-disaggregation argument. Virgo (ASPLOS'25) and that Blackwell feature are contemporaneous; **this paper makes no claim about Blackwell and none should be inferred.** (Within this cluster, `GPU-SC26-02` documents `tcgen05.mma` accumulating in TMEM on SM100 — that is that paper's evidence.)
- The substrate is **Vortex**, an open-source RISC-V GPGPU with 8-lane warps, plus **Gemmini** — so absolute performance does not transfer to any commercial GPU. `[inference]` the *relative* energy conclusions are the transferable part, and the paper's own limitation note about depending on open-source rather than production-grade tooling says as much.

## 12.13 Limitations

Stated or acknowledged in the paper [paper]:
- Larger tile sizes reduce flexibility for **smaller GEMM dimensions** — the 128×64×128 tile is a poor fit for small problems.
- **Synchronisation overhead averages 2.4% of runtime** — the cost of the asynchronous/barrier model.
- Dependence on **open-source tooling (Vortex, Gemmini) rather than production-grade implementations**.
- 2D banking costs 9.6% area.
- No explicit future-work section was located. `NOT_IN_PAPER`.
- `[inference]` Sharing one matrix unit across 4–8 cores is a *contention* design point: the paper reports aggregate utilisation but the rendering read does not give a per-core fairness or tail-latency analysis under mixed workloads.
- `[inference]` Since the matrix unit reads operands from SMEM and writes accumulators to a dedicated SRAM, any kernel that wants to consume accumulator values in the SIMT lanes (a fused epilogue) must route them back through SMEM; the cost of that path is not separated out in the numbers read.

## 12.14 Relation to prior corpus

- **Complementary** to every kernel-level paper in this cluster: ConvStencil, SPIDER, FlashSparse, Acc-SpMM and the emulation papers all take the fragment shape and register-anchored operand contract as *given* and work around it. Virgo is the only assigned paper that proposes changing that contract. It is the cluster's architecture-side counterpart.
- **Cited prior work** [paper]: Tensor Core microarchitecture studies ([34], [39], [10]), **Gemmini** [21], **Vortex** [42], register-pressure mitigation work **INTERPRET** [30] and **Duplo** [29], and decoupled access/execute [38].
- **Self-positioning**: "the first effort to integrate a matrix unit at the core cluster" [paper] — the authors' claim, not verified here.
- **Watchlist adjacency**: *Cooperative Warp Execution in Tensor Core for RISC-V GPGPU* (HPCA 2025) is the closest neighbour — also a Tensor Core integrated into an open RISC-V GPGPU, but attacking warp-level cooperative issue rather than cluster-level disaggregation. *Uni-STC* (HPCA 2026) and *Coruscant* (MICRO 2025) are the sparse-unit-design neighbours. *Avant-Garde* (ISCA 2025) is the numeric-format-datapath neighbour. None has readable full text from here except Coruscant.
- **External-corpus caveat**: Virgo is a GPU architecture paper evaluated on GEMM and FlashAttention-3 and is plausibly present in the un-imported AI/HPC corpus (`domains/ai_hpc_systems/` = `EXTERNAL_IMPORT_PENDING`); no duplication claim is asserted. In-repo hits: `domains/gpu_systems/census/ASPLOS_2025.md` (census row) and `domains/hpc_quantum/corpus/quantum-hpc-survey/working-evidence/v2.txt` line 39, which is a **raw proceedings-TOC dump** (`3716281|1382-1399|Virgo: …`) and is existence evidence only, not an analysis. `NO_EXISTING_ANALYSIS` in-repo.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The paper's subject *is* a GPU microarchitectural property: the coupling of the matrix unit's operands and accumulators to the **per-warp register file** inside a SIMT core, and the occupancy/energy consequences of that coupling. Its mechanisms are all GPU-structural — a matrix unit placed at the **core-cluster (SM) level** shared across 4–8 SIMT cores, a dedicated accumulator SRAM replacing register-file accumulators, **two-dimensional (bank × subbank) shared-memory banking** invented specifically so a 64-byte systolic-array access and 8 lanes' worth of 4-byte SIMT requests can proceed in the same cycle, unaligned-lane-access filtering, split read/write paths for DMA producer / core consumer overlap, and an asynchronous warp execution model with cluster-wide barriers. There is no CPU analogue of "the matrix accumulator lives in the warp register file", so there is no CPU version of this contribution. It is verified against synthesised RTL and an inspected Chisel artifact.

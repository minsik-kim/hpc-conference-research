# GPU-MICRO25-61 — Dissecting and Modeling the Architecture of Modern GPU Cores

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — GPU core / warp execution: instruction issue, dependency handling, register file and register-file cache, memory pipeline` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `N — GPU simulation and performance modelling (Accel-Sim / GPGPU-Sim fidelity); microbenchmark-based reverse engineering`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` + `CODE` — abstract, introduction (simulator-obsolescence argument), reverse-engineering methodology (hand-written SASS + CLOCK timing, CUAssembler, NVBit 1.7.5, control-bit extraction from CUDA binary utilities), the dissected core model (L0 I-cache + stream buffer, fetch/issue schedulers, CGGTY policy, control bits, register file banking/ports, register file cache, result queue/bypass, memory pipeline and latency tables), the Accel-Sim re-implementation, validation against seven real SKUs, the control-bits-vs-scoreboard case study, limitations, related work. Code: `github.com/upc-arco/modern-gpu-simulator-micro-2025` cloned at commit `117f9dca3f46b1d85d2a1ec9ddac6b89d49399b3`; read `README.md`, `remodeling/warp_dependency_state.h`, `remodeling/register_file.h`, directory listing of `remodeling/`.

## 12.1 Bibliographic facts

- **Title** [paper]: *Dissecting and Modeling the Architecture of Modern GPU Cores*.
- **Venue** [paper]: MICRO 2025 — 58th IEEE/ACM International Symposium on Microarchitecture. `ARCHIVAL_MAIN_PAPER`.
- **DOI** [official-web]: `10.1145/3725843.3756041` (ACM DL record; `dl.acm.org` full text → 403, known constraint).
- **Authors** [paper]: Rodrigo Huerta, Mojtaba Abaie Shoushtary, José-Lorenzo Cruz, Antonio González — all Universitat Politècnica de Catalunya, Barcelona.
  - The artifact's copyright header spells the third author **"Josep-Llorenç Cruz"** [code, `warp_dependency_state.h`]; the PDF spells it "José-Lorenzo Cruz". Recorded as a discrepancy, not resolved.
- **Access** [official-web]: institutional-repository PDF at `upcommons.upc.edu/bitstreams/3d75bf4b-84c5-4901-a435-413ba8036f1b/download`, fetched 2026-09-18.
- **Artifact** [artifact]: `github.com/upc-arco/modern-gpu-simulator-micro-2025`, cloned at `117f9dca3f46b1d85d2a1ec9ddac6b89d49399b3`. Contains `simulator-remodeled/` (a modified Accel-Sim/GPGPU-Sim tree) and `APEs/` (per-configuration, per-application absolute percentage errors).
- **CORRECTION to the task assignment**: arXiv `2501.12084` is **not** this paper. `arxiv.org/abs/2501.12084` and `arxiv.org/html/2501.12084v2` serve *"Dissecting the NVIDIA Hopper Architecture through Microbenchmarking and Multiple Level Analysis"* by Weile Luo et al. (HKUST-GZ / HIT-Shenzhen) — the extended version of the IPDPS 2024 Hopper paper, analysed separately as `GPU-IPDPS24-61`. No arXiv preprint of the UPC MICRO 2025 paper was located; `NOT_FOUND_AFTER_SEARCH`.

## 12.2 Core question (one sentence)

What does the *issue stage, dependency-handling mechanism, register file and memory pipeline of a real modern NVIDIA GPU core* actually look like — and how much of the error in academic GPU simulators is caused by still modelling a 2006 Tesla core? [paper]

## 12.3 GPU/HPC problem translation

**Synchronization/dependency** and **scheduling**, at the finest granularity the machine has, plus a **methodology** contribution.

The paper's object is not a workload but the *core model itself*. Its claim is that the dominant open GPU simulator (GPGPU-Sim, and Accel-Sim built on it) "models GPU core architectures based on designs that are more than 15 years old" with Tesla (2006) as the baseline [paper], so that microarchitecture results published against it may not transfer. The mechanism dissected is intra-warp dependency resolution: how a modern core knows when a warp's next instruction is safe to issue.

## 12.4 Why the problem exists (hardware root cause)

[paper] NVIDIA publishes no core microarchitecture specification. Three consequences the paper identifies and fixes:

1. **The dependency mechanism is in the wrong place.** Academic models resolve RAW/WAW with a hardware scoreboard. Real Turing/Ampere/Blackwell cores instead carry **compiler-encoded control bits** in the SASS encoding. The hardware that a simulator spends state on does not exist in silicon.
2. **The operand collector does not exist either.** The paper's sharpest structural finding: modern NVIDIA GPUs "do not make use of" operand collector units. The reason is causal, not incidental — a compiler-set **stall counter** encodes *latency minus the number of instructions between producer and first consumer*, so the compiler must know the exact issue-to-writeback latency at compile time. Operand collectors "would introduce variability in the elapsed time between issue and write-back, making it impossible to handle dependencies correctly" [paper]. **The fixed-latency contract and the operand collector are mutually exclusive.**
3. **Missing structures.** No L0 instruction cache, no instruction prefetcher, no uniform register file, no register file cache in the baseline model; fetch and decode were collapsed into a single cycle [paper, and README items 9–12 of the artifact].

## 12.5 Mathematical / performance model

The paper's quantitative claim is a **fidelity** model, not an analytic one: MAPE of simulated cycles against real-hardware cycles over 128 kernels from 84 applications [paper].

| Real GPU (ground truth) | Architecture | This model, MAPE | Accel-Sim baseline, MAPE | Correlation (this / Accel-Sim) |
|---|---|---|---|---|
| RTX A6000 | Ampere | **13.45%** | 34.03% | 0.99 / 0.98 |
| RTX 3080 | Ampere | **13.24%** | 29.37% | 0.99 / 0.98 |
| RTX 2080 Ti | Turing | **19.30%** | 29.38% | 0.99 / 0.97 |
| RTX 5070 Ti | Blackwell | **17.41%** | — (no prior model) | 0.99 / — |

Tail behaviour, RTX A6000: worst-case per-benchmark APE 62% (this model) vs 513% (Accel-Sim); 90th-percentile APE 29.78% vs 89.31% [paper]. The headline "20.58% average MAPE improvement" is an average across configurations.

A second, structural model is the **dependency-state cost**:

- control bits: six 6-bit dependence counters + one 4-bit stall counter + one yield bit = **41 bits per warp**, 1,968 bits per SM, **0.09%** of the register file [paper];
- scoreboard: two tables × 332 entries × log₂(64) ≈ **2,324 bits per warp**, 111,552 bits per SM, **2.28%** of the register file at the 63-consumer configuration [paper].

(The abstract-level figure "1,968+ bits per warp / 5.32%" that appears in some renderings of this work conflates the per-SM control-bit total with a per-warp scoreboard figure; the per-warp/per-SM pairs above are the ones to quote, each with its configuration qualifier.)

## 12.6 Data layout and ownership

- **thread → warp**: 32 threads; a warp owns 64 architectural registers' worth of the 2,048 warp registers, plus **64 uniform registers, 8 predicate registers, 8 uniform predicates, 6 dependence (SB) counters and ≥16 B registers** [paper]. The uniform and predicate register files are separate structures the prior model lacked.
- **warp → sub-core**: dependency state is strictly per-warp. In the artifact this is the class `Dependency_State`, holding `m_yield`, `m_stall_counter` and a set of `Wait_Barrier` objects, each a single counter with `increase_counter()` / `decrease_counter()` and `is_ready(min_val)` [code, `warp_dependency_state.h`]. `Wait_Barrier_Type` is `{READ_WAIT_BARRIER, WRITE_WAIT_BARRIER}` — i.e. the model tracks the WAR-decrementing and RAW/WAW-decrementing roles as distinct barrier types, exactly as the paper describes.
- **sub-core → SM**: 65,536 32-bit registers per SM, organised as **two banks per sub-core** with 32,768 registers per bank; one 1024-bit read port and one 1024-bit write port per bank [paper]. Four sub-cores per SM.
- **Register file cache**: two entries per sub-core (one per bank), each caching three 1024-bit values (one per source-operand position) — **six 1024-bit operand values per sub-core** [paper]. In the artifact, `Register_file_cache` holds `std::vector<std::vector<Register_file_cache_entry>> m_entries` dimensioned `[m_max_num_operands][m_num_banks]`, and each `Register_file_cache_entry` is keyed by `{m_warp_id, m_reg_id}` with `is_hit(warp_id, reg_id)` [code, `register_file.h`] — confirming that the cache is indexed by *operand position × bank* and matched on *warp + register id*, which is precisely the paper's hit condition.
- **SM → GPU**: shared memory-pipeline structures accept one request per two cycles from any sub-core [paper].

## 12.7 Pseudo code

The issue-eligibility predicate, reconstructed from the paper's description and cross-checked against the artifact's class interface.

```
# --- per-warp dependency state ------------------------------------------- [paper]
warp.stall_counter : 4 bits          # 0..15, set by compiler per instruction
warp.yield         : 1 bit
warp.SB[0..5]      : 6 x 6 bits      # "dependence counters" / wait barriers

each cycle:                                                    # Dependency_State::cycle() [code]
    if warp.stall_counter > 0: warp.stall_counter -= 1

# --- producer side --------------------------------------------------------
on issue(inst):                                                # [paper]
    warp.stall_counter = inst.ctrl.stall            # fixed-latency covering
    if inst.ctrl.yield: warp.must_not_issue_next_cycle = True
    for b in inst.ctrl.set_barriers:                # variable-latency producers
        SB[b] += 1                                  # visible next cycle
on register_read_done(inst):  for b in inst.war_barriers:  SB[b] -= 1   # WAR
on writeback(inst):           for b in inst.raw_barriers:  SB[b] -= 1   # RAW/WAW

# --- consumer side: the issue predicate -----------------------------------
def ready(warp, inst):                                         # [paper]
    return (warp.stall_counter == 0)
       and (not warp.must_not_issue_next_cycle)
       and all(SB[b] == 0 for b in inst.ctrl.wait_mask)   # 6-bit mask
       and rf_ports_available(inst)
       and exec_unit_latch_free(inst)
       and l0_fl_constant_tag_resolved_or_timed_out(inst)  # 4-cycle timeout

# DEPBAR.LE relaxes the all-zero test:                         # [paper]
#   DEPBAR.LE SB1, 0x3, {4,3,2}  ==>  SB1 <= 3 and SB4==SB3==SB2==0

# --- issue scheduler: CGGTY (Compiler Guided Greedy Then Youngest) -------- [paper]
def select_warp(ready_warps):
    if last_issued_warp in ready_warps and not last_issued_warp.yielded:
        return last_issued_warp              # greedy
    return youngest(ready_warps)             # NOT oldest — youngest
```

Two details that matter and are easy to get wrong:
- the fallback tier is **youngest**, not oldest — this is not GTO [paper];
- the **yield bit** is an explicit compiler instruction to the hardware *not* to issue the same warp next cycle, i.e. warp interleaving is partly software-directed.

## 12.8 Real implementation

[artifact] `github.com/upc-arco/modern-gpu-simulator-micro-2025` @ `117f9dca3f46b1d85d2a1ec9ddac6b89d49399b3`.

- The new core model lives in `simulator-remodeled/gpu-simulator/gpgpu-sim/src/gpgpu-sim/remodeling/`. Files present [code, directory listing]: `subcore.{cc,h}`, `sm.{cc,h}`, `register_file.{cc,h}`, `warp_dependency_state.{cc,h}`, `first_level_instruction_cache.{cc,h}`, `stream_buffer.{cc,h}`, `ibuffer_remodeled.{cc,h}`, `functional_unit.{cc,h}`, `ldst_unit_sm.{cc,h}`, `l0_icnt.{cc,h}`, `gmmu.{cc,h}`, `page_table_walker.{cc,h}`, `fusedMemory/`, `new_stats.h`.
- The presence of a **separate `stream_buffer` module and `first_level_instruction_cache`** confirms the paper's L0-I-cache-plus-stream-buffer-prefetcher claim as implemented, not merely described [code].
- `README.md` enumerates 16 deltas vs Accel-Sim [README]. The ones load-bearing for this analysis: "Tracer that parses control bits"; "Simulator that interprets control bits"; "Configurable dependence handling: scoreboards or control bits"; "Enhanced scoreboard detects dependencies in uniform, predicate, and uniform-predicate registers"; "Additional scoreboard to protect against WAR hazards"; "Added L0 instruction cache"; "Added stream-buffer instruction prefetcher"; "Corrected fetch and decode stage timing (no longer both in a single cycle)". The *configurable* dependence handling is what makes the control-bits-vs-scoreboard case study a like-for-like comparison inside one simulator.
- The repository also carries an **independent contribution the paper does not claim**: OpenMP parallelisation of the simulator, which the README asks be cited as Huerta & González, ISPASS 2025 / CAMS 2024 [README]. Do not attribute simulator speed to the MICRO 2025 paper.
- Traces are stored with **Google Protocol Buffers** and static instruction metadata is dumped to JSON [README] — a format change from stock Accel-Sim traces, relevant to anyone reusing traces across the two.
- `APEs/` holds the per-configuration error data underlying the MAPE tables [artifact]. Not read in this pass — `NOT_INSPECTED`.

## 12.9 Kernel execution

The corrected kernel → block → warp → instruction path [paper]:

1. **Fetch**: each sub-core has a private L0 instruction cache backed by a shared L1 I-cache, with a stream-buffer prefetcher whose inferred size is **8 entries**. One instruction fetched per sub-core per cycle. The fetch scheduler is greedy on the previously-issuing warp, falling back to the **youngest** warp with instruction-buffer space.
2. **Instruction buffer**: **three entries per warp**, not the two prior models assume [paper].
3. **Issue**: CGGTY as above.
4. **Control stage**: increments dependence counters, handles clock reads.
5. **Allocate stage** (fixed-latency instructions only): reserves register-file read ports for the next three cycles; stalls on conflict.
6. **Read**: *all* fixed-latency instructions take three cycles of operand read (Control, Allocate, read) regardless of operand count — FADD, FMUL and FFMA have identical read latency [paper]. Bank conflicts add bubbles: FMUL with both operands in one bank costs 1 cycle; FFMA with three operands in one bank costs 2 cycles.
7. **Writeback / result queue**: fixed-latency results bypass the register file. **Memory load results cannot use the bypass**, costing consumers an extra cycle [paper].

## 12.10 Memory traffic

Register ↔ RFC ↔ register file: the RFC absorbs repeat reads of the same operand position, allocated under compiler control via a **reuse bit** in the instruction's operand field; a hit requires same warp, same register ID *and* same operand position as the instruction that triggered caching. A cached value is invalidated once a read request arrives at the same bank and operand position, hit or miss [paper].

Register file ← memory: **512 bits per cycle** written back from memory operations [paper].

Memory pipeline [paper]: per-sub-core queue of 4 entries plus one dispatch latch (5 consecutive instructions buffered). The shared structures' one-request-per-two-cycles limit produces the issue-rate schedule: one memory instruction every 4 cycles with one sub-core active, still every 4 with two, every 8 with four contending.

Selected measured latencies (real hardware, per Table 2) [paper] — quote with the address-register qualifier, they differ by it:

| Instruction | Address register | WAR latency | RAW/WAW latency |
|---|---|---|---|
| Global load, 32-bit | uniform | 9 | 29 |
| Global load, 32-bit | regular | 11 | 32 |
| Shared load, 32-bit | uniform | 9 | 23 |
| Global store, 32-bit | uniform | 10 | — |

Constant path: fixed-latency instructions use an **L0 FL constant cache** (miss ≈79 cycles); `LDC` uses a **separate L0 VL constant cache** [paper].

## 12.11 Why it is faster/slower (decomposed cause)

The paper's performance claim is about *fidelity* and about *the hardware's own design choice*, not about a speedup it delivers.

**Why software dependence management wins** [paper, simulated with the artifact's configurable mechanism]:
- Performance: control bits 1.0× (baseline) vs scoreboard 0.98× at the 63-consumer scoreboard configuration. A *single*-consumer scoreboard is far worse — cutlass-sgemm runs at 0.62×; widening the scoreboard to 63 consumers recovers it to 0.96×. So the scoreboard's deficit is a **consumer-tracking-capacity** problem, and closing it is what makes the scoreboard expensive.
- Area: 0.09% of the register file vs 2.28% [paper].
- Fidelity: modelling control bits gives 13.45% MAPE vs 15.21% with a scoreboard, on RTX A6000 [paper] — the hardware behaves more like the control-bit model, which is the evidential core of the claim.

**Where Accel-Sim's 34.03% error came from** is not attributed to a single cause by the paper; the ablation sweeps configurations (stream-buffer size disabled/1–32/perfect, 1 vs 2 RF read ports, with/without RFC, scoreboard consumer counts) rather than decomposing the baseline error. `[inference]` the largest single structural gap is the absent L0 I-cache + prefetcher plus the collapsed fetch/decode timing, but the paper does not isolate it and this should not be stated as a finding.

## 12.12 Hardware generation dependence

- **Real SKUs used** [paper]: Ampere — RTX 3080, RTX 3080 Ti, RTX 3090, RTX A6000; Turing — RTX 2070 Super, RTX 2080 Ti; Blackwell — RTX 5070 Ti. Seven SKUs, three generations. These are **measurements on real silicon** for the microbenchmarks and the validation targets; the model's outputs are **simulated**.
- Tooling: CUDA 12.8 (CUDA 11.4 for some comparisons), CUAssembler for cross-architecture SASS modification, NVBit 1.7.5 for tracing, CUDA binary utilities for control-bit extraction (NVBit does not expose control bits) [paper].
- **Scope is consumer/workstation Turing→Blackwell.** Hopper (H100) is **not** in the SKU list, and no Hopper-specific mechanism (TMA, wgmma, distributed shared memory, thread-block clusters) is dissected here. Blackwell coverage is the RTX 5070 Ti, i.e. **GB20x consumer Blackwell, not the B100/B200 datacenter part** — no claim about TMEM or `tcgen05` appears and none should be inferred. Do not merge this paper's Blackwell findings with datacenter-Blackwell microbenchmark results.
- Older generations (Tesla, Fermi, Kepler) are explicitly treated as obsolete baselines, not modelled [paper].

## 12.13 Limitations

Stated [paper]:
- The exact **instruction fetch policy** was not determined; it is *assumed* similar to the issue policy.
- **Register-file read arbitration is not fully characterised** — "we could not find a model that perfectly fits all the experiments". This is the authors' own strongest caveat and it sits underneath the RF-port and bank-conflict numbers.
- Operand collection for **variable-latency** instructions is not fully resolved (the "no operand collector" finding is established for the fixed-latency path).
- Some Deepbench kernels have no available SASS, so the evaluation falls back to a **hybrid mode using traditional scoreboards** for those kernels — meaning the control-bit model is not exercised uniformly across the 128-kernel set.
- Some memory latencies in Table 2 are marked approximate; WAR/RAW latencies for 64-bit and 128-bit stores could not be fully gathered.

`[inference]`, not stated: reverse engineering by timing hand-written SASS establishes *behavioural equivalence*, not structural truth — a different structure with the same timing is not excluded. The paper's own hedging on RF arbitration is an instance of this.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep for the title finds only `domains/gpu_systems/census/MICRO_2025.md` — a STEP A/B census row.
- **Directly revises the baseline of** `GPU-ISCA24-61` (GhOST, ISCA 2024): GhOST adds out-of-order issue on top of Accel-Sim's scoreboard-and-operand-collector core model, which this paper measures at 34.03% MAPE against an RTX A6000 and argues is structurally wrong for the very stage GhOST modifies. GhOST also identifies operand-collector congestion as LOOG's failure mode — a structure this paper says modern hardware does not have. **The two papers are in direct tension about what the issue stage is, and neither evaluates against the other.** This is the single most consequential cross-paper finding in this cluster.
- **Complementary methodology sibling**: `GPU-IPDPS24-61` (Luo et al., Hopper dissection) does microbenchmark-based reverse engineering of a *different* layer (memory hierarchy, tensor-core instruction latency, TMA, DSM) on a *different* generation (Hopper H800 vs Ampere/Turing/Blackwell consumer parts). Together they establish microbenchmarking-plus-SASS as the dominant 2024–2026 method for GPU core knowledge.
- **Complementary**: `GPU-MICRO25-01` (STEM/root-sampled GPU simulation) and `GPU-HPCA24-41` (GPU scale-model simulation) address simulator *cost*; this paper addresses simulator *correctness*. They are orthogonal and composable.
- **Precursors cited** [paper]: Jia et al. (Volta, Turing microbenchmarking), Lashgar et al. (Fermi/Kepler memory), Abdelkhalik et al. (Ampere PTX→SASS latencies), Wong et al. 2009 (Tesla control flow), Shoushtary et al. 2024 (Hopper DPX), Khairy et al. (Volta L1/L2), Ahn et al. 2021 and **Jin et al. 2024** (GPU NoC — the latter is `GPU-MICRO24-63` in this cluster); simulators GPGPU-Sim, Accel-Sim, MGPUSim, NVArchSim.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: Every dissected mechanism is a property of the SIMT core. (a) The dependency state is **per-warp**, and its cost argument is expressed as a fraction of the *register file* — 41 bits/warp at 0.09% of the RF vs a scoreboard at 2.28% — a ratio that exists only because a GPU register file is enormous relative to its control state; on a CPU the comparison inverts. (b) The **absence of operand collector units** is derived from the compiler-set stall counter requiring statically known issue-to-writeback latency, a contract that only makes sense when the compiler schedules a warp's instruction stream against banked, wide (1024-bit) register-file ports. (c) The **yield bit** is a compiler directive controlling *warp interleaving* — software-directed latency hiding with no CPU analogue. (d) The issue policy CGGTY is a warp-selection policy; "greedy then youngest" is meaningless without resident warps. (e) The memory-pipeline model is expressed in terms of **sub-core contention for shared SM structures** (one request per two cycles across four sub-cores). The contribution is a model *of* the GPU core; it does not survive translation to any other machine.

verdict: `CORE_GPU`

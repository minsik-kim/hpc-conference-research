# GPU-MICRO24-61 — Concurrency-Aware Register Stacks for Efficient GPU Function Calls

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — GPU core / warp execution: register file organisation, register allocation, occupancy` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `B — ABI / calling convention and hardware-software contract; GPU L1D bandwidth contention; thread-block concurrency control`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` — motivation (40.4% L1D-access figure, inlining cost), background (warp-granular register allocation, NVIDIA ABI, local-memory stack), the CARS mechanism (RFP/RSP, offset renaming, three watermark policies, dynamic policy state machine, circular stack, trap handler), divergence/recursion/indirect-call handling, evaluation setup (Accel-Sim + NVBit + AccelWattch, V100 config, 22 apps), full results incl. idealised-configuration comparison, LTO comparison, L1D-bandwidth and cross-architecture sensitivity, residual spill/fill table, limitations, related work. **No artifact/code repository located — `NOT_INSPECTED`.**

## 12.1 Bibliographic facts

- **Title** [paper]: *Concurrency-Aware Register Stacks for Efficient GPU Function Calls*.
- **Venue** [census]: MICRO 2024, Session 5A "GPU Synchronization/Concurrency". `ARCHIVAL_MAIN_PAPER`. The PDF itself does not print the venue — venue is from `domains/gpu_systems/census/MICRO_2024.md` and the author's publication page path `tgrogers/publication/kang-micro-2024/`.
- **Authors**: the PDF byline reads **Ni Kang, Ahmad Alawneh, Mengchi Zhang, Timothy G. Rogers** (Elmore Family School of ECE, Purdue University); Mengchi Zhang is noted as now at Meta [paper]. The census row records the order as *Ni Kang, Mengchi Zhang, Ahmad Alawneh, Timothy G. Rogers*. **Discrepancy recorded, not resolved** — do not assert an order.
- **DOI**: `UNKNOWN`. Census gives only `ieeexplore.ieee.org/document/10764484/` (→ 418, not retried).
- **Access** [official-web]: author PDF `engineering.purdue.edu/tgrogers/publication/kang-micro-2024/kang-micro-2024.pdf`, fetched 2026-09-18. NSF PAR mirror `par.nsf.gov/servlets/purl/10591701` also listed in the census (not needed).
- **Artifact**: `NOT_FOUND_AFTER_SEARCH` per census; none located here. `NOT_INSPECTED`.
- **Acronym**: the paper names the mechanism **CARS**.

## 12.2 Core question (one sentence)

If a GPU's register file is large enough to hold several nested function frames but the ABI forces callee-saved registers out to the local-memory stack anyway, can the *call stack itself be kept in the register file* — and what does that cost in occupancy? [paper]

## 12.3 GPU/HPC problem translation

**Memory** traffic caused by a **scheduling/resource-allocation** contract.

The paper's target is not computation but the bytes moved between the register file and L1D purely to satisfy the calling convention. Across 22 function-calling applications on an **NVIDIA V100**, **40.4% of in-core L1D accesses come from moving register state back and forth between the register file and the L1D** to maintain ABI compliance [paper]. That traffic is simultaneously a *capacity* problem (it evicts real data) and a *bandwidth* problem (it occupies L1D ports).

The alternative the ecosystem currently uses is aggressive inlining, which the paper prices: relative to separate compilation, full inlining costs **10.15× binary construction time and 1.54× binary size** [paper].

## 12.4 Why the problem exists (hardware root cause)

[paper] Three properties compose into the problem:

1. **Registers are allocated per warp, contiguously, and fixed at kernel compile time.** Each warp receives a contiguous fixed region; register identifiers are 8-bit, capping architectural registers at 256 per function. An SM holds 2,048 warp-registers' worth of state.
2. **The linker must size that region for the worst case over the whole call graph** — the deepest call path determines every warp's allocation. So deep call graphs either burn occupancy or force spilling.
3. **The GPU ABI was inherited from RISC CPUs.** Callee-saved registers begin at R16 and are preserved by *storing them to local memory*, which on NVIDIA hardware is an L1D-backed memory operation. There is no register-window or renaming hardware to avoid it.

The decisive observation is that **even an infinite register file does not fix this**: the ABI's preservation semantics are expressed in memory instructions, so the spill/fill happens regardless of capacity. The paper substantiates this by measuring an idealised "virtual warps" configuration with unlimited registers and shared memory, which yields only **1.06× geomean** versus CARS's 1.26× [paper, Accel-Sim, V100 config, 22 apps].

## 12.5 Mathematical / performance model

The allocation model is a static analysis plus a runtime policy [paper]:

- **FRU** (Function Register Usage): additional registers a function needs.
- **MaxStackDepth**: the maximum register demand over any path in the call graph, computed by lightweight call-graph analysis at link time. Defined for **acyclic** graphs; for cyclic (recursive) graphs the analysis assumes one iteration.

Three allocation policies trade concurrency against spilling:

| Policy | Registers reserved per warp for the stack | Consequence |
|---|---|---|
| Low-watermark | one function call + base kernel | maximum occupancy; spills whenever call depth > 1 |
| High-watermark | `MaxStackDepth` | zero spills for acyclic call graphs; minimum occupancy; may force context switches at barriers |
| N×Low-watermark | `N ×` Low-watermark | middle ground |

Selection is **dynamic and per-SM** [paper]: initially half the SMs run Low-watermark and half High-watermark; after each thread block completes, its performance is recorded and new thread blocks are deployed with whichever allocation performed better, then adjusted by a 2× or 0.5× multiplier. This is a hill-climb over allocation size using SM-level A/B measurement, not a compile-time decision.

The renaming rule is arithmetic, not a table [paper]:

```
if  16 <= x < 16 + (RSP - RFP):
        physical_register = RFP + (x - 16)
else:   physical_register = x        # architectural register, unmodified
```

This works *only* because the ABI's callee-saved registers are a **contiguous block starting at R16** — the paper's stated reason for avoiding "expensive register renaming tables".

## 12.6 Data layout and ownership

- **thread → warp**: registers are 128 B wide — 4 B per thread × 32 threads. Nothing in CARS is per-thread; the stack is a *warp* object.
- **warp state added** [paper]: a **Register Frame Pointer (RFP)**, a **Register Stack Pointer (RSP)**, and a free-register count. Three small per-warp values.
- **SM state added** [paper]: a **stalled-warp list** for warps awaiting register allocation, sized at most **64 × 6 bits = 48 bytes**; plus register-allocation metadata held in the issue stage.
- **SM**: 2,048 registers total across warps; 128 KB L1D per SM in the modelled V100 configuration.
- Nothing crosses the SM boundary. No multi-GPU dimension.

The overflow path is a **circular register stack**: when demand exceeds the allocation, the oldest frames are evicted to memory in wraparound order and refilled when the corresponding functions return [paper]. So memory is not eliminated, it is demoted to a backstop.

## 12.7 Pseudo code

Reconstructed from the paper's call/return description; `RFP`, `RSP`, `FRU`, `MaxStackDepth`, low/high/N×-watermark are the paper's own names.

```
# --- link time ------------------------------------------------------------ [paper]
for f in call_graph:  FRU[f] = extra registers f needs
MaxStackDepth = max over acyclic paths of sum(FRU)      # cyclic: assume 1 iteration

# --- kernel launch -------------------------------------------------------- [paper]
stack_budget = policy in {Low, N x Low, High=MaxStackDepth}   # per SM, adapted

# --- call ----------------------------------------------------------------- [paper]
on CALL f from warp w:
    push(w.RFP)                                  # caller frame pointer onto reg stack
    if free_registers(w) >= FRU[f]:
        w.RFP = w.RSP
        w.RSP += FRU[f]
    else:
        software_trap()                          # spill oldest frame(s) to memory
                                                 # circular stack wraps around

# --- operand rename (every instruction, issue stage) ---------------------- [paper]
def rename(x):
    return RFP + (x - 16) if 16 <= x < 16 + (RSP - RFP) else x

# --- return --------------------------------------------------------------- [paper]
on RET in warp w:
    w.RSP = w.RFP                                # deallocate frame
    w.RFP = pop()                                # restore caller frame pointer

# --- divergence ----------------------------------------------------------- [paper]
# threads in one warp calling different functions -> allocate max(FRU) over them
# threads returning at different points -> delay deallocation until SIMT-stack rejoin
# indirect call -> max(FRU) over all functions reachable from that call site
```

The divergence rules are where the GPU-specificity is starkest: a warp has **one** RFP/RSP pair, so a divergent call must be sized for the union of the callees and the frame cannot be popped until the SIMT stack reconverges.

## 12.8 Real implementation

No public artifact was located; census records `NOT_FOUND_AFTER_SEARCH`. **No `[code]` evidence exists for this entry — do not attribute symbols.**

Simulation stack [paper]:
- **Accel-Sim**, cycle-level trace-driven; traces generated with **NVBit** from real V100 execution.
- **AccelWattch** for energy.
- Baseline modelled on **NVIDIA V100** (128 KB L1D per SM, 2,048 registers per SM).
- Compilation with **NVCC, CUDA 11.4**, using separate compilation (`-dc`) specifically to *prevent* automatic inlining — i.e. the baseline is deliberately the non-inlined one.
- Version/commit for Accel-Sim, NVBit and AccelWattch: `UNKNOWN`.

## 12.9 Kernel execution

Kernel → thread block → warp is unchanged; what changes is the **occupancy computation**. The paper lists the four standard limits on thread blocks per core (thread count, thread-block count, register usage, shared-memory usage) and CARS acts on the third by making the register allocation *dynamic and policy-selected* rather than linker-fixed at worst case.

Warp-level: call and return are direct branches executed by all threads of the warp in lockstep. CARS inserts, at the issue stage, a renaming step and a free-register check on `CALL`; the check's failure path is a **software trap**, not a stall.

Residual trap frequency [paper, Accel-Sim, V100, per-application]: for **PTA**, 0.014% of function invocations enter the trap handler and 0.78 bytes are spilled/filled per function call; **all other non-recursive applications show zero residual spills/fills**. Only 1 of 22 applications (PTA) ever requires a context switch.

## 12.10 Memory traffic

The whole point. Register ↔ L1D spill/fill traffic drops by **40% on average across the 22 workloads** [paper, Accel-Sim, V100 config]. Note this is a 40% reduction in *spill/fill accesses*, which is a different quantity from the 40.4% *share of L1D accesses* that motivated the work — the two 40s are not the same number and must not be conflated.

Second-order effect [paper]: in the PTA kernel, **global-memory bandwidth utilisation rises 98%** under CARS even though absolute bandwidth use is lower, because local-memory interference is removed and real global traffic can finally use the port. This is the clearest evidence that the problem was contention, not volume.

The L1D-bandwidth sensitivity study makes the same point from the other side [paper]: scaling cache ports from 2× to 8× baseline buys only **1.02–1.03×**, while CARS holds **1.28–1.29×** throughout. **Adding bandwidth does not solve a problem caused by spill/fill volume.**

## 12.11 Why it is faster/slower (decomposed cause)

Geomean **1.26×** performance and **1.28×** energy efficiency over the baseline V100 configuration [paper, Accel-Sim + AccelWattch, 22 apps]. The paper decomposes benefit into four regimes (its Table II):

1. **L1D capacity contention** — DMR, MST, CFD, GOL, STUT, ResnetFP. Confirmed by the fact that a 10 MB L1D also helps these.
2. **L1D bandwidth contention** — PTA, SSSP, TRAF, FIB, and the Rapids set (SVR, KMEAN, RF). Cache size is irrelevant here; only removing the traffic helps.
3. **Low occupancy** — Bert Atscore, Bert Atop. Benefit arrives as **reduced load-dependency stalls**, because the warp no longer waits on a fill.
4. **No benefit** — LULESH, NBD, COLI, RAY, where spills/fills are under ~5% of instructions.

Against idealised alternatives [paper]: unlimited-resource virtual warps give 1.06×; an oracle concurrency limiter (Best-SWL) helps only the capacity cases; CARS at 1.26× beats both, because it is the only one that removes the *instructions*.

Against full inlining via LTO [paper]: LTO 1.28× vs CARS 1.26× geomean — **essentially a tie**, but with a very different distribution. On PTA, CARS gives **2.74×** against LTO's 1.26×, attributed to smaller binaries (less instruction-cache pressure) and better inter-warp locality from the concurrency limiting. So CARS is not merely "inlining in hardware"; where it wins it wins for an occupancy/I-cache reason inlining cannot reach.

Where it loses: **MST cross-architecture** [paper] — on an RTX 3070 (Ampere) configuration MST gets 1.21× versus 3.82× on V100, because Ampere's occupancy constraints force the Low-watermark policy and therefore more spills. The mechanism's benefit is *conditional on being able to afford High-watermark*.

## 12.12 Hardware generation dependence

- **Primary model**: NVIDIA **V100** (Volta) configuration in Accel-Sim, traces from real V100 hardware via NVBit. **Simulated, not measured** — the only real-hardware step is trace collection and the motivating 40.4% L1D-access measurement.
- **Secondary model**: RTX 3070 (**Ampere**) configuration, used for the cross-architecture sensitivity study. Most workloads track V100 at ~1.26×; MST regresses as above.
- **Not evaluated**: Turing, Hopper, Blackwell, or any AMD part. No claim about TMA, thread-block clusters, wgmma or CDNA register-file organisation appears, and none should be inferred. AMD's register allocation differs (vector/scalar register files on CDNA) and is entirely outside scope.
- The mechanism's dependence on **callee-saved registers starting contiguously at R16** is an NVIDIA-ABI property. A different ABI breaks the offset-renaming trick and would require a rename table.

## 12.13 Limitations

Stated or clearly implied [paper]:
- **Recursion**: static analysis assumes one iteration; High-watermark gives no zero-spill guarantee for cyclic call graphs. FIB is included to demonstrate *correctness*, not benefit.
- **Divergent calls waste registers**: the warp allocates for the maximum over all functions called by any lane, so lanes not taking that path hold dead space.
- **Indirect calls are pessimistic**: sized by the maximum FRU over all statically possible targets.
- **Context switches** add memory traffic and are only triggered at barriers; no general forward-progress guarantee is given. Exercised by 1 of 22 applications.
- **Trap-handler overhead is not quantified**.
- Benefit requires meaningful spill/fill traffic; LULESH sees 1.01×.
- Occupancy limits arising from shared memory or thread-block count are untouched.

`[inference]`, not stated: the dynamic policy state machine measures per-thread-block completion time on half the SMs at a time, which presumes thread blocks are roughly homogeneous; for kernels with highly variable per-block work the A/B signal would be noisy. The paper does not evaluate this.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Register Stacks" finds only `domains/gpu_systems/census/MICRO_2024.md`.
- **Same group, same conference, adjacent question**: `GPU-MICRO24-62` (ThreadFuser, Alawneh/Kang/Khairy/Rogers, MICRO 2024) shares two authors and independently identifies the same pathology from the other end — it observes that x86 compilers' register allocation, being unaware of SIMT's large multi-threaded register file, causes "unnecessary spills/fills" when CPU binaries are analysed under SIMT. **The two papers frame register spill/fill as a first-class GPU bottleneck in the same session year.**
- **Complementary, opposite direction**: `GPU-MICRO25-61` (Dissecting and Modeling Modern GPU Cores) reverse-engineers the same register file — two banks per sub-core, 1024-bit ports, a compiler-managed register file cache — on Turing/Ampere/Blackwell. CARS adds a *stack* to the register file; MICRO'25 finds NVIDIA already added a *cache* to it. Neither cites the other (CARS predates).
- **Precursors cited** [paper]: Zorua (holistic virtualisation of registers/scratchpad/thread slots), CRAT (Xie et al., TLP-coordinated register allocation spilling to shared memory), RegDem (Sakdhnagool et al.), Oehmke et al. register virtualisation, SVF (Lee et al.), SPARC register windows, Tomasulo; on the scheduling side CCWS and Divergence-Aware Warp Scheduling (Rogers et al. — the last author's own line). The paper's claimed distinction: prior GPU register work targets **capacity** contention only, while CARS targets **bandwidth interference** from the spill/fill memory instructions themselves.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The contribution is a register-window idea, and register windows are a CPU idea (SPARC) — but every design decision here is forced by GPU structure, and the paper's own measurements show the CPU version would not work. (a) The **cost being paid is occupancy**: reserving stack registers reduces thread blocks per SM, so the design's central tension (Low- vs High-watermark, adapted per SM at runtime) is a concurrency/latency-hiding trade-off that exists only because the GPU converts register pressure into fewer resident warps. On a CPU, reserving registers costs nothing in thread count. (b) The **spill destination is the L1D**, shared with all resident warps, so preservation traffic from one warp degrades every other warp's cache — the 40.4%-of-L1D-accesses figure and the 98% global-bandwidth recovery on PTA are both interference effects between concurrent warps. (c) The **frame is a warp object, not a thread object**: divergent calls must be sized for the union of callees and frames cannot be popped until the **SIMT stack** reconverges. (d) Registers are allocated at **warp granularity in contiguous linker-fixed regions sized for the worst-case call path**, which is why the problem exists at all. (e) The renaming shortcut depends on the NVIDIA ABI's contiguous callee-saved block at R16. Remove SIMT and nothing in the design has a reason to be as it is.

verdict: `CORE_GPU`

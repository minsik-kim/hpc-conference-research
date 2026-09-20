# GPU-ISCA24-61 — GhOST: A GPU Out-of-Order Scheduling Technique for Stall Reduction

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `A — GPU core / warp execution: instruction issue, warp scheduling, SIMT pipeline` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `B — instruction-level dependency handling and scoreboarding; GPU simulation methodology (SASS-trace vs PTX-trace evaluation)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` — introduction/motivation (stall taxonomy, SSSP latency-variability argument), background (SIMT warp scheduling, GTO, scoreboard, instruction buffer), the GhOST microarchitecture (Dependence Checker / Issue Buffer / GhOST scheduler / Instruction Table), RTL area+power methodology, evaluation setup (Accel-Sim, two SKUs, 28 benchmarks), limit study (Table V), IsB-size and warp-scheduler-policy sensitivity, GhOST-Precise variant, software-vs-hardware renaming study, LOOG comparison, limitations, related work. **No artifact/code repository located — `NOT_INSPECTED`.**

## 12.1 Bibliographic facts

- **Title** [paper]: *GhOST: A GPU Out-of-Order Scheduling Technique for Stall Reduction*.
- **Venue** [paper] / [census]: ISCA 2024, Session 1A "Microarchitecture". Publication type `ARCHIVAL_MAIN_PAPER`.
- **DOI** [census]: `10.1109/ISCA59077.2024.00011` (from `domains/gpu_systems/census/ISCA_2024.md`).
- **Authors** [paper]: Ishita Chaturvedi, Bhargav Reddy Godala, Yucan Wu, Ziyang Xu (Princeton University); Konstantinos Iliakis, Panagiotis-Eleftherios Eleftherakis, Sotirios Xydis, Dimitrios Soudris (National Technical University of Athens); Tyler Sorensen (UC Santa Cruz); Simone Campanoni (Northwestern University); Tor M. Aamodt (University of British Columbia); David I. August (Princeton University).
- **Access** [official-web]: author-hosted PDF at `liberty.cs.princeton.edu/Publications/isca24_ghost.pdf`, fetched 2026-09-18. `dl.acm.org` → 403 (known environment constraint, not retried).
- **Artifact**: none found. Census records `NOT_FOUND_AFTER_SEARCH`. `NOT_INSPECTED`.
- **Title-rendering note** [census]: the ISCA 2024 program page prints "…Technique for Stall Reduction" with lower-case "a GPU"; the proceedings record uses "A GPU". Same paper.

## 12.2 Core question (one sentence)

Can a GPU core recover the instruction-level parallelism that a *compiled SASS binary* still leaves on the table — without register renaming, a reorder buffer, a load–store queue, or branch speculation — by letting the existing warp scheduler pick from a small per-warp window of dependence-cleared instructions instead of only the head of the instruction buffer? [paper]

## 12.3 GPU/HPC problem translation

This is a **scheduling** paper at the *instruction-issue* granularity, with a **synchronization/dependency** root cause.

- Compute: not the bottleneck being attacked; the paper's premise is that functional units are idle.
- Memory: the *variance* of memory latency is the trigger, but GhOST does not change the memory hierarchy.
- Synchronization/dependency: the stall the paper removes is an intra-warp RAW/WAW dependency on an in-flight variable-latency instruction; the mechanism is a dependence checker, not a cache or prefetcher.
- Scheduling: GhOST sits strictly between decode and the existing warp scheduler; the warp scheduler's *policy* (GTO) is unchanged, only its *candidate set* widens. [paper]

The paper's framing belongs to the "latency hiding by TLP has run out" line: GPUs provide up to 64 warps per core [paper], but many applications cannot fill them, so per-warp ILP becomes the only remaining slack.

## 12.4 Why the problem exists (hardware root cause)

[paper] The GPU issue stage is strictly in-order *per warp*. A warp's instruction buffer (IB) holds two decoded instructions; the issue stage may only consider the oldest valid one. When that instruction has a dependence bit set in the per-warp dependence bit-vector against an in-flight write, the warp is ineligible — even if the *second* IB entry is independent and ready. The GPU's answer to this has historically been "switch to another warp", which works only while occupancy is high.

Root causes the paper names:
1. **Latency variability defeats static scheduling.** In SSSP the load latency distribution spans roughly 10⁰–10⁴ cycles [paper], so the compiler's chosen stall distance is right only for one point of that distribution. A statically optimal schedule "for every basic block execution" is therefore unattainable.
2. **Low occupancy removes the fallback.** When too few warps are resident, warp-switching cannot cover the stall.
3. **Hazard bits are per-warp and positional, not per-instruction-slot.** In the baseline, the dependence bit-vector is checked only for the IB head, so an independent younger instruction is invisible to the scheduler.

## 12.5 Mathematical / performance model

`NOT_IN_PAPER` as a closed-form model. The paper instead establishes an **empirical upper bound** by a limit study on idealised out-of-order execution with a deep reorder queue [paper]:

| Idealisation enabled (Accel-Sim, SASS traces, 28 benchmarks) | Geomean speedup over in-order GTO baseline |
|---|---|
| perfect branch prediction alone | 8.0% |
| perfect memory alias checking alone | 7.4% |
| unbounded register renaming alone | 15.1% |
| all three combined | 22% |

The design argument follows directly from this decomposition: renaming dominates, but it is also the most expensive; branch prediction and store-bypass alias checking buy the least. GhOST therefore keeps neither renaming nor speculation, and the paper's realised 6.9% geomean (RTX 2060S, Accel-Sim, SASS traces, vs in-order GTO) is positioned against the 22% idealised ceiling. **All of these are simulated, not measured.**

## 12.6 Data layout and ownership

- **thread → warp**: unchanged. GhOST never reorders across lanes; the SIMT lane-to-thread binding and the active mask are untouched.
- **warp → scheduler**: the per-warp state grows from an IB (2 entries) to an IB plus an **Issue Buffer (IsB)** whose baseline depth is 8 entries per warp, organised as an 8-way banked structure with one entry per warp per bank [paper].
- **scheduler → sub-core**: the Dependence Checker (DC, 8 IB-Calc structures) and the GhOST scheduler are **time-shared** across warps within a scheduler, not replicated per warp [paper] — this is the reason the area cost stays at 1276 µm² per scheduler.
- **SM**: 4 warp schedulers per SM in both modelled SKUs, so 4 GhOST instances per SM [paper].
- No state crosses SM, GPU or node boundaries. GhOST has no multi-GPU dimension.

## 12.7 Pseudo code

Reconstructed from the paper's §-level description of the three-stage flow; names in `[reconstruction]` unless the paper names them.

```
# --- decode stage: fill the Issue Buffer ---------------------------------
on decode(inst, warp w):                                   # [paper]
    inflight_dep = check_against_scoreboard(inst)          # baseline behaviour
    ib_dep[inst] = bitvector(len = |IsB[w]|)               # [paper] "IB-dep"
    for older in IsB[w]:                                   # NEW in GhOST
        if hazard(inst, older) in {RAW, WAR, WAW}:         # [paper] DC checks all three
            ib_dep[inst][pos(older)] = 1
    IsB[w].push(inst, inflight_dep, ib_dep)

# --- GhOST scheduler: choose candidates ----------------------------------
each cycle, time-shared over warps:                        # [paper]
    ready = [i for i in IsB[w]
               if i.inflight_dep == 0
              and i.ib_dep == 0                            # RDC: "Register Dependence Checker"
              and memory_order_ok(i)]                      # see below
    cand  = OSel(ready, k = 2)      # [paper] "Oldest Instruction Selection", 2 oldest
    ITab[w] = cand                  # [paper] Instruction Table, 2 entries per warp

# --- memory ordering constraint ------------------------------------------
def memory_order_ok(i):                                    # [paper]
    # only load-load pairs may be reordered; every other memory pair,
    # and every synchronisation instruction, is kept in program order.
    ...

# --- warp scheduler: UNMODIFIED policy, widened candidate set -------------
issue():                                                   # [paper]
    w = GTO_select(warps with non-empty ITab)   # policy logic unchanged
    emit(ITab[w].oldest_issuable())
```

The essential asymmetry: **the DC computes hazards against instructions that have not yet issued** (the IsB), which the baseline never does; the baseline scoreboard only tracks instructions already in flight.

## 12.8 Real implementation

- **No public artifact located** — census records `NOT_FOUND_AFTER_SEARCH` for a repository; none was found in this pass. All implementation claims are `[paper]`; no `[code]` evidence exists for this entry. Do not attribute simulator symbols to this work.
- **Simulator implementation** [paper]: GhOST was implemented inside **Accel-Sim**. The paper does not state an Accel-Sim commit or release version — `UNKNOWN`.
- **RTL implementation** [paper]: the Dependence Checker, Issue Buffer and GhOST scheduler were written in RTL and synthesised with **Synopsys** at the **45 nm** node. This is the only part of the work that touches a physical-design flow; the pipeline as a whole was not synthesised.

## 12.9 Kernel execution

GhOST is invisible above the warp. Kernel → thread block → warp mapping, CTA scheduling, the active mask, reconvergence and barriers are all unchanged [paper]. The change is confined to the warp's instruction stream:

- fetch/decode proceed as before, but decode now writes into the IsB via the DC rather than into a 2-entry IB consumed in strict order;
- up to 2 instructions per warp become simultaneously issuable;
- the warp scheduler still issues **one instruction per cycle**;
- `bar.sync`-class synchronisation instructions and stores act as ordering fences within the warp's window [paper].

**Branches**: GhOST *may* move a branch earlier relative to older independent instructions in the IsB, but it does not predict or speculate past it — dependent instructions wait for resolution [paper]. This is the single largest departure from a CPU OoO core and is why no ROB or recovery path is needed.

## 12.10 Memory traffic

GhOST does not change the register ↔ shared ↔ L1 ↔ L2 ↔ HBM path, cache sizes or coalescing. Both simulated SKUs use a 64 KB L1 and 65,536 registers per SM [paper]. The only memory-side effect is *reordering in time*: an independent load can be issued earlier, moving its miss earlier and overlapping it with the stalled instruction's latency. The paper attributes the benefit to earlier miss initiation rather than to any reduction in traffic volume.

Notably, the paper diagnoses its predecessor's failure in exactly this layer: under LOOG, "the operand collector may become congested with stalled instructions due to true dependencies… this congestion prevents ready-to-issue instructions from proceeding due to structural hazards" [paper]. GhOST avoids the operand-collector occupancy problem because instructions are held in the IsB *before* register read, not after.

## 12.11 Why it is faster/slower (decomposed cause)

1. **Widened per-warp candidate set.** The ready condition is evaluated on up to 8 buffered instructions instead of 1, so a warp that the baseline would mark ineligible can still issue. Stall reduction across benchmarks is reported at 22%–94% [paper, Accel-Sim, SASS traces].
2. **Benefit is inversely correlated with occupancy.** Geomean 6.9% on RTX 2060S (32 warps/SM max) vs 5% on RTX 3070 (48 warps/SM max) [paper]. More resident warps means the baseline's warp-switching already covers the stall. The same gradient appears in the scheduler-policy sensitivity study: as the policy becomes *less* aggressive (GTO → LRR → SRR), GhOST's gain grows [paper].
3. **Renaming is the missing 8 points.** The limit study attributes 15.1% to unbounded renaming alone vs GhOST's realised 6.9% [paper]. The paper argues the gap is partly recoverable *in software*: compiler loop unrolling plus register renaming within the 255-architectural-register limit closes much of it, with "this performance gap is not significant" [paper] — an explicitly qualitative claim, no number given for the software-renaming geomean.
4. **Why GhOST does not regress where LOOG does.** Evaluated on SASS, LOOG shows a 16.5% geomean **slowdown** and a worst case of 0.35× [paper], whereas the original LOOG paper reported a 16% speedup on PTX. GhOST reports **no slowdown on any of the 28 workloads** [paper]. Two causes are named: (a) the operand-collector congestion above; (b) PTX-vs-SASS — "the optimized static instruction scheduling of the final binary form negates many purported improvements from OoO execution" [paper].

**This is the paper's most transferable finding and it is a methodological one**: prior GPU out-of-order results measured on PTX traces do not survive re-measurement on SASS traces.

## 12.12 Hardware generation dependence

- **Modelled**: Turing (RTX 2060S — 34 SMs, 32 warps/SM, 4 schedulers/SM, 1905 MHz) and Ampere (RTX 3070 — 46 SMs, 48 warps/SM, 4 schedulers/SM, 1132 MHz) [paper]. Traces were collected on the **real RTX 2060S** with NVBit; execution itself is **simulated in Accel-Sim**, not measured.
- **Not modelled**: Hopper and Blackwell. No claim about TMA, wgmma, distributed shared memory, thread-block clusters or TMEM appears, and none should be inferred.
- **Area/power numbers are synthesis estimates at 45 nm**, then scaled by a stated multiplicative factor of 0.17 toward a 14 nm node and compared against the RTX 2060S's 445 mm² 12 nm die to yield "0.007% area increase" and 1.1707 mW [paper]. **This is a simulated/synthesised estimate with a cross-node scaling step, not a measured silicon number**, and the 45 nm → 12 nm comparison mixes nodes; treat the 0.007% figure as order-of-magnitude.
- **A generation-dependence caveat the paper does not resolve**: GhOST's dependence checking presumes a hardware scoreboard tracking in-flight writes. `GPU-MICRO25-61` (Huerta et al., MICRO 2025) reverse-engineers real Turing/Ampere/Blackwell cores as using **compiler-encoded control bits (stall counter, yield bit, six dependence counters) rather than a scoreboard**, and reports that Accel-Sim's scoreboard-based model is not what the hardware does. GhOST's mechanism is therefore defined against a *model* of the issue stage whose fidelity that later paper disputes. `[inference]` — GhOST predates it and does not discuss this; the interaction is unevaluated.

## 12.13 Limitations

Stated by the paper [paper]:
- No branch prediction — rollback cost across thousands of threads per warp is judged prohibitive.
- No register renaming, hence the ~8-point gap to the limit study.
- Memory reordering restricted to **load–load pairs only**; stores and synchronisation instructions remain ordered. This is deliberate: it avoids the alias-checking hardware LOOG needs.
- **Trace collection was incomplete**: "we could not collect SASS traces for all benchmarks as the GPU ran out of memory…, the NVbit tool crashed or the application ran for over six days." The 28-benchmark set is therefore a survivorship-filtered sample.
- Only two GPU generations evaluated; no claim about newer parts.
- The precise-exception-capable variant (**GhOST-Precise**, needed for demand paging / virtual memory) costs 0.6 percentage points, dropping geomean from 6.9% to 6.3% [paper].

Not stated, added here as `[inference]`:
- The IsB-size sensitivity (8 → 6.9%, 16 → 7.9%, 32 → 7.5% on RTX 2060S) is **non-monotonic** at 32; the paper does not explain the inversion.
- Power is reported only at 45 nm with no scaling; the area number is scaled but the power number is not.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Grep over the whole repository finds "GhOST" only in `domains/gpu_systems/census/{ISCA_2024,ISCA_2026,MICRO_2024,MICRO_2025}.md` — STEP A/B census rows, not analyses. (The MICRO 2024 hit is the unrelated *Ghost Arbitration* side-channel paper; the ISCA 2026 hit is unrelated.)
- **Competing/superseded model**: `GPU-MICRO25-61` (Dissecting and Modeling the Architecture of Modern GPU Cores, MICRO 2025) directly challenges the baseline GhOST is measured against — it shows the unmodified Accel-Sim core model carries 34.03% MAPE against a real RTX A6000 and that real cores use compiler control bits instead of a scoreboard.
- **Complementary**: `GPU-SC26-41` (Leo, cross-vendor GPU stall backward slicing) attacks the same object — issue-stage stalls — from the *measurement/attribution* side on real silicon rather than the microarchitecture side in simulation.
- **Precursors cited by GhOST** [paper]: LOOG (the direct competitor), Warped Pre-Execution, MIPSGPU, HAWS; on the warp-scheduling side TLS/LWM, CCWS, Dyncta, OWL, LCS, PCAL, Poise; plus Breathing Operand Windows and Shader Execution Reordering as compatible. GhOST positions itself as orthogonal to all TLP-throttling work: it exploits ILP, they manage TLP.
- **Historical framing** [paper]: explicitly modelled on the CDC 6600 — dynamic scheduling without renaming or speculation.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The mechanism is defined by GPU-specific structure on three counts. (a) The unit of buffering and dependence tracking is the **warp** — the IsB is banked one entry per warp per bank and the DC/GhOST scheduler are *time-shared across the warps of one warp scheduler*, which is what makes the design cost 1276 µm² instead of a CPU OoO front-end. (b) The design's central omission — no branch prediction — is justified by SIMT: rollback would have to be undone for every thread in a warp, so speculation is priced out by the width of the lane array, not by transistor budget. (c) The benefit is a direct function of **occupancy** (6.9% at 32 warps/SM vs 5% at 48 warps/SM; gains rise as the warp scheduler policy weakens), i.e. GhOST recovers exactly the latency-hiding that GPU thread-level parallelism fails to supply — a quantity that has no CPU analogue. A CPU out-of-order core retargeted at a GPU is precisely what LOOG was, and the paper's own measurement shows that design *loses* 16.5% on SASS; the delta between the two is the GPU-specific part. Additionally, the operand-collector congestion failure mode that GhOST avoids is a property of the GPU's banked register file and operand-collection stage.

verdict: `CORE_GPU`

# GPU-ASPLOS24-21 — T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `M GPU-aware / GPU-initiated communication & collectives`
secondary_topics: `L Multi-GPU interconnect & data paths; device-resident collective control`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2401.16677v1) read across motivation, the tracker/NMC/MCA mechanism description, the transparency claim, simulator and evaluation setup, near-memory reduction, results, §7 discussion incl. §7.8, limitations and related work. Figures/tables not individually transcribed; Table 1 config only partially recovered.`

## 12.1 Bibliographic facts
- Title (publisher capitalisation per census: "Fine-grained", not "Fine-Grained") `[census]`: *T3: Transparent Tracking & Triggering for Fine-grained Overlap of Compute & Collectives*
- Authors `[paper]`: Suchita Pati, Shaizeen Aga, Mahzabeen Islam, Nuwan Jayasena, Matthew D. Sinclair — University of Wisconsin–Madison and Advanced Micro Devices, Inc.
- Venue: ASPLOS '24, 27 April–1 May 2024, La Jolla, CA. DOI `10.1145/3620665.3640410` `[census]`
- Publication type: `ARCHIVAL_MAIN_PAPER`; read source is the `PREPRINT`.

## 12.2 Core question (one sentence)
Can the all-reduce on the tensor-parallel critical path be overlapped with the producer GEMM at *sub-kernel* granularity without rewriting the GEMM kernel, by having the GPU memory system itself notice the producer's stores and trigger the communication? `[paper]`

## 12.3 GPU/HPC problem translation
- **Communication**: tensor-parallel all-reduce sits between layers, on the critical path, and cannot be hidden by independent work the way data-parallel gradient all-reduce can.
- **Compute**: the producer GEMM; T3's point is to avoid changing it.
- **Memory**: the contribution's centre of gravity — reduction is moved into compute-enhanced memory, and a memory-controller arbitration policy manages the two competing streams.
- **Synchronization**: replaced. Instead of fine-grained software sync between GEMM tiles and collective chunks, a hardware tracker observes store completion.
- **Scheduling**: GEMM workgroups are staggered across GPUs so that each GPU produces the chunk its neighbour needs next.

## 12.4 Why the problem exists
Root causes the paper establishes `[paper]`:
1. **TP all-reduce is serialized with compute by dependence**, unlike DP all-reduce, so coarse overlap has nothing to overlap with.
2. **The ratio is worsening**: compute FLOPS scale faster than network bandwidth, and the paper projects communication at up to 46% (training) and 44% (inference) of runtime for futuristic models.
3. **Fine-grained software overlap costs either synchronization or intrusiveness**: prior approaches need "expensive fine-grained synchronization" or GEMM-kernel modifications that are "disruptive to GPU software infrastructure."
4. **Overlap creates resource contention** for both compute units and memory bandwidth, which erodes the benefit — so an overlap mechanism that consumes CUs/CUs-equivalent is self-defeating. This is why the tracker must be outside the compute units.
5. **Ring reduce-scatter's read-modify-write pattern multiplies memory traffic**, which is the specific traffic the near-memory reduction removes.

## 12.5 Mathematical / performance model
`NOT_IN_PAPER` as a closed-form analytical model. The paper's quantitative frame is a simulated cycle-level evaluation with a stated **6% error** for its multi-GPU Accel-Sim extension. No α–β model or roofline derivation is presented in the read text.

## 12.6 Data layout and ownership
- **workgroup (thread block)**: the unit whose output stores the tracker observes; workgroups are *staggered* across GPUs so producer order matches ring-reduce-scatter consumption order. `[paper]`
- **GPU**: each GPU owns a shard of the GEMM output; the collective is a ring reduce-scatter + all-gather across GPUs.
- **memory controller / near-memory logic**: owns the reduction operation itself — the accumulate happens at memory, so no GPU rank "owns" the partial sum in registers.
- **address space**: the key ownership device is that the producer's *output address space mapping* is configured so that stores into it are what initiates communication.
- thread/warp-level ownership: `NOT_IN_PAPER`.

## 12.7 Pseudo code
Reconstructed `[reconstruction]` from the paper's mechanism description; no symbol names are given in the read text, so all names below are invented and marked as such:
```
# ---- one-time setup (host) ----
configure_output_address_space(GEMM_out, mode = TRACK_AND_TRIGGER)   # [reconstruction]
program_tracker(dma_descriptors_for_ring_reduce_scatter)             # [reconstruction]

# ---- steady state, no host or kernel involvement ----
GEMM workgroup writes its output tile          # ordinary stores
  -> tracker observes stores to tracked range
  -> when a stage's stores complete, tracker issues pre-programmed DMA to the ring neighbour
  -> arriving DMA write lands on compute-enhanced memory, which performs an
     atomic in-place accumulate (near-memory reduction), no SM read-modify-write
  -> memory-controller arbitration (MCA) interleaves producer stream vs communication stream
```
`[inference]`: the paper does not publish tracker register names, DMA descriptor formats, or an MCA policy formula in the read text; these are described functionally only.

## 12.8 Real implementation
No artifact repository exists — census records `NOT_FOUND_AFTER_SEARCH`. `NOT_INSPECTED`. **No source symbols are asserted**; T3 is a simulated architecture proposal, and all names in §12.7 are `[reconstruction]`.

## 12.9 Kernel execution
- **kernel**: the producer GEMM kernel, essentially unmodified; no separate collective kernel is launched during the overlapped phase. This absence is the mechanism's point.
- **thread block**: staggered across GPUs so that chunk production order matches ring consumption order.
- **warp / instruction**: `NOT_IN_PAPER`. The paper does not report warp-level or instruction-level behaviour; the tracker operates on memory transactions, not on instructions.

## 12.10 Memory traffic
This is where the paper's causal story lives `[paper]`:
- Baseline ring reduce-scatter per step: read local chunk from HBM → reduce with received data in compute units → write result to HBM. Multiple read-modify-write cycles per element.
- T3: the arriving DMA write is *itself* the accumulate, performed by near-memory logic in compute-enhanced memory, citing prior compute-enhanced-memory proposals (Lee et al. 2021; Kim et al. 2021b). The intermediate reads and writes disappear and no compute-unit bandwidth is consumed for reduction.
- Result: **22% geomean (max 36%) reduction in data movement**. *(Qualifier: simulated, across the evaluated Transformer sublayers and TP degrees.)*
- **MCA** then arbitrates between the producer's store stream and the communication stream at the memory controller to reduce residual contention.

## 12.11 Why it is faster/slower (decomposed cause)
1. **Overlap granularity drops to the workgroup/stage level** without any software synchronization, because store completion in a tracked address range *is* the readiness signal.
2. **No compute units are spent on communication** — the paper states T3 requires "no additional GPU compute resources for communication," so overlap does not cannibalize the GEMM.
3. **Reduction traffic is eliminated at the memory**, not merely moved.
4. **Residual memory-bandwidth contention is arbitrated**, addressing the failure mode Rashidi et al. identified for coarse overlap.
5. **Where it is weaker**: benefits require communication to be on the critical path (i.e. TP), scale with model size and device count, and are simulated rather than measured.

Numbers with qualifiers `[paper]`, all from simulation with 6% modelling error:
- **Communication-heavy sublayers: 30% geomean (max 47%) speedup** for Mega-GPT-2 and T-NLG at **TP=8 and TP=16**.
- **29% geomean** for sublayers of ~500B-parameter models (PALM, MT-NLG) at **TP=32**.
- **Data movement: 22% geomean (max 36%) reduction.**
- **End-to-end: up to 12% for training, up to 15% for inference (prompt phase).** Note the end-to-end numbers are far below the sublayer numbers — the sublayer figure must never be quoted as a model speedup.
- Futuristic models evaluated at TP=64.

## 12.12 Hardware generation dependence
High, and in a direction that matters `[paper]`:
- **Requires compute-enhanced / near-memory-compute memory** that can atomically update on stores. The paper acknowledges this "is not yet standard in production GPUs," so T3 is a forward-looking architecture, not a deployable technique.
- Requires a new **programmable tracker** in the memory system and a new **memory-controller arbitration policy** — both are hardware additions.
- Reuses **existing DMA engines**, which is the one component assumed present.
- The interconnect modelled is a **ring topology** for all-reduce; **NVLink generation, switch topology and per-link bandwidth are not specified in the read text — recorded `UNKNOWN`.** This is a genuine gap relative to every measured paper in this cluster.
- GPU model: a modern GPU with 80 compute units and HBM; finer configuration in Table 1 was not fully recovered — `UNKNOWN`.

## 12.13 Limitations
Author-stated and read-established `[paper]`:
1. Optimized for **ring all-reduce in tensor parallelism**; other collectives (standalone all-gather/reduce-scatter, all-to-all) and other parallelism forms (DP, PP, MoE) are only discussed in §7.
2. **Near-memory compute is not standard hardware.**
3. **Simulation only** (extended Accel-Sim, 6% error); no real multi-GPU hardware validation.
4. Workgroup staggering requires scheduling coordination whose overhead is not quantified.
5. **"Transparent" is qualified**: the paper still requires producer-kernel changes described as "minor," plus output-address-space remapping — so transparency is relative to prior fused-collective work, not absolute.
6. Tested to 64 GPUs; genuinely multi-node scenarios appear only in §7.8 discussion.
7. Recorded here: the fabric is unspecified, so results cannot be tied to an NVLink/xGMI generation.

## 12.14 Relation to prior corpus
- No prior in-repo analysis. `[repo-grep]` `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` applies.
- **Same ASPLOS 2024 session (1B: Optimizing ML Communication) as TCCL** `[census]`, watchlisted in this cluster's ledger.
- **Competing / complementary** to `GPU-ASPLOS26-01` (MSCCL++): identical diagnosis (NCCL cannot fuse with compute), opposite remedy — T3 adds hardware so the *existing* software need not change; MSCCL++ changes the software so no hardware is needed. Both cannot be "the" answer.
- **Distinct from** `GPU-SC26-21` and `GPU-HPDC26-01`: T3's trigger is a memory-system hardware tracker, not a kernel issuing puts. It is the cluster's only pure *device-triggered* design.
- The paper positions against **NVSHMEM** by arguing symmetric memory "requires explicit synchronization and doesn't automatically orchestrate collective progress" — i.e. T3 treats symmetric memory as insufficient rather than as a step to build on.
- Related SC 2024 work in the verdict-only set, *Optimizing Distributed ML Communication with Fused Computation-Collective Operations*, is in the same design space and should be cross-checked when full text becomes available.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — but with the weakest GPU-specificity in this cluster, and that should be recorded honestly.** The GPU-specific properties the contribution depends on are: (a) the **GEMM workgroup** as the tracking and staggering granularity, so that sub-kernel progress is observable at all; (b) the fact that GPU **compute units are the scarce resource** a collective would otherwise steal, which is why the tracker must sit in the memory system; (c) GPU **HBM/compute-enhanced-memory** as the site of the atomic accumulate; and (d) GPU **DMA engines** as the pre-existing movers. The *pattern* — track producer stores, trigger DMA, reduce near memory — is not intrinsically GPU-only and could in principle be posed for another accelerator with workgroup-style parallelism and NMC-capable memory. The verdict is NO because the paper's problem (TP all-reduce on GPU clusters), its contention analysis (compute units and memory bandwidth), and its granularity (GEMM workgroups) are all stated in GPU terms.

**Control placement**: `device-triggered`. Not host-driven and not device-resident. The paper: "T3 transparently fuses producer operations with the subsequent communication by configuring the producer's output address space to initiate communication directly on the producer's store, requiring minimal application changes," and "It uses a lightweight and programmable hardware-tracker to track the producer/communication progress and triggers communication using pre-programmed DMA commands, requiring no additional GPU compute resources for communication." No CPU involvement and no explicit GPU-kernel synchronization occur during the overlapped phase; the *hardware* initiates. Established from the full text. `[paper]`

verdict_basis: The contribution is a GPU memory-system addition whose granularity (GEMM workgroup stores), scarce resource (compute units), and reduction site (compute-enhanced GPU memory) are GPU-specific; it is also the cluster's only design where initiation is performed by hardware rather than by a host or a kernel.

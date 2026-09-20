# GPU-ASPLOS26-166 — Bullet: Boosting GPU Utilization for LLM Serving via Dynamic Spatial-Temporal Orchestration

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` (LLM-serving subject matter; `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and explicitly covers serving — no claim is made about whether it holds a Bullet record). No analysis exists in this repository.
primary_topic: `K — GPU sharing / co-location (intra-device, SM-level)`
secondary_topics: `J — GPU runtime and scheduling; LLM prefill/decode disaggregation`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation incl. the wave-quantization and chunked-prefill measurements; design §3.2 performance estimator (SM-scaling roofline model), §3.3 SLO-aware task scheduler, §3.4 concurrent execution engine and §3.4.2 computational resource manager; runtime/driver interaction (libsmctrl, CUDA IPC, streams); evaluation setup (three GPU SKUs, three models, three traces, four baseline systems); limitations. Read via one full-text pass over the author-hosted ASPLOS'26 PDF. **Ablation section and per-configuration result tables were NOT returned by that pass** and are recorded as NOT_READ. Artifact inspected directly at the pinned commit below.`

## 12.1 Bibliographic facts

- Title: *Bullet: Boosting GPU Utilization for LLM Serving via Dynamic Spatial-Temporal Orchestration* `[paper]`
- Authors: Zejia Lin, Hongxin Xu, Guanyi Chen, Zhiguang Chen, Yutong Lu, Xianwei Zhang — all Sun Yat-sen University, Guangzhou `[paper]`
- Venue: ASPLOS '26, Pittsburgh PA, 22–26 March 2026. DOI `10.1145/3779212.3790135` `[official-web]` `[census/ASPLOS_2026.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Full text used: https://xianweiz.github.io/doc/papers/26asplos_bullet.pdf (author-hosted) `[paper]`. Preprint: https://arxiv.org/abs/2504.19516 `[README]` — the arXiv v1 carries the different title *"Boosting LLM Serving through Spatial-Temporal GPU Resource Sharing"*; recorded, not resolved.
- Artifact: https://github.com/zejia-lin/BulletServe, commit **`445afae2abc15d578d3107d37a9b57ebc49e5e46`** `[code]`. README confirms ASPLOS 2026 acceptance (2025/11) and arXiv release (2025/04). `[README]`

## 12.2 Core question (one sentence)

LLM prefill is compute-bound and decode is memory-bound, so chunked prefill forces a bad compromise on one GPU and disaggregation forces buying two — can both phases run *concurrently on the same device* with the SM array split between them and the split moved at runtime? `[paper]`

## 12.3 GPU/HPC problem translation

- **Compute (primary).** The resource being divided is the **SM array**, at TPC granularity, between two co-resident engines.
- **Scheduling.** The split is re-decided per prefill layer and per decode step, under an SLO objective.
- **Memory.** Not partitioned — the two engines *share* the KV cache and model weights through CUDA IPC, which is the opposite choice from every MIG-based system in this cluster.
- **Synchronization.** Two OS processes coordinate through shared memory with control bits and a ZeroMQ metadata channel. `[paper]`

## 12.4 Why the problem exists (hardware root cause)

1. **Wave quantization.** A kernel's CTAs execute in waves across the SMs; when the grid is not a multiple of the machine's CTA capacity the final wave leaves SMs idle. Chunked prefill makes this worse by construction: "chunked prefill typically uses suboptimal chunk sizes below GPU-saturating levels to prioritize low latency. This produces severe wave quantization effects, creating GPU bubbles." `[paper]` Measured: a 1k-token sequence's O-proj reaches "only 49% utilization versus theoretical 59%". `[paper]`
2. **Chunking degrades progressively.** "a progressive 10% compute efficiency drop across successive chunks (71% → 61%), with final chunk latency 1.9× that of the initial chunk"; a 16k-token prefill with 1k chunks costs "1.13× compared to unchunked execution", and with 2k chunks per-chunk latency rises "1.86×". `[paper]` (All qualified to the measured model/GPU configuration described in 12.12.)
3. **Prefill and decode are bound by different hardware resources.** Prefill saturates FLOPs, decode saturates memory bandwidth. Running them serially on one device means the FLOP units idle during decode and the bandwidth idles during prefill.
4. **The hardware offers no supported way to split the SM array per stream.** MPS's `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` is coarse, per-client and static; MIG is per-instance and offline. Bullet therefore uses an **undocumented debug path in the CUDA driver** — see 12.8.

## 12.5 Mathematical / performance model

The paper's model is the **SM-scaling roofline model (SRM)**, a roofline re-parameterised by the number of SMs allocated. As returned by the full-text pass:

- `T'_k,p = flop_k · min(flop_k/mem_k · D_p, C_p)^-1` — kernel *k*'s predicted time under partition *p*, where `C_p` is the compute ceiling and `D_p` the bandwidth available to that partition. `[paper]`
- Calibration: `α_p,ES = T_measured / T'_p,ES`, and the paper states the model "requires only 2 profiling samples". `[paper]` That is the design's key practicality claim — an SM-count-parameterised roofline calibrated from two points, rather than the exhaustive 5 × 8 × 3 profiling grid ParvaGPU needs (`GPU-SC24-161`).
- The scheduler "greedily searches for the optimal configuration and invokes computational resource manager to repartition SMs", operating **layer-wise for prefill and step-wise for decode**. `[paper]`

## 12.6 Data layout and ownership

- **thread → warp → CTA → TPC:** ownership is set by a **TPC bitmask attached to a CUDA stream**. The mask is a bitmask in which *a set bit disables* that TPC: "A set bit in the mask indicates that the respective Thread Processing Cluster (TPC) is to be __disabled__." `[code]` (`csrc/src/libsmctrl.h`)
- **TPC range assignment is contiguous and mirrored.** The artifact builds masks from a `[low, high_exclusive)` TPC range via `libsmctrl_make_mask`, and the decode engine takes its range **from the opposite end**: `SMController.set_stream_mask(..., reversed=True)` maps `low, high = total_tpcs - high, total_tpcs - low`. `[code]` (`python/sglang/srt/bullet/sm_controller.py`) So prefill grows upward from TPC 0 and decode grows downward from the top — the two ranges meet at a movable boundary and never overlap. **This is the cleanest realisation of software spatial partitioning in the cluster: the partition is literally one integer.**
- **Stream → engine:** each engine owns one CUDA stream; `tp_worker.py` creates `self.forward_stream = torch.cuda.Stream(priority=-1 if server_args.is_bullet_decode else 0)` — the decode engine's stream is given **higher CUDA stream priority** in addition to its TPC mask. `[code]` This combination (priority + mask) is not described in the prose returned by the full-text pass and is a genuine implementation finding.
- **GPU memory → shared, not partitioned.** The two processes share GPU buffers via `cudaIpcGetMemHandle` / `cudaIpcOpenMemHandle`. `[paper]` Control state lives in "OS-managed shared memory" with "control bits to indicate data availability". `[paper]`
- **Device → node:** evaluated at 8 GPUs per node across three SKUs (12.12).

## 12.7 Pseudo code

Component names, the SRM formula and the scheduling cadence are `[paper]`; the masking calls and the reversal are `[code]`; arrangement is `[reconstruction]`.

```
# Once per prefill layer / per decode step                            # [paper]
num_tpcs, policy = shared_mng.set_adaptive_prefill_num_tpcs(longest_queue_ms)   # [code]
              or  shared_mng.set_adaptive_decode_num_tpcs(longest_queue_ms)     # [code]

if num_tpcs != last_num_tpc:                                          # [code] change-only
    smctrl.set_stream_mask(forward_stream, 0, num_tpcs,
                           reversed = is_bullet_decode)               # [code]
    last_num_tpc = num_tpcs                                           # [code]

# inside SMController.set_stream_mask                                 # [code]
if reversed: low, high = total_tpcs - high, total_tpcs - low          # [code]
mask = libsmctrl_make_mask(low, high)                                 # [code]
libsmctrl_set_stream_mask(stream, mask)         # <128 SMs            # [code]
libsmctrl_set_stream_mask_ext(stream, u128)     # >=128 SMs           # [code]
# all subsequently launched kernels on `stream` are confined to those TPCs
```

The `num_tpcs != last_num_tpc` guard is worth noting: the mask is only rewritten when the decision changes, which is how the "microsecond-level overhead" claim `[paper]` is kept true in a per-layer control loop.

## 12.8 Real implementation

Repository `https://github.com/zejia-lin/BulletServe`, commit **`445afae2abc15d578d3107d37a9b57ebc49e5e46`**. `[code]` Built on **SGLang v0.4.6** and **PyTorch 2.6.0**, "4100 lines of Python code". `[paper]`

Real symbols read from the artifact — none reconstructed:

| Symbol | Where | What it does |
|---|---|---|
| `libsmctrl_set_global_mask(uint64_t)` | `csrc/src/libsmctrl.h` | default TPC mask for *all* kernels including CUDA-internal ones; supported CUDA 6.5–12.6 `[code]` |
| `libsmctrl_set_stream_mask(void*, uint64_t)` | same | per-stream TPC mask, overrides global; CUDA 8.0–12.6 `[code]` |
| `libsmctrl_set_stream_mask_ext(void*, uint128_t)` | same | 128-bit form, required above 64 TPCs `[code]` |
| `libsmctrl_set_next_mask(uint64_t)` | same | mask for the next launch from this CPU thread only `[code]` |
| `libsmctrl_get_tpc_info_cuda`, `libsmctrl_make_mask`, `libsmctrl_validate_stream_mask` | same / `sm_controller.py` | TPC count query, range→mask construction, mask verification `[code]` |
| `SMController`, `_LibSMCtrl`, `ScheduleBudget` | `python/sglang/srt/bullet/sm_controller.py` | ctypes binding and the prefill/decode range logic `[code]` |
| `set_adaptive_prefill_num_tpcs`, `set_adaptive_decode_num_tpcs` | `python/sglang/srt/managers/tp_worker.py` | the per-step partition decision, keyed on `longest_queue_ms` `[code]` |
| `cudaIpcGetMemHandle` / `cudaIpcOpenMemHandle` | `[paper]` | cross-process GPU memory sharing |
| ZeroMQ | `[paper]` | asynchronous metadata transport between engines |

**The decisive provenance fact, read from the artifact's own header:** libsmctrl is "Copyright 2022-2024 Joshua Bakita. Library to control TPC masks on CUDA launches. **Co-opts preexisting debug logic in the CUDA driver library**, and thus requires a build with `-lcuda`." `[code]` The dependency is pinned in the README: "CUDA <= 12.6, required by libsmctrl". `[README]` So Bullet's partitioning primitive is an *undocumented debug path in NVIDIA's closed driver, with an upper bound on the CUDA version it works with.* The same library underpins `GPU-PPoPP25-164` (SGDRC). Two independent ASPLOS/PPoPP-class systems in this cluster rest on one unsupported reverse-engineered interface — the single most important structural finding in this cluster.

Also read from the artifact: a guard that `libsmctrl_set_global_mask` is rejected when `total_sms >= 128` ("this method is problematic"), forcing the 128-bit per-stream path on H100-class parts. `[code]` And `SMController` degrades to a no-op under `is_hip()` — AMD is stubbed, not supported. `[code]` The repo also contains `list_mps_proc.py` `[code]`, consistent with the paper's note that "MPS enabled for spatial sharing but replaced with libsmctrl for dynamic control". `[paper]`

## 12.9 Kernel execution

1. **kernel → stream → TPC set.** A kernel inherits its stream's TPC mask at launch. Because the mask is per *stream*, not per launch, one write covers every subsequent kernel of that phase until the boundary moves. `[code]`
2. **TPC granularity, not SM.** TPCs contain 2 SMs on the evaluated parts — the artifact's own logging multiplies by two (`f"...set {low * 2}-{high_exclusive * 2} SMs for stream..."`). `[code]` So the partition quantum is 2 SMs: much finer than MIG's 16-SM `1g` slice on H100 (`GPU-ISC26-165`) but not arbitrary.
3. **No preemption, and none needed.** Because the two engines' TPC ranges are disjoint, neither needs to evict the other — contrast `GPU-PPoPP25-164`, which shares the SM pool over time and therefore needs a cooperative eviction flag polled with `ld.cv`. Bullet's disjoint-range design sidesteps GPU non-preemptibility rather than working around it. That is the cleanest engineering idea in the paper.
4. **Memory system is deliberately *not* isolated.** Both engines hit the same L2 and HBM. Bullet's bet is that prefill (compute-bound) and decode (bandwidth-bound) are *complementary* consumers, so sharing the memory path is a feature. SGDRC's bet on the same hardware level is the opposite — that channel contention is the dominant problem and must be colour-isolated. **The two papers make directly contradictory assumptions about whether co-located tenants should share the memory system, and neither tests the other's case.**

## 12.10 Memory traffic

- **KV cache and weights are shared**, not duplicated, via CUDA IPC. `[paper]` This is what makes intra-device disaggregation cheaper than the xPyD disaggregation baseline (MoonCake), which must move KV cache between devices.
- **HBM bandwidth is the decode engine's binding resource**, and the paper's own limitation acknowledges the consequence: "On low-compute GPUs running dense models, the limited SM budget obliges the decode phase to claim a larger ratio of SMs to saturate memory bandwidth, slightly tempering concurrent-execution benefits." `[paper]` I.e. on a bandwidth-rich/FLOP-poor part the partition boundary is pushed toward decode and the co-location gain shrinks.
- No L2/HBM counter analysis was in the read sections → `NOT_IN_PAPER`. Metrics were collected with Nsight Systems. `[paper]`

## 12.11 Why it is faster/slower (decomposed)

Mechanistic decomposition (headline throughput/goodput tables were **NOT_READ**, so no speedup number is asserted here):

- **Removed: wave quantization from chunking.** Prefill can run unchunked (or in large chunks) on its own TPC range instead of being cut into GPU-under-saturating chunks. The measured cost of the chunking it replaces: 71%→61% efficiency across successive chunks, final chunk 1.9× the first, 1.13×/1.86× latency inflation at 1k/2k chunks. `[paper]`
- **Removed: phase serialisation.** Decode proceeds on its own TPCs while prefill runs, so neither phase's bound resource idles.
- **Removed: inter-device KV transfer** relative to disaggregation, via CUDA IPC sharing on one device. `[paper]`
- **Added: partition control cost**, kept small by the change-only guard and the microsecond-level mask write. `[paper]` `[code]`
- **Added: memory-system contention**, unmanaged by design.
- **Added: a hard dependency on an undocumented driver debug path with a CUDA ≤ 12.6 ceiling.** `[code]` `[README]`

## 12.12 Hardware generation dependence

- Evaluated on **8×A100-80GB (108 SMs)**, **8×H100 (132 SMs)** and **8×H20 (78 SMs)**. `[paper]` The H20 inclusion is meaningful — it is the FLOP-reduced, bandwidth-preserved part, i.e. exactly the "low-compute GPU" case the limitations flag.
- **The 64-TPC boundary is a real code-visible generation break:** below 128 SMs the 64-bit mask path is used; at or above 128 SMs the 128-bit `_ext` path is mandatory and `set_global_mask` is refused outright. `[code]` A100 (108 SMs / 54 TPCs) uses the 64-bit path; H100 (132 SMs / 66 TPCs) does not.
- **CUDA ≤ 12.6** is a hard ceiling from libsmctrl. `[README]` Unlike MIG, this mechanism can be removed by a driver update.
- AMD/HIP is a no-op stub. `[code]`

## 12.13 Limitations

Stated by the paper:
- Reduced benefit on low-compute GPUs running dense models (decode must claim more SMs to saturate bandwidth). `[paper]`
- "For specialized architectures like DeepSeek-MLA where disaggregation proves fundamentally advantageous, Bullet's co-located approach may not match dedicated solutions' peak performance." `[paper]`
- Latency model does not yet cover new attention variants or LoRA. `[paper]`
- "Bullet's SM isolation policy could be relaxed to partial sharing, yet such exploration is orthogonal". `[paper]`

Added here:
- **No memory-system isolation whatsoever** — the assumption that prefill and decode are complementary consumers is untested against an adversarial or third co-tenant.
- **Unsupported driver dependency with a version ceiling** (CUDA ≤ 12.6, debug-logic co-option). `[code]` `[README]`
- **Two-phase, single-application scope.** This is intra-application co-location, not multi-tenant isolation; nothing here provides a security or fault boundary.
- Ablation and result tables **NOT_READ** in this pass.

## 12.14 Relation to prior corpus

- **Shares its partitioning primitive with `GPU-PPoPP25-164` (SGDRC).** Both use libsmctrl/TPC masks; SGDRC drives it through Task Meta Data to control *kernel* placement and adds persistent threads plus VRAM-channel colouring; Bullet drives it through the simpler *per-stream* mask and adds nothing in the memory system. This is the same mechanism deployed with opposite views of whether memory contention matters.
- **Opposite school to `GPU-SC24-161` (ParvaGPU) and `GPU-ISC26-165`.** Bullet's quantum is 2 SMs and changes per layer; MIG's is 16 SMs on H100 and changes only when the device is idle. Bullet's calibration needs 2 samples; ParvaGPU's needs a 5 × 8 × 3 grid per model.
- **Opposite school to `GPU-ASPLOS26-163` (gShare)**, which shares the whole GPU in time with no spatial split and no cooperation from tenant code. Bullet requires full control of both tenants (they are the same application).
- **Isolation-guarantee lineage:** `GPU-MICRO24-02` (STAR) and `GPU-ISC26-165` establish that even MIG — the strongest boundary here — leaks through the shared L3 TLB and the device-wide power domain. Bullet draws no memory boundary at all, so those leaks are not a *failure* of its design; they are its operating assumption. The corpus-level statement is that **the isolation strength ordering is MIG > TPC-mask+channel-colouring (SGDRC) > TPC-mask alone (Bullet) > time-slicing (gShare), and every one of them leaks somewhere.**
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and explicitly covers serving; SGLang/vLLM/MoonCake/Nanoflow records may exist there. Nothing is asserted.
- **`domains/hpc_systems_operations/`:** checked; no GPU-sharing or LLM-serving content in its topic files. No `GPU_DELTA_ANALYSIS` owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The mechanism is a **TPC bitmask written into a CUDA stream's driver-side state** — `libsmctrl_set_stream_mask` / `_ext`, a library that "co-opts preexisting debug logic in the CUDA driver library" and works only up to CUDA 12.6 — with the prefill and decode engines taking contiguous TPC ranges from opposite ends of the device. `[code]` The problem it solves, **wave quantization** (a kernel's CTAs not filling an integral number of waves across the SM array), is a SIMT-hardware phenomenon with no CPU analogue, and it is measured as such (49% achieved vs 59% theoretical for O-proj at 1k tokens; 71%→61% across chunks). `[paper]` The design further depends on the two engines sharing device memory through `cudaIpc*` handles rather than being isolated. On a CPU this would be thread-pool sizing; there is no contribution.

**Isolation mechanism: software SM partitioning at TPC granularity via per-stream TPC masks (`libsmctrl`, an undocumented CUDA driver debug path), with disjoint contiguous TPC ranges for the two engines, CUDA stream priority as a secondary lever, and *no* memory-system isolation (shared KV cache via CUDA IPC). Not MIG; MPS present but explicitly replaced.** `[paper]` `[code]`

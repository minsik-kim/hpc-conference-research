# GPU-SC24-161 — ParvaGPU: Efficient Spatial GPU Sharing for Large-Scale DNN Inference in Cloud Environments

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `K — GPU sharing / MIG / MPS / virtualisation / co-location`
secondary_topics: `J — GPU runtime and scheduling; bin-packing over hardware-constrained partition slots`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation (internal slack, external fragmentation); background on MIG GPC profiles and MPS; design (Profiler, GPU Segment Configurator = Optimal Triplet Decision + Demand Matching, GPU Segment Allocator = Segment Relocation + Allocation Optimization); evaluation setup (cloud instance type, MIG sizes, batch-size grid, process counts, baseline list); related-work comparison table; limitations. Read via three targeted full-text passes over arxiv.org/html/2409.14447v1. **Algorithm pseudocode boxes were not returned by any pass** — the algorithmic detail below is instead taken from the authors' released C implementation (commit pinned in 12.8), which is stronger evidence than the prose anyway.`

## 12.1 Bibliographic facts

- Title: *ParvaGPU: Efficient Spatial GPU Sharing for Large-Scale DNN Inference in Cloud Environments* `[paper]`
- Authors: Munkyu Lee, Sihoon Seong, Minki Kang, Jihyuk Lee, Cheol-Ho Hong (Chung-Ang University, Seoul); Gap-Joo Na, In-Geol Chun (ETRI, Daejeon); Dimitrios Nikolopoulos (Virginia Tech) `[paper]`
- Venue: SC 2024. DOI `10.1109/SC41406.2024.00048` `[census/SC_2024.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Full text used: https://arxiv.org/abs/2409.14447 → https://arxiv.org/html/2409.14447v1 `[paper]`
- Artifact: https://github.com/MunQ-Lee/ParvaGPU_SC24, commit `5f3de1e18582b4c81896a1c3eb0e2915238dfee6` `[code]`; Zenodo DOI badge `10.5281/zenodo.13329587` `[README]`. Note the README's own install instruction points at a *different* host (`gitfront.io/r/sslab6943/GPwisjzMNg8H/ParvaGPU.git`) than the GitHub mirror actually cloned — recorded as an artifact-provenance discrepancy, not resolved. `[README]`

## 12.2 Core question (one sentence)

Given that NVIDIA MIG can only carve an A100 into a small fixed set of GPC-count profiles at fixed placement slots, and that a workload's throughput rarely lands exactly on one of those profiles, how should a cloud provider choose *(instance size, batch size, MPS process count)* per DNN service and then pack those partitions across a fleet so that every service's latency+rate SLO is met with the fewest total GPUs? `[paper]`

## 12.3 GPU/HPC problem translation

- **Scheduling (primary).** Two distinct losses are named and separated, which is the paper's framing contribution:
  - *Internal slack* — "underutilization of the internal space of a partitioned GPU", i.e. a service placed in a partition larger than it needs. `[paper]`
  - *External fragmentation* — "non-continuous small spaces may preclude assignment of larger-sized GPU partitions", i.e. free GPCs that exist but cannot be combined into a legal MIG profile. `[paper]`
- **Compute.** SM/GPC count is the allocation quantum. MIG's quantum on A100 is a *GPU Processing Cluster*, and the legal instance sizes are 1, 2, 3, 4 and 7 GPCs — "5 and 6 GPC configurations unavailable due to hardware limitations". `[paper]`
- **Memory.** Memory rides along with the compute slice and is not independently sizable: an 80 GB A100's instances carry "10, 20, 40, 40, 80GB". `[paper]` Memory is also the binding constraint on MPS fan-out — the process count is capped at three "considering out-of-memory scenarios within the MIG instance". `[paper]` `[README]`
- **Synchronization / communication.** Not first-order. Each segment runs one model's inference processes; no inter-segment communication is designed for. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

The root cause is that **MIG's partition lattice is a hardware artifact, not a continuous resource dial**, and it is coarser than the granularity at which inference demand actually varies.

1. **Legal sizes are quantised and non-contiguous.** 1/2/3/4/7 GPCs only; 5 and 6 do not exist. `[paper]` A service that needs "5 GPCs' worth" of throughput must take 7 (internal slack) or be split.
2. **Legal *combinations* are enumerable and small.** The paper states the A100 admits "only 19 combinations such as 1-1-1-1-1-1-1, 4-3, 4-2-1, and 4-1-1-1". `[paper]` The artifact ships a shorter enumerated list of 11 configurations it actually drives, expressed as GI profile IDs: `mig_config=("0", "5,9", "5,14,19", "5,19,19,19", "9,14,14", "9,14,19,19", "9,19,19,19,19", "14,14,14,19", "14,14,19,19,19", "14,19,19,19,19,19", "19,19,19,19,19,19,19")` in `scripts/mig_config_set.sh`. `[code]` The commented header of that file lists the same 11 as GPC counts (`7`, `4,3`, `4,2,1`, `4,1,1,1`, `2,2,3`, `2,1,1,3`, `1,1,1,1,3`, `2,2,2,1`, `2,2,1,1,1`, `2,1,1,1,1,1`, `1,1,1,1,1,1,1`). `[code]` The discrepancy between "19 combinations" in the paper and 11 driven by the artifact is `UNRESOLVED` here; the 11 are the ones the evaluation can actually instantiate.
3. **Placement slots are constrained, not just counts.** This is the sharpest hardware fact in the work and it is only fully visible in the code. `src/allocator.c::find_fit_placement()` encodes, per instance size, which of the seven slots a new instance may occupy: a size-7 or size-4 instance may only start at slot 0; a size-3 instance may only start at slot 4; a size-2 instance may start at slot 0, 4 or 2 (in that preference order); a size-1 instance at 0, 6, 4, 1, 2, … `[code]` `find_fit_gpu()` additionally rejects a GPU for a size-3 request when slot 4 already holds a size-3, and rejects a size-1 request when slots 0 and 4 both hold size-3 instances. `[code]` **External fragmentation is therefore not a generic bin-packing artefact — it is a consequence of MIG's fixed placement lattice.**
4. **MIG alone under-fills an instance; MPS alone cannot isolate.** The paper's two-sided argument: MIG's "granularity is too coarse" to match a service's demand, while under MPS "internal GPU resources such as caches and memory controllers are shared among workloads, this could lead to interference issues". `[paper]` ParvaGPU's answer is to use each for what it is good at — MIG for the isolation boundary between *different* workloads, MPS for concurrency *within* one workload's instance where interference is between copies of the same model and is therefore profilable.

## 12.5 Mathematical / performance model

There is no closed-form analytic model; the model is **an empirical lookup table plus a greedy selection rule**, and the rule is legible in the code.

The profiling table is indexed by the triple *(instance size, batch size, process count)* and stores throughput and latency: `prof_data_arr[model_idx][instance_size][batch_size][num_proc]` with fields `trp`, `ltc` (and unused-in-selection `sm_active`, `sm_occu`, `dram_util`, `tensor_active`). `[code]` Grid extent per `inc/parva_sched.h`: `MAX_INSTANCE 5` (the five legal GPC counts), `MAX_BATCH 1024`, `MAX_NUM_PROC 3`, `NUM_MODEL 11`. `[code]` The README states the recommended batch grid is eight powers of two from 1 to 128. `[README]`

**Optimal Triplet Decision** (`src/configurator.c::optimal_triplet_decision`) maximises *throughput per GPC*, not throughput:

```
target_trp_per_instance = target_trp / target_instance_size        # [code]
```

subject to a latency admission test that is **hard-coded to 45% of the SLO**:

```
if (target_ltc < (float)(slo_ltc/2 * 0.9))                          # [code]
```

i.e. a kernel-side latency must fit in half the SLO with a further 10% margin, leaving the remaining budget for queueing and batch formation. The code also computes `batch_time = ((batch_size*(num_proc+1))/req_rate)*1000` — the time to accumulate one batch at the offered rate — but in commit `5f3de1e` this value is only printed in the debug trace, **not** used in the admission condition. `[code]` That is a real gap between the paper's stated intent (fit batching delay inside the SLO) and the released implementation, and it is recorded here rather than smoothed over.

The instance count for a service is `num_optimal_points = floor(req_rate / target_trp)`, decremented by one when the division is exact. `[code]` **Demand Matching** (`src/configurator.c::demand_matching`) then covers the residual rate `last_instance_trp = req_rate - optimal_trp` with a *single* extra instance, chosen as the smallest of the per-size best points (`size_1_point` … `size_7_point`) whose throughput covers the residual. `[code]` This is precisely the internal-slack-minimisation step: the bulk of the demand is served at the best throughput-per-GPC point, and only the remainder pays for a size mismatch.

## 12.6 Data layout and ownership

- **thread → warp → SM → GPC:** the GPC is the unit MIG hands out; ParvaGPU never reasons below it. `[paper]`
- **GPC → MIG instance:** one instance = 1, 2, 3, 4 or 7 GPCs at a legal placement slot. Modelled in code as `struct mig_instance { int placement; int size; struct svc_level_obj *service; }`. `[code]`
- **MIG instance → GPU segment:** a segment is "an MPS-activated MIG instance". `[paper]` `[README]` Ownership inside a segment is *one model*, replicated across up to three MPS client processes. Cross-model sharing inside a segment is deliberately never done — that is what preserves the isolation argument.
- **GPU:** `struct gpu_device { int idx; int usage; int config; float avail_req_rate; struct mig_instance *mig_instances[7]; }` — the seven-element array is the placement lattice. `[code]`
- **Node → cluster:** `NUM_GPU_PER_NODE 8`, `TOTAL_GPU 2000` in the shipped header. `[code]` Deployment output is grouped by node and by GPU within node. `[README]`

MPS is started per MIG instance with its own control daemon and pipe directory: `CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-$1:$2 CUDA_MPS_LOG_DIRECTORY=/var/log/nvidia-mps-$1:$2 CUDA_VISIBLE_DEVICES=$3 nvidia-cuda-mps-control -d` followed by `echo start_server -uid 0 | …`. `[code]` **No `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` is set anywhere in the artifact** — ParvaGPU does *not* use MPS's thread-percentage throttle; concurrency inside a segment is controlled purely by how many client processes are launched. `[code]` This is a substantive design fact that the paper's prose does not state.

## 12.7 Pseudo code

Component names, the two-stage structure and the objective are `[paper]`; function and field names are `[code]`; statement-level arrangement is `[reconstruction]`.

```
# Stage 1 — Segment Configurator                                   # [paper]
optimal_triplet_decision():                                        # [code] symbol
  for each model m:
    best = argmax over (size,batch,proc) of  trp/size              # [code]
           subject to  ltc < 0.45 * slo_ltc                        # [code]
    n = floor(req_rate(m) / trp(best));  if exact: n -= 1          # [code]
    total += size(best)*n + demand_matching(m)                     # [code]

demand_matching(m):                                                # [code] symbol
  residual = req_rate(m) - n*trp(best)
  for s in [1,2,3,4,7]:                                            # [code] ordering
      if residual <= trp(size_s_point(m)): pick s; break           # [code]
  return s

# Stage 2 — Segment Allocator                                      # [paper]
segment_relocation():                                              # [code] symbol
  enqueue every requested segment into per-size queues             # [code] size_7_queue…size_1_queue
  dequeueing(): for each segment, largest size first:
      g = find_fit_gpu(size)        # best-fit on free GPCs,       # [code]
                                    # *plus* MIG legality filters  # [code]
      p = find_fit_placement(g,size)# legal start slot for size    # [code]
      alloc_mig_instance(service,p,size)                           # [code]

optimization():                                                    # [code] symbol
  walk GPUs from the tail; for a lightly-loaded GPU,
      split its services' segments into size-2 / size-1 segments
      and re-place them, freeing whole GPUs                        # [code] structure
```

## 12.8 Real implementation

Repository `https://github.com/MunQ-Lee/ParvaGPU_SC24`, commit **`5f3de1e18582b4c81896a1c3eb0e2915238dfee6`** (clone depth 1, this pass). `[code]`

Real, inspected symbols and files — nothing below is reconstructed:

| File | Lines | Contents actually read |
|---|---|---|
| `src/parva_sched.c` | 42 | `main()`; calls `get_data_from_csv()`, `init_deploy()`, `optimal_triplet_decision()`, `segment_relocation()`; times the last two with `CLOCK_MONOTONIC`. |
| `src/configurator.c` | 195 | `demand_matching()`, `optimal_triplet_decision()`. |
| `src/allocator.c` | 528 | `init_deploy()`, `find_fit_gpu()`, `find_fit_placement()`, `alloc_mig_instance()`, `dequeueing()`, `optimization()`; the five size queues `size_7_queue`…`size_1_queue`. |
| `src/data_load.c` | 264 | profiling-CSV ingestion. `NOT_INSPECTED` in detail. |
| `src/queue.c`, `inc/queue.h` | 55 / 20 | queue primitives. `NOT_INSPECTED` in detail. |
| `inc/parva_sched.h` | 119 | `struct prof_data`, `struct svc_level_obj`, `struct mig_instance`, `struct gpu_device`; the constants quoted in 12.5/12.6; build switches `DATA_GEN`, `NO_MPS`, `NO_OPTIM`. |
| `scripts/mig_config_set.sh` | 50 | `nvidia-smi mig -dci; nvidia-smi mig -dgi;` teardown then `nvidia-smi mig -cgi <profile-ids> -C`; UUID enumeration by parsing `nvidia-smi -L`. |
| `scripts/mps_set.sh` | 3 | per-instance `nvidia-cuda-mps-control -d` + `start_server -uid 0`. |
| `prof_data/*.csv` | 11 files | profiling tables for bert, densenet121/169/201, inceptionv3, mobilenetv2, resnet50/101/152, vgg16/19 — these are the "11 diverse DNN workloads". `[code]` |

Two implementation facts worth carrying forward because they are invisible in the paper:
- The build switches `NO_MPS` and `NO_OPTIM` in `inc/parva_sched.h` are the ablation harness — the paper's ablations correspond to compiling these out. `[code]` `[inference]` on the correspondence.
- The MIG reconfiguration path is destructive: `pgrep -f mps | xargs kill; nvidia-smi mig -dci; nvidia-smi mig -dgi;` before `-cgi`. `[code]` MIG instances are torn down wholesale and MPS daemons killed, which is direct confirmation that **ParvaGPU's placement is a deployment-time decision, not an online one.** The paper does not state this; the code does.

## 12.9 Kernel execution

ParvaGPU contains no GPU kernels of its own. The kernel-level consequence of a decision is indirect and threefold:
1. **Instance size sets the SM budget** available to a kernel — a 1-GPC instance's grid is capped by that instance's SM count, so a kernel with many CTAs serialises in waves rather than co-residing. `[inference]` from MIG semantics; the paper reports no per-kernel occupancy analysis → `NOT_IN_PAPER`.
2. **MPS process count sets intra-instance concurrency.** With 2–3 client processes on one instance, kernels from different processes are submitted to the same hardware work queues under the MPS server, so CTAs from different processes can be resident on the same SM. The paper's justification for allowing this is that the co-runners are *the same model*, so interference is measurable once and reused. `[paper]`
3. **Batch size sets CTA count per kernel launch**, which is how the profiler's grid reaches the throughput/latency frontier. `[code]`

## 12.10 Memory traffic

No memory-traffic instrumentation is reported in the sections read → `NOT_IN_PAPER`. The profiling struct does carry `dram_util` and `tensor_active` fields `[code]`, so the harness can record DRAM utilisation and Tensor-pipe activity, but **the selection logic in `optimal_triplet_decision()` reads only `trp` and `ltc`** — these fields are collected and then not used for the decision. `[code]` This is a real limitation of the mechanism: ParvaGPU's segment choice is blind to memory-bandwidth pressure, and MIG's per-instance memory-slice isolation is being relied on to make that blindness safe.

The relevant hardware path is the one MIG actually partitions on A100: GPC → its own L2 slices and memory controllers/HBM stacks. Because ParvaGPU never co-locates *different* models in one instance, cross-tenant traffic interference is excluded by construction rather than managed. `[inference]`

## 12.11 Why it is faster/slower (decomposed)

ParvaGPU does not make any kernel faster. It reduces the **number of GPUs required to serve a fixed SLO set**, by three separable mechanisms:

1. **Throughput-per-GPC rather than throughput as the objective.** Selecting `argmax trp/size` rather than `argmax trp` is what stops the configurator from defaulting to 7-GPC instances. `[code]`
2. **Residual absorption by a single differently-sized instance** (Demand Matching) rather than rounding the whole service up. This is the direct attack on internal slack. `[code]`
3. **Placement-aware best-fit plus a splitting pass** (Segment Relocation + Allocation Optimization) — the splitting of a large segment into several smaller ones "and reallocating them" `[paper]` is what converts a fragmented tail of GPUs into freed whole GPUs.

**Cost side, which the paper is honest about:** profiling is a one-off per model per GPU over a 5 × 8 × 3 grid `[README]`, and MIG reconfiguration is destructive `[code]`, so a demand change requires re-solving and re-deploying.

## 12.12 Hardware generation dependence

Strongly dependent, and in a way that is architectural rather than incidental:
- The 1/2/3/4/7-GPC lattice, the 19 combinations and the placement-slot rules are **A100 facts**. `[paper]` `[code]` The artifact's profile IDs (`0`, `5`, `9`, `14`, `19`) are A100 GI profile IDs. `[code]`
- The README claims applicability to "NVIDIA A100 or H100" `[README]`, but the hard-coded profile-ID list and the placement rules in `find_fit_placement()` are not parameterised by SKU `[code]`, so H100 support is an assertion, not something the released code demonstrates. Compare `GPU-ISC26-165` in this cluster, which enumerates the **H100 96 GB** profile set (`1g.12gb`/`2g.24gb`/`3g.48gb`/`4g.48gb`/`7g.96gb`) and shows the SM counts differ (16/32/60/64/132) — a different lattice.
- Anything below the GPC (SM count per GPC, L2 slice topology) is invisible to ParvaGPU and would change silently across generations.

## 12.13 Limitations

- **Inference only.** "Applicability demonstrated for inference; adaptability for HPC and training requires modification". `[paper]`
- **Three MPS processes maximum**, set by out-of-memory risk inside an instance, not by a performance argument. `[paper]` `[README]`
- **Heuristic batch-size search**, not exhaustive. `[paper]`
- **Static deployment.** MIG reconfiguration in the artifact kills MPS daemons and destroys all compute/GPU instances first. `[code]` No online re-partitioning is demonstrated.
- **The admission test is a fixed 45%-of-SLO constant** in the released code, and the batch-formation delay it computes is not actually applied. `[code]` A workload whose queueing behaviour differs from the authors' assumption would be mis-admitted.
- **Memory-bandwidth-blind selection** — `dram_util` is profiled but unused. `[code]`
- **No comparison against software-partitioning approaches.** The baseline set (GSLICE, gpulet, iGniter, PARIS/ELSA, MIG-serving `[paper]`) is entirely MPS- or MIG-based. Systems that partition SMs *below* the MIG boundary via TPC masks (see `GPU-PPoPP25-164`) are absent from the comparison.

## 12.14 Relation to prior corpus

- **Direct background, already analysed:** `GPU-MICRO24-02` (STAR, MICRO 2024) shows that MIG does **not** partition the last-level TLB, and measures a 40% average slowdown for co-running MIG tenants versus running alone on that account. ParvaGPU's entire isolation argument rests on MIG being a sufficient boundary; STAR is the counter-evidence that the boundary is incomplete in the translation path. Neither paper cites the other (different submission windows); the pairing is this corpus's contribution and is the single most useful cross-read in this cluster.
- **Same cluster, competing isolation philosophy:** `GPU-PPoPP25-164` (SGDRC, PPoPP 2025) explicitly argues MIG's "granularity is too coarse … and can only reconfigure the allocation when it is idle", and builds SM control via TPC masks instead. ParvaGPU accepts the coarse lattice and solves the packing problem around it; SGDRC rejects the lattice. `[paper]` for SGDRC's characterisation.
- **Same cluster, characterisation counterpart:** `GPU-ISC26-165` measures on H100 what ParvaGPU assumes on A100 — that MIG slices are coarse relative to demand — and finds a residual interference channel (power throttling) that MIG does not isolate.
- **Utilisation context:** `GPU-IPDPS26-41` (production GPU telemetry) documents at cluster scale the underutilisation that motivates spatial sharing.
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and explicitly covers serving; whether it holds a ParvaGPU record is **not asserted**.
- **`domains/hpc_systems_operations/`:** checked. `topics/gpu_operations.md` and `topics/scheduling_resource_management.md` contain **no** MIG, MPS, GPU-sharing, co-location or spatial-partitioning content (verified by grep, zero hits). No `GPU_DELTA_ANALYSIS` is owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The optimisation variables *are* GPU hardware-partition facts: the legal MIG instance sizes on A100 are 1/2/3/4/7 GPCs with 5 and 6 physically unavailable, the legal start slots per size are fixed by the MIG placement lattice (encoded directly in `find_fit_placement()`), and the third variable is the MPS client-process count inside an instance. `[paper]` `[code]` Both the internal-slack term and the external-fragmentation term are defined by that lattice — on a hypothetical accelerator with continuously divisible resources both terms vanish and the paper has no subject. This is *not* generic bin packing: a generic bin-packer would not need `find_fit_gpu()` to reject a GPU because slot 4 already holds a size-3 instance.

**Isolation mechanism: MIG (between workloads) + MPS (within one workload's instance), with no MPS thread-percentage throttle.** `[paper]` `[code]`

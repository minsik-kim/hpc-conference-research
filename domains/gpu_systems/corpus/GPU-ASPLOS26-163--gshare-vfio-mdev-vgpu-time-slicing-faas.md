# GPU-ASPLOS26-163 — gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `K — GPU sharing / MIG / MPS / virtualisation / co-location`
secondary_topics: `J — GPU runtime and scheduling; serverless/FaaS cold-start and model swapping`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation with the production model-size and price measurements; design (vGPU virtualization via vfio-mdev, vgpu controller, vgpu scheduler, round-robin time slicing; function memory management with vGPU hot-plugging, checkpoint & restore, fast model swap; SLO-aware Dual-Queue Lazy Scheduling); runtime/driver interaction incl. the ioctl interception inventory and LOC; evaluation setup (server/GPU counts, slice sizes, trace, five baselines); results; limitations. Read via one full-text pass over the author-hosted ACM PDF at cis.temple.edu. Formal algorithm boxes and the theoretical DQLS analysis were **not** returned by that pass and are recorded as NOT_READ rather than reconstructed.`

## 12.1 Bibliographic facts

- Title: *gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform* (lower-case "platform" as published) `[paper]` `[census/ASPLOS_2026.md]`
- Authors: Yanan Yang, Zhengxiong Jiang, Meiqi Zhu, Hongqiang Xu, Yujun Wang, Liang Li, Jiansong Zhang (China Telecom Cloud Computing Research Institute, Beijing); Jie Wu (Temple University, Philadelphia) `[paper]`
- Venue: ASPLOS '26, Pittsburgh PA, 22–26 March 2026; session 2C "GPU Systems & Scheduling", volume 31V2. DOI `10.1145/3779212.3790168` `[paper]` `[census/ASPLOS_2026.md]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Full text used: https://cis.temple.edu/~jiewu/research/publications/Publication_files/3779212.3790168.pdf (co-author-hosted copy of the ACM PDF) `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` → no repository, commit or source symbol is asserted; `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

In a serverless GPU platform where most tenant models are small and requests arrive sparsely, can a GPU be sliced at *arbitrary* memory sizes and time-shared by many tenant functions — without MIG, without MPS, and without a user-space CUDA-API proxy — by mediating the GPU at the kernel driver's ioctl boundary? `[paper]`

## 12.3 GPU/HPC problem translation

- **Scheduling (primary).** Temporal multiplexing of one physical GPU across many vGPUs, plus request-level admission ordering by deadline slack.
- **Memory (co-primary).** GPU memory capacity is the hard admission constraint that makes the problem exist: a tenant's model must be resident to serve a request, but keeping it resident is what costs money. The motivating distribution is "78.1% of models are less than 4GB". `[paper]`
- **Compute.** Explicitly *not* partitioned. Each vGPU "exclusively occupies the GPU device within its time slice". `[paper]` gShare deliberately trades SM-level packing away in exchange for a partitioning mechanism that works on any GPU and requires nothing from the tenant's code.
- **Communication.** Model swap traffic between host memory / shared-memory snapshot pools and GPU memory is the cost term the design attacks.

## 12.4 Why the problem exists (hardware root cause)

1. **GPU memory is the scarce, non-overcommittable resource.** A function cannot serve until its weights are on the device, and the device has no demand paging that would make an idle tenant free. Hence FaaS "keep-alive" — and its cost: GPU instances at "approximately $3.06/h" against CPU at "$0.34/h". `[paper]` Coarse allocation on top of that wastes up to 85% of the resource, because "existing coarse-grained GPU functions may not precisely match user needs" when most models are under 4 GB. `[paper]`
2. **The GPU's control interface is closed and lives in the driver.** There is no vendor-supported way to give a VM or container a *fraction* of a GPU with arbitrary memory size. gShare's answer is to become the mediator at the one boundary that is stable and enumerable: the character-device ioctl interface between user space and `nvidia`/`nvidia-uvm`.
3. **GPU kernels are non-preemptive.** This is the hard constraint gShare must live with rather than remove, and the paper states the consequence plainly: a kernel "exclusively occupies the GPU device within its time slice" without preemption, and kernels longer than the 20 ms period "may span multiple scheduling periods, causing significant performance degradation". `[paper]` A time-slicing scheduler on a non-preemptive engine can only choose *when to admit the next kernel*, never *when to stop the current one*. Every design decision downstream (deadline-slack ordering, 40% time-estimate padding) follows from that.
4. **User-space proxying is too expensive.** Prior proxy-based swapping introduces "7%-61% performance fluctuations" and "10s to 100s of milliseconds" latency overhead. `[paper]` This is the argument for moving the interception point down into the kernel.

## 12.5 Mathematical / performance model

No closed-form model; a set of stated parameters and rules:

- **Time slice:** round-robin with a configurable period, **default 20 ms**. `[paper]`
- **Slice size range:** vGPU memory slices "range from 128MB to 40GB" on 40 GB A100s — i.e. continuous sizing, which is the direct contrast with MIG's five legal sizes. `[paper]`
- **Hot-plug latency:** attaching a vGPU to a running function drops from "~700ms to <1ms" via a "pseudo offloading" strategy. `[paper]`
- **Scheduling rule:** *Dual-Queue Lazy Scheduling* (DQLS) orders requests by **deadline slack**, splitting them into a `cacheQueue` (high SLO-violation risk) and a `shareQueue`, with a **minimum heap** maintaining the ordering. `[paper]`
- **Safety margin:** the model requires "40% redundancy to the original predicted model execution time" to absorb estimation error. `[paper]` That 40% is the price of scheduling non-preemptive work against deadlines.

## 12.6 Data layout and ownership

- **thread → warp → SM → GPU:** ownership is *whole-GPU, per time slice*. gShare never subdivides SMs. This is the cluster's clearest example of temporal rather than spatial sharing.
- **GPU → vGPU:** a vGPU is a mediated device exposed through **vfio-mdev**, giving "direct I/O device access between hardware and virtual machines". `[paper]` A vGPU owns a memory slice (128 MB – 40 GB) permanently and the compute engine transiently.
- **Channel state:** the scheduler "ensures that only one channel is active at any time". `[paper]` The GPU *channel* — the hardware command-submission context — is the object being multiplexed. That is the precise level at which gShare's isolation lives, and it is why no cooperation from the tenant's kernels is needed.
- **Model → snapshot:** checkpoint/restore stores model snapshots in **shared memory pools**, and "Fast Model Swap" skips the swap-out step entirely by reusing the cached snapshot. `[paper]`
- **Node → cluster:** 20 physical servers, 64 A100 (40 GB) GPUs. `[paper]`

## 12.7 Pseudo code

Component names, the ioctl inventory, the period and the queue structure are `[paper]`; arrangement is `[reconstruction]`. **No algorithm box was read** — this is a structural sketch, not a transcription.

```
# vgpu controller (kernel space, mdev)                             # [paper]
on ioctl(fd, cmd, arg) from a function process:
    if cmd in {17 NV_ESC APIs} ∪ {40 UVM_APIs}:                    # [paper] 57 total
        filter / account / rewrite                                 # [paper] "API filtering"
        enforce per-vGPU memory usage limit                        # [paper]
    forward to nvidia / nvidia-uvm

# vgpu scheduler                                                   # [paper]
loop every period (default 20 ms):                                 # [paper]
    v = next vGPU in round robin                                   # [paper]
    activate v's channel ; deactivate all others                   # [paper] one active channel
    # no preemption: the resident kernel runs to completion        # [paper]

# DQLS request admission                                           # [paper]
slack(r) = deadline(r) - now - 1.4 * predicted_exec_time(r)        # [paper] 40% redundancy
if slack(r) small: push r on cacheQueue   (keep model resident)    # [paper]
else:              push r on shareQueue   (allow swap / share)     # [paper]
pop from min-heap ordered by slack                                 # [paper]
```

## 12.8 Real implementation

No artifact located → `NOT_FOUND_AFTER_SEARCH`; nothing below is a code symbol read from a repository. The implementation facts the paper itself states:

- **Interception surface:** "**57 ioctl interfaces (17 NV_ESC APIs and 40 UVM_APIs)**" implemented in "**60,000 lines of C code**". `[paper]` The 17/40 split is the important structural fact: the majority of the intercepted surface is the **UVM** path, not the classic `NV_ESC_*` control path — i.e. most of what a modern CUDA process does to the driver goes through unified-memory calls, and that is where a shim has to do its work.
- **Mechanism:** `vfio-mdev` mediated devices. `[paper]`
- **Position relative to CUDA:** the vgpu scheduler "captures the CUDA driver API intercepted by the vgpu controller" — so interception is at the driver ioctl layer and the CUDA driver API is *reconstructed* from it, rather than being hooked in user space. `[paper]`
- **Compatibility claim:** "full CUDA interface", "compatible with today's mainstream ML frameworks" naming TensorFlow Serving, PyTorch, vLLM, SGLang. `[paper]` This is the payoff of intercepting below CUDA: no framework or kernel-source cooperation is required.
- **AMD:** "Adaptation efforts for AMD ROCm are in progress". `[paper]`

## 12.9 Kernel execution

gShare does not touch the kernel → CTA → warp → instruction chain at all, and that is the design's defining property. Its unit of control is the **channel**, one level above the kernel: a vGPU's channel is either active or not, and while active its kernels run to completion on the whole GPU.

Consequences the paper itself draws:
- **Under-fill.** "GPU virtualization is actually a temporal GPU sharing technology", risking underutilization "if kernels cannot fill all SM cores". `[paper]` A tenant whose kernel occupies 20% of the SMs wastes the other 80% for the whole slice — precisely the loss that SGDRC (`GPU-PPoPP25-164`) and ParvaGPU (`GPU-SC24-161`) exist to avoid.
- **Long kernels break the period.** Kernels longer than 20 ms span slices, with "significant performance degradation" from context switching and queueing. `[paper]`

So gShare buys universality (any GPU, any framework, any kernel, arbitrary memory sizes) at the cost of intra-slice SM utilisation. That trade is the cleanest single data point in this cluster.

## 12.10 Memory traffic

The traffic gShare manages is **model weights moving in and out of GPU memory**, not kernel-level HBM traffic (no HBM/L2 analysis is reported → `NOT_IN_PAPER`).

- Baseline cost of a swap-driven cold start under prior proxy approaches: "10s to 100s of milliseconds". `[paper]`
- vGPU hot-plug: "~700ms to <1ms" via pseudo offloading. `[paper]`
- Fast Model Swap removes the swap-*out* transfer by keeping a snapshot in the shared-memory pool. `[paper]`
- Aggregate effect, with qualifiers: **"gShare reduces GPU usage by 43%–63%"** while keeping ">95%" of latency targets, on 64 A100 40 GB GPUs across 20 servers, under one week of production traces from China Telecom's cloud plus MLPerf, against Keepalive (15-min TTL), FaasCache, FaaSwap, NoCache and FIFO. `[paper]` And "1.8×–2.7×" cost/performance over the state of the art under those same conditions. `[paper]`

## 12.11 Why it is faster/slower (decomposed)

- **The saving is a residency saving, not a throughput saving.** gShare's 43–63% GPU-usage reduction comes from *not keeping idle tenants resident*, which is possible because (a) slices are arbitrarily sized so a small model occupies little, and (b) hot-plug plus snapshot restore makes re-admission sub-millisecond rather than hundreds of milliseconds. `[paper]`
- **DQLS converts the non-preemption constraint into an ordering problem.** Since a running kernel cannot be stopped, the only lever is which request is admitted next; ordering by deadline slack and protecting at-risk requests in `cacheQueue` is a direct response to that.
- **Kernel-space interception is what makes the overhead small.** The comparison point is explicit: proxy-based approaches cost 7–61% fluctuation and 10s–100s ms; the mdev path avoids a user-space round trip per API call. `[paper]`
- **Where gShare is slower:** any workload whose kernels neither fill the SMs nor fit in 20 ms. The paper states the regime where it wins: "gShare performs particularly well in environments with a large number of tenant functions and sparse request arrival patterns". `[paper]` That is an honest scoping statement and should be carried with every number above.

## 12.12 Hardware generation dependence

- **Low at the mechanism level, high at the interface level.** Nothing in gShare depends on MIG, on SM counts, or on a partition lattice, so it applies to GPUs that have no partitioning support at all — the opposite of ParvaGPU's A100-specific design.
- But the 57 intercepted ioctls and the channel-activation mechanism are **driver-version-specific**, undocumented NVIDIA interfaces. A driver revision that changes the UVM ioctl surface breaks 40 of the 40+17. `[inference]` from the interception design; the paper does not discuss driver-version churn → `NOT_IN_PAPER`.
- Evaluated only on **A100 40 GB**. `[paper]` Whether one active channel per period remains the right control point on parts with more copy/compute engines is untested → `NOT_IN_PAPER`.

## 12.13 Limitations

Stated by the paper:
- **Temporal only** — no spatial sharing, so SM under-fill is unaddressed. `[paper]`
- **Non-preemptive execution** — kernels over 20 ms degrade significantly. `[paper]`
- **Prediction-dependent** — needs 40% padding on predicted execution time. `[paper]`
- **Workload-regime-dependent** — wins with many functions and sparse arrivals. `[paper]`
- **ROCm incomplete.** `[paper]`

Added here:
- **60 kLOC of kernel-space C mediating 57 undocumented ioctls** is a large trusted computing base sitting under every tenant; the paper reports no security analysis of the shim itself → `NOT_IN_PAPER`.
- **No comparison against MIG or MPS.** The five baselines are all FaaS caching/swapping systems. `[paper]` gShare's isolation is therefore never measured against the hardware isolation it implicitly replaces.

## 12.14 Relation to prior corpus

- **Third school in this cluster's three-way split.** `GPU-SC24-161` (ParvaGPU) = hardware partitioning (MIG+MPS); `GPU-PPoPP25-164` (SGDRC) = software SM partitioning (TPC masks, persistent threads, channel colouring); **gShare = driver-level interception with temporal sharing**. gShare is the only one of the three that requires nothing whatsoever from the tenant's code — SGDRC needs kernel source, ParvaGPU needs per-model profiling — and the only one that gives up spatial packing entirely.
- **Direct tension with SGDRC's premise:** SGDRC argues temporal multiplexing "cannot fully harness the GPU's resources, as BE tasks may be starved". `[paper]` (SGDRC) gShare concedes exactly this point in its own limitations and argues the FaaS regime (sparse arrivals, small models) makes it acceptable. Both statements can be true; the disagreement is about the workload, not the mechanism.
- **Complementary, already analysed:** `GPU-MICRO24-02` (STAR) is about interference *below* a hardware partition; gShare has no hardware partition to leak through, but pays the full under-fill cost instead.
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — `domains/ai_hpc_systems/` (`EXTERNAL_IMPORT_PENDING`) explicitly covers serving and serverless; no claim is made about whether it holds gShare or FaaSwap/FaasCache records.
- **`domains/hpc_systems_operations/`:** checked; no GPU-sharing, MIG, MPS or virtualisation content in its topic files. No `GPU_DELTA_ANALYSIS` owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The mechanism is a mediated **NVIDIA GPU character device**: 57 specific driver ioctls (17 `NV_ESC` control APIs and 40 UVM APIs, 60 kLOC) are intercepted through `vfio-mdev`, and multiplexing is performed by keeping exactly one GPU **channel** active per 20 ms period. `[paper]` Both the closed driver interface being the only available control point, and the necessity of period-based channel switching rather than preemption, are consequences of GPU-specific properties — a non-preemptive kernel execution model and a vendor-opaque runtime. On a CPU this is process scheduling; there is no contribution. The design's own stated weakness (SM under-fill within a slice) is likewise a GPU-specific failure mode.

**Isolation mechanism: driver shim (`vfio-mdev` mediated vGPU, ioctl interception) + time slicing at GPU-channel granularity, 20 ms round robin. Not MIG, not MPS, no spatial partitioning.** `[paper]`

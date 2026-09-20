# GPU-PPoPP25-164 — SGDRC: Software-Defined Dynamic Resource Control for Concurrent DNN Inference on NVIDIA GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `K — GPU sharing / MIG / MPS / virtualisation / co-location`
secondary_topics: `J — GPU runtime and scheduling; C — GPU caches / memory-channel structure (reverse-engineered); B — SM/TPC-level execution control`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation incl. the quantitative critique of MPS, MIG, temporal multiplexing, Orion and FGPU; design (tidal SM masking via libsmctrl/TMD, persistent-thread transformation, eviction flag, sliding window; VRAM-channel reverse engineering, shadow page table, bimodal tensors); implementation (TVM/nvcc pipeline, nvidia-uvm memory pool, index translation macro); evaluation setup (Tesla P40, RTX A2000, LS/BE model sets, Apollo trace, five baselines); results incl. SPT overhead; limitations incl. A100/H100 applicability and vendor-library incompatibility. Read via a full-text pass over the author-hosted PPoPP'25 PDF (people.cs.vt.edu), plus a pass over arXiv 2407.13996v1, which is the **same work under the earlier name "Missile"** — see 12.1.`

## 12.1 Bibliographic facts

- Title: *SGDRC: Software-Defined Dynamic Resource Control for Concurrent DNN Inference on NVIDIA GPUs* `[paper]`
- Authors: Yongkang Zhang, Haoxuan Yu (HKUST); Chenxia Han (CUHK); Cheng Wang (Alibaba Group, Shenzhen); Baotong Lu (Microsoft Research, Beijing); Yunzhe Li (Shanghai Jiao Tong University); Zhifeng Jiang (HKUST); Yang Li (China University of Geosciences, Wuhan); Xiaowen Chu (HKUST Guangzhou); Huaicheng Li (Virginia Tech) `[paper]`
- Venue: PPoPP '25, Las Vegas, NV, 1–5 March 2025. DOI `10.1145/3710848.3710863` `[census/PPoPP_2025.md]` `[official-web]`
- Publication type: `ARCHIVAL_MAIN_PAPER`
- Full text used: https://people.cs.vt.edu/~huaicheng/p/ppopp25-sgdrc.pdf (author-hosted) `[paper]`
- **Naming/versioning note, recorded rather than resolved:** arXiv `2407.13996` is listed in search results under the SGDRC title, but the HTML of `arxiv.org/html/2407.13996v1` renders as ***Missile: Fine-Grained, Hardware-Level GPU Resource Isolation for Multi-Tenant DNN Inference***, same first author and overlapping author list, same three-layer mechanism (libsmctrl TPC control, shadow page table, VRAM-channel coloring), plus an additional **PCIe Completely Fair Scheduler** component and a wider GPU set (V100, P40, RTX A2000, RTX A5500) that the PPoPP paper does not carry. `[paper]` The safe statement: **the arXiv record and the PPoPP paper are the same line of work under two titles, and the arXiv version is the larger one.** Which version is "v1" versus a later retitling is `UNRESOLVED` — `arxiv.org/abs/2407.13996` did not return its version history to this environment. Numbers below are taken from the PPoPP PDF unless explicitly marked as arXiv/Missile.
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` in this pass → all implementation symbols below are `[paper]`-sourced, and no repository commit is asserted. Code symbols quoted are those the paper names.

## 12.2 Core question (one sentence)

On the mid- and low-end NVIDIA GPUs that have no MIG at all, can hardware-grade isolation between a latency-sensitive and a best-effort DNN inference tenant be reconstructed purely in software — by masking which TPCs each kernel may land on, and by colouring which VRAM channels each tensor may occupy? `[paper]`

## 12.3 GPU/HPC problem translation

- **Scheduling / partitioning (primary).** Which SMs (TPCs) a kernel's CTAs may be placed on, decided per launch and adjusted over a sliding window.
- **Memory (co-primary, and the distinctive axis).** Not memory *capacity* but **VRAM channel bandwidth**. SGDRC's claim is that compute isolation without channel isolation is insufficient: MPS "statically partitions GPUs at the thread slice level and cannot isolate VRAM bandwidth, resulting in unmanaged contention among colocated services". `[paper]`
- **Compute.** Kernels are rewritten into persistent-thread style so that the hardware CTA scheduler cannot undo the TPC masking decision.
- **Synchronization.** A software preemption point is introduced where the hardware has none: a BE kernel polls an eviction flag in global memory with `ld.cv`. `[paper]`
- **Communication.** In the arXiv/Missile version only, the PCIe bus is treated as a third contended resource and time-sliced at 1 KiB packet granularity. `[paper]` (arXiv version)

## 12.4 Why the problem exists (hardware root cause)

Four separate root causes, each named with its hardware reason:

1. **MPS partitions the wrong thing.** MPS's control is over *thread slices* (the active-thread-percentage knob) and it is static; it has no notion of memory channels. Co-located tenants therefore contend invisibly in the memory system. `[paper]`
2. **MIG exists only on flagship parts, is too coarse, and cannot be changed while busy.** "MIG fully isolates compute units and VRAM bandwidth, [but] it is available only in a few flagship GPUs (e.g., A100 and H100) but not in other low-end GPUs (e.g., Tesla T4)", "its granularity is too coarse (e.g., up to 7 instances of 10 GiB for A100) and can only reconfigure the allocation when it is idle". `[paper]` This is the cleanest statement in this cluster of *why* a software-partitioning school exists at all.
3. **GPU kernels are non-preemptive.** There is no timeslice preemption point in a running kernel, so a latency-sensitive arrival cannot displace a resident best-effort kernel by any hardware means. SGDRC manufactures one in software (the eviction flag). `[paper]`
4. **The memory-channel hash is undocumented and not a pure XOR.** The prior software-partitioning system FGPU "assumes that the GPU L2 cacheline and DRAM bank hash mapping functions are pure XOR functions. We attempted to reverse engineer other GPUs using FGPU's approach, but all failed because this assumption does not hold for many NVIDIA GPUs." `[paper]` The closed driver/hardware interface is itself the root cause of the paper's most expensive component.

A fifth, quantitative root cause is aimed at the nearest competitor: under Orion, as LS load rises the LS service keeps its SLO but BE throughput collapses, because "73.8% of their kernels are subjected to at least one constraint". `[paper]` Orion's interference control is therefore a throughput tax on the BE tenant, not an isolation boundary.

## 12.5 Mathematical / performance model

No closed-form model. The design is a set of allocation rules with tunable ratios:

- **Compute allocation.** "SGDRC allocates $SM_{LS}$ TPCs to each LS kernel, which is the minimum number of TPCs required to achieve the lowest latency for LS kernels", determined by offline profiling. `[paper]` The reservation is computed over a **sliding window**: "the number of SMs reserved for the next LS kernel is the maximum number of SMs required by LS kernels in the sliding window." `[paper]` That max-over-window is the whole adaptivity mechanism — a conservative envelope rather than a prediction.
- **Memory allocation.** The BE tenant is confined to a fraction $Ch_{BE}$ of VRAM channels, with **coloring granularity 2 KiB and $Ch_{BE} = 1/3$** in the evaluated configuration; both are stated to be tunable but are not tuned, because "there are only a few valid values for Tesla P40 and RTX A2000". `[paper]`
- **Channel structure discovered by the reverse engineering.** "each contiguous 1 KiB of physical VRAM space belongs to the same VRAM channel (i.e., a channel partition). The mapped VRAM channel IDs of contiguous channel partitions form an *m*-permutation." `[paper]` This *m*-permutation structure is the paper's substantive hardware finding and is what makes colouring at 1–4 KiB feasible at all.
- **Cost of the index translation.** "each re-indexing operation requires 2 integer operations, 8 GPU cycles". `[paper]`

## 12.6 Data layout and ownership

- **thread → warp → CTA:** CTAs are rewritten into persistent threads so that a fixed, known number of resident blocks — not the hardware scheduler — determines placement. `[paper]`
- **CTA → TPC:** ownership is set by the **Task Meta Data** field that `libsmctrl` writes: the library "manipulates Task Meta Data (TMD, an NVIDIA-specific, little-known interface), to control the set of TPCs to which each launched kernel can be assigned." `[paper]` Ownership here is *per kernel launch*, which is finer in time than MIG (per reconfiguration) and finer in space than MPS (per process).
- **Tensor → VRAM channel:** a tensor's pages are drawn from colour-specific free lists. The mechanism is the **shadow page table (SPT)**: "the mapping between the array index and the offset in `reserved_memspace`". `[paper]` (arXiv version phrasing; the PPoPP version describes the same object.) Steps named by the paper: divide each 4 KiB page into sectors; label each sector's colour from the lookup table; reserve a memory pool **in the `nvidia-uvm` kernel module** with per-colour linked lists of *n* KiB chunks; write each chunk's physical page frame number into the GPU page table; rewrite array indices in the kernel so tensors land on same-colour sectors. `[paper]`
- **Tensor → two copies (bimodal tensors):** for each memory-bound BE tensor SGDRC keeps "2 copies: 1) one mapped to all VRAM channels; and 2) one mapped to $Ch_{BE}$ of the VRAM channels". `[paper]` Ownership of bandwidth thus switches by *switching which copy is used* — **monopolization** state when the LS tenant is idle, **colocation** state when it is not. This is the mechanism by which a static colouring becomes a dynamic bandwidth allocation, and it costs memory capacity (a duplicate of every memory-bound BE tensor).

## 12.7 Pseudo code

Component names, the eviction-flag mechanism, the sliding window, the index-translation macro and the SPT steps are `[paper]`; arrangement is `[reconstruction]`.

```
# Offline                                                            # [paper]
for each DNN:
    compile with TVM -> fused CUDA kernels                           # [paper]
    transform large-grid kernels into persistent-thread style        # [paper]
    rewrite tensor indices:                                          # [paper] verbatim macro
        #define translate(offset) ((offset) + ((offset)&0xFFFFFE00))
        C[translate(i)] = A[translate(i)] + B[translate(i)];
    nvcc -> cubin                                                    # [paper]
    profile SM_LS = min TPCs for lowest LS-kernel latency            # [paper]
    label memory-bound tensors                                       # [paper]

# Reverse engineering (one-off, per GPU)                             # [paper]
collect 15K physical-address -> VRAM-channel samples   (~1 month)    # [paper]
train DNN to fit the (non-linear) channel hash                       # [paper]
batch-infer a lookup table                              (~1 hour)    # [paper]
# accuracy: >99.9% of channel IDs on unseen physical addresses       # [paper]

# Online                                                             # [paper]
on LS kernel arrival:
    SM_reserve = max over sliding window of SM_LS                    # [paper]
    libsmctrl: mask LS kernel to SM_reserve TPCs                     # [paper]
    set eviction flag in global memory                               # [paper]
    switch BE memory-bound tensors: monopolization -> colocation     # [paper]
on BE persistent kernel:
    poll eviction flag with ld.cv ; yield its TPCs when set          # [paper]
when LS idle:
    switch BE tensors back to monopolization (all channels)          # [paper]
```

## 12.8 Real implementation

No public artifact was located → `NOT_FOUND_AFTER_SEARCH`; **no repository, commit or file path is asserted.** The symbols and components the paper itself names, which are therefore safe to record:

- **`libsmctrl`** — third-party library, cited by the paper as reference [7], used to write TMD and thereby restrict a launch's TPC set. `[paper]`
- **`ld.cv`** — the PTX load instruction used to poll the eviction flag (a cache-bypassing/volatile load, which is what makes the flag visible promptly to a resident kernel). `[paper]`
- **`nvidia-uvm`** — the NVIDIA kernel module SGDRC modifies to reserve the coloured memory pool and maintain per-colour chunk lists. `[paper]` In the arXiv/Missile version an added driver entry point is named: **`GetPhysAddrFromVirtAddr`**, roughly 100 LOC in `nvidia-uvm`, which parses the page-table entry for a queried virtual address, using `uvm_page_table_range_entry_address`. `[paper]` (arXiv version)
- **`translate()`** — the index-rewriting macro quoted verbatim in 12.7. `[paper]`
- **TVM** — the DNN compiler that generates the kernels SGDRC is allowed to rewrite; `nvcc` produces the cubins. `[paper]` The paper also names MLIR and Triton as acceptable front ends. `[paper]`
- Scale of driver change (arXiv version): "~1K LOC to reverse-engineer VRAM channels", described as deliberately minimal. `[paper]` (arXiv version)

## 12.9 Kernel execution

This is where SGDRC differs most from every MIG/MPS system in this cluster, so it is worth being precise about the chain:

1. **kernel → TPC set.** The launch's TMD carries a TPC mask; the hardware CTA scheduler may only place this kernel's CTAs on the unmasked TPCs. Granularity is the **TPC** (a pair of SMs on the evaluated parts), not the SM. `[paper]`
2. **TPC → resident CTAs.** Because the kernel is persistent-thread style, the number of CTAs equals the number of slots the mask allows, and they stay resident. The paper's stated reason: this "reduce[s] conflicts caused by the GPU hardware scheduler". `[paper]` Without it, a large-grid kernel's later waves would be scheduled by hardware after the mask decision was made, and the partition would drift.
3. **CTA → preemption.** Each persistent BE CTA polls the eviction flag with `ld.cv`; on seeing it set, the CTA exits, freeing its TPC for the LS kernel. `[paper]` **This is a cooperative, software preemption point with kernel-author cooperation as its precondition** — which is exactly why SGDRC cannot handle closed-source vendor kernels (12.13).
4. **instruction level.** Each rewritten memory reference pays 2 integer ops / 8 cycles for `translate()`. `[paper]`

## 12.10 Memory traffic

SGDRC's central object *is* memory traffic, at the channel level:

- Physical VRAM is partitioned into 1 KiB channel partitions whose channel IDs form an *m*-permutation across contiguous partitions. `[paper]`
- Colouring is applied at **2 KiB** granularity in the evaluated setting (the mechanism supports 1–4 KiB). `[paper]`
- The BE tenant's memory-bound tensors are confined to **1/3 of channels** while the LS tenant is active, and released to all channels when it is not (bimodal tensors). `[paper]`
- Effect on the LS tenant, with its qualifiers intact: **"For all LS kernels, on Tesla P40 and RTX A2000, SGDRC's VRAM channel isolation reduces p99 latencies … by 28.7% and 47.5% on average and by up to 135% and 106.3%, respectively"** — LS models being MobileNetV3/SqueezeNet/ShuffleNet/EfficientNet/ResNet34/MobileBert/MobileViT/EfficientFormer under the Baidu Apollo trace, against SGDRC without channel isolation. `[paper]` (The ">100%" reduction figures are as printed in the paper; they are not re-derived here.)
- Cost: "the overhead of SPT is 2.9% on average" and "the end-to-end DNN inference time (including CPU-side operations) increases by ∼0.5% on average". `[paper]`

## 12.11 Why it is faster/slower (decomposed)

Against **Orion** on **Tesla P40**, with LS/BE model sets as listed and the Apollo trace: "improves overall throughput by up to 1.47× and BE job throughput by up to 2.36×", at "99.0% on average" SLO attainment. `[paper]` The decomposition:

- **Orion constrains kernels; SGDRC constrains placement.** Orion throttles BE kernels that would interfere (73.8% of them hit at least one constraint `[paper]`), which suppresses BE throughput directly. SGDRC instead gives the BE tenant a *smaller but unthrottled* region of the machine — fewer TPCs and one third of the channels — so BE work runs at full rate inside its region.
- **The LS gain comes from the memory side, not the compute side.** The channel-isolation ablation is what moves LS p99 (28.7% / 47.5% average on P40 / A2000 `[paper]`). Compute masking alone does not fix LS tail latency, because the contention that was hurting it was in the memory channels.
- **The BE gain comes from bimodal tensors.** Without the two-copy scheme the BE tenant would be permanently confined to $Ch_{BE}$; with it, BE reclaims all channels during LS idle periods. `[paper]`
- **Costs paid:** an extra copy of every memory-bound BE tensor (capacity), 8 cycles per rewritten access (instruction), 2.9% SPT overhead, and a one-month per-GPU reverse-engineering campaign. `[paper]`

## 12.12 Hardware generation dependence

Severe, and the paper says so:

- The channel hash must be re-learned **per GPU model**: 15K samples, one month of collection, a trained DNN, a generated lookup table. `[paper]`
- Evaluated on **Tesla P40 (Pascal, 12 VRAM channels, 24 GiB)** and **RTX A2000 (Ampere, 6 VRAM channels, 12 GiB)**. `[paper]` The arXiv/Missile version adds V100 and RTX A5500. `[paper]` (arXiv version)
- **A100/H100 break the method's assumption**: "the L2 caches in A100 and H100 consist of multiple separate caches, making their L2 caches a hybrid of UMA and NUMA. Consequently, SGDRC's reverse engineering approach will require slight adaptation for NVIDIA A100 and H100." `[paper]` So the software-partitioning school is, today, evaluated on exactly the parts where the hardware school (MIG) is unavailable, and vice versa. **The two schools have not been compared on the same silicon anywhere in this cluster.**
- `libsmctrl`/TMD is an undocumented NVIDIA interface; its continued existence across driver versions is not guaranteed by anything. `[inference]`

## 12.13 Limitations

- **Closed-source kernels are out of scope.** "CUDA kernels of other GPU tasks may originate from closed-source vendor libraries (e.g., cuDNN, Cutlass, and cuBLAS) and CUDA binaries, which are not currently compatible with SGDRC." `[paper]` This is the decisive practical limitation: SGDRC requires source-level cooperation from every co-located tenant, which MIG does not.
- **No fault isolation.** "SGDRC and these solutions cannot isolate colocated DNNs' GPU runtime errors". `[paper]`
- **Security.** The arXiv version concedes that decrypting the channel/L2 hash "could facilitate side-channel attacks". `[paper]` (arXiv version)
- **Parameters left untuned** (coloring granularity, $Ch_{BE}$) because the evaluated GPUs admit too few valid values. `[paper]`
- **No dynamic batching** in SGDRC or in any baseline. `[paper]`
- **Two-tenant framing.** The design is LS-vs-BE; generalisation to many symmetric tenants is not demonstrated. `[inference]` from the evaluation structure.
- **Reverse-engineering cost is per-SKU and enormous** (one month), which bounds deployability more than any performance number.

## 12.14 Relation to prior corpus

- **Competing school, same cluster:** `GPU-SC24-161` (ParvaGPU, SC 2024) is the exact opposite design choice — accept MIG's lattice and solve the packing problem; SGDRC rejects the lattice as too coarse and unavailable, and rebuilds partitioning in software. SGDRC's critique of MIG ("granularity too coarse … can only reconfigure when idle" `[paper]`) is independently corroborated by ParvaGPU's own artifact, whose reconfiguration script tears down all instances and kills MPS before re-creating them. `[code]` (ParvaGPU artifact, commit `5f3de1e…`). The two papers do not cite each other.
- **Corroborating hardware evidence, already analysed:** `GPU-MICRO24-02` (STAR, MICRO 2024) shows MIG leaves the last-level TLB shared across instances — an interference channel of the same *kind* SGDRC attacks (a shared structure below the partition boundary), but in translation rather than in VRAM channels. Read together, the two say the partition boundary is porous at more than one level.
- **Corroborating characterisation:** `GPU-ISC26-165` finds, on H100 MIG, a further residual interference channel — **power throttling** — that neither MIG nor SGDRC's channel colouring addresses.
- **Runtime/driver-interception school:** `GPU-ASPLOS26-163` (gShare) reaches isolation from below, in the kernel driver, with no kernel-source cooperation at all — the complementary extreme to SGDRC's source-level requirement.
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and covers serving; no claim is made about whether it holds SGDRC/Missile.
- **`domains/hpc_systems_operations/`:** checked; no MIG/MPS/sharing content in `topics/gpu_operations.md` or `topics/scheduling_resource_management.md`. No `GPU_DELTA_ANALYSIS` owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO — and this is the strongest NO in the cluster.**

verdict_basis: Every one of SGDRC's three mechanisms is defined by a specific NVIDIA hardware or driver property: (a) compute partitioning is performed by writing the **TPC mask in the Task Meta Data** via `libsmctrl`, an undocumented NVIDIA interface with no analogue on a CPU or a generic accelerator; (b) the preemption point exists only because **GPU kernels are non-preemptive**, forcing a cooperative eviction flag polled with the PTX `ld.cv` instruction inside persistent-thread CTAs; (c) the memory mechanism rests on a reverse-engineered, **non-linear, per-SKU VRAM-channel hash** whose 1 KiB-partition *m*-permutation structure is a property of NVIDIA memory systems, and it is realised by modifying the `nvidia-uvm` kernel module. `[paper]` On a CPU, cache/DRAM page colouring is a solved and documented technique and core affinity is an OS primitive — the paper would not exist.

**Isolation mechanism: software SM partitioning at TPC granularity (TMD masks via `libsmctrl`) + persistent-thread kernels + cooperative eviction flag + VRAM-channel page colouring through a modified `nvidia-uvm`. Explicitly *not* MIG and *not* MPS.** `[paper]`

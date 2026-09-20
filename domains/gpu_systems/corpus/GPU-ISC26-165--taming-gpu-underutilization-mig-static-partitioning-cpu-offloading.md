# GPU-ISC26-165 — Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `K — GPU sharing / MIG / MPS / co-location (characterisation)`
secondary_topics: `J — GPU runtime and scheduling; D — GPU virtual memory / CPU-GPU coherent offloading; power and throttling`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `abstract; introduction/motivation; background on MIG as a hardware partitioning mechanism; the MIG profile table for a 96 GB H100 (Table II) with per-profile SM and memory figures; the application table (Table III); the memory-offloading proposal over NVLink-C2C; methodology incl. hardware/software stack and the metric set; selected characterisation results (SM occupancy and memory-underutilisation figures). Read via one full-text pass over arxiv.org/html/2604.08451v1. **The full results section, per-application energy/throughput tables, the ablation and the related-work section were NOT returned by that pass** and are recorded as NOT_READ; only the numbers explicitly quoted below are asserted.`

## 12.1 Bibliographic facts

- Title: *Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading* `[paper]`
- Authors: Gabin Schieffer, Ruimin Shi (KTH Royal Institute of Technology, Stockholm); Jie Ren (William & Mary, Williamsburg); Ivy Peng (KTH Royal Institute of Technology) `[paper]`
- Venue: recorded as **ISC 2026** in this project's assignment. **`MEMBERSHIP_UNVERIFIED`** — `census/ISC_2026.md` states explicitly that no source read states this is an ISC 2026 research paper, and the arXiv HTML pass returned no venue note. Treat the venue as unconfirmed; the paper itself is not in doubt. `[census/ISC_2026.md]`
- Publication type: `PREPRINT` (arXiv) pending venue confirmation.
- DOI: `UNKNOWN`.
- Full text used: https://arxiv.org/abs/2604.08451 → https://arxiv.org/html/2604.08451v1 `[paper]`
- Artifact/code: `NOT_FOUND_AFTER_SEARCH` → `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Does MIG actually fix GPU underutilisation for *real HPC and AI applications* on an H100, and where does its fixed-size slicing still mismatch what applications need — and can a cache-coherent CPU–GPU link be used to bridge the gap when a workload is slightly too large for a slice? `[paper]`

## 12.3 GPU/HPC problem translation

- **Scheduling / partitioning (primary).** The paper's subject is the *granularity mismatch* between MIG's fixed slice sizes and applications' actual resource demands, measured rather than assumed.
- **Compute.** SM occupancy is the primary measured quantity, and the paper separates it from SM *utilisation*: "SM utilization metric, which reports the percentage of time that SM are busy in the sampling period. In addition, we collect the more granular SM occupancy metrics". `[paper]` That distinction matters — a kernel can keep SMs busy while occupying few warp slots, and only the second is evidence of wasted capacity.
- **Memory.** Capacity underutilisation is measured separately from bandwidth, and the proposed mechanism acts on capacity.
- **Power (the paper's distinctive finding).** Interference survives MIG: "interference still occurs through shared resources, such as power throttling". `[paper]`
- **Communication.** NVLink-C2C between Grace CPU and Hopper GPU is the offload path.

## 12.4 Why the problem exists (hardware root cause)

1. **MIG couples compute and memory in fixed ratios.** "An instance comprises of a portion of the GPU's compute resources and a portion of the GPU's memory resources." `[paper]` An application that is memory-hungry but SM-light, or the reverse, cannot be served without waste. The paper states the general finding: "coarse-grained provisioning for tightly coupled compute and memory resources often mismatches application needs." `[paper]`
2. **The lattice on a 96 GB H100 is small and non-proportional.** From Table II `[paper]`:

   | Profile | Max instances | Usable SMs | Memory |
   |---|---|---|---|
   | `1g.12gb` | 7 | 16 | 11 GB |
   | `2g.24gb` | 3 | 32 | 23 GB |
   | `3g.48gb` | 2 | 60 | 46.5 GB |
   | `4g.48gb` | 1 | 64 | 46.5 GB |
   | `7g.96gb` | 1 | 132 | 94.5 GB |

   Two structural facts fall out that matter for the whole cluster. **The SM counts are not proportional to the profile number**: 7×16 = 112 SMs, not 132 — roughly 15% of the SMs are unavailable when the GPU is fully sliced into seven. And **`3g.48gb` and `4g.48gb` carry the same memory (46.5 GB) with different SM counts (60 vs 64)**, so the compute:memory ratio is not even monotone across the lattice.
3. **Partition changes are offline.** "The static configuration in MIG is a known limitation, as changing the MIG configuration is not possible while GPU applications are running." `[paper]` This is the third independent confirmation of the same fact in this cluster (cf. SGDRC's "can only reconfigure the allocation when it is idle" and ParvaGPU's artifact tearing down all instances before `-cgi`).
4. **Power is not partitioned.** The GPU's power and clock domain is device-wide; MIG partitions SMs and memory slices but nothing prevents one instance's power draw from causing a throttle that all instances feel. This is the paper's own finding and it is a *hardware* root cause that no MIG-based scheduler in this cluster accounts for.
5. **Applications genuinely leave SMs idle even with the whole GPU.** Measured examples: NekRS at "12% to 25% SM occupancy" across configurations; Hotspot at "60% SM occupancy" on the full GPU; LAMMPS at "40% SM occupancy" on the full GPU. `[paper]` (These are SM-occupancy figures on the H100 96 GB described in 12.12, and must not be quoted without that qualifier.)

## 12.5 Mathematical / performance model

No analytic model. The study is a **performance–resource scaling characterisation**: each application is run under each MIG profile (and under full-GPU, time-slicing and MPS) and its throughput, occupancy, memory usage, bandwidth, power, clock and throttling state are recorded. `[paper]` The offloading proposal is likewise empirical rather than modelled.

Reported aggregate effects, with their qualifiers:
- Sharing raises occupancy for some codes: "AutoDock variants show SM occupancy nearly doubled under sharing". `[paper]`
- Memory-capacity waste falls under sharing: "seven cases see reduced memory underutilization, by 20-60%". `[paper]`
- Direction of the headline claim: MIG "can significantly reduce resource underutilization, and enable system-level improvements in throughput and energy" — but with interference persisting through power throttling. `[paper]` The per-application throughput and energy tables were **NOT_READ**.

## 12.6 Data layout and ownership

- **thread → warp → SM:** ownership is by MIG instance; the instance's usable SM count is fixed by the profile (16/32/60/64/132 on the 96 GB H100). `[paper]`
- **SM → GPC → instance:** MIG's slice boundary. The non-proportionality noted in 12.4 means a slice's SMs are not simply 1/7 of the device.
- **Instance → memory slice:** 11 / 23 / 46.5 / 46.5 / 94.5 GB. `[paper]` Memory is *not* independently sizable — that is precisely the gap the offloading scheme targets.
- **GPU → CPU (the new edge):** NVLink-C2C on the Grace Hopper superchip, "a cache-coherent 'chip-to-chip' interconnect … up to 450 GB/s bandwidth in each direction". `[paper]` The host's 512 GB of LPDDR5X becomes a spill target reachable coherently.
- **Power domain:** device-wide, *not* partitioned — the ownership boundary MIG does not draw. `[paper]`

## 12.7 Pseudo code

The offloading scheme, as the paper describes it `[paper]`; arrangement `[reconstruction]`:

```
# Goal: run a workload whose footprint slightly exceeds a MIG slice
# without promoting it to the next (much larger) slice.          # [paper]

choose smallest MIG profile p with SMs(p) sufficient             # [paper] intent
if footprint(app) > memory(p):
    allocate the overflow with a spilling allocator:
        cudaMallocManaged(...)   # coherent, migratable          # [paper] named
        or  malloc(...)          # host LPDDR5X, reached over C2C# [paper] named
    # NVLink-C2C carries the accesses coherently at up to
    # 450 GB/s per direction                                     # [paper]
```

The paper states the implementation scope plainly: "We implement such offloading strategy for three of the applications … by using a memory allocator that supports spilling out of GPU memory, namely `cudaMallocManaged` or `malloc`." `[paper]` **Three applications, not the full set** — this is a proof of concept, not a system.

## 12.8 Real implementation

No artifact located → `NOT_FOUND_AFTER_SEARCH`; no repository or commit asserted.

Stack, as stated `[paper]`:
- **GPU:** "Nvidia H100 GPU integrated in a Grace Hopper system … 96 GB of HBM3 memory, and features 132 SMs".
- **CPU:** "72-core Arm Neoverse-V2 CPU, equipped with 512 GB of LPDDR5X memory".
- **Software:** "CUDA runtime 12.4, Nvidia GPU driver version 550.54.15, and Linux kernel 5.14.0".
- **Only API symbols named:** `cudaMallocManaged`, `malloc`. No custom runtime or driver component is claimed.
- **Applications (Table III):** Qiskit (quantum simulation), FAISS (data analytics), NekRS (CFD), LAMMPS (molecular dynamics), AutoDock-GPU (molecular docking), LLM training (GPT-2), LLM inference (Llama3), Rodinia hotspot, STREAM-Nvlink, STREAM-GPU. `[paper]`
- **Sharing modes compared:** full GPU (no sharing), time-slicing, MPS, and MIG configurations including "7×1g" and "7×1c.7g". `[paper]` The `1c.7g` form is a **compute-instance** subdivision within a single 7g GPU instance — a distinct MIG concept from a GPU instance, and its inclusion means the study covers both levels of MIG's hierarchy.

## 12.9 Kernel execution

No kernel-level mechanism is contributed. What the paper establishes about kernel execution under partitioning:
- An application's CTAs are confined to its instance's SMs (16 at `1g.12gb`), so occupancy is bounded by the slice, and a code that already fails to fill 132 SMs (NekRS at 12–25%) may fill 16 much better — that is the utilisation gain.
- The `1c.7g` configuration additionally partitions *compute instances* within one GPU instance, sharing the instance's memory slice — a finer compute cut with no memory cut. `[paper]`
- No warp-scheduler or occupancy-limiter analysis is offered → `NOT_IN_PAPER`.

## 12.10 Memory traffic

- **Capacity** is the managed quantity: the offloading scheme moves allocations out of HBM3 into host LPDDR5X across NVLink-C2C.
- **Bandwidth asymmetry is the risk the paper implicitly takes on**: HBM3 on H100 is roughly an order of magnitude faster than the 450 GB/s-per-direction C2C link, so spilled data is far more expensive per access. The paper's framing — spill only what is needed to fit a workload "slightly larger than a MIG slice" `[paper]` — is the mitigation. Quantified sensitivity of each application to the spill fraction was **NOT_READ**.
- STREAM-Nvlink and STREAM-GPU are in the application table precisely to calibrate the two bandwidth domains. `[paper]`
- Measured metric set includes "memory capacity usage and bandwidth usage" alongside "GPU power draw, GPU clock frequency, and GPU throttling information". `[paper]`

## 12.11 Why it is faster/slower (decomposed)

- **Gains come from filling otherwise-idle SMs.** Codes with low occupancy on the full GPU (NekRS 12–25%, LAMMPS 40%, hotspot 60% `[paper]`) can be packed several-to-a-device; occupancy roughly doubles for AutoDock variants under sharing `[paper]`.
- **Gains also come from reclaiming stranded memory**: 20–60% reduction in memory underutilisation in seven cases. `[paper]`
- **Losses come from a channel MIG does not isolate: power.** Because the power/clock domain is device-wide, a co-tenant that pushes the GPU into throttling slows every instance. This is the finding that distinguishes this paper from the many "MIG improves utilisation" results, and it is a caution that applies directly to `GPU-SC24-161` and to SMART-MIG (IPDPS 2026; watchlist, no deep analysis in this corpus — an earlier draft cited a non-existent `GPU-IPDPS26-166`, corrected 2026-09-19), both of which assume MIG-instance performance is independent of what else runs on the device.
- **The offloading scheme trades bandwidth for slice size**: paying C2C latency/bandwidth on part of the footprint in exchange for not promoting the job to a slice with 2× the SMs it needs.

## 12.12 Hardware generation dependence

- **Everything is H100-96GB-and-Grace-Hopper specific.** The profile table (`1g.12gb` … `7g.96gb`, 16/32/60/64/132 SMs, 11/23/46.5/94.5 GB) is that SKU's. `[paper]` Compare `GPU-SC24-161`, whose A100 lattice is expressed in GPC counts 1/2/3/4/7 with 5 and 6 unavailable and 10/20/40/80 GB — a *different* lattice with different non-proportionalities. Any MIG scheduler tuned to one is not portable to the other.
- **The offloading mechanism requires NVLink-C2C**, i.e. a Grace Hopper (or successor) superchip. On a PCIe-attached H100 the same scheme would run over PCIe at roughly an order of magnitude less bandwidth and without cache coherence, and the paper's premise would not hold. `[inference]` — the paper does not evaluate a PCIe baseline → `NOT_IN_PAPER`.
- Driver 550.54.15 / CUDA 12.4 pin the MIG behaviour observed. `[paper]`

## 12.13 Limitations

- **Static configuration** — MIG cannot be reconfigured while applications run. `[paper]`
- **Offloading demonstrated for three applications only.** `[paper]`
- **Venue unconfirmed** (`MEMBERSHIP_UNVERIFIED`, per this project's census). `[census/ISC_2026.md]`
- **No artifact** → results not independently reproducible from here.
- **Characterisation, not a system.** There is no scheduler, no policy and no runtime; the offloading proposal is a manual allocator substitution.
- **Results section not read in this pass** → per-application throughput/energy claims must not be quoted from this file.

## 12.14 Relation to prior corpus

- **Empirical foundation for the MIG schedulers in this cluster.** `GPU-SC24-161` (ParvaGPU) optimises placement *within* the A100 lattice and SMART-MIG (IPDPS 2026; watchlist, no deep analysis here) learns a repartitioning policy; both assume a MIG instance's performance is a function of its own profile. This paper measures the H100 lattice directly and finds a residual cross-instance channel — **power throttling** — that falsifies that assumption in part. It is the most useful single cross-check available to either.
- **Second independent falsification of MIG isolation:** `GPU-MICRO24-02` (STAR, MICRO 2024, already analysed by the memory cluster) shows the **last-level TLB is shared across MIG instances**, with co-running tenants losing 40% on average versus isolation. Taken together: MIG isolates SMs and memory slices, but not the L3 TLB (STAR) and not the power/clock domain (this paper). **That pair is the strongest statement this corpus can make about the limits of hardware GPU partitioning.**
- **Opposing school:** `GPU-PPoPP25-164` (SGDRC) rejects MIG for exactly the reason this paper measures — coarse granularity and offline reconfiguration — and rebuilds partitioning in software. This paper is the quantitative case for SGDRC's premise, produced independently and on the hardware where MIG *is* available.
- **Memory-offload lineage:** `GPU-ISC24-01` (porting HPC applications to MI300A unified memory with OpenMP) and `GPU-SC24-82` (Hydrogen, contention-aware hybrid CPU-GPU memory) are the nearest corpus neighbours for the C2C spilling idea; the novelty here is using coherent spilling *as a partition-granularity workaround* rather than as a capacity extension.
- **Utilisation context:** `GPU-IPDPS26-41` reports the same underutilisation at production-cluster scale.
- **External corpus:** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` — no claim about `domains/ai_hpc_systems/`.
- **`domains/hpc_systems_operations/`:** checked; no MIG/sharing content. No `GPU_DELTA_ANALYSIS` owed.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The object of study is **MIG's fixed partition lattice on a specific GPU** — the enumerated profiles `1g.12gb`/`2g.24gb`/`3g.48gb`/`4g.48gb`/`7g.96gb` with their non-proportional SM counts (16/32/60/64/132 out of 132) and coupled memory slices — together with MIG's inability to be reconfigured while work is running. `[paper]` The finding that matters (interference persists through **power throttling** despite SM and memory-slice isolation) is a statement about a GPU's device-wide power/clock domain. The proposed remedy depends on **NVLink-C2C cache-coherent CPU–GPU attachment at 450 GB/s per direction**. None of these objects exists on a CPU; on a generic accelerator without a fixed partition lattice the paper has no question to ask.

**Isolation mechanism: MIG (hardware partitioning), compared against MPS, time-slicing and full-GPU baselines, with a proposed NVLink-C2C memory-offload escape hatch for slice-size mismatch. Finding: MIG does not isolate power.** `[paper]`

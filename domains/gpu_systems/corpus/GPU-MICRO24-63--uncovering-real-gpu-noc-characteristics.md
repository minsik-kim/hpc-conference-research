# GPU-MICRO24-63 — Uncovering Real GPU NoC Characteristics: Implications on Interconnect Architecture

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `B — GPU on-chip interconnect / NoC structure; SM-to-L2 fabric, GPC/TPC clustering, partitioned dies` *(letter per this cluster's task assignment; no A–Q taxonomy file exists in the repository — `NOT_IN_REPOSITORY`)*
secondary_topics: `A — SM/core placement and its effect on memory latency; N — GPU simulator fidelity (NoC and L2-bandwidth modelling); side-channel implications of NoC non-uniformity`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER` — motivation (idealised-NoC assumptions in simulation), microbenchmark methodology (Algorithms 1 and 2, `smid` pinning, `-dlcg=cg` L1 bypass, `clock()`, nvprof per-slice counters, correlation-based placement inference), discovered topology and latency/bandwidth characteristics on V100/A100/H100, the CPC finding, interface-vs-bisection-bandwidth argument, the 6×6-mesh contrast experiment, prior-work configuration survey (Fig. 22), limitations, related work. **§ on side-channel implications: `PARTIALLY_READ` — its existence and the randomised-scheduling caveat were read, the mechanism was not.** **No artifact/code repository located — `NOT_INSPECTED`.**

## 12.1 Bibliographic facts

- **Title** [paper]: *Uncovering Real GPU NoC Characteristics: Implications on Interconnect Architecture*.
- **Venue** [census]: MICRO 2024, Session 6B "Networks-on-Chip". `ARCHIVAL_MAIN_PAPER`. The PDF does not print the venue; venue and DOI from `domains/gpu_systems/census/MICRO_2024.md`.
- **DOI** [census]: `10.1109/MICRO61859.2024.00070`.
- **Authors** [paper]: Zhixian Jin, Christopher Rocca, Jiho Kim, Hans Kasan, Minsoo Rhu (KAIST); Ali Bakhoda (Microsoft, Bellevue WA); Tor M. Aamodt (University of British Columbia); John Kim (KAIST).
  - Note: **Ali Bakhoda** is the author of the prior throughput-effective GPU NoC work the paper revises, and **Tor Aamodt** is a GPGPU-Sim originator — i.e. the paper is partly a self-correction by the people who wrote the model being corrected.
- **Access** [official-web]: author PDF `people.ece.ubc.ca/aamodt/publications/papers/realgpu-noc.micro2024.pdf`, fetched 2026-09-18.
- **Artifact**: `NOT_FOUND_AFTER_SEARCH` per census; none located. `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

What is the on-chip network of a real NVIDIA GPU actually shaped like, and how much of the published GPU-NoC design literature is solving a problem created by the simulator's 2D-mesh assumption rather than by the hardware? [paper]

## 12.3 GPU/HPC problem translation

**Communication** (on-die), with a **methodology** payload and a **scheduling** consequence.

The paper's object is the SM→L2 fabric. It reframes what the design target should be: prior GPU-NoC work optimised **bisection bandwidth**, while the real constraint is **interface bandwidth** — the bandwidth of the connection between the network and the memory partitions [paper]. A simulator whose interface bandwidth is undersized relative to its memory bandwidth manufactures a "network wall" that does not exist in silicon; the paper surveys prior works' baseline configurations (its Fig. 22, plotted as memory bandwidth vs interface bandwidth) to show which papers sit in that regime.

## 12.4 Why the problem exists (hardware root cause)

[paper] Three structural facts, none of them in the standard model:

1. **The real fabric is a hierarchical crossbar, not a multi-hop mesh.** SMs cluster into TPCs, TPCs into GPCs, GPCs into the GPU. On A100 and H100 there is a further **central partition split (left/right)**.
2. **Latency is non-uniform and determined by physical placement** — "by the physical location of the SM within the GPC and the L2 slice within the memory partition". On V100 the average SM→L2 round trip is ≈212 cycles but ranges **175–248 cycles**, a 33% spread within a GPC; the paper reports up to a **70% difference** overall. On A100/H100, crossing the central partition costs ≈**400 cycles** versus ≈**200 cycles** locally.
3. **The traffic pattern is many-to-few-to-many**, with distinct request and reply networks. Prior work identified the reply network as the bottleneck but did so on idealised topologies.

The root cause of the *literature's* error is that a 2D mesh cannot deliver uniform bandwidth irrespective of node placement. The paper demonstrates this directly: with round-robin arbitration on a 6×6 mesh, "some nodes will receive much higher throughput, by up to 2.4×" [paper].

## 12.5 Mathematical / performance model

No closed-form model. The quantitative core is a measured characterisation [paper], and the numbers must always carry their SKU and their granularity qualifier:

| Quantity | Value | Qualifier |
|---|---|---|
| SM→L2 round-trip latency, mean | ≈212 cycles | V100, single-thread-per-warp, L1 bypassed, L2 warm |
| SM→L2 round-trip latency, range | 175–248 cycles (33% spread) | V100, within a GPC |
| Partition-crossing latency | ≈400 cycles vs ≈200 local | A100/H100 |
| CPC-distance latency | 196–213 cycles | H100 |
| Bandwidth, one SM → one L2 slice | ≈34 GB/s (σ = 0.147) | measured |
| Bandwidth, one GPC → one L2 slice | ≈85 GB/s (σ = 0.06) | measured |
| Far- vs near-partition bandwidth | ≈26 GB/s vs ≈39.5 GB/s | A100, few SMs; asymmetry vanishes at ≈8+ SMs |
| Aggregate L2 fabric bandwidth | 2.4–3.5× off-chip memory bandwidth | measured |

The last row is the paper's most consequential single number for simulator builders: **the on-chip fabric is provisioned well above HBM bandwidth**, so a model that bottlenecks L2 bandwidth at the network is wrong in kind, not just in degree.

The bandwidth uniformity result is equally important and cuts the other way from the latency result: "bandwidth provided to each L2 slice from the different cores (SMs) and GPCs are approximately similar" — the low σ values quantify it. **Real GPU NoCs are latency-non-uniform but bandwidth-uniform**; a mesh is neither.

## 12.6 Data layout and ownership

The paper's contribution *is* the ownership hierarchy [paper]:

```
thread -> warp -> SM
SM     -> TPC                       (several SMs per TPC)
TPC    -> [CPC]  -> GPC             (CPC: H100 only, newly identified here)
GPC    -> partition (left/right)    (A100, H100)
partition -> GPU
                 |
                 +-- hierarchical crossbar -->  memory partition -> L2 slice -> HBM channel
```

- The **CPC (Compute Processing Cluster)** between TPC and GPC on H100 is the paper's new structural finding. **It lacks official NVIDIA documentation** — existence inferred from latency-correlation patterns and hardware teardowns [paper], and the paper says so. Treat as `[inference]` by the authors, not vendor fact.
- Address→L2-slice mapping is a hash. On V100 the destination slice was identified with nvprof per-slice counters; **on A100/H100 those counters are unavailable**, so the hash was reversed manually by contention testing [paper].

## 12.7 Pseudo code

Reconstructed from the paper's Algorithms 1 and 2; flag names and register names are the paper's.

```
# --- Algorithm 1: isolate NoC round-trip latency -------------------------- [paper]
compile with  -dlcg=cg                  # bypass L1, so every access reaches L2
warm_L2(buffer)                         # guarantee L2 hits, exclude DRAM
pin kernel to a chosen SM               # read %smid, exit if not the target SM
use ONE thread per warp                 # no intra-warp coalescing, no queueing
t0 = clock();  v = *p;  t1 = clock()    # dependent load
latency[SM, L2_slice] = t1 - t0         # = SM pipeline + NoC + L2 hit

# --- Algorithm 2: per-path bandwidth ------------------------------------- [paper]
use all threads in warps, multiple thread blocks
sequential / strided access, destination L2 slice precomputed
bandwidth = bytes_transferred / execution_time

# --- placement inference -------------------------------------------------- [paper]
for each pair of SMs:  r = pearson(latency_profile[SM_i], latency_profile[SM_j])
cluster SMs by r  ->  TPC / CPC / GPC / partition membership
cross-check against die photographs
```

The design of Algorithm 1 is what makes the result trustworthy: bypassing L1, warming L2, and using a single thread per warp removes coalescing, MSHR queueing and DRAM from the measured quantity, leaving the fabric.

## 12.8 Real implementation

No artifact; **no `[code]` evidence — do not attribute symbols.**

Measurement stack [paper]: CUDA micro-kernels on real **V100, A100 and H100** hardware, `nvprof` and hardware counters, the `-dlcg=cg` compile flag, the `%smid` special register, `clock()`. CUDA/driver versions: `UNKNOWN`.

Simulation, used only as a *contrast*: a **network-only simulation of a 6×6 2D mesh with random traffic from 30 compute nodes to 6 memory controllers** [paper]. The simulator name is not stated in what was read — `UNKNOWN`. **This is the paper's only simulated component**; every characterisation number above is measured on real silicon.

## 12.9 Kernel execution

The paper does not modify execution; it makes execution *placement-sensitive*. The operative finding for kernel authors and for the hardware block scheduler [paper]:

> Load-balancing kernel execution across SMs is more critical than load-balancing L2 slices, because of the asymmetric NoC speedup.

That is a direct claim about CTA→SM assignment: which SM a thread block lands on changes its memory latency by up to 33% within a GPC and by ~2× across an A100/H100 partition boundary. The GPU's own block scheduler does not expose or guarantee this placement, so the effect is invisible to the programmer and unmodelled by the simulator.

## 12.10 Memory traffic

The paper characterises exactly the SM ↔ L2 leg of the hierarchy, and deliberately excludes the rest (L1 bypassed, L2 warm, DRAM excluded). Its statement about the leg below is a ratio, not a measurement of HBM: aggregate L2 fabric bandwidth is **2.4–3.5× off-chip memory bandwidth** [paper, V100/A100/H100].

The request/reply asymmetry matters here: the fabric is many-to-few in the request direction (many SMs → few memory partitions) and few-to-many in the reply direction, carrying wider payloads. Prior work (Bakhoda et al.) identified the reply network as the bottleneck; this paper's contribution is that the binding constraint is the **interface** to the memory partitions rather than the network's bisection [paper].

## 12.11 Why it is faster/slower (decomposed cause)

There is no proposed mechanism to be faster — this is a characterisation paper whose output is a set of corrections. Decomposed:

1. **Simulated GPU NoCs are slower than real ones for a structural reason**: a mesh's multi-hop distance makes bandwidth placement-dependent (up to 2.4× throughput spread under round-robin arbitration on a 6×6 mesh), whereas the real hierarchical crossbar delivers near-uniform per-SM and per-GPC bandwidth to each L2 slice (σ = 0.147 and 0.06 respectively).
2. **Simulated GPUs bottleneck at the network where real ones do not**, because the modelled interface bandwidth is undersized relative to modelled memory bandwidth. The paper's Fig. 22 survey places prior proposals on that plane.
3. **Real GPUs are slower than simulated ones in one respect the simulators miss**: latency non-uniformity of up to 70%, and a ~2× penalty for crossing the A100/H100 central partition. This is a real cost that no idealised model charges.
4. **The A100 far-partition bandwidth penalty is load-dependent** — ≈26 vs ≈39.5 GB/s with few SMs, vanishing at roughly 8 or more SMs [paper]. So a microbenchmark at low occupancy sees an asymmetry that a saturated application does not. This is a trap for anyone re-measuring.

## 12.12 Hardware generation dependence

- **Measured on real silicon**: NVIDIA **V100 (Volta), A100 (Ampere), H100 (Hopper)**. Everything in §12.5 is a measurement, not a simulation.
- Generation-specific structure: the **left/right central partition split** appears on A100 and H100 but not V100; the **CPC** level appears on H100 only. Do not carry a V100 latency figure to A100, or an A100 topology to H100.
- **Not covered**: Blackwell (B200/GB20x), AMD CDNA, or any multi-chiplet/MCM GPU. The hierarchy described is monolithic-die-with-partitions, which is *not* the same thing as a chiplet GPU; do not read the "partition" finding as a chiplet finding.
- The analysis is agnostic to tensor cores, TMA, DSM and thread-block clusters — none appear, and the H100 measurements should not be reused as evidence about them.

## 12.13 Limitations

Stated [paper]:
- **The reverse engineering is explicitly incomplete**: the authors "do not completely reverse-engineer the GPU NoC architecture or the memory hierarchy."
- **Per-L2-slice performance counters are unavailable on A100 and H100**, forcing a manual contention-comparison approach in place of the profiler-based method used on V100. The A100/H100 slice attributions therefore rest on weaker evidence than the V100 ones.
- **The CPC layer is unconfirmed by NVIDIA documentation**; it is inferred from correlation patterns and teardowns.
- **Workload evaluation is thin**: the analysis is driven by synthetic microbenchmarks, with only limited real-application validation (BFS and Gaussian).
- The side-channel defence discussed (randomised scheduling) is not established as secure — "remains to be seen if the proposed solution is fully secure against various timing side-channel attacks." **This section was only partially read; treat the side-channel content of this entry as `PARTIALLY_READ`.**

`[inference]`, not stated: latency measured with one thread per warp and a warm L2 is a *floor*; under real occupancy, queueing at the L2 slice and the memory partition will add to it, and the measured 33% placement spread may be either amplified or masked. The paper's own A100 near/far-bandwidth result (asymmetry vanishing above ~8 SMs) shows the sign of this effect is not obvious.

## 12.14 Relation to prior corpus

- `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Real GPU NoC" returns `domains/gpu_systems/census/MICRO_2024.md` (STEP A/B row), plus incidental substring hits in `GPU-IPDPS26-42` and `_LEDGER_profiling_reliability.md` that are not this paper.
- **Cited as a precursor by** `GPU-MICRO25-61` (Dissecting and Modeling Modern GPU Cores, MICRO 2025), which lists "Jin et al. (2024)" among the NoC reverse-engineering works it builds on [paper, MICRO'25 related work]. **This is a verified lineage link inside the corpus**: real-GPU NoC dissection (MICRO'24) → real-GPU core dissection (MICRO'25), both correcting Accel-Sim, one year apart.
- **Same first author, same conference**: *Ghost Arbitration: Mitigating Interconnect Side-Channel Timing Attacks in GPU* (Zhixian Jin et al., MICRO 2024 Session 8A) is the security-side companion; the NoC non-uniformity characterised here is the attack surface there. Verdict-only in this cluster's ledger.
- **Complementary**: `GPU-HPCA24-41` and `GPU-MICRO25-01` address simulator cost; this paper and `GPU-MICRO25-61` address simulator *correctness* in two different subsystems.
- **Precursors cited** [paper]: Bakhoda et al.'s throughput-effective NoC (a co-author's own earlier work, here revised); a run of NoC proposals [29]–[35] that assume 2D meshes or omit L2-bandwidth coupling; prior V100/A100 dissections that "do not provide a detailed analysis of the interconnect"; Accel-Sim, which the paper notes had already acknowledged L2-bandwidth modelling discrepancies; AES/RSA timing side-channel work.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

verdict_basis: The paper says so itself and backs it structurally: a GPU NoC differs from a CPU NoC because of the "high-bandwidth (and high-throughput) required" and the **many-to-few-to-many** traffic pattern — many SMs to few memory partitions and back — which is a direct consequence of having dozens of throughput cores share a partitioned L2 and HBM stack. Every finding is expressed in GPU structural terms that have no CPU analogue: the **SM/TPC/CPC/GPC hierarchy**, per-**L2-slice** bandwidth from a single **SM** versus from a whole **GPC**, latency determined by an SM's position within its GPC, and the load-dependence of the A100 far-partition penalty on the number of active SMs. The actionable recommendation — balance work across **SMs** rather than across L2 slices — is a CTA-scheduling statement. The measurement method itself is GPU-specific (`%smid` pinning, `-dlcg=cg` L1 bypass, one thread per warp to defeat coalescing). A CPU interconnect study would neither ask nor answer any of this.

verdict: `CORE_GPU`

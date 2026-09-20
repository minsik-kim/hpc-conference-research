# GPU_INTEGRATION_QUESTIONS — twelve cross-cutting questions, answered from corpus evidence

last_updated: 2026-09-19
knowledge_as_of: 2026-09-19

## How to read this document

Each answer is built only from this domain's own census, ledgers, deep analyses
and lineage documents, and links to them. Where the corpus cannot support an
answer, the answer says so rather than supplying a plausible trend. Three
constraints bind every number below:

- The corpus covers **ten venues, three years, main tracks only**. It is not a
  survey of the field.
- **Three venue-years have no denominator** (HPCA 2026, MICRO 2026, SC 2026),
  so no share-of-venue trend is computed anywhere.
- **Reachability is uneven.** 85 papers were read in full; 202 candidates were
  not, 27 of them open access but unreachable from the build environment. A
  trend that would be visible only in unread papers is invisible here.

---

## 1. How did GPU research focus change from 2024 to 2026?

**What the corpus supports.** Three shifts are visible in the read set, and
each rests on named papers rather than on counts.

*From modelling the GPU core to measuring it.* The 2024 anchor of the
architecture line is a simulator proposal built on a scoreboard-and-operand-collector
core model ([`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md)).
By 2025 a measurement study puts that baseline at 34.03% MAPE against a real
RTX A6000 and reports that real Turing-to-Blackwell cores use compiler control
bits and have no operand collectors
([`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)),
and by 2026 the same question is being answered by microbenchmarking real
silicon ([`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md)).
Detail in [`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §6.3.

*From the data path to the control path.* In GPU memory, the cost that papers
attack moves from moving bytes to deciding to move them —
[`GPU_MEMORY_LINEAGE.md`](GPU_MEMORY_LINEAGE.md) §1. The same movement appears
in compression, where the binding cost is variable-length **output placement**
rather than the codec, and in communication, where the question becomes who
issues the transfer rather than how fast the link is.

*From single-device performance to fleet behaviour.* 2026 adds production
telemetry and fleet-scale characterisation as a category with its own method
([`GPU-IPDPS26-41`](../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md),
[`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md)),
including a published falsification of the assumption that GPU health telemetry
predicts application slowdown.

**What the corpus does not support.** Any claim that GPU work grew or shrank as
a share of any venue. The denominators are missing for three venue-years and
approximate for several others.

---

## 2. Which hardware features after Hopper created new research topics?

From [`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §2 and
the analyses it cites:

- **Thread-block clusters and distributed shared memory** turned an
  inter-block memory tier into something a compiler can schedule — the basis of
  [`GPU-HPCA26-144`](../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md),
  whose own ablation prices the non-DSM residue at 1.52× of a 3.29× total.
- **`wgmma` and warp-group issue** changed what a "tile" means to a language,
  visible in the tile-level language
  [`GPU-ASPLOS26-141`](../corpus/GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md).
- **FP8 and the microscaling formats** created the precision-emulation branch
  outright — see Q5.
- **`cp.async` / TMA pipelining** became a structural assumption of sparse
  kernel design rather than an optimisation.

One caveat the corpus insists on: Hopper matrix throughput **depends on the
input data**, with zeros drawing under 200 W at over 95% of peak while random
data reaches 350 W and drops the clock below the published figure
([`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §7.1). Any
Hopper matrix number without a stated input distribution is not reproducible.

---

## 3. What new research axes appear with Blackwell?

**TMEM and `tcgen05`** are the substantive change in the read set: accumulators
move out of the register file into dedicated memory, and matrix-instruction
issue returns to warp scope after a generation at warp-group scope
([`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md)).
The corpus records the reversal and states plainly that **why it reversed is
unexplained** ([`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §6.2).

A second, contested axis: a reported **B200 FP64 matrix-throughput regression**
against H200, which if real makes precision emulation a necessity rather than
an option. The corpus also holds an ISC 2026 paper measuring working FP64 DMMA
on GB200 that does not mention any reduction. Different products; neither paper
reconciles them; the corpus records the tension rather than picking a side
([`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §6.1).

A third: whether Blackwell can be modelled at all is itself disputed — one
paper builds a model at 17.41% MAPE on a consumer part, another says TMEM
cannot be modelled on the datacentre part. Recorded as a product tension, not a
contradiction ([`GPU_HARDWARE_GENERATION_MAP.md`](GPU_HARDWARE_GENERATION_MAP.md) §6.4).

Blackwell coverage in this corpus is **thin and recent**; treat §3 as the
smallest-evidence answer in this document.

---

## 4. How did GPU virtual-memory research develop — page walk → migration → prefetch → multi-GPU memory?

Tested against the citations in [`GPU_MEMORY_LINEAGE.md`](GPU_MEMORY_LINEAGE.md).
The proposed progression is **partly real and partly a mis-description**.

*Real, and well-evidenced:* the translation layer is a genuine cited chain
ending at wafer-scale distributed page address translation
([`GPU-HPCA26-01`](../corpus/GPU-HPCA26-01--hdpat-hierarchical-distributed-page-address-translation.md)),
with each predecessor cited and quantitatively beaten. And multi-GPU placement
is a real branch with its own verified author-cluster lineage (§4.2).

*The mis-description:* **prefetch is not an independent stage.** It appears as
a tactic inside oversubscription and migration work, not as a phase the field
passed through.

*What reorganises the area instead:* the dominant cost is the **control path,
not the data path**, established independently on both vendors — host
involvement measured at ~7× the transfer time at 64 KB pages on one system; a
separate AMD study finding data movement is under half the total with
`cpu_update` + `SDMA_setup` + `alloc` at ~76%; a third reporting >65% of time
in page migrations. Three papers, two vendors, and **no verified citation among
them** — convergent independent evidence, not a lineage (§1).

Three distinct responses follow: keep the host driver but feed it semantics;
remove the host from the fault path; or delete the mechanism architecturally
with unified physical memory on an APU (§1.1). A recurring strategy across the
area is to **reclaim existing translation capacity rather than provision more**
(§2.1), and the hidden control variable throughout is **management
granularity**, which every paper pays for (§3.2).

---

## 5. How did Tensor Core research extend beyond AI GEMM into scientific and sparse workloads?

The corpus's clearest negative result about a supplied hypothesis. The expected
chain *scientific kernels → sparse kernels → precision emulation → new numeric
formats* is **not one citation chain**; it is three largely disjoint branches
that meet only in one cross-generation characterisation paper
([`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md) §0).

- **Branch A, scientific/non-GEMM**, is a real five-deep cited chain from
  TCStencil through [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md)
  to [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md),
  each citing and measuring against its predecessors.
- **Branch B, sparse**, runs from TC-GNN/DTC-SpMM through
  [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md) to
  [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md)
  and [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md),
  and cites none of the stencil work.
- **Branch C, emulation**, runs Ozaki → OzIMMU → INT8 →
  [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md) →
  [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md),
  and cites neither of the others.

The fourth stage — new numeric formats — **could not be tested**: no paper in
that sub-branch reached a deep analysis.

Two distinctions the corpus insists on. **Dense MMA on denser blocks is not the
Sparse Tensor Core**: two of the best-known "sparse tensor core" papers run
dense `mma` on 8×8 blocks and use 2:4 metadata nowhere (§5.2). And sparse
formats are now designed around **instruction tile sizes** rather than around
matrices — one format's bitmap is a single `uint64` because an 8×8 block has 64
positions (§2.4).

---

## 6. What control-placement difference does GPU-initiated communication make against host-driven MPI/NCCL?

[`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) answers this with a
vocabulary rather than a binary: **host-driven** (CPU enqueues, stream-ordered),
**device-triggered** (hardware tracker or pre-staged descriptors; the GPU rings
a doorbell), **device-resident** (a kernel itself issues puts and gets).

The decisive corpus evidence is that **the same runtime occupies two positions
depending on the fabric**: device-resident on mlx5 InfiniBand, where the kernel
builds work-queue entries and rings the User Access Region doorbell, but only
device-triggered on Slingshot CXI, where the host pre-stages a 256-entry
deferred work queue and the GPU merely rings the doorbell
([`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md)).
Control placement is a property of the fabric, not of the year
([`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) §3).

What the difference buys, where it is available, is the removal of a
synchronisation round-trip: inside an NVLink domain the residual cost of a
collective is microseconds of synchronisation, and a barrier above 1 µs is
roughly 40% of a 5 µs all-reduce. What it costs is portability: a major 2026
communication library states that current interconnects require a CPU thread to
initiate transfer and supports **no GPU-initiated RDMA at all**
([`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md)).

For 30 communication rows the corpus records control placement as `UNKNOWN`
rather than infer it from an abstract — `governance/ANTI_HALLUCINATION_RULES.md`
names this distinction as one that may not be answered from a compressed source.

---

## 7. Are GPU collectives actually evolving topology-aware → device-resident → symmetric-memory?

**No — not as a progression.** This is a verified negative
([`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) §7).

The stages coexist within single venue-years: IPDPS 2026 holds both a
device-resident multi-path balancing paper and a fully host-driven collective
library; SC 2026 holds both a device-resident speed-of-light collective and a
host-enqueued compressed collective. The two most recent host-driven papers do
not engage the device-initiated line at all — one has no MSCCL, no NVSHMEM
comparison and no discussion of kernel-resident collectives; another supports
only MPI/NCCL/RCCL backends and therefore *structurally cannot observe* the
claimed end-state.

Symmetric memory in particular is **contested, not traversed**: an ASPLOS 2026
paper reports finding no implementation where NVSHMEM outperforms NCCL for
collectives, while an SC 2026 paper one cycle later adopts PGAS as a core
principle and reports the former's multicast hanging on GB200
([`GPU_COMMUNICATION_STACK.md`](GPU_COMMUNICATION_STACK.md) §5).

What *is* converging, orthogonally to who initiates, is **in-fabric
reduction** — NVLink SHARP-style multicast reduce instructions appear across
several papers and three separate in-switch-computing proposals (§4). And
"vendor defaults are wrong" is independently corroborated three times (§6).

The corpus recommends replacing the ladder with a two-axis map: **who initiates
× which fabric is crossed**, with the fabric axis predicting the initiation
axis.

---

## 8. Has research on instruction, dependency and synchronisation bottlenecks grown, beyond compute-bound and memory-bound framing?

**Yes, and this one the corpus does support as a trend**, in the papers' own
framing rather than by counting
([`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §6).

On instruction issue: a 2024 simulator proposal for out-of-order issue is
followed by a 2026 *circuit-level* out-of-order GPU design framework and by a
statically scheduled SIMT proposal that takes the measured "compiler control
bits, not scoreboards" finding to its limit.

On dependency management as an object in its own right: the 2025 measurement
study quantifies it — 41 bits per warp of control bits at 0.09% of the register
file, against a scoreboard's 2.28% — and shows software dependence management
beating hardware on both performance and area.

On synchronisation: a 2024 multi-chiplet implicit-synchronisation paper is
followed by a 2026 paper on the same problem; scoped atomics get their own
2024 paper; and two correctness papers attack under- and over-synchronisation
from opposite sides in the same year without citing each other.

Outside the architecture venues the same shift is visible in application
kernels: one sparse solver's stated motivation is that **over 30% of its
baseline was inter-kernel synchronisation**, removed with a hand-built software
grid barrier ([`GPU-SC24-103`](../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md)),
and a 2026 sparse direct solver reduces kernel count to ~1.1% of baseline
([`GPU-PPoPP26-104`](../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md)).

---

## 9. Where does GPU production telemetry and reliability research connect to architecture-level research?

At one concrete, mechanical place: **the HBM repair budget**
([`GPU_TOPIC_LINEAGES.md`](GPU_TOPIC_LINEAGES.md) §6.4 and the reliability
topic). Volta repairs by page retirement with a 64-page table; Ampere and
Hopper by row remapping capped at 512 rows on both. H100's substantially larger
HBM3 against a flat 512-row budget is the architecture-level cause of a
fleet-level regression, and the per-GB framing versus the per-GPU framing
differ by roughly a factor of three — which is itself the finding
([`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md)).

A second connection runs through power. A production study finds ~33 W power
*swings*, not temperature level, correlated with GPU memory failures
([`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md)), and
three separate papers then show that software manufactures exactly those swings
— training loops dipping to a fraction of TDP at every iteration boundary,
coherently across thousands of GPUs. The corpus records the link from
parallelism-strategy tuning to memory-reliability risk as an **inference**,
asserted by no paper.

The connection that does **not** hold: GPU health telemetry does not predict
application slowdown. Real per-device heterogeneity exists at fleet scale, but
the rank correlation to runtime is ~0.07–0.08
([`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md)).
Any architecture-level proposal justified by "telemetry shows degradation" has
to clear this first.

---

## 10. How do SC, ICS, IPDPS and ISC see GPUs differently from ISCA, MICRO and HPCA?

Argued from the evidence type of the papers themselves
([`GPU_CROSS_VENUE_MAP.md`](GPU_CROSS_VENUE_MAP.md) §2 and §4), not from
reputation.

**The split is near-categorical.** Across SC/ICS/IPDPS/ISC/HPDC/PPoPP — 49
analyses — 48 rest on real hardware (44 measured, 4 production studies) and
exactly one is simulated. Across ISCA/MICRO/HPCA — 22 analyses — 15 involve a
simulator. PPoPP is 10 for 10 measured, the only venue in the corpus with no
simulated paper.

So: at the HPC venues **the contribution is a measured system on named
silicon**, and the paper must say which GPU, which library version and which
workload. At the architecture venues **the contribution is a mechanism, and the
baseline is a model** — which makes the model's fidelity load-bearing in a way
the HPC venues never face.

The sharpest critique of the architecture venues' evidence base came from
*inside* them: a MICRO 2025 measurement puts the standard simulator baseline at
34.03% MAPE against real silicon, and a MICRO 2024 measurement finds the real
on-chip network is a hierarchical crossbar rather than the simulated mesh.

A caution that belongs with this answer: **access asymmetry** partly shapes
what is visible here, and `GPU_CROSS_VENUE_MAP.md` §3 separates that
methodological artefact from the substantive difference.

---

## 11. What compiler/runtime bridge role do PPoPP and ASPLOS play between those two groups?

**The corpus rejects the bridging assumption**, on the citation evidence it
actually read ([`GPU_CROSS_VENUE_MAP.md`](GPU_CROSS_VENUE_MAP.md) §4.4).

PPoPP and ASPLOS in this read set import from **programming languages, formal
methods and databases**, not from architecture: one PPoPP 2024 runtime paper's
citation base is IPDPS/PPoPP/ICS/VLDB/SIGMOD/HPEC with no ISCA/MICRO/HPCA
presence at all; an ASPLOS 2024 memory-model paper cites PLDI, POPL, CAV and
TACAS; an ASPLOS 2026 capability-protection paper cites neither of the two
obvious GPU-memory-safety predecessors.

The traffic that does exist runs the **other** way: an HPCA 2026 kernel-fusion
paper imports from PLDI, OSDI, SOSP and an SC 2024 paper — a verified
SC → HPCA citation link.

What this rests on is stated exactly: five papers' self-reported citation bases
in one cluster's read set, not a bibliometric study. It is enough to refuse the
assumption, not enough to assert its opposite as a law.

---

## 12. When the same paper belongs to both the AI/HPC corpus and the GPU corpus, what should each preserve?

The operational answer is in
[`GPU_EXISTING_CORPUS_OVERLAP.md`](GPU_EXISTING_CORPUS_OVERLAP.md); the
principle is this.

**The AI/HPC corpus should preserve the workload argument**: what model or
workload the paper serves, what parallelism strategy it assumes, what it
changes about end-to-end training or inference, and how it sits in that
field's lineage.

**The GPU corpus should preserve the device argument**: warp and wavefront
execution, SM/CU scheduling, register and shared-memory/LDS budgets, cache and
TLB behaviour, HBM traffic, PTX/ISA and matrix-instruction semantics, the
CUDA/HIP runtime boundary, device-side synchronisation, and the
NVLink/xGMI/PCIe/NIC data path — plus the generation dependence and the
counterfactual record that says *why* the contribution is GPU-specific.

Neither should restate the other. The mechanism for that already exists here:
`GPU_DELTA_ANALYSIS`, used seven times in this domain against the imported
operations corpus. Each of those files states at the top what the prior record
already holds and adds only device-level depth — and two of them **corrected**
the prior record, which is the other reason the delta form is right: a second
pass over the same paper from a different angle is where errors surface.

One constraint that is not negotiable. `domains/ai_hpc_systems/` is
`EXTERNAL_IMPORT_PENDING` and holds no corpus in this repository, so for **99
papers** duplication is recorded as `NOT DETERMINED` — never as absent. 21 of
those already carry a GPU deep analysis, so an import containing them would
create a genuine double explanation. **A de-duplication pass must run before
that import, not after it.**

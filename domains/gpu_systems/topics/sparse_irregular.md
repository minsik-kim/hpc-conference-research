# Sparse and irregular GPU kernels (taxonomy G)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD in depth, POOR in breadth — and the corpus says why.**
Seven deep analyses (the cluster's `101–107` ID band), all `CORE_GPU`. But
`../corpus/_LEDGER_sparse_irregular.md` adjudicated **45 distinct papers** and
read only **7 of 45 (16%)** in full. Verdict ledger:
`../corpus/_LEDGER_sparse_irregular.md`.

> Front-matter note: two of the seven files carry the letter `H` in
> `primary_topic` ("Graph / irregular GPU workloads", "Irregular GPU
> workloads"). That is the *sparse cluster's* own sub-letter and must not be
> confused with the compiler cluster's `H`. Membership is by ID band and by
> `../corpus/_LEDGER_sparse_irregular.md` §6, not by the letter.

## 1. Problem landscape

Sparsity breaks three GPU assumptions at once: the output size is not known
before the kernel runs, the work per thread is not uniform, and the memory
access pattern is not coalesced. The corpus's most useful structural result is
that the field **split** rather than converged on one of them:

> **SpMM (sparse × dense) converged on matrix-unit exploitation *via* format
> design — the format exists to feed the instruction. SpGEMM (sparse × sparse),
> sparse solvers and graph workloads converged on load balancing and
> synchronisation, with no matrix unit in sight**
> (`../corpus/_LEDGER_sparse_irregular.md` §7.1, verified from full text).

The reason is mechanical, not fashionable: **no matrix unit helps with an
unknown output pattern**, and SpGEMM's output pattern is unknown by definition.

## 2. Key concepts

SpMM vs SpGEMM vs SpMV vs sparse direct solve; BCSR and block formats keyed to
an MMA operand shape (`m16n8k16`); **dense MMA on dense blocks vs 2:4
Sparse-Tensor-Core metadata**; the unpredictable-output-size problem and
device-side allocation; atomics, CAS loops and `atomicMax`; work stealing
(intra-block through shared memory, inter-block through a leader warp) vs
host-side priority aggregation; persistent single-kernel execution with a
hand-built software grid barrier; HyperLogLog cardinality estimation as an
allocation oracle; the five bottleneck classes this ledger uses — compute,
memory, dependency, synchronisation, **load imbalance**.

## 3. Main mechanism families

**Family G1 — feed the matrix unit by reshaping the format.**
`../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md` (BCSR at the
instruction shape, Jaccard row clustering) and
`../corpus/GPU-ASPLOS26-101--insum-indirect-einsums-sparse-gpu-kernels.md`
(push sparsity into *index tensors* so a dense compiler still emits `tl.dot`).

**Family G2 — estimate the unknown output size instead of computing it.**
`../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md`
(HyperLogLog, with a measured overflow rate and a fallback kernel).

**Family G3 — compute the unknown output size exactly, in two passes.**
`../corpus/GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md`
(two-pass join; the paper names this as its own limitation 5).

**Family G4 — redistribute work at run time, on the device.**
`../corpus/GPU-PPoPP26-105--diggerbees-dfs-hierarchical-block-level-stealing.md`
(hierarchical work stealing).

**Family G5 — redistribute work ahead of time, on the host.**
`../corpus/GPU-PPoPP26-104--trojan-horse-aggregate-and-batch-sparse-direct-solvers.md`
(priority aggregation; a drop-in layer under existing solvers).

**Family G6 — remove the inter-kernel boundary entirely.**
`../corpus/GPU-SC24-103--mille-feuille-tile-grained-mixed-precision-single-kernel-cg.md`
(persistent single kernel, hand-built software grid barrier, tile-grained
mixed precision — **no matrix unit anywhere in the paper**).

## 4. Representative papers

- **SMaT** (SC 2024) — **MEASURED** on **A100**. The C/B/T breakdown is what
  makes it worth reading rather than its speedup table: asynchronous loads
  (`cuda::memcpy_async`) modest; BCSR pointer arrays to skip empty blocks
  incremental; **the Tensor Core MMA API ≈10×**, with the fully optimised
  kernel **22× over naive**; Jaccard preprocessing cuts block count 1.3×–2.4×
  and `mip1`'s per-row block-count standard deviation **8.4×** `[paper]`.
  **The causal ranking contradicts the paper's own title emphasis** — the
  low-level kernel work dominates the algorithmic reordering. Confirmed from
  full text to use **dense MMA on BCSR blocks (`m16n8k16`), not NVIDIA's
  structured 2:4 format** `[paper]`.
- **Insum** (ASPLOS 2026) — **MEASURED** (H100, RTX 3090). Figure 13 ablation
  on structured SpMM (4096×4096, 32×32 dense blocks, **RTX 3090**): COO
  baseline → **+ grouping ≈8×** → **+ blocking ≈20× cumulative** (the dense
  inner block is what makes `tl.dot` legal at all) → **+ Tensor Core fusion
  +2.6×** `[paper]`. Dense MMA, not 2:4 metadata.
- **Ocean** (ICS 2026) — **MEASURED** on **NERSC Perlmutter (A100 40 GB, CUDA
  12.9)** and **NCSA DeltaAI (H100 96 GB, CUDA 12.4)**, **337 square** (≥100M
  FLOPs) and **64 rectangular** SuiteSparse matrices. On A100, geometric mean
  **1.4× over spECK, 2.6× over OpSparse, 3.5× over TileSpGEMM, 2.0× over
  HSMU-SpGEMM**; best on **86%** of matrices; **63.23 GFLOP/s** mean against
  spECK's 46.2. On H100, **1.6× over spECK**. **A negative case is disclosed:
  `torso1` at 0.55×** `[paper]`. Contains **no occurrence of "Tensor Core",
  "MMA" or "tensor core" anywhere in its text or references** — verified by
  targeted full-text query.
- **GPUlog** (ASPLOS 2025) — **MEASURED** (A100/H100 class, NCSA Delta).
  Composes library primitives (Thrust/CUB/RMM) rather than writing a device
  protocol — the opposite implementation style from DiggerBees at the same
  bottleneck class.
- **DiggerBees** (PPoPP 2026) — **MEASURED** on **H100 (132 SMs, 2.02 TB/s)**
  and **A100 (108 SMs, 1.94 TB/s)**, CUDA 12.8, driver 570.153.02; CPU
  baselines on an **Intel Xeon Max 9462 (64 cores, 2×64 GB HBM)**; **234
  SuiteSparse graphs** (151 DIMACS10, 68 SNAP, …). **1.37× avg over CKL-PDFS
  (CPU work-stealing DFS, up to 6.24×)**, **1.83× over ACR-PDFS**, **30.18×
  over NVG-DFS (up to 1841.68×)** `[paper]`. The inter-block stealing tier
  alone is worth **25.94×–38.41×** in the ablation. **The 30.18×/1.37× pair is
  the number to carry**: the gap over the previous *GPU* DFS is 22× larger than
  the gap over *CPU* work stealing — the contribution is the GPU mapping.
- **Trojan Horse** (PPoPP 2026) — **MEASURED**. Scale-up on **RTX 5060 Ti
  (0.37 TFlop/s FP64, 0.45 TB/s)**, **RTX 5090 (1.64 TFlop/s, 1.79 TB/s)** and
  **A100 PCIe 40 GB (9.75 TFlop/s, 1.56 TB/s)**, 4 moderate matrices plus 200
  further SuiteSparse matrices on A100: **SuperLU_DIST v9.1.0 + Trojan Horse
  5.47× average, up to 418.79×**; **PanguLU v5.0.0 + Trojan Horse 2.84×
  average, up to 5.59×** `[paper]`. Scale-out on **16× H100 SXM** (two nodes ×
  8, 400 Gbps IB) and **16× AMD MI50** (four nodes × 4, 200 Gbps IB):
  **SuperLU_DIST 3.5× average, up to 24.6×**. Kernel count falls to
  **1.10%/1.48%** of baseline — a metric with **no CPU meaning**, which is why
  the strict counterfactual returns `CORE_GPU`.
- **Mille-feuille** (SC 2024) — **MEASURED** on **A100 (CUDA 12.0)** and **AMD
  MI210 (ROCm 5.7.3)**; **230 SPD SuiteSparse matrices for CG**, **686
  nonsymmetric/indefinite for BiCGSTAB**, relative residual `< 10⁻¹⁰` or 1000
  iterations, RHS `A·1`, `x₀ = 0`; baselines run FP64 throughout. CG **3.03×
  avg (up to 8.77×) vs cuSPARSE 12.0**, **5.37× (up to 16.54×) vs PETSc 3.20**,
  **4.36× vs Ginkgo 1.7.0**; PCG **3.82× avg, up to 40.38×** `[paper]`. Its
  **>30% inter-kernel synchronisation share** is likewise a quantity with no
  CPU meaning.

## 5. Historical lineage

Taken from the papers' own citations, baselines and author overlaps, read in
the full texts (`../corpus/_LEDGER_sparse_irregular.md` §7.5); the wider chains
are in `../synthesis/GPU_TOPIC_LINEAGES.md`.

- **SpMM line**: SMaT (SC 2024) → FlashSparse / Acc-SpMM (PPoPP 2025) → Insum
  (ASPLOS 2026). SMaT is the **earliest member** of the dense-MMA-on-blocks
  line, a correction this cluster made to `../corpus/_LEDGER_tensor_cores.md`
  from read full text.
- **SSSLab / China University of Petroleum-Beijing (Weifeng Liu, Zhou Jin)** is
  the most productive single group here, verified by author lists on the read
  PDFs: **DASP (SC 2023) → PanguLU (SC 2023) → AmgT + Mille-feuille (SC 2024)
  → CuBie + DiggerBees + Trojan Horse (PPoPP 2026)**. Internal tension worth
  recording: **DASP is a baseline that beats SMaT by ~28× on `dc2`**, and
  **PanguLU is simultaneously a baseline and an integration target for Trojan
  Horse**.
- **Marc Casas (BSC)** appears on DiggerBees, BerryBees, Swift (HPCA 2026) and
  Extending Sparse Patterns (HPDC 2024) — on **both** the matrix-unit and the
  no-matrix-unit sides.
- **Yihao Sun / Ahmedur Rahman Shovon**: GPUlog (ASPLOS 2025) → Multi-node
  Multi-GPU Datalog (ICS 2025), confirmed by GPUlog's own stated future work.

## 6. Implementation families

All seven are `REAL_SILICON`; there is **no simulator paper among the deep
analyses in this topic**. Four of the full-text successes came from two labs
that post their own PDFs (SSSLab/CUPB — Mille-feuille, Trojan Horse,
DiggerBees; and Thomas Gilray — GPUlog), which is itself the explanation for
this topic's access profile (§8). Implementation style splits sharply:
library composition (GPUlog on Thrust/CUB/RMM) versus hand-written warp-level
protocols built from atomics and fences (DiggerBees) — **opposite ends of the
spectrum within the same bottleneck class**.

## 7. Important disagreements / tensions

**T1 — the unpredictable-output-size problem is being solved three times in
parallel, with no cross-citation, and a general solution exists that none of
them uses.** Ocean estimates it probabilistically (HyperLogLog, **0.3–1.2%
overflow**, fallback kernel); GPUlog computes it exactly with a two-pass join
and names that as its limitation; a third line pre-sizes. **Gallatin**
(`../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md`)
is the general-purpose device-side allocator that would subsume all three, and
**none of them uses it** — GPUlog uses RAPIDS RMM, Ocean uses fixed geometric
binning, and neither read paper cites Gallatin or INFINEL. The ledger calls
this "the clearest un-exploited connection this cluster found"
(`../corpus/_LEDGER_sparse_irregular.md` §7.2). Ocean (ICS 2026) and GPUlog
(ASPLOS 2025) are two answers to the same GPU constraint **published one year
apart in different communities, apparently without contact**.

**T2 — the sparse-GPU community and the RT-unit-repurposing community do not
cite each other, verified by targeted query.** SMaT was checked against its
entire text and references for "ray tracing", "RT core", "RT unit", "BVH",
"RTSpMSpM" and "LibRTS": **no** on all six. Ocean: **no** on all six. Yet the
corpus holds a substantial RT-unit line including **RTSpMSpM** (ISCA 2025),
which is *sparse matrix multiplication on the RT unit*. See
`fixed_function_repurposing.md`.

**T3 — matrix units are not this community's answer to irregularity, and the
evidence is the same authors changing their minds.** BerryBees (PPoPP 2025)
does BFS on bit Tensor Cores; **Niu and Casas wrote DiggerBees one year later
using no matrix unit at all** for DFS. CuBie, from the same lab, places
BFS/SpGEMM in the quadrant where the matrix unit helps least. Three
independent attachments, one conclusion.

**T4 — a static schedule loses to a dynamic one on a power-law distribution,
however well you reorder first.** SMaT's honest failure on `dc2`
(**2.5 GFLOP/s vs DASP's 69.1**, ≈28×) is the counter-example that motivates
families G4 and G5. Three *independent* PPoPP 2026 papers then attack load
imbalance by dynamic work redistribution — DiggerBees (device-side stealing),
RDMCE/Root-Down Exposure (Tsinghua, **1.25–5.38×** over prior GPU MCE) and
Trojan Horse (host-side aggregation) — two of the three from one lab, the third
from a different group `[../corpus/_LEDGER_sparse_irregular.md §7.3]`.

**T5 — "on GPUs" in a title does not indicate a GPU mechanism here, unlike in
the tensor-core cluster.** Of 45 adjudicated papers, **13 are `RELATED_GPU`**,
every one an *algorithm* paper — a preconditioner sparsification, a
communication-avoiding partitioning, a Strassen recursion, a bidirectional
search, a Louvain port. The ledger reports this as a structural feature: sparse
linear algebra and graph analytics have large algorithm-first literatures that
Tensor-Core work does not. The cleanest discriminator found across all 45 was
**whether the paper's headline metric has a CPU meaning**
(`../corpus/_LEDGER_sparse_irregular.md` §7.6).

## 8. Current limitations

**This topic is bounded by full-text access more sharply than any other in the
corpus, and the ledger quantifies it: 7 of 45 papers (16%) were readable in
full**, against 9 of 42 in the sibling Tensor-Core cluster
(`../corpus/_LEDGER_sparse_irregular.md` §3). The ledger's own diagnosis is
that the difference is **not venue mix but author-PDF culture** — every one of
the four author-PDF successes came from two labs that post their own papers.
**ACM and IEEE paywalls account for essentially all of the 27 `CLOSED_ACCESS`
rows** (`dl.acm.org` → 403, `ieeexplore.ieee.org` → 418 from this environment;
`conference-publishing.com/toc/PPOPP24|25/abs` returns a server-side "empty
event record" error while the PPOPP26 equivalent works). **This is an
access-path limitation, not a claim about any paper's licence** — see
`../synthesis/GPU_PENDING_FULLTEXT.md`.

Consequences to state plainly:
- Every cross-paper claim in §7 rests on **seven** read papers. T2's
  non-citation result is verified on two of them (SMaT, Ocean), not on all
  seven.
- **Five verdicts are withheld rather than guessed** — HR-SpMM and cuMIS
  (census flagged the GPU target as unverified), GLUMIN and Fine-Grained
  Redundancy (title names no mechanism, abstract unreachable), and
  Loop-Carried (existence unconfirmed). Per
  `../../../governance/ANTI_HALLUCINATION_RULES.md` these were not upgraded.
- **No paper in this cluster was excluded**, so the 45 are a candidate pool,
  not a filtered one.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. Would Gallatin close T1? Three papers pay three different prices for an
   unknown output size and a general device-side allocator exists in the same
   corpus, uncited by any of them.
2. RTSpMSpM (ISCA 2025) claims sparse matrix multiplication on the RT unit and
   is invisible to this community (T2). Is that a real mechanism gap or a
   citation gap? The corpus cannot tell without RTSpMSpM's full text.
3. Does SpGEMM stay matrix-unit-free? Ocean's verified absence of any
   matrix-unit term is one data point at one venue-year; the SpMM line's
   trajectory (§5) suggests the pressure will arrive.

## 10. Deeper lookup paths

`../corpus/_LEDGER_sparse_irregular.md` — §3 access summary, §4 verdict
summary, §5 the two corrections it made to `../corpus/_LEDGER_tensor_cores.md`
from read full text, §7 the seven cross-paper findings → the seven analyses
above → the papers and their artifacts.
Cross-topic: `tensor_cores.md` (the dense-MMA-vs-2:4 distinction and the SpMM
line), `compiler_programming.md` (Gallatin, and the language-level end of
G1/G3), `fixed_function_repurposing.md` (the RT-unit line this community does
not cite).

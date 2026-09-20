# HBM and data movement, GPU compression, GPU–storage and GPU–host I/O (taxonomy E)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD on compression, THIN on the storage path.**
Seven deep analyses (taxonomy `E`), six `CORE_GPU` and one `RELATED_GPU`
(Hydrogen, re-adjudicated from full text and **confirmed**, not overturned).
Verdict ledger: `../corpus/_LEDGER_data_movement_compression.md`.

## 1. Problem landscape

HBM bandwidth is the binding resource, and this topic is four communities
paying four different prices to move fewer bytes across it — or around it.
The corpus's central technical finding is not about compression at all:
**variable-length output placement, not compression, is what limits GPU
compressors**, and every paper solves it differently
(`../corpus/_LEDGER_data_movement_compression.md` §D.1, supported by four
independent sources).

The second structural finding is sociological and verified in both directions:
this topic contains **four mutually non-citing communities working on the same
GPU problem** — standalone scientific compressors, compression-inside-
collectives, hardware cache compression, and lossless floating-point
compression (§7, T2).

## 2. Key concepts

Error-bounded lossy compression (value-range-relative error bound `eb`) vs
lossless; prediction (Lorenzo, spline interpolation) vs transform (ZFP) vs
sorting; quantisation, Huffman, and a second lossless pass; **decoupled
look-back / variable look-back** as the single-pass variable-length placement
technique (Merrill–Garland), and `__threadfence()`-separated flag protocols;
compression ratio vs throughput as an explicit trade-off axis; achieved
bandwidth against HBM peak; GPUDirect Storage, `cuFile`, NVMe submission and
completion queues and doorbells; HBM as a *tier* rather than as a ceiling.

## 3. Main mechanism families

**Family E1 — ratio branch.** Multi-level spline interpolation plus a second
lossless pass. `../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md`.

**Family E2 — speed branch.** Single fused kernel, warp-level everything.
`../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md`.

**Family E3 — un-fuse to escape the dependency.**
`../corpus/GPU-ICS26-81--gpz-gpu-lossy-compressor-particle-data.md` splits
compaction into write / device prefix-sum / copy.

**Family E4 — composition of cheap reversible integer transforms (lossless).**
`../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md`.

**Family E5 — buy the same problem in silicon.**
`../corpus/GPU-ISCA25-81--ecco-entropy-aware-cache-compression-hbm-bandwidth.md`
puts entropy-coded compression in the L2↔HBM path.

**Family E6 — reallocate HBM rather than shrink the data.**
`../corpus/GPU-SC24-82--hydrogen-contention-aware-hybrid-memory-cpu-gpu.md`.

**Family E7 — device-resident storage control.**
`../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md`.

## 4. Representative papers

- **cuSZ-i** (SC 2024) — **MEASURED** on **A100 80 GB (1555 GB/s)** and
  **A40 48 GB (695.8 GB/s)**, six SDRBench-class datasets (JHTDB 512³, Miranda
  256×384×384, Nyx 512³, QMCPack, RTM, S3D 500³), value-range-relative error
  bounds **1e-2 / 1e-3 / 1e-4** `[paper]`. Deliberately **slower** than its GPU
  predecessors and buys ratio with that time; moves the Huffman codebook build
  **off the GPU to the CPU (~200 µs)** `[paper]`. Resolves its entire
  stride-4/2/1 level chain inside `__shared__ T data[9][9][33]` `[code]`.
- **Aatrox** (ICS 2025) — **MEASURED** on **A100 (108 SMs, 40 GB, CUDA
  11.4.120)** and **RTX A4000 (40 SMs)**, nine SDRBench/Open-SciVis datasets.
  One initial value per **32,768** elements instead of one per 32. **388.3 GB/s
  compression / 718.0 GB/s decompression** `[paper]`. Measures the cost of
  placement directly: **global prefix sum = 32.8% of compression time and
  39.8% of decompression time**, block concatenation a further **41.5%** from
  non-coalesced access — **about 74% of compression time is placing bytes, not
  compressing them** `[paper]`. The hierarchical-delta gain shrinks as the
  error bound tightens: **1.74× at eb 1e-2 → 1.50× at 1e-3 → 1.39× at 1e-4**.
- **GPZ** (ICS 2026) — **MEASURED** on **RTX 4090 (24 GB, 1008 GB/s peak)**,
  **H100 SXM (3.35 TB/s)** and **L4**, six particle datasets (USGS/3DEP 734 M
  particles; OuterRim 84 M; NewWorlds 144 M; WarpX 273 M; LAMMPS 67 M; XGC
  13 M). Reaches **809 GB/s against a 1008 GB/s RTX 4090 peak (~80%)** in the
  compaction stage `[paper]` — **the only achieved-vs-peak figure in this
  topic**. Cumulative ablation on RTX 4090: **89 → 588 GB/s compression**,
  **102 → 656 GB/s decompression** — i.e. most of the result is
  micro-optimisation, not algorithm. Honest cost: **7–23% lower ratio than
  cuSZ in three cases, while 3–6× faster** `[paper]`.
- **Lossless FP compression** (ASPLOS 2025) — **MEASURED** on **RTX 4090
  (128 SMs)** and **A100 (108 SMs)** plus two CPUs. Uses **Merrill and
  Garland's variable look-back strategy**, implemented as `propagate_carry`
  (`speed-compressor-single.cu:111-145`) `[code]`. Keeps all chunk data in
  shared memory between transformations with a **16 KB chunk** sized for
  exactly that `[paper]`. States its own failure mode: "we do not expect our
  algorithms to compress non-smooth data particularly well" `[paper]`.
- **Ecco** (ISCA 2025) — **SIMULATED** on a modelled **A100 in modified
  Accel-Sim / GPGPU-Sim 4.0**, NVBit 1.7.1 traces, stated simulation error
  within 10%; LLaMA/LLaMA-2/Mistral decoding only, batch 1–64, sequence 1K–4K
  `[paper]`. **Up to 2.9× vs AWQ, 2.4× vs Olive, 1.8× vs SmoothQuant, average
  2.9× vs FP16** — all **simulated**. The hardware cost of variable-length
  decoding, stated in silicon: **64 parallel decoders, 8 speculative
  sub-decoders each trying bit-offsets 0–7, a 6-stage merge tree, 5.11 mm² and
  7.36 W** `[paper]` — **synthesis estimates, not measured silicon**. Honest
  limitation: **Grouped-Query Attention models show reduced speedup** because
  GQA turns memory-bound GEMVs into compute-bound GEMMs `[paper]`.
- **Hydrogen** (SC 2024, `RELATED_GPU`) — **SIMULATED** in zsim on a modelled
  8-core CPU + integrated GPU with 96 EUs, 16 MB shared LLC, HBM2E 16ch +
  DDR4-3200 4ch, 12 CPU+GPU workload pairs. **1.24× average / up to 1.48×** vs
  non-partitioned; **1.16× / 1.31×** vs Profess; **1.47× / 1.98×** vs
  HAShCache `[paper]`. Its citation neighbourhood is memory-systems, not
  GPU-architecture, which is itself evidence for the `RELATED_GPU` verdict.
- **AGILE** (SC 2025) — **MEASURED** on an **RTX 5000 Ada over PCIe Gen4x16**
  with one Dell Ent NVMe 1.6 TB and two Samsung 990 PRO 1 TB, each Gen4x4;
  driver 550.54, CUDA 12.8. A GPU thread writes an NVMe SQE and rings the
  doorbell; a GPU daemon kernel reaps the CQ — **the CPU is in neither the
  control nor the data path** `[paper]`. **1.88×** over BaM, **1.32× fewer
  registers per thread**, **3.12× lower software-cache and 2.85× lower NVMe
  I/O overhead** on graph applications `[paper]`.

## 5. Historical lineage

The SZ family tree, reconstructed **only from the papers' own citations**
(`../corpus/_LEDGER_data_movement_compression.md` §D.3): CPU SZ2 → SZ3 → QoZ;
GPU **ratio branch** cuSZ (Tian '20/'21) → cuSZ+ → **cuSZ-i** ('24) → PRISM
(PPoPP '26, unread); GPU **speed branch** cuSZx / FZ-GPU → cuSZp (SC '23) →
cuSZp2 (SC '24) → cuSZp3 (SC '25) and the **Aatrox** mode (ICS '25) → **GPZ**
(ICS '26, particle branch); transform branch cuZFP, MGARD-X → BlockMGARD
(SC '26, unread); **lossless branch** GFC, MPC, ndzip-gpu, nvCOMP → the
ASPLOS '25 SP/DP compressors, **with no contact with SZ at all**.

Verified convergence in the on-chip principle: five independent groups converge
on *keep the multi-stage pipeline in on-chip memory and touch HBM once in, once
out* — cuSZ-i's `9×9×33` shared tile, the ASPLOS'25 16 KB chunk, Aatrox's
register-resident layers with `__shfl_up_sync`, GPZ's deliberate shared-memory
under-allocation "to enlarge the effective L1 cache", and BlockMGARD's
abstract-level "in-cache block decomposition"
(`../corpus/_LEDGER_data_movement_compression.md` §D.5). **Corollary: block and
chunk size in this literature is set by the scratchpad budget, not by the
algorithm** — 8×8×8, 16 KB, 32×32×32, runtime-sized.

Cross-topic lineage detail is collected in `../synthesis/GPU_TOPIC_LINEAGES.md`
and the hardware-generation dependences in
`../synthesis/GPU_HARDWARE_GENERATION_MAP.md`.

## 6. Implementation families

`REAL_SILICON` software compressors with public artifacts: cuSZ-i (pinned
`[code]`), Aatrox, GPZ, the ASPLOS'25 lossless pair, AGILE (which vendors a
BaM NVMe driver in-tree, `driver/bam_nvme_driver-linux-6.8.0/` `[code]` —
unusually good comparative hygiene). `SIMULATOR`: Ecco (Accel-Sim), Hydrogen
(zsim). Area and power figures for Ecco are synthesis estimates and are never
reported here as measured
(`../../../governance/SOURCE_EVIDENCE_RULES.md`).

## 7. Important disagreements / tensions

**T1 — four different prices for the same problem, and no table should put
them in one column.** Variable-length output placement costs: a **stall**
(cuSZp2/Aatrox's `__threadfence()`-separated look-back), **HBM traffic**
(GPZ's un-fused three-kernel compaction, which writes the data twice), **area**
(Ecco's 5.11 mm² and 7.36 W of speculative decoders), or **nothing beyond the
textbook algorithm** (ASPLOS'25's `propagate_carry`). These are four points on
a cost curve, not four results `[../corpus/_LEDGER_data_movement_compression.md §D.1]`.

**T2 — four mutually non-citing communities, verified in both directions.**
`SUPPORTED`, by targeted full-text checks:
(a) standalone compressors → collectives: cuSZ-i, Aatrox and GPZ contain **no
reference to gZCCL, hZCCL, ghZCCL or any NCCL-integrated compressor** `[paper,
all three]`;
(b) collectives → standalone: `../corpus/GPU-SC26-22--ncclz-compression-enabled-gpu-collectives.md`
cites gZCCL, ghZCCL, COCCL and MVAPICH2-class MPI compression and **no
standalone GPU compressor**;
(c) hardware: Ecco cites BDI, Buddy Compression, GIST, JPEG-ACT and the LLM
quantisation literature and **no SZ-family work**;
(d) lossless: the ASPLOS'25 paper cites **none** of cuSZ/cuSZp/cuSZp2/FZ-GPU/cuZFP.
Authors overlap heavily across (a) and (b) — Sheng Di, Franck Cappello,
Jiajun Huang, Xiaodong Yu — so this is **two disjoint citation practices, not
two disjoint groups of people**. Recorded as an observation about the
literature, **with no claim about intent**.

**T3 — almost no paper establishes what bounds its own throughput.** Of the
compression papers read at full text, exactly **one** reports an
achieved-vs-peak bandwidth figure (GPZ, one stage only) and **one** establishes
a bound by stage decomposition (Aatrox). cuSZ-i reports only ratios against
cuSZ. **Rooflines, occupancy figures and achieved-bandwidth measurements are
essentially absent from this literature**, which makes cross-paper throughput
claims unusually hard to adjudicate. Two anomalies went unexplained by their
own authors: GPZ's compression barely moves from RTX 4090 to H100 (**598 →
616 GB/s**) while decompression rises (**651 → 1091 GB/s**) — so H100
compression is *not* bandwidth-bound and nothing says what it is bound by
`[../corpus/_LEDGER_data_movement_compression.md §D.2]`.

**T4 — the two GPU compression branches stopped competing.** Aatrox's baselines
are FZ-GPU / cuSZp / cuSZp2 / cuZFP; **cuSZ-i is cited in related work but not
evaluated against** `[paper]`. GPZ does evaluate across both branches and is
the only head-to-head robustness evidence found: it reports **cuSZ-i lacks 1D
data support** and **cuSZp2 produces verification errors on H100** `[paper]`.

**T5 — the storage path is easier than the network path, and the corpus can say
why.** AGILE achieves fully device-resident NVMe control, while
`../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md` records
that GPU-initiated **RDMA** is not supported and inter-node transfers need a
host proxy. The reason is mechanical: NVMe doorbells are plain MMIO registers
mappable into the GPU's address space, whereas RDMA needs a driver-mediated
work-queue protocol. `[inference]`, but from the two papers side by side.

## 8. Current limitations

**Bounded by full-text access in two specific places.** `dl.acm.org` → 403 and
`ieeexplore.ieee.org` → 418 from this environment, so several papers the census
marks as open at the publisher are nonetheless `CLOSED_ACCESS` *as determined
here* — an access-path limitation, not a statement about licence. The
consequences for this topic:

- The GPU–storage path has **one** deep analysis (AGILE). **Phoenix** (SC 2025,
  artifact-only) and **OS2G** (ASPLOS 2025, unread, DPU-routed) are the other
  two branches and neither was read. Calling this topic "GPU–storage coverage"
  would overstate a single data point.
- **FSZ** (SC 2026, "Breaking the Prediction-Throughput Trade-off in GPU Lossy
  Compression"), the one title that promises to collapse T4's split, is unread;
  existence verified via the official SC26 Best Paper finalists announcement
  `[official-web]`.
- **PRISM** (PPoPP '26), **TZ** (HPDC '26) and **BlockMGARD** (SC '26) are
  unread members of the family tree in §5.
- Seven rows carry `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` because
  `../../ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` — Ecco, Hydrogen,
  MLP-Offload (SC 2025), CXL tensor offloading (SC 2024), SuperOffload
  (ASPLOS 2026), DLRM dual-level lossy compression (SC 2024), ADTopk
  (HPDC 2024). **No claim of non-duplication is made**
  (`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).

**Bounded by the literature, not by access:** T3. The absent rooflines are the
papers' own omission, and no amount of further retrieval fixes it.

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. What bounds GPZ's H100 compression at 616 GB/s against a 3.35 TB/s peak?
   Neither the paper nor any other in this topic answers (T3).
2. Would any of the software placement schemes benefit from Ecco-style
   speculation if a *warp*, not a thread, were the speculating unit? No paper
   in the corpus tries; the two communities do not cite each other (T2).
3. Does the on-chip-residency principle (§5) impose a ceiling on ratio that a
   larger scratchpad would lift, given that every group sizes its block to the
   scratchpad rather than to the data?

## 10. Deeper lookup paths

`../corpus/_LEDGER_data_movement_compression.md` — especially §D (six
cross-paper findings, each grounded in a quoted claim or a pinned commit) →
the seven analyses above → the pinned artifacts in each §12.8.
Cross-topic: `multi_gpu_communication.md` for the compression-in-collectives
branch that this topic does not cite; `memory_virtualization.md` for DREAM,
the device-driven analogue of AGILE on the host-memory path.
For anything quantitative or contested, descend to the corpus file and then to
the paper, per `../../../governance/ANTI_HALLUCINATION_RULES.md`.

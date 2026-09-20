# GPU_HARDWARE_GENERATION_MAP — what changed per generation, and which corpus paper establishes it

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
source: `## 12.12 Hardware generation dependence` in all 85 corpus analyses, plus
`_LEDGER_core_execution.md` §3 and `_LEDGER_power_energy.md` §2.

---

## 0. Rules this map enforces

1. **The NVIDIA and AMD lines are kept separate.** They are not two columns of
   one table; they are two design histories that the corpus's papers rarely
   measure together.
2. **Generation features are never mixed.** A Hopper feature is not carried onto
   Blackwell and a Blackwell feature is not read back onto Hopper, even where the
   silicon is contemporaneous. Several papers state this explicitly and it is
   reproduced as their instruction, not as editorial caution.
3. **Product, not family.** H800 ≠ H100. A800 ≠ A100. RTX 5070 Ti (GB20x
   consumer Blackwell) ≠ B200 (datacenter Blackwell). MI300A (APU) ≠ MI300X
   (discrete). GB200 Superchip ≠ B200 SXM. Every row names the measured product.
4. **Measured vs modelled is marked.** A simulated "Hopper-style" baseline is not
   a Hopper measurement.
5. Every quantitative entry keeps its hardware/workload/baseline qualifier.

---

## 1. NVIDIA — Volta / Turing / Ampere (through A100)

| Feature established | Evidence | Corpus file |
|---|---|---|
| **Access counters with remote-access tracking**, 64 KB page-group granularity, migration threshold 256, attributed to "NVIDIA Volta and newer" | `[paper]` | [`GPU-HPCA24-01`](../corpus/GPU-HPCA24-01--grit-fine-grained-dynamic-page-placement.md) |
| **UVM fault-based migration** with 4 KB base page, 60 KB speculative prefetch, 2 MB VABlock eviction | `[paper]` | [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) |
| **16-sub-entry coalesced last-level TLB entries**, anchored to "NVIDIA's Ampere generations" | `[paper]` | [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md) |
| **MIG leaves the L3 TLB unpartitioned**; co-running tenants lose 40% on average vs isolation (A100, MGPUSim, 3 tenants at (3g,2g,2g)/(3g,3g), 64 KB pages; benefit falls to 10% at 2 MB pages and to 12.1% at six co-runners) | `[paper]` | [`GPU-MICRO24-02`](../corpus/GPU-MICRO24-02--star-subentry-sharing-aware-tlb-mig.md) |
| **A100 MIG lattice**: 1/2/3/4/7 GPCs, 5 and 6 illegal; 19 legal combinations; profile IDs 0/5/9/14/19; 10/20/40/80 GB | `[paper]` `[code]` | [`GPU-SC24-161`](../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md) |
| **CUDA low-level VMM API** (`cuMemCreate`/`cuMemMap`/`cuMemSetAccess`), 2 MB physical-chunk granularity, `cuMemSetAccess` at **96.8x** native `cuMalloc`; multiple VA→PA mappings to one chunk permitted by the GPU MMU (A100-80GB, CUDA 11.4) | `[paper]` | [`GPU-ASPLOS24-01`](../corpus/GPU-ASPLOS24-01--gmlake-gpu-memory-defragmentation-vm-stitching.md) |
| **`cp.async`** available from Ampere onward; Ampere-era `cuda::memcpy_async` is the async-copy mechanism used by the SpMM line | `[paper]` | [`GPU-PPoPP25-02`](../corpus/GPU-PPoPP25-02--acc-spmm-general-purpose-tensor-core-spmm.md), [`GPU-SC24-102`](../corpus/GPU-SC24-102--smat-unstructured-spmm-tensor-cores.md) |
| **FP64 matrix shape `m8n8k4`** (A100); A100 FP64 vector peak 19.5 TFLOP/s | `[paper]` | [`GPU-PPoPP24-01`](../corpus/GPU-PPoPP24-01--convstencil-stencil-to-matmul-tensor-cores.md) |
| **Warp-scope `mma`** is the matrix-instruction issue unit on Ampere/Ada; asymmetric `m=16`/`n=8` extents of the `mma.m16n8k*` family | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md), [`GPU-PPoPP25-01`](../corpus/GPU-PPoPP25-01--flashsparse-swap-and-transpose-sparse-tensor-cores.md) |
| **2:4 Sparse Tensor Cores introduced with Ampere** (`mma.sp m16n8k16`, FP16) | `[paper]` | [`GPU-PPoPP26-01`](../corpus/GPU-PPoPP26-01--spider-sptcstencil-sparse-tensor-cores-stencil.md) |
| **A100 already ships lossless cache compression**; A100 L2 peak 5120 B/cycle, 826 mm² die, 82 W idle at 1410 MHz | `[paper]` | [`GPU-ISCA25-81`](../corpus/GPU-ISCA25-81--ecco-entropy-aware-cache-compression-hbm-bandwidth.md) |
| **Partitioned L2 with left/right central split appears on A100 and H100 but NOT on V100**; near/far L2 ~200 vs ~400 cycles | `[paper]` | [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md) |
| p-chase corroboration: A100 near/far L2 hit **208 / 356.6 cycles** | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **No hardware scoreboard and no operand collector units** on real Turing/Ampere/Blackwell cores — compiler-encoded control bits (stall counter, yield bit, six dependence counters) instead; stock Accel-Sim core model measured at **34.03% MAPE vs a real RTX A6000** | `[paper]` | [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md) |
| **Register spill/fill as a first-class cost**: 40.4% of in-core L1D accesses on a real V100 are ABI register traffic; an idealised unlimited-register machine recovers only 1.06x where CARS recovers 1.26x — i.e. the cost is the memory *instructions*, not capacity | `[paper]` | [`GPU-MICRO24-61`](../corpus/GPU-MICRO24-61--cars-concurrency-aware-register-stacks-gpu-function-calls.md) |
| **V100 HBM2 repair = 64-entry page-retirement table**; exhaustion produces page-retirement failures. Pre-Ampere row-remap cap is 64 | `[paper]` | [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md), [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md) |
| **Ampere-and-later 512-row remap budget** | `[paper]` | [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md) |
| **Ampere FP64/FP32/FP16/Tensor pipe counter split** (DCGM); tensor pipe idle for most of a production A100 population; 44% of jobs FP64-only | `[paper]` | [`GPU-IPDPS26-41`](../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md) |

**Volta/Turing/Ampere features NOT present**, stated so they are not imported:
no TMA, no `wgmma`, no thread-block clusters, no distributed shared memory, no
DPX hardware, no FP8 matrix path, no TMEM, no `tcgen05`. Ada (RTX 4090) likewise
has **no DSM, no `wgmma` and no DPX hardware**
`[paper, ` [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md)`]`.

---

## 2. NVIDIA — Hopper (H100 / H200 / H800)

| Feature established | Evidence | Corpus file |
|---|---|---|
| **`wgmma` — warp-group matrix issue, 128 threads**, measured at **128 cycles at `m64n256k16`** on H800 PCIe | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **`wgmma.mma_async` accumulates in the register file**, `tM=64, tK=32`; at SM90 EmuGEMM reaches 1,639 TOP/s = 83% of INT8 peak, 1.4x cuBLAS TF32, up to 2.3x ZGEMM (GH200) | `[paper]` | [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md) |
| **TMA** (`cp.async.bulk` family), characterised as an extension | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **Thread-block clusters + distributed shared memory (DSM)** — Hopper-only; cluster size ≤16 as a pruning rule, 227 KB SMEM, 2–3 TB/s global bandwidth on H100; pre-Hopper parts degenerate to the DA-only configuration, priced at 1.52x rather than 3.29x | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md), [`GPU-HPCA26-144`](../corpus/GPU-HPCA26-144--flashfuser-kernel-fusion-inter-core-connection-dsm.md) |
| **DPX hardware** | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **FP8 tensor cores** | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **H100 partitioned L2 plus an undocumented CPC level** (TPC/GPC/CPC hierarchy); CPC appears on H100 only | `[paper]` | [`GPU-MICRO24-63`](../corpus/GPU-MICRO24-63--uncovering-real-gpu-noc-characteristics.md) |
| p-chase corroboration on H800: near/far L2 hit **258 / 414.1 cycles** | `[paper]` | [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md) |
| **H100 96 GB MIG lattice**: `1g.12gb`…`7g.96gb` at **16/32/60/64/132 SMs**, 11/23/46.5/94.5 GB — a *different* lattice from A100's, with different non-proportionalities; a MIG scheduler tuned to one is not portable to the other | `[paper]` | [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md) |
| **MIG does not partition the power/clock domain** — residual cross-instance throttling channel on H100 | `[paper]` | [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md) |
| **128-SM / 64-TPC code-visible break**: below 128 SMs the libsmctrl 64-bit mask path is used; at or above 128 SMs the 128-bit `_ext` path is mandatory and `set_global_mask` is refused. A100 (108 SMs / 54 TPCs) uses the 64-bit path; H100 (132 SMs / 66 TPCs) does not | `[code]` | [`GPU-ASPLOS26-166`](../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md) |
| **H100 = 96 GB HBM3 with an unchanged 512-row remap budget**, against A100's 40 GB HBM2e — the stated cause of a 3.2x lower per-GPU MTBE (only 24% lower per-GB) | `[paper]` | [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md) |
| **Wattchmen instruction coverage falls from 70% on A100 to 66% on H100** because of new Tensor-Core opcodes — every new matrix-core generation reopens the coverage hole | `[paper]` | [`GPU-ICS26-183`](../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md) |

**Do not carry onto Blackwell**: Hopper's TMA and DSM must not be assumed on
Blackwell without evidence — stated explicitly in
[`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) `[paper]`.

---

## 3. NVIDIA — Blackwell (B200 / GB200; and the consumer part, which is different silicon)

| Feature established | Evidence | Corpus file |
|---|---|---|
| **`tcgen05.mma` — back to warp-scope issue**, measured at **11.4 cycles at `m256n256k16`** on B200; removal of warp-group synchronisation named as a cause of the latency drop | `[paper]` | [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) |
| **TMEM — accumulators leave the register file**; `tcgen05.mma` at SM100 uses `tM=128, tK=32`, giving 3,654 TOP/s = 81% of peak, 1.7x cuBLAS TF32, up to 5.5x ZGEMM (B200) | `[paper]` | [`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md), corroborated independently by [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) |
| **A hardware decompression engine** whose behaviour Accel-Sim and GCoM cannot model | `[paper]` | [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) |
| **FP6 / FP4 low-precision paths**, alongside much higher memory bandwidth on GB200 | `[paper]` | [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md) |
| **B200 FP64 matrix throughput ~30 TFLOP/s against H200's ~67 TFLOP/s** — a regression. The authors warn it "may directly undermine FP64 MMU adoption". *Qualifier: the paper's own Figure 12, FP64 matrix-unit throughput, B200 vs H200.* | `[paper]` | [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md) |
| **INT8 matrix throughput is being withdrawn in favour of FP8.** B300 (Blackwell Ultra) specification: **150 TOP/s INT8 against 4500 TFLOP/s FP8**. *Qualifier: the paper's Table I, vendor specifications as tabulated; **B300 was not measured**.* On the measured B200, INT8-Ozaki-II is ~2.1x faster than FP8-Ozaki-II at 16384³ (137–138 vs 61–65 TFLOP/s) | `[paper]` + `[documentation]` for the B300 row | [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md) |
| **GB200 SoL collective constants**: `L_SoL = 2·L_L2_RTT + L_remote_store` = **1.404 µs on two GB200**; barriers measured at >1 µs, ~40% of a 5 µs small-message AllReduce; scale-up domain GB200 NVL72, 72 GPUs, 130 TB/s aggregate | `[paper]` | [`GPU-SC26-21`](../corpus/GPU-SC26-21--every-microsecond-matters-speed-of-light-gpu-collectives.md) |
| **Consumer Blackwell (RTX 5070 Ti, GB20x) is a different product**: no TMEM, no `tcgen05`, no decompression engine in evidence. A core model validated at 17.41% MAPE against it says nothing about B200 | `[paper]` | [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md), flagged by [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) |

**Accumulator placement across three generations** — register file (Ampere) →
register file (Hopper) → **TMEM** (Blackwell). The claim is corroborated from two
independent directions: from the kernel-author side by
[`GPU-SC26-02`](../corpus/GPU-SC26-02--emugemm-fused-tensor-core-precision-emulation.md)
and from the instruction-measurement side by
[`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md).

---

## 4. AMD — CDNA2 (MI250X) and CDNA3 (MI300X, MI300A)

**CDNA2 — MI250X**

| Feature established | Evidence | Corpus file |
|---|---|---|
| **SVM interfaces with the Linux kernel's HMM**, contrasted by the paper with NVIDIA UVM being "developed for NVIDIA's specific hardware" — a stated generality/performance trade-off | `[paper]` | [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) |
| **SVM's management unit is a *range*, not a page**: 4 KB–1 GB, 1 GB-aligned, up to **256 K pages**; a single serviceable fault can migrate the whole range. Against UVM's 2 MB VABlock this is up to a ~512x granularity ratio, which is why insights do not transfer between vendors | `[paper]` | [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) |
| **Eviction is Least-Recently-Faulted, not LRU** — "may evict the most intensely reused data" | `[paper]` | [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) |
| **97–99% duplicate GPU fault storm**, no fault batching | `[paper]` | [`GPU-ICS24-02`](../corpus/GPU-ICS24-02--shared-virtual-memory-design-performance-implications.md) |
| **Dual-GCD package**: 2 GCDs per package, 64 GB HBM2e per GCD, intra-package Infinity Fabric; 1–4 Infinity Fabric links per GCD pair, i.e. **per-pair link counts are non-uniform** | `[paper]` | [`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md), [`GPU-SC24-01`](../corpus/GPU-SC24-01--gpu-to-gpu-communication-supercomputer-interconnects.md) |
| **Running an MI250X as a single GPU uses only half its compute resources** because of the dual-chiplet packaging | `[paper]` | [`GPU-ASPLOS25-107`](../corpus/GPU-ASPLOS25-107--gpulog-optimizing-datalog-for-the-gpu.md) |
| **Package-aggregated power reporting; no native 1 ms power mode** | `[paper]` | [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md) |
| Frontier node layout: **8 GCDs/node, 4 Cassini NICs/node, 2 GCDs per NIC** | `[paper]` | [`GPU-IPDPS26-02`](../corpus/GPU-IPDPS26-02--big-send-off-scalable-performant-collectives-deep-learning.md) |

**CDNA3 — MI300X (discrete) and MI300A (APU). These are not the same part.**

| Feature established | Part | Evidence | Corpus file |
|---|---|---|---|
| **Unified *physical* memory** — "any memory allocator including `hipMalloc` will allocate unified memory"; the migration path is deleted rather than tuned. Motivating cost on discrete AMD GPUs: **>65% of time in page migrations** (updating GPU tables + copying) | MI300A | `[paper]` | [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) |
| Requires **ROCm-6.0-era OpenMP** for `requires unified_shared_memory` with pointers mapped as zero-sized array sections; production OpenFOAM ported with O(100) lines by deleting `map` clauses | MI300A | `[paper]` | [`GPU-ISC24-01`](../corpus/GPU-ISC24-01--porting-hpc-applications-mi300a-unified-memory-openmp.md) |
| **Native 1 ms power mode** that MI250X lacks; but CPU and GPU sit in one package and therefore in **one power number** | MI300A | `[paper]` | [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md) |
| **228 CUs, 5.3 TB/s memory bandwidth** | MI300A | `[paper]` | [`GPU-SC26-41`](../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md) |
| **1.155x temperature and 1.062x frequency spread across an 8-GPU node**, producing persistent stragglers through a leader/straggler DVFS equilibrium | MI300X | `[paper]` | [`GPU-ISCA26-187`](../corpus/GPU-ISCA26-187--lit-silicon-thermal-imbalance-multi-gpu-coupling.md) |
| **MSCCL++ AMD port cost**: 7 weeks / one developer for MI300X, with fewer than 10 lines of hardware-specific code outside the algorithms (H100 NVSwitch support: 8 weeks / two developers). Portability is reported as engineering cost, not as an automatic property | MI300X | `[paper]` | [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) |
| **FP8 variant handling differs**: the CDNA-era branch is `HIP_R_8F_E4M3_FNUZ`, not E4M3 | CDNA | `[code]` | [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md) |
| **Wavefront width 64, not 32** — structurally breaks warp-width-coupled designs (a `log₂(32)=5`-step butterfly becomes 6 steps; 32x32x32 blocking must be redesigned) | CDNA generally | `[paper]` `[code]` | [`GPU-ASPLOS25-81`](../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md), [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md) |
| **RDNA3 ray accelerator: software owns the traversal stack**, one `IMAGE_INTERSECT_RAY` instruction — structurally different from the NVIDIA-style hardware state machine | RDNA3 | `[paper]` | [`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md) vs [`GPU-MICRO24-122`](../corpus/GPU-MICRO24-122--tta-generalizing-ray-tracing-accelerators-tree-traversals.md) |

**Explicitly NOT established for AMD in this corpus:**
- **No CDNA2/CDNA3 matrix-core (MFMA) numbers anywhere.** Cubie's introduction
  names AMD Matrix Core but **the evaluation is NVIDIA-only** — the census's seed
  note claiming NVIDIA/AMD/Intel coverage is corrected by the analysis
  `[paper]`, [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md).
  The entire sparse-on-matrix-unit line (FlashSparse, Acc-SpMM, SMaT, SPIDER) has
  **no AMD CDNA evaluation** — `NOT_IN_PAPER` in each. `NOT_ESTABLISHED`.
- The one AMD part measured by the Ozaki-II emulation paper is a **Radeon RX 9070
  XT (RDNA-class consumer)**, *not* a CDNA3 MI300. MI300X/MI325X/MI350X/MI355X
  are named as targets only. **Do not claim MI300X emulation measurements from
  that paper.** `[paper]`
- **No `W`/`T` power-sensor window table exists for any AMD GPU.**
  `NOT_ESTABLISHED`.

---

## 5. GH200 — Grace Hopper with NVLink-C2C

| Feature established | Evidence | Corpus file |
|---|---|---|
| **72 Arm cores + H100, 96 GB HBM3; 34 TFLOP/s FP64 vector against 67 TFLOP/s FP64 tensor-core peak.** That 2x vector→tensor FP64 ratio is what makes the DMMA path attractive on Hopper at all | `[paper]` | [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md) |
| **NVLink-C2C coherence makes the NIC detour unnecessary** for GPU-initiated far memory — named by DREAM's own related work as the hardware alternative that "requires new CPU design" | `[paper]` | [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) |
| **C2C coherent spilling used as a MIG partition-granularity workaround** — offloading requires NVLink-C2C; on a PCIe-attached H100 the same scheme runs at roughly an order of magnitude less bandwidth and without cache coherence, and the paper's premise would not hold (`[inference]`; no PCIe baseline is evaluated → `NOT_IN_PAPER`) | `[paper]` + `[inference]` | [`GPU-ISC26-165`](../corpus/GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md) |
| **GH200 packaging is a confound in resilience comparisons.** In the A100↔H100 comparison the H100s are delivered *as GH200 Superchips*, tightly coupled to Grace CPUs via NVLink-C2C — a packaging change, not only a GPU change, and the authors flag it | `[paper]` | [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md) |
| **GH200 power sensor regresses**: 20 ms GPU / 10 ms CPU window inside a 100 ms period — a **20% duty cycle**, the worst in the measured population | `[paper]` | [`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md) |
| **GH200 is an N4-node part** in the four-process-node energy series (N7 A100 → N6 MI250X → N5 MI300A → N4 GH200) | `[paper]` | [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md) |
| **132 SMs, 4.0 TB/s** | `[paper]` | [`GPU-SC26-41`](../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md) |
| **GICC on GH200 + IB HDR**: device-resident (kernels build WQEs and ring the mlx5 UAR doorbell), 2 nodes | `[paper]` | [`GPU-HPDC26-01`](../corpus/GPU-HPDC26-01--gicc-gpu-initiated-communication-coordination-runtime.md) |
| FP64 FEM validated to **9,216 GH200 on Alps** | `[paper]` | [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md) |

---

## 6. Tensions the corpus found and did NOT resolve

These are recorded as open, not adjudicated. Each is a case where two corpus
papers make measurements that do not reconcile and neither paper reconciles them.

### 6.1 B200 FP64 matrix regression vs working FP64 DMMA on GB200

- [`GPU-PPoPP26-02`](../corpus/GPU-PPoPP26-02--cubie-characterizing-matrix-multiplication-units.md)
  measures **B200 FP64 matrix throughput at ~30 TFLOP/s against H200's ~67
  TFLOP/s** and warns this "may directly undermine FP64 MMU adoption" `[paper]`.
- [`GPU-ISC26-02`](../corpus/GPU-ISC26-02--fp64-tensor-cores-high-order-finite-element.md)
  runs **working FP64 DMMA on GB200** and reports higher absolute GDOF/s than
  GH200. Critically, **that paper does not discuss any reduction or removal of
  FP64 Tensor Core capability on Blackwell** — verified by targeted query in the
  analysis `[paper]`. Its lower MDOF/W on GB200 is attributed by its own authors
  to three *other* causes: higher idle GPU power, a 4% higher clock, and much
  higher bandwidth and low-precision throughput that these kernels do not use.
- **The two are different products** — B200 SXM vs GB200 Superchip — and
  **neither paper reconciles them**. Do not merge the two measurements. Recorded
  as an **open tension**; the resolution is `NOT_ESTABLISHED`.
- This tension is load-bearing for the emulation branch: if the regression is
  real and general, FP64 emulation on low-precision matrix engines stops being
  clever and becomes necessary. See
  [`GPU_TENSOR_CORE_LINEAGE.md`](GPU_TENSOR_CORE_LINEAGE.md) §3.

### 6.2 Matrix-instruction issue scope: warp → warp-group → warp

Visible only by reading two IPDPS papers together `[paper, both]`:

```
Ampere / Ada    warp-scope      mma
Hopper          warp-GROUP      wgmma      128 threads, 128 cycles at m64n256k16 (H800 PCIe)
Blackwell B200  warp-scope      tcgen05.mma            11.4 cycles at m256n256k16 (B200)
```
Anchors: [`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md),
[`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md).

**The issue unit widened and then narrowed again in two generations, while
accumulator placement moved monotonically away from the register file
(RF → RF → TMEM).** Neither paper explains *why* the issue scope reversed; the
Blackwell paper names removal of warp-group synchronisation as a cause of the
latency drop, which is a consequence, not a design rationale. The rationale is
`NOT_ESTABLISHED`.

The practical consequence for the kernel literature is concrete: the whole
warp-level `mma.m16n8k*` sparse line (FlashSparse, Acc-SpMM, SMaT) uses **no
Hopper-specific feature at all**, so an H100 result from those papers is a
warp-level kernel running on a warpgroup-capable part —
`[inference]`, and part of why H100 shows the *smallest* relative gain in
Acc-SpMM's three-generation table.

### 6.3 What a GPU issue stage is

[`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md)
assumes a hardware scoreboard and operand collectors;
[`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)
measures that real Turing/Ampere/Blackwell cores have neither. Neither evaluates
against the other. **Any future work must state which core model it assumes.**
Unresolved.

### 6.4 Whether a Blackwell model is possible at all

[`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md)
builds a Blackwell model at 17.41% MAPE;
[`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md)
states a Blackwell model of TMEM and the decompression engine **is not yet
possible**. Both are correct — MICRO'25 models a *consumer* part that has neither
unit. This is a product tension, not a contradiction, and it is recorded here
precisely so it is not read as one.

---

## 7. Measurement caveats that make generation numbers non-comparable

**These caveats apply to every number in §1–§5 and must travel with them.**

### 7.1 Hopper matrix throughput depends on the input *data*, with a power and clock consequence

[`GPU-IPDPS24-61`](../corpus/GPU-IPDPS24-61--benchmarking-dissecting-nvidia-hopper.md)
measures on an **H800 PCIe** that `wgmma` throughput depends on the *contents* of
the input matrices:

- **all-zero inputs: under 200 W, >95% of peak**
- **random inputs: 350 W, and the clock falls below the 1620 MHz whitepaper figure**

The paper reports matrix throughput as `Total_OPS / Duration` rather than in
cycles precisely to expose this `[paper]`.

**The mechanism was later isolated deliberately.**
[`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md)
decomposes GPU energy into control and datapath and finds the **datapath is only
8–35% of HBM energy**, the rest being content-independent control. Two labs, two
purposes, one physics. That paper's own citations place the effect on a nine-year
lineage: Lucas et al. 2016 (ALUPower) → Bhalachandra et al. 2022 (the
random-vs-zero methodology adopted) → Gregersen et al. 2025 `[paper]`.

**Consequence, stated as an inference and grounded in both papers' measured
quantities:** any GPU power or energy number measured with zero-filled or
constant-filled input buffers is a **lower bound** on real datapath energy,
potentially by the full datapath fraction `[inference]`. And any matrix-unit
*throughput* number measured on zeros is an upper bound on what a real workload
will see, because the real workload will clock down.

### 7.2 NVML's boxcar sampling window — most of the time is unobserved

[`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md)
is the only paper in the corpus with a **real external ground truth**: an
ElmorLabs PMD-USB, 12-bit ADC, 0–31 V ±0.1 V, 0–200 A ±0.5 A, 34 kHz internal /
**5 kHz effective over serial**, shunted on the 6/8-pin connectors and the PCIe
slot via a modified riser (the 3.3 V rail, ~10 W, is unmeasured). Population:
**70+ physical GPUs, 25+ models, 12 architectural generations (Fermi→Hopper)**.

Measured boxcar window `W` inside publication period `T`:

| Generation | `T` (period) | `W` (boxcar window) | Duty cycle |
|---|---|---|---|
| Kepler / Maxwell / Pascal / Volta | 20 ms | 10 ms | 50% |
| Turing (incl. RTX 3090 `instant`) | 100 ms | 100 ms | **100% — contiguous** |
| A100 (`instant`) | 100 ms | **25 ms** | 25% |
| H100 (`instant`) | 100 ms | **25 ms** | 25% |
| H100 (`average`) | 100 ms | 1 s | — |
| GH200 | 100 ms | **20 ms GPU / 10 ms CPU** | 20% |

**The direction of travel is backwards.** Turing had a contiguous window; A100,
H100 and GH200 each sample a shrinking fraction of the period. Because the design
used multiple physical samples per model, the paper can further state that the
gain error is **board-to-board random rather than model-systematic** `[paper]`.

**Three consequences for reusing generation numbers:**

1. **Any power *range* or *swing* statistic computed from NVML is a lower bound**
   on the true swing: excursions falling in the unobserved 75% are simply
   missing. This directly qualifies
   [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md)'s
   headline — DBEs tracking a ~33 W 15-minute power *range* (p = 0.00056 after
   Šidák correction) on **V100**, a `W = T/2` part. The sensor result does not
   weaken that finding; it strengthens its *direction* while making its
   *magnitude* untrustworthy. **Any re-analysis of power-swing-vs-reliability on
   Ampere or Hopper telemetry must correct for `W/T = 0.25` or it will
   systematically understate the swing** `[inference, grounded in both papers'
   measured quantities]`.
2. **The Hopper 200 W / 350 W `wgmma` figures in §7.1 are `nvidia-smi` numbers**,
   i.e. produced by a 25 ms-in-100 ms observer. The *direction* is robust because
   it is a large steady-state difference; the *absolute* values inherit the ±5%
   proportional error and any phase misalignment during the throttling transient.
3. **Papers that use NVML as ground truth inherit its granularity as their
   accuracy floor.** Both
   [`GPU-ICS26-183`](../corpus/GPU-ICS26-183--wattchmen-per-instruction-gpu-energy-modeling.md)
   and [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md)
   say so. Wattchmen's stated NVML-granularity limitation is exactly the
   phenomenon Yang et al. quantified — **and Wattchmen does not cite that paper**
   `NOT_CITED`.

### 7.3 The AMD side has no equivalent table, and the tooling cadence differs from the native cadence

[`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md)
independently rediscovers the same failure mode on AMD — an **undocumented
running average** in the power field — but takes a different route: it
**bypasses** the filter by differentiating the `rocm-smi`/`amd-smi` **energy
counter** at **1 ms** (native on MI300A; MI250X lacks the mode), and validates
only sensor-against-sensor (Cray PM "to within 5% (Frontier) / 1% (Portage)",
against an unnamed reference; +30 W static NIC offset on Portage, declared
non-generalisable). **It never derives a `W`/`T` pair.**

Consequence: [`GPU-SC25-184`](../corpus/GPU-SC25-184--benchmark-driven-energy-attribution-gpu-supercomputing.md)
samples MI250X and MI300A at **1 Hz** — three orders of magnitude coarser — and
reports that **AMD thermal throttling confounds its zero-vs-random datapath
separation on exactly those two parts**. Read together, the LBNL confound is a
predictable consequence of sampling a throttling device at 1 Hz, and the ISC 2026
instrument is the one that would resolve it. **Nobody has done this**
`NOT_ESTABLISHED`.

### 7.4 Simulated numbers and measured numbers are in different units of trust

- **The fixed-function-repurposing area is the worst case**: the software branch
  measures real silicon (RTX 3090, RTX 4060 Ti) against SIMT baselines and
  reports 10x–100x; the hardware branch simulates (Accel-Sim V100, Vulkan-Sim
  8–30 SM scale models, Emerald) against an *already-RT-accelerated* baseline and
  reports 1.1x–2.5x. **No table should place them in the same column.**
- **Virgo's Volta/Ampere/Hopper "baselines" are the authors' RTL abstractions**
  at 8 lanes/warp and 400 MHz on a 16 nm PDK — **not** measurements of V100, A100
  or H100. Every Virgo comparative number is Virgo-vs-*model*
  `[paper]`, [`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md).
- **HSU's simulated GPU is a Volta V100 configuration** — a GPU that in reality
  has **no RT cores at all**; the RT unit is a modelled addition
  `[paper]`, [`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md).
- **GhOST's 0.007% area figure** is a 45 nm synthesis estimate scaled by a stated
  0.17 multiplier toward 14 nm and compared against a 445 mm² 12 nm die. It mixes
  process nodes; treat it as order-of-magnitude
  `[paper]`, [`GPU-ISCA24-61`](../corpus/GPU-ISCA24-61--ghost-gpu-out-of-order-warp-scheduling.md).

### 7.5 Export-restricted and binned parts are not the headline parts

**H800 ≠ H100** (different interconnect and some throughput characteristics);
**A800 ≠ A100**. Both appear in the corpus as measured parts and both are flagged
by their own analyses. Likewise the **A100 40 GB vs 80 GB** difference in
production variability is a within-generation *binning* effect, not a generation
effect `[paper]`, [`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md).

### 7.6 Telemetry counters move when software moves

Three independent papers establish that a software-stack change can shift a
hardware counter by orders of magnitude — a standing hazard for any longitudinal
GPU-fleet study:
- A **RHEL 8 update on 18 August 2021 correlates with a 170-fold increase in
  page-retirement-failure counts** from 1 September 2021 `[paper]`,
  [`GPU-ICS24-01`](../corpus/GPU-ICS24-01--summit-gpu-memory-corruption.md).
- H100's **zero observed NVLink errors** is explicitly *not* attributed to
  hardware improvement, because changes in NVLink error-logging mechanisms cannot
  be ruled out `[paper]`, [`GPU-SC25-01`](../corpus/GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md).
- A **libfabric 1.20.1 regression** whose 14 January 2025 fix measurably reduced
  measured variability `[paper]`,
  [`GPU-IPDPS26-42`](../corpus/GPU-IPDPS26-42--elusive-application-performance-production-gpu.md).

### 7.7 Two semantic traps in production GPU telemetry

`GPU_UTIL` vs `SM_ACTV` mean different things and are routinely confused; DCGM
has a **10-second sampling floor**; exclusive allocation strands capacity. All
three are properties of the DCGM/LDMS/Slurm stack rather than of Ampere and
**will recur on any DCGM-monitored machine** `[paper]`,
[`GPU-IPDPS26-41`](../corpus/GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md).
DCGM is NVIDIA-only, so there is no AMD or Intel arm to this dataset.

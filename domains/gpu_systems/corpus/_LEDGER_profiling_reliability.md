# Profiling, debugging, correctness, simulation & performance modelling + reliability/telemetry/production performance (taxonomy N and O) — GPU relevance verdict ledger

last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
cluster: `N` = profiling, debugging, correctness checking, simulation & performance modelling · `O` = reliability, telemetry & production GPU performance

Verdicts are `CORE_GPU` / `RELATED_GPU` / `EXCLUDE` / `UNRESOLVED`.
Access states are `PUBLIC_FULLTEXT` / `CLOSED_ACCESS` / `PENDING_FULLTEXT` /
`PUBLIC_ARTIFACT_ONLY` / `ABSTRACT_ONLY`.
`evidence_read` records what was **actually** read. A verdict reached from a
title and a census row says so and **may not** be used to justify a deep
analysis (task §2). Every row carries a counterfactual answer (task §3).

---

## 0. Reading notes that apply to the whole ledger

1. **The counterfactual test was applied strictly.** Where a paper's method is
   architecture-neutral and only its subject happens to run on GPUs, the
   verdict is `RELATED_GPU`, not `CORE_GPU` — see the `Interpretable Analysis
   of Production GPU Clusters` and `PICO`-style reasoning. Two rows below are
   deliberately downgraded on this ground.
2. **Verdict-only rows were not upgraded by guesswork.** For papers whose only
   available evidence is an official title plus this repository's census row,
   `evidence_read` is `TITLE + CENSUS_ROW` and the counterfactual answer is
   explicitly marked as resting on a title-named GPU mechanism. These rows are
   watchlisted, never deep-analysed.
3. **`dl.acm.org` (403), `ieeexplore.ieee.org` (418) and `dblp.org` (robots)
   are unreachable from this environment**, which is why several ACM/IEEE-only
   papers are `CLOSED_ACCESS` despite being formally open-access at the
   publisher. This is an access-path limitation, not a claim about the paper's
   licence.
4. **arXiv ID `2609.07912` (the SC 2026 PyKokkos debugger) returned HTTP 429 on
   eight attempts** across `/abs/`, `/pdf/` and `/html/v1`, `/html/v2` paths,
   spread over the session with pauses. Other arXiv IDs fetched normally in the
   same session (`2503.11901` v1/v4, `2604.20032` v1), so this is specific to
   that identifier, not a general arXiv block. Recorded as `PENDING_FULLTEXT`.
5. **Stable-ID band.** This cluster's colliding IDs sit in a **`-41`/`-42`
   band**. `-01`/`-02` for SC 2024, HPCA 2024, IPDPS 2026, SC 2026 and
   MICRO 2024 were concurrently assigned by other clusters writing into
   `domains/gpu_systems/corpus/` during this pass; per
   `governance/ID_NAMING_RULES.md` an ID is never reused for a different
   source, so these were renumbered into a distinct band rather than
   collided. `GPU-SC25-01`, `GPU-MICRO25-01` and `GPU-ICS24-01` are
   uncontested — and the memory/virtualization cluster's ledger explicitly
   records that it **ceded `GPU-ICS24-01`** to this cluster's Summit analysis
   and renumbered its own file to `GPU-ICS24-02`. See §3.

---

## 1. Priority papers

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| HiRace: Accurate and Fast Data Race Checking for GPU Programs | SC 2024 | `PUBLIC_FULLTEXT` (author PDF `userweb.cs.txstate.edu/~mb92/papers/sc24.pdf`; NSF PAR mirror `par.nsf.gov/10583102`) + `[code]` artifact cloned `github.com/JohnJacobsonIII/HiRace-Artifact-SC24` @ `44a935f90acfe43c6178b2187ea84c9ab0c01450` | Full paper in two passes: motivation and prior-tool critique, shadow-state/FSM design, Clang instrumentation; then evaluation hardware, Indigo + Rodinia/cuda-samples suites, accuracy tables vs iGUARD and compute-sanitizer, slowdown, memory overhead, limitations, related work. Plus real source: 25 named ISM states, `TRANSITION_COUNT 1200`, the exact 64-bit shadow bit-field layout | **NO** — the FSM's axes *are* the GPU hierarchy: sync scopes `{UNSYNC, WARPSYNC, BLOCKSYNC}` × thread relations `{SAMETHREAD, SAMEWARP, SAMEBLOCK, SAMEGRID}`, with block- vs grid-scoped atomics (`BA`/`GA`) as distinct memory actions | `CORE_GPU` | Replaces per-accessor vector clocks with a fixed 8-byte state over the scoped-barrier lattice; the motivating constraint (per-address records cannot cover device memory, which is why NVIDIA's racecheck sees only shared memory) is a GPU capacity fact. | `GPU-SC24-41--hirace-gpu-data-race-checking.md` |
| Story of Two GPUs: Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs | SC 2025 | `PUBLIC_FULLTEXT` (arXiv 2503.11901, v1 + v4 HTML). DOI `10.1145/3712285.3759821` | Full paper across two versions: v1 for system, XID pipeline, per-XID MTBE/persistence tables, propagation analysis, job impact, hardware mechanisms; v4 for the A100-vs-H100 comparison, per-GPU and per-GB MTBE, component-improvement table, HBM3 argument, availability projection, limitations | **NO** — every mechanism is a GPU failure mode in NVIDIA's XID vocabulary: GSP coprocessor, PMU SPI link, GPU MMU, NVLink CRC retry, and the HBM row-remapping engine with its 512-spare-row budget and contained/uncontained containment states | `CORE_GPU` | The finding — H100 memory resilience regressed because HBM capacity per GPU grew 2.4× while the row-remap spare pool stayed at 512 rows — has no CPU analogue; it is a property of on-die DRAM repair hardware. | `GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md` |
| Characterizing Production GPU Workloads using System-wide Telemetry Data | IPDPS 2026 | `PUBLIC_FULLTEXT` (official author PDF `cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026c.pdf`; preprint arXiv 2502.18680). DOI `10.1109/ipdps65963.2026.00078`, pp. 899–912 | Full paper: system config, LDMS/DCGM/Prometheus/Slurm stack, 10 s sampling, the complete counter list with the authors' own definitions, utilisation-by-job-size, FP-pipeline intersections, HBM capacity findings, roofline split, spatial/temporal imbalance, counter correlations, limitations | **NO** — the instrument is the DCGM counter set and the findings are about GPU microarchitectural structures: per-precision pipe activity (`FP16/FP32/FP64/TNSR_ACTV`), `SM_ACTV` defined over warps per multiprocessor, HBM capacity/DRAM activity, NVLink vs PCIe rates | `CORE_GPU` | 44% of jobs are FP64-only with the tensor pipe dark; 55% of 80 GB-requesting jobs fit in 40 GB of HBM; 12% of 4-GPU jobs strand three GPUs. Each is meaningless without per-precision pipes and multi-GPU-per-node packaging. | `GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md` |
| The Case of the Elusive Application Performance on Production GPU Supercomputers | IPDPS 2026 | `PUBLIC_FULLTEXT` (official author PDF `cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026b.pdf`). DOI `10.1109/ipdps65963.2026.00079`, pp. 913–927 | Full paper: both systems, the full app/run table reconciling to 761 jobs, node-hours and window, the Cassini NIC counter table, mpiP / PyTorch Profiler / HTA tooling, the GEMM + MPI + NCCL/RCCL micro-benchmark harness, Spearman and XGBoost attribution with MAPE and Direction Accuracy, per-system variability, the GPU-exclusion test, feature importances, limitations | **NO** (closest call in the cluster) — the method is architecture-neutral, but the substantive contribution is a *GPU-specific falsification*: it builds a per-GPU FP16 GEMM instrument, establishes real A100/MI250X heterogeneity, shows it does not reach runtime (Spearman 0.07/0.08), and relocates the variance into NCCL/RCCL collectives and the GPU→NIC PCIe hop | `CORE_GPU` | Degraded-but-alive GPUs are real (28% GEMM spread system-wide on Perlmutter) yet explain none of the variability; the variance lives in GPU-resident collectives (DeepCAM `Allreduce` up to 24× slower on Frontier). | `GPU-IPDPS26-42--elusive-application-performance-production-gpu.md` |
| LEO: Tracing GPU Stall Root Causes via Cross-Vendor Backward Slicing | **venue UNRESOLVED** — assigned as SC 2026; census records `NOT_FOUND` in any official SC26 source and `SC26_MEMBERSHIP_UNVERIFIED`; the arXiv record carries no venue comment. Treat as `PREPRINT` | `PUBLIC_FULLTEXT` (arXiv 2604.20032 v1 HTML only — `/abs/` and `/pdf/` both returned no extractable text) | Full paper in two passes: title/authors/abstract, motivation, five-phase workflow, CCT dependency graph, instrumentation substrate, platforms and 21 workloads, limitations; then per-vendor synchronization modelling, the four pruning stages, the inverse-distance blame formula, per-vendor stall taxonomies, overhead and analysis time, the per-workload speedup table, related work | **NO** — decodes GPU-specific compiler-managed synchronization hardware: AMD `s_waitcnt` with `vmcnt`/`lgkmcnt` outstanding-operation counters, NVIDIA B1–B6 scoreboard barrier bits in SASS control fields with `control.stall` hints, Intel SWSB `SBID` tokens; consumes CUPTI's 13, ROCprofiler-SDK's 10+ and Level Zero's 8 stall categories | `CORE_GPU` | No CPU has an `s_waitcnt`-style software wait counter to reverse-count; cited CPU machine-code slicing work never faced this. **Venue unverified — record as preprint.** | `GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md` |
| GCStack+GCScaler: Fast and Accurate GPU Performance Analyses Using Fine-Grained Stall Cycle Accounting and Interval Analysis | ISCA 2025 (Session 8A Performance and Modeling) | **`PUBLIC_ARTIFACT_ONLY`** — paper `CLOSED_ACCESS`: `dl.acm.org/doi/pdf/10.1145/3695053.3731068` returned **403** (single attempt, not retried per environment rules); no author-hosted PDF found by search of the Yonsei HPCP lab pages. Artifact **is** public and was cloned: `github.com/yonsei-hpcp/gcstack_gcscaler` @ `95ea0dea3d3098dcfed31eea6ae143cd56db5df2` | `[code]` + `[README]` **only — no paper text.** Verified from source: GCStack's per-warp-scheduler classification in `gpu-simulator/gpgpu-sim/src/gpgpu-sim/shader.cc` (`sub_core_stack` indices 0=Base, 1=idle, 2=Ctrl, 3=last/SCBLAST, 4=bar, 5=memData, 6=comData, 7=Struct) and its emitted fields `GCStack_Base / MemStruct / MemData / Sync / ComStruct / ComData / Control / Idle / Total` plus idle sub-classification `EmptyWS / IdleSubcore / IdleSM`; GCScaler's `GCoMModel::CycleBreakdown` in `gcscaler/src/include/interval_model.h` (`base, comData, comStruct, memData, memStruct, idle` + `memDataScbLast, memDataQueue, memDataQueueNoC, memDataQueueDRAM, memStructMSHR, memStructL1Bank`). READMEs confirm GCStack is built on Accel-Sim and GCScaler extends **GCoM (ISCA '22)**, calibrating representative warps from GCStack's baseline CPI | **NO** — the artifact's own data structures are a warp-scheduler stall taxonomy (per-warp `memData` vs `comData` vs `Struct` vs `bar` vs `Ctrl`) with sub-classification down to MSHR and L1-bank structural stalls and NoC-vs-DRAM queueing; these are SM issue-stage and GPU memory-hierarchy categories | `CORE_GPU` | Verdict is safe from `[code]` evidence alone. **Deep analysis NOT permitted (task §2: artifact-only ⇒ verdict only).** → **watchlist** | — (watchlist) |
| Swift and Trustworthy Large-Scale GPU Simulation with Fine-Grained Error Modeling and Hierarchical Clustering (**STEM+ROOT**) | MICRO 2025 (Session 7B Tools and Simulators) | `PUBLIC_FULLTEXT` (author PDF `seonjinna.github.io/assets/pdf/MICRO25_stem_root.pdf`). DOI `10.1145/3725843.3757107` | Full paper: motivation and the critique of PKA/Sieve/Photon/TBPoint, the CLT sample-size derivation and KKT multi-cluster allocation, the ROOT recursive-split rule and its simulation-time stopping condition, weighted-sum reconstruction, simulator/GPU/benchmark setup with speedup and error tables, DSE and cross-GPU portability, limitations | **NO** — the sampling unit is the **GPU kernel invocation**, and the premise is that GPU AI workloads replay a fixed compute graph launching one kernel symbol up to 11.6 M times with identical code but different tensor shape, sparsity, alignment and inherited L2 state, so static code signatures are provably constant across invocations that differ in cycles | `CORE_GPU` | Displaced baselines are all GPU kernel samplers; the warmup ablation is over GPU L2 between launches; evaluation runs in MacSim/AccelSim/MGPUSim. **The real claim is bounded error, not speed** — Photon is 1.54× faster on CASIO at 27× the error. | `GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md` |
| GPU Scale-Model Simulation | HPCA 2024 (Session 10B GPU) | `PUBLIC_FULLTEXT` (author PDF `users.elis.ugent.be/~leeckhou/papers/hpca2024.pdf`). DOI `UNKNOWN` | Full paper: motivation and critique of prior sampling / reduced-input / FPGA work and of CPU scale-model regression, the proportional-scaling construction with Table I, all three extrapolation formulas with variable definitions, Accel-Sim config, the 21+6 benchmark scaling classification, strong- and weak-scaling accuracy against four regression baselines, the multi-chiplet case study, speedups, assumptions and failure cases | **NO** — the paper exists *because* the CPU scale-model method fails on GPUs (logarithmic regression: 69% avg / 86% max error at 128 SMs, since GPU workloads split 7 super-linear / 9 linear / 5 sub-linear). Scaling variable is SM count; invariants are per-SM warp slots (48 warps × 32 threads), L1 and scratchpad; scaled quantities are shared L2 (34 MB / 64 slices), NoC bisection BW, HBM BW and memory-controller count | `CORE_GPU` | The cliff term `1/(1−f_mem)` is defined over the fraction of cycles in which *all resident warps on an SM* await data — a warp-level-parallelism latency-hiding statement with no single-thread CPU analogue. | `GPU-HPCA24-41--gpu-scale-model-simulation.md` |
| Understanding GPU Memory Corruption at Extreme Scale: The Summit Case Study | ICS 2024 (Session 5A Reliability, Dependability and Availability) | `PUBLIC_FULLTEXT` (author-hosted PDF `christian-engelmann.de/publications/oles24understanding.pdf`). DOI `10.1145/3650200.3656615`. Released dataset DOI `10.13139/OLCF/1970187` | Full paper: authors/venue/DOI, Summit configuration, XID + 1 Hz power/thermal + scheduler + reboot-log pipeline, the released dataset, the numbered Findings, DBE distribution and streak analysis, the power-vs-temperature result with Šidák-corrected p-value and effect size, Cox regression over user/project strata, HBM2/SECDED/page-retirement mechanisms, operational implications, limitations | **NO** — the mechanism is NVIDIA's GPU memory-repair path: XID 48/63/64, the driver's dynamic **page-retirement** table with its **64-page cap**, and SECDED over 3D-stacked HBM2, with per-GPU 1 Hz power telemetry from a 6-GPU node as the decisive covariate | `CORE_GPU` | A CPU DRAM field study would use MCE counters and OS page offlining, with no per-device retirement budget to exhaust and no 33 W burst-power signal from SM/Tensor-Core activity. The mixed-precision susceptibility finding needs mixed-precision units. | `GPU-ICS24-01--summit-gpu-memory-corruption.md` |
| Interactive Debugger for Performance Portable Python HPC Kernels (**pkdb**) | SC 2026 — census records `SC26_MEMBERSHIP_UNVERIFIED`; the artifact README states **"Artifact for SC'26"**, which is `[README]` evidence for the venue | **`PENDING_FULLTEXT`** + `PUBLIC_ARTIFACT` — arXiv 2609.07912 returned **HTTP 429 on eight attempts** across `/abs/`, `/pdf/`, `/html/v1`, `/html/v2` with pauses (other arXiv IDs succeeded in the same session). Artifact cloned: `github.com/EngineeringSoftware/pkdb` @ `abbe687eb81686edecd158ceea52684b7e6ac8b2` | `[code]` + `[README]` **only — no paper text.** Verified from source: `pkdb/controllers/accelerator_gdb_controller.py` sets `gdb_executable = "rocgdb"` for `hip` and `"cuda-gdb"` otherwise, driving them over GDB/MI (`interpreter-exec mi3`, annotate3); `pkdb/commands/accelerator_helpers.py` parses **`info cuda threads`** / **`info hip threads`** and issues `info cuda kernels`; `pkdb/core/breakpoint_manager.py` holds `_python_to_cpp: (source_file, python_line) -> [(functor_path, cpp_line)]` with a reverse map, resolving Python breakpoints to lines in the generated Kokkos **functor** C++; `pkdb/runtime/helper.py` detects `{"type":"cuda"}` / `{"type":"hip"}`; README's prerequisite table maps OpenMP→`gdb`, Cuda→`cuda-gdb`, HIP→`rocgdb`, and names three advanced capabilities (live code evaluation, kernel call-site substitution, concurrent kernel comparison). A modified PyKokkos is vendored | **NO** — debugging is **on the real device, not a CPU fallback**: pkdb attaches the vendor GPU debuggers (`cuda-gdb`/`rocgdb`) to a live PyKokkos process and reads GPU thread state through `info cuda threads` / `info hip threads`, while mapping Python source lines onto lines of the generated CUDA/HIP Kokkos functor | `CORE_GPU` | Verdict is safe from `[code]`+`[README]` evidence. **Deep analysis NOT permitted (task §2: no full text read).** → **watchlist**, and the arXiv 429 should be retried from another network path. | — (watchlist) |

---

## 2. Verdict-only papers

Ordered by cluster sub-theme. No row here was deep-analysed **except**
*Over-Synchronization in GPU Programs*, which is marked and explained.

### 2.1 Correctness, sanitizers, numerical reliability (taxonomy N)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| **Over-Synchronization in GPU Programs** (**ScopeAdvice**) | MICRO 2024 (Session 5C Debugging Correctness/Performance) | `PUBLIC_FULLTEXT` (author PDF `csa.iisc.ac.in/~arkapravab/papers/MICRO24_ScopeAdvice.pdf`) | **Full paper** — scope/cost motivation, the three over-synchronization variants, trace model and windowing, NVBit instrumentation with per-location metadata layout, Rules 1–3 and the detection algorithm, the PTX-memory-model validity argument, full evaluation (hardware, instance counts, speedup + stall-cycle table, four-stage overhead breakdown, memory overhead), limitations, related work | **NO** — defined by CUDA's scoped memory model over an **incoherent per-SM L1 / coherent L2**: `__threadfence_block()` vs `__threadfence()` vs `__threadfence_system()`, a measured **21× block-vs-device fence cost on RTX 3090**, the `MultiBlock` bit over CUDA threadblocks, soundness discharged against the **PTX** memory model, and SASS/PTX instrumentation (`LDG.SYS`, `isspacep.global`) | `CORE_GPU` | The exact dual of HiRace — too *much* synchronization rather than too little, over the same scope lattice. 29–37% speedups on real library code (cuML, cudpp); 0% where fences were not hot. **Deep-analysed under the task's spare-capacity permission.** | `GPU-MICRO24-41--over-synchronization-in-gpu-programs.md` |
| RedSan: A Redundant Memory Instruction Sanitizer for GPU Programs | SC 2025 | `CLOSED_ACCESS` — DOI `10.1145/3712285.3759830`, pp. 368–382; census records `NOT_FOUND_AFTER_SEARCH` for public full text; `dl.acm.org` 403 | TITLE + CENSUS_ROW (census screen reason: "GPU memory-instruction sanitizer (compiler/runtime instrumentation of GPU kernels)") | **NO**, on a title-named GPU mechanism — a *redundant memory instruction* sanitizer for GPU programs implies compiler/runtime instrumentation of GPU kernel memory accesses. Basis is the title and census row, not the paper | `CORE_GPU` | Title-explicit "for GPU Programs" plus a memory-instruction instrumentation mechanism. The immediate sanitizer neighbour of HiRace and Triton-Sanitizer. → **watchlist** | — (watchlist) |
| Triton-Sanitizer: A Fast and Device-Agnostic Memory Sanitizer for Triton with Rich Diagnostic Context | ASPLOS 2026 (4A ML Training & Monitoring, 31V2) | `CLOSED_ACCESS` via this environment — DOI `10.1145/3779212.3790241`; census notes an **open publisher PDF** at `dl.acm.org/doi/pdf/…` (403 here) and an author-group page `jokeren.tech/publication/wu-2026-triton-sanitizer/`. Related group repo `github.com/Deep-Learning-Profiling-Tools/triton-viz` is **not stated to be the paper's artifact** | TITLE + CENSUS_ROW | **NO**, on a title-named GPU mechanism — Triton is a GPU kernel language; a memory sanitizer for it instruments GPU kernel memory accesses. "Device-agnostic" in the title means across GPU vendors, not across GPU/CPU | `CORE_GPU` | GPU memory-safety instrumentation at the Triton compiler/runtime boundary. → **watchlist**; the open publisher PDF is worth retrying from another network path. | — (watchlist) |
| FloatGuard: Efficient Whole-Program Detection of Floating-Point Exceptions in AMD GPUs | HPDC 2025 (session "Numerical Methods") | `CLOSED_ACCESS` — census records `NOT_FOUND_AFTER_SEARCH` for both full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW + authors (Dolores Miao, Ignacio Laguna, Cindy Rubio-González), `CONFIRMED_IN_POPULATION` | **NO** — title-explicit "in **AMD** GPUs"; whole-program FP-exception detection on the ROCm/HIP stack requires AMD GPU-specific exception reporting and instrumentation | `CORE_GPU` | One of very few AMD-specific correctness tools in the corpus, and the AMD counterpart to the NVIDIA-oriented FP-exception line below. → **watchlist** | — (watchlist) |
| FPBOXer: Efficient Input-Generation for Targeting Floating-Point Exceptions in GPU Programs | HPDC 2024 (session "Resilience") | `CLOSED_ACCESS` — census records `NOT_FOUND_AFTER_SEARCH` for full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW + authors (Anh Tran, Ignacio Laguna, Ganesh Gopalakrishnan); census marks it **title-explicit** | **NO**, on a title-named GPU mechanism — input generation targeting FP exceptions *in GPU kernels*; the search space and the exception-observation mechanism are GPU-kernel-specific. Basis is title + census row | `CORE_GPU` | Title-explicit "in GPU Programs". Shares an author (Gopalakrishnan) with HiRace, i.e. the same Utah correctness group. → **watchlist** | — (watchlist) |
| Fine-Grained Global Search for Inputs Triggering Floating-Point Exceptions in GPU Programs | IPDPS 2025 (S32 Error Prediction and Fault Tolerance) | `CLOSED_ACCESS` — census records `NOT_FOUND_AFTER_SEARCH` for full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW | **NO**, on a title-named GPU mechanism — same problem class as FPBOXer, one year on, with a finer-grained global search. Basis is title + census row | `CORE_GPU` | Title-explicit "in GPU Programs"; census screen reason is GPU numerical-reliability tooling. Appears to be the direct successor to FPBOXer — **an unverified lineage worth confirming.** → **watchlist** | — (watchlist) |
| Towards Unified Analysis of GPU Consistency | ASPLOS 2024 **volume 4** (29V4) — DOI year 2024, **presented at ASPLOS 2025**; census records it `NOT_IN_MAIN_POPULATION` for 2025 and files it under `ASPLOS_2024.md` | `PUBLIC_FULLTEXT` (author PDF `hernanponcedeleon.github.io/pdfs/asplos2024.pdf`; second copy `researchportal.helsinki.fi/files/646149224/Towards.pdf`). DOI `10.1145/3622781.3674174`. **Full text not fetched in this pass** | TITLE + CENSUS_ROW (census screen reason: "GPU memory-consistency model; axiomatic unification of PTX/Vulkan/scoped GPU models. GPU memory model is the whole paper"). First author recorded as Haining Tong et al. from the author-page PDF title line | **NO** — the subject is the axiomatic semantics of **scoped** GPU consistency models (PTX and Vulkan), i.e. the formal object that ScopeAdvice's soundness argument and HiRace's sync lattice both rely on | `CORE_GPU` | Census states the GPU memory model *is* the whole paper. **Access is public — this is the highest-value unread item in the cluster**, because it is the formal foundation the two 2024 synchronization tools depend on. → **watchlist, priority** | — (watchlist) |

### 2.2 Profiling and performance attribution (taxonomy N)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| DeepContext: A Context-aware, Cross-platform, and Cross-framework Tool for Performance Profiling and Analysis of Deep Learning Workloads | ASPLOS 2026 (4A ML Training & Monitoring) | `CLOSED_ACCESS` — census records DOI `UNKNOWN` and `NOT_SEARCHED` for full text; `dl.acm.org` 403 | TITLE + CENSUS_ROW, **plus a verified external citation**: LEO's related-work section names DeepContext as a cross-platform tool that "lack[s] instruction-level root-cause analysis" `[paper, LEO]` | **NO**, on a title-named GPU mechanism plus LEO's characterisation — call-path attribution across the CPU/GPU boundary for DL workloads. Basis is title + census row + LEO's citation, not DeepContext's own text | `CORE_GPU` | Census screen reason is GPU profiling tooling (call-path attribution across CPU/GPU). LEO positions itself one abstraction level *below* it, which is independent evidence that it is a GPU profiler. → **watchlist** | — (watchlist) |
| GVARP: Detecting Performance Variance on Large-Scale Heterogeneous Systems | SC 2024 | `CLOSED_ACCESS` — DOI `10.1109/SC41406.2024.00063`; census records `UNKNOWN (not individually searched)`; `ieeexplore` 418 | TITLE + CENSUS_ROW (gpu_systems census screen reason: "Performance-variance detection on heterogeneous (GPU) nodes `[title-inference]`"), **plus a one-line prior-corpus row** in `hpc_systems_operations/.../02_PAPER_CENSUS.md`: "분산의 *국소화*. 애플리케이션 계측 기반, production 사례 없음" (localisation of variance; application-instrumentation-based; no production case), graded L5 · D1–D2 · P4 | **UNRESOLVED on current evidence** — "heterogeneous systems" is not GPU-specific on its face, and the prior corpus describes the method as application instrumentation. Whether the variance attribution reaches a GPU-specific mechanism cannot be decided from a title | `UNRESOLVED` | Deliberately **not** upgraded: the census itself marks GPU centrality `[title-inference]`. Its natural comparator is `GPU-IPDPS26-42`, which localises variance from system counters instead and finds GPUs *not* to be the cause. → **watchlist** | — (watchlist) |
| SNOOPIE: A Multi-GPU Communication Profiler and Visualizer | ICS 2024 (Session 9B Software Design for Accelerators) | `PENDING_FULLTEXT` — census records `NOT_SEARCHED` for both full text and artifact; DOI `UNKNOWN`. `CONFIRMED_IN_POPULATION` as entry 42 | TITLE + CENSUS_ROW | **NO**, on a title-named GPU mechanism — a *multi-GPU communication* profiler must instrument the GPU-to-GPU data path (NVLink/PCIe peer transfers, and plausibly NVSHMEM-style device-initiated traffic). Basis is title + census row | `CORE_GPU` | Title-explicit "Multi-GPU". Overlaps this cluster's profiling theme and the separate multi-GPU-communication cluster; **coordinate before deep-analysing to avoid duplicating that cluster's work.** → **watchlist** | — (watchlist) |
| Uncovering Real GPU NoC Characteristics: Implications on Interconnect Architecture | MICRO 2024 (Session 6B Networks-on-Chip) | `PUBLIC_FULLTEXT` (author PDF `people.ece.ubc.ca/aamodt/publications/papers/realgpu-noc.micro2024.pdf`). DOI `10.1109/MICRO61859.2024.00070`. **Full text not fetched in this pass** | TITLE + CENSUS_ROW (census screen reason: "Reverse-engineering of real NVIDIA GPU on-chip interconnect"), first author Zhixian Jin et al. | **NO** — reverse-engineering the on-chip interconnect of real NVIDIA GPUs is definitionally a GPU-microarchitecture contribution | `CORE_GPU` | Census-verified as reverse-engineering of real NVIDIA GPU NoC. Supplies the architecture-side measurement that `GPU-IPDPS26-42` treats as a black box. **Access is public** → **watchlist, priority** | — (watchlist) |

### 2.3 Simulation and performance modelling (taxonomy N)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| HyFiSS: A Hybrid Fidelity Stall-Aware Simulator for GPGPUs | MICRO 2024 (Session 2A Simulation) | `PUBLIC_ARTIFACT_ONLY` — paper `CLOSED_ACCESS` (DOI `10.1109/MICRO61859.2024.00022`; census records `NOT_FOUND_AFTER_SEARCH`, "no arXiv; IEEE/ACM paywalled"). Artifact public: `github.com/ConvolutedDog/HyFiSS` — **not cloned in this pass** | TITLE + CENSUS_ROW (census screen reason: "GPGPU performance simulator; **warp-level stall modelling is the entire contribution**"), first author Jianchao Yang et al. | **NO** — warp-level stall modelling in a GPGPU simulator is a SIMT-execution-model contribution by construction | `CORE_GPU` | Census states warp-level stall modelling is the whole contribution. Directly comparable to GCStack's stall taxonomy and to STEM+ROOT's sampling; **the artifact is public and unexamined** → **watchlist, priority** | — (watchlist) |
| GRASP: Fine-grained and Adaptive Sampled Simulation for GPU Performance Modeling | ICS 2026 (S05 Performance Modeling & Insight) | `PENDING_FULLTEXT` — census records `NOT_SEARCHED` for full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW. **Disambiguation resolved from the census**: ICS 2026 contains a *second, unrelated* paper also named GRASP — "GRASP: Optimizing VLIW Instruction Scheduling via Graph Reinforcement Learning" (S02), which the census explicitly records as **not GPU-related**. The paper assigned here is the **S05** one, first author R. Xue et al. | **NO**, on a title-named GPU mechanism — fine-grained adaptive sampled simulation for GPU performance modelling. Basis is title + census row | `CORE_GPU` | Title-explicit "GPU Performance Modeling". **The name collision the task warned about is confirmed and resolved in `census/ICS_2026.md` §3 and §5.** The closest competitor to STEM+ROOT (`GPU-MICRO25-01`). → **watchlist** | — (watchlist) |
| TrioSim: A Lightweight Simulator for Large-Scale DNN Workloads on Multi-GPU Systems | ISCA 2025 (Session 8A Performance and Modeling) | `PUBLIC_FULLTEXT` (author PDF `bu-icsg.github.io/publications/2025/TrioSim_ISCA_2025.pdf`) + public artifact `github.com/sarchlab/triosim`. DOI `10.1145/3695053.3731082`. **Neither fetched nor cloned in this pass** | TITLE + CENSUS_ROW (census screen reason: "Multi-GPU system simulator") | **NO**, on a title-named GPU mechanism — a simulator for DNN workloads on multi-GPU systems must model inter-GPU communication and per-GPU memory capacity. Basis is title + census row | `CORE_GPU` | Title-explicit "Multi-GPU Systems". **Both full text and artifact are public and unexamined** — the highest-readiness unread simulation item. → **watchlist, priority** | — (watchlist) |
| AMALI: An Analytical Model for Accurately Modeling LLM Inference on Modern GPUs | ISCA 2025 (Session 8A Performance and Modeling) | `CLOSED_ACCESS` — DOI `10.1145/3695053.3731064`; census records `NOT_FOUND_AFTER_SEARCH` for full text and artifact; `dl.acm.org` 403 | TITLE + CENSUS_ROW (census screen reason: "Analytical performance model of modern GPUs") | **NO**, on a title-named GPU mechanism — an analytical model of LLM inference *on modern GPUs* must parameterise GPU compute and memory-hierarchy structures. Basis is title + census row | `CORE_GPU` | Title-explicit "on Modern GPUs". `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). → **watchlist** | — (watchlist) |
| PIPEWEAVE: Synergizing Analytical and Learning Models for Unified GPU Performance Prediction | ISCA 2026 (7B Performance Modeling / Datacenter) | `PUBLIC_FULLTEXT` (arXiv 2601.14910; the census records the preprint as stating "Accepted to ISCA 2026"). DOI `UNKNOWN`. **Not fetched in this pass** | TITLE + CENSUS_ROW + full author list (Kaixuan Zhang, Yunfan Cui, Shuhao Zhang, Chutong Ding, Shiyou Qian, Luping Wang, Jian Cao, Guangtao Xue, Cheng Huang, Guodong Yang, Liping Zhang) | **NO**, on a title-named GPU mechanism — a hybrid analytical + ML model for unified *GPU* performance prediction. Basis is title + census row | `CORE_GPU` | Title-explicit "GPU Performance Prediction". **Access is public** → **watchlist, priority** | — (watchlist) |
| Forecasting GPU Performance for Deep Learning Training and Inference | ASPLOS 2025 (Session 5A / 30V1) | `CLOSED_ACCESS` — DOI `10.1145/3669940.3707265`; census records `NOT_SEARCHED` for full text and artifact; `dl.acm.org` 403 | TITLE + CENSUS_ROW (census screen reason: "GPU performance modelling / prediction across GPU generations `[title-only]`") | **NO**, on a title-named GPU mechanism — forecasting performance *across GPU generations* requires modelling generational GPU microarchitectural change. Basis is title + census row; the census itself marks this `[title-only]` | `CORE_GPU` | Title-explicit "GPU Performance". `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). → **watchlist** | — (watchlist) |

### 2.4 Reliability, resilience, fault tolerance (taxonomy O)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems | SC 2025 | `CLOSED_ACCESS` — DOI `10.1145/3712285.3759883`; census records `UNKNOWN (not individually searched)`; `dl.acm.org` 403 | TITLE + CENSUS_ROW + **a substantive prior-corpus analysis** in `hpc_systems_operations/.../raw/A_SC_main.md` entry **S25-1**: authors (Levitt, Barella, Zeltner, Musta, Cheney, Espinosa, Franza, Gerofi — Intel/Argonne), the problem (MTTR dominates availability as MTBF falls), the data (**Aurora production event history**), the mechanism (centralized meta-database + fine-grained multi-strike repair policies + automated recovery), the scale (**Aurora: 10,624 nodes, 63,744 Intel Max GPUs**), in-production deployment, the result (**MTTR reduced up to 84×** vs manual servicing), and the limits (policy engineering rather than learned inference; single site; manual baseline) | **NO**, on the prior corpus's evidence — repair policies over a fleet of 63,744 **Intel Max** GPUs, driven by GPU/node failure statistics. Note this is the cluster's only **Intel** GPU reliability datapoint | `CORE_GPU` | **`GPU_DELTA_ANALYSIS` would be required if analysed** — a substantive operations-angle analysis already exists (S25-1); only the GPU-specific delta (which Intel Max GPU failure modes, the GPU-level repair actions, Aurora's HBM/tile/Xe-link specifics) should be written. The closed-loop counterpart to `GPU-SC25-01`. → **watchlist** | — (watchlist) |
| Demystifying the Resilience of Large Language Model Inference: An End-to-End Perspective | SC 2025 | `CLOSED_ACCESS` — DOI `10.1145/3712285.3759803`; census records `UNKNOWN (not individually searched)`; `dl.acm.org` 403 | TITLE + CENSUS_ROW (census screen reason: "Fault/error behaviour of LLM inference on GPUs `[title-inference]`") | **UNRESOLVED on current evidence** — LLM inference resilience could be studied through GPU-specific fault injection (HBM ECC, SM register corruption) or purely at the model/serving level. The census marks GPU centrality `[title-inference]` and the title names no GPU mechanism | `UNRESOLVED` | Deliberately not upgraded. If GPU-specific, it is the software-visible consequence of exactly the uncorrected errors `GPU-ICS24-01` and `GPU-SC25-01` measure. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). → **watchlist** | — (watchlist) |
| DRUTO: Upper-Bounding Silent Data Corruption Vulnerability in GPU Applications | IPDPS 2024 (Session 5B Resilience) | `CLOSED_ACCESS` — census records `NOT_FOUND_AFTER_SEARCH` for full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW (census screen reason: "'GPU Applications' in title; GPU reliability / SDC vulnerability — GPU *mechanism* (reliability) contribution"), first author Md Hasanur Rahman et al. | **NO**, on a title-named GPU mechanism — upper-bounding SDC vulnerability in GPU applications requires GPU fault-injection into GPU state (registers, shared memory, HBM) and GPU-kernel-level error propagation analysis. Basis is title + census row | `CORE_GPU` | Title-explicit "in GPU Applications"; census classifies it as a GPU reliability-mechanism paper. A repository-wide grep produced a file-level hit in the operations corpus that **could not be confirmed at line level**, so treat prior coverage as `NO_EXISTING_ANALYSIS`. → **watchlist** | — (watchlist) |
| ATTNChecker: Highly-Optimized Fault Tolerant Attention for Large Language Model Training | PPoPP 2025 (S6 Large Language Models) | `PUBLIC_FULLTEXT` (arXiv 2410.11720). DOI `UNKNOWN`. **Not fetched in this pass** | TITLE + CENSUS_ROW. The census records an important caveat: the **official PPoPP detail page's abstract does not name a device**, and GPU centrality rests on the matching arXiv preprint; the census explicitly says "the GPU-specific mechanism should be confirmed from the full text at the verdict step" | **PROBABLY NO, but not confirmed** — ABFT for attention kernels is presumably implemented as GPU kernel-level checksums, but the title names no device and the required confirmation was not performed in this pass | `UNRESOLVED` | Honouring the census's own instruction: the GPU mechanism must be confirmed from full text, which was not read here. **Access is public** → **watchlist, priority**. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). | — (watchlist) |
| TurboFFT: Co-Designed High-Performance and Fault-Tolerant Fast Fourier Transform on GPUs | PPoPP 2025 (S2 GPU I) | `PUBLIC_FULLTEXT` (arXiv 2412.05824). DOI `UNKNOWN`. **Not fetched in this pass** | TITLE + CENSUS_ROW; `CONFIRMED_IN_POPULATION`. Census records that the **abstract names NVIDIA A100 and Tesla T4** | **NO** — title-explicit "on GPUs", with named NVIDIA hardware in the abstract and an ABFT scheme co-designed with the FFT kernel, i.e. fused into GPU kernel structure | `CORE_GPU` | Title-explicit and hardware-named. Sits at the boundary of this cluster (fault tolerance) and a kernel-optimization cluster; **coordinate before deep-analysing.** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). → **watchlist** | — (watchlist) |
| GPU Faults Across Cloud Providers | SC 2026 (seed) | **`UNRESOLVED` — existence not established** | Census verification only: `census/SC_2026.md` §5 records **`NOT_FOUND` — "no paper with this exact or near title located"** | Not answerable — no paper located | `UNRESOLVED` | **The task asked to verify existence; the census's independent STEP A/B search could not locate any paper with this or a near title.** Do not carry this forward as a real paper without a new primary source. → **watchlist (existence unverified)** | — (does not exist on current evidence) |
| SigmaTrace | SC 2026 (seed) | **`UNRESOLVED` — existence not established** | Census verification only: `census/SC_2026.md` §5 records **`NOT_FOUND` — "nothing located"** | Not answerable — no paper located | `UNRESOLVED` | Same as above: **existence unverified**, and not even a full title is available. → **watchlist (existence unverified)** | — (does not exist on current evidence) |

### 2.5 Production telemetry, monitoring and fleet operations (taxonomy O)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining | IPDPS 2024 (Session 3B Scheduling I) | `CLOSED_ACCESS` — DOI `10.1109/ipdps57955.2024.00037`, pp. 337–349 (recovered from the prior corpus); gpu_systems census records `NOT_SEARCHED (deprioritised)`; `ieeexplore` 418 | TITLE + CENSUS_ROW + **a substantive prior-corpus analysis** in `hpc_systems_operations/.../02_PAPER_CENSUS.md` entry **M-23**: authors (Baolin Li, Northeastern; Siddharth Samsi, Vijay Gadepally, MIT-LL; Devesh Tiwari, Northeastern), the operational problem (operators cannot act on black-box models; interpretable rules are needed), the system (GPU cluster, MIT SuperCloud-class), the data (production GPU monitoring time series), the method (association rule mining), the contribution ("operator consumability as an explicit optimisation target"), and the limit (**evaluation scale unverified**) | **YES, substantially** — association rule mining over monitoring time series is a general data-mining method, and the contribution the prior corpus identifies is *operator interpretability*, not a GPU mechanism. This is precisely the task's excluded pattern: "an anomaly-detection method applied to a machine that happens to have GPUs is not GPU research" | `RELATED_GPU` | **Deliberately downgraded.** Genuinely useful to this cluster as the methodological neighbour of `GPU-IPDPS26-41`, but the method does not depend on any GPU-specific property. If ever analysed, `GPU_DELTA_ANALYSIS` applies (M-23 already exists). → **watchlist** | — (watchlist) |
| CCL-D: A High-Precision Diagnostic System for Slow and Hang Anomalies in Large-Scale Model Training | PPoPP 2026 (Distributed Training; **Best Paper Nominee**) | `CLOSED_ACCESS` — census records `NOT_FOUND_AFTER_SEARCH` for full text and artifact; paper id `3786429`; official page `ppopp26.sigplan.org/details/PPoPP-2026-papers/19/x` | TITLE + CENSUS_ROW, first author Yida Gu et al. Census records that although the title has no GPU term, **the abstract names a 4,000-GPU cluster and "faulty GPU rank"** — census screen reason: "GPU collective-comm fault localization" | **NO**, on the census-recorded abstract — localising a *faulty GPU rank* in collective communication on a 4,000-GPU cluster is a GPU-collective (NCCL/RCCL-class) diagnosis problem. Basis is title + census row + census-quoted abstract fragments | `CORE_GPU` | The production-diagnosis counterpart to `GPU-IPDPS26-42`: where that paper cannot localise, CCL-D claims to. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` also applies (see §4). → **watchlist** | — (watchlist) |

### 2.6 Hardware characterisation and microbenchmarking (taxonomy N/O boundary)

| Paper | Venue/Year | Access state | Evidence read | Counterfactual answer | Verdict | Rationale (1-2 sentences) | Deep analysis file |
|---|---|---|---|---|---|---|---|
| Benchmarking and Dissecting the Nvidia Hopper GPU Architecture | IPDPS 2024 (Session 6A Accelerators) | `PENDING_FULLTEXT` — census records `NOT_SEARCHED` for full text and artifact; DOI `UNKNOWN` | TITLE + CENSUS_ROW; `CONFIRMED_IN_POPULATION` with a title correction (the official program spells the vendor "Nvidia"); authors Weile Luo, Ruibo Fan, Zeyu Li, Dayou Du, Qiang Wang, Xiaowen Chu | **NO** — microarchitectural characterisation of a named GPU architecture is definitionally a GPU contribution | `CORE_GPU` | Census screen reason: "microarchitectural characterisation — core GPU mechanism paper". → **watchlist** | — (watchlist) |
| Microbenchmarking NVIDIA's Blackwell Architecture: An in-depth Architectural Analysis | IPDPS 2026 | `PUBLIC_FULLTEXT` + `PUBLIC_ARTIFACT` (arXiv 2512.02189; artifact `github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark` and `zenodo.org/records/18716313`, artifact DOI `10.5281/zenodo.18716313`). **Neither fetched nor cloned in this pass** | TITLE + CENSUS_ROW. Authors Aaron Jarmusch, Sunita Chandrasekaran (Univ. of Delaware). Census screen reason: "Microbenchmark suite for the NVIDIA Blackwell **B200** vs **H200**: memory subsystem, Tensor Core pipelines, FP precisions, energy efficiency." Census also records a subtitle discrepancy (the author slide deck says "Architecture Analysis", arXiv and Zenodo say "Architectural") and that the title match was made on abstract content plus the author's slide deck and Zenodo record because arXiv's markdown conversion strips the title block | **NO** — microbenchmarking the memory subsystem and Tensor Core pipelines of a named GPU architecture | `CORE_GPU` | Directly extends `GPU-SC25-01`'s HBM argument into the Blackwell generation (B200 vs H200). **Both full text and artifact are public and unexamined; the artifact has its own DOI** → **watchlist, priority**. **AMENDED 2026-09-18 by central reconciliation: this watchlist row is discharged** — the core-execution cluster read the full paper and cloned the artifact, and the analysis now exists. | `GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md` |
| Characterizing Performance, Power, and Energy of AMD CDNA3 GPU Family | SC 2025 | `PENDING_FULLTEXT` — DOI `10.1145/3712285.3759768`, pp. 905–934; census records no arXiv and flags the publisher PDF as `ACM_OA?` (`dl.acm.org/doi/epdf/…`, 403 here) | TITLE + CENSUS_ROW; `CONFIRMED_IN_POPULATION`, first author Bagus Hanindhito. Census screen reason: "Direct microarchitectural/power characterization of AMD MI300X/MI325X (CDNA3, Matrix Cores, HBM)". A **one-line prior-corpus row** also exists in `hpc_systems_operations/.../raw/A_SC_main.md` grading it L1–L3 · D2 · P2 · SC-REGULAR-RELEVANT — shallow, no analysis | **NO** — direct microarchitectural and power characterisation of named AMD GPUs (MI300X/MI325X), covering Matrix Cores and HBM | `CORE_GPU` | The AMD counterpart to the Hopper/Blackwell characterisation papers, and the power/energy axis that connects to `GPU-ICS24-01`'s power-swing finding. If analysed, `GPU_DELTA_ANALYSIS` applies against the one-line ops row. → **watchlist** | — (watchlist) |
| Debunking the CUDA Myth Towards GPU-based AI Systems | ISCA 2025 (Session 9B HPC) | `PUBLIC_FULLTEXT` (arXiv 2501.00210). DOI `10.1145/3695053.3731050`. **Not fetched in this pass** | TITLE + CENSUS_ROW (census screen reason: "GPU/CUDA programmability and performance study (vs. Intel Gaudi NPU)") | **NO** — the paper's whole structure is a comparison of the CUDA/GPU stack against a non-GPU accelerator (Intel Gaudi), so GPU-specific programmability and performance properties are the object of study | `CORE_GPU` | One of very few papers in the corpus that treats "GPU vs a different accelerator" as the research question, which makes it unusually useful as a counterfactual reference point for this whole cluster. **Access is public** → **watchlist, priority** | — (watchlist) |

---

## 3. Stable IDs issued by this cluster

| Stable ID | Paper | File |
|---|---|---|
| `GPU-SC24-41` | HiRace (SC 2024) | `GPU-SC24-41--hirace-gpu-data-race-checking.md` |
| `GPU-SC25-01` | Story of Two GPUs (SC 2025) | `GPU-SC25-01--story-of-two-gpus-h100-a100-resilience.md` |
| `GPU-SC26-41` | LEO (venue unresolved) | `GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md` |
| `GPU-ICS24-01` | Summit GPU memory corruption (ICS 2024) | `GPU-ICS24-01--summit-gpu-memory-corruption.md` |
| `GPU-IPDPS26-41` | Production GPU workloads via system telemetry (IPDPS 2026) | `GPU-IPDPS26-41--production-gpu-workloads-system-telemetry.md` |
| `GPU-IPDPS26-42` | Elusive application performance (IPDPS 2026) | `GPU-IPDPS26-42--elusive-application-performance-production-gpu.md` |
| `GPU-MICRO24-41` | Over-Synchronization / ScopeAdvice (MICRO 2024) | `GPU-MICRO24-41--over-synchronization-in-gpu-programs.md` |
| `GPU-MICRO25-01` | STEM+ROOT (MICRO 2025) | `GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md` |
| `GPU-HPCA24-41` | GPU Scale-Model Simulation (HPCA 2024) | `GPU-HPCA24-41--gpu-scale-model-simulation.md` |

**Numbering and collisions.** Numbering began at `-01` per venue-year for this
cluster, as instructed. Six IDs then collided with files written concurrently
into `domains/gpu_systems/corpus/` by other clusters
(`GPU-SC24-01`, `GPU-HPCA24-01`, `GPU-IPDPS26-01`, `GPU-IPDPS26-02`,
`GPU-SC26-01`, `GPU-MICRO24-01`). Per `governance/ID_NAMING_RULES.md` an ID is
never reused for a different source, so **this cluster's six were renumbered
into a `-41`/`-42` band** and every cross-reference inside this cluster's nine
files was updated. A band distinct from the multi-GPU-communication cluster's
`-21`/`-22` band was chosen so the two do not collide in future.
`GPU-SC25-01`, `GPU-MICRO25-01` and `GPU-ICS24-01` were uncontested;
`domains/gpu_systems/corpus/_LEDGER_memory_virtualization.md` independently
records that it **ceded `GPU-ICS24-01`** to this cluster and renumbered its own
ICS 2024 file to `GPU-ICS24-02`.

**One duplicate remains in the directory and is NOT this cluster's:**
`GPU-ISC26-01` was held by two files from two other clusters; reconciled centrally on 2026-09-18 — PICO (first writer) keeps `GPU-ISC26-01`, the ISC 2026 FP64-Tensor-Core paper was reissued as `GPU-ISC26-02`
(`…--pico-performance-insights-collective-operations.md` and
`…--fp64-tensor-cores-high-order-finite-element.md`). Both of those ledgers
already flag it for central reconciliation. Left untouched here.

---

## 4. Prior-corpus deduplication summary (task §4)

**`GPU_DELTA_ANALYSIS` — written as a GPU-specific delta against existing
operations-angle analyses (4 papers, all deep-analysed):**

| Paper | Where the pre-existing analysis is | What it already held |
|---|---|---|
| Story of Two GPUs | `hpc_systems_operations/corpus/aiops-survey/raw/A_SC_main.md` **S25-2**; `synthesis/02_PAPER_CENSUS.md` **M-05**; `synthesis/03_SC_REGULAR_PRECEDENTS.md` **§P4**; `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` | Authors, DOI, framing question, the data asset (1,056 GPUs / 2.5 y / 11.7 M GPU-hours), method (taxonomy + MTBE + availability projection), headline results (3.2× worse H100 memory MTBE; ~5% overprovisioning), limits, and the SC20-Titan → SC25 lineage |
| Characterizing Production GPU Workloads using System-wide Telemetry Data | `synthesis/02_PAPER_CENSUS.md` **M-24**; `raw/B_hpdc_ipdps_cluster_isc_acsos.md`; `synthesis/03_SC_REGULAR_PRECEDENTS.md` | Authors, venue/DOI/pages, the operational question, "large-scale empirical characterization", an L2·D2·P2–P3 grading, the judgement that it is descriptive with no predictive/diagnostic model, and its strategic role. **System identity was `[system identity A — confirm]` and scale/duration `[UNVERIFIED]` — both now closed** (Perlmutter; 1 Mar–1 Apr 2025; 75,703 jobs; 10 s sampling) |
| The Case of the Elusive Application Performance on Production GPU Supercomputers | `synthesis/02_PAPER_CENSUS.md` **M-25**; `raw/B`, `raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`; `synthesis/03_SC_REGULAR_PRECEDENTS.md` | Authors, venue/DOI/pages, systems and scale (761 runs / 8,118 node-hours / 4 months / ~10 TB per system), method (repeated runs + NIC counters + XGBoost), results (Frontier 2.6× / Perlmutter 1.4×; cause attributed to network congestion and top users, not compute), the authors' own Rosetta-counter blocker, and the reading that "GPU degradation as the main cause has already been measured and falsified" |
| Understanding GPU Memory Corruption at Extreme Scale | `synthesis/02_PAPER_CENSUS.md` (one table row); `raw/D_workshops.md`; `raw/H_centers.md`; `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` | **Shallow** — a one-line row: "27,648 V100. DBEs recur on the same GPU and correlate with sustained power, not temperature", the DOI, and the OLCF lineage. Also carried an author-order discrepancy flag. **Both prior records name the wrong final author** (Wang, not Engelmann) — corrected in the delta file |

**`GPU_DELTA_ANALYSIS` would be required if these verdict-only papers are ever
analysed:** *Fine-grained Automated Failure Management* (substantive analysis
at `raw/A_SC_main.md` **S25-1**); *Interpretable Analysis of Production GPU
Clusters* (substantive analysis at `02_PAPER_CENSUS.md` **M-23**);
*Characterizing Performance, Power, and Energy of AMD CDNA3* and *GVARP*
(one-line operations-census rows only).

**`NO_EXISTING_ANALYSIS`** — HiRace, LEO, STEM+ROOT, GPU Scale-Model
Simulation, Over-Synchronization/ScopeAdvice, and the remaining verdict-only
papers. Repository-wide greps (exact title, normalized title, DOI, arXiv ID,
first author + distinctive term) returned only `domains/gpu_systems/census/*`
rows and, for some, raw TOC dumps in
`domains/hpc_quantum/corpus/quantum-hpc-survey/working-evidence/` — which per
task §4 are **existence evidence only, never an existing analysis**.

**`KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`** — `domains/ai_hpc_systems/` is
`EXTERNAL_IMPORT_PENDING`; its `DOMAIN_CONTEXT.md` states that a ~80-paper
AI/HPC corpus exists in an external workspace, has not been imported, and that
**nothing about its content may be asserted** — including venues, counts or
coverage. Its declared scope explicitly includes "performance analysis" and
"GPU communication and collectives". The following assigned papers are
plausibly within that external corpus, and **no claim either way about
duplication is made for them**:

- *Demystifying the Resilience of Large Language Model Inference* (SC 2025)
- *AMALI: An Analytical Model for Accurately Modeling LLM Inference on Modern GPUs* (ISCA 2025)
- *Forecasting GPU Performance for Deep Learning Training and Inference* (ASPLOS 2025)
- *PIPEWEAVE* (ISCA 2026)
- *TrioSim* (ISCA 2025)
- *DeepContext* (ASPLOS 2026)
- *CCL-D* (PPoPP 2026)
- *ATTNChecker* (PPoPP 2025)
- *TurboFFT* (PPoPP 2025)

---

## 5. Cross-paper findings verified from the papers' own citations

Each item below is grounded in a citation or a quoted claim actually read, not
in topical adjacency.

1. **GPA (GPU Performance Advisor) is the hub of the GPU performance-advisory
   literature — verified from two independent citing papers.** LEO names GPA as
   the work that "pioneered backward slicing for GPUs, but GPA supports only
   NVIDIA GPUs and cannot trace memory access dependencies through
   synchronization instructions such as AMD's `s_waitcnt`" `[paper, LEO]`, and
   ScopeAdvice independently lists GPA among the instruction-level profiling
   tools it complements `[paper, ScopeAdvice]`. A 2024 synchronization-scope
   tool and a 2026 cross-vendor stall slicer converge on the same ancestor.

2. **A verified non-citation: HiRace (SC 2024) and ScopeAdvice (MICRO 2024) are
   exact duals that do not cite each other.** ScopeAdvice's related work names
   iGUARD (overhead 27–649×), BARRACUDA (~3700×), ScoRD and
   compute-sanitizer racecheck as the race-detection art and states the goals
   are orthogonal — under- versus over-synchronization `[paper, ScopeAdvice]`.
   **HiRace is absent from that list**, and HiRace's related work does not
   mention over-synchronization `[paper, HiRace]`. The two papers analyse the
   same programs over the same CUDA scope lattice and cite the same baselines.
   Their independent characterisations of iGUARD are mutually consistent
   (27–649× vs ">30× average with outliers to ~1000×"), which strengthens both.

3. **Where production reliability research meets architecture research: the
   HBM repair budget.** This is the cluster's clearest verified bridge, and it
   runs through a single mechanism across three GPU generations.
   `GPU-ICS24-01` establishes that Volta/HBM2 repairs by **page retirement
   with a 64-page table**, and that exhausting it produces page-retirement
   failures `[paper]`. `GPU-SC25-01` establishes that Ampere and Hopper repair
   by **row remapping capped at 512 rows on both**, and that H100's 2.4×
   larger HBM3 against an unchanged 512-row budget is *the* reason its memory
   resilience regressed (3.2× lower per-GPU MTBE; only 24% lower per-GB)
   `[paper, v4]`. Both papers work in the same XID vocabulary (48/63/64). The
   architecture-side consequence is a concrete, falsifiable prediction: unless
   the spare-row budget scales with capacity, the regression worsens on
   larger-HBM parts — which is exactly what *Microbenchmarking NVIDIA's
   Blackwell Architecture* (B200 vs H200) is positioned to test, and why it is
   flagged priority in §2.6. Note also that the two papers **disagree on the
   binding constraint**: Summit locates it in per-device predisposition plus
   short-term power swings (≈33 W, p = 0.00056 Šidák-corrected) with
   temperature level insignificant (≈1.5 °C), overturning the Titan-era
   cooling-geometry account; Delta locates it in the repair budget.

4. **Production performance research has already falsified the GPU-degradation
   story, which constrains what reliability telemetry may claim.**
   `GPU-IPDPS26-42` builds a per-GPU FP16 GEMM instrument, measures real device
   heterogeneity (up to 28% system-wide on Perlmutter's A100s; 12% per-GCD on
   Frontier's MI250X), and then shows it does **not** reach application
   runtime — Spearman 0.07 and 0.08 against the count of slowest-1% GPUs in an
   allocation, unchanged at the 10% and 30% thresholds `[paper]`. The variance
   instead sits in GPU-resident collectives (NCCL/RCCL `Allreduce` up to 24×
   slower on Frontier) and in NIC/PCIe counters. **Any claim that GPU health
   telemetry predicts application slowdown must now clear this bar.** The prior
   operations corpus reached the same conclusion from a different angle and
   recorded it as a strategic warning `[hpc_systems_operations, M-25]`.

5. **Two independent tool-design bets on ISA-level versus source-level
   instrumentation, each quantified — and they disagree.** ScopeAdvice
   instruments SASS through **NVBit** and measures that **NVBit alone
   contributes ~64% of a 29–522× slowdown** `[paper]`. HiRace deliberately
   rejects NVBit for **Clang source rewriting**, citing NVBit's deprecation and
   its incompatibility "with NVIDIA architectures released since
   [iGUARD's] publication", and achieves ~3× average and 7.5× broad-evaluation
   slowdown `[paper]`. LEO takes the ISA route further still — per-vendor
   decoders for `s_waitcnt`, NVIDIA B1–B6 barrier bits and Intel SBID tokens,
   plus `nvdisasm`/`llvm-objdump`/GED `[paper]` — buying cross-vendor reach at
   the cost of permanent per-architecture maintenance. The 64% figure is direct
   quantitative support for HiRace's choice, and neither paper cites the other.

6. **The simulation-cost literature partitions cleanly, and the two halves have
   never been composed.** `GPU-MICRO25-01` and `GPU-HPCA24-41` both name
   **Principal Kernel Analysis, TBPoint and Photon** as the prior sampling art
   `[paper, both]` — a verified shared literature. But they reduce different
   costs: STEM+ROOT reduces *how many kernel invocations* are simulated
   (3× to 31,719× depending on kernel-call multiplicity), while Scale-Model
   Simulation reduces *how large a machine* is simulated (9.3×, and it is the
   only method that works when no model of the target exists at all). Neither
   paper mentions composing them, and nothing in either design forbids it.
   A second caution worth carrying: **STEM+ROOT's headline is bounded error,
   not speed** — Photon is 1.54× faster on the CASIO suite at 9.85% error
   against STEM's 0.36% `[paper]`, so the 31,719× figure is meaningless
   without its error column.

7. **Two independent warnings that GPU telemetry counters are not stable across
   software changes.** `GPU-ICS24-01` reports that a **RHEL 8 update on
   18 August 2021 correlates with a 170-fold increase in page-retirement-failure
   counts** from 1 September 2021 `[paper]`. `GPU-SC25-01`'s authors refuse to
   attribute H100's **zero observed NVLink errors** to hardware improvement
   because they cannot rule out "potential changes in NVLink error logging
   mechanisms" `[paper, v4]`. And `GPU-IPDPS26-42` documents a libfabric
   1.20.1 regression whose 14 January 2025 fix measurably reduced measured
   variability `[paper]`. Three separate papers in this cluster independently
   establish that a software-stack change can move a hardware counter by
   orders of magnitude — a standing methodological hazard for any longitudinal
   GPU-fleet study.

---

## 6. Watchlist (papers that must not be deep-analysed on current evidence)

**Blocked by access path, but public full text or artifact exists — highest
value to revisit first:**

| Paper | What exists | Why it matters |
|---|---|---|
| Towards Unified Analysis of GPU Consistency (ASPLOS 2024/29V4) | author PDF, two mirrors | the formal PTX/Vulkan scoped-consistency foundation that HiRace and ScopeAdvice both rely on |
| TrioSim (ISCA 2025) | author PDF **and** public artifact | multi-GPU DNN simulator; nothing in this cluster covers multi-GPU simulation |
| Uncovering Real GPU NoC Characteristics (MICRO 2024) | author PDF | the architecture-side interconnect measurement that `GPU-IPDPS26-42` treats as a black box |
| Microbenchmarking NVIDIA's Blackwell Architecture (IPDPS 2026) | arXiv + artifact with its own DOI | tests finding §5.3's prediction on B200 vs H200 |
| HyFiSS (MICRO 2024) | public artifact (paper paywalled) | census says warp-level stall modelling is the *entire* contribution; directly comparable to GCStack |
| PIPEWEAVE (ISCA 2026) | arXiv 2601.14910 | hybrid analytical + learned GPU performance prediction |
| Debunking the CUDA Myth (ISCA 2025) | arXiv 2501.00210 | the only paper here whose research question is "GPU versus a different accelerator" |
| ATTNChecker (PPoPP 2025) | arXiv 2410.11720 | the census itself instructs that GPU centrality be confirmed from full text at the verdict step |

**Artifact read but paper unavailable — verdict safe, deep analysis forbidden
(task §2):**
- **GCStack+GCScaler** (ISCA 2025) — `PUBLIC_ARTIFACT_ONLY`; publisher 403.
  Full stall taxonomy recovered from source, listed in §1.
- **pkdb / Interactive Debugger for Performance Portable Python HPC Kernels**
  (SC 2026) — `PENDING_FULLTEXT`; arXiv `2609.07912` returned HTTP 429 on eight
  attempts across four URL forms. Mechanism recovered from source, listed in §1.
  **Retry from a different network path.**

**Existence unverified — do not carry forward as real papers:**
- **GPU Faults Across Cloud Providers** (SC 2026 seed) — census: `NOT_FOUND`.
- **SigmaTrace** (SC 2026 seed) — census: `NOT_FOUND`, not even a full title.

**Verdict genuinely unresolved on current evidence (4):** *GVARP* (SC 2024),
*Demystifying the Resilience of LLM Inference* (SC 2025), *ATTNChecker*
(PPoPP 2025), plus the two non-existent seeds above.

**Venue unverified:** *LEO* — analysed as `GPU-SC26-41` on public full text,
but the census records `NOT_FOUND` in every official SC26 source and the arXiv
record carries no venue comment. **Treated as a preprint; the SC 2026
attribution in the task assignment is uncorroborated.** *pkdb*'s SC 2026
attribution rests on `[README]` evidence ("Artifact for SC'26") only.

# GPU runtime, task graphs, scheduling, and GPU sharing / MIG / MPS / virtualisation / co-location — GPU relevance verdict ledger

cluster: taxonomy **J** (GPU runtime, task graphs, scheduling) and **K** (GPU sharing, MIG, MPS, virtualisation, co-location)
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

Verdicts are `CORE_GPU` / `RELATED_GPU` / `EXCLUDE` / `UNRESOLVED`.
Access states are `PUBLIC_FULLTEXT` / `CLOSED_ACCESS` / `PENDING_FULLTEXT` /
`PUBLIC_ARTIFACT_ONLY` / `ABSTRACT_ONLY`.
`evidence_read` records what was actually read — a verdict reached from an
abstract says `ABSTRACT_ONLY` and may **not** be used to justify a deep analysis.

## The strict counterfactual, as applied in this cluster

This is the cluster most prone to false positives, because scheduling *GPU jobs*
is usually not *GPU research*. The rule applied here, without exception:

- A queueing, bin-packing, forecasting or fairness policy over resources that
  happen to be accelerators → **`RELATED_GPU`**.
- A mechanism that manipulates **SM / TPC / CTA / MIG / MPS / channel / driver**
  structure, or that depends on a GPU-specific property (non-preemptive kernels,
  the kernel-launch boundary, wave quantization, a fixed partition lattice, a
  closed driver interface) → **`CORE_GPU`**.

Every row records the **isolation mechanism**, which is this cluster's spine.

## How access states were determined in this pass

- **Reachable:** `arxiv.org/abs/` and `arxiv.org/html/<id>v1`; author- and
  group-hosted PDFs (`cis.temple.edu`, `people.cs.vt.edu`, `xianweiz.github.io`);
  ICS 2025 proceedings PDFs at `hpcrl.github.io/ICS2025-webpage/`;
  `research.ibm.com/publications/...`; GitHub over Bash.
- **Not reachable (not retried):** `dl.acm.org` → 403; `ieeexplore.ieee.org` → 418;
  `dblp.org` → robots; `par.nsf.gov` → robots-disallowed; `arxiv.org/search`,
  `export.arxiv.org`, `web.archive.org` → unavailable.
- **arXiv rate limiting materially affected this pass.** `arxiv.org/html/2606.29775v1`
  and `arxiv.org/pdf/2606.29775` returned HTTP 429 on five separate attempts spread
  across the session, while `arxiv.org/abs/2606.29775` succeeded. SMART-MIG is
  therefore `PUBLIC_FULLTEXT` **by access state** but `ABSTRACT_ONLY` **by evidence
  read** — and under the full-paper gate it gets a verdict and a watchlist entry,
  not a deep analysis. The same 429 wall blocked a planned deep analysis of Dilu
  (`arxiv.org/html/2503.05130v1`).

## Prior-corpus deduplication summary

Whole-repo grep (`*.md`, `*.txt`, `*.tsv`, excluding `.git`) was run for every
assigned title. Findings:

- **No paper in this cluster has an existing deep analysis** in
  `domains/gpu_systems/corpus/`. All hits were (a) this project's own STEP A/B
  rows in `domains/gpu_systems/census/`, (b) raw TOC dumps in
  `domains/hpc_quantum/.../working-evidence/`, or (c) unrelated string collisions
  (e.g. "AGIO" inside "AGILE"; "LEGO" inside "LEGOSim"; "Dilu" inside a word).
- **`domains/hpc_systems_operations/` is imported and was checked directly.**
  `topics/gpu_operations.md` (34 lines) and `topics/scheduling_resource_management.md`
  (34 lines) were read in full and grepped for `MIG`, `MPS`, `GPU sharing`,
  `co-locat`, `spatial` — **zero hits**. That corpus's GPU coverage is DCGM-based
  health/utilisation monitoring and Slurm-family cluster scheduling; it contains
  no GPU-partitioning or co-location content. **No `GPU_DELTA_ANALYSIS` is owed by
  any paper in this cluster.**
- **`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`** (~80-paper AI/HPC
  corpus, not imported, explicitly covering serving and runtime). Every
  LLM-serving / DL-serving / serverless row below is flagged
  `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. **No claim is made about what that corpus
  does or does not contain.**
- Two rows are owned by other clusters and are adjudicated here only as data
  points: **CUDASTF** (compiler cluster owns the row) and **Fine-grained Automated
  Failure Management** (profiling cluster owns the row). **DEFT** overlaps the
  power cluster, which owns that row.

---

## Priority papers

| Paper | Venue/Year | Access state | Evidence read | Isolation mechanism | Counterfactual answer | Verdict | Rationale | Deep analysis file |
|---|---|---|---|---|---|---|---|---|
| **ParvaGPU: Efficient Spatial GPU Sharing for Large-Scale DNN Inference in Cloud Environments** | SC 2024, DOI `10.1109/SC41406.2024.00048` | `PUBLIC_FULLTEXT` — arXiv 2409.14447 + GitHub artifact | Full text (3 passes over `/html/2409.14447v1`) **+ artifact read at commit `5f3de1e1`** | **MIG between workloads + MPS within one workload's instance**; no `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` anywhere in the artifact | **NO** — the optimisation variables are MIG's legal GPC counts (1/2/3/4/7, with 5 and 6 physically unavailable), MIG's placement-slot lattice, and MPS client count | `CORE_GPU` | Internal slack and external fragmentation are both *defined by* the MIG lattice; `find_fit_gpu()` rejects a GPU because slot 4 holds a size-3 instance — not generic bin packing | `GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md` |
| **A Device-Side Execution Model for Multi-GPU Task Graphs** (system name **Mustard**) | ICS 2025, DOI `10.1145/3721145.3730426` | `PUBLIC_FULLTEXT` — `hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-66.pdf` | Full text pass: motivation, background, design, implementation, limitations. **Evaluation section NOT returned → no performance number asserted** | **None** (not a sharing system). Scheduling quantum = subgraph, claimed via NVSHMEM device atomics; only guard is voluntary occupancy accounting | **NO** — device-side `cudaGraphLaunch` from a persistent kernel, NVSHMEM multi-GPU atomics, and the **120-graphs-per-device** device-side-launch cap | `CORE_GPU` | The contribution *is* removing the host from the kernel-launch boundary; StarPU is cited as "up to 13x slower compared to CUDA Graphs". A CPU work-stealing task runtime is a solved problem | `GPU-ICS25-162--mustard-device-side-execution-multi-gpu-task-graphs.md` |
| **gShare: Efficient GPU Sharing with Aggressive Scheduling in Multi-tenant FaaS platform** | ASPLOS 2026, DOI `10.1145/3779212.3790168` | `PUBLIC_FULLTEXT` — co-author-hosted ACM PDF at `cis.temple.edu` | Full text pass: motivation, design, driver interaction, evaluation, limitations. Algorithm boxes not returned | **Driver shim** — `vfio-mdev` mediated vGPU, 57 intercepted ioctls (17 `NV_ESC` + 40 UVM) in 60 kLOC of C; **time slicing** at GPU-*channel* granularity, 20 ms round robin | **NO** — interception of the closed NVIDIA driver ioctl surface, one active hardware channel per period, and the non-preemptive kernel model (kernels >20 ms "cause significant performance degradation") | `CORE_GPU` | The mechanism *is* the GPU driver interface; its own stated weakness (SM under-fill within a slice) is a GPU-specific failure mode | `GPU-ASPLOS26-163--gshare-vfio-mdev-vgpu-time-slicing-faas.md` |
| **SGDRC: Software-Defined Dynamic Resource Control for Concurrent DNN Inference on NVIDIA GPUs** | PPoPP 2025, DOI `10.1145/3710848.3710863` | `PUBLIC_FULLTEXT` — `people.cs.vt.edu/~huaicheng/p/ppopp25-sgdrc.pdf` | Full text pass over the PPoPP PDF + a pass over arXiv 2407.13996v1, which renders as the **same work under the name "Missile"** (larger version, adds a PCIe fair scheduler and two more GPUs) | **Software SM partitioning at TPC granularity** (TMD masks via `libsmctrl`) + **persistent-thread kernels** + cooperative **eviction flag polled with `ld.cv`** + **VRAM-channel page colouring** through a modified `nvidia-uvm`. Explicitly *not* MIG, *not* MPS | **NO** — TMD/`libsmctrl` is an undocumented NVIDIA interface; the eviction flag exists only because GPU kernels are non-preemptive; the channel colouring rests on a reverse-engineered non-linear per-SKU VRAM hash | `CORE_GPU` | The strongest NO in the cluster: all three mechanisms are NVIDIA-hardware or NVIDIA-driver objects. On a CPU, page colouring and core affinity are documented primitives | `GPU-PPoPP25-164--sgdrc-software-defined-dynamic-resource-control.md` |
| **Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading** | ISC 2026 (**`MEMBERSHIP_UNVERIFIED`** per `census/ISC_2026.md`) — arXiv 2604.08451 | `PUBLIC_FULLTEXT` — `/html/2604.08451v1` | Full text pass: abstract, motivation, MIG background, **Table II profile table**, Table III applications, offloading proposal, methodology. **Results/ablation/related-work NOT returned** | **MIG** (characterised), compared against **MPS**, **time slicing** and full-GPU; plus a proposed **NVLink-C2C coherent CPU memory offload** as a slice-size escape hatch | **NO** — the object of study is MIG's H100 lattice (`1g.12gb`…`7g.96gb`, 16/32/60/64/132 SMs), its offline-only reconfiguration, and the finding that **interference survives MIG through power throttling** | `CORE_GPU` | Characterisation, but of GPU hardware partitioning itself. The power-throttling finding falsifies an assumption every MIG scheduler in this cluster makes | `GPU-ISC26-165--taming-gpu-underutilization-mig-static-partitioning-cpu-offloading.md` |
| **Bullet: Boosting GPU Utilization for LLM Serving via Dynamic Spatial-Temporal Orchestration** *(added from the verdict-only list — public full text + artifact both reachable)* | ASPLOS 2026, DOI `10.1145/3779212.3790135` | `PUBLIC_FULLTEXT` — `xianweiz.github.io/doc/papers/26asplos_bullet.pdf`; preprint arXiv 2504.19516 (v1 under a different title) | Full text pass: motivation, §3.2–§3.4 design, runtime interaction, evaluation setup, limitations. **Ablation/result tables NOT returned** → no speedup asserted. **Artifact read at commit `445afae2`** | **Software SM partitioning at TPC granularity via per-stream TPC masks** (`libsmctrl_set_stream_mask`/`_ext`), disjoint contiguous ranges growing from opposite ends of the device, CUDA stream priority as a secondary lever, **no memory-system isolation** (KV cache shared via `cudaIpc*`) | **NO** — the partitioning primitive "co-opts preexisting debug logic in the CUDA driver library" (libsmctrl header, CUDA ≤ 12.6), and the problem solved is **wave quantization**, a SIMT-hardware phenomenon | `CORE_GPU` | Same primitive as SGDRC, opposite assumption about memory contention. Also the finest software partition quantum in the cluster: 1 TPC = 2 SMs, changed per prefill layer / decode step | `GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md` |
| **SMART-MIG: A Learning Framework for Scalable and Energy-Efficient GPU Scheduling** | IPDPS 2026 — arXiv 2606.29775; IBM Research publication page | `PUBLIC_FULLTEXT` (a full text exists and is open) **but evidence read is `ABSTRACT_ONLY`** — `/html/` and `/pdf/` returned HTTP 429 on five attempts; `/abs/` and the IBM page succeeded | `ABSTRACT_ONLY` + bibliographic metadata (authors Wenqing Yu, Neel Karia, Tanvi Hisaria, Clifford Stein, Olivier Tardieu, Asser Tantawi; IBM Research; "14 pages, 13 figures, accepted at 40th IEEE IPDPS") | **MIG** — the learned action is **MIG repartitioning**; job scheduling onto "the slices of the heterogeneous partitions" is by tailored heuristics | **NO (provisional, abstract-level)** — the action space *is* MIG partitioning, an NVIDIA hardware feature; the energy claim rests on running "smaller machine learning models on partitions of a GPU rather than the entire device" | `CORE_GPU` | MIG repartitioning is a GPU hardware mechanism, so the row clears the strict test even at abstract level. **But the MF-MARL layer on top is generic scheduling**, and whether the paper models MIG's real constraints (legal profiles, placement slots, offline-only reconfiguration, power coupling) is exactly what could not be read. **WATCHLIST — highest priority re-read in this cluster.** | — (gate not met) |
| **GFS: A Preemption-aware Scheduling Framework for GPU Clusters with Predictive Spot Instance Management** | ASPLOS 2026, DOI `10.1145/3760250.3762231` — arXiv 2509.11134 | `PUBLIC_FULLTEXT` — `/abs/2509.11134` read | `ABSTRACT_ONLY` (full abstract, authors, acceptance note) | **None at the device level** — the unit of preemption is a *job/spot instance*, not a kernel, an SM range or a MIG slice | **YES** — a forecasting model for tenant demand, a dynamic spot quota, and a preemptive priority policy would be substantially the same over CPU nodes, TPUs or any other quota-managed resource | `RELATED_GPU` | **The clearest false-positive candidate in the cluster, and the reason the strict test exists.** Nothing in the abstract depends on SM occupancy, MIG profiles, MPS, kernel non-preemptibility or the driver interface. The reported numbers (33.0% fewer evictions, 44.1% lower queuing delay, up to 22.8% better GPU allocation rate, ~$459,715/month on a >10,000-GPU production cluster) are cluster-economics results, not GPU-mechanism results. Re-read could upgrade it **only** if the preemption mechanism turns out to manipulate device state | — (verdict-only) |
| **µShare: Non-Intrusive Kernel Co-Locating on NVIDIA GPUs** | HPCA 2026 (first author Wenhao Huang, per proceedings TOC) | `CLOSED_ACCESS` (effectively) — no preprint, author PDF or open record located; `ieeexplore` 418, `dl.acm.org` 403. DOI `UNKNOWN` | `TITLE_AND_CENSUS_ROW` only | **`UNKNOWN`** — the title's "Non-Intrusive" and "Kernel Co-Locating" imply co-location *without* kernel-source modification, which would place it opposite SGDRC and Bullet (both of which rewrite or re-target kernels) and alongside gShare's interception school. **This is inference from the title and is not evidence.** | **NO (title-level, provisional)** — "Kernel Co-Locating on NVIDIA GPUs" is title-explicit about the device and about the kernel as the unit | `CORE_GPU` (provisional) | **WATCHLIST — the highest-value missing paper in this cluster.** If "non-intrusive" means transparent co-location of *unmodified, closed-source* kernels, it resolves the one limitation that both software-partitioning papers here concede (SGDRC: "closed-source vendor libraries … are not currently compatible"). Must be re-hunted from a network with IEEE access | — (gate not met) |
| **Asynchrony and GPUs: Bridging this Dichotomy for I/O with AGIO** | ASPLOS 2026, DOI `10.1145/3779212.3790130`, session 2C | `CLOSED_ACCESS` (effectively) — no preprint or author PDF located; one candidate lead (an EPFL Infoscience record) was fetched and proved to be **GPUfs (ASPLOS '13)**, not AGIO. Authors `UNKNOWN` | `TITLE_AND_CENSUS_ROW` only; **no abstract obtained** | **`UNKNOWN`** — not a sharing paper; the subject is GPU I/O asynchrony | **`UNRESOLVED`** — the title names GPUs and an execution-model dichotomy (asynchronous I/O vs the synchronous SIMT execution model), which *suggests* a GPU-specific contribution, but nothing was read | `UNRESOLVED` | **WATCHLIST.** Belongs more to a GPU-storage/IO cluster than to this one; the nearest analysed neighbour is `GPU-SC25-81` (AGILE, asynchronous GPU–SSD integration). **A verdict must not be inferred from the title alone** (`governance/ANTI_HALLUCINATION_RULES.md`) | — (gate not met) |

---

## Verdict-only papers

Access states below are stated with how they were determined. Where the row's
only evidence is this project's own census, that is said explicitly and the
verdict is marked provisional. **None of these rows may be used to justify a
deep analysis.**

| Paper | Venue/Year | Access state (how determined) | Evidence read | Isolation mechanism | Counterfactual answer | Verdict | Rationale |
|---|---|---|---|---|---|---|---|
| Dilu: Enabling GPU Resourcing-on-Demand for Serverless DL Serving via Introspective Elasticity | ASPLOS 2025, DOI `10.1145/3669940.3707251` | `PUBLIC_FULLTEXT` — **arXiv 2503.05130 located this pass** (`/html/2503.05130v1`), but the fetch was blocked by the same arXiv 429 wall | `TITLE_AND_CENSUS_ROW` + confirmed preprint URL | `UNKNOWN` (title implies intra-GPU elastic resourcing) | **NO (provisional, title-level)** — "GPU Resourcing-on-Demand" with "introspective elasticity" for serving implies scaling *within* a device | `CORE_GPU` (provisional) | **WATCHLIST — the best-value deferred deep analysis in this cluster**, because a public full text is confirmed to exist and is reachable outside the rate-limit window. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` (serving). |
| UGPU: Dynamically Constructing Unbalanced GPUs for Enhanced Resource Efficiency | ISCA 2025, DOI `10.1145/3695053.3731103` | `PENDING_FULLTEXT` — census records the ACM DL `/doi/full/` form as open; unreachable here (403). **Not `CLOSED_ACCESS`** | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — architectural reconfiguration of the compute:memory balance, i.e. a hardware partitioning primitive *below* MIG | **NO (title-level, provisional)** | `CORE_GPU` (provisional) | Already carried on the core-execution cluster's ledger (`_LEDGER_core_execution.md`) as a watchlist row. Noted here because "dynamically constructing unbalanced GPUs" is the architectural answer to the *same* mismatch `GPU-ISC26-165` measures empirically (MIG couples compute and memory in fixed, non-proportional ratios). **Cross-cluster read pair.** |
| Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs | ISCA 2026 | `CLOSED_ACCESS` (effectively) — ISCA 2026 program page only; `NOT_FOUND_AFTER_SEARCH` per census | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — "Resources Within GPUs" is title-explicit about intra-device partitioning | **NO (title-level, provisional)** | `CORE_GPU` (provisional) | Same shape as Bullet (`GPU-ASPLOS26-166`): balance work across devices *and* split resources within one. **WATCHLIST.** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| BOER: Enhancing Resource Utilization for Deep Learning Inference with Hybrid Spatial GPU Sharing | SC 2025, DOI `10.1145/3712285.3759857` | `PENDING_FULLTEXT` — census `UNKNOWN (not individually searched)`; SC 2025 ACM DL blocked here | `TITLE_AND_CENSUS_ROW` | "**Hybrid** Spatial GPU Sharing" — title implies combining two spatial mechanisms, most plausibly MIG + MPS, i.e. the same construction as ParvaGPU's "GPU segment". **Inference, not evidence.** | **NO (title-level, provisional)** | `CORE_GPU` (provisional) | **WATCHLIST — the closest direct successor to `GPU-SC24-161`.** If it is MIG+MPS it is a one-year-later competitor at the same venue and the comparison is the first thing to check. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| FluidFaaS: A Dynamic Pipelined Solution for Serverless Computing with Strong Isolation-based GPU Sharing | HPDC 2025 (Xinning Hui, Yuanchao Xu, Xipeng Shen) | `CLOSED_ACCESS` (effectively) — HPDC 2025 program page only; `NOT_FOUND_AFTER_SEARCH` per census | `TITLE_AND_CENSUS_ROW` | Title says "**Strong Isolation**-based GPU Sharing" — which in this cluster's vocabulary means MIG (the only mechanism anyone here calls strong). **Inference.** | **NO (title-level, provisional)** | `CORE_GPU` (provisional) | Direct contrast with `GPU-ASPLOS26-163` (gShare), which reaches serverless GPU sharing via a driver shim and *weak* (temporal) isolation. **WATCHLIST.** `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| ESG: Pipeline-Conscious Efficient Scheduling of DNN Workflows on Serverless Platforms with Shareable GPUs | HPDC 2024 (Xinning Hui, Yuanchao Xu, Zhishan Guo, Xipeng Shen) | `CLOSED_ACCESS` (effectively) — HPDC 2024 program page only | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — "Shareable GPUs" is title-explicit but names no mechanism | **`UNRESOLVED`** — the contribution word is *scheduling of DNN workflows*; the GPU sharing may be an assumed substrate rather than a contribution | `RELATED_GPU` (provisional) | Same group as FluidFaaS and one year earlier; reading the pair would show whether the group's contribution moved from *policy* to *mechanism*. Downgraded relative to FluidFaaS because "pipeline-conscious scheduling" is a policy over a shareable resource. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| RAP: Resource-aware Automated GPU Sharing for Multi-GPU Recommendation Model Training and Input Preprocessing | ASPLOS 2024, session 3C ML Cluster Scheduling | `CLOSED_ACCESS` (effectively) — census `NOT_SEARCHED`; no preprint located | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — "Automated GPU Sharing" between training and input preprocessing on the same devices | **NO (title-level, provisional)** — co-locating the data-preprocessing pipeline with training *on the GPU* is an intra-device resource-division problem | `CORE_GPU` (provisional) | Distinctive because the co-tenants are two stages of one job (like Bullet's prefill/decode), not two tenants. **WATCHLIST.** |
| PAL: A Variability-Aware Policy for Scheduling ML Workloads in GPU Clusters | SC 2024, DOI `10.1109/SC41406.2024.00032` | `PENDING_FULLTEXT` — census `UNKNOWN (not individually searched)` | `TITLE_AND_CENSUS_ROW` | **None** — cluster-level placement policy | **YES** — a variability-aware placement policy applies to any cluster of non-identical nodes | `RELATED_GPU` | Per-GPU performance variability is a real GPU fact, but the *contribution* is a scheduling policy that consumes it. Compare `GPU-IPDPS26-42` (already analysed), which finds production GPU run-to-run variability is **not** attributable to the GPUs — a direct and useful tension to check if PAL is ever read. |
| Fast and Fair Training for Deep Learning in Heterogeneous GPU Clusters | ICS 2025, GPU Scheduling session | `CLOSED_ACCESS` (effectively) — census `NOT_SEARCHED`; ICS 2025 proceedings PDFs *are* reachable at `hpcrl.github.io`, so this is **recoverable with one more fetch** | `TITLE_AND_CENSUS_ROW` | **None expected** — cluster fairness policy | **YES (provisional)** — fairness under heterogeneity is a generic scheduling problem | `RELATED_GPU` (provisional) | Recoverable cheaply from the same ICS 2025 proceedings host that supplied `GPU-ICS25-162`. Low expected GPU-mechanism content. |
| SortingHat: System Topology-aware Scheduling of Deep Neural Network Models on Multi-GPU Systems | ICS 2025, GPU Scheduling session | `CLOSED_ACCESS` (effectively) — as above, recoverable from `hpcrl.github.io` | `TITLE_AND_CENSUS_ROW` | **None expected** — placement over an interconnect topology | **NO (provisional, weak)** — NVLink/NVSwitch/PCIe topology asymmetry is a GPU-system property, but topology-aware placement is a generic technique | `RELATED_GPU` (provisional) | Belongs with the multi-GPU communication cluster rather than here. See `_LEDGER_multi_gpu_communication.md`. |
| Cephalo: Harnessing Heterogeneous GPU Clusters for Training Transformer Models | ICS 2025, GPU Scheduling session | `CLOSED_ACCESS` (effectively) — recoverable from `hpcrl.github.io` | `TITLE_AND_CENSUS_ROW` | **None expected** | **YES (provisional)** — heterogeneity-aware work partitioning for distributed training | `RELATED_GPU` (provisional) | Training-systems work; `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| NotebookOS: A Replicated Notebook Platform for Interactive Training with On-Demand GPUs | ASPLOS 2026, session 4A | `CLOSED_ACCESS` (effectively) — census `NOT_SEARCHED (deprioritised)` | `TITLE_AND_CENSUS_ROW` | **None expected** — on-demand allocation and replication at the platform level | **YES (provisional)** — a replicated interactive platform with on-demand resource attachment is not GPU-specific | `RELATED_GPU` (provisional) | Platform/systems contribution. Only a mechanism that attaches or detaches GPU *device state* (rather than scheduling whole GPUs) would change this. |
| Bullet — *see the priority table* | ASPLOS 2026 | `PUBLIC_FULLTEXT` | Full text + artifact | per-stream TPC masks | **NO** | `CORE_GPU` | **Promoted out of the verdict-only list to a full deep analysis** because both a public PDF and a public artifact proved reachable. |
| LEGO: Supporting LLM-Enhanced Games with One Gaming GPU | HPCA 2026 (first author Han Zhao) | `CLOSED_ACCESS` (effectively) — HPCA 2026 track page only; `NOT_FOUND_AFTER_SEARCH` per census | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — "One Gaming GPU" implies co-locating **rendering and LLM inference** on a consumer part, which has neither MIG nor (reliably) MPS | **NO (title-level, provisional)** — graphics and compute contending for the same SMs on a consumer GPU is a GPU-specific co-location problem | `CORE_GPU` (provisional) | **WATCHLIST, and the most *distinctive* missing paper here**: every other co-location paper in this cluster co-locates compute with compute. Graphics/compute co-location has a different contention structure, and the target hardware is precisely where MIG does not exist — the same regime SGDRC (`GPU-PPoPP25-164`) targets. |
| Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism | SC 2025, DOI `10.1145/3712285.3759784` | `PENDING_FULLTEXT` — census `UNKNOWN (not individually searched)` | `TITLE_AND_CENSUS_ROW` | **None expected** — parallelism assignment across heterogeneous devices | **YES (provisional)** | `RELATED_GPU` (provisional) | Heterogeneity + parallelism, not intra-device partitioning. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| ElasticRoom: Multi-Tenant DNN Inference Engine via Co-design with Resource-constrained Compilation and Strong Priority Scheduling | HPDC 2024 | `CLOSED_ACCESS` (effectively) — HPDC 2024 program page only | `TITLE_AND_CENSUS_ROW` | `UNKNOWN` — "**resource-constrained compilation**" implies compiling kernels to a bounded resource footprint, i.e. an occupancy/CTA-level cap decided at compile time | **NO (title-level, provisional)** — compiling a kernel to fit a constrained SM/register/shared-memory budget is a GPU-specific co-design | `CORE_GPU` (provisional) | **WATCHLIST.** If the reading is right, ElasticRoom is a *fourth* software-partitioning variant in this cluster — compile-time occupancy capping, versus SGDRC/Bullet's runtime TPC masking. That would be a distinct branch of the software-partitioning school and worth resolving. |
| Loki: A System for Serving ML Inference Pipelines with Hardware and Accuracy Scaling | HPDC 2024 | `CLOSED_ACCESS` (effectively) — HPDC 2024 program page only | `TITLE_AND_CENSUS_ROW` | **None expected** | **YES (provisional)** — scaling hardware allocation and model accuracy against load is device-agnostic | `RELATED_GPU` (provisional) | Census itself flags the device as not named in the title. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| CUDASTF: Bridging the Gap Between CUDA and Task Parallelism | SC 2024, DOI `10.1109/SC41406.2024.00049` | `PUBLIC_FULLTEXT` — author PDF at `mgarland.org/papers/2024/cudastf/` per census (not fetched this pass) | `TITLE_AND_CENSUS_ROW` | **None** — a task/stream programming model | **NO (provisional)** — a CUDA-stream/task-graph programming model built on CUDA's own dependency primitives | `CORE_GPU` (provisional) | **ROW OWNED BY THE COMPILER CLUSTER — adjudicated here only as a task-graph data point, and that cluster's verdict governs.** Recorded because it is the natural host-side counterpart to `GPU-ICS25-162`: CUDASTF keeps the task runtime on the host and ships in NVIDIA CCCL; Mustard moves the scheduler onto the device. **No claim about CUDASTF's content is made from this cluster.** |
| Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems | SC 2025, DOI `10.1145/3712285.3759883` | `PENDING_FULLTEXT` — census `UNKNOWN (not individually searched)` | `TITLE_AND_CENSUS_ROW` | Not applicable | — | — | **ROW OWNED BY THE PROFILING/RELIABILITY CLUSTER.** Noted here only because "fine-grained failure management" touches the fault-isolation gap that both `GPU-PPoPP25-164` and its arXiv version concede ("cannot isolate colocated DNNs' GPU runtime errors"). See `_LEDGER_profiling_reliability.md`. No verdict issued from this cluster. |
| SPPO: Making Million-Token LLM Training Practical on Modest GPU Clusters | ICS 2026, session S08 | `CLOSED_ACCESS` (effectively) — census `NOT_SEARCHED` | `TITLE_AND_CENSUS_ROW` | **None expected** | **YES (provisional)** — long-context training parallelism/memory strategy | `RELATED_GPU` (provisional) | Training-systems work, outside this cluster's spine. `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. |
| DEFT: Joint Task Placement and DVFS for Energy-Efficient Multi-GPU Runtimes | ICS 2026, session S22 Energy-Aware Systems (J. Chen, M. Pericàs) | `CLOSED_ACCESS` (effectively) — census `NOT_SEARCHED` | `TITLE_AND_CENSUS_ROW` | **None** — placement plus frequency control | **Probably YES (title-level)** — the current evidence names a classic scheduling formulation using GPUs as controlled resources, not a GPU-internal mechanism | `RELATED_GPU` (provisional, title-level) | **Authoritative classification is owned by `_LEDGER_power_energy.md:80`; overlap noted only.** `GPU-ISC26-165` finds that power throttling is the interference channel MIG does not isolate, so a multi-GPU runtime that controls DVFS is manipulating exactly the resource that defeats hardware partitioning. |

---

## Isolation-mechanism roll-up

Every paper in this cluster for which a mechanism could be established, ordered by
where the partition boundary is drawn. **This is the cluster's central finding.**

| Boundary drawn in | Mechanism | Quantum | Reconfiguration cost | Papers | Leaks through |
|---|---|---|---|---|---|
| **Hardware (silicon partition)** | **MIG** GPU instances, optionally subdivided into compute instances (`1c.7g`) | A100: 1/2/3/4/7 GPCs (5 and 6 illegal). H100 96 GB: 16/32/60/64/132 SMs at `1g.12gb`…`7g.96gb` | **Offline only** — "not possible while GPU applications are running"; ParvaGPU's artifact does `nvidia-smi mig -dci; -dgi` and kills MPS before `-cgi` | `GPU-SC24-161` (ParvaGPU), `GPU-ISC26-165`, SMART-MIG (abstract-level), BOER + FluidFaaS (provisional) | **Last-level TLB** (`GPU-MICRO24-02`, STAR: 40% average loss co-running vs isolation) and **device-wide power/clock domain** (`GPU-ISC26-165`) |
| **Hardware (process multiplexing)** | **MPS** | Client process; optionally `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` — **not used by any paper analysed here** | Start/stop the control daemon | `GPU-SC24-161` (within a MIG instance, same model only), baseline in `GPU-ISC26-165` and `GPU-PPoPP25-164` | Caches, memory controllers, VRAM bandwidth — "cannot isolate VRAM bandwidth" (`GPU-PPoPP25-164`) |
| **Software (SM/TPC masking)** | **TPC bitmask written through `libsmctrl`**, which "co-opts preexisting debug logic in the CUDA driver library" (CUDA ≤ 12.6) | **1 TPC = 2 SMs**; per-stream, per-launch or global | **Microsecond-level**; Bullet rewrites the mask only when the decision changes | `GPU-PPoPP25-164` (SGDRC, via TMD, + persistent threads + `ld.cv` eviction flag), `GPU-ASPLOS26-166` (Bullet, per-stream masks, disjoint ranges from opposite ends) | Memory system — unless separately colored. Bullet leaves it shared **by design**; SGDRC colors it |
| **Software (memory channels)** | **VRAM-channel page colouring** via shadow page table + modified `nvidia-uvm`, over a reverse-engineered non-linear hash | 1–4 KiB sectors (2 KiB used); $Ch_{BE}=1/3$ | Bimodal tensors switch the colour set at LS-activity boundaries | `GPU-PPoPP25-164` only | Requires kernel source; closed vendor libraries (cuDNN/cuBLAS/CUTLASS) are excluded |
| **Driver (mediated device)** | **`vfio-mdev` vGPU**, 57 intercepted ioctls (17 `NV_ESC` + 40 UVM), 60 kLOC | Memory slice 128 MB – 40 GB (continuous); compute = whole GPU per slice | vGPU hot-plug ~700 ms → <1 ms | `GPU-ASPLOS26-163` (gShare) | **Everything spatial** — SM under-fill within a slice is conceded, and kernels >20 ms break the period |
| **Time only** | **Round-robin channel activation**, one active channel per 20 ms period | Whole GPU | Period boundary | `GPU-ASPLOS26-163`; baseline in `GPU-ISC26-165` | SM occupancy entirely |
| **None (not a sharing system)** | Device-side task-graph scheduling; voluntary occupancy accounting | Subgraph (≤120 per device) | n/a | `GPU-ICS25-162` (Mustard) | Vendor libraries defeat the occupancy accounting (cuBLAS/cuSOLVER choose their own block/thread counts) |
| **None at the device level** | Job/spot-instance preemption at cluster scope | Job | n/a | GFS (`RELATED_GPU`) | n/a — this is why it is `RELATED_GPU` |

### What each school says about the others' isolation guarantees

Taken from the papers' own words, not from this project's editorialising:

- **The software school on MIG.** SGDRC: MIG "is available only in a few flagship
  GPUs … its granularity is too coarse … and can only reconfigure the allocation
  when it is idle." `[paper]` Bullet ships MPS support but "replaced [it] with
  libsmctrl for dynamic control." `[paper]`
- **The software school on MPS.** SGDRC: MPS "statically partitions GPUs at the
  thread slice level and cannot isolate VRAM bandwidth, resulting in unmanaged
  contention among colocated services." `[paper]`
- **The software school on temporal sharing.** SGDRC: "temporal multiplexing …
  cannot fully harness the GPU's resources, as BE tasks may be starved due to
  frequent LS task preemption." `[paper]`
- **The temporal school on itself.** gShare concedes the same point:
  "GPU virtualization is actually a temporal GPU sharing technology", risking
  underutilization "if kernels cannot fill all SM cores." `[paper]`
- **The hardware school on software sharing.** ParvaGPU's justification for MIG
  is that under MPS "internal GPU resources such as caches and memory controllers
  are shared among workloads, this could lead to interference issues." `[paper]`
  Its baseline set contains **no** software-partitioning system.
- **The corpus on all of them.** `GPU-MICRO24-02` (STAR) shows MIG does not
  partition the last-level TLB; `GPU-ISC26-165` shows MIG does not partition
  power. **No mechanism in this cluster provides complete isolation, and no paper
  in this cluster evaluates its mechanism against a mechanism from a different
  school on the same silicon.**

### The convergence question, answered from the evidence

GPU sharing research is **not** converging on one mechanism. It has **forked by
hardware availability**:

- Where MIG exists (A100/H100 and successors), work accepts the lattice and
  optimises placement inside it — ParvaGPU, SMART-MIG, BOER, and the
  characterisation work.
- Where MIG does not exist (Pascal, Turing, consumer and mid-range parts, and
  gaming GPUs), work rebuilds partitioning in software on top of an **undocumented
  CUDA driver debug path** — SGDRC and Bullet both depend on `libsmctrl`, and
  SGDRC's evaluation hardware (Tesla P40, RTX A2000) is precisely the set MIG
  cannot serve. SGDRC states that A100/H100 would "require slight adaptation".
- Where neither is acceptable because tenants are untrusted and unmodifiable,
  work goes **below** CUDA into the kernel driver and gives up spatial sharing
  entirely — gShare.

The forks are essentially untested against each other: **SGDRC evaluates on GPUs
that have no MIG; ParvaGPU and the ISC characterisation evaluate on GPUs that do;
gShare compares only against FaaS caching systems.** The one shared dependency
across the software fork — `libsmctrl`, a reverse-engineered co-option of CUDA
driver debug logic pinned at CUDA ≤ 12.6 — is a single point of failure for two
top-tier systems papers, and neither paper discusses what happens when NVIDIA
removes it.

---

## Stable IDs used in this pass

`GPU-SC24-161`, `GPU-ICS25-162`, `GPU-ASPLOS26-163`, `GPU-PPoPP25-164`,
`GPU-ISC26-165`, `GPU-ASPLOS26-166`.
IDs `167`–`179` in this cluster's assigned band remain unused and are reserved
for the watchlist papers above (SMART-MIG, µShare, AGIO, Dilu, BOER, LEGO,
ElasticRoom, FluidFaaS, Symbiotic MLLM Serving, RAP).

## Watchlist, in priority order

1. **µShare** (HPCA 2026) — "Non-Intrusive Kernel Co-Locating"; would resolve the
   limitation both software-partitioning papers concede. No public copy found.
2. **SMART-MIG** (IPDPS 2026) — full text is open, blocked only by arXiv rate
   limiting this session. Need: whether it models MIG's legal profiles, placement
   slots, offline-only reconfiguration and power coupling, and whether the
   evaluation is real hardware or simulation.
3. **Dilu** (ASPLOS 2025) — arXiv 2503.05130 confirmed to exist; same 429 wall.
4. **BOER** (SC 2025) — "hybrid spatial GPU sharing"; the direct successor to
   ParvaGPU at the same venue.
5. **LEGO** (HPCA 2026) — graphics/compute co-location on a consumer GPU; the only
   non-compute-vs-compute co-location case in the cluster.
6. **ElasticRoom** (HPDC 2024) — possible compile-time occupancy capping, a fourth
   software-partitioning branch.
7. **AGIO** (ASPLOS 2026) — `UNRESOLVED`; likely belongs to a GPU-storage cluster.

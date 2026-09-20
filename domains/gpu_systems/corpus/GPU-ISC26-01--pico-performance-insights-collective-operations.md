# GPU-ISC26-01 — PICO: Performance Insights for Collective Operations

gpu_relevance: `RELATED_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `M GPU-aware / GPU-initiated communication & collectives`
secondary_topics: `L Multi-GPU interconnect & data paths`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2508.16809v1) read across what PICO is, backend architecture, metrics and metadata/reproducibility model, the four case-study findings, §4.3 rail-tuning case study, limitations, and related work (OMB, IMB, nccl-tests, CommBench). Figures not individually transcribed.`

## 12.1 Bibliographic facts
- Title: *PICO: Performance Insights for Collective Operations* `[paper]` `[census]`
- **Author-list conflict, recorded and NOT resolved by choosing.** The arXiv HTML v1 read here gives **Saverio Pasqualoni, Lorenzo Piarulli, Daniele De Sensi (Sapienza University of Rome)** `[paper]`. The official ISC 2026 program, per census `ISC_2026.md`, gives **Tommaso Bonato, Lorenzo Piarulli, Torsten Hoefler, Marco Canini, Daniele De Sensi**, with **Saverio Pasqualoni (KAUST / Sapienza) as speaker** `[census]` `[official-web]`. Only Piarulli and De Sensi appear in both. The arXiv version read may be an earlier author set. Both lists are recorded.
- Venue: **ISC High Performance 2026, Hans Meuer Research Paper Award session**, `CONFIRMED_IN_POPULATION` `[census]`. Publisher version stated open access at IEEE Xplore; DOI not retrieved (Xplore returns HTTP 418 from this environment).
- Publication type: `ARCHIVAL_MAIN_PAPER`; read source is the `PREPRINT`.

## 12.2 Core question (one sentence)
How much performance is lost to collective-algorithm and backend-parameter *selection* on production GPU supercomputers, and can a single framework measure that loss reproducibly across MPI, NCCL and RCCL with phase-level attribution? `[paper]`

## 12.3 GPU/HPC problem translation
- **Communication**: collective throughput and latency across message sizes and node counts; network traffic estimation split into local vs global link usage.
- **Memory**: explicitly separated out — memory allocation and copying are measured as their own phase, which produces the paper's most useful finding.
- **Compute**: reduction arithmetic inside allreduce is measured as a distinct phase.
- **Scheduling**: algorithm selection is the object of study.
- **Synchronization**: not separately instrumented in the read text.

## 12.4 Why the problem exists
Root causes the paper establishes `[paper]`:
1. **Library defaults are chosen once and not per platform.** Measured consequence: default MPI algorithm choice falls short of optimal "typically by around 30–40%, and in the worst cases achieving only 1/5 of optimal performance", on Leonardo, LUMI and MareNostrum 5.
2. **Backend transport parameters are invisible but decisive.** Changing UCX's `UCX_MAX_RNDV_RAILS` from 2 to 4 on a **2,048-node Leonardo allreduce** produced "performance differences of more than ×2 for certain message sizes".
3. **Existing tools cannot express the experiment.** OMB does not capture runtime metadata and does not integrate algorithm selection into its interface; IMB is MPI-only; nccl-tests is tied to NCCL with no cross-library comparison; CommBench is extensible but has minimal metadata logging and requires writing low-level benchmarking logic.
4. **Cost models under-determine reality.** Distance-doubling and distance-halving reduce-scatter have *identical* cost-model profiles yet differ measurably on hardware due to locality in the communication sequence — so a model cannot substitute for measurement.

## 12.5 Mathematical / performance model
PICO does not contribute a model; it contributes the apparatus that falsifies models. The paper's explicit finding is that two algorithms with identical α–β-style cost-model profiles (distance-doubling vs distance-halving reduce-scatter) diverge on real hardware. `[paper]`
Network traffic estimation distinguishes local vs global link usage; the estimator's formulation was not recovered — `UNKNOWN`.

## 12.6 Data layout and ownership
- **rank → GPU**: resource allocation is tracked as node-to-rank and GPU mappings in CSV.
- **configuration ownership**: environment configuration files (JSON) describe cluster characteristics once and are reused; test configuration files specify collective, algorithm, message sizes and backend.
- **build isolation**: separate compilation per backend library, so NCCL/RCCL/MPI measurements are not contaminated by a shared build.
- thread/warp/block-level: not applicable — PICO does not instrument inside collective kernels.

## 12.7 Pseudo code
Reconstructed workflow `[reconstruction]`; the only literal identifier is the UCX variable the paper names `[paper]`:
```
env.json   := {cluster topology, GPUs per node, rails, software versions}   # written once
test.json  := {collective, algorithm, backend, message sizes, iterations}
run(env.json, test.json):
    for each iteration, each rank:
        record execution time; record phase breakdown
        (phases instrumented by MANUALLY INSERTED MACROS in the algorithm code)
    capture metadata: env vars (e.g. UCX_MAX_RNDV_RAILS), library versions,
                      backend config, hardware setup, node->rank and GPU mappings (CSV)
aggregate: min / max / mean per rank and per iteration
```

## 12.8 Real implementation
The official ISC abstract calls PICO "an open-source benchmarking framework", but **no repository URL was exposed on any page read** — census records `NOT_FOUND_AFTER_SEARCH` and the paper as read gives no artifact URL. `NOT_INSPECTED`. **No symbols asserted.** The one literal identifier reported is the UCX environment variable `UCX_MAX_RNDV_RAILS`, which the paper prints. `[paper]` `[census]`

## 12.9 Kernel execution
`NOT_IN_PAPER` / not applicable. PICO measures collective libraries from outside; it does not instrument kernel, CTA, warp or instruction behaviour. Phase-level instrumentation is by **manually inserted macros in algorithm code**, which is a source-level, not kernel-level, mechanism.

## 12.10 Memory traffic
PICO's most substantive GPU-relevant result is a memory-path result `[paper]`: for **allreduce on Leonardo**, memory allocation and copying have "only a minor impact for small messages (up to 128 KiB), but become a major contributor, around **50% of the total runtime**, once the message size reaches **1 MiB**". This identifies buffer management, not the wire, as half the cost in that regime — a decomposition that `GPU-SC24-01`'s end-to-end curves could not produce.
Register/shared/L1/L2/HBM decomposition: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)
PICO is not faster than anything; it explains why others are slower. Its decomposed causes `[paper]`:
1. **Default algorithm ≠ best algorithm**: 30–40% typical loss, up to 5× worst case, across three named systems.
2. **Rail count in the transport layer** changes allreduce performance by >2× at 2,048 nodes (`UCX_MAX_RNDV_RAILS` 2→4).
3. **Buffer management dominates at ≥1 MiB** (~50% of allreduce runtime on Leonardo).
4. **Cost-model-equivalent algorithms differ on hardware** due to communication-sequence locality.
Census additionally records, from the official ISC abstract, that defaults can be "up to 5x slower than the best available choice" and that LLM-training simulations show "reductions in training times of up to 44%" `[census]` `[official-web]` — the 44% figure was **not** found in the arXiv text read here and is therefore carried as official-abstract evidence only, not `[paper]`.

## 12.12 Hardware generation dependence
- Systems: **Leonardo, LUMI, MareNostrum 5**. Leonardo is described with a Dragonfly+ topology and 100 Gbps links; LUMI's topology is inferred in the read text rather than stated.
- **GPU SKUs are not named in the read text — `UNKNOWN`.** This is a substantive weakness for a GPU-corpus entry: the paper names multi-GPU nodes and scale-up fabrics (NVLink, Infinity Fabric, and forward-looking UALink) and scale-out fabrics (InfiniBand, Slingshot, Ultra Ethernet) generically. (Cross-reference: `GPU-SC24-01` establishes Leonardo as 4× A100 and LUMI-G as 4× MI250X / 8 GCDs — but that is *that* paper's evidence, not this one's, and must not be silently attributed here.)
- **Rails**: §4.3 shows `UCX_MAX_RNDV_RAILS` default 2, tested to 4; the paper notes multi-rail configurations exist but are not standardized across platforms.
- The framework is generation-independent by design; its *findings* are explicitly platform-specific and the authors acknowledge limited generalizability.

## 12.13 Limitations
Author-stated and read-established `[paper]`:
1. **Tuning artifacts are manual**: users "create these tuning artifacts manually by translating measured performance data into rule files"; automation is future work. So PICO diagnoses but does not fix.
2. **Phase instrumentation requires manual macro insertion** in algorithm code — not automated, and not applicable to a closed library's internals.
3. **Backend coverage is MPI / NCCL / RCCL only**; no SHMEM, no standalone UCX, and — critical for this cluster — **no NVSHMEM and no device-initiated backend**.
4. It is unclear whether all low-level transport behaviours are captured.
5. Findings are platform- and configuration-specific.

## 12.14 Relation to prior corpus
- No prior in-repo analysis. `[repo-grep]` `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` applies.
- **Successor to `GPU-SC24-01`** (shared author Daniele De Sensi): same thesis — the default GPU collective path is not the best one — advanced from a three-system measurement study to a reusable, metadata-capturing framework with phase attribution. **Whether the arXiv version cites the SC24 paper could not be settled**: the read pass reported it both as an omission and as bibliography entry [12]. Recorded `UNKNOWN`; the shared authorship makes a citation likely but that is `[inference]`, not evidence.
- **Directly critiques CommBench** (ICS 2024, verdict-only in this cluster's ledger): credits it as "a significant step toward extensibility" with a library-agnostic API, but faults its minimal metadata logging and steep learning curve, and notes it assumes a one-process-per-GPU execution model. This is the cluster's clearest benchmark-lineage relation. `[paper]`
- **Critiques nccl-tests** as NCCL-locked — relevant because NCCLZ (`GPU-SC26-22`) and Big Send-off (`GPU-IPDPS26-02`) both report against nccl-tests-style baselines.
- **Complementary** to every optimization paper in this cluster: PICO supplies the selection-cost baseline that MSCCL++, PCCL and NIMBLE each implicitly claim to capture.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**PARTIALLY YES — and this is why the verdict is `RELATED_GPU` rather than `CORE_GPU`.** PICO is a *hybrid* benchmarking framework: it measures CPU-based MPI collectives and GPU-resident-buffer NCCL/RCCL collectives with the same apparatus, and the paper states it is "agnostic to whether data moves via GPU or CPU". Its headline findings — default algorithms are 30–40% off optimal; a transport rail parameter changes results by >2×; cost-model-equivalent algorithms differ on hardware — are properties of collective-library *selection*, and each would be reproducible in a CPU-only MPI study.

The GPU-specific elements are real but supporting rather than constitutive: NCCL and RCCL backends and GPU-resident buffers; GPU-specific tuning knobs (the paper names the number of channels in *CCL); GPU-to-GPU measurement over scale-up fabrics; and node-to-rank *and GPU* mapping capture. The one finding that is meaningfully GPU-flavoured is the memory-allocation/copy phase reaching ~50% of allreduce runtime at ≥1 MiB on Leonardo, since GPU buffer staging is the specific cost being isolated.

**Control placement**: `host-driven`, and PICO **cannot observe anything else**. All supported backends (MPI, NCCL, RCCL) are host-enqueued. The paper does not emphasize device-initiated DMA versus CPU-driven paths, lists no SHMEM/NVSHMEM backend, and therefore provides no measurement of device-resident or device-triggered communication. Established from the full text. `[paper]` This is itself a finding: as of ISC 2026, the field's most capable collective-benchmarking framework has no device-initiated backend.

verdict_basis: `RELATED_GPU`. The framework's central findings concern collective-algorithm and transport-parameter selection, which are not GPU-specific and would replicate on CPU-only MPI; the GPU content (NCCL/RCCL backends, GPU-resident buffers, *CCL channel tuning, GPU-buffer staging cost isolation) makes it a genuine and useful instrument for this cluster without making the contribution itself GPU-dependent.

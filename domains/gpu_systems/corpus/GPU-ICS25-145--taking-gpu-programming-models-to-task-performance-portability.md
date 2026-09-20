# GPU-ICS25-145 — Taking GPU Programming Models to Task for Performance Portability

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `H — GPU programming models (portability layers) and their compiler/backend behaviour`
secondary_topics: `performance portability metrics; vendor compiler/backend quality (NVHPC, ROCmCC, DPC++, AdaptiveCpp, Clacc); occupancy and register pressure as compilation outcomes; warp-level reduction codegen; profiling (Nsight Compute, Omniperf)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via the ICS 2025 proceedings PDF (https://hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-63.pdf), read in two passes — (a) title/authors/affiliations/venue, motivation and research question, the seven programming models, the five proxy applications, the five machines and their GPUs, the P-parallel portability metric; (b) results per model and application, the per-kernel root-cause analysis (registers per thread, static instruction counts, occupancy, warp stalls, L1/L2 behaviour, reduction codegen, shared-memory use, struct alignment), the full compiler/toolchain version table per system, threats to validity and the explicit non-tuning decision, conclusions and recommendations, related work. An arXiv preprint (2402.08950) and two author-hosted PDFs also exist; the ICS proceedings PDF was used.`

## 12.1 Bibliographic facts

- Title: **Taking GPU Programming Models to Task for Performance Portability** [paper].
- Venue: **ICS '25** — "2025 International Conference on Supercomputing, June 8–11, 2025, Salt Lake City, UT, USA" [paper]. Census places it in the **Performance Analysis** session [census: `domains/gpu_systems/census/ICS_2025.md`, row 22].
- DOI: `10.1145/3721145.3730423` (from the publisher landing page surfaced in search; `dl.acm.org` is 403 here so it was not dereferenced) — recorded as `[official-web]`-grade evidence, not `[paper]`.
- Authors and affiliations [paper]: **Joshua Hoke Davis, Pranav Sivaraman, Joy Kitson, Isaac Minn, Abhinav Bhatele** (University of Maryland, Department of Computer Science); **Konstantinos Parasyris, Harshitha Menon, Giorgis Georgakoudis** (Lawrence Livermore National Laboratory).
- Preprint: **arXiv 2402.08950** (v2 exists) — `PREPRINT` of the same work; the ICS proceedings PDF was the version read.
- Artifact: no repository URL was read in the fetched PDF. `NOT_INSPECTED`; **no source symbols asserted**.
- Publication type: `ARCHIVAL_MAIN_PAPER`.

## 12.2 Core question (one sentence)

Across two GPU vendors and three NVIDIA generations, which of the seven GPU programming models a scientific application might be written in actually deliver performance close to the best-observed implementation on every machine — and when they do not, is the cause the *model*, the *vendor compiler*, or the *port*?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's root-cause findings are overwhelmingly about *how much work the compiler emitted*: e.g. OpenMP miniBUDE generates "dramatically more static instructions (1463 vs. 357)" than the reference [paper]; Kokkos "generates a 797-instruction kernel" [paper]. The portability failure is a code-generation failure.
- **Memory.** su3_bench's "complex number struct" causes OpenMP/OpenACC to issue "twice as many global loads and stores as CUDA"; aligning the struct to `sizeof(T) * 2` recovers the loss [paper]. This is a coalescing failure caused by a *language-level* data declaration.
- **Synchronization.** Reductions are named as "a major bottleneck" [paper]. The mechanism is explicit: RAJA "take[s] advantage of warp-level primitives and shared memory to perform the reduction", while Kokkos CloverLeaf does "2D reduction instead of collapsing the kernel into a 1D reduction" and loses performance [paper]. So the difference between two portability libraries is whether their backend emits a warp-shuffle reduction.
- **Scheduling / occupancy.** su3_bench under OpenACC runs at "only 36 threads per block despite iterations being assigned to blocks of size 128"; loop collapsing fixes it [paper]. Kokkos CloverLeaf shows "barrier warp stalls" and "fewer eligible warps on average" [paper].
- **Communication.** Single-GPU kernels; no inter-GPU aspect. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (root cause)

- **The abstraction layers do not control the things that determine GPU performance.** Registers per thread, block size, shared-memory usage and reduction strategy are chosen by a *backend*, and the portability model gives the programmer no portable handle on them. The paper's own recommendation list names the consequences: "improved compiler handling of reductions, techniques to reduce register spilling, more semantic-preserving performance tuning knobs" [paper].
- **The two vendors' toolchains are at different maturity.** The paper's per-system compiler table (12.8) shows OpenACC on AMD depends on **Clacc 2023-08-15**, which could not even compile CloverLeaf ("lack of support for the `host_data` clause" [paper]) — so "OpenACC struggles with AMD systems" [paper] is partly a statement about one compiler's completeness, not about the model.
- **Directive models cannot express GPU-only resources.** The paper reports being "unable to add dynamic shared memory allocation inside the kernel for OpenMP and OpenACC ports due to lack of support" [paper]. The scratchpad is invisible to the directive model — which is a *language design* root cause, not a compiler bug.
- **Arithmetic intensity itself is not portable.** XSBench shows "substantially different arithmetic intensity" between AMD (**1.00**) and NVIDIA (**0.26**) [paper, Figure 1 roofline]. The same source code lands on a different part of the roofline on the two vendors, which bounds what any model can do.

## 12.5 Mathematical / performance model

- **Metric**: **P∥**, the **harmonic mean of application efficiency across systems**, where "application efficiency is the ratio of minimum observed runtime to actual runtime", producing values in 0–1.0 with 1.0 meaning best performance on all systems [paper]. The harmonic mean is what makes a single bad platform dominate the score — that property is the metric's whole point.
- **Provenance of the metric**: Pennycook et al. [paper, refs 33–36, 44]. Alternatives the paper discusses: Daniel et al.'s `P_D` accounting for problem size; Marowka's comparison of `P_p` with an arithmetic-mean variant `P_a` [paper].
- **Roofline** is used as the secondary model: arithmetic intensity vs achieved performance; "most kernels are memory-bound except miniBUDE (compute-bound)" [paper, Figure 1].
- **Measurement noise**: "runs of a given setup differing by at most 3.3%" [paper] — the paper's own bound on what differences are meaningful.

## 12.6 Data layout and ownership

- **thread**: registers per thread is a headline diagnostic — OpenMP miniBUDE at "62 vs. 62 registers per thread" alongside the instruction-count blow-up [paper, as printed; the two numbers being equal is what makes the instruction count the explanatory variable]; Kokkos at "69 registers per thread" [paper].
- **warp**: the level at which reductions either are or are not done well — RAJA uses "warp-level primitives and shared memory" [paper]; Kokkos CloverLeaf's "barrier warp stalls" and "fewer eligible warps" are the observed symptom [paper].
- **thread block**: block size is deliberately *not* tuned ("we specifically do not tune kernel grid size, block size, and shared memory per block" [paper]) — which makes the OpenACC 36-threads-per-block finding a genuine model/compiler artefact rather than a tuning artefact.
- **shared memory / LDS**: a first-class variable — miniBUDE RAJA was initially "not making use of shared memory", later given "dynamic allocating shared memory" [paper]; OpenMP and OpenACC cannot request it in-kernel at all [paper].
- **SM / CU**: L1 and L2 behaviour are reported per vendor via Nsight Compute (NVIDIA) and Omniperf (AMD) [paper].
- **GPU SKUs, all five** [paper]: **NVIDIA V100** (Summit, ORNL), **NVIDIA A100** (Perlmutter, NERSC), **NVIDIA H100** (Zaratan, UMD), **AMD MI50** (Corona, LLNL), **AMD MI250X** (Frontier, ORNL).
- **node/cluster**: single-GPU measurements on those machines; no scaling study. `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# --- the study design, as described -------------------------------  [paper]
models = { CUDA, HIP, SYCL, Kokkos, RAJA, OpenMP(target), OpenACC }
apps   = { BabelStream, XSBench, CloverLeaf, su3_bench, miniBUDE }
systems= { Summit/V100, Perlmutter/A100, Zaratan/H100,
           Corona/MI50, Frontier/MI250X }

# deliberately NOT tuned: grid size, block size, shared memory per block
for (m, a, s) in models x apps x systems:
    t[m][a][s] = median_runtime(build(m, a, s))     # <= 3.3% run-to-run spread

app_eff[m][a][s] = min_over_m'( t[m'][a][s] ) / t[m][a][s]
P_parallel[m][a] = harmonic_mean over s of app_eff[m][a][s]

# root-cause pass, per (m, a, s) outlier
diagnose with Nsight Compute  (NVIDIA): occupancy, shared memory per block,
                                        static instruction count, DRAM traffic,
                                        registers per thread
        with Omniperf        (AMD)   : Gflop/s, L1/L2 cache behaviour
```

`[reconstruction]` applies to the loop shape. Model names, application names, machine/GPU names, the metric definition, the non-tuning decision and the two profilers' metric lists are printed in the paper.

## 12.8 Real implementation

No system is built; the artefact is the study. What can be pinned precisely is the **toolchain matrix**, which is the paper's most reusable factual contribution [paper]:

| Programming model | NVIDIA toolchain | AMD toolchain |
|---|---|---|
| CUDA | GCC 12.2.0 | N/A |
| HIP | N/A | ROCmCC 5.7.0 |
| SYCL | DPC++ 2024.01.20 | DPC++ 2024.01.20 |
| Kokkos | GCC 12.2.0 | ROCmCC 5.7.0 |
| RAJA | GCC 12.2.0 | ROCmCC 5.7.0 |
| OpenMP | NVHPC 24.1 | LLVM 17.0.6 |
| OpenACC | NVHPC 24.1 | **Clacc 2023-08-15** |

Noted exceptions [paper]: "For SYCL port of CloverLeaf, **AdaptiveCpp 23.10.0** is consistently superior"; "**ROCmCC 5.7.0** for OpenMP su3_bench on AMD GPUs".

**These versions are the paper's expiry date.** Any reuse of its conclusions must restate them — an OpenACC-on-AMD verdict resting on Clacc 2023-08-15 is not a verdict on OpenACC.

Profilers used: **Nsight Compute** (NVIDIA) and **Omniperf** (AMD) [paper]. No repository located; `NOT_INSPECTED`.

## 12.9 Kernel execution

- **kernel**: the unit of measurement and of root-causing. The instruction-count comparisons (1463 vs 357 for OpenMP vs reference on miniBUDE; 797 for Kokkos [paper]) are per-kernel static counts from Nsight Compute.
- **thread block**: OpenACC su3_bench launching "only 36 threads per block despite iterations being assigned to blocks of size 128" [paper] is a compiler-chosen launch geometry that the source does not control.
- **warp**: warp-level primitives in RAJA's reduction vs their absence in the alternatives [paper]; "barrier warp stalls" and "fewer eligible warps on average" for Kokkos CloverLeaf [paper].
- **instruction**: static instruction count is the paper's primary explanatory variable for OpenMP/Kokkos regressions [paper].

## 12.10 Memory traffic

- **Global loads/stores**: su3_bench under OpenMP/OpenACC issues "twice as many global loads and stores as CUDA" because of a complex-number struct; the fix is alignment to `sizeof(T) * 2` [paper]. This is the cleanest example in the paper of a *source-level* declaration determining coalescing.
- **L1/L2**: "L1 cache bandwidth", "L2 cache hit rate", "stalls on L2 cache data" are named diagnostics; the register/instruction bloat produces a "**500% increase in cycles spent in L2 cache activity**" [paper].
- **DRAM traffic** is collected via Nsight Compute [paper].
- **Roofline placement**: most kernels memory-bound; miniBUDE compute-bound; XSBench arithmetic intensity **1.00 on AMD vs 0.26 on NVIDIA** [paper].

## 12.11 Why it is faster/slower (decomposed cause)

Scores [paper, P∥ across the five systems]:

| Model | Range across the five applications |
|---|---|
| SYCL | **0.91** (BabelStream dot) – **0.97** (su3_bench) |
| RAJA | **0.67** (miniBUDE) – **0.99** (XSBench) |
| Kokkos | **0.80** (CloverLeaf) – **0.99** (XSBench) |
| OpenACC | **0.54** (miniBUDE) – **0.93** (XSBench) |
| OpenMP | **0.41** (miniBUDE) – **0.95** (XSBench) |

Headline statements [paper]: "SYCL most consistently achieves performance portability for our tests, followed closely by RAJA and Kokkos"; "CUDA almost always performs at or near the best observed performance" on NVIDIA systems; "OpenACC struggles with AMD systems".

Decomposed causes, each tied to a named mechanism rather than to the score:

1. **Instruction-count inflation** in the directive models and Kokkos on miniBUDE (1463 vs 357; 797) → register pressure → "500% increase in cycles spent in L2 cache activity" [paper].
2. **Reduction lowering.** Warp-level primitives + shared memory (RAJA) vs a 2D reduction that was not collapsed (Kokkos CloverLeaf) [paper].
3. **Launch geometry chosen by the compiler**, not the source (OpenACC, 36 threads/block) [paper].
4. **Coalescing lost to a struct layout** (su3_bench complex type) [paper].
5. **Inability to request shared memory** in OpenMP/OpenACC [paper] — a capability gap, not a tuning gap.
6. **Toolchain completeness**, notably Clacc on AMD [paper].

Note the direction of the miniBUDE result: it is the **compute-bound** application, and it is where every portability layer scores worst (RAJA 0.67, OpenACC 0.54, OpenMP 0.41). The abstractions cost most exactly where register allocation matters most.

## 12.12 Hardware generation dependence

- Spans **three NVIDIA generations (V100 Volta, A100 Ampere, H100 Hopper)** and **two AMD generations (MI50 GCN/Vega, MI250X CDNA2)** [paper]. That breadth is the study's point, and it is unusually wide for this corpus.
- Findings are **tied to specific toolchain versions** (12.8), not to silicon generations, with the important exception of the roofline/arithmetic-intensity divergence between AMD and NVIDIA on XSBench, which is an architectural fact.
- No Intel GPU (Aurora/PVC) is included, despite SYCL being the best-scoring model — a notable scope gap given SYCL's Intel provenance. `NOT_IN_PAPER`.

## 12.13 Limitations

Stated by the paper:

- **Deliberate non-tuning**: "we specifically do not tune kernel grid size, block size, and shared memory per block" to keep the comparison fair [paper]. This cuts both ways: it isolates the model/compiler, but it means the numbers are not what a tuned application would see.
- **One baseline is admittedly immature**: the XSBench HIP port was "created using Hipify tool", so it is "not a fully optimized and mature baseline" [paper]. Any AMD comparison against it inherits that caveat.
- **A missing cell**: CloverLeaf OpenACC on AMD could not be built with Clacc (`host_data` unsupported), so that configuration is absent [paper].
- **Capability gaps counted as model results**: dynamic in-kernel shared memory is unavailable in the OpenMP and OpenACC ports [paper].
- **Tooling gap the authors flag**: "Line-level stall attribution is a crucial capability missing from Omniperf" [paper] — i.e. the AMD-side root-causing is shallower than the NVIDIA-side by construction.
- Five proxy applications, not full applications.

## 12.14 Relation to prior corpus

- **Direct methodological sibling of `GPU-SC26-41` (Leo, cross-vendor GPU stall backward slicing)**: this paper's own conclusion — "Line-level stall attribution is a crucial capability missing from Omniperf" [paper] — is precisely the capability Leo builds. Read in sequence, ICS 2025 states the tooling gap and SC 2026 fills it. This is the strongest cross-corpus link this cluster produced and it rests on the papers' own text, not on inference about topics.
- **Complementary to `GPU-ISC24-01` (Porting HPC applications to MI300A with unified memory and OpenMP)**: both are AMD-side portability experience, at application and at model granularity respectively.
- **Complementary to the microbenchmarking cluster** (`GPU-IPDPS24-61` Hopper, `GPU-IPDPS26-61` Blackwell B200, `GPU-PPoPP26-02` CuBie): those establish what the hardware can do; this establishes how much of it each programming model reaches.
- **Prior work named by the paper, with venues as it reports them** [paper]: Pennycook et al. (the P∥ metric), Daniel et al., Marowka; Dufek et al. (Kokkos vs SYCL, Milc-Dslash); Rangel et al. (CRK-HACC in SYCL); Brunst et al. (SPEChpc 2021); Kuncham et al. (SYCL vs CUDA on V100); **Deakin et al.** (five models over BabelStream, TeaLeaf, CloverLeaf, Neutral, MiniFMM); Lin et al. (C++17 StdPar vs five models on AMD); Kwack et al.; Harrell et al. (portability with developer productivity). **Cited venue set: P3HPC workshop, SC workshops, IPDPS, CCGrid** — i.e. an SC/IPDPS/workshop citation base, with essentially no ISCA/MICRO/HPCA presence.
- `NO_EXISTING_ANALYSIS`. Not an AI/HPC-import candidate (no ML content).

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO.**

**Stack level of the contribution**: **source language → framework → CUDA/HIP → kernel**. The study's object is the portability *layer* (Kokkos, RAJA, SYCL, OpenMP target, OpenACC) together with the vendor backend it lowers through; its findings are read off at the kernel/PTX-and-GCN level via profilers.

verdict_basis: The measured quantities and every named root cause are GPU-architectural objects that have no CPU counterpart — **registers per thread and spilling**, **occupancy and eligible-warp counts**, **barrier warp stalls**, **threads per block chosen by the compiler**, **in-kernel dynamic shared memory**, and **warp-level shuffle primitives as the correct lowering for a reduction** [paper]. The study's central negative result (directive models lose most on the compute-bound kernel, with 1463 vs 357 static instructions and a 500% rise in L2 cycles) is a statement about GPU register allocation and the kernel-launch boundary. A CPU study of the same libraries would share the metric (P∥ is generic) but none of the mechanisms, and the paper's actionable recommendations — compiler handling of GPU reductions, register-spilling reduction, portable knobs for block size and shared memory — would be empty. Recorded honestly: **the metric is generic and not novel here; the GPU specificity lies entirely in the root-cause analysis**, which is the bulk of the paper.

verdict: `CORE_GPU`

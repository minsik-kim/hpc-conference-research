# GPU-MICRO25-01 — Swift and Trustworthy Large-Scale GPU Simulation with Fine-Grained Error Modeling and Hierarchical Clustering

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `N — profiling, debugging, correctness checking, simulation & performance modelling`
secondary_topics: `sampled simulation methodology; LLM/ML workload characterisation; statistical error bounding`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER_SINGLE_DEEP_PASS — author-hosted PDF (seonjinna.github.io/assets/pdf/MICRO25_stem_root.pdf) read for authors/affiliations/tool names, motivation and the critique of prior kernel-sampling methods, the CLT-based sample-size derivation and KKT multi-cluster formulation, the ROOT recursive clustering rule and its stopping condition, the sampling and weighted-sum reconstruction, the simulator/GPU/benchmark evaluation setup with speedup and error tables, the design-space-exploration and cross-GPU portability results, and the stated limitations. NOT read line-by-line: full equation derivations 1-5, individual figure captions, and the related-work section beyond the named prior methods.`

## 12.1 Bibliographic facts

- Official title: *Swift and Trustworthy Large-Scale GPU Simulation with Fine-Grained Error Modeling and Hierarchical Clustering* [paper].
- Tool names: **STEM** (statistical error modeling) + **ROOT** (the hierarchical clustering framework); the paper is presented as the STEM+ROOT pair [paper].
- Authors: **Euijun Chung** (Georgia Tech, School of Computer Science), **Seonjin Na** (Georgia Tech, SCS), **Sung Ha Kang** (Georgia Tech, **School of Mathematics**), **Hyesoon Kim** (Georgia Tech, SCS) [paper]. The mathematics co-author is worth noting — the contribution is genuinely statistical.
- Venue: MICRO 2025, Session 7B "Tools and Simulators". DOI `10.1145/3725843.3757107` [census].
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Public full text: author-hosted PDF `https://seonjinna.github.io/assets/pdf/MICRO25_stem_root.pdf` [official-web].
- Artifact: `NOT_FOUND_AFTER_SEARCH` (census). `NOT_INSPECTED`.

## 12.2 Core question (one sentence)

Existing GPU sampled-simulation methods choose which kernels to simulate from *static* code signatures (instruction mixes, basic-block vectors, control flow) and therefore cannot bound their own error when the same kernel behaves differently at different invocations — so can sample selection instead be driven by the *measured runtime distribution* of each kernel, with a statistically derived sample size that delivers a user-specified error bound? [paper]

## 12.3 GPU/HPC problem translation

- **Compute.** The unit of work is the kernel invocation; the quantity estimated is total execution cycles.
- **Memory.** The paper's motivating counterexample is memory-hierarchy-driven: identical GEMM kernels vary because of "input sparsity, tensor layout, memory alignment, cache locality" [paper]. Memory behaviour is the *source* of the variance the method exploits, though it is never measured directly.
- **Scheduling / synchronization / communication.** NOT_IN_PAPER. Single-GPU; multi-GPU synchronization and communication kernels are explicitly future work.

## 12.4 Why the problem exists (down to hardware root cause)

- **The cost.** Cycle-level simulators update microarchitectural state every cycle, so "even a 1-second large language model (LLM) inference workload can require several days of simulation" [paper]. The scale problem is now set by LLM workloads: the paper's Huggingface suite averages **11.6 million kernel calls** per workload [paper].
- **The accuracy failure of static signatures.** Prior methods "rely on instruction-level and control-flow-related metrics as kernel signatures" but these "often fail to capture input-dependent characteristics at runtime" [paper]. The concrete mechanism: "even the same GPU kernel … can be invoked repeatedly in a fixed compute graph but show significantly varying performance due to microarchitectural effects."
- **Why this is worse on GPUs than on CPUs.** Modern GPU AI workloads execute a *fixed compute graph* in which the same kernel symbol is launched thousands or millions of times with different tensor shapes, sparsity, and cache residency. Static code metrics are by construction identical across all those launches — the code did not change, only the data and the cache state did. So the very structure that makes GPU AI workloads huge (graph replay of a few kernel symbols) is also what makes static signatures blind `[inference]`; the paper states the phenomenon and the GEMM example but does not frame it as a GPU-graph-replay consequence.
- **The observable that does carry the information.** "The execution time distribution of a kernel exhibits distinct peaks," which the authors read as "multiple performance saturations — each peak reflecting the kernel's operation in a different context" [paper]. Multimodality in the runtime histogram is the signal.

## 12.5 Mathematical / performance model

This is the paper's core, and it is a genuine statistical model rather than a heuristic.

**Foundation — Central Limit Theorem.** "The sample mean X̄ will always follow a normal distribution, regardless of the original distribution of execution times" [paper]. This is what licenses a confidence-interval statement without assuming the runtime distribution is normal — important, since the paper's own motivating observation is that these distributions are multimodal.

**Single-cluster sample size (the paper's Equation 3)** [paper]:

```
m = ceil( ( z_{1-alpha/2} * (sigma/mu) / epsilon )^2 )
```

- `m` — required number of sampled invocations
- `sigma/mu` — the coefficient of variation (CoV) of the kernel's measured execution times
- `epsilon` — the user's error bound (e.g. 5%)
- `z_{1-alpha/2}` — 1.96 for 95% confidence

The structure is the classic sample-size formula, and its consequence is the design's central lever: **required samples scale with the square of the coefficient of variation.** A kernel whose runtime is tight needs almost no samples; a kernel whose runtime is spread needs many. This is exactly the adaptivity that static-signature methods cannot express, because CoV is not visible in the code.

**Multi-cluster allocation (Equation 6).** With several clusters, a **KKT (Karush–Kuhn–Tucker) solver** minimises total simulation time subject to the aggregate error bound `epsilon` [paper]. So the method does not merely bound error — it allocates a *simulation-time budget* across clusters optimally under that bound. This is the "trustworthy" half of the title: the error bound is an input, not an outcome.

**Reconstruction — weighted sum** [paper]: "it computes the total time as the sum of the execution times of the sampled kernels, each multiplied by a weight corresponding to the number of corresponding kernel invocations in the full workload that the sample represents," i.e.

```
t_total = SUM_i ( N_i * Xbar_i )
```

for cluster `i` with population size `N_i` and sample mean `Xbar_i`.

**Sampling discipline.** Samples are drawn **with replacement** to satisfy the i.i.d. assumption the CLT requires [paper]. This is a small detail with real consequence: without-replacement sampling from a finite cluster would violate independence and invalidate the interval.

## 12.6 Data layout and ownership

**Granularity: kernel-level.** "Per-kernel, not intra-kernel" [paper]. Explicitly *not* thread-block or warp granularity — this distinguishes it from TBPoint (thread-block sampling) and is a deliberate scope choice.

| Level | Role in STEM+ROOT |
|---|---|
| instruction / warp / thread block | **not represented**; the method is agnostic to intra-kernel structure |
| kernel invocation | the sampling unit; carries one measured execution time |
| kernel symbol (by name) | the initial grouping key |
| cluster (post-ROOT) | a subset of one symbol's invocations with homogeneous runtime; carries `N_i`, `Xbar_i`, CoV, and an allocated sample count |
| workload | the weighted sum over clusters |
| GPU | one device; multi-GPU is future work |

**ROOT clustering** [paper]:
- **Features clustered:** kernel execution times — distribution shape, standard deviation, mean.
- **Method:** recursive **k-means with k = 2** at each split.
- **Distance metric:** not explicitly named in the paper. UNKNOWN.
- **Depth:** adaptive, not fixed. "ROOT continues splitting clusters until further splits no longer yield meaningful simulation time savings."
- **Stopping rule:** for a cluster `C`, apply k-means to get subclusters; compare total predicted simulation time `tau_old` (before split) against `tau_new` (after). Accept the split iff `tau_old > tau_new`; otherwise stop.

The stopping rule is the elegant part of the design: splitting is judged **by its effect on the objective (total simulation time at fixed error), not by a clustering-quality score.** A split is worth making only if the reduction in within-cluster CoV — and hence in required samples via the squared dependence in Equation 3 — outweighs the cost of having to sample an additional cluster at all. Clustering and budgeting are the same decision.

## 12.7 Pseudo code

`[reconstruction]` of the described pipeline:

```
# 1. lightweight profiling on real hardware (NOT simulation)
times <- nsight_systems_kernel_durations(workload)   # per invocation

# 2. group by kernel symbol
for each kernel name k:
    C_k <- { invocation times of k }

# 3. ROOT: recursive cluster splitting judged by simulation-time savings
def root(C):
    tau_old <- predicted_sim_time([C])               # via Eq.3 sample size for C
    (A, B)  <- kmeans(C, k=2)                        # on execution-time features
    tau_new <- predicted_sim_time([A, B])
    if tau_old > tau_new:
        return root(A) + root(B)
    else:
        return [C]

clusters <- concat( root(C_k) for all k )

# 4. STEM: allocate sample counts under a global error bound
#    single cluster:  m = ceil( (z * CoV / eps)^2 )            # Eq.3
#    many clusters:   solve KKT to minimise SUM_i m_i * cost_i
#                     subject to aggregate error <= eps        # Eq.6
m <- kkt_allocate(clusters, eps, confidence=0.95)

# 5. simulate only the drawn samples
for cluster i:
    S_i <- sample_with_replacement(clusters[i], m[i])   # i.i.d. for CLT
    Xbar_i <- mean( cycle_level_simulate(s) for s in S_i )

# 6. reconstruct
t_total <- SUM_i ( N_i * Xbar_i )
```

Note that step 1 runs on **real hardware with a lightweight profiler**, not in the simulator. That is what makes the profiling overhead reduction possible (12.11) and is also the source of the method's main portability limitation (12.13).

## 12.8 Real implementation

`NOT_INSPECTED` — no artifact repository identified. Named software dependencies [paper]:
- **MacSim** — the cycle-accurate simulator used for evaluation; the authors state compatibility with **AccelSim** and **MGPUSim** as well.
- **NVIDIA Nsight Systems** — the lightweight profiler used to collect per-invocation kernel durations.

No internal symbols were read; none are attributed.

## 12.9 Kernel execution

The method deliberately does not descend below the kernel. Its implicit model of kernel execution is that an invocation's cycle count is a single random draw from a context-dependent distribution, and that the context (tensor shape, sparsity, alignment, inherited cache state) is *not* recoverable from the code but *is* recoverable from the runtime [paper].

The workload scale tells the story [paper]:

| Suite | Workloads | Mean duration | Mean kernel calls |
|---|---|---|---|
| Rodinia (GPGPU) | 13 | 6.46 s | ~1,403 |
| CASIO (ML) | 11 | 7.26 s | ~64,279 |
| Huggingface (LLM/ML) | 6 | 1,835.27 s | **~11.6 million** |

Four orders of magnitude in kernel-call count between traditional GPGPU and LLM workloads. That gap is the paper's reason for existing, and it is why the speedups differ so wildly across suites (12.11).

## 12.10 Memory traffic

Not measured. Memory behaviour enters in three places [paper]:

1. **As the cause of the variance being exploited** — "input sparsity, tensor layout, memory alignment, cache locality" are named as the microarchitectural effects making identical GEMM kernels differ.
2. **As the cache-warmup assumption.** The method "assumes ideal warmup of cache and hardware states," and inter-kernel L2 state may not be accurately modelled in sampled simulation. The authors test this: **flushing L2 between kernels increases error by only 0.07% on CASIO and 0.70% on Rodinia** [paper]. This is a well-designed ablation — it directly bounds the cost of the assumption rather than arguing it away. The result implies inter-kernel L2 reuse is negligible for these workloads, which is plausible for ML graph replay where working sets exceed L2 `[inference]`.
3. **As the reason memory-bound kernels get more samples.** The authors argue that adaptive sampling of variable kernels mitigates cross-hardware risk, because memory-bound kernels are the variable ones and therefore automatically receive more samples [paper]. The CoV-squared rule does this without being told which kernels are memory-bound — a genuinely attractive property.

## 12.11 Why it is faster/slower (decomposed cause)

The speedup decomposes into two independent multiplicative effects, and the suite-by-suite results separate them cleanly [paper]:

| Suite | Method | Speedup | Error |
|---|---|---|---|
| Rodinia | **STEM** | 3.00× | **0.93%** |
| Rodinia | Photon | 2.84× | 2.71% |
| CASIO | **STEM** | 109.60× | **0.36%** |
| CASIO | Photon | **168.61×** | 9.85% |
| Huggingface | **STEM** | **31,719×** | **0.57%** |
| Huggingface | Random (0.1%) | 1,004.97× | 2.40% |

Reading these honestly:

1. **Redundancy exploited.** Speedup tracks how many invocations share a distribution. On Rodinia (~1,403 calls) there is little to exploit: 3.00×. On Huggingface (~11.6 M calls) there is enormous redundancy: 31,719×. The speedup is a property of the workload's kernel-call multiplicity, not of the algorithm's cleverness.
2. **Error control, not speed, is the actual contribution.** **On CASIO, Photon is 1.54× *faster* than STEM (168.61× vs 109.60×) — but at 9.85% error against STEM's 0.36%, a 27× error difference.** STEM trades speed for a bounded error. The paper reports a **27.6–81.9× reduction in error** versus prior methods on CASIO [paper]. Anyone citing the 31,719× figure without the error column has taken the wrong number: the claim is *trustworthiness at comparable speed*, not raw speed.
3. **Profiling overhead is a separate, large win.** STEM reduces profiling overhead by **53.07× to 669.60×** on CASIO versus PKA/Sieve/Photon [paper]. Because STEM needs only kernel *durations* from Nsight Systems, while PKA needs 12 instruction-level metrics, Sieve needs instruction counts, and Photon needs basic-block vectors across all invocations — all of which require heavier instrumentation `[inference]`. This is arguably the most practically important result and is independent of the simulation speedup.

Robustness results [paper]:
- **Design-space exploration:** cache ×2/×0.5 and SM count ×2/×0.5 in MacSim — STEM maintains ~2% error across variants. So a profile collected once supports a microarchitectural sweep.
- **Cross-GPU portability:** using H100 profiles to drive H200 simulation gives **5.46% average error**. Usable but an order of magnitude worse than same-hardware error (0.36–0.93%).

## 12.12 Hardware generation dependence

- Profiling hardware: **NVIDIA RTX 2080, H100, H200** [paper]. Simulator: **MacSim** with modified cache sizes and SM counts.
- The dependence is *asymmetric and unusual*: the method is largely independent of the **simulated** architecture (DSE sweeps hold ~2% error) but dependent on the **profiled** architecture (H100→H200 transfer costs 5.46% error).
- Root cause of that asymmetry: the clustering is derived from execution times measured on real silicon, so the cluster structure encodes that silicon's microarchitecture. "When we perform profiling and sampling on hardware A but run the simulation on hardware B, the sampled kernels from hardware A may fail to capture the workload's runtime behavior on hardware B" [paper]. The authors' mitigation argument — variable (memory-bound) kernels get more samples anyway — is plausible but is an argument, not a measurement, beyond the single H100→H200 datapoint.
- **This is the sharpest methodological contrast with `GPU-HPCA24-41` (GPU Scale-Model Simulation).** STEM+ROOT needs real hardware of roughly the right kind to profile on; Scale-Model Simulation explicitly targets the case where "access to a simulation model of the target system … might not be available" and needs no target hardware at all. They are complementary halves of the same cost problem: STEM reduces *how many kernels* you simulate, Scale-Model reduces *how big a machine* you simulate. In principle they compose; neither paper says so.

## 12.13 Limitations

Stated by the authors [paper]:
1. **Profiling-hardware dependence** — profiles from hardware A may not characterise behaviour on hardware B (5.46% H100→H200).
2. **Cache warmup** — assumes ideal warmup; inter-kernel L2 state may be mismodelled. Quantified at 0.07% (CASIO) / 0.70% (Rodinia) by L2-flush ablation.
3. **Single-GPU only** — multi-device environments with synchronization and communication kernels are future work.
4. **Trace generation** — for trace-based simulators, tracing only sampled kernels helps, but some tools may still need a full-workload trace.

Practical constraints in the evaluation [paper]:
5. Full cycle-level simulation was **infeasible** for large Huggingface workloads, so **machine profiles (real hardware cycle counts) were used as the reference** for computing speedup and error. The 31,719× / 0.57% Huggingface result is therefore validated against measured hardware time, not against a full simulation — a reasonable substitution, but it is not the same experiment as the Rodinia one.
6. Full-simulation experiments on Rodinia used **reduced input sizes**.

Observed by this analysis:
7. **No artifact**, so neither ROOT's clustering nor the KKT allocation is reproducible.
8. **The k-means distance metric is unspecified.** UNKNOWN. For clustering over "distribution shape, standard deviation, mean" the metric choice is not incidental.
9. **Sampling with replacement** satisfies the CLT but means a single unusually fast or slow invocation can be drawn repeatedly into a small sample; no discussion of variance inflation from this.
10. The method estimates a **mean**. It says nothing about tail behaviour, so it cannot answer questions about worst-case kernel latency — relevant for any latency-SLO reasoning about inference.

## 12.14 Relation to prior corpus

- **Prior corpus:** `NO_EXISTING_ANALYSIS`. Repository-wide grep for "Hierarchical Clustering" returns only `domains/gpu_systems/census/MICRO_2025.md` (a census row).
- **Competing prior methods, all named and critiqued in the paper** [paper]:
  - **PKA** (Principal Kernel Analysis) — 12 instruction-level metrics; selects the first chronological kernel from each cluster.
  - **Sieve** — instruction count as the feature vector; stratifies into three variation groups; first-chronological selection.
  - **Photon** — GPU Basic Block Vectors; 95% similarity threshold; compares BBVs across all invocations. The strongest baseline, and faster than STEM on CASIO at 27× the error.
  - **TBPoint** — microarchitecture-independent metrics, hierarchical clustering, samples the kernel closest to the cluster centre. The closest structural relative (it also clusters hierarchically) but over static metrics rather than runtimes.
  - **LoopPoint** — cited as the multi-threaded CPU extension.
  The consistent pattern in the critique: every prior method selects a *representative* invocation (first-chronological or nearest-centroid) and therefore has no sample size and no error bound. STEM replaces representative selection with random sampling plus an interval.
- **Complementary, same problem, orthogonal axis:** `GPU-HPCA24-41` (*GPU Scale-Model Simulation*, HPCA 2024) — see 12.12. Also *GRASP: Fine-grained and Adaptive Sampled Simulation for GPU Performance Modeling* (ICS 2026) and *HyFiSS* (MICRO 2024), both in this cluster's verdict-only list, occupy the sampled/hybrid-fidelity simulation space directly.
- **Complementary, measurement rather than simulation:** `GPU-SC26-41` (LEO) and *GCStack+GCScaler* (ISCA 2025) address GPU performance analysis cost from the hardware-measurement and analytical-model sides. See `_LEDGER_profiling_reliability.md`.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**Answer: NO — with a caveat that the statistical machinery itself is generic.**

verdict_basis: Equations 3 and 6 (CLT sample sizing, KKT allocation) are domain-neutral statistics, and LoopPoint shows the sampled-simulation problem exists on CPUs too. What makes this CORE_GPU is that the *phenomenon being modelled* is specific to GPU execution: the sampling unit is the **GPU kernel invocation**, and the paper's whole premise is that GPU AI workloads replay a fixed compute graph in which one kernel symbol is launched up to 11.6 million times with identical code but different tensor shape, sparsity, alignment and inherited L2 state — so static code signatures (instruction mix, basic-block vectors) are provably constant across invocations that differ in cycles. The baselines it displaces (PKA, Sieve, Photon, TBPoint) are all GPU-kernel samplers, the cache-warmup ablation is over GPU L2 between kernel launches, the evaluation runs in GPU simulators (MacSim/AccelSim/MGPUSim), and the stated future work — synchronization and communication kernels in multi-GPU settings — is GPU-specific. On a CPU there is no kernel-launch granularity to sample at and no graph-replay redundancy to exploit.

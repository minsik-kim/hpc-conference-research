# PPoPP 2026 — GPU Census

census_status: `COMPLETE_CENSUS`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | **51** |
| counted items excluded from population | **posters: 0** — PPoPP 2026 has **no poster track and no poster session** (verified against the track list and the full program); **workshops/tutorials: 5** co-located events (CACHP, MLIR, ScaleDNN, DiffPP, DDRP); artifact-evaluation track (separate track); plenary keynotes of the joint HPCA/CGO/PPoPP/CC 2026 meeting |
| population source (primary) | https://ppopp26.sigplan.org/track/PPoPP-2026-papers — 51 accepted-paper entries, all labelled "Main Conference" — `official-program` |
| population source (corroborating) | (a) https://www.conference-publishing.com/toc/PPOPP26/noabs — official proceedings ToC of the *31st ACM SIGPLAN Symposium*, 14 research sections, per-paper DOIs — `publisher-proceedings`; (b) per-item official detail pages `https://ppopp26.sigplan.org/details/PPoPP-2026-papers/<N>/x` for N=1..51 map **one-to-one and in order** onto the DOI suffixes `10.1145/3774934.3786411` … `10.1145/3774934.3786461`, a **contiguous block of exactly 51** with no gaps — `official-program` + `publisher-proceedings`; (c) https://ppopp26.sigplan.org/program/program-PPoPP-2026/ — 11 four-paper sessions on Mon 2 / Tue 3 Feb (44 papers), remainder in later proceedings sections |
| source class | `official-program` (primary, corroborating b,c); `publisher-proceedings` (corroborating a,b) |
| enumeration completeness | `EXACT` |
| paper-type mixing notes | Every entry on the 2026 track page carries the "Main Conference" designation; no `POSTER:` prefix appears on any of the 51 detail pages (contrast PPoPP 2025, where 11 posters were interleaved into the track page). The proceedings ToC contains no "Posters" / "Extended Abstracts" section in the portion that could be read, and the program contains no poster event on any day. The DOI block being exactly 51 long and gap-free rules out unlisted additional research papers in this proceedings. |

### 1.1 Population evidence notes

- Source statement: the accepted-papers track page enumerates 51 titles.
- Source statement: DOI suffixes recovered from detail pages and the proceedings ToC cover every integer from `3786411` to `3786461` inclusive — 51 values, no gaps, no values outside the range. Three of the 51 DOIs were recovered by title search rather than detail-page read: `…3786427` and `…3786453` (the two remaining numerical-algebra papers, of which *A Distributed Matrix-Block-Vector Multiplication* is confirmed as `…3786453`) and `…3786456` (*Characterizing Matrix Multiplication Units*, confirmed via its ACM PDF URL).
- Source statement: 11 program sessions × 4 papers = 44; the proceedings adds a section "Optimizing Transformers" (3 papers) plus further numerical-algebra sections (4 papers) = 51.
- Inference: three agreeing enumerations, one of them a contiguous publisher DOI block ⇒ EXACT.
- **No official acceptance-rate or submission-count statement was found.** The proceedings frontmatter ("Welcome from the Chairs") could not be read — the ToC page truncates before/within it and `dl.acm.org` returns 403. csconfstats lists "2026: accepted 51, submissions N/A", consistent with 51 but adding no rate. Recorded as `NOT_FOUND_AFTER_SEARCH`.

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population (all 51 papers;
abstracts read via official detail pages), not over the seed list. Keyword hits
were used only to order review, never to decide relevance. All DOIs below are
under the prefix `10.1145/3774934.`.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|
| 1 | DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs | Yuyao Niu et al. | Scheduling and Load Balancing | 3786457 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/47/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title; GPU block-level work stealing |
| 2 | PRISM: An Efficient GPU-Based Lossy Compression Framework for Progressive Data Retrieval with Multi-Level Interpolation | Bing Lu et al. (Best Paper Nominee) | GPU and Heterogeneous Computing | 3786438 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/28/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU-Based" in title |
| 3 | Root-Down Exposure for Maximal Clique Enumeration on GPUs | Zhe Pan, Peng Qu, Youhui Zhang | GPU and Heterogeneous Computing | 3786449 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/39/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title |
| 4 | ROME: Maximizing GPU Efficiency for All-Pairs Shortest Path via Taming Fine-Grained Irregularities | Weile Luo et al. | GPU and Heterogeneous Computing | 3786461 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/51/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU Efficiency" in title; GPU irregularity mitigation |
| 5 | SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping | Qiqi Gu, Chenpeng Wu, Heng Shi, Jianguo Yao | Stencil and Sparse Matrix Computation | 3786414 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/4/x | https://arxiv.org/abs/2506.22035 (v3 carries the SPIDER title; v1/v2 titled "SPTCStencil") | NOT_FOUND_AFTER_SEARCH | Abstract names Tensor Cores, Sparse Tensor Cores (SpTCs), cuDNN |
| 6 | Exploiting Efficient Mapping and Pipelined Execution for Accelerating SpMV on Tensor Cores | Kaige Zhang et al. | Stencil and Sparse Matrix Computation | 3786441 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/31/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on Tensor Cores" in title; GPU tensor-core SpMV |
| 7 | VDHA: Vector-Driven Hash Aggregation for Sparse Matrix-Sparse Vector Multiplication on GPUs | Yuchen Li, Zhe Pan, Peng Qu, Youhui Zhang | Stencil and Sparse Matrix Computation | 3786447 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/37/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title |
| 8 | RoMeo: Mitigating Dual-dimensional Outliers with Rotated Mixed Precision Quantization | Qihao Zhang et al. | Mixed Precision and Quantization | 3786419 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/9/x | NOT_FOUND_AFTER_SEARCH | https://github.com/thu-pacman/RoMeo | Title has no GPU term; abstract names GPUs |
| 9 | High-Throughput Non-Uniformly Quantized 3-bit LLM Inference | YuAng Chen, Wenqi Zeng, Jeffrey Xu Yu | Mixed Precision and Quantization | 3786423 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/13/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names **NVIDIA L40 GPUs, CUDA, Tensor Cores** |
| 10 | HierCut: Enabling 16-bit Format Mixed Precision for Molecular Dynamics through Hierarchical Cutoff | zeyu song et al. (Best Artifact Award) | Mixed Precision and Quantization | 3786433 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/23/x | NOT_FOUND_AFTER_SEARCH | https://zenodo.org/records/17958414 | Title has no GPU term; abstract names **NVIDIA A100 GPUs** and LAMMPS/KOKKOS multi-GPU scaling |
| 11 | Scaling GPU-to-CPU Migration for Efficient Distributed Execution on CPU Clusters | Ruobing Han, Hyesoon Kim | Cluster and Cloud Computing | 3786435 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/25/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "GPU-to-CPU Migration" in title; GPU (CUDA) program semantics are the source model being migrated |
| 12 | Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters | Yida Li et al. (Best Paper Nominee) | Cluster and Cloud Computing | 3786442 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/32/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPU Clusters" in title |
| 13 | COCCL: A Collective Communication Library Supporting Easy Integration and Configuration of Customized Compression for Scalable LLM Training | Xingchen Liu et al. | Distributed Training | 3786432 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/22/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract discusses **GPU clusters and NCCL** — a GPU collective-communication library |
| 14 | Elastor: Elastic and Efficient Model Partitioning and Checkpointing for Fault-Tolerant Distributed Training | Xuanyu Wang et al. | Distributed Training | 3786445 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/35/x | NOT_FOUND_AFTER_SEARCH | https://github.com/PKU-DAIR/Hetu | Title has no GPU term; abstract discusses GPU availability and multi-GPU clusters |
| 15 | HelixPipe: Efficient Distributed Training of Long Sequence Transformers with Attention Parallel Pipeline Parallelism | Geng Zhang et al. | Distributed Training | 3786417 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/7/x | NOT_FOUND_AFTER_SEARCH | https://github.com/zxgx/Megatron-LM | Title has no GPU term; abstract names **H20 GPUs** |
| 16 | CCL-D: A High-Precision Diagnostic System for Slow and Hang Anomalies in Large-Scale Model Training | Yida Gu et al. (Best Paper Nominee) | Distributed Training | 3786429 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/19/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; abstract names a **4,000-GPU cluster** and "faulty GPU rank" — GPU collective-comm fault localization |
| 17 | Pipelonk: Accelerating End-to-End Zero-Knowledge Proof Generation on GPUs for PLONK-Based Protocols | Zhiyuan Zhang et al. | Parallel Algorithms | 3786448 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/38/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPUs" in title |
| 18 | ParDiff: Efficiently Parallelizing Reverse-Mode Automatic Differentiation with Direct Indexing | Shuhong Huang et al. | Parallel Algorithms | 3786418 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/8/x | NOT_FOUND_AFTER_SEARCH | https://github.com/roastduck/FreeTensor | Title has no GPU term; abstract names "multi-core CPUs and GPUs" — GPU centrality PARTIAL (see §6) |
| 19 | TAC: Cache-Based System for Accelerating Billion-Scale GNN Training on Multi-GPU Platform | Zhiqiang Liang et al. | Graphs and Graph Neural Networks | 3786460 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/50/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "Multi-GPU Platform" in title; GPU-memory cache |
| 20 | FlashAttention-T: Towards Fully Tensorized Attention by Exploiting Tensor-Vector Parallelism | Jianxing Xu et al. | Optimizing Transformers | 3786425 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/15/x | NOT_FOUND_AFTER_SEARCH | https://zenodo.org/records/17673796 | Title has no GPU term; abstract names **NVIDIA Ampere (A100, AGX Orin), Hopper (H100), Tensor Cores and CUDA cores** — tensor-core/CUDA-core co-scheduling |
| 21 | Accelerating Sparse Transformer Inference on GPU | Wenhao Dai et al. | Optimizing Transformers | 3786434 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/24/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPU" in title |
| 22 | MetaAttention: A Unified and Performant Attention Framework Across Hardware Backends | Feiyang Chen et al. | Optimizing Transformers | 3786444 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/34/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | Title has no GPU term; multi-backend attention kernel framework. **Abstract names no device** — listed as a candidate on title/venue-section grounds only; GPU centrality UNVERIFIED (see §6) |
| 23 | Towards Singular Value Decomposition for Rank-Deficient Matrices: An Efficient and Accurate Algorithm on GPU Architectures | Lu Shi, WeiWei Xu, Shaoshuai Zhang | UNKNOWN (proceedings section not readable) | 3786427 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/17/x | NOT_FOUND_AFTER_SEARCH | NOT_FOUND_AFTER_SEARCH | "on GPU Architectures" in title; abstract names GPU and **cuSOLVER** |
| 24 | Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing | Yuechen Lu, Hongwei Zeng, Marc Casas, Weifeng Liu | UNKNOWN (proceedings section not readable) | 3786456 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/46/x | https://www.ssslab.cn/assets/papers/2026-lu-Cubie.pdf (author-hosted PDF); ACM PDF at https://dl.acm.org/doi/pdf/10.1145/3774934.3786456 | https://zenodo.org/records/17725527 | Matrix-multiplication-unit characterization study — tensor/matrix-core units are the object of study |
| 25 | ChituDiffusion: A Data-Characteristic-Aware Serving System for Diffusion Models | Chengzhang Wu et al. | ML Inference | 3786424 | https://ppopp26.sigplan.org/details/PPoPP-2026-papers/14/x | NOT_FOUND_AFTER_SEARCH | https://github.com/thu-pacman/chitu/tree/Diffusion | Title has no GPU term; abstract names **A100 and H100** |

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|
| PANA: A Fine-Grained Runtime-Adaptive Load Balancing for Parallel SpMV on Multicore CPUs | Keywords: SpMV, load balancing. Title states **Multicore CPUs** explicitly. |
| ASM-SpMM: Unleashing the Potential of Arm SME for Sparse Matrix Multiplication Acceleration | Keywords: SpMM, prefetch. Abstract targets **Arm SME (Armv9 Scalable Matrix Extension)** — a CPU matrix extension, not a GPU. |
| Faster and Cheaper: Pushing the Sequence Alignment Throughput with Commercial CPUs | Keyword: throughput/kernel. Abstract states **commercial CPUs**. Code: github.com/zzhofict/BWA-FastAlign |
| PIM-zd-tree: A Fast Space-Partitioning Index Leveraging Processing-in-Memory | Keyword: memory. Abstract targets **PIM** (processing-in-memory) hardware, not GPUs. |
| A Diagonal Block Memory-Aware Polynomial Preconditioner for Linear and Eigenvalue Solvers | Keywords: memory, sparse, solver. Abstract evaluates on **"x86 and Arm HPC platforms"**; no GPU named. |
| A Distributed Matrix-Block-Vector Multiplication in Presence of System Performance Variability | Keywords: matrix-vector, distributed. Abstract names no hardware; distributed-variability scheduling. |
| Dynamic Detection of Inefficient Data Mapping Patterns in Heterogeneous OpenMP Applications | Keywords: profiling, memory, compiler. Abstract speaks of "accelerators" and OMPT tracing generically; **no GPU, CUDA or vendor device is named**. Likely OpenMP-offload-to-GPU work — see §6. |
| Cacheman: A Comprehensive Last-Level Cache Management System for Multi-tenant Clouds | Keywords: cache, memory. Abstract names no GPU; host LLC partitioning. |
| zBuffer: Zero-Copy and Metadata-Free Serialization for Fast RPC with Scatter-Gather Reflection | Keywords: RDMA-adjacent, zero-copy, memory. Abstract names no hardware; RPC serialization. |
| Laser: Unlocking Layer-Level Scheduling for Efficient Multi-SLO LLM Serving | Keyword: scheduling/kernel. Abstract names no device. GPU centrality unverified — see §6. |
| MixFusion: A Patch-Level Parallel Serving System for Mixed-Resolution Diffusion Models | Keyword: parallel serving. Abstract names no device (code: github.com/desenSunUBW/mixfusion). GPU centrality unverified — see §6. |
| JanusQuant: Accurate and Efficient 2-bit KV Cache Quantization for Long-Context Inference | Keywords: memory, quantization. Abstract names no device. GPU centrality unverified — see §6. |
| BEEMS: Boosting Machine Vision Efficiency via Computation Graph-Based Memory Smoothing | Keywords: memory, compiler. Abstract names no device; described as compilation-level memory optimization. GPU centrality unverified — see §6. |
| ElasGNN: An Elastic Training Framework for Distributed GNN Training | Keyword: distributed training. Abstract names no device. GPU centrality unverified — see §6. |
| APERTURE: Algorithm-System Co-optimization for Temporal Graph Network Inference | Keywords: memory, parallelism. Abstract names no device. GPU centrality unverified — see §6. |
| DTMiner: A Data-Centric System for Efficient Temporal Motif Mining | Keyword: mining/parallel. Abstract names no device. GPU centrality unverified — see §6. |
| Fixing Non-blocking Data Structures for Better Compatibility with Memory Reclamation Schemes | Keyword: memory. CPU concurrent data structures. |
| Multiverse: Transactional Memory with Dynamic Multiversioning | Keyword: memory. CPU transactional memory. |
| Binary Compatible Critical Section Delegation | Keyword: delegation/sync. CPU; no hardware accelerator. |
| Hapax Locks: Scalable Value-Based Mutual Exclusion | — CPU locks. |
| UFO Trees: Practical and Provably-Efficient Parallel Batch-Dynamic Trees | — CPU parallel algorithms. |
| Sharded Elimination and Combining for Highly-Efficient Concurrent Stacks | — CPU concurrent data structures. |
| Concurrent Balanced Augmented Trees | — CPU concurrent data structures. |
| Parallel Dynamic Spatial Indexes | — Abstract names no hardware; CPU parallel indexes. |
| Rethinking Thread Scheduling under Oversubscription | Keyword: scheduling. CPU user-space runtime scheduling. |
| Waste-Efficient Work Stealing | Keyword: scheduling/stealing. CPU work stealing. |

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|
| RoMeo: Mitigating Dual-dimensional Outliers with Rotated Mixed Precision Quantization | Abstract names GPUs |
| High-Throughput Non-Uniformly Quantized 3-bit LLM Inference | Abstract names NVIDIA L40 GPUs, CUDA, Tensor Cores |
| HierCut: Enabling 16-bit Format Mixed Precision for Molecular Dynamics through Hierarchical Cutoff | Abstract names NVIDIA A100 GPUs; multi-GPU LAMMPS/KOKKOS scaling |
| COCCL: A Collective Communication Library … for Scalable LLM Training | Abstract discusses GPU clusters and NCCL |
| Elastor: Elastic and Efficient Model Partitioning and Checkpointing … | Abstract discusses GPU availability and multi-GPU clusters |
| HelixPipe: Efficient Distributed Training of Long Sequence Transformers … | Abstract names H20 GPUs |
| CCL-D: A High-Precision Diagnostic System for Slow and Hang Anomalies … | Abstract names a 4,000-GPU cluster and "faulty GPU rank" |
| ParDiff: Efficiently Parallelizing Reverse-Mode Automatic Differentiation with Direct Indexing | Abstract names "multi-core CPUs and GPUs" (PARTIAL) |
| FlashAttention-T: Towards Fully Tensorized Attention by Exploiting Tensor-Vector Parallelism | Abstract names NVIDIA A100 / AGX Orin / H100, Tensor Cores and CUDA cores |
| ChituDiffusion: A Data-Characteristic-Aware Serving System for Diffusion Models | Abstract names A100 and H100 |
| Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing | Matrix/tensor-core units are the object of the characterization study |
| MetaAttention: A Unified and Performant Attention Framework Across Hardware Backends | Included on section/title grounds; abstract names no device (UNVERIFIED — §6) |

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|
| SPIDER | `TITLE_CORRECTED_TO:` **SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping** — `CONFIRMED_IN_POPULATION` (DOI …3786414) |
| a paper characterizing matrix multiplication units across NVIDIA/AMD/Intel accelerators | `TITLE_CORRECTED_TO:` **Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing** — `CONFIRMED_IN_POPULATION` (DOI …3786456). *Note: the NVIDIA/AMD/Intel vendor coverage stated in the seed was NOT verified from any source read here; only the title, authors and DOI are confirmed.* |
| PRISM | `TITLE_CORRECTED_TO:` **PRISM: An Efficient GPU-Based Lossy Compression Framework for Progressive Data Retrieval with Multi-Level Interpolation** — `CONFIRMED_IN_POPULATION` (Best Paper Nominee; DOI …3786438) |
| ROME | `TITLE_CORRECTED_TO:` **ROME: Maximizing GPU Efficiency for All-Pairs Shortest Path via Taming Fine-Grained Irregularities** — `CONFIRMED_IN_POPULATION` (DOI …3786461) |
| VDHA | `TITLE_CORRECTED_TO:` **VDHA: Vector-Driven Hash Aggregation for Sparse Matrix-Sparse Vector Multiplication on GPUs** — `CONFIRMED_IN_POPULATION` (DOI …3786447) |
| a paper about scaling GPU-to-CPU migration | `TITLE_CORRECTED_TO:` **Scaling GPU-to-CPU Migration for Efficient Distributed Execution on CPU Clusters** — `CONFIRMED_IN_POPULATION` (DOI …3786435) |
| DiggerBees | `TITLE_CORRECTED_TO:` **DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs** — `CONFIRMED_IN_POPULATION` (DOI …3786457) |
| a paper with "Trojan Horse" and GPU clusters in the title | `TITLE_CORRECTED_TO:` **Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters** — `CONFIRMED_IN_POPULATION` (Best Paper Nominee; DOI …3786442) |

All 8 PPoPP 2026 seeds are present in the main-conference population. None resolved to `NOT_IN_MAIN_POPULATION` or `NOT_FOUND`.

## 6. Unresolved / blocked items

- **No official acceptance rate / submission count.** The proceedings frontmatter could not be read (ToC page truncates; `dl.acm.org` 403). Recorded `NOT_FOUND_AFTER_SEARCH`.
- **Proceedings section UNKNOWN for two papers**: *Towards Singular Value Decomposition for Rank-Deficient Matrices* (…3786427) and *Characterizing Matrix Multiplication Units* (…3786456), plus the two §3 numerical papers (…3786446, …3786453). The `conference-publishing.com/toc/PPOPP26/noabs` page truncates after "Optimizing Transformers", so the final 1–2 section headings (which the ToC states bring the total to 14 sections) were never rendered. The program page likewise truncated before Wed 4 Feb. Sessions not inferred.
- **GPU centrality UNVERIFIED for 7 ML/graph-systems papers** whose official abstracts name no device: *Laser*, *MixFusion*, *JanusQuant*, *BEEMS*, *ElasGNN*, *APERTURE*, *DTMiner*. These are placed in §3 rather than promoted on assumption; each should be re-screened against its full text before a verdict, since several are very likely GPU-resident systems. *MetaAttention* is the mirror case — placed in §2 on title/section grounds with the same caveat.
- **GPU centrality PARTIAL**: *ParDiff* (abstract names "multi-core CPUs and GPUs"); *Dynamic Detection of Inefficient Data Mapping Patterns in Heterogeneous OpenMP Applications* (accelerators named only generically — placed in §3, likely OpenMP GPU offload).
- **Public full texts**: only SPIDER (arXiv 2506.22035) and *Characterizing Matrix Multiplication Units* (author-hosted PDF) were found. arXiv's search UI is robots-disallowed and `export.arxiv.org` returns 403, so only indexed web search was available; most 2026 papers have no preprint indexed as of 2026-09-18.
- Artifact URLs recorded were those exposed on official detail pages or found via search (GitHub / Zenodo); the PPoPP 2026 artifact-evaluation track page does not publish a per-paper artifact index, so absence here is `NOT_FOUND_AFTER_SEARCH`, not evidence of no artifact.

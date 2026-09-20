# GPU-IPDPS26-02 — The Big Send-off: Scalable and Performant Collectives for Deep Learning

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `M GPU-aware / GPU-initiated communication & collectives`
secondary_topics: `L Multi-GPU interconnect & data paths`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `Author-hosted PDF (www.cs.umd.edu/~bhatele/pubs/pdf/2026/ipdps2026a.pdf) read across motivation/library-deficiency characterization, the PCCL two-level design and both inter-node algorithms, the SVM dispatcher, evaluation setup on Frontier and Perlmutter, microbenchmark and end-to-end results, limitations and related work. Venue string not printed in the PDF header as read.`

## 12.1 Bibliographic facts
- Title: *The Big Send-off: Scalable and Performant Collectives for Deep Learning*; library name **PCCL**. `[paper]`
- Authors `[paper]` `[census]`: Siddharth Singh, Keshav Pradeep, Mahua Singh, Cunyang Wei, Abhinav Bhatele. Affiliations per the PDF: University of Maryland (Singh, Pradeep, Wei, Bhatele); Indian Institute of Technology Guwahati (M. Singh).
- Venue: IPDPS 2026, per census `IPDPS_2026.md` row 6 `[census]`. DOI `UNKNOWN`. The PDF as read does not print the venue string — recorded from census, not from the paper.
- **Earlier preprint of the same work under a different title**: *The Big Send-off: High Performance Collectives on GPU-based Supercomputers*, arXiv:2504.18658 `[census]`. Recorded; the retitled IPDPS 2026 version is the archival one.
- Publication type: `ARCHIVAL_MAIN_PAPER`; read source is an author-hosted copy.

## 12.2 Core question (one sentence)
Why do NCCL, RCCL and Cray-MPICH all scale poorly for the moderate-to-large message sizes (tens to hundreds of MB) that dominate distributed LLM training, and can a thin hierarchical layer over them fix it at thousands of GPUs? `[paper]`

## 12.3 GPU/HPC problem translation
- **Communication**: the contribution — all-gather, reduce-scatter and all-reduce at 2,048 GPUs/GCDs.
- **Compute**: reduction arithmetic is moved onto the GPU as custom CUDA/HIP kernels, because Cray-MPICH offloads reductions to the CPU.
- **Memory**: a device-local transpose/shuffle kernel is the final step of the hierarchical decomposition.
- **Scheduling**: an SVM-based dispatcher selects a backend per (GPU count, message size) at runtime.
- **Synchronization**: unchanged — collective orchestration remains synchronous and host-driven.

## 12.4 Why the problem exists
The paper's per-library diagnosis `[paper]`:
1. **Cray-MPICH underutilizes the NICs and offloads reductions to the CPU** rather than the GPU — so the reduce path is bounded by the wrong processor and the multi-NIC bandwidth is left unused.
2. **NCCL and RCCL rely solely on ring algorithms** for all-gather and reduce-scatter, so latency scales *linearly* with process count. At 2,048 endpoints that linear term dominates even for large messages.
3. **Consequently "all libraries struggle with efficiency and scalability in regimes of moderate message sizes (tens of MBs) and large GPU counts"**, and "none of the libraries are able to achieve" flat scaling curves.
4. **RCCL is additionally unreliable at scale**, forcing fallback to Cray-MPICH — a robustness, not just performance, root cause.

The root cause is therefore *algorithmic diversity*, not fabric capability: the hardware bandwidth exists but no library's algorithm set can reach it at that endpoint count.

## 12.5 Mathematical / performance model
`NOT_IN_PAPER` as a closed-form model. The argument is asymptotic-qualitative — ring gives latency linear in process count, recursive doubling/halving gives logarithmic latency — plus empirical curves. No α–β fit or explicit cost expressions were recovered from the read text; recorded `UNKNOWN` rather than reconstructed.
The one quantified predictive component is the **SVM dispatcher, at 75–95.4% accuracy on unseen test data** `[paper]`.

## 12.6 Data layout and ownership
- **GPU/GCD**: one rank per GPU (Perlmutter) or per GCD (Frontier, 8 GCDs per node).
- **node**: intra-node phase is delegated to the vendor library (NCCL or RCCL) over NVLink (A100) or Infinity Fabric (MI250X).
- **cluster**: inter-node phase uses custom MPI point-to-point, in one of two algorithms — `PCCL_ring` (ring, with GPU-offloaded reductions) or `PCCL_rec` (recursive doubling/halving, log-latency).
- **NIC binding**: on Frontier the design explicitly maps GCDs to NICs — 4 Slingshot-11 Cassini NICs per node, 2 GCDs per NIC.
- **final step**: a device-local transpose/shuffle kernel reorders data after the two-level decomposition.
- thread/warp-level ownership: `NOT_IN_PAPER`.

## 12.7 Pseudo code
Reconstructed `[reconstruction]` from the paper's description; names `PCCL_ring` / `PCCL_rec` are the paper's own `[paper]`:
```
pccl_allgather(buf, n, comm):
    backend = svm_dispatch(num_gpus, message_size)   # {cray-mpich, nccl, rccl, PCCL_ring, PCCL_rec}
    if backend in {cray-mpich, nccl, rccl}: return vendor_call(...)
    # two-level hierarchical path
    inter_node_phase  = PCCL_ring or PCCL_rec        # custom MPI point-to-point
    intra_node_phase  = nccl/rccl native API         # vendor library over NVLink / Infinity Fabric
    reductions        = custom GPU kernel             # never on the CPU
    device_local_transpose_shuffle_kernel(buf)        # final reorder
```
Python bindings are exposed via **Pybind11** for framework integration. `[paper]`

## 12.8 Real implementation
No artifact repository was established — census records `NOT_FOUND_AFTER_SEARCH`. `NOT_INSPECTED`. **No source symbols are asserted.** `PCCL_ring`, `PCCL_rec` and Pybind11 are named in the paper text. `[paper]`

Software stack at evaluation time `[paper]`:
- Frontier: ROCm 6.4.1, RCCL 2.22.3, Cray-MPICH 8.1.32
- Perlmutter: CUDA 12.9, NCCL 2.27.3, Cray-MPICH 8.1.30

## 12.9 Kernel execution
- **kernel**: two GPU kernel roles are named — the reduction kernel (replacing Cray-MPICH's CPU reduction) and the device-local transpose/shuffle kernel.
- **thread block / warp / instruction**: `NOT_IN_PAPER`.

## 12.10 Memory traffic
- The two-level decomposition means each byte crosses the intra-node fabric (NVLink or Infinity Fabric) and the inter-node fabric (Slingshot-11) once per phase, plus one device-local transpose pass in HBM.
- Because reductions run on the GPU, reduction operands stay in HBM/GPU caches rather than crossing PCIe to host memory — this is the specific traffic Cray-MPICH's CPU offload incurs and PCCL avoids. `[paper]` + `[inference]` on the PCIe implication.
- Register/shared/L1/L2 decomposition: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)
1. **The latency term's asymptotics change**: substituting recursive doubling/halving for ring on the inter-node phase turns a term linear in endpoint count into a logarithmic one. At 2,048 endpoints this is the dominant cause, and it explains why the gains are largest exactly where ring is worst.
2. **Reductions move to the GPU**, removing Cray-MPICH's CPU reduction.
3. **NICs are used deliberately**, via explicit GCD→NIC mapping (2 GCDs per NIC on Frontier).
4. **The right backend is chosen per regime** by the SVM dispatcher, so the library does not pay a wrong-algorithm penalty.
5. **Where it does not help** `[paper]`: all-reduce on Perlmutter gains only ~1.3× because NCCL already uses log-latency tree algorithms for all-reduce — i.e. the improvement is specific to the collectives where the vendor offers only ring.

Numbers with qualifiers `[paper]` — note the asymmetry between Frontier/RCCL and Perlmutter/NCCL is itself the finding:
- **All-gather, 256–512 MB per GPU**: up to **33× vs RCCL on Frontier at 2,048 MI250X GCDs**; up to **5.7× vs NCCL on Perlmutter at 2,048 A100s**.
- **Reduce-scatter, 256–512 MB per GPU**: up to **168× vs RCCL on Frontier at 2,048 GCDs**; up to **4.2× vs NCCL on Perlmutter at 2,048 GPUs**.
- **All-reduce, 64–128 MB per GPU**: up to **5.8× vs RCCL (Frontier, 2,048 GCDs)**; ~**1.3× vs NCCL (Perlmutter, 2,048 GPUs)**.
- **End-to-end**: DeepSpeed ZeRO-3 up to **4.9× vs RCCL** and PyTorch DDP up to **2.4× vs RCCL**, both on Frontier at 2,048 GCDs.
- The 168× and 33× figures are against **RCCL specifically** and must never be restated as speedups over "NCCL" or over "collective libraries" generally.

## 12.12 Hardware generation dependence
- Evaluated on two fabrics, both **Slingshot-11 Dragonfly**: Frontier (AMD MI250X, 8 GCDs/node, Infinity Fabric intra-node, 4 Cassini NICs/node, 2 GCDs per NIC) and Perlmutter (NVIDIA A100, 4 GPUs/node, NVLink intra-node, Slingshot-11).
- **The hierarchical design is coupled to a 4-NIC-per-node layout**; the authors flag that generalization to other NIC-per-node counts is not addressed.
- **Only Slingshot-11 was tested**; InfiniBand behaviour is unexplored — a notable gap given that `GPU-SC24-01` showed the MPI-vs-NCCL ordering differs between Slingshot and InfiniBand HDR.

## 12.13 Limitations
Author-stated and read-established `[paper]`:
1. **Gains against NCCL are far smaller than against RCCL**; all-reduce shows minimal benefit because NCCL already has log-latency trees.
2. **NIC-topology coupling**: explicit GCD→NIC mapping; non-4-NIC-per-node architectures not addressed.
3. **Dispatcher can mispredict**: 75–95.4% accuracy, so a wrong backend can be selected.
4. **Only Slingshot-11 tested**; InfiniBand unexplored.
5. **Optimized for 16 MB–1 GB**; behaviour below 16 MB, and interaction with compression, unclear.
6. **Only ring and recursive doubling/halving** — no topology-aware synthesized algorithms.
7. **Requires a reliable MPI**; RCCL's failures at scale necessitate a Cray-MPICH fallback.

## 12.14 Relation to prior corpus
- No prior in-repo analysis. `[repo-grep]` `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` applies.
- **Directly evaluates and contradicts HiCCL** (IPDPS 2025, verdict-only in this cluster's ledger): the paper states HiCCL "achieves gains at smaller node counts but falls below vendor libraries at larger node counts", positioning PCCL as the large-scale-regime answer. This is a concrete cross-paper claim to carry forward. `[paper]`
- **Complementary / contrasting** to `GPU-IPDPS26-01` (NIMBLE): same venue and year, both target the gap between available and achieved GPU-cluster bandwidth; NIMBLE re-plans *paths* at execution time on NVLink-4 + NDR400, PCCL re-plans *algorithms* hierarchically on Slingshot-11.
- **Confirms and extends `GPU-SC24-01`**: that paper found NCCL/RCCL alltoall benchmarks stalling at 512+ GPUs and RCCL underperforming GPU-aware MPI; PCCL independently reports RCCL unreliability at scale and quantifies the algorithmic deficit.
- **The most important negative relation for this cluster**: the paper's related work has **no comparison with MSCCL and no comparison with GPU-initiated/NVSHMEM-based approaches**, and **no discussion of kernel-resident collective implementations or device-side algorithm selection**. A 2026 large-scale collectives paper that does not engage the device-initiated line is direct evidence against a claimed field-wide progression.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO, but this is the weakest-GPU-specificity paper among the nine deep analyses in this cluster, and that is recorded deliberately.** The GPU-specific properties the contribution depends on are: (a) the **two-level decomposition boundary is the GPU-interconnect boundary** — intra-node NVLink/Infinity Fabric is delegated to NCCL/RCCL while inter-node uses custom MPI, a split that exists only because a node contains a fast GPU peer fabric; (b) **the GCD abstraction** on MI250X, where 8 GCDs per node are 8 endpoints, which is what makes the endpoint count reach 2,048 at 256 nodes; (c) **reductions must run on the GPU**, and the paper's diagnosis of Cray-MPICH is precisely that it does them on the CPU; (d) the **GCD→NIC mapping** (2 GCDs per NIC). The *algorithms themselves* (ring vs recursive doubling/halving) are classical MPI collective algorithms and are not GPU-specific — the contribution is their correct placement relative to a GPU node's fabric hierarchy.

**Control placement**: `host-driven`. All communication is CPU/host-initiated through standard MPI send/receive and vendor-library APIs. Reduction *arithmetic* runs in GPU-resident kernels, but the collective orchestration is synchronous and CPU-driven, with no kernel-based NIC access and no NVSHMEM-style device-resident put/get. Established from the full text; the paper's related work explicitly does not engage device-resident collective implementations. `[paper]`

verdict_basis: The contribution is the placement of classical collective algorithms against a GPU node's specific fabric hierarchy (GCD endpoints, intra-node NVLink/Infinity Fabric delegated to NCCL/RCCL, GPU-resident reduction kernels, GCD→NIC binding); the algorithms are not GPU-specific but their arrangement and the diagnosed failure modes are.

# GPU-SC24-01 — Exploring GPU-to-GPU Communication: Insights into Supercomputer Interconnects

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `L Multi-GPU interconnect & data paths`
secondary_topics: `M GPU-aware / GPU-initiated communication & collectives`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `arXiv HTML v1 (arxiv.org/html/2408.14090v1) read across §II Systems Description, §III Intra-node Point-to-Point, §IV Intra-node Collectives, §V Inter-node Performance, §VI Network Congestion and Noise, §VIII Discussion. Section headings verified verbatim. Figures/tables not individually transcribed.`

## 12.1 Bibliographic facts
- Title (official, per census `SC_2024.md` row 13): *Exploring GPU-to-GPU Communication: Insights into Supercomputer Interconnects* `[paper]`
- Authors `[paper]`: Daniele De Sensi, Lorenzo Pichetti, Flavio Vella, Tiziano De Matteis, Zebin Ren, Luigi Fusco, Matteo Turisini, Daniele Cesarini, Kurt Lust, Animesh Trivedi, Duncan Roweth, Filippo Spiga, Salvatore Di Girolamo, Torsten Hoefler. Affiliations named in the HTML include Sapienza University of Rome, Vrije Universiteit Amsterdam, University of Trento, ETH Zurich, CINECA, University of Antwerp, HPE Cray, NVIDIA. `[paper]` — the HTML author/affiliation mapping was read but the exact author-to-institution pairing is recorded as partially `UNKNOWN` (the conversion interleaves them).
- Venue: SC 2024. DOI `10.1109/SC41406.2024.00039` `[census]`
- Publication type: `ARCHIVAL_MAIN_PAPER`; the read source is the `PREPRINT` at arXiv:2408.14090.

## 12.2 Core question (one sentence)
Across three production/pre-production multi-GPU supercomputers with three different interconnect stacks, which GPU-to-GPU data path and communication API actually delivers the available bandwidth and latency, and where does the software stack — not the hardware — become the limit? `[paper]`

## 12.3 GPU/HPC problem translation
- **Communication**: the whole contribution. The paper is a measurement study of the inter-GPU data path at two levels: intra-node (NVLink 4.0, NVLink 3.0 + PCIe Gen4, AMD Infinity Fabric between GCDs) and inter-node (Slingshot-11 Dragonfly, InfiniBand HDR Dragonfly+). `[paper]`
- **Memory**: the staging choice (host-memory bounce buffer vs. direct device-to-device) is treated as a first-class variable, because it determines whether data crosses PCIe and host DRAM. `[paper]`
- **Synchronization**: only indirectly — collective-library internals are treated as a black box.
- **Compute / scheduling**: not addressed.

## 12.4 Why the problem exists
Root causes the paper's own measurements support:
1. **Heterogeneous intra-node fabrics with non-uniform per-pair link counts.** On Alps each H100 pair has 6 NVLink 4.0 links (paper states 1.2 Tb/s unidirectional); on Leonardo each A100 pair has 4 NVLink 3.0 links (800 Gb/s) *plus* a PCIe Gen4 path (256 Gb/s per GPU); on LUMI-G each MI250X GCD has between one and four 400 Gb/s Infinity Fabric links to other GCDs. Because the per-pair link count varies, a library that assumes a uniform peer bandwidth mis-plans. `[paper]`
2. **Library bandwidth estimation can be simply wrong.** The paper attributes the LUMI GPU0↔GPU5 RCCL deficit to a bandwidth-estimation issue inside the library rather than to the fabric. `[paper]`
3. **Rail structure differs even at equal nominal bandwidth.** Alps and LUMI-G both use 4× HPE Cray Cassini-1 200 Gb/s NICs; Leonardo uses 2× dual-port NVIDIA ConnectX-6 at 100 Gb/s per port, i.e. 4 ports but a different NIC-to-GPU attachment. `[paper]`

## 12.5 Mathematical / performance model
`NOT_IN_PAPER` as a closed-form model. The paper reports goodput and latency curves against transfer size, plus an efficiency figure (fraction of achieved vs. expected bandwidth) for alltoall at scale. No analytical latency/bandwidth model (no α–β fit) is derived. `[paper]`

## 12.6 Data layout and ownership
- **GPU → node**: a rank owns one GPU (or one GCD on LUMI-G, where the 4 MI250X are treated as 8 GPUs). Buffers are either device-resident or host-resident, and the paper measures both.
- **node → cluster**: measured at same-switch, same-group, and different-group placements on Leonardo; the paper reports network *location* sensitivity separately per system.
- Thread/warp/block-level ownership: `NOT_IN_PAPER` — the study does not open the collective kernels.

## 12.7 Pseudo code
The measured primitives, as the paper names them `[paper]`:
```
# Baseline: host staging
cudaMemcpy(h_buf, d_buf, n, D2H); MPI_Send(h_buf,...); # "Trivial Staging"

# Device-to-device copy (intra-node), using shared memory handles across processes
cudaIpcGetMemHandle / peer mapping, then device-to-device copy   # "Device-Device Copy"

# GPU-Aware MPI
MPI_Send(d_buf, ...)            # device pointer passed directly

# Collectives
ncclAllReduce / ncclAlltoAll (Alps, Leonardo)
rcclAllReduce / rcclAlltoAll  (LUMI-G)
```
No new algorithm is proposed, so there is no contributed pseudo code. `[paper]`

## 12.8 Real implementation
No artifact repository was established for this paper (census records artifact as `UNKNOWN`). `NOT_INSPECTED` — no code was read, and no symbols are asserted beyond the API names the paper itself prints. `[paper]`

## 12.9 Kernel execution
`NOT_IN_PAPER`. The study measures NCCL/RCCL/MPI as opaque libraries; it does not report channel counts, CTA counts, or per-warp behaviour inside the collective kernels.

## 12.10 Memory traffic
The paper distinguishes only at the path level: host-staged transfers traverse device→PCIe→host DRAM→NIC; device-to-device transfers traverse NVLink/Infinity Fabric directly; inter-node GPU-buffer transfers traverse the NIC with GPU memory as the source. Register/shared/L1/L2/HBM breakdown is `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)
The paper's decomposed findings, each with its qualifier `[paper]`:
- **GPU-aware MPI beats NCCL for intra-node point-to-point on Leonardo** (4× A100, NVLink 3.0 + PCIe Gen4): up to 2× higher goodput at medium transfer sizes. Cause attributed to library path selection, not fabric.
- **GPU-aware MPI beats RCCL for small intra-node collectives on LUMI-G** (MI250X GCDs, Infinity Fabric): up to 3× faster at small transfers.
- **RCCL underperforms on a specific GCD pair on LUMI-G**: less than half the goodput of GPU-aware MPI for GPU0↔GPU5, attributed to a bandwidth-estimation defect.
- **MPI beats NCCL for inter-node point-to-point**: up to one order of magnitude on small transfers and up to 3× on larger transfers.
- **But NCCL wins intra-node collectives on Alps and Leonardo at all transfer sizes.** The direction of the MPI-vs-NCCL result therefore flips between operation class and system — this, not any single number, is the paper's substantive result.
- **Network placement sensitivity is system-dependent**: on Leonardo (InfiniBand HDR Dragonfly+, 23 groups) average latency increases ~2× for GPU-memory buffers when the peers are in different groups vs. on the same switch; on Alps and LUMI-G (Slingshot-11 Dragonfly) placement impact is below 30% for latency and below 1% for goodput.
- **Alltoall efficiency**: NCCL sustains around 75% efficiency up to 1,024 GPUs on Alps and Leonardo.
- **Noise**: on Leonardo only, network noise adds a further ~20% drop on alltoall and ~50% on allreduce at 1,024 GPUs; the paper states Slingshot is largely unaffected.

## 12.12 Hardware generation dependence
Strongly generation- and vendor-dependent by construction: NVLink 4.0 (H100/Alps) vs. NVLink 3.0 + PCIe Gen4 (A100/Leonardo) vs. Infinity Fabric between MI250X GCDs (LUMI-G); Slingshot-11 vs. InfiniBand HDR; Cassini-1 vs. ConnectX-6. The MPI-vs-NCCL/RCCL ordering does not transfer across these. `[paper]`

## 12.13 Limitations
Stated by the authors `[paper]`:
1. Alps was not yet in production; stack-wide optimization ongoing, with acknowledged instability.
2. Scale caps set by allocation policy, not by the method: Leonardo stops at 1,024 GPUs (256-node job limit), Alps GPU-aware tests at 2,048 GPUs (512 nodes available), LUMI at 512 nodes.
3. NCCL and RCCL alltoall benchmarks get stuck at 512+ GPUs; the NCCL benchmark stalls at 1,024 GPUs and above.
4. Three systems only; the authors caveat that very large fat-tree systems may show higher latency due to greater diameter.
5. Noise analysis confined to Leonardo.
6. **No device-initiated measurements.** NVSHMEM, device-side put/get and GPU-initiated RDMA are not evaluated. This is the single most important limitation for this cluster.

## 12.14 Relation to prior corpus
- No prior analysis exists in this repository (`domains/gpu_systems/corpus/` contained only templates before this cluster). `[repo-grep]`
- `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`: `domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` and is known to contain GPU communication/collectives coverage. No claim is made here about whether this paper is or is not already analysed there.
- **Complementary / precursor** to `GPU-ISC26-01` (PICO): shares author Daniele De Sensi and the same "default library choice is not the best choice" thesis, moved from measurement to a reusable framework.
- **Baseline supplier** to `GPU-ASPLOS26-01` (MSCCL++), `GPU-SC26-21` (Every Microsecond Matters), `GPU-IPDPS26-01` (NIMBLE), `GPU-IPDPS26-02` (Big Send-off): all four argue against NCCL/RCCL defaults, which this paper quantifies first.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.** The contribution is a measurement of specific inter-GPU fabrics — NVLink 4.0/3.0 link counts per GPU pair, PCIe Gen4 as a *parallel* intra-node path alongside NVLink, AMD Infinity Fabric with a variable one-to-four link count between MI250X GCDs, and the GCD-as-GPU abstraction — together with GPU-resident-buffer vs. host-staged path comparison. None of those objects exist for a CPU-only system, and the specific asymmetries measured are properties of these GPU packages/fabrics.

**Control placement**: `host-driven`. All measured paths are host-initiated: MPI ranks on the CPU enqueue transfers, collective libraries launch device kernels from the host, and the device-to-device copy path is set up by the CPU via shared memory handles across processes. The paper contains no device-resident put/get measurement and does not evaluate NVSHMEM. Established from the full text, §III–§V and §VIII. `[paper]`

verdict_basis: The measured objects (NVLink generations and per-pair link counts, Infinity Fabric GCD topology, GPU-memory-sourced NIC transfers, GPU-aware MPI vs. NCCL/RCCL) are GPU-interconnect properties with no CPU analogue; the study's findings are not restatements of general network results.

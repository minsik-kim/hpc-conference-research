# GPU-MICRO24-122 — Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS`
primary_topic: `Q — fixed-function GPU units repurposed for general computation (RT accelerator generalisation)`
secondary_topics: `GPU microarchitecture; tree traversal (B-tree/B*-tree/B+-tree, octree/quadtree, radius search); SIMT divergence; DRAM bandwidth utilisation; Vulkan ray-tracing programming model`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via author-hosted PDF (people.ece.ubc.ca/aamodt/publications/papers/tta.micro2024.pdf) — introduction/motivation and Figure 1, §II background on RTA structure (Figure 4a) and §II-C the four stated RTA advantages, §III-A programming interface, §III-B TTA hardware changes (Algorithms 1 and 2, Figure 8), §III-C TTA+ OP-unit architecture and Table I latencies, §IV evaluation setup and Table II config, Figures 12-20 results/ablations/energy, limitations as stated, related work.`

## 12.1 Bibliographic facts

- Title: **Generalizing Ray Tracing Accelerators for Tree Traversals on GPUs** [paper]
- Venue: **MICRO 2024**, session **7B GPU Microarchitecture II** [official-program, census `MICRO_2024.md` row 16]. The author-hosted PDF does not print a venue banner; venue comes from the census/program row. IEEE Xplore document 10764639 (418 here).
- Authors and affiliations [paper]: **Dongho Ha, Lufei Liu, Yuan Hsi Chou, Seokjin Go, Won Woo Ro, Hung-Wei Tseng, Tor M. Aamodt** — Yonsei University (Ha, Go, Ro); University of British Columbia (Liu, Chou, Aamodt); UC Riverside (Tseng).
- DOI: **`10.1109/MICRO61859.2024.00080`** [official-web: escalab.org publications page, Hung-Wei Tseng's lab]. IEEE Xplore document 10764639 (418 here).
- Publication type: `ARCHIVAL_MAIN_PAPER`.
- Artifact: `https://zenodo.org/doi/10.5281/zenodo.13294690` — **NOT_INSPECTED** (Zenodo not fetched in this pass). No source symbols are asserted.
- Proposed units: **TTA (Tree Traversal Accelerator)** and **TTA+** (the programmable, OP-unit-decomposed variant) [paper].

## 12.2 Core question (one sentence)

The GPU's Ray-Tracing Accelerator is not really a *ray* engine — it is a **divergence-absorbing tree-walking state machine** with a hardware traversal stack, a node-request coalescing memory scheduler and fixed-function predicate units; so can its predicate units be re-specified (TTA) or fully decomposed into a programmable network of operation units (TTA+) so that B-trees, octrees/quadtrees and radius search get the same 91% dynamic-instruction reduction and 2x DRAM-utilisation benefit that ray tracing already gets?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's §II-C enumerates exactly what the RTA buys, and these are the four quantities the generalisation is trying to transfer [paper]: (1) fixed-function units reduce dynamic instructions by **~91%**; (2) a single `traceRay` instruction **eliminates SIMT divergence** for the traversal loop; (3) a dedicated memory scheduler improves **DRAM utilisation by ~2x**; (4) general-purpose cores are freed for shading/post-processing.
- **Memory.** The RTA's **memory scheduler coalesces node requests and issues one memory request per cycle** [paper, Figure 4a]. This is the structure that a SIMT reimplementation has no analogue for, and Figure 13 shows TTA/TTA+ raise DRAM bandwidth utilisation across all tree traversals.
- **Synchronization.** The **warp buffer** holds per-ray traversal stack and ray origin/direction; TTA **repurposes it as a general-purpose register file** with 16 x 32-bit ray registers (RR) and node registers (NR) per entry, sized **8 KB for rays** (64 B/ray x 4 warps x 32 threads) and **2 KB for nodes** [paper].
- **Scheduling.** A **warp scheduler** selects warps per cycle inside the unit; an **operation arbiter** decodes node type and routes to the right intersection unit via an **operation destination table** [paper, Figure 4a].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

- Tree traversal is "inherently divergent and irregular" on GPUs [paper]; Figure 1 shows low SIMT efficiency **and** low DRAM utilisation across diverse tree workloads — the same two pathologies the RTA was built to cure for ray tracing.
- The RTA cannot be used directly because its predicate hardware is **geometrically hardwired**: the **Ray-Box unit** is a 4-stage pipeline of FP subtractors, multipliers, min/max units and comparators (**13-cycle latency**), and the **Ray-Triangle unit** computes barycentric coordinates via cross/dot products, subtractors, multipliers, reciprocals and comparators (**37-cycle latency**) [paper]. A B-tree needs `key ? separator`, not a slab test.
- Software repurposing (RTNN and friends) pays "substantial overhead from suboptimal fit between the graphics pipeline and algorithms" and needs complex intersection shaders [paper] — this is the paper's explicit statement of why the software-mapping line (category Q's software branch) hits a ceiling.

## 12.5 Mathematical / performance model

Two new predicate kernels are defined as *reuses* of existing arithmetic [paper]:

- **Algorithm 1 — Query-key value comparison.** Modifies the **Ray-Box unit's min/max operations**: input query `X` is compared against key values `K1, K2, K3`; **equality operations are added** to detect key matches; the reused min/max pairs let the unit process **up to 9 children per min/max pair**. The 9-wide B-tree configuration in the evaluation follows from this.
- **Algorithm 2 — Point-to-point distance.** Leverages the **Ray-Triangle unit's** existing vector subtractors, dot-product units, multipliers and comparators to compute a **squared distance for threshold comparison**, integrated as an alternative datapath within that unit.

**TTA+** replaces the two fixed pipelines with a set of interconnected **OP units** [paper, Table I, latencies in cycles]: Vec3 Add/Sub (4), Multiplier (4), RCP (4), Cross Product (5), Dot Product (5), Vec3 CMP (1), MINMAX (1), MAXMIN (1), Logical (1), SQRT (11), R-XFORM matrix multiply (4), and a **PUSH unit for stack management**. Each OP unit carries an input decoder, compute unit, output buffer, configuration registers and an **operation destination table** that selects the next unit from node type and micro-op PC — i.e. the traversal predicate becomes a short dataflow program, not a wire.

## 12.6 Data layout and ownership

- **thread/ray → warp buffer entry**: 16 x 32-bit ray registers + node registers; 8 KB ray RF + 2 KB node RF [paper].
- **warp → TTA unit**: **1 TTA unit per SM, 4 warp buffers, 4 intersection-unit sets** [paper, Table II].
- **SM → GPU**: **8 SMs**, 32 max warps/SM, 32,768 registers/SM, GTO warp scheduler; **64 KB L1 + shared** (fully associative LRU, 20 cycles); **3 MB L2** (16-way, LRU, 160 cycles); clock ratio compute:interconnect:L2:memory = **1365:1365:1365:3500 MHz** [paper, Table II].
- **node layout is programmer-declared**: `DecodeR`, `DecodeI`, `DecodeL` specify **byte offsets** for the ray/query record, internal-node record and leaf-node record [paper]. This is the key layout mechanism — the tree's memory format is handed to the unit as an offset table instead of being fixed by the BVH format.
- **node → cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# ---- programming interface (§III-A) ----                      [paper]
DecodeR(byte offsets of the ray/query record)
DecodeI(byte offsets of the internal-node record)
DecodeL(byte offsets of the leaf-node record)
ConfigI(assembly program: the internal-node intersection test)
ConfigL(assembly program: the leaf-node intersection test)
ConfigTerminate(traversal termination condition)

# ray tracing:  traceRayEXT(...)          ->  traverseTreeTTA(...)
# host:         vkCmdTraceRaysKHR(...)    ->  vkCmdTraverseTree(...)

# ---- baseline traversal the unit absorbs (Algorithm 3) ----   [paper]
push(root)
while stack not empty:
    node = pop()
    if internal:  for child in children: if test(query, child): push(child)
    else:         leaf_test(query, node)
```

`traverseTreeTTA`, `vkCmdTraverseTree`, `DecodeR/DecodeI/DecodeL`, `ConfigI/ConfigL/ConfigTerminate`, `traceRayEXT`, `vkCmdTraceRaysKHR` are the paper's names [paper]; the while-loop skeleton is `[reconstruction]` of the paper's Algorithm 3.

## 12.8 Real implementation

`NOT_INSPECTED`. The Zenodo artifact (`10.5281/zenodo.13294690`) was not fetched in this pass; no source symbols are asserted. The simulator is **Vulkan-Sim** [paper, cited as reference 83], modified in two ways the paper states: the functional simulation was extended to support the new programming model, and individual operation-unit models were added for TTA+ [paper].

## 12.9 Kernel execution

kernel → CTA → warp → **`traverseTreeTTA` instruction**, which replaces an entire traversal loop. The paper measures the consequence directly: **TTA instructions reduce dynamic instructions by 91% on average**, and **TTA instructions are only 2% of total dynamic instructions** [paper, Figure 20]. The execution-level point is that the loop is no longer in the instruction stream at all — it has become a hardware state machine plus, in TTA+, a micro-op program inside the OP-unit network.

## 12.10 Memory traffic

- **DRAM**: Figure 13 shows TTA/TTA+ significantly improve bandwidth utilisation for all tree traversals, most strongly for B-tree variants and radius search [paper]. The cause is the RTA's node-request coalescing memory scheduler, now applied to non-BVH nodes.
- **On-unit RF**: 8 KB ray + 2 KB node [paper].
- **Cache**: 64 KB L1+shared (20 cycles), 3 MB L2 (160 cycles) in the modelled GPU [paper, Table II].
- Per-level byte counts: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

All results are **simulated in Vulkan-Sim on the 8-SM configuration of Table II**; **no real GPU was benchmarked** [paper].

**Versus CUDA implementations on the GPU's general-purpose cores** [paper, Figure 12]:
- **B-Tree: up to 5.4x** (geometric mean **2.4x** across variants)
- **B\*-Tree**: competitive with B-Tree
- **B+-Tree: ~1.2x** — explicitly attributed to B+-trees having **less divergence to remove**
- **N-Body (Barnes-Hut, 2D quadtree / 3D octree, 8k–64k particles): 1.1–1.7x** (1.2x with kernel fusion on TTA+)
- **Radius search (RTNN framework, 32k–128k KITTI points): 1.4x** by offloading intersection shaders to TTA+
- **WKND_PT (ray-sphere via procedural geometry)**: unsupported by TTA; TTA+ with optimisation reaches **1.2x**

The B+-tree result is the most informative single data point in the cluster: the gain is **proportional to the divergence and irregularity removed**, not to the arithmetic offloaded. Where the baseline is already coherent, the RTA-shaped unit has nothing to sell.

**Cost of generality, versus an unmodified RTA on graphics work** [paper, Figure 16]: TTA+ is **8% slower on average** on unmodified LumiBench workloads, because decomposing the fixed pipelines into interconnected OP units serialises operations and adds crossbar latency — **Ray-Box latency rises ~10x**. Selected workloads recover: WKND_PT **+22%** with TTA+'s square-root unit; SHIP_SH recovers via the SATO optimisation. This is the honest price of programmability and should always be quoted with the 8% figure attached.

**Energy** [paper, Figure 19]: B-Tree variants **15–62% energy reduction** versus the baseline GPU; N-Body similar despite lower speedup; RTNN/WKND_PT **19–29%** when intersection shaders are offloaded. These are **model estimates from the simulator plus 45 nm FreePDK45 synthesis**, not measured energy.

**Area** [paper]: TTA **0.7%**; TTA+ **up to 36.4% over baseline**, driven by the SQRT unit. Again synthesised, not measured.

## 12.12 Hardware generation dependence

- The baseline is the **NVIDIA-style RTA model as implemented in Vulkan-Sim** — a **hardware** state machine that owns the traversal stack, with a warp buffer, warp scheduler, memory scheduler, operation arbiter and fixed-function Ray-Box (13-cycle) / Ray-Triangle (37-cycle) units [paper, Figure 4a]. This is deliberately **not** the AMD RDNA3 model used by `GPU-MICRO24-121` (HSU), where **software** manages the stack and one `IMAGE_INTERSECT_RAY` instruction does the test. The two MICRO 2024 papers generalise **different** RT hardware models, and their numbers must never be compared directly.
- **No RT-core generation is named** (Turing 1st-gen / Ampere 2nd-gen / Ada 3rd-gen with SER and OMM/DMM / Blackwell 4th-gen). The model is a generic RTA. Do not attribute the results to any specific generation. `NOT_IN_PAPER`.
- **No real GPU**; simulation only. The modelled GPU is an 8-SM scale model, far smaller than any shipping RT-capable part [paper, Table II].
- Interface is **Vulkan** (`traceRayEXT`, `vkCmdTraceRaysKHR`), not OptiX/CUDA — a different API surface from the software-mapping papers in this cluster [paper].

## 12.13 Limitations

Stated or directly supported [paper]:
1. **Simulation only** — no silicon, no real-GPU validation.
2. **Generality costs graphics performance**: TTA+ loses **8% on average** on unmodified LumiBench; recovery requires **manual code adaptation**.
3. **Interconnect overhead**: serialised OP-unit operations and the crossbar raise Ray-Box latency ~10x.
4. **Configuration constraints**: applications must express their predicate within the OP-unit sequencing; complex post-processing stays on general-purpose cores.
5. **Area trade-off**: the SQRT unit alone costs 36.4%; the optimal OP-unit count is workload-dependent.
6. **Traversal phase only** — post-processing computation is out of scope.
- `[inference]` The TTA (non-plus) variant supports only the two new predicate families it hardwires; WKND_PT's unsupported-by-TTA status shows the fixed variant's coverage is narrow, and the programmable variant is where the generality actually lives — at 8% graphics cost.

## 12.14 Relation to prior corpus

- **Twin paper, same session**: `GPU-MICRO24-121` (HSU, Barnes/Shen/Rogers). Same MICRO 2024 session 7B, same thesis, different RT hardware baseline (NVIDIA-style hardware stack vs AMD RDNA3 software stack), different mechanism (reconfigurable OP-unit network + Vulkan API extension vs three new fixed instructions), different simulator (Vulkan-Sim vs Accel-Sim/GPGPU-Sim 4.0). Together they are the **hardware branch of category Q**.
- **Cited downstream, verified**: `GPU-ASPLOS25-124` (Treelet Accelerated Ray Tracing, Chou & Aamodt) cites "Ha et al. [14]" and "Barnes et al. [6]" in its conclusion as the works extending RTAs to general tree traversal [paper, Treelet]. Same group (Aamodt, UBC) and shared co-author Yuan Hsi Chou.
- **Supersedes-by-argument**: the software-mapping line — RTNN (Zhu), RTIndeX (Henneberg & Schuhknecht), RT-DBSCAN and RT-kNNS Unbound (Nagarajan et al.), Morrical/Wald mesh point location, Wald's ray transforms [paper, related work]. `GPU-ICS24-125` (Arkade) and RT-BarnesHut belong to that line. TTA both cites it and measures against it: RTNN's radius search is one of TTA+'s benchmarks, improved 1.4x by offloading the intersection shader.
- **Complementary, cross-cluster**: Heliostat (ISCA 2025), `_LEDGER_memory_virtualization.md`, `CORE_GPU`/`ABSTRACT_ONLY`. Won Woo Ro co-authors both TTA and Heliostat — a **verified author-level lineage** from "generalise the RTA for application trees" (MICRO 2024) to "run the page-table walk on the RTA" (ISCA 2025).
- **Contrast**: the tensor-core cluster's papers repurpose a dense-arithmetic unit with **no hardware change**; TTA/TTA+ change the hardware and pay a measured graphics-performance tax for it.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

**Sharp form — would the contribution survive if the RT accelerator were replaced by ordinary SIMT cores?** No, and this paper names the missing pieces more precisely than any other in the cluster. SIMT cores do not supply: (a) the **hardware traversal stack and state machine** that turns a divergent while-loop into one instruction (hence the 91% dynamic-instruction reduction and the elimination of traversal divergence); (b) the **dedicated node-request coalescing memory scheduler**, whose absence is why the CUDA baselines show low DRAM utilisation in Figure 1 and why Figure 13 shows TTA restoring it; (c) the **fixed-function predicate units** (Ray-Box 13-cycle, Ray-Triangle 37-cycle) whose subtractors, multipliers, min/max units and comparators the new query-key and point-to-point modes reuse rather than duplicate; and (d) the **warp buffer**, reused as the unit's register file. The B+-tree result (only ~1.2x, because that baseline is already coherent) is the internal control that proves the gain comes from the divergence/bandwidth machinery, not from arithmetic throughput.

**Hardware change or software mapping?** **HARDWARE CHANGE**, in two degrees: TTA (modest — add equality comparators and a bypass to the Ray-Box unit, add an alternative datapath inside the Ray-Triangle unit; 0.7% area) and TTA+ (radical — decompose the fixed pipelines into a programmable OP-unit network; up to 36.4% area and an 8% graphics slowdown). A programming-interface change (Vulkan `traverseTreeTTA` / `vkCmdTraverseTree` plus Decode/Config calls) accompanies both.

**Simulated or measured?** **SIMULATED** — Vulkan-Sim, 8-SM configuration (Table II), with 45 nm FreePDK45 synthesis for area/energy. No real GPU SKU was benchmarked; area and energy figures are estimates, not measurements.

verdict_basis: The contribution is a microarchitectural generalisation of the GPU ray-tracing accelerator — its traversal state machine, warp buffer, memory scheduler and fixed-function intersection units — evaluated inside a cycle-level GPU simulator. Every quantity it improves (SIMT efficiency, DRAM utilisation, dynamic instruction count) is a property of the GPU RTA that no CPU or generic accelerator possesses.

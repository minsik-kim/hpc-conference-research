# SC 2024 / SC 2025 — Quantum-HPC Regular Paper Census

**Phase 2 of the Quantum-HPC Research Landscape**
**Census date: 2026-09-06 (KST)**
**Scope: SC 2024 and SC 2025 main-conference regular/full technical research papers only**

---

## 0. How to read this document

Evidence tags used throughout:

| Tag | Meaning |
|---|---|
| `[official-program]` | Verified against the official SC technical program (sc24/sc25.conference-program.com) |
| `[proceedings]` | Verified against the publisher volume record (Crossref container metadata, ACM DL, IEEE Xplore) |
| `[paper]` | Read from the paper full text — **preprint where noted** |
| `[abstract]` | Only the abstract was obtainable |
| `[code]` | Observed directly in a source repository |
| `[artifact]` | From an artifact package, Zenodo deposit, or reproducibility report metadata |
| `[documentation]` | From a README, project page, or official docs |
| `[inference]` | My reasoning on top of the above — **never a paper fact** |

Status vocabulary: `PUBLISHED_REGULAR_PAPER`, `STATUS_UNCLEAR`, `NOT_FOUND`, `CONTEXT_NOT_STATED`.
Artifact vocabulary: `PUBLIC_CODE`, `PUBLIC_ARTIFACT`, `PARTIAL`, `NO_PUBLIC_ARTIFACT_FOUND`, `UNKNOWN`.
Trend vocabulary: `OBSERVED_SHIFT` (defensible from the corpus), `INSUFFICIENT_SAMPLE` (n too small to claim a trend).
Absence vocabulary: `VENUE_GAP` only. **This document never declares a research gap.**

> **A note on sources.** IEEE Xplore and the ACM Digital Library were unreachable from this environment (proxy 403 on CONNECT), and SC's own `/proceedings/` paths are robots-disallowed. Bibliographic facts were therefore established through the **Crossref REST API** (which returns the authoritative container-title and DOI prefix, the only reliable main-track-vs-workshop discriminator) and the **official SC program sites**, which were reachable. Paper *content* came from arXiv preprints where they exist. **Every preprint-sourced fact is marked, because the published version may differ.** Two papers — LEXIQL and DQTetris — are closed access with no preprint, and their entries are honestly thin as a result.

---

## 1. Executive summary

### 1.1 The population

**SC 2024: 7 relevant main-track regular papers. SC 2025: 4.** Both counts were established by exhaustive enumeration of the publisher volume, not by keyword sampling, and both match Phase 1's figures.

| | SC 2024 | SC 2025 |
|---|---|---|
| Relevant regular papers | **7** | **4** |
| Total regular research papers in volume | 99 (+9 Gordon Bell = 108 archival) `[proceedings]` | 137 accepted / 144 printed (133 regular + 11 Gordon Bell) `[official-program]` `[proceedings]` |
| Quantum share of regular papers | **7.1%** | **2.9%** |
| Acceptance rate | `NOT_FOUND` (no official figure obtainable) | **22%** (137 of 623) `[official-program]` |
| Quantum sessions | **3** — "Quantum and Approximate Computing I / II / III" | **1** — "Quantum Computing and Simulation" |
| Papers with public code or data | 4 of 7 | 3 of 4 |
| Papers with an official SC Reproducibility Report | 0 | 1 |
| Papers that used a real QPU substantively | **0** | **1** (QDockBank) |
| Papers reporting strong or weak scaling | 2 of 7 | 1 of 4 (partly asserted) |

### 1.2 The core research branches

Across the 11 papers, five branches account for everything:

| Branch | SC24 | SC25 | Papers |
|---|---|---|---|
| **Quantum compilation / mapping / routing** | 3 | 1 | QFT Kernels, PARALLAX, (Surface Codes adjacent), DQTetris |
| **Classical simulation of quantum circuits** | 3 | 1 | Atlas, Surpassing Sycamore, MPS Quantum Kernels, PTSBE |
| **Resource management / orchestration** | 0 | 1 | Qonductor |
| **Reliability / QEC characterization** | 1 | 0 | Surface Codes |
| **Application / dataset** | 1 | 1 | LEXIQL, QDockBank |

### 1.3 The most important observation

**SC does not have one definition of "HPC contribution" in quantum research. It has at least four, and they are not equally demanding.**

1. **HPC *is* the contribution.** The quantum content is purely the workload. *Atlas* is the pure case — it contains no quantum algorithm, no physics, no approximation, and its entire contribution is ILP-based partitioning, communication minimization, and a GPU/DRAM memory hierarchy. `[paper]`
2. **HPC is what makes a quantum claim possible.** *Surpassing Sycamore* argues a quantum-physics point (random circuit sampling is not an advantage), but the argument only exists because of a 32 TB distributed tensor network on 2,304 A100s with a custom complex-fp16 einsum and int4 communication quantization. `[paper]`
3. **HPC is the cost model of compilation.** *QFT Kernels*, *PARALLAX* and *DQTetris* all make their SC case by showing that the incumbent exact method does not scale — SAT timing out at 2 hours, SMT at 24 hours — and replacing it with something polynomial or closed-form. `[paper]`
4. **HPC is the scarce resource consumed.** *QDockBank* reports **no classical hardware at all** and contains no parallelism, no performance claim, and no systems methodology. Its argument is >60 hours of utility-scale QPU time and a publicly released dataset. `[paper]`

The fourth pathway is the one that should change how the rest of this research programme reads SC. It means SC's operative test is sometimes *scale of resource consumed and community value of the artifact*, not *nature of the methodological contribution*. That is a recognizable and long-standing SC tradition — hero runs and community benchmarks — being extended to a new resource type.

### 1.4 What the SC contribution shapes have in common

Where an HPC contribution *is* present, it is almost always one of three moves, and none of them is "we made a quantum thing better":

- **Replace a combinatorial search with something that scales.** QFT Kernels replaces SAT-based mapping with a synthesized closed-form affine movement pattern and reports *"Our method does not have compilation time as it is an analytical approach"* `[paper]`. PARALLAX replaces DPQA's SMT formulation — which *"cannot compile even small 9-16 qubit circuits within 24 hours"* `[paper]` — with a stated O(q⁵ + gq² + a²q² + ga²s + ga³) heuristic. Atlas replaces heuristic partitioning with a binary ILP proven to return the minimum stage count `[paper]`.
- **Amortize an expensive step across a batch.** PARALLAX replicates a compiled circuit up to 121× across a 1,225-atom array so one physical shot yields many logical shots. PTSBE pre-samples all stochastic decisions so statevector preparation scales with the number of *unique trajectories* rather than the number of shots. Both are the classical accelerator occupancy/batching argument, transplanted.
- **Make communication the object of optimization.** Atlas's ILP weights inter-node movement at c=3 relative to intra-node and pushes all communication to stage boundaries. DQTetris minimizes qubit *reassignment events* rather than per-gate teleportations. Surpassing Sycamore quantizes inter-node traffic to int4 because InfiniBand is ~3× slower than NVLink.

### 1.5 Five things that are true of this corpus and should be carried forward

1. **Real QPUs are almost absent.** Of 11 papers, exactly one (QDockBank) ran a substantial real-hardware campaign. Qonductor used real IBM devices only to build a training dataset and characterize fleet imbalance — its headline evaluation runs on eight Qiskit FakeBackends. `[paper]` The widely quotable "evaluated on 7,000+ real quantum runs" is precise but easy to misread.
2. **Most "N×" numbers in this corpus are not speedups.** They are circuit-quality ratios — gate count, depth, SWAP count, logical error rate. Reading them as performance numbers is a category error. §7.4 lists every headline number with its real context.
3. **Evaluation rigour is below general SC norms.** Four of eleven papers report no classical hardware whatsoever. Baseline software versions are essentially never given. Not one SC25 paper compares against an independent third-party system of the same kind.
4. **Artifact availability is much better than Phase 1 recorded** — 7 of 11 have public code or data, including four Zenodo deposits. Phase 1 marked nearly all of these `UNKNOWN`. This is the largest single correction this census produces.
5. **Reproducibility badging and artifact openness are decoupled.** The only paper with an official SC25 Reproducibility Report (DQTetris) is also the only SC25 paper with no discoverable public artifact and no open-access text.

---

## 2. Methodology

### 2.1 Inclusion

A paper is included if it is an **SC main-conference regular/full technical research paper** in 2024 or 2025 AND concerns quantum **computing** with relevance under at least one of:

- `HPC_FOR_Q` — classical HPC serving quantum: statevector / tensor-network / stabilizer / decision-diagram simulation, compilation and mapping, QEC decoding, circuit cutting, classical pre/post-processing
- `Q_IN_HPC` — QPU as a heterogeneous HPC resource: runtime, scheduling, resource management, workflow, multi-QPU, programming model
- `Q_FOR_HPC` — quantum methods for scientific/HPC workloads with computational or system implications
- `FUTURE_WORKLOAD` — quantum methods that materially change circuit count, shot count, depth, parallelism, CPU-QPU synchronization, classical pre/post-processing, communication, or memory requirements

Execution on a real QPU or a real supercomputer is **not** required. Conversely, running on a large machine is not by itself sufficient.

### 2.2 Exclusion

Structurally excluded and never counted: **workshop papers** (SC24-W / SC-W '25), posters, research posters, ACM Student Research Competition, Doctoral Showcase, demos, panels, Birds of a Feather, tutorials, invited talks, keynotes, short papers, extended abstracts, Exhibitor Forum presentations, and Reproducibility Reports (which are separate 2-page items in the SC25 volume — their *existence* is recorded as evidence, but they are not regular papers).

Topically excluded: **classical** quantum chemistry / many-body / quantum transport / quantum materials / DFT / neural-network-quantum-states work; post-quantum cryptography; "quantum-inspired" classical methods; pure device physics.

### 2.3 How main-track status was determined

The publisher volume identity is the discriminator, and it is unambiguous:

| Year | Main track | Workshops (excluded) |
|---|---|---|
| SC 2024 | container-title `SC24: International Conference for High Performance Computing, Networking, Storage and Analysis`, DOI prefix `10.1109/SC41406.2024.` | `SC24-W: Workshops of the…`, DOI prefix `10.1109/SCW63240.2024.` |
| SC 2025 | ACM, DOI prefix `10.1145/3712285.` | SC-W '25, DOI prefix `10.1145/3731599.` |

Every paper in §3 and §4 was individually confirmed against its Crossref DOI record's container-title. `[proceedings]`

**Title-form warning for downstream citation.** Three papers render differently across sources and will defeat naive string matching:
- **LEXIQL** / **PARALLAX** — IEEE and Crossref (the DOI record) use all caps; **ACM DL and the SC24 program render `LexiQL` and `Parallax`.** This document uses the DOI-record form.
- **QDockBank** — ACM/Crossref use lowercase *"A dataset"*; the SC25 program renders *"A Dataset"*. This document uses the publisher-of-record form.
- **Preprint titles differ from published titles** for two papers: *Surpassing Sycamore* (arXiv 2407.00769 is *"Achieving Energetic Superiority Through System-Level **Quantum** Circuit Simulation"* — no "Surpassing Sycamore:" prefix) and *Qonductor* (arXiv v1 is *"Orchestrating Quantum Cloud Environments with Qonductor"*). Atlas's arXiv version is an *"(Extended Version)"*.

### 2.4 How completeness was established

This is the part that matters most, because a census is only as good as its denominator.

**SC 2024.** The container was enumerated exhaustively via Crossref: a **contiguous, gap-free run of DOIs `.00001` through `.00114`** — 114 records, zero gaps, zero duplicates, with `.00115` returning 404, confirming `.00114` is the last item. All 114 titles were then swept with a ~25-term keyword set (not just "quantum"): qubit, QPU, NISQ, statevector, tensor network, stabilizer, decision diagram, circuit cutting/partitioning, transpil*, compile/map/route, error correction, decoder, surface code, neutral atom, trapped ion, superconducting, annealing, Ising, QUBO, post-Moore, entanglement, photonic, hybrid, emerging. Two independent Crossref relevance-ranked queries over the same container were run as a guard. `[proceedings]`

Volume structure: `.00001–.00006` front matter; `.00007–.00009` Gordon Bell Climate Modelling finalists; `.00010–.00015` Gordon Bell finalists; `.00016–.00114` = **99 regular technical papers**.

**SC 2025.** Crossref has no working container-title filter for this volume, so enumeration used the exact publication date (`2025-11-15`, shared by both SC volumes) with `filter=prefix:10.1145,type:proceedings-article`. That returned `total-results = 433`, and paging recovered **433 unique DOIs with zero duplicates** — an exact match, so the enumeration is complete rather than partial. Split: **181** items with prefix `10.1145/3712285.` (main) and **252** with `10.1145/3731599.` (workshops). The 181 main-volume items are **144 papers (pp. 1–2265) + 37 Reproducibility Reports (pp. 2266–2329)**. `[proceedings]`

**The strongest completeness proof is pagination.** Sorting the 144 SC25 papers by first page gives a perfectly contiguous run in which every paper's `last_page + 1` equals the next paper's `first_page`, with **no gap and no overlap across 2,265 pages**. A missing paper would necessarily leave a page gap. There is none.

### 2.5 A resolved discrepancy in the Phase 1 record

Phase 1 described SC24's quantum papers as sitting in "two consecutive session blocks" at `.00073/74/75` and `.00085/86/87`, yet also listed PARALLAX at `.00079` — in neither block. That internal inconsistency was the first thing this census tested. **Resolution: SC24 had three quantum sessions, not two blocks.** `[official-program]`

| DOI | Item | Session |
|---|---|---|
| `.00073` `.00074` `.00075` | LEXIQL, QFT Kernels, Surface Codes | **Quantum and Approximate Computing I** |
| `.00076` `.00077` | Revisiting Computation for Research; Understanding Data Movement Patterns in HPC | Analysis of HPC Systems |
| `.00078` | HPAC-ML: A Programming Model for Embedding ML Surrogates in Scientific Applications | **Quantum and Approximate Computing II** — the *approximate computing* half |
| `.00079` | PARALLAX | **Quantum and Approximate Computing II** |
| `.00080`–`.00084` | MixQ; LONG EXPOSURE; Adaptive Patching; TorchGT; Speed Galerkin Transformer | Sparsity and Quantization in ML; ML/transformer sessions |
| `.00085` `.00086` `.00087` | Surpassing Sycamore, MPS Quantum Kernels, Atlas | **Quantum and Approximate Computing III** |

PARALLAX is not an anomaly: its session held only two talks, and the other one was an approximate-computing paper. Note the trap this creates — **`.00078` (HPAC-ML) sits inside a session named "Quantum and Approximate Computing II" and has no quantum content at all.** Anyone censusing SC24 from session names rather than paper content will produce a false positive here.

### 2.6 Artifact search protocol

For each paper, in order: (1) the paper's own availability statement; (2) official SC artifact material — AD/AE appendices, SC25 Reproducibility Reports, badges; (3) author/lab/project homepage; (4) official GitHub/GitLab; (5) Zenodo / Figshare / HuggingFace. Where a repository was found it was **cloned and read** — README, top-level structure, build files, and key source files — to check whether the paper's headline systems claim is plausibly implemented. This is a repo-level check, deliberately not a line-by-line review.

`NO_PUBLIC_ARTIFACT_FOUND` means all five steps were searched and nothing official was located. **It does not mean code does not exist.**

### 2.7 Limitations — stated plainly

1. **Two papers could not be read.** LEXIQL (SC24) is closed access with no preprint; its entry is abstract-level only. DQTetris (SC25) is closed access with no preprint, and its cost model, baselines, benchmarks and hardware are all `NOT_FOUND`. Neither gap is fillable without institutional ACM/IEEE access.
2. **Nine of eleven entries rest partly on arXiv preprints**, not the published versions. Every such fact is tagged. One divergence was actually detected (Qonductor, §4.1) — which is direct evidence that this caveat is not theoretical.
3. **Two paper titles differ between preprint and publication.** Surpassing Sycamore's arXiv version (2407.00769) is titled *"Achieving Energetic Superiority Through System-Level **Quantum** Circuit Simulation"*. Atlas's arXiv version (2408.09055v2) is explicitly an *"(Extended Version)"* — its theorems and complexity analysis may not all appear in the SC24 paper.
4. **SC24's acceptance rate could not be obtained** from any official source; the 99/108 denominators are counted from the DOI enumeration, not quoted from SC.
5. **No AD/AE appendix could be read**, since all publisher PDFs were unreachable. Artifact-badge status is therefore unverified for every SC24 paper.
6. **One artifact status is contested between two independent searches** — see DQTetris in §9.

---

## 3. SC 2024 census

**Session structure** `[official-program]`: three sessions, all in the SC24 technical program.
- *Quantum and Approximate Computing I* — Wed 20 Nov 2024, 3:30–5:00pm EST, Room B308 (sess385), **chair Helena Liebelt** (Deggendorf Institute of Technology / Intel) — 3 talks
- *Quantum and Approximate Computing II* — Thu 21 Nov 2024, 9:00–10:00am EST, Room B312-B313A (sess387), **chair Flavio Vella** (University of Trento) — 2 talks, one of which is not quantum
- *Quantum and Approximate Computing III* — Thu 21 Nov 2024, 10:30am–12:00pm EST, Room B312-B313A (sess386), **chair Tirthak Patel** (Rice University) — 3 talks

### 3.0 SC 2024 master table

| # | Title | First author / group | DOI | Session | Tags | Branch | Artifact |
|---|---|---|---|---|---|---|---|
| 1 | LEXIQL: Quantum Natural Language Processing on NISQ-era Machines | Silver (Northeastern) | `10.1109/SC41406.2024.00073` | QAC I | `Q_FOR_HPC` `FUTURE_WORKLOAD` | application | `NO_PUBLIC_ARTIFACT_FOUND` |
| 2 | Optimizing Quantum Fourier Transformation (QFT) Kernels for Modern NISQ and FT Architectures | Jin (Rutgers) | `.00074` | QAC I | `HPC_FOR_Q` | compiler | `PUBLIC_CODE` |
| 3 | On the Efficacy of Surface Codes in Compensating for Radiation Events in Superconducting Devices | Vallero (Trento) | `.00075` | QAC I | `HPC_FOR_Q` `FUTURE_WORKLOAD` | QEC / reliability | `NO_PUBLIC_ARTIFACT_FOUND` |
| 4 | PARALLAX: A Compiler for Neutral Atom Quantum Computers under Hardware Constraints | Ludmir (Rice) | `.00079` | QAC II | `HPC_FOR_Q` | compiler + throughput | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` |
| 5 | Surpassing Sycamore: Achieving Energetic Superiority Through System-Level Circuit Simulation | Fu (Shanghai AI Lab / USTC / CAS) | `.00085` | QAC III | `HPC_FOR_Q` | tensor-network simulation | `NO_PUBLIC_ARTIFACT_FOUND` |
| 6 | Realizing Quantum Kernel Models at Scale with Matrix Product State Simulation | Metcalf (HSBC) + Quantinuum | `.00086` | QAC III | `HPC_FOR_Q` `Q_FOR_HPC` | MPS simulation | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` |
| 7 | Atlas: Hierarchical Partitioning for Quantum Circuit Simulation on GPUs | Xu (CMU) | `.00087` | QAC III | `HPC_FOR_Q` | distributed GPU simulation | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` |

**Awards** `[official-program]`: **LEXIQL (.00073) and Surface Codes (.00075) were both Best Student Paper Finalists.** No quantum paper was a Gordon Bell finalist. The final winners list could not be retrieved (SC24 awards pages robots-disallowed).

---

### 3.1 LEXIQL: Quantum Natural Language Processing on NISQ-era Machines

**Bibliographic.** Daniel Silver, Aditya Ranjan (Northeastern), Rakesh Achutha (IIT-BHU Varanasi), Tirthak Patel (Rice), Devesh Tiwari (Northeastern). SC 2024, main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing I* (chair Helena Liebelt, Deggendorf Institute of Technology / Intel), **Best Student Paper Finalist** `[official-program]`. DOI `10.1109/SC41406.2024.00073`, pp. 1–15. `PUBLISHED_REGULAR_PAPER`.
> **Evidence note for the award claim.** The Best Student Paper Finalist badge for LEXIQL renders **only on the SC24 presenter page** ([`sc24.conference-program.com/presenter/?uid=304504`](https://sc24.conference-program.com/presenter/?uid=304504), Aditya Ranjan) — **not** on the paper's own presentation page, and neither author group's website annotates it. Cite that specific URL. (The Surface Codes badge, by contrast, renders directly on the session page.)
**Classification.** `Q_FOR_HPC` + `FUTURE_WORKLOAD`. Branch: scientific/ML application.

> **Source limitation — read first.** This paper is closed access on IEEE and ACM, has **no arXiv preprint** (Semantic Scholar reports `openAccessPdf.status: "CLOSED"`), is not in NSF-PAR, and the authors' lab publications page shows an **empty artifact link placeholder**. **Everything below abstract level is `NOT_FOUND`, and nothing has been filled in by inference from the group's other papers.**

**Research question** `[abstract]`. Can text classification be performed on NISQ machines with a circuit design and training method that remains effective under real device noise, rather than only in noiseless simulation?

**A. Quantum problem** `[abstract]`. Expressibility and noise tolerance are in direct conflict: expressible ansätze are deep and are destroyed by NISQ noise; shallow noise-tolerant circuits lack representational power. LEXIQL's stated answers are *"an incremental data injection approach to process textual data in a quantum circuit"* and training over *"a diverse mix of expressible and shallow quantum circuits."*

**B. HPC problem.** **Not identifiable from any reachable source — and this is a finding, not a search failure.** The abstract states no computational-cost, parallelism, memory, communication, scheduling or latency problem. Variational training over an ensemble of circuits implies repeated classical optimization and repeated noisy simulation, which is a genuine cost, but **no reachable source states this as a problem the paper solves** `[inference]`. Of the eleven papers in this census, this is the one where an HPC contribution is least legible from outside the paywall.

**C. SC contribution.**
- *Quantum novelty:* an incremental data-injection encoding for text in quantum circuits, plus noise-aware training across a heterogeneous mixture of ansätze. `[abstract]`
- *HPC novelty:* `NOT_FOUND`.
- *Category* `[inference]`, tentative: **end-to-end system** and **algorithm–architecture co-design**. I deliberately do **not** claim workload characterization or performance model, which would require the full text.

**Core mechanism** `[abstract]`. Text is encoded into a circuit incrementally — injected at multiple points rather than in one up-front encoding block — and a classifier is trained over a deliberately heterogeneous set of ansätze trading expressibility against depth, selected with noise awareness. The encoding mechanics, loss, optimizer, and how the circuit mixture combines at inference are all `NOT_FOUND`.

**Evaluation.** Classical hardware `NOT_FOUND`. Real QPU `NOT_FOUND` — the abstract's *"ideal and noisy environments"* does **not** distinguish a noisy simulator from a real device and must not be read as either. Simulator `NOT_FOUND`. Qubit counts, depth, gate counts `NOT_FOUND`. Datasets: Yelp, IMDB, Amazon, plus synthetic QNLP datasets `[abstract]`; sizes and splits `NOT_FOUND`. Baseline `NOT_FOUND` — no competing QNLP method (lambeq/DisCoCat or otherwise) is named. Metrics `NOT_FOUND`. Speedup claims: none available. Scaling `NOT_FOUND`.

**Why an SC paper?** `[inference]` On available evidence its fit rests on being an application paper in SC24's Post-Moore topic area — a full application pipeline mapped onto a constrained emerging architecture — rather than on scale, parallelism or system design. The committee clearly valued it (Best Student Paper Finalist), but the SC-specific hook visible from outside is application-to-architecture co-design.

**Counterfactual** `[inference]`. Hardest of the eleven to answer honestly, because **no separable HPC contribution can be identified to remove.** My reading: *unclear, leaning "it already is the quantum-only version."* That is itself the census-relevant answer — SC24 accepted at least one quantum paper whose HPC contribution is not externally legible.

**Why it matters for Quantum-HPC.** It stakes out NLP — the workload currently driving classical HPC procurement — as a quantum application target, with device noise treated as a first-class design constraint. Its opacity (closed access, no preprint, no artifact) is also a data point on reproducibility norms in SC's quantum corner.

**Artifact.** `NO_PUBLIC_ARTIFACT_FOUND`. Searched: Goodwill Computing Lab open-source page (21 artifacts listed spanning HPDC'19–HPCA'26; **LEXIQL absent**), the lab publications page (empty `[Artifact]()` placeholder), `github.com/GoodwillComputingLab`, `github.com/positivetechnologylab` (24 repos, none matching; 8 plausible names probed by `git ls-remote`, all 404), Tirthak Patel's publications page, Zenodo, HuggingFace. GitHub search for "LexiQL" returns only an unrelated GraphQL tool.

---

### 3.2 Optimizing Quantum Fourier Transformation (QFT) Kernels for Modern NISQ and FT Architectures

**Bibliographic.** Yuwei Jin, Minghao Guo, Henry Chen, Fei Hua, Eddy Z. Zhang (Rutgers); Xiangyu Gao (NYU); Chi Zhang. SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing I*. DOI `10.1109/SC41406.2024.00074`, pp. 1–15. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q`. Branch: compiler / circuit mapping.
**Content source: arXiv:2408.11226v1 preprint** — published version may differ.

**Research question** `[paper]`. Can hardware-compliant QFT circuits with *provably linear depth* be constructed directly for Google Sycamore, IBM heavy-hex, and fault-tolerant lattice surgery, eliminating the combinatorial mapping search that SAT-based compilers and heuristic routers currently perform?

**A. Quantum problem** `[paper]`. QFT is built from controlled-phase gates over all qubit pairs — effectively all-to-all connectivity — while real devices have sparse 2D nearest-neighbour topologies. Bridging the gap needs SWAP insertion, which inflates depth and gate count; and because backends differ and QFT size varies, every configuration demands recompilation with inconsistent quality.

**B. HPC problem** `[paper]`. **Strong and explicit — this is the paper's real SC hook.** Qubit mapping is a combinatorial search whose space explodes with qubit count. The paper reports **SATMAP timing out at 2 hours in most cases** (439.79 s even for a 2×5 heavy-hex instance) and SABRE's compile time growing 0.28 s → 55.26 s across their range while producing suboptimal depth. The move is to eliminate the search: use **program synthesis (SKETCH), offline and once**, to discover a parameterized affine movement pattern that provably satisfies the CPHASE dependency specification, then instantiate it analytically at any N. Their own statement: *"Our method does not have compilation time as it is an analytical approach."* This is the classical HPC pattern of replacing a runtime search with a closed-form tuned kernel — the QFT analogue of a hand-tuned BLAS routine — and it is what lets them reach 1024 qubits where solvers cannot reach 30.

**C. SC contribution.**
- *Quantum novelty:* first constructions guaranteeing **linear-depth QFT** on Sycamore, heavy-hex and lattice surgery, enabled by two insights — **relaxed ordering** (CPHASE gates are diagonal and commute, so "Type I" dependencies can be broken while "Type II" are preserved) and **sub-kernel partitioning** (recursive decomposition into units, reusing known linear-nearest-neighbour solutions inside units).
- *HPC novelty:* replacing solver-based compilation with synthesized closed-form affine mapping schedules — zero compile time, unbounded scalability, deterministic quality — plus exploitation of **heterogeneous link cost** in the FT backend (diagonal SWAP = 2 CNOTs / depth 2; horizontal or vertical = 3 CNOTs / depth 6), which is a latency-aware scheduling optimization.
- *Categories:* **algorithm–architecture co-design** (primary), **performance model** (closed-form asymptotic depth bounds), **scheduling algorithm**, **scalability study**.

**Core mechanism** `[paper]`. QFT is treated not as an arbitrary circuit to be routed but as a structured kernel whose regularity mirrors the hardware's. CPHASE commutativity relaxes the dependency graph so qubits sweep past one another in a fixed repeating movement pattern instead of an ad-hoc SWAP schedule. The N-qubit problem is recursively partitioned into units; inside a unit the known LNN linear-depth solution applies, and between units a synchronized movement pattern brings every cross-unit pair into adjacency exactly once. SKETCH synthesizes the *parameters* of that pattern as affine loops, checked against a formal specification that every required CPHASE executes and every preserved dependency holds. Architecture instantiations: heavy-hex decomposes into a main line plus dangling vertices (5N + O(1) cycles); Sycamore pairs adjacent rows into units meeting through diagonal links (7m² + O(m) = 7N + O(√N)); lattice surgery treats each grid row as a unit with paired SWAP layers ordered to exploit cheap diagonal links (5m² + O(1) = 5N + O(1)).

**Evaluation** `[paper]`.
- Classical hardware: `NOT_FOUND` — no CPU, RAM, node count or cluster named.
- Real QPU: **no**. Analysis and simulation only; their own simulator is used **only to verify mapping correctness**, not to model noise.
- Problem scale: NISQ backends to **100 qubits**; lattice surgery to **1024 qubits** (m=32). Reported points include Sycamore 6×6 (depth 208, SWAPs 540), heavy-hex 6×5 (depth 139, SWAPs 360), lattice surgery 30×30 (depth 4446, SWAPs 208800).
- Baselines: **LNN** (Maslov), **SATMAP**, **SABRE**. **Versions `NOT_FOUND` for all three**; no Qiskit version stated.
- Metrics: circuit **depth**, **SWAP count**, **compilation time**. **No fidelity, no success rate, no error rate, no noise model** — a notable omission for a paper targeting NISQ.
- **Headline claim in full context:** *"up to 53% in SWAP gate and 92% in depth"* reduction vs **SABRE**, same QFT benchmark, same target architecture, same qubit count. **This is a circuit-quality ratio, not a wall-clock speedup** — no runtime, no hardware, no precision, no communication is involved. Per-architecture: Sycamore ~50% lower depth / ~20% fewer SWAPs; heavy-hex depth 24% and SWAPs 48% of SABRE's.
- Compile time: their method is analytic (none); SATMAP mostly times out at 2 h; SABRE 0.28–55.26 s. **`CONTEXT_NOT_STATED`** — the machine on which the SATMAP and SABRE timings were measured is not reported, so the compile-time comparison has no stated hardware context.
- Scaling: neither strong nor weak. What is presented is an **asymptotic scalability study** of depth and SWAP count vs qubit count, backed by proven bounds.

**Why an SC paper?** Partly argued by the paper itself `[paper]`: the incumbents are a solver that does not scale and a heuristic that scales but degrades, and the fix is a domain-specific architecture-specific kernel with a closed-form cost model, demonstrated at 1024 qubits. That is the SC idiom — optimize the most important kernel for the machine you actually have and prove its cost. The heterogeneous-link-latency optimization is recognizably latency-aware scheduling.

**Counterfactual** `[inference]`. **Probably not.** Stripped to "we found a linear-depth QFT construction," this is quantum-circuit theory belonging at QIP/QCE or a quantum journal. The compile-time-scalability framing, the analytic performance model, and treating QFT as a per-architecture tuned kernel are what make it SC-shaped — though it would remain publishable at ASPLOS/MICRO-class venues.

**Why it matters for Quantum-HPC.** It establishes that for structured high-value quantum kernels the right answer may be a hand-derived architecture-specific mapping with a proven cost model — **a kernel library, not a general compiler.** That transfers directly to a future quantum-HPC software stack, where compile time sits on the critical path of hybrid loops and where per-backend tuned kernels for QFT, QPE and arithmetic primitives would play the role BLAS plays today.

**Artifact.** `PUBLIC_CODE` — **https://github.com/XiangyuG/qft_on_regular_architectures** (owner `XiangyuG` = second author Xiangyu Gao). README first line: *"This is the AD/AE for the paper (Optimizing Quantum Fourier Transformation (QFT) Kernels for Modern NISQ and FT Architectures)"* `[documentation]`.
**Cross-check verdict: `CONSISTENT`.** `[code]` All three architectures have their own generator — `Googlesycamore_qft.py` (m×m grid), `heavy_hex_qft.py`, `lattice_sugery_qft_mix.py` (27 KB, with `unit_size`/`unit_count`, `SWAP_gate_implementation`, `logical_unit_swap`). `Googlesycamore_qft.py` implements LNN / reverse-LNN / USWAP with explicit `swap_total` accounting, matching the paper's SWAP-count and depth metrics. The SABRE baseline is present at `AE/sabre/sabre_qft.py`, parameterized for `"N*N"`, `"sycamore"`, `"heavy-hex"`; `fig_gen/csv_data/` holds 15 result CSVs split by architecture and by ≤100 / ≥100 qubits, matching the paper's figure structure. No MPI or GPU code — correctly so for a compiler paper. **One small discrepancy** `[inference]`: the preprint cites this URL only as *"Simulator to verify the QFT qubit mapping output"*, but no statevector simulator is present in the repo; the repo is the full AD/AE, which the paper's own description understates.

---

### 3.3 On the Efficacy of Surface Codes in Compensating for Radiation Events in Superconducting Devices

**Bibliographic.** Marzio Vallero, Gioele Casagranda, Flavio Vella, Paolo Rech (University of Trento). SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing I*, **Best Student Paper Finalist** `[official-program]`. DOI `10.1109/SC41406.2024.00075`, pp. 1–15. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q` + `FUTURE_WORKLOAD`. Branch: QEC / reliability characterization.
**Content source: arXiv:2407.10841v1 preprint** — published version may differ.

> **Note on discovery.** This paper's title contains **neither "quantum" nor "qubit"**. It was caught only by the `surface code` and `supercondu*` sweep patterns. It is the concrete demonstration that a title-only "quantum" search under-counts SC.

**Research question** `[paper]`. How resilient are real surface-code implementations to radiation-induced faults, and can the choice and tuning of the code — distance, family, qubit roles, device topology — raise the probability of correcting such an event **without adding any qubit overhead**?

**A. Quantum problem** `[paper]`. A particle strike generates electron–hole pairs in the substrate, breaking Cooper pairs into quasiparticles that decay into long-lived phonons spreading energy isotropically. The result is a **spatially correlated, long-lasting, multi-qubit decoherence event**: *"Any particle interaction can alter the qubit(s) state, forcing them into a decoherent state for long periods of time (up to 100s of seconds)"*, occurring *"every tens of seconds, several orders of magnitude greater than in CMOS transistors."* Where CMOS faults last nanoseconds, qubit effects last 25 ms to >100 s. QEC assumes largely independent errors; a correlated burst attacks exactly the assumption surface codes rest on.

**B. HPC problem.** **Present in scale, absent as an engineered contribution — and this is the paper's most important census finding.** The measurable computational problem is a **Monte-Carlo fault-injection campaign of over 400 million injections** across two code families, a range of distances, every impact location, 10 discretized time samples per event, >12 configurations and seven device topologies, with an MWPM decode on every shot. That is a large, embarrassingly-parallel, decode-bound campaign.

**However** `[paper]`: the preprint reports **no HPC hardware, no parallelization strategy, no wall-clock time, no throughput figure, and no MPI or GPU usage.** The only occurrence of "supercomputer" is a *comparison*: *"The whole Titan supercomputer (composed of 14,000 nodes) has an error rate in the order of one error every few hours."* The single place cost shapes a design decision is the note that more temporal samples "comes at the expense of computational overhead," which is why they settled on 10. **The honest characterization: the HPC content is methodological lineage — large-scale fault injection, the standard HPC-resilience technique — rather than a systems-performance contribution.**

**C. SC contribution.**
- *Quantum novelty:* a physically-grounded spatio-temporal radiation fault model injected into surface-code circuits, and the first large-scale quantitative mapping from *physical* radiation faults to *post-decoding logical* error rates across code families, distances, qubit roles and topologies. Practical finding: tuning the code raises radiation-fault correction probability by **up to 10% at zero overhead**.
- *HPC novelty:* **weak.** No parallel algorithm, no memory or communication optimization, no performance model of the simulation itself. The transplant of HPC-resilience fault-injection methodology into QEC is the genuine — but methodological, not performance — contribution `[inference]`.
- *Categories:* **workload characterization** (more precisely reliability characterization) as primary; **scalability study** in the sense of sweeping distance and topology; **other:** a fault-injection model and toolkit.

**Core mechanism** `[paper]`. The device is an undirected **architecture graph** of qubit couplings. A radiation event is the product of temporal decay and spatial damping: `T(t) = e^{−γt}` with γ=10 at 10 equidistant samples, and `S(d) = n²/(d+n)²` with n=1 where d is graph distance from impact; per-qubit fault probability is `F(t,d) = T(t)·S(d)`. Injection **appends a non-unitary reset to each gate acting on an affected qubit with probability p_qi** — a decoherence-style fault, deliberately distinct from the unitary Pauli errors of the standard depolarizing model, which is retained at p = 1% as the intrinsic-noise baseline. Repetition codes (up to distance (15,1)) and XXZZ codes (up to (5,5)) run on a 5×6 base lattice; the logical operation is an X gate on |0⟩ expecting |1⟩, with syndromes decoded by **MWPM** via Qiskit Topological Codes. A logical error is counted whenever the decoder returns |0⟩.

**Evaluation** `[paper]`.
- Classical hardware: `NOT_FOUND` — no CPU, GPU, node count or cluster named, **despite 400M injections**.
- Real QPU: **no**. Simulation only. Simulator: Qiskit + Qiskit Topological Codes; **versions `NOT_FOUND`**.
- Problem scale: **>400 million fault injections**; repetition to (15,1), XXZZ to (5,5); 5×6 base lattice; 100 ms simulated event duration; 10 temporal samples; >12 configurations; topologies linear, mesh, Brooklyn, Cairo, Cambridge, Almaden, Johannesburg. **Shots per configuration `NOT_FOUND`** — the paper does not show how the 400M decomposes.
- Baseline: the **intrinsic depolarizing model at p = 1%** plus cross-comparison among families, distances and topologies. **There is no competing tool or prior method as a baseline** — this is a characterization study, not a "we beat X" study.
- Metrics: post-decoding logical error rate.
- Claims in context: **"up to 10%"** improvement in radiation-fault correction probability *"by simply selecting and tuning properly the surface code, thus without introducing any overhead."* Up to 7% (repetition) and 9% (XXZZ) attributable to topology. Logical error at impact (t=0): repetition-(5,1) ≈27% average, peak 48%; XXZZ-(3,3) ≈50% average, peak 54%. **Distance inversion — the paper's most consequential result:** repetition-(3,1) ≈8% vs repetition-(13,1) ≈20.5%, i.e. **larger code distance performs *worse* under a correlated radiation event**, the opposite of the independent-error intuition. Topology comparison at distance (11,1)/(3,3): linear 15–17%, mesh 16–22%, Brooklyn ≈19%, Cambridge/Johannesburg 17–27%, Cairo 21–23% (worst). All figures are same-simulator, same-noise-model comparisons; `CONTEXT_NOT_STATED` for compute context because there is none to state.
- Scaling: **neither.** No speedup or efficiency measurement of any kind. What scales is the parameter space, not the computation.

**Why an SC paper?** The paper argues part of this itself `[paper]`, framing qubit reliability as the successor to HPC system reliability — benchmarking explicitly against Titan's error rate and CMOS soft-error behaviour. `[inference]` Beyond that the fit is methodological and communal: fault-injection campaigns, physical-to-logical error extrapolation, and radiation-effects characterization are the native vocabulary of SC's resilience community, and Rech's group brings that lineage directly from CPU/GPU radiation testing. **The SC fit is methodology and community, not compute scale** — nothing in the text says this could not have run on a workstation.

**Counterfactual** `[inference]`. Close to already being "the quantum-only version," since no separable HPC-performance contribution exists to remove. Honest answer: **yes, it plausibly still lands at SC** — for a reason worth recording: **SC's resilience tradition accepts characterization-by-fault-injection as a contribution in its own right, independent of parallelism or performance.** Strip the HPC-resilience framing (Titan comparison, CMOS lineage, injection-campaign methodology) and it becomes a QCE or DSN paper.

**Why it matters for Quantum-HPC.** Correlated long-duration radiation faults break the independence assumption underlying all surface-code threshold arguments, and the distance inversion shows the practical consequence. Any future quantum accelerator sited in an HPC facility inherits this as a facility-level reliability problem, exactly as neutron-induced soft errors did for large GPU systems.

**Artifact.** `NO_PUBLIC_ARTIFACT_FOUND`. The preprint promises one: *"We translate this model into a flexible and easy-to-use quantum fault injection toolkit, which is part of our contribution and will be disclosed as open-source code [39]"* — but **reference [39] reads verbatim: "T. B.D. (2024) Repository name. To be disclosed after peer review."** `[paper]` It has not been disclosed since. Searched `github.com/MarzioVallero` (11 repos, none matching), the lab org `QuTAM` (3 repos: `QuFI`, `DSN2022_QuFI_Data`, `IOLTS2022_QC_Cutting_Data`), Zenodo, the HiCREST/Trento lab site, and a 2026 follow-up (arXiv 2602.06202, no code statement).
**Warning against false attribution** `[inference]`: `QuTAM/QuFI` belongs to the **DSN 2022** paper *"QuFI: a Quantum Fault Injector…"*, not to this SC24 paper, and the SC24 work uses a different stack. Do not cite it as this paper's artifact.

---

### 3.4 PARALLAX: A Compiler for Neutral Atom Quantum Computers under Hardware Constraints

**Bibliographic.** Jason Ludmir, Tirthak Patel (Rice University). SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing II*. DOI `10.1109/SC41406.2024.00079`, pp. 1–17. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q`. Branch: compiler / scheduling + throughput.
**Content source: arXiv:2409.04578v1 preprint** — published version may differ.

**Research question** `[paper]`. How can arbitrary circuits be compiled onto neutral-atom machines with **zero SWAP gates**, while satisfying AOD movement constraints, minimum atom separation and the Rydberg blockade — in polynomial time, at scales where SMT-based compilers cannot finish at all?

**A. Quantum problem** `[paper]`. Neutral-atom machines trap qubits in static SLM traps and mobile AOD traps and permit physical atom movement instead of SWAP-based routing. But movement is heavily constrained: atoms must never approach closer than a minimum separation; *"AOD rows/columns cannot cross over each other, meaning the relative order of the rows and columns must be maintained"*; and *"Qubits on an AOD row/column have to move in tandem."* Concurrently the **Rydberg blockade** (radius ≈2.5× the interaction radius) forbids exciting neighbouring non-participating atoms, throttling gate parallelism. The cost asymmetry motivating everything: a SWAP is three CZs at ≈1.43% cumulative error, whereas movement carries <0.1% atom loss and is far faster.

**B. HPC problem** `[paper]`. **The strongest and most explicit of the SC24 cohort.** Three distinct systems problems:
1. **Compilation search-space explosion.** The exact SMT approach **DPQA** *"cannot compile even small 9-16 qubit circuits within 24 hours."* PARALLAX replaces it with a heuristic pipeline of stated complexity **O(q⁵ + gq² + a²q² + ga²s + ga³)** — polynomial, dominated by the O(q⁵) placement term.
2. **Hardware utilization / throughput.** A 9-qubit circuit on a 1,225-atom machine wastes essentially the whole device. PARALLAX **replicates the compiled circuit spatially across the array**, sharing AOD rows and columns so all copies move in lockstep, executing many *logical* shots per *physical* shot — up to **121 copies** for a 9-qubit circuit — yielding a **97% average reduction** in total time to complete 8,000 logical shots. This is an occupancy/data-parallelism argument, structurally identical to batching on a GPU.
3. **Movement scheduling and obstruction resolution.** A blocked atom path triggers **recursive displacement** of obstructing atoms, bounded at 80 iterations.

**C. SC contribution.**
- *Quantum novelty:* *"the first heuristical compilation method to have zero SWAP gates and parallelize circuit executions while facilitating atom movements and satisfying nontrivial hardware constraints."* The key structural trick is **placing only one atom per AOD row/column pair**, which dissolves the tandem-movement constraint and collapses collision avoidance.
- *HPC novelty:* (a) a polynomial-time heuristic replacing an exponential SMT formulation, completing where DPQA and ELDI time out at 24 h; (b) **logical-shot replication as a throughput optimization** — spare hardware capacity amortizing per-shot overhead, an occupancy argument imported wholesale from classical accelerator practice; (c) a layered gate scheduler with randomized tie-breaking and recursive obstruction resolution.
- *Categories:* **scheduling algorithm** (primary), **algorithm–architecture co-design**, **end-to-end system**, plus **other: throughput/occupancy parallelization**.

**Core mechanism** `[paper]`. Four to five stages. **(1) Placement:** the circuit becomes a graph with qubits as nodes and gate counts as weighted edges; Graphine's dual-annealing optimizer places qubits so frequently-interacting pairs sit close. The plane is **discretized so one unit equals twice the minimum separation plus padding**, making legal spacing structural rather than checked. **(2) AOD selection:** a weighted heuristic picks mobile atoms — weight 0.99 on out-of-range interaction count, 0.01 on Rydberg-blockade interference degree — subject to **one atom per AOD row/column pair**, with recursive nudging to resolve row/column collisions. **(3) Scheduling:** layer by layer, at most one gate per qubit respecting dependencies; for a CZ whose atoms are out of range, move the AOD-trapped atom into range; if neither is in an AOD, fall back to trap-switching (100 µs, needed for only **1.3% of CZ gates**); if the path is obstructed, *"the system will recursively move that obstructing atom out of the way"* up to 80 iterations. Gates are **randomly shuffled before blockade checking** so *"one qubit [doesn't get] arbitrary execution preference over the others."* After each layer, AOD atoms return to their pre-layer positions by reversing movement vectors. **(4) Replication:** the compiled circuit is copied across the full array, all copies sharing AOD rows and columns so one synchronized movement schedule drives every copy.

**Evaluation** `[paper]`.
- Classical hardware (for compilation): *"a local research cluster with Ubuntu 22.04.2 LTS on a 32-core 2.0 GHz AMD EPYC 7551P processor with 32 GB RAM."* **Effectively a single node. No GPU.** This is the only SC24 quantum paper that names its compilation machine.
- Real QPU: **no**. *"PARALLAX's evaluation is conducted via a simulator that emulates the hardware characteristics of real neutral atom testbed systems."* Simulated machines: QuEra **Aquila, 256 qubits** (16×16) and Atom Computing's **1,225-qubit** system (35×35).
- Software: Python 3.11.5, **Qiskit 0.45.0**, **SciPy 1.11.3**.
- Problem scale: 18 algorithms, **9–128 qubits** — ADD, ADV, HLF, KNN, MLT, QAOA, QFT (9–10); GCM, HSB, QEC, SECA (13–17); SQRT, WST, VQE (18–28); QV (32); QGAN (39); TFIM (128).
- Baselines: **ELDI, GEYSER, GRAPHINE, DPQA**. **ELDI and GRAPHINE were modified by the authors "to make them hardware-compatible"** — worth flagging, since the baselines are not run as published. **Versions `NOT_FOUND`.**
- Hardware model (Table II): U3 error 0.0127%, CZ error 0.48%, SWAP error 1.43%, readout 5%, atom loss 0.7%, T1 4.0 s, T2 1.49 s, U3 2 µs, CZ 0.8 µs, trap switch 100 µs, AOD speed 55 µm/µs.
- Claims in full context: **39% fewer CZ gates vs GRAPHINE, 25% fewer vs ELDI** (average over 18 benchmarks, same simulated hardware and noise model — a circuit-quality ratio). **46% higher success probability vs GRAPHINE, 28% vs ELDI**, *"while achieving similar runtimes on average."* Best case (QV, 32 qubits): 67% CZ reduction vs ELDI, 87% vs GRAPHINE. **The 97% average execution-time reduction is PARALLAX-with-replication versus single-copy execution for 8,000 logical shots on the same simulated 1,225-atom machine** — it is *not* measured against a competitor's parallelization, and it is a **simulated** execution-time model built from the Table II timing parameters, not a measured wall-clock. DPQA could not compile 9–16 qubit circuits within 24 h; ELDI failed on VQE within 24 h. **PARALLAX's own per-benchmark compile times: `NOT_FOUND`.**
- Scaling: **neither** strong nor weak in the classical sense. There is a throughput/occupancy scaling argument (replication count vs array size) and a formal complexity analysis.

**Why an SC paper?** Argued substantially by the paper `[paper]`: prior exact compilers do not scale (DPQA's 24-hour failures), and replication *"effectively address[es] scalability issues of atom movement by maximizing the utilization of the system's hardware."* Both are SC arguments — polynomial-vs-exponential compilation cost, and utilization of an expensive shared machine. `[inference]` The shot-replication result is the most legibly-HPC contribution in the SC24 cohort: it is batching for occupancy on an accelerator, transplanted to atoms.

**Counterfactual** `[inference]`. **Probably not.** Without the compile-time-scalability argument and shot parallelization, PARALLAX is a neutral-atom mapping-and-routing compiler — an excellent fit for MICRO, ASPLOS or IEEE QCE, all of which regularly publish exactly this. The 97%-via-121-parallel-copies result is what converts it into a recognizably SC paper.

**Why it matters for Quantum-HPC.** Neutral atoms are the most plausible near-term path to thousand-qubit arrays, and PARALLAX shows the compiler — not the hardware — currently determines both fidelity (via SWAP elimination) and throughput (via occupancy). **"A large machine running a small circuit should run many copies of it"** is the quantum analogue of batching, and it will matter the moment quantum devices become shared scheduled resources inside HPC centres, where per-shot overhead and utilization drive cost.

**Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — **https://github.com/positivetechnologylab/Parallax**, Zenodo `10.5281/zenodo.12587550`. README: *"This repository contains the open-sourced artifacts for PARALLAX, which will appear at… SC 2024"* `[documentation]`; the preprint states the URL directly.
**Cross-check verdict: `CONSISTENT`.** `[code]` `na_arch.py` models exactly the constraints the title names — classes `AOD_Atom`, `Row`, `Column`, `AODGrid`, `NA_Architecture(grid_dims, array_dims, qubit_topology, connect_count, radius, qasm_str)` with `self.radius = radius #Rydberg interaction radius`, and methods `adjust_overlapping_rows` / `adjust_overlapping_columns` / `move_empty_rows_cols_out_of_frame` enforcing AOD row/column ordering and non-crossing. `mobile_qubits.py::select_mobile_qubits(...)` implements the SLM-vs-AOD partition weighted by `qubit_edge_counts`, `interference_count` and distance — the paper's core placement decision. **Both baselines are in-repo**: `graphine.py` + `graphine_discretized_compilation.py`, and a vendored `neutral-atom-compilation/` (ELDI) with `eldi_compile.py`. `run_baseline.py` / `run_parallel.py` / `run_aod_ablation.py` map to Figs 9–11 per the README. `benchmarks/` contains 18 QASM circuits including `tfim_128.qasm`, `qugan_n39`, `vqe_uccsd_n28`, `qv_32`.

---

### 3.5 Surpassing Sycamore: Achieving Energetic Superiority Through System-Level Circuit Simulation

**Bibliographic.** Rong Fu, Zhongling Su, Han-Sen Zhong, Xiti Zhao, Jianyang Zhang (Shanghai AI Lab); Feng Pan (USTC); Pan Zhang (CAS); Xianhe Zhao, Ming-Cheng Chen, Chao-Yang Lu, Jian-Wei Pan (USTC); Zhilin Pei, Xingcheng Zhang, Wanli Ouyang (Shanghai AI Lab). SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing III*. DOI `10.1109/SC41406.2024.00085`, pp. 1–20. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q`. Branch: tensor-network simulation.
**Content source: arXiv:2407.00769v1**, titled *"Achieving Energetic Superiority Through System-Level **Quantum** Circuit Simulation"* — **note the title differs from the published version.** Published version may differ further.

**Research question** `[paper]`. Can a classical GPU supercomputer generate 3×10⁶ **uncorrelated** bitstring samples from Google's 53-qubit, 20-cycle Sycamore random circuit at the same XEB fidelity (~0.002), faster *and* at lower energy than Sycamore itself? Prior classical refutations either produced correlated samples or beat Sycamore only on time, not energy.

**A. Quantum problem** `[paper]`. Random circuit sampling on Sycamore: 53 qubits, 20 full cycles + half cycle, √X/√Y/√W single-qubit gates and parameterized fSim two-qubit gates. Samples must be at target linear XEB ≈ 0.002 **and statistically uncorrelated** — the paper explicitly flags that earlier work's samples *"exhibit significant correlations among them, thus not considered as faithfully simulating the Sycamore quantum processor."*

**B. HPC problem** `[paper]`. **A tensor-network contraction problem at the memory wall; essentially every difficulty is a systems difficulty.**
- **Contraction-order / memory tradeoff.** Contraction FLOP complexity is roughly inversely proportional to the maximum allowed intermediate-tensor memory (explored 64 GB → 2 PB). A bigger memory budget means cheaper contraction — but that budget must be *synthesized* across nodes.
- **Tensor networks exceeding a node.** The working networks are **4 TB and 32 TB** (complex-float); a 32T subtask needs **20 TB per multi-node level**, ~32 nodes' aggregate HBM. A single 80 GB A100 is 250× too small.
- **Inter-node communication dominates.** Distributing a "stem tensor" across nodes means einsum contractions move slices over InfiniBand (100 GB/s unidirectional), ~3× slower than intra-node NVLink (300 GB/s).
- **Kernel gap.** PyTorch has no complex-half einsum; naive fp32 doubles memory and forgoes fp16 tensor cores.
- **Energy as a first-class objective** — unusual: the optimization target is joules, not only seconds.
- **Sparse-state memory blowup** in the final contraction stages, where one tensor exceeds GPU memory.

**C. SC contribution.**
- *Quantum novelty:* modest-to-moderate. The contraction-order search and slicing come from prior work by co-author Feng Pan et al.; the genuinely quantum-algorithmic piece is the **post-processing / post-selection scheme** extracting uncorrelated top-*k* bitstrings from a small subspace, cutting the number of subtasks that must be computed by 6–16×.
- *HPC novelty:* the paper's weight. A three-level (global / multi-node / device) decomposition co-designed to the NVLink-vs-InfiniBand bandwidth hierarchy; a **custom complex-half-precision einsum kernel**; **int4 quantization applied only to inter-node communication**; a recomputation scheme trading FLOPs for halved node count; sparse-state chunked contraction; NVML-instrumented energy accounting; scaling to 2,304 A100s at 561 PFLOPS peak half-precision.
- *Categories:* **end-to-end system** + **communication reduction** + **GPU kernel/acceleration** + **memory optimization** + **algorithm–architecture co-design**; secondary **scalability study**.

**Core mechanism** `[paper]`. The circuit becomes a tensor network whose optimal contraction path is found under an explicit memory budget, exploiting the inverse relation between allowed memory and contraction complexity — so they deliberately choose *huge* (4 TB / 32 TB) networks to minimize total FLOPs, then build the system to hold them. The network is sliced into independent subtasks (2¹⁸ for 4T, 2¹² for 32T), embarrassingly parallel at the **global level**. At the **multi-node level** a large stem tensor is split along its first N_inter modes across nodes (32 nodes per subtask for 32T, holding 20 TB); at the **device level** the remaining N_intra modes split across 8 GPUs over NVLink. A hybrid communication algorithm chooses the N_inter/N_intra split from measured bandwidths so expensive InfiniBand traffic is minimized. Inter-node transfers are **int4-quantized (group size 128)**, cutting communication time by over 85%; at the chosen operating point this cost 6.55% relative fidelity for a 50.08% time reduction and 30.23% energy reduction. A custom complex-fp16 einsum extension halves memory and enables fp16 tensor cores, and a recomputation trick computes tensor halves sequentially to halve nodes per subtask. **"System-level" is exactly this global/node/device stack** — the claim is that the algorithm was known but nobody had built a machine-level system able to host a 32 TB tensor network.

**Evaluation** `[paper]`.
- Hardware: NVIDIA **A100 80 GB** (312 TFLOPS FP16 tensor core each), **up to 2,304 GPUs across 288 nodes**, 8 GPUs/node; **NVLink 300 GB/s** intra-node, **InfiniBand 100 GB/s** inter-node; 640 GB HBM per node; peak **561 PFLOPS** half-precision at **16.65–21.09%** achieved efficiency. **Named cluster `NOT_FOUND`**; CPU model `NOT_FOUND`.
- Real QPU: **no**. Sycamore's numbers are taken from Arute et al. 2019, **not re-measured**.
- Framework: PyTorch **2.1**, cuTENSOR **1.7.0**, CUDA **12.0**. Not cuQuantum, not Qiskit.
- Problem scale: Sycamore RCS, **53 qubits, m=20**; tensor networks of **4 TB** and **32 TB**; 3×10⁶ bitstrings.
- **Baseline — unusual and important: there is no software baseline.** The comparison is *against Google's Sycamore QPU* (600 s, 4.3 kWh, cited to Arute et al.). Prior classical simulations are discussed as related work but **no head-to-head same-hardware re-run is reported.**
- Precision: complex half-precision (fp16) with some fp32; **int4** for inter-node communication.
- Verified results (Table 4), all four configurations:

| | 4T no post-proc | 4T post-proc | 32T no post-proc | **32T post-proc** |
|---|---|---|---|---|
| Time complexity (FLOP) | 4.7×10¹⁷ | 7.9×10¹⁶ | 1.3×10¹⁷ | 1.6×10¹⁶ |
| XEB (%) | 0.2036 | 0.2059 | 0.21194 | **0.2158** |
| Subtasks run / total | 528 / 2¹⁸ | 84 / 2¹⁸ | 9 / 2¹² | **1 / 2¹²** |
| A100 count | 2112 | 96 | **2304** | **256** |
| Time-to-solution (s) | 32.51 | 133.15 | **14.22** | **17.18** |
| Energy (kWh) | 5.77 | 1.12 | **2.39** | **0.29** |

- **The energy claim, stated exactly** `[paper]`: *"our best-case without post-processing, we have reduced the time-to-solution to 14.22 seconds, with a power consumption of 2.39 kwh with fidelity of 0.002. Then with the technique of post-processing… we remarkably reduce the time-to-solution for sampling 3×10⁶ bitstrings to just 17.18 seconds, with a power consumption of 0.29 kWh. This represents a one-order-of-magnitude reduction in both time and energy compared to the Google's quantum processor Sycamore."*
  - Comparison is **against the Sycamore QPU**, not another simulator. Sycamore reference: **600 s, 4.3 kWh** for 3×10⁶ uncorrelated samples. Ratios: **34.9× time, 14.8× energy** for the 17.18 s / 0.29 kWh row.
  - **What the classical energy budget covers** `[paper]`: NVML power sampling at ~20 ms intervals integrated over runtime, covering GPU + communication power (measured per-A100: idle 60 W, communication 90–135 W, computation 220–450 W). **Not included:** cooling, power-conversion loss, CPU/host power, storage, or datacenter overhead — no PUE factor. **`[inference]`, not a paper disclosure:** verification confirmed the paper contains *no* discussion of PUE, cooling, or host power anywhere, so this exclusion is a sound deduction from an NVML-device-only methodology but **must not be attributed to the authors.** A PUE-corrected number would be roughly 1.3–1.6× higher.
  - **What Sycamore's 4.3 kWh covers: `NOT ITEMIZED` by this paper.** It does not state whether the figure includes the dilution refrigerator or control electronics. **This is the weakest link in the comparison and the thing most likely to be misquoted** `[inference]` — cryogenic overhead dominates a superconducting QPU's real draw, so the two sides are very likely not measured on the same boundary.
  - **A caveat the paper does not foreground:** the 0.29 kWh headline run computed **1 subtask out of 2¹²** (0.024%) on **256 GPUs**, relying on post-selection to produce uncorrelated samples. **Conflating "2,304 GPUs" with "0.29 kWh" is wrong** — the 2,304-GPU figure belongs to the 14.22 s / 2.39 kWh row.
  - Sycamore's own XEB is **not restated** for side-by-side comparison.
- Scaling: **strong scaling** reported, 32T configuration, **256 → 2,304 GPUs**, with energy roughly constant as node count grows (near-linear speedup). No weak scaling. The preprint's node arithmetic is internally inconsistent at one point (256 GPUs annotated "2 nodes"; at 8 GPUs/node this should be 32) — **treat GPU counts as the reliable figures.**

**Why an SC paper?** `[inference]` The scientific claim is quantum-physics content, but everything that makes it true is HPC: a 32 TB distributed tensor network, a bandwidth-hierarchy-aware decomposition, a custom fp16 complex einsum, int4 communication quantization, and NVML energy measurement across 2,304 GPUs. A quantum venue would take the result on faith and skip the system. SC is also the natural home for an energy-to-solution argument. This is a Gordon-Bell-shaped paper.

**Counterfactual** `[inference]`. **No.** Strip the systems layer and this is "we applied a known contraction-order algorithm plus post-selection to Sycamore" — an incremental entry in a crowded refutation literature (Pan/Zhang 2021, Liu et al. Gordon Bell 2021, Kalachev et al.) belonging at a physics venue. The 2,304-GPU system and the energy measurement *are* the paper.

**Why it matters for Quantum-HPC.** It establishes **energy-to-solution as the benchmark axis for quantum advantage claims**, not just time-to-solution — the right framing as HPC centres begin hosting QPUs on a power budget. It also shows classical simulation capability is a moving target driven by systems engineering, so any advantage claim has a shelf life set by supercomputer engineering. The unresolved issue — two energy budgets drawn at different system boundaries — is precisely the measurement-methodology problem the Quantum-HPC community needs to standardize.

**Artifact.** `NO_PUBLIC_ARTIFACT_FOUND`. arXiv 2407.00769 exists in **v1 only** and its full text contains **no code/data availability statement and no repository URL** `[paper]`. Searched all author names and the Shanghai AI Lab / USTC / CAS groups.
**Warning against false attribution** `[inference]`: `github.com/Fanerst/artensor` (Feng Pan) is contraction-order code for a **different paper** — Pan & Zhang, *"Solving the sampling problem of the Sycamore quantum supremacy circuits"* (PRL 2022). It contains none of this paper's distinguishing systems content (no multi-node stem-tensor decomposition, no int4 communication quantization, no complex-fp16 einsum). **Do not cite it as the SC24 artifact.** Publisher AD/AE appendices were unreachable, so an SC24 artifact appendix cannot be positively ruled out.

---

### 3.6 Realizing Quantum Kernel Models at Scale with Matrix Product State Simulation

**Bibliographic.** Mekena Metcalf (HSBC Holdings Plc., Innovation and Ventures, San Francisco); Pablo Andrés-Martínez, Nathan Fitzpatrick (Quantinuum, Cambridge UK). SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing III*. DOI `10.1109/SC41406.2024.00086`, pp. 1–20. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q` + `Q_FOR_HPC`. Branch: MPS / tensor-network simulation; QML application.
**Content source: arXiv:2411.09336v1** (posted Nov 2024, after SC24, so likely close to camera-ready).

> **Attribution precision.** Phase 1 recorded this as a Quantinuum paper. The **first author is at HSBC**, with Quantinuum co-authors; the Zenodo deposit lists Metcalf as Berkeley Lab. Cite it as HSBC + Quantinuum.

**Research question** `[paper]`. Can quantum kernel methods be evaluated at industry-relevant scale — hundreds of features, thousands of training points — by replacing statevector simulation with MPS, and where does the CPU-vs-GPU crossover for that workload lie?

**A. Quantum problem** `[paper]`. A quantum kernel / QSVM (feature counts swept at 15, 50, 100 and 165). Data is encoded by a **Trotterized Ising Hamiltonian evolution** feature map, U(**x**) = (e^{−iH_XX(**x**)}·e^{−iH_Z(**x**)})^r, with single-qubit Z and two-qubit XX Pauli terms on a linear chain, tunable **interaction distance d** and **repetitions r**; one qubit per feature. Kernel entries are fidelities K_ij = |⟨ψ(x_i)|ψ(x_j)⟩|². The open quantum question: does classification quality improve with feature count and dataset size, and does expressivity help or trigger kernel concentration?

**B. HPC problem** `[paper]`. Two quantified difficulties:
- **Statevector memory 2ⁿ is fatal.** 165 features → 165 qubits → 2¹⁶⁵ amplitudes; statevector simulation caps near 40 qubits. MPS replaces this with **O(mχ²) memory and O(mχ³) time** for m qubits at bond dimension χ.
- **Bond-dimension growth is the new cost driver**, and it is set by a *quantum model design choice*. Measured χ runs ~10 at d=2 to ~595–600 at d=12, with per-state memory **0.02 MiB → 106.35 MiB**. Because cost is cubic in χ, the interaction distance d directly sets the HPC bill — and this is where the CPU/GPU crossover comes from, since small χ means small dense linear algebra that A100s cannot fill.
- **Quadratic Gram-matrix work.** 6,400 training points → **~20.5 million inner products**, while only 6,400 circuit simulations are needed. Simulation is linear, kernel evaluation quadratic — so the two scale differently and must be scheduled differently.
- **Load imbalance and a memory-vs-communication tradeoff** in tiling a symmetric Gram matrix across MPI ranks, including asymmetric tile grids.

**C. SC contribution.**
- *Quantum novelty:* moderate — the *scale* is the claim. 165 features and 6,400 training points is stated as well beyond prior work for quantum kernels. Findings: the quantum kernel beats a Gaussian RBF baseline; accuracy improves with feature dimension and training-set size; **increasing circuit depth/expressivity does not help** (AUC 0.898 at r=2 → 0.798–0.844 at r≥8, consistent with kernel concentration). The feature map itself is not new.
- *HPC novelty:* **the weakest of the three SC24 simulation papers, and honestly so.** This is a **characterization** paper, not a new mechanism: an empirical CPU-vs-GPU crossover for MPS quantum-kernel workloads (GPUs win only when χ ≳ 320, i.e. d ≥ 10), two MPI Gram-matrix decomposition strategies with a memory-vs-communication tradeoff, and a scaling extrapolation. No new kernel, no new algorithm, no new runtime. The notable negative-result contribution is **"CPUs suffice"** for practical quantum-kernel workloads.
- *Categories:* **workload characterization** + **scalability study** + **end-to-end system**; secondary, parallel decomposition of the Gram matrix.

**Core mechanism** `[paper]`. Each datapoint's feature vector parameterizes a Trotterized Ising circuit on a chain of m = (number of features) qubits; the state is an MPS whose χ is controlled by SVD truncation, discarding singular values down to Σsᵢ² ≈ 10⁻¹⁶ so truncation error sits at 64-bit floating-point noise. Because χ is bounded by entanglement rather than by 2ⁿ, 165 qubits become tractable. Kernel entries are MPS–MPS inner products at O(mχ³). The Gram matrix is decomposed into tiles (symmetric for training, rectangular for inference) distributed over MPI ranks by two schemes: **"no-messaging"**, where each of O(√k) processes redundantly re-simulates the circuits it needs so no MPS is ever communicated; and **"round-robin"**, where each circuit is simulated exactly once and MPS tensors are passed between ranks — more memory-efficient, and superior whenever communication is cheaper than re-simulation. Asymmetric tile grids are handled by grouping ranks with extra MPI communication for the remainder. Backends are swappable: ITensors.jl on AMD EPYC CPUs, and a custom pytket-cutensornet path on A100s via cuTensorNet.

**Evaluation** `[paper]`.
- Hardware: **NERSC Perlmutter** (named; NERSC award DDR-ERCAP0029782). CPU backend **AMD EPYC 7763**, core count per run `NOT_FOUND`. GPU backend **NVIDIA A100, 2 to 32 GPUs**, 4 GPUs/node → up to 8 nodes; most runs use 4. Interconnect `NOT_FOUND`. MPI rank count `NOT_FOUND` (described only as "k processes").
- Real QPU: **no** — the paper explicitly runs no quantum hardware experiments.
- Framework: Python 3.10; **pytket 1.26.0**; **pytket-cutensornet 0.6.0**; **cuTensorNet/cuQuantum 3.10** as printed; **ITensors.jl 0.3.37** on Julia 1.9.4; scikit-learn 1.4.1.post1; mpi4py 3.1.5.
- Problem scale: **15–165 qubits** (= features; the sweep runs 15, 50, 100, 165); d ∈ {1,2,4,6,8,10,12}; r ∈ {2,4,8,12,16,20}; **χ ≈ 10 → 595**; MPS memory 0.02 → 106.35 MiB per state; training sets 300 / 1,500 / **6,400**, 80/20 split; up to **~20.5M kernel entries**. Dataset: Elliptic Bitcoin (165 features, 46,564 points).
- Baselines: **two, neither a simulator baseline.** (1) ML baseline — classical Gaussian RBF kernel. (2) Systems baseline — ITensors.jl CPU vs pytket-cutensornet GPU, i.e. self-comparison. **No comparison to Qiskit Aer, quimb, cuStateVec, or any other quantum simulator, and no competing quantum-kernel implementation.**
- Metrics: 50 features — Gaussian AUC 0.892 vs quantum kernel (d=4, γ=0.5) **AUC 0.904**. **+2.44% AUC** using 165 vs 100 features at 6,400 samples. Expressivity: r=2 → 0.898; r=4 → 0.900; r≥8 → 0.844 down to 0.798. Runtime: single circuit (100 qubits, d=6, r=2) **~70 s on GPU**; full training run (6,400 samples, 165 qubits, d=1) **~3 hours on 32 GPUs**. **CPU/GPU crossover: GPU advantage appears at d ∈ [8,10], i.e. χ ≳ 320.** Extrapolation (not measured): 64,000 entries in 30 h on 320 GPUs or 15 h on 640 GPUs. Energy, FLOPs, communication volume all `NOT_FOUND`.
- **This paper makes no *competitive* speedup claim against a rival quantum simulator** — unusual for an SC paper, and worth recording. **Do not manufacture one from the 2→32 GPU scaling figure.** *Precision note added at verification:* the CPU side of the crossover is **ITensors**, a third-party Julia tensor-network library, so an external package *is* a comparison point — but it runs the same MPS algorithm, making this an architectural CPU-vs-GPU crossover rather than a competitive claim. The paper itself flags the limit: *"it would not be fair to compare the total runtime of ITensors against pytket-cutensornet on a distributed setting."*
- Scaling: **weak scaling only** (loosely) — Figure 8, **2 → 32 GPUs**, doubling data and GPUs together; MPS simulation time stays constant while inner-product time grows 4× per data doubling (the quadratic term). No strong scaling. Parallel efficiency `NOT_FOUND`.

**Why an SC paper?** Partly argued `[paper]` — it frames itself as removing "obstacles to testing quantum ML at scale," and the scale is only reachable with a DOE leadership allocation. `[inference]` The census-relevant read: SC accepted this as an **HPC-enabled science result plus a workload characterization** — "here is what this quantum workload actually costs on real HPC hardware, and here is where accelerators stop paying off." That is a recognizable SC genre even without a new mechanism. The honest counter-read is that the ML result is the actual contribution and the HPC content is enabling infrastructure.

**Counterfactual** `[inference]`. **Probably not, or at least a much harder sell.** The quantum result alone — a quantum kernel edging out an RBF kernel by 0.012 AUC on one dataset, with depth hurting — is a QML-workshop or journal result, and the margin is thin. What makes it SC-legible is the 165-qubit / 20M-kernel-entry scale on Perlmutter and the CPU-vs-GPU crossover. **Of the SC24 corpus this is the paper whose SC membership depends most on scale-as-contribution rather than mechanism-as-contribution** — a useful boundary case.

**Why it matters for Quantum-HPC.** A clean instance of **classical HPC as the instrument for testing quantum algorithms**: you cannot know whether a quantum kernel is useful at 165 features without a supercomputer, because no QPU can run it and no statevector simulator can either. It also delivers an unfashionable systems finding — **CPUs are sufficient and GPUs only pay off past χ ≈ 320** — pushing back on reflexive GPU acceleration of quantum simulation. And it makes bond dimension the explicit bridge variable between a quantum model-design knob (interaction distance) and an HPC resource decision, exactly the cross-layer parameter Quantum-HPC co-design needs.

**Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — **https://github.com/PabloAndresCQ/qml-cutensornet** (branch/tag `SC24_paper`), Zenodo **`10.5281/zenodo.12568631`** ("SC24 paper publication", 18.5 MB, CC-BY-4.0). The preprint gives both URLs `[documentation]`.
**Cross-check verdict: `CONSISTENT`.** `[code]` **MPI is real and non-trivial**: `main.py`, `main_no_test.py`, `main_track_mem.py` all open with `from mpi4py import MPI` / `MPI.COMM_WORLD` / `Get_rank(), Get_size()`. **Rank decomposition of the Gram matrix** is in `gpu_backend/kernel_state_ansatz.py`: X and Y datasets are chunked per rank, each rank contracts its own MPS chunk (`SimulationAlgorithm.MPSxGate`), then chunks are exchanged. **Both communication styles from the paper are present** — point-to-point (`mpi_comm.send(mps, dest=proc_recv)` / `recv`, and `mpi_comm.sendrecv(mps, dest=(rank-1)%n_procs_in_RR)` for the round-robin cycle) and a collective final reduction (`mpi_comm.reduce(kernel_mat, op=MPI.SUM, root=root)`). GPU path is pytket-cutensornet `Config(truncation_fidelity=1-truncation_error)` on `CuTensorNetHandle`, with bond dimensions tracked via `mps.get_virtual_dimensions(i)`; CPU path is a separate Julia/ITensors backend (`KernelPkg/`, `cpu_backend/`). **The paper's evaluated configurations are present as scripts:** `runs/qml_figures/slurm_scripts/32gpus.sh` (`#SBATCH -N 8`, `-G 32`, `--ntasks-per-node 4`) and `4gpus.sh`, plus `runs/table3/`, `runs/qubit_scaling/`, `runs/crossover/`, each with `run_all.sh`, `to_csv.py` and committed `results.csv`. README makes CUDA-aware MPI explicit and names Perlmutter and GCP as tested platforms `[documentation]`. Reproduction requires manually downloading the Elliptic dataset from Kaggle.

---

### 3.7 Atlas: Hierarchical Partitioning for Quantum Circuit Simulation on GPUs

**Bibliographic.** Mingkuan Xu (CMU), Shiyi Cao (UC Berkeley EECS), Xupeng Miao (CMU), Umut A. Acar (CMU), Zhihao Jia (CMU). SC 2024 main-track regular paper `[proceedings]`, session *Quantum and Approximate Computing III*. DOI `10.1109/SC41406.2024.00087`, pp. 1–17. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `HPC_FOR_Q`. Branch: distributed multi-GPU statevector simulation.
**Content source: arXiv:2408.09055v2, explicitly an "(Extended Version)"** — richer than the SC24 paper. Theorems 1/2/5 and the complexity analysis in particular may be extended-version-only.

**Research question** `[paper]`. How should a Schrödinger-style full-statevector simulator partition a circuit across a multi-node multi-GPU machine so data parallelism is exploited while communication is minimized — and can that partitioning be *derived by optimization* rather than hand-tuned?

**A. Quantum problem** `[paper]`. Exact full-statevector simulation of general circuits: maintain 2ⁿ complex amplitudes and apply gates. Benchmarks are standard algorithmic circuits (QFT, QPE, amplitude estimation, Deutsch-Jozsa, GHZ, graph state, Ising, QSVM, SU2 random ansatz, VQC, W state), 28–36 qubits. The quantum content is essentially *given*: no new quantum algorithm, physics, or approximation. **Atlas is exact — unlike the other two SC24 simulation papers there is no fidelity or truncation knob.**

**B. HPC problem** `[paper]`. **The cleanest pure-systems problem in the whole census.**
- **2ⁿ amplitudes exceed one GPU.** A 40 GB A100 holds ~2²⁸ complex amplitudes; anything larger must be sharded. Each GPU holds 2^L amplitudes, each node's DRAM 2^(L+R), and 2^G nodes span the rest.
- **Gate locality determines communication class.** Cost depends entirely on *which* qubit index a gate touches: **local qubits** (first L) need no communication; **regional qubits** (next R) need intra-node inter-device transfers; **global qubits** (final G) need inter-node transfers. The optimization problem is therefore choosing the qubit→physical-index mapping.
- **Non-local gates force all-to-all.** Changing the local/global assignment mid-circuit requires permuting and re-sharding the whole statevector. Communication dominates beyond a single node.
- **Kernel granularity tradeoff.** Fusing gates into one matrix costs 4^k work but amortizes memory traffic; running gates one-by-one from shared memory avoids the blowup but pays per-gate overhead. The optimum is circuit-dependent.
- **Arithmetic intensity is terrible** — measured ~0.5 on real circuits — so this is memory- and communication-bound, not FLOP-bound.
- **Capacity beyond aggregate GPU memory** requires DRAM offloading with swap scheduling.

**C. SC contribution.**
- *Quantum novelty:* **essentially none, deliberately.** No new quantum algorithm, no approximation, no physics. Atlas simulates the same circuits everyone else does, exactly. **For the census this is the single most valuable data point: SC accepted a quantum-titled paper whose quantum novelty is zero and whose entire contribution is compiler/systems.**
- *HPC novelty:* high and specific — replacing heuristic partitioning with **provably optimal combinatorial optimization at two levels**: (i) a **binary ILP** that stages the circuit, proven (Theorem 1) to return the *minimum* number of stages; (ii) a **dynamic program** for kernelization within a stage, proven (Theorem 2) to preserve topological equivalence, with complexity bound O((3.2n/ln n)^n · |C|) (Theorem 5). Plus a two-level memory hierarchy (GPU / node-DRAM / cluster) with Legion-based DRAM offloading, and a cost model with an explicit inter-node penalty weight (c=3) letting the ILP trade intra- against inter-node traffic.
- *Categories:* **new parallel algorithm** + **communication reduction** + **scheduling algorithm** + **memory optimization** + **end-to-end system**, with a performance/cost model underneath.

**Core mechanism** `[paper]`. The hierarchy is both a *memory* and a *partitioning* hierarchy. Each GPU holds 2^L amplitudes; each node's DRAM 2^(L+R) (regional); the cluster spans 2^G nodes (global). A circuit is cut into **stages**, and each stage's gates grouped into **kernels**; every stage carries its own qubit→physical mapping.

*Staging (ILP).* A stage is a contiguous subcircuit in which *"all non-insular qubits of all gates can only operate on local physical qubits"* — within a stage **every gate is communication-free** and each shard simulates independently on one GPU, pushing all communication to stage boundaries. Choosing stages is a **binary ILP**: minimize Σ_k Σ_q (S_{q,k} + c·T_{q,k}) where S and T count local- and global-qubit remappings between consecutive stages, with **c = 3** weighting inter-node above inter-GPU cost. Constraints enforce gate locality, topological dependency order, and the hardware budget (exactly L local and G global qubits per stage). Algorithm 2 calls the solver with increasing stage counts until feasible; **Theorem 1** guarantees minimality. Between stages the statevector is permuted and re-sharded via **all-to-all**, with the runtime tracking the current permutation P to avoid redundant movement.

*Kernelization (DP).* Within a stage, gates are grouped into kernels *"large enough to benefit from parallelism but also small enough to prevent exponential blowups in cost."* A DP with state DP[i, κ] minimizes total execution cost; two validity restrictions (weak convexity and monotonicity) keep candidate kernels topologically legal, and **Theorem 2** proves equivalence. Each kernel is tagged with one of **two execution strategies**, both explored by forking DP states: **fusion** (precompute the gate-matrix product and issue one big gate through **cuQuantum**) or **shared-memory** (load the statevector into GPU shared memory in batches, applying gates one at a time, at cost α + Σ_g Cost(g)).

*Execution and offloading.* Stages run sequentially; within a stage, shards run in a `parfor` (one GPU per shard) and kernels within a shard run sequentially. *"If sufficiently many GPUs are available, then each shard may be assigned to a GPU… If, however, fewer GPUs are available, the shards may be stored in the shared DRAM at each node, and swapped in and out of the GPUs for execution"* — the DRAM-offloading path, built on the **Legion** task runtime.

**Evaluation** `[paper]`.
- Hardware: **Perlmutter (NERSC), 64 nodes**, **4× A100-SXM4-40GB per node = 256 GPUs**; **AMD EPYC 7763** 64-core/128-thread per node; **256 GB DRAM per node**; **HPE Slingshot 200 Gb/s**. Toolchain GCC 12.3.0, CUDA 12.2, **NCCL 2.19.4**. Preprocessing measured separately on a single-threaded **Intel Xeon W-1350**.
- Real QPU: **no** — simulator only.
- Framework: built on **cuQuantum** (gate application), **NCCL**, **Legion** (offload mode), ILP via **PuLP** with the **HiGHS** solver. cuQuantum version `NOT_FOUND`.
- Problem scale: **28–36 qubits**, 11 circuit families from **MQT Bench** and **NWQBench**; largest 36 qubits (`vqc`) on 256 GPUs. Circuit depths/gate counts `NOT_FOUND`.
- Baselines: **HyQuas**, **cuQuantum** (via Qiskit Aer cuStateVec), **Qiskit** (Aer GPU backend), **QDAO** (offloading comparison only). **UniQ** named but excluded as *"extremely similar to HyQuas"*. Not compared: Pennylane, Qulacs, Quokka, QuEST, Intel-QS. **Baseline versions `NOT_FOUND` for all** — a real gap.
- **Every N× claim with context:**

| Claim | Baseline | Context |
|---|---|---|
| **up to 20.2×, 4.0× avg** | HyQuas | Same hardware, same GPU counts, 28–36q suite. Which circuit/GPU count gives 20.2×: `NOT_STATED`. Whether HyQuas ran multi-node: `CONTEXT_NOT_STATED`. |
| **up to 7.2×, 3.2× avg** | cuQuantum (Aer cuStateVec) | Same hardware, same GPU counts. Peak-case circuit `NOT_STATED`. |
| **up to 2,126×, 286× avg** | Qiskit Aer GPU | Same hardware. **This is a Qiskit framework-overhead artifact, not a partitioning result** `[inference]` — quote with care. |
| **74× avg, "two orders of magnitude"** | QDAO | DRAM-offloading regime only, 29–32 qubits. A different experiment from the above. |
| **">2× on average" over SOTA** | aggregate | The abstract's conservative framing. |

- **Shared context for all Atlas speedups:** **Same hardware — yes**, all baselines on Perlmutter A100s. **Fair-comparison control stated explicitly** `[paper]`: *"all baselines perform state-vector-based simulation and directly store the entire state vector on GPUs. While Atlas also supports more scalable quantum circuit simulation by offloading the state vector to a much larger CPU DRAM, to conduct a fair comparison, in this experiment, we disable Atlas' DRAM offloading and directly store the entire state vector on GPUs."* This is a genuinely well-controlled setup and deserves credit. **Precision: `CONTEXT_NOT_STATED`** — no mention of complex64/complex128 anywhere in the evaluation, so precision parity with baselines is **unverifiable**. **Preprocessing: effectively excluded** — it *"finishes in 7.2 seconds on average for each circuit in a single thread"* (staging 3.3 s + kernelization 3.9 s), reported separately and never stated to be included in the speedup figures; `[inference]` including it would materially change the single-shot end-to-end picture, though it amortizes over repeated runs of the same circuit, which is the realistic VQE/QAOA case. **Communication: included** — it is what is being optimized. **End-to-end** simulation time, minus preprocessing. Energy and byte-level communication volume `NOT_FOUND`.
- Scaling: **both.** **Weak scaling 1 → 256 GPUs** (28 local qubits fixed, global 0 → 8): on `graphstate`, Atlas's runtime grows **13.7×** while HyQuas's grows **267.9×** — **the most convincing single result in the paper**, since it isolates communication scaling rather than kernel speed. **Strong scaling** for a 32-qubit QFT on 1, 2, 4 GPUs with DRAM offloading — a narrow range.
- Limitations acknowledged `[paper]`: staging/kernelization runtime depends on circuit structure and solver, and the DP bound's tightness is unknown.

**Why an SC paper?** `[inference]` Because it is not really a quantum paper — it is a **parallel-compiler and data-movement paper whose data structure happens to be a statevector.** Substitute "distributed tensor with index-dependent communication cost" and the ILP-staging / DP-kernelization / all-to-all-repartitioning structure is a classic SC contribution. The authors are a systems group (CMU Catalyst / FlexFlow / Legion lineage, plus Acar for the algorithmic complexity), and the proof obligations and cost model are systems-conference currency. A quantum venue would have no reviewer equipped to evaluate the ILP formulation or the Legion offloading.

**Counterfactual** `[inference]`. **Emphatically no — and this paper is the strongest single evidence for this census's thesis.** Remove the HPC contribution and *nothing remains*: no quantum algorithm, no physics, no approximation, no hardware; the quantum content is entirely the benchmark suite. Conversely the HPC contribution stands alone perfectly well. **Atlas is the purest case of "quantum as workload, HPC as contribution."**

**Why it matters for Quantum-HPC.** Classical simulation is the workhorse of near-term quantum computing — algorithm development, QPU output verification, noise studies — so simulator throughput is rate-limiting for the whole field. Atlas's specific lesson is that **the local/regional/global qubit assignment is a compilation decision that should be solved optimally, not hand-tuned**, and that framing generalizes: the same local-vs-global partitioning problem appears in distributed/modular QPU architectures, where non-local gates cost entangling links rather than NCCL transfers. The weak-scaling gap (13.7× vs 267.9× growth to 256 GPUs) is the quantitative case that communication-optimal partitioning, not kernel micro-optimization, determines whether quantum simulation scales.

**Artifact.** `PUBLIC_CODE` + `PUBLIC_ARTIFACT` — the strongest in the census. Code **https://github.com/quantum-compiler/atlas**; artifact repo **https://github.com/quantum-compiler/atlas-artifact**; Zenodo **`10.5281/zenodo.12588145`** ("Artifact for SC'24 paper: Atlas…", 5.3 MB, CC-BY-4.0, 2024-08-17, prepared for the **Artifact Freeze stage** — i.e. it went through SC24 AD/AE). The paper states both `[paper]`: *"Atlas is publicly available as an open-source project [35] and also in the artifact supporting this paper [36]."*
**Cross-check verdict: `CONSISTENT`.** `[code]` **MPI + NCCL both present** in `src/base/simulator.cu`: `MPI_Bcast` of the NCCL unique ID to bootstrap (`ncclGetUniqueId`, `MPICHECK(MPI_Bcast(...MPI_COMM_WORLD))`), then `ncclGroupStart()` / `all2all(d_sv[i], sendsize, ncclDouble, recv_buf[i], …, comms[i], s[i], global_swap, myncclrank)` / `ncclGroupEnd()`, with `printf("Using NCCL for cross-node shuffle\n")` — i.e. **collective all-to-all for the global-qubit shuffle**, exactly as described. **Local vs global gate handling is explicit**: `n_local` / `n_global` throughout, `global_mask` and `local_mask` built from `new_global_pos[i] >= n_local`, and cuStateVec index-bit swaps issued separately as `GlobalIndexBitSwaps` and `LocalIndexBitSwaps`; `d_sv[k]` is the per-device sub-statevector with `subSvSize = (1 << n_local)`. **Precision is configurable**: `include/const.h` selects `cuFloatComplex` (FP32) or `cuDoubleComplex` (FP64). **The named hierarchical-partitioning mechanism lives in the Quartz submodule** (`deps/quartz` → github.com/quantum-compiler/quartz), whose `src/quartz/simulator/schedule.h` declares the three-level hierarchy directly: `compute_qubit_layout_with_ilp(const CircuitSeq&, int num_local_qubits, int num_regional_qubits, …)` documented in-header as *"@param num_regional_qubits The number of regional qubits per node"*, plus `get_schedules_with_ilp(...)`, `compute_local_qubits_with_ilp(...)`, `get_local_swaps_from_previous_stage(const Schedule& prev)`, `is_local_qubit(int)`, `local_qubit_mask_`, and kernel-scheduling variants (`compute_kernel_schedule`, `…_simple`, `…_greedy_pack_fusion`). **The ILP is a real solver formulation**: `src/python/simulator/ilp.py` uses PuLP with `a[i,j] = 1 iff the i-th qubit is a local qubit in the j-th iteration`; DP variant at `src/benchmark/dp.cpp`; stage-count ILP at `src/benchmark/ilp_num_stages.cpp`; `verify_schedule(...)` exists. **Evaluated configurations are present**: 312 `.schedule` files including staged variants (`ae30_28.stage0/1/2.schedule` — 30 qubits, 28 local), 267 QASM circuits, and `scripts/perlmutter/bench/` with per-node-count Slurm scripts for Atlas, HyQuas and Quartz (`srun-{1,2,4,8,16}-{hyquas,quartz}.sh`) plus `dist_cuquantum.py`. `atlas-artifact` adds `MQTBench_{28..34,42}q/`, `NWQBench/`, `staging_bench/`, `kernelization_bench/`, `table_scripts/`, `perlmutter/e2e/`. README documents both modes with an honest caveat: `USE_LEGION=OFF` for distributed multi-GPU and `USE_LEGION=ON` for CPU offload, *"the second mode hasn't been tested for multi-node execution."* Example invocation matches the paper's parameterization: `--import-circuit qft --n 31 --local 28 --device 4 --use-ilp`.

---

## 4. SC 2025 census

**Session structure** `[official-program]`: **one** session containing exactly these four papers.
*Quantum Computing and Simulation* — Paper session, Tue 18 Nov 2025, 3:30–5:00pm CST, Room 260-267, session id `sess164`, **chair Angel Yanguas-Gil (Argonne National Laboratory)**. Presentation order: Qonductor (3:30), QDockBank (3:52), PTSBE (4:15), DQTetris (4:37). Session and presentation topic tags: **"Post-Moore Computing"** and **"Quantum Computing"**.

The four papers occupy a **contiguous page block, pp. 728–788**, preceded by a numerics/mixed-precision session (pp. 661–727) and followed by a PIM/near-memory session (pp. 789–854). SC25 scheduled papers in "sets of four talks per session", so **the quantum block is exactly one whole session — no more, no less** `[official-program]` `[proceedings]`.

### 4.0 SC 2025 master table

| # | Title | First author / group | DOI | pp. | Tags | Branch | Artifact | Repro. Report |
|---|---|---|---|---|---|---|---|---|
| 1 | Qonductor: A Cloud Orchestrator for Quantum Computing | Giortamis (TU Munich) | `10.1145/3712285.3759785` | 728–745 | `Q_IN_HPC` | resource management / orchestration | `PUBLIC_CODE` | no |
| 2 | QDockBank: A dataset for Ligand Docking on Protein Fragments Predicted on Utility-Level Quantum Computers | Zhang (Kent State) | `.3759799` | 746–761 | `Q_FOR_HPC` `FUTURE_WORKLOAD` | dataset / application | `PUBLIC_ARTIFACT` (dataset) | no |
| 3 | Augmenting Simulated Noisy Quantum Data Collection by Orders of Magnitude Using Pre-Trajectory Sampling with Batched Execution | Patti (NVIDIA) | `.3759871` | 762–773 | `HPC_FOR_Q` | GPU simulation throughput | `PUBLIC_CODE` (upstreamed) | no |
| 4 | Optimizing Quantum Circuit Mapping to Reduce Inter-Module Communications in Distributed Architectures | Xu (East China Normal University) | `.3759789` | 774–788 | `HPC_FOR_Q` `Q_IN_HPC` | compiler / communication reduction | `UNKNOWN` (contested — §9) | **yes** — `10.1145/3712285.3769463` |

**Program context** `[official-program]`: SC25 accepted **137 papers from 623 submissions — 22%**. The volume printed 144 papers (133 regular + 11 Gordon Bell / GB-Climate). **No quantum paper won or was a finalist for Best Paper, Best Student Paper, or the Gordon Bell Prizes.** The Best Research Poster was quantum-adjacent (*"Time-stepping Hamiltonian Simulation for Solving Nonlinear PDEs via a Quantum-Classical Hybrid Approach"*, RIKEN/Kobe/Hokkaido) but posters are out of scope.

---

### 4.1 Qonductor: A Cloud Orchestrator for Quantum Computing

**Bibliographic.** Emmanouil Giortamis, Francisco Romão, Nathaniel Tornow, Dmitry Lugovoy, Pramod Bhatotia (Technical University of Munich). SC 2025 main-track regular paper `[proceedings]`, session *Quantum Computing and Simulation*. DOI `10.1145/3712285.3759785`, pp. 728–745. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `Q_IN_HPC`. Branch: scheduling / resource management.
**Content sources: arXiv 2408.04312 preprint AND the published SC25 PDF** (mirrored on the TUM DSE group site and co-author Francisco Romão's site), which allowed a direct preprint-vs-published comparison — see the divergence below. **Note the arXiv v1 also carries a different title**, *"Orchestrating Quantum Cloud Environments with Qonductor"* — so this paper diverges from its preprint in title, abstract figure, and framing.

**Research question** `[paper]`. How should a quantum cloud orchestrate hybrid quantum-classical jobs across a fleet of heterogeneous noisy QPUs plus classical resources, jointly serving *users'* QoS (job completion time, fidelity) and the *operator's* resource efficiency (utilization, load balance)?

**A. Quantum problem** `[paper]`. NISQ device heterogeneity and noise. Fidelity varies sharply across nominally identical devices — *"up to 38% higher fidelity in auckland than algiers"*. Error mitigation and circuit knitting can buy fidelity by spending classical compute, but how much to spend is unsolved.

**B. HPC problem** `[paper]`. **Textbook heterogeneous resource management.** The motivating measurement is load imbalance: *"on 26-11-23, mumbai has ~100× more pending jobs than kolkata"* — i.e. **queue wait time, not execution time, dominates job completion time.** The problems are heterogeneous scheduling, load balancing across a device fleet, queueing-delay minimization, multi-objective (latency vs quality) optimization, resource utilization, and the scalability of the scheduler itself under growing system size and load.

**C. SC contribution.**
- *Quantum novelty:* modest. Regression-based fidelity/runtime estimation and circuit knitting pre-exist; the novelty is systematizing them into selectable "resource plans."
- *HPC novelty:* the substance. First application of Pareto-optimal multi-objective scheduling (NSGA-II) plus learned performance prediction to a QPU fleet, with an **operator-side utilization objective**. The paper claims *"the first hybrid scheduler that balances the tradeoff between conflicting objectives of fidelity vs. JCTs."*
- *Categories:* **end-to-end system** + **scheduling algorithm** + **performance model**.

**Core mechanism** `[paper]`. The **API** exposes four functions — `createWorkflow`, `deploy`, `invoke`, `workflowResults` — and is hardware-agnostic; users declare requirements in a YAML deployment config (e.g. *"at least one GPU"*, *"a QPU with at least 20 qubits"*) and delegate allocation to a leader node. The **resource estimator** applies error-mitigation transformations to generate candidate circuits, transpiles each to per-QPU template models, then predicts fidelity and execution time with regression models trained on *"over 7,000 job executions collected from our experiments on the IBM quantum cloud"*; features include circuit depth, two-qubit-operation count, qubit topology and error rates. *"Polynomial Regression yields the highest accuracy, achieving an R² score of 0.998 for execution time and 0.976 for fidelity prediction."* It emits (by default three) **resource plans**, each a different point on the classical-compute-buys-quantum-fidelity curve — this is the QPU-vs-classical decision. The **hybrid scheduler** then runs three stages: job pre-processing/filtering; multi-objective optimization via **NSGA-II** (pymoo) minimizing `f₁ = mean JCT` and `f₂ = mean error (1 − mean fidelity)` to build a Pareto front with customized genetic operators; then **Multiple-Criteria Decision-Making** selection using pseudo-weights `P=(p₁,p₂)`, `p₁+p₂=1`. The pseudo-weight vector is the operator-facing tradeoff knob.

**Evaluation** `[paper]`.
- Classical hardware: *"AMD EPYC 7713P 64-Core servers with 0.5 TB of RAM"*. **Server count `NOT_FOUND`.** No GPUs used, despite the API exposing GPU requests.
- Software: Python 3.11, Go 1.21, on Kubernetes; Qiskit Transpiler 0.45.3, Mapomatic 0.10.0, scikit-learn 1.4.0, pymoo 0.6.1.
- **Real QPU — partial, and easy to misread.** Real IBM hardware was used **only to build the estimator's training dataset and characterize the fleet**, not to run the headline evaluation. Provider: IBM Quantum **open access plan**, *"all freely available QPUs"*; *"we monitor all available QPUs on the IBM Quantum platform for ten days in November 2023"* and *"more than 7,000 job executions from our experimentation within the IBM quantum cloud"*. **Devices named:** cairo, hanoi, kolkata, mumbai, algiers, auckland (27-qubit class). Per-device job counts, shot counts and total QPU-time `NOT_FOUND`.
- **The headline evaluation is SIMULATED**: *"use Qiskit's FakeBackends for noisy simulations"*, with the authors patching FakeBackends *"with the ability to maintain their own queue of scheduled jobs, job waiting and execution times, and the notion of time flow."* **Eight simulated QPUs.** *Precision note added at verification:* the paper never writes "8 FakeBackends" — the count is a join of the FakeBackends statement with a separate reference to *"eight simulated QPUs"* in §8.2. The join is defensible; the phrasing is not the paper's.
- Workload: *"more than 70,000 benchmark circuits, 2 to 130 qubits in size"* from MQT Bench (VQE, Grover, Shor, QAOA, QFT); load 1,500 applications/hour for one simulated hour.
- **Baseline: exactly one — First-Come-First-Serve.** The paper states the exclusion explicitly: *"To our knowledge, [72] is the only peer-reviewed work for scheduling quantum jobs. However, its source code is unavailable."* All other comparisons are against *"different configurations of our system."*
- **Quantitative claims — one is materially misleading if quoted loosely:**

| Claim | Real context |
|---|---|
| "up to **54%** lower JCT" | **NOT against FCFS.** It is an intra-Pareto-front tradeoff (Fig 10b): balanced pseudo-weights vs the fidelity-prioritized extreme of Qonductor's *own* front. *"assigning equal weights selects a balanced solution, where 6% lower fidelity leads to 54% lower JCT."* |
| **vs the actual baseline** | *"Qonductor's mean completion times are ~48% lower than FCFS"* (Fig 6b). **48%, not 54%, is the scheduler-vs-baseline number.** |
| "**66%** higher utilization" | vs FCFS, 8 simulated QPUs, 1,500 apps/h, one simulated hour: *"achieves 66% higher utilization than FCFS, on average, by distributing the quantum job load."* |
| Pareto extreme | *"67% lower JCT than the worst case (priority on fidelity)"* |
| Quality cost | **PREPRINT/PUBLISHED DIVERGENCE — and it is worse than a changed number.** arXiv says **6% fidelity**; the published SC25 abstract says *"sacrificing **3% execution quality**"*. But the published **body** still reads *"6% lower fidelity leads to 54% lower JCT"* while *separately* reporting *"Qonductor's mean fidelity is 2−3% lower than that of FCFS"*. **The published abstract therefore appears to splice a vs-FCFS fidelity delta (3%) onto a Pareto-front JCT tradeoff (54%) — two different measurements.** Quote the body, not the abstract. |
| Scalability | *"Doubling the system size from 4 to 8 QPUs improves JCTs by 52.8% and making it four times larger (16 QPUs) improves JCT by 81%"*; load scaled 1,500 → 3,000 → 4,500 jobs/h (*"up to 3× the current IBM load"*); scheduler stage runtimes *"relatively constant as the cluster size increases."* |

- Scaling: **neither** strong nor weak in the classical sense. It is a *system scalability study* — grow the fleet 4→16 and the offered load 1×→3× — not scaling of a parallel kernel.

**Why an SC paper?** `[inference]` The entire contribution is expressed in systems vocabulary — queueing, load balance, utilization, QoS, Pareto scheduling, Kubernetes orchestration — and the quantum layer is treated as an opaque heterogeneous accelerator. The operator-vs-user objective conflict is a datacenter framing, not a physics one.

**Counterfactual** `[inference]`. **The question inverts here.** Strip the HPC angle and nothing remains — the quantum content alone (error mitigation, knitting, fidelity estimation) is derivative and would not carry a paper anywhere. This is a systems paper that happens to schedule QPUs, and it would plausibly have been publishable at OSDI/EuroSys/HPDC. Its SC acceptance costs the venue nothing.

**Why it matters for Quantum-HPC.** **This is the closest existing template for operating a QPU fleet as a shared HPC-centre resource** — learned performance prediction + multi-objective scheduling + utilization accounting is precisely the Slurm/PBS integration problem. Its weakness is equally instructive: eight FakeBackends against a single FCFS baseline means **nobody has yet validated such a scheduler against a real multi-QPU fleet or a real batch scheduler.**

**Artifact.** `PUBLIC_CODE` — **https://github.com/manosgior/Qonductor-SC25** (MIT). Note the paper itself names **no URL**, saying only *"We implement an open-source prototype"*; the repo is on the first author's personal account, **not** under `github.com/TUM-DSE` (that org has no quantum repos).
**Cross-check verdict: `CONSISTENT`.** `[code]` `requirements.txt` confirms the exact claimed stack: **pymoo≥0.6.0.1** (NSGA-II), scikit-learn≥1.3.0, mapomatic≥0.10.0, mqt.bench, mqt.predictor, qiskit-ibm-runtime, Supermarq. `src/scheduler/multi_objective_scheduler.py` imports `from pymoo.algorithms.moo.nsga2 import NSGA2` and instantiates it in two configurations with `SBX`/`TwoPointCrossover`, `PM`/`BitflipMutation`, `RoundingRepair`, `StarmapParallelization`, and **`PseudoWeights` for picking a point off the Pareto front** (`_get_best_solution(result, weights)`) — matching the paper's MCDM stage exactly. Problem encodings in `src/optimization/binary_problem.py` and `discrete_problem.py` (pymoo `ElementwiseProblem`). The estimator is real: `src/execution_time/regression_estimator.py` uses `PolynomialFeatures` + `LinearRegression` plus GradientBoosting/ExtraTrees/RandomForest/AdaBoost/HistGradientBoosting, with `_run_grid_search`, `_choose_best_model`, `_extract_circuit_features`; trained models are committed (`data/regression_model.joblib`, `data/regression_models/` 16 MB). Fidelity path present (`_calculate_fidelity`, `_transpile_circuit`, `_get_best_layout`, `_calculate_backend_queue_waiting_times`). The scalability simulation is `src/scheduling_manager/scheduling_manager.py` + `load_generator.py`. **Figure mapping is documented and the data is committed** — `ibm_status_analysis.py`→Fig 2, `e2e_performance.py`→Fig 6, `estimator_analysis.py`→Fig 7, `scheduler_analysis.py`→Fig 10, `scheduling_manager_analysis.py`→Figs 8–9; `data/` is 334 MB including `data/ibm_status/{load_imbalance,spatial_variance,temporal_variance}` (211 MB) backing the >7,000-real-run claim.
**Gap to record** `[code]`: there is **no Go and no Kubernetes code** in the artifact, though the paper describes a Kubernetes/Go prototype. The public artifact is the Python estimator + scheduler + simulation harness — everything needed to reproduce the *figures*, not the orchestrator itself.
**Warning against false attribution**: `github.com/TUM-DSE/QOS` is the same group's **OSDI'25 QOS paper**, not Qonductor.

---

### 4.2 QDockBank: A dataset for Ligand Docking on Protein Fragments Predicted on Utility-Level Quantum Computers

**Bibliographic.** Yuqi Zhang (Kent State), Yuxin Yang (Lerner Research Institute, Cleveland Clinic), Cheng-Chang Lu (Qradle Inc), Weiwen Jiang (George Mason), Feixiong Cheng (Cleveland Clinic), Bo Fang (PNNL), Qiang Guan (Kent State). SC 2025 main-track regular paper `[proceedings]`. DOI `10.1145/3712285.3759799`, pp. 746–761. `PUBLISHED_REGULAR_PAPER`.
**Classification.** `Q_FOR_HPC` + `FUTURE_WORKLOAD`. Branch: dataset / scientific application.
**Content source: arXiv 2508.00837v1**; the published abstract is identical to the preprint abstract.
*(Title note: ACM/Crossref render "dataset" lowercase; the SC25 program page renders "A Dataset". The Crossref form is used here.)*

**Research question** `[paper]`. Can utility-scale quantum hardware produce protein-fragment structures in ligand-binding pockets accurate enough to be useful for docking — and can a standardized dataset of such structures serve as a community benchmark?

**A. Quantum problem** `[paper]`. VQE-based protein folding on a tetrahedral lattice model. The Hamiltonian has four terms encoding *"chirality constraints, geometric backbone constraints, residue collision prevention, and pairwise amino acid interaction energies."* Executed at 12–102 qubits and circuit depths 53–413 on noisy superconducting hardware — deep enough that noise is a first-order concern, which the paper handles by asserting moderate noise *"may function as stochastic perturbations."*

**B. HPC problem. — Essentially none. This is the key finding of the SC25 census.**
An explicit negative search over the full text found **no** mention of high-performance computing, HPC, supercomputers, parallelism, GPUs, clusters, workflow systems, job scheduling, throughput, or queueing. **No classical computing hardware is specified anywhere in the paper.** The only resource-consumption argument is economic and quantum-side: *"commercial access to IBM quantum processors is billed by the minute"*, >60 h of QPU runtime, >$1M cost. There is no systems methodology, no parallel algorithm, no performance engineering, and no measured classical cost. `[paper]`

**Be precise about this: the HPC problem here is not thin — it is absent.**

**C. SC contribution.**
- *Quantum novelty:* real. First protein-structure dataset generated entirely on utility-scale QPUs; claims to beat AlphaFold2/3 on these fragments.
- *HPC novelty:* **none identified.**
- *Category:* **dataset/benchmark**, unambiguously and exclusively.

**Core mechanism** `[paper]`. Fragments are drawn from **PDBbind**, *"specifically from ligand-binding pockets or their adjacent regions"*, giving **55 fragments** in three length groups: S (5–8 residues, 19), M (9–12, 22), L (13–14, 12). Each fragment's conformation is encoded on a tetrahedral lattice and its four-term Hamiltonian minimized by **VQE using Qiskit's EfficientSU2 ansatz with the gradient-free COBYLA optimizer over "more than 200 iterations"**, each energy evaluation executing the circuit where *"the circuit is repeatedly executed and measured 100,000 times."* Qubit counts and depths scale with fragment length: S = 12–46 qubits / depth 53–189; M = 54–102 / 221–333; L = 92–102 / 373–413. All runs on **IBM 127-qubit Eagle r3** processors (native gates ECR, ID, RZ, SX, X); **no error mitigation is stated**. Evaluation docks each structure with **AutoDock Vina** under *"20 independent docking simulations, each initialized with a distinct random seed"*, each yielding *"the top 10 binding poses"* — **>2,000 docking tests** — scored by **RMSD** against experimental X-ray structures (Biopython) and by binding affinity in kcal/mol.

**Evaluation** `[paper]`.
- **Classical hardware: `NOT_FOUND`.** No CPU, GPU, cluster, or node information anywhere. Tools only: Qiskit, Open Babel, AutoDock Vina, Biopython. One author is at PNNL but **no PNNL computational resources are described.**
- **Real QPU: yes** — *"IBM's 127-qubit superconducting quantum processor"*, *"the IBM Eagle r3 processor"*. **Specific device names (ibm_kyiv, ibm_brisbane, etc.) `NOT_FOUND`** — the paper names the processor *family* only, a real reporting gap for a paper whose central claim is hardware provenance.
- QPU effort: *"more than 60 hours of quantum processor runtime"*; *"hundreds of thousands of quantum circuit executions"*; 100,000 shots per circuit measurement.
- **Cost claim: *"a total computational cost exceeding one million USD."* The derivation is `CONTEXT_NOT_STATED`** — 60 h of runtime is reconciled with $1M only via the unquantified "billed by the minute" remark. **Treat this number as unverified.**
- Problem scale: 55 fragments; 12–102 qubits; depth 53–413; >2,000 docking tests.
- **Baselines: AlphaFold2, AlphaFold3, and experimental X-ray structures.** Notably **no classical physics-based folding baseline and no classically-simulated VQE baseline** — so there is no evidence in the paper that the quantum hardware was *necessary* rather than incidental `[inference]`.
- Metrics: RMSD; docking binding affinity. Claimed: *"over 90% of entries surpassing AlphaFold2 and more than 80% surpassing AlphaFold3 in accuracy."*
- Scaling: **neither.**
- **Limitations section: none.** The conclusion states no limitations and no future work `[paper]`.

**Why an SC paper?** `[inference]` Nothing in the paper argues venue fit. Plausible reconstruction: (a) the contribution is a **capability demonstration on a scarce large-scale machine** — >60 h of utility-scale QPU time is the structural analogue of an SC "hero run", and SC has long rewarded consuming a flagship resource and publishing the result; (b) SC has an established tradition of accepting benchmark and dataset papers as community infrastructure; (c) the SC25 Post-Moore topic area was broad enough to admit a quantum applications dataset. **The $1M and 60-hour figures are doing the work that node-hours normally do.**

**Counterfactual** `[inference]`. **The sharpest boundary case in the census, and the counterfactual inverts.** There is no HPC contribution to remove — so **the paper already *is* the counterfactual.** SC25 accepted a main-track regular paper whose entire contribution is a quantum-application dataset with zero computer-systems content, no classical hardware reported, no parallelism, and no performance claim.
The implication is direct: **for this paper, SC's operative definition of "HPC contribution" was resource consumption, not methodology.** The dataset was expensive to produce on a scarce machine and was released publicly; that sufficed. This is a meaningfully wider boundary than the one the other three papers sit inside, and it is the single most important datapoint in this session for the census question.

**Why it matters for Quantum-HPC.** Two things. First, precedent: SC will accept quantum datasets and QPU-hours as a legitimate resource-consumption argument, which opens a submission path. Second, it exposes an unclaimed problem **directly adjacent to it** — nobody in this paper addresses how to run such a campaign *efficiently*. Hundreds of thousands of circuit executions, 200+ COBYLA iterations per fragment, 100k shots each, across 55 fragments, with no batching strategy, no error-mitigation cost/benefit analysis, no hybrid VQE orchestration, and no classical-resource accounting. **That gap is exactly the HPC paper this paper is not, and it is well-posed.**

**Artifact.** `PUBLIC_ARTIFACT` (dataset only) — canonical URL **https://github.com/qiqi-xingyi/QDockBank_**. *Corrected at verification:* the preprint names `github.com/QDockBank/QDockBank_`, but that path resolves only through a GitHub owner-transfer redirect — the `QDockBank` account holds two differently-named repositories (`Databank_Creation`, `QCloudSim-SigSim2025`) and no `QDockBank_`. **Cite the `qiqi-xingyi` path.**
**Cross-check verdict: `CONSISTENT`** for the stated deliverable. `[artifact]` Unpacking `QDockBank.zip` yields **exactly 55 fragment directories, 55 `*_metadata.json`, 55 `*_RMSD_docking_result.json` and 55 `.pdb` files** — matching the paper's 55 fragments. Quantum metadata is per-fragment and specific, e.g. `4jpy`: `"number_of_qubits": 102, "circuit_depth": 413, "lowest_energy": 23332.067906, "execution_time_s": 12918.78`. Qubit counts span **12 → 102** (12, 23, 38, 46, 54, 63, 72, 82, 92, 102), consistent with the "utility-level" claim. Docking records match the stated protocol: `rmsd`, `rmsd_tool: "BioPython"`, `docking.average_affinity`, and `runs` = 20 independent Vina runs each with 9 binding `modes`. `index.txt` groups fragments L/M/S.
**Caveat** `[code]`: the repo is a **data distribution hub only** — no VQE/Qiskit generation pipeline, no Hamiltonian construction, no docking pipeline, and no AlphaFold comparison baselines. **The "generated on IBM utility-level QPUs via VQE" provenance is asserted by metadata, not reproducible from this artifact.**

---

### 4.3 Augmenting Simulated Noisy Quantum Data Collection by Orders of Magnitude Using Pre-Trajectory Sampling with Batched Execution

**Bibliographic.** Taylor Lee Patti, Thien Nguyen, Justin Gage Lietz, Alex J. McCaskey, Brucek Khailany (NVIDIA Corporation). SC 2025 main-track regular paper `[proceedings]`. DOI `10.1145/3712285.3759871`, pp. 762–773. `PUBLISHED_REGULAR_PAPER`. Referred to below as **PTSBE**, its name in the shipped software.
**Classification.** `HPC_FOR_Q`. Branch: GPU-accelerated simulation throughput.
**Content source: arXiv 2504.16297v1**; published abstract identical to the preprint abstract.

**Research question** `[paper]`. How can noisy-quantum-circuit measurement datasets be generated orders of magnitude larger than current trajectory simulators permit, so that data-hungry downstream tasks — principally **ML-based QEC decoder training** — become feasible?

**A. Quantum problem** `[paper]`. Noisy simulation cost. Noiseless n-qubit states scale as `2ⁿ`; noisy systems require `2ⁿ × 2ⁿ` density matrices. Trajectory methods replace the density matrix with an ensemble of `m ≪ 2ⁿ` pure states, but *"current implementations use unoptimized sampling, redundant state preparation, and single-shot data collection"*, and *"conventional trajectory simulations interleave gate applications with per-step noise sampling, forcing serial execution and discarding critical error metadata."*

**B. HPC problem** `[paper]`. **Throughput of a GPU data-generation pipeline.** The expensive operation is statevector preparation; the cheap operation is measurement sampling. Conventional trajectory simulation pays the expensive one once per *shot*, destroying arithmetic intensity and forcing serialization. The systems problem is to decouple stochastic sampling from state evolution so shots batch against a reused statevector — plus distributing a single trajectory's statevector across GPUs (strong scaling) and independent trajectories across GPUs (embarrassingly parallel). Memory-wise it avoids ever materializing the `O(4ⁿ)` density matrix.

**C. SC contribution.**
- *Quantum novelty:* modest. Trajectory methods date to Carmichael; the novelty is pre-sampling Kraus-operator sets, tailoring error types (Pauli twirling, spatially correlated noise), and **retaining error provenance**.
- *HPC novelty:* the substance. Restructuring the algorithm so **the number of expensive statevector simulations scales with the number of unique trajectories `T` rather than the total shot count `N`** — `[documentation]` *"the number of circuit simulations scales with the number of unique trajectories T, not the shot count N"* — which is what makes batching and near-linear multi-GPU scaling possible.
- *Categories:* **GPU kernel/acceleration** + **memory optimization** + **algorithm–architecture co-design**, delivered as a **runtime/system mechanism** in CUDA-Q.

**Core mechanism** `[paper]` `[documentation]`. A **trajectory** is one complete assignment of Kraus operators across all noise sites in the circuit, with probability the product of the per-site choices. Where conventional Monte Carlo interleaves noise sampling with gate application, **PTS precomputes every stochastic decision — error types, locations, mitigation parameters — before statevector propagation begins.** Execution then has three phases: (1) **Trajectory Sampling** draws `T` unique trajectories under a selectable sampling strategy; (2) **Shot Allocation** distributes the `N` requested shots across those trajectories, e.g. proportional to trajectory probability; (3) **Batched Execution** prepares each trajectory's statevector *once* and draws its whole allocated block of shots in bulk, merging outcomes into a single `SampleResult`. The economics are stated plainly: *"As shot sampling is much more efficient than statevector preparation, sampling large numbers of shots from a given Kraus operator subset is highly efficient"* — the exponential-cost step is amortized across a batch. Against **density-matrix simulation** it never forms the `2ⁿ × 2ⁿ` object; against **standard MC trajectories** it eliminates per-shot state re-preparation and recompilation and, crucially, retains **error provenance via lightweight metadata tags attached to each trajectory**, so generated shots arrive pre-labeled with which errors produced them — that is what makes them *decoder training data* rather than merely samples. Stated limits `[documentation]`: PTSBE requires a **static circuit** (no mid-circuit measurement, no measurement-conditioned control flow) and a local simulator backend, and it introduces **correlated sampling** — it suits *"a data-hungry downstream task that is not necessarily inhibited by correlated sampling, such as training AI models."*

**Evaluation** `[paper]`.
- Hardware: *"Four H100 GPUs with 80GBs of vRAM each"* per configuration, on **NVIDIA's Eos DGX SuperPOD**. Budget: **4,445 H100 GPU-hours** (statevector) and **2,223 H100 GPU-hours** (tensor network). **Node counts `NOT_FOUND`.**
- Software: *"All experiments were done using CUDA-Q v0.10"*; backends `nvidia` (statevector) and `tensornet`.
- Circuits: **magic state distillation.** 35-qubit case = 5 logical qubits in the **[[7,1,3]] color code** (5×7=35), statevector. 85-qubit case = 5 logical qubits in the **[[17,1,5]] color code** (5×17=85), tensor network. **Circuit depth `NOT_FOUND`.**
- Real QPU: **none.** Simulator only.
- **Noise model: `NOT_FOUND` / `CONTEXT_NOT_STATED`.** The paper gives only the generic Kraus/CPTP formalism and mentions depolarizing noise as an example. **No error rates and no concrete noise-model parameters are given for the actual 35- and 85-qubit runs** — a genuine reporting gap in a paper whose entire subject is noisy simulation.
- **Baseline: "conventional trajectory methods" — the unbatched, one-statevector-per-shot mode of the *same* framework.** **NOT** density-matrix simulation, **NOT** a competing simulator, **NOT** CPU. Confirmed independently by CUDA-Q documentation `[documentation]`: *"Traditional trajectory methods construct a new statevector for every measurement shot."* **No third-party simulator (Qiskit Aer, qsim, etc.) is compared against.**
- **Quantitative claims in full context:**

| Claim | Real context |
|---|---|
| "**10⁶×**" | *"the efficiency increase reaching ∼10⁶ for batch sizes of 10⁶–10⁷ shots."* A **shots/second efficiency ratio at the largest batch sizes**, against the same framework's unbatched mode — **not a wall-clock speedup on a fixed workload.** 35 qubits, [[7,1,3]], statevector, 4×H100, statistics over 100 experiments. |
| "**16×**" | *"an over 16x efficiency increase in shot collection was obtained for batched samples of just 10³ shots"* — 85 qubits, [[17,1,5]], tensornet, 4×H100, statistics over 200 experiments. |
| Datasets produced | **one trillion** 35-qubit shots; **one million** 85-qubit shots. |
| Absolute throughput | Figures report shots/second (35q) and shots/minute (85q) as *curves*. **Absolute values `NOT_FOUND`**, and there is **no tabular head-to-head against any competing method.** |
| Accuracy tradeoff | `[documentation]` *"achieves traditional trajectory simulation accuracy at a fraction of the computational cost when the number of unique trajectories (errors) is much smaller than the total shot count"* — speed and sampling-distribution fidelity trade off via `T/N`. |

- Scaling: **both, informally.** *Strong:* intra-trajectory multi-GPU statevector distribution shows *"nearly linear speedup with increasing numbers of GPUs."* *Weak/embarrassingly parallel:* *"inter-trajectory efficiency scaling (not shown) is by definition linear with GPU number."* **Note that the inter-trajectory claim is asserted and explicitly "not shown"** — there is no measured multi-node scaling data.

**Why an SC paper?** `[inference]` The contribution is GPU throughput engineering on a named supercomputer, budgeted in GPU-hours, with multi-GPU scaling curves, delivered into a production HPC software stack. Every element of the argument is an SC element; the quantum content is the workload, not the contribution.

**Counterfactual** `[inference]`. **No — the least ambiguous case in the SC25 session.** Without the batching and GPU-throughput contribution, "pre-sample the Kraus operators before propagating" is a modest algorithmic rearrangement worth a short quantum-simulation note. The 10⁶×, the trillion-shot dataset, the 6,668 GPU-hours and the multi-GPU scaling — all HPC-resource statements — *are* the paper.

**Why it matters for Quantum-HPC.** It converts **QEC decoder training data into a supercomputer workload**, one of the most concrete near-term Quantum-HPC couplings that exists. More transferably, it demonstrates a reusable pattern: **restructure a quantum simulation so the exponential-cost step is amortized across a batch, making the sampling cost — not the state cost — dominant.** That should generalize to other stochastic quantum-simulation workloads. Its weaknesses (no noise-model disclosure, no third-party baseline, no measured multi-node scaling) are all straightforwardly addressable by a follow-up.

**Artifact.** `PUBLIC_CODE` — **upstreamed into open-source CUDA-Q, no paper-specific repository.** The paper itself contains **no artifact statement and no URL** `[paper]`. However, PTSBE is a shipped, documented feature of **CUDA-Q 0.14** (release blog 2026-03-16): docs at **https://nvidia.github.io/cuda-quantum/0.14.0/using/examples/ptsbe.html**, source in **https://github.com/NVIDIA/cuda-quantum**. **The documentation explicitly cites this SC25 paper as `[Patti2025]`**, which is what makes this a genuine artifact rather than a same-authors-different-paper false attribution `[documentation]`.
**Cross-check verdict: `CONSISTENT`** for the mechanism. `[code]` The implementation is a dedicated subsystem at `runtime/cudaq/ptsbe/` (20 files): `PTSBESampler.{h,cpp}`, `PTSBESamplerImpl.h`, `PTSBESample.{h,cpp}`, `PTSBESampleResult.{h,cpp}`, `PTSBEOptions.h`, `PTSBEExecutionData.{h,cpp}`, `NoiseExtractor.{h,cpp}`, `KrausTrajectory.h`, `KrausSelection.h`, `PTSSamplingStrategy.h`, `ShotAllocationStrategy.{h,cpp}`, `TrajectoryDeduplication.{h,cpp}`, `strategies/{Ordered,Probabilistic}SamplingStrategy.cpp`; Python binding `python/runtime/cudaq/algorithms/py_sample_ptsbe.cpp`; 8 test files under `python/tests/ptsbe/`. **Pre-trajectory sampling is literal**: `PTSSamplingStrategy.h` defines `struct NoisePoint { circuit_location; qubits; op_name; cudaq::kraus_channel channel; }` and `computeTotalTrajectories(...)` — *"Calculates the combinatoric product of operator counts across all noise points… total = k_1 × k_2 × … × k_N"* — capped at 2^40 (~1 trillion), matching the paper's trillion-shot scale. **Batched execution** is the `PTSBatch` type dispatched through `struct BatchSimulator { virtual … sampleWithPTSBE(const PTSBatch &batch) = 0; }`. **Deduplication with multiplicity** — the mechanism turning shots into unique trajectories — is `TrajectoryDeduplication.h`: *"Deduplicate trajectories by content (kraus_selections). Representatives keep the first occurrence's probability, trajectory_id, and num_shots; multiplicity is the sum of all merged trajectories' multiplicities."* Documented backends include `nvidia`, **`nvidia, option=mgpu`**, `nvidia, option=mqpu`, `tensornet`, `tensornet-mps` — covering both arms of the paper's evaluation `[documentation]`.
**Gap to record** `[code]`: the paper's specific experiment harness is **not** present — no scripts for the 35-qubit trillion-shot or 85-qubit runs, no Eos SuperPOD configs, and neither generated dataset is published. `PTSBESample.h:420` notes *"PTSBE is simulator-only so no multi-QPU distribution is used."* So the **mechanism is fully verifiable; the reported results are not reproducible from this repo.**

---

### 4.4 Optimizing Quantum Circuit Mapping to Reduce Inter-Module Communications in Distributed Architectures

**Bibliographic.** Longshan Xu, Edwin Hsing-Mean Sha, Xiulin Cui, Qingfeng Zhuge (East China Normal University). SC 2025 main-track regular paper `[proceedings]`. DOI `10.1145/3712285.3759789`, pp. 774–788. `PUBLISHED_REGULAR_PAPER`. System name **DQTetris**.
**Classification.** `HPC_FOR_Q` + `Q_IN_HPC`. Branch: compiler / communication reduction.

> **⚠ Source limitation — read before using anything below.** This paper is **closed access** (OpenAlex `open_access: closed`, no OA URL), has **no arXiv preprint** (verified by title, author and topic searches), and **ACM DL was fully blocked** from this environment across `/doi/`, `/doi/full/` and `/doi/pdf/`. Semantic Scholar's reference list is publisher-elided. **Everything below is derived from the abstract only** — verified identical across the SC25 program page, ACM DL metadata, OpenAlex, and the ECNU Pure institutional record — plus the reproducibility report's metadata. **The cost model, baselines, benchmarks and hardware are all `NOT_FOUND`, and none has been guessed at.**

**Research question** `[abstract]`. How should a quantum circuit be mapped onto a modular / multi-module (multi-chip) architecture so inter-module communication is minimized under per-module qubit capacity constraints?

**A. Quantum problem** `[abstract]`. *"Executing circuits in such distributed systems necessitates non-local operations between modules, incurring significant communication overhead."* Two-qubit gates spanning module boundaries must be realized by gate teleportation or by teleporting qubit state between modules — both consume entanglement, add latency, and are substantially more error-prone than local gates. Module capacity bounds how many qubits can be co-located.

**B. HPC problem** `[inference]` on `[abstract]`. This is a **partitioning + communication-minimization problem**, structurally the same as graph/mesh partitioning for distributed-memory HPC: assign qubits (vertices) to modules (partitions) under capacity constraints so as to minimize cut edges (non-local gates). The distinctive — and genuinely HPC — twist is that the interaction graph **evolves over circuit time**, so the algorithm must also decide **when to repartition** (temporal segmentation) and must account for the **migration cost of repartitioning**, which here is teleportation. **That is dynamic load balancing with migration cost — the adaptive-mesh-refinement repartitioning problem in different clothing.**

**C. SC contribution.**
- *Quantum novelty:* the hierarchical "seek a globally communication-free assignment first, then fall back to locally communication-free subcircuits via layer-wise gate pruning" formulation, plus adaptive gate teleportation.
- *HPC novelty:* the **objective formulation** — minimizing **qubit reassignment *events*** (migrations) rather than per-gate teleportations, achieved through optimal circuit segmentation. A migration-count objective rather than a cut-count objective is the HPC-recognizable move.
- *Category:* **communication reduction** (primary), realized as a mapping/partitioning algorithm.

**Core mechanism** `[abstract]` only; internals `NOT_FOUND`. DQTetris uses *"a hierarchical framework that first seeks a global communication-free qubit mapping assignment under module capacity constraints"* — a single partition for the whole circuit with zero cut two-qubit gates. *"If infeasible, it searches for subcircuits with local communication-free qubit assignments via layer-wise gate pruning"* — peeling gates off layer by layer until the remaining subcircuit admits a cut-free assignment. Because *"executing adjacent subcircuits with different qubit assignments incurs inter-module data teleportation,"* the residual cost is the transitions between segments, and *"DQTetris minimizes these overheads by reducing qubit reassignment events through optimal circuit segmentation, qubit assignment selection, and adaptive gate teleportation."* Three levers: **where to cut the circuit into segments**, **which of several feasible assignments to pick per segment** (minimizing the delta to its neighbours), and **when to teleport the gate instead of moving the qubit**.
**The exact cost model is `NOT_FOUND`** — whether "communication cost" counts EPR pairs consumed, teleportation operations, added latency/depth, or a weighted combination is not stated in any accessible source. **The optimization method (exact, ILP, heuristic, greedy) is `NOT_FOUND`.**

**Evaluation — almost entirely `NOT_FOUND`.**
- Hardware: `NOT_FOUND`.
- Real QPU: `NOT_FOUND`. *(Do not assume. This is a compiler/mapping paper and is almost certainly simulation/analysis only, but that could not be verified, so it is recorded as `NOT_FOUND` rather than asserted.)*
- Problem scale: `NOT_FOUND` — module count, per-module capacity, qubit counts, circuit depths all unavailable.
- **Baseline: `NOT_FOUND`.** The abstract says only *"compared with existing methods."* No reachable source names them. Citing/adjacent work was checked and does not identify them. **The usual candidates in this literature — FGP-rOEE, OEE, Autocomm, QuComm, pytket-dqc, Qiskit SABRE — are NOT verified as DQTetris's baselines and must not be assumed.**
- Benchmarks: `NOT_FOUND` — *"various benchmarks"* only. (QASMBench is the field norm but is unverified here.)
- **Only quantitative claim** `[abstract]`: *"DQTetris can achieve average reductions in communication costs ranging from 28% to 75% across various benchmarks."* **`CONTEXT_NOT_STATED` on every axis** — which benchmark yields 28% vs 75%, against which baseline, at how many modules, with what capacity. Note the 28–75% is a range *across benchmarks*, of *average* reductions.
- Scaling: `NOT_FOUND`.
- Bibliographic scale: 70 references (Semantic Scholar) / 52 referenced works (OpenAlex).

**Why an SC paper?** `[inference]` **Framing.** Presented as *qubit mapping*, this is DAC/ICCAD/quantum-compiler material; presented as **communication minimization in a distributed architecture**, it is SC-shaped. The abstract's vocabulary — modular, distributed, communication overhead, segmentation, capacity constraints — maps one-to-one onto HPC partitioning, and SC25 filed it under Post-Moore Computing. The venue fit is achieved by choosing the communication objective as the headline rather than circuit fidelity or gate count.

**Counterfactual** `[inference]`. Borderline, leaning **"it would still land somewhere, but not necessarily at SC."** Strip the communication framing and present the same algorithm as a qubit-mapping heuristic and it reads as DAC/ICCAD/ASPLOS material. The HPC angle is real — the temporal-repartitioning-with-migration-cost structure is not cosmetic — but it is largely a *framing* of a compilation problem in communication-minimization terms. That is worth noting without cynicism: **graph partitioning became an HPC topic by exactly this route.**

**Why it matters for Quantum-HPC.** Modular/multi-chip QPUs are the consensus scaling path and inter-module communication is their bottleneck, so this problem will grow in importance. The formulation — partition under capacity constraints, over a time-evolving interaction graph, minimizing migrations rather than cuts — is the same problem HPC solved for adaptive mesh refinement and dynamic load balancing, which means **direct methodology transfer is available** from ParMETIS/Zoltan-style diffusive repartitioning and migration-cost-aware objectives. This paper is the SC-side anchor for that thread.

**Artifact.** `UNKNOWN` — **but an artifact demonstrably exists and was independently evaluated.** This is the one status in the census where two independent searches disagreed; see §9.3.
The **SC25 Reproducibility Report** was located with full metadata: *"Reproducibility Report for SC25 Paper Optimizing Quantum Circuit Mapping to Reduce Inter-Module Communications in Distributed Architectures"*, **single author Kurt H. Maier (Pacific Northwest National Laboratory)**, DOI **`10.1145/3712285.3769463`**, pp. 2280–2281, DBLP key `conf/sc/Maier25`. Its abstract `[abstract]`: *"This reproducibility report provides details about the artifact evaluation done with regards to the Artifact Description and Evaluation appendix of SC25 paper… The work was done as part of the Reproducibility Initiative of SC25. The author is a member of the SC25 Reproducibilty Committee."*
**What this establishes:** the paper carries an **AD/AE appendix**, and an SC25 Reproducibility Committee member performed artifact evaluation under the SC25 Reproducibility Initiative. **What it does not establish:** the report's *body* — which would name the repository, the evaluation hardware, and what was reproduced — is behind the ACM paywall and was not retrievable; likewise the AD/AE appendix itself. The report is also closed access with no OA copy.
**No public repository found.** Targeted searches for "DQTetris" across GitHub, Zenodo, Gitee and figshare returned nothing; searches on all four author names returned nothing attributable; the ECNU Pure record lists no code or dataset link; OpenAlex and Crossref both report the paper and the report as closed with zero OA locations and empty `relation` fields; the SC25 program page shows no artifact badge or DOI.
**No implementation claim was verified for this paper — there are no `[code]` observations for it.**
**Recommended follow-up:** obtain the ACM PDFs of both `10.1145/3712285.3759789` (for the AD/AE appendix, cost model, baselines and benchmarks) and `10.1145/3712285.3769463` (for the repository URL and reproduction outcome) through institutional access. **Those two documents would close essentially every `NOT_FOUND` in this entry** — this is the single highest-value follow-up action identified by the census.

---

## 5. Cross-year comparison: SC 2024 vs SC 2025

**Standing caution: n = 7 and n = 4.** Nothing in this section is a statistical trend. Each observation is labelled `OBSERVED_SHIFT` (defensible from the corpus as a change in *kind*) or `INSUFFICIENT_SAMPLE` (the numbers moved, but two data points cannot support the inference).

### 5.1 The numbers

| Measure | SC 2024 | SC 2025 | Reading |
|---|---|---|---|
| Relevant regular papers | 7 | 4 | `INSUFFICIENT_SAMPLE` |
| Regular papers in volume | 99 | 137 accepted (144 printed) | `[proceedings]` `[official-program]` |
| **Quantum share** | **7.1%** | **2.9%** | Arithmetic is verified; **the interpretation is `INSUFFICIENT_SAMPLE`** |
| Quantum sessions | 3 | 1 | Not directly comparable — SC25 scheduled a uniform "four talks per session", SC24's quantum sessions held 3 / 2 / 3 talks and session II was half approximate-computing |
| Acceptance rate | `NOT_FOUND` | 22% (137/623) | — |
| Papers with public code/data | 4 of 7 (57%) | 3 of 4 (75%) | `INSUFFICIENT_SAMPLE` |
| Papers with an SC Reproducibility Report | 0 | 1 of 4 | See 5.4 |
| Substantive real-QPU use | 0 of 7 | 1 of 4 | `INSUFFICIENT_SAMPLE` |
| Strong or weak scaling reported | 2 of 7 (Atlas, Sycamore; MPS weak-only) | 1 of 4, partly asserted (PTSBE) | `INSUFFICIENT_SAMPLE` |
| Papers naming their classical hardware | 3 of 7 | 3 of 4 | — |

**On the share drop.** Both the numerator and denominator are verified from the publisher volumes, so 7.1% → 2.9% is arithmetic, not estimate. But two years cannot distinguish a decline in submissions, a decline in acceptances, a shift of this work to ASPLOS/ISCA, or ordinary variance in a small population. **SC26 is required to say anything.** It is worth recording that SC26's papers CFP renamed its topic area from "Post-Moore Computing" to **"Post-Moore & Quantum Computing"** — an escalating scope signal that points the opposite way from the share drop.

### 5.2 Topic composition — `OBSERVED_SHIFT` in kind, `INSUFFICIENT_SAMPLE` in magnitude

| Branch | SC 2024 | SC 2025 |
|---|---|---|
| Classical simulation of quantum circuits | **3** (Atlas, Sycamore, MPS) | **1** (PTSBE) |
| Quantum compilation / mapping | **2** (QFT Kernels, PARALLAX) | **1** (DQTetris) |
| QEC / reliability characterization | **1** (Surface Codes) | 0 |
| **Resource management / orchestration** | **0** | **1** (Qonductor) |
| Application / dataset | **1** (LEXIQL) | **1** (QDockBank) |

The defensible statement is about **paper shapes, not proportions**: SC25 introduced **two shapes that were entirely absent from SC24** — a QPU resource-management/orchestration paper (Qonductor) and a pure dataset paper (QDockBank) — while SC24's dominant shape (circuit compilation and simulation, 5 of 7) shrank to 2 of 4. `OBSERVED_SHIFT`.

This matters more than the count. **Qonductor is the first main-track SC paper in this corpus that treats the QPU as a managed HPC-centre resource rather than as a thing to be simulated or compiled for.** That is the `Q_IN_HPC` branch arriving at SC, and it is precisely the branch this research programme is about.

### 5.3 What did *not* change

- **Architecture papers: zero in both years.** No quantum architecture, control microarchitecture, or QEC decoder-hardware paper appeared in either SC. That work is at ISCA/MICRO/HPCA/ASPLOS. `[proceedings]`
- **Real QPUs remained marginal.** Zero substantive real-hardware campaigns in SC24; one in SC25.
- **Baseline discipline stayed weak.** No paper in either year states baseline software versions. Not one SC25 paper compares against an independent third-party system of the same kind.
- **The "N× is usually not a speedup" pattern held in both years.**

### 5.4 A venue-level observation, carefully bounded

The SC25 main volume contains **37 Reproducibility Reports** (pp. 2266–2329, DOIs `.3769434`–`.3769470`), one of which covers a quantum paper. The SC24 enumeration (`.00001`–`.00114`) contains **no comparable item class**. `[proceedings]`
**What can be said:** the SC25 volume publishes reproducibility reports as a distinct archival item class, and the SC24 volume as enumerated does not.
**What cannot be said:** that SC24 had no reproducibility programme. SC has run artifact description/evaluation for years, and the SC24 AD/AE appendices were unreachable from this environment. This is an observation about *volume structure*, not about *policy change*. `[inference]`

---

## 6. SC Quantum-HPC contribution taxonomy

Derived from the 11-paper corpus, not imposed on it. Papers appear more than once where they contribute in more than one way.

```
SC Quantum-HPC (2024–2025)
│
├── Classical simulation of quantum circuits           [4 papers — the largest branch]
│   ├── Distributed multi-GPU statevector              → Atlas (SC24)
│   │     · communication-optimal partitioning by ILP
│   │     · local / regional / global qubit hierarchy
│   │     · GPU-memory → node-DRAM offload
│   ├── Tensor-network contraction at scale            → Surpassing Sycamore (SC24)
│   │     · memory-budget-driven contraction ordering
│   │     · bandwidth-hierarchy-aware decomposition
│   │     · precision and communication quantization
│   ├── Matrix product state                           → MPS Quantum Kernels (SC24)
│   │     · bond dimension as the cost variable
│   │     · CPU-vs-GPU crossover characterization
│   └── Noisy / trajectory simulation throughput       → PTSBE (SC25)
│         · batching to amortize state preparation
│
├── Quantum compilation and mapping                    [3 papers]
│   ├── Kernel-specific closed-form mapping            → QFT Kernels (SC24)
│   │     · eliminate the search, don't accelerate it
│   ├── Hardware-constrained movement scheduling       → PARALLAX (SC24)
│   │     · plus occupancy/replication for throughput
│   └── Inter-module communication minimization        → DQTetris (SC25)
│         · temporal repartitioning with migration cost
│
├── Resource management and orchestration              [1 paper — NEW in SC25]
│   └── Multi-objective QPU fleet scheduling           → Qonductor (SC25)
│         · learned performance prediction
│         · Pareto scheduling, utilization objective
│
├── Reliability and QEC characterization               [1 paper]
│   └── Large-scale fault injection                    → Surface Codes (SC24)
│         · HPC-resilience methodology transplanted
│
└── Applications and datasets                          [2 papers]
    ├── Quantum ML application pipeline                → LEXIQL (SC24)
    └── QPU-generated scientific dataset               → QDockBank (SC25)
```

**Two structural notes.**
1. **The taxonomy has no architecture branch.** Phase 1 predicted this; the census confirms it for both years.
2. **Two of the five branches contain no identifiable HPC mechanism** (Applications/datasets), and one contains methodology rather than performance engineering (Reliability). Only the first three branches are "HPC contribution" in the conventional SC sense.

---

## 7. What makes a quantum paper an SC paper?

This is the census's central question. The answer is not one rule.

### 7.1 Four acceptance pathways, in descending order of methodological demand

**Pathway 1 — HPC *is* the contribution; quantum is the workload.**
Papers: **Atlas**, **PTSBE**, (largely) **Qonductor**.
The quantum novelty is near zero by design. Atlas contains no quantum algorithm, no physics, no approximation — remove the HPC contribution and *nothing remains* `[inference]`. These papers would be publishable at OSDI/ASPLOS/EuroSys on their systems merits alone. **This is the cleanest and most demanding pathway, and it is the one this research programme should target.**

**Pathway 2 — HPC is what makes a quantum claim possible.**
Papers: **Surpassing Sycamore**, **MPS Quantum Kernels**.
The headline claim is quantum ("RCS is not an advantage"; "quantum kernels beat RBF at 165 features"), but the claim only exists because of the machine. Sycamore's argument requires a 32 TB tensor network on 2,304 A100s; the MPS paper's requires a Perlmutter allocation, because neither a QPU nor a statevector simulator can reach 165 qubits. **The HPC content is instrumental rather than novel — and in the MPS case it is explicitly characterization rather than mechanism.**

**Pathway 3 — the HPC problem is the *cost of compilation*.**
Papers: **QFT Kernels**, **PARALLAX**, **DQTetris**.
All three make their SC case by showing the incumbent exact method does not scale — **SATMAP timing out at 2 hours, DPQA at 24 hours** — and replacing it with something polynomial or closed-form. The measured failure of the prior art *is* the HPC problem statement. Note that PARALLAX adds a second, stronger argument (occupancy), and that DQTetris's fit is achieved substantially by *framing* the problem as communication minimization rather than as qubit mapping.

**Pathway 4 — the HPC content is resource consumption and community artifact.**
Papers: **QDockBank**, and (as far as can be determined) **LEXIQL**.
QDockBank reports **no classical hardware at all**, no parallelism, no performance claim, and no systems methodology. Its argument is >60 hours of utility-scale QPU time, a claimed >$1M cost, and a publicly released dataset. **For this paper SC's operative test was scale of resource consumed and community value of the artifact, not nature of the methodological contribution.** `[inference]`

**This fourth pathway is the finding that should change how the rest of the programme reads SC.** It is not an aberration — it is SC's hero-run and community-benchmark tradition extended to a new resource type, where QPU-hours substitute for node-hours. But it means "SC accepted it" does not by itself imply "it contains an HPC contribution."

### 7.2 The three recurring HPC moves

Where a genuine HPC contribution exists, it is almost always one of these — and **never** "we made the quantum part better":

| Move | Instances |
|---|---|
| **Replace a combinatorial search with something that scales** | QFT Kernels (SKETCH-synthesized closed form, *"no compilation time"*); PARALLAX (polynomial heuristic vs DPQA's 24-h timeout); Atlas (ILP with a proven minimum-stage guarantee) |
| **Amortize an expensive step across a batch** | PARALLAX (121 circuit copies per physical shot); PTSBE (statevector prep scales with unique trajectories, not shots) |
| **Make communication the object of optimization** | Atlas (ILP with c=3 inter-node penalty; all communication pushed to stage boundaries); Surpassing Sycamore (int4 quantization of inter-node traffic only); DQTetris (minimize migration *events*, not cut gates) |

### 7.3 Counter-examples and boundary cases — read these carefully

The pattern is only useful if its exceptions are stated:

- **QDockBank** has none of the three moves and no HPC problem at all, and was accepted. `[paper]`
- **Surface Codes** has no HPC *performance* contribution — no hardware reported, no parallelization, no wall-clock, despite 400M fault injections — and was a **Best Student Paper Finalist**. Its pathway is **methodological lineage**: SC's resilience community accepts characterization-by-fault-injection as a contribution in its own right. `[inference]`
- **LEXIQL** was also a Best Student Paper Finalist, and its HPC contribution is **not externally legible at all** from the abstract. Both SC24 finalists in this corpus are papers whose HPC content is weakest by the conventional reading — which should temper any confident claim about what SC "requires."
- **MPS Quantum Kernels** makes **no competitive speedup claim against a rival simulator** — unusual for an SC paper, and a reminder that scale-as-contribution is a valid SC currency.

### 7.4 Every headline number in the corpus, with its real context

This table exists because these are the numbers most likely to be misquoted downstream.

| Paper | Headline | What it actually is |
|---|---|---|
| QFT Kernels | "53% SWAP, 92% depth" vs SABRE | **Circuit-quality ratio, not a speedup.** Same benchmark/architecture/qubit count. No runtime, no hardware, no precision involved |
| Surface Codes | "up to 10%" | Improvement in *probability of correcting a radiation fault* from code/topology choice, same simulator and noise model |
| PARALLAX | "39% / 25% fewer CZ gates" | Circuit-quality ratio vs GRAPHINE / ELDI (both **modified by the authors** to be hardware-compatible) |
| PARALLAX | **"97% execution-time reduction"** | Replication vs **single-copy execution of the same system**, for 8,000 logical shots, on a **simulated** 1,225-atom machine using Table II timing parameters. **Not measured wall-clock, not vs a competitor** |
| Surpassing Sycamore | **"0.29 kWh vs Sycamore's 4.3 kWh"** | A **256-GPU run computing 1 subtask of 2¹²** (0.024%) with post-selection. **The 2,304-GPU figure belongs to the 14.22 s / 2.39 kWh row.** The two energy budgets are drawn at **different system boundaries** — GPU-only NVML on the classical side (cooling/PUE/host power excluded, an `[inference]` from the method, not stated by the paper); unitemized on the Sycamore side, cited to Arute et al. |
| MPS Quantum Kernels | *(none)* | **Makes no competitive N× claim against a rival simulator.** Its only cross-implementation timing is a CPU (ITensors) vs GPU (pytket-cutensornet) crossover running the same MPS algorithm. Do not manufacture a speedup from the 2→32 GPU figure |
| Atlas | "4.0× avg vs HyQuas, 3.2× avg vs cuQuantum" | Defensible. Same hardware, same GPU counts, with an **explicitly stated fair-comparison control** (DRAM offloading disabled). **But precision parity is `CONTEXT_NOT_STATED`, and 7.2 s of ILP+DP preprocessing is excluded** |
| Atlas | "up to 2,126× vs Qiskit" | A **Qiskit framework-overhead artifact**, not a partitioning result `[inference]` |
| Atlas | "13.7× vs 267.9× growth, 1→256 GPUs" | **The most convincing single number in the corpus** — isolates communication scaling rather than kernel speed |
| Qonductor | **"54% lower JCT"** | **NOT against the baseline.** An intra-Pareto-front tradeoff against Qonductor's own fidelity-prioritized extreme. **The vs-FCFS number is 48%** |
| Qonductor | "66% higher utilization" | vs FCFS, **8 Qiskit FakeBackends**, 1,500 apps/h, one simulated hour |
| Qonductor | fidelity cost | **Preprint says 6%; published version says 3%. Use 3%** |
| QDockBank | ">$1M computational cost" | **Derivation `CONTEXT_NOT_STATED`** — unverifiable from 60 QPU-hours |
| PTSBE | **"10⁶×"** | **Shots/second efficiency ratio at 10⁶–10⁷ batch sizes vs the same framework's unbatched mode.** Not a fixed-workload wall-clock speedup, not vs density-matrix simulation, and it buys speed with **correlated sampling** |
| DQTetris | "28% to 75%" | **No stated baseline, benchmark, or module count in any reachable source** |

### 7.5 The short answer

**SC accepts a quantum paper when the quantum system is treated as a machine to be operated, not as physics to be advanced.** Simulation throughput, compilation cost, communication volume, occupancy, scheduling, utilization, energy-to-solution, and reliability characterization are all admissible SC currencies. Fidelity improvements, new ansätze, new optimizers and algorithmic quantum speedups are not — except when they arrive attached to a scarce-resource consumption argument (Pathway 4).

**For this research programme, the operational test on any candidate idea is:** *can the contribution be stated entirely in the vocabulary of classical computer systems — memory, communication, parallelism, scheduling, throughput, cost model — with the quantum device appearing only as a constraint or a workload?* If yes, it is SC-shaped. Atlas is the reference example.

---

## 8. Venue gaps — `VENUE_GAP` only

**These are absences in the SC 2024–2025 main-track corpus. They are NOT research gaps.** A topic absent from SC may be immature, may be a better fit for another community, may not yet have produced a real HPC problem, or may already be well served elsewhere. Each entry below gives the plausible alternative explanations alongside the observation.

| Branch | SC 24/25 | Where it *is* published (Phase 1) | Plausible readings — do not choose one |
|---|---|---|---|
| **QEC decoding as a throughput/latency workload** | **absent** | ASPLOS, ISCA, MICRO, HPCA, EuroSys, IISWC | (a) decoder latency is a µs-scale hardware problem, natively architecture-community work; (b) not yet a *facility* problem because no HPC centre runs a fault-tolerant machine; (c) SC24's Surface Codes paper shows SC takes QEC *reliability characterization*, just not decoder systems. **Note that SC25's PTSBE is explicitly motivated by generating decoder training data — the adjacent problem is already at SC.** |
| **Multi-QPU / distributed quantum execution** | compilation only (DQTetris) | ISCA, ASPLOS, HPCA, ICDCS, QCE | (a) no multi-QPU system exists to run on, so the work is necessarily architectural; (b) the execution-runtime version of the problem may simply not exist yet |
| **Hybrid CPU/GPU/QPU runtime and execution model** | **absent** | OSDI, PLDI, QCE-QSYS, CCGrid, ISC | (a) OSDI has absorbed it (QOS, HyperQ, qTPU); (b) at SC it lives in the **workshops** — SC-W '25 alone has a quantum middle layer, HPC-QC integration case studies, and pulse-level HPCQC stack work |
| **Circuit cutting / knitting** | **absent from the main track** | ASPLOS, ICS, QCE, SC-W | Present in SC-W '25 (*"Orchestrating Quantum-HPC Workflows with Distributed Quantum Circuit Cutting"*), i.e. **workshop-level at SC**, main-track elsewhere |
| **QPU scheduling / resource management** | **arrived once, SC25** | OSDI, ICPP, CCGrid, ICCAD, IPDPS, QCE | Qonductor is the first. Whether it is the start of a branch or a one-off is `INSUFFICIENT_SAMPLE` |
| **Programming models for hybrid quantum-classical** | **absent** | PLDI, CGO, OOPSLA, QCE-QSYS | Natural SIGPLAN territory |
| **HPC-centre QPU integration and operations** | **absent** | **ISC** (near-exclusively), SC-W | Phase 1 found this is essentially an ISC/LRZ-TUM thread. At SC it is workshop content |

**The most striking single absence, stated carefully.** Real-time QEC decoding is structurally a classical HPC problem — a latency-bounded, throughput-bounded, parallelizable computation that must keep pace with a physical device, with a hard bandwidth constraint at the cryogenic boundary — and it is the densest topic at four architecture venues while being absent from SC's main track in both years. **That is a `VENUE_GAP` and nothing more.** The honest alternative readings are all live: the problem may be genuinely architectural rather than facility-scale; it may not become an HPC problem until a machine exists to host it; and SC has demonstrably already accepted its *adjacent* problems (fault-injection characterization in SC24, decoder training-data generation in SC25).

---

## 9. Code / artifact matrix

### 9.1 The matrix

| Paper | Year | Status | URL | Verification verdict | Deep-dive value |
|---|---|---|---|---|---|
| **Atlas** | SC24 | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` | [github.com/quantum-compiler/atlas](https://github.com/quantum-compiler/atlas) · [atlas-artifact](https://github.com/quantum-compiler/atlas-artifact) · Zenodo `10.5281/zenodo.12588145` | **`CONSISTENT`** | **Highest** |
| **MPS Quantum Kernels** | SC24 | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` | [github.com/PabloAndresCQ/qml-cutensornet](https://github.com/PabloAndresCQ/qml-cutensornet) (tag `SC24_paper`) · Zenodo `10.5281/zenodo.12568631` | **`CONSISTENT`** | High |
| **PARALLAX** | SC24 | `PUBLIC_CODE` + `PUBLIC_ARTIFACT` | [github.com/positivetechnologylab/Parallax](https://github.com/positivetechnologylab/Parallax) · Zenodo `10.5281/zenodo.12587550` | **`CONSISTENT`** | High |
| **Qonductor** | SC25 | `PUBLIC_CODE` | [github.com/manosgior/Qonductor-SC25](https://github.com/manosgior/Qonductor-SC25) | **`CONSISTENT`** (Go/Kubernetes layer absent) | **Highest** |
| **QFT Kernels** | SC24 | `PUBLIC_CODE` | [github.com/XiangyuG/qft_on_regular_architectures](https://github.com/XiangyuG/qft_on_regular_architectures) | **`CONSISTENT`** | Medium |
| **PTSBE** | SC25 | `PUBLIC_CODE` (upstreamed) | [NVIDIA/cuda-quantum](https://github.com/NVIDIA/cuda-quantum) → `runtime/cudaq/ptsbe/` · [docs](https://nvidia.github.io/cuda-quantum/0.14.0/using/examples/ptsbe.html) | **`CONSISTENT`** (mechanism); experiments not reproducible | High |
| **QDockBank** | SC25 | `PUBLIC_ARTIFACT` (dataset) | [github.com/qiqi-xingyi/QDockBank_](https://github.com/qiqi-xingyi/QDockBank_) | **`CONSISTENT`** for the dataset; generation pipeline absent | Low |
| **DQTetris** | SC25 | **`UNKNOWN`** — contested, see 9.3 | — (Reproducibility Report: `10.1145/3712285.3769463`) | **`INSUFFICIENT_EVIDENCE`** | Medium (blocked) |
| **LEXIQL** | SC24 | `NO_PUBLIC_ARTIFACT_FOUND` | — | n/a | Low (inaccessible) |
| **Surface Codes** | SC24 | `NO_PUBLIC_ARTIFACT_FOUND` | — | n/a | Medium (blocked) |
| **Surpassing Sycamore** | SC24 | `NO_PUBLIC_ARTIFACT_FOUND` | — | n/a | High (blocked) |

**Totals: 7 of 11 have public code or data; 6 of 11 were repo-verified as `CONSISTENT`; 4 have Zenodo or equivalent archival deposits.**

**Zenodo DOI note.** The DOIs above are **concept DOIs** ("all versions"), which is correct citation practice and is what each repository's own badge displays. Version DOIs also exist and will differ: PARALLAX v1.0.0 = `10.5281/zenodo.12587551` and v1.0.1 = `10.5281/zenodo.13323644`; Atlas's latest-version DOI is `10.5281/zenodo.13334618`. **A source citing a version DOI is not contradicting this document.** `[artifact]`

### 9.2 Papers searched hardest with nothing found

All five artifact-search steps (§2.6) were exhausted for these three. `NO_PUBLIC_ARTIFACT_FOUND` **does not mean code does not exist.**

- **LEXIQL** — the authors' own lab pages are the strongest evidence: the Goodwill Computing Lab publications page shows the LEXIQL entry with a **literally empty `[Artifact]()` link**, and its dedicated Open-Source Artifacts page lists 21 released artifacts spanning HPDC'19–HPCA'26 with **LEXIQL absent**. Eight plausible repository names were probed by `git ls-remote` across two lab orgs; all 404.
- **Surface Codes** — the preprint promises a toolkit and cites it as reference **[39], which reads verbatim: *"T. B.D. (2024) Repository name. To be disclosed after peer review."*** It has not been disclosed since, including in a 2026 follow-up paper. **`QuTAM/QuFI` is the DSN 2022 QuFI paper's injector, not this one** — do not cite it as this paper's artifact.
- **Surpassing Sycamore** — arXiv v1 contains no availability statement of any kind. **`Fanerst/artensor` belongs to Pan & Zhang's PRL 2022 paper**, contains none of this paper's distinguishing systems content, and must not be cited as the SC24 artifact.

### 9.3 A disagreement worth recording

Two independent searches reached **different artifact statuses for DQTetris**: one concluded `PARTIAL` (reasoning that the Reproducibility Report proves an artifact exists and was evaluated), the other `UNKNOWN` (reasoning that no public artifact location was discoverable and no implementation claim could be checked).

**This census records `UNKNOWN`, the more conservative reading**, because `PARTIAL` in this vocabulary means "something was released but not the paper's core system," and **nothing has been confirmed released publicly**. The existence of the AD/AE appendix and the Reproducibility Report is recorded prominently alongside it, since that is genuine and important evidence. The disagreement is documented rather than silently resolved.

### 9.4 An inversion worth noting

**Reproducibility badging and artifact openness are decoupled in this corpus.** The three SC25 papers with public code or data (Qonductor, QDockBank, PTSBE) have **no** Reproducibility Report. The one paper **with** an official SC25 Reproducibility Report (DQTetris) is the one with **no discoverable public artifact and no open-access text**. `[proceedings]` `[inference]`

---

## 10. Recommended deep-dive papers

Five papers, ranked by what they teach about HPC research mechanism, weighted toward those with verifiable public code.

### 1. Atlas — *Hierarchical Partitioning for Quantum Circuit Simulation on GPUs* (SC24)
**Why:** the purest instance of "quantum as workload, HPC as contribution" in the corpus, and the closest to this programme's own background in topology-aware placement and communication minimization.
**Mechanisms to learn:** ILP formulation of a partitioning problem with an explicit inter-node cost weight; proving minimality of a schedule; DP over kernel groupings with two competing execution strategies; NCCL all-to-all for global-index shuffles; a GPU/node-DRAM/cluster memory hierarchy with Legion offload; **and the weak-scaling methodology that produced the corpus's most convincing number (13.7× vs 267.9× growth to 256 GPUs).**
**Code:** `PUBLIC_CODE` + Zenodo, verified `CONSISTENT` — including the Quartz submodule where `compute_qubit_layout_with_ilp(…, num_local_qubits, num_regional_qubits, …)` lives.
**Watch for:** precision parity with baselines is `CONTEXT_NOT_STATED`, and 7.2 s of preprocessing is excluded from the reported speedups.

### 2. Qonductor — *A Cloud Orchestrator for Quantum Computing* (SC25)
**Why:** the only SC main-track paper in this corpus that treats a QPU as a managed shared resource, which is exactly the `Q_IN_HPC` branch this programme targets. It is also the closest existing analogue to PBS/Slurm integration for QPUs.
**Mechanisms to learn:** learned performance prediction as a scheduling input (regression on circuit features, R²=0.998 execution time / 0.976 fidelity); NSGA-II multi-objective scheduling with an operator-side utilization objective; pseudo-weight MCDM as the tradeoff knob; trace-driven simulation as an evaluation methodology for schedulers.
**Code:** `PUBLIC_CODE`, verified `CONSISTENT`, with figure-to-script mapping documented and 334 MB of committed data.
**Watch for:** the headline 54% is an intra-Pareto tradeoff, not a baseline comparison (48% is); the evaluation is eight FakeBackends against a single FCFS baseline; the Go/Kubernetes orchestrator is not in the artifact.

### 3. Surpassing Sycamore (SC24)
**Why:** the corpus's only energy-to-solution argument and its largest-scale system (2,304 A100s), and a masterclass in bandwidth-hierarchy-aware decomposition. It is also a cautionary study in how a headline comparison can be drawn across incommensurable system boundaries.
**Mechanisms to learn:** choosing contraction order against an explicit memory budget (FLOPs inversely proportional to allowed memory); three-level global/multi-node/device decomposition matched to NVLink-vs-InfiniBand bandwidths; **applying int4 quantization to inter-node communication only**; custom complex-fp16 einsum; NVML-based energy accounting.
**Code:** `NO_PUBLIC_ARTIFACT_FOUND` — this is the deep-dive's main limitation, and it is notable that the corpus's most contested claim is its least reproducible.
**Watch for:** the 0.29 kWh figure is a 256-GPU, one-subtask-of-2¹² run; the classical energy excludes cooling, host power and PUE; Sycamore's 4.3 kWh is unitemized.

### 4. PARALLAX (SC24)
**Why:** the clearest transplant of a classical accelerator idea (batching for occupancy) into quantum execution, and the most explicit compile-time-scalability argument in the corpus.
**Mechanisms to learn:** replacing an SMT formulation with a polynomial heuristic and stating the complexity; the structural trick (one atom per AOD row/column pair) that dissolves a hardware constraint rather than working around it; recursive obstruction resolution with a bounded iteration count; **spatial replication so one physical shot yields many logical shots.**
**Code:** `PUBLIC_CODE` + Zenodo, verified `CONSISTENT`, with both baselines vendored in-repo.
**Watch for:** the 97% is against single-copy execution of the same system on a simulated machine; two baselines were modified by the authors.

### 5. PTSBE (SC25)
**Why:** it converts QEC decoder training data into a supercomputer workload — one of the most concrete near-term Quantum-HPC couplings — and demonstrates a reusable restructuring pattern. It is also the corpus's only example of a technique upstreamed into production HPC software.
**Mechanisms to learn:** decoupling stochastic sampling from state evolution so cost scales with unique trajectories rather than shots; trajectory deduplication with multiplicity; shot-allocation strategies; retaining error provenance so generated shots are *labeled* training data.
**Code:** `PUBLIC_CODE` via CUDA-Q `runtime/cudaq/ptsbe/`, verified `CONSISTENT` for the mechanism.
**Watch for:** the 10⁶× is an efficiency ratio against the same framework's unbatched mode; correlated sampling is the price; no noise-model parameters are disclosed for the headline runs; multi-node scaling is asserted, not measured.

**Deliberately not recommended for deep dive:** QDockBank (no HPC mechanism to learn), LEXIQL (inaccessible), Surface Codes and DQTetris (both blocked — worth revisiting with institutional access, and DQTetris in particular would repay it).

---

## 11. Implications for the next venue census

Phase 1's queue puts **ASPLOS** next, then **ISC**, then **ISCA**, with **ICS** in Wave 2. This census supports that ordering and sharpens what to look for.

### 11.1 Recommended next venue: ASPLOS

Three reasons, in order:
1. **It is where Pathway-1 papers concentrate.** Atlas is the SC corpus's purest "HPC is the contribution" paper, and Phase 1 found ASPLOS has the highest quantum share of any venue-year surveyed (7.9% in 2026) with dedicated sessions in all three years. The SC corpus gives 11 papers; ASPLOS 2024–2026 gives ~31.
2. **It is where the artifacts are.** Phase 1 identified BQSim (GPU batched decision-diagram simulation) and Micro Blossom (FPGA MWPM decoding) at ASPLOS 2025, both with public code — the same profile as Atlas.
3. **It contains the branch SC does not have.** QEC decoding as a systems problem is dense at ASPLOS and absent at SC. Censusing ASPLOS immediately after SC puts the sharpest `VENUE_GAP` from §8 under direct examination.

**ISC should follow ASPLOS rather than precede it**, because ISC's distinctive thread (HPC-centre QPU integration and operations) is the branch SC lacks *within its own community*, and it will read better against both poles. **ICS is the third priority** — Phase 1 found ICS 2026 ran a five-paper "Quantum Computing" session, which is larger than either SC year in this census and the fastest-growing HPC signal found.

### 11.2 Questions to carry into every subsequent census

1. **Which of the four acceptance pathways (§7.1) does each paper use?** This is now the primary analytic axis. Specifically: does the venue have a Pathway-4 equivalent — does it accept resource consumption in place of methodology?
2. **Apply the A/B/C split from the start.** The Quantum problem / HPC problem / SC contribution separation was the most productive instrument in this census, and it is the one that exposed QDockBank and Surface Codes.
3. **Does the venue's quantum work use real QPUs?** SC's answer was 1 of 11. If ASPLOS's answer differs materially, that is a substantive community difference, not a detail.
4. **Does the venue report strong/weak scaling?** SC's answer was 3 of 11, weakly. This is a measurable proxy for how much "HPC" is in the HPC contribution.
5. **Restore the context of every headline number before recording it** (§7.4). In this corpus, most N× figures were circuit-quality ratios, self-comparisons, or simulated models. Expect the same elsewhere and check for it explicitly.
6. **Check baseline discipline.** No SC paper in either year stated baseline software versions; no SC25 paper compared against an independent third-party system. If ASPLOS is materially better, that is worth knowing before choosing a target venue.
7. **Look for the same three HPC moves** (§7.2) — search elimination, batching/amortization, communication as objective. If a venue's quantum papers use *different* moves, that difference defines the venue.

### 11.3 A specific comparison to set up

Three near-identical problems now have a paper at both poles. Reading these pairs side by side will characterize the SC-vs-architecture boundary faster than any aggregate count:

| Problem | SC paper | Architecture-venue counterpart (Phase 1) |
|---|---|---|
| GPU circuit simulation | **Atlas** (SC24) — distributed statevector, ILP partitioning | **BQSim** (ASPLOS 2025) — GPU batched decision diagram |
| Noisy-simulation cost | **PTSBE** (SC25) — pre-trajectory sampling, batching | **Accelerating Simulation of Quantum Circuits under Noise via Computational Reuse** (ISCA 2025) |
| QPU scheduling / multi-tenancy | **Qonductor** (SC25) — cloud orchestrator | **QOS** and **Quantum Virtual Machines** (OSDI 2025), **Qoncord** (MICRO 2024), **AQUA** (IPDPS 2025) |

The Qonductor↔QOS pair is especially instructive: **same group (TU Munich / Bhatotia), adjacent problems, two venues, same year.** Comparing what each paper foregrounds will show precisely how the same research is dressed for SC versus for OSDI.

---

## 12. Sources

All URLs checked 2026-09-06.

**Official SC program and volume metadata**
[SC24 Papers CFP](https://sc24.supercomputing.org/program/papers/) · [SC24 Quantum and Approximate Computing I](https://sc24.conference-program.com/session/?sess=sess385) · [II](https://sc24.conference-program.com/session/?sess=sess387) · [III](https://sc24.conference-program.com/session/?sess=sess386) · [Analysis of HPC Systems (DOI-gap session)](https://sc24.conference-program.com/session/?sess=sess388) · [Sparsity and Quantization in ML](https://sc24.conference-program.com/session/?sess=sess398) · [SC25 Papers CFP](https://sc25.supercomputing.org/program/papers/) · [SC25 session sess164 "Quantum Computing and Simulation"](https://sc25.conference-program.com/session/?sess=sess164) · [SC25 papers-scheduling post — 137/623/22%](https://sc25.supercomputing.org/2025/09/you-asked-we-listened-minimizing-overlap-in-papers-scheduling/) · [SC25 Awards](https://sc25.supercomputing.org/program/awards/) · [Crossref REST API](https://api.crossref.org/) (container enumeration for both volumes) · [SC24 Gordon Bell finalists (HPCwire)](https://www.hpcwire.com/off-the-wire/presenting-the-finalists-for-the-2024-gordon-bell-prize/)

**SC 2024 papers**
LEXIQL — [ACM DL record](https://dl.acm.org/doi/10.1109/SC41406.2024.00073) · [SC24 program entry](https://sc24.conference-program.com/presentation/?id=pap313&sess=sess385) · [Goodwill Computing Lab publications](https://goodwillcomputinglab.github.io/publications/) · [lab open-source artifacts](https://goodwillcomputinglab.github.io/open_source/) · [Tirthak Patel publications](https://www.tirthakpatel.com/publications)
QFT Kernels — [arXiv:2408.11226](https://arxiv.org/abs/2408.11226) · [artifact repo](https://github.com/XiangyuG/qft_on_regular_architectures)
Surface Codes — [arXiv:2407.10841](https://arxiv.org/abs/2407.10841) · [ACM DL record](https://dl.acm.org/doi/10.1109/SC41406.2024.00075) · [QuTAM/QuFI — different paper](https://github.com/QuTAM/QuFI) · [HiCREST lab](https://hicrest.unitn.it/mars/) · [2026 follow-up arXiv:2602.06202](https://arxiv.org/abs/2602.06202)
PARALLAX — [arXiv:2409.04578](https://arxiv.org/abs/2409.04578) · [artifact repo](https://github.com/positivetechnologylab/Parallax) · Zenodo `10.5281/zenodo.12587550`
Surpassing Sycamore — [arXiv:2407.00769](https://arxiv.org/abs/2407.00769) *(different title)* · [Fanerst/artensor — different paper](https://github.com/Fanerst/artensor)
MPS Quantum Kernels — [arXiv:2411.09336](https://arxiv.org/abs/2411.09336) · [repo](https://github.com/PabloAndresCQ/qml-cutensornet) · [Zenodo 10.5281/zenodo.12568631](https://zenodo.org/doi/10.5281/zenodo.12568631)
Atlas — [arXiv:2408.09055 (Extended Version)](https://arxiv.org/abs/2408.09055) · [repo](https://github.com/quantum-compiler/atlas) · [artifact repo](https://github.com/quantum-compiler/atlas-artifact) · [Quartz submodule](https://github.com/quantum-compiler/quartz) · [Zenodo 10.5281/zenodo.12588145](https://zenodo.org/doi/10.5281/zenodo.12588145) · [SC24 program entry](https://sc24.conference-program.com/presentation/?id=pap183&sess=sess386)

**SC 2025 papers**
Qonductor — [arXiv:2408.04312](https://arxiv.org/abs/2408.04312) · [published SC25 PDF](https://franciscoromao.github.io/files/Qonductor_sc25.pdf) · [artifact repo](https://github.com/manosgior/Qonductor-SC25) · [TUM FIS record](https://portal.fis.tum.de/en/publications/qonductor-a-cloud-orchestrator-for-quantum-computing/) · [SC25 program entry](https://sc25.conference-program.com/presentation/?id=pap193&sess=sess164) · [TUM DSE group](https://dse.in.tum.de/quantum-software-systems-group/)
QDockBank — [arXiv:2508.00837](https://arxiv.org/abs/2508.00837) · [dataset repo (canonical)](https://github.com/qiqi-xingyi/QDockBank_) *(the preprint's `QDockBank/QDockBank_` path is a redirect)*
PTSBE — [arXiv:2504.16297](https://arxiv.org/abs/2504.16297) · [CUDA-Q PTSBE documentation](https://nvidia.github.io/cuda-quantum/0.14.0/using/examples/ptsbe.html) · [CUDA-Q 0.14 release blog](https://nvidia.github.io/cuda-quantum/blogs/blog/2026/03/16/cudaq-0.14/) · [NVIDIA/cuda-quantum](https://github.com/NVIDIA/cuda-quantum)
DQTetris — [SC25 program entry](https://sc25.conference-program.com/presentation/?id=pap226&sess=sess164) · [ECNU Pure record](https://pure.ecnu.edu.cn/en/publications/optimizing-quantum-circuit-mapping-to-reduce-inter-module-communi/) · [Reproducibility Report metadata (OpenAlex)](https://api.openalex.org/works/doi:10.1145%2F3712285.3769463)

---

## Appendix A — False positives and borderline cases

Understanding what SC's quantum boundary *excludes* is as informative as what it includes. Every item below was examined and rejected, with the reason recorded.

### A.1 Classical quantum chemistry / many-body physics — the dominant false-positive class

These papers use "quantum" in the physics sense (quantum-mechanical simulation on classical computers). They are classical HPC and are **not** quantum computing. Several are Gordon Bell finalists, which makes them prominent and therefore easy to mis-include.

| Year | Title | DOI | Why initially relevant | Why excluded |
|---|---|---|---|---|
| SC24 | Pushing the Limit of Quantum Mechanical Simulation to the Raman Spectra of a Biological System with 100 Million Atoms | `10.1109/SC41406.2024.00011` | "Quantum Mechanical Simulation" in the title; Gordon Bell finalist | Classical DFT/electronic-structure simulation |
| SC24 | Breaking the Million-Electron and 1 EFLOP/s Barriers: Biomolecular-Scale Ab Initio Molecular Dynamics Using MP2 Potentials | `.00015` | Ab initio quantum chemistry; **2024 Gordon Bell Prize winner** | Classical MP2 |
| SC24 | Many-Body Electronic Correlation Energy using Krylov Subspace Linear Solvers | `.00066` | "Many-Body", Krylov — matches quantum-algorithm vocabulary | Classical electronic structure / linear algebra |
| SC24 | Enabling 13K-Atom Excited-State GW Calculations via Low-Rank Approximations and HPC on the New Sunway Supercomputer | `.00067` | GW, excited states | Classical electronic structure |
| SC24 | Towards Exascale Simulations of Nanoelectronic Devices in the GW Approximation | `.00069` | "quantum transport" adjacency | Classical device simulation |
| SC25 | Ab-initio Quantum Transport with the GW Approximation, 42,240 Atoms, and Sustained Exascale Performance | `10.1145/3712285.3771784` | "Quantum Transport"; Gordon Bell finalist | Classical electronic structure |
| SC25 | Multiscale Light-Matter Dynamics in Quantum Materials: From Electrons to Topological Superlattices | `.3771785` | "Quantum Materials"; Gordon Bell finalist | Classical materials physics |
| SC25 | Advancing Quantum Many-Body GW Calculations on Exascale Supercomputing Platforms | `.3772093` | "Quantum Many-Body" | Classical many-body GW |
| SC25 | Matrix Is All You Need: Rearchitecting Quantum Chemistry to Scale on AI Accelerators | `.3759829` (pp. 2126–2142) | "Quantum Chemistry" + accelerators | Classical quantum chemistry on AI accelerators. Session "Algorithms", not the quantum session |
| SC25 | NNQS-SCI: Tackling Trillion-Dimensional Hilbert Space with Adaptive Neural Network Quantum States | `.3759800` (pp. 1646–1660) | "Quantum States", "Hilbert Space" | Classical variational Monte Carlo with neural ansätze. Session "Applications: Atomistic Modeling" |

### A.2 The session-name trap — the most dangerous SC24 false positive

| Title | DOI | Why initially relevant | Why excluded |
|---|---|---|---|
| **HPAC-ML: A Programming Model for Embedding ML Surrogates in Scientific Applications** | `10.1109/SC41406.2024.00078` | **It sits inside the session literally named "Quantum and Approximate Computing II"**, immediately before PARALLAX | It is the *approximate computing* half of the session. **No quantum content whatsoever.** Anyone censusing SC24 from session names rather than paper content will include this |

### A.3 Vocabulary collisions

| Year | Title | DOI | Why initially relevant | Why excluded |
|---|---|---|---|---|
| SC24 | MixQ: Taming Dynamic Outliers in Mixed-Precision Quantization by Online Prediction | `.00080` | "Quantization" — adjacent DOI to the quantum block | Numeric precision, not quantum |
| SC24 | Hydrogen: Contention-Aware Hybrid Memory for Heterogeneous CPU-GPU Architectures | `.00017` | Matched "hybrid" and "heterogeneous" | CPU-GPU memory system |
| SC24 | Accelerated Atomistic Kinetic Monte Carlo Simulations of Resistive Memory Arrays | `.00097` | Emerging-hardware adjacency (ReRAM) | Classical device/materials simulation |
| SC25 | Δ-Motif: Subgraph Isomorphism at Scale via Data-Centric Parallelism | *(not in proceedings)* | The SC25 schedule tags it **"Quantum & Other Post Moore Computing Technologies"**, and the author is at Q-CTRL Inc | **Exhibitor Forum presentation** (`exforum114`/`sess491`), **not in the proceedings** — absent from all 433 enumerated items. It is a GPU/RAPIDS graph-processing talk. See Appendix B.3 for the tag correction this produced |

### A.4 Workshop papers that would be tempting to include

These are **SC-W '25 (`10.1145/3731599.`) workshop papers**, structurally excluded. They are listed because several are more directly "Quantum-HPC" by topic than the main-track papers, which is itself a finding about where this work currently sits at SC.

| DOI | Title |
|---|---|
| `.3767547` | Orchestrating Quantum-HPC Workflows with Distributed Quantum Circuit Cutting |
| `.3767554` | An HPC-Inspired Blueprint for a Technology-Agnostic Quantum Middle Layer |
| `.3767551` | First Practical Experiences Integrating Quantum Computers with HPC Resources: A Case Study With a 20-qubit Superconducting Quantum Computer |
| `.3767549` | Towards a user-centric HPC-QC environment |
| `.3767552` | Tackling the Challenges of Adding Pulse-level Support to a Heterogeneous HPCQC Software Stack |
| `.3767553` | Scaling Hybrid Quantum–HPC Applications with the Quantum Framework |
| `.3767548` | A Simulation Framework for Workload Management in Hybrid Quantum-HPC Cloud System |
| `.3767546` | Towards Supporting QIR |
| `.3767540` | Post-Variational Quantum Neural Networks on a Hybrid HPC-QC System |
| `.3767456` | Rapid Quantum Network Simulation Design with a Path to Scalable Execution |
| `.3767550` | A Practical Quantum Solver for Multidimensional Partial Differential Equations |
| `.3769278` | Implications of Full-System Modeling for Superconducting Architectures |

**Note the page-number trap:** the SC-W volume repaginates from 1, so its page numbers collide with the main volume's. **DOI prefix, not page number, is the only safe discriminator.**

### A.5 Borderline inclusions — papers kept, with the argument against recorded

| Paper | Case for inclusion | Case against |
|---|---|---|
| **QDockBank** (SC25) | Real utility-scale QPU campaign; `Q_FOR_HPC` / `FUTURE_WORKLOAD` by execution-pattern relevance; a released community dataset | **No HPC content whatsoever** — no classical hardware, no parallelism, no performance claim. Kept because it is unambiguously a main-track regular paper about quantum computing, and because **excluding it would hide the census's most important finding about SC's boundary** |
| **LEXIQL** (SC24) | A quantum application pipeline designed against device constraints; Best Student Paper Finalist | HPC contribution not externally legible; abstract-level evidence only. Kept for the same reason as QDockBank |
| **Surface Codes** (SC24) | QEC with system/reliability implications; 400M-injection campaign | No HPC performance contribution; no compute hardware reported. Kept — the campaign scale and the HPC-resilience methodology are genuine, and it is a distinct acceptance pathway |

---

## Appendix B — `PHASE1_CORRECTION_CANDIDATE` items

Per the Phase 2 brief, conflicts with the Phase 1 documents are recorded here first and applied to those documents only where verification is sufficient. Applied changes are listed in Appendix C.

### B.1 Confirmed errors — recommend applying

**B.1.1 — SC24 session structure.** Phase 1 (`QUANTUM_HPC_VENUE_MAP.md` §4.1) states SC24's quantum papers sat in *"two consecutive session blocks"* at `.00073/74/75` and `.00085/86/87`, while separately listing PARALLAX at `.00079`. **This is internally inconsistent and factually wrong.** SC24 had **three** sessions — *Quantum and Approximate Computing I / II / III* — with 3 / 2 / 3 talks, and session II's other talk (`.00078`, HPAC-ML) is an approximate-computing paper, not a quantum one. `[official-program]` **Severity: moderate** — it produced a false model of the venue and would mislead a future census.

**B.1.2 — SC25 Papers-track topic tag.** Phase 1 (§4.1 and the master table) reports SC25 using the tag *"Quantum & Other Post Moore Computing Technologies"*. **That tag belongs to the SC25 Exhibitor Forum taxonomy, not the Papers track.** SC25 Papers use two schedule tags, **"Post-Moore Computing"** and **"Quantum Computing"**; the CFP topic area is **"Post-Moore Computing"** with "Quantum computing" as a bullet — **there is no standalone "Quantum Computing" CFP area**, so the two tags are peers in the *schedule* taxonomy, not in the CFP taxonomy. The disputed string was independently located on Exhibitor Forum items (e.g. `exforum122`, session "Quantum Discussions Part 2", and `exforum114`/Δ-Motif). `[official-program]` **Severity: moderate** — citing it as the Papers-track tag is wrong.

**B.1.3 — SC25 Gordon Bell block extent.** Phase 1 states *"The pp. 1–59 block corresponds to Gordon Bell finalists."* The Gordon Bell / GB-Climate block is **pp. 1–136, 11 papers**, DOI suffixes `.3771783`–`.3771790`, `.3771989`, `.3772093`, `.3772094`. pp. 48–59 sits inside it. `[proceedings]` **Severity: minor.**

**B.1.4 — Truncated title.** Phase 1 lists *"Multiscale Light-Matter Dynamics in Quantum Materials"*. The verbatim title is *"Multiscale Light-Matter Dynamics in Quantum Materials: **From Electrons to Topological Superlattices**"*. `[proceedings]` **Severity: minor.**

**B.1.5 — Artifact statuses substantially out of date.** Phase 1 recorded artifact status as `UNKNOWN` for essentially all SC papers, with `PUBLIC_ARTIFACT` only for the ECNU mapping paper (inferred from its Reproducibility Report). The census establishes **7 of 11 have public code or data, 6 verified `CONSISTENT` at repo level, and 4 have Zenodo deposits.** `[code]` `[artifact]` **Severity: high for usefulness** — this is the largest single improvement the census produces, and it changes which SC papers are deep-dive candidates.

**B.1.6 — Attribution precision on the MPS paper.** Phase 1 describes *"MPS-based quantum-kernel ML at scale (Quantinuum)"*. The **first author, Mekena Metcalf, is at HSBC Holdings** (listed as Berkeley Lab on the Zenodo deposit), with Quantinuum co-authors Andrés-Martínez and Fitzpatrick. `[proceedings]` **Severity: minor.**

### B.2 Enrichments — new facts, not corrections

- **SC24 volume totals:** 99 regular technical papers (`.00016`–`.00114`), plus 9 Gordon Bell / GB-Climate finalists and 6 front-matter items = 114 records. **Quantum share 7 / 99 = 7.1%.** SC24's acceptance rate remains `NOT_FOUND`. `[proceedings]`
- **SC25 volume totals:** 137 accepted from 623 submissions = **22%**; the volume prints 144 papers plus 37 Reproducibility Reports. **Quantum share 4 / 137 = 2.9%.** `[official-program]` `[proceedings]`
- **SC24 awards:** LEXIQL (`.00073`) and Surface Codes (`.00075`) were both **Best Student Paper Finalists**. `[official-program]`
- **SC25 session details:** *"Quantum Computing and Simulation"*, `sess164`, chair **Angel Yanguas-Gil (Argonne National Laboratory)**. `[official-program]`
- **SC25 awards:** no quantum paper won or was a finalist for Best Paper, Best Student Paper, or either Gordon Bell Prize. `[official-program]`
- **Preprint title divergence:** Surpassing Sycamore's arXiv version (2407.00769) is titled *"Achieving Energetic Superiority Through System-Level **Quantum** Circuit Simulation"*; Atlas's arXiv version is an **Extended Version** whose theorems may not all appear in the SC24 paper. **Anyone citing from arXiv should note both.**

### B.3 Recorded but NOT recommended for application

- **Phase 1's "What appears" paragraph for SC** mixes SC24 and SC25 papers without year attribution — it lists Atlas, Surpassing Sycamore and the MPS paper (all SC24) alongside NVIDIA's batched pre-trajectory sampling (SC25) in one sentence. Read as a description of "SC" generally this is not wrong, but it is ambiguous. **Recommendation: leave as is** — the paragraph is explicitly a venue-level summary, and the master table carries the per-year counts correctly.
- **Phase 1's SC24 count (7) and SC25 count (4) are both confirmed correct**, as is the SC25 contiguous-block claim (pp. 728–788), the `SC41406`/`SCW63240` and `3712285`/`3731599` discriminators, and the five SC25 classical-chemistry false positives. **No change needed.**

---

## Appendix C — Changelog of Phase 1 document edits

Applied on 2026-09-06 following this census. Only items verified against an official program or publisher record were applied; everything else remains a candidate in Appendix B.

| # | File | Change | Basis |
|---|---|---|---|
| C1 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 (SC) | "two consecutive session blocks" → **three sessions**, *Quantum and Approximate Computing I / II / III* (3/2/3 talks), with the HPAC-ML session-name trap noted | B.1.1 `[official-program]` |
| C2 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 census warning | Added the SC25 Papers-track tag correction: **"Post-Moore Computing" + "Quantum Computing"**, not the Exhibitor Forum's "Quantum & Other Post Moore Computing Technologies" | B.1.2 `[official-program]` |
| C3 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 census warning | SC25 Gordon Bell block corrected pp. 1–59 → **pp. 1–136 (11 papers)**; "Multiscale Light-Matter Dynamics…" title completed | B.1.3, B.1.4 `[proceedings]` |
| C4 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 + master table | Added verified volume totals and quantum shares (SC24 7/99 = 7.1%; SC25 4/137 = 2.9%, 22% acceptance) and the two SC24 Best Student Paper Finalists | B.2 `[proceedings]` `[official-program]` |
| C5 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 | Artifact status updated from "UNKNOWN" to the census result: **7 of 11 public, 6 repo-verified, 4 Zenodo deposits**, with a pointer to the census matrix | B.1.5 `[code]` `[artifact]` |
| C6 | `QUANTUM_HPC_VENUE_MAP.md` §4.1 | MPS paper attribution corrected: **HSBC first author** with Quantinuum co-authors | B.1.6 `[proceedings]` |
| C7 | `QUANTUM_HPC_VENUE_MAP.md` Appendix C | New subsection C.6 recording that Phase 2 verified Phase 1's SC counts and listing what changed | this census |
| C8 | `QUANTUM_HPC_RESEARCH_QUEUE.md` | SC entry marked **CENSUS COMPLETE** with the result; SC census mechanics updated with the three-session structure and the HPAC-ML trap; ASPLOS rationale sharpened per §11.1 | §11 |

---

## Appendix D — Verification pass record

Per the Phase 2 brief, the draft and the verification pass were kept **explicitly separate**. The draft in §§1–12 and Appendices A–C was written first from four independent research passes; a fifth, adversarial pass then re-verified the load-bearing claims from scratch against primary sources, without access to the reasoning that produced them. This appendix records what that pass checked and what it changed, because Phase 1 had a precedent of precision errors surviving into a finished document.

### D.1 Scope of the verification pass

**37 discrete claims** across four groups: (1) bibliographic accuracy of all 11 papers — title, year, authors, DOI, main-track status; (2) seven program-structure claims — session names, chairs, dates, tags, awards, volume totals; (3) nine quantitative claim-sets, verified against the original papers; (4) nine artifact claims including three **negative** claims.

### D.2 Confirmed without change

- **All 11 papers**: titles, years, author lists, DOIs, page ranges, and main-track status. Every one returns `type: proceedings-article` in the correct container. No workshop, poster, SRC, doctoral-showcase or exhibitor item is present in the census.
- **The SC24 three-session structure** and every paper-to-session assignment, including the HPAC-ML session-name trap.
- **The SC25 session** name, chair, date, room and four-paper membership — independently corroborated by Argonne's own SC participation page listing Yanguas-Gil as chair.
- **The SC25 topic-tag correction** (both halves), **SC24's volume structure** (`.00001`–`.00114`, `.00115` = 404, 99 regular papers), and **SC25's 137/623/22%**.
- **Q1, Q2, Q3, Q6, Q8, Q9 in full** — including the Surface Codes distance inversion, PARALLAX's 97%-vs-single-copy caveat, Atlas's every speedup figure and its fair-comparison statement, PTSBE's baseline identity, and **QDockBank's negative check** (no occurrence of HPC, supercomputer, parallelism, GPU, cluster, or classical computing hardware anywhere in the paper).
- **Q4's contested Sycamore table**: the 0.29 kWh / 17.18 s headline run did use **256 GPUs and compute 1 subtask of 2¹²**, and the 2,304-GPU run is the 14.22 s / 2.39 kWh row.
- **Q7's Qonductor correction**: the 54% is an intra-Pareto tradeoff, the vs-FCFS number is ~48%, and the preprint/published divergence is real.
- **All artifact URLs**, including the three negative claims. Reference [39] of arXiv 2407.10841 was verified verbatim as *"T. B.D. (2024) Repository name. Tobedisclosedafterpeerreview."*

### D.3 Corrections applied

| # | Issue | Correction | Where |
|---|---|---|---|
| **D1** | MPS paper's qubit range stated as 100–165 | **15–165** — the sweep runs 15, 50, 100, 165 | §3.6 |
| **D2** | MPS paper described as making "no speedup claim against any **external** baseline" — overstated, since the CPU side is the third-party **ITensors** library | Reworded to "**no *competitive* speedup claim against a rival quantum simulator**", with the ITensors point and the paper's own fairness caveat added | §3.6, §7.3, §7.4 |
| **D3** | Sycamore energy exclusions (cooling/PUE/host power) implied to be a paper disclosure | Retagged as **`[inference]` from an NVML-device-only methodology**, with an explicit note that the paper never discusses PUE, cooling or host power | §3.5, §7.4 |
| **D4** | QDockBank repo cited as `github.com/QDockBank/QDockBank_` (the preprint's URL) | Canonical URL is **`github.com/qiqi-xingyi/QDockBank_`**; the preprint path resolves only via an owner-transfer redirect, and the `QDockBank` account holds two differently-named repos | §4.2, §9.1, §12 |
| **D5** | LEXIQL's Best Student Paper Finalist status cited to the program generally | Badge renders **only on the presenter page** `?uid=304504`, not on the paper's presentation page or either lab site; that URL is now cited explicitly, with the contrast to Surface Codes (badge on the session page) noted | §3.1 |

### D.4 Findings the verification pass strengthened

- **The Qonductor divergence is worse than a changed number.** The published abstract's "3% execution quality" is a **vs-FCFS fidelity delta**, while the published *body* still reports "6% lower fidelity leads to 54% lower JCT" as a Pareto-front tradeoff. **The abstract appears to splice two different measurements.** The census now says to quote the body, not the abstract. The arXiv v1 **title** also differs.
- **The "8 FakeBackends" count** is a join of two separate statements in the paper, not the paper's own phrasing — now flagged.
- **SC25 has no standalone "Quantum Computing" CFP area** — "Post-Moore Computing" and "Quantum Computing" are peers in the *schedule* taxonomy only. B.1.2 sharpened accordingly.

### D.5 Enrichments added at verification

SC24 session chairs (Helena Liebelt / Flavio Vella / Tirthak Patel); a title-casing warning for LEXIQL/PARALLAX/QDockBank and the three preprint-title divergences; and a Zenodo concept-vs-version DOI note (PARALLAX's `12587550` concept DOI is correct; `12587551` and `13323644` are version DOIs, and a source citing those is not contradicting this document).

### D.6 What the verification pass could not close

The two closed-access papers — **LEXIQL** and **DQTetris** — remain unreadable from this environment, and no verification could change that. Their entries are honestly thin and are labelled as such throughout. **Obtaining the ACM PDFs of `10.1145/3712285.3759789` and its Reproducibility Report `10.1145/3712285.3769463` through institutional access remains the single highest-value follow-up identified by this census.**

---

## Appendix E — Cross-reference to the ASPLOS 2024–2026 census

**Added 2026-09-06. This appendix is a cross-reference only. Nothing in §§1–12 or Appendices A–D was altered on the strength of ASPLOS evidence.** Where an ASPLOS finding bears on an SC claim, it is recorded here and the SC claim is left standing on its own sources.

**Companion documents:** `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`.

### E.1 Where the two censuses meet

| Dimension | SC 2024–2025 | ASPLOS 2024–2026 | Reading |
|---|---|---|---|
| Corpus | 11 regular papers | 36 regular papers | ASPLOS carries a sustained double-digit quantum population every year; SC has 7 and 4. |
| **Compilation argument** | **3 of 3** papers argue compile-time scalability; the incumbent exact method's measured failure (SATMAP at 2 h, DPQA at 24 h) *is* the problem statement | **2 of 10** argue it centrally (QTurbo, PowerMove); 7 argue output quality or use another cost model | **The sharpest difference between the two venues.** GUOQ is the clean inversion — compile time as experimental *control*, not dependent variable. |
| Public artifact rate | 7 of 11 (**64%**) | 22 of 36 (**61%**) | Statistically indistinguishable, **despite ASPLOS running formal Artifact Evaluation and SC not requiring one.** Process does not move the rate. |
| Artifact *kind* | simulation and compiler code | ~16 of ~22 Python/C++ simulation and compiler code; **exactly one HDL artifact in 36 papers** | An architecture conference produces the same artifact profile as an HPC conference. |
| QEC decoding | **absent** | densest single branch (11 papers) | `VENUE_GAP`, recorded as such in both documents. **Not** a research gap. |
| Denominator hazard | SC: session-name trap (`.00078` HPAC-ML sits in "Quantum and Approximate Computing II" and is not quantum) | ASPLOS: deferred-volume rule, plus a program page that truncates after Session 8C | Both venues punish naive counting, in different ways. |

### E.2 Cross-references bearing on specific SC claims — no SC text changed

- **SC's four acceptance pathways (§8)** were used unmodified as the comparison frame in the ASPLOS census §10. The ASPLOS corpus supplies the contrast case rather than a correction: papers ASPLOS accepts that would fail all four SC pathways are enumerated there (instruction-set proposals with no cost model at scale; full-machine architectures evaluated by analytic model; NISQ mitigation and QML with no scarce-resource argument; output-quality-only compilation).
- **The QEC-decoder `VENUE_GAP`** recorded in the SC census is confirmed from the other side: the ASPLOS census finds 11 QEC papers and traces two irreconcilable design philosophies (fixed-capacity predecoding vs growing the machine with the graph). The gap statement in both documents remains `VENUE_GAP`, never `RESEARCH_GAP`.
- **Micro Blossom and BQSim**, named in the SC census's forward-looking notes as the most HPC-relevant ASPLOS 2025 papers, are confirmed by the ASPLOS census — with two cautions recorded there: Micro Blossom's 0.8 µs is an *average* on a 62 MHz implementation that hits a wall at d=15, and its repository claims exceed its paper.

### E.3 One SC-side follow-up the ASPLOS census suggests

The ASPLOS corpus contains a documented **numeric mis-transfer between papers** (a 13.9× figure cited at an error rate outside the range the source paper swept). The SC census's cross-paper comparisons were not re-audited for the same failure mode. **Auditing SC's cross-paper numeric citations against the swept parameter ranges of their sources is an open item** — recorded here, not acted on, because acting on it means re-opening §§1–12.

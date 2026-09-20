# FGCS Quantum-HPC Census 2024-2026

**Journal:** Future Generation Computer Systems (FGCS) · Elsevier · ISSN 0167-739X  
**Census window:** 2024-2026 · **Records classified:** 85 · **Compiled:** 2026-09-17 · **Revision: rev2**

> **rev2 changes.** An independent adversarial verification pass found one window error and a
> four-record recall gap. FGCS-001 is reclassified **OUT_OF_WINDOW** (online-first 2023-12-04), and
> four records recovered by an extended cover-date sweep are added as **FGCS-A01..A04**. All counts,
> tables, logs and the special-collection section below are the revised figures.

---

## 1. Scope and method

This is a venue census of the **HPC x quantum-computing interface** in FGCS, not a quantum-computing
literature review. Every record was judged against the shared Three-Gate test:

1. **Gate 1** - is there a real classical systems problem (cost, parallelism, memory, communication,
   latency, throughput, scheduling, resource allocation, runtime, orchestration, distributed execution,
   scaling, compilation cost, data movement, accelerator design, performance modeling)?
2. **Gate 2** - is an HPC / systems / architecture technique a major part of the contribution?
3. **Gate 3** - does it materially inform future CPU/GPU/HPC <-> QPU heterogeneous computing?

### Candidate pool provenance and the cover-date correction

The pool began as a systematic Crossref full-population sweep of 1,567 FGCS articles 2024-2026 filtered
by a quantum-vocabulary regex, unioned with an OpenAlex title+abstract search, yielding 81 records.

**That sweep filtered on the Elsevier *cover* date.** FGCS volume cover dates run roughly six months
ahead of online-first, so every article online-first from 2026-07-17 onward carries a **2027 cover date**
(volumes 186-187) and fell outside the original window. The sweep was extended to cover-date
**2027-12-31** and re-filtered to first-availability **<= 2026-09-17**. This closed a **four-record recall
gap** — FGCS-A01, FGCS-A02, FGCS-A03 and FGCS-A04, all volume 186 with a 2027-01 cover date and
online-first dates between 2026-07-18 and 2026-08-04. JPDC had no equivalent gap.

The same cover-date/online-first offset caused an error in the other direction: **FGCS-001** was admitted
on its 2024-04 volume-153 cover date, but its first public availability is **2023-12-04**, placing it
outside the window. It is reclassified OUT_OF_WINDOW in section 6 and removed from the INCLUDED and
2024 counts. Its Three-Gate assessment is retained for audit; the verdict was vacated on window, not on merit.

### Census-year convention

Census year = year of first public availability (Elsevier online-first). The final volume/issue and its
cover date are recorded separately and routinely differ by one year, and for the added records by two
calendar years (FGCS-A02 is online-first 2026-07-29 in a 2027-01 issue). Years were not re-derived except
for the FGCS-001 correction above.

### Evidence discipline

41 of the original 81 dossier records carried `*** NO ABSTRACT RETRIEVED ***`. Abstracts, highlights and
availability statements were retrieved by targeted fetching (ScienceDirect abstract pages via DOI->PII
resolution, arXiv, Crossref, OpenAlex, GitHub) for 22 high-priority records, the four added records and
all three collection editorials. Where a field could not be evidenced it is written `INSUFFICIENT_EVIDENCE`;
where a record is classified from its title alone it is flagged `NO_ABSTRACT`. Performance numbers are
recorded only with their baseline, or marked `BASELINE_UNCLEAR`.

---

## 2. Headline result

| Metric | Value |
|---|---|
| Records classified | 85 |
| &nbsp;&nbsp;in-window records | 84 |
| &nbsp;&nbsp;OUT_OF_WINDOW | 1 (FGCS-001) |
| **INCLUDED** | **22** |
| &nbsp;&nbsp;of which ORIGINAL_RESEARCH (counts toward included population) | 20 |
| &nbsp;&nbsp;of which PERSPECTIVE (BIBLIOGRAPHY_HUB) | 2 |
| BORDERLINE | 8 |
| EXCLUDED (false positives + gate failures) | 54 |
| Precision of the in-window candidate pool (INCLUDED / 84) | 26% |
| Census policy judgement | **CORE_CENSUS** |

### Per-year distribution (census year = online-first year)

| Census year | Records | INCLUDED | &nbsp;&nbsp;of which orig. research | BORDERLINE | EXCLUDED | OUT_OF_WINDOW |
|---|---|---|---|---|---|---|
| 2023 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2024 | 25 | 6 | 5 | 2 | 17 | 0 |
| 2025 | 31 | 8 | 8 | 4 | 19 | 0 |
| 2026 | 28 | 8 | 7 | 2 | 18 | 0 |
| **In-window total** | **84** | **22** | **20** | **8** | **54** | — |

The 2023 row is FGCS-001 alone, carried for audit only; it is excluded from every in-window total.

### Article types across all classified records

| Article type | Count |
|---|---|
| ORIGINAL_RESEARCH | 73 |
| REVIEW_SURVEY | 4 |
| PERSPECTIVE | 3 |
| EDITORIAL | 0 |
| SPECIAL_ISSUE_INTRO | 4 |
| OTHER | 1 |

### Scenario tags (INCLUDED + BORDERLINE, multiple allowed)

| Scenario | Count |
|---|---|
| HPC_FOR_Q | 22 |
| Q_IN_HPC | 16 |
| Q_FOR_HPC | 8 |
| FUTURE_WORKLOAD | 12 |

---

## 3. Per-year tables

### Census year 2024

| ID | Verdict | Type | Title | First author | DOI |
|---|---|---|---|---|---|
| FGCS-002 | **INCLUDED** | ORIGINAL_RESEARCH | QFaaS: A Serverless Function-as-a-Service framework for Quantum computing | Hoa T. Nguyen | 10.1016/j.future.2024.01.018 |
| FGCS-003 | excluded | ORIGINAL_RESEARCH | Replay with Feedback: How does the performance of HPC system impact user submission b... | Maël Madon | 10.1016/j.future.2024.01.024 |
| FGCS-004 | excluded | ORIGINAL_RESEARCH | Quantum annealing-driven branch and bound for the single machine total weighted numbe... | Wojciech Bożejko | 10.1016/j.future.2024.02.016 |
| FGCS-005 | excluded | ORIGINAL_RESEARCH | Quantum particle swarm optimization algorithm based on diversity migration strategy | Chen Gong | 10.1016/j.future.2024.04.008 |
| FGCS-006 | excluded | ORIGINAL_RESEARCH | Comparing Adiabatic Quantum Computers for satellite images feature extraction | Lorenzo Rocutto | 10.1016/j.future.2024.04.027 |
| FGCS-007 | **INCLUDED** | ORIGINAL_RESEARCH | Paving the way to hybrid quantum–classical scientific workflows | Sandeep Suresh Cranganore | 10.1016/j.future.2024.04.030 |
| FGCS-008 | excluded | ORIGINAL_RESEARCH | SkySwapping: Entanglement resupply by separating quantum swapping and photon exchange | Alin-Bogdan Popa | 10.1016/j.future.2024.04.031 |
| FGCS-009 | excluded | ORIGINAL_RESEARCH | A lattice-based efficient certificateless public key encryption for big data security... | Juyan Li | 10.1016/j.future.2024.04.039 |
| FGCS-010 | **INCLUDED** | PERSPECTIVE | Quantum-centric supercomputing for materials science: A perspective on challenges and... | Yuri Alexeev | 10.1016/j.future.2024.04.060 |
| FGCS-011 | excluded | ORIGINAL_RESEARCH | Quantum simulation of dissipation for Maxwell equations in dispersive media | Efstratios Koukoutsis | 10.1016/j.future.2024.05.028 |
| FGCS-012 | excluded | ORIGINAL_RESEARCH | Quantum Annealing for Computer Vision minimization problems | Shahrokh Heidari | 10.1016/j.future.2024.05.037 |
| FGCS-013 | excluded | ORIGINAL_RESEARCH | AQUA: Analytics-driven quantum neural network (QNN) user assistance for software vali... | Soohyun Park | 10.1016/j.future.2024.05.047 |
| FGCS-014 | **INCLUDED** | ORIGINAL_RESEARCH | Performance of algorithms for emerging ion-trap quantum hardware | Arthur Kurlej | 10.1016/j.future.2024.06.005 |
| FGCS-015 | **INCLUDED** | ORIGINAL_RESEARCH | Parallel quantum computing simulations via quantum accelerator platform virtualization | Daniel Claudino | 10.1016/j.future.2024.06.007 |
| FGCS-016 | _BORDERLINE_ | PERSPECTIVE | Assessing and advancing the potential of quantum computing: A NASA case study | Eleanor G. Rieffel | 10.1016/j.future.2024.06.012 |
| FGCS-017 | excluded | REVIEW_SURVEY | Quantum-empowered federated learning and 6G wireless networks for IoT security: Conce... | Danish Javeed | 10.1016/j.future.2024.06.023 |
| FGCS-018 | **INCLUDED** | ORIGINAL_RESEARCH | Integrating quantum computing resources into scientific HPC ecosystems | Thomas Beck | 10.1016/j.future.2024.06.058 |
| FGCS-019 | excluded | ORIGINAL_RESEARCH | Deciphering the abundance of immune cells in glomerular endothelium of Alport syndrom... | Yizhou Sun | 10.1016/j.future.2024.07.013 |
| FGCS-020 | _BORDERLINE_ | ORIGINAL_RESEARCH | Quantum resource estimation for large scale quantum algorithms | Vlad Gheorghiu | 10.1016/j.future.2024.107480 |
| FGCS-021 | excluded | ORIGINAL_RESEARCH | Software stewardship and advancement of a high-performance computing scientific appli... | William F. Godoy | 10.1016/j.future.2024.107502 |
| FGCS-022 | excluded | SPECIAL_ISSUE_INTRO | Special Collection on Advances in Quantum Computing: Methods, Algorithms, and Systems | Stefano Markidis | 10.1016/j.future.2024.107503 |
| FGCS-023 | excluded | ORIGINAL_RESEARCH | Designing optimal Quantum Key Distribution Networks based on Time-Division Multiplexi... | Juan Carlos Hernandez-Hernandez | 10.1016/j.future.2024.107557 |
| FGCS-024 | excluded | ORIGINAL_RESEARCH | A blockchain-assisted privacy-preserving signature scheme using quantum teleportation... | Sunil Prajapat | 10.1016/j.future.2024.107581 |
| FGCS-025 | excluded | REVIEW_SURVEY | Quantum machine learning algorithms for anomaly detection: A review | Sebastiano Corli | 10.1016/j.future.2024.107632 |
| FGCS-026 | excluded | ORIGINAL_RESEARCH | Flexible hybrid post-quantum bidirectional multi-factor authentication and key agreem... | A. Braeken | 10.1016/j.future.2024.107634 |

### Census year 2025

| ID | Verdict | Type | Title | First author | DOI |
|---|---|---|---|---|---|
| FGCS-027 | excluded | ORIGINAL_RESEARCH | Raising user awareness through unsupervised clustering of energy consumption habits | Francesca Marcello | 10.1016/j.future.2024.107623 |
| FGCS-028 | excluded | ORIGINAL_RESEARCH | Devising an actor-based middleware support to federated learning experiments and systems | Alessio Bechini | 10.1016/j.future.2024.107646 |
| FGCS-029 | excluded | ORIGINAL_RESEARCH | Generating hard Ising instances with planted solutions using post-quantum cryptograph... | Salvatore Mandrà | 10.1016/j.future.2025.107721 |
| FGCS-030 | excluded | ORIGINAL_RESEARCH | Chained continuous quantum federated learning framework | Dev Gurung | 10.1016/j.future.2025.107800 |
| FGCS-031 | excluded | ORIGINAL_RESEARCH | Denoising diffusion models with optimized quantum implicit neural networks for image ... | Jiale Zhang | 10.1016/j.future.2025.107875 |
| FGCS-032 | excluded | ORIGINAL_RESEARCH | Multi-omic and quantum machine learning integration for lung subtypes classification | Mandeep Kaur Saggi | 10.1016/j.future.2025.107905 |
| FGCS-033 | **INCLUDED** | ORIGINAL_RESEARCH | MLQM: Machine learning approach for accelerating optimal qubit mapping | Wenjie Sun | 10.1016/j.future.2025.107906 |
| FGCS-034 | _BORDERLINE_ | ORIGINAL_RESEARCH | Is quantum optimization ready? An effort towards neural network compression using adi... | Zhehui Wang | 10.1016/j.future.2025.107908 |
| FGCS-035 | excluded | ORIGINAL_RESEARCH | Exploring the performance of CP2K simulations on the CPU-GPDSP Fusion intra-heterogen... | Qi Du | 10.1016/j.future.2025.107912 |
| FGCS-036 | **INCLUDED** | ORIGINAL_RESEARCH | State of practice: Evaluating GPU performance of state vector and tensor network methods | Marzio Vallero | 10.1016/j.future.2025.107927 |
| FGCS-037 | _BORDERLINE_ | ORIGINAL_RESEARCH | Solving combinatorial optimization and machine learning problems on hybrid near-term ... | Mateusz Slysz | 10.1016/j.future.2025.107934 |
| FGCS-038 | excluded | ORIGINAL_RESEARCH | Quantum annealing for the two-level facility location problem | Alessia Ciacco | 10.1016/j.future.2025.107961 |
| FGCS-039 | **INCLUDED** | ORIGINAL_RESEARCH | MPGP-QOC: Multi-programming and graph-partition-based QOC for QNN inference | Yiding Liu | 10.1016/j.future.2025.107966 |
| FGCS-040 | _BORDERLINE_ | ORIGINAL_RESEARCH | A multiple-circuit approach to quantum resource reduction with application to the qua... | Melody Lee | 10.1016/j.future.2025.107975 |
| FGCS-041 | **INCLUDED** | ORIGINAL_RESEARCH | Tightly-integrated quantum–classical computing using the QHDL hardware description la... | Gilbert Netzer | 10.1016/j.future.2025.107977 |
| FGCS-042 | excluded | ORIGINAL_RESEARCH | Feedback-based quantum strategies for constrained combinatorial optimization problems | Salahuddin Abdul Rahman | 10.1016/j.future.2025.107979 |
| FGCS-043 | **INCLUDED** | ORIGINAL_RESEARCH | Bridging paradigms: Designing for HPC-Quantum convergence | Amir Shehata | 10.1016/j.future.2025.107980 |
| FGCS-044 | excluded | ORIGINAL_RESEARCH | Parameter-efficient Quantum Denoising Diffusion Probabilistic Models with temporal en... | Xuefen Zhang | 10.1016/j.future.2025.107981 |
| FGCS-045 | **INCLUDED** | ORIGINAL_RESEARCH | NetQIR: An extension of QIR for distributed quantum computing | F. Javier Cardama | 10.1016/j.future.2025.107989 |
| FGCS-046 | excluded | SPECIAL_ISSUE_INTRO | Editorial on future generation computer systems (FGCS) special collection on advances... | Stefano Markidis | 10.1016/j.future.2025.107993 |
| FGCS-047 | excluded | ORIGINAL_RESEARCH | Distributed machine learning based on quantum cloud with quantum homomorphic encryption | Lin Zeng | 10.1016/j.future.2025.108053 |
| FGCS-048 | excluded | ORIGINAL_RESEARCH | A performance evaluation framework for post-quantum TLS | José A. Montenegro | 10.1016/j.future.2025.108062 |
| FGCS-049 | _BORDERLINE_ | ORIGINAL_RESEARCH | A hybrid quantum-classical particle-in-cell method for plasma simulations | Pratibha Raghupati Hegde | 10.1016/j.future.2025.108087 |
| FGCS-050 | excluded | ORIGINAL_RESEARCH | Anomaly-aware quantum convolutional neural network for carbon-efficient job arrival r... | Shivani Tripathi | 10.1016/j.future.2025.108096 |
| FGCS-051 | excluded | ORIGINAL_RESEARCH | Intrusion detection with improved quantum neural network: A bigdata perspective | Nithya BN | 10.1016/j.future.2025.108102 |
| FGCS-052 | excluded | ORIGINAL_RESEARCH | The NextGen Quantum-Secure Edge AI-Blockchain System: Enhancing Supply Chain Trust wi... | Israelin Insulata J | 10.1016/j.future.2025.108179 |
| FGCS-053 | excluded | ORIGINAL_RESEARCH | Zero-trust token authorization with trapdoor hashes for scalable distributed firewalls | Dr. Daniel Díaz-Sánchez | 10.1016/j.future.2025.108227 |
| FGCS-054 | excluded | ORIGINAL_RESEARCH | Federated reinforcement learning-based adaptive stream applications scheduling in edg... | Sabeur Lajili | 10.1016/j.future.2025.108235 |
| FGCS-055 | **INCLUDED** | ORIGINAL_RESEARCH | LuGo: An enhanced quantum phase estimation implementation | Chao Lu | 10.1016/j.future.2025.108270 |
| FGCS-056 | excluded | ORIGINAL_RESEARCH | SoA-SDA: Quantum-Resistant, Energy-Efficient In-Network Aggregation Protocol for Reso... | Lei Song | 10.1016/j.future.2025.108321 |
| FGCS-057 | **INCLUDED** | ORIGINAL_RESEARCH | Efficient and scalable branch-and-bound algorithm for exact qubit allocation | Jean-Philippe Valois | 10.1016/j.future.2025.108342 |

### Census year 2026

| ID | Verdict | Type | Title | First author | DOI |
|---|---|---|---|---|---|
| FGCS-058 | _BORDERLINE_ | ORIGINAL_RESEARCH | Cost-efficient quantum cloud task offloading with quantum-inspired particle swarm opt... | Santanu Ghosh | 10.1016/j.future.2025.108095 |
| FGCS-059 | excluded | ORIGINAL_RESEARCH | Quantum-resistant blockchain architecture for secure vehicular networks: A ML-KEM-ena... | Muhammad Asim | 10.1016/j.future.2026.108391 |
| FGCS-060 | excluded | OTHER | Corrigendum to “Solving combinatorial optimization and machine learning problems on h... | Mateusz Slysz | 10.1016/j.future.2026.108408 |
| FGCS-061 | excluded | ORIGINAL_RESEARCH | DQVeriChain: Distributed quantum-state-verified and DID-based self-attentive large la... | Rabi Shaw | 10.1016/j.future.2026.108412 |
| FGCS-062 | excluded | ORIGINAL_RESEARCH | Applying quantum error-correcting codes for fault-tolerant blind quantum cloud comput... | Qiang Zhao | 10.1016/j.future.2026.108451 |
| FGCS-063 | _BORDERLINE_ | ORIGINAL_RESEARCH | Addressing the minor-embedding problem in quantum annealing and evaluating state-of-t... | Aitor Gómez-Tejedor | 10.1016/j.future.2026.108481 |
| FGCS-064 | **INCLUDED** | ORIGINAL_RESEARCH | HiMA: Hierarchical quantum microarchitecture for qubit-scaling and quantum process-le... | Qi Zhou | 10.1016/j.future.2026.108484 |
| FGCS-065 | **INCLUDED** | ORIGINAL_RESEARCH | GraMA: A gradient matrix-guided assignment method for solving qubit mapping problems | Xinyu Piao | 10.1016/j.future.2026.108485 |
| FGCS-066 | **INCLUDED** | PERSPECTIVE | The role of quantum computing in advancing scientific high-performance computing: A p... | Gilles Buchs | 10.1016/j.future.2026.108487 |
| FGCS-067 | excluded | ORIGINAL_RESEARCH | Enhancing adversarial robustness of neural networks via quantum computing | Xiangyu Shi | 10.1016/j.future.2026.108542 |
| FGCS-068 | excluded | ORIGINAL_RESEARCH | Towards post-quantum secure and practical privacy-preserving top-k maximum inner prod... | Yuqi Song | 10.1016/j.future.2026.108566 |
| FGCS-069 | excluded | ORIGINAL_RESEARCH | Scalable quantum Trotterised-vs-continuous annealing for pseudo-Boolean multi-objecti... | Zakaria Abdelmoiz Dahi | 10.1016/j.future.2026.108568 |
| FGCS-070 | excluded | ORIGINAL_RESEARCH | Quantum message authentication code verifiable by multiple parties independently | Ping Wang | 10.1016/j.future.2026.108569 |
| FGCS-071 | excluded | ORIGINAL_RESEARCH | Entropic optimal transport with quantum amplitude estimation | Francisco Orts | 10.1016/j.future.2026.108570 |
| FGCS-072 | excluded | ORIGINAL_RESEARCH | A dynamic access control scheme for cross-border trade data based on blockchain and RLWE | Rong Jiang | 10.1016/j.future.2026.108590 |
| FGCS-073 | **INCLUDED** | ORIGINAL_RESEARCH | Universal quantum computer simulation of 50 qubits on Europe’s first exascale superco... | Hans De Raedt | 10.1016/j.future.2026.108592 |
| FGCS-074 | excluded | ORIGINAL_RESEARCH | QTIS: A QAOA-based Quantum Time Interval Scheduler | José A. Tirado-Domínguez | 10.1016/j.future.2026.108594 |
| FGCS-075 | excluded | ORIGINAL_RESEARCH | Entanglement in the trees: Optimal entanglement distribution in binary tree quantum n... | Iulian Ioan Bîrlică | 10.1016/j.future.2026.108597 |
| FGCS-076 | excluded | REVIEW_SURVEY | Quantum Artificial Intelligence for mission-critical systems: Foundations, architectu... | Siva Sai | 10.1016/j.future.2026.108602 |
| FGCS-077 | excluded | SPECIAL_ISSUE_INTRO | ATIS: Novel applications and techniques in information security and outlook | Shiva Raj Pokhrel | 10.1016/j.future.2026.108647 |
| FGCS-078 | excluded | ORIGINAL_RESEARCH | Hybrid quantum Graph Neural Networks for robust botnet detection in modern IoT ecosys... | Vincenzo Sammartino | 10.1016/j.future.2026.108650 |
| FGCS-079 | **INCLUDED** | ORIGINAL_RESEARCH | Workflow decomposition algorithm for scheduling with quantum annealer-based hybrid so... | Marcin Kroczek | 10.1016/j.future.2026.108686 |
| FGCS-080 | **INCLUDED** | ORIGINAL_RESEARCH | Three ways to share a QPU: Scheduling strategies for hybrid Quantum-HPC applications | Marco Cipollini | 10.1016/j.future.2026.108699 |
| FGCS-081 | excluded | REVIEW_SURVEY | Generative AI in the age of quantum computing: A taxonomy, architectural elements and... | Siva Sai | 10.1016/j.future.2026.108714 |
| FGCS-A01 | excluded | ORIGINAL_RESEARCH | Performance benchmarking of Tensor Trains for quantum-inspired homogenization on TPU,... | Sascha H. Hauck | 10.1016/j.future.2026.108709 |
| FGCS-A02 | **INCLUDED** | ORIGINAL_RESEARCH | Closed-loop calculations of electronic structure on a quantum processor and a classic... | Tomonori Shirakawa | 10.1016/j.future.2026.108731 |
| FGCS-A03 | **INCLUDED** | ORIGINAL_RESEARCH | DistributedEstimator: Distributed training of quantum neural networks via circuit cut... | Prabhjot Singh | 10.1016/j.future.2026.108746 |
| FGCS-A04 | excluded | SPECIAL_ISSUE_INTRO | Editorial on Future Generation Computer Systems (FGCS) special collection on advances... | Stefano Markidis | 10.1016/j.future.2026.108754 |

**Added in rev2:** FGCS-A01, FGCS-A02, FGCS-A03 and FGCS-A04 appear in the 2026 table above.

---

## 4. Full records - INCLUDED (22)

### FGCS-002 — QFaaS: A Serverless Function-as-a-Service framework for Quantum computing

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.01.018` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.01.018 |
| Census year | 2024 (online-first 2024-01-21; issue 2024-05) |
| Volume / issue / pages | 154 / - / 281-300 |
| First author (institution as given) | Hoa T. Nguyen — CLOUDS Laboratory, The University of Melbourne (as given) |
| Author count | 3 |
| arXiv | 2205.14845 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC |
| Branch | quantum_runtime_orchestration, hybrid_workflow |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Runtime, orchestration and resource management for hybrid quantum-classical functions across heterogeneous backends; containerisation and deployment cost.  
**Gate 2.** A serverless middleware/runtime layer (function lifecycle, containerisation, backend selection, DevOps integration) is the core contribution.  
**Gate 3.** Defines a concrete software-stack pattern for delivering QPU access as a managed service alongside classical compute.

| Analysis field | Content |
|---|---|
| Research question | Can the serverless Function-as-a-Service model be adapted to hide quantum SDK and backend heterogeneity behind a uniform hybrid execution service? |
| Quantum problem | Fragmentation of quantum programming languages (Qiskit, Q#, Cirq, Braket) and provider backends. |
| Classical/HPC problem | Orchestration, containerisation and lifecycle management of short-lived hybrid functions across multiple execution backends. |
| Mechanism | Layered serverless architecture: API gateway, function lifecycle manager, containerised hybrid quantum-classical functions, backend-agnostic dispatch to simulators and cloud QPUs. |
| Computational bottleneck | Backend selection/queueing and classical-quantum round-trip latency in hybrid functions. |
| Evaluation platform | IBM Quantum and Amazon Braket cloud QPUs plus simulators; containerised deployment. |
| Scale | Two use cases; device sizes INSUFFICIENT_EVIDENCE. |
| Performance metrics | end-to-end function execution time; deployment/operation workflow feasibility |
| **Major claim (with baseline)** | A unified serverless layer can execute hybrid functions across four SDKs and two providers; BASELINE_UNCLEAR (no quantitative baseline framework comparison stated). |
| Limitation | Targets cloud QPU providers rather than an on-premise HPC batch system; no HPC scheduler integration reported. |
| Relevance to future quantum-HPC | Early template for QPU-as-a-service abstractions that later HPC-QPU middleware (e.g. gateway/API designs) builds on. |
| Artifact | PUBLIC_CODE — https://github.com/Cloudslab/qfaas |
| Conference extension | UNKNOWN |
| Prior-work note | An arXiv preprint (2205.14845) predates the journal version, and a further QFaaS application-development paper exists from the same group. A preprint is not a conference paper, so this does not meet the CONFIRMED_EXTENSION or RELATED_LINEAGE evidence bar. |

### FGCS-007 — Paving the way to hybrid quantum–classical scientific workflows

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.04.030` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.04.030 |
| Census year | 2024 (online-first 2024-04-22; issue 2024-09) |
| Volume / issue / pages | 158 / - / 346-366 |
| First author (institution as given) | Sandeep Suresh Cranganore — University of Vienna (as given) |
| Author count | 4 |
| arXiv | 2404.10389 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, HPC_FOR_Q |
| Branch | hybrid_workflow, scientific_workflow_application |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Mapping workflow components onto heterogeneous resources, and workflow management across the computing continuum - resource allocation and orchestration.  
**Gate 2.** Formalisation of hybrid quantum-classical workflows plus a software architecture for a hybrid workflow management system.  
**Gate 3.** Defines how quantum tasks are identified, split out and scheduled next to classical tasks in a scientific workflow engine.

| Analysis field | Content |
|---|---|
| Research question | How should extreme-data scientific workflows be formalised and decomposed so that quantum components can be identified and mapped onto quantum resources in the computing continuum? |
| Quantum problem | Identifying which parts of a scientific application are amenable to quantum execution. |
| Classical/HPC problem | Workflow formalisation, component-to-resource mapping and workflow management across a heterogeneous continuum. |
| Mechanism | Formal model of hybrid quantum-classical workflows; procedure to identify quantum components and map them to resources; reference software architecture for a hybrid WMS. |
| Computational bottleneck | Resource mapping and data movement between classical workflow stages and quantum tasks. |
| Evaluation platform | A real scientific use case (demonstration); concrete machine INSUFFICIENT_EVIDENCE. |
| Scale | INSUFFICIENT_EVIDENCE |
| Performance metrics | qualitative workflow feasibility |
| **Major claim (with baseline)** | Hybrid quantum-classical scientific workflows can be formalised and managed by an extended WMS architecture; BASELINE_UNCLEAR (no quantitative baseline). |
| Limitation | Architecture-level contribution; no production WMS implementation or performance measurement reported in the abstract. |
| Relevance to future quantum-HPC | Supplies the workflow-level vocabulary (quantum component identification, mapping) that later HPC-QC scheduling work operationalises. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-010 — Quantum-centric supercomputing for materials science: A perspective on challenges and future directions

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.04.060` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.04.060 |
| Census year | 2024 (online-first 2024-05-31; issue 2024-11) |
| Volume / issue / pages | 160 / - / 666-710 |
| First author (institution as given) | Yuri Alexeev — Argonne National Laboratory (as given) |
| Author count | 128 |
| arXiv | 2312.09733 |
| Article type | PERSPECTIVE · BIBLIOGRAPHY_HUB |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC, Q_FOR_HPC, FUTURE_WORKLOAD |
| Branch | hpc_qpu_integration, scientific_workflow_application, benchmarking_performance_modeling |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Supercomputing-centre simulation, analysis and data resources are explicitly framed as the constrained resource; hard-problem identification and validation cost.  
**Gate 2.** Sets out the quantum-centric supercomputing model: QPU and HPC interacting for validation, partitioning and hybrid execution.  
**Gate 3.** Directly about how QPUs and HPC systems will share a materials-science workload - resource usage, execution and software stack.

| Analysis field | Content |
|---|---|
| Research question | What must change in algorithms, software and centre infrastructure for quantum-centric supercomputing to serve materials science? |
| Quantum problem | Quantum simulation of materials/electronic structure on near- and long-term QPUs. |
| Classical/HPC problem | Supercomputing centres already saturated by materials simulation; need for approximate-result validation and hard-problem identification. |
| Mechanism | Community roadmap: identifies the QC-HPC interaction modes (validation, hard-instance identification, synergy) and reviews algorithm/hardware/software readiness. |
| Computational bottleneck | Classical simulation and validation cost of correlated materials problems. |
| Evaluation platform | Review/perspective; no single platform. |
| Scale | 128 authors across a large multi-institution community. |
| Performance metrics | qualitative readiness assessment |
| **Major claim (with baseline)** | Materials science requires QC and HPC to be co-designed rather than used separately; BASELINE_UNCLEAR (perspective, no measured baseline). |
| Limitation | Roadmap rather than measurement; no implementation or benchmark. |
| Relevance to future quantum-HPC | Among the most heavily referenced statements of the quantum-centric supercomputing model; a primary bibliography hub for this corpus. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-014 — Performance of algorithms for emerging ion-trap quantum hardware

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.06.005` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.06.005 |
| Census year | 2024 (online-first 2024-06-12; issue 2024-11) |
| Volume / issue / pages | 160 / - / 654-665 |
| First author (institution as given) | Arthur Kurlej — MITRE (as given) |
| Author count | 3 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, FUTURE_WORKLOAD |
| Branch | benchmarking_performance_modeling, architecture_control |
| Deep-dive priority | **3 / 5** |

**Gate 1.** Runtime and overhead of benchmark applications across architecture variants, and the compilation step that produces them.  
**Gate 2.** Architectural simulation plus compilation to target devices used as a quantitative architecture-evaluation methodology - quantum performance modeling.  
**Gate 3.** Informs how QPU architectural choices change execution time and overhead, i.e. performance and architecture of the accelerator side.

| Analysis field | Content |
|---|---|
| Research question | How do trapped-ion architectural design choices affect the runtime and overhead of representative quantum applications? |
| Quantum problem | Performance of benchmark quantum algorithms (including adaptive variational algorithms for chemistry) on ion-trap hardware. |
| Classical/HPC problem | Architectural simulation and compilation infrastructure needed to estimate runtime/overhead before hardware exists. |
| Mechanism | Pipeline of benchmark application selection, compilation to candidate ion-trap targets, and architectural simulation to extract runtime and overhead. |
| Computational bottleneck | Shuttling/connectivity overheads in trapped-ion architectures as exposed by compiled circuits. |
| Evaluation platform | Architectural simulator for ion-trap devices (simulated, not physical hardware). |
| Scale | INSUFFICIENT_EVIDENCE (qubit counts not stated in retrieved material) |
| Performance metrics | runtime; architectural overhead |
| **Major claim (with baseline)** | A benchmark-plus-architectural-simulation methodology can quantitatively separate ion-trap design options; BASELINE_UNCLEAR. |
| Limitation | Simulation-based architectural estimates; no physical ion-trap measurements reported. |
| Relevance to future quantum-HPC | Performance-modeling methodology for choosing accelerator architectures before deployment in a centre. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-015 — Parallel quantum computing simulations via quantum accelerator platform virtualization

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.06.007` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.06.007 |
| Census year | 2024 (online-first 2024-06-07; issue 2024-11) |
| Volume / issue / pages | 160 / - / 264-273 |
| First author (institution as given) | Daniel Claudino — Oak Ridge National Laboratory (as given) |
| Author count | 3 |
| arXiv | 2406.03466 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | distributed_gpu_simulation, hpc_qpu_integration, quantum_runtime_orchestration |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Parallelism and strong scaling across HPC nodes; throughput of large batches of independent circuit executions.  
**Gate 2.** Virtualisation of QPUs: an array of virtual QPUs mapped onto classical HPC nodes inside XACC, with GPU-accelerated backends via cuQuantum.  
**Gate 3.** A direct model for how many logical QPU endpoints an HPC system can present, and how shot/circuit batches are distributed.

| Analysis field | Content |
|---|---|
| Research question | Can quantum circuit execution batches be parallelised by exposing a large array of virtual QPUs mapped onto HPC nodes? |
| Quantum problem | Workflows requiring many independent measurements over large sets of slightly different circuits (VQE gradients, circuit learning). |
| Classical/HPC problem | Distributing an embarrassingly parallel but large circuit-execution workload across HPC nodes and GPUs. |
| Mechanism | Virtual quantum processing unit array mapped one-to-one onto classical HPC nodes, implemented inside XACC so it is backend-agnostic; GPU simulation through cuQuantum. |
| Computational bottleneck | Serialised circuit execution and per-circuit simulation cost; memory per node for state-vector simulation. |
| Evaluation platform | GPU-accelerated HPC platform using the cuQuantum SDK via XACC (specific machine INSUFFICIENT_EVIDENCE). |
| Scale | Strong-scaling study varying qubit count and circuit layer count; node counts INSUFFICIENT_EVIDENCE. |
| Performance metrics | strong scaling efficiency; time to compute multi-contracted VQE gradients |
| **Major claim (with baseline)** | Strong scaling is demonstrated on two domain-science problems (multi-contracted VQE gradients and data-driven circuit learning); BASELINE_UNCLEAR (speedup ratios not stated in retrieved text). |
| Limitation | Virtual QPUs are simulators, so results characterise simulation throughput rather than physical QPU sharing. |
| Relevance to future quantum-HPC | One of the clearest FGCS statements of QPU virtualisation as an HPC resource abstraction. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-018 — Integrating quantum computing resources into scientific HPC ecosystems

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.06.058` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.06.058 |
| Census year | 2024 (online-first 2024-07-02; issue 2024-12) |
| Volume / issue / pages | 161 / - / 11-25 |
| First author (institution as given) | Thomas Beck — Oak Ridge National Laboratory (as given) |
| Author count | 18 |
| arXiv | 2408.16159 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, HPC_FOR_Q, FUTURE_WORKLOAD |
| Branch | hpc_qpu_integration, qpu_scheduling_resource_mgmt, quantum_runtime_orchestration |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Resource management, allocation and lifecycle of a QC resource inside an HPC centre; integration of accelerators into existing batch/allocation processes.  
**Gate 2.** A hardware-agnostic integration framework that treats the QPU as an HPC accelerator, spanning simulators and physical devices and the centre's lifecycle management.  
**Gate 3.** Explicitly about how a supercomputing facility procures, allocates and operates quantum resources alongside classical ones.

| Analysis field | Content |
|---|---|
| Research question | How can quantum computing resources be integrated into an existing scientific HPC ecosystem as computational accelerators? |
| Quantum problem | NISQ noise and device heterogeneity make direct QPU exposure to users impractical. |
| Classical/HPC problem | Centre-level resource integration: allocation, lifecycle management, user access and the software stack around a non-classical accelerator. |
| Mechanism | Hardware-agnostic framework layering simulators and physical QPU backends behind an HPC-facing interface, aligned with DOE/ORNL HPC lifecycle management practice. |
| Computational bottleneck | Integration friction between quantum backends and HPC allocation/scheduling processes. |
| Evaluation platform | ORNL HPC environment with a spectrum of simulators and hardware technologies. |
| Scale | Centre-scale; concrete node/QPU counts INSUFFICIENT_EVIDENCE. |
| Performance metrics | qualitative integration feasibility |
| **Major claim (with baseline)** | A single hardware-agnostic layer can serve both current NISQ devices and future fault-tolerant machines inside an HPC centre; BASELINE_UNCLEAR. |
| Limitation | Framework and process description; limited quantitative performance evaluation. |
| Relevance to future quantum-HPC | A primary reference for centre-level HPC-QPU integration practice; directly precedes FGCS-043 from the same laboratory. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-033 — MLQM: Machine learning approach for accelerating optimal qubit mapping

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107906` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107906 |
| Census year | 2025 (online-first 2025-05-22; issue 2025-12) |
| Volume / issue / pages | 173 / - / 107906 |
| First author (institution as given) | Wenjie Sun — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 6 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | compiler_mapping_routing |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **3 / 5** |

**Gate 1.** Compilation cost: solving time and memory (search-space size) of exact qubit mapping are the quantities optimised.  
**Gate 2.** Classical compilation scalability - search-space pruning and adaptive solver-variable adjustment to make an exact mapping solver tractable.  
**Gate 3.** Compiler throughput and memory are hard constraints on any HPC-hosted quantum software stack.

| Analysis field | Content |
|---|---|
| Research question | Can machine learning prune the search space of optimal qubit mapping enough to make exact solving practical? |
| Quantum problem | Mapping logical circuits onto constrained hardware connectivity without losing solution quality. |
| Classical/HPC problem | Solving time and memory footprint of the exact (solver-based) mapping formulation. |
| Mechanism | Global search-space pruning with an ML model plus prior knowledge; data augmentation by gate allocation and qubit rearrangement; local pruning by adaptive dynamic solver-variable adjustment. |
| Computational bottleneck | Combinatorial blow-up of the exact mapping solver's search space. |
| Evaluation platform | Classical solver benchmarks (machine specification INSUFFICIENT_EVIDENCE). |
| Scale | Benchmark circuit suite; sizes INSUFFICIENT_EVIDENCE. |
| Performance metrics | mapping solving time; space complexity; solution quality |
| **Major claim (with baseline)** | Average 1.79x solving speedup with 22% space-complexity reduction while maintaining solution quality, measured against state-of-the-art exact mapping approaches (baseline named only as 'state-of-the-art' - partially BASELINE_UNCLEAR). |
| Limitation | Gains depend on the learned model transferring to unseen circuit/topology combinations; training cost not reported. |
| Relevance to future quantum-HPC | Compilation time is a real scheduling-relevant cost when many jobs share a QPU; this attacks it directly. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-036 — State of practice: Evaluating GPU performance of state vector and tensor network methods

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107927` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107927 |
| Census year | 2025 (online-first 2025-05-31; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107927 |
| First author (institution as given) | Marzio Vallero — Politecnico di Torino (as given) |
| Author count | 3 |
| arXiv | 2401.06188 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | distributed_gpu_simulation, benchmarking_performance_modeling |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Memory footprint and execution time of quantum circuit simulation, and the scalability limit of top HPC machines for state-vector simulation.  
**Gate 2.** Systematic GPU-accelerated simulation benchmarking across state-vector and tensor-network backends (cuStateVec, cupy, cuTensorNet under cuQuantum/qsim).  
**Gate 3.** Establishes where the classical simulation frontier sits, which determines what an HPC system can still verify or replace on the QPU side.

| Analysis field | Content |
|---|---|
| Research question | Where does the practical limit of GPU-accelerated classical quantum-circuit simulation lie for state-vector versus tensor-network methods? |
| Quantum problem | Simulating large quantum systems classically while NISQ devices remain non-fault-tolerant. |
| Classical/HPC problem | Exponential memory growth of state-vector simulation and contraction cost of tensor networks on GPU hardware. |
| Mechanism | Controlled benchmark of three GPU backends (qsim-cusv, qsim-cuda, cutn) across circuit families, measuring time and memory as qubit count and depth scale. |
| Computational bottleneck | GPU memory capacity for state vectors; contraction cost/ordering for tensor networks. |
| Evaluation platform | AMD EPYC 7643 48-core CPU, 128 GB RAM, NVIDIA A100 80 GB GPU; NVIDIA cuQuantum with qsim. |
| Scale | Single-node GPU study; qubit counts scaled to the memory limit of an 80 GB A100. |
| Performance metrics | execution time; memory footprint; scaling with qubit count and depth |
| **Major claim (with baseline)** | Each simulation family saturates for different reasons - state vector on memory, tensor network on contraction structure - so the practical frontier is circuit-dependent; comparison is between the three GPU backends (baseline is stated). |
| Limitation | Single-node A100 study; multi-node/distributed simulation is not covered. |
| Relevance to future quantum-HPC | Gives the empirical basis for provisioning GPU simulation capacity in a centre that also hosts QPUs. |
| Artifact | PARTIAL |
| Artifact note | The paper cites a code/execution-time repository and an interactive plot, but no URL was recoverable from the retrieved text. |
| Conference extension | UNKNOWN |

### FGCS-039 — MPGP-QOC: Multi-programming and graph-partition-based QOC for QNN inference

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107966` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107966 |
| Census year | 2025 (online-first 2025-06-21; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107966 |
| First author (institution as given) | Yiding Liu — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 1 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC |
| Branch | qpu_scheduling_resource_mgmt, compiler_mapping_routing |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Throughput (inference speedup), compilation time, and device occupancy via multi-programming - several devices' worth of work packed onto one QPU.  
**Gate 2.** Multi-programming (concurrent circuits on one device, i.e. QPU sharing) combined with graph partitioning and quantum optimal control - a scheduling/compilation systems technique.  
**Gate 3.** Directly about how a shared QPU is packed and how much classical compilation that costs.

| Analysis field | Content |
|---|---|
| Research question | Can multi-programming plus graph-partitioned quantum optimal control raise QNN inference throughput without losing accuracy? |
| Quantum problem | Slow, pulse-level-inefficient QNN inference on NISQ devices. |
| Classical/HPC problem | Compilation time of optimal-control pulse synthesis and under-utilisation of a single QPU by one small circuit. |
| Mechanism | Partition the parameterised circuit graph, apply quantum optimal control per partition, and pack multiple programs concurrently onto the device. |
| Computational bottleneck | Quantum optimal control compilation cost, which scales badly with circuit size - addressed by partitioning. |
| Evaluation platform | Existing quantum software/hardware platforms (specific device INSUFFICIENT_EVIDENCE). |
| Scale | INSUFFICIENT_EVIDENCE |
| Performance metrics | inference speedup; compilation time reduction; inference accuracy |
| **Major claim (with baseline)** | 10.1x average (up to 10.4x) speedup over state-of-the-art QNN inference with up to 6.5x compilation-time reduction and comparable accuracy; the baseline is named only as 'state-of-the-art QNN inference' - partially BASELINE_UNCLEAR. |
| Limitation | Crosstalk and fidelity consequences of multi-programming are a known risk; accuracy is reported as comparable rather than improved across the board. |
| Relevance to future quantum-HPC | QPU sharing by multi-programming is one of the concrete mechanisms for utilising a scarce QPU in a shared facility. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-041 — Tightly-integrated quantum–classical computing using the QHDL hardware description language

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107977` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107977 |
| Census year | 2025 (online-first 2025-06-27; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107977 |
| First author (institution as given) | Gilbert Netzer — KTH Royal Institute of Technology (as given) |
| Author count | 4 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC |
| Branch | architecture_control, compiler_mapping_routing |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Latency and timing of classical feedback inside the control loop; compilation and co-simulation cost; modular description of circuits.  
**Gate 2.** A hardware description language plus compiler, debugger and co-simulation infrastructure, with classical modules realised at RTL/gate level inside the control system.  
**Gate 3.** Defines the tightly-coupled control-plane layer of the quantum-classical software stack - where classical computation must meet real-time deadlines.

| Analysis field | Content |
|---|---|
| Research question | Can digital hardware-design methodology (a VHDL-like language with synchronous interfaces) express tightly-coupled quantum-classical computation including mid-circuit classical feedback? |
| Quantum problem | Measurement-in-the-middle and dynamic circuits require classical computation inside the coherence window. |
| Classical/HPC problem | Timing-critical classical computation embedded in the control system; modular description and co-simulation of mixed quantum-classical designs. |
| Mechanism | QHDL language with modular circuit description, a compiler, a debugger and co-simulation; synchronous interfaces to RTL/gate-level classical blocks for precise timing. |
| Computational bottleneck | Classical feedback latency between measurement and conditional quantum operation. |
| Evaluation platform | Four use cases: Bell pair circuits, dynamic delay, Quantum Fourier Transform, teleportation; co-simulation infrastructure. |
| Scale | Small demonstration circuits. |
| Performance metrics | timing/coupling behaviour of classical modules; expressiveness of the modular description |
| **Major claim (with baseline)** | RTL/gate-level classical modules give coupling performance suitable for current control systems; BASELINE_UNCLEAR (no quantitative baseline language or stack reported). |
| Limitation | Demonstrated on small circuits; no deployment onto a physical control stack is reported in the retrieved material. |
| Relevance to future quantum-HPC | Addresses the tightest part of the classical-quantum loop, which sits below the runtime/scheduler layer other included papers target. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-043 — Bridging paradigms: Designing for HPC-Quantum convergence

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107980` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107980 |
| Census year | 2025 (online-first 2025-07-02; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107980 |
| First author (institution as given) | Amir Shehata — Oak Ridge National Laboratory (as given) |
| Author count | 8 |
| arXiv | 2503.01787 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, HPC_FOR_Q, FUTURE_WORKLOAD |
| Branch | hpc_qpu_integration, qpu_scheduling_resource_mgmt, quantum_runtime_orchestration |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Resource management, job scheduling and data movement between classical and quantum resources are named explicitly as the challenges addressed.  
**Gate 2.** A full software-stack architecture: quantum gateway interface, standardised resource-management APIs, scheduling mechanisms, Quantum Platform Manager API.  
**Gate 3.** This is the software-stack and scheduling blueprint for a heterogeneous CPU/GPU/QPU facility.

| Analysis field | Content |
|---|---|
| Research question | What software-stack architecture lets an HPC centre expose quantum accelerators without breaking existing HPC workflows? |
| Quantum problem | Heterogeneous, fast-changing QPU backends spanning NISQ and future fault-tolerant devices. |
| Classical/HPC problem | Resource management, job scheduling and classical-quantum data movement inside an established HPC environment. |
| Mechanism | Layered, hardware-agnostic stack: quantum gateway interface, Quantum Platform Manager API, standardised resource-management APIs, and scheduling support that preserves existing HPC workflow compatibility. |
| Computational bottleneck | Scheduling a scarce QPU against classical allocations, and moving data across the classical-quantum boundary. |
| Evaluation platform | ORNL HPC environment (architecture-level; quantitative evaluation INSUFFICIENT_EVIDENCE). |
| Scale | Centre-scale architecture. |
| Performance metrics | qualitative architectural coverage |
| **Major claim (with baseline)** | A single hardware-agnostic stack can serve both NISQ and fault-tolerant devices while keeping existing HPC workflows working; BASELINE_UNCLEAR (architecture paper, no measured baseline). |
| Limitation | Design-level contribution; the retrieved text reports no quantitative scheduling or throughput evaluation. |
| Relevance to future quantum-HPC | The most complete HPC-QPU stack specification in this journal-year window; the natural counterpart to the measurement-led FGCS-080. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-045 — NetQIR: An extension of QIR for distributed quantum computing

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107989` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107989 |
| Census year | 2025 (online-first 2025-07-03; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107989 |
| First author (institution as given) | F. Javier Cardama — CiTIUS, Universidade de Santiago de Compostela (as given) |
| Author count | 6 |
| arXiv | 2408.03712 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC |
| Branch | multi_qpu_distributed_qc, compiler_mapping_routing |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Inter-QPU communication, distributed execution and the network/hardware abstraction layer are the explicit subject.  
**Gate 2.** An intermediate representation extension with hardware-independent network communication instructions for compilers targeting distributed QPUs.  
**Gate 3.** Defines the compiler/IR layer through which multi-QPU execution would be expressed in a software stack.

| Analysis field | Content |
|---|---|
| Research question | What intermediate-representation abstractions does a compiler need to target distributed quantum computing across networked QPUs? |
| Quantum problem | Per-chip qubit limits push toward networking multiple QPUs to run one algorithm. |
| Classical/HPC problem | Absence of network- and hardware-layer abstraction in existing IRs, forcing hardware-specific distributed code. |
| Mechanism | NetQIR extends Microsoft's QIR with hardware-independent instruction specifications for inter-QPU communication, in the spirit of a message-passing abstraction. |
| Computational bottleneck | Inter-QPU communication (entanglement distribution and classical coordination) expressed at compile time. |
| Evaluation platform | Specification/compiler-infrastructure work; execution evaluation INSUFFICIENT_EVIDENCE. |
| Scale | Specification level. |
| Performance metrics | abstraction coverage of distributed communication primitives |
| **Major claim (with baseline)** | Distributed quantum programs can be expressed at IR level with hardware-independent communication instructions; BASELINE_UNCLEAR (no performance baseline). |
| Limitation | Specification without reported end-to-end distributed execution measurements. |
| Relevance to future quantum-HPC | Directly analogous to the role MPI plays for classical distributed execution; central to any multi-QPU HPC deployment. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-055 — LuGo: An enhanced quantum phase estimation implementation

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.108270` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.108270 |
| Census year | 2025 (online-first 2025-12-03; issue 2026-05) |
| Volume / issue / pages | 178 / - / 108270 |
| First author (institution as given) | Chao Lu — National Center for Computational Sciences, Oak Ridge National Laboratory (confirmed via arXiv 2503.15439) |
| Author count | 3 |
| arXiv | 2503.15439 — Verified: arXiv 2503.15439 is 'LuGo: An Enhanced Quantum Phase Estimation Implementation', Lu / Gopalakrishnan Meena / Gottiparthi, all National Center for Computational Sciences, ORNL. |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_FOR_HPC |
| Branch | compiler_mapping_routing, benchmarking_performance_modeling |
| Special collection | Advances in Quantum Computing Vol III |
| Deep-dive priority | **3 / 5** |

**Gate 1.** Classical circuit-generation time is the headline cost reduced, plus gate count and depth; parallelisation is the mechanism.  
**Gate 2.** A parallelised circuit-construction framework that removes duplicated sub-circuits - classical compilation/generation scalability.  
**Gate 3.** Circuit generation is a real classical cost in the quantum software stack, particularly for HHL-style workloads driven from a classical application.

| Analysis field | Content |
|---|---|
| Research question | Can quantum phase estimation circuits be generated and executed more cheaply by eliminating circuit duplication and parallelising construction? |
| Quantum problem | QPE circuit width/depth growth for realistic system matrices, and the fidelity cost that follows. |
| Classical/HPC problem | Classical time to generate large QPE circuits, which becomes the dominant bottleneck before any execution happens. |
| Mechanism | LuGo framework: detects and removes duplicated circuit structure and parallelises circuit generation. |
| Computational bottleneck | Classical circuit-generation time for large unitary decompositions. |
| Evaluation platform | Ideal quantum simulators; applied to HHL and a Hele-Shaw fluid-flow simulation. |
| Scale | A 2^6 x 2^6 system matrix. |
| Performance metrics | circuit generation time; gate count; circuit depth; fidelity |
| **Major claim (with baseline)** | 50.68x reduction in circuit generation time and over 31x reduction in gates and depth for a 2^6 x 2^6 system matrix, with no fidelity loss on ideal simulators; baseline is the standard (non-LuGo) QPE implementation. |
| Limitation | Fidelity claim is on ideal simulators, so noise behaviour on hardware is not established. |
| Relevance to future quantum-HPC | Makes classical circuit-generation cost visible as a scheduler-relevant term, which pure gate-count work does not. |
| Artifact | PARTIAL |
| Artifact note | Stated that the code is available for academic or commercial use on request through ORNL; no open repository URL given. |
| Conference extension | UNKNOWN |

### FGCS-057 — Efficient and scalable branch-and-bound algorithm for exact qubit allocation

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.108342` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.108342 |
| Census year | 2025 (online-first 2025-12-24; issue 2026-06) |
| Volume / issue / pages | 179 / - / 108342 |
| First author (institution as given) | Jean-Philippe Valois — INSUFFICIENT_EVIDENCE (affiliation not in dossier; co-authors Helbecque and Melab indicate a Lille/Inria lineage) |
| Author count | 3 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | compiler_mapping_routing, distributed_gpu_simulation |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Intra-node and inter-node parallelism, strong scaling on HPC infrastructure, and the runtime of an exact compilation step.  
**Gate 2.** A performance-aware parallel and distributed branch-and-bound implementation exploiting 128 cores per node and 64 nodes - core HPC methodology applied to a quantum compilation problem.  
**Gate 3.** Directly shows how much HPC capacity is needed to push exact quantum compilation to larger circuits.

| Analysis field | Content |
|---|---|
| Research question | How far can exact qubit allocation be pushed by parallelising branch-and-bound across an HPC system? |
| Quantum problem | Adapting abstract circuits to NISQ connectivity constraints optimally rather than heuristically. |
| Classical/HPC problem | Severe scalability limits of exact qubit-allocation solvers; parallel search with load balancing across nodes. |
| Mechanism | Reformulate qubit allocation as a permutation-based quadratic assignment problem; refined sequential branch-and-bound, then a parallel distributed implementation with intra-node and inter-node work distribution (Chapel/PGAS skeletons from the P3D-DFS project). |
| Computational bottleneck | Exponential search tree of the exact formulation; load imbalance across distributed workers. |
| Evaluation platform | HPC cluster: up to 128 cores per node intra-node, and 64 nodes / 8192 cores inter-node. |
| Scale | Benchmark circuits up to 26 qubits, versus prior exact limits reported around 16 qubits. |
| Performance metrics | sequential runtime vs prior exact approaches; intra-node parallel efficiency; inter-node speedup; largest circuit solved exactly |
| **Major claim (with baseline)** | The sequential version beats previous exact approaches on 20 of 21 benchmarks; the parallel version reaches over 87% of linear speedup on 128 cores and 74% of ideal speedup on 64 nodes (8192 cores), yielding exact solutions up to 26 qubits - baselines are prior exact qubit-allocation approaches and ideal linear speedup. |
| Limitation | Exact solving remains exponential; 26 qubits is far below device sizes, so the result bounds the exact approach rather than replacing heuristics. |
| Relevance to future quantum-HPC | The clearest example in this corpus of classical HPC being spent to improve quantum compilation quality, with real scaling numbers. |
| Artifact | PUBLIC_CODE — https://github.com/Guillaume-Helbecque/P3D-DFS |
| Conference extension | UNKNOWN |
| Prior-work note | Built on the P3D-DFS parallel branch-and-bound skeleton project, which has its own publication record. That is a software lineage, not an identified conference predecessor for this paper. |

### FGCS-064 — HiMA: Hierarchical quantum microarchitecture for qubit-scaling and quantum process-level parallelism

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108484` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108484 |
| Census year | 2026 (online-first 2026-03-21; issue 2026-09) |
| Volume / issue / pages | 182 / - / 108484 |
| First author (institution as given) | Qi Zhou — University of Science and Technology of China (as given; co-authors from Origin Quantum and Institute of Artificial Intelligence, Hefei) |
| Author count | 13 |
| arXiv | 2408.11311 — Content-matched: the arXiv 2408.11311 abstract page describes the HiMA hierarchical microarchitecture for quantum control. Title/author strings were not extractable from the fetched page, so the match is by content, not by string comparison. |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC |
| Branch | architecture_control, qpu_scheduling_resource_mgmt |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Process-level parallelism, throughput (CLOPS), control-system scalability to thousands of qubits, and multi-user concurrency.  
**Gate 2.** A control microarchitecture: discrete qubit-level operations, hierarchical trigger mechanisms and multiprocessing scheduling - architecture and resource-sharing design.  
**Gate 3.** Directly about how a QPU is controlled, shared between processes and scaled, which is the QPU-side counterpart to HPC job scheduling.

| Analysis field | Content |
|---|---|
| Research question | How should a quantum control microarchitecture be organised so that qubit count scales and multiple quantum processes can run concurrently? |
| Quantum problem | Control-electronics complexity and serialised single-program execution limit both qubit scaling and device utilisation. |
| Classical/HPC problem | Microarchitecture, instruction triggering and multiprocessing scheduling in the classical control plane; utilisation of a scarce shared device. |
| Mechanism | Three-part hierarchical architecture - discrete qubit-level operations, hierarchical trigger mechanisms, and multiprocessing support enabling hardware-level asynchronous execution of multiple quantum processes. |
| Computational bottleneck | Control-signal generation and trigger distribution as qubit count grows; device idle time under single-program execution. |
| Evaluation platform | Implemented for a 102-qubit superconducting processor deployed on a public quantum cloud platform; architecture stated to scale to 6144 qubits. |
| Scale | 102 qubits in deployment; 5-process parallel benchmark; 6144-qubit design target. |
| Performance metrics | speedup under multi-process execution; CLOPS (circuit layer operations per second) |
| **Major claim (with baseline)** | Up to 4.89x speedup with a 5-process parallel setup and a 3.55x CLOPS improvement; the baseline is the same system without multiprocessing (single-process execution). |
| Limitation | Results are for one superconducting platform and one vendor control stack; the 6144-qubit figure is a design projection, not a measurement. |
| Relevance to future quantum-HPC | One of very few records here that measures QPU sharing on real hardware in production, complementing the cluster-level sharing work in FGCS-080. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-065 — GraMA: A gradient matrix-guided assignment method for solving qubit mapping problems

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108485` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108485 |
| Census year | 2026 (online-first 2026-03-20; issue 2026-09) |
| Volume / issue / pages | 182 / - / 108485 |
| First author (institution as given) | Xinyu Piao — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 3 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | compiler_mapping_routing |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Compilation time and computational complexity of qubit mapping as device size and circuit complexity grow; explicitly covers multi-programming scenarios.  
**Gate 2.** Classical compilation scalability: replaces iterative combinatorial search and solver calls with a single matrix differentiation.  
**Gate 3.** Compilation latency is a direct cost on a shared QPU pipeline; the multi-programming case ties it to device sharing.

| Analysis field | Content |
|---|---|
| Research question | Can an initial qubit layout of comparable quality be obtained analytically instead of by iterative combinatorial optimisation? |
| Quantum problem | Assigning logical to physical qubits under connectivity and error constraints on growing NISQ devices. |
| Classical/HPC problem | Computational complexity and compilation time of solver-based or iterative mapping approaches at scale. |
| Mechanism | Formulate logic-to-physical mapping as a matrix-form optimisation; compute its gradient by a single matrix differentiation; use the gradient matrix, which encodes physical-qubit centrality against logical-qubit connectivity, to pick the assignment directly. |
| Computational bottleneck | Iterative combinatorial exploration and optimisation-solver calls in existing mapping methods. |
| Evaluation platform | Simulation study across circuit benchmarks, including multi-programming and large-scale device models. |
| Scale | Large-scale quantum computer models and multi-programming scenarios; exact device sizes INSUFFICIENT_EVIDENCE. |
| Performance metrics | compilation time; execution reliability / fidelity of the mapped circuit |
| **Major claim (with baseline)** | Comparable execution reliability at significantly reduced compilation time, including for multi-programming and large devices; the baseline is existing (iterative/solver-based) mapping methods, named generically - partially BASELINE_UNCLEAR. |
| Limitation | A single-shot analytic assignment gives up the optimality guarantees of exact methods such as FGCS-057. |
| Relevance to future quantum-HPC | Sits at the opposite end of the mapping trade-off from FGCS-057: cheap-and-good-enough versus exact-and-HPC-expensive. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-066 — The role of quantum computing in advancing scientific high-performance computing: A perspective from the ADAC institute

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108487` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108487 |
| Census year | 2026 (online-first 2026-03-19; issue 2026-09) |
| Volume / issue / pages | 182 / - / 108487 |
| First author (institution as given) | Gilles Buchs — INSUFFICIENT_EVIDENCE (affiliation not in dossier; ADAC is an international consortium of supercomputing centres) |
| Author count | 22 |
| arXiv | 2508.11765 |
| Article type | PERSPECTIVE · BIBLIOGRAPHY_HUB |
| Scenario tags | FUTURE_WORKLOAD, Q_IN_HPC, HPC_FOR_Q |
| Branch | hpc_qpu_integration, benchmarking_performance_modeling |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Computational efficiency, scalability limits of current quantum systems, and the division of labour with HPC resources are the explicit subject.  
**Gate 2.** A supercomputing-centre consortium view of how QC and HPC combine - integration model, workload placement and centre readiness.  
**Gate 3.** Squarely about future heterogeneous facilities: which workloads go where, and what the centres must provide.

| Analysis field | Content |
|---|---|
| Research question | What complementary roles will quantum computing and HPC play in scientific computing, from the standpoint of leading supercomputing centres? |
| Quantum problem | High error rates, limited coherence and insufficient scalability of current quantum systems for practical applications. |
| Classical/HPC problem | How supercomputing centres should plan for, host and use quantum resources alongside classical capacity. |
| Mechanism | Multi-centre perspective synthesising hardware status, application readiness and the QC-HPC integration model. |
| Computational bottleneck | Error rates and coherence limits bounding useful QPU work, against HPC capability for the same problems. |
| Evaluation platform | Perspective across ADAC member centres; no single platform. |
| Scale | 22 authors across an international consortium of supercomputing institutions. |
| Performance metrics | qualitative readiness and complementarity assessment |
| **Major claim (with baseline)** | QC and HPC are complementary rather than substitutive, and near-term value comes from integration rather than replacement; BASELINE_UNCLEAR (perspective). |
| Limitation | Consensus perspective; no measurement or implementation. |
| Relevance to future quantum-HPC | The 2026 counterpart to FGCS-010 and a primary bibliography hub for centre-level integration planning. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-073 — Universal quantum computer simulation of 50 qubits on Europe’s first exascale supercomputer harnessing its heterogeneous CPU–GPU architecture

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108592` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108592 |
| Census year | 2026 (online-first 2026-05-15; issue 2026-10) |
| Volume / issue / pages | 183 / - / 108592 |
| First author (institution as given) | Hans De Raedt — Jülich Supercomputing Centre / University of Groningen lineage (as given) |
| Author count | 8 |
| arXiv | 2511.03359 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | distributed_gpu_simulation, benchmarking_performance_modeling |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Memory capacity beyond GPU limits, CPU-GPU interconnect bandwidth, network traffic, and end-to-end runtime - all central to the contribution.  
**Gate 2.** Three explicit systems techniques: extending usable memory across the CPU-GPU interconnect into LPDDR5, adaptive data encoding to shrink the state-vector footprint, and an on-the-fly network traffic optimizer.  
**Gate 3.** This is the canonical HPC_FOR_Q result: how an exascale heterogeneous machine is engineered to hold and move a 2^50 state vector.

| Analysis field | Content |
|---|---|
| Research question | How can the heterogeneous CPU-GPU architecture of an exascale system be exploited to simulate a 50-qubit universal quantum computer? |
| Quantum problem | Exact universal quantum circuit simulation at 50 qubits, needed as a reference for device validation. |
| Classical/HPC problem | State-vector memory grows as 2^n and exceeds aggregate GPU memory; all-to-all communication for qubit permutations saturates the network. |
| Mechanism | JUQCS-50: (1) use high-bandwidth CPU-GPU interconnects and LPDDR5 to extend usable memory past GPU capacity; (2) adaptive data encoding trading precision and compute for memory footprint; (3) an on-the-fly network traffic optimizer. |
| Computational bottleneck | Aggregate memory capacity and inter-node network traffic for global-qubit operations. |
| Evaluation platform | JUPITER supercomputer with NVIDIA GH200 superchips (Europe's first exascale system). |
| Scale | 50 qubits; exact node count INSUFFICIENT_EVIDENCE from the retrieved abstract. |
| Performance metrics | qubit count simulated; speedup versus previous record; memory footprint; network traffic |
| **Major claim (with baseline)** | 16.6-fold speedup over the previous 48-qubit record - the baseline is explicitly the earlier JUQCS 48-qubit run on the K computer, so this compares across two different machines and two software generations. |
| Limitation | Adaptive data encoding trades precision for memory, so results at 50 qubits carry an accuracy caveat relative to full double precision. |
| Relevance to future quantum-HPC | Defines the current classical-simulation ceiling that any quantum-advantage claim must clear, and shows which exascale hardware features carry it. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |
| Prior-work note | Continues the JUQCS simulator line from Julich, whose prior 48-qubit K computer result is the stated baseline. The prior JUQCS publications are journal articles, not a conference predecessor of this paper. |

### FGCS-079 — Workflow decomposition algorithm for scheduling with quantum annealer-based hybrid solver

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108686` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108686 |
| Census year | 2026 (online-first 2026-06-30; issue 2026-12) |
| Volume / issue / pages | 185 / - / 108686 |
| First author (institution as given) | Marcin Kroczek — INSUFFICIENT_EVIDENCE for the exact first-author affiliation; the QHyper toolchain and the co-author record point to AGH University of Krakow. |
| Author count | 3 |
| arXiv | 2506.01567 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_FOR_HPC, Q_IN_HPC |
| Branch | scientific_workflow_application, hybrid_workflow, qpu_scheduling_resource_mgmt |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Scientific workflow scheduling under deadlines, solver capacity as the binding resource limit, and decomposition to fit it - scheduling and resource allocation.  
**Gate 2.** A decomposition algorithm (series-parallel / TTSP-based) plus workload-weighted deadline distribution that turns an over-sized workflow-scheduling instance into solver-ready subproblems for a hybrid quantum solver.  
**Gate 3.** Shows concretely how a capacity-limited quantum solver can be slotted into a real workflow-scheduling pipeline, and at what quality cost.

| Analysis field | Content |
|---|---|
| Research question | How can workflow-scheduling instances be decomposed so that a capacity-limited quantum annealer-based hybrid solver can handle realistic scientific workflows? |
| Quantum problem | Limited variable capacity of quantum and hybrid solvers relative to real problem sizes. |
| Classical/HPC problem | Scheduling scientific workflows (task graphs) onto resources under deadline and cost objectives. |
| Mechanism | Series-Parallel Workflow Decomposition (SPWD): a two-terminal series-parallel heuristic that splits the workflow graph, plus workload-weighted deadline distribution across the resulting subproblems, each solved by the D-Wave CQM hybrid solver via the QHyper toolchain. |
| Computational bottleneck | Solver variable-capacity limit; quality loss introduced by decomposition. |
| Evaluation platform | D-Wave Constrained Quadratic Model hybrid solver; Gurobi as the classical reference; real workflows from WfCommons. |
| Scale | Real-life scientific workflow instances from WfCommons, including instances the undecomposed solver could not handle. |
| Performance metrics | solvable instance size; schedule cost versus Gurobi reference |
| **Major claim (with baseline)** | SPWD lets the D-Wave CQM solver handle previously unsolvable instances, at a cost increase of up to 17.5% - the baseline is explicitly the Gurobi reference solution. |
| Limitation | Decomposition costs up to 17.5% schedule quality, and the comparison shows the classical solver still produces better schedules where it can run. |
| Relevance to future quantum-HPC | A rare honest accounting of what a quantum solver buys and costs inside a real HPC workflow-scheduling pipeline. |
| Artifact | UNKNOWN |
| Artifact note | The paper states that the SPWD Python source and the experimental results are held in GitHub repositories, but no URL was recoverable from the ScienceDirect abstract page or from the arXiv preprint (2506.01567), so the artifact could not be verified. Downgraded from PUBLIC_CODE to UNKNOWN rather than asserting an unverified URL. |
| Conference extension | UNKNOWN |

### FGCS-080 — Three ways to share a QPU: Scheduling strategies for hybrid Quantum-HPC applications

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108699` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108699 |
| Census year | 2026 (online-first 2026-07-09; issue 2026-12) |
| Volume / issue / pages | 185 / - / 108699 |
| First author (institution as given) | Marco Cipollini — INSUFFICIENT_EVIDENCE (affiliation not in dossier; the author list spans Italian and Spanish HPC centres and E4/LINKS-type partners) |
| Author count | 24 |
| arXiv | 2604.14955 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, HPC_FOR_Q, FUTURE_WORKLOAD |
| Branch | qpu_scheduling_resource_mgmt, hpc_qpu_integration, hybrid_workflow, quantum_runtime_orchestration |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Scheduling, resource allocation, utilisation and execution time on production HPC clusters, with the QPU as the scarce resource.  
**Gate 2.** Three concrete systems mechanisms compared head to head: time-based multiplexing, dynamic resource management (malleability), and workflow decomposition.  
**Gate 3.** This is the heterogeneous-scheduling question stated and measured directly.

| Analysis field | Content |
|---|---|
| Research question | Which scheduling strategy should an HPC centre use to share a scarce QPU among hybrid quantum-classical jobs, and under which workload balance? |
| Quantum problem | QPU scarcity and immature quantum software stacks; mismatch between quantum and classical programming models. |
| Classical/HPC problem | Standard HPC scheduling mechanisms cannot express a job that holds classical nodes while waiting on a scarce accelerator, wasting classical resources. |
| Mechanism | Implementation and comparison of three strategies - time-based multiplexing of QPU access, dynamic resource management/malleability that releases classical nodes during quantum phases, and workflow decomposition that splits hybrid jobs into separately schedulable stages. |
| Computational bottleneck | Classical nodes idling while a job waits on the QPU, and QPU idling between hybrid iterations. |
| Evaluation platform | Production HPC clusters plus real quantum hardware. |
| Scale | Multiple workload scenarios spanning quantum/classical balance; exact node and QPU counts INSUFFICIENT_EVIDENCE. |
| Performance metrics | classical resource consumption; QPU utilisation; cluster-level execution time |
| **Major claim (with baseline)** | Malleability and workflow decomposition cut classical resource consumption by up to 45.7% and 64% respectively for balanced hybrid jobs, while time-multiplexing gives the best QPU utilisation and cluster execution time under strong classical-quantum imbalance - the baseline is standard (non-adaptive) HPC scheduling of the same hybrid workloads. |
| Limitation | The three strategies are complementary rather than dominant, so a production scheduler needs a policy to choose among them, which the paper frames as remaining work. |
| Relevance to future quantum-HPC | The single most directly on-target paper in this FGCS census: real QPUs, production clusters, and QPU sharing measured three ways. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-A02 — Closed-loop calculations of electronic structure on a quantum processor and a classical supercomputer at full scale

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108731` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108731 |
| Census year | 2026 (online-first 2026-07-29; issue 2027-01) |
| Volume / issue / pages | 186 / - / 108731 |
| First author (institution as given) | Tomonori Shirakawa — RIKEN (as given by co-author affiliation pattern; exact first-author affiliation INSUFFICIENT_EVIDENCE). Author list spans RIKEN/R-CCS and IBM Quantum. |
| Author count | 21 |
| arXiv | 2511.00224 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, HPC_FOR_Q, Q_FOR_HPC, FUTURE_WORKLOAD |
| Branch | hpc_qpu_integration, hybrid_workflow, quantum_runtime_orchestration, scientific_workflow_application |
| Deep-dive priority | **5 / 5** |

**Gate 1.** Resource orchestration across 152,064 classical nodes and a co-located QPU; the paper's own stated aim is to characterise the scalability and efficiency of hybrid quantum-classical workflows, i.e. scaling, orchestration and communication between the two resources.  
**Gate 2.** The contribution is the closed-loop HPC-QPU workflow itself: an on-premises Heron processor coupled to a full supercomputer allocation, with the classical side doing the heavy post-processing at full machine scale. This is quantum accelerator integration into HPC and hybrid workflow orchestration, not a chemistry method paper.  
**Gate 3.** The clearest existing measurement of what full-scale CPU<->QPU coupling costs and how far it scales; it directly informs resource usage, execution and orchestration for heterogeneous facilities.

| Analysis field | Content |
|---|---|
| Research question | How do a quantum processor and a full-scale classical supercomputer interact in a closed loop, and how should the scalability and efficiency of such a hybrid workflow be characterised? |
| Quantum problem | Sampling electronic-structure configurations on a Heron processor for chemistry models beyond the reach of exact diagonalization. |
| Classical/HPC problem | Orchestrating a closed loop between a QPU and an entire supercomputer allocation - dispatching quantum samples, running the classical post-processing across 152,064 nodes, and returning results into the next iteration, at a scale where scheduling and data movement dominate. |
| Mechanism | Closed-loop quantum-centric supercomputing workflow: an on-premises IBM Heron quantum processor issues samples, the full Fugaku allocation performs the classical solve/post-processing, and the loop iterates. The systems contribution is the orchestration of the two resources at full machine scale. |
| Computational bottleneck | Classical post-processing of quantum samples, which is what consumes the full-machine allocation; plus the coordination/latency of the QPU-to-supercomputer loop. |
| Evaluation platform | IBM Heron quantum processor deployed on premises with the supercomputer Fugaku (RIKEN R-CCS). |
| Scale | 152,064 classical Fugaku nodes - the entire machine; Heron qubit count INSUFFICIENT_EVIDENCE from the retrieved abstract. |
| Performance metrics | scale of classical resources orchestrated (node count); accuracy of the approximated electronic structure; workflow scalability/efficiency characterisation |
| **Major claim (with baseline)** | The largest electronic-structure computation to date combining quantum and classical HPC, reaching accuracy comparable to some all-classical approximation methods - the baseline is explicitly (a) exact diagonalization, which the chemistry models are stated to exceed, and (b) all-classical approximation methods for the accuracy comparison. No speedup or advantage over the classical methods is claimed, and none should be read in. |
| Limitation | Accuracy is stated as comparable to, not better than, classical approximation methods, so the result demonstrates orchestration capability rather than quantum advantage. The workflow consumes an entire national supercomputer for one chemistry problem, which bounds its practicality. Per-component timing and the classical/quantum time split are INSUFFICIENT_EVIDENCE from the abstract. |
| Relevance to future quantum-HPC | The upper bound on what HPC-QPU coupling currently achieves in production. Together with FGCS-080 (scheduling three ways to share a QPU) it gives this corpus both the policy question and the full-scale existence measurement. Separate the chemistry result, which is not this corpus's interest, from the orchestration result, which is. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Artifact note | No code or data availability statement in the arXiv abstract page or the retrieved metadata. |
| Conference extension | UNKNOWN |
| Notes | EXISTENCE_CHECK_SEED ('closed-loop quantum processor + Fugaku work') - confirmed to exist and assessed on its own merits, not admitted because it was seeded. Recovered by the extended cover-date sweep. |

### FGCS-A03 — DistributedEstimator: Distributed training of quantum neural networks via circuit cutting

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108746` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108746 |
| Census year | 2026 (online-first 2026-08-02; issue 2027-01) |
| Volume / issue / pages | 186 / - / 108746 |
| First author (institution as given) | Prabhjot Singh — INSUFFICIENT_EVIDENCE |
| Author count | 3 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q, Q_IN_HPC |
| Branch | circuit_cutting_reconstruction, multi_qpu_distributed_qc, benchmarking_performance_modeling |
| Deep-dive priority | **4 / 5** |

**Gate 1.** Per-query time breakdown, parallel execution, exponential subexperiment growth, scaling limits and straggler sensitivity - distributed-execution cost is the measured quantity throughout.  
**Gate 2.** Circuit-cutting reconstruction cost treated explicitly as a staged distributed workload, with the pipeline instrumented across partitioning, subexperiment generation, parallel execution and classical reconstruction. 'Circuit-cutting reconstruction cost' is a named INCLUDE shape in Gate 2.  
**Gate 3.** Quantifies which stage of a cut-circuit workload dominates wall-clock time and where it stops scaling - directly informs execution, communication and runtime design for distributed quantum workloads.

| Analysis field | Content |
|---|---|
| Research question | Where does time actually go in a circuit-cutting pipeline treated as a staged distributed workload, and where does it stop scaling? |
| Quantum problem | Circuits too large for one device must be cut into independent subcircuits, whose results are then classically reconstructed. |
| Classical/HPC problem | Classical reconstruction cost, exponential subexperiment fan-out, parallel scheduling of subexperiments and straggler sensitivity in the distributed execution stage. |
| Mechanism | DistributedEstimator: a cut-aware estimator pipeline that treats circuit cutting as a staged distributed workload, instrumented across partitioning, subexperiment generation, parallel execution and classical reconstruction, with runtime traces collected per stage. Built on qiskit-addon-cutting and qiskit-machine-learning with PyTorch. |
| Computational bottleneck | Classical reconstruction, measured as the dominant per-query cost (median 53%, 95th percentile 58% at three cuts), and O(9^c) subexperiment growth in the number of cuts. |
| Evaluation platform | Qiskit circuit-cutting and machine-learning addons with PyTorch; runtime traces on Iris and MNIST classification tasks. |
| Scale | Limited to small qubit counts by the O(9^c) subexperiment growth, as the paper itself reports. |
| Performance metrics | per-query time share by pipeline stage; subexperiment count growth O(9^c); scaling limit; straggler sensitivity; accuracy and robustness preservation |
| **Major claim (with baseline)** | Reconstruction dominates per-query time - median 53% and 95th-percentile 58% at three cuts - and O(9^c) subexperiment growth confines practical experiments to small qubit counts. The baseline is the paper's own uncut / fewer-cut configurations and the per-stage decomposition of its own pipeline; there is no external system baseline, so cross-system comparison is BASELINE_UNCLEAR. |
| Limitation | The workload is QNN training on Iris and MNIST, which are small ML benchmarks rather than HPC-scale workloads, and the reported scaling limit is a property of circuit cutting itself rather than of the implementation. |
| Relevance to future quantum-HPC | Supplies the measured cost profile of circuit cutting - the stage-level accounting that makes reconstruction, not quantum execution, the thing a scheduler must budget for. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Artifact note | No availability statement found. The work builds on open-source components (qiskit-addon-cutting, qiskit-machine-learning, PyTorch), but those are dependencies, not this paper's artifact. |
| Conference extension | UNKNOWN |
| Notes | The coordinator anticipated BORDERLINE / NO_ABSTRACT. The ScienceDirect abstract page resolved on the first attempt, so this is classified on evidence rather than on title. The QML *target* (QNN training) is a documented false-positive class, but the *contribution* is distributed-execution cost measurement of circuit cutting, which is a named Gate 2 INCLUDE shape - so the tension the coordinator flagged resolves to INCLUDED. Recovered by the extended cover-date sweep. |

---

## 5. BORDERLINE records (8)

Recorded, not discarded. None are counted in the included population.

### FGCS-016 — Assessing and advancing the potential of quantum computing: A NASA case study

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.06.012` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.06.012 |
| Census year | 2024 (online-first 2024-06-12; issue 2024-11) |
| Volume / issue / pages | 160 / - / 598-618 |
| First author (institution as given) | Eleanor G. Rieffel — NASA Ames Research Center (as given) |
| Author count | 23 |
| arXiv | 2406.15601 |
| Article type | PERSPECTIVE · BIBLIOGRAPHY_HUB |
| Scenario tags | FUTURE_WORKLOAD, HPC_FOR_Q |
| Branch | benchmarking_performance_modeling |
| Deep-dive priority | **2 / 5** |

**Reasons FOR inclusion.** Institution-scale assessment of where QPUs can beat supercomputers; covers algorithms, hardware evaluation and application readiness across a national-lab programme; a useful bibliography hub.

**Reasons AGAINST inclusion.** Primary substance is algorithms and application assessment; no scheduling, runtime, orchestration or simulation-systems contribution is evidenced in the abstract.

**Gate 1.** Partially: the paper frames QPU capability against 'the largest supercomputers' and reports assessment work, but no specific classical systems mechanism is identified in the retrieved abstract.  
**Gate 2.** Partially: a programme-level assessment methodology, not an HPC/systems technique in itself.  
**Gate 3.** Yes at the level of readiness and workload placement, weakly at the level of runtime/scheduling mechanism.

| Analysis field | Content |
|---|---|
| Research question | How should a research agency assess and advance the practical potential of quantum computing across algorithms, hardware and applications? |
| Quantum problem | NISQ device limitations versus useful real-world application requirements. |
| Classical/HPC problem | INSUFFICIENT_EVIDENCE (classical systems mechanism not identified in the retrieved abstract). |
| Mechanism | Programme case study spanning near- and long-term algorithms, hardware evaluation and application exploration. |
| Computational bottleneck | INSUFFICIENT_EVIDENCE |
| Evaluation platform | Multiple quantum hardware platforms and classical assessment tooling; specifics INSUFFICIENT_EVIDENCE. |
| Scale | Multi-year, 23-author programme review. |
| Performance metrics | qualitative readiness assessment |
| **Major claim (with baseline)** | NISQ processors remain too small and noisy for direct real-world application use despite specialised advantage demonstrations; BASELINE_UNCLEAR. |
| Limitation | Breadth-over-depth programme narrative; systems content is not separable from algorithm content in the abstract. |
| Relevance to future quantum-HPC | Useful as a citation hub for workload-placement arguments; weak as a systems-mechanism source. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

### FGCS-020 — Quantum resource estimation for large scale quantum algorithms

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2024.107480` |
| Publisher URL | https://doi.org/10.1016/j.future.2024.107480 |
| Census year | 2024 (online-first 2024-08-12; issue 2025-01) |
| Volume / issue / pages | 162 / - / 107480 |
| First author (institution as given) | Vlad Gheorghiu — softwareQ Inc. / Institute for Quantum Computing (as given) |
| Author count | 2 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | FUTURE_WORKLOAD |
| Branch | benchmarking_performance_modeling |
| Deep-dive priority | **2 / 5** |

**Reasons FOR inclusion.** Quantifies QEC overhead in both qubits and runtime and puts classical and quantum algorithm costs on a common footing - genuine performance/resource modeling for future heterogeneous systems.

**Reasons AGAINST inclusion.** Criteria treat 'resource estimates with no systems mechanism' as a false-positive class; the application is cryptanalysis and no classical systems technique is part of the contribution.

**Gate 1.** Partially: qubit counts and runtime under surface-code fault tolerance are quantified, but the costed resource is the QPU, not a classical system.  
**Gate 2.** Partially: a comparison framework for classical versus quantum algorithm cost - performance modeling in spirit, but no classical systems mechanism (no parallel estimator, no compilation-scalability result) is evidenced.  
**Gate 3.** Yes for sizing future fault-tolerant machines and for deciding which workloads a QPU could ever take.

| Analysis field | Content |
|---|---|
| Research question | How should the cost of a large-scale fault-tolerant quantum algorithm be estimated and compared against its best classical counterpart? |
| Quantum problem | Logical-to-physical overhead of quantum error correction for large algorithms. |
| Classical/HPC problem | Cost model for the classical algorithms being compared against (Gate 1 only partially satisfied). |
| Mechanism | Framework accounting for surface-code QEC overhead in qubits and runtime, applied to cryptanalytic algorithms. |
| Computational bottleneck | Physical-qubit and runtime overhead of fault tolerance. |
| Evaluation platform | Analytical/resource-estimation tooling; no HPC measurement reported. |
| Scale | Large-scale (cryptanalysis-scale) algorithm instances; exact figures INSUFFICIENT_EVIDENCE. |
| Performance metrics | physical qubit count; logical runtime; QEC overhead factor |
| **Major claim (with baseline)** | Provides snapshot estimates of realistic costs of quantum attacks on widely used cryptographic algorithms; BASELINE_UNCLEAR for any classical-machine comparison. |
| Limitation | Estimates are architecture-assumption dependent (surface code, specific error rates); no classical compute cost of the estimation itself is reported. |
| Relevance to future quantum-HPC | Feeds workload-placement and machine-sizing arguments; weak on classical systems mechanism. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-034 — Is quantum optimization ready? An effort towards neural network compression using adiabatic quantum computing

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107908` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107908 |
| Census year | 2025 (online-first 2025-05-30; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107908 |
| First author (institution as given) | Zhehui Wang — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 7 |
| arXiv | 2505.16332 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_FOR_HPC, FUTURE_WORKLOAD |
| Branch | benchmarking_performance_modeling |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **2 / 5** |

**Reasons FOR inclusion.** A Q_FOR_HPC readiness study on a workload (large-model compression) that is genuinely compute- and memory-bound; asks the placement question directly.

**Reasons AGAINST inclusion.** The contribution is an application of adiabatic quantum computing to an optimisation problem; annealer/QUBO application is a documented false-positive class here.

**Gate 1.** Partially: model size and sustainable deployment cost of large DNNs are named as the motivating constraint.  
**Gate 2.** Partially: mapping a large-scale DNN compression problem onto a capacity-limited annealer requires decomposition, but no classical systems technique is evidenced as the main contribution.  
**Gate 3.** Weakly: informs whether a quantum optimiser could serve a real classical ML workload.

| Analysis field | Content |
|---|---|
| Research question | Is adiabatic quantum optimisation mature enough to be applied to deep neural network compression? |
| Quantum problem | Limited annealer capacity and connectivity versus very large optimisation instances. |
| Classical/HPC problem | Cost of optimising and deploying ever-larger DNN models. |
| Mechanism | Formulation of DNN compression for AQC plus the handling needed to fit it to device capacity (details INSUFFICIENT_EVIDENCE). |
| Computational bottleneck | Annealer size/connectivity versus problem size. |
| Evaluation platform | Adiabatic quantum computing hardware/simulation (specifics INSUFFICIENT_EVIDENCE). |
| Scale | INSUFFICIENT_EVIDENCE |
| Performance metrics | compression quality; solution quality vs classical optimiser |
| **Major claim (with baseline)** | Assesses readiness of quantum optimisation for DNN compression; BASELINE_UNCLEAR. |
| Limitation | Readiness framing implies the answer is qualified; device-capacity limits dominate. |
| Relevance to future quantum-HPC | A concrete data point on whether a QPU can take an AI-workload sub-problem in a heterogeneous centre. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-037 — Solving combinatorial optimization and machine learning problems on hybrid near-term quantum photonic computers

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107934` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107934 |
| Census year | 2025 (online-first 2025-06-23; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107934 |
| First author (institution as given) | Mateusz Slysz — Poznan Supercomputing and Networking Center (as given) |
| Author count | 7 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC, Q_FOR_HPC |
| Branch | hpc_qpu_integration, benchmarking_performance_modeling |
| Deep-dive priority | **3 / 5** |

**Reasons FOR inclusion.** Explicitly frames photonic QPUs as data-centre accelerators, uses real photonic hardware coupled to GPUs, reports a scaling improvement from a tiling technique, and lists multi-QPU among its keywords.

**Reasons AGAINST inclusion.** The headline outcomes are solution quality on optimisation and ML benchmarks; no scheduling, runtime or resource-management mechanism is evidenced.

**Gate 1.** Scaling is addressed: a tiling technique is reported to turn quadratic into linear scaling for larger problems, and GPU-plus-photonic-QPU coupling is described.  
**Gate 2.** Partially: the hybrid photonic-QPU + GPU integration and multi-QPU keyword point at accelerator integration, but the reported results are algorithmic quality on Max-Cut, JSSP and QNNs.  
**Gate 3.** Yes in framing (QPUs as accelerators in supercomputing and data centres), weaker in measured systems evidence.

| Analysis field | Content |
|---|---|
| Research question | Can a photonic QPU coupled to GPUs solve combinatorial optimisation and ML problems at practically relevant sizes? |
| Quantum problem | Limited size and noise of near-term photonic (boson-sampling) devices. |
| Classical/HPC problem | Coupling a room-temperature photonic accelerator to GPU compute and scaling the problem-decomposition step. |
| Mechanism | Hybrid photonic-QPU + GPU pipeline with a Binary Bosonic Solver and an improved tiling technique for problem decomposition. |
| Computational bottleneck | Device mode count limiting instance size; tiling overhead. |
| Evaluation platform | Photonic quantum computer operating at room temperature plus GPUs. |
| Scale | Max-Cut and Job Shop Scheduling instances larger than previously reported for this platform; exact sizes INSUFFICIENT_EVIDENCE. |
| Performance metrics | solution quality vs exhaustive search; instance size reached; scaling behaviour of tiling |
| **Major claim (with baseline)** | The Binary Bosonic Solver beats complete solution search on larger Max-Cut instances and solves substantially larger JSSP instances than prior work on this platform; hybrid QNNs gained stability but no clear quality advantage over classical networks. |
| Limitation | Hybrid neural networks showed no clear quality advantage; a corrigendum was subsequently issued (FGCS-060). |
| Relevance to future quantum-HPC | One of few FGCS records using a physical non-superconducting QPU coupled to classical accelerators in a supercomputing-centre context. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |
| Notes | Corrected by FGCS-060 (corrigendum, 10.1016/j.future.2026.108408). |

### FGCS-040 — A multiple-circuit approach to quantum resource reduction with application to the quantum lattice Boltzmann method

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.107975` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.107975 |
| Census year | 2025 (online-first 2025-07-01; issue 2026-01) |
| Volume / issue / pages | 174 / - / 107975 |
| First author (institution as given) | Melody Lee — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 6 |
| arXiv | 2401.12248 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_FOR_HPC, FUTURE_WORKLOAD |
| Branch | circuit_cutting_reconstruction, benchmarking_performance_modeling |
| Special collection | Advances in Quantum Computing Vol II |
| Deep-dive priority | **3 / 5** |

**Reasons FOR inclusion.** Uses parallel multi-circuit execution as the mechanism, which maps onto shot/circuit orchestration; targets a canonical HPC workload (CFD).

**Reasons AGAINST inclusion.** Core contribution is an algorithm reformulation of QLBM; no classical systems technique or measured systems cost is reported.

**Gate 1.** Partially: CFD workloads are framed by trillions of grid points and millions of time steps, and the paper targets resource (qubit/depth) cost; the resource costed is quantum, not classical.  
**Gate 2.** Partially: splitting one circuit into many circuits executed in parallel is an execution-model change, but no classical runtime, scheduler or simulator mechanism is contributed.  
**Gate 3.** Yes at the level of execution model - how many circuits and shots a CFD time step would demand of a QPU.

| Analysis field | Content |
|---|---|
| Research question | Can splitting a quantum lattice Boltzmann computation across multiple circuits reduce per-circuit quantum resource requirements? |
| Quantum problem | Single-circuit QLBM formulations demand more qubits and depth than noisy devices can support. |
| Classical/HPC problem | Computational burden of CFD simulations at production grid sizes. |
| Mechanism | Multi-circuit QLBM decomposition executed in parallel, reducing per-circuit width/depth at the cost of more circuit executions. |
| Computational bottleneck | Circuit depth and noise per circuit; total shot count after decomposition. |
| Evaluation platform | Quantum simulation (specific platform INSUFFICIENT_EVIDENCE). |
| Scale | INSUFFICIENT_EVIDENCE |
| Performance metrics | qubit count; circuit depth; number of circuits |
| **Major claim (with baseline)** | Multi-circuit decomposition lowers per-circuit quantum resource requirements for QLBM; BASELINE_UNCLEAR (comparison is against single-circuit QLBM formulations, quantitative factors not stated in retrieved text). |
| Limitation | More circuits means more executions and more classical reconstruction work; that trade-off cost is not quantified in the retrieved abstract. |
| Relevance to future quantum-HPC | Illustrates the shot/circuit-count pressure a quantum-accelerated CFD workload would place on an HPC-QPU scheduler. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-049 — A hybrid quantum-classical particle-in-cell method for plasma simulations

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.108087` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.108087 |
| Census year | 2025 (online-first 2025-08-20; issue 2026-02) |
| Volume / issue / pages | 175 / - / 108087 |
| First author (institution as given) | Pratibha Raghupati Hegde — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 7 |
| arXiv | 2505.09260 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_FOR_HPC, FUTURE_WORKLOAD |
| Branch | scientific_workflow_application, hybrid_workflow |
| Special collection | Advances in Quantum Computing Vol III |
| Deep-dive priority | **3 / 5** |

**Reasons FOR inclusion.** A concrete kernel-offload study on a canonical HPC application (PIC plasma simulation) with computational cost measured as a primary outcome; exactly the coupling pattern a heterogeneous centre would face.

**Reasons AGAINST inclusion.** The quantum part runs on a PennyLane simulator rather than a QPU, and the mechanism is a hybrid neural-network solver (adjacent to false-positive class 5) rather than a systems technique.

**Gate 1.** Computational cost of the hybrid method is explicitly evaluated alongside accuracy against a standard PIC benchmark.  
**Gate 2.** Partially: the contribution is a hybrid solver plus a cost/accuracy evaluation, not a runtime, scheduler or simulator-systems technique.  
**Gate 3.** Yes at the workload level - it quantifies what offloading one kernel (the Poisson solve) of a production-style scientific code to a quantum backend costs.

| Analysis field | Content |
|---|---|
| Research question | What accuracy and computational cost result from replacing the electrostatic Poisson solver in a PIC code with a hybrid classical-quantum neural network? |
| Quantum problem | Expressing a field solver as a trainable quantum circuit with acceptable accuracy. |
| Classical/HPC problem | Cost of the field solve within a PIC time-step loop, and the cost of the classical-quantum round trip around it. |
| Mechanism | Hybrid classical-quantum neural network (data-driven and physics-informed training) replaces the electrostatic Poisson solver; particle push and field interpolation stay classical. |
| Computational bottleneck | Per-time-step cost of the quantum-simulated solver relative to a classical Poisson solve. |
| Evaluation platform | PennyLane quantum simulator for the quantum part; classical system for particle motion and interpolation. |
| Scale | Two-stream instability benchmark; grid/particle counts INSUFFICIENT_EVIDENCE. |
| Performance metrics | solution accuracy vs classical PIC; computational cost of the hybrid approach |
| **Major claim (with baseline)** | The hybrid PIC reproduces the two-stream instability benchmark; the accompanying computational-cost comparison is against classical PIC (direction and magnitude of the cost difference INSUFFICIENT_EVIDENCE from the retrieved abstract). |
| Limitation | Simulator-based, so the reported cost is simulation cost rather than QPU execution cost; no hardware run reported. |
| Relevance to future quantum-HPC | A candid cost-side data point on scientific-application coupling, which the more architectural papers in this corpus do not supply. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |

### FGCS-058 — Cost-efficient quantum cloud task offloading with quantum-inspired particle swarm optimization

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2025.108095` |
| Publisher URL | https://doi.org/10.1016/j.future.2025.108095 |
| Census year | 2026 (online-first not stated; issue 2026-02) |
| Volume / issue / pages | 175 / - / 108095 |
| First author (institution as given) | Santanu Ghosh — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 2 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | Q_IN_HPC |
| Branch | qpu_scheduling_resource_mgmt |
| Deep-dive priority | **2 / 5** |

**Reasons FOR inclusion.** The problem addressed - deciding which tasks go to which quantum cloud resource at what cost - is exactly QPU resource allocation, which this corpus cares about.

**Reasons AGAINST inclusion.** The mechanism is a quantum-inspired classical metaheuristic (false-positive class 2), and no abstract was retrievable, so the systems substance is unverified.

**Gate 1.** Plausibly yes: task offloading to quantum cloud resources is a resource-allocation and cost problem, but NO_ABSTRACT means this is inferred from the title only.  
**Gate 2.** Doubtful: the stated method is a quantum-inspired particle swarm optimiser, a documented false-positive class, applied as a heuristic solver.  
**Gate 3.** Plausibly yes for QPU resource allocation in a cloud setting; unverified.

| Analysis field | Content |
|---|---|
| Research question | How should tasks be offloaded to quantum cloud resources to minimise cost? (inferred from title; NO_ABSTRACT) |
| Quantum problem | INSUFFICIENT_EVIDENCE |
| Classical/HPC problem | Task offloading / resource allocation and cost optimisation across quantum cloud resources (inferred). |
| Mechanism | Quantum-inspired particle swarm optimisation used as the offloading decision heuristic (from title). |
| Computational bottleneck | INSUFFICIENT_EVIDENCE |
| Evaluation platform | INSUFFICIENT_EVIDENCE |
| Scale | INSUFFICIENT_EVIDENCE |
| Performance metrics | INSUFFICIENT_EVIDENCE |
| **Major claim (with baseline)** | INSUFFICIENT_EVIDENCE - NO_ABSTRACT; BASELINE_UNCLEAR. |
| Limitation | NO_ABSTRACT: classification rests on the title alone. |
| Relevance to future quantum-HPC | Potentially relevant to QPU allocation policy; requires full-text reading before any use. |
| Artifact | UNKNOWN |
| Conference extension | UNKNOWN |
| Notes | NO_ABSTRACT. Resolve by full-text read before including in any downstream count. |

### FGCS-063 — Addressing the minor-embedding problem in quantum annealing and evaluating state-of-the-art algorithm performance

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2026.108481` |
| Publisher URL | https://doi.org/10.1016/j.future.2026.108481 |
| Census year | 2026 (online-first 2026-03-17; issue 2026-09) |
| Volume / issue / pages | 182 / - / 108481 |
| First author (institution as given) | Aitor Gómez-Tejedor — INSUFFICIENT_EVIDENCE (affiliation not in dossier) |
| Author count | 3 |
| Article type | ORIGINAL_RESEARCH |
| Scenario tags | HPC_FOR_Q |
| Branch | compiler_mapping_routing, benchmarking_performance_modeling |
| Deep-dive priority | **3 / 5** |

**Reasons FOR inclusion.** Treats embedding as a compilation/mapping stage and quantifies both its runtime and its downstream effect on solution error - the same shape as included qubit-mapping work (FGCS-033, FGCS-065).

**Reasons AGAINST inclusion.** The platform is a quantum annealer (adjacent to false-positive class 2), and the output is an evaluation of an existing tool (Minorminer) rather than a systems mechanism.

**Gate 1.** Execution-time performance of the embedding algorithm and the quality/robustness of its output are measured, i.e. the cost of the annealer's mapping step.  
**Gate 2.** Partially: minor-embedding is the annealer analogue of qubit mapping/compilation and the paper evaluates its scalability, but the contribution is an empirical evaluation rather than a technique.  
**Gate 3.** Yes for resource usage and mapping quality on annealer hardware, weaker for scheduling/runtime.

| Analysis field | Content |
|---|---|
| Research question | How much does embedding quality affect annealer solution error, and how good and how fast is Minorminer at producing embeddings? |
| Quantum problem | Non-hardware-native problem topologies must be minor-embedded onto the annealer graph, with chains degrading results. |
| Classical/HPC problem | Runtime and robustness of the classical embedding algorithm, and the quality/error trade-off it imposes. |
| Mechanism | Systematic experimental study: correlate average chain length with relative solution error, then benchmark Minorminer's embedding capability, quality, robustness and execution time on Erdos-Renyi graphs, with Clique Embedding as a deterministic worst-case reference. |
| Computational bottleneck | Embedding search time and chain length growth as graph density rises. |
| Evaluation platform | D-Wave Systems quantum annealers; Minorminer and Clique Embedding. |
| Scale | Erdos-Renyi graph families; sizes INSUFFICIENT_EVIDENCE. |
| Performance metrics | average chain length; relative solution error; embedding success rate; embedding execution time |
| **Major claim (with baseline)** | A clear correlation holds between average chain length and relative solution error, and Minorminer leaves substantial room for improvement; baselines are Minorminer itself and Clique Embedding as a worst case. |
| Limitation | Annealer-specific; results do not transfer directly to gate-model qubit mapping. |
| Relevance to future quantum-HPC | Quantifies a compilation-stage cost that any annealer-hosting facility would have to budget for. |
| Artifact | NO_PUBLIC_ARTIFACT_FOUND |
| Conference extension | UNKNOWN |

---

## 6. OUT_OF_WINDOW record (1)

### FGCS-001 — Effective quantum volume, fidelity and computational cost of noisy quantum processing experiments

| Field | Value |
|---|---|
| DOI | `10.1016/j.future.2023.12.002` |
| Publisher URL | https://doi.org/10.1016/j.future.2023.12.002 |
| First public availability | **2023-12-04** |
| Volume / pages / issue cover date | 153 / 431-441 / 2024-04 |
| First author | K. Kechedzhi (+6) |
| arXiv | 2306.15970 |
| Article type | ORIGINAL_RESEARCH |
| Verdict | **OUT_OF_WINDOW** |
| Prior verdict | INCLUDED (vacated on window correction, not on merit - the Three-Gate assessment below still stands) |

**Why it is out of window.** First public availability is 2023-12-04 (OpenAlex publication_date and Crossref created date; the DOI stem j.future.2023.12 is the Elsevier acceptance month). The 2024-04 cover date of volume 153 was used in error. Outside the 2024-2026 census window. Assessment retained for audit; removed from the INCLUDED and 2024 counts.

**Assessment retained for audit.** Gate 1: Computational cost of classical simulation (tensor-network contraction, MPS, full wavefunction) on state-of-the-art supercomputers is the central quantity analysed. Gate 2: Builds a performance/cost model tying effective circuit volume to classical simulation effort and device fidelity - quantum performance modeling. Gate 3: Directly informs when a QPU beats an HPC simulation for a given workload, i.e. the classical-vs-quantum performance frontier.

Major claim as originally recorded: A single effective-circuit-volume framework reproduces measured fidelities and estimates classical simulation cost; BASELINE_UNCLEAR for any quantitative speed comparison.

---

## 7. False-positive log (54 EXCLUDED records)

| Paper | Why search matched | Why excluded |
|---|---|---|
| **FGCS-003** Replay with Feedback: How does the performance of HPC system impact... (`10.1016/j.future.2024.01.024`) | The token 'quantum' appears once in the abstract, in the phrase 'quantum simulations' used as an example of a large-scale scientific workload. | Purely classical HPC job-scheduling / user-behaviour simulation study. No quantum computing content at all - fails the core inclusion condition before Gate 1. |
| **FGCS-004** Quantum annealing-driven branch and bound for the single machine to... (`10.1016/j.future.2024.02.016`) | 'quantum annealing' + 'scheduling' vocabulary. | False-positive class 2/7: quantum annealing applied to an operations-research single-machine scheduling problem. 'Scheduling' here is manufacturing job sequencing, not HPC/QPU resource scheduling. No classical systems mechanism (Gate 2 fails). NO_ABSTRACT. |
| **FGCS-005** Quantum particle swarm optimization algorithm based on diversity mi... (`10.1016/j.future.2024.04.008`) | 'quantum' in 'quantum particle swarm optimization'. | False-positive class 2: quantum-inspired classical metaheuristic. No quantum hardware, no classical systems contribution. NO_ABSTRACT. |
| **FGCS-006** Comparing Adiabatic Quantum Computers for satellite images feature ... (`10.1016/j.future.2024.04.027`) | 'adiabatic quantum computers'. | False-positive class 2/5: annealer-based application study on an image-processing task; the comparison is application accuracy, not systems performance. Gate 2 fails. NO_ABSTRACT. |
| **FGCS-008** SkySwapping: Entanglement resupply by separating quantum swapping a... (`10.1016/j.future.2024.04.031`) | 'quantum swapping', 'entanglement'. | False-positive class 4: quantum networking / entanglement distribution protocol. No computing-systems contribution. NO_ABSTRACT. |
| **FGCS-009** A lattice-based efficient certificateless public key encryption for... (`10.1016/j.future.2024.04.039`) | 'lattice-based' (post-quantum cryptography vocabulary). | False-positive class 1: post-quantum cryptography scheme. NO_ABSTRACT. |
| **FGCS-011** Quantum simulation of dissipation for Maxwell equations in dispersi... (`10.1016/j.future.2024.05.028`) | 'quantum simulation', 'qubit lattice algorithm'. | False-positive class 7: quantum algorithm construction (probabilistic dilation of non-unitary operators) for an electromagnetics problem. Gate 1 fails - no classical systems problem is addressed substantively. |
| **FGCS-012** Quantum Annealing for Computer Vision minimization problems (`10.1016/j.future.2024.05.037`) | 'quantum annealing'. | False-positive class 2: annealer/QUBO application to computer-vision energy minimisation. No classical systems mechanism. NO_ABSTRACT. |
| **FGCS-013** AQUA: Analytics-driven quantum neural network (QNN) user assistance... (`10.1016/j.future.2024.05.047`) | 'quantum neural network'. | False-positive class 5: QNN software-validation tooling. No HPC/systems technique in the contribution (Gate 2 fails). NO_ABSTRACT - classification rests on title plus venue metadata. |
| **FGCS-017** Quantum-empowered federated learning and 6G wireless networks for I... (`10.1016/j.future.2024.06.023`) | 'quantum computing', 'quantum-empowered federated learning'. | False-positive class 5: survey of quantum machine learning / federated learning for IoT security. No HPC or quantum-systems contribution. |
| **FGCS-019** Deciphering the abundance of immune cells in glomerular endothelium... (`10.1016/j.future.2024.07.013`) | Incidental token match in the full record (the quantum vocabulary regex fired on a term in the text/metadata; exact term UNKNOWN). | Biomedical bioinformatics paper with no quantum computing content. Fails the core inclusion condition. NO_ABSTRACT. |
| **FGCS-021** Software stewardship and advancement of a high-performance computin... (`10.1016/j.future.2024.107502`) | 'quantum' in 'quantum Monte Carlo' / QMCPACK. | False-positive class 3: classical quantum Monte Carlo HPC application software-engineering paper. A genuine HPC contribution, but no quantum computing. NO_ABSTRACT. |
| **FGCS-022** Special Collection on Advances in Quantum Computing: Methods, Algor... (`10.1016/j.future.2024.107503`) | Collection title contains 'Quantum Computing'. | Editorial / special-collection introduction. Not an original research contribution; excluded from the included population by article type, but retained and analysed under special_collections. |
| **FGCS-023** Designing optimal Quantum Key Distribution Networks based on Time-D... (`10.1016/j.future.2024.107557`) | 'Quantum Key Distribution'. | False-positive class 4: QKD network design. Multiplexing here is of optical transceivers for key distribution, not of compute resources. NO_ABSTRACT. |
| **FGCS-024** A blockchain-assisted privacy-preserving signature scheme using qua... (`10.1016/j.future.2024.107581`) | 'quantum teleportation'. | False-positive class 4: quantum cryptography / blockchain signature scheme. NO_ABSTRACT. |
| **FGCS-025** Quantum machine learning algorithms for anomaly detection: A review (`10.1016/j.future.2024.107632`) | 'quantum machine learning'. | False-positive class 5: review of QML anomaly-detection algorithms. No systems, runtime or HPC dimension (Gate 1 and Gate 2 fail). Member of Special Collection Vol II. |
| **FGCS-026** Flexible hybrid post-quantum bidirectional multi-factor authenticat... (`10.1016/j.future.2024.107634`) | 'post-quantum', 'KEM'. | False-positive class 1: post-quantum cryptography authentication scheme. NO_ABSTRACT. |
| **FGCS-027** Raising user awareness through unsupervised clustering of energy co... (`10.1016/j.future.2024.107623`) | Incidental token match (exact term UNKNOWN; no quantum vocabulary in the title). | Classical unsupervised clustering of energy-consumption data. No quantum computing content. NO_ABSTRACT. |
| **FGCS-028** Devising an actor-based middleware support to federated learning ex... (`10.1016/j.future.2024.107646`) | Incidental token match (exact term UNKNOWN). | Classical actor-based federated-learning middleware. No quantum computing content. NO_ABSTRACT. |
| **FGCS-029** Generating hard Ising instances with planted solutions using post-q... (`10.1016/j.future.2025.107721`) | 'post-quantum cryptographic', 'Ising'. | False-positive classes 1+2: constructs hard Ising/QUBO benchmark instances via the McEliece protocol. Benchmark-instance construction is not an HPC/systems technique, so Gate 2 fails. Logged as a near-miss because its purpose is benchmarking annealers and classical solvers. Member of Special Collection Vol II. |
| **FGCS-030** Chained continuous quantum federated learning framework (`10.1016/j.future.2025.107800`) | 'quantum federated learning'. | False-positive class 5: QML/federated-learning framework. NO_ABSTRACT. Member of Special Collection Vol II. |
| **FGCS-031** Denoising diffusion models with optimized quantum implicit neural n... (`10.1016/j.future.2025.107875`) | 'quantum implicit neural networks'. | False-positive class 5: QML generative model for images. NO_ABSTRACT. Member of Special Collection Vol II. |
| **FGCS-032** Multi-omic and quantum machine learning integration for lung subtyp... (`10.1016/j.future.2025.107905`) | 'quantum machine learning'. | False-positive class 5: QML applied to a biomedical classification task. NO_ABSTRACT. Member of Special Collection Vol II. |
| **FGCS-035** Exploring the performance of CP2K simulations on the CPU-GPDSP Fusi... (`10.1016/j.future.2025.107912`) | 'quantum' in the quantum-chemistry description of CP2K. | False-positive class 3: classical electronic-structure code (CP2K) ported to a heterogeneous CPU-GPDSP HPC system. A genuine HPC performance paper, but no quantum computing. NO_ABSTRACT. |
| **FGCS-038** Quantum annealing for the two-level facility location problem (`10.1016/j.future.2025.107961`) | 'quantum annealing', 'QUBO'. | False-positive class 2: D-Wave QUBO formulation of a logistics facility-location problem. The network-preprocessing step reduces problem size, not systems cost; Gate 2 fails. Member of Special Collection Vol II. |
| **FGCS-042** Feedback-based quantum strategies for constrained combinatorial opt... (`10.1016/j.future.2025.107979`) | 'quantum optimization', FALQON. | False-positive class 7: extension of a quantum optimisation algorithm to a broader constraint class. No classical systems mechanism (Gate 1 and Gate 2 fail). |
| **FGCS-044** Parameter-efficient Quantum Denoising Diffusion Probabilistic Model... (`10.1016/j.future.2025.107981`) | 'quantum denoising diffusion probabilistic models'. | False-positive class 5: QML generative model. 'Parameter-efficient' refers to circuit parameters, not systems resources. NO_ABSTRACT. Member of Special Collection Vol II. |
| **FGCS-046** Editorial on future generation computer systems (FGCS) special coll... (`10.1016/j.future.2025.107993`) | Collection title contains 'Quantum Computing'. | Editorial / special-collection introduction; excluded from the included population by article type. Retained and analysed under special_collections. |
| **FGCS-047** Distributed machine learning based on quantum cloud with quantum ho... (`10.1016/j.future.2025.108053`) | 'quantum cloud', 'distributed machine learning'. | False-positive classes 4+5: quantum homomorphic-encryption protocol (QCRRA) enabling privacy-preserving quantum federated learning. Communication-overhead reduction is a cryptographic-protocol property, not an HPC systems mechanism; Gate 2 fails. Logged as a near-miss because 'distributed' and 'quantum cloud' are systems vocabulary. |
| **FGCS-048** A performance evaluation framework for post-quantum TLS (`10.1016/j.future.2025.108062`) | 'post-quantum'. | False-positive class 1: performance evaluation of post-quantum TLS handshakes. Genuine performance engineering, but the subject is PQC, not quantum computing systems. NO_ABSTRACT. |
| **FGCS-050** Anomaly-aware quantum convolutional neural network for carbon-effic... (`10.1016/j.future.2025.108096`) | 'quantum convolutional neural network', 'job arrival rate', 'cloud computing'. | False-positive class 5: a QCNN applied to a prediction task. Although the application domain is cloud workload/resource management (POSSIBLE_CROSSOVER), the contribution is a QML model, not a systems technique, so Gate 2 fails. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-051** Intrusion detection with improved quantum neural network: A bigdata... (`10.1016/j.future.2025.108102`) | 'quantum neural network'. | False-positive class 5: QNN intrusion-detection classifier. NO_ABSTRACT. |
| **FGCS-052** The NextGen Quantum-Secure Edge AI-Blockchain System: Enhancing Sup... (`10.1016/j.future.2025.108179`) | 'quantum-secure'. | False-positive classes 1+4: post-quantum/quantum-secure blockchain and edge AI system. NO_ABSTRACT. |
| **FGCS-053** Zero-trust token authorization with trapdoor hashes for scalable di... (`10.1016/j.future.2025.108227`) | Post-quantum / trapdoor cryptography vocabulary. | False-positive class 1: cryptographic authorisation scheme for distributed firewalls. No quantum computing. NO_ABSTRACT. |
| **FGCS-054** Federated reinforcement learning-based adaptive stream applications... (`10.1016/j.future.2025.108235`) | Incidental token match (exact term UNKNOWN; no quantum vocabulary in the title). | Classical edge/cloud scheduling with federated reinforcement learning. No quantum computing content. NO_ABSTRACT. |
| **FGCS-056** SoA-SDA: Quantum-Resistant, Energy-Efficient In-Network Aggregation... (`10.1016/j.future.2025.108321`) | 'quantum-resistant'. | False-positive class 1: post-quantum secure aggregation protocol. NO_ABSTRACT. |
| **FGCS-059** Quantum-resistant blockchain architecture for secure vehicular netw... (`10.1016/j.future.2026.108391`) | 'quantum-resistant', 'ML-KEM'. | False-positive class 1: post-quantum cryptography in a blockchain architecture. NO_ABSTRACT. |
| **FGCS-060** Corrigendum to “Solving combinatorial optimization and machine lear... (`10.1016/j.future.2026.108408`) | Inherits the quantum vocabulary of the corrected article (FGCS-037). | Corrigendum - front-matter class, not a research contribution. Recorded as OTHER and linked to FGCS-037. |
| **FGCS-061** DQVeriChain: Distributed quantum-state-verified and DID-based self-... (`10.1016/j.future.2026.108412`) | 'distributed quantum-state', 'quantum'. | False-positive class 4/5: quantum-state verification used as a blockchain security primitive alongside an LLM application. No computing-systems contribution. NO_ABSTRACT. |
| **FGCS-062** Applying quantum error-correcting codes for fault-tolerant blind qu... (`10.1016/j.future.2026.108451`) | 'quantum error-correcting codes', 'quantum cloud computation'. | False-positive classes 4+7: a blind-quantum-computation delegation protocol hardened with concatenated QEC codes. Per the QEC rule, a new/applied QEC code construction with no classical decoding, parallelisation or systems mechanism is excluded; the resource quantification is of quantum resources only. Logged as a near-miss because 'quantum cloud' and 'resource consumption' are systems-adjacent vocabulary. |
| **FGCS-067** Enhancing adversarial robustness of neural networks via quantum com... (`10.1016/j.future.2026.108542`) | 'quantum computing' applied to neural networks. | False-positive class 5: QML applied to adversarial robustness of classifiers. No systems contribution. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-068** Towards post-quantum secure and practical privacy-preserving top-k ... (`10.1016/j.future.2026.108566`) | 'post-quantum secure'. | False-positive class 1: post-quantum cryptography for private search. NO_ABSTRACT. |
| **FGCS-069** Scalable quantum Trotterised-vs-continuous annealing for pseudo-Boo... (`10.1016/j.future.2026.108568`) | 'quantum annealing', 'scalable'. | False-positive class 2/7: comparison of annealing schedules for a multi-objective optimisation formulation. 'Scalable' refers to problem size, not to a classical systems mechanism; Gate 2 fails. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-070** Quantum message authentication code verifiable by multiple parties ... (`10.1016/j.future.2026.108569`) | 'quantum message authentication'. | False-positive class 4: quantum cryptographic protocol. NO_ABSTRACT. |
| **FGCS-071** Entropic optimal transport with quantum amplitude estimation (`10.1016/j.future.2026.108570`) | 'quantum amplitude estimation'. | False-positive class 7: quantum algorithm applied to an optimal-transport problem. No classical systems mechanism evidenced. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-072** A dynamic access control scheme for cross-border trade data based o... (`10.1016/j.future.2026.108590`) | 'RLWE' (ring learning-with-errors, post-quantum lattice cryptography). | False-positive class 1: lattice-based post-quantum cryptography in a blockchain access-control scheme. NO_ABSTRACT. |
| **FGCS-074** QTIS: A QAOA-based Quantum Time Interval Scheduler (`10.1016/j.future.2026.108594`) | 'scheduler', 'scheduling', 'QAOA'. | False-positive class 7 with a scheduling-vocabulary trap: a QAOA variant with ancilla-assisted overlap detection for a task-scheduling QUBO. The scheduling is generic operations-research scheduling across manufacturing, logistics and healthcare, not HPC job or QPU scheduling, and no classical systems technique is contributed (Gate 2 fails). Member of Special Collection Vol III. |
| **FGCS-075** Entanglement in the trees: Optimal entanglement distribution in bin... (`10.1016/j.future.2026.108597`) | 'entanglement distribution', 'quantum network'. | False-positive class 4: quantum network topology and entanglement routing without a computing-systems contribution. NO_ABSTRACT. |
| **FGCS-076** Quantum Artificial Intelligence for mission-critical systems: Found... (`10.1016/j.future.2026.108602`) | 'Quantum Artificial Intelligence', 'quantum computing', 'architectural elements'. | False-positive class 5: survey of quantum AI/QML for mission-critical domains. Despite 'low-latency' and 'architectural elements' framing, the substance is QML capability review, not a computing-systems contribution. Member of Special Collection Vol III. |
| **FGCS-077** ATIS: Novel applications and techniques in information security and... (`10.1016/j.future.2026.108647`) | Quantum/post-quantum security vocabulary inherited from the collection scope. | Special-issue introduction for an information-security collection. Not an original research contribution, and the topic is security rather than quantum computing systems. NO_ABSTRACT - article type inferred from title form. |
| **FGCS-078** Hybrid quantum Graph Neural Networks for robust botnet detection in... (`10.1016/j.future.2026.108650`) | 'hybrid quantum', 'graph neural networks'. | False-positive class 5: hybrid QML classifier for network intrusion detection. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-081** Generative AI in the age of quantum computing: A taxonomy, architec... (`10.1016/j.future.2026.108714`) | 'quantum computing', 'architectural elements'. | False-positive class 5: taxonomy/survey of generative AI and quantum computing. No HPC or quantum-systems contribution. NO_ABSTRACT. Member of Special Collection Vol III. |
| **FGCS-A01** Performance benchmarking of Tensor Trains for quantum-inspired homo... (`10.1016/j.future.2026.108709`) | 'quantum-inspired' in the title, plus Tensor Train vocabulary that the quantum regex shares with tensor-network simulation. | False-positive class 2 (quantum-inspired classical method) - CONFIRMED. The subject is FFT/SFFT-based computational homogenization of ultra-high-resolution CT microstructure data, accelerated by low-rank Tensor Train representations and benchmarked across TPU, GPU and CPU. There is no quantum computer, no qubit, no QPU and no quantum algorithm anywhere in the contribution; 'quantum-inspired' names a classical numerical-linear-algebra technique. It fails the core inclusion condition before Gate 1, exactly as the coordinator read it. Logged as a high-value near-miss for a different reason: it is a genuine multi-architecture HPC performance-benchmarking paper, so it is the strongest example in this pool of the tensor-train/quantum-inspired numerics false-positive class carrying real systems content that is nonetheless out of scope. |
| **FGCS-A04** Editorial on Future Generation Computer Systems (FGCS) special coll... (`10.1016/j.future.2026.108754`) | Collection title contains 'Quantum Computing'. | Editorial / special-collection introduction; excluded from the included population by article type, on the same basis as FGCS-022 (Vol I) and FGCS-046 (Vol II). Retained and analysed under special_collections. |

### False-positive classes by volume

| Class | Records | Count |
|---|---|---|
| 1. Post-quantum cryptography | FGCS-009, FGCS-026, FGCS-048, FGCS-052, FGCS-053, FGCS-056, FGCS-059, FGCS-068, FGCS-072 | 9 |
| 2. Quantum-inspired / annealing-QUBO classical methods | FGCS-004, FGCS-005, FGCS-006, FGCS-012, FGCS-029, FGCS-038, FGCS-069, FGCS-A01 | 8 |
| 3. Classical quantum chemistry / many-body HPC codes | FGCS-021, FGCS-035 | 2 |
| 4. Quantum networking / QKD / quantum crypto protocols | FGCS-008, FGCS-023, FGCS-024, FGCS-047, FGCS-061, FGCS-062, FGCS-070, FGCS-075 | 8 |
| 5. Quantum machine learning applications and surveys | FGCS-013, FGCS-017, FGCS-025, FGCS-030, FGCS-031, FGCS-032, FGCS-044, FGCS-050, FGCS-051, FGCS-067, FGCS-076, FGCS-078, FGCS-081 | 13 |
| 6. Quantum sensing / metrology / device physics | _none in this pool_ | 0 |
| 7. Quantum algorithms / complexity with no systems mechanism | FGCS-011, FGCS-042, FGCS-071, FGCS-074 | 4 |
| 8. No quantum content at all (incidental token match) | FGCS-003, FGCS-019, FGCS-027, FGCS-028, FGCS-054 | 5 |
| 9. Editorial / special-issue intro / corrigendum (article type) | FGCS-022, FGCS-046, FGCS-060, FGCS-077, FGCS-A04 | 5 |

Class 6 (quantum sensing, metrology and device physics) has **0 records** — a real finding about FGCS's
editorial scope. Class 5 (QML) remains the largest single false-positive class at **13 records**, ahead
of post-quantum cryptography at 9. This inverts the corpus-wide expectation that PQC dominates.

**rev2 note on class 2.** FGCS-A01 (Tensor Trains for quantum-inspired homogenization on TPU/GPU/CPU) is
the most instructive member of the quantum-inspired class: it is a genuine multi-architecture HPC
performance-benchmarking paper with real systems content, and it still fails the core inclusion condition
because there is no quantum computer anywhere in it. The coordinator's reading is confirmed.

### Logged near-misses (excluded, but worth re-reading if the corpus definition widens)

| ID | Why it is a near-miss |
|---|---|
| FGCS-A01 | A real TPU/GPU/CPU performance-benchmarking study; 'quantum-inspired' names a classical low-rank tensor method, so it is out of scope despite strong systems content. |
| FGCS-029 | Its purpose is benchmarking annealers *and* classical solvers; only the absence of a classical systems technique fails Gate 2. |
| FGCS-047 | Reports reduced communication overhead in a distributed quantum-cloud learning setting - systems vocabulary around a cryptographic contribution. |
| FGCS-050 | The target domain is cloud job-arrival prediction, i.e. resource management, but the contribution is a QCNN. POSSIBLE_CROSSOVER. |
| FGCS-062 | 'Quantum cloud computation' plus quantified resource consumption, but the mechanism is a QEC-hardened delegation protocol. |
| FGCS-074 | Title carries 'scheduler'/'scheduling', but the scheduling is operations-research task scheduling solved by QAOA, not HPC/QPU scheduling. A scheduling-vocabulary trap. |
| FGCS-048 | A genuine performance-evaluation framework - but the subject is post-quantum TLS. |
| FGCS-021, FGCS-035 | Genuine HPC performance-engineering papers (QMCPACK, CP2K) in which 'quantum' refers to classical electronic-structure physics. |

---

## 8. Special-collection analysis

FGCS runs a recurring quantum special collection, **Advances in Quantum Computing: Methods, Algorithms,
and Systems**, guest-edited across all three volumes by **Stefano Markidis (KTH)**, **Michela Taufer
(University of Tennessee, Knoxville)** and **Lucio Grandinetti**. Its existence is the single strongest
structural reason to treat FGCS as a standing venue for this corpus.

| | Vol I | Vol II | Vol III |
|---|---|---|---|
| Editorial DOI | `10.1016/j.future.2024.107503` | `10.1016/j.future.2025.107993` | `10.1016/j.future.2026.108754` |
| Dossier record | FGCS-022 | FGCS-046 | **FGCS-A04** (added in rev2) |
| Editorial online-first | 2024-08-30 | 2025-06-25 | 2026-08-04 |
| Volume / cover date | v163 / 2025-02 | v174 / 2026-01 | v186 / 2027-01 |
| Papers | INSUFFICIENT_EVIDENCE | 15 | 24 |
| Papers identifiable in this corpus | 0 | 15 | 10 of 24 |
| Pass gates (of identifiable) | INSUFFICIENT_EVIDENCE | 6 INCLUDED + 2 BORDERLINE of 15 | 1 INCLUDED + 1 BORDERLINE of 10 |

### Vol I

Only the title, venue and guest-editor names were retrievable; the editorial body is behind access control
and two fetch attempts returned metadata only. Collection scope, paper count and membership are
**INSUFFICIENT_EVIDENCE**. No records are assigned to Vol I, and none were inferred.

### Vol II (15 papers, three thematic groups)

Stated scope: work aimed at improving the practicality of quantum computing, particularly for NISQ and
hybrid systems. The gate outcome splits cleanly along the editorial's own thematic groups:

| Editorial thematic group | Papers | INCLUDED | BORDERLINE | EXCLUDED |
|---|---|---|---|---|
| Quantum algorithms, simulation and optimization | FGCS-040, FGCS-036, FGCS-029, FGCS-038, FGCS-034 | 1 (FGCS-036) | 2 (FGCS-040, FGCS-034) | 2 |
| Quantum machine learning and applications | FGCS-031, FGCS-044, FGCS-032, FGCS-025, FGCS-030 | 0 | 0 | **5** |
| Quantum systems, compilation and infrastructure | FGCS-033, FGCS-039, FGCS-041, FGCS-043, FGCS-045 | **5** | 0 | 0 |

The systems/compilation group passes **5 of 5**; the QML group passes **0 of 5**. Membership in the
quantum collection is therefore not by itself evidence of relevance — the gates were applied
independently and a third of the collection failed them.

### Vol III (24 papers; 10 titles recoverable) — now inside the corpus

The Vol III editorial is record **FGCS-A04**, recovered by the extended cover-date sweep; in rev1 it could
only be analysed from outside the dossier. Stated scope: breadth from theoretical methods and
quantum-inspired algorithms to experimental platforms and hybrid quantum-classical workflows, organised
into (a) quantum algorithms, optimization and AI, (b) quantum architectures and HPC systems, (c) quantum
networking, cloud computing and security.

| Identified Vol III member | Verdict |
|---|---|
| FGCS-055 LuGo | **INCLUDED** |
| FGCS-049 hybrid quantum-classical PIC | _BORDERLINE_ |
| FGCS-076, FGCS-074, FGCS-071, FGCS-069, FGCS-067, FGCS-050, FGCS-081, FGCS-078 | excluded (8) |

The remaining 14 titles are **INSUFFICIENT_EVIDENCE**. FGCS-A01, FGCS-A02 and FGCS-A03 sit in the same
volume 186 that carries this editorial, but none appears among the 10 recovered titles, so their
membership is **INSUFFICIENT_EVIDENCE** — as is that of the strongest 2026 systems papers (FGCS-064,
FGCS-065, FGCS-073, FGCS-080). **OPEN_QUESTION.**

### Net observation on the collection

The collection's declared scope is broad (algorithms + ML + systems) and its systems sub-stream is a
minority — roughly a third of Vol II and a smaller share of the identifiable Vol III. It is nonetheless
the mechanism by which FGCS accumulated its compilation and software-stack cluster (FGCS-033, -039, -041,
-043, -045 all arrived together in v174).

---

## 9. Topic shift 2024 -> 2025 -> 2026

### 2024 — position, architecture and integration vision

The 2024 included set is dominated by **statements of intent about HPC-QPU integration rather than
measured systems**. FGCS-018 (ORNL, integrating QC into scientific HPC ecosystems) and FGCS-010
(128-author quantum-centric supercomputing perspective for materials science) set the centre-level frame;
FGCS-007 formalises hybrid quantum-classical scientific workflows and proposes a WMS architecture;
FGCS-002 (QFaaS) delivers the cloud-side serverless abstraction. The measured papers concern classical
simulation and architecture: FGCS-015 parallelises circuit execution by mapping virtual QPUs onto HPC
nodes, and FGCS-014 supplies architectural simulation of ion-trap hardware. Evaluation is largely
qualitative or simulator-based; no included 2024 paper reports scheduling on a production cluster.

_rev2 note: the classical-simulation-cost framing that opened this year (FGCS-001) is now OUT_OF_WINDOW,
which makes the 2024 set purely integration-and-architecture in character._

### 2025 — the compiler and software-stack year

2025 is the year the topic becomes **concrete software artifacts**, and Special Collection Vol II is the
vehicle. Five compilation/infrastructure papers arrive together in v174: FGCS-033 (MLQM, mapping solve
time), FGCS-039 (MPGP-QOC, multi-programming + graph partitioning), FGCS-041 (QHDL, the control-plane
HDL), FGCS-043 (ORNL HPC-quantum convergence stack), FGCS-045 (NetQIR, an IR for distributed multi-QPU
execution). Alongside them, FGCS-036 benchmarks GPU state-vector versus tensor-network simulation on an
A100, and at the end of the year FGCS-057 spends 8,192 cores on exact qubit allocation. The centre of
gravity moves from *should we integrate* to *what does the stack look like and what does compilation cost*.

### 2026 — measured hardware, sharing, exascale simulation, and full-scale coupling

2026 delivers the **measurement**, and rev2 strengthens this year considerably. FGCS-073 (JUQCS-50) runs a
50-qubit state-vector simulation on JUPITER's GH200 superchips for a 16.6x speedup over the 48-qubit K
computer record. FGCS-080 compares three QPU-sharing scheduling strategies on production HPC clusters
against real quantum hardware (45.7% and 64% classical-resource reductions). FGCS-064 (HiMA) measures
multi-process QPU sharing on a deployed 102-qubit cloud processor. **FGCS-A02 couples an on-premises IBM
Heron processor to the entire Fugaku supercomputer — 152,064 nodes — in a closed-loop electronic-structure
workflow**, which is the largest HPC-QPU orchestration measurement in this corpus. **FGCS-A03**
(DistributedEstimator) instruments circuit cutting as a staged distributed workload and finds classical
reconstruction, not quantum execution, dominates per-query time. FGCS-079 puts a hybrid annealer solver
inside a real WfCommons workflow-scheduling pipeline and reports its 17.5% quality cost honestly;
FGCS-065 offers an analytic alternative to FGCS-057's exact mapping; FGCS-066 (ADAC, 22 authors) restates
the centre-level perspective two years after FGCS-010.

### Summary of the shift

| | 2024 | 2025 | 2026 |
|---|---|---|---|
| Dominant mode | position / architecture | software artifacts, compilers | measured systems on real hardware |
| Typical evaluation | qualitative, simulator | benchmark suites, single-node GPU | exascale machine, production cluster, deployed QPU, full-machine closed loop |
| Representative records | FGCS-018, -010, -007, -002, -015 | FGCS-043, -045, -041, -033, -039, -036, -057 | FGCS-A02, -073, -080, -064, -A03, -079, -065, -066 |
| Scheduling / sharing content | absent | multi-programming (FGCS-039) only | explicit and measured (FGCS-080, -064) |
| Real QPU + real supercomputer | absent | absent | FGCS-A02 (Heron + full Fugaku), FGCS-080 (production clusters + real QPUs) |
| Included original research | 5 | 8 | 7 |

The trajectory is consistent: **vision (2024) -> stack (2025) -> measurement (2026)**, and the 2026
measurement tier now reaches full-machine scale. The background false-positive load shifts too — PQC is
steady throughout, while QML grows from 4 records in 2024 to 6 in 2025 and 5 in 2026 and becomes the
largest single false-positive class overall.

---

## 10. Topic-coverage checklist

| Topic | Present in FGCS 2024-2026? | Evidence |
|---|---|---|
| HPC-QPU integration | **Yes, strong** | FGCS-A02 (Heron + full Fugaku), FGCS-018 (ORNL ecosystems), FGCS-043 (stack + gateway), FGCS-010 / FGCS-066 (centre perspectives), FGCS-080 |
| Quantum workflow | **Yes** | FGCS-A02 (closed-loop workflow at full machine scale), FGCS-007 (formalisation + WMS architecture), FGCS-079 (SPWD on WfCommons workflows), FGCS-080 |
| Scheduling | **Yes** | FGCS-080 (three strategies, measured), FGCS-043 (scheduling APIs), FGCS-064 (multiprocessing scheduling in the control plane), FGCS-079 (workflow scheduling) |
| QPU sharing | **Yes** | FGCS-080 (time multiplexing / malleability / decomposition), FGCS-064 (hardware-level asynchronous multi-user processes), FGCS-039 (multi-programming) |
| Resource allocation | **Yes** | FGCS-A02 (orchestration across 152,064 nodes), FGCS-043 (resource-management APIs), FGCS-080 (dynamic resource management), FGCS-018. Note: 'qubit allocation' in FGCS-057 is compilation, a different sense. |
| Virtualization | **Yes, one record** | FGCS-015 (virtual QPU array mapped onto HPC nodes in XACC) |
| MPI / distributed execution | **Yes** | FGCS-A03 (staged distributed circuit-cutting workload with straggler analysis), FGCS-057 (64 nodes / 8,192 cores, Chapel/PGAS), FGCS-073 (distributed state vector + network-traffic optimizer), FGCS-045 (NetQIR inter-QPU communication IR). Explicit MPI usage: INSUFFICIENT_EVIDENCE. |
| Runtime / orchestration | **Yes** | FGCS-A02, FGCS-002 (serverless runtime), FGCS-043 (Quantum Platform Manager), FGCS-041 (control-plane timing), FGCS-080 |
| Scientific application coupling | **Yes** | FGCS-A02 (electronic structure at full scale), FGCS-049 (PIC plasma), FGCS-055 (HHL + Hele-Shaw flow), FGCS-040 (lattice Boltzmann CFD), FGCS-010, FGCS-007 |
| Real QPU + supercomputer workflows | **Yes — upgraded in rev2** | **FGCS-A02 is the decisive record**: an on-premises Heron processor closed-loop-coupled to the entire Fugaku machine. FGCS-080 adds production clusters with real quantum hardware; FGCS-064 uses a real 102-qubit processor on a quantum cloud; FGCS-037 couples a photonic QPU to GPUs. In rev1 this row read 'thin'; it no longer does. |
| Circuit cutting / reconstruction cost | **Yes — new in rev2** | FGCS-A03 measures reconstruction as the dominant per-query cost (median 53%) with O(9^c) subexperiment growth. FGCS-040 (multi-circuit QLBM) is a BORDERLINE relative. |

### Topics UNDERREPRESENTED_IN_THIS_CORPUS (FGCS 2024-2026)

| Topic | Records | Note |
|---|---|---|
| QEC classical processing (decoders, syndrome bandwidth, real-time decoding) | **0** | A clear JOURNAL_GAP, unchanged by rev2. No parallel decoder, GPU/FPGA/ASIC decoder, decoder scheduling or syndrome-compression paper appears anywhere in the 85-record pool. The only QEC-adjacent record, FGCS-062, is a blind-computation protocol. |
| Decision-diagram simulation | **0** | Only state-vector and tensor-network simulation appear (FGCS-036, FGCS-073). |
| Multi-QPU *execution* results | **0 measured** | FGCS-045 specifies the IR; FGCS-A03 distributes subcircuits of one cut circuit rather than across multiple QPUs. No record reports a measured multi-QPU run. |
| Shot/measurement orchestration as a stated subject | **0 direct** | Implied by FGCS-015, FGCS-040 and FGCS-A03, never the stated contribution. |

_Removed from this list in rev2: circuit cutting and reconstruction cost, now directly covered by FGCS-A03._

---

## 11. Artifact table

| ID | Paper | Verdict | Artifact status | URL / note |
|---|---|---|---|---|
| FGCS-002 | QFaaS: A Serverless Function-as-a-Service framewo... | INCLUDED | PUBLIC_CODE | https://github.com/Cloudslab/qfaas |
| FGCS-007 | Paving the way to hybrid quantum–classical scient... | INCLUDED | UNKNOWN | — |
| FGCS-010 | Quantum-centric supercomputing for materials scie... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-014 | Performance of algorithms for emerging ion-trap q... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-015 | Parallel quantum computing simulations via quantu... | INCLUDED | UNKNOWN | — |
| FGCS-018 | Integrating quantum computing resources into scie... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-033 | MLQM: Machine learning approach for accelerating ... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-036 | State of practice: Evaluating GPU performance of ... | INCLUDED | PARTIAL | The paper cites a code/execution-time repository and an interactive plot, but no URL was recoverable from the retrieved text. |
| FGCS-039 | MPGP-QOC: Multi-programming and graph-partition-b... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-041 | Tightly-integrated quantum–classical computing us... | INCLUDED | UNKNOWN | — |
| FGCS-043 | Bridging paradigms: Designing for HPC-Quantum con... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-045 | NetQIR: An extension of QIR for distributed quant... | INCLUDED | UNKNOWN | — |
| FGCS-055 | LuGo: An enhanced quantum phase estimation implem... | INCLUDED | PARTIAL | Stated that the code is available for academic or commercial use on request through ORNL; no open repository URL given. |
| FGCS-057 | Efficient and scalable branch-and-bound algorithm... | INCLUDED | PUBLIC_CODE | https://github.com/Guillaume-Helbecque/P3D-DFS |
| FGCS-064 | HiMA: Hierarchical quantum microarchitecture for ... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-065 | GraMA: A gradient matrix-guided assignment method... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-066 | The role of quantum computing in advancing scient... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-073 | Universal quantum computer simulation of 50 qubit... | INCLUDED | UNKNOWN | — |
| FGCS-079 | Workflow decomposition algorithm for scheduling w... | INCLUDED | UNKNOWN | The paper states that the SPWD Python source and the experimental results are held in GitHub repositories, but no URL was recoverable from the ScienceDirect abstract page or from the arXiv preprint (2506.01567), so the artifact could not be verified. Downgraded from PUBLIC_CODE to UNKNOWN rather than asserting an unverified URL. |
| FGCS-080 | Three ways to share a QPU: Scheduling strategies ... | INCLUDED | UNKNOWN | — |
| FGCS-A02 | Closed-loop calculations of electronic structure ... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | No code or data availability statement in the arXiv abstract page or the retrieved metadata. |
| FGCS-A03 | DistributedEstimator: Distributed training of qua... | INCLUDED | NO_PUBLIC_ARTIFACT_FOUND | No availability statement found. The work builds on open-source components (qiskit-addon-cutting, qiskit-machine-learning, PyTorch), but those are dependencies, not this paper's artifact. |
| FGCS-016 | Assessing and advancing the potential of quantum ... | BORDERLINE | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-020 | Quantum resource estimation for large scale quant... | BORDERLINE | UNKNOWN | — |
| FGCS-034 | Is quantum optimization ready? An effort towards ... | BORDERLINE | UNKNOWN | — |
| FGCS-037 | Solving combinatorial optimization and machine le... | BORDERLINE | NO_PUBLIC_ARTIFACT_FOUND | — |
| FGCS-040 | A multiple-circuit approach to quantum resource r... | BORDERLINE | UNKNOWN | — |
| FGCS-049 | A hybrid quantum-classical particle-in-cell metho... | BORDERLINE | UNKNOWN | — |
| FGCS-058 | Cost-efficient quantum cloud task offloading with... | BORDERLINE | UNKNOWN | — |
| FGCS-063 | Addressing the minor-embedding problem in quantum... | BORDERLINE | NO_PUBLIC_ARTIFACT_FOUND | — |

**Artifact availability is poor, and rev2 makes it slightly worse.** Of 22 INCLUDED papers, only **2**
carry a confirmed public repository — FGCS-002 (QFaaS, github.com/Cloudslab/qfaas) and FGCS-057 (exact
qubit allocation, github.com/Guillaume-Helbecque/P3D-DFS). Two are PARTIAL (FGCS-036 cites a repository
without a retrievable URL; FGCS-055 offers code on request through ORNL). FGCS-079 was downgraded from
PUBLIC_CODE to **UNKNOWN** in rev2 because the stated GitHub repositories could not be located from either
the abstract page or the arXiv preprint — an unverified URL is not recorded. None of the flagship systems
papers — FGCS-A02 (Fugaku closed loop), FGCS-073 (JUQCS-50), FGCS-080 (QPU sharing), FGCS-064 (HiMA),
FGCS-043 (ORNL stack) — has a public artifact identified. For reproducibility this remains the weakest
dimension of the FGCS quantum-HPC output.

---

## 12. Deep-dive priority ranking

| Priority | Records |
|---|---|
| 5 / 5 | FGCS-010, FGCS-018, FGCS-043, FGCS-057, FGCS-064, FGCS-073, FGCS-080, FGCS-A02 |
| 4 / 5 | FGCS-002, FGCS-007, FGCS-015, FGCS-036, FGCS-039, FGCS-041, FGCS-045, FGCS-065, FGCS-066, FGCS-079, FGCS-A03 |
| 3 / 5 | FGCS-014, FGCS-033, FGCS-055, FGCS-037, FGCS-040, FGCS-049, FGCS-063 |
| 2 / 5 | FGCS-016, FGCS-020, FGCS-034, FGCS-058 |

The priority-5 set — **FGCS-A02** (Heron + full Fugaku closed loop), **FGCS-080** (QPU sharing measured
three ways), **FGCS-073** (50 qubits on JUPITER), **FGCS-064** (HiMA control microarchitecture),
**FGCS-057** (parallel exact qubit allocation), **FGCS-043** (ORNL HPC-quantum stack), **FGCS-018** (ORNL
HPC ecosystem integration) and **FGCS-010** (quantum-centric supercomputing perspective) — is where FGCS
carries material this corpus cannot get elsewhere in the same form.

---

## 13. Census-policy judgement: **CORE_CENSUS**

FGCS should be treated as a **CORE_CENSUS** venue and swept in full every year. The rev2 evidence
strengthens rather than weakens the rev1 judgement. Yield: 22 of 84 in-window candidates pass all three
gates (20 original research plus 2 perspectives), with 8 more BORDERLINE — about 26% precision on the
candidate pool and a steady 5 / 8 / 7 included original-research count across 2024 / 2025 / 2026, so this
is not a one-year spike. Distinctiveness: FGCS carries material hard to source elsewhere in this shape —
the largest HPC-QPU closed-loop orchestration measurement anywhere in this corpus (FGCS-A02, an
on-premises Heron processor driving 152,064 Fugaku nodes), the exascale simulation record (FGCS-073), the
only measured QPU-sharing scheduling comparison on production clusters with real hardware (FGCS-080), a
deployed control microarchitecture with multi-process sharing (FGCS-064), a stage-level cost breakdown of
circuit cutting (FGCS-A03), two national-lab software-stack specifications (FGCS-018, FGCS-043), and the
two most citable centre-level perspectives in the window (FGCS-010, FGCS-066). Structure: the standing
guest-edited quantum special collection, now in its third volume under the same three editors, gives the
venue a durable intake channel for exactly the systems/compilation sub-stream this corpus wants, and Vol
II's systems group passing 5 of 5 gates shows the channel works. Three operational cautions follow from
rev2 rather than changing the verdict. **Sweep on online-first, not cover date** — the six-month FGCS
offset cost four records at the recent end and wrongly admitted one at the old end, and any future sweep
must run to cover-date +1 year and filter back. The majority of the pool remains false positives
concentrated in quantum machine learning (13) and post-quantum cryptography (9), so the vocabulary filter
must stay aggressive on both. Artifact availability is poor, and QEC classical processing is entirely
absent, so FGCS cannot serve as the corpus's source for decoder-acceleration work. FGCS is additionally a
strong **BIBLIOGRAPHY_HUB** venue through FGCS-010 and FGCS-066.

---

## Appendix A — record index

| ID | DOI | Verdict |
|---|---|---|
| FGCS-001 | `10.1016/j.future.2023.12.002` | OUT_OF_WINDOW |
| FGCS-002 | `10.1016/j.future.2024.01.018` | INCLUDED |
| FGCS-003 | `10.1016/j.future.2024.01.024` | EXCLUDED |
| FGCS-004 | `10.1016/j.future.2024.02.016` | EXCLUDED |
| FGCS-005 | `10.1016/j.future.2024.04.008` | EXCLUDED |
| FGCS-006 | `10.1016/j.future.2024.04.027` | EXCLUDED |
| FGCS-007 | `10.1016/j.future.2024.04.030` | INCLUDED |
| FGCS-008 | `10.1016/j.future.2024.04.031` | EXCLUDED |
| FGCS-009 | `10.1016/j.future.2024.04.039` | EXCLUDED |
| FGCS-010 | `10.1016/j.future.2024.04.060` | INCLUDED |
| FGCS-011 | `10.1016/j.future.2024.05.028` | EXCLUDED |
| FGCS-012 | `10.1016/j.future.2024.05.037` | EXCLUDED |
| FGCS-013 | `10.1016/j.future.2024.05.047` | EXCLUDED |
| FGCS-014 | `10.1016/j.future.2024.06.005` | INCLUDED |
| FGCS-015 | `10.1016/j.future.2024.06.007` | INCLUDED |
| FGCS-016 | `10.1016/j.future.2024.06.012` | BORDERLINE |
| FGCS-017 | `10.1016/j.future.2024.06.023` | EXCLUDED |
| FGCS-018 | `10.1016/j.future.2024.06.058` | INCLUDED |
| FGCS-019 | `10.1016/j.future.2024.07.013` | EXCLUDED |
| FGCS-020 | `10.1016/j.future.2024.107480` | BORDERLINE |
| FGCS-021 | `10.1016/j.future.2024.107502` | EXCLUDED |
| FGCS-022 | `10.1016/j.future.2024.107503` | EXCLUDED |
| FGCS-023 | `10.1016/j.future.2024.107557` | EXCLUDED |
| FGCS-024 | `10.1016/j.future.2024.107581` | EXCLUDED |
| FGCS-025 | `10.1016/j.future.2024.107632` | EXCLUDED |
| FGCS-026 | `10.1016/j.future.2024.107634` | EXCLUDED |
| FGCS-027 | `10.1016/j.future.2024.107623` | EXCLUDED |
| FGCS-028 | `10.1016/j.future.2024.107646` | EXCLUDED |
| FGCS-029 | `10.1016/j.future.2025.107721` | EXCLUDED |
| FGCS-030 | `10.1016/j.future.2025.107800` | EXCLUDED |
| FGCS-031 | `10.1016/j.future.2025.107875` | EXCLUDED |
| FGCS-032 | `10.1016/j.future.2025.107905` | EXCLUDED |
| FGCS-033 | `10.1016/j.future.2025.107906` | INCLUDED |
| FGCS-034 | `10.1016/j.future.2025.107908` | BORDERLINE |
| FGCS-035 | `10.1016/j.future.2025.107912` | EXCLUDED |
| FGCS-036 | `10.1016/j.future.2025.107927` | INCLUDED |
| FGCS-037 | `10.1016/j.future.2025.107934` | BORDERLINE |
| FGCS-038 | `10.1016/j.future.2025.107961` | EXCLUDED |
| FGCS-039 | `10.1016/j.future.2025.107966` | INCLUDED |
| FGCS-040 | `10.1016/j.future.2025.107975` | BORDERLINE |
| FGCS-041 | `10.1016/j.future.2025.107977` | INCLUDED |
| FGCS-042 | `10.1016/j.future.2025.107979` | EXCLUDED |
| FGCS-043 | `10.1016/j.future.2025.107980` | INCLUDED |
| FGCS-044 | `10.1016/j.future.2025.107981` | EXCLUDED |
| FGCS-045 | `10.1016/j.future.2025.107989` | INCLUDED |
| FGCS-046 | `10.1016/j.future.2025.107993` | EXCLUDED |
| FGCS-047 | `10.1016/j.future.2025.108053` | EXCLUDED |
| FGCS-048 | `10.1016/j.future.2025.108062` | EXCLUDED |
| FGCS-049 | `10.1016/j.future.2025.108087` | BORDERLINE |
| FGCS-050 | `10.1016/j.future.2025.108096` | EXCLUDED |
| FGCS-051 | `10.1016/j.future.2025.108102` | EXCLUDED |
| FGCS-052 | `10.1016/j.future.2025.108179` | EXCLUDED |
| FGCS-053 | `10.1016/j.future.2025.108227` | EXCLUDED |
| FGCS-054 | `10.1016/j.future.2025.108235` | EXCLUDED |
| FGCS-055 | `10.1016/j.future.2025.108270` | INCLUDED |
| FGCS-056 | `10.1016/j.future.2025.108321` | EXCLUDED |
| FGCS-057 | `10.1016/j.future.2025.108342` | INCLUDED |
| FGCS-058 | `10.1016/j.future.2025.108095` | BORDERLINE |
| FGCS-059 | `10.1016/j.future.2026.108391` | EXCLUDED |
| FGCS-060 | `10.1016/j.future.2026.108408` | EXCLUDED |
| FGCS-061 | `10.1016/j.future.2026.108412` | EXCLUDED |
| FGCS-062 | `10.1016/j.future.2026.108451` | EXCLUDED |
| FGCS-063 | `10.1016/j.future.2026.108481` | BORDERLINE |
| FGCS-064 | `10.1016/j.future.2026.108484` | INCLUDED |
| FGCS-065 | `10.1016/j.future.2026.108485` | INCLUDED |
| FGCS-066 | `10.1016/j.future.2026.108487` | INCLUDED |
| FGCS-067 | `10.1016/j.future.2026.108542` | EXCLUDED |
| FGCS-068 | `10.1016/j.future.2026.108566` | EXCLUDED |
| FGCS-069 | `10.1016/j.future.2026.108568` | EXCLUDED |
| FGCS-070 | `10.1016/j.future.2026.108569` | EXCLUDED |
| FGCS-071 | `10.1016/j.future.2026.108570` | EXCLUDED |
| FGCS-072 | `10.1016/j.future.2026.108590` | EXCLUDED |
| FGCS-073 | `10.1016/j.future.2026.108592` | INCLUDED |
| FGCS-074 | `10.1016/j.future.2026.108594` | EXCLUDED |
| FGCS-075 | `10.1016/j.future.2026.108597` | EXCLUDED |
| FGCS-076 | `10.1016/j.future.2026.108602` | EXCLUDED |
| FGCS-077 | `10.1016/j.future.2026.108647` | EXCLUDED |
| FGCS-078 | `10.1016/j.future.2026.108650` | EXCLUDED |
| FGCS-079 | `10.1016/j.future.2026.108686` | INCLUDED |
| FGCS-080 | `10.1016/j.future.2026.108699` | INCLUDED |
| FGCS-081 | `10.1016/j.future.2026.108714` | EXCLUDED |
| FGCS-A01 | `10.1016/j.future.2026.108709` | EXCLUDED |
| FGCS-A02 | `10.1016/j.future.2026.108731` | INCLUDED |
| FGCS-A03 | `10.1016/j.future.2026.108746` | INCLUDED |
| FGCS-A04 | `10.1016/j.future.2026.108754` | EXCLUDED |

## Appendix B — rev2 change log

| Change | Detail |
|---|---|
| Window correction | FGCS-001 (`10.1016/j.future.2023.12.002`) reclassified **OUT_OF_WINDOW**; first availability 2023-12-04. Removed from INCLUDED and from the 2024 counts; assessment retained for audit. |
| Recall recovery | Sweep extended to cover-date 2027-12-31, re-filtered to first-availability <= 2026-09-17. Four records added: FGCS-A01 (EXCLUDED), FGCS-A02 (INCLUDED), FGCS-A03 (INCLUDED), FGCS-A04 (EXCLUDED, editorial). |
| FGCS-079 artifact | PUBLIC_CODE with a literal 'UNKNOWN' URL resolved to **artifact_status UNKNOWN**; repositories are stated in the paper but no URL was recoverable from the abstract page or arXiv 2506.01567. arXiv id 2506.01567 added. |
| arXiv ids added | FGCS-055 -> 2503.15439 (verified: title and all three ORNL authors match). FGCS-064 -> 2408.11311 (content-matched to the HiMA microarchitecture; title/author strings not extractable from the fetched page). |
| Conference lineage | FGCS-002, FGCS-057 and FGCS-073 downgraded from RELATED_LINEAGE to **UNKNOWN** — a preprint, a software-skeleton project and a prior journal article respectively do not meet the conference-predecessor evidence bar. The lineage evidence is preserved in a `prior_work_note` field rather than discarded. |
| Vol III collection | Editorial is now record FGCS-A04, inside the corpus; special_collections updated accordingly. |

---

## Note on vocabulary

The words `novel` and `first` appear in this document only inside verbatim paper titles that must be
reproduced exactly for DOI/title fidelity (FGCS-077 "ATIS: Novel applications..."; FGCS-073 "...Europe's
first exascale supercomputer...") and in the structural labels `first author`, `online-first`,
`first public availability` and `first-availability`. No assessment in this census is stated in those
terms; the census uses VENUE_GAP, JOURNAL_GAP, UNDERREPRESENTED_IN_THIS_CORPUS, POSSIBLE_CROSSOVER,
OPEN_QUESTION and INSUFFICIENT_EVIDENCE instead.

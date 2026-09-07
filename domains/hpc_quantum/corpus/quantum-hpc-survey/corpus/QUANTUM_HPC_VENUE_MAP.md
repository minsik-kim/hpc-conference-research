# Quantum-HPC Research Venue Map

**Phase 1 — Research Venue Mapping**
**Survey date: 2026-09-06 (KST)**
**Scope: main-conference regular/full research papers only, 2024–2026**

---

## 0. How to read this document

Every factual claim carries an evidence tag:

| Tag | Meaning |
|---|---|
| `[official-CFP]` | Verified against the conference's own Call for Papers page |
| `[official-program]` | Verified against the official technical program / accepted-papers list |
| `[proceedings]` | Verified against the publisher volume (ACM DL, IEEE Xplore, Springer LNCS, Crossref container metadata) |
| `[paper]` | Verified by reading the paper record itself |
| `[inference]` | My reasoning on top of the above — explicitly not a verified fact |

Publication status vocabulary: `PUBLISHED_REGULAR_PAPER`, `ACCEPTED_FORTHCOMING`, `PREPRINT`, `PROGRAM_LISTED`, `STATUS_UNCLEAR`.
Artifact vocabulary: `PUBLIC_CODE`, `PUBLIC_ARTIFACT`, `PARTIAL`, `NO_PUBLIC_ARTIFACT_FOUND`, `UNKNOWN`.

> **`NO_PUBLIC_ARTIFACT_FOUND` never means "no code exists."** It means an official public repository was searched for and not located. `UNKNOWN` means not searched. In this survey, artifact status is `UNKNOWN` for the large majority of papers — the artifact pass was deliberately shallow at this phase.

---

## 1. Mission and scope

### 1.1 What this survey is for

The five-year working hypothesis is that QPUs will not be used standalone but will attach to CPU/GPU HPC infrastructure as heterogeneous accelerators or workflow components:

```
CPU/GPU HPC system  ↕  Quantum Processing Unit (QPU)
```

This document answers: **which conference communities are actually producing regular research papers at that interface, and which ones should be tracked to find SC-publishable research problems.**

This is a *venue* map, not a paper analysis. Representative paper titles appear only as evidence that a venue publishes this class of work.

### 1.2 Three scenario tags used throughout

| Tag | Definition | Typical topics |
|---|---|---|
| `HPC_FOR_Q` | Classical HPC enables or supports quantum computing | distributed/GPU statevector & tensor-network simulation, stabilizer/sparse/decision-diagram simulation, quantum compilation & mapping, QEC decoding with system contribution, circuit-cutting reconstruction, classical optimization for hybrid loops, measurement postprocessing |
| `Q_IN_HPC` | QPU enters a heterogeneous HPC system alongside CPU/GPU | CPU/GPU/QPU runtimes, hybrid execution models, task/DAG runtimes, scheduling, co-scheduling, QPU multiplexing, multi-QPU execution, resource management, workflow orchestration, programming models, performance modeling |
| `Q_FOR_HPC` / `FUTURE_WORKLOAD` | Quantum algorithms that may absorb part of a scientific/HPC workload, or whose execution pattern strongly shapes HPC integration | chemistry, materials, optimization, linear algebra, Monte Carlo, PDE, QML — judged on circuit count, shot count, depth, parallelism, classical pre/post-processing, CPU-QPU sync, memory/communication |

### 1.3 Inclusion criteria

A paper is in scope if it is a **main-conference regular/full research paper** AND falls in one of:

- HPC/parallel algorithm for a quantum workload
- GPU / multi-GPU / distributed quantum simulation
- quantum-aware runtime, QPU scheduling or resource management
- heterogeneous CPU/GPU/QPU execution
- distributed quantum algorithm; circuit cutting/partitioning with systems implications
- quantum compilation with substantial performance or system contribution
- quantum architecture relevant to scalable computation
- workload characterization, performance modeling, benchmarking
- QEC decoding with architecture / performance / system contribution
- future scientific quantum workload whose execution pattern strongly affects HPC integration

**Execution on a real supercomputer is not required.** Workstation- or simulator-evaluated work is included when algorithmic parallelism, future QPU/HPC integration relevance, architecture/runtime/compiler implication, or a natural path to distributed scaling is clear. Conversely, running on a large machine is not by itself a reason to include.

### 1.4 Exclusion criteria

**Structurally excluded — never counted as evidence anywhere in this document:**
workshop papers and workshop proceedings, posters, demos, extended abstracts, short papers where the venue treats them as a lesser category, tutorials, panels, keynotes, industry/vendor presentations, doctoral symposia, competition results, invited re-presentation tracks (e.g. HPCA "Best of CAL"), journal-first presentation slots (e.g. PLDI `[TOPLAS]` entries).

**Topically excluded:**
pure quantum device physics; materials/device fabrication only; pure quantum information theory with no systems/HPC implication; chemistry-accuracy improvement alone; a new VQE ansatz alone; a new optimizer alone; pure mathematical speedup claims with no computational/system implication; pure QEC theory with no decoding/system/architecture implication.

**Three recurring false-positive classes** that must be filtered at every venue — each was caught multiple times during this survey:

1. **Post-quantum cryptography.** PQC papers use the word "quantum" and are not quantum computing. Found at CCGrid 2025 & 2026, PACT 2025, HiPCW 2025. `[proceedings]`
2. **Classical quantum chemistry / many-body simulation.** Papers titled "quantum many-body", "quantum transport", "quantum materials", "neural network quantum states" are classical HPC. Found at SC24 (Gordon Bell), SC25 (five papers, three of them inside the pp. 1–136 Gordon Bell block), ICPP 2024, ICS 2026, Euro-Par 2026, HPDC 2026. `[proceedings]`
3. **"Quantum-inspired" classical methods.** Vector/Ising annealing, QUBO solvers on classical hardware. Found at ISC 2025, HiPC 2025, and ISCA 2026 (SATIC, an Ising compiler sitting inside a quantum session). `[official-program]`

---

## 2. Executive summary

### 2.1 The one-paragraph answer

Quantum-HPC regular-paper research is **not** concentrated in the HPC community. It is concentrated in the **computer architecture community** (ASPLOS, ISCA, MICRO, HPCA — roughly 92 main-track quantum papers across 11 completed venue-years in 2024–2026) and in the **SIGPLAN compiler/PL community** (CGO, PLDI, OOPSLA — ~38 papers). The classical HPC venues (SC, ISC, IPDPS, ICS, ICPP) produce a much thinner but rapidly growing stream of roughly 33–37 papers across 15 venue-years, and they are the only venues where the *`Q_IN_HPC` integration* branch — QPU-as-HPC-resource, telemetry, topology models, HPC-centre operations, orchestration — actually appears. IEEE QCE is the largest single reservoir of Quantum-HPC systems work by raw count but is materially less selective, and its most HPC-specific content sits in a **workshop** (WIHPQC) that is out of scope by definition. Two systems venues have broken through decisively and were not on the original candidate list's radar as likely hits: **OSDI** (quantum operating systems and virtualization) and **SIGMETRICS** (quantum performance measurement and exascale simulation).

### 2.2 Where each research branch actually lives

This is the most actionable finding in the survey. **Contribution shape, not quantum-ness, determines venue.**

| Research branch | Where it is actually published |
|---|---|
| Distributed / GPU / multi-GPU statevector & tensor-network simulation | **SC, ICS, ASPLOS, SIGMETRICS, OOPSLA**, HPEC, QCE-QSYS |
| QEC decoding with throughput/architecture contribution | **ISCA, MICRO, HPCA, ASPLOS**, EuroSys, IISWC, ICCAD, DAC |
| Quantum compilation / mapping / routing at scale | **CGO, ISCA, HPCA, ASPLOS, DAC, DATE, ICCAD**, ICS, PLDI |
| QPU scheduling, resource management, multiplexing, quantum OS | **OSDI**, SC (Qonductor), IPDPS (AQUA), CCGrid, ICPP, ICDCS, QCE-QSYS |
| Hybrid CPU/GPU/QPU runtime & workflow orchestration | **CCGrid, OSDI, Euro-Par, ISC**, PLDI (QVM), QCE-QSYS |
| HPC-centre QPU integration & operations (telemetry, topology, calibration) | **ISC** — essentially unique to ISC, driven by LRZ/TUM |
| Performance modeling, benchmarking, workload characterization, variability | **SIGMETRICS, IISWC**, ISC, QCE-QSYS |
| Multi-QPU / distributed quantum architecture | **ISCA, ASPLOS, HPCA**, ICDCS, ICPP, QCE-QNET |
| Quantum PL / type systems / verification | POPL, PLDI, OOPSLA — **largely out of scope for HPC systems work** |

### 2.3 Nine findings that change how the candidate list should be used

**F1 — CFP scope is a weak predictor of yield; it is neither necessary nor sufficient.**
Sufficiency fails: **CC** explicitly solicits quantum compiler work in *two separate CFP bullets* and has accepted **zero** papers in 2024, 2025, and 2026 `[official-CFP]` `[official-program]`. **PPoPP** names quantum computers in its scope statement and accepted zero across 121 main-track papers. **HPDC** carries a standing post-Moore quantum bullet and accepted zero across ~91 papers. Necessity fails: **ASPLOS** has never used the word "quantum" in any CFP (2024, 2025, 2026 checked) `[official-CFP]` yet has the highest quantum share of any venue-year in the survey (7.9%, ASPLOS 2026). PLDI, POPL and OOPSLA have no quantum CFP language and accepted ~45 quantum papers between them.
**Consequence: always verify against the main technical program, never the CFP alone.**

**F2 — The architecture community, not the HPC community, is the volume centre.**
ASPLOS ran dedicated quantum sessions in all three years (2/2/3); ISCA went 1→3→3 sessions; MICRO 1→2; HPCA 0→2→2. Absolute counts: ASPLOS 9/10/12, ISCA 6/16/12, MICRO 3/8/—, HPCA 1/7/8. `[official-program]` `[proceedings]`
> ⚠ **PHASE 3 CORRECTION (2026-09-06).** The ASPLOS figure **9/10/12 is a program-based count and is an undercount for 2024**. A full volume sweep finds **14/10/12** presented. See the correction block under *ASPLOS — March/April* in §4, and `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`. The counts for ISCA, MICRO and HPCA in this map were produced by the same program-based method and **have not been re-verified**; treat them as lower bounds until their own censuses run.

**F3 — But the 2024 baseline was much weaker than the field's reputation suggests.**
HPCA 2024 had **no dedicated quantum session** and only **one** main-track regular quantum paper in a 75-paper program (its apparent second paper is a "Best of CAL" invited re-presentation, not a main-track paper). MICRO 2024 had 3 in 113 (2.7%). ISCA 2024's six quantum papers were essentially all single-QPU NISQ circuit compilation — nothing an HPC systems researcher could build on. **The phenomenon is real from 2025 onward, not from 2024.** `[official-program]`

**F4 — The architecture venues pivoted from NISQ compilation to fault-tolerant systems, and that pivot moves toward HPC.**
2024 was dominated by NISQ circuit compilation and error mitigation. 2025–2026 is dominated by QEC decoder throughput and scheduling, magic-state and resource estimation, multi-QPU interconnect, and distributed compilation. Roughly **50–60% of 2025–2026 quantum papers at these four venues are HPC-relevant**, against ~40–50% device-level (calibration, ion shuttling, atom-array layout, cryogenic wiring, frequency planning). In 2024 that ratio was far worse. `[inference]` on top of `[official-program]`

**F5 — ICS is the fastest-rising HPC venue, and its growth is invisible in its CFP.**
ICS went **0 found (2024) → 2 (2025) → 5 (2026)**, and ICS 2026 ran a session literally titled **"Quantum Computing"** (Thursday 15:30–17:10, Minor Hall, chair Miquel Moretó) with five papers in a contiguous proceedings block, pp. 1296–1362. `[official-program]` `[proceedings]` The ICS CFP's only quantum language is a parenthetical inside the architectures bullet. This is the single best example of *de facto* scope diverging from *de jure* scope.

**F6 — SC's scope commitment is escalating on a datable schedule.**
SC24 and SC25 had a topic area named "Post-Moore Computing" with "Quantum computing" as a bullet. **SC26 renamed the topic area to "Post-Moore & Quantum Computing"** — quantum is now a co-headline topic. `[official-CFP]` **Read this as escalating visibility, not new eligibility:** "Quantum computing" was already an explicit bullet *inside* the Post-Moore area in SC24 and SC25, and it remains one bullet among several in SC26. What changed is the track title. SC25 separately added the first *systems*-flavored quantum paper (Qonductor, a QPU cloud orchestrator) rather than only simulation and compilation.

**F7 — ISC is proportionally the densest HPC venue and owns a research thread nobody else has.**
ISC's research track is small (~20–25 papers/year), so 5/3/4 quantum papers is a large share. It has a **dedicated top-level "Quantum Computing" submission track** with six named subtopics and its own area chair `[official-CFP]`, and a **named "Research Paper Session: Quantum Computing"** in the ISC 2025 program `[official-program]`. Uniquely, ISC hosts a sustained LRZ/TUM stream on *operating a QPU inside an HPC centre* — calibration, telemetry, sys-sage topology extension, HPCQC-tailored measurement. **No other venue publishes this thread.**

**F8 — Two systems venues broke through, and their intake is shaped by contribution type.**
**OSDI** (0/2/1) accepts quantum work only when framed as resource management, virtualization, or runtime: QOS (quantum operating system) and "Quantum Virtual Machines" (the HyperQ system) at OSDI '25 — both in a mainstream *"Scheduling and Resource Management"* session, both with artifact-evaluation badges — and qTPU (hybrid tensor-network quantum-classical acceleration) at OSDI '26. `[official-program]` **SIGMETRICS** (0/4/5) accepts it only when framed as measurement and modeling: ScaleQsim (exascale quantum circuit simulation; SeoulTech-led, with LBNL co-authors), Anchor (QPU performance-variability characterization), ECCentric (empirical QEC code analysis). SIGMETRICS names "Quantum computing and communication" in its CFP in all three years `[official-CFP]`. Meanwhile **SOSP, NSDI, EuroSys(-until-2026) and USENIX ATC accepted zero.**

**F9 — Several widely-assumed facts are wrong. Correct these before citing them.**
- There is **no Euro-Par quantum computing track** in 2024, 2025 or 2026. Quantum appears only as a phrase inside Track 3's post-Moore bullet, and Euro-Par's three papers arrived through three *different* tracks. `[official-CFP]`
- **USENIX ATC has been discontinued.** ATC '25 (July 2025) was the final USENIX edition, announced in 2025. It now continues as the **ACM SIGOPS Annual Technical Conference**, Hong Kong, November 2026 (the official site says 15–18 Nov, its CFP says 16–18 — the discrepancy is unresolved), notification 18 Sept 2026, after this survey date. The organizers frame this as a change of sponsor rather than a new venue — *"ATC 2026 is now an ACM conference, but with the same community and scope as before"* — so treat it as a continuation. `[official-CFP]`
- **PACT's quantum scope is non-monotonic, and the 2026 wording is the most on-target signal it has ever given.** PACT 2024 had a named special section, *"PACT for Quantum and Neurmorphic"* (misspelled in the original), with the bullet *"Quantum computing architectures and compilers"*, and yielded one paper. **PACT 2025's CFP dropped quantum entirely** and yielded zero. **PACT 2026's CFP brings it back in a narrower, explicitly HPC-flavored form: *"Quantum-HPC interfacing"*,** a sub-bullet under "Middleware and runtime system support for parallel computing". `[official-CFP]` *(Caution: SIGARCH's abbreviated PACT 2026 listing omits this — it is a condensed announcement, not the CFP. The authoritative CFP is `pact2026.github.io/submit/`.)*
- **HiPC created a dedicated first-class quantum track.** HiPC 2026 Track 5 is "Quantum Computing Systems and Applications", whose stated scope explicitly names *"Quantum HPC frameworks for scientific simulations"*, compilers and runtime systems. `[official-CFP]` **The change is the *track*, not the presence of quantum language:** HiPC 2024 already carried long-standing boilerplate mentions of quantum computing inside its Algorithms and Architecture track topic lists (*"Classical and emerging computation models (e.g., parallel/distributed models, quantum computing, neuromorphic…)"*). What did not exist in 2024 was a dedicated top-level quantum track.

### 2.4 Answers to the seven judgment questions

1. **Which communities produce Quantum-HPC regular papers?** Architecture (ASPLOS/ISCA/MICRO/HPCA) at highest volume; SIGPLAN compilers (CGO/PLDI/OOPSLA) second; classical HPC (SC/ISC/ICS/ICPP/IPDPS/CCGrid/HiPC) third but growing fastest in the integration branch; EDA (DAC/ICCAD/DATE/ICCD) a large fourth pool skewed to compilation and decoder hardware; two systems venues (OSDI, SIGMETRICS) as genuine breakthroughs; IEEE QCE as a high-volume, lower-selectivity reservoir.
2. **How do topics differ by community?** See §2.2 and §5. Architecture → QEC hardware, FT system architecture, control microarchitecture. Compilers → mapping, synthesis, IR, DSLs, simulators. HPC → simulation at scale, QPU-in-centre integration, scheduling, orchestration. Systems → OS/virtualization (OSDI) and measurement (SIGMETRICS). EDA → synthesis, routing, decoder ASICs, cryo-control.
3. **Where did quantum enter main tracks 2024→2026?** ISCA (1→3 sessions, 2025), HPCA (0→2 sessions, 2025), MICRO (1→2 sessions, 2025), ICS (0→5 papers + named session, 2026), SIGMETRICS (0→4, 2025), OSDI (0→2, 2025), EuroSys (0→1, 2026), Euro-Par (0→1→2).
4. **Most active branch right now?** **QEC decoding with system/architecture contribution.** It appears at ISCA, MICRO, HPCA, ASPLOS, EuroSys, IISWC, ICCAD, DAC and QCE simultaneously, and it is the branch where public artifacts actually cluster.
5. **What is regular-paper-level rather than workshop-level?** Simulation at scale, QEC decoding, compilation at scale, QPU scheduling/virtualization, performance characterization. **Still mostly workshop-level:** end-to-end HPC-QC middleware and centre integration case studies — these dominate QCE's WIHPQC and SC-W but appear only sparsely in main tracks (Qonductor at SC25, Pilot-Quantum at CCGrid 2025, the ISC LRZ/TUM thread).
6. **Fastest early-warning sensors for future SC topics?** **IEEE QCE (QSYS track) and ASPLOS.** QCE hosts a problem roughly 12–24 months before a hardened version reaches SC/ASPLOS — the QEC-decoder lineage (Yale group: QCE25 main track → ASPLOS 2025 Micro Blossom) and the parallel-simulation lineage (GraFeyn at QCE24 → Atlas at SC24) both demonstrate this. `[inference]` on `[proceedings]`
7. **Which venue to census first?** SC, then ASPLOS, then ISC. See the companion `QUANTUM_HPC_RESEARCH_QUEUE.md`.

### 2.5 A caution about interpreting the counts

Much of this field is currently carried by a **small number of research groups**, so venue counts are partly group signals. TU Munich (Bhatotia) accounts for OSDI '25, OSDI '26, PLDI '25 and SIGMETRICS '26; TUM/LRZ (Schulz) for the ISC integration thread, QCE24 QSYS and WIHPQC; Rice (Patel) for SIGMETRICS '25, two SIGMETRICS '26 papers and ICS 2026; Wisconsin (Tannu) for EuroSys '26, MICRO '25, HPCA '25, DAC '25; Wille/TUM-CDA for the entire MQT line across DAC, DATE and ICCAD. Treat a venue's count as evidence that the venue *accepts* the work, not that a broad community is producing it. `[inference]`

---

## 3. Venue master table

**Reading the year columns.** A number is given only where it was counted from an official program or a publisher proceedings volume. `0*` means "none found by systematic keyword sweep" rather than a hand-counted zero. `—` means the program was not public as of 2026-09-06. Parenthetical notes flag material caveats.

**SC Relevance** = how directly this venue's output connects to the kind of research SC publishes, on a 1–5 scale (`[inference]`).

### 3.1 Core HPC / parallel

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Regular-paper Evidence | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **SC** | HPC | **7** | **4** | — *(PROGRAM_INCOMPLETE_AS_OF_2026-09-06)* | `[official-CFP]` Topic area "Post-Moore Computing" (SC24/25) → **renamed "Post-Moore & Quantum Computing" (SC26)** | `[proceedings]` IEEE `SC41406.2024`, ACM `10.1145/3712285`; SC25 block pp. 728–788 | Tensor-network & GPU simulation at scale; compilation (neutral-atom, multi-module); surface-code reliability; **QPU cloud orchestration (new 2025)** | **ACTIVE** | 5 | **Tier 1** |
| **ISC High Performance** | HPC | **5** | **3** (+1 quantum-inspired) | **4** | `[official-CFP]` **Dedicated "Quantum Computing" track**, 6 named subtopics incl. "Integration of Quantum Computing and HPC", own area chair | `[proceedings]` IEEE `10.23919/ISC.<yr>`; `[official-program]` named "Research Paper Session: Quantum Computing" (2025) | **HPC-centre QPU integration & operations (unique)**; classical-resource requirements; circuit synthesis; QUBO for scheduling | **ACTIVE** *(densest per capita)* | 5 | **Tier 1** |
| **ICS** | HPC | **0\*** | **2** | **5** | `[official-CFP]` weak — only a parenthetical in the architectures bullet | `[official-program]` ICS 2026 session **"Quantum Computing"**; `[proceedings]` contiguous block pp. 1296–1362 | Multi-GPU stabilizer & compressed statevector simulation; compiler autotuning; circuit partitioning; quantum-cloud security | **EMERGING → ACTIVE** *(fastest-rising)* | 5 | **Tier 1** |
| **ICPP** | HPC | **1** | **3** *(1 STATUS_UNCLEAR)* | **3** *(PROGRAM_LISTED)* | `[official-CFP]` **Dedicated "Quantum Computing" track** (2025, 2026): "parallel simulators…, parallel computing for quantum compilation…, co-design…, hybrid parallel/quantum tools" | `[proceedings]` ACM `3673038`/`3754598`; `[official-program]` icpp2026.github.io/schedule | Parallel circuit simulators; quantum-cloud job scheduling (RL); FTQC ancilla routing; large-scale QAOA | **SCOPE_CONFIRMED**, volume EMERGING | 4 | Tier 2 |
| **IPDPS** | HPC/parallel | **2** | **1** | **2** | `[official-CFP]` sub-bullet in 3 tracks (Architecture; Programming Models/Compilers/Runtime; System Software) — no dedicated track | `[proceedings]` IEEE `IPDPS57955.2024` / `IPDPS64566.2025` / `IPDPS65963.2026` | ARM/SVE statevector simulation; **qubit allocation & multi-programming (AQUA)**; classical kernels for hybrid pipelines; error mitigation | **WATCH** *(leaning EMERGING; down from 3 in 2023)* | 4 | Tier 2 |
| **CCGrid** | cluster/cloud | **0** core *(1 education paper)* | **3** | **0** core *(1 quantum-networking adjacent)* | `[official-CFP]` named topic; Track 4 "Future Compute Continuum" (2024–25) → Track 1 "Hardware Systems…" (2026) | `[proceedings]` IEEE `CCGrid64434.2025`; 2025 papers clustered in main-track session FCC1 | **Quantum-HPC middleware & workload mgmt (Pilot-Quantum)**; FaaS hybrid workflow orchestration; tensor-network simulation | **ACTIVE** *(2025 spike; 2026 core yield fell to 0)* | 4 | Tier 2 |
| **HiPC** | HPC (India) | **2** | **1** | Dec 2026 — not held | `[official-CFP]` **NEW dedicated Track 5 "Quantum Computing Systems and Applications"** (2026), scope names *"Quantum HPC frameworks for scientific simulations"*; **no dedicated quantum track in 2024** (generic quantum boilerplate did appear inside the Algorithms/Architecture tracks) | `[proceedings]` IEEE `HiPC62374.2024` / `HiPC66333.2025` | Classical-quantum integration; GPU circuit simulation + circuit cutting; phase-polynomial synthesis | **ACTIVE** *(institutionalizing)* | 4 | Tier 2 |
| **Euro-Par** | parallel (EU) | **0** /88 | **1** /78 | **2** /87 | `[official-CFP]` **No dedicated quantum track exists** — quantum is one phrase in Track 3's post-Moore bullet | `[proceedings]` Springer main-conference LNCS volumes only (workshop volumes excluded) | No centre of gravity: one mapping paper, one hybrid workflow framework (QSplit), one data-encoding paper — three *different* tracks | **EMERGING** *(clean 0→1→2)* | 3 | Tier 3 |
| **PPoPP** | parallel prog. | **0** /32 | **0** /38 | **0** /51 | `[official-CFP]` scope statement names "quantum computers" | `[official-program]` + `[proceedings]` full enumeration, all three years | — (GPU kernels, sparse LA, LLM systems, concurrency) | **LOW_PRIORITY** | 2 | Tier 3 |
| **HPDC** | parallel/dist. | **0** /26 | **0** /25 | **0** /~40 | `[official-CFP]` "Novel post-Moore computing technologies including … quantum computing" | `[official-program]` + `[proceedings]`; **4 Crossref "HPDC" quantum papers are QUASAR workshop papers — false positives** | — main track; QUASAR **workshop** is dense and in its 3rd edition | **WATCH** *(satellite active, main track not converting)* | 3 | Tier 3 |
| **IEEE Cluster** | cluster | **0** *(1 poster)* | **0** *(2 posters)* | Sept 2026 — not held | `[official-CFP]` **no quantum language in 2024**; added 2025: "Transversal and emerging topics such as … quantum computing" | `[official-program]` full session enumeration 2024, 2025 | — main track; quantum content is entirely poster-level (QPU simulation, distributed quantum MPI) | **WATCH** *(datable scope opening + rising posters)* | 3 | Tier 3 |
| **PACT** | parallel arch./compilers | **1** | **0** | Oct 2026 — not held | `[official-CFP]` **non-monotonic**: 2024 named section "PACT for Quantum and Neurmorphic" [sic] → **2025: quantum language absent** → **2026: returns as "Quantum-HPC interfacing"** under middleware/runtime | `[proceedings]` ACM `10.1145/3656019` (2024) | Quantum circuit compilation / native-gate SWAP decomposition | **WATCH** *(scope signal improving; volume has not followed)* | 4 | Tier 3 |

### 3.2 Architecture

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Regular-paper Evidence | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **ASPLOS** ⚠ | arch/PL/OS | **9** /193 (4.7%) ⚠ | **10** /177 (5.6%) ⚠ | **12** /152 (**7.9%**) ⚠ | `[official-CFP]` **The word "quantum" never appears** in the 2024, 2025 or 2026 CFP — scope is practice-only | `[official-program]` dedicated sessions **all three years** (2/2/3); `[proceedings]` multi-round ACM volumes | NISQ variational + modular arch (2024) → **QEC decoding + GPU simulation (2025)** → compilation-at-scale, QEC scheduling, distributed execution (2026) | **ACTIVE** | 5 | **Tier 1** |
| **ISCA** | architecture | **6** /83 (7.2%) | **16** /132 (12.1%) | **12** /206 (~5.8%; 11 strictly quantum) | `[official-CFP]` sub-clause (2024) → **standalone bullet "Quantum computer architecture" (2025, 2026)** | `[official-program]` sessions 1→**3**→**3**; `[proceedings]` ACM `10.1145/3695053`, DBLP TOC session headings | 2024 all single-QPU compilation → 2025–26 **decoder throughput/scheduling, magic states, resource estimation, multi-QPU interconnect**; 2026 keynote on hybrid QC scale/FT | **ACTIVE** | 5 | **Tier 1** |
| **HPCA** | HPC architecture | **1** regular /75 (1.3%) *(+1 "Best of CAL" — excluded)* | **7** /112 (6.3%) | **8** /119 (6.7%) | `[official-CFP]` **weakest of the four** — always bundled: "Quantum/Superconducting computing" → "Quantum, Superconducting and Emerging technologies…" | `[official-program]` **0**→2→2 sessions; `[proceedings]` IEEE Xplore / DBLP | 2025 compilation + a genuine quantum memory-hierarchy abstraction (LSQCA) → **2026 QEC decoding (incl. cryogenic predecoder) + distributed compilation** | **ACTIVE** *(only since 2025)* | 4 | **Tier 1** |
| **MICRO** | microarchitecture | **3** /113 (2.7%) | **8** /123 (6.5%) | — *(PROGRAM_INCOMPLETE_AS_OF_2026-09-06; 404 on program page)* | `[official-CFP]` **standalone "Quantum computing" bullet all three years** — longest-standing explicit scope of the four | `[official-program]` 1→2 sessions; `[proceedings]` ACM `10.1145/3725843`, IEEE Xplore | **QEC decoding hardware, quantum control microarchitecture, cryogenic I/O and wiring**. Skews closest to hardware; **no classical-simulation papers** in either year | **ACTIVE** *(from 2025)* | 4 | Tier 2 |

### 3.3 Compiler / programming languages

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Regular-paper Evidence | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **CGO** | code gen/opt | **1** | **4** | **3** | `[official-CFP]` explicit: "Code generation and optimizations for heterogeneous or specialized targets, TPUs, GPUs, SoCs, CGRA, and **quantum computers**" | `[official-program]` + `[proceedings]`; **CGO 2025 has two sessions named "Quantum Computing (1)/(2)"** | Circuit mapping under hardware & QEC constraints; retargetable neutral-atom/FPQA backends; quantum DSL compilation; **JIT numerical synthesis (OpenQudit, LBNL)** | **ACTIVE** | 4 | Tier 2 |
| **OOPSLA** (SPLASH) | PL/systems | **4** | **6** | **5** | `[official-CFP]` no quantum language | `[official-program]` `/details/…OOPSLA/…` URLs; **dedicated "Quantum" session (2025)** | Circuit optimization & synthesis; **parallel sparse simulators (qblaze — strong multi-core scaling)**; simulator fuzzing; verification | **ACTIVE** *(for the compilation/simulation subset)* | 3 | Tier 2 |
| **PLDI** | PL design/impl | **5** | **5** | **5** | `[official-CFP]` no quantum language | `[official-program]` PLDI Research Papers track; PACMPL issues | Circuit optimization/compilation; **QVM quantum gate virtualization (runtime)**; simulation compilation (MarQSim); **Cobble — block encodings for quantum linear algebra** (2026 Distinguished Paper) | **ACTIVE** *(subset)* | 3 | Tier 3 |
| **POPL** | PL theory | **5** | **5** | **5** | `[official-CFP]` no quantum language | `[official-program]`; **dedicated "Quantum 1" session (2026)** | Type systems, uncomputation, categorical semantics, circuit verification, assertion languages — **overwhelmingly theory** | **WATCH** *(not a Quantum-HPC venue)* | 1 | Tier 3 |
| **CC** | compiler construction | **0** /22 | **0** /17 | **0** /16 | `[official-CFP]` **explicit, twice**: "…**quantum computing**, and DNA computing" and "…**quantum computing hardware**" | `[official-program]` + `[proceedings]` full enumeration all three years | — (CGO absorbs this work: 8 papers over the same window) | **SCOPE_CONFIRMED / LOW_PRIORITY** | 2 | Tier 3 |

### 3.4 Systems / measurement

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Regular-paper Evidence | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **ACM SIGMETRICS** | perf. measurement | **0** | **4** /80 | **5** /94 | `[official-CFP]` **explicit all three years**: "Quantum computing and communication" under Emerging Topics | `[official-program]` accepted-papers pages; POMACS | **ScaleQsim (exascale quantum circuit simulation, LBNL)**; QPU performance-variability characterization (Anchor); empirical QEC analysis (ECCentric); quantum network resource allocation; QUBO on photonic hardware | **ACTIVE** | 4 | **Tier 1** |
| **OSDI** | operating systems | **0** /38 | **2** | **1** | `[official-CFP]` no quantum language | `[official-program]` USENIX; both 2025 papers in the mainstream **"Scheduling and Resource Management"** session, both artifact-evaluated | **QOS (quantum operating system)**, **HyperQ (quantum virtual machines / multi-tenancy)**, **qTPU (hybrid tensor-network quantum-classical runtime)** | **ACTIVE** | 4 | **Tier 1** |
| **EuroSys** | systems (EU) | **0** /80 | **0** /88 | **1** /150 | `[official-CFP]` no quantum language; nearest bullet is "systems for emerging hardware" | `[proceedings]` ACM `10.1145/3767295.3803584` | **Elastic QEC decoders** — capacity planning & scheduling for classical decoder hardware; `PUBLIC_CODE` | **EMERGING** | 4 | Tier 2 |
| **SOSP** | operating systems | **0** /46 | **0** /72 | **0** /67 | `[official-CFP]` no quantum language | `[official-program]` full enumeration; note an **NSF Workshop on Quantum Operating Systems** was co-located with SOSP 2024 (workshop — excluded) | — | **WATCH** *(OSDI's sibling; most likely next breakthrough)* | 3 | Tier 3 |
| **NSDI** | networking | **0** | **0** | **0** *(spring cycle; fall PROGRAM_INCOMPLETE)* | `[official-CFP]` no quantum language | `[official-program]` full enumeration | — even quantum *networking* work goes to SIGMETRICS/ICDCS instead | **LOW_PRIORITY** | 1 | Tier 3 |
| **USENIX ATC** | systems | **0** /47 | **0** /~60 | **SPONSOR CHANGED** — continues as **ACM SIGOPS ATC**, Hong Kong, Nov 2026 | `[official-CFP]` no quantum language in either the USENIX or the SIGOPS CFP | ATC '25 was the final USENIX-sponsored edition | — | **LOW_PRIORITY** *(track ACM SIGOPS ATC as a WATCH entry)* | 1 | Tier 3 |

### 3.5 Quantum-side sensor

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Regular-paper Evidence | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **IEEE QCE** (Quantum Week) | quantum | 222 tech. papers (**QSYS 46**) | 266 (**QSYS 51**) | **372 in 9 tracks** *(program public; per-track PDFs not yet posted)* | `[official-CFP]` **QSYS**: "full quantum software stack: compilers, runtimes, workflows…", "quantum simulators", "hybrid quantum-classical systems", "resource estimation", "benchmarking". **QAPP**: *"Integrated high-performance computing (HPC) and quantum applications"* | `[official-program]` **per-track "Accepted Technical Papers" PDFs are the authoritative main-track list**; `[proceedings]` IEEE Xplore, volume-partitioned | Simulation, QEC decoding, circuit cutting, scheduling/multiprogramming, multi-QPU, benchmarking, HPC-QC integration | **SCOPE_CONFIRMED + ACTIVE**, with a **WATCH** qualifier on rigor | 3 *(as sensor: 5)* | **Tier 1 (as sensor)** |

### 3.6 Additional venues discovered in this survey

| Venue | Community | 2024 | 2025 | 2026 | Quantum/HPC Scope | Dominant Topics | Status | SC Rel. | Priority |
|---|---|---|---|---|---|---|---|---|---|
| **DAC** | EDA | **5** | **7** | **≥3** | `[official-CFP]` **Research topic area "DES6. Quantum Computing"** with 4 subtopics incl. "DES6.4 EDA for quantum computing systems"; research track 20–25% accept | Neutral-atom & lattice-surgery compilation; FT synthesis; distributed QC hardware-software co-design (Argonne); QEC decoders; readout accelerators | **ACTIVE** *(densest non-candidate venue)* | 3 | Tier 2 |
| **ICCAD** | EDA | 7 quantum total (**4** in scope) | **2** | — | `[official-CFP]` "Quantum computing, algorithms, and applications" **and "Quantum and classical computing integration"** | Circuit knitting/gate cutting; **QPU job scheduling**; microsecond QEC decoder hardware; state-prep synthesis | **ACTIVE** | 3 | Tier 2 |
| **DATE** | EDA (EU) | **2** | **3** | **1+** | `[official-CFP]` **standing named topic "D16 Design Automation for Quantum Computing"** | Compiler figures-of-merit (LRZ co-author); SAT-based FT state prep; **MQT Compiler Collection — quantum-classical compilation framework**; cryo-CMOS control | **ACTIVE** | 3 | Tier 3 |
| **IISWC** | workload characterization | **2** | **1** | — | `[official-CFP]` "Quantum computations and communication" under emerging workloads | **VelociTI (architecture-level perf. model)**, **QRIO (quantum resource orchestrator)**, **decoder-bench (QEC decoder benchmark suite)** | **EMERGING** *(highest signal-to-noise per paper)* | **5** | Tier 2 |
| **ICDCS** | distributed systems | **6** | **2** | — | `[official-CFP]` named main-track topic area **"Quantum Networks and Computing"** | Multi-QPU interconnect topology design; **CloudQC multi-tenant distributed QC**; remote gate scheduling; entanglement routing (mostly off-axis) | **ACTIVE** *(for the multi-QPU / quantum-cloud branch only)* | 3 | Tier 3 |
| **HPEC** | HPC (US) | **3** | **5** | — | `[official-CFP]` topic area **"Quantum and Non-Deterministic Computing"**; full papers archival in IEEE Xplore, extended abstracts non-archival | **TN-Sim tensor-network backend for NWQ-Sim (PNNL)**; partition-based surface-code compilation; QAOA parameter transfer; multilevel hybrid QUBO (NASA QuAIL) | **ACTIVE** *(second-tier archival; excellent community tracker)* | 3 | Tier 3 |
| **ICCD** | computer design | **5** *(3 in scope)* | **6** *(2 in scope)* | — | `[official-CFP]` **not verified** — current CFP unretrievable; recommendation rests on published papers | **Mera & MOSQ — classical simulation acceleration**; UQ-based NISQ benchmarking (PNNL); concolic testing of quantum compilers. 2025 block skews to security | **EMERGING** | 3 | Tier 3 |
| **ACM Computing Frontiers** | emerging arch. | 0 found | **1** | — | `[official-CFP]` "**Quantum computing systems, runtimes**, algorithms and applications" | Thin; the one verified 2025 main-proceedings paper is algorithmic (state prep) | **WATCH** | 2 | Tier 3 |
| **ISPASS** | perf. analysis | **0** | **0** /28 | — | `[official-CFP]` "Quantum computing" listed under emerging technologies | — none verified. The natural sibling of IISWC; that work is going to IISWC instead | **SCOPE_CONFIRMED / WATCH** | 3 | Tier 3 |
| **ASP-DAC** | EDA (Asia) | 0 found | 0 found | — | `[official-CFP]` "EDA and circuits design for quantum and Ising computing" (Topic 13) | — none verified | **SCOPE_CONFIRMED / WATCH** | 2 | Tier 3 |

---

## 4. Venue-by-venue notes

Each entry: official scope → recent main-program evidence → what kind of Quantum-HPC research appears → population density → connection to SC → investigation value.

### 4.1 Tier 1 venues

#### SC (ACM/IEEE Supercomputing) — November
**Official scope.** `[official-CFP]` SC24 and SC25 ran a papers topic area named **"Post-Moore Computing"** whose bullets include verbatim *"Quantum computing"*; SC25 added *"Architectures for extreme heterogeneity or HPC/Quantum hybrids"*. **SC26 renamed the area to "Post-Moore & Quantum Computing"** — the strongest datable scope signal at any HPC venue in this survey.

**Recent evidence.** `[proceedings]` `[official-program]` *(counts and structure re-verified by the Phase 2 SC census, 2026-09-06 — see `SC_2024_2025_QUANTUM_HPC_CENSUS.md`.)* SC24 produced **7** main-track quantum papers across **three** sessions — *Quantum and Approximate Computing I / II / III*, holding 3 / 2 / 3 talks (IEEE DOIs `SC41406.2024.00073/74/75`, `.00079`, `.00085/86/87`). **Correction to an earlier reading: these are not "two consecutive blocks."** Session II's other talk, `.00078` (HPAC-ML, an ML-surrogate programming model), has **no quantum content** despite sitting in a session named "Quantum and Approximate Computing" — a session-name trap for any future census. SC24's volume holds **99 regular technical papers** (`.00016`–`.00114`) plus 9 Gordon Bell / GB-Climate finalists, so the quantum share is **7 / 99 = 7.1%**; SC24's acceptance rate could not be obtained from any official source. **LEXIQL (`.00073`) and the Surface Codes paper (`.00075`) were both Best Student Paper Finalists.** SC25 produced **4**, in a single contiguous block at pp. 728–788 of the ACM volume `10.1145/3712285`, forming exactly one session — *"Quantum Computing and Simulation"* (`sess164`, chair **Angel Yanguas-Gil**, Argonne National Laboratory). SC25 accepted **137 papers from 623 submissions (22%)**, so the quantum share is **4 / 137 = 2.9%**. **No SC25 quantum paper won or was a finalist for any award.** SC26: notification was 1 July 2026 and Best/Best-Student Paper finalists were announced in August 2026 (**none quantum**), but the schedule site returns HTTP 401 and no accepted-papers list is public → `PROGRAM_INCOMPLETE_AS_OF_2026-09-06`.

**What appears.** Two strands. (i) *Simulation at scale*: hierarchical multi-GPU statevector partitioning (Atlas, CMU); tensor-network random-circuit sampling with system/energy co-optimization (Shanghai AI Lab/USTC); MPS-based quantum-kernel ML at scale (HSBC first author, with Quantinuum co-authors); batched pre-trajectory sampling for noisy simulation (NVIDIA). (ii) *Compilation and reliability*: QFT kernel optimization for NISQ and FT targets (Rutgers); neutral-atom compilation under hardware constraints (Rice); surface codes against radiation-induced faults (Trento); inter-module communication-minimizing mapping for distributed architectures (ECNU). **SC25 added the first systems paper: Qonductor, a cloud orchestrator scheduling heterogeneous QPU + classical resources (TU Munich).**

**Density.** Moderate and stable — a dedicated quantum block every year, ~4–7 papers.

**SC connection.** This *is* SC.

**Investigation value: highest.** It defines the target. Note that SC's quantum papers skew toward simulation and compilation; the `Q_IN_HPC` integration branch has only just arrived (Qonductor, 2025), which is precisely the gap worth watching.

**Artifact status — superseded by the Phase 2 census.** This document originally recorded artifact status as `UNKNOWN` for nearly every SC paper. The census established that **7 of the 11 have public code or data**, **6 were verified `CONSISTENT`** at repository level, and **4 carry Zenodo deposits**: Atlas (`10.5281/zenodo.12588145`), the MPS quantum-kernel paper (`…12568631`), PARALLAX (`…12587550`), plus public code for QFT Kernels, Qonductor and QDockBank's dataset, and PTSBE upstreamed into NVIDIA CUDA-Q. **`NO_PUBLIC_ARTIFACT_FOUND` holds for LEXIQL, the Surface Codes paper, and Surpassing Sycamore** — note that the last of these is the corpus's most contested claim and its least reproducible. See §9 of `SC_2024_2025_QUANTUM_HPC_CENSUS.md` for the full matrix. `[code]` `[artifact]`

> **Warning for the census:** SC's proceedings pages are robots-disallowed to automated fetch. The reliable discriminator is the publisher volume identity — `SC24:` (`10.1109/SC41406.2024`) vs `SC24-W: Workshops of…` (`10.1109/SCW63240.2024`); `10.1145/3712285` (SC '25) vs `10.1145/3731599` (SC-W '25). Every `SCW`/`3731599` item is a workshop paper. SC-W '25 alone contains circuit-cutting workflows, a "quantum middle layer", and a 20-qubit HPC-integration case study — all tempting, all out of scope. **Note also that the SC-W volume repaginates from 1, so its page numbers collide with the main volume's — use the DOI prefix, never the page number.**
>
> **Two corrections from the Phase 2 census.** (1) **SC25's Papers-track topic tags are "Post-Moore Computing" and "Quantum Computing"** — *not* "Quantum & Other Post Moore Computing Technologies", which belongs to the **Exhibitor Forum** taxonomy (observed on `exforum122` and on Δ-Motif, `exforum114`). There is no standalone "Quantum Computing" CFP area; the two are peers in the schedule taxonomy only. (2) **The SC25 Gordon Bell block is pp. 1–136 (11 papers)**, DOI suffixes `.3771783`–`.3771790`, `.3771989`, `.3772093`, `.3772094` — not pp. 1–59 as originally recorded; pp. 48–59 sits inside it. Also note the full title of one false positive: *"Multiscale Light-Matter Dynamics in Quantum Materials: **From Electrons to Topological Superlattices**"*. `[official-program]` `[proceedings]`

#### ISC High Performance — June, Hamburg
**Official scope.** `[official-CFP]` ISC has a **dedicated top-level "Quantum Computing" track**, one of six, with its own committee and area chair, and six named subtopics: *Integration of Quantum Computing and HPC; Quantum Computing Basics and Theory; Quantum Computing Technologies and Architectures; Quantum Computing Use Cases; Quantum Error Correction and Fault Tolerance; Quantum Program Development and Optimization.* This is formally the strongest quantum scope of any HPC venue.

**Recent evidence.** `[proceedings]` **5 / 3 / 4** for 2024/2025/2026 in the IEEE research-paper volumes (`10.23919/ISC.<year>`). `[official-program]` ISC 2025 ran a session literally named **"Research Paper Session: Quantum Computing"** (Tue 10 June, Hall 4, chair Amanda Randles).

**What appears.** ISC owns a research thread no other venue has: **operating a QPU inside an HPC centre.** LRZ/TUM produce this steadily — superconducting QPU calibration and performance evaluation in an HPC centre (2024); telemetry for quantum systems in HPC centres (2025); extending the `sys-sage` system-topology library to describe QPUs alongside classical resources (2025); an HPCQC-tailored scalable observable-measurement approach (2026). Alongside: NERSC/LBNL's quantification of the classical compute/memory/bandwidth needed to support large-scale QC; hierarchical multigrid ansatz for VQAs (LANL); tree-based Pauli decomposition (Paris-Saclay/Eviden); MCTS circuit synthesis (Argonne); QUBO for HPC workflow mapping and scheduling (GWDG/Göttingen).

**Density.** Proportionally the densest venue in the survey — 3–5 papers out of a ~20–25-paper research track.

**SC connection.** Same community, same reviewers, European centre of gravity. ISC is where HPC-centre integration work gets published before (or instead of) SC.

**Investigation value: highest, and structurally distinct from SC.** If the research goal is "QPU as a managed HPC-centre resource", ISC is the primary literature, not SC.

> **Publisher note:** since 2024 ISC *research papers* are **IEEE Xplore** (`10.23919/ISC.<year>`), no longer Springer LNCS. ISC **workshops** remain Springer LNCS (`High Performance Computing. ISC High Performance <year> International Workshops`) — excluded.

#### ASPLOS — March/April
**Official scope.** `[official-CFP]` **The word "quantum" does not appear in the ASPLOS 2024, 2025 or 2026 CFP.** The relevant bullet is *"Existing, emerging, and nontraditional compute platforms at all scales."* Scope here is established entirely by revealed practice and PC composition — which makes it less durable and worth re-checking annually.

**Recent evidence.** `[official-program]` Dedicated quantum sessions in **all three years**: 2024 (Quantum Architecture, Variational Quantum Computing), 2025 (Quantum Computing, Quantum Error Correction), 2026 (Quantum Computing: Compilation, Quantum Error Correction, Quantum & Emerging Computing). Counts **9 / 10 / 12** against shrinking programs of 193 / 177 / 152 — so the quantum share *rose* 4.7% → 5.6% → **7.9%**, the highest venue-year share in the survey. `[proceedings]` ASPLOS publishes multiple submission rounds as separate ACM volumes; all are main-conference.

> ### ⚠ PHASE 3 CORRECTION — this paragraph is superseded (2026-09-06)
> The full ASPLOS census (`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`) refutes four claims above.
>
> 1. **Counts are 14 / 10 / 12 presented**, not 9 / 10 / 12. The 2024 figure was undercounted by five papers — One Gate Scheme (AshN), MorphQPV, OnePerc, Fermihedral, Permutable Operators. Cause: the official ASPLOS 2024 program page **truncates after Session 8C**, and one of the five is a deferred paper. **A program page is not a census instrument.**
> 2. **Denominators were wrong and were mixed.** Proceedings totals are **194 / 176 / 152**, not 193 / 177 / 152. Program totals are *derived* from volume structure, never counted: 2024 ≈ 193 `TOTAL_COUNT_UNVERIFIED`, 2025 = 184, 2026 = 168.
> 3. **The share does not rise.** Corrected: **7.7% → 4.5% → 7.2%** by proceedings year, ~7.3% → ~5.4% → ~7.1% by program year. The 4.7% → 5.6% → 7.9% growth story does not survive. `INSUFFICIENT_SAMPLE` for any trend; what did change is **composition** (NISQ variational → QEC + simulation → compilation/FT).
> 4. **"Highest venue-year share in the survey" (7.9%) is withdrawn** — it rested on the wrong 2026 numerator/denominator pair.
>
> **The one structural fact this map missed entirely:** ASPLOS runs three submission cycles and **publishes a volume branded year N that is presented at conference year N+1**. Verbatim from the ASPLOS 2024 CFP: *"Accepted major revisions of the fall cycle will be published as ASPLOS'24 papers but will be presented in ASPLOS'25."* `[official-CFP]` Proceedings year ≠ program year at this venue, and every count in the original paragraph mixed them. **Any future ASPLOS, ISCA, MICRO or HPCA census in this project must establish the volume↔program mapping before counting anything.**

**What appears.** 2024: modular/chiplet architecture, a million-qubit distributed FT machine design, adaptive predecoding for real-time QEC — but *half the papers were NISQ variational-algorithm and mitigation work* with little for a systems builder. 2025 is the **strongest single year in the survey for HPC transferability**: GPU-accelerated batched decision-diagram simulation (BQSim, `PUBLIC_CODE`), FPGA MWPM decoding at sub-microsecond latency (Micro Blossom, `PUBLIC_CODE`), circuit cutting + qubit reuse for running large circuits on small devices (QRCC), real-time QEC scheduling (RESCQ), heterogeneous QEC code architectures (HetEC), QEC layout synthesis (QECC-Synth). 2026: distributed multi-party SWAP test, analog-simulation compiler (QTurbo, Penn/LBNL), syndrome-circuit scheduling (AlphaSyndrome), FT resource estimation, a shot-reduction execution framework (TreeVQA).

**Density.** Highest consistent share; ~58–60% of its quantum papers are HPC-relevant in 2025–2026.

**SC connection.** ASPLOS's PL/OS identity means its quantum papers are the most likely of the architecture venues to contain runtime, compiler-infrastructure and system-software contributions an HPC centre could adopt. **Public artifacts cluster here** — the two most HPC-relevant confirmed public-code papers in the whole survey (BQSim, Micro Blossom) are both ASPLOS 2025.

**Investigation value: highest among architecture venues.**

#### ISCA — June/July
**Official scope.** `[official-CFP]` Promoted from a sub-clause in 2024 (*"Architectures for emerging technologies including … quantum computing, etc."*) to a **standalone bullet, "Quantum computer architecture"**, in 2025 and 2026. A datable scope signal.

**Recent evidence.** `[official-program]` Sessions: **1 (2024) → 3 (2025) → 3 (2026)**. Counts 6 / 16 / 12. ISCA 2026 also ran a keynote titled *"Architecting Hybrid Quantum-Classical Computing for Scale and Fault Tolerance."*

**What appears.** A clean topical pivot. 2024 was **entirely single-QPU circuit compilation** — bosonic compilation, VQA compilation frameworks, neutral-atom compilers, context-aware noise-suppressing compilation, SAT-based lattice surgery. From 2025 the profile becomes HPC-shaped: speculative window decoding to hide decoder latency (SWIPER, `PUBLIC_ARTIFACT`), computational reuse across noisy-simulation trajectories, switch-network topologies for multi-QPU data centres (SwitchQNet), low-latency hybrid quantum-classical integration (Qtenon), transversal-architecture resource analysis, FTQC synchronization, entanglement distillation for quantum interconnects. 2026 continues: adaptive parallel-window decode scheduling (Triage), ensemble decoder algorithm-hardware co-design, cryogenic syndrome compression at 4 K, noisy-simulation cost reduction (TUSQ), transpiler-architecture co-design at FT scale, Hamiltonian-simulation compilation (Kernpiler).

**Density.** Highest absolute session count. HPC-relevant fraction ~1/6 in 2024 → ~50% in 2025 → ~2/3 in 2026.

**SC connection.** Indirect but strong: decoder throughput, multi-QPU interconnect and resource estimation are exactly the problems that become HPC-centre problems once a QPU is attached to a machine room.

**Investigation value: high.** Watch the decoder and multi-QPU strands specifically; skip the device-layout papers.

#### HPCA — Feb/March
**Official scope.** `[official-CFP]` **Weakest explicit scope of the four architecture venues** despite the name — quantum is always bundled: *"Quantum/Superconducting computing"* (2024) → *"Quantum, Superconducting and Emerging technologies impacting computer architectures"* (2025) → *"Architectures using quantum, superconducting, and emerging technologies"* (2026).

**Recent evidence.** `[official-program]` **HPCA 2024 had no dedicated quantum session at all** and only **one** main-track regular quantum paper in 75 (MIRAGE, mirror-gate decomposition + routing co-design). Two dedicated sessions appeared in 2025 ("Quantum Slots 1/2", 7 papers) and 2026 ("Quantum Computing Architecture", "Quantum Compilation and Simulation", 8 papers).

**What appears.** 2025: a genuine **load/store memory-hierarchy abstraction for early-FT machines** (LSQCA, U. Tokyo/NTT/RIKEN) — the clearest "memory hierarchy for quantum" paper in the survey; Clifford extraction/absorption circuit optimization (QuCLEAR, Argonne/UChicago); Hamiltonian-aware fermion-to-qubit mapping (HATT, Penn/Berkeley/LBNL — directly targets chemistry workloads); reuse-aware zoned neutral-atom compilation (UCLA). 2026 is where HPCA becomes genuinely useful: **fully parallelized BP decoding for QLDPC codes outperforming BP-OSD** (NC State/PNNL, `PUBLIC_CODE`), a cryogenic predecoder (Pinball, Michigan), distributed MBQC compilation (DC-MBQC, ICT CAS), and trace-based dataflow reconstruction for FT systems (TraceQ, Yale/UChicago).

**Density.** 1 → 7 → 8. Latest bloomer of the four.

**SC connection.** The 2026 decoder papers, one with public code, are the most directly transferable HPC artifacts at any architecture venue this year.

**Investigation value: high, but only from 2025 onward.** **Do not cite HPCA 2024 as evidence of an established quantum track — it is not.**

#### ACM SIGMETRICS — June
**Official scope.** `[official-CFP]` **Explicit in all three years.** SIGMETRICS 2026 lists *"Quantum computing and communication"* under "Emerging Topics and Application Areas"; identical language in 2025; SIGMETRICS 2024 listed *"Quantum computing"* plus *"…quantum networks…"*.

**Recent evidence.** `[official-program]` **0 (2024) → 4 (2025) → 5 (2026)**. Note the one-year lag: scope preceded uptake by a full year.

**What appears.** This is the only venue in the survey where the **performance-modeling and measurement branch is well populated**. 2026: **ScaleQsim, "Highly Scalable Quantum Circuit Simulation Framework for Exascale HPC Systems"** (SeoulTech + LBNL + Chung-Ang) — the single most on-target paper found anywhere, with explicit exascale HPC framing and DOE-lab co-authorship; **Anchor**, reducing temporal and spatial output performance variability on quantum computers (Rice) — a classic SIGMETRICS variability study applied to QPUs; **ECCentric**, empirical analysis of QEC codes (TU Munich); a fine-grained reliability analysis framework for noisy circuits; QUBO on real photonic hardware (ObliQ). 2025: PachinQo (Rydberg-atom modeling/simulation for HW-SW co-design, Rice), quantum network routing and fair resource allocation, quantum-based FEC in the RAN.

**Density.** Moderate and rapidly growing, on an explicit standing invitation.

**SC connection.** Very strong methodologically. Performance modeling, benchmarking, variability characterization and queueing analysis of quantum cloud services are SC-shaped contributions; SIGMETRICS is currently the best home for them and has almost no HPC-venue competition.

**Investigation value: high, and underrated.** This venue was on the candidate list but is far more productive than its position there suggested.

#### OSDI — July
**Official scope.** `[official-CFP]` No quantum language. Acceptance is entirely bottom-up.

**Recent evidence.** `[official-program]` **0 (2024, 38 papers) → 2 (2025) → 1 (2026)**. Both 2025 papers sat in the mainstream **"Scheduling and Resource Management"** session — not a special track — and both carry artifact-evaluation badges.

**What appears.** All three are systems papers, none are compiler or theory papers.
- **QOS: Quantum Operating System** (TU Munich) — modular quantum OS with a hardware-agnostic job API, error mitigation, and space/time multi-programming; reports 2.6–456.5× fidelity and up to 9.6× utilization on IBM devices.
- **"Quantum Virtual Machines"** — cite by title; **HyperQ** is the system inside it (Tao & Zhu, U. Maryland; Nieh & Gu, Columbia; Yao, Toronto) — a virtualization layer multiplexing multiple quantum programs on one QPU in time and space with isolation, working unmodified with existing compilers; up to an order of magnitude utilization/throughput gain.
- **qTPU: Hybrid Tensor Networks for Quantum-Classical Acceleration** (TU Munich, OSDI '26) — programming model + compiler + runtime over a hybrid tensor-network abstraction; reports 3–4 orders of magnitude lower classical overhead and >20× end-to-end speedups.

**Density.** Sparse but real, from a zero baseline, with no CFP encouragement.

**SC connection.** Direct and important. QPU multiplexing, multi-tenancy and job scheduling are the same problem class as HPC batch scheduling and node sharing — this is the closest existing literature to what a supercomputing centre would need to run a QPU as a shared resource.

**Investigation value: high.** OSDI is the only top-tier OS venue that has actually admitted quantum resource-management work.

#### IEEE QCE (IEEE Quantum Week) — September
**Official scope.** `[official-CFP]` Nine technical tracks in 2026 (seven in 2024–25). **QSYS (Quantum System Software)** — *"the design, architecture, and operation of full-stack quantum computing systems"* — is the primary track to watch, with topics naming *"full quantum software stack: compilers, runtimes, workflows, languages, transpilers, profilers"*, *"quantum simulators"*, *"hybrid quantum-classical systems"*, *"resource estimation"*, *"benchmarking of quantum systems"*, *"software for co-design"*. **QAPP** is the only track whose CFP names HPC explicitly: *"Integrated high-performance computing (HPC) and quantum applications"* (identical in 2024, 2025, 2026). **QNET** carries *"distributed quantum computing"*.

**Recent evidence.** `[official-program]` 222 technical papers in 2024 (QSYS 46), 266 in 2025 (QSYS 51), and **372 in 9 tracks in 2026** (program public; conference 13–18 Sept 2026, Toronto). QSYS is ~19–21% of the main track. QCE26's QSYS track alone runs **29 sessions**, including *Scalable Quantum Circuit Simulation, Real-Time QEC Decoding, Distributed Quantum Systems, Modular Architectures & Communication-Aware Compilation, Quantum Systems & Resource Management, Runtime Workflows & Compilation Reuse, Quantum Circuit Cutting & Partitioned Execution, Accelerated QEC & Feedback Systems, Benchmarking & Reproducibility.*

**What appears.** Representative confirmed main-track examples: HPC-QPU integration architecture (Elsharkawy/Schulz, TUM); **GraFeyn**, efficient parallel sparse circuit simulation (CMU/Yale, QSYS Best Paper 2nd place, `PUBLIC_CODE`); decision-diagram vs statevector simulation efficiency; a **quantum hardware roofline** porting HPC roofline methodology to QPU design-space evaluation (LBNL); scalable circuit cutting + scheduling on distributed QPUs (Fordham/PNNL); parallel quantum job scheduling (CWRU); network-integrated real-time QEC decoding under lattice surgery (Yale); a highly-parallel atom rearrangement sequencer (TUM); online job scheduling for FT multiprogramming; multi-core layout synthesis over a teleport interconnect; *"Is circuit depth accurate for comparing quantum circuit runtimes?"* (Argonne); observable-estimation performance assessment (LBNL/NERSC); the IBM Quantum Engine Compiler (MLIR-based, `PUBLIC_CODE`).

**Selectivity — be realistic.** The official target is *"approximately 40-50% of the submitted papers"*; actuals were ~49% (2024: 222/450+) and ~48% (2025: 266/557+). Review is **single-blind** with 3 TPC reviews. CORE ranks QCE **National/Regional**; SC is **Rank A**. `[official-CFP]` `[proceedings]`

**Density.** By raw count the largest reservoir in the survey. But note where the *HPC* content actually sits — see the warning below.

**SC connection: as a sensor, excellent.** Two demonstrated migration lineages: the Yale QEC-decoder group published network-integrated real-time decoding at QCE25 main track while the same group's **Micro Blossom** went to **ASPLOS 2025**; GraFeyn (QCE24) sits in the same problem space as **Atlas** at **SC24**. QCE consistently hosts a problem 12–24 months before a hardened version reaches SC/ASPLOS.

**Investigation value: high as a sensor, moderate as a target.** For someone aiming at SC-type venues, a QCE paper is a credible stepping stone and a good way to establish presence, but it will not substitute for an SC/IPDPS/ASPLOS line.

> **Two hard warnings for the QCE census.**
> **(1) The most HPC-relevant-sounding QCE titles are usually workshop papers.** The QCE25 **WIHPQC25** workshop (5th International Workshop on Integrating HPC with Quantum Computing, organized by Schulz/TUM, Schulz/ANL, Karlsson/DTU) alone contained *"HPCQCMark: a new Modular HPC-QC Benchmarking Framework"*, *"Towards System-Level Quantum-Accelerator Integration"*, *"Dynamic Solutions for Hybrid Quantum-HPC Resource Allocation"*, and *"Qubit Health Analytics and Clustering for HPC-Integrated Quantum Processors"*. **None are main-track.** QCE's HPC centre of gravity is its workshop; its main-track HPC content is filed under QSYS as compilation/simulation/QEC/scheduling rather than under an "HPC" label.
> **(2) Never classify from IEEE Xplore alone.** A single QCE proceedings contains technical papers, workshop papers, poster abstracts, and panel/tutorial abstracts under the same conference name. **The authoritative main-track list is the official per-track "Accepted Technical Papers" PDF** published by the organizers. Page count is not a reliable discriminator: QCE25 workshop papers ran ~6–7 pages, overlapping the ≤7-page short-paper band; only the proceedings volume/section heading or the official PDF settles it. Note also that no per-track PDF has been posted for QCE26 as of 2026-09-06 — the QCE26 census should wait for it or for the Xplore posting.

#### ICS (ACM International Conference on Supercomputing) — June/July
**Official scope.** `[official-CFP]` Thin. Five domains, and the only quantum mention is a parenthetical: *"architectures based on future and emerging hardware (e.g. quantum, superconducting, photonic, neuromorphic)"*. **The CFP badly understates what ICS is actually doing.**

**Recent evidence.** `[official-program]` **ICS 2026 ran a session titled "Quantum Computing"** (Thu 15:30–17:10, Minor Hall, chair Miquel Moretó) with **5 papers**, verified against a contiguous ACM proceedings block, pp. 1296–1362. Counts: **0 found (2024) → 2 (2025) → 5 (2026)**.

**What appears.** 2026: multi-GPU extended-stabilizer simulation (quEStab, Kyungpook Nat'l Univ.); memory-hierarchy-style qubit management for zoned neutral-atom machines (EZCache, ECNU); autotuning quantum compiler pass pipelines at scale (TuniQ, Rice); closeness-centrality circuit partitioning for distributed simulation (C-3PQ, LBNL/RIKEN/UNC); diagonal-budgeted Trotterization for Hamiltonian simulation (NC State/ORNL). 2025: lossy-compression to fit large statevector simulations in GPU memory (BMQSim, Indiana/PNNL); output obfuscation for circuits on untrusted quantum clouds (OpaQue, Rice/Northeastern/Oxford).

**Density.** Sharply growing; ICS 2026 is the densest single venue-year among the HPC venues.

**SC connection.** Same community, same reviewers, heavily overlapping PC. ICS is currently a leading indicator for SC.

**Investigation value: high, and rising fastest.** Also the cleanest example of why the CFP must never be trusted alone.

> ICS 2024: reported as **"none found by keyword sweep"**, not a hand-counted zero — the ACM DL TOC could not be walked page-by-page. Confirm before citing ICS 2024 as an empty year.

### 4.2 Tier 2 venues

#### CGO — February/March (co-located with PPoPP/HPCA/CC)
`[official-CFP]` Explicit: *"Code generation and optimizations for heterogeneous or specialized targets, TPUs, GPUs, SoCs, CGRA, and **quantum computers**"*. `[official-program]` **CGO 2025's proceedings TOC labels two sessions "Quantum Computing (1)" and "Quantum Computing (2)"** — a structural commitment, not incidental acceptance. Counts **1 / 4 / 3**. Topics: surface-code circuit mapping and scheduling under lattice-surgery constraints (Ecmas); compiler-driven synthesis of quantum simulators; retargetable FPQA/neutral-atom compiler backends (Weaver); a full compiler for the Qwerty basis-oriented quantum language (ASDF); qubit-movement-optimized codegen for zoned neutral-atom processors; **dependence-driven circuit mapping with affine/polyhedral abstractions** (2026 — the strongest methodological transfer from classical HPC compilers found anywhere); space-time optimization for early-FT computation (Cambridge); **OpenQudit, a JIT-compiled DSL for numerical quantum compilation (LBNL)**. **Investigation value: high for anyone with a compiler angle.** For a Quantum-HPC compiler submission, CGO strictly dominates CC on demonstrated acceptance.

#### MICRO — October/November
`[official-CFP]` Standalone *"Quantum computing"* bullet in all three years — the longest-standing explicit scope among the architecture venues. `[official-program]` Sessions 1 (2024) → 2 (2025); counts 3 / 8 / —. MICRO's quantum work sits **closest to the hardware** of the four: QLDPC decoding hardware (Vegapunk — online hierarchical decoder + sparse accelerator, ZJU; Flag-Proxy Networks, Georgia Tech/IBM), distributed quantum control architecture (Distributed-HISQ, ICT CAS), speculative leakage detection for QEC (Wisconsin), cryogenic wiring and multiplexing, ion shuttle scheduling. **Multi-device VQA job scheduling (Qoncord, UBC/UT Austin, 2024) is the closest analogue to an HPC batch scheduler for QPUs.** Notably **no classical-simulation papers** in either year — a gap versus ASPLOS and ISCA. `PROGRAM_INCOMPLETE_AS_OF_2026-09-06`: the MICRO-59 program page returns 404 and the Program menu lists only Workshops & Tutorials; notifications went out ~7 July 2026. **Re-check late Sept/Oct 2026.**

#### ICPP — Sept/Oct
`[official-CFP]` **Dedicated top-level "Quantum Computing" track** in 2025 and 2026, with verbatim scope *"Parallel simulators of quantum computers, use of parallel computing for quantum compilation and optimization, co-design of parallel- and quantum-computing applications, hybrid parallel/quantum software-development tools."* Formally the second-strongest scope after ISC. `[proceedings]` But realized volume is only **1 / 3 / 3**, and — a mild negative signal — **ICPP 2026 has no quantum session**; its three papers are scattered across generically named sessions. Topics: decision-diagram circuit simulation with flat-array layout (FlatDD); cycle-aware parallel optimization against ZZ crosstalk; **RL-based adaptive job scheduling in quantum clouds** (Kent State); cluster-scale statevector simulation via cache blocking and gate fusion (NTU/NCKU); scalable surface-code ancilla routing for distributed FTQC (S2PAR, PNNL/Princeton/Fordham/UMass); MillionQAOA. **Worth submitting to** — the track guarantees appropriate reviewers — **but not yet a high-yield venue for harvesting.**

> `STATUS_UNCLEAR`: *Q-GEAR: Improving quantum simulation framework* (Guo et al., NERSC/LBNL) is registered in Crossref under **both** the ICPP'25 main proceedings (`10.1145/3754598.3754608`, pp. 638–647) **and** the ICPP'25 Workshops proceedings (`10.1145/3750720.3757302`, pp. 200–209), with internally coherent page ranges in both. **Do not cite it as a main-track paper without an ACM DL check.**

#### IPDPS — May/June
`[official-CFP]` No dedicated track; quantum appears as an emerging-platform qualifier inside three tracks (Architecture; Programming Models/Compilers/Runtime; System Software). `[proceedings]` **2 / 1 / 2**, down from 3 in 2023 — the only HPC venue trending slightly *down*. Papers cluster in adjacent DOIs, i.e. a small quantum session each year. Topics: scalable differentiable simulator for quantum computational chemistry (CAS); memory-efficient parallel graph coloring for Pauli-term grouping (Picasso, PNNL/NCSU); **AQUA — hardware-agnostic qubit allocation for quantum multi-programming** (Korea Univ., 2025; the only QPU-multiplexing paper at an HPC venue); vector-length-agnostic statevector simulation on ARM/SVE (KTH/LLNL/JSC, 2026); contrast-filter error mitigation (NC State). **Reliable 1–2 papers a year; monitor, don't prioritize.**

#### CCGrid — May
`[official-CFP]` Named topic sustained across a track restructuring: Track 4 "Future Compute Continuum" (2024–25) → Track 1 "Hardware Systems, Architectures, and Future Compute Platforms" (2026). `[official-program]` **2025 is the standout year: three in-scope main-track papers concentrated in one session (FCC1)** — deliberate PC grouping, not accident. Topics: **Pilot-Quantum, a middleware for Quantum-HPC resource, workload and task management** (Mantha, Kiwit, Saurabh, Jha, Luckow — `PUBLIC_CODE`, `github.com/radical-cybertools/pilot-quantum`); choreography and profiling of quantum-classical FaaS workflows on hybrid clouds (IISc/IBM); tensor-network contraction optimization for circuit simulation (SWIFTN, SeoulTech/LBNL). **Caveat:** the 2026 core yield fell to zero, with quantum content shifting to networking and PQC. **Investigation value: high for the middleware/orchestration branch specifically — Pilot-Quantum is one of the few main-track HPC-QC middleware papers that exists.**

#### HiPC — December, Bengaluru
`[official-CFP]` **The most significant structural change found in this survey.** HiPC 2024 had **no dedicated quantum track** — only long-standing boilerplate mentions of quantum computing inside the Algorithms and Architecture track topic lists. HiPC 2026 restructured to five tracks of which **Track 5 is "Quantum Computing Systems and Applications"** — *"original research on designing innovative quantum and quantum-classical hybrid algorithms, hardware, applications, compiler and runtime systems"* — with listed topics including **"quantum HPC frameworks"**. (The exact introduction year, 2025 or 2026, is `STATUS_UNCLEAR`: the 2025 CFP page has been overwritten and Wayback was blocked.) `[proceedings]` Main-track papers in **both** years checked — 2024: classical-quantum integration challenges (Kulkarni & Bethel), and circuit partitioning vs full-circuit execution for GPU-based simulation; 2025: hardware-aware optimal phase-polynomial synthesis (HOPPS, Case Western/Argonne). **This is a venue transitioning from incidental acceptance to institutional commitment. HiPC 2026 (Dec 2026) is a priority monitoring target.**

> **Census warning:** HiPC's advance programme publishes session names **without paper titles**. Programme-page inspection alone will find nothing — go to the IEEE proceedings volume (`HiPC<id>.<year>` for main, `HiPCW<id>.<year>` for workshops).

#### OOPSLA (SPLASH) — October
`[official-CFP]` No quantum language. `[official-program]` **4 / 6 / 5**, with a dedicated **"Quantum" session in 2025**. The HPC-relevant core is small but real: **qblaze, "An Efficient and Scalable Sparse Quantum Simulator"** (INSAIT/Sofia, Oxford, ETH Zurich) — a parallel sparse state-vector simulator with a compact sorted-array representation, orders-of-magnitude gains and strong multi-core scaling; this is a genuine HPC simulation paper and the single most on-target OOPSLA item. Also: learning-based circuit optimization (Quarl), fast circuit synthesis (Synthetiq, ETH), a quantum control-flow abstract machine (MIT), fuzzing of quantum *simulator implementations*, and 2026's synthesis of circuit-optimization rules and quantum-regular-language state compilation. The rest is verification-heavy and out of scope.

#### EuroSys — April
`[official-CFP]` No quantum language; nearest bullet is "systems for emerging hardware". `[official-program]` **0 / 0 / 1**. The one paper is well-formed and directly relevant: **"A Case for Elastic Quantum Error Correction Decoders"** (Maurya, Molavi, Albarghouthi, Tannu, Wisconsin) — capacity planning and elastic resource allocation for classical QEC decoder hardware, treating decoding as a classical systems provisioning problem, with `PUBLIC_CODE` at `github.com/satvikmaurya/decoder-resources`. **EMERGING; watch EuroSys 2027 to see whether it repeats.**

#### DAC / ICCAD / DATE — the EDA pool
Collectively the largest *uncovered* pool found. **DAC** `[official-CFP]` has a research topic area **"DES6. Quantum Computing"** with four subtopics including *"DES6.4 EDA for quantum computing systems"*, and a 20–25% research-track acceptance rate; counts 5 / 7 / ≥3. **ICCAD** `[official-CFP]` lists *"Quantum computing, algorithms, and applications"* **and "Quantum and classical computing integration"**. **DATE** `[official-CFP]` has a standing named topic **"D16 Design Automation for Quantum Computing"**.
The HPC-relevant slice: hardware-software co-design for **distributed** quantum computing (Argonne, DAC 2025); **QPU job scheduling to reduce execution latency** (ICCAD 2024); hardware-aware gate cutting / circuit knitting (ICCAD 2024); microsecond-latency hardware QEC decoders (SOME, ICCAD 2025; Ising-model decoder, DAC 2025); scalable zoned neutral-atom and lattice-surgery compilation (DAC 2026); **The MQT Compiler Collection — a blueprint for a future-proof quantum-classical compilation framework** (DATE 2026); compiler figures-of-merit work with an LRZ co-author (DATE 2025). Roughly **half of the EDA quantum output is device- or EDA-internal** (readout electronics, cryo-CMOS control, AQFP circuits) and should be filtered out. **Investigation value: moderate-to-high, concentrated in compilation and decoder hardware.** Note the Wille/TUM-CDA group's MQT line is open source and spans all three venues.

#### IISWC — Oct/Nov
`[official-CFP]` *"Quantum computations and communication"* listed under characterization of emerging workloads. Only **2 / 1** papers found — but **the highest signal-to-noise per paper in the entire survey**, because every one is exactly the genre SC publishes: **VelociTI**, an architecture-level performance modeling framework for trapped-ion quantum computers (Harvard, Brooks/Wei); **QRIO**, a Quantum Resource Infrastructure Orchestrator (Michigan, Ravi); **decoder-bench**, a benchmark suite for QEC decoders (Wisconsin/UChicago/Arizona/UT Austin — Maurya, Viszlai, Raveendran, Das, Tannu). **Strong upgrade candidate to ACTIVE if 2026 continues.** Note IISWC has two main-proceedings categories, Regular papers (10 pp.) and Tool-and-benchmark papers (6–10 pp.); both are main track, posters are separate.

### 4.3 Tier 3 and negative findings

**Negative findings are results.** Four venues in the original candidate list produce essentially nothing, and saying so precisely is more useful than padding.

- **PPoPP** — 0 across 121 main-track papers in three years, despite a CFP scope statement that names quantum computers. Actual acceptances are GPU kernels, sparse linear algebra, LLM systems, concurrent data structures, stencils. **LOW_PRIORITY.** *(Co-location trap: PPoPP shares its week with CGO/HPCA/CC — never attribute a CGO or HPCA quantum paper to PPoPP.)*
- **CC** — 0 across 22/17/16 papers, despite the **most inviting CFP of any venue surveyed** (two separate quantum bullets). The cleanest "declared scope, zero uptake" case in the survey; CGO absorbs this work. **SCOPE_CONFIRMED / LOW_PRIORITY.**
- **HPDC** — 0 main-track across ~91 papers. But three structural signals suggest a maturing pipeline: a standing CFP bullet, a **QUASAR workshop now in its 3rd edition and growing** (3 papers 2025 → 4 papers 2026), and a 2025 quantum-software keynote by Fred Chong. **WATCH; re-check after HPDC 2027.**
- **IEEE Cluster** — 0 main-track, but a datable scope opening (**no quantum language in the 2024 CFP; added in 2025**: *"Transversal and emerging topics such as AI for HPC, HPC for AI, quantum computing, accelerators…"*) and a rising poster signal (SYCL QPU simulation framework, NetQMPI distributed-quantum MPI library, Ethernet-connected QEC systems). **WATCH** — the specific event to look for is a poster author converting to a full paper. Cluster 2026 (22–25 Sept, Alexandria VA) falls just past this survey.
- **Euro-Par** — 0 / 1 / 2, a clean monotonic rise, but the papers landed in **three different tracks**, which suggests organic diffusion rather than a single sympathetic chair. **EMERGING.** Correct the record: **there is no Euro-Par quantum track.**
- **PACT** — 1 / 0 / not-yet-held. Its CFP scope is **non-monotonic**: a named *"PACT for Quantum and Neurmorphic"* [sic] section in 2024 (yield: one paper, on native-gate SWAP decomposition), **no quantum language in 2025** (yield: zero), and in 2026 a return in the narrowest but most relevant form yet — ***"Quantum-HPC interfacing"***, a sub-bullet under "Middleware and runtime system support for parallel computing". For a Quantum-HPC map specifically, that 2026 phrasing is the strongest signal PACT has ever given, even though volume has not followed. **WATCH; re-assess after PACT 2026 (19–22 Oct, Chicago).** *(Use `pact2026.github.io/submit/` as the CFP — the SIGARCH listing is an abbreviated announcement that omits the quantum sub-bullet.)*
- **POPL** — 5 papers a year and a dedicated "Quantum 1" session in 2026, but overwhelmingly type systems, semantics and verification with no performance or system artifact. Only two papers in three years cross into scope (SimuQ 2024; Amy & Lunderville's relational analyses for circuit optimization, 2025). **WATCH — not a Quantum-HPC venue.**
- **PLDI** — 5/5/5, and two 2026 Distinguished Papers are quantum, which signals community endorsement rather than tolerance. For this map the relevant items are **QVM (Quantum Gate Virtualization Machine, TU Munich, 2025)** and **Cobble (compiling block encodings for quantum computational linear algebra, 2026)**. Most of the rest is circuit optimization or verification. **Tier 3, monitor selectively.**
- **SOSP** — 0 across 46/72/67. **WATCH, not LOW_PRIORITY**: identical CFP and overlapping PC with OSDI, which has now taken three quantum papers, and an **NSF Workshop on Quantum Operating Systems and Real-Time Control was co-located with SOSP 2024** (workshop — excluded, but a real signal that the quantum-OS community courted this audience). Most likely next systems venue to break through.
- **NSDI** — 0 across three years. The telling detail: even *quantum networking* papers, NSDI's natural entry point, are going to SIGMETRICS and ICDCS instead. **LOW_PRIORITY.**
- **USENIX ATC** — **discontinued as a USENIX conference.** ATC '25 was the final USENIX edition, announced in 2025 citing declining participation. It continues under ACM SIGOPS sponsorship as the **ACM SIGOPS Annual Technical Conference**, Hong Kong, November 2026 (official site: 15–18 Nov; CFP: 16–18 Nov — unresolved), notification 18 Sept 2026, so `PROGRAM_INCOMPLETE_AS_OF_2026-09-06`. The organizers assert continuity (*"the same community and scope as before"*), so treat it as a sponsor change rather than a new venue. Neither CFP has quantum language. **Track ACM SIGOPS ATC as a WATCH entry.**
- **ICDCS** — 6 (2024) / 2 (2025), with a named main-track topic area *"Quantum Networks and Computing"*. Be honest about the composition: the body is dominated by **entanglement-routing / quantum-internet** work, a distinct community from HPC systems. Only three papers are genuinely multi-QPU resource-management systems papers (network topology design for distributed QC; **CloudQC**, network-aware multi-tenant distributed QC; remote gate scheduling). **ACTIVE for the multi-QPU branch only.**
- **HPEC** — a *native HPC-community* venue with a **"Quantum and Non-Deterministic Computing"** topic area; 3 (2024) / 5 (2025). Full papers are archival in IEEE Xplore; extended abstracts are not and must be excluded. High cultural fit, lighter review than SC (6 pages). Where PNNL (**TN-Sim tensor-network backend for NWQ-Sim**), Lincoln Lab, NASA QuAIL and Argonne-adjacent groups put quantum-HPC work that is not yet an SC submission. **Excellent as a venue-of-first-resort and a people tracker.**
- **ICCD** — underrated. 2024's **Mera** (memory reduction + acceleration for quantum circuit simulation) and **MOSQ** (accelerating classical simulation of UCCSD ansatz circuits) are squarely `Q_IN_HPC`/simulation papers; 2025's **UQ-VarQA** is PNNL benchmarking work. Caveat: the 2025 quantum block skews to security/side-channel (4 of 6). Also publishes 4-page short papers — check page spans. **EMERGING.**
- **ISPASS** — `[official-CFP]` lists "Quantum computing" under emerging technologies, but **ISPASS 2025's full 28-paper accepted list has zero quantum papers**. The natural sibling of IISWC; that work is going to IISWC instead. **SCOPE_CONFIRMED / WATCH.**
- **ASP-DAC** — `[official-CFP]` "EDA and circuits design for quantum and Ising computing" (Topic 13, identical 2025 and 2026), but no quantum-titled papers found in the 2025 proceedings. **SCOPE_CONFIRMED / WATCH**; include for Asia-Pacific coverage, don't staff it.
- **ACM Computing Frontiers** — `[official-CFP]` *"Quantum computing systems, runtimes, algorithms and applications"* is genuinely on-target wording, and CF has historical form (heterogeneous-HPC quantum simulators, 2019; heterogeneous quantum computer architecture, 2016), but 2024–2026 main-track yield is thin and the one verified 2025 paper is algorithmic. **WATCH.** Note CF publishes a separate workshops-and-special-sessions volume — do not count it.

### 4.4 Considered and rejected

- **ICPE** — full 2025 accepted list across all tracks: zero quantum; no quantum wording in the research-track description.
- **MASCOTS** — 2026 CFP topic list contains no mention of quantum.
- **PASC** — papers track is properly peer-reviewed with ACM DL proceedings and full 10-page papers, so it passes structurally, but PASC 2025 accepted **19 papers total, none quantum**, and the only CFP quantum wording is a parenthetical inside a domain label. Structurally sound, statistically negligible.
- **IEEE eScience** — 2024 CFP promotes four key topics, none quantum.
- **HOTI** — 2026 CFP has no quantum entry; the 2025 program (9 papers) has none. Quantum-interconnect work goes to ICDCS and quantum-native venues.
- **DSN** — CFP *does* mention quantum twice under emerging computing paradigms, but no 2024–2026 main-track regular quantum paper could be verified. Scope without population; reconsider if evidence appears.
- **SoCC, Middleware** — no quantum main-track papers found.
- **ICSE / FSE / ASE / ISSTA** — ICSE's main research track has none; ICSE quantum content lives in the **Q-SE workshop** and in tutorials. ASE 2024 has one genuine main-track paper (quantum program testing via commuting Pauli strings), but honestly assessed, quantum-SE testing has essentially no bearing on HPC systems research. **LOW_PRIORITY.**
- **SPAA, ICPADS, HPCC** — no quantum papers or CFP wording found.
- **ICRC (IEEE Rebooting Computing)** — historically the natural "emerging paradigms" home, but it **no longer publishes conference proceedings**: ICRC 2025 full papers are journal-reviewed into *npj Unconventional Computing*. Structurally unlike the other venues; excluded, but this is the discontinuity in the emerging-paradigms lineage.
- **ISVLSI** — its quantum content is a dedicated **Quantum Workshop**, an excluded category.
- **Quantum-physics / quantum-information venues, explicitly ruled out** per the brief's instruction not to sweep in all quantum venues:
  - **QIP** — quantum information theory; talk/abstract-based, no systems proceedings.
  - **TQC** — complexity and theory; no HPC/parallel/systems content.
  - **APS March Meeting** — abstract-only physics meeting, no peer-reviewed proceedings.
  - **QEC Conference** — QEC theory and codes; the systems-side decoder work an HPC researcher needs appears at MICRO/ISCA/IISWC/ICCAD/HPCA instead.
  - **QTML** — quantum ML algorithms; no systems track.
  - **QCNC (IEEE Quantum Communications, Networking, and Computing)** — a genuine borderline case: engineering/systems-flavored rather than pure physics, with published accepted-paper lists. Rejected as duplicative of the QCE slot and centred on communications rather than HPC. Revisit only if a quantum-networking branch is added to the map.

---

## 5. Research-topic × venue matrix

**Legend.** `●●●` = a sustained thread, multiple confirmed main-track papers across years · `●●` = clearly present, ≥2 confirmed papers · `●` = present, isolated confirmed paper(s) · *(blank)* = none found in this survey · `?` = not verified at this venue.

**Blanks are deliberate and meaningful.** They have not been filled in speculatively.

### 5.1 HPC / parallel venues

| Topic | SC | ISC | ICS | ICPP | IPDPS | CCGrid | HiPC | Euro-Par | HPEC | Cluster | HPDC | PPoPP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Distributed / GPU statevector simulation | ●● | | ●● | ●● | ● | | ● | | ● | | | |
| Tensor-network simulation | ●● | | | | | ● | | | ● | | | |
| Stabilizer / sparse / decision-diagram simulation | | | ● | ● | | | | | | | | |
| Hybrid execution model / CPU-QPU coupling | | ●● | | | | ● | ● | ● | | | | |
| Scheduling / resource mgmt / QPU multiplexing | ● | ● | | ● | ● | ● | | | | | | |
| Workflow orchestration / HPC-QC middleware | ● | | | | | ●● | | ● | | | | |
| Compiler / circuit mapping / routing | ●● | ● | ●● | ● | | | ● | ● | ● | | | |
| Compiler IR / DSL / programming model | | ● | | | | | | | | | | |
| QEC decoding (systems contribution) | | | | | | | | | | | | |
| QEC architecture / FT resource estimation | ● | | | ● | | | | | ● | | | |
| Circuit cutting / partitioning | | | ● | | | | ● | | | | | |
| Multi-QPU / distributed quantum | ● | | | ● | | | | | | | | |
| Performance modeling / benchmarking | | ●● | | | | | | | | | | |
| Reliability / performance variability | ● | | | | ● | | | | | | | |
| **HPC-centre QPU integration & operations** | | **●●●** | | | | | ● | | | | | |
| Application workloads (chem / opt / QML) | ●● | ● | ● | ● | ● | | | ● | ●● | | | |
| Quantum control microarch / cryogenic I/O | | ● | | | | | | | | | | |

### 5.2 Architecture, compiler, systems and measurement venues

| Topic | ASPLOS | ISCA | HPCA | MICRO | CGO | PLDI | OOPSLA | OSDI | SIGMETRICS | EuroSys | IISWC | QCE | EDA¹ | ICDCS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Distributed / GPU statevector simulation | ●● | ●● | ● | | ● | | ●● | | ●● | | | ●● | ● | |
| Tensor-network simulation | | | | | | ● | | ● | | | | ●● | | |
| Stabilizer / sparse / decision-diagram simulation | ●● | | | | | | ●● | | | | | ●● | ● | |
| Hybrid execution model / CPU-QPU coupling | ● | ●● | | | | ● | | ●● | | | | ●● | | |
| Scheduling / resource mgmt / QPU multiplexing | ● | | | ● | | | | **●●●** | | | ● | ●● | ●● | ●● |
| Workflow orchestration / HPC-QC middleware | | | | | | | | ● | | | ● | ●● | | |
| Compiler / circuit mapping / routing | **●●●** | **●●●** | **●●●** | ●● | **●●●** | **●●●** | **●●●** | | | | | **●●●** | **●●●** | |
| Compiler IR / DSL / programming model | ● | ● | | | ●● | ●● | ●● | ● | | | | ●● | ● | |
| **QEC decoding (systems contribution)** | **●●●** | **●●●** | ●● | **●●●** | | | | | ● | ● | ● | ●● | ●● | |
| QEC architecture / FT resource estimation | **●●●** | **●●●** | ●● | ●● | ● | ● | | | | | | ●● | ●● | |
| Circuit cutting / partitioning | ● | | | | | | | ● | | | | ●● | ● | |
| Multi-QPU / distributed quantum | ●● | **●●●** | ● | ●● | | ● | | | ● | | | ●● | ● | ●● |
| Performance modeling / benchmarking | ● | ● | ● | | | | ● | | **●●●** | | **●●●** | **●●●** | ● | |
| Reliability / performance variability | ● | ● | | ● | | | | | ●● | | ● | ●● | | |
| HPC-centre QPU integration & operations | | | | | | | | | | | | ●² | | |
| Application workloads (chem / opt / QML) | ●● | ● | ● | ● | | ● | ● | | ● | | | **●●●** | ● | |
| Quantum control microarch / cryogenic I/O | ● | ●● | ●● | **●●●** | | | | | | | | ● | ●● | |

¹ EDA = DAC + ICCAD + DATE + ICCD aggregated.
² QCE main track only. The HPC-centre integration thread at QCE is overwhelmingly in the **WIHPQC workshop**, which is out of scope — see §4.1.

### 5.3 What the matrix shows

Three structural observations that follow directly from the blanks and the clusters:

1. **Compilation is the universal topic; everything else is venue-specific.** The "Compiler / circuit mapping / routing" row is the only one populated across every community. If a paper's contribution is compilation, venue choice is nearly free. Every other contribution shape has 2–4 realistic homes.
2. **QEC decoding is entirely absent from the HPC venues.** Look at the QEC-decoding row in §5.1: it is empty across SC, ISC, ICS, ICPP, IPDPS, CCGrid, HiPC, Euro-Par and HPEC. It is simultaneously the densest topic at ASPLOS, ISCA, MICRO and HPCA, and it has appeared at EuroSys and IISWC. **This is the clearest open opportunity in the map**: real-time QEC decoding is a throughput-bound, latency-bound, parallel classical computation — an HPC problem by every structural measure — and no HPC venue is currently publishing it.
3. **HPC-centre QPU integration and operations is a single-venue thread.** It exists at ISC and essentially nowhere else in main-track form. Everything similar elsewhere is workshop content (WIHPQC, SC-W, QUASAR). That is either a gap or a signal about what main-track PCs currently consider a research contribution rather than an experience report — probably both.

---

## 6. Recommended venue tiers

**These are relevance rankings for this specific research programme, not prestige rankings.** ISCA and MICRO outrank ISC and ICPP on general prestige; they do not outrank them here, because ISC and ICPP publish the QPU-in-HPC-centre and parallel-simulator threads that this programme is about.

### Tier 1 — census these; they define the research space
| Venue | Why Tier 1 |
|---|---|
| **SC** | The target venue. 7/4 papers, escalating CFP commitment (topic area renamed "Post-Moore & Quantum Computing" for SC26), and the first main-track QPU orchestration paper (2025). |
| **ASPLOS** | **Censused — see `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`.** 36 papers over three years (14/10/12), the largest quantum population of any venue in this survey; a sustained double-digit population every year; dedicated sessions all three years; 61% public-artifact rate. *(The "highest share anywhere, 7.9%" claim in the original row is withdrawn — corrected shares are 7.7% → 4.5% → 7.2%.)* |
| **ISC High Performance** | Only venue with a dedicated Quantum Computing submission track *and* the unique HPC-centre-integration research thread. Proportionally densest. |
| **ISCA** | Highest absolute session count; the FT/decoder/multi-QPU pivot from 2025 is the direction of interest. |
| **IEEE QCE (QSYS + QAPP tracks)** | Largest reservoir and the best early-warning sensor — problems appear here 12–24 months before SC/ASPLOS. Census as a *sensor*, with the workshop-exclusion rule applied rigorously. |
| **ICS** | Fastest-rising HPC venue: 0→2→5 with a named "Quantum Computing" session in 2026. |
| **SIGMETRICS** | Owns the performance-modeling/characterization branch outright (ScaleQsim, Anchor, ECCentric) with explicit standing CFP scope. |
| **OSDI** | Owns the quantum-OS / virtualization / QPU-multi-tenancy branch (QOS, HyperQ, qTPU). Closest existing literature to running a QPU as a shared centre resource. |
| **HPCA** | Two dedicated sessions in 2025 and 2026; 2026's decoder papers are the most transferable artifacts of the year. **Treat 2024 as a non-year.** |

### Tier 2 — strong secondary venues; census after Tier 1
**MICRO** (decoder hardware, control microarchitecture — the hardware end of the decoder thread) · **CGO** (explicit quantum scope, named sessions, and the strongest classical-compiler-methodology transfer) · **CCGrid** (the HPC-QC middleware/orchestration branch: Pilot-Quantum, FaaS workflow choreography) · **ICPP** (dedicated CFP track; parallel simulators and quantum-cloud scheduling) · **IPDPS** (reliable 1–2 papers/year; the only HPC venue with a QPU-multiplexing paper) · **HiPC** (new dedicated track naming "quantum HPC frameworks"; institutionalizing now) · **IISWC** (tiny volume, highest signal-to-noise: performance models, orchestrators, decoder benchmarks) · **OOPSLA** (the qblaze parallel sparse simulator; circuit optimization and synthesis) · **DAC** (densest EDA venue; distributed-QC co-design, FT compilation, decoder hardware) · **ICCAD** (QPU job scheduling, circuit knitting, microsecond decoders) · **EuroSys** (one paper, but exactly the right one — elastic QEC decoder provisioning, with public code)

### Tier 3 — watch; do not census yet
**Euro-Par** (clean 0→1→2 rise) · **DATE** (MQT quantum-classical compilation framework; LRZ connection) · **HPEC** (HPC-native, second-tier archival; excellent people/community tracker) · **ICDCS** (multi-QPU and quantum-cloud subset only) · **ICCD** (simulation acceleration; underrated) · **PLDI** (QVM, Cobble; selective monitoring) · **HPDC** (main track empty but QUASAR workshop growing) · **IEEE Cluster** (scope opened 2025; posters converting) · **SOSP** (OSDI's sibling; most likely next breakthrough) · **PACT** (non-monotonic scope; the 2026 CFP's *"Quantum-HPC interfacing"* is its most on-target wording yet, but volume has not followed) · **ISPASS** (scope confirmed, zero papers; IISWC's sibling) · **ACM Computing Frontiers** · **ASP-DAC** · **ACM SIGOPS ATC** (new venue, first edition Nov 2026)

### Not on the map
**PPoPP, CC, NSDI, USENIX ATC** (now ACM SIGOPS ATC — watch, don't census), **POPL** (theory only), **ICPE, MASCOTS, PASC, eScience, HOTI, DSN, SoCC, Middleware, SPAA, ICPADS, HPCC, ICSE/FSE/ASE/ISSTA, ICRC, ISVLSI**, and all pure quantum-physics / quantum-information venues (**QIP, TQC, APS March Meeting, QEC Conference, QTML, QCNC**).

---

## 7. Suggested research order

Full detail, with per-venue census instructions, is in the companion **`QUANTUM_HPC_RESEARCH_QUEUE.md`**. The short form:

**Wave 1 — establish the target and the two densest pools (venues 1–4).** SC → ASPLOS → ISC → ISCA. These four answer "what does a publishable Quantum-HPC paper look like at each of the two poles: the HPC pole and the architecture pole?"

**Wave 2 — the growth edge and the two branch owners (5–8).** ICS → IEEE QCE (QSYS) → SIGMETRICS → OSDI. Wave 2 is where the *newest* problems are, and where the scheduling/measurement branches live.

**Wave 3 — complete the HPC community and the decoder thread (9–14).** HPCA → MICRO → CGO → CCGrid → ICPP → IPDPS.

**Wave 4 — secondary and EDA (15–21).** IISWC → HiPC → EuroSys → OOPSLA → DAC → ICCAD → Euro-Par.

**Deferred / monitor only.** DATE, HPEC, ICDCS, ICCD, PLDI, HPDC, Cluster, SOSP, PACT, ISPASS, CF, ASP-DAC, SIGOPS ATC.

**Rationale for the ordering.** It is not prestige-ordered and not alphabetical. It front-loads (a) the venue being targeted, (b) the venues with the highest density of relevant papers, and (c) the venues that own a research branch nobody else publishes. IPDPS and ICPP sit in Wave 3 despite being prominent HPC venues because their yield is 1–3 papers a year; HPCA sits in Wave 3 despite Tier 1 status because its useful window is only 2025–2026 and its decoder thread overlaps ISCA's.

---

## 8. Evidence and sources

All URLs checked **2026-09-06**.

### 8.1 Core HPC
SC — [SC24 Papers CFP](https://sc24.supercomputing.org/program/papers/) · [SC25 Papers CFP](https://sc25.supercomputing.org/program/papers/) · [SC26 Papers CFP](https://sc26.supercomputing.org/program/papers/) · [SC26 Best Paper finalists](https://sc26.supercomputing.org/2026/08/announcing-best-paper-and-best-student-paper-finalists/) · [SC25 schedule](https://sc25.conference-program.com/) · publisher volumes via [Crossref REST API](https://api.crossref.org/) (`10.1109/SC41406.2024`, `10.1145/3712285`; workshop volumes `10.1109/SCW63240.2024`, `10.1145/3731599`)
ISC — [Research Paper CFP](https://isc-hpc.com/submissions/research-paper/) · [ISC 2024 Research Paper Committee](https://www.isc-hpc.com/research-papers-2024.html) · [ISC 2025 "Research Paper Session: Quantum Computing"](https://isc.app.swapcard.com/widget/event/isc-high-performance-2025/planning/UGxhbm5pbmdfMjU4OTMyMA==) · [ISC 2026 program](https://isc-hpc.com/program/schedule/) · volumes `10.23919/ISC.2024/2025/2026`
IPDPS — [IPDPS 2026 CFP](https://www.ipdps.org/ipdps2026/2026-call-for-papers.html) · volumes `10.1109/IPDPS57955.2024`, `IPDPS64566.2025`, `IPDPS65963.2026`
ICS — [ICS steering site](https://ics-conference.org/) · [ICS 2026 CFP](https://dipsa-qub.github.io/ICS2026-webpage/call-for/call-for-papers.html) · [**ICS 2026 program (Quantum Computing session)**](https://dipsa-qub.github.io/ICS2026-webpage/program/program.html) · volumes `10.1145/3721145` (ICS'25), `10.1145/3797905` (ICS'26); workshops `10.1145/3774895`
ICPP — [ICPP 2025 CFP](https://icpp2025.sdsc.edu/registration/call-for-papers) · [ICPP 2026 CFP](https://icpp2026.github.io/call-for-papers/) · [ICPP 2026 schedule](https://icpp2026.github.io/schedule/) · volumes `10.1145/3673038`, `10.1145/3754598`; workshops `10.1145/3677333`, `10.1145/3750720`

### 8.2 Parallel / distributed
PPoPP — [2024](https://conf.researchr.org/track/PPoPP-2024/PPoPP-2024-papers) · [2025](https://ppopp25.sigplan.org/track/PPoPP-2025-Main-Conference-1) · [2026](https://ppopp26.sigplan.org/track/PPoPP-2026-papers) · [CFP scope](https://www.sigarch.org/call-contributions/ppopp-2026/)
HPDC — [2024](https://hpdc.sci.utah.edu/2024/program.html) · [2025](https://hpdc.sci.utah.edu/2025/program.html) · [2026](https://hpdc.sci.utah.edu/2026/program.html) · [2026 CFP](https://hpdc.sci.utah.edu/2026/calls-cfp.html)
CCGrid — [2024 CFP](https://2024.ccgrid-conference.org/call-for-papers/) · [2025 research CFP](https://site.uit.no/ccgrid2025/research-paper/) · [2025 program PDF](https://site.uit.no/ccgrid2025/wp-content/uploads/sites/519/2025/05/program_ccgrid2025-44.pdf) · [2026 CFP](https://ccgrid2026.cdms.westernsydney.edu.au/cfp.html) · [2026 full program PDF](https://ccgrid2026.cdms.westernsydney.edu.au/assets/ccgrid2026-full-program.pdf) · [Pilot-Quantum code](https://github.com/radical-cybertools/pilot-quantum)
Cluster — [2024 CFP](https://clustercomp.org/2024/papers/) · [2024 program](https://clustercomp.org/2024/program/at_a_glance.html) · [2025 CFP](https://clustercomp.org/2025/papers/) · [2025 program](https://clustercomp.org/2025/program/at_a_glance.html) · [2026 CFP](https://clustercomp.org/2026/papers/)
Euro-Par — [2024 accepted papers](https://2024.euro-par.org/program/accepted-papers) · [2024 Track 3 topics](https://2024.euro-par.org/calls/topics/topic3/) · [2025 CFP](https://2025.euro-par.org/calls/papers) · [2026 accepted papers](https://2026.euro-par.org/fileadmin/2026/images/program/Euro-Par26_accepted_papers.html) · [2026 artifact community](https://zenodo.org/communities/europar_2026)
HiPC — [**HiPC 2026 CFP, Track 5 "Quantum Computing Systems and Applications"**](https://hipc.org/papers/) · [HiPC 2024 CFP](https://www.acm.org/articles/acm-india-bulletins/2024/hipc-2024-call-for-papers) · [2024 advance program PDF](https://www.hipc.org/wp-content/uploads/2024/12/Advance-Program-2024-For-Program-Handbook-2024-1.pdf) · volumes `10.1109/HiPC62374.2024`, `HiPC66333.2025`; workshops `HIPCW63042.2024`, `HiPCW66559.2025`
PACT — [**2024 CFP (official)**](https://pact2024.github.io/submit/) · [**2025 CFP (official) — no quantum language**](https://pact2025.github.io/submit/) · [**2026 CFP (official) — "Quantum-HPC interfacing"**](https://pact2026.github.io/submit/) · volume `10.1145/3656019` · *(the [SIGARCH PACT 2026 listing](https://www.sigarch.org/call-contributions/pact-2026/) is an abbreviated announcement that omits the quantum sub-bullet — do not use it as the CFP)*

### 8.3 Architecture
ISCA — [2024 program](https://www.iscaconf.org/isca2024/program/) · [2024 CFP](https://www.iscaconf.org/isca2024/submit/papers.php) · [2025 program](https://www.iscaconf.org/isca2025/program/) · [2025 CFP](https://www.iscaconf.org/isca2025/submit/papers.php) · [2026 program](https://iscaconf.org/isca2026/program/) · [2026 CFP](https://iscaconf.org/isca2026/submit/callforpapers.php) · [2026 trip report](https://www.sigarch.org/isca-2026-trip-report/)
MICRO — [MICRO-57 program](https://microarch.org/micro57/program/) · [MICRO-57 CFP](https://www.microarch.org/micro57/submit/papers.php) · [MICRO-58 program](https://www.microarch.org/micro58/program/) · [MICRO-58 CFP](https://www.microarch.org/micro58/submit/papers.php) · [MICRO-59 site](https://www.microarch.org/micro59/) · [MICRO-59 CFP](https://www.microarch.org/micro59/submit/papers.php) · volume `10.1145/3725843`
HPCA — [2024 program](https://www.hpca-conf.org/2024/program/main.php) · [2024 CFP](https://www.hpca-conf.org/2024/submit/papers.php) · [2025 program](https://hpca-conf.org/2025/main-program/) · [2025 CFP](https://hpca-conf.org/2025/call-for-papers/) · [2026 program](https://2026.hpca-conf.org/program/program-hpca-2026/) · [2026 main track](https://2026.hpca-conf.org/track/hpca-2026-main-conference) · [DBLP HPCA 2026](https://dblp.org/db/conf/hpca/hpca2026.html) · [BP-SF decoder code](https://github.com/Dies-Irae/BP-SF)
ASPLOS — [2024 program](https://www.asplos-conference.org/asplos2024/main-program/) · [2024 CFP](https://www.asplos-conference.org/asplos2024/cfp/index.html) · [2025 program](https://www.asplos-conference.org/asplos2025/program.html) · [2025 CFP](https://www.asplos-conference.org/asplos2025/cfp.html) · [2026 program](https://www.asplos-conference.org/asplos2026/program/index.html) · [2026 CFP](https://www.asplos-conference.org/asplos2026/cfp/index.html) · [BQSim code](https://github.com/IDEA-CUHK/BQSim) · [Micro Blossom code](https://github.com/yuewuo/micro-blossom) · [Promatch code](https://github.com/nargesalavi/Promatch) · [SWIPER code](https://github.com/jviszlai/swiper)

### 8.4 Compiler / PL / systems / measurement
CGO — [2024 TOC](https://www.conference-publishing.com/toc/CGO24) · [2025 papers](https://conf.researchr.org/track/cgo-2025/cgo-2025-papers) · [2025 TOC](https://www.conference-publishing.com/toc/CGO25) · [2026 papers](https://2026.cgo.org/track/cgo-2026-papers) · [CFP topics](https://conf.researchr.org/track/cgo-2027/cgo-2027-papers)
PLDI — [2024](https://pldi24.sigplan.org/track/pldi-2024-papers) · [2025](https://pldi25.sigplan.org/track/pldi-2025-papers) · [2026](https://pldi26.sigplan.org/track/pldi-2026-papers) · [2026 CFP](https://www.sigplan.org/announce/2025-09-24-pldi-2026/) · [QVM DOI](https://dl.acm.org/doi/10.1145/3729290)
POPL — [2024](https://conf.researchr.org/track/POPL-2024/POPL-2024-popl-research-papers) · [2025](https://conf.researchr.org/track/POPL-2025/POPL-2025-popl-research-papers) · [2026](https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers)
OOPSLA — [2024](https://2024.splashcon.org/track/splash-2024-OOPSLA) · [2025](https://2025.splashcon.org/track/OOPSLA) · [2026](https://2026.splashcon.org/track/oopsla-2026) · [qblaze entry](https://2025.splashcon.org/details/OOPSLA/53/qblaze-An-Efficient-and-Scalable-Sparse-Quantum-Simulator)
CC — [2024](https://conf.researchr.org/track/CC-2024/CC-2024-papers) · [2025](https://conf.researchr.org/track/CC-2025/CC-2025-main-conference) · [2026 TOC](https://www.conference-publishing.com/toc/CC26) · [**2026 CFP — explicit quantum scope, zero papers**](https://conf.researchr.org/track/CC-2026/calls)
OSDI — [OSDI 24](https://www.usenix.org/conference/osdi24/technical-sessions) · [OSDI 25](https://www.usenix.org/conference/osdi25/technical-sessions) · [**QOS**](https://www.usenix.org/conference/osdi25/presentation/giortamis) · [**HyperQ**](https://www.usenix.org/conference/osdi25/presentation/tao) · [**qTPU**](https://www.usenix.org/conference/osdi26/presentation/tornow) · [OSDI 26 CFP](https://www.usenix.org/conference/osdi26/call-for-papers)
SOSP — [2024](https://sigops.org/s/conferences/sosp/2024/accepted.html) · [2025](https://sigops.org/s/conferences/sosp/2025/accepted.html) · [2025 CFP](https://sigops.org/s/conferences/sosp/2025/cfp.html) · [2026](https://sigops.org/s/conferences/sosp/2026/accepted.html) · [NSF Quantum-OS workshop @ SOSP'24 (workshop — excluded)](https://www.sigarch.org/call-contributions/nsf-workshop-on-quantum-operating-systems-and-real-time-control-sosp-2024-and-micro-2024/)
EuroSys — [2024](https://2024.eurosys.org/accepted-papers.html) · [2025](https://2025.eurosys.org/accepted-papers.html) · [2026](https://2026.eurosys.org/papers.html) · [2026 CFP](https://2026.eurosys.org/cfp.html) · [Elastic QEC Decoders DOI](https://dl.acm.org/doi/10.1145/3767295.3803584) · [code](https://github.com/satvikmaurya/decoder-resources)
ATC / NSDI — [ATC editions 1992–2025](https://www.usenix.org/conferences/byname/131) · [ATC '25, final USENIX edition](https://www.usenix.org/conference/atc25) · [ATC discontinuation report](https://lwn.net/Articles/1020306/) · [**ACM SIGOPS ATC 2026 CFP**](https://sigops.org/s/conferences/atc/2026/cfp.html) · [ACM SIGOPS ATC 2026 home (date discrepancy)](https://sigops.org/s/conferences/atc/2026/) · [NSDI 24](https://www.usenix.org/conference/nsdi24/technical-sessions) · [NSDI 25](https://www.usenix.org/conference/nsdi25/technical-sessions) · [NSDI 26 spring](https://www.usenix.org/conference/nsdi26/spring-accepted-papers)
SIGMETRICS — [2024 CFP](https://www.sigmetrics.org/sigmetrics2024/call_for_papers.html) · [2024 accepted](http://sigmetrics.org/sigmetrics2024/accepted_papers.html) · [2025 CFP](https://www.sigmetrics.org/sigmetrics2025/call_for_papers.html) · [2025 accepted](https://www.sigmetrics.org/sigmetrics2025/accepted_papers.html) · [**2026 CFP**](https://www.sigmetrics.org/sigmetrics2026/call_for_papers.html) · [**2026 accepted**](https://www.sigmetrics.org/sigmetrics2026/accepted.html)

### 8.5 IEEE QCE
[QCE main site](https://qce.quantum.ieee.org/) · [**QCE26 Call for Technical Papers (track definitions)**](https://qce.quantum.ieee.org/2026/call-for-technical-papers/) · [**QCE26 Reviewing Guidelines PDF (paper categories, 40–50% target)**](https://qce.quantum.ieee.org/2026/wp-content/uploads/sites/13/2026/02/QCE26-Guidelines-Technical-Paper-Reviewing-V55-c.pdf) · [QCE26 Call for Workshops (4-page limit)](https://qce.quantum.ieee.org/2026/call-for-workshops/) · [QCE26 Call for Posters](https://qce.quantum.ieee.org/2026/call-for-posters/) · [QCE26 News (372 papers / 9 tracks)](https://qce.quantum.ieee.org/2026/news-and-updates/) · [QCE26 Technical Papers Schedule PDF](https://qce.quantum.ieee.org/2026/wp-content/uploads/sites/13/2026/08/QCE26-Technical-Papers-Schedule-V123.pdf) · [QCE25 Technical Papers Program](https://qce.quantum.ieee.org/2025/technical-papers-program/) · [**QCE25 All Accepted Technical Papers PDF**](https://qce.quantum.ieee.org/2025/wp-content/uploads/sites/12/2025/07/QC25-All-Accepted-Technical-Papers.pdf) · [**QCE25 QSYS Accepted PDF**](https://qce.quantum.ieee.org/2025/wp-content/uploads/sites/12/2025/07/QSYS-Accepted-Technical-Papers.pdf) · [**QCE24 Accepted Technical Papers PDF**](https://qce.quantum.ieee.org/2024/wp-content/uploads/sites/8/2024/07/QCE24-Accepted-Technical-Papers-QALG-QSYS-QAPP-QPHO-QNET-QTEM-QML.pdf) · [QCE25 proceedings TOC (volume partitioning)](https://www.proceedings.com/content/083/083032webtoc.pdf) · [QCE24 proceedings TOC](https://www.proceedings.com/content/077/077500webtoc.pdf) · [WIHPQC25 workshop (excluded, but the HPC-QC community hub)](https://www.hpcqc.org/wihpqc25) · [CORE ranking: QCE](https://portal.core.edu.au/conf-ranks/2325/) · [CORE ranking: SC](https://portal.core.edu.au/conf-ranks/77/) · [GraFeyn code](https://github.com/UmutAcarLab/grafeyn) · [IBM qe-compiler code](https://github.com/openqasm/qe-compiler)

### 8.6 Additional venues
DAC — [**Research topics DES6 Quantum Computing**](https://dac.com/2026/research-topics) · [Research manuscript submissions (20–25% accept)](https://dac.com/2026/research-manuscript-submissions)
ICCAD — [2026 CFP PDF](https://ieee-cas.org/files/ieeecass/2026-02/iccad-2026-cfp.pdf) · [2025 CFP PDF](https://ieee-ceda.org/files/ieeeceda/2025-03/iccad25-cfp_web-10%20(1).pdf)
DATE — [**D16 Design Automation for Quantum Computing**](https://date25.date-conference.com/call-for-papers) · [current CFP](https://www.date-conference.com/call-for-papers)
IISWC — [**2025 CFP (quantum under emerging workloads)**](https://iiswc.org/iiswc2025/cfp.html) · [2025 accepted papers](https://iiswc.org/iiswc2025/accepted-papers.html) · [2024 program PDF](https://iiswc.org/iiswc2024/assets/pdfs/iiswc24-program.pdf)
ICDCS — [**2024 CFP "Quantum Networks and Computing"**](https://icdcs2024.icdcs.org/call-for-papers/) · [2024 accepted](https://icdcs2024.icdcs.org/accepted-papers/) · [2025 detailed program](https://icdcs2025.icdcs.org/detailed-program/)
HPEC — [**CFP "Quantum and Non-Deterministic Computing"**](https://ieee-hpec.org/index.php/call-for-papers/)
ISPASS — [2026 CFP](https://www.sigarch.org/call-contributions/ispass-2026/) · [2025 accepted papers (zero quantum)](https://ispass.org/ispass2025/accepted-papers.php)
ASP-DAC — [2026 CFP](https://www.aspdac.com/aspdac2026/cfp/) · [2025 CFP](https://www.aspdac.com/aspdac2025/cfp/)
Computing Frontiers — [CF 2025](https://www.computingfrontiers.org/2025/)
Rejected venues — [ICPE 2025 accepted](https://icpe2025.spec.org/accepted-papers/) · [MASCOTS 2026 CFP](https://mascots26.iitis.pl/call-for-papers/) · [PASC 2025 papers](https://pasc-conference.org/editions/pasc25/program/papers) · [eScience 2024 CFP](https://www.escience-conference.org/2024/call-for-papers) · [HOTI 2026 CFP](https://hoti.org/2026/call-for-papers.html) · [DSN 2026 CFP](https://dsn2026.github.io/cfpapers.html) · [ICRC 2025 (no proceedings)](https://rebootingcomp.github.io/icrc2025/) · [SIAM proceedings policy](https://www.siam.org/publications/proceedings/) · [SIAM PP26](https://www.siam.org/conferences-events/past-event-archive/pp26/)

---

## Appendix A — Revised research taxonomy

The provisional taxonomy held up well. Four changes are warranted by what the literature actually contains.

```
Quantum-HPC Research
│
├── Hybrid execution models
│   ├── loose coupling
│   ├── tight coupling                        [ISCA Qtenon; ISC HPCQC measurement]
│   ├── iterative hybrid execution            [ASPLOS TreeVQA — shot reduction]
│   ├── task-parallel hybrid execution
│   └── ★ virtualization & multi-tenancy      [NEW — OSDI HyperQ, PLDI QVM]
│
├── Scheduling / resource management
│   ├── co-scheduling
│   ├── QPU multiplexing                      [IPDPS AQUA; OSDI QOS/HyperQ]
│   ├── malleability
│   ├── adaptive allocation
│   ├── multi-resource scheduling
│   └── ★ quantum-cloud / multi-tenant QPU    [NEW — ICS OpaQue, ICPP RL scheduler,
│         provisioning                         ICCAD latency scheduling, ICDCS CloudQC]
│
├── Runtime systems
│   ├── DAG/task runtime
│   ├── asynchronous execution
│   ├── dynamic backend selection
│   ├── heterogeneous resource management
│   └── ★ quantum operating systems           [NEW — OSDI QOS; the branch that did not
│                                              exist in the provisional taxonomy]
│
├── Performance modeling / workload characterization
│   ├── end-to-end performance
│   ├── bottleneck analysis
│   ├── scalability
│   ├── workload motifs
│   ├── ★ performance variability             [NEW — SIGMETRICS Anchor]
│   └── ★ classical-resource requirement      [NEW — ISC Camps et al.; QCE quantum
│         estimation for QC                     hardware roofline]
│
├── Classical quantum simulation
│   ├── statevector                           [SC Atlas; IPDPS ARM/SVE; ICPP cache blocking]
│   ├── tensor network                        [SC Surpassing Sycamore; CCGrid SWIFTN; HPEC TN-Sim]
│   ├── stabilizer                            [ICS quEStab]
│   ├── sparse representation                 [OOPSLA qblaze; QCE GraFeyn]
│   ├── ★ decision diagram                    [NEW — ICPP FlatDD; ASPLOS BQSim]
│   ├── ★ noisy / trajectory / density-matrix [NEW — SC NVIDIA batching; ISCA TUSQ,
│   │                                          computational reuse]
│   ├── ★ compression-assisted simulation     [NEW — ICS BMQSim]
│   ├── CPU/GPU
│   └── distributed / multi-GPU
│
├── Distributed quantum algorithms
│   ├── circuit cutting                       [ICS C-3PQ; ASPLOS QRCC; QCE scalability study]
│   ├── observable parallelism
│   ├── shot parallelism
│   ├── subcircuit execution
│   └── multi-QPU                             [ISCA SwitchQNet; SC inter-module mapping]
│
├── Compiler / IR / programming model         [the universal topic — every community]
│
├── ★★ QEC as a classical computing workload  [NEW TOP-LEVEL BRANCH — see note below]
│   ├── real-time decoding (throughput/latency)
│   ├── decoder hardware (FPGA/ASIC/cryogenic)
│   ├── parallel & window decoding
│   ├── decoder resource provisioning         [EuroSys elastic decoders]
│   ├── syndrome I/O and bandwidth
│   └── decoder benchmarking                  [IISWC decoder-bench]
│
├── Reliability / performance variability
│
├── Benchmarking
│
├── ★ HPC-centre QPU integration & operations [NEW — almost entirely an ISC thread:
│   ├── calibration & characterization in situ  calibration, telemetry, sys-sage topology,
│   ├── telemetry & monitoring                  HPCQC-tailored measurement]
│   ├── system topology & resource models
│   └── middleware & orchestration            [CCGrid Pilot-Quantum; SC Qonductor]
│
└── Application workloads
    ├── VQE · QAOA · QPE · QITE/Krylov
    ├── chemistry / materials
    ├── QML
    ├── ★ quantum linear algebra              [NEW — PLDI Cobble block encodings]
    └── others
```

**The one change that matters most: QEC deserves promotion to a top-level branch.**
In the provisional taxonomy, QEC appears only implicitly. In the actual 2024–2026 literature it is **the single densest topic** at ASPLOS, ISCA, MICRO and HPCA simultaneously, and it has now appeared at EuroSys, IISWC, ICCAD and DAC. More importantly for this programme, **real-time QEC decoding is structurally a classical HPC problem**: a latency-bounded, throughput-bounded, parallelizable classical computation that must keep pace with a physical device, with a hard bandwidth constraint at the cryogenic boundary. It is currently absent from every HPC venue. That combination — dense elsewhere, absent here, structurally an HPC problem — makes it the most defensible open research direction the map identifies.

Two secondary observations:
- **"Quantum operating systems" was not in the provisional taxonomy and now exists as a real branch** with OSDI-quality papers behind it (QOS, HyperQ). It is distinct from "runtime systems" because the contribution is multi-tenancy, isolation and fair-share — the classical OS concerns — rather than task orchestration.
- **"HPC-centre QPU integration and operations" is a real branch but is publishing almost entirely at ISC and in workshops.** Whether it becomes a main-track branch elsewhere is an open question and a thing to watch.

---

## Appendix B — Principles for the paper deep-dive phase

Recorded now so the deep-dive phase is consistent. **These are not applied in this Phase 1 document** — no paper here has been analyzed at this depth.

### B.1 Code and artifact cross-verification

When a public implementation exists, verify the chain:

```
paper claim → algorithm → implementation → experiment configuration → reported result
```

Tag every statement with its evidence level:

| Level | Meaning |
|---|---|
| `[paper]` | Stated in the paper text, figures or tables |
| `[code]` | Read directly from source code |
| `[artifact]` | From an artifact-evaluation package, container, or reproducibility appendix |
| `[documentation]` | From README, docs, or supplementary material |
| `[reconstruction]` | Derived by re-running or re-deriving it |
| `[inference]` | My reasoning — always marked, never presented as fact |

When the paper's description and the code disagree, classify the discrepancy:

| Verdict | Meaning |
|---|---|
| `CONSISTENT` | Code implements what the paper describes |
| `PARTIAL_MATCH` | Core mechanism matches; details, defaults or parameters differ |
| `MISMATCH` | Code does something materially different from the paper's description |
| `INSUFFICIENT_EVIDENCE` | Cannot be determined from available material |

**Hard rule: never invent implementation details that are not in the paper and not in the code.** If an implementation detail is unknown, record it as unknown. A plausible reconstruction is `[reconstruction]` or `[inference]`, never `[code]`.

Public code is **not** a paper-selection criterion — much of this field does not release code. But among otherwise comparable papers, one with a public artifact is worth more deep-dive time because the chain above can actually be closed.

### B.2 Reading performance claims strictly

A claim of "10× faster" is not a summarizable fact until these are known. Record each as answered or `UNSPECIFIED`:

- **Baseline** — against what, and is it a credible state-of-the-art baseline or a naive one?
- **Hardware scale** — CPU/GPU model, node count, core count, memory per node
- **Precision** — fp64 / fp32 / fp16 / mixed / complex64 vs complex128 (a major factor in statevector simulation)
- **Problem size** — qubit count, circuit depth, gate count, bond dimension, shot count
- **Preprocessing included?** — transpilation, contraction-order search, and index optimization are frequently excluded and frequently dominant
- **Communication included?** — or kernel-only timing on a single device
- **Initialization included?** — state allocation and memory setup can dominate at scale
- **Kernel-only or end-to-end?**
- **Simulator or real QPU?** — and if real hardware, queue/latency effects and calibration drift
- **Strong or weak scaling?** — and over what range
- **Variance** — number of runs, and whether variability is reported at all (particularly important on real QPUs, where SIGMETRICS' *Anchor* shows output performance varies temporally and spatially)

**Selection heuristic for Phase 2:** prefer papers that specify these clearly. A paper that reports its baseline, scale, precision and end-to-end boundary honestly is more useful than one with a larger headline number and an unspecified setup — both for learning and for later comparison.

---

## Appendix C — Methodology, limitations, and known gaps

### C.1 Method
Six parallel investigations, each verifying against official conference sites, official CFPs, official technical programs, and publisher proceedings (ACM DL, IEEE Xplore, Springer LNCS, USENIX, PACMPL/POMACS). Where a publisher site or program page was unreachable, the **Crossref REST API** was used, because it returns the exact `container-title` and DOI prefix of the volume a paper sits in — which is the most reliable available discriminator between a main-track volume and a workshop volume.

### C.2 Known gaps — these should be closed in Phase 2
1. **Artifact status is `UNKNOWN` for the large majority of papers.** The artifact pass was deliberately shallow. Confirmed public code was located for only about ten papers across the entire survey (BQSim, Micro Blossom, Promatch, SWIPER, BP-SF, decoder-resources, Pilot-Quantum, GraFeyn, qe-compiler, plus the MQT line). **Do not read `UNKNOWN` or `NO_PUBLIC_ARTIFACT_FOUND` as evidence that code does not exist.**
2. **ICS 2024 is "none found by keyword sweep", not a hand-counted zero.** The ACM DL TOC could not be walked page-by-page.
3. **Q-GEAR (ICPP 2025) is registered in Crossref under both the main and the workshop volume** with coherent page ranges in each. `STATUS_UNCLEAR` until checked against ACM DL.
4. **SC per-paper evidence is publisher-record-based, not schedule-based** — SC's proceedings pages are robots-disallowed to automated fetch.
5. **Three programs were not public as of 2026-09-06:** SC26 (schedule site returns 401), MICRO-59 (program page returns 404), and ACM SIGOPS ATC 2026 (notification 18 Sept 2026). IEEE Cluster 2026 (22–25 Sept), PACT 2026 (19–22 Oct), HiPC 2026 (16–19 Dec) and QCE26 (13–18 Sept) had not yet been held.
6. **QCE26 has no per-track "Accepted Technical Papers" PDF yet** — titles are currently obtainable only from the schedule PDF. Wait for the PDFs or the Xplore posting before censusing QCE26.
7. **The exact year HiPC introduced its quantum track (2025 or 2026) could not be pinned down** — the 2025 CFP page has been overwritten and Wayback was blocked.
8. **HPCA 2026 author attributions on the researchr program page were misaligned** and had to be corrected against DBLP/IEEE. Verify author lists from the publisher, not the program page, for that venue-year.

### C.3 Five census traps, collected
1. **HPDC's QUASAR workshop papers are deposited under the HPDC main proceedings container in Crossref.** Four papers would be false positives at face value. Separate by event date (the workshop day precedes the main track) and page-range discontinuity.
2. **HPCA's "Best of CAL" session** is an invited re-presentation of already-published *IEEE Computer Architecture Letters* papers — not main-track. Naive scraping overcounts HPCA 2024 by exactly one.
3. **PLDI's `[TOPLAS]` entries are journal-first presentations, and keynotes sit under the papers-track URL prefix** (`/details/pldi-2026-papers/…`). Both are easy false positives.
4. **QCE's proceedings mix technical papers, workshop papers, poster abstracts and program abstracts under one conference name in IEEE Xplore.** Page count does not separate short main-track papers (≤7 pp.) from QCE25-era workshop papers (~6–7 pp.). Only the official per-track PDF or the proceedings volume section heading settles it.
5. **Co-location confusion.** CGO, PPoPP, HPCA and CC share a week; ASPLOS 2025 was co-located with EuroSys. Verify each paper against its own venue's track page and proceedings volume — never attribute by week.

### C.4 Explicit non-findings
Per the brief's instruction that "this conference has almost no relevant papers" is itself a result: **PPoPP (0/121), CC (0/55), SOSP (0/185), NSDI (0), USENIX ATC (0/107), IEEE Cluster (0 main-track), HPDC (0/~91), ISPASS (0/28), ICPE (0), and Euro-Par 2024 (0/88) produced no qualifying main-track regular papers.** These counts were verified by full enumeration where the program was public, and no list anywhere in this document has been padded to make a venue look more active than it is.

### C.5 Independent verification pass

Ten load-bearing claims were re-checked against primary sources by a separate reviewer working from scratch. Results, recorded for transparency:

**Confirmed as written:** the ICS 2026 "Quantum Computing" session (name and 5-paper count exact); the ASPLOS CFPs containing no occurrence of "quantum" in 2024, 2025 or 2026 while running 2/2/3 dedicated quantum sessions; the CC 2026 CFP's two quantum bullets against zero accepted quantum papers; the two OSDI 2025 quantum papers sharing the "Scheduling and Resource Management" session; ScaleQsim at SIGMETRICS 2026 against zero quantum papers at SIGMETRICS 2024; and QCE26's "372 Technical Papers in 9 Tracks" with the officially stated 40–50% acceptance target.

**Corrected in this document:**
1. **PACT — the original finding was inverted and has been rewritten.** The claim that PACT retained quantum in 2025 and removed it in 2026 is wrong in both halves. The official CFPs (`pact2025.github.io/submit/`, `pact2026.github.io/submit/`) show quantum **absent in 2025** and **returning in 2026** as *"Quantum-HPC interfacing"*. The earlier reading came from SIGARCH's abbreviated PACT 2026 announcement, which omits the sub-bullet. This matters: it changes PACT from "declining" to "the most on-target CFP wording in the survey, with volume not yet following."
2. **HiPC 2024 — "no quantum language whatsoever" is not supportable and has been softened.** HiPC 2024's CFP did carry long-standing boilerplate quantum mentions inside its Algorithms and Architecture tracks. The defensible claim is the structural one: no *dedicated quantum track* in 2024, one in 2026. *(`2024.hipc.org` is under maintenance and web archives were blocked, so this rests on a CFP mirror plus matching boilerplate on a live older HiPC CFP page.)*
3. **USENIX ATC — reframed from "discontinued, replaced by a new venue" to "sponsor change".** The organizers explicitly assert continuity: *"ATC 2026 is now an ACM conference, but with the same community and scope as before."* Also: the ACM SIGOPS ATC 2026 site and its CFP give **different dates** (15–18 vs 16–18 November), unresolved; the venue is Hong Kong.
4. **SC26's rename is escalating visibility, not new eligibility** — "Quantum computing" was already an explicit bullet inside the Post-Moore area in SC24 and SC25. Caveat added.
5. **The OSDI 2025 virtualization paper's title is "Quantum Virtual Machines"; HyperQ is the system inside it.** Authors span U. Maryland, Columbia and Toronto — not Columbia alone.
6. **CC paper counts corrected** to 22 / 17 / 16 for 2024 / 2025 / 2026 (was 21 / 17 / 18); the three-year total is 55, not 56.
7. **ScaleQsim is SeoulTech-led with LBNL co-authors**, not an LBNL paper.

**Two additional cautions surfaced by the verification pass:**
- `asplos2025/program/` (with a trailing slash) silently serves the **2026** program. The correct ASPLOS 2025 URL is `asplos2025/program.html`.
- PACT 2024's official section heading is misspelled in the original — *"PACT for Quantum and Neurmorphic"*. Quote it as-is or mark it `[sic]`.

### C.6 Phase 2 SC census — what it verified and what it changed (2026-09-06)

The Phase 2 census of SC 2024 and SC 2025 (`SC_2024_2025_QUANTUM_HPC_CENSUS.md`) re-derived this venue's numbers from scratch, by exhaustive enumeration of both publisher volumes rather than keyword sampling.

**Confirmed unchanged:** the counts **7 (SC24)** and **4 (SC25)**; the SC25 contiguous-block claim (pp. 728–788); the `SC41406`/`SCW63240` and `3712285`/`3731599` discriminators; and all five SC25 classical-quantum-chemistry false positives. Completeness was proved two ways — SC24's DOI run is contiguous `.00001`–`.00114` with `.00115` returning 404, and SC25's 144 main-volume papers paginate **without a single gap or overlap across pp. 1–2265**.

**Changed in this document:**
1. SC24's "two consecutive session blocks" → **three sessions** (*Quantum and Approximate Computing I / II / III*, 3/2/3 talks), with the `.00078` HPAC-ML session-name trap documented.
2. SC25's Papers-track topic tag corrected — the previously recorded string belongs to the **Exhibitor Forum** taxonomy.
3. SC25's Gordon Bell block corrected from pp. 1–59 to **pp. 1–136 (11 papers)**; one false-positive title completed.
4. Volume totals and quantum shares added (**SC24 7/99 = 7.1%**; **SC25 4/137 = 2.9%, 22% acceptance**), plus SC24's two Best Student Paper Finalists and SC25's session chair.
5. Artifact status upgraded from `UNKNOWN` to the verified matrix — **7 of 11 public, 6 repo-verified `CONSISTENT`, 4 Zenodo deposits**.
6. MPS quantum-kernel paper re-attributed: **HSBC first author** with Quantinuum co-authors.

**The census's own headline finding, for this document's purposes:** SC does not apply one definition of "HPC contribution" to quantum work. It has at least **four acceptance pathways**, ranging from "HPC *is* the contribution, quantum is merely the workload" (Atlas) down to "the HPC content is the scarce resource consumed and the artifact released" (QDockBank, which reports **no classical hardware at all**). **"SC accepted it" therefore does not by itself imply "it contains an HPC contribution"** — a caveat that should be carried into every subsequent venue census in this programme.

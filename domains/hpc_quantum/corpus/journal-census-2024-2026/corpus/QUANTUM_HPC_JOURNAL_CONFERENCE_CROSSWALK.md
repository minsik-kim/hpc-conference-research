# QUANTUM_HPC_JOURNAL_CONFERENCE_CROSSWALK

**Where do the conference branches accumulate in the journals?**

Compiled 2026-09-17 (KST). Reads the 2024–2026 eight-journal census
(`QUANTUM_HPC_JOURNAL_CENSUS_2024_2026.md`, 89 included original-research papers) against the
existing conference corpus in this domain: the SC 2024–2025 census (11 papers), the ASPLOS 2024–2026
census (36 papers) and the 21-venue `QUANTUM_HPC_VENUE_MAP.md`.

**Scope limit.** The conference side of this comparison is only as complete as the conference corpus
is. SC and ASPLOS are censused; ISC, ISCA, ICS, HPCA, MICRO, QCE and the rest are **queued and not
performed** (`RESEARCH_STATUS.md`). Every statement below that involves an uncensused venue is
therefore a `POSSIBLE_CROSSOVER` or an `OPEN_QUESTION`, never a finding. No conference count is
revised here.

---

## 1. The correspondence hypotheses, tested

The brief proposed four venue↔journal correspondences. Here is what the corpus actually supports.

| Proposed correspondence | Verdict | Evidence |
|---|---|---|
| SC / ICS / ISC ↔ **FGCS / TPDS / JPDC** | **PARTIALLY SUPPORTED — and the partition inside it matters more than the correspondence** | FGCS carries the HPC-centre thread in full (12 `Q_IN_HPC` papers, runtime/orchestration/workflow/scheduling). TPDS carries exactly two papers, both cluster-level simulation. JPDC carries none. The HPC-journal side of this pairing is **FGCS alone**; TPDS is a simulation-only channel and JPDC is empty. |
| ISCA / HPCA / MICRO / ASPLOS ↔ **TC / TACO / TQE** | **SUPPORTED IN SHAPE, NOT IN DENSITY** | The architecture-venue branches do reappear in these three journals — QEC classical processing (TQE 4, TACO 1), architecture & control (TQE 8, TC 0 but 3 FPGA-substrate papers), multiprogramming and shared-QPU scheduling (TACO 3). But ASPLOS alone published 36 quantum papers in three years against TC's 6 and TACO's 4. The architecture community's quantum output stays at its conferences. |
| CGO / DAC / ICCAD ↔ **TCAD / TACO** | **STRONGLY SUPPORTED for TCAD** | TCAD is the compilation journal of this corpus: 7 of 12 inclusions and 9 of 24 included-plus-borderline records are mapping/routing/scheduling/compilation. TACO's compilation work (4 of 4 records) is compilation *for a shared resource*, which is a different argument. |
| QCE / QSW ↔ **TQE / TQC** | **SUPPORTED** | TQE and TQC hold 45 of 89 included papers (51%). Their subject mix — control systems, QEC classical processing, simulation engines, multi-QPU compilation, benchmarking — matches the QCE QSYS track headings recorded in the venue map (Real-Time QEC Decoding, Distributed Quantum Systems, Scalable Quantum Circuit Simulation, Quantum Systems & Resource Management, Runtime Workflows & Compilation Reuse) closely enough that the correspondence is the cleanest of the four. QCE itself remains uncensused, so this is `POSSIBLE_CROSSOVER`, not a verified lineage. |

---

## 2. Branch-by-branch crosswalk

| Branch | SC 2024–25 (11 papers) | ASPLOS 2024–26 (36 papers) | Journals 2024–26 (89 papers) | Reading |
|---|---|---|---|---|
| **Classical simulation of quantum circuits** | **4 of 11 — the largest SC branch** (Atlas, Surpassing Sycamore, MPS Kernels, PTSBE) | **1 of 36 — the smallest ASPLOS branch** (BQSim) | **22 of 89 (25%)** — TQC 7, FGCS 4, TQE 3, TCAD 3, TC 3, TPDS 2 | The SC/ASPLOS asymmetry does **not** reproduce in the journals. Journals take simulation from every level of the stack and from both communities. This is the branch where journals are least like either conference. |
| **Compilation / mapping / routing** | 3 of 11, all three arguing compile-time scalability | 10 of 36, only 2 arguing compile-time scalability | **38 of 89 (43%) — the dominant journal branch** | Compilation is the journal literature's centre of gravity, roughly double either conference's share. The journals absorb the volume that ASPLOS's page budget cannot. |
| **QEC as a classical computing workload** | **1 of 11**, and that one is reliability characterisation, not decoding | **11 of 36 (31%) — the largest ASPLOS branch** | **8 of 89 (9%)**, and **all 8 in quantum-native journals** (TQE 4, TQC 3, TACO 1) | The conference corpus's central `VENUE_GAP` — decoding dense at architecture venues, absent from SC — **persists on the journal side as a `JOURNAL_GAP`**. Zero decoder papers in FGCS, TCAD, TC, TPDS, JPDC. |
| **Resource management / scheduling / orchestration** | 1 of 11 (Qonductor) | 1 of 36 (RESCQ, real-time QEC scheduling) | **28 of 89** across `qpu_scheduling_resource_mgmt` (14) and `quantum_runtime_orchestration` (14), concentrated in FGCS (12) | **The sharpest single result of this crosswalk.** A branch that is one paper per venue at both conferences is the second-largest journal branch. Long-form journals are where scheduling, orchestration and resource management actually accumulate. |
| **HPC-QPU integration & operations** | 0 in the SC main track (the venue map places this thread at ISC) | 0 | **8 of 89**, 5 of them in FGCS, plus 7 `hybrid_workflow` records (5 FGCS) | The ISC-owned branch identified in the venue map has a journal home, and it is FGCS. |
| **Multi-QPU / modular / distributed QC** | 1 of 11 (DQTetris, inter-module mapping) | 3 of 36 (MECH, COMPAS, million-qubit architecture) | **13 of 89** — TQE 4, TQC 3, TCAD 2, FGCS 2, TC 1, TACO 1 | Genuinely shared; the only branch with no clear owner on either side. |
| **Circuit cutting / reconstruction** | 0 | 1 of 36 (QRCC) | 5 of 89 — TQE 3, FGCS 1, TACO 1 | Small but present in both; TQE is its journal home. |
| **Benchmarking / performance modeling** | (cross-cutting; SC census treats artifacts separately) | (cross-cutting) | **20 of 89**, TQE 6, TQC 6, FGCS 5 | Journals give performance modelling and benchmarking a standing home that neither censused conference does. |
| **Architecture & control** | **0 architecture papers in 11** (SC census, §10.1) | 11 of 36 propose hardware or machine organisations | **17 of 89**, TQE 8, FGCS 3, TCAD 3 | TQE is where architecture-shaped quantum systems work lands in journal form. |
| **Application / dataset** | 2 of 11 (LEXIQL, QDockBank) | 6 of 36 (QML, variational, mitigation) | **3 of 89** (`scientific_workflow_application`, all FGCS) | The application pathway barely exists in the journals under this corpus's gates — application-accuracy papers are excluded by design, so this row is a scope artefact as much as a finding. |

---

## 3. The four research questions this crosswalk can answer

### 3.1 Do journal contributions differ in kind from conference contributions?

**Yes, and along one axis in particular: the object of the contribution.**

The ASPLOS census established that ASPLOS rewards *a designed mechanism or abstraction* and SC
rewards *a measured cost that falls*. The journals in this corpus reward a third thing:
**a described and evaluated system**, with scheduling, orchestration and resource management as its
subject matter far more often than either conference.

The evidence is the scheduling/orchestration row above — 1 paper at SC, 1 at ASPLOS, 28 in the
journals. Long-form venues give room for the workflow, the middleware layer, the resource model and
the operational context that a 10-page conference paper has to cut. That is the answer to the brief's
question *"does workflow/runtime/resource management appear more often in long-form journals?"*:
it does, by a factor that is not marginal.

### 3.2 Is QEC classical-workload research architecture-centric in journals too?

**Yes, and more narrowly than at the conferences.** All eight journal QEC records are in quantum-native
venues. TQE's four are an FPGA distributed Union-Find decoder, a cryogenic SFQ coprocessor, a QEC
controller benchmark and a flag-sharing syndrome-extraction study; TQC's three are qLDPC memory
architecture, parallel minimum-distance computation and related; TACO's one is surface-code compilation
for platform throughput. None appears in a parallel-computing or HPC journal.

The ASPLOS census had already complicated the "decoding is dense at architecture venues" premise by
showing the decoder-microarchitecture line is exactly two ASPLOS papers and leaves after 2025. The
journal evidence is consistent with that: the decoder work is not migrating to journals either. What
this corpus can say is `JOURNAL_GAP` — the work is not in these eight journals' HPC-facing titles.
What it cannot say is anything about whether the problem is unaddressed; the venue map places active
decoder work at ISCA, MICRO, HPCA, EuroSys, IISWC, ICCAD and DAC, none of which is censused.

### 3.3 Where does distributed quantum simulation get published?

**All three of TPDS, TC and FGCS — but at different layers, and TQC more than any of them.**
See `QUANTUM_HPC_JOURNAL_MAP.md` §2.5. The short answer:

- cluster/communication level → **TPDS** (2 papers, both 2026)
- engine level (multi-GPU state vector, parallel decision diagrams, tensor networks) → **TQC** (7)
- representation level (decision diagrams, gate fusion, tensor-network contraction) → **TCAD** (3)
- substrate level (FPGA, storage hierarchy) → **TC** (3)
- named-machine level (50 qubits on an exascale system) → **FGCS** (4)

### 3.4 How are compiler/mapping papers split between TCAD, TACO and TQC?

- **TCAD** takes the EDA-shaped work: mappers, routers, schedulers, partitioners, with the classical
  compilation cost or the multi-chip communication cost as the objective. It is the branch owner.
- **TQC** takes the multi-core/multi-QPU and toolchain-shaped work: mapping for multi-core
  architectures, distributing-and-routing with execution-time objectives, end-to-end QASM compilation
  frameworks.
- **TACO** takes compilation *for a shared machine*: multiprogramming partitioning, cutting plus
  mapping across heterogeneous QPUs, surface-code compilation aimed at platform throughput, offline
  multi-version compilation with runtime dispatch.
- **TQE** takes compilation with a control-plane or architecture co-design attachment (zoned
  architectures for atom arrays, circuit packing and scheduling on trapped ions).

The distinguishing question is not the algorithm but the **objective function**: classical compile
cost (TCAD), execution time across processors (TQC), machine throughput and utilisation (TACO),
architecture co-design (TQE).

---

## 4. Conference-extension lineage — what could not be established

The census records **zero `CONFIRMED_EXTENSION`** relationships across all 89 included papers.
Four records carry `RELATED_LINEAGE` with stated evidence:

| Journal record | Related conference work | Evidence |
|---|---|---|
| TACO `10.1145/3631525` QuCloud+ | QuCloud, HPCA 2021 | shared lead author, `+` naming over a named predecessor system |
| TACO `10.1145/3760783` Ecmas+ | a predecessor *Ecmas* | `+` naming over a named predecessor system |
| TQC `10.1145/3837861` QASMTrans | arXiv:2308.07581 | arXiv record notes substantial text overlap |
| (one further TQC/TCAD record) | — | see per-journal files |

Every other record is `UNKNOWN`. This is an **evidence limitation, not a finding**: the front-matter
footnote where "an earlier version of this paper appeared at …" is normally printed was not reachable,
because ACM article pages returned HTTP 403 and IEEE Xplore was unreachable from the research
environment.

**Consequence for any later analysis.** Until this is closed, the 89 journal papers and the 47
conference papers (SC 11 + ASPLOS 36) **must not be summed** into a single count of independent
contributions to the research landscape. The overlap is unmeasured. Recorded as
`INSUFFICIENT_EVIDENCE` and as the highest-priority follow-up in `FOLLOW_UP_CANDIDATES.md`.

---

## 5. Observations carried forward, in the permitted vocabulary

- `JOURNAL_GAP` — QEC classical processing (decoder acceleration, decoder scheduling, syndrome
  compression) appears in zero papers across FGCS, TCAD, TC, TPDS and JPDC, 2024–2026.
- `JOURNAL_GAP` — `Q_FOR_HPC` (quantum accelerating a classical HPC workload) is 3 of 89 papers.
- `UNDERREPRESENTED_IN_THIS_CORPUS` — `Q_IN_HPC` outside FGCS: 11 papers across the other seven
  journals combined.
- `UNDERREPRESENTED_IN_THIS_CORPUS` — GPU-based simulation is absent from TQE's retained set despite
  TQE holding the largest included population.
- `POSSIBLE_CROSSOVER` — the scheduling/orchestration concentration in FGCS against its
  one-paper-per-venue presence at SC and ASPLOS.
- `POSSIBLE_CROSSOVER` — QCE QSYS ↔ TQE/TQC, testable once QCE is censused.
- `OPEN_QUESTION` — whether the 2026 dip at FGCS (7), TQE (6) and TCAD (1) is real or an artefact of
  a partial year plus IEEE Early Access records that carry no retrievable abstract. TCAD's 2026 figure
  is demonstrably depressed by three `INSUFFICIENT_EVIDENCE` records.
- `OPEN_QUESTION` — whether the NISQ → FTQC/system-integration shift that the ASPLOS census observed
  across 2024–2026 is visible in the journals. The FGCS sub-census reports a within-journal
  trajectory from position papers (2024) to software stacks (2025) to measured systems on named
  machines (2026); whether that generalises across the eight journals is `INSUFFICIENT_EVIDENCE` at
  n=89 over a partial third year.

No entry above is promoted beyond `CANDIDATE` status, and none is a novelty claim. Any promotion must
go through `governance/RESEARCH_GAP_RULES.md`.

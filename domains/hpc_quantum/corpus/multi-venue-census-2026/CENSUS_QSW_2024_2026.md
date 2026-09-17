# IEEE QSW 2024–2026 — Quantum-HPC Regular-Paper Census

**Censused 2026-09-17.** Method, tags and exclusion rules: `METHODOLOGY.md`.
**No Phase-1 seed list existed for this venue** — it was built from scratch, which also means there
was no anchoring bias to fight.

## 1. Why this venue needs category work before anything else

QSW runs under the **IEEE World Congress on Services / IEEE SERVICES** umbrella alongside sibling
conferences. Umbrella events blur paper categories badly, and QSW blurs differently **in each of the
three years**. Establishing the category taxonomy is therefore a prerequisite, not a formality.

### Page limits, from the official Information-for-Authors pages `[official-CFP]`

**2024 and 2025 are identical:**

| Category | Limit (verbatim) |
|---|---|
| **Regular** | "7 to 10 pages for the main contents … **with additional pages for appropriate references**" |
| **Short** | "4 to 6 pages for the main contents … **with additional pages for appropriate references**" |
| **Work-in-Progress** | "up to 3 pages (**including** main contents and references)" |

The QSW 2025 CFP states three categories: *"full, short, or work-in-progress"*.

**The irreducible ambiguity:** because references are *excess* to the main-content count for **both**
regular and short papers, a **7-page total is genuinely ambiguous** — either a minimum-length regular
paper or a maximum-length short paper. Page count alone cannot discriminate in that band. Banding
rule applied here, stated so it can be audited: ≤3 pp. → WIP; 4–6 pp. → SHORT; **7 pp. → BOUNDARY /
`STATUS_UNCLEAR`**; 8–12 pp. → REGULAR. The boundary band is not small — 3 of 17 main-track items in
2024 and 6 of 28 in 2025, up to a fifth of the population. **The three 2024 boundary items are**
*Efficient Encodings of the Travelling Salesperson Problem for VQAs* (pp. 81–87), *Stripping Quantum
Decision Diagrams of their Identity* (pp. 168–174) and *AdvQuNN* (pp. 175–181); only the second is
Quantum-HPC relevant, and it is recorded in §3.

### Additional category hazards, one per year

- **2024 — invited symposium papers bound into the front of the volume.** QSW 2024 ran **QSWUtil**
  ("Symposium on Quantum Software: Towards Quantum Utility in the NISQ Era"), whose page states
  verbatim that *"Accepted **invited** papers will be published in the Proceedings of the 2024 IEEE
  International Conference on Quantum Software."* The official program distinguishes them with a
  separate ID namespace (`QSW_SYM_nn` vs `QSW_CON_*`), but **the proceedings TOC does not**. Because
  the volume is ordered **chronologically by program** and the symposium ran on day 1, these sit at
  **pp. 1–23, the front of the volume** — so the usual "extras are at the back" heuristic fails here.
- **2025 — four non-QSW papers bound into the back.** researchr lists **32** entries; the official
  program lists **28**. The four extras (pp. 257–280) are a Kafka/IoT tuning paper, a geo-distributed
  microservice deployment paper, an interface-definition-language paper and an edge-ML fault-tolerance
  benchmark — **sibling SERVICES-congress papers**, each exactly 6 pp., in no QSW session. Ironically
  they are the most "systems" papers in the volume and are not quantum at all: a relevance-first
  screen that skipped category work would have pulled them in.
- **2026 — categories are explicit, and this is the gold standard.** The official program labels
  every paper `QSW_REG_nn` or `QSW_SHT_nn`. No WIP, symposium, poster or vision items appear.

**In all three years the official program, not the proceedings TOC, is the authoritative category
source** — and only in 2026 does the program encode category explicitly.

## 2. Population and denominators

| Year | Volume items | Main-track papers | **Regular (confident)** | Boundary 7 pp. | Short | WIP | Excluded by category | Method | Count status |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 2024 (Shenzhen, 7–13 Jul) | 21 | 17 | **13** | 3 | 0 | 1 | 4 (invited symposium) | `PUBLISHER_TOC_ENUMERATED` + partial `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` (volume); `TOTAL_COUNT_UNVERIFIED` (regular/short split) |
| 2025 (Helsinki, 7–12 Jul) | 32 | 28 | **17** | 6 | 5 | 0 | 4 (non-QSW volume-mates) | `PROGRAM_ENUMERATED` (authoritative) + `PUBLISHER_TOC_ENUMERATED` | `TOTAL_COUNT_VERIFIED` (28-paper program); `TOTAL_COUNT_UNVERIFIED` (split) |
| 2026 (Sydney, 13–18 Jul) | unknown | 27 | **17** | n/a | 10 | 0 | 0 | `PROGRAM_ENUMERATED` | `TOTAL_COUNT_VERIFIED` (program); **`TOTAL_COUNT_UNVERIFIED`** (publisher TOC not retrieved) |

**2024** — 21 entries tile **pp. 1–181** contiguously with zero gaps or overlaps. DOI prefix
`10.1109/QSW62656.2024.*`, established from an institutional record matching researchr exactly.
**2025** — 32 entries reconstruct a perfect tiling over **1–280** once two entries with corrupt page
metadata are placed in the two 12-page gaps (48–59 and 104–115); which of the two occupies which slot
is `[inference]` and nothing depends on it. DOI prefix `10.1109/QSW67625.2025.*`.
**2026** — the conference **has taken place** and its program is final (rooms, chairs, no TBDs), and
an IEEE Xplore conference-home record for the proceedings exists (`conhome/11662132`), but the TOC
could not be retrieved (Xplore 418; no researchr page — it 404s; CSDL returned page chrome only).
**So 2026 has no page ranges, no page-block analysis, and no second source shape** — the weakest year
of the three. Its category work is nonetheless the strongest, because the program IDs are explicit.

Sessions 2026: S1 Architecture-Aware Compilation (3 REG) · S2 Optimization and Complexity (3 REG) ·
S3 Quantum Machine Learning (3 REG) · S4 Software Systems and Workflows (3 REG) · S5 Performance and
Reliability (3 REG) · S6 Analysis/testing/debugging (1 REG + 3 SHT) · S7 Applications (1 REG + 3 SHT)
· S8 Emerging Methods (4 SHT).

*One provenance curiosity recorded:* a 2025 program item carries the ID `CON_REG_25` rather than the
`QSW_nn` used by the other 27 — apparently routed into QSW from the congress-wide regular pool. It is
in a QSW session and is counted, with the provenance flagged.

## 3. Relevant papers

| Year | Regular denominator | Relevant | Rate | Plus boundary-band relevant |
|---|---:|---:|---:|---|
| 2024 | 13 | **6** | 46% | +1 (Stripping QDD, 7 pp.) |
| 2025 | 17 | **5** | 29% | +1 (trapped-ion shuttling, 7 pp.) |
| 2026 | 17 | **9** | 53% | — |

### QSW 2024 — 6 of 14

**1 · Accelerating Decision Diagram-based Multi-node Quantum Simulation with Ring Communication and
Automatic SWAP Insertion** — Yusuke Kimura (Fujitsu), Shaowen Li, Hiroyuki Sato, Masahiro Fujita
(U. Tokyo) · pp. 107–115 (9 pp., REGULAR), Xplore doc 10646511, arXiv 2405.09033 · `HPC_FOR_Q`,
`FUTURE_WORKLOAD` · **SOFTWARE_SIMULATION on REAL_HARDWARE** · Artifact
`NO_PUBLIC_ARTIFACT_FOUND` · GENERAL

**The most HPC-shaped paper QSW has published.** MPI ring ("bucket relay") communication plus
automatic SWAP insertion for QMDD decision-diagram simulation across supercomputer nodes.
**Simulation detail** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §5): representation is **QMDD**
as adopted by DDSIM; node counts are restricted to powers of two up to 256; local qubits are
node-resident while global qubits force inter-node traffic; the ring replaces broadcast, measured at
**10–20% faster for Shor** and **~6× faster than broadcast** for random circuits; two SWAP-insertion
variants (v1 preserves qubit order, v2 minimizes swap count).
**Numbers with context:** Wisteria-O (U. Tokyo), **A64FX 48 cores @ 2.2 GHz, Tofu Interconnect-D**.
The **26×** is not a generic result — it is **38-qubit Shor (factoring 511, 400,123 gates) at 256
nodes with ring + v1 versus single-node execution, 3,881 s → 147 s**, the same run as the "38-qubit
Shor in 147 s" claim. **Strong scaling, and non-monotonic:** 20-qubit QCBM (761 gates) is fastest at
32–64 nodes and *slower* at 128 and 256 — communication overhead overtakes the DD's node sharing.
**This is the corpus's one direct measurement of a distributed-scaling crossover going the wrong
way**, and it is the clearest evidence in the census that "more nodes" is not monotonically good for
this workload class.
*Artifact note:* the paper states "We will disclose our GitHub URL after the double-blind review
process." **No repository has appeared.**

**2 · Q-Profile: Profiling Tool for Quantum Control Stacks applied to the Quantum Approximate
Optimization Algorithm** — Koen J. Mesman et al.
(all Qblox, Delft) · pp. 116–124 (9 pp., REGULAR), Xplore doc 10646547, arXiv 2303.01450 ·
`Q_IN_HPC`, `HPC_FOR_Q` · **emulator / hardware-in-the-loop** (Qblox Cluster driving virtual transmon
qubits, 4–14 qubits, 1 Gbps Ethernet to an Intel i5 host) · Artifact **`PUBLIC_CODE`** — ships in the
open-source Quantify/Quantify-Scheduler stack (`https://gitlab.com/quantify-os/quantify-scheduler`)
· NISQ
Instruments a heterogeneous CPU↔instrument pipeline to attribute wall-clock latency, then removes the
two dominant costs it finds: **passive qubit reset (1.40×)** and **host↔control-stack communication
overhead (a further 1.37× from parallel module initialization)**. This is classical systems
performance engineering applied to the control stack — and the closest thing in the census to
telemetry for a QPU's classical control path.

**3 · Deep Reinforcement Learning Strategies for Noise-Adaptive Qubit Routing** — Gonçalo Pascoal,
João Paulo Fernandes, Rui Abreu (U. Lisbon / INESC-ID) · pp. 146–156 (11 pp., REGULAR),
**DOI `10.1109/QSW62656.2024.00030`** (verified) · `HPC_FOR_Q` · **classical + simulator scoring** ·
Artifact `UNKNOWN` · NISQ. PPO agents perform calibration-aware routing across five IBM topologies:
**up to 37.3% fewer additional two-qubit gates** and **up to 26.8% higher estimated success
probability** vs Qiskit's best routing algorithm.

**4 · Towards Application-Aware Quantum Circuit Compilation** — Nils Quetschlich, Lukas Burgholzer,
Robert Wille (TU Munich / SCCH) with BMW Group and LMU · pp. 135–142 (8 pp., REGULAR),
arXiv 2404.12433 · `HPC_FOR_Q` · **noisy simulator** (ibmq_quito 5q, nairobi 7q, montreal 27q;
4/6/8-qubit instances) · Artifact **`PUBLIC_CODE`**
`https://github.com/cda-tum/mqt-predictor/tree/quantum_generative_modeling` · NISQ
Drives compilation by an **application-level** figure of merit rather than circuit-level proxies
(gate count, depth), inside an automated search over compilation passes.

**5 · Bounding Rounding Errors in the Simulation of Quantum Circuits** — Jonas Klamroth,
Bernhard Beckert (FZI/KIT `[inference]`) · pp. 99–106 (8 pp., REGULAR) · `HPC_FOR_Q` ·
evaluation `UNKNOWN` · Artifact `UNKNOWN` · GENERAL
*HPC relevance:* numerical-precision analysis of a large floating-point computation — what determines
whether a simulator can use single vs double precision, a first-order memory-footprint and throughput
decision at scale. **Weakest-evidenced 2024 inclusion** — judged from title plus venue context, the
abstract was not retrieved. Treat as provisional.

**6 · Polynomial Reduction Methods and their Impact on QAOA Circuits** — Lukas Schmidbauer,
Karen Wintersperger, Elisabeth Lobe, Wolfgang Mauerer (OTH Regensburg / Siemens / DLR `[inference]`)
· pp. 35–45 (11 pp., REGULAR) · `FUTURE_WORKLOAD`, `HPC_FOR_Q` · evaluation `UNKNOWN` ·
Artifact `UNKNOWN` · NISQ. Classical pre-processing whose choices set circuit width and depth — i.e.
the downstream resource requirement. Provisional, moderate relevance.

**Boundary-band (7 pp., `STATUS_UNCLEAR`, not counted): Stripping Quantum Decision Diagrams of their
Identity** — Aaron Sander, Ioan-Albert Florea, Lukas Burgholzer, Robert Wille (TU Munich) ·
pp. 168–174, arXiv 2406.11959 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · Artifact **`PUBLIC_CODE`**
`https://github.com/cda-tum/mqt-ddsim`, `https://github.com/cda-tum/mqt-core` · GENERAL
Counter-evidence toward regular status: TU Munich's publication page records it as **Best Student
Paper** at QSW 2024, and awards are not normally given to short papers. Still excluded from the
confident count per the banding rule, and recorded here in full.
**Code cross-validation** (`DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §6, verdict `PARTIAL_MATCH`):
**the mechanism is verified in the merged upstream code.** In `mqt-core/include/mqt-core/dd/Package.hpp`,
`Package::makeDDNode` carries the comment *"Check if node resembles the identity. If so, skip it"* and,
for matrix nodes after normalization, returns the node to the memory manager and skips a level when
`es[0].p == es[3].p` with weights (1,0,0,1). Supporting symbols seen: `Edge::isIdentity`,
`Package::isCloseToIdentity`, `reduceAncillae`, and the recorded invariants *"Missing DD levels
represent identity wires"* and *"Matrix widths include leading identity levels omitted from the DD"*.
The headline magnitudes (up to **70× runtime**, **3462× node-count reduction**, QFT to **4,096
qubits**) could not be re-read from the paper body and no benchmark reproducing them ships with the
merged code — hence `PARTIAL_MATCH`: mechanism confirmed, magnitudes unverified.

### QSW 2025 — 5 of 17

**1 · QAOA in Quantum Datacenters: Parallelization, Simulation, and Orchestration** —
Amana Liaqat, Ahmed Darwish, Adrian Roman, Stephen Diadamo (affiliations unverified) ·
session S8 "Infrastructure and Lifecycle for Quantum Software Systems", program ID `QSW_6`,
pp. 195–205 (11 pp., REGULAR), Xplore doc 11134327, arXiv 2503.06233 · `Q_IN_HPC`, `HPC_FOR_Q`,
`FUTURE_WORKLOAD` · Artifact `UNKNOWN` · NISQ

**The strongest Quantum-HPC paper at this venue.** An automated, massively parallel QAOA workflow
that partitions problems, batches jobs, selects simulators and schedules execution across distributed
heterogeneous resources (components named **Divi** and **Maestro**). The abstract's own framing:
*"Scaling quantum computing requires networked systems, leveraging HPC for distributed simulation now
and quantum networks in the future… Tasks like algorithm partitioning, job batching, and resource
allocation divert focus from quantum program development."* Finds that **partitioning does not
significantly degrade optimization quality** and often beats classical solvers. Node/core scale
`UNKNOWN`.

**2 · Enhancing Quantum Circuit Compilation with Modular Floorplanning** — Giacomo Lancellotti,
Giovanni Agosta, Alessandro Barenghi, Gerardo Pelosi (Politecnico di Milano) · session S3,
`QSW_19`, pp. 72–80 (9 pp., REGULAR), **DOI `10.1109/QSW67625.2025.00018`** (verified) · `HPC_FOR_Q` ·
evaluation `UNKNOWN` · Artifact `UNKNOWN` · NISQ. Borrows **VLSI floorplanning** to place circuit
modules onto modular/multi-core quantum hardware — the same data-locality problem as partitioning a
task graph across NUMA domains or chiplets.

**3 · Optimization of Hybrid Quantum-Classical Algorithms** — Lian Remme, Alexander Weinert,
Andre Waschk (DLR) · session S9, `QSW_40`, pp. 215–226 (12 pp., REGULAR), arXiv 2505.12853
(**primary category cs.DC**) · `Q_IN_HPC`, `HPC_FOR_Q` · Artifact `UNKNOWN` · GENERAL
Seven optimization routines and three metrics for compiler-optimizing *hybrid* programs in Quil,
where classical control flow and quantum instructions interleave. Opening premise, verbatim:
*"Quantum computers do not run in isolation; rather, they are embedded in quantum-classical hybrid
architectures."* The authors themselves filed it under **cs.DC**.

**4 · SAT Strikes Back: Parameter and Path Relations in Quantum Toolchains** — Lukas Schmidbauer,
Wolfgang Mauerer (OTH Regensburg / Siemens `[inference]`) · session S4, `QSW_43`, 12 pp. (REGULAR),
Xplore doc 11134339, arXiv 2505.22060 · `HPC_FOR_Q`, `FUTURE_WORKLOAD` · **classical-only** ·
Artifact **`PUBLIC_ARTIFACT`** Zenodo `10.5281/zenodo.15464391` +
`https://github.com/lfd/QSW25-SAT-Strikes-Back` · NISQ
Systematic analysis of transformation paths from k-SAT to QUBO and the structural properties each
induces — a scaling study of how *classical front-end* choices propagate into downstream resource
requirements (variable count, coupling density).

**5 · Make Some Noise! Measuring Noise Model Quality in Real-World Quantum Software** —
Stefan Raimund Maschek, Jürgen Schwitalla, Maja Franz, Wolfgang Mauerer (OTH Regensburg
`[inference]`) · session S1, `QSW_56`, pp. 1–11 (11 pp., REGULAR) · `HPC_FOR_Q` · evaluation
`UNKNOWN` · Artifact `UNKNOWN` · NISQ. *HPC relevance:* noise-model fidelity determines whether large
classical simulation campaigns are predictive of hardware, and noise-model complexity is itself a
simulation-cost driver. **Weakest-evidenced 2025 inclusion; borderline.**

**Boundary-band (7 pp., not counted): Shuttling for Trapped-Ion Quantum Computers with Embedded
Processing Zones** — Daniel Schönberger, Janine Hilder, Ferdinand Schmidt-Kaler, Robert Wille ·
session S5, `QSW_12`, pp. 123–129 · `HPC_FOR_Q` · NISQ. *A follow-up, "Robust Shuttling Compilation
for Trapped-Ion Quantum Computer," appears at QSW 2026 as `QSW_SHT_55` — an explicitly labelled
**short** paper, therefore excluded there too.*

### QSW 2026 — 9 of 17

**Evidence caveat for this entire subsection:** categories are `[official-program]`-verified via the
`QSW_REG_` prefix, but **DOIs, page ranges, abstracts, affiliations, evaluation platforms and
artifacts are largely unverified** — the proceedings TOC was unreachable and most 2026 papers are not
yet indexed in reachable open sources. Titles and program IDs are verbatim; descriptions marked
`[inference]` are read off the title and are **not** abstract-verified. Author affiliations have
deliberately **not** been filled in from prior work.

1. **Pêlαγos: An Adaptive GPU Decoder for Error Correction Simulations…** (title truncated in the
program) — Dionysios Diamantopoulos et al. · S5 "Performance and Reliability", `QSW_REG_11` ·
`HPC_FOR_Q` · EARLY_FTQC/FTQC `[inference]`. **The single most on-target Quantum-HPC title in the
2026 program**: GPU-accelerated QEC decoding is the canonical HPC-for-quantum workload, and it is the
only GPU decoder anywhere in this six-venue census. No preprint found; evaluation and artifact
`UNKNOWN`.
2. **qScheduler: A Hybrid Reservation–Dispatch System…** (truncated) — Abhishek Nautiyal et al. ·
S4 "Software Systems and Workflows", `QSW_REG_26` · `Q_IN_HPC` `[inference]`. A batch scheduler
combining **reservation (Slurm-style advance reservation) with opportunistic dispatch** — the core of
treating a QPU as an HPC-centre resource. Artifact **unresolved**: a repository
`abhishek-nautiyal97/qScheduler` is indexed by a third-party wiki but
`https://github.com/abhishek-nautiyal97/qScheduler` **returned 404** — private, renamed or deleted;
recorded as unresolved rather than claimed. *(Distinct from arXiv 2604.05505 "Qurator", a different
paper by different authors — checked and rejected to avoid misattribution.)*
3. **DisMap: Calibration-Aware Distributed Compilation for Multi-Chip Quantum Systems** —
Zefan Du et al. · S1 "Architecture-Aware Compilation", `QSW_REG_34` · `HPC_FOR_Q`,
`FUTURE_WORKLOAD` `[inference]`. Distributed compilation and partitioning against a non-uniform,
time-varying resource topology.
4. **An efficient compilation architecture for quantum** (title truncated in the program) —
Lukas Scheller et al. · S1, `QSW_REG_13` · `HPC_FOR_Q` `[inference]` · GENERAL.
5. **A Multi-Level Compiler Pipeline for Qoala Quantum Internet Programs** — Sacha Bernheim et al. ·
S1, `QSW_REG_38` · `HPC_FOR_Q`, `Q_IN_HPC` `[inference]`. A multi-level IR/lowering pipeline for a
distributed runtime mixing local gates with network operations under strict timing. Artifact
**`PARTIAL`/unconfirmed** — `https://github.com/SoftwareQuTech/qoala-mlir` exists and matches the
subject, but was **not** verified to be this paper's artifact.
6. **Fidelity-Based Quantum Device Selection Using Graph Neural Networks** — Antonio Tudisco et al. ·
S5, `QSW_REG_33` · `Q_IN_HPC` `[inference]`. Device selection is the placement decision in a
heterogeneous multi-QPU pool, with a learned model predicting achievable fidelity per device.
7. **Branch-Aware Quantum Constant Propagation for Dynamic Quantum Circuits** — Innocenzo Fulginiti
et al. · S5, `QSW_REG_54` · `HPC_FOR_Q`, `FUTURE_WORKLOAD` `[inference]` · EARLY_FTQC. Dynamic
circuits are exactly where the classical control path enters the critical timing path. *Same first
author as ISC 2026's dynamic-circuit compiler paper — a visible author thread across the two venues.*
8. **Automatic De-Quantization of Quantum Programs Using Constant Propagation** — Lian Remme et al.
(DLR, same group as QSW 2025 §3 `[inference]`) · S4, `QSW_REG_30` · `HPC_FOR_Q` `[inference]` ·
GENERAL. Compiler analysis that moves work off the QPU onto the classical host when provably
equivalent — directly reducing QPU occupancy. *(A third-party index gives arXiv 2605.22980;
**not independently verified** — do not cite without checking. Note arXiv 2605.16955 is a
**different** QSW 2026 paper, DQI-Kit.)*
9. **Software Between Quantum and Machine Learning — And Down to Pulses** — Maja Franz et al.
(OTH Regensburg / Mauerer group `[inference]`) · S3, `QSW_REG_32` · `HPC_FOR_Q` `[inference]` · NISQ.
Spans the stack from ML framework down to control pulses. **Weakest of the nine**; included because
pulse-level lowering is a genuine systems contribution, but relevance is title-inferred.

## 4. Exclusions

**(a) Not regular main-track papers.**
QSW 2024's four QSWUtil invited-symposium items (pp. 1–23): *The MQT Handbook* (pp. 1–8; TU Munich's
record labels it "Invited Paper" — it would otherwise have been a plausible inclusion, since it
surveys simulation, compilation and verification tooling), *Composable Quantum Oracles* (pp. 9–11, at
the 3-page WIP limit), *Backcasting Perspectives on Services of Future Quantum Internet*
(`QSW_SYM_79`) and *Towards An Architecture Description Language for Hybrid Quantum-Classical
Systems* (`QSW_SYM_97`). Also 2024's *A Web-based Software Development Kit for Quantum Network Simulation* (pp. 143–145,
3 pp. = WIP), which would otherwise have been a borderline relevance candidate.
QSW 2025's four non-QSW volume-mates (pp. 257–280) and five short papers — **including
*A Quantum Algorithm for Nonlinear Electromagnetic Fluid Dynamics via Koopman–von Neumann
Linearization* (pp. 35–40, 6 pp.), a genuine `Q_FOR_HPC` CFD topic excluded purely on category.**
QSW 2026's ten `QSW_SHT_*` papers — of which two would qualify on relevance if short papers were ever
in scope: `QSW_SHT_3` *On Distributed Quantum Computing with Distributed Fan-Out Operations* and
`QSW_SHT_55` *Robust Shuttling Compilation for Trapped-Ion Quantum Computer*.
QSW 2025 session S7 was a **panel** ("Teaching Quantum Software Development to CS Students") and
correctly contributes 0.

**(b) Regular papers excluded as not Quantum-HPC relevant — the quantum-software-engineering bulk.**

| Year | Regular papers | Excluded as quantum-SE / application with no systems dimension | Share |
|---|---:|---:|---:|
| 2024 | 13 | 7 | 54% |
| 2025 | 17 | 12 | 71% |
| 2026 | 17 | 8 | 47% |
| **Total** | **47** | **27** | **≈57%** |

Representative: automated verification of Silq programs with SMT solvers; circuit-ansatz design
patterns; quantum denoising diffusion models; repository-mining studies of quantum software;
reporting-guideline proposals; barrier-certificate circuit verification; QML application studies;
framework/toolbox papers (AutoQML, Qmod, ProvideQ, DQI-Kit) whose contribution is expressiveness and
usability rather than performance or resource management; metamorphic testing of VQCs; ansatz
expressivity theory. Two 2025 items were genuinely borderline and are flagged for revisiting if the
scope widens: *Detecting and Tolerating Faults in Hybrid Quantum Software Systems Using Architectural
Redundancy*, and the astrophysics/CMB QML application papers. Category-rule exclusions also removed
QKD/QPUF work (2026 `REG_18`, `SHT_50`) under the post-quantum-cryptography rule.

## 5. What QSW rewards as a contribution

1. **QSW is a quantum *software-engineering* venue first and a systems venue only incidentally.**
≈57% of its regular papers are testing, debugging, verification, repository mining, design patterns,
reporting methodology, QML applications or framework/usability papers with no parallelism, scaling,
memory, communication or resource-management dimension.
2. **A tool that exists is a first-class contribution here.** An unusually large share of accepted
papers are toolkits and SDKs (MQT, AutoQML, Qmod, ProvideQ, qoala-mlir). Several accepted papers
report **no speed-up at all** and would struggle at a performance-oriented venue. Reproduction
packages (Zenodo + GitHub) are common and clearly valued.
3. **The HPC door is explicitly open and widening.** The 2024 CFP already listed *"High Performance
Computing with Quantum Computers — HPC architectures and quantum-classical workflows"* as a named
topic; 2025 adds Cloud computing; and **2026 made it structural**, with dedicated *"Software Systems
and Workflows"* and *"Performance and Reliability"* sessions that did not exist in 2024, and with a
GPU QEC decoder, a QPU job scheduler and a distributed multi-chip compiler accepted as regular papers.
The Quantum-HPC share of regular papers roughly **doubles from 2025 (29%) to 2026 (53%)** and the
2026 papers are markedly more systems-flavoured. **`OBSERVED_SHIFT`** — the denominator is small
(17 regular papers) and 2026's evidence is the weakest of the three years, so this is recorded as an
observation, not a trend claim.
4. **Compilation is the reliable bridge.** Across all three years the systems-flavoured papers that
get in are overwhelmingly *compiler and toolchain* papers. Compilation is legible to this community
as "software", so HPC-adjacent work framed as a compiler pass lands cleanly where the same work
framed as a performance study might not.
5. **Page count alone is not sufficient at this venue** — the 7-page boundary band is up to a fifth
of the population, and any census setting a single page threshold will misclassify roughly that
fraction.

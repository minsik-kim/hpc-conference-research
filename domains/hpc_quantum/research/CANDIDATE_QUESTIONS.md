# CANDIDATE_QUESTIONS — HPC & Quantum

**Status of every entry below: `CANDIDATE`, source-reported.** These are
`VENUE_GAP` / `POSSIBLE_CROSSOVER` / `OPEN_QUESTION` observations already
present, verbatim in substance, inside the imported corpus. **None was
generated during this import, and none has been independently
re-falsified** through the `governance/RESEARCH_GAP_RULES.md` pipeline
(own-corpus cross-check → closest-work search → external targeted
literature search → novelty falsification → experiment feasibility). A
future session performing that pipeline should start here, not treat these
as `STILL_OPEN` or novelty-confirmed on the strength of this index alone.

The source corpus is explicit that `VENUE_GAP ≠ RESEARCH_GAP`
(`ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:508`,
`SC_2024_2025_QUANTUM_HPC_CENSUS.md:1247`) — an absence from one venue's
main track is not evidence that no one works on the topic.

## 1. VENUE_GAP candidates

| # | Observation | Pointer | Plausible alternative readings (source's own, not resolved) |
|---|---|---|---|
| G1 | Real-time QEC decoding is structurally a classical HPC problem (latency-bounded, throughput-bounded, parallelizable, hard cryogenic-boundary bandwidth constraint) and is the densest topic at four architecture venues, but is absent from SC's main track in both 2024 and 2025. | `corpus/quantum-hpc-survey/corpus/SC_2024_2025_QUANTUM_HPC_CENSUS.md:911-925` | (a) genuinely architectural, not facility-scale; (b) not an HPC problem until a fault-tolerant machine exists to host it; (c) SC has already accepted *adjacent* problems (SC24 fault-injection characterization, SC25 decoder training-data generation) |
| G2 | Multi-node/distributed quantum simulation is SC's largest branch (4 of 11) but is entirely absent from ASPLOS's main track in this window (0 of 36). | `corpus/quantum-hpc-survey/corpus/ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:506-520`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:121` | (a) requires a machine ASPLOS reviewers do not expect; (b) the single-device version is the natural ASPLOS framing; (c) the work is submitted elsewhere |
| G3 | Dataset/application papers with no classical-hardware mechanism (e.g. SC's QDockBank) have no ASPLOS analogue — every one of the 36 ASPLOS papers has an identifiable classical mechanism. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:521-523` | `[inference]` in the source itself — ASPLOS's boundary may simply not extend that far |
| G4 | Hybrid CPU/GPU/QPU runtime and execution model is absent from SC's main track. | `SC_2024_2025_QUANTUM_HPC_CENSUS.md:919` | (a) OSDI has absorbed it (QOS, HyperQ, qTPU per the source's Phase-1 map); (b) lives in SC's own workshops (SC-W'25) |
| G5 | Circuit cutting/knitting is absent from SC's main track. | `SC_2024_2025_QUANTUM_HPC_CENSUS.md:920` | present at SC-W'25 (workshop level), main-track at ASPLOS/ICS/QCE |
| G6 | QPU scheduling/resource management arrived at SC only once (Qonductor, SC25). | `SC_2024_2025_QUANTUM_HPC_CENSUS.md:921` | whether this is the start of a branch or a one-off is explicitly marked `INSUFFICIENT_SAMPLE` in the source |
| G7 | Programming models for hybrid quantum-classical computing are absent from SC's main track. | `SC_2024_2025_QUANTUM_HPC_CENSUS.md:922` | source reads this as "natural SIGPLAN territory" (CGO/PLDI/OOPSLA) |
| G8 | HPC-centre QPU integration/operations is absent from SC's main track. | `SC_2024_2025_QUANTUM_HPC_CENSUS.md:923` | source's Phase-1 map found this is essentially an ISC/LRZ-TUM thread |
| G9 | Fault-tolerant full-machine architecture proposals (6+ at ASPLOS) have no SC analogue (0). | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:506-511` | these are machines that do not yet exist, evaluated analytically; SC's evaluation norms may not accommodate that |
| G10 | Both venues are thin on modular/multi-QPU architecture (ASPLOS 3, SC 1). | `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:204` | — |

## 2. POSSIBLE_CROSSOVER candidates

| # | Observation | Pointer |
|---|---|---|
| C1 | At QEC code distance d ≥ 21–27, a single logical qubit's decoding graph no longer fits one FPGA/ASIC device (Micro Blossom is already at 867k/900k LUTs at d=15); partitioning a single decoding graph across devices, or inter-block fusion during lattice surgery, would introduce a real communication term under a hard real-time deadline — the source's own candidate for the most consequential crossover in the corpus. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:417-450` |
| C2 | The modular/multi-QPU branch (MECH, COMPAS) is natively distributed, so scale-out beyond one interconnect fabric requires no reframing, only more machine. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:450`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:204` |
| C3 | BQSim's single-GPU batched decision-diagram simulation, if scaled the way SC's Atlas/PTSBE already scale hierarchical partitioning and random-circuit sampling, is a direct analogue the source says has "already crossed elsewhere" (at SC). | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:448` |
| C4 | The successor generation of the QEC-decoder lineage (post-ASPLOS, now at ISCA) is dominated by parallel/windowed/distributed vocabulary — read by the source as "the direction of travel," not a confirmed trend. | `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:62` |
| C5 | The qLDPC turn in QEC (surface code → qLDPC as a first-class object from 2025) implies BP/BP+OSD decoding rather than matching — a bulk-synchronous message-passing computation over a sparse factor graph, which maps to conventional HPC parallel primitives; **none of the four qLDPC papers in the ASPLOS corpus analyses the resulting real-time decoder cost.** | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:440`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md:90` |

## 3. OPEN_QUESTION candidates (not framed as gap or crossover)

| # | Observation | Pointer |
|---|---|---|
| Q1 | Trapped-ion timing (measurement 400 µs, two-qubit gates 40 µs) is roughly 400× slower than the superconducting 1 µs that Promatch and Micro Blossom both anchor their real-time decoding deadlines to — whether/how decoder architecture should differ by qubit modality is not analyzed by any paper in the corpus. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:381` |
| Q2 | Micro Blossom names "dynamic decoding-graph fusion during lattice surgery" as required future work, not yet solved by any paper in the corpus. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:420` |
| Q3 | Micro Blossom's stated requirement that the control stack "load and route syndrome data at Terabit/s" is flagged by the source as the single most HPC-shaped number in the corpus — whether existing HPC network/interconnect research addresses this bandwidth class is not investigated in-corpus. | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md:426` |

## 4. Explicitly not investigated as gaps in this corpus

VQE-adjacent absences (initialization/warm-start, barren plateaus,
gradient estimation) are `NOT_COVERED` in this workspace (see
`TOPIC_MAP.md`), not `VENUE_GAP` candidates — the source corpus is a
venue-census project and never attempted a VQE-methods gap analysis, so
there is nothing here to index for that subfield.

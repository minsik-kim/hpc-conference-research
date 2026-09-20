# QUANTUM_HPC_JOURNAL_MAP

**Eight core journals at the HPC × Quantum-Computing interface, 2024–2026 — comparative map.**

Compiled 2026-09-17 (KST). Companion documents: `QUANTUM_HPC_JOURNAL_CENSUS_2024_2026.md`
(master census), `QUANTUM_HPC_JOURNAL_CONFERENCE_CROSSWALK.md` (conference correspondence),
`VERIFICATION_CHANGELOG.md` (post-draft corrections), and the four per-journal detail files.

This map is a claim about **eight journals over three years**, nothing more. It is not a map of
quantum computing, and it is not a claim about journals outside the commissioned list.

---

## 1. The comparison table

| Journal | Role in the Quantum-HPC landscape | Population swept | Included original research (2024/2025/2026) | Dominant branches | Conference correspondence | Future census policy |
|---|---|---:|---|---|---|---|
| **FGCS** (Elsevier) | **The HPC-centre integration journal.** The only venue in the eight where the QPU is treated as a resource *inside* a computing centre rather than a device to be compiled for. | 1,567 | **20** (5 / 8 / 7) | runtime & orchestration, QPU scheduling & resource management, hybrid workflow, HPC-QPU integration, benchmarking | SC · ISC · CCGrid · ICS | **CORE_CENSUS** |
| **TQE** (IEEE) | **The systems-and-control journal of the quantum-engineering community.** Largest absolute yield, but the lowest signal-to-noise of the eight. | 254 (full population screened) | **25** (7 / 12 / 6) | compiler & mapping, architecture & control, benchmarking, QEC classical processing, multi-QPU | QCE (QSYS) · ISCA · MICRO · HPCA | **SELECTIVE_CENSUS** |
| **TQC** (ACM) | **The quantum software-and-systems journal.** The clearest home for classical simulation engines and multi-core/multi-QPU compilation, plus the corpus's two best navigation surveys. | 97 (full population screened) | **20** (7 / 4 / 9) | compiler & mapping, distributed/GPU simulation, benchmarking, multi-QPU, runtime | QCE · ASPLOS · CGO · PLDI | **SELECTIVE_CENSUS** |
| **TCAD** (IEEE) | **The compilation and EDA journal.** Owns the mapping/routing/scheduling branch outright, but 60% of its quantum population is device-level EDA and PQC hardware. | 1,562 | **12** (5 / 6 / 1) | compiler & mapping (dominant), simulation representation, architecture & control | DAC · ICCAD · DATE · ASPLOS | **CORE_CENSUS** with a hard scope filter |
| **TC** (IEEE) | **The accelerator-substrate journal.** Thin but distinctive: where quantum simulation and emulation meet FPGA and storage hierarchies. | 849 | **6** (2 / 2 / 2) | FPGA/accelerated simulation, compiler & mapping, distributed-QC architecture | MICRO · HPCA · FCCM/FPGA | **SELECTIVE_CENSUS** |
| **TACO** (ACM) | **A narrow, high-precision sensor.** 1% yield, but every survivor frames the QPU as a *shared resource* — multiprogramming, cutting, throughput. | 412 | **4** (1 / 2 / 1) | QPU scheduling & multiprogramming, compiler & mapping, circuit cutting | ASPLOS · HPCA · CGO | **BIBLIOGRAPHY_SENSOR** |
| **TPDS** (IEEE) | **The cluster-level simulation journal — and only that.** Two papers, both distributed state-vector simulation, both 2026. | 552 | **2** (0 / 0 / 2) | distributed/GPU simulation | SC · IPDPS · ICS | **LOW_YIELD** |
| **JPDC** (Elsevier) | **Essentially empty.** One survey, zero original research. | 388 | **0** (0 / 0 / 0) | — | — | **BIBLIOGRAPHY_SENSOR** |

**Totals: 5,681 articles swept · 563 candidates · 94 included · 89 included original research ·
80 borderline · 383 excluded · 3 unresolved.**

---

## 2. The six things this map establishes

### 2.1 FGCS's prominence survives a full census — and is a prominence of *kind*, not of volume

The pre-scan suggested FGCS was the most directly relevant journal. A full-population sweep confirms
it, but the reason is not that FGCS publishes the most Quantum-HPC papers. TQE publishes more (25 vs
20). FGCS is the strongest journal because of **what it publishes that nobody else in these eight
does**: 12 of its 20 included papers carry the `Q_IN_HPC` scenario tag — a QPU integrated into a
computing centre — against 3 at TQE, 3 at TQC, 3 at TACO, 2 at TCAD and **0 at TC, TPDS and JPDC**.
More than half of the entire corpus's `Q_IN_HPC` weight (12 of 23) sits in one journal.

FGCS is also the only journal of the eight with a **standing guest-edited quantum collection** —
*Advances in Quantum Computing: Methods, Algorithms, and Systems*, now in its third volume, with the
same three guest editors (Markidis, KTH; Taufer, UTK; Grandinetti) across all three. That collection
is the mechanism behind the journal's steady yield, and it is also why FGCS's false-positive profile
is unusual: its largest excluded class is **quantum machine learning (13)**, not post-quantum
cryptography (9), inverting the pattern in every other non-quantum journal here.

### 2.2 The corpus's centre of gravity is compilation, not simulation and not QEC

| Branch | Papers | Where it lives |
|---|---:|---|
| `compiler_mapping_routing` | 38 | everywhere; TCAD and TQC and TQE own it jointly |
| `distributed_gpu_simulation` | 22 | TQC (7), FGCS (4), TQE (3), TCAD (3), TC (3), TPDS (2) |
| `benchmarking_performance_modeling` | 20 | TQE (6), TQC (6), FGCS (5) |
| `architecture_control` | 17 | TQE (8), FGCS (3), TCAD (3) |
| `quantum_runtime_orchestration` | 14 | FGCS (6) |
| `qpu_scheduling_resource_mgmt` | 14 | FGCS (6), TACO (3) |
| `multi_qpu_distributed_qc` | 13 | TQE (4), TQC (3) |
| `hpc_qpu_integration` | 8 | FGCS (5) |
| `qec_classical_processing` | 8 | TQE (4), TQC (3), TACO (1) |
| `hybrid_workflow` | 7 | FGCS (5) |
| `circuit_cutting_reconstruction` | 5 | TQE (3) |
| `scientific_workflow_application` | 3 | FGCS (3) |

Compilation is 38 of 89 papers — 43% — and it is the one branch present in seven of the eight
journals. This is the most important structural fact about the journal landscape and it differs
sharply from both conference censuses in the existing corpus (see the crosswalk document).

### 2.3 QEC classical processing is `UNDERREPRESENTED_IN_THIS_CORPUS`, and absent from every classical-systems journal

Eight records across eight journals, and **all eight sit in quantum-native venues** (TQE 4, TQC 3,
TACO 1). FGCS, TCAD, TC, TPDS and JPDC contain **zero** decoder-acceleration, decoder-scheduling or
syndrome-compression papers in three years.

This is the journal-side counterpart of the existing conference corpus's most load-bearing
observation — that real-time QEC decoding is dense at ASPLOS/ISCA/MICRO/HPCA and absent from SC's
main track. The journal evidence extends that observation rather than resolving it: the work is not
appearing in the HPC journals either. Recorded as `JOURNAL_GAP`, not as a research gap. No novelty
claim is made or implied.

### 2.4 The classical-systems journals are sparse, and the sparsity is real

TPDS (2 of 552), TACO (4 of 412), TC (6 of 849), JPDC (0 of 388). Together, four of the most
established parallel-computing and architecture journals in the field produced **12 included
original-research papers in three years** — fewer than TQE alone.

The low-yield hypothesis for TPDS and JPDC is **CONFIRMED on evidence, not assumed**:

- **TPDS** — 10 candidates in 552 articles. Eight are false positives: three post-quantum
  cryptography GPU implementations, four classical electronic-structure codes (NNQS, PWDFT, DFPT),
  one classical simulated annealing. The two survivors are both distributed state-vector simulation
  and both 2026 (`10.1109/tpds.2026.3652733`, `10.1109/tpds.2026.3678345`). There is **no** QPU
  scheduling, workflow or runtime paper in TPDS in 2024 or 2025.
- **JPDC** — 7 candidates in 388 articles, **zero original research**. The single inclusion is a
  survey of quantum serverless platforms (`10.1016/j.jpdc.2026.105303`), recorded as
  `BIBLIOGRAPHY_HUB`. The other six are quantum-inspired metaheuristics, QML applications and PQC.

Zero is a result. It was not padded.

### 2.5 Journals split simulation by *level*, not by contest

The three journals that publish classical quantum simulation do not compete; they occupy different
layers of the same stack:

- **TCAD — the representation level.** Decision diagrams, tensor-network contraction, gate
  fusion/scheduling inside a simulator kernel.
- **TC — the substrate level.** FPGA emulation, FPGA + SATA storage hierarchies for large state
  vectors.
- **TPDS — the cluster level.** Communication volume and CPU+GPU communication-partition
  co-optimisation across nodes.
- **TQC — the engine level.** Multi-GPU state-vector reordering, parallel decision diagrams,
  tensor-network simulation on A100s, emulator benchmarking to 1,024 qubits.
- **FGCS — the machine level.** 50-qubit universal simulation on a named exascale system.

A question about "where does distributed quantum simulation get published" therefore has no single
answer; it has a layer-dependent answer.

### 2.6 The whole corpus is `HPC_FOR_Q`; the reverse direction barely exists

| Scenario | Papers | Share |
|---|---:|---:|
| `HPC_FOR_Q` — classical HPC serving quantum computing | 84 | 94% |
| `FUTURE_WORKLOAD` — analysis of future heterogeneous CPU/GPU/QPU systems | 27 | 30% |
| `Q_IN_HPC` — a QPU integrated into an HPC centre | 23 | 26% |
| `Q_FOR_HPC` — quantum accelerating a classical HPC workload | **3** | 3% |

Classical computing serving quantum computing is essentially the entire journal literature at this
interface. The direction a supercomputing centre would actually buy a QPU for — quantum accelerating
a classical workload — is three papers in 5,681. Recorded as `UNDERREPRESENTED_IN_THIS_CORPUS`.

---

## 3. Per-journal census policy, with reasons

### FGCS — **CORE_CENSUS**
Steady 5/8/7 yield, a standing guest-edited quantum collection now in Vol III, and material that
exists in this shape nowhere else in the eight: full-machine hybrid workflows, QPU sharing on
production clusters, HPC-centre integration position papers. Sweep **on online-first date, not volume
cover date** — Elsevier cover dates run about six months ahead, and sweeping on cover date cost this
census four records on the first pass, including the Fugaku closed-loop paper. Expect the majority of
candidates to be false positives, concentrated in QML and PQC. FGCS will not source
decoder-acceleration work.

### TQE — **SELECTIVE_CENSUS**
Real and sustained yield, but 74% of the venue is out of scope with a stable year-to-year share, and
TQE has no section headings to filter on. Track by topic, in these seven areas only: classical
circuit simulation at scale; QEC classical processing (parallel/FPGA decoders, controller
benchmarks); compilation cost and scalability; circuit cutting and distributed execution;
multi-QPU/modular architecture; QPU resource management and runtime; classical control-plane work
that states a latency, memory, bandwidth or thermal budget. Do **not** census the
networking/QKD, sensing/device, optimization-application, QML, VQA-methodology or code-theory
segments — 49 + 32 + 29 + 21 + 16 exclusions came from exactly those. Suggested cadence: quarterly
title screen against the seven areas; full-population pass every three years.

### TQC — **SELECTIVE_CENSUS**
Rising yield (7/4/9) concentrated in six sub-areas: distributed and multi-core execution; classical
simulation engines; compilers that report compile-time cost; QPU scheduling, orchestration and shot
budgeting; HPC-QPU integration surveys and throughput benchmarking; classical parallel kernels for
QEC. About 60% must be screened out — dominated by algorithms/complexity (21) and gate-count-only
synthesis (11). TQC also carries the corpus's two most useful navigation surveys
(`10.1145/3743149`, `10.1145/3762672`).

### TCAD — **CORE_CENSUS**, with a hard scope filter
The compiler/mapping branch's owner: 7 of 12 inclusions and 9 of its included+borderline records are
compilation. But 41 of 68 candidates are out of scope — 11 PQC/side-channel, 9 superconducting/AQFP/
SiDB EDA and device modelling, 5 QML feature selection. TCAD also needs a **full-text pass, not an
abstract sweep**: 10 TCAD candidates had no retrievable abstract and three remain
`INSUFFICIENT_EVIDENCE`. The 2026 figure (1) is depressed by that, not by a fall in output.

### TC — **SELECTIVE_CENSUS**
Two recurring shapes only: accelerator/emulator substrates for simulation (FPGA + SATA, FPGA
emulators) and distributed-QC architecture with a quantitative performance model. Screen on those two
and on PQC negation — 12 of 28 TC exclusions are post-quantum cryptography, the highest PQC share of
any journal here.

### TACO — **BIBLIOGRAPHY_SENSOR**
About 1% yield against 412 articles, but the four survivors are strong, non-duplicated and share a
single frame: the QPU as a shared resource under multiprogramming. A keyword sweep plus a four-class
filter removes 4 of the 5 false positives automatically, so the cost of keeping TACO as a sensor is
near zero. Do not run a full census.

### TPDS — **LOW_YIELD**
Screen annually on `quantum circuit simulation` and `distributed quantum` only. Both 2026 papers are
worth reading; neither 2024 nor 2025 produced anything. Do not assume a parallel-computing journal
must contain quantum systems papers — three years of evidence says it does not.

### JPDC — **BIBLIOGRAPHY_SENSOR**
Zero original research in three years. Annual title scan only.

---

## 4. Recommended future tracking set

**Census continuously (2):** FGCS, TCAD.
**Selective topical tracking (3):** TQE, TQC, TC.
**Annual sensor scan only (3):** TACO, TPDS, JPDC.

If the tracking set must be cut to four: **FGCS, TCAD, TQE, TQC** — those four hold 77 of the 89
included original-research papers (87%).

A note against over-narrowing: TACO and TPDS have the lowest volume and the highest per-paper
relevance in the corpus (TACO 4 of 4 frame the QPU as a shared resource; TPDS 2 of 2 are cluster-level
simulation). Dropping them entirely would lose the two branches that map most directly onto a
supercomputing centre's own concerns. Sensor-scan cost is a few minutes a year.

---

## 5. Evidence limitations of this map

1. **Artifact status is `UNKNOWN` for 46 of 89 included papers.** IEEE Xplore, ACM DL badge pages and
   Elsevier full text were not reachable from the research environment. `UNKNOWN` means *not checked*.
2. **Zero `CONFIRMED_EXTENSION` records.** Conference-extension footnotes live in publisher front
   matter that could not be read. Four `RELATED_LINEAGE` records carry stated evidence; every other
   record is `UNKNOWN`, which is *not established*, not *not an extension*.
3. **TQE census years rest on the volume cover year** (`YEAR_BASIS=ISSUE`), because IEEE Early Access
   dates were not obtainable for it. One TQE record was provably outside the window on this basis and
   was moved to `OUT_OF_WINDOW`; others may be affected.
4. **Three TCAD Early Access records are `INSUFFICIENT_EVIDENCE`** — no abstract retrievable.
5. **Abstracts were truncated to ~700–900 characters** for the screening pass. Twenty candidate
   records had no abstract at all and were screened on title plus targeted retrieval.
6. **Recall rests on two independent metadata sources** (Crossref full-population enumeration by
   ISSN, unioned with an OpenAlex title-and-abstract search) and a 19-term vocabulary. A paper whose
   title and abstract contain none of those terms would be missed. No such case was found in the
   secondary sweep, but the sweep could not be completed for every term because of API rate limits.
7. **Seed-anchoring:** 23 of 24 pre-scan seed titles are present and all 23 are INCLUDED — a 100% hit
   rate against a 17% corpus-wide inclusion rate. That asymmetry is expected (the seeds were drawn
   from a prior relevance scan) but is recorded as an anchoring risk. 69 of the 89 included papers
   (78%) are non-seed, so the census rebuilt the population rather than confirming the seed list.

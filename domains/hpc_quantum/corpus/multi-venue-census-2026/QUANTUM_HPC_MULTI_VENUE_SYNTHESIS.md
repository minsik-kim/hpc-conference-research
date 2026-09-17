# Quantum-HPC Multi-Venue Synthesis — ISC · ISCA · ICS · HPCA · MICRO · QSW, 2024–2026

**Compiled 2026-09-17** from the six venue censuses and two code cross-validation deep dives in this
directory, read against the completed SC 2024–2025 and ASPLOS 2024–2026 censuses in
`../quantum-hpc-survey/`.

**No research gap is declared in this document.** Permitted vocabulary only: `VENUE_GAP`,
`POSSIBLE_CROSSOVER`, `OPEN_QUESTION`, `UNDEREXPLORED_IN_THIS_CORPUS`, `INSUFFICIENT_EVIDENCE`
(`governance/RESEARCH_GAP_RULES.md`).

## 1. What was screened

**1,281 main-track regular research papers** across 18 venue-years, of which **102** are Quantum-HPC
relevant (7.96%). Three denominators inside that total are `TOTAL_COUNT_UNVERIFIED` — HPCA 2026 is
**≥118** and enters as 118, ISCA 2025's research subtotal carries a ±1, and QSW 2026's 17 rests on a
program with no publisher TOC — so the honest form is **1,281 with a known one-sided uncertainty**.

| Venue | 2024 | 2025 | 2026 | Relevant total | Papers screened | Rate |
|---|---|---|---|---:|---:|---:|
| **ISC High Performance** | 6 / 24 | 3 / 28 | 4 / 35 (+1 borderline) | **13** | 87 | 14.9% |
| **ISCA** | 6 / 83 | 16 / 131 | 11 / 161 | **33** | 375 | 8.8% |
| **ICS** | 1 / 45 | 2 / 83 | 5 / 102 | **8** | 230 | 3.5% |
| **HPCA** | 1 / 75 | 7 / 113 | 9 / ~118 | **17** | 306 | 5.6% |
| **MICRO** | 3 / 113 | 8 / 123 | `PROGRAM_INCOMPLETE` | **11** | 236 | 4.7% |
| **IEEE QSW** | 6 / 13 | 5 / 17 | 9 / 17 | **20** | 47 | 42.6% |
| **Total** | **23** | **41** | **38** (+MICRO-59 unknown) | **102** | **1,281** | **7.96%** |

Denominators are regular research-track papers; ISCA and HPCA industry-track papers are archival but
none is quantum, and the table uses research-track denominators for both. QSW's denominator is
*confident* regular papers only, excluding its 7-page boundary band.

**The rate column is the single most misleading number here.** QSW's 42.6% and ISC's 14.9% reflect
tiny, topically pre-filtered populations; ISCA's 8.8% of 375 is a far larger absolute body of work.
Read the absolute counts, not the shares.

## 2. Bottom-up taxonomy

Rebuilt from what the 102 papers actually contain, not fitted to the Phase-1 scaffold. Papers carry
multiple tags, so the branch counts below sum to more than 102; they are indicative, not a partition.

```
Quantum-HPC (2024–2026, six venues)
│
├── Compilation, mapping and synthesis ................................ ~40  ← the largest branch
│   ├── routing / qubit mapping / ISA-portable routing
│   ├── zoned neutral-atom and trapped-ion movement scheduling
│   ├── fermion-to-qubit encoding, Pauli-ordering, Trotterization
│   ├── lattice-surgery layout and scheduling (FT-scale)
│   ├── autotuning / RL-driven pass selection            [NEW branch vs Phase 1]
│   ├── dynamic-circuit and classical-control compilation [NEW branch vs Phase 1]
│   └── distributed / multi-chip compilation             [NEW branch vs Phase 1]
│
├── QEC as a classical computing workload ............................ ~20
│   ├── real-time decoding: windowed, speculative, scheduled
│   ├── decoder hardware: FPGA, ASIC, cryogenic predecoding
│   ├── qLDPC decoding (BP-family) — distinct from surface-code matching
│   ├── leakage speculation / classification in the control loop
│   ├── syndrome I/O, compression and the cryogenic bandwidth boundary
│   ├── syndrome-extraction architecture and scheduling
│   └── defect tolerance, calibration and drift during FT execution
│
├── Classical quantum simulation ..................................... ~10
│   ├── statevector (compression-assisted, tensor-contraction, dataflow-accelerated)
│   ├── stabilizer / extended stabilizer
│   ├── decision diagram (single-node structural, multi-node ring)
│   └── noisy / trajectory (computational reuse, tracking-uncomputation-sampling)
│
├── Scheduling, resource management and runtime ...................... ~10
│   ├── multi-device / fleet job scheduling (queue or machine abstraction)
│   ├── hybrid host↔QPU integration and offload latency
│   ├── observable-measurement and shot orchestration     [NEW branch vs Phase 1]
│   └── multi-tenancy, isolation and untrusted-cloud execution
│
├── Multi-QPU / distributed quantum computing ........................ ~9
│   ├── switch-network topology for quantum datacenters
│   ├── entanglement distillation as interconnect engineering
│   ├── distributed control across multiple controllers
│   └── modular trapped-ion / multi-chip partitioning
│
├── Architecture, memory and control microarchitecture ............... ~7
│   ├── load/store abstraction and memory hierarchy for FTQC
│   ├── cryostat wiring, multiplexing and pin budget
│   ├── real-time control ISA and feedback speculation
│   └── access-trace analysis / telemetry of FT execution [NEW branch vs Phase 1]
│
├── HPC-centre QPU integration and operations ........................ ~4  ← ISC and QSW only
│   ├── in-situ calibration as an operational procedure
│   ├── telemetry and monitoring in a machine room
│   └── system-topology representation for schedulers and mappers
│
├── Performance modeling and classical-resource estimation ........... ~4
│   ├── classical hardware requirements for large-scale QC
│   └── parallel-scaling-law analysis for quantum algorithms
│
└── Applications and algorithms with HPC implications ................ ~6
```

**Four branches in this corpus were not in the Phase-1 taxonomy and are earned by the evidence:**
compiler **autotuning** (TuniQ), **dynamic-circuit / classical-control compilation** (ISC 2026,
QSW 2026 — the compile-side counterpart of real-time QEC), **distributed compilation** (DC-MBQC,
DisMap), and **observable-measurement / shot orchestration as a runtime service** (ISC 2026).
Conversely, **circuit cutting** — a named Phase-1 branch — is nearly absent here: only QuTracer
(ISCA 2024) and MILQ (ISC 2024) use it, and in both it is a means rather than the contribution.

## 3. Cross-venue branch matrix

Including SC and ASPLOS from the Phase-1 censuses for comparison. Cells are approximate paper counts;
`—` means no paper in that branch at that venue in the censused years.

| Branch | ISC | ISCA | ICS | HPCA | MICRO | QSW | SC (24–25) | ASPLOS (24–26) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Compilation / mapping / synthesis | 3 | 15 | 2 | 8 | 2 | 10 | 3 | 10 |
| QEC as a classical workload | 1 | 6 (+4 FT-arch) | — | 5 | 5 | 1 | **0 decoder papers** (1 QEC *reliability characterization*) | **densest branch, 11 of 36** (of which 2 are decoder microarchitecture) |
| Classical simulation | — | 2 | 4 | 1 | **0** | 3 | 4 | 1 |
| Scheduling / runtime / resource mgmt | 2 | 2 | 1 | — | 1 | 4 | 1 | 1 |
| Multi-QPU / distributed QC | 1 | 2 | — | 2 | 2 | 2 | 1 | 3 |
| Architecture / memory / control | — | 1 | — | 4 | 2 | — | — | several |
| **HPC-centre integration & operations** | **3** | — | — | — | — | **1** | **0** | **0** |
| Performance modeling / resource estimation | 2 | 2 | — | — | — | — | — | — |
| Applications with HPC implications | 1 | 2 | 1 | 1 | 1 | — | 2 | — |

**What the matrix shows.**

1. **Compilation is the universal topic** — every venue, every year, the largest single branch. It is
   the lingua franca of quantum-adjacent systems work, and the one contribution shape that is legible
   everywhere.
2. **QEC as a classical workload is dense at four architecture venues (ASPLOS, ISCA, MICRO, HPCA) and
   essentially absent from the HPC venues.** ISC has exactly one paper, and it is a *resource-
   estimation* paper (Camps et al.) rather than a decoder. ICS has none. **SC has no decoder-systems
   paper in either censused year, but it is not a bare zero** — the Phase-1 SC census records one
   *QEC reliability characterization* paper (SC24's surface-code radiation-event study), and is
   explicit that SC takes QEC reliability characterization but not decoder systems. That qualifier
   must travel with the finding. **The Phase-1 `VENUE_GAP` observation survives contact with four
   more venues** — and is now much better evidenced, because those four venues were the hypothesized
   alternative home and they are indeed where the work is. Note also that the ASPLOS decoder-
   microarchitecture line is itself only two papers (Promatch 2024, Micro Blossom 2025) and, per the
   Phase-1 census, has since moved to ISCA — so "dense at ASPLOS" is true of QEC broadly, not of
   decoder hardware specifically.
3. **Classical simulation is the mirror image:** strong at ICS (4) and SC (4), present at ISCA and
   QSW, and **entirely absent from MICRO in both censused years**. Simulation and QEC decoding are
   the two branches that most sharply separate the HPC pole from the microarchitecture pole.
4. **HPC-centre QPU integration and operations exists only at ISC (3) and QSW (1).** Zero at SC, zero
   at every architecture venue. This is the most venue-exclusive branch in the entire domain.
5. **Scheduling and resource management is thin everywhere** — 0–4 papers per venue, **10 across the
   six venues censused here** (12 including SC's Qonductor and ASPLOS's RESCQ), against 1,281
   screened papers. It is the branch with the largest gap between
   apparent importance to the Quantum-HPC thesis and actual publication volume.

## 4. Venue contribution shapes, tested against the corpus

The Phase-1 expectations were broadly right; three need refinement.

**ISC — confirmed and sharpened.** HPC-centre integration, scientific workflow, system
representation, performance/resource characterization. The refinement: **ISC accepts papers whose
entire contribution is an operational procedure or a software library, with no speedup at all**
(calibration procedure, telemetry architecture, sys-sage extension). That is a materially different
acceptance criterion from every other venue here and is why this branch exists nowhere else.

**ISCA — confirmed, with a datable pivot.** 2024 is entirely single-QPU compilation and error
mitigation; from 2025 the profile becomes architecture-mechanism-transfer: speculation and rollback,
branch prediction, barrier synchronization, switch fabrics, canonical IRs, memory hierarchies. The
recurring shape is **take a classical architecture mechanism and apply it to the quantum control or
correction path**.

**ICS — confirmed, and the most predictive of SC.** ICS accepts quantum work **only when it is shaped
like an existing ICS paper**: a multi-GPU data structure, a memory hierarchy with reuse prediction,
compiler autotuning, communication-avoiding partitioning with portable codegen, a sparse kernel with
SIMD/GPU optimization. Not a machine proposal — a kernel, data structure or scheduling technique
**with measured scaling**.

**HPCA — confirmed, but only from 2025.** The 2024 "non-year" finding holds exactly (1 paper, no
session, and the Best-of-CAL trap inflates it to 2 if not excluded). From 2025 the shape is
architecture-native: load/store abstraction, cache-like reuse, topology/parallelism scaling anomalies,
access-trace side channels, power- and bandwidth-constrained accelerators, and sequential-to-parallel
algorithm restructuring.

**MICRO — confirmed, and the most hardware-proximate.** Control ISAs, distributed synchronization
protocols on real hardware, FPGA decoder accelerators, nanosecond speculation classifiers with LUT
budgets, cryostat wiring. Three of its eleven papers report FPGA resource numbers and one reports
measured real-QPU calibration data — **the highest hardware-evidence rate of the six venues.** And it
publishes **no classical simulation work at all**.

**QSW — new to this project, and the finding is a calibration.** QSW is a quantum *software-
engineering* venue first: **≈58% of its regular papers** are testing, verification, repository mining,
design patterns, reporting methodology, QML applications or usability-focused frameworks with no
systems dimension. A tool that exists is a first-class contribution; several accepted papers report
no speed-up at all. **But the HPC door is explicitly open and widening** — the 2024 CFP already named
"High Performance Computing with Quantum Computers", and 2026 made it structural with dedicated
"Software Systems and Workflows" and "Performance and Reliability" sessions, accepting a GPU QEC
decoder, a QPU job scheduler and a distributed multi-chip compiler as regular papers.

## 5. Answers to the thirteen questions this census had to settle

**1. Where are Quantum-HPC regular papers actually concentrated?**
By absolute volume, **ISCA (33)** dominates, followed by **QSW (20)**, **HPCA (17)**, **ISC (13)**,
**MICRO (11)** and **ICS (8)** — against ASPLOS's 36 and SC's 11 from Phase 1. By density within a
screened population, ISC and QSW lead but on tiny denominators. **The architecture venues
(ASPLOS + ISCA + MICRO + HPCA = 97 papers) hold roughly two-thirds of all Quantum-HPC systems work
in this eight-venue map**, and the HPC venues (SC + ISC + ICS = 32) about a fifth.
*Year-basis caveat:* ASPLOS's 36 is a **program-year** count (14/10/12); its proceedings-year count is
34 (15/8/11). The Phase-1 census is emphatic that the two denominators must never be mixed, and this
aggregate mixes a program-year figure with volume-enumerated counts at the other venues. The
split is immaterial to the two-thirds/one-fifth shape but is declared here rather than hidden.

**2. What contribution shape does each venue require?** §4 above.

**3. How do the HPC, architecture, microarchitecture and software communities differ?**
They differ most sharply on **what counts as evaluation**. The HPC venues want measured scaling on
real machines (C-3PQ on three supercomputers; the DD ring simulator on 256 Wisteria-O nodes). The
architecture venues accept **analytically evaluated machines that do not exist** — ISCA 2025's
transversal-architecture paper budgets 19 million qubits and 5.6 days for RSA-2048. MICRO wants a
hardware artifact or a resource count. QSW wants a usable tool. This is the same four-pathway
acceptance structure the SC census found, observed across four more venues.

**4. Why is QEC decoding concentrated at the architecture community?**
The evidence supports a structural answer rather than a sociological one. Every QEC paper in this
corpus is framed as one of: a **microarchitectural mechanism** (speculation, prediction, pipelining),
a **hardware resource budget** (LUTs, area, 4 K power), or a **scheduling/allocation problem over
fixed hardware**. All three are architecture-venue currencies. Crucially, **no paper in the corpus
frames decoding as a distributed-memory parallel computation with a communication term** — which is
the HPC currency. Triage comes closest, and even it models a decoder *pool* with **zero interconnect
cost**. `[inference]`

**5. What are the crossover conditions under which QEC decoding becomes an HPC problem?**
Two distinct, independently quantified mechanisms — see §6.

**6. In quantum simulation, is the bottleneck memory, compute or communication?**
**Memory, for four of the six simulation papers that were code-cross-validated; communication for the
two that run multi-node.** BMQSim, quEStab, the HPCA Schrödinger accelerator and the MQT identity-
stripping work all attack the memory term on a single device by four different routes (compression,
representation, dataflow, structural elision). Only C-3PQ and the QSW DD ring simulator attack
communication, and they are precisely the two running on production supercomputers.
**Stated with its denominator:** this is 6 of the ~10 simulation papers in the corpus, and one of the
six (the MQT identity-stripping paper) is a QSW boundary-band item outside the 102. The four not
deep-dived — ISCA's Computational Reuse and TUSQ, ICS's Diagonal-Budgeted Trotterization, and the
remaining QSW item — attack *redundant compute* rather than memory, so the ratio would shift if they
were included. The defensible claim is therefore narrower than it first appears: **within the
deep-dived subset, simulation work is predominantly single-device memory engineering rather than
distributed-memory parallelism** — and no paper in the corpus contradicts that, but the corpus-wide
ratio is `INSUFFICIENT_EVIDENCE`.

**7. How mature is multi-GPU / distributed simulation?**
Less than the vocabulary suggests. BMQSim's "multi-GPU" mode has **no inter-GPU communication at all**
and caps at 2.3× on 4 GPUs, PCIe-bound. C-3PQ does weak-scale on Perlmutter, Frontier and Fugaku but
**starts at 4 GPUs for 30 qubits** and never runs single-device, so its speedup claim lacks a
single-device reference point. The QSW DD ring paper is the only one reporting a full strong-scaling
curve — and it is **non-monotonic**, with a 20-qubit workload getting *slower* beyond 64 nodes.
`INSUFFICIENT_EVIDENCE` for any claim that distributed simulation is a solved or saturated area.

**8. Is CPU/GPU/QPU scheduling forming as an independent research branch?**
**Weakly, and it is fragmenting rather than converging.** Twelve papers across eight venues in three
years — ten at the six venues censused here, plus Qonductor (SC 2025) and RESCQ (ASPLOS). The three real schedulers (Qoncord, MILQ, Qonductor) converge on the same abstraction —
a **job × backend cost matrix with per-backend capacity**, i.e. unrelated parallel machines — and
diverge on where the queue lives (simulated, absent-and-replaced-by-setup-times, or a first-class
input vector). **No paper in the corpus models a QPU as a memory hierarchy**, and none integrates
with a real batch system: **Slurm appears nowhere in any scheduler's code or evaluation.** QSW 2026's
qScheduler, with reservation-plus-dispatch, is the closest thing to an HPC-centre batch scheduler in
the entire census — and its artifact URL 404s.

**9. What does multi-QPU / distributed QC actually study today?**
Nine papers, and they are studying **interconnect and partitioning, not programming models**:
switch-network topology (SwitchQNet), entanglement distillation rate as a link-engineering problem,
distributed control-plane synchronization on real hardware (Distributed-HISQ), graph partitioning
with modularity-driven imbalance control plus layer scheduling proved NP-hard (DC-MBQC), and
multi-level zone scheduling (MUSS-TI). **The GPU-cluster ↔ multi-QPU analogy holds well for
partitioning and topology, and poorly for everything else** — there is no analogue of a collective
communication library, no analogue of an MPI-like programming model, and the "network" has a fidelity
dimension classical interconnects do not. `[inference]`

**10. How does NISQ → FTQC change the classical workload?** §7 below.

**11. Where are public artifacts best?**
**HPCA 2026 is the standout**: 3 of its 9 relevant papers ship public code, including the two most
transferable in the corpus (**BP-SF** and **Pinball**). Across the census, confirmed public
code/artifacts: ISCA 5/33, HPCA 6/17, MICRO 5/11, QSW 3/20, ISC 3/13, ICS 2/8 — **24 of 102**, with
many of the remainder `UNKNOWN` rather than searched-and-absent. By branch, **QEC has the best artifact
rate** (SWIPER, Pinball, BP-SF, Coset, gladiator, and — as architecture/scheduling rather than
decoding — Flag-Proxy Networks) and **classical
simulation the worst** — C-3PQ, BMQSim, quEStab and the QSW DD ring simulator **all have no public
artifact**, and the DD paper explicitly promised a URL after review that never appeared. That is a
notable asymmetry: the branch whose results are most reproducible-in-principle publishes the least
code.
**Caveat on quality:** four of the artifacts that do exist were found to be materially incomplete —
Coset's `hardware_code/` is an empty `.gitkeep` despite an FPGA LUT claim; Pinball's repo contains no
power, area or bandwidth model despite headline numbers for all three; SWIPER ships FPGA *results*
but no HDL; Qoncord's headline number is not emitted by any shipped script. **Artifact existence and
claim reproducibility are different properties**, and this census separates them.

**12. Which `OPEN_QUESTION`s are worth a future novelty-falsification pass?** §8 below.

**13. Which venue should be censused next?** §9 below.

## 6. Architecture → HPC crossover analysis

The governing form is `T(P) = W/P + C(P)`: work `W` spread over parallelism `P` plus a
communication/synchronization term `C(P)`. Scale-out helps only while `C(P)` stays under the deadline,
and for real-time QEC the deadline is hard. Two crossover mechanisms are quantified in this corpus,
and **they are not the same thing** — a distinction the domain has been conflating.

**(a) The cryogenic power/bandwidth boundary — quantified only by Pinball.**
Peak power **< 0.56 mW** per predecoder unit, and **up to 2,668 logical qubits at d = 21 under a 1.5 W
4 K power budget**. Since 1.5 W ÷ 0.56 mW ≈ 2,679, the stated figure is essentially the power budget
divided by per-unit power `[inference]`. The consequence is structural: **the cryogenic tier saturates
at a logical-qubit count, not at a code distance.** Past that point one needs a second cryostat or
power domain, and the syndrome stream is **partitioned across physical boundaries by construction** —
which is the point at which a single-accelerator problem becomes a multi-node one whether or not
anyone designed it that way. `POSSIBLE_CROSSOVER`. Note Pinball's O(d²) is per stabilizer basis, so a
full deployment doubles it `[code]`.

**(b) The decoder-pool throughput boundary — quantified only by Triage.**
`τ_dec < τ_gen` must hold or syndrome backlog grows **exponentially**, with decoder latency modelled
`t_decode = A · volume^α`, **α = 1.17**. Because α > 1, per-window volume growth outruns decoder
speed, so **the crossover to a larger pool is driven by the super-linear exponent, not by qubit count
alone** `[inference]`. Triage's `M ≤ N` decoder pool with an independent-set assignment constraint is
already, formally, a distributed-resource-allocation problem.
**`UNDEREXPLORED_IN_THIS_CORPUS`: no paper models inter-decoder network latency.** Decoders are a
pool with zero interconnect cost — exactly the term that would dominate a real distributed deployment.

**(c) Parallelism structure, per decoder family** (full treatment in `DEEPDIVE_QEC_DECODING.md` §C):
- **Windowed/MWPM** (SWIPER, Triage): parallelism is window decomposition; the synchronization term
  is a **DAG of window dependencies** plus Pauli-frame synchronization. SWIPER converts the dependency
  wait into speculation with a tunable rollback blast radius — **that blast radius is the distributed
  communication term**, and it is measured directly.
- **Predecoding** (Pinball): `(d²−1)/2` replicated AND/XOR primitives, **no synchronization term at
  all**. Embarrassingly parallel by construction, bounded by power, not by parallelism.
- **BP-family** (BP-SF, Vegapunk): BP itself is fine-grained and communication-heavy — a poor fit for
  distribution. **BP-SF's contribution sits one level up and is the corpus's best candidate for a
  genuinely distributable decoding workload**: ≤100 fully independent candidate decodes, per-candidate
  payload one syndrome vector, reduction an argmin, only a first-to-finish flag as synchronization
  `[code]`. `POSSIBLE_CROSSOVER`: parallel degree saturates at ~100 workers, beyond which scaling must
  come from batching independent *syndromes*.
- **Union-find/ensemble** (Coset): deliberately trades the parallel axis for area via temporal reuse —
  the opposite of the distributed direction.

**(d) Beyond QEC.** The same question in the other branches:
*Simulation* — see §5 Q6/Q7; the crossover is data-dependent, and the DD ring paper measured it going
**the wrong way** (a 20-qubit workload slowing beyond 64 nodes).
*Compilation* — **`UNDEREXPLORED_IN_THIS_CORPUS`**: all six compile-cost papers measure single-node
compile time, none reports compiler memory footprint, and **none reports parallel or distributed
compilation**, even where the cost is severe (Genesis: 1,152 s for an 1,884-Pauli-string input).
*Measurement/shot orchestration* — ISC 2026's hierarchical runtime is the only paper treating shot
distribution as a load-balancing problem over classical workers.

## 7. NISQ → Early-FTQC → FTQC, and what it does to the classical workload

Regime tags across the 102 papers, approximately: **NISQ ~45, EARLY_FTQC ~12, FTQC ~25,
GENERAL/UNCLEAR ~20**.

The composition shifts visibly by venue and by year. **ISCA 2024 is almost entirely NISQ** (compilation
and error mitigation); **ISCA 2025–2026 is majority FTQC** (decoding, synchronization, magic-state
distillation, lattice surgery, resource analysis). **HPCA 2026's quantum block is predominantly FTQC**;
**MICRO 2025 spans both** (gladiator and LANCER are FT, YOUTIAO and MUSS-TI are NISQ-scale hardware).
**ICS and ISC remain mostly NISQ/GENERAL** — their simulation and compilation work is regime-agnostic.
`OBSERVED_SHIFT` — the per-venue samples are small and the classification is partly `[inference]`.

**What the transition does to the classical side**, as evidenced in this corpus rather than asserted:
- **NISQ** puts the classical load in *compilation and characterization*: pass selection, routing,
  calibration search, noise-model fidelity, shot budgets.
- **FTQC** moves it into a **hard real-time loop**: decoding within a cycle budget (1 µs per round,
  100 ns for leakage classification), syndrome bandwidth across the cryogenic boundary, barrier
  synchronization between logical qubits, and Pauli-frame tracking. **This is a qualitative change in
  the classical requirement, not a quantitative one** — from throughput-oriented batch computation to
  deadline-driven streaming computation.
- The corpus contains **one paper that explicitly re-costs a workload class across the transition** —
  ISCA 2025's *VQAs in the era of Early Fault Tolerance* — and **one that quantifies the classical
  infrastructure needed at FT scale** — ISC 2024's Camps et al. (2–500 Gbps syndrome data, ~1 petaflop
  for real-time decoding, logical clock 100–10,000 Hz). Those two papers, at two different venues,
  are the corpus's only bridges between the regime question and the HPC procurement question.

## 8. `OPEN_QUESTION`s and `POSSIBLE_CROSSOVER`s carried forward

Candidates only. None has been through the `governance/RESEARCH_GAP_RULES.md` pipeline, and none may
be promoted on the strength of this document.

| # | Statement | Status | Evidence pointer |
|---|---|---|---|
| M1 | No paper in the corpus states a syndrome bandwidth in **absolute units (bits/s)** — every bandwidth claim is a ratio. The bandwidth axis of the "QEC decoding is an HPC problem" thesis cannot be quantified from decoder papers alone; the only absolute figure in the domain is ISC 2024's 2–500 Gbps estimate. | `UNDEREXPLORED_IN_THIS_CORPUS` | `DEEPDIVE_QEC_DECODING.md` §A |
| M2 | No decoder paper models **inter-decoder network latency**; Triage's pool has zero interconnect cost. | `UNDEREXPLORED_IN_THIS_CORPUS` | `DEEPDIVE_QEC_DECODING.md` §C |
| M3 | Pinball's 4 K power budget implies the cryogenic tier saturates at a **logical-qubit count** (~2,668 at d = 21, 1.5 W), forcing partition across physical boundaries beyond it. | `POSSIBLE_CROSSOVER` | `DEEPDIVE_QEC_DECODING.md` §C |
| M4 | BP-SF's candidate-level parallelism is bounded at ~100 and untested beyond P = 8; whether the latency reduction continues toward P = 100, and how parallel-vs-serial candidate ordering affects LER, is not evaluated. | `OPEN_QUESTION` | `DEEPDIVE_QEC_DECODING.md` §3 |
| M5 | Whether statevector **compression** (BMQSim) and **inter-node partitioning** (C-3PQ) compose — compressed fragments over GPU-aware MPI — is evaluated by no paper; the two designs each forgo what the other does. | `OPEN_QUESTION` | `DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §D |
| M6 | The DD ring simulator measures distributed scaling **going the wrong way** (20-qubit QCBM slower beyond 64 nodes). What governs the node count at which DD node-sharing loses to communication is not characterized. | `OPEN_QUESTION` | `CENSUS_QSW_2024_2026.md` |
| M7 | **No scheduler in the corpus integrates with a real batch system** — Slurm appears in no scheduler's code or evaluation — and none models a QPU as a memory hierarchy. | `UNDEREXPLORED_IN_THIS_CORPUS` | `DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §C |
| M8 | **No compilation paper reports parallel or distributed compilation or compiler memory footprint**, despite compile costs reaching 1,152 s (Genesis) and despite compilation being named the bottleneck (TuniQ). | `UNDEREXPLORED_IN_THIS_CORPUS` | `DEEPDIVE_SIMULATION_RUNTIME_COMPILATION.md` §B |
| M9 | The Phase-1 `VENUE_GAP` — real-time QEC decoding is dense at architecture venues and absent from HPC main tracks — **now holds across six more venue-years** (ISC 1 resource-estimation paper, ICS 0, SC 0). Still a `VENUE_GAP`, still **not** a research gap. | `VENUE_GAP` (reinforced) | §3 above; `../quantum-hpc-survey/` G1 |
| M10 | HPC-centre QPU integration and operations exists **only at ISC and QSW** across eight venues. | `VENUE_GAP` | §3 above |

## 9. Which venue to census next

1. **MICRO-59 (2026)** — the only *incomplete* item in this census. Re-check when the program
   publishes (late Sept/Oct 2026), including the status of its new **Industry Track**.
2. **IEEE QCE (QSYS + QAPP tracks)** — the Phase-1 queue's designated early-warning sensor, and QSW's
   result strengthens the case: the quantum-software community is where scheduling, workflow and
   orchestration work is landing 12–24 months before the systems venues.
3. **SC 2026** — the target venue; its accepted-paper list closes the largest gap in the map, and the
   topic area is now named "Post-Moore & Quantum Computing".
4. **OSDI / SIGMETRICS** — each owns a branch (quantum OS/virtualization; performance variability)
   that is absent from all six venues censused here.
5. **CGO** — the compilation branch is the largest in this corpus by a wide margin, and CGO is the one
   uncensused venue with two dedicated quantum sessions.

## 10. Temporal trend, stated with its sample caveat

| Signal | 2024 | 2025 | 2026 | Reading |
|---|---|---|---|---|
| Relevant papers (6 venues) | 23 | 41 | 38 + MICRO unknown | `OBSERVED_SHIFT`, not a decline — MICRO-59 is missing from 2026 |
| Dedicated quantum sessions | ISCA 1, MICRO 1 | ISCA 3, HPCA 2, MICRO 2 | ISCA 3, HPCA 2, **ICS 1 (new)** | institutionalizing |
| QEC share of the architecture venues | low | rising | dominant | clearest single trend |
| Regime mix | mostly NISQ | mixed | FTQC-leaning at ISCA/HPCA | `OBSERVED_SHIFT` |
| Simulation papers | 2 | 3 | 5 | concentrated at ICS |
| Scheduling/runtime papers | 3 | 3 | 5 | thin but growing, mostly at QSW |
| Real-QPU / real-device evaluation | rare | rare | rare | **8 of 102 papers** touch real quantum hardware |
| Public artifacts | — | — | — | 25 of 102 confirmed; best at HPCA 2026 |

**The single most robust temporal statement available:** dedicated quantum sessions went from two
venues in 2024 (ISCA, MICRO) to three in 2026 (ISCA, HPCA, ICS) — with MICRO-59 unresolved — and
ICS, the HPC venue closest to SC in community and reviewer overlap, created its first in 2026. **`OBSERVED_SHIFT`**, small samples, no trend extrapolated.

**The single most robust cross-sectional statement:** **only 8 of 102 papers touch real quantum
hardware.** Seven execute on a real QPU — ISC 2024 (superconducting QPU calibration at LRZ), ISC 2025
(telemetry on deployed LRZ systems), ISCA 2024 QuTracer ("noisy simulations and real device
experiments"), HPCA 2025 HATT (IonQ), ICS 2025 OpaQue (IBM Lagos/Toronto/Washington), ICS 2026 TuniQ
(IBM Torino/Fez/Kingston/Pittsburgh) and MICRO 2025 Distributed-HISQ (a 66-qubit superconducting chip
with 110 couplers) — and an eighth, MICRO 2025 YOUTIAO, uses **measured data from self-developed Xmon
chips** to drive a model without running an end-to-end experiment. One more, ISCA 2024's IBM-authored
context-aware compiling paper, is `[inference]` only and is not counted.

Everything else — 94 of 102 — is software simulation, architectural or cycle simulation, RTL
synthesis, or analytic projection. **That is the largest single evidence limitation in this domain**,
and it is a property of the field rather than of this census. Note the distribution: **four of the eight
come from the two HPC venues** (ISC ×2, ICS ×2), which between them account for only 21 of the 102
relevant papers. The venues publishing the most Quantum-HPC papers are the least likely to run on a
quantum computer.

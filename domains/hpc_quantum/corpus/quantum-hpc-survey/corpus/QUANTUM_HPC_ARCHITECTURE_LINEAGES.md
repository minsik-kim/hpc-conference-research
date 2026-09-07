# Quantum-HPC Architecture Research Lineages

**Compiled 2026-09-06 from the ASPLOS 2024–2026 census, cross-referenced against the SC 2024–2025 census and the Phase 1 venue map.**

This document traces how specific research threads move — between problems, between abstraction layers, and between venues. It exists because the ASPLOS census found that **the most informative structure in this field is not the branch taxonomy but the lineage**: who extends whom, where a line stops, and where it goes next.

Evidence tags as in the censuses. `[inference]` marks my reasoning; citation relationships are `[paper-preprint]` unless noted.

---

## 1. QEC decoding — the best-documented lineage, and it leaves ASPLOS

### 1.1 The two opposing design philosophies

```
LINE A — "shrink the problem to fit fixed capacity"     LINE B — "grow the machine with the graph"
Georgia Tech (Qureshi / Das)                            Yale (Zhong)
│                                                       │
├─ LILLIPUT (ASPLOS'22)                                 ├─ Parity Blossom (2023)
│    lookup tables, d=3/5, 29/42 ns                     │    exact MWPM, CPU
│    "tables grow exponentially with the distance"      │
├─ AFS (HPCA'22) — union-find                           ├─ Fusion Blossom (2023)
├─ Astrea / Astrea-G (ISCA'23)                          │    coarse-grained parallelism
│    exact brute force to d=7 in 456 ns                 ├─ Helios (FPGA union-find, same group)
├─ Clique (ISCA'23) — predecoder                        │
▼                                                       ▼
PROMATCH (ASPLOS'24)                                    MICRO BLOSSOM (ASPLOS'25)
predecoder + Astrea-G's fixed exact capacity            O(d³) PUs: one per vertex, one per edge
345 KB monolithic path table                            state distributed into the fabric
RTL_SYNTHESIS, 960 ns allotted MAX @ 250 MHz            FPGA_PROTOTYPE, 800 ns AVERAGE @ 62 MHz
accuracy is a tunable                                   accuracy is exactly MWPM
        │                                                       │
        └──────────────► COLLISION ◄───────────────────────────┘
      Micro Blossom cites Promatch and rejects Line A:
      "their approximation leads to more than 13.9x higher
       logical error rate [at d=13, p=0.1%]"
      — but see the mis-transfer warning in §1.3
```

**The governing ideas are irreconcilable.** Line A holds the machine fixed and shrinks the problem, so progress in code distance costs accuracy. Line B holds accuracy fixed and grows the machine, so progress in code distance costs silicon. **They fail in different currencies, and "which scales better" has no single answer.**

### 1.2 Where the line goes after ASPLOS 2025 — it leaves

`[inference]` on citation evidence from Micro Blossom's ~27 citing works:

```
MICRO BLOSSOM (ASPLOS'25)
   │
   ├─► SWIPER — speculative window decoding ............ ISCA 2025
   ├─► Triage — adaptive parallel window scheduler ..... ISCA 2026
   ├─► Coset Ensemble Decoder — algo/HW co-design ...... ISCA 2026
   ├─► A Case for Elastic QEC Decoders ................. EuroSys 2026
   ├─► Snowflake — distributed streaming decoder ....... Quantum (journal)
   ├─► Network-Integrated Decoding w/ Lattice Surgery ... IEEE QCE 2025
   └─► decoder-bench ................................... IISWC 2025
```

**ASPLOS 2026's five QEC papers contain zero decoder-hardware designs.** They are compiler, synthesis, code-layout and platform-architecture papers. `[proceedings]`

**The accurate statement is therefore not "QEC decoding lives at ASPLOS".** It is: **ASPLOS hosted the decoder-microarchitecture line for exactly two years (2024–2025), after which the successor generation — parallel, windowed, speculative, distributed — went to ISCA and elsewhere, while ASPLOS's own QEC interest migrated one layer up into compile-time synthesis.**

Note the direction of travel: the successor generation is dominated by **parallel/windowed/distributed** concerns. That is the vocabulary of scale-out. `POSSIBLE_CROSSOVER`, and it is happening at ISCA, not at an HPC venue.

### 1.3 A number that must not be repeated without its provenance

Micro Blossom's *"more than 13.9× higher logical error rate"* for Promatch at d=13, p=0.1% is **Promatch's own worst-case figure over its sweep — and that sweep runs p = 10⁻⁴ to 5×10⁻⁴. p = 0.1% = 10⁻³ is outside the range Promatch evaluated.** At Promatch's design point (d=13, p=10⁻⁴), Promatch ‖ Astrea-G reports parity with MWPM. Classification: `DIFFERENT_REGIME`, not `TRUE_CONFLICT`. Promatch's degradation with p is real; the specific d=13/p=0.1% comparison is not a jointly evaluated result. `[paper-preprint]`

### 1.4 The abstraction-layer migration inside ASPLOS QEC

```
2024–2025:  RUNTIME HARDWARE          2026:  COMPILE-TIME SYNTHESIS
  Promatch      — FPGA predecoder       AlphaSyndrome — MCTS scheduling
  Micro Blossom — FPGA accelerator      PropHunt      — MaxSAT optimization
  RESCQ         — runtime scheduler     QECC-Synth    — MaxSAT layout (2025, early)
                                        ACQC          — layout co-design
```

**The deadline pressure did not go away; the response migrated from meeting it with hardware to reducing it at compile time.** `OBSERVED_SHIFT`. Pushing work from a microsecond-deadline runtime into an hours-long offline search is a way of *avoiding* the scale-out question rather than answering it. `[inference]`

### 1.5 A silent algorithm-class change

```
2024: surface code only        →  2025: qLDPC arrives      →  2026: majority qLDPC
      (Promatch, chiplet)          (HetEC gross code)          (ACQC, AlphaSyndrome, PropHunt)
      decoder = MATCHING           ...                          decoder = BELIEF PROPAGATION
```

Matching (blossom, union-find) and belief propagation have **different parallel structures**: blossom builds dynamic forests with an irregular serial residue; BP is bulk-synchronous message passing over a sparse factor graph, which maps far more naturally onto conventional parallel machines — **but is iterative with data-dependent convergence, converting bounded work into unbounded iterations.**

**None of the four qLDPC papers in the ASPLOS corpus analyses the resulting real-time decoder cost.** HetEC in particular adopts the gross code and abstracts decoding into a fixed "logical clock speed". `OPEN_QUESTION`.

### 1.6 The non-connection worth noting

The chiplet-codesign paper's **super-stabilizers deform the matching graph**, which is a direct input to any MWPM decoder's cost model. Neither the decoder line nor the code-layout line cites the other. `[inference]` This is the most conspicuous missing edge in the lineage graph.

---

## 2. Quantum simulation — the venue-split lineage

```
                        CPU / single-node
                               │
                ┌──────────────┴───────────────┐
                ▼                              ▼
        DEVICE-CENTRIC (ASPLOS)        SCALE-CENTRIC (SC)
                │                              │
        BQSim (ASPLOS'25)              Atlas (SC24)
        1 GPU, decision diagrams       256 GPUs on Perlmutter
        batching across circuits       ILP staging, local/regional/global qubits
        contribution = data structure  NCCL all-to-all, Legion DRAM offload
        + memory system                contribution = communication minimization
                                              │
                                       PTSBE (SC25)
                                       4×H100, 6,668 GPU-hours
                                       trajectory batching
                                       upstreamed into CUDA-Q
```

**The same class of contribution, framed by two different scarcities.** BQSim's scarce resource is **device memory and DD irregularity**; Atlas's is **inter-node communication**. Communication does not appear in BQSim's argument at all; the memory hierarchy does not appear in Atlas's headline. `[inference]`

**Population asymmetry:** simulation is SC's largest branch (4 of 11) and ASPLOS's smallest (1 of 36). This is the exact mirror image of the QEC asymmetry (ASPLOS 11 of 36; SC 1 of 11, and that one a *reliability characterization* rather than a decoder). **The two venues have complementary, near-disjoint quantum portfolios.** `VENUE_GAP` in both directions.

---

## 3. Compilation — three parallel lineages, and a venue-shaped divide

### 3.1 By research group

```
YUFEI DING (UCSD, + Cisco / PNNL / ORNL)
  MECH (24, chiplet interconnect) ─┐
  OnePerc (24, photonic) ──────────┼─► PowerMove (25→26, neutral atom, zoned)
  QECC-Synth (25, QEC layout) ─────┘   iSwitch (26, ion trap)
  Agenda: compilers for the platforms that are NOT superconducting circuits, each defined by
  one exotic physical constraint. Method constant: graph algorithms and greedy heuristics,
  never solvers; a layered pass structure with an explicit IR; simulator-only evaluation.

GUSHU LI (Penn, + AWS / LBNL)
  Fermihedral (24, fermion-to-qubit, SAT) ─► QTurbo (26, analog) ─► AlphaSyndrome (26, QEC MCTS)
  Agenda: moves from introducing solvers to escaping them. Fermihedral ADDS a SAT solver and
  pays for it; QTurbo REMOVES a monolithic solve and reports 600x. National-lab co-authorship
  (LBNL/Iancu) throughout.

SWAMIT TANNU (Wisconsin, + Albarghouthi)
  GUOQ (25, anytime optimizer) ─► Reducing T Gates / trasyn (26) ─► PropHunt (26, MaxSAT QEC)
  Agenda: optimization quality under a fixed budget. GUOQ's design choice — hold compile time
  at one hour and compare output — is the corpus's clearest statement of that philosophy.

ALIBABA DAMO
  One Gate Scheme / AshN (24) ─► ReQISC (26)
  Agenda: instruction-set design for quantum. No cost model in either paper.

SEOUL NATIONAL UNIVERSITY (Jangwoo Kim, HPCS Lab)
  Million Qubit-Scale Distributed QC (24) ─► ACQC (26, qLDPC)
  Agenda: full-machine architecture at 10^7+ physical qubits. Both abstract-only from here;
  neither has a public artifact.
```

### 3.2 The venue-shaped divide — the census's sharpest quantitative result

```
                  COMPILE-TIME SCALABILITY AS THE CENTRAL ARGUMENT
     SC:  ███████████████████████████████████████████████  3 / 3
 ASPLOS:  ██████████                                       2 / 10
```

SC's incumbents fail measurably — SATMAP at 2 hours, DPQA at 24 hours — and that failure *is* the problem statement. ASPLOS's ten compilation papers argue, in the majority, **output quality** or a **different cost model entirely**:

| Cost model | Papers |
|---|---|
| Compile time (SC-shaped) | QTurbo, PowerMove |
| Compile time, secondary | trasyn |
| Output quality only | GUOQ, ReQISC, AshN, Fermihedral |
| **QPU executions / shots** | MorphQPV (9.3×10⁵ → 8,974 executions) |
| **Hard real-time execution latency** | OnePerc (online pass must fit a ~5,000-cycle photon lifetime) |
| **Verification time** | Borrowing Dirty Qubits |

**Two structural observations.**
1. **Fermihedral is the inversion of the SC pattern.** SC: an exact solver exists, it times out, replace it. Fermihedral: closed-form constructions exist and are free but give poor output, so *introduce* a SAT solver and pay for it. **In SC's terms, Fermihedral is the paper SATMAP would have been.**
2. **The venues converge exactly where the hardware is analog and continuous** — QTurbo on QuEra Aquila, PowerMove on atom movement. There the compiler output is a schedule over continuous parameters, the search is genuinely large, and the argument reverts to SC's shape. `[inference]`

### 3.3 OnePerc's deadline — a compiler with a decoder's problem

OnePerc's online pass must complete inside a photon lifetime (~5,000 RSG cycles at ~1 ns each). **This is structurally the QEC decoder's deadline constraint, applied to the online half of a compiler.** It is the only place in the ASPLOS corpus where a compilation problem and a decoding problem share a cost model, and neither literature cites the other. `[inference]`

---

## 4. Modular / multi-QPU — the natively distributed lineage

```
MECH (ASPLOS'24) ──────────► COMPAS (ASPLOS'26)
inter-chiplet communication    distributed multi-party SWAP test
"highway" with multiple entries teledata vs telegate methods
                                      │
Million Qubit-Scale (ASPLOS'24) ──────┤
distributed FT machine, 10^7 qubits   │
                                      ▼
                          SC24: DQTetris — inter-module
                          communication minimization (compilation only)
```

**This is the one branch whose vocabulary already matches HPC's** — modules, interconnect, communication cost, partitioning under capacity constraints. DQTetris (SC 2025) is structurally the adaptive-mesh-refinement repartitioning problem in different clothing: partition under capacity constraints over a time-evolving interaction graph, minimizing migrations rather than cuts.

**Both venues are thin here** (ASPLOS 3, SC 1). `VENUE_GAP` in both. `POSSIBLE_CROSSOVER`: the branch is natively distributed, so scale-out requires no reframing — only more modules than one fabric spans.

---

## 5. Cross-lineage summary — where each thread currently sits

| Lineage | Current venue home | Evidence level | Artifact culture | Crossover status |
|---|---|---|---|---|
| **QEC decoder microarchitecture** | **Left ASPLOS after 2025 → ISCA** | `FPGA_PROTOTYPE` (best case) | 5/5 have artifacts; **1 has HDL** | `POSSIBLE_CROSSOVER` at d ≥ 21–27 or lattice-surgery fusion; blocked by a ~1 µs budget |
| **QEC compile-time synthesis** | ASPLOS 2026 | `SOFTWARE_SIMULATION` | good | Avoids the scale-out question by construction |
| **QEC system architecture** | ASPLOS, all three years | `ANALYTIC_MODEL` / `ARCH_SIMULATION` | **0/7 artifacts** | Already at HPC scale in assumptions; the gap is in evaluation methodology |
| **Quantum simulation** | **SC** (multi-node) / ASPLOS (single device) | `REAL_HARDWARE` (classical) | strong at both | **Already crossed** — SC is the multi-node form |
| **Compilation** | Both, with different cost models | `SOFTWARE_SIMULATION` mostly | 8/12 | Search is parallelizable; **no paper reports a parallel-efficiency study of its own compiler** |
| **Modular / multi-QPU** | ASPLOS (architecture), SC (compilation) | mixed | mixed | Natively distributed; vocabulary already matches |
| **NISQ applications** | ASPLOS 2024, collapsing by 2026 | `REAL_HARDWARE` (small QPUs) | 9/12 | Not a scale-out branch |

---

## 6. The three questions these lineages leave open

Stated as `OPEN_QUESTION` — none is a claim, and none asserts that anyone has failed to address it.

1. **What is the real-time decoder cost of the qLDPC turn?** The code family moved from surface codes to qLDPC across 2024–2026, which changes the decoder algorithm class from matching to belief propagation. Four ASPLOS papers make that move; none models the resulting decoder cost, and HetEC explicitly abstracts it into a fixed logical clock speed.
2. **Is decoding an architecture problem, or a superconducting-modality problem?** Every decoder paper anchors to a 1 µs superconducting cycle. Trapped-ion measurement at 400 µs (Jones & Murali, same corpus) is a ~400× budget expansion under which exact MWPM at d=13 fits comfortably in software. No paper in the corpus makes this comparison.
3. **Is the Terabit/s syndrome data plane a placement problem or a network problem?** Micro Blossom names the requirement; no paper in the corpus addresses decoder placement, and Promatch does not mention the cryostat.
